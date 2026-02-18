# Blockers Report — EST_DEL-02-04_2026-02-18_1130

## Summary

| Metric | Value |
|---|---|
| Hard blockers preventing estimate | 0 |
| Soft blockers (information gaps reducing accuracy) | 5 |
| Dependencies identified in Dependencies.csv | 20 |
| Upstream prerequisites (EXECUTION class) | 6 |
| Downstream interfaces | 3 |
| Anchor/traceability entries | 9 |

## Soft Blockers (Information Gaps)

These are not hard blockers (the estimate was produced), but they represent information dependencies that will materially improve accuracy when resolved.

### BLK-01: Architectural Program Not Yet Confirmed
- **Dependency:** DEP-0204-E01 (DEL-02-01 prerequisite)
- **Impact:** Building dimensions, bay vs office area split, perimeter, and wall heights are all derived from PP-05 design-basis assumptions. Confirmation of the architectural program would validate or refine the quantity basis for CBS 03-CONCRETE, 05-STEEL, 07-ENVELOPE, 08-OPENINGS, and 09-FLOORING.
- **Estimated Cost Sensitivity:** +/- 15-20% of total estimate ($260k-$345k range impact)
- **Resolution:** Confirm preliminary floor plan concept from DEL-02-01.

### BLK-02: Bay Layout Not Yet Confirmed
- **Dependency:** DEP-0204-E02, DEP-0204-E03 (DEL-02-02 and DEL-02-03 prerequisites)
- **Impact:** Bay dimensions, column grid spacing, and overhead door locations affect structural framing quantities and foundation layout. Current assumption is 8 bays at ~1,500 sf each.
- **Estimated Cost Sensitivity:** +/- 10% of structural and foundation costs ($83k range impact)
- **Resolution:** Confirm bay layouts from DEL-02-02 (Firehall) and DEL-02-03 (Public Works).

### BLK-03: Geotechnical Report Not Reviewed
- **Dependency:** DEP-0204-E05 (Geotechnical Investigation Report)
- **Impact:** Foundation type selection (screw piles assumed per DEC-01) depends on soil conditions confirmed in the geotechnical report. Actual foundation costs could differ significantly if soil conditions require a different system.
- **Estimated Cost Sensitivity:** +/- 15-20% of CBS 03-CONCRETE ($55k-$74k range impact)
- **Resolution:** DB structural engineer to review Geotechnical Report (RFP Appendix D).

### BLK-04: Alberta Building Code Edition and Load Tables
- **Dependency:** DEP-0204-E06 (Alberta Building Code constraint)
- **Impact:** Specific snow loads, wind loads, and seismic design category for Penhold, AB affect structural steel sizing and tonnage. Current steel intensity assumption (25 kg/m2) is typical but not site-verified.
- **Estimated Cost Sensitivity:** +/- 10% of CBS 05-STEEL ($46k range impact)
- **Resolution:** DB structural engineer to confirm applicable code edition and load tables for Penhold, AB.

### BLK-05: Overhead Door Count (Drive-Through Configuration)
- **Dependency:** DEP-0204-E02, DEP-0204-E03 (bay layout prerequisites)
- **Impact:** PP-13 states 8 overhead doors total. If the design uses drive-through bays (doors on both ends), the actual count could be 16. This would double the overhead door cost (+$160,000).
- **Estimated Cost Sensitivity:** Potential +$160,000 if drive-through configuration confirmed with 2 doors per bay
- **Resolution:** Confirm bay configuration and overhead door count with DEL-02-02 and DEL-02-03 bay layouts.
