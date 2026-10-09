# C3-R2-P1 — recoverable current-status source/proof plan

PROPOSED named source plan awaiting independent review, based on merged
C3-OD-02 at 0580a56a3718f4801f73d1b6a072fb332a15d28f. Owner selected recoverable
current status with exact recovery-critical evidence; older full intermediate
snapshots may be replaced. R2 is a design/proof target, not selected storage,
quota, retirement, migration or implementation. CAM64 is unchanged and separate.

## 1. Recoverable subject under selected W2

One undertaking's current status must retain exact selected base-account,
answer, manager review/contribution, intended ordinary operation, observed
supplier outcome and independent target observations, plus unresolved attempts,
limitations and actor responsibility. A2 current/historical custody remains
separate from durable state. An intent is the actual supplied request and known
intended target/basis; it is not an enforceable insert plan or an App scope grant.
W2 does not warrant exclusive causality, only the supported observation join.

Cold recovery finds committed recorded state, not restored SourceRequest,
RoleBinding, original runtime permission, authority or human act. No automatic
supplier turn, retry, graph write or stage advancement follows. It must distinguish
not requested, request outcome unknown, observed terminal failure, observed tool
completion, independently observed target state, missing manager reconciliation,
and final account publication outcome without collapsing them into success.
These are semantic distinctions; exact enum/format remains for reviewed schema.

## 2. Concrete design options and recommendation

**R2-S (baseline to develop):** per-undertaking two complete bounded snapshots
and one commit descriptor, under an opened project root and shared project quota.
Publish inactive snapshot, synchronize, atomically replace descriptor with exact
journal identity/revision/hash, synchronize, preserve prior confirmed generation
until confirmation. A candidate snapshot1MiB/descriptor64KiB and aggregate countN
come from the earlier assessment as sizing candidates only. They are NOT adopted
caps; do not allocate or invent N in implementation. One active full memory
payload remains unchanged; two disk slots do not permit two full resident sets.

**R2-L (comparison option):** bounded append journal with exact framed entries
and an independently committed checkpoint/compaction boundary. It can preserve
more incremental history but needs entry/byte ceilings, torn-tail rules, original
attempt uncertainty, compaction and reference survival. It is not automatically
safer: prefix parsing cannot promote an unconfirmed append to durable success,
and an unbounded old log is prohibited. Compare total storage and recovery work
with R2-S before selecting a mechanism; the owner selected current-status
retention, not a particular write primitive.

Recommended next source result is the complete R2-S transaction/reference and
resource design, with R2-L retained as a concrete alternative if filesystem or
bounded-payload proof fails. This plan does not select a journal implementation.
CRP's immutable no-replace account publication is not already mutable journal
atomicity. Shared locking/quota across App processes and agent undertakings must
be actual, not a renderer count or one process's mutex.

## 3. W2 ordering and irreducible uncertainty

Durably commit exact intent before a newly initiated tracked supplier request;
then dispatch only through actual current Host custody/permissions. A journal
cannot prevent an unrelated supplier turn editing files, and this ordering is
not a new global supplier veto. Where the App did not initiate/track the request,
record that observation boundary; do not fabricate a write-ahead intent.

Crash after intent but before dispatch and crash after dispatch before event
recording can look identical. Recover unknown, never infer no write or replay.
Tool completion before journal outcome commit may be lost; current matching file
bytes may corroborate state, never reconstruct the missing original Attempt or
exclusive causality. Stop, interruption and owner withdrawal do not undo effects.
Preserve live original attempts on storage errors; if process exit loses them,
record missing original evidence rather than manufacturing a replacement.

Whole graph write, supplier event, target reread and journal commit are not one
transaction. Describe the actual observed order, not a fictitious atomic action.
Incomplete source/target/history must be visible even if a descriptor is valid.
No silent rollback, repair, unlink, retargeting or automatic retry.

## 4. Retention, identity and final account

Current snapshot must keep exact recovery-critical artifacts and unresolved
attempts or immutable references whose continued resolution is actually ensured.
Hash-only references to replaced mutable slots cannot recover required bytes.
If cumulative evidence exceeds selected bounds, refuse advancement visibly;
do not summarize exact messages or discard uncertainty to fit. Deleting old
full stage snapshots is allowed only when required current evidence survives.
This is owner-selected retention direction, not blanket deletion authorization.

Final account binds an exact committed pre-final outcome snapshot; a subsequent
journal state may reference the final bound account, avoiding a hash cycle.
Final publication remains CAM/CRP one-use with uncertain Attempt retention. A
final account that omits required historical evidence cannot justify journal
retirement. No physical slot reuse may rebind an old journal identity.

Retirement/cancellation terminal retention and quota reclamation need an explicit
bounded design: durable terminal outcome/reference, no unresolved attempt,
required evidence independently resolvable, crash-safe retirement markers,
finite marker/tombstone storage and visible refusal at exhaustion. No eviction
of uncertain journals; no manual restart as capacity policy. The separate final
CAM registry still consumes64 identities per App-instance lifetime. A future
CAM durable-outcome/hot-entry-retirement assessment is not this journal policy.

## 5. Proof plan and consumer obligations

Designed checks, not executed tests:

| Boundary | Required negative/proof |
|---|---|
| Admission | Concurrent undertakings/processes race for last quota; only real shared accounting admits; no per-agent multiplication. |
| Snapshot | Exact UTF8/escaping overhead, evidence growth, oversized imported descriptors, partial write, symlink/rename substitution and wrong root; bounded refusal without source promotion. |
| Commit | Crash before/after snapshot sync, descriptor replace and directory sync; wrong revision/hash, orphan candidate, forked descriptors, lost acknowledgment; never select newest timestamp. |
| Request | Intent-confirmed crash before dispatch versus effect-before-observation; both may remain unknown; no automatically repeated request. |
| Evidence | Closed/replaced generation, missing exact message, unknown writer, multi-file effect, conflicting reread, missing manager reconciliation; same-byte presence not proof of performance. |
| Replacement | Required old artifact referenced only by soon-reused slot; refuse replacement or preserve exact bytes within selected bound. |
| Finalization | Final account succeeds but journal update fails and converse; independent outcomes, no cycle, no restart token revival. |
| Retirement | Crash at each marker/delete/quota boundary, unresolved attempt, missing final bytes, duplicate identities, marker limit; no silent eviction/reuse. |
| Product fit | Fleet workload traces with cancellations/revisions/unknowns; refuse honestly at finite quota, assess final CAM64 separately before90. |

C3/PM05 owns recovery status and source presentation; Host supplies actual source
facts, never reconstructed capabilities; RS reviews exact reference/write/read
standing; CRP/CAM owners review final-account interface; project/fleet owner
reviews placement/undertaking identity without becoming an implementation
prerequisite. Technical design includes exact finite numeric/resource choices
for owner suitability assessment. No policy/PRD edit, migration, journal write,
new agent, native act, supplier launch or download is authorized by this plan.
