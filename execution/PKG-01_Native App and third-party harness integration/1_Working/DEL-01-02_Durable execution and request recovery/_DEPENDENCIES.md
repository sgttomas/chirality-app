# Dependencies: DEL-01-02 Durable execution and request recovery

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
- **Status:** EXTRACTED — locally validated; no global closure decision.
- **Register:** `Dependencies.csv` (v3.1; 29 canonical columns).
- **Counts:** 21 ACTIVE / 0 RETIRED; 17 ANCHOR (1 parent, 13 scope traces, 3 objective traces); 4 EXECUTION (2 UPSTREAM, 2 DOWNSTREAM); 0 DECLARED; 0 EXTERNAL; 0 UNKNOWN.

| Dependency | Class / type | Direction | Target | Closure |
|---|---|---|---|---|
| DEP-01-02-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-01 | NOT_APPLICABLE |
| DEP-01-02-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-007 | NOT_APPLICABLE |
| DEP-01-02-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-008 | NOT_APPLICABLE |
| DEP-01-02-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-060 | NOT_APPLICABLE |
| DEP-01-02-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-061 | NOT_APPLICABLE |
| DEP-01-02-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-062 | NOT_APPLICABLE |
| DEP-01-02-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-063 | NOT_APPLICABLE |
| DEP-01-02-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-064 | NOT_APPLICABLE |
| DEP-01-02-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-065 | NOT_APPLICABLE |
| DEP-01-02-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-066 | NOT_APPLICABLE |
| DEP-01-02-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-122 | NOT_APPLICABLE |
| DEP-01-02-012 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-123 | NOT_APPLICABLE |
| DEP-01-02-013 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-124 | NOT_APPLICABLE |
| DEP-01-02-014 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-125 | NOT_APPLICABLE |
| DEP-01-02-015 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | NOT_APPLICABLE |
| DEP-01-02-016 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | NOT_APPLICABLE |
| DEP-01-02-017 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE |
| DEP-01-02-018 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | TBD |
| DEP-01-02-019 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-01-04 | TBD |
| DEP-01-02-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | TBD |
| DEP-01-02-021 | EXECUTION / CONSTRAINT | UPSTREAM | DEL-04-01 | TBD |

## Lifecycle Summary
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Register lifecycle: ACTIVE 21; RETIRED 0. Closure: NOT_APPLICABLE 17; TBD 4; PENDING 0; IN_PROGRESS 0; SATISFIED 0; WAIVED 0.
- Execution RequiredMaturity is INITIALIZED only for the approved local Deliverable contract threshold. Actual supplier boundary/types, policy and produced interface/evidence conditions remain explicit and unclaimed. Anchor closure is NOT_APPLICABLE.

## Run Notes
- Workflow: `chirality-root:bundled:workflow:dependency-extract`; method basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`, unchanged current workflow source checked by SHA256.
- SCOPE DEL-01-02; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; ARCHITECTURE_BASIS_POLICY NONE; DOC_ROLE_MAP DEFAULT.
- RUN_ROOT: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- DECOMPOSITION_PATH: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; available. The frozen historical candidate labels are read with the accepted Group3 basis supplied by this brief and local contract.
- SOURCE_DOCS, ANCHOR_DOC and EXECUTION_DOC_ORDER: `ScopeOfWork.md` only. Pass 1 completed with one parent plus explicit scope/objective traces before Pass 2 extracted the four positive transfers. Canonical companion rows resolve labels/IDs; dispatch rows resolve actual local paths. No sibling source contracts read.
- Source SHA256 before/after: `057ae2fdf4c3e98c961214739d2170a7c8ab29a530208f0c476af15125d6c6b4` (matches dispatch). Human-owned mode/upstream/downstream sections and existing Run History are preserved byte-for-byte.
- Declaration mirrors: added 0, refreshed 0, retired 0; skipped 2 initial-setup placeholders. No prior CSV rows existed to merge or retire.
- Ownership/exclusion inventories (CLM-003/REQ-009), bare citations and verification scenario lists are not edges. No generic approval or future-human-act prerequisite was extracted. Runtime response rules alone are not project input dependencies.
- OI-008 allocation, OI-012 supplier pin, DEP-005 supplier/version/environment inputs and the local persistence/request/reconnect/fixture means remain open at their source-stated points of need. OI-001/OI-002 policy choices remain with actual owners; independent recovery definition can proceed. No implementation means, timing thresholds, API fields or v3 Runtime service are selected.
- Actual human act, recorder identity, observed/unknown outcome and wider-undertaking recovery limits remain explicit in execution rows. Optional old-client reuse remains optional; no product execution, qualification, release, reliance or adoption is claimed.
- Local schema, all used enum and stable-ID validators, one-parent, evidence/quote, uniqueness, source immutability, declared-section preservation and summary-count checks passed; exact commands/results and input hashes are in `_run_records/dependency-extract-20260927.md`. The optional whole-execution EVQ/DRB report was not run; equivalent local blank-quote, placeholder-locus and DEP-prefix checks passed.
- Integrity warnings: none. Nonfatal limitations: actual input/handoff fulfilment is unverified; open means and policy remain unresolved as stated. No project graph, schedule or global closure is assembled here.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:11:19Z — TASK /root/renewal_research_strategy/dep_del_01_02; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` available; 21 ACTIVE (17 ANCHOR, 4 EXECUTION), 0 RETIRED; integrity warnings none; actual fulfilment unclaimed.
