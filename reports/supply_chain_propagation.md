# Supply-Chain Propagation

> **DATA PROVENANCE: OFFICIAL SOURCES**
>
> All figures below derive from official statistical or legal sources.
>
> run_id `20260809T194259Z-597ee5ff` · git `c53443d-dirty` · config `sample_slice.yaml` (sha256 `597ee5ffe47a`) · data period 2017-01 to 2019-08 · generated 2026-08-09T19:42:59.887758+00:00


Mapping product-level tariff exposure into U.S. industries using pre-treatment BEA input-output weights. Pre-treatment weights are used so that the exposure measure cannot respond to the shock it is being used to explain.

## Exposure channels, measured separately

Protection on an industry's own output and the cost of its imported inputs pull in opposite directions. They are reported as two numbers. A net figure would hide the distributional question that motivates the analysis, so the `net_contrast_do_not_use_alone` column is present only for contrast and is named accordingly.

**9 industries are exposed through both channels at once.**

**summary by class**

| exposure_class | n_industries | mean_protection | mean_input_cost | mean_downstream |
| --- | --- | --- | --- | --- |
| LITTLE_DIRECT_EXPOSURE | 49 | 0.0000 | 0.0022 | 0.0214 |
| INPUT_COST_EXPOSED_ONLY | 14 | 0.0000 | 0.0111 | 0.0235 |
| BOTH_PROTECTED_AND_COST_EXPOSED | 9 | 0.1772 | 0.0345 | 0.2733 |


## Industries exposed through both channels

**both channels**

| industry_code | industry_name | output_protection_exposure | imported_input_cost_exposure | downstream_total_requirements_exposure |
| --- | --- | --- | --- | --- |
| 3361MV | Motor vehicles, bodies and trailers, and parts | 0.2383 | 0.0762 | 0.3769 |
| 322 | Paper products | 0.2347 | 0.0536 | 0.3428 |
| 321 | Wood products | 0.1682 | 0.0393 | 0.2662 |
| 337 | Furniture and related products | 0.2354 | 0.0385 | 0.2500 |
| 333 | Machinery | 0.1575 | 0.0327 | 0.2082 |
| 332 | Fabricated metal products | 0.1615 | 0.0224 | 0.2953 |
| 326 | Plastics and rubber products | 0.2066 | 0.0213 | 0.2742 |
| 331 | Primary metals | 0.0524 | 0.0159 | 0.2500 |
| 334 | Computer and electronic products | 0.1406 | 0.0109 | 0.1959 |


## Highest imported-input cost exposure

**input cost**

| industry_code | industry_name | imported_input_cost_exposure | output_protection_exposure | exposure_class |
| --- | --- | --- | --- | --- |
| 3361MV | Motor vehicles, bodies and trailers, and parts | 0.0762 | 0.2383 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 322 | Paper products | 0.0536 | 0.2347 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 321 | Wood products | 0.0393 | 0.1682 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 337 | Furniture and related products | 0.0385 | 0.2354 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 333 | Machinery | 0.0327 | 0.1575 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 323 | Printing and related support activities | 0.0242 | 0.0000 | INPUT_COST_EXPOSED_ONLY |
| 332 | Fabricated metal products | 0.0224 | 0.1615 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 326 | Plastics and rubber products | 0.0213 | 0.2066 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 335 | Electrical equipment, appliances, and components | 0.0188 | 0.0000 | INPUT_COST_EXPOSED_ONLY |
| 23 | Construction | 0.0174 | 0.0000 | INPUT_COST_EXPOSED_ONLY |
| 3364OT | Other transportation equipment | 0.0166 | 0.0000 | INPUT_COST_EXPOSED_ONLY |
| 331 | Primary metals | 0.0159 | 0.0524 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 339 | Miscellaneous manufacturing | 0.0118 | 0.0000 | INPUT_COST_EXPOSED_ONLY |
| 311FT | Food and beverage and tobacco products | 0.0112 | 0.0000 | INPUT_COST_EXPOSED_ONLY |
| 334 | Computer and electronic products | 0.0109 | 0.1406 | BOTH_PROTECTED_AND_COST_EXPOSED |


## Highest output protection

**protection**

| industry_code | industry_name | output_protection_exposure | imported_input_cost_exposure | exposure_class |
| --- | --- | --- | --- | --- |
| 3361MV | Motor vehicles, bodies and trailers, and parts | 0.2383 | 0.0762 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 337 | Furniture and related products | 0.2354 | 0.0385 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 322 | Paper products | 0.2347 | 0.0536 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 326 | Plastics and rubber products | 0.2066 | 0.0213 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 321 | Wood products | 0.1682 | 0.0393 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 332 | Fabricated metal products | 0.1615 | 0.0224 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 333 | Machinery | 0.1575 | 0.0327 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 334 | Computer and electronic products | 0.1406 | 0.0109 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 331 | Primary metals | 0.0524 | 0.0159 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 323 | Printing and related support activities | 0.0000 | 0.0242 | INPUT_COST_EXPOSED_ONLY |
| 335 | Electrical equipment, appliances, and components | 0.0000 | 0.0188 | INPUT_COST_EXPOSED_ONLY |
| 23 | Construction | 0.0000 | 0.0174 | INPUT_COST_EXPOSED_ONLY |
| 3364OT | Other transportation equipment | 0.0000 | 0.0166 | INPUT_COST_EXPOSED_ONLY |
| 339 | Miscellaneous manufacturing | 0.0000 | 0.0118 | INPUT_COST_EXPOSED_ONLY |
| 311FT | Food and beverage and tobacco products | 0.0000 | 0.0112 | INPUT_COST_EXPOSED_ONLY |


## Concordance quality and aggregation loss

Concordance status: **COARSE_APPROXIMATION**.

BEA summary commodities are far broader than HS6 lines. A summary commodity that contains both tariffed and untariffed HS6 products receives an import-weighted average rate, so industry-level exposure is attenuated relative to the true product-level shock, and heterogeneity within a commodity is lost entirely.

These exposure numbers are a qualitative ordering of industries. They are not elasticities and must not be used as inputs to a welfare calculation.

**concordance**

| concordance_method | concordance_level | n_mapped_products | n_unmapped_products | aggregation_loss | concordance_source | warnings |
| --- | --- | --- | --- | --- | --- | --- |
| configured HS-to-BEA-commodity map | HS6 -> BEA summary commodity | 922 | 0 | BEA summary commodities are far broader than HS6 lines. A summary commodity that contains both tariffed and untariffed HS6 products receives an import-weighted average rate, so industry-level exposure is attenuated relative to the true product-level shock, and heterogeneity within a commodity is lost entirely. | config/io_concordance.yaml |  |


---

## Reproducibility

- run id: `20260809T194259Z-597ee5ff`
- git commit: `c53443d-dirty`
- configuration: `sample_slice.yaml` (sha256 `597ee5ffe47af577cc12c18a77fbd8ceb65895fed1ca83ff18eb0e2ce7bb7338`)
- data provenance: `OFFICIAL`
- data period: 2017-01 to 2019-08
- generated: 2026-08-09T19:42:59.887758+00:00
- python 3.12.13 on macOS-26.6.1-arm64-arm-64bit

_This document is generated by `scripts/generate_reports.py`. Do not edit it by hand; edit the generator or the underlying result tables._
