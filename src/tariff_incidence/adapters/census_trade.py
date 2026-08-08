"""U.S. Census Bureau international-trade adapter (monthly imports by HS x country).

Endpoint: ``https://api.census.gov/data/timeseries/intltrade/imports/hs``

**An API key is required.** Census retired keyless access to this endpoint; an
unauthenticated request returns an HTML "Missing Key" page with HTTP 200, which
is precisely the kind of failure that silently poisons a pipeline, so the
adapter checks the payload shape rather than trusting the status code.

Register free at https://api.census.gov/data/key_signup.html and export::

    export CENSUS_API_KEY=...

Variable semantics (from the endpoint's own ``variables.json``, fetched and
cached at runtime rather than hard-coded)
-----------------------------------------------------------------------------

``GEN_VAL_MO``   General imports, total value. All merchandise arriving, whether
                 entered for consumption or into bonded warehouse/FTZ.
``CON_VAL_MO``   Imports **for consumption**, total value. The customs value of
                 goods entering the U.S. economy. This is the correct
                 denominator for duty ratios, because duties are assessed on
                 entries for consumption.
``DUT_VAL_MO``   Dutiable value: the portion of consumption value actually
                 subject to duty. Differs from customs value when part of an
                 entry enters duty-free.
``CAL_DUT_MO``   Calculated duties. The duty amount computed by Customs.
``CON_CHA_MO``   Import charges: freight, insurance and other charges to bring
                 the goods to the U.S. border. Customs value **excludes** these.
``CON_QY1_MO``   Primary quantity, in ``UNIT_QY1``.
``CON_QY2_MO``   Secondary quantity, in ``UNIT_QY2``.

Measurement caution carried downstream
--------------------------------------

A unit value is ``value / quantity`` over a heterogeneous bundle of transactions
within an HS line, country and month. It is **not** a transaction price. It moves
with product mix, quality, contract timing and unit-of-measure changes as well
as with prices. Every unit value this project constructs is labelled as a
customs unit value, and the reporting layer refuses to call it a price.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import polars as pl

from .base import (
    SourceUnavailable,
    cached_get,
    has_env,
    require_env,
)

BASE = "https://api.census.gov/data/timeseries/intltrade/imports/hs"
VARIABLES_URL = f"{BASE}/variables.json"
KEY_ENV = "CENSUS_API_KEY"
KEY_SIGNUP = "https://api.census.gov/data/key_signup.html"

CHINA = "5700"

#: Variables requested for the import panel. Verified against variables.json at
#: runtime by :func:`verify_schema`.
DEFAULT_VARIABLES = [
    "CTY_CODE",
    "CTY_NAME",
    "I_COMMODITY",
    "I_COMMODITY_SDESC",
    "COMM_LVL",
    "GEN_VAL_MO",
    "CON_VAL_MO",
    "DUT_VAL_MO",
    "CAL_DUT_MO",
    "CON_CHA_MO",
    "CON_QY1_MO",
    "UNIT_QY1",
    "CON_QY2_MO",
    "UNIT_QY2",
    "SUMMARY_LVL",
]

NUMERIC_VARS = {
    "GEN_VAL_MO",
    "CON_VAL_MO",
    "DUT_VAL_MO",
    "CAL_DUT_MO",
    "CON_CHA_MO",
    "CON_QY1_MO",
    "CON_QY2_MO",
}


@dataclass(frozen=True, slots=True)
class CensusQuery:
    year: int
    month: int
    commodity_level: str = "HS6"
    commodities: tuple[str, ...] = ()
    countries: tuple[str, ...] = ()
    variables: tuple[str, ...] = tuple(DEFAULT_VARIABLES)

    @property
    def period(self) -> str:
        return f"{self.year:04d}-{self.month:02d}"


def available() -> bool:
    return has_env(KEY_ENV)


def verify_schema(requested: list[str], *, force: bool = False) -> tuple[list[str], list[str]]:
    """Check requested variables against the endpoint's live ``variables.json``.

    Returns ``(valid, unknown)``. Called before any data pull so a renamed
    variable fails loudly at the schema step instead of producing a column of
    nulls.
    """
    res = cached_get(VARIABLES_URL, "census_imports_hs_variables.json", subdir="census", force=force)
    doc = json.loads(res.path.read_text())
    known = set(doc.get("variables", {}))
    valid = [v for v in requested if v in known]
    unknown = [v for v in requested if v not in known]
    return valid, unknown


def _check_payload(text: str, url_desc: str) -> list[list[str]]:
    stripped = text.lstrip()
    if stripped.startswith("<"):
        lowered = stripped[:400].lower()
        if "missing key" in lowered or "invalid key" in lowered:
            raise SourceUnavailable(
                f"Census returned an HTML key error for {url_desc}. The endpoint requires a "
                f"valid API key in {KEY_ENV}. Register free at {KEY_SIGNUP}."
            )
        raise SourceUnavailable(f"Census returned HTML rather than JSON for {url_desc}")
    try:
        rows = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SourceUnavailable(f"Census response for {url_desc} is not JSON: {exc}") from None
    if not rows or not isinstance(rows, list):
        raise SourceUnavailable(f"Census returned an empty result for {url_desc}")
    return rows


def fetch_month(query: CensusQuery, *, force: bool = False) -> pl.DataFrame:
    """Fetch one month of import data. Requires ``CENSUS_API_KEY``."""
    key = require_env("U.S. Census international trade API", KEY_ENV, KEY_SIGNUP)

    params: list[tuple[str, str]] = [
        ("get", ",".join(query.variables)),
        ("YEAR", f"{query.year:04d}"),
        ("MONTH", f"{query.month:02d}"),
        ("COMM_LVL", query.commodity_level),
        ("key", key),
    ]
    for c in query.commodities:
        params.append(("I_COMMODITY", c))
    for c in query.countries:
        params.append(("CTY_CODE", c))

    tag_bits = [
        query.period,
        query.commodity_level,
        f"c{len(query.commodities)}",
        f"k{len(query.countries)}",
    ]
    res = cached_get(
        BASE,
        f"census_imports_{'_'.join(tag_bits)}.json",
        params=params,
        subdir="census",
        timeout=240.0,
        force=force,
    )
    rows = _check_payload(res.path.read_text(), f"{query.period} {query.commodity_level}")
    header, *body = rows
    df = pl.DataFrame({h: [r[i] for r in body] for i, h in enumerate(header)})
    return _coerce(df, query)


def _coerce(df: pl.DataFrame, query: CensusQuery) -> pl.DataFrame:
    exprs = []
    for c in df.columns:
        if c in NUMERIC_VARS:
            exprs.append(pl.col(c).cast(pl.Float64, strict=False).alias(c))
        else:
            exprs.append(pl.col(c).cast(pl.String, strict=False).alias(c))
    out = df.with_columns(exprs)
    return out.with_columns(
        pl.lit(date(query.year, query.month, 1)).alias("month_date"),
        pl.lit(query.period).alias("period"),
    )


def iter_months(start: str, end: str) -> Iterator[tuple[int, int]]:
    """Yield ``(year, month)`` inclusive between ``YYYY-MM`` bounds."""
    sy, sm = (int(x) for x in start.split("-"))
    ey, em = (int(x) for x in end.split("-"))
    y, m = sy, sm
    while (y, m) <= (ey, em):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def fetch_range(
    start: str,
    end: str,
    *,
    commodities: list[str],
    countries: list[str],
    commodity_level: str = "HS6",
    out_dir: Path | None = None,
    max_calls: int = 500,
) -> list[Path]:
    """Incrementally fetch a month range, one partition file per month.

    Writes partitioned Parquet so no month is re-downloaded and the full panel
    never has to be held in memory.
    """
    from ..paths import STAGED

    out_dir = out_dir or (STAGED / "census_imports")
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    calls = 0
    for y, m in iter_months(start, end):
        target = out_dir / f"year={y}" / f"month={m:02d}" / "part.parquet"
        if target.exists():
            written.append(target)
            continue
        if calls >= max_calls:
            break
        q = CensusQuery(
            year=y,
            month=m,
            commodity_level=commodity_level,
            commodities=tuple(commodities),
            countries=tuple(countries),
        )
        df = fetch_month(q)
        target.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(target)
        written.append(target)
        calls += 1
    return written
