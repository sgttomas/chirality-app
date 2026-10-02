# OBS-3 — return to HELP_HUMAN

- Node OBS-3 (Type 2 TASK), run `APP-V4-DESIGN-PASS-3-20261001`, 2026-10-02 18:01–18:14 UTC.
- Brief: `BRIEFS.md` "OBS-3" (sha256 `d5bd0e204b9c…`); scope R19-6 with R19-1…R19-3 (`R19_RESOLUTIONS.md` `2aee038f6275…`); authority DECISION-L and K-11 (`OWNER_DECISIONS.md` `ea96c55710af…`); method and stop conditions from the OBS-1 brief §8 and OBS-2 (record `61cc34ffb811…`, harness reused unchanged).
- Record: `PKG-01…/DEL-01-01…/Design/OBS_3_0.158.0.md` (redacted as OBS-2's). Standing: dated observations at Codex 0.158.0 with LM Studio 0.4.16+2 and `qwen/qwen3.5-9b`; not qualification.
- Hard limits held: no sign-in, no key or token, no download (0 S-2 lines; models folder and `lms ls` unchanged), no install, scratch `CODEX_HOME`s only (never `~/.codex`), invented material only, **11 model predictions, one at a time** (parallel 1), plus 37 capture-only requests that made no model call. **S-9 not hit** (sampled every 250 ms; maximum level 2). Every process this node started was stopped: Codex sessions, the tap, the log stream, the download watch; the model was unloaded and the LM Studio server, which this node started, was stopped.

## Items

| Item | Result | What reached the model | Compliance |
|---|---|---|---|
| W-1 `skill` input | **Accepted; honoured only for a discovered skill at its canonical path.** The skill must be a `SKILL.md` in a root Codex discovers (the home's `skills/` or a root set by the stable `skills/extraRoots/set`), and the path must be the canonical spelling `skills/list` reports (`/private/var/…`, not `/var/…`). The name is not checked. A `WORKFLOW.md`, a `SKILL.md` outside a root, a folder, a missing file or a non-canonical path: **accepted and silently ignored** (no error, warning or notification; the item looks the same) | a separate user-role message `<skill><name>…</name><path>abs path</path>` + the file's bytes verbatim + `</skill>`, after the text | followed A (2 of 2 replies) |
| W-2 chaining | **Accepted.** A then B in one thread; "run 1 has ended" line + `skill` B | A's injected text stays in history on every later turn; B's is appended | followed B, dropped A (2 of 2) |
| W-2b (supplement) | Injected bytes are fixed in the rollout at turn start and replayed after the file changes and the supplier restarts; **extra roots are not kept across a restart**; after re-setting the root a new skill input injects the current file | — | — |
| W-3 `mention` | **Accepted, not honoured**, even for the discovered skill's path | nothing beyond the text | did not follow A |
| W-4 plain text | **Accepted** | the bytes as the user's text | followed B |
| W-5 `thread/settings/update` (experimental) | **Accepted.** Each change appends a `<collaboration_mode>` developer message (set before the first turn it joins the first developer message); earlier texts remain; persists across turns and a restart (`thread/resume` returns it); in plan mode the value **replaces** Codex's Plan Mode text, `null` restores it | developer role | followed A, then B (3 of 3) |
| W-6 `thread/fork` + new `developerInstructions` | **Accepted and ignored** (also `config.developer_instructions`), for a loaded and a not-loaded source. The fork carries the source's developer text and full history, a fresh environment context, a new thread id with `forkedFromId` (in `thread/read`; `thread/list` shows null), the source's turn ids; its rollout references the source's history instead of copying it. Fork + experimental settings update adds the new text but keeps the old | the source's role text only | no role marker (this model did not follow role-ending lines, as in OBS-2) |

`thread/read` for W-1/W-2 shows each run's start as `userMessage.content` `[text, {type:"skill", name, path}]`; the workflow **bytes are not in `thread/read`** (only in the rollout). For W-4 the bytes are in the `userMessage` text.

## Recommendation for R19-1 (supply route)

**Recommended: the text input**, carrying the registered revision's exact bytes as its own text element of the turn that starts the run, between App-authored lines that name the workflow and say the previous run ended (W-2's wording sufficed with this model).

1. **Verifiable record.** It is the only route whose supplied bytes Codex returns in `thread/read`, so the App's per-run record of "the exact bytes and content identity it supplied" (R19-1) can be checked against Codex's own history. With `skill`, Codex gives no acknowledgement in any App Server event: the item echoes name and path whether or not anything was injected.
2. **No silent failure.** `skill` is ignored without a signal unless the path is exactly a discovered skill's canonical path. A wrong spelling or a lost root would start a run that has no workflow.
3. **No advertisement.** Every skill in a discovered root is listed to the model, with its description and absolute path, on every request. With registered workflows in a root, the model can load any of them on its own, which goes against R19-2(b): a proposal is never a selection.
4. **No path disclosure or restart chores.** The `<skill>` message gives the model the file's absolute path, which for an App root under the person's home would include the user name (inference). Extra roots must be set again after every Codex spawn.
5. **Least version-sensitive (R19-5).** Plain text is the most basic input. The skill-matching rules found here are behaviour, not protocol.

**The native `skill` input is a close second.** It works and gives a structured run-start marker. The App could adopt it with these mitigations:
- Copy the revision byte-equal as `<App root>/<name>/SKILL.md`. Its frontmatter is already SKILL.md-shaped.
- Call `skills/extraRoots/set` on every spawn, and pass the canonical path.
- Check `skills/list` before `turn/start` and refuse to start if the path is not there.
- Keep only the run's workflow in the root, so others are not advertised. Not observed: how the skills block changes mid-conversation when the root changes. The restart case appended a new block.
- Hash its own copy of the bytes.

`skills/config/write {enabled:false}` might hide the other skills from the list without disabling explicit use. That is not observed and is listed as UNRESOLVED.

**Not recommended for workflows:** `thread/settings/update`.
- It is experimental.
- Its developer text persists for the conversation until replaced, which re-creates a conversation binding in another form.
- Every change accumulates.
- It replaces plan mode's instructions.

**All routes:** nothing removes an earlier workflow from history. Ending a run relies on the end-of-run line and recency. A fork with `lastTurnId` before the run, or a new conversation, is the only way to drop it.

**R19-3 consequence:** a fork does **not** take new guidance at 0.158.0. So "Continue as ‹role›" falls to R19-3's other branch: a new conversation with the role's guidance and a handoff summary the person sees. A fork followed by the experimental settings update is not a clean role change, because the old role text stays first in the developer messages.

## Pointers for the D nodes and node F (not edits)

- **D5 / D6 / F (R19-1 row DEL-02-04 → DEL-02-02):** the supplier of per-run bytes is the run starter. With the text route, no skill root and no file materialisation are needed. With the skill route, DEL-02-02's registered store must publish `SKILL.md` copies in an App root.
- **D6:** fork ignores `developerInstructions` and `config.developer_instructions` (W-6, W-6b). `developerInstructions` at start remains the only stable role lever (with OBS-2 O-5).
- **D1 (DEL-01-02):** run boundaries in history. `skill` runs leave a structured element; text runs leave text. Capture-only failures put threads in `systemError` (harness effect).
- **HOSTING (F):** new supplier facts at 0.158.0:
  - skill input is matched by canonical path among discovered skills and is otherwise silently ignored;
  - `mention` ignores files and skills;
  - extra roots are per process and not persisted;
  - the skill block is advertised on every request;
  - injected skill bytes are recorded in the rollout and replayed;
  - fork lineage is by reference (`forked_from_id`, `forked_from_ordinal_exclusive`);
  - `thread/list` shows `forkedFromId` null for forks.

## Stops and deviations

- No stop condition hit (S-1…S-11; details in the record §10).
- D-1: one `supp` invocation was refused by the harness's own argument parser before the scenario was registered; no process started.
- D-2: capture-only turns end `failed` and stay in those scratch threads.
- D-3: a first capture pass used non-canonical paths. That is how the canonical-path rule was found; both passes are kept.
- D-4: this model followed reply-start workflow markers but not role-ending words, so W-6 is judged by the provider tap.

## Network destinations seen

| From | To | When |
|---|---|---|
| Codex (`<V>`) | loopback only: 127.0.0.1:12350 (OBS-3 tap) → 127.0.0.1:1234 (LM Studio) | turns only |
| Codex | **no non-loopback socket** in any of 13 sessions (lsof every 250 ms); no `git` child (`[features] plugins = false`); nothing under `~/.codex` | throughout |
| LM Studio's own `lmlink-connector` (not Codex) | 2606:b740:49::…:80, 2607:f740:f::…:443, 2606:b740:1:20::…:443 (as in OBS-2) | throughout |

## Files written

| File | sha256 |
|---|---|
| `PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/OBS_3_0.158.0.md` | reported in the hand-back |
| `…/Design/prototype/obs3/obs3_harness.py` | reported in the hand-back |
| `…/Design/prototype/obs3/obs3_provider_tap.py` | reported in the hand-back |
| `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/D/OBS-3.md` (this file) | reported in the hand-back |
| scratch (not committed): `$TMPDIR/chirality-obs3-0.158.0/` (10 homes, invented packages, logs; raw-log hashes in the record §12) | — |

## UNRESOLVED

- `skills/config/write {enabled:false}`: does it keep explicit injection while hiding a skill from the advertised list?
- `skills/extraRoots/set`: scope (process or connection), clearing, and the skills block when the root changes mid-conversation without a restart.
- What `mention` serves.
- Model adherence with a stronger model (latest workflow over earlier ones; role lines).
- Whether removing or archiving a source thread breaks its forks.
