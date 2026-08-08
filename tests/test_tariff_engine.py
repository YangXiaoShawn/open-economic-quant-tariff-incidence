"""Tariff-engine tests.

Covers acceptance criteria 2 (implementation dates, rates, exclusions) and the
design commitment that ambiguity is never silently resolved.

Dates and rates used here are the real Section 301 values, each read from the
Federal Register notice cited in the test.
"""

from __future__ import annotations

from datetime import date

import pytest

from tariff_incidence.tariff.engine import (
    BaselineRateSource,
    TariffEngine,
    ValidationStatus,
)
from tariff_incidence.tariff.records import (
    Confidence,
    RecordType,
    SourceRef,
    TariffRecord,
)

CHINA = "5700"
VIETNAM = "5520"


def src(doc: str = "2018-20610", cite: str = "83 FR 47974") -> SourceRef:
    return SourceRef(
        document_id=doc,
        citation=cite,
        title="Notice of Modification of Section 301 Action",
        url=f"https://www.federalregister.gov/d/{doc}",
        publication_date="2018-09-21",
        checksum_sha256="0" * 64,
    )


def rec(
    code: str,
    *,
    effective: date,
    rate: float | None,
    action: str = "SEC301_LIST3",
    rtype: RecordType = RecordType.ADDITIONAL_DUTY,
    expiry: date | None = None,
    country: str = CHINA,
    partial: bool = False,
    rid: str | None = None,
    confidence: Confidence = Confidence.OFFICIAL_PARSED,
) -> TariffRecord:
    return TariffRecord(
        record_id=rid or f"{action}:{code}:{effective}:{rtype.value}",
        episode_id="US_SECTION301_CHINA",
        action_id=action,
        record_type=rtype,
        product_code=code,
        product_code_level=len(code),
        product_code_vintage="HTS2018",
        partner_country_code=country,
        announcement_date=date(2018, 7, 17),
        effective_date=effective,
        expiry_date=expiry,
        ad_valorem_rate=rate,
        source=src(),
        confidence=confidence,
        partial_line=partial,
    )


# --------------------------------------------------------------------- #
# implementation dates
# --------------------------------------------------------------------- #


def test_duty_not_applied_before_effective_date():
    """List 3 took effect 2018-09-24 (83 FR 47974). The day before is untreated."""
    e = TariffEngine([rec("84713001", effective=date(2018, 9, 24), rate=0.10)])
    a = e.assess("84713001", CHINA, date(2018, 9, 23))
    assert a.additional_rate == 0.0
    assert a.status is ValidationStatus.NO_MATCH
    assert not a.is_treated


def test_duty_applied_on_effective_date_itself():
    e = TariffEngine([rec("84713001", effective=date(2018, 9, 24), rate=0.10)])
    a = e.assess("84713001", CHINA, date(2018, 9, 24))
    assert a.additional_rate == pytest.approx(0.10)
    assert a.status is ValidationStatus.OK
    assert a.is_treated


def test_rate_increase_supersedes_original_within_the_same_action():
    """84 FR 20459 raised the List 3 rate to 25% on 2019-05-10, not on announcement."""
    e = TariffEngine(
        [
            rec("84713001", effective=date(2018, 9, 24), rate=0.10),
            rec("84713001", effective=date(2019, 5, 10), rate=0.25,
                rtype=RecordType.RATE_CHANGE),
        ]
    )
    assert e.assess("84713001", CHINA, date(2019, 5, 9)).additional_rate == pytest.approx(0.10)
    assert e.assess("84713001", CHINA, date(2019, 5, 10)).additional_rate == pytest.approx(0.25)


def test_announcement_date_does_not_trigger_the_duty():
    r = rec("84713001", effective=date(2019, 5, 10), rate=0.25)
    e = TariffEngine([r])
    assert r.announcement_date < r.effective_date
    assert e.assess("84713001", CHINA, r.announcement_date).additional_rate == 0.0


def test_untargeted_country_is_never_treated():
    e = TariffEngine([rec("84713001", effective=date(2018, 9, 24), rate=0.10)])
    a = e.assess("84713001", VIETNAM, date(2019, 1, 1))
    assert a.additional_rate == 0.0
    assert a.status is ValidationStatus.NO_MATCH


# --------------------------------------------------------------------- #
# exclusions
# --------------------------------------------------------------------- #


def test_exclusion_suppresses_the_duty_inside_its_window():
    e = TariffEngine(
        [
            rec("84713001", effective=date(2018, 9, 24), rate=0.10),
            rec("84713001", effective=date(2019, 3, 1), rate=None,
                rtype=RecordType.EXCLUSION, expiry=date(2019, 9, 1), rid="EXC1"),
        ]
    )
    assert e.assess("84713001", CHINA, date(2019, 2, 28)).additional_rate == pytest.approx(0.10)
    mid = e.assess("84713001", CHINA, date(2019, 5, 1))
    assert mid.additional_rate == 0.0
    assert mid.status is ValidationStatus.EXCLUDED
    assert mid.exclusion_active
    assert "EXC1" in mid.exclusion_record_ids


def test_duty_resumes_after_exclusion_expires():
    e = TariffEngine(
        [
            rec("84713001", effective=date(2018, 9, 24), rate=0.10),
            rec("84713001", effective=date(2019, 3, 1), rate=None,
                rtype=RecordType.EXCLUSION, expiry=date(2019, 9, 1), rid="EXC1"),
        ]
    )
    after = e.assess("84713001", CHINA, date(2019, 9, 1))
    assert after.additional_rate == pytest.approx(0.10)
    assert not after.exclusion_active


def test_reinstatement_cancels_an_earlier_exclusion():
    e = TariffEngine(
        [
            rec("84713001", effective=date(2018, 9, 24), rate=0.10),
            rec("84713001", effective=date(2019, 3, 1), rate=None,
                rtype=RecordType.EXCLUSION, rid="EXC1"),
            rec("84713001", effective=date(2019, 6, 1), rate=None,
                rtype=RecordType.REINSTATEMENT, rid="REIN1"),
        ]
    )
    assert e.assess("84713001", CHINA, date(2019, 4, 1)).status is ValidationStatus.EXCLUDED
    back = e.assess("84713001", CHINA, date(2019, 7, 1))
    assert back.additional_rate == pytest.approx(0.10)
    assert not back.exclusion_active


# --------------------------------------------------------------------- #
# ambiguity is surfaced, never silently resolved
# --------------------------------------------------------------------- #


def test_conflicting_actions_produce_conflict_and_no_rate():
    e = TariffEngine(
        [
            rec("84713001", effective=date(2018, 9, 24), rate=0.10, action="SEC301_LIST3"),
            rec("84713001", effective=date(2018, 9, 24), rate=0.25, action="OTHER_ACTION"),
        ]
    )
    a = e.assess("84713001", CHINA, date(2019, 1, 1))
    assert a.status is ValidationStatus.CONFLICT
    assert a.additional_rate is None, "engine must refuse to pick between conflicting rates"
    assert not a.status.usable_for_treatment


def test_duplicate_identical_records_do_not_create_a_conflict():
    e = TariffEngine(
        [
            rec("84713001", effective=date(2018, 9, 24), rate=0.10, action="A", rid="r1"),
            rec("84713001", effective=date(2018, 9, 24), rate=0.10, action="B", rid="r2"),
        ]
    )
    a = e.assess("84713001", CHINA, date(2019, 1, 1))
    assert a.status is ValidationStatus.OK
    assert a.additional_rate == pytest.approx(0.10)


def test_partial_statutory_line_is_flagged():
    e = TariffEngine(
        [rec("29319090", effective=date(2018, 9, 24), rate=0.10, partial=True)]
    )
    a = e.assess("29319090", CHINA, date(2019, 1, 1))
    assert a.status is ValidationStatus.PARTIAL_LINE
    assert not a.status.usable_for_treatment


def test_non_numeric_code_is_ambiguous_not_untreated():
    e = TariffEngine([rec("84713001", effective=date(2018, 9, 24), rate=0.10)])
    a = e.assess("84XX3001", CHINA, date(2019, 1, 1))
    assert a.status is ValidationStatus.AMBIGUOUS_CODE
    assert a.additional_rate is None


# --------------------------------------------------------------------- #
# HS6 coverage
# --------------------------------------------------------------------- #


def test_hs6_partial_coverage_is_reported_not_averaged_away():
    """Three of four HS8 children covered -> PARTIAL_HS6_COVERAGE, coverage 0.75."""
    children = {"847130": ["84713001", "84713002", "84713003", "84713004"]}
    recs = [
        rec(c, effective=date(2018, 9, 24), rate=0.10)
        for c in ["84713001", "84713002", "84713003"]
    ]
    e = TariffEngine(recs, hs6_children=children)
    a = e.assess("847130", CHINA, date(2019, 1, 1))
    assert a.status is ValidationStatus.PARTIAL_HS6_COVERAGE
    assert a.coverage_share == pytest.approx(0.75)
    assert not a.status.usable_for_treatment


def test_hs6_full_coverage_is_ok():
    children = {"847130": ["84713001", "84713002"]}
    recs = [rec(c, effective=date(2018, 9, 24), rate=0.10) for c in children["847130"]]
    e = TariffEngine(recs, hs6_children=children)
    a = e.assess("847130", CHINA, date(2019, 1, 1))
    assert a.status is ValidationStatus.OK
    assert a.coverage_share == pytest.approx(1.0)


def test_hs6_coverage_can_be_trade_weighted():
    children = {"847130": ["84713001", "84713002"]}
    e = TariffEngine(
        [rec("84713001", effective=date(2018, 9, 24), rate=0.10)], hs6_children=children
    )
    a = e.assess(
        "847130", CHINA, date(2019, 1, 1), hs8_weights={"84713001": 9.0, "84713002": 1.0}
    )
    assert a.coverage_share == pytest.approx(0.9)
    assert any("trade-weighted" in m for m in a.messages)


def test_hs10_resolves_through_its_hs8_parent():
    e = TariffEngine([rec("84713001", effective=date(2018, 9, 24), rate=0.10)])
    a = e.assess("8471300150", CHINA, date(2019, 1, 1))
    assert a.additional_rate == pytest.approx(0.10)
    assert a.product_code_level == 10


# --------------------------------------------------------------------- #
# baseline vs additional duty
# --------------------------------------------------------------------- #


def test_total_rate_adds_baseline_to_the_additional_duty():
    base = BaselineRateSource({("90330090", 2019): 0.044})
    e = TariffEngine(
        [rec("90330090", effective=date(2018, 9, 24), rate=0.10)], baseline=base
    )
    a = e.assess("90330090", CHINA, date(2019, 1, 1))
    assert a.baseline_rate == pytest.approx(0.044)
    assert a.additional_rate == pytest.approx(0.10)
    assert a.total_rate == pytest.approx(0.144)


def test_total_rate_is_none_when_baseline_unknown():
    """A missing MFN rate must not be silently treated as zero."""
    e = TariffEngine([rec("84713001", effective=date(2018, 9, 24), rate=0.10)])
    a = e.assess("84713001", CHINA, date(2019, 1, 1))
    assert a.baseline_rate is None
    assert a.total_rate is None
    assert a.additional_rate == pytest.approx(0.10)


# --------------------------------------------------------------------- #
# record validation
# --------------------------------------------------------------------- #


def test_record_rejects_expiry_before_effective():
    with pytest.raises(ValueError, match="precedes effective"):
        rec("84713001", effective=date(2019, 5, 1), rate=0.1, expiry=date(2019, 1, 1))


def test_record_rejects_rate_expressed_as_a_percentage():
    with pytest.raises(ValueError, match="implausible ad valorem"):
        rec("84713001", effective=date(2018, 9, 24), rate=25.0)


def test_record_rejects_code_length_mismatch():
    with pytest.raises(ValueError, match="does not match declared level"):
        TariffRecord(
            record_id="x", episode_id="e", action_id="a",
            record_type=RecordType.ADDITIONAL_DUTY,
            product_code="8471", product_code_level=8,
            product_code_vintage="HTS2018", partner_country_code=CHINA,
            announcement_date=None, effective_date=date(2018, 9, 24),
            expiry_date=None, ad_valorem_rate=0.1, source=src(),
        )
