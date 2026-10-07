# V9: independent review of the J1 publication candidate

2026-10-07. Chirality TASK (Type 2), independent code reviewer, dispatched by
HELP_HUMAN (Claude Opus 5.5, Claude Code) for run `APP-V4-GROUP-A-20261004`.
No delegation. I did not write the code under review. My only write is this
file. I made no commits and used no network, credentials, `~/.codex`, model
calls or UI. I read `AGENTS.md`, `agents/AGENT_TASK.md` and
`projects/chirality-app-v4/loop/LOOP_INIT.md`.

## Candidate

- Branch `claude/app-v4-j1-publication`, commit
  `8a785ac4e382116a5c7db11c02e0a3606dfc12f3`. It is four commits on base
  `3d0db214cb`: `3b4612d204`, `93210138d7`, `9df51f87f4` and `8a785ac4e3`
  (`git log`).
- I used only `git log`, `git diff`, `git show` and `git archive 8a785ac4e3`
  on the worktree `.claude/worktrees/agent-a30b47a03f09fe083`. I wrote nothing
  there.
- While I was reviewing, that worktree changed. Someone else's merge commit,
  `75306094ed` ("Merge J2 compatibility … into J1 branch for J3", 13:23), now
  sits on the branch, and four `src-tauri/src` files have uncommitted edits.
  None of that is mine. This review covers only the exact bytes of
  `8a785ac4e3`. I confirmed with `diff -r` against a fresh archive that my
  copy's `src-tauri/src` equalled the candidate after my mutations were
  reverted.
- Files changed, from `git diff --numstat 3d0db214cb 8a785ac4e3` (all under
  `projects/chirality-app-v4/app/`), with SHA-256 at the candidate:

| File | +/- | SHA-256 |
|---|---|---|
| `CONTRACT_ISSUES.md` | +47/-0 | `980aa8d15660f2af9fc2ad7c6acb7ac1b71c14bd3a06d48e939c55cc894e4e1c` |
| `src-tauri/src/lib.rs` | +15/-2 | `e30f646c774658c912746f555d342fe9a5f46413a3fec30b9220fb586e3b6188` |
| `src-tauri/src/record_supply.rs` | +175/-5 | `1ec1abf71fb3af2f571396ff8edd096efd084e9265d19a5cffa3911b6efa5718` |
| `src-tauri/src/records.rs` | +58/-0 | `3ab54c5bd3139f2851ebd008b184772b2a5da1d196fcde21ab35b92bd529e84c` |
| `src-tauri/src/runtime_session.rs` | +495/-38 | `650c7e3119d9b14963132183fb400689a21f2486417383a994aacfe14b30c32c` |
| `src-tauri/src/workflow_record_store.rs` | +279/-3 | `75b07de715c69f80f8265f93871d44d78321b4be8515291a39f434b415c7ff55` |
| `src-tauri/src/workflow_record_store_tests.rs` | +148/-0 | `7c46c49695412aca3708e2076b27f35870e8ac01aeda3564b62288bba351f331` |
| `src-tauri/src/workflow_workspace.rs` | +88/-34 | `07f0cb56b1ddb9d49a1ec044f28477111256890b82ac9de55899cbf68527dc70` |
| `src/App.tsx` | +11/-5 | `de10a60737487030f31d9c61c0e37320f4cc769b1821d233a419904ddc0ab1b6` |

- Write fence: `DISPATCH.md` row J1 allows the WR store and workspace,
  `record_supply`, `records`, the Root receivers (`runtime_session.rs`,
  `lib.rs`, `App.tsx`) and an append to CONTRACT_ISSUES. The diff stays inside
  that fence. The CONTRACT_ISSUES change only appends. J2's entry was
  renumbered CI-19 on main, so CI-18 does not collide.

## Scope

The scope is the eight review questions in the brief, judged against:
- WR Design §16 (all of it), TT-1, TX-1, the LS table, WP-1…WP-7, SC-1…SC-6
  and RN-1…RN-5;
- the WR schemas `workspace-registration.schema.json` and
  `workflow-record-envelope.schema.json` (`cmp` shows the bundled copies equal
  the Design copies);
- RS §13.3, §13.6a, §13.7, §14.1 W-0…W-2 and VC-40, and `RS_RECORD.schema.json`
  `$defs/runId` and `$defs/recordId`;
- `CC-RS-WR-SUPPLY-FIT-ASTRA.md`, `I2-DEVELOPMENT-CATALOG.md` and
  `V6-WR-RS-PUBLICATION-IMPLEMENTATION.md`.

The following are out of scope: EXEC lifecycle (run open, run end, CH-1), the
native witness, and UI operation.

## Method actually performed

1. I extracted `git archive 8a785ac4e3 projects/chirality-app-v4` into
   `$TMPDIR/j1-review/`. That is the whole project, including `execution/`.
2. I ran the brief's full command in that copy, with the given `CARGO_HOME`,
   offline flags and Codex 0.160.0 pins. It exited 0. My log has SHA-256
   `200dfdc789d21473cc1261dfa232f14e283d932d20205f46c1903d2da737b2a2`.
   - `npm install --offline` and `npm run build` (`tsc --noEmit`, then
     `vite build`) passed.
   - `cargo test --offline --locked` gave 44 result lines: **610 passed (606
     top-level plus 4 nested subprocess runs), 0 failed, 3 ignored**. This
     matches J1's account and the counts in J1's `final-2-cargo-test.log`. My
     list of test names matches J1's log apart from the interleaving order of
     the nested runs.
   - `npm test` (`node --test tests/validate-records.test.mjs`): 3/3 passed.
3. I read the full diff and the surrounding unchanged code:
   - the store `publish`/`resolve`/`relations` path;
   - `PendingRecord`;
   - the Host's `history_dispatch`, `NativeItemsSupplyCheck`,
     `NativeItemCoverageSeal`, `finish_native_items_supply_check` and
     `HistoryDispatch`;
   - `records::append_reserved`;
   - `PreparedRunText::compare_observed_text`;
   - `lib.rs` `AppState.workspace`;
   - every caller of each new minting function (`grep`).
4. I diffed the two moved tests against the base. Only these change:
   - `fixture.selected()` becomes `fixture.registered()`;
   - `prepare_run` gains a `project` argument;
   - `run.prepared` becomes `run.prepared()`.

   Every assertion is byte-identical.
5. I ran five mutations of my own, each against the relevant filtered suites
   (`workflow_root`, `publication`, `supply`; M2b used the full suite), and
   restored the original bytes after each:

| ID | Mutation | Result |
|---|---|---|
| M1 | Send first: move pre-send publication and the WP-3 recheck after `turn_start_prepared_run_text` | **Caught**: 3 tests fail. `…publishes_before_send…` sees `[[]]` WR files at turn/start; `…publication_failure_sends_nothing…` sees 1 turn/start; `…refused_send…` sees 0 durable records |
| M2 | Accept development selections: `run_admission` always `Ok` and the store-level `RegisteredRevision` guard disabled | **Caught**: `…development_selection_run_is_refused_tt1_tx1` gets `Ok("run:workflow:…")` |
| M2b | Only the store-level `PreparedRunPublication::new` development guard disabled | **Survives**: full cargo suite, 44/44 result lines ok (F-6) |
| M3 | A reread reuses the first check's body `check` identity (SC-6 relabel) | **Survives**: 51/51 (F-4) |
| M4 | Drop the W-2 "record write failed" late-write limit in `append_live` | **Caught**: `…post_send_record_failures_retry_without_resend` |
| M5 | Drop the `pages.len() != seal.page_count()` binding in `from_native_coverage` | **Survives**: 51/51 (F-3) |

6. I added a temporary probe test, since removed, for the W-2 ordering case
   behind F-2. Its observed output is in F-2.
7. I read J1's `control-stage1.log` and `mutation1…4.log`. Its controls failed
   before implementation, and each of its mutations made one J1 test fail. The
   logs do not name the mutations, so I judged only their failing assertions.

## Answers to the review questions

**1. Ordering and failure semantics.** No send path runs without both records
being durable.
- `send()` (`runtime_session.rs:4234-4294`) runs four steps in order:
  1. it calls `publish_pre_send()`, which needs both `ProjectRecords::publish`
     calls to return a resolved record after the directory sync;
  2. it re-checks the exact text against the published `run_text` (WP-3);
  3. only then does it set `attempted = true`;
  4. it calls the only production sender.
- `grep` finds no other production caller of `turn_start_prepared_run_text`.
- On publication failure, `attempted` stays false and nothing is sent.
- `retry_records()` only publishes and never sends.
- Once `attempted` is set, a resend is refused.
- In the uncertain case (`FAIL_AFTER_LINK`), the selection is linked and the
  call returns an error. The retry then takes the existing-file branch. That
  branch compares the original serialized bytes, re-syncs, resolves, and only
  then publishes `run_text`. The test confirms that the identity, the bytes and
  `observed_at` (equal to the original `selected_at`) are unchanged.
- `FAIL_AFTER_LINK` and its injection point are `#[cfg(test)]` only.

**2. Minting authority.**
- `CompletedSupplyCheck` has private fields and no Clone, Deserialize or public
  constructor. Its only constructors are the two `pub(crate)` functions, and
  each has exactly one production caller (`runtime_session.rs:4337`, `:4343`).
- `PublishedSupplyCheck` is created only by `PendingSupplyCheck::publish`.
- `PendingSuppliedGuidance` is created only by `prepare_live`.
- The test helpers (`synthetic_for_test`, struct literals in the
  `workflow_record_store` child test module) are `cfg(test)` or
  module-private.
- No cold read, JSON or `ResolvedRecord` can reach any of these.

The seal-to-pages binding is adequate for the sole caller but is weak by
construction (F-3). Several things bind the pages in that caller:
- `read_native_items` takes each page from a Host-minted
  `AcceptedNativeItemPage`;
- the Host re-validates each continuation;
- `finish_native_items_supply_check` compares the last page with the Host's
  retained response.

`from_native_coverage` itself checks only that the page count equals the
sealed coverage.

**3. Mapping.** The state mapping is faithful.
- `equal composed text` maps to `verified`.
- The two `text differs` states and `incomparable` are copied from
  `compare_observed_text`, which works by method and then value.
- `not found` covers three cases: no user message, no text element, and no
  page item.
- `unreadable` covers a read failure after a Host-issued dispatch, an unusable
  page shape or cursor, and a located message without an item id. The schema
  requires `item` for the located states, so an item-less message cannot be
  verified. That reading is reasonable.
- R3 copies the state exactly through `correspond` (test
  `…each_read_maps_state_faithfully…`, 7 modes) and keeps
  `adoption: "unknown"`.
- `nativeTurn` is `check.turn`, and no R3 is produced without a turn, which
  matches RS §13.6a.

`incomparable` is reachable only in the pure mapping test, as J1 states. See
the display note in F-9.

**4. R3 writer.**
- `append_project_reserved` delegates to the existing `append_reserved`
  without weakening it. That function validates W-1 against the bundled
  schema, refuses when validation is unavailable, checks for a partial line,
  scans the whole project record set for identity conflicts, and keeps `seq`
  per writer.
- The reserved `recordId` and the original `observedAt` survive failures.
- An uncertain write that did land is recognised by its id and exact body,
  so it is not written twice.
- `note_project_late_write` is idempotent per subject (M4 caught).

One gap is ordering when the writer recovers between checks (F-2).

**5. Durable reader.**
- Resolution stays bound to the project descriptor. `list_references` only
  enumerates names and keeps those that parse as WR keys, and each one is
  resolved through `read_raw` with `openat`/`O_NOFOLLOW`. No out-of-project
  record can be resolved.
- The listing itself re-traverses the path, and it reads a dangling symlink as
  "no records" (F-5).
- Standing is truthful: `read_project_supply` claims "historical
  correspondence only; no live native witness, model adoption, registration or
  run lifecycle inferred", and the fresh-process test shows no `run_opened` or
  `run_ended` and no live run.

**6. Conformance calls.**
- **CI-18 is correct.** I checked the quoted TT-1, TX-1 and WP-6 text
  verbatim. The development catalog's standing is none of LS-1, LS-5, LS-6 or
  LS-8, and I2's "after its usual checks" does not override TX-1.
- The moved tests change only their call shape (Method 4).
- `run:workflow:<uuid>` matches `^run:[A-Za-z0-9._:/-]+$` (F-7).
- The RN-4 treatment departs from WR and is not logged (F-1).

**7. Test strength.**
- M1, M2 and M4 are caught.
- M3 and M5 survive, giving F-4 and F-3.
- M2b survives in the pre-existing store test, giving F-6.

**8. Collateral.**
- `compare_untrusted_pages` was refactored onto `locate_turn_text`, and its
  behaviour is equivalent: same states, same `item` and `located_by`, and the
  existing role/receiving tests pass.
- `lib.rs` only adds code: two commands, and `workflow_prepare_run` now passes
  `state.workspace`, the same explicit project the other record writers use.
- `records.rs` only adds code.
- In `App.tsx`, preparation is disabled unless `runnable === true`, with a
  visible reason. It adds a retry button and a read-only records button, and
  the raw JSON moves into `<details>`.
- `WorkflowRun.prepared` became the private `prepared()`, and there are no
  external users.

I found no unintended behaviour change.

## Findings

### F-1 MAJOR: a refused `turn/start` mints no WR `supply_check` *not found*; this departure from WR is not logged

- **Where:**
  - `runtime_session.rs:4271` and `:4288`: the status reads "RN-4 not-found
    check not minted";
  - `runtime_session.rs:4700-4712`: the test
    `workflow_root_refused_send_mints_no_check_and_keeps_r3_unavailable`
    asserts that exactly 2 WR files exist;
  - `CONTRACT_ISSUES.md`: no entry.
- **Evidence:**
  - WR §16.4, "Workflow in force": the row "*starting A* | `turn/start` refused
    or fails before the item is recorded" requires the record "`supply_check`
    *not found*".
  - WR §16.7 RN-4: "Refused or failed · `supply_check` *not found*".
  - The schema allows it. In `supply_check`, `turn` is optional, and `item`,
    `turn` and `located_by` are required only for the four located states.
  - RS §13.6a agrees with WR here: "if no source-bound turn is available,
    retain WR evidence and report R3 unavailable".
  - CC-RS-WR-SUPPLY-FIT says only that a failed send cannot establish supplied
    text or a `nativeTurn`, which is about R3. J1 handles R3 correctly.
  - `LOOP_INIT.md` (Change control): "Log each contract issue found in
    implementation in `app/CONTRACT_ISSUES.md`".
  - J1 resolved the tension between its brief ("mint only at the genuine native
    comparison boundary") and RN-4 by not minting. It disclosed this only in
    code strings and its return.
- **Consequence:** a refused run start leaves no durable WR evidence. A later
  process cannot tell "published, never sent" from "sent and refused by
  Codex". The new test fixes the departure in place as if it were the
  contract.
- **Needed:** one of the following.
  - Mint a *not found* check for a definite native refusal, citing the actual
    `turn/start` source receipt, with no `turn` and R3 still unavailable. Keep
    "no check" only for an unknown outcome, where *not found* would be an
    unsupported claim.
  - Or log a contract issue (next free number, CI-20) that states the conflict,
    the rationale and the alternative, for HELP_HUMAN or design-owner
    disposition, and adjust the test comment to cite it.

### F-2 MINOR: when the writer recovers between checks, a later R3 is appended before an earlier pending R3

- **Where:**
  - `runtime_session.rs:4362`: `check_native_supply` advances only the new
    slot;
  - `runtime_session.rs:4081-4106`: `WorkflowCheckSlot::advance`;
  - `record_supply.rs:118`: one late-write limit per entry.
- **Evidence:** my probe ran this sequence:
  1. block `.chirality/records/runs` and run check 1 (R3 pending);
  2. unblock and run check 2;
  3. call `retry_records`.

  The run's `app-workflow-supply-writer` log then held:

| `seq` | Kind | `observedAt` | Notes |
|---|---|---|---|
| 1 | `supplied_guidance` | `…52.995Z` | check 2 |
| 2 | `supplied_guidance` | `…52.513Z` | check 1, late |
| 3 | `evidence_limit` | — | "record write failed", subject check 1 |

  After check 2, check 1 stayed "pending write" until a manual retry. RS W-2
  says: "At the next append or retry, writes the pending entries in their
  order, then an `evidence_limit` … naming them". WP-5 says: "Retained RS
  entries follow W-0…W-2 in original order/time".
- **Consequence:** the log order inverts the observation order. `observedAt`
  and the limit keep the facts recoverable, so no evidence is lost.
- **Fix:** at each new check, advance earlier pending slots in order before
  appending the new R3. If an earlier slot cannot be written, hold the new one
  pending.

### F-3 MINOR: page bytes are bound to the seal by count only; the doc comment overstates this

- **Where:** `workflow_record_store.rs:351-354` (doc) and `:383` (the count
  check).
- **Evidence:**
  - M5 (remove even the count check) survives every J1 test.
  - The Host already retains each page's response (`native_item_source`,
    checked for the last page in `finish_native_items_supply_check`), so a
    byte-level check of every page is feasible.
  - The doc says the check is minted from "a consumed Host coverage seal plus
    the pages of that traversal". In fact any in-crate caller that holds a
    genuine seal can supply other pages of the same length.
  - J1's return states the gap. The code and CONTRACT_ISSUES do not.
- **Consequence:** this is not exploitable today, because the sole caller takes
  its pages from Host-minted accepted pages. It is a latent authority weakness
  for future in-crate callers.
- **Fix:** carry the accepted page bytes inside the seal, or have the Host
  compare each page with its retained response. Until then, state the limit in
  the doc comment.

### F-4 MINOR: a test gap on SC-6, since reusing the body `check` identity is not detected

- **Where:** `runtime_session.rs:4321`, and the tests at `:4614-4697`.
- **Evidence:** M3 survives. The tests assert distinct WR envelope `record_id`s
  per read, but not distinct body `check` identities. WR says "A check is never
  relabelled; a later read is a new check". The production code is correct (a
  fresh `opaque_id` on each read).
- **Fix:** assert that each read's `body.check` is unique.

### F-5 MINOR: `list_references` re-traverses by path after the descriptor checks

- **Where:** `workflow_record_store.rs:147-178`.
- **Evidence:**
  - It checks `.chirality/records/workflow` with `child()`, which uses
    `O_NOFOLLOW`.
  - It then calls `std::fs::read_dir(self.root.join(…))` and `Path::exists()`,
    both of which follow symlinks.
  - A dangling `.chirality` or `workflow` symlink returns `Ok([])`, read as "no
    records", instead of an error.
  - If the project path is replaced after `open`, names are enumerated from the
    other directory.
- **Consequence:** listing and standing can be misreported. Resolution still
  goes through the pinned descriptor, so no foreign record is resolved.
- **Fix:** enumerate from the pinned directory descriptor (`fdopendir` on a
  dup of the `child()` result), and report a non-plain `.chirality`, `records`
  or `workflow` entry as unreadable.

### F-6 NOTE: the store-level WP-6 development guard is untested in isolation (pre-existing)

- **Where:** `workflow_record_store.rs:666-673`. The test
  `typed_publication_retains_prepared_text_and_refuses_lost_source_or_development`
  dates from V6.
- **Evidence:**
  - M2b (guard disabled) passes the full cargo suite.
  - That test's development case fails for another reason. It pairs a
    development selection with a registered prepared text after deleting the
    revision store, so the admission mismatch or `verify_store` refuses it.
  - The statement in CI-18 that `PreparedRunPublication` refuses development
    admission is true of the code, but no test shows it.
  - J1's Root guard is tested (M2 caught).
- **Fix (optional):** add a store test that uses a development selection with a
  matching development prepared text.

### F-7 NOTE: `run:workflow:<uuid>` is an App-local RS `runId` with no EXEC `run_opened`

- **Where:** `runtime_session.rs:4020-4022`.
- **Evidence:**
  - The id satisfies `$defs/runId`.
  - WR §16.1 and §16.2 make the run identity DEL-02-03's.
  - The base already used an App-local `workflow-run:` id, so this is a prefix
    change only.
  - R3 entries are now written under that id without `run_opened`, which RS
    marks Required for R1. The fresh-process test shows that no run claim is
    made.
- **Fix:** record the interim nature where EXEC integration will see it (for
  example in CI-16's follow-up), not only in a code comment.

### F-8 NOTE: `unreadable_after_dispatch` accepts any Host-issued item dispatch for the same thread and turn

- **Where:** `workflow_record_store.rs:409-421`.
- **Evidence:** `HistoryDispatch` is `pub` and Clone, so a crate caller could
  pass a genuine dispatch issued for another purpose, such as History browsing
  of that turn. The sole caller passes only its own traversal's dispatches.
  This is crate-internal trust and acceptable as stated.

### F-9 NOTE: the display of *incomparable*

- **Where:** `runtime_session.rs:4115`.
- **Evidence:** `supplyReading` reads "supplied — not verified" for every
  non-verified state. RS §13.6a says *incomparable* reads "supplied — not
  verified, incomparable methods". This is unreachable in production today.
  Fix it when historical or other-method expected texts can occur.

### F-10 NOTE: integration items for the caller

- **Several selection records:** each `prepare_run` mints its own
  `selection_record` envelope. Preparing twice from one selection in one
  conversation yields two records with the same `selection_id`. One run at a
  time (CH-1) is EXEC's to enforce.
- **Pending custody is in memory only:** pending check and R3 custody is lost
  with the process (WP-5, as J1 states). `read_project_supply` shows *missing
  in record* for such checks. It does not surface W-2 late-write limits next
  to the R3 they qualify.
- **Shared RS limits block R3:** `append_live` refuses whenever any project RS
  log reports a limit. This is inherited from `append_reserved`, so one
  unrelated torn log blocks new R3 until it is repaired.
- **Panel states are untested:** they are covered only by `tsc` and a build. No
  UI test ran, as the brief required.
- **MEMORY.md entries:** `LOOP_INIT.md` asks for a Runs entry in each affected
  deliverable's MEMORY.md (DEL-02-02, DEL-04-03). That was outside J1's fence
  and remains for HELP_HUMAN.

## Verdict

**NOT READY.**

I found no BLOCKING defect.
- **Ordering:** both records are durable before the only send, publication
  failure sends nothing, there is no resend, and a retry keeps identity,
  bytes and `observed_at`.
- **Minting:** only Host-traversal evidence can mint a check, and only a
  published check yields R3.
- **Validation:** W-1 validation is intact.
- **Records:** there is no fallback store, and fresh-process records resolve
  with no run claim.
- **CI-18 and the moved tests:** both are correct.
- **Counts:** the suite counts match J1's account.

F-1 is an unlogged departure from accepted WR text (§16.4 and RN-4), contrary
to the loop's change-control rule, and a new test fixes it in place. The
candidate becomes READY when both of these hold:
- F-1 is repaired, or logged as a contract issue with a recorded disposition;
- F-2 is repaired, or explicitly deferred in that record.

F-3, F-4 and F-5 should be repaired or listed as known limits. F-6…F-10 need
no change before integration.
