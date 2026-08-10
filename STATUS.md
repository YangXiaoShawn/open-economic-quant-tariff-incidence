# STATUS

**Last updated:** 2026-08-10 · session 13

## One-line state

Official Census data at HS10, all three Section 301 waves, stacked multi-wave
design, and a pre-trend test that separates bias from imprecision from a
near-null effect. **The incidence account closes**: the tariff was passed
through to the U.S. importer close to in full, with no detectable exporter
absorption, and the bound on the customs unit value is what carries the claim.
Landed cost **CLEAN**; customs unit value a **bounded null** (0.072); quantity
**no detectable differential trend**, qualified reading.

The sections below are in reverse chronological order; earlier sections record
what was true at the time and are superseded by later ones.

## Session 13: the power limit had a published answer

Session 12 closed with the propagation test underpowered at 22 clusters and
three named ways out. The one that costs nothing turned out to be sitting in a
file the project had been downloading since session 8.

BEA publishes **detail-level** input-output tables — roughly 400 industries
against the summary level's 71 — for benchmark years only: 2007, 2012, 2017.
This project's pre-treatment year is 2017, so the finest published industry
breakdown exists exactly where a shift-share design needs its weights. Only the
summary members of `AllTablesSUP.zip` were being read.

| | summary | detail |
|---|---|---|
| BEA industries in the IO table | 71 | 401 |
| panel NAICS codes mapped | 219 → 19 commodities | 211 of 219 |
| customs value covered | 99.8% | 97.8% |
| industries with tariff exposure | 24 | 148 |
| **industries with a matched PPI series** | **22** | **125** |

125 clusters puts cluster-robust inference back inside the range where it
behaves. The wild cluster bootstrap (D-042) stays anyway.

**Three things this turned up that were not the point.** Each is in D-043.

1. *BEA already publishes the hierarchy I hand-coded.* Every detail workbook
   ships a `NAICS Codes` sheet with BEA's own Sector/Summary/U.Summary/Detail
   nesting. `bls_ppi.BEA_TO_NAICS` was hand-written in session 12 — the same
   mistake in kind as D-011 and D-037. Checked against the published sheet, it
   **agrees exactly**, so no prior result changes; a test now holds it there.
2. *The two workbooks disagree on header row order.* Summary writes codes above
   the label row, detail below it. Taking them by position returned industry
   *titles* where codes belonged, and nothing would have raised — the downstream
   join would simply have matched nothing.
3. *A footnote had been an industry since session 8.* `Note. Detail may not add
   to total due to rounding.` was a 72nd row of the summary exposure table, zero
   exposure, never in an estimate, but present in a published result table. The
   71 real industries are unchanged to 1e-17 after the fix.

**The detail estimate has not been run.** BLS v1 allows only a few requests per
address per day and the coverage probes exhausted today's allowance. The script
refused to estimate on whichever series happened to be cached, because a sample
that changed silently is worse than no result. The cache is now **per series and
per year** rather than per request payload, and existing raw responses were
re-read into it at no cost: of the 472 series the detail run needs for 2017-2019,
176 are already complete, leaving 296 — twelve requests once the allowance resets.

## Session 12: the last data source, and the first honest power result

BLS PPI is back up (it was 503 in session 1). The adapter uses the **NAICS
industry** classification, matching the classification the exposure measure is
already built in, rather than the commodity system which would need a second
undocumented crosswalk (D-040). 29 of 35 series returned, covering 22 of 24 BEA
industries over 48 months. Agriculture has no industry-classification PPI and is
reported unmatched, not substituted.

**Does exposure show up in domestic producer prices?** All three channels carry
the expected positive sign and none is statistically distinguishable from zero:

| Channel | Coefficient | 95% CI | bootstrap p |
|---|---|---|---|
| imported-input cost | +1.230 | [−0.450, +2.909] | 0.110 |
| output protection | +0.374 | [−0.050, +0.797] | 0.084 |
| downstream (Leontief) | +0.164 | [−0.050, +0.379] | 0.112 |

This is a **power result, not a null** (D-041). The input-cost interval spans
roughly −1% to +9% of producer prices at mean exposure — uninformative, and
deliberately not labelled `PRECISE_NULL_EFFECT_BOUNDED`, which is earned by a
tight interval around zero and this is the opposite. Two structural reasons: 22
clusters, and PPI indices covering whole NAICS groups while exposure comes from
10-digit lines.

Entering both channels together halves the input-cost coefficient (+1.23 to
+0.35): the two exposures are correlated across industries, so reporting either
alone attributes the other's variation to it — a concrete reason beyond the
distributional one for never netting them.

With 22 clusters the analytic standard errors over-reject, so every coefficient
carries a **wild cluster bootstrap** p-value with the null imposed and
Rademacher weights at the cluster level (D-042). Here the two broadly agree.

## Session 11: per-year concordance vintages

Session 10 left 2.5% of customs value unmapped because the 2017-2019
concordances are legacy `.xls` and openpyxl reads only `.xlsx`. That was the
same error as D-011 in miniature: one tool failing is not the resource being
unreadable. `xlrd` reads `.xls` and nothing else — exactly the complement — so
both readers are now supported (D-039).

Vintages are combined so the industry assignment is **pre-determined**, for the
same reason the exposure weights are: the 2017 file governs, later vintages
supply only codes created after 2017, and each code records its source vintage.

| | 2020 alone | 2017 primary + fill |
|---|---|---|
| Panel lines reaching a BEA industry | 5,057 | 5,182 |
| Share of customs value mapped | 97.50% | **99.80%** |

172 codes carry a different NAICS in a later vintage than in 2017 — concentrated
between the 2018 and 2019 files (2019 vs 2020 differs for only 2). That count is
reported rather than resolved: it bounds how much the primary-vintage choice
matters, which is the honest answer when two official vintages disagree.

## Session 10: the official concordance existed all along

D-011 concluded the Census HS-to-NAICS concordance was unavailable, after
reference URLs returned 404/403, and fell back to a hand-built HS2-chapter map.
That was wrong in an instructive way: the resource existed the whole time. The
404s came from guessing URL patterns instead of reading the index Census
publishes — and a plain urllib request to that index is itself 403'd, so it needs
a browser user-agent (D-037).

`impconcord20.xlsx` is 19,137 rows keyed on the **10-digit commodity code**, the
exact level this panel is built at, each carrying one NAICS industry. No
weighting assumption at all, where the chapter map had to send a whole HS2
chapter to one BEA commodity. 98.8% of lines reach a BEA summary industry;
97.4% of the panel's customs value is mapped.

**The coarse map was not merely imprecise — it understated exposure
systematically** (D-038):

| Exposure class | chapter map | official |
|---|---|---|
| Both protected and cost-exposed | 9 | **19** |
| Input-cost exposed only | 15 | **29** |
| Little direct exposure | 48 | **24** |

Half the industries the chapter map called barely exposed are exposed, and
chemicals, food and beverage, nonmetallic minerals and other transportation
equipment all went from a reported zero output protection to 0.22-0.25. A coarse
mapping loses coverage rather than adding symmetric noise, and lost coverage
reads as absence of exposure. Anyone who read the earlier exposure figures got a
materially understated picture.

The chapter map is retained behind `--force-chapter-map` so the comparison stays
reproducible.

## Session 9: the selection threat is answered, not just noted

Session 8 left a real threat: only 379 never-treated lines survived the window
extension, and they are what USTR declined to tariff even in the $300bn round.

The answer uses variation already in the panel. Products tariffed *later* are
untreated during an earlier wave's window, and being eventual targets they are
economically much closer to the treated group. A third control definition,
`not_yet_treated`, admits them — but only where the arithmetic permits: a cohort
qualifies only if its treatment starts strictly after the sub-experiment's window
ends. Lists 1-3 end at month indices 24233-24235 and List 4A starts at 24237, so
its 795 lines are clean controls for all three; the List 4A stack has no later
cohort and falls back to never-treated. A test refuses a cohort treated on the
boundary (D-036).

| Controls | landed | customs | quantity | n |
|---|---|---|---|---|
| never-treated | +0.1544 CLEAN | +0.0253 bounded null | −0.3793 | 395,468 |
| not-yet-treated | +0.1513 CLEAN | +0.0259 bounded null | −0.3710 | 535,132 |

Control group roughly triples, sample grows 35%, every verdict identical and
every estimate within 0.008. A comparison group built from products the same
agency *did* tariff gives the same answer, so selection is not driving the
result. All three control definitions now run and are reported side by side.

## Session 8: window extended to 2020-02; results replicate

With List 4A in the schedule the window could finally run past 2019-08. It now
ends 2020-02, and that endpoint is a judgement about COVID rather than tariffs:
U.S. entries lag Chinese shipment by four to six weeks, so February 2020 entries
reflect pre-disruption production while March entries do not (D-033).

**The conclusion replicates across three windows** — full, ending 2019-12, and
the old pre-List-4A window. Every pre-trend verdict identical, every estimate
within 0.004. Incidence accounting on the full window: duty in force 17.65%,
mechanical log(1+tau) 0.1626, observed landed **+0.1544**, customs **+0.0253**.

Two defects the extension exposed:

* **A fixed classification date.** Cohorts were assigned by assessing each line
  on 2018-10-01, which predates List 4A — so every List 4A product landed in the
  control group the moment the window passed 2019-09. Classification is now by
  the actions that *ever* cover a line in the window (D-034).
* **The replication check counted "unvalidatable" as "failed"**, reporting
  MISMATCH for T1 because List 4A's notice states no count for its annex. It now
  separates checkable from deferred, as the data-quality battery already did
  (D-035).

**A selection threat now worth naming.** The never-treated control group falls
from 1,174 lines to 379 — 7% of the sample, and not a random 7%: they are what
USTR declined to tariff even in the $300bn round. Stability across windows is
reassuring but the three share most of that control group.

## Session 7: List 4A parsed; two latent defects surfaced

`parse_all_annexes` now iterates operative anchors rather than assuming one
action per notice. 84 FR 43304 carries two, and a session-1 note claiming List 4
used 10-digit annexes was simply wrong — they are 8-digit, differing from Lists
1-3 only by an ": i)" prefix. Three regex generalisations serve both (D-030).

List 4A is in the schedule: 3,233 lines, **15% from 2019-09-01** (never 10% —
84 FR 45821 set 15% on the existing effective date), 7.5% from 2020-02-14. List
4B is recorded as **suspended, never effective** and deliberately not encoded as
a duty (D-031).

Two defects that only a second overlapping action could expose (D-032):

* **A boundary regression**, caught by re-running Lists 1-3. Scoping partial-line
  notes to whole pages dropped three of List 3's eleven carve-outs and broke its
  exact 5,745 reconciliation — its note runs onto the page carrying the next
  ANNEX header. Scope is now taken by text position; List 3 reconciles again.
* **A real engine bug.** Carve-outs were applied after the conflict check and
  zeroed rates globally, so a statistical number carved out of one action but
  covered by another came back untreated. They are now applied per action,
  before the check.

The panel is unchanged: the window ends 2019-08 and List 4A takes effect
2019-09-01, so products treated only by List 4A are correctly controls for this
window. Extending the window is the next step and needs more Census months.

## Session 6: the incidence conclusion closes

`log_customs_unit_value` was never contaminated. Plotting both unit-value paths
side by side showed their pre-periods are nearly identical (RMS 0.0183 against
0.0169) and differ by a constant +0.010 — the MFN duty. The verdicts diverged
only because the post effects differ 4.7x. A relative-magnitude test punishes a
small true effect; an outcome whose effect is genuinely zero fails it however
clean the design (D-028).

A fourth verdict, `PRECISE_NULL_EFFECT_BOUNDED`, now reports the **bound** on
such an effect. Its first version had a false positive on a synthetic panel with
an injected pre-trend — a real trend deflates the post RMS and disguises itself
as a null — so the branch is gated on the slope being statistically
undetectable. The test suite caught that; the rule was fixed, not the test.

**The incidence account now closes.** Value-weighted duty in force **15.3%**;
mechanical log(1+tau) with zero absorption **0.1424**; observed landed
**+0.1494**, customs **+0.0225** bounded at **0.072**.

The landed figure is *not* independent evidence — it contains the duty by
construction. The behavioural quantity is the customs unit value, which falls
only if the exporter cuts its border price. It did not. **The tariff was passed
through to the U.S. importer close to in full, with no detectable exporter
absorption**, and it is the bound that carries that claim (D-029).

| Outcome (stacked) | mean post | verdict |
|---|---|---|
| log landed unit value | +0.149 | CLEAN |
| log customs unit value | +0.023 | PRECISE_NULL, bound 0.072 |
| log quantity | −0.350 | NOISY_PRE_PERIOD_NO_SLOPE |

## Session 5: exclusions are unbuildable, and now provably so

Milestone 1 (parse product exclusions) is **closed as not achievable from
published statistics**, with the reason quantified rather than asserted.

Across 11 USTR notices: **16 exclusions expressed as a 10-digit subheading, 824
as a product description — 1.9% mappable.** A product description identifies a
subset of a statistical reporting number; trade data is published at that number
and no finer. Every annex is a raster image with no text layer, and OCR is not
used (D-005's rule against unvalidatable transcription into a legal variable).

Instead of an unbuildable adjustment, the gap is **bounded**. Share of treated
customs value where the realised duty falls more than 3pp short of statutory:
**4.4% before** exclusions were first granted (2018-12), **20.1% after**. The
pre-exclusion figure is preference programmes and duty-free entry, not
exclusions, so at most ~15.7pp is attributable to them — an upper bound with the
right timing signature (D-027).

Exclusions also introduce a third kind of date: retroactive to the *action's*
effective date, expiring one year after *publication*.

## Session 4: the pre-trend was mostly my own statistic

Five hypotheses were tested against `log_quantity` and all five failed:
announcement-date event time (made it *worse*, 1.57 — and dilutes the effect
from −0.350 to −0.192 by putting the no-duty window into the post period),
balanced lines only, trimming to flows over $1M/month, and stacked PPML in
levels. Small-flow noise is real (month-to-month SD of log quantity is 2.44
under $10k/month versus 0.69 over $1M/month, and the small flows are 26% of
flows but 0.07% of value) but trimming them did not move the statistic.

Looking at the coefficient path rather than the summary statistic showed why:
the pre-period oscillates around −0.07 with no drift, and the three months
nearest treatment are +0.06, +0.04, −0.03. The post-period falls monotonically
to −0.58. That is a good event study being failed by a bad statistic.

**The statistic compared `max|pre|` against `mean|post|`** — the maximum of a
dozen noisy coefficients against the mean of another dozen. Replaced with
like-for-like RMS, plus a slope test and the implied bias over the post window
in the outcome's own units. The correction leaves `log_quantity` still above the
threshold (0.54 -> 0.27), which is the check that it did not manufacture a pass
(D-026).

| Outcome (stacked) | rms/rms | slope/mo | p | implied bias | verdict |
|---|---|---|---|---|---|
| log landed unit value | 0.11 | +0.0010 | 0.54 | +0.005 | **CLEAN** |
| log quantity | 0.27 | +0.0134 | 0.068 | +0.067 | NOISY_PRE_PERIOD_NO_SLOPE |
| log customs unit value | 0.55 | +0.0024 | 0.142 | +0.012 | **PRETREND_PRESENT** |

Quantity's implied bias is 19% of its effect and of the *opposite* sign, so
correcting it would deepen the estimated contraction rather than explain it
away. The customs unit value's implied bias is half its effect; that is the
outcome now correctly isolated as unusable.

## Session 3: diagnosing the pre-trend

The quantity "pre-trend" turned out not to be a trend. The months nearest
treatment were near zero; distant months oscillated with no drift. Root cause:
**with a single treatment date, event time is calendar time** — event −12 is
literally 2017-09 and event 0 is 2018-09 — so treated-group-specific time
variation cannot be separated from treatment dynamics by any choice of fixed
effects. Country-by-month, chapter-by-month and month-of-year-by-treated-group
were all tried; none worked, one made it worse (D-022).

The fix was a stacked design: one sub-experiment per wave, controls drawn from
never-treated products only, flow-by-stack and month-by-stack effects. Its main
justification is the forbidden comparison under staggered adoption, not calendar
collinearity — a claim I corrected after a test refuted the first version
(D-023).

| Outcome | single-wave | stacked | mean post effect |
|---|---|---|---|
| log landed unit value | IMPRECISE (0.47) | **CLEAN (0.16)** | **+0.149** |
| log customs unit value | IMPRECISE (1.61) | IMPRECISE (1.30) | +0.023 |
| log quantity | PRETREND_PRESENT (1.02) | PRETREND_PRESENT (0.54) | −0.350 |

Reading: the duty-inclusive landed cost of treated Chinese imports runs about
15 log points above the never-treated counterfactual, on a design that passes
its pre-trend test. The tariff-exclusive border price moves ~2 log points and
cannot be distinguished from zero. That is the incidence result, and it now has
one leg standing on a licensed design.

## What changed this session

A Census API key was supplied and verified. The first live pull immediately
forced a design change: **Census reports no quantity at HS6** (`UNIT_QY1 = "-"`,
`CON_QY1_MO = 0`), because the 10-digit lines beneath a heading carry different
units of measure. Without quantity there are no unit values, and without unit
values the central incidence question cannot be answered at all. The panel moved
to HS10 (D-019).

That turned out to be strictly better for a second, independent reason: Section
301 is legislated at HS8 and HS10 nests exactly within it, so the
partial-coverage problem disappears. The 598 HS6 headings previously excluded
are back in, correctly classified, and **0 of 489,733 observations are now
ambiguous** (previously 6, with 598 headings dropped entirely).

The engine also now resolves partial lines **exactly** at 10 digits: U.S. note
20(g) names the carved-out statistical numbers, so an HS10 line either is one of
them or is not. 17 codes moved from treated to control on that basis.

## Verification state

| Check | Result |
|---|---|
| Tests | **92 passed, 0 failed** |
| ruff / mypy | clean |
| Section 301 parse vs notices' own counts | exact: 818 / 279 / 5,745 |
| Data-quality battery | 6 pass, 6 fail — **no blocking (ERROR) failures** |
| Ambiguous tariff assessments | **0 of 489,733** |
| End-to-end reproduce | passes, provenance `OFFICIAL` |

## Panel

489,733 rows · 3,456 HS10 lines (2,303 treated by List 3 only, 1,153
never-treated) across 949 HS6 headings · 9 partners · 2017-01 to 2019-08 ·
773,929 raw rows staged from 320 chapter-month partitions (18 MB).

A companion HS6 panel (186,609 rows) is built by aggregation; 6.1% of its
cells have mixed units across their 10-digit lines and carry null quantities by
construction rather than a meaningless sum.

## First official estimates

Two-way fixed effects (flow + month), clustered on HS6, n = 319,063:

| Outcome | Estimate | 95% CI |
|---|---|---|
| log customs unit value (tariff-exclusive) | −0.036 | [−0.182, +0.111] |
| log landed unit value (duty-inclusive) | **+0.663** | [+0.514, +0.812] |
| log quantity | −1.202 | [−1.492, −0.911] |
| log customs value | −1.389 | [−1.628, −1.151] |

The pattern is near-complete pass-through to the U.S. importer: the
duty-inclusive border cost rises sharply and precisely while the foreign border
price is statistically indistinguishable from unchanged.

**But no outcome clears its pre-trend test**, so all of this is reported as
descriptive:

| Outcome | max abs pre-coef | mean abs post-coef | ratio | verdict |
|---|---|---|---|---|
| log customs unit value | 0.040 | 0.025 | 1.61 | IMPRECISE |
| log landed unit value | 0.042 | 0.088 | 0.47 | IMPRECISE |
| log quantity | 0.338 | 0.330 | 1.02 | **PRETREND_PRESENT** |

## Diversion, counterfactual-adjusted

Against a never-treated-product counterfactual, China's imports of the targeted
products ran **−$1.79bn/month** below counterfactual (−41%). Third countries in
this sample ran **−$512mn/month below** their own counterfactual: only Korea
(+$101mn) and India (+$8mn) gained; Vietnam, Thailand, Taiwan, Malaysia, Mexico
and Canada all fell short. Adjusted replacement ratio **−0.29**.

That is a notable pattern and it needs the caveats attached: a restricted
10-chapter, 8-partner sample; a 10-month post window; a counterfactual doing
heavy lifting (Korea's control products *fell* 11%, which is most of its
apparent gain); and a quantity outcome that fails its pre-trend test.

## Industry exposure

Of 72 BEA summary industries: 9 face **both** output protection and higher
imported-input costs, 14 face input costs only, 49 little direct exposure.
Concordance remains `COARSE_APPROXIMATION`.

## A defect found and fixed

`scripts/generate_reports.py` resolved its results directory to `data/` instead
of `data/results/`, so **every report generated before this session had empty
tables** — including the ones committed in `c53443d`. The prose was real; the
tables were missing. Fixed, and reports regenerated with content.

## Next actions, in priority order

1. **Run the detail-level propagation estimate** once the BLS daily allowance
   resets: `make estimate-propagation-detail`. Twelve requests are needed; the
   per-series cache holds the rest. This is the first time the two exposure
   channels can be separated with enough clusters to mean anything, and the
   answer may well still be "no detectable effect" — which would then be a
   result rather than a power limit.
2. **Re-read the summary-level result against it.** If the detail estimate
   sharpens the intervals, D-041's "power result, not a null" verdict needs
   restating in whichever direction the evidence goes.
3. Structural Armington/CES module (M10, D-017), still deliberately deferred:
   calibrating it would produce counterfactuals with no informational content
   beyond the reduced-form slice.
4. Portfolio polish: dashboard pages for the detail exposure, and a pass over
   the reports now that the industry axis is ten times finer.

## Known gaps carried forward

- Exclusions unparsed → intention-to-treat only.
- List 4A unparsed → window ends 2019-08.
- USITC HTS serves the current vintage, not HTS2018.
- IO concordance official and per-vintage; 99.8% of customs value mapped.
  Exposure magnitudes still do not feed any welfare statement.
- 42.5% of rows have no single ad valorem MFN baseline (compound duty lines);
  nulls propagate rather than being filled.
- 34.8% of rows have no usable quantity, so unit values are undefined there.
- No structural module, deliberately (D-017) → no welfare number exists.
