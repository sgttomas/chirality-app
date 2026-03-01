# DEL-021-05: Dependencies

**Deliverable ID:** DEL-021-05_Warranty
**Dependency Tracking Status:** TRACKED
**Register Schema:** v3.1

## Upstream Dependencies
- **DEL-021-02** (Performance-Bonds): Performance bond must remain in effect during warranty period
- **DEL-021-03** (Insurance): Contractor insurance should remain in effect during warranty
- **DEL-021-04** (Contract-Execution): Contract terms establish warranty period and obligations
- **PKG-020** (Commissioning & Closeout): Substantial completion triggers warranty period start

## Internal Package Dependencies
None identified beyond upstream dependencies.

## External Package Dependencies
None currently identified.

## Cross-Project Dependencies
None currently identified.

## Dependency Notes
Warranty period management begins upon substantial completion (end of PKG-020 activities) and extends for the contract-specified warranty period, typically 1-2 years. Performance bond and insurance may continue during warranty to support remediation activities.

## Monitoring
Warranty period will be monitored through deficiency logs, inspection reports, and remediation completion documentation.

---

## Extracted Dependency Register

**Total rows:** 10
**ACTIVE:** 10 | **RETIRED:** 0

### ANCHOR Dependencies (4 rows)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-021-05-A01 | IMPLEMENTS_NODE | WBS_NODE | PKG-021 -- Bonding Insurance & Warranty | HIGH | ACTIVE |
| DEP-021-05-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0120 | HIGH | ACTIVE |
| DEP-021-05-A03 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0121 | HIGH | ACTIVE |
| DEP-021-05-A04 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-008 | HIGH | ACTIVE |

### EXECUTION Dependencies (6 rows)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Status | EstimateImpactClass |
|---|---|---|---|---|---|---|---|
| DEP-021-05-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-020-02 (Final Inspection & CCC) | HIGH | ACTIVE | BLOCKING |
| DEP-021-05-E02 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-021-02 (Performance & Payment Bonds) | HIGH | ACTIVE | ADVISORY |
| DEP-021-05-E03 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-021-03 (Insurance Package) | HIGH | ACTIVE | ADVISORY |
| DEP-021-05-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-021-04 (CCDC 14-2013 Contract Execution) | HIGH | ACTIVE | BLOCKING |
| DEP-021-05-E05 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-020 (Commissioning & Closeout) | HIGH | ACTIVE | BLOCKING |
| DEP-021-05-E06 | UPSTREAM | INTERFACE | DOCUMENT | AB-2026-01424-WDMLRL RFP.pdf | HIGH | ACTIVE | INFO |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE | 10 |
| RETIRED | 0 |
| **Total** | **10** |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 4 | 0 |
| EXECUTION | 6 | 0 |

### Closure-State Breakdown (EXECUTION rows only)

| SatisfactionStatus | Count |
|---|---|
| PENDING | 6 |
| SATISFIED | 0 |
| WAIVED | 0 |
| IN_PROGRESS | 0 |
| TBD | 0 |

---

## Run Notes

**Run timestamp:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

### Defaults and Paths Used

| Setting | Value | Rationale |
|---|---|---|
| SOURCE_DOCS | AUTO | Scanned deliverable folder; identified Datasheet.md, Guidance.md, Procedure.md, Specification.md |
| ANCHOR_DOC | Datasheet.md | Selected by DOC_ROLE_MAP heuristic (filename contains "datasheet") |
| EXECUTION_DOC_ORDER | Procedure.md, Specification.md, Guidance.md | Procedure first (workflow clarity), then Specification (normative), then Guidance (directional) |
| DECOMPOSITION_PATH | _Decomposition/WDMLRL_Decomposition_Claude.md | Provided by invoker; file found and validated |
| _REFERENCES.md | Present and read | Used for document target resolution (R-01 RFP reference) |

### Assumptions

- No stage metadata found in decomposition; project treated as single stage for dependency direction interpretation.
- All EXECUTION dependencies are UPSTREAM (no DOWNSTREAM handoffs identified in source documents for this deliverable).
- DEP-021-05-E04 (DEL-021-04 interface) classified as BLOCKING for estimating because the CCDC 14-2013 contract may impose additional warranty obligations beyond RFP sections 2.10-2.11, and estimating readiness requires knowledge of the full obligation scope (Specification Standards, Semantic Lensing C-001).
- DEP-021-05-E02 and DEP-021-05-E03 (bonds and insurance) classified as ADVISORY rather than BLOCKING because they constrain warranty administration but do not gate scope or quantity definition for estimating purposes.

### Warnings

None.

### Quality Check Results

- Schema validation: PASS (31 columns, all required columns present)
- DependencyID uniqueness: PASS (10 unique IDs)
- EvidenceFile + SourceRef present: PASS (all ACTIVE rows have both)
- Parent anchor check: PASS (exactly 1 IMPLEMENTS_NODE row: DEP-021-05-A01)
- Enum normalization: PASS (all values are canonical write-form)
- Referential integrity: PASS (FromDeliverableID = DEL-021-05 on all rows)
- CSV parseability: PASS

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | _Decomposition/WDMLRL_Decomposition_Claude.md (found, validated) | None | 4 | 6 | 10 |

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Estimating-Relevant Summary

DEL-021-05 (Guarantee Period Obligations) is a post-construction warranty administration deliverable. Its execution depends entirely on upstream deliverables completing first (CCC issuance, bonds, insurance, contract execution, commissioning/closeout).

**BLOCKING dependencies for estimating (3):**
- **DEP-021-05-E01 (DEL-020-02):** The CCC issuance date determines when the 2-year warranty period begins. Without CCC, the warranty period start date and expiry date cannot be established, and no warranty administration scope can be quantified.
- **DEP-021-05-E04 (DEL-021-04):** The executed CCDC 14-2013 contract may contain warranty clauses beyond the RFP. Until the contract is reviewed, the full obligation scope is not known (Semantic Lensing item C-001). This affects estimating of warranty administration effort.
- **DEP-021-05-E05 (PKG-020):** Substantial completion of commissioning and closeout is the gating event. The commissioning punch list directly informs the initial deficiency set that warranty administration inherits.

**ADVISORY dependencies for estimating (2):**
- **DEP-021-05-E02 (DEL-021-02):** Bond continuation status may affect cost recovery assumptions but does not change the scope of warranty administration work.
- **DEP-021-05-E03 (DEL-021-03):** Insurance continuation status is similar -- affects risk posture but not task scope or quantities.

**INFO dependencies (1):**
- **DEP-021-05-E06 (RFP):** The RFP is the primary normative source and is already accessible. No estimating gate.

### Key Estimating Considerations

- Warranty administration effort is primarily driven by: (a) the number and severity of deficiencies discovered, (b) the inspection cadence adopted, and (c) the duration (fixed at 2 years per RFP section 2.10.2).
- The deficiency volume is not knowable at estimating time; estimating should use parametric or analogous methods based on facility type, construction quality assumptions, and historical data.
- The 10-day rectification timeline (SOW-0121) creates a fixed cadence for administrative follow-up per deficiency event.
