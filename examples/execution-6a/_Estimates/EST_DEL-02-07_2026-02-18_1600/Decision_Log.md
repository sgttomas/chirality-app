# Decision Log — EST_DEL-02-07_2026-02-18_1600

## Decisions Made During This Run

### DEC-EST-001: Fallback from QUOTE to ALLOWANCE

| Field | Value |
|---|---|
| **Decision** | All line items priced using ALLOWANCE method instead of QUOTE |
| **Reason** | BASIS_OF_ESTIMATE=QUOTE but no vendor quote exists for DEL-02-07 scope. FALLBACK_POLICY=ALLOW_ALLOWANCE permits fallback. ALLOW_MIXED_METHODS=TRUE permits method mixing. |
| **Affected Lines** | All (L-0207-010 through L-0207-050) |
| **Reversibility** | Replace with vendor quotes when available; current ALLOWANCE amounts become budget ceiling for quote comparison. |

### DEC-EST-002: EQ-04 Used as All-Inclusive System Price

| Field | Value |
|---|---|
| **Decision** | EQ-04 ($150,000 recommended) treated as the all-inclusive generator system price, including ATS (EQ-05). EQ-05 is not added separately. |
| **Reason** | EQ-04 notes state: "Includes: genset; ATS; distribution to essential loads; fuel tank (72-hr per assumption); concrete pad; exhaust system; sound attenuation; commissioning." EQ-05 notes state: "Included in EQ-04 system price; listed separately for reference if itemized." |
| **Affected Lines** | L-0207-010 |
| **Risk** | If EQ-04 is later itemized, ATS should not be double-counted. |

### DEC-EST-003: Emergency Distribution Estimated Separately

| Field | Value |
|---|---|
| **Decision** | Emergency power distribution from generator to essential loads (L-0207-020, $18,000) estimated as a separate line item from EQ-04. |
| **Reason** | Although EQ-04 notes include "distribution to essential loads," the brief's cost ownership rules state DEL-02-07 owns "distribution from generator to essential loads." A dedicated sub-panel and branch circuits to kitchen, meeting room, 2 bathrooms, and emergency lighting represent additional scope beyond the generator-side distribution included in EQ-04 (which covers ATS output to essential loads panel). This line captures the building-side distribution from the essential loads panel to the actual load points. |
| **Affected Lines** | L-0207-020 |
| **Risk** | Potential overlap with EQ-04 "distribution to essential loads." Conservative approach: include it; remove if vendor quote covers full distribution. |

### DEC-EST-004: Door Backup Mechanism Costed at $2,000/Door

| Field | Value |
|---|---|
| **Decision** | Overhead door backup power mechanism integration estimated at $2,000 per door x 8 doors = $16,000. |
| **Reason** | No specific pricing source for door backup mechanisms. Per brief, DEL-02-07 owns "overhead door BACKUP POWER mechanism integration" (not the doors themselves). Estimated as battery backup motor or UPS per door opener. Door count confirmed at 8 (PP-13). |
| **Affected Lines** | L-0207-030 |
| **Risk** | Mechanism type (battery backup unit vs generator-fed circuit) not yet determined. Actual cost could range $1,000-$3,500 per door depending on solution. |

### DEC-EST-005: Installation Labour Added as Incremental Scope

| Field | Value |
|---|---|
| **Decision** | Generator installation labour (L-0207-040, $12,000) added as a separate line despite EQ-04 including "commissioning." |
| **Reason** | EQ-04 system price likely assumes factory commissioning and standard installation. Site-specific installation labour (crane setting, electrical hookup, millwright alignment) is incremental. Labour rates from Construction_Labour_Rates.csv. |
| **Affected Lines** | L-0207-040 |
| **Risk** | If vendor quote includes full installation, this line should be removed to avoid double-counting. |

### DEC-EST-006: Scope Boundary Exclusions Applied

| Field | Value |
|---|---|
| **Decision** | The following items are explicitly EXCLUDED from this estimate per brief cost ownership rules: (1) Normal power distribution to generator transfer point (DEL-02-06); (2) Main electrical panels, feeders, branch circuits (DEL-02-06); (3) Generator pad site preparation/grading (DEL-03-02); (4) Generator fuel supply piping beyond tank (separate if applicable). |
| **Reason** | Brief states clear cost ownership boundaries. EQ-04 includes the concrete pad within its system price; DEL-03-02 owns site preparation/grading to the pad location. |
| **Affected Lines** | N/A (exclusions) |
| **Risk** | Interface gaps possible at pad preparation / grading handoff between DEL-02-07 and DEL-03-02. |
