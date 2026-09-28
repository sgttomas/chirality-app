# Codex 0.158.0 pin spike — observation record
- Contribution: DEL-01-01/PIN-SPIKE-v0.1
- Status: OBSERVATION RECORD — spike evidence at pin 0.158.0, not qualification
- Serves: OUT-002 (generated protocol types with provenance at the selected pin; supplement assessment), OUT-003 (local-provider requirement account inputs L-1…L-6), OUT-004 (first recorded exchanges and a regeneration method); REQ-001, REQ-002, REQ-003, REQ-005, REQ-006; evidence toward VER-001, VER-002, VER-005, VER-006 (none of them is passed by this record)
- Basis: repo `be8bb46dd` (worktree `test-ci-optimization-f6cacd`, branch base `6e18505e3`); ScopeOfWork.md sha256 eddd122cf8b6e2c1ce5933ddb82aa9ec8591baa138a20f439e171ce5d83c4773; owner decision D4 in `_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` (sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e); W11 brief in that run's `BRIEFS.md`
- Consumed inputs: DEL-01-01/HOSTING-BOUNDARY-v0.1 (`Design/HOSTING_BOUNDARY.md`, sha256 f1da7f76f686991f67b3e974478b9b453df804839712a7e5cc24e7bc4849d728), §4, §5, §6, §7, §8.1, §9, §10 (P-01…P-15)
- Receivers: DEL-01-01/HOSTING-BOUNDARY v0.2 repair (R1); DEL-01-02 (lifecycle, register, post-restart reads) via DEP-01-01-019; DEL-01-03 (plan/revision, subagent items) via DEP-01-01-020; DEL-01-04 (server-request answer forms) via DEP-01-01-021; DEL-01-05 (providers, accounts, home, network) via DEP-01-01-022; DEL-01-06 (distribution identity, signing) via DEP-01-01-023; DEL-02-04 (additive instruction inputs) via S-6; App implementation owner (OI-008, generator-reference choice, pin re-examination under D4)

**Reading note.** Supplier method and field names appear here because this is
a record of what the supplier actually emits at 0.158.0. They remain supplier
facts, not Chirality wire choices. Standing labels used below:
`observed` (behavior seen live in this spike); `observed-in-generated-types`
(present in this pin's generator output; runtime behavior not exercised);
`published-only` (help text or doc comment only); `not-observed`. Nothing here
adopts, qualifies or passes anything (D4: "The selection does not establish
qualification (DEP-005)").

## 1. Authority and environment

- Authority: owner decision D4 (OI-012). Performed only what the W11 brief
  permits: scratch npm install; `--version`, `--help`, `app-server --help`,
  generator subcommands (and their `--help`); `app-server` over stdio with an
  empty scratch `CODEX_HOME` for the handshake and unknown-method behavior.
- Not performed: sign-in, model turns, `~/.codex` use, global npm prefix, git
  operations. Two extra help pages (`app-server proxy --help`,
  `app-server daemon --help`) and two handshake variants beyond the brief's
  minimum (unknown method before `initialize`; `SIGTERM` instead of stdin
  close) were run to answer P-05/P-07; no request other than `initialize` and
  one deliberately unknown method was ever sent.
- Host: macOS 26.6.2 arm64 (Darwin 25.6.0), Node v24.5.0, npm 11.5.2. Date
  2026-09-28, ~00:46–01:00 local.
- Scratch: `<SCRATCH>` = the session scratchpad `…/scratchpad/codex-0.158.0`;
  install prefix `<SCRATCH>/pkg`; `CODEX_HOME=<SCRATCH>/codex-home` for every
  invocation; child cwd `<SCRATCH>/cwd`.
- `~/.codex`: none of the spike's processes had a `~/.codex` path open at any
  snapshot (lsof). Entries under `~/.codex` did change during the window
  (`.codex-global-state.json`, `models_cache.json`, `logs_2.sqlite-wal`),
  including after the last spike process ended; a separately running Codex
  desktop process owned by the person was present. Attribution to the spike is
  **not established and not indicated**; recorded for completeness.
- **Side effect outside scratch (supplier-initiated):** on each start with a
  fresh `CODEX_HOME` the supplier fetched `https://github.com/openai/plugins.git`
  (≈24 MB pack) without sign-in or any turn (§5, S-F-10). Three fresh-home
  starts occurred, so three fetches.

## 2. Exact commands and exit codes

`C` = `<SCRATCH>/pkg/node_modules/.bin/codex` (npm wrapper, which spawns the
vendor binary); `V` = `<SCRATCH>/pkg/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex`.

| # | Command | Exit | Output (abridged) |
|---|---|---|---|
| 1 | `npm install --prefix <SCRATCH>/pkg @openai/codex@0.158.0` | 0 | "added 7 packages"; installed `@openai/codex@0.158.0` + `@openai/codex-darwin-arm64` (= `@openai/codex@0.158.0-darwin-arm64`) |
| 2 | `shasum -a 256 V …` | 0 | §3 |
| 3 | `codesign -dv --verbose=2 V` / `codesign --verify --verbose V` | 0 / 0 | Developer ID Application: OpenAI OpCo, LLC (2DC432GLL2); "valid on disk", "satisfies its Designated Requirement" |
| 4 | `spctl --assess --type execute -vv V` | 3 | "rejected (the code is valid but does not seem to be an app)"; origin OpenAI OpCo, LLC — expected for a bare Mach-O; not a notarisation verdict |
| 5 | `C --version` | 0 | `codex-cli 0.158.0` (also created `CODEX_HOME/tmp/arg0/…`, S-F-17) |
| 6 | `C --help` | 0 | lists `app-server  [experimental] Run the app server or related tooling` |
| 7 | `C app-server --help` | 0 | subcommands `daemon`, `proxy`, `generate-ts`, `generate-json-schema` (both generators labeled `[experimental]`); `--listen` default `stdio://`; `--analytics-default-enabled` ("Analytics are disabled by default for app-server" — published-only) |
| 8 | `C app-server generate-ts --help` | 0 | `-o/--out <DIR>` (required), `--experimental`, `-p/--prettier <PRETTIER_BIN>`, `-c`, `--enable`, `--disable` |
| 9 | `C app-server generate-json-schema --help` | 0 | `-o/--out <DIR>` (required), `--experimental`, `-c`, `--enable`, `--disable` |
| 10 | `C app-server proxy --help`; `C app-server daemon --help` | 0; 0 | proxy "to the running app-server control socket"; daemon start/stop/restart/version/… (not used) |
| 11–18 | `_spike/generate.sh <SCRATCH>` = for n in 1 2: `C app-server generate-ts [--experimental] --out …/run$n`, `C app-server generate-json-schema [--experimental] --out …/run$n` | 0 (all 8) | stdout and stderr empty for all 8; see `_spike/generate.commands.log` |
| 19 | `python3 _spike/inventory.py <stable-schema> <experimental-schema>` | 0 | `_spike/inventory.txt` |
| 20–29 | `node _spike/handshake.mjs <SCRATCH> {A,B,C,D} {bin,vendor}` (10 runs, §5) | 0 (all) | child exit code 0, signal none, in every run |
| 30 | `python3 _spike/redact.py <SCRATCH> _spike/transcripts` | 0 | 8 redacted transcripts |

## 3. Distribution and identity (P-01, P-02)

| Element | Observed value | Standing |
|---|---|---|
| Package | npm `@openai/codex@0.158.0` (tarball integrity `sha512-GBhcKpQmVLsCtEP5mUf6WFye6QQgTKotwsXrYPM0GFmEsoOSahik6hkf2FHabX9kZBl0Y0/PQowLu7uYMKT8dg==`); platform package `@openai/codex@0.158.0-darwin-arm64` (integrity `sha512-0OKSjlWY1j4Ld1fT87QttNw3Y2SthcXi4GcrWSHjleZg1n86eG3+shJl4Pv+siUmsBJhWlNmm6rRO4Yv8ZyQLg==`) | observed |
| Version label | `codex-cli 0.158.0` (`--version`); `codex-package.json`: version 0.158.0, target `aarch64-apple-darwin`, entrypoint `bin/codex` | observed |
| Binary content identity (SHA-256) | `bin/codex` 788a818fbb9596869c7a487554507cb8bdca17584b8671112b23f9e225ba35c8 (239,662,592 B, Mach-O arm64) | observed |
| Sibling executables the supplier ships | `bin/codex-code-mode-host` d47e28a83f8b5c38f3dbf59f9590c580b3d95ae66102e3e180f0e0d6f050fc4c; `codex-path/rg` e04d453360b68749ce735f65e8dbbe70685a51f7b88288f617e610076cce3aac; `codex-resources/zsh/bin/zsh`; `codex-resources/voice/…` (host binary, GStreamer dylibs) | observed |
| npm wrapper | `bin/codex.js` 61b0194f3bb6534439c8d26a3ed57d0805f84b884588b761795323eeb92fcf70; spawns the vendor binary with `CODEX_MANAGED_PACKAGE_ROOT` and `CODEX_MANAGED_BY_NPM=1` added to the environment, forwards signals | observed |
| Signing | Developer ID Application: OpenAI OpCo, LLC (2DC432GLL2); hardened runtime flag; signature timestamp Sep 27 2026 22:40:09; `com.apple.provenance` xattr present | observed |
| Licence | `package.json` of both packages: `Apache-2.0`; no LICENSE file in either npm package (only third-party licences under `codex-resources/voice/licenses`) | observed |
| Standalone run (P-02) | Vendor binary started directly from its package location gave the same handshake as via the wrapper (A-vendor, D-vendor). Generators ran without missing-asset errors (contrast: T11's 0.149 probe exit 2 — historical). Running the binary relocated away from its sibling resources: not tested | observed (partial); relocation not-observed |

## 4. Generation (P-03, P-04)

**Commands and flags.** `codex app-server generate-ts --out DIR
[--experimental] [--prettier BIN]` and `codex app-server
generate-json-schema --out DIR [--experimental]`. `--experimental` "Include
experimental methods and fields in the generated output". No prettier was
used, so TS is the generator's raw form. TS files carry the header
"generated by ts-rs … Do not edit this file manually".

**Output and determinism** (each variant generated twice; every file
byte-identical between runs):

| Variant | Files | Bytes | Per-variant manifest SHA-256 (sorted `shasum` listing) |
|---|---|---|---|
| TS stable | 732 (94 top-level, 637 `v2/`, 1 `serde_json/`) | 426,930 | 5606da9ab4986e7cb08e152b2c9327766c2da01f09d7bcd2808b7311eb84386d |
| TS experimental | 873 (+141 files, 0 removed; 22 common files differ) | 516,626 | 9929458e2a7532299c31166954d4356b2315f29777f3651c0a2fcf53e085dd4b |
| JSON Schema stable | 314 (37 top-level incl. 2 bundles, 2 `v1/`, 275 `v2/`) | 3,534,610 | f4901c6aafb9870a5f6d9b6329c2283bdc1eff8c2b024f02eeb7ade35b527aa4 |
| JSON Schema experimental | 440 (+126, 0 removed) | 4,280,228 | 95942cbe0624f6685f61727e3feae27e86ffcf67ca161a846295f9e676e6f6c9 |

**What is committed** (`generated/0.158.0/`, total ≈2.93 MB with `_spike/`):
all of `ts/stable/` and `ts/experimental/`; from JSON Schema experimental only
the two self-contained bundles `codex_app_server_protocol.schemas.json`
(862,263 B) and `codex_app_server_protocol.v2.schemas.json` (750,395 B), which
together contain a definition for every one of the 438 per-type schema files
(checked by title). `MANIFEST.sha256` (sha256
42b95826d7bd6d58df7941da7420064ee55d54a347a2eab22eafbfa16231569e) lists all
2,359 files of all four variants; 1,607 are present, 752 (the rest of JSON
Schema) are omitted and verifiable only by regeneration.
**Deviation from the brief's size rule, stated:** the rule says to commit JSON
Schema plus a TS manifest when the total exceeds ~3 MB. Here JSON Schema alone
exceeds 3 MB (3.5 / 4.3 MB) while TS is 0.4 / 0.5 MB, and TS carries five
methods the JSON Schema omits (next paragraph). The parent may re-select;
regeneration is deterministic.

**Parent re-selection (HELP_HUMAN, 2026-09-28):** the TS trees are **not
committed**. They add 1,605 files to the repository and are byte-deterministic
and fully hashed in `MANIFEST.sha256`. The committed form is the two
JSON Schema bundles, the manifest and `_spike/`. The TS output (including the
five TS-only methods) is regenerated with `_spike/generate.sh` at the pin and
verified against the manifest. Committed TS types belong with the App
implementation when it starts, under its own location decision.

**Inventory** (`_spike/inventory.txt`; TS cross-check by `"method":` literals):

| Set | JSON Schema stable / experimental | TS stable / experimental |
|---|---|---|
| Client → server requests | 104 / 167 (63 experimental-only) | 107 / 170 |
| Client → server notifications | 1 / 1 (`initialized`) | 1 / 1 |
| Server → client requests | 10 / 11 (`currentTime/read` experimental-only) | 10 / 11 |
| Server → client notifications | 83 / 83 | 85 / 85 |

- **The two generators disagree at the same pin.** TS includes client methods
  `getAuthStatus`, `getConversationSummary`, `gitDiffToRemote` and
  notifications `rawResponse/completed`, `rawResponseItem/completed`; the JSON
  Schema output has none of the five, in either variant. The running server's
  own list of accepted client methods (from its unknown-method error, §5)
  names exactly the 170 TS client methods. (S-F-03)
- Server requests at 0.158.0: `item/commandExecution/requestApproval`,
  `item/fileChange/requestApproval`, `item/tool/requestUserInput`,
  `mcpServer/elicitation/request`, `item/permissions/requestApproval`,
  `item/tool/call`, `account/chatgptAuthTokens/refresh`,
  `attestation/generate`, `applyPatchApproval`, `execCommandApproval`
  (+ experimental `currentTime/read`). Against the historical v3 comparison
  aid (approval, user-input, elicitation, dynamic-tool, auth-refresh,
  attestation — T11): all present; new are `item/permissions/requestApproval`,
  `currentTime/read`, and the legacy v1 pair `applyPatchApproval` /
  `execCommandApproval`. v3 used 16 client methods; 170 are accepted now.
- Experimental markers are not reliable from doc comments:
  `item/plan/delta` ("EXPERIMENTAL" in its doc comment) and
  `ToolRequestUserInputResponse` ("EXPERIMENTAL") are both in the stable
  (non-`--experimental`) output. Experimental status is determinable only by
  diffing the two generator variants. (S-F-04)
- Experimental-only fields of App interest (22 differing TS files): on
  `turn/start` `collaborationMode` (plan mode; `ModeKind` = `plan`|`default`),
  `multiAgentMode`, `additionalContext`, `environments`; on `thread/start`
  `dynamicTools`, `multiAgentMode`, `historyMode`, `allowProviderModelFallback`,
  `experimentalRawEvents`; on command-approval params `availableDecisions`,
  `additionalPermissions`; on `thread/resume` `history`, `path`,
  `initialTurnsPage`; methods `collaborationMode/list`, `thread/settings/update`,
  `turn/settings/update`, `thread/queue/*`, `process/*`, `remoteControl/*`.

## 5. Handshake, transport and exit (P-05, P-06, P-07)

Scenarios (script `_spike/handshake.mjs`; redacted transcripts in
`_spike/transcripts/`):

| Run (transcript) | Launcher | Home | Sequence |
|---|---|---|---|
| A-bin.first-attempt | wrapper | fresh | init(exp=false) → `initialized` → unknown request → unknown notification → 2nd init → close stdin (earlier script revision; fewer snapshots) |
| A-bin (2nd fresh run) | wrapper | fresh | as A; transcript overwritten by a later run — only its values seen in-session are cited, marked "(unretained)" |
| A-bin-freshhome | wrapper | fresh | as A |
| A-bin-warmhome, A-vendor-warmhome | wrapper / vendor | warm | as A |
| B-bin | wrapper | warm | init(exp=true) → `initialized` → unknown request → close stdin |
| C-bin | wrapper | warm | unknown request **before** init → init → close stdin |
| D-bin, D-vendor | wrapper / vendor | warm | init → `initialized` → `SIGTERM` (stdin open) |

(A-vendor ran twice on a warm home; the second is retained.)

**Initialize request as sent** (per generated `InitializeParams`):
`{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":…,"title":…,"version":…},"capabilities":{"experimentalApi":false,"requestAttestation":false}}}`.
Generated `InitializeCapabilities`: `experimentalApi` (required boolean),
`requestAttestation` (required boolean), optional `explicitGatewayOauth`,
`mcpServerOpenaiFormElicitation` (legacy), `optOutNotificationMethods`
("Exact notification method names that should be suppressed"), `extensions`;
`capabilities` itself may be null.

**Observed:**

| Observation | Value | Runs |
|---|---|---|
| Initialize response | ~2–15 ms after send: `{"id":1,"result":{"userAgent":"chirality-w11-spike/0.158.0 (Mac OS 26.6.2; arm64) unknown (chirality-w11-spike; 0.0.0-spike)","codexHome":"<SCRATCH>/codex-home","platformFamily":"unix","platformOs":"macos"}}`. No dedicated version element; the version appears only inside `userAgent`, prefixed by the client's own `clientInfo.name`. Identical with `experimentalApi` true (B) | all |
| Unsolicited notification | Same instant as the response, **before** the client's `initialized`: `{"method":"remoteControl/status/changed","params":{"status":"disabled","serverName":"<HOSTNAME>","installationId":"<INSTALLATION-ID>","environmentId":null},"emittedAtMs":…}` | all |
| Framing | One JSON object per `\n`-terminated line on stdout; every line parsed. Server frames **omit** the `"jsonrpc":"2.0"` member. Notifications carry a top-level `emittedAtMs` beside `method`/`params` (declared in TS `ServerNotificationEnvelope`, not in JSON Schema `JSONRPCNotification`) | all |
| stderr | 0 bytes in every run | all |
| Unknown client method (after init) | `{"error":{"code":-32600,"message":"Invalid request: unknown variant ‹chirality/spikeUnknownMethod›, expected one of ‹initialize›, … ‹fuzzyFileSearch/sessionStop›"},"id":2}` (the supplier quotes names with backticks; shown here as ‹ ›) — code **-32600** (Invalid Request), not -32601; id echoed; no `data`; message lists 170 accepted methods, equal to the TS experimental client set, including experimental ones when `experimentalApi` was false; connection continues | A, B, A-vendor |
| Unknown client method before init | Same -32600 unknown-variant error (parse precedes any initialization check); a following `initialize` succeeds | C |
| Unknown client notification | No reply, no stderr; connection continues | A |
| Second `initialize` | `{"error":{"code":-32600,"message":"Already initialized"},"id":3}` | A |
| stdin closed | Child exits code 0, no signal, 8–29 ms after close (wrapper and vendor alike) | A, B, C |
| `SIGTERM` | Child exits code **0**, no signal, 3–6 ms after the signal (wrapper forwards; vendor direct) | D-bin, D-vendor |
| Child processes | Fresh home: supplier spawned `git -c safe.bareRepository=explicit -C <CODEX_HOME>/.tmp/plugins-clone-XXXX fetch --depth 1 --no-tags https://github.com/openai/plugins.git +1dc195897af4161d039b80d8471ec0a10c9bbc89:refs/codex/curated-sync` (+ `git-remote-https`, `index-pack`), with an established TCP connection to port 443. Warm home: no child processes and no IP sockets at either snapshot | fresh / warm |
| Descendants outliving the supplier | A-bin-freshhome: 500 ms after the supplier exited (code 0), the four git processes were still alive, reparented to PID 1; they finished later and left `.tmp/plugins-clone-D34zRh` (sync not finalized). In the unretained 2nd fresh run the fetch finished within ~6 s and produced `.tmp/plugins/` (62 plugin directories, ≈89 MB) and `.tmp/plugins.sha` | fresh |
| Supplier's own sockets | No IP socket on the supplier process itself at snapshots; one unix-domain connection to an unidentified peer (not identified) | all |

## 6. Per-item observations against HOSTING_BOUNDARY v0.1

Verdict column: **consistent**, **refines** (v0.1 holds but needs a named
element), **contradicts** (a v0.1 statement does not match the pin).

| Item | Observed at 0.158.0 | Standing | Verdict vs v0.1 |
|---|---|---|---|
| P-01 | §3: version label, SHA-256, signing, licence declaration, size | observed | **refines** §7.1: the supplier executes sibling binaries (`codex-code-mode-host`, `rg`, bundled `zsh`), so "binary content identity" should be a distribution identity over the vendor tree (S-F-02) |
| P-02 | Vendor binary runs directly; wrapper adds `CODEX_MANAGED_*` env; generators work | observed (partial) | **refines** H1 configuration identity: record launcher and its added environment (S-F-02) |
| P-03 | Generators, flags, exit 0, output trees, determinism: identical | observed | **refines** §7.1 generated-schema identity: must name generator kind (TS / JSON Schema), `--experimental` variant and prettier use (S-F-03) |
| P-04 | Inventory §4; TS ⊃ JSON Schema by 3 client methods + 2 notifications; server accepts the TS set | observed + observed-in-generated-types | **contradicts** v0.1's single "generated set" in §6.1/§7.3/§9.3: two sets differ at one pin (S-F-03) |
| P-05 | Initialize params/response §5; no version element; unsolicited notification before `initialized`; `initialized` sent — whether it is *required* not tested; known method before init not tested | observed | **contradicts** §7.1/§7.2 "handshake-reported identity … must not contradict the declared pin" as a distinct identity: only `userAgent` text carries a version (S-F-01). **Refines** §4.1/§4.2: frames arrive during `handshaking` (S-F-09) |
| P-06 | Opt-in = `capabilities.experimentalApi`; plan collaboration mode (`turn/start.collaborationMode`, `collaborationMode/list`), `dynamicTools`, `availableDecisions`, `currentTime/read` are experimental-only in generated types; whether the server rejects them without the opt-in: not observed | observed-in-generated-types | **consistent** (plan collaboration still experimental, as at 0.154 per T11); **refines** §7.3: `--experimental` now generates these, so the supplement's role narrows (S-F-04) and classification depends on the declared opt-in (S-F-05) |
| P-07 | NDJSON; no `jsonrpc` member on server frames; top-level `emittedAtMs`; stderr empty; stdin close → exit 0; `SIGTERM` → exit 0; descendants may outlive the supplier; notification opt-out facility present (`optOutNotificationMethods`), not used | observed | **refines** §5 framing (S-F-08); **contradicts** the implicit §4.3 assumption that exit facts distinguish ends (both ends give code 0; S-F-07); **contradicts** §4.5 "terminate the child" as sufficient (descendants survive; S-F-06); H7/U-07 consistent (facility exists, unused; S-F-14) |
| P-08 | Answer forms (generated): command approval `accept`, `acceptForSession`, `{acceptWithExecpolicyAmendment}`, `{applyNetworkPolicyAmendment}`, `decline`, `cancel`; file change `accept`, `acceptForSession`, `decline`, `cancel`; elicitation `action` `accept`/`decline`/`cancel` + `content` + `_meta`; user input `answers` map; permissions `{permissions, scope: turn|session, strictAutoReview?}`; dynamic tool `{contentItems, success}`; auth refresh `{accessToken, chatgptAccountId, chatgptPlanType}`; attestation `{token}`; current time `{currentTimeAt}`; legacy `ReviewDecision` `approved`, `{approved_execpolicy_amendment}`, `approved_for_session`, `approved_mcp_policy_amendment`, `{network_policy_amendment}`, `{denied:{rejection}}`, `timed_out`, `abort`. JSON-RPC error reply to a known kind; never-answered behavior | observed-in-generated-types; error/unanswered **not-observed** | **consistent** with R8 (native decisions preserved); **refines** R3/U-11 (a native `timed_out` form exists) and the origin set (supplier-side auto review, S-F-11) |
| P-09 | `serverRequest/resolved` `{threadId, requestId}` in stable notifications | observed-in-generated-types; semantics not-observed | **refines** §6.2 `resolved-by-supplier` and F-10/U-09: an observable element exists at the pin (S-F-12) |
| P-10 | `turn/plan/updated` `{threadId, turnId, explanation, plan:[{step, status: pending|inProgress|completed}]}` (whole plan each time, no revision number); item `{type:"plan", id, text}`; `item/plan/delta` `{threadId, turnId, itemId, delta}` ("clients should not assume concatenated deltas match the completed plan item"); plan-mode request via experimental `turn/start.collaborationMode` | observed-in-generated-types; live not-observed | **refines** S-2: no native revision identity; DEL-01-03 derives it (S-F-13) |
| P-11 | `thread/start` and `thread/resume` carry `modelProvider`; `modelProvider/capabilities/read` → `{namespaceTools, imageGeneration, webSearch}`; config key `model_provider`; CLI `--oss`, `--local-provider lmstudio|ollama` (TUI/exec surface). Provider definition form and required wire interface (L-2) are **not** in generated types | observed-in-generated-types / published-only; L-2 not-observed | **consistent** with L-1 (per-conversation element present, F-08 confirmed at pin); L-2…L-6 remain not-observed |
| P-12 | `account/login/start` variants `apiKey`, `chatgpt`, `chatgptDeviceCode`, `chatgptAuthTokens`, `amazonBedrock`, `amazonBedrockAccessKeys`; `account/read`, `account/logout`, `account/login/cancel`, `account/gatewayOAuth/*`, TS-only `getAuthStatus`; server request `account/chatgptAuthTokens/refresh`; credential store modes `file`|`keyring`|`auto`|`ephemeral`. Actual storage location: not observed (no sign-in) | observed-in-generated-types | **consistent**; feeds OI-010/OI-009 at DEL-01-05 |
| P-13 | `thread/resume` (rejoins a running thread by id; `excludeTurns`), `thread/read`, `thread/list`, `thread/loaded/list`, `thread/turns/list`, `thread/items/list`, `thread/unsubscribe`; subagent items `collabAgentToolCall` `{tool, status, senderThreadId, receiverThreadIds, prompt, model, reasoningEffort, agentsStates}` and `subAgentActivity` `{kind, agentThreadId, agentPath}`. Post-restart results: not observed | observed-in-generated-types | **consistent**; DEL-01-02/DEL-01-03 inputs |
| P-14 | `CODEX_HOME` honored (echoed as `codexHome`). Written at start: `installation_id`, `state_5.sqlite`, `logs_2.sqlite`, `goals_1.sqlite`, `memories_1.sqlite`, `queue_1.sqlite` (+WAL/SHM), `skills/.system/` (imagegen, openai-docs, plugin-creator, review-agent, skill-creator, skill-installer), `tmp/arg0/…` symlinks (`apply_patch`, `applypatch`, `codex-execve-wrapper` → the binary), `.tmp/plugins*` sync. No `config.toml` created. No `~/.codex` path open. Reads outside `CODEX_HOME`: not observed beyond lsof snapshots | observed | **refines** §7.2 (even `--version` writes to the home, S-F-17) and U-03/OI-009 |
| P-15 | `baseInstructions` and `developerInstructions` on `thread/start` and on `thread/resume` ("Configuration overrides for the resumed thread"); `personality` deprecated. Whether resume overrides apply to an already-loaded thread (v3: 0.154 ignored them — T11): not observed | observed-in-generated-types | **consistent**; open for DEL-02-04 |
| L-4 (§8.1) | Fresh home: network fetch of `github.com/openai/plugins` at start, no sign-in, no turn; warm home: none seen in ~6 s | observed | **changes** the L-4 row from not-observed to observed (S-F-10) |

**Supplement, initial entries.** None. No App-needed field was found absent
from both generator outputs; the gaps found are *between* the generators
(S-F-03) and the `emittedAtMs` envelope element that only TS declares. A
supplement entry needs a recorded live exchange (§7.3), which this spike did
not produce beyond the handshake.

**X-01.** Not recorded as an X-01 fixture: there is no App candidate and no
§7.2 verification step. The transcripts are spike recordings (standing
`recorded`, redacted) of verify-less start/handshake/stop.

## 7. Findings requiring a v0.2 change to HOSTING_BOUNDARY

- **S-F-01 (§7.1, §7.2) Handshake identity.** The initialize response has
  `userAgent`, `codexHome`, `platformFamily`, `platformOs` and no version
  element; the version is embedded in `userAgent` after the client's own name.
  v0.2 should define the handshake-reported identity as these elements and
  state that any version comparison is a parse of `userAgent` text, weaker
  than the label + content check.
- **S-F-02 (§7.1, H1, S-5) Distribution identity and launcher.** Identity
  should cover the vendor tree the supplier executes (codex,
  codex-code-mode-host, rg, bundled zsh/voice resources), and configuration
  identity should record whether the npm wrapper or the vendor binary is
  spawned (the wrapper adds `CODEX_MANAGED_PACKAGE_ROOT`,
  `CODEX_MANAGED_BY_NPM`).
- **S-F-03 (§6.1, §7.3, §9.3) Two generators, two sets.** At one pin, TS has
  5 methods the JSON Schema lacks; the server accepts the TS client set.
  v0.2 must name which output (or union) is the classification and
  conformance reference and put generator kind + variant into the
  generated-schema identity. Choice belongs to the App implementation owner.
- **S-F-04 (§7.3) Supplement role.** `--experimental` now emits experimental
  methods/fields; the supplement narrows to elements absent from the chosen
  generator output (e.g. `emittedAtMs` if JSON Schema is the reference) plus
  a record of the declared opt-in. Experimental status must come from the
  variant diff, not doc comments.
- **S-F-05 (§6.1) Classification depends on declared capabilities.**
  `currentTime/read` exists only with the experimental variant;
  `attestation/generate` is opt-in (`requestAttestation`). The familiar set
  must be (generator variant × capabilities actually declared at handshake).
- **S-F-06 (§4.3, §4.4, §4.5) Supplier descendants.** The supplier spawns
  networked `git` children that outlived its exit. Deliberate stop and
  restart must address the supplier's descendants (process group), and a
  restart may overlap a still-running sync on the same home
  (`.tmp/plugins.sync.lock`).
- **S-F-07 (§4.3, §4.5) Exit status does not distinguish ends.** Stdin close
  and `SIGTERM` both yield exit code 0; "deliberate" must come from the App's
  own stop record, never from exit facts.
- **S-F-08 (§5) Framing facts.** NDJSON confirmed; server frames omit
  `jsonrpc`; notifications carry top-level `emittedAtMs`. The frame parser
  must not require `jsonrpc`, and H6 must treat `emittedAtMs` as native
  content, not boundary envelope metadata.
- **S-F-09 (§4.1, §4.2, H4) Frames during handshaking.** A notification
  arrives with the initialize response, before `initialized`. v0.2 needs a
  rule for delivering or holding frames received in `handshaking`.
- **S-F-10 (§8.1 L-4, priority 3) Network at start.** With a fresh home the
  supplier fetched ≈24 MB from `github.com/openai/plugins` with no sign-in
  or turn. Route to the owner and DEL-01-05; whether a setting disables it was
  not observed.
- **S-F-11 (§6.1 settlement origin, R3, R7, H9, D3)** The supplier has its own
  approval routing (`approvalsReviewer`: `user` | `auto_review` |
  `guardian_subagent`; `item/autoApprovalReview/*` notifications;
  `thread/approveGuardianDeniedAction`; CLI `--approve-for-me`). Under D3 this
  is the user's Codex setting, carried unchanged. v0.2 needs an origin value or
  observation for decisions made inside the supplier, distinct from
  `person-via-interaction` and `app-rule`. A native `timed_out` answer form
  exists (legacy `ReviewDecision`); sending it would be an App rule under U-11,
  never automatic.
- **S-F-12 (§6.2, F-10, U-09)** `serverRequest/resolved` exists; v0.2 can
  name it as the candidate source for `resolved-by-supplier`, with semantics
  still to be observed.
- **S-F-13 (§8 S-2, P-10)** Native plan updates carry the whole plan with no
  revision identity; plan-mode requests are experimental. S-2 should say
  revision identity is derived by DEL-01-03 from turn and item identities.
- **S-F-14 (H7, U-07)** `optOutNotificationMethods` is present in stable
  `initialize` capabilities; the definition's "uses none" choice now has a
  concrete facility to not use.
- **S-F-15 (§9.1 redaction)** The stream carries the host name
  (`serverName`), an installation identifier, and the absolute home path;
  add these to the redaction categories.
- **S-F-16 (R2)** The supplier's own reply to an unknown client method is
  -32600 with the id echoed and the accepted list in the message. v0.1's R2
  names no code. The App's code for unfamiliar *server* requests remains an
  implementation choice.
- **S-F-17 (§7.2, U-03/OI-009)** `codex --version` creates
  `CODEX_HOME/tmp/arg0/…`, so the verification probe writes into the account
  home the child uses.
- **S-F-18 (DEP-005)** At 0.158.0 the supplier labels `app-server`,
  `generate-ts` and `generate-json-schema` `[experimental]` in its own help.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this record |
|---|---|---|---|
| Live behavior of P-08 (error reply to a known request, never-answered), P-09 semantics, P-10 revision request, P-13 post-restart reads, P-15 resume overrides | App implementation owner; live run needs the owner's credential or a qualified local provider (§9.1) | Before settlement fixtures and qualification | Recorded as observed-in-generated-types / not-observed only |
| Reference generator output (TS, JSON Schema or union) for classification and conformance (S-F-03) | App implementation owner | Before R2/R5 implementation | Both committed in part; no reference selected |
| Commit form for `generated/0.158.0/` (deviation from the brief's size rule, §4) | Parent (HELP_HUMAN) with owner | Before commit | RESOLVED by parent re-selection (§4): JSON Schema bundles + manifest + `_spike/` committed; TS regenerated on demand |
| Supplier plugin sync network at start (S-F-10): acceptability under priority 3; whether configurable | Owner with DEL-01-05 | Before local-operation claims | Observed only; no configuration probed |
| Descendant handling on stop/restart (S-F-06) | DEL-01-02 with App implementation owner | Before lifecycle implementation | Observed only |
| Whether `initialized` is required; behavior of a known method before initialize; runtime gating of experimental elements without opt-in | Next spike (App implementation owner) | Before handshake implementation | not-observed |
| Relocatability of the vendor binary apart from its sibling resources | DEL-01-06 | Before packaging | not-observed |
| L-2 wire interface for custom/local providers (not in generated types) | DEL-01-05 | Before provider qualification | not-observed |
| Re-examination of the 0.158.0 pin before implementation (D4) | App implementation owner | Before implementation | Pin is definition/generation basis only |

## Verification cases

Status per case: RUN (in this spike, result shown) or DESIGNED (not run).

| Case | Action | Expected result | Status / result | Serves |
|---|---|---|---|---|
| SV-01 Regeneration determinism | `_spike/generate.sh <scratch>` with the same package; compare per-variant manifests and `MANIFEST.sha256` | All 2,359 lines match; run1 = run2 per variant | RUN: identical (4/4 variants) | VER-002 |
| SV-02 Committed-file integrity | `grep -v '^#' MANIFEST.sha256 \| shasum -a 256 -c` in `generated/0.158.0/` | 1,607 OK; 752 reported missing (omitted JSON Schema files) and no mismatch | RUN: 1,607 OK, 752 missing, 0 mismatched | VER-002 |
| SV-03 Binary identity | `shasum -a 256` of the vendor binary; `codesign --verify` | 788a818f…35c8; valid | RUN: as expected | VER-001, VER-006 |
| SV-04 Handshake reproduction | `node _spike/handshake.mjs <scratch> A bin` on a fresh home | 4-field initialize result; `remoteControl/status/changed`; unknown method → -32600; 2nd init → "Already initialized"; exit 0 on stdin close | RUN: as expected (plus plugin fetch, S-F-10) | VER-001, VER-005 |
| SV-05 Inventory | `python3 _spike/inventory.py` on both schema variants; TS `"method":` count | Counts as §4 | RUN: as §4 | VER-002 |
| SV-06 Live seam set X-02…X-10 at 0.158.0 | HOSTING_BOUNDARY §9.4 captures with an identified candidate | Per §9.4 | DESIGNED (needs owner credential or local provider, and a candidate) | VER-001, VER-003, VER-005, VER-006 |

## Files

- `Design/PIN_SPIKE_0.158.0.md` (this record)
- `Design/generated/0.158.0/MANIFEST.sha256`
- `Design/generated/0.158.0/ts/**`: not committed (parent re-selection, §4); hashed in the manifest
- `Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.schemas.json`, `…v2.schemas.json`
- `Design/generated/0.158.0/_spike/`: `generate.sh`, `handshake.mjs`, `inventory.py`, `redact.py`, `generate.commands.log`, `inventory.txt`, `transcripts/*.jsonl` (8, redacted)
