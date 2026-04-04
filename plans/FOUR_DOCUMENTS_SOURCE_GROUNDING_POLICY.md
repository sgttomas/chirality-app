# 4_DOCUMENTS Source-Grounding Review And Policy Plan

## Status

Reference. Reflected in `agents/AGENT_4_DOCUMENTS.md` via the completed source-grounding work package.

## Role

Policy Input

## Relationship

This note provided policy input for [`plans/AGENT_SOURCE_GROUNDING_INSTRUCTION_UPDATE_PLAN.md`](/Users/ryan/ai-env/projects/chirality-app/plans/AGENT_SOURCE_GROUNDING_INSTRUCTION_UPDATE_PLAN.md), which has now been completed. It is retained as the policy basis and rationale record for the implemented `4_DOCUMENTS` source-grounding redlines.

This note reviews the current `4_DOCUMENTS` instruction contract with source
fidelity in mind and proposes a clean source-grounding policy that matches the
spirit of the DOMAIN policy without forcing unnecessary rereads.

## Review Summary

`AGENT_4_DOCUMENTS.md` already signals the right intent:

- non-trivial statements must cite sources
- inferences must be labeled `ASSUMPTION`
- missing information should become `TBD`
- Pass 3 treats `_SEMANTIC_LENSING.md` as a candidate worklist, not evidence

However, the current instructions still leave too much discretion in how the
agent reaches source-grounded content.

The main issue is that source access is described as:

- read decomposition entry
- read `_REFERENCES.md`
- read accessible references best-effort

That is not yet a strong enough rule set to ensure the four documents remain
faithful to authoritative source material when those materials are locally
available.

## Current Strengths In `AGENT_4_DOCUMENTS.md`

The file already contains good fidelity anchors:

1. Source-anchored invariant
   - non-trivial statements must cite sources

2. Safe handling of uncertainty
   - use `TBD`
   - label `ASSUMPTION`

3. Evidence-first Pass 3 posture
   - `_SEMANTIC_LENSING.md` is not evidence
   - changes require underlying sources or `location TBD`

4. Cross-document consistency requirement
   - reduces drift inside the four-doc set

These should be preserved.

## Main Fidelity Gaps

### Gap 1: No explicit authority hierarchy

The current instructions do not sharply separate:

- authoritative source materials
- decomposition summaries
- prior drafts
- semantic lensing suggestions

That creates risk that the agent becomes faithful to the decomposition entry
or existing drafts rather than to the actual source package.

### Gap 2: No bounded source-read requirement in Pass 1

Pass 1 says to read accessible references best-effort, but it does not state
that authoritative source slices must be read before drafting when they are
available locally.

This leaves too much room for summary-driven drafting.

### Gap 3: No explicit “source slice” concept

The instructions do not define the minimum source region that must be read
to preserve meaning.

Without this, the agent may:

- read too little and lose context, or
- read too much and waste effort

### Gap 4: Pass 2 source reread conditions are underspecified

Pass 2 says to fix inconsistencies when resolvable from sources, but it does
not define when the agent must re-open sources versus when draft-local checks
are enough.

### Gap 5: Pass 3 still does not require source reread before revision

The file correctly says lensing is not evidence, but it does not explicitly
require the agent to re-read the relevant authoritative source slices before
changing deliverable content.

### Gap 6: No explicit handling of source-package incompleteness

The current file allows best-effort reference reading, but it does not define
what should happen when:

- the cited source exists in `_REFERENCES.md` but is inaccessible
- the source exists but the exact location is unclear
- the decomposition makes a claim that cannot be confirmed from source

## Proposed Policy Direction

Use the same basic posture as the DOMAIN policy:

- decomposition = routing and scoping layer
- source package = authority for factual / normative / bounded content
- drafted docs = derived interface
- semantic lensing = candidate enrichment worklist

For `4_DOCUMENTS`, the source-grounding policy should be **deliverable-bounded**
rather than KTY-bounded.

## Proposed Authority Order

1. Authoritative source materials explicitly referenced for the deliverable
   - design basis documents
   - source specifications
   - source standards text when locally available
   - approved source notes or calculations when explicitly referenced

2. Deliverable-local reference pointers
   - `_REFERENCES.md`
   - `_CONTEXT.md`
   - decomposition pointer / entry

3. Decomposition narrative
   - deliverable entry
   - objective mapping
   - package grouping context

4. Existing drafted files
   - `Datasheet.md`
   - `Specification.md`
   - `Guidance.md`
   - `Procedure.md`
   - `_SEMANTIC_LENSING.md`

Authority rule:

- decomposition may scope and explain the deliverable
- source materials remain authority for what the deliverable must say

## Proposed Source Slice Concept

Introduce a source-slice heuristic for `4_DOCUMENTS`:

A source slice is the smallest local source region needed to preserve meaning
for a cited claim, requirement, constraint, or procedure step.

It should usually include:

- the cited section / clause / heading
- the immediate parent heading when it frames applicability or scope
- any embedded tables, acceptance criteria, notes, or enumerations
- adjacent exclusions / exceptions when they materially constrain meaning

This lets the agent stay bounded without becoming summary-driven.

## Proposed Pass Policy

## Pass 1

### Pass 1 must read

Before drafting the four documents, `4_DOCUMENTS` should read:

1. Deliverable-local setup files
   - `_CONTEXT.md`
   - `_REFERENCES.md`
   - `_DEPENDENCIES.md`
   - `_STATUS.md`

2. Decomposition material
   - the exact deliverable entry in `DECOMPOSITION_REF`
   - objective mapping material if used for context

3. Authoritative reference slices for the deliverable
   - every locally accessible source explicitly listed in `_REFERENCES.md`
     that is relevant to this deliverable
   - any cited sections / clauses / tables needed to support:
     - datasheet attributes
     - specification requirements
     - guidance rationale
     - procedure prerequisites / steps / verification

4. Any locally accessible authority cited by the decomposition entry when it
   carries actual technical or contractual content

### Pass 1 may remain best-effort

These do not need mandatory reads unless they directly govern the deliverable:

- secondary references listed only for background
- alternate document revisions not selected as the governing basis
- external URLs without local copies
- standards named but not locally available in text form
- references outside the deliverable's bounded authority set

### Pass 1 drafting rule

When authoritative source material is locally accessible, draft content should
be grounded in that source slice rather than only in:

- the decomposition entry
- `_CONTEXT.md`
- previous drafts
- generic deliverable-type conventions

### Pass 1 fallback rule

If an expected source is not accessible:

- proceed only with bounded statements supported by what is available
- mark unsupported specifics as `TBD`
- keep inferred statements narrow and labeled `ASSUMPTION`
- do not manufacture clause-level or numeric detail from decomposition prose

## Pass 2

### Pass 2 should stay draft-local by default

Draft-local checks are enough for:

- presence of all four docs
- default heading completeness
- internal terminology consistency
- cross-document reference presence

### Pass 2 should re-open source when needed

Re-open bounded source slices when:

- values differ across documents
- requirements and verification do not align
- guidance rationale appears to overstate source support
- procedure steps imply actions not warranted by source
- standards / code mentions may be mismatched or overclaimed

### Pass 2 rule

Use source rereads only to resolve material inconsistencies, not for a
wholesale redraft.

## Pass 3

### Pass 3 must re-read before changing content

For every warranted lensing item that would alter document substance, the
agent should re-read:

1. The affected target document sections
2. The authoritative source slice underlying the affected claim
3. Any sibling document sections implicated by the same requirement, term,
   or verification path

### Pass 3 must re-read source for these item types

- `Conflict`
  - reread all contender source slices before preserving or refining the
    conflict table entry

- `WeakStatement`
  - reread the underlying authority before tightening wording

- `VerificationGap`
  - reread the requirement source and any adjacent acceptance criteria before
    adding verification content

- `Normalization`
  - reread the governing source usage before changing terminology

- `MissingSlot`
  - search the bounded authority set first; if absent, preserve as `TBD` or
    conflict rather than inventing a fill

- `RationaleGap`
  - reread nearby framing or commentary sections before adding rationale

- `TBD_Question`
  - perform a bounded source check before leaving it unresolved

### Pass 3 may remain best-effort

These do not need automatic rereads unless directly implicated:

- unrelated source documents
- unrelated deliverable sections
- background-only references
- inaccessible standards text

## Proposed Behavioral Guardrails

The eventual instruction revision should state explicitly:

1. Do not treat `_SEMANTIC_LENSING.md` as authority.
2. Do not draft requirements from decomposition summaries when governing
   source text is locally available.
3. Do not create procedural steps from generic convention alone unless they
   are clearly marked `TBD` / `ASSUMPTION`.
4. Do not use prior draft wording as if it were source.
5. When source and decomposition differ, source wins and the discrepancy is
   recorded.

## Proposed Minimal Instruction Changes Later

If this policy is converted into instruction changes, the smallest effective
edits would be:

1. Add an explicit authority hierarchy near the invariants section.
2. Add a bounded source-slice definition in the glossary or protocol.
3. Strengthen Step 1 so authoritative local source materials are not merely
   best-effort when they are available and relevant.
4. Add a Pass 1 source-read requirement before Step 4 drafting.
5. Add explicit Pass 2 reread triggers.
6. Add explicit Pass 3 reread requirements for every substantive lens-driven
   change.
7. Add QA checks that distinguish:
   - sourced claims
   - assumptions
   - unresolved but source-checked TBDs

## Recommended QA Additions Later

If revised, the QA contract should add checks like:

- authoritative source set identified
- substantive claims grounded in locally accessible authority where available
- unsupported source gaps converted to `TBD`
- Pass 3 changes rechecked against source before incorporation
- decomposition-derived claims not overstated beyond source support

## Open Design Questions

These should be settled before converting this plan into redlines:

1. Should Pass 1 fail hard if no authoritative local sources are accessible,
   or proceed with warnings?
2. Should `_REFERENCES.md` be tightened so one subset is explicitly marked
   as governing authority vs background references?
3. Should a deliverable-local source manifest be introduced later so
   `4_DOCUMENTS` knows which references are mandatory vs optional?
4. Should standards named in decomposition or references be treated as
   governing only when the actual text is available locally?

## Short Conclusion

`AGENT_4_DOCUMENTS.md` already values source fidelity, but it still leaves too
much of the actual grounding behavior implicit.

The needed change is not a new philosophy. It is a stronger operational
policy:

- Pass 1 must read relevant authoritative source slices before drafting
- Pass 2 rereads source only when inconsistencies require it
- Pass 3 must re-read the implicated source slices before making substantive
  lens-driven changes

That would make `4_DOCUMENTS` more faithful to original source materials
without forcing full-document rereads for every deliverable.
