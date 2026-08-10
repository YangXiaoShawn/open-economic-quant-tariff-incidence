"""Census import-concordance adapter tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from tariff_incidence.adapters.census_concordance import (
    build_hs10_to_bea,
    naics_to_bea_summary,
    parse_concordance,
)
from tariff_incidence.paths import RAW

REAL = RAW / "census_concordance" / "impconcord20.xlsx"


@pytest.mark.parametrize(
    ("naics", "expected"),
    [
        ("334413", "334"),      # semiconductors -> computer and electronic products
        ("332999", "332"),      # fabricated metal
        ("336111", "3361MV"),   # automobiles -> the motor-vehicle composite
        ("336411", "3364OT"),   # aircraft -> other transportation equipment
        ("311111", "311FT"),    # food -> food, beverage and tobacco
        ("313210", "313TT"),    # textile mills
        ("315220", "315AL"),    # apparel
        ("112920", "111CA"),    # animal production -> farms
        ("211120", "211"),      # oil and gas extraction
    ],
)
def test_naics_maps_to_the_documented_bea_summary_industry(naics, expected):
    assert naics_to_bea_summary(naics) == expected


def test_longer_composite_prefix_wins_over_the_three_digit_fallback():
    """3361 must resolve to the motor-vehicle composite, not to a bare 336."""
    assert naics_to_bea_summary("336112") == "3361MV"
    assert naics_to_bea_summary("336510") == "3364OT"


def test_unmappable_naics_returns_none_rather_than_a_guess():
    assert naics_to_bea_summary("999999") is None
    assert naics_to_bea_summary("") is None
    assert naics_to_bea_summary("541511") is None  # services, outside the IO groups used


def test_census_x_placeholder_still_maps_when_the_prefix_is_unambiguous():
    """Census writes X where it aggregates undisclosed detail."""
    assert naics_to_bea_summary("33251X") == "332"
    assert naics_to_bea_summary("11211X") == "111CA"


def test_legacy_xls_vintage_is_refused_rather_than_silently_skipped(tmp_path: Path):
    p = tmp_path / "impconcord19.xls"
    p.write_bytes(b"not really a workbook")
    with pytest.raises(ValueError, match="legacy .xls format"):
        parse_concordance(p, 2019)


@pytest.mark.skipif(not REAL.exists(), reason="concordance workbook not cached")
def test_official_concordance_is_keyed_on_ten_digit_lines():
    load = parse_concordance(REAL, 2020)
    assert load.n_rows > 15000
    codes = load.mapping["hs10"].to_list()
    assert all(len(c) == 10 and c.isdigit() for c in codes[:500])
    assert len(set(codes)) == len(codes), "one NAICS per commodity line, no duplicates"


@pytest.mark.skipif(not REAL.exists(), reason="concordance workbook not cached")
def test_official_concordance_reaches_a_bea_industry_for_almost_every_line():
    load = parse_concordance(REAL, 2020)
    _, q = build_hs10_to_bea(load)
    assert q["share_mapped"] > 0.95
    assert q["n_distinct_bea"] >= 20
    assert q["n_unmapped_to_bea"] > 0, "unmapped lines are counted, not hidden"
    assert any("outside the BEA summary" in w for w in q["warnings"])


@pytest.mark.skipif(not REAL.exists(), reason="concordance workbook not cached")
def test_aggregated_naics_codes_are_reported_not_truncated():
    load = parse_concordance(REAL, 2020)
    assert load.n_aggregated_naics > 0
    withx = load.mapping.filter(load.mapping["naics"].str.contains("X"))
    assert withx.height == load.n_aggregated_naics
    assert all("X" in n for n in withx["naics"].to_list()[:20])
