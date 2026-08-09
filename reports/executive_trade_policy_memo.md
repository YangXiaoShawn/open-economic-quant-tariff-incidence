# Executive Trade-Policy Memo

> **DATA PROVENANCE: OFFICIAL SOURCES**
>
> All figures below derive from official statistical or legal sources.
>
> run_id `20260809T220507Z-597ee5ff` · git `304fded-dirty` · config `sample_slice.yaml` (sha256 `597ee5ffe47a`) · data period 2017-01 to 2019-08 · generated 2026-08-09T22:05:07.519708+00:00


A short answer to each policy question this project was built to address, with the evidential status of each answer stated rather than implied.

## Questions and answers

**Who appears to bear the tariff?**

See the incidence table: compare the customs unit value response (exporter absorption) with the duty-inclusive landed unit value response (importer cost).

In this run the customs unit value coefficient is +0.0884 [95% CI -0.0354, +0.2123] (interval includes zero, so the sign is not resolved) and the duty-inclusive landed unit value coefficient is +0.7969 [95% CI +0.6725, +0.9212]***.

**How much sourcing moved away from the treated country?**

Treated-country imports of the targeted products changed by -1,940,130,697 in monthly-average customs value (-36.9% of the pre-period level). Against a never-treated-product counterfactual, the largest third-country gains were: 5800 (+304,119,017), 5880 (+65,462,283), 5330 (+25,029,963).

**Which alternative countries gained?**

Treated-country imports of the targeted products changed by -1,940,130,697 in monthly-average customs value (-36.9% of the pre-period level). Against a never-treated-product counterfactual, the largest third-country gains were: 5800 (+304,119,017), 5880 (+65,462,283), 5330 (+25,029,963).

A third-country increase in customs data is consistent with relocated production, with rerouting of treated-origin goods, and with origin misdeclaration. Customs statistics cannot separate these.

**Which U.S. industries received protection?**

0 industries show output protection without material input-cost exposure; 16 face input-cost exposure without protection; **9 face both at once**, including Motor vehicles, bodies and trailers, and parts, Paper products, Wood products, Furniture and related products. Exposure here is a qualitative ordering built on a COARSE_APPROXIMATION concordance, not a magnitude.

**Which U.S. industries faced higher input costs?**

See the imported-input cost exposure table in `supply_chain_propagation.md`. The industries with the largest input-cost exposure are mostly the same manufacturing sectors that also receive protection, which is why the two channels are never netted.

**Which conclusions are causal?**

Outcome by outcome, according to each one's own pre-trend test:

- `log_customs_unit_value`: **PRETREND_PRESENT** under the stacked multi-wave design -> **a causal reading is not supported**; read as descriptive
- `log_landed_unit_value`: **CLEAN** under the stacked multi-wave design -> a causal reading is supported by this test
- `log_quantity`: **NOISY_PRE_PERIOD_NO_SLOPE** under the stacked multi-wave design -> **a qualified causal reading** — no differential trend is detectable, but the pre-period is noisy, so the estimate is less precise than the interval alone suggests. The pre-period slope is not statistically distinguishable from zero; extrapolated across the post window it would shift the estimate by +0.067 against a post-treatment RMS of 0.393.

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

- run id: `20260809T220507Z-597ee5ff`
- git commit: `304fded-dirty`
- configuration: `sample_slice.yaml` (sha256 `597ee5ffe47af577cc12c18a77fbd8ceb65895fed1ca83ff18eb0e2ce7bb7338`)
- data provenance: `OFFICIAL`
- data period: 2017-01 to 2019-08
- generated: 2026-08-09T22:05:07.519708+00:00
- python 3.12.13 on macOS-26.6.1-arm64-arm-64bit

_This document is generated by `scripts/generate_reports.py`. Do not edit it by hand; edit the generator or the underlying result tables._
