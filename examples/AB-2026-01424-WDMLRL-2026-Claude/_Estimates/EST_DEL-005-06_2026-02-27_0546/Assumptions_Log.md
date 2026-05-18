# Assumptions Log — EST_DEL-005-06_2026-02-27_0546

## ASM-001 — Parametric Hours Represent Full Scope

- **Assumption:** The 90 total hours allocated in Level_of_Effort.csv for DEL-005-06 (6 PM + 4 Cost Estimator + 24 BIM Technician + 56 Civil Engineer) are sufficient to cover all 9 Procedure steps (plus Step 4A), all 14 Specification requirements, and all 10 Datasheet calculation topics.
- **Basis:** Level_of_Effort.csv row notes indicate "PKG-005 Civil Engineer — Calculation Package" for all four role allocations. The source data is parametric with MEDIUM confidence.
- **Risk if wrong:** If the actual scope of work requires more hours (e.g., adverse geotechnical conditions requiring extensive slope stability analysis, or complex stormwater management approach), the estimate will understate cost.

## ASM-002 — No Rework Contingency Included

- **Assumption:** The estimated hours do not include contingency for rework arising from County rejection at Step 8 (Preliminary Submission to County for Approval). Procedure Step 8.4 defines a rework path if the County rejects the preliminary design.
- **Basis:** The parametric model in Level_of_Effort.csv does not distinguish between first-pass and rework hours. If rework occurs, additional hours will be required.
- **Risk if wrong:** A County rejection requiring fundamental redesign could add 20-40% to the Civil Engineer and BIM Technician hours.

## ASM-003 — Hourly Rates Are Current for 2026

- **Assumption:** The hourly rates in Professional_Staff_Rates.csv are applicable for the 2026 project year (Base Year = 2026 per PP-18).
- **Basis:** Assumed_Project_Parameters.csv PP-18 defines base year as 2026. No escalation factor is applied.
- **Risk if wrong:** If rates increase during the project, actual costs will exceed the estimate. MEDIUM confidence rates have +/-20-30% accuracy per the INDEX.md data quality statement.

## ASM-004 — Single Calculation Pass (No Iterative Refinement)

- **Assumption:** The calculation package is produced in a single pass through the Procedure steps, with one County submission and approval cycle.
- **Basis:** The Procedure defines a linear workflow (Steps 1-9). Iterative refinement loops are not explicitly allocated in the parametric hours.
- **Risk if wrong:** Design iteration (e.g., changes driven by evolving stormwater management approach, updated geotechnical data, or design storm return period changes) could increase effort.

## ASM-005 — Labour Only (No Direct Costs)

- **Assumption:** The Civil Calculation Package is a professional services deliverable requiring only labour costs. No material, equipment, software licensing, travel, or other direct costs are included.
- **Basis:** The deliverable type is "Calculation Package" — an engineering analysis document. All costs are professional staff hours. Site visit costs (Step 1.3 — mandatory site meeting) are assumed covered within the PM and Civil Engineer hourly allocations.
- **Risk if wrong:** If specialized software (e.g., hydraulic modeling software licenses) or additional site visits are required, those costs are not captured.

## ASM-006 — Currency Is CAD

- **Assumption:** All costs are in Canadian Dollars (CAD) with no currency conversion required.
- **Basis:** PP-17 in Assumed_Project_Parameters.csv confirms CAD. Project is located in Alberta, Canada. All professional staff rates are denominated in CAD.
- **Risk if wrong:** Negligible. The project is entirely domestic.
