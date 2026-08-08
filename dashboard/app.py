"""Lightweight Streamlit dashboard.

    make dashboard

Every displayed estimate carries its sample, outcome, treatment definition,
aggregation level, time period, weighting and specification. A number without
that context is not shown.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import polars as pl  # noqa: E402
import streamlit as st  # noqa: E402

from tariff_incidence.manifest import list_manifests  # noqa: E402
from tariff_incidence.paths import layer_path  # noqa: E402

RESULTS = ROOT / "data" / "results"

st.set_page_config(page_title="Tariff Incidence", layout="wide")


def read(name: str) -> pl.DataFrame | None:
    p = RESULTS / f"{name}.parquet"
    return pl.read_parquet(p) if p.exists() else None


def read_json(name: str) -> dict | None:
    p = RESULTS / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else None


panel_stamp_path = layer_path("analytical", "trade_panel.runstamp.json")
stamp = json.loads(panel_stamp_path.read_text()) if panel_stamp_path.exists() else {}
provenance = stamp.get("data_provenance", "UNKNOWN")

st.title("Tariff Incidence, Supply-Chain Reallocation, and Domestic Propagation")

if provenance != "OFFICIAL":
    st.error(
        f"**DATA PROVENANCE: {provenance}** — trade flows come from the documented synthetic "
        "generator. Every estimate below measures whether the estimation code behaves as "
        "designed. Nothing here describes U.S. trade. Set `CENSUS_API_KEY` and rebuild to "
        "produce official results.",
        icon="🚫",
    )
else:
    st.success("**DATA PROVENANCE: OFFICIAL** — all inputs trace to official sources.", icon="✅")

c1, c2, c3, c4 = st.columns(4)
c1.metric("run id", stamp.get("run_id", "—")[:18])
c2.metric("git commit", stamp.get("git_commit", "—"))
c3.metric("data period", f"{stamp.get('data_period_start')} → {stamp.get('data_period_end')}")
c4.metric("config", stamp.get("config_name", "—"))

tabs = st.tabs(
    [
        "Tariff timeline",
        "Product & sourcing",
        "Incidence estimates",
        "Diversion",
        "Industry exposure",
        "Data quality",
        "Pipeline status",
    ]
)

# ---------------------------------------------------------------- tariff
with tabs[0]:
    st.header("Section 301 tariff timeline")
    sched_p = layer_path("normalized", "tariff_schedule.parquet")
    if sched_p.exists():
        sched = pl.read_parquet(sched_p)
        summary = (
            sched.group_by(
                ["action_id", "record_type", "announcement_date", "effective_date",
                 "ad_valorem_rate", "source_citation"]
            )
            .agg(pl.len().alias("n_lines"), pl.col("partial_line").sum().alias("n_partial"))
            .sort("effective_date")
        )
        st.dataframe(summary.to_pandas(), width="stretch")
        st.caption(
            "Announcement and effective dates are distinct facts. The List 3 increase was "
            "announced for 2019-01-01, postponed twice, and took effect 2019-05-10."
        )
        parse = layer_path("normalized", "tariff_schedule_parse_report.json")
        if parse.exists():
            rep = json.loads(parse.read_text())
            st.subheader("Parse validation against each notice's own stated count")
            st.dataframe(
                pl.DataFrame(
                    [
                        {
                            "document": p["document_number"],
                            "heading": p["chapter99_heading"],
                            "parsed": p["parsed_line_count"],
                            "stated in notice": p["stated_line_count"],
                            "match": p["count_matches_notice"],
                        }
                        for p in rep["parses"]
                    ],
                    strict=False,
                ).to_pandas(),
                width="stretch",
            )
    else:
        st.info("Run `make build-tariff-schedule`.")

# ------------------------------------------------------- product/sourcing
with tabs[1]:
    st.header("Product search and sourcing")
    ppath = layer_path("analytical", "trade_panel.parquet")
    if ppath.exists():
        panel = pl.read_parquet(ppath)
        products = sorted(panel["hs6"].unique().to_list())
        sel = st.selectbox("HS6 product", products)
        sub = panel.filter(pl.col("hs6") == sel)
        meta = sub.row(0, named=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("ever treated", "yes" if meta["ever_treated_product"] else "no")
        m2.metric("pre-treatment China share", f"{meta['pretreatment_treated_country_share']:.1%}")
        m3.metric("tariff status", meta["tariff_status"])

        st.subheader("Customs value by partner")
        wide = sub.pivot(on="country_code", index="month_date", values="customs_value")
        st.line_chart(wide.to_pandas().set_index("month_date"))

        st.subheader("Customs vs duty-inclusive unit value (China)")
        cn = sub.filter(pl.col("is_treated_country")).select(
            ["month_date", "customs_unit_value", "landed_unit_value_duty_inclusive"]
        )
        st.line_chart(cn.to_pandas().set_index("month_date"))
        st.caption(
            "A unit value is value divided by quantity over a heterogeneous bundle. It is not "
            "a transaction price."
        )

        st.subheader("Treated-country share and supplier concentration")
        conc = sub.select(
            ["month_date", "treated_country_share", "supplier_hhi_in_sample"]
        ).unique().sort("month_date")
        st.line_chart(conc.to_pandas().set_index("month_date"))
    else:
        st.info("Run `make build-trade-panel`.")

# ------------------------------------------------------------- incidence
with tabs[2]:
    st.header("Incidence estimates")
    est = read("incidence_estimates")
    specs = read("specification_register")
    if est is not None:
        st.dataframe(
            est.select(
                ["rung", "outcome_label", "term", "estimate", "std_error", "ci_low", "ci_high",
                 "p_value", "n_obs", "absorbed_effects", "cluster_vars", "data_provenance"]
            ).to_pandas(),
            width="stretch",
        )
    for outcome in ["log_customs_unit_value", "log_landed_unit_value", "log_quantity"]:
        for ref in [1, 3]:
            ev = read(f"event_study_{outcome}_ref{ref}")
            if ev is None:
                continue
            with st.expander(f"Event study — {outcome} (reference −{ref})"):
                d = ev.filter(pl.col("event_time").is_not_null()).sort("event_time")
                st.line_chart(
                    d.select(["event_time", "estimate", "ci_low", "ci_high"])
                    .to_pandas()
                    .set_index("event_time")
                )
                st.dataframe(d.to_pandas(), width="stretch")

    ident = read_json("identification_checks")
    if ident:
        st.subheader("Pre-trend tests")
        st.dataframe(
            pl.DataFrame(
                [{"test": k, **{a: b for a, b in v.items() if a != "caveat"}}
                 for k, v in ident.get("pretrend_tests", {}).items()],
                strict=False,
            ).to_pandas(),
            width="stretch",
        )
        st.subheader("Placebo and stability checks")
        st.dataframe(pl.DataFrame(ident.get("checks", []), strict=False).to_pandas(),
                     width="stretch")
    sut = read("sutva_control_group_diagnostic")
    if sut is not None:
        st.subheader("Control-group contamination diagnostic")
        st.dataframe(sut.to_pandas(), width="stretch")
        st.caption(
            "Third-country suppliers of a treated product are not untreated bystanders. A gap "
            "between the two control groups is evidence of diversion spillover."
        )
    if specs is not None:
        with st.expander("Specification register"):
            st.dataframe(specs.to_pandas(), width="stretch")

# ------------------------------------------------------------- diversion
with tabs[3]:
    st.header("Trade diversion")
    tot = read("diversion_totals")
    adj = read("diversion_counterfactual_adjusted")
    gains = read("diversion_country_gains")
    if tot is not None:
        t = tot.row(0, named=True)
        a, b, c = st.columns(3)
        a.metric("treated-country change", f"{t['treated_total']:,.0f}")
        b.metric("alternative-source change", f"{t['alternative_total']:,.0f}")
        c.metric("net change", f"{t['total_change']:,.0f}")
        st.caption("Contraction and expansion are reported separately and never netted.")
    if adj is not None:
        st.subheader("Counterfactual-adjusted (net of never-treated product growth)")
        st.dataframe(adj.to_pandas(), width="stretch")
        st.info(
            "The raw pre/post replacement ratio credits ordinary trade growth to the tariff. "
            "Read the adjusted figures."
        )
    if gains is not None:
        st.subheader("Partner-country detail")
        st.dataframe(gains.to_pandas(), width="stretch")
    st.warning(
        "A third-country increase in customs data is consistent with relocated production, "
        "rerouting of treated-origin goods, and origin misdeclaration. Customs statistics "
        "cannot separate these."
    )

# ------------------------------------------------------------- exposure
with tabs[4]:
    st.header("Industry exposure")
    expo = read("industry_tariff_exposure")
    summ = read("industry_exposure_summary")
    if expo is not None:
        if summ is not None:
            st.dataframe(summ.to_pandas(), width="stretch")
        st.subheader("Protection vs imported-input cost, by industry")
        st.dataframe(
            expo.select(
                ["industry_code", "industry_name", "output_protection_exposure",
                 "imported_input_cost_exposure", "downstream_total_requirements_exposure",
                 "exposure_class", "concordance_status"]
            ).to_pandas(),
            width="stretch",
        )
        st.warning(
            "The two channels are never netted. An industry can be protected on its output "
            "and squeezed on its inputs at the same time."
        )
        q = read_json("io_exposure_quality")
        if q:
            st.caption(f"Concordance status: {q.get('concordance_config_status')} — "
                       f"{q['concordance']['aggregation_loss']}")
    else:
        st.info("Run `make build-io-exposure`.")

# ---------------------------------------------------------------- quality
with tabs[5]:
    st.header("Data quality")
    dq = read("data_quality_report")
    if dq is not None:
        st.dataframe(dq.to_pandas(), width="stretch")
        st.caption("A check that could not run is reported SKIPPED, never PASS.")
    else:
        st.info("Run `make validate-data`.")

# ---------------------------------------------------------------- status
with tabs[6]:
    st.header("Pipeline status and data freshness")
    mans = list_manifests()
    if mans:
        st.dataframe(
            pl.DataFrame(
                [
                    {
                        "dataset": m.dataset_id,
                        "layer": m.layer,
                        "rows": m.row_count,
                        "provenance": m.data_provenance,
                        "retrieved": m.retrieval_timestamp_utc[:19],
                        "vintage": m.source_release_or_vintage[:60],
                        "checksum": m.checksum_sha256[:12],
                    }
                    for m in mans
                ]
            ).to_pandas(),
            width="stretch",
        )
        st.subheader("Known limitations recorded on each dataset")
        for m in mans:
            if m.known_limitations:
                with st.expander(m.dataset_id):
                    for lim in m.known_limitations:
                        st.markdown(f"- {lim}")
    else:
        st.info("No manifests yet. Run `make reproduce-sample`.")
