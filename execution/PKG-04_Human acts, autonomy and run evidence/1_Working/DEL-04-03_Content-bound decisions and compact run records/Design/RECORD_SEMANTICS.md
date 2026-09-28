# Record Semantics
- Contribution: DEL-04-03/RS-v0.5
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 and OUT-004 (definition content); OUT-002 and OUT-003 (behaviour and fixture design only — no writer, reader or fixture exists); REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; AC-001…AC-007 via designed VER-001…VER-006
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 74d42c38eaf2a6638b75bc5184f1741bc7d4f17171662a05a233d40f245340c1; `P/docs/PRD.md` §4.3 V4-EXE-01…03, §4.5 V4-AUT-01…05, §4.6 V4-PM-06, §4.7 V4-REC-01…05, §10; `P/docs/HOST_INTEGRATION.md` §1, V4-HI-04, V4-HI-11/12, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-50…52, V4-HI-70/71, §11; `P/docs/ARCHITECTURE.md` §4, V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-21/22/31; `P/docs/OPERATING_METHOD.md` V4-OPS-30…32; `DECISION_BRIEF.html` d2, d3; `OWNER_DIRECTIONS.md` J, O; `SCC-CASE-002/Case_Datasheet.md` M1, M2, M3, M3-CP; `_Decomposition/Open_Issues.csv` OI-001/002/013/014/021; `External_Dependencies.csv` DEP-001. Run folder `APP-V4-FIRST-INCREMENT-20260928` at commit **8fb51f07f**: `OWNER_DECISIONS.md` (DECISION-1 and DECISION-2; sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c); `R1_RESOLUTIONS.md` (2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4); `R2_RESOLUTIONS.md` (77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088); `R3_RESOLUTIONS.md` (202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf); `R4_RESOLUTIONS.md` (50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24); `R5_RESOLUTIONS.md` (254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1); `reviews/V2.md` (75ba1dff8a0c4fa2eb294471127147cbd19a0925daf9169b32ddc88727dde6ef); `reviews/V3-A.md` (f25f5af1177b7fe2a698bd4ef1e1caafa4c2ef25cfc73111f031e17c7cc21d87); `reviews/V3-B.md` (5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3); IR1-A/B/C and V1-A/B/C as cited in RS-v0.3
- Consumed inputs: DEL-04-03/RS-v0.4 (sha256 56806b64b12a946e706ff236dd1c25fe27ac00877aac13b50ee8603aaf540199, commit cc58211c5). Current sibling versions read from commit **8fb51f07f** with `git show` (not the working tree): DEL-02-03/EXEC-v0.2 `EXECUTION_COMPATIBILITY.md` sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0 (§2 HP-4/HP-H, §3.3 CR-14, §3.6, §4.5, §4.7, §4.9, §4.10); DEL-03-01/C-v0.4 `CATALOG_AND_READ_BASIS.md` sha256 e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c (§10.1 FXA-1…FXA-5, LIB-A1/A2, AF-1; §10.3; §10.4); DEL-04-01/ACT-POLICY-v0.4 `ACT_AND_POLICY_CONTRACT.md` sha256 d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b (§2.4); DEL-01-01/HOSTING-BOUNDARY-v0.4 `HOSTING_BOUNDARY.md` sha256 201ea32005dd2c9fb5281a376eb25eebfcb5a644d09a6d3bf5901aaf934c7e58 (§8.3); DEL-03-03/ADAPTER-v0.2 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc. R6 in-place pass (no version bump): C-v0.5 `CATALOG_AND_READ_BASIS.md` sha256 a6306bd477decad22d4405fb86ca6212fb189e4865c68dbbcba90e1335be7a29 (§10.4 V-GR1, GR-1…GR-3, GR-P/GR-R/GR-S) and DEL-02-03/EXEC-v0.3 `EXECUTION_COMPATIBILITY.md` sha256 889e48819baa21ec112c4878e4e38004dcbaa9eb3645a31c24221ac116ee548e (§3.6 HS-1…HS-5, F-24), read at commit d3cebd1cc for the R6 in-place pass; R6_RESOLUTIONS.md and reviews/V4-A.md at commit c7f5513db. The R5 elements earlier marked "per R5-n" (V-GR1, the R5-1 values, P §3.3 carriage) are now present in those sibling texts. DEL-04-02/AS-v0.5 was revised concurrently by the same executor; §8 here and its §6 are byte-identical.
- Receivers: CASE-002 M1 — DEL-02-01 (OUT-001/002; REQ-003; VER-003), DEL-02-03 (OUT-001/002; REQ-003; VER-003), DEL-04-02 (OUT-001/002; REQ-002/004; VER-002/004), DEL-05-01 (OUT-001/004; REQ-005/007; VER-008), DEL-05-02 (OUT-001/003; REQ-001/003; VER-001/003); DEL-01-04 and DEL-02-02 are outside this undertaking (D1). CASE-002 M3 — DEL-04-02 (OUT-001/003; REQ-002/004/005; VER-002/004/005). Dependencies.csv DEP-04-03-011…016 — PKG-02, PKG-03, PKG-06, DEL-04-02, DEL-09-11, external host run recording. By join (not registered): DEL-03-03 (external dispatch entries, destination, evidence limits), DEL-09-06 (transfer links).

## Changes from v0.4

The v0.3 → v0.4 change table is preserved in RS-v0.4 at commit `cc58211c5`.

| Item | Change in v0.5 |
|---|---|
| R5-1 (V3-A MAJOR-1) | R8 hold support uses the four ruled values: **enforced by the host loop** · **enforced on the host route** · **not established** · **not enforceable**. EXEC-v0.1's "enforced before dispatch" and "held after observation" are retired. The workflow requirement consequence is recorded with the value (*not established* is never a pass and never *unsupported*; *not enforceable* → *unsupported*) |
| R5-2 (V3-B MAJOR-1) | §5 carriage assurance: **host-held** covers host derivation or host verification against its own declaration copy (and the host loop's own evaluation); a constraint the host only received keeps its source's assurance; **App-assured is not available in this increment**; only host-held satisfies R2-12 |
| R5-4 (V3-A m-11; Y-3) | R5 records the model destination **per turn** (requested and effective kept separate; reroutes with their turn; unobserved turns *unknown*); the run-level value is the **set** observed; a switch starts no new run. D16 split: "may flow; no gating" SETTLED by DECISION-2; "record and show" relabelled **INTEGRATION (DECISION-2 reading)**. E12 and VC-22 updated |
| R5-5 (Y-4) | L-12: a lapse re-holds whatever caused it, including the person's own undo; OE-8 and R11: the person's own operations are never *action during hold*; an undo never re-holds an A5 arrival. E6 extended |
| R5-6 (Y-5) | §3 and §5: an operation that performs a reserved act (OP-C6/C7/C8, the A12/A13 controls) produces the human-act record, and its R7 entry references it; the person's A1/A2 stay R7 operations. E1 and E2 cite it |
| R5-7 (V3-A MAJOR-3/MAJOR-5; Y-6) | E7 and VC-13 re-pointed to **V-GR1** (per R5-7; C adds it): CP-grant arrives at r15, T15's A12 is captured after the arrival, the held OP-C9 call is dispatched unchanged as T16; sub-variants pending, refused, confirmation lost, later established A12. On the main timeline T15 is before any CP-grant arrival and does **not** count. L-RS-3 removed. L-13 notes the owner-visible cost |
| R5-8 (V3-A MAJOR-2) | E10 and VC-17: "held after observation" and "run stops" removed. The App run shows hold support **not enforceable** (App-only checkpoint → workflow *unsupported*) and records dispositions and **action during hold** with no claimed stop; a host-operation variant over X shows **not established** (awaiting SQ-02) |
| R5-9 (V3-A m-2, m-3, m-12) | Citations re-pointed to current sibling versions (EXEC-v0.2, C-v0.4, ACT-v0.4, HOSTING-v0.4, ADAPTER-v0.2) at commit 8fb51f07f; C fixture assumptions cited **FXA-n**; stale "C declares only V-CP1" reasons replaced (C FXA-5 declares CP-accept **and** CP-check); E1 uses FXA-5's CP-accept arrival; App-side subjects LIB-A1/LIB-A2/AF-1 used where relevant (VC-27) |
| V3-A m-9 | Annotation string unified: **"waiting — re-held, lapsed at ‹t› after resume"** (R8, L-12) |
| R6-1 (in place; V4-A MAJOR-1) | Hold support is classified by the checkpoint's **held actions**: all host operations → HS-3, valued by SQ-02 status (enforced on the host route · not established · not enforceable); any App-side held action → **not enforceable** in App runs (HS-5). R8 states the rule; E10 CP-row-check classified (holds App agent turns → not enforceable) and variant (vii) (holds only a host operation → not established while SQ-02 is unanswered) |
| R6-3 (in place; V4-A m-4) | L-12, OE-8 and R11: the run **stops** only under *enforced by the host loop*; under *enforced on the host route* the host refuses the held host operations and every other run action is *action during hold*; under *not established* / *not enforceable* nothing is stopped and actions are *action during hold* |
| R6-5 (in place; V4-A m-13; EXEC F-24) | R11 *action during hold* carries the **turn initiator**: person-directed · agent · App rule |
| R6-4 / V4-A m-1 (in place) | Stale markers removed: V-GR1 is cited from C-v0.5 (run 13; GR-1…GR-3, GR-P/GR-R/GR-S) instead of "per R5-7; C adds it"; header cites C-v0.5 and EXEC-v0.3. R6-2: V-GR1's `CP-grant` via X is *not established* (HS-3, SQ-02 unanswered) |

## 0. Reading this definition

- Element names are **semantic names, not wire names**. No serialization,
  field spelling, type, file path, persistence, transport, hash or
  canonicalization algorithm, process placement or shared-component placement
  is selected (SoW TBD-002; OI-013; OI-014; DEL-03-01 TBD-003).
- `⟨…⟩` is an opaque identity token. Equal tokens stand for "the designated
  identity method reports the same identity".
- **Act names (DEL-04-01 §2.1):** A1 propose · A2 apply · A3 examine · A4 mark
  checked · A5 accept · A6 approve (engineering approval only) · A7 rely · A8
  request · A9 record · A10 reject · A11 withdraw · A12 set grant · A13 enable
  external access · A14 answer tool permission. A9 is a recording act; A14 is
  never a human-act record (R2-8).
- **Class values (DEL-04-01 §8.1; R2-1):** none · may apply within granted
  autonomy · proposal only · reserved to the person (SETTLED, V4-HI-02) · **no
  policy basis**, with reason ∈ {omitted, unassigned, pending OI-021}
  (INTEGRATION).
- **Reserved to the person.** ADOPTED by D2: A4; A5 wherever the active
  autonomy requires a proposal; A6; A7; A12; enabling external access (A13).
  DERIVED: A10 wherever A5 is; operations that perform any of these (R2-2).
  INTEGRATION: disabling external access is also a person's A13 (R2-3). The SWB
  model-change class (DEL-04-01 P-03) is *may apply within granted autonomy*
  (DERIVED), default *propose*. Operation-specific additions await OI-021.
  Host adoption is not shown (DEP-001).
- **Grant value** (direct / propose) is what the person sets; **treatment** is
  what the host route resolves.
- Examples are **fixture subjects** from DEL-03-01/C-v0.4 §10 (FX-PIPE-01).

## 1. Settled distinctions relied on

| # | Settled distinction | Citation |
|---|---|---|
| D1 | Workflow definitions, the person's decisions and accepted records are ordinary files in the user's project or workspace | V4-REC-02 |
| D2 | A harness session store is operational, not the authority for any human act; coordination views are derived and rebuildable | V4-REC-03; V4-PM-06 |
| D3 | Host domain truth stays in the host's own store | V4-REC-01 |
| D4 | Host receipts, hashes and origin marks evidence what changed; the run record links them and does not copy them | V4-HI-71; V4-REC-04 |
| D5 | `success` means it ran; a submitted proposal is "queued" until the host records acceptance and application | V4-HI-25 |
| D6 | Proposal lifecycle drafted → validated → queued → accepted → applied (receipt), with rejected / withdrawn / stale, and outcome unknown | V4-HI-23 |
| D7 | Only observed events are shown as having happened; an unobserved outcome is unknown | V4-EXE-03; V4-EXM-31 |
| D8 | A human act binds to the content it concerns and lapses visibly when that content changes | V4-HI-32; V4-REC-05 |
| D9 | "accept", never "approve", for proposals | V4-HI-33 |
| D10 | No fabricated human act; faithful recording of an actually performed act is permitted | V4-HI-31; V4-AUT-03; d3 |
| D11 | Acts are distinct subjects; evidence of one establishes none of the others; no acceptance-first chain | d3; V4-AUT-03 |
| D12 | Nothing agent-produced is presented as certified, sealed, approved or code-compliant | V4-AUT-05 |
| D13 | Git history and reviewed pull requests are primary change records | V4-OPS-31 |
| D14 | Reserved to the person (first increment, App/shared): mark checked; accept where autonomy requires a proposal; engineering approval; reliance; changing the grant or enabling external access. No grant widens past a reserved act or declared checkpoint. The host names and enforces its own list | OWNER_DECISIONS D2; V4-HI-30 |
| D15 | App routine tool-permission and sandbox modes are the user's own Codex setting per project/turn; they govern tool execution only and never stand in for a reserved or professional act. Hosts have no classifier permission mode in the first increment | OWNER_DECISIONS D3 |
| D16 | Host content read by the App's Codex through the external channel may flow to the App conversation's selected model, cloud included; the App does not gate on the model destination. A host may restrict its own channel (DEP-001); V4-HOST-02 still governs the host's embedded agent. (That the App **records** the destination per turn and shows it in the channel status is **INTEGRATION (DECISION-2 reading)**, R4-1/R5-4, not part of this settled row) | OWNER_DECISIONS DECISION-2 D5; R5-4 |

App-side run holds at checkpoints are `UNRESOLVED{D6}` (DECISION-2 D6,
deferred to SWBPIPE SQ-02). This format records hold support with the four
R5-1 values and action during hold; it never records an App hold as enforced
when it was not (R4-2). SQ-02 can decide holds only for checkpoints on host
operations; App-only checkpoints stay **not enforceable** whatever it answers
(R5-10).

## 2. Ordinary-file authority rules

(Renamed OF-n in v0.4; C §10.1 cites its fixture assumptions as FXA-n.)

| Rule | Statement | Serves |
|---|---|---|
| OF-1 | The authority for "person P performed act K on content C for purpose U" is an **act record** in an ordinary project/workspace file together with the evidence it references. Nothing else supplies a missing act. | REQ-001, REQ-003; AC-001 |
| OF-2 | Harness session content, transcripts, agent memory, derived views, search indexes, PEC projections, A14 settlements and user-input/elicitation answers may **locate** evidence. Their assertion that an act occurred creates none. | REQ-001; D2; D15; R4-12 |
| OF-3 | Host domain truth, receipts, hashes and origin marks stay with the host. A record holds **references** plus what is needed to resolve and compare them: reference, claimed identity, identity method designation, resolution status. Never a substitute copy. | REQ-002; D3, D4 |
| OF-4 | Workflow definitions and accepted records remain owned by their producing deliverables; this format supplies the act and run records that refer to them. | REQ-001, REQ-005 |
| OF-5 | A written act record is not edited to change actor, act kind, bound content, scope or purpose. A correction is a new record naming the corrected one; both remain readable. Supersession of A12/A13 (L-0) is a relation, not an edit. (Proposed; mechanism unselected.) | REQ-003, REQ-004 |
| OF-6 | Git history is the primary change record for the files (D13); records cite a repository revision where their own revision matters. | AX-003 |
| OF-7 | Each record identifies its **format version** and **record kind**; a reader refuses or limits an unknown version. | OUT-001 |
| OF-8 | The **recorder** is always identified and is never the decision actor merely by having written the record. A person's own act captured in a surface is *direct capture* by that surface, not self-recording. | REQ-003; D10 |
| OF-9 | App runs keep records with the user's project/workspace; host-agent runs keep records with the host project (V4-HI-70). Path and host persistence are not selected (U-05, U-06). | REQ-001, REQ-005 |

## 3. Record kinds and identity

| Record kind | Authority for | Produced by |
|---|---|---|
| Run record | That a workflow run occurred with the identified workflow, conversation, model and destination, settings, requested operations and observed outcomes, linking host evidence | App writer (OUT-002) for App runs; host run recording (external owner, DEP-04-03-016) for host-agent runs, in the shared meaning |
| Human-act record | That an identified person performed A4, A5, A6, A7, A10, A12 or A13, or A11 when the person is the proposer, on identified content, scope and purpose, with capture evidence (ACT §2.4). A person's own proposals (A1) and applications (A2) are R7 operation entries with author type *person*, not human-act records. An operation that **performs a reserved act** (C OP-C6/OP-C7/OP-C8; the A12/A13 controls) produces the human-act record of that act, and its R7 entry, if any, references it (R5-6) | A recorder: capturing surface, App, host facility, or an agent performing A9 |
| **Act-declined event** | That a person decided **not** to perform a required A4, A6, A7 or A12 on an identified subject, with capture evidence (R2-5). Not an act of that kind; satisfies nothing that requires the act | Same recorders |
| **Act-lapsed event** | That a performed act was observed lapsed at ‹t›, with c₀/c₁ (R2-19) | Record reader/writer on evaluation |
| **Run-resumed event** | The resume point of an arrival: {arrival, time, first action reference} — the first run action after the arrival became *performed* or *resolved negatively* with a proceed/return path (EXEC HD-5; R4-3) | Executor (App: DEL-02-03; host: loop) |
| **Run-ended event** | That the run stopped (V4-EXE-01): who stopped it (the person, or the observer reporting an end), cause (e.g. "stopped by declared negative path", "interruption not recovered"), and which arrivals were then *waiting* (R2-5; EXEC RE-4) | Run writer |
| Decision / accepted record | A PKG-06 or workflow-owned record an act record may cite | Its owning deliverable |

Common identity elements: *record identity*, *record kind*, *format version*,
*recorder identity*, *recording context* (App, or host identity),
*written-at order*, *corrects* (optional).

**Run finality (R4-4; EXEC §4.9; PROPOSED).** A run with a run-ended event is
closed and never resumed. Its arrival dispositions are final, except the
R2-19 change from *performed* to *lapsed* on a later lapse. An act performed
after the run ended is recorded and marked **"after run end"**; it changes no
disposition of the ended run. Continuation is a **new run** whose run record
carries **continues ⟨run⟩**; nothing carries into it (no arrival, disposition
or act). An interruption without a run-ended event is not a run end.

## 4. Run-record inventory

Every element named in REQ-002 / SOW-186 / V4-HI-70 is present. "Required"
means present as a value or as an explicit absence statement; *not
applicable* is allowed only with its reason. Elements marked **addition** go
beyond the SoW inventory and name their source.

| # | Element (semantic) | Meaning | Supplier | Absent / unknown handling |
|---|---|---|---|---|
| R1 | Run identity | Stable identity of this run, distinct from conversation, proposal and operation identities; **who started it** (EXEC RE-5); **continues ⟨run⟩** where this run continues an ended one — **addition** (R4-4) | Record writer | Required; *continues* absent unless recorded |
| R2 | Workflow identity as observed | {kind, origin, source root, name, revision} + derived-from; promised vs observed separate. Trace links as separate facts (EXEC §6.1): *listed*, *selected*, *resolved* with **revision verification** outcome (recomputed content identity equals the revision, or "revision not verified"); holding library at listed/selected/resolved, never in identity equality (EXEC §6.2, confirmed). **Transfer links** — exported, relayed, received, adapted — with transfer identity and **carriage-manifest reference**, each marked original or revised identity — **addition** (R4-11) | DEL-02-01 §6.1; DEL-02-03 §6 | "revision not verified", "relay not evidenced", "receipt not observed" stay explicit; a revised identity never inherits a link of the original |
| R3 | Supplied guidance identity and limits — **addition** (R-10; R2-20) | Per thread and turn, source identity and content identity (with method) of each guidance input supplied; "supplied ≠ adopted" | DEL-01-01 (App); host loop (relay) | *unknown* where not recordable |
| R4 | Conversation reference | Reference to the harness conversation/session | Harness | Reference only — operational, not authority |
| R5 | Model used and **model destination** | Model identity and serving endpoint class as observed, separate from configured. **Destination** (INTEGRATION, DECISION-2 reading; R4-1, R5-4): recorded **per turn** where the supplier reports it (HOSTING §8.3) — the **requested** provider/model and the supplier-reported **effective** one kept separate, each **re-route** recorded with its turn, destination class (local model server / user-chosen cloud) from the person's provider configuration; a turn not observed is *unknown*. The **run-level value is the set** of destinations observed, never a single inferred value. A model switch or re-route starts no new run and affects no disposition. Covers host content read over the external channel. Information only — never a gate, never a permission | DEL-01-01 HOSTING §8.3; DEL-05-01; DEL-03-03 | "Requested X; effective unknown" and unobserved turns are valid |
| R5a | Seat role meaning — **addition** (R-7) | The role meaning in force for the acting seat | DEL-05-01 / DEL-02-01 | *unknown* where not determinable |
| R6 | Autonomy settings | Every settings version in force, requested or refused for the run: scope; per-class grant value and class value; display state (§8 list); requester; setting actor; A12 act reference for person-set states; policy-class record reference and default for *effective (policy default)*; establishment evidence or refusal reason | DEL-04-02 settings-in (§8); DEL-04-01 | Never shown effective without its evidence |
| R7 | Requested operations | One entry per submission, read, examination, or loop-side refusal (§5) | Loop/adapter trace; DEL-03-01; DEL-03-02; DEL-03-03 external dispatch entries | Required per request made |
| R8 | Checkpoints and arrivals | Per declared checkpoint: required act kind (closed list A4, A5, A6, A7, A12; outside → *invalid*; unrecognized → *not established*); **subject class** (own element, R2-17/R3-1): change items of a named proposal · named output · **objects a named output concerns** · objects changed by a named outcome · targets of the held call (kind (a) only) · grant setting; **hold support** on the acting surface, one of the four R5-1 values (owner EXEC §3.6): **enforced by the host loop** (embedded route; host evidence DEP-001) · **enforced on the host route** (host-held constraint, evidenced by SQ-02 and a candidate) · **not established** (awaiting a host answer or unagreed exposure; the workflow requirement check is *not established*, never a pass and never *unsupported*) · **not enforceable** (no mechanism on this surface; workflow *unsupported*) — **addition** (R4-2; R5-1). The value is classified by the checkpoint's **held actions** (R6-1): if every held action is a host operation (HS-3), SQ-02 answered with host-held carriage evidenced → *enforced on the host route*, unanswered → *not established*, answered with no host-held route → *not enforceable*; if any held action is App-side (App agent turn, App tool/harness action, App file write or return step), in App runs → *not enforceable* (HS-5, D6); host loop → *enforced by the host loop*; an invalid declaration takes **no value** (HS-1; check *not established*); governing checkpoint constraint issued with its carriage assurance. **Per arrival** (EXEC §4.1): **arrival ordinal**, arrival event and its evidenced time, bound subject referents and their content identities, disposition (waiting · performed · resolved negatively · lapsed · not reached · unknown), **performance ordinal**, satisfying act / A10 / act-declined references, per-item decisions (A5 · A10 · undecided · left · unknown) with *partial* annotation and item-left events, annotations (lapsed at ‹t›; **waiting — re-held, lapsed at ‹t› after resume**; **replaced by arrival n+1**; **A12 awaiting control confirmation**; **A12 refused by control: ‹reason›**; **prior act not counted**; act order unknown; act on other content; subject absent; hold not enforceable; **after run end**), run-resumed events, act-lapsed events, run-ended event if the run ended while waiting | DEL-02-01 declares; DEL-02-03 hold machine (App); DEL-05-01 (host) | Not observed → *not reached*. Run ended while waiting → stays *waiting* with run-ended event |
| R9 | Human acts | References to human-act records, act-declined events and act-lapsed events | §6 | None created without capture evidence |
| R10 | Agent examination findings | References to A3 findings (e.g. C OP-C3) | Agent output | Never "host checks passed" (that is a host check, e.g. C OP-C12), never A4. Host-stored findings through a change operation are also R7 (U-14) |
| R11 | Evidence limits | Lost acknowledgement; missing receipt; unresolvable reference; origin mismatch; omitted governing checkpoint constraint; constraint carried only model-supplied; **unverified caller identity** (R4-15); cited basis not observed; agent-written configuration; native hint mismatch (DEL-03-03); **action during hold** — each **run** action taken while an arrival was waiting and not stopped by the hold (every run action under *not established* / *not enforceable*; under *enforced on the host route*, every action other than the refused host operations), with its reference and its **turn initiator** — *person-directed* · *agent* · *App rule* (R4-2; R6-3; R6-5; EXEC HD-4, F-24); the person's own operations (e.g. an undo) are never action during hold (R5-5); unobserved adoption | Record writer; DEL-03-03; DEL-02-03 | Required |
| R12 | Record identity elements | §3 common elements | Record writer | Required |
| R13 | Tool-permission settlements (A14) — **addition** (D3; R2-8) | Each tool-permission request and its settlement origin: the person via interaction; the user's own Codex mode inside the supplier; an App named-rule decline or explicit error (INTEGRATION: the App never answers affirmatively by rule) | DEL-01-01 observed facts in this undertaking; DEL-01-02 later (D1) | **Only here**. *Not applicable* in host-loop runs (D3) |
| R14 | Compatibility-report reference — **addition** (R4-11; EXEC §3.3) | Reference to each required-tool compatibility report evaluated for the run (report identity CR-1, occasion, pass result CR-10, per-checkpoint hold support CR-9) | DEL-02-03 | "no report evaluated" stays explicit |

### 4.1 Elements added in v0.4 (R4-11)

| Element | Home |
|---|---|
| Arrival ordinal; performance ordinal | R8 (per arrival) |
| Run-resumed event | §3, R8 |
| Re-held and replaced annotations | R8 |
| A12 control effect (established · pending · refused · unconfirmed) | R8 annotations; §6.1 relations; L-0 |
| "Prior act not counted" | R8; L-13 |
| Continues ⟨run⟩ | R1; §3 run finality |
| Action during hold | R11 |
| Transfer links; revision verification | R2 |
| Compatibility-report reference | R14 |
| Model destination | R5 |

## 5. Operation entries and outcome evidence

**Entry elements (semantic).** Operation identity and version (DEL-03-01);
**request-side origin** per DEL-03-02 §3.3: author type (person / agent),
author identity (the person, or the agent seat instance; over the external
channel **unverified** until a caller-identity mechanism exists, R4-15),
seat role meaning, channel, conversation, workflow identity (R2), workflow
run, standing at drafting, settings reference at route decision, settings
reference at application (host-reported, otherwise *unconfirmed*), reason,
and the **governing checkpoint constraint** {workflow run, checkpoint name,
required act A5, operation} with its **carriage assurance** ∈ {host-held,
model-supplied, absent; App-assured is **not available in this increment**}
(R2-12; R4-14; R5-2). Host-held means the host derived the constraint from its
own resolved declaration copy or verified a received one against it
(including the host loop's own evaluation); a constraint the host only
received keeps its source's assurance. Only host-held satisfies R2-12;
model-supplied or absent is an R11 limit; **host origin-mark reference**
(linked; mismatch → R11); **relied-on basis**; **observed basis** for reads
and examinations; **evaluated basis** on every non-success; route (direct /
proposal); treatment at resolution where it differs from standing at drafting;
**proposal identity**, lineage, per-item **change-item content identity**;
item dispositions with actors; **outcome**; receipt references; **resulting
objects** (R2-14); standing received; **submission ordinal**; **reverses
⟨receipt⟩ (entry ⟨ref⟩)** for an undo; **observer** for outcome unknown;
whether the action was taken **during hold** (R11); for an operation that performs a reserved act, the **reference to the human-act record** it produced (R5-6).

**Outcome vocabulary** is DEL-03-02 §9 and DEL-03-01 §4.1, adopted unchanged
(R-7), with R2/R4 amendments:

| Outcome as recorded | Minimum evidence referenced | Actor / observer | May NOT be inferred from |
|---|---|---|---|
| not offered (loop-side, never dispatched) | Operation absent from the catalog edition offered to the loop (R2-4) | Loop | Any host response |
| unavailable | Failed precondition, reason, evaluated basis (HI-04 parity) | Host | Channel off; a class reason |
| not exposed on this surface | Host-declared per-surface exposure element, relayed (R2-4) | Host (relayed by loop/adapter) | *unavailable*, *missing*, *channel not enabled*, or a class reason |
| channel not enabled | External access off; A13 not performed | **App** when its own configuration is off; **host** when the host channel is off (R4-16) | *unavailable* |
| not permitted | Governing treatment and policy record — or the governing checkpoint constraint — and evaluated basis. Reserved entry: an A8 is **offered**; an A8 record exists only if issued (R2-4). Never converted into a proposal | Host route | A class reason rendered as unavailable or not exposed |
| error | Error identity, evaluated basis, effect statement | Host | — |
| drafted / validated | Host validation result (validated) with treatment and settings reference | Proposer (A1) / host | Agent assertion |
| refused — invalid | Host validation refusal with catalog error | Host | — (never "rejected") |
| refused — stale | Reason; relied-on and current bases; affected items | Host | Local comparison alone; a retry's own effects (R2-13) |
| queued | Host acknowledgement | Host | Transport completion |
| accepted (per item) | A5 human-act record bound to the item's change-item content identity | Person (A5) | Success, receipt, agent statement |
| rejected (per item) | A10 human-act record | Person (A10) | Host refusal; silence |
| withdrawn | A11 record | Proposer (A11) | A person removing another's proposal (A10) |
| applied (receipt) | Applied-outcome association: proposal/item, relied-on basis, receipt, resulting revision, branch, resulting objects with post-application subject identities | Host | `success`, queued, accepted |
| application error | Error identity; effect *none* / *partial* (receipt references) / *unknown* (→ overlay) | Host | Any unstated effect |
| outcome unknown (overlay) | Observation gap; last observed state | The observer that lost observation | — |
| success (operation ran) | Result reference and observed basis | Host | Any human act |

Rules. **OE-1** Transport success, a tool-call return, source resolution or a
resolvable receipt *reference* never upgrades an outcome. **OE-2** A re-draft
after *refused — stale* is a new entry with a new proposal identity and
lineage. **OE-3** Each submission is its own entry, recording only the effects
actually observed; "one effect per proposal identity" is a host obligation
(DEP-001), not a recorded fact. **OE-4** A retry keeps the same proposal
identity; identity de-duplication precedes the basis check, and the retry
entry records what the host returned; it is never recorded as *refused —
stale* because of the proposal's own effects (R2-13). **OE-5** A derived
proposal state is never stronger than its items. **OE-6** An undo is a change
through the one route with its own entry; *undone* is *applied (receipt)* with
**reverses ⟨receipt⟩ (entry ⟨ref⟩)**; it erases no act record; A5/A10 on the
reversed item are not lapsed; acts bound to subject content the undo changes
lapse under §7 (R2-15). **OE-7** Accepted then refused stale: both the A5
record and the *refused — stale* entry are present; A5 not lapsed; item not
applied (R2-16). **OE-8** A **run** action taken while an arrival was waiting
and not stopped by the hold (R6-3) is recorded normally **and** flagged
*during hold* with its turn initiator (R11); an arrival it produces is a separate arrival (EXEC MA-3). The
person's own operations (proposals, applications, undo) are never flagged
*during hold* (R5-5).

## 6. Human-act record

### 6.1 Elements (semantic)

| Element | Meaning | Required |
|---|---|---|
| Act identity | Identity of this record | Yes |
| Act kind | A4, A5, A6, A7, A10, A12, A13, or A11 when the person is the proposer (ACT §2.4). Never A1/A2 (R7 entries), A9 (carried by recording mode) or A14 (R13 only) | Yes |
| Act class | As applicable: "reserved to the person" for A4, A6, A7, A12, A13 (D2; disabling A13 INTEGRATION) and for A5/A10 where the active autonomy requires a proposal; for acts through a catalog operation, that operation's class from the DEL-04-01 policy-class record, including *no policy basis* with reason | As applicable |
| Governing policy reference | Policy-class record and policy revision identity (DEL-04-01 §8.1); DECISION-1 for D2/D3 | With act class |
| Decision actor | The person who performed the act | Yes |
| Recorder | Capturing surface, App, host facility, or agent | Yes |
| Recording mode (sub-element of A9) | *direct capture* or *faithful recording* (cites capture evidence) | Yes |
| Bound subject | Change item(s) (A5/A10); host row/object (A4/A6/A7); App file; setting content (A12/A13) | Yes |
| Bound content c₀ with method m₀ | A5/A10: change-item content identity; A4/A6/A7 on host content: subject content identity; App files: file content identity; A12/A13: the setting content (classes, grant values, scope) | Yes, or "not obtainable" → lapse permanently *unknown* |
| Scope | Change-item identities; row/object identities; setting scope | Yes |
| Purpose | What the act was for; at a checkpoint, the arrival's declared purpose it answers | Yes |
| Capture evidence references | From the capturing surface (host act facility; App interface per EXEC CAP-1…CAP-9; control surface for A12), each with resolution status | At least one; without it the record is non-conformant |
| Evidence limits | What the evidence does not show (e.g. App person identity scheme, EXEC CAP-8) | Yes |
| Relations | Run, operation entry, arrival answered (if any), workflow, decision record; for A12: **control effect** — established ⟨settings version⟩ · pending · refused ⟨reason⟩ · unconfirmed (R4-6); **superseded by ⟨act⟩** (L-0); **after run end** where captured after the run's run-ended event | As applicable; no required prior act |
| Order | Capture time as evidenced; request relation to an arrival where the capturing surface records one | Yes |
| Lapse evaluation | Latest state with compared c₀/c₁ and m₀/m₁ (§7); derived. Not evaluated for A12/A13 | Derived |

### 6.2 Rules

- **HA-1** Written only from capture evidence that the person performed the
  act. Not such evidence: a proposal, success, grant, receipt, A3 findings, A8
  request, A14 settlement, silence, timeout, a chat statement, **an answer to a
  supplier user-input or MCP elicitation request** (R4-12; EXEC CAP-6), or
  **App-side configuration an agent could write** (never A13 evidence, R4-13).
- **HA-2** Decision actor and recorder are separate elements. A record naming
  the recorder as decision actor of A4–A7, A10, A12 or A13 is non-conformant.
- **HA-3** One record, one act kind. A5 never produces A4, A6 or A7. An
  independently evidenced act is recordable without any A5.
- **HA-4** A6 and A7 name the accountable person and scope only as evidenced;
  no certification label. A6 is engineering approval only.
- **HA-5** A12 and A13 are human-act records; R6 references A12. An agent's A8
  request creates no A12.
- **HA-6** Act class is carried, never computed here. *No policy basis* is
  shown "no policy basis — held (reason)".
- **HA-7** Faithful recording (A9) by any identified recorder distinct from
  the decision actor is a conformant record shape. It satisfies a checkpoint
  only through the capture evidence it cites (R-5; EXEC SP-3).
- **HA-8** For A5 the negative decision is A10; for A4, A6, A7 or A12 an
  act-declined event. Stopping the run is a separate run-ended event.
- **HA-9** No faithful record is made through a catalog operation that
  performs a reserved act (R2-2). App-side A9 records are DEL-04-03 files. A
  host-offered faithful-record operation, if any, must not change act state,
  must cite capture evidence, never satisfies a checkpoint and takes ordinary
  policy; whether any host offers one is a relay question.

## 7. Content binding and lapse comparison rule

Notation: *S* bound subject; *c₀*, *m₀* bound content identity and method
designation; *c₁*, *m₁* the current identity of the same subject and scope.

| Step | Rule |
|---|---|
| L-0 | **A12/A13 are not lapse-evaluated.** A later A12 on overlapping classes and scope **that the control establishes** supersedes the earlier one; the record shows *superseded by ⟨act⟩*. A **refused** later A12 supersedes nothing: the earlier established setting stays in force. A **pending** A12 leaves an A12 arrival *waiting* ("A12 awaiting control confirmation"); a refused one leaves it *waiting* ("A12 refused by control: ‹reason›"); a lost confirmation makes it *unknown* (R4-6; EXEC §4.10). A checkpoint the earlier established A12 performed stays *performed*, with the supersession shown. Same rule for a later A13 on the same interface. |
| L-1 | Obtain c₁ for exactly the bound subject and scope from one of three sources: change-item content identity (DEL-03-02) for A5/A10; subject content identity (DEL-03-01 §5.3) for A4/A6/A7 on host content; file content identity for App files. Never the workspace generation or model revision. |
| L-2 | Compare method designations. m₁ ≠ m₀ or comparability not shown → **unknown (incomparable)**. |
| L-3 | c₁ not obtainable → **unknown (unavailable)**. |
| L-4 | S no longer exists → **lapsed (subject absent)**. |
| L-5 | c₁ = c₀ → **not lapsed**. |
| L-6 | c₁ ≠ c₀ → **lapsed**, retaining c₀, scope and purpose; an act-lapsed event is recorded. |
| L-7 | Multi-element scope: evaluate per element. A batch A5 lapses per item. A multi-row A4 with some rows changed is **partially lapsed**; its purpose for unchanged rows is an owner question (U-07). |
| L-8 | Lapse never deletes or edits the act record. |
| L-9 | Host-presented lapse is linked where supplied; an App/host disagreement is shown and is an R11 limit. |
| L-10 | Applying an accepted change item does not lapse its A5. A basis failure between A5 and application is *refused — stale* (OE-7). An undo does not lapse A5/A10 on the reversed item; acts bound to subject content the undo changes lapse under L-6. |
| L-11 | Content returning to c₀ after an observed lapse is shown "matches c₀ again after observed lapse", keeping the lapse interval visible; effect is U-12. |
| L-12 | **Checkpoint effect of a lapse (R4-3; EXEC HD-5, §4.7).** The **resume point** is the arrival's run-resumed event. *Before resume*: act-lapsed event recorded; the arrival returns to **waiting**, "lapsed at ‹t›". *After resume, run live*: act-lapsed event recorded; the **same** arrival (same referents) returns to **waiting**, "waiting — re-held, lapsed at ‹t› after resume" — whatever caused the lapse: a person's edit, **the person's own undo** (an R7 operation, never action during hold), or the run's own later action (R5-5); what "held" means follows the hold-support value (R6-3): under *enforced by the host loop* the run stops at its next action boundary; under *enforced on the host route* the host refuses the held host operations and every other run action is recorded as action during hold; under *not established* or *not enforceable* nothing is stopped and run actions are recorded as action during hold; nothing already done is undone; actions between resume and lapse stay recorded as taken under the earlier performance; outputs whose promised standing names this checkpoint as gating show standing **lapsed** for the affected referents; the act request is re-issued for the **whole** bound scope with lapsed referents marked; a satisfying act gives the next performance ordinal. If the run ends while re-held, the final disposition is **waiting** with the run-ended event. *After the run ended*: the disposition becomes **lapsed** per referent. **A5 and A12 never re-hold** (L-10; L-0); in particular an undo never re-holds an A5 arrival (R5-5). |
| L-13 | **Capture after arrival (R4-5; EXEC SP-6; PROPOSED).** An act counts toward an arrival only if captured at or after that arrival's event — by a request relation where the capturing surface records one, otherwise by evidenced times. An earlier act on the subject is recorded and shown **"prior act not counted"**; if the order cannot be established, "act order unknown" and the act does not count. This orders an act only against its own arrival; it adds no order between act kinds. The owner alternative (count a prior act bound to current content) is U-26. Owner-visible cost (R5-7): the person may have to repeat an act — e.g. an A12 whose setting content is already in force — made before the arrival. |

Lapse states: not lapsed · lapsed · lapsed (subject absent) · partially
lapsed · matches c₀ again after observed lapse · unknown (incomparable) ·
unknown (unavailable) · not yet evaluated. For A12/A13: current · superseded.
*Not yet evaluated* never renders as *not lapsed*.

## 8. Settings-in / record-out exchange with DEL-04-02 (CASE-002 M3)

Identical in DEL-04-02/AS-v0.5 §6. A data exchange, not an ordering between
human acts and not a second authority.

**Settings-in (DEL-04-02 → DEL-04-03 writer), per run and per change:** run
identity; settings version identity; **scope** (representation-neutral
dimensions, e.g. model/workspace, object set, run, period, consequence); per
operation class — **grant value** (direct / propose) and **class value**
(DEL-04-01 policy-class record reference; for *no policy basis*, its reason);
display state (effective (person-set) · effective (policy default) ·
requested by agent · set by person, not yet confirmed by control ·
unconfirmed · not set · refused (reason)); **requester** (person; agent via
A8; *none — policy default*); **setting actor** (the person, only where an
A12 exists; *none — policy default*); **setting act reference** (A12 record)
— or, for *effective (policy default)*, the **policy-class record reference
and its default value** in its place; **establishment evidence** (control
confirmation) or refusal reason; order relative to operation entries; source
of control (App or host).

**Record-out (DEL-04-03 reader → DEL-04-02), per run:** record identity and
format version; continues ⟨run⟩ where present; recorded settings versions
with the fields above; per operation entry the two settings references,
route, treatment at resolution, governing checkpoint constraint with carriage
assurance, outcome, item dispositions with actors, receipt/origin references,
resulting objects, *reverses* relations, evaluated/relied/current bases and
the *during hold* flag; human-act records, act-declined events and act-lapsed
events with actor, recorder, recording mode, kind, act class, bound subject,
scope, purpose, c₀/c₁ with method designations, lapse or supersession state,
A12 control effect, *after run end* marking and capture evidence references
with resolution status; checkpoint arrivals with subject class, hold support,
arrival and performance ordinals, disposition, annotations, run-resumed and
run-ended events; evidence limits.

**Comparison (DEL-04-02)** per settings version: displayed vs recorded →
*match* · *mismatch* · *missing in record* · *missing in display*. Mismatch is
shown to the person and returned as a defect observation. The record is
authoritative for what was recorded; the control for the current grant; the
display is derived. Neither side auto-corrects the other. A person-set state
without an A12 reference, or an *effective (policy default)* state without a
policy-class record reference, is a defect, not an established setting.

## 9. Evidence references

Each reference carries: evidence kind (receipt, content identity, origin
mark, capture evidence, commit, supplier settlement, compatibility report,
carriage manifest), claimed identity, identity method designation where
applicable, and resolution status at write (resolved / unresolvable / not
supplied) and at read. "Resolved" means the source was found with the claimed
identity; it does not make the referenced change or act more than the source
states (OE-1).

## 10. Consumer and host interface

| Consumer | Consumes (meaning) | Supplies back | Held part / limit |
|---|---|---|---|
| DEL-02-01 | Act names; R8 subject classes and dispositions; R2 | Workflow identity; checkpoint reached-when, subject class, §4.3.7 mixed-item rule | Closed act list A4/A5/A6/A7/A12 |
| DEL-02-03 | R8 arrivals and events; R2 transfer links; R11 action during hold; R14 | Hold machine (§4), resume point, re-hold, finality and continuation, refused-A12 effect, SP-6, compatibility reports, transfer trace, App capture requirements (CAP-1…CAP-9) | D6 (U-25); SP-6 alternative (U-26) |
| DEL-03-01 | R7 identity/basis; c₁ for A4/A6/A7 | Subject content identity; method designation; exposure element; shared fixture §10 | Algorithm unselected |
| DEL-03-02 | §5 evidence rules | §9 outcomes; change-item content identity; origin incl. constraint and author identity (may be unverified); resulting objects; item-left events | One-effect mechanism unselected |
| DEL-03-03 | R5 destination; R7 external entries; R9; R11; R13 | External dispatch entries; model destination class; evidence limits (cited basis not observed, omitted constraint, origin mismatch, agent-written configuration, unverified identity, native hint mismatch); A14 observations | Caller identity verification (U-27) |
| DEL-04-02 | Record-out (§8) | Settings-in (§8) | Executable M3 trace needs candidate writer/reader |
| DEL-05-01 | R3/R4/R5/R5a/R7/R8 meanings | Observer-attributed unknown; origin, seat role, grant in force, constraint per dispatch; loop-side *not offered*; host-loop hold support; run-resumed/run-ended | — |
| DEL-05-02 | Act, act-declined, lapse, supersession, annotation display meanings | — | — |
| DEL-01-01 | R3, R5, R13 meanings | Supplied-guidance identities; per-turn requested/effective model and re-routes (HOSTING §8.3); A14 settlement origin (observed facts) | Pin 0.158.0 is definition only; whether requested and effective can differ is not observed (HOSTING U-19) |
| DEL-09-06 | R2 transfer links | Joined round-trip evidence | Host links AWAITING INPUT |
| PKG-06 (DEL-06-01/06-02) | Act records; actor ≠ recorder; lapse | Decision records as act subjects | Coordination recorder never becomes actor |
| DEL-09-11 | Complete records for the week-later reconstruction (inspection replay, EXEC RP-6) | — | This format does not perform the witness |
| DEL-01-02, DEL-01-04, DEL-02-02, DEL-02-04 | R3/R4/R7/R13; act display; review/registration; App act control | Observation evidence; role bytes; App capture control | Outside this undertaking (D1) |
| External host run recording (DEP-04-03-016; DEP-001) | §§3–9 | Receipts, origin marks, subject content identities, capture evidence and reference, lapse, per-operation settings version, constraint receipt, per-turn guidance, host holds (SQ-02), channel restrictions on destination | Adoption unclaimed; OI-013 placement |

## 11. Excluded acts and owners (REQ-006)

OI-001/OI-002 were decided at App/shared level by the Owner in DECISION-1
(D2, D3); D5 by the Owner in DECISION-2; D6 is deferred by the Owner to the
SWBPIPE answer (SQ-02). Operation-specific additions remain with the Owner via
the outside SWB session and App/shared owner (OI-021). The SoW's TBD-001 still
reads OI-001/OI-002 as open — a pointer reconciliation for closeout C1.
Defining and carrying policy — DEL-04-01. Autonomy/standing UI — DEL-04-02.
Hold machine and transfer — DEL-02-03. Reconstruction witness — DEL-09-11.
Host domain changes, receipts, storage, host run recording, host enforcement
of its reserved list and its own channel restrictions — responsible host owner
(SWBPIPE outside session). Performing any human act — the person. Professional
reliance and certification — the accountable professional. This format
faithfully records evidenced acts; it performs none.

## 12. Examples (fixture subjects — invented; no act was performed)

All identifiers are DEL-03-01/C-v0.4 §10 (commit 8fb51f07f): FX-PIPE-01,
FX-W1, g1, run R-100 (fixture run 12, conversation K-7), supports S-1…S-4 and
S-5 (created at T12), Engineer A, workflow `supports-adjust` (origin *host*,
⟨fx-root⟩, ⟨rev-3⟩, declaring `CP-accept` and `CP-check` per FXA-5), bases
B1/B2, PR-1/PR-2, RC-1…RC-3, ⟨set-1⟩/⟨set-2⟩, T1–T17 and T16a, variants V-S1,
V-CP1, V-NP1, V-R1, V-X1, V-OU1, V-ED1, fixture assumptions FXA-1…FXA-5,
App-side subjects LIB-A1, LIB-A2, AF-1. **V-GR1** is
cited from C-v0.5 §10.4 (run 13; GR-1…GR-3; GR-P, GR-R, GR-S). Local cases are `L-RS-n`, each saying why.

**E1 — Stale, re-draft, per-item decisions, application (T3–T12).** T3 OP-C1
→ B1. T5 PR-1 relies on B1 (item 1 OP-C4, item 2 OP-C5). T6 Engineer A edits
S-3 (r13). T7 both items **refused — stale** (relied B1, current B2). T9 PR-2
(lineage PR-1) on B2; T10 queued — `CP-accept` **arrives** (FXA-5; PR-1 was
never queued). T11 Engineer A operates OP-C7: it performs the reserved act
and produces ⟨act:1⟩ **A5** on item 1 (host facility, direct capture, c₀
⟨ci:PR-2/1⟩ ⟨m-fx⟩, "reserved to the person (D2b)"); the OP-C7 R7 entry
references ⟨act:1⟩ (R5-6). OP-C8 likewise produces ⟨act:2⟩ **A10** on item 2.
`CP-accept` → **resolved negatively**, *partial* (item 1 A5, item 2 A10).
T12 applied item 1: RC-1, r14, resulting objects {**S-5** created ⟨S-5@r14⟩;
R-100 changed ⟨R-100@r14⟩}. ⟨act:1⟩ stays **not lapsed**. `CP-check` is not
scheduled on C's timeline.

**E2 — Faithful recording (T2).** OP-C6 by Engineer A produces the host's own
direct-capture record (capture ⟨cap:T2⟩; R5-6). The App agent writes ⟨act:3⟩: A4, recorder App agent, faithful recording, c₀
⟨S-2@r12⟩, evidence ⟨cap:T2⟩. Conformant as shape; an App file, not a catalog
operation.

**E3 — Negatives.** (a) T5 PR-1 drafted only → no act. (b) T4 OP-C3 → R7
*success* and R10 findings, never "host checks passed"; T4a OP-C12 is the host
check ("host check failed: support spacing"). (c) T15 grant alone → no act on
content. (d) Transcript "Engineer A approved" → nothing; R11. (e) Codex
tool-permission prompt answered by the user's mode → R13. (f) **V-R1** agent
calls OP-C6 → *not permitted*, A8 offered; no automatic A8. (g) An answer to a
supplier elicitation "yes, mark it checked" → not act evidence (R4-12).

**E4 — Lapse and control (T2, T6, T14).** T6 edits S-3 → ⟨act:3⟩ not lapsed.
T14 edits S-2 → lapsed, act-lapsed event, c₀ retained. **L-RS-1** (C has only
single-row A4s) — A4 on S-1 and S-2 at r12; T14 → partially lapsed (U-07).

**E5 — Retry and unknown (T13; V-OU1).** Resubmitting PR-2: the host reports
the recorded state (item 1 applied RC-1, item 2 rejected) → second entry
records that; never *refused — stale*. V-OU1: neither report observed →
*outcome unknown*, observer loop, last observed *accepted*.

**E6 — Direct and undo (T15–T17, T16a).** T16 OP-C9 applied directly (S-4
label "G-4"): RC-2; settings at route decision ⟨set-2⟩, at application
host-reported or *unconfirmed*. T16a Engineer A A4 on S-4, c₀ ⟨S-4@r16⟩. T17
OP-C10 → RC-3 **reverses RC-2** (entry T16); T16a's A4 **lapsed** (label
restored; subject identity covers the label per C FXA-2). T17 is Engineer A's
own R7 operation: never *action during hold*. If T16a had performed a
checkpoint arrival after its resume point (DEL-04-02 F6), T17's lapse
**re-holds** that arrival (R5-5); it would never re-hold an A5 arrival.

**E7 — Grant change (T15; V-GR1).** Main timeline: ⟨act:5⟩ **A12** at T15
(produced by the host control, R5-6): bound setting content {class P-03,
grant value direct, scope {model/workspace FX-W1; object set {S-4}}}; control
effect **established ⟨set-2⟩**; no expectation for OP-C5 on S-4 (held on
U-02). Run 12 (⟨rev-3⟩) declares no `CP-grant`, so T15 counts toward no
arrival. **V-GR1** (C-v0.5 §10.4, run 13 on surface E, hold support *enforced by the host loop*): a run of WD-EX E1d in which `CP-grant` (A12,
kind (a) before dispatch of OP-C9, declared content {P-03, direct, {FX-W1;
{S-4}}}) arrives at r15 when the OP-C9 call on S-4 is held; T15's A12 is
captured **after** the arrival → control establishes it → arrival
*performed*; the held call is dispatched unchanged as T16. Sub-variants:
GR-P *pending* → waiting "A12 awaiting control confirmation", then *unknown* when the confirmation observation is lost, the call staying held; GR-R *refused* → waiting
"A12 refused by control: ‹reason›", ⟨act:5⟩ supersedes nothing and **⟨set-1⟩** stays in force; GR-S a later
**established** A12 narrowing the scope → ⟨act:5⟩ *superseded*, arrival stays
*performed* with the supersession shown. From the App via X, `CP-grant` hold
support is **not established** (HS-3 on OP-C9, SQ-02 unanswered; R6-2). An A12
captured before the arrival would be "prior act not counted" (L-13).

**E8 — Stale after acceptance (V-S1).** After T11, S-2 edited before T12
(r14′) → *refused — stale* (relied B2, current ⟨B-r14′⟩); ⟨act:1⟩ present,
not lapsed; item 1 not applied.

**E9 — No policy basis (V-NP1).** OP-C11 direct → *not permitted* (no policy
basis, pending OI-021); proposal → queued, confers no permission; A12
widening → refused (reason: no policy basis); fixture result **held**.

**E10 — Checkpoints, arrivals and hold (L-RS-5: C FXA-5 declares `CP-accept`
and `CP-check`, neither with the R3-1 subject class).** App run of a workflow
on surface X (App conversation, host reads over the external channel).
Checkpoint *CP-row-check* requires A4, subject class **objects a named output
concerns** = the spans named in T4a's OP-C12 output (S-2, S-3), reached-when
*on production of that output*. Its held actions are the run's next actions,
which include App agent turns (e.g. the agent's drafting of PR-1 at T5 in the
App conversation) — App-side held actions, so hold support is **not
enforceable** in the App run (R6-1 HS-5; D6), whatever SQ-02 returns, and the
workflow requirement check reports *unsupported* (reason: checkpoint hold not
enforceable on this surface: CP-row-check). The arrival is still recorded (EXEC HD-4). (i) Arrival 1 at
T4a. T2's A4 on S-2 → **"prior act not counted"** (L-13). (ii) The agent's
next dispatch (T5 drafting PR-1) proceeds → R7 entry flagged *during hold*,
R11 "action during hold", turn initiator *agent*; no stop is claimed. (iii) Engineer A performs A4 on
S-2 and S-3 (host capture; App faithful record) → *performed*, performance
ordinal 1; run-resumed event at the next run action. (iv) T6 edits S-3 →
act-lapsed event; arrival 1 **"waiting — re-held, lapsed at T6 after
resume"**; no stop is recorded; later run actions are flagged *during hold*.
(v) Variant: Engineer A declines → act-declined event → *resolved
negatively*. (vi) Variant: nobody acts and the run ends → run-ended event;
arrival stays **waiting**. (vii) Variant: a kind (a) checkpoint whose only held
action is a host operation over X → HS-3: **not established** while SQ-02 is
unanswered (the requirement check is *not established*, never a pass);
*enforced on the host route* once SQ-02 is answered with host-held carriage
evidenced on a candidate (the host refuses that operation; other run actions
are action during hold); *not enforceable* if answered with no host-held
route.

**E11 — After run end and continuation (L-RS-6: run finality has no C step).**
After E10 (vi), Engineer A performs A4 on S-2/S-3 → recorded, marked **"after
run end"**; the ended run's arrival stays *waiting*. A new run starts with
**continues ⟨run 12⟩**; its CP-row-check starts *not reached*; when it
arrives, the post-end A4 is **"prior act not counted"**.

**E12 — Model destination (D16; DEL-03-03 L-ADAPTER-8).** An App run whose
conversation requested a user-chosen cloud model reads OP-C1 over the external
channel. R5 records per turn: turn 1 requested = effective = cloud model M1;
turn 2 a supplier re-route M1 → M2 recorded with its turn; turn 3 not observed
→ *unknown*. Run-level value: the set {M1, M2, unknown}. No gate, no new run,
no grant change, no act.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 Operation-specific reserved additions `OI-021` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Class may be *no policy basis (pending OI-021)*; fixtures held |
| U-02 Consequence vocabulary | DEL-04-01 with host policy owner | Before class assignment in DEL-03-01 | Scope dimension "consequence" is a slot; OP-C5 on S-4 under ⟨set-2⟩ held |
| U-04 Serialization, field names, identity algorithms, record-identity form, carriage-manifest representation | DEL-04-03 with DEL-03-01 (TBD-003) and DEL-02-01 | Before OUT-001 CONFIG and writer implementation | L-2 depends on method designations only |
| U-05 App record location | DEL-04-03 with OI-014 owners | Before writer implementation | "Ordinary files" only |
| U-06 Host persistence/placement `OI-013` | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Host recording follows meaning only |
| U-07 Purpose of a multi-row A4 after partial lapse | DEL-04-01 with Owner | At its point of need (carried to C1; EXEC's whole-scope request satisfies every option) | Per-row lapse only |
| U-08 Workflow review/registration as act kind | DEL-04-01 with DEL-02-02 (later, D1) | DEL-02-02 definition | Not recorded here |
| U-09 Host evidence that application re-checks the basis after acceptance | Host owner (DEP-001) | Before connected integration | OE-7 records both entries |
| U-11 Host capture requirement per act kind; capture-evidence reference | Host owner (DEP-001; relay) | Before host act-recording integration | No host-content arrival reaches *performed* without it |
| U-12 Content returning to c₀ after observed lapse | Host owner (U-C2) with DEL-04-03 | Before lapse display criteria are fixed | L-11 keeps lapse visible |
| U-14 Host-stored findings as a change operation | Host owner | Before V4-EXM-21 fixture binding | R10 may also need R7 |
| U-15 Host receipts, origin marks, subject identities, resulting objects, lapse, per-operation settings version, de-duplication `DEP-001` | SWBPIPE outside implementation session | Before corresponding connected-journey integration/examination and fallback-replacement decision | All host evidence is fixture |
| U-16 Reader/writer placement `OI-014` | App/shared contract owners | Before structural/production contract allocation | No common service assumed |
| U-19 Host receipt or own evaluation of the governing checkpoint constraint | Host owner (relay SQ-02) | Before connected integration | Only host-held satisfies R2-12; App-assured unavailable (R5-2); model-supplied or absent is an R11 limit |
| U-20 R13 feed beyond DEL-01-01 observed facts | DEL-01-02 (later, D1) | DEL-01-02 definition | R13 fed by DEL-01-01 only |
| U-21 Host-loop per-turn guidance identities | Host owner (relay) | Before connected integration | R3 *unknown* where absent |
| U-25 App-side run holds `UNRESOLVED{D6}` | Owner, deferred to SWBPIPE SQ-02 for host-operation checkpoints; App-only checkpoints are a separate D6 follow-up for the Owner (R5-10) | Before App-side hold fixtures | R8 hold support (R5-1 values) and R11 action during hold recorded; no unenforced hold recorded as held |
| U-26 SP-6 versus counting a prior act on current content (EXEC U-E4) | DEL-02-01 with DEL-04-01; Owner if preferred | Before hold-machine fixtures run | L-13 applied as PROPOSED; owner-visible cost recorded (R5-7) |
| U-27 Caller identity verification over the external channel (ADAPTER OC-6) | App owner with host owner | Before origin conformance | Author identity *unverified*; R11 limit |
| U-28 App person identity scheme and App act control (EXEC U-E8) | DEL-01-04 (later, D1) with DEL-04-03 | Before App capture fixtures | Evidence limit on App-captured acts |

Closed in v0.5: none. Closed in v0.4: U-17 (R4-6; EXEC §4.10), U-18 (EXEC §4.11 confirmed), U-22
(EXEC §6.2 confirmed), U-23 (R4-4), U-24 (R4-3). Earlier: U-03, U-10, U-13.

## Verification cases (designed, not run)

| Case | Input (fixture subject) | Expected result | Serves |
|---|---|---|---|
| VC-01 Authority | E1; transcript and derived view claim an A5 on PR-2 item 2 | Only ⟨act:1⟩/⟨act:2⟩; the claim creates no act | VER-001 (AC-001) |
| VC-02 Inventory completeness | E1 run (App) and a host-loop run | R1–R14 each value, explicit absence, or *not applicable* with reason (R13 in host loop) | VER-001 (AC-002) |
| VC-03 Link not copy | E1 with RC-1 | Reference, claimed identity, method, resolution status only | VER-001 (AC-002) |
| VC-04 Faithful recording | E2 | A4, recorder App agent, faithful recording, capture evidence cited | VER-002 (AC-003) |
| VC-05 Fabrication negatives | E3 (a)–(g) | No act records; (d) R11; (e) R13 only; (f) no automatic A8; (g) not act evidence | VER-002 (AC-003) |
| VC-06 Independent act | Engineer A marks own edit checked, no proposal | A4 recorded; no A5 required | VER-002 (AC-003) |
| VC-07 Row lapse and control | E4 | T6 not lapsed; T14 lapsed with act-lapsed event | VER-003 (AC-004) |
| VC-08 Incomparable / unavailable | E2 with m₁ ≠ m₀; host unreachable | *unknown (incomparable)*; *unknown (unavailable)* | VER-003 (AC-004) |
| VC-09 Model-row partial lapse | L-RS-1 | Partially lapsed (S-2); purpose U-07 | VER-003 (AC-004) |
| VC-10 Acceptance survives application | E1 | ⟨act:1⟩ not lapsed after T12 | VER-003 (AC-004) |
| VC-11 Undo lapses row-bound act | E6 (T16a, T17) | T16a A4 lapsed; RC-3 reverses RC-2 | VER-003 (AC-004) |
| VC-12 Restore after lapse | E4, then S-2 restored | "matches c₀ again after observed lapse" | VER-003 (AC-004) |
| VC-13 A12 at a checkpoint and supersession (V-GR1) | E7 main timeline and V-GR1 sub-variants | Main: T15 counts toward no arrival; V-GR1: captured after arrival → performed, held call dispatched unchanged as T16; pending/refused → waiting; lost → unknown; later established A12 → superseded, arrival stays performed; refused A12 supersedes nothing | VER-003 (AC-004) |
| VC-14 Retry vs stale | E5 | Retry entry records the host's report or unknown with observer; never stale from own effect | VER-004 (AC-005) |
| VC-15 Stale after acceptance | E8 | A5 not lapsed; *refused — stale* with both bases | VER-004 (AC-005) |
| VC-16 Outcome vocabulary | Not offered; T8 unavailable; V-X1 not exposed; channel not enabled (App-reported and host-reported); V-R1, V-NP1, V-CP1 not permitted; refused — invalid; T7 stale; application error; A10; A11 | Each distinct with evidence and actor/observer; host refusal never "rejected" | VER-004 (AC-005) |
| VC-17 Checkpoint arrivals and hold support | E10 (i)–(vii) | Classified by held actions (R6-1): App agent turns held → **not enforceable** → *unsupported*; arrival still recorded; prior act not counted; action during hold in R11 with turn initiator and **no stop claimed**; performed with ordinal; "waiting — re-held, lapsed at T6 after resume"; resolved negatively; waiting + run-ended; (vii) host operation only → **not established** now (never a pass), with its SQ-02-dependent alternatives | VER-002 (AC-003) |
| VC-18 Lapse before resume | E10 with T6 before the run-resumed event | "waiting — lapsed at T6"; no re-hold annotation | VER-003 (AC-004) |
| VC-19 No policy basis | E9 | *not permitted*; A12 refused; **held**, not pass | VER-004 (AC-005) |
| VC-20 Grant change | E7; an A8 alone; ⟨set-1⟩ default | A12 referenced from R6; A8 → "requested by agent"; default → policy-class record, no A12 | VER-002 (AC-003) |
| VC-21 After run end and continuation | E11 | Post-end act marked "after run end"; ended disposition unchanged; new run carries continues ⟨run 12⟩ and inherits nothing | VER-004 (AC-005) |
| VC-22 Destination per turn and unverified caller | E12; an external dispatch with unverified author identity | Per-turn requested/effective kept separate; re-route with its turn; unobserved turn *unknown*; run-level set; no gate, no new run; author identity *unverified*, R11 limit | VER-001 (AC-002) |
| VC-23 Transfer and revision links | A carried unadapted workflow and a host adaptation (EXEC §6.1) | Links recorded separately; revised identity inherits none; "revision not verified" explicit | VER-001 (AC-002) |
| VC-26 Person's undo re-holds, never action during hold | E6 with the DEL-04-02 F6 arrival | Re-held after resume; T17 not flagged *during hold*; an A5 arrival is never re-held by an undo | VER-003 (AC-004) |
| VC-27 Reserved-act operation and App file | E1 OP-C7/OP-C8; an App-captured A4 on C AF-1 (⟨AF-1@f1⟩, then edited to ⟨AF-1@f2⟩) | Human-act records produced by the reserved-act operation and referenced from R7; AF-1 act bound by file content identity lapses on edit | VER-002 (AC-003) |
| VC-28 Hold-support values | E10 (App-side held actions; host-operation-only variant); a host-loop run; an invalid declaration | Only the four R5-1 values; classified by held actions (R6-1); *not established* never a pass or *unsupported*; *not enforceable* → *unsupported*; invalid declaration takes no value; no retired value | VER-005 (AC-006) |
| VC-24 Coverage inventory | VC-01…VC-23 and VC-26…VC-28 against AC-001…AC-005 | Each AC has ≥1 positive and ≥1 negative case; held/AWAITING INPUT never counted as pass; distinct from DEL-09-11 | VER-005 (AC-006) |
| VC-25 Owner trace | §10, §11, UNRESOLVED | Each REQ-005 consumer and REQ-006 excluded act traced; D2/D3/D5/D6 cited only for what they say; no delivery/adoption asserted | VER-006 (AC-007) |
