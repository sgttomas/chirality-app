# Renderer check of the Run guide labels and the held-copy wording, 2026-11-04

Standing: automated renderer observations of App-side behaviour. They are not
owner or human acceptance, not native J1/J2 passes, and not model, sign-in,
native window or production qualification. Holds last only as long as the App
window.

## Subject

- **Merged result:** PR #124, merged to main as `2d584803`. Its whole tree
  (`8d6e2140…`) is identical to the head integrated from, `7e57e3cf`.
- **Render subjects:** `f1a76e98` and `824e60f3`. Both are ancestors of
  `7e57e3cf`; the later main and stack unions were reviewed in source and not
  rendered again here.
- **Baseline:** the Run guide facts observed on `9248a36e`, and the #119
  "ready to send" residual observed on `114365c1`.
- **Builds:** each build is an offline `npm run build` of an immutable
  `git archive` export. The lock file and `package.json` were unchanged
  throughout.

## Method

- **Renderer:** cached headless Chromium, driven over CDP from a 127.0.0.1
  server, at desktop (1100×800) and narrow (480×860) widths.
- **Real input:** the host status from the frontend's executed Rust producers
  (packet sha256 `6d292510…`).
- **Synthetic, and labelled in each report:**
  - `workflow_select_listed` outcomes: never settling, success, and refusal;
  - `selection.newerRevision`;
  - a second registered revision;
  - run start outcomes;
  - the bring-back `null` result with the pre-fill still listed.

## Observed

| Head | Result |
|---|---|
| `9248a36e` (baseline) | **Run guide:**<ul><li>The "last result" printed raw JSON.</li><li>A newer registered revision showed only in the studio.</li><li>Same-name Use buttons didn't name their revision.</li><li>Focus dropped to `body` after Start.</li></ul> |
| `f1a76e98` | **Run guide:**<ul><li>**Last result:** nothing shows before it settles. Success shows plain words with the reply under "What the App reported", and a refusal reads "Couldn't ‹action›: ‹message›".</li><li>**Newer revision:** the Workflow step states it. Its button sends `workflow_follow_newer_revision` with the exact `selectionRef` and revision.</li><li>**Labels:** the button reads "Use ‹name› revision 2".</li><li>**Focus:** it moves to Start after Prepare, and to Run progress after Start.</li></ul>**#119 held copy:**<ul><li>The results line reads "…are prepared in ‹conversation›, but sending them is held…".</li><li>"Open … to read or remove" issues no IPC, and "Next" names the held state.</li></ul>**Defect:** after the acknowledgement, the row showed a second identical Open. |
| `824e60f3` | **Held copy after the acknowledgement:** the row has no button and reads "…prepared for this conversation but held… see below." A single Open remains on the results line.<br>**A copy that isn't held:** unchanged. |

## #119 residual

The "ready to send" label for the held copy was open when #119 was integrated
(main `f96e4252`). It is repaired by this subject: rendered at `f1a76e98` and
`824e60f3`, and merged as main `2d584803`. It was never waived.

## Not established

- Any real Codex turn, model, native window, or registration on the host.
- Owner or human use, and J1/J2 completion.

Evidence (task scratch `app-p2-trial-u5RbDlpZ`): `out-j2-base`, `out-j2-124`,
`out-j2-124b` (reports and screenshots), plus the synthetic peer `mock-j2.js`
and the driver `j2drive.mjs`.
