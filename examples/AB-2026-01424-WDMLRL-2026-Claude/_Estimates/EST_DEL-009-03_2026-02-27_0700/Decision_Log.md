# Decision_Log.md
## Estimate Decision Log — DEL-009-03 Safety Code Permits

---

| Decision ID | Decision | Rationale | Impact |
|-------------|----------|-----------|--------|
| DEC-009-03-01 | Use PARAMETRIC method for all lines | BASIS_OF_ESTIMATE=PARAMETRIC as specified in run brief. All pricing sources (Professional_Staff_Rates.csv, Level_of_Effort.csv) are PARAMETRIC basis. | All 11 lines use Method=PARAMETRIC. Consistent with brief. |
| DEC-009-03-02 | Price items ITM-009-03-03 through ITM-009-03-11 using assumed hours despite absence from LOE | FALLBACK_POLICY=ALLOW_PARAMETRIC permits pricing items without direct LOE backing. The Procedure document describes 5 phases with 15 steps requiring specialist effort. Leaving these as TBD would produce a misleading total ($1,530 vs. $12,995). | 9 lines priced at LOW confidence using R-22 and R-05 rates. Total estimate is more representative of actual effort but carries assumption risk. |
| DEC-009-03-03 | Assign R-22 (Permitting Specialist) as primary role for permit process activities | R-22 is described as "Permits, code process tracking" in Professional_Staff_Rates.csv, which directly matches the DEL-009-03 scope. R-01 (Project Manager) provides oversight but is not the primary worker for permit applications and coordination. | Rates of $125/hr applied to 9 specialty items. |
| DEC-009-03-04 | Assign R-05 (HSE Manager) to OH&S-related activities | The Prime Contractor Designation (ITM-009-03-05), inspection coordination (ITM-009-03-08), and OH&S pre-qualification (ITM-009-03-11) require safety management expertise beyond general permitting. R-05 at $140/hr is the appropriate role. | R-05 hours included in 3 line items alongside R-22 hours. |
| DEC-009-03-05 | Exclude permit fees from estimate | RFP Section 3.3.1 explicitly states permit fee costs are County's responsibility. Confirmed by Specification REQ-009-03-08. | No material or fee line items. Estimate is 100% professional services labour. |
| DEC-009-03-06 | Assume 6 Safety Code permit categories | Datasheet and Guidance identify anticipated categories (building, electrical, fire, gas, plumbing, elevator/crane) based on RFP Section 3.4 building systems. Exact count is TBD pending audit. 6 is used as the working assumption for hour estimates. | Affects hours assumed for application preparation, submission tracking, and inspection coordination. |
| DEC-009-03-07 | CBS categories set to LABOUR-MGMT and LABOUR-SPECIALTY | No material, equipment, or third-party fee costs apply. Management roles (R-01, R-08) classified as LABOUR-MGMT; specialty roles (R-05, R-22) classified as LABOUR-SPECIALTY. | Clear CBS breakdown in WBS_CBS_Matrix.csv. |
| DEC-009-03-08 | Use CAD as currency | Run brief specifies CURRENCY=CAD. All rates in Professional_Staff_Rates.csv are CAD. Confirmed by Assumed_Project_Parameters.csv PP-17. | All amounts in CAD. |
