# V14-R1: confirmation review of the J6 repairs

2026-10-08. Type 2 TASK reviewer for run `APP-V4-GROUP-A-20261004`, dispatched
by HELP_HUMAN (Claude Opus 5.5, Claude Code). Harness-native child, no
delegation. I did not write this code. The candidate worktree was read-only.
Builds, tests and mutations ran in `git archive 5a6af1cfa7` copies under
`$TMPDIR`. My only write is this file. No network, git fetch, credentials,
`~/.codex`, model call, UI launch, native act, commit or push.

**Verdict: READY** for merge.

- F1–F5, F7, F8 and F10 are repaired. The owner's three-button layout is
  implemented as decided.
- No path other than the middle button acts.
- The App route cannot cause a capture or send against content other than
  the content the host froze.
- The two new commands are read-only and widen nothing.
- One MINOR finding remains (R1-1): CI-22 (c) and the owner-decision effect
  assert that Escape never acts. This is not
  established, and it gates the native re-witness rather than the merge.
  Correct the wording in this PR or the next.
- F9 (natively witnessing the bound) stays open, as expected.

## Candidate

| Item | Value |
|---|---|
| HEAD | `5a6af1cfa7` "V14 repairs (F1-F5, F7, F8, F10) and the owner's three-button layout" |
| Parent | `e930ec06b8`, a merge of `0501d540b0` and the integration head `8868614f93` (including `007489e72b`, the CC-WR-RECONFIRM adoption) |
| Repair diff `e930ec06b8..5a6af1cfa7` | 11 files: `CONTRACT_ISSUES.md`, `package.json`, `a15_native.rs`, `act_control.rs`, `act_control_a15.rs`, `act_control_file.rs`, `file_act_native.rs`, `lib.rs`, `App.tsx`, `presentation.ts`, `presentation.test.mjs` |
| New basis | OWNER_DECISIONS "Native confirmation default key — 2026-10-08" (`81a18adea4`), read: three buttons [Don't ‹act› (default)] [‹Act›] [Cancel] for A15, A16 and request answers; file acts excluded as a recorded limit |
| HELP_HUMAN's retained logs | `validation/J6_5a6af1cf/`: `shasum -a 256 -c SHA256SUMS` reports every file OK |

## (3) Suite and my mutations

The briefed offline environment was used (`CARGO_HOME` group-a cache, the
pinned Codex binary and digest, `CARGO_NET_OFFLINE`), with `CARGO_TARGET_DIR`
in `$TMPDIR`.

| Part | Result |
|---|---|
| `npm install --offline`, `npm run build` | pass |
| `cargo test --offline --locked --no-fail-fast`, top level | **40 binaries, 698 passed, 0 failed, 3 ignored** (lib 384 + 2 ignored) |
| Nested `cargo test` invocations | **4, 4 passed** |
| `npm test` (now includes `presentation.test.mjs`) | 7 passed, 0 failed |

No known-flaky test failed in this run. 698 is my V14 count of 691 plus 7,
and the lib test count went from 377 to 384. No new warning points at a J6
line; the two in `act_control_a15.rs:212/221` predate J6.

I ran eight mutations of my own, each against the full lib suite and each
reverted. The restored tree is byte-identical to the archive (`diff -r`). All
eight were killed:

| Mutation | Killed by |
|---|---|
| R1: act label in the default slot (`act_buttons` order `act, dont, Cancel`) | `act_buttons_only_the_middle_slot_acts`, `native_adapter_three_buttons_only_the_middle_captures`, `reconfirmation_descriptor_has_its_own_statement_and_act_label` |
| R2: drop the compose-time review digest refusal | `review_with_a_non_integer_number_is_refused_at_review_time_with_its_location` |
| R3: logout shows counts only (`listed` empty) | `logout_lists_every_item_or_names_the_whole_assessment_by_digest` |
| R4: App content never withdrawn (no `retain` in `Drop`) | `shown_in_app_only_while_the_alert_is_open`, `native_adapter_three_buttons…` |
| R5: `refusal_or` reports the person's cancel | `refusal_is_reported_as_refusal_not_as_the_persons_cancel` |
| R6: re-confirmation variant always "Register" | `reconfirmation_descriptor_has_its_own_statement_and_act_label` |
| R7: the App shows other content than the content digested | `logout_lists…`, `operational_dialogs_are_readable_and_route_overflow_to_the_app`, `a16_statement_is_bounded…` |
| R8: file-act bound moved after the freeze and `Presented` | `over_long_file_act_statement_is_refused_before_it_is_shown` |

## (1) Status of each finding

| V14 | Status | Evidence |
|---|---|---|
| F1 logout listing | **Repaired** | `act_control.rs:349–390` lists one line per live turn, outstanding request, active child, unknown-activity child and unresolved turn observation. `logout_statement` (l. 391–440) uses `whole_or_in_app`: the whole list when it fits; otherwise counts plus the sha-256 of the frozen assessment, with that assessment shown in the App while the alert is open. Test `logout_lists_every_item…`; R3 and R7 killed. The overflow route depends on the App window staying readable while the parentless alert is open, which is a native re-witness item |
| F2 non-integers | **Repaired** | `content_digest` (`act_control.rs:556–567`) refuses with a JSON Pointer and the "integers only" cause. `compose_a15` refuses at review time (`act_control_a15.rs:430`). The misleading "offer is not offered" text is gone (tested). Integers above 2^53 are digested exactly by the host (tested) and reported through `workflow_review_digest` (`lib.rs:642`). The webview declines to recompute them and says why (`presentation.ts`; node test) |
| F3 file acts | **Repaired** | `act_control_file.rs:226–246`: readable lines (no `{` or `"`, tested), and `bounded` runs before the actor and context freeze and `Presented`. The refused offer stays Composed and unfrozen (tested; R8 killed). The 24000-byte check and the late bound in `file_act_native.rs` are removed |
| F4 refusal shown as cancel | **Repaired** | `confirm_bounded` stores the cause (`lib.rs:630–635`); logout, sign-in cancel and attachment source return `refusal_or(refused, result)` = `Err(cause)` (`lib.rs:213, 239, 504`). Unit-tested (R5 killed). The Tauri glue is checked by reading only |
| F5 impossible long operations | **Repaired** | A16 (`confirmation_statement`), request answers (l. 492) and attachment comparisons (l. 457) use `whole_or_in_app`. The test confirms a 40-consequence A16 end to end and binds the frozen offer digest; a 4500-character answer and deep paths are routed to the App. The remaining hard refusals are listed honestly in CI-22 (b): A15 entry identities, fixed parts over the bound, sign-in cancel and file acts |
| F6 default button | **Implemented per owner decision** | `act_buttons` = `YesNoCancelCustom(dont, act, "Cancel")` (`act_control.rs:516`). Used by A15 (`a15_native.rs:94–95`, `chose(&result, variant.act)`), A16 (`lib.rs:855–865`, `chose(…, DECIDE)`) and request answers (`lib.rs:598–608`, `chose(…, SEND_ANSWER)`), all through `blocking_show_with_result`. `dialog_model::outcomes` matches my V14 reading of the plugin and rfd: default is slot 1, aborts go to the third label. The A15 adapter test drives every modelled ending plus `Cancel/Ok/Yes/No/"register"`, and only "middle" captures. File acts, logout, sign-in cancel and attachment source keep Return as the act; this is recorded in CI-22 (c). Escape: see R1-1 |
| F7 re-confirmation | **Repaired** | `a15_variant` (`act_control_a15.rs:313–321`) selects on `descriptor_kind == "a15_descriptor"` and `disposition == "re-confirmation"`. It gives the adopted AAC §4.2 sentence and [Don't re-confirm] [Re-confirm] [Cancel] (l. 400–412; R6 killed). The test uses a synthetic descriptor. J8 at `1a74f7f307` composes a draft `a15_descriptor` with the same literal `"re-confirmation"` on the descriptor (`workflow_library.rs:292`, J8 test l. 877), so the selector will match it after merge. V15 should confirm the full J8 descriptor |
| F8 webview trust | **Repaired** | `DIGEST_LIMIT` (`presentation.ts:141`) appears beside every digest (the review digest line and `NativeConfirmationContent`), and CI-22 (f) states the limit. The App also compares the host digest with its own and warns on a mismatch |
| F9 native bound | **Open (expected)** | Native re-witness |
| F10 pending record | **Repaired** | `presentation.ts:177`; node test |

## (2) New code

- **Only the middle button acts.** I checked every `blocking_show*` site:
  - A15, A16 and request answers act only on `Custom(act label)` from slot 2.
  - File acts are unchanged: `Custom(wording)` acts and `Custom("Decline this act")` declines.
  - `confirm_bounded` (logout, sign-in cancel, attachment) uses `blocking_show()`. For `OkCancel` and `OkCancelCustom` that is true only for `Ok` or `Custom(ok label)`.
  - Sign-in start, the API-key home and the counterpart prompt are fixed text and unchanged.
  - The synthetic adapters remain `#[cfg(test)]`.
- **The App route cannot change what is bound.** The content the App shows
  comes from the host-side static `SHOWN`. It is filled by `showing_in_app`
  from the very `Value` the host digested, and withdrawn on return or unwind
  (tested; R4 and R7 killed). The webview can neither write nor replace it.
  Each operation's binding is still host-side and unchanged:
  - A15: frozen review equality plus the named digest (`act_control_a15.rs:576`).
  - A16: the frozen offer and its digest (the `confirm` test checks `offerDigest`); the App content is built from the same `o` that is frozen.
  - Logout: the frozen assessment and the `material` recheck.
  - Request answer: the same `answer` argument previewed and sent, plus the context recheck.
  - Attachment: the owner and revision recheck.

  A compromised webview could still *display* other bytes. That is a reading
  limit, stated in F8, not a capture path.
- **The read-only commands widen nothing.**
  - `native_confirmation_content` (`lib.rs:638`) takes no arguments. It returns only content an open host confirmation published, and it touches only the `SHOWN` mutex.
  - `workflow_review_digest` (`lib.rs:642`) hashes an existing review's `status.presentation`, which the App already receives. It takes `workflows` briefly and `try_lock`s the review, so it reports "held by an open native confirmation" and never blocks the dialog path.
  - Neither command mutates state, and like every App command neither is reachable from Codex or its tools (NA-1).
  - `NativeConfirmationContent` polls once a second. That is cheap, and it needs the main thread to be free while the parentless alert is open, which it is: rfd shows `CFUserNotification` from a spawned thread.
- **CI-22 honesty.** It says plainly that the A16 App route and the button
  layout "go beyond the committed §4.1a and §6.2 text", and that the adoption
  text is "not applied to the Design". It also says the re-confirmation
  statement is tested only with a synthetic descriptor. Two overclaims
  remain (R1-1).

## Findings

| ID | Severity | Where | Evidence | Consequence / action |
|---|---|---|---|---|
| R1-1 | MINOR | `CONTRACT_ISSUES.md` CI-22 (c) ("every candidate records nothing"); the OWNER_DECISIONS effect line "Return and Escape never act". The code comments (`a15_native.rs:42–47`, `act_control.rs:509–515`) claim only Return and abort, which is correct | Which button Escape triggers in a parentless `CFUserNotificationDisplayAlert` is not observed. The act now sits in the **alternate** slot, the one that held "Cancel" in the old two-button layout. If the notification panel gives Escape to the alternate button rather than to the button titled "Cancel" or the cancel response, Escape would act, which is a regression from J6's first layout. CI-22's "a request answer of any length can be confirmed" also overstates: over-long content holding a non-integer number is refused, correctly, with its location | Reword to "Escape: not yet observed; must be witnessed before reliance". Make the Escape press a **gating** step of the native re-witness, before any person uses the build for an act. If Escape reaches the middle slot, revisit the layout (for example the owner's custom NSAlert option). Qualify the "any length" sentence |
| R1-2 | NOTE | `act_control.rs:391–440` | A logout assessment too long to list *and* holding a non-integer would be refused, so logout would be impossible, with the cause reported (F4). I saw no float in the assessment fields | None now. Watch it in the re-witness |
| R1-3 | NOTE | — | Native-only items stay open: whether the App window is live and readable while the alert is open (the F1/F5 route depends on it); Escape (R1-1); Return → "Don't ‹act›"; whether 30 lines and 1500 characters fit; digest wrapping and copy | Re-witness |

## (4) J8 overlap (informational)

`git merge-tree --write-tree 5a6af1cfa7 1a74f7f307` (merge base `007489e72b`):

- `CONTRACT_ISSUES.md` auto-merges.
- **`lib.rs` conflicts** in the `generate_handler!` list: J6 adds `workflow_review_digest` and `native_confirmation_content`; J8 adds `workflow_refine_registered`. Resolve by taking both.
- **`App.tsx` conflicts** in the review `<article>`: J6 adds the digest line and `readablePaths`; J8 adds a re-confirmation note and disposition-dependent button text. Resolve by taking both.
- `runtime_session.rs` is J8-only and does not conflict.

After merging, rerun `reconfirmation_descriptor…` together with J8's journey
test, to confirm that the real descriptor selects the re-confirmation
variant.
