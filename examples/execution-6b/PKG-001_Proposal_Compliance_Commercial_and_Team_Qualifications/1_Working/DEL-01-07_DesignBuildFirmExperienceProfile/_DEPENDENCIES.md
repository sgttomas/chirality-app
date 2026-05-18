# Dependencies

**Deliverable ID:** DEL-01-07
**Deliverable Name:** Design-Build Firm Experience Profile
**Package:** PKG-001 -- Proposal Compliance, Commercial & Team Qualifications
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated in the declared sections above. Only interface-critical dependencies are recorded there. The extracted register below is machine-generated from source document analysis.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 10
**Total RETIRED rows:** 0

| Class | Count |
|---|---|
| ANCHOR | 3 |
| EXECUTION | 7 |

### ANCHOR Dependencies (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-0107-A001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0016 | HIGH |
| DEP-0107-A002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-006 | HIGH |
| DEP-0107-A003 | TRACES_TO_REQUIREMENT | REQUIREMENT | RFP Section 7.1.6 | HIGH |

### EXECUTION Dependencies (7 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-0107-E001 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-09 (Appendix I - Subtrade and Consultant List) | HIGH |
| DEP-0107-E002 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-08 (Key Team Members and Resumes) | HIGH |
| DEP-0107-E003 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 (Formal Submission Package) | HIGH |
| DEP-0107-E004 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP AB-2024-07156 | HIGH |
| DEP-0107-E005 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Addendum 03 | MEDIUM |
| DEP-0107-E006 | UPSTREAM | PREREQUISITE | EXTERNAL | Firm Project Portfolio (Historical Records) | HIGH |
| DEP-0107-E007 | UPSTREAM | PREREQUISITE | EXTERNAL | Client Reference Contacts (Firm CRM) | HIGH |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and paths used:**
- DECOMPOSITION_PATH: `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (located automatically; v2.3 FINAL)
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified 4 source documents: `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md`
- DOC_ROLE_MAP: DEFAULT heuristic applied
  - ANCHOR_DOC: `Datasheet.md` (contains identification, SOW/OBJ references, traceability fields)
  - EXECUTION_DOCS (ordered): `Procedure.md`, `Specification.md`, `Guidance.md`
- _REFERENCES.md: read; contains cross-references to DEL-01-08 and DEL-01-09 (consistent with extracted execution dependencies)
- Existing Dependencies.csv: not present (new file created)

**Extraction notes:**
- Pass 1 (ANCHOR): 3 rows extracted. One parent anchor (SOW-0016 via IMPLEMENTS_NODE), two trace anchors (OBJ-006, RFP Section 7.1.6).
- Pass 2 (EXECUTION): 7 rows extracted. 2 deliverable interfaces (DEL-01-09, DEL-01-08), 1 deliverable handover (DEL-01-02), 2 document prerequisites (RFP, Addendum 03), 2 external prerequisites (firm portfolio, client references).
- Coordination relationships (DEL-01-08/DEL-01-09 consistency) are modeled as INTERFACE rather than pure coordination because the source documents explicitly state data transfer requirements (names must match, firms must appear in Appendix I).
- Guidance P-005 and Specification V-09 both establish explicit cross-document consistency checks that require data from DEL-01-08 and DEL-01-09, confirming these are true information-flow dependencies, not mere coordination.
- The firm project portfolio and client reference contacts are modeled as EXTERNAL PREREQUISITE because they originate outside the deliverable system (firm historical records, CRM). Both are marked PENDING per Procedure Prerequisites status.
- Evaluation criteria (RFP 8.2-8.3) are not modeled as a separate dependency because they are part of the same RFP document already captured in DEP-0107-E004.
- Addendum 03 is modeled as MEDIUM confidence because it is an informational input that shapes content strategy (differentiating experience) rather than a hard gate on deliverable production.

**Warnings:** None.

**Quality check results:**
- Schema check: PASS -- all required columns present; CSV parseable
- DependencyID uniqueness: PASS -- 10 unique IDs
- Evidence check: PASS -- all ACTIVE rows have EvidenceFile and SourceRef populated
- Parent anchor check: PASS -- exactly 1 IMPLEMENTS_NODE row (DEP-0107-A001)
- Enum normalization: PASS -- all values use canonical write-form enums
- Referential integrity: PASS -- FromDeliverableID = DEL-01-07 for all rows
- Target resolution: PASS -- all targets resolved; no UNKNOWN entries
- _DEPENDENCIES.md consistency: PASS -- counts match CSV (3 ANCHOR + 7 EXECUTION = 10 ACTIVE, 0 RETIRED)

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 10 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 10 |
| RETIRED | 0 |

**Closure-state breakdown (ACTIVE rows):**

| SatisfactionStatus | Count |
|---|---|
| TBD | 8 |
| PENDING | 2 |

The 2 PENDING rows are external prerequisites (firm portfolio, client references) whose status is explicitly marked Pending in Procedure.md Prerequisites.
