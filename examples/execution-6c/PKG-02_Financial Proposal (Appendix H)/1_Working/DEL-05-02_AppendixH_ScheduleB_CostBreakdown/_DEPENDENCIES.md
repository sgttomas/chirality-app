# Dependencies: DEL-05-02 AppendixH ScheduleB CostBreakdown

## Dependency Tracking Mode
- **Mode:** TRACKED (DEPENDENCIES agent — Type 2)
- **Notes:** Dependency artifacts managed by DEPENDENCIES agent. Declared lists below are human-owned and preserved.

---

## Upstream (I need these before I can proceed)

- DEL-02-01 (Concept Design Package): Required to extract building GFA, massing, structural system, and major systems for cost estimating (Procedure.md Step 2)
- DEL-05-01 (Schedule A): Reconciliation interface — Schedule B detailed costs must sum to match Schedule A totals (mandatory acceptance criterion)
- DEL-05-03 (Pricing Narrative and Assumptions): Developed in parallel; assumptions and exclusions in Schedule B must be consistent with pricing narrative
- RFP Appendix H Schedule B template: Critical path blocker — template format and structure govern all cost line decisions (must be obtained before Step 1)
- Addendum 03: Scope constraints (pickled sand storage building removed; 12-acre developable site) must be reflected in all line items

## Downstream (These need me)

- DEL-05-01 (Schedule A): Schedule B totals flow to Schedule A summary pricing
- DEL-05-03 (Pricing Narrative and Assumptions): Cost assumptions, exclusions, and allowances must be consistent; pricing narrative references Schedule B structure
- DEL-01-02 (Formal Submission Package): Final Schedule B is delivered to Proposal Manager for integration into the full proposal PDF

---

## Extracted Dependency Register

**Register schema version:** v3.1
**Source file:** `Dependencies.csv`
**Run date:** 2026-02-18
**MODE:** UPDATE | **STRICTNESS:** CONSERVATIVE

### Summary Counts

| Class | Direction | Count (ACTIVE) |
|-------|-----------|----------------|
| ANCHOR | UPSTREAM | 3 |
| EXECUTION | UPSTREAM | 4 |
| EXECUTION | DOWNSTREAM | 3 |
| **TOTAL ACTIVE** | | **10** |
| RETIRED | | 0 |

### Compact Table (ACTIVE rows)

| DependencyID | Class | AnchorType | Dir | Type | TargetType | TargetID / TargetName | Confidence | SatisfactionStatus |
|---|---|---|---|---|---|---|---|---|
| DEP-05-02-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | PKG-02 Financial Proposal (Appendix H) | HIGH | TBD |
| DEP-05-02-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-006 Schedule B complete breakdown | HIGH | TBD |
| DEP-05-02-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-007 Produce a competitive compliant price package | HIGH | TBD |
| DEP-05-02-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 ConceptDesignPackage | HIGH | PENDING |
| DEP-05-02-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-01 AppendixH ScheduleA PricingSummary | HIGH | PENDING |
| DEP-05-02-006 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-01 AppendixH ScheduleA PricingSummary | HIGH | PENDING |
| DEP-05-02-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-03 PricingNarrativeAndAssumptions | MEDIUM | PENDING |
| DEP-05-02-008 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-05-03 PricingNarrativeAndAssumptions | MEDIUM | PENDING |
| DEP-05-02-009 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 FormalSubmissionPackage | HIGH | PENDING |
| DEP-05-02-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Appendix H Schedule B Template | HIGH | PENDING |
| DEP-05-02-011 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | Addendum 03 Scope Changes and Clarifications | HIGH | PENDING |

---

## Run Notes

**Defaults and choices for this run:**

- `RUN_ROOT`: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c`
- `DECOMPOSITION_PATH`: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` — located and read successfully.
- `SOURCE_DOCS`: AUTO — scanned deliverable folder; all present documents read: `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`, `_CONTEXT.md`, `_REFERENCES.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`.
- `DOC_ROLE_MAP`: DEFAULT — `Datasheet.md` and `_CONTEXT.md` treated as ANCHOR_DOC candidates (contain identification, traceability, scope); `Specification.md`, `Guidance.md`, `Procedure.md` treated as EXECUTION_DOC candidates.
- `ANCHOR_DOC`: `_CONTEXT.md` (highest-confidence match for traceability signals: explicit `Scope Traceability` and `Package` fields). Datasheet.md also used for cross-validation.
- `EXECUTION_DOC_ORDER`: `Procedure.md` (primary workflow), `Specification.md` (requirements/interfaces), `Guidance.md` (coordination/principles).
- `MODE`: UPDATE
- `STRICTNESS`: CONSERVATIVE — ANCHOR rows emitted only where identifiers appear explicitly; EXECUTION rows emitted only where source states explicit information/artifact transfer.
- `CONSUMER_CONTEXT`: NONE

**Anchor resolution notes:**
- `PKG-02` confirmed in Decomposition Section 7 as the parent package of DEL-05-02; label "Financial Proposal (Appendix H)" confirmed.
- `SOW-006` confirmed in Decomposition Scope Ledger (Section 10) as mapped to DEL-05-02 with source "App H".
- `OBJ-007` confirmed in Decomposition Section 6; also in Evaluation Criteria crosswalk (Section 15 — 35 points for Proposal Price, primary deliverables DEL-05-01/02/03).
- No ambiguity on parent anchor; single IMPLEMENTS_NODE row emitted (PKG-02).

**Execution dependency notes:**
- DEL-02-01 identified as PREREQUISITE from Procedure.md Prerequisites section (explicit statement). Step 2 describes consuming DEL-02-01 outputs (GFA, massing, structural system) for quantity and cost basis.
- DEL-05-01 has a dual relationship: UPSTREAM INTERFACE (reconciliation requirement — R-005) and DOWNSTREAM HANDOVER (Schedule B totals flow to Schedule A). Both rows retained as they represent distinct information flows.
- DEL-05-03 has a dual relationship: UPSTREAM INTERFACE (develop in parallel; consistency of assumptions) and DOWNSTREAM INTERFACE (Schedule B cost basis informs pricing narrative). Confidence set to MEDIUM because the source states parallel development rather than a strict upstream gate.
- DEL-01-02 identified as DOWNSTREAM HANDOVER from Procedure.md Step 6 (explicit: "Deliver to Proposal Manager for integration into full proposal PDF (per DEL-01-02 submission package)").
- RFP Appendix H template identified as UPSTREAM PREREQUISITE DOCUMENT from Procedure.md (marked CRITICAL PATH BLOCKER in source).
- Addendum 03 identified as UPSTREAM CONSTRAINT DOCUMENT from Specification.md R-007/R-008 and Guidance.md Principle 3 (explicit disqualification risk stated).
- `TargetLocation` for DOCUMENT rows set to `_Sources/` path per `_REFERENCES.md`; actual file locations TBD (files not confirmed present in _Sources/).

**Decisions and exclusions:**
- DEL-05-01 addenda acknowledgement coordination (Specification.md R-006, Lensing B-004): Not extracted as a separate dependency row. The acknowledgement location is TBD (may be on Schedule A, Schedule B, or Appendix H cover). If confirmed on DEL-05-01, a COORDINATION relationship would apply — but coordination-only relationships are excluded per agent instructions. Will be captured if/when source explicitly states an artifact transfer.
- DEL-09-02 (Site Conditions): Referenced in Procedure.md as site reference reports for sitework estimating (item 6). However, Procedure.md marks this as "TBD" with no explicit transfer statement; excluded under CONSERVATIVE strictness.
- No attempt to emit rows for relationships stated only as "keep aligned" or general consistency without specific artifact/data transfer.

**Warnings:**
- None. One IMPLEMENTS_NODE anchor found (no FLOATING_NODE or AMBIGUOUS_ANCHOR condition).

---

## Lifecycle Summary

| Dimension | Count |
|-----------|-------|
| ACTIVE rows | 11 |
| RETIRED rows | 0 |
| ANCHOR / IMPLEMENTS_NODE (ACTIVE) | 1 |
| ANCHOR / TRACES_TO_REQUIREMENT (ACTIVE) | 2 |
| EXECUTION / UPSTREAM (ACTIVE) | 4 |
| EXECUTION / DOWNSTREAM (ACTIVE) | 3 |
| SatisfactionStatus = TBD | 3 |
| SatisfactionStatus = PENDING | 8 |
| SatisfactionStatus = SATISFIED | 0 |

**Tree integrity:** PASS — exactly one ACTIVE IMPLEMENTS_NODE anchor (PKG-02). No FLOATING_NODE. No AMBIGUOUS_ANCHOR.

---

## Run History

| Run # | Timestamp | Mode | Strictness | Decomposition Status | Warnings | ACTIVE Count |
|-------|-----------|------|------------|---------------------|----------|--------------|
| 1 | 2026-02-18 | UPDATE | CONSERVATIVE | Located and read: Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md | None | 11 |
