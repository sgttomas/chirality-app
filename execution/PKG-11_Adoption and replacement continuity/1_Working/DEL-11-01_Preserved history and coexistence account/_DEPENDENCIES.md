# Dependencies: DEL-11-01 Preserved history and coexistence account

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
- **Status:** EXTRACTED
- **Counts:** 12 ACTIVE; 7 ANCHOR (1 parent, 6 traces); 5 EXECUTION (4 upstream inputs, 1 downstream handoff); 0 RETIRED; 0 DECLARED; 0 EXTERNAL; 0 UNKNOWN.

| DependencyID | Class | Direction | Target | Type |
|---|---|---|---|---|
| DEP-11-01-001 | ANCHOR | UPSTREAM | PKG-11 | OTHER |
| DEP-11-01-002 | ANCHOR | UPSTREAM | SOW-114 | OTHER |
| DEP-11-01-003 | ANCHOR | UPSTREAM | SOW-251 | OTHER |
| DEP-11-01-004 | ANCHOR | UPSTREAM | SOW-252 | OTHER |
| DEP-11-01-005 | ANCHOR | UPSTREAM | SOW-253 | OTHER |
| DEP-11-01-006 | ANCHOR | UPSTREAM | SOW-258 | OTHER |
| DEP-11-01-007 | ANCHOR | UPSTREAM | OBJ-009 | OTHER |
| DEP-11-01-008 | EXECUTION | UPSTREAM | DEL-10-03 | PREREQUISITE |
| DEP-11-01-009 | EXECUTION | UPSTREAM | DEL-10-01 | PREREQUISITE |
| DEP-11-01-010 | EXECUTION | UPSTREAM | DEL-11-02 | PREREQUISITE |
| DEP-11-01-011 | EXECUTION | DOWNSTREAM | DEL-11-03 | HANDOVER |
| DEP-11-01-012 | EXECUTION | UPSTREAM | 47fc49e96c2931ba18090f1a82d56a49f230b3ee | PREREQUISITE |

---

## Lifecycle Summary
- ACTIVE=12; RETIRED=0. Closure: NOT_APPLICABLE=7 (anchors), TBD=5 (execution); PENDING=0, IN_PROGRESS=0, SATISFIED=0, WAIVED=0.
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.

---

## Run Notes
- Method: `chirality-root:bundled:workflow:dependency-extract`; MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE; DOC_ROLE_MAP=DEFAULT.
- SCOPE=DEL-11-01; RUN_ROOT=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`; DECOMPOSITION_PATH=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. Accepted companion rows resolve labels; dispatch rows resolve current local paths.
- SOURCE_DOCS, ANCHOR_DOC and EXECUTION_DOC_ORDER: `ScopeOfWork.md` only. Pass 1 completed with seven anchors before Pass 2 emitted five execution relationships.
- Source SHA256 before/after: `272f76221dd429a52143e51ef4898ce290669b7be1d773a8fba3476282f04309`; matches dispatch. No source or reference edits. Human-owned mode and declared sections remain byte-identical; original history is preserved.
- Declared mirrors: added 0, refreshed 0, retired 0; skipped 2 `None declared at initial setup` placeholders. Existing CSV absent; added 12 extracted rows; no prior rows to retire.
- Four local Deliverable relationships carry RequiredMaturity=INITIALIZED only for local contract maturity; each actual input/handoff condition remains in its statement/notes. All five execution SatisfactionStatus values are TBD; no receipt, production completion or dependency closure is claimed.
- Own `_REFERENCES.md` identifies the later scoped OI-017 edition selection in `projects/chirality-app-v4/execution/_Coordination/CURRENT_EXECUTION_BASIS.md`; this pointer was read, its body was not. Historical OPEN source wording creates no new edition decision and no evidence of wider adoption or active-agent supply.
- Owner exclusions, sibling lists and source citations alone created no edges. Retirement/adoption/replacement and professional reliance retain actual actors and evidence. OI-024/OQ-12 stay with Owner with affected consumers at their stated points of need; OI-018 remains at instruction change/dependent supply. These are not invented prerequisites to this extraction or a blanket project hold.
- The thesis row records an explicit production comparison input, not completed verification. Old projects, archives, thesis and sources remain unchanged by this run; no broad archive audit, technical implementation, migration, retirement, adoption, release or lifecycle advancement occurred.
- Mandatory local schema, enum, ID, evidence, quote, duplicate, count, single-parent and preservation checks: PASS (details in `_run_records/dependency-extract-20260927.md`). Whole-execution EVQ/DRB scan skipped as directed while peers write. Warnings: none; receipt and production-evidence limits above remain unresolved.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:39:58Z — TASK dependency-extract; UPDATE/CONSERVATIVE; accepted GROUP3-20260928T001055Z decomposition and companion labels available; ACTIVE=12 (ANCHOR=7, EXECUTION=5), RETIRED=0; warnings=0; local checks PASS; technical input receipt and closure unclaimed.
