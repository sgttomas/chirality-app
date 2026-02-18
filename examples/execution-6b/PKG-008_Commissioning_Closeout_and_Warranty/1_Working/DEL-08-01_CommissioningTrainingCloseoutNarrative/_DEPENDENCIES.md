# Dependencies

**Deliverable ID:** DEL-08-01
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 14
**Total RETIRED rows:** 0

### ANCHOR Dependencies (2 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-08-01-A001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0023 | HIGH | ACTIVE |
| DEP-08-01-A002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | HIGH | ACTIVE |

### EXECUTION Dependencies (12 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-08-01-E001 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-08-02 (Deficiencies Management Narrative) | HIGH | ACTIVE |
| DEP-08-01-E002 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-08-03 (Warranty Requirements Narrative) | HIGH | ACTIVE |
| DEP-08-01-E003 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-05 (Quality Management Narrative) | HIGH | ACTIVE |
| DEP-08-01-E004 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-01 (Construction Methodology Narrative) | MEDIUM | ACTIVE |
| DEP-08-01-E005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-02 (Construction Administration Narrative) | MEDIUM | ACTIVE |
| DEP-08-01-E006 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-09-01 (Detailed Project Schedule) | HIGH | ACTIVE |
| DEP-08-01-E007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 (Architectural Concept Package) | HIGH | ACTIVE |
| DEP-08-01-E008 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-04 (Mechanical Concept Narrative) | HIGH | ACTIVE |
| DEP-08-01-E009 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-05 (Electrical IT Concept Narrative) | HIGH | ACTIVE |
| DEP-08-01-E010 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-10-02 (Site Conditions and Due Diligence Summary) | HIGH | ACTIVE |
| DEP-08-01-E011 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-06-02 (Detailed Design and Construction Docs Plan) | MEDIUM | ACTIVE |
| DEP-08-01-E012 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP 2024_004 Sections 7.3.6 and 7.5 | HIGH | ACTIVE |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE
**Decomposition Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL)
**Decomposition Status:** Located and used for validation and label resolution.

**Source Documents Scanned (AUTO):**
- ANCHOR_DOC: Datasheet.md (primary anchor/definition signals)
- EXECUTION_DOCS (in order): Procedure.md, Specification.md, Guidance.md
- READ-ONLY: _REFERENCES.md (used for target resolution)

**Defaults Applied:**
- SOURCE_DOCS=AUTO: scanned all .md files in deliverable folder excluding dependency artifacts and generated files.
- DOC_ROLE_MAP=DEFAULT: Datasheet.md selected as ANCHOR_DOC; Procedure.md, Specification.md, Guidance.md as EXECUTION_DOCS.
- ANCHOR_DOC=AUTO: Datasheet.md (contains Identification table with Scope Item and Objective fields).
- EXECUTION_DOC_ORDER=AUTO: Procedure.md (highest workflow clarity), Specification.md, Guidance.md.

**ID Mapping Note (Pass 2):**
- Procedure.md P-004 references "DEL-02-03" for mechanical and "DEL-02-04" for electrical. Per decomposition v2.3, mechanical concept is DEL-02-04 and electrical/IT concept is DEL-02-05. The Procedure.md appears to use a numbering offset (possibly referencing discipline order within PKG-002 rather than canonical IDs). Mapped to correct decomposition IDs: DEL-02-04 (mechanical) and DEL-02-05 (electrical/IT).

**Warnings:** None.

---

## Run History

| Run Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Notes |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (located) | None | 2 | 12 | Initial extraction run. 14 total ACTIVE rows. |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE (total) | 14 |
| RETIRED (total) | 0 |
| ANCHOR -- IMPLEMENTS_NODE | 1 |
| ANCHOR -- TRACES_TO_REQUIREMENT | 1 |
| EXECUTION -- PREREQUISITE | 4 |
| EXECUTION -- INTERFACE | 8 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 14 |

---
