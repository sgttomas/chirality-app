# Dependencies: DEL-02-01 Architectural Program, Layout & Code Planning

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (23 rows; 23 ACTIVE, 0 RETIRED)
- **Schema Version:** v3.1

### Summary by Class

| DependencyClass | AnchorType | Count (ACTIVE) |
|---|---|---|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 9 |
| EXECUTION | NOT_APPLICABLE (UPSTREAM) | 6 |
| EXECUTION | NOT_APPLICABLE (DOWNSTREAM) | 7 |
| **Total** | | **23** |

### ANCHOR Rows (Tree -- Definition Traceability)

| DependencyID | AnchorType | TargetRefID / TargetName | Confidence |
|---|---|---|---|
| DEP-02-01-001 | IMPLEMENTS_NODE | DEL-02-01_Architectural-Program-and-Space-Planning (PKG-002) | HIGH |
| DEP-02-01-002 | TRACES_TO_REQUIREMENT | SOW-0200: Integrated PSB design | HIGH |
| DEP-02-01-003 | TRACES_TO_REQUIREMENT | SOW-0207: Shared spaces program | HIGH |
| DEP-02-01-004 | TRACES_TO_REQUIREMENT | SOW-0208: Meeting room 40p/15 EM | HIGH |
| DEP-02-01-005 | TRACES_TO_REQUIREMENT | SOW-0218: Ceiling system approach | HIGH |
| DEP-02-01-006 | TRACES_TO_REQUIREMENT | SOW-0219: Accessibility per ABC | HIGH |
| DEP-02-01-007 | TRACES_TO_REQUIREMENT | SOW-0220: Adaptability/expansion | HIGH |
| DEP-02-01-008 | TRACES_TO_REQUIREMENT | SOW-0229: Code-required signage | HIGH |
| DEP-02-01-009 | TRACES_TO_REQUIREMENT | SOW-0600: Program dimension flexibility | HIGH |
| DEP-02-01-010 | TRACES_TO_REQUIREMENT | SOW-0601: Two-storey option | HIGH |

### EXECUTION Rows (DAG -- Information Flow)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-02-01-011 | UPSTREAM | PREREQUISITE | DOCUMENT | Functional Program (Appendix B) | HIGH |
| DEP-02-01-012 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Investigation Report (Appendix D) | HIGH |
| DEP-02-01-013 | UPSTREAM | PREREQUISITE | DOCUMENT | Site Grading Drawings (Appendix E) | HIGH |
| DEP-02-01-014 | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta Building Code | HIGH |
| DEP-02-01-015 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-01 Site Plan (PKG-003) | HIGH |
| DEP-02-01-016 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-04 Structural grid input (PKG-002) | HIGH |
| DEP-02-01-017 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-02 Firehall bays/support (PKG-002) | HIGH |
| DEP-02-01-018 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-03 PW shop/support (PKG-002) | HIGH |
| DEP-02-01-019 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-04 Structure/envelope (PKG-002) | HIGH |
| DEP-02-01-020 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-05 Mechanical/plumbing (PKG-002) | HIGH |
| DEP-02-01-021 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-06 Electrical/IT (PKG-002) | HIGH |
| DEP-02-01-022 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-07 Emergency power (PKG-002) | HIGH |
| DEP-02-01-023 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-04 Permitting/AHJ (PKG-001) | HIGH |

## Run Notes

### Run 2026-02-17 (initial extraction)

**Run Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: AUTO (resolved to: Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved to: Procedure.md, Guidance.md, Specification.md, Datasheet.md)
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (confirmed accessible; validated)

**Defaults Applied:**
- ANCHOR_DOC selected by heuristic: Datasheet.md (contains `datasheet` keyword and identification/traceability fields)
- EXECUTION_DOC_ORDER: Procedure.md first (contains `procedure` keyword; highest workflow clarity), then Guidance.md, Specification.md, Datasheet.md
- _REFERENCES.md read for document resolution; used to confirm Functional Program and Alberta Building Code pointers

**Assumptions:**
- SOW trace anchors emitted only for scope items explicitly mapped to DEL-02-01 in the decomposition scope ledger (CONSERVATIVE strictness)
- DEL-02-04 appears both as upstream (structural grid input, DEP-02-01-016) and downstream (building configuration output, DEP-02-01-019) because two distinct information flows exist

**Warnings:**
- None. Parent anchor found (1 IMPLEMENTS_NODE). No integrity warnings.

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE_ANCHOR | ACTIVE_EXECUTION | ACTIVE_Total |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Validated (FINAL v1.0) | None | 10 | 13 | 23 |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 23 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 21 |
| PENDING | 2 |

**Notes on PENDING rows:**
- DEP-02-01-011 (Functional Program): location TBD; document not yet accessible
- DEP-02-01-014 (Alberta Building Code): external; not directly accessible in this run

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT: NONE -- no handoff notes generated for this run.
