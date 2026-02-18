# Dependencies

**Deliverable ID:** DEL-10-01
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here. Extracted dependencies are maintained in Dependencies.csv.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 12
**Total RETIRED rows:** 0

| Class | Count |
|-------|-------|
| ANCHOR | 2 |
| EXECUTION | 10 |

### ANCHOR Rows (ACTIVE)

| DependencyID | AnchorType | TargetType | TargetName | Confidence |
|-------------|------------|------------|------------|------------|
| DEP-10-01-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0028 -- Risk register & mitigations | HIGH |
| DEP-10-01-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-008 -- Manage risk and unknowns transparently | HIGH |

### EXECUTION Rows (ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence |
|-------------|-----------|---------------|------------|------------|------------|
| DEP-10-01-003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-10-02 -- Site Conditions and Due Diligence Summary | HIGH |
| DEP-10-01-004 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-01-06 -- Pricing Narrative and Assumptions | HIGH |
| DEP-10-01-005 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-07-01 -- Construction Methodology Narrative | HIGH |
| DEP-10-01-006 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-09-01 -- Detailed Project Schedule | HIGH |
| DEP-10-01-007 | UPSTREAM | PREREQUISITE | DOCUMENT | Penhold PSB Project Decomposition v2.3 | HIGH |
| DEP-10-01-008 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP 2024_004 (Sections 2-9) | HIGH |
| DEP-10-01-009 | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 03 (Jul 31 2024) | HIGH |
| DEP-10-01-010 | UPSTREAM | CONSTRAINT | DOCUMENT | 2021 Geotechnical Investigation Report | MEDIUM |
| DEP-10-01-011 | UPSTREAM | PREREQUISITE | DOCUMENT | Wetland Assessment and Impact Report | MEDIUM |
| DEP-10-01-012 | UPSTREAM | PREREQUISITE | DOCUMENT | Desktop Environmental Assessment (Ghostpine) | MEDIUM |

---

## Run Notes

### Defaults and Paths Used

- **RUN_ROOT:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL, located as only file in _Decomposition/)
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; identified 4 source documents:
  - Datasheet.md (ANCHOR_DOC -- contains identification, SOW/OBJ traceability, conditions, risk register entries)
  - Procedure.md (EXECUTION_DOC -- contains prerequisites, steps, cross-document consistency checks)
  - Guidance.md (EXECUTION_DOC -- contains principles, considerations, trade-offs)
  - Specification.md (EXECUTION_DOC -- contains requirements, standards, verification, downstream alignment)
- **ANCHOR_DOC:** Datasheet.md (selected: contains SOW Coverage, Objective Alignment, and deliverable identification fields)
- **EXECUTION_DOC_ORDER:** Procedure.md, Guidance.md, Specification.md
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **_REFERENCES.md:** Read; used to confirm DEL-10-02 and DEL-01-06 cross-references

### Assumptions and Decisions

- Parent anchor set to SOW-0028 (the governing scope item explicitly stated in Datasheet). Decomposition confirms SOW-0028 maps to DEL-10-01 under PKG-010.
- OBJ-008 anchor extracted from explicit Objective Alignment field in Datasheet. Decomposition confirms OBJ-008.
- DEL-10-02 dependency classified as UPSTREAM PREREQUISITE because Datasheet explicitly states it "provides site/environmental risk inputs to this register."
- DEL-01-06, DEL-07-01, DEL-09-01 classified as DOWNSTREAM INTERFACE because the risk register produces risk entries that must be reconciled with those deliverables' assumptions and milestones (information flows FROM this deliverable TO those deliverables for consistency alignment).
- Document-level dependencies (RFP, Addenda, reference reports, Decomposition) included as UPSTREAM PREREQUISITE or CONSTRAINT where explicitly stated as required inputs in Procedure prerequisites.
- 2021 Geotechnical Investigation Report classified as CONSTRAINT (not just PREREQUISITE) because DEC-013 explicitly constrains foundation risk assessment to this single report -- it is a binding constraint on the risk register's content.
- Reference reports with "location TBD" status (Geotechnical, Wetland, Environmental) assigned Confidence=MEDIUM due to inaccessibility; their dependency is real but the information transfer is incomplete.
- Coordination-only references to DEL-02-* deliverables in Guidance C-002 were NOT extracted as dependencies because they describe design coordination context, not explicit information/artifact transfer to/from this deliverable.

### Warnings

None.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION |
|-----------|------|-----------|---------------|----------|---------------|-----------------|
| 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (located) | None | 2 | 10 |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 12 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|-------------------|-------|
| TBD | 12 |

---
