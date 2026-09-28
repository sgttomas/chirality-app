# Dependencies: DEL-02-04 Additive role selection and supply

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

- Canonical register: `Dependencies.csv` (v3.1; 29 columns).
- Total/ACTIVE: **16**; RETIRED: **0**. ANCHOR: **9** (1 parent, 8 traces); EXECUTION: **7** (5 UPSTREAM, 2 DOWNSTREAM).
- Target types: WBS_NODE 1; REQUIREMENT 8; DELIVERABLE 4; EXTERNAL 3; UNKNOWN 0.
- EXTRACTED: 16; DECLARED: 0. All evidence comes from `ScopeOfWork.md` with precise loci and verbatim quotations of at most 30 words.

| DependencyID | Class / relation | Direction | Target | Satisfaction |
|---|---|---|---|---|
| DEP-02-04-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-02 | NOT_APPLICABLE |
| DEP-02-04-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-013 | NOT_APPLICABLE |
| DEP-02-04-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-057 | NOT_APPLICABLE |
| DEP-02-04-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-058 | NOT_APPLICABLE |
| DEP-02-04-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-059 | NOT_APPLICABLE |
| DEP-02-04-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-126 | NOT_APPLICABLE |
| DEP-02-04-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | NOT_APPLICABLE |
| DEP-02-04-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | NOT_APPLICABLE |
| DEP-02-04-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-003 | NOT_APPLICABLE |
| DEP-02-04-010 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | PENDING |
| DEP-02-04-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | PENDING |
| DEP-02-04-012 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | PENDING |
| DEP-02-04-013 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-11-02 | PENDING |
| DEP-02-04-014 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-006 | PENDING |
| DEP-02-04-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-008 | PENDING |
| DEP-02-04-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-018 | PENDING |

## Lifecycle Summary

- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- ACTIVE 16; RETIRED 0. Satisfaction: NOT_APPLICABLE 9 (anchors); PENDING 7 (execution); SATISFIED 0.
- RequiredMaturity INITIALIZED appears only on 4 local Deliverable interfaces as the approved contract-maturity default. Actual technical contracts, applicable allocations and evidence handoffs remain required separately. Non-Deliverable maturity remains TBD; ProposedMaturity is blank throughout. This extraction does not establish closure, qualification, adoption or release.

## Run Notes

- Initialized under the approved coordination policy. Dependency extraction now completed by bounded native TASK `/root/renewal_research_strategy/dep_del_02_04`, parent WORKING_ITEMS `/root/renewal_research_strategy`, root HELP_HUMAN `/root`; no child delegation.
- Method: `chirality-root:bundled:workflow:dependency-extract`; selected source basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`, unchanged setup source `ddd721a90ade401d452d102e6e40d1ffdae654eb` / identical-tree main integration `82efe62783bbe8ac7d21476a6662195c0b0a7587` (identities supplied by manager brief; actual read hashes recorded locally).
- SCOPE DEL-02-04; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; ARCHITECTURE_BASIS_POLICY NONE; DOC_ROLE_MAP DEFAULT. SOURCE_DOCS, ANCHOR_DOC and EXECUTION_DOC_ORDER each resolve solely to `ScopeOfWork.md`.
- RUN_ROOT: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`.
- DECOMPOSITION_PATH: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; present. Accepted companion rows resolve canonical names/IDs only; dispatch rows resolve current local paths. No sibling SoW was read or used as evidence.
- Pass 1 completed first: explicit PKG-02 parent and five SOW / three OBJ trace anchors. Pass 2 records two upstream receiving contracts, two downstream role-evidence handoffs, the actual-adoption witness input and two direct owner-choice constraints. Existing CSV absent; no old rows to retire.
- Declared sections and mode preserved byte-for-byte. Two `None declared at initial setup` placeholders skipped; mirror rows added/refreshed/retired: 0/0/0. Initial history retained.
- OI-012 supplier pin and OI-014 shared placement remain conditions of their actual receiving-contract inputs. OI-008 and OI-018 keep their named owners and exact points of need. OI-024 and external DEP-006 remain scoped to actual adoption/retirement and the VER-005 positive witness, without creating a prerequisite between distinct human acts.
- OI-001 reserved acts and OI-002 routine permissions remain with Owner with App/SWB contract owners, respectively Before operation-policy production contracts and Before permission-policy implementation. Their local text excludes role selection from deciding policy; it is not positive evidence of an incoming DEL-04-01 production handoff, so no such edge was invented.
- OI-017's source-bound owner/point remains Owning project-definition manager / Before dependent execution relies on manual editions. `_REFERENCES.md` identifies a later scoped CURRENT_EXECUTION_BASIS disposition; that record was not loaded. No unverified current manual decision or duplicate generic product dependency is asserted here.
- Host-loop/panel ownership, an unenforceable-role fixture, optional legacy reuse, sibling exclusions and reference listings alone create no production dependency. No external host construction edge, fifth role, common service, supplier version, wire field or new enforcement feature is inferred.
- Nonfatal limits: actual inputs and owner choices have not been supplied/verified by this extraction; provider-internal facts remain unknown when unobserved. Source locations support all targets; no UNKNOWN target or unresolved target identity remains. Global DAG assembly and closure remain downstream.
- Required schema, every used canonical enum and supported ID-format checks passed; one parent, unique IDs/semantic rows, complete evidence, verbatim quotations, human-section preservation, source hash and counts passed. Detailed summarized validation and source/output hashes: `_run_records/dependency-extract-20260927.md`. Optional whole-execution EVQ/DRB scan not run; local checks cover equivalent quote/locus/prefix conditions.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27 — TASK dependency-extract; UPDATE / CONSERVATIVE; explicit GROUP3-20260928T001055Z decomposition present; ACTIVE 16 (ANCHOR 9, EXECUTION 7), RETIRED 0; no mandatory integrity warning. Actual execution timestamp and verification evidence recorded in `_run_records/dependency-extract-20260927.md`.
