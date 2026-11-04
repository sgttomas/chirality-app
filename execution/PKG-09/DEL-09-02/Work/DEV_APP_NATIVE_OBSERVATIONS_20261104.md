# Dev-App native self-test observations, 2026-11-04

Standing: automated development test observations. They are not owner or human
acceptance, not native J1/J2 passes and not production qualification. The GUI
test loop is closed. The cause of the blank window is not isolated, and no
product exoneration is claimed.

## Subject

- **Build:** packaging's disposable debug build of PR #111 head `a6fbc9a8`
  (`a6fbc9a8cf79b1d1ca6e28caa11a43208caa8eb0`). The binary is ad hoc signed
  only and is not a production subject.
  - Executable SHA-256 `535a19c0…`.
  - Bundle tree v2 `701fae87…`.
  - ID `dev.chirality.app-v4.candidate.20261103-87cb47af`.
  - Configuration: custom-protocol only; distribution-successor off.
- **Test data:** disposable fixtures in task scratch only. No model, sign-in,
  credentials, keychain, enrollment or owner data. The owner's signed App and
  Codex processes were untouched.
- **Launch routes:**
  - Runs 1–5: a launchd job running `t3_slot`, then `sandbox-exec` with
    `deny network*` (localhost only, `~/.codex` denied), then a `perl` alarm.
    WebKit's system services are outside that sandbox.
  - Runs 6–8: an ordinary LaunchServices `open -n -W` with a fresh, empty
    `CODEX_HOME`. These runs were not network-denied.
  - Every run had an independent bound and ended with a normal Quit from the
    App's own menu (exit 0). No run needed signals or administrative cleanup.
- **Untested build:** the later `26a01ff9` dev build was not launched. Its two
  authorized cases are unused, and nothing here transfers to it.

## Observed

| Run | Result |
|---|---|
| 1 | The first-use window is titled "Chirality" and shows the new welcome: three numbered steps, with "Start with new settings (recommended)" preselected. "Review setup" is disabled until a project choice is made. The accessibility structure reads in a coherent order: heading level 1, then three level-2 sections, the project buttons, a labelled radio group, Review setup, and a "Technical details" disclosure. This is the accessibility tree, not a VoiceOver run. The web area is named "Chirality App v4" while the window is titled "Chirality". |
| 1 | "Choose project folder…" opens the native picker as a sheet attached to the window, with the message "Choose the project for the next App launch". Cancelling returns to an unchanged welcome with nothing chosen. Quit while the sheet is open exits normally. Before confirmation, no AppData exists for the dev ID; WebKit creates its own cache and data folders. |
| 2–8 | With the App inactive, the main window (unique exact match: 1100×800, "Chirality", on screen) **painted the welcome at about 3 s and was blank (dark) by about 8 s**. It stayed blank at 11–20 s. No AX window or web area was exposed. Captures were byte-identical across runs (rendered 335,288 B; blank 77,655 B). In runs 6–8 the window was 100% covered by two owner windows (an occlusion-fraction measurement). WebContent processes that started in the launch second stayed alive (correlated by timing only). The App had no child process before setup was saved. |
| 3, 7, 8 | Activation attempts did not activate the App: setting AXFrontmost (run 3), pressing the exact Dock tile through AX (run 8), and a title-bar HID click (run 7), which was not posted because the window was covered. Each request was accepted, but `isActive` stayed false. |

## Not observed

- Picker selection: this tooling can't reach the out-of-process panel.
- The new-settings review, the native "Leave setup unchanged" and "Create
  settings and save for next launch" choices, "You're set up", and the settings
  and home layout and modes.
- Relaunch to the workspace, Codex ready or error, supplier cleanup, and window
  close and reopen.
- The J1/J2 guide navigation added after `a6fbc9a8`.

## Capability limit

From this session, the disposable App can't be activated or brought forward
while the owner's windows cover it. The owner's windows are not moved, and no
owner act or new account is requested. Native first-use and lifecycle self-tests
therefore stop here. Rendered and backend self-tests continue independently of
the desktop.

Private evidence is in task scratch `app-devtest-111-vbW3A9qh`: run timelines,
watchdog logs and window-only captures. The dev-ID state for this build is
preserved.
