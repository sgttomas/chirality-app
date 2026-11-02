# Product window targeting and setup-picker parenting

Owner AFK direction selects useful product UI/native-boundary work, preserving
v3 visual design and current contracts. This slice starts from actual main
3f7974bcfac00a6a246c17b6c282657e4f352c40. Lane4 owns DesktopSetupPanel,
DailyWorkspace, limited App navigation and their frontend tests; its route was
notified before Rust edits. No frontend/style files, labels or IPC payloads were
changed here. The frozen typed diagnostic zootd3ob and actual candidate
1f67d3822b-8c83d74ae3ce remain unchanged/unrun; no new native experiment is implied.

## Source-demonstrable defects and changes

1. show_main_window used the first value of the webview-window map. A secondary
window could be selected instead of the configured main, or substituted when
main was absent. Dock reopening and Waiting navigation must target the same
main label that the Waiting wake event and lifecycle parent lookup use. The new
small main_window::original helper requests only get_webview_window("main") and
retains that window. It never selects first/focused/auxiliary windows. This is a
source-level targeting correction, not evidence that current AX self-reference
was caused by a secondary window (the current config has one main window).

2. desktop_setup_pick used parentless blocking file/folder dialogs while the
subsequent desktop_setup_prepare already used its retained invoking window.
Pick now receives Tauri's implicit invoking Window and dispatches the native
picker asynchronously on the main thread, with both raw handles checked and
cached before set_parent (the plugin otherwise ignores failed handle lookups).
Only the command worker waits. A selected result is revalidated against that
same original window on the main thread before returning. Missing/destroyed
parent or dispatch/channel failure refuses selection; no replacement window or
parentless fallback is allowed. No returned selection remains null, including
a cancelled picker after the original window disappears. No Root guard is held
across the dialog, and no configuration, token or path is saved by picking.

The command name and {kind} payload remain unchanged. config/agents are files;
skills/project are folders. All four titles and the existing native-path/display
JSON conversion remain unchanged. Preview and prepare commands, tokens, pending
next-launch semantics and native confirmation are untouched. No implicit save,
new timeout, test-only authority bypass or supplier start is introduced.

3. Waiting-request errors used an unparented informational dialog. The menu
callback now retains main and queues the existing checked-parent notice on a
named worker so the UI thread does not block awaiting its result. Missing or
destroyed original windows only log; no parentless fallback. This uses the same
notice/confirmation machinery already used for Quit refusals and changes neither
Waiting intent selection nor approval authority. Quit's assessment, confirmation,
settlement, cancellation and exit policies are untouched.

## Startup/accessibility audit and limits

Locked Tauri2.11.1 app.rs setup builds configured webview windows before invoking
the App setup hook. The App uses the default main label and existing walking-
skeleton title; no title/label was renamed for the controller. The setup hook
resolves/admit_root/freeze_startup_state and initializes admitted consumers;
supplier start runs in its own worker. Native-window construction is not WebKit
AX readiness, frontend render readiness, host readiness or supplier settlement.
The allow_operational branch still controls operational consumer initialization.
No new UI-ready flag or authority shortcut was added.

Bounded inspection of locked Tao0.35.2 macOS window and Wry0.55.1 wkwebview code
found ordinary native NSWindow/WebKit construction, with no project override
that establishes the application-self AX cause. No missing entitlement, TCC
denial, timing cause or OS/App fault is inferred. The already-prepared same-
reference typed discriminator remains the pending observation; it is held while
the owner is away because autonomous recovery is not proven. These product
parenting fixes are independently useful and are not claimed to solve that
unmeasured AX representation issue.

## Verification and delivery boundaries

Offline Rust unit compilation used copied existing registry/target caches in
app-native-window-unit-fNamafSD, normal shared wrapper admission/jobs2 and a fresh
scratch Codex home. No App bundle was built or launched; the old candidate/cache
sources were not mutated. Tauri's dev-only test feature supplies MockRuntime;
production dependency pins/features and Cargo.lock are unchanged.

38 targeted tests passed:2 real Tauri mock-manager window-selection cases
(auxiliary/main in both insertion orders; missing main never substitutes aux),
12 desktop setup parent/save tests including the new picker-kind and selected-
result/cancellation guards,6 lifecycle parent/result tests and18 Quit tests.
Mocks establish source behavior and refusal semantics, not native UI operation.
The native picker/window effect, AX hierarchy and actual cancellation on hardware
remain unobserved. Independent Astra MEDIUM scrutiny covers the changed native
presentation/IPC-invoker boundary before parent integration; no completed review
is repeated solely for the updated model policy.

Existing DEL01-02 window/Quit and DEL01-04 setup/presentation commitments remain
unchanged. This DEL09-02 source contribution records the implementation correction
and receiving limits; it does not grant native qualification, publication or a
candidate identity change. Parent owns integration and future candidate/runtime
selection. Owner actions, signing, recovery exceptions and publication remain
separate authority.

Independent Astra MEDIUM review completed at
4e942918f1fc4e99140665b2cbb36024c937255e against
3f7974bcfac00a6a246c17b6c282657e4f352c40, with no actionable findings.
The reviewer independently reran the2 mock-manager window tests and2 picker
regressions; all4 passed and diff-check was clean. The broader38-test result
above is the manager's verification, not attributed to the reviewer. Native
hardware lifetime/cancellation/AX behavior remains unqualified. Hosted exact-head
checks and parent integration remain required; candidate/diagnostic holds stand.

CI follow-up:4970534a failed the pinned package/EXP/SQ receiving cohort because
the dev-only Tauri test feature changed Cargo.toml bytes. The maintained
app/examination/package_receiving/generate.py regenerated only its four outputs:
package source profile/adapter constant and SQ package pins/reader constant.
The source delta is Cargo.toml's exact digest plus derived digests; no validator,
legacy cohort, historical evidence or candidate identity was relaxed/rewritten.
All41 targeted package-successor and joined receiving tests passed offline.
Actual maina6800aa35cdb269eaa268517dedbeae27bd9eb4b (PR84 frontend slice) was
normally merged before generation. The four Rust/product files are byte-identical
to reviewed4970534a; picker IPC payload/result/titles remain compatible. No
unchanged Rust tests or independent reviews were repeated for this pin repair.
