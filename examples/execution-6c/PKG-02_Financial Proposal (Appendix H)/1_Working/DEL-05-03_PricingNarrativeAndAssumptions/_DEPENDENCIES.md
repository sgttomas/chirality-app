# Dependencies: DEL-05-03 PricingNarrativeAndAssumptions

## Dependency Tracking Mode

- **Mode:** TRACKED (upgraded from NOT_TRACKED by DEPENDENCIES agent run 2026-02-18)
- **Notes:** Prior mode was NOT_TRACKED (human-coordinated). This file now contains a machine-extracted register per AGENT_DEPENDENCIES protocol. Human-declared sections below are preserved.

---

## Upstream (I need these before I can proceed)

- DEL-05-01 (Schedule A) — narrative must be consistent with numerical pricing (cross-check required)
- DEL-05-02 (Schedule B) — allowance line items and monitoring fee separation must match narrative
- DEL-02-01 (Concept Design Package) — pricing assumptions must align with building size, structure type, site layout
- DEL-02-02 (Design Brief Narrative) — materials and systems must be consistent with pricing basis
- DEL-04-01 (Construction Methodology Narrative) — construction approach must align with pricing assumptions
- DEL-08-01 (Detailed Project Schedule) — schedule durations and procurement lead times must align
- DEL-09-02 (Site Conditions and Due Diligence Summary) — site condition assumptions reference geotech/wetland/enviro reports
- RFP 2024_004 (Appendix H, §4.2–4.3, §8.5) — governing compliance constraint
- Addendum 03 — primary constraint: exclusions, allowance approach, FF&E treatment, technical requirements

## Downstream (These need me)

- DEL-01-02 (Formal Submission Package) — narrative is integrated into final proposal PDF by Proposal Manager
- DEL-09-01 (Risk Register) — aggressive/uncertain pricing assumptions and allowances feed risk identification

---

## Extracted Dependency Register

**Register schema version:** v3.1
**Run date:** 2026-02-18
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Decomposition path used:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
**Decomposition status:** FOUND AND VALIDATED

### Summary Counts

| Class | Direction | Count (ACTIVE) |
|---|---|---|
| ANCHOR — IMPLEMENTS_NODE | UPSTREAM | 1 |
| ANCHOR — TRACES_TO_REQUIREMENT | UPSTREAM | 2 |
| EXECUTION — INTERFACE | UPSTREAM | 2 |
| EXECUTION — PREREQUISITE | UPSTREAM | 4 |
| EXECUTION — HANDOVER | DOWNSTREAM | 2 |
| EXECUTION — CONSTRAINT | UPSTREAM | 2 |
| **TOTAL ACTIVE** | | **14** |
| RETIRED | | 0 |

### Compact Table

| DependencyID | Class | AnchorType | Dir | Type | TargetType | TargetID / TargetName | Confidence | SatisfactionStatus |
|---|---|---|---|---|---|---|---|---|
| DEP-05-03-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | PKG-02 — Financial Proposal (Appendix H) | HIGH | TBD |
| DEP-05-03-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-007 — Produce a competitive compliant price package | HIGH | TBD |
| DEP-05-03-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-028 — Value alternatives listed separately | HIGH | TBD |
| DEP-05-03-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-01 — Schedule A Pricing Summary | HIGH | PENDING |
| DEP-05-03-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-02 — Schedule B Cost Breakdown | HIGH | PENDING |
| DEP-05-03-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 — Concept Design Package | HIGH | PENDING |
| DEP-05-03-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-02 — Design Brief Narrative | MEDIUM | PENDING |
| DEP-05-03-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-01 — Construction Methodology Narrative | HIGH | PENDING |
| DEP-05-03-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-08-01 — Detailed Project Schedule | HIGH | PENDING |
| DEP-05-03-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-09-02 — Site Conditions and Due Diligence Summary | HIGH | PENDING |
| DEP-05-03-011 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-09-01 — Risk Register and Mitigation Plan | HIGH | PENDING |
| DEP-05-03-012 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 — Formal Submission Package | HIGH | PENDING |
| DEP-05-03-013 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | RFP 2024_004 — Appendix H / §4.2–4.3 / §8.5 | HIGH | PENDING |
| DEP-05-03-014 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | Addendum 03 — Pricing clarifications / scope removals / allowance approach | HIGH | SATISFIED |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 14 |
| RETIRED | 0 |

| SatisfactionStatus | Count (ACTIVE rows) |
|---|---|
| TBD | 3 |
| PENDING | 10 |
| SATISFIED | 1 |
| IN_PROGRESS | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |

**Parent anchor (IMPLEMENTS_NODE) check:** 1 ACTIVE row — PASS.
**Ambiguous anchor check:** No multiple IMPLEMENTS_NODE rows — PASS.

---

## Run Notes

- **SOURCE_DOCS:** AUTO — scanned deliverable folder. Documents read: Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md, _SEMANTIC.md.
- **ANCHOR_DOC:** Datasheet.md (matched heuristic for `datasheet` filename; highest-confidence for ANCHOR signals).
- **EXECUTION_DOC_ORDER:** Procedure.md (primary workflow/execution signals), Specification.md (requirements and boundary conditions), Guidance.md (principles and considerations), _CONTEXT.md (scope traceability).
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` — found and validated.
- **MODE:** UPDATE — prior `_DEPENDENCIES.md` was NOT_TRACKED stub; all rows are new EXTRACTED rows.
- **STRICTNESS:** CONSERVATIVE — anchors emitted only for explicitly stated identifiers; no speculative anchors added.
- **CONSUMER_CONTEXT:** NONE (default).

### Decisions and Defaults

- The deliverable ID `DEL-05-03` was confirmed in decomposition §8.
- Parent package `PKG-02` confirmed as the canonical WBS node in decomposition §7.
- `OBJ-007` confirmed as traced objective in _CONTEXT.md Scope Traceability, confirmed in decomposition §6.
- `SOW-028` confirmed as the primary scope item in _CONTEXT.md Scope Traceability and decomposition §10 scope ledger.
- DEL-05-01 and DEL-05-02 (siblings in PKG-02) are classified as INTERFACE (not PREREQUISITE) because the relationship is bidirectional cross-check for consistency, not a strict one-way gating input.
- DEL-02-01, DEL-02-02, DEL-04-01, DEL-08-01, DEL-09-02 are classified as PREREQUISITE: these are inputs whose content DEL-05-03 pricing assumptions must reflect before narrative can be finalized.
- DEL-09-01 (Risk Register) is DOWNSTREAM HANDOVER: Procedure.md and Guidance explicitly state that pricing risks feed the risk register (information flows from this deliverable to DEL-09-01).
- DEL-01-02 (Final Submission Package) is DOWNSTREAM HANDOVER: Procedure.md Step 7 explicitly states narrative is integrated into the proposal PDF by the Proposal Manager.
- RFP 2024_004 and Addendum 03 are UPSTREAM CONSTRAINT (TargetType=DOCUMENT): they govern the content of this deliverable as compliance/regulatory sources. Addendum 03 SatisfactionStatus set to SATISFIED because it has been integrated into the decomposition (CHG-003) and all requirements trace to it.
- DEL-02-02 set to Confidence=MEDIUM: the cross-check to design brief is stated in Procedure Step 5, but the Specification boundary condition for design brief alignment is marked ASSUMPTION rather than FACT.
- No coordination-only or structural adjacency edges were created. All edges represent explicit information flow or artifact transfer stated in source documents.

### Quality Check Results

- Schema check: PASS — all required columns present; CSV is parseable.
- DependencyID uniqueness: PASS — 14 unique IDs (DEP-05-03-001 through DEP-05-03-014).
- Evidence completeness: PASS — all ACTIVE rows contain EvidenceFile and SourceRef.
- Enum normalization: PASS — all enums use canonical write-form values.
- Parent anchor count: 1 — PASS (no FLOATING_NODE, no AMBIGUOUS_ANCHOR warning).
- Duplicate check: PASS — no duplicate extracted edges detected.
- Count consistency: PASS — 14 rows in CSV (1 header + 14 data); 14 ACTIVE + 0 RETIRED. Breakdown: 3 ANCHOR + 11 EXECUTION. SatisfactionStatus sums to 14 (TBD: 3, PENDING: 10, SATISFIED: 1).

---

## Run History

| Run # | Date | Mode | Strictness | Decomposition Status | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-18 | UPDATE | CONSERVATIVE | FOUND | None | 14 |
