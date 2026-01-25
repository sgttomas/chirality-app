# SPEC

## Normative — "What must it be?"

This document defines the requirements for a valid project decomposition.

---

## Completeness Requirements

A decomposition is complete when:

| Requirement | Validation |
|-------------|------------|
| Scope defined | Agent and user have aligned on the project scope (the Scope of Work has been transformed into a Structured Scope of Work (normalized scope items + taxonomy) that is coherent) |
| Project defined | Project name + objectives derived from the structured scope and confirmed by the user |
| Objective coverage (best-effort) | Each objective is supported by one or more Deliverables when reasonably possible; unmapped objectives are surfaced as open issues |
| All Packages have scope | No Package without scope description |
| All Deliverables assigned | Every Deliverable belongs to exactly one Package |
| All Deliverables have responsibility | Responsible party identified for each |
| All Deliverables have type | Artifact type specified for each Deliverable |
| Artifacts anticipated | Expected Artifacts identified within Deliverables |
| Full coverage verified | All scope items represented in Deliverables |

---

## Consistency Requirements

A decomposition is consistent when:

| Requirement | Validation |
|-------------|------------|
| No orphan Deliverables | Every Deliverable has a parent Package |
| No orphan Artifacts | Every Artifact has a parent Deliverable |
| No scope gaps | Package scopes cover the project without gaps |
| No scope overlaps | Each scope item belongs to exactly one Package (explicit assignment exists); overlaps are resolved by redefining boundaries, splitting items, or adding Packages |
| Terminology consistent | Language used consistently throughout |
| Scope coherence | Structured Scope of Work is consistent with the user's input across ontology, epistemology, praxeology, and axiology; discrepancies are surfaced and resolved by the user |
| Organization scheme applied | Same scheme used consistently across Packages |
| Artifact type consistency | All Artifacts within a Deliverable share the same type |
| Contradictions surfaced | Agent identifies inconsistencies; user decides resolution |

---

## Invalid States

A decomposition is invalid if any of the following are true:

| Invalid State | Why |
|---------------|-----|
| Deliverable without parent Package | Violates containment |
| Artifact without parent Deliverable | Violates containment |
| Package without scope description | Cannot determine what belongs |
| Overlapping Package scopes | Ambiguous assignment (a scope item belongs to more than one Package) |
| Deliverable with no responsible party | No accountability |
| Deliverable with no type | Cannot constrain Artifacts |
| Artifacts of mixed types in one Deliverable | Violates type consistency |
| Scope not defined | Structuring without scope definition |
| Skipped confirmation gate | User validation bypassed |
| Contradictions not surfaced | Agent failed to identify inconsistencies |

---

## Anti-Patterns

Behaviors that produce invalid decompositions:

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| Agent invents structure without input | No grounding in tacit knowledge |
| User works without structure | Knowledge stays tacit, cannot be shared |
| Allowing overlapping Packages | Ambiguity persists; scope cannot be cleanly assigned |
| Skipping confirmation gates | Errors propagate without correction |
| Resolving ambiguity silently | Assumptions become hidden defects |
| Structuring before scope definition | Structure built on unstable foundation |
| Failing to surface contradictions | Inconsistencies become embedded defects |
| Proposing without explaining reasoning | User cannot evaluate or correct the proposal |
| Agent self-approves | Bypasses user validation |
