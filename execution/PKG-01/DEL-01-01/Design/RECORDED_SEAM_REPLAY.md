# Recorded ST-5 and NV-04 traffic at the App seam

`app/supplier_checks/recorded_replay.py` is offline development equipment for
HOSTING §9.1, X-09/X-10 and RECOVERY RQ-05. It serves the existing redacted
0.160.0 `prototype/st5/recordings/` captures through the actual Rust Host's
process custody, stdio reader, request register and native receiving view.
It executes no recorded command and starts no model or stock supplier.

The caller binds the exact recording SHA-256 and selects its generation.
Supplier frames retain their recorded JSON values except correlated client
response IDs. Server request IDs occupy a separate namespace. App input must
match the selected profile; divergence refuses replay rather than generating
a convenient supplier response. The scratch audit identifies the recording,
consumed source indices, correlations, declared adaptations and unplayed tail.
Redacted captures do not establish original byte identity.

The `app` profile admits only the current App's initialize identity and added
gateway capability, its explicit captured model/provider selection in place of
the capture harness's policy/sandbox parameters, and empty native text-element
metadata. The recording's `<WORKSPACE>` remains an inert fixture value. These
are App-side comparison adaptations, not evidence that the peer honored a
permission setting or model selection. Other payload changes are refused.

The `app-recovery` profile selects only ST-5 generation 2 through its metadata
and turn-history responses. The actual automatic reader requests metadata
without turns, then descending summary turns, whereas the capture harness
requested full history. The recorded supplier results remain unchanged.
Capture tail operations (`thread/loaded/list` and explicit `thread/resume`)
are outside that segment; the App must not automatically resume or resend.

The separate `app-continue` profile retains the complete ST-5 generation 2
tail. It adds one explicitly **constructed** catalog prerequisite after the
recorded empty loaded-ID list: a person-directed `thread/list` query gets a
new response envelope containing the unchanged thread object from source
frame 25. The capture contains no catalog query or response, so that exchange
and its catalog membership have constructed standing in the audit, separate
from the consumed recording indices. An empty loaded-ID list cannot supply
the history catalog needed for selection.

The connecting test dispatches that catalog through the real `HistorySession`,
selects its thread, then invokes the ordinary explicit Continue factory and
retains its original Host receipt through reconciliation. A gate after the
recorded idle notification proves that status alone admits nothing. A wait
ending before the reply causes no retry; a later matching reply admits only
while the original selection remains current. Reselecting while it is pending
prevents admission. Repeated reconciliation creates no duplicate admission,
the lost acknowledgment stays unknown, and an unbound App role stays unknown
after native admission. This tests current source with a constructed prerequisite; it is
not a wholly recorded discovery journey or a candidate witness.

`hosting_recorded_replay_tests.rs` connects the peer to an actual scratch
recovery ledger and the App's configured home/project association. A written
answer followed by process EOF retains unknown acknowledgment and an RQ-05
fact. The automatic recovery tick consumes the recorded history into the native
view after both a supplier restart and a new App session reading the persisted
index; an unindexed conversation is a negative control. NV-04 delivery pauses
after recorded parent completion until the consumer observes its still-live
child, then releases the child's separate completion without changing frames.

From `app/`:

```sh
python3 -B supplier_checks/test_recorded_replay.py
CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --manifest-path src-tauri/Cargo.toml --lib recorded_replay_tests -- --test-threads=1
```

The Python checks also run in `npm test`; the actual seam checks run with the
ordinary Rust suite. All homes, peer wrappers and audit output are test-owned
scratch files. The peer's emulated version label is a protocol fixture; Host
standing remains `unverified-development`.

This implementation does not select or rebuild C1, execute a candidate-bound
EXP replay, establish a native witness, or open RUN-A. Existing capture-only
EXP records and U-SQ-5/U-SQ-6 conditions keep their standing. Qualification
still needs the selected candidate and applicable owner inputs. ScopeOfWork
commitments and acceptance criteria are unchanged; this is an implementation
and verification path for those existing requirements.
