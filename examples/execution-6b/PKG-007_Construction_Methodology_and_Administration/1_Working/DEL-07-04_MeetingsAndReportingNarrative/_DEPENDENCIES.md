# Dependencies

**Deliverable ID:** DEL-07-04
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Register:** `Dependencies.csv` (RegisterSchemaVersion v3.1)
**Total rows:** 11
**ACTIVE:** 11 | **RETIRED:** 0

### ANCHOR Dependencies (2 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-0704-A001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0022 | HIGH |
| DEP-0704-A002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | HIGH |

### EXECUTION Dependencies -- UPSTREAM (7 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (short) | Confidence |
|---|---|---|---|---|---|
| DEP-0704-E001 | PREREQUISITE | DELIVERABLE | DEL-09-01 (Detailed Project Schedule) | Phasing and milestone data to justify meeting frequency | HIGH |
| DEP-0704-E002 | PREREQUISITE | DELIVERABLE | DEL-07-01 (Construction Methodology) | Construction approach and schedule control context | HIGH |
| DEP-0704-E003 | INTERFACE | DELIVERABLE | DEL-07-02 (Construction Administration) | Document management and reporting coordination | HIGH |
| DEP-0704-E004 | INTERFACE | DELIVERABLE | DEL-07-03 (Subconsultant Approach) | Sub-consultant virtual participation consistency | MEDIUM |
| DEP-0704-E005 | PREREQUISITE | DOCUMENT | RFP Section 7.3.5 (p. 22) | Primary governing requirements for meetings/reporting | HIGH |
| DEP-0704-E006 | CONSTRAINT | DOCUMENT | CCDC 14-2013 + Appendix J | Contract admin framework; specific clauses TBD | MEDIUM |
| DEP-0704-E008 | INTERFACE | DELIVERABLE | DEL-08-01 (Commissioning/Closeout) | Close-out meeting alignment with closeout workflow | MEDIUM |

### EXECUTION Dependencies -- DOWNSTREAM (1 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (short) | Confidence |
|---|---|---|---|---|---|
| DEP-0704-E007 | HANDOVER | DELIVERABLE | DEL-01-02 (Formal Submission Package) | Final narrative handed over for proposal assembly | HIGH |

### EXECUTION Dependencies -- UPSTREAM (continued, 1 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (short) | Confidence |
|---|---|---|---|---|---|
| DEP-0704-E009 | INTERFACE | DELIVERABLE | DEL-08-02 (Deficiencies Management) | Close-out meeting alignment with deficiencies process | MEDIUM |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 11 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 11 |

| DependencyClass | Count |
|---|---|
| ANCHOR | 2 |
| EXECUTION | 9 |

---

## Run Notes

**Run date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE

**Defaults and paths used:**
- DECOMPOSITION_PATH: `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located automatically)
- SOURCE_DOCS: AUTO -- scanned deliverable folder; found 4 source documents: `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
- DOC_ROLE_MAP: DEFAULT heuristic applied
  - ANCHOR_DOC: `Datasheet.md` (contains definition/traceability signals: deliverable ID, scope reference, objective alignment)
  - EXECUTION_DOCS (order): `Procedure.md` (workflow/prerequisites), `Guidance.md` (considerations/interfaces), `Specification.md` (requirements/exclusions)
- _REFERENCES.md: read; confirmed cross-references to DEL-07-02 and DEL-09-01

**Decomposition validation:**
- SOW-0022 confirmed in Decomposition SS10 Scope Ledger: maps to PKG-007 / DEL-07-04 / OBJ-002. PASS.
- OBJ-002 confirmed in Decomposition SS6 Objectives table. PASS.
- All target deliverable IDs (DEL-09-01, DEL-07-01, DEL-07-02, DEL-07-03, DEL-08-01, DEL-08-02, DEL-01-02) confirmed in Decomposition SS9 Deliverables section. PASS.

**Integrity checks:**
- Parent anchor check: 1 ACTIVE IMPLEMENTS_NODE row (DEP-0704-A001). PASS.
- DependencyID uniqueness: 11 unique IDs. PASS.
- All ACTIVE rows have EvidenceFile and SourceRef. PASS.
- Schema columns complete and CSV parseable. PASS.
- No duplicate rows detected. PASS.
- Enum normalization: all values canonical (v3.1). PASS.

**Assumptions logged:**
- DEP-0704-E006 (CCDC 14 constraint): Specific CCDC 14 clauses governing meeting/reporting obligations not yet located (Lensing A-002). Marked ASSUMPTION in row Notes. Satisfaction cannot be verified until clauses are identified.

**Warnings:** None.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 11 |
