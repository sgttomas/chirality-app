# Assumptions_Log.md
## Estimate Assumptions Log — DEL-009-04

**RunID:** EST_DEL-009-04_2026-02-27_0730

---

| Assumption ID | Assumption | Basis | Impact if Wrong | Confidence |
|---|---|---|---|---|
| ASM-001 | The 10 total LOE hours (6h PM + 4h CE) from Level_of_Effort.csv can be allocated across Phase 1 and Phase 2 setup activities based on professional judgment of relative effort per step | Level_of_Effort.csv provides only aggregate role hours per deliverable without step-level breakdown | Individual line amounts (DL-001 through DL-008) would shift, but total remains $1,530 | MEDIUM |
| ASM-002 | The LOE source hours cover register framework design and initial setup only (Phases 1-2), not ongoing construction-phase operation (Phase 3+) | LOE.csv Notes column reads "PKG-009 Project Manager -- TBD," suggesting the effort estimate is preliminary; 10h is consistent with template/schema design work, not months of operational activity | If LOE is intended to cover full lifecycle, the estimate is correctly priced but the scope allocation in DL-001 through DL-008 may need revision | MEDIUM |
| ASM-003 | Currency is CAD throughout | Assumed_Project_Parameters.csv PP-17 confirms CAD; Alberta project context | Negligible — all sources use CAD | HIGH |
| ASM-004 | Professional staff hourly rates in Professional_Staff_Rates.csv are applicable without escalation or overhead multiplier | Rates are stated as PARAMETRIC with MEDIUM confidence; no escalation factor or overhead/profit markup is included in the source | Actual costs may differ; rates may need burden/overhead loading for a complete cost picture | MEDIUM |
| ASM-005 | Permit fees are excluded from this estimate per RFP §3.3.1 (County responsibility) | RFP §3.3.1 explicitly states permit fees paid by County; Datasheet confirms | No impact — this is a confirmed exclusion, not an assumption risk | HIGH |
| ASM-006 | The register is a professional-services deliverable with no material, equipment, or subcontractor costs | Deliverable type is Register/Log per _CONTEXT.md; all Procedure steps are administrative/management activities | If register requires specialized software licensing or external consulting, those costs are missing | MEDIUM |
| ASM-007 | Construction-phase inspection coordination, deficiency tracking, and guarantee-period register maintenance effort will be quantifiable once permits are issued and the inspection schedule is known | Logical: permit conditions drive inspection count, which drives coordination hours | If permits are delayed or conditions are unusually numerous, operational effort could be material | MEDIUM |
