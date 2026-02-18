# Dependencies: DEL-03-02 Grading, Earthworks, Drainage & Stormwater

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETED
- **Dependencies.csv:** 11 rows (11 ACTIVE, 0 RETIRED)
- **Schema Version:** v3.1

### Summary by Class

| DependencyClass | AnchorType | Count |
|---|---|---|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 2 |
| EXECUTION | NOT_APPLICABLE | 8 |

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID / TargetName | Direction | Confidence |
|---|---|---|---|---|
| DEP-0302-001 | IMPLEMENTS_NODE | OBJ-005 | UPSTREAM | HIGH |
| DEP-0302-002 | TRACES_TO_REQUIREMENT | SOW-0105 | UPSTREAM | HIGH |
| DEP-0302-003 | TRACES_TO_REQUIREMENT | SOW-0106 | UPSTREAM | HIGH |

### EXECUTION Rows (8 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-0302-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-05 Environmental Constraints Flood Hazard & Regulatory Compliance | HIGH |
| DEP-0302-005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-01 Site Plan Circulation Parking & Operational Layout | HIGH |
| DEP-0302-006 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-03 Pavements Aggregate Yard Areas & Concrete Aprons | HIGH |
| DEP-0302-007 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-04 Site Utilities Distribution & Allowance-Based Tie-Ins | MEDIUM |
| DEP-0302-008 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Investigation Report (USG1123) | HIGH |
| DEP-0302-009 | UPSTREAM | PREREQUISITE | DOCUMENT | Site Grading Drawings (TPN46) | HIGH |
| DEP-0302-010 | UPSTREAM | CONSTRAINT | EXTERNAL | Geotechnical Services Retention (OSR 10.3.6) | HIGH |
| DEP-0302-011 | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta OHS Code 2009 Part 32 | HIGH |

## Run Notes

### Run 2026-02-17 (initial extraction)

**Run Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: AUTO (resolved to: Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved to: Procedure.md, Guidance.md, Specification.md)

**Decomposition:**
- Path: `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md`
- Status: Available; used for anchor validation and label resolution.

**Defaults Applied:**
- ANCHOR_DOC selected as Datasheet.md (matches "datasheet" heuristic pattern).
- EXECUTION_DOC_ORDER: Procedure.md first (matches "procedure" pattern), then Guidance.md (matches "guidance" pattern), then Specification.md (matches "spec" pattern).

**Extraction Notes:**
- Pass 1 (ANCHOR): 1 parent anchor (OBJ-005) and 2 trace anchors (SOW-0105, SOW-0106) extracted from Datasheet.md Identification section. All confirmed against decomposition scope ledger.
- Pass 2 (EXECUTION): 8 execution dependencies extracted across Guidance.md, Procedure.md, and Specification.md.
- DEP-0302-004 (DEL-03-05 blocking prerequisite) is the strongest execution dependency: multiple explicit "shall not proceed" statements in Guidance, Procedure, and Specification (REQ-3212) confirm this is a blocking gate for stormwater pond construction.
- DEP-0302-005 (DEL-03-01 interface) captures that building orientation/siting from the site plan is a required input to grading layout.
- DEP-0302-006 and DEP-0302-007 are downstream interfaces where this deliverable provides sulphate resistance and subgrade specs to DEL-03-03 and DEL-03-04 respectively.
- DEP-0302-008 and DEP-0302-009 are document prerequisites confirmed as available (SATISFIED).
- DEP-0302-010 and DEP-0302-011 are external constraints (geotechnical services retention and OHS excavation safety code).
- DEP-0302-007 marked MEDIUM confidence because the cross-deliverable coordination note in Guidance is explicit but the information transfer is narrower (only S-2 sulphate requirement) compared to DEP-0302-006 which has both sulphate and subgrade/compaction spec transfer.

**Warnings:** None.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Available (v1.0 PHASE7) | None | 3 | 8 | 11 |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 11 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 6 |
| PENDING | 3 |
| SATISFIED | 2 |

**Notes:**
- SATISFIED rows (DEP-0302-008, DEP-0302-009): Source documents confirmed available in _Sources/references/.
- PENDING rows (DEP-0302-004, DEP-0302-010, DEP-0302-011): Require action before work can proceed (flood fringe approval, geotech retention, OHS compliance plan).
- TBD rows: Satisfaction status not yet determined.

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT is NONE; no consumer-specific notes generated.
