# Trade Diversion — Results

> **DATA PROVENANCE: OFFICIAL SOURCES**
>
> All figures below derive from official statistical or legal sources.
>
> run_id `20260809T194259Z-597ee5ff` · git `c53443d-dirty` · config `sample_slice.yaml` (sha256 `597ee5ffe47a`) · data period 2017-01 to 2019-08 · generated 2026-08-09T19:42:59.887758+00:00


How much sourcing moved away from the treated country, and where it went. The contraction of treated-country imports and the expansion of third-country imports are distinct quantities measured separately.

## Raw decomposition (monthly-average customs value)

- Treated-country change: **-1,586,378,606** (intensive -1,582,041,588, extensive -4,337,018)
- Alternative-source change: **-129,125,506** (intensive -86,485,526, extensive -42,639,980)
- Net change in total imports of the treated products: **-1,715,504,113**

The two directions are reported separately and are never netted into one 'diversion' figure.

**totals**

| treated_intensive | treated_extensive | alternative_intensive | alternative_extensive | treated_total | alternative_total | total_change | pre_treated_value | pre_alternative_value | pre_total_value | post_total_value | n_alt_suppliers_entered | n_alt_suppliers_exited | n_treated_flows_exited | treated_pct_change | replacement_ratio | run_id | git_commit | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| -1,582,041,588.3204 | -4,337,017.8056 | -86,485,526.3732 | -42,639,980.0425 | -1,586,378,606.1260 | -129,125,506.4158 | -1,715,504,112.5418 | 4,170,431,011.1524 | 6,183,241,698.4242 | 10,353,672,709.5766 | 8,638,168,597.0348 | 258 | 326 | 11 | -0.3804 | -0.0814 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |


## Why the raw replacement ratio is not the headline

A raw pre-versus-post comparison credits ordinary trade growth to the tariff. Over this window that inflates apparent third-country expansion and can push the replacement ratio above one when nothing was replaced. The counterfactual-adjusted table below nets out the growth of never-treated products, country by country, and is the figure to read.

## Counterfactual-adjusted decomposition

**by partner**

| country_code | pre_monthly_value | post_monthly_value | counterfactual_post_value | excess_change | control_growth_factor | is_treated_country | excess_pct_vs_counterfactual | run_id | git_commit | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5800 | 361,910,551.8321 | 422,637,419.3346 | 321,447,485.3234 | 101,189,934.0112 | 0.8882 | no | 0.3148 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5330 | 125,741,336.6441 | 140,502,196.3066 | 132,216,047.6557 | 8,286,148.6509 | 1.0515 | no | 0.0627 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5590 | 53,561,139.5890 | 48,181,033.9914 | 51,847,245.0248 | -3,666,211.0333 | 0.9680 | no | -0.0707 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5520 | 196,266,737.6667 | 236,472,684.6785 | 248,119,279.6307 | -11,646,594.9523 | 1.2642 | no | -0.0469 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5880 | 483,572,281.6613 | 480,596,093.0670 | 519,248,640.8442 | -38,652,547.7771 | 1.0738 | no | -0.0744 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 1220 | 1,263,355,847.1993 | 1,191,412,017.9420 | 1,288,747,745.7163 | -97,335,727.7743 | 1.0201 | no | -0.0755 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5490 | 284,836,755.0182 | 217,673,982.0903 | 329,382,089.1988 | -111,708,107.1084 | 1.1564 | no | -0.3391 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 2010 | 3,413,997,048.8136 | 3,316,640,764.5979 | 3,675,477,830.0055 | -358,837,065.4076 | 1.0766 | no | -0.0976 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5700 | 4,170,431,011.1524 | 2,584,052,405.0264 | 4,374,255,147.1734 | -1,790,202,742.1471 | 1.0489 | yes | -0.4093 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |


## Partner-country detail

**countries**

| country_code | pre_monthly_value | post_monthly_value | change | pct_change | is_treated_country | pre_share | post_share | share_change | run_id | git_commit | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5800 | 361,910,551.8321 | 422,637,419.3346 | 60,726,867.5025 | 0.1678 | no | 0.0350 | 0.0489 | 0.0140 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5520 | 196,266,737.6667 | 236,472,684.6785 | 40,205,947.0118 | 0.2049 | no | 0.0190 | 0.0274 | 0.0084 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5330 | 125,741,336.6441 | 140,502,196.3066 | 14,760,859.6625 | 0.1174 | no | 0.0121 | 0.0163 | 0.0041 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5880 | 483,572,281.6613 | 480,596,093.0670 | -2,976,188.5943 | -0.0062 | no | 0.0467 | 0.0556 | 0.0089 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5590 | 53,561,139.5890 | 48,181,033.9914 | -5,380,105.5975 | -0.1004 | no | 0.0052 | 0.0056 | 0.0004 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5490 | 284,836,755.0182 | 217,673,982.0903 | -67,162,772.9278 | -0.2358 | no | 0.0275 | 0.0252 | -0.0023 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 1220 | 1,263,355,847.1993 | 1,191,412,017.9420 | -71,943,829.2573 | -0.0569 | no | 0.1220 | 0.1379 | 0.0159 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 2010 | 3,413,997,048.8136 | 3,316,640,764.5979 | -97,356,284.2157 | -0.0285 | no | 0.3297 | 0.3840 | 0.0542 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| 5700 | 4,170,431,011.1524 | 2,584,052,405.0264 | -1,586,378,606.1260 | -0.3804 | yes | 0.4028 | 0.2991 | -0.1037 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |


## Heterogeneity by pre-treatment dependence

**groups**

| dependence_group | n_products | treated_change | alternative_change | pre_treated_value | median_replacement_ratio | treated_pct_change | run_id | git_commit | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| low_dependence | 1049 | -1,275,141,226.0129 | 48,970,027.6725 | 4,553,534,825.3869 | 0.9156 | -0.2800 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |
| high_dependence | 1033 | -3,532,382,464.2088 | -420,922,937.4448 | 10,105,570,652.6263 | 0.3486 | -0.3495 | 20260809T194010Z-597ee5ff | c53443d-dirty | OFFICIAL | 2017-01..2019-08 |


## Interpretation limits

- The RAW pre-versus-post decomposition attributes ordinary trade growth to the tariff and its replacement ratio is not interpretable on its own. Use the counterfactual-adjusted figures.
- An increase in imports from a third country is not evidence of production relocation. Rerouting of treated-origin goods, transshipment, and origin misdeclaration produce the same pattern in customs data.
- The replacement ratio compares value flows only. It says nothing about whether the replacing goods are the same quality or the same variety.
- Domestic substitution is invisible in import data. A fall in imports that is not matched by third-country gains may reflect domestic production, lower final demand, or inventory drawdown, and these cannot be separated without domestic output data.
- The supplier set is the configured comparison group, not the world. Concentration measures are within-sample.

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
