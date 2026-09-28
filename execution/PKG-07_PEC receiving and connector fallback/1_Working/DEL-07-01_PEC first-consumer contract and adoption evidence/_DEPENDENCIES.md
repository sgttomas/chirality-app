# Dependencies: DEL-07-01 PEC first-consumer contract and adoption evidence

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
- **Status:** EXTRACTED — local validation recorded in run record.
- **Rows:** 15 ACTIVE / 0 RETIRED; 8 ANCHOR / 7 EXECUTION; 15 EXTRACTED / 0 DECLARED.
- **Targets:** 4 EXTERNAL / 0 UNKNOWN; 2 local DELIVERABLE execution rows / 1 DOCUMENT execution row.

| Dependency | Class/type | Direction | Target |
|---|---|---|---|
| DEP-07-01-001 | ANCHOR/IMPLEMENTS_NODE | UPSTREAM | PKG-07 |
| DEP-07-01-002 | ANCHOR/TRACES_TO_REQUIREMENT | UPSTREAM | SOW-028 |
| DEP-07-01-003 | ANCHOR/TRACES_TO_REQUIREMENT | UPSTREAM | SOW-029 |
| DEP-07-01-004 | ANCHOR/TRACES_TO_REQUIREMENT | UPSTREAM | SOW-030 |
| DEP-07-01-005 | ANCHOR/TRACES_TO_REQUIREMENT | UPSTREAM | SOW-031 |
| DEP-07-01-006 | ANCHOR/TRACES_TO_REQUIREMENT | UPSTREAM | SOW-244 |
| DEP-07-01-007 | ANCHOR/TRACES_TO_REQUIREMENT | UPSTREAM | SOW-248 |
| DEP-07-01-008 | ANCHOR/TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-007 |
| DEP-07-01-009 | EXECUTION/PREREQUISITE | UPSTREAM | PEC provider — agreed receiving contract and response shape |
| DEP-07-01-010 | EXECUTION/INTERFACE | UPSTREAM | PEC provider — actual response and source identity for a qualified receiving witness |
| DEP-07-01-011 | EXECUTION/CONSTRAINT | UPSTREAM | PEC provider — actual candidate/release identity and qualification evidence |
| DEP-07-01-012 | EXECUTION/CONSTRAINT | UPSTREAM | PEC:DEL-04-03 |
| DEP-07-01-013 | EXECUTION/CONSTRAINT | UPSTREAM | D-PEC-108 |
| DEP-07-01-014 | EXECUTION/INTERFACE | UPSTREAM | DEL-07-02 |
| DEP-07-01-015 | EXECUTION/HANDOVER | DOWNSTREAM | DEL-07-02 |

---

## Lifecycle Summary
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Extraction: 15 ACTIVE / 0 RETIRED. Closure: 8 NOT_APPLICABLE anchors / 7 PENDING execution inputs or handoffs; 0 SATISFIED.

---

## Run Notes
- Run timestamp: 2026-09-28T03:05:46+00:00; selected method: `chirality-root:bundled:workflow:dependency-extract`.
- SCOPE: `DEL-07-01`; RUN_ROOT: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- DECOMPOSITION_PATH: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. Accepted snapshot companions resolved package, scope, objective and DEL-07-02 labels only; frozen historical candidate labels do not reverse the accepted basis described in the source.
- SOURCE_DOCS / ANCHOR_DOC / EXECUTION_DOC_ORDER: `ScopeOfWork.md` only; DOC_ROLE_MAP: DEFAULT; MODE: UPDATE; STRICTNESS: CONSERVATIVE; CONSUMER_CONTEXT: NONE; ARCHITECTURE_BASIS_POLICY: NONE.
- Pass 1 completed with 8 ANCHOR rows: 1 explicit parent, 6 scope traces, 1 objective trace. Pass 2 then produced 7 EXECUTION rows: 4 EXTERNAL, 1 DOCUMENT and 2 local DELIVERABLE rows. No UNKNOWN target; unresolved contract terms remain OI-022/TBD-001.
- Source SHA256 before/after: `5e2fba1d2191d97832a3f09feeb91f4f4231775a6a99b2b6c769a54c43edc5e3`. Source, references, statuses and decomposition were not edited. The three human-owned sections remain byte-identical.
- No prior CSV existed; 15 rows added, 0 refreshed, 0 retired, 0 deleted. Declaration mirrors: 0 added/refreshed/retired; 2 setup placeholders skipped.
- INITIALIZED is only the local contract maturity threshold for DEL-07-02. Actual route availability, PEC contract/response, qualification/release evidence and deliberate App adoption remain separately required and unclaimed. Non-deliverable maturity is TBD; anchor closure is NOT_APPLICABLE; execution closure is PENDING.
- PEC DEL-04-03 is qualified as external and cannot resolve to App DEL-04-03. PEC source documents and D108 were not independently inspected; their target pointers are grounded in this local source. D108's ACCEPT_AS_IS retains MAJOR/partly met meaning and establishes no repair, service readiness, release or adoption.
- The upstream DEL-07-02 route and downstream limitation/responsibility handoff are distinct information flows, not a synthetic ordering cycle. CLM-004/REQ-007 ownership exclusions do not create DEL-06-01/02, DEL-08-01/02 or Piping edges. Optional PEC and independent Domains/fallback treatment remain intact.
- OI-022 stays open for actual receiving terms and point-of-need evidence; preparation may continue. No provider/host construction, wire schema, deadline, approval, project DAG, lifecycle advancement or global closure is inferred.
- Local validation results and source identities are recorded in `_run_records/dependency-extract-20260927.md`; optional whole-execution EVQ/DRB scan not run.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:05:46+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` and named canonical rows resolved. ACTIVE: 15 (8 ANCHOR / 7 EXECUTION); 0 RETIRED; 4 EXTERNAL / 0 UNKNOWN. No integrity warnings; OI-022 and actual receiving fulfilment remain open.
