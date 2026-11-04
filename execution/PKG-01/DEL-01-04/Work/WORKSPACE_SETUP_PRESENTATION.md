# Workspace setup and navigation presentation

Owner-directed frontend slice on App main `3f7974bcfac00a6a246c17b6c282657e4f352c40`.
The existing workspace keeps conversation and workflow panes, existing controls
and their mounted state. This contribution applies the selected v3 light visual
identity and makes first setup, review, connection status and keyboard movement
usable. It is not a native journey result or a replacement for those panes'
remaining product work. Candidate `1f67d3822b-8c83d74ae3ce` remains historical;
no installed v3 binary or current candidate identity is inferred from source.

## Selected v3 source and assets

Actual read source: shared Chirality Git
`485051eac923c759238948a54cd7bb094eee4899`, under
`projects/chirality-app-dev/frontend/src/`. No maintenance-head substitution.
Read extents: `app/globals.css` lines 1–155 (light tokens and explicit theme
standing), `app/layout.tsx` 1–110 (local font families/weights and fallbacks),
`components/shell/app-shell.tsx` 1–95 (pane composition),
`components/shell/shell-frame.tsx` 1–70 (compact shell/control disclosure),
`components/shell/folder-select.tsx` 1–100 (native picker, pending/explicit path,
Escape focus return). This is presentation/asset reuse, not adoption of v3's
runtime, persistence, themes or retired tools. Root is never a build/test dependency.

The exact ten existing IBM Plex WOFF2 assets and OFL license are copied unchanged
into `app/src/fonts/`. Light is the existing primary v3 theme; the selected warm
ground/surface/ink/rules/accent/CTA tokens and Sans/Serif/Mono families retain
that identity. No generated artwork, new palette, network font, brand icon
replacement or automatic dark-theme choice. Existing v4 bundled icons/resources
are untouched. `workspace.css` supplies local font faces; the entry HTML links
the retained license as a build asset. Exact asset hashes follow below.

## Interaction and authority

- Setup has two labelled field groups and a live next-step explanation tied to
  the disabled Review button. The existing accessible control names stay intact.
  Typed paths and native picker bytes remain distinct; no path/home discovery or
  implicit model/provider/account choice is added.
- Review announces checking, then focuses its heading. Edit setup choices or
  Escape dismisses only that local preview, preserves choices and focuses Review.
  During native confirmation these local dismissal controls are unavailable;
  Escape is not intercepted as a native Cancel or permission to end a question.
- Pending picker/review/save operations disable input and announce their stage.
  A synchronous in-flight guard prevents duplicate retained-click dispatches.
  Unmounted completion does not publish UI state; explicit field edits invalidate
  a preview. Errors retain actual host text and focus an alert; successful save
  reports next-launch standing only. Native cancellation cannot fabricate a save.
- Resource/source diagnostics remain available in a disclosure. Current custody
  or resource-reading problems stay visible outside it. No host refusal is
  removed. The connection overview reports the supplied host state, distinguishes
  closed generations from ready, and links to existing controls. It performs no
  IPC and supplies no supplier/authentication/admission or qualification claim.
- Workspace anchors open existing disclosures, focus the summary/destination and
  scroll there. They neither remount panes nor change current conversation,
  workflow selection, unsent text or prepared message target. Existing internal
  reveal calls keep their non-focusing behavior unless explicitly requested.

The existing `desktop_setup_pick`, `desktop_setup_preview`,
`desktop_setup_project_preview` and `desktop_setup_prepare` IPC shapes are
unchanged. Host preview tokens, original-window confirmation, custody checks,
persistence and next-launch admission remain authoritative. No Rust/lifecycle/
SEAL-C/native-controller change, file write from the webview, hidden test command,
sign-in or auto-start. Scope/needs in DEL-01-04 and DEL-01-05 retain their existing
meaning; their existing code/test ownership covers the changed controls.

## Verification and limits

Maintained Node miniDOM tests mount actual React components and consume packets
from the executed Rust `desktop_startup::tests::mounted_setup_packets` producer.
They check exact IPC arguments, confirmation token, pending-only save, native
refusal/cancel, picker cancellation, lossless paths, review/edit/Escape focus,
loading/disabled reasons and duplicate-click prevention. Navigation tests retain
A/C/B/D selection and composer guards while checking destination focus and
reported connection states without new commands. Focus instrumentation checks
which mounted element receives `focus()`; miniDOM provides no layout, real
keyboard dispatch or macOS accessibility-tree qualification.

Offline TypeScript/Vite build checks and asset/license correspondence accompany
these source tests. No browser, native App, screenshot capture, model, account,
keychain, signing, download or VM operation was performed. A later identified
candidate must still verify visual layout, font rendering, native focus and
screen-reader/keyboard behavior. This source change does not claim those passes.

## Retained font asset correspondence

| File | Bytes | SHA256 |
|---|---:|---|
| `LICENSE-IBM-Plex-OFL.txt` | 4429 | `d0283623ef57e722fd0eb688a8041589670c608ab780cd3612d06ba6f153d3fd` |
| `ibm-plex-mono-latin-400-normal.woff2` | 14708 | `08949f728dc52d528e69b1667d15c89a5686a4ee9a296ff90983985f99c380f7` |
| `ibm-plex-mono-latin-500-normal.woff2` | 14888 | `01d285447409c8a588692162439a038b8cbd7871309ee20267b0d2d91c6e8e22` |
| `ibm-plex-sans-latin-400-italic.woff2` | 24356 | `6de912e531b6c98084f1b2d5e5a91bad77be4e68bc4e396e43c46fc435e5f3d9` |
| `ibm-plex-sans-latin-400-normal.woff2` | 22588 | `3b646991d30055a93a4ecc499713d4347953a74a947ecab435ab72070cbdab0e` |
| `ibm-plex-sans-latin-500-normal.woff2` | 24184 | `0717336fb31fcdcde4b8deb3675bb4a0f7f6d484864afcd6751ac29975962203` |
| `ibm-plex-sans-latin-600-normal.woff2` | 24252 | `8960851d691c054ed38e259bdcf1a6190d157b4203ed5bb32c632a863fb8ec2f` |
| `ibm-plex-sans-latin-700-normal.woff2` | 22832 | `42e7b0c143c19df9d99fd896e76b48f846edf0902d200bc29796b34d12c33aa7` |
| `ibm-plex-serif-latin-400-italic.woff2` | 20900 | `d3f861b1ca55e50ca94de4c1756cb0d67c73de615172adf6b5b2078d939c723a` |
| `ibm-plex-serif-latin-400-normal.woff2` | 19580 | `cb2c5eee2c0a43ff30d2365407c7bc8b20e3bd90720a4a64102ba0b328022a02` |
| `ibm-plex-serif-latin-600-normal.woff2` | 20516 | `e279e4f8baa0d4634d98868092f2198ae0dcd9e142c935822c385b9843352a9b` |

Local verification: 82 maintained Node tests passed (desktop setup 11,
prepared-message/navigation 67, workflow selection 4), including one real Rust
setup-packet producer test; zero skips. TypeScript and Vite production build pass
with the existing >500 kB chunk warning. Every emitted WOFF2 and linked OFL
license matches its retained source bytes. Deliverable structure has zero errors;
whitespace checks pass. Native owner's separately coordinated picker-parenting
work preserves the same `{kind}` / null-or-location interface; no frontend
assumption about which native window is selected is added here.

## Find and inspect a past conversation

Next frontend slice on integrated App `a6800aa35cdb269eaa268517dedbeae27bd9eb4b`.
The previous PR84 assets, palette and exact v3 source remain unchanged. Additional
v3 source inspected at the same Root `485051eac923c759238948a54cd7bb094eee4899`:
`components/shell/workspace-sidebar.tsx` lines 1–70 and
`components/shell/session-list-view.tsx` lines 1–165. The former places Sessions
and Transcript in the workspace; the latter supplies explicit empty/loading/
error/opening presentation. This adopts presentation lessons only. Its v3
runtime event-buffer hydration and automatic list reads are not v4 contracts.

The current v4 history route gains a direct **History** workspace link, opening
and focusing the existing disclosure while preserving every mounted pane.
**Find in received conversations** filters only currently supplied IDs and
previews, case-insensitively. It neither reads disk nor fetches another page,
selects a conversation nor resumes it. Counts explicitly cover received rows,
not all saved history. No-match/empty-list states explain the next explicit
read. The selected conversation stays in the chooser even outside the filter
or current received list, clearly labelled; it is not silently replaced by a
matching row. Clear search restores the full received list and input focus.
The filter persists across same-source polls and inspection choices, resets on
home/generation change, and is not persisted to storage.

Read, inspection and Continue retain distinct controls and existing exact IPC
arguments. Pending operations now name the requested read/selection/continuation
and mark the region busy; unavailable-source guidance explains disabled reads.
The existing duplicate-operation guard remains in force. A failed list refresh
explicitly identifies retained observations; the original source error remains
in the unchanged diagnostic details. Paged buttons have stream-specific accessible
names while preserving their existing text and exact cursor/direction/reference
bindings. Conversation source/role metadata moves into a disclosure; current
receiving limits, original guidance notices and resume consequences remain visible.

No change to `historyPageBinding`, stream acceptance, resume ticket/admission,
observer currency or navigation checks, original role standing, host authority,
persistence or native code. A successful history read never becomes an active
conversation. Continue still needs its matched original native resume, and never
automatically resends text or overwrites the current draft/model/access choice.
No interaction is inferred merely from filtering, rendering, focusing or a
closed/reopened disclosure. PR85 retains native integration priority and has no
frontend overlap; no receiving pin changes are made here.

Verification uses the existing native-history, history-continue-navigation and
prepared-message-navigation Node suites: 122 tests passed, zero skips. New cases
exercise local search, unchanged host data/IPC, exact selection request, source
reset, retained selected row, clear focus, pending/error/no-retry and direct
History navigation. Existing accepted-page, cursor and Continue source/epoch/
request/race/refusal guards remain covered. These tests mount production React
with controlled host-shaped packets; this slice does not claim a newly executed
Rust producer, actual native history or a candidate walkthrough. TypeScript/Vite
and structure/whitespace checks accompany the contribution; real layout/keyboard/
AX/native focus remain unrun. All prior candidate/evidence identities remain intact.

## Explicit workflow discovery and draft creation

Next frontend slice on App `446b06a501299316e3709b5103db1ec5d6e70d77`.
The exact v3 visual assets/tokens remain those already integrated by PR84.
Additional inspected source at Root `485051eac923c759238948a54cd7bb094eee4899`,
`projects/chirality-app-dev/frontend/src/components/woven-dialogue/`:
`workflows-view.tsx` lines 1–33 (complete file) and `workflow-draft-review.tsx`
lines 1–80. Their explicit content/read/review progress informs presentation;
v3 fetch, registration and runtime authority are not adopted.

Workflow studio now groups choosing content/library, creating a named draft,
and trying/reviewing drafts in that order. Create moves before the draft list,
with its current prerequisite and opened destination adjacent. Its name begins
empty instead of implicitly proposing `coordinated-knowledge-work` for every
source. Empty/whitespace-only names disable Create; all other submitted text
is preserved exactly for the host's existing validation, not trimmed/rewritten.
No inspected name, catalogue entry, revision or conversation is auto-selected.
Exact-revision/in-place operations remain under an Advanced disclosure and use
the same explicitly entered name; normal draft review remains in the draft list.
Original labels, source/role notices, actual review text and native confirmation
controls are retained. This introduces no new path, library, registration,
selection or persistence contract.

A synchronous local in-flight guard prevents repeated retained callbacks from
issuing another workflow operation before the original command and observation
finish. The panel announces the pending stage and marks its region busy. The
original operation still captures exact `workflowArguments` before awaiting,
returns the unchanged host value, reports its original relation, and performs
the existing single original-context draft observation after Create/Refine.
A failed observation remains a separate limit and cannot turn original success
into an invitation to duplicate the write. Refusal releases the local guard;
there is no retry, queue, native-confirmation shortcut or webview filesystem
write. Native host validation remains the authority even if a stale callback
has retained earlier values.

Verification: 94 maintained Node tests passed, zero skipped, across
workflow-library, workflow-action-result, library-entries and prepared-message-
navigation suites. The maintained action-result and library-entry suites execute
their existing Rust source producers with invented filesystem/host fixtures;
this is not App/native/model execution. New checks require explicit names,
retain exact submitted text/context, verify missing-prerequisite messages and
prove duplicate Create callbacks cannot issue a second mutation while the
original view read is pending. Existing original-result/failed-observation,
source-switch, registration, selection and independent-composer cases remain.
TypeScript/Vite, structure and whitespace checks accompany the slice. The
user manual now follows these actual stages. Real visual/native/keyboard/AX
verification and all historical candidate limits remain unchanged.

## Ordinary conversation readiness and effective interruption

Source basis App `509e7cc1bc9da55e296934bf6843a69f6c8437f8`. The current
ConversationPanel offered Interrupt while `codexBusy` was true and explicitly
said that turn interruption remained available during Stop/Restart. Its handler
nevertheless returned on the combined send `busy` flag, silently doing nothing.
The existing codex-controls test checked the button/source text, not the handler
under that condition. This slice repairs that demonstrated frontend mismatch.

`interruptTurn` now uses the panel's own pending state plus the current source,
selected/live turn, duplicate-request and synchronous control-pending checks.
The button also refuses a closed generation. A process-operation busy flag alone
continues to pause Send/Steer/attachments but no longer nullifies the offered
turn-interrupt action. It neither confirms nor dismisses the native lifecycle
question. The unchanged parent `conversationAction` retains original-source
request/observer currency; Rust `lib.rs::conversation_interrupt` resolves the
actual generation and `runtime_session::interrupt_conversation_turn` rechecks
current conversation, live observation and existing interruption records before
dispatch. No host guard, lifecycle policy, timeout, receipt or IPC is altered.

Ordinary Send now has a nearby live readiness message and accessible description:
connection, conversation selection, pending operation, empty text or ready target.
The existing exact draft/model lifetime and send outcome rules remain. Links to
connection/new/history destinations only reveal existing panels. Interruption
has its own grouped live-turn selector and status explaining unavailable source,
pending own operation, absent live observation, missing choice, already requested
or ready. Unknown/acknowledged/ended remain distinct; no workflow-run or child-
settlement claim follows. Existing v3 palette/assets and historical candidates
remain unchanged; no diagnostics-first route or new framework is introduced.

Targeted maintained conversation-panel/codex-controls/prepared-message-navigation
regressions exercise the actual React handler during process busy, exact target
arguments, duplicate callback refusal, preserved draft, closed source/no live
turn/already-requested refusal and readiness messages. These are controlled
source-level packets, not native interruption or App execution. Test/build jobs
are admitted through the shared slot wrapper; actual results are recorded in
the PR, not inferred from code inspection. Real visual/keyboard/AX/native focus
and recovery qualification remain unrun; the recovery hold is unchanged.

After shared-slot admission, all 152 focused Node tests pass with zero skips;
TypeScript/Vite production build passes with the existing chunk warning. The
first run exposed a pre-existing codex-controls source-text assertion requiring
`codexBusy` to be the first JSX prop. Main already placed other props before it.
The bounded test repair checks the actual `ConversationPanel` JSX attribute via
the existing TypeScript parser, retaining the exact `processBusy` binding check
without depending on formatting/order. No product code changed for that repair.
Independent Astra/medium source review of `16547e68` found no actionable defects;
it inspected source/host guards before the queued checks ran and claims no
independent runtime pass. The later test repair and passing run are manager
verification, not an invented repeat review.

## One pending ordinary turn submission

Integrated-source inspection at `3b964e650179b79937a7c568f310af2c1fe44072`
found a concrete adjacent gap: `attachmentText` relied only on React busy state,
so two deliveries of the original attachment callback before a render invoked
its submission twice. The new maintained regression failed on the original
source with **2 dispatches, expected 1**, using the existing actual Rust-produced
attachment snapshot and result in mounted React. Its original failure log is
retained in the task scratch. This is a demonstrated source defect, not a claim
that a real user/native session duplicated a turn.

ConversationPanel now shares one synchronous ref among ordinary text (including
plan/default), steering, ordered-attachment Send/Steer and turn interruption.
The first operation owns that guard through its command and existing optional
observer read; repeated or competing retained callbacks return without another
dispatch. Success or refusal releases it only after that sequence completes.
This is a small replacement of the separate local refs, not a new queue,
framework, persistence store or host-wide exclusion claim. Other workflow/role/
trial controls retain their own contracts and existing busy presentation.

Steering/attachment handlers and plan/steering/attachment button readiness also
use the same current-source condition as Send and Interrupt, including closed
generations. An offered closed-source plan send can no longer silently reach
an ordinary handler that refuses it, and direct attachment/steering deliveries
refuse that closed source before dispatch. Native generation/selection/custody/
ordered-list/target/reply revalidation remains unchanged and authoritative.
No submitted payload is transformed; acknowledgment, pending/late reply,
observer failure and original-source result standing remain separate. The PR88
exception for an observed live-turn interrupt during process-only busy remains,
subject to source readiness and no pending operation in these turn controls.

Verification: 108 maintained Node tests pass, zero skips, across attachment-
outcome, conversation-panel, codex-controls and plan-mode. The attachment suite
executes its existing Rust fixture producer; mounted timing controls test
pre-render duplicates, competing controls, guard retention through observer
completion and closed-source refusal. Existing exact ordered refs/owner/revision,
source switches, late acknowledgments, native errors and immutable original
outcomes remain covered. TypeScript/Vite, structure and whitespace checks
accompany the source. No visuals/assets, Rust, IPC, native lifecycle policy or
pins change. Real layout/keyboard/AX/native recovery verification is still
blocked by the hold; no App/browser/model/auth/signing/download/VM action or
historical candidate relabelling is inferred from these source tests.

## Setup prerequisites in product language (J1 increment)

Owner direction of 2026-11-03 sets publication journey J1 (DEL-02-02
`Work/PUBLICATION_JOURNEYS.md`): setup must explain the required settings and
access, and a missing prerequisite must name a concrete next action. Before
any choice is saved, Desktop setup now says in plain words what the App needs:

- its own new, empty sign-in folder (the native preview's "Create new account
  directory"), with no credential import or reuse from other Codex tools, and
  sign-in under Connection & access after reopening;
- the person's existing Codex `config.toml`, `AGENTS.md` and skills folder,
  which the App links to rather than copies (the preview's "Create … link"
  effects), so other Codex tools read the same files;
- an optional project folder, where the project's workflows (its `.chirality`
  folder) are kept and where runs write results.

It also states the next-launch consequence: quit and reopen, while the current
window keeps working until then. The action, project and supplier options and
the two group legends use product words ("First-time setup…", "Keep my current
sign-in; change only the project", "No project for now", "Codex included with
the App (development build, not yet qualified)"). Option values, accessible
control names, IPC, preview effects, native confirmation and persistence are
unchanged. The explanation describes the existing native preview; it creates
no default, path or write. The setup disclosure gains id `desktop-setup`, so the
J1 guide's "Choose a project in Desktop setup" link reveals it without a command.

Checked by the maintained `desktop-setup` mounted tests (unchanged option
values and labels) and `run-journey` link checks. Whether a person understands
this wording on the signed candidate is unobserved; that remains native J1
evidence for DEL-09-02.

## Composer offer for an App-composed request (J2 increment)

The ordinary conversation composer accepts one App-composed message offer
(`ComposerOffer`: sequence, exact generation/thread key, text), used by DEL-02-02's
Make a workflow guide. An offer applies once, only when the composer's own
conversation is selected. It fills the text only when the composer is empty;
otherwise the person's unsent text is kept and "Replace my text with the
request" or "Discard the request" is offered. Applying or holding an offer
reveals the conversation. The offer never sends, never changes model, mode,
attachments or steering, and adds no IPC; Send keeps its existing readiness,
single-submission and outcome behavior. Checked by `app/tests/make-journey.test.mjs`
against the mounted `ConversationPanel`.

## New conversation: route, model list, advanced IDs

The New conversation section now reads as **1. How it connects** (an explicit
built-in route button for the active home, beside the existing configured
local-provider read and choice), **2. Model** ("Read available models", the
reported list with display names, IDs, descriptions, a "Codex's default" label
and explicit "Use ‹name›" choices), and **Advanced: enter IDs yourself** holding
the unchanged model, provider and access-entry fields. Meaning, native read and
choice rules are in DEL-01-05 `ACCOUNT_AND_PROVIDER_ACCESS.md` ("Explicit route
and model discovery for a new conversation"). Role choice, the choice summary,
Start and its disabled conditions are unchanged. The first-use mounted check in
`app/tests/prepared-message-navigation.test.mjs` now expects the route and model
list to be shown and the manual IDs to sit in the closed Advanced disclosure.

## First use: a focused welcome while setup is required

The owner's first use of signed candidate `fe811788` ("I don't understand what
I'm looking at?") showed the full workspace with nine equal links, a window
titled "walking skeleton", and setup asking for an explicit action, three raw
shared paths, a project mode and a single-option supplier, beside unavailable
keep-account diagnostics.

While `desktopSetup.launch.state` is `setup-required`, the App now shows only
**Welcome to Chirality** (`app/src/FirstUse.tsx`); the workspace stays mounted
but hidden, the native-confirmation content stays visible and the waiting
bridge stays mounted. The welcome asks, in order:

1. **Your project folder** — "Choose project folder…" (native picker) or
   "Continue without a project".
2. **Codex settings** — "Start with new settings" (recommended; DEL-01-05 "First-use
   setup with new App-owned settings") or "Use my existing Codex settings",
   which then shows three Choose…/path fields for the existing files. "Keep my
   current sign-in and settings" appears only when the host reports it
   available.
3. **Review and confirm** — "Review setup" shows the host's own effects;
   "‹host action›…" opens the native confirmation; "Change my choices" or
   Escape discards only the local review. A cancelled dialog keeps the choices.

Once saved, the welcome says to quit (⌘Q) and reopen, then sign in under
Connection & access and start a conversation. Launch state, App data, the
included Codex, an unavailable keep-account reason and resource limits are
under **Technical details**. No model, provider, sign-in, keychain or network
is chosen or touched. The ordinary Desktop setup panel (shown once admitted)
no longer has a supplier selector — the included Codex is fixed and named — and
no longer advises typing a path that does not exist. The window title is
"Chirality" (`tauri.conf.json`); the development product name and identifier
are unchanged, and the supplier `clientInfo` title is not user-visible and is
unchanged.

Checks: three mounted tests in `app/tests/desktop-setup.test.mjs` with the
executed Rust packets (new-settings journey with exact IPC; no-project,
existing-settings, cancel and change; the mounted App showing only the welcome
while setup is required and the workspace once admitted) plus the updated
existing setup tests. No native window, AX, layout or person act is observed.

### Local rendered self-test of the welcome (owner steer, 2026-11-03)

The owner asked for substantially more of our own testing before involving
them, with signed rebuilds reserved for when their direction is needed. The
welcome was therefore rendered from the production bundle (`vite build`) in
the locally cached headless Chromium, driven over the DevTools protocol at
1100×800 (the App window) and 480×860. A synthetic IPC peer answered with the
packets the executed Rust producer `mounted_setup_packets` emitted; the native
picker and confirmation were simulated (immediate synthetic results, marked as
such), so no real dialog, home, settings, model or sign-in was involved. Flows
captured privately in scratch: first screen, project chosen, new-settings
review, saved, saved with details; existing-settings route and review;
dialog cancelled; save error.

Found and fixed in the same change: the review was dominated by long internal
paths (the new-settings effects are now plain statements, with the exact
locations in a host-supplied `locations` list under "Exact locations"; the
native statement still names every path); after saving, the intro still said
"First, choose…" (now only the next action shows); the existing-settings path
fields truncated the chosen paths (now wide enough). Paths elsewhere in effects
render in a quieter wrapping style. No horizontal overflow, unhandled IPC or raw
diagnostic outside Technical details was observed at either size.

Observed limits: the existing-settings route still reviews the host's original
technical effects (shared with the admitted Desktop setup panel); a focus ring
frames the review heading and messages after programmatic focus; fonts, macOS
window chrome, VoiceOver and the real native dialogs were not observed. This
rendered check is local evidence for the next development App test, not native
qualification or owner acceptance.

## Task views instead of one long page (Agent 0 decision, 2026-11-04)

The rendered self-test measured the admitted workspace at about 14–16k px:
every guide, the whole workflow studio, the conversation and every secondary
panel rendered inline. Agent 0 decided to address this now. The workspace
now shows one task view at a time from a small navigation — **Run a workflow**,
**Make a workflow**, **Conversation**, **History**, **Settings & tools** — with
`aria-current` on the active view. Every view stays mounted; an inactive view
is only `hidden`, so unsent text, exact selections, pending composers, offers
and review bindings survive switching. The detailed workflow studio is a
collapsed **Advanced: workflow studio** disclosure after the guides in both
workflow views. New conversation sits in the Conversation view; provider
administration, Desktop setup, connection, files, records, connectors and
diagnostics are in Settings & tools; History and recovery has its own view.
The waiting-request overview, requests outside the selected conversation, the
act control and native-confirmation content stay above the views, visible in
every view. No IPC, persistence, consent or authority changed.

Navigation that crosses views — Answer/Show the conversation, Put the request
in the conversation, prepared-message Open — sets its view in the same update
as its own state, so the following reveal finds its target visible; any other
reveal of a target in a hidden view first makes that view visible
(`registerWorkspaceViews`). Nav links point at the destination itself
(`#conversation`, `#workspace-history`, `#workspace-tools` or the guide), so a
link still opens and focuses it.

Conversation labels in the guides and the conversation chooser use a title or
preview only when the host row supplies one (live host rows currently carry
neither; the supplier's `Thread.name`/`preview` and `thread/name/set` exist at
0.160.0 but are not received into these rows), otherwise a session-local
"Conversation N" with the model second; the option value is unchanged and the
exact ID is under "Exact conversation ID". Nothing is persisted or invented.
The page title is "Chirality", matching the window title (native observation
of the web-area name).

Rendered self-test (production bundle, cached headless Chromium, real
`selected_chain` host status and draft row, labelled synthetic states) at
1100×800 and 480×860: each view measures about 0.8–2.1k px; unsent composer
text survives Conversation → Run → History → Conversation; Answer in the
conversation, Put the request and trial Open each land in the Conversation view
on their target; no horizontal overflow. Mounted tests in
`prepared-message-navigation.test.mjs` now reach controls through the
navigation as a person would and check hidden-but-mounted retention and
always-visible confirmation content; `workflow-action-result.test.mjs` locates
the studio by its section. Not observed: native window, VoiceOver, real dialogs
(the native dev-App run of `a6fbc9a8` and an unresolved blank-window startup
observation are with the native and runtime owners).

### Native development-App observations of the first-use welcome (2026-11-04)

The native qualification lane ran an automated dev build of PR #111 head
`a6fbc9a8` (full note: DEL-09-02 `Work/DEV_APP_NATIVE_OBSERVATIONS_20261104.md`,
PR #112). These are development-test facts, not acceptance.

Observed working: window title "Chirality"; the welcome renders with its three
numbered steps and "Start with new settings (recommended)" preselected; "Review
setup" stays disabled until a project choice is made; the accessibility tree
reads h1, the three h2 steps, buttons, a labelled radio group, Review and the
Technical details disclosure in order (AX structure, not VoiceOver); "Choose
project folder…" opens a native sheet parented to the window with the message
"Choose the project for the next App launch"; Cancel returns cleanly with
nothing chosen; Quit with the sheet open exits normally; no App data is written
before confirmation. The web area was still named "Chirality App v4" on that
build; `26a01ff9` sets the page title to "Chirality".

Not observed: a picker selection; the native confirmation statement and its
actions; "You're set up", the `shared-settings/settings-*` and `account-homes`
results and their modes; quit and reopen into the workspace; and the J1/J2 task
views and navigation of `623a6b8e`/`26a01ff9`, which were not launched natively.
Those remain unrun native product cases; the browser renders above are evidence
only for what they show.

Open observation, cause not isolated: when the App was launched inactive under
fully covering windows, the welcome painted at about 3 s and the same window was
blank by about 8 s, with no accessibility window exposed (runs 2–8); activation
attempts did not activate it. The GUI loop was closed at this capability limit.
No source bug is claimed or excluded, and no presentation workaround was made;
any cause belongs to the runtime owner's diagnosis.
