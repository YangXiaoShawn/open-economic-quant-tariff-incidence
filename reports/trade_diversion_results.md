# Trade Diversion — Results

> **DATA PROVENANCE: OFFICIAL SOURCES**
>
> All figures below derive from official statistical or legal sources.
>
> run_id `20260809T220507Z-597ee5ff` · git `304fded-dirty` · config `sample_slice.yaml` (sha256 `597ee5ffe47a`) · data period 2017-01 to 2019-08 · generated 2026-08-09T22:05:07.519708+00:00


How much sourcing moved away from the treated country, and where it went. The contraction of treated-country imports and the expansion of third-country imports are distinct quantities measured separately.

## Raw decomposition (monthly-average customs value)

- Treated-country change: **-1,940,130,697** (intensive -1,935,333,762, extensive -4,796,935)
- Alternative-source change: **605,856,781** (intensive 655,931,960, extensive -50,075,178)
- Net change in total imports of the treated products: **-1,334,273,916**

The two directions are reported separately and are never netted into one 'diversion' figure.

**totals**

| treated_intensive | treated_extensive | alternative_intensive | alternative_extensive | treated_total | alternative_total | total_change | pre_treated_value | pre_alternative_value | pre_total_value | post_total_value | n_alt_suppliers_entered | n_alt_suppliers_exited | n_treated_flows_exited | treated_pct_change | replacement_ratio | run_id | git_commit | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| -1,935,333,761.6178 | -4,796,935.4907 | 655,931,959.5597 | -50,075,178.0881 | -1,940,130,697.1085 | 605,856,781.4717 | -1,334,273,915.6368 | 5,251,501,172.0544 | 16,242,476,350.1495 | 21,493,977,522.2039 | 20,159,703,606.5671 | 470 | 540 | 23 | -0.3694 | 0.3123 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |


## Why the raw replacement ratio is not the headline

A raw pre-versus-post comparison credits ordinary trade growth to the tariff. Over this window that inflates apparent third-country expansion and can push the replacement ratio above one when nothing was replaced. The counterfactual-adjusted table below nets out the growth of never-treated products, country by country, and is the figure to read.

## Counterfactual-adjusted decomposition

**by partner**

| country_code | pre_monthly_value | post_monthly_value | counterfactual_post_value | excess_change | control_growth_factor | is_treated_country | excess_pct_vs_counterfactual | run_id | git_commit | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5800 | 1,456,838,620.6293 | 1,586,939,426.6484 | 1,282,820,409.6825 | 304,119,016.9659 | 0.8806 | no | 0.2371 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5880 | 2,655,896,210.4242 | 2,822,136,936.7100 | 2,756,674,653.2372 | 65,462,283.4728 | 1.0379 | no | 0.0237 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5330 | 285,322,092.8696 | 317,624,390.8836 | 292,594,427.6663 | 25,029,963.2172 | 1.0255 | no | 0.0855 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 1220 | 3,898,900,958.3505 | 3,843,300,255.8285 | 3,837,044,564.4188 | 6,255,691.4097 | 0.9841 | no | 0.0016 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5590 | 335,127,177.7856 | 302,796,514.6236 | 342,268,299.3235 | -39,471,784.6998 | 1.0213 | no | -0.1153 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5520 | 413,360,354.5043 | 441,056,864.7414 | 531,126,839.4283 | -90,069,974.6869 | 1.2849 | no | -0.1696 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5490 | 473,745,570.9354 | 416,493,489.6985 | 531,161,998.0060 | -114,668,508.3075 | 1.1212 | no | -0.2159 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 2010 | 6,723,285,364.6506 | 7,117,985,252.4872 | 7,415,993,162.9682 | -298,007,910.4810 | 1.1030 | no | -0.0402 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5700 | 5,251,501,172.0544 | 3,311,370,474.9459 | 5,591,058,397.3080 | -2,279,687,922.3621 | 1.0647 | yes | -0.4077 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |


## Partner-country detail

**countries**

| country_code | pre_monthly_value | post_monthly_value | change | pct_change | is_treated_country | pre_share | post_share | share_change | run_id | git_commit | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2010 | 6,723,285,364.6506 | 7,117,985,252.4871 | 394,699,887.8366 | 0.0587 | no | 0.3128 | 0.3531 | 0.0403 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5880 | 2,655,896,210.4242 | 2,822,136,936.7100 | 166,240,726.2857 | 0.0626 | no | 0.1236 | 0.1400 | 0.0164 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5800 | 1,456,838,620.6293 | 1,586,939,426.6484 | 130,100,806.0191 | 0.0893 | no | 0.0678 | 0.0787 | 0.0109 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5330 | 285,322,092.8696 | 317,624,390.8836 | 32,302,298.0140 | 0.1132 | no | 0.0133 | 0.0158 | 0.0025 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5520 | 413,360,354.5043 | 441,056,864.7414 | 27,696,510.2371 | 0.0670 | no | 0.0192 | 0.0219 | 0.0026 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5590 | 335,127,177.7856 | 302,796,514.6236 | -32,330,663.1620 | -0.0965 | no | 0.0156 | 0.0150 | -0.0006 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 1220 | 3,898,900,958.3505 | 3,843,300,255.8285 | -55,600,702.5220 | -0.0143 | no | 0.1814 | 0.1906 | 0.0092 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5490 | 473,745,570.9354 | 416,493,489.6985 | -57,252,081.2369 | -0.1208 | no | 0.0220 | 0.0207 | -0.0014 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| 5700 | 5,251,501,172.0544 | 3,311,370,474.9459 | -1,940,130,697.1085 | -0.3694 | yes | 0.2443 | 0.1643 | -0.0801 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |


## Heterogeneity by pre-treatment dependence

**groups**

| dependence_group | n_products | treated_change | alternative_change | pre_treated_value | median_replacement_ratio | treated_pct_change | run_id | git_commit | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_dependence | 1817 | -4,224,230,910.3266 | -119,994,744.9408 | 12,624,079,500.6563 | 0.2559 | -0.3346 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |
| low_dependence | 1845 | -1,763,891,437.9158 | 977,442,220.5444 | 5,794,588,236.6765 | 0.7127 | -0.3044 | 20260809T215130Z-597ee5ff | f505959-dirty | OFFICIAL | 2017-01..2019-08 |


## Interpretation limits

- The RAW pre-versus-post decomposition attributes ordinary trade growth to the tariff and its replacement ratio is not interpretable on its own. Use the counterfactual-adjusted figures.
- An increase in imports from a third country is not evidence of production relocation. Rerouting of treated-origin goods, transshipment, and origin misdeclaration produce the same pattern in customs data.
- The replacement ratio compares value flows only. It says nothing about whether the replacing goods are the same quality or the same variety.
- Domestic substitution is invisible in import data. A fall in imports that is not matched by third-country gains may reflect domestic production, lower final demand, or inventory drawdown, and these cannot be separated without domestic output data.
- The supplier set is the configured comparison group, not the world. Concentration measures are within-sample.

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
