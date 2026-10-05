# Independent I1 steering transport review — 2026-10-05

TASK `/root/group_a_execution/hosting_contract_review`, parent `/root/group_a_execution`; native descendant, no delegation. Software-code-review applied. Write scope is this report only. Product, Design, schemas, Git and dependency files unchanged; no native/model/provider/UI launch, network, authentication or Cargo execution.

**READY for bounded Host text-steering transport fan-in.** No blocking, major or minor actionable finding in the frozen branch and affected sender/lifecycle paths. This verdict does not qualify the supplier or approve broader History/UI/attachment/workflow support.

## Exact candidate and supplied basis

| Subject | SHA-256 |
| --- | --- |
| hosting.rs | `d20d8ef399911f49f4604fa9530703c91a1f83cf0885e9609885dd12e39f6c75` |
| changes/I1-STEERING.md | `f0d5a929b3978bef72c3af66c08b00c5855e9a8d36190c8b3c2ff808853fa7dc` |
| maintained 0.160 native schema bundle | `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5` |
| HOSTING_BOUNDARY.md | `47b8f1c6fb01e1f495099b06cd3fc10e95d03c032e8d122ede4378f28e194087` |
| EXECUTION_AND_RECOVERY.md | `9b443fbc5e7fc617e51e18c4cb8aec7af0d429bc7fefe3e0ec9e52f968aa79d1` |
| ATTACHMENT_DECISION_PREPARATION.md | `24c2908fd651cca447f88e50030202a04c26560e6012673ab086f0d8ad763299` |
| accepted V2-I1-CONVERSATION-R1.md | `01084bf59381e38fc12c66c559dc4c1f9790ebd0784da6e41adf5b03c491ea62` |

Root/TASK/project loop and skill origins remain recorded in the preceding reviews. No other role instructions activated. The review deliberately carries the accepted scoped sender and terminal non-revival warrant forward, then assesses the added steering branch, start-request receipt boundary, current-target selection and affected assertions directly. Source and record seals were independently verified.

## Source assessment

At hosting.rs:737–745, `turn_steer_text(generation,thread_id,expected_live_turn,text)` builds only `threadId`, `expectedTurnId`, and native text input `{type:"text",text:<unchanged>,text_elements:[]}`. Empty thread/expected turn/text refuse. Published TurnSteerParams requires these three members, and its expectedTurnId description explicitly requires the active turn; TurnSteerResponse requires turnId. Unicode/newlines and JSON-looking content stay text. No attachment context, role/base/config/model/provider/approval/sandbox/collaboration override or fallback turn/start is introduced. Omission preserves native inheritance at the wrapper source boundary; actual supplier carriage and inheritance still require their own witness.

At scoped registration (hosting.rs:590–626), the full expected generation/open-ready checks and known current-generation thread/live expected-target check run under the state lock before ID allocation and source-pipe acquisition. The accepted sender discipline remains: acquire actual source pipe while registration is locked, release state during write while retaining that pipe, release pipe before re-locking state. This prevents a rejected old tuple being newly registered against a successor pipe; native expectedTurnId additionally guards any change after the local reading. No automatic resend occurs.

At hosting.rs:820–829, the current target is read from current-generation raw started/completed receipt order and guarded memo facts. A delayed earlier start response cannot replace a newer native event: its dispatch receipt boundary is retained at registration and attached only to the corresponding source-bound response memo. One fresh response-only in-progress target may establish the target; multiple such candidates refuse as ambiguous. An observed terminal tuple, ended observation, completed latest event without a distinct fresh target, or contradictory later active-looking terminal memo cannot qualify. The previous terminal nativeTurn/source/position preservation and independent terminal marker guards remain intact; distinct new turn identity remains usable.

At hosting.rs:753–775, reply consumption rechecks full generation/open-ready before returning success. Raw native errors are returned as errors with journal evidence retained. A native result reporting another turnId refuses without rebinding. A changed/ended/ambiguous target after receipt refuses with its received response/client correlation retained. Steering success never edits conversationTurns or promotes acknowledgment to turn completion, rollback, run end, human-act proof or model prediction.

The existing source-bound correlation and uncertainty paths are preserved: write failure remains write-failed/unknown-no-response, expiry ends waiting while the request remains pending, a late matching reply may still correlate, and generation closure ends observation without fabricating native final status. Raw response data and contradictory notifications remain in the journal, separate from guarded eligibility. Existing text-start and interrupt body/signature/duplicate/lifecycle semantics are unchanged apart from the recorded start dispatch boundary used by the new target selector.

## Verification assessment and return

Author reports actual isolated offline checks: steering **5/5** and conversation transport **14/14**, both exit0. I inspected all five new assertions and affected old conversation assertions rather than claiming a reviewer rerun. Their oracles independently agree with the schema and governing distinction: exact body/ack without state edits; pre-registration stale/foreign/unknown/terminal refusal; raw native mismatch/error, failed write and late reply; post-receipt target/terminal/full-tuple changes; delayed older response versus newer native event, plus distinct fresh response-only control. The terminal-marker corruption negative checks an independent guard rather than only mirroring the reducer. No schema/criterion weakening was found. No suspected defect required a focused scratch execution; no Cargo slot acquired.

Release this exact Host API for the next bounded consumer slice. Consumer integration must retain the observed current full tuple/thread/expected turn, surface refused/unknown/waiting states, keep the draft on uncertainty, avoid fallback start or automatic resend, and distinguish steering acceptance from observed native lifecycle. Actual stock supplier/model execution, shared UI behavior, durable custody/relaunch/history and wider NIR/attachment/workflow support remain separately unfinished. This report does not reopen unrelated reviews or approve moving consumer modules.
