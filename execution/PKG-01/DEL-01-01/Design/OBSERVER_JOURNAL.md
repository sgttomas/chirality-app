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

Before enabling retention, preserve delivery into the Rust native projection
and checkpoint/model-turn recorders independently of window replay. Then add
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
