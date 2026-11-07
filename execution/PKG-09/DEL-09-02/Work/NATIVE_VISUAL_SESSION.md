# Native visual session helper (development only)

Status on 2026-11-07: **built and checked offline only. Never run.** The
owner approved *building and offline-checking* this helper, with one
independent review. That approval is not desktop availability, not an
owner window and not a GO. Running `native_visual_session.py` (anything other
than `--help`) launches the retained development App. It therefore needs its
own fresh owner/Root GO, an explicit owner-window end and an ordinary
`t3_slot`. This file creates no window, root, entry or GO.

## Purpose and limits

After repeated refusals from the earlier structural (AX) automation, the owner
wants direct visual Computer Use. This helper is the minimum glue for that: it
keeps one original `NativeSession` alive while a parent operator alternates
between looking at a screenshot (`view_image`) and sending one explicit
action. It is not a generic automation framework, an AX parser, private App
IPC, OCR or a model/API service. It does not prove App handling, setup
semantics, J1 or qualification.

The intended future StageA segment uses one reviewed 66d39df5/75e953fe
development App. Admission, original binding and cleanup are loaded before any
UI. The operator then selects the invented project in the picker, reviews the
full effects and the native confirmation, saves the pending request and reads
it back, quits normally and observes the original's actual absence. The
segment excludes any saved-workspace relaunch, supplier, model or sign-in.

## Source basis (reused unchanged; never monkeypatched)

| Input | SHA-256 | Used for |
|---|---|---|
| `Work/j1_stage_a_phase.py` | `f510d9be6a4e2e8d8eb77f25642e1f16a33f13c8d909898ff7f71ff6f6a3ccdc` | `NativeSession.admit/launch_once/bind_cleanup/check/normal_terminate/absent/hold_until_absent/verify_saved/launch_unknown`, `AppKit`, `private_journal`, `cleanup_receipt`, `setup_effects`, `checked_locations`, `checked_pending`, `Subject` |
| `Work/native_b_diagnostic.py` | `fd37834b301f138963cdfe76f8bf3a146aea373b99ab2c994546ff73c939af19` | `window_inventory` (owner-PID filter before decoding) over the admitted backend; backend `identity` for birth checks |
| current binding `…/app-native-visual-current-subject-hoamd1ib/preflight-current.json` | `5567d97631e281a82c2682c60f73798439534a9a54611ed11655e42e5bb6034b` | explicit current subject pinned as `REVIEWED_SUBJECT`: source `66d39df5…`, identifier `dev.chirality.app-v4.candidate.20261107-75f470c7`, executable SHA `75e953fe…`, unchanged packet `app-j1-owner-reviewed-naw71ke6` |
| historical corrected receipt `…/app-j1-stage-a-_i48c648/preflight-corrected.json` | `56116108ab21e1499d0e4c6f53381449f970232c3bcf7972e8b8bd94d45ee6fa` | original policy/packet input, preserved unchanged; not current artifact, state, permission or GO evidence |

Both sources are loaded by hash from their bytes (`load_core`, `load_reader`).
The helper does not call `StageA.run`, `run_prepared` or the picker-diagnostic
and cap frameworks. The consumed entry
`app-j1-root-boundary-corrected-staged-aaz00q6m/entry.py` was read statically
for subject identity; it was not executed, imported or rearmed. The old 180/110
StageA budgets and the 185 s entry guard are unchanged. The CBD diagnostic
chain stays stopped.

Agent0 selected the current post-PR150 bundle after receiving its successful
ordinary offline build. The new binding verifies the current executable,
Info.plist, build record and unchanged eleven packet members. It contains only
the current development-state paths and route-switch names; it does not copy
old absence/environment observations to the new subject. `ready=true` means
static binding ready, with runtime state/trust/route/absence still unqueried
until future admission. Authentic561 and the older eaf bundle are unchanged.

## Future invocation (only after a fresh GO)

```sh
CODEX_HOME=<fresh scratch> TMPDIR=<fresh scratch> /Users/ryan/dev/chirality-t3/tools/t3_slot.sh \
  python3.13 -I -B execution/PKG-09/DEL-09-02/Work/native_visual_session.py \
  --owner-window-end '<FRESH UTC …Z FROM THE GO>' \
  --preflight /Users/ryan/dev/chirality-t3/scratch/app-native-visual-current-subject-hoamd1ib/preflight-current.json \
  --journal '<NEW EMPTY PRIVATE JOURNAL DIRECTORY>'
```

Use one persistent operator exec/PTY session with stdin kept open; send JSON
lines (for example `{"op":"capture"}`) to that same session and inspect its
output/frame with `view_image`. An ordinary exec tool may yield a live session
identifier while the worker runs. Do not launch a separate keeper process or
replace the worker with one-shot shell input commands. EOF begins cleanup.

The helper requires a new, empty journal directory with mode 0700. Frames are
written to `<journal>/frames/frame-NNN.png` (mode 0600). Each journal record is
an exclusive `NNN-kind.json` file written by `private_journal`. `NativeSession.admit` also requires the
parent process to be `t3_slot_run.sh`.

## Control protocol

stdin takes one JSON object per line, at most 4096 bytes. Keys must match
exactly and duplicates are refused. Nothing else is accepted: no eval, shell,
paths (except the two bounded locations below), PIDs or free text. stdout
returns one JSON line per event or response, each with `ui_seconds_left`.

| op | fields | effect |
|---|---|---|
| `capture` | — | Checks identity, records foreground/window/display facts, runs `screencapture -x -m` to a numbered file, then records the facts again. A frame is `actionable` only if the facts did not change, the original App is foreground, its windows are visible and the geometry is unambiguous. |
| `click` | `frame,x,y` (integer pixels) | One left down/up pair at the mapped global point, inside a visible original-App window |
| `key` | `frame,key` | Only `go_to_folder` (⌘⇧G), `select_all` (⌘A) or `return` |
| `type_project` | `frame` | Types the exact text `/Users/ryan/dev/chirality-t3/scratch/app-j1-owner-reviewed-naw71ke6/session/project` as UTF-16 Unicode events |
| `activate` | `frame` | Activates the original `NSRunningApplication` once per session, and only when the frame shows it is not foreground |
| `confirm_first_effect` | `frame` | Records the operator's assertion (not a proof) that a fresh post-click frame shows the first click's effect |
| `wait` | `seconds` (0 < s ≤ 10) | Sleeps, clipped to the UI cutoff. Sends no action. |
| `expected_effects` | `settings_folder, sign_in_folder` | Returns `setup_effects(...)` for the operator to compare with the visible text. Both paths must lie under the exact development AppData. |
| `verify_saved` | — | Calls `NativeSession.verify_saved` with those reviewed locations, once only |
| `status` / `quit` | — | `quit` begins normal cleanup |

Rules: every input (`click`, `key`, `type_project`) and `activate` consumes the
permission of the latest frame, even if a later check refuses. Stale, replayed,
unknown or older-than-60 s frames are refused. The first input must be a single
benign visible click. No further input is accepted until
`confirm_first_effect` names a frame captured after it. The tool never repeats
an action. Every input reports `dispatch: attempted` and `handling: unknown`.

## Deadlines

The session is capped at 600 s in total. The UI phase gets at most 480 s, and
120 s is reserved for normal cleanup. Admission time counts against the total.
Each deadline is the earlier of the monotonic cap and the absolute owner-window
end. Launch is refused unless at least 180 s of UI time remains after
admission, so a stale or insufficient end refuses before any native load. The
stdin loop wakes at the UI cutoff and never blocks indefinitely. EOF, the UI
cutoff, `quit`, any fatal error, lost output or SIGTERM/SIGHUP/SIGINT all go to
cleanup. Signals are ignored once cleanup begins, so the slot stays held. No
command can extend, rearm or retry a session. Native calls are cooperative, so
overrun is reported as `overrun` / `owner_end_overrun`.

## Coordinates

These are the frame-geometry rules:

- Capture is of the main display only (`-m`).
- `CGDisplayBounds(CGMainDisplayID())` must have origin (0,0), and its size
  must equal the display mode's point size.
- The PNG pixel size must equal the mode's pixel size.
- The scale must be the same on both axes and be exactly 1 or 2.
- Global point = origin + pixel / scale.
- The target must fall inside a listed on-screen layer-0 window owned by the
  original PID (rows are filtered by owner PID before decoding). The frontmost
  containing window, in WindowServer list order, is chosen, and its number is
  set on the mouse event (fields 91 and 92).

Anything else refuses. Before any input, the helper repeats the full original
check (birth, UID, path, PGID and executable hash) and the supplier-child
check. The foreground, window and display facts must still equal the frame's.

## Input and cleanup

Events use a private `CGEventSource`
(`kCGEventSourceStatePrivate`) and `CGEventPostToPid` to the original PID only.
The helper uses no clipboard, global or HID-tap posting, or private API. All
events are allocated before the first post. The full identity check runs
immediately before posting. Each up event follows its down event, including
after a post error, but only after a birth re-check: an up event is never sent
to a possibly reused PID. Every CF object is released in `finally`, and release
errors stop the session.

Cleanup runs without a parent roundtrip: `check` is followed by exactly one
`normal_terminate`, which is never repeated, even after an error. Absence is
then polled until the total deadline. Only actual original-birth absence closes
the session. If absence is late or unknown, the helper writes `held` /
`no_more_input` and calls the existing `hold_until_absent`, keeping the slot.
It never forces termination or signals another process. Native resources are
closed afterwards. Exit code 0 means only that cleanup closed with evidence
intact. It is not closure evidence and not a claim about setup.

## Future setup checkpoints (for the GO, not performed here)

1. Hosted CI and review of this helper are complete. The parent's independent
   review is integrated.
2. The owner selects a fresh window, and the
   `--owner-window-end` leaves ≥ 300 s plus slot wait.
3. The development AppData for the identifier is absent. No
   instance of the identifier is running. The packet manifests and executable
   hash are unchanged. `admit` refuses otherwise.
4. The same worker's no-prompt preflights (`CGPreflightScreenCaptureAccess`,
   `CGPreflightPostEventAccess`, `AXIsProcessTrusted`) are all true. No
   prompts or permission changes.
5. The first action is a benign visible click whose effect a fresh frame
   shows. Only Root continues after confirming it.
6. Before any affirmative confirmation click, the parent reads the full visible
   effects and the native question, and compares them with `expected_effects`.

## Unproved native behaviour (all mocked; none run)

- Whether `CGEventPostToPid` mouse events are hit-tested and handled by
  WebKit/AppKit in this App, including with window fields 91 and 92 set.
- Whether keyboard and Unicode events reach the picker's Go-to field, and
  whether NSOpenPanel is in-process for this unsandboxed debug App. An
  out-of-process panel would not receive these events.
- Whether `NSWorkspace.frontmostApplication` and `isActive` are fresh in a
  runloop-less worker (a 0.05 s `CFRunLoopRunInMode` is attempted).
- Whether `activateWithOptions:0` takes effect under macOS cooperative
  activation.
- Whether `screencapture -m` and `CGMainDisplayID` always name the same display.
- Whether the CGDisplayMode pixel size matches the capture under every scaled
  mode.
- The CGWindowList front-to-back order with `kCGWindowListOptionAll`, and
  foreign overlays above the App. Overlays are visible in the frame but are
  not detected, because foreign rows are not decoded.
- The cost of the reused reader holding CF key strings per row until close.

Screenshot and foreground facts do not prove machine isolation or guaranteed
dispatch.

## Offline verification

`test_native_visual_session.py` uses injected fakes for the OS, session, time
and streams. The exact core and reader are loaded through the hash-checked
loaders, and `verify_saved`/`checked_pending`/`setup_effects` are exercised
through the real core functions against a temporary request file. No native
framework, capture, input, App, process or resource probe is involved.

The implementation task reported 30 passing wrapped unit tests, deliverables
and syntax/diff checks. It also ran nine mutation checks directly through
Python outside the required slot wrapper, and deleted the shared gitignored
`Work/__pycache__` directory. These are task deviations, not compliant
validation or cleanup authority. They are retained truthfully; no mutation
rerun is needed to relabel them. Original protected source bytes are unchanged.
After current-subject binding and the persistent-session instructions were
updated, Agent0 ran the same focused suite under the maintained wrapper with
a fresh scratch home: 30 passed, zero failures, with no native operations.
The wrapped deliverables check also passed. The checked commands/logs are in
`/Users/ryan/dev/chirality-t3/scratch/app-native-visual-current-checks-uwi5ojt2/CHECKS.json`.
One independent review of this exact contribution remains before integration;
there has been no native click/type or setup trial.
