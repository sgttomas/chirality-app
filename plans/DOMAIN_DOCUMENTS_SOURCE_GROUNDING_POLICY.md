# DOMAIN_DOCUMENTS Source-Grounding Policy

## Status

Proposed policy only. Not yet applied to any agent instructions.

This note defines a clean source-grounding policy for `DOMAIN_DOCUMENTS`
so the agent remains faithful to original domain material without requiring
wasteful full-corpus rereads on every pass.

## Purpose

Reduce fidelity loss between:

- original source materials in `_Sources/`
- decomposition extracts and unit mappings
- drafted `Scoping.md` and `KA-*.md` Knowledge Artifact files
- Pass 3 enrichment driven by `_SEMANTIC_LENSING.md`

The intended posture is:

- decomposition is the routing and scoping layer
- source materials are the authority for factual and bounded content
- drafted DOMAIN documents are derived products, not the authority

## Core Policy

`DOMAIN_DOCUMENTS` should use a bounded, evidence-first source-grounding model:

1. Use decomposition data to identify the KTY, its Subjects, and its evidence set.
2. Use `SourceRef` and `_REFERENCES.md` to locate the authoritative source slices.
3. Read the minimum source slices needed to draft or revise faithfully.
4. Do not rely only on decomposition summaries when the cited source files are
   locally accessible.
5. Do not re-read the entire DBM unless the KTY actually requires it.

This is not a corpus-wide reread policy. It is a bounded source verification
policy.

## Source Priority

Use this priority order:

1. Original source material under local `_Sources/`
   - source markdown or PDF-derived markdown
   - exact sections cited by `SourceRef`
   - tables/lists/figures embedded in those sections

2. KTY-local reference pointers
   - `_REFERENCES.md`
   - explicit source file paths
   - explicit section pointers

3. Decomposition data
   - `KnowledgeTypes.csv`
   - `HandbookUnits.csv`
   - `DomainLedger.csv`

4. Existing drafted files
   - `Scoping.md`
   - `KA-*.md`
   - `_SEMANTIC_LENSING.md`

Authority rule:

- decomposition and lensing artifacts help locate, scope, and suggest
  changes
- original source material remains the authority for what the domain source
  actually says

## Definitions

### Source slice

A source slice is the smallest source region that preserves meaning for a
cited topic. It should usually include:

- the exact cited heading or section
- the opening prose under that heading
- any tables or lists directly under that heading
- the immediate parent heading when that parent supplies boundary or framing
  context

Example:

- if a Subject points to `§1.4.1 Included Scope`, the slice should normally
  include:
  - `1.4 Basic Scope of Work` opening paragraph, and
  - `1.4.1 Included Scope`, including its tables

### Bounded source set

The bounded source set for one KTY is:

- all source files explicitly named in that KTY's `_REFERENCES.md`
- all source files named by `SourceRef` values in its evidence set
- only the sections needed for that KTY's Subjects, conflicts, and revisions

## Pass 1 Policy

### Pass 1 must read

Before drafting `Scoping.md` and `KA-*.md`, `DOMAIN_DOCUMENTS` should read:

1. KTY-local setup files
   - `_CONTEXT.md`
   - `_REFERENCES.md`

2. Decomposition tables
   - `KnowledgeTypes.csv`
   - `HandbookUnits.csv`
   - optional `DomainLedger.csv`

3. Evidence-linked source slices for the KTY
   - every source section cited by the KTY's evidence set
   - any parent heading needed to preserve boundary/context
   - any table/list directly under those cited sections

4. Any additional source sections explicitly cited in `_REFERENCES.md` and
   needed to support:
   - boundary statements
   - intended use framing
   - interfaces / responsibilities
   - cross-subject distinctions inside the same KTY

### Pass 1 may remain best-effort

These do not need mandatory reads unless the KTY actually depends on them:

- secondary reference documents in `_REFERENCES.md`
- alternate revisions of the same DBM
- external URLs
- uncited DBM chapters outside the KTY's bounded source set
- non-local references that are listed but not accessible

### Pass 1 drafting rule

When the cited source file is locally accessible, artifact prose should be
grounded in the source slice, not only in:

- `HandbookUnits.csv.AtomicStatement`
- path-like `SourceRef` strings
- prior draft wording

### Pass 1 fallback rule

If a required source file or section is not accessible:

- proceed using decomposition data only if needed
- mark the affected item as bounded by source unavailability
- prefer `TBD` or narrow factual phrasing over synthesized detail
- do not include direct excerpts that were not actually read

## Pass 2 Policy

Pass 2 is mainly a consistency pass, so it should not trigger a full
source reread.

### Pass 2 should re-open source only when needed

Re-open bounded source slices only for:

- value mismatches across `KA-*.md` files
- identity inconsistencies
- conflicting terminology
- apparent contradictions between `Scoping.md` and an artifact
- claims that cannot be resolved from current drafts alone

### Pass 2 may remain draft-local

If a check is purely structural, it can remain local to the drafted files:

- artifact-plan to file presence checks
- duplicate filename checks
- heading/schema completeness checks

## Pass 3 Policy

Pass 3 should be source-grounded revision work, not blind application of
`_SEMANTIC_LENSING.md`.

### Pass 3 must re-read

For every warranted item that would change artifact content, `DOMAIN_DOCUMENTS`
should re-read:

1. The current target files
   - affected `KA-*.md`
   - `Scoping.md` if the change affects identity, artifact plan, conflicts,
     or KTY-wide framing

2. The cited source slice(s) underlying the affected claim
   - source sections already cited in the affected artifact
   - source sections named in the lensing item's provenance
   - any competing source slices when the item is a conflict

3. Any sibling artifact(s) implicated by the same topic or boundary
   - especially for included/excluded scope pairs
   - cross-referenced terms
   - normalized terminology

### Pass 3 should re-read source for these item types

- `Conflict`
  - reread every contender source section before preserving or refining the
    conflict

- `WeakStatement`
  - reread the underlying source section before tightening wording

- `Normalization`
  - reread the source section(s) for the competing terms before unifying
    terminology

- `MissingSlot`
  - search the bounded source set first; if absent, keep as `TBD` or preserve
    as a gap

- `RationaleGap`
  - reread nearby framing sections; if rationale is still absent, record the
    gap rather than inventing explanation

- `VerificationGap`
  - reread the relevant source section and any adjacent acceptance/criteria
    passages in the bounded source set; if nothing supports the addition,
    keep it as a question or gap

- `TBD_Question`
  - perform a bounded source check before leaving it unresolved

### Pass 3 may remain best-effort

These do not need automatic rereads unless the lensing item touches them:

- unrelated KTY source sections
- unrelated DBM chapters
- secondary reference documents not implicated by the change
- external references without local copies

## What Must Never Happen

- Do not apply `_SEMANTIC_LENSING.md` suggestions as facts without rechecking
  source.
- Do not rely only on `AtomicStatement` or decomposition summaries when the
  source file is locally available.
- Do not re-draft an entire KTY from memory or from prior `KA-*.md` text.
- Do not widen from a bounded KTY source set into a whole-document reread
  unless the local evidence actually forces that move.

## Source Slice Heuristic

When a `SourceRef` points to a section, read:

1. the cited section itself
2. the content under that section until the next same-or-higher heading
3. the immediate parent heading when it contributes scope or framing
4. directly embedded tables/lists under the cited section

This keeps fidelity high without requiring a full DBM reread.

## Practical Operating Rule

### Pass 1

Use decomposition to locate the KTY and evidence set, then read the cited
source slices before drafting.

### Pass 2

Stay local unless a draft inconsistency cannot be resolved without source.

### Pass 3

Treat `_SEMANTIC_LENSING.md` as a worklist, then re-read the implicated source
slices before incorporating, rejecting, or converting each item to `TBD` /
Conflict.

## Why This Is The Right Middle Ground

This policy avoids both bad extremes:

- too little grounding:
  - faithful only to decomposition abstractions, not to the DBM

- too much grounding:
  - expensive full-document rereads for every KTY and every pass

The right operating point is:

- bounded by KTY
- bounded by evidence set
- bounded by cited source slices
- re-opened selectively during Pass 3 where edits are actually being made

## Review Questions

Before converting this into agent-instruction changes, these points should be
confirmed:

1. Should local `_Sources/` markdown be considered mandatory authority when
   present, or only preferred authority?
2. Should Pass 1 fail hard when required cited source slices are inaccessible,
   or continue with warnings plus `TBD`?
3. Should Pass 3 require explicit reread evidence in the run report for each
   incorporated lensing item?
4. Should `_REFERENCES.md` be tightened so the KTY always lists the exact
   source files expected for Pass 1 grounding?

## Short Summary

Recommended policy:

- Pass 1 must read the KTY's cited source slices before drafting.
- Pass 2 rereads source only when draft inconsistencies require it.
- Pass 3 must re-read the source slices implicated by every substantive
  lens-driven change.
- Secondary or unrelated materials remain best-effort.
