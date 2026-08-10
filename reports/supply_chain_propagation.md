# Supply-Chain Propagation

> **DATA PROVENANCE: OFFICIAL SOURCES**
>
> All figures below derive from official statistical or legal sources.
>
> run_id `20260810T140904Z-b1495fb3` · git `43a1a31-dirty` · config `sample_slice.yaml` (sha256 `b1495fb3b363`) · data period 2017-01 to 2020-02 · generated 2026-08-10T14:09:04.004804+00:00


Mapping product-level tariff exposure into U.S. industries using pre-treatment BEA input-output weights. Pre-treatment weights are used so that the exposure measure cannot respond to the shock it is being used to explain.

## Exposure channels, measured separately

Protection on an industry's own output and the cost of its imported inputs pull in opposite directions. They are reported as two numbers. A net figure would hide the distributional question that motivates the analysis, so the `net_contrast_do_not_use_alone` column is present only for contrast and is named accordingly.

**9 industries are exposed through both channels at once.**

**summary by class**

| exposure_class | n_industries | mean_protection | mean_input_cost | mean_downstream |
| --- | --- | --- | --- | --- |
| LITTLE_DIRECT_EXPOSURE | 43 | 0.0000 | 0.0021 | 0.0264 |
| INPUT_COST_EXPOSED_ONLY | 20 | 0.0000 | 0.0112 | 0.0242 |
| BOTH_PROTECTED_AND_COST_EXPOSED | 9 | 0.2085 | 0.0440 | 0.3218 |


## Industries exposed through both channels

**both channels**

| industry_code | industry_name | output_protection_exposure | imported_input_cost_exposure | downstream_total_requirements_exposure |
| --- | --- | --- | --- | --- |
| 3361MV | Motor vehicles, bodies and trailers, and parts | 0.2429 | 0.0873 | 0.3923 |
| 322 | Paper products | 0.2399 | 0.0565 | 0.3561 |
| 333 | Machinery | 0.2014 | 0.0457 | 0.2614 |
| 337 | Furniture and related products | 0.2420 | 0.0452 | 0.2572 |
| 321 | Wood products | 0.1727 | 0.0415 | 0.2758 |
| 331 | Primary metals | 0.1708 | 0.0406 | 0.4427 |
| 332 | Fabricated metal products | 0.2038 | 0.0405 | 0.3674 |
| 326 | Plastics and rubber products | 0.2346 | 0.0249 | 0.3103 |
| 334 | Computer and electronic products | 0.1683 | 0.0138 | 0.2326 |


## Highest imported-input cost exposure

**input cost**

| industry_code | industry_name | imported_input_cost_exposure | output_protection_exposure | exposure_class |
| --- | --- | --- | --- | --- |
| 3361MV | Motor vehicles, bodies and trailers, and parts | 0.0873 | 0.2429 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 322 | Paper products | 0.0565 | 0.2399 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 333 | Machinery | 0.0457 | 0.2014 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 337 | Furniture and related products | 0.0452 | 0.2420 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 321 | Wood products | 0.0415 | 0.1727 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 331 | Primary metals | 0.0406 | 0.1708 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 332 | Fabricated metal products | 0.0405 | 0.2038 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 335 | Electrical equipment, appliances, and components | 0.0297 | 0.0000 | INPUT_COST_EXPOSED_ONLY |
| 323 | Printing and related support activities | 0.0260 | 0.0000 | INPUT_COST_EXPOSED_ONLY |
| 326 | Plastics and rubber products | 0.0249 | 0.2346 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 3364OT | Other transportation equipment | 0.0219 | 0.0000 | INPUT_COST_EXPOSED_ONLY |
| 23 | Construction | 0.0204 | 0.0000 | INPUT_COST_EXPOSED_ONLY |
| 339 | Miscellaneous manufacturing | 0.0152 | 0.0000 | INPUT_COST_EXPOSED_ONLY |
| 334 | Computer and electronic products | 0.0138 | 0.1683 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 311FT | Food and beverage and tobacco products | 0.0126 | 0.0000 | INPUT_COST_EXPOSED_ONLY |


## Highest output protection

**protection**

| industry_code | industry_name | output_protection_exposure | imported_input_cost_exposure | exposure_class |
| --- | --- | --- | --- | --- |
| 3361MV | Motor vehicles, bodies and trailers, and parts | 0.2429 | 0.0873 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 337 | Furniture and related products | 0.2420 | 0.0452 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 322 | Paper products | 0.2399 | 0.0565 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 326 | Plastics and rubber products | 0.2346 | 0.0249 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 332 | Fabricated metal products | 0.2038 | 0.0405 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 333 | Machinery | 0.2014 | 0.0457 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 321 | Wood products | 0.1727 | 0.0415 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 331 | Primary metals | 0.1708 | 0.0406 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 334 | Computer and electronic products | 0.1683 | 0.0138 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 335 | Electrical equipment, appliances, and components | 0.0000 | 0.0297 | INPUT_COST_EXPOSED_ONLY |
| 323 | Printing and related support activities | 0.0000 | 0.0260 | INPUT_COST_EXPOSED_ONLY |
| 3364OT | Other transportation equipment | 0.0000 | 0.0219 | INPUT_COST_EXPOSED_ONLY |
| 23 | Construction | 0.0000 | 0.0204 | INPUT_COST_EXPOSED_ONLY |
| 339 | Miscellaneous manufacturing | 0.0000 | 0.0152 | INPUT_COST_EXPOSED_ONLY |
| 311FT | Food and beverage and tobacco products | 0.0000 | 0.0126 | INPUT_COST_EXPOSED_ONLY |


## Concordance quality and aggregation loss

Concordance status: **COARSE_APPROXIMATION**.

BEA summary commodities are far broader than HS6 lines. A summary commodity that contains both tariffed and untariffed HS6 products receives an import-weighted average rate, so industry-level exposure is attenuated relative to the true product-level shock, and heterogeneity within a commodity is lost entirely.

These exposure numbers are a qualitative ordering of industries. They are not elasticities and must not be used as inputs to a welfare calculation.

**concordance**

| concordance_method | concordance_level | n_mapped_products | n_unmapped_products | aggregation_loss | concordance_source | warnings |
| --- | --- | --- | --- | --- | --- | --- |
| configured HS-to-BEA-commodity map | HS6 -> BEA summary commodity | 1458 | 0 | BEA summary commodities are far broader than HS6 lines. A summary commodity that contains both tariffed and untariffed HS6 products receives an import-weighted average rate, so industry-level exposure is attenuated relative to the true product-level shock, and heterogeneity within a commodity is lost entirely. | config/io_concordance.yaml |  |


---

## Reproducibility

- run id: `20260810T140904Z-b1495fb3`
- git commit: `43a1a31-dirty`
- configuration: `sample_slice.yaml` (sha256 `b1495fb3b363c158ae3b162babd17a515adfc9a8c26038b6c09edb9ec55652a3`)
- data provenance: `OFFICIAL`
- data period: 2017-01 to 2020-02
- generated: 2026-08-10T14:09:04.004804+00:00
- python 3.12.13 on macOS-26.6.1-arm64-arm-64bit

_This document is generated by `scripts/generate_reports.py`. Do not edit it by hand; edit the generator or the underlying result tables._
