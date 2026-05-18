# Dependencies

**Deliverable ID:** DEL-04-03
**Deliverable Name:** Electrical Energy Efficiency
**Package:** PKG-004 -- Sustainability & Energy
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 12
**Total RETIRED rows:** 0

| Class | Count |
|---|---|
| ANCHOR | 3 |
| EXECUTION | 9 |

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-04-03-A001 | IMPLEMENTS_NODE | WBS_NODE | PKG-004 -- Sustainability & Energy | HIGH |
| DEP-04-03-A002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 -- Deliver a strong Design Brief (5 pts) | HIGH |
| DEP-04-03-A003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0012 -- Sustainability/energy narrative | HIGH |

### EXECUTION Rows (9 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-04-03-E001 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-05 (Electrical/IT Concept) | HIGH |
| DEP-04-03-E002 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-01 (Building Envelope) | HIGH |
| DEP-04-03-E003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-02 (Mechanical Energy) | HIGH |
| DEP-04-03-E004 | UPSTREAM | PREREQUISITE | DOCUMENT | Functional Program (Appendix B) | HIGH |
| DEP-04-03-E005 | UPSTREAM | PREREQUISITE | DOCUMENT | OSR (Appendix A) | HIGH |
| DEP-04-03-E006 | UPSTREAM | CONSTRAINT | DOCUMENT | Addendum 03 (Jul 31 2024) | HIGH |
| DEP-04-03-E007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-04 (Mechanical Concept) | MEDIUM |
| DEP-04-03-E008 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-05 (Electrical/IT Concept) | HIGH |
| DEP-04-03-E009 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-03 (Structural Design Brief) | MEDIUM |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 12 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 12 |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Decomposition Path:** `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL)
**Decomposition Status:** Available and used for anchor validation and target resolution.

**Source Documents Scanned (AUTO):**
- `Datasheet.md` (ANCHOR_DOC -- primary anchor/traceability source)
- `Procedure.md` (EXECUTION_DOC -- primary execution dependency source)
- `Specification.md` (EXECUTION_DOC -- requirements and cross-references)
- `Guidance.md` (EXECUTION_DOC -- design principles and considerations)
- `_REFERENCES.md` (read-only reference resolution)
- `_CONTEXT.md` (read-only context)

**ANCHOR_DOC:** `Datasheet.md` (selected by heuristic: contains `datasheet` in filename)
**EXECUTION_DOC_ORDER:** `Procedure.md`, `Specification.md`, `Guidance.md`

**Defaults Applied:**
- SOURCE_DOCS: AUTO (all .md files in deliverable folder excluding dependency artifacts and generated files)
- DOC_ROLE_MAP: DEFAULT
- ANCHOR_DOC: AUTO (Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (Procedure.md > Specification.md > Guidance.md)

**Warnings:** None.

**Integrity Check Results:**
- Parent anchor (IMPLEMENTS_NODE): 1 found (DEP-04-03-A001 -> PKG-004). PASS.
- Schema validation: All required columns present. PASS.
- Evidence completeness: All ACTIVE rows have EvidenceFile and SourceRef. PASS.
- DependencyID uniqueness: All 12 IDs unique. PASS.
- Enum normalization: All enums in canonical write form. PASS.
- Referential integrity: FromDeliverableID = DEL-04-03 on all rows. PASS.

**Extraction Notes:**
- DEL-02-05 appears in both UPSTREAM (E001, as prerequisite input) and DOWNSTREAM (E008, as interface consumer). This is a bidirectional relationship: DEL-04-03 requires draft inputs from DEL-02-05 and also produces narrative content (solar provisions, metering architecture, lighting controls) that DEL-02-05 must incorporate into drawings/schematics.
- DEL-02-04 (Mechanical Concept, PKG-002) is referenced in the Datasheet for generator electrical interface details. This is an INTERFACE dependency, not a formal prerequisite gate like DEL-04-02.
- DEL-03-03 (Structural Design Brief, PKG-003) is explicitly named in Procedure Step 4.2 for roof structural capacity confirmation for the solar inverter pad. Classified as INTERFACE (specific data point, not a formal prerequisite gate).
- Addendum 03 is classified as CONSTRAINT rather than PREREQUISITE because it imposes mandatory compliance requirements (solar-ready provisions) rather than serving as a production input.
- Functional Program (Appendix B) and OSR (Appendix A) are classified as DOCUMENT prerequisites because they are RFP appendices required as source inputs, not deliverables within the project decomposition.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3) | None | 3 | 9 | 12 |
