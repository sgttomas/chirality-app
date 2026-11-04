# Real-backend workflow fixture (stock Codex 0.160, included LS-5 workflow)

## Purpose and standing

The greeting fixture ([LOCAL_RESPONSES_BACKEND_SMOKE.md](LOCAL_RESPONSES_BACKEND_SMOKE.md))
proves transport only. This fixture joins J1's workflow lifecycle to the **real**
pinned stock Codex 0.160 app-server. It drives the production
`WorkflowRootSession` run pipeline end to end for the App's included workflow
(WR LS-5, [BUNDLED_RUN_ADMISSION.md](../../../PKG-02/DEL-02-02/Work/BUNDLED_RUN_ADMISSION.md)):
- select;
- prepare;
- recorded supply copy;
- send;
- one real native tool execution;
- observed finished offer;
- the person's end;
- history and record read-back;
- normal stop.

The model side is the deterministic loopback Responses fixture. Its two replies
are **scripted synthetic facts**:
- a fixed tool request;
- the finished line.

Neither is inference. The person's end is the test's call. Nothing here is model,
human, J1/J2, native GUI or release qualification. The owner-visible J1
observation on an identified candidate remains DEL-09-02's.

## Invocation (opt-in only; CI never runs it)

The test is `runtime_session::workflow_root_tests::real_backend_fixture_tests::parent_authorized_stock_native_bundled_workflow_fixture`
(`app/src-tauri/src/workflow_real_backend_fixture_tests.rs`). It is `#[ignore]`.
- **Location.** It is a unit test in the existing owning test module, because
  `WorkflowRootSession`, `start_workflow_run` and the installed-root binding are
  crate-private. No production item was widened and no external controller was
  added.
- **Gate.** `CHIRALITY_RUN_NATIVE_BACKEND_SMOKE=parent-authorized-0160-local-workflow-fixture`
  is distinct from both earlier gates. Without it, the test refuses before any
  path lookup or execution.
- **Input.** `CHIRALITY_NATIVE_SMOKE_BIN` is the absolute stock binary, pinned to
  SHA-256 `112fae7a…`. There is no auth, provider, model or credential input.
- **Scratch.** One `0700` root under `TMPDIR` holds:
  - the project;
  - a fresh `0700` Codex home;
  - an `mktemp -d` probe home;
  - the App data instruction seed;
  - an **explicitly bound test resources root**, `<root>/installed-resources/workflows`,
    with the exact pinned manifest and package bytes. It is bound through
    `configure_installed_bundle`, as `lib.rs` setup binds `resource_dir()/workflows`.

  The root is removed on every path.
- **Codex home.** It uses the App's local-provider literal, with the invented
  model `chirality-fixture-model` and provider `chirality-workflow-local`. It also
  makes the home's own policy choice: `approval_policy = "never"` and
  `sandbox_mode = "danger-full-access"`. The App sends neither field.

  Codex's own seatbelt cannot nest inside the parent's sandbox. Its
  `sandbox_apply` call fails with "Operation not permitted", which was checked
  directly. So the parent's profile is the boundary:
  - outbound and inbound network to `localhost` only;
  - no owner `~/.codex` reads or writes;
  - writes denied under `$HOME` except the owned scratch.

  The profile does **not** restrict writes outside `$HOME`; there they are
  limited only by ordinary file permissions. Codex's own tool sandbox and
  approval flow are therefore **not** exercised, and no production guard was
  changed.
- **Run.** Under that profile, with `env -i`, a 180 s alarm and `t3_slot`.
- **Retained profile.** It stays outside the repository at
  `chirality-t3/scratch/app-workflow-backend-fixture-TvyUbFBZ/network.sb`, SHA-256
  `70117bbb439d7256ad71a9616612a5e0645805f40d884c3479ff5329c41654c0`. The same
  folder keeps the run logs `run1.log`…`run7.log` and `greeting.log`. Its exact
  text, with the home folder written here as `$HOME` and the scratch root as
  `$SCRATCH`, is:

  ```
  (version 1)
  (allow default)
  (deny network*)
  (allow network-outbound (remote ip "localhost:*"))
  (allow network-inbound (local ip "localhost:*"))
  (deny file-read* (subpath "$HOME/.codex"))
  (deny file-write* (subpath "$HOME"))
  (allow file-write* (subpath "$SCRATCH"))
  (deny file-write* (subpath "$HOME/.codex"))
  ```

## Joined path and assertions

1. **Startup.** Real `Host` start reports `codex-cli 0.160.0`. Conversation
   start carries the seeded `HELP_HUMAN` composition, and `thread/start` reports
   the fixture model and provider. The conversation is held in a real
   `HomeSession`.
2. **Select.** `select_production_bundle` on the bound root. The choice is
   runnable, with origin `bundled` and revision `3730d84d…`.
3. **Prepare.** `prepare_run` with the person's text. The tool's output file does
   not exist yet.
4. **Send.** `start_workflow_run`, the `workflow_send_run` path. The lifecycle is
   `Open`.
5. **Observe.** `host_tick::tick_home`, the production record tick, runs until
   the native terminal, which is `completed`. The conversation has exactly one
   turn, so there was no duplicate send.
6. **Tool.** Real Codex executed the one fixed action. The invented file
   `fixture-output/real-codex-tool-result.txt` holds the exact scripted line, and
   history shows a completed `fileChange` item. The fixture saw the call's
   result returned under its `call_id`.
7. **Offer and end.**
   - **Offer.** `host_tick::workflow_status` offers the run's finished report,
     `Workflow finished: bundled:coordinated-knowledge-work`.
   - **End.** `end_requested` with the offered message, as `workflow_end_run`
     does, records cause `completed`.
   - **Run view.** It shows the statement, and `endedAfterTurn` is the
     observed turn.
8. **Records.**
   - **WR.** The project holds exactly `selection_record` and `run_text`. The
     selection's standing is `bundled`, its origin `bundled` and its revision the
     pinned revision. Its `holding_library` is the bound root.
   - **RS.** The run's entries begin `run_opened` and end with one `run_ended`,
     cause `completed`.
   - **No checkpoint arrival.** The included package declares no checkpoints, so
     the file change is no checkpoint arrival.
9. **Supplied files.** The single TX-7 (c) supply copy under
   `.chirality/workflow-supply/coordinated-knowledge-work/` is byte-identical to
   the package.
10. **History read-back.** Through `NativeHistory` and `Host::history_dispatch`:
    - one turn;
    - the user message's two text inputs: the run text with the pinned begin
      marker and the supply-copy line, but no App-bundle path, and then the
      person's exact text;
    - the `fileChange`;
    - the exact scripted report.
11. **Fixture traffic.** Exactly 2 Responses requests: the tool step and the
    report. All came from loopback, all used the fixture model with streaming,
    and all carried the run text and the person's text. There were no other
    requests.
12. **Stop.** Normal stop with 0 surviving descendants.

### Tool protocol finding (pin 0.160, unknown model)

The first attempt scripted an `apply_patch` custom tool call. Stock Codex offers
an unknown model only these tools:
- `exec_command`;
- `write_stdin`;
- `request_user_input`;
- `view_image`;
- the `multi_agent_v1` namespace;
- the goal tools;
- `web_search`.

It offers no `apply_patch` tool. It answered that call with a 43-byte
`custom_tool_call_output` and wrote nothing. The fixed action is therefore one
`exec_command` function call whose command is an `apply_patch` heredoc, with
`login: false`. Codex recognizes that form and applies the patch itself, and
reports a `fileChange` item. This is the scripted fixture's protocol choice, not
an observation of what a model would do.

## Shared fixture

The loopback Responses peer moved from `tests/native_backend_smoke.rs` into
`app/src-tauri/tests/support/responses_fixture.rs`. The smoke test includes it
with `#[path]`, and the workflow test with `include!`; there is no product use.
- **Scripting.** Each Responses request takes the next scripted list of output
  items, and the last list repeats.
- **Facts kept.** Facts stay names and booleans only:
  - labelled marker presence;
  - offered tool names;
  - returned tool-result call IDs and sizes.
- **Greeting behaviour unchanged.** The greeting fixture's script is its single
  canned message, so its behaviour is unchanged. Its prompt check now reads
  `markers.prompt`.

## Observed runs (2026-11-04)

- **Source.** Main `98722981` plus this branch; stock binary `112fae7a…`.
- **Workflow fixture.** Two consecutive passes, 2.75 s and 5.13 s, under the
  profile above. Published facts:
  - supplier `codex-cli 0.160.0`;
  - workflow `coordinated-knowledge-work` at `3730d84d…`, standing `bundled`;
  - 1 native turn, `completed`;
  - history items `userMessage`, `fileChange`, `agentMessage`;
  - RS `run_opened`, `model_turn`, `model_turn`, `run_ended` (`completed`);
  - WR `selection_record`, `run_text`;
  - 2 Responses requests;
  - 0 surviving descendants.
- **Gate refusal.** Without the gate, the test refused with "opt-in absent;
  nothing executed".
- **Regressions run.**
  - The greeting fixture, gated, passed in 3.58 s.
  - The smoke file's non-ignored tests passed (3).
  - The LS-5 tests `bundled_ls5*`, `bundled_run_admission*` and
    `bundled_publication*` passed (6).
- **Cleanup.** No Codex process remained and no fixture scratch was left. The
  existing `cfg(test)` records-store placement (`chirality-test-records-<pid>`)
  is created under the run's `TMPDIR`, which is inside the owned scratch.

## End notice and fresh-process join (follow-on, branch `app/real-backend-end-notice`)

The same gated test continues past the end, using the same scripted model side.
Step 2 is one scripted reply that repeats for each later ordinary message.
- **Run-text check.** Before the end, the home's own history owner selects the
  conversation, as the history panel does. `check_native_supply` compares the
  run text with the real native pages; the result is `verified`.
- **End notice.**
  - The end reports `endNotice: pending: the next ordinary turn in this
    conversation carries it`.
  - The first ordinary message goes through the production `ordinary_send_text`,
    the `conversation_send_text` path. It returns `end notice and the person's
    text sent once`.
  - After it, no notice is pending (`send_with_pending_notice` is `None`).
  - A second ordinary message carries the person's text only.
  - The run stays `Ended`, and no finished offer is shown for it.
  - `check_end_notice_supply` reports `verified`, with R3 `recorded`.
- **Records.** The counts are asserted exactly.
  - **RS.** The run's log is exactly `run_opened`, `model_turn`, `model_turn`,
    `supplied_guidance` (the run text's R3), `run_ended` (`completed`), and
    `supplied_guidance`. The last is the one entry after the end: the end
    notice's R3, form `workflow run end notice (turn text)`.
  - **WR.** It holds exactly 1 `selection_record`, 2 `run_text` (the run start
    and the end notice) and 2 `supply_check`. Each supply check is cited by
    exactly one R3.
- **History.** Three native turns, each holding a user message and the scripted
  reply:
  1. the run text and the person's text;
  2. the end notice first, then the follow-up. The notice starts
     `[Chirality] Workflow run ended:`, names the run and ends `No workflow is in
     force.`;
  3. the second follow-up only.

  The fixture saw exactly 4 Responses requests. The notice text first appeared
  in the **scripted fixture's** request 3, with the follow-up. Request 4 carries
  it again only as replayed conversation history, which is not a second supply.
  No model received it and no inference occurred.
- **Fresh process.** After a normal stop, a new `Host` starts over the same Codex
  home and project, giving a new generation, and a new `WorkflowRootSession`
  holds no run.
  - **Records read.** The existing records reader, `records::supply::read_project_runs`,
    reads the ended run with no read limits:
    - its conversation is the thread;
    - its lifecycle is `Ended {stopped_by: "the person", cause: "completed"}`;
    - its workflow is `bundled` / `coordinated-knowledge-work` / `3730d84d…`;
    - nothing is live, or possibly live, in the conversation.
  - **Repeat end.** `end_recorded_run` on the ended run is refused with "The
    record does not show this run open, or in an unknown state, in this
    conversation; nothing recorded".
  - **No new records.** The repeat end and `observe_ended_runs` add no RS or WR
    record.
  - **History.** The new generation's `NativeHistory` reads the same three turns
    with the same user texts.
  - **Stop.** Normal stop leaves 0 surviving descendants.

### Observed runs (2026-11-04)

- **Source.** `558ea694` (#116 head) plus this branch, with the same stock binary
  `112fae7a…`. This evidence is separate from #116's.
- **Results.** Two consecutive passes, 5.96 s and 6.45 s.
- **Profile.** The same profile text as above, with this scratch root. It is
  retained at
  `chirality-t3/scratch/app-workflow-end-notice-UhybcNYk/network.sb`, SHA-256
  `d73ed32eeacac4d99ba7c4af0cde84b6ada487628c10a28c1665879bcee5c1aa`, beside the
  logs `run1.log` and `run2.log`.
- **Cleanup.** No Codex process and no fixture scratch remained.

These are scripted synthetic facts. The notice and the follow-ups reached only
the scripted fixture. No model received or acted on them, and no inference
occurred. The fresh process is a new Host
and Root in the same test process, not an App relaunch.

## Limits

- The model replies, the finished line and the person's end are synthetic.
  Useful work, completion quality and model behaviour are not established.
- Codex's own tool sandbox and approval flow are not exercised: the test home
  uses `danger-full-access` and `approval_policy = "never"`. The outer profile
  restricts writes only under `$HOME` (see above).
- The test binds a test resources root, not a signed candidate's
  `Contents/Resources/workflows`.
- The frontend, GUI first screen, an ordinary launch and any real local model
  server are outside this fixture.
- No endpoint, model, credential, signing identity or owner state was used.
