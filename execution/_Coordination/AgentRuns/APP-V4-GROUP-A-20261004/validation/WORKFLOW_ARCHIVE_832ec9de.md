# Workflow receiving: repaired committed archive validation

HELP_HUMAN `/root` validated complete Git archive **832ec9de93f9d2f28bf536a323bef2d93e06d9f7**. This includes the reviewed workflow contribution at a515b5bf and the independently reviewed test-only failed-write fixture repair. No private witness or later file-act implementation supplied code to this archive.

| Check | Actual result |
|---|---|
| `cargo test --offline --locked` | 528 passed, 0 failed, 2 ignored; 69.44s |
| `npm test` | 3 passed, 0 skipped; isolated stock handshake included |
| `npm run build` | TypeScript and Vite passed |
| `python3 schemas/sync.py` | 6 canonical resources match bytes, hashes and IDs |
| Source invariance | All 3883 archived regular tracked files unchanged |

The ignored internal worker is exercised by its watchdog; the authenticated smoke remains unrun. Existing approved dependency cache was used. Stock Codex 0.160.0 ran from its [complete, integrity-checked development layout](../probes/CODEX_0160_COMPLETE_DEVELOPMENT_INSTALL.json), with the package's codex-path prepended in the child environment. Main binary identity is unchanged. No download, authentication, real model turn, native App UI, human act, signing or release occurred in these checks. Complete development layout is not qualified distribution identity.

## Failure and warranted repair

The [original a515 archive](WORKFLOW_ARCHIVE_a515b5bf_FAILED.json) stopped at the failed-write `sentFrame.is_null()` assertion. Its exact executable and unchanged source remain preserved. Astra diagnosis observed the killed test peer's pipe reader in other still-spawning owned children; actual writes could therefore succeed. The Host reported those writes correctly. The isolated passing rerun was not treated as repair.

The cfg(test)-only helper now supplies a read-only descriptor, producing an actual OS write failure. Original assertions, positive pipe controls and parallelism are unchanged. [Independent V5 review](../reviews/V5-HISTORY-WRITE-REPAIR.md) checks the source boundary, original oracle, affected Host controls and separate concurrent descriptor controls. No production behavior was changed to obtain this pass.

## Review and remaining scope

The candidate retains the independent Host page/sender, hot A15, registration/durability/listing, settings-comparison and Root receiving reviews identified in [the manager handoff](../MANAGER_ASTRA_HANDOFF.md). The Root lock-order failure and original repair controls remain recorded. All blocking findings in this contribution have reviewed dispositions; the new full archive covers their assembled source.

The private connected supplier witness remains uncompiled/unexecuted at this validation boundary. Native UI/capture/auth/provider journeys, complete child-role discovery and supply (CI-15), deferred SEAL-2 cold provenance, external host inputs and whole Group A C1/M1/F1 remain open. No 90% acceptance or release is inferred.

Raw logs, result and summary JSON are at `/private/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-v4-candidate-_y_sr0ch`. Reproduce from the committed source and maintained checks; temporary paths are not product dependencies. Cargo was released after execution.

| Log | SHA-256 |
|---|---|
| rust.log | `f27f98b84608c118490c6d32415741e7e7e4460aa56dcd204a01f087ee035ba3` |
| node.log | `1535ecb8ea530ae371b29b32a2409a6701e6e6c138da9d37451063ce7b1a17a1` |
| frontend.log | `67c3a102d0f6543c383d2eef8bedd68fb5f6577da0afb612e06f6da8617fb913` |
| schemas.log | `fea59bb900e1e9438e2645cec44da4fbbe38c1e184ba04541fa447a5ad31fb55` |
