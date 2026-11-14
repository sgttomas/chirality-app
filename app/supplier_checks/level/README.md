# Sandbox and approval settings at Codex 0.167.0

What the pinned Codex app server does with the approval and sandbox settings a
client may send, shown by starting it against a loopback stub that scripts the
model's tool calls. No model, no sign-in, no credential. These are facts about
the supplier at the pin, kept as tests so that they keep guarding it. They
qualify no App candidate.

- `level_fixture.py`: the stub, a fresh root per run, the App side of the
  JSON-RPC exchange, and `judge`, which decides what happened to one scripted
  call. Every approval request the fixture receives is declined. Every command
  the stub scripts is one of `Run.commands()`. Each writes one file under the
  run's own folders, reads the project, or connects to the stub's own loopback
  address, and every path in it is quoted for the shell.
- `test_level_live.py`: one fact per test.
  - It needs `CHIRALITY_CODEX_BIN` set to the pinned binary, whose digest is
    checked against `GENERATION.json` before every start, and is skipped
    otherwise.
  - It runs in the full suite's product job (`.github/workflows/app-v4.yml`).
    That step sets `LEVEL_REQUIRE_LIVE=1`, under which a missing binary fails
    the suite instead of skipping it. An unpinned binary fails either way.
  - `LEVEL_SCRATCH` names where the roots are made. `LEVEL_HOLD_SECONDS` sets
    how long a call to an App-supplied tool is left unanswered (default 120).
- `test_level_stub.py`: the stub, the run's folders, the fixed commands, the
  cleanup, and `judge` itself, with no Codex. It runs in `repository-checks`.
  It includes tests that break the suite on purpose and must fail: a call
  removed from the script, a turn that never completes, a failure without the
  sandbox's text, and a misleading configuration report.

From `app/`: `CHIRALITY_CODEX_BIN=/abs/codex python3 supplier_checks/level/test_level_live.py`.

## How a run is set up

The app server is started as the App starts it on an account home
(`-c analytics.enabled=false -c model_provider="openai" -c openai_base_url=…
app-server`), with an environment built whole:
- `PATH`, with the package's `codex-path` first;
- `HOME`, `CODEX_HOME` and `TMPDIR`, all inside the run's root;
- `TZ` and `LANG`;
- the examination launcher's proxy overrides.

The stub answers the WebSocket upgrade with 426, so Codex uses HTTP at once.
The project has no `.git` above it, as the launcher requires; some cases put a
`.git` folder inside the project. The cases that write to `/tmp` use a folder
`/private/tmp/chirality-level-<run>/`. The run refuses to start if that folder
exists, makes it itself, and removes it afterwards.

"Edits" below is `on-request` with `workspaceWrite`; "supervised" is
`untrusted` with `readOnly`; "full access" is `never` with `dangerFullAccess`.
The level is sent on each turn (`turn/start` `approvalPolicy` and
`sandboxPolicy`) unless the row says otherwise.

## How an outcome is decided

Each assertion names one outcome of one scripted call. `judge` decides it from
the protocol stages that outcome has, each tied to the call's id:
- **ran and succeeded**: the output says exit 0, and Codex started a command
  item with the call's id;
- **ran and was refused by the sandbox**: the output says a non-zero exit and
  carries the refusal's own text ("operation not permitted", from the shell, or
  from the network probe, which prints the system's reason where curl would
  not);
- **declined**: an approval request with the call's id reached the fixture, and
  the output says rejected;
- **rejected by policy**: the output says so, and no request was raised for the
  call;
- **not offered**: the stub could not make the call. This is inconclusive: the
  test fails, saying so.

A turn that did not complete, a call the stub never issued, or an output
nobody recognises refuses. Every assertion that no request arrived keeps, in
the same test, a request arriving on the same client where one is expected.

## What the tests show

Each row is asserted by its test, as the row states it. The commands and
destinations named are the only ones tried. The 0.167.0 schema is the source
for the parameter names; no row rests on the schema alone.

| Fact | Test |
| --- | --- |
| **The examinations' level.** Edits with approval `never`, network off and both temporary folders excluded. The project write succeeds. Writes outside the project, to `TMPDIR`, to `/tmp` and into the project's `.git`, and the network probe, each run and are refused by the sandbox, with its text. A command asking for escalation is rejected by Codex's policy before it runs. No request of any kind arises on that thread. The control: on the same client, an escalation at edits raises a request. | `Presets.test_edits_that_never_ask_fail_whatever_needs_more_and_raise_nothing` |
| **Nothing sent** (what the App sends today). The reply reports `on-request`, `readOnly` with network off, and profile `:read-only`. The writes tried (the project, outside it, `TMPDIR`, `/tmp`, `.git`) and the network probe each run and are refused by the sandbox, and none raises a request. On the same thread, a command that asks for escalation raises `item/commandExecution/requestApproval` for that call. | `Presets.test_nothing_sent_is_on_request_read_only_and_a_refused_write_asks_no_one` |
| A write the sandbox refused completes no `commandExecution` item; a write that succeeds has one. | `Presets.test_a_write_the_sandbox_refused_completes_no_command_item` |
| **Supervised** raises a command approval, for that call, before every command tried: the five writes, the network probe and a plain `/bin/ls`. Each declined command does not run. | `Presets.test_supervised_asks_before_every_command_tried_and_a_declined_one_does_not_run` |
| **Edits, network off.** The writes to the project, `TMPDIR` and `/tmp` succeed. The writes outside the project and into `.git`, and the network probe, are refused by the sandbox. Nothing is asked, except for a command asking for escalation. | `Presets.test_edits_with_network_off` |
| **Edits, network on.** The same, except that the network probe connects to the stub. | `Presets.test_edits_with_network_on` |
| **Full access.** Every write tried, `.git` included, and the network probe succeed, and nothing is asked. A command asking for escalation is rejected by Codex's policy. The control: on the same client, an escalation at edits raises a request. | `Presets.test_full_access_writes_everywhere_tried_and_an_escalation_request_is_refused_by_codex` |
| `excludeSlashTmp` makes a write to `/tmp` refused, while `TMPDIR` stays writable. `excludeTmpdirEnvVar` makes a write to `TMPDIR` refused, while `/tmp` stays writable. | `Presets.test_the_two_temporary_folder_exclusions` |
| A `writableRoots` entry makes a write there succeed that is refused without it, and the project stays writable. | `Presets.test_an_extra_writable_root` |
| Under a scratch folder whose name holds spaces, single quotes, parentheses, a semicolon and an ampersand, the quoted commands write only their own targets, and nothing appears beside the folder. | `Presets.test_paths_with_spaces_and_shell_characters_stay_contained` |
| **Codex finding.** With a double quote in the project's path, the macOS sandbox profile Codex writes does not parse. A command under workspace write fails with `sandbox-exec`'s own parse error and does not run, so it fails closed. Under full access, which uses no sandbox, the same write succeeds. | `Presets.test_a_double_quote_in_the_project_path_makes_every_sandboxed_command_fail_to_start` |
| A setting sent on `thread/start` is held to and reported. A setting on `turn/start` is held to on that turn and on the next one sent with none. `thread/read` reports neither `approvalPolicy` nor `sandbox`. After a restart, `thread/resume` with none reports and holds the last setting, whether it was set at start or on a turn. `thread/resume` with a narrower setting reports it and holds to it. | `Carriers.test_thread_start_turn_start_and_resume` |
| `thread/start`, `thread/resume` and `thread/fork` take only a sandbox mode name. `config.sandbox_workspace_write` carries `network_access`, `exclude_slash_tmp`, `exclude_tmpdir_env_var` and `writable_roots`. Each reply reports the whole policy, and on start, fork and resume the allowed and the refused effects are each observed. | `Carriers.test_config_carries_the_workspace_write_options_on_start_fork_and_resume` |
| A writable root in the Codex home's `config.toml` (the person's own settings) widens workspace write, and the start reply lists it. `config.sandbox_workspace_write.writable_roots = []` on `thread/start` removes it: the write there is then refused, and the project's write succeeds. A turn's `sandboxPolicy` with `writableRoots: []` does not remove it: the write still succeeds. | `Carriers.test_writable_roots_from_the_home_config_are_removed_only_by_a_start_override` |
| Two home configurations were tried. One names the widest values: approval `never`, the automatic reviewer, full access, network on, neither temporary folder excluded. The other names a full-access permissions profile. In each, nothing sent gives the person's own: the reply reports them, and a write outside the project succeeds. The level sent at start, or on each turn alone, then decides approval, reviewer, sandbox, network and both exclusions. The project write succeeds; outside, `TMPDIR`, `/tmp` and the network probe are refused by the sandbox; an escalation raises a request for the call. Writable roots are the one exception (row above). | `Carriers.test_the_level_sent_wins_over_the_home_config_on_every_other_dimension` |
| `thread/fork` with none inherits the source's setting; with a setting, it applies it. Each fork reply reports it, and each fork is held to it: a write its level forbids is refused, and one it allows succeeds. A fork's requests to the provider carry no `tools`, yet a call made anyway runs. | `Carriers.test_fork` |
| A command started in one turn is still running when the turn completes. The next turn's narrower setting is in force (its own write is refused), yet the running command still writes outside the project. | `Narrowing.test_a_running_command_outlives_its_turn_and_a_narrower_next_turn` |
| A child spawned by `spawn_agent` is held to the parent's level. Under edits, its project write succeeds, its write outside is refused by the sandbox, and its escalation is declined at a request raised on the child's thread for that call. Under full access, both writes succeed and its escalation is rejected by policy. Neither child is offered `spawn_agent`, and each child's turn completes. | `Child.test_a_child_under_edits`, `Child.test_a_child_under_full_access` |
| **A call to an App-supplied tool** (`dynamicTools` at thread start) arrives on its thread and turn.<br>Unanswered for `LEVEL_HOLD_SECONDS`, the turn does not end and the server stays up; answered, the turn completes with the answer.<br>`turn/interrupt` ends the turn as interrupted, and by the end of that server's life no `serverRequest/resolved` was sent (the interval is in the test's message).<br>Ended with a call outstanding, the restarted server, after resume, never raised that call or the interrupted one again, through the rest of its life in the test (10 s and more). That turn reads interrupted.<br>After resume, a new call is raised and answered.<br>On a fork the tool is not listed to the model, yet a call is routed to the fork's thread and answered. | `AppTool.test_held_interrupted_relaunched_resumed_and_forked` |
| A child is not offered the App-supplied tool, and Codex answers its call as unsupported; nothing reaches the client. The control: the parent's own call reaches the client. | `AppTool.test_a_child_is_not_given_the_app_tool` |
| `request_user_input` is listed to the model in an ordinary conversation, but a call to it is refused in Default mode, and nothing reaches the client. In plan mode the call reaches the client as `item/tool/requestUserInput`. | `Question.test_offered_but_refused_in_default_mode`, `Question.test_reaches_the_client_in_plan_mode` |

## Read from the source, not shown by a fixture

`CODEX_EXEC_SERVER_URL`, `CODEX_HOME/environments.toml` and the
`CODEX_EXEC_SERVER_NOISE_*` variables. What these do was read from the public
source at `rust-v0.167.0`; none was set by any fixture. Set to a URL, or
configured by the file, they move commands and file edits to another exec
server, where this Mac's sandbox does not apply, while the replies report the
same policy.
