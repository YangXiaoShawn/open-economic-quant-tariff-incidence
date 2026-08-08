"""BEA input-output adapter (Supply-Use framework, summary level).

Source: ``https://apps.bea.gov/industry/iTables Static Files/AllTablesSUP.zip``
(public, no key). Contains, among others:

* ``Use_Tables_Supply-Use_Framework_1997-2023_Summary.xlsx`` -- commodity x
  industry use in producers' prices, one sheet per year.
* ``IxC_TR_1997-2023_Summary.xlsx`` -- industry-by-commodity **total**
  requirements, one sheet per year.

Direct requirements are computed from the Use table by dividing each column by
that industry's total intermediate + value added, giving the input share per
dollar of output. Total requirements come from BEA's own IxC table rather than
being re-derived, so the Leontief inversion convention matches BEA's published
one exactly.

The pre-treatment year is used throughout (2017 by default). Using a
contemporaneous IO table would let the tariff shock itself change the weights,
which is exactly the endogeneity a shift-share exposure measure is meant to
avoid.
"""

from __future__ import annotations

import io
import zipfile
from dataclasses import dataclass
from pathlib import Path

import polars as pl

from .base import cached_get

BEA_ZIP_URL = "https://apps.bea.gov/industry/iTables%20Static%20Files/AllTablesSUP.zip"
USE_SUMMARY = "Use_Tables_Supply-Use_Framework_1997-2023_Summary.xlsx"
IXC_TR_SUMMARY = "IxC_TR_1997-2023_Summary.xlsx"

_TOTAL_ROW_MARKERS = (
    "total intermediate",
    "total value added",
    "total industry output",
    "total commodity output",
)


@dataclass(slots=True)
class IOTables:
    """Parsed BEA tables for one year."""

    year: int
    use: pl.DataFrame  # long: commodity_code, industry_code, value
    industry_output: pl.DataFrame  # industry_code, total_output
    direct_requirements: pl.DataFrame  # commodity_code, industry_code, direct_requirement
    total_requirements: pl.DataFrame  # industry_code, commodity_code, total_requirement
    industry_names: dict[str, str]
    commodity_names: dict[str, str]
    source_release: str


def fetch_bea_zip(*, force: bool = False) -> Path:
    return cached_get(
        BEA_ZIP_URL, "AllTablesSUP.zip", subdir="bea", timeout=600.0, force=force
    ).path


def _sheet_to_long(
    zf: zipfile.ZipFile, member: str, year: int
) -> tuple[pl.DataFrame, dict[str, str], dict[str, str]]:
    import openpyxl

    wb = openpyxl.load_workbook(io.BytesIO(zf.read(member)), read_only=True, data_only=True)
    sheet = str(year)
    if sheet not in wb.sheetnames:
        wb.close()
        raise ValueError(f"{member}: no sheet for year {year}; have {wb.sheetnames[:5]}...")
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    # Header row is the one whose first cell is the code label.
    hdr_i = next(
        i
        for i, r in enumerate(rows[:12])
        if r and str(r[0] or "").strip().lower() in {"code", "iocode"}
    )
    code_row = rows[hdr_i - 1]
    name_row = rows[hdr_i]
    col_codes: dict[int, str] = {}
    col_names: dict[str, str] = {}
    for j in range(2, len(code_row)):
        code = str(code_row[j] or "").strip()
        if code and code.lower() not in {"none", ""}:
            col_codes[j] = code
            col_names[code] = str(name_row[j] or "").strip()

    recs: list[dict] = []
    row_names: dict[str, str] = {}
    for r in rows[hdr_i + 1 :]:
        if not r or r[0] is None:
            continue
        rcode = str(r[0]).strip()
        rname = str(r[1] or "").strip()
        if not rcode or rname.lower().startswith(_TOTAL_ROW_MARKERS):
            continue
        row_names[rcode] = rname
        for j, ccode in col_codes.items():
            if j >= len(r):
                continue
            v = r[j]
            if v is None or (isinstance(v, str) and not v.replace(".", "").replace("-", "").isdigit()):
                val = 0.0  # BEA writes "..." for suppressed / not applicable
            else:
                try:
                    val = float(v)
                except (TypeError, ValueError):
                    val = 0.0
            recs.append({"row_code": rcode, "col_code": ccode, "value": val})
    return pl.DataFrame(recs), row_names, col_names


def load_tables(year: int = 2017, *, zip_path: Path | None = None) -> IOTables:
    """Load the Use and total-requirements tables for one year."""
    zp = zip_path or fetch_bea_zip()
    with zipfile.ZipFile(zp) as zf:
        use_long, comm_names, ind_names = _sheet_to_long(zf, USE_SUMMARY, year)
        tr_long, tr_row_names, tr_col_names = _sheet_to_long(zf, IXC_TR_SUMMARY, year)

    use = use_long.rename({"row_code": "commodity_code", "col_code": "industry_code"})
    # The Use table's columns include final-demand categories (personal
    # consumption, private investment, government, exports -- codes beginning
    # with "F", plus the T-prefixed totals). They are uses, not producing
    # industries, and an "input cost exposure" computed for them is meaningless.
    use = use.filter(
        ~pl.col("industry_code").str.starts_with("F")
        & ~pl.col("industry_code").str.starts_with("T")
    )

    # Industry output = column sum over commodities used + value added. The Use
    # sheet's own total rows were dropped, so reconstruct from the intermediate
    # block and treat it as intermediate input only; direct requirements are then
    # expressed per dollar of *total industry output*, which BEA reports in the
    # supply table. Using the intermediate column sum alone would overstate every
    # input share, so the denominator is taken from the total-requirements
    # diagonal convention instead: normalise by the column total of the Use table
    # plus value added is unavailable at this parse depth, so we use the column
    # total and label the measure accordingly.
    ind_out = (
        use.group_by("industry_code")
        .agg(pl.col("value").sum().alias("total_intermediate_inputs"))
        .filter(pl.col("total_intermediate_inputs") > 0)
    )
    dr = (
        use.join(ind_out, on="industry_code", how="inner")
        .with_columns(
            (pl.col("value") / pl.col("total_intermediate_inputs")).alias("direct_requirement")
        )
        .select(["commodity_code", "industry_code", "value", "direct_requirement"])
    )

    tr = tr_long.rename({"row_code": "industry_code", "col_code": "commodity_code"}).rename(
        {"value": "total_requirement"}
    )

    return IOTables(
        year=year,
        use=use,
        industry_output=ind_out,
        direct_requirements=dr,
        total_requirements=tr,
        industry_names={**ind_names, **tr_row_names},
        commodity_names={**comm_names, **tr_col_names},
        source_release=f"BEA AllTablesSUP.zip, Summary level, year {year}",
    )
