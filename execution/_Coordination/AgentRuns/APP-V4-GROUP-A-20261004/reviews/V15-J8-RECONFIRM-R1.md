# V15-R1 — confirmation review of J8 repairs and the J6 merge

2026-10-08. Type 2 TASK reviewer for run `APP-V4-GROUP-A-20261004`, dispatched
by HELP_HUMAN (Claude Opus 5.5, Claude Code). Harness-native child, no
delegation. I wrote V15 and did not write this code. The candidate worktree
was read-only for me and was still clean at `7f0300cfe2` when I finished.
All builds, tests, mutations and probes ran in a `git archive 7f0300cfe2`
copy under `$TMPDIR`. My only write is this file. No commit, network,
credentials, `~/.codex`, model call, UI launch or native act.

**Verdict: READY.** F1, the MAJOR finding, is repaired: no path I found now
writes a ledger line that the App's own reader refuses, and one act keeps one
line. My probes P1, P2 and P5 now leave the ledger readable, with one line
per A15. F2–F5, F7 and F8 are repaired. F6 is resolved by the J6 merge: the
DS-8 descriptor selects J6's re-confirm statement and its "Re-confirm"
button.

One new MINOR finding remains (R1-1), and it is safe: no duplicate line and
no unreadable ledger. In one second-process case the first process keeps
showing "durability uncertain" indefinitely, although the ledger already
holds a definite *not completed* line, and CI-24 (b) describes that case
wrongly. I recommend a small follow-up, either before or after merge.
Everything else is a NOTE.

## Candidate and basis

| Item | Value | How checked |
|---|---|---|
| Candidate | `claude/app-v4-j8-reconfirm` at `7f0300cfe2` | `git rev-parse`, `git status` clean |
| History | `5ccfcba039` (repairs) → `673ef66d53` (merge, parents `5ccfcba039` and `9d1e0bb0cd`) → `7f0300cfe2` (journey test and CI-24 (f)) | `git log --format='%h %p %s'` |
| Against the integration head `9d1e0bb0cd` | only J8's 7 files differ; `a15_native.rs` and `act_control_a15.rs` are unchanged | `git diff --stat` |
| `workflow_library.rs` | sha256 `2c82d7e2…eed4bd1`, the same at `5ccfcba039` and `7f0300cfe2` | `git show … \| shasum` |
| Basis | as in V15 (WR `6bfb2277…`, WR schema `6f772b3b…`, AAC `94409f56…`, `OWNER_DECISIONS.md` `223f9093…`); J6's `a15_variant`, `a15_buttons` and `a15_native.rs:80–110` read at the candidate | as stated |
| Implementer logs | `validation/J8R_7f0300cf/`, `SHA256SUMS` 25/25 OK. Control `52870b53…bea1a` shows 0/3 on `1a74f7f307`. Cargo log `fa39ef49…ce35`. Each mutation log opens with its diff and closes with a revert hash equal to the pristine `2c82d7e2…` | `shasum -a 256 -c` and reading the logs |

## Suite (`git archive 7f0300cfe2`)

| Part | Result |
|---|---|
| `npm run build` | pass |
| `cargo test --offline --locked --no-fail-fast`, top level | **40 binaries, 717 passed, 0 failed, 3 ignored** |
| Nested worker runs | **4, each 1 passed**. One result line is interleaved with another test's line (log l. 1345–1346), as the implementer reported |
| `npm test` | 7 passed, 0 failed |
| `python3 schemas/sync.py` | "6 schema resources match …" |

The known flaky tests passed on the first run. These counts match the
implementer's.

## Status of V15 findings

| ID | Status | Evidence |
|---|---|---|
| F1 (MAJOR) | **Repaired** | `rc9_guard` (`workflow_library.rs:923`) runs `check_reconfirmation_lines` over `rows + [line]` before every re-confirmation append: the in-process retry of an intended line (l. 1124), G-4R before the journal is written (l. 1289), `fail_entry` (l. 1349) and X-2 (l. 1574). If the reader would refuse the line, nothing is appended and the attempt stays pending. The already-cited check (l. 1131–1144) runs before G-1 for a re-confirmation: if a ledger line already cites the receipt's A15, it appends nothing, closes the journal and ends the attempt *not completed* in this process, naming that line. Probes rerun: **P1** gives "X-2 pending: re-confirmation line not appended: … RC-9 …" and the ledger reads `Ok(1)`. **P2** gives *NotCompleted* "A15 … already has ledger line 2 (not completed); nothing appended …", one line cites the A15, and the ledger reads `Ok(2)`. **P5** gives *Pending* "re-confirmation line not appended …" and the ledger reads `Ok(1)`. The tests `v15_p1_…` (l. 1481), `v15_p2_…` (l. 1525) and `v15_p5_…` (l. 1576) are red on `1a74f7f307` (control log, 0/3). CI-25 records the WR conflict. CI-24 (b) is corrected, apart from one sub-case (R1-1) |
| F2 (MINOR) | **Repaired** | New tests `v15_f2_rc5d_…` (l. 1615), `v15_f2_ls4_record_bound_to_other_content_is_ds4` (l. 1635), `v15_f2_rc9_reader_names_each_breach` (l. 1671, 8 cases: `reconfirms` sequence and identity, another slot, identity, prior, reviewed content, a *not completed* line, a later line) and `v15_f2_g1r_registered_line_changed_is_not_completed` (l. 1765). The implementer's MA–ME logs are now killed. Two new guards are untested (R1-N3) |
| F3 (MINOR) | **Repaired** | `standing_as_read` returns the snapshot it verified, and RF-1 copies those bytes (l. 117–120). The copy goes through `publish_reserved_store` (l. 134), which is exclusive and removes partial copies. A failure in `sync_package`, `sync_dir` or the base record goes through `discard_unbased_copy` (l. 138–150). Tested by `v15_f3_…` (l. 1799, cases (a) base and (b) directory sync). My N7 (return on a sync failure without cleanup) is killed |
| F4 (MINOR) | **Repaired at G-1R** | `ActRecordFault` (l. 872) separates `LogUnreadable` from `Incomplete`. At G-1R an unreadable log keeps the attempt pending (l. 1250), and a missing record or one bound to other content ends it *not completed* (l. 1256). `v15_f4_…` (l. 1857) restores the log and the same attempt then completes. My N4 is killed. **The WR-VC-19 test change is honest.** Renaming the `recordId` in place keeps the log fully readable (schema-valid, sequence intact), so the reader genuinely does not find the record, which is exactly LS-4 "record missing". Deleting the line, as before, now creates a sequence gap, a read limit, and that case is pending by design. CI-24 (k) discloses that a sequence gap counts as unreadable. The review-time wording is NOTE R1-N1 |
| F5 (MINOR) | **Repaired** | `registered_listing` (l. 83) feeds the Root snapshot `libraries[].registered` (`runtime_session.rs:3855`). The label is WR's "registered — re-confirm to use in this App session", or "… selectable in this App session" when this process holds the result. `App.tsx:339` shows the active library's rows, each with a Refine button. Tested by `v15_f5_…` (l. 1890). My N5 is killed. The list does not show LS-4 standing (probe P7; disclosed in CI-24 (l)) — NOTE R1-N2 |
| F6 (NOTE) | **Resolved by the merge** | `a15_variant` (`act_control_a15.rs:313–321`) chooses the re-confirm variant when the descriptor kind is `a15_descriptor` and the disposition is *re-confirmation*. That gives the statement "Re-confirm revision ‹short k› of ‹origin›:‹name› for use in this App session. This registers no new revision." (l. 399–406) and the buttons [Don't re-confirm] [Re-confirm] [Cancel] through `a15_buttons`, where only `chose(…, variant.act)` captures (`a15_native.rs:90–99`). The variant is read from the frozen binding's descriptor, which the DS-8 path composes with that disposition. Journey step 9 asserts the "Re-confirm" label, the statement and the absence of "Registering makes", and that a registration keeps "Register". CI-24 (f) is accurate |
| F7 (NOTE) | **Repaired** | Each implementer mutation log opens with its diff and the pristine hash and closes with "reverted; sha256 … == pristine" |
| F8 (NOTE) | **Repaired** | X-2 lists cheaply first, takes the lock, lists again (l. 1528), and reports a vanished journal as "already closed" (l. 1540). This is untested (R1-N3) |

## New code: the questions asked

- **Can `rc9_guard` wedge an attempt, and is pending recoverable?**
  - **In process.** A guard refusal returns `Err` before `Progress::Intended`
    is set (`fail_entry`, G-4R) or while it stays set (the retry path). Each
    Continue therefore re-evaluates against the current ledger. Once the
    ledger is restored, the same attempt can proceed; this is the same
    mechanism as in `v15_f4_…`. Otherwise it stays pending until the process
    ends. Nothing persists after that, because G-1R and G-4R refuse before
    the journal is written, and the act stays in the act log with no effect
    (CI-25).
  - **At X-2.** A refused journal is kept and reported as "X-2 pending" on
    every open until the ledger is repaired or the journal is removed by
    hand. That is recoverable by hand only, it is disclosed in CI-24 (b),
    and it is safe.
  - **Conclusion.** No path wedges into a wrong state.
- **Is the already-cited ending honest in the UI?**
  - Yes for the case it covers (P2). Root shows "not completed" with the
    reason naming the existing line and its outcome. The ledger holds that
    line, and ‹k› is not held.
  - It covers only attempts that are not in *Intended*. The intended case is
    R1-1.
- **Do the listing or the per-row Refine widen authority?** No.
  - The listing reads the ledger under the owner's `try_lock` and only
    displays it.
  - Per-row Refine calls the existing `workflow_refine_registered` command,
    with a name and revision taken from the ledger. The command was already
    reachable with any arguments, and `refine_from_store` still validates the
    name, the registered line and the standing as read.
  - No selection, act or capture is created.
- **Is the merge resolution correct?** Yes.
  - Against `9d1e0bb0cd`, `lib.rs` adds only `workflow_refine_registered`
    (the function and its `generate_handler!` entry), keeping J6's
    `workflow_review_digest` and `native_confirmation_content`.
  - `App.tsx` keeps J6's digest paragraph and `readablePaths`, and adds
    J8's listing, Refine input, DS-8 note, button wording and *re-confirmed*
    selection. The digest paragraph now names "Re-confirm" for DS-8.
  - J6's `act_control_a15.rs` and `a15_native.rs` are untouched.
- **Does the DS-8 descriptor select J6's variant?** Yes; see F6 above. One
  cosmetic difference remains (R1-N4).

## Mutations (mine, on `7f0300cfe2`)

Each was run against `cargo test --lib -- workflow` (145 tests). Afterwards
both files compared byte-equal to the candidate (`cmp`).

| ID | Mutation | Result |
|---|---|---|
| N1 | Drop the already-cited check | killed (`v15_p2_…`) |
| N2 | Drop `rc9_guard` in `fail_entry` | killed (`v15_p5_…`) |
| N3 | Drop `rc9_guard` in X-2 | killed (`v15_p1_…`) |
| N4 | Treat an unreadable act log at G-1R as a missing record | killed (`v15_f4_…`) |
| N5 | Listing never marks a row as held | killed (`v15_f5_…`) |
| N6 | Drop `rc9_guard` on the intended-line retry | **survived** (R1-N3) |
| N7 | RF-1 returns on a sync failure without cleanup | killed (`v15_f3_…`) |
| N8 | X-2 treats a vanished journal as an error (F8) | **survived** (R1-N3) |

## Probes (rerun; source kept as `v15r1-probe-tests.rs.txt`)

| Probe | V15 (`1a74f7f307`) | R1 (`7f0300cfe2`) |
|---|---|---|
| P1 bad journal at X-2 | ledger unreadable | "X-2 pending … RC-9 …"; ledger `Ok(1)`; journal kept |
| P2 directory-sync fault + second process + Continue | 2 lines for one A15; ledger unreadable | *NotCompleted* "already has ledger line 2 (not completed)"; 1 line; ledger `Ok(2)` |
| P3 unrelated invalid act-log line | DS-4 "LS-4 … act log not completely readable" | unchanged at review (disclosed, CI-24 (k)) |
| P4 RC-5 (d) | correct | correct; now tested |
| P5 registered line no longer registered after capture | ledger unreadable | *Pending* "re-confirmation line not appended …"; ledger `Ok(1)` |
| **P6 (new)** append refused (ledger made read-only), then process C opens (X-2), then B continues twice | — | C writes *not completed*. B stays *Pending* "registration ledger durability uncertain; same hot attempt retained" on every Continue. 1 line cites the A15; ledger readable (R1-1) |
| **P7 (new)** listing when ‹k›'s store no longer recomputes | — | row labelled "registered — re-confirm to use in this App session" (R1-N2) |

## Findings (R1)

| ID | Severity | Where | Rule | Failure scenario (evidence) | Repair |
|---|---|---|---|---|---|
| R1-1 | MINOR | `workflow_library.rs:1105–1126` (intended-line path); CI-24 (b) | NA-6 state limits; CI-24 (b) accuracy | **Trigger.** Process B's append fails without writing, so its progress is *Intended*. A second process's X-2 then writes *not completed* for B's A15. **What B does.** On every Continue, B takes the intended path. That path refuses on `ledger_seq` ("intended ledger line no longer appendable"), and `advance` replaces the cause with "registration ledger durability uncertain; same hot attempt retained", indefinitely. **Safe.** One line, readable ledger, ‹k› not held (P6). **What is wrong.** CI-24 (b) says that when the first process continues, "G-1R finds the ledger already citing its A15 … ends the attempt *not completed* … naming the line". That is true only when the attempt was not in *Intended*, which is the P2 case | In the intended path, before the `ledger_seq` check: if another line cites this A15 (`v != &line`), set `Failed` with the same "already has ledger line ‹n›" reason. Add P6 as a test. Or, at minimum, correct CI-24 (b) to name this case |
| R1-N1 | NOTE | `workflow_library.rs:319`; RF-1 message at l. 120 | CI-24 (k) "a read limit, not LS-4" | At review, an unreadable log still reads "whose standing is LS-4 registration record incomplete: act log not completely readable …" (P3). The cause is exact; only the LS-4 label is wrong | Word it "standing not readable: ‹cause›" when the fault is `LogUnreadable` |
| R1-N2 | NOTE | `registered_listing` l. 83 | WR §4.6 "shown as read" | The listing labels an LS-4 row "registered — re-confirm …" (P7). Refine then refuses with the LS-4 cause. Disclosed in CI-24 (l) | Optional: add the standing as read per row |
| R1-N3 | NOTE | l. 1124; l. 1536–1544 | Test coverage | N6 (the guard on the intended retry) and N8 (F8's vanished journal) survive. Both are defensive and both are correct by reading | Optional tests |
| R1-N4 | NOTE | `reconfirmation_view` (`statement` uses the sequence) vs `act_control_a15.rs:403` (short revision) | AAC §4.2 "in substance" | The in-App note says "Re-confirm revision 3 of project:…", while the native statement says "Re-confirm revision 1a2b3c4d5e6f of project:…". Both identify ‹k›. The person sees two forms | Optional: show both forms in one place |
| R1-N5 | NOTE | l. 1250 and l. 1256 | — | `act_record_found` is read twice at G-1R. If the log changes between the two reads, a read limit can end the attempt *not completed* | Call it once and match on the fault |

## CI-24 / CI-25 accuracy

- **CI-24.**
  - (a), (c), (d), (e), (g), (h), (i) and (j) are unchanged and accurate.
  - **(b)** is accurate on the journal location, X-2 under the lock, the
    RC-9 refusal and the P2 path. It is inaccurate on the intended sub-case
    (R1-1).
  - **(f)** is accurate. I checked `a15_variant`, the buttons and journey
    step 9.
  - **(k)** is accurate, including "As before, any unreadable line … blocks
    DS-8" and "a sequence gap".
  - **(l)** is accurate ("It does not check LS-1; Refine checks it").
  - **(m)** is accurate.
- **CI-25** is accurate. It states the WR G-1R vs RC-9 conflict, the App's
  stricter behaviour, the "slot moved on" variant (P5's actual path), and the
  `written_at` case that still writes *not completed*. Its tests exist and
  pass, and it offers the WR owner options.

## Logs

`$TMPDIR/v15r1/logs/` (`/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/v15r1/logs/`), with `SHA256SUMS`:

| File | sha256 |
|---|---|
| `01-npm-build.log` | `a3e4b5c0376fdfd34f5d110474a63c1415d155e299f7316ea4ef3a45583e67f8` |
| `02-cargo-test.log` | `711fa3c3ac029c36253e3872d85dc115a3f0faeccd6849739d2508c39c630e38` |
| `03-npm-test.log` | `02c2c366a3d5883f8ffc33c422b11fda9e837949b3b5bf6b3d45f532e32254b1` |
| `04-schema-sync.log` | `41fcd5fa95db8bc1d13cdd5d6c6770c91ca1bbbcb7647c6fbcc36a054b8ee6cc` |
| `mut-N1.log` … `mut-N8.log` | `1350baf5…bb88`, `7cde02d1…a66`, `dfb4109a…a8b1`, `769166a5…3e73`, `3d1b5ff2…bcaf`, `00b2de06…35ea`, `f816b3fc…0c91`, `aa7f57d7…13f4` |
| `probes.log` | `14f5bff0232846c1103d1e32fbc76f6b19f8a9096243159e91f3e4c482d6615b` |
| `v15r1-probe-tests.rs.txt` | `ec36a2c7f07f8dfd83b9b4e67eabccd79a7da7ad479e3f2097306af7ce77e449` |

## Limits

- No native act, UI launch or native witness. The J6 variant was checked
  through the test double and by reading the code.
- "Second process" means a second `LibraryOwner` on the same root.
- P6 refuses the append by making the ledger file read-only. That is one way
  an append can fail without writing.
- I did not rerun the implementer's 13 mutations. I checked their logs and
  hashes.
- `$TMPDIR` is machine-local.

## Return

- Verdict: **READY.**
- Recommended small follow-up, before or after merge as HELP_HUMAN prefers:
  R1-1. Either fail with "already has ledger line" on the intended path and
  add P6 as a test, or correct the CI-24 (b) text.
- NOTEs R1-N1…N5 are optional.
- No owner question. CI-25 goes to the WR owner.
