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

**The project's files in the trusted-project rows are not checked at run
time.** What they contain rests on the fixture's builders, as reviewed, and
on the stub-only tests that check the builders' output:
- At run time, the write helpers allow only the names in `TRUST_FILES` (or,
  for a control, `HOME_FILES`). Nothing checks what a test passes them to
  write.
- The builders name only marker commands (`Run.marker_command`, one per
  `PROJECT_MARKERS` entry) and only the run's second loopback stub as an
  address. The stub-only tests check each builder's output for those
  commands and that address by comparing values and counting occurrences.
  They do not reject every other command or address a file could hold.

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
  a second project folder, or a project's own files with their marker commands
  and a second loopback stub), the App side of the JSON-RPC exchange, and
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

The run's cleanup also covers the failure paths:
- **The app server.** If setting up a started app server fails before it is
  handed back (`Client.__init__`), its process group is ended and its pipes
  are closed before the error is raised.
- **The second stub.** It is registered with the run before it starts
  serving, so the run's cleanup closes it even if serving never starts.
- **Open connections.** Closing a stub ends every connection a handler still
  holds.

The stub-only tests show each of these.

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

### A trusted project's own files

What a `trusted` entry for a project turns on at the pinned Codex beyond the
rows above (its `AGENTS.md` and its writable root), what the project's own
files can do that the App's level does not override, what the App's own start
can keep off while the entry stays `trusted`, and what an `untrusted` entry
with the App handing over the instructions gives instead. The project is A, the
folder the app server is started in. Unless its row says otherwise, each start
carries what the App sends at the edits level for a conversation in A (the
folder, the level's approval, reviewer, mode name and workspace options) and
the one trust entry for A's root, `untrusted` or `trusted`; each turn sends the
level. The App never sends `bypass_hook_trust` or `hooks.state`, and no row
sends them. The project's files are written by the fixture
(`Run(trusted_project=True)`, `write_trust_file`, one of `TRUST_FILES`), and
every program they name is the fixture's marker command: `/usr/bin/printf`
appending one line to its own file under `outside`, run through `/bin/sh -c`
where a setting takes a program and its arguments. A destination they name is
a second loopback stub made and closed by the run (`Run.other`). The stub
counts every connection it accepts: a count is an accepted socket, not a
completed exchange.

**What a row says.** Each row says only what its test asserts. What a test
records and prints without asserting is given apart, after "Recorded". Each row
names its own controls in the Control column. Most rows compare the two
entries; some add a positive control in the person's own settings (the Codex
home). The three rows under "kept off while trusted" and the resume row compare
cases within one trust state. Every test records all its observations before
it asserts anything. It prints them to standard error under `OBSERVED`
whatever its outcome, and a failure states them all.

**What rests on the source.** Some statements here rest on reading the public
source at `rust-v0.169.0` and on no test. Each is marked *(read from the
source)* where it is made. The files read were:
- `.codex/hooks.json` and the hook trust check
  (`codex-rs/hooks/src/engine/discovery.rs`, `config_rules.rs`);
- the project layer, its trust gate and its denylist
  (`codex-rs/config/src/loader/mod.rs`, `PROJECT_LOCAL_CONFIG_DENYLIST`);
- the session layer (`codex-rs/app-server/src/config_manager.rs`) and the
  merging of layers (`codex-rs/config/src/merge.rs`);
- MCP servers (`codex-rs/config/src/mcp_types.rs`,
  `codex-rs/rmcp-client/src/http_headers.rs`) and providers
  (`codex-rs/model-provider-info/src/lib.rs`);
- exec-policy rules (`codex-rs/core/src/exec_policy.rs`,
  `codex-rs/core/src/tools/sandboxing.rs`);
- the shell environment (`codex-rs/protocol/src/shell_environment.rs`) and the
  instruction fields (`codex-rs/core/src/config/mod.rs`).

| Fact | Control | Test |
| --- | --- | --- |
| **The project layer.** The project's `.codex/config.toml` names developer instructions (a marker line), approval, sandbox, network, reviewer, another provider and model, the built-in provider's address and a notify program. Each case is a fresh run. The home's settings either hold Codex's own trust mark for A ("marked") or are absent ("not marked"), and their state is asserted before the start. `config/read` for A with layers, as the App reads it, before any start. Marked: one project layer, enabled, with the keys approval, reviewer, developer instructions, model, sandbox mode and workspace options. The marker is the effective developer instructions; the project's approval (`never`), sandbox (full access), reviewer (automatic) and model are the effective values; the provider is still the built-in one. None of the four keys this file supplies that the source's denylist names *(read from the source)* is present: `model_provider`, `model_providers`, `notify` and `openai_base_url`. Not marked: the same keys in one layer, disabled with a reason, and the marker not effective. Then one start. Marked: the turn carries the marker with no entry and with a `trusted` entry, not with an `untrusted` entry, and the settings stay the mark. Not marked: with **no entry** the marker is carried and Codex writes `[projects."<A>"] trust_level = "trusted"` into the settings; with a `trusted` entry the marker is carried and the settings stay absent; with an `untrusted` entry, neither. Recorded: the wording of the reason. | Marked against not marked; each entry against the others. | `TrustedProject.test_a_project_layer_loads_with_a_trusted_mark_or_entry_and_with_no_entry_but_not_with_an_untrusted_entry` |
| **Hooks.** A command hook in the project's `.codex/hooks.json` for each of five events: session start, user prompt submitted, before and after a tool call, and stop. One turn whose command (the project write) succeeds; then the server is stopped and its output drained. With either entry, for each event, its marker has not run and no `hook/started` names it. With the `trusted` entry, `hooks/list` for the thread lists the five: from the source `project`, enabled, with the trust status `untrusted`. | The person's own approval of each hook as Codex listed it (key and current hash, in `hooks.state` in the Codex home), with the `trusted` entry: for each of the five events, its marker runs and a `hook/started` names it, and the command succeeds. | `TrustedProject.test_a_projects_own_hooks_do_not_run_and_are_listed_untrusted` |
| **A project approving its own hooks.** The same hooks. With the `trusted` entry, `hooks/list` gives a key and current hash for each of the five events, and the test requires all five. The project's own `.codex/config.toml` then approves each, in the form the person's approval takes (`hooks.state.<key>.trusted_hash`). On a fresh server with the `trusted` entry, each is still listed `untrusted`; for each event its marker does not run and no `hook/started` names it; the command succeeds. | In the same test: the project's file emptied and the same approvals written into the person's settings. For each of the five events, its marker runs and a `hook/started` names it. | `TrustedProject.test_a_projects_own_hook_state_does_not_approve_its_hooks` |
| **MCP servers** (a finding). Two servers in the project's `.codex/config.toml`. One's command is the marker command, writing its marker under `outside`, outside the project; the other is at the second stub's loopback address. Each case on a fresh server at edits. With the `trusted` entry: nothing has run and no connection was accepted before the thread starts. By thread start, the marker has run and the second stub has accepted a connection; by the end of the first turn both counts have risen. The startup notifications, as an unordered set, are `starting` and `failed` for each of the two (the fixture's programs are not MCP servers). None of their tools is offered; `mcpServerStatus/list` for the thread lists neither. On the same thread, a command's plain write under `outside` is refused by the sandbox, where the server's marker landed. With the `untrusted` entry: no marker run and no connection at any sample, through the listing and the stop; no notification; nothing listed; the same refusal. Recorded: the counts. | The same two servers in the person's settings, with the `untrusted` entry: nothing before the thread starts, both started at thread start and risen by the turn, the same notifications, and the listing names both. | `TrustedProject.test_a_trusted_projects_own_mcp_servers_are_started_and_an_untrusted_ones_are_not` |
| **A notify program.** `notify` in the project's `.codex/config.toml` names the marker command. With either entry, a turn completes, and the marker has not run when read 3 s later with the server stopped and drained. | The same `notify` in the person's settings, with the `untrusted` entry: the marker runs. | `TrustedProject.test_a_projects_own_notify_program_does_not_run` |
| **Approval, sandbox, network and reviewer.** The project's `.codex/config.toml` names approval `never`, full access, `sandbox_workspace_write.network_access = true` and the automatic reviewer. At the App's edits level, with either entry: the reply reports `on-request`, reviewer `user`, workspace write and network off. A write outside the project and the network probe each run and are refused by the sandbox; an escalation raises a request for that call, declined. At the supervised level, with either entry: the reply reports `untrusted`, reviewer `user` and read-only, and the project write is put to the client first and declined. | Each entry against the other; on each thread, the refused and the asked operations. | `TrustedProject.test_a_projects_approval_sandbox_network_and_reviewer_do_not_move_the_apps_level` |
| **A permissions profile.** The project's `.codex/config.toml` selects `default_permissions = ":danger-full-access"`. At edits, with either entry: the reply reports workspace write with network off and no active permissions profile. A write outside the project and the network probe each run and are refused by the sandbox. No case selects a profile, so the row shows the App's frame kept, not what the setting does where it applies. | Each entry against the other. | `TrustedProject.test_a_projects_default_permissions_do_not_move_the_apps_level` |
| **The model's destination.** The project's `.codex/config.toml` names another provider, defined there at the second stub's address, another model, and `openai_base_url` at that address. The App's start sends the model and provider on the frame; the process is started with `model_provider="openai"` and its own `openai_base_url`. With either entry, each on a fresh server: the reply reports the App's model and the built-in provider. The turn's requests reach the stub, and each names the App's model. The second stub has accepted no connection when read after the server is stopped and drained. | Each entry against the other; the stub's requests for the turn. | `TrustedProject.test_a_projects_provider_and_model_do_not_move_the_turn` |
| **A settings file Codex cannot load.** Two causes, each the project's whole `.codex/config.toml`, each on a fresh server. First, a key Codex no longer supports, `experimental_thread_store_endpoint`, named at the second stub's address. The `trusted` entry's start is refused, "failed to load configuration: `experimental_thread_store_endpoint` is no longer supported; remove it from config.toml", and the second stub accepts no connection. Second, a file that is not TOML. The `trusted` entry's start is refused with a message holding "failed to load configuration: Error parsing project config file ", the project's `.codex/config.toml`, "TOML parse error at line 1, column 6" and "key with no value, expected `=`". With the `untrusted` entry, each start succeeds and a turn completes. *(Read from the source:* `experimental_thread_store` takes only a local or in-memory store, and no supported key found points saved conversations at an address.*)* | Each entry against the other. | `TrustedProject.test_a_trusted_projects_settings_file_codex_cannot_load_refuses_the_start` |
| **Instructions from settings.** The project's `.codex/config.toml` sets `developer_instructions` to a marker line. With the `trusted` entry and no `developerInstructions` from the App, the turn carries the project's marker. With the App's own `developerInstructions` (another marker line), it carries the App's and not the project's. With the `untrusted` entry, never the project's. The App's marker is carried whenever the App sends it. | Each entry against the other; each start with and without the App's own. | `TrustedProject.test_a_trusted_projects_developer_instructions_are_carried_and_the_apps_own_are_kept` |
| **The trust mark with a `trusted` entry.** As the trust-mark rows: at full access, in the App's layout with the home's new, empty settings, in a git project, each case on a fresh run. With one `trusted` entry for the project's root, the home's `config.toml` is still empty when read two seconds after the start. | With no entry, the trust mark is written. | `TrustedProject.test_a_trusted_entry_writes_nothing_into_the_settings` |
| **An exec-policy rule** (a finding). The project's `.codex/rules/invented.rules` allows `/usr/bin/touch`, by its path and by its name. Each entry runs on a fresh server, at edits and at supervised. Each thread runs a `touch` of a file outside the project and a plain write outside the project that the rule does not match. With the `trusted` entry: at edits, the `touch` succeeds with no request and its file appears, while the plain write is refused by the sandbox. At supervised, the `touch` succeeds with no request, while the plain write is put to the client first and declined. With the `untrusted` entry: at edits both are refused by the sandbox; at supervised both are put to the client first and declined. | The same rule in the person's own rules (`rules/default.rules` in the Codex home), with the `untrusted` entry, at edits: the `touch` succeeds, while a plain write outside the project is refused by the sandbox. | `TrustedProject.test_a_trusted_projects_allow_rule_takes_a_command_out_of_the_sandbox_and_past_the_person` |
| **A shell environment** (a finding). The project's `.codex/config.toml` sets, through `shell_environment_policy.set`, three variables. One is the fixture's own. `ZDOTDIR` names a folder whose `.zshenv` exports `LEVEL_INVENTED_STARTUP=ran` (a shell builtin, starting no program and writing nothing) and then runs its marker command, writing under `outside`. `BASH_ENV` names a file that does the same with a marker of its own. The start-up file is the one the commands' shell reads, observed and not assumed: the one whose marker ran with the `trusted` entry at full access (zsh reads `ZDOTDIR`'s, bash `BASH_ENV`'s). The test prints which, and fails if neither or both ran there. Observed with zsh on a development Mac; observed with bash on the hosted macOS runner, as recorded in the hosted run of 2026-11-19. At edits and at full access, each entry on a fresh server, with two commands on the thread, each printing the start-up file's variable and the project's. With the `trusted` entry, at both levels, each command sees the project's variable and the start-up file's: the start-up file runs inside each command. At edits it runs under that command's sandbox, with either shell: its marker's runs do not rise across either command, its write outside the project being refused there. At full access its write succeeds, and its marker's runs rise across each of the two commands. With the `untrusted` entry, at both levels, each command sees both variables unset and its marker never runs. In every case the other start-up file's marker never runs. Recorded: both markers' counts, and each command's other output lines (at edits, the start-up file's refused write). | The same policy in the person's settings, with the `untrusted` entry, at full access: each command sees both variables and the start-up file's marker's runs rise across each. | `TrustedProject.test_a_trusted_projects_shell_environment_reaches_commands_and_runs_its_start_up_file` |
| **Kept off while trusted: MCP servers by name.** The person's own settings name two servers. One has the same name as the project's stdio server and its own marker command; the other is the person's own. Every case has the `trusted` entry and the App's start at edits, on a fresh server. Every turn completes. When the project names no server, the person's two servers have run by the end of the turn, and the second stub accepts no connection through the stop. When the project names its two servers, with no override, by the end of the turn the project's definition of the shared name has run and the person's has not. The person's other server has run, and the second stub has accepted a connection. `mcpServerStatus/list` lists the person's other server and the shared name, not the project's HTTP server. When `mcp_servers.<name>.enabled = false` is sent in the start's `config` for each server the project names, neither the project's nor the person's definition of the shared name runs through the stop, and the second stub accepts no connection. No notification names either of the project's names; the person's other server has run by the end of the turn. In this configuration `mcpServerStatus/list` for the conversation fails with "failed to reload config: invalid transport", naming `mcp_servers.<the project's HTTP server>`. Recorded: every marker's runs just before the listing, as it returns, a second after it and after the stop. In one run, with the project naming both and no override, the person's own definition of the shared name ran once after the listing was asked for, and the person's other server once more; this is a record, not a rule. *(A possibility, read from the source and not observed: the listing reloads the settings without the project's layer, and starts what it finds.)* Untested: whether `config/read` gives the App the names of a trusted project's servers. | The three cases against each other, all `trusted`. | `TrustedProject.test_with_a_trusted_entry_enabled_false_on_the_start_keeps_each_named_project_mcp_server_off` |
| **Kept off while trusted: the shell environment.** The project's policy of the row above, with the `trusted` entry. Each case uses the App's start at full access, one command and a fresh server, with the override in the start's `config.shell_environment_policy`. The start-up file is the one the commands' shell reads, observed as in the row above: the one whose marker ran with no override. The test prints which, and fails if neither or both ran there. Observed with zsh on a development Mac; observed with bash on the hosted macOS runner, as recorded in the hosted run of 2026-11-19. Of the forms exercised, two keep it out. First, each key the project sets given an empty value: the project's start-up file does not run (its marker), and the command sees the variable empty, not unset. Second, `include_only` listing the names of the environment Codex is given: the variable is unset and the marker does not run. Three forms do not keep it out: `exclude` of each key, `inherit = "none"`, and the whole table sent again with an empty `set`. After each, the command still sees the project's variable and the marker still runs. In every case the other start-up file's marker never runs. Recorded: both markers' counts. | The case with no override: the variable and the start-up file's marker; all cases `trusted`. | `TrustedProject.test_with_a_trusted_entry_only_an_empty_value_or_include_only_on_the_start_keeps_a_projects_shell_environment_out` |
| **Kept off while trusted: an allow rule, by a profile that denies a read.** The project's rule of the rules row, with the `trusted` entry, on one server. In place of the mode name and workspace options, a permissions profile is sent in the start's `config` and named by `permissions` on the start and on each turn. The profile is `extends = ":workspace"`, with one invented folder under `outside` denied for reading. The reply reports `on-request`, reviewer `user`, workspace write and network off, and the profile as active. The allowed `touch` outside the project runs and is refused by the sandbox; a plain write outside is refused by the sandbox; the project write succeeds; an escalation raises a request for that call, which the client declines. With the same profile without the denied read, everything is the same except that the allowed `touch` outside the project succeeds with no request. Between those two profiles, the denied read is the difference. *(Read from the source: an allow rule's command runs without the sandbox unless the file-system policy denies some read, `sandbox_override_for_first_attempt` and `unsandboxed_execution_allowed`; such a denial comes only from a permissions profile.)* | The App's own start with the same entry: `touch` outside the project succeeds, with no request. The matched profile without the denied read. | `TrustedProject.test_with_a_trusted_entry_a_profile_denying_a_read_keeps_an_allow_rules_command_in_the_sandbox` |
| **Handing over the project's instructions.** The project's `AGENTS.md` and the App's own developer instructions each carry a marker line. A marker is placed by the text of the request's messages: the roles of the messages holding it, how many times, and how many more times it appears anywhere else in the request. With the `trusted` entry and the App's instructions, the start names the project's `AGENTS.md` by its full path and no other file. The turn carries both markers, each once and nowhere else: the App's in a developer message, the file's in a user message after it. With the `untrusted` entry, the file's text follows the App's instructions in `developerInstructions`. The start names no file, and the turn carries both markers, each once and nowhere else, in the same developer message. *(Read from the source: `developerInstructions` takes the place of the settings' `developer_instructions`; `baseInstructions` and the `instructions` setting replace Codex's base instructions; no start field carries the text Codex reads from `AGENTS.md`.)* | Each route against the other. | `TrustedProject.test_with_an_untrusted_entry_agents_md_text_handed_over_in_developer_instructions_reaches_the_model` |
| **A nested `AGENTS.md`.** A git project with its own `AGENTS.md` and `sub/AGENTS.md`, each with a marker line. The conversation's folder is `sub`, and the one entry is for the project's root. With the `trusted` entry, the start names both files by their full paths and no other, and the turn carries both markers. With the `untrusted` entry, neither file is named and neither marker is carried. | Each entry against the other. | `TrustedProject.test_a_nested_agents_md_is_named_and_carried_with_a_trusted_entry_and_neither_file_with_an_untrusted_one` |
| **Handed-over instructions after a resume.** Two conversations are started with the `untrusted` entry, the App's instructions (a marker line) followed by the file's text (another), and one turn each. The server is stopped and a second server started. Each conversation is resumed as the App's Continue resumes it: the first without `developerInstructions`, the second sending the text again; one turn each. Every turn completes. Every turn, before and after the resume, carries both markers, each once and nowhere else, in the same developer message. The text is carried after a resume without being sent again, and sending it again does not carry it twice. Recorded: the instruction files each resume reply names. | The first turns and the two resumes against each other, all `untrusted`. | `TrustedProject.test_handed_over_instructions_after_a_resume` |
| **What else a trusted project's settings start.** `mcp_servers.<name>.http_headers_helper` on an HTTP server at the second stub *(read from the source: Codex runs the helper as `sh -c <command>`)*. With the `trusted` entry: the helper has not run before the thread starts, and has run by thread start and by the end of the first turn. The startup notifications, as an unordered set, are `starting` and `failed` for the server; `mcpServerStatus/list` lists nothing of it. The second stub has accepted no connection at any sample, from before the thread starts through the stop. With the `untrusted` entry: the helper never runs, no notification names the server, nothing is listed, and no connection. Recorded: how many times the helper ran. | Each entry against the other. | `TrustedProject.test_what_else_a_trusted_projects_settings_start` |

**What the start can and cannot switch off** *(read from the source, not
tested)*.
- A project's exec-policy rules load from every enabled project layer
  (`policy_files` in `codex-rs/core/src/exec_policy.rs`). The only switch is
  `LoaderOverrides::ignore_user_and_project_exec_policy_rules`
  (`codex-rs/config/src/state.rs`), which the app server sets only in its test
  helpers (`codex-rs/app-server/src/main.rs`). It is no setting, feature or
  start field.
- Only the trust entry switches the project layer off for one thread.
  `LoaderOverrides::ignore_project_config` skips project layers but cannot be
  reached from a request. `project_root_markers` from the start only moves the
  root, and `.codex` in the conversation's own folder is still read
  (`discover_project_layers` in `codex-rs/config/src/loader/mod.rs`).
- The start's `config` becomes the session layer, above the project's
  (`load_with_validation` in `codex-rs/app-server/src/config_manager.rs`).
  Layers merge key by key, tables merging and lists replacing
  (`merge_toml_values` in `codex-rs/config/src/merge.rs`).
  - So for MCP servers there is no whole-table replacement and no feature
    switch. An allow-list exists only in managed requirements, which a request
    cannot set, so a server can be turned off only by its name.
  - So for the shell environment, a key the project's `set` names cannot be
    removed, only given another value. Codex builds a command's environment in
    this order (`populate_env` in
    `codex-rs/protocol/src/shell_environment.rs`): `inherit`, the default
    excludes, `exclude`, then `set`, then `include_only`. Patterns are `*` and
    `?` wildcards only.

**Keys a project's settings may still set that this section does not test.**
The reason given for each is a choice of scope, or a finding read from the
public source *(read from the source)*. The list is not a survey of every
setting. The keys:
- `mcp_oauth_callback_url` and `mcp_oauth_callback_port` (an OAuth sign-in);
- MCP `auth`, `oauth`, `bearer_token_env_var`, `env_http_headers`
  (credentials);
- `apps`, `plugins.*`, `marketplaces.*`, `orchestrator.*`, `cloud.*` (an
  account or a plugin install);
- `analytics` and `feedback` (sent only when signed in; the App's own
  `analytics.enabled=false` flag is the higher layer);
- `web_search`, `tools.web_search`, `tools.client_search_provider` (run by the
  provider);
- `memories`, `auto_review`, `realtime`, `audio` (a model's work);
- `agents.<role>.config_file` (read only for instructions, model and feature
  switch-offs, in `codex-rs/core/src/agent/role.rs`);
- `computer_use` and `browser_use` (access policies, no program);
- `permissions.<name>.network.proxy_url` (used only by a selected profile, and
  the App names a mode);
- `features.network_proxy` (experimental, off by default);
- `js_repl_node_path` (its feature is removed);
- `file_opener` (links, not run);
- `model_catalog_json`, `model_instructions_file`, `log_dir`, `sqlite_home`,
  `history` (files, not processes or connections);
- `oss_provider` (used only with the command line's own option).

The source's denylist for a project's settings also names `openai_base_url`,
`chatgpt_base_url`, `model_provider`, `model_providers`, `notify`, `profile`,
`profiles`, `otel`, `apps_mcp_product_sku`, `responses_api_metadata` and the
two realtime addresses. Of these, only the four the project-layer row supplies
are tested.

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
