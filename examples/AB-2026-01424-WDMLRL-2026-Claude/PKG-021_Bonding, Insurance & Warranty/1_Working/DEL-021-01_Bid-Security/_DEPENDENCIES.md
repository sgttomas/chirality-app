# DEL-021-01: Dependencies

**Deliverable ID:** DEL-021-01_Bid-Security
**Dependency Tracking Status:** TRACKED
**Register Schema:** v3.1
**Register File:** Dependencies.csv

## Upstream Dependencies
None identified — this deliverable must be completed before bid submission.

## Internal Package Dependencies
- **DEL-021-02** (Performance-Bonds): Performance bond will be required following contract award
- **DEL-021-03** (Insurance): Insurance requirements will complement bonding requirements

## External Package Dependencies
None currently identified.

## Cross-Project Dependencies
None currently identified.

## Dependency Notes
Bid security is a prerequisite deliverable that must be completed and submitted with the bid proposal. Failure to provide required bid security will result in bid rejection. Following contract award, performance bonding will be required under DEL-021-02.

## Monitoring
Bid security will be monitored through bid submission verification and surety confirmation.

---

## Extracted Dependency Register

**Total rows:** 10 | **ACTIVE:** 10 | **RETIRED:** 0

### ANCHOR Rows (4 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-021-01-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-021 — Bonding, Insurance & Warranty | HIGH |
| DEP-021-01-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-008 — Commercial & Legal Compliance | HIGH |
| DEP-021-01-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0097 — Provide 10% bid bond or certified cheque | HIGH |
| DEP-021-01-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0098 — Provide Consent of Surety | HIGH |

### EXECUTION Rows (6 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-021-01-005 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-021-02 — Performance & Payment Bonds | HIGH | ADVISORY |
| DEP-021-01-006 | UPSTREAM | PREREQUISITE | UNKNOWN | Cost Estimate / Bid Amount (Proposal Section 3.0) | HIGH | BLOCKING |
| DEP-021-01-007 | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 1 Section 4.11 | HIGH | INFO |
| DEP-021-01-008 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 Contract | MEDIUM | ADVISORY |
| DEP-021-01-009 | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-021-04 — Contract Execution | HIGH | ADVISORY |
| DEP-021-01-010 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Main Document | HIGH | INFO |

---

## Run Notes

**Run timestamp:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

### Defaults and Paths Used
- **RUN_ROOT:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- **DELIVERABLE_PATH:** {RUN_ROOT}/PKG-021_Bonding, Insurance & Warranty/1_Working/DEL-021-01_Bid-Security/
- **DECOMPOSITION_PATH:** {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md (located, used for validation)
- **SOURCE_DOCS (AUTO):** Datasheet.md, Guidance.md, Procedure.md, Specification.md
- **DOC_ROLE_MAP (DEFAULT):**
  - ANCHOR_DOC: Datasheet.md (matched on "datasheet" keyword)
  - EXECUTION_DOCS: Procedure.md, Guidance.md, Specification.md (matched on "procedure", "guidance", "spec" keywords)
- **ANCHOR_DOC:** Datasheet.md
- **EXECUTION_DOC_ORDER:** Procedure.md, Guidance.md, Specification.md
- **_REFERENCES.md:** Present, used for document pointer resolution

### Assumptions
- ASSUMPTION: Proposal preparation items SOW-0105 through SOW-0119 are excluded from decomposition per decision D-003. The cost estimate / bid amount dependency (DEP-021-01-006) cannot be resolved to a deliverable ID; recorded as TargetType=UNKNOWN.
- ASSUMPTION: DEL-021-03 (Insurance) is referenced in _REFERENCES.md as related documentation but no explicit information-flow dependency was found in source documents. Per CONSERVATIVE strictness, no EXECUTION row was emitted for DEL-021-03 (coordination-only, no specific artifact transfer stated).

### Warnings
- None.

### Integrity Check Results
- Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE row (DEP-021-01-001) -- PASS
- DependencyID uniqueness: 10 unique IDs out of 10 rows -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- Schema version v3.1 on all rows -- PASS
- Enum normalization: all values canonical -- PASS
- FromDeliverableID consistency: all rows = DEL-021-01_Bid-Security -- PASS

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (available, validated) | None | 10 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 10 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 4 |
| PENDING | 4 |
| SATISFIED | 2 |

**Closure notes:**
- 4 ANCHOR rows have SatisfactionStatus=NOT_APPLICABLE (anchors do not require closure).
- 2 DOCUMENT dependencies (DEP-021-01-007, DEP-021-01-010) are marked SATISFIED because the governing documents (Addendum 1, RFP) are accessible and reviewed.
- 4 EXECUTION dependencies remain PENDING: DEL-021-02 handover (awaiting award), cost estimate input (awaiting bid finalization), CCDC 14-2013 compatibility (document not yet reviewed), and DEL-021-04 enablement (awaiting award).

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

The following observations are relevant for downstream task estimating:

1. **BLOCKING dependency (DEP-021-01-006):** The bid bond face value cannot be determined until the cost estimate / bid amount is finalized (Proposal Section 3.0). This is a hard gate on bid bond issuance. Estimating for DEL-021-01 must account for this sequencing constraint. The cost estimate deliverable is not tracked in the project decomposition (excluded per D-003 as pre-contract proposal preparation).

2. **ADVISORY dependencies:**
   - **DEP-021-01-005 (HANDOVER to DEL-021-02):** Surety identity, Consent of Surety, underwriting documentation, and bid amount/contract price must transfer from DEL-021-01 to DEL-021-02 upon award. Estimating for DEL-021-02 should account for this input dependency.
   - **DEP-021-01-008 (CONSTRAINT from CCDC 14-2013):** Consent of Surety form compatibility with CCDC 14-2013 is TBD. If CCDC 14-2013 prescribes a specific form, this could affect surety coordination effort.
   - **DEP-021-01-009 (ENABLES DEL-021-04):** Bid security completion is a precondition for contract execution activation. Estimating for DEL-021-04 should account for this sequencing.

3. **INFO dependencies (DEP-021-01-007, DEP-021-01-010):** Governing documents (Addendum 1, RFP) are accessible and reviewed. No estimating impact.
