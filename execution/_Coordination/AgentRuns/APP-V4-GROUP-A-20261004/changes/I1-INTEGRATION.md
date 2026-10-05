# I1 App consumer integration — bounded source/test unit

TASK `/root/group_a_execution/runtime_integration`, parent `/root/group_a_execution`, delegated-harness-native descendant. Supplied launch model gpt-6.1-sol / medium; no descendants. Production branch base `38bb2bc87a`. No Git, instruction-amendment, Design, schema, Cargo or other shared-module writes performed. App v3 AGENTS was incidentally read while discovering the project path; its rules were discarded as inapplicable. Parent's initial v3 product-default suggestion was superseded; copied files were removed before any application execution or adoption.

## Connected behavior

`lib.rs` exposes `host_observe(generation: Value, after: u64)` as the public atomic read-only full-generation observer. `host_status` consumes the same Host observer using a main-process `RuntimeSession` cursor and returns the host snapshot plus `nativeView`, `nativeViewLimits`, `observerCursor`, `observerGap`, `accountObservation`, `accessSelection`, `roleSupply`, and instruction/recovery initialization limits. UI reload loses no register or host cursor, sends no answer, and writes no record. Full tuple changes reset receiving view/account namespace; terminal closure marks live observation lost, and checklist loss remains explicit. Repeated receipts do not produce additional revisions. Unrecognized raw frames/fields remain in the host journal and native view; tool, parent and child status imply no checking, acceptance or integration.

`answer_native_request(generation, requestId, answer)` accepts neither origin, rule nor actor input. `answer_preview` checks the live ready tuple/card/outstanding state and runs the native generated validator/offered-choice checks before composing masked confirmation. The named native App confirmation is the only person submission path; cancel keeps custody outstanding. The host derives `person:… (identity not verified)` from the editable display name, actual OS account and only correlated same-generation native-reported Codex account. The authoritative Host register checks again after confirmation, serializes reply write/resolution, distinguishes failure, written/no-ack and supplier resolution, and redacts secret question answers. Submitted secret question/form bytes are absent from confirmation/returned success text and disposable UI drafts are cleared before submission. Neither person inputs nor native tool permissions create reserved human-act evidence. Existing P0 native decision capture remains host-native; its identity now includes a Codex account only when the same-generation observation supplies one.

`App.tsx` renders exact modern offered decision values (including supplier-proposed amendments), native legacy values, requested/subset permission grants with explicit scope, question option labels/free inputs with secret masking, and native elicitation action/content. Declines keep per-kind shapes. Parameters and unknown raw fields are inspectable. Unknown/error/supplier-resolved/reply-write/ack states use custody's actual fields. Raw JSON native execution details are a first receiving view, not a completed polished conversation interface.

`thread_start` requires explicit model/provider/access entry, uses `ConversationSelection` and refuses unavailable API-key-home entry without fallback. This first host owns its configured account home; distinct API-key home/multiple concurrently owned homes are unfinished. Each Start thread is a new conversation with a fresh selection. Primary role is none or HELP_HUMAN/HELPS_HUMANS/WORKING_ITEMS; TASK is refused by `Composition`. Reviewed `role_supply` composes exact common/full-role bytes; the Host owner's `thread_start_with_guidance` sends only additive `developerInstructions`. Selection/carried source hashes are exposed with adoption unknown and native children not supplied. No parser modules are imported, no base instructions replaced and no model/provider/network/configuration/sandbox/approval defaults added.

## Explicit prerequisites and remaining work

The v4 packaged instruction tranche is being supplied/reviewed independently. Production defaults currently contain no instruction body and fail visibly before seeding. No v3 or repository corpus is activated as product common guidance. On admitted bytes, `seed_instructions` uses exclusive creation under host-resolved App user-data/instructions and preserves existing edits; `Guidance::read_seeded` retains default/modified identity and refuses unreadable/symlink files. Failed initialization has no alternate path. Supply/default/readback/native-child qualification remain separate obligations; supported API transport does not establish model adoption.

`reviewed_ledger_path(App-own-user-data)` prepares exactly runtime/recovery.ledger.jsonl. Actual `configure_recovery` startup adoption awaits manager V0-REC-R9-LEDGER; UI explicitly reports not-adopted, with Host recoveryPersistenceError separately visible. Tests use only an explicit unique scratch path and no payload/credential copy. Required native replies remain independent of persistence. The preexisting reviewed later-error RECOVERY mapping gap, conversation/run/tag/read/interrupt/quit/session transitions, actual relaunch/recovery, native protected capture/SEAL-2 and trusted cold replay remain unfinished with their graph owners.

## Verification

- `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --test runtime_integration`: **5 passed, 0 failed**, exit 0; affected rerun after question/form masking, account-change invalidation and P0 actor account wiring also 5/5 (0.23 s). Manager granted serialized Cargo slot; returned after command completion. Synthetic register → view/request association → native preview → write/no-ack → supplier ack → pointer-only scratch ledger is exercised. Separate tests cover replay deduplication and full-home transition, strict offer/origin/secret checks, explicit fixture guidance with primary TASK refusal, and correlated same-generation native account observation/loss/change invalidation.
- `app/node_modules/.bin/tsc --noEmit`: exit 0 (after UI/role plumbing).
- Existing P0 capture, independent sibling source tests and physical native UI/supplier proof are not claimed by these tests. No supplier process/model turn/network/download/sign-in/credential use performed.
- Independent source review is required before PR. Candidate changes/default/ledger adoption require affected rerun and review coverage.

## Consulted sources

Full TASK and v4 LOOP, manual entry list/headings, Field Book full text, current group graph and reviewed I1/V2-I1-R1, and bounded NIR request rules, ACCESS home/selection/identity rules, RECOVERY storage placement, NPTD plans/tools/descendants/actor rules and native-items public API. Root AGENTS was supplied by the user; exact current file fingerprint below preserves its repository origin. App v3 incidental discovery is recorded above and confers no v4 applicability.

| Origin relative to repository root | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28` |
| `docs/alignment-manual/README.md` | `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |
| `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` | `2ee7236aeeb45de6e8a6fbefe3bb570d1eb67f62533a2cb9a089f7cd5c33fac6` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1.md` | `587a10c27dfc77687c8d1ac7002d639ebe4f63dbd1350b9b35d11280b26d85f7` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V2-I1-R1.md` | `f703ac3d1fd897448594f02576e8a5cf7d8b39a3a5c0f7bea39cd342f34b7d0c` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md` | `f9794dcc24d55b813b760daa0f120d9fc53c4893282e907b550e60cdb085ab7a` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-03_Native plans, tools and delegation views/Design/NATIVE_PLANS_TOOLS_DELEGATION.md` | `8b8d0e46a25b6872e806aa49cc9e7604515d643bbd4a51c0913bbcace2585c54` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_AND_PROVIDER_ACCESS.md` | `0f177361460a30c52615607457289c1fe275f55264cbe0d95f9c6d4e0ed0ed57` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` | `a19beb59638a954078e093658d326bdeae4a2c9d1241d5ff69d262abc3e9b4b5` |

## Frozen consumer source after affected checks

No changes to these four source/test files after the following fingerprints. A successor default or ledger adoption must reopen affected checks and review. Companion hosting/role source remains with its separate owners.

| Consumer file relative to project root | SHA-256 |
|---|---|
| `app/src-tauri/src/lib.rs` | `f114c22b597162b61e13a24610af0cf831a34de45be192d7eb9f899cfb934769` |
| `app/src-tauri/src/runtime_session.rs` | `d65dc498c8d214ce3d65aa9d28c7d331b96e7af29c149db4bb0ac916cd6b2026` |
| `app/src/App.tsx` | `78e1aef406289f781e85a4f162dee6527696d0c40e29dd8284e8e3fe5d241a1f` |
| `app/src-tauri/tests/runtime_integration.rs` | `4a0b3b0484b116241b409833ff6f85f2c5f54d828927d49d15d28cf9f5f94ae0` |

## Successor repair and affected checks — 2026-10-05

The earlier five-test/empty-default candidate above remains historical. Original-owner TASK runtime_integration repaired the independently reported request/attribution/continuity seams: partial/unanswered question maps and empty inputs remain possible; form/openai/form/openaiForm all collect and validate native content; openai/userVerification acceptance is explicitly unsupported without device proof (no invented proof; decline/cancel remain native). Current atomic Host observation is consumed before answer/A16 attribution and compared again after native confirmation, including account-change revision so an intervening change/same-email reread cannot reuse the old context. Context change requires a new confirmation and creates no act/reply.

The independently READY V0-INSTRUCTION-TRANCHE's exact five v4-owned instruction resources are now embedded; SOURCE_MAP is evidence, never composed as extra guidance. Scratch checks cover exclusive first seed, preserved modified files, missing/non-UTF8/link refusal without reseeding, per-part source state/default identity and fixed old composition versus new entry reading edits. No v3/root Git corpus was adopted. Restore/upgrade controls, actual native/supplier role supply and model behavior remain unfinished at their points of need.

A direct successor generation archives the old receiving view only under its old full namespace, with per-turn checklist-loss notice and observation-ended/not-live-custody standing. Native same-generation final admitted envelopes are consumed before closing; later closed/foreign frames cannot alter that closed view. Current/previous views stay separate. observerRecovery explicitly says Codex history has not been read or rebuilt; no cached view or archived checklist is promoted to live custody/recovered history.

Affected offline checks: baseline eight tests passed 8/8; after the two independently specified continuity regressions, runtime_integration passed **10/10**, exit 0, 0.17 s. Real App.tsx transient SSR rendered checks pass for enabled partial/unanswered Send, omission control, secret mask, all three form aliases and no device acceptance button with native negatives retained. TypeScript --noEmit and diff-check pass. Native IPC was stubbed only in that explicitly synthetic SSR check; no native picker/window/confirmation/model/supplier/account/network/download witness is claimed. Serialized Cargo slot was returned after each completed run.

Frozen I1 successor seals verified before the next shared I4 unit:

| Project-relative source | SHA-256 |
|---|---|
| `app/src-tauri/src/lib.rs` | `b92010c8b372fc61a50d383af1235aa24bb4a5cdab728b6907528fa7a03fdece` |
| `app/src-tauri/src/runtime_session.rs` | `77114507c1715442d6384d7cd9dde71c97bfaf80bc6f69f6428affda150f412e` |
| `app/src/App.tsx` | `9501bb821cf06739df7a19461b8f33803f6fac380abde78925f5f857beb1985c` |
| `app/src-tauri/tests/runtime_integration.rs` | `18ed6496863eb76cc950c96e162ddb955139a92d776a313c3a9e7a4591195ee2` |

Independent hosting reviewer reports final two continuity checks 2/2 PASS and matching successor seals; its named final report is retained by the manager. Ledger startup is still not adopted here: named RT mapping product adoption/backcheck remains pending. Device-verification flow, history reconstruction, actual native interaction, protected capture/SEAL-2 and trusted cold replay remain unfinished. This is bounded repaired source/test readiness, not whole entry/NIR/ROLE/Group A completion or release.
