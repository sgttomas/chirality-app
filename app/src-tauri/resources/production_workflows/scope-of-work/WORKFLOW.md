---
name: scope-of-work
description: Initialize, convert, revise under an accepted scope-change amendment, validate, and independently verify one objective-anchored PROJECT/SOFTWARE ScopeOfWork.md under the active SOW_V1 transition contract. Do not use for DOMAIN/KTY or independent schemas, lifecycle changes, or unauthorized corpus conversion.
metadata:
  kind: instruction
  surface: workflow
---

# WORKFLOW — scope-of-work

## What a scope says

A scope gives its deliverable an identity and the criteria to achieve. It is
the local objective the code is measured against, not a description of the
code. The six parts are kept, and every part states what contribution is
intended, under what conditions, and what would establish that it is adequate.

- **Purpose and traceability:** the result this deliverable contributes, in
  words, linked to its decomposition and PRD objective and, where the project
  has one, the release-target result it serves, stated in words.
- **Ontology:** outputs, the terms that define the product, the boundary.
- **Epistemology:** requirements and acceptance criteria as observable
  properties of the product.
- **Praxeology:** method choices that define the product, and how each
  criterion is examined.
- **Axiology:** the values that govern trade-offs, including one or two
  sentences on which way is better, each naming the measure that improves and
  what it may never trade away. A new capability is not a direction; it enters
  by scope change.
- **Matrix:** output → objective → requirement → acceptance → verification →
  evidence expectation.

**The scope leads.** Objectives and criteria come from the PRD, the
decomposition, the release target and the owner's decisions, never from the
code. A commitment the code has not met stays as written; the shortfall is the
work to do. A description is corrected only where intended behaviour and
boundary are unchanged. Something the code does enters a scope only if an
acceptable replacement implementation would also have to do it and a PRD
clause, the decomposition or an owner decision already authorises it. Changed commitments, unresolved intent and code outside
the deliverable's identity go to the owner.

**Current statements only.** A decision appears only as the current statement
it settles, with no date, quotation, amendment record or history; Git keeps
earlier text. Something undecided is a plain statement in the part it affects,
deleted when resolved. A scope carries no status, progress or "current
implementation" notes, no resolved open items, quoted approvals, repeated
disclaimers or quoted legacy document kits, and no hashes or revision pins of
the project's own mutable files. An exact edition is named only for an external
source such as a published standard.

**Requirements and their grounds.** State what the deliverable must achieve and
explain the reasons needed to understand its boundaries and trade-offs. Write
these as current statements, without dates, approval quotations or appeals to
past decisions. Refer to current governing requirements where that clarifies
the relationship; explain a shared reason once.

Each criterion's matrix row identifies the evidence that would establish it and
the comparison or judgment required. Name independent references precisely
enough to examine them. A chosen target is a requirement to assess, not evidence
of its own adequacy. Agreement with the product's earlier output establishes
consistency, not correctness. State any consequential gap in what the evidence
can establish; do not disguise it with a rationale or authority label.

**Changing a statement.** A statement's attribution does not determine who may
change it. Reconcile meaning within the applicable delegation; take changes
outside it to the responsible decision holder. Removing attribution or history
must preserve current obligations, boundaries and action restrictions. If a
requirement appears wrong, explain the problem and proposed correction rather
than changing the objective merely to fit the implementation.

**Independent review keeps the text honest; tests do not.** A reviewer who did
not write the text, and does not see the writer's reasoning, reads the scope
against the PRD and decomposition, the code it represents and neighbouring
scopes, and asks: is the text honest; and could an agent holding this scope and
the code identify a justified next step and the evidence needed to stop?
Numerical and runtime checks remain the way product correctness is examined.

## Purpose

Produce or verify one `SOW_V1` production contract. `MODE=INIT` creates a new
source-grounded PROJECT/SOFTWARE contract; `MODE=CONVERT` preserves every
legacy source range in an isolated `MIGRATION_DUAL` workspace; `MODE=REVISE`
revises an existing `SOW_V1` contract only where an accepted `scope-change`
amendment changes its scope; `MODE=VERIFY` is read-only on production content.

Read [resources/brief.md](resources/brief.md) before accepting a run. Read
[resources/tools.md](resources/tools.md) before invoking tools and use
[resources/checks.md](resources/checks.md) for acceptance.

## Current-project use and reconciliation

A current PROJECT/SOFTWARE locality is ScopeOfWork.md and deliverable.yaml.
`INIT`, `VERIFY` and current-project `REVISE` do not require `_STATUS.md` or a legacy source kit. Preserve
such files if present; their absence is not a reason to create them or invent a
lifecycle state. This workflow never advances status.

Ordinary factual reconciliation of an existing contract and its needs occurs
through `bounded-reconciliation` in the implementation PR before integration,
within the project's existing authority. Use these validators to check the
changed contract. Preserve commitments, acceptance criteria and explicit holds;
substantive changes require their actual owner decision. Do not force routine
description corrections into the formal amendment route below. `MODE=REVISE`
remains the route when an accepted scope-change amendment selects it; `CONVERT`
retains its isolated historical source-preservation requirements.

For `REVISE`, select the project profile from its governing instructions and
accepted amendment. In the current profile, use the accepted named amendment,
prior valid contract/hash and exact revision scope; `SOURCE_STATE: not used` is
valid when no lifecycle is adopted. Existing legacy files remain untouched and
alone select no lifecycle. An actual project hold or acceptance condition still
applies. The retained lifecycle preconditions below apply only where that
lifecycle is explicitly adopted; missing required lifecycle evidence is then a
failure, not permission to switch profiles.

## Suitable agent shell

- `TASK` with one deliverable-local sealed brief.

## Method

1. Confirm `MODE`, exact deliverable path, accepted decomposition basis,
   objective references, format state, and disjoint write targets.
2. Resolve the production format fail-closed. `INIT` requires no production
   contract; `CONVERT` requires complete `LEGACY_FOUR_DOC` plus exact isolated
   migration authority; `REVISE` requires a valid `SOW_V1` contract and an accepted amendment;
   an adopted legacy lifecycle additionally requires `INITIALIZED`,
   `SEMANTIC_READY` or `IN_PROGRESS`
   (see [Revision under an accepted amendment](#revision-under-an-accepted-amendment));
   `VERIFY` requires `SOW_V1` or authorized `MIGRATION_DUAL`. Missing,
   partial, invalid, or unauthorized dual input fails before output.
3. For `INIT`, ground every definition in accepted decomposition/source
   evidence. For `CONVERT`, hash the four sources and `_STATUS.md`, then use
   the deterministic converter to create a lossless scaffold. Tests may
   implement verification but never create scope or acceptance criteria.
4. Refine the working contract. Define stable IDs, complete the
   output/evaluation matrix, preserve epistemic labels, and mark substantive
   ambiguity `CONFLICT`. Under `INIT`, state each verification entry's kind
   (see [Verification entries](#verification-entries)). For `CONVERT`, the working contract is the evidence
   candidate and its conversion source markers are never dropped. For `INIT`,
   the working contract is the production `ScopeOfWork.md` itself; there is no
   evidence candidate and no source marker.
5. For `CONVERT` only: run source mapping and parity on the evidence candidate,
   then use the deterministic finalizer to create a separate clean production
   contract and external finalization report. Require the map and parity report
   to bind the clean production hash. `INIT` produces no evidence candidate,
   runs no mapping, parity, or finalization, and authors the production
   contract directly. `REVISE` follows its own steps below and produces no
   evidence candidate.
6. Validate and derive the WORKING_ITEMS (workflow: review) checklist from the production contract, and
   optionally render HTML from it. Under `CONVERT` the production contract is
   the clean finalized artifact and no other.
7. Return the production contract path and hash, validation result, checklist,
   conflicts, and preservation of `_STATUS.md` if it exists (otherwise report
   that no lifecycle source is used). A separately authorized status act belongs
   to its own actor; this workflow never performs it. For `CONVERT`,
   additionally return the evidence-candidate path, source and evidence hashes,
   finalization report, claim map, and parity report. For `REVISE`,
   additionally return the prior contract hash, the amendment reference, the
   revised parts, and the `MODE=VERIFY` result.

## Verification entries

A verification entry that an `INIT` or `REVISE` run writes or changes opens its
one-line definition by stating its kind and what the verification rests on. So
does an entry whose examination an ordinary reconciliation edit changes, in
what it examines or how. A corrected path or name alone does not bring a
stated kind with it. The kinds are:

- **Executable check:** what it observes, which is the behaviour or output the
  criterion names. Where it can observe only a proxy, it says so. The entry
  states the examination whether or not the check exists yet; whether it
  exists is read from the code.
- **Comparison with a named reference:** the reference.
- **Judgment by a named role:** who judges, and what they examine. A
  `HUMAN_REVIEW:` matrix entry is this kind and names the role. A judgment by
  a role that is not a person, such as an independent reviewer agent, is a
  `VER-*` entry.

Choose the kind by what settles pass or fail: a result the check computes and
tests against the criterion, agreement with something external, or someone's
assessment. Automation is incidental. Expected values the criterion itself
determines leave a check executable. An automated test against values
produced elsewhere, such as another solver's output, a prior run or a
published table, is a comparison. An entry that combines kinds states each part. For example:
`Executable check (observes the exported file's rows against the displayed table): …`

Keep the definition on one line, because checklist derivation reads one-line
definitions. A stated kind describes the intended examination. It does not
establish that the check exists, runs or passes.

Entries a run does not change keep their wording. `VERIFY` does not fail an
entry for lacking a stated kind, `REVISE` already leaves everything outside
`REVISION_SCOPE` untouched, and `CONVERT` preserves source meaning and does
not classify.

## Revision under an accepted amendment

Current projects use the exact accepted amendment/review binding from the current
`scope-change` profile; an immutable snapshot/register is required only where
the selected route uses it. Both profiles require group-3 acceptance before
this deferred revision runs. If the accepted amendment itself already changed
the contract, verify that result rather than applying the revision twice.

`MODE=REVISE` applies when an accepted `scope-change` amendment (checkpoint
group 3 accepted) names this deliverable with action `MODIFY` or `RECLASSIFY`
and did not itself change `ScopeOfWork.md` within its write boundary. The
usual dispatcher is `project-setup`'s current-project incremental route or,
where explicitly adopted, `project-setup-retained` in `INCREMENTAL` mode.

1. Bind the inputs: the accepted amendment and its ID, the accepted
   actions naming this deliverable bound to their reviewed revision/content
   (register hash where that route uses one), the amended
   decomposition basis, the `REVISION_SCOPE` (the parts of the contract the
   amendment changes), and the prior contract's hash.
2. Under an explicitly adopted legacy lifecycle, refuse before output when
   the lifecycle state is `CHECKING` or `ISSUED`,
   and return `UNSUPPORTED_STATE` so the deliverable is held for the human.
   `CHECKING` changes only after a human reversal to `IN_PROGRESS`; `ISSUED`
   only after the human records `ISSUED → IN_PROGRESS` under the accepted
   amendment. Also refuse `LEGACY_FOUR_DOC`,
   `MIGRATION_DUAL`, and a contract that does not validate before revision.
   For the current profile, inspect actual holds and authority without inventing
   lifecycle state. Both profiles reject invalid or ambiguous input formats.
3. Revise only the parts the amendment names: the affected definitions,
   matrix rows and references, and the `decomposition_basis`,
   `project_scope_refs` or `package_objective_refs` values the amendment
   changes. Keep every other byte. Keep existing `OUT-*`, `AC-*`, `VER-*` and
   other local IDs; never renumber them or reuse an ID the amendment removes.
   A verification entry this step writes or changes states its kind (see
   [Verification entries](#verification-entries)).
   Mark a change the amendment does not clearly determine `CONFLICT`.
4. Validate and derive the checklist (Method step 6), then end with a
   `MODE=VERIFY` run on the revised contract. The return includes a diff of
   the prior and revised contracts for the independent check that nothing
   outside `REVISION_SCOPE` changed.

`REVISE` never changes lifecycle state: it runs only under `NO_STATUS_TOUCH`,
and recording any later transition is a separate authorized act.

## Non-negotiable constraints

- In `CONVERT`, keep all four legacy documents and `_STATUS.md` byte-identical;
  the isolated dual state remains derivative until atomic replacement by the authorized implementation owner under the
  project's change conventions; the conversion authority and preservation checks
  above still apply.
- Do not modify `_STATUS.md`, lifecycle state, underscore control files,
  historical evidence, or other deliverables.
- Do not run `REVISE` without an accepted amendment that names the
  deliverable, contrary to an adopted lifecycle or actual project hold, or outside the named
  `REVISION_SCOPE`. `REVISE` is not a general editing mode.
- Do not resolve substantive conflicts through formatting.
- Do not treat generated HTML, migration receipts, or parity reports as
  authoritative deliverable truth.
- Do not run `CONVERT` without exact path-scoped migration authority.
- Do not treat `MIGRATION_DUAL` as an accepted deliverable baseline.
- Never integrate the evidence-rich migration candidate. Production must be
  the exact deterministic finalization and contain no migration-only metadata.
- Cite an upstream deliverable's local IDs by one of exactly two routes, never
  as a bare ID. Local-ID syntax is deliverable-scoped: a bare `REQ-004` in
  contract prose always means *this* contract's `REQ-004`, so an upstream ID
  written bare in own-voice prose either collides with a local definition or
  scans as an unresolved local reference.
  - **Qualified form (canonical for own-voice prose):** write the upstream
    deliverable ID, a `/`, then the local ID — `DEL-01-02/REQ-003`. Extraction
    ignores any ID preceded by `-`, `/`, or a word character, so a qualified
    citation is never harvested as a local definition or reference. The
    hyphen-separated spelling `DEL-01-02-REQ-004` is guarded identically, but
    the slash form is canonical because it parses back into its parts
    unambiguously.
  - **Blockquote form:** quote the upstream text in a `> ` blockquote and add
    an explicit carve-out sentence — "ID-shaped text inside this quotation is
    upstream source context, not a local definition or reference" — naming the
    upstream deliverable in own-voice prose around the quotation. The
    blockquote marker must sit at column 0–3; a blockquote indented four or
    more spaces is not exempt from ID extraction.
- Refuse `ISSUED` preparation unless the brief binds the source commit, all
  four source hashes, `_STATUS.md` hash, and accepted basis. Preparation never
  authorizes integration or reissuance; H1 remains a later human gate.
- Preserve `LEGACY_FOUR_DOC` compatibility; this workflow does not retire it.
- Do not manually re-extract, summarize, reorder, or renumber `AC-*` records
  for WORKING_ITEMS (workflow: review); use the registered deterministic checklist artifact.
- For each boundary-exclusion requirement, enumerate the acts it excludes and
  name an owner for each, citing the claim that carries that owner. Enumerating
  the acts in a sentence is semantic work and belongs to this method; the
  resolution half is checked deterministically by
  `check_boundary_owner_resolution.py`, which asserts that every owner ID a
  whole-requirement exclusion names is also named by a claim that requirement
  cites. Where the tool reports `NOT_CHECKABLE` — a per-act exclusion clause
  whose owner is not syntactically bound to a claim — carry the one-for-one
  check in this method instead, and prefer binding the owner to its claim in
  the requirement text so the deterministic check can reach it.
- In the Output and Evaluation Matrix, a row's verification references apply to
  every acceptance criterion in that row. Group acceptance criteria in one row
  only when the row's verification set is exactly the union of those criteria's
  own methods **and those criteria's method sets are identical** — grouping is
  safe only when every criterion in the row is verified by exactly the same
  methods. Otherwise give each acceptance criterion its own row. Union equality
  alone is not sufficient: two criteria with different methods satisfy it while
  each still inherits the other's non-verifying method. Checklist derivation is
  row-scoped and cannot recover a finer pairing.

## Failure semantics

- Return `FAILED_INPUTS` for missing sources, objective mappings, accepted
  basis, required migration authority, lifecycle evidence, or, for `REVISE`,
  an amendment that is not accepted or does not name the deliverable.
- Return `UNSUPPORTED_STATE` for an operation not authorized for the resolved
  format/lifecycle state.
- Return `CONFLICT` for a semantic change or authority question.
- Return `FAILED_VALIDATION` for schema, mapping, parity, or write-boundary
  failures. Preserve evidence and do not claim conversion success.

## Package conversion coordination

For an authorized multi-deliverable representation conversion, WORKING_ITEMS loads [the representation-migration profile](resources/representation-migration.md) to partition batches, dispatch author and independent verifier work, and preserve member-complete evidence. TASK receives one bounded authoring or verification assignment.
