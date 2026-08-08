# STATUS

**Last updated:** 2026-08-08 · session 1

## One-line state

The reduced-form vertical slice is complete and runs end to end
(`make reproduce-sample`). The Section 301 tariff schedule is built from
official sources and reconciles exactly. **No empirical finding about U.S. trade
exists yet** — the Census API key is the single blocking constraint.

## What runs

```bash
make reproduce-sample
```

Tariff schedule → panel → validation → descriptives → replication → incidence →
diversion → industry exposure → 8 generated reports. A few minutes on a laptop.

## Verification state

| Check | Result |
|---|---|
| Tests | **83 passed, 0 failed** |
| ruff | clean |
| mypy (core interfaces) | clean, 12 files |
| Section 301 parse vs notices' own counts | **exact: 818 / 279 / 5,745** |
| Data-quality battery | 10 pass, 2 fail (both expected, see below) |
| End-to-end reproduce | passes |

The two quality failures are informative, not defects:
`PANEL_GAPS` (9 of 810 flows have gaps — the synthetic exit hazard firing) and
`TARIFF_AMBIGUOUS` (6 rows with a non-scalar tariff status, correctly surfaced).

## Data sources actually accessed

| Source | Status | What came from it |
|---|---|---|
| Federal Register API + GPO PDFs | ✅ working | 4 notices, 17.7 MB, **12,587 tariff records** |
| USITC HTS `reststop` | ✅ working | 2,951 HS8 lines, 1,585 HS6 headings, 2,944 MFN rates |
| BEA Supply-Use static files | ✅ working | 2017 tables: 72 industries, 81 commodities |
| **U.S. Census trade API** | ❌ **key required** | nothing — synthetic fallback in use |
| BLS PPI | ❌ HTTP 503 maintenance | nothing; M9 deferred |
| Census HS→NAICS concordance | ❌ HTTP 404/403 | nothing; coarse chapter map in use |

## Estimator validation against known parameters

| Parameter | Truth | Contaminated controls | Clean controls |
|---|---|---|---|
| Exporter pass-through | −0.050 | **−0.0485** | **−0.0515** |
| Quantity response (implied slope) | −1.339 | −1.686 | **−1.256** |

The quantity gap is the session's main methodological result: third-country
suppliers of treated products gain from diversion and are therefore not valid
controls. The price parameter is unaffected, as the generator has no
third-country price spillover. Both control groups are now reported on every
run.

## Blocking constraint

**A Census API key.** Free, ~2 minutes:
<https://api.census.gov/data/key_signup.html>

```bash
export CENSUS_API_KEY=your_key_here && make build-trade-panel report
```

Every provenance tag flips `MIXED` → `OFFICIAL` with no code change. This
unblocks milestones M5 (trade-based replication), M9 (domestic prices) and M10
(structural).

## Next actions, in priority order

1. **Census key** — everything else is second-order.
2. **List 4A parser** (10-digit annex construction in 84 FR 43304) — extends the
   window past 2019-08.
3. **Product exclusions** → `EXCLUSION` records; moves estimates from
   intention-to-treat to treatment-on-the-treated.
4. **Stacked staggered design** for Lists 1–3 jointly. The slice currently
   restricts the treated group to List 3 only, precisely to avoid biased
   two-way-FE estimates under staggered adoption.
5. Official HS→NAICS concordance, replacing `COARSE_APPROXIMATION`.
6. BLS PPI adapter (M9), then the structural module (M10, D-017).

## Files in this session

**Created:** 42 files — 20 library modules, 8 pipeline scripts, 4 test modules
(83 tests), 3 config files, 7 docs, 8 generated reports, 4 portfolio documents,
1 dashboard, `Makefile`, `pyproject.toml`.

**Preserved:** `untitled.md` (pre-existing, empty, untouched).

## Known gaps carried forward

Recorded in `docs/DECISION_LOG.md` and in each dataset's manifest
`known_limitations`:

- List 4A unparsed → window ends 2019-08.
- Exclusions unparsed → intention-to-treat only.
- USITC HTS serves the current vintage, not HTS2018.
- IO concordance is `COARSE_APPROXIMATION` → exposure is an ordering, not a
  magnitude.
- 598 HS6 headings excluded from both groups for partial coverage.
- 38% of rows have no single ad-valorem MFN baseline (compound duty lines);
  nulls propagate rather than being filled.
- No structural module, deliberately (D-017) → no welfare number exists.
