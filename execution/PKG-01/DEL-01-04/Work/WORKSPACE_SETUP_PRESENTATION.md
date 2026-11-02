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
