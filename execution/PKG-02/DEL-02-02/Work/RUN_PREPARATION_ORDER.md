# Run preparation order (display metadata for `workflowRoot.runs[]`)

## Why

`WorkflowRootSession.runs` is a `HashMap`, so the `runs[]` rows in the Root
snapshot come in no defined order. A consumer that reversed that array, or took
its last row as the newest or current run, read map iteration order. Ordered test
mocks hid this (#125 source review).

The Root already keeps the authoritative order: the private
`conversations: HashMap<(home, conversation), Vec<run reference>>` (RE-7), which
`prepare_run` appends to once per preparation.

## Field

Each ordinary `workflowRoot.runs[]` row gains `preparationOrder`. Its value is
`null` or a non-negative integer:
- **Value.** It is the run reference's 0-based position in the Root's vector for
  that run's own key, which is `(generation["home"], thread id)`. `prepare_run`
  computes `home_key` from `generation["home"]` and stores the reference under
  `conversations.entry((home_key, thread))`.
- **Key.** The key is the **home ID and the bare thread ID**, not the serialized
  full generation. The existing key and storage are unchanged. A Codex restart
  in the same home, with the same thread ID, can therefore continue the same
  vector. Consumers that group runs or pick a current run require the full
  generation separately (#125).
- **Scope.** It is the relative preparation order **within one Root and one
  home ID + conversation**. It is not a time, and it is not comparable across
  conversations, homes or App processes; a relaunched Root starts empty. It
  confers no live, admission, selection or end capability. The row's existing
  generation, home and reference are unchanged.
- **When it is `null`.** `null` means the order is not established:
  - no vector holds the reference;
  - more than one vector holds it;
  - the reference occurs more than once in its vector;
  - the run's own readable scope `(home, conversation)` is not that vector's key.

  A run whose operation is pending, so its row cannot be read, still gets its
  position from the unique vector holding it.
- **No new state.** There is no new order state, clock, counter, persistence,
  schema migration, command or admission effect. Displaying an old preparation
  order needs no current Host readiness.

The frontend lane, consumer #125, confirmed the semantics. It sorts only within
one exact (generation, home, conversation) group. It treats the unique highest
order as the latest run. When any row in the group lacks an order, it says the
order is not known instead of picking a run.

## Checks

Tests are in `src/run_preparation_order_tests.rs`, in the `runtime_session`
workflow test module. They use the maintained local protocol peer, with no
production item widened.
- `preparation_order_follows_actual_preparation_per_conversation_and_is_null_when_not_established`:
  - three preparations in one conversation read 0, 1 and 2: two ended runs, then
    one prepared run;
  - another conversation's run reads 0, and rows are looked up by reference, so
    array order is irrelevant;
  - a busy run's row keeps its order;
  - an unassociated reference, and one held by two vectors, read `null` while the
    other rows keep their order;
  - reading the snapshot sends, records and changes nothing (wire, WR, RS and
    lifecycle).
- `preparation_order_is_per_home_and_a_run_scope_mismatch_reads_null`: the same
  thread ID under another home key does not match the run's own scope, so it
  reads `null`. It reads 0 again once restored.
- **Mutation check.** Removing the scope check fails the second test.
- **Focused regressions.** The `workflow_root_tests`, `workflow_journey`,
  `attachment_outcome`, `authoring_source`, `records_portable_reconstruction` and
  `records_scale` filters ran in one parallel run (`--test-threads=2`, `TMPDIR`
  outside `$HOME`): 331 passed, 2 ignored, 1 failed. The failure was
  `recorder_write_failure_is_visible_and_written_late_with_its_limit`, which
  passed twice when rerun alone. That shows no observed regression and does not
  prove the cause.

This is a read-only view addition, so no new admission review or full-suite
repeat was run.
