# QA CHECKS — scope-of-work

Items 2, 5–7, 10–12, 14, and 17 apply to `CONVERT` only; under `INIT` they are
`NOT_APPLICABLE` and are recorded as such rather than passed or failed. Items
1, 3, 4, 8, 9, 13, 16, and 18 apply to every mode. Item 15 applies whenever an
HTML derivative was requested, in any mode. Items 19, 20, and 21 apply to every
mode. `VERIFY` runs the mode-applicable subset read-only.

1. The exact pilot variance covers the deliverable path.
2. All four source files exist, remain byte-identical, and retain authority.
3. `_STATUS.md` is byte-identical and its lifecycle state is unchanged.
4. Working-contract frontmatter, headings, IDs, references, and matrix validate.
5. Every source line is covered by a source marker and disposition.
6. Every marker binds the current source hash and a defined target ID.
7. `MERGED` and `SPLIT` mappings preserve all contributing references.
8. Every `OUT-*` maps to declared scope/objective references.
9. Every `AC-*` maps to `VER-*` or an explicit human-review method.
10. Finalization is deterministic; its external report binds the evidence
    candidate, clean production hash, source metadata, authority, and any
    `ISSUED` preparation metadata.
11. The clean production contract validates, preserves literal source content
    as quotations, and contains no source markers, migration authority,
    preparation bindings, or migration-candidate labels.
12. The claim map and parity report bind the clean production hash and reject
    a modified or independently authored production file.
13. Deterministic checklist JSON contains every production `AC-*` exactly once,
    in source order, with exact text, qualified/source identity,
    production-contract hash, and its matrix-linked `VER-*` or explicit
    human-review method.
14. Parity passes with no silent drop or text mismatch.
15. Repeated HTML rendering is byte-identical, production-hash-bound, script-free,
    and contains no external resource reference.
16. The return distinguishes schema, project-content, and execution-substrate
    findings.
17. No accepted branch is left in dual-format state, and no evidence-rich
    candidate is selected for integration.
18. Repeated checklist derivation is byte-identical, and invalid or ambiguous
    input without the exact variance fails without an output artifact.
19. Every upstream deliverable's local ID is cited either in the qualified form
    (`DEL-NN-NN/REQ-NNN`) or inside a blockquote carrying an explicit
    upstream-context carve-out; no own-voice prose carries a bare ID-shaped
    token that is not a local definition or local reference.
20. No Output and Evaluation Matrix row groups multiple `AC-*` whose own
    verification method sets differ — grouping is permitted only when every
    grouped criterion is verified by exactly the same methods, and the row's
    verification set is exactly that shared set; the derived checklist entry
    for each `AC-*` names no method that does not verify it.

21. Every act excluded by a boundary-exclusion requirement resolves one-for-one
    to a named owner in a claim that requirement cites, and
    `check_boundary_owner_resolution.py` reports no `UNRESOLVED_OWNER` or
    `UNDEFINED_CLAIM` finding for the contract.

Any failure produces a failed return and rerun requirements; it does not
silently weaken the acceptance gate.
