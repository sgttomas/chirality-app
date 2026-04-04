# Agent Source-Grounding Instruction Update Plan

## Status

Queued under the active master plan. No agent instruction files have yet been updated by this plan.

## Role

Supporting Work Package

## Relationship

This is the next bounded instruction-revision package for source-grounding behavior. It is subordinate to [`plans/PHASED_STABILIZATION_AND_EXECUTABLE_SKILLS_PLAN.md`](/Users/ryan/ai-env/projects/chirality-app/plans/PHASED_STABILIZATION_AND_EXECUTABLE_SKILLS_PLAN.md) and should not be treated as an independent active roadmap.

This note defines the plan for converting the proposed source-grounding
policies into concrete agent-instruction revisions.

Related policy notes:

- [DOMAIN_DOCUMENTS Source-Grounding Policy](/Users/ryan/ai-env/projects/chirality-app/plans/DOMAIN_DOCUMENTS_SOURCE_GROUNDING_POLICY.md)
- [4_DOCUMENTS Source-Grounding Review And Policy Plan](/Users/ryan/ai-env/projects/chirality-app/plans/FOUR_DOCUMENTS_SOURCE_GROUNDING_POLICY.md)

## Goal

Update the drafting agents so source fidelity is operationalized, not merely
stated as a value.

The intended result is:

- decomposition continues to scope and route work
- original source materials become the explicit authority for factual and
  bounded content when locally available
- Pass 3 enrichment becomes explicitly source-rechecked rather than merely
  suggestion-driven

## In-Scope Instruction Files

Primary targets:

1. [AGENT_DOMAIN_DOCUMENTS.md](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_DOMAIN_DOCUMENTS.md)
2. [AGENT_4_DOCUMENTS.md](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_4_DOCUMENTS.md)

Secondary review target only if needed:

3. [AGENT_ORCHESTRATOR.md](/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_ORCHESTRATOR.md)

Out of scope for the first revision:

- `AGENT_CHIRALITY_FRAMEWORK.md`
- `AGENT_CHIRALITY_LENS.md`
- `AGENT_PREPARATION.md`

These files may reference the resulting behavior later, but they do not need
to carry the main source-grounding policy.

## Update Strategy

Do not invent a new philosophy. Strengthen the existing one by making the
following explicit in the drafting agents:

1. Authority hierarchy
2. Bounded source-set definition
3. Source-slice heuristic
4. Pass-specific must-read / may-remain-best-effort rules
5. Explicit Pass 3 source reread requirements before substantive edits
6. QA checks tied to source-grounding behavior

## Planned Changes By File

## 1. AGENT_DOMAIN_DOCUMENTS.md

### Objective

Convert the current best-effort source use into a bounded source-grounding
contract for KTY drafting and enrichment.

### Planned changes

1. Add an authority hierarchy near invariants or early protocol
   - local `_Sources/` and cited source files
   - `_REFERENCES.md`
   - decomposition tables
   - existing drafts
   - `_SEMANTIC_LENSING.md` as candidate worklist only

2. Add a bounded-source-set definition
   - source files named in `_REFERENCES.md`
   - source files named by `SourceRef`
   - source sections needed by the KTY's evidence set and revisions

3. Add a source-slice heuristic
   - cited section
   - immediate parent heading when it frames scope
   - embedded tables/lists
   - adjacent exception/exclusion material when relevant

4. Strengthen Step 1 / Step 2 / Step 4 for Pass 1
   - require reading evidence-linked source slices before drafting when
     locally accessible
   - keep secondary references and unrelated chapters best-effort

5. Strengthen Pass 2
   - define when the agent must reopen source to resolve inconsistencies
   - keep structural checks draft-local

6. Strengthen Pass 3
   - require rereading implicated source slices before incorporating a
     substantive lens-driven change
   - define item-type-specific reread triggers for:
     - `Conflict`
     - `WeakStatement`
     - `Normalization`
     - `MissingSlot`
     - `RationaleGap`
     - `VerificationGap`
     - `TBD_Question`

7. Extend QA contract
   - source set identified
   - substantive claims grounded in accessible authority
   - unsupported specifics converted to `TBD`
   - Pass 3 changes source-rechecked before incorporation

### Expected outcome

`DOMAIN_DOCUMENTS` becomes explicitly faithful to the original KTY source
material, not merely to decomposition abstractions or prior drafts.

## 2. AGENT_4_DOCUMENTS.md

### Objective

Make the four-doc drafting process explicitly source-grounded and
deliverable-bounded rather than “cite sources when possible.”

### Planned changes

1. Add an authority hierarchy near invariants
   - authoritative source package
   - `_REFERENCES.md`, `_CONTEXT.md`, decomposition entry
   - existing drafts
   - `_SEMANTIC_LENSING.md`

2. Add a bounded authority-set definition
   - local authoritative references relevant to the deliverable
   - cited source sections supporting requirements, values, rationale, and
     procedural content

3. Add a source-slice heuristic
   - cited clause/section
   - parent applicability/scope framing
   - embedded tables, notes, exceptions, acceptance criteria

4. Strengthen Step 1 for Pass 1
   - reading authoritative local sources becomes required when available and
     relevant, not merely best-effort

5. Strengthen Pass 1 drafting rules
   - `Datasheet.md` values must come from source or become `TBD`
   - `Specification.md` requirements must come from source or be labeled
     `ASSUMPTION`
   - `Guidance.md` rationale must not outrun source support
   - `Procedure.md` steps must not be invented from generic convention unless
     clearly marked `TBD` / `ASSUMPTION`

6. Strengthen Pass 2
   - define source-reread triggers for resolving inconsistent values,
     requirement/verification drift, terminology drift, and overclaimed
     rationale

7. Strengthen Pass 3
   - require rereading implicated source slices before applying lens-driven
     edits
   - explicitly state that `_SEMANTIC_LENSING.md` cannot authorize new facts

8. Extend QA contract
   - authoritative source set identified
   - material claims grounded in accessible authority
   - unsupported source gaps converted to `TBD`
   - Pass 3 changes rechecked against source

### Expected outcome

`4_DOCUMENTS` remains fast and bounded, but becomes materially less likely to
drift into summary-based or draft-based fabrication.

## 3. AGENT_ORCHESTRATOR.md

### Objective

Only revise if needed to align orchestration expectations with the new source
grounding contract.

### Planned change decision

Default posture: no required change.

Optional later change:

- add one short note that `4_DOCUMENTS` and `DOMAIN_DOCUMENTS` are expected
  to read bounded authoritative source slices, not only decomposition
  summaries, when local sources are available

This is not required for the first revision because the behavioral contract
belongs mainly in the drafting agents themselves.

## Recommended Revision Order

1. Update `AGENT_DOMAIN_DOCUMENTS.md`
2. Update `AGENT_4_DOCUMENTS.md`
3. Review for shared wording patterns and normalize terminology
4. Optionally adjust `AGENT_ORCHESTRATOR.md` if the human wants orchestration
   text to advertise the stronger grounding contract

## Editing Method

When implementing:

1. Preserve the existing agent shape and pass model
   - do not redesign the pipeline
   - do not add new passes

2. Prefer local insertions over broad rewrites
   - invariants section
   - Step 1 context/source read section
   - Pass 2 consistency section
   - Pass 3 enrichment section
   - QA contract
   - rationale

3. Keep “bounded, evidence-first” language consistent across both files

4. Avoid introducing mandatory corpus-wide rereads

## Acceptance Criteria For The Future Instruction Revision

The revision is acceptable when:

1. Both drafting agents define a clear authority hierarchy.
2. Both drafting agents define a bounded source set and source-slice rule.
3. Pass 1 explicitly requires source reading when relevant local sources are
   available.
4. Pass 2 explicitly distinguishes draft-local checks from source-reread
   triggers.
5. Pass 3 explicitly requires source reread before substantive lens-driven
   edits.
6. QA contracts include source-grounding checks, not just citation presence.
7. No instruction requires full-document rereads by default.

## Risks To Avoid During The Revision

1. Overcorrecting into a mandatory full-corpus read for every deliverable/KTY
2. Using vague wording like “best-effort source review” where stronger rules
   are needed
3. Making Pass 3 depend on source access so rigidly that normal enrichment
   collapses unnecessarily
4. Letting decomposition remain de facto authority despite new language
5. Adding too much process burden for trivial or low-risk edits

## Open Decisions Before Applying The Revisions

These should be settled before converting this plan into redlines or patches:

1. If required local source files are missing, should Pass 1:
   - continue with warnings and `TBD`, or
   - fail as `FAILED_INPUTS`?

2. Should `_REFERENCES.md` later distinguish:
   - governing authority sources
   - background/context sources

3. Should Pass 3 require explicit run-report evidence that the cited source
   slices were re-read before a change was made?

4. Should standards named in decomposition or references be treated as
   governing only when their actual text is locally accessible?

## Deliverable Of The Next Step

If approved, the next work product should be:

- exact redline text blocks for `AGENT_DOMAIN_DOCUMENTS.md`
- exact redline text blocks for `AGENT_4_DOCUMENTS.md`
- optional minor redline for `AGENT_ORCHESTRATOR.md`

No wider file set should be touched in the first implementation pass.

## Short Summary

This plan prepares a narrow, controlled instruction revision:

- strengthen source fidelity in `DOMAIN_DOCUMENTS`
- strengthen source fidelity in `4_DOCUMENTS`
- keep the change bounded to authority order, source reading rules, pass
  behavior, and QA
- avoid changing the overall pipeline structure
