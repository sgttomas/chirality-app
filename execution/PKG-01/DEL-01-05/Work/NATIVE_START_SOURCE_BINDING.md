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
- **New conversation.** It sends the latest host view's generation at the press.
  Its choice stays bound to the home-class epoch, as in #110. Whether to bind
  that choice to the generation as well is a frontend decision reserved to
  Agent 0. The native side refuses a start whose generation changed before
  dispatch either way.

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
- **Clean trial.** `trial_flows::start_bound_clean_trial` binds the source
  **before** the trial's begin step, so a mismatch is a `SendRefusal` with
  `prefillKept: true`: the pre-fill and the person's inputs stay, and nothing
  starts. The start then runs through `start_conversation` with the same
  generation, which rechecks it. If the source changes in the remaining window
  between binding and the start, the existing failed-start handling applies: the
  pre-fill is withdrawn and "Try again" is shown.
- **Unchanged.** The response shape, `startGeneration`, refusal messages as
  strings, retained receipts and uncertain-start handling.
  - **Refusal type.** The frontend offered to release Continue as's hold for a
    typed pre-dispatch refusal, e.g. `{message, started:false}`. That would
    change the interface and is not part of this clause. Without it, the
    frontend keeps holding such a refusal as it holds an unknown outcome.

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
- `a_clean_trial_with_a_changed_source_is_refused_before_its_begin_and_keeps_the_prefill`:
  - a replaced source is refused with the pre-fill kept, and with no start, send
    or RS record;
  - a class with no source is refused the same way;
  - the matching source starts the trial in the bound home and sends once.
- **Mutation check.** Removing the source check from `start_source` fails all
  three tests.
- **Affected regressions.** The `trial`, `continue_as`, `start`, `role_supply`,
  `home` and `router` filters ran 315 tests; 311 passed. All four failures are
  environment-only:
  - Three `historical_learning` tests fail only under parallel load and pass
    serially.
  - `run_start_files_line_names_a_usable_folder_or_refuses_the_start` fails only
    when `TMPDIR` is under `$HOME`, where the run text abbreviates `~/`. It passes
    with `TMPDIR` outside `$HOME`.
- **Not tested.** `lib.rs` commands are not unit-tested (no `AppState` harness).
  Their wiring is reviewed instead. No GUI, native launch, model or credential was
  used.

## Integration order

The frontend lane's PR #117 emits `generation` first. The current native code
ignores the extra key. This native enforcement integrates **after** #117. If it
landed first, a caller without `generation` would be refused by argument
deserialization before the command runs.
