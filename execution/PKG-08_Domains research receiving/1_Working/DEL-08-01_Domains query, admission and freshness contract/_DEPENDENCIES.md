# Dependencies: DEL-08-01 Domains query, admission and freshness contract

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
- **Status:** EXTRACTED_AND_LOCALLY_VALIDATED
- **Register:** `Dependencies.csv` (v3.1; 29 columns).
- **Counts:** 16 ACTIVE rows: 7 ANCHOR (1 parent, 6 scope/objective traces), 9 EXECUTION (6 UPSTREAM, 3 DOWNSTREAM); 0 RETIRED; 0 DECLARED; EXECUTION target types: DELIVERABLE 5, EXTERNAL 3, UNKNOWN 1.

| DependencyID | Class / anchor | Direction / type | Target | Satisfaction | Status |
|---|---|---|---|---|---|
| DEP-08-01-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM / OTHER | PKG-08 | NOT_APPLICABLE | ACTIVE |
| DEP-08-01-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-023 | NOT_APPLICABLE | ACTIVE |
| DEP-08-01-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-024 | NOT_APPLICABLE | ACTIVE |
| DEP-08-01-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-025 | NOT_APPLICABLE | ACTIVE |
| DEP-08-01-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-247 | NOT_APPLICABLE | ACTIVE |
| DEP-08-01-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-249 | NOT_APPLICABLE | ACTIVE |
| DEP-08-01-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | OBJ-007 | NOT_APPLICABLE | ACTIVE |
| DEP-08-01-008 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-05-01 | TBD | ACTIVE |
| DEP-08-01-009 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-07-02 | TBD | ACTIVE |
| DEP-08-01-010 | EXECUTION / NOT_APPLICABLE | DOWNSTREAM / HANDOVER | DEL-07-02 | TBD | ACTIVE |
| DEP-08-01-011 | EXECUTION / NOT_APPLICABLE | DOWNSTREAM / HANDOVER | DEL-09-10 | TBD | ACTIVE |
| DEP-08-01-012 | EXECUTION / NOT_APPLICABLE | DOWNSTREAM / HANDOVER | DEL-08-02 | TBD | ACTIVE |
| DEP-08-01-013 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | chirality-app-v4:DEP-003 | TBD | ACTIVE |
| DEP-08-01-014 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | Admitted test sources and identified source/admission/freshness basis | TBD | ACTIVE |
| DEP-08-01-015 | EXECUTION / NOT_APPLICABLE | UPSTREAM / CONSTRAINT | chirality-app-v4:OI-023 | TBD | ACTIVE |
| DEP-08-01-016 | EXECUTION / NOT_APPLICABLE | UPSTREAM / CONSTRAINT | chirality-app-v4:OI-026 | TBD | ACTIVE |

## Lifecycle Summary
- ACTIVE: 16; RETIRED: 0. Satisfaction (ACTIVE): NOT_APPLICABLE 7; TBD 9.
- Execution SatisfactionStatus=TBD is the register convention. INITIALIZED on Deliverable targets is local contract maturity only; actual technical input/transfer remains separately required and fulfilment is unclaimed.

## Run Notes
- Method: `chirality-root:bundled:workflow:dependency-extract`; MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE; DOC_ROLE_MAP=DEFAULT.
- SCOPE=DEL-08-01; RUN_ROOT=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- DECOMPOSITION_PATH=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; accepted snapshot basis supplied by the dispatch brief. Canonical companion rows resolve identities/labels only. Historical pending labels do not reverse the supplied accepted standing.
- SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md`; pass 1 completed with seven anchors before pass 2 constructed execution rows.
- Source SHA256 before/after: `581b399ff56c5c9ee153916727b6245cda9aa116487087759f2b2bd7c765ddf1`. No source contract, reference, status, decomposition, sibling or Git edits.
- Declared mirrors: added 0; refreshed 0; retired 0; skipped 2 initial-setup placeholders. Human-owned mode/upstream/downstream sections and existing Run History preserved byte-for-byte.
- RequiredMaturity=INITIALIZED on local Deliverable targets means a checked contract, not receipt of the specific requirements, recovery behavior, cases or handoff. All nine execution rows remain SatisfactionStatus=TBD; actual technical/decision conditions are retained separately.
- Open inputs: external Domains query access (supplier allocation TBD), admitted test sources/admission basis (UNKNOWN), and OI-023/OI-026 resolutions with their exact owners/points of need. External knowledge development does not settle provider allocation, deployment, transport or data boundary. Definition continues where independently supported; Domains is later and PEC-independent.
- DEL-07-02 has distinct upstream recovery-policy input and downstream Domains-case handoff; neither is a synthetic reciprocal start gate. CLM-005 explicitly identifies case consumers. Owner exclusions, B-key citation lists and adjacency did not create rows.
- No host construction/application or human approval prerequisite was added from an ownership exclusion or the later witness's needs. Candidate creation, checking, actual approval/application and reliance remain distinct acts.
- Validation: mandatory schema/used-enum/ID/evidence/summary/source-preservation checks recorded in `_run_records/dependency-extract-20260927.md`. Whole-execution optional EVQ/DRB report not run; local EVQ-003/EVQ-004/DRB-006 conditions checked directly.
- Nonfatal limitations: one UNKNOWN target has no selected source identity/location; three EXTERNAL targets retain qualified references and no TargetDeliverableID. No parent ambiguity, missing decomposition, unread declared entry or declared mismatch. No closure, readiness, qualification, adoption or project DAG is claimed.

- **Run 2026-09-29 (DX-3, APP-V4-BASIS-ALIGN-20260928; dependency-extract UPDATE after SCA-V4-001 SoW revision).** Method `chirality-root:bundled:workflow:dependency-extract` (WORKFLOW.md SHA256 `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3`). Brief: run folder `BRIEFS.md` § DX (group DX-3). Defaults and chosen paths: SCOPE=DEL-08-01; MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE; DOC_ROLE_MAP=DEFAULT; SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only (explicit); RUN_ROOT=`projects/chirality-app-v4/execution`; DECOMPOSITION_PATH=`projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (current, post-SCA-V4-001).
- Source `ScopeOfWork.md` SHA256 `df2795869011f9364d5acf7541d66e2c32ffdd382c757153ad8d1fe8492607d7` (commit `340ecf341`; only CLM-003 revised and AX-005 added), unchanged during the run. The deliverable has no `Design/` folder. Pass 1 re-confirmed parent PKG-08 and traces SOW-023/024/025/247/249 and OBJ-007 (not amended by SCA-V4-001).
- Pass 2 result: 0 rows added; 1 row refreshed in place (`DEP-08-01-008` → DEL-05-01: Statement now names the host-agent destination constraint of PRD V4-HOST-02 as revised by APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5, from revised CLM-003); 15 rows re-observed unchanged (LastSeen only); 0 retired. The SoW does not name DEL-03-04, so no supplier-side mirror (P2 M-04-08-01, deferred) is extracted.
- Declaration mirrors added/refreshed/retired: 0/0/0; 2 placeholders skipped. Human-owned sections byte-identical.
- Function 5 checks: `validate_dependencies_schema.py` VALID (29 columns, 16 rows); `validate_enum.py` 23 invocations, 0 failures; `validate_id_format.sh` 31 invocations, 0 failures; unique IDs; prefix matches; exactly 1 ACTIVE parent anchor; no blank quote or placeholder locus; no Status=CANDIDATE. Run record: `_run_records/dependency-extract-20260929.md`.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:06:06+00:00 — TASK `/root/renewal_research_strategy/dep_del_08_01`; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` available (accepted snapshot); 16 ACTIVE (7 ANCHOR / 9 EXECUTION), 0 RETIRED; nonfatal unresolved source identity/allocation/decisions retained; no structural warning.
- 2026-09-29T14:38:50+00:00 — TASK DX-3 (APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS=ScopeOfWork.md; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` available. Added 0, refreshed 1 (DEP-08-01-008), retired 0. ACTIVE=16 (ANCHOR=7; EXECUTION=9), RETIRED=0. Mandatory local checks passed; no integrity warnings.
