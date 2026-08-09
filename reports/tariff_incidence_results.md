# Tariff Incidence — Results

> **DATA PROVENANCE: OFFICIAL SOURCES**
>
> All figures below derive from official statistical or legal sources.
>
> run_id `20260809T215131Z-597ee5ff` · git `f505959-dirty` · config `sample_slice.yaml` (sha256 `597ee5ffe47a`) · data period 2017-01 to 2019-08 · generated 2026-08-09T21:51:31.073422+00:00


Estimates of how the additional duty maps into customs unit values, duty-inclusive landed unit values, quantities and trade values. The customs unit value is tariff-exclusive and is a proxy for the foreign border price; it is a value-over-quantity ratio across a heterogeneous bundle of transactions and is **not** a transaction price. The duty-inclusive landed unit value is what the U.S. importer faces at the border, excluding freight. Reading incidence requires both.

## Which of these outcomes survives its own pre-trend test

The parallel-trends assumption is tested per outcome, and it does not hold uniformly. The verdict below governs how each result may be read; it is placed first so it cannot be skipped.

- `log_customs_unit_value`: **PRETREND_PRESENT** under the stacked multi-wave design -> **a causal reading is not supported**; read as descriptive
- `log_landed_unit_value`: **CLEAN** under the stacked multi-wave design -> a causal reading is supported by this test
- `log_quantity`: **NOISY_PRE_PERIOD_NO_SLOPE** under the stacked multi-wave design -> **a qualified causal reading** — no differential trend is detectable, but the pre-period is noisy, so the estimate is less precise than the interval alone suggests. The pre-period slope is not statistically distinguishable from zero; extrapolated across the post window it would shift the estimate by +0.067 against a post-treatment RMS of 0.393.

## Rung 2 — two-way fixed-effects regressions

- **log customs unit value (TARIFF-EXCLUSIVE; foreign border price proxy, not a transaction price)** — `additional_tariff_rate` +0.0884 [95% CI -0.0354, +0.2123] (interval includes zero, so the sign is not resolved), n = 494,794, FE: flow_id|month_key, clustered on hs6
- **log landed unit value (DUTY-INCLUSIVE, excludes freight; U.S. importer border cost)** — `additional_tariff_rate` +0.7969 [95% CI +0.6725, +0.9212]***, n = 494,794, FE: flow_id|month_key, clustered on hs6
- **log import quantity (primary quantity unit)** — `additional_tariff_rate` -1.6403 [95% CI -1.8381, -1.4426]***, n = 494,794, FE: flow_id|month_key, clustered on hs6
- **log customs value** — `additional_tariff_rate` -1.6540 [95% CI -1.8089, -1.4992]***, n = 600,200, FE: flow_id|month_key, clustered on hs6

**estimates**

| outcome | term | estimate | std_error | ci_low | ci_high | p_value | n_obs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| log_customs_unit_value | additional_tariff_rate | 0.0884 | 0.0631 | -0.0354 | 0.2123 | 0.1617 | 494794 |
| log_landed_unit_value | additional_tariff_rate | 0.7969 | 0.0634 | 0.6725 | 0.9212 | 0.0000 | 494794 |
| log_quantity | additional_tariff_rate | -1.6403 | 0.1008 | -1.8381 | -1.4426 | 0.0000 | 494794 |
| log_customs_value | additional_tariff_rate | -1.6540 | 0.0789 | -1.8089 | -1.4992 | 0.0000 | 600200 |


## Rung 5 — PPML on trade flows in levels

- **customs_value (levels, PPML; full sample)** — `log1p_additional_tariff` -2.0596 [95% CI -2.8180, -1.3012]***, n = 773,929, FE: flow_id|month_key, clustered on hs6
- **quantity (levels, PPML; full sample)** — `log1p_additional_tariff` -1.4243 [95% CI -3.0480, +0.1995]* (interval includes zero, so the sign is not resolved), n = 771,699, FE: flow_id|month_key, clustered on hs6
- **customs_value (levels, PPML; subsample with an ad valorem MFN baseline)** — `log1p_total_tariff` -2.4604 [95% CI -3.3538, -1.5670]***, n = 446,346, FE: flow_id|month_key, clustered on hs6
- **quantity (levels, PPML; subsample with an ad valorem MFN baseline)** — `log1p_total_tariff` -1.3900 [95% CI -3.1691, +0.3891] (interval includes zero, so the sign is not resolved), n = 445,518, FE: flow_id|month_key, clustered on hs6

**estimates**

| outcome | term | estimate | std_error | ci_low | ci_high | p_value | n_obs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| customs_value | log1p_additional_tariff | -2.0596 | 0.3866 | -2.8180 | -1.3012 | 0.0000 | 773929 |
| quantity | log1p_additional_tariff | -1.4243 | 0.8278 | -3.0480 | 0.1995 | 0.0855 | 771699 |
| customs_value | log1p_total_tariff | -2.4604 | 0.4554 | -3.3538 | -1.5670 | 0.0000 | 446346 |
| quantity | log1p_total_tariff | -1.3900 | 0.9069 | -3.1691 | 0.3891 | 0.1256 | 445518 |


## Rung 6 — heterogeneity

- **log quantity -- high_pretreatment_dependence (split at median 0.367)** — `additional_tariff_rate` -1.9832 [95% CI -2.2495, -1.7168]***, n = 234,728, FE: flow_id|month_key, clustered on hs6
- **log quantity -- low_pretreatment_dependence (split at median 0.367)** — `additional_tariff_rate` -1.3425 [95% CI -1.6171, -1.0680]***, n = 256,020, FE: flow_id|month_key, clustered on hs6

**estimates**

| outcome | term | estimate | std_error | ci_low | ci_high | p_value | n_obs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| log_quantity | additional_tariff_rate | -1.9832 | 0.1357 | -2.2495 | -1.7168 | 0.0000 | 234728 |
| log_quantity | additional_tariff_rate | -1.3425 | 0.1399 | -1.6171 | -1.0680 | 0.0000 | 256020 |


## Event study — log_customs_unit_value (reference period −1)

Coefficients are relative to event month −1. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.0272 | 0.0238 | -0.0739 | 0.0195 | 0.2528 | yes |
| -11 | -0.0275 | 0.0240 | -0.0747 | 0.0197 | 0.2527 | yes |
| -10 | -0.0032 | 0.0234 | -0.0491 | 0.0428 | 0.8927 | yes |
| -9 | -0.0303 | 0.0233 | -0.0761 | 0.0155 | 0.1946 | yes |
| -8 | -0.0221 | 0.0243 | -0.0696 | 0.0255 | 0.3630 | yes |
| -7 | -0.0253 | 0.0245 | -0.0734 | 0.0227 | 0.3013 | yes |
| -6 | 0.0146 | 0.0238 | -0.0321 | 0.0614 | 0.5396 | yes |
| -5 | 0.0103 | 0.0229 | -0.0346 | 0.0553 | 0.6523 | yes |
| -4 | 0.0064 | 0.0232 | -0.0391 | 0.0518 | 0.7831 | yes |
| -3 | -0.0054 | 0.0219 | -0.0483 | 0.0376 | 0.8068 | yes |
| -2 | -0.0153 | 0.0216 | -0.0577 | 0.0270 | 0.4774 | yes |
| -1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| 0 | -0.0048 | 0.0225 | -0.0489 | 0.0393 | 0.8309 | no |
| 1 | 0.0099 | 0.0215 | -0.0322 | 0.0520 | 0.6460 | no |
| 2 | 0.0203 | 0.0240 | -0.0267 | 0.0673 | 0.3965 | no |
| 3 | -0.0101 | 0.0239 | -0.0571 | 0.0368 | 0.6719 | no |
| 4 | -0.0070 | 0.0258 | -0.0576 | 0.0435 | 0.7847 | no |
| 5 | 0.0289 | 0.0251 | -0.0205 | 0.0782 | 0.2513 | no |
| 6 | 0.0430 | 0.0262 | -0.0084 | 0.0943 | 0.1008 | no |
| 7 | 0.0376 | 0.0232 | -0.0080 | 0.0832 | 0.1058 | no |
| 8 | 0.0288 | 0.0258 | -0.0217 | 0.0794 | 0.2632 | no |
| 9 | -0.0189 | 0.0251 | -0.0680 | 0.0303 | 0.4520 | no |
| 10 | -0.0049 | 0.0246 | -0.0533 | 0.0434 | 0.8423 | no |
|  | -0.0071 | 0.0197 | -0.0457 | 0.0314 | 0.7168 | no |
|  | -0.0040 | 0.0256 | -0.0543 | 0.0463 | 0.8762 | no |


## Event study — log_customs_unit_value (reference period −3)

Coefficients are relative to event month −3. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.0219 | 0.0243 | -0.0695 | 0.0258 | 0.3682 | yes |
| -11 | -0.0222 | 0.0238 | -0.0689 | 0.0246 | 0.3529 | yes |
| -10 | 0.0022 | 0.0235 | -0.0440 | 0.0484 | 0.9256 | yes |
| -9 | -0.0249 | 0.0233 | -0.0707 | 0.0208 | 0.2855 | yes |
| -8 | -0.0167 | 0.0241 | -0.0639 | 0.0305 | 0.4879 | yes |
| -7 | -0.0200 | 0.0251 | -0.0692 | 0.0292 | 0.4254 | yes |
| -6 | 0.0200 | 0.0245 | -0.0282 | 0.0681 | 0.4156 | yes |
| -5 | 0.0157 | 0.0231 | -0.0297 | 0.0611 | 0.4979 | yes |
| -4 | 0.0117 | 0.0229 | -0.0332 | 0.0566 | 0.6082 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | -0.0100 | 0.0228 | -0.0548 | 0.0348 | 0.6620 | yes |
| -1 | 0.0054 | 0.0219 | -0.0376 | 0.0483 | 0.8068 | yes |
| 0 | 0.0006 | 0.0234 | -0.0453 | 0.0464 | 0.9810 | no |
| 1 | 0.0152 | 0.0235 | -0.0310 | 0.0614 | 0.5182 | no |
| 2 | 0.0257 | 0.0261 | -0.0256 | 0.0769 | 0.3257 | no |
| 3 | -0.0048 | 0.0256 | -0.0549 | 0.0454 | 0.8517 | no |
| 4 | -0.0017 | 0.0263 | -0.0532 | 0.0499 | 0.9489 | no |
| 5 | 0.0342 | 0.0268 | -0.0184 | 0.0868 | 0.2020 | no |
| 6 | 0.0483 | 0.0273 | -0.0053 | 0.1019 | 0.0773 | no |
| 7 | 0.0430 | 0.0256 | -0.0073 | 0.0932 | 0.0939 | no |
| 8 | 0.0342 | 0.0259 | -0.0166 | 0.0850 | 0.1867 | no |
| 9 | -0.0135 | 0.0267 | -0.0658 | 0.0388 | 0.6128 | no |
| 10 | 0.0005 | 0.0264 | -0.0513 | 0.0522 | 0.9863 | no |
|  | -0.0018 | 0.0196 | -0.0401 | 0.0366 | 0.9277 | no |
|  | 0.0014 | 0.0266 | -0.0508 | 0.0536 | 0.9591 | no |


## Event study — log_landed_unit_value (reference period −1)

Coefficients are relative to event month −1. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.0171 | 0.0239 | -0.0641 | 0.0298 | 0.4747 | yes |
| -11 | -0.0171 | 0.0242 | -0.0646 | 0.0304 | 0.4801 | yes |
| -10 | 0.0072 | 0.0236 | -0.0390 | 0.0535 | 0.7593 | yes |
| -9 | -0.0201 | 0.0235 | -0.0662 | 0.0260 | 0.3920 | yes |
| -8 | -0.0118 | 0.0243 | -0.0596 | 0.0359 | 0.6265 | yes |
| -7 | -0.0154 | 0.0246 | -0.0636 | 0.0329 | 0.5318 | yes |
| -6 | 0.0246 | 0.0239 | -0.0223 | 0.0715 | 0.3040 | yes |
| -5 | 0.0193 | 0.0230 | -0.0257 | 0.0644 | 0.4001 | yes |
| -4 | 0.0139 | 0.0232 | -0.0316 | 0.0594 | 0.5479 | yes |
| -3 | -0.0009 | 0.0219 | -0.0439 | 0.0421 | 0.9674 | yes |
| -2 | -0.0144 | 0.0216 | -0.0567 | 0.0280 | 0.5061 | yes |
| -1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| 0 | 0.0428 | 0.0227 | -0.0018 | 0.0874 | 0.0598 | no |
| 1 | 0.1358 | 0.0215 | 0.0935 | 0.1780 | 0.0000 | no |
| 2 | 0.1508 | 0.0245 | 0.1028 | 0.1987 | 0.0000 | no |
| 3 | 0.1200 | 0.0243 | 0.0723 | 0.1677 | 0.0000 | no |
| 4 | 0.1226 | 0.0259 | 0.0717 | 0.1734 | 0.0000 | no |
| 5 | 0.1584 | 0.0254 | 0.1085 | 0.2082 | 0.0000 | no |
| 6 | 0.1739 | 0.0264 | 0.1222 | 0.2257 | 0.0000 | no |
| 7 | 0.1678 | 0.0235 | 0.1218 | 0.2138 | 0.0000 | no |
| 8 | 0.1685 | 0.0260 | 0.1174 | 0.2196 | 0.0000 | no |
| 9 | 0.1663 | 0.0251 | 0.1172 | 0.2155 | 0.0000 | no |
| 10 | 0.1904 | 0.0246 | 0.1422 | 0.2387 | 0.0000 | no |
|  | 0.0045 | 0.0199 | -0.0345 | 0.0434 | 0.8222 | no |
|  | 0.1771 | 0.0257 | 0.1266 | 0.2276 | 0.0000 | no |


## Event study — log_landed_unit_value (reference period −3)

Coefficients are relative to event month −3. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.0162 | 0.0244 | -0.0641 | 0.0317 | 0.5065 | yes |
| -11 | -0.0162 | 0.0239 | -0.0632 | 0.0308 | 0.4989 | yes |
| -10 | 0.0081 | 0.0236 | -0.0382 | 0.0545 | 0.7310 | yes |
| -9 | -0.0192 | 0.0234 | -0.0651 | 0.0267 | 0.4119 | yes |
| -8 | -0.0110 | 0.0241 | -0.0583 | 0.0364 | 0.6502 | yes |
| -7 | -0.0145 | 0.0251 | -0.0638 | 0.0348 | 0.5644 | yes |
| -6 | 0.0255 | 0.0246 | -0.0228 | 0.0737 | 0.3002 | yes |
| -5 | 0.0202 | 0.0232 | -0.0252 | 0.0657 | 0.3827 | yes |
| -4 | 0.0148 | 0.0229 | -0.0301 | 0.0598 | 0.5172 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | -0.0135 | 0.0228 | -0.0583 | 0.0313 | 0.5553 | yes |
| -1 | 0.0009 | 0.0219 | -0.0421 | 0.0439 | 0.9674 | yes |
| 0 | 0.0437 | 0.0236 | -0.0026 | 0.0900 | 0.0641 | no |
| 1 | 0.1367 | 0.0236 | 0.0904 | 0.1829 | 0.0000 | no |
| 2 | 0.1517 | 0.0266 | 0.0996 | 0.2037 | 0.0000 | no |
| 3 | 0.1209 | 0.0259 | 0.0701 | 0.1717 | 0.0000 | no |
| 4 | 0.1235 | 0.0264 | 0.0716 | 0.1753 | 0.0000 | no |
| 5 | 0.1593 | 0.0270 | 0.1064 | 0.2121 | 0.0000 | no |
| 6 | 0.1748 | 0.0276 | 0.1208 | 0.2289 | 0.0000 | no |
| 7 | 0.1687 | 0.0258 | 0.1180 | 0.2194 | 0.0000 | no |
| 8 | 0.1694 | 0.0261 | 0.1181 | 0.2207 | 0.0000 | no |
| 9 | 0.1672 | 0.0267 | 0.1149 | 0.2196 | 0.0000 | no |
| 10 | 0.1913 | 0.0263 | 0.1397 | 0.2429 | 0.0000 | no |
|  | 0.0054 | 0.0197 | -0.0333 | 0.0440 | 0.7854 | no |
|  | 0.1780 | 0.0267 | 0.1256 | 0.2304 | 0.0000 | no |


## Event study — log_quantity (reference period −1)

Coefficients are relative to event month −1. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.1259 | 0.0336 | -0.1918 | -0.0601 | 0.0002 | yes |
| -11 | -0.1254 | 0.0330 | -0.1900 | -0.0607 | 0.0001 | yes |
| -10 | -0.2051 | 0.0322 | -0.2682 | -0.1419 | 0.0000 | yes |
| -9 | -0.1060 | 0.0333 | -0.1714 | -0.0406 | 0.0015 | yes |
| -8 | -0.0562 | 0.0323 | -0.1196 | 0.0071 | 0.0816 | yes |
| -7 | -0.0243 | 0.0323 | -0.0877 | 0.0392 | 0.4531 | yes |
| -6 | -0.1790 | 0.0339 | -0.2456 | -0.1125 | 0.0000 | yes |
| -5 | -0.2273 | 0.0330 | -0.2920 | -0.1626 | 0.0000 | yes |
| -4 | -0.1267 | 0.0311 | -0.1877 | -0.0657 | 0.0000 | yes |
| -3 | -0.0570 | 0.0280 | -0.1120 | -0.0020 | 0.0421 | yes |
| -2 | 0.0115 | 0.0283 | -0.0441 | 0.0671 | 0.6850 | yes |
| -1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| 0 | -0.0910 | 0.0298 | -0.1495 | -0.0325 | 0.0023 | no |
| 1 | -0.2392 | 0.0297 | -0.2975 | -0.1809 | 0.0000 | no |
| 2 | -0.3074 | 0.0340 | -0.3741 | -0.2407 | 0.0000 | no |
| 3 | -0.1062 | 0.0389 | -0.1825 | -0.0298 | 0.0065 | no |
| 4 | -0.3845 | 0.0373 | -0.4577 | -0.3112 | 0.0000 | no |
| 5 | -0.4508 | 0.0368 | -0.5231 | -0.3786 | 0.0000 | no |
| 6 | -0.5977 | 0.0369 | -0.6701 | -0.5254 | 0.0000 | no |
| 7 | -0.6160 | 0.0368 | -0.6883 | -0.5438 | 0.0000 | no |
| 8 | -0.5230 | 0.0384 | -0.5982 | -0.4477 | 0.0000 | no |
| 9 | -0.5098 | 0.0367 | -0.5818 | -0.4378 | 0.0000 | no |
| 10 | -0.5485 | 0.0363 | -0.6197 | -0.4773 | 0.0000 | no |
|  | -0.1734 | 0.0300 | -0.2324 | -0.1145 | 0.0000 | no |
|  | -0.5780 | 0.0383 | -0.6531 | -0.5029 | 0.0000 | no |


## Event study — log_quantity (reference period −3)

Coefficients are relative to event month −3. Pre-period coefficients are the test of the design, not decoration.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.0689 | 0.0342 | -0.1360 | -0.0018 | 0.0441 | yes |
| -11 | -0.0684 | 0.0332 | -0.1335 | -0.0032 | 0.0398 | yes |
| -10 | -0.1480 | 0.0328 | -0.2123 | -0.0837 | 0.0000 | yes |
| -9 | -0.0490 | 0.0322 | -0.1122 | 0.0142 | 0.1286 | yes |
| -8 | 0.0008 | 0.0315 | -0.0610 | 0.0626 | 0.9802 | yes |
| -7 | 0.0327 | 0.0317 | -0.0294 | 0.0949 | 0.3018 | yes |
| -6 | -0.1220 | 0.0333 | -0.1873 | -0.0567 | 0.0003 | yes |
| -5 | -0.1703 | 0.0323 | -0.2338 | -0.1069 | 0.0000 | yes |
| -4 | -0.0697 | 0.0281 | -0.1248 | -0.0145 | 0.0133 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | 0.0685 | 0.0284 | 0.0128 | 0.1242 | 0.0159 | yes |
| -1 | 0.0570 | 0.0280 | 0.0020 | 0.1120 | 0.0421 | yes |
| 0 | -0.0340 | 0.0312 | -0.0952 | 0.0273 | 0.2770 | no |
| 1 | -0.1822 | 0.0316 | -0.2442 | -0.1202 | 0.0000 | no |
| 2 | -0.2504 | 0.0350 | -0.3191 | -0.1817 | 0.0000 | no |
| 3 | -0.0492 | 0.0369 | -0.1215 | 0.0231 | 0.1825 | no |
| 4 | -0.3275 | 0.0376 | -0.4012 | -0.2537 | 0.0000 | no |
| 5 | -0.3938 | 0.0382 | -0.4687 | -0.3189 | 0.0000 | no |
| 6 | -0.5407 | 0.0382 | -0.6157 | -0.4657 | 0.0000 | no |
| 7 | -0.5590 | 0.0377 | -0.6329 | -0.4851 | 0.0000 | no |
| 8 | -0.4660 | 0.0359 | -0.5364 | -0.3955 | 0.0000 | no |
| 9 | -0.4527 | 0.0367 | -0.5248 | -0.3807 | 0.0000 | no |
| 10 | -0.4914 | 0.0378 | -0.5655 | -0.4174 | 0.0000 | no |
|  | -0.1164 | 0.0298 | -0.1748 | -0.0580 | 0.0001 | no |
|  | -0.5210 | 0.0380 | -0.5954 | -0.4465 | 0.0000 | no |


## Stacked multi-wave event study — log_landed_unit_value (controls: never_treated_products)

One sub-experiment per Section 301 wave, each drawing controls from never-treated products only, with flow-by-stack and calendar-month-by-stack effects. No already-treated unit is ever used as a control.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.0116 | 0.0268 | -0.0641 | 0.0409 | 0.6639 | yes |
| -11 | -0.0024 | 0.0256 | -0.0526 | 0.0478 | 0.9253 | yes |
| -10 | 0.0168 | 0.0253 | -0.0329 | 0.0665 | 0.5068 | yes |
| -9 | -0.0225 | 0.0255 | -0.0725 | 0.0276 | 0.3786 | yes |
| -8 | -0.0016 | 0.0262 | -0.0530 | 0.0497 | 0.9502 | yes |
| -7 | -0.0178 | 0.0270 | -0.0707 | 0.0351 | 0.5093 | yes |
| -6 | 0.0245 | 0.0259 | -0.0262 | 0.0753 | 0.3430 | yes |
| -5 | 0.0230 | 0.0248 | -0.0257 | 0.0717 | 0.3537 | yes |
| -4 | 0.0161 | 0.0246 | -0.0322 | 0.0643 | 0.5138 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | -0.0199 | 0.0242 | -0.0675 | 0.0277 | 0.4119 | yes |
| -1 | 0.0101 | 0.0234 | -0.0358 | 0.0560 | 0.6655 | yes |
| 0 | 0.0403 | 0.0254 | -0.0096 | 0.0901 | 0.1131 | no |
| 1 | 0.1444 | 0.0251 | 0.0951 | 0.1937 | 0.0000 | no |
| 2 | 0.1498 | 0.0279 | 0.0952 | 0.2045 | 0.0000 | no |
| 3 | 0.1279 | 0.0273 | 0.0744 | 0.1814 | 0.0000 | no |
| 4 | 0.1196 | 0.0275 | 0.0656 | 0.1736 | 0.0000 | no |
| 5 | 0.1591 | 0.0286 | 0.1031 | 0.2152 | 0.0000 | no |
| 6 | 0.1834 | 0.0301 | 0.1244 | 0.2424 | 0.0000 | no |
| 7 | 0.1799 | 0.0279 | 0.1252 | 0.2345 | 0.0000 | no |
| 8 | 0.1794 | 0.0283 | 0.1239 | 0.2349 | 0.0000 | no |
| 9 | 0.1680 | 0.0286 | 0.1119 | 0.2241 | 0.0000 | no |
| 10 | 0.1912 | 0.0286 | 0.1350 | 0.2474 | 0.0000 | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |


## Stacked multi-wave event study — log_customs_unit_value (controls: never_treated_products)

One sub-experiment per Section 301 wave, each drawing controls from never-treated products only, with flow-by-stack and calendar-month-by-stack effects. No already-treated unit is ever used as a control.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.0215 | 0.0265 | -0.0735 | 0.0305 | 0.4175 | yes |
| -11 | -0.0123 | 0.0253 | -0.0620 | 0.0374 | 0.6281 | yes |
| -10 | 0.0066 | 0.0251 | -0.0426 | 0.0557 | 0.7933 | yes |
| -9 | -0.0322 | 0.0252 | -0.0817 | 0.0173 | 0.2016 | yes |
| -8 | -0.0117 | 0.0260 | -0.0626 | 0.0392 | 0.6526 | yes |
| -7 | -0.0274 | 0.0268 | -0.0799 | 0.0252 | 0.3071 | yes |
| -6 | 0.0148 | 0.0257 | -0.0356 | 0.0652 | 0.5641 | yes |
| -5 | 0.0149 | 0.0247 | -0.0335 | 0.0634 | 0.5458 | yes |
| -4 | 0.0103 | 0.0245 | -0.0378 | 0.0584 | 0.6753 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | -0.0170 | 0.0243 | -0.0645 | 0.0306 | 0.4847 | yes |
| -1 | 0.0158 | 0.0234 | -0.0301 | 0.0617 | 0.4991 | yes |
| 0 | 0.0005 | 0.0252 | -0.0490 | 0.0499 | 0.9854 | no |
| 1 | 0.0233 | 0.0251 | -0.0259 | 0.0726 | 0.3531 | no |
| 2 | 0.0253 | 0.0275 | -0.0285 | 0.0792 | 0.3562 | no |
| 3 | 0.0040 | 0.0269 | -0.0489 | 0.0568 | 0.8829 | no |
| 4 | -0.0036 | 0.0274 | -0.0573 | 0.0501 | 0.8954 | no |
| 5 | 0.0361 | 0.0284 | -0.0196 | 0.0918 | 0.2035 | no |
| 6 | 0.0601 | 0.0299 | 0.0015 | 0.1186 | 0.0445 | no |
| 7 | 0.0586 | 0.0277 | 0.0042 | 0.1129 | 0.0346 | no |
| 8 | 0.0492 | 0.0281 | -0.0059 | 0.1043 | 0.0801 | no |
| 9 | -0.0089 | 0.0286 | -0.0649 | 0.0471 | 0.7556 | no |
| 10 | 0.0034 | 0.0287 | -0.0530 | 0.0597 | 0.9069 | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |


## Stacked multi-wave event study — log_quantity (controls: never_treated_products)

One sub-experiment per Section 301 wave, each drawing controls from never-treated products only, with flow-by-stack and calendar-month-by-stack effects. No already-treated unit is ever used as a control.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.1016 | 0.0373 | -0.1749 | -0.0284 | 0.0066 | yes |
| -11 | -0.1089 | 0.0359 | -0.1793 | -0.0385 | 0.0024 | yes |
| -10 | -0.1884 | 0.0358 | -0.2586 | -0.1181 | 0.0000 | yes |
| -9 | -0.0583 | 0.0356 | -0.1281 | 0.0116 | 0.1021 | yes |
| -8 | -0.0332 | 0.0344 | -0.1007 | 0.0343 | 0.3347 | yes |
| -7 | 0.0132 | 0.0345 | -0.0544 | 0.0809 | 0.7013 | yes |
| -6 | -0.1325 | 0.0355 | -0.2023 | -0.0628 | 0.0002 | yes |
| -5 | -0.1827 | 0.0344 | -0.2502 | -0.1153 | 0.0000 | yes |
| -4 | -0.0807 | 0.0300 | -0.1396 | -0.0218 | 0.0073 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | 0.0645 | 0.0302 | 0.0052 | 0.1238 | 0.0329 | yes |
| -1 | 0.0375 | 0.0299 | -0.0212 | 0.0961 | 0.2103 | yes |
| 0 | -0.0284 | 0.0336 | -0.0944 | 0.0376 | 0.3986 | no |
| 1 | -0.2144 | 0.0339 | -0.2809 | -0.1478 | 0.0000 | no |
| 2 | -0.2834 | 0.0377 | -0.3574 | -0.2095 | 0.0000 | no |
| 3 | -0.0664 | 0.0387 | -0.1424 | 0.0096 | 0.0866 | no |
| 4 | -0.3192 | 0.0393 | -0.3963 | -0.2421 | 0.0000 | no |
| 5 | -0.3837 | 0.0397 | -0.4615 | -0.3058 | 0.0000 | no |
| 6 | -0.5454 | 0.0406 | -0.6250 | -0.4659 | 0.0000 | no |
| 7 | -0.5756 | 0.0395 | -0.6531 | -0.4981 | 0.0000 | no |
| 8 | -0.4865 | 0.0379 | -0.5610 | -0.4121 | 0.0000 | no |
| 9 | -0.4538 | 0.0389 | -0.5301 | -0.3776 | 0.0000 | no |
| 10 | -0.4965 | 0.0398 | -0.5746 | -0.4185 | 0.0000 | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |


## Stacked multi-wave event study — log_landed_unit_value (controls: never_treated_products_treated_country_only)

One sub-experiment per Section 301 wave, each drawing controls from never-treated products only, with flow-by-stack and calendar-month-by-stack effects. No already-treated unit is ever used as a control.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | 0.0398 | 0.0429 | -0.0443 | 0.1240 | 0.3532 | yes |
| -11 | 0.0403 | 0.0409 | -0.0400 | 0.1205 | 0.3252 | yes |
| -10 | 0.0676 | 0.0411 | -0.0131 | 0.1482 | 0.1007 | yes |
| -9 | 0.0466 | 0.0389 | -0.0298 | 0.1229 | 0.2319 | yes |
| -8 | 0.0549 | 0.0400 | -0.0236 | 0.1334 | 0.1701 | yes |
| -7 | 0.0565 | 0.0394 | -0.0207 | 0.1337 | 0.1511 | yes |
| -6 | 0.0789 | 0.0401 | 0.0001 | 0.1576 | 0.0496 | yes |
| -5 | 0.0351 | 0.0349 | -0.0334 | 0.1037 | 0.3149 | yes |
| -4 | 0.0440 | 0.0333 | -0.0212 | 0.1093 | 0.1858 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | -0.0063 | 0.0304 | -0.0659 | 0.0533 | 0.8348 | yes |
| -1 | 0.0023 | 0.0315 | -0.0595 | 0.0640 | 0.9427 | yes |
| 0 | 0.0498 | 0.0379 | -0.0245 | 0.1241 | 0.1887 | no |
| 1 | 0.1649 | 0.0384 | 0.0895 | 0.2403 | 0.0000 | no |
| 2 | 0.2064 | 0.0407 | 0.1265 | 0.2862 | 0.0000 | no |
| 3 | 0.1815 | 0.0406 | 0.1019 | 0.2611 | 0.0000 | no |
| 4 | 0.1624 | 0.0405 | 0.0831 | 0.2418 | 0.0001 | no |
| 5 | 0.2282 | 0.0419 | 0.1460 | 0.3103 | 0.0000 | no |
| 6 | 0.2069 | 0.0441 | 0.1205 | 0.2934 | 0.0000 | no |
| 7 | 0.2350 | 0.0425 | 0.1516 | 0.3185 | 0.0000 | no |
| 8 | 0.2038 | 0.0429 | 0.1196 | 0.2881 | 0.0000 | no |
| 9 | 0.2241 | 0.0415 | 0.1426 | 0.3056 | 0.0000 | no |
| 10 | 0.2473 | 0.0419 | 0.1652 | 0.3294 | 0.0000 | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |


## Stacked multi-wave event study — log_customs_unit_value (controls: never_treated_products_treated_country_only)

One sub-experiment per Section 301 wave, each drawing controls from never-treated products only, with flow-by-stack and calendar-month-by-stack effects. No already-treated unit is ever used as a control.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | 0.0094 | 0.0405 | -0.0701 | 0.0890 | 0.8157 | yes |
| -11 | 0.0099 | 0.0387 | -0.0661 | 0.0859 | 0.7985 | yes |
| -10 | 0.0362 | 0.0387 | -0.0397 | 0.1120 | 0.3501 | yes |
| -9 | 0.0164 | 0.0370 | -0.0562 | 0.0889 | 0.6583 | yes |
| -8 | 0.0236 | 0.0383 | -0.0516 | 0.0988 | 0.5384 | yes |
| -7 | 0.0257 | 0.0380 | -0.0487 | 0.1002 | 0.4978 | yes |
| -6 | 0.0477 | 0.0390 | -0.0288 | 0.1242 | 0.2212 | yes |
| -5 | 0.0116 | 0.0343 | -0.0557 | 0.0789 | 0.7359 | yes |
| -4 | 0.0317 | 0.0328 | -0.0327 | 0.0961 | 0.3343 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | 0.0017 | 0.0305 | -0.0582 | 0.0616 | 0.9556 | yes |
| -1 | 0.0124 | 0.0313 | -0.0491 | 0.0739 | 0.6918 | yes |
| 0 | 0.0062 | 0.0378 | -0.0680 | 0.0804 | 0.8701 | no |
| 1 | 0.0347 | 0.0384 | -0.0406 | 0.1099 | 0.3666 | no |
| 2 | 0.0727 | 0.0408 | -0.0074 | 0.1528 | 0.0753 | no |
| 3 | 0.0477 | 0.0404 | -0.0316 | 0.1271 | 0.2381 | no |
| 4 | 0.0305 | 0.0406 | -0.0492 | 0.1102 | 0.4536 | no |
| 5 | 0.0965 | 0.0420 | 0.0142 | 0.1789 | 0.0217 | no |
| 6 | 0.0752 | 0.0442 | -0.0115 | 0.1618 | 0.0891 | no |
| 7 | 0.1058 | 0.0428 | 0.0219 | 0.1897 | 0.0135 | no |
| 8 | 0.0677 | 0.0430 | -0.0166 | 0.1521 | 0.1154 | no |
| 9 | 0.0526 | 0.0416 | -0.0290 | 0.1342 | 0.2060 | no |
| 10 | 0.0691 | 0.0419 | -0.0131 | 0.1512 | 0.0992 | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |


## Stacked multi-wave event study — log_quantity (controls: never_treated_products_treated_country_only)

One sub-experiment per Section 301 wave, each drawing controls from never-treated products only, with flow-by-stack and calendar-month-by-stack effects. No already-treated unit is ever used as a control.

**coefficients**

| event_time | estimate | std_error | ci_low | ci_high | p_value | is_pre |
| --- | --- | --- | --- | --- | --- | --- |
| -12 | -0.2899 | 0.0751 | -0.4372 | -0.1426 | 0.0001 | yes |
| -11 | -0.2619 | 0.0719 | -0.4030 | -0.1208 | 0.0003 | yes |
| -10 | -0.3674 | 0.0733 | -0.5111 | -0.2237 | 0.0000 | yes |
| -9 | -0.3213 | 0.0651 | -0.4490 | -0.1935 | 0.0000 | yes |
| -8 | -0.3038 | 0.0631 | -0.4276 | -0.1800 | 0.0000 | yes |
| -7 | -0.2447 | 0.0601 | -0.3625 | -0.1268 | 0.0000 | yes |
| -6 | -0.3138 | 0.0630 | -0.4374 | -0.1901 | 0.0000 | yes |
| -5 | -0.2118 | 0.0509 | -0.3116 | -0.1120 | 0.0000 | yes |
| -4 | -0.1081 | 0.0462 | -0.1989 | -0.0174 | 0.0195 | yes |
| -3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | yes |
| -2 | -0.0008 | 0.0415 | -0.0822 | 0.0805 | 0.9842 | yes |
| -1 | -0.0098 | 0.0468 | -0.1015 | 0.0820 | 0.8345 | yes |
| 0 | -0.1716 | 0.0608 | -0.2908 | -0.0524 | 0.0048 | no |
| 1 | -0.3855 | 0.0633 | -0.5096 | -0.2614 | 0.0000 | no |
| 2 | -0.5100 | 0.0693 | -0.6459 | -0.3740 | 0.0000 | no |
| 3 | -0.3795 | 0.0626 | -0.5023 | -0.2567 | 0.0000 | no |
| 4 | -0.5516 | 0.0614 | -0.6721 | -0.4310 | 0.0000 | no |
| 5 | -0.6067 | 0.0597 | -0.7237 | -0.4896 | 0.0000 | no |
| 6 | -0.5500 | 0.0624 | -0.6725 | -0.4275 | 0.0000 | no |
| 7 | -0.6624 | 0.0622 | -0.7844 | -0.5404 | 0.0000 | no |
| 8 | -0.5250 | 0.0615 | -0.6456 | -0.4044 | 0.0000 | no |
| 9 | -0.6116 | 0.0623 | -0.7339 | -0.4893 | 0.0000 | no |
| 10 | -0.6695 | 0.0641 | -0.7953 | -0.5437 | 0.0000 | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |
|  | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  | no |


## Stacked design composition

How much weight each wave carries, reported rather than buried.

**stacks**

| stack_id | n_obs | n_treated_obs | n_products | treatment_month_index | run_id | git_commit | config | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SEC301_LIST1 | 262359 | 26245 | 2503 | 24223 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| SEC301_LIST2 | 150827 | 7348 | 1484 | 24224 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| SEC301_LIST3 | 356362 | 44864 | 3453 | 24225 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |


## Pre-treatment trend tests

Two criteria are reported. Statistical detectability alone is a poor guide in a large panel, where standard errors shrink until economically trivial pre-period movement becomes significant; the verdict field combines significance with magnitude relative to the post-treatment coefficients.

**pre-trend tests**

| test | n_pre_coefs | approx_chi2 | approx_p_value | any_pre_significant_5pct | max_abs_pre_coef | rms_pre_coef | mean_abs_post_coef | rms_post_coef | max_abs_post_coef | rms_pre_relative_to_rms_post | max_pre_relative_to_max_post | max_pre_relative_to_mean_post | pre_slope_per_month | pre_slope_se | pre_slope_p_value | implied_bias_over_post_window | slope_material | economically_small | relative_threshold | verdict | reference_period | design | control_definition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pretrend_log_customs_unit_value_ref3 | 11 | 5.5779 | 0.9000 | no | 0.0249 | 0.0170 | 0.0201 | 0.0263 | 0.0483 | 0.6466 | 0.5159 | 1.2375 | 0.0025 | 0.0013 | 0.0763 | 0.0127 | yes | no | 0.2000 | PRETREND_PRESENT | -3 |  |  |
| pretrend_log_customs_unit_value_ref1 | 11 | 7.4378 | 0.7626 | no | 0.0303 | 0.0195 | 0.0195 | 0.0233 | 0.0430 | 0.8355 | 0.7050 | 1.5553 | 0.0025 | 0.0014 | 0.1032 | 0.0126 | yes | no | 0.2000 | PRETREND_PRESENT | -1 |  |  |
| pretrend_log_landed_unit_value_ref3 | 11 | 4.8352 | 0.9389 | no | 0.0255 | 0.0158 | 0.1461 | 0.1511 | 0.1913 | 0.1047 | 0.1332 | 0.1744 | 0.0016 | 0.0014 | 0.2717 | 0.0081 | no | yes | 0.2000 | CLEAN | -3 |  |  |
| pretrend_log_landed_unit_value_ref1 | 11 | 5.0369 | 0.9294 | no | 0.0246 | 0.0160 | 0.1452 | 0.1502 | 0.1904 | 0.1062 | 0.1291 | 0.1693 | 0.0017 | 0.0015 | 0.2767 | 0.0087 | no | yes | 0.2000 | CLEAN | -1 |  |  |
| pretrend_log_quantity_ref3 | 11 | 89.3326 | 0.0000 | yes | 0.1703 | 0.0912 | 0.3406 | 0.3850 | 0.5590 | 0.2369 | 0.3047 | 0.5000 | 0.0109 | 0.0065 | 0.1311 | 0.0543 | no | no | 0.2000 | NOISY_PRE_PERIOD_NO_SLOPE | -3 |  |  |
| pretrend_log_quantity_ref1 | 11 | 179.1134 | 0.0000 | yes | 0.2273 | 0.1320 | 0.3976 | 0.4362 | 0.6160 | 0.3027 | 0.3690 | 0.5717 | 0.0090 | 0.0069 | 0.2236 | 0.0449 | no | no | 0.2000 | NOISY_PRE_PERIOD_NO_SLOPE | -1 |  |  |
| pretrend_stacked_log_landed_unit_value_never_treated_products | 11 | 4.9018 | 0.9358 | no | 0.0245 | 0.0169 | 0.1494 | 0.1549 | 0.1912 | 0.1090 | 0.1283 | 0.1642 | 0.0010 | 0.0016 | 0.5398 | 0.0050 | no | yes | 0.2000 | CLEAN |  | stacked_multi_wave | never_treated_products |
| pretrend_stacked_log_customs_unit_value_never_treated_products | 11 | 5.6588 | 0.8951 | no | 0.0322 | 0.0183 | 0.0248 | 0.0331 | 0.0601 | 0.5512 | 0.5368 | 1.2997 | 0.0024 | 0.0015 | 0.1423 | 0.0118 | yes | no | 0.2000 | PRETREND_PRESENT |  | stacked_multi_wave | never_treated_products |
| pretrend_stacked_log_quantity_never_treated_products | 11 | 103.5284 | 0.0000 | yes | 0.1884 | 0.1068 | 0.3503 | 0.3930 | 0.5756 | 0.2717 | 0.3272 | 0.5377 | 0.0134 | 0.0065 | 0.0678 | 0.0671 | no | no | 0.2000 | NOISY_PRE_PERIOD_NO_SLOPE |  | stacked_multi_wave | never_treated_products |
| pretrend_stacked_log_landed_unit_value_never_treated_products_treated_country_only | 11 | 16.5805 | 0.1209 | yes | 0.0789 | 0.0482 | 0.1918 | 0.1988 | 0.2473 | 0.2426 | 0.3189 | 0.4110 | -0.0050 | 0.0018 | 0.0233 | -0.0248 | no | no | 0.2000 | NOISY_PRE_PERIOD_NO_SLOPE |  | stacked_multi_wave | never_treated_products_treated_country_only |
| pretrend_stacked_log_customs_unit_value_never_treated_products_treated_country_only | 11 | 4.7323 | 0.9434 | no | 0.0477 | 0.0244 | 0.0599 | 0.0661 | 0.1058 | 0.3694 | 0.4509 | 0.7969 | -0.0007 | 0.0012 | 0.5733 | -0.0035 | no | no | 0.2000 | NOISY_PRE_PERIOD_NO_SLOPE |  | stacked_multi_wave | never_treated_products_treated_country_only |
| pretrend_stacked_log_quantity_never_treated_products_treated_country_only | 11 | 165.0330 | 0.0000 | yes | 0.3674 | 0.2519 | 0.5112 | 0.5303 | 0.6695 | 0.4750 | 0.5488 | 0.7187 | 0.0344 | 0.0057 | 0.0002 | 0.1719 | yes | no | 0.2000 | PRETREND_PRESENT |  | stacked_multi_wave | never_treated_products_treated_country_only |


## Placebo and stability checks

Each check is reported whether or not it is favourable.

**checks**

| check | description | n_obs | max_abs_post_coef | any_post_significant_5pct | interpretation | status | note | treatment_used | label | n_variants | estimate_spread | min | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| placebo_treatment_date_minus_12m | treatment date moved 12 months earlier, pre-period sample only | 268171 | 0.0943 | yes | a significant 'effect' here means the design picks up differential trends rather than the tariff |  |  |  |  |  |  |  |  |
| placebo_product_group | half the never-treated products labelled treated at the real date | 93100 | 0.2498 | yes |  |  |  |  |  |  |  |  |  |
| announcement_vs_effective |  |  |  |  |  | PARTIAL | the tariff schedule stores announcement and effective dates separately and the event study uses the effective date; an announcement-dated variant requires re-deriving event time from announcement_date and is listed as a remaining milestone | additional_tariff_rate | effective_date_treatment |  |  |  |  |
| leave_one_chapter_out |  |  |  |  |  |  |  |  |  | 10 | 0.2393 | -1.7612 | -1.5219 |
| leave_one_country_out |  |  |  |  |  |  |  |  |  | 8 |  |  |  |


## Leave-one-chapter-out

**Leave-one-chapter-out**

| dropped_chapter | estimate | std_error | n_obs | run_id | git_commit | config | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 39 | -1.5219 | 0.1067 | 450705 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 40 | -1.6339 | 0.1018 | 469526 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 44 | -1.6500 | 0.1028 | 474780 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 48 | -1.6439 | 0.1040 | 470886 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 73 | -1.7239 | 0.1043 | 434155 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 76 | -1.6542 | 0.1011 | 480506 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 84 | -1.7612 | 0.1277 | 349648 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 85 | -1.5371 | 0.1140 | 390713 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 87 | -1.6787 | 0.1042 | 458345 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 94 | -1.6272 | 0.1026 | 473882 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |


## Leave-one-country-out

**Leave-one-country-out**

| dropped_country | estimate | std_error | n_obs | run_id | git_commit | config | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1220 | -1.7775 | 0.1034 | 411879 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 2010 | -1.6336 | 0.1035 | 428913 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5330 | -1.5557 | 0.1012 | 449469 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5490 | -1.6031 | 0.1008 | 461350 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5520 | -1.5347 | 0.1006 | 469129 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5590 | -1.6621 | 0.1014 | 477237 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5800 | -1.6462 | 0.1017 | 441386 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| 5880 | -1.7327 | 0.1017 | 425208 | 20260809T214912Z-597ee5ff | f505959-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |


---

## Reproducibility

- run id: `20260809T215131Z-597ee5ff`
- git commit: `f505959-dirty`
- configuration: `sample_slice.yaml` (sha256 `597ee5ffe47af577cc12c18a77fbd8ceb65895fed1ca83ff18eb0e2ce7bb7338`)
- data provenance: `OFFICIAL`
- data period: 2017-01 to 2019-08
- generated: 2026-08-09T21:51:31.073422+00:00
- python 3.12.13 on macOS-26.6.1-arm64-arm-64bit

_This document is generated by `scripts/generate_reports.py`. Do not edit it by hand; edit the generator or the underlying result tables._
