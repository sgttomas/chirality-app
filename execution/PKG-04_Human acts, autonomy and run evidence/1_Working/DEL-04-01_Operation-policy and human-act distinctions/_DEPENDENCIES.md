# Dependencies: DEL-04-01 Operation-policy and human-act distinctions

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

- **Status:** EXTRACTED; canonical Dependencies.csv v3.1.
- **ACTIVE:** 21 total — 11 ANCHOR (1 parent, 10 scope/objective traces), 10 EXECUTION (5 downstream handoffs, 5 upstream external inputs/constraints).
- **RETIRED:** 0. **EXTERNAL:** 5. **UNKNOWN:** 0. **DECLARED:** 0.

| Dependency | Class / type | Direction | Target |
|---|---|---|---|
| DEP-04-01-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-04 |
| DEP-04-01-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-074 |
| DEP-04-01-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-079 |
| DEP-04-01-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-082 |
| DEP-04-01-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-179 |
| DEP-04-01-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-180 |
| DEP-04-01-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-181 |
| DEP-04-01-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-182 |
| DEP-04-01-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-235 |
| DEP-04-01-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 |
| DEP-04-01-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 |
| DEP-04-01-012 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-01 |
| DEP-04-01-013 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 |
| DEP-04-01-014 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-01 |
| DEP-04-01-015 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 |
| DEP-04-01-016 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 |
| DEP-04-01-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 |
| DEP-04-01-018 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 |
| DEP-04-01-019 | EXECUTION / PREREQUISITE | UPSTREAM | projects/chirality-app-v4/execution/_Decomposition/External_Dependencies.csv#DEP-001 |
| DEP-04-01-020 | EXECUTION / PREREQUISITE | UPSTREAM | Person setting operation/consequence scope — recorded grant |
| DEP-04-01-021 | EXECUTION / PREREQUISITE | UPSTREAM | Person performing the human act — attributable evidence for faithful-recording case |

## Lifecycle Summary

- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Register lifecycle: ACTIVE 21; RETIRED 0.
- Closure states: NOT_APPLICABLE 11 (anchors); TBD 10 (execution). No execution dependency is marked SATISFIED.

## Run Notes

- Parameters: SCOPE DEL-04-01; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; DOC_ROLE_MAP DEFAULT; ARCHITECTURE_BASIS_POLICY NONE.
- SOURCE_DOCS, ANCHOR_DOC and EXECUTION_DOC_ORDER: ScopeOfWork.md only, with the ANCHOR pass completed before the EXECUTION pass.
- RUN_ROOT: /Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution.
- DECOMPOSITION_PATH: /Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md; available. Accepted companion rows resolve canonical labels and IDs; the dispatch table resolves current local paths. Historical candidate labels in frozen bytes are retained as qualified by the source contract and dispatch brief.
- Source SHA256 verified before and after: fc1a0503abad4196e869402b664bd76280773d197b5c77994c34e858a406f5e6. No source, reference, status, sibling, decomposition or instruction file was modified.
- Five local consumers are supported by CLM-002's positive policy-meaning supply statement. DEL-05-01/DEL-05-02 ownership, exclusions, source citations and runtime behavior rules alone were not extracted as production edges.
- OI-001/OI-002 remain open at the affected concrete policy points of need. DEP-001 remains external and its actual host evidence is required only for corresponding host assertions. Local contract definition/conformance may continue independently.
- VER-001 requires recorded person-set scope for comparison. VER-002 explicitly requires actual-act evidence for its positive faithful-recording case: the human decision actor differs from an agent recorder; no act, permission, professional standing or synthetic acceptance prerequisite is created. Actors/evidence locations are not identified here and remain TBD.
- INITIALIZED is the local Deliverable contract threshold for the five handoffs; actual policy content, applicable adopted decisions, external evidence and human acts remain separate and unfulfilled/unassessed. All EXECUTION SatisfactionStatus values are TBD; all ANCHOR values are NOT_APPLICABLE.
- Declared mirroring: added 0; refreshed 0; retired 0; skipped 2 initial-setup placeholders. Human-owned sections are byte-identical. Previous Run History is preserved; no prior register rows existed.
- Checks: canonical29 schema, all used enum values, applicable stable-ID formats, one parent, unique IDs/semantic edges, verbatim quotes of at most 30 words, evidence completeness, target placement, source hash and summary counts passed. Source-local OI-001/OI-002 and qualified external DEP-001 references are retained as external source identities, not coerced into DependencyID format. Optional whole-execution EVQ/DRB scan not run; equivalent local blank-quote, placeholder-locus and prefix checks passed.
- Structural warnings: none. Scope is deliverable-local extraction; no graph closure, adoption, product readiness, release or lifecycle advancement is claimed.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:25:20Z — TASK dependency-extract; UPDATE / CONSERVATIVE; decomposition projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md available; ACTIVE 21 (ANCHOR 11 / EXECUTION 10), RETIRED 0; structural warnings none; external/point-of-need inputs remain unassessed.
