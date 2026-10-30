# OBS-3 — per-turn workflow supply, chaining and fork at Codex 0.158.0 against a local LM Studio model (observation record)

- **Date:** 2026-10-02, 18:01–18:14 UTC. **Node:** OBS-3 (Type 2 TASK) of run `APP-V4-DESIGN-PASS-3-20261001`, dispatched by HELP_HUMAN.
- **Standing:** dated observations at one version (Codex 0.158.0, LM Studio 0.4.16+2, one model). **Not qualification** of the pin, the provider or the model; not an X-02 fixture; no App candidate was involved. Every answer the harness gave to a supplier request has origin `observation-harness` (none was needed: no supplier request arrived).
- **Authority:** DECISION-L ("run the local check") and K-11 (`OWNER_DECISIONS.md`, sha256 `ea96c55710af41c9…`); ruling R19-6 with R19-1…R19-3 (`R19_RESOLUTIONS.md`, `2aee038f62753ee3…`); `BRIEFS.md` "OBS-3" (`d5bd0e204b9c45f8…`); method and stop conditions from `WAVE_B/OBS-1_BRIEF.md` §8 (`b3e7a4b6d98f1720…`) as adapted by OBS-2 (`OBS_2_0.158.0.md`, `61cc34ffb811eb27…`). None of these files was edited.
- **Result in one line:** the native `skill` input supplies a workflow per turn **only when its path is the canonical path of a skill Codex has discovered** (here: an App-set extra skill root); then Codex injects the file's bytes as a `<skill>` user message, the model followed A and then B within one conversation, and the bytes are kept in the rollout. Every other path or file shape was **accepted and silently ignored**. `mention` reaches nothing. Plain text works. `thread/settings/update` (experimental) works, persists, and replaces plan mode's text. `thread/fork` **ignores** new `developerInstructions`. No stop condition was hit.

**Redaction (HOSTING §9.1, OBS-1 brief §12, as OBS-2).** `<OBS>` = `$TMPDIR/chirality-obs3-0.158.0` (Codex reports it with a `/private` prefix; both forms are `<OBS>` here), `<scratchpad>` the session scratchpad, `<V>` the Codex binary. The host's time zone and the installation identifier, which Codex sends to the provider, are left out. Remote IP addresses are shortened. Thread and turn identifiers are kept: they name invented test threads in scratch homes. The raw logs stay unredacted in `<OBS>/logs` and `<OBS>/homes` until HELP_HUMAN decides what is committed.

## 1. Versions, materials, configuration

| Item | Value |
|---|---|
| Codex binary `<V>` | `<scratchpad>/codex-0.158.0/pkg/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex`, run directly; sha256 `788a818fbb9596869c7a487554507cb8bdca17584b8671112b23f9e225ba35c8` (`shasum -a 256` at 18:01 UTC; begins `788a818f` as the brief requires). Nothing installed |
| LM Studio | app 0.4.16+2; server **OFF** at start; started by this node at 18:05:25 and stopped by it at 18:13:39 |
| Model | `qwen/qwen3.5-9b` (installed; no download), loaded at 18:05:33 in 7.7 s, 5.57 GiB, context **24576**, parallel **1** (one prediction at a time) |
| Generated types | `<scratchpad>/codex-0.158.0/gen/ts-stable/run1` and `ts-experimental/run1` (read only): `v2/UserInput.ts` (`skill`, `mention`), `v2/ThreadSettingsUpdateParams.ts`, `v2/ThreadForkParams.ts`, `v2/SkillsExtraRootsSetParams.ts`. `thread/fork`, `skills/list`, `skills/extraRoots/set` are in the stable `ClientRequest`; `thread/settings/update` only in the experimental one |
| Harness | `prototype/obs3/obs3_harness.py` and `prototype/obs3/obs3_provider_tap.py` (Python 3.13.7, standard library). They import the OBS-2 harness and tap **unchanged** (`prototype/obs2/obs2_harness.py` `589a9d703a73…`, `obs2_provider_tap.py` `b316815fc1cb…`, re-hashed after the run). OBS-1's `prototype/obs1/download_watch.sh` (`79436fce9ffb…`) ran unchanged |
| Provider path | Codex → `obs3_provider_tap.py` on 127.0.0.1:**12350** → LM Studio 127.0.0.1:1234. The tap is the OBS-2 pass-through recorder; while the flag file `<OBS>/logs/capture.flag` exists it is OBS-2's capture-only mode (records the request, answers HTTP 400, no model call). It never rewrites anything (the OBS-2 namespace adapter was not used) |
| Homes | Scratch `CODEX_HOME=<OBS>/homes/<name>` only (10 homes), cwd `<OBS>/cwd/<name>`. No credential anywhere; never `~/.codex`. `~/.agents/skills` does not exist on this host (checked with `ls`), so no person's skill was discoverable |

Base configuration of every home (OBS-2's, plus `plugins = false`, which OBS-2 O-7 found stops both start-up connections, so no plugin cache was copied):

```toml
model = "qwen/qwen3.5-9b"
model_provider = "obs2_lmstudio"
sandbox_mode = "read-only"
web_search = "disabled"
model_context_window = 24576

[analytics]
enabled = false

[model_providers.obs2_lmstudio]
name = "LM Studio (OBS-2)"
base_url = "http://127.0.0.1:12350/v1"
wire_api = "responses"

[features]
plugins = false
```

**Invented workflow packages** (written by the harness under `<OBS>/pkgs`). A's `WORKFLOW.md`, byte-identical to its `SKILL.md`-shaped copy (sha256 `8aa24bd2da42…`); B is the same with "B" and `[WF-B]`:

```markdown
---
name: obs3-workflow-a
description: Invented workflow A for the OBS-3 observation (test material only).
---
# Workflow A (invented, OBS-3)

This is invented test material. While workflow A is in force:

- Begin every reply with the exact text [WF-A] followed by a space.
- Keep each reply to one short sentence after that marker.
```

Thread developer text (role guidance stand-in) for W-1…W-5: "You are running an observation test with invented data. Invented role guidance: you are the OBS3 HELPER role. Answer briefly."

## 2. Timeline (UTC)

| Time | Step | Outcome |
|---|---|---|
| 18:01 | binary hash; `lms status` (server OFF); `lms ls`; models-folder baseline | hash equal |
| 18:01:56 | download watch and tap started | ran to 18:13:34; 633 watch lines, **0 S-2** |
| 18:02:07–18:02:25 | `capture` (13 variants, capture-only, LM Studio off) | §3.1 |
| 18:04:05–18:04:20 | `capture2` (10 variants, canonical paths, capture-only) | §3.1 |
| 18:05:25–18:05:33 | `lms server start`; `lms load qwen/qwen3.5-9b --context-length 24576 --parallel 1 -y` | memory-pressure level 2 for the next 6 s |
| 18:05:52–18:06:57 | `w12` (W-1, W-2): 4 predictions | §3.2, §4 |
| 18:07:30–18:08:00 | `w34` (W-3, W-4): 2 predictions | §5, §6 |
| 18:08:14–18:09:12 | `w5` (W-5): 3 predictions, then 4 capture-only turns after a restart | §7 |
| 18:09:31–18:10:17 | `w6` (W-6): 2 predictions, then 3 capture-only turns | §8 |
| 18:11:29 | `supp` refused by the harness's own argument parser (scenario not yet registered); no process started | deviation D-1 |
| 18:12:11–18:12:25 | `supp` (W-2b, W-6b; capture-only) | §4.1, §8.1 |
| 18:13:34–18:13:39 | tap, log stream and watch stopped; `lms unload --all`; `lms server stop` | no Codex process, tap or `lms` helper of this node remained (`ps`, `pgrep`); `lms status` OFF |

**Model calls:** 11 pass-through requests (HTTP 200), each one prediction, strictly one at a time; LM Studio's server log shows 11 `/v1/responses` requests. 37 capture-only requests (HTTP 400) made no model call. Models folder and `lms ls --json` identical before and after.

## 3. W-1 — a turn whose input includes `{type:"skill", name, path}` for workflow A

### 3.1 Which path and file shape Codex honours (capture-only, no model call)

Each row is one new thread and one `turn/start` with `[text "…Starting workflow A (run 1). Say hello…", <input>]`. "Accepted" = `turn/start` returned a turn with no error. "Reached the model" = the provider request recorded by the tap.

| # | Input item | Accepted | What reached the model besides the text | Item and history |
|---|---|---|---|---|
| c1 | `skill`, path = `…/workflows/obs3-workflow-a/WORKFLOW.md` (no skill root) | yes | **nothing** | `userMessage.content` echoes the `skill` element |
| c2 | `skill`, path = `…/skill-copies/obs3-workflow-a/SKILL.md` (no skill root) | yes | **nothing** | as c1 |
| c3 | `skill`, path = the folder | yes | nothing | as c1 |
| c4 | `skill`, wrong name, SKILL.md outside roots | yes | nothing | as c1 |
| c5 | `skill`, path to a missing file | yes | nothing; **no error or warning** | as c1 |
| c6 | `skill` only, no text item | yes | an **empty** user message | as c1 |
| c10 | `skill`, A installed at `<home>/skills/obs3-workflow-a/SKILL.md`, path given as `/var/folders/…` | yes | **nothing** | as c1 |
| c11 | `skill`, B in an extra root set by `skills/extraRoots/set`, path `/var/folders/…` | yes | nothing | as c1 |
| c13 | `skill`, SKILL.md outside roots while roots are set | yes | nothing | as c1 |
| r1, r2 | c1, c2 with canonical (`realpath`) paths | yes | **nothing** | as c1 |
| **r5** | `skill`, A installed in the home root, **canonical path** (`/private/var/folders/…`, as `skills/list` reports it) | yes | **a separate user-role message `<skill>\n<name>obs3-workflow-a</name>\n<path>…/SKILL.md</path>\n` + the file's bytes verbatim + `\n</skill>`** after the text message | as c1 |
| **r6** | `skill`, B in the App-set extra root, canonical path | yes | `<skill>` message with B's bytes | as c1 |
| r8 | as r5 with a **wrong name** | yes | the `<skill>` message, with the **real** name `obs3-workflow-a` | as c1 |
| r10 | as r5 with no text item | yes | an empty user message, then the `<skill>` message | as c1 |
| r7 | no skill item; text contains `$obs3-workflow-a` | yes | the `<skill>` message (A injected from the text mention) | text only |

- **Matching is by canonical path among discovered skills;** the name is not checked (r8). The skill must be discovered: `skills/list` showed A in the home's user root and B in the extra root (scope `user`, `enabled: true`). Any other path, including the right file under a non-canonical spelling (`/var/folders` versus `/private/var/folders`), is **accepted and silently ignored**: no error, warning or notification, and the `userMessage` item looks the same either way.
- **File shape:** a `WORKFLOW.md` is never honoured. An extra root holding only `obs3-workflow-b/WORKFLOW.md` was not discovered (`skills/list` after `skills/extraRoots/set` listed A and the system skills only). A `SKILL.md` with the same frontmatter (`name`, `description`) is. No other file shape was needed.
- **Roots:** both the home's user root (`$CODEX_HOME/skills/<name>/SKILL.md`) and an extra root set by the stable `skills/extraRoots/set {extraRoots:[abs path]}` (response `{}`) work. The extra root is **not kept across a supplier restart** (§4.1).
- **Side effect of discovery:** every discovered skill is listed in the `<skills_instructions>` developer block of **every** request in that home, with name, description and a path under a "Skill roots" table (`r0`…). Here A and B were advertised on every turn of every thread in the root homes, whether supplied or not (§9).
- **Path disclosure:** the injected `<skill>` message and the skills block carry the absolute path of the skill file to the model (here a temporary-folder path; for an App root under the person's home it would contain the user name; inference).
- The injected text is **not an App Server item**: `item/started`/`item/completed` and `thread/read` show only the `userMessage` with `{type:"skill", name, path}`. The bytes are written to the rollout as a separate user `response_item` (`<OBS>/homes/w12/sessions/…/rollout-…-01a0fdcb-4c20….jsonl`, lines 8 and 31).

### 3.2 W-1 with a real prediction (`w12`, extra root, canonical path)

Home `w12`; `skills/extraRoots/set` → `{}`; `skills/list` → `obs3-workflow-a`, `obs3-workflow-b` (user) and six system skills. Thread `01a0fdcb-4c20-7ed3-8fc3-250d9eb8b096`.

| Turn | Input | Reached the model (new items, tap) | Reply | Compliance |
|---|---|---|---|---|
| t1 `…4c66…a17a` | text "…Starting workflow A (run 1). Say hello in one short sentence." + `skill` A | the text message, then the `<skill>` message with A's bytes | "[WF-A] Hello!" | **follows A** |
| t2 `…fb95…cd84` (follow-up, no skill item) | text "…Name one invented colour…" | history (incl. A's `<skill>` message) + the text | "[WF-A] Cobalt." | A stays in force |

**W-1: accepted** for a discovered skill at its canonical path; the model received the workflow's bytes inside `<skill>…</skill>` as a user-role message and followed it.

## 4. W-2 — chaining: run B started the same way, with a line saying run A ended

Same thread, after W-1.

| Turn | Input | Reached the model (new items) | Reply | Compliance |
|---|---|---|---|---|
| t3 `…11db…6d1d` | text "…Run 1 (workflow obs3-workflow-a) has ended; its instructions no longer apply. Starting workflow B (run 2). Say hello…" + `skill` B | the full history **including A's `<skill>` message**, then the text, then B's `<skill>` message | "[WF-B] Hello!" | **follows B, drops A** (no `[WF-A]`) |
| t4 `…2852…10a6` (follow-up) | text "…Name one invented animal…" | history (A's and B's `<skill>` messages both present) + the text | "[WF-B] Bloblins." | B stays in force; A dropped |

- **Nothing is removed from history.** A's injected text is still sent on every later turn; B's is appended after the "ended" line. Dropping A rests on the end-of-run text and on recency; with this model that sufficed.
- **`thread/read {includeTurns:true}`:** four `completed` turns. Turn 1's `userMessage.content` = `[text, {type:"skill", name:"obs3-workflow-a", path:"<OBS>/pkgs/extra-root-ab/obs3-workflow-a/SKILL.md"}]`; turn 3's = `[text, {type:"skill", name:"obs3-workflow-b", path:…}]`; turns 2 and 4 text only; each turn then `reasoning`, `agentMessage`. **The workflow bytes are not in `thread/read`**, only the name and path. `thread/turns/list` gives the same turns.

### 4.1 W-2b — recorded bytes, file change, restart (supplement, capture-only)

Home `supp-w2b`, thread with turn b1 = text + `skill` A (extra root). Then the supplier was stopped (stdin), one invented line was appended to A's `SKILL.md` (sha256 `8aa24bd2da42…` → `2d8c7d1da82d…`), and a new process resumed the thread.

- `skills/list` in the new process: system skills only. **The extra root was not kept** across the restart.
- b2 (plain text after resume): history replays **A's original bytes** (the recorded `<skill>` message, without the added line), and Codex appends a **new** `<skills_instructions>` developer message reflecting the current skill set (no A or B); the old block still lists them.
- b3 (`skill` A again, root not set): **silently not injected**.
- b4 (after `skills/extraRoots/set` again): a new skills block (A and B listed) and a new `<skill>` message with the **changed** bytes. The original turn's bytes stay as recorded.
- Reading: the bytes Codex supplies are read from the file when the turn starts and are then fixed in the rollout; a later change of the file affects only later skill inputs.

## 5. W-3 — the `mention` input with the same file

- Capture-only (c7, c8, r3, r4, r9): `mention` with `WORKFLOW.md`, with the `SKILL.md` copy, and with the **discovered** skill's canonical path: **accepted; nothing reached the model** (neither the bytes nor the path; only the text message). The `userMessage` item echoes `{type:"mention", name, path}`.
- Real prediction (`w34`, turn `…cd09…cbbe`, discovered skill A in the extra root, canonical path): reply "Hello!" — **does not follow A**.
- **W-3: accepted by the protocol, not honoured for files or skills at 0.158.0** (which mention targets it serves was not determined).

## 6. W-4 — workflow B's bytes as a plain text input (baseline)

Real prediction (`w34`, turn `…2071…f176`): one text item "This is a test with invented data. Starting workflow B (run 1). The workflow follows.\n\n" + B's bytes + "\nSay hello in one short sentence." The model received exactly that user message; reply "[WF-B] Hello" — **follows B**. `thread/read` holds the **full bytes** in the `userMessage` text. Same capture as c9.

## 7. W-5 — experimental `thread/settings/update` with `collaborationMode.settings.developer_instructions`

Home `w5`, `initialize` with `experimentalApi: true`, thread `01a0fdcd-77d0-7153-a513-b97c1a2dcce7`. Each update: `thread/settings/update {threadId, collaborationMode:{mode, settings:{model, reasoning_effort:null, developer_instructions}}}`; response `{}`, then `thread/settings/updated` with the full `threadSettings` including the new `collaborationMode`. Each turn's text: "…Say hello in one short sentence, following your instructions."

| Step | Sent | Reached the model (tap) | Reply |
|---|---|---|---|
| u1, then t1 | mode `default`, dev = A's bytes (before the first turn) | A wrapped as `<collaboration_mode>…</collaboration_mode>` became a **fourth part of the thread's first developer message** (after the role text, skills and permissions blocks) | "[WF-A] Hello! I'm ready to help." — follows A |
| u2, then t2 | mode `default`, dev = B | history unchanged (A still in the first developer message), then a **new developer message** `<collaboration_mode>` B, then the user text | "[WF-B] Hello! …" — follows B, no `[WF-A]` |
| t3 | no update | no new developer message; B (and A) as before | "[WF-B] Hello! …" — B persists |
| stop (stdin), new process, `thread/resume {excludeTurns:true}` | — | resume response **`collaborationMode` = default with B's text** | — |
| t4 (capture) | no update | the same history; no new developer message | (no call) |
| u5 + capture | mode **`plan`**, dev = B | a new developer message `<collaboration_mode>` **B only — no Plan Mode text** | — |
| u6 + capture | mode `plan`, dev **null** | a new developer message with Codex's built-in "# Plan Mode (Conversational)" text | — |
| u7 + capture | mode `default`, dev null | a new developer message with the built-in "# Collaboration Mode: Default" text | — |

- **Later turns do not carry only the current text.** Each change appends a developer message at the point of change; every earlier one (A, B, plan text) remains in history and is resent. The latest is what this model followed.
- **Persists** across turns without an update and across a supplier restart (reported by `thread/resume`'s `collaborationMode`; recorded in the rollout).
- **Plan mode:** a `developer_instructions` value **replaces** the selected mode's built-in text (u5); `null` restores it (u6). A workflow supplied this way in plan mode removes the Plan Mode instructions.
- `thread/read` after the capture turns reported thread status `systemError`: an effect of the harness's capture-only HTTP 400 answers, not of the update.
- The same mechanism on `turn/start` was seen by OBS-2 (O-5b).

## 8. W-6 — `thread/fork` with new `developerInstructions`

Home `w6`. Source thread `01a0fdce-a33d-74a2-bfd7-a6679c79aa73` started with ROLE ONE ("…Invented role line: you are OBS3 ROLE ONE. End every reply with the word ROLEONE."); turn s1 `…a38b…1484` completed (reply "Here is a made-up fruit: **Orango** …"; this 9B model did not add ROLEONE, as in OBS-2).

| Step | Request | Response / what reached the model | Reply |
|---|---|---|---|
| fork | `thread/fork {threadId: source, developerInstructions: ROLE TWO}` | no error; new thread **`01a0fdcf-0cdf-7870-b9c4-c3890258fe59`**, `forkedFromId` = source, `parentThreadId` null, `source` "vscode", `agentRole` null, `instructionSources` [], status idle; `thread.turns` = the source's turn with the **same turn id** `…a38b…1484` | — |
| f1 on the fork (real) | text "…Name one invented city…" | developer message **ROLE ONE**; the source's history (user, reasoning, assistant); a fresh `<environment_context>`; the new text. **ROLE TWO nowhere** (in none of the W-6 requests, and in none of the files of home `w6`) | "Here is an invented city: **Quilvera** …" (neither marker) |
| s2 on the source (capture) | same text | ROLE ONE + its own history; unaffected by the fork | — |
| control fork (capture) | `thread/fork {threadId, lastTurnId: s1}` (no developer text) | thread `…3696…46c9`; same developer message ROLE ONE | — |
| fork of a not-loaded source (new process, capture) | `thread/fork {threadId, developerInstructions: ROLE TWO, excludeTurns:true}` | thread `…48ff…8a42`; ROLE ONE; carries the source's full history including a failed capture turn | — |

### 8.1 W-6b (supplement, capture-only, home `supp-w6b`)

- `thread/fork {threadId, config:{developer_instructions: ROLE TWO}}`: no error; ROLE ONE only. **Ignored** as well.
- `thread/fork {…developerInstructions: ROLE TWO}` then experimental `thread/settings/update` with `collaborationMode` default and dev = ROLE TWO: the fork's next request carries ROLE ONE in the first developer message **and** a new `<collaboration_mode>` ROLE TWO developer message after the copied history.

**W-6 findings.** At 0.158.0, a fork **does not take new developer instructions** (`developerInstructions` and `config.developer_instructions` are accepted and ignored, for a loaded and a not-loaded source); it carries the source's developer text and full history, adds a fresh environment context, and gets a new thread id with `forkedFromId` = the source while the copied turns keep the source's turn ids. The fork's rollout begins with `session_meta` naming `forked_from_id` and `forked_from_ordinal_exclusive` (15) and holds only the fork's own new turn: the copied history is **referenced from the source's rollout, not copied** (observed in the file; that a fork therefore depends on the source's rollout is an inference). `thread/loaded/list` listed source and forks. `thread/list` listed source and forks alike with `forkedFromId` **null** and `parentThreadId` null; only `thread/read` (and the fork response) reports `forkedFromId`.

## 9. Content sent to the model and network

- **What Codex adds:** its base instructions; the thread's developer text; a `<skills_instructions>` block listing every discovered skill (system skills always; A and B whenever a root held them); a permissions block; `<environment_context>` (cwd, shell, date, time zone, workspace roots). `client_metadata` and the `x-codex-turn-metadata` header carry the installation id and thread, session and turn ids (to the loopback tap here). No `/Users/` path, user name, scratchpad path or `~/.codex` path appeared in any of the 48 recorded requests; `<OBS>` paths did.
- **Sockets:** process snapshots and `lsof -nP -a -i -g <pgid>` every 250 ms for all 13 Codex sessions: **no non-loopback socket** from any Codex process group, no `git` child (plugins off), no path under `~/.codex` (S-5, S-6 not hit). Codex's only traffic: 127.0.0.1:12350 (tap) → 127.0.0.1:1234 (LM Studio).
- LM Studio's own `lmlink-connector` (not Codex) held connections to 2606:b740:49::…:80, 2607:f740:f::…:443 and 2606:b740:1:20::…:443 throughout, as in OBS-2 (download watch "NET" lines, 584).

## 10. Stops and deviations

| Item | Record |
|---|---|
| S-9 | **not hit.** Memory-pressure level sampled every 250 ms during every scenario (OBS-2 `Run.global_watch`): never 4. Level 2 right after the model load, 1 at the end |
| S-1…S-8, S-10, S-11 | S-1: every `codexHome` equalled its scratch home. S-2: 0 lines; models folder and `lms ls` unchanged. S-3: no `account/*` request; every `thread/start` reported `qwen/qwen3.5-9b` and `obs2_lmstudio`. S-4: every `instructionSources` was []. S-5, S-6: none. S-7: every real turn completed. S-10: predictions only as listed in §2 |
| D-1 | 18:11:29 `supp` was invoked before it was registered in the harness; the argument parser refused it; no process started |
| D-2 | Capture-only turns end `failed` (the tap's HTTP 400) and stay in those threads' history; threads `w5`, `w6` (source) and the capture threads read back `systemError`. Only the scratch threads are affected |
| D-3 | The first capture pass (c1…c13) gave paths in their `/var/folders` form; the second (r1…r10) repeated the decisive cases with canonical paths. Both are kept as results |
| D-4 | Model adherence: this model followed workflow markers at the start of a reply but not role lines asking for an ending word (ROLEONE), as in OBS-2. W-6 is therefore judged by the tap, not by the reply |

## 11. Item rows

| Item | Result | What reached the model | Compliance | `thread/read` |
|---|---|---|---|---|
| W-1 `skill` | **accepted; honoured only for a discovered skill at its canonical path** (home root or `skills/extraRoots/set`), `SKILL.md` shape; every other path or shape accepted and silently ignored | a separate user message `<skill><name/><path/>`bytes`</skill>` after the text | followed A (2/2 replies) | `userMessage` with `{type:"skill", name, path}`; bytes only in the rollout |
| W-2 chaining | **accepted** | all earlier injections stay in history; B's appended after the "run A ended" line | followed B and dropped A (2/2) | both runs' `skill` elements in their turns' `userMessage`s |
| W-2b | observed | recorded bytes replayed after a file change; extra roots lost on restart; a new skill input then injects the current file | — | — |
| W-3 `mention` | **accepted, not honoured** | nothing beyond the text | did not follow A | `{type:"mention", name, path}` |
| W-4 text | **accepted** | the bytes as the user's text | followed B | full bytes in `userMessage` |
| W-5 `thread/settings/update` (experimental) | **accepted** | a `<collaboration_mode>` developer message appended per change (or part of the first developer message if set before the first turn); earlier ones remain; persists across turns and restart; replaces plan mode's built-in text | followed A, then B (3/3) | `thread/settings/updated`; `thread/resume.collaborationMode` |
| W-6 `thread/fork` + `developerInstructions` | **accepted, ignored** (also `config.developer_instructions`) | the source's developer text and history | no role marker (D-4) | new id, `forkedFromId`, same turn ids; history referenced from the source's rollout |

## 12. Files

| File | sha256 |
|---|---|
| `Design/OBS_3_0.158.0.md` (this record) | in the return file `D/OBS-3.md` |
| `Design/prototype/obs3/obs3_harness.py` | in the return file |
| `Design/prototype/obs3/obs3_provider_tap.py` | in the return file |
| raw, not committed (`<OBS>/logs`): `run_events.jsonl` 7b5f19e20e52…; `provider_tap.jsonl` 560efdcdfe9e…; `capture_result.json` 70095a11a04d…; `capture2_result.json` db3d9f0e7e14…; `w12_result.json` 7dca8fa8f3a5…; `w34_result.json` 2bed02b9811b…; `w5_result.json` 6f6fd099d1e0…; `w6_result.json` 39e194c460f4…; `supp_result.json` 884a7be4f7c7…; `lmstudio.server.log` 204a5bc86fd9…; `download_watch.log` e71a01f8f9e0…; per-session `frames.jsonl`, `snapshots.jsonl`, `codex.stderr` | as listed |

## UNRESOLVED

- Whether a skill disabled by `skills/config/write {enabled:false}` is still injected by an explicit `skill` input while no longer advertised in the skills block (would let an App root hold registered workflows without advertising them). Not run.
- Whether `skills/extraRoots/set` is per process or per connection, and whether it can be cleared by `[]`; and how the appended skills block behaves when the root changes between runs in one conversation beyond the restart case of §4.1.
- What the `mention` input serves (apps, plugins or connectors), since it ignores files and skills.
- Whether a stronger model separates "follow the latest workflow" from earlier injected ones more or less reliably than this 9B model; and whether role lines are followed (D-4).
- Whether deleting or archiving a source thread breaks its forks (the fork's rollout references the source's).
