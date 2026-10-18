# Observer replay and operational custody

RECOVERY §3.3 OA-01/OA-02 and HOSTING §5 require a bounded, disposable
per-generation replay journal. The implemented defaults for replay are **4,096
frames or 16 MiB of serialized UTF-8 envelopes per home's current full
generation**, whichever limit is reached first. The byte metric includes the
retained envelope's metadata and unknown fields after existing sensitive-data
projection. It measures retained serialized content, not Rust heap overhead.
These are the observer-journal numbers left open by REC U-R4 / HOSTING U-05;
the implementation owner selects them under the session's development grant.
Both limits are enforced on disposable public replay. Diagnostic envelopes
consume the same budgets, including when they have no source receipt position.

`hosting_observation_facts.rs` separates the operational facts previously read
from that replay storage. The Host captures them from its actual current,
open source receipts; no renderer, saved record or recovered history creates
them. They remain process memory, not another durable transcript:

- The latest turn-event boundary per thread retains full generation, receipt
  position, method, turn ID and reported status. Unknown or malformed later
  boundary content cannot revive an older active-looking memo. Existing
  terminal guards and issued-after-receipt rules still govern start responses.
- Supplier-resolution references retain typed request ID and thread scope.
  A queued reply cannot become eligible because a diagnostic frame disappears.
  Register settlement and acknowledgment remain separate facts.
- The latest account-change receipt position, qualified by full generation,
  invalidates an older logout assessment even through identical/redacted ABA
  observations. Another read alone is not a namespace change.
- Original EOF/exit observations retain their source-scoped facts for Stop.
  A diagnostic journal entry or a later numeric PID supplies no process custody.

The Host snapshot exposes `turnEventBoundaries` and
`accountNamespaceRevision` as disposable projections. Steering and logout
assessment consume those fields rather than scanning raw replay. The Host
still rechecks actual source/generation/target at dispatch. These fields are
not serialized capabilities or permission to operate from renderer JSON.

The minimal facts replace each other within one current full generation.
Turn boundaries are one per observed thread; resolution references deduplicate
by typed subject. This is not a bound on total Host memory, request custody,
native views or pending record observations.

Delivery into the Rust native projection and checkpoint/model-turn recorders
is independent of window replay through the private handoff below. Public
retention uses the floor and history path described below without resuming a
thread, answering a request, replaying history as new events or claiming
unavailable checklist revisions were recovered. An oversized native frame is processed normally by the
protocol/custody paths; it is omitted from replay without truncation and makes
that receipt a disclosed gap. The preceding public prefix is discarded so a
retained earlier frame cannot conceal this hole. An oversized diagnostic is
omitted without removing an otherwise continuous primary source prefix.

`hosting_observation_custody_tests.rs` removes diagnostic replay as an explicit
test stimulus and checks operational source facts. `steering_integration.rs`
checks the receiving projection independently. Those checks establish this
separation, not a total Host-memory cap, candidate examination or native
supplier qualification. ScopeOfWork commitments and dependency conditions
retain their existing meanings.

## Private native delivery and recording

`hosting_native_delivery.rs` owns an unread-only sequence separate from public
replay: actual ready publication, positioned projected envelopes, and source
closure. Its original Host issues one non-serializable receiving owner. A
pending batch retains exact Arc prefix identities; acknowledgment validates
the entire original prefix before removing it. Later receipts remain pending.
Dropping a batch acknowledges nothing. Public observers, cursors and equal JSON
cannot drain the sequence or replace its owner.

`HomeSession` gives that owner to its existing `RuntimeSession`. Status, actor,
action and host-tick reads share this projection. They incorporate source
frames in order, outside the Host lock, then acknowledge incorporation. This
prevents a Runtime/Host lock inversion and keeps record IO off the protocol
reader. Consecutive frames are applied as a generation batch rather than
serializing the complete native view for every frame. Failed startup supplies
no invented ready state; closed or foreign-source frames remain diagnostics.

Actual ready/frame/close input is processed even if its source closed before
the first read. Closed original projections retain their live-observed receipt
standing for recording, while current controls receive only the final current
snapshot. A Stop request makes current controls and actor-account attribution
unavailable immediately; it does not end private source incorporation before
the original close delivery. Frames received between Stop and EOF remain
original observations and can reach recording. The record tick visits retained source projections in source order,
with thread/turn/request/custody metadata qualified by that same generation.
Execution custody retains each event's actual observing source at creation,
separately from the unchanged event JSON: request outcomes and recovered turn
outcomes do not all have a top-level generation field. The private capture
uses that original association, never a guessed field or decoded event ID.
It cannot fill an old source's access mode from a later selection. History
rows retain recovered-from-supplier standing and do not become fresh arrivals.
Persistent native-event deduplication is unchanged.

Acknowledgment means projection incorporation, not durable recording. Status
writes no records. A busy run can be retried because its source projection
remains available; existing pending record identities and IO-retry behavior
remain the writer's responsibility. Neither the unread handoff nor retained
closed projections acquire a disposal policy or a total-memory bound here.

The actual checkpoint regression in `runtime_session.rs` removes public replay
before the ordinary tick and reopens the real run records. It covers closed
sources, status-first delivery, busy runs, repeated ticks, two generations,
source metadata order, Stop-before-EOF delivery and history/duplicate controls. The module's focused
checks cover owner/prefix identity, concurrent append and refusal without
partial acknowledgment. Ordinary App CI runs both maintained cohorts.

## Replay coverage and reattachment

`hosting_observer_journal.rs` counts the compact JSON serializer's actual UTF-8
output without allocating a second complete serialized copy. The count
includes metadata, unknown fields, escapes and Unicode, with no trailing
newline. Exactly the selected limits can be retained. The oldest envelopes
leave first; omission counters disclose discarded primary and diagnostic
entries. These counters do not grant request or process authority.

Coverage is scoped by the actual full generation, never an incoming envelope.
The delivered high-water **H** is the greatest primary receipt position
released to public replay. The omission floor **D** is the greatest omitted
primary receipt position. A current open-source cursor is continuous exactly
when `D <= after <= H`; an absent, foreign, closed, expired or future cursor
gets the current snapshot and a gap. Returned frames are a retained current
source suffix, not a closed source's replay. `observerRetention` reports both
positions and the actual retained serialized-byte and envelope counts.

Receipt assignment alone does not advance H. Pre-ready frames keep their
existing held lifetime and handshake deadline. At ready, the original ordered
native frames enter private delivery before the public replay budgets evict
any prefix. Pre-ready public auth-reply diagnostics are held separately until
the same ordered release; they cannot skip held source frames by advancing a
window cursor early. Failed startup discloses never-ready input without
inventing readiness. The budgets do not bound held input, native unread
delivery, private receipts, active views, wire input or Rust heap usage.

The window reader uses its own in-memory position per owning home/full
generation. It advances from received status coverage; an initial or expired
attachment calls `host_observe` with the **current selected source separately
from the cursor**. The Host checks that source atomically. A stale source has
no active-home fallback. Closing or hiding a window sends no Stop or answer.

## Partial history after a replay gap

`hosting_observer_rebuild.rs` queues actual loaded conversation IDs only for
the owning ready/open source. A public gap read enqueues memory state; it
performs no synchronous supplier call or durable write. The existing background
Codex-read tick attempts at most one target at a time, using the existing
recovery-read wait limit. It reads `thread/read` metadata and the first
descending `thread/turns/list` summary page through original private Host
receipts with initiator `app-rule:observer-history-read`.

Jobs deduplicate by full source, omitted-through cut and conversation. Later
cuts coalesce, targets are scheduled fairly, and a completed error is not
retried by ordinary same-cut polling. A later result never covers a newer cut
silently. The Host checks source/readiness and the loaded target after waits
and at publication. Unavailable, no-known-target and superseded results remain
explicit. Rejected payloads and supplier error text/data are withheld from
failure summaries; original receipts retain their own custody.

`observerRebuild` is a separate memory-only partial-history result. It never
feeds the canonical live native view, current control guards, execution custody,
the ledger or recording views. A delayed history result therefore cannot
overwrite newer live facts or create fresh checkpoint/model-turn arrivals.
This path does not use CV recovery transitions merely because a window missed
replay. Restart recovery retains its existing separate behavior.

`ObserverAttachment.tsx` displays actual read state, metadata, turn summaries
and reported pagination extent. It keeps source changes and late replies
separate. Earlier pages and item pages remain unloaded; existing stored-history
controls can read them. An exhausted turn-list cursor is not complete item,
goal, checklist or transcript reconstruction, and `fullHistoryRebuilt` remains
false. These are source/fixture mechanisms, not native candidate qualification
or completion of the joined recovery witness.
