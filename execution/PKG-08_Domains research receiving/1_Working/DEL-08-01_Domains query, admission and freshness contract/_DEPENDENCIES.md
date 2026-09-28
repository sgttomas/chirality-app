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
- **Status:** EXTRACTED; canonical `Dependencies.csv` v3.1.
- **Counts:** 16 ACTIVE / 0 RETIRED; 7 ANCHOR (1 parent + 6 traces), 9 EXECUTION; 16 EXTRACTED / 0 DECLARED.

| Dependency | Class / type | Direction | Target |
|---|---|---|---|
| DEP-08-01-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-08 |
| DEP-08-01-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-023 |
| DEP-08-01-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-024 |
| DEP-08-01-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-025 |
| DEP-08-01-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-247 |
| DEP-08-01-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-249 |
| DEP-08-01-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-007 |
| DEP-08-01-008 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 |
| DEP-08-01-009 | EXECUTION / INTERFACE | UPSTREAM | DEL-07-02 |
| DEP-08-01-010 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-07-02 |
| DEP-08-01-011 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-10 |
| DEP-08-01-012 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-08-02 |
| DEP-08-01-013 | EXECUTION / PREREQUISITE | UPSTREAM | chirality-app-v4:DEP-003 |
| DEP-08-01-014 | EXECUTION / PREREQUISITE | UPSTREAM | Admitted test sources and identified source/admission/freshness basis |
| DEP-08-01-015 | EXECUTION / CONSTRAINT | UPSTREAM | chirality-app-v4:OI-023 |
| DEP-08-01-016 | EXECUTION / CONSTRAINT | UPSTREAM | chirality-app-v4:OI-026 |

---

## Lifecycle Summary
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Register extraction: ACTIVE=16; RETIRED=0. Closure: NOT_APPLICABLE=7 (anchors); TBD=9 (execution); PENDING=0; IN_PROGRESS=0; SATISFIED=0; WAIVED=0.
- Target types: WBS_NODE=1; REQUIREMENT=6; DELIVERABLE=5; EXTERNAL=3; UNKNOWN=1.

---

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

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:06:06+00:00 — TASK `/root/renewal_research_strategy/dep_del_08_01`; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` available (accepted snapshot); 16 ACTIVE (7 ANCHOR / 9 EXECUTION), 0 RETIRED; nonfatal unresolved source identity/allocation/decisions retained; no structural warning.
