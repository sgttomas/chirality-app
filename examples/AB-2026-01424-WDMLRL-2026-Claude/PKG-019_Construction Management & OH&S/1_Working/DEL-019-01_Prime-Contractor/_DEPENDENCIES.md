# DEL-019-01: Dependencies

**Deliverable ID:** DEL-019-01_Prime-Contractor
**Dependency Tracking Status:** TRACKED
**Register Schema:** v3.1

---

## Upstream Dependencies

| Source | Target | Type | Class | Notes |
|---|---|---|---|---|
| DEL-019-01 | DEL-021-04 (CCDC 14-2013 Contract Execution) | PREREQUISITE | EXECUTION | Contract award required before designation form can be executed |
| DEL-019-01 | Camrose County (Prime Contractor Designation Form) | PREREQUISITE | EXECUTION | County-issued form; Proponent cannot self-generate |
| DEL-019-01 | DEL-021-03 (Insurance Package) | PREREQUISITE | EXECUTION | Insurance certificates required before contract execution |
| DEL-019-01 | R-03 / Appendix A (H&S Pre-Qualification form) | PREREQUISITE | EXECUTION | County-provided form template required for proposal submission |

## Internal Package Dependencies

| Source | Target | Type | Class | Notes |
|---|---|---|---|---|
| DEL-019-01 | DEL-019-02 (Weekly Coordination) | ENABLES | EXECUTION | Depends on prime contractor designation for coordination structure |
| DEL-019-01 | DEL-019-03 (Subcontractor Mgmt) | ENABLES | EXECUTION | Depends on prime contractor authority establishment |
| DEL-019-01 | DEL-019-04 (QC Management) | ENABLES | EXECUTION | Depends on prime contractor oversight structure |

## External Package Dependencies

| Source | Target | Type | Class | Notes |
|---|---|---|---|---|
| DEL-019-01 | DEL-009-04 (Code Compliance Register & Inspection Log) | INTERFACE | EXECUTION | Prime Contractor enables inspection coordination function |

## Cross-Project Dependencies

None identified.

## Anchors (Tree Linkage)

| Anchor | Target | AnchorType | Notes |
|---|---|---|---|
| DEL-019-01 | SOW-0083 | IMPLEMENTS_NODE | Primary SSOW item: Assume Prime Contractor designation |
| DEL-019-01 | OBJ-007 | TRACES_TO_REQUIREMENT | Zero lost-time incidents; full OH&S compliance |

---

## Extracted Dependency Register

**Total rows:** 10
**ACTIVE:** 10 | **RETIRED:** 0

| DependencyID | Class | AnchorType | Dir | DepType | TargetType | Target | Status |
|---|---|---|---|---|---|---|---|
| DEP-019-01-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0083 | ACTIVE |
| DEP-019-01-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-007 | ACTIVE |
| DEP-019-01-003 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-021-04 | ACTIVE |
| DEP-019-01-004 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | EXTERNAL | Camrose County (Designation Form) | ACTIVE |
| DEP-019-01-005 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-021-03 | ACTIVE |
| DEP-019-01-006 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DOCUMENT | R-03 (Appendix A) | ACTIVE |
| DEP-019-01-007 | EXECUTION | N/A | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-019-02 | ACTIVE |
| DEP-019-01-008 | EXECUTION | N/A | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-019-03 | ACTIVE |
| DEP-019-01-009 | EXECUTION | N/A | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-019-04 | ACTIVE |
| DEP-019-01-010 | EXECUTION | N/A | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-009-04 | ACTIVE |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE (all) | 10 |
| RETIRED (all) | 0 |
| ANCHOR rows | 2 |
| EXECUTION rows | 8 |
| UPSTREAM | 6 |
| DOWNSTREAM | 4 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 5 |
| PENDING | 5 |

### Integrity Checks

| Check | Result |
|---|---|
| Parent anchor (IMPLEMENTS_NODE) | PASS (1 found: SOW-0083) |
| DependencyID uniqueness | PASS (10/10 unique) |
| FromDeliverableID consistency | PASS (all = DEL-019-01) |
| EvidenceFile + SourceRef present | PASS (all ACTIVE rows have evidence) |

---

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

The following observations are relevant for downstream estimating workflows:

1. **BLOCKING upstream prerequisites (3 rows):**
   - DEP-019-01-003: Contract execution (DEL-021-04) must precede designation. This gates all site-related estimating for this deliverable.
   - DEP-019-01-004: Prime Contractor Designation Form from Camrose County is an external dependency with no Proponent control over timing. Estimating should assume form availability immediately post-award.
   - DEP-019-01-005: Insurance Package (DEL-021-03) must be in place before contract execution. Insurance procurement lead time should be factored into pre-construction scheduling.

2. **ADVISORY items (5 rows):**
   - DEP-019-01-006: Appendix A (H&S Pre-Qualification) is a proposal-stage artifact; its preparation effort is pre-contract and may or may not be included in project cost estimates depending on estimating boundary.
   - DEP-019-01-007/008/009: Three downstream deliverables (DEL-019-02, -03, -04) are enabled by this deliverable. Their estimating readiness depends on DEL-019-01 scope being well-defined.
   - DEP-019-01-010: Interface with DEL-009-04 (inspection coordination) may affect estimating for inspection-related effort allocation.

3. **Estimating boundary note:** Several prerequisites (contract award, insurance, Appendix A) are pre-construction / proposal-stage activities. Estimators should confirm whether pre-contract effort is within the estimating scope boundary for this project.

---

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING

### Defaults and Paths Used

| Parameter | Value |
|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude |
| DELIVERABLE_PATH | {RUN_ROOT}/PKG-019_Construction Management & OH&S/1_Working/DEL-019-01_Prime-Contractor/ |
| DECOMPOSITION_PATH | {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md |
| DECOMPOSITION_STATUS | Located and used for anchor validation and label resolution |
| SOURCE_DOCS (AUTO) | Datasheet.md, Specification.md, Procedure.md, Guidance.md |
| DOC_ROLE_MAP | ANCHOR_DOC = Datasheet.md; EXECUTION_DOCS = Procedure.md, Guidance.md, Specification.md |
| _REFERENCES.md | Read; used for document target resolution (R-03 -> Appendix A) |
| Dependencies.csv (prior) | Not found; created new |

### Assumptions

- ASSUMPTION: Appendix A (R-03) is treated as a DOCUMENT dependency (required input form template) rather than a DELIVERABLE, because it is a County-provided template, not a project deliverable.
- ASSUMPTION: Contract award / CCDC 14-2013 execution is mapped to DEL-021-04 based on decomposition §7 PKG-021.
- ASSUMPTION: Insurance Package mapped to DEL-021-03 based on decomposition §7 PKG-021.

### Warnings

None.

### Decisions Not Taken

- Did not create EXECUTION edges for "coordination" references that lack specific information/artifact transfer (e.g., general references to "keeping aligned" with County).
- Did not create EXECUTION edges for structural adjacency within PKG-019 (e.g., DEL-019-01 and DEL-019-02 are co-packaged but the only edge is the explicit ENABLES relationship stated in source documents).
- Did not create ANCHOR rows for the package-level identity (PKG-019) since SOW-0083 is the canonical IMPLEMENTS_NODE anchor.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Located: WDMLRL_Decomposition_Claude.md | None | 2 | 8 | 10 |

---

## Dependency Notes

This deliverable establishes the foundational governance and authority structure for all subsequent construction management activities within PKG-019. It has a clear upstream dependency chain (contract execution -> insurance -> designation form from County) and enables three downstream sibling deliverables plus an inter-package interface with inspection coordination (DEL-009-04).

The Prime Contractor designation is a legal instrument under Alberta OH&S legislation, not merely an administrative task. The external dependency on Camrose County issuing the Designation Form (DEP-019-01-004) represents a hard gate that the Proponent cannot accelerate.

## Monitoring

Dependencies will be monitored through status reports and coordination meetings as outlined in DEL-019-02. The SatisfactionStatus of each dependency row should be updated as prerequisites are fulfilled during project execution.
