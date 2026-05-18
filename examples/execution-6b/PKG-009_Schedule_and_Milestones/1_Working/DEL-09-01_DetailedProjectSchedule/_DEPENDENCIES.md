# Dependencies

**Deliverable ID:** DEL-09-01
**Tracking Mode:** DECLARED (critical dependencies only)

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total Rows:** 11
**ACTIVE:** 11 | **RETIRED:** 0

### ANCHOR Dependencies (2 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-09-01-A001 | IMPLEMENTS_NODE | SOW-0025 | SOW-0025 -- Detailed project schedule | HIGH |
| DEP-09-01-A002 | TRACES_TO_REQUIREMENT | OBJ-009 | OBJ-009 -- Provide a believable, optimized schedule | HIGH |

### EXECUTION Dependencies (9 ACTIVE)

| DependencyID | Direction | Type | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-09-01-E001 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-06-02 (Design Docs Plan) | HIGH |
| DEP-09-01-E002 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-01 (Construction Methodology) | HIGH |
| DEP-09-01-E003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-08-01 (Commissioning/Closeout) | HIGH |
| DEP-09-01-E004 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-10-02 (Site Due Diligence Summary) | MEDIUM |
| DEP-09-01-E005 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Section 7.1.9 | HIGH |
| DEP-09-01-E006 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Section 7.1.8 | HIGH |
| DEP-09-01-E007 | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 03 | HIGH |
| DEP-09-01-E008 | UPSTREAM | PREREQUISITE | DOCUMENT | Site Reference Reports (Appendices D-F) | MEDIUM |
| DEP-09-01-E009 | UPSTREAM | PREREQUISITE | DOCUMENT | CCDC 14-2013 + Appendix J | MEDIUM |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 11 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 8 |
| SATISFIED | 3 |

**Closure note:** Three DOCUMENT dependencies (RFP 7.1.9, RFP 7.1.8, Addendum 03) are marked SATISFIED because the source documents are confirmed available in _Sources/. All deliverable-to-deliverable dependencies remain TBD (dependent deliverables not yet produced). CCDC 14-2013 and Site Reference Reports remain TBD (specific clause text / report content accessibility to be confirmed).

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- DECOMPOSITION_PATH: `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (located; v2.3 FINAL)
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (selected by heuristic)
- SOURCE_DOCS (AUTO): `Datasheet.md`, `Specification.md`, `Procedure.md`, `Guidance.md`
- _REFERENCES.md: present; used for cross-reference validation

**Extraction Decisions:**
- Pass 1 (ANCHOR): One parent anchor (SOW-0025) and one trace anchor (OBJ-009) extracted from Datasheet.md Identification table. Both confirmed against Decomposition v2.3 Scope Ledger (Section 10) and Objectives (Section 6).
- Pass 2 (EXECUTION): Four deliverable-to-deliverable dependencies extracted (DEL-06-02, DEL-07-01, DEL-08-01, DEL-10-02). Five document dependencies extracted (RFP 7.1.9, RFP 7.1.8, Addendum 03, Site Reference Reports, CCDC 14-2013).
- Excluded: DEL-01-08 (key personnel) -- mentioned only as a staffing assumption in Procedure Step 5, not an information/asset transfer. DEL-01-03 (bonding/insurance) -- mentioned only as a contractual assumption in Procedure Step 5, not an information/asset transfer. DEL-08-02 and DEL-08-03 -- referenced in Datasheet Construction (Phase 5) but only as part of the general phase description; no explicit input/output requirement stated for the schedule deliverable itself.
- No DOWNSTREAM dependencies extracted. DEL-09-01 is a terminal proposal artifact (RFP Section 7.1.9 response). No source document for DEL-09-01 states that another deliverable explicitly requires its output.

**Warnings:**
- None.

**Quality Check Results:**
- Schema columns: PASS (all 29 required columns present)
- DependencyID uniqueness: PASS (11 unique IDs)
- EvidenceFile + SourceRef on all ACTIVE rows: PASS
- Parent anchor check: PASS (exactly 1 IMPLEMENTS_NODE row: DEP-09-01-A001)
- Enum normalization: PASS (all values canonical)
- _DEPENDENCIES.md counts match Dependencies.csv: PASS (11 ACTIVE, 0 RETIRED)
- No duplicate rows detected: PASS

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 11 |
