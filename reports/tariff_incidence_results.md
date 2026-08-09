# Tariff Incidence — Results

> **DATA PROVENANCE: OFFICIAL SOURCES**
>
> All figures below derive from official statistical or legal sources.
>
> run_id `20260809T194259Z-597ee5ff` · git `c53443d-dirty` · config `sample_slice.yaml` (sha256 `597ee5ffe47a`) · data period 2017-01 to 2019-08 · generated 2026-08-09T19:42:59.887758+00:00


Estimates of how the additional duty maps into customs unit values, duty-inclusive landed unit values, quantities and trade values. The customs unit value is tariff-exclusive and is a proxy for the foreign border price; it is a value-over-quantity ratio across a heterogeneous bundle of transactions and is **not** a transaction price. The duty-inclusive landed unit value is what the U.S. importer faces at the border, excluding freight. Reading incidence requires both.

## Which of these outcomes survives its own pre-trend test

The parallel-trends assumption is tested per outcome, and it does not hold uniformly. The verdict below governs how each result may be read; it is placed first so it cannot be skipped.

- `log_customs_unit_value`: pre-trend verdict **IMPRECISE_CANNOT_RULE_OUT_A_MEANINGFUL_PRETREND** -> **a causal reading is not supported**; read as descriptive
- `log_landed_unit_value`: pre-trend verdict **IMPRECISE_CANNOT_RULE_OUT_A_MEANINGFUL_PRETREND** -> **a causal reading is not supported**; read as descriptive
- `log_quantity`: pre-trend verdict **PRETREND_PRESENT** -> **a causal reading is not supported**; read as descriptive

## Rung 2 — two-way fixed-effects regressions

- **log customs unit value (TARIFF-EXCLUSIVE; foreign border price proxy, not a transaction price)** — `additional_tariff_rate` -0.0355 [95% CI -0.1822, +0.1112] (interval includes zero, so the sign is not resolved), n = 319,063, FE: flow_id|month_key, clustered on hs6
- **log landed unit value (DUTY-INCLUSIVE, excludes freight; U.S. importer border cost)** — `additional_tariff_rate` +0.6629 [95% CI +0.5138, +0.8120]***, n = 319,063, FE: flow_id|month_key, clustered on hs6
- **log import quantity (primary quantity unit)** — `additional_tariff_rate` -1.2017 [95% CI -1.4925, -0.9109]***, n = 319,063, FE: flow_id|month_key, clustered on hs6
- **log customs value** — `additional_tariff_rate` -1.3893 [95% CI -1.6276, -1.1509]***, n = 378,789, FE: flow_id|month_key, clustered on hs6

**estimates**

| outcome | term | estimate | std_error | ci_low | ci_high | p_value | n_obs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| log_customs_unit_value | additional_tariff_rate | -0.0355 | 0.0748 | -0.1822 | 0.1112 | 0.6348 | 319063 |
| log_landed_unit_value | additional_tariff_rate | 0.6629 | 0.0760 | 0.5138 | 0.8120 | 0.0000 | 319063 |
| log_quantity | additional_tariff_rate | -1.2017 | 0.1482 | -1.4925 | -0.9109 | 0.0000 | 319063 |
| log_customs_value | additional_tariff_rate | -1.3893 | 0.1215 | -1.6276 | -1.1509 | 0.0000 | 378789 |


## Rung 5 — PPML on trade flows in levels

- **customs_value (levels, PPML; full sample)** — `log1p_additional_tariff` -2.0837 [95% CI -3.3214, -0.8461]***, n = 489,733, FE: flow_id|month_key, clustered on hs6
- **quantity (levels, PPML; full sample)** — `log1p_additional_tariff` -2.2137 [95% CI -5.7029, +1.2756] (interval includes zero, so the sign is not resolved), n = 488,248, FE: flow_id|month_key, clustered on hs6
- **customs_value (levels, PPML; subsample with an ad valorem MFN baseline)** — `log1p_total_tariff` -2.6884 [95% CI -4.0402, -1.3366]***, n = 281,658, FE: flow_id|month_key, clustered on hs6
- **quantity (levels, PPML; subsample with an ad valorem MFN baseline)** — `log1p_total_tariff` -2.4262 [95% CI -5.9874, +1.1350] (interval includes zero, so the sign is not resolved), n = 281,154, FE: flow_id|month_key, clustered on hs6

**estimates**

| outcome | term | estimate | std_error | ci_low | ci_high | p_value | n_obs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| customs_value | log1p_additional_tariff | -2.0837 | 0.6307 | -3.3214 | -0.8461 | 0.0010 | 489733 |
| quantity | log1p_additional_tariff | -2.2137 | 1.7780 | -5.7029 | 1.2756 | 0.2134 | 488248 |
| customs_value | log1p_total_tariff | -2.6884 | 0.6888 | -4.0402 | -1.3366 | 0.0001 | 281658 |
| quantity | log1p_total_tariff | -2.4262 | 1.8145 | -5.9874 | 1.1350 | 0.1815 | 281154 |


## Rung 6 — heterogeneity

- **log quantity -- high_pretreatment_dependence (split at median 0.484)** — `additional_tariff_rate` -1.8122 [95% CI -2.1719, -1.4524]***, n = 150,166, FE: flow_id|month_key, clustered on hs6
- **log quantity -- low_pretreatment_dependence (split at median 0.484)** — `additional_tariff_rate` -0.5778 [95% CI -1.0049, -0.1507]***, n = 165,936, FE: flow_id|month_key, clustered on hs6

**estimates**

| outcome | term | estimate | std_error | ci_low | ci_high | p_value | n_obs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| log_quantity | additional_tariff_rate | -1.8122 | 0.1831 | -2.1719 | -1.4524 | 0.0000 | 150166 |
| log_quantity | additional_tariff_rate | -0.5778 | 0.2175 | -1.0049 | -0.1507 | 0.0081 | 165936 |


## Event study — log_customs_unit_value (reference period −1)

Coefficients are relative to event month −1. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.0047 | 0.0272 | -0.0581 | 0.0486 | 0.8618 | yes |
| -11 | -0.0112 | 0.0284 | -0.0669 | 0.0444 | 0.6919 | yes |
| -10 | -0.0047 | 0.0259 | -0.0556 | 0.0461 | 0.8554 | yes |
| -9 | -0.0158 | 0.0289 | -0.0726 | 0.0410 | 0.5856 | yes |
| -8 | -0.0093 | 0.0266 | -0.0614 | 0.0429 | 0.7268 | yes |
| -7 | -0.0359 | 0.0278 | -0.0905 | 0.0187 | 0.1967 | yes |
| -6 | 0.0066 | 0.0267 | -0.0458 | 0.0589 | 0.8059 | yes |
| -5 | 0.0358 | 0.0262 | -0.0156 | 0.0872 | 0.1716 | yes |
| -4 | -0.0104 | 0.0256 | -0.0605 | 0.0398 | 0.6855 | yes |
| -3 | 0.0044 | 0.0249 | -0.0444 | 0.0532 | 0.8607 | yes |
| -2 | -0.0097 | 0.0234 | -0.0556 | 0.0362 | 0.6771 | yes |
| -1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| 0 | -0.0083 | 0.0254 | -0.0581 | 0.0416 | 0.7447 | no |
| 1 | 0.0105 | 0.0245 | -0.0376 | 0.0587 | 0.6678 | no |
| 2 | -0.0455 | 0.0259 | -0.0963 | 0.0054 | 0.0795 | no |
| 3 | -0.0570 | 0.0281 | -0.1121 | -0.0018 | 0.0430 | no |
| 4 | -0.0049 | 0.0305 | -0.0649 | 0.0550 | 0.8714 | no |
| 5 | 0.0107 | 0.0298 | -0.0478 | 0.0692 | 0.7195 | no |
| 6 | 0.0324 | 0.0297 | -0.0259 | 0.0907 | 0.2757 | no |
| 7 | 0.0304 | 0.0276 | -0.0238 | 0.0846 | 0.2708 | no |
| 8 | -0.0049 | 0.0309 | -0.0655 | 0.0557 | 0.8736 | no |
| 9 | -0.0374 | 0.0306 | -0.0974 | 0.0226 | 0.2212 | no |
| 10 | -0.0195 | 0.0289 | -0.0762 | 0.0372 | 0.5008 | no |
|  | -0.0174 | 0.0225 | -0.0615 | 0.0267 | 0.4397 | no |
|  | -0.0178 | 0.0295 | -0.0757 | 0.0401 | 0.5466 | no |


## Event study — log_customs_unit_value (reference period −3)

Coefficients are relative to event month −3. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.0091 | 0.0282 | -0.0645 | 0.0463 | 0.7475 | yes |
| -11 | -0.0156 | 0.0276 | -0.0697 | 0.0385 | 0.5717 | yes |
| -10 | -0.0091 | 0.0276 | -0.0633 | 0.0452 | 0.7425 | yes |
| -9 | -0.0201 | 0.0285 | -0.0761 | 0.0358 | 0.4799 | yes |
| -8 | -0.0137 | 0.0258 | -0.0642 | 0.0369 | 0.5964 | yes |
| -7 | -0.0403 | 0.0283 | -0.0958 | 0.0152 | 0.1544 | yes |
| -6 | 0.0022 | 0.0260 | -0.0488 | 0.0532 | 0.9328 | yes |
| -5 | 0.0315 | 0.0261 | -0.0198 | 0.0827 | 0.2289 | yes |
| -4 | -0.0147 | 0.0246 | -0.0631 | 0.0337 | 0.5506 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | -0.0141 | 0.0261 | -0.0653 | 0.0370 | 0.5885 | yes |
| -1 | -0.0044 | 0.0249 | -0.0532 | 0.0444 | 0.8607 | yes |
| 0 | -0.0126 | 0.0266 | -0.0649 | 0.0397 | 0.6355 | no |
| 1 | 0.0062 | 0.0264 | -0.0456 | 0.0579 | 0.8151 | no |
| 2 | -0.0498 | 0.0291 | -0.1070 | 0.0074 | 0.0877 | no |
| 3 | -0.0613 | 0.0290 | -0.1182 | -0.0045 | 0.0345 | no |
| 4 | -0.0093 | 0.0302 | -0.0685 | 0.0499 | 0.7577 | no |
| 5 | 0.0063 | 0.0314 | -0.0552 | 0.0679 | 0.8398 | no |
| 6 | 0.0280 | 0.0302 | -0.0313 | 0.0874 | 0.3540 | no |
| 7 | 0.0261 | 0.0304 | -0.0337 | 0.0858 | 0.3920 | no |
| 8 | -0.0093 | 0.0296 | -0.0674 | 0.0488 | 0.7541 | no |
| 9 | -0.0418 | 0.0305 | -0.1017 | 0.0181 | 0.1715 | no |
| 10 | -0.0238 | 0.0298 | -0.0823 | 0.0347 | 0.4245 | no |
|  | -0.0217 | 0.0222 | -0.0652 | 0.0217 | 0.3268 | no |
|  | -0.0221 | 0.0302 | -0.0815 | 0.0372 | 0.4638 | no |


## Event study — log_landed_unit_value (reference period −1)

Coefficients are relative to event month −1. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | 0.0075 | 0.0275 | -0.0465 | 0.0614 | 0.7861 | yes |
| -11 | 0.0006 | 0.0287 | -0.0556 | 0.0569 | 0.9822 | yes |
| -10 | 0.0073 | 0.0262 | -0.0441 | 0.0587 | 0.7806 | yes |
| -9 | -0.0038 | 0.0293 | -0.0613 | 0.0537 | 0.8973 | yes |
| -8 | 0.0027 | 0.0268 | -0.0499 | 0.0553 | 0.9193 | yes |
| -7 | -0.0240 | 0.0281 | -0.0791 | 0.0310 | 0.3916 | yes |
| -6 | 0.0180 | 0.0269 | -0.0347 | 0.0708 | 0.5023 | yes |
| -5 | 0.0453 | 0.0263 | -0.0062 | 0.0968 | 0.0848 | yes |
| -4 | -0.0044 | 0.0256 | -0.0545 | 0.0458 | 0.8645 | yes |
| -3 | 0.0037 | 0.0249 | -0.0451 | 0.0525 | 0.8821 | yes |
| -2 | -0.0098 | 0.0234 | -0.0557 | 0.0361 | 0.6761 | yes |
| -1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| 0 | -0.0004 | 0.0254 | -0.0502 | 0.0494 | 0.9873 | no |
| 1 | 0.0932 | 0.0247 | 0.0448 | 0.1416 | 0.0002 | no |
| 2 | 0.0411 | 0.0259 | -0.0097 | 0.0920 | 0.1126 | no |
| 3 | 0.0298 | 0.0282 | -0.0255 | 0.0851 | 0.2904 | no |
| 4 | 0.0810 | 0.0307 | 0.0207 | 0.1413 | 0.0085 | no |
| 5 | 0.0965 | 0.0299 | 0.0379 | 0.1552 | 0.0013 | no |
| 6 | 0.1188 | 0.0298 | 0.0603 | 0.1772 | 0.0001 | no |
| 7 | 0.1160 | 0.0276 | 0.0618 | 0.1702 | 0.0000 | no |
| 8 | 0.0965 | 0.0310 | 0.0356 | 0.1574 | 0.0019 | no |
| 9 | 0.1435 | 0.0308 | 0.0831 | 0.2038 | 0.0000 | no |
| 10 | 0.1802 | 0.0289 | 0.1235 | 0.2369 | 0.0000 | no |
|  | -0.0057 | 0.0229 | -0.0507 | 0.0392 | 0.8026 | no |
|  | 0.1825 | 0.0296 | 0.1243 | 0.2406 | 0.0000 | no |


## Event study — log_landed_unit_value (reference period −3)

Coefficients are relative to event month −3. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | 0.0038 | 0.0285 | -0.0522 | 0.0598 | 0.8947 | yes |
| -11 | -0.0030 | 0.0279 | -0.0577 | 0.0516 | 0.9129 | yes |
| -10 | 0.0036 | 0.0279 | -0.0511 | 0.0583 | 0.8971 | yes |
| -9 | -0.0075 | 0.0288 | -0.0641 | 0.0491 | 0.7956 | yes |
| -8 | -0.0010 | 0.0260 | -0.0520 | 0.0500 | 0.9702 | yes |
| -7 | -0.0277 | 0.0285 | -0.0836 | 0.0282 | 0.3305 | yes |
| -6 | 0.0143 | 0.0262 | -0.0370 | 0.0657 | 0.5840 | yes |
| -5 | 0.0416 | 0.0262 | -0.0098 | 0.0930 | 0.1125 | yes |
| -4 | -0.0081 | 0.0247 | -0.0564 | 0.0403 | 0.7440 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | -0.0135 | 0.0261 | -0.0646 | 0.0377 | 0.6055 | yes |
| -1 | -0.0037 | 0.0249 | -0.0525 | 0.0451 | 0.8821 | yes |
| 0 | -0.0041 | 0.0266 | -0.0563 | 0.0481 | 0.8777 | no |
| 1 | 0.0895 | 0.0265 | 0.0376 | 0.1415 | 0.0008 | no |
| 2 | 0.0375 | 0.0292 | -0.0198 | 0.0947 | 0.1997 | no |
| 3 | 0.0261 | 0.0290 | -0.0308 | 0.0830 | 0.3684 | no |
| 4 | 0.0773 | 0.0303 | 0.0179 | 0.1368 | 0.0109 | no |
| 5 | 0.0928 | 0.0314 | 0.0312 | 0.1545 | 0.0032 | no |
| 6 | 0.1151 | 0.0303 | 0.0556 | 0.1745 | 0.0002 | no |
| 7 | 0.1123 | 0.0304 | 0.0526 | 0.1720 | 0.0002 | no |
| 8 | 0.0928 | 0.0297 | 0.0345 | 0.1512 | 0.0018 | no |
| 9 | 0.1398 | 0.0307 | 0.0794 | 0.2001 | 0.0000 | no |
| 10 | 0.1765 | 0.0297 | 0.1182 | 0.2349 | 0.0000 | no |
|  | -0.0094 | 0.0226 | -0.0537 | 0.0349 | 0.6767 | no |
|  | 0.1788 | 0.0303 | 0.1194 | 0.2382 | 0.0000 | no |


## Event study — log_quantity (reference period −1)

Coefficients are relative to event month −1. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.1634 | 0.0442 | -0.2502 | -0.0766 | 0.0002 | yes |
| -11 | -0.1667 | 0.0424 | -0.2499 | -0.0835 | 0.0001 | yes |
| -10 | -0.2351 | 0.0405 | -0.3146 | -0.1557 | 0.0000 | yes |
| -9 | -0.0392 | 0.0452 | -0.1279 | 0.0495 | 0.3860 | yes |
| -8 | -0.0228 | 0.0400 | -0.1013 | 0.0558 | 0.5694 | yes |
| -7 | -0.0528 | 0.0431 | -0.1374 | 0.0319 | 0.2214 | yes |
| -6 | -0.2351 | 0.0437 | -0.3208 | -0.1494 | 0.0000 | yes |
| -5 | -0.3223 | 0.0440 | -0.4087 | -0.2358 | 0.0000 | yes |
| -4 | -0.0759 | 0.0397 | -0.1537 | 0.0020 | 0.0561 | yes |
| -3 | 0.0155 | 0.0365 | -0.0561 | 0.0871 | 0.6709 | yes |
| -2 | -0.0095 | 0.0365 | -0.0812 | 0.0621 | 0.7939 | yes |
| -1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| 0 | -0.0145 | 0.0376 | -0.0882 | 0.0593 | 0.7005 | no |
| 1 | -0.1550 | 0.0383 | -0.2302 | -0.0798 | 0.0001 | no |
| 2 | -0.1493 | 0.0408 | -0.2295 | -0.0692 | 0.0003 | no |
| 3 | 0.2108 | 0.0460 | 0.1204 | 0.3011 | 0.0000 | no |
| 4 | -0.2777 | 0.0507 | -0.3772 | -0.1783 | 0.0000 | no |
| 5 | -0.3764 | 0.0471 | -0.4688 | -0.2840 | 0.0000 | no |
| 6 | -0.6261 | 0.0466 | -0.7176 | -0.5346 | 0.0000 | no |
| 7 | -0.5262 | 0.0470 | -0.6184 | -0.4339 | 0.0000 | no |
| 8 | -0.3214 | 0.0471 | -0.4138 | -0.2290 | 0.0000 | no |
| 9 | -0.3880 | 0.0459 | -0.4781 | -0.2979 | 0.0000 | no |
| 10 | -0.4456 | 0.0470 | -0.5379 | -0.3534 | 0.0000 | no |
|  | -0.1597 | 0.0397 | -0.2376 | -0.0817 | 0.0001 | no |
|  | -0.4688 | 0.0482 | -0.5633 | -0.3742 | 0.0000 | no |


## Event study — log_quantity (reference period −3)

Coefficients are relative to event month −3. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.1789 | 0.0459 | -0.2690 | -0.0889 | 0.0001 | yes |
| -11 | -0.1822 | 0.0434 | -0.2674 | -0.0971 | 0.0000 | yes |
| -10 | -0.2506 | 0.0419 | -0.3329 | -0.1684 | 0.0000 | yes |
| -9 | -0.0547 | 0.0444 | -0.1418 | 0.0324 | 0.2181 | yes |
| -8 | -0.0383 | 0.0402 | -0.1171 | 0.0406 | 0.3408 | yes |
| -7 | -0.0683 | 0.0425 | -0.1516 | 0.0151 | 0.1082 | yes |
| -6 | -0.2506 | 0.0401 | -0.3293 | -0.1720 | 0.0000 | yes |
| -5 | -0.3378 | 0.0418 | -0.4198 | -0.2558 | 0.0000 | yes |
| -4 | -0.0914 | 0.0358 | -0.1616 | -0.0211 | 0.0109 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | -0.0250 | 0.0371 | -0.0979 | 0.0478 | 0.4997 | yes |
| -1 | -0.0155 | 0.0365 | -0.0871 | 0.0561 | 0.6709 | yes |
| 0 | -0.0300 | 0.0410 | -0.1104 | 0.0504 | 0.4645 | no |
| 1 | -0.1705 | 0.0413 | -0.2515 | -0.0896 | 0.0000 | no |
| 2 | -0.1648 | 0.0466 | -0.2563 | -0.0734 | 0.0004 | no |
| 3 | 0.1953 | 0.0471 | 0.1029 | 0.2876 | 0.0000 | no |
| 4 | -0.2932 | 0.0514 | -0.3941 | -0.1923 | 0.0000 | no |
| 5 | -0.3919 | 0.0509 | -0.4918 | -0.2920 | 0.0000 | no |
| 6 | -0.6416 | 0.0476 | -0.7351 | -0.5481 | 0.0000 | no |
| 7 | -0.5417 | 0.0501 | -0.6401 | -0.4433 | 0.0000 | no |
| 8 | -0.3369 | 0.0467 | -0.4286 | -0.2453 | 0.0000 | no |
| 9 | -0.4035 | 0.0490 | -0.4997 | -0.3073 | 0.0000 | no |
| 10 | -0.4611 | 0.0488 | -0.5568 | -0.3654 | 0.0000 | no |
|  | -0.1752 | 0.0395 | -0.2527 | -0.0976 | 0.0000 | no |
|  | -0.4843 | 0.0509 | -0.5841 | -0.3844 | 0.0000 | no |


## Pre-treatment trend tests

Two criteria are reported. Statistical detectability alone is a poor guide in a large panel, where standard errors shrink until economically trivial pre-period movement becomes significant; the verdict field combines significance with magnitude relative to the post-treatment coefficients.

**pre-trend tests**

| test | n_pre_coefs | approx_chi2 | approx_p_value | max_abs_pre_coef | mean_abs_post_coef | max_pre_relative_to_mean_post | relative_threshold | any_pre_significant_5pct | economically_small | verdict | reference_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pretrend_log_customs_unit_value_ref3 | 11 | 5.4809 | 0.9057 | 0.0403 | 0.0250 | 1.6147 | 0.2000 | no | no | IMPRECISE_CANNOT_RULE_OUT_A_MEANINGFUL_PRETREND | -3 |
| pretrend_log_customs_unit_value_ref1 | 11 | 4.6102 | 0.9486 | 0.0359 | 0.0238 | 1.5120 | 0.2000 | no | no | IMPRECISE_CANNOT_RULE_OUT_A_MEANINGFUL_PRETREND | -1 |
| pretrend_log_landed_unit_value_ref3 | 11 | 4.2829 | 0.9609 | 0.0416 | 0.0876 | 0.4750 | 0.2000 | no | no | IMPRECISE_CANNOT_RULE_OUT_A_MEANINGFUL_PRETREND | -3 |
| pretrend_log_landed_unit_value_ref1 | 11 | 4.5660 | 0.9504 | 0.0453 | 0.0906 | 0.4998 | 0.2000 | no | no | IMPRECISE_CANNOT_RULE_OUT_A_MEANINGFUL_PRETREND | -1 |
| pretrend_log_quantity_ref3 | 11 | 185.2585 | 0.0000 | 0.3378 | 0.3301 | 1.0235 | 0.2000 | yes | no | PRETREND_PRESENT | -3 |
| pretrend_log_quantity_ref1 | 11 | 151.8581 | 0.0000 | 0.3223 | 0.3174 | 1.0155 | 0.2000 | yes | no | PRETREND_PRESENT | -1 |


## Placebo and stability checks

Each check is reported whether or not it is favourable.

**checks**

| check | description | n_obs | max_abs_post_coef | any_post_significant_5pct | interpretation | status | note | treatment_used | label | n_variants | estimate_spread | min | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| placebo_treatment_date_minus_12m | treatment date moved 12 months earlier, pre-period sample only | 193094 | 0.1104 | yes | a significant 'effect' here means the design picks up differential trends rather than the tariff |  |  |  |  |  |  |  |  |
| placebo_product_group | half the never-treated products labelled treated at the real date | 89375 | 0.2601 | yes |  |  |  |  |  |  |  |  |  |
| announcement_vs_effective |  |  |  |  |  | PARTIAL | the tariff schedule stores announcement and effective dates separately and the event study uses the effective date; an announcement-dated variant requires re-deriving event time from announcement_date and is listed as a remaining milestone | additional_tariff_rate | effective_date_treatment |  |  |  |  |
| leave_one_chapter_out |  |  |  |  |  |  |  |  |  | 10 | 0.2169 | -1.3433 | -1.1264 |
| leave_one_country_out |  |  |  |  |  |  |  |  |  | 8 |  |  |  |


## Leave-one-chapter-out

**Leave-one-chapter-out**

| dropped_chapter | estimate | std_error | n_obs | run_id | git_commit | config | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 39 | -1.1699 | 0.1507 | 304102 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 40 | -1.1507 | 0.1488 | 293985 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 44 | -1.1813 | 0.1538 | 299049 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 48 | -1.1514 | 0.1600 | 295155 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 73 | -1.3433 | 0.1617 | 260082 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 76 | -1.2382 | 0.1497 | 305016 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 84 | -1.1984 | 0.1618 | 258491 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 85 | -1.1888 | 0.1648 | 267240 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 87 | -1.2862 | 0.1577 | 290296 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 94 | -1.1264 | 0.1542 | 298151 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |


## Leave-one-country-out

**Leave-one-country-out**

| dropped_country | estimate | std_error | n_obs | run_id | git_commit | config | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1220 | -1.4030 | 0.1537 | 265174 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 2010 | -1.1782 | 0.1529 | 276022 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5330 | -1.0937 | 0.1478 | 289377 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5490 | -1.1299 | 0.1470 | 296092 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5520 | -1.0341 | 0.1466 | 299373 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5590 | -1.2321 | 0.1489 | 309886 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5800 | -1.2356 | 0.1508 | 286204 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5880 | -1.3329 | 0.1510 | 279086 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |


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
