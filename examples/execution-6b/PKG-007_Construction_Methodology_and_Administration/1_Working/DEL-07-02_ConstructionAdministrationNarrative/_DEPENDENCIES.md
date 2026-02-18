# Dependencies

**Deliverable ID:** DEL-07-02
**Deliverable Name:** Construction Administration Narrative
**Package:** PKG-007 -- Construction Methodology & Administration
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 10
**Total RETIRED rows:** 0

### ANCHOR Dependencies (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-07-02-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0020 | HIGH | ACTIVE |
| DEP-07-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | HIGH | ACTIVE |
| DEP-07-02-003 | TRACES_TO_REQUIREMENT | DOCUMENT | RFP SS7.3 SS7.3.1-SS7.3.3 | HIGH | ACTIVE |

### EXECUTION Dependencies (7 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-07-02-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-07-01 (Construction Methodology Narrative) | HIGH | ACTIVE |
| DEP-07-02-005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-04 (Meetings and Reporting Narrative) | HIGH | ACTIVE |
| DEP-07-02-006 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-05 (Quality Management Narrative) | HIGH | ACTIVE |
| DEP-07-02-007 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 + Appendix J (Supplementary Conditions) | HIGH | ACTIVE |
| DEP-07-02-008 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 (Formal Submission Package) | HIGH | ACTIVE |
| DEP-07-02-009 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-08-02 (Deficiencies Management Narrative) | MEDIUM | ACTIVE |
| DEP-07-02-010 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-08-01 (Commissioning Training Closeout Narrative) | MEDIUM | ACTIVE |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

### Defaults and Paths Used

| Setting | Value |
|---|---|
| RUN_ROOT | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/` |
| DECOMPOSITION_PATH | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL) |
| SOURCE_DOCS | AUTO -- resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md |
| ANCHOR_DOC | AUTO -- resolved to: Datasheet.md (contains Identification table with Scope Item, Objective Alignment, RFP Authority) |
| EXECUTION_DOC_ORDER | AUTO -- resolved to: Specification.md, Procedure.md, Guidance.md |
| _REFERENCES.md | Present and read; used for cross-reference validation |
| Existing Dependencies.csv | Not present; created new |

### Assumptions Made During Extraction

- DEP-07-02-010: Interface between DEL-07-02 closeout document assembly (R-CA-005) and DEL-08-01 is inferred from scope boundary exclusion rather than an explicit handover statement. Marked as ASSUMPTION with MEDIUM confidence.

### Warnings

None.

### Quality Check Results

| Check | Result |
|---|---|
| Required columns present and CSV parseable | PASS |
| DependencyID unique within file | PASS (10 unique IDs) |
| All ACTIVE rows have EvidenceFile and SourceRef | PASS |
| Status and SatisfactionStatus values canonical | PASS |
| _DEPENDENCIES.md counts match Dependencies.csv | PASS (10 ACTIVE, 0 RETIRED) |
| No obvious duplicate rows | PASS |
| Parent anchor (IMPLEMENTS_NODE) count | PASS (exactly 1: DEP-07-02-001 -> SOW-0020) |
| FromDeliverableID matches host deliverable | PASS (all rows: DEL-07-02) |
| Enum normalization | PASS (all Direction values use UPSTREAM/DOWNSTREAM; all DependencyClass values canonical) |
| TargetDeliverableID populated only for TargetType=DELIVERABLE | PASS |
| TargetRefID used for non-deliverable targets | PASS |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 10 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 9 |
| PENDING | 1 |

**Note:** DEP-07-02-007 (CCDC 14-2013 + Appendix J) is marked PENDING because the source documents explicitly state that specific clauses affecting superintendent authority, RFI turnaround, and change order thresholds are "TBD pending document review" -- the dependency is known but not yet satisfied.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 10 |
