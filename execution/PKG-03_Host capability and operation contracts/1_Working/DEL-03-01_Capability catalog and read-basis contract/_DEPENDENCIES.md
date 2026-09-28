# Dependencies: DEL-03-01 Capability catalog and read-basis contract

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
- **Schema:** v3.1 (canonical 29 columns).
- **Counts:** 29 ACTIVE extracted rows: 21 ANCHOR (1 parent + 18 scope + 2 objective) and 8 EXECUTION (6 upstream + 2 downstream); 0 RETIRED; 0 DECLARED; 2 EXTERNAL and 2 UNKNOWN targets.

| IDs | Class/direction | Target / input |
|---|---|---|
| DEP-03-01-001 | ANCHOR | PKG-03 parent |
| DEP-03-01-002–019 | ANCHOR | 18 assigned SOW traces |
| DEP-03-01-020–021 | ANCHOR | OBJ-004 and OBJ-005 traces |
| DEP-03-01-022 | EXECUTION DOWNSTREAM | Workflow and role portability |
| DEP-03-01-023 | EXECUTION DOWNSTREAM | Proposal, validation and outcome contract |
| DEP-03-01-024 | EXECUTION UPSTREAM | Operation-policy and human-act distinctions |
| DEP-03-01-025 | EXECUTION UPSTREAM | Host owner including external SWBPIPE implementation session |
| DEP-03-01-026 | EXECUTION UPSTREAM | Proposal, validation and outcome contract |
| DEP-03-01-027 | EXECUTION UPSTREAM | Extension trace and owner/host-contract-owner retain/narrow/defer disposition |
| DEP-03-01-028 | EXECUTION UPSTREAM | App/shared and affected host/consumer technical agreement |
| DEP-03-01-029 | EXECUTION UPSTREAM | Owner via outside SWB session and App/shared owner: connected examination inputs |

## Lifecycle Summary
- 29 ACTIVE extracted rows: 21 ANCHOR (1 parent + 18 scope + 2 objective) and 8 EXECUTION (6 upstream + 2 downstream); 0 RETIRED; 0 DECLARED; 2 EXTERNAL and 2 UNKNOWN targets.
- Satisfaction: 21 NOT_APPLICABLE anchors; 8 PENDING execution inputs/handoffs; 0 SATISFIED.
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Local-deliverable RequiredMaturity=INITIALIZED is a checked contract threshold; actual technical inputs, agreements, human acts and host evidence remain separate conditions at their stated points of need. Non-deliverable maturity is TBD; ProposedMaturity remains blank.

## Run Notes
- Workflow: `chirality-root:bundled:workflow:dependency-extract`; SCOPE DEL-03-01; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; ARCHITECTURE_BASIS_POLICY NONE.
- RUN_ROOT: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- DECOMPOSITION_PATH: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; accepted companion Packages.csv, Deliverables.csv, ScopeLedger.csv and Objectives.csv supply identity/label resolution only. Frozen historical pending labels are not treated as new decisions.
- SOURCE_DOCS, ANCHOR_DOC and EXECUTION_DOC_ORDER: `ScopeOfWork.md` only; DOC_ROLE_MAP DEFAULT. Pass 1 completed before Pass 2. `_REFERENCES.md` read for pointers; citations alone created no execution edges.
- Existing register absent. Added 29 extracted rows; no prior rows to retire. Declared mirror counts: added/refreshed/retired 0; skipped 2 initial-setup placeholders. All human-owned mode and declared sections preserved byte-for-byte; prior history retained.
- PKG-02 receiving granularity remains PACKAGE; no sibling selected by ownership list. DEL-03-03 and DEL-04-03 exclusions create no edges. No source-linked runtime behavior was converted into a production dependency without explicit receipt/handoff/constraint evidence.
- DEL-03-02 has distinct downstream operation/basis supply and upstream proposal-behavior receipt. These information flows do not assert production sequence or global graph closure.
- UNKNOWN targets preserve the unresolved extension-trace/disposition and technical-agreement inputs without inventing artifacts or allocating their production to an App deliverable. Actual decisions and qualification inputs remain limited to affected claims/implementation or live examination; independent definition continues.
- External SWBPIPE contributions remain externally owned; actual delivery/adoption is unclaimed. No host/provider/shared-service construction, live operation choice, blanket acceptance-before-checking gate or stronger human-act standing is inferred.
- Source SHA256 verified against dispatch before extraction: `179a6d355d84dba915daddd746d9d62eb7c8ef483e68122a096dfbde6f6b3b84`; source unchanged and output checks are recorded in `_run_records/dependency-extract-20260927.md`.

- Local validation: schema, all used enums/IDs, source/quote/count/uniqueness and preservation assertions PASS. Optional EVQ/DRB scan returned exit 0; 0 findings for this register, including EVQ-003, EVQ-004 and DRB-006. Full command/result summary is in the single run record.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27 — TASK `/root/renewal_research_strategy/dep_del_03_01` executed UPDATE/CONSERVATIVE from accepted GROUP3-20260928T001055Z canonical decomposition; 29 ACTIVE (21 ANCHOR/8 EXECUTION), 0 RETIRED. No parent-anchor or decomposition warnings; unresolved execution targets and fulfilment remain explicit.
