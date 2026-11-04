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
- **Test data:** disposable fixtures in task scratch. No model, sign-in,
  credentials, keychain or enrollment. The owner's signed App and Codex
  processes were untouched. An early accessibility walk included Recent Items
  filenames; that dump was deleted. The first picker also opened in an owner
  folder before its initial location was restricted to scratch. No owner file
  contents were read. Later walks were restricted to App windows or named
  controls; retained private picker captures include scratch contents and
  sidebar volume names. A sandbox spot-check also attempted
  `cat ~/.codex/config.toml` under the explicit deny rule: it was denied
  (exit 1), its output was discarded, and no configuration bytes were read.
  No filenames or captures are published here.
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
| 2 | A blank dark main window was captured at about 14 s after launch and remained blank at about 20 s, inactive, with no reachable web area. Its earlier paint state was not captured. |
| 3 | The main window was blank at 6.7 s and 9.9 s, with zero reachable AX windows. Setting AXFrontmost returned success but did not activate the App. Its earlier paint state was not captured. |
| 4 | The 1100×800 main window was on screen at 3 s and 8 s; AXWindows exposed one window. The captures selected a different, offscreen 500×500 window, so rendering of the main window is **unobserved**. Those captures are retained with that limitation. |
| 5 | The same uniquely selected main window painted the welcome at about 3 s and was blank by about 8 s, with no intervening input. It remained inactive and exposed no AX window or web area, even while painted. |
| 6 | LaunchServices reproduced paint at about 3 s followed by blank at 8 s and 20 s. The App was inactive and exposed no AX window. WebContent processes started near launch and remained alive through 20 s; association with this App is timing correlation only. |
| 7 | The main window was 100% occluded by two windows above it at 3 s, 8 s and 11 s. It painted at about 3 s and was blank by about 8 s. The title-bar click was **not posted**, because its point was covered by another window. No other app was affected. |
| 8 | The main window was already blank at the first sample (9.1 s) and stayed blank through the later samples (about 10–15 s). It was 100% occluded and inactive, with no AX window. Exactly one Dock tile matched the dev bundle's path; AXPress returned success, but actual activation and occlusion did not change. |

Dark main-window captures from the properly selected windows in runs 2, 3,
5, 6, 7 and 8 were reported byte-identical (77,655 bytes). The corresponding
rendered captures in runs 5, 6 and 7 were reported byte-identical (335,288 bytes).
These comparisons do not supply the missing observations in other runs.
Every run ended through the App's own Quit menu item. No Codex supplier was
spawned, and AppData for this dev ID remained absent throughout.


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
