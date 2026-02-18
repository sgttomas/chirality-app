# Decision Log

## Run: EST_DEL-09-01_2026-02-18_1500

---

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-001 | CBS codes assigned based on Role Category from Professional_Staff_Rates.csv: Management -> CBS-MGMT, Construction -> CBS-CONST. | Deterministic mapping rule; no CBSHint present in decomposition for DEL-09-01. Documented in Run_Context.md. |
| DEC-EST-002 | All 3 LOE rows for DEL-09-01 used without modification. No rows added or removed. | Level_of_Effort.csv provides complete role/hour allocation for this deliverable. STRICT fallback policy means no additional lines invented. |
| DEC-EST-003 | Rounding applied at DOLLAR level to individual line items. | Per brief: ROUNDING=DOLLAR. All line items produce whole-dollar amounts naturally (integer hours x integer rates), so no rounding adjustment was needed. |
| DEC-EST-004 | Dependency register loaded from deliverable path (AUTO mode) but no blockers identified for production cost estimation. | Upstream prerequisites are reference documents needed for content production, not for estimating the cost of producing DEL-09-01. Document availability does not affect the hours-based cost model. |
| DEC-EST-005 | Quality Lead (R-23) hours attributed to SOW-027 QMP component per Level_of_Effort.csv notes. | LOE notes state "QMP component (SOW-027) embedded in this DEL in 6c." This confirms the dual-scope nature of the deliverable. |
