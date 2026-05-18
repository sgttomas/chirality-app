# Dependencies: DEL-02-07 Emergency Power & Backup Generator

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** `Dependencies.csv` (13 rows)
- **Last Run:** 2026-02-17
- **Schema Version:** v3.1

### Summary

| DependencyClass | AnchorType | Count (ACTIVE) |
|---|---|---|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 3 |
| EXECUTION | NOT_APPLICABLE | 9 |
| **Total** | | **13** |

### ANCHOR Rows (4 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-0207-A001 | IMPLEMENTS_NODE | SOW-0222 | SOW-0222 | HIGH |
| DEP-0207-A002 | TRACES_TO_REQUIREMENT | SOW-0216 | SOW-0216 | HIGH |
| DEP-0207-A003 | TRACES_TO_REQUIREMENT | OBJ-002 | OBJ-002 | HIGH |
| DEP-0207-A004 | TRACES_TO_REQUIREMENT | OBJ-008 | OBJ-008 | HIGH |

### EXECUTION Rows (9 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement (short) |
|---|---|---|---|---|---|
| DEP-0207-E001 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-04 | Overhead door spec (size, operator type, door count) required for bay door secondary opening mechanism |
| DEP-0207-E002 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-06 | Electrical distribution concept required for ATS/essential loads panel integration |
| DEP-0207-E003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-01 | Site layout required for generator pad location |
| DEP-0207-E004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-04 | Site electrical service and generator pad location |
| DEP-0207-E005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-05 | Generator exhaust routing and outdoor placement coordination |
| DEP-0207-E006 | UPSTREAM | CONSTRAINT | EXTERNAL | Owner (Town of Penhold) | 72-hour runtime confirmation required before sizing |
| DEP-0207-E007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-04 | Permits for generator installation, fuel storage, electrical work |
| DEP-0207-E008 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-07 | Commissioning records, test results, and training records to closeout |
| DEP-0207-E009 | UPSTREAM | CONSTRAINT | EXTERNAL | AHJ | Post-disaster importance ruling needed for seismic anchorage |

## Run Notes

### Run 2026-02-17 (Initial Extraction)

**Run Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: AUTO (resolved to: Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved to: Procedure.md, Specification.md, Guidance.md)
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md`

**Defaults Applied:**
- ANCHOR_DOC selected as Datasheet.md (contains "datasheet" keyword; has Identification table with Covers Scope Items and Supports Objectives fields).
- EXECUTION_DOC_ORDER: Procedure.md first (contains "procedure" keyword; has explicit Prerequisites section), then Specification.md, then Guidance.md.
- Decomposition located and used for anchor validation and target resolution.

**Assumptions:**
- None. All extracted rows are based on explicit evidence.

**Warnings:**
- None.

**Integrity Checks:**
- Parent anchor (IMPLEMENTS_NODE) count: 1 (SOW-0222). PASS.
- DependencyID uniqueness: 13 unique / 13 total. PASS.
- All ACTIVE rows have EvidenceFile and SourceRef. PASS.
- FromDeliverableID consistency: all rows = DEL-02-07. PASS.
- CSV parseable: PASS (validated with Python csv.DictReader).

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Located (FINAL v1.0 PHASE7) | None | 4 | 9 | 13 |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 13 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 11 |
| PENDING | 2 |

**Notes on PENDING rows:**
- DEP-0207-E006 (Owner 72-hour runtime confirmation): Open issue; awaiting Owner response.
- DEP-0207-E009 (AHJ post-disaster importance ruling): Awaiting AHJ ruling on seismic anchorage applicability.

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT: NONE. No consumer-specific notes generated.
