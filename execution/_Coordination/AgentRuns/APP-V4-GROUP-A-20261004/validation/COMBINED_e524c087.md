# Combined pause checkpoint: compile and check

HELP_HUMAN (Claude Opus 5.5, Claude Code session of 2026-10-07) checked the
committed pause checkpoint **e524c087f563d0cae8e61c51f41301c3d27b13ff**. Its
App sources equal the 276-file pause manifest
(`recovery/PAUSE-ASTRA-20261006/CURRENT_APP_SOURCES.json`) byte for byte. This
is the first compile and check of the combined REC custody, REC Root reader,
WR publisher, RS historical correspondence and compatibility-core fan-in.
Before this, each contribution had been reviewed only on its own.

| Check | Actual result |
|---|---|
| `npm run build` | TypeScript and Vite passed |
| `python3 schemas/sync.py` | 6 resources match canonical bytes, hashes and IDs |
| `cargo build --offline --locked` | Exit 0; 51 warnings, all dead code (below) |
| `cargo test --offline --locked` | 40 targets: 595 top-level passes, 0 failures, 3 marked ignored; 58.9 s |
| FIFO worker subprocesses | 4 additional successful nested executions, counted separately |
| `npm test` | 3 passed, 0 skipped; stock 0.160.0 handshake included |
| Source invariance | `git status` shows no tracked change under `app/` after the checks |

Comparison: the PR 1099 archive (b44f6bfc) had 550 top-level passes. The 45
additional tests are the integrated REC, WR, RS and compatibility tests.

**Environment.** The tests ran against the complete stock Codex 0.160.0
package (`bin/codex` sha256 `112fae7a…b4b`) with its `codex-path` on `PATH`,
using fresh isolated homes created by the tests. Cargo used the restored
isolated home (`dependencies/RESTORE_20261007.md`) offline. There was no
model call, authentication, native UI or credential use.

**What this establishes.** The combined source compiles, and every maintained
test passes on it. No integration failure was found, so there was nothing to
diagnose or repair.

**What it does not establish.** The warnings show which produced parts still
have no production caller:
- the WR publication types (`PreparedRunPublication`, `PublishedRunText`,
  `CompletedSupplyCheck`, `PreparedEndPublication`, `PublishedEndNotice`, and
  the store's `new`/`publish`);
- the run-end lifecycle (`RunEndReason` variants `ByPerson`, `Completed` and
  `ToStart`, and `end_notice`);
- the compatibility report (`PreparedReport`, `Check`, `Outcome`, `Basis` and
  related types in `compatibility_report.rs` and `execution_compatibility.rs`);
- `RegistrationAdapterClaim` and `RegistrationClaimMatch`.

These are the connecting obligations already named in the pause handoff,
resume steps 3–5. Passing component and combined tests is not evidence of
the connected journey, native behaviour, or the 90% gate.

Logs are retained beside this file in `COMBINED_e524c087/`:

| Log | SHA-256 |
|---|---|
| cargo-build.log | `2459308b8506581e40665ce30f620988c9a6ee3aa1ae48af70ecac25aabe19f7` |
| rust.log | `8bf02bec0b6e558d6171c2b4faa1154aaa2ba204674df630675e9675881a9fd7` |
| node.log | `afc866a5d675616d62b9d2023f5184ef3fe470237e1305aada6f0852a266e685` |
| frontend-build.log | `b55f517300508c2763b94606f333254a718d5e262ed135fb727e14105b7e20aa` |
| schema-sync.log | `fea59bb900e1e9438e2645cec44da4fbbe38c1e184ba04541fa447a5ad31fb55` |
