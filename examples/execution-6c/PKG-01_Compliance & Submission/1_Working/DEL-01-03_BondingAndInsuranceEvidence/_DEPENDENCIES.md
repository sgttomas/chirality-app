# Dependencies: DEL-01-03 BondingAndInsuranceEvidence

## Dependency Tracking Mode
- **Mode:** TRACKED (agent-managed)
- **Register:** Dependencies.csv (schema version v3.1)
- **Notes:** Overwritten from NOT_TRACKED stub by DEPENDENCIES agent run (2026-02-18). Declared sections preserved below; extracted register added.

---

## Upstream (I need these before I can proceed)

- RFP §5.3.1 — Governing requirements document; defines bond types, amounts, format, and insurance requirements (location TBD — PDF not yet accessible).
- DEL-05-01 (AppendixH_ScheduleA_PricingSummary) — Pricing development must be underway so that the anticipated contract value range is available for surety capacity confirmation and bond cost roll-up verification.
- DEL-05-02 (AppendixH_ScheduleB_CostBreakdown) — Bond cost line item in Schedule B must be available for cross-document reconciliation (REQ-07).

## Downstream (These need me)

- DEL-01-01 (ComplianceMatrixAndChecklist) — Agreement to Bond must be listed on the compliance matrix as a mandatory item; compliance matrix references page/section location in final proposal PDF.
- DEL-01-02 (FormalSubmissionPackage) — All three components of DEL-01-03 must be integrated into the formal submission package in the correct location.
- DEL-05-02 (AppendixH_ScheduleB_CostBreakdown) — Receives the final bond cost figure from DEL-01-03 for inclusion as a line item in Schedule B.
- DEL-05-03 (PricingNarrativeAndAssumptions) — Bond cost inclusion statement may be integrated into pricing narrative (conditional on DEL-05-03 being produced).

---

## Extracted Dependency Register

**Total ACTIVE rows:** 11
**Total RETIRED rows:** 0

| DependencyID | Class | AnchorType | Dir | Type | TargetType | TargetRefID / TargetDeliverableID | TargetName | Confidence | SatisfactionStatus |
|---|---|---|---|---|---|---|---|---|---|
| DEP-01-03-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | PACKAGE | PKG-01 | Compliance & Submission | HIGH | TBD |
| DEP-01-03-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-004 | Agreement to Bond + bond inclusion | HIGH | TBD |
| DEP-01-03-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-001 | Pass all mandatory requirements | HIGH | TBD |
| DEP-01-03-004 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-007 | Produce a competitive compliant price package | HIGH | TBD |
| DEP-01-03-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | RFP-5.3.1 | RFP §5.3.1 (Agreement to Bond requirements) | HIGH | PENDING |
| DEP-01-03-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-01 | AppendixH_ScheduleA_PricingSummary | HIGH | PENDING |
| DEP-01-03-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-02 | AppendixH_ScheduleB_CostBreakdown | HIGH | PENDING |
| DEP-01-03-008 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-01 | ComplianceMatrixAndChecklist | HIGH | PENDING |
| DEP-01-03-009 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 | FormalSubmissionPackage | HIGH | PENDING |
| DEP-01-03-010 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-02 | AppendixH_ScheduleB_CostBreakdown | HIGH | PENDING |
| DEP-01-03-011 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-03 | PricingNarrativeAndAssumptions | MEDIUM | PENDING |

---

## Lifecycle Summary

| Dimension | Count |
|---|---|
| ACTIVE rows (total) | 11 |
| RETIRED rows | 0 |
| ANCHOR rows (ACTIVE) | 4 |
| EXECUTION rows (ACTIVE) | 7 |
| UPSTREAM rows (ACTIVE) | 6 |
| DOWNSTREAM rows (ACTIVE) | 5 |
| SatisfactionStatus = TBD | 4 |
| SatisfactionStatus = PENDING | 7 |
| SatisfactionStatus = SATISFIED | 0 |
| Confidence = HIGH | 10 |
| Confidence = MEDIUM | 1 |

**Tree integrity:** 1 ACTIVE IMPLEMENTS_NODE anchor (DEP-01-03-001). No FLOATING_NODE or AMBIGUOUS_ANCHOR warnings.

---

## Run Notes

**Run date:** 2026-02-18
**Mode:** UPDATE (overwrite)
**Strictness:** CONSERVATIVE
**Schema version written:** v3.1
**Consumer context:** NONE (EstimateImpactClass and ConsumerHint populated in Notes column as advisory)

**Source documents scanned:**
- `Datasheet.md` — ANCHOR_DOC (primary anchor/traceability signals)
- `Specification.md` — EXECUTION_DOC (requirements, interfaces, REQ-07 cross-document consistency)
- `Guidance.md` — EXECUTION_DOC (principles, considerations, downstream handoffs)
- `Procedure.md` — EXECUTION_DOC (prerequisites, reference materials, traceability and handoffs)
- `_CONTEXT.md` — ANCHOR_DOC supplement (deliverable identity, scope traceability)
- `_REFERENCES.md` — Reference pointer resolution
- `_SEMANTIC.md` — Scanned; no additional dependency signals extracted (semantic algebra matrices; no explicit information flow edges)

**Decomposition path used:**
`/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
Status: FOUND and read. Used to validate anchor IDs (PKG-01, SOW-004, OBJ-001, OBJ-007) and resolve deliverable names/package assignments.

**Defaults applied:**
- ANCHOR_DOC: `Datasheet.md` (matched ANCHOR_DOC heuristic; confirmed by `_CONTEXT.md` decomposition references)
- EXECUTION_DOC_ORDER: `Specification.md`, `Guidance.md`, `Procedure.md` (matched EXECUTION_DOC heuristic)

**Key extraction decisions:**
- DEP-01-03-007 and DEP-01-03-010 both reference DEL-05-02 but in opposite directions: DEP-01-03-007 is UPSTREAM INTERFACE (DEL-01-03 requires Schedule B figures for reconciliation); DEP-01-03-010 is DOWNSTREAM HANDOVER (DEL-01-03 provides the bond cost figure TO Schedule B). These are distinct, non-duplicate edges representing a genuine bidirectional information exchange explicitly described in sources.
- RFP §5.3.1 registered as UPSTREAM CONSTRAINT (DOCUMENT) because it is explicitly named as the governing requirement that DEL-01-03 must satisfy; content is TBD due to PDF access failure. Marked BLOCKING in Notes.
- DEP-01-03-011 (DEL-05-03) assigned Confidence=MEDIUM due to conditional ("if DEL-05-03 is produced") language in source.
- No COORDINATION-only edges emitted. "Align with" language was not used as sole basis for any row.

**Warnings:**
- [INFO] RFP §5.3.1 content (bond amounts, insurance types, format requirements) is TBD — PDF was not accessible during document production. All rows referencing §5.3.1 requirements carry SatisfactionStatus=PENDING. Bond amounts and insurance minimums remain unknown until §5.3.1 is extracted.

---

## Run History

| Run Date | Mode | Strictness | Decomposition Status | ACTIVE Rows | Warnings |
|---|---|---|---|---|---|
| 2026-02-18 | UPDATE | CONSERVATIVE | FOUND (`Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`) | 11 | [INFO] RFP §5.3.1 content TBD (PDF not accessible) |

---

## Downstream Handoff Notes

*(Consumer context was NONE for this run. No downstream handoff notes required.)*
