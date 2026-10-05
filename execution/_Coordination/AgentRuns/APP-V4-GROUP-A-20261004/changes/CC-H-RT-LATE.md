# CC-H-RT-LATE — later known-answerable protocol error transition

2026-10-05. PROPOSED technical amendment applied in DEL-01-01 HOSTING/prototype only; independent review before product mapping adoption. TASK `/root/group_a_execution/design_hosting_access` under WORKING_ITEMS `/root/group_a_execution`, no descendants. No app, other Design, schema, Cargo, Git, shared graph, MEMORY, SoW/register, supplier/network/auth/model-turn changes.

## Recovered requirement and exact repair

CC-REC-R9 and independent V0-REC-R9-LEDGER identify a source-table gap: HOSTING R9/§6.4 already allows a named App-rule or boundary error later on a listed known-answerable request, but RT has no successful later-error edge. RECOVERY is a receiving owner, not permission to invent a supplier transition. This amendment supplies the exact hosting-owned transition without expanding origin authority.

- Accept a valid later protocol error only for the current outstanding known-answerable request, after full H5 namespace/request/state/native-error/origin validation. Origin is the actual explicit boundary origin or nonempty named App rule, never person/agent-origin error. Native code is an integer (not boolean), message is text and content must be JSON-serializable without NaN. Error content/origin remain unchanged.
- Reuse RT-06 into settling after validation. **RT-14** `settling --reply-written-protocol-error--> errored`, guard successful error frame write. Store native error, exact origin, written result and initially not-observed acknowledgment. A failed write instead follows existing RT-09 to settle-write-failed with unknown outcome; no successful frame or acknowledgment inferred.
- **RT-15** `errored --supplier-reported-resolution--> errored`, guard the RT-14 later-error branch only, successful write, subsequent matching full H5 generation/request supplier resolution before generation closure. Observe acknowledgment only; create no new settlement or human act. The scoped model’s frame counters are internal to its one session/home; exported identity remains full H5 and explicit caller identity is checked as the full object. Foreign/bare-counter callers refuse.
- Absence of acknowledgment through closure remains not-observed for custody handling. Wrong generation, after-closure resolution, failed transport and receipt RT-02/RT-03 errors cannot acquire RT-15 acknowledgment. Existing RT-12/RT-13 answer/decline guards and receipt-time `_write_error` behavior remain unchanged.
- Refused origin, empty rule name, invalid native error, stale namespace or already-settled request writes nothing and leaves prior entry state unchanged. No person answer, human_act, reserved act, grant or checkpoint satisfaction arises. The method does not authorize arbitrary autonomous errors or a new timing/error policy; actual named-rule applicability remains the implementation’s R9 obligation.

HOSTING §6.2 state diagram, §6.2.1 rows, §6.4 offered result and exact receiving join now agree. Existing server-entry schema already admits errored/error/written and settle-write-failed/error/write-failed; its shape/id is unchanged. Receipt RT-02/03 remain errored at receipt even when their write failed, as previously defined; they are not retroactively converted to this later branch.

## Exact RECOVERY and production adoption

Receiving owner updates `DEL-01-02/Design/EXECUTION_AND_RECOVERY.md` as part of its own named adoption:

| Hosting result | RECOVERY join | Meaning |
|---|---|---|
| Later successful RT-14 | RQ-03 entry-settled | Listed request closed, endedAs errored, replyWrite written, actual named origin and full generation/request reference |
| Later failed RT-09 | RQ-03 entry-settled | Closed, settle-write-failed/write-failed; outcome unknown, no acknowledgment fabricated |
| Subsequent matching RT-15 | RQ-09 acknowledgment-observed | The later written-error branch only; extend the RQ-09 guard’s current RT-12/RT-13 list with RT-15 |
| Written RT-14 with no ack through close | RQ-05 generation-closed | acknowledgment_not_observed; preserve written settlement, no successful acknowledgment |
| Receipt RT-02/RT-03 | RQ-08 unchanged | Error at receipt with its original result/origin; never relabel RQ-03 |

RQ-03's source list can now explicitly name RT-14 rather than an unnumbered R9 outcome. RQ-09 must explicitly name RT-15 with its written/later/full-generation guard; it must not admit failed-write or receipt errors. CC-REC-R9 remains the receiving proposal; this amendment neither edits it nor claims its production adoption. Independent joined review must cover the exact source/receiver candidates before claiming complete mapping.

I1 consumers: HOSTING reducer/error transport → ledger RQ-03/RQ-09; generation-close missing-ack account; native cards; reconnect/relaunch summaries. Exact origin/full namespace/native content and write-versus-ack uncertainty must survive persistence/replay. Mapping failure remains visible and must not strand later summaries or fabricate RQ-08. RS/EXEC receive only their own custody facts with limits; no stronger act. Manager supplies product mappings/code tests and receiving notices after review. No host one-effect or supplier/App qualification claim.

## Focused evidence

`python3 -B Design/prototype/check_later_protocol_error.py`: exit 0, four case groups pass. Pure Writer double; no supplier process/socket/network. Named-rule and explicit-boundary written error+ack, no-ack closure, failed-write+spurious resolution, wrong-generation acknowledgment, after-close resolution, person/empty-rule/boolean-code/NaN/bare-counter/full-namespace refusal, native error/origin preservation, full exported generation and no human_act examined. Every emitted entry checked against unchanged server-entry schema, including RT-02/RT-03 written/write-failed fixtures.

Focused integration into existing `run_cases.py` registers actually exercised new RT rows for future full-suite coverage; no old oracle is changed. `late_protocol_errors()` plus `hosting_tables()` pass: all 24 lifecycle and 15 register rows equal HOSTING source. Original RT-02/03 helper untouched; exact receipt fixtures pass. No full network/loopback suite rerun needed or claimed for this narrow new path. `git diff --check` passes in owned Design.

```text
PASS named/boundary later error: RT06/14 write, matching RT15 ack, native origin/full H5 preserved; no human_act
PASS written/no-ack close retains lack of ack; failed write RT09 stays unknown/no frame/no ack, even after resolution or close
PASS person/empty-rule/invalid native/full namespace mismatch refuse without state or transport mutation
PASS RT02/03 receipt-time written/write-failed outcomes unchanged; no late-error ack routing
VC-27 (tables in HOSTING) | pass (model) | HOSTING §4.7 (24 rows) and §6.2.1 (15 rows) equal the model's tables
```

## Limitations and reserved matters

Focused model evidence checks this technical transition contract, not actual native transport, durable publication/relaunch, supplier acknowledgment behavior or acceptance/qualification. The observed supplier may resolve a request without reply (RT-10); that remains separate and is never called a person's answer. Error applicability, actual main-process custody/transport and production mapping remain with their respective implementation owners under the existing contract. Independent review/disposition precedes adoption; no extra human gate or scope amendment inferred.

## Read sources / SHA-256

Root/TASK/loop previously supplied and read; this task selectively recovered HOSTING H5/R9/§6.2–6.5, RECOVERY RQ03/05/08/09 later-error join, the two named receiving/review records and unchanged schema. Historical workers and source observations retain their own identities; no replay is claimed as a prior author's act.

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-REC-R9.md` — `b9f1a2e12c17867afa69f16e41049ef229bfbadd43563e4b2d80d88a0639d3a4`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-REC-R9-LEDGER.md` — `6b142b530e47418c659c5687a38196f62b37f247f3e971034cccfffdeb5ba34d`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` — `a19beb59638a954078e093658d326bdeae4a2c9d1241d5ff69d262abc3e9b4b5`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/hosting.server-request-entry.schema.json` — `b295fc5891e3fee8435f1293f731a9939d43383ce80ec87b8a993f35b0adce7f`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/ScopeOfWork.md` — `bbc81a8d31eeacab3497acf297c8c6eeac7b2f6febda5381f332ec14b8f65d02`

## Captured pre-change source identities

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` — `b01ef84d5fcfd494cbf60c81860c5d0ccd159ccb90598147184b6f8c17475cc5`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/prototype/boundary_model.py` — `5925636a0b08bd258b4c5262dddffcdf999fd8add7363cce1b5d290cb20f27a3`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/prototype/run_cases.py` — `0f8816123564038b0a6f0e1f4eb6dfca0dca6993034fd03e8447f36cc8881872`

## Candidate outputs / SHA-256 (record self-hash returned separately)

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` — `47b8f1c6fb01e1f495099b06cd3fc10e95d03c032e8d122ede4378f28e194087`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/prototype/boundary_model.py` — `1cdffd0c0eec01e5e8864f9984332615828204a53f77edbd37902f6522d2b632`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/prototype/run_cases.py` — `bca41f423ff7104447870f30513197d6ef6a4906ffccfb052619f5c778d32648`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/prototype/check_later_protocol_error.py` — `6e22c12b1324bb60600d4b9993d72c0e47295eaf4d80c6dc0bd6e70cb468aee7`
