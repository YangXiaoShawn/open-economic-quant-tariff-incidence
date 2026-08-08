#!/usr/bin/env python
"""Trade-diversion decomposition and descriptive sourcing analysis.

    python scripts/estimate_diversion.py

Separates the contraction in imports from the treated country from any expansion
by third countries, on intensive and extensive margins, and never nets the two.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl  # noqa: E402

from tariff_incidence.config import load_config  # noqa: E402
from tariff_incidence.econ.diversion import (  # noqa: E402
    counterfactual_adjusted,
    country_gains,
    decompose,
)
from tariff_incidence.paths import ensure_layers, layer_path  # noqa: E402
from tariff_incidence.provenance import DataProvenance, RunStamp  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="sample_slice.yaml")
    args = ap.parse_args()
    ensure_layers()

    cfg = load_config(args.config)
    panel = pl.read_parquet(layer_path("analytical", "trade_panel.parquet"))
    provenance = DataProvenance(
        json.loads((layer_path("analytical", "trade_panel.runstamp.json")).read_text())[
            "data_provenance"
        ]
    )
    stamp = RunStamp.create(
        config_name=cfg.config_name,
        config_bytes=cfg.raw_bytes,
        data_provenance=provenance,
        data_period_start=cfg.sample.start_month,
        data_period_end=cfg.sample.end_month,
    )
    print(stamp.banner())

    treated_country = cfg.sample.treated_country_code
    pre = (-cfg.estimation.event_window_pre, -1)
    post = (1, cfg.estimation.event_window_post)

    # Only ever-treated products have an event time; the decomposition is about
    # what happened to the products the policy actually targeted.
    treated_products = panel.filter(pl.col("ever_treated_product"))

    by_product, totals = decompose(
        treated_products,
        treated_country_code=treated_country,
        pre_window=pre,
        post_window=post,
    )
    gains = country_gains(
        treated_products,
        treated_country_code=treated_country,
        pre_window=pre,
        post_window=post,
    )

    def _w(df: pl.DataFrame, name: str) -> None:
        df.with_columns(
            pl.lit(stamp.run_id).alias("run_id"),
            pl.lit(stamp.git_commit).alias("git_commit"),
            pl.lit(stamp.data_provenance.value).alias("data_provenance"),
            pl.lit(f"{stamp.data_period_start}..{stamp.data_period_end}").alias("data_period"),
        ).write_parquet(layer_path("results", f"{name}.parquet"))

    _w(by_product, "diversion_by_product")
    _w(totals, "diversion_totals")
    _w(gains, "diversion_country_gains")

    t = totals.row(0, named=True)
    print("Decomposition of the pre-to-post change in average monthly customs value")
    print(f"  window: event months {pre[0]}..{pre[1]} vs {post[0]}..{post[1]}")
    print(f"  treated-country intensive     {t['treated_intensive']:>18,.0f}")
    print(f"  treated-country extensive     {t['treated_extensive']:>18,.0f}")
    print(f"  treated-country TOTAL         {t['treated_total']:>18,.0f}  "
          f"({t['treated_pct_change']:.1%} of pre-period treated value)")
    print(f"  alternative-source intensive  {t['alternative_intensive']:>18,.0f}")
    print(f"  alternative-source extensive  {t['alternative_extensive']:>18,.0f}")
    print(f"  alternative-source TOTAL      {t['alternative_total']:>18,.0f}")
    print(f"  NET change in total imports   {t['total_change']:>18,.0f}")
    rr = t["replacement_ratio"]
    print(f"  replacement ratio             {rr:.3f}" if rr is not None else
          "  replacement ratio             n/a (treated-country value did not fall)")
    print(f"  treated flows that exited     {t['n_treated_flows_exited']}")
    print(f"  alt suppliers entered/exited  {t['n_alt_suppliers_entered']}/{t['n_alt_suppliers_exited']}")

    print("\nBy partner country (average monthly customs value):")
    print(gains.select(["country_code", "pre_monthly_value", "post_monthly_value",
                        "change", "pct_change", "share_change"]))

    # Counterfactual-adjusted decomposition (difference-in-differences version).
    adj, adj_summary = counterfactual_adjusted(
        panel,
        treated_country_code=treated_country,
        pre_window=pre,
        post_window=post,
    )
    if adj.height:
        _w(adj, "diversion_counterfactual_adjusted")
        print("\nCounterfactual-adjusted (net of never-treated product growth):")
        print(adj.select(["country_code", "pre_monthly_value", "post_monthly_value",
                          "counterfactual_post_value", "excess_change",
                          "excess_pct_vs_counterfactual", "control_growth_factor"]))
        print(f"  treated-country excess change      {adj_summary['treated_country_excess_change']:>16,.0f}")
        print(f"  alternative-countries excess change{adj_summary['alternative_countries_excess_change']:>16,.0f}")
        arr = adj_summary["adjusted_replacement_ratio"]
        print(f"  adjusted replacement ratio         {arr:>16.3f}" if arr is not None
              else "  adjusted replacement ratio         n/a")
        print(
            "  NOTE: the raw ratio above is inflated by ordinary trade growth; the adjusted "
            "figure is the one to read."
        )

    # Heterogeneity by pre-treatment dependence on the treated country.
    dep = (
        treated_products.select(["hs6", "pretreatment_treated_country_share"])
        .unique()
        .join(by_product, on="hs6", how="inner")
    )
    med = dep["pretreatment_treated_country_share"].median()
    het = (
        dep.with_columns(
            pl.when(pl.col("pretreatment_treated_country_share") > med)
            .then(pl.lit("high_dependence"))
            .otherwise(pl.lit("low_dependence"))
            .alias("dependence_group")
        )
        .group_by("dependence_group")
        .agg(
            pl.len().alias("n_products"),
            pl.col("treated_total").sum().alias("treated_change"),
            pl.col("alternative_total").sum().alias("alternative_change"),
            pl.col("pre_treated_value").sum().alias("pre_treated_value"),
            pl.col("replacement_ratio").median().alias("median_replacement_ratio"),
        )
        .with_columns(
            (pl.col("treated_change") / pl.col("pre_treated_value")).alias("treated_pct_change")
        )
    )
    _w(het, "diversion_heterogeneity_by_dependence")
    print("\nHeterogeneity by pre-treatment dependence on the treated country:")
    print(het)

    stamp.write(layer_path("results", "diversion.runstamp.json"))
    (layer_path("results", "diversion_interpretation.json")).write_text(
        json.dumps(
            {
                "run": stamp.to_dict(),
                "counterfactual_adjusted_summary": adj_summary,
                "warnings": [
                    "The RAW pre-versus-post decomposition attributes ordinary trade growth to "
                    "the tariff and its replacement ratio is not interpretable on its own. Use "
                    "the counterfactual-adjusted figures.",
                    "An increase in imports from a third country is not evidence of production "
                    "relocation. Rerouting of treated-origin goods, transshipment, and origin "
                    "misdeclaration produce the same pattern in customs data.",
                    "The replacement ratio compares value flows only. It says nothing about "
                    "whether the replacing goods are the same quality or the same variety.",
                    "Domestic substitution is invisible in import data. A fall in imports that "
                    "is not matched by third-country gains may reflect domestic production, "
                    "lower final demand, or inventory drawdown, and these cannot be separated "
                    "without domestic output data.",
                    "The supplier set is the configured comparison group, not the world. "
                    "Concentration measures are within-sample.",
                ],
            },
            indent=2, default=str,
        )
        + "\n"
    )
    print(f"\nwrote diversion results (run_id={stamp.run_id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
