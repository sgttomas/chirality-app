# Handoff State — D-GOV-11 Agent Hierarchy Refactor

Status: COMPLETE / MERGED TO MAIN
DecisionBasis: `docs/governance_harness/_DECISIONS/D-GOV-11_runtime_agent_hierarchy.md`; `docs/governance_harness/_DECISIONS/D-GOV-12_multi_agent_orchestration.md`
Branch: `codex/agent-governance-redesign`
IntegrationPR: `#188`
IntegrationCommit: `a0dc7be326a8aa05e0c34ee2fbc7085264aad888`

## Accepted Direction

- HELP_HUMAN is sole Agent 0 Supervising Architect.
- Agent 1 managers are direct human entry points and may run under Agent 0.
- Agent 2 may be TASK, ephemeral generalist, or approved dedicated specialist.
- Standards are external constraints, not agents.
- Runtime delegation is hierarchical; filesystem and Git state provide many-to-many coordination.
- EVALUATION owns generic audit/reconciliation semantics.
- RECONCILIATION is reserved for deliverable-corpus concordance.
- PDF2MD and DRAWING_EXTRACT remain Agent 1.
- Terminal fan-out/fan-in and supervised many-to-many agency are complementary
  canonical patterns; mixed work graphs are allowed.
- WORKING_ITEMS is a package-level Agent 1 and SOFTWARE_DEV is deferred.

## Implemented in This Instruction Tranche

- Canonical doctrine in `AGENTS.md`; exact `CLAUDE.md` import and validator/export enforcement.
- HELPS_HUMANS consolidated component design, skill/tool design, context transposition, and decomposition-component design.
- HELP_HUMAN rewritten as sole read-only Agent 0 with managed delegation; durable launch briefs are runtime evidence, not an execution fallback.
- `docs/DECOMPOSITION_STANDARD.md` extracted; DECOMP_BASE persona removed and live managers rebound.
- EVALUATION expanded; old generic RECONCILIATION semantics transferred.
- RECONCILIATION activated from the ratified method and integrated app-dev and
  piping calibration/pause evidence.
- SCHEDULING merged into ORCHESTRATOR; SKILLMAKER, TOOLMAKER, CONTEXT_TRANSPOSE, and SCHEDULING persona files removed after live caller redirection.
- PDF2MD and DRAWING_EXTRACT source/target calibration and novel-generalist semantics added.
- D-GOV-12 doctrine, package-level WORKING_ITEMS, cross-package HELP_HUMAN,
  orchestration vocabulary, and managed-runtime record schema added.
- DBM, disposition matrix, TYPES, DIRECTIVE, README, professional-engineering mapping, roadmap, validators, skill/tool ownership, and export contract updated.
- App-dev and piping loops now use package-level WORKING_ITEMS work graphs.
- Project software profiles, five software TASK skills, and deterministic
  discovery/check/scope/comparison/drift tools are live.
- Managed child sessions, terminal/background execution, coordination notices,
  updates, amendments, acknowledgments, runtime records, actual named
  instruction loading, and fail-closed retirement of the record-less SDK
  compatibility path are implemented.
- Completion-audit hardening enforces child read scopes and write targets at
  permission/hook boundaries, fails closed on unbounded managed Bash, validates
  return markers, versions replans, injects updates at safe turn boundaries,
  requires acknowledgments, reconstructs handoff state, and isolates failures.
- Current generic audit and REVIEW snapshots write under `_Evaluation/`;
  historical generic `_Reconciliation/` snapshots remain immutable evidence.
  RECONCILIATION alone owns new deliverable-corpus concordance runs.
- D-GOV-13 records the approved fourteen-role requalification baseline with
  persistent output/recovery and live-reference compatibility evidence. Named
  execution remains subject to every declared runtime gate.

## Validation Evidence

The owner-ruled, SHA-bound candidate has the following verified completion
evidence:

- Root governance/tool checks: 333 practitioner-harness, validation, and
  software-workflow tests pass; instruction entrypoints pass; all 43 live
  skills validate; all 33 agent packages validate with zero errors or warnings;
  434 source path-anchor surfaces pass; and every numbered review finding
  (C01-C61, H01-H04, and V01-V08) has a tested disposition.
- App-dev: the merged Vitest suite passes 97 files (one skipped), 699 tests
  (four skipped); TypeScript typechecking, generated tool-catalog identity,
  desktop packaging/building, and byte identity for all 43 packaged instruction
  files pass. The live premerge probe passes all 8 Section 8 scenarios and all
  16 Section 9 report-only gates. The D-APP-55 R6 handoff is `CLOSED / PASS`.
- Piping: the post-integration evidence sweep passes tests for all 36 Rust crate
  manifests, 496 Python tests, 476 desktop Vitest tests, 18 development
  Playwright tests, the production-distribution WASM Playwright test, and the
  production build. Its evidence is commit-bound to `b8a5e15d`.
- The public derivative regenerates with 586 files and zero boundary findings.
  Its independent staging tree passes all 33 agent packages, all 43 skills,
  canonical instruction entrypoints, and 425 exported path-anchor surfaces.
- `CLAUDE.md` is exactly the one-line `@AGENTS.md` import, HELP_HUMAN is the
  only live Agent 0, the standards are ratified at
  `ee35409f5cf3a81ecb29a271527156b991df97b9`, and the D-GOV-13/D-GOV-14 ruling
  publication commit resolves as
  `d22f80bf5d6c1190ce151df75d936bfcf4d38bc3`.
- The post-ruling validator no longer emits `TYPE2_APPROVAL_NOT_RULED`.

The following was the accepted pre-review evidence at PR #188 head before the
review-remediation tranche. It is retained as historical evidence, not as a
claim about the current unvalidated remediation tree:

- Root governance/tool suite: 762 tests passed. Agent hierarchy/output-root,
  project-loop/entrypoint, skill, and path validators pass with 33 agent
  packages at zero errors and zero warnings and all 43 live skills valid.
- App-dev runtime: TypeScript typecheck passed; the complete Vitest suite passed
  94 files (one skipped), 682 tests (four skipped). The unsigned desktop package
  built; packaged instruction-root integrity passed; the live premerge probe
  passed 8 Section 8 scenarios and 16 Section 9 gates.
- Piping: the complete evidence sweep passed 36 Rust crate tests, 459 Python
  tests, 471 desktop unit/component tests, 18 development browser-flow tests,
  the production-distribution WASM test, and the desktop production build.
- Path-anchor and instruction-entrypoint validators passed. `git diff --check`
  reported no whitespace errors.
- Public derivative regenerated from the audit-repair commit with 585 manifest
  entries and zero boundary findings. Its staging tree independently passed the
  agent, instruction-entrypoint, skill-metadata, and path-anchor validators.

## Deferred Evolution

- Continue slimming retained Agent 1 roles around human decisions and handoffs
  when use evidence identifies a safe replacement-first migration.
- Reconsider `SOFTWARE_DEV` only if WORKING_ITEMS plus the software activation
  profile, TASK skills, and deterministic tools prove insufficient in practice.

## Integration Hold

The owner ratified the three standards and approved D-GOV-13 through D-GOV-14,
published at `d22f80bf5d6c1190ce151df75d936bfcf4d38bc3`.
The app-dev proto-run is `CLOSED / PASS`; its accepted changes and R6 terminal
handoff are integrated from `main`. The piping D-41 proto-run is also closed;
its distributed terminal package and accepted R4/R5 changes are integrated
from `main`. The owner confirmed on 2026-07-12 that a
non-rewriting merge of `main` satisfies D-GOV-14 item 8 in place of a literal
history-rewriting rebase, preserving the SHA-bound D-GOV-13/D-GOV-14 ruling
commits. PR #188 must not merge until full packaging, live-premerge,
piping-sensitive, independent public-staging, and completion-audit validation
passes. Those local gates and the hosted governance check passed. PR #188 was
merged to `main` with history-preserving merge commit
`a0dc7be326a8aa05e0c34ee2fbc7085264aad888` on 2026-07-12.

## Required Resume Sequence

All required resume steps are complete: the completion-audit commit was pushed,
the hosted check passed, PR #188 merged with history preserved, and this narrow
provenance closeout records the integration commit.

## Closure Verdict

Instruction tranche: OWNER-RULED; COMPLETION AUDIT PASS.
RECONCILIATION activation: COMPLETE.
Runtime bridge: REMEDIATED; FULL LOCAL ACCEPTANCE PASS.
Overall D-GOV-11 implementation: owner-approved; both proto-runs integrated;
merged to `main` at `a0dc7be326a8aa05e0c34ee2fbc7085264aad888`.

## Known Non-Blocking Residuals

- App-dev instruction source-completeness remains `needs_remediation` solely
  because the existing KG-001 `examples/` asset is absent. Packaged instruction
  byte identity passes, so this is a product-content residual, not an
  instruction-bundle mismatch or a release claim from this governance tranche.
- Piping `npm ci` reports four existing audit advisories (two low, two high),
  and the production build retains its existing chunk-size warning. No
  dependency mutation or security-remediation claim is included in PR #188.
