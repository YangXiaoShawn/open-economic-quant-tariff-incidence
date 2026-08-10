# Executive Trade-Policy Memo

> **DATA PROVENANCE: OFFICIAL SOURCES**
>
> All figures below derive from official statistical or legal sources.
>
> run_id `20260810T161717Z-b1495fb3` · git `2b81d99-dirty` · config `sample_slice.yaml` (sha256 `b1495fb3b363`) · data period 2017-01 to 2020-02 · generated 2026-08-10T16:17:17.249594+00:00


A short answer to each policy question this project was built to address, with the evidential status of each answer stated rather than implied.

## Questions and answers

**Who appears to bear the tariff?**

See the incidence table: compare the customs unit value response (exporter absorption) with the duty-inclusive landed unit value response (importer cost).

In this run the customs unit value coefficient is +0.0138 [95% CI -0.0903, +0.1178] (interval includes zero, so the sign is not resolved) and the duty-inclusive landed unit value coefficient is +0.7424 [95% CI +0.6382, +0.8465]***.

**How much sourcing moved away from the treated country?**

Treated-country imports of the targeted products changed by -2,073,786,984 in monthly-average customs value (-31.3% of the pre-period level). Against a never-treated-product counterfactual, the largest third-country gains were: 5800 (+653,182,583), 5880 (+195,418,686), 5590 (+41,555,445).

**Which alternative countries gained?**

Treated-country imports of the targeted products changed by -2,073,786,984 in monthly-average customs value (-31.3% of the pre-period level). Against a never-treated-product counterfactual, the largest third-country gains were: 5800 (+653,182,583), 5880 (+195,418,686), 5590 (+41,555,445).

A third-country increase in customs data is consistent with relocated production, with rerouting of treated-origin goods, and with origin misdeclaration. Customs statistics cannot separate these.

**Which U.S. industries received protection?**

0 industries show output protection without material input-cost exposure; 29 face input-cost exposure without protection; **19 face both at once**, including Motor vehicles, bodies and trailers, and parts, Plastics and rubber products, Paper products, Machinery. Exposure here is a qualitative ordering built on a COARSE_APPROXIMATION concordance, not a magnitude.

**Which U.S. industries faced higher input costs?**

See the imported-input cost exposure table in `supply_chain_propagation.md`. The industries with the largest input-cost exposure are mostly the same manufacturing sectors that also receive protection, which is why the two channels are never netted.

**Which conclusions are causal?**

Outcome by outcome, according to each one's own pre-trend test:

- `log_customs_unit_value`: **PRECISE_NULL_EFFECT_BOUNDED** under the stacked multi-wave design -> **the effect is bounded near zero**. The post-treatment path does not rise clear of the pre-period noise, so the design cannot separate the effect from zero — which for a near-null outcome is a finding, not a failure. Taking the observed path and the slope bias together, the effect is at most 0.076 log points in absolute value.
- `log_landed_unit_value`: **CLEAN** under the stacked multi-wave design -> a causal reading is supported by this test
- `log_quantity`: **NOISY_PRE_PERIOD_NO_SLOPE** under the stacked multi-wave design -> **a qualified causal reading** — no differential trend is detectable, but the pre-period is noisy, so the estimate is less precise than the interval alone suggests. The pre-period slope is not statistically distinguishable from zero; extrapolated across the post window it would shift the estimate by +0.033 against a post-treatment RMS of 0.418.

Even where the test is passed, the estimate is intention-to-treat with respect to the statutory list, because product exclusions are not parsed. The data-quality battery puts a floor under how much that matters: realised duty rates depart from the statutory schedule on a material share of dutiable observations.

**Which conclusions are descriptive or model-dependent?**

The sourcing shares, supplier concentration and entry/exit counts are descriptive. The industry exposure measures are constructed from pre-treatment input-output weights and a coarse concordance; they are accounting constructs, not estimates. No structural counterfactual has been run, so no model-implied welfare number exists in this project.

**What evidence would change the recommendation?**

- A specification that clears the pre-trend test for the quantity outcome. As it stands the quantity and diversion results are descriptive, and the headline sourcing numbers rest on them.
- Parsing product exclusions, which would move estimates from intention-to-treat toward treatment-on-the-treated.
- A parsed List 4A, allowing the window to extend past 2019-08 with a clean control group.
- An official HS-to-NAICS concordance, replacing the coarse chapter map and making industry exposure magnitudes usable.
- Domestic output and price data, without which a fall in imports cannot be attributed to domestic substitution rather than lower demand.

---

## Reproducibility

- run id: `20260810T161717Z-b1495fb3`
- git commit: `2b81d99-dirty`
- configuration: `sample_slice.yaml` (sha256 `b1495fb3b363c158ae3b162babd17a515adfc9a8c26038b6c09edb9ec55652a3`)
- data provenance: `OFFICIAL`
- data period: 2017-01 to 2020-02
- generated: 2026-08-10T16:17:17.249594+00:00
- python 3.12.13 on macOS-26.6.1-arm64-arm-64bit

_This document is generated by `scripts/generate_reports.py`. Do not edit it by hand; edit the generator or the underlying result tables._
