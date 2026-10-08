# C3 PM-05 durable recovery assessment

Source-only proposal; no recovery policy selected or implemented. Undertaking
basis: CCE source dd50b1692c7d3c710ade07a5c344cc16fafeee77, with source decision
repair 3c59d92f3ffe380d923af4ae881ec7e318041db4. S/T/W scope admission,
operation treatment and controlled writer/adapter remain unselected. No real
graph operation is authorized. This assessment is the next question named in
C3_TARGET_SCOPE_DECISION.md, not a claim of full reconstruction or PM-05 closure.

## 1. Finding and recommendation

PRD V4-PM-05 requires status recoverable across sessions from files. Lifecycle A
retains only same-process unfinished CCE state; its prefreeze loss does not meet
that requirement for the whole workflow. Compare **R1 immutable stage checkpoints** with **R2 bounded reusable current-
status journals**, both requiring durably confirmed intent before graph dispatch
and historical-only cold recovery. Neither is ranked for product adoption until
the capacity/product-fit decision below is made. This is a design option for owner selection,
not reuse already authorized by CAM. R1 changes when existing CAM identity slots are spent and needs a new
checkpoint representation, store/reader adoption and named CAM/CCE amendment.
R2 instead introduces separate journal identity/storage and explicit retention
policy; final accounts still consume CAM slots. Neither changes the accepted
64/one-payload/1 MiB bounds in this assessment.

R1 can make last-known stage and uncertainty recoverable; it cannot guarantee
preservation of every emitted answer or observed effect in the interval before
its checkpoint is durably confirmed. It cannot make graph edit and checkpoint
publication one transaction. Cold absence means not observed in available
records, never proof that the operation did not occur. No hot token, original
source capability, scope, grant or human act is reconstructed from records.

Alternatives:

- **R0: retain A.** No new storage or slot cadence; status before final save is
  lost on process exit. Lowest implementation cost, explicit PM-05 gap remains.
- **R1: CRP-style immutable checkpoints.** Bounded snapshots and
  references, original outcome retained, no overwrite/compaction/reset. Greater
  slot consumption and partial chains are visible. Requires reviewed successor
  support; not currently supported by CRP account validation.
- **R2: separate recovery journal/sidecar.** Could avoid an account slot per stage
  and record finer events, but introduces its own identity, retention, size,
  atomicity, torn-write and migration policy. Existing recovery ledger is a
  pointer ledger, not a license to store CCE artifacts or authority. No new
  budget or unlimited log is presumed. Section7 supplies a concrete bounded
  snapshot-journal candidate and its still-unselected policy costs.

## 2. What current code actually supplies

connector_route_store supports formats 0.1–0.4, not proposed 0.5 or checkpoints.
ProjectRouteStore writes validated account bytes with no-replace rename,
file/directory synchronization and post-publication inode/hash/account checks.
It returns BoundReference or an error with possible Attempt/temporary leftover.
An uncertain rename/publication does not retry or unlink automatically.
`discover` reports completeness/issues; `resolve` checks exact binding and
canonical duplicate identity; `reconcile` needs the original Attempt's created
file identity. Discovery cannot recreate missing original inode evidence.

CAM's registry holds 64 frozen identities for one App instance. Cancelled,
superseded, refused or uncertain consumed entries retain their slot. One payload
at most 1 MiB is retained across prepared/in-flight states; after write only
compact result remains. Registry/hot tokens disappear on restart. CRP cold
inspection is not previous-success proof. recovery.rs separately records App
pointer metadata and explicitly cannot revive old supplier requests. No existing
code provides a joined CCE checkpoint producer or source-admission restoration.

CRP's opened-directory identities constrain operation targets; mutable-path
rename races and uncertain foreign-name substitution remain as already defined.
R1 inherits these limits if selected, not stronger physical or transactional
assurance. Composer size checks do not cure legacy cold read allocation limits.
Reader resource treatment for a new checkpoint carrier must be explicitly
reviewed without silently changing old-format compatibility.

## 3. Concrete candidate checkpoint plan and costs

Define a new closed recovery carrier before implementation; do not force early
stages into 0.5 (which requires an answer) or smuggle them into fact fields.
Proposed six freezes/publications for one uninterrupted successful full path:

| Stage | Durable content and next-step condition | Identity cost |
|---|---|---|
| C0 admitted undertaking | Exact base account bytes reference/question, task attempt identity, current stage and explicit no answer/review yet; historical source limits | 1 |
| C1 answer | Exact selected answer artifact bytes/hash and original observed-authorship reference; predecessor C0 | 1 |
| C2 review | Exact review artifact and answer binding, review disposition, planned target/plan references only where legitimately available; predecessor C1 | 1 |
| C3 graph intent | Exact intended operation, target/preimage/plan, admitted dispatch-basis references and predecessor C2; graph dispatch allowed only after durable confirmation AND fresh S/T/W recheck | 1 |
| C4 graph outcome | Actual original dispatch/operation/outcome evidence or explicit unknown/partial effect, pre/post/reread bindings and limitations; predecessor C3 | 1 |
| C5 final account | Valid final contribution account linking exact base, answer, review, intent and outcome references; retains all gaps | 1 |

No graph dispatch on refused or uncertain C3 publication. Confirmation means the
selected writer's actual durable-success path, not merely bytes found later.
Even confirmed C3 only establishes an intent record; crash immediately after it
may precede dispatch. On restart that state is "dispatch outcome unknown",
not "dispatched" and not "never dispatched". A separate optional dispatch-start
checkpoint would add a slot and still cannot remove the next instruction/crash
gap; it is NOT included. C4 is retained separately so C5 failure does not erase
already persisted observed outcome. An answer/review-only terminal path may stop
after C1/C2 with explicit outstanding integration; its final account is another
freeze if separately produced. A cancellation terminal record also costs a slot
if selected; it is not a free write. Maximum planned full path is six; repeats,
corrections or reconciliation records are new proposals, not hidden retries.

Every successfully frozen checkpoint consumes one existing lifetime slot before
its attempted publication, including definite failure or uncertain publication.
Failed preflight consumes none. A completed six-freeze path costs six slots:
with an otherwise empty instance, ten such paths cost 60 and four slots remain;
no promise an eleventh can complete. Existing 0.3/0.4/final drafts consume the same
budget. This arithmetic is not a reservation mechanism. Admission should report
available slots and planned cost; guaranteeing completion by reserving multiple
slots would itself need a different selected rule. Before C3, lack of remaining
capacity for outcome/final recording must prevent new dispatch under the proposed
route; race-free capacity accounting and no competing preparation need review.

Only one full serialized working payload at a time. Freezing/publishing each
stage must transfer the shared payload, not keep a second full draft. Prior
artifacts can be cited by exact immutable references and streamed/resolved within
reviewed bounds; do not duplicate their full text in diagnostics. Retaining
artifact caches simultaneously is not assumed compatible. A concrete memory/
serialization implementation must prove the one-payload rule before release.
Each carrier's exact escaped bytes, metadata and excerpt content fit 1 MiB or
refuse without truncation. No retirement, compaction, deletion, slot reclamation
or auto restart by default. Process restart loses the hot registry; cold IDs are
not hot CAM tokens and must never authorize reuse or automatic continuation.

## 4. Crash and restart matrix

"Same-process" below uses retained genuine custody only; restart always loses it.
A later cold hash match establishes current bytes, not prior successful commit,
original authorship truth or effective authority.

| Boundary | Same-process result | Restart/cold result and next action |
|---|---|---|
| Before C0 or while C0 publication uncertain | Retain refusal/Attempt; no authored-stage advance dependent on confirmed C0 | No found record: undertaking status unavailable; discovered candidate: historical/unconfirmed start. Do not fabricate prior registry/Attempt |
| After C0, before answer emission | Original active source may continue | Undertaking known, answer not recorded; fresh source/role admission needed |
| After answer observed, before C1 durable | Keep actual answer while process lives; uncertain checkpoint retains Attempt | C0 only means answer not retained, not never authored. Recovered C1 bytes require validation/resolution; no fresh authorship mint from them |
| After C1, before/after review emission but before C2 durable | Retain original review if observed | Answer historical; review not recorded/unknown. New review requires fresh original source and exact historical answer binding |
| After C2, before C3 | Current sources and S/T/W needed for dispatch | Review historical; no authorized continuation from cold references. Re-admit scope/treatment/selection/target |
| C3 rename/publication uncertain | Refuse graph dispatch; preserve Attempt/leftover, never automatically retry | Candidate intent remains historical/unconfirmed; do not dispatch or infer prior write from it |
| C3 durable, before dispatch | Fresh recheck may permit dispatch only on selected route | Could have crashed before or after dispatch; outcome unknown. Target inspection under fresh applicable read scope/authority can compare the exact intended insertion, never automatically retry |
| After dispatch, before original outcome observation | Keep dispatch and uncertainty, even on cancellation/revocation | C3 is last-known intent, effect unknown; no atomic graph/checkpoint guarantee |
| After observed graph write, before C4 durable | Actual/uncertain observation retained; saving failure is not graph rollback | C3 only: graph outcome not durably retained. Fresh target bytes may match plan but cannot establish exclusive causality or recreate operation receipt |
| After C4, before C5 freeze | Retain real outcome; capacity/save failure does not erase it | Historical observed outcome recoverable if chain resolves; no current authorization or re-execution |
| C5 frozen, before/during save; final rename uncertain | Token consumed; actual error/Attempt retained; no second writer invocation | C4 persists; final account may exist or not. Discover/validate exact candidate; absence does not restore token or prove no publication |
| After C5 durably confirmed | BoundReference retained, earlier observations remain | Cold final account and chain historical; no hot revival, no human acceptance inferred |

Changed/missing/duplicate checkpoint, base, answer, review or predecessor blocks
that chain's complete status. Show resolved prefix plus exact missing/conflicting
edge, never select newest timestamp or silently take a matching-name substitute.
Multiple successors are branches/conflicts, not an ordered sequence. A self-
consistent imported chain is still only recorded claims unless actual original
custody independently remains; checks never mint performance or authority.

## 5. References, recovery and migration

Each checkpoint needs distinct record identity, stage, predecessor exact byte
reference, base account identity/hash/length/question and original undertaking
association. References carry kind, identity/method and resolution-at-write;
cold reads report resolution-at-read separately. Exact artifact text hashes are
not parsed-frame wire hashes. Retain originally observed frame method/generation/
positions and contribution limits. Do not store raw transport/history/hidden
reasoning. Manager review continues to bind the exact answer; correction branches
never make an old review cover a changed answer.

Durable graph intent/outcome references are conditional on the future selected
writer source; no invented operation receipt schema is adopted here. Exact
scope/treatment references remain historical evidence, not authority tokens.
Reopening and target inspection require fresh applicable read scope/authority,
explicit project association, fresh source/role admission,
current target preimage and independent applicable treatment; outcome inspection
is read-only and distinct from permission to retry. Recovery UI should separate
"recorded last-known stage", "current resolution", "current source admission"
and "integration effect known/unknown".

No in-place migration of 0.3/0.4/0.5 data. Existing 0.3/0.4 accounts remain source
and reconstruction records with their existing limits. Existing 0.5 definition
fixtures/proposal files are not production checkpoints and cannot be promoted
into actual authorship. A future explicit import may cite exact old bytes as
historical subject data, never fabricate missing C0–C4 or claim former stage
completion. Reader support must be added explicitly; old readers refuse unknown
carrier/version. External PEC/Domains/fleet/examination owners decide their
adoption; recovery does not create their completion prerequisite.

## 6. Selection questions and examination plan

Owner choices needed: select R0, R1 or R2. For R1, decide changed CAM
slot-consumption cadence (not numerical expansion), carrier/placement and reader
adoption, terminal cancel/correction/reconciliation record costs, and behavior
when remaining slots cannot preserve a started outcome. For R2, separately
decide journal identity and shared quota ownership, aggregate byte/entry limits,
snapshot/descriptor atomicity, permitted historical retention loss, terminal
retirement/reuse and final-account evidence preservation. Neither option is
selected by this assessment. No capacity reservation or extra metadata
store is smuggled into R1. S/T/W decisions remain separately required for graph
work; one may implement answer/review recovery first only after its own reviewed
source and actual capture seams exist.

Required future negative cases (designed, NOT run): crash injection at every
matrix boundary; fsync/no-replace failure before and after rename; substituted
temporary/final name; missing original Attempt; incomplete discovery; duplicate
identity and forked predecessor; changed base/answer/review; source generation
closure; unknown actor/capture; partial chain with valid hashes but fabricated
custody; exhausted budget at each stage; cancelled/uncertain checkpoint retains
slot; concurrent preparation cannot steal outcome capacity; escaped payload over
cap; no original hot token after restart; matching postimage cannot prove writer
origin; revoked scope after dispatch does not erase outcome; final save failure
with successful graph write; old0.3/0.4/0.5 imported data never upgrades standing.

This assessment has inspected source and arithmetic only. No crash tests, native
acts, graph writes, new identities, publication or recovery implementation ran.
R1 reduces lost status only after each durable checkpoint; the remaining windows
must be presented honestly. Do not present whole-product 90% sufficiency while
PM-05 recovery and capacity/product suitability remain unresolved.

## 7. Product-fit repair: bounded R2 compared substantively

The recommendation at 85605da681a7b0df68b06dcf0cecadf6a498360a was insufficient:
it preferred CRP reuse despite only ten ordinary full paths per otherwise empty
App instance. PRD §1.2 seeks work "at scale, reliably"; §4.6 includes a fleet and
PM-05 requires cross-session status. Revisions, cancellations and other drafts
reduce R1's ten-path figure further. That is a material product-fit concern, not
a small implementation cost. Restart is NOT a capacity policy or a supported
way to recover uncertainty. The initial reviewer READY at 326b9925d7 was withdrawn
on this finding; neither option is now recommended as a selected product policy.
Recommend the owner compare R2 seriously before accepting R1 as more than a
bounded development demonstration. No numeric policy changes here.

**Concrete R2 candidate mechanism.** One recovery identity per undertaking,
separate from account IDs and CAM hot tokens; repeated stages update its bounded
current-status journal rather than consuming another CAM identity. Only final
account freeze uses the existing CAM slot. This separation is a NEW identity
policy needing explicit selection. It is not an extra account secretly outside
64. An opaque random journal ID is a locator, never an authority credential.

A candidate bounded implementation uses two on-disk snapshot slots per journal,
each holding a complete cumulative status/artifact snapshot of at most 1 MiB
serialized, plus a small commit descriptor. The snapshot contains exact previous
committed revision/hash, current stage, artifacts, intent/outcome and gaps. The
one-payload App memory rule still applies; two disk generations are not permission
for two retained full in-memory payloads. The descriptor has a separately selected
metadata bound; a sizing candidate for review is 64 KiB, NOT an accepted cap.
A finite selected project journal-count limit N is also required. Storage upper
bound is approximately N*(2 MiB + descriptor bound), plus explicitly bounded
one-publication temporary overhead; N is an owner sizing choice, not invented
unlimited capacity. At N full/unretirable journals refuse another undertaking
visibly; do not evict the uncertain one or reset by restart.

Single-writer serialization per opened project/journal is required. Write only
the inactive snapshot, synchronize it, publish its exact hash/revision through a
synchronized descriptor update, and preserve the previous committed generation
until the new descriptor is confirmed. Recovery follows the exact committed
reference, not newest timestamp/enumeration order. Incomparable descriptors,
forked same revisions, missing referenced bytes or duplicate journal IDs give
conflict/unknown; never select an arbitrary winner. A complete inactive snapshot
without a committed descriptor is an unconfirmed candidate, not a new stage.
The two-slot publication primitive, descriptor replacement, filesystem races,
partial-write behavior and writer exclusion need independent design/probes;
CRP write-once account rename is NOT already this journal transaction.

Write-ahead intent must be durably committed before dispatch, followed by fresh
S/T/W recheck. Outcome observation updates current status, but graph edit and
journal update still are not one transaction. Crash in between retains unknown
outcome. Original scope/role/source custody does not survive restart; a journal
is historical recovery evidence only. Old stage history can be summarized by
exact predecessor bindings only if the owner accepts the retention loss below.

**Retention/reuse choice.** A current-status journal is not an unlimited audit
log. Reusing the inactive slot eventually removes earlier full stage snapshots.
That is permissible only under an explicit selected retention rule requiring the
current snapshot to preserve recovery-critical exact answer/review/intent/outcome
and unresolved-attempt evidence. If cumulative evidence cannot fit 1 MiB, refuse
further advancement; do not truncate or silently discard prior uncertainty.
An indefinitely repeated revision history cannot fit this bound. The owner must
choose whether full historical stage recovery is required (which defeats simple
two-slot reuse), or current recoverable status plus final immutable account is
sufficient, with clearly stated historical loss.

Retirement is explicit, never automatic merely because an operation returned.
A candidate retirement condition is: final account durably bound and independently
resolved, required historical artifacts/evidence preserved there or in separately
accepted immutable references, no unresolved attempt, and explicit retirement
choice. A cancellation before dispatch may retire only with a selected rule for
retaining its terminal status. Unknown outcome, uncertain journal/account write,
missing final evidence or unresolved target effect forbids retirement. Deletion/
slot reuse is a new policy, not authorized here; crash-safe retirement markers
and cleanup need design. If retirement records must themselves remain forever,
their storage needs its own bound and the claimed fixed total cannot omit it.
No unbounded tombstone list is hidden in the descriptor budget.

| Dimension | R1 immutable account-like checkpoints | R2 bounded current-status journal |
|---|---|---|
| Identity cost | Six CAM lifetime identities per full path, fewer than 11 paths/instance | One separate recovery identity/undertaking and one final CAM identity; new identity policy |
| Repeated normal work | Exhausts current budget rapidly even if all work succeeds | Can reuse explicitly retired journal capacity, but final CAM64 still limits account preparations; does NOT solve total product capacity |
| Historical evidence | Immutable stages retained, no compaction policy | Current cumulative evidence plus limited prior generation; owner must choose permitted stage-history loss |
| Atomicity | Existing CRP semantics after new carrier adoption; multiple partial records | New two-slot/descriptor transaction and retirement protocol; must be proved, not assumed |
| Recovery | Exact chain/prefix, missing edges explicit | Exact committed snapshot; conflicting/uncertain descriptor explicit |
| Uncertainty | Consumes more identities; no automatic retry | Occupies non-evictable journal until resolved; capacity may stall |
| Implementation/owner cost | New carrier/adoption and changed slot cadence | New storage/identity/retention/atomicity policy and actual writer; more design work but materially different throughput |

R2 is not dismissed because it is new policy, and R1 is not preferred merely for
CRP reuse. Both are finite. Neither establishes that 64 lifetime final identities
is adequate for professional fleet use. Whole-product capacity design remains a
separate owner/product suitability decision before a 90% claim.

## 8. Sharpened preconditions: capacity and one working payload

R1 needs at least three usable future freezes at admission to C3 (intent,
outcome, final) and an exclusive continuation that prevents another preparation
from consuming them before C4/C5. The present policy has no multi-slot reservation;
checking a count alone is not a guarantee. A proposed continuation exclusion may
reuse the one-active-set constraint, but its precise lifecycle between publications
requires review. No implicit reserved slots or extra registry are adopted.
Before dispatch, inability to establish this capacity condition refuses dispatch.
After dispatch, capacity loss or publication failures cannot erase the retained
actual/uncertain outcome; failed frozen publications still cost slots and may
exhaust even an initially adequate margin. No finite allowance guarantees
successful durable recovery through unlimited failures. Retain same-process
outcome and report inability to persist; restart can lose it. This limit survives
both recommendations and requires explicit UI/examination treatment.

For both options, publishing a stage while retaining the active CCE working set
must not create two full payloads. Proposed data flow transfers the sole immutable
payload to the writer, blocks mutation/other preparation while in flight, and
retains only bounded source capability handles and compact outcome metadata.
After publication, any next cumulative snapshot must be composed within the same
budget, using exact prior persisted artifacts or the transferred buffer without
retaining another complete copy. Cold reads, serialization temporaries and
source-owned message history are not magically covered by that phrase: the
implementation must demonstrate actual allocation/ownership and bounded readers.
Until this is proved, cross-stage one-payload compliance is a design hold.

Additional designed negatives: journal count N exhausted; descriptor cap and
snapshot cap exceeded; interrupted inactive-slot write; descriptor commit lost;
self-consistent tampered or forked descriptor; attempt to retire uncertainty;
retirement crash leaving both/live/neither marker; no hidden unbounded tombstones;
capacity checked then consumed by competing preparation; post-dispatch C4/C5
failure exhaustion; two full payloads retained during stage transfer. These are
assessment obligations, not executed tests or a selected recovery contract.

### R2 carrier, torn publication and final-account binding precision

R2 here is per-undertaking **bounded snapshot journaling**, not an append-only
shared log. Its fixed live entry inventory is two snapshot slots and one commit
descriptor per journal, plus at most one bounded publication temporary per active
writer. No append stream or indefinite entry count is hidden. A truncated/torn
snapshot or descriptor is invalid, never parsed as a valid prefix or silently
repaired; recover the prior exact committed generation only when its descriptor
and bytes remain independently resolvable. Otherwise show ambiguous/unknown.
A traditional append alternative would need its own selected byte/entry ceilings,
framing/checksum/commit marker, torn-tail preservation and compaction rules; it
is not assumed to be safer or already implemented by recovery.rs.

After any fsync/rename/descriptor error, preserve the original in-process attempt
and exact uncertainty; a later successful read cannot prove that the original
write was durably confirmed. Following restart, absent original attempt evidence
is reported absent, not reconstructed from a plausible snapshot. A partially
advanced descriptor cannot authorize dispatch. The proposed retirement protocol
must preserve this uncertainty through crashes; its feasibility is still open.

Final account must bind the exact committed pre-final outcome snapshot identity,
revision and bytes, while retaining every artifact needed after retirement in
itself or separately accepted immutable storage. A later journal revision may
then point to the exact final account BoundReference. This avoids a hash cycle:
final account does not hash the later journal revision that points back to it.
Do not retire snapshots if the final account would retain only unresolved mutable
journal locators. Copying evidence for retirement must preserve exact bytes and
limits within the same serialized cap; overflow refuses retirement. Journal ID
remains fixed for one undertaking; slot revision and content hash distinguish
versions. Reusing a retired physical slot assigns a new identity, never rebinds
old references to another undertaking. No immutable history is claimed for slots
that the selected policy permits replacing.

N is an aggregate **project** journal quota, not a separate allowance silently
granted to each agent. All participating writers need a real shared quota/locking
owner; per-process counters alone cannot enforce it against another App process.
Multiple projects additionally require an explicit aggregate disk-budget decision
if a system-wide bound is claimed. The current option establishes neither that
cross-project limit nor a production value for N. Stage memory stays globally one
payload in this App instance. Candidate descriptor64KiB and snapshot1MiB figures
are design values for sizing review, not adopted recovery storage policy.
Final CAM preparations still consume the existing64 lifetime slots; journal reuse
cannot hide, reset or expand that remaining product capacity constraint.

## 9. Separate future CAM product-capacity assessment

Question for a later bounded design assessment: can verified durable terminal
outcomes permit retirement of a hot CAM registry entry while preserving exact
outcome discovery, original uncertainty and replay refusal across restart?
This concerns CAM's final-account registry, separately from R2 journal retirement.
Inputs are current CAM-R1 success/cancel/supersede/refusal/uncertain states, CRP
BoundReference/Attempt/reconciliation, cold identity/duplicate rules and actual
long-running fleet demand. Output should compare immutable durable outcome
records plus explicit retirement against the existing lifetime registry, including
storage/identity/retention costs, crash between durability and retirement,
missing/changed/duplicate outcome records, replay of consumed tokens and concurrent
retirement/publication. Unknown or uncertain outcomes must not disappear, and
cold records must never revive a publication token or authorize replay.

No retirement mechanism, value or number is selected here. Existing CAM remains
64 identities per App-instance lifetime, including successful/cancelled/consumed
entries, with no eviction, reuse or reset. Even R2 continues to hit that final
preparation limit. Any durable-outcome/retirement route requires a named new
policy, exact source/consumer review and owner selection before implementation;
it cannot be inferred from a successful save or restart. This separate capacity
question remains part of the product-suitability assessment before a whole-
product 90% claim.
