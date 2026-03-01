# DEL-021-02: Dependencies

**Deliverable ID:** DEL-021-02_Performance-Bonds
**Dependency Tracking Status:** TRACKED

## Upstream Dependencies
- **DEL-021-01** (Bid-Security): Surety relationship established through bid bond process facilitates performance bonding

## Internal Package Dependencies
- **DEL-021-03** (Insurance): Insurance and bonding are complementary risk mitigation measures
- **DEL-021-04** (Contract-Execution): Performance and payment bonds must be in place before contract execution

## External Package Dependencies
None currently identified.

## Cross-Project Dependencies
None currently identified.

## Dependency Notes
Performance and payment bonds must be executed following contract award but before contract execution. Surety relationship established through bid security process typically continues for performance bonding, streamlining the process.

## Monitoring
Bonds will be monitored through contract documentation and periodic surety verification.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total rows:** 10
**ACTIVE:** 10 | **RETIRED:** 0

### ANCHOR Edges (4 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-021-02-001 | IMPLEMENTS_NODE | WBS_NODE | OBJ-008 | Commercial & Legal Compliance | HIGH |
| DEP-021-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0099 | Provide 50% Performance Bond upon contract execution | HIGH |
| DEP-021-02-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0100 | Provide 50% L&M Payment Bond upon contract execution | HIGH |
| DEP-021-02-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0101 | Provide bonding within 10 days of award notification | HIGH |

### EXECUTION Edges (6 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-021-02-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-021-01 (Bid Security Package) | HIGH | BLOCKING |
| DEP-021-02-006 | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-021-04 (CCDC 14-2013 Contract Execution) | HIGH | BLOCKING |
| DEP-021-02-007 | UPSTREAM | PREREQUISITE | EXTERNAL | Contract Award Notification | HIGH | BLOCKING |
| DEP-021-02-008 | UPSTREAM | CONSTRAINT | DOCUMENT | RFP Section 2.12 (Surety Bonding) | HIGH | INFO |
| DEP-021-02-009 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 Contract | MEDIUM | ADVISORY |
| DEP-021-02-010 | UPSTREAM | PREREQUISITE | EXTERNAL | Confirmed Contract Price | HIGH | BLOCKING |

---

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING

### Paths and Defaults Used

| Setting | Value | Source |
|---|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude | Provided by invoker |
| DECOMPOSITION_PATH | _Decomposition/WDMLRL_Decomposition_Claude.md | Provided by invoker; file located and validated |
| SOURCE_DOCS | AUTO: Datasheet.md, Guidance.md, Procedure.md, Specification.md | Scanned deliverable folder; excluded dependency artifacts and metadata files |
| ANCHOR_DOC | Datasheet.md | AUTO heuristic: filename contains 'datasheet'; highest anchor-signal match |
| EXECUTION_DOC_ORDER | Procedure.md, Guidance.md, Specification.md | AUTO heuristic: 'procedure' ranked first, then 'guidance', then 'spec' |
| _REFERENCES.md | Present and read; used for document pointer resolution | Deliverable-local |

### Decomposition Validation

Decomposition file located at `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25).
- DEL-021-02 confirmed in decomposition (PKG-021, line 577)
- OBJ-008 confirmed (line 309)
- SOW-0099, SOW-0100, SOW-0101 confirmed in scope ledger (lines 692-694), all mapped to DEL-021-02
- DEL-021-01 confirmed as sibling deliverable in PKG-021 (line 576)
- DEL-021-04 confirmed as sibling deliverable in PKG-021 (line 579)

### Extraction Decisions

1. **DEL-021-03 (Insurance) NOT extracted as EXECUTION dependency.** The declared internal package dependency notes that insurance and bonding are "complementary risk mitigation measures," but no explicit data/artifact transfer is stated between DEL-021-02 and DEL-021-03. Per the information-flow-only model, this is structural adjacency / coordination, not a dependency edge. The declared relationship is preserved in the upstream human-owned section above.

2. **RFP section number discrepancy noted.** _CONTEXT.md and _REFERENCES.md cite "RFP §2.10" while all four production documents consistently reference "RFP §2.12." See Guidance Conflict Table CON-021-02-03. Dependencies extracted using §2.12 as the production-document-consistent reference. This agent does not modify _CONTEXT.md or _REFERENCES.md.

3. **Contract Award Notification and Confirmed Contract Price extracted as EXTERNAL targets.** These are data/artifact inputs from outside the deliverable/package structure. They are not deliverables in the decomposition but are explicitly stated prerequisites in the Procedure.

### Warnings

None.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | Located: WDMLRL_Decomposition_Claude.md | None | 4 | 6 | 10 |

---

## Lifecycle Summary

| Metric | Count |
|---|---|
| Total rows | 10 |
| ACTIVE | 10 |
| RETIRED | 0 |
| ANCHOR rows (ACTIVE) | 4 |
| EXECUTION rows (ACTIVE) | 6 |

### Closure Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 6 |
| PENDING | 4 |

### Parent Anchor Check

- IMPLEMENTS_NODE count (ACTIVE): **1** (DEP-021-02-001 -> OBJ-008)
- Status: PASS (exactly one parent anchor)

---

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

### Estimating-Relevant Summary

DEL-021-02 has **4 BLOCKING execution dependencies** that directly affect estimating readiness:

1. **DEP-021-02-005 (DEL-021-01 Bid Security):** The surety relationship must be established at bid. If Consent of Surety was not obtained, performance bond procurement is blocked. For estimating: the cost of surety engagement (premium) is a function of the project value and surety market conditions. This dependency gates whether the surety channel is available.

2. **DEP-021-02-007 (Contract Award Notification):** The 10-day bond delivery clock starts at award notification. For estimating: this is a pure schedule gate. No bond costs can be finalized or committed until award is received.

3. **DEP-021-02-010 (Confirmed Contract Price):** Bond amounts are 50% of Contract price each. For estimating: the absolute bond amounts (and therefore the bond premium) cannot be calculated until the contract price is confirmed. This is the primary quantity driver for bond cost.

4. **DEP-021-02-006 (DEL-021-04 Contract Execution):** DEL-021-02 produces bonds consumed by DEL-021-04. For estimating: this is a downstream gate -- DEL-021-04 cannot be estimated as complete until DEL-021-02 is satisfied.

**ADVISORY dependency:**
- **DEP-021-02-009 (CCDC 14-2013):** Bond form compatibility with CCDC 14-2013 may affect form selection and surety process but is unlikely to change total bond costs significantly.

**Key estimating unknowns (TBD items from source documents):**
- Contract Price (drives bond face amounts and premium)
- Surety Company Identity (affects premium rate)
- Bond Form Standard (CCDC A312 assumed but not confirmed)
- Bond Duration/Maintenance obligations (may affect ongoing costs)
