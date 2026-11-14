# Sandbox and approval settings at Codex 0.167.0

What the pinned Codex app server does with the approval and sandbox settings a
client may send, shown by starting it against a loopback stub that scripts the
model's tool calls. No model, no sign-in, no credential. These are facts about
the supplier at the pin, kept as tests so that they keep guarding it. They
qualify no App candidate.

- `level_fixture.py`: the stub, a fresh root per run, and the App side of the
  JSON-RPC exchange. Every approval request the fixture receives is declined.
  Every command the stub scripts is one of `Run.commands()`, writing one file
  under the run's own folders or asking the stub's own loopback address.
- `test_level_live.py`: one fact per test. It needs `CHIRALITY_CODEX_BIN` set to
  the pinned binary, whose digest is checked against `GENERATION.json` before
  every start, and is skipped otherwise. It runs in the full suite's product
  job (`.github/workflows/app-v4.yml`). The CI step sets `LEVEL_REQUIRE_LIVE=1`, under which a missing binary fails the suite instead of skipping it; an unpinned binary fails either way. `LEVEL_SCRATCH` names where the roots
  are made; `LEVEL_HOLD_SECONDS` sets how long a call to an App-supplied tool is
  left unanswered (default 120).
- `test_level_stub.py`: the stub, the run's folders and the fixed commands, with
  no Codex. It runs in `repository-checks`.

From `app/`: `CHIRALITY_CODEX_BIN=/abs/codex python3 supplier_checks/level/test_level_live.py`.

## How a run is set up

The app server is started as the App starts it on an account home
(`-c analytics.enabled=false -c model_provider="openai" -c openai_base_url=…
app-server`), with an environment built whole: `PATH` (the package's
`codex-path` first), `HOME`, `CODEX_HOME` and `TMPDIR` inside the run's root,
`TZ`, `LANG`, and the examination launcher's proxy overrides. The stub answers
the WebSocket upgrade with 426, so Codex uses HTTP at once. The project has no
`.git` above it, as the launcher requires; some cases put a `.git` folder inside
the project. The cases that write to `/tmp` use a folder
`/private/tmp/chirality-level-<run>/` that the run refuses to start if it
exists, makes itself and removes afterwards.

"Edits" below is `on-request` with `workspaceWrite`; "supervised" is
`untrusted` with `readOnly`; "full access" is `never` with `dangerFullAccess`.
The level is sent on each turn (`turn/start` `approvalPolicy` and
`sandboxPolicy`) unless the row says otherwise. Effects are read from the file
system and the stub's probe count, never from message text.

## What the tests show

| Fact | Test |
| --- | --- |
| With nothing sent (what the App sends today), the replies report `on-request`, `readOnly` with network off, profile `:read-only`. Every write, the project's included, is refused by the sandbox; the command runs and fails, and no request reaches the client. The network probe fails. Only a command that itself asks for escalation raises `item/commandExecution/requestApproval`, on its own thread. | `Presets.test_nothing_sent_is_on_request_read_only_and_a_refused_write_asks_no_one` |
| A write the sandbox refused completes no `commandExecution` item; a command that fails by its exit code does. | `Presets.test_a_write_the_sandbox_refused_completes_no_command_item` |
| Supervised raises a command approval before every command, the network probe included; a declined command does not run. | `Presets.test_supervised_asks_before_every_command_and_a_declined_one_does_not_run` |
| Supervised asks before a plain read (`/bin/ls`) too: at the pin it asked before every command tried. | `Presets.test_supervised_asks_before_a_plain_read_too` |
| Edits, network off: writes in the project, `TMPDIR` and `/tmp`; not outside the project and not inside the project's `.git`; no network. No request, except for a command that asks for escalation. | `Presets.test_edits_with_network_off` |
| Edits, network on: the same, and the network probe reaches the stub. | `Presets.test_edits_with_network_on` |
| Full access: writes everywhere tried, `.git` included, with network, and no request. A command that asks for escalation is refused by Codex itself and does not run. | `Presets.test_full_access_writes_everywhere_and_an_escalation_request_is_refused_by_codex` |
| Edits with approval `never`, network off and both temporary folders excluded (the level the examinations run at): writes only in the project; a write outside it, to either temporary folder or into `.git`, and the network probe each run and fail; a command that asks for escalation is refused by Codex before it runs. No request of any kind reaches the client. | `Presets.test_edits_that_never_ask_fail_whatever_needs_more_and_raise_nothing` |
| `excludeSlashTmp` removes `/tmp` from the writable folders; `excludeTmpdirEnvVar` removes `TMPDIR`. | `Presets.test_the_two_temporary_folder_exclusions` |
| An entry in `writableRoots` is writable, and the project stays writable. | `Presets.test_an_extra_writable_root` |
| A setting sent on `thread/start` takes effect and its reply reports it. A setting sent on `turn/start` takes effect and holds for the next turn sent with none. `thread/read` reports no setting. After a restart, `thread/resume` with none reports and applies the last setting, whether it was set at thread start or on a turn; `thread/resume` with a narrower setting reports and applies it. | `Carriers.test_thread_start_turn_start_and_resume` |
| `thread/start`, `thread/resume` and `thread/fork` take only a sandbox mode name; `config.sandbox_workspace_write` (`network_access`, `exclude_slash_tmp`, `exclude_tmpdir_env_var`) carries the rest, takes effect, and each reply reports the whole policy. | `Carriers.test_config_carries_the_workspace_write_options_on_start_fork_and_resume` |
| A writable root in the Codex home's `config.toml` (the person's own settings) widens workspace write, and the start reply lists it. `config.sandbox_workspace_write.writable_roots = []` on `thread/start` removes it; a turn's `sandboxPolicy` with `writableRoots: []` does not. | `Carriers.test_writable_roots_from_the_home_config_are_removed_only_by_a_start_override` |
| With the home's `config.toml` naming the widest values (approval `never`, the automatic reviewer, full access, network on, neither temporary folder excluded), or a named permissions profile, nothing sent gives the person's own; the level sent at start, or on each turn alone, decides approval, reviewer, sandbox, network and both exclusions, and an escalation request reaches the client. Writable roots are the one exception (row above). | `Carriers.test_the_level_sent_wins_over_the_home_config_on_every_other_dimension` |
| `thread/fork` with none inherits the source's setting; with a setting, applies it; the reply reports what applies. A turn on a fork sends the provider no `tools` at all, yet a call the model makes is still carried out. | `Carriers.test_fork` |
| A command started in one turn keeps running after the turn ends, and a narrower setting on the next turn does not stop it from writing outside the project. | `Narrowing.test_a_running_command_outlives_its_turn_and_a_narrower_next_turn` |
| A child spawned by `spawn_agent` takes the parent's level: under edits it writes in the project and not outside, and its escalation request arrives on the child's thread id; under full access it writes outside and raises nothing. A child is not offered `spawn_agent`. | `Child.test_a_child_under_edits`, `Child.test_a_child_under_full_access` |
| A call to an App-supplied tool (`dynamicTools` at thread start) arrives on the thread's id and can stay unanswered for `LEVEL_HOLD_SECONDS` without the turn ending; answered, the turn completes with the answer. `turn/interrupt` ends the turn as interrupted and the client is sent no `serverRequest/resolved`. Ended with a call outstanding, the restarted server does not raise it again on resume, and that turn reads interrupted. After resume the tool is still offered; on a fork it is not listed to the model, yet a call is still routed to the client on the fork's thread. | `AppTool.test_held_interrupted_relaunched_resumed_and_forked` |
| A child is not offered the App-supplied tool, and its call to it is answered by Codex as an unsupported call; nothing reaches the client. | `AppTool.test_a_child_is_not_given_the_app_tool` |
| `request_user_input` is listed to the model in an ordinary conversation, but a call to it is refused in Default mode and nothing reaches the client. In plan mode the call reaches the client as `item/tool/requestUserInput`. | `Question.test_offered_but_refused_in_default_mode`, `Question.test_reaches_the_client_in_plan_mode` |
