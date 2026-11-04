# Renderer check of trial start and Continue as, 2026-11-04

Standing: automated renderer observations of App-side behaviour. They are not
owner or human acceptance, not native J1/J2 passes, and not model, sign-in,
native window or production qualification. The native GUI loop stays closed
(`DEV_APP_NATIVE_OBSERVATIONS_20261104.md`).

## Subject

- **Merged result:** PR #117, merged to main as `d968d643`. Its `app/` tree is
  `cca60fa7…`, identical to the tested head `9248a36e`; the final head
  `3c4d85b4` differs from it only in documents.
- **Baseline:** main `98722981`, before #117.
- **Intermediate heads:** `c64e81a3` and `8a61a49b` were checked on the way to
  the final head.
- **Builds:** each build is an offline `npm run build` of an immutable
  `git archive` export. The lock file and `package.json` were unchanged
  throughout.

## Method

- **Renderer:** the built `dist/` runs in cached headless Chromium, driven over
  CDP from a 127.0.0.1 server, at desktop (1100×800) and narrow (480×860)
  widths.
- **Real packets:**
  - host status and the draft row from the frontend's executed Rust producers
    (`selected_chain_actual_status_reports_b_before_the_ordinary_choice`,
    `workflow_action_actual_create_result_precedes_explicit_draft_observation`;
    packet sha256 `6d292510…`);
  - the IPC command names and arguments as the App sends them.
- **Synthetic, and labelled in each report:**
  - the role set;
  - the model lists (named, unnamed, other provider, wrong generation,
    incomplete);
  - the pending and started clean trial, shaped like `trials.test.mjs`;
  - the Continue as handoff;
  - every command outcome: success, refusal, and unknown. Trial refusals carry
    `prefillKept`; `thread_start` errors are plain strings.
- **Not run in a browser:** the retained-callback cases. The frontend's mounted
  tests cover them.

## Observed

| Head | Result |
|---|---|
| `98722981` (baseline) | **Clean trial and Continue as panels:**<ul><li>They offered only raw Model and Configured Codex provider fields, plus an Access entry.</li><li>Send and Start stayed disabled until IDs were typed.</li><li>Tab left the panel after Access entry.</li></ul>**Entry path:** the Make guide's link landed on `#conversation` and showed the engineering line "Original composer owner: global clean composer; no conversation render owner." |
| `c64e81a3` | **Chooser:** Access route → Read available models → Use, with the expected arguments, across all model-list variants; the wording and landing focus were repaired.<br>**Defect:** a clean-trial generation change remounted the panel and lost the person's edited inputs. |
| `8a61a49b` | **Clean-trial retention:** the edited inputs survive a generation or home change, shown with an out-of-date marker and Send disabled. A home change offers that home's own route. Starting a trial that was started but not sent works. Error and unknown wording is right, and the inputs are kept.<br>**Defect:** a Continue as start that failed or had an unknown outcome showed no outcome in the panel. The host text appeared at the top of the page prefixed `thread_start:`, a distant alert said "see the message below", and Start was re-enabled. |
| `9248a36e` | **Continue as start outcome**, for both failure and unknown, at both widths:<ul><li>A focused role=alert "Start outcome" appears in the panel and is visible.</li><li>The host text is shown under "What was reported", and the distant alert no longer fires.</li><li>Start stays held after an edit until "I've checked — let me start again". That button starts nothing.</li><li>The handoff text is kept, and `thread_start` carries `generation`.</li></ul>**Full regression of the earlier items held:** route, read and use; the model variants; clean retention; error and unknown wording; a started-but-unsent send; `generation` in `workflow_trial_start_clean` and `workflow_trial_send`. |

## Not established

- Native generation binding at admission; this is a separate runtime follow-up.
- Any real model list, sign-in, provider contact or native window behaviour.
- Owner or human use, and J1/J2 completion.
- **PR #119**, the guide's trial state, bring-back and review, is **held**. Its
  renderer findings are open and are not results here.
- **Seen on the same tree, but not results of #117:**
  - The Run guide prints raw JSON as its last result, never mentions a newer
    revision, and names the Use button without the revision.
  - History Continue admits a conversation but stays in History, with no focus
    on the admitted conversation.
  - An unknown ordinary-send outcome leaves Send enabled.

  These go to later increments.

Evidence (task scratch `app-p2-trial-u5RbDlpZ`): `out-main`, `out-pr117`,
`out-pr117b`, `out-pr117c` (reports and screenshots), plus the synthetic peer
`mock-p2.js` and the driver `p2drive.mjs`.
