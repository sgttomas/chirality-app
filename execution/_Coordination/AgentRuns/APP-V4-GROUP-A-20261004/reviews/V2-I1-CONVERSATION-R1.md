# V2-I1-CONVERSATION-R1 — independent operational transport/terminal backcheck

2026-10-05. Independent TASK `/root/group_a_execution/hosting_contract_review` under WORKING_ITEMS `/root/group_a_execution`, delegated-harness-native; no descendants. Own repository write: this report only. Root/TASK/LOOP/software-code-review/manual basis retained from prior reviews; RECOVERY §3.2–3.4/CV/SR, NIR turn composition/outcome TO/TC clauses, exact maintained 0.160.0 schema and V3 scoped-sender warrant consulted. Product/Design/Git/delegation, supplier/UI/window/model/network/auth/credential operations were not performed.

## Exact candidate and disposition

**READY for manager fan-in of the repaired plain-text/interrupt Host transport and its terminal/live-turn guards. No unresolved blocking finding in this bounded contribution.** Public APIs remain unchanged. Durable SR/cause/quit/run accounting, history/resume/fork/relaunch, public/native integration and actual supplier/provider witnesses remain separate required production; no whole conversation/deliverable or qualification claim.

`changes/I1-CONVERSATION.md` final seal `95085b185a0758d466b5b42cf6e0ae190f703f709ba26f7c3b83cbe251547081`; Host source `fbe61326d878fc92d7301773e38e0781dbaca6f98eb46ba87df06b80b6991510`; reducer/guard section `2ea05e6ed2835a393928325fcb1986ce470a24974882a91d012dcdc1d6328695`; conversation test module `c69d0f237dd2370678b1a9617abf9e67ff2b2023e8454f09ed4b1d63ece435b1`. Whole source and both reported section hashes independently match. Maintained native root digest remains `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5`.

The original inspected source `de157560c4d36436162176ff4fb6c38a1a15be83f57317b860faaa68361d2b49` and its 7/17 author passes remain historical, not re-labelled as the successor. Original review was being completed when the manager dispatched R1. There was no written V2-I1-CONVERSATION.md artifact; this authorized R1 report preserves the actual original finding/reproduction and final disposition rather than inventing such a file.

## Original CONV-M1 (major, blocking then; repaired now)

At original hosting.rs:765–786, remember_turn guarded a terminal entry only against a late turn/start response. A later same-tuple turn/started observation could overwrite nativeTurn.status to inProgress while terminalEventObserved remained true; interrupt eligibility tested status/observationEnded but not the known terminal marker.

Independent exact-helper reproduction: full generation `{appSession:"s",home:"h",spawnCounter:1}`, known thread t. Call unchanged remember_turn with turn `{id:"turn",status:"completed",items:[]}`, source turn/completed at position1, then `{id:"turn",status:"inProgress",items:[]}`, source turn/started at position2. The original cache became:

```text
nativeTurn.status=inProgress
source=turn/started
receiptPosition=2
terminalEventObserved=true
```

check_conversation_request(turn/interrupt, thread t/turn turn) returned Ok(()); independent assertion that the already-ended tuple cannot qualify as known live **FAILED**, exit101, 2.11s compile/0.00s run. These were exact copied source helpers inside a minimal Rust Inner fixture, not reimplemented predicates, actual Host execution or observed stock supplier behavior.

Warrant: RECOVERY CV-05 leaves turn-live on observed completion; SR-01 admits interruption only of a live in-progress turn. NIR TO-1/TO-3 separate live progress from observed completion. A contradictory later active-like report must remain raw evidence without reviving the ended tuple or granting a new interrupt.

Successor fixes both sides: terminal nativeTurn/source/receipt position are retained for the exact full tuple against active-like processed observations and late start responses; incoming source/position/status is added to inconsistencyLimits with an explicit unchanged-journal reference. Raw frames are still journaled unchanged. Interrupt independently requires terminalEventObserved != true, preventing an active-looking/corrupted cached payload from bypassing the terminal fact. Distinct new turn ID remains eligible, so this is not a blanket thread stop.

## Final affected backcheck and checks

Parent granted two short serialized scratch Cargo slots. Scratch lock resolved offline against the approved CARGO_HOME; no repository source or dependency files changed. Exact helpers were refreshed from successor into the same temporary target. Only the original case was rerun with additional nativeTurn/source/position/terminal/limit assertions: **PASS1/1**, exit0, 0.16s compile/0.00s run. It now returns no-live-turn and preserves terminal data plus incoming source/status limit. Slot immediately released; scratch removed after preserving this report. No actor, native process, supplier or model execution was hidden behind the helper test.

Author's reported successor tests are **9/9 conversation** and **19/19 affected Host**, independently read as assertions/source, not claimed reviewer whole-suite reruns. New actual Host regression checks the exact completed→started case, raw extra field/journal preservation, helper/public refusal and no outbound registration; another checks active-like completion notification, late response, corrupted status with terminal marker, and a distinct next turn remaining live. Prior exact-body, ordinary live/end, duplicate/error/timeout/closure, full-generation and stale-response tests remain. No criterion/schema was weakened to obtain a pass. Scoped diff-check passed during inspection.

## Operational source assessment

turn_start_text takes only generation/thread/text and emits exactly native threadId plus input [{type:text,text:unchanged,text_elements:[]}]. Unicode/newline and JSON-looking policy text remain ordinary text, not parameter overrides. turn_interrupt emits only threadId/turnId. Generated TurnStartParams/TurnInterruptParams require those native members. At source level model/provider/role/base/config/approval/sandbox/collaboration overrides are omitted, leaving native thread inheritance; actual supplier/base/role behavior still needs its own parent/provider witness.

Generation validation is full H5. Known current-generation/home thread lookup and live-turn/duplicate checks occur inside scoped registration before request ID/pipe write. The accepted V3 sender discipline remains: acquire actual source pipe while registration/full generation is locked, release state during write but keep source pipe, then release pipe before state re-lock. Stale/closed tuples cannot be newly registered or sent on a successor pipe. After response, full tuple/current ready/open checks refuse stale return before successor mutation; source-bound response/client records remain raw in the journal.

conversationTurns is ephemeral, with full generation/thread/turn and unmodified native Turn/source/receipt position; no durable transcript is asserted. Native turn events, not interrupt response, establish status. Completion-before-start-response remains terminal. Generation closure marks observationEnded with native last status unchanged rather than invent final interruption or descendant end.

Duplicate pending/acknowledged interrupt refuses; native error permits explicit retry, write failure remains unknown-no-response/write-failed, wait expiry remains pending with waitingEnded, and a late matching reply still correlates. Interrupt result object is acknowledgment only: no rollback, turn end, run end or human act follows. turnInterruptRequests retains request binding/client outcome beside a separate native-event outcome statement. modelTurnExercised becomes null after a recorded turn/start attempt; modelTurnEvidence labels protocol records without claiming provider prediction. Mock results/request success are not a model witness.

## Return and remaining production

Release the named APIs for the next combined slice against these exact hashes. Integration must preserve selected known thread/full tuple and uncertainty/draft handling, avoid auto resend on timeout, keep acknowledgment versus native end separate, and show inconsistency limits without changing raw reports. Plain text is not full attachment/plan/workflow/run composition; those joins remain their owners' work. Stop-request/cause/quit records, actual history and relaunch, native human-origin controls, current provider/model execution and qualification remain missing witnesses or production, not discharged here.

This backcheck does not reopen unrelated prior Host/source reviews or approve shared integration/other moving modules. Actual Root/role/skill/manual reading origins remain in V3/prior reports; added RECOVERY/NIR/schema source identity is the named author's preserved basis and current clauses examined here. No other role instruction was activated.
