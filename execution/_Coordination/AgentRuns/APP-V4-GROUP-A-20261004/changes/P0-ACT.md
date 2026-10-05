# P0-ACT — native act, storage and record-ID implementation

2026-10-04; TASK `/root/group_a_execution/act_storage_propagation`, native delegated-harness descendant of WORKING_ITEMS `/root/group_a_execution`. No descendants. Parent supplied bounded brief and independently READY CC-R/A, CC-P-R/A and CC-ID under V0-RX/A/P/ID. Applied chirality-change; no workflow selected. No Git mutation, downloads, credentials, sign-in, network or live Codex execution. Shared schema and hosting code remain their owners' changes; parent owns Node runner/docs and integration.

## Result

Recorder uses the full registered package validator, never the old lean shape admission. Current package scope is copied faithfully into requests; absent/empty scope becomes exactly `not named by the package` only in offer, native text, capture and human act. The reviewed agent-package route records requester kind `agent` without identity and a separate referenced RS requester limit with the exact §13.6 detail. Interrupted request/limit sequencing repairs the missing limit without reissuing the request. Decision view renders unknown requester identity explicitly.

Rust freezes the chosen alternative, complete authoritative offer and observed actor when composing native text; capture refuses differing choice, offer/digest, actor or changed source bytes. Full statement and consequences are presented in the host dialog; script/agent/App-rule sources and dismissed/second captures refuse. Existing Tauri native confirmation remains the only production capture path. No OS presence/password check or verified-identity claim was added.

Capture evidence is create-new and synced before RS append. A create-new durable pending sidecar reserves the original capture facts, record ID and owning relative log before publication; it is recovery state, not a second act record. The original capture initially has no recordId. W-1 remains fail-closed on the complete entry; successful append and verified durability precede the sole atomic, add-once backlink. Backlink failure reports AC-8 with actual durable record and backlink failure; it never returns a fabricated backlink or AC-7. Late/relaunch recovery searches every discovered owning log, matches captureRef plus original record ID/body, preserves all original act facts and retries only a definitely missing append. Partial/invalid/unreadable/duplicate/disagreeing record sets block replay; sync failures remain uncertain until explicit filesystem durability can be re-established. Pending captures block a fresh compose for that request. Refresh/relaunch view displays pending failures and performs bounded reconciliation.

Selected App paths implement RS §13.7: project run/writer and outside-run writer logs, library `.chirality/records/acts.jsonl` API with library-local captures, and explicit original `records/coordination.rs.jsonl` discovery. Legacy bytes and opaque IDs remain in place; nothing is copied or reissued. SHA-256 opaque path keys map identity strings separately; symlink-containing owning paths refuse visibly. Run append API retains actual runId and creates no duplicate outside-run index. No silent relocation occurs. Library API/storage reopen is exercised; actual A15 implementation remains later work.

New record IDs are fallible OS-entropy UUIDv4 `rec:app:<uuid>`. Reserved ID survives late write. Detected cross-log conflict refuses, historical IDs remain opaque. A filesystem advisory ownership lock serializes append/seq/conflict checking within each owning records root, including independent processes opening that root; successful append takes the next writer-log sequence. Readers report malformed/unreadable/unterminated records as limits. No W-0 repair or generic persistence service was added.

Maintained FX-DP1 bytes now live under `app/tests/fixtures/FX-DP1`; originals are unchanged. Test assertions retain reference content, authoritative semantics, actor/recorder distinction, refusals, lapse and no-write view checks. Minted IDs, boundSubject/requestRef and separate requester limits use explicit current invariants instead of comparing new random IDs to old fixture counters.

## Validation

All commands offline with `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home` and `--locked`. Final full suite: `env -u CHIRALITY_CODEX_BIN CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml`: 8 lib + 11 act_storage + 3 decide_flow + 3 hosting_contract + 6 schema_validation pass; handshake test explicitly returns skipped with no supplier process; main/doc tests empty. `npm run build` in app: TypeScript and Vite pass. Subsequent exact requester-detail correction was rechecked: 8 lib, 11 act_storage, 3 decide_flow and 6 schema_validation pass. Final added duplicate/disagreement regression brought act_storage to 12/12 passing; only this test file changed after the source checks. Shared helper dead-code warnings are informational.

Meaningful filesystem cases: capture target refusal/no relocation; torn owning log then relaunch/late retry with stable ID and original facts; crash-after-append fixture then backlink-only repair; actual directory-permission backlink failure then recovery without append; foreign partial log blocks all replay/backlink; duplicate and disagreeing discovered capture records block replay/backlink; full-shape malformed packages; duplicate alternatives; frozen choice/digest/script/cancel refusals; exact optional-scope behavior; legacy preservation; portable library reopen; run/outside-run separation; 8 concurrent appenders × 8 records give unique sequential entries; separate same-seq logs get distinct IDs; injected collision refuses without bytes change; injected entropy failure through the writer path creates no log/seq.

Cargo manifest adds only exact cached uuid1.23.1 and getrandom0.4.2. Parent authorized root-dependency lock admission. Offline generate-lockfile attempted unrelated resolver movement, was rejected/restored, then only the two root dependency edges were admitted. Before/after package/version/checksum sets and every other package object match the pre-lane lock; no archive was acquired. Existing parent CI9 changes remain untouched.

## Limits and integration needs

Independent product review still required at these bytes. Tests are synthetic filesystem/state-machine witnesses, not proof a person used the native dialog or native authenticity/custody qualification. The crash fixture simulates the durable append/backlink boundary; actual process kill and OS fsync-error injection have not been witnessed. Advisory locks cover cooperating App writers on the selected local filesystem; they do not qualify network filesystems or protect against unrelated tools deliberately rewriting evidence. UUID collision resistance is probabilistic and conflict checks cover the discovered owning roots, not every offline/unattached project. Storage mappings/library API do not claim actual A15 implementation, SWBPIPE joins, common service allocation, global OI closure, human acceptance or release. Parent Node/schema export integration must adopt five output lines: two requests, two referenced limits, one human act.

## Supplied origins and hashes

Root was supplied by the human; TASK role and chirality-change were read from the paths below. LOOP_INIT, manual current-edition index, manual headings, full Field Book and owner decisions were consulted. App README was read as shared mutable implementation context; parent documentation remains unfrozen and owned separately. Hashes below identify the stable sources observed at return, not a new acceptance.

| Origin | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `.agents/skills/chirality-change/SKILL.md` | `1a2b056263ec77e4104efdf99afe3fe76dda792334a243fb2f21c60bc9c81450` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28` |
| `docs/alignment-manual/README.md` | `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/OWNER_DECISIONS.md` | `57e9412cbbc84862c2658a573ed9390a333ace8400c22bd6a81c8ce0eb77535a` |

## Review candidate

Shared lib/Cargo files include pre-existing W-1/schema-owner contributions; the lane preserves those gates. Source HEAD is `cb5a88b29ac10fc0c09f9b6a44f497ab917e8a71`; candidate includes working changes, not a commit or acceptance. Exact output bytes:

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` | `5a1de69dd988adc23bb3f4aaa06a76ef357062bd72e6fcbc4ad0f64f0661c5c3` |
| `projects/chirality-app-v4/app/src-tauri/src/recorder.rs` | `162c03a488a184ddd3982059fe3c7cad11791cdb92e3f2daaef12ff8a01406c5` |
| `projects/chirality-app-v4/app/src-tauri/src/records.rs` | `72ef071a92533986e1a7221ab2693839cdc5d4796682fd19eb9288b1ca7014ca` |
| `projects/chirality-app-v4/app/src-tauri/src/decision_view.rs` | `636798c6b36e6a3295fb4b55b7c7ee9a11c3dce520b5e9bae241f12d3f41f4f4` |
| `projects/chirality-app-v4/app/src-tauri/src/storage.rs` | `a5314b4acb64a52fd338a293a9e2b973cb213b921ced4597c121d4d9f4064197` |
| `projects/chirality-app-v4/app/src-tauri/src/util.rs` | `50cfa90c75e4cb7b52de76e99313a266290f818b8e8456817b69188e10626b22` |
| `projects/chirality-app-v4/app/src-tauri/src/lib.rs` | `295d27635a581ccd893dd47807f90ff3a043655b902dfdb988553b5144fbc5a5` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.toml` | `2d89ee516e013d3e8990c15a2eaeebb1ce08588934a26193bfb93b604e4f7d31` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.lock` | `2fad2d658b3ffaf7b3973d5ab7da693788613f7462eaeca9d4b6b9ad826f7012` |
| `projects/chirality-app-v4/app/src-tauri/tests/decide_flow.rs` | `174d4acfb9c2ebcb84600344f2f1855bbd456a0d3fa213bc1682b3509e60e247` |
| `projects/chirality-app-v4/app/src-tauri/tests/act_storage.rs` | `4c8770dd161bd67bd017115a46a4c9ff2860543ba7bf6c86745644583531876b` |
| `projects/chirality-app-v4/app/src/App.tsx` | `dd546b4cb38cb1c24f321bbbb12bbb033777bd58b5d6ecec272f66300671a408` |
