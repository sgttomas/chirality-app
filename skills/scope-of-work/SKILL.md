---
name: scope-of-work
description: Initialize, convert, validate, and independently verify one objective-anchored PROJECT/SOFTWARE ScopeOfWork.md under the active SOW_V1 transition contract. Do not use for DOMAIN/KTY or independent schemas, lifecycle changes, or unauthorized corpus conversion.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
allowed-tools: python3 tools/scope_of_work/validate_scope_of_work.py:{scope_path}/**, python3 tools/scope_of_work/render_scope_of_work.py:{scope_path}/**, python3 tools/scope_of_work/convert_four_documents_to_scope_of_work.py:{scope_path}/**, python3 tools/scope_of_work/finalize_scope_of_work.py:{scope_path}/**, python3 tools/scope_of_work/map_scope_of_work_claims.py:{scope_path}/**, python3 tools/scope_of_work/report_scope_of_work_parity.py:{scope_path}/**, python3 tools/scope_of_work/derive_review_checklist.py:{scope_path}/**
---

# SKILL — scope-of-work

## Purpose

Produce or verify one `SOW_V1` production contract. `MODE=INIT` creates a new
source-grounded PROJECT/SOFTWARE contract; `MODE=CONVERT` preserves every
legacy source range in an isolated `MIGRATION_DUAL` workspace; `MODE=VERIFY`
is read-only on production content. The ratified
`docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md` governs all modes.

Read [BRIEF_SCHEMA.md](BRIEF_SCHEMA.md) before accepting a run. Read
[TOOL_POLICY.md](TOOL_POLICY.md) before invoking tools and use
[QA_CHECKS.md](QA_CHECKS.md) for acceptance.

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
4. Refine the evidence candidate without dropping conversion source markers.
   Define stable IDs, complete the output/evaluation matrix, preserve epistemic
   labels, and mark substantive ambiguity `CONFLICT`.
5. Run source mapping and parity on the evidence candidate, then use the
   deterministic finalizer to create a separate clean production contract and
   external finalization report. Require the map and parity report to bind the
   clean production hash.
6. Validate, derive the REVIEW checklist, and optionally render HTML from the
   clean production contract only.
7. Return both candidate paths, source/evidence/production hashes, finalization
   report, claim map, parity report, checklist, validation result, conflicts,
   and `_STATUS.md` before/after hash.

## Non-negotiable constraints

- In `CONVERT`, keep all four legacy documents and `_STATUS.md` byte-identical;
  the isolated dual state remains derivative until atomic replacement by CHANGE.
- Do not modify `_STATUS.md`, lifecycle state, underscore control files,
  historical evidence, or other deliverables.
- Do not resolve substantive conflicts through formatting.
- Do not treat generated HTML, migration receipts, or parity reports as
  authoritative deliverable truth.
- Do not run `CONVERT` without exact path-scoped migration authority.
- Do not treat `MIGRATION_DUAL` as an accepted deliverable baseline.
- Never integrate the evidence-rich migration candidate. Production must be
  the exact deterministic finalization and contain no migration-only metadata.
- Refuse `ISSUED` preparation unless the brief binds the source commit, all
  four source hashes, `_STATUS.md` hash, and accepted basis. Preparation never
  authorizes integration or reissuance; H1 remains a later human gate.
- Preserve `LEGACY_FOUR_DOC` compatibility; this skill does not retire it.
- Do not manually re-extract, summarize, reorder, or renumber `AC-*` records
  for REVIEW; use the registered deterministic checklist artifact.

## Failure semantics

- Return `FAILED_INPUTS` for missing sources, objective mappings, accepted
  basis, required migration authority, or lifecycle evidence.
- Return `UNSUPPORTED_STATE` for an operation not authorized for the resolved
  format/lifecycle state.
- Return `CONFLICT` for a semantic change or authority question.
- Return `FAILED_VALIDATION` for schema, mapping, parity, or write-boundary
  failures. Preserve evidence and do not claim conversion success.
