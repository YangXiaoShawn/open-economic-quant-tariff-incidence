# Methodology and Limitations

> **DATA PROVENANCE: MIXED (OFFICIAL POLICY + SYNTHETIC TRADE FLOWS)**
>
> Tariff-policy and classification inputs are official. Trade flows come from the documented synthetic generator. **Estimates below measure whether the estimation code recovers a known ground truth. They are not evidence about the U.S. economy and must not be cited as empirical findings.**
>
> run_id `20260808T224044Z-55c15b82` · git `NO_COMMIT` · config `sample_slice.yaml` (sha256 `55c15b82b4e1`) · data period 2017-01 to 2019-08 · generated 2026-08-08T22:40:44.256222+00:00


What this design can and cannot support.

## Specification register

Every specification estimated in this run, with its estimand and identifying assumption. Fixed effects were chosen to match the estimand: product-time effects are excluded from level specifications precisely because they would absorb the product-level tariff shock being measured.

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
| trade_panel_hs6_country_month | analytical | TRADE FLOWS ARE SYNTHETIC. No estimate from this panel is an empirical finding about U.S. trade. Set CENSUS_API_KEY to rebuild with official data. |


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

- run id: `20260808T224044Z-55c15b82`
- git commit: `NO_COMMIT`
- configuration: `sample_slice.yaml` (sha256 `55c15b82b4e1bdd1697f82c0fa9dbcdb690a23b4c1ecae6ffd57dcdd3287f988`)
- data provenance: `MIXED`
- data period: 2017-01 to 2019-08
- generated: 2026-08-08T22:40:44.256222+00:00
- python 3.12.13 on macOS-26.6.1-arm64-arm-64bit

_This document is generated by `scripts/generate_reports.py`. Do not edit it by hand; edit the generator or the underlying result tables._
