---
name: construct-local-work-graph
description: Derive the relevant dependency neighbourhood and plan a route from the user's intended result to usable work.
metadata:
  kind: instruction
  surface: workflow
---
# Construct a local work graph

Use this method when connected work needs a sequencing decision. A work graph
is an optional, generated view, not an authored progress record or a prerequisite
to ordinary work. The human's steering supplies the objective; deliverable files
supply current commitments, design and dependency conditions.

Read the affected scopes, then query the relevant upstream and
downstream needs with the project's deliverable tool when available. Until that
tool is available, inspect the relevant dependency sources directly. Follow only
connections needed to understand this undertaking. Preserve non-gating links and
report cycles; a mutual design relationship need not be an impossible execution
order. A missing input or unclear mapping stays unknown.

Compare those needs with code, artifacts, checks and in-flight PRs at the actual
revision. Existence or a merged PR does not establish fulfilment. Evaluate a
condition automatically only where a reliable executable check establishes it;
otherwise assess suitability from the evidence. Identify the specific unresolved
condition before blocking dependent work.

Plan the smallest useful route to the intended result. Name outcomes, relevant
deliverables, required inputs, write boundaries and meaningful checks in the
assignment. Use one integration owner and disjoint concurrent writes. Apply
`coordinated-knowledge-work` where contributions need coordination. Verification
and independent scrutiny follow the consequences under the Library's `AGENTS.md`.

Update scope or dependency conditions in their source files when the
work changes them, obtaining owner decisions for reserved commitments or
criteria. Regenerate a graph when needed; do not commit the generated view or
maintain a second status table. Code-path matches identify relevance, not
exclusive ownership or completion. PRs hold the change and verification account.

Finish when the authorized result and its required checks are established.
Return the result location, checks, findings and open decisions. No compulsory
closeout PR, receipt, MEMORY update, recovery note or handoff chain is part of
this method.
