---
name: bounded-reconciliation
description: Compare affected deliverable commitments, design and dependency conditions with a concrete result and make warranted source edits.
metadata:
  kind: instruction
  surface: workflow
---
# Bounded reconciliation

Use this method when a change may leave its current deliverable documents out of
step with the result. Reconcile as the work develops and before integration;
this is a bounded comparison, not a separate compulsory ceremony or corpus audit.
Perform warranted edits in the PR doing the work. The implementation owner carries
the requirement into bounded assignments and owns it through repairs; the
integration owner checks the combined result before merge.

Identify the affected deliverables, actual candidate, relevant consumers and
permitted scope from the assignment and diff. Read their ScopeOfWork, the code
it represents and dependency conditions. Follow only the sources needed to establish the
meaning of the affected commitment or interface. During migration, existing
CSV dependencies remain source inputs until their replacement is available.

Compare the documents with implementation and meaningful verification, under
[the scope leads](../scope-of-work/WORKFLOW.md#what-a-scope-says). Separate
missing behaviour from stale description and missing evidence. A passing rerun
alone does not explain how a known defect was repaired.

Correct ordinary factual descriptions and dependency conditions within the
assignment, including a need this work showed to be wrong or missing, or to no
longer apply. Decisions edit the current text they govern. Preserve commitments,
acceptance criteria, explicit holds and product boundaries; bring a changed
commitment, unresolved intent or code outside the deliverable's identity to the
owner as a concrete choice and consequence. Do not turn incidental
implementation detail into another continuing documentation obligation.

Reconcile a scope only if the thing being made, or its description within the
six parts, materially changed. Keep `code_paths` and check pointers accurate
when their bindings change, even when the need conditions remain unchanged.

Check the changed documents together with affected consumers. Where a comparison
finds no warranted edit, report that result without creating a record. Where it
finds unfinished required work, repair it within authority or report the specific
obstruction; moving it to another list does not complete it.

Return the changed locations, checks, findings and open decisions. The PR is the
change record. This comparison does not itself declare acceptance or release.
