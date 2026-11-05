# Renderer check of the Make guide's trials, bring-back and review, 2026-11-04

Standing: automated renderer observations of App-side behaviour. They are not
owner or human acceptance, not native J1/J2 passes, and not model, sign-in,
native window or production qualification. The holds observed last only as long
as the App window; they are not deduplication by the host, across windows or
after a relaunch.

## Subject

- **Merged result:** PR #119, merged to main as `f96e4252`.
  - Its whole tree (`6180f652…`) is identical to the head integrated from,
    `9a0c73c9`.
  - That head contains `114365c1` plus the merged main #123. The #123 additions
    were source-reviewed and tested separately. They were not rendered again
    here.
- **Render subjects:** each keeps its own identity.
  - `dd47ee35`: first after-pass.
  - `f280a050`: repairs.
  - `03f4d2d1`: hold, source and identity repairs.
  - `5f87a444`: a missing result.
  - `114365c1`: display.
- **Baseline:** the #117 source `9248a36e`, where the guide had no trial or
  bring-back region.
- **Builds:** each build is an offline `npm run build` of an immutable
  `git archive` export. The lock file and `package.json` were unchanged
  throughout.

## Method

- **Renderer:** cached headless Chromium, driven over CDP from a 127.0.0.1
  server, at desktop (1100×800) and narrow (480×860) widths.
- **Real inputs:**
  - the host status and draft row from the frontend's executed Rust producers
    (packet sha256 `6d292510…`);
  - the review from the executed
    `library_entries_real_observation_ordered_subset_to_existing_review_packet`
    DTO;
  - the Rust strings:
    - `trial_native_source`;
    - `bring_back_send` kept / `not_kept`;
    - `workflow_register_native` dismissed / unavailable / duplicate.
- **Synthetic, and labelled in each report:**
  - **Trial rows and pending bring-backs:** shaped like `trials_for_draft`,
    `trial_rows` and `pendingBringBacks`:
    - newest first;
    - bare `trialConversation` and `broughtBack[].to`;
    - a hot `authoringConversation` tuple only while `authoringSourceLimit` is
      null.
  - **The review:** the DTO's `entries[0].identity.name`, `library`,
    `source_root` and `origin` are substituted with the draft and the active
    library row.
  - **Outcomes and changes of state:**
    - send outcomes: unknown, observation not written, `null`, refusal;
    - restart and home change keeping the same ID;
    - a library switch;
    - a run bring-back;
    - two copies of a prepared message.
  - **Draft state after an A15 act:** no change of draft state is assumed.
- **Not run in a browser:** the other retained-callback variants. The
  frontend's mounted tests cover them.

## Observed

| Head | Result |
|---|---|
| `9248a36e` (baseline) | **Trials:** the guide had no trial region. Trials, bring-back and Open could be reached only from the studio's draft list and its prepared-message control. |
| `dd47ee35` | **Working:**<ul><li>Rows keep the host order, and bare, hot-unloaded and null conversation references get truthful labels.</li><li>A same-name result from another library is hidden.</li><li>Holds apply while a trial is live, has a source limit, is cold, or no conversation is chosen.</li><li>`workflow_trial_bring_back` gets its exact arguments, and Open sends nothing.</li></ul>**Defects:**<ul><li>An unknown send could be repeated blindly. The host withdrew the pre-fill, the composer's outcome vanished, the only notice was a prefixed panel alert off-screen, and the guide still offered Bring.</li><li>Pressing Bring twice made duplicate pre-fills.</li><li>Focus dropped to `body` after Bring and after Open.</li><li>The top "Next" line was stale.</li><li>After a dismissed or unavailable A15, the review guidance didn't match the controls.</li></ul> |
| `f280a050` | **Working:**<ul><li>Focus goes to the results control after Bring, and to the composer textarea after Open.</li><li>An unconfirmed send gives a focused notice in the conversation and holds Bring in the guide and the studio.</li><li>Captured callbacks issue no IPC, and the acknowledgement issues no IPC.</li><li>"Next" is truthful, and the review wording is right.</li></ul>**Defects:**<ul><li>A successful send to another conversation released the hold.</li><li>The studio's pending check read `destination` instead of `target`.</li><li>A run doubt had no acknowledgement.</li><li>Guidance from the old library's review followed the draft into another library.</li><li>A generation change lifted the hold for the same thread ID.</li></ul> |
| `03f4d2d1` | **All five repaired:**<ul><li>No count or record releases a hold.</li><li>The studio reads `target`.</li><li>A run doubt can be acknowledged with no IPC.</li><li>A review is matched by library identity.</li><li>A same-home restart or home change keeps the same-ID hold, while a different conversation stays allowed.</li></ul>**Dispatch guards:** a retained Send of a withdrawn message, a second copy, a double Send or Bring, and a retained Bring after publication issue no further IPC.<br>**Defect:** a `null` result with the pre-fill still listed showed "Transcript sent". |
| `5f87a444` | **Null result with the pre-fill still listed:** it reads "Not confirmed… may or may not have been sent", with no success words. The text is kept, and a captured or repeated Send issues no IPC. |
| `114365c1` | **Notice wording:** it says the message is still listed while it is, and withdrawn once it's gone. "Reported: The host did not report the send's outcome." was read in the expanded details.<br>**Send controls:** the held copy's Send is visibly disabled with its reason, and stays disabled after the acknowledgement (no IPC). A second copy is held until the acknowledgement. |

## Not established

- **Residual, later repaired:** the "ready to send" label for the held copy was
  open when #119 was integrated (main `f96e4252`). It was repaired by #124:
  rendered at `f1a76e98` and `824e60f3`, and merged as main `2d584803`. See
  `RENDERER_RUN_GUIDE_LABELS_20261104.md`. It was never waived.
- **Not rendered:** a later guard on `runReading` belongs to #125 and was tested
  only in its source.
- Any real Codex turn, model, native A15 dialog or window behaviour.
- Owner or human use, and J1/J2 completion.

Evidence (task scratch `app-p2-trial-u5RbDlpZ`): `out-j2-base`,
`out-j2-119` … `out-j2-119i` (reports and screenshots), plus the synthetic peer
`mock-j2.js` and the driver `j2drive.mjs`.
