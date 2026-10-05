# CC-REC-GEN — lossless full-generation references in RECOVERY

TASK `/root/group_a_execution/design_records_exec`, parent WORKING_ITEMS `/root/group_a_execution`; no delegation. Only DEL-01-02 Design and this record changed. Independent review before I1 product adoption. No App/Cargo/shared graph/SoW/register/MEMORY/Git/network/auth writes. Existing schema shapes and IDs are unchanged; old prototype results/source-version evidence remain history.

**Meaning recovered:** SoW CLM-002/REQ-001/REQ-003/REQ-005 require per-home custody and actual-state recovery without answering ended requests or upgrading unknown outcomes. HOSTING H5 exports full `{appSession, home, spawnCounter}`, unique across launches/homes; counter-only equality is confined to an internal cache explicitly scoped to session/home, never an exported record. RECOVERY §1/V2-1 already states this tuple, but its schemas use nonempty string `generation`/`lastLoadedGeneration` and prototype concatenates session/home/counter using slash delimiters.

**Named technical choice:** retain existing string schema and encode full tuple as exactly `gen:v1:s:<session-utf8-lowerhex>:h:<home-utf8-lowerhex>:n:<counter-decimal>`. Input session/home are nonempty Unicode scalar strings, strict UTF-8, no normalization; payload lowercase hex two digits per byte. Counter is actual positive H5 spawnCounter, canonical ASCII decimal without sign/leading zeros. Tagged fixed order and delimiter-disjoint hex give an injective/reversible representation; colons/slashes/NUL/Unicode cannot split the tuple. This is neither generation minting nor content hashing/canonicalization. No invented pre-spawn generation; optional ref omitted or generation-required event not emitted until source has actual tuple. Historical opaque references remain history, never silently decoded using implicit current session/home or counter-only matching.

**I1 handoff:** public boundary lifecycle/client/server envelopes retain full H5 object; encode its entire tuple only at RECOVERY's string ledger/custody/stop seam. All comparisons/readback use full tuple or canonical encoded ref, never only spawnCounter. Decode is allowed only for recognized canonical v1 refs; legacy opaque ref reading does not establish an absent tuple. Stable home is App identity, not credential/path. Local prototype adds generation_ref.py and uses it on scripted actual spawns; run_cases stops parsing slash prefixes and compares complete encoded refs. Example generation fields updated to same encoding, other request identities/facts preserved. No request-custody, observer, close/relaunch, outcome or acknowledgment meaning changes.

**Checks:** offline Python 3 standard library; `python3 -B prototype/check_generation_ref.py`: 324 distinct tuple roundtrips including punctuation/NUL/composed and decomposed Unicode, cross-home/session/counter changes; rejects empty IDs, nonpositive/bool/absent counter, surrogate, malformed UTF-8/hex/noncanonical decimal and legacy counter-only shapes. `python3 -B prototype/run_cases.py`: exit 0, 16/16 results as expected; 58/58 transition rows covered. This includes schema/examples (C-09), custody/unknown/observer/relaunch and multi-home generation checks. These are scripted local evidence, not native product execution or historical tuple qualification.

Consumers: I1 hosting/recovery adapter, DEL-01-04/01-03 native views, EXEC run tags, ADAPTER in-flight/relaunch custody, RS custody reference consumers, and examination owner DEL-09-02. They receive exact representation through named adoption; no outside files edited. No new dependency/download or human checkpoint required; representation clarifies existing accepted tuple promise. Full-generation metadata must stay available on public interfaces even where RECOVERY persists a string reference.

## Sources

| Source | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/ScopeOfWork.md` | `6c62de1d749022a388d9a2c466655a35e06b0b9fa7779a7912f9df4424226a07` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/MEMORY.md` | `844f822e6add30c2492e35e23cf564d0e29396c10951f9f3a69549e32d18aae1` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` | `b01ef84d5fcfd494cbf60c81860c5d0ccd159ccb90598147184b6f8c17475cc5` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/hosting.lifecycle-event.schema.json` | `40d9dc95330f7186ed43d152459a10441c732233403bf49642b87ec67d13cd97` |

## Returned files

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` | `2e05fa1346fde759a53d1f2d932650f23eb93fd0bc23c36172d6b403c744d3b5` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/prototype/generation_ref.py` | `23ff8f64ad43fbee297af86ed36ac98b68aea9bf8eb49de22eef0596b63a5701` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/prototype/check_generation_ref.py` | `0db53012909f0e064a408219833e2484ab14c70154986ffa89b458819d1672bd` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/prototype/recovery_model.py` | `f46bcabfade9fc58bbcd02689636f5764757511dd563278e4d6551284166f63f` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/prototype/run_cases.py` | `0f3fac7316b84ad3f23778c3fa7b6b823750db0f282b53860b523b6906f1872c` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/prototype/README.md` | `700f345f0cadda74158eb9858b3ddc48748b61352676c107961a17f84aa19cf1` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.app-ledger-entry.example.invalid.json` | `48bb3270e7f0d8fd47afdd27dbaddfe547b018f073ec5f6b692365599d30890b` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.app-ledger-entry.example.valid.json` | `4d6c3a735b43bd24cbde4a5ae0143035da269214b1a348cccdce2c29987f74c1` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.custody-event.example.invalid.json` | `6b03270f68bc2bd633a9d1917d7b0230f0d4f1128753e30bdc579f8d233fb77a` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.custody-event.example.valid.json` | `a9b3b1a4a1b21bb898b78b438cb1d93838ef9e3c92cc89816f956b07df47e7f1` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.stop-request.example.invalid.json` | `f8d22fddda9590ce48c26d83133780f148ce8c4de3270bf2eee57b3748a07f85` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.stop-request.example.valid.json` | `d20d17fa3a4f8b118a982c72cc50088f94b81c18521e44a2dc5e02fe21a3340e` |

## Unchanged schemas

| Schema | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.app-ledger-entry.schema.json` | `33a454f83da05364fa65de96b2724c874093d1b318e1752bd7c0092e2be6a2d1` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.custody-event.schema.json` | `033398508abc813e90aee0a074a18cb91bd59be88b6991111504ae5662653773` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.stop-request.schema.json` | `738bad11f825e9976ba9f8f1158b8938bf621c640ceae561c7e26d2899e6c5ef` |
