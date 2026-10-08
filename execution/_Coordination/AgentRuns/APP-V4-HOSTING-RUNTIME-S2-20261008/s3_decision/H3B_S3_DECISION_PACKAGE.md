# H3B S3 acquisition and probe decision package

**Prepared for independent review, then the parent's owner decision. No acquisition or native execution is authorized by this document.** Recommended candidate for investigation: Codex **0.161.0**, macOS ARM64, latest non-prerelease reported by official release metadata at lookup. It is **not a qualification pin** until the R23-22 version-advance rule is satisfied. Recommend authorize A+B below first; retain C as separately bounded live-version-advance work once its actual local provider basis is concrete.

Prepared 2026-10-08, metadata lookup completed before 12:29:22 UTC. TASK `/root/hosting_runtime_manager/rs_concurrence` under WORKING_ITEMS `/root/hosting_runtime_manager` under HELP_HUMAN `/root`, harness-native bounded preparation; no delegation. Parent authorized read-only official upstream metadata lookup. No archive, binary, extraction, supplier launch, signing, credential operation or build occurred. Only JSON/text metadata was retrieved, and this temporary report/evidence was saved.

## Concrete artifact offered for authorization A

| Item | Exact proposed value / observed metadata |
|---|---|
| Official release | [OpenAI Codex 0.161.0](https://github.com/openai/codex/releases/tag/rust-v0.161.0), tag `rust-v0.161.0`, release ID 405921402, prerelease=false |
| Release publication | 2026-10-07T15:58:45Z; release created_at 2026-10-06T22:34:38Z |
| Archive | `codex-package-aarch64-apple-darwin.tar.gz` (full package candidate; not the single-binary, app-server-only, DMG or provisioned alternative) |
| Exact download URL | https://github.com/openai/codex/releases/download/rust-v0.161.0/codex-package-aarch64-apple-darwin.tar.gz |
| Compressed size | **131,714,490 bytes** (131.71449 decimal MB; approximately 125.612 MiB), asset ID 619133667 |
| Published digest | SHA-256 **f0feee8537daf8dd6b4e0a36e764549ad14afdbb419d8775aeab9feb20182313** |
| Digest/size source | Official GitHub release API: https://api.github.com/repos/openai/codex/releases/tags/rust-v0.161.0 ; latest selection discovery: https://api.github.com/repos/openai/codex/releases/latest |
| Asset timestamps | created_at 2026-10-07T15:58:19Z; updated_at 2026-10-07T15:58:24Z |
| Unpacked size / actual archive shape | **Not measured or established by this lookup.** Do not reuse 0.160.0's unpacked estimate as this archive's size. Inspect the authorized archive before extraction/measurement; package-name compatibility is not proof of selected vendor-tree shape. |
| Proposed scratch root | `/private/tmp/chirality-s3-0161-20261008-<fresh-random>` created exclusively at execution; no reuse/overwrite; user name absent |
| Proposed destinations | `acquisition/codex-package-aarch64-apple-darwin.tar.gz`, `extracted/`, `homes/probe/`, `homes/generator-<variant>-<run>/`, `generated/`, `evidence/` below that fresh root |

The digest is **published metadata**, not an independently recomputed archive digest. No supplier bytes were obtained or authenticated here. Preserve raw metadata evidence `/private/tmp/H3B_S3_RELEASE_METADATA.json` (hash below). At actual acquisition recheck asset identity/size/digest, retain response/redirect provenance and locally recompute SHA-256; a changed asset/digest or mismatch stops reliance and returns the concrete changed package, never silently substitutes latest. A stable release URL alone is not immutable-byte proof. This approval target is one archive, not all release assets or dependencies.

## Accepted rule and prior authorization boundary

R23-22 §2 and PKG U-PKG-3 select **the newest version that has passed a version-advance check when the candidate is built**, not whatever upstream labels latest. 0.158.0 remains the historical definition/generation basis; 0.160.0 is recorded checked/design-compatible. There is no qualified pin asserted by HOSTING §9.5. A newer candidate cannot inherit the old pass. Routine advance needs no new pin-choice decision unless a relied-on behavior changes; that does not waive the project's explicit download/native-action authority requirements.

The 2026-10-03 owner decision said “yes, download it” for the one npm file `codex-0.160.0-darwin-arm64.tgz` at `https://registry.npmjs.org/@openai/codex/-/codex-0.160.0-darwin-arm64.tgz`, for node VC/session scratch. Its stated effect permits that one file and requires a new answer for any other download or sign-in. It does not authorize this GitHub 0.161.0 archive or new probe run. The old VC's local-model executions and observed no-network result are historical execution evidence, not standing permission or a prediction for this version.

Current S2/Host source review is likewise not acquisition/native authorization: receiving `c9bfde526912b7da933c89f956ecc43489178a09`, reviewed Host `5c9aabcfb400bab3ef1e283362dc378414621da7`; exact-head review explicitly excludes S3/production selection/qualification. No use of owner credentials is requested.

## Authorization choices for the owner

**A — acquire and inspect only.** Authorize download of exactly the archive/URL/size/digest above into the fresh scratch destination; inspect headers/member paths without executing anything; verify digest; extract inertly into `extracted/` after rejecting absolute/parent-traversal entries, links/hardlinks, special entries, duplicate/conflicting paths and unsafe modes. No npm install, lifecycle scripts, system installation, chmod-based repair, signing or launch. Keep archive permissions/modes evidence and extraction procedure; use a safe containment-aware extractor, with no blind tar extraction. Determine the actual vendor subtree containing `bin/codex`, `codex-path`, `codex-resources`, `codex-package.json` without rewriting its contents. If absent or incompatible with selected bounded method, return mismatch/shape issue rather than assemble a substitute tree. Compute no-follow complete inventory/root+directory modes/empty directories/regular-file sizes+hashes, plus historical manifest. These are measurements, not qualified expectations.

**B — isolated label/help and generation probes (recommended together with A).** After A passes, authorize only the measured direct vendor executable, same-root `codex-path` prefix, isolated new probe/generator homes and outputs outside the vendor tree. Proposed arguments: `--version`, `--help`, `app-server --help`, generator help, then `app-server generate-ts --out <fresh-output>` and `app-server generate-json-schema --out <fresh-output>`, each with and without `--experimental`, each twice. No formatter download or `--prettier`; preserve raw outputs and exact manifests. Remove credential and wrapper environment variables by name, do not dump ambient values; do not read/copy/link real homes/configuration/auth/keyring. Use scratch-only configuration with analytics disabled and plugins disabled as in the accepted prior bounded VC, recording these as probe-specific settings. Do not modify user settings or production policy.

Expected B effects: new native supplier processes; scratch config/log/cache/tmp writes (including possible `tmp/arg0`); generated files; possible OS process/network observations; resource use. Previous flags reduced startup connections but cannot guarantee 0.161.0 is network-silent. Proposed B grants **no non-loopback network and no model-service contact**. Use actual host-enforced network restriction when available plus recorded monitoring/stop conditions; monitoring alone is not prevention. If required enforcement is unavailable or supplier attempts extra fetch/contact, stop and return the limit, do not follow links or download dependencies. No supplier app-server session, model load, tool execution or credential act is part of B. Record exact stdout bytes separately from trimmed/parsed label; label equality does not establish full-tree qualification. Recheck tree stability before/after probes and immediately before any separately authorized spawn.

**C — finish version-advance live coverage, later concrete sub-brief.** A+B alone cannot satisfy R23-22. HOSTING §9.5 also requires accepted-method handshake/error observation, validation of earlier recordings, necessary live captures and semantic comparisons/App seam replay; its version-advance paragraph calls for the local observation harnesses within their approved limits. The prior VC used LM Studio 0.4.16+2 with already-installed qwen/qwen3.5-9b, 24,576 context, one prediction at a time, direct loopback 127.0.0.1:1234 and taps on 12340/12350; **current availability and suitability have not been inspected or established**. This package does not authorize reuse of that provider or load. After A+B, prepare the exact current provider/model/version/memory cap, port/process ownership, scenario list and scratch harness hashes for an explicit C native-run decision. No model download, remote model, sign-in or credentials. Expected eventual C effects include supplier handshake sessions, loopback requests, local model memory/GPU use, scratch threads/logs, invented tool/approval fixtures, interrupts/stops and process cleanup. Non-loopback contacts and plugin fetch remain excluded unless separately named and authorized. Required cases that cannot run remain not checked, never “pass by omission.”

Owner can choose A only, A+B, defer all, or request a fully specified C package before any acquisition. These are concrete scope choices, not a request to approve supplier qualification. Parent should present them after independent review and record the owner's actual words/source; this preparer does not ask the owner directly.

## Missing R23-22/S3 evidence and completion contract

For 0.161.0 **all of the following remain missing/unperformed**:

1. Authorized acquisition/custody, local archive digest, safe extraction/source-subtree chain and selected full inventory comparison.
2. Isolated exact label, launcher/environment/home evidence and post-probe tree stability.
3. Both generator kinds × both variants × two runs, determinism, manifests and generation-source correspondence. Compare against maintained 0.158.0 definition/reference and 0.160.0 last checked outputs; no relabelling of old generated bytes.
4. Structural method/request/notification/field and experimental/divergence diffs; server's accepted-method list; supplement review; classify every changed seam consumed/not consumed.
5. Earlier-recording conformance, bounded obs1/obs2/obs3 reruns as required by current reliance, semantic recording diff/App seam replay, selected-version check and affected receiver statement inventory. Explicit gaps in old VC remain gaps; changed relied-on behavior returns for its applicable decision. Current release notes mention permission/configuration and resume behavior changes, so they warrant investigation, not automatic compatibility.
6. A source-bound version-advance result with unresolved incompatibilities and owning adoption disposition under R23-22; re-evaluate newest-passed at actual candidate build time. 0.161.0 may fail or remain incomplete; 0.160.0 remains only the last checked record found here, not silently qualified.
7. Frozen immutable expected-reference, then independent review and separate qualification attestation binding exact bytes, then trusted build selection/compiled anchor. No own-digest or final-App-package cycle; no synthetic attestation, runtime self-promotion or `qualified:true` shortcut. Supplier-reference qualification does not require Group B's final package; installed App/custody/signing/native witnesses remain separate.

A+B result is a measurement/generation packet with explicit C residuals. It must not claim completed S3, FP-2/W-4, installed integrity/custody, SEAL-2, App release or canonical consumer rollout. Keep raw evidence outside measured tree; preserve immutable artifacts before review. Parent coordinates DEL-01-01/06, affected RS/REC/ACCESS/NIR/examiners and separate exact-source consumer adoption.

## Lookup and source provenance

Official release HTML was opened using web tools; metadata JSON was retrieved with system HTTPS certificate validation after sandbox DNS and Python certificate-store failures. No TLS bypass used. GitHub OpenAI official upstream was used as explicitly requested; no release binary URL was fetched. Metadata/date/digest claims above derive from that first-party release record. Local governing texts were read via exact Git objects, not the stale local `main` branch.

| Source | SHA-256 |
|---|---|
| `projects/chirality-app-v4/loop/LOOP_INIT.md` at `c9bfde526912b7da933c89f956ecc43489178a09` | `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/R23_RESOLUTIONS.md` at `c9bfde526912b7da933c89f956ecc43489178a09` | `21b2ccfa0f63d61671eddcebe5c2a41dccd2fc5f901e529808605bd017b3fc11` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/OWNER_DECISIONS.md` at `c9bfde526912b7da933c89f956ecc43489178a09` | `e4350f61a93edf0d2d4bfc588fcaa17ae23981baa6059617dcc430cda3008cd8` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` at `c9bfde526912b7da933c89f956ecc43489178a09` | `9839cb38310ff55045657e51f7bb7dcfcb2024eb43ec3bab364959e33e5c1e85` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/VERSION_ADVANCE_0.160.0.md` at `c9bfde526912b7da933c89f956ecc43489178a09` | `0dee021d7dc425967b8cc6e867a970fd9397d63ff0f6d3c317e24fb900fad97a` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-06_macOS packaging and distribution evidence/Design/PACKAGING_AND_DISTRIBUTION.md` at `c9bfde526912b7da933c89f956ecc43489178a09` | `0d8d14d2ce08d859ec3b304f5c8c250afa7f0a6fe95eae3a61920f71d2a442b4` |
| `/private/tmp/H3B_S3_RELEASE_METADATA.json` | `cad3a563a812e0a9f5770c98da89e0272647bd5a05f99aec1e0b6caa87ac8f74` |
| `/private/tmp/hosting-secondary-manager/projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-HOSTING-RUNTIME-S2-20261008/h3b2_lt23/review/EXACT_HEAD_REVIEW.md` | `dbee9c335af5915e5404fb5017dba0db50a3468538ebafdf77abdadddf27d405` |
| `/Users/ryan/.codex/skills/.system/openai-docs/SKILL.md` | `aa6829e21df2223167c85d2e49b6337a7345c84c1033f1ec10182c7882b36d45` |
