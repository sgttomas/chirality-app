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
