---
name: proposal-format
description: Express actionable Chirality findings as evidence-grounded PROPOSAL blocks with precise changes, risks, status, and a human-decision interface.
---

# Proposal Format

Use this format for recommendations within one declared deliverable. When no specific task is supplied, scan for the highest-value completeness, consistency, verification, source-fidelity, and identity issues, plus unresolved markers and dependency concerns.

Write every recommendation as:

```text
- PROPOSAL: <short title>
  - Evidence: <file and best-effort section or heading>
  - Change: <precise change>
  - Why: <clarity, completeness, verification, consistency, source fidelity, or other concrete benefit>
  - Risk: <specific downstream effect or conflict>
  - Status: <PROPOSED | APPLIED | NEEDS_HUMAN_RULING>
```

Use `PROPOSED` by default, `APPLIED` only when an authorized edit was made, and `NEEDS_HUMAN_RULING` for a real contradiction, trade-off, or scope decision. Evidence must cite accessible authority or production content; use `location TBD` when the exact anchor is unknown. A semantic worklist is not evidence. Add a `Lens:` field only when semantic lensing is active or explicitly requested.

After the proposals, always provide `MISSING:`, `NEEDS_HUMAN_RULING:`, and `DEPENDENCY_NOTES:`; each may be `none`. Keep unknowns as `TBD`, make each change specific enough to apply without interpretation, and state when no meaningful issue exists rather than padding the result.

Do not invent supporting evidence, widen scope, or silently reconcile conflicts. Apply changes or update deliverable memory only when the request explicitly authorizes those writes.
