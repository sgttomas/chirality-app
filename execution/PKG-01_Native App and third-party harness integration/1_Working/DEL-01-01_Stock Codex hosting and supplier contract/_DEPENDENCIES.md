# Dependencies: DEL-01-01 Stock Codex hosting and supplier contract

## Dependency Tracking Mode
- **Mode:** FULL_GRAPH
- **Register:** the declared sections of this file together with Dependencies.csv (schema v3.1) when present (docs/SPEC.md §5.3)
- **Notes:** `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`; no individual human-declared edge yet. Accepted interface descriptions are sources for later extraction, not declarations inferred by scaffolding.

---

## Declared Upstream (I need these before I can proceed)
- None declared at initial setup.

## Declared Downstream (These need me)
- None declared at initial setup.

---

## Extracted Dependency Register
- **Status:** LOCAL_EXTRACTION_CHECKED
- **Register:** `Dependencies.csv` — v3.1, 29 canonical columns.
- **ACTIVE:** 24 EXTRACTED rows: 15 ANCHOR (1 parent, 14 traces) and 9 EXECUTION (4 upstream, 5 downstream).
- **Targets:** 3 EXTERNAL (1 supplier contribution, 2 internal-project owner decisions external to this unit); 0 UNKNOWN; 6 DELIVERABLE execution rows.
- **Declared mirrors:** 0; both initial-setup placeholders were skipped. No prior CSV existed and no rows were deleted or retired.

| DependencyID | Class / relation | Target | Satisfaction |
|---|---|---|---|
| DEP-01-01-001 | ANCHOR/IMPLEMENTS_NODE | PKG-01 | NOT_APPLICABLE |
| DEP-01-01-002 | ANCHOR/TRACES_TO_REQUIREMENT | SOW-097 | NOT_APPLICABLE |
| DEP-01-01-003 | ANCHOR/TRACES_TO_REQUIREMENT | SOW-099 | NOT_APPLICABLE |
| DEP-01-01-004 | ANCHOR/TRACES_TO_REQUIREMENT | SOW-100 | NOT_APPLICABLE |
| DEP-01-01-005 | ANCHOR/TRACES_TO_REQUIREMENT | SOW-101 | NOT_APPLICABLE |
| DEP-01-01-006 | ANCHOR/TRACES_TO_REQUIREMENT | SOW-118 | NOT_APPLICABLE |
| DEP-01-01-007 | ANCHOR/TRACES_TO_REQUIREMENT | SOW-119 | NOT_APPLICABLE |
| DEP-01-01-008 | ANCHOR/TRACES_TO_REQUIREMENT | SOW-121 | NOT_APPLICABLE |
| DEP-01-01-009 | ANCHOR/TRACES_TO_REQUIREMENT | SOW-128 | NOT_APPLICABLE |
| DEP-01-01-010 | ANCHOR/TRACES_TO_REQUIREMENT | SOW-131 | NOT_APPLICABLE |
| DEP-01-01-011 | ANCHOR/TRACES_TO_REQUIREMENT | SOW-135 | NOT_APPLICABLE |
| DEP-01-01-012 | ANCHOR/TRACES_TO_REQUIREMENT | SOW-149 | NOT_APPLICABLE |
| DEP-01-01-013 | ANCHOR/TRACES_TO_REQUIREMENT | OBJ-001 | NOT_APPLICABLE |
| DEP-01-01-014 | ANCHOR/TRACES_TO_REQUIREMENT | OBJ-002 | NOT_APPLICABLE |
| DEP-01-01-015 | ANCHOR/TRACES_TO_REQUIREMENT | OBJ-004 | NOT_APPLICABLE |
| DEP-01-01-016 | UPSTREAM/CONSTRAINT | chirality-app-v4:OI-008 | TBD |
| DEP-01-01-017 | UPSTREAM/CONSTRAINT | chirality-app-v4:OI-012 | TBD |
| DEP-01-01-018 | UPSTREAM/PREREQUISITE | chirality-app-v4:DEP-005 | TBD |
| DEP-01-01-019 | DOWNSTREAM/HANDOVER | DEL-01-02 | TBD |
| DEP-01-01-020 | DOWNSTREAM/HANDOVER | DEL-01-03 | TBD |
| DEP-01-01-021 | DOWNSTREAM/HANDOVER | DEL-01-04 | TBD |
| DEP-01-01-022 | DOWNSTREAM/HANDOVER | DEL-01-05 | TBD |
| DEP-01-01-023 | DOWNSTREAM/HANDOVER | DEL-01-06 | TBD |
| DEP-01-01-024 | UPSTREAM/INTERFACE | DEL-01-05 | TBD |

## Lifecycle Summary
- ACTIVE 24; RETIRED 0; EXTRACTED 24; DECLARED 0.
- ANCHOR closure: NOT_APPLICABLE 15. EXECUTION closure: TBD 9; SATISFIED 0.
- RequiredMaturity: INITIALIZED 6 local Deliverable contract relationships; TBD 18 non-deliverable/anchor rows. ProposedMaturity is empty throughout.
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- The maturity default does not satisfy technical input, candidate qualification, decision, handoff or receipt conditions.

## Run Notes
- Run `2026-09-28T03:06:28+00:00`; source-qualified method `chirality-root:bundled:workflow:dependency-extract`; method basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`. Actual bytes/hashes and checks are in `_run_records/dependency-extract-20260927.md`.
- SCOPE `DEL-01-01`; RUN_ROOT `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. Explicit snapshot selected; no auto-discovery. Accepted companion CSVs resolved only canonical identifiers/labels and mappings.
- SOURCE_DOCS / ANCHOR_DOC / EXECUTION_DOC_ORDER: `ScopeOfWork.md` only. DOC_ROLE_MAP DEFAULT; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; ARCHITECTURE_BASIS_POLICY NONE. ANCHOR pass completed with 15 rows before EXECUTION pass.
- Source SHA256 verified before/after: `eddd122cf8b6e2c1ce5933ddb82aa9ec8591baa138a20f439e171ce5d83c4773`. No source, references, decomposition, status or sibling file edits. Human-owned prefix and prior history remain byte-identical.
- Declared mirror counts: added 0; refreshed 0; retired 0; placeholders skipped 2; unread entries 0. One parent; no duplicate row/ID; no missing evidence or invented target.
- OI-008 and OI-012 retain the App implementation owner's actual decisions at their stated points of need. EXTERNAL classifies actors outside this bounded unit and does not move ownership outside the project. DEP-005 alone denotes the separate supplier contribution; its version/environment and capability are unresolved.
- CLM-004 explicitly says the five receivers consume the supplier boundary. CLM-005/REQ-007/REQ-008 ownership/exclusion lists alone generated no edges. Specific plan and local-provider handoffs use REQ-003/REQ-005; the reciprocal DEL-01-05 evidence input preserves VER-005's **when needed** qualification. No blanket hold or generic act sequence is inferred.
- Fixed source snapshot is source-grounded; frozen decomposition draft/pending labels are historical and read with the manager's accepted basis. This local run does not re-decide acceptance or read sibling source contracts.
- Checks: canonical schema, all used enums, supported ID formats, exact evidence quotations (at most 30 words), canonical target identity, field completeness, unique parent/rows/IDs, prefix/history preservation, source unchanged and count consistency PASS. Optional whole-execution EVQ/DRB report was not run; equivalent local evidence/prefix checks passed.
- Limitations: supplier pin/environment, architecture allocation, artifact delivery and actual qualification/receiving evidence remain unfulfilled/unclaimed. This is local extraction only; reciprocal handoff closure, project graph assembly, lifecycle advancement, human acts, release and adoption remain downstream.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:06:28+00:00 — TASK `/root/renewal_research_strategy/dep_del_01_01`, UPDATE / CONSERVATIVE; explicit accepted decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` resolved; no integrity warnings; ACTIVE 24 (ANCHOR 15, EXECUTION 9); source unchanged; local checks PASS; fulfilment unclaimed.
