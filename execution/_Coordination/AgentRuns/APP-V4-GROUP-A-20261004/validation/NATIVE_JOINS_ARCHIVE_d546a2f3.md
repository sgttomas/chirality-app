# Group A native joins: committed candidate validation

2026-10-05. HELP_HUMAN `/root` tested complete Git archive `d546a2f316d444f4c53db780330e239bd0ccbc48`, based on merged PR #1096 (`196914d35bb0c41630331352b2183504a65531ef`). Existing approved dependency cache and stock Codex 0.160.0 were used; no downloads, authentication, model turns, native UI, signing or release occurred in these checks. Private future native-page and A15 work was not supplied.

| Check | Result |
|---|---|
| `cargo test --offline --locked` | 482 passed, 0 failed, 2 ignored; 73.01s |
| `npm test` | 3 passed, 0 skipped; isolated stock handshake included |
| `npm run build` | TypeScript and Vite passed |
| `python3 schemas/sync.py` | 6 canonical resources match bytes, hashes and IDs |
| Source invariance | All 3794 archived regular source files unchanged |

The ignored internal worker is exercised by its watchdog; the authenticated backend smoke remains unrun. Stock handshake uses an isolated scratch home and localhost stand-in provider without a model turn. Cargo reservation was released after execution.

Independent bounded reviews cover [OAuth Host/privacy](../reviews/V3-I1-OAUTH-HOST-RECEIVING.md), [OAuth Root receiving](../reviews/V3-I1-OAUTH-ROOT-CONSUMING.md), [development catalog API](../reviews/V3-I2-DEVELOPMENT-CATALOG-API.md), [copied content and tranche](../reviews/V3-I2-DEVELOPMENT-CATALOG-CONTENT.md), and [capture-label repair](../reviews/V3-I3-CAPTURE-LABEL.md). Each retains its original findings and successor disposition. The last review verifies that the later writer-facade repair leaves the previously reviewed OAuth code unchanged. OH-1 malformed authentication framing, OR-1 stale generation/replaced operation, and the fabricated AC-8 label each retain actual failing controls and reviewed repairs; passing aggregate counts alone are not their disposition.

Actual native OAuth/authentication, genuine native-page supply, workflow registration, hot A15 capture, external host witnesses and Group A closure remain unfinished. SEAL-2 is explicitly deferred by the owner. The development catalog is build-owned development admission, not release qualification or A15 registration. The earlier approved UI inspection applies only to the PR #1096 binary; it does not qualify this successor. No 90% gate acceptance is implied.

Raw logs and result/summary JSON remain machine-local at `/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-v4-candidate-639961vl`. Reproduce from Git and maintained checks; temporary files are not product dependencies.

| Raw log | SHA-256 |
|---|---|
| `rust.log` | `3a69e1be47ea576ef30d050f0054cab4b75d880b610ca95a9f45d5a30e87fd3f` |
| `node.log` | `4b41d205f2bfbcaac85f9490e7cef22cfc0348c4f4329b0980bc043f4fccba65` |
| `frontend.log` | `4a68f5acb3703b9eb90f948578722cf7870a8b602d89362b37acbbaa240e6b59` |
| `schemas.log` | `fea59bb900e1e9438e2645cec44da4fbbe38c1e184ba04541fa447a5ad31fb55` |
