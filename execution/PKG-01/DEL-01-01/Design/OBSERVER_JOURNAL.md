# Observer replay and operational custody

RECOVERY §3.3 OA-01/OA-02 and HOSTING §5 require a bounded, disposable
per-generation replay journal. The current implementation still retains the
whole journal. The selected implementation defaults for replay are **4,096
frames or 16 MiB of serialized UTF-8 envelopes per home's current full
generation**, whichever limit is reached first. The byte metric includes the
retained envelope's metadata and unknown fields after existing sensitive-data
projection. It measures retained serialized content, not Rust heap overhead.
These are the observer-journal numbers left open by REC U-R4 / HOSTING U-05;
the implementation owner selects them under the session's development grant.
No eviction is enabled by this change.

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
is independent of window replay through the private handoff below. Before
enabling retention, add
retained-floor/gap semantics and source-scoped history reconstruction without
resuming a thread, answering a request, replaying old observations as new
events, or claiming unavailable checklist revisions were recovered. Handshake
overflow must preserve ordered delivery or refuse startup truthfully. Selected
limits' implementation and independently reviewed overflow behavior remain
activation inputs. An oversized native frame is processed normally by the
protocol/custody paths; it is omitted from replay without truncation and makes
that receipt a disclosed gap. Older windows rebuild from supplier history.

`hosting_observation_custody_tests.rs` removes diagnostic replay as an explicit
test stimulus and checks operational source facts. `steering_integration.rs`
checks the receiving projection independently. Those checks establish this
separation, not an implemented memory cap, candidate examination or native
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
snapshot. The record tick visits retained source projections in source order,
with thread/turn/request/custody metadata qualified by that same generation.
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
source metadata order and history/duplicate controls. The module's focused
checks cover owner/prefix identity, concurrent append and refusal without
partial acknowledgment. Ordinary App CI runs both maintained cohorts.
