# Decision Log

**Snapshot:** EST_DEL-03-01_2026-02-18_2000

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-D-001 | CBS code assigned as `PROF-ARCH` (Professional - Architecture) | Deterministic mapping rule: `PROF-{discipline}` where discipline is derived from role category. R-04 (Architect, Project) maps to Architecture. Documented in Run_Context.md. |
| EST-D-002 | Level_of_Effort.csv used as the authoritative hour quantity source | Brief specifies "Use Level_of_Effort.csv for hours." File contains exactly 1 row for DEL-03-01: R-04 at 12 hours. No ambiguity. |
| EST-D-003 | Professional_Staff_Rates.csv used as the authoritative rate source | Brief specifies "Use Professional_Staff_Rates.csv for rates." R-04 rate = $145/hr CAD, MARKET basis, MEDIUM confidence. No ambiguity. |
| EST-D-004 | Assumed_Project_Parameters.csv not used for DEL-03-01 pricing | DEL-03-01 is a narrative deliverable priced on professional hours only. No area-based, quantity-based, or financial parameters apply. File indexed but not consumed for pricing. |
| EST-D-005 | `Method` set to RATE_TABLE (not PARAMETRIC) despite hours having PARAMETRIC basis | The pricing method is RATE_TABLE: hours x rate from a rate table. The fact that the hour quantity was derived parametrically by the Level_of_Effort author is metadata about the quantity source, not the estimate method. BASIS_OF_ESTIMATE=RATE_TABLE governs. |
| EST-D-006 | Scope limited to DEL-03-01 only (architectural sub-brief of SOW-0011) | Per brief: "SOW-0011 multi-mapping -- each DEL covers ONLY its discipline sub-brief, not the full Design Brief." No hours from other DEL-03-xx deliverables are included. |
| EST-D-007 | No fallback pricing applied | FALLBACK_POLICY=STRICT. All line items have rate table evidence. No TBD amounts. |
