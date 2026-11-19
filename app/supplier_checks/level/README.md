# Sandbox and approval settings at Codex 0.169.0

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
- a process of the run outside the servers' process groups. After the servers
  stop, `Run.nothing_remains` waits until none of the Codex servers the run
  started is running (known by its number and the start time recorded when it
  started) and each server's process group is empty (a signal 0 to the group),
  or fails naming each that is not. It reads no process's command line or open
  files. A command Codex ran in a process group of its own is not seen there:
  the rows that start such commands print their numbers and end them themselves
  (`end_known`). The network probe is not one of the servers; it bounds its
  whole run with a 3 s alarm, connection and read included.

## Files

- `level_fixture.py`: the stub, a fresh root per run (with, where a test asks,
  a second project folder), the App side of the JSON-RPC exchange, and
  `judge`. Every approval request the fixture receives is declined.
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
app-server`), with an environment built whole. The default fixture start omits
the question feature. The feature tests add the same session flag the App
supplies. The environment:
- `PATH`, with the package's `codex-path` first;
- `HOME`, `CODEX_HOME` and `TMPDIR`, all inside the run's root;
- `TZ` and `LANG`;
- the examination launcher's proxy overrides.

The stub answers the WebSocket upgrade with 426, so Codex uses HTTP at once.
The project has no `.git` above it, as the launcher requires; some cases put a
`.git` folder inside the project. The app server is always started in the
project, A. The folder-per-conversation rows add a second project, B, beside
A in the run's root (`Run(second_project=...)`), made with the same care, and,
as each row says, an invented `AGENTS.md` with a marker line of its own or an
invented `.codex/config.toml` naming a writable root of its own under
`outside`, in each of A and B. The cases that write to `/tmp` use a folder
`/private/tmp/chirality-level-<run>/` that the run refuses to start if it
exists, makes itself, and removes afterwards; the case that writes to
`/private/var/tmp` uses `/private/var/tmp/chirality-level-<run>/` on the same
terms.

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
| **The temporary folder's entries, with nothing sent.** The App's layout, with invented names: a fresh Codex home with new, empty settings inside an invented data folder, and `TMPDIR` a folder made inside `codex-tmp` in the `<data folder> Working Files` folder beside it. The start reply reports `on-request`, `readOnly` and `:read-only`. Each command tried exits non-zero with its own exact refusal line, and no request arises: renaming the temporary folder's entry; removing it and making it again; moving it aside to put a link in its place; making a new link beside it; renaming `codex-tmp`, removing it, and moving it aside for a link; renaming the Working Files folder, and making a link inside it. Each compound command stops at its refused first step, so its `mkdir` or replacement link is never reached. Afterwards, at the points sampled, the run's root, the data folder, the Working Files folder, `codex-tmp` and the temporary folder are each the same folder by device, inode and type. The data folder is the Working Files folder's sibling, not an ancestor of the temporary folder. The run's root, the Working Files folder and `codex-tmp` held the same names; the data folder's and the temporary folder's contents are not listed. The tested sandboxed write inside the temporary folder was refused too. | At full access each of these succeeds and is seen to take effect, except removing the non-empty `codex-tmp`, which fails with `Directory not empty`, where the sandbox refused it with `Operation not permitted`. The write inside succeeds. On the same thread, an escalation raises a request. | `TemporaryFolderEntries.test_with_nothing_sent_no_entry_on_the_temporary_folders_path_changes`, `TemporaryFolderEntries.test_at_full_access_the_same_operations_change_the_entries` |
| A write the sandbox refused completes no `commandExecution` item. | On the same thread, a write that succeeds has one. | `Presets.test_a_write_the_sandbox_refused_completes_no_command_item` |
| **Supervised** raises a command approval, for that call, before every command tried: the five writes, the network probe and a plain `/bin/ls`. For each declined command, what is observed is the decline's own output, a completed item ended `declined` with no exit code, and no effect on its file or the network. This does not show that a declined command never ran. | Every row is its own: each request is tied to its call. | `Presets.test_supervised_asks_before_every_command_tried_and_a_declined_one_shows_no_effect` |
| **Edits, network off.** The project, `TMPDIR` and `/tmp` writes succeed. Outside, `.git` and the network probe are refused by the sandbox. An escalation is declined at its request. | The allowed and refused writes on the same thread. | `Presets.test_edits_with_network_off` |
| **Edits, network on.** The same, except that the network probe connects to the stub. | As above. | `Presets.test_edits_with_network_on` |
| **Full access.** Every write tried and the network probe succeed, and nothing is asked. An escalation is rejected by policy. | On the same client, an escalation at edits raises a request. | `Presets.test_full_access_writes_everywhere_tried_and_an_escalation_request_is_refused_by_codex` |
| **`/private/var/tmp`.** Under each of the App's three edits levels (edits, edits with network, edits that never ask), each sending both temporary folder exclusions as the App does, a write in the run's own folder under `/private/var/tmp` runs and is refused by the sandbox. The source has a scratch grant for `/private/tmp` and `/private/var/tmp` when the platform defaults are included under the process profile (`sandboxing/src/seatbelt.rs:899-909`). This row shows that the grant did not make `/private/var/tmp` writable in this configuration. It does not establish which of those conditions was false. | At full access the same write succeeds; on each edits thread, the project write succeeds. | `Presets.test_no_edits_level_writes_in_private_var_tmp` |
| `excludeSlashTmp` makes a `/tmp` write refused while `TMPDIR` stays writable; `excludeTmpdirEnvVar` the reverse. | Each exclusion's other folder, and the project. | `Presets.test_the_two_temporary_folder_exclusions` |
| A `writableRoots` entry makes a write there succeed that is refused without it. | The same write without the entry. | `Presets.test_an_extra_writable_root` |
| Under a scratch base whose name holds spaces, single quotes, parentheses, a semicolon and an ampersand, the commands write only their own targets, and nothing appears beside the base. | The refused write outside the project. | `Presets.test_paths_with_spaces_and_shell_characters_stay_contained` |
| **Codex finding.** With a double quote in the project folder's name, the macOS sandbox profile Codex writes does not parse. A command under workspace write fails with `sandbox-exec: unbound variable:` and does not run, so it fails closed. | Full access in the same project succeeds, and the same level in a plain project succeeds. | `Presets.test_a_double_quote_in_the_project_path_prevents_the_workspace_write_command_from_starting` |
| **The App's own table.** Each row of `app/src-tauri/src/codex_levels.json` is sent as the App sends it: on `thread/start`, the approval, reviewer `user`, the mode name and the workspace options through `config`; on each turn, the approval, reviewer and structured policy. The start reply reports the row's approval, reviewer `user` and every field of its policy. Then each row's stated dimensions are observed. Writes "project": the project write succeeds; outside, `.git`, `TMPDIR` and `/tmp` are refused. Writes "everywhere": all of them succeed. Network on: the probe connects; off: it is refused. Asks "when beyond the sandbox": an escalation is declined at its request. Asks "never": it is rejected by policy. Supervised ("before a command not known safe"): the project write and a plain read are each put to the person first. Its writes' own effects are not observed here, because the client declines; the read-only sandbox's effects are shown in the "nothing sent" row. | Each row's refused and allowed effects on one thread. For "never", on the same client, an escalation at edits raises a request. | `Table.test_each_row_of_the_apps_table_does_what_its_dimensions_say` |
| **Carriers.** A setting sent on `thread/start` is held to and reported. A setting on `turn/start` is held to on that turn and the next one sent with none. After a restart, `thread/resume` with none reports and holds the last setting. `thread/resume` with a narrower setting reports and holds it. Each approval stated is shown by an escalation: rejected under `never`, declined under `on-request`. `thread/read` reports neither `approvalPolicy` nor `sandbox`. | The same thread before the turn's setting (refused), and the narrowed resume (refused, and declined). | `Carriers.test_thread_start_turn_start_and_resume` |
| **The config carrier.** `thread/start`, `thread/fork` and `thread/resume` take only a sandbox mode name (from the 0.169.0 schema, not a test); `config.sandbox_workspace_write` carries `network_access`, both exclusions and `writable_roots`. A root given at start is writable. The fork's `[]` removes it, so that write is refused. Resume gives it again, so it is writable again. Each reply reports the whole policy, and each policy's allowed and refused effects are observed. | Each step's opposite effects. | `Carriers.test_config_carries_the_workspace_write_options_on_start_fork_and_resume` |
| **The writable-roots override.** A writable root in the Codex home's `config.toml` (the person's own settings) widens workspace write, and the start reply lists it. `writable_roots = []` through `config` on `thread/start` removes it: the write there is refused. A turn's `sandboxPolicy` with `writableRoots: []` does not remove it: the write succeeds. | The project write succeeds where the root is removed. | `Carriers.test_writable_roots_from_the_home_config_are_removed_only_by_a_start_override` |
| **The level wins.** Two home configurations were tried: one names approval `never`, the automatic reviewer, full access, network on and neither temporary folder excluded; the other names a full-access permissions profile. With nothing sent, the reply reports the person's own, and a write outside the project succeeds. The level sent at start, or on each turn alone, decides approval, reviewer, sandbox, network and both exclusions: the project write succeeds; outside, `TMPDIR`, `/tmp` and the network probe are refused; an escalation is declined at its request. Writable roots are the exception (row above). | The unsent thread's own effects. | `Carriers.test_the_level_sent_wins_over_the_home_config_on_every_other_dimension` |
| **Fork.** `thread/fork` with none inherits; with a setting, applies it; each reply reports it. Each fork's approval is shown by an escalation: rejected under `never`, declined at its request under `on-request`. A full-access fork writes outside and reaches the network. A read-only fork's writes in and outside the project are refused, and its read succeeds. A fork's requests to the provider carry no `tools`, yet a call made anyway runs. | Each fork's allowed and forbidden operations. | `Carriers.test_fork` |
| **A fork's first turn.** The level sent on a fork's first turn, as on every turn, governs that turn, whatever the fork inherited. A fork of a full-access thread whose first turn sends read-only refuses the project write and declines an escalation at its request. A fork of a read-only thread whose first turn sends edits writes in the project and is refused outside it. | Each source thread's own effects before the fork. | `Carriers.test_a_forks_first_turn_is_governed_by_the_level_sent_on_that_turn` |
| **Narrowing.** A command started in one turn is still running when the turn completes. On the next turn read-only is in force: the project write, which workspace write would allow, is refused. Yet the running command still writes outside the project. | The refused project write on the narrowed turn. | `Narrowing.test_a_running_command_outlives_its_turn_and_a_narrower_next_turn` |
| **A trust mark written into the settings.** At full access, in the App's layout with the home's new, empty settings, `thread/start` in a git project with no project trust entry writes `[projects."<project>"] trust_level = "trusted"` into the home's `config.toml`. With one entry for the project's root, `trust_level = "untrusted"`, as the App sends it, nothing is written. | Each start is the other's control. | `TrustWrite.test_a_git_project_is_marked_trusted_in_the_settings_unless_an_entry_is_sent` |
| **A worktree's trust mark.** The same in a git worktree (a `.git` file pointing into another repository's `.git/worktrees`): with no entry, the trust mark is written for the main repository, not the worktree. One entry for the worktree's own root is enough: nothing is written. | Each start is the other's control. | `TrustWrite.test_a_worktree_marks_its_main_repository_unless_an_entry_for_the_worktree_is_sent` |
| **Asking about each command, inside the project.** Approval `untrusted` with a workspace-write sandbox (not one of the App's levels), reported back as such. A command that writes outside the project is put to the person once. Declined, nothing is written. Allowed, the write outside the project succeeds: the allowed command is not kept inside the project's sandbox. At the pinned Codex, asking about each command does not keep what is allowed inside the project. | The same command, declined. | `AskEachCommandInsideTheProject.test_an_allowed_command_is_not_kept_inside_the_project` |
| **A running process on a narrower turn.** A command started at full access with a terminal (`echo PID $$; exec cat > <outside>/w-held`, the same held command as the row on what ends a running process) is still running when a later turn runs at each narrower level of the App's own table. On that turn the agent tries to write to the process. At `supervised`, `edits` and `edits-network`, the attempt first raises a command approval request, whose reason says the terminal "runs without a filesystem sandbox"; declined, nothing reaches the process. At `edits-no-asking` (`never`), no request is raised and the attempt is refused ("approval required by policy, but AskForApproval is set to Never"); nothing reaches the process. | Accepted at `supervised`, the line is written outside the project. | `RunningProcess.test_each_narrower_level_of_the_apps_table_asks_or_refuses_before_it_uses_a_process_started_at_full_access` |
| **What ends a running process.** `turn/interrupt` of a later turn does not end running processes. The turn ends `interrupted`, yet afterwards `thread/backgroundTerminals/list` still lists that turn's own `sleep 20`, and the held process still takes input at full access. `thread/backgroundTerminals/clean` ends the held process: that process, known by the number it printed and its start time, is gone, and writing to it then fails with `Unknown process id`. Not shown: that cleaning also ends processes the held one started. | Input before and after cleaning. | `RunningProcess.test_an_interrupt_leaves_running_processes_and_cleaning_ends_them` |
| **Ending Codex normally ends background commands.** Two commands are left running at full access: one with a terminal (`sleep 7771 & echo PIDS $! $$; exec cat > <outside>/w-held`) and one without (`sleep 7772 & echo PIDS $! $$; exec sleep 7773`). Each prints its background child's process number and its own, then becomes its last program; the four processes are checked by number and start time, and no other process is searched. Each runs in a process group of its own, not the server's. Codex's input is closed, as the App's stop does first, and the server's process group is empty within the 3 s the App waits for it. All four processes, the commands and what they started, have ended, before any process group is signalled. | Each process is seen running before. | `QuitEnds.test_closing_codexs_input_ends_background_commands_and_what_they_started` |
| **Ending Codex at once leaves a background command without a terminal.** The same two commands. The server's whole process group is killed at once, as a crash would end it, or the App's forced end if the server has not exited within 3 s. The terminal's command and what it started end. The command without a terminal, and what it started, keep running: they are in process groups of their own, so they outlive Codex. The test then ends them itself. | The terminal's commands, which end. | `QuitEnds.test_when_codex_is_ended_at_once_a_background_command_without_a_terminal_outlives_it` |
| **Cleaning ends background commands while Codex runs.** The same two commands. With Codex still running, `thread/backgroundTerminals/clean` on the conversation ends both commands and what they started, the command without a terminal included. | Each process is seen running before. | `QuitEnds.test_with_codex_answering_cleaning_ends_a_command_without_a_terminal_and_what_it_started` |
| **A background command's item.** A command left running when its turn completes was started as an item with status `inProgress` and a process id. Once the turn has completed, the item has not completed. When the process ends, the item completes with status `completed` and exit code 0. | The turn's own completion, observed before the item's. | `Background.test_a_background_commands_item_stays_in_progress_after_its_turn_and_completes_when_it_ends` |
| **What the App's account read contacts.** On an account home with no sign-in, `account/read` (empty params) answers `account: null` and no attempt is recorded during it. With an INVENTED ChatGPT sign-in (a made-up `auth.json` in the run's own home, kept in that file by `cli_auth_credentials_store = "file"`), `account/read` tries `chatgpt.com:443`, and may try `auth.openai.com:443`: the workspace routing discovery, read in the source as `get_accounts_check` on `chatgpt_base_url`. Refused, the read answers an error and never an account. In both cases Codex itself tries `chatgpt.com:443` at start, before any request from the client. Each read is made after Codex's own attempts have stopped for 3 s. | The two homes are each other's control. | `AccountRead.test_with_no_sign_in_the_account_read_contacts_nothing_and_reports_no_account`, `AccountRead.test_with_an_invented_sign_in_the_account_read_contacts_the_account_server_and_fails_when_refused` |
| **The model list read contacts nothing itself.** In both homes `model/list` answers the list, and no attempt is recorded during it. Not shown: what Codex's own background model refresh contacts at start. | As above. | same tests |
| **The history list read contacts nothing.** In both homes `thread/list` (`sortDirection` `desc`, as the App sends it) answers a list, and no attempt is recorded during it. | As above. | same tests |
| **A child** spawned by `spawn_agent` is held to the parent's level. Under edits, its project write succeeds, its write outside is refused, and its escalation is declined at a request raised for that call on the child's thread. Under full access, both writes succeed and its escalation is rejected by policy. Neither child is offered `spawn_agent`, and each child's turn completes. | Each child's allowed and forbidden writes. | `Child.test_a_child_under_edits`, `Child.test_a_child_under_full_access` |
| **A call to an App-supplied tool** (`dynamicTools` at thread start) arrives on its thread and turn. Unanswered for `LEVEL_HOLD_SECONDS`, the turn does not end and the server stays up; answered, the turn completes with the answer. `turn/interrupt` ends the turn as interrupted. After a restart and resume, a new call is raised and answered. On a fork the tool is not listed to the model, yet a call is routed to the fork's thread and answered. | The answer completing the held turn; the new calls on the restarted server. | `AppTool.test_held_interrupted_relaunched_resumed_and_forked` |
| **Observation:** no `serverRequest/resolved` arrived for the interrupted call during that server's whole life, read to its end. The window is from the interrupt to the server's end, stated in the test's message. | None. | same test |
| **Observation:** after the restart, the call outstanding when the server ended, and the interrupted one, were never raised again in the second server's whole life, read to its end (from resume to its stop, 10 s and more). | New calls on the same client were raised. | same test |
| A child is not offered the App-supplied tool, and Codex answers its call as unsupported; nothing reaches the client. | The parent's own call reaches the client. | `AppTool.test_a_child_is_not_given_the_app_tool` |
| `request_user_input` is listed in an ordinary conversation, but a call to it is refused in Default mode, and nothing reaches the client. In plan mode the call reaches the client as `item/tool/requestUserInput`. | Each mode, on one client, is the other's. | `Question.test_refused_in_default_mode_and_reaches_the_client_in_plan_mode` |
| **A question in an ordinary conversation, with the feature.** Codex is started with `-c features.default_mode_request_user_input=true` (a feature the supplier marks under development, off by default) and no collaboration mode is sent on any turn. At each row of the App's table, sent as the App sends it, a `request_user_input` call reaches the client as `item/tool/requestUserInput` on its thread and turn, with the question's id, header, wording and options unchanged, `isOther` true, `isBlocking` false and no automatic resolution timeout, and it is the only request raised in that server's whole life, read to the end of its output after the turn completed. Until it is answered the turn does not complete; the answer given reaches the agent as given. | Without the feature, the same start at full access refuses the call ("unavailable in Default mode") and raises nothing. | `QuestionInAnOrdinaryConversation.test_at_every_level_of_the_apps_table_the_question_reaches_the_client_and_its_answer_reaches_the_agent`, `QuestionInAnOrdinaryConversation.test_without_the_feature_the_same_start_refuses_the_question` |
| **The feature named off in the home's own settings.** With `[features] default_mode_request_user_input = false` in the home's `config.toml` and the same session flag given, the question still reaches the client and its answer the agent, and the file is unchanged afterwards. | A fresh home with the same settings, started without the flag, refuses the call and raises no question request. | `QuestionInAnOrdinaryConversation.test_with_the_feature_off_in_the_homes_own_settings_the_session_flag_still_raises_the_question` |
| **A question left waiting, declined, interrupted, and outstanding when Codex ends.** At full access with the feature. Unanswered for `LEVEL_HOLD_SECONDS`, the turn does not end, the server stays up and the agent is told nothing; then a free answer reaches the agent as given. An answer with no answers reaches the agent as `{"answers":{}}`. `turn/interrupt` ends the turn as interrupted and the call is not answered. After the server is ended with a question outstanding and the conversation is resumed on a new server, that turn reads interrupted; a new question on the resumed conversation, and one on a fork of it, are raised and answered. | The answers completing the held turns; the new questions on the restarted server. | `QuestionInAnOrdinaryConversation.test_held_declined_interrupted_relaunched_resumed_and_forked` |
| **Observation:** after the restart, the question outstanding when the server ended, and the interrupted one, were never raised again in the second server's whole life, read to its end. | New questions on the same client were raised. | same test |
| **A child's question.** With the feature, a child spawned by `spawn_agent` that calls `request_user_input` is answered "request_user_input can only be used by the root thread"; nothing reaches the client on the child's thread. | The parent's own question reaches the client. | `QuestionInAnOrdinaryConversation.test_a_childs_question_is_refused_and_reaches_no_one` |
| **What a catalogue model is told.** For a model with an entry in Codex's bundled catalogue (`gpt-6.1-sol`), the request to the provider carries no `tools`. With the feature, the request holds the tool's description "This tool is only available in Default or Plan mode" and the catalogue's own Default-mode words: to use the tool "only for optional questions where the answer would materially improve" the work and, with no answers, to "continue with best judgment instead of asking again". A call is raised and answered. Not shown: what any model does with those words. | Without the feature, the request does not hold that description and the call is refused. | `QuestionInAnOrdinaryConversation.test_what_a_catalogue_model_is_told_about_the_tool_with_and_without_the_feature` |
| **The question that does not wait.** With no feature set and no collaboration mode sent, on a model whose catalogue entry lists it (`gpt-6.1-sol`), a `request_user_input_async` call returns `{"accepted":true}` without waiting for a person's answer and raises no request. The turn completes with no answer from anyone. The question arrives as an `agentMessage` item whose id is the call's, with `delivery` `async` and `questions` as given (a title and option strings). After the server is ended and the conversation resumed, `thread/read` with its turns still holds that item and its questions. Not shown: how a reply is tied to the question; the source says it arrives as an ordinary next message. | On the fixture's invented model, which has no catalogue entry, the same call is answered as unsupported and no such item arrives. | `QuestionThatDoesNotWait.test_the_question_arrives_as_an_agent_message_item_and_the_turn_does_not_wait`, `QuestionThatDoesNotWait.test_on_a_model_the_catalogue_does_not_list_it_for_the_same_call_is_unsupported` |
| **A plain resume gives the question; the reply is an ordinary message after it.** On the same catalogue model, a `request_user_input_async` call is answered `{"accepted":true}` and the turn completes; among that turn's completed `agentMessage` items the question (id the call's) comes before the agent's closing message. Codex is ended at once (its process group killed) and started again. The reply to `thread/resume`, with nothing further read, holds in `thread.turns[].items[]` that one question item, on its turn, with its questions as given; so does `thread/turns/list` with no further parameters. The person's next ordinary message starts a new turn that completes, and no request is raised on that conversation by the new server. `thread/read` with `includeTurns` then lists the asking turn and the reply turn in that order; the reply turn's first item is a `userMessage` holding the person's words, and the question item is still the only one with questions. Not shown: anything tying the reply to the question beyond that order. | None of its own: the row above's control (the same call on a model the catalogue does not list is unsupported) applies to the call. | `QuestionThatDoesNotWait.test_a_plain_resume_gives_the_question_and_the_persons_reply_is_an_ordinary_message_after_it` |
| **A turn summary leaves items out.** After a restart and a resume with `excludeTurns`, `thread/turns/list` asked newest first with `itemsView` `summary`, as the App's history reads ask, answers each turn marked `summary`. The summary of the turn that asked holds one message from the person and one agent message, where the turn has three items; the others are left out. Which agent message a summary keeps is not asserted: the source says the first message from the person and the final agent message, and here it kept the question and left out the agent's closing message. So a summary cannot say whether a question waits or a message from the person follows it. | `thread/read` with its turns holds all three items of that turn, in order. | `QuestionThatDoesNotWait.test_a_turn_summary_leaves_items_out_so_it_cannot_say_whether_a_question_waits` |

### One app server, a folder per conversation

What the pinned Codex does with a conversation given its own folder, B, by an
app server started in another, A. Unless its row says otherwise, each start
and resume carries the fields the App sends at the edits level: the folder,
the level's approval, reviewer, mode name and workspace options, and one trust
entry for the folder's root, `untrusted`, as the App sends it for a folder the
person's settings do not mark; each turn sends the edits level and no folder.
The fixture supplies the rest as the other rows do (an invented model, the
built-in provider, no guidance and no App tool), and gives the trust entry
directly where the App first reads the settings to choose it. Where a test
fails, its message names the folder observed.

| Fact | Control | Test |
| --- | --- | --- |
| **Reported and listed.** The start reply's `cwd` and its thread's `cwd` are B. In `thread/list` (`sortDirection` `desc`, as the App sends it), the conversation's row reports B. With the `cwd` filter set to B, the list holds that conversation and not one started in A; set to A, the reverse. | A conversation started in A on the same server, reported and listed under A. | `FolderPerConversation.test_a_thread_started_in_b_reports_b_and_is_listed_under_b_alone` |
| **Where a command runs.** `/bin/pwd -P` prints B. A write to a relative name succeeds and its file lands in B, not in A. A conversation in A is open on the same server and the two take turns (B, A, B, A, B): each runs and writes in its own folder every time. The relative write checks the folder it is in within the same shell call and writes only in A or in B. | The conversation in A, run between B's turns, prints A and lands in A. | `FolderPerConversation.test_a_command_in_a_thread_started_in_b_runs_in_b` |
| **The sandbox's project.** At edits, the write in B succeeds; the write in A, the server's own folder, runs and is refused by the sandbox, as is the write outside. | On the same thread at full access, the write in A succeeds. | `FolderPerConversation.test_at_the_edits_level_the_sandbox_takes_b_as_the_project_and_refuses_a` |
| **The project's instructions.** With a `trusted` entry for B, the start reply's `instructionSources` names B's `AGENTS.md` and not A's, and the requests the stub receives for that conversation's turn carry B's marker line and not A's. With the `untrusted` entry, no instruction file is named and no marker is carried. The markers are looked for in the requests carrying that turn's key. B's untrusted start comes before its trusted one and A's after. | A conversation started in A: with a `trusted` entry it names A's file and carries A's marker alone; with the `untrusted` entry, none. | `FolderPerConversation.test_a_thread_started_in_b_loads_bs_instructions_and_not_as` |
| **The project's own settings.** The setting is `sandbox_workspace_write.writable_roots` in a project's `.codex/config.toml`, chosen because the rows above show it in the start reply's `sandbox.writableRoots` and in effect, and show that a turn's `writableRoots: []` does not remove it. A's names `outside/root-a`, B's `outside/root-b`, and the home's own settings mark A trusted. The start departs from what the App sends in one field: it sends no `config.sandbox_workspace_write` (the next row sends it). With B's entry `trusted`, the reply lists root-b and not root-a, the write in root-b succeeds and the write in root-a is refused by the sandbox. With B's entry `untrusted`, neither of the two is listed and both writes are refused. | A conversation started in A with its entry `trusted` lists root-a; the write in B succeeds in each case. | `FolderPerConversation.test_a_thread_started_in_b_loads_bs_own_settings_and_only_when_b_is_trusted` |
| **The App's own start against a trusted project's writable root.** The App's start at edits, whole, with its `config.sandbox_workspace_write` (`writable_roots = []`) beside a `trusted` entry for B, whose own settings name root-b. The reply lists neither of the two roots and the write in root-b is refused by the sandbox; the write in B succeeds. | The row above: the same trusted start without that one field lists root-b, and the write there succeeds. | `FolderPerConversation.test_with_the_apps_own_start_a_trusted_projects_writable_root_is_not_added` |
| **The trust mark written.** As the trust-mark rows: at full access, in the App's layout with the home's new, empty settings, with A and B both git projects. A start in B with no trust entry writes `[projects."<B>"] trust_level = "trusted"` into the home's `config.toml`, and nothing for A. With one entry for B, `untrusted`, as the App sends it, nothing is written. As in the trust-mark rows, the file is read once, two seconds after the start. | Each start is the other's control. | `FolderPerConversation.test_a_start_in_b_marks_b_in_the_settings_unless_an_entry_for_b_is_sent` |
| **Continued in B after a restart.** A conversation started in B and saved; the server stopped; a second server started, again in A; the conversation resumed as the App's Continue resumes it: the thread, `excludeTurns`, B as its folder, the level and the one entry. The reply is for that thread and its `cwd` and its thread's `cwd` are B; `/bin/pwd -P` prints B; the relative write lands in B; the write in B succeeds; the write in A runs and is refused by the sandbox. The folder sent is the folder saved, as it always is from the App: the row shows the conversation continuing in B, not which of the two Codex took it from. | The write in B, against the write in A. | `FolderPerConversation.test_resumed_with_b_in_a_new_server_started_in_a_the_thread_is_governed_by_b` |

One further observation about the supplier is held out of this folder pending
the owner's decision.

## What the temporary folder row does not show

- Operations not tried. These are untried mechanisms, not known bypasses:
  - a hard link, an exchange of two entries, or a change of owner, mode, access list, extended attribute, times or file flags;
  - a mount;
  - recursive deletion;
  - the at-variants of unlink and rename;
  - a rename onto an existing destination;
  - replacement by an object that is not a link;
  - relative paths, directory descriptors or other aliases;
  - case-only renames;
  - races.
- Steps not reached: with nothing sent, `mkdir` and the replacement link are never reached, because each compound command's first step is refused. The Working Files folder's own replacement by a link was not tried.
- Comparison: made at sampled points, not by a trace. A change undone between two samples would not be seen.
- Ancestors and siblings: the run's root, which is the Working Files folder's parent, and the data folder, its sibling, were compared but not operated on. The App's real folders sit under the person's Library, with other names and depth.
- Other levels: no protection is claimed for any level other than nothing sent. Full access appears only as the control. The local read-only policy grants no ordinary writable directory roots, including these folders, so nothing in this row is particular to them.
- Actors outside the sandbox: an approved escalation, a command allowed by a lasting rule, full access, Codex's own server process, the App, or another program. Each of these can change the entries to the extent of its own filesystem rights.
- The App's own checks when it makes these folders.
- The label. "Refused by the sandbox" rests on four things: the non-zero exit, the exact refusal line, the paired full-access control, and the source of the read-only policy. It does not rest on an independent observation of the sandbox backend.

## Read from the source, not shown by a fixture

`CODEX_EXEC_SERVER_URL`, `CODEX_HOME/environments.toml` and the
`CODEX_EXEC_SERVER_NOISE_*` variables. What these do was read from the public
source at `rust-v0.167.0`; no fixture set any of them. Set to a URL, or
configured by the file, they move commands and file edits to another exec
server, where this Mac's sandbox does not apply, while the replies report the
same policy.
