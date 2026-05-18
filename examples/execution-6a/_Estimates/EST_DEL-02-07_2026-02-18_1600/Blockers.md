# Blockers Report — EST_DEL-02-07_2026-02-18_1600

## Summary

| Metric | Count |
|---|---|
| **Total dependencies examined** | 13 |
| **Blockers (PENDING external confirmations)** | 2 |
| **Upstream prerequisites (TBD satisfaction)** | 5 |
| **Downstream handovers** | 1 |
| **Anchor/traceability records** | 4 |

## Critical Blockers

### BLOCKER-1: Owner Confirmation of 72-Hour Runtime (DEP-0207-E006)

| Field | Value |
|---|---|
| **DependencyID** | DEP-0207-E006 |
| **Type** | CONSTRAINT (External) |
| **Target** | Owner (Town of Penhold) |
| **Status** | PENDING |
| **Impact** | Generator sizing, fuel tank capacity, and fuel storage costs all depend on confirmed runtime. PP-26 assumes 72 hours but Owner has not confirmed. |
| **Estimate Impact** | If runtime increases beyond 72 hours, generator system cost (EQ-04 range $120k-$180k) may exceed the $150k recommended price. Fuel tank sizing is directly proportional. |
| **Action Required** | Owner must confirm runtime requirement before generator procurement. |

### BLOCKER-2: AHJ Ruling on Seismic Anchorage (DEP-0207-E009)

| Field | Value |
|---|---|
| **DependencyID** | DEP-0207-E009 |
| **Type** | CONSTRAINT (External) |
| **Target** | AHJ (Authority Having Jurisdiction) |
| **Status** | PENDING |
| **Impact** | If seismic anchorage is required, generator pad design and installation costs may increase. Not currently priced. |
| **Estimate Impact** | Potential cost addition of $3,000-$8,000 for seismic anchorage hardware and engineering (not included in current estimate). |
| **Action Required** | Responsible engineer to confirm with AHJ whether seismic anchorage is required or exempted. |

## Upstream Prerequisites (TBD Satisfaction — Not Blocking but Monitoring)

| DependencyID | Target | What is Needed | Status | Estimate Impact |
|---|---|---|---|---|
| DEP-0207-E001 | DEL-02-04 (Envelope/Doors) | Overhead door specification (size, operator type, count) | TBD | Needed for door backup mechanism design; count assumed at 8 doors per PP-13. |
| DEP-0207-E002 | DEL-02-06 (Electrical) | General electrical distribution concept | TBD | Needed for ATS placement and essential loads panel integration. Interface risk. |
| DEP-0207-E003 | DEL-03-01 (Site Plan) | Site layout for generator pad location | TBD | May affect pad costs if location requires additional civil work. |
| DEP-0207-E004 | DEL-03-04 (Site Utilities) | Site electrical service and generator connection point | TBD | Generator must connect to building electrical service; routing TBD. |
| DEP-0207-E005 | DEL-02-05 (Mechanical) | Generator exhaust routing coordination | TBD | Exhaust routing design needed for generator siting; may affect pad location. |
| DEP-0207-E007 | DEL-01-04 (Permitting) | Permits for generator installation, fuel storage, electrical | TBD | Construction-phase prerequisite; does not affect estimate pricing. |
