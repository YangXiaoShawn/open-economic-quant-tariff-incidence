# Tariff Incidence, Supply-Chain Reallocation, and Domestic Propagation

A reproducible research system measuring how U.S. product-level tariffs affect
import prices, landed costs, quantities, sourcing countries, supplier
concentration, and downstream domestic industries.

**Setting:** the 2018–2019 U.S. Section 301 actions against China. New tariff
episodes are added through configuration, not code.

> ### Read this before reading any number
>
> The pipeline runs on **official U.S. Census data** (provenance `OFFICIAL`).
> 489,733 HS10 x country x month observations, 2017-01 to 2019-08.
>
> Under a **stacked multi-wave design**, `log_landed_unit_value` passes its
> pre-trend test (**CLEAN**) and carries a causal reading. The customs unit value
> is **undetermined** — its effect is near zero and pre-period noise of the same
> size cannot be ruled out. Quantity still **fails** its pre-trend test, so every
> sourcing and diversion finding is descriptive. The reports state this per
> outcome, first, before any number.
>
> Estimates are also **intention-to-treat** with respect to the statutory list,
> because USTR product exclusions are not yet parsed. The data-quality battery
> measures the gap: realised duties depart from the statutory schedule on 12.5%
> of dutiable observations.

---

## Quick start

```bash
make setup
```

```bash
make reproduce-sample
```

That runs the whole pipeline — tariff schedule → panel → validation →
descriptives → replication → incidence → diversion → industry exposure →
reports — in a few minutes on a laptop, and writes to `reports/`.

To use official trade data:

```bash
export CENSUS_API_KEY=your_key_here && make build-trade-panel report
```

## What has actually been verified

### The Section 301 schedule reconciles exactly against the source notices

The parser anchors on the operative legal sentence (*"Heading 9903.88.0X applies
to all products of China that are classified in the following 8-digit
subheadings"*) rather than on page layout, and validates its output against the
line count each notice states in its own preamble:

| Action | Citation | Effective | Rate | Notice states | Parsed | Match |
|---|---|---|---|---|---|---|
| List 1 | 83 FR 28710 | 2018-07-06 | 25% | 818 | 818 | ✅ |
| List 2 | 83 FR 40823 | 2018-08-23 | 25% | 279 | 279 | ✅ |
| List 3 | 83 FR 47974 | 2018-09-24 | 10% | 5,745 | 5,734 full + 11 partial | ✅ |
| List 3 ↑ | 84 FR 20459 | 2019-05-10 | 25% | — | inherited | ✅ |

Reaching an exact match required three things a naive parse misses:

1. **Excluding Chapter 98/99 provisions.** 9802.00.80 and the 9903.88.0X
   headings are legal machinery, not targeted products. List 2 was over by one.
2. **Parsing partial statutory lines.** U.S. note 20(g) covers 11 HS8 lines
   *except* named 10-digit statistical numbers. List 3 was short by 11.
3. **Resolving one truncated code without guessing.** A code renders as
   `9033.00` with its final digits lost in typesetting. It is resolved only
   because the USITC HTS contains exactly one unclaimed 8-digit line under that
   heading, and the record is marked `DERIVED`, not `OFFICIAL_PARSED`.

### Estimates on official data, under a design that survives its own test

The single-wave event study failed for a structural reason: with one effective
date, **event time is calendar time** (event −12 *is* 2017-09), so
treated-group-specific time variation cannot be separated from treatment
dynamics. Country-by-month, chapter-by-month and month-of-year effects were all
tried; none removed it, one made it worse.

The fix is a **stacked design** — one sub-experiment per Section 301 wave,
controls drawn from never-treated products only, so no already-treated unit is
ever used as a control:

| Outcome | Mean post effect | Pre-trend ratio | Verdict |
|---|---|---|---|
| log landed unit value (duty-**inclusive**) | **+0.149** | 0.16 | **CLEAN** |
| log customs unit value (tariff-**exclusive**) | +0.023 | 1.30 | IMPRECISE |
| log quantity | −0.350 | 0.54 | PRETREND_PRESENT |

The duty-inclusive landed cost of treated Chinese imports runs ~15 log points
above the never-treated counterfactual, on a design that clears its pre-trend
test. The foreign border price moves ~2 log points and cannot be distinguished
from zero — the tariff is not being absorbed by the exporter in these data.

Reading incidence requires both numbers; one alone cannot separate exporter
absorption from importer cost.

### Sourcing did not visibly relocate in this sample

Against a never-treated-product counterfactual, China ran **−$1.79bn/month**
below counterfactual on the targeted products (−41%). Third countries ran
**−$512mn/month below** their own counterfactual — only Korea and India gained.
Adjusted replacement ratio **−0.29**.

This cuts against the usual relocation narrative and should be read with its
caveats: 10 chapters, 8 partners, a 10-month post window, and a counterfactual
doing heavy lifting (most of Korea's apparent gain is its *control* products
falling 11%).

### Estimator validation against a known data-generating process

Still run, via `--force-synthetic`, because knowing the right answer is the only
way to test an estimator. It surfaced a design problem: third-country suppliers
of a treated product are **not untreated bystanders**, so using them as controls
violates no-interference and biased the quantity elasticity by 26% while leaving
the price elasticity untouched. Both control groups are now reported on every
run.

### Industries are exposed through two channels that are never netted

Using pre-treatment BEA input-output weights, of 72 industries: 9 face **both**
output protection and higher imported-input costs simultaneously — including
primary metals, fabricated metal products, machinery, and motor vehicles. A
single "net exposure" number would hide exactly the distributional question the
analysis exists to answer, so the column that computes it is named
`net_contrast_do_not_use_alone`.

## Design commitments

These are enforced by code and tests, not by good intentions.

**Ambiguity is surfaced, never resolved silently.** The tariff engine returns a
`ValidationStatus` with every answer. Conflicting records return no rate at all.
Working at HS10 removes the ambiguity rather than papering over it: **0 of
489,733 observations** carry an unusable status, because HS10 nests exactly
inside the HS8 line the statute names, and the 11 partial lines are resolved
against the specific 10-digit numbers U.S. note 20(g) carves out.

**Value concepts stay distinct.** `customs_unit_value` (tariff-exclusive) and
`landed_unit_value_duty_inclusive` answer different questions; incidence cannot
be read without both. Neither is ever called a price — a unit value is
value-over-quantity across a heterogeneous bundle.

**Announcement ≠ effective.** Both are carried through the pipeline. The List 3
increase to 25% was announced for 2019-01-01, postponed twice, and took effect
2019-05-10; conflating the dates would misplace the shock by seven months.

**Mid-month effective dates are day-weighted.** List 3 took effect on 24
September — 7 of 30 days. Month-start assessment says untreated, month-end says
fully treated, and both errors land on the event-time-zero coefficient.

**Nulls are never filled silently.** A line whose column-1 general rate is
compound or specific has no single ad-valorem baseline; those rows (42.5% of the
panel) carry a null, not a zero. An earlier version filled them and attenuated
every total-rate estimate. Census's own "no quantity collected" convention
(`UNIT_QY1 = "-"`, quantity 0) is likewise read as null, not as zero — treating
it as zero would make those unit values infinite.

**Reports cannot make claims the data cannot support.** `guard_language` raises
on causal assertions under non-official provenance and on quantified welfare
claims under any provenance, and it runs on every generated report. It caught
two of this project's own sentences during development; both were rephrased.

**Contradicting evidence is reported.** `reports/failed_hypotheses.md` is
generated from the pipeline, not curated.

## Repository layout

```
src/tariff_incidence/
  adapters/      Federal Register, USITC HTS, Census, BEA; fetch and parse split
  tariff/        records, point-in-time policy engine, schedule builder
  concordance/   versioned HS mappings (stable-code + weighted samples)
  panel/         analytical panel; synthetic generator
  quality/       12-check data-quality battery
  econ/          HDFE absorption, OLS, PPML, designs, diversion
  io_exposure/   BEA-based industry exposure
  reporting/     rendering + the claim guard
config/          episodes, samples, concordances
data/            raw → staged → normalized → analytical → results
reports/         GENERATED — never edit by hand
```

## Documentation

| Document | What it covers |
|---|---|
| [AGENTS.md](AGENTS.md) | Rules for anyone working in the repo |
| [docs/RESEARCH_DESIGN.md](docs/RESEARCH_DESIGN.md) | Identification, estimands, what would falsify them |
| [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md) | Milestones, acceptance tests, risk register |
| [docs/DECISION_LOG.md](docs/DECISION_LOG.md) | Every non-obvious choice and what it costs |
| [data/DATA_ACCESS.md](data/DATA_ACCESS.md) | Source-by-source access status |
| [data/DATA_DICTIONARY.md](data/DATA_DICTIONARY.md) | Every column, precisely defined |
| [STATUS.md](STATUS.md) | Current state |

## Commands

```bash
make help
```

`setup` · `download-sample` · `build-tariff-schedule` · `build-trade-panel` ·
`validate-data` · `descriptive` · `replicate` · `estimate-incidence` ·
`estimate-diversion` · `build-io-exposure` · `structural` · `test` · `lint` ·
`typecheck` · `reproduce-sample` · `report` · `dashboard`

## Known gaps

| Gap | Consequence |
|---|---|
| **Quantity fails its pre-trend test** | Sourcing and diversion results are descriptive, not causal. The binding constraint now. |
| List 4A unparsed | Window ends 2019-08 to keep the control group clean |
| Product exclusions unparsed | Estimates are intention-to-treat, not treatment-on-the-treated |
| HS→NAICS concordance 404 | Industry exposure is an ordering, not a magnitude |
| USITC HTS serves current vintage | Baseline rates predate/postdate the HTS2018 lists |
| Structural module deferred | No welfare number exists, by design (D-017) |
| BLS PPI in maintenance | No domestic price outcomes yet |

Requires Python 3.12. Runs on Apple Silicon in ~16 GB; no GPU.
