# Native start source binding (New conversation, Continue as, clean trial)

## Why

Review of frontend PR #117 found a gap. Native `thread_start` and
`workflow_trial_start_clean` took a home class but no generation, and
`start_conversation_inner` recaptured the host's **current** generation. The
frontend binds each composer's choice to the full generation shown at press, but
the frontend alone cannot bind the *native* start to that source. After a Codex
restart in the same class, the press would have run under the replacement
generation.

This clause makes the native start take the displayed source and bind to it.
WR, ACCESS and ROLE commitments are unchanged; the change is limited to the
native source-binding path.

## Contract (agreed with the frontend lane, #117 head `9248a36e`)

- **Key.** `generation`, **required** on `thread_start` and
  `workflow_trial_start_clean`.
- **Value.** The full host-reported generation object
  `{appSession, home, spawnCounter}`, passed unmodified.
- **Clean trial and Continue as.** Both send the generation that
  `useBoundModelChoice` bound at press. For Continue as, that is the home the new
  conversation starts in, not the source conversation's home.
- **New conversation.** It sends the latest host view's full generation at the
  press. Its model choice stays bound to the home-class epoch, as in #110, and is
  **not** generation-bound. Agent 0 decided on 2026-11-04 to keep this for this
  increment, with no frontend clearing or reselection. The native side binds the
  start to the generation sent and refuses one that changed before dispatch.

## Native rule (source)

- **Binding before effects.** `HomeRouter::start_source(class, generation)`
  binds the start. `runtime_session::check_start_source` is its check, and binding
  happens before every effect or record. Binding requires:
  - a complete generation tuple (`recovery::generation_ref`), with nothing filled
    in;
  - the home of the named class;
  - that home running exactly that generation (home, App session and spawn
    counter), with host state `ready` and the generation not closed.

  A home/class mismatch, a same-class replacement, a stale or future tuple, or a
  closed source is refused. There is no fallback to the current generation or to
  another home.
- **Refusal effects.** In `start_conversation`, a source refusal returns before:
  - endpoint-edit invalidation;
  - role preparation;
  - the provider reading;
  - the start claim.

  It also publishes **no** role refusal observation, so nothing is recorded under
  another generation. A refusal for an unknown class or an absent home
  (for example, no key home configured) keeps its existing observation.
- **Carried through.** `start_conversation_inner` takes the bound home and
  generation and no longer recaptures. The bound generation is carried through:
  - the provider admission reading (`config/read` under that generation);
  - `ConversationSelection::start_params`;
  - role-child preparation;
  - dispatch: `thread_start_with_role_dispatch` sends under the admission's
    generation, and the Host refuses a changed or closed generation at request
    registration.
- **Change during preparation.** A source change during preparation is
  rechecked immediately before the start is claimed. It is then refused through
  the existing pre-dispatch path, whose role observation names the bound
  generation, never the replacement. If the source changes after the claim, the
  Host's own refusal and the existing uncertain-start handling apply unchanged.
- **Host attribution.** A request carrying an expected generation that is no
  longer the Host's current one is refused **before** the Host's not-ready
  branch. So a request bound to G1 records nothing, even when it arrives during
  a restart into a G2 that is still starting. Previously it appended a
  `client-request` not-ready refusal under G2 (review finding P2).

  A request of the current generation that is not ready keeps its existing
  not-ready record. A closed current generation keeps its existing order.
- **Clean trial.** `trial_flows::start_bound_clean_trial` binds the source
  **before** the trial's begin step, so a mismatch is refused and nothing starts
  or changes. The refusal reports `prefillKept: true` only when the trial is
  actually pending and not already being started, and that state is only read.
  An absent, withdrawn, consumed or in-flight reference reports
  `prefillKept: false` (review finding P3). The start then runs through `start_conversation` with the same
  generation, which rechecks it. If the source changes in the remaining window
  between binding and the start, the existing failed-start handling applies: the
  pre-fill is withdrawn and "Try again" is shown.
- **Unchanged.** The response shape, `startGeneration`, refusal messages as
  strings, retained receipts and uncertain-start handling.
  - **Refusal type.** Agent 0 decided on 2026-11-04 to keep string errors, with
    no typed pre-dispatch refusal. The frontend keeps Continue as's
    conservative hold: a refusal is held as an unknown outcome is, until the
    person's existing separate acknowledgement. The clean trial's pre-effect
    refusal keeps `prefillKept: true`.

## Checks

The tests are in the `runtime_session` workflow test module
(`src/start_source_binding_tests.rs`). They use the maintained local protocol
peer and a second, custody-sharing key home. No production item was widened for
them.
- `a_new_start_binds_only_the_exact_current_source_of_its_home_class`:
  - a matching source works for each class;
  - account↔key home/class mismatch is refused both ways;
  - each incomplete tuple is refused: null, a string, `{}`, a missing spawn
    counter, an extra key;
  - an altered `appSession`, `home` or spawn counter is refused;
  - with no key home there is no account fallback, and Probe is refused;
  - no `thread/start` is sent on either home.
- `a_replaced_or_closed_source_is_refused_and_never_recaptured`:
  - after a same-class restart the chosen generation is refused and the
    replacement works;
  - the pre-claim recheck refuses the original;
  - a Host dispatch carrying the original generation is refused with no
    `thread/start`;
  - after a stop, the last generation is refused.
- `a_source_replaced_after_binding_is_refused_before_dispatch_and_records_nothing_under_the_replacement`:
  - the source binds while current, then Codex is replaced;
  - the pre-claim recheck and a Host dispatch carrying the bound generation are
    both refused;
  - no `thread/start` is sent, and no `thread/start` client-request record is
    attributed to the replacement.
- `hosting::…::a_request_for_a_replaced_generation_records_nothing_while_the_replacement_starts`:
  - a G1-bound `thread/start` reaches a Host already on G2, in states
    `handshaking`, `starting`, `stopped` and `ready`;
  - both through the scoped request and through
    `thread_start_with_guidance_dispatch`, it is refused with no client-request
    record and no write;
  - a current-generation request that is not ready keeps exactly one not-ready
    record under its own generation.
- `a_clean_trial_with_a_changed_source_is_refused_before_its_begin_and_keeps_the_prefill`:
  - a replaced source is refused with the pre-fill kept, and with no start, send
    or RS record;
  - an absent reference, and a trial whose start is already in flight, report
    no pre-fill kept, and the in-flight start is left as it was;
  - a class with no source is refused the same way;
  - with the matching source, the bound home is handed to the start and the
    send, and one turn is sent. The start response is **scripted** in this
    test, so native start admission is covered by the Host tests above, not
    here.
- **Mutation checks.**
  - Removing the source check from `start_source` failed all three original
    tests.
  - Reverting the Host reorder fails the Host test.
  - Reporting `prefillKept: true` unconditionally fails the clean-trial test.
- **Affected regressions.** The `trial`, `continue_as`, `start`, `role_supply`,
  `home` and `router` filters ran 315 tests in one parallel run
  (`--test-threads=2`, `TMPDIR` inside the scratch under `$HOME`). 311 passed and
  4 failed:
  - three `historical_learning` tests;
  - `run_start_files_line_names_a_usable_folder_or_refuses_the_start`.

  Reruns of the same build:
  - **Serially**, all `historical_learning` tests passed.
  - **With `TMPDIR` outside `$HOME`**, the files-line test passed. It had failed
    on a `~/`-abbreviated folder in the run text.
  - **A focused rerun** after the final wiring change passed 22/22.

  These comparisons show no observed regression. They do not prove the cause of
  the initial failures.
- **Not tested.** `lib.rs` commands are not unit-tested (no `AppState` harness).
  Their wiring is reviewed instead. No GUI, native launch, model or credential was
  used.

- **Full lib suite after the review repairs.** One parallel run of the whole lib
  suite (`--test-threads=2`, `TMPDIR` outside `$HOME`, `t3_slot`): 2048 tests,
  2031 passed, 12 ignored, 5 failed. The five were:
  - `checkpoint_recorder::…compact_snapshot_keeps_exact_records_decline_content_order_and_public_file_view`;
  - `fleet_records::…fleet_reader_preserves_an_already_opened_store_identity_without_repairing_it`;
  - `records_retention::…records_retention_disposed_unlinked_project_never_falls_back_when_store_becomes_unavailable`;
  - `runtime_session::…after_end_file_lapse_concurrent_source_refresh_keeps_only_bounded_rows_and_reuses_them`;
  - `runtime_session::…recorder_write_failure_is_visible_and_written_late_with_its_limit`.

  Each passed when rerun alone on the same build. This shows no observed
  regression. It does not prove the cause of the parallel failures.

## Independent review (Astra MEDIUM, `c8a285b0`, static only)

| Finding | Repair |
|---|---|
| **P2.** A G1-bound request during a restart into a not-ready G2 recorded a not-ready refusal under G2. | The generation mismatch is checked before the not-ready branch (`hosting.rs`), and a Host regression test covers it. |
| **P3.** An early clean-trial refusal claimed `prefillKept: true` for absent, consumed or in-flight trials. | The flag is read from the trial's actual pending and in-flight state, and the absent and in-flight cases are tested. |
| **Evidence.** The matching-source test scripts the start response. | This account says so, and native admission is covered by the Host tests. |
| **Evidence.** No test replaced the source *between* binding and dispatch. | The new after-binding test and the non-ready replacement Host test cover it. |

No second review round was run.

## Reconciliation after #117

#117 merged as main `d968d643`. Its account in
[ACCOUNT_AND_PROVIDER_ACCESS.md](ACCOUNT_AND_PROVIDER_ACCESS.md) had said the
start commands take no generation, so the binding was the App's, in two places:
- the trial and Continue as paragraph;
- the "Generation at the native boundary (staged)" paragraph, which said that
  the native receiver ignores the key and that the binding is the App's only.

Both now record that as the state when #117 landed, followed by this clause's
native binding. The per-composer generation mapping is kept, and New
conversation's model choice stays described as home-bound, not
generation-bound.

## Integration order

The frontend lane's PR #117 emitted `generation` before native enforcement was
integrated. The native commands now require it; a caller without `generation`
is refused by argument deserialization before the command runs.
