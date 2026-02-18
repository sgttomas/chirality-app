# Dependencies

**Deliverable ID:** DEL-03-02
**Deliverable Name:** Civil Design Brief
**Package:** PKG-003 -- Design Brief
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here. Extracted dependencies are maintained in Dependencies.csv.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 18
**Total RETIRED rows:** 0

### ANCHOR Dependencies (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-03-02-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0011 | HIGH |
| DEP-03-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | HIGH |
| DEP-03-02-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | RFP Section 7.1.2(2) | HIGH |

### EXECUTION Dependencies -- UPSTREAM (11 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (short) |
|---|---|---|---|---|
| DEP-03-02-004 | PREREQUISITE | DELIVERABLE | DEL-02-02 Civil Site Concept Plan | Draft/complete concept required as input |
| DEP-03-02-005 | PREREQUISITE | DELIVERABLE | DEL-02-01 Architectural Concept Package | Draft concept required for footprint and orientation |
| DEP-03-02-006 | INTERFACE | DELIVERABLE | DEL-02-03 Structural Concept Narrative | Grading and foundation drainage coordination |
| DEP-03-02-007 | INTERFACE | DELIVERABLE | DEL-02-04 Mechanical Concept Narrative | Utility service points and sump drainage routing |
| DEP-03-02-008 | PREREQUISITE | DOCUMENT | Appendix D -- Geotechnical Investigation Report (2021) | Grading and utility installation basis |
| DEP-03-02-009 | PREREQUISITE | DOCUMENT | Appendix D -- Wetland Assessment and Impact Report | Wetland constraints for layout and drainage |
| DEP-03-02-010 | PREREQUISITE | DOCUMENT | Appendix D -- Desktop Environmental Assessment (Ghostpine) | Environmental findings for site planning |
| DEP-03-02-011 | PREREQUISITE | DOCUMENT | Appendix E -- Site Grading | Existing conditions baseline for grading |
| DEP-03-02-012 | PREREQUISITE | DOCUMENT | Appendix F -- Site Plan / Subdivision Plan | Site boundaries and subdivision context |
| DEP-03-02-013 | CONSTRAINT | DOCUMENT | RFP Section 7.1.2(2) | Defines seven required brief topics |
| DEP-03-02-014 | CONSTRAINT | DOCUMENT | Addendum 03 | Site area, sumps, fill stations, cash allowance, survey |

### EXECUTION Dependencies -- DOWNSTREAM (4 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (short) |
|---|---|---|---|---|
| DEP-03-02-015 | INTERFACE | DELIVERABLE | DEL-01-06 Pricing Narrative and Assumptions | Cash allowance consistency |
| DEP-03-02-016 | INTERFACE | DELIVERABLE | DEL-10-02 Site Conditions and Due Diligence Summary | Consistent site condition language |
| DEP-03-02-017 | INTERFACE | DELIVERABLE | DEL-03-01 Architectural Design Brief | Site layout description consistency |
| DEP-03-02-018 | HANDOVER | DELIVERABLE | DEL-01-01 Compliance Matrix and Checklist | Completion triggers SOW-0011 compliance update |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

### Defaults and Paths Used

| Setting | Value |
|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/ |
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md |
| SOURCE_DOCS (AUTO) | Datasheet.md, Guidance.md, Procedure.md, Specification.md |
| DOC_ROLE_MAP | ANCHOR_DOC: Datasheet.md; EXECUTION_DOCS: Procedure.md, Guidance.md, Specification.md |
| ANCHOR_DOC | Datasheet.md |
| EXECUTION_DOC_ORDER | Procedure.md, Specification.md, Guidance.md |
| _REFERENCES.md | Read; used for cross-reference validation |

### Assumptions

- ANCHOR_DOC selected as Datasheet.md (contains Identification table with Scope Item, Objective, and RFP Authority fields).
- Execution doc ordering: Procedure.md first (has explicit prerequisites table and step-by-step workflow), Specification.md second (has requirements and documentation references), Guidance.md third (has considerations and trade-offs).
- Coordination inputs listed in the Procedure prerequisites table (DEL-01-06, DEL-10-02) are treated as DOWNSTREAM INTERFACE edges because DEL-03-02 produces content that must be consistent with them, and Procedure Step 4 directs cross-checking from DEL-03-02 outward.
- DEL-03-01 is classified as DOWNSTREAM because Procedure Step 4 directs sharing the DEL-03-02 draft with the Architect for consistency check against DEL-03-01.
- DEL-01-01 compliance matrix update (Procedure Step 6) is classified as DOWNSTREAM HANDOVER because DEL-03-02 completion produces a status signal consumed by DEL-01-01.

### Warnings

- None.

### Quality Check Results

| Check | Result |
|---|---|
| Required columns present and CSV parseable | PASS |
| DependencyID unique within file | PASS (18 unique IDs) |
| All ACTIVE rows have EvidenceFile and SourceRef | PASS |
| Status and SatisfactionStatus values canonical | PASS |
| _DEPENDENCIES.md counts match CSV | PASS (18 ACTIVE, 0 RETIRED) |
| No obvious duplicate extracted rows | PASS |
| Parent anchor (IMPLEMENTS_NODE) count | PASS (exactly 1: DEP-03-02-001 -> SOW-0011) |
| Multiple parent anchors | PASS (no ambiguity) |
| Enum normalization | PASS (all write-form canonical) |
| FromDeliverableID consistency | PASS (all rows = DEL-03-02) |
| TargetDeliverableID placement | PASS (non-deliverable targets use TargetRefID/TargetName only) |

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 18 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 18 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 18 |

| DependencyClass | ACTIVE Count |
|---|---|
| ANCHOR | 3 |
| EXECUTION | 15 |

| Direction | ACTIVE Count |
|---|---|
| UPSTREAM | 14 |
| DOWNSTREAM | 4 |
