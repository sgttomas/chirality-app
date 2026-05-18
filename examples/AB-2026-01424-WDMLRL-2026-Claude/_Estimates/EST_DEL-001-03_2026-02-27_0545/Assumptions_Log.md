# Assumptions Log — EST_DEL-001-03_2026-02-27_0545

| ASM-ID | Assumption | Impact | Confidence | Source |
|---|---|---|---|---|
| ASM-001 | Hourly rates in Professional_Staff_Rates.csv are applicable to this project without adjustment | Rates directly determine all line item amounts; if actual rates differ, total will change proportionally | MEDIUM | Professional_Staff_Rates.csv — all rates tagged "PARAMETRIC, MEDIUM" |
| ASM-002 | Level of effort allocations in Level_of_Effort.csv are appropriate for the Exterior Elevations deliverable | Hours directly determine all line item amounts; LOE uses same allocation for all PKG-001 Drawing Set deliverables (54h Sr. Arch, 42h Arch, 24h BIM, 6h PM, 4h CE) | MEDIUM | Level_of_Effort.csv rows 12-16 — all tagged "PARAMETRIC" |
| ASM-003 | The parametric hour allocation for a Drawing Set deliverable type is a reasonable proxy for the specific effort required for Exterior Elevations | Exterior Elevations may require more or fewer hours than an average Drawing Set depending on complexity (number of faces, coordination intensity with MEP, interface with existing building) | MEDIUM | Implicit in LOE data — all PKG-001 Drawing Set deliverables share identical allocations |
| ASM-004 | Currency is CAD as specified in INIT-TASK brief and confirmed by Assumed_Project_Parameters.csv (PP-17) | All amounts denominated in CAD | HIGH | INIT-TASK brief; PP-17 |
| ASM-005 | No subconsultant markup, overhead, or profit margins are included | Estimate reflects direct staff effort at blended hourly rates only | MEDIUM | Rates in Professional_Staff_Rates.csv do not indicate whether they are loaded or bare rates |
| ASM-006 | The scope of this estimate is limited to design production effort; no construction material, equipment, or installation costs are included | Design-only scope is consistent with the deliverable type (Drawing Set) and the pricing sources available | HIGH | Deliverable type = Drawing Set; LOE data covers design roles only |
