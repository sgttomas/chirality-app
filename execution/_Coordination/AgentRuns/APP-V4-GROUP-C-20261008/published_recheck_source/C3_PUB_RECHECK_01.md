# C3-PUB-RECHECK-01 — live published-entry inspection

PROPOSED named technical source selection for owning review before code release.
Basis9a82cbcf29c46bb6f722c074b5854de7ef470450. This is one joined read-only UI
slice, not a new carrier, TASK service, source mint, native witness or R2 store.
No N/S/D/T/Q, CAM identity/reset/retirement change or publication prerequisite.
Existing0.1–0.4 publication, full resolve/discovery and read-only0.5 remain unchanged.

## 1. Actual gap and minimal custody amendment

Current connector_materialization::Entry retains published outcome as JSON;
publish_with drops Payload including its Arc<ProjectRouteStore> after success.
Only recovery from an Attempt retains the store. Therefore current code does
NOT hold same-open-root published custody, and reading outcome JSON cannot supply it.

Propose private PublishedCustody {store: Arc<ProjectRouteStore>, reference:
BoundReference} on the SAME existing Entry. Populate it only from the actually
successful writer return and the payload's original store, before dropping the
full payload. Never deserialize from JSON, cold record, renderer path or a matching
file. No reopen-and-compare fallback is selected. Uncertain/refused/prepared/
cancelled entries get no PublishedCustody; existing Attempt recovery is separate.
If registry installation fails after the writer returned, do not fabricate an
admitted published entry or typed association from later matching JSON/bytes;
preserve the actual exceptional publication-result boundary.
Historical already-published entries without the new typed field are unavailable,
not reconstructed from their JSON. Process loss loses the typed handle.

One existing identity still costs one slot, including the64 lifetime maximum.
Arc cloning aliases one store/root descriptor rather than duplicating its file
descriptor. At worst64 confirmed entries retain64 distinct store root descriptors;
sharing actual store Arcs can reduce that count, never assumed. Retain compact
BoundReference metadata per entry, no account payload. Count reference strings,
ordered directory identities and Arc/storage objects in resource review; no exact
heap bound is inferred from slot count. An in-flight read holds its own Arc clone
until completion; temporary traversal/account descriptors close afterward.
FD exhaustion must report unavailable and preserve original publication outcome.
This resource addition needs exact Host/CRP review, not implicit source adoption.

## 2. Only token command, original root, unlocked IO

Proposed command `recheck_published_connector_draft(token,generation)` accepts ONLY
existing opaque strings. No caller-supplied path, binding, account ID, version,
project or bytes. The App resolves current explicit project context internally.
Registry validates token, original entry generation and published typed custody,
captures a genuine per-entry immutable publication/custody revision plus
same-entry Arc/reference under its lock, then
releases registry/source/App routing locks BEFORE filesystem IO. No Host/role
lock or callback is needed. A current source-session change alone does not erase
a genuine published outcome; the command is not a new source preparation.

Use actual source_project/AppState immutable workspace and explicit App project
context: known, unknown or mismatch. Compare its lossless path and opened-root
identity against the retained store. This is NOT Payload.association (Git binding),
source-session liveness or a new Git/source verification. A different project, replaced root, unknown token/generation
or missing typed custody refuses this read without altering original outcome.
Retaining rootfd does not assert the mutable path still names that root. Apply
store root/chain checks before AND after inspection. Concurrent rename limits
remain CRP's observed-directory-identity limits, not continuous-path containment.

After IO, re-lock briefly and revalidate token/generation/entry revision and same
typed custody before returning/updating the inspection projection. A changed
entry/actual project context invalidates the result as a stale command refusal;
never attach it to a new entry. Unrelated entry mutations, cancel or reconciliation
must not invalidate immutable published custody through a global registry revision.
UI likewise rejects a late response after selection/project/request changes.
Do not hold a mutex across IO to solve that race. Use the actual immutable workspace/context owner, not a fictional project epoch.
If a later integration permits context mutation, it must expose its actual owner
revision for before/after checking. Exact per-entry custody revision and
project-context cut need code review; source-session liveness is not substituted
for immutable publication identity. Any transient result is observational only.

## 3. Narrow direct inspection method

Add a distinct private store method for the original confirmed0.3/0.4 binding;
it does NOT call discover(), resolve(), reconcile() or scan sibling names.
Confirm reference format is0.3 or0.4 and canonical CRP relative UUID path exactly
under the original held store. Traverse original expected directories from that
root with no-follow safeguards and compare full original identity chain. Open
ONLY that canonical file with O_NOFOLLOW/O_NONBLOCK/O_CLOEXEC preserved; require regular/single-link and original file inode/
device identity. The filename/account ID/hash/version are independent checks.

Acquire at most existing1MiB LIMIT plus one sentinel byte before parse. Actual
bytes—not stat length alone—enforce the bound; growth during read cannot allocate
unboundedly. Reject duplicate JSON keys, invalid UTF-8/JSON or unsupported version;
apply the same existing0.3/0.4 owning semantic validators. Verify exact original
raw SHA256, account ID and declared version. Compare pre/post file metadata,
reopened named file identity and original root/chain again. Same bytes on a new
inode is changed, not current match. A valid other account with wrong binding
refuses. No unknown-format or generic read_account read_to_end path is used. Retain
parser duplicate-key, depth and error bounds; a1MiB byte cap is not a total
parser/validator allocation bound.

Command refusals (busy, invalid token/generation, stale entry/context, unavailable
original custody) are separate from completed file-inspection observations. A
stale result cannot be reported current_match. For an admitted inspection return
independent statuses: current_match, missing, changed, unsafe, unavailable.
Missing means exact target/required chain absent; changed covers identity/content/
version/semantic mismatch or stale binding; unsafe covers symlink/nonregular/
hardlink/path violations; unavailable covers unsupported capability/IO/oversize/
original-custody absence. Preserve original errno and unsafe/missing causes; existing compare wraps errors
as LocationMismatch and cannot be blindly reused for this classification. An
observed root/directory/file replacement is changed; unavailable means a check
could not be completed, not a known replacement. Error detail preserves actual cause without returning
hostile content as markup. Never call this a unique account or complete namespace
resolution. Duplicate matching account ID elsewhere is irrelevant to this DIRECT
inspection, remains unexamined and cannot be reported absent. Legacy full resolver
continues its existing uniqueness/discovery rules independently.

## 4. UI meaning and lifecycle

Add a read-only recheck action to each eligible published0.3/0.4 entry in the
existing ConnectorSourcePanel. Display "original publication outcome" unchanged,
then separately "current exact-file inspection" with status, observed binding,
limits. Return only compact status and observed identity/hash/version, not the
full parsed account or a second draft view.
No reread failure turns a published outcome into failed publication. No matching
bytes add truth, performed duty, current source custody or human acceptance.

Do not invoke publish again, reconcile an Attempt, clear/reset the registry,
restore a token, rewrite or delete files. No automatic retry. Missing/changed
current bytes leave the original confirmed outcome intact. After restart this
hot-token action is unavailable; existing cold readers remain separate. The UI
must not accept arbitrary content from a renderer reference or infer uniqueness.

One transient inspection lease in the existing App registry is the proposed
technical concurrency budget: IPC admission refuses a second inspection as busy,
without queuing, regardless of UI busy state. Acquire a small private RAII lease/
revision under the registry lock, clone the typed Arc/reference, release locks
before IO, and revalidate entry/project/lease revision on return. The unique inspection lease/revision is separate from publication inflight.
Release the lease on success, failure, stale return and early exit/panic-safe
unwinding; never clear a different newer lease. Arrange guard/drop ordering so
RAII cleanup never relocks a registry mutex already held by that same thread. No account identity/slot is consumed. UI busy is
presentation only, not enforcement.

Read buffer and parsed account exist only within this one inspection; discard
them before returning compact status+identity/hash/version. No full readback is
cached in Entry, registry, response or UI. An existing prepared CAM payload may
coexist: one frozen payload plus transient read/parse/validation allocations is
NOT a global1MiB memory guarantee. Measure/account those simultaneous costs.
The resource bound is at most64 distinct retained published-store root FDs plus
one inspection's temporary chain/read/check handles; Arc clones alias existing
FD ownership, not duplicate FDs. This is not the entire App FD bound: count
coexisting prepared/root/source handles and uncertain recovery Arcs as well as
inspection root/chain/reopen handles and metadata. The precise counts
need code review. This technical inspection budget is not a product N policy.

## 5. Authorized code fence after release and joined tests

Candidate code fence only: connector_materialization.rs typed custody/recheck
lookup and state handling; connector_route_store.rs direct known-binding bounded
method; lib.rs command orchestration; ConnectorSourcePanel.tsx existing panel and
its narrowly relevant presentation/test helpers; connector materialization/store
and UI connected tests. No Host exporter/role service/new carrier/R2/RS schema,
old resolver rewrite or blanket cold acquisition change. Exact code release is
still held pending source/Host/CRP and independent review.

Required joined constructed path: ordinary local Git fixture, injected source
selection through existing seam, actual source read/Git observation, real0.3 and
0.4 prepare/publish, returned token command, actual published file inspection and
existing compact inspection-status panel projection. Synthetic events/selection are labelled; no native
launch or person witness is claimed. Test unsupported/stale token/project,
source-session change, root/ancestor replacement, symlink/hardlink/nonregular,
post-read rename/substitution, same-byte different inode, file growth above cap,
semantic/hash/version mismatch, missing file, late UI reply and FD failure.
Place huge hostile unrelated file and duplicate account elsewhere; instrument
that they are NEVER opened/enumerated by this method and no uniqueness claim
appears. Exercise all64 confirmed entries and Arc lifetimes without secondpayload/
newslot/reset; repeated reads cannot repeat publication. Preserve uncertain
Attempt behavior and legacy0.1/0.2/full resolve/0.5 tests unchanged.

## 6. Comparison with connected Host export

HOST_REQUEST_EXPORT_CONNECTED_ASSESSMENT.md describes a useful different slice:
actual original request facts exist, but a new bounded atomic Host projection,
source-method/association mapping and live source/gap inspector must be designed.
Capture under Host Inner, then release before external work; closure/currentness
is point-in-time, not a lease. No complete answer/review issuer exists there.

Prioritize this publication recheck because the exact successful writer result
and same-store Arc are already available together at publication, and the draft
UI is its immediate consumer. The missing bridge is retaining that typed custody
and a direct bounded read, not reconstructing a request/role join. The Host export
remains held unless C3 adopts its actual connected consumer. Neither slice can
claim complete reconstruction, new carrier adoption or durable recovery. The
comparison is technical sequencing, not a claim Host exports lack useful facts.
