# Technical Report

> **DATA PROVENANCE: OFFICIAL SOURCES**
>
> All figures below derive from official statistical or legal sources.
>
> run_id `20260809T194259Z-597ee5ff` · git `c53443d-dirty` · config `sample_slice.yaml` (sha256 `597ee5ffe47a`) · data period 2017-01 to 2019-08 · generated 2026-08-09T19:42:59.887758+00:00


How the system is built and how each component is validated.

## Pipeline

```
Federal Register PDFs ──┐
USITC HTS (MFN, HS6→HS8)┼→ tariff schedule ──┐
                        │                    ├→ analytical panel ─┬→ incidence
Census imports (or the  ┘                    │                    ├→ diversion
synthetic generator) ────────────────────────┘                    └→ reports
BEA Supply-Use ───────────────────────────────→ industry exposure ─┘
```

## Datasets and manifests

**manifests**

| dataset | layer | rows | provenance | vintage | checksum |
| --- | --- | --- | --- | --- | --- |
| industry_tariff_exposure | results | 72 | OFFICIAL | BEA AllTablesSUP.zip, Summary level, year 2017 | e82714834368 |
| tariff_schedule_section301_china | normalized | 12587 | OFFICIAL | 83 FR 28710 (2018-13248); 83 FR 40823 (2018-17709); 83 FR 47974 (2018- | 76959e30c729 |
| trade_panel_hs6_country_month | analytical | 489733 | OFFICIAL | Census live API | 0433227a53e1 |


## Tariff-schedule parse validation

Each notice states how many tariff lines it covers. The parser is validated against that count rather than against an expectation supplied by the author.

**parses**

| document | chapter99_heading | full_lines | partial_lines | parsed_total | stated_in_notice | matches |
| --- | --- | --- | --- | --- | --- | --- |
| 2018-13248 | 9903.88.01 | 818 | 0 | 818 | 818 | yes |
| 2018-17709 | 9903.88.02 | 279 | 0 | 279 | 279 | yes |
| 2018-20610 | 9903.88.03 | 5734 | 11 | 5745 | 5745 | yes |
| 2019-09681 | 9903.88.03 | 5734 | 11 | 5745 | 5745 | yes |


## Codes truncated in the source rendering

Resolved only where the USITC HTS leaves exactly one candidate; marked DERIVED, never guessed.

**resolutions**

| document | truncated | resolved_to |
| --- | --- | --- |
| 2018-13248 | 9033.00 | 90330090 |


## Specifications estimated

**register**

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
