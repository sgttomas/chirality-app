# Sandbox and approval settings at Codex 0.167.0

What the pinned Codex app server does with the approval and sandbox settings a
client may send. The tests start it against a loopback stub that scripts the
model's tool calls: no model, no sign-in, no credential. They are facts about
the supplier at the pin, kept as tests so that they keep guarding it. They
qualify no App candidate.

## What a pass means

**Acceptance rule.** A test passes only when it has observed what its row
names: for the listed operations, at the levels stated, within the stated
observation window. The observations are the protocol stages of each call,
tied to the call's id (see "How an outcome is decided"), and the effects on
the file system and on the stub.

**The fixture's own inputs are fixed, and this is enforced before anything
reaches Codex:**
- **The commands.** The only commands a scripted shell call may carry are
  those of `Run.commands()`. The stub refuses any other before issuing it
  (`ScriptedStub.answer`, against `allowed_commands`, which `Run.__enter__`
  sets), so such a call never reaches Codex.
- **The paths.** Every path lies under a scratch base the fixture checks
  (`checked_scratch`, called by `Run`). The base and each of its ancestors
  must be free of `$`, a backquote, `"` and `\`, the characters a shell
  expands or mishandles inside double quotes. Only the project folder's own
  name may differ, and only in the one test that needs it (`project_name`).
  Every path in a command is quoted for the shell.

**The faults the suite has been shown to reject.** Each class below was
introduced on purpose, and the tests concerned then failed or were
inconclusive. The second independent reading did this by hand across the suite
(137 calls removed, 132 completions suppressed, 125 effects inverted, 54
non-sandbox failures substituted). The stub-only tests do it for the judge
itself.
- a tested call removed from the script;
- a turn's completion suppressed;
- a command's effect inverted;
- a command failing for a reason that is not the sandbox, including the words
  "operation not permitted" printed by the command or held in its path, and the
  refusal line for a different target;
- a reply reporting one policy while the effects are another's;
- a declined command whose item ran, or carries an exit code;
- a fork's effective approval inverted;
- a call raised as the server ends, and a reader that stopped before the end of the output;
- an item of another type or turn carrying the call's id;
- a command off the fixed list;
- a scratch base holding an expanding character;
- a process of the run left behind, and a permission error from the final
  signal while the group has members.

This shows the tests are sensitive to those faults. It does not show that
every possible false pass is excluded.

**Not guarded, and so stated:**
- a command or a path written to imitate evidence: the fixture writes all of
  them;
- a process of the run whose command line names no path of the run. After the
  servers stop, `Run.nothing_remains` waits until no process names the run's
  root, or fails listing each one that does. The network probe is such a
  process: its argument is only the port. It bounds its whole run with a 3 s alarm, connection and read
  included.

## Files

- `level_fixture.py`: the stub, a fresh root per run, the App side of the
  JSON-RPC exchange, and `judge`. Every approval request the fixture receives
  is declined.
- `test_level_live.py`: one fact per test.
  - It needs `CHIRALITY_CODEX_BIN` set to the pinned binary, whose digest is
    checked before every start, and is skipped otherwise.
  - The full suite's product job (`.github/workflows/app-v4.yml`) runs it with
    `LEVEL_REQUIRE_LIVE=1`, under which a missing binary fails instead of
    skipping. An unpinned binary fails either way.
  - `LEVEL_SCRATCH` names the scratch base, which the check above admits or
    refuses. `LEVEL_HOLD_SECONDS` sets how long a call to an App-supplied tool
    is left unanswered (default 120).
- `test_level_stub.py`: the stub, the run's folders, the fixed commands, the
  guards above, the cleanup and `judge`, with no Codex. It runs in
  `repository-checks`.

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
`/private/tmp/chirality-level-<run>/` that the run refuses to start if it
exists, makes itself, and removes afterwards.

"Edits" below is `on-request` with `workspaceWrite`; "supervised" is
`untrusted` with `readOnly`; "full access" is `never` with `dangerFullAccess`.
The level is sent on each turn (`turn/start` `approvalPolicy` and
`sandboxPolicy`) unless the row says otherwise.

## How an outcome is decided

`judge` decides each scripted call's outcome from the protocol stages that
outcome has, tied to the call's id:
- **ran and succeeded**: the output says exit 0, and a `commandExecution` item
  with the call's id started in the call's own turn;
- **ran and was refused by the sandbox**: a non-zero exit, and the whole output
  is exactly the refusal line for the expected target. For a write, that is
  the line zsh, bash or sh prints naming that path and "operation not
  permitted". For the network probe (a perl connect, because curl prints the
  same text for a sandbox refusal and a closed port), it is its own
  "connect failed: Operation not permitted". Any other failure is
  inconclusive when a refusal was expected;
- **declined**: an approval request with the call's id reached the fixture, the
  output says rejected, and the call's item completed `declined` with no exit
  code. This does not show that the command never ran; it shows what is observed;
- **rejected by policy**: the output says so, and no request was raised for
  the call;
- **not offered**: the stub could not make the call. This is inconclusive, and
  the test fails.

A turn that did not complete, a call the stub never issued, or an output
nobody recognises refuses.

## What the tests show

Each row is asserted by its test as stated, for the operations named, and
names its control. A row marked **observation** states its window and has no
control.

| Fact | Control | Test |
| --- | --- | --- |
| **The examinations' level.** Edits with approval `never`, network off and both temporary folders excluded. The project write succeeds. Writes outside the project, to `TMPDIR`, to `/tmp` and into `.git`, and the network probe, each run and are refused by the sandbox. A command asking for escalation is rejected by policy. No request of any kind arises on that thread in the test. | On the same client, an escalation at edits raises a request. | `Presets.test_edits_that_never_ask_fail_whatever_needs_more_and_raise_nothing` |
| **Nothing sent** (what the App sends today). The reply reports `on-request`, `readOnly` with network off, and profile `:read-only`. Each write tried and the network probe are refused by the sandbox, with no request. | On the same thread, an escalation raises a request for that call. | `Presets.test_nothing_sent_is_on_request_read_only_and_a_refused_write_asks_no_one` |
| **The temporary folder's entries, with nothing sent.** The App's layout, with invented names: a fresh Codex home with new, empty settings inside an invented data folder, and `TMPDIR` a folder made inside `codex-tmp` in the `<data folder> Working Files` folder beside it. Each command tried is refused by the sandbox with its own exact line, and nothing is asked: renaming the temporary folder's entry; removing it and making it again; moving it aside to put a link in its place; making a new link beside it; renaming `codex-tmp`, removing it, and moving it aside for a link; renaming the Working Files folder, and making a link inside it. Afterwards each folder from the run's root down to the temporary folder is the same folder, by device and inode, and each holds the same names. A write inside the temporary folder itself is also refused: with nothing sent, a sandboxed command cannot use the folder the App gives Codex as `TMPDIR`. | At full access each of these succeeds and is seen to take effect, except removing the non-empty `codex-tmp`, which fails with `Directory not empty`, where the sandbox refused it with `Operation not permitted`. The write inside succeeds. On the same thread, an escalation raises a request. | `TemporaryFolderEntries.test_with_nothing_sent_no_entry_on_the_temporary_folders_path_changes`, `TemporaryFolderEntries.test_at_full_access_the_same_operations_change_the_entries` |
| A write the sandbox refused completes no `commandExecution` item. | On the same thread, a write that succeeds has one. | `Presets.test_a_write_the_sandbox_refused_completes_no_command_item` |
| **Supervised** raises a command approval, for that call, before every command tried: the five writes, the network probe and a plain `/bin/ls`. For each declined command, what is observed is the decline's own output, a completed item ended `declined` with no exit code, and no effect on its file or the network. | Every row is its own: each request is tied to its call. | `Presets.test_supervised_asks_before_every_command_tried_and_a_declined_one_does_not_run` |
| **Edits, network off.** The project, `TMPDIR` and `/tmp` writes succeed. Outside, `.git` and the network probe are refused by the sandbox. An escalation is declined at its request. | The allowed and refused writes on the same thread. | `Presets.test_edits_with_network_off` |
| **Edits, network on.** The same, except that the network probe connects to the stub. | As above. | `Presets.test_edits_with_network_on` |
| **Full access.** Every write tried and the network probe succeed, and nothing is asked. An escalation is rejected by policy. | On the same client, an escalation at edits raises a request. | `Presets.test_full_access_writes_everywhere_tried_and_an_escalation_request_is_refused_by_codex` |
| `excludeSlashTmp` makes a `/tmp` write refused while `TMPDIR` stays writable; `excludeTmpdirEnvVar` the reverse. | Each exclusion's other folder, and the project. | `Presets.test_the_two_temporary_folder_exclusions` |
| A `writableRoots` entry makes a write there succeed that is refused without it. | The same write without the entry. | `Presets.test_an_extra_writable_root` |
| Under a scratch base whose name holds spaces, single quotes, parentheses, a semicolon and an ampersand, the commands write only their own targets, and nothing appears beside the base. | The refused write outside the project. | `Presets.test_paths_with_spaces_and_shell_characters_stay_contained` |
| **Codex finding.** With a double quote in the project folder's name, the macOS sandbox profile Codex writes does not parse. A command under workspace write fails with `sandbox-exec: unbound variable:` and does not run, so it fails closed. | Full access in the same project succeeds, and the same level in a plain project succeeds. | `Presets.test_a_double_quote_in_the_project_path_makes_every_sandboxed_command_fail_to_start` |
| **Carriers.** A setting sent on `thread/start` is held to and reported. A setting on `turn/start` is held to on that turn and the next one sent with none. After a restart, `thread/resume` with none reports and holds the last setting. `thread/resume` with a narrower setting reports and holds it. Each approval stated is shown by an escalation: rejected under `never`, declined under `on-request`. `thread/read` reports neither `approvalPolicy` nor `sandbox`. | The same thread before the turn's setting (refused), and the narrowed resume (refused, and declined). | `Carriers.test_thread_start_turn_start_and_resume` |
| **The config carrier.** `thread/start`, `thread/fork` and `thread/resume` take only a sandbox mode name (from the 0.167.0 schema, not a test); `config.sandbox_workspace_write` carries `network_access`, both exclusions and `writable_roots`. A root given at start is writable. The fork's `[]` removes it, so that write is refused. Resume gives it again, so it is writable again. Each reply reports the whole policy, and each policy's allowed and refused effects are observed. | Each step's opposite effects. | `Carriers.test_config_carries_the_workspace_write_options_on_start_fork_and_resume` |
| **The writable-roots override.** A writable root in the Codex home's `config.toml` (the person's own settings) widens workspace write, and the start reply lists it. `writable_roots = []` through `config` on `thread/start` removes it: the write there is refused. A turn's `sandboxPolicy` with `writableRoots: []` does not remove it: the write succeeds. | The project write succeeds where the root is removed. | `Carriers.test_writable_roots_from_the_home_config_are_removed_only_by_a_start_override` |
| **The level wins.** Two home configurations were tried: one names approval `never`, the automatic reviewer, full access, network on and neither temporary folder excluded; the other names a full-access permissions profile. With nothing sent, the reply reports the person's own, and a write outside the project succeeds. The level sent at start, or on each turn alone, decides approval, reviewer, sandbox, network and both exclusions: the project write succeeds; outside, `TMPDIR`, `/tmp` and the network probe are refused; an escalation is declined at its request. Writable roots are the exception (row above). | The unsent thread's own effects. | `Carriers.test_the_level_sent_wins_over_the_home_config_on_every_other_dimension` |
| **Fork.** `thread/fork` with none inherits; with a setting, applies it; each reply reports it. Each fork's approval is shown by an escalation: rejected under `never`, declined at its request under `on-request`. A full-access fork writes outside and reaches the network. A read-only fork's writes in and outside the project are refused, and its read succeeds. A fork's requests to the provider carry no `tools`, yet a call made anyway runs. | Each fork's allowed and forbidden operations. | `Carriers.test_fork` |
| **A fork's first turn.** The level sent on a fork's first turn, as on every turn, governs that turn, whatever the fork inherited. A fork of a full-access thread whose first turn sends read-only refuses the project write and declines an escalation at its request. A fork of a read-only thread whose first turn sends edits writes in the project and is refused outside it. | Each source thread's own effects before the fork. | `Carriers.test_a_forks_first_turn_is_governed_by_the_level_sent_on_that_turn` |
| **Narrowing.** A command started in one turn is still running when the turn completes. On the next turn read-only is in force: the project write, which workspace write would allow, is refused. Yet the running command still writes outside the project. | The refused project write on the narrowed turn. | `Narrowing.test_a_running_command_outlives_its_turn_and_a_narrower_next_turn` |
| **A child** spawned by `spawn_agent` is held to the parent's level. Under edits, its project write succeeds, its write outside is refused, and its escalation is declined at a request raised for that call on the child's thread. Under full access, both writes succeed and its escalation is rejected by policy. Neither child is offered `spawn_agent`, and each child's turn completes. | Each child's allowed and forbidden writes. | `Child.test_a_child_under_edits`, `Child.test_a_child_under_full_access` |
| **A call to an App-supplied tool** (`dynamicTools` at thread start) arrives on its thread and turn. Unanswered for `LEVEL_HOLD_SECONDS`, the turn does not end and the server stays up; answered, the turn completes with the answer. `turn/interrupt` ends the turn as interrupted. After a restart and resume, a new call is raised and answered. On a fork the tool is not listed to the model, yet a call is routed to the fork's thread and answered. | The answer completing the held turn; the new calls on the restarted server. | `AppTool.test_held_interrupted_relaunched_resumed_and_forked` |
| **Observation:** no `serverRequest/resolved` arrived for the interrupted call during that server's whole life, read to its end. The window is from the interrupt to the server's end, stated in the test's message. | None. | same test |
| **Observation:** after the restart, the call outstanding when the server ended, and the interrupted one, were never raised again in the second server's whole life, read to its end (from resume to its stop, 10 s and more). | New calls on the same client were raised. | same test |
| A child is not offered the App-supplied tool, and Codex answers its call as unsupported; nothing reaches the client. | The parent's own call reaches the client. | `AppTool.test_a_child_is_not_given_the_app_tool` |
| `request_user_input` is listed in an ordinary conversation, but a call to it is refused in Default mode, and nothing reaches the client. In plan mode the call reaches the client as `item/tool/requestUserInput`. | Each mode, on one client, is the other's. | `Question.test_refused_in_default_mode_and_reaches_the_client_in_plan_mode` |

One further observation about the supplier is held out of this folder pending
the owner's decision.

## What the temporary folder row does not show

- Other operations on these entries: a hard link, an exchange of two entries, a change of owner, mode, access list, extended attribute or times, or a mount.
- Ancestors above the Working Files folder: the data folder and the run's root were compared afterwards, but no operation on them was tried. The App's real folders sit under the person's Library, with other names and depth.
- Any level other than nothing sent. The read-only sandbox refuses every write; nothing in this row is particular to these folders.
- A process outside the sandbox: an approved escalation, a command allowed by a lasting rule, full access, Codex's own server process, the App, or another program. Any of these can change the entries.
- The App's own checks when it makes these folders.

## Read from the source, not shown by a fixture

`CODEX_EXEC_SERVER_URL`, `CODEX_HOME/environments.toml` and the
`CODEX_EXEC_SERVER_NOISE_*` variables. What these do was read from the public
source at `rust-v0.167.0`; no fixture set any of them. Set to a URL, or
configured by the file, they move commands and file edits to another exec
server, where this Mac's sandbox does not apply, while the replies report the
same policy.
