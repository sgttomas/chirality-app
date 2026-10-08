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

## Repair confirmation

2026-10-07. Same reviewer, same rules. My only write is this appended section.
I made no commits and used no network, credentials, `~/.codex`, model calls or
UI.

### What was checked

- **Repair head:** `1dad2331e8a63bc78055e2f6af66d9b233f56195`.
- **Repair commits:** `af7a5725e0` (G-1), `9a3dd4029d` (G-2), `47968f999a`
  (G-3), `555c570241` (G-4), `47e7a6eb9b` (G-5) and `1dad2331e8` (G-7).
- **Repair range** `4dd5f5a402..1dad2331e8` (`numstat`):
  `CONTRACT_ISSUES.md` +31/-9, `lib.rs` +12/-3, `record_supply.rs` +20/-0,
  `runtime_session.rs` +481/-60, `workflow_workspace.rs` +10/-0, `App.tsx`
  +4/-1.
- **Copy:** a fresh `git archive 1dad2331e8` at `$TMPDIR/j3r/`. After my
  mutations and probes were reverted, `diff -r` shows `src-tauri/src`
  identical to the candidate.
- **SHA-256 at `1dad2331e8`:**

| File | SHA-256 |
|---|---|
| `runtime_session.rs` | `8bfb523adfe0afdf5db278e9e8a59a01a6a03aade49254421a08e64727f6d15d` |
| `record_supply.rs` | `26de513ea913a4205894a3c66237377cf403f79f8822ddc4831397753f58bfe2` |
| `workflow_workspace.rs` | `1ad027a1094e2e9dbca579033bc5b438dbdca4f28e2efb8029d10d38453064eb` |
| `lib.rs` | `118fa4c9ee06a88e63df9bdf4ce936a7d0ee0e69bd91152a6a040403579d04fb` |
| `App.tsx` | `ade3ba023352f8842c2a81ee9518fbb232909282791177f27ca3853a4c6e46eb` |
| `CONTRACT_ISSUES.md` | `c85723f9928f15509ef3ed22ffaf8fd9331f6bed6ec185e39e5d4ce988091289` |

### Full suite

I ran the brief's full command with cargo `--no-fail-fast`. The log's SHA-256
is `211f70dd5029c6711be5562a9dd95a2baeb6acc9aaae29ae22feef9b468f9c30`.

- `npm run build`: passed.
- `cargo test`: 44 result lines, **663 passed (659 top-level plus 4 nested), 0
  failed, 3 ignored**. This matches J3's report.
- `npm test`: 3/3 passed.
- All `credential_rpc` tests passed.

### Mutations rerun

Each mutation ran against the `workflow_root`, `publication`, `supply`, `j3_`,
`v10_`, `native_coverage` and `prepared_turn` filters, and the original bytes
were restored after each.

| ID | Mutation | Result |
|---|---|---|
| JM1 | Cold check disabled (`possibly_live_in`) | **Caught**: `j3_vc_e_17_…` and `v10_g3_…` |
| JM2 | Hot open run not refused | **Caught**: 4 tests |
| JM3 | No supersede | **Caught** |
| JM4 | Order by kind instead of observation time (`flush_records` takes the first candidate) | **Caught**: `v10_g4_late_records_follow_observation_order_across_kinds`. The V10 survivor is now caught |
| JM4b | Held R3 gets no W-2 limit (`hold` removed) | **Caught**: the same test |
| JM5 | Incomplete record read as open | **Caught**: 2 tests |
| JM6 | Advisory gates the start | **Caught** |
| G1M2 | Notice not re-scoped (`with_generation` → `clone`) | **Caught**: `v10_g1_pending_notice_survives_…` |
| G2M | Fallback keeps "ended to start" | **Caught**: `v10_g2_…falls_back_…` |
| G1M | Accept a source with **no** observed write attempt (drop the `actualWriteAttemptObserved` gate at `runtime_session.rs:5127`) | **Survives**: 90/90 (R-1) |

### Probes rerun, plus new ones

These were temporary and have been removed.

| Probe | What it does | Result |
|---|---|---|
| P1 | V10 G-1 sequence | The notice's record failed, Codex was relaunched, and the next turn sent it: `turn/start` frames went 1 → 2, the view reads "sent once …", and a third send returns `None`. **G-1 repaired.** |
| P2 | V10 G-2 sequence | `Err("revision not verified; the live run was not ended")`. A is `Open` with no `run_ended`. **G-2 repaired.** |
| P3 | `skip_end_notice` right after `end_run`, with no record failure | Accepted. It records `evidence_limit` "record write failed", with detail "its record could not be written …" (R-4). |
| P4 | A permanently unwritable earlier R3 (reserved-id conflict), then `end_run` and `retry_records` | `run_ended` is never written; it is held "behind an earlier unwritten record (W-2)" (R-3). |
| P5 | A is busy when B's start runs | `start_workflow_run` returns `Err("Another run operation is pending …")` before sending. A's end stays held in memory: no `run_ended`, no pending notice, and the next ordinary turn carries none. Retrying B's start succeeds, and A then gets "ended to start …" (R-2). |

### Per finding

**G-1 is repaired.**
- The notice is marked `Sent` only when the Host returned a source whose
  evidence shows `actualWriteAttemptObserved`. Otherwise it stays pending.
- **Re-scoping cannot redirect a notice.** `with_generation`
  (`workflow_workspace.rs:952`) keeps the composed text, record and
  conversation, rejects a generation from another home, and replaces only
  `scope.generation`.
  - `turn_params` takes `threadId` from the unchanged `scope.conversation`.
  - `send_end_notice` first checks `current_conversation(generation, scope.conversation)`.
  - `pending_notice_for` is keyed by (home of the caller's generation, thread),
    and the Host rechecks the prepared generation and home.

  So a notice cannot move to another home or conversation.
- **CI-20 (i)** now matches the code. A write that was attempted and then
  failed still counts as consumed, which is consistent with "observed a write
  attempt".
- **Residual:** see R-1.

**G-2 is repaired.**
- B is now prepared first. CH-1 is waived for exactly A, and the chain uses A's
  prospective end. A preparation failure leaves A untouched (P2 and the new
  test).
- A's end is held unwritten until B's outcome is known. If B opens, A's
  `run_ended` ("ended to start ‹B›") is written before B's `run_opened`.
- **The fallback is truthful.** If B does not open, A's never-written entry
  becomes "ended by the person". That is true: the person ended it, and WR's
  notice pattern admits no other cause. A gets a pending notice, and a B that
  was never sent is withdrawn.
- **The CI-20 (e) residual is truthful and complete for an unknown outcome.**
  B's chain line may have reached the model while A's record says "ended by the
  person", and the notice follows too.
- **One small omission in (e):** with a definite refusal, B's own published
  `selection_record` (`prior_run.ended`) and `run_text` chain line still say
  "ended to start ‹B›" while A's `run_ended` says otherwise. These are the
  records of a run that was never opened, so they make no false RS claim.
  Naming them in (e) would help readers.
- **Residual:** see R-2.

**G-3 is repaired.** `possibly_live_in` includes `Unknown` runs. The refusal
names the reason and the record limits, and offers the end route.
`end_recorded_run` accepts an `Unknown` run, but only once the record set is
complete (the writer refuses an incomplete set). The new test passes, and JM1
and JM5 are caught.

**G-4 is repaired.** `flush_records` writes lifecycle entries and both kinds of
R3 in observation order (ties go to the lifecycle entry), and stops at the
first failure. Everything behind that point is marked held, so each late item
gets its W-2 limit. Both defects J3 reported are pinned by tests (JM4 and JM4b
are caught). **Residual:** see R-3.

**G-5 is repaired.**
- Pending-notice state is read from per-run atomic flags. A busy run with no
  pending notice no longer blocks ordinary text (test).
- The flag is synced at every notice transition: `end_run`,
  `release_held_end`, `send_end_notice`, `skip_end_notice` and supersede.
  `AwaitingTurn` → `Prepared` changes no flag.
- When the record cannot be written, the person is told why and offered "Retry
  the end-notice record" (it publishes without sending) or "Send without the
  end notice".
- **The skip path never presents the notice as supplied:**
  - the state reads "not supplied …";
  - there is no `Sent` state, no R3 and no `supplyForm` end-notice entry (test
    and P3);
  - the next ordinary turn carries no notice.
- **Residual:** see R-4.

**G-7 is repaired.** `workflow_end_recorded` no longer accepts `completed`, and
`end_recorded_run(…, true)` is refused (FN-2). A null conversation gets a clear
error.

**G-6 and G-8** remain NOTEs, as allowed.

### Residual findings

#### R-1 MINOR: the "no write attempt" branch of G-1 is untested

- **Where:** `runtime_session.rs:5127`.
- **Evidence:** G1M survives. The `NOTICE_REFUSED_BEFORE_WRITE` test seam
  simulates only an `Err` from the Host. Nothing exercises the Host returning
  `Ok(source)` with `actualWriteAttemptObserved == false`, for example when the
  generation closes before the write.
- **Fix:** add a test, for example by closing the generation between begin and
  write as the Host's own tests do (`hosting.rs:2472`).

#### R-2 MINOR: A's held end stays in memory if B's start fails before its send

- **Where:** `start_workflow_run` (`runtime_session.rs:4319-4350`); the
  try-lock of other runs happens before `predecessor` is released.
- **Evidence (P5):**
  - while A is busy, B's start fails early, and nothing releases A's held end;
  - A shows *ended* in the process, but its `run_ended` is unwritten and no
    notice is pending, so the next ordinary turn carries none;
  - a retry of B's start completes the step correctly;
  - if the process ends first, the confirmed end is lost, and A reopens as
    *open; interrupted*.
- **Fix:** on any early `start_workflow_run` failure for a held successor,
  either release A's end as a plain end with a pending notice, or keep the
  successor clearly "ready to retry", and record the held state's in-memory
  limit in CI-20 (e).

#### R-3 MINOR: a permanently unwritable earlier record holds `run_ended` indefinitely

- **Where:** `flush_records` (`runtime_session.rs:4673`).
- **Evidence (P4):** an R3 whose reserved identity conflicts can never be
  written, so the person's later `run_ended` stays held. After a relaunch the
  run reads *open; interrupted* although the person ended it.
- W-2 orders pending entries but gives no escape for an entry that can never be
  written. The view does show "held behind an earlier unwritten record (W-2)".
- **Fix:** record this in CI-20, or define a terminal "not writable" state for
  such an entry (with its limit) so later records can proceed.

#### R-4 MINOR: "Send without the end notice" can record a write failure that did not happen

- **Where:**
  - `skip_end_notice` (`runtime_session.rs:5057`);
  - the panel, which shows the button whenever the notice is pending.
- **Evidence (P3):** right after "End run", before any send or publication
  attempt, skip is accepted. It writes `evidence_limit` "record write failed",
  with detail "its record could not be written and the person chose to send
  without it".
- **Consequence:** the durable record states a failure that did not occur. The
  fact that the notice was not supplied is still true.
- **Fix:** allow skip only after a recorded publication failure of this notice,
  and show the button only then. Or word the limit by its actual cause.

### Updated verdict (J3 scope)

**READY.**
- G-1 and G-2 are repaired with tests, and their probes now pass.
- G-3, G-4, G-5 and G-7 are repaired with tests.
- CI-20 (e) and (i) are corrected and truthful.
- The suite matches the reported count, and every V10 mutation is now caught.

R-1 to R-4 are MINOR. None sends wrongly or presents the notice as supplied.
They should be repaired or recorded in CI-20. R-4, a durable statement of a
failure that did not happen, is the one to fix first.

## Second repair confirmation

2026-10-07. Same reviewer, same rules. My only write is this appended section.
I made no commits and used no network, credentials, `~/.codex`, model calls or
UI.

### What was checked

- **Head:** `07ff35486051fa49eac4b584d31b142b2719f7a1`.
- **Commits after `1dad2331e8`:** `eb8984cbf0` (R-4), `02297948ad` (R-2),
  `b2ca7ff581` (R-1), and `07ff354860` (R-3 recorded as CI-20 (j), plus the
  CI-20 (e) addition).
- **`numstat`:** `CONTRACT_ISSUES.md` +38/-0, `runtime_session.rs` +172/-13,
  `App.tsx` +1/-1.
- **SHA-256:**
  - `runtime_session.rs`: `ca1df750e1816ae27200702b192d9ce329720c45f0b1687190304b1ab51d4990`
  - `CONTRACT_ISSUES.md`: `a7c831aae6c1a4a73f0429e46dffdd1ad9abf2896316160a033c05f5476c8490`
  - `App.tsx`: `816e85b3a5ce20d58d1c8a83df2cda301bfbb8c53cda3a56558a5c554ea9c023`
- **Copy:** a fresh `git archive` at `$TMPDIR/j3f/`. After all mutations and
  probes were reverted, `diff -r` shows `src-tauri/src` identical to the
  candidate.

### Suite, stability and mutations

**Full suite.** The log's SHA-256 is
`e67c16ba96b2da0fe997d8114b3e6258f9e113f76a332452e03e793fd761e98f`.
- `npm run build`: passed.
- `cargo test`: **669 passed (665 top-level plus 4 nested), 0 failed, 3
  ignored**. This matches J3's report.
- `npm test`: 3/3 passed.
- All `credential_rpc` tests passed.

**The R-1 test is stable.** `v10_r1_notice_accepted_but_never_written_stays_pending`
passed 8 times out of 8:
- 5 runs on its own (4.8 s each);
- 2 runs within the full parallel lib suite (351 passed each);
- 1 run in the full suite above.

**Mutations,** each against the `workflow_root`, `publication`, `supply`,
`j3_`, `v10_`, `native_coverage` and `prepared_turn` filters:

| ID | Mutation | Result |
|---|---|---|
| G1M | Accept a source with no observed write attempt | **Caught** by the R-1 test. It survived before. |
| JM1 | Cold check disabled | **Caught** |
| JM2 | Hot open run not refused | **Caught** |
| JM3 | No supersede | **Caught** |
| JM4 | Order by kind instead of observation time | **Caught** |
| JM5 | Incomplete record read as open | **Caught** |
| JM6 | Advisory gates the start | **Caught** |
| R4M | Skip allowed without a failure | **Caught** by 2 tests |
| R2M | The hold is read, not removed (`held_successors.get` instead of `remove`) | **Survives** (see "Claim races") |

R2M is the only survivor. It is harmless in practice, because
`release_held_end` is idempotent through `held_end`, and a second sender
reaches B's `attempted`/no-resend guard. The removal itself is not pinned by a
concurrency test.

### Probes

These were temporary, and the copy has been restored. P3–P7 ran three times
each with identical results.

| Probe | What it does | Result |
|---|---|---|
| P3 | Skip right after End | Refused: "The end-notice record has not failed to be written …". 0 evidence limits written. **R-4 repaired.** |
| P4 | A permanently unwritable earlier R3 | `run_ended` is still held, unchanged by design. **R-3** is now recorded accurately as CI-20 (j) with three options for the RS owner. Accepted as a recorded limit. |
| P5 | A busy when B starts | B's start now waits for A instead of failing. A's end is written ("ended to start …") and B opens. **R-2 repaired.** |
| P6 | Two concurrent starts of B, released by a barrier | One gets `Err("Original run operation pending")`, the other succeeds. 1 `turn/start` for B, 1 `run_ended` for A, 1 `run_opened` for B, and `held_successors` empty afterwards. |
| P7 | A ended separately while held | `end_run(A)` is refused ("Only an open run can be ended"). `end_recorded_run(A)` is refused ("held by this process"). `retry_records` writes nothing while held. Then B's start writes exactly one `run_ended` for A. |
| P8 | A third run C prepared and started in this conversation **between** `end_and_start` returning and B's start | C opens. Its chain line says A "ended to start …". B is then refused ("live in this conversation"). A's end falls back to "ended by the person" with a notice. The next ordinary turn sends "[Chirality] Workflow run ended: … No workflow is in force." **while C is live** (R-5). |

### Judgement

**R-1 is repaired.** The real Host no-write path is exercised without a test
seam: a stalled peer, a large frame holding the writer, and the Codex stop. The
test is stable.

**R-2 is repaired.** Every outcome of B's start releases A's held end, whether
the failure comes before the send, the start is refused, or the outcome is
unknown. A busy A no longer blocks B. The CI-20 (e) "in-memory window" text is
accurate.

**R-3 is recorded.** CI-20 (j) is accurate and no code was changed, which
fits a decision that belongs to the RS owner.

**R-4 is repaired.** Skip requires a recorded notice-record failure, and the
evidence limit carries that failure's text. The panel shows the button only
then. A later successful record write clears the failure.

**The CI-20 (e) addition** about B's own records after a definite refusal is
accurate.

**Claim races** for `held_successors`:
- **Two starts of B are safe.**
  - The claim is removed under the Root lock.
  - A non-claiming caller meets B's lock (`try_lock`) or `hold_open_for` ("already
    in progress") and sends nothing.
  - P6 shows exactly one send and one A end.
- **A ended separately while held is safe.** Both end routes refuse, and
  `flush_records` returns early while held (P7).

#### R-5 MINOR: a held successor does not reserve its conversation

- **Where:** `conversation_prior` and `start_workflow_run`
  (`runtime_session.rs:4324`).
- **Evidence (P8):**
  - Between `end_and_start` returning and B's start, A is *Ended*, and B is
    *Prepared* but holds A's end.
  - Neither counts as live, so another run C can be prepared and started.
  - B is then refused, and A falls back to a plain end with a notice.
  - The next ordinary turn tells the model "No workflow is in force" while C is
    live, and C's chain line names A's end as "ended to start ‹B›".
- **Reachability:** two separate commands have to interleave inside one
  `workflow_end_and_start` call (prepare and send of C between its two steps).
  The panel blocks this with its `busy` flag, so it is not reachable through
  the App's own UI in ordinary use.
- **Fix:** treat a run listed in `held_successors`, or carrying
  `hold_open_for`, as live for CH-1, in both `conversation_prior` and the start
  live-check. Or record the window in CI-20 (e).

G-6 and G-8 remain NOTEs.

### Final verdict (J1 + J3)

**READY.**
- **J1:** V9 F-1…F-5 were repaired and F-7 recorded. Confirmed at
  `152eeac3df`, and unchanged in substance at this head (the suite and all J1
  tests pass).
- **J3:** V10 G-1…G-5 and G-7, and R-1, R-2 and R-4, are repaired with tests.
  R-3 is recorded as CI-20 (j).
- **Suite:** it matches the reported count, and every mutation except R2M is
  caught. R2M is harmless.

**Remaining, none blocking:**
- R-5 MINOR. Not reachable through the panel; it should be repaired or
  recorded in CI-20 (e).
- G-6 NOTE.
- G-8 NOTE.

## R-5 confirmation

2026-10-07. Same reviewer, same rules. My only write is this appended section.
I made no commits and used no network, credentials, `~/.codex`, model calls or
UI.

### What was checked

- **Head:** `2e2a02844a0fb28552fde5622e17855756d197bf`, one commit on
  `07ff354860`.
- **`numstat`:** `runtime_session.rs` +95/-4, `CONTRACT_ISSUES.md` +4/-0.
- **SHA-256:**
  - `runtime_session.rs`: `4ee2e2af3ed6bd85a6f47762cc685d58522fc6daa6b70a3fcbc84b8e16a9e726`
  - `CONTRACT_ISSUES.md`: `e00d9a7cb5f414fb3cffc282aedfa6e58fa02e14e5bb54931ed811251ed52317`
- **Copy:** a fresh `git archive` at `$TMPDIR/j3g/`. After the probes and the
  mutation were reverted, `diff -r` shows `src-tauri/src` identical to the
  candidate.

### Repair

- **New checks:** `held_step_in`, which reads the Root `held_successors` map
  against the runs of the conversation, and a per-run `held_step`, from
  `hold_open_for` or `held_end`.
- **Where they apply:**
  - preparation (`conversation_prior`);
  - dispatch: the `reserved` check in `start_workflow_run`, applied on both the
    claimed and unclaimed paths, plus each other run's `held_step` inside the
    live check.
- **B's own claim is not blocked:** it is removed from `held_successors` before
  the reservation is computed, and A, its own predecessor, is excluded from
  the live check.
- **Release:** the reservation ends with B's outcome
  (`v10_r5_reservation_ends_with_the_successor_outcome`).
- **CI-20 (e)** gains the matching text.

### Suite

The log's SHA-256 is
`3ba4607416356c9408d52e26c895311ed5c433e9ca7b3571b0a0b2938456f211`.
- `npm run build`: passed.
- `npm test`: 3/3 passed.
- **Cargo (`--no-fail-fast`): 668 top-level tests, of which 667 passed and 1
  failed, plus the 4 nested runs.** One nested result line is interleaved with
  other output in the log; the per-binary totals reconcile (lib 354, which is
  351 + 3 new R-5 tests).

**The one failure is a pre-existing, load-sensitive integration test, not R-5.**
- The test is `tests/handshake.rs::hosts_codex_initialize_then_thread_start`.
  It panicked at `:147`: "remoteControl/status/changed delivered".
- It runs the real Codex 0.160.0 binary and expects a notification to arrive
  with the initialize response.
- `tests/handshake.rs` is unchanged since base `3d0db214cb` (`git diff` is
  empty), and R-5 touches only `runtime_session.rs` and `CONTRACT_ISSUES.md`.
- The same test passed in the `npm test` phase of the same run, and in 6 of 6
  immediate reruns of `cargo test --test handshake` (5/5 each).
- I record it as an intermittent timing failure of the real supplier, outside
  J1/J3. It should be watched in CI.

### Probes and mutation

These were temporary and have been removed. P6–P8 ran three times each with
identical results.

| Probe | What it does | Result |
|---|---|---|
| P8 | Prepare C between `end_and_start` and B's start | **Refused**: "\"End and start\" is in progress in this conversation (A ended to start B); … no other run may be prepared or started here (RE-7, CH-1). Nothing prepared." B then starts: exactly one live run (B), A's cause is "ended to start …", and no notice is pending. A later C is refused because B is live. **R-5 repaired.** |
| P6 | Two concurrent starts of B | One succeeds. The other is refused ("already in progress" or "Original run operation pending", depending on timing). 1 `turn/start` for B, 1 `run_ended` for A, 1 `run_opened` for B, no hold left. |
| P7 | A ended separately while held | Unchanged and safe. Both end routes are refused, retry writes nothing while held, and B's start writes exactly one `run_ended` for A. |

| ID | Mutation | Result |
|---|---|---|
| R2M | `held_successors.get` instead of `remove` | **Caught by 6 tests**, including `v10_r5_concurrent_successor_starts_claim_the_hold_once` and both other `v10_r5_*` tests. |

### Final verdict (J1 + J3 at `2e2a02844a`)

**READY.**
- **J1:** V9 F-1…F-5 are repaired and F-7 is recorded.
- **J3:** V10 G-1…G-5, G-7 and R-1, R-2, R-4, R-5 are repaired with tests, and
  R-3 is recorded as CI-20 (j).
- **Mutations:** every reviewer mutation is now caught.

**Remaining, none blocking:**
- G-6 NOTE: compatibility currency.
- G-8 NOTE: record-truth limits, logged in CI-20 (c) and (d).
- The pre-existing `handshake.rs` timing flake above. Required CI must pass on
  the merge candidate, so a recurrence there should be rerun or investigated
  separately.
