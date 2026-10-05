# I1-ACCESS-HOME-NEXT — separate API-key-owned home and secret-safe native boundary

2026-10-05. TASK `/root/group_a_execution/design_hosting_access`, parent WORKING_ITEMS `/root/group_a_execution`, no delegation. SOURCE PREPARATION ONLY while parent validates fixed4a5fd9 archive; no product/Design/Cargo/Git/actual credential/home-content/auth/CLI/native/model/network/download operation. Only this packet written. Current inspected code seals below are source snapshots, not substituted for the parent's archive or a qualification verdict.

## Smallest ready contribution

**Immediately ready next bounded code/test seam:** **credential-safe native account RPC/source observation**, exercised on synthetic supplied Host/home descriptors, reusing the existing Host transport/lifecycle/full-namespace machinery and pinned0.160 APIs with synthetic canaries only. Keep H-acct primary operational path intact; do not pretend account-only closes required API-key/configuration work. No new home registry/service/engine, auth copy, App keychain store or generic provider gateway.

ACCESS §3/§4 K2-1 is already adopted by DECISION-L L-1: H-acct for Codex ChatGPT sign-in/local providers; separate App-owned H-key created on the person's add-key route, Codex owns its credential. One child per home; history/readability retained after key removal (§6 Q-7/U-A5), not automatic deletion. Config/settings/global AGENTS/skills share through accepted M-A links; own credential/session/log/state per home. Neither re-login-per-conversation in H-acct, credentials via env/config nor copying the person's auth.json is a permitted shortcut. Home physical bootstrap must be an explicit Root-supplied App-owned path/descriptor, not inferred from cwd/project/library or copied from another home. Exact key-home path/source bootstrap is an ordinary receiving implementation allocation to record before actual filesystem integration, not an invented human gate; this packet chooses no new layout/registry.

Separate **home class** (`account`, `api-key`, `probe`) from actual opaque `generation.home`. Current Host uses `app-home:<SHA256 physical-path bytes>`; that is an existing opaque home identity, not literally `api-key`, the OS path, a credential hash or project ID. Use the full {appSession,home,spawnCounter} for every source/receipt/registration; route class→explicit owned Host and keep actual home identity in observation. Same counter/RPC/thread label in another home never matches. Current lib has one configured Host (`CHIRALITY_CODEX_HOME`) and a thread-only home-kind map; separate-home adoption must make ambiguous/native thread lookup home-scoped rather than assume globally unique IDs. AccountObservation takes actual opaque identity; model entry uses home class. Shared App-session meaning and per-home counters must remain explicit; no identity registry invented.

## Actual source blocker to direct API reuse

Current hosting.rs SourceRequest retains frame.clone in source_requests and exposes attempted_frame/attemptedFrame/sentFrame/status. That general evidence route would retain/expose apiKey after a real login call, contradicting ACCESS CR-1/CR-2/CR-4/CR-6. **Do not release real-key handling through it unchanged.** Ordinary code work can first supply a method-aware sensitive path on the same proven source primitive: raw credential only in transient one-write memory/native frame, metadata/redacted source receipt/journal/errors afterward, buffers/entry field released on successful/failed/unknown attempt. No replay/automatic retry, hash-of-key identifier, full/partial key display, debug formatting leak or secret-bearing cached request. Redacted evidence explicitly states it is not original frame bytes; preserve genuine full namespace/RPC/method/type/write/outcome facts without a false byte-equality proof. Existing non-secret Bridge/role/input behavior and all-write liveness/serialization guards remain unchanged. A separate sender daemon/protocol translator is not needed or authorized.

**Exact transient/redaction boundary for this seam (CR-1/CR-2/CR-4).**
The secure entry and source-defined one-write serialization may hold the
synthetic/real value only for that bounded submission/attempt; release the UI
field, transient buffer and queued sensitive frame when written/failed/cancelled
or generation-lost as actually observed. Necessary bounded transient processing
is allowed; no persistent/long-lived second key copy solely for later matching.
Do not claim allocator/OS physical erasure from ordinary release/drop. CR-1's
post-write release is retained: asynchronous diagnostics can use method/field
projection rather than extending key lifetime to compare arbitrary text.

CR-2 request recording keeps account/login/start method/type/loginId where
actually present; apiKey/accessToken/secretAccessKey/sessionToken are explicit
redaction markers before any retained client/source frame, journal, snapshot,
diagnostic or error formatting. Sensitive response authUrl/verificationUrl/
userCode exist only in their source-defined pending native sign-in presentation,
never durable/logged source evidence; complete/error/cancel/loss clears them.
For this API-key call, retain only actual safe typed response/method/RPC/outcome
facts. Account-method free-form error text may echo a released key: treat that
text as sensitive and return an explicit redacted/unavailable marker plus
actual safe code/limits, not an unchanged-original claim or a retained matcher.
Incoming native bytes can be processed transiently to build that redacted source
observation; do not keep raw secret-bearing response/error in SourceEvidence,
SourceRequest reply/status, journal/debug/UI diagnostics after that boundary.
Preserve that a real response/error was observed and its exact source identity;
redacted bytes are not the original frame. This is targeted account-method/
known-field custody, **not** generic DLP, unrelated notification filtering,
supplier patching, transcript scanning or a blanket evidence-erasure guarantee.
Existing native notifications still reach their owners with actual source/limits;
source redaction decisions must be explicit and independently tested.

Native secure-entry/private credential-origin handoff is NIR/shared-owner work before real UI; a renderer JSON key or synthetic constructor does not prove native field/user origin. This seam may use private synthetic input only, no actual credential or home store read. Actual UI/source/security/real Codex custody and account access remain later witnesses, not blanket preconditions for ordinary synthetic implementation.

## Exact0.160 native inputs and interpretation

Pinned embedded bundle hash e77b7d14…827c is the same actual generated reference; read only.

- `configRequirements/read {}` → requirements object/null. Read allowedLoginMethods/cliAuthCredentialsStore in each home and config/read `{includeLayers:true,cwd:<actual native project-layer context where relevant>}`. Empty allowedLoginMethods permits none; api exclusion is KE-3/not-permitted, never repaired by changing user config. Omitted/null restriction is not invented permission/policy evidence; preserve source limit and actual native refusal. Credential store file/keyring/auto/ephemeral is user's carried setting, not App-selected storage policy.
- `account/login/start {type:"apiKey",apiKey:<transient person/synthetic buffer>}` on H-key only → LoginAccountResponse `{type:"apiKey"}`. KE-5→KE-6 records present per source; **validity unknown until actual use** (AK-5), no model/account qualification from the response. Native error redacted→KE-7; lost response/generation→KE-8 unknown, never replay key.
- `account/read` without forced refresh/include-token → native account `{type:"apiKey"}` or null. GetAccountResponse requires requiresOpenaiAuth; account itself can be omitted. Omitted account is unknown/unavailable, not fabricated absent. apiKey account carries no email/person identity; do not use it as codexAccount/verified actor.
- `account/logout {}` on H-key after real live-work assessment for that home → empty typed result; KE-13…KE-18. Do not inspect auth.json/keyring to claim removal or delete history/home. Confirmed lifecycle acts retain NIR/REC behavior; synthetic tests simulate, never perform person's act.
- `model/list` on entry's home, then native `thread/start` with explicit person-chosen modelProvider/model and owning role composition. No account-per-thread selector in this pin; switching another home is not native thread transfer. No default/fallback or false provider capability inference.

Provider configuration contribution stays retained but separate after the secret/home seam: Q-8 `config/batchWrite` with edits `{keyPath,mergeStrategy,value}`, explicit **resolved target** filePath, expectedVersion from actual config read, then native reread. Link is verified after writes; conflict/overridden policy shown, no retry/fixup. Share actual user's settings by the accepted link, never copy into session flags or own config silently; M-E own-config fallback is a later observed link-reading failure choice, not permission to force a working primary path. No credential field/env_key/bearer/auth/aws/gateway_oauth written by this local-provider path. Constructor/layout/link-test fixtures use invented config/AGENTS/skills only. Codex owns base/discovery; ROLE supplies additive product+active role, never baseInstructions/user-config veto or registered workflows as skills. Actual linked global guidance/skills discovery/base preservation is an explicit witness, not inferred from filesystem topology.

## Concrete bounded implementation/test return

**Unit A first, independently buildable:** isolate method-sensitive transient
account RPC and repair generic SourceRequest frame/reply/snapshot/journal/error
exposure with synthetic canaries; actual H-key topology is not a precondition
for this code. Illustrative private entrypoint
`account_login_api_key(&Host, exact_generation, TransientApiKeyInput)` serializes
only `{type:"apiKey",apiKey:<borrowed transient value>}` through the existing
scoped complete-frame writer; its returned source observation is metadata/
explicitly redacted, never a retained raw secret frame or a JSON-replayable
credential capability. The input is private/source-created, no Clone/Debug/
Deserialize secret reflection; no API shape here claims that a supplied fake
home has real H-key authority. `account/read`/policy/logout projections consume
actual typed responses/unknowns, not credential files. Exact code names/signature
can fit existing Host API without a new transport service; source lifetime and
redacted-versus-original evidence constraints above are the fixed contract.

**Unit B explicit dependent receiving work:** actual source-owned H-key
bootstrap/Host/config binding and shared-resource wiring using Root-supplied
descriptors alongside unchanged H-acct, KE/home-scoped selection/REC lifecycle
and native secure-entry UI. Its actual path/resource inputs must be supplied
before any real key operation; no automatic auth/config clone or guessed home.
Do not make Unit B/full topology or configuration qualification a blanket hold
on Unit A's concrete exposure repair. Neither unit is permission for real
credentials/sign-in/native/model use under this synthetic-only release.

No generic architecture expansion. Fake published-protocol supplier/test pipe only; two synthetic paths/config/link fixtures, no actual Codex/home/auth/network call.

Required cases: identical counters/RPC/thread labels in two homes refuse cross-home routing; H-acct chatgpt/local unaffected; key canary occurs exactly once in designated transient wire buffer, absent from retained SourceRequest getters/snapshot/client/journal/errors/debug/disk; error echoes/key/auth-url/device-code redacted; known api restriction refuses with no frame/config change; absent restriction/account stays qualified unknown; typed login result/policy/logout and KE failure/loss transitions; unknown attempt never resends; stale/closed generation and queued stop retain all-write truth/liveness; user-selected provider/model carried unchanged and old home/thread never transferred. Actual attempted/completed source observations and malformed/scope limits remain, not optimistic Boolean receipts. Use independent review on exact code/schema resource seals; preserve actual Bridge/secret/settlement controls and source oracles.

Definition/custody/selection code may be built using synthetic inputs under ordinary authority now. Shared Root physical H-key bootstrap/config links, NIR secure entry/UI and per-home REC stop/quit/source reader integration are exact next receiving inputs, not claimed already available. Real API-key/sign-in/storage/provider validation and supplier/App qualification need their own owner-coordinated credential/environment evidence; current task authorizes none. U-A2/OI010 deferred real-key observations, U-A4 ChatGPT UI options and U-A5 removal lifetime remain their owners' questions at the applicable point. Existing adopted K2-1/settings/native base obligations are not reopened or narrowed simply because the current source is account-only. Parent/Root handles genuinely reserved credential/live/release/privacy choices; no new approval ceremony for these ordinary implementation means.

## Read sources / current SHA-256

ACCESS K2-1/Q1/Q6/Q7/Q8/KE/CR/AK and account-home decision M-A, HOST full namespace/redaction/source API, ROLE additive/base/discovery and REC DEF5/6 selectively recovered; embedded published types/startup/source frame storage inspected. No actual home or credential bytes read and no supplier executable invoked.

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_AND_PROVIDER_ACCESS.md` — `5067ed0b64b0a7787d33809b542c1cbadd02793e136b136e330bb933d5f8a203`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_HOME_DECISION_RECORD.md` — `f77f87927558ca73ab862fbe1452eaf5a0c47b6bb53b89c1419e2324ec4dad5d`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` — `5b67393fd2cf2e45c51b72b1110a1dc1bce4ad7e0f3f3749e8940270975437b0`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_SUPPLY.md` — `b279a23a5c8d8b2170618a062b3a5ccc3ea07a1cecdfcec7c61d0320f6559ba9`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` — `e78b9ead452b0a1adb20cf07493a1eccbd2ee651e68d4f75772c440a6a228056`
- `projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.v2.schemas.json` — `e77b7d1436a78f431a74b2cb263a862e92ae40d70411bc63835b47ab2168827c`
- `projects/chirality-app-v4/app/src-tauri/src/lib.rs` — `921c6e09c83d15e1aee18d02eb16d4ddc7ed84d3b7afbdf207b64210d975035b`
- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` — `cf798098bd40bc2de4c5dac6ec15c929f45e7fe6a6b8d75dcd6abcb1dbd26b70`
- `projects/chirality-app-v4/app/src-tauri/src/access.rs` — `cf6a439f98433b3fbfb1d96a7fb0f4270b080e1b7bb1e1a6bcf470b78716a5ac`
