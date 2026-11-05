# Renderer check of returning to an unfinished draft, 2026-11-04

Standing: automated renderer observations of App-side behaviour. They are not
owner or human acceptance, not native J2 passes, and not model, sign-in,
native window, relaunch or production qualification.

## Subject

- **Merged result:** PR #128, merged to main as `eaf5d057`. Its whole tree
  (`ce5b122d…`) is identical to the head integrated from, `d53b334a`.
- **Render subjects:** each is an ancestor of `d53b334a` and keeps its own
  identity.
  - `ecff44b1`: R2 and R3, compared with the #125 head `0b9a9068`.
  - `a7f9deae`: R1.
  - `f5cdc006`: the integration head that resolved the HistoryPanel conflict with
    main #123. It was checked with one natural chain.
- **Not rendered:**
  - Later unions were compared in source only.
  - R1's same-commit staleness guard was inspected in source; I tested no
    transition for it.
- **Baseline:** `out-j2-ret`, on the #125 head `9efa17a7`.
- **Builds:** each build is an offline `npm run build` of an immutable
  `git archive` export. The lock file and `package.json` were unchanged
  throughout.

## Method

- **Renderer:** cached headless Chromium, driven over CDP from a 127.0.0.1
  server, at desktop (1100×800) and narrow (480×860) widths.
- **Real inputs:**
  - the host status and draft row from the frontend's executed Rust producers
    (packet sha256 `6d292510…`);
  - the real `trial_native_source` and `authoringSourceLimit` strings.
- **Synthetic, and labelled in each report:**
  - **The relaunch:** every trial link is saved/cold, with bare conversation IDs,
    and the old conversations are not loaded.
  - **The History list** and the admitted resume.
  - **For the chain only:** trial 3's saved authoring ID equals the ID of the
    stored History conversation.

## Observed

| Head | Result |
|---|---|
| Baseline (`9efa17a7`) | **R1:** "Continue ‹draft›" left focus on the button, off-screen.<br>**R2:** there was no route to the saved conversation, and the drafts text said reading History "doesn't continue it".<br>**R3:** each disabled Bring showed the raw host string. |
| `ecff44b1` | **R2:**<ul><li>Each cold row offers "Look for it in History".</li><li>It opens History with the saved ID in the focused search box and a note that this is only a search.</li><li>It issues no IPC: no read, select, home change or Continue.</li><li>The drafts text now names Continue as a separate step.</li></ul>**R3:** each cold Bring shows a plain reason, with the exact `sourceLimit` under "Why".<br>**Defect (R1):** focus went to a Draft status region taller than the viewport, so its first lines were out of view. |
| `a7f9deae` | **R1:** focus goes to the draft state line at the top of the viewport, and the next-action sentence is in view below it. |
| `f5cdc006` | **Natural chain:**<ol><li>A kept composer draft.</li><li>Back in the draft, the saved-ID search issues no IPC.</li><li>The explicit list, select and Continue issue exactly those three host commands.</li><li>The landing is the Conversation view, with focus in the visible composer, the kept text intact, and "Where your text goes" naming the continued conversation.</li></ol> |

## Not established

- A real relaunch, durable trial records, or a real History read or resume.
- R1's same-commit staleness guard in a renderer.
- Any model, native window or Codex turn.
- Owner or human use, and J2 completion.

Evidence (task scratch `app-p2-trial-u5RbDlpZ`): `out-j2-ret`,
`out-j2-128base`, `out-j2-128`, `out-j2-128b`, `out-j2-128c` (reports and
screenshots), plus the synthetic peer `mock-j2.js` and the driver
`j2drive.mjs`.
