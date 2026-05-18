# Assumptions Log -- DEL-03-06

**RunID:** EST_DEL-03-06_2026-02-18_2330

---

| AssumptionID | Assumption | Source | Impact |
|---|---|---|---|
| EST-ASM-001 | Architect (Project) rate of $145/hr CAD is applicable to DEL-03-06 scope | Professional_Staff_Rates.csv, R-04, Basis=MARKET, Confidence=MEDIUM | Rate directly determines total amount. If actual rate differs, amount scales linearly. |
| EST-ASM-002 | 8 hours is sufficient for both the accessibility narrative (SOW-0015) and the adaptability narrative (SOW-0014) including cross-discipline coordination | Level_of_Effort.csv, DEL-03-06 row, Basis=PARAMETRIC | If coordination with structural/mechanical engineers requires more time than assumed, hours may increase. The BOE Context states this covers "Architect hours (coordinating structural/mechanical input)." |
| EST-ASM-003 | No separate hours are needed for Structural Engineer or Mechanical Engineer input to DEL-03-06 | Level_of_Effort.csv (no R-09, R-11 rows for DEL-03-06) | Coordination effort from structural/mechanical engineers is assumed to be captured in their own deliverable hours (DEL-03-03, DEL-03-04). If DEL-03-06 requires dedicated structural/mechanical authoring time, hours would increase. |
| EST-ASM-004 | The accessibility scope (Alberta Building Code) does not require a separate accessibility consultant | Level_of_Effort.csv (no specialty consultant row for DEL-03-06) | If a specialized accessibility consultant is needed, an additional role and hours would be required. |
