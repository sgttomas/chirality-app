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

- **Status:** EXTRACTED; local validation recorded in `_run_records/dependency-extract-20260927.md`.
- **Rows:** 20 ACTIVE / 0 RETIRED; 4 ANCHOR (1 parent, 3 traces), 16 EXECUTION (15 local Deliverable interfaces, 1 document comparison input); 0 DECLARED; 0 EXTERNAL; 0 UNKNOWN.

| Dependency IDs | Class | Input / trace |
|---|---|---|
| DEP-03-04-001 | ANCHOR | PKG-03 parent |
| DEP-03-04-002–004 | ANCHOR | SOW-156; SOW-187; OBJ-004 |
| DEP-03-04-005–019 | EXECUTION | Named App v4 contract definitions and evidence limits required by the receiving map and guide comparisons |
| DEP-03-04-020 | EXECUTION | H §10 checklist comparison basis |

## Lifecycle Summary

- 20 ACTIVE / 0 RETIRED; satisfaction: NOT_APPLICABLE=4 anchors, TBD=16 execution inputs; SATISFIED=0.
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Local Deliverable inputs use RequiredMaturity=INITIALIZED for checked contract maturity only. Actual identified definitions, adopted or held policy, technical artifacts, evidence and point-of-use conditions remain separate and unfulfilled/unverified here. No lifecycle change.

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

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:20:20+00:00 — TASK `/root/renewal_research_strategy/dep_del_03_04`; UPDATE / CONSERVATIVE; accepted GROUP3 canonical decomposition resolved; 20 ACTIVE (4 ANCHOR / 16 EXECUTION), 0 RETIRED, 0 declared mirrors; one parent; no floating/ambiguous/missing-decomposition warnings; all execution satisfaction TBD.
