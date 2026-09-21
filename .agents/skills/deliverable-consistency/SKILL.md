---
name: deliverable-consistency
description: Check one Chirality deliverable for unresolved markers, missing core artifacts, identity mismatches, cross-document conflicts, and candidate unsourced numeric statements.
---

# Deliverable Consistency

Keep the review within one declared deliverable. Resolve its production format and any requested document focus before scanning; ambiguous, invalid, partial, or unauthorized dual-format input fails closed.

Run `tools/validation/scan_deliverable_consistency.py` first when available, then inspect only the flagged files and nearby context. Compare files directly where the deterministic scan cannot decide. Check unresolved `TBD`, `ASSUMPTION`, and `CONFLICT:` markers, required artifacts, identity labels, cross-section or cross-document consistency, and numeric claims that may lack a source.

Return evidence-backed findings as `PROPOSAL:` blocks, missing inputs under `MISSING:`, and genuine contradictions under `NEEDS_HUMAN_RULING:`. Cite each finding to a file and best-effort heading or section. Preserve unknowns as `TBD` and say explicitly when the sweep finds no meaningful issue.

Apply only minimal, reversible corrections when edits are explicitly authorized. Do not widen the review beyond the deliverable or silently resolve a conflict.
