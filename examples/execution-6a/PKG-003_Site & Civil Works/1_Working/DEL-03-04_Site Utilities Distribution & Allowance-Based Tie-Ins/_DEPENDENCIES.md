# Dependencies: DEL-03-04 Site Utilities Distribution & Allowance-Based Tie-Ins

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (16 rows; 16 ACTIVE, 0 RETIRED)
- **Schema Version:** v3.1
- **Last Run:** 2026-02-17

### ANCHOR edges (5 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence | Notes |
|---|---|---|---|---|---|
| DEP-03-04-001 | IMPLEMENTS_NODE | -- | PKG-003 -- Site & Civil Works | HIGH | Parent package |
| DEP-03-04-002 | TRACES_TO_REQUIREMENT | SOW-0109 | Provide and coordinate all required site services and utilities connections | HIGH | Explicit scope coverage |
| DEP-03-04-003 | TRACES_TO_REQUIREMENT | SOW-0110 | Utility tie-ins as cash allowance | HIGH | Explicit scope coverage; DEC-004 |
| DEP-03-04-004 | TRACES_TO_REQUIREMENT | OBJ-005 | Deliver complete site/civil works | MEDIUM | Best-effort mapping (ASSUMPTION) |
| DEP-03-04-005 | TRACES_TO_REQUIREMENT | OBJ-008 | Execute safe controlled Design-Build delivery | MEDIUM | Best-effort mapping (ASSUMPTION) |

### EXECUTION edges (11 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence | Notes |
|---|---|---|---|---|---|---|
| DEP-03-04-006 | UPSTREAM | PREREQUISITE | EXTERNAL | Owner-provided underground services drawings | HIGH | Post-award gate; OSR 10.3.2 |
| DEP-03-04-007 | UPSTREAM | PREREQUISITE | EXTERNAL | Survey files from civil engineering firm | HIGH | Post-award gate; Addendum 03 s1.20 |
| DEP-03-04-008 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical investigation report (Appendix D of RFP) | HIGH | Available at proposal phase |
| DEP-03-04-009 | UPSTREAM | PREREQUISITE | EXTERNAL | Town of Penhold municipal servicing standards | HIGH | To be obtained during design |
| DEP-03-04-010 | UPSTREAM | PREREQUISITE | EXTERNAL | Utility Provider connection standards and applications | HIGH | Per REQ-01; RFP s7.3.3 |
| DEP-03-04-011 | UPSTREAM | INTERFACE | DELIVERABLE (DEL-03-01) | Site Plan, Circulation, Parking & Operational Layout | HIGH | Building locations affect routing |
| DEP-03-04-012 | UPSTREAM | INTERFACE | DELIVERABLE (DEL-03-02) | Grading, Earthworks, Drainage & Stormwater | HIGH | Grading affects trench depths/grades |
| DEP-03-04-013 | DOWNSTREAM | INTERFACE | PACKAGE (PKG-002) | Main PSB building mechanical/electrical systems | MEDIUM | Scope boundary at building entry |
| DEP-03-04-014 | DOWNSTREAM | HANDOVER | DELIVERABLE (DEL-01-07) | Commissioning, Training, Closeout & Warranty | HIGH | As-built utility data handover |
| DEP-03-04-015 | UPSTREAM | INTERFACE | DELIVERABLE (DEL-01-04) | Permitting, Inspections & AHJ Coordination | MEDIUM | Permit coordination per SOW-0009 |
| DEP-03-04-016 | DOWNSTREAM | INTERFACE | PACKAGE (PKG-004) | Cold Storage Building utility connections | HIGH | Must serve both PSB and cold storage |

## Run Notes

### Run: 2026-02-17

**Run Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: AUTO (resolved: Datasheet.md -- contains Identification table with scope coverage, objectives, and decision references)
- EXECUTION_DOC_ORDER: AUTO (resolved: Procedure.md, Specification.md, Guidance.md)
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (available; validated)

**Defaults Applied:**
- ANCHOR_DOC selected as Datasheet.md (highest-confidence match for definition/traceability signal per DEFAULT heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER: Procedure.md first (filename contains "procedure"), then Specification.md (filename contains "spec"), then Guidance.md (filename contains "guidance")
- _REFERENCES.md present and consulted for document target resolution

**Assumptions Recorded:**
- OBJ-005 and OBJ-008 trace anchors: Datasheet explicitly tags these as "ASSUMPTION: best-effort mapping per PKG-003 package grouping." Included at MEDIUM confidence.
- DEL-03-01 and DEL-03-02 interfaces: Procedure states these "are expected to progress in parallel rather than strictly sequential." Recorded as INTERFACE (not PREREQUISITE) to avoid implying strict sequencing.
- PKG-002 downstream interface: Specification states building-internal utility systems are under PKG-002 but does not name a single deliverable. TargetDeliverableID left blank; TargetType set to PACKAGE.
- PKG-004 downstream interface: Datasheet confirms utility distribution serves Cold Storage Building. TargetDeliverableID left blank; TargetType set to PACKAGE.

**Warnings:**
- None. All quality checks passed.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE (Anchor) | ACTIVE (Execution) | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Available (v1.0 Phase 7) | None | 5 | 11 | 16 |

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 16
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown, ACTIVE rows only)
- **TBD:** 11
- **PENDING:** 5 (DEP-03-04-006, -007, -009, -010 -- post-award/design-phase prerequisites not yet received)

### Tree x DAG Integrity
- **IMPLEMENTS_NODE count (ACTIVE):** 1 -- PASS (exactly one parent anchor)
- **TRACES_TO_REQUIREMENT count (ACTIVE):** 4 (SOW-0109, SOW-0110, OBJ-005, OBJ-008)
- **No warnings issued.**

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT: NONE -- no consumer-specific notes generated.
