#!/usr/bin/env python
"""Map product-level tariff exposure into U.S. industries via BEA input-output tables.

    python scripts/build_io_exposure.py [--year 2017]

Produces the four exposure channels separately. Protection and imported-input
cost are never combined into a single number.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl  # noqa: E402
import yaml  # noqa: E402

from tariff_incidence.adapters import bea_io  # noqa: E402
from tariff_incidence.adapters.base import SourceUnavailable  # noqa: E402
from tariff_incidence.config import load_config  # noqa: E402
from tariff_incidence.io_exposure.exposure import (  # noqa: E402
    build_exposures,
    commodity_tariff_exposure,
    summarize,
)
from tariff_incidence.manifest import DatasetManifest  # noqa: E402
from tariff_incidence.paths import CONFIG, ensure_layers, layer_path  # noqa: E402
from tariff_incidence.provenance import DataProvenance, RunStamp  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="sample_slice.yaml")
    ap.add_argument("--year", type=int, default=2017, help="pre-treatment IO table year")
    args = ap.parse_args()
    ensure_layers()

    cfg = load_config(args.config)
    conc = yaml.safe_load((CONFIG / "io_concordance.yaml").read_bytes())
    hs2_map: dict[str, str] = conc["hs2_to_bea_commodity"]

    panel = pl.read_parquet(layer_path("analytical", "trade_panel.parquet"))
    trade_prov = DataProvenance(
        json.loads((layer_path("analytical", "trade_panel.runstamp.json")).read_text())[
            "data_provenance"
        ]
    )

    try:
        tables = bea_io.load_tables(args.year)
    except (SourceUnavailable, ValueError, KeyError) as exc:
        print(f"BEA input-output tables unavailable: {exc}")
        print("Cannot build industry exposure without them. Nothing written.")
        return 1

    print(
        f"BEA {args.year} summary tables: "
        f"{tables.direct_requirements['industry_code'].n_unique()} industries, "
        f"{tables.direct_requirements['commodity_code'].n_unique()} commodities, "
        f"{tables.total_requirements.height:,} total-requirement cells"
    )

    hs_to_commodity = {
        hs6: hs2_map[hs6[:2]]
        for hs6 in panel["hs6"].unique().to_list()
        if hs6[:2] in hs2_map
    }

    # Pre-treatment weight window ends the month before the first action takes
    # effect, so exposure weights cannot respond to the tariff.
    first_treated = panel.filter(pl.col("treated"))["month_index"].min()
    pre_idx = (
        int(first_treated) - 1 if first_treated is not None else int(panel["month_index"].max())
    )
    ce, quality = commodity_tariff_exposure(
        panel, hs_to_commodity, pre_period_end_month_index=pre_idx
    )
    print(
        f"commodity exposure: {ce.height} BEA commodities from "
        f"{quality.n_mapped_products} mapped products "
        f"({quality.n_unmapped_products} unmapped)"
    )

    exposure = build_exposures(
        ce, tables.direct_requirements, tables.total_requirements
    ).with_columns(
        pl.col("industry_code")
        .replace_strict(tables.industry_names, default=None)
        .alias("industry_name"),
        pl.lit(conc["status"]).alias("concordance_status"),
    )

    stamp = RunStamp.create(
        config_name=cfg.config_name,
        config_bytes=cfg.raw_bytes,
        data_provenance=(
            DataProvenance.OFFICIAL
            if trade_prov is DataProvenance.OFFICIAL
            else DataProvenance.MIXED
        ),
        data_period_start=str(args.year),
        data_period_end=str(args.year),
        notes=f"BEA {args.year} summary IO; concordance status {conc['status']}",
    )
    out = layer_path("results", "industry_tariff_exposure.parquet")
    exposure.with_columns(
        pl.lit(stamp.run_id).alias("run_id"),
        pl.lit(stamp.git_commit).alias("git_commit"),
        pl.lit(stamp.data_provenance.value).alias("data_provenance"),
    ).write_parquet(out)
    ce.write_parquet(layer_path("results", "commodity_tariff_exposure.parquet"))
    summarize(exposure).write_parquet(layer_path("results", "industry_exposure_summary.parquet"))
    stamp.write(layer_path("results", "io_exposure.runstamp.json"))

    (layer_path("results", "io_exposure_quality.json")).write_text(
        json.dumps({"run": stamp.to_dict(), "concordance": quality.to_row(),
                    "concordance_config_status": conc["status"]}, indent=2, default=str) + "\n"
    )

    DatasetManifest.for_file(
        out,
        dataset_id="industry_tariff_exposure",
        layer="results",
        source=f"BEA Supply-Use summary tables {args.year} + project tariff schedule",
        source_url=bea_io.BEA_ZIP_URL,
        source_release_or_vintage=tables.source_release,
        schema_version="io_exposure_v1",
        transformation_version="build_io_exposure.py@v1",
        row_count=exposure.height,
        data_provenance=stamp.data_provenance,
        date_range=(str(args.year), str(args.year)),
        known_limitations=[
            quality.aggregation_loss_note,
            f"HS-to-commodity concordance status: {conc['status']}. Exposure magnitudes are "
            "an ordering, not elasticities, and must not feed a welfare calculation.",
            "Direct requirements are normalised by the intermediate-input column total, not by "
            "total industry output including value added, so shares are input shares of "
            "intermediate purchases.",
        ],
        columns={c: str(t) for c, t in zip(exposure.columns, exposure.dtypes, strict=True)},
    ).write()

    print("\nexposure classes:")
    print(summarize(exposure))
    both = exposure.filter(pl.col("exposure_class") == "BOTH_PROTECTED_AND_COST_EXPOSED")
    print(f"\nindustries exposed through BOTH channels: {both.height}")
    print(
        both.select(
            ["industry_code", "industry_name", "output_protection_exposure",
             "imported_input_cost_exposure", "downstream_total_requirements_exposure"]
        ).head(12)
    )
    print("\ntop imported-input cost exposure:")
    print(
        exposure.select(
            ["industry_code", "industry_name", "imported_input_cost_exposure",
             "output_protection_exposure", "exposure_class"]
        ).head(12)
    )
    print(f"\nwrote {out} (run_id={stamp.run_id})")
    print(f"NOTE: concordance status is {conc['status']}; see config/io_concordance.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
