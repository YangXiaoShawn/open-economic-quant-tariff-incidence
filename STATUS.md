# STATUS

**Last updated:** 2026-08-09 · session 2

## One-line state

The pipeline now runs end to end on **official U.S. Census data**. The panel is
at HS10, every observation carries an unambiguous tariff assessment, and the
first real estimates are in. The binding constraint is no longer data access —
it is that the **quantity outcome fails its pre-trend test**, so the sourcing
results are descriptive rather than causal.

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

1. **Diagnose the quantity pre-trend.** Candidates: front-running ahead of the
   known effective date, the 2018 List 1/2 waves contaminating chapter-mates,
   and composition change as HS10 lines enter and exit. Until this clears, the
   sourcing findings are descriptive.
2. **Parse product exclusions.** `DUTY_VS_ENGINE` flags 12,861 of 102,950
   dutiable observations (12.5%) where the realised duty departs from the
   statutory schedule — a direct, measurable floor on how much
   intention-to-treat differs from treatment-on-the-treated.
3. **List 4A parser**, to extend past 2019-08.
4. Stacked staggered design for Lists 1-3 jointly.
5. Official HS→NAICS concordance.
6. BLS PPI (M9), then the structural module (M10, D-017).

## Known gaps carried forward

- Exclusions unparsed → intention-to-treat only.
- List 4A unparsed → window ends 2019-08.
- USITC HTS serves the current vintage, not HTS2018.
- IO concordance coarse → exposure is an ordering, not a magnitude.
- 42.5% of rows have no single ad valorem MFN baseline (compound duty lines);
  nulls propagate rather than being filled.
- 34.8% of rows have no usable quantity, so unit values are undefined there.
- No structural module, deliberately (D-017) → no welfare number exists.
