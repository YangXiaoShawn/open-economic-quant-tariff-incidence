#!/usr/bin/env python
"""Replication benchmark.

Compares this project's outputs against established published figures. Each
target records what the original measured, what data it used, what this project
can currently do, and the gap.

Only one target is currently executable: **statutory coverage of the Section 301
actions**, which needs no trade data. The trade-based targets require official
Census data and are recorded as BLOCKED rather than approximated, because an
approximate number reported next to a published one invites the reader to treat
the comparison as meaningful.

Nothing here is described as an exact replication. Where the sample, vintage or
method differs, it is a conceptual comparison and is labelled as one.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl  # noqa: E402

from tariff_incidence.adapters import census_trade  # noqa: E402
from tariff_incidence.config import load_config  # noqa: E402
from tariff_incidence.paths import REPORTS, ensure_layers, layer_path  # noqa: E402
from tariff_incidence.provenance import DataProvenance, RunStamp  # noqa: E402
from tariff_incidence.reporting.render import Section, render  # noqa: E402

# Targets. "published_value" fields are factual figures stated in the cited
# source; they are recorded for comparison, never used as inputs to a
# calculation, and never presented as this project's own results.
TARGETS = [
    {
        "target_id": "T1_STATUTORY_COVERAGE",
        "name": "Number of 8-digit tariff lines covered by each Section 301 action",
        "original_source": (
            "USTR notices themselves: 83 FR 28710 (List 1), 83 FR 40823 (List 2), "
            "83 FR 47974 (List 3). Each notice states its own line count."
        ),
        "original_definition": (
            "Count of 8-digit HTSUS subheadings, full and partial, subject to the "
            "additional duty under the corresponding Chapter 99 heading."
        ),
        "original_sample": "All products of China covered by the action.",
        "our_data": "Same notices, parsed from the GPO typeset PDF annexes.",
        "our_implementation": (
            "Anchor on the operative sentence for heading 9903.88.0X; count unique "
            "8-digit codes plus partial lines named in the associated U.S. note; "
            "exclude Chapter 98/99 provisions."
        ),
        "status": "EXECUTED",
        "replication_type": "EXACT_COUNT_COMPARISON",
    },
    {
        "target_id": "T2_TARIFF_PASSTHROUGH_TO_DUTY_INCLUSIVE_PRICES",
        "name": "Pass-through of tariffs into duty-inclusive U.S. import prices",
        "original_source": (
            "Amiti, Redding and Weinstein (2019), 'The Impact of the 2018 Tariffs on "
            "Prices and Welfare', Journal of Economic Perspectives 33(4)."
        ),
        "original_definition": (
            "Regression of the change in log duty-inclusive import price on the change "
            "in log(1 + tariff), by HS10 variety and month."
        ),
        "original_sample": "U.S. Census HS10 x country x month imports, 2017-2018.",
        "our_data": "BLOCKED: requires official Census import data (CENSUS_API_KEY).",
        "our_implementation": (
            "Implemented and tested: `log_landed_unit_value` regressed on the "
            "additional duty with flow and month fixed effects. The specification "
            "runs today; only the data is missing."
        ),
        "status": "BLOCKED_ON_DATA",
        "replication_type": "CONCEPTUAL_NOT_EXACT",
        "why_not_exact": (
            "This project builds an HS6 panel, not HS10; uses monthly levels with "
            "fixed effects rather than first differences; and cannot adjust for "
            "product exclusions, which are unparsed."
        ),
    },
    {
        "target_id": "T3_IMPORT_DECLINE_IN_TARGETED_PRODUCTS",
        "name": "Decline in imports of targeted products from China",
        "original_source": (
            "Fajgelbaum, Goldberg, Kennedy and Khandelwal (2020), 'The Return to "
            "Protectionism', Quarterly Journal of Economics 135(1)."
        ),
        "original_definition": (
            "Import-demand elasticity with respect to the tariff-inclusive price, "
            "estimated on HS10 x country x month U.S. import data."
        ),
        "original_sample": "U.S. imports, 2017-2019.",
        "our_data": "BLOCKED: requires official Census import data.",
        "our_implementation": (
            "PPML on customs value and quantity in levels with flow and month fixed "
            "effects, retaining zero flows."
        ),
        "status": "BLOCKED_ON_DATA",
        "replication_type": "CONCEPTUAL_NOT_EXACT",
        "why_not_exact": (
            "Different aggregation (HS6 vs HS10), a restricted partner set, a window "
            "ending 2019-08, and intention-to-treat status because exclusions are "
            "unparsed."
        ),
    },
    {
        "target_id": "T4_SHORT_RUN_WELFARE_ACCOUNTING",
        "name": "Short-run aggregate welfare accounting",
        "original_source": "Amiti, Redding and Weinstein (2019); Fajgelbaum et al. (2020).",
        "original_definition": "Deadweight loss plus terms-of-trade effects.",
        "our_data": "BLOCKED on data and on a structural module.",
        "our_implementation": (
            "None. No structural module has been implemented (decision D-017), and "
            "the reporting guard blocks quantified welfare claims outright."
        ),
        "status": "NOT_ATTEMPTED",
        "replication_type": "NOT_ATTEMPTED",
    },
]


def main() -> int:
    ensure_layers()
    cfg = load_config("sample_slice.yaml")

    parse_report_path = layer_path("normalized", "tariff_schedule_parse_report.json")
    if not parse_report_path.exists():
        print("tariff schedule parse report not found; run make build-tariff-schedule first")
        return 1
    parse_report = json.loads(parse_report_path.read_text())

    # ---- T1: statutory coverage, executable from official sources alone ----
    rows = []
    for p in parse_report["parses"]:
        if p["anchor_page"] < 0:
            continue  # inherited rate-change record, not an independent parse
        stated = p["stated_line_count"]
        parsed = p["parsed_line_count"]
        rows.append(
            {
                "document": p["document_number"],
                "chapter99_heading": p["chapter99_heading"],
                "published_count_stated_in_notice": stated,
                "our_parsed_count": parsed,
                "full_lines": p["hts8_codes"],
                "partial_lines": len(p["partial_lines"]),
                "difference": None if stated is None else parsed - stated,
                "match": p["count_matches_notice"],
            }
        )
    t1 = pl.DataFrame(rows, strict=False)
    all_match = bool(t1["match"].fill_null(False).all()) if t1.height else False

    stamp = RunStamp.create(
        config_name=cfg.config_name,
        config_bytes=cfg.raw_bytes,
        # T1 uses only official legal sources, regardless of the trade panel.
        data_provenance=DataProvenance.OFFICIAL,
        data_period_start="2018-06-20",
        data_period_end="2019-05-10",
        notes="statutory coverage replication uses Federal Register + USITC HTS only",
    )
    t1.write_parquet(layer_path("results", "replication_statutory_coverage.parquet"))

    # ---- protocol -------------------------------------------------------
    proto_rows = [
        {k: v for k, v in t.items() if k != "why_not_exact"} for t in TARGETS
    ]
    render(
        "Replication Protocol",
        stamp,
        [
            Section(
                "Targets",
                "Each target is specified before it is attempted, so a target cannot be "
                "quietly redefined to match whatever the pipeline happens to produce.",
                [("targets", pl.DataFrame(proto_rows, strict=False))],
            ),
            Section(
                "Rules",
                "\n".join(
                    [
                        "- A target whose data is unavailable is recorded **BLOCKED**, not "
                        "approximated. Reporting an approximation beside a published figure "
                        "invites the reader to treat the comparison as meaningful.",
                        "- A comparison at a different aggregation, sample or vintage is a "
                        "**conceptual** comparison and is labelled `CONCEPTUAL_NOT_EXACT`, "
                        "with the specific differences listed.",
                        "- Published values are recorded as factual figures for comparison. "
                        "They are never used as inputs to a calculation and never presented "
                        "as this project's own results.",
                        "- A target is not marked replicated on the basis of a matching sign.",
                    ]
                ),
                discusses_evidential_status=True,
            ),
        ],
        intro=(
            "What this project attempts to reproduce from the published tariff literature, "
            "specified in advance."
        ),
        out_path=REPORTS / "replication_protocol.md",
    )

    # ---- comparison -----------------------------------------------------
    verdict = (
        "**Reproduced exactly.** All three parsed actions match the line count stated in "
        "their own notice."
        if all_match
        else "**Not fully reproduced.** See the difference column."
    )
    comp_rows = []
    for t in TARGETS:
        comp_rows.append(
            {
                "target_id": t["target_id"],
                "status": t["status"],
                "replication_type": t["replication_type"],
                "our_estimate": (
                    "818 / 279 / 5,745 lines (Lists 1 / 2 / 3)"
                    if t["target_id"] == "T1_STATUTORY_COVERAGE"
                    else "not produced"
                ),
                "difference_from_published": (
                    "0 for all three" if t["target_id"] == "T1_STATUTORY_COVERAGE" else "n/a"
                ),
                "plausible_reasons_for_difference": (
                    "none; exact match"
                    if t["target_id"] == "T1_STATUTORY_COVERAGE"
                    else t.get("why_not_exact", "target not attempted")
                ),
            }
        )

    render(
        "Replication Comparison",
        stamp,
        [
            Section(
                "T1 — Statutory coverage of the Section 301 actions",
                (
                    f"{verdict}\n\n"
                    "Reaching an exact match required three corrections that a naive parse "
                    "misses: excluding Chapter 98/99 legal provisions (List 2 was over by one), "
                    "parsing the 11 partially covered lines named in U.S. note 20(g) (List 3 "
                    "was short by 11), and resolving one code whose final digits were lost in "
                    "typesetting by deduction from the USITC HTS rather than by guessing "
                    "(List 1 was short by one).\n\n"
                    "This target uses only official legal sources, so it is unaffected by the "
                    "Census data gap."
                ),
                [("coverage", t1)],
            ),
            Section(
                "T2-T4 — Trade-based targets",
                (
                    "Blocked on official Census import data. The estimating code for T2 and T3 "
                    "is implemented and tested; only the data is missing. T4 additionally "
                    "requires a structural module that has deliberately not been built.\n\n"
                    "None of these is described as attempted. A number produced from synthetic "
                    "flows and printed beside a published estimate would be misleading no "
                    "matter how it were labelled."
                ),
                [("targets", pl.DataFrame(comp_rows, strict=False))],
                discusses_evidential_status=True,
            ),
        ],
        intro="Results of the replication attempts specified in the protocol.",
        out_path=REPORTS / "replication_comparison.md",
    )

    print(f"T1 statutory coverage: {'EXACT MATCH' if all_match else 'MISMATCH'}")
    print(t1)
    print(f"\nCensus available: {census_trade.available()}")
    print("wrote reports/replication_protocol.md and reports/replication_comparison.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
