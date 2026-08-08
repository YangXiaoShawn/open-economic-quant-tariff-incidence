# Tariff Incidence, Supply-Chain Reallocation, and Domestic Propagation

A reproducible research system measuring how U.S. product-level tariffs affect
import prices, landed costs, quantities, sourcing countries, supplier
concentration, and downstream domestic industries.

**Setting:** the 2018–2019 U.S. Section 301 actions against China. New tariff
episodes are added through configuration, not code.

> ### Read this before reading any number
>
> The U.S. Census international-trade API requires an API key that is **not
> available in this environment**. Trade flows therefore come from a documented
> synthetic generator, and every artefact built from them is tagged
> `MIXED` or `SYNTHETIC_PIPELINE_VALIDATION`.
>
> **No estimate in this repository is currently an empirical finding about U.S.
> trade.** The estimates demonstrate that the estimation code recovers
> parameters that were deliberately injected into simulated data.
>
> What *is* built from official sources and is real: the entire Section 301
> tariff schedule (12,587 records parsed from Federal Register PDFs), MFN
> baseline rates from the USITC HTS, and BEA input-output tables.
>
> Set `CENSUS_API_KEY` ([free, ~2 minutes](https://api.census.gov/data/key_signup.html))
> and re-run — every provenance tag flips to `OFFICIAL` with no code change.

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

### The estimators recover parameters injected into simulated data

| Parameter | Injected | Recovered | Control group |
|---|---|---|---|
| Exporter pass-through | −0.050 | **−0.0485** [−0.102, +0.005] | contaminated |
| Exporter pass-through | −0.050 | **−0.0515** | clean |
| Quantity response (implied slope) | −1.339 | −1.686 | contaminated |
| Quantity response (implied slope) | −1.339 | **−1.256** | clean |

The gap in the quantity row is the finding, not a defect. Third-country
suppliers of a treated product are **not untreated bystanders** — the policy
pushes demand toward them. Using them as controls violates the no-interference
assumption and biases the estimate away from zero. The price parameter, which
has no third-country spillover in the generator, is recovered correctly under
either control group. The pipeline reports both, always.

### Industries are exposed through two channels that are never netted

Using pre-treatment BEA input-output weights, of 72 industries: 8 face **both**
output protection and higher imported-input costs simultaneously — including
primary metals, fabricated metal products, machinery, and motor vehicles. A
single "net exposure" number would hide exactly the distributional question the
analysis exists to answer, so the column that computes it is named
`net_contrast_do_not_use_alone`.

## Design commitments

These are enforced by code and tests, not by good intentions.

**Ambiguity is surfaced, never resolved silently.** The tariff engine returns a
`ValidationStatus` with every answer. Conflicting records return no rate at all.
An HS6 heading whose HS8 children are only partly covered returns
`PARTIAL_HS6_COVERAGE` and a coverage share — 598 such headings were excluded
from both treatment groups rather than assigned an invented rate.

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

**Nulls are never filled silently.** An HS6 heading containing a compound duty
line has no single ad-valorem baseline; those rows carry a null, not a zero. An
earlier version filled them and attenuated 38% of the sample.

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
| **No Census API key** | No empirical finding exists yet. The binding constraint. |
| List 4A unparsed | Window ends 2019-08 to keep the control group clean |
| Product exclusions unparsed | Estimates are intention-to-treat, not treatment-on-the-treated |
| HS→NAICS concordance 404 | Industry exposure is an ordering, not a magnitude |
| USITC HTS serves current vintage | Baseline rates predate/postdate the HTS2018 lists |
| Structural module deferred | No welfare number exists, by design (D-017) |
| BLS PPI in maintenance | No domestic price outcomes yet |

Requires Python 3.12. Runs on Apple Silicon in ~16 GB; no GPU.
