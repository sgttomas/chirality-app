# I1 operational conversation transport — 2026-10-05

TASK `/root/group_a_execution/runtime_core_production`, parent `/root/group_a_execution`; original Host owner, native descendant, no delegation. Writes: hosting.rs, its inline tests and this record only. Shared lib/UI/runtime_session, Design/schemas/resources/dependency manifests and Git remain untouched. No stock supplier/model/native turn, credentials/auth, network/download or key operation. Mock /bin/cat is env-cleared and reaped.

## Frozen available API

```rust
pub fn turn_start_text(&self, generation: &Value, thread_id: &str, text: &str)
    -> Result<Value, String>;
pub fn turn_interrupt(&self, generation: &Value, thread_id: &str, turn_id: &str)
    -> Result<Value, String>;
```

The text request is exactly threadId plus input [{type:"text", text:<unchanged>, text_elements:[]}]. The interrupt request is exactly threadId/turnId. Maintained 0.160.0 definitions/v2/TurnStartParams requires input and threadId; UserInput text requires type/text and defines text_elements; TurnInterruptParams requires both IDs. Tests compile those unchanged generated targets. No role/base/config/model/provider/approval/sandbox/collaboration override is emitted; the already selected native thread supplies its settings. No renderer actor/origin/authority argument is accepted. The fixed person-directed initiation label is operation routing metadata, not identity verification or reserved-act evidence.

Full H5 generation is validated before dispatch. Known current-generation/home thread identity is checked inside scoped registration before any request ID/pipe write. Existing scoped sender binds the actual source pipe under the registration lock, retains it through writing with state lock released for reader progress, then releases pipe before any state re-lock. Stale/foreign/closed tuples and unregistered threads refuse without sending. This path currently admits only threads in Host's observed current-generation registry; future history/resume integration must populate that registry from a bound native result, not renderer assertions.

## State and observation semantics

Main-process ephemeral conversationTurns contains full generation, native thread/turn IDs, unchanged native Turn and its source/receipt position. Scoped start responses and turn/started or turn/completed frames provide those source facts. A start response after an observed terminal event cannot revive its live status. The all-frame native journal remains unchanged. No durable conversation transcript is created.

Interrupt admits only an observed inProgress turn in the known thread/full generation, and refuses a second pending/acknowledged interrupt (stop-already-requested). A native error permits an explicit retry; a pending wait-timeout remains pending and prevents duplicate automatic dispatch. The acknowledgment object is not a turn end, rollback, run end or human_act. Native turn/completed supplies interrupted/completed/failed outcome; generation closure marks observation ended without inventing a final status. It does not assume descendants ended.

Snapshot turnInterruptRequests links the bound operation to its client request record and explicitly separates turn outcome. Write failure remains write-failed/unknown-no-response; wait expiry sets waitingEnded while outcome stays pending, and a later matching response still correlates. Native errors remain in the raw journal with their data. If full tuple changes after receipt but before wrapper consumption, the wrapper returns an explicit stale result message and no successor state is mutated; the received old-generation native frame/client result remains source-bound.

The legacy modelTurnExercised=false does not persist after a recorded turn/start attempt: it becomes null (unknown), with modelTurnEvidence exposing actual protocol request records and an explicit no-provider/model-witness standing. Request success, a mock result or a native acknowledgment is not provider prediction or supplier qualification.

This is an operational Host path. Durable RECOVERY stop-request/cause/quit/run-tag records, native human UI origins, history/resume/fork/relaunch and actual App/provider/supplier witnesses remain separate production obligations. No checkpoint hold, grant, actor privilege or complete recovery is inferred.

## Actual checks and consumer next step

Cwd app/src-tauri; CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home, manager-granted shared slot.

| Command | Exit/result |
| --- | --- |
| `cargo test --offline --locked --lib conversation_transport_tests` | 0; 7 passed, 0 failed, 0 ignored; 0.07s after 4.62s compile |
| `cargo test --offline --locked --lib hosting::` | 0; 17 passed, 0 failed, 0 ignored; 0.06s |

No test failure or oracle change. Seven new tests exercise actual ChildStdin/correlation with synthetic responses: exact Unicode/newline text and schema-shaped minimal args; text/start response plus interrupt ack and duplicate/end guards; foreign session/home/counter/scalar and unknown identities; native error/data, failed write, wait and late response; completed-event-before-start-response; interrupt error/timeout/closure uncertainty; and deterministic after-response full-tuple transitions for both operations. Existing hosting/guidance/custody tests were included because the shared scoped sender and snapshot changed. No live stock/model witness is claimed. Cargo slot released promptly; no additional checks are pending in this bounded author unit.

Shared integration owner can now consume the signatures with its selected known thread/full generation, send ordinary text, expose separate native turn/interrupt facts and retain draft/uncertainty appropriately. Do not silently resend on timeout or display acknowledgment as ended work. Source is frozen for fresh independent affected review; shared-file implementation and native qualification remain unclaimed.

## Frozen source/basis seals

| Subject | SHA-256 |
| --- | --- |
| `app/src-tauri/src/hosting.rs` | `de157560c4d36436162176ff4fb6c38a1a15be83f57317b860faaa68361d2b49` |
| `new conversation_transport_tests block` | `41fd9166f4f4281f329030748cf96aed8612e92c362c95b639bb347aea5ae172` |
| `conversation methods/helpers section` | `0e351a238d53987456626fb03d1c9dc33574f283b7d0b9c8ec2ff78980f6b869` |
| `maintained native schema bundle` | `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5` |
| `RECOVERY §3.4/4.1/SQ-I source` | `9b443fbc5e7fc617e51e18c4cb8aec7af0d429bc7fefe3e0ec9e52f968aa79d1` |

Test-block boundary is cfg(test)/conversation_transport_tests through EOF. Method section starts at the Plain text only comment and ends immediately before spawn_reader; whole-file seal also covers scoped sender, native frame cache and snapshot updates.

## I1-CONVERSATION-R1 terminal non-revival successor — 2026-10-05

Parent relayed the independent reviewer's exact original helper repro against the preceding de157560c4d36436162176ff4fb6c38a1a15be83f57317b860faaa68361d2b49 source: completed(g/thread/turn), then started for the same tuple overwrote nativeTurn.status to inProgress while terminalEventObserved remained true; check_conversation_request returned Ok for interrupt. This original sequence and prior source seal remain historical evidence; the prior 7/17 passing tests did not cover it. No independent original-version rerun is claimed here.

NIR TO1/TO3 and RECOVERY CV05/SR01/SR11 require terminal/non-live preservation. Source repair changes only hosting.rs's turn reading/interrupt predicate and adds two regression tests in the existing owned test module. API signatures/native bodies, shared UI/lib/runtime_session, Design, records and dependencies are untouched.

remember_turn now preserves the prior terminal nativeTurn, source and receipt position for that exact full tuple against every later processed inProgress payload, including started/completed notifications, and against late turn/start responses. It appends an explicit inconsistencyLimits observation with incoming source/position/status and the unchanged journal reference; the contradictory native frame is still journaled verbatim. This is a guarded App reading, never rewriting or dropping native evidence. Interrupt also checks terminalEventObserved independently of payload status, so an accidentally active-looking payload cannot grant a terminal interrupt.

The exact completed→started regression checks prior terminal payload/source/position, explicit limit, raw extra native field preservation, helper and public no-live-turn refusal, and zero outbound registration. It additionally checks that even a test-corrupted inProgress payload with the terminal marker cannot pass the guard. The second regression covers an active-looking completed notification, late start response, and a distinct native next-turn ID remaining admissibly live. Existing ordinary live/start/end and duplicate/timeout/error/full-generation controls are retained. No original oracle was narrowed.

Approved cache and cwd as above; manager granted Cargo, no other owner executing:

| Command | Result |
| --- | --- |
| `cargo test --offline --locked --lib conversation_transport_tests` | exit0; 9 passed, 0 failed, 0 ignored; 0.07s after 3.46s compile |
| `cargo test --offline --locked --lib hosting::` | exit0; 19 passed, 0 failed, 0 ignored; 0.06s |

No failed run on this successor, test weakening, native/model/credential/network operation or Git action. Mock pipe cases remain env-cleared /bin/cat with synthetic native fields. Cargo released promptly before shared owner's affected checks. Source frozen for the same independent reviewer; actual supplier/native qualification and other conversation obligations remain as above.

| Frozen successor subject | SHA-256 |
| --- | --- |
| `hosting.rs` | `fbe61326d878fc92d7301773e38e0781dbaca6f98eb46ba87df06b80b6991510` |
| `turn reducer/interrupt-guard section` | `2ea05e6ed2835a393928325fcb1986ce470a24974882a91d012dcdc1d6328695` |
| `conversation test module` | `c69d0f237dd2370678b1a9617abf9e67ff2b2023e8454f09ed4b1d63ece435b1` |

Section boundaries: remember_turn through immediately before spawn_reader; test module cfg(test)/conversation_transport_tests through EOF. Original whole-file and test seals above are superseded for this bounded behavior, not silently rebound.
