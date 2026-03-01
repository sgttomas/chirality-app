# DEL-019-03: Dependencies

**Deliverable ID:** DEL-019-03_Subcontractor-Mgmt
**Dependency Tracking Status:** TRACKED

## Upstream Dependencies
- **DEL-019-01** (Prime-Contractor): Requires prime contractor authority to manage and coordinate subcontractors
- **DEL-019-02** (Weekly-Coordination): Weekly meetings provide forum for subcontractor coordination and issue resolution
- **DEL-021-03** (Insurance Package): Design-Builder's insurance covering independent subcontractors must be verified before onboarding

## Internal Package Dependencies
- **DEL-019-04** (QC-Management): Quality control activities directly impact subcontractor performance evaluation

## External Package Dependencies
- **DEL-020-03** (Closeout Documentation): WCB clearance letter and Statutory Declaration produced by subcontractor close-out are required closeout inputs
- **PKG-010 through PKG-018** (Construction trade packages): Subcontractor management covers trades performing work across these packages

## Cross-Project Dependencies
None currently identified.

## Dependency Notes
Subcontractor management is subordinate to prime contractor designation and relies on weekly coordination meetings for status updates and issue resolution. Quality control activities provide essential performance feedback that informs subcontractor evaluations. The Design-Builder's insurance (DEL-021-03) must be verified as covering independent subcontractors before any onboarding proceeds. The CCDC 14-2013 contract text (available post-award) and Alberta OH&S/Prompt Payment legislation are external constraints on the subcontractor management framework.

## Monitoring
Dependencies will be monitored through weekly coordination meetings and subcontractor performance reports.

---

## Extracted Dependency Register

**Register Schema Version:** v3.1
**Total Rows:** 13
**ACTIVE:** 13 | **RETIRED:** 0

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-019-03-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0088 -- Manage all subcontractors | HIGH |
| DEP-019-03-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 -- Complete all work on or before December 31 2026 | HIGH |
| DEP-019-03-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-007 -- Maintain safe site operations under Prime Contractor designation | HIGH |

### EXECUTION Edges (10 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-019-03-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-019-01 Prime Contractor Designation & OH&S Program | HIGH | BLOCKING |
| DEP-019-03-005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-019-02 Weekly Meetings & Billing Coordination | HIGH | ADVISORY |
| DEP-019-03-006 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-019-04 Construction Quality Control | HIGH | ADVISORY |
| DEP-019-03-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-021-03 Insurance Package | HIGH | BLOCKING |
| DEP-019-03-008 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 Design-Build Stipulated Price Contract | MEDIUM | BLOCKING |
| DEP-019-03-009 | UPSTREAM | CONSTRAINT | DOCUMENT | AB-2026-01424-WDMLRL RFP.pdf | HIGH | INFO |
| DEP-019-03-010 | DOWNSTREAM | INTERFACE | PACKAGE | PKG-010 through PKG-018 (Construction trade packages) | MEDIUM | ADVISORY |
| DEP-019-03-011 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-020-03 Closeout Documentation | HIGH | ADVISORY |
| DEP-019-03-012 | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta OH&S Act Regulations and Code | MEDIUM | INFO |
| DEP-019-03-013 | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta Prompt Payment and Construction Lien Act | MEDIUM | INFO |

---

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING

### Paths Used
- **RUN_ROOT:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- **DELIVERABLE_PATH:** {RUN_ROOT}/PKG-019_Construction Management & OH&S/1_Working/DEL-019-03_Subcontractor-Mgmt/
- **DECOMPOSITION_PATH:** {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md
- **Decomposition Status:** Available; used for anchor validation and label resolution.

### Source Documents (AUTO-resolved)
- **ANCHOR_DOC:** Datasheet.md (selected: contains `datasheet` in filename; highest-confidence anchor signal with SOW Coverage, Linked Objectives, and Upstream Dependencies fields)
- **EXECUTION_DOC_ORDER:**
  1. Procedure.md (contains `procedure`; strongest execution/prerequisite/workflow signal)
  2. Specification.md (contains `spec`; requirements and standards signal)
  3. Guidance.md (contains `guidance`; considerations and trade-offs signal)

### Read-Only Inputs
- **_REFERENCES.md:** Present; used for document pointer resolution.
- **_CONTEXT.md:** Present; used for deliverable identity and scope verification.
- **_DEPENDENCIES.md (prior):** Present; declared upstream/internal dependencies preserved.

### Defaults Applied
- SOURCE_DOCS=AUTO: Scanned deliverable folder; identified 4 source documents (Datasheet.md, Specification.md, Guidance.md, Procedure.md).
- DOC_ROLE_MAP=DEFAULT: Applied heuristic filename matching.
- ANCHOR_DOC=AUTO: Selected Datasheet.md.
- EXECUTION_DOC_ORDER=AUTO: Ordered as Procedure.md, Specification.md, Guidance.md.

### Assumptions Logged
- DEP-019-03-010: Not all construction trade packages (PKG-010 through PKG-018) necessarily require separate subcontractors; some may be self-performed by the Design-Builder. Marked MEDIUM confidence.

### Warnings
None. All integrity checks passed:
- Parent anchor (IMPLEMENTS_NODE) count: 1 (nominal).
- No duplicate rows detected.
- All ACTIVE rows have EvidenceFile and SourceRef populated.
- All FromDeliverableID values match DEL-019-03.
- DependencyID uniqueness confirmed (13 unique of 13).

---

## Run History

| Timestamp | Mode | Strictness | Consumer Context | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | RETIRED |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | WDMLRL_Decomposition_Claude.md (available) | None | 3 | 10 | 0 |

---

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 13
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown, ACTIVE rows only)
- **TBD:** 5 (DEP-019-03-001, -002, -003, -010, -011)
- **PENDING:** 8 (DEP-019-03-004, -005, -006, -007, -008, -009, -012, -013)
- **SATISFIED:** 0
- **WAIVED:** 0
- **NOT_APPLICABLE:** 0

---

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

### Estimating-Relevant Summary

**BLOCKING dependencies (3):** These gate meaningful estimating for DEL-019-03. Scope or key quantities cannot be fully estimated without resolution.

1. **DEP-019-03-004 (DEL-019-01 Prime Contractor):** Prime Contractor designation is a prerequisite for any subcontractor mobilisation. Estimating for subcontractor management effort requires knowing that PC designation is in place. Not a quantity driver but a gate.
2. **DEP-019-03-007 (DEL-021-03 Insurance Package):** Insurance verification gates onboarding. If insurance is not procured or does not cover subcontractors, the management scope changes. Estimating should confirm insurance procurement is on the critical path.
3. **DEP-019-03-008 (CCDC 14-2013 Contract):** The governing contract text defines subcontractor engagement terms, non-compliance framework, and change order processes. Until contract text is available post-award, the subcontractor contract template and non-compliance procedures remain TBD. Estimating for framework establishment effort is uncertain without this.

**ADVISORY dependencies (4):** These may change quantities, specs, or approach but are not hard gates.

1. **DEP-019-03-005 (DEL-019-02 Weekly Coordination):** The coordination forum is an interface, not a hard gate. Estimating should account for subcontractor management effort at weekly meetings.
2. **DEP-019-03-006 (DEL-019-04 QC Management):** QC feedback feeds performance evaluation. Estimating should account for coordination overhead between QC and subcontractor management.
3. **DEP-019-03-010 (PKG-010 through PKG-018):** The number and type of subcontractors depends on which trade packages are subcontracted vs. self-performed. This is the primary quantity driver for subcontractor management effort. The full list of required subcontracted trades is TBD.
4. **DEP-019-03-011 (DEL-020-03 Closeout Documentation):** WCB clearance and Statutory Declaration are downstream outputs. Estimating should account for closeout administration effort.

**INFO dependencies (3):** Informational context with low likelihood of changing totals.

1. **DEP-019-03-009 (RFP):** Contractual obligations are fixed and known. No estimating uncertainty.
2. **DEP-019-03-012 (Alberta OH&S legislation):** Regulatory framework is fixed. Compliance effort is part of standard Prime Contractor operations.
3. **DEP-019-03-013 (Alberta Prompt Payment Act):** Payment obligations are legislated. Compliance effort is part of standard construction administration.

### Key Estimating Uncertainty
The primary estimating uncertainty for DEL-019-03 is the **number and type of subcontractors** to be managed, which depends on the Design-Builder's self-perform vs. subcontract decisions across PKG-010 through PKG-018 (9 construction trade packages). Until this is resolved, the management effort (qualification, onboarding, monitoring, close-out per subcontractor) cannot be accurately quantified.
