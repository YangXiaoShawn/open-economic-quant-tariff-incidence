"""Census import concordance: 10-digit HTS to NAICS.

Source: ``https://www.census.gov/foreign-trade/reference/codes/concordance/``,
files ``impconcordNN.xls[x]`` where NN is the two-digit year. Public, no key.

This replaces the hand-built HS2-chapter map that industry exposure previously
relied on (D-011). That map assigned whole chapters to a single BEA commodity
and was labelled ``COARSE_APPROXIMATION`` because within-chapter heterogeneity
was lost. The official concordance is keyed on the **10-digit commodity code** —
exactly the level this project's panel is built at — and gives each line one
6-digit NAICS industry, so no weighting assumption is required at all.

Two things worth knowing before using it.

**Vintage matters.** Census publishes one file per year because commodity codes
and their NAICS assignments change. ``impconcord19`` is the 2019 vintage. Mixing
a 2020 concordance into a 2018 panel would silently misassign lines that were
renumbered, so the vintage actually used is recorded in the manifest.

**NAICS codes here are not always six clean digits.** Census writes an ``X`` in
positions where it aggregates detail it does not publish separately, e.g.
``11211X``. Those are kept verbatim rather than coerced: the ``X`` is
information about what Census would not disclose, and silently truncating it to
a shorter code would assert a precision the source declines to give.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import polars as pl

from .base import cached_get

CONCORDANCE_BASE = "https://www.census.gov/foreign-trade/reference/codes/concordance"

#: Two-digit year -> filename. Census switched extension in 2020.
_FILENAMES = {
    17: "impconcord17.xls",
    18: "impconcord18.xls",
    19: "impconcord19.xls",
    20: "impconcord20.xlsx",
    21: "impconcord21.xlsx",
    22: "impconcord22.xlsx",
}

_NAICS_OK = re.compile(r"^[0-9X]{2,6}$")


@dataclass(slots=True)
class ConcordanceLoad:
    """A parsed concordance plus what it could not resolve."""

    vintage_year: int
    source_file: str
    mapping: pl.DataFrame
    """hs10, naics, unit_qy1, end_use, sitc."""
    n_rows: int = 0
    n_unmapped: int = 0
    n_aggregated_naics: int = 0
    """Rows whose NAICS carries an X, i.e. Census aggregated undisclosed detail."""
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, str]:
        return dict(
            zip(
                self.mapping["hs10"].to_list(),
                self.mapping["naics"].to_list(),
                strict=True,
            )
        )


def fetch_concordance(vintage_year: int, *, force: bool = False) -> Path:
    """Download one vintage of the import concordance."""
    yy = vintage_year % 100
    if yy not in _FILENAMES:
        raise ValueError(
            f"no concordance filename known for 20{yy:02d}; available: "
            + ", ".join(f"20{k:02d}" for k in sorted(_FILENAMES))
        )
    name = _FILENAMES[yy]
    res = cached_get(
        f"{CONCORDANCE_BASE}/{name}",
        name,
        subdir="census_concordance",
        timeout=300.0,
        force=force,
    )
    return res.path


def parse_concordance(path: Path, vintage_year: int) -> ConcordanceLoad:
    """Parse an ``impconcord`` workbook into an HS10 -> NAICS table.

    Pure function over a local file, so it runs offline in the test suite.
    """
    import openpyxl

    if path.suffix.lower() == ".xls":
        raise ValueError(
            f"{path.name} is the legacy .xls format, which openpyxl cannot read. "
            "Use a .xlsx vintage (2020 onward) or convert the file first; this is "
            "surfaced rather than silently skipped because using a different "
            "vintage than intended would misassign renumbered commodity codes."
        )

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet = next(
        (s for s in wb.sheetnames if s.lower().startswith("impconcord")), wb.sheetnames[-1]
    )
    ws = wb[sheet]
    rows = ws.iter_rows(values_only=True)
    header = [str(h).strip().lower() if h is not None else "" for h in next(rows)]

    def col(name: str) -> int:
        try:
            return header.index(name)
        except ValueError as exc:
            raise ValueError(
                f"{path.name}: expected column {name!r}; found {header}"
            ) from exc

    i_c, i_n = col("commodity"), col("naics")
    i_u = header.index("unit_qy1") if "unit_qy1" in header else None
    i_e = header.index("end_use") if "end_use" in header else None
    i_s = header.index("sitc") if "sitc" in header else None

    recs: list[dict] = []
    unmapped = 0
    aggregated = 0
    for r in rows:
        if r is None or r[i_c] is None:
            continue
        hs10 = str(r[i_c]).strip().replace(".", "")
        if not hs10.isdigit() or len(hs10) != 10:
            continue
        naics_raw = r[i_n]
        naics = str(naics_raw).strip().upper() if naics_raw is not None else ""
        if not naics or not _NAICS_OK.match(naics):
            unmapped += 1
            continue
        if "X" in naics:
            aggregated += 1
        recs.append(
            {
                "hs10": hs10,
                "naics": naics,
                "unit_qy1": (str(r[i_u]).strip() if i_u is not None and r[i_u] else ""),
                "end_use": (str(r[i_e]).strip() if i_e is not None and r[i_e] else ""),
                "sitc": (str(r[i_s]).strip() if i_s is not None and r[i_s] else ""),
            }
        )
    wb.close()

    mapping = pl.DataFrame(recs).unique(subset=["hs10"], keep="first")
    load = ConcordanceLoad(
        vintage_year=vintage_year,
        source_file=path.name,
        mapping=mapping,
        n_rows=mapping.height,
        n_unmapped=unmapped,
        n_aggregated_naics=aggregated,
    )
    if unmapped:
        load.warnings.append(
            f"{unmapped} commodity lines carry no usable NAICS code and are excluded"
        )
    if aggregated:
        load.warnings.append(
            f"{aggregated} lines map to a NAICS code containing 'X', where Census "
            "aggregates detail it does not disclose; kept verbatim, not truncated"
        )
    return load


# --------------------------------------------------------------------------- #
# NAICS -> BEA summary industry
# --------------------------------------------------------------------------- #

#: BEA summary industries that combine several NAICS 3- or 4-digit groups.
#: Taken from BEA's published summary-level definitions rather than inferred, so
#: each entry is a documented aggregation and not a judgement call. Anything not
#: listed here falls back to its NAICS 3-digit prefix, which is what the
#: remaining BEA manufacturing codes (321, 322, ... 339) already are.
_BEA_COMPOSITES: dict[str, tuple[str, ...]] = {
    "111CA": ("111", "112"),
    "113FF": ("113", "114", "115"),
    "211": ("211",),
    "212": ("212",),
    "213": ("213",),
    "311FT": ("311", "312"),
    "313TT": ("313", "314"),
    "315AL": ("315", "316"),
    "3361MV": ("3361", "3362", "3363"),
    "3364OT": ("3364", "3365", "3366", "3369"),
}

#: BEA summary manufacturing industries that are exactly a NAICS 3-digit group.
_BEA_DIRECT = (
    "321", "322", "323", "324", "325", "326", "327",
    "331", "332", "333", "334", "335", "337", "339",
)


def naics_to_bea_summary(naics: str) -> str | None:
    """Map a NAICS code to a BEA summary industry, or ``None`` if unmapped.

    Longest match first, so a 4-digit composite such as 3361 wins over the
    3-digit fallback 336. Codes containing Census's ``X`` still map whenever the
    disclosed prefix is long enough to be unambiguous; where it is not, the
    result is ``None`` rather than a guess.
    """
    if not naics:
        return None
    code = naics.strip().upper()

    for bea, prefixes in _BEA_COMPOSITES.items():
        for p in sorted(prefixes, key=len, reverse=True):
            if code.startswith(p):
                return bea
    for p in _BEA_DIRECT:
        if code.startswith(p):
            return p
    if code[:3].isdigit() and code[:2] in {"11", "21", "22", "23", "42", "48", "49"}:
        return code[:3]
    return None


def build_hs10_to_bea(load: ConcordanceLoad) -> tuple[pl.DataFrame, dict[str, Any]]:
    """Extend an HS10 -> NAICS mapping to HS10 -> BEA summary industry."""
    m = load.mapping.with_columns(
        pl.col("naics")
        .map_elements(naics_to_bea_summary, return_dtype=pl.String)
        .alias("bea_summary")
    )
    mapped = m.filter(pl.col("bea_summary").is_not_null())
    warnings: list[str] = list(load.warnings)
    quality: dict[str, Any] = {
        "vintage_year": load.vintage_year,
        "source_file": load.source_file,
        "n_hs10_lines": load.n_rows,
        "n_mapped_to_bea": mapped.height,
        "n_unmapped_to_bea": load.n_rows - mapped.height,
        "share_mapped": mapped.height / load.n_rows if load.n_rows else None,
        "n_distinct_naics": int(m["naics"].n_unique()),
        "n_distinct_bea": int(mapped["bea_summary"].n_unique()),
        "n_aggregated_naics": load.n_aggregated_naics,
        "warnings": warnings,
        "method": (
            "Official Census import concordance at the 10-digit commodity level, then "
            "NAICS to BEA summary industry by BEA's published summary definitions. No "
            "weighting assumption is involved: each 10-digit line carries exactly one "
            "NAICS code."
        ),
    }
    if quality["n_unmapped_to_bea"]:
        warnings.append(
            f"{quality['n_unmapped_to_bea']} lines have a NAICS outside the BEA summary "
            "manufacturing and primary-sector groups (services, government, unclassified) "
            "and are excluded from industry exposure rather than forced into a bucket"
        )
    return m, quality
