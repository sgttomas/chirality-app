# I1 OAuth Root receiving draft — 2026-10-05

TASK `/root/group_a_execution/access_consumer_resume`, parent WORKING_ITEMS `/root/group_a_execution`; delegated-harness-native, no descendants. Source preparation only while parent uses an immutable UI bundle and Core repairs OH1. Sole live write is this plan. No live lib/runtime/App apply, Cargo/build/test/native UI/browser/account/auth/model/real-home/credential/network/download/Git operation. Earlier access15/frontend/native-source records remain their own candidates.

Private draft at `/private/tmp/chirality-oauth-root-draft-9ntPmS`: `basis/` and `edited/` retain exact three owned source files; `oauth-root.patch` applies relative to `projects/chirality-app-v4`. Actual live three-file comparison still equals every basis byte. This patch is **unapplied, uncompiled, untested and unreviewed**; ready as a concrete source preparation for coordinated compile/review, not product READY or native qualification.

## API fit and actual draft

No new Core API is required for this bounded adapter. Actual source APIs are crate-private `NativeLoginMode`, `OAuthLogin`, `NativeLoginView<'_>`, `NativeLoginLease`, `NativeLoginPresentation`, `account_oauth_start/observation/present/cancel` and `OAuthLogin.source()`. The current Host-issued wrapper retains original fullG/typedRPC/reference; Root never builds one from a public pointer or reconstructs native loginId. `HomeSession` retains one private Arc wrapper plus a start-only gate; no payload clone, schema/store/ledger/auth copy or secret-bearing browser DTO. Start gate ends before reply wait/presentation and never serializes Cancel/Stop through native display. Core remains one-at-a-time/current-source/final-dispatch authority; pure controller shape is not native policy, source authenticity or person identity.

Draft commands route supplied fullG to its original HomeSession. Browser/device start is Account-only, requires a native confirmation, reads genuine same-source policy and stores the actual issued wrapper before waiting. A timeout/error retains original pending/unknown control, never restarts/retries/replaces it. Safe `homeOAuth` status reads only Host observation; matching completion remains separate from native account/read confirmation. Existing explicit account-read control supplies that confirmation; this adapter does not infer signed-in identity from controller success or silently implement the broader AE/AR account state machine.

Presentation captures the original private wrapper. Core gives its one-use borrowed view outside Host/controller/pipe locks; macOS adapter synchronously dispatches its borrowed stack context to the native main queue (or calls directly when already main), never enqueues a detached/'static Rust secret clone. It rechecks lease and exact current Host generation/ready status at native delivery. Browser authUrl is passed once via native NSURL/NSWorkspace to the person's system browser, then App material is released. CR3 does not supply browser-tab reclaim or OS/browser erasure, and none is claimed. Device verification URL/code are copied only into the bounded native NSAlert display; an AppKit modal-session polling loop checks lease/current source, ends its own session and clears/hides its own window on revocation/dismissal. Callback return feeds Core dismissal while retaining live pending cancellation. Other platforms return truthful unavailable. No callback or modal session was invoked.

Cancel captures original Arc before native confirmation, holds no HomeSession/Host lock through that confirmation, then compares original wrapper association and calls `account_oauth_cancel(original)`. Core owns final same-source dispatch/private loginId serialization; no current-source retarget. Public safe statuses distinguish actual `canceled` and `notFound` ("Codex had no pending sign-in") from error/unknown/unavailable; dismissal/source loss never invents signed-out/cancel/native termination. UI supplies only mode/fullG intents; URLs/codes/native ID never cross IPC/journal/diagnostics. The explicit native confirmation/callback path is source code, not proof of authentic NativeUser or successful native act.

## Source/native checks and remaining execution

Rustfmt syntax parsing only, `--edition 2021 --emit stdout --config skip_children=true`, succeeded for both scratch Rust sources; formatted parse outputs retained separately, draft formatting unchanged. Local TypeScript `transpileModule` TSX syntax diagnostics: PASS; no typecheck/build/render/native invocation. No Git apply check was run; exact basis/live equality and generated unified diff are source recovery evidence.

Read current Host wrapper/private callback and source gates, actual repaired a78a/461 projection association, controller custody/view/lease/delivery/cancel interface and pure review, adopted ACCESS CR2/CR3/Q2–4/AE/AR/§7.1 and HOST §5.1/§9.1 privacy. Historical V3 OH1 blocker/original inverse controls and pure READY are preserved; parent separately reports actual OH1 author checks and source backcheck, not this adapter's proof. Installed SDK read confirms NSWorkspace.openURL, NSAlert.window, NSApplication.modalWindow/beginModalSessionForWindow/runModalSession/endModalSession and Continue=-1002. SDK libdispatch main queue is the exported `_dispatch_main_q` address (dispatch_get_main_queue is C inline); scratch uses that exact symbol plus dispatch_sync_f. No SDK install/download/native call.

Next boundary: manager coordinates exact Core/shared freeze, applies reviewed scratch delta, then actual Rust/frontend checks and independent Root/native/privacy/source review. Synthetic tests must retain original wrapper across source/home switches, policy exclusion, delayed/failed reply, pre-presentation terminal/source loss, device lease revocation and dismissal retaining cancel, original confirmation race/one cancel attempt, actual canceled/notFound/unknown distinctions, zero raw canaries in public serialization. Native AppKit/modal/button/main-queue ABI and device-window liveness/dismissal are **unverified** until permitted platform examination; source declarations alone prove none of these. No new framework, synthetic authority DTO or workaround native exposure is proposed. Actual auth/browser/native qualification stays parent/owner-controlled.

## Exact draft association

| Owned file | Basis SHA-256 | Prepared SHA-256 |
|---|---|---|
| `app/src-tauri/src/lib.rs` | `09d654a1f5220cc451bf5b536876b5513289cf8b3296cd49c6ad6ec9e7897730` | `57b90e58fd74aeb65b82eb4284c2f154a51701c5d996a1ac181dd609bdcc4768` |
| `app/src-tauri/src/runtime_session.rs` | `5cfeb3ffaa6f75374495c1e8ef1b1f1ffd283924e5a8bf7f2bcf0047883138bd` | `afba1e0310ab50377c9f4c6667dc53ceaef98be909b49b3e2e668843103e781c` |
| `app/src/App.tsx` | `021571c21c72a47c2a4d15d37e8bdd73d4ceb213cd7de235c5da0110ace99b7a` | `28a83a3485d9f4f437dc0cceb907475a3855c343b3f32fc67fa731a87733a489` |

Patch SHA-256 `3b977c303332ffc43f2553c22426733fd50d202e8e3258dbad85bc910e7de931`. Current inspected Core source copies are `inspected-hosting.rs`, `inspected-auth_rpc.rs`, `inspected-oauth_control.rs` in the scratch root, keeping association recoverable during subsequent owner writes.

| Read source/origin | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-ACCESS-OAUTH-CONTROL-CUSTODY.md` | `8efa4401058a74d03cd57177699e463798cff5e78d123e7b8d5f6a7642fb36a4` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-OAUTH-HOST-RECEIVING-PLAN.md` | `b40811bc11a70c9e0e13df39ef2883e2ffbe70f0cd44477ad479bf83bfa0050d` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-OAUTH-HOST-RECEIVING.md` | `eaacc2b2e7cea5ee082d5e739bf2630087f3054d05a9e9d8632317f87fdf1d1c` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V1-I1-OAUTH-CONTROL.md` | `698002f32ed79d94fca99a67c9ea3a8fc3e4df51aefe4edcabb1c07f8655a975` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V3-I1-OAUTH-HOST-RECEIVING.md` | `0b9da9c0a673494d670dd280355265f6528b1d9036f9b3280e9e2e14ca21ca86` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_AND_PROVIDER_ACCESS.md` | `26659864fd1b720d51bc5bf8038311238e9d6b1775f62a4e08fd2917dba4f9ec` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` | `9839cb38310ff55045657e51f7bb7dcfcb2024eb43ec3bab364959e33e5c1e85` |
| `/private/tmp/chirality-oauth-root-draft-9ntPmS/inspected-hosting.rs` | `a78a2a7206434e44b1946139098521d678a07057cc8fd8fd1da329afa31ef263` |
| `/private/tmp/chirality-oauth-root-draft-9ntPmS/inspected-auth_rpc.rs` | `461166dcc28b621a80c23b75cef939951d6794620db1b4bc89acf3efcd58306d` |
| `/private/tmp/chirality-oauth-root-draft-9ntPmS/inspected-oauth_control.rs` | `8096834b5eb9d73f140f585a01bd55535d4d7ec682220ca145daeecddf283060` |

## Actual receiving successor after released Core/privacy review

2026-10-05. Parent explicitly released private patch3b977c30 after Core independent READYdabb7e40 on Hosta78a/auth461. HEAD `fc8c2eb1b6ae7e1c5ae21aa172efb3449248a18b` verified. Actual three shared baseline pins09d/5cf/0215 and patch hash verified; current private wrapper/view/lease APIs and V3 exact successor READY read. `git apply --check --directory=projects/chirality-app-v4` exit0 followed one atomic apply exit0. Prepared lib57b90/runtimeafba1/App28a83 hashes matched immediately afterward. Historical scratch draft remains its own unapplied/uncompiled boundary; this is the later actual adoption.

Live owning runtime now factors `present_original_native_oauth(home, original, callback)`: production native wrapper and contained cfg(test) injection call the same genuine Host-issued wrapper/one-use view/lease path. No public factory/DTO/native authority or callback qualification inferred. Seven connected contained `oauth_root_` tests use an owned scratch Python frame peer whose version label is fabricated solely for explicitly `unverified-development` Host start and initialize result is `unqualified-root-owned-fixture`. Genuine Host policy/start/cancel wrappers and actual native notification admission are exercised; no stock supplier/native UI/browser/model/provider/credential/account call. Synthetic canaries appear only in designated own wire/private callback values, not Root/Host/account public serialized observations.

Actual tested controls: browser one-use and original private-ID cancel; device dismissal/null account-read preserving actual notFound cancel; real lease revocation from a matched emitted completion outside Host lock; null-ID event preserving pending then pre-delivery terminal suppressing callback; native confirmation dismissal/source Stop preventing cancel dispatch; actual HomeRouter account→key switch using same actual App custody plus foreign-wrapper refusal with zero foreign cancel; native-start dismissal/real source policy exclusion/uncertain native cancel error without retry. Every fixture invokes actual own Host Stop and removes own scratch root; no actual native display function executes.

First exact `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --lib oauth_root_`: **PASS7 exit0**, compile3.68s/run1.60s, on runtime48aac/lib57b90/App28a83/Corea78a/auth461/controller809683. Five warnings retain unused explicit Core dismiss and existing NativeHistory seam; no warning suppression or first compile/test failure. Cargo released immediately. Frontend TypeScript/Vite30 build PASS366ms on exact App28a83; WS-disabled safe OAuth HomeAccessPanel static render PASS `/private/tmp/chirality-oauth-root-live-render.html`, no action callback. These are code/test/render evidence only, not actual native queue/modal/browser behavior.

Source-only follow-up identified before first grant crossed: synchronous worker→main queue `Context.current` should require `Fn()->bool + Sync`, making the actual shared HomeSession-capturing source check's thread safety explicit. Runtime48aac remains the actual first pass; type-bound tightening and affected final replay await manager disposition. Native OS/main queue/modal/button/user-act behavior stays source-only until parent's authorized examination. No first7 result silently becomes a later source pass.

## Final author candidate and exact affected replay

Parent authorized the narrow native thread-safety tightening. Saved actual first-pass runtime48aac at `/private/tmp/chirality-oauth-root-sync-before-g5Lt8i/runtime_session.rs` before any edit; hash matched. Only native adapter/current Context/nonmac signature changed to `Fn()->bool + Sync`; the compiler checks the actual shared HomeSession-capturing closure, with no unsafe bypass/test shortcut. Final runtimefe0c source remains a successor of first48aac, not rebound to its initial7 pass.

Actual first final command `cargo test --offline --locked --lib oauth_root_ --test access_integration --test recovery_startup`: exit0, compile6.83s, **Root7 PASS** run1.21s. Cargo's global positional filter also applied to the integration binaries: actual access0 with9 filtered, startup0 with6 filtered. Those zero executions are **not** fifteen passing controls. No code/test failure inferred; invocation selection corrected while stationary source and already granted lane remained unchanged.

Actual separate unfiltered `cargo test --offline --locked --test access_integration --test recovery_startup`: exit0, compile0.15s, **access9/startup6 PASS**, run0.71s/0.04s. Together **22 distinct affected PASS** on exact final source. Source/Core/controller stayed stationary across both commands. All used approved isolated CARGO_HOME, CHIRALITY_SKIP_CODEX=1 and offline/locked. Cargo released immediately before source sealing/record work. Retained unused explicit dismiss and NativeHistory warnings only; no first or final Rust compile/test failure. Earlier scratch syntax/intermediate7/filter-zero associations remain historical and explicit.

Final exact review source copies: `/private/tmp/chirality-oauth-root-final-iyjrup/` with original relative paths. Source hashes after final checks match the actual pre-run pins. Final three-owned-source `git diff --check` exit0. No source edit after final pass. Parent must commission independent native adapter/Root source/current-wrapper/privacy/routing review before fan-in; author has not self-certified READY or native qualification. Core/privacy READYdabb7e40 remains separately attributed; unchanged namespace/sole-ledger/access controls now passed at this actual receiving revision.

| Final tested input | SHA-256 |
|---|---|
| `app/src-tauri/src/lib.rs` | `57b90e58fd74aeb65b82eb4284c2f154a51701c5d996a1ac181dd609bdcc4768` |
| `app/src-tauri/src/runtime_session.rs` | `fe0c5faf3c21e8443ae948be78b445551a44d20513393782b23048d2f9c2eefb` |
| `app/src/App.tsx` | `28a83a3485d9f4f437dc0cceb907475a3855c343b3f32fc67fa731a87733a489` |
| `app/src-tauri/src/hosting.rs` | `a78a2a7206434e44b1946139098521d678a07057cc8fd8fd1da329afa31ef263` |
| `app/src-tauri/src/auth_rpc.rs` | `461166dcc28b621a80c23b75cef939951d6794620db1b4bc89acf3efcd58306d` |
| `app/src-tauri/src/oauth_control.rs` | `8096834b5eb9d73f140f585a01bd55535d4d7ec682220ca145daeecddf283060` |
| `app/src-tauri/src/recovery.rs` | `f0fff309d2f8eec23046b5349e4969308ef26319a4e5b6eedf46b3c4da50bc31` |
| `app/src-tauri/src/attachment_custody.rs` | `04f82cbd64fe5a9c40b57556a804c063740019d584f0cf68aeab9172a2d58082` |
| `app/src-tauri/src/home_resources.rs` | `5d55a03511acf04609456f647589f82e2456bc9caeaf0d35b5880515e7f6a5f9` |
| `app/src-tauri/tests/access_integration.rs` | `e74701f913ad2d2e1a6bcec2c5e2d0a04a2e9dd80487cd30561018e42803ac8f` |
| `app/src-tauri/tests/recovery_startup.rs` | `778562fa9f550014753e6b31b91e05eae2c1b8925ac007fcb3f7a3a100b69a78` |

Actual native browser/NSURL/NSWorkspace dispatch, main-queue interoperability, NSAlert/modal-session/button/field clearing and OS/browser lifecycle were never invoked; static native type compilation and injected revocation callbacks do not witness those behaviors or physical erasure/person origin. Their source contracts are reviewable and actual platform examination remains parent/owner-controlled. No real native supplier/auth/credential/account/model/provider/network operation or dependency download occurred. No OAuth hosted-route authority, matching real account/signed-in validity, complete AE/AR event reconciliation, native-guidance/discovery qualification or whole Group A closure inferred. This bounded author receiving contribution and warranted synthetic checks are complete; exact source is frozen for independent review/repair.

## OR-1 reopened receiving warrant and original execution

Independent reviewer `reviews/V3-I1-OAUTH-ROOT-CONSUMING.md` SHA `fe22a0232697bf60d18c0de6f64ed9930380690dbdb8d0eb25353638370f047e` is NOT READY for original control retarget. First22/native-source/frontend claims above retain their tested scope; they did not cover stale same-home successor commands or same-G automatic-presentation replacement. No readiness inferred.

Actual lib57b90/runtimefe0c/App28a83 preimages were verified/copied to `/private/tmp/chirality-or1-original-4Bm0eh/preimage/`. Parent explicitly permitted a behavior-preserving native callback and automatic-continuation extraction for original proof: original latest-slot behavior and omitted requested-generation fence stayed unchanged. Actual libf03ed/runtime d44839 source/test copies saved at `extracted-failing/` in that scratch root. This original execution is associated with those extracted bytes, not falsely labelled byte-identical fe0c.

Original `--lib oauth_root_or1_`: **exit101, 0 PASS / 3 FAIL**, compile1.96s/run0.96s. Actual same-App-session/same-home restart increased spawnCounter and genuine matched completion permitted new pending control. Stale presentation callback count1 versus required0; stale cancel native-confirmation count1 versus required0; original start auto continuation after genuine terminal/same-G replacement callback count1 versus required0. Governing zero-replacement-effect criteria were retained before repair; no Core/native/auth operation or broad suite occurred. Cargo released immediately on result. This is executed Root receiving reproduction, separate from original review's source-confirmed status.

Minimal owning repair carries a private `NativeOAuthStart` with the actual issued Arc through wait and automatic delivery, with no JSON/Serde/Debug constructor. Explicit helpers receive requested fullG and validate it against captured wrapper plus current ready source, then preserve exact captured Arc through native interaction/final Core dispatch. Automatic delivery validates original operation association and never selects a later slot; safe start/result observations also use the issued original source. Historical HomeRouter lookup remains unchanged for history/retained-generation consumers. Core remains final one-use/pending/cancel/write/source authority.

Separate source-fit comparison followed the existing key-entry/logout pre/post metadata pattern: an actual optional HomeBootstrapSet is carried from AppState into helpers, revalidated before/after native confirmation/policy wait, and checked by the pending display's current-source callback. Metadata checks address current intended Account/Probe relationships; absent descriptors preserve existing explicit account-source limits rather than invent a default/native startup veto. They do not establish hostile filesystem atomicity, future discovery/config writes, credential legitimacy or native window clearing. Three meaningful synthetic metadata controls added: start confirmation drift blocks policy/login, cancel confirmation drift sends no RPC and preserves control until restored inverse, active display checker sees physical drift independently of still-active Core lease and reports unavailable. No physical-home source contract changed.

Coherent repair candidate lib5707a056/runtimee75f4457/App28a83, with original3 assertions retained plus valid successor/same-G new-operation inverses and physical3, requested for targeted Root13 and access9/startup6. Not yet a successor pass or independent reviewer verdict.

## OR-1 exact repaired author return

Actual focused `--lib oauth_root_` on lib5707/runtimee75f/App28a83/Corea78a461: **PASS13 exit0**, compile2.02s/run1.99s. Original3 zero replacement effects and valid successor/operation inverses passed; metadata3 passed; prior7 source/privacy/lease/cancel controls retained. Actual separate unfiltered `--test access_integration --test recovery_startup`: **PASS15 exit0**, compile4.11s/run0.76s/0.07s. **28 distinct affected PASS**; original0/3 failure and prior22 are not aggregated/rebound. No repaired compile/test failure or criterion weakening. All used approved isolated CARGO_HOME/CHIRALITY_SKIP_CODEX/offline/locked with actual stationary shared/Core compile inputs. Cargo released immediately; I2 catalog's later disjoint lane is not this source's evidence.

Final actual source archive `/private/tmp/chirality-or1-repaired-bKffPe` retains original relative paths. Post-run hashes match tested pins; no source edits after28. App28a83 remains its prior exact frontend build/render source; no frontend source changed for OR1. Same original reviewer is completing exact source/preservation/original-criterion backcheck; no author self-independent READY/native qualification claim. Actual OS/browser/modal/field behavior remains uninvoked/source-only, metadata checks non-atomic, and broader account/AE/AR/native/supplier/hosted-route qualifications retain existing owners/limits.

| OR-1 final tested source | SHA-256 |
|---|---|
| `app/src-tauri/src/lib.rs` | `5707a056e3e331c6d40c123a687c03b72c960b5d77d4887fa386760e355bb3ab` |
| `app/src-tauri/src/runtime_session.rs` | `e75f4457be8efb8f0e332b86c5e72b81b4ffced0fca7e4a4095f68cc1aec4d3a` |
| `app/src/App.tsx` | `28a83a3485d9f4f437dc0cceb907475a3855c343b3f32fc67fa731a87733a489` |
| `app/src-tauri/src/hosting.rs` | `a78a2a7206434e44b1946139098521d678a07057cc8fd8fd1da329afa31ef263` |
| `app/src-tauri/src/auth_rpc.rs` | `461166dcc28b621a80c23b75cef939951d6794620db1b4bc89acf3efcd58306d` |
| `app/src-tauri/src/oauth_control.rs` | `8096834b5eb9d73f140f585a01bd55535d4d7ec682220ca145daeecddf283060` |
| `app/src-tauri/src/recovery.rs` | `f0fff309d2f8eec23046b5349e4969308ef26319a4e5b6eedf46b3c4da50bc31` |
| `app/src-tauri/src/attachment_custody.rs` | `04f82cbd64fe5a9c40b57556a804c063740019d584f0cf68aeab9172a2d58082` |
| `app/src-tauri/src/home_resources.rs` | `5d55a03511acf04609456f647589f82e2456bc9caeaf0d35b5880515e7f6a5f9` |
| `app/src-tauri/tests/access_integration.rs` | `e74701f913ad2d2e1a6bcec2c5e2d0a04a2e9dd80487cd30561018e42803ac8f` |
| `app/src-tauri/tests/recovery_startup.rs` | `778562fa9f550014753e6b31b91e05eae2c1b8925ac007fcb3f7a3a100b69a78` |
