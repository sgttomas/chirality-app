# Dependencies: DEL-01-04 Native requests, outcomes and attachments

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

- ACTIVE: 19 (6 ANCHOR; 13 EXECUTION). RETIRED: 0. DECLARED: 0.
- Parent anchors: 1; scope/objective trace anchors: 5. External targets: 7; unknown targets: 0.

| Dependency | Class/type | Direction | Target |
|---|---|---|---|
| DEP-01-04-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-01 |
| DEP-01-04-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-005 |
| DEP-01-04-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-014 |
| DEP-01-04-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-129 |
| DEP-01-04-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 |
| DEP-01-04-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 |
| DEP-01-04-007 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-01 |
| DEP-01-04-008 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-02 |
| DEP-01-04-009 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-02 |
| DEP-01-04-010 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-02 |
| DEP-01-04-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 |
| DEP-01-04-012 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 |
| DEP-01-04-013 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 |
| DEP-01-04-014 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 |
| DEP-01-04-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-008 |
| DEP-01-04-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-012 |
| DEP-01-04-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-014 |
| DEP-01-04-018 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-005 |
| DEP-01-04-019 | EXECUTION / PREREQUISITE | UPSTREAM | Person performing the positive human-act case and separate faithful recorder |

## Lifecycle Summary

- ACTIVE 19; RETIRED 0. Closure: NOT_APPLICABLE 6 (anchors), TBD 13 (execution), SATISFIED 0.
- INITIALIZED records checked local contracts only. Actual supplier inputs, implemented interfaces, adopted policy, owner decisions and the human-act witness remain separate and unverified. This run does not advance status, accept the graph or claim implementation, qualification, adoption or release.

## Run Notes

- Workflow: `chirality-root:bundled:workflow:dependency-extract`; MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE; DOC_ROLE_MAP=DEFAULT.
- SCOPE=DEL-01-04. SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md`. Pass 1 completed before Pass 2: one explicit parent, three scope references, two objectives.
- RUN_ROOT=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`. DECOMPOSITION_PATH=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. Accepted snapshot companion rows resolve canonical labels/identities; dispatch rows supply current target paths. Preserved candidate-stage wording in snapshot documents does not revise the supplied accepted-basis standing.
- Source SHA256 before/after: `7261a58f93d4531ca080c16d7fe088818871c3444085bade2eb2350ace94e60a`; unchanged and matches dispatch. RequiredMaturity=INITIALIZED applies only to the six local-deliverable rows; all other targets use TBD, and anchors have NOT_APPLICABLE closure.
- Declared mirroring: added 0, refreshed 0, retired 0; skipped 2 initial-setup placeholders. Human-owned mode/upstream/downstream bytes and prior Run History preserved. No existing CSV rows to retire.
- DEL-01-03 joint-map and excluded ownership are not production inputs; no execution row inferred from them. Opposite DEL-02-02 directions are separate actual interfaces (workflow state received; native interactions supplied), not duplicate edges or an invented sequence.
- OI-001/002/008/012/014 remain with their exact owners and points of need. Optional legacy UI reuse stays conditional; no common component, storage design, adopted pin, supplier wire field or global reserved-act list is selected.
- DEP-005 remains an external supplier contribution; no external reused DEL identity resolves to an App Deliverable. The positive VER-005 human-act witness requires an actually performed act and separate recorder only for that case. Runtime approval, registration and host-receipt behavior is not a blanket project dependency.
- Interpretation limits: all execution fulfilment is TBD; the person/recorder identities and witness location are not supplied. Joined workflow/recovery qualification remains with integration owners, and no unnamed joined consumer was invented from local fixture coverage.
- Local checks: canonical 29-column schema, all used enums and supported ID formats, one parent, unique IDs/no duplicate edges, exact evidence quotes (at most 30 words), complete source loci, counts, source unchanged and human sections preserved. External OI/DEP reference forms were matched to accepted companion rows because the local dependency-ID validator does not govern them. Optional whole-root EVQ/DRB report not run; equivalent quote/locus/prefix checks passed locally.
- No integrity warnings. Full verification and input/output hashes are in `_run_records/dependency-extract-20260927.md`.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:14:57+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted GROUP3-20260928T001055Z canonical SOFTWARE_DECOMP.md available; warnings 0; ACTIVE 19 (ANCHOR 6 / EXECUTION 13), RETIRED 0; no lifecycle act.
