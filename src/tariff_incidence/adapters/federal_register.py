"""Federal Register adapter: Section 301 tariff actions.

The Federal Register is the authoritative publication for USTR Section 301
actions. Its public API (no key required) gives document metadata; the annexes
listing covered tariff lines are only rendered in the GPO typeset PDF, so the
product lists are extracted from those PDFs.

Parsing strategy
----------------

We anchor on the *operative legal sentence* rather than on page numbers or
visual layout::

    Heading 9903.88.01 applies to all products of China that are classified
    in the following 8-digit subheadings:

That sentence is what actually imposes the duty. Anchoring on it means the
parser extracts the legally covered lines, not the "informational" annex whose
own text disclaims that it delimits the scope of the action. The Chapter 99
heading in the anchor also identifies the action, so the action id is read out
of the document instead of being assumed.

Codes are collected from the anchor page forward while pages remain code grids,
stopping at the next annex heading. Parsed line counts are then checked against
the count the notice itself states in prose; a mismatch is recorded on the
result rather than suppressed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

from ..provenance import sha256_file
from ..tariff.records import Confidence, RecordType, SourceRef, TariffRecord
from .base import FetchResult, cached_get

FR_API = "https://www.federalregister.gov/api/v1/documents"
GOVINFO_PDF = "https://www.govinfo.gov/content/pkg/FR-{ymd}/pdf/{doc}.pdf"

CHINA_CENSUS_CODE = "5700"

# The operative sentence. Tolerant of the line breaks PDF extraction inserts.
_ANCHOR = re.compile(
    r"[Hh]eading\s+(9903\.88\.\d{2})\s+applies\s+to\s+all\s+products\s+of\s+China\s+that\s+are\s+"
    r"classified\s+in\s+the\s+following\s+8-?digit\s+subheadings",
    re.IGNORECASE,
)
_ANNEX_HEAD = re.compile(r"(?m)^\s*ANNEX\s+[B-Z]\b")
_HTS8 = re.compile(r"\b(\d{4})\.(\d{2})\.(\d{2})\b")
_HTS10 = re.compile(r"\b(\d{4})\.\s?(\d{2})\.\s?(\d{2})\.?(\d{2})\b")
# A code whose final two digits were lost in typesetting, e.g. "9033.00" at a
# column edge. Never repaired by guessing -- reported as unresolved.
_TRUNCATED = re.compile(r"(?<![\d.])(\d{4}\.\d{2})(?![.\d])")
# "approximately 818 tariff lines" / "5,745 full and partial tariff subheadings"
_STATED_COUNT = re.compile(
    r"(?:approximately\s+)?([\d,]{3,7})\s+(?:full\s+and\s+partial\s+)?tariff\s+"
    r"(?:lines|subheadings)",
    re.IGNORECASE,
)
# Partial-line construction in a U.S. note:
#   "... provided for in 2931.90.90, except for such compounds provided for in
#    statistical reporting number 2931.90.9051;"
_PARTIAL_ITEM = re.compile(
    r"provided\s+for\s+in\s+(\d{4}\.\d{2}\.\d{2})\s*,\s*except\s+for\s+such\s+[^;]{0,90}?"
    r"provided\s+for\s+in\s+statistical\s+reporting\s+numbers?\s+([^;]{0,160})",
    re.IGNORECASE | re.DOTALL,
)
_NOTE_HEADER = re.compile(
    r"For\s+the\s+purposes\s+of\s+heading\s+(9903\.88\.\d{2})\s*,\s*products\s+of\s+China",
    re.IGNORECASE,
)

# Chapters 98 and 99 are special classification provisions, not product lines.
_SPECIAL_CHAPTERS = ("98", "99")


def _normalize_page(text: str) -> str:
    """Collapse whitespace so codes split across line or column breaks re-join.

    GPO typesetting occasionally splits a code as ``9401. 71.0007``. Joining on
    whitespace inside an otherwise well-formed code is a safe repair: it adds no
    digits. Codes missing digits entirely are never repaired.
    """
    t = text.replace(" ", " ")
    # "9401. 71.0007" / "9401.\n71.0007" -> "9401.71.0007". Requires a full
    # 4-digit heading before the break and 2+2 or 2+4 digits after, so ordinary
    # sentence punctuation ("in 2018. 5,745 lines") cannot match.
    t = re.sub(r"(\d{4})\.\s*\n?\s*(\d{2}\.\d{2,4})\b", r"\1.\2", t)
    t = re.sub(r"(\d{4}\.)\s*\n?\s*(\d{2}\.)\s*\n?\s*(\d{2})\b", r"\1\2\3", t)
    t = re.sub(r"(\d{4}\.\d{2}\.\d{2})\.\s*(\d{2})\b", r"\1.\2", t)
    return t


@dataclass(slots=True)
class FRDocument:
    """Metadata for one Federal Register document."""

    document_number: str
    citation: str
    title: str
    publication_date: str
    html_url: str
    pdf_url: str
    agencies: list[str] = field(default_factory=list)

    @property
    def ymd(self) -> str:
        return self.publication_date

    def source_ref(self, checksum: str, locator: str = "") -> SourceRef:
        return SourceRef(
            document_id=self.document_number,
            citation=self.citation,
            title=self.title,
            url=self.html_url,
            publication_date=self.publication_date,
            checksum_sha256=checksum,
            page_or_locator=locator,
        )


@dataclass(slots=True)
class AnnexParse:
    """Result of extracting one action's covered tariff lines from a notice."""

    document_number: str
    chapter99_heading: str
    hts8_codes: list[str]
    anchor_page: int
    last_page: int
    stated_line_count: int | None
    parsed_line_count: int
    count_matches_notice: bool | None
    warnings: list[str] = field(default_factory=list)
    partial_lines: dict[str, list[str]] = field(default_factory=dict)
    """HS8 line -> 10-digit statistical numbers carved *out* of the duty."""
    unresolved_codes: list[str] = field(default_factory=list)
    """Codes seen truncated in the source rendering and deliberately not repaired."""
    special_provision_codes: list[str] = field(default_factory=list)
    """Chapter 98/99 codes seen in the annex; legal provisions, not product lines."""

    @property
    def discrepancy(self) -> int | None:
        if self.stated_line_count is None:
            return None
        return self.parsed_line_count - self.stated_line_count

    @property
    def total_full_and_partial(self) -> int:
        return len(set(self.hts8_codes) | set(self.partial_lines))


def fetch_document_metadata(document_number: str, force: bool = False) -> FRDocument:
    """Retrieve FR document metadata via the public API (no key required)."""
    import json

    res = cached_get(
        f"{FR_API}/{document_number}.json",
        f"fr_meta_{document_number}.json",
        params={
            "fields[]": "document_number",
        },
        subdir="federal_register",
        force=force,
    )
    # The single-document endpoint ignores repeated fields[] via dict params, so
    # request the full record and select locally.
    doc = json.loads(res.path.read_text())
    if "citation" not in doc:
        res = cached_get(
            f"{FR_API}/{document_number}.json",
            f"fr_meta_full_{document_number}.json",
            subdir="federal_register",
            force=True,
        )
        doc = json.loads(res.path.read_text())

    return FRDocument(
        document_number=doc["document_number"],
        citation=doc.get("citation") or "",
        title=doc.get("title") or "",
        publication_date=doc.get("publication_date") or "",
        html_url=doc.get("html_url") or "",
        pdf_url=doc.get("pdf_url") or "",
        agencies=[a.get("name", "") for a in doc.get("agencies", [])],
    )


def fetch_notice_pdf(doc: FRDocument, force: bool = False) -> FetchResult:
    """Download the GPO typeset PDF, which is the only rendering carrying annexes."""
    url = doc.pdf_url or GOVINFO_PDF.format(ymd=doc.publication_date, doc=doc.document_number)
    return cached_get(
        url,
        f"{doc.document_number}.pdf",
        subdir="federal_register",
        timeout=420.0,
        force=force,
    )


def _page_texts(pdf_path: Path) -> list[str]:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    return [(p.extract_text() or "") for p in reader.pages]


def parse_annex(
    pdf_path: Path,
    document_number: str,
    *,
    min_codes_per_grid_page: int = 20,
) -> AnnexParse:
    """Extract the covered 8-digit lines for one Section 301 action from a notice PDF.

    Pure function over a local file: runs offline and is exercised against a
    committed fixture in the test suite.
    """
    raw_pages = _page_texts(pdf_path)
    pages = [_normalize_page(t) for t in raw_pages]
    flat = [re.sub(r"[ \t]+", " ", t) for t in pages]

    anchor_page = -1
    heading = ""
    for i, t in enumerate(flat):
        m = _ANCHOR.search(t.replace("\n", " "))
        if m:
            anchor_page, heading = i, m.group(1)
            break
    if anchor_page < 0:
        raise ValueError(
            f"{document_number}: operative anchor sentence not found; this notice does not "
            "use the 8-digit 'applies to all products of China' construction and needs its "
            "own parser (List 4 notices enumerate 10-digit statistical lines instead)"
        )

    warnings: list[str] = []
    codes: list[str] = []
    specials: list[str] = []
    truncated: list[str] = []
    last_page = anchor_page

    for i in range(anchor_page, len(pages)):
        text = pages[i]
        if i > anchor_page and _ANNEX_HEAD.search(text):
            break
        if i > anchor_page and _ANCHOR.search(text.replace("\n", " ")):
            break  # a second action begins in the same document
        found = [f"{a}{b}{c}" for a, b, c in _HTS8.findall(text)]
        products = [c for c in found if c[:2] not in _SPECIAL_CHAPTERS]
        specials.extend(c for c in found if c[:2] in _SPECIAL_CHAPTERS)
        if i > anchor_page and len(products) < min_codes_per_grid_page:
            break
        codes.extend(products)
        # Codes whose last pair was lost in typesetting. Repairing these would
        # mean inventing digits, so they are surfaced instead.
        blanked = _HTS8.sub("", text)
        truncated.extend(
            m.group(1) for m in _TRUNCATED.finditer(blanked) if m.group(1)[:2] not in _SPECIAL_CHAPTERS
        )
        last_page = i

    unique = sorted(set(codes))
    if len(unique) != len(codes):
        warnings.append(
            f"{len(codes) - len(unique)} duplicate code occurrences collapsed "
            "(codes can repeat across column breaks)"
        )

    partials = _parse_partial_lines(pages, anchor_page)
    if partials:
        warnings.append(
            f"{len(partials)} HS8 line(s) are covered only in part, with named 10-digit "
            "statistical numbers carved out; these are flagged partial_line and must not be "
            "treated as fully treated"
        )

    truncated = sorted(set(truncated))
    if truncated:
        warnings.append(
            f"{len(truncated)} code(s) appear truncated in the source rendering "
            f"({', '.join(truncated[:6])}); NOT repaired by guessing, and therefore absent "
            "from the covered-line list. This is a known undercount."
        )

    # Cross-check against the count the notice states in its own preamble.
    preamble = " ".join(flat[: anchor_page + 1]).replace("\n", " ")
    stated: int | None = None
    candidates = [int(m.group(1).replace(",", "")) for m in _STATED_COUNT.finditer(preamble)]
    if candidates:
        # Prefer the candidate closest to what we parsed; notices often mention
        # several counts (proposed vs final, this list vs a prior one).
        stated = min(candidates, key=lambda c: abs(c - len(unique)))
        if len(candidates) > 1:
            warnings.append(
                f"notice preamble states several line counts {sorted(candidates)}; "
                f"compared against the closest ({stated})"
            )

    # The notice's stated count covers "full and partial tariff subheadings", so
    # the comparable parsed figure includes partial lines.
    total = len(set(unique) | set(partials))
    matches = None if stated is None else (stated == total)
    if stated is not None and matches is False:
        warnings.append(
            f"PARSED COUNT {total} (= {len(unique)} full + {len(partials)} partial) != COUNT "
            f"STATED IN NOTICE {stated} (difference {total - stated}). Treat this action's "
            "line list as provisional until reconciled."
        )

    return AnnexParse(
        document_number=document_number,
        chapter99_heading=heading,
        hts8_codes=unique,
        anchor_page=anchor_page,
        last_page=last_page,
        stated_line_count=stated,
        parsed_line_count=total,
        count_matches_notice=matches,
        warnings=warnings,
        partial_lines=partials,
        unresolved_codes=truncated,
        special_provision_codes=sorted(set(specials)),
    )


def _parse_partial_lines(pages: list[str], anchor_page: int) -> dict[str, list[str]]:
    """Extract HS8 lines covered only in part, from the U.S. note that names them.

    The construction is::

        1. Other non-aromatic organo-inorganic compounds, provided for in
           2931.90.90, except for such compounds provided for in statistical
           reporting number 2931.90.9051;

    Returns ``{hs8: [excluded 10-digit statistical numbers]}``. These lines are
    genuinely partially treated: a panel built at HS8 or HS6 that marks them
    fully treated introduces measurement error in the treatment variable.
    """
    out: dict[str, list[str]] = {}
    window = " ".join(pages[anchor_page:])
    window = re.sub(r"\s+", " ", window)
    if not _NOTE_HEADER.search(window):
        return out
    for m in _PARTIAL_ITEM.finditer(window):
        hs8 = m.group(1).replace(".", "")
        tail = m.group(2)
        stat = [
            f"{a}{b}{c}{d}"
            for a, b, c, d in _HTS10.findall(tail)
        ]
        if stat:
            out.setdefault(hs8, [])
            for s in stat:
                if s not in out[hs8]:
                    out[hs8].append(s)
    return out


def annex_to_records(
    annex: AnnexParse,
    doc: FRDocument,
    *,
    episode_id: str,
    action_id: str,
    effective_date: date,
    announcement_date: date,
    ad_valorem_rate: float,
    product_code_vintage: str,
    checksum: str,
    partner_country_code: str = CHINA_CENSUS_CODE,
    record_type: RecordType = RecordType.ADDITIONAL_DUTY,
    expiry_date: date | None = None,
) -> list[TariffRecord]:
    """Convert a parsed annex into one :class:`TariffRecord` per covered line."""
    src = doc.source_ref(checksum, locator=f"pp.{annex.anchor_page}-{annex.last_page} (0-indexed)")
    confidence = (
        Confidence.OFFICIAL_PARSED
        if annex.count_matches_notice is not False
        else Confidence.DERIVED
    )
    out: list[TariffRecord] = []
    full = [c for c in annex.hts8_codes if c not in annex.partial_lines]
    for code in full:
        out.append(
            TariffRecord(
                record_id=f"{action_id}:{code}:{effective_date.isoformat()}:{record_type.value}",
                episode_id=episode_id,
                action_id=action_id,
                record_type=record_type,
                product_code=code,
                product_code_level=8,
                product_code_vintage=product_code_vintage,
                partner_country_code=partner_country_code,
                announcement_date=announcement_date,
                effective_date=effective_date,
                expiry_date=expiry_date,
                ad_valorem_rate=ad_valorem_rate,
                source=src,
                confidence=confidence,
                notes=f"Chapter 99 heading {annex.chapter99_heading}",
                tags=("section301", annex.chapter99_heading),
            )
        )
    for code, carved_out in sorted(annex.partial_lines.items()):
        out.append(
            TariffRecord(
                record_id=f"{action_id}:{code}:{effective_date.isoformat()}:{record_type.value}",
                episode_id=episode_id,
                action_id=action_id,
                record_type=record_type,
                product_code=code,
                product_code_level=8,
                product_code_vintage=product_code_vintage,
                partner_country_code=partner_country_code,
                announcement_date=announcement_date,
                effective_date=effective_date,
                expiry_date=expiry_date,
                ad_valorem_rate=ad_valorem_rate,
                source=src,
                confidence=confidence,
                partial_line=True,
                partial_line_note=(
                    "statistical reporting number(s) carved out of the duty: "
                    + ", ".join(carved_out)
                ),
                partial_line_excluded_codes=tuple(carved_out),
                notes=f"Chapter 99 heading {annex.chapter99_heading} (partial line)",
                tags=("section301", annex.chapter99_heading, "partial_line"),
            )
        )
    return out


def parse_iso(d: str) -> date:
    return datetime.strptime(d, "%Y-%m-%d").date()


def file_checksum(path: Path) -> str:
    return sha256_file(path)
