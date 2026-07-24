# D-GOV-15 — Deliverable Scope-of-Work Stage 1

Status:       RULED
HumanRuling:  APPROVED — owner response, 2026-07-12: "I rule APPROVED for all nine. Incorporate this, but do not proceed with implementation."
Proposed SHA: c4c5dd2df0d7b5424d48672c38d1eef37262e2f6
Ruling SHA:   58aa81d62f4a32e3c2d687e4356a1e4be8141674
Date:         2026-07-12
FramedBy:     deliverable Scope-of-Work architecture assessment and Stage-1 plan
EvidenceBasis: `67ba77e5107f941e6fcc7382ef467b6b018e972d`

## Decision requested

The owner is asked to rule on the following Stage-1 slate as one bounded
architecture-and-pilot authorization. Authorship, registration, tests, or a
Git commit do not approve any item.

1. **Authorize candidate architecture and machinery.** Permit HELPS_HUMANS to
   design the candidate `chirality-deliverable-sow/v1` schema, skill, tools,
   validators, registries, format resolver, compatibility behavior, and
   deprecation plan. Canonical candidate truth is `ScopeOfWork.md`.
   `ScopeOfWork.html` is deterministic, generated on demand, untracked,
   source-hash/version stamped, script-free, and never authoritative.
   `_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`,
   `_SEMANTIC.md`, and structured dependency/evidence surfaces remain
   separate homes and outside the production-document consolidation.

2. **Authorize the candidate typed grammar.** The candidate carries explicit
   objective traceability and the practical ontology, epistemology,
   praxeology, and axiology sections. Register local `OUT-NNN`, `CLM-NNN`,
   `REQ-NNN`, `AC-NNN`, `VER-NNN`, `AX-NNN`, `TBD-NNN`, `CON-NNN`, and
   `REM-NNN` kinds, with externally qualified references such as
   `DEL-07-03-AC-001`. Validation is membership-driven from the eventual
   catalog. REVIEW consumes deliverable `AC-*` records directly. Migration
   dispositions are `PRESERVED`, `MERGED`, `SPLIT`, `SUPERSEDED`, `DEFERRED`,
   and `CONFLICT`; they are not epistemic labels or lifecycle states.
   Candidate frontmatter must declare `schema`, `deliverable_id`,
   `package_id`, `decomposition_basis`, `project_scope_refs`, and
   `package_objective_refs`. Its required human-facing sections are “Purpose
   and Objective Traceability,” “Deliverable Definition — Ontology,”
   “Completion and Reliance Basis — Epistemology,” “Production and
   Verification Method — Praxeology,” “Governing Values and Decisions —
   Axiology,” and “Output and Evaluation Matrix.” These are Stage-1 candidate
   constraints, not ratified successor canon.

3. **Limit Stage 1 to project deliverables and ten pilot candidates.** The
   live sizing basis is 53 App Dev plus 101 Piping deliverables (154 total), as
   recorded in
   `docs/governance_harness/SCOPE_OF_WORK_STAGE1_SIZING_REPORT.md`.
   DOMAIN/KTY, archives, templates, fixtures, exports, generated trees, and
   analogous independent schemas are out of scope. Stage 1 covers only the
   six App Dev PKG-07 and four Piping PKG-13 `IN_PROGRESS` deliverables named
   by the paths below. It does not authorize conversion of the other 144
   deliverables.

4. **Grant a narrow pilot variance if this slate is approved.** Only isolated
   pilot worktrees may contain candidate `ScopeOfWork.md` beside the ratified
   four-document kit under these exact path prefixes:

   ```text
   projects/chirality-app-dev/execution/PKG-07_Filesystem_Execution_Lifecycle_and_Dependencies/1_Working/
   projects/chirality-piping/execution/PKG-13_Physical Design Knowledge and Constraint Engine/1_Working/
   ```

   The variance overrides only the current `TYPES.md`/`SPEC.md` requirement
   that these pilot candidates have an unambiguous single production format.
   The four source documents remain authoritative. Candidate pilot documents
   do not merge to `main` in Stage 1. All other authority, scope, provenance,
   permission, lifecycle, and human-gate rules remain in force. This proposed
   record does **not** activate the variance before the owner rules it.

5. **Require lifecycle and content neutrality.** Conversion preserves current
   lifecycle state and leaves `_STATUS.md` byte-identical. REVIEW may derive a
   candidate checklist but performs no Stage-1 lifecycle transition. The
   Piping `ISSUED` baseline is excluded. Reorganization is permitted; a new or
   changed substantive claim, objective, requirement, criterion, authority,
   or scope is `CONFLICT` and routes to SCOPE_CHANGE or the human rather than
   being silently accepted as migration.

6. **Authorize qualified native orchestration with sequential fallback.** A
   platform-native hierarchical TASK/subagent facility may execute the pilots
   only if it freezes equivalent briefs, scopes, parentage, outputs, and
   returns as required by root doctrine. If that equivalence cannot be
   demonstrated, record a substrate failure and use sequential single-agent
   conversion. The App Dev Desktop harness is not required. Substrate,
   schema, and project-content results remain separately scored.

7. **Assign preservation audit to RECONCILIATION.** Every pilot conversion
   binds the accepted source commit and four source hashes and produces a
   claim map, parity report, receipt, and independent verifier return.
   RECONCILIATION audits 100% disposition and package/cross-project fan-in.
   These run packages are derivative evidence citing the frozen upstream
   snapshot; they do not replace decomposition or deliverable truth.

8. **Adopt fail-closed abort behavior.** Silent claim loss, invalid mapping,
   lifecycle mutation, unresolved authority conflict, or variance breach
   fails the affected pilot. Failed candidate changes never merge. Preserve a
   FAILED handoff with evidence and rerun requirements, then retire the pilot
   worktree/branch. No accepted branch may retain dual-format ambiguity.

9. **Reserve exact canon and corpus conversion for Stage 2.** This ruling does
   not ratify candidate `TYPES.md`, `SPEC.md`, or Scope-of-Work standard text;
   does not redefine `INITIALIZED`; does not retire `four-documents`; and does
   not authorize corpus-wide conversion. A later D-GOV-16 owner ruling is
   required for all exact-text amendments, project-loop adoption, ISSUED
   handling, remaining-corpus conversion, and legacy retirement.

## Stage-2 entry gates

D-GOV-16 may be proposed only after the frozen-schema pilots demonstrate:

- 100% of source claims dispositioned with no silent drop; every merge/split
  retains all source references;
- every output mapped to project scope and package objective;
- every `AC-*` mapped to a `VER-*` or explicit human-review method;
- deterministic repeated REVIEW checklist derivation from the pilot `AC-*`;
- green legacy-only and SOW-only consumers, with missing and ambiguous formats
  failing outside the variance;
- byte-identical `_STATUS.md` and preserved lifecycle state;
- byte-identical repeated HTML rendering, source/version binding, and no
  scripts or external network dependencies;
- unchanged historical receipts, plans, briefs, concordance evidence, and
  DOMAIN/KTY or analogous independent schemas;
- after schema freeze, no more than one conversion and one verifier run per
  deliverable, no more than one fresh rerun across the ten candidates, and
  human intervention only for genuine content or authority conflicts;
- schema, project-content, and native-substrate outcomes reported separately;
- all applicable root, App Dev, Piping, export, workflow-component, agent,
  skill, path, practitioner-harness, and registered project checks passing;
  and
- root and both project handoffs recording accepted basis, derivative status,
  evidence, blockers, rerun requirements, and a Stage-2 recommendation.

Failure of a gate produces a decision-ready failed or partial handoff; it does
not silently relax the gate or turn the candidate into authority.

## Candidate implementation sequence if approved

1. Publish the ruling and its exact SHA; freeze the source-state basis.
2. Establish the root coordination loop and commit-bound reports.
3. Build and validate the replacement-first candidate components and
   dual-format readers while legacy behavior remains authoritative.
4. Calibrate one deliverable in each pilot package, then freeze the schema.
   The calibration pair is App Dev `DEL-07-03` and Piping `DEL-13-01`.
5. Reconvert the calibration pair from the frozen source basis and convert the
   remaining eight candidates.
6. Run RECONCILIATION preservation audits and applicable project checks.
7. Stop with a Stage-2 decision packet; do not merge candidate deliverables.

## Evidence and authority

- `docs/governance_harness/SCOPE_OF_WORK_STAGE1_SIZING_REPORT.md` supplies the
  commit-bound 154/616 census and exclusions.
- `docs/governance_harness/FOUR_DOCUMENT_CONSUMER_INVENTORY.md` supplies the
  active-caller, historical-evidence, independent-schema, and
  retirement-candidate map.
- `docs/TYPES.md` and `docs/SPEC.md` remain ratified current authority unless
  and until the owner rules exact successor text.
- D-GOV-11 and D-GOV-12 govern role ownership and multi-agent orchestration.
- D-GOV-14 is the precedent for an express, narrow, time-bounded variance; it
  does not itself authorize this new pilot.

## Owner ruling

APPROVED for all nine items by the human owner on 2026-07-12. The owner also
directed that this ruling be incorporated without proceeding with pilot
implementation in the current session. The path-scoped variance is therefore
authorized but not yet exercised. A later session must resume from the ruled
snapshot, derive a fresh execution graph, and preserve every Stage-1 fence and
Stage-2 stop gate above.

## Owner-authorized checklist correction addendum — 2026-07-12

After pilot extraction and preservation evidence existed, the owner asked
whether repeated agentic checklist derivation added value over deterministic
extraction and expressly authorized revision of the governance while
Chirality's core functionality is being revised. The durable direction is
recorded in
`execution/_Coordination/AgentRuns/SOW-STAGE1-20260712/amendments/RUN/v3.md`.

For D-GOV-15 item 5 and the Stage-2 checklist gate, **derive** now means:

1. a registered deterministic tool validates the candidate and compiles every
   defined `AC-*` in source order into stable structured output;
2. the output binds candidate hash, exact criterion text and source identity,
   and the matrix-linked `VER-*` record or explicit human-review method;
3. invalid, legacy-only, or ambiguous input without the exact accepted
   D-GOV-15 variance fails closed before output; and
4. REVIEW consumes that artifact without independently extracting,
   paraphrasing, reordering, renumbering, or omitting candidate criteria.

Repeated agentic extraction is not a Stage-1 value claim or gate. Stage 1
instead proves byte-identical deterministic reproduction and REVIEW-contract
compatibility. REVIEW adds semantic judgment only during an actual
human-gated review.

This addendum supersedes only the earlier implication that REVIEW itself
performs candidate criterion extraction. It leaves all nine approved items,
the pilot path variance, lifecycle/content neutrality, preservation audit,
fail-closed behavior, Stage-2 reservation, exact-canon reservation, corpus
boundary, and no-pilot-merge fence unchanged.
