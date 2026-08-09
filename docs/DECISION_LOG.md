# Decision log

Every non-obvious choice, why it was made, and what it costs. Entries are
append-only; superseded entries are marked, not deleted.

---

### D-001 — Anchor annex parsing on the operative legal sentence

**Decision.** Section 301 product lists are extracted by locating the sentence
*"Heading 9903.88.0X applies to all products of China that are classified in the
following 8-digit subheadings"* and reading the code grid that follows, rather
than by page ranges or by parsing the descriptive annex.

**Why.** That sentence is what imposes the duty. The descriptive annex in the
same notice states that its product descriptions "are provided for informational
purposes only, and are not intended to delimit in any way the scope of the
action". Parsing the informational annex would extract a list the notice itself
disclaims. The Chapter 99 heading in the anchor also identifies the action, so
the action id is read out of the document rather than assumed.

**Cost.** List 4 notices (84 FR 43304) use a different construction and
enumerate 10-digit statistical lines, so this parser raises on them rather than
producing a wrong answer. See D-008.

---

### D-002 — Validate parsed line counts against the count each notice states

**Decision.** After parsing, compare the number of lines found against the count
the notice states in its own preamble ("5,745 full and partial tariff
subheadings"). Mismatches are recorded on the parse result and propagate into the
dataset manifest.

**Why.** Validating against a number the author supplies from memory validates
the memory, not the parser. The notice's own count is an independent check
present in the source.

**Outcome.** All three parsed lists reconcile exactly: List 1 = 818, List 2 =
279, List 3 = 5,745 (5,734 full + 11 partial). Reaching that required D-003,
D-004 and D-005.

---

### D-003 — Exclude Chapter 98 and 99 codes from product lists

**Decision.** Codes in chapters 98 and 99 found inside an annex are recorded as
`special_provision_codes`, not as covered products.

**Why.** 9802.00.80 (articles assembled abroad from U.S. components) and
9903.88.0X (the Section 301 headings themselves) appear in the legal text as
provisions, not as targeted products. Including them overstated List 2 by one
line (280 vs the stated 279).

---

### D-004 — Parse partial statutory lines as first-class records

**Decision.** U.S. note 20(g) to subchapter III of chapter 99 (heading
9903.88.04) covers 11 HS8 lines *except* for named 10-digit statistical
reporting numbers. These are parsed into records with `partial_line=True` and
the carved-out statistical numbers recorded in `partial_line_note`.

**Why.** They are what the notice means by "full and **partial** tariff
subheadings". Without them List 3 parses to 5,734 against a stated 5,745. More
importantly, marking a partially covered line as fully treated introduces
measurement error directly into the treatment variable.

**Cost.** The engine returns `PARTIAL_LINE` for these, which is deliberately not
usable as a scalar treatment, so they leave the main estimation sample.

---

### D-005 — Never repair a truncated code by guessing; resolve it only by deduction

**Decision.** In 83 FR 28710 one code renders as `9033.00`, its final pair lost
in typesetting. The parser reports it as `unresolved_codes` and omits it. A
separate resolver consults the USITC HTS and resolves it **only** when exactly
one 8-digit line under that heading is not already claimed. The resolved record
is marked `Confidence.DERIVED`, not `OFFICIAL_PARSED`.

**Why.** Filling in `.90` because it "looks right" is fabrication. Deducing it
from the HTS, where 9033.00.20 and 9033.00.30 are already in the list and
9033.00.90 is the only other line under the heading, is an argument from an
official source that a reader can check.

**Cost.** Ambiguous truncations stay unresolved and are reported as a known
undercount.

---

### D-006 — Whitespace repair inside codes is allowed; digit invention is not

**Decision.** `_normalize_page` rejoins `9401. 71.0007` into `9401.71.0007`.

**Why.** Joining across whitespace adds no digits — it recovers a code the
source contains. The pattern requires a full 4-digit heading before the break
and 2+2 or 2+4 digits after, so ordinary sentence punctuation ("in 2018. 5,745
lines") cannot match. There is a regression test for exactly that case.

---

### D-007 — Announcement dates are set to the proposal, not the final notice

**Decision.** For List 2, the announcement date is 2018-06-20 (the proposal in
83 FR 28710 Annex C), not 2018-08-16 (the final notice). For List 3 it is
2018-07-17 (83 FR 33608). Effective dates are always the date duties were
collected.

**Why.** Anticipation and front-running respond to the first public signal.
Setting announcement equal to the final notice would understate the anticipation
window by weeks. Setting effective equal to announcement would misplace the cost
shock by months — for the List 3 rate increase, by more than seven, since it was
announced for 2019-01-01, postponed twice, and took effect 2019-05-10.

---

### D-008 — Restrict the vertical slice to Lists 1–3 and end the window 2019-08

**Decision.** List 4A (effective 2019-09-01) is not parsed. The sample window
ends 2019-08.

**Why.** List 4A covers most remaining consumer goods. Running past its
effective date without parsing it would place genuinely treated products in the
never-treated control group, which biases every estimate toward zero and is
worse than a shorter window.

**Cost.** No estimates covering the 2019-09 onward period, and no coverage of the
2020-02-14 reduction to 7.5%. Recorded as a known gap in the episode config.

---

### D-009 — Census API requires a key that is unavailable; use a labelled synthetic generator

> **SUPERSEDED 2026-08-09.** A key was supplied and verified against the live
> endpoint. The panel is now built from official Census data and carries
> provenance `OFFICIAL`. The synthetic generator remains in the codebase and is
> still exercised by the test suite and by `--force-synthetic`, because
> validating estimators against a known data-generating process is worth keeping
> regardless of data availability. The entry below records the state that held
> while no key existed. See D-019 for what the first live pull revealed.

**Decision.** The Census `timeseries/intltrade/imports/hs` endpoint now requires
an API key (an unauthenticated request returns an HTML "Missing Key" page with
HTTP 200). No key is available in this environment. The adapter is fully
implemented and key-gated; when no key is present, the pipeline generates trade
flows from a documented synthetic DGP and tags every downstream artefact
`MIXED` or `SYNTHETIC_PIPELINE_VALIDATION`.

**Why.** The alternative to a labelled simulation is either abandoning the
vertical slice or producing plausible-looking numbers with no provenance. The
second is fabrication. A simulation whose parameters are declared in advance
lets the estimation code be validated against a known answer, which is a real
result about the code even though it is not a result about the world.

**Cost.** No empirical finding about U.S. trade exists in this repository yet.
This is the single binding constraint on the project. The moment
`CENSUS_API_KEY` is set, `make build-trade-panel` uses official data and the
provenance tags flip to `OFFICIAL` with no change to estimation code.

**Detection.** The adapter inspects the payload shape rather than the HTTP
status, because Census returns 200 with an HTML error body.

---

### D-010 — USITC HTS serves the current vintage, not HTS2018

**Decision.** Baseline MFN rates and HS6→HS8 child maps come from the live USITC
HTS endpoint, which serves the current schedule.

**Why.** It is keyless, official and machine-readable, and no archived 2018
vintage is available through the same interface.

**Cost.** A vintage mismatch: Section 301 lists are HTS2018 while baselines are
current. Lines added or retired since 2018 are mismatched. Recorded in the panel
manifest. Fixing it requires an archived HTS2018 release.

---

### D-011 — Census HS-to-NAICS concordance unavailable; use a coarse chapter map

**Decision.** The Census foreign-trade reference concordance URLs returned HTTP
404/403. Industry mapping falls back to a hand-built HS2-chapter → BEA summary
commodity map in `config/io_concordance.yaml`, with `status:
COARSE_APPROXIMATION`.

**Cost.** Within-chapter heterogeneity is lost, so industry exposure is
attenuated and the magnitudes are not usable as elasticities or as welfare
inputs. Exposure results are explicitly labelled a qualitative ordering. Every
report carrying them states the concordance status.

---

### D-012 — Day-weight the tariff rate within a month

**Decision.** The panel carries a day-weighted average statutory rate over each
calendar month, alongside month-start and month-end variants.

**Why.** List 3 took effect on 24 September 2018 — 7 of that month's 30 days.
Assessing at month start labels September untreated; assessing at month end
labels it fully treated. Both errors land on the event-time-zero coefficient,
which is the one readers look at hardest. Day weighting also matters for the
2019-05-10 rate increase.

**Evidence it matters.** Before this change the synthetic ground-truth recovery
was visibly attenuated because the generator and the panel builder disagreed
about May 2019. Both now use the same convention and it is tested.

---

### D-013 — Missing MFN baselines stay null

**Decision.** An HS6 heading containing any HS8 child with a compound or
specific duty has no single ad valorem baseline. Those rows carry a null
`total_modeled_tariff_rate`.

**Why.** An earlier version filled the null with zero when constructing
`log1p_total_tariff`, which asserted "no tariff" for 38% of rows and attenuated
every total-rate estimate. That is exactly the silent fill this project forbids.

**Consequence.** The primary treatment variable is `log1p_additional_tariff`,
which isolates the policy variation and is defined everywhere. The total-rate
specification runs on the subsample with a defined baseline and is reported
beside it rather than merged.

---

### D-014 — Two event-study reference periods, always

**Decision.** Event studies are estimated with reference period −1 and −3, and
both are reported.

**Why.** Event month −1 is the month most exposed to front-running ahead of a
known effective date. If importers pull shipments forward, the reference period
is itself treated and every coefficient shifts. Disagreement between the two is
diagnostic information, not noise to be resolved by picking one.

---

### D-015 — Pre-trend tests report significance and magnitude separately

**Decision.** `pretrend_test` returns a verdict combining statistical
detectability with magnitude relative to the mean post-treatment coefficient.

**Why.** In a large panel, standard errors shrink until economically trivial
pre-period movement is "significant". A rule that discards any design with a
significant pre-coefficient discards good work; a rule that ignores magnitude
accepts bad work. Reporting one number invites the reader to apply whichever
rule suits them.

---

### D-016 — The raw diversion decomposition is not the headline

**Decision.** The pre-versus-post decomposition is reported alongside a
counterfactual-adjusted version that nets out, country by country, the growth of
never-treated products over the same calendar months.

**Why.** The raw comparison credits ordinary trade growth to the tariff. In the
current run it produces a replacement ratio near 10, which is not interpretable.
The adjusted figure is a difference-in-differences version resting on the same
parallel-trends assumption as the event study, stated explicitly.

---

### D-017 — Defer the structural module

**Decision.** No Armington/CES module has been implemented.

**Why.** The brief requires the reduced-form vertical slice to be stable and
passing tests first. It now is, but calibrating a structural model on synthetic
trade flows would produce counterfactuals with no informational content while
carrying the appearance of substance. The module is specified in
`docs/PROJECT_PLAN.md` (M8) and gated behind official data.

---

### D-018 — The claim guard is part of the build, not documentation

**Decision.** `guard_language` raises on causal assertions under non-official
provenance and on quantified welfare claims under any provenance, and it runs on
every generated report.

**Why.** A rule written in a style guide gets violated. A rule that fails the
build does not. During development it caught two of this project's own generated
sentences; both were rephrased rather than the guard weakened.

**Design note.** It distinguishes assertions ("the tariff caused") from
vocabulary used to *discuss* evidential status ("which conclusions are causal"),
because the executive memo is required to answer that question.

---

### D-019 — Census reports no quantity at HS6; the panel moves to HS10

**Decision.** The analytical panel is built at 10-digit statistical lines. An HS6
panel is still produced, by aggregation, for comparison across aggregation
levels.

**Why.** This was discovered on the first live pull after a Census API key
became available, not reasoned about in advance. At ``COMM_LVL=HS6`` the
endpoint returns ``CON_QY1_MO = 0`` and ``UNIT_QY1 = "-"`` for every line,
because the 10-digit lines beneath an HS6 heading carry different units of
measure (pieces, kilograms, dozens) and Census will not add them. Verified
across chapters 39, 73, 84, 87 and 94.

Without quantity there is no unit value, and without unit values the two central
incidence outcomes — the tariff-exclusive customs unit value and the
duty-inclusive landed unit value — do not exist. An HS6 panel can support value
and duty outcomes only, which cannot answer who bears the tariff.

**Second reason, independent of the first.** Section 301 is legislated at HS8,
and 10-digit statistical lines nest exactly within HS8. At HS10 the
partial-coverage problem simply does not arise: the 598 HS6 headings previously
excluded because only some of their HS8 children were covered can all re-enter
the sample, correctly classified. Superseding the exclusion described in
D-013's neighbourhood is a strict improvement in both coverage and precision.

**Cost.** Roughly an order of magnitude more rows, and 320 API calls instead of
32. Mitigated by chapter-prefix wildcard queries (``I_COMMODITY=84*``), one
Parquet partition per chapter-month, and never re-fetching an existing
partition.

**Unexpected benefit.** Census emits explicit zero rows for country-product
combinations with no trade, so the extensive margin is *observed* rather than
inferred from a missing record. This partially retires the ``PANEL_GAPS``
caveat, which previously had to say that absence and true zero were
indistinguishable.

---

### D-020 — HS6 aggregates refuse to sum quantities across unlike units

**Decision.** When aggregating HS10 to HS6, values always add. Quantities add
only when every constituent 10-digit line in that HS6-country-month reports the
same unit of measure. Otherwise the aggregate quantity is null and
``hs6_units_mixed`` is set.

**Why.** Adding pieces to kilograms produces a number, and dividing value by it
produces a unit value that moves with product mix rather than with price. That
is exactly the measurement artefact this project exists to avoid, and it is
precisely how a careless HS6 panel would manufacture a spurious "price" effect.

**Cost.** A meaningful share of HS6-country-months carry no unit value. That is
the honest representation of what the data supports, and it is recorded on the
panel rather than hidden.

---

### D-021 — Tariff assessments are keyed on the 8-digit line, not the observation

**Decision.** ``attach_tariff_treatment`` computes one assessment per distinct
(HS8, country, month) and joins it onto the observations.

**Why.** Correctness first: every HS10 child of an HS8 parent is subject to the
same statute, so keying on HS8 is exact, not an approximation. Performance
follows: on a full HS10 panel this turns roughly 1.4 million engine calls into a
few tens of thousands. ``_month_segments`` was also changed to use the engine's
prebuilt (HS8, country) index instead of scanning all 12,587 records per call,
which was O(n x records) and would not have completed.

A regression test asserts that HS10 siblings under one HS8 parent receive
identical rates and statuses.
