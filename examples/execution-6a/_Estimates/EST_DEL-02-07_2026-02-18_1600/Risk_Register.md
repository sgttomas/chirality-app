# Risk Register — EST_DEL-02-07_2026-02-18_1600

## Identified Risks

### RISK-001: Generator System Cost Exceeds Allowance

| Field | Value |
|---|---|
| **Likelihood** | MEDIUM |
| **Impact** | MEDIUM |
| **Description** | The $150,000 generator system allowance (EQ-04 recommended) is based on parametric data with a $120k-$180k range. Actual vendor quotes may exceed $180k if: (a) runtime exceeds 72 hours, (b) essential loads are larger than assumed, (c) site-specific conditions require premium solutions, or (d) market pricing has shifted. |
| **Trigger** | Vendor quote received above $180,000 |
| **Mitigation** | Obtain competitive vendor quotes early; confirm essential loads list; confirm runtime before procurement. |
| **Related Assumptions** | ASM-001, ASM-002 |

### RISK-002: Scope Creep on Essential Loads List

| Field | Value |
|---|---|
| **Likelihood** | MEDIUM |
| **Impact** | MEDIUM |
| **Description** | The current essential loads list (kitchen, meeting room, 2 bathrooms, emergency lighting, door backups) is the stated minimum. During design, additional loads may be added (e.g., IT/server rooms, additional bathrooms, HVAC for occupied spaces), requiring a larger generator. |
| **Trigger** | Essential loads analysis exceeds 150 kW |
| **Mitigation** | Lock essential loads list with Owner before generator procurement; size with modest margin. |
| **Related Assumptions** | ASM-002, ASM-005 |

### RISK-003: Double-Counting with Adjacent Deliverables

| Field | Value |
|---|---|
| **Likelihood** | LOW-MEDIUM |
| **Impact** | LOW |
| **Description** | Potential overlap between: (a) EQ-04 system price and L-0207-020/L-0207-040 (distribution and installation), and (b) L-0207-050 design fees and DEL-02-06 electrical engineering fees. |
| **Trigger** | Vendor quote scope overlaps with estimate line items |
| **Mitigation** | Clear scope boundary documentation (DEC-EST-003, DEC-EST-005, DEC-EST-006); reconcile when vendor quotes are received. |
| **Related Decisions** | DEC-EST-002, DEC-EST-003, DEC-EST-005 |

### RISK-004: Seismic Anchorage Requirement

| Field | Value |
|---|---|
| **Likelihood** | MEDIUM |
| **Impact** | LOW |
| **Description** | AHJ may require seismic anchorage for generator installation. If required, estimated additional cost of $3,000-$8,000 is not included in the current estimate. |
| **Trigger** | AHJ ruling requires seismic anchorage |
| **Mitigation** | Obtain AHJ ruling early; carry contingency for anchorage if uncertain. |
| **Related Blockers** | BLOCKER-2 (DEP-0207-E009) |
