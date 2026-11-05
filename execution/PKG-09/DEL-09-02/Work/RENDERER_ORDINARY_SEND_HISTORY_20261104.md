# Renderer check of ordinary send and History Continue, 2026-11-04

Standing: automated renderer observations of App-side behaviour. They are not
owner or human acceptance, not native J1/J2 passes, and not model, sign-in,
native window or production qualification. The native GUI loop stays closed
(`DEV_APP_NATIVE_OBSERVATIONS_20261104.md`).

## Subject

- **Merged result:** PR #123, merged to main as `f9dd4ef7`. Its whole tree
  (`3e928e48…`) is identical to the tested final head `90706dae`.
- **Baseline:** the History run on `9248a36e`, whose `app/` tree is identical to
  main `d968d643`.
- **Heads checked on the way:** `7add592a`, `1f54e4ab` and `90706dae`.
- **Builds:** each build is an offline `npm run build` of an immutable
  `git archive` export. The lock file and `package.json` were unchanged
  throughout.

## Method

- **Renderer:** cached headless Chromium, driven over CDP from a 127.0.0.1
  server, at desktop (1100×800) and narrow (480×860) widths.
- **Real input:** host status from the frontend's executed Rust producers
  (packet sha256 `6d292510…`).
- **Synthetic, and labelled in each report:**
  - `conversation_send_text` outcomes: success, plain-string refusal, plain-string
    unknown, and `null`;
  - the History list, selection and admitted resume. Their shapes are copied from
    `history-continue-navigation.test.mjs` and `continuation-fixture.mjs`;
  - Codex restart and home change while keeping the same thread ID;
  - plan mode marked as offered;
  - the Make-guide request offer.
- **Not run in a browser:** the other variants of the retained-handler (stale
  closure) case. The frontend's mounted tests cover them.

## Observed

| Head | Result |
|---|---|
| `9248a36e` (baseline) | **History Continue** admitted the conversation, but the History view stayed shown with focus on `body`.<br>**Draft text:** text written for Conversation 1 was now addressed to the resumed conversation, shown only by a raw thread ID.<br>**Ordinary send:** an unknown outcome looked the same as a refusal; the text was kept and "Send text" stayed enabled. |
| `7add592a` | **Held outcomes:** unknown, `null` and plain-string refusal are all held without parsing the text.<ul><li>The text and the model are kept.</li><li>The alert's details show the message, mode, model, conversation and session, and what was reported.</li><li>"Send text" is disabled, and the readiness line says why.</li><li>A captured callback issues no IPC, and editing the text doesn't lift the hold.</li></ul>**Other cases:** another conversation stays sendable, with the record still listed. A same-ID restart or home change stays held, with "isn't loaded now" and same-ID wording. The acknowledgement issues no IPC; then exactly one new send. A successful send clears the text.<br>**Continue:** shows the Conversation view, with a labelled notice and the "Where your text goes" note.<br>**Defect:** the focused message box after Continue was off-screen (top 2253 / 3339). |
| `1f54e4ab` | **After Continue:** the message box and its note are in view, with focus in the box.<br>**After an unconfirmed send:** focus moves once to the record's alert, which is in view.<br>**Plan and default buttons:** they are disabled while held, and a captured plan callback issues no IPC (synthetic plan mode offered). |
| `90706dae` | **Draft destination:** a request offered from the Make guide, and text replaced in the composer, both now get a "Where your text goes" note naming the continued conversation after Continue. At `1f54e4ab` the offered request had no note.<br>**Fresh send after acknowledgement:** a Send captured before the unconfirmed attempt issues no IPC after the acknowledgement. Fresh sends to A and then B each keep their own text and model. |

## Not established

- Any real Codex turn, model, provider contact, sign-in or native window
  behaviour.
- Owner or human use, and J1/J2 completion.
- Deduplication by the host, across windows or after a relaunch. The holds last
  only as long as the App window.

Evidence (task scratch `app-p2-trial-u5RbDlpZ`): `out-j2-base` (baseline
History), `out-j2-123`, `out-j2-123b`, `out-j2-123c`, `out-j2-123d` (the
`1f54e4ab` reference) and `out-j2-123e` (reports and screenshots), plus the
synthetic peer `mock-j2.js` and the driver `j2drive.mjs`.
