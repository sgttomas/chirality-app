# deliverable-consistency — QA Checks

Minimum checks for a valid run:

1. The deliverable path exists.
2. The deterministic scan completes successfully unless tool use was explicitly excluded.
3. The findings reference only files inside the deliverable.
4. Each significant finding includes best-effort evidence location.
5. Contradictions are surfaced as rulings-needed items, not silently resolved.
6. If edits were applied, they are limited to authorized files.
7. `MEMORY.md` captures any durable decisions or accepted proposals.

Recommended reporting groups:

- identity mismatch
- unresolved markers
- contradiction
- unsourced numeric parameter
- missing artifact / missing reference

Success case with no findings:

- Explicitly state that no material consistency findings were discovered in scope.
- Mention residual risk if references are sparse or some artifacts were missing.
