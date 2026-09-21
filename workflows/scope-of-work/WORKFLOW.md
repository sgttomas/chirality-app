---
name: scope-of-work
description: Initialize, convert, validate, and independently verify one objective-anchored PROJECT/SOFTWARE ScopeOfWork.md under the active SOW_V1
  transition contract. Do not use for DOMAIN/KTY or independent schemas, lifecycle changes, or unauthorized corpus conversion.
---

# WORKFLOW — scope-of-work

## Purpose

Produce or verify one `SOW_V1` production contract. `MODE=INIT` creates a new
source-grounded PROJECT/SOFTWARE contract; `MODE=CONVERT` preserves every
legacy source range in an isolated `MIGRATION_DUAL` workspace; `MODE=VERIFY`
is read-only on production content. The ratified
`docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md` governs all modes.

Read [resources/brief.md](resources/brief.md) before accepting a run. Read
[resources/tools.md](resources/tools.md) before invoking tools and use
[resources/checks.md](resources/checks.md) for acceptance.

## Suitable agent shell

- `TASK` with one deliverable-local sealed brief.

## Method

1. Confirm `MODE`, exact deliverable path, accepted decomposition basis,
   objective references, format state, and disjoint write targets.
2. Resolve the production format fail-closed. `INIT` requires no production
   contract; `CONVERT` requires complete `LEGACY_FOUR_DOC` plus exact isolated
   migration authority; `VERIFY` requires `SOW_V1` or authorized
   `MIGRATION_DUAL`. Missing, partial, invalid, or unauthorized dual input
   fails before output.
3. For `INIT`, ground every definition in accepted decomposition/source
   evidence. For `CONVERT`, hash the four sources and `_STATUS.md`, then use
   the deterministic converter to create a lossless scaffold. Tests may
   implement verification but never create scope or acceptance criteria.
4. Refine the working contract. Define stable IDs, complete the
   output/evaluation matrix, preserve epistemic labels, and mark substantive
   ambiguity `CONFLICT`. For `CONVERT`, the working contract is the evidence
   candidate and its conversion source markers are never dropped. For `INIT`,
   the working contract is the production `ScopeOfWork.md` itself; there is no
   evidence candidate and no source marker.
5. For `CONVERT` only: run source mapping and parity on the evidence candidate,
   then use the deterministic finalizer to create a separate clean production
   contract and external finalization report. Require the map and parity report
   to bind the clean production hash. `INIT` produces no evidence candidate,
   runs no mapping, parity, or finalization, and authors the production
   contract directly.
6. Validate and derive the WORKING_ITEMS (workflow: review) checklist from the production contract, and
   optionally render HTML from it. Under `CONVERT` the production contract is
   the clean finalized artifact and no other.
7. Return the production contract path and hash, validation result, checklist,
   conflicts, and the `_STATUS.md` hash — unchanged under `NO_STATUS_TOUCH`, or
   before/after when the brief authorizes a status act. For `CONVERT`,
   additionally return the evidence-candidate path, source and evidence hashes,
   finalization report, claim map, and parity report.

## Non-negotiable constraints

- In `CONVERT`, keep all four legacy documents and `_STATUS.md` byte-identical;
  the isolated dual state remains derivative until atomic replacement by WORKING_ITEMS (workflow: change).
- Do not modify `_STATUS.md`, lifecycle state, underscore control files,
  historical evidence, or other deliverables.
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
  basis, required migration authority, or lifecycle evidence.
- Return `UNSUPPORTED_STATE` for an operation not authorized for the resolved
  format/lifecycle state.
- Return `CONFLICT` for a semantic change or authority question.
- Return `FAILED_VALIDATION` for schema, mapping, parity, or write-boundary
  failures. Preserve evidence and do not claim conversion success.

## Package conversion coordination

For an authorized multi-deliverable representation conversion, WORKING_ITEMS loads [the representation-migration profile](resources/representation-migration.md) to partition batches, dispatch author and independent verifier work, and preserve member-complete evidence. TASK receives one bounded authoring or verification assignment.
