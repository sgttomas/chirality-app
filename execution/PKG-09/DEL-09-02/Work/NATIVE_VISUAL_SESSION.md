# Native visual session helper (development only)

Later disposition (2026-11-07): the repaired helper's final session captured
the App but established no visible effect from its single click. Normal
original closure was verified. See
[the final actual account](J1_VISUAL_SETUP_FINAL_ACTUAL_20261107T182502Z.md).
Both attempts and the one repair are consumed. This custom control-tool path
is stopped; no third attempt, input-mechanism change or further helper work is
selected. Earlier preparation/review text below retains its dated meaning.

Status on 2026-11-07 (updated): the helper at `eb488ce0` ran once; that first
actual session stopped before any input because it captured the main display
while the App window was on another display (`J1_VISUAL_SETUP_ACTUAL_20261107T172459Z.md`).
The one bounded window-capture repair (last section) is **built and checked
offline only and has never run.** Original status: the owner approved *building and offline-checking* this helper, with one
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
| `capture` | — | Checks identity and records foreground/window facts. It selects the frontmost on-screen layer-0 window owned by the original PID from those fresh rows and runs `screencapture -x -o -l <thatWindowID>` to a numbered file. Then it records the facts again. If no such window exists, nothing is captured; the frame is image-less and not actionable. A frame is `actionable` only if the facts did not change, the same window is still the frontmost targetable one with the same bounds, the original App is foreground and the PNG is exactly that window's bounds at 1x or 2x. |
| `click` | `frame,x,y` (integer pixels local to the captured window image) | One left down/up pair at the mapped global point, inside the captured original-App window only |
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

These are the frame-geometry rules (since the window-capture repair; the
original main-display rules are kept in the repair section):

- The captured window is the first on-screen layer-0 row with sane finite
  bounds and an exact nonzero 32-bit window number. Rows come from the reused
  reader, which filters by original owner PID before decoding, in WindowServer
  order. The window ID never comes from the operator, a foreign row, a fixed
  or stale value, or a display. There is no fallback capture.
- Capture is of that one window, without its shadow (`-l <id> -o -x`). It is
  not a whole-display capture and no display ID is involved.
- The PNG size divided by the window's CG point size must give the same scale
  on both axes, exactly 1 or 2. Any other size refuses as ambiguous (for
  example a shadow, an attached overhang, a crop or a mixed scale).
- The window origin may be nonzero or negative. Global point = window origin +
  capture-local pixel / scale.
- The target must fall inside the captured window. That window's number is set
  on the mouse event (fields 91 and 92).
- Frame output reports `capture` (`basis: original-window`, `window_id`,
  `origin_points`, `size_points`, `whole_display: false`). It also reports
  `windows_capture_pixels`, which are each owned window's rectangle in pixels
  local to the capture and may lie outside the image. The journal also keeps
  `windows_global_points`.

Anything else refuses. Before any input, the helper repeats the full original
check (birth, UID, path, PGID and executable hash) and the supplier-child
check. The foreground and owned-window facts must still equal the frame's.

## Input and cleanup

Events use a private `CGEventSource`
(`kCGEventSourceStatePrivate`) and `CGEventPostToPid` to the original PID only.
The helper uses no clipboard, global or HID-tap posting, or private API. All
events are allocated before the first post. After allocation and journal
work, every new down/chunk rechecks the original, foreground, owned-window
facts, frame age and current UI/owner cutoff. Activation has an equivalent
final identity/time check after AppKit preparation. Each up event follows its down event, including
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
- Whether `screencapture -l <id> -o` produces exactly the window's CG bounds
  times its backing scale on every display and scaled mode. A mismatch is
  refused, not corrected.
- Whether an attached sheet or panel appears as its own frontmost owned row or
  only inside or beyond its parent's image. An overhang beyond the parent's
  bounds is refused.
- The CGWindowList front-to-back order with `kCGWindowListOptionAll`. Foreign
  overlay rows are not decoded, and a window capture does not establish
  whether the App is occluded on the desktop. Attached-window composition
  remains a native unknown rather than an exclusion guarantee.
- (Historical, eb488 only) main-display capture: the first actual session
  showed that `-m` can miss the App window entirely.
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
The one independent review of `64cecd469d63ae58a74648d4be4a1b692573712d`
found two dispatch-boundary gaps: preparation could cross the cutoff, and
visual facts could change during journaling/allocation. Agent0 repaired those
boundaries directly. Three regression methods cover expiration during intent,
allocation and final checks, activation preparation, foreground/window/frame
drift and Unicode expiry after one down. An already attempted down still gets
its original-birth-checked up; no later chunk starts after cutoff.

The isolated regressions fail in thirteen scenarios against the reviewed
source. All 33 methods then pass on the repaired source under the maintained
wrapper, and deliverables checks pass. A shallow fake-window fixture initially
leaked bounds between cases; the fake now deep-copies its rows. The initial
failure and final isolated results are retained at
`/Users/ryan/dev/chirality-t3/scratch/app-visual-review-fixes-aukewaog/`.
No second review round, native click/type or setup trial was performed.

## Window-capture repair after the first actual session (2026-11-07)

**First actual facts (preserved, from the committed account `f629bf4c`, cherry-picked unchanged as `6a9df95b`).**
Helper `eb488ce05d40dfb0d3b4175afbc7bbf49a20d4e3` ran once on the
66d39df5/75e953fe development App. It launched original PID 38825 and
captured one frame of the main display: 2624x1696 pixels, scale 2, global
bounds `[0,0,1312,848]`. The only targetable owned window, 62477, was at
global point bounds `[1722,93,1100,800]`, wholly on another display. The frame
was still labelled actionable, because the old helper required only that some
on-screen owned window existed. It showed another application. The operator
sent no click, key, text or activation and quit. Cleanup began at53.859592s;
actual original-birth absence was verified by controller elapsed54.250037s,
with no overrun. This is not the termination call's duration. The wrapper
ended at17:25:53Z, rc0.
This was a capture/coordinate assumption failure. It is not an App failure
and not evidence about input effectiveness. That window and journal are
consumed.

**Scope of this repair (the one bounded mechanics repair).**

- `capture_plan` takes the frontmost targetable original-PID window from the
  fresh reader rows of each capture. `owned_windows` now also requires an
  exact nonzero uint32 window number.
- `MacVisual.capture(number, window, timeout)` runs `/usr/sbin/screencapture
  -x -o -l <window> <path>` and refuses a non-`int` or out-of-range ID before
  any process starts.
- `window_geometry` replaces `frame_geometry`: the window origin plus pixel
  divided by scale, with the scale exactly 1 or 2 and equal on both axes.
- After capture, the window must still be the same frontmost targetable
  window with the same bounds. Otherwise the frame is not actionable.
- `map_target` maps only into that captured window.
- If no targetable window exists, nothing is captured. The image-less frame
  stays usable only for the existing one-time `activate` and cannot be used
  for `confirm_first_effect`.
- Output metadata is capture-local and labelled as a window capture.
- The main-display CG bindings (`CGMainDisplayID`, `CGDisplayBounds`,
  `CGDisplayCopyDisplayMode`/mode getters/release), the `geometry()` adapter
  method, the `display` facts and the `CGRect`/`CGSize` structs are removed.
  There is no monitor catalogue or new API.
- Unchanged:
  - event creation, posting and release;
  - `Gesture` pairing and the P1/P2 dispatch-boundary rechecks;
  - activation time checks;
  - the original/foreground/supplier checks;
  - once-only normal Quit, absence and the held slot;
  - the allowed keys and the exact project text;
  - the subject, profile `5567d976…` and the core/reader hashes
    (`f510d9be…`, `fd37834b…`).

**Checks.** Unit, deliverables and syntax checks ran under `/Users/ryan/dev/chirality-t3/tools/t3_slot.sh`
with a fresh scratch `CODEX_HOME`/`TMPDIR` and `python3.13 -B`. The scratch
directory is `/Users/ryan/dev/chirality-t3/scratch/app-visual-window-capture-checks-CZt2tFxi/`.
`unit.log` records 41 passing tests and zero failures. That is 33 earlier
methods, with geometry expectations adapted, plus 8 new
`OriginalWindowCapture` methods. The new methods cover:

- the actual off-main shape `[1722,93,1100,800]` at 1x and 2x, mapping
  pixel (0,0) to (1722,93) and the last pixel inside the window;
- the actual 2624x1696 main-display PNG, which is refused;
- a negative origin;
- frontmost owned-window selection;
- no foreign, arbitrary, invalid-ID or display fallback;
- move, resize, disappearance or a new front window during capture;
- the image-less activation route;
- the exact `-x -o -l 62477` argv through a mocked `subprocess.run` on a
  `MacVisual.__new__` instance.

The deliverables check is logged as `deliverables.log`. No mutation campaign,
before-repair negative run, native capture, input, App, preflight or
process/resource probe was run. The only native-adjacent action was reading
the installed `screencapture` usage text and man page. Edit scripts, hashes,
a metadata-JSON read and the usage command ran directly, as did Git's diff
check; no unit or mutation test ran outside the wrapper.

**Still unproved natively.** Window-capture size and scale fidelity, sheet and
panel representation, CGEventPostToPid handling, keyboard and Unicode
delivery, activation, and foreground freshness. No independent review was
done for this repair. A second live session needs this repaired source
reviewed and committed by the parent, plus a fresh owner GO. If it also fails
on mechanics, tooling stops.
