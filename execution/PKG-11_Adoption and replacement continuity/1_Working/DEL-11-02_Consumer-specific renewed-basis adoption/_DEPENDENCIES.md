# Dependencies: DEL-11-02 Consumer-specific renewed-basis adoption

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
- **Register:** `Dependencies.csv` v3.1, 29 canonical columns; 22 ACTIVE rows, 0 RETIRED, all EXTRACTED.
- **Classes:** 7 ANCHOR (1 parent, 5 scope traces, 1 objective trace); 15 EXECUTION (13 upstream, 2 downstream).
- **Targets:** 7 EXTERNAL; 1 UNKNOWN (specific later-mainline/consumer comparison corpus); package contracts retained at source granularity.

| Dependency ID | Class | Direction | Target | Type |
|---|---|---|---|---|
| DEP-11-02-001 | ANCHOR | UPSTREAM | PKG-11 | OTHER |
| DEP-11-02-002 | ANCHOR | UPSTREAM | SOW-250 | OTHER |
| DEP-11-02-003 | ANCHOR | UPSTREAM | SOW-254 | OTHER |
| DEP-11-02-004 | ANCHOR | UPSTREAM | SOW-255 | OTHER |
| DEP-11-02-005 | ANCHOR | UPSTREAM | SOW-256 | OTHER |
| DEP-11-02-006 | ANCHOR | UPSTREAM | SOW-257 | OTHER |
| DEP-11-02-007 | ANCHOR | UPSTREAM | OBJ-009 | OTHER |
| DEP-11-02-008 | EXECUTION | UPSTREAM | DEL-10-03 | PREREQUISITE |
| DEP-11-02-009 | EXECUTION | UPSTREAM | PKG-02 | PREREQUISITE |
| DEP-11-02-010 | EXECUTION | UPSTREAM | PKG-03 | PREREQUISITE |
| DEP-11-02-011 | EXECUTION | UPSTREAM | PKG-04 | PREREQUISITE |
| DEP-11-02-012 | EXECUTION | UPSTREAM | PKG-05 | PREREQUISITE |
| DEP-11-02-013 | EXECUTION | UPSTREAM | DEP-006 | INTERFACE |
| DEP-11-02-014 | EXECUTION | DOWNSTREAM | DEL-11-01 | HANDOVER |
| DEP-11-02-015 | EXECUTION | DOWNSTREAM | DEL-11-03 | HANDOVER |
| DEP-11-02-016 | EXECUTION | UPSTREAM | Relevant later mainline and consumer changes for the pinned research comparison | CONSTRAINT |
| DEP-11-02-017 | EXECUTION | UPSTREAM | OI-017 | CONSTRAINT |
| DEP-11-02-018 | EXECUTION | UPSTREAM | OI-018 | CONSTRAINT |
| DEP-11-02-019 | EXECUTION | UPSTREAM | OI-019 | CONSTRAINT |
| DEP-11-02-020 | EXECUTION | UPSTREAM | OI-020 | CONSTRAINT |
| DEP-11-02-021 | EXECUTION | UPSTREAM | OI-024 | CONSTRAINT |
| DEP-11-02-022 | EXECUTION | UPSTREAM | OI-014 | CONSTRAINT |

---

## Lifecycle Summary
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Extraction lifecycle: ACTIVE 22; RETIRED 0; DECLARED 0; EXTRACTED 22.
- Closure lifecycle: NOT_APPLICABLE 7 (anchors); TBD 15 (execution); PENDING/IN_PROGRESS/SATISFIED/WAIVED 0.
- Local deliverable contract thresholds use INITIALIZED; non-deliverable thresholds remain TBD. Actual account, contract, owner-evidence and decision conditions remain explicit in statements/notes and are not discharged by contract initialization.

---

## Run Notes
- Selected workflow: `chirality-root:bundled:workflow:dependency-extract`; method basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`, unchanged-source setup candidate `ddd721a90ade401d452d102e6e40d1ffdae654eb` / identical-tree integration `82efe62783bbe8ac7d21476a6662195c0b0a7587` per dispatch brief. Actual read hashes are in the local run record.
- SCOPE DEL-11-02; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; ARCHITECTURE_BASIS_POLICY NONE.
- RUN_ROOT `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- DECOMPOSITION_PATH `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. Historical pending wording remains historical; the dispatch identifies this as accepted Group3 basis. Companion Packages/Deliverables/ScopeLedger/Objectives CSVs resolved canonical IDs and names; dispatch paths resolved current local locations.
- SOURCE_DOCS `[ScopeOfWork.md]`; ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER `[ScopeOfWork.md]`; DOC_ROLE_MAP DEFAULT. No AUTO discovery or legacy document source selected.
- Pass 1 completed with one parent and explicit five scope/one objective anchors before Pass 2. All evidence quotes are verbatim and at most 30 words; all EvidenceFile values are ScopeOfWork.md.
- Source SHA256 before/after must remain `2d962646f8b24a1b76fcd30307859f7c7632c25e78864c28b5fd04fb687a057c`. Existing register was absent. Declared mode/upstream/downstream bytes and existing history are preserved. Mirror rows added/refreshed/retired: 0/0/0; skipped placeholders: 2 (`None declared at initial setup`).
- Explicit CLM-002 consumed contracts support four PACKAGE targets; no individual sibling Deliverables were guessed from contract-owner lists. CLM-004/REQ-007 ownership exclusions alone create no input edge. Positive production-method status handoffs resolve DEL-11-01 and DEL-11-03.
- Owner evidence under DEP-006 remains external to this local contribution. Publication, source resolution, supply, provider adoption, behavior, consumer adoption, technical change and checking have separate warrants. An actual human decision may be faithfully recorded without transferring the human's act to the recorder; no acceptance-before-checking sequence is inferred.
- OI-017/018/019/020/024/014 rows retain only their exact conditional points of need. The local _REFERENCES.md identifies current OI-017 selection for this definition run; that pointer does not establish other-loop adoption or fulfill all future manual outputs. The target CURRENT_EXECUTION_BASIS.md body was not loaded. Independent authorized definition continues.
- Nonfatal limitation: the actual later-mainline and consumer revisions/comparison corpus remain UNKNOWN (DEP-11-02-016). Source inspection does not prove deployed or observed behavior. External/open-matter IDs are source-qualified by App-v4 names and exact register pointers, not treated as App Deliverable IDs.
- No global graph, schedule, closure, receiving adoption, lifecycle advancement, release or replacement determination is made. No new architecture/service/provider construction or instruction amendment is authorized. Optional whole-execution EVQ/DRB checks are omitted while peers write; required local schema, enum, ID and evidence/preservation checks are recorded locally.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27 — TASK `/root/renewal_research_strategy/dep_del_11_02`; UPDATE / CONSERVATIVE; selected accepted Group3 decomposition available; ACTIVE 22 (ANCHOR 7, EXECUTION 15), RETIRED 0; one parent; no structural warnings; unresolved comparison corpus retained UNKNOWN. Local validation and hashes: `_run_records/dependency-extract-20260927.md`.
