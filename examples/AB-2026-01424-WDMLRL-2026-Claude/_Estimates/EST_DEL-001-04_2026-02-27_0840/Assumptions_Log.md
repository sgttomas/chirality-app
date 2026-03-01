# Assumptions Log — EST_DEL-001-04_2026-02-27_0840

| AssumptionID | Assumption | Impact | Source |
|---|---|---|---|
| ASM-001 | Hourly rates in Professional_Staff_Rates.csv are representative for a 2026 Alberta design-build project | Rates directly determine all line item amounts. If actual rates differ, totals scale proportionally. | Professional_Staff_Rates.csv (Confidence: MEDIUM) |
| ASM-002 | Level of effort for DEL-001-04 (6/4/54/42/24 hours) is adequate for producing Building Section drawings covering 5+ section cuts, preliminary and IFC stages | Underestimation would increase actual costs; overestimation would reduce them. The LOE is identical across all PKG-001 Drawing Set deliverables, which may not reflect the specific coordination complexity of Building Sections. | Level_of_Effort.csv (DEL-001-04 rows) |
| ASM-003 | Currency is CAD | All amounts denominated in Canadian dollars. | Assumed_Project_Parameters.csv (PP-17); INIT-TASK brief |
| ASM-004 | No subconsultant, material, software licensing, or plotting/reproduction costs are included | This estimate covers professional design labour only. Any non-labour costs for this deliverable are excluded. | Scope of PRICE_SOURCES (labour-only sources provided) |
| ASM-005 | The 5 roles identified in Level_of_Effort.csv are the complete staffing requirement for this deliverable | No additional roles (e.g., QA/QC Lead, Document Controller) are required beyond the 5 listed. | Level_of_Effort.csv — only 5 rows for DEL-001-04 |
