# Dependencies: DEL-07-03 Appendix I - Subtrade and Consultant List

## Dependency Tracking Mode
- **Mode:** TRACKED (agent-managed; overrides prior NOT_TRACKED declaration as of 2026-02-18 run)
- **Notes:** Prior file declared NOT_TRACKED (human-coordinated). This run establishes the machine-tracked register per DEPENDENCIES agent protocol. Human-declared sections below are preserved; extracted register sections are appended.

---

## Upstream (I need these before I can proceed)

<!-- Human-declared section — do not remove or rename -->

- **DEL-05-02** (Appendix H Schedule B Cost Breakdown, PKG-02): Required to cross-check scopes in the team list against priced scopes. Status: TBD / coordinated externally.
- **DEL-02-01** (Concept Design Package, PKG-04): Informs which specialty consultants and trades are required (e.g., solar-capable roof, overhead door systems, fire apparatus exhaust). Status: TBD / coordinated externally.
- **RFP Appendix I Template** (from RFP PDF in `_Sources/`): Defines required table fields; must be extracted before formatting. Status: TBD / not yet accessible in deliverable folder.
- **Addendum 03** (in `_Sources/`): Scope clarifications (pickled sand building removed; technical systems included) must be integrated. Status: Accessible (satisfied).

---

## Downstream (These need me)

<!-- Human-declared section — do not remove or rename -->

- **DEL-01-01** (Compliance Matrix and Checklist, PKG-01): Appendix I completion is checked as a mandatory compliance item (Constraint C-06).
- **DEL-01-02** (Formal Submission Package, PKG-01): Approved Appendix I is embedded in the final proposal PDF.
- **DEL-07-01** (Design-Build Firm Experience Profile, PKG-03): Firms listed in Appendix I must be profiled in the firm experience narrative; cross-reference consistency required.
- **DEL-07-02** (Key Team Members and Resumes, PKG-03): Personnel named in Appendix I must have corresponding resumes; cross-reference consistency required.

---

## Extracted Dependency Register

**Total rows (ACTIVE):** 12
**Total rows (RETIRED):** 0
**Schema version:** v3.1

| DependencyID | Class | AnchorType | Direction | DependencyType | TargetType | TargetRefID / TargetDeliverableID | TargetName | Confidence | SatisfactionStatus | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| DEP-07-03-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | PACKAGE | PKG-03 | PKG-03 Team Qualifications (Appendix I + resumes) | HIGH | TBD | ACTIVE |
| DEP-07-03-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-007 | SOW-007 Complete Appendix I list of subtrades / DB team | HIGH | TBD | ACTIVE |
| DEP-07-03-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-006 | OBJ-006 Demonstrate a strong team and firms | HIGH | TBD | ACTIVE |
| DEP-07-03-004 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | C-06 | C-06 Design-Build team list (Hard Constraint) | HIGH | TBD | ACTIVE |
| DEP-07-03-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-02 | DEL-05-02 Appendix H Schedule B Cost Breakdown | HIGH | PENDING | ACTIVE |
| DEP-07-03-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 | DEL-02-01 Concept Design Package | MEDIUM | PENDING | ACTIVE |
| DEP-07-03-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | RFP-AppI | RFP Appendix I Template | HIGH | PENDING | ACTIVE |
| DEP-07-03-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum03 | Addendum 03 (scope clarifications) | HIGH | SATISFIED | ACTIVE |
| DEP-07-03-009 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-01 | DEL-01-01 Compliance Matrix and Checklist | HIGH | PENDING | ACTIVE |
| DEP-07-03-010 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 | DEL-01-02 Formal Submission Package | HIGH | PENDING | ACTIVE |
| DEP-07-03-011 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-07-01 | DEL-07-01 Design-Build Firm Experience Profile | HIGH | PENDING | ACTIVE |
| DEP-07-03-012 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-07-02 | DEL-07-02 Key Team Members and Resumes | HIGH | PENDING | ACTIVE |

---

## Lifecycle Summary

| Dimension | Count |
|---|---|
| ACTIVE rows (total) | 12 |
| RETIRED rows (total) | 0 |
| ANCHOR / ACTIVE | 4 |
| EXECUTION / ACTIVE | 8 |
| UPSTREAM / ACTIVE | 8 |
| DOWNSTREAM / ACTIVE | 4 |
| SatisfactionStatus = TBD | 4 |
| SatisfactionStatus = PENDING | 7 |
| SatisfactionStatus = SATISFIED | 1 |

**Parent anchor (IMPLEMENTS_NODE) count:** 1 — integrity check PASS.

---

## Run Notes

**Run date:** 2026-02-18
**Mode:** UPDATE
**STRICTNESS:** CONSERVATIVE
**CONSUMER_CONTEXT:** NONE

**Paths used:**
- Deliverable path: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-03_Team Qualifications (Appendix I + resumes)/1_Working/DEL-07-03_AppendixI_SubtradeAndConsultantList/`
- Decomposition path: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` — FOUND and READ successfully.

**Source documents scanned (AUTO):**
- `Datasheet.md` — ANCHOR_DOC (primary anchor signal; contains Identification table and References)
- `Specification.md` — EXECUTION_DOC (requirements, documentation dependencies upstream/downstream)
- `Guidance.md` — EXECUTION_DOC (principles and considerations including cross-deliverable cross-references)
- `Procedure.md` — EXECUTION_DOC (explicit prerequisites, steps, and downstream handover steps)
- `_CONTEXT.md` — read for deliverable identity and scope traceability
- `_REFERENCES.md` — read to resolve document pointers
- `_SEMANTIC.md` — read; no additional dependency signals beyond those in other docs

**Decomposition validation:**
- DEL-07-03 confirmed in Decomposition §8 under PKG-03.
- PKG-03 confirmed in Decomposition §7.
- SOW-007 confirmed in Decomposition §9 and §10 Scope Ledger (mapped to PKG-03 / DEL-07-03 / OBJ-006).
- OBJ-006 confirmed in Decomposition §6 ("Demonstrate a strong team & firms: Complete Appendix I + key resumes + relevant experience").
- C-06 confirmed in Decomposition §3 Hard Constraints.
- All target deliverable IDs (DEL-05-02, DEL-02-01, DEL-01-01, DEL-01-02, DEL-07-01, DEL-07-02) confirmed present in Decomposition §8.

**Defaults applied:**
- `SOURCE_DOCS`: AUTO
- `DOC_ROLE_MAP`: DEFAULT
- `ANCHOR_DOC`: AUTO → Datasheet.md selected (contains "datasheet" in filename; strongest identification/traceability signal)
- `EXECUTION_DOC_ORDER`: AUTO → Procedure.md (primary workflow signal), Specification.md, Guidance.md

**Prior file state:**
- `_DEPENDENCIES.md` previously existed with `Mode: NOT_TRACKED`. Declared sections preserved; extracted register sections overwritten per UPDATE mode.
- `Dependencies.csv` did not previously exist (created fresh this run).

**Extraction decisions:**
- DEP-07-03-001: ANCHOR / IMPLEMENTS_NODE to PKG-03. Explicit in Datasheet.md Identification table and confirmed in Decomposition §7/§8. TargetType=PACKAGE (PKG-03 is the parent work package, not a WBS_NODE in the traditional sense; closest match is PACKAGE per schema enums).
- DEP-07-03-002: ANCHOR / TRACES_TO_REQUIREMENT to SOW-007. Explicit in _CONTEXT.md "Scope items: SOW-007" and Decomposition §10 Scope Ledger.
- DEP-07-03-003: ANCHOR / TRACES_TO_REQUIREMENT to OBJ-006. Explicit in _CONTEXT.md "Objectives: OBJ-006" and Decomposition §6.
- DEP-07-03-004: ANCHOR / TRACES_TO_REQUIREMENT to C-06. Explicit in Specification.md REQ-01 citing Decomposition §3 Constraint C-06; decomposition §3 confirms as hard constraint.
- DEP-07-03-005: EXECUTION / PREREQUISITE / UPSTREAM from DEL-05-02. Explicitly stated in Procedure.md Prerequisites and Step 4 as a required cross-check input.
- DEP-07-03-006: EXECUTION / PREREQUISITE / UPSTREAM from DEL-02-01. Explicitly stated in Procedure.md Prerequisites as an upstream dependency; Confidence=MEDIUM because the Procedure notes this is "coordinated externally" and the scope is characterised as informing rather than gating.
- DEP-07-03-007: EXECUTION / PREREQUISITE / UPSTREAM from RFP Appendix I Template. Procedure.md Step 1 explicitly lists this as a required reference material before starting; SatisfactionStatus=PENDING as template is flagged TBD / not accessible.
- DEP-07-03-008: EXECUTION / PREREQUISITE / UPSTREAM from Addendum 03. Procedure.md Prerequisites explicitly lists Addendum 03 as required; status listed as Accessible; SatisfactionStatus=SATISFIED.
- DEP-07-03-009: EXECUTION / HANDOVER / DOWNSTREAM to DEL-01-01. Procedure.md Step 10 and Specification.md Downstream Documentation explicitly require completion confirmation handed to DEL-01-01.
- DEP-07-03-010: EXECUTION / HANDOVER / DOWNSTREAM to DEL-01-02. Procedure.md Step 9 explicitly states Appendix I is embedded in the final proposal PDF (DEL-01-02).
- DEP-07-03-011: EXECUTION / INTERFACE / DOWNSTREAM to DEL-07-01. Specification.md REQ-08 and Downstream Documentation require firms in Appendix I to be profiled in DEL-07-01; bidirectional consistency required.
- DEP-07-03-012: EXECUTION / INTERFACE / DOWNSTREAM to DEL-07-02. Specification.md REQ-08 and Downstream Documentation require personnel in Appendix I to have resumes in DEL-07-02; bidirectional consistency required.

**Signals NOT extracted (conservative exclusions):**
- "Functional Program (Appendix B)" referenced in Procedure.md Prerequisites: listed as TBD / not accessible; no stable ID resolvable from decomposition; not emitted as a row — recorded here as awareness item for human follow-up.
- General coordination statements (e.g., "Proposal Manager to coordinate with Lead Architect"): coordination-only, no specific artifact transfer.
- Decomposition §15 evaluation criteria crosswalk: structural context, not an information-flow edge.

**Quality checks:**
- Schema: all required columns present. CSV parseable.
- DependencyID uniqueness: all 12 IDs unique within file.
- EvidenceFile + SourceRef: present on all ACTIVE rows.
- Status enum: all ACTIVE — canonical.
- SatisfactionStatus enum: TBD / PENDING / SATISFIED — all canonical.
- IMPLEMENTS_NODE count (ACTIVE): 1 — PASS (no FLOATING_NODE, no AMBIGUOUS_ANCHOR warning).
- _DEPENDENCIES.md counts consistent with Dependencies.csv: 12 ACTIVE, 0 RETIRED — PASS.
- No obvious duplicate rows.

**Awareness items (for human follow-up, not blocking):**
- RFP Appendix I Template (DEP-07-03-007): SatisfactionStatus=PENDING. Procedure flags this as requiring human action to extract template from RFP PDF.
- Functional Program (Appendix B): referenced in Procedure.md as a required reference material but no stable decomposition ID exists; not emitted as a dependency row. Human should confirm whether this is accessible and what its scope impact is on discipline categories.

---

## Run History

| Run # | Date | Mode | Strictness | Decomp Status | Warnings | ACTIVE Count | RETIRED Count |
|---|---|---|---|---|---|---|---|
| 1 | 2026-02-18 | UPDATE | CONSERVATIVE | FOUND — Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md | None | 12 | 0 |
