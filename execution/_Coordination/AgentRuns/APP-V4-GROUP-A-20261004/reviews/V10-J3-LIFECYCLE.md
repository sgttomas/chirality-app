# V10: independent review of the J3 lifecycle candidate

2026-10-07. Chirality TASK (Type 2), independent code reviewer, dispatched by
HELP_HUMAN (Claude Opus 5.5, Claude Code) for run `APP-V4-GROUP-A-20261004`.
I did not delegate, and I did not write the code under review. My only write
is this file. I made no commits and used no network, credentials, `~/.codex`,
model calls or UI. Earlier I reviewed J1 (V9 and its repair confirmation), so I
know that code. I excluded `bd1b9fbc8a` there; it is in scope here.

## Candidate

- **Branch and commit:** `claude/app-v4-j1-publication`, commit
  `4dd5f5a402bc58102fc0ba854ded6cf56ebba3c3`.
- **J3 range:**
  - the WIP commit `bd1b9fbc8a`;
  - `152eeac3df..4dd5f5a402`: `e46431e547` (two J1 fixtures), `af92ead655`
    (end-and-start, cold end, tests), `e3f97fe40e` (seal), `adedde9c0a` (lib),
    `291fba465d` (panel) and `4dd5f5a402` (CI-20 (c)–(i)).
- **How I read it:** the worktree `.claude/worktrees/agent-a30b47a03f09fe083` is
  read-only for me. I used `git show`, `git diff` and `git archive` only.
- **Changed files** (`numstat`):
  - from `152eeac3df`: `CONTRACT_ISSUES.md` +63/-0, `lib.rs` +58/-2,
    `runtime_session.rs` +248/-10, `workflow_record_store.rs` +17/-3,
    `workflow_record_store_tests.rs` +14/-0, `App.tsx` +16/-3;
  - WIP over `75306094ed`: `record_supply.rs` +246/-0, `runtime_session.rs`
    +635/-34, `workflow_record_store.rs` +147/-16, `workflow_workspace.rs`
    +25/-0.
- **SHA-256 at the candidate:**

| File | SHA-256 |
|---|---|
| `CONTRACT_ISSUES.md` | `a916b1ec7006c1aeb77aa58fe05e054e1e885632a7e207c1223e05b62847ec82` |
| `lib.rs` | `cb75fe192fc52830dd9aa98a765390f2d4f2eac140d4eedc1057cce6598723e1` |
| `runtime_session.rs` | `113f11c2f5f9a0d323be23022ba99a9bd855ad66ea5bb4275db274882a42a11a` |
| `record_supply.rs` | `8e289ebb53c1cd60522ae57b06d734d37e3507e67f13fbe090710c36e984a743` |
| `workflow_record_store.rs` | `327f2f054e307aceaa5166a9b8d0edd236103b2c92d5dfe9152c9c6aafda4345` |
| `workflow_record_store_tests.rs` | `500c754029c331ac03aaac79562c849c9f013a9019024fca9d69fccced325234` |
| `workflow_workspace.rs` | `dbdc46b1ead7cd9fc35bff2f433e9fec05252b758c04980a95f54bed7d87f7aa` |
| `App.tsx` | `d9a617209cc59f6d6207afee32d3731eaea0e85ce768f2020ac7c93e163e3651` |

## Scope

In scope are J3 brief items 1–6 and the brief's look-hard list, judged against
these sources:
- EXEC `EXECUTION_COMPATIBILITY.md`: AE-7, A-2, A-3, A-11, RE-4, RE-6, RE-7,
  §2.7, CK-1…CK-3 and VC-E-17;
- WR §16.2 TX-5, §16.3 CH-1/CH-2, §16.4, §16.7 SQ-END and SQ-CHAIN;
- RS W-2, R1/R8 and VC-42;
- J2's `Request` seam doc in `compatibility_report.rs`;
- CI-20 (a)–(i).

J1 code is re-examined only where J3 changed it.

## Method actually performed

1. **Full suite.** I ran the brief's full command (cargo with
   `--no-fail-fast`) on a fresh `git archive 4dd5f5a402` copy at
   `$TMPDIR/j3-review/`. The log's SHA-256 is
   `3936f0e9c9fa5ef49564f998945af2a7eb7a2dab30150926db676ede71818f03`.
   - `npm run build` passed.
   - `cargo test`: 44 result lines, **652 passed (648 top-level plus 4 nested),
     0 failed, 3 ignored**. This matches the expected count.
   - `npm test`: 3/3 passed.
   - All 9 `credential_rpc` tests passed in this run.
2. **Reading.** I read the J3 diff and the code around it: `conversation_prior`,
   `start_workflow_run`, `send_with_pending_notice`, `send_end_notice`,
   `end_run`, `end_and_start`, `end_recorded_run`, `open_run`,
   `flush_entries`, `append_run_entry`, `read_project_runs`,
   `evaluate_compatibility`, `PreparedEndPublication::for_turn`, and the Host's
   `turn_start_prepared_run_text`. I also read the lib commands, the panel, and
   the source clauses listed above. `grep` shows that only `end_run` and
   `end_recorded_run` write `run_ended`, and only `end_run` sets
   `RunLifecycle::Ended`.
3. **Seal probe (compile only).** First I appended
   `impl PublishedText for ReviewerFakePublished` to `runtime_session.rs`. It
   failed with **E0277**, `ReviewerFakePublished: Sealed` not satisfied, and
   rustc names it a "sealed trait". I then added
   `impl …::sealed::Sealed for ReviewerFakePublished`. That failed with
   **E0603**, module `sealed` is private. The seal is real at compile time.
4. **Mutations.** I ran six of my own, each against the `workflow_root`,
   `publication`, `supply`, `j3_`, `native_coverage` and `prepared_turn`
   filters, restoring the original bytes after each:

| ID | Mutation | Result |
|---|---|---|
| JM1 | `conversation_prior` ignores cold interrupted runs (the `live_in` check disabled) | **Caught**: `j3_vc_e_17_…` |
| JM2 | A hot `Open` run no longer refuses a second start | **Caught**: 4 tests |
| JM3 | A successor start no longer supersedes the pending end notice | **Caught**: `j3_successor_after_plain_end_…` |
| JM4 | `flush_entries` continues past a failed lifecycle entry (`break` → `continue`; W-2 order) | **Survives**: 79/79 (G-4) |
| JM5 | `read_project_runs` reads an incomplete record set as `OpenInterrupted` | **Caught**: `j3_reopen_after_state_loss_…` |
| JM6 | A refused CK-2 publication gates the start (advisory turned into a gate) | **Caught**: 26 tests |

5. **Probes.** I added two temporary probe tests and removed them afterwards.
   `diff -r` against a fresh archive shows `src-tauri/src` identical to the
   candidate. The probes support G-1 and G-2, and their observed output is
   quoted there.

## Answers to the brief

1. **One live run per conversation.** `open_run` writes `run_opened` only after
   `turn_start_prepared_finish` succeeds (A-2). A refused or unknown start sets
   `StartNotConfirmed`, writes no `run_opened`, and does not block (A-3,
   CI-20 (e)). A second start is refused in two places: at prepare, against a
   hot open run or a cold interrupted run, and again at dispatch in
   `start_workflow_run`. JM1 and JM2 are caught. See G-3 for the incomplete
   record case.
2. **Explicit end only.** Nothing but `end_run`, `end_and_start` (through
   `end_run`) and `end_recorded_run` ends a run.
   - The tests show that an interrupt, a stop, process loss and the
     finished/proposal lines leave the run open.
   - Logout and window close have no code path into runs.
   - `completed` is recorded only through the person's `end_run(true)`.
3. **End notice, chaining and forks.**
   - On the success path, the notice is published before the send and supplied
     once (test, plus the `try_lock` refusal of concurrent sends).
   - A successor consumes it through its chain line (JM3 is caught).
   - B `follows` A and inherits no checks.
   - A fork is another (home, thread) and has no live run.
   - **However**, a pre-dispatch failure consumes the notice without sending it
     (G-1).
   - **And** "End and start" ends A even when B cannot be prepared (G-2).
4. **Reopen.**
   - `read_project_runs` derives `OpenInterrupted`, `Ended`,
     `StartNotConfirmed` or `Unknown` from the records alone. Conflicting
     entries are `Unknown`.
   - An incomplete record set never yields "open" or "ended" (JM5 is caught).
   - It infers no completion and creates no process run.
   - Interrupted runs blocking new starts is **supported by the source**: EXEC
     RE-7 says "An interrupted run (RE-4) is still live", and VC-E-17 (i)
     expects the run to stay live, or interrupted after relaunch.
   - The person can end the run explicitly (`end_recorded_run`, DEF-4).
   - RE-4's "continues as the same run" and its run-owner fallback are not
     implemented. CI-20 (c) and (d) record this.
5. **Compatibility.**
   - CK-1 is evaluated in `prepare_run`, and CK-2 in `send` just before
     `attempted`. Both use the run's own selection, holding library, home,
     generation and thread. The role comes from `binding(home, thread)`, and
     is `Unknown` when the binding is missing or busy. This meets the
     same-conversation obligation as CI-20 (g) describes it.
   - A refused publication writes no R14 (test).
   - The advisory never gates a start (JM6 is caught).
   - The view keeps J2's own `occasion` and `advisory` fields.
   - One display note is in G-6.
6. **CI-20 (c)–(i)** state their gaps accurately, except (i), which G-1
   contradicts.

**The look-hard items:**
- **The fresh-process test's assertion change preserves J1's intent and hides
  no defect.**
  - J1's assertion ("no `run_opened`") encoded J1's lack of a lifecycle. EXEC
    A-2 now requires `run_opened` when the start turn is observed. The fixture
    turn is `failed`, and AE-7 says a failed turn is not a run end.
  - The new assertions keep the protected properties: exactly one opening, no
    `run_ended` (no completion claim), the record read as `OpenInterrupted`,
    and no in-memory run recreated (`fresh.snapshot().runs` is empty).
  - "No live run" in that test means no process run object. In the record, the
    run is still live for CH-1, and `j3_vc_e_17_…` asserts the resulting
    refusal. That is consistent with RE-7.
- **Seal:** real (Method 3). The guard test `published_text_is_sealed_to_two_types`
  only matches the source text. The compiler is the actual enforcement.
- **W-2 run-entry queue:** correct as written. `flush_entries` stops at the
  first failure, and R3 waits for `run_opened` or `run_ended`. It is untested
  (G-4).
- **Ordinary sending through `conversation_send_text`:** with no pending notice
  and no busy run in the conversation, behaviour is unchanged. See G-1 and G-5.
- **Lib and panel collateral:**
  - five new commands are registered;
  - `workflow_send_run` now goes through `start_workflow_run`, which does not
    hold the Root lock during the native wait;
  - the panel offers End, End (finished), End and start, and End for a reopened
    interrupted run (completed=false only). It also checks the notice and shows
    the advisory.
  - Other notes are in G-7.

## Findings

### G-1 MAJOR: an end notice is marked "sent once" and consumed when nothing was dispatched

- **Where:**
  - `runtime_session.rs:4877-4935` (`send_end_notice`): line `:4915` maps a
    `turn_start_prepared_run_text` error to "native send not started", and line
    `:4924` sets `NoticeState::Sent` unconditionally;
  - `CONTRACT_ISSUES.md:464` (CI-20 (i)).
- **Evidence:** the probe ran these steps:
  1. open run A in `thread`, then `end_run(false, None)`;
  2. make the WR directory read-only (0o500) and call `send_with_pending_notice`.
     The result is `Err("End notice not durably recorded; nothing sent:
     Permission denied")`, and the notice stays `Prepared`, as intended;
  3. restore the permissions, stop Codex and relaunch it (a new generation,
     same App process);
  4. call `send_with_pending_notice` with the new generation.

  Results:
  - Step 4 returns `Err("End notice turn outcome unavailable; not resent:
    {…"limit":"prepared turn full generation/home differs from original run
    scope","state":"native send not started"}")`. The `Prepared` notice
    carries the old generation, so the Host rejects it before writing any
    frame.
  - The run view then shows `"state":"sent once with the next ordinary turn",
    "turn":null`.
  - A further `send_with_pending_notice` returns `None`, so the next ordinary
    turn goes without the notice.
  - The `turn/start` frame count stayed at 1 → 1 across the notice attempts.

  CI-20 (i) says the notice "counts as consumed when its turn is
  dispatched", but here it is consumed **without** dispatch. Any pre-write
  refusal by `turn_start_prepared_run_text` (parameter validation,
  `request_begin_scoped` refusal, scope mismatch) has the same effect.
- **Consequence:**
  - TX-5 and SQ-END are violated: the model is never told the run ended.
  - The UI and run view state a false fact ("sent once").
  - A published end-notice `run_text` exists in WR that was never supplied.
- **Fix:**
  - Mark the notice `Sent` only when a source request exists, that is, when a
    frame was written. Otherwise keep it pending.
  - Re-derive a `Prepared` notice's turn scope for the current generation
    before sending, keeping the original record identity and bytes, or
    re-prepare it when the record body does not depend on the generation.
  - Correct CI-20 (i) to match.

### G-2 MAJOR: "End ‹A› and start ‹B›" ends A before B can be prepared

- **Where:** `runtime_session.rs:4190-4213` (`end_and_start`). It calls
  `end_run(false, Some(&successor))` at `:4210`, then `prepare_run` at `:4212`.
  The lib `workflow_end_and_start` propagates the error with `?`.
- **Evidence:** the probe ran these steps:
  1. open run A;
  2. change the selected hot registered copy's `WORKFLOW.md`;
  3. call `end_and_start`.

  The call returns `Err("revision not verified")`, but A is already ended:
  - its lifecycle is `Ended`;
  - its notice reads "not composed: ended to start a successor; its chain line
    carries the end";
  - RS holds `run_ended` with cause "ended to start coordinated-knowledge-work";
  - the next ordinary turn carries **no** notice
    (`send_with_pending_notice(...).is_some() == false`).

  B was never prepared, so no chain line will ever be sent. The same happens on
  every other `prepare_run` failure after the end, for example an unopenable
  project, a failed `verify_store` or failed WR preparation.

  RE-7 makes the confirmation "A's explicit end … followed by B's run start".
  CI-20 (e) covers only "B's start is not confirmed", not a successor that was
  never prepared.
- **Consequence:**
  - A durable `run_ended` cause names a successor start that never happened.
  - The model is never told that A ended.
  - The person sees an error after A was irreversibly ended.

  All of this is avoidable, because the failure is known before anything is
  sent.
- **Fix:** check B's preconditions before ending A: admission, `verify_store`,
  that the project opens, and that composition is possible. One way is to
  prepare B with CH-1 waived only for this exact A, and end A only once B is
  prepared. Failing that, if preparation fails after the end, revert A's
  notice to a pending end notice and do not record the "ended to start" cause.
  Record the residual case under CI-20 (e).

### G-3 MINOR: an `Unknown` recorded run never blocks a new start

- **Where:** `runtime_session.rs:4130-4140` (`conversation_prior` uses
  `reading.live_in(thread)`) and `record_supply.rs:338`.
- **Evidence:**
  - When the project's record set is incomplete (any torn RS log), a run with
    `run_opened` but no readable `run_ended` is `Unknown`.
  - `live_in` returns only `OpenInterrupted`, so the gate lets a new start
    through. The test `j3_reopen_after_state_loss_…` asserts this ("unknown is
    not invented as live").
  - That is right for display, but as a CH-1 gate it admits a possible second
    live run (RE-7: "never two live runs in one conversation", VC-E-17).
  - The new run's own `run_opened` would then fail too, because
    `append_reserved` refuses an incomplete record set.
- **Fix:** refuse, or require explicit confirmation, when the conversation has
  an `Unknown` run, and name the record limit.

### G-4 MINOR: the W-2 lifecycle-entry queue is untested

- **Where:** `runtime_session.rs:4573-4584` (`flush_entries`) and
  `record_supply.rs` (`append_run_entry`).
- **Evidence:** JM4 survives. No test fails a `run_opened` write. Every
  RS-blocking test in the suite blocks the writer after the start.
- **Consequence:** these behaviours are unexercised:
  - a late `run_opened`;
  - `run_ended` waiting behind it;
  - the "record write failed" limit;
  - R3 held until `run_opened` is written.
- **Fix:** add a test that blocks `.chirality/records/runs` before `send`, then
  ends the run and retries. Assert the order `run_opened`, its limit,
  `run_ended`, then R3.

### G-5 MINOR: collateral on ordinary sending

- **Where:** `lib.rs:423-427`; `runtime_session.rs:4153-4175`
  (`pending_notice_for`) and `send_with_pending_notice`.
- **Evidence:**
  - `pending_notice_for` calls `try_lock` on every run in the conversation. So
    ordinary text in a conversation with any workflow run is refused ("A run
    operation is pending … nothing sent") while that run is busy, for example
    during a supply or notice check that waits up to 20 s for each history page.
  - When the end-notice publication fails, every ordinary send in that
    conversation fails until WR storage recovers. That is intended (SC-1 before
    send), but it has no escape and does not tell the person why ordinary chat
    is blocked.
  - The response shape differs from the ordinary `turn/start` result. The
    panel ignores the value, so this is benign today.
- **Fix:** check readiness without failing ordinary sends, for example by
  tracking pending notices in the Root index so no `try_lock` is needed. State
  the blocked-send cause in the conversation panel.

### G-6 NOTE: compatibility currency never changes

- **Where:** `runtime_session.rs:4657-4660`.
- **Evidence:** `current_basis` is built from the run's own prepared scope,
  which never changes. A relaunch or generation change therefore never marks
  CK-1 or CK-2 "not current", as J2's seam asks ("a changed basis marks it not
  current").
- **Fix:** pass the Host's current generation.

### G-7 NOTE: lib and panel details

- `workflow_end_recorded` accepts `completed: true` from the webview. A cold
  run has no finished report to justify *completed* (FN-2), although the panel
  sends only `false`.
- A reopened run with `conversation: null` would fail deserialization in that
  command. This is harmless, but the error message is opaque.
- `workflow_end_and_start` returns `Ok` with "successor not started" when B's
  start fails. That is correct. G-2 covers the earlier failure path.

### G-8 NOTE: record-truth limits (already logged)

- A `run_opened` that was still pending when the process died reads
  *start not confirmed in record*, although the start was observed. This is a
  WP-5 consequence of lost pending custody, and is truthful to the record.
- RE-4's "continues as the same run" (further checks or R3 on a cold
  interrupted run) and the run-owner fallback are not implemented. CI-20 (c)
  and (d) cover both.

## Verdict

**NOT READY.**

These parts conform:
- one live run per conversation (hot and cold) and the explicit-end-only rule;
- `run_opened`/`run_ended` ordering, with `follows` and the chain line;
- reopen truthfulness;
- the advisory CK-1/CK-2 wiring with no R14;
- the `PublishedText` seal, which is compile-enforced.

The suite matches the expected count, and four of my six mutations are caught.

Two MAJOR findings are reachable on ordinary person paths and leave false or
incomplete lifecycle evidence, and in both the model is never told the run
ended:
- **G-1:** the end notice is consumed and shown "sent once" without dispatch;
- **G-2:** A is ended as "ended to start B" when B cannot be prepared.

The candidate becomes READY when:
- G-1 and G-2 are repaired, each with a test;
- CI-20 (i), and CI-20 (e) where relevant, are corrected;
- G-3 to G-5 are repaired or listed as known limits.

G-6 to G-8 need no change before integration.
