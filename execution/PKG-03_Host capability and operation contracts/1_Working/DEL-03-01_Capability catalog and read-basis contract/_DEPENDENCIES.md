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
- **Counts:** 30 ACTIVE extracted rows: 21 ANCHOR (1 parent + 18 scope + 2 objective) and 9 EXECUTION (7 upstream + 2 downstream); 0 RETIRED; 0 DECLARED; 3 EXTERNAL and 1 UNKNOWN targets.

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
| DEP-03-01-027 | EXECUTION UPSTREAM | Owner with host contract owner — automatic catalog-extension disposition (OI-003) |
| DEP-03-01-028 | EXECUTION UPSTREAM | App/shared and affected host/consumer technical agreement |
| DEP-03-01-029 | EXECUTION UPSTREAM | Owner via outside SWB session and App/shared owner: connected examination inputs |
| DEP-03-01-030 | EXECUTION UPSTREAM | DEL-09-09 candidate-bound extension trace and generated/adapted-work account; ruling remains DEP-03-01-027 |

## Lifecycle Summary
- 30 ACTIVE extracted rows: 21 ANCHOR (1 parent + 18 scope + 2 objective) and 9 EXECUTION (7 upstream + 2 downstream); 0 RETIRED; 0 DECLARED; 3 EXTERNAL and 1 UNKNOWN targets.
- Satisfaction: 21 NOT_APPLICABLE anchors; 9 PENDING execution inputs/handoffs; 0 SATISFIED.
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Existing local-deliverable RequiredMaturity=INITIALIZED is a checked contract threshold; actual technical inputs, agreements, human acts and host evidence remain separate conditions at their stated points of need. R6 preserves RequiredMaturity=TBD for both the actual owner ruling (DEP-03-01-027) and candidate-bound trace (DEP-03-01-030); ProposedMaturity remains blank and both inputs remain PENDING.

## Run Notes
- Workflow: `chirality-root:bundled:workflow:dependency-extract`; SCOPE DEL-03-01; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; ARCHITECTURE_BASIS_POLICY NONE.
- RUN_ROOT: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- DECOMPOSITION_PATH: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; accepted companion Packages.csv, Deliverables.csv, ScopeLedger.csv and Objectives.csv supply identity/label resolution only. Frozen historical pending labels are not treated as new decisions.
- SOURCE_DOCS, ANCHOR_DOC and EXECUTION_DOC_ORDER: `ScopeOfWork.md` only; DOC_ROLE_MAP DEFAULT. Pass 1 completed before Pass 2. `_REFERENCES.md` read for pointers; citations alone created no execution edges.
- Initial extraction (2026-09-27): existing register absent. Added 29 extracted rows; no prior rows to retire. Declared mirror counts: added/refreshed/retired 0; skipped 2 initial-setup placeholders. All human-owned mode and declared sections preserved byte-for-byte; prior history retained.
- PKG-02 receiving granularity remains PACKAGE; no sibling selected by ownership list. DEL-03-03 and DEL-04-03 exclusions create no edges. No source-linked runtime behavior was converted into a production dependency without explicit receipt/handoff/constraint evidence.
- DEL-03-02 has distinct downstream operation/basis supply and upstream proposal-behavior receipt. These information flows do not assert production sequence or global graph closure.
- R6 resolves the extension-trace producer to DEL-09-09 and preserves the separate external OI-003 ruling with Owner with host contract owner. The remaining UNKNOWN target is the App/shared and affected host/consumer technical agreement. Actual decisions and qualification inputs remain limited to affected claims/implementation or live examination; independent definition continues.
- External SWBPIPE contributions remain externally owned; actual delivery/adoption is unclaimed. No host/provider/shared-service construction, live operation choice, blanket acceptance-before-checking gate or stronger human-act standing is inferred.
- Source SHA256 verified against dispatch before extraction: `179a6d355d84dba915daddd746d9d62eb7c8ef483e68122a096dfbde6f6b3b84`; source unchanged and output checks are recorded in `_run_records/dependency-extract-20260927.md`.

- Initial extraction validation (2026-09-27): schema, all used enums/IDs, source/quote/count/uniqueness and preservation assertions PASS. Optional EVQ/DRB scan returned exit 0; 0 findings for this register, including EVQ-003, EVQ-004 and DRB-006. Its command/result summary remains in `_run_records/dependency-extract-20260927.md`.

- Target-resolution repair (2026-09-28): applied only R6 from `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/TARGET_RESOLUTION.md` (SHA256 `f85a371853ec5ef18d3a1b1ebdc016e37e1bbd321217f726c4350204a2cefaa1`). Accepted G3 provenance is `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv` SOW-073/SOW-203, `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` DEL-09-09 and `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Open_Issues.csv` OI-003. Producer OUT-002/OUT-003 proof is supplied by that independently authored report; no other deliverable SoW was read in this repair.
- Local repair checks: schema, all used enum values and supported stable-ID formats; exact 21-anchor preservation; source/quote/ID/semantic-key/count/target-binding and byte-preservation assertions PASS. The original DEP-03-01-027 ID, timestamps and full AC-007 quote remain; the new DEP-03-01-030 uses the actual UTC repair date and the same quote. All 28 unrelated rows are byte-identical. Human-owned sections, prior history and old run record remain unchanged. Evidence: `_run_records/dependency-target-resolution-20260928.md`.
- The new DEL-03-01 → DEL-09-09 arc records a trace input before the dependent extension claim; it creates no universal initial-definition prerequisite, owner ruling, narrower criterion, satisfaction or graph closure. Refreeze the complete candidate and refresh global closure downstream after owning repairs and independent review. No global check ran amid concurrent peer repairs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27 — TASK `/root/renewal_research_strategy/dep_del_03_01` executed UPDATE/CONSERVATIVE from accepted GROUP3-20260928T001055Z canonical decomposition; 29 ACTIVE (21 ANCHOR/8 EXECUTION), 0 RETIRED. No parent-anchor or decomposition warnings; unresolved execution targets and fulfilment remain explicit.
- 2026-09-28 — TASK `/root/renewal_research_strategy/resolve_dep_03_01` executed bounded R6 UPDATE/CONSERVATIVE against accepted GROUP3-20260928T001055Z and target-resolution report: 30 ACTIVE (21 ANCHOR/9 EXECUTION), 0 RETIRED; 3 EXTERNAL/1 UNKNOWN. Parent-anchor and local checks pass; actor ruling and actual trace remain PENDING; global closure refresh is downstream.
