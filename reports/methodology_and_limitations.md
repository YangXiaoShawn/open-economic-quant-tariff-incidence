# Methodology and Limitations

> **DATA PROVENANCE: OFFICIAL SOURCES**
>
> All figures below derive from official statistical or legal sources.
>
> run_id `20260809T194259Z-597ee5ff` · git `c53443d-dirty` · config `sample_slice.yaml` (sha256 `597ee5ffe47a`) · data period 2017-01 to 2019-08 · generated 2026-08-09T19:42:59.887758+00:00


What this design can and cannot support.

## Specification register

Every specification estimated in this run, with its estimand and identifying assumption. Fixed effects were chosen to match the estimand: product-time effects are excluded from level specifications precisely because they would absorb the product-level tariff shock being measured.

**specifications**

| specification | outcome | estimator | treatment_definition | fixed_effects | cluster_vars | sample | weighting | aggregation_level | estimand | identifying_assumption | rung | reference_period | run_id | git_commit | config | data_provenance | data_period |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| twfe_log_customs_unit_value_on_additional_tariff_rate | log_customs_unit_value | OLS-HDFE | additional_tariff_rate | flow_id + month_key | hs6 | non-missing, finite outcome | unweighted | hs6 x country x month | average effect of the additional duty on the outcome | conditional on the absorbed effects, treated and untreated flows would have followed parallel paths | 2_twfe |  | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| twfe_log_landed_unit_value_on_additional_tariff_rate | log_landed_unit_value | OLS-HDFE | additional_tariff_rate | flow_id + month_key | hs6 | non-missing, finite outcome | unweighted | hs6 x country x month | average effect of the additional duty on the outcome | conditional on the absorbed effects, treated and untreated flows would have followed parallel paths | 2_twfe |  | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| twfe_log_quantity_on_additional_tariff_rate | log_quantity | OLS-HDFE | additional_tariff_rate | flow_id + month_key | hs6 | non-missing, finite outcome | unweighted | hs6 x country x month | average effect of the additional duty on the outcome | conditional on the absorbed effects, treated and untreated flows would have followed parallel paths | 2_twfe |  | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| twfe_log_customs_value_on_additional_tariff_rate | log_customs_value | OLS-HDFE | additional_tariff_rate | flow_id + month_key | hs6 | non-missing, finite outcome | unweighted | hs6 x country x month | average effect of the additional duty on the outcome | conditional on the absorbed effects, treated and untreated flows would have followed parallel paths | 2_twfe |  | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| event_study_log_customs_unit_value_ols | log_customs_unit_value | OLS-HDFE | event-time indicators interacted with is_treated_country; reference period -3 | flow_id + month_key | hs6 | event window [-12, 10] with binned endpoints | unweighted | hs6 x country x month | dynamic effect of the tariff action relative to the reference month | parallel trends absent treatment, no anticipation before the window | 3_event_study | -3 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| event_study_log_customs_unit_value_ols | log_customs_unit_value | OLS-HDFE | event-time indicators interacted with is_treated_country; reference period -1 | flow_id + month_key | hs6 | event window [-12, 10] with binned endpoints | unweighted | hs6 x country x month | dynamic effect of the tariff action relative to the reference month | parallel trends absent treatment, no anticipation before the window | 3_event_study | -1 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| event_study_log_landed_unit_value_ols | log_landed_unit_value | OLS-HDFE | event-time indicators interacted with is_treated_country; reference period -3 | flow_id + month_key | hs6 | event window [-12, 10] with binned endpoints | unweighted | hs6 x country x month | dynamic effect of the tariff action relative to the reference month | parallel trends absent treatment, no anticipation before the window | 3_event_study | -3 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| event_study_log_landed_unit_value_ols | log_landed_unit_value | OLS-HDFE | event-time indicators interacted with is_treated_country; reference period -1 | flow_id + month_key | hs6 | event window [-12, 10] with binned endpoints | unweighted | hs6 x country x month | dynamic effect of the tariff action relative to the reference month | parallel trends absent treatment, no anticipation before the window | 3_event_study | -1 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| event_study_log_quantity_ols | log_quantity | OLS-HDFE | event-time indicators interacted with is_treated_country; reference period -3 | flow_id + month_key | hs6 | event window [-12, 10] with binned endpoints | unweighted | hs6 x country x month | dynamic effect of the tariff action relative to the reference month | parallel trends absent treatment, no anticipation before the window | 3_event_study | -3 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| event_study_log_quantity_ols | log_quantity | OLS-HDFE | event-time indicators interacted with is_treated_country; reference period -1 | flow_id + month_key | hs6 | event window [-12, 10] with binned endpoints | unweighted | hs6 x country x month | dynamic effect of the tariff action relative to the reference month | parallel trends absent treatment, no anticipation before the window | 3_event_study | -1 | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| ppml_customs_value_on_log1p_additional_tariff | customs_value | PPML-HDFE | log1p_additional_tariff | flow_id + month_key | hs6 | full sample | PPML (implicit) | hs6 x country x month | semi-elasticity of the trade flow in levels with respect to the tariff term | correct conditional mean given the absorbed effects; tariff variation is conditionally exogenous | 5_ppml |  | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| ppml_quantity_on_log1p_additional_tariff | quantity | PPML-HDFE | log1p_additional_tariff | flow_id + month_key | hs6 | full sample | PPML (implicit) | hs6 x country x month | semi-elasticity of the trade flow in levels with respect to the tariff term | correct conditional mean given the absorbed effects; tariff variation is conditionally exogenous | 5_ppml |  | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| ppml_customs_value_on_log1p_total_tariff | customs_value | PPML-HDFE | log1p_total_tariff | flow_id + month_key | hs6 | subsample with an ad valorem MFN baseline | PPML (implicit) | hs6 x country x month | semi-elasticity of the trade flow in levels with respect to the tariff term | correct conditional mean given the absorbed effects; tariff variation is conditionally exogenous | 5_ppml |  | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |
| ppml_quantity_on_log1p_total_tariff | quantity | PPML-HDFE | log1p_total_tariff | flow_id + month_key | hs6 | subsample with an ad valorem MFN baseline | PPML (implicit) | hs6 x country x month | semi-elasticity of the trade flow in levels with respect to the tariff term | correct conditional mean given the absorbed effects; tariff variation is conditionally exogenous | 5_ppml |  | 20260809T194150Z-597ee5ff | c53443d-dirty | sample_slice.yaml | OFFICIAL | 2017-01..2019-08 |


## Known limitations recorded on each dataset

**limitations**

| dataset | layer | limitation |
| --- | --- | --- |
| industry_tariff_exposure | results | BEA summary commodities are far broader than HS6 lines. A summary commodity that contains both tariffed and untariffed HS6 products receives an import-weighted average rate, so industry-level exposure is attenuated relative to the true product-level shock, and heterogeneity within a commodity is lost entirely. |
| industry_tariff_exposure | results | HS-to-commodity concordance status: COARSE_APPROXIMATION. Exposure magnitudes are an ordering, not elasticities, and must not feed a welfare calculation. |
| industry_tariff_exposure | results | Direct requirements are normalised by the intermediate-input column total, not by total industry output including value added, so shares are input shares of intermediate purchases. |
| tariff_schedule_section301_china | normalized | LIST_4A_NOT_PARSED: List 4A (84 FR 43304, effective 1 Sep 2019 at 15%, reduced to 7.5% on 14 Feb 2020 by 85 FR 3741) enumerates 10-digit statistical lines under a different annex construction and is not yet parsed. Products treated only by List 4A are therefore absent from the treatment schedule and would be misclassified as untreated. The vertical-slice sample is restricted to chapters where Lists 1-3 are the binding action, and the control group is screened against a List 4A chapter blacklist. |
| tariff_schedule_section301_china | normalized | EXCLUSIONS_NOT_PARSED: USTR granted thousands of product exclusions in a long series of notices (e.g. 84 FR 38717, 84 FR 61674, 85 FR 6674). Most are written as narrative product descriptions under new 9903.88.xx headings rather than as clean HTS8 lists, so they cannot be mapped to statistical lines mechanically. The tariff engine fully supports exclusion records; the schedule currently carries none from this source. |
| trade_panel_hs6_country_month | analytical | Customs unit values are value/quantity over heterogeneous transactions; they are not transaction prices and move with product mix and quality. |
| trade_panel_hs6_country_month | analytical | HS6 aggregation loses the HS8 level at which Section 301 lists are written; partially covered headings are excluded from both treatment groups. |
| trade_panel_hs6_country_month | analytical | Sample ends 2019-08 to avoid List 4A contamination of the control group. |


## Measurement cautions carried throughout

- Customs unit values are value divided by quantity over a heterogeneous bundle within an HS line, country and month. They move with product mix, quality and unit-of-measure changes as well as with prices, and are never called transaction prices in this project.
- Customs value excludes freight and insurance; import charges are carried as a separate column and the CIF and duty-inclusive concepts are built explicitly rather than assumed.
- Section 301 lists are legislated at 8 digits. An HS6 panel therefore has headings that are only partly covered; those are excluded from both treatment groups rather than assigned a coverage-weighted rate, and the count of excluded headings is reported.
- A duty effective mid-month applies to part of that month. The panel carries a day-weighted average statutory rate, plus month-start and month-end variants, so the event-time-zero coefficient is not an artefact of a timing convention.
- The USITC HTS endpoint serves the current tariff schedule, not the 2018 vintage. Baseline MFN rates and HS6-to-HS8 child maps therefore come from a later vintage than the Section 301 lists.
- An HS6 heading containing any compound or specific duty line has no single ad valorem baseline. Those rows carry a null total rate rather than a zero, and drop out of total-rate specifications.

## Identification threats not resolved by this design

- **Policy endogeneity.** Product lists were chosen partly on expected domestic impact, so treatment is not random across products.
- **Anticipation and front-running.** Effective dates were publicly known in advance. Shipments pulled forward contaminate event month −1, which is why two reference periods are reported.
- **Concurrent policy.** Section 232 steel and aluminium actions, and retaliation by trading partners, overlap this window.
- **Exchange rates.** RMB depreciation over 2018-2019 moves customs unit values in the same direction as exporter absorption and is not separated here.
- **Transshipment and origin misdeclaration.** Third-country increases in customs data cannot be distinguished from relocation of production.
- **Product reclassification.** Firms have an incentive to reclassify into untreated lines, which appears as treated-product exit plus control-product entry.
- **Exclusions are not in the schedule.** Estimates are intention-to-treat with respect to the statutory list, not treatment-on-the-treated.

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
