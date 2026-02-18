# Dependencies

**Deliverable ID:** DEL-05-04
**Deliverable Name:** Electrical Maintainability
**Package:** PKG-005 -- Building Durability & Maintenance
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here. Extracted dependencies are maintained in `Dependencies.csv` and summarized below.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 8
**Total RETIRED rows:** 0

| Class | Count |
|-------|-------|
| ANCHOR | 2 |
| EXECUTION | 6 |

### ANCHOR Rows (2 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|-------------|------------|------------|--------------------------|------------|
| DEP-05-04-A01 | IMPLEMENTS_NODE | WBS_NODE | SOW-0013 | HIGH |
| DEP-05-04-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-005 | HIGH |

### EXECUTION Rows (6 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement (short) | Confidence |
|-------------|-----------|----------------|------------|--------|-------------------|------------|
| DEP-05-04-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-05 | Conceptual design baseline required before narrative authoring | HIGH |
| DEP-05-04-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-03 | LED/controls/solar-ready decisions affect maintainability | HIGH |
| DEP-05-04-E03 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-03 | Mechanical-electrical interfaces (generator, exhaust, sump pumps) | HIGH |
| DEP-05-04-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-05 | System philosophy from design brief informs maintainability | HIGH |
| DEP-05-04-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-01 | Shared apparatus bay environmental context | MEDIUM |
| DEP-05-04-E06 | DOWNSTREAM | HANDOVER | PACKAGE | PKG-001 | Service contract/spare parts/training costs to pricing | MEDIUM |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located automatically)
- ANCHOR_DOC: `Datasheet.md` (selected by DOC_ROLE_MAP heuristic -- filename contains "datasheet")
- EXECUTION_DOC_ORDER: `Specification.md`, `Procedure.md`, `Guidance.md` (selected by DOC_ROLE_MAP heuristic)
- SOURCE_DOCS (AUTO): Datasheet.md, Specification.md, Procedure.md, Guidance.md (4 source documents scanned)
- _REFERENCES.md: present and used for target resolution

**Decomposition Status:** Available and validated. DEL-05-04 confirmed in decomposition §9 under PKG-005 with SOW-0013 and OBJ-005 linkages verified in §7 (scope ledger) and §6 (objectives).

**Assumptions:**
- No prior Dependencies.csv existed; all rows are newly created.
- Package-level anchor (PKG-005) not extracted as a dependency edge per protocol (structural adjacency from decomposition).

**Warnings:** None.

**Quality Check Results:**
- Schema columns: PASS (all 29 required columns present)
- DependencyID uniqueness: PASS (8 unique IDs)
- ACTIVE rows with evidence: PASS (all 8 rows have EvidenceFile and SourceRef)
- Parent anchor count: PASS (1 IMPLEMENTS_NODE row -- DEP-05-04-A01)
- CSV parseable: PASS
- Enum normalization: PASS (all values canonical)
- _DEPENDENCIES.md vs CSV consistency: PASS (8 ACTIVE, 0 RETIRED matches)

---

## Run History

| Run Date | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Notes |
|----------|------|------------|---------------|----------|---------------|------------------|-------|
| 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (available) | None | 2 | 6 | Initial extraction. 4 source docs scanned. No prior CSV. |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 8 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|-------------------|-------|
| TBD | 8 |
