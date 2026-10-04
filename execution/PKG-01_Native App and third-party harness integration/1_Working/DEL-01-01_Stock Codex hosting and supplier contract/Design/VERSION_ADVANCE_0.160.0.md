# Codex version-advance check 0.158.0 → 0.160.0 (observation record)

- **Contribution:** DEL-01-01/VERSION-ADVANCE-0.160.0-v0.1. **Status:** OBSERVATION RECORD. These are dated observations at one version pair. They do not qualify either version and do not adopt 0.160.0. The pin stays 0.158.0 (D4) until its owner decides otherwise (HOSTING §9.5 step 10).
- **Date:** 2026-10-04, 03:30–04:05 UTC (evening of 2026-10-03, local time). **Node:** VC, a Type 2 TASK of run `APP-V4-DESIGN-PASS-4-20261003`, dispatched by HELP_HUMAN.
- **Authority:** ruling R19-5 (design pass 3) and HOSTING-v0.9 §9.5, "Version-advance check". Owner direction 4 C and the download approval ("yes, download it", naming `codex-0.160.0-darwin-arm64.tgz`) are in this run's `OWNER_DECISIONS.md`. Observation limits are those of OBS-2 and OBS-3 and of the OBS-1 brief §8 stop conditions: no sign-in, no key, scratch `CODEX_HOME`s only, never `~/.codex`, invented material, one model prediction at a time, and S-9 (critical memory pressure) means stop.
- **Basis read (not edited):** `PIN_SPIKE_0.158.0.md`, `OBS_1_0.158.0.md`, `OBS_2_0.158.0.md`, `OBS_3_0.158.0.md`, `HOSTING_BOUNDARY.md` (v0.9) §7, §8.4, §9.5 and §10, and `generated/0.158.0/` (`MANIFEST.sha256` 42b95826…, `_spike/generate.sh`, `_spike/inventory.py`). The harnesses `prototype/obs2/` and `prototype/obs3/` were imported unchanged; their sha256 values match the OBS records (§4.1). The repository was at HEAD `cec590c5c3`. Other nodes edited some Design files during this check. The statement inventory in §7 gives the sha256 of every file at the time it was read.
- **Result in one line:** The download was verified and is the only network use. The 0.160.0 protocol differs from 0.158.0 by **four additive or documentation-only changes** and nothing else: every method, notification, server request, stable/experimental split and deprecation is the same. Every rerun observation (O-1, O-2, O-3, O-5, O-5b, O-6, O-7 with plugins off, O-8, W-1…W-6, W-2b, W-6b, and the handshake) gave the **same mechanism** as at 0.158.0, with two exceptions. First, a fork's first turn **no longer gets a fresh environment context**. Second, the bundled system skill `plugin-creator` **is gone**. The 9B local model's adherence varied from run to run (§5.4). **No design decision changes.** One wording (NIR `Turn.error`) and the identity values in HOSTING §7.1 would need updating if the pin moved.

**Redaction (HOSTING §9.1; as OBS-2 and OBS-3).** `<session scratchpad>/` is the session scratchpad, whose path contains the user name. `<OBS>` is `<session scratchpad>/codex-0.160.0/obs`, `<V>` is the 0.160.0 vendor binary, `~/` is the home folder, and `$TMPDIR` is the per-user temporary folder that holds the 0.158.0 raw logs (read only here). Left out: the host name (`serverName`), installation identifiers and the host's time zone. Thread and turn identifiers are kept because they name invented scratch threads. The raw logs stay unredacted in `<OBS>/logs` and `<OBS>/homes`.

## 1. Download and distribution identity (HOSTING §9.5 step 2; §7.1)

| Item | 0.160.0 (this node) | 0.158.0 (PIN_SPIKE §3) |
|---|---|---|
| File | `codex-0.160.0-darwin-arm64.tgz` from `https://registry.npmjs.org/@openai/codex/-/codex-0.160.0-darwin-arm64.tgz` (`curl -f`, HTTP 200, 134,311,083 B, 03:30:47–03:30:50 UTC) into `<session scratchpad>/codex-0.160.0/` | npm install of `@openai/codex@0.158.0` (wrapper + platform package) |
| Registry check **before extraction** | `shasum -a 1` = `f78898f04bc6989ab371de42b6acdbf56b54dc9c` (= dist.shasum); `sha512-` + base64(`openssl dgst -sha512 -binary`) = `sha512-aefV6cqZA2REZgR//4McyXlp7zLcTti4CI2v3j9IVgNndPBv2kCeNEcz07qeelXcwOdSFPUKb6roA48vZmDgrQ==` (= dist.integrity). **Both equal**; then `tar -xzf` into `<session scratchpad>/codex-0.160.0/pkg/` (318 MB) | integrity `sha512-0OKSjlWY…ZyQLg==` |
| Package | `package.json` name `@openai/codex`, version `0.160.0-darwin-arm64`, licence Apache-2.0; no npm wrapper (only the platform tarball was approved) | wrapper `bin/codex.js` + platform package |
| `codex-package.json` | version 0.160.0, target `aarch64-apple-darwin`, entrypoint `bin/codex`, layoutVersion 1 | same shape |
| Version label | `codex-cli 0.160.0` | `codex-cli 0.158.0` |
| `bin/codex` | sha256 `112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b`, 241,555,024 B | `788a818f…35c8`, 239,662,592 B |
| Siblings | `bin/codex-code-mode-host` `679eedae…a65a`; `codex-path/rg` `7c7d5b09…739b`; `codex-resources/zsh/bin/zsh` `d715e06e…3b15`; `codex-resources/voice/…` | `d47e28a8…`, `e04d4533…`; same composition |
| Signing | `codesign --verify`: valid on disk, satisfies its Designated Requirement; Developer ID Application: OpenAI OpCo, LLC (2DC432GLL2); hardened runtime; timestamp Oct 1, 2026 | same signer and flags; Sep 27, 2026 |
| Help pages | `--help`, `app-server --help` and `app-server generate-ts --help` are byte-identical to 0.158.0's (`diff`). `app-server`, `generate-ts`, `generate-json-schema` and `remote-control` are still labelled `[experimental]` (S-F-18) | — |
| Nothing installed | no npm install, no global prefix; every run used `CODEX_HOME` under `<session scratchpad>/codex-0.160.0/` | — |

**Distribution identity (S-F-02, HOSTING §7.1):** the structure is unchanged (the same executed vendor tree) and every value changed.

## 2. Generation at 0.160.0 (HOSTING §9.5 step 3)

**Method.** This is `_spike/generate.sh` (0.158.0) run as `<session scratchpad>/codex-0.160.0/generate.sh`: both generators, both variants, each twice, no `--prettier`, per-file sha256 manifests compared between runs. There are two stated differences. (a) The vendor binary is run directly, because there is no npm wrapper. (b) `CODEX_HOME` holds a `config.toml` with `[features] plugins = false` and `[analytics] enabled = false`, so that a fresh home makes no start-up connection (OBS-2 O-7). A network watch (`lsof -i` on the generator processes every 100 ms) saw no socket.

**Equivalence check of the method.** The same script with the same home configuration, run with the **0.158.0** vendor binary, reproduced all four 0.158.0 per-variant manifests exactly (5606da9a…, 9929458e…, f4901c6a…, 95942cbe…). Its combined manifest body (2,359 lines) equals the committed `generated/0.158.0/MANIFEST.sha256` body line for line. The two deviations therefore do not change generator output.

| Variant | Files | Bytes | Determinism (run1 = run2) | Per-variant manifest sha256 |
|---|---|---|---|---|
| TS stable | 734 (+2) | 428,142 | identical | `afa54a7da0d1a12005b74d7980218ec6312eb1e101e49b05156546addf124b00` |
| TS experimental | 875 (+2) | 517,838 | identical | `79a27ed3dcd85729525bb8830a7a95b8cf2efa57ededc5d255b0345355f56420` |
| JSON Schema stable | 314 (=) | 3,540,819 | identical | `534d1246b1a6450cfe91391de982f2f77668bf5874c8debc7c62757c06941545` |
| JSON Schema experimental | 440 (=) | 4,286,533 | identical | `207b1fafe328b999baa46d5dc55961cb07a377fffe127fbdadf6a4996e8430b4` |

Combined `MANIFEST.sha256` in the 0.158.0 format: 2,363 file lines, sha256 `ef47ec4e1d85552e076bc1a875909f2cd9f3240299ed772745cd5287410d3f37`; body without header `5cfd4a73ac333cab…`. The experimental bundles are `codex_app_server_protocol.schemas.json` `7243ba241962af92…` (863,788 B; 0.158.0 `aa5cb3fb…`) and `codex_app_server_protocol.v2.schemas.json` `e77b7d1436a78f43…` (751,818 B; 0.158.0 `34f28a48…`). Everything is in `<session scratchpad>/codex-0.160.0/gen/` (`commands.log`, `run{1,2}.sha256`, `inventory.txt`) and nothing is committed. If 0.160.0 were adopted, a `generated/0.160.0/` committed form would be a new decision for the parent, as at 0.158.0.

## 3. Protocol comparison 0.158.0 → 0.160.0 (HOSTING §9.5 step 4)

### 3.1 Method sets and stable/experimental split: unchanged

- `_spike/inventory.py` run on the 0.160.0 JSON Schema variants gives output **byte-identical** to the 0.158.0 `_spike/inventory.txt` (`diff`). The figures: client requests 104 stable / 167 experimental (63 experimental-only); client notifications 1/1; server requests 10/11 (`currentTime/read` experimental-only); server notifications 83/83.
- TS `"method"` literals: client 107 / 170, server requests 10 / 11, server notifications 85 / 85, all equal to 0.158.0. The five TS-only elements (`getAuthStatus`, `getConversationSummary`, `gitDiffToRemote`, `rawResponse/completed`, `rawResponseItem/completed`) are still absent from JSON Schema. The generator divergence (S-F-03) is unchanged.
- The running server's accepted-method list, read from its unknown-method error, still names **170** methods (§4.3).
- The stable↔experimental TS split, as `diff -rq` between the two variants, has the same 163 entries at both versions (`diff` of the two listings: identical). Experimental status moved for no element.
- Deprecations: no `deprecated` text or field changed. The structural diff below covers every description string. At run time the same two `deprecationNotice` texts (full-history hydration) and the same model-metadata `warning` were emitted (§5).

### 3.2 Every change (structural JSON diff of all 314 + 440 schema files; TS diff of all 734 + 875 files)

| # | Element | 0.158.0 | 0.160.0 | Kind | Seams that consume it (§9.5 "consumed") |
|---|---|---|---|---|---|
| Δ1 | `ThreadItemsListParams.cursor` (`thread/items/list`, stable) | `string \| null`, "Opaque cursor to pass to the next call to continue after the last item." | `ThreadItemsListCursor \| null`, where the new type `ThreadItemsListCursor = string \| ThreadItemsListAnchor` and `ThreadItemsListAnchor = {type: "item", itemId}`: "Opaque continuation cursor or an exclusive item anchor in the requested visible turn. An item anchor requires a non-empty `turnId`; ascending … returns items after it, and descending … before it. Continue with the returned string cursor." Two new TS files | additive widening | **consumed**: WR SC-3, RECOVERY R-4/§9, NPTD SQ-1, EXEC A-3/VC-E-18 (they page with the returned `nextCursor`, which is unchanged; the anchor is a new option) |
| Δ2 | `ListMcpServerStatusParams.serverName` (`mcpServerStatus/list`, stable) | absent | optional `string \| null`: "Limit discovery to one server. With a thread ID, reuse that thread's MCP connection." | additive field | **consumed**: HOSTING §6.8/HCG-A05, ADAPTER channel state, EXEC `mcp-tool-call` presence reading, WD `mcp-tool-call` (none requires it) |
| Δ3 | `Turn.error` description | "Only populated when the Turn's status is failed." | "Error associated with a failed or interrupted turn." | documentation only (type unchanged) | **consumed**: NIR §4 (L396 "`Turn.error` only when failed"); RECOVERY outcome reading. Observed at 0.160.0: every interrupted turn (O-1, O-2 ×2, O-3, and the `cancel` decline) still had `error: null` |
| Δ4 | `CodexErrorInfo` enum | … `misalignmentPolicyViolation` | + `"tooManyDenials"` | additive enum value | **not consumed** by name in any Design file (grep). Receivers that render `codexErrorInfo` must accept unknown values, which they already do by the H-rules |

Δ3 and Δ4 appear in 17–20 schema files each, because `Turn` and `CodexErrorInfo` are embedded in many response and notification definitions. Those files differ only by these strings. No other path differs in any file.

**Focus surfaces checked by name in the 0.160.0 types (all identical to 0.158.0 by the diff above):** `thread/start` (stable `baseInstructions`, `developerInstructions`; experimental `dynamicTools`, `historyMode`, `multiAgentMode`); `turn/start` (experimental `collaborationMode`, `multiAgentMode`, `additionalContext`); `thread/resume` (`developerInstructions`, `excludeTurns`; experimental `initialTurnsPage`); `thread/fork` (`developerInstructions`, `excludeTurns`); `UserInput` types `text`, `image`, `localImage`, `audio`, `localAudio`, `skill`, `mention`; `account/login/start` variants `apiKey`, `chatgpt`, `chatgptDeviceCode`, `chatgptAuthTokens`, `amazonBedrock`, `amazonBedrockAccessKeys`; server request `account/chatgptAuthTokens/refresh`; `skills/list`, `skills/extraRoots/set`, `skills/config/write` (stable); `thread/items/list` (stable, Δ1); experimental-only `collaborationMode/list`, `thread/settings/update`, `turn/settings/update`, `remoteControl/*` (enable, disable, status/read, pairing/*, client/*), `plugin/search`; stable `plugin/*` and `marketplace/*`.

### 3.3 Non-protocol differences found

| Item | 0.158.0 | 0.160.0 | How checked |
|---|---|---|---|
| Feature flags (`codex features list`; `experimentalFeature/list`) | 151 flags | the same plus three `under development`, default **off**: `guardian_conversation_history_tools`, `guardian_root_handoff_context`, `instant_interrupt`. `plugins` (stable, default on), `multi_agent` (stable, on), `multi_agent_v2` (stable, off), `apps`, `remote_plugin`, `tool_suggest` (stable, on), `collaboration_modes` and `remote_control` (`removed`) unchanged | `diff` of the two listings |
| Bundled system skills (`skills/.system`) | imagegen, openai-docs, **plugin-creator**, review-agent, skill-creator, skill-installer | the same **without `plugin-creator`** (the binary no longer contains the string: `strings` count 15 → 0) | home listing, `skills/list`, binary strings |
| Base instructions; built-in Plan Mode and Default mode texts; permissions block; request body keys; `x-codex-*` header names (incl. `x-codex-beta-features: remote_compaction_v2`) | — | **identical** (sha256 of every distinct value in the provider-tap captures, 0.158.0 vs 0.160.0) | tap logs |
| Rollout record kinds (O-2 thread) | — | identical set (`session_meta`, `turn_context`, `world_state`, `response_item`, `event_msg` kinds, `token_usage_record`) | rollout files |
| `codex --version` side effect (S-F-17) | writes `CODEX_HOME/tmp/arg0` | the same (`tmp/` created) | home listing |

### 3.4 Recordings against the new reference (HOSTING §9.5 step 6)

This was checked with the DEL-01-01 prototype validator `jsonschema_subset.py` (unchanged) against the definitions `ServerNotification` and `ServerRequest` of both experimental bundles. **All 2,781 notifications and 4 server requests** in the 0.158.0 OBS-1/OBS-2/OBS-3 raw frame logs (`$TMPDIR/chirality-obs{1,2,3}-0.158.0`, read only) are valid against 0.158.0 and against 0.160.0. All 2,398 notifications and 3 server requests recorded at 0.160.0 in §4 are valid against both. The supplement stays empty (§9.5 step 5): no App-needed element appeared in or disappeared from either generator.

## 4. Observation reruns at 0.160.0 (HOSTING §9.5 step 7, limited)

### 4.1 Set-up

| Item | Value |
|---|---|
| Codex | `<V>` = `<session scratchpad>/codex-0.160.0/pkg/package/vendor/aarch64-apple-darwin/bin/codex`, run directly (sha256 §1) |
| LM Studio | app 0.4.16+2, CLI commit efce996 (the same as OBS-2 and OBS-3). The server was **OFF**; this node started it at 03:37:39 UTC and stopped it at 03:56:09 |
| Model | `qwen/qwen3.5-9b` (installed; nothing downloaded), loaded with `--context-length 24576 --parallel 1` (one prediction at a time), 5.57 GiB, in 11.6 s; unloaded at 03:56:07 |
| Harnesses (unchanged, sha256) | `obs2/obs2_harness.py` `589a9d703a73…`, `obs2/obs2_provider_tap.py` `b316815fc1cb…`, `obs3/obs3_harness.py` `cbf96655a80b…`, `obs3/obs3_provider_tap.py` `c25d6cb3f72c…`, `obs1/download_watch.sh` `79436fce9ffb…`. The OBS-2 CLI test tool is a scratch copy of `prototype/obs1_cli_tool.py` (`c27dc227c2f3…`) |
| Wrapper (new) | `prototype/version_advance/va_harness.py` (sha256 `fbe61c7272ca452cf75ceab930adb01fb2b162a394a808bf7b34b7b4f0fb98e8`). It imports both harnesses without editing them and changes four things at run time: (1) every home is cold (no OBS-1b plugin-cache template); (2) a session whose `config.toml` lacks `plugins = false` is launched with `-c features.plugins=false` (OBS-3 homes and the O-7 variants carry it in `config.toml` already); (3) a `git` process in a Codex process group ends that group, and **any** non-loopback socket from a Codex group stops the scenario (S-5 widened to all times); (4) O-7 runs only the variants with `plugins = false`. Everything else is the OBS-2/OBS-3 code |
| Provider path | O-1, O-2, O-3: Codex → LM Studio 127.0.0.1:1234 directly. O-5, O-8: through `obs2_provider_tap.py` on 127.0.0.1:12340 (pass-through). OBS-3 scenarios: through `obs3_provider_tap.py` on 127.0.0.1:12350 (pass-through, or capture-only while the flag file exists) |
| Homes | 38 Codex sessions, every one with `CODEX_HOME=<OBS>/homes/<name>` (reported `codexHome` = the scratch home every time, S-1). No `auth.json` anywhere, no `account/*` server request, no API key. `~/.codex` was never opened (S-6: 1,275 snapshots, none) |
| Watches | `download_watch.sh` 03:34–03:56 UTC: 963 lines, **0 S-2**. All are NET lines from LM Studio's own `lmlink-connector`, as in OBS-2 and OBS-3. The models folder and `lms ls --json` were identical before and after. Memory pressure was sampled every 250 ms inside every scenario |

### 4.2 Timeline (UTC, 2026-10-04)

| Time | Scenario | Model predictions |
|---|---|---|
| 03:34:23 | probe (features, config/read, account/read, remoteControl/status/read, collaborationMode/list) | 0 |
| 03:34:47–03:36:10 | O-7 v1, v6, v7, v8 (20 s idle each) | 0 |
| 03:36:10–03:37:18 | O-6 M0…M5 | 0 |
| 03:37:39–03:37:51 | `lms server start`; `lms load …` (memory pressure **4** for three 1-s samples right after the load, then 2; no Codex process was running; D-1) | — |
| 03:38:22–03:42:55 | O-1; O-3; O-2 with stdin stop; O-2 with SIGKILL | 1; 1; 1; 1 |
| 03:43:19–03:45:58 | O-5 (tap); O-8 (tap) | 3; 3 |
| 03:46:31–03:48:02 | OBS-3 `capture`, `capture2`, `capture` again under the non-canonical path spelling (D-3) | 0 (capture-only) |
| 03:48:10–03:52:50 | `w12` (W-1, W-2); `w34` (W-3, W-4); `w6`; `w5`; `supp` (W-2b, W-6b) | 4; 2; 2; 3; 0 |
| 03:54:01–03:55:56 | second samples: `w12`, `w5` (D-4) | 4; 3 |
| 03:56:07–03:56:09 | taps, log stream and watch stopped; `lms unload --all`; `lms server stop` | — |

**Model calls:** 28 `POST /v1/responses` in LM Studio's server log, one prediction each and strictly one at a time. 54 capture-only requests (HTTP 400) made no model call. **Stop conditions:** no S-1…S-9, S-10 or S-11 stop was triggered by Codex. The harness's one `S-11` is O-6 M3, Codex's refusal of `--profile` for `app-server`, which is that case's result as at 0.158.0. S-9 did not fire inside any scenario (D-1). **Clean-up:** afterwards `pgrep` found no Codex process of this node, no tap, no `lms log stream` and no watch, and `lms status` reported OFF. The person's own Codex desktop processes were running throughout and were not touched.

### 4.3 Handshake and exit (PIN_SPIKE §5; scratch script `handshake_check.py`, fresh homes, plugins off)

The `initialize` response has the same four fields (`userAgent` = `chirality-vc/0.160.0 (Mac OS 26.6.2; arm64) unknown (chirality-vc; 0.0.0-vc)`, `codexHome`, `platformFamily`, `platformOs`), still with **no version element** (S-F-01). `remoteControl/status/changed` `disabled` arrives with the response, before `initialized` (S-F-09). An unknown client method gives **-32600**, echoes the id and lists **170** accepted methods, before or after `initialize` (S-F-16). A second `initialize` gives -32600 "Already initialized". Server frames omit `jsonrpc`; notifications carry `emittedAtMs` (S-F-08). Exit is code 0 in 4.6 ms on stdin close and code 0 in 4.6 ms on SIGTERM (S-F-07). stderr is 0 bytes. **All unchanged.**

### 4.4 Item results (0.158.0 record → 0.160.0)

| Item | 0.158.0 (record) | 0.160.0 (this node) | Same? |
|---|---|---|---|
| **O-1** interrupt | `{}` in ≈21 ms; `turn/completed` `interrupted`, error null; the open reasoning item never completes and is not in history | `{}` in 112 ms; then `thread/status/changed` idle and `turn/completed` `interrupted`, `error: null`, itemsView `notLoaded`; reasoning item `rs_…` started and **never completed**; `thread/read` and `thread/turns/list`: the turn holds only `userMessage` | **same** (slower response, one sample) |
| **O-2** stop with live turn and pending approval; restart; resume | Not re-raised; `interrupted` after both stdin stop and kill; graceful stop writes `<turn_aborted>` note; kill writes nothing | stdin: exit 0 in 70 ms; rollout gains `function_call_output` "aborted by user", the `<turn_aborted>` user message and `turn_aborted`. Kill: signal 9 in 9.8 ms; the rollout ends at the `function_call`. Both read back `notLoaded` then `interrupted` (userMessage, reasoning, agentMessage); resume: `idle`, approvalPolicy `untrusted`, no server request, no model request; `deprecationNotice`, `thread/goal/cleared` as before; `thread/loaded/list` the thread | **same** |
| **O-3** request resolved by the supplier | `turn/completed` `interrupted`, then `serverRequest/resolved {threadId, requestId 0}`; a late answer is ignored; the command item never completes and is not in history | the same order (resolved 0.1 ms after `turn/completed`); late `cancel` ignored (nothing in 4 s); `commandExecution` started, never completed, absent from `thread/read`. `availableDecisions` = `accept`, `{acceptWithExecpolicyAmendment}`, `cancel` (as OBS-1b and OBS-2) | **same** |
| **O-5** `thread/resume` + new `developerInstructions` | Accepted, ignored, loaded or not; nothing reports it | Both resumes are error-free with an **identical response shape** (result and thread keys equal to 0.158.0's); all three provider requests carry **ALPHA-7 only**; BRAVO/CHARLIE appear nowhere in the tap or the home; replies "Hello! ALPHA" | **same** |
| **O-5b** `collaborationMode.settings.developer_instructions` on `turn/start` | Added as a `<collaboration_mode>` developer message; reply ended "DELTA" | The same developer-message layout, identical to 0.158.0's (role text, …, Plan Mode block, DELTA-7 block); reply "Hello! How can I help you today?" (**did not follow DELTA**) | mechanism **same**; compliance differed (D-4) |
| **O-6** configuration sharing | M1 symlink works (user layer named by B's path, A's content); M2 `-c` works (sessionFlags); M3 `--profile` refused at launch; M4/M5 indistinguishable without a credential; A's file unchanged | All the same. A's `config.toml` sha256 `7536731d…` before and after. M3 is refused with the same message (exit 1). Every case shows an extra `sessionFlags` entry `features.plugins = false` from the wrapper (D-2) | **same** |
| **O-7** start-up traffic, plugins off (v1, v6, v7, v8) | No connection; `git` none; remote-control loop "waiting … until authentication" once a second, stopped only by `CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED=1` (v7: 17 log rows) | **No non-loopback socket**, no `git`, no `.tmp/` in any variant. The log has the loop started for the ChatGPT backend URL and 20 × "waiting to resolve remote control preference until authentication is available" in 20 s (v1, v6, v8). v7: 17 log rows, loop started Disabled. `remoteControl/status/changed` `disabled` | **same** |
| O-7 baseline (v0, v2…v5, plugins on) | featured-plugins request to the ChatGPT backend (401), `git ls-remote`/fetch from github.com | **not run**: it would make network connections outside the one approved download | not re-checked |
| **O-8** plan mode | `collaborationMode/list` Plan/Default; one `plan` item `<turnId>-plan` via `item/plan/delta`, no agentMessage, no `turn/plan/updated`; persists; role text sent beside it | The same: list `Plan` (medium) and `Default`; `plan` item `…-plan` via 177 `item/plan/delta`; no agentMessage, no `turn/plan/updated`; turn 2 "I am in **Plan Mode**."; tool list identical (incl. namespace `multi_agent_v1`) | **same** |
| O-4/O-4a/O-4b delegation | Stock: not provoked (delegation tools only in a `namespace` tool, dropped by LM Studio); observed through the OBS-2 adapter | Not rerun. Re-observed: the delegation tools still travel only in namespace `multi_agent_v1` (O-8 tool list), and LM Studio 0.4.16+2 logged "Ignoring unsupported tool type(s): namespace." 28 times. The stock "not provoked" condition therefore holds | **not re-checked** (behaviour through the adapter) |
| **W-1** `skill` input | Honoured only for a discovered skill at its **canonical** path: a separate user message `<skill><name/><path/>bytes</skill>`; everything else accepted and silently ignored | The same in all 23 capture variants. c10/c11 with the non-canonical spelling: ignored; r5/r6 canonical: injected; r8 wrong name: injected with the real name; r7 `$name` text mention: injected; r10 skill-only: empty user message then `<skill>` (D-3). Real: run 1 t1 "Hello!" (**marker missing**), t2 "[WF-A] …"; run 2 t1 "[WF-A] Hello!", t2 "[WF-A] …" | mechanism **same**; compliance 3/4 (0.158.0: 2/2) |
| **W-2** chaining | All injections stay in history; B follows the "run A ended" line; followed B, dropped A (2/2) | The same input layout; "[WF-B] Hello!" and "[WF-B] …" in both runs (4/4) | **same** |
| **W-2b** | Extra root lost on restart; recorded bytes replayed; a new skill input injects the changed file | The same (b1…b4 identical in shape) | **same** |
| **W-3** `mention` | Accepted, nothing reaches the model | The same (c7, c8, r3, r4, r9); real reply did not follow A | **same** |
| **W-4** text bytes | Followed B; full bytes in `thread/read` | The same; "[WF-B] Hello!" | **same** |
| **W-5** `thread/settings/update` (experimental) | `<collaboration_mode>` developer message appended per change; persists across turns and restart; replaces plan text; null restores it; followed A then B (3/3) | Mechanism identical: same layouts, resume reports `collaborationMode` default with B, and u5/u6/u7 give the same last developer message as 0.158.0. Replies: run 1 A, **A**, **A**; run 2 A, (none), B | mechanism **same**; compliance 3/6 (D-4) |
| **W-6** `thread/fork` + `developerInstructions` | Accepted, ignored (also `config.developer_instructions`); copies the source's developer text and history with the same turn ids; `forkedFromId` in the fork response and `thread/read`, null in `thread/list`; history referenced from the source's rollout (`forked_from_id`, `forked_from_ordinal_exclusive` 15); fork's first request adds a **fresh `<environment_context>`** | All the same (ROLE TWO nowhere in w6; `forked_from_ordinal_exclusive` 15; `thread/list` `forkedFromId` null), **except that the fork's first request no longer carries a fresh `<environment_context>` user message**. Requests have three user rows where 0.158.0 had four; the copied history still holds the source's environment context. The not-loaded-source fork (fu1) keeps its four rows | **changed (detail)** |
| **W-6b** | `config.developer_instructions` ignored; fork + `thread/settings/update` adds ROLE TWO as `<collaboration_mode>` | The same (ROLE TWO only in the c2 request); the fork requests lack the fresh environment context as in W-6 | same apart from W-6's detail |
| Content sent to the model (OBS-3 §9) | Base instructions, developer text, skills block, permissions block, `<environment_context>`; `client_metadata` with installation id | The same, except that the skills block lists five system skills (`plugin-creator` gone, §3.3) | **changed (detail)** |

## 5. Deviations and notes

| Id | Record |
|---|---|
| D-1 (S-9) | Right after the model load (03:37:51–53 UTC), before any Codex process, three 1-second samples of `kern.memorystatus_vm_pressure_level` read **4**, then 2. This is the pattern OBS-2 recorded as its D-1, and the run went ahead as OBS-2's did. Inside every scenario the harnesses sampled every 250 ms and never read 4; the level was 1 at the end of each model scenario. HELP_HUMAN may judge whether going ahead after a post-load reading of 4 was within the brief |
| D-2 | The wrapper's changes (§4.1): cold homes, `-c features.plugins=false` where needed, wider guards, and O-7 limited to the plugins-off variants. The O-7 baseline and the variants that leave plugins on were not run because they contact the ChatGPT backend and github.com. The OBS-2 tool-list captures (`tools`) and O-4 were not in the brief's list and were not run |
| D-3 | The scratch folder is already in canonical form (`/private/tmp/…`), unlike `$TMPDIR` (`/var/folders` → `/private/var/folders`). The first `capture` pass therefore gave c10/c11 canonical paths, and Codex injected them. To test the non-canonical case, `capture` was rerun with `--obs` spelled through the `/tmp` link to the same folder (suffix `-nc`): c10/c11 were then ignored, as at 0.158.0. Both result files are kept (`capture_result.canonical-obs.json`, `capture_result.noncanonical-obs.json`) |
| D-4 | Model adherence (not a version fact). The provider requests of W-1, W-5 and O-5b are structurally identical to 0.158.0's (base instructions, developer messages and injected blocks have equal sha256 after path normalisation). Yet replies varied: W-1 t1 missed `[WF-A]` once in two runs; W-5 followed the latest text 3 times in 6 (0.158.0: 3/3); O-5b did not end with DELTA. Second samples of `w12` and `w5` were taken to show the variance. Six of the 28 predictions were these extra samples |
| D-5 | The model inputs at this node carry `<OBS>` paths, and because `<OBS>` is under the session scratchpad, those paths contain the user name. This affects `<environment_context>`, skill paths and the skills block. They reached only the local loopback provider; no non-loopback socket was opened by any Codex process group. No `~/` path appeared. This differs from OBS-3 §9 only because the brief puts the scratch folder there |
| D-6 | The 0.158.0 raw logs under `$TMPDIR/chirality-obs{1,2,3}-0.158.0` were read (never written) for the comparisons in §3.4, §4.4 and D-4 |

## 6. Effect on design decisions

**No design decision changes at 0.160.0.** Every behaviour a design rests on was observed again with the same mechanism, or is unchanged in the generated types. The differences bear on designs as follows.

1. **Pin identity values (HOSTING §7.1 L1107, L1108, L1113; VC-07 L2199; NPTD L459 "manifest 42b95826…").** These are values, not rules. If the owner advanced the pin, they would be replaced by §1 and §2's values, and a `generated/0.160.0/` committed form would be chosen. The identity rules themselves (vendor tree, launcher, generator kind and variant, `userAgent` as the only version carrier) hold unchanged.
2. **`Turn.error` (NIR L396, "only when failed"; Δ3).** The generated documentation now allows an error on an interrupted turn. No interrupted turn here carried one. NIR's wording should become "on a failed turn, and possibly on an interrupted one", with a defence for an interrupted turn that has an error. RECOVERY already reads the status, not the error, so its outcome causes are unaffected.
3. **`thread/items/list` item anchor (Δ1).** This adds an option. WR SC-3, RECOVERY R-4 and NPTD SQ-1 page with the returned string cursor, which still works unchanged. An anchor could let SC-3 read "items after the supplied user message" directly. That is an optional refinement for DEL-02-02 and DEL-01-02, not a needed change.
4. **`mcpServerStatus/list` `serverName` (Δ2).** This adds an option for ADAPTER's channel-state read of one server. Nothing requires it.
5. **Fork without a fresh environment context (W-6).** ROLE's fork-as-role-copy and RECOVERY's `forkedFrom` rest on "developer text and history copied; new `developerInstructions` ignored", which is unchanged. No design relies on the fork getting a fresh environment context. The fork now runs with the source's working-directory context as copied, which matters only if an App fork changed `cwd` (no design does).
6. **`plugin-creator` gone from system skills.** No design names it. The skills block every request carries is one entry shorter.
7. **Adherence variance (D-4).** The designs supply a workflow as a text element of the turn that starts the run, with an "ended" line when chaining (R19-1, R19-7). They do not use `thread/settings/update` or `collaborationMode` developer text for workflows. The W-2/W-4 route they depend on was followed in every sample (6/6). The W-5 variance supports the existing choice not to rely on `thread/settings/update`.
8. **Not re-checked, and why** (§7 lists every affected statement): the delegation run through the OBS-2 adapter (O-4/O-4a/O-4b); the OBS-1 MCP route (A-1…A-7, OB-10, L-3); OBS-1b's answer-to-`serverRequest/resolved` timing (OB-4); the plugins-on start-up traffic and fetch (S-F-10, L-4, O-7 v0); and supplier descendants (S-F-06, H11). With plugins off no `git` child arises, and no descendant survived any exit here. None of these was in the brief's required list. The baseline-traffic items would need network the brief does not allow.

## 7. Statements that name 0.158.0 or rest on a 0.158.0 fact

**Method.** Every Markdown file under `execution/**/Design/` (42 files hold such statements) was split into statement units: one table row, one paragraph or list item, or one code block. A unit was selected if it names `0.158`, cites `OBS-1`/`OBS-1b`/`OBS-2`/`OBS-3`, `PIN_SPIKE`/`SPIKE §`, an `S-F-n` finding or an `OB-`/`OB2-`/`OB3-` label, or says `observed-in-generated-types` or "generated types". This gave **962 units**. Each unit was matched against the facts it rests on (legend below), and its verdict is the weakest of its facts. Rule hits were checked by hand for every *changed* unit and for the Δ1–Δ4 surfaces (grep for `items/list`, `cursor`, `mcpServerStatus`, `Turn.error`, `CodexErrorInfo`, `plugin-creator`, `environment_context`, identity values). The file sha256 values were taken at 04:04 UTC and were unchanged across the extraction. Line numbers refer to those revisions. The scripts and the per-unit JSON are in `<session scratchpad>/codex-0.160.0/stmts/` (`units.py`, `classify.py`, `verdict.py`, `rows.json`).

**Verdicts:** *changed* (how, given per unit); *not re-checked* (why, given per unit); *partly not re-checked* (the unit also rests on an unchanged fact; the item not re-checked is named); *unchanged+* (unchanged, and 0.160.0 adds an option: Δ1 or Δ2); *unchanged* (the fact was re-observed or the generated types are identical); *names the pin or a record only* (a pin label, a heading, a record or basis citation by hash, or a dated 0.158.0 record line whose truth as a record is unaffected).

**Facts (legend; status at 0.160.0):** F02 distribution identity: structure unchanged, values changed. F03 generated-output identity: values changed. F04 method inventory and generator divergence: unchanged. F05 `thread/items/list`/cursors: unchanged+ (Δ1). F06 `mcpServerStatus/list`: unchanged+ (Δ2). F07 `Turn.error`: changed doc (Δ3). F09 handshake, framing, exit: unchanged. F10 start-up network: plugins-off half unchanged, plugins-on half not re-checked. F11 descendants: not re-checked. F12 remote-control loop: unchanged. F13 O-1, F14 O-2, F15 O-3: unchanged. F16 delegation: types and features unchanged; adapter run not re-checked. F17 O-5, F18 O-5b/W-5 (mechanism), F19 O-6, F20 O-8, F21 W-1/W-2/W-2b, F22 W-3, F23 W-4: unchanged. F24 W-6: unchanged except the fresh environment context. F25 content sent: unchanged except the system-skill list. F26 MCP: types unchanged; OBS-1 live route not re-checked. F27 item order and `phase` null (OBS-1 O-5/O-6): unchanged (re-observed in O-5 frames). F28 OBS-1b approval facts: unchanged (O-2/O-3), except OB-4 timing, which was not re-checked. F29 local provider route (L-2, Responses, LM Studio): unchanged. F30 other generated-type facts: unchanged. F32 model adherence: re-observed, more variance (D-4).

**Totals (962 units):** changed 22 · not re-checked 43 · partly not re-checked 174 · unchanged+ 18 · unchanged 523 · names the pin or a record only 182.

**The 22 *changed* units, by substance:**
- *Identity values*: HOSTING L1107 (`codex-cli 0.158.0` → `codex-cli 0.160.0`), L1108 (vendor-tree sha256 values; same composition), L1113, L1143–1152, L216, L2199 (0.158.0 generated-output identities and committed form; 0.160.0 output differs); NPTD L459 (version-line text names manifest 42b95826…); COMMITTED_STATE L5. The dated records PIN_SPIKE (L58, L73, L74, L101, L192, L339), OBS_1 (L14, L15, L273), OBS_2 (L14, L15) and OBS_3 (L14) state the 0.158.0 binary, `userAgent` and package values. They stay true as records; at 0.160.0 the values differ.
- *Behaviour*: OBS_3 L191 (W-6 findings: "adds a fresh environment context": no longer at 0.160.0).
- *Documentation*: NIR L396 (`Turn.error` "only when failed": now "failed or interrupted"; observed still null on interrupt).

### 7.1 Per-file inventory

Units are given by their start line, or by a line range. For each file: sha256 at inventory time, unit counts, then the units under each verdict.
- **Note (pass-4 closeout C2; R23-29 item 3):** the sha256 values below hash the working-tree bytes as read at 04:04 UTC; six of them (AAC `eca9a079…`, ACT `e5bf830c…`, RS `1068e295…`, EXP `dc6b6a0c…`, LHQ `2668d955…`, TOP `cf0b65f2…`) are held by no commit and cannot be re-verified from git; the current versions of these files are named under the R23 rulings (`R23_RESOLUTIONS.md` of run `APP-V4-DESIGN-PASS-4-20261003`: R23-17, R23-21, R23-23), not here.

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md`** (sha256 `ce235650e8a9494c…`;261 units: changed 6, not re-checked 9, partly not re-checked 51, unchanged+ 4, unchanged 153, names the pin or a record only 38)
- *changed:* L216 (0.158.0 generated-output identity; 0.160.0 output identity differs (§3.1)); L1107 (0.160.0 reports `codex-cli 0.160.0`); L1108 (new per-file identities (bin/codex 112fae7a…1b4b, 241,555,024 B); same composition of the vendor tree); L1113 (new generated-output identities (VERSION_ADVANCE §3.1); same shape); L1143–1152 (0.158.0 generated-output identity; 0.160.0 output identity differs (§3.1)); L2199 (0.158.0 generated-output identity; 0.160.0 output identity differs (§3.1))
- *not re-checked:* L66 [supplier descendants]; L105 [delegation run (adapter)]; L242 [supplier descendants]; L246 [plugins-on start-up traffic]; L410–419 [plugins-on start-up traffic, supplier descendants]; L1692–1696 [OBS-1 MCP route]; L1828 [delegation run (adapter)]; L1963–1978 [plugins-on start-up traffic, supplier descendants, OBS-1 MCP route]; L2168 [supplier descendants]
- *partly not re-checked:* L30–41 [delegation run (adapter)]; L75 [OBS-1 MCP route]; L97 [delegation run (adapter)]; L110 [supplier descendants]; L136 [plugins-on start-up traffic, delegation run (adapter), OBS-1 MCP route]; L142 [delegation run (adapter), OBS-1 MCP route]; L143 [OBS-1 MCP route]; L284–297 [supplier descendants]; L389–406 [OBS-1 MCP route]; L450–485 [plugins-on start-up traffic, OBS-1 MCP route]; L546–554 [supplier descendants]; L595–611 [supplier descendants]; L841–850 [OBS-1b answer-to-resolved timing]; L875–884 [supplier descendants]; L1068–1075 [OBS-1 MCP route]; L1082 [delegation run (adapter), OBS-1 MCP route]; L1248 [delegation run (adapter), OBS-1 MCP route]; L1249 [plugins-on start-up traffic, OBS-1 MCP route]; L1274–1278 [delegation run (adapter)]; L1290 [delegation run (adapter)]; L1293–1304 [delegation run (adapter)]; L1448 [delegation run (adapter), OBS-1 MCP route]; L1450 [OBS-1 MCP route]; L1451 [delegation run (adapter), OBS-1 MCP route]; L1720 [supplier descendants]; L1731–1751 [plugins-on start-up traffic, OBS-1 MCP route]; L1753–1769 [OBS-1 MCP route, OBS-1b answer-to-resolved timing]; L1785 [delegation run (adapter), OBS-1 MCP route]; L1786 [OBS-1 MCP route]; L1788 [OBS-1b answer-to-resolved timing]; L1790 [OBS-1 MCP route]; L1793 [plugins-on start-up traffic]; L1794 [OBS-1 MCP route]; L1796 [supplier descendants]; L1798–1803 [delegation run (adapter), OBS-1 MCP route]; L1807–1819 [delegation run (adapter)]; L1826 [delegation run (adapter), OBS-1 MCP route]; L1827 [delegation run (adapter)]; L1833 [plugins-on start-up traffic, supplier descendants]; L1835–1839 [delegation run (adapter)]; L1843–1847 [delegation run (adapter)]; L1893 [supplier descendants]; L1911 [supplier descendants]; L2010–2023 [delegation run (adapter)]; L2098–2110 [OBS-1 MCP route]; L2111–2127 [delegation run (adapter)]; L2161 [OBS-1b answer-to-resolved timing]; L2170 [plugins-on start-up traffic, OBS-1 MCP route]; L2171 [delegation run (adapter), OBS-1 MCP route]; L2174 [delegation run (adapter), OBS-1 MCP route]; L2204 [OBS-1 MCP route]
- *unchanged+:* L112 [items-list cursor]; L557–568 [items-list cursor]; L1079 [`mcpServerStatus/list` gains optional `serverName` at 0.160.0 (additive)]; L1286 [items-list cursor]
- *unchanged:* L10, L12, L13, L14, L16–22, L68, L74, L76, L91, L102, L125, L133, L134, L201, L203, L237, L238, L239, L240, L241, L243, L244, L245, L247, L248, L249, L250, L251, L252, L253, L254, L255, L343–350, L359–364, L374–379, L380–385, L486–509, L515–518, L528–534, L584–585, L586–594, L638, L681–689, L702–706, L721, L757–762, L764–773, L799–812, L830, L852–858, L864–868, L885–893, L919–932, L933–935, L964, L966–971, L1015–1028, L1066, L1080, L1087, L1111, L1120–1128, L1130–1134, L1138–1142, L1153–1159, L1171–1184, L1185–1190, L1200, L1202, L1204, L1217, L1224, L1227–1240, L1246, L1247, L1250, L1258–1272, L1282, L1284, L1285, L1287, L1288, L1289, L1291, L1312–1317, L1336–1339, L1340–1342, L1343–1346, L1365–1374, L1378–1386, L1399–1405, L1438–1440, L1442, L1445, L1452, L1529–1547, L1698–1701, L1705–1710, L1714, L1717, L1719, L1721, L1722, L1723, L1724, L1725, L1726, L1727, L1728, L1771, L1773–1781, L1787, L1789, L1791, L1792, L1795, L1823, L1824, L1825, L1829, L1830, L1831, L1832, L1851, L1852, L1853, L1854, L1855, L1856, L1857, L1894, L1912, L1913, L1936–1938, L1942–1943, L1945–1951, L1952–1962, L1996–2002, L2003–2009, L2028–2033, L2078–2090, L2128–2136, L2137–2147, L2155, L2162, L2172, L2178, L2196, L2200, L2201, L2211, L2218, L2222
- *names the pin or a record only:* L9, L24–28, L54–59, L108, L144, L157, L163, L213, L219, L226, L234, L318, L823, L1104, L1106, L1114, L1167–1170, L1215, L1222, L1244, L1280, L1306–1310, L1348–1354, L1356–1363, L1376, L1388–1394, L1462–1474, L1577, L1596–1598, L1703, L1712, L1805, L1841, L1863, L1914, L2062–2077, L2153, L2183–2189

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/OBS_1_0.158.0.md`** (sha256 `7b984b541edca0b1…`;28 units: changed 3, not re-checked 2, partly not re-checked 7, unchanged 13, names the pin or a record only 3)
- *changed:* L14 (0.158.0 identity value; the 0.160.0 value differs (§2)); L15 (0.158.0 identity value; the 0.160.0 value differs (§2)); L273 (0.158.0 identity value; the 0.160.0 value differs (§2))
- *not re-checked:* L138 [plugins-on start-up traffic, supplier descendants]; L176 [supplier descendants]
- *partly not re-checked:* L27–46 [OBS-1 MCP route]; L112 [delegation run (adapter)]; L166 [OBS-1 MCP route]; L215 [delegation run (adapter)]; L223 [OBS-1 MCP route]; L263 [supplier descendants]; L362 [delegation run (adapter)]
- *unchanged:* L1, L4, L8, L114, L136, L219, L221, L222, L243–257, L327, L349, L353, L366–376
- *names the pin or a record only:* L3, L5, L204

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/OBS_2_0.158.0.md`** (sha256 `61cc34ffb811eb27…`;23 units: changed 2, not re-checked 1, partly not re-checked 5, unchanged 12, names the pin or a record only 3)
- *changed:* L14 (0.158.0 identity value; the 0.160.0 value differs (§2)); L15 (0.158.0 identity value; the 0.160.0 value differs (§2))
- *not re-checked:* L149 [delegation run (adapter)]
- *partly not re-checked:* L5 [delegation run (adapter)]; L25 [plugins-on start-up traffic]; L135 [delegation run (adapter)]; L168 [delegation run (adapter)]; L269 [delegation run (adapter)]
- *unchanged:* L1, L4, L8, L18, L26, L28–42, L93, L147, L153, L181, L213, L238
- *names the pin or a record only:* L3, L19, L281

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/OBS_3_0.158.0.md`** (sha256 `554ac4451d112824…`;20 units: changed 2, partly not re-checked 1, unchanged 12, names the pin or a record only 5)
- *changed:* L14 (0.158.0 identity value; the 0.160.0 value differs (§2)); L191 (at 0.160.0 the fork's first turn gets no fresh environment context (§5.3))
- *partly not re-checked:* L19 [delegation run (adapter)]
- *unchanged:* L1, L4, L8, L17, L22, L24–41, L45–56, L147, L172, L176, L197, L208
- *names the pin or a record only:* L3, L5, L18, L203, L226

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/PIN_SPIKE_0.158.0.md`** (sha256 `0e090a4ca14e3ec3…`;66 units: changed 6, not re-checked 5, partly not re-checked 3, unchanged+ 1, unchanged 40, names the pin or a record only 11)
- *changed:* L58 (0.158.0 identity value; the 0.160.0 value differs (§2)); L73 (0.158.0 identity value; the 0.160.0 value differs (§2)); L74 (0.158.0 identity value; the 0.160.0 value differs (§2)); L101–114 (0.158.0 generated-output identity; 0.160.0 output identity differs (§3.1)); L192 (0.158.0 identity value; the 0.160.0 value differs (§2)); L339 (0.158.0 generated-output identity; 0.160.0 output identity differs (§3.1))
- *not re-checked:* L42–45 [plugins-on start-up traffic]; L228 [plugins-on start-up traffic]; L268–272 [supplier descendants]; L283–286 [plugins-on start-up traffic]; L326 [supplier descendants]
- *partly not re-checked:* L219 [supplier descendants]; L223 [delegation run (adapter)]; L341 [plugins-on start-up traffic]
- *unchanged+:* L225 [items-list cursor]
- *unchanged:* L9–16, L133–138, L139–148, L149–153, L213, L214, L215, L216, L217, L218, L220, L221, L222, L224, L226, L227, L230–234, L242–247, L248–253, L254–258, L259–263, L264–267, L273–275, L276–279, L280–282, L287–295, L296–298, L299–301, L302–304, L305–307, L308–311, L312–314, L315–316, L322, L323, L325, L329, L343, L350, L351
- *names the pin or a record only:* L1, L2, L3, L33–35, L54, L211, L324, L330, L347, L348, L349

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/generated/0.158.0/COMMITTED_STATE.md`** (sha256 `2cb7f1d29383e682…`;2 units: changed 1, names the pin or a record only 1)
- *changed:* L5–9 (0.158.0 generated-output identity; 0.160.0 output identity differs (§3.1))
- *names the pin or a record only:* L1

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/prototype/README.md`** (sha256 `902163604f497285…`;3 units: not re-checked 1, unchanged 1, names the pin or a record only 1)
- *not re-checked:* L20 [OBS-1 MCP route]
- *unchanged:* L17
- *names the pin or a record only:* L14

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md`** (sha256 `d84c7e26f4342d26…`;70 units: not re-checked 2, partly not re-checked 13, unchanged+ 3, unchanged 39, names the pin or a record only 13)
- *not re-checked:* L466 [supplier descendants]; L486 [supplier descendants]
- *partly not re-checked:* L28 [delegation run (adapter)]; L30 [supplier descendants, delegation run (adapter)]; L46–55 [delegation run (adapter)]; L337–345 [delegation run (adapter)]; L357–371 [supplier descendants, delegation run (adapter)]; L415 [delegation run (adapter)]; L566–571 [OBS-1b answer-to-resolved timing]; L579 [plugins-on start-up traffic, supplier descendants]; L675 [delegation run (adapter)]; L682 [supplier descendants, delegation run (adapter)]; L684 [OBS-1b answer-to-resolved timing]; L835–838 [delegation run (adapter)]; L883 [delegation run (adapter)]
- *unchanged+:* L525–538 [items-list cursor]; L677 [items-list cursor]; L678 [items-list cursor]
- *unchanged:* L5, L10, L11, L23, L24, L25, L26, L81–93, L135, L200–208, L290–308, L320, L325–335, L347–355, L387, L391–396, L419, L468–474, L489–494, L496–510, L519, L521, L522, L577, L580, L621, L622, L672, L673, L674, L676, L679, L680, L685, L695, L823–825, L826–828, L839–841, L891
- *names the pin or a record only:* L13, L31, L57–62, L64–70, L668, L670, L687–688, L690, L721–724, L749–759, L774–777, L845–854, L892

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/prototype/README.md`** (sha256 `ed6381a20675a2be…`;1 units: partly not re-checked 1)
- *partly not re-checked:* L12 [delegation run (adapter)]

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-03_Native plans, tools and delegation views/Design/NATIVE_PLANS_TOOLS_DELEGATION.md`** (sha256 `6eed39dcee4acf4b…`;57 units: changed 1, not re-checked 5, partly not re-checked 15, unchanged+ 2, unchanged 27, names the pin or a record only 7)
- *changed:* L459 (0.158.0 generated-output identity; 0.160.0 output identity differs (§3.1))
- *not re-checked:* L125 [delegation run (adapter)]; L329 [delegation run (adapter)]; L415–419 [delegation run (adapter)]; L420–422 [delegation run (adapter)]; L641–648 [delegation run (adapter)]
- *partly not re-checked:* L5 [delegation run (adapter)]; L33–39 [delegation run (adapter)]; L55 [delegation run (adapter)]; L150–154 [delegation run (adapter)]; L334–341 [delegation run (adapter)]; L359–375 [delegation run (adapter)]; L377–381 [delegation run (adapter)]; L387 [delegation run (adapter)]; L390 [delegation run (adapter)]; L393–396 [delegation run (adapter)]; L405–414 [supplier descendants, delegation run (adapter)]; L426–428 [delegation run (adapter)]; L532 [supplier descendants]; L657 [supplier descendants]; L749 [delegation run (adapter)]
- *unchanged+:* L180 [items-list cursor]; L530 [items-list cursor]
- *unchanged:* L11, L12, L17–31, L54, L56, L83–92, L104, L139–140, L145, L156–161, L162–165, L181, L224, L230–242, L294, L296, L305–307, L308–312, L347–349, L391, L590, L616, L618, L654, L759–760, L767–768, L781
- *names the pin or a record only:* L142, L176, L178, L613, L668–672, L741–742, L744

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-03_Native plans, tools and delegation views/Design/prototype/README.md`** (sha256 `a573f3ae186db9b6…`;2 units: unchanged 1, names the pin or a record only 1)
- *unchanged:* L16–18
- *names the pin or a record only:* L20–23

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md`** (sha256 `eca9a079f2b4ca40…`;2 units: unchanged 2)
- *unchanged:* L34, L338

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md`** (sha256 `49e180907d39db3d…`;40 units: changed 1, partly not re-checked 6, unchanged 28, names the pin or a record only 5)
- *changed:* L396–399 (generated doc of `Turn.error` now reads 'Error associated with a failed or interrupted turn'; interrupted turns still read error null in O-1, O-2, O-3)
- *partly not re-checked:* L18–28 [delegation run (adapter)]; L46 [delegation run (adapter)]; L51 [delegation run (adapter), OBS-1 MCP route]; L422–426 [delegation run (adapter)]; L483–489 [delegation run (adapter)]; L771 [supplier descendants, delegation run (adapter)]
- *unchanged:* L35, L43, L44, L45, L55–98, L117–126, L230–233, L249–251, L257, L264–268, L284, L330–332, L334–338, L420, L455, L473–481, L493–495, L503, L522, L532–544, L552, L723, L763, L785, L837, L844, L845, L854
- *names the pin or a record only:* L228, L279–280, L744, L746, L861

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/README.md`** (sha256 `586d356f3a4ddb19…`;3 units: unchanged 1, names the pin or a record only 2)
- *unchanged:* L49–53
- *names the pin or a record only:* L16, L21–33

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_AND_PROVIDER_ACCESS.md`** (sha256 `7a2ad8e4a7423943…`;71 units: not re-checked 4, partly not re-checked 10, unchanged 46, names the pin or a record only 11)
- *not re-checked:* L65–71 [binary strings were not re-extracted at 0.160.0 (types re-checked: unchanged)]; L623–624 [OBS-1 MCP route]; L628 [plugins-on start-up traffic, OBS-1 MCP route]; L629 [plugins-on start-up traffic, OBS-1 MCP route]
- *partly not re-checked:* L54–63 [supplier descendants]; L73–80 [delegation run (adapter)]; L114 [OBS-1 MCP route]; L126 [delegation run (adapter)]; L630 [plugins-on start-up traffic]; L636–647 [plugins-on start-up traffic, OBS-1 MCP route]; L662–669 [supplier descendants]; L722–728 [delegation run (adapter)]; L739 [delegation run (adapter)]; L829–832 [delegation run (adapter)]
- *unchanged:* L23–38, L40–52, L93–95, L115, L124, L125, L158, L203–208, L215, L232–234, L238–251, L258, L263, L265–272, L423–428, L455–468, L525–527, L538–544, L567–575, L610–616, L617, L618–621, L626, L631, L658–661, L671–677, L694, L695, L696, L697, L699, L701, L705–711, L738, L740, L741, L742, L778, L823–828, L871, L906, L945–959, L1011–1013, L1017, L1025, L1053
- *names the pin or a record only:* L15–18, L82–87, L96–98, L222–230, L261, L689–690, L732–734, L833–838, L857–862, L899–900, L1005–1007

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_HOME_DECISION_RECORD.md`** (sha256 `f77f87927558ca73…`;15 units: not re-checked 1, unchanged 10, names the pin or a record only 4)
- *not re-checked:* L125 [OBS-1 MCP route]
- *unchanged:* L6–10, L27, L45, L48, L69–75, L90–101, L103–104, L106, L132, L148–153
- *names the pin or a record only:* L11–15, L88, L113, L127

**`PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/prototype/README.md`** (sha256 `cca3ee5ee098789e…`;1 units: names the pin or a record only 1)
- *names the pin or a record only:* L3–10

**`PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/EXAMPLES.md`** (sha256 `85fa5a3f9200cef8…`;3 units: unchanged 1, names the pin or a record only 2)
- *unchanged:* L10
- *names the pin or a record only:* L971, L1275

**`PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/WORKFLOW_DECLARATION.md`** (sha256 `d752810933510d0f…`;27 units: not re-checked 1, partly not re-checked 6, unchanged+ 1, unchanged 15, names the pin or a record only 4)
- *not re-checked:* L110 [delegation run (adapter), OBS-1 MCP route]
- *partly not re-checked:* L8 [delegation run (adapter)]; L48 [delegation run (adapter)]; L58 [delegation run (adapter)]; L101 [delegation run (adapter), OBS-1 MCP route]; L725 [delegation run (adapter)]; L726 [delegation run (adapter), OBS-1 MCP route]
- *unchanged+:* L552 [items-list cursor]
- *unchanged:* L9, L12, L13, L90, L98, L625, L708–718, L727, L731, L733–739, L772–788, L1304–1309, L1323–1327, L1574, L1605
- *names the pin or a record only:* L706, L720, L1571, L1701

**`PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/WORKSPACE_AND_REGISTRATION.md`** (sha256 `c5332e9333ccb18c…`;21 units: unchanged+ 5, unchanged 12, names the pin or a record only 4)
- *unchanged+:* L68 [items-list cursor]; L438 [items-list cursor]; L445 [items-list cursor]; L477 [items-list cursor]; L573 [items-list cursor]
- *unchanged:* L6, L22, L30, L292, L365, L478, L479, L482, L489, L501, L532, L572
- *names the pin or a record only:* L20, L21, L425, L510

**`PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/EXECUTION_COMPATIBILITY.md`** (sha256 `69e6e79af078980b…`;57 units: not re-checked 1, partly not re-checked 23, unchanged+ 1, unchanged 26, names the pin or a record only 6)
- *not re-checked:* L1956 [OBS-1 MCP route]
- *partly not re-checked:* L8 [delegation run (adapter)]; L58 [OBS-1 MCP route]; L61 [delegation run (adapter)]; L75 [OBS-1 MCP route]; L92 [OBS-1 MCP route]; L113 [OBS-1 MCP route]; L127 [delegation run (adapter), OBS-1 MCP route]; L133 [delegation run (adapter)]; L313–320 [OBS-1 MCP route]; L529 [OBS-1 MCP route]; L706–719 [OBS-1 MCP route]; L725 [delegation run (adapter), OBS-1 MCP route]; L732 [OBS-1 MCP route]; L746 [OBS-1 MCP route]; L787–788 [OBS-1 MCP route]; L801 [OBS-1 MCP route]; L949 [delegation run (adapter)]; L950 [delegation run (adapter), OBS-1 MCP route]; L1524–1533 [OBS-1 MCP route]; L1734 [OBS-1 MCP route]; L2015 [OBS-1 MCP route]; L2170 [delegation run (adapter), OBS-1 MCP route]; L2201 [OBS-1 MCP route]
- *unchanged+:* L1961 [items-list cursor]
- *unchanged:* L9, L11, L12, L122, L126, L132, L290–294, L296–311, L490, L525, L689–692, L699–704, L726, L730, L731, L733, L744, L747, L925, L935–942, L946, L953, L1704, L1929, L2035, L2198
- *names the pin or a record only:* L110, L521, L750, L752–755, L807, L896

**`PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/prototype/README.md`** (sha256 `03d53193f8ff31e4…`;2 units: partly not re-checked 1, names the pin or a record only 1)
- *partly not re-checked:* L18 [OBS-1 MCP route]
- *names the pin or a record only:* L38–39

**`PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_SUPPLY.md`** (sha256 `92bb421b7bccee9a…`;44 units: not re-checked 4, partly not re-checked 8, unchanged 25, names the pin or a record only 7)
- *not re-checked:* L27 [delegation run (adapter)]; L112 [delegation run (adapter)]; L119 [delegation run (adapter)]; L120 [delegation run (adapter)]
- *partly not re-checked:* L8 [delegation run (adapter)]; L20 [delegation run (adapter)]; L111 [delegation run (adapter)]; L113 [delegation run (adapter)]; L117 [delegation run (adapter)]; L579 [delegation run (adapter)]; L663–666 [delegation run (adapter)]; L678–681 [delegation run (adapter)]
- *unchanged:* L18, L19, L28, L39, L49, L55, L64–69, L105, L106, L107, L108, L109, L110, L114, L118, L190–194, L195–201, L295–304, L338–339, L368–375, L398–399, L475, L622, L652–658, L708
- *names the pin or a record only:* L30, L99, L341, L478, L590–596, L635, L698

**`PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/prototype/README.md`** (sha256 `bcc0461af5da15b5…`;1 units: unchanged 1)
- *unchanged:* L3–7

**`PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/CATALOG_AND_READ_BASIS.md`** (sha256 `eae7369fc0109f4c…`;1 units: partly not re-checked 1)
- *partly not re-checked:* L8 [delegation run (adapter)]

**`PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/prototype/README.md`** (sha256 `9d7fd8c12fcff1f8…`;2 units: partly not re-checked 1, names the pin or a record only 1)
- *partly not re-checked:* L15 [OBS-1 MCP route]
- *names the pin or a record only:* L54–55

**`PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md`** (sha256 `f432356d054cb784…`;1 units: not re-checked 1)
- *not re-checked:* L8 [delegation run (adapter)]

**`PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/ADAPTER_ENABLEMENT_AND_RECEIVING.md`** (sha256 `71a397d918319ff8…`;44 units: not re-checked 3, partly not re-checked 12, unchanged 22, names the pin or a record only 7)
- *not re-checked:* L10 [delegation run (adapter)]; L311–315 [plugins-on start-up traffic]; L362 [OBS-1 MCP route]
- *partly not re-checked:* L363 [OBS-1 MCP route]; L364 [delegation run (adapter), OBS-1 MCP route]; L370 [delegation run (adapter)]; L921–933 [delegation run (adapter)]; L934–942 [delegation run (adapter)]; L1278 [delegation run (adapter), OBS-1 MCP route]; L1280 [OBS-1 MCP route]; L1762 [delegation run (adapter), OBS-1 MCP route]; L1766 [delegation run (adapter), OBS-1 MCP route]; L1767 [delegation run (adapter), OBS-1 MCP route]; L1792 [delegation run (adapter)]; L1825 [OBS-1 MCP route]
- *unchanged:* L9, L21, L29–35, L121–136, L148–153, L354–357, L365, L366, L369, L371, L584–600, L650–654, L1279, L1282, L1289, L1378, L1436, L1750, L1759, L1769–1773, L1779–1786, L1826
- *names the pin or a record only:* L8, L13, L20, L80, L352, L1276, L1390–1394

**`PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/prototype/README.md`** (sha256 `411e4d6634ec507d…`;1 units: unchanged 1)
- *unchanged:* L30–35

**`PKG-03_Host capability and operation contracts/1_Working/DEL-03-04_Host boundary and integration guide/Design/HOST_INTEGRATION_GUIDE.md`** (sha256 `8ca61f2de2364279…`;22 units: not re-checked 2, partly not re-checked 6, unchanged 9, names the pin or a record only 5)
- *not re-checked:* L101 [delegation run (adapter)]; L1146 [delegation run (adapter)]
- *partly not re-checked:* L131 [delegation run (adapter)]; L140 [delegation run (adapter), OBS-1 MCP route]; L486 [delegation run (adapter)]; L507 [delegation run (adapter), OBS-1 MCP route]; L526 [OBS-1 MCP route]; L1065 [delegation run (adapter)]
- *unchanged:* L9, L10, L18, L100, L416, L439, L471, L865, L867
- *names the pin or a record only:* L34, L92, L143, L372, L1095

**`PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Design/ACT_AND_POLICY_CONTRACT.md`** (sha256 `e5bf830c0d1c3096…`;2 units: unchanged 2)
- *unchanged:* L29, L32

**`PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/Design/AUTONOMY_AND_STANDING_EXCHANGE.md`** (sha256 `dc3fd0b68406fc0f…`;2 units: unchanged 2)
- *unchanged:* L12, L14

**`PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md`** (sha256 `1068e295fa367142…`;9 units: unchanged+ 1, unchanged 7, names the pin or a record only 1)
- *unchanged+:* L323 [items-list cursor]
- *unchanged:* L13, L15, L32, L40, L334, L393, L1408
- *names the pin or a record only:* L724

**`PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/LOOP_RECEIVING_CONTRACT.md`** (sha256 `d47d2249eb5f863a…`;29 units: not re-checked 1, partly not re-checked 3, unchanged 7, names the pin or a record only 18)
- *not re-checked:* L2682–2694 [OBS-1 MCP route]
- *partly not re-checked:* L16 [delegation run (adapter)]; L164 [delegation run (adapter), OBS-1 MCP route]; L364 [delegation run (adapter), OBS-1 MCP route]
- *unchanged:* L11, L18, L203, L813, L1457–1471, L2167, L2599–2603
- *names the pin or a record only:* L12, L124–134, L152–157, L167–170, L185, L222, L363, L1391–1396, L1450, L1481–1485, L2150–2156, L2237–2249, L2445–2455, L2664–2674, L2738, L2741, L2760, L2781

**`PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/prototype/README.md`** (sha256 `0218e16675866b29…`;2 units: names the pin or a record only 2)
- *names the pin or a record only:* L16–20, L28

**`PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Design/PANEL_RECEIVING_CONTRACT.md`** (sha256 `4898b6f80832b3ba…`;2 units: partly not re-checked 1, unchanged 1)
- *partly not re-checked:* L15 [delegation run (adapter)]
- *unchanged:* L17

**`PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-01_Candidate examination infrastructure and evidence protocol/Design/EXAMINATION_PROTOCOL.md`** (sha256 `dc6b6a0c24a3c780…`;6 units: unchanged 1, names the pin or a record only 5)
- *unchanged:* L120
- *names the pin or a record only:* L28–31, L59–68, L93–99, L481, L484

**`PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/Design/CONNECTED_ACTIVITY_CONTRACT.md`** (sha256 `eb133d4101ea5013…`;9 units: unchanged 2, names the pin or a record only 7)
- *unchanged:* L8, L12
- *names the pin or a record only:* L27, L479, L611, L814, L953, L1159, L1162

**`PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/Design/prototype/README.md`** (sha256 `5a510eee1c011536…`;1 units: names the pin or a record only 1)
- *names the pin or a record only:* L47–49

**`PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/Design/LOCAL_HOST_QUALIFICATION.md`** (sha256 `2668d95578a736b0…`;2 units: unchanged 1, names the pin or a record only 1)
- *unchanged:* L7
- *names the pin or a record only:* L80

**`PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/Design/TRAFFIC_OBSERVATION_PLAN.md`** (sha256 `cf0b65f2fe9607eb…`;2 units: names the pin or a record only 2)
- *names the pin or a record only:* L7, L32

**`PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Design/EXTERNAL_TRACE_CASES.md`** (sha256 `d973677bab5abdc0…`;5 units: unchanged 3, names the pin or a record only 2)
- *unchanged:* L8, L12, L619
- *names the pin or a record only:* L96, L826

## UNRESOLVED

| Item | Owner | Point of need | Effect here |
|---|---|---|---|
| Whether to advance the definition pin to 0.160.0 (D4; HOSTING §9.5 step 10; U-01) | Owner / App implementation owner | Before implementation | Not decided; this record only shows 0.160.0 is a near drop-in for the designs |
| Plugins-on start-up traffic and fetch at 0.160.0 (S-F-10, L-4, O-7 v0) | Owner (network) with DEL-01-05 | Before local-operation claims at a new pin | Not re-checked (network outside the brief) |
| Delegation through the adapter (O-4/O-4a/O-4b), the OBS-1 MCP route (A-1…A-7, OB-10), OBS-1b OB-4 timing, supplier descendants (S-F-06) at 0.160.0 | App implementation owner | Before relying on them at a new pin | Not re-checked |
| `Turn.error` on an interrupted turn: when does 0.160.0 populate it (Δ3)? | DEL-01-04, DEL-01-02 | Before outcome rendering | Doc says possible; never observed here |
| What the under-development `instant_interrupt` flag changes in interrupts (default off) | DEL-01-02 | If ever enabled | Not exercised |

## Files

| File | sha256 |
|---|---|
| `Design/VERSION_ADVANCE_0.160.0.md` (this record) | in the return file `RUN/VC.md` |
| `Design/prototype/version_advance/va_harness.py` | `fbe61c7272ca452cf75ceab930adb01fb2b162a394a808bf7b34b7b4f0fb98e8` |
| Scratch, not committed (`<session scratchpad>/codex-0.160.0/`): `codex-0.160.0-darwin-arm64.tgz` (sha1 `f78898f0…dc9c`); `pkg/`; `generate.sh`; `gen/` (`commands.log`, `MANIFEST.sha256` `ef47ec4e…3f37`, `inventory.txt` `33dbe087311333f0…`, run1/run2 trees); `check-0.158.0/` (the 0.158.0 regeneration); `diff/`; `jdiff.py`, `xval.py`, `cmp3.py`, `rows.py`, `handshake_check.py`; `features.txt`; `stmts/` | — |
| Raw logs (`<OBS>/logs`, unredacted): `run_events.jsonl` 29b100e20ebd…; `provider_tap.jsonl` 41501d1ca345…; `provider_tap_o2.jsonl` 680563d494ea…; `lmstudio.server.log` f0eaf6923ca7…; `download_watch.log` 7ce15750aebc…; `probe/probe_result.json` cf7f4659369b…; `o7_summary.json` 0f2694b7e83f…; `o6_result.json` a7e8cc4a07de…; `o1/o1_result.json` 2fc68fd360fc…; `o3/o3_result.json` 31b0887ce238…; `o2_result_stdin.json` d490656abea7…; `o2_result_kill.json` ff99efde7660…; `o5_result.json` 202e8dd4f3e3…; `o8/o8_result.json` 810d5e3bc3ee…; `capture_result.canonical-obs.json` 510120b3f855…; `capture_result.noncanonical-obs.json` 05cdb26c9479…; `capture2_result.json` eeeb46e9146c…; `w12_result.run1.json` 60101eb5108a…; `w12_result.run2.json` edf5d82d3f7b…; `w34_result.json` a7f5288adc13…; `w5_result.run1.json` 48a12fe0bbf1…; `w5_result.run2.json` 2118f2cac00e…; `w6_result.json` 34d28a5f84b3…; `supp_result.json` a4b12e7a6a3e…; per-session `frames.jsonl`, `snapshots.jsonl`, `codex.stderr` | as listed |
