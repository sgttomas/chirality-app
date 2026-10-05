# Independent Root OAuth consuming review — 2026-10-05

**NOT READY: OR-1 is a blocking, source-confirmed original-control retarget defect.** The seven injected Root checks and access9/startup6 passes do not cover the command-level same-home stale-generation and automatic-presentation replacement cases below. Actual native UI/auth/credential qualification remains separate.

TASK `/root/group_a_execution/access_consuming_review_resume`, parent WORKING_ITEMS `/root/group_a_execution`; same replacement reviewer as V2, native delegated harness, no descendants. Applied software-code-review against previously reviewed lib09d654/runtime5cfeb/App021571 and frozen OAuth consumer57b90/fe0c/28a83. Read updated LOOP entry. Only this review written; no code/Design/schema/instructions, Cargo/native UI/browser/auth/model/credential/real-home/Git/network/download operation. No executing reproduction is claimed. Concrete source finding returned to manager promptly.

## OR-1 — Blocking: preserve the requested/issued original control through Root admission and auto-presentation

Locations: `app/src-tauri/src/lib.rs:202–211` (`oauth_present`/`oauth_cancel`), `lib.rs:195–197` (automatic presentation after start), and `runtime_session.rs:2704–2732`, `2751–2780` (issued wrapper storage, latest-slot observation, latest-slot selection).

`HomeRouter::for_generation` at runtime_session.rs2108–2128 deliberately locates an owning HomeSession by native home and App session; it does not require spawnCounter equality because retained-generation history/read routes need that owner. Its comment explicitly leaves stale operational admission to Host. Both new explicit presentation/cancel commands pass the requested full generation only into this router, then discard it. The runtime functions subsequently select the latest `home.oauth_login` Arc. Core checks the source bound to that selected latest wrapper and has no copy of the discarded caller generation.

Concrete trigger: account Host G1 stops, restarts under the same genuine App session/home as G2, and starts a new pending sign-in with a G2 wrapper. A stale renderer `oauth_present(G1)` routes to the same HomeSession, selects the G2 wrapper and can deliver its native view; `oauth_cancel(G1)` can show confirmation for and cancel G2. Actual current G2 Core gates pass, since Core receives G2's genuine wrapper. The wrapper pointer comparison after native confirmation protects only against another change after selection; it does not bind that selection to requested G1. Thus a valid private capability is retargeted by Root, rather than a public pointer directly constructing authority. Cross-home refusal and Stop tests do not cover same-home/same-session successor counters.

A related same-generation race exists in the start command. `start_native_oauth` issues/stores a particular login, drops its start-only gate before waiting, then returns `native_oauth_observation(home)` from the latest slot. `oauth_start` subsequently calls `present_native_oauth(home)`, again selecting latest slot. If the issued operation terminates and another allowed same-G sign-in starts before the first waiter resumes, the first native start act can automatically present the replacement wrapper/mode. Full-generation equality alone will not repair that same-G race. This is possible after genuine matched completion/cancel, without bypassing Core's one-pending-operation rule. The original issued receipt remains privately retained, but the consumer does not use it for automatic delivery.

Impact: stale or superseded source intents can present/cancel a different original native sign-in. This contradicts the adopted ACCESS §7.1 original full H5/typed RPC/mode custody, source-bound native presentation/person cancellation, and the author plan's no current-source retarget interface. It also contradicts the new functions' own original-control captions. No real sign-in exposure/cancellation is claimed; the defect is demonstrated by the deterministic source data flow.

Repair direction: at explicit presentation/cancel admission, require requested full generation to equal the captured wrapper source generation and the current ready source; retain that exact captured private wrapper across confirmation and delivery, never reselect after a wait. Keep the issued wrapper private through start's observation/automatic presentation so that the original start's return cannot consume a later slot. Preserve Core's final original-wrapper gates, one-use lease, one-attempt cancel/unknown behavior, and source loss checks. A public observation pointer or Boolean must not become control authority. Do not globally tighten HomeRouter's retained history routing merely to mask this consumer bug.

Meaningful controls needed: a genuine same-home/same-App-session restart with old G1 request and current G2 pending wrapper must refuse before native presentation/confirmation/cancel, with zero replacement dispatch and unchanged G2 control; repeat valid G2 delivery/cancel as inverse. Also terminate the original start and issue a distinct same-G replacement before its old continuation; its automatic presentation must not deliver that replacement. Use the actual production receiving seam/retained private wrapper and synthetic native callback/wire only. Preserve the current privacy canary and one-use/dismissal/cancel source oracles. No native/auth operation or broad suite is necessary to establish this bounded repair.

## Other inspected source and limits

Native consumer secrets remain in private Rust views/leases and source-issued wrappers. Safe homeOAuth status, IPC inputs, diagnostics and static UI carry only mode/full generation and redacted observations, not native loginId/URL/code or JSON control constructors. Requirements come from actual same-source policy; native start dismissal sends no policy/login request. Genuine Core current-source/wrapper/final pipe admission remains independently reviewed at Hosta78a/auth461/controller809683; OR-1 is in Root's selection/continuation, not an allegation that Core allows foreign wrappers.

The macOS source synchronously dispatches the borrowed stack context to exported libdispatch main queue, with an already-main branch to avoid self dispatch. Current-source callback has an explicit Sync bound. Native view is not cloned into detached/static work. Browser mode performs one NSURL/NSWorkspace OS dispatch and releases App NSString material; system-browser custody is outside App reclaim/erasure. Device mode uses an App-owned NSAlert modal session, periodically tests lease/current Host source, ends its session and clears/hides its window on callback exit. Dismissal retains live private cancellation. No Host/pipe/controller lock spans native presentation/confirmation. Local primary SDK headers independently confirm the used NSWorkspace openURL, NSApplication modal-session selectors and Continue=-1002, dispatch_sync_f and exported main queue address; these declarations and compile evidence do not prove actual AppKit/modal/button/main-queue behavior or clearing/OS erasure.

Root physical descriptor validation currently occurs before each command; native callback checks Host source/lease and cancellation rechecks wrapper/Core source after confirmation. These are different checks. I informed manager of the separate pre/post physical-binding question for receiving follow-up; I do not inflate acknowledged non-atomic filesystem limits into a second confirmed defect without an exact governing requirement. OR-1 alone blocks this candidate.

Previous namespace/key/logout/ROLE/Stop/sole-ledger source remains unchanged except the private OAuth slots and safe source status integration. This review retains V2's bounded warrant and native witness limitations; no former whole ACCESS readiness is invented.

## Actual examined candidate and evidence

Independently hashed every listed live file and compared it byte-for-byte with `/private/tmp/chirality-oauth-root-final-iyjrup`. All match.

| Repository file | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/lib.rs` | `57b90e58fd74aeb65b82eb4284c2f154a51701c5d996a1ac181dd609bdcc4768` |
| `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` | `fe0c5faf3c21e8443ae948be78b445551a44d20513393782b23048d2f9c2eefb` |
| `projects/chirality-app-v4/app/src/App.tsx` | `28a83a3485d9f4f437dc0cceb907475a3855c343b3f32fc67fa731a87733a489` |
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `a78a2a7206434e44b1946139098521d678a07057cc8fd8fd1da329afa31ef263` |
| `projects/chirality-app-v4/app/src-tauri/src/auth_rpc.rs` | `461166dcc28b621a80c23b75cef939951d6794620db1b4bc89acf3efcd58306d` |
| `projects/chirality-app-v4/app/src-tauri/src/oauth_control.rs` | `8096834b5eb9d73f140f585a01bd55535d4d7ec682220ca145daeecddf283060` |
| `projects/chirality-app-v4/app/src-tauri/tests/access_integration.rs` | `e74701f913ad2d2e1a6bcec2c5e2d0a04a2e9dd80487cd30561018e42803ac8f` |
| `projects/chirality-app-v4/app/src-tauri/tests/recovery_startup.rs` | `778562fa9f550014753e6b31b91e05eae2c1b8925ac007fcb3f7a3a100b69a78` |

Read exact final author return I1-OAUTH-ROOT-RECEIVING-PLAN at d51a825238bfa784b067cd2a56c1be53cc626ee520d30d536fd3704869501179. Actual author final Root7 PASS plus separately unfiltered access9/startup6 PASS establish22 distinct checks on57b90/fe0c/28a83. The accidentally globally filtered integration0/9 +0/6 is recorded as zero executed, not fifteen passes. First runtime48aac7 pass remains its prior source; later Sync tightening is qualified by actual final replay. Frontend TypeScript/Vite/static safe OAuth panel render applies to exact28a83; no action/native callback ran. Existing NativeHistory/explicit-dismiss warnings remain disclosed. Reviewer did not repeat Cargo or borrow author executions as independent tests.

Inspected all seven injected tests: actual private browser one-use/original-ID cancel; device dismissal/null account preserving notFound cancel; matched source completion revoking lease outside Host lock; null/unmatched terminal suppression; confirmation dismissal and source Stop refusing cancel; cross-home genuine custody switch with foreign-wrapper refusal; native-start dismissal/policy exclusion/cancel-error no retry. Each creates an explicitly unqualified owned synthetic peer and stops/reaps it. Tests manually pass a captured wrapper to injection or invoke runtime helpers without a requested generation; therefore they do not establish command-level source-intent association in OR-1.

## Supplied context custody and return

Root/TASK/software-code-review and manual/Field Book origins from V2 retained; updated LOOP read now, along with current author plan, adopted OAuth custody, Core receiving successor review, current source/private interfaces and local primary SDK headers. No different role/workflow activated. Manager owns updated graph/cross-group reconciliation and any native or Cargo reservation.

| Actual origin | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `.agents/skills/software-code-review/SKILL.md` | `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-OAUTH-ROOT-RECEIVING-PLAN.md` | `d51a825238bfa784b067cd2a56c1be53cc626ee520d30d536fd3704869501179` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-ACCESS-OAUTH-CONTROL-CUSTODY.md` | `8efa4401058a74d03cd57177699e463798cff5e78d123e7b8d5f6a7642fb36a4` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V3-I1-OAUTH-HOST-RECEIVING.md` | `dabb7e40e89fe74a15657d3a5d8f5129076bbc3b1393a2d440816ccc9ba82c27` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V2-I1-ACCESS-CONSUMING.md` | `78b685849d37b18a3291dbd4585b96b789343ea30acaf12efb59aa19e82ce7a0` |

Return OR-1 for bounded source-faithful repair and exact successor backcheck. Other unchanged contributions remain usable within their own READY scope. No extra human gate, whole Group A completion, native authentication, credential validity, hosted verification or release follows.

## OR-1 exact successor backcheck — 2026-10-05

**READY for the bounded Root OAuth consuming contribution at lib5707/runtimee75f/App28a83. OR-1 repaired; no remaining actionable finding established in the reviewed scope.** Same reviewer affected backcheck, not historical identity substitution or independent test execution. Original NOT READY report prefix SHA `fe22a0232697bf60d18c0de6f64ed9930380690dbdb8d0eb25353638370f047e` remains unchanged. Native UI/auth/browser/modal/credential qualification and broader account reconciliation remain their separate owning boundaries.

Independently read/hashed current repaired source and final author return SHA `ddd230e6611ea297269ce94e0d5a55decdaba5fdf7ccf39aba5abb736959129a`; compared every eleven frozen consumer/Core/home/test file byte-for-byte with final `/private/tmp/chirality-or1-repaired-bKffPe` archive. All match. Actual candidate pins:

| App-v4 relative source | SHA-256 |
|---|---|
| `app/src-tauri/src/lib.rs` | `5707a056e3e331c6d40c123a687c03b72c960b5d77d4887fa386760e355bb3ab` |
| `app/src-tauri/src/runtime_session.rs` | `e75f4457be8efb8f0e332b86c5e72b81b4ffced0fca7e4a4095f68cc1aec4d3a` |
| `app/src/App.tsx` | `28a83a3485d9f4f437dc0cceb907475a3855c343b3f32fc67fa731a87733a489` |
| `app/src-tauri/src/hosting.rs` | `a78a2a7206434e44b1946139098521d678a07057cc8fd8fd1da329afa31ef263` |
| `app/src-tauri/src/auth_rpc.rs` | `461166dcc28b621a80c23b75cef939951d6794620db1b4bc89acf3efcd58306d` |
| `app/src-tauri/src/oauth_control.rs` | `8096834b5eb9d73f140f585a01bd55535d4d7ec682220ca145daeecddf283060` |

Explicit commands now pass their requested full G through the receiving helpers. Capture checks Account class/current ready source and requested G, then verifies the actual captured wrapper source G and repeats currentness. Presentation and cancel preserve that private Arc; current guards compare its original source and actual receiving-slot association, rather than choosing a later control after native interaction. Cancellation rechecks after confirmation before Core's final original-wrapper dispatch. The inherited home/session router remains untouched for retained-generation history. Stale same-home/App-session G1 admission now refuses before successor G2 presentation or native confirmation/cancel.

`NativeOAuthStart` privately carries the exact issued Arc and its safe original observation through wait/return/automatic continuation. No Serde/Debug/public constructor or JSON control authority was added. Automatic delivery checks that issued operation's source/current slot association and reads its original observation; it never selects a replacement slot. A same-G second operation thus cannot receive the earlier start's automatic native act. Core still owns one-use presentation, revocation, one-pending control, original cancel ID, final pipe/source admission and unknown/no-retry semantics.

The optional genuine bootstrap descriptor now follows the existing key/logout receiving pattern: recheck before/after start confirmation and after policy wait, before/after cancellation confirmation, and through the native display's current callback plus post-display currentness. Current Account/Probe drift refuses while healthy unrelated prospective-key state has its established independence. Missing new descriptors retain legacy explicit account limits; no default, root widening, native discovery or atomic filesystem promise. Physical checks do not substitute for Core lease or source control. A device callback can observe physical refusal while lease remains active, then return unavailable/error and retain original pending Cancel until restored.

Independently verified exact preservation of the complete HomeRouter block (SHA `467a97e5f0a037d2369a7c2f052358836ea5568b3b19519c9a3e200cb029e2df`) and native_oauth_display nonmac/mac platform adapter block (SHA `7f9524186b7055a352abf48d2b1781c413813b13b1fa7de53941f596b41645e4`) against original runtimefe0c. Their earlier source review warrants remain. App28a83/Corea78a/auth461/controller809683 are unchanged; no new native platform claim follows from receiving repair.

Original preimages at `/private/tmp/chirality-or1-original-4Bm0eh/preimage` independently match lib57b90/runtimefe0c. Read the disclosed extracted predecessor: helper extraction preserves latest-slot selection, omits requested-generation fence, and auto continuation still uses safe result availability then latest slot. Its author execution is correctly associated with libf03ed/runtime d448, not byte-identical fe0c. Final record preserves actual exit101 zero/three failures: stale presentation callback1, stale cancellation confirmation1, old same-G auto continuation callback1 against required zero. This is now author-executed original-vector evidence, distinct from this reviewer's original source-only finding.

Inspected original and repaired three tests. Original zero-effect assertions/messages, genuine same-App-session/same-home restart counter inequality, original request identity distinction, successor availability and zero cancel predicates remain. Necessary helper signature/private-start-return access changes are disclosed; whole test byte identity is not claimed. Valid G2 presentation/cancel and same-G second-start inverses were appended without weakening the original oracles. Metadata three controls separately test confirmation drift with zero policy/login, cancel drift with zero native request and pending control retained/restored valid inverse, and active display currentness refusal independently of lease. Existing seven tests preserve their source/privacy/one-use/dismissal/null-ID/null-account/policy/no-retry meanings.

Read actual final author evidence: approved isolated offline/locked skip-stock `--lib oauth_root_` exit0 **13 PASS**, compile2.02s/run1.99s, including original three controls/inverses and metadata three; separate unfiltered `--test access_integration --test recovery_startup` exit0 **9+6 PASS**, compile4.11s/run0.76s+0.07s. Thus **28 distinct affected PASS** on this exact stationary source. Original0/3, prior22 and earlier filtered-zero runs remain historical and are not added/rebound. Existing explicit-dismiss/NativeHistory warnings remain disclosed. Cargo was released before author sealing; no later source edit. Frontend28a83 retains its exact prior build/static render evidence. These are author executions; I performed source/hash/oracle/preservation/diff checks only, no repeated Cargo/native/auth call.

The repaired mechanism plus retained original-vector criteria and valid inverses establish repair; passing counts alone do not. Release exact bounded Root OAuth consumer for manager fan-in. Actual AppKit/main-queue/modal/window/button/device clearing, OS/system-browser custody, real native sign-in/account identity/credential validity, complete AE/AR implementation, hosted userVerification and whole Group A/90%/release remain outside this READY verdict. No extra human gate follows from repair/backcheck.
