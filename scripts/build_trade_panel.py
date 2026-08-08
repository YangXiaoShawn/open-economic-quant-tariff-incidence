#!/usr/bin/env python
"""Build the product x country x month analytical panel.

Uses official Census data when ``CENSUS_API_KEY`` is set. Otherwise falls back to
the documented synthetic generator so the pipeline stays testable, and tags every
downstream artefact ``SYNTHETIC_PIPELINE_VALIDATION`` so no number produced from
it can be mistaken for an empirical finding.

    python scripts/build_trade_panel.py [--force-synthetic] [--n-treated 40]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl  # noqa: E402

from tariff_incidence.adapters import (
    census_trade,  # noqa: E402
    usitc_hts,  # noqa: E402
)
from tariff_incidence.adapters.base import SourceUnavailable  # noqa: E402
from tariff_incidence.config import load_config  # noqa: E402
from tariff_incidence.manifest import DatasetManifest  # noqa: E402
from tariff_incidence.panel.build import (  # noqa: E402
    ambiguity_report,
    build_panel,
    month_average_additional_rate,
)
from tariff_incidence.panel.synthetic import (  # noqa: E402
    GroundTruth,
    SyntheticSpec,
    generate,
    write_ground_truth,
)
from tariff_incidence.paths import ensure_layers, layer_path  # noqa: E402
from tariff_incidence.provenance import DataProvenance, RunStamp  # noqa: E402
from tariff_incidence.tariff.engine import TariffEngine  # noqa: E402
from tariff_incidence.tariff.schedule import frame_to_records  # noqa: E402

COUNTRY_NAMES = {
    "5700": "China",
    "5520": "Vietnam",
    "5490": "Thailand",
    "5590": "Malaysia",
    "5330": "India",
    "5800": "Korea, South",
    "5880": "Taiwan",
    "2010": "Mexico",
    "1220": "Canada",
}


def select_products(
    engine: TariffEngine,
    hs6_children: dict[str, list[str]],
    chapters: list[str],
    country: str,
    n_treated: int,
    n_control: int,
    restrict_to_action: str | None = "SEC301_LIST3",
) -> tuple[list[str], list[str], list[str]]:
    """Split HS6 headings in the sampled chapters into treated / control / ambiguous.

    Assignment is made by the tariff engine, so the split reflects the same legal
    logic used everywhere else.

    The treated group is restricted to headings covered **only** by the single
    action named in ``restrict_to_action``. Mixing waves would give the panel
    staggered adoption, and two-way fixed effects with staggered adoption uses
    already-treated units as controls, which is not the estimand claimed here. A
    stacked design is the right tool for the multi-wave version and is listed as
    the next iteration in the project plan.

    Headings with partial coverage go to neither group: assigning a
    coverage-weighted rate to a partly covered HS6 heading would invent
    precision the law does not have.
    """
    as_of = date(2018, 10, 1)
    treated, control, ambiguous = [], [], []
    for hs6 in sorted(hs6_children):
        if hs6[:2] not in chapters:
            continue
        a = engine.assess(hs6, country, as_of)
        if a.coverage_share >= 0.999 and a.is_treated:
            if restrict_to_action is None or a.active_action_ids == (restrict_to_action,):
                treated.append(hs6)
            else:
                ambiguous.append(hs6)  # treated, but by a different or multiple waves
        elif a.coverage_share == 0.0:
            control.append(hs6)
        else:
            ambiguous.append(hs6)
    rng_treated = treated[:: max(len(treated) // n_treated, 1)][:n_treated]
    rng_control = control[:: max(len(control) // n_control, 1)][:n_control]
    return rng_treated, rng_control, ambiguous


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="sample_slice.yaml")
    ap.add_argument("--force-synthetic", action="store_true")
    ap.add_argument("--n-treated", type=int, default=45)
    ap.add_argument("--n-control", type=int, default=45)
    args = ap.parse_args()

    ensure_layers()
    cfg = load_config(args.config)
    sample = cfg.sample

    sched = pl.read_parquet(layer_path("normalized", "tariff_schedule.parquet"))
    records = frame_to_records(sched)
    print(f"tariff schedule: {len(records):,} records")

    # HS6 -> HS8 children and MFN baselines from the USITC HTS.
    try:
        hts_lines = usitc_hts.load_chapters(sample.hs2_chapters)
        children = usitc_hts.hs6_children(hts_lines)
        baseline = usitc_hts.baseline_source(hts_lines, 2018)
        hts_ok = True
        print(f"USITC HTS: {len(hts_lines):,} 8-digit lines, {len(children):,} HS6 headings, "
              f"{len(baseline):,} MFN ad valorem rates")
    except SourceUnavailable as exc:
        print(f"! USITC HTS unavailable ({exc}); HS6 coverage will use schedule-only denominators")
        children, baseline, hts_lines, hts_ok = {}, None, [], False

    engine = TariffEngine(records, baseline=baseline, hs6_children=children)

    treated, control, ambiguous = select_products(
        engine, children, sample.hs2_chapters, sample.treated_country_code,
        args.n_treated, args.n_control,
    )
    print(
        f"product split in chapters {sample.hs2_chapters}: "
        f"{len(treated)} treated / {len(control)} control sampled; "
        f"{len(ambiguous):,} HS6 headings have partial coverage and are excluded from both"
    )

    countries = [sample.treated_country_code, *sample.comparison_country_codes]

    # ---- data source selection ------------------------------------------
    use_census = census_trade.available() and not args.force_synthetic
    if use_census:
        valid, unknown = census_trade.verify_schema(census_trade.DEFAULT_VARIABLES)
        if unknown:
            print(f"! Census schema changed; unknown variables: {unknown}")
        print(f"Census API key detected; fetching {sample.start_month}..{sample.end_month}")
        paths = census_trade.fetch_range(
            sample.start_month,
            sample.end_month,
            commodities=treated + control,
            countries=countries,
            commodity_level="HS6",
            max_calls=sample.max_api_calls,
        )
        staged = pl.concat([pl.read_parquet(p) for p in paths], how="diagonal_relaxed")
        staged = staged.rename(
            {v: v.lower() for v in staged.columns if v.upper() == v}
        ).rename({"i_commodity": "hs6", "cty_code": "country_code", "cty_name": "country_name"},
                 strict=False)
        provenance = DataProvenance.OFFICIAL
        truth = None
        source_desc = "U.S. Census Bureau timeseries/intltrade/imports/hs"
        source_url = census_trade.BASE
    else:
        why = (
            "forced by --force-synthetic"
            if args.force_synthetic
            else f"{census_trade.KEY_ENV} is not set ({census_trade.KEY_SIGNUP})"
        )
        print(f"\n*** SYNTHETIC MODE: {why}")
        print("*** Estimates from this panel validate the code, not the world.\n")

        # The generator's rate path comes from the tariff engine itself, month by
        # month, so the data-generating process and the estimation panel cannot
        # disagree about timing or about which action covers a product.
        months = list(census_trade.iter_months(sample.start_month, sample.end_month))
        rate_sched: dict[str, dict[str, float]] = {}
        eff: dict[str, str] = {}
        for p in treated:
            path = {}
            for y, m in months:
                r = month_average_additional_rate(
                    engine, p, sample.treated_country_code, date(y, m, 1)
                )
                if r > 0:
                    path[f"{y:04d}-{m:02d}"] = r
            rate_sched[p] = path
            first = min(path) if path else None
            eff[p] = f"{first}-01" if first else ""
        eff = {k: v for k, v in eff.items() if v}

        mfn = {}
        for p in treated + control:
            a = engine.assess(p, sample.treated_country_code, date(2018, 1, 1))
            mfn[p] = a.baseline_rate if a.baseline_rate is not None else 0.0

        spec = SyntheticSpec(
            hs6_treated=treated,
            hs6_control=control,
            countries={c: COUNTRY_NAMES.get(c, c) for c in countries},
            alternative_supplier_codes=[c for c in countries if c != sample.treated_country_code],
            treated_country_code=sample.treated_country_code,
            start_month=sample.start_month,
            end_month=sample.end_month,
            treatment_effective=eff,
            baseline_mfn=mfn,
            additional_rate_schedule=rate_sched,
            ground_truth=GroundTruth(),
        )
        staged, truth = generate(spec)
        provenance = DataProvenance.MIXED
        source_desc = (
            "SYNTHETIC generator (tariff_incidence.panel.synthetic) + OFFICIAL tariff schedule "
            "and OFFICIAL USITC HTS baselines"
        )
        source_url = "n/a (locally generated)"
        write_ground_truth(truth, layer_path("analytical", "synthetic_ground_truth.json"))

    staged_path = layer_path("staged", "trade_staged.parquet")
    staged.write_parquet(staged_path)

    # ---- build the analytical panel --------------------------------------
    panel = build_panel(
        staged,
        engine,
        treated_country_code=sample.treated_country_code,
        pre_period_end=date(2018, 6, 30),
    )
    # No silent null-filling of tariff variables. A null baseline means the HS6
    # heading contains at least one 8-digit line whose column-1 general rate is
    # compound or specific, so no single ad valorem rate exists for it. Filling
    # that with zero would assert a fact the tariff schedule does not support and
    # would attenuate every estimate that uses the total rate.
    panel = panel.with_columns(
        pl.col("total_modeled_tariff_rate").is_not_null().alias("baseline_mfn_available"),
        (1.0 + pl.col("total_modeled_tariff_rate")).log().alias("log1p_total_tariff"),
        (1.0 + pl.col("additional_tariff_rate")).log().alias("log1p_additional_tariff"),
        pl.concat_str([pl.col("hs6"), pl.col("country_code")], separator="_").alias("flow_id"),
        pl.col("month_date").dt.strftime("%Y-%m").alias("month_key"),
    )
    n_no_base = int((~panel["baseline_mfn_available"]).sum())
    print(
        f"  MFN baseline unavailable for {n_no_base:,} of {panel.height:,} rows "
        f"({n_no_base / panel.height:.1%}): HS6 headings containing compound or specific duty "
        "lines. These rows keep a null total rate and drop out of total-rate specifications; "
        "the additional-duty specification is unaffected."
    )

    out = layer_path("analytical", "trade_panel.parquet")
    panel.write_parquet(out)

    amb = ambiguity_report(panel)
    amb.write_parquet(layer_path("analytical", "tariff_assessment_status.parquet"))

    stamp = RunStamp.create(
        config_name=cfg.config_name,
        config_bytes=cfg.raw_bytes,
        data_provenance=provenance,
        data_period_start=sample.start_month,
        data_period_end=sample.end_month,
        notes=source_desc,
    )
    stamp.write(layer_path("analytical", "trade_panel.runstamp.json"))

    DatasetManifest.for_file(
        out,
        dataset_id="trade_panel_hs6_country_month",
        layer="analytical",
        source=source_desc,
        source_url=source_url,
        source_release_or_vintage=("Census live API" if use_census else "synthetic v1"),
        schema_version="panel_v1",
        transformation_version="build_trade_panel.py@v1",
        row_count=panel.height,
        data_provenance=provenance,
        product_code_vintage="HTS2018",
        date_range=(sample.start_month, sample.end_month),
        partition_keys=["hs6", "country_code", "month_date"],
        known_limitations=(
            [
                "Customs unit values are value/quantity over heterogeneous transactions; they are "
                "not transaction prices and move with product mix and quality.",
                "HS6 aggregation loses the HS8 level at which Section 301 lists are written; "
                "partially covered headings are excluded from both treatment groups.",
                "Sample ends 2019-08 to avoid List 4A contamination of the control group.",
            ]
            + (
                []
                if use_census
                else [
                    "TRADE FLOWS ARE SYNTHETIC. No estimate from this panel is an empirical "
                    "finding about U.S. trade. Set CENSUS_API_KEY to rebuild with official data."
                ]
            )
        ),
        columns={c: str(t) for c, t in zip(panel.columns, panel.dtypes, strict=True)},
        extra={
            "n_treated_products": len(treated),
            "n_control_products": len(control),
            "n_ambiguous_hs6_excluded": len(ambiguous),
            "countries": countries,
            "hts_available": hts_ok,
            "synthetic_ground_truth": (truth or {}).get("parameters") if truth else None,
        },
    ).write()

    print(f"\nwrote {out}")
    print(f"  rows={panel.height:,}  products={panel['hs6'].n_unique()}  "
          f"countries={panel['country_code'].n_unique()}  months={panel['month_date'].n_unique()}")
    print(f"  provenance={provenance.value}  run_id={stamp.run_id}")
    print("\ntariff assessment status:")
    print(amb)

    with (layer_path("analytical", "product_groups.json")).open("w") as fh:
        json.dump(
            {"treated": treated, "control": control, "ambiguous_excluded": ambiguous},
            fh,
            indent=2,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
