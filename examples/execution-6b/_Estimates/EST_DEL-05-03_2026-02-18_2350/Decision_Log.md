# Decision Log -- EST_DEL-05-03_2026-02-18_2350

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS assigned as PROFESSIONAL_SERVICES.MECHANICAL_ENGINEERING | DEL-05-03 is a T2 Narrative deliverable; the sole cost driver is professional staff hours (R-11, Mechanical Engineer Senior). No construction materials, equipment procurement, or subcontractor costs. CBS reflects the discipline of the primary role. |
| EST-DEC-002 | Single line item used (no sub-task breakdown) | Level_of_Effort.csv assigns a single role (R-11, 8 hours) to DEL-05-03. There is no basis in the pricing sources to split this into sub-tasks (e.g., HVAC maintainability vs. plumbing maintainability vs. fire protection maintainability). A single consolidated line item is the most honest representation of the source data. |
| EST-DEC-003 | Assumed_Project_Parameters.csv listed as informational context only | DEL-05-03 is a narrative deliverable priced by professional hours, not by construction parameters (sf, equipment counts). Project parameters do not directly drive the cost of this deliverable. |
| EST-DEC-004 | No fallback applied | FALLBACK_POLICY = STRICT; all required pricing inputs (rate + hours) are available from the two primary sources. No TBD amounts needed. |
| EST-DEC-005 | Rounding had no effect | 8 hours x $160/hr = $1,280 CAD -- already a whole dollar amount. No rounding adjustment required. |
