# Dependencies: DEL-09-01 Candidate examination infrastructure and evidence protocol

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
- **Status:** EXTRACTED; local checks recorded in the run record.
- **Register:** `Dependencies.csv`, schema v3.1, 29 columns.
- **Rows:** 30 ACTIVE; 0 RETIRED; 12 ANCHOR (1 parent, 11 traces); 18 EXECUTION (8 upstream, 10 downstream); 1 EXTERNAL; 2 UNKNOWN; 0 DECLARED.

| Dependency | Class / direction | Target | Type |
|---|---|---|---|
| DEP-09-01-001 | ANCHOR / UPSTREAM | PKG-09 | OTHER |
| DEP-09-01-002 | ANCHOR / UPSTREAM | SOW-103 | OTHER |
| DEP-09-01-003 | ANCHOR / UPSTREAM | SOW-155 | OTHER |
| DEP-09-01-004 | ANCHOR / UPSTREAM | SOW-189 | OTHER |
| DEP-09-01-005 | ANCHOR / UPSTREAM | SOW-190 | OTHER |
| DEP-09-01-006 | ANCHOR / UPSTREAM | SOW-191 | OTHER |
| DEP-09-01-007 | ANCHOR / UPSTREAM | SOW-192 | OTHER |
| DEP-09-01-008 | ANCHOR / UPSTREAM | SOW-193 | OTHER |
| DEP-09-01-009 | ANCHOR / UPSTREAM | SOW-194 | OTHER |
| DEP-09-01-010 | ANCHOR / UPSTREAM | SOW-229 | OTHER |
| DEP-09-01-011 | ANCHOR / UPSTREAM | OBJ-008 | OTHER |
| DEP-09-01-012 | ANCHOR / UPSTREAM | OBJ-010 | OTHER |
| DEP-09-01-013 | EXECUTION / UPSTREAM | Identified candidate examination basis | PREREQUISITE |
| DEP-09-01-014 | EXECUTION / UPSTREAM | Focused feature-owner evidence | PREREQUISITE |
| DEP-09-01-015 | EXECUTION / UPSTREAM | Identified recorded real protocol exchanges | PREREQUISITE |
| DEP-09-01-016 | EXECUTION / UPSTREAM | DEL-01-06 | PREREQUISITE |
| DEP-09-01-017 | EXECUTION / UPSTREAM | Independently produced candidate review record | PREREQUISITE |
| DEP-09-01-018 | EXECUTION / UPSTREAM | Evidence of an actually performed human act | PREREQUISITE |
| DEP-09-01-019 | EXECUTION / UPSTREAM | DEL-01-01 | CONSTRAINT |
| DEP-09-01-020 | EXECUTION / UPSTREAM | External Domains receiving owners — later research-fixture admission input | PREREQUISITE |
| DEP-09-01-021 | EXECUTION / DOWNSTREAM | DEL-01-06 | HANDOVER |
| DEP-09-01-022 | EXECUTION / DOWNSTREAM | DEL-09-02 | HANDOVER |
| DEP-09-01-023 | EXECUTION / DOWNSTREAM | DEL-09-05 | HANDOVER |
| DEP-09-01-024 | EXECUTION / DOWNSTREAM | DEL-09-06 | HANDOVER |
| DEP-09-01-025 | EXECUTION / DOWNSTREAM | DEL-09-07 | HANDOVER |
| DEP-09-01-026 | EXECUTION / DOWNSTREAM | DEL-09-09 | HANDOVER |
| DEP-09-01-027 | EXECUTION / DOWNSTREAM | DEL-09-10 | HANDOVER |
| DEP-09-01-028 | EXECUTION / DOWNSTREAM | DEL-09-11 | HANDOVER |
| DEP-09-01-029 | EXECUTION / DOWNSTREAM | DEL-09-12 | HANDOVER |
| DEP-09-01-030 | EXECUTION / DOWNSTREAM | Candidate independent reviewer | HANDOVER |

---

## Lifecycle Summary
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Extraction: ACTIVE 30; RETIRED 0. Closure: NOT_APPLICABLE 12 (anchors); TBD 18 (execution); SATISFIED 0.
- No lifecycle/status act was performed by this extraction.

---

## Run Notes

### Initial extraction — 2026-09-27 (historical)
- Initialized under the approved coordination policy.
- Run 2026-09-27: `chirality-root:bundled:workflow:dependency-extract`; `MODE=UPDATE`; `STRICTNESS=CONSERVATIVE`; `CONSUMER_CONTEXT=NONE`; `ARCHITECTURE_BASIS_POLICY=NONE`; `DOC_ROLE_MAP=DEFAULT`.
- `SCOPE=DEL-09-01`; `SOURCE_DOCS=ScopeOfWork.md`; `ANCHOR_DOC=ScopeOfWork.md`; `EXECUTION_DOC_ORDER=[ScopeOfWork.md]`. Both passes used only this source; the 12-anchor pass completed before execution extraction.
- `RUN_ROOT=/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- `DECOMPOSITION_PATH=/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; accepted companion rows resolved parent/scope/objective/Deliverable labels; dispatch rows resolved current local paths.
- Source SHA256 before/after: `8e53669468bd5885739ceaeb633dc5a3b134a04f1bf862235d8d2272dd5f658a`. Source, references and decomposition were not changed.
- Human-owned mode/upstream/downstream bytes are preserved. Both `None declared at initial setup` entries are placeholders, so declared mirrors added/refreshed/retired: 0/0/0; placeholders skipped: 2. No prior CSV existed; 30 extracted rows added, none retired.
- Local Deliverable `RequiredMaturity=INITIALIZED` records the approved contract threshold only. Actual candidate, focused evidence, exchanges, packaged application, review and human-act inputs stay at their stated examination/check points. All 18 execution rows retain `SatisfactionStatus=TBD`; no delivery, qualification, acceptance, release or adoption is inferred.
- REQ-008 contains a positive support/evidence-interface handoff to its named owners, supporting nine downstream rows. CLM-005 and the exclusion list alone produce no edge. Candidate-specific reviewer results have a separate, unresolved recipient identity. The support handoff to packaging and the package/evidence input describe distinct transfers, not a scheduling cycle or a project-DAG decision.
- Three UNKNOWN targets preserve unresolved actual candidate basis, selected Codex pin and independent reviewer identity; four DOCUMENT targets have no supplied artifact path. One EXTERNAL target retains conditional later Domains admission responsibility/input. No PEC or external SWB Deliverable number was mapped to App; Domains provider construction/deployment/allocation and additional host/platform scope remain undecided.
- Other TBD-001 owner/point-of-need inventory is retained in the source rather than expanded into speculative edges. Existing policy/criterion choices constrain only affected work; human acts remain separate; optional connectors and absence fallback are not blanket project gates. OI-015 is resolved in the source.
- Verification methods are future checks, not executed candidate results or supplied qualification. Historical candidate passes, replay/browser results, actual native/host witnesses and human acts retain their separate standing. No fixed run quota, validation period or numeric fitness criterion is invented.
- Local check results and actual read-source hashes are recorded in `_run_records/dependency-extract-20260927.md`. No downstream closure or graph assembly is claimed.

### Target resolution UPDATE — 2026-09-28 (UTC)
- Bounded R2 repair under `chirality-root:bundled:workflow:dependency-extract`: only `DEP-09-01-019` target/provenance fields and its `LastSeen` changed. All other rows remain byte-identical. `MODE=UPDATE`; `STRICTNESS=CONSERVATIVE`; `CONSUMER_CONTEXT=NONE`; `ARCHITECTURE_BASIS_POLICY=NONE`; `DOC_ROLE_MAP=DEFAULT`; `SCOPE=DEL-09-01`; source/anchor/execution source remains `ScopeOfWork.md`, and run/decomposition paths remain those recorded above.
- Pass 1 rechecked the 12 existing anchors (one parent and 11 traces) against the local source and accepted G3 records before Pass 2 resolved the pin-producing obligation. Accepted provenance: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv#SOW-135` and `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv#DEL-01-01`; the supplied `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/TARGET_RESOLUTION.md` R2 records prior independent producer `OUT-002/REQ-006` proof. No other deliverable source was read in this repair.
- Current counts: 30 ACTIVE, 0 RETIRED; 12 ANCHOR; 18 EXECUTION (8 upstream, 10 downstream); 1 EXTERNAL; 2 UNKNOWN (actual candidate basis and candidate-specific independent reviewer). Four DOCUMENT artifact paths remain unresolved. The actual Codex version, decision artifact and qualification remain open under OI-012. `RequiredMaturity=TBD`, blank `ProposedMaturity`, `SatisfactionStatus=TBD`, statement and evidence are preserved; no historical version is selected and independent support definition continues.
- Human-owned sections and prior history are preserved; declared mirrors added/refreshed/retired: 0/0/0; initial-setup placeholders skipped: 2. Source SHA256 remains `8e53669468bd5885739ceaeb633dc5a3b134a04f1bf862235d8d2272dd5f658a`; prior run record, references and status are unchanged. Local schema/enums/IDs, quotes, anchors, duplicates and preservation checks are recorded in `_run_records/dependency-target-resolution-20260928.md`. No global checks, graph changes, delivery, satisfaction or lifecycle act are claimed.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27 — TASK dependency-extract; UPDATE/CONSERVATIVE; accepted Group3 decomposition available; 30 ACTIVE (12 ANCHOR, 18 EXECUTION), 0 RETIRED; no missing/ambiguous parent or decomposition warning; unresolved input/recipient identities and optional later admission remain explicit.
- 2026-09-28T04:27:30.851032+00:00 — TASK bounded R2 target resolution; UPDATE/CONSERVATIVE; accepted Group3 basis available; DEP-09-01-019 producer resolved to DEL-01-01. 30 ACTIVE (12 ANCHOR, 18 EXECUTION), 0 RETIRED; 1 EXTERNAL, 2 UNKNOWN. One parent; no parent/decomposition warning. Actual pin/qualification and all fulfilment remain unresolved.
