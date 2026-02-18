# Decision Log

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-02-01_2026-02-04_1323 |
| **Deliverable** | DEL-02-01 ConceptDesignPackage |

---

## Decisions

### D-001: Currency Selection

| Property | Value |
|----------|-------|
| **Decision ID** | D-001 |
| **Decision** | Use CAD (Canadian Dollars) as estimate currency |
| **Trigger** | Currency specification required for estimate |
| **Evidence** | Task assignment explicitly specified "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | Foundational; all amounts in CAD |
| **Override Path** | Update _CONFIG.md with alternate currency |

---

### D-002: Pricing Method Selection

| Property | Value |
|----------|-------|
| **Decision ID** | D-002 |
| **Decision** | Use ALLOWANCE method for all line items |
| **Trigger** | No rate tables available in _RateTables/ directory; no vendor quotes |
| **Evidence** | _RateTables/ directory empty; straight-through pipeline requires pricing basis |
| **Impacted WBS/CBS** | All line items (E, PM, CONT) |
| **Estimate Impact** | HIGH - all pricing based on allowances; confidence affected |
| **Override Path** | Provide rate tables in _RateTables/ for next estimate run |

---

### D-003: CBS Mapping

| Property | Value |
|----------|-------|
| **Decision ID** | D-003 |
| **Decision** | Map DEL-02-01 primarily to Engineering & Design (E) CBS category |
| **Trigger** | Deliverable type requires CBS assignment |
| **Evidence** | _CONTEXT.md identifies deliverable as "Design Package" under "Architecture / Design" discipline; produces concept drawings and narrative |
| **Impacted WBS/CBS** | PKG-04/DEL-02-01 mapped to E (primary), PM (secondary) |
| **Estimate Impact** | LOW - standard design deliverable classification |
| **Override Path** | Revise CBS mapping in config if project uses different classification |

---

### D-004: Contingency Rate

| Property | Value |
|----------|-------|
| **Decision ID** | D-004 |
| **Decision** | Apply 15% contingency to base estimate |
| **Trigger** | PCT_BY_BUCKET contingency method requires percentage selection |
| **Evidence** | Source documents contain multiple TBDs: Appendix B location TBD, Town setback requirements TBD, Code edition TBD per Datasheet and Specification; blocking conflicts identified (C-002, A-003) |
| **Impacted WBS/CBS** | CONT category; $5,700 |
| **Estimate Impact** | MED - contingency covers scope uncertainty from TBDs |
| **Override Path** | Resolve TBDs and reduce contingency in next estimate iteration |

---

### D-005: Scope Boundary

| Property | Value |
|----------|-------|
| **Decision ID** | D-005 |
| **Decision** | Scope limited to proposal-stage concept package production; excludes detailed design |
| **Trigger** | Scope definition required for estimate boundary |
| **Evidence** | Specification explicitly states "This is a concept-level package for proposal evaluation, not construction documentation"; Procedure states "Target schematic design level of detail" |
| **Impacted WBS/CBS** | All line items - sized for concept-level effort |
| **Estimate Impact** | HIGH - defines level of effort for all drawing and documentation tasks |
| **Override Path** | If detailed design required, create new deliverable estimate |

---

### D-006: Engineering Coordination Scope

| Property | Value |
|----------|-------|
| **Decision ID** | D-006 |
| **Decision** | Include Civil, Structural, and MEP coordination as separate allowance line items |
| **Trigger** | Procedure Step 9.2 requires engineering coordination; Addendum 03 technical requirements require MEP input |
| **Evidence** | Procedure identifies Civil Engineer, Structural Engineer, Mechanical Engineer, Electrical Engineer in Team Roles table; Specification R3-R8 requires technical integration |
| **Impacted WBS/CBS** | L-008, L-009, L-010 (E category) |
| **Estimate Impact** | MED - $5,500 for coordination effort |
| **Override Path** | Adjust coordination hours if team structure differs |

---

### D-007: Pricing Date

| Property | Value |
|----------|-------|
| **Decision ID** | D-007 |
| **Decision** | Use 2026-02 as pricing date |
| **Trigger** | Pricing date required for BOE |
| **Evidence** | Estimate created 2026-02-04; no alternate pricing date specified |
| **Impacted WBS/CBS** | All - establishes "dollars of" basis |
| **Estimate Impact** | LOW - short-duration deliverable |
| **Override Path** | Specify alternate pricing_date in _CONFIG.md |

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Author** | ESTIMATING Agent (Type 2) |

---

**END OF DECISION LOG**
