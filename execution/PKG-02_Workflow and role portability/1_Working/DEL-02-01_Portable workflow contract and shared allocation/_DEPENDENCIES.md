# Dependencies: DEL-02-01 Portable workflow contract and shared allocation

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

- **Status:** EXTRACTED; local checks recorded in `_run_records/dependency-extract-20260927.md`.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 24 ACTIVE / 0 RETIRED, all EXTRACTED.
- **Classes:** 16 ANCHOR (1 parent + 12 scope + 3 objective), 8 EXECUTION.
- **Execution targets:** 5 local DELIVERABLE, 3 EXTERNAL, 0 UNKNOWN; all UPSTREAM, 6 INTERFACE + 2 CONSTRAINT.
- **Declared mirrors:** 0 added, 0 refreshed, 0 retired; 2 initial-setup placeholders skipped.

| DependencyID | Class / type | Target | Closure |
|---|---|---|---|
| DEP-02-01-001 | ANCHOR / IMPLEMENTS_NODE | PKG-02 | NOT_APPLICABLE |
| DEP-02-01-002 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-021 | NOT_APPLICABLE |
| DEP-02-01-003 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-022 | NOT_APPLICABLE |
| DEP-02-01-004 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-037 | NOT_APPLICABLE |
| DEP-02-01-005 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-038 | NOT_APPLICABLE |
| DEP-02-01-006 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-039 | NOT_APPLICABLE |
| DEP-02-01-007 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-042 | NOT_APPLICABLE |
| DEP-02-01-008 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-043 | NOT_APPLICABLE |
| DEP-02-01-009 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-044 | NOT_APPLICABLE |
| DEP-02-01-010 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-045 | NOT_APPLICABLE |
| DEP-02-01-011 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-145 | NOT_APPLICABLE |
| DEP-02-01-012 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-146 | NOT_APPLICABLE |
| DEP-02-01-013 | ANCHOR / TRACES_TO_REQUIREMENT | SOW-147 | NOT_APPLICABLE |
| DEP-02-01-014 | ANCHOR / TRACES_TO_REQUIREMENT | OBJ-003 | NOT_APPLICABLE |
| DEP-02-01-015 | ANCHOR / TRACES_TO_REQUIREMENT | OBJ-004 | NOT_APPLICABLE |
| DEP-02-01-016 | ANCHOR / TRACES_TO_REQUIREMENT | OBJ-005 | NOT_APPLICABLE |
| DEP-02-01-017 | EXECUTION / INTERFACE | DEL-03-01 | PENDING |
| DEP-02-01-018 | EXECUTION / INTERFACE | DEL-04-01 | PENDING |
| DEP-02-01-019 | EXECUTION / INTERFACE | DEL-04-03 | PENDING |
| DEP-02-01-020 | EXECUTION / INTERFACE | DEL-05-01 | PENDING |
| DEP-02-01-021 | EXECUTION / INTERFACE | DEL-05-02 | PENDING |
| DEP-02-01-022 | EXECUTION / INTERFACE | SWBPIPE | PENDING |
| DEP-02-01-023 | EXECUTION / CONSTRAINT | OI-014 | PENDING |
| DEP-02-01-024 | EXECUTION / CONSTRAINT | OI-013 | PENDING |

## Lifecycle Summary

- ACTIVE: 24; RETIRED: 0. Closure: NOT_APPLICABLE 16, PENDING 8, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. Each execution row retains its actual descriptor, semantics, consumer input or owner decision condition. None is reported received, compatible, adopted, qualified or complete by this extraction.

## Run Notes

- SCOPE DEL-02-01; selected method `chirality-root:bundled:workflow:dependency-extract`; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; ARCHITECTURE_BASIS_POLICY NONE; DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` (accepted frozen basis; historical draft labels do not reverse the recorded acceptance). Companion CSVs resolve canonical identity only.
- SOURCE_DOCS / ANCHOR_DOC / EXECUTION_DOC_ORDER: `ScopeOfWork.md` only. Two passes completed in order: 16 anchors persisted before execution extraction.
- Source SHA256 before/after: `080d7f5a8e55d93c06f51e5332b53954deb03e0877b1ee49be3011e3de14a294`, matching the dispatch row.
- FACT: catalog descriptors, human-act distinctions, record semantics and minimal-loop/panel/external host consumer needs are consumed through positive receiving statements. CLM-002/003 resolve the suppliers. CLM-002 and REQ-006 ownership/exclusion lists alone do not establish other edges; no sibling inventory was copied into the graph.
- FACT: OI-014 and OI-013 retain owner decisions at their stated points of need. Conditional shared allocation remains required; no common service, repository placement or host/shared implementation is presumed. Actual human acts are distinct from contract authorship, evidence recording and host presentation; no acceptance-first sequence is introduced.
- FACT: external SWBPIPE input remains external and qualified by accepted DEP-001; local definition may proceed with explicit gaps. Source mentions and INITIALIZED status do not prove supplied technical inputs or joined conformance.
- No old register existed; no rows were deleted or retired. Human-owned mode/upstream/downstream bytes and prior Run History were preserved. Mirror totals: 0 added/refreshed/retired, 2 placeholders skipped.
- Validation: schema, used enum values and canonical local IDs, exact source quotes (at most 30 words), source hash, one parent, duplicate-row check, target placement, summary and human-section preservation checked in the local run record. OI references are resolved against Open_Issues.csv; SWBPIPE is an external name, not a local ID-validator family.
- Optional whole-execution EVQ/DRB scan omitted to keep checks local. Local evidence checks found no blank quotes, placeholder SourceRefs or mismatched DEP prefixes.
- Warnings: none. Limits: open owner decisions and unreceived technical inputs remain PENDING; local extraction does not establish graph closure or acceptance.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:09:04+00:00 — TASK `/root/renewal_research_strategy/dep_del_02_01`; UPDATE / CONSERVATIVE; accepted decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` resolved; 24 ACTIVE (16 ANCHOR / 8 EXECUTION), 0 RETIRED; warnings 0; dependency closure unclaimed.
