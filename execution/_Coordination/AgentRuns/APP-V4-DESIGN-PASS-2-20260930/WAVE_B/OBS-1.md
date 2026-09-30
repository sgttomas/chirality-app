# OBS-1 — return (Type 2 TASK, 2026-09-30)

Brief: `WAVE_B/OBS-1_BRIEF.md` (sha256 b3e7a4b6d98f…) with the integrator's decisions in `BRIEFS.md` "OBS-1 — the live Codex turn" (sha256 b006996cd794…). Record: `PKG-01…/DEL-01-01…/Design/OBS_1_0.158.0.md`.

## Outcome

- **One Codex turn ran and completed** (0.158.0 vendor binary, sha256 788a818f… = SPIKE §3; route R-1 only; LM Studio 0.4.16+2; `qwen/qwen3.5-9b` 4-bit MLX, installed; context 24576).
- **S-8 hit: no `mcpToolCall`.** Codex sent one `POST /v1/responses`. LM Studio logged "Ignoring unsupported tool type(s): namespace." and never placed `example_lookup` in the model's tool list. The model still produced two well-formed calls to `example_lookup`, which LM Studio skipped as having an "invalid tool name". The final agent message says the tool is not available. Reading (inference): Codex offers MCP tools to a Responses provider as a `namespace` tool, which LM Studio drops. A different or smaller model would likely meet the same drop, so Qwen3 4B may not help. This node downloaded nothing and did not try R-2.
- **Part B not run.** The owner's approval, relayed by HELP_HUMAN, was conditional on the first turn not hitting a stop condition, and it did. O-7 and A-7 are not observed.
- Parts C and D and pre-flight P-5 were run (allowed).

## Headline observations

- **EXEC:** O-1…O-4 not observed. O-5: 3 agentMessages (two whitespace-only), `phase` present and null, the last completed before `turn/completed`. O-6: same identities in started and completed; turn status `completed`, 67.7 s; no model element on the turn. O-9: none. No server request of any kind.
- **ADAPTER:** A-1: the pre-thread list gives runtimeStatus null, httpOrigin null and authStatus `unsupported`; on the thread, `starting` → `ready` in 18 ms. A-3: `_meta.progressToken` appears on list calls, and `tools/call` was not observed. A-5 (partial): the MCP server wrote its log outside cwd under the read-only sandbox. A-6: a dotted `config` key `mcp_servers.obs1d` adds the server to that thread only (thread-scoped list shows `connected`; the global list shows neither the new server nor a runtime status). A-2 and A-4 not observed.
- **LOOP (part C, Chat Completions):** (1) Each call arrives as two fragments: id, type and name with `arguments ""`, then the whole arguments JSON in one fragment. (2) The final chunk has an empty delta and `finish_reason "tool_calls"`, then `[DONE]`. (3) Two calls come in one response as index 0 then index 1, sequentially. (4) A tool with no parameters gets arguments `"{}"`. Reasoning streams as `delta.reasoning_content`.
- **HOSTING:** L-2 observed at this pair (Responses; LM Studio ignored `prompt_cache_key` and `include`, and turned developer into system). L-3 negative for MCP. Requested and reported model and provider were equal; no reroute. stderr was 0 bytes. No survivors at exit (H11). `remoteControl/status/changed` came before `initialized` (H4).

## Stops, deviations, network

- **Deviation (P-3):** memory-pressure level 2 (warn) at 32768 and again at 24576. The run went ahead under S-9's "critical" definition and never reached level 4.
- The warm home was not fully synced, so the supplier re-fetched `github.com/openai/plugins.git` with `git` from start until 25 s into the turn (U-18). Before the thread, Codex contacted **chatgpt.com**: a remote-control loop, and a featured-plugins request that returned **401**. Its local log records the host name and installation id beside that URL. Neither is a model request, and no sign-in request came to the client. Not treated as S-3 or S-5; flagged.
- During the turn: loopback to 127.0.0.1:1234 only (besides the plugin git fetch). No `lms get`, no new model folder, 0 S-2 hits. LM Studio's own periodic Cloudflare connections and `lmlink-connector` traffic were already present before this node.
- The model's context contained only `<OBS>` paths, plus the host's time zone (a finding under K1-6).
- This node started the LM Studio server, then unloaded all models and stopped it at the end.

## Files written (sha256, 12-char prefix)

| File | sha256 |
|---|---|
| `DEL-01-01…/Design/OBS_1_0.158.0.md` | e3a221c1d874 |
| `DEL-01-01…/Design/prototype/obs1/obs1_harness.py` | 0b1325547b78 |
| `DEL-01-01…/Design/prototype/obs1/download_watch.sh` | 79436fce9ffb |
| `DEL-01-01…/Design/prototype/obs1/partc_chat.py` | cc5e1ded3fb6 |
| `WAVE_B/OBS-1.md` (this file) | computed by the integrator |
| Scratch (not committed): `$TMPDIR/chirality-obs1-0.158.0/` (logs, frames 0965e24adefa, scratch home with rollout) | — |

No other repository file was edited, and no git writes were made. `OWNER_DECISIONS.md` now reads f5a8ff89d500…, not the brief's 1dfd5bf4…: it was changed by the integrator, not by this node.

## For HELP_HUMAN

Next options, each needing a decision: (a) find out whether Codex can send flat function tools to a custom Responses provider; (b) a local server that accepts `namespace` tools; (c) the owner's sign-in route under K1-6. Downloading Qwen3 4B alone is unlikely to change the S-8 cause.
