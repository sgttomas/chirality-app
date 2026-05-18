# Dependencies: DEL-03-01 Site Plan, Circulation, Parking & Operational Layout

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (21 rows; 21 ACTIVE, 0 RETIRED)
- **Schema Version:** v3.1

### Summary Counts

| Category | Count |
|---|---|
| **Total rows** | 21 |
| **ACTIVE** | 21 |
| **RETIRED** | 0 |
| **ANCHOR rows** | 8 |
| **EXECUTION rows** | 13 |
| IMPLEMENTS_NODE (parent anchor) | 1 |
| TRACES_TO_REQUIREMENT | 7 |
| UPSTREAM EXECUTION | 9 |
| DOWNSTREAM EXECUTION | 4 |

### Compact Register Table

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Status |
|---|---|---|---|---|---|---|---|
| DEP-03-01-001 | ANCHOR | IMPLEMENTS_NODE | UP | OTHER | WBS_NODE | PKG-003 | ACTIVE |
| DEP-03-01-002 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0100 | ACTIVE |
| DEP-03-01-003 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0101 | ACTIVE |
| DEP-03-01-004 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0102 | ACTIVE |
| DEP-03-01-005 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0103 | ACTIVE |
| DEP-03-01-006 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0104 | ACTIVE |
| DEP-03-01-007 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | OBJ-005 | ACTIVE |
| DEP-03-01-008 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | OBJ-007 | ACTIVE |
| DEP-03-01-009 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-02-01 | ACTIVE |
| DEP-03-01-010 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-02-02 | ACTIVE |
| DEP-03-01-011 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-02-03 | ACTIVE |
| DEP-03-01-012 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-04-01 | ACTIVE |
| DEP-03-01-013 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-04-02 | ACTIVE |
| DEP-03-01-014 | EXECUTION | N/A | UP | PREREQUISITE | DOCUMENT | TPN46 | ACTIVE |
| DEP-03-01-015 | EXECUTION | N/A | UP | PREREQUISITE | DOCUMENT | Geotech Report | ACTIVE |
| DEP-03-01-016 | EXECUTION | N/A | UP | CONSTRAINT | DOCUMENT | Civil survey files | ACTIVE |
| DEP-03-01-017 | EXECUTION | N/A | UP | PREREQUISITE | DOCUMENT | Adj Subdiv exhibit | ACTIVE |
| DEP-03-01-018 | EXECUTION | N/A | DOWN | HANDOVER | DELIVERABLE | DEL-03-02 | ACTIVE |
| DEP-03-01-019 | EXECUTION | N/A | DOWN | HANDOVER | DELIVERABLE | DEL-03-03 | ACTIVE |
| DEP-03-01-020 | EXECUTION | N/A | DOWN | INTERFACE | DELIVERABLE | DEL-03-05 | ACTIVE |
| DEP-03-01-021 | EXECUTION | N/A | DOWN | INTERFACE | DELIVERABLE | DEL-03-04 | ACTIVE |

## Run Notes

### Run: 2026-02-17 (initial extraction)

**Run Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: AUTO (resolved to: Datasheet.md -- contains definition/traceability fields)
- EXECUTION_DOC_ORDER: AUTO (resolved to: Procedure.md, Specification.md, Guidance.md, Datasheet.md)
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (available; validated)
- _REFERENCES.md: present (used for document target resolution)

**Defaults Applied:**
- ANCHOR_DOC selected as Datasheet.md (contains Identification table with Package ID, scope item references, and traceability fields)
- EXECUTION_DOC_ORDER prioritized Procedure.md (prerequisites, workflow steps) then Specification.md (requirements with explicit deliverable cross-references), then Guidance.md (considerations, trade-offs), then Datasheet.md (attributes)

**Decomposition Validation:**
- Decomposition located and read successfully
- DEL-03-01 confirmed in decomposition under PKG-003 with CoversScopeItems: SOW-0100 through SOW-0104
- SupportsObjectives confirmed: OBJ-005, OBJ-007
- All target deliverable IDs (DEL-02-01, DEL-02-02, DEL-02-03, DEL-04-01, DEL-04-02, DEL-03-02, DEL-03-03, DEL-03-04, DEL-03-05) confirmed present in decomposition

**Assumptions Recorded:**
- OBJ-007 mapping is marked ASSUMPTION in source (best-effort per PACKAGE_HEURISTIC); however, it is confirmed in the decomposition SupportsObjectives column. Recorded as MEDIUM confidence.
- DEP-03-01-021 (downstream interface to DEL-03-04 for utility routing) is IMPLICIT -- the source implies spatial constraint but does not state an explicit handover. Recorded as MEDIUM confidence with ASSUMPTION note.

**Integrity Check Results:**
- Parent anchor count (ACTIVE IMPLEMENTS_NODE): 1 -- PASS (no FLOATING_NODE or AMBIGUOUS_ANCHOR warning)
- All DependencyIDs unique: PASS
- All ACTIVE rows have EvidenceFile + SourceRef: PASS
- All enums canonical: PASS
- All FromDeliverableID = DEL-03-01: PASS
- CSV parseable with 29 columns matching schema: PASS
- No obvious duplicate rows: PASS

**No warnings generated.**

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Available (FINAL v1.0 PHASE7) | None | 21 |

## Lifecycle Summary

### Extraction Lifecycle
| Status | Count |
|---|---|
| ACTIVE | 21 |
| RETIRED | 0 |

### Closure Lifecycle (SatisfactionStatus breakdown, ACTIVE rows only)
| SatisfactionStatus | Count |
|---|---|
| TBD | 20 |
| PENDING | 1 |

**Note:** DEP-03-01-016 (civil survey files) has SatisfactionStatus=PENDING because the files are explicitly noted as post-award only (not available at proposal stage).

### Confidence Distribution (ACTIVE rows only)
| Confidence | Count |
|---|---|
| HIGH | 17 |
| MEDIUM | 4 |

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT=NONE; no downstream handoff notes generated this run.
