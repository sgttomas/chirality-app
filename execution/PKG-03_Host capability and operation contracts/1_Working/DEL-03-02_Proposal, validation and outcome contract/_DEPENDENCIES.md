# Dependencies: DEL-03-02 Proposal, validation and outcome contract

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
- **Register:** Dependencies.csv (v3.1; 29 canonical columns)
- **Rows:** 26 ACTIVE / 0 RETIRED; 15 ANCHOR (1 parent, 12 scope traces, 2 objective traces), 11 EXECUTION.
- **Execution:** 5 UPSTREAM / 6 DOWNSTREAM; 7 local DELIVERABLE targets / 4 EXTERNAL targets / 0 UNKNOWN targets.
- **Origin:** 26 EXTRACTED / 0 DECLARED. Initial-setup placeholders are not edges.

| Dependency ID | Class | Direction | Target | Type |
|---|---|---|---|---|
| DEP-03-02-001 | ANCHOR | UPSTREAM | PKG-03 | OTHER |
| DEP-03-02-002 | ANCHOR | UPSTREAM | SOW-070 | OTHER |
| DEP-03-02-003 | ANCHOR | UPSTREAM | SOW-090 | OTHER |
| DEP-03-02-004 | ANCHOR | UPSTREAM | SOW-091 | OTHER |
| DEP-03-02-005 | ANCHOR | UPSTREAM | SOW-170 | OTHER |
| DEP-03-02-006 | ANCHOR | UPSTREAM | SOW-171 | OTHER |
| DEP-03-02-007 | ANCHOR | UPSTREAM | SOW-172 | OTHER |
| DEP-03-02-008 | ANCHOR | UPSTREAM | SOW-173 | OTHER |
| DEP-03-02-009 | ANCHOR | UPSTREAM | SOW-174 | OTHER |
| DEP-03-02-010 | ANCHOR | UPSTREAM | SOW-175 | OTHER |
| DEP-03-02-011 | ANCHOR | UPSTREAM | SOW-176 | OTHER |
| DEP-03-02-012 | ANCHOR | UPSTREAM | SOW-177 | OTHER |
| DEP-03-02-013 | ANCHOR | UPSTREAM | SOW-178 | OTHER |
| DEP-03-02-014 | ANCHOR | UPSTREAM | OBJ-004 | OTHER |
| DEP-03-02-015 | ANCHOR | UPSTREAM | OBJ-005 | OTHER |
| DEP-03-02-016 | EXECUTION | UPSTREAM | DEL-03-01 | PREREQUISITE |
| DEP-03-02-017 | EXECUTION | UPSTREAM | DEL-04-01 | PREREQUISITE |
| DEP-03-02-018 | EXECUTION | DOWNSTREAM | DEL-04-02 | HANDOVER |
| DEP-03-02-019 | EXECUTION | DOWNSTREAM | DEL-04-03 | HANDOVER |
| DEP-03-02-020 | EXECUTION | DOWNSTREAM | DEL-03-03 | HANDOVER |
| DEP-03-02-021 | EXECUTION | DOWNSTREAM | DEL-03-04 | HANDOVER |
| DEP-03-02-022 | EXECUTION | DOWNSTREAM | DEL-09-09 | HANDOVER |
| DEP-03-02-023 | EXECUTION | UPSTREAM | EXTERNAL DEP-001 | PREREQUISITE |
| DEP-03-02-024 | EXECUTION | DOWNSTREAM | EXTERNAL DEP-001 | HANDOVER |
| DEP-03-02-025 | EXECUTION | UPSTREAM | ISSUES OI-014 | CONSTRAINT |
| DEP-03-02-026 | EXECUTION | UPSTREAM | Relevant contract and host owners: agreement on proposal representation and mechanics | CONSTRAINT |

## Lifecycle Summary
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Extraction status: ACTIVE 26; RETIRED 0. Closure: NOT_APPLICABLE 15 (anchors); TBD 11 (execution); SATISFIED 0.
- INITIALIZED is required only as local defined-contract maturity for the 7 Deliverable targets. Actual adopted policy, technical artifacts, owner agreements, host evidence and delivered handoffs remain separately required where stated, with fulfilment unclaimed. External maturity is TBD; proposed maturity is empty.

## Run Notes
- Workflow: `chirality-root:bundled:workflow:dependency-extract`; method basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`; supplied source candidate `ddd721a90ade401d452d102e6e40d1ffdae654eb` / identical-tree integration `82efe62783bbe8ac7d21476a6662195c0b0a7587`.
- SCOPE DEL-03-02; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; ARCHITECTURE_BASIS_POLICY NONE; DOC_ROLE_MAP DEFAULT.
- RUN_ROOT: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- DECOMPOSITION_PATH: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. Canonical companion rows resolve IDs and labels only; preserved historical candidate wording does not undo the accepted snapshot.
- SOURCE_DOCS, ANCHOR_DOC and EXECUTION_DOC_ORDER: `ScopeOfWork.md` only. Pass 1 completed with one parent and fourteen traces before Pass 2 execution extraction. Evidence is exclusively positive local source text, with verbatim quotes of at most 30 words.
- Source SHA256 before/after must remain `42328987c71dd243323805faf2634067cca0113b81ca93d4d129193b2a71128a`. Exact input hashes, checks and output identity are in `_run_records/dependency-extract-20260927.md`.
- No prior CSV existed. Declared mode/upstream/downstream sections preserved byte-for-byte; 2 placeholder entries skipped; mirror rows added/refreshed/retired: 0/0/0. Existing Run History retained.
- Semantics: OI-001/OI-002 are received through DEL-04-01's adopted distinctions; no blanket project hold. OI-014 placement and owner agreement on representation/mechanics remain separate constraints at their points of need. The source supplies no stable decision ID for the latter; its exact local locus is retained, without invented identity.
- Conditional EXTERNAL DEP-001 host evidence is not a prerequisite to independent definition. Host construction and actual human acts retain their owners; faithful recording does not perform the act. Outgoing host-view information is a distinct transfer. Local fixtures do not prove external implementation or joined qualification.
- REQ-013 exclusions, source bibliography, sibling ownership inventories, OI-021 activity selection and OI-003 extension decision do not independently create new local edges. No schedule, accepted project DAG, release, adoption or lifecycle advancement is asserted.
- Local validation results are recorded in the run record; unresolved technical choices are nonfatal extraction limitations, not resolved inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:05:57.943525+00:00 — TASK `/root/renewal_research_strategy/dep_del_03_02`; UPDATE / CONSERVATIVE; explicit accepted decomposition path above; 26 ACTIVE (15 ANCHOR / 11 EXECUTION), 0 RETIRED; no floating/multiple-parent warning; conditional external inputs and open agreements retained.
