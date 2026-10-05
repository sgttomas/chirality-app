# Exact App v4 access candidate validation

2026-10-05. HELP_HUMAN `/root`. Code candidate `ff9a8d51d9007075acc7edf4e0365e4bc8f0080a`, including normal main integration `c47d63c5af4f74778c9c70afeeed85d75f733e26` / main `0d151c64692ec2f213afc8e798d50752f28947c4`. Complete Git archive of `projects/chirality-app-v4`; no live working files or unapplied OAuth patch supplied code. Existing approved dependency cache and stock 0.160.0 binary used. No downloads, authentication, model turn, native App UI, signing or release.

| Check | Actual result |
|---|---|
| `cargo test --offline --locked` | 445 passed, 0 failed, 2 ignored; 62.79s |
| `npm test` | 3 passed, 0 skipped; includes isolated stock initialize/thread-start handshake |
| `npm run build` | TypeScript and Vite passed |
| `python3 schemas/sync.py` | 6 resources match canonical bytes, hashes and IDs |
| Archive source after checks | All 3743 regular tracked files byte-identical to archived source |

One ignored internal worker is invoked by its passing watchdog; the authenticated backend smoke remains ignored/unrun. The stock handshake uses actual `mktemp -d` homes, a localhost:9 stand-in provider, no login and no model turn. Socket-observation failures now fail the maintained check; no OS-wide network-isolation guarantee is inferred.

## Original failure and bounded disposition

The first full archive at `c47d63c5…` stopped at `hosting_contract.rs:86`: a second home returned counter1 where the old test expected counter2. [Original result](ACCESS_ARCHIVE_c47d63c5_FAILED.json) is retained. HOST H5/REC require the full session/home/counter identity, not one cross-home numeric sequence. The [owning-criterion review](../reviews/V2-I1-GENERATION-COUNTER-DISPOSITION.md) independently accepts removing that incidental assertion and adding actual restart, return, custody recreation, independent-session and full-generation controls. Production and Design bytes did not change to obtain the pass. This run checks that reviewed successor; it does not erase the original failure.

## Review and integration standing

Bounded source reviews remain at their exact scopes: [Core guard](../reviews/V2-I1-NATIVE-NAMESPACE-GUARD.md), [shared App consumer](../reviews/V2-I1-ACCESS-CONSUMING.md), [pointer-queue retirement repair](../reviews/V1-I1-SHARED-APP-CUSTODY-R1.md), [credential RPC](../reviews/V1-I1-CREDENTIAL-RPC-R2.md), and [socket observation](../reviews/V2-I1-HANDSHAKE-OBSERVATION.md). The graph links reviewed workflow/parser, private controller, native-page accessor, reader and CP0 contributions. Incoming main changed only App loop wording/notices, not candidate product bytes; historical consultation hashes remain unchanged.

Actual native key entry/logout execution, OAuth Host/presentation hooks, genuine native-page/workflow supply, real registration/shipping/capture authority, deferred SEAL-2/cold replay, external host witnesses and whole-Group-A closure remain open. This is one substantive code contribution, not a stage-gate or release decision. Cargo/target reservation released after checks.

## Recoverable execution

Machine-local archive and raw logs: `/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-v4-candidate-sqou5da4`. `result.json` records exact commands' exits and durations; `summary.json` records counts and source comparison. Reproduce through the checked Git revision and maintained tests; temporary paths are not product dependencies.

| Raw log | SHA-256 |
|---|---|
| `rust.log` | `29e82635d061073fffde5e5fec095436794b6b152190faf4a53aa0be4ce0df8f` |
| `node.log` | `342056afded69f592f140577d76af20b2fbbf1ebd3fdcae3cc2e5cf39db7ca11` |
| `frontend.log` | `2e71e55c4ddd5d8e1a2e0ffacc6bda6a6fb0aa79aa73824392ceb11d6ca84f6c` |
| `schemas.log` | `fea59bb900e1e9438e2645cec44da4fbbe38c1e184ba04541fa447a5ad31fb55` |
