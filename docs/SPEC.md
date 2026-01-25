# SPEC

## Normative — "What must it be?"

This document defines the requirements for a valid project decomposition.

---

## Completeness Requirements

A decomposition is complete when:

| Requirement | Validation |
|-------------|------------|
| Scope defined | Agent and user have aligned on what the scope contains |
| Project defined | Project with objectives established |
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
| Terminology consistent | Language used consistently throughout |
| Organization scheme applied | Same scheme used consistently across Packages |
| Artifact type consistency | All Artifacts within a Deliverable share the same type |
| Contradictions surfaced | Agent identifies inconsistencies; user decides resolution |

---

## Validation Requirements

| Requirement | Description |
|-------------|-------------|
| User validates at each gate | Confirmation required before proceeding |
| User is the halting condition | Decomposition complete when user explicitly approves |
| No self-approval | Agent does not declare its own output valid |
| Scope alignment first | Scope must be aligned before structuring begins |

---

## Invalid States

A decomposition is invalid if any of the following are true:

| Invalid State | Why |
|---------------|-----|
| Deliverable without parent Package | Violates containment |
| Artifact without parent Deliverable | Violates containment |
| Package without scope description | Cannot determine what belongs |
| Overlapping Package scopes | Ambiguous assignment |
| Deliverable with no responsible party | No accountability |
| Deliverable with no type | Cannot constrain Artifacts |
| Artifacts of mixed types in one Deliverable | Violates type consistency |
| Scope not defined | Structuring without scope definition |
| Skipped confirmation gate | User validation bypassed |
| Contradictions not surfaced | Agent failed to identify inconsistencies |
