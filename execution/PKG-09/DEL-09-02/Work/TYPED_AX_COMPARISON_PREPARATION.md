# Small typed AX comparison and post-am98 recovery assessment

Preparation only; no further App launch or live AX read is authorized. PR48's
actual evidence/audit remains separate. The parent accepted the review advisory:
passed A with the same base reader, distinct B menu objects and agreement across
existing B readers already make a general ctypes bug unlikely. This component
is a lower-priority residual check, not an assumed product fix or a new framework.

## Prioritized post-am98 state

A fresh read-only projection is retained at
`/Users/ryan/dev/chirality-t3/scratch/app-typed-ax-prep-hz419ka_/post-am98-runtime-assessment.json`.
It did not reuse or rewrite the three-row basis. Current App-ledger SHA256 is
`2d09bb9af4a653c3eca7fc663f32096664f2dfd2fd1307c07fa38f12bb4b164c`.
There are six schema-valid rows: two sessions, each start/empty-work Quit request/
`session_ended` marked `quit` with empty stop requests. Latest start12:06:30.670Z
reads prior end `clean`; latest Quit12:07:21.748Z and end12:07:22.022Z. No other
ledger kinds occur. Exact saved A request remains unchanged. Before/after
read-only immutable/query-only checks found no App WAL/SHM/journal or observed
open DB descriptor and the hash/mtime stayed unchanged. This is bounded
current-user observation, not atomic exclusion of every possible writer.

Only metadata was read for supplier files. Relative to the pre-am98 basis,
additional goals WAL and state SHM/WAL files exist; logs/queue/tmp metadata and
WebKit statistics database metadata changed. Project and shared-skills metadata
are unchanged. App ledger/runtime and record-index directory metadata changed.
These are actual observations to account for, not automatically admitted future
state. No supplier SQLite, authentication, key or installed-skill contents were
read. All earlier projections, prepared attempts and scratch remain retained.

In retained `fdcf608f`, `RecoveryLedger::start_session_inner` classifies the last
matching quit end without a confirmed live-work answer as `clean`, appends a
new session marker, then closes earlier listed request/stop records. With these
six rows there are no `register_entry_summary`, `stop_request` or
`conversation_index` targets for RQ06/SR08/conversation recovery. `runtime_session`
initializes the reviewed ledger and starts the supplier through the existing
saved-request path; recovery history failure is reported rather than silently
replaced. These functions are byte-unchanged between fdcf608f and684e046a.
A future launch would still write its own session/records and start the supplier;
empty App history does not prove absence of unrecorded supplier state, a live
generation, LT23 or exhaustive settlement. The earlier fixed three-row v1
admission must refuse this changed database; no relaxed/new admission is created
by this assessment.

## Source-grounded A/B comparison

A started the same identified bundle with no saved request, showed the setup
form, saved it, and quit. B admitted that saved request, seeded operational
instructions/records/recovery and started the supplier. Later B runs carried
forward App and supplier/WebKit metadata. All use the same configured main
window/title; A and B both deny network and personal Codex-home access. A denies
fork and admits only App exec; B admits fork and exact App/Codex/mktemp exec,
and later B profiles isolate operator control files. The App's fixed environment
and project are bound; B uses a fresh fallback/tmp while retaining saved account
and shared inputs. No undocumented activation step was found in A's launch path.
A's recorded Python3.13.14 path and B's Python3.13 path currently resolve to the
same executable/hash; that current check is not a newly reconstructed historical
binary attestation for A.

Tao0.35.2 constructs a TaoWindow subclass through NSWindow's
`initWithContentRect:styleMask:backing:defer:` with deferNO and sets the title.
Its explicit class overrides are focusability for canBecomeMain/KeyWindow and
sendEvent (including a window-drag case), not accessibility methods. The bounded
Tao/Wry macOS and Tauri/runtime-Wry source searches found no explicit override
explaining the observed Application-as-window reference. The application hides
only on CloseRequested and shows on Reopen; neither action was issued to cure B.
WindowServer already proves the owned main window existed on-screen, and menus
were accessible. That does not prove native accessibility exposure or WebKit
content behavior, nor does absence of an override prove framework correctness.
No source-grounded product repair or more discriminating *nonintrusive* native
observation was established. App-side NSWindow accessibility instrumentation
would require a changed candidate and a separately scoped observation; it is
not introduced here merely to obtain another window-existence result.

## Prepared C boundary

`typed_ax/reader.c` directly calls SDK-typed AX functions and CF conversion APIs.
Its only observation entrypoint receives an AX application reference retained
by the keeper wrapper. The wrapper creates that reference from the original
retained Child's PID after its identity/reservation checks; C creates no AX
object and accepts no PID. It accepts no PID, creates no application/global AX
object, and performs no action, WindowServer read, image capture or permission
request. It derives the root PID with GetPid, checks every reference's owner
before role content, suppresses foreign PID/role data, tracks duplicate/self
references without recursion, and uses four fixed attributes with64 references
maximum each. Owned Create/Copy values are released; borrowed array items are
used only while the copied array remains retained. Per-element timeout0.5s and
an inter-call3s deadline bound ordinary work, not a hard cancellation guarantee.
Raw AX codes and CF type IDs are distinct from internal observation statuses;
INT32_MIN means a call was not attempted, not an AX return code.

`native_b_typed_ax.py` validates a source/build manifest bound inside the actual
admission, then invokes the local library only after retained-Child WNOWAIT and
kernel birth/path/parent/UID/executable-hash checks. It compares Python against
the same local app reference used by C, with identity rechecks between and after
the readers. The Python reference reader accepts an optional precreated app
reference and fixed-attribute subset; its default behavior is unchanged. The C decoder does not call Python
conversion code. A stop/evidence reason or less than57s headroom refuses entry;
Python gets a4s inter-call budget. Python attributes are captured separately, so one attribute refusal does not
erase earlier pairs or the C section. C reports per-reference errors; Python
can still refuse an entire attribute, so anomalous references may lack a paired
value. Other Python/decode exceptions are recorded with the C result/header
rather than silently replacing it. Failed C role conversion clears its text;
UTF8 replacement is not claimed as complete role text.
Sequential observations are not atomic; neither agreement nor disagreement
alone establishes a product/OS cause or qualification. An in-process C/FFI
fault can kill the keeper holding the original Child reservation and cleanup
authority. Headroom/timeouts do not cover a crash; no safe observer-release
claim follows from it. That residual risk must be included in any live disposition.
`completed` means traversal completed, even when attributes report errors; it
does not mean observation success or qualification.

Staging requires an externally supplied reviewed build-manifest SHA256 and the
exact production source set (no empty/self-selected source list or fixture
files). The builder hashes sources and selected headers before and after
compilation, refusing observed drift. Before a future admission, the checked
library and a source-bound manifest must
be copied write-once into its private controller root. Capture requires that
manifest use `typed-ax-build.json` and its library `typed-ax-reader.dylib` inside
the root, and that the admitted sandbox policy retain the control-root denial.
It cannot load from App-writable output filenames. The component checks the
policy hash and required denial; live integration must retain the launch
controller's exact `policy(value, root)` comparison, not treat a substring check
as a general SBPL policy validator. The supplier-writable build tree is not a valid
live-load location. Staging loads no library and refuses an existing admission.
The source/build manifest records compiler binary/hash/version, SDK identity and selected direct API/type/attribute header
hashes (including AXAttributeConstants.h, not the entire transitive SDK), source
hashes, command/environment, times and dylib hash. Offline builds
run through the existing slot/memguard wrapper, with fresh scratch Codex home;
no download, App rebuild or manual signing occurs. Production exports only the
reference-based comparison and its output-size query. Harmless test builds
replace AX functions at compile time with SDK-typed fake functions on owned CF
dictionaries/arrays. Symbol inspection confirms the fixture imports no real
AXUIElement functions; production has the direct SDK imports. Tests cover raw
errors, wrong types, bounds, ownership exclusion, cycles/duplicates, per-object
timeout-setting refusal, retain-count stability, fixed POD ABI and keeper/admission
refusals. Added fixtures exercise the inter-call deadline, null/wrong/oversize
roles and foreign-PID exclusion; the final compiled run passed as recorded below.
Absolute source hashes fail safe if the worktree changes or disappears; they
check disk bytes, not already-imported Python module memory.

Retained earlier build (superseded for live use after protected-staging changes):
`/Users/ryan/dev/chirality-t3/scratch/app-typed-ax-prep-hz419ka_/build-2`.
Reader manifest SHA256:
`e7c924ef662d345fb92f0ae9c4c5479a9992454b6c994c5ade3d9b2472dab4b5`;
reader dylib SHA256:
`5cefa96fd60215dc01a6bae09481165579b75db19147885d9bd57e8302a2aeca`.
Apple clang21.0.0 compiled the production library; it has not been invoked.
Build1 and build2 each completed ten passing tests. A correction record
distinguishes an initially premature build2 test attribution from its later
actual completion. Those runs preceded the review fixes; the final build3/checks below supersede
them for source-binding and fixture coverage without deleting their records.

## Minimal future profile and remaining conditions

The component is not wired into the current launch controller or an executable
admission. This is deliberate preparation separation, not a live-ready claim.
A future selected profile would admit exact post-am98 six-row/source/metadata
state under a new identity, bind the typed library manifest in its inputs, and
call the comparison once from the existing keeper after readiness observation
fails or succeeds, replacing the already-satisfied WindowServer diagnostic.
Known-source cleanup and the exact failed-qualification original-Child release
stay unchanged; no new cleanup authority is supplied by this reader.

If C agrees with Python later, it adds evidence against a condition-dependent
client-decoding issue, not proof of an App/OS cause. If they differ, compare the
exact observations and timestamps before any product repair. Independent
Claude Opus5.5/high scrutiny of this new observation boundary is required before
returning it for a parent's separate live disposition. No current launch, reset,
permission change, supplier/model/auth/network action or candidate rebuild is
implied by this prepared component or its ordinary tests.

Independent Claude Opus5.5/high review of `3200f17d` found no blocking C
observation defect, with the boundary unwired. Its staging-trust, fixed-name,
partial-result, role-text, provenance, test and documentation findings are
addressed in the subsequent bounded delta. Existing build1/2 records are
historical. Final build3 and the compiled-fixture checks were subsequently
verified below. No clean repeat review or live-ready admission is claimed.

## Final checked preparation after review fixes

Guarded offline build3 completed with source and selected-header hashes stable
before/after compilation. Its source digests match the final fixed files:
`/Users/ryan/dev/chirality-t3/scratch/app-typed-ax-prep-hz419ka_/build-3`.
Production manifest SHA256:
`efde5fc5fdb1345db2fabef1180778013c5a5a27f4a5b25a1e0979ce44352bc0`;
production library SHA256:
`3d9e0587df7ee52aede244b8760e874ace66623e62124d16edc1c2a29150ad5d`.
All18 tests passed against that build:14 mocked binding/staging/error cases and
4 compiled harmless CF/fake-AX cases. The13 reference-reader tests also passed.
Production symbol inspection finds only the comparison and size-query exports;
fixture imports contain no actual AXUIElement functions. The production dylib
has never been loaded or invoked.

Using the explicitly selected manifest hash above, staging passed without native
loading into `/Users/ryan/dev/chirality-t3/scratch/app-typed-ax-staging-patgfy2p`.
The protected `typed-ax-build.json` digest is
`a9067c5c9fe2bffc1f5da51bc56bfe902ade78fdd851fd0fb3d4acaabdc8118a`.
The fixed-name library copy is plain owned0600. No admission.json or launch was
created there. Exact commands, compiler/SDK/header/source identities and final
verification remain in the retained build3 records. Live library-validation
acceptance, load timing and real AX behavior remain unobserved. A future use
still needs a new post-am98 admission identity, exact controller-policy check,
once-only integration and the parent's separate live disposition.
