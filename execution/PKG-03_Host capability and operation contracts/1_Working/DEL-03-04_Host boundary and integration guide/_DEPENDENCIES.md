# Dependencies: DEL-03-04 Host boundary and integration guide

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
- **Counts:** 23 ACTIVE rows: 4 ANCHOR (1 parent, 3 scope/objective traces), 19 EXECUTION (19 UPSTREAM, 0 DOWNSTREAM); 0 RETIRED; 0 DECLARED; EXECUTION target types: DELIVERABLE 18, DOCUMENT 1.

| DependencyID | Class / anchor | Direction / type | Target | Satisfaction | Status |
|---|---|---|---|---|---|
| DEP-03-04-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM / OTHER | PKG-03 | NOT_APPLICABLE | ACTIVE |
| DEP-03-04-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-156 | NOT_APPLICABLE | ACTIVE |
| DEP-03-04-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-187 | NOT_APPLICABLE | ACTIVE |
| DEP-03-04-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-03-04-005 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-03-01 | TBD | ACTIVE |
| DEP-03-04-006 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-03-02 | TBD | ACTIVE |
| DEP-03-04-007 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-03-03 | TBD | ACTIVE |
| DEP-03-04-008 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-02-01 | TBD | ACTIVE |
| DEP-03-04-009 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-02-03 | TBD | ACTIVE |
| DEP-03-04-010 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-02-04 | TBD | ACTIVE |
| DEP-03-04-011 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-04-01 | TBD | ACTIVE |
| DEP-03-04-012 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-04-02 | TBD | ACTIVE |
| DEP-03-04-013 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-04-03 | TBD | ACTIVE |
| DEP-03-04-014 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-05-01 | TBD | ACTIVE |
| DEP-03-04-015 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-05-02 | TBD | ACTIVE |
| DEP-03-04-016 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-07-01 | TBD | ACTIVE |
| DEP-03-04-017 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-07-02 | TBD | ACTIVE |
| DEP-03-04-018 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-08-01 | TBD | ACTIVE |
| DEP-03-04-019 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-08-02 | TBD | ACTIVE |
| DEP-03-04-020 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | App v4 host integration basis — HOST_INTEGRATION.md §10 | TBD | ACTIVE |
| DEP-03-04-021 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-01-01 | TBD | ACTIVE |
| DEP-03-04-022 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-09-06 | TBD | ACTIVE |
| DEP-03-04-023 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | DEL-09-09 | TBD | ACTIVE |

## Lifecycle Summary
- ACTIVE: 23; RETIRED: 0. Satisfaction (ACTIVE): NOT_APPLICABLE 4; TBD 19.
- Execution relationships carry SatisfactionStatus=TBD (register convention). INITIALIZED on Deliverable targets is the local contract threshold only; actual input receipt, satisfaction, global closure and graph acceptance remain unassessed.

## Run Notes

- Selected method: `chirality-root:bundled:workflow:dependency-extract`; method basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`. Source hash matched dispatch before and after.
- SCOPE=`DEL-03-04`; MODE=`UPDATE`; STRICTNESS=`CONSERVATIVE`; CONSUMER_CONTEXT=`NONE`; ARCHITECTURE_BASIS_POLICY=`NONE`; DOC_ROLE_MAP=`DEFAULT`.
- RUN_ROOT=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`; DECOMPOSITION_PATH=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. Accepted snapshot companion IDs/labels were resolved; historical candidate wording inside the preserved markdown is not a new acceptance decision.
- SOURCE_DOCS=`ScopeOfWork.md`; ANCHOR_DOC=`ScopeOfWork.md`; EXECUTION_DOC_ORDER=`ScopeOfWork.md`. Pass 1 completed with exactly one parent and three explicit traces before Pass 2. `_REFERENCES.md` was read only for local pointers. No sibling source contract was read.
- Existing register absent. Added 20 extracted rows; no retirement or declared-row change. Declared mirror counts: added=0, refreshed=0, retired=0; skipped placeholders=2. The human-owned mode/upstream/downstream sections remain byte-identical; prior Run History is preserved.
- Positive execution evidence is the receiving-map introduction requiring named input definitions at actual use, the named contribution rows, consumed definitions in CLM-002/REQ-002/REQ-004, and guide comparison methods VER-001/003/004/005/008. Ownership/exclusion lists and structural adjacency alone emitted no edges.
- Open OI decisions and actual host/connector technical evidence are carried at their stated points of need, not converted into blanket guide/project holds. No provider deployment or shared/host construction is allocated. Human decisions remain actual human acts, separately evidenced, with no synthetic act sequence.
- Optional external access and independent PEC/Domains paths preserve disabled/absent/limited fallbacks. PEC D108 retains accepted-as-is MAJOR/partly-met limitations and proves no repair, release or adoption. Domains remains later and unallocated; content outside this repository does not settle tool deployment. These runtime qualification conditions do not become external provider prerequisites to guide definition.
- No external identities were rebound to App Deliverable IDs; all 15 DEL targets are expressly App v4. No unsupported unknown target or guessed schedule was added. Actual input receipt, satisfaction, global closure and graph acceptance remain unassessed.
- Mandatory local schema, used-enum, ID, quote/locus, duplicate, parent, completeness, preservation and hash checks are recorded in the local run record. Optional whole-execution EVQ/DRB scan was omitted to keep this check bounded.

- **Run 2026-09-29 (DX-3, APP-V4-BASIS-ALIGN-20260928; dependency-extract UPDATE after SCA-V4-001 SoW revision).** Method `chirality-root:bundled:workflow:dependency-extract` (WORKFLOW.md SHA256 `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3`). Brief: run folder `BRIEFS.md` § DX (group DX-3). Defaults and chosen paths: SCOPE=DEL-03-04; MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE; DOC_ROLE_MAP=DEFAULT; SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only (explicit; `Design/` DRAFT files not read); RUN_ROOT=`projects/chirality-app-v4/execution`; DECOMPOSITION_PATH=`projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (current, post-SCA-V4-001).
- Source `ScopeOfWork.md` SHA256 `895f004e4d0f133798f461d8157ac63fff880da09f471be9bae885fe0cfb7c28` (commit `340ecf341`), unchanged during the run. SoW line numbers cited in existing SourceRefs (28, 43, 52, 59–65, 70, 72, 92) are unchanged by the revision. Pass 1 re-confirmed parent PKG-03 and traces SOW-156, SOW-187, OBJ-004 before Pass 2.
- Pass 2 result: 3 rows added from the new CLM-003 final sentence (SCA-V4-001, C1 S-04-6, edit E-0304-06): `DEP-03-04-021` → DEL-01-01, `DEP-03-04-022` → DEL-09-06, `DEP-03-04-023` → DEL-09-09, each UPSTREAM INTERFACE. 1 row refreshed in place (`DEP-03-04-011` → DEL-04-01: Statement/SourceRef/Notes for revised REQ-004 and TBD-001/TBD-002, C1 S-04-1 / E-0304-01; SatisfactionStatus unchanged). 19 rows re-observed unchanged (LastSeen only). 0 retired. All 23 quotes re-checked verbatim.
- Applied owner decisions in the revised receiving-map rows and REQ-005 (DECISION-2 D5; SWBPIPE-INTAKE DECISION-4 D4-1/D4-3 and DECISION-5; PRD V4-HOST-01/02) are carried meanings, not open inputs; no row. No DEL-00-* or supplier-side mirror rows are in scope.
- Declaration mirrors added/refreshed/retired: 0/0/0; 2 placeholders skipped. Human-owned sections byte-identical.
- Function 5 checks: `validate_dependencies_schema.py` VALID (29 columns, 23 rows); `validate_enum.py` 19 invocations, 0 failures; `validate_id_format.sh` 53 invocations, 0 failures; unique IDs; prefix matches; exactly 1 ACTIVE parent anchor; no blank quote or placeholder locus; no Status=CANDIDATE. Run record: `_run_records/dependency-extract-20260929.md`.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:20:20+00:00 — TASK `/root/renewal_research_strategy/dep_del_03_04`; UPDATE / CONSERVATIVE; accepted GROUP3 canonical decomposition resolved; 20 ACTIVE (4 ANCHOR / 16 EXECUTION), 0 RETIRED, 0 declared mirrors; one parent; no floating/ambiguous/missing-decomposition warnings; all execution satisfaction TBD.
- 2026-09-29T14:38:50+00:00 — TASK DX-3 (APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS=ScopeOfWork.md; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` available. Added 3 (DEL-01-01, DEL-09-06, DEL-09-09 UPSTREAM INTERFACE), refreshed 1 (DEP-03-04-011), retired 0. ACTIVE=23 (ANCHOR=4; EXECUTION=19), RETIRED=0. Mandatory local checks passed; no integrity warnings.
