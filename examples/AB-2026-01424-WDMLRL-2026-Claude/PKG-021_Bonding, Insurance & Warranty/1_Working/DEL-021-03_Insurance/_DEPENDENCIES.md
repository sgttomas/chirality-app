# DEL-021-03: Dependencies

**Deliverable ID:** DEL-021-03_Insurance
**Dependency Tracking Status:** TRACKED
**Register Schema Version:** v3.1

## Upstream Dependencies
- **DEL-021-01** (Bid-Security): Insurance program must be designed consistent with bonding strategy
- **DEL-021-02** (Performance-Bonds): Insurance and bonding are complementary risk mitigation

## Internal Package Dependencies
- **DEL-021-04** (Contract-Execution): Insurance documentation must be in place before contract execution

## External Package Dependencies
- **DEL-020-03** (Closeout-Docs): WCB clearance letter produced at closeout; WCB coverage initiated under this deliverable

## Cross-Project Dependencies
None currently identified.

## Dependency Notes
Insurance requirements must be satisfied before contract execution. Coordination between bonding and insurance requirements is important to ensure comprehensive risk coverage and avoid gaps or overlaps.

## Monitoring
Insurance will be monitored through certificate maintenance and periodic coverage verification.

---

## Extracted Dependency Register

**Total rows:** 9 | **ACTIVE:** 9 | **RETIRED:** 0

### ANCHOR Dependencies (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-021-03-001 | IMPLEMENTS_NODE | WBS_NODE | OBJ-008 | OBJ-008 -- Commercial & Legal Compliance | HIGH |
| DEP-021-03-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0102 | SOW-0102 -- Provide insurance coverage per RFP 4.2 | HIGH |
| DEP-021-03-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0103 | SOW-0103 -- Name County as additional insured (except E&O) | HIGH |

### EXECUTION Dependencies (6 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-021-03-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-021-01 Bid Security Package | HIGH | ADVISORY |
| DEP-021-03-005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-021-02 Performance & Payment Bonds | HIGH | ADVISORY |
| DEP-021-03-006 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-021-04 CCDC 14-2013 Contract Execution | HIGH | BLOCKING |
| DEP-021-03-007 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-020-03 Closeout Documentation | MEDIUM | INFO |
| DEP-021-03-008 | UPSTREAM | CONSTRAINT | DOCUMENT | RFP Section 4.2 | HIGH | BLOCKING |
| DEP-021-03-009 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 (insurance provisions) | MEDIUM | BLOCKING |

---

## Lifecycle Summary

| Metric | Count |
|---|---|
| ACTIVE (total) | 9 |
| RETIRED (total) | 0 |
| ANCHOR ACTIVE | 3 |
| EXECUTION ACTIVE | 6 |

### Closure State Breakdown

| SatisfactionStatus | Count |
|---|---|
| TBD | 3 (all ANCHOR rows) |
| PENDING | 6 (all EXECUTION rows) |
| SATISFIED | 0 |

### Estimate Impact Breakdown (EXECUTION rows only)

| EstimateImpactClass | Count |
|---|---|
| BLOCKING | 3 |
| ADVISORY | 2 |
| INFO | 1 |

---

## Run Notes

### Defaults and Paths Used
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **DECOMPOSITION_PATH:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (located and used successfully)
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; identified 4 production documents
- **ANCHOR_DOC:** `Datasheet.md` (selected: contains Identification table with SOW/OBJ links; highest anchor signal)
- **EXECUTION_DOC_ORDER:** `Procedure.md`, `Specification.md`, `Guidance.md`, `Datasheet.md`
- **_REFERENCES.md:** Read for document pointer resolution; used to confirm RFP and CCDC references

### Source Documents Scanned
| Document | Role | Anchor Signal | Execution Signal |
|---|---|---|---|
| Datasheet.md | ANCHOR_DOC (primary) | HIGH (Identification table, Linked SOW/OBJ) | MEDIUM (Construction artifacts, Conditions) |
| Procedure.md | EXECUTION_DOC | LOW | HIGH (Prerequisites, Steps with explicit handoffs) |
| Specification.md | EXECUTION_DOC | MEDIUM (Requirements with source tracing) | HIGH (Scope exclusions naming other DELs, Standards table) |
| Guidance.md | EXECUTION_DOC | LOW | MEDIUM (Principles with cross-DEL references) |

### Extraction Decisions
1. **Parent anchor (DEP-021-03-001):** Anchored to OBJ-008 rather than PKG-021 because OBJ-008 is the explicit objective stated in the Datasheet Identification table and confirmed by the decomposition deliverable table. PKG-021 is the package context (captured in `FromPackageID`), not a separate anchor target.
2. **DEP-021-03-004 (DEL-021-01 PREREQUISITE):** Classified as PREREQUISITE rather than INTERFACE because the source states the insurance program "must be designed consistent with" the bonding strategy -- an explicit input dependency. Classified as ADVISORY for estimating because it informs program design but does not gate insurance procurement.
3. **DEP-021-03-005 (DEL-021-02 INTERFACE):** Classified as INTERFACE because the source states both programs "must be coordinated" and "reviewed together" -- a bidirectional information exchange, not a sequential gate. ADVISORY for estimating.
4. **DEP-021-03-006 (DEL-021-04 PREREQUISITE):** Classified as DOWNSTREAM PREREQUISITE because DEL-021-03 is a hard gate for DEL-021-04 (contract execution). BLOCKING for estimating because contract execution cannot proceed without insurance acceptance.
5. **DEP-021-03-007 (DEL-020-03 HANDOVER):** Classified as DOWNSTREAM HANDOVER because the WCB clearance letter is an artifact that originates from DEL-021-03's WCB coverage and is produced at closeout under DEL-020-03. INFO for estimating because this is a late-stage handover with no scope impact on DEL-021-03 itself.
6. **DEP-021-03-008 (RFP 4.2 CONSTRAINT):** Classified as UPSTREAM CONSTRAINT (DOCUMENT) because RFP 4.2 is the governing requirements source that constrains all insurance coverage decisions. BLOCKING for estimating because scope and quantities cannot be determined without this document.
7. **DEP-021-03-009 (CCDC 14-2013 CONSTRAINT):** Classified as UPSTREAM CONSTRAINT (DOCUMENT) because the contract form may contain supplementary insurance requirements not yet visible. BLOCKING for estimating because inaccessible contract provisions may expand scope.

### Edges Considered but Not Extracted
1. **Contract Award Notification:** Procedure Prerequisites mention contract award as a trigger. This is a scheduling/milestone dependency, not an information-flow edge with a specific artifact transfer. Not extracted per information-flow-only rule.
2. **Alberta WCB / Insurance Act:** Referenced in Specification Standards as governing frameworks. These are regulatory context, not information-flow edges between project entities. Not extracted.
3. **Subcontractor insurance flow-down:** Referenced in multiple documents as an ASSUMPTION. No confirmed information flow or artifact transfer exists -- the ASSUMPTION must be resolved first. Not extracted per CONSERVATIVE strictness.

### Warnings
- None. All quality checks passed.

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | WDMLRL_Decomposition_Claude.md (available) | None | 3 | 6 | 9 |

---

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

### Estimating-Relevant Summary

DEL-021-03 (Insurance Package) has **3 BLOCKING** execution dependencies that affect estimating readiness:

1. **DEP-021-03-006 (DOWNSTREAM to DEL-021-04):** Insurance acceptance is a hard gate for contract execution. Estimating for DEL-021-04 should account for the insurance procurement lead time as a predecessor constraint.

2. **DEP-021-03-008 (UPSTREAM from RFP 4.2):** RFP Section 4.2 is the governing source for all coverage types, limits, and conditions. This document is accessible and has been reviewed -- no estimating blockage on the requirements side. Estimating can proceed using the 10 requirements (REQ-INS-001 through REQ-INS-010) as scope definition.

3. **DEP-021-03-009 (UPSTREAM from CCDC 14-2013):** The CCDC 14-2013 contract form is not yet accessible. It may contain supplementary insurance requirements (e.g., builder's risk / course of construction insurance per GC 11.1) that would expand scope and cost. **Estimating should carry a contingency allowance for potential additional coverage requirements** until the contract is reviewed at DEL-021-04.

### Advisory Dependencies
- DEL-021-01 and DEL-021-02 bonding program outputs inform insurance program design (coverage coordination, gap/overlap review). These are unlikely to change insurance cost totals significantly but may affect policy structure.

### Key Estimating Inputs
- Coverage types and limits are defined by RFP 4.2 (6 coverage lines, 4 with $5M limits)
- Insurance cost is borne entirely by the Proponent (REQ-INS-009)
- No premium estimates available in current source set (Datasheet Estimated Cost = TBD)
- Builder's risk / course of construction insurance status TBD pending CCDC 14-2013 review
