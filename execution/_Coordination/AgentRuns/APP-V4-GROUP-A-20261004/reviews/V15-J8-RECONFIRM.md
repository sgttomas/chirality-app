# V15 — independent code review of J8 (DS-8 A15 re-confirmation and RF-1)

2026-10-08. Type 2 TASK reviewer for run `APP-V4-GROUP-A-20261004`, dispatched
by HELP_HUMAN (Claude Opus 5.5, Claude Code). Harness-native child, no
delegation. I did not write this code. The candidate worktree was read-only
for me, and it was still clean at `1a74f7f307` when I finished. All builds,
tests, mutations and probes ran in a `git archive` copy under `$TMPDIR`. My
only write is this file. No commit, network, credentials, `~/.codex`, model
call, UI launch or native act.

**Verdict: NOT READY.** Most of the change follows the adopted WR text. DS-8
is offered only for an LS-1 ‹k› that this process does not hold. No new
revision, sequence, store folder or published copy is created. Selection
comes only from this process's own commits. X-2 never completes a
re-confirmation. F14 does not regress J5. The full suite passes (686
top-level), and the core paths kill the mutations aimed at them. One MAJOR
finding blocks merge (F1). On three paths the App writes a re-confirmation
ledger line that its own RC-9 reader then refuses. After that write, every
review, registration, Refine and X-2 in that library fails until someone
repairs the ledger by hand. One of the three paths is a production fault
path that CI-24 (b) describes as harmless. Each path was shown with a
probe. The repair is small: run the RC-9 check before every append, and
check at G-1R that the act is not already cited. F2–F5 are MINOR.

## Candidate and basis

| Item | Value | How checked |
|---|---|---|
| Candidate | `claude/app-v4-j8-reconfirm` at `1a74f7f307`; parent `39519096c4`; base `007489e72b` | `git log`, `git rev-parse` in the candidate worktree; `git status` clean |
| Files changed `007489e72b..1a74f7f307` | 7: `CONTRACT_ISSUES.md`, `lib.rs`, `runtime_session.rs`, `workflow_journey_tests.rs`, `workflow_library.rs`, `workflow_library_tests.rs`, `App.tsx` | `git diff --stat`. `a15_native.rs` and `act_control_a15.rs` are not in the diff, so `1a74f7f307` restores them to the `007489e72b` blobs, as stated |
| `changes/CC-WR-RECONFIRM.md` (rev. 2) at `007489e72b` | `0b3678ce…b9d603e` | sha256 of `git show` bytes |
| `reviews/V13-CC-WR-RECONFIRM.md` at `007489e72b` | `f6a9d73b…d740f2` | as above (this differs from the `5b1a8260…` the change record cites; the file was extended in the adoption commit) |
| WR `WORKSPACE_AND_REGISTRATION.md` at `007489e72b` | `6bfb2277…251838` (equals the change record's postimage) | sha256 |
| WR schema, Design copy and App copy at `007489e72b` | both `6f772b3b0f51abf750fc0970a169ea3ff601d2015f3a6941308aff87c1ef51f5` (equals the change record's postimage); byte-identical (`cmp`) | sha256, `cmp` |
| AAC `APP_ACT_CONTROL.md` / `aac.offer.schema.json` (Design) at `007489e72b` | `94409f56399da797…f71426` / `34e61d5ac20bc448…d603e` | sha256; read §1.2 A15 row, §4.2 incl. the re-confirmation paragraph, §5.1, VC-AAC-08; schema `allOf/6` |
| `OWNER_DECISIONS.md` at HEAD `81a18adea4` | `223f9093…c5ac` | sections "SEAL-2 explicit deferral", "Rerunning an unchanged workflow after relaunch", "Native confirmation default key — 2026-10-08" read |
| `app/CONTRACT_ISSUES.md` | base `a0b72061…f426`; candidate `a032c98b…68a2068` | CI-18…CI-24 read |
| Role basis | `AGENTS.md` `f96feb19…`, `agents/AGENT_TASK.md` `1a13a5b0…`, `loop/LOOP_INIT.md` `c2e88f81…` | sha256 |
| Format | `reviews/V14-J6-PRESENTATION.md` at HEAD `5c754ef6…ac5` | sha256 |
| Implementer logs | `validation/J8_1a74f7f3/` in the HELP_HUMAN worktree | `shasum -a 256 -c SHA256SUMS`: 17/17 OK |

WR sections read: §4.1 (SP-4 incl. DS-4/DS-8, SP-4a), §4.3 RB-3/RB-4/RB-8,
§4.6 (LS table, LS-1 note, RF-1), §4.8 RC-1…RC-10, §5.1–§5.4 rows tagged
CC-WR-RECONFIRM, §6 R-3, SQ-G note, X-2, X-4, §8 rows, §9 row, §12 WR-VC-16…20,
§15 U-WR-21…23. Schema `$defs`: `reconfirmed_revision`, `library_entry`
(incl. `allOf`), `identity_or_none`; WD `workflow_identity` (no null
`derived_from`, so the serde round trip of ‹k›'s tuple is exact).

## Suite

Command as briefed, in `$TMPDIR/v15-j8/copy` (a `git archive 1a74f7f307` of
all of `projects/chirality-app-v4`; `node_modules` symlinked read-only from the
candidate worktree; `CARGO_TARGET_DIR` under `$TMPDIR`).

| Part | Result |
|---|---|
| `npm run build` | pass |
| `cargo test --offline --locked --no-fail-fast` | 44 `test result:` lines, all ok. **Top level: 40 binaries, 686 passed, 0 failed, 3 ignored.** Nested worker runs (nonzero "filtered out"): 4, each 1 passed |
| `npm test` | 3 passed, 0 failed |
| `python3 schemas/sync.py` | "6 schema resources match source bytes, hashes and declared IDs" |

The known flaky tests (`credential_rpc_*`, `handshake.rs`) all passed on the
first run, so I did not rerun them. The implementer's `j8-full-2-cargo-test.log`
gives the same counts (690 including the 4 nested). All 10 new or changed J8
tests pass: `wr_vc_16…20` (5 functions for WR-VC-19 and 20), `rf_1_…`,
`j8_control_…`, the J5 test, and journey step 9.

## Q1 — Faithfulness to the adopted text

These checks hold. Each was verified by reading the code against the WR rule,
and the line marked "probe" was also run.

- **SP-4a order.** `review` (`workflow_library.rs:255–306`) decides DS-5 and
  DS-6 first, then SP-3 through `lineage_reaches` (DS-3), then identical
  content (DS-4 or DS-8), and otherwise DS-2. WR-VC-18 tests "identical bytes
  without a base → DS-3".
- **RC-1 / DS-4 / DS-8.** ‹k› may be any registered line of the slot. The
  checks run in this order:
  - `is_held` gives DS-4 "identical to revision ‹n›; select it instead".
  - `standing_as_read` failing gives DS-4 with LS-4 and the exact cause:
    record not found, bound to other content, store not readable, or not
    recomputing.
  - Otherwise the disposition is DS-8.

  The messages match SP-4's substance.
- **RC-2.** `held` is filled only by `hold()`, which `finish_commit` and
  `finish_reconfirm` call (l. 1292, 1225). It is never filled from disk. X-2
  never calls it. Each Root library context opens one owner per root and
  process (`runtime_session.rs:3877–3925`), so the set is not lost between
  calls.
- **RC-3, and no new identity anywhere.**
  - The subject is ‹k›'s tuple from its line (`identity = k`, l. 291).
  - The *re-confirmed* line copies ‹k›'s `sequence` and `store_path` and uses
    ‹k›'s own prior (`act_prior`).
  - G-2R/G-3R only recompute the store. There is no G-5.
  - Root reports `"newRevision":false` (`runtime_session.rs` ~4704).
  - Tested in WR-VC-16 and journey step 9: one store folder, the published
    copy unchanged, and the ledger identity equal to ‹k›'s.
- **RC-4.**
  - Wording and purpose are correct, and `freshness.slot_latest` is the slot's
    latest at review (`workflow_workspace.rs:320`).
  - `relations.prior_revision` and `derived_from` are ‹k›'s own.
  - `registration_disposition.prior_revision`, which is `review.prior`, stays
    the slot's latest.
  - The receipt binding compares `a.prior()` with `act_prior(e)` (l. 627).
- **RC-5.**
  - (b) is compared through `slot_latest_now` (l. 491).
  - (c) requires exact equality of the whole registered line, act record and
    store recompute (l. 513–547).
  - (d) is `is_held`. Probe 4 confirms that a second review goes stale with
    "already selectable".
- **RC-6.**
  - Order: G-1R (slot latest, then the line, the act record and `held`), then
    the App's base check (CI-24 (h)), then G-2R (store), then the journal
    (*stored*), then G-4R, then G-6R.
  - Everything runs under the ledger lock held by `advance`.
  - An unreadable ledger leaves the attempt pending.
- **RC-9 reader.** `check_reconfirmation_lines` (l. 766–828) implements every
  listed check. `latest()` ignores non-*registered* lines.
- **RC-10.** `reconfirmation_view` and `registration_notice` carry ‹k›'s
  sequence and LS-1 as read, the earlier registration time and act labelled
  "registered earlier; not verified in this session", the slot's latest when
  it is not ‹k›, the base, and the sentence.
- **AAC.** The offer passes through `compose_a15` unchanged and validates
  against the adopted offer schema, whose `allOf/6` was checked. CI-24 (e)'s
  claim about `entry:` was checked against `allOf/6` and is accurate.

## Q2 — Failure and concurrency

- The G-1R failure branches write *not completed* citing the new A15, and X-2
  never completes an attempt. Both are tested (WR-VC-19).
- **CI-24 (b) is not accurate, and the defect behind it blocks merge (F1).**
  - A journal exists outside the lock only after the append failed or was
    uncertain, or after `write_attempt_journal` failed once the file was
    already visible.
  - In the last case the progress is *Pending*, not *Intended*. A later
    **Continue** therefore re-runs G-1R from scratch, and G-1R does not check
    whether the ledger already cites the attempt's own A15.
  - If a second App process opens the library in between, its X-2 writes
    *not completed* for that A15. The first process then appends
    *re-confirmed* for the same A15 and holds ‹k› (probe 2).
  - The result is two lines for one act, and the reader refuses the whole
    ledger.
- In the other cases a second process is safe: either the line exists, or
  the Intended path refuses the append on a `ledger_seq` mismatch.
- I judge the second-process limit acceptable to integrate once F1's
  check is added and CI-24 (b) is corrected. It is not acceptable as written.

## Q3 — RF-1

- It never overwrites. `symlink_metadata` refuses an existing target, and
  `publish_new` uses an exclusive `create_dir`.
- Standing as read is required. Tested: LS-4 gives no draft.
- The App-kept base is recorded with `put(name, k, false)`, read from the
  ledger at that time, and shown and frozen at review. Tested, including a
  revision registered in place.
- It makes no selection.
- Cleanup covers only a failure to record the base (F3).

## Q4 — F14 and J5

- G-1 and RB-3 (b) compare `latest()` of the slot's *registered* lines
  instead of the whole slot.
- Registered lines are append-only, and `latest()` refuses a revision
  registered twice. A changed latest is therefore exactly "a registered line
  was added", and the DS-2 sequence (`e.slot` registered count + 1) stays
  correct.
- The in-place and multi-entry paths keep "slot moved on" when a
  registration lands.
- The J5 base check was moved into `base_changed`. For registrations it runs
  in the same order as before.
- The presentation's `base`/`stale_base` now read the App-kept base. For
  DS-2 this equals the old `identity.derived_from`; for in-place entries both
  are none.
- All J5 tests pass. The J5 assertion change (DS-4 → DS-8 after relaunch,
  DS-4 kept in the same process) is the change named in the change record's
  App items ("about line 495 … not by weakening a check").

## Q5 — Tests and mutations

**My mutations.** Each was run against `cargo test --lib -- workflow` (135
tests), then reverted. Afterwards both files compared byte-equal to the
candidate blobs (`cmp`).

| ID | Mutation | Result |
|---|---|---|
| MA | RF-1: skip `discard_unbased_copy` when the base is not recorded | **survived** |
| MB | RC-9: drop the same-slot / `reconfirms.identity` / `sequence` check | **survived** |
| MC | RC-5 (d) in `current()`: drop the `is_held` check | **survived** (the behaviour is correct, probe 4; no test asserts it) |
| MD | LS-1 as read: accept an A15 bound to any content | **survived** |
| ME | RC-9: drop the "reviewed content is the revision" check | **survived** |
| MF | G-1R: drop the `is_held` check | killed (`wr_vc_19_dismissal…`) |
| MG | RF-1: skip `standing_as_read` | killed (`wr_vc_17…`) |
| MH | Ledger line uses the slot's latest as prior instead of ‹k›'s own | killed (6 tests incl. journey) |
| MI | Keep the snapshot identity instead of ‹k›'s tuple (RC-3) | killed (6 tests incl. journey) |

**Implementer mutations.** The six logs (`mut1`, `mut1b`, `mut2`…`mut5`)
each show the named tests failing, and the control log is red on the
pre-change code (`workflow_library_tests.rs:822`). The logs do not include
the mutation diffs, so I could confirm only the failures, not what was
mutated (F7).

**Probes** (temporary tests appended to the copy and then removed; source
kept as `v15-probe-tests.rs.txt`):

| Probe | Result |
|---|---|
| P1: X-2 from a journal whose intended line is schema-valid but breaks RC-9 (`reconfirms.sequence` 2) | X-2 appends; then `read_ledger` → "registration ledger ambiguous … line 2 (not completed) names line 1 with another slot, tuple or sequence" |
| P2: process B publishes the journal but the directory sync fails (`storage::fail_directory_for_test`, the production `create_json → sync_publication` path) → *Pending*; process C opens the library (X-2) → *not completed*; B continues | B reports *ReConfirmed*, holds ‹k›; **2 ledger lines cite one A15**; `read_ledger` → "line 3 (re-confirmed): its A15 … is cited by another ledger line" |
| P3: one unrelated invalid line appended to the library act log | the DS-8 review becomes DS-4 "LS-4 … act log not completely readable: … invalid line 2" |
| P4: two DS-8 reviews; A commits; B's `current()` | Err "already selectable in this App session" (correct) |
| P5: after capture, registered line 1 edited outside the App so it no longer reads as registered (WR G-1R "line changed or missing") | the attempt ends *not completed* "slot moved on", and `read_ledger` → "line 2 (not completed) re-confirms line 1, which is not an earlier registered line" |

## Q6 — Root and UI wiring

- **Refine command.** `workflow_refine_registered` (`lib.rs:641–643`, and
  registered in `generate_handler`) calls `refine_registered`
  (`runtime_session.rs` ~3995). That calls the owner under `try_lock`, for
  the active library only, with validated name and revision. It writes only
  a new draft and the App-kept base, and makes no selection, so no authority
  is widened.
- **Status and selection.** Root records *re-confirmed* outcomes in
  `registered` (selectable in this process only) and shows them as
  `"state":"re-confirmed","newRevision":false,"selectable":"in this App
  session only"`.
- **Refusal messages.**
  - The cold `select_hot_registered_copy` refusals now name the route
    ("registered — re-confirm to use in this App session (Review a draft
    with its bytes, or Refine to make one)"). This is accurate.
  - The "Actual hot registered revision unavailable in this review" refusal
    adds "registered — re-confirm …". That is also correct when the revision
    is held by a different review in this process, but there it is not the
    best route; this is minor and not raised as a finding.
- **`App.tsx` (l. 280–289).** For DS-8 it shows the message and statement
  and labels the button "Re-confirm this revision …". Selection is offered
  for *re-confirmed* entries. Refine needs the content identity typed in by
  hand (F5).

## Findings

| ID | Severity | Where | Rule | Failure scenario (evidence) | Repair |
|---|---|---|---|---|---|
| F1 | **MAJOR** | `workflow_library.rs:1141–1197` (`advance_reconfirmation`, G-1R…G-4R), `1244–1252` (`fail_entry`), `1391–1465` (`reconcile_reconfirmations`); the reader at `766–828` | RC-7 / RB-8 "one act never has two ledger lines"; RC-9 (the App's own reader); WR G-1R "line changed or missing → *not completed*" | The App appends re-confirmation lines without checking them against RC-9, and G-1R does not check whether the ledger already cites the receipt's A15. Three demonstrated paths: (a) P2, a production fault path (a journal publication whose directory sync fails), a second App process opening the library, then Continue gives two lines for one A15; (b) P5, WR's own G-1R branch for a registered line edited or removed after capture writes a *not completed* line whose `reconfirms` breaks RC-9, so the WR rule conflicts with RC-9 here and the conflict is not logged; (c) P1, X-2 appends whatever a malformed or foreign journal names. In each case `read_ledger` then refuses the **whole** library ledger, all slots, until hand repair. CI-24 (b) says only that the attempt "would close … as lost", which is inaccurate. WR-VC-19's "registered line changed after capture" case is untested | (1) A helper used before **every** append of a line with disposition *re-confirmation* (`fail_entry`, G-4R, X-2): run `check_reconfirmation_lines` over `rows + [line]`. If it would fail, append nothing and leave the attempt pending with the exact cause. (2) At G-1R, if any ledger line already cites `receipt.record_id()`, end the attempt without appending: treat it as *not completed* in this process only, citing that line. (3) Log the WR G-1R vs RC-9 conflict for the WR owner as a new CI item: the "missing / no longer registered" branch cannot write an RC-9-valid *not completed* line. (4) Correct CI-24 (b). (5) Add P1, P2 and P5 as tests |
| F2 | MINOR | `workflow_library_tests.rs` (J8 block) | WR §12 WR-VC-19 and WR-VC-20 as designed | MA–ME survive. Untested branches: RC-5 (d) in `current()`; LS-4 "bound to other content"; RC-9 same slot, identity, sequence, prior and reviewed content; a line citing a *not completed* or later line (only 3 of WR-VC-20's reader negatives are exercised); RF-1 cleanup; G-1R "registered line changed". The schema negatives of WR-VC-20 are not exercised in the App | Add one test per branch. MB, MD and ME each need a single crafted ledger line or act record |
| F3 | MINOR | `workflow_library.rs:99–110` (`refine_from_store`) | RF-1 with V11 J5-2 ("no draft is left that can only be DS-3") | A failure in `publish_new` (part-way), `sync_package` or `sync_dir` returns early. It leaves a draft with no App-kept base, which reviews as DS-3, and D-1 forbids the App to overwrite it. Only a failure to record the base is cleaned up. Also, the second `Snapshot::capture` of the store (l. 99) is not compared with ‹k› after `standing_as_read`, so a store changed in between is copied while ‹k› is recorded as the base | Route every failure after `create_dir` through a cleanup that removes partial copies, using the prefix check `publish_reserved_store` already uses. Have `standing_as_read` return its snapshot and copy those bytes |
| F4 | MINOR | `workflow_library.rs:838–846` (`act_record_found`) | WR LS-4 causes ("A15 record missing or bound to other content"); G-1R "ledger unreadable → pending" | Any unreadable line anywhere in the library act log, even one unrelated to ‹k› (P3), or a transient read error, makes **every** revision LS-4: DS-8 is never offered. At G-1R it ends a captured re-confirmation *not completed*, so the person's act is spent on a read failure rather than a missing record | Separate "act log not readable" from "record not found / other content": at review show DS-4 with that cause (as now); at G-1R keep the attempt pending with the cause. Record the choice in CI-24 for the WR owner |
| F5 | MINOR | `App.tsx:280–281`; `runtime_session.rs` snapshot | WR §4.6 LS-1 note and §5.4 ("listed 'registered — re-confirm to use in this App session'"); change record App items (runtime_session listing text) | No listing of registered revisions exists. After a relaunch the UI never shows a revision's content identity, yet Refine requires the person to type it. The phrase appears only inside refusal text. CI-24 does not record this | Add the slot's registered revisions to the Root snapshot or library view, labelled as WR states, with a Refine action per row. Or log the gap in CI-24 |
| F6 | NOTE | CI-24 (f) | AAC §4.2 re-confirmation; owner decision 2026-10-08 | (f) names the statement but not the act button. A re-confirmation is still confirmed with "Register", and the three-button layout ([Don't ‹act›] [‹Act›] [Cancel]) must also cover it. Until J6 lands, no native witness should use J8 alone | Extend (f): the J6 integration supplies the re-confirm statement and the button label under the three-button layout |
| F7 | NOTE | `validation/J8_1a74f7f3/j8-mut*.log` | Evidence replayability | The logs name the mutations but do not contain their diffs | Keep each mutation diff with its log in future runs |
| F8 | NOTE | `workflow_library.rs:1399–1421` | — | X-2 lists the journal directory before it takes the lock. A process that waits on the lock while another closes the journal reports "X-2 pending: … No such file" | Read the directory after taking the lock, or treat NotFound as closed |

Not counted as defects, as briefed: the native statement and dialog wording
for a re-confirmation (J6). Verified: CI-24 (a), (c), (d), (e), (g), (h), (i)
and (j) are accurate. CI-21 (b) is closed with its history kept.

## Logs

Reviewer logs are in `$TMPDIR/v15-j8/logs/`
(`/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/v15-j8/logs/`), with
`SHA256SUMS`:

| File | sha256 |
|---|---|
| `01-npm-build.log` | `6c4e35d74efc1ae4f0f00ac617307bb3667f27beeb8667d7081318eef83457a7` |
| `02-cargo-test.log` | `28169ab7e807c9613e4bb49b5f137218fd9cdedfa70bc055e0edb6b65aa559e6` |
| `03-npm-test.log` | `48c9314ca1540f737269e1d8cf0efeefef852ea48ebe7c2d01a5053317c217f9` |
| `04-schema-sync.log` | `41fcd5fa95db8bc1d13cdd5d6c6770c91ca1bbbcb7647c6fbcc36a054b8ee6cc` |
| `mut-MA.log` … `mut-ME.log` | `4c31bfda…c604c151`, `d99acff0…f64103`, `1bd67769…a51`, `475627a1…16c5`, `e63a679b…eb3eed` |
| `mut-MF.log` … `mut-MI.log` | `a40ce500…d322`, `e363bbe1…07a`, `32f854b5…22e`, `9d1dce33…62a2` |
| `probes.log` | `efe3c83367a05b9ae482f3a5a45db9a262d615695ce88df2b65e7e23c1415816` |
| `v15-probe-tests.rs.txt` | `b2b461fbb130866bf9f187882b958960639eeb3794a0214b4689d3d8bd755179` |

## Limits

- No native act, UI launch or real second App process. "Second process" in
  P2 is a second `LibraryOwner` on the same root, which is how the tests
  model a relaunch.
- I did not merge J8 with J6, and I did not check the native statement.
- I did not rerun the implementer's mutations.
- The probes tamper with App-kept files where noted (P1, P3, P5). P2 uses
  only the existing test fault hook on a production code path.
- `$TMPDIR` is machine-local and may be cleared.

## Return

- Verdict: **NOT READY** (F1).
- Must do: F1. That means a pre-append RC-9 check, a G-1R check that the
  A15 is not already cited, tests for P1/P2/P5, a corrected CI-24 (b), and a
  CI item for the WR owner on the G-1R / RC-9 conflict.
- Should do with it: F2–F5. They can also be routed as CI entries.
- No owner question arises.
