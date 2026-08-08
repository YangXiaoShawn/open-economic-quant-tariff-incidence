"""Product x country x month analytical panel construction.

Turns a staged trade table plus a tariff schedule into the analysis panel.

Value concepts are kept strictly separate and separately named, because
collapsing them is the most common way tariff-incidence work goes wrong:

``customs_value``
    Value at the foreign port of export, excluding freight and insurance.
``import_charges``
    Freight, insurance and other charges to the U.S. border.
``cif_value``
    ``customs_value + import_charges``.
``dutiable_value``
    Portion of customs value actually subject to duty.
``calculated_duties``
    Duty computed by Customs on the dutiable value.
``customs_unit_value``
    ``customs_value / quantity``. **Tariff-exclusive.** Not a transaction price.
``landed_unit_value_duty_inclusive``
    ``(customs_value + calculated_duties) / quantity``. What the importer pays at
    the border, excluding freight.
``landed_unit_value_full``
    ``(customs_value + import_charges + calculated_duties) / quantity``.

The three unit-value concepts answer different questions. Incidence on the
*exporter* shows up in ``customs_unit_value``; incidence on the *U.S. importer*
shows up in the duty-inclusive measures.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date

import polars as pl

from ..tariff.engine import TariffEngine, ValidationStatus

PANEL_SCHEMA_VERSION = "panel_v1"


def _month_index(df: pl.DataFrame, col: str = "month_date") -> pl.DataFrame:
    return df.with_columns(
        (pl.col(col).dt.year() * 12 + pl.col(col).dt.month()).alias("month_index")
    )


def construct_value_measures(df: pl.DataFrame) -> pl.DataFrame:
    """Derive value and unit-value concepts, keeping each separately labelled."""
    out = df.rename(
        {
            "con_val_mo": "customs_value",
            "gen_val_mo": "general_imports_value",
            "dut_val_mo": "dutiable_value",
            "cal_dut_mo": "calculated_duties",
            "con_cha_mo": "import_charges",
            "con_qy1_mo": "quantity",
            "unit_qy1": "quantity_unit",
            "con_qy2_mo": "quantity_2",
            "unit_qy2": "quantity_2_unit",
        },
        strict=False,
    )

    q = pl.col("quantity")
    valid_q = (q.is_not_null()) & (q > 0)

    return out.with_columns(
        (pl.col("customs_value") + pl.col("import_charges")).alias("cif_value"),
        pl.when(valid_q)
        .then(pl.col("customs_value") / q)
        .otherwise(None)
        .alias("customs_unit_value"),
        pl.when(valid_q)
        .then((pl.col("customs_value") + pl.col("calculated_duties")) / q)
        .otherwise(None)
        .alias("landed_unit_value_duty_inclusive"),
        pl.when(valid_q)
        .then(
            (pl.col("customs_value") + pl.col("import_charges") + pl.col("calculated_duties")) / q
        )
        .otherwise(None)
        .alias("landed_unit_value_full"),
        # Realised duty rate implied by the data, independent of the policy engine.
        pl.when(pl.col("dutiable_value") > 0)
        .then(pl.col("calculated_duties") / pl.col("dutiable_value"))
        .otherwise(None)
        .alias("realised_duty_rate_on_dutiable"),
        pl.when(pl.col("customs_value") > 0)
        .then(pl.col("calculated_duties") / pl.col("customs_value"))
        .otherwise(None)
        .alias("realised_duty_rate_on_customs"),
        pl.when(pl.col("customs_value") > 0)
        .then(pl.col("import_charges") / pl.col("customs_value"))
        .otherwise(None)
        .alias("freight_share_of_customs_value"),
    )


def _month_segments(
    month_start: date, engine: TariffEngine, product: str, country: str
) -> list[tuple[date, int]]:
    """Split a month into segments of constant tariff law, with day weights.

    Section 301 duties take effect on a specific day (List 3 on 24 September
    2018), but trade data is monthly. Assessing the month at its first day says
    "untreated" for a month in which duties were collected for a week;
    assessing at the last day says "fully treated". Both are wrong, and the
    error lands squarely on the event-time-zero coefficient.

    This returns the distinct legal regimes within the month and how many days
    each covered, so the panel can carry a day-weighted average statutory rate.
    """
    if month_start.month == 12:
        nxt = date(month_start.year + 1, 1, 1)
    else:
        nxt = date(month_start.year, month_start.month + 1, 1)
    n_days = (nxt - month_start).days

    cuts = {month_start}
    for r in engine.records:
        if r.product_code[:8] != product[:8] and not r.product_code.startswith(product[:6]):
            continue
        if r.partner_country_code != country:
            continue
        for d in (r.effective_date, r.expiry_date):
            if d is not None and month_start < d < nxt:
                cuts.add(d)
    ordered = sorted(cuts)
    segs: list[tuple[date, int]] = []
    for i, start in enumerate(ordered):
        end = ordered[i + 1] if i + 1 < len(ordered) else nxt
        segs.append((start, (end - start).days))
    assert sum(d for _, d in segs) == n_days
    return segs


def month_average_additional_rate(
    engine: TariffEngine, product: str, country: str, month_start: date
) -> float:
    """Day-weighted average additional duty over a calendar month.

    Exposed so anything that needs the same number -- the panel builder, the
    synthetic generator, the dashboard -- uses one implementation. Two
    implementations of a timing convention will disagree, and the disagreement
    shows up as measurement error in the treatment variable.
    """
    segs = _month_segments(month_start, engine, product, country)
    total_days = sum(d for _, d in segs)
    acc = 0.0
    for start, days in segs:
        a = engine.assess(product, country, start)
        acc += (a.additional_rate or 0.0) * days
    return acc / total_days if total_days else 0.0


def attach_tariff_treatment(
    df: pl.DataFrame,
    engine: TariffEngine,
    *,
    product_col: str = "hs6",
    country_col: str = "country_code",
    month_col: str = "month_date",
    hs8_weights: dict[str, dict[str, float]] | None = None,
    day_weight_within_month: bool = True,
) -> pl.DataFrame:
    """Attach point-in-time tariff assessments from the policy engine.

    The engine is queried once per distinct (product, country, month) rather than
    per row. Ambiguous assessments are carried through as explicit status flags,
    never silently converted into a treatment indicator.

    With ``day_weight_within_month`` the reported rate is the day-weighted
    average statutory rate over the month, which is what a monthly duty
    collection actually reflects. ``statutory_rate_month_end`` is kept alongside
    it so a specification can use the discrete-jump definition instead, and the
    two can be compared.
    """
    keys = (
        df.select([product_col, country_col, month_col])
        .unique()
        .sort([product_col, country_col, month_col])
    )

    recs = []
    for prod, ctry, mth in keys.iter_rows():
        when: date = mth
        weights = (hs8_weights or {}).get(prod)
        segs = (
            _month_segments(when, engine, prod, ctry)
            if day_weight_within_month
            else [(when, 1)]
        )
        total_days = sum(d for _, d in segs)
        assessments = [(engine.assess(prod, ctry, s, hs8_weights=weights), d) for s, d in segs]
        primary = assessments[-1][0]  # end-of-month legal state
        first = assessments[0][0]

        def _avg(attr: str, _asmts=assessments, _days=total_days) -> float | None:
            vals = [(getattr(a, attr), d) for a, d in _asmts]
            if any(v is None for v, _ in vals):
                return None
            return sum(v * d for v, d in vals) / _days

        recs.append(
            {
                product_col: prod,
                country_col: ctry,
                month_col: mth,
                "baseline_mfn_rate": primary.baseline_rate,
                "additional_tariff_rate": _avg("additional_rate"),
                "total_modeled_tariff_rate": _avg("total_rate"),
                "additional_tariff_rate_month_end": primary.additional_rate,
                "additional_tariff_rate_month_start": first.additional_rate,
                "tariff_regime_changed_within_month": len(segs) > 1,
                "tariff_coverage_share": primary.coverage_share,
                "tariff_status": primary.status.value,
                "tariff_confidence": primary.confidence.value,
                "active_actions": "|".join(primary.active_action_ids),
                "exclusion_active": primary.exclusion_active,
                "tariff_source_records": "|".join(primary.source_records[:4]),
                "tariff_usable_for_treatment": primary.status.usable_for_treatment,
                "treated": bool(primary.is_treated),
            }
        )
    tar = pl.DataFrame(recs)
    return df.join(tar, on=[product_col, country_col, month_col], how="left")


def add_event_time(
    df: pl.DataFrame,
    *,
    product_col: str = "hs6",
    treated_flag: str = "treated",
    month_col: str = "month_date",
) -> pl.DataFrame:
    """Add first-treatment date and event time in months, per product.

    Event time is defined on the **product**, not the product-country flow: the
    policy targets a product line from one origin, and defining event time per
    flow would give control-country observations no event time at all, making
    difference-in-differences impossible.
    """
    df = _month_index(df, month_col)
    first = (
        df.filter(pl.col(treated_flag))
        .group_by(product_col)
        .agg(pl.col("month_index").min().alias("first_treated_month_index"))
    )
    out = df.join(first, on=product_col, how="left")
    return out.with_columns(
        (pl.col("month_index") - pl.col("first_treated_month_index")).alias("event_time"),
        pl.col("first_treated_month_index").is_not_null().alias("ever_treated_product"),
    )


def add_sourcing_measures(
    df: pl.DataFrame,
    *,
    treated_country_code: str,
    product_col: str = "hs6",
    country_col: str = "country_code",
    month_col: str = "month_date",
    value_col: str = "customs_value",
) -> pl.DataFrame:
    """Add supplier shares, supplier counts and concentration per product-month.

    Concentration is a Herfindahl index over supplier-country value shares within
    the sampled country set. Because the sample is a selected set of partners,
    this is a *within-sample* HHI and is labelled as such; it is not the true
    global supplier concentration for the product.
    """
    tot = df.group_by([product_col, month_col]).agg(
        pl.col(value_col).sum().alias("product_month_total_value"),
        (pl.col(value_col) > 0).sum().alias("supplier_count_in_sample"),
    )
    out = df.join(tot, on=[product_col, month_col], how="left")
    out = out.with_columns(
        pl.when(pl.col("product_month_total_value") > 0)
        .then(pl.col(value_col) / pl.col("product_month_total_value"))
        .otherwise(None)
        .alias("supplier_value_share")
    )
    hhi = (
        out.group_by([product_col, month_col])
        .agg((pl.col("supplier_value_share") ** 2).sum().alias("supplier_hhi_in_sample"))
    )
    out = out.join(hhi, on=[product_col, month_col], how="left")

    treated_share = (
        out.filter(pl.col(country_col) == treated_country_code)
        .select([product_col, month_col, pl.col("supplier_value_share").alias("treated_country_share")])
    )
    out = out.join(treated_share, on=[product_col, month_col], how="left")
    return out.with_columns(
        (1.0 - pl.col("treated_country_share")).alias("alternative_source_share"),
        (pl.col(country_col) == treated_country_code).alias("is_treated_country"),
    )


def add_extensive_margin(
    df: pl.DataFrame,
    *,
    product_col: str = "hs6",
    country_col: str = "country_code",
    value_col: str = "customs_value",
) -> pl.DataFrame:
    """Flag flow entry, exit and activity on the product-country extensive margin."""
    out = df.sort([product_col, country_col, "month_index"])
    active = (pl.col(value_col).fill_null(0.0) > 0).alias("flow_active")
    out = out.with_columns(active)
    return out.with_columns(
        pl.col("flow_active")
        .shift(1)
        .over([product_col, country_col])
        .alias("flow_active_lag"),
    ).with_columns(
        (pl.col("flow_active") & ~pl.col("flow_active_lag").fill_null(False)).alias("flow_entry"),
        (~pl.col("flow_active") & pl.col("flow_active_lag").fill_null(False)).alias("flow_exit"),
    )


def add_pretreatment_exposure(
    df: pl.DataFrame,
    *,
    treated_country_code: str,
    pre_period_end: date,
    product_col: str = "hs6",
    country_col: str = "country_code",
    month_col: str = "month_date",
    value_col: str = "customs_value",
) -> pl.DataFrame:
    """Pre-treatment dependence on the treated country, per product.

    Computed on a fixed pre-period window so it cannot be contaminated by the
    post-treatment reallocation it is used to explain. This is the standard
    shift-share precaution: the share is a *pre-determined* weight.
    """
    pre = df.filter(pl.col(month_col) <= pre_period_end)
    tot = pre.group_by(product_col).agg(pl.col(value_col).sum().alias("_pre_total"))
    trt = (
        pre.filter(pl.col(country_col) == treated_country_code)
        .group_by(product_col)
        .agg(pl.col(value_col).sum().alias("_pre_treated"))
    )
    exp = (
        tot.join(trt, on=product_col, how="left")
        .with_columns(
            (pl.col("_pre_treated").fill_null(0.0) / pl.col("_pre_total"))
            .alias("pretreatment_treated_country_share")
        )
        .select([product_col, "pretreatment_treated_country_share"])
    )
    return df.join(exp, on=product_col, how="left")


def build_panel(
    staged: pl.DataFrame,
    engine: TariffEngine,
    *,
    treated_country_code: str,
    pre_period_end: date,
    hs8_weights: dict[str, dict[str, float]] | None = None,
) -> pl.DataFrame:
    """Full analytical-panel construction pipeline."""
    df = construct_value_measures(staged)
    df = attach_tariff_treatment(df, engine, hs8_weights=hs8_weights)
    df = add_event_time(df)
    df = add_sourcing_measures(df, treated_country_code=treated_country_code)
    df = add_extensive_margin(df)
    df = add_pretreatment_exposure(
        df, treated_country_code=treated_country_code, pre_period_end=pre_period_end
    )
    return df.with_columns(
        pl.lit(PANEL_SCHEMA_VERSION).alias("panel_schema_version"),
        pl.col("customs_unit_value").log().alias("log_customs_unit_value"),
        pl.col("landed_unit_value_duty_inclusive").log().alias("log_landed_unit_value"),
        pl.col("quantity").log().alias("log_quantity"),
        pl.col("customs_value").log().alias("log_customs_value"),
        (pl.col("hs6").str.slice(0, 2)).alias("hs2_chapter"),
    ).sort(["hs6", "country_code", "month_date"])


def ambiguity_report(panel: pl.DataFrame) -> pl.DataFrame:
    """Count observations by tariff-assessment status.

    Surfaced in every run so a sample with many ``PARTIAL_HS6_COVERAGE`` or
    ``CONFLICT`` rows cannot quietly be treated as cleanly identified.
    """
    return (
        panel.group_by("tariff_status")
        .agg(
            pl.len().alias("n_obs"),
            pl.col("hs6").n_unique().alias("n_products"),
            pl.col("customs_value").sum().alias("customs_value"),
        )
        .sort("n_obs", descending=True)
    )


def stable_code_sample(
    panel: pl.DataFrame,
    stable_codes: Iterable[str],
    product_col: str = "hs6",
) -> pl.DataFrame:
    """Restrict to product codes that did not change definition over the window."""
    return panel.filter(pl.col(product_col).is_in(list(stable_codes)))


def unambiguous_sample(panel: pl.DataFrame) -> pl.DataFrame:
    """Restrict to observations whose tariff assessment is usable without judgement."""
    return panel.filter(
        pl.col("tariff_status").is_in(
            [
                ValidationStatus.OK.value,
                ValidationStatus.NO_MATCH.value,
                ValidationStatus.EXCLUDED.value,
            ]
        )
    )
