# Dependencies: DEL-003-01 Preliminary Mechanical Design
## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register
- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (v3.1 schema)
- **Total ACTIVE rows:** 21
- **ANCHOR rows:** 4 (1 IMPLEMENTS_NODE, 3 TRACES_TO_REQUIREMENT)
- **EXECUTION rows:** 17 (2 PREREQUISITE, 6 INTERFACE, 6 HANDOVER, 3 CONSTRAINT)

| DependencyID | Class | Direction | Type | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-003-01-001 | ANCHOR | UPSTREAM | IMPLEMENTS_NODE | PKG-003 Mechanical Design | HIGH |
| DEP-003-01-002 | ANCHOR | UPSTREAM | TRACES_TO_REQUIREMENT | SOW-0010c | HIGH |
| DEP-003-01-003 | ANCHOR | UPSTREAM | TRACES_TO_REQUIREMENT | OBJ-003 | HIGH |
| DEP-003-01-004 | ANCHOR | UPSTREAM | TRACES_TO_REQUIREMENT | OBJ-004 | HIGH |
| DEP-003-01-005 | EXECUTION | UPSTREAM | PREREQUISITE | R-01 RFP | HIGH |
| DEP-003-01-006 | EXECUTION | UPSTREAM | PREREQUISITE | R-04 App B (Shop) | HIGH |
| DEP-003-01-007 | EXECUTION | UPSTREAM | INTERFACE | DEL-001-01 Preliminary Architectural | MEDIUM |
| DEP-003-01-008 | EXECUTION | UPSTREAM | INTERFACE | DEL-002-01 Preliminary Structural | MEDIUM |
| DEP-003-01-009 | EXECUTION | UPSTREAM | INTERFACE | DEL-006-01 Preliminary Plumbing | MEDIUM |
| DEP-003-01-010 | EXECUTION | UPSTREAM | INTERFACE | DEL-004-01 Preliminary Electrical | MEDIUM |
| DEP-003-01-011 | EXECUTION | UPSTREAM | CONSTRAINT | Natural gas tie-in (SOW-0080) | HIGH |
| DEP-003-01-012 | EXECUTION | DOWNSTREAM | HANDOVER | DEL-003-02 HVAC Plans | HIGH |
| DEP-003-01-013 | EXECUTION | DOWNSTREAM | HANDOVER | DEL-003-03 Ductwork Plans | HIGH |
| DEP-003-01-014 | EXECUTION | DOWNSTREAM | HANDOVER | DEL-003-04 Exhaust Plans | HIGH |
| DEP-003-01-015 | EXECUTION | DOWNSTREAM | HANDOVER | DEL-003-05 Equipment Schedule | HIGH |
| DEP-003-01-016 | EXECUTION | DOWNSTREAM | HANDOVER | DEL-003-06 Calculation Package | HIGH |
| DEP-003-01-017 | EXECUTION | DOWNSTREAM | HANDOVER | DEL-003-07 Specification | HIGH |
| DEP-003-01-018 | EXECUTION | UPSTREAM | CONSTRAINT | County approval of preliminary design | HIGH |
| DEP-003-01-019 | EXECUTION | UPSTREAM | INTERFACE | DEL-008-01 Geotechnical Report | MEDIUM |
| DEP-003-01-020 | EXECUTION | UPSTREAM | INTERFACE | Crane supplier (runway envelope) | MEDIUM |
| DEP-003-01-021 | EXECUTION | UPSTREAM | CONSTRAINT | P.Eng. review of preliminary design | HIGH |

## Run Notes
- **Run Date:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS:** AUTO (Datasheet.md, Specification.md, Guidance.md, Procedure.md)
- **ANCHOR_DOC:** Datasheet.md (contains explicit Deliverable ID, Package, SOW, and Objective fields)
- **EXECUTION_DOC_ORDER:** Procedure.md, Specification.md, Guidance.md, Datasheet.md
- **DECOMPOSITION_PATH:** _Decomposition/WDMLRL_Decomposition_Claude.md (R1 -- 2026-02-25)
- **Decomposition status:** Available; anchor validation and label resolution performed successfully
- **_REFERENCES.md status:** Available; used for document target resolution (R-01, R-04 locations confirmed)
- **Parent anchor check:** PASS (1 IMPLEMENTS_NODE row: DEP-003-01-001)
- No warnings.

### New rows added this run
- **DEP-003-01-019:** Geotechnical report interface -- Datasheet Conditions table explicitly states "mechanical equipment placement may be affected" by geotech results (RFP §4.8.2). Procedure characterizes as informational at preliminary stage ("may proceed without"). Classified as INTERFACE/ADVISORY rather than PREREQUISITE/BLOCKING.
- **DEP-003-01-020:** Crane supplier interface -- Specification REQ-003-01-13 explicitly requires verification that mechanical equipment and ductwork do not conflict with crane runway envelope. Crane supplier is a distinct external source for runway dimensions separate from structural design (DEL-002-01).
- **DEP-003-01-021:** P.Eng. review constraint -- Specification REQ-003-01-10 (enriched per F-001) explicitly requires P.Eng. review of preliminary design direction before County submission. This is a distinct approval gate from the County approval (DEP-003-01-018).

### Exclusion notes
- **Site meeting (RFP §3.2):** Procedure lists site meeting attendance as a prerequisite but explicitly notes it "is a prerequisite for the overall RFP response process, not solely for this deliverable." Not extracted under CONSERVATIVE strictness.
- **Welding equipment specs from County:** Datasheet notes welding equipment supply is County responsibility (SOW-0204), but no explicit statement that County must provide specifications as an input to DEL-003-01. Not extracted.
- **Coordination-only references:** Multiple references to "coordination" with other disciplines appear throughout sources. Only those with explicit information/artifact transfer statements were extracted; pure coordination mentions were excluded per information-flow-only model.

## Run History
| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26T00:00 | UPDATE | CONSERVATIVE | Available (R1) | None | 18 |
| 2026-02-26T01:00 | UPDATE | CONSERVATIVE | Available (R1) | None | 21 |

## Lifecycle Summary
- **ACTIVE:** 21
- **RETIRED:** 0
- **SatisfactionStatus breakdown:** TBD: 21

### By DependencyClass
| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 4 | 0 |
| EXECUTION | 17 | 0 |

### By Direction (EXECUTION only)
| Direction | Count |
|---|---|
| UPSTREAM | 11 |
| DOWNSTREAM | 6 |

### By DependencyType (EXECUTION only)
| Type | Count |
|---|---|
| PREREQUISITE | 2 |
| INTERFACE | 6 |
| HANDOVER | 6 |
| CONSTRAINT | 3 |

### By EstimateImpactClass (EXECUTION only)
| Impact | Count |
|---|---|
| BLOCKING | 9 |
| ADVISORY | 6 |
| INFO | 2 |

## Downstream Handoff Notes
**CONSUMER_CONTEXT: TASK_ESTIMATING**

### Blocking dependencies for estimating
- **DEP-003-01-018 (County approval):** County approval of the preliminary mechanical design is a BLOCKING constraint for estimating. Scope and system selections cannot be finalized without it. Until approval is received, all downstream deliverables (DEL-003-02 through DEL-003-07) remain gated.
- **DEP-003-01-011 (Natural gas tie-in):** Natural gas availability at site (PKG-018 scope, SOW-0080) is BLOCKING for heating system estimating. If gas is unavailable, alternate fuel systems change the cost basis entirely.
- **DEP-003-01-021 (P.Eng. review):** P.Eng. review of the preliminary design direction is BLOCKING -- it gates County submission and therefore gates all downstream estimating.
- **DEP-003-01-012 through DEP-003-01-017 (downstream handovers):** All 6 downstream deliverables (DEL-003-02 through DEL-003-07) cannot be estimated until this preliminary design is approved. These are BLOCKING handovers.

### Advisory dependencies for estimating
- **DEP-003-01-007 through DEP-003-01-010 (discipline interfaces):** Coordination interfaces with DEL-001-01 (Architectural), DEL-002-01 (Structural), DEL-004-01 (Electrical), DEL-006-01 (Plumbing) are ADVISORY. They may affect layout and sizing but do not gate estimating commencement. The Procedure notes these are concurrent inputs.
- **DEP-003-01-019 (Geotechnical report):** Geotechnical results may affect mechanical equipment placement, but the Procedure explicitly states DEL-003-01 may proceed without it. ADVISORY for estimating.
- **DEP-003-01-020 (Crane supplier):** Crane runway envelope dimensions may affect ductwork routing and equipment placement. ADVISORY -- design can proceed with assumed clearances, but final sizing may change.

### Informational dependencies
- **DEP-003-01-005, DEP-003-01-006 (RFP and App B):** These source documents are already available and do not gate estimating. Classified as INFO.
