# Supply-Chain Propagation

> **DATA PROVENANCE: OFFICIAL SOURCES**
>
> All figures below derive from official statistical or legal sources.
>
> run_id `20260810T151441Z-b1495fb3` · git `f7862dc-dirty` · config `sample_slice.yaml` (sha256 `b1495fb3b363`) · data period 2017-01 to 2020-02 · generated 2026-08-10T15:14:41.105712+00:00


Mapping product-level tariff exposure into U.S. industries using pre-treatment BEA input-output weights. Pre-treatment weights are used so that the exposure measure cannot respond to the shock it is being used to explain.

## Exposure channels, measured separately

Protection on an industry's own output and the cost of its imported inputs pull in opposite directions. They are reported as two numbers. A net figure would hide the distributional question that motivates the analysis, so the `net_contrast_do_not_use_alone` column is present only for contrast and is named accordingly.

**19 industries are exposed through both channels at once.**

**summary by class**

| exposure_class | n_industries | mean_protection | mean_input_cost | mean_downstream |
| --- | --- | --- | --- | --- |
| INPUT_COST_EXPOSED_ONLY | 29 | 0.0000 | 0.0113 | 0.0570 |
| LITTLE_DIRECT_EXPOSURE | 24 | 0.0000 | 0.0024 | 0.0347 |
| BOTH_PROTECTED_AND_COST_EXPOSED | 19 | 0.1947 | 0.0440 | 0.3159 |


## Industries exposed through both channels

**both channels**

| industry_code | industry_name | output_protection_exposure | imported_input_cost_exposure | downstream_total_requirements_exposure |
| --- | --- | --- | --- | --- |
| 3361MV | Motor vehicles, bodies and trailers, and parts | 0.2306 | 0.0918 | 0.4109 |
| 326 | Plastics and rubber products | 0.2099 | 0.0688 | 0.3380 |
| 322 | Paper products | 0.2242 | 0.0660 | 0.4106 |
| 321 | Wood products | 0.2045 | 0.0567 | 0.3267 |
| 333 | Machinery | 0.2307 | 0.0534 | 0.3238 |
| 337 | Furniture and related products | 0.2372 | 0.0534 | 0.2545 |
| 311FT | Food and beverage and tobacco products | 0.2500 | 0.0501 | 0.3411 |
| 313TT | Textile mills and textile product mills | 0.0752 | 0.0479 | 0.1489 |
| 3364OT | Other transportation equipment | 0.2224 | 0.0452 | 0.2818 |
| 325 | Chemical products | 0.2221 | 0.0451 | 0.6297 |
| 335 | Electrical equipment, appliances, and components | 0.2150 | 0.0432 | 0.2630 |
| 332 | Fabricated metal products | 0.2253 | 0.0429 | 0.4743 |
| 331 | Primary metals | 0.1447 | 0.0396 | 0.5168 |
| 323 | Printing and related support activities | 0.2492 | 0.0369 | 0.2651 |
| 327 | Nonmetallic mineral products | 0.2500 | 0.0314 | 0.3142 |
| 339 | Miscellaneous manufacturing | 0.1604 | 0.0265 | 0.1838 |
| 315AL | Apparel and leather and allied products | 0.1784 | 0.0140 | 0.1800 |
| 334 | Computer and electronic products | 0.1283 | 0.0135 | 0.2390 |
| 113FF | Forestry, fishing, and related activities | 0.0410 | 0.0091 | 0.1007 |


## Highest imported-input cost exposure

**input cost**

| industry_code | industry_name | imported_input_cost_exposure | output_protection_exposure | exposure_class |
| --- | --- | --- | --- | --- |
| 3361MV | Motor vehicles, bodies and trailers, and parts | 0.0918 | 0.2306 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 326 | Plastics and rubber products | 0.0688 | 0.2099 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 322 | Paper products | 0.0660 | 0.2242 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 321 | Wood products | 0.0567 | 0.2045 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 333 | Machinery | 0.0534 | 0.2307 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 337 | Furniture and related products | 0.0534 | 0.2372 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 311FT | Food and beverage and tobacco products | 0.0501 | 0.2500 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 313TT | Textile mills and textile product mills | 0.0479 | 0.0752 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 3364OT | Other transportation equipment | 0.0452 | 0.2224 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 325 | Chemical products | 0.0451 | 0.2221 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 335 | Electrical equipment, appliances, and components | 0.0432 | 0.2150 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 332 | Fabricated metal products | 0.0429 | 0.2253 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 331 | Primary metals | 0.0396 | 0.1447 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 323 | Printing and related support activities | 0.0369 | 0.2492 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 23 | Construction | 0.0345 | 0.0000 | INPUT_COST_EXPOSED_ONLY |


## Highest output protection

**protection**

| industry_code | industry_name | output_protection_exposure | imported_input_cost_exposure | exposure_class |
| --- | --- | --- | --- | --- |
| 311FT | Food and beverage and tobacco products | 0.2500 | 0.0501 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 327 | Nonmetallic mineral products | 0.2500 | 0.0314 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 323 | Printing and related support activities | 0.2492 | 0.0369 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 337 | Furniture and related products | 0.2372 | 0.0534 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 333 | Machinery | 0.2307 | 0.0534 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 3361MV | Motor vehicles, bodies and trailers, and parts | 0.2306 | 0.0918 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 332 | Fabricated metal products | 0.2253 | 0.0429 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 322 | Paper products | 0.2242 | 0.0660 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 3364OT | Other transportation equipment | 0.2224 | 0.0452 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 325 | Chemical products | 0.2221 | 0.0451 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 335 | Electrical equipment, appliances, and components | 0.2150 | 0.0432 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 326 | Plastics and rubber products | 0.2099 | 0.0688 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 321 | Wood products | 0.2045 | 0.0567 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 315AL | Apparel and leather and allied products | 0.1784 | 0.0140 | BOTH_PROTECTED_AND_COST_EXPOSED |
| 339 | Miscellaneous manufacturing | 0.1604 | 0.0265 | BOTH_PROTECTED_AND_COST_EXPOSED |


## Concordance quality and aggregation loss

Concordance status: **CENSUS_IMPORT_CONCORDANCE_2020_HS10_TO_NAICS_TO_BEA**.

Each 10-digit commodity line carries exactly one NAICS industry in the official concordance, so no within-line weighting assumption is made. Aggregation loss remains only where Census itself writes an 'X' in a NAICS code to hide undisclosed detail (198 lines), and where a line's NAICS falls outside the BEA summary manufacturing and primary groups.

These exposure numbers are a qualitative ordering of industries. They are not elasticities and must not be used as inputs to a welfare calculation.

**concordance**

| concordance_method | concordance_level | n_mapped_products | n_unmapped_products | aggregation_loss | concordance_source | warnings |
| --- | --- | --- | --- | --- | --- | --- |
| CENSUS_IMPORT_CONCORDANCE_2020_HS10_TO_NAICS_TO_BEA | HS10 -> NAICS 6-digit -> BEA summary industry | 4707 | 249 | Each 10-digit commodity line carries exactly one NAICS industry in the official concordance, so no within-line weighting assumption is made. Aggregation loss remains only where Census itself writes an 'X' in a NAICS code to hide undisclosed detail (198 lines), and where a line's NAICS falls outside the BEA summary manufacturing and primary groups. | Census impconcord20.xlsx | 249 products have no commodity mapping and are excluded |


---

## Reproducibility

- run id: `20260810T151441Z-b1495fb3`
- git commit: `f7862dc-dirty`
- configuration: `sample_slice.yaml` (sha256 `b1495fb3b363c158ae3b162babd17a515adfc9a8c26038b6c09edb9ec55652a3`)
- data provenance: `OFFICIAL`
- data period: 2017-01 to 2020-02
- generated: 2026-08-10T15:14:41.105712+00:00
- python 3.12.13 on macOS-26.6.1-arm64-arm-64bit

_This document is generated by `scripts/generate_reports.py`. Do not edit it by hand; edit the generator or the underlying result tables._
