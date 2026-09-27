> **WITHDRAWN — not to be launched.** The owner declined these tests on
> 2026-09-26 (D-16, `OWNER_MESSAGES.md` M-02). The brief was never run. It is
> kept as the record of what was proposed; the text below is unchanged from
> commit `d7c7d2c5a` (SHA-256 of that version
> `620b83af28d4fc2a91d8402ca9e15488b36ee6b7132f665365f8d729a6042c0b`).

# HX-01 — Harness experiments with a local model server (brief)

Standing: **brief for an executing agent on another machine.** Written by
HELPS_HUMANS (run V4-CONCEPT-20260925, Chirality App v4 conceptual
undertaking) for the owner to hand to an agent on the machine that runs the
oMLX server. The owner launches that agent; this file is not evidence that
it ran. Its return is examined by HELPS_HUMANS and brought to the owner.

## 1. Purpose

Produce evidence for the v4 harness choice (question Q-05): whether a local
model server works for agentic work through **T3 Code** (with Codex and with
Claude Code) and through the **stock Codex App Server** directly, and whether
subscription sign-in, API key and local model can coexist. The owner's
requirements: a local model server is required; the harness must not be
constraining and should be the easiest to maintain; OAuth, API key and local
model available to the user, possibly all at once; Mac first.

This is **observation, not selection**. Report what happened; do not
recommend a supplier.

## 2. Basis to read first

On branch `claude/chirality-app-v4-architecture-9f35c4` of
`sgttomas/chirality`, under `projects/chirality-app-v4/`:

- `conceptual/DISCUSSION_2026-09-25.md` §6 — the question and the four
  experiments this brief makes concrete.
- `execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/tasks/T8-t3code.return.md`
  — what is already known about T3 Code, Codex custom providers and oMLX,
  including known T3 issues (#13436 truncation, #4729 auth warning, #11873
  usage warning, #644 profile flag, #4149 Claude model aliases).
- `…/tasks/T7-supplier-landscape.return.md` §1.1–1.2 — Codex App Server and
  Claude Agent SDK facts.

## 3. Your role and boundary

- You are a bounded executor. Do not delegate to other agents.
- **Use only scratch locations** created for this work (for example
  `~/hx01-scratch/`). Do not edit `~/.codex/config.toml`,
  `~/.claude/settings.json`, or any existing project. Pass custom providers
  through command-line overrides (`-c …`) or scratch config directories.
- **T3 Code:** installing it is permitted on this machine for this work
  (the owner's go-ahead is the launch of this brief). Use the official
  release from `github.com/pingdotgg/t3code` releases or `t3.codes`; record
  the version and the download's SHA-256. Run with an isolated home
  (`T3CODE_HOME` or `--base-dir` in scratch) and with telemetry off
  (`T3CODE_TELEMETRY_ENABLED=false`). Use **Supervised** permission mode, not
  the default Full access, so approvals can be observed.
- **oMLX:** use the server as the owner has it running. Do not restart it,
  change its model, or change its settings. Record the model it serves.
- **Accounts:** use the owner's existing Codex and Claude Code sign-ins as
  they are. Never copy, print, log, or commit credentials, tokens, pairing
  codes, API keys, `auth.json`, or account e-mail addresses.
- **Data:** invented material only (§5). No real engineering or client data.
- **Stop rather than improvise:** if a step fails, record the exact error and
  move to the next step. Keep each experiment within about 90 minutes.
- Leave the machine as you found it apart from the scratch folder and the
  T3 Code installation; record anything else you had to change.

## 4. Record the environment first

`ENVIRONMENT.md`: macOS version, chip, memory; versions of `t3` / T3 Code
desktop, `codex`, `claude`, Node, oMLX; the oMLX model identifier,
quantisation and context window as served; the oMLX address as used (host
and port only; no key); how each tool was installed, with source URL and
checksum where available; date and time (UTC).

## 5. The standard task

Create a scratch Git repository `~/hx01-scratch/repo` containing:

- `calc.py` with a function `pipe_area(d_mm)` returning the cross-sectional
  area in mm² (a deliberately wrong formula: `3.14 * d_mm`), and
- `test_calc.py` with one `unittest` test that fails on the wrong formula,
- `README.md` with one line describing the repository.

Commit it. The standard task given to the agent under test, in each run:

1. "Make a plan to fix the failing test and document the function." (plan
   mode where the harness offers one)
2. "Carry out the plan: fix `calc.py`, add a docstring, update `README.md`,
   and run the test." (expect two file edits and one shell command, and at
   least one approval request in Supervised mode — approve it)
3. After the first file edit, **interrupt** the turn, then resume or continue
   in the same conversation and let it finish.
4. Quit the harness or server process, relaunch, reopen the same conversation,
   and ask: "What did you change, and did the test pass?"

## 6. Experiments

Run in this order. Each has its own folder of evidence (§7).

**X1 — T3 Code + Codex + oMLX.** Create a T3 Codex provider instance whose
launch arguments point Codex at oMLX (for example
`-c model_provider="omlx" -c model_providers.omlx.name="oMLX"
-c model_providers.omlx.base_url="http://<host>:<port>/v1"
-c model_providers.omlx.env_key="OMLX_API_KEY"`, with `OMLX_API_KEY` set as a
sensitive variable if oMLX needs one) and add the served model as a custom
model. Run the standard task. Then, in a second conversation, start with a
ChatGPT-signed-in Codex instance and try switching that conversation to the
oMLX instance mid-way; record what T3 offers and what happens.

**X2 — T3 Code + Claude Code.** Create a Claude instance pointed at oMLX's
Anthropic-compatible endpoint (a separate `CLAUDE_CONFIG_DIR` in scratch,
with `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, and an empty
`ANTHROPIC_API_KEY`; the served model as a custom model). Run the standard
task. If the owner's Claude subscription sign-in is present, also create a
subscription instance and run step 1 only, to show both instances side by
side. An API-key instance is optional (only if the owner supplies a key in
that session; never record it).

**X3 — Stock Codex App Server + oMLX, without T3.** In scratch, write a
minimal client (Node or Python, under 300 lines) that starts
`codex app-server` over stdio, sends `initialize`, `thread/start` with
`modelProvider` set to the oMLX provider (defined with `-c` overrides when
launching `codex app-server`), and `turn/start` with the standard task.
Answer approval requests by accepting them. Log every JSON-RPC message
(request, response, notification) to a JSONL file. Then kill the process,
relaunch, `thread/resume`, and send step 4. If time allows, start a second
thread in the same process **without** `modelProvider` (the owner's ChatGPT
sign-in) and send step 1, to show local and cloud threads in one server.

**X4 — Headless T3 Code with a host tool over MCP (optional; do it if X1 and
X2 finished).** Write a tiny MCP server (streamable HTTP, current protocol
where the harness supports it) exposing two tools over an invented
"pipe model": `inspect_selection` (returns a fixed JSON object with a
`basis` field) and `submit_proposal` (accepts an operation and returns
`{"status": "queued"}`; it never applies anything). Register it with the
Codex instance through launch arguments (`-c mcp_servers.hx.url=…`). Run
`t3 serve` headless in scratch, obtain a client credential with `t3 pair`,
and drive one conversation through the HTTP API (create project, create
thread, start turn asking the agent to inspect the selection and submit a
proposal to change a pipe diameter; answer approvals through the API). If
the MCP protocol version is refused, record the exact handshake error.

## 7. Evidence to return

Place everything in
`projects/chirality-app-v4/execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/experiments/HX-01/`:

```
HX-01/
  RETURN.md          summary (below)
  ENVIRONMENT.md
  X1/ X2/ X3/ X4/    one folder per experiment, each with:
    COMMANDS.md      exact commands and settings used (secrets replaced by <REDACTED>)
    OBSERVATIONS.md  step-by-step: what was done, what happened, exact error text
    logs/            raw logs and event streams (JSONL), trimmed to the relevant runs
    screenshots/     PNGs of the T3 Code interface at each step, where there is an interface
    repo.patch       `git -C ~/hx01-scratch/repo diff <initial-commit>` after the run
  MANIFEST.json      path, size and SHA-256 of every file above
```

`RETURN.md` contains a table with one row per step of each experiment:
experiment, step, **outcome** (passed / failed / blocked / not run /
inconclusive), evidence file(s), and a one-line note. Below it, separately:
limitations, anything you had to change outside scratch, and your own
interpretation clearly marked as interpretation. Report failures as
plainly as successes; a failed step is useful evidence.

The repository is **public**. Before committing: search the evidence for
keys, tokens, e-mail addresses, pairing codes and `auth.json` content and
remove them; keep every file under 5 MB (trim logs; downscale screenshots
if needed); include no private or client data.

## 8. Delivery

From the branch `claude/chirality-app-v4-architecture-9f35c4`, create the
branch `claude/v4-hx01-evidence`, commit only the `HX-01/` folder, and push
it. Do not open or merge a pull request. If Git access is not available on
that machine, give the folder to the owner to pass on.

## 9. What happens on receipt

HELPS_HUMANS checks the return against this brief (every step reported,
manifest hashes match, claims supported by the logs and screenshots),
records its standing as an executed check on the named host by the named
agent, launched by the owner, and brings the findings and their limits to
the owner. Questions go back through the owner.
