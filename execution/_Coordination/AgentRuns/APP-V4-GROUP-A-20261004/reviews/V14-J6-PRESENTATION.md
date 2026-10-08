# V14 — independent code review of J6 (readable native confirmations, D-1/D-2/D-3)

2026-10-08. Type 2 TASK reviewer for run `APP-V4-GROUP-A-20261004`, dispatched
by HELP_HUMAN (Claude Opus 5.5, Claude Code). Harness-native child, no
delegation. I did not write this code. The candidate worktree was read-only
for me. All builds, tests, mutations and probes ran in `git archive` copies
under `$TMPDIR`. My only write is this file. No commit, network, credentials,
`~/.codex`, model call, UI launch or native act.

**Verdict: NOT READY.** The D-1 repair itself is sound. It is faithful to the
committed AAC, every capture binding is kept, the new named-digest check
holds, the Rust and TypeScript digests agree, and the tests kill every
mutation I tried. One MAJOR finding blocks merge: the logout confirmation no
longer lists live work before the person decides (F1). This narrows a
DEL-01-05 Design requirement without a contract-issue entry. The repair is
small: restore the listing within the bound, or log the deviation as a
contract issue and route it. F2–F5 are MINOR and can be repaired together
with F1 or routed.

## Candidate and basis

| Item | Value | How checked |
|---|---|---|
| Candidate | `claude/app-v4-j6-presentation` at `0501d540b0`; parent `84f90438d1` (control test only, 57 lines in `act_control_a15.rs`); its parent `b9a818d580` | `git log`, `git show --stat`; worktree clean |
| Files changed `b9a818d580..0501d540b0` | 9: `CONTRACT_ISSUES.md`, `a15_native.rs`, `act_control.rs`, `act_control_a15.rs`, `file_act_native.rs`, `lib.rs`, `App.tsx`, new `src/presentation.ts`, new `tests/presentation.test.mjs` | `git diff --stat`. Nothing else was touched |
| AAC basis | `git show b9a818d580:…/APP_ACT_CONTROL.md`, sha256 `098875a39b33543a…`. Read §0, §1, §2, §3, §4.1, §4.1a, §4.2, §5.1 (offer digest), §5.2, §6, §8 | as stated |
| `OWNER_DECISIONS.md` at `b9a818d580` | `7fa0723b0576dee8…`. "Native-confirmation implementation allocation" (l. 41–43) read | as stated |
| Witness | `probes/NATIVE_JOURNEY_WITNESS_1113.md` `33e916eb98fb7e91…`. D-1…D-7 read | as stated |
| Also read | `AGENTS.md` `f96feb19…`, `agents/AGENT_TASK.md` `1a13a5b0…`, `loop/LOOP_INIT.md` `c2e88f81…`; WR at `b9a818d580` §4.6–§4.7; WR at `007489e72b` DS-8, RC-1…RC-5; DEL-01-05 `ACCOUNT_AND_PROVIDER_ACCESS.md` Q-5, AE-12, KE-13; NIR "confirm" passages | as stated |
| Dependency sources | `tauri-plugin-dialog-2.7.2/src/{lib.rs,desktop.rs,models.rs}`; `rfd-0.16.0/src/backend/macos/{message_dialog.rs,utils.rs,utils/user_alert.rs}`, `gtk3/message_dialog.rs`, `win_cid/message_dialog.rs` | read from `~/Library/Caches/chirality-dev/cargo-home-group-a/registry/src/` |

The CC-WR-RECONFIRM adoption is now committed in the HELP_HUMAN checkout as
`007489e72b`. I reviewed J6 against the AAC at `b9a818d580`, as briefed, and
checked the interaction separately (F7).

## Suite (Q7)

Command as briefed, in `$TMPDIR/v14` (a `git archive 0501d540b0` of the whole
`projects/chirality-app-v4`), with `CARGO_TARGET_DIR` in `$TMPDIR`.

| Part | Result |
|---|---|
| `npm install` (offline), `npm run build` (`tsc --noEmit && vite build`) | pass |
| `cargo test --offline --locked --no-fail-fast`, top level | **40 binaries, 691 passed, 0 failed, 3 ignored** (lib 377 + 2 ignored; one ignored in `native_backend_smoke`) |
| Nested `cargo test` invocations inside lib tests | **4 invocations, 4 passed** |
| `npm test` | 3 passed, 0 failed |
| `node --test tests/presentation.test.mjs` | 3 passed, 0 failed |

The author's "44 binaries, 695 passed, 0 failed, 3 ignored" is these two rows
added together (40 + 4 binaries, 691 + 4 passed). Against HELP_HUMAN's
baseline of 677 top-level plus 4 nested, the top level grows by 14. That
equals the 14 new `#[test]` functions in the diff: 5 in `native_statement`,
1 A16 test, 6 in `act_control_a15.rs` (the control among them) and 2 in
`file_act_native.rs`. The counts were derived from the log by a script: in
each binary block, the last `test result` line is the binary's own and
earlier lines are nested. No new compiler warning points at a J6 line.

**Merged with the adoption.** `git merge-tree 007489e72b 0501d540b0`
conflicts only in `CONTRACT_ISSUES.md`: both sides append, CI-23 on main and
CI-22 here. The code merges cleanly. The full suite on the merged tree gives
the same counts (691 + 4, 0 failed) and the node tests pass.

## Q1 — Faithfulness to the AAC

**It is faithful. It is not a contract change, and CI-22 is a clarification,
not a prerequisite.**

- §6.2 P-2 (committed text) lists what the native confirmation shows: "the
  act wording, subject and its identity, scope, purpose, the arrival or
  'standing act', and the buttons". The J6 statement shows each of these. I
  printed a realistic single-draft statement: 20 lines and 1220 characters
  with a 106-character library path. It has the wording, each entry's name,
  origin, disposition, method, short revision and full revision on its own
  line, the prior revision, library and scope, purpose, the standing, the
  actor and its limit, the consequence, and what Register and Cancel do.
- §4.2 step 1 puts the review package with DEL-02-02 ("shows the review
  package"). §6.2 allows the offer in the webview "for reading; only the
  native confirmation captures". No committed text requires the review
  itself in the native surface.
- The owner's allocation asks for "full immutable selected act
  statement/consequences". The statement is composed only from the frozen
  offer and binding, and it is shown whole or refused. The review is the
  subject's content, not the act statement. The witness itself named this
  repair: "a readable statement with reachable controls, with the full review
  available separately".
- What the statement leaves out of the offer is not in P-2's list: the
  descriptor ID and kind, each entry's ID-3 string (a "reviewed draft" marker
  stands for it), `composedAt`, and the offer digest beyond 12 characters.
  The offer ID is shown whole.
- CI-22 is worth adopting because "full" in the owner's wording could be read
  as covering the review. Route it to the AAC owner, without holding J6.

## Q2 — Binding

**No binding weakened, and one was added.**

- `confirm_a15_after_native_event` keeps every prior check (`act_control_a15.rs:500–531`):
  Presented state; full `BoundReview::matches`, which already includes
  `presentation ==` (l. 200–209); offer ID; offer digest, both stored and
  recomputed; frozen actor; and owning context. The named-digest check
  (l. 520) comes after them. It is redundant with `presentation ==` today,
  but harmless and correct.
- The statement, the frozen digest and the actor/context freeze are composed
  from the frozen binding after `matches(&now)`. They are frozen only after
  `bounded` succeeds (l. 456–467).
- The production event is still built only in `confirm_native` with a real
  `blocking_show_with_result`. `synthetic_a15_native` is `#[cfg(test)]`.
- **Canonicalization (Rust `canonical.rs` against TS `canonicalJson`).** The
  two agree on key order (both use code points: Rust by byte order, TS by an
  explicit code-point compare), separators, the escape set (`\b \t \n \f \r`,
  other code points below U+0020 as `\u00xx`, everything else literal,
  including U+007F, U+2028 and non-ASCII), and literals. Numbers differ only
  outside the shared domain, and both fail closed there. Rust refuses every
  non-integer. TS refuses non-safe integers. A float with an integral value,
  such as `1.0`, is refused by Rust before anything is shown. An integer
  above 2^53 is digested by Rust, but the App shows "unavailable" (F2).
  Strings cannot carry lone surrogates on either side. Evidence:
  - The shared vector `f0320f0c…` was recomputed independently in Python,
    written from AAC §5.1's text.
  - A 3001-value random corpus was hashed by TS (`reviewDigest`) and by a
    temporary Rust probe (`review_digest`). Both gave 0 mismatches against
    Python. The corpus covers astral, BMP-max and control-character keys and
    strings, U+2028/2029, BOM, and integers up to ±(2^53−1).
- **Mutations** were run against the full lib suite, and each was reverted;
  the restored tree was byte-identical (`diff -r`). All were killed:

| Mutation | Killed by |
|---|---|
| Drop the named-digest check | `capture_still_requires_the_frozen_offer_and_the_named_review_digest` |
| `chose`: any `Custom` or `Ok` captures | `native_adapter_only_explicit_register_captures…`, `actor_line_and_choice` |
| `chose`: `Ok` also captures | the same two |
| `chose`: case-insensitive label | `native_adapter_only_explicit_register_captures…` |
| A15 unbounded | `over_long_statement_is_refused_before_presentation_with_its_cause` |
| A16 unbounded | `a16_statement_is_bounded_and_an_over_long_one_is_refused…` |
| A16 freezes the selection before the bound | the same |
| File act unbounded | `over_long_file_act_statement_is_refused_before_it_is_shown` |
| Swap A15 button slots | `native_adapter_only_explicit_register_captures…` |
| Bound lines off by one | `bound_refuses_with_cause_and_never_truncates` |
| Bound counts bytes, not characters | the same |
| Statement shows only a short review digest | `control_a15_native_statement_is_bounded_and_names_every_binding` |
| Cancel path skips `dismiss_a15` | `native_adapter_only_explicit_register_captures…` |
| TS: UTF-16 key sort; escape U+2028; first, not latest, check; allow floats; drop `\xNN`; drop control escapes | `presentation.test.mjs` (6/6 killed) |

## Q3 — Bounds on every native path

Every `blocking_show*` call site was checked (`grep` in `src-tauri/src`).

| Site | Dynamic text? | Bounded before showing | Nothing frozen, captured or sent on refusal |
|---|---|---|---|
| A15 `a15_native.rs:70–75` | yes | yes (`act_control_a15.rs:460`) | yes; offer stays Composed (tested) |
| A16 `lib.rs:831–839` | yes | yes (`act_control.rs:695`, before `selected`/frozen) | yes (tested) |
| File acts `file_act_native.rs:56–65` | yes | yes, but after `freeze_file_native` | nothing captured; offer **frozen, then dismissed** (F3) |
| Logout `lib.rs:211` | yes | yes (`confirm_bounded`) | nothing sent; reported as the person's cancel (F4) |
| Sign-in cancel `lib.rs:235` | yes | yes | as logout (F4) |
| Attachment source `lib.rs:496` | yes | yes | as logout (F4) |
| Request answer `lib.rs:591` | yes | yes (`?` returns the cause to the App) | nothing sent |
| Sign-in start `lib.rs:220`, API-key home `lib.rs:243`, counterpart `lib.rs:541` | fixed short text | not needed | — |
| File pickers (`blocking_pick_*`) | — | not applicable | — |

## Q4 — The default-button hazard (CI-22 (c))

**J6's analysis is correct.** With no `.parent(...)`, as here, rfd 0.16 on
macOS does not use `NSAlert`. It uses `CFUserNotificationDisplayAlert`
(`user_alert.rs`, `async_pop_dialog`), which runs off the main thread and
outside the App window. Slot 1 is the default button (Return), slot 2 the
alternate and slot 3 the other.

rfd returns `Cancel` in four cases: the display call fails (`is_cancel != 0`),
the alert is cancelled (`kCFUserNotificationCancelResponse`), the response is
not matched (`_ =>`), or the result channel is dropped. The plugin
(`desktop.rs:236–251`) maps rfd `Cancel` to the **cancel-slot label**: the
second label of `OkCancelCustom`, the third of `YesNoCancelCustom`.
`OkCancelCustom("Cancel", "Register")` would therefore register on a failed
or aborted alert. Windows and GTK end the same way: Escape or close gives
`IDCANCEL` or `DELETE_EVENT`, then rfd `Cancel`, then the cancel-slot label.
rfd exposes no key-equivalent or default-button control. A `.parent` would
switch to an `NSAlert` sheet, whose first button is still the default and
which blocks the App window while open.

Options within existing dependencies:

1. **Three-slot layout (recommended, small).**
   `YesNoCancelCustom("Don't register", "Register", "Cancel")`:
   - Return activates slot 1, which does not capture.
   - Register is only `Custom("Register")`. That comes from the alternate
     response on macOS (`kCFUserNotificationAlternateResponse`), `ID_CUSTOM_NO`
     on Windows, and `GTK_RESPONSE_NO` mapped to `Custom(no)` on GTK.
   - Every abort or failure maps to slot 3, "Cancel", which does not capture.
   - Change `a15_buttons` and its test (assert `Register` is in slot 2 and
     neither slot 1 nor slot 3 is `Register`). `chose(…, REGISTER)` is
     unchanged.
   - Give slots 1 and 3 distinct labels. Which key Escape triggers in a
     CFUserNotification must be witnessed natively; every candidate is
     non-capturing.
   - The same layout fits A16 (`Decide` in slot 2) and the request answer
     (`Send answer` in slot 2).
   - It does **not** fit file acts, which use all three slots (act, decline,
     cancel). Moving decline to slot 3 would make an aborted alert record a
     **decline**. For file acts, keep the current layout, or make Return
     safe with option 3.
2. **Keep the current layout** (J6 as is). Return still registers, but the
   statement is now readable and the buttons are on screen. This removes
   D-1's root cause, the unreadable alert. It does not remove the risk of a
   habitual Return. This is the owner's call under CI-22 (c).
3. **A custom `NSAlert` through `objc2-app-kit`**, which is already in the
   lockfile through rfd. Set Register's key equivalent to "" and Cancel's to
   "\r", or leave no default. Optionally add an `accessoryView` holding a
   scrollable `NSTextView`, so even the complete review could be shown with
   the buttons always visible. This removes the hazard on every act kind.
   The cost: `unsafe` Objective-C on the main thread, a direct dependency
   edit (the Cargo.lock root entry changes), and a possible need for
   objc2-app-kit features whose optional crates may not be in the offline
   cache. Check that with `cargo tree -e features` before choosing it.
   Larger and macOS-only.
4. **Rejected:** `OkCancelCustom("Cancel", "Register")`, which registers on
   abort (as J6 says). A preliminary "I have read the review" step in the
   webview is not authoritative (NA-3).

The same hazard exists today on A16 (`Decide`), file acts (the act wording),
request answers (`Send answer`), attachment source (`Use current source`) and
logout (`OK`). CI-22 (c) names only A15.

## Q5 — D-2 and D-3

- **D-2** (`presentation.ts:137`, `App.tsx:321`). `run.checks` is appended in
  order (`runtime_session.rs:5010`), so the last check is the latest. Before
  any check, the summary keeps `status.supplied`. This is correct and
  display-only. It drops the row's "check record pending" qualifier
  (F10, NOTE).
- **D-3** (`presentation.ts:12–79`; `act_control.rs` `native_path_text`,
  `escape_invalid`). This is display-only. Every action argument still comes
  from the original values (`review.reference`, `entry.identity.revision`,
  `row.selection.selectionRef`), and the test checks that the input is not
  mutated. Valid UTF-8/UTF-16 is shown as text. Otherwise an explicit marker
  is shown, with each invalid byte as `\xNN` (or each unpaired unit as
  `\u{NNNN}`). I traced Rust (`error_len`) and TS (lead-width resync) by hand
  on truncated, overlong, surrogate, >U+10FFFF and interleaved cases, and
  they produce the same text. A literal `\xNN` in a valid path is ambiguous
  with an escape only after the marker. This is display-only (NOTE).

## Q6 — Test strength and collateral

The tests are meaningful: every mutation above is killed, and the control
commit was red before the repair (the author reports 128 lines and 5394
characters; I did not rerun the base).

There is no test of `lib.rs`'s `confirm_bounded`, its refusal branch, or the
logout, sign-in-cancel and attachment wiring. These are Tauri command glue.
Its behaviour is F4.

The `lib.rs` dialog changes are safe for act capture:
- `confirm_bounded` uses `blocking_show()`. For `OkCancelCustom` that returns
  true only for `Custom(ok_label)` (plugin `lib.rs:323–339`).
- The kind `Info` equals the plugin default for logout and sign-in cancel.

No file outside the nine was touched.

## Findings

| ID | Severity | Where | Evidence | Consequence / repair |
|---|---|---|---|---|
| F1 | **MAJOR** | `act_control.rs:343–385` (`logout_statement`); `lib.rs:211`; `runtime_session.rs:2531–2554` | DEL-01-05 AE-12, KE-13 and Q-5: sign-out and key removal "asks first … listing its live turns, outstanding requests and active delegated children … all three are listed". Before J6 the native alert printed the whole frozen assessment. J6 shows only **counts** and says the assessment "is returned to the App with the result", which is after the decision. The App shows no assessment before `logout_home` (`App.tsx:362`). CI-22 and the commit message do not record this narrowing | The person decides on a credential-removing act without seeing which turns, requests or children are live. This undisclosed Design deviation breaks LOOP_INIT change control. Repair: (a) list each item on one short line (thread/turn, request method and ID, child), refusing with the cause above the bound. Refusal blocks logout when there is much live work, so state that; or (b) show the frozen assessment in the App first and name it in the native summary by digest, as A15 does; or (c) log a CI for DEL-01-05 and route it before merge |
| F2 | MINOR | `act_control_a15.rs:294–300, 459`; `presentation.ts:109–115` | A temporary probe: a draft whose `workflow-declaration` block holds `{"x": 1.5}` is preserved in `presentation.entries[0].declaration.raw`. `compose_a15` succeeds, then `a15_confirmation_text` fails with "A15 complete review digest unavailable (non-integer number: the offer is not offered); nothing presented or captured". Before J6 this review was presentable | This new refusal is not in CI-22. The text names "the offer", which is wrong (it is the review), and does not say where the number is. Integers above 2^53 work in Rust but the App shows "unavailable", so the person cannot compare. Repair: refuse at review time with a locating cause, or keep non-canonical values out of the digested presentation (for example the raw declaration as its source text). Record it in CI-22 |
| F3 | MINOR | `file_act_native.rs:76–87`; `act_control_file.rs:226–236` | The bound runs after `freeze_file_native` has set `Presented` and frozen actor and context. On refusal the offer is `Dismissed` without being shown. A15 and A16 stay Composed and unfrozen. The file-act text still embeds raw JSON: subject ref, `contentIdentity` object and the whole actor. The old 24000-byte check is now dead | This is inconsistent with "nothing frozen" and leaves an AC-5 transition from an unpresented offer. The file-act statement is not "readable" as the commit says. Repair: apply `bounded` inside `freeze_file_native` before the state change, and render lines as A16 does |
| F4 | MINOR | `lib.rs:618–622` | `confirm_bounded` shows the cause in a native OK alert and returns `false`. The callers then report the person's choice: "native confirmation cancelled; no logout request", "…dismissed; original pending control retained", "confirmation-cancelled" | A host refusal is recorded to the App as a person's cancel. Nothing is sent, so this is safe, but the result is misattributed. Repair: return `Err(cause)`, as the request-answer path does |
| F5 | MINOR | `act_control.rs:431–439`, `412–427`, `695` | The bound makes some operations impossible: a request answer (free text) longer than about 1350 characters can never be sent; an A16 whose chosen consequences exceed it can never be decided; an attachment re-confirmation with two deep paths can never be confirmed. NIR sets no answer length limit. CI-22 (b) mentions refusal for "every kind" generically | Each is a functional limit with no alternative path. For the request answer, consider the A15 pattern (full preview in the App, named by digest). At minimum, list these consequences in CI-22 for the owners of NIR, AAC §4.1a and attachments |
| F6 | NOTE | `a15_native.rs:42–51`; CI-22 (c) | Verified (Q4). Return still registers | Owner decision. Options in Q4. The hazard is wider than A15 |
| F7 | NOTE | `act_control_a15.rs:378`, `a15_native.rs:41` | AAC at `007489e72b` (CC-WR-RECONFIRM) requires, for disposition *re-confirmation*, "Re-confirm revision ‹k› of ‹origin›:‹name› for use in this App session. This registers no new revision." J6 hard-codes "Registering makes these reviewed bytes available in this library; earlier revisions are kept" and the button "Register" | The re-confirmation implementation must branch the consequence line, and preferably the act label (`chose` compares a constant), on disposition, and keep it within the bound. The merge with `007489e72b` is clean apart from the `CONTRACT_ISSUES.md` append conflict, and tests pass there |
| F8 | NOTE | `App.tsx:272–304` | The App computes the digest in the webview it is supposed to check. A compromised webview could show other bytes beside the true digest. Capture binding is host-side and unaffected | Add this limit to the App text or CI-22 (NA-6: state limits) |
| F9 | NOTE | `act_control.rs:171–176` | 30 lines / 1500 characters is not natively witnessed. CFUserNotification wraps 64-hex lines. A realistic single draft is 20 lines / 1220 characters | Native re-witness, as J6 says. Include an Escape press (still unwitnessed per the witness "Limits") |
| F10 | NOTE | `presentation.ts:137–145` | The summary drops "check record pending" | Optional: append the publication state |

## Return

- Verdict: **NOT READY** (F1).
- Must do: repair or record F1. Should do with it: F2–F5.
- Owner question to carry: CI-22 (c), the default button. Option 1 is the
  small safe change for A15, A16 and request answers.
- CI-22's AAC §6.2 wording is a reasonable clarification for the AAC owner;
  it does not gate J6.
