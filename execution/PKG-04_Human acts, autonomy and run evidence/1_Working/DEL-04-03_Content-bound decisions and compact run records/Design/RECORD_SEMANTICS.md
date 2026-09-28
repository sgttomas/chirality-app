# Record Semantics
- Contribution: DEL-04-03/RS-v0.2
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 and OUT-004 (definition content); OUT-002 and OUT-003 (behaviour and fixture design only — no writer, reader or fixture exists); REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; AC-001…AC-007 via designed VER-001…VER-006
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 74d42c38eaf2a6638b75bc5184f1741bc7d4f17171662a05a233d40f245340c1; `P/docs/PRD.md` §4.3 V4-EXE-02/03, §4.5 V4-AUT-01…05, §4.6 V4-PM-06, §4.7 V4-REC-01…05, §10; `P/docs/HOST_INTEGRATION.md` §1, V4-HI-04, V4-HI-11/12, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-52, V4-HI-70/71, §11; `P/docs/ARCHITECTURE.md` §4, V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-21/22/31; `P/docs/OPERATING_METHOD.md` V4-OPS-30…32; `DECISION_BRIEF.html` d2, d3; `OWNER_DIRECTIONS.md` J, O; `SCC-CASE-002/Case_Datasheet.md` M1, M2 (DEL-02-04 row), M3, M3-CP; `_Decomposition/Open_Issues.csv` OI-001/002/013/014/021; `External_Dependencies.csv` DEP-001. Run folder `APP-V4-FIRST-INCREMENT-20260928`: `OWNER_DECISIONS.md` (DECISION-1, D1–D4; sha256 f3f8e5f31ec87006…), `R1_RESOLUTIONS.md` (R-1…R-10; sha256 2f9c7e72aa836262…), `comparisons/V1-A.md` (01811533bf0aedad…), `V1-B.md` (09eebfe0ed78058a…), `V1-C.md` (8d46258ad0120067…)
- Consumed inputs: DEL-04-03/RS-v0.1 (sha256 1e4bb89e648f0891…, as compared in V1). Owner rulings D2/D3 (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1`), carried through DEL-04-01's adopted-decision record per R1_RESOLUTIONS R-2. The following supplier v0.2 elements are taken **from R1_RESOLUTIONS, not from the supplier files** (those are under concurrent repair and were not read), each "per R1_RESOLUTIONS R-n; to be confirmed at IR1": DEL-04-01 canonical act names A1–A14 and label rule (R-1, R-4), treatment → runtime outcome map (R-3); DEL-03-01 subject content identity, identity method designation, per-surface exposure element, shared fixture catalogue FX-PIPE-01 (R-6, R-9); DEL-03-02 change-item content identity, §9 outcome taxonomy including application error, reporter-attributed outcome unknown, retry identity (R-6, R-7); DEL-02-01 workflow identity and checkpoint reached-when / dispositions (R-5, R-9); DEL-01-01 supplied-guidance content identity (R-10). DEL-04-02/AS-v0.2 was repaired concurrently by the same executor; §8 here and its §6 state the same exchange.
- Receivers: CASE-002 M1 — DEL-02-01 (OUT-001/002; REQ-003; VER-003), DEL-02-03 (OUT-001/002; REQ-003; VER-003), DEL-04-02 (OUT-001/002; REQ-002/004; VER-002/004), DEL-05-01 (OUT-001/004; REQ-005/007; VER-008), DEL-05-02 (OUT-001/003; REQ-001/003; VER-001/003); DEL-01-04 and DEL-02-02 (M1) are outside this undertaking per D1 and keep their receiver rows for a later undertaking. CASE-002 M3 — DEL-04-02 (OUT-001/003; REQ-002/004/005; VER-002/004/005). Dependencies.csv DEP-04-03-011…016 — PKG-02, PKG-03, PKG-06, DEL-04-02, DEL-09-11, external host run recording.

## Changes from v0.1

| V1 item | Change in v0.2 |
|---|---|
| V1-A D-01; V1-C D-17 (R-1) | §0 uses canonical names A1–A14; "accept an edit" → **accept** (A5); faithful recording is **record** (A9), a recording act, with *recording mode* as sub-element |
| V1-A D-02, D-03, §5 rows; V1-B D-08, §5 rows (R-2) | Blanket `UNRESOLVED{OI-001}` removed. Act class carries the DEL-04-01 adopted record (D2) with decision basis DECISION-1; open only for operation-specific additions (OI-021) and items listed in UNRESOLVED |
| V1-A D-17; V1-B D-12 (R-1 A12, R-8) | Grant change recorded as an **A12 set grant** human-act record; R6 references it; U-08 closed for grant change |
| V1-A D-18 (R-1 A9) | Recording mode {direct capture, faithful recording} kept as sub-element of A9 |
| V1-A D-19 | Act class element is "as applicable"; act kinds A4–A7, A12, A13 carry "reserved to the person (D2)"; governing policy reference + revision (V1-A AB-07) |
| V1-A D-11; R-5 | E2/VC-04 marked "conformant as shape"; checkpoint satisfaction requires capturing-surface evidence (§6.2 HA-7) |
| V1-A D-10; R-5 | Decline/stop event for A4/A6/A7 as its own record kind (§3); A10 reject is the negative pair of A5 |
| V1-A D-25; V1-B D-01, D-10 (R-6) | A5 binds to change-item content identity; acceptance unit = change item; per-item lapse; application does not lapse acceptance; multi-row A4 purpose after partial lapse stays an owner question |
| V1-B D-02, D-03 (R-6) | L-1 has three c₁ sources; L-2 compares identity method designations |
| V1-B D-04, D-05, D-21, D-23; V1-A D-16; V1-C D-11, D-12 (R-7) | §5 adopts DEL-03-02 §9 / DEL-03-01 §4.1 unchanged: item dispositions, last observed state, both bases on stale, evaluated basis on non-success, observed basis on reads/checks, application error with effect statement, reporter-attributed outcome unknown, actors for A5/A10/A11; host refusal ≠ rejected |
| V1-B D-06, D-07; V1-A D-08 (R-3, R-8) | Two settings references per operation (route decision; in force at application — host-reported or unconfirmed); standing at drafting vs treatment at resolution when they differ |
| V1-B D-09 (R-7) | OE-3 rewritten: each submission is its own entry with only observed effects; one effect is a host obligation to be evidenced |
| V1-B D-11, D-12, D-13 (R-8); V1-A D-06, D-07 | R6 and §8 carry scope, requester, setting actor, A12 act reference, establishment evidence, the R-8 state list incl. not set and refused (reason); record-out adds bound subject, c₀/c₁ with method, recording mode, evidence references, act class, checkpoint events |
| V1-B D-14 | Lapse vocabulary kept as the shared list; *not yet evaluated* never renders as not lapsed |
| V1-B D-17; V1-C AB-03 (R-7) | Request-side origin carries all DEL-03-02 origin elements (author type person/agent, seat/role instance, channel, conversation, workflow run, standing at drafting, reason); host origin mark linked; mismatch is an evidence limit |
| V1-B D-18 | *undoes* relation added to R7 entries |
| V1-B D-20; R-9 | Examples use model FX-PIPE-01 and DEL-03-01 operation references; local divergences stated (§12) |
| V1-B X-04 | DEL-03-02 U-P3 (basis fails after accept, before apply) mirrored in UNRESOLVED |
| V1-B X-05 | Restore/revert after lapse: display rule L-10 and UNRESOLVED U-12 |
| V1-B X-06 | DEL-03-01 U-C5 (host-stored findings as change operation) mirrored in R10 and UNRESOLVED |
| V1-B X-10; V1-A AB-05 (R-2 D3) | Tool-permission settlements (A14) get their own element R13, never in R6 and never a human-act record of A4–A7/A12 (proposed; DEL-04-01 to confirm) |
| V1-C D-10 (R-9) | R2 workflow identity = {kind, origin, source root, name, revision} + derived-from |
| V1-C AB-02, AB-04, AB-05 (R-7) | R5a seat role meaning; each dispatch carries origin, seat role and grant in force; retry keeps proposal identity |
| V1-C D-16 (R-10) | R3 supplied guidance records content identity per thread and turn |
| V1-A AB-02 | Workflow review/registration kind stays open; DEL-02-02 is outside this undertaking (D1) |
| V1-A AB-06 | Host capture requirement per act kind listed as DEP-001 item |

## 0. Reading this definition

- Element names are **semantic names, not wire names**. No serialization,
  field spelling, JSON or TypeScript type, file path, persistence mechanism,
  transport, hash or canonicalization algorithm, process placement or
  shared-component placement is selected (SoW TBD-002; OI-013; OI-014;
  DEL-03-01 TBD-003).
- `⟨…⟩` is an opaque identity token in examples. It is not a hash. Equal tokens
  stand for "the designated identity method reports the same identity".
- **Act names are canonical (R1_RESOLUTIONS R-1; owner DEL-04-01; to be
  confirmed at IR1):** A1 propose · A2 apply · A3 examine · A4 mark checked ·
  A5 accept · A6 approve (engineering approval only) · A7 rely · A8 request ·
  A9 record · A10 reject · A11 withdraw · A12 set grant · A13 enable external
  access · A14 answer tool permission. A9 is a recording act by the recorder,
  not a decision act, and never satisfies a checkpoint by itself.
- **Act class.** Carried from DEL-04-01's adopted-decision record. Under D2
  (DECISION-1) A4, A5 (wherever the active autonomy requires a proposal), A6,
  A7, A12 and A13 are **reserved to the person**. The SWB model-change class
  is **may apply within granted autonomy** (DERIVED from V4-HI-41) with the
  accepted default setting *propose*. Operation-specific additions await
  OI-021. The ruling does not show SWBPIPE adoption or enforcement (DEP-001).
- Examples use the invented model **FX-PIPE-01** and are labelled **fixture
  subjects**. They record no act that anyone performed.

## 1. Settled distinctions relied on

| # | Settled distinction | Citation |
|---|---|---|
| D1 | Workflow definitions, the person's decisions and accepted records are ordinary files in the user's project or workspace | V4-REC-02 |
| D2 | A harness session store is operational, not the authority for any human act; coordination views are derived and rebuildable | V4-REC-03; V4-PM-06 |
| D3 | Host domain truth stays in the host's own store | V4-REC-01 |
| D4 | Host receipts, hashes and origin marks evidence what changed; the run record links them and does not copy them | V4-HI-71; V4-REC-04 |
| D5 | `success` means it ran, never that a person accepted anything; a submitted proposal is "queued" until the host records acceptance and application | V4-HI-25 |
| D6 | Proposal lifecycle drafted → validated → queued → accepted → applied (receipt), with rejected / withdrawn / stale, and outcome unknown | V4-HI-23 |
| D7 | Only observed events are shown as having happened; an unobserved outcome is shown as unknown | V4-EXE-03; V4-EXM-31 |
| D8 | A human act binds to the content it concerns and lapses visibly when that content changes | V4-HI-32; V4-REC-05 |
| D9 | "accept", never "approve", for proposals; accepting an edit is not engineering approval | V4-HI-33 |
| D10 | No fabricated human act; faithful recording of an actually performed act is permitted | V4-HI-31; V4-AUT-03; d3 |
| D11 | Acts are distinct subjects; evidence of one establishes none of the others; no universal acceptance-first chain | d3; V4-AUT-03 |
| D12 | Nothing agent-produced is presented as certified, sealed, approved or code-compliant | V4-AUT-05 |
| D13 | Git history and reviewed pull requests are primary change records | V4-OPS-31 |
| D14 | Reserved to the person (first increment, App/shared): mark checked; accept wherever autonomy requires a proposal; engineering approval; reliance; changing the grant or enabling external access. No grant widens past a reserved act or declared checkpoint. The host names and enforces its own list | OWNER_DECISIONS D2; V4-HI-30 |
| D15 | App routine tool-permission and sandbox modes are the user's own Codex setting; they govern tool execution only and never stand in for a reserved or professional act. Hosts have no classifier mode in the first increment | OWNER_DECISIONS D3 |

## 2. Ordinary-file authority rules

| Rule | Statement | Serves |
|---|---|---|
| FA-1 | The authority for "person P performed act K on content C for purpose U" is an **act record** in an ordinary project/workspace file together with the evidence it references. Nothing else supplies a missing act. | REQ-001, REQ-003; AC-001 |
| FA-2 | Harness session content, transcripts, agent memory, derived views, search indexes, PEC projections and tool-permission settlements (A14) may **locate** evidence. Their assertion that an act occurred is not an act record and creates none. | REQ-001; D2; D15 |
| FA-3 | Host domain truth, receipts, hashes and origin marks stay with the host. A record holds **references** plus the minimum needed to resolve and compare them (reference, claimed identity, identity method designation where an identity is claimed, resolution status). It never holds a copy that could stand in for host truth. | REQ-002; D3, D4 |
| FA-4 | Workflow definitions and accepted records remain owned by their producing deliverables. This format supplies the act and run records that refer to them. | REQ-001, REQ-005 |
| FA-5 | A written act record is not later edited to change actor, act kind, bound content, scope or purpose. A correction is a new record naming the corrected record and why; both remain readable. (Proposed; mechanism unselected.) | REQ-003, REQ-004 |
| FA-6 | Git history remains the primary change record for the files (D13). A record cites a repository revision where its own revision matters; it does not duplicate commit history. | AX-003 |
| FA-7 | Each record identifies its **format version** and **record kind**; a reader refuses or limits an unknown version rather than guessing. | OUT-001 |
| FA-8 | The **recorder** is always identified and is never the decision actor merely by having written the record. | REQ-003; D10 |
| FA-9 | App runs keep records with the user's project/workspace; host-agent runs keep records with the host project (V4-HI-70). Exact path and host persistence are not selected (U-05, U-06). | REQ-001, REQ-005 |

## 3. Record kinds and identity

| Record kind | Authority for | Produced by |
|---|---|---|
| Run record | That a workflow run occurred with the identified workflow, conversation, model, settings, requested operations and observed outcomes, linking host evidence | App record writer (OUT-002) for App runs; host run recording (external owner, DEP-04-03-016) for host-agent runs, in the shared meaning |
| Human-act record | That an identified person performed an identified act kind (A4–A7, A10–A13; A1/A2/A8 when the person performs them) on identified content, scope and purpose, with evidence | A recorder: App, host facility, or an agent performing A9 |
| Decline event record | That a person decided **not** to perform A4, A6 or A7 on an identified subject (R1_RESOLUTIONS R-5). It is not an act of that kind and satisfies no checkpoint | Same recorders; naming to be confirmed with DEL-04-01 at IR1 (U-13) |
| Decision / accepted record | A PKG-06 or workflow-owned record that an act record may cite | Its owning deliverable; consumed only |

Common identity elements (semantic): *record identity*, *record kind*, *format
version*, *recorder identity*, *recording context* (App, or host identity),
*written-at order*, *corrects* (optional).

## 4. Run-record inventory

Every element named in REQ-002 / SOW-186 / V4-HI-70 is present. "Required"
means present **as a value or as an explicit absence statement**.

| # | Element (semantic) | Meaning | Supplier (by accepted meaning / R1 ruling) | Absent / unknown handling |
|---|---|---|---|---|
| R1 | Run identity | Stable identity of this run, distinct from conversation, proposal and operation identities | Record writer | Required |
| R2 | Workflow identity as observed | {kind, origin (project / user / bundled / host), source root, name, revision} + derived-from; promised vs observed kept separate. An unadapted carried workflow keeps its original origin; a host adaptation has host origin and derived-from; "App-origin" is not an origin class | DEL-02-01 (per R1_RESOLUTIONS R-9; to be confirmed at IR1) | Selection alone does not show supply or adoption |
| R3 | Supplied guidance identity and limits | Content identity of each guidance input actually supplied, **per thread and turn**, not only the launch configuration; where provider adoption/enforcement is unobservable | DEL-01-01 (R-10), DEL-02-04 (M2; later undertaking per D1) | "Not observed" stays explicit; no adoption claim |
| R4 | Conversation reference | Reference to the harness conversation/session | Harness | Reference only — operational, not authority (D2) |
| R5 | Model used | Model identity and serving endpoint class (local server / user-chosen cloud) as observed, separate from configured | DEL-01-01, DEL-05-01 | "Requested X; observed unknown" is valid |
| R5a | Seat role meaning | The role meaning of the agent seat that acted; "unknown" when not determinable | DEL-05-01 / DEL-02-01 (V1-C AB-02; R-7) | Unknown recorded as such |
| R6 | Autonomy settings | Every settings version in force or requested for the run, with **scope**, per-class treatment, display state (§8 list), **requester**, **setting actor**, **A12 act record reference** for person-set states, **establishment evidence** (control confirmation) or refusal reason | DEL-04-02 settings-in (§8); DEL-04-01 policy | Unconfirmed, not set or refused recorded as such, never as effective |
| R7 | Requested operations | One entry per submission or read (§5) | Loop/adapter trace; DEL-03-01; DEL-03-02 | Required per request made |
| R8 | Checkpoint events | Declared checkpoint, its *reached-when* observation, bound subject referent, disposition (waiting · performed · resolved negatively · lapsed · not reached · unknown), satisfying act record or A10 / decline event reference | DEL-02-01 declares; DEL-05-01 evaluates in hosts; DEL-02-03 hold machine (R-5) | Not observed → *not reached*, never satisfied |
| R9 | Human acts | References to human-act and decline-event records (§6) | §6 | None created without evidence |
| R10 | Agent examination findings | References to A3 findings attached to rows/results | Agent output | Findings are A3, never A4. If the host stores findings through a change operation, that is an R7 entry too (DEL-03-01 U-C5, U-14) |
| R11 | Evidence limits | What the recorder could not observe (lost acknowledgement, missing receipt, unresolvable reference, origin mismatch, unobserved adoption) | Record writer | Required |
| R12 | Record identity elements | §3 common elements | Record writer | Required |
| R13 | Tool-permission settlements (A14) | Reference to each tool-permission request and its settlement origin (person; user's Codex mode inside the supplier; App named-rule decline or explicit error) | DEL-01-01 settlement origin; DEL-01-02 (later undertaking) | Never placed in R6; never a human-act record of A4–A7/A12 (D15). Proposed home; DEL-04-01 to confirm (U-10) |

## 5. Operation entries and outcome evidence

**Entry elements (semantic).** Operation identity and version (DEL-03-01);
**request-side origin** with all DEL-03-02 origin elements — author type
(person / agent), author identity (seat/role instance), channel (embedded /
external / human UI), conversation, workflow run, autonomy standing at
drafting, reason; **host origin-mark reference** (linked, not copied; a
mismatch with the request-side origin is an R11 limit); **relied-on basis**
(workspace identity, generation, model revision, canonical content identity
with method designation — as cited, never a later queue-time basis, HI §11);
**observed basis** for read and non-mutating check entries; **evaluated
basis** on every non-success; **route** (direct / proposal); **settings
reference at route decision (validation)** and **settings reference in force at
application** (host-reported, otherwise *unconfirmed*) (R-8); treatment at
resolution when it differs from standing at drafting (R-3.6); **proposal
identity** and per-item **change-item content identity** (R-6); **item
dispositions**; **outcome**; receipt references; standing received
(V4-HI-12); **submission ordinal**; **undoes ⟨entry⟩** where the operation is an
undo (V1-B D-18); outcome **reporter** for outcome unknown.

**Outcome vocabulary** is DEL-03-02 §9 and DEL-03-01 §4.1, adopted unchanged
(per R1_RESOLUTIONS R-7; to be confirmed at IR1). The record may state an
outcome only with the listed evidence:

| Outcome as recorded | Minimum evidence referenced | Actor / reporter | May NOT be inferred from |
|---|---|---|---|
| unavailable | Catalog precondition failure with reason and evaluated basis (HI-04 parity) | Host | Channel off; policy refusal |
| not exposed on this surface | Per-surface exposure element (DEL-03-01, R-9) | Host / adapter | *unavailable*, *missing*, *channel not enabled* |
| channel not enabled | External access off; A13 not performed | Adapter / host | *unavailable* |
| not permitted | Governing treatment and policy record named; evaluated basis (R-3.2–3.4). A direct request without an effective direct treatment is *not permitted*, never silently converted to a proposal | Host route | Absence of a grant alone rendered as unavailable |
| error | Catalog error identity, evaluated basis, partial-effect statement | Host | — |
| drafted / validated | Host validation result reference (validated) | Proposer / host | Agent assertion |
| refused — invalid | Host validation refusal with catalog error; nothing applied | Host | — (never "rejected") |
| stale (refused) | Host refusal with reason, **relied-on basis and current basis** | Host | Local basis comparison alone |
| queued | Host queue acknowledgement | Host | Transport completion |
| accepted (per item) | A5 human-act record bound to the item's change-item content identity | Person (A5) | Success, a later receipt, agent statement |
| rejected (per item) | A10 human-act record | Person (A10) | Host refusal; silence; timeout |
| withdrawn | A11 record by the proposer | Proposer (A11) | Person removing another's proposal (that is A10) |
| applied (after acceptance / direct under grant) | Host receipt reference; for direct, origin mark + settings references; the association proposal/item ↔ relied-on basis ↔ receipt ↔ resulting revision | Host | `success`, queued, accepted |
| application error | Error identity + effect statement: none / partial (with receipt references) / unknown (→ outcome unknown) | Host | — |
| outcome unknown (overlay) | The observation gap; **last observed state** | Whoever lost observation: loop, App adapter or host | — (default when evidence is missing) |
| success (operation ran) | Result reference and observed basis (reads, non-mutating checks) | Host | Any human act |

Rules. **OE-1** Transport success, tool-call return, source resolution or a
resolvable receipt *reference* never upgrades an outcome (REQ-002; V4-EXM-31).
**OE-2** A re-draft after a stale refusal is a new entry with a new proposal
identity and lineage; the stale entry stays. **OE-3** Each submission,
including a retry of the same proposal identity, is its own entry, and records
only the effects actually observed (the same receipt, two receipts, or
unknown). "One effect per proposal identity" is a host obligation to be
evidenced (DEP-001), not a recorded fact (R-7). **OE-4** A retry keeps the
same proposal identity (R-7). **OE-5** A derived proposal state is never
stronger than its item dispositions. **OE-6** An undo is a change through the
one route with its own entry, origin, basis and outcome; *undone* is recorded
as applied (receipt) with the *undoes* relation (V1-B D-18; DEL-03-02 to
confirm at IR1).

## 6. Human-act record

### 6.1 Elements (semantic)

| Element | Meaning | Required |
|---|---|---|
| Act identity | Identity of this act record | Yes |
| Act kind | Canonical name A1–A14 (R-1) | Yes |
| Act class | As applicable: for A4–A7, A12, A13 "reserved to the person (D2)"; for acts on a catalog operation, the operation's class from the DEL-04-01 policy-class record; "operation-specific addition pending OI-021" where so | As applicable |
| Governing policy reference | DEL-04-01 adopted-decision record and its **policy revision identity**; for D2/D3, `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` | With act class |
| Decision actor | The person who performed the act | Yes |
| Recorder | Software, host facility or agent that wrote the record | Yes |
| Recording mode (sub-element of A9) | *direct capture* (the capturing surface wrote it) or *faithful recording* (recorder ≠ capturing surface; cites capturing-surface evidence) | Yes |
| Bound subject | Change item(s) (A5/A10); host row/object (A4/A6/A7); App file; settings version (A12) | Yes |
| Bound content identity c₀ | With its **identity method designation** m₀: change-item content identity (DEL-03-02) for A5/A10; subject content identity (DEL-03-01) for A4/A6/A7 on host content; file content identity for App files; settings-version identity for A12 | Yes, or "not obtainable" → lapse permanently *unknown* |
| Scope | Change-item identities for A5/A10 (a batch/multi-row A5 lists several items, each item-bound); row/object identities for A4/A6/A7 | Yes |
| Purpose | What the act was for, in the actor's terms | Yes |
| Evidence references | Capturing-surface evidence (host act facility for host content; App interface for App acts), each with resolution status | At least one |
| Evidence limits | What the evidence does not show | Yes |
| Relations | Run, operation entry, checkpoint, workflow, decision record | As applicable; **no required prior act** |
| Order | Sequence/time as evidenced | Yes |
| Lapse evaluation | Latest state with compared c₀/c₁ and m₀/m₁ (§7); derived, re-computable | Derived |

### 6.2 Rules

- **HA-1** An act record is written only from evidence that the person
  performed the act. A proposal, operation success, grant, receipt, A3
  findings, A8 request, A14 settlement, silence or timeout is not such
  evidence (D5, D10, D15).
- **HA-2** Decision actor and recorder are separate elements; an agent
  recorder never appears as decision actor for A4–A7, A10, A12, A13.
- **HA-3** One record, one act kind. A5 never produces A4, A6 or A7, and vice
  versa. An independently evidenced act is recordable without any A5.
- **HA-4** A6 and A7 records name the accountable person and scope only as
  evidenced; no certification, sealing or code-compliance label (D12). A6 is
  engineering approval only; V4-HI-65 design-candidate approval is a separate
  later-increment act, out of this increment (R-1).
- **HA-5** A12 set grant (and A13) is recorded as a human-act record; R6
  references it. An agent's A8 request for a grant change creates no A12.
- **HA-6** Act class is carried, never computed here. A class without a policy
  basis is shown as such, never treated as permission (R-3.5).
- **HA-7** Faithful recording (A9) by any identified recorder distinct from
  the decision actor is a **conformant record shape**. It satisfies a
  checkpoint only because the attributable evidence it cites comes from the
  capturing surface (R-5). Any host-specific capture requirement is the
  host's (DEP-001; U-11).
- **HA-8** A person's decision not to perform A4/A6/A7 is a decline event
  (§3), not an act of that kind. For A5 the negative decision is A10.

## 7. Content binding and lapse comparison rule

Notation: *S* bound subject; *c₀*, *m₀* bound content identity and its method
designation; *c₁*, *m₁* the current identity of the same subject and scope.

| Step | Rule |
|---|---|
| L-1 | Obtain c₁ for exactly the bound subject and scope, from one of three sources (R-6): **change-item content identity** (DEL-03-02) for A5/A10; **subject content identity** per row/object (DEL-03-01, host-supplied, distinct from the read-basis canonical content identity) for A4/A6/A7 on host content; **file content identity** for App files. Never the workspace generation or model revision: an unrelated edit must not lapse a subject-bound act. |
| L-2 | Compare the **identity method designations**. If m₁ ≠ m₀ or comparability cannot be shown → **unknown (incomparable)**, never "not lapsed". |
| L-3 | If c₁ cannot be obtained → **unknown (unavailable)**. |
| L-4 | If S no longer exists → **lapsed (subject absent)**. |
| L-5 | If c₁ = c₀ → **not lapsed**. |
| L-6 | If c₁ ≠ c₀ → **lapsed**: shown lapsed for the changed content, retaining c₀, scope and purpose; not carried to the new content. |
| L-7 | Multi-element scope: evaluate per element. A batch A5 lapses **per item** (settled by per-item binding, R-6). A multi-row A4 with some rows changed is **partially lapsed**, listing the rows; whether its purpose survives for unchanged rows is an owner question (U-07). |
| L-8 | Lapse never deletes or edits the act record (FA-5). The historical fact remains; lapse concerns effectiveness for current content. |
| L-9 | The host may present its own lapse (V4-HI-32). Where supplied, the record links it; if App and host evaluations disagree, both are shown and the disagreement is an R11 limit. |
| L-10 | Applying an accepted change item does **not** lapse its A5 (the change-item identity is unchanged). A basis failure between A5 and application is a **stale refusal** under DEL-03-02 (U-P3), not a lapse. |
| L-11 | If content returns to c₀ after an observed lapse (restore, revert, new generation), the evaluation shows "matches c₀ again after an observed lapse" and keeps the lapse interval visible; whether the act is effective again is `UNRESOLVED` U-12. It never silently reverts to *not lapsed*. |
| L-12 | A lapsed act that performed a checkpoint moves that checkpoint's disposition to **lapsed**; re-hold is DEL-02-03's (R-5). |

Lapse states: not lapsed · lapsed · lapsed (subject absent) · partially
lapsed · matches c₀ again after observed lapse · unknown (incomparable) ·
unknown (unavailable) · not yet evaluated. *Not yet evaluated* never renders
as *not lapsed*.

## 8. Settings-in / record-out exchange with DEL-04-02 (CASE-002 M3)

Identical in DEL-04-02/AS-v0.2 §6. A data exchange, not an ordering between
human acts and not a second authority.

**Settings-in (DEL-04-02 → DEL-04-03 writer), per run and per change:** run
identity; settings version identity; **scope** (representation-neutral
dimensions, e.g. model/workspace, object set, run, period, consequence); per
operation class — treatment (direct / propose) and policy basis (DEL-04-01
record reference, or "no policy basis"); display state (effective · requested
by agent · set by person, not yet confirmed by control · unconfirmed · not set
· refused (reason)); **requester** (person, or agent via A8); **setting actor**
(the person, only where an A12 exists); **setting act reference** (A12 record);
**establishment evidence** (control confirmation) or refusal reason; order
relative to operation entries; source of control (App or host).

**Record-out (DEL-04-03 reader → DEL-04-02), per run:** record identity and
format version; recorded settings versions with the fields above; per
operation entry the two settings references, route, outcome, item
dispositions, receipt/origin references and evaluated/relied/current bases;
act and decline-event records with actor, recorder, **recording mode**, kind,
**act class**, **bound subject**, scope, purpose, **c₀/c₁ with method
designations**, lapse state and **evidence references with resolution
status**; **checkpoint events** (R8); evidence limits.

**Comparison (DEL-04-02)** per settings version: displayed vs recorded →
*match* · *mismatch* · *missing in record* · *missing in display*. Mismatch is
shown to the person and returned as a defect observation. The record is
authoritative for what was recorded; the control for the current grant; the
display is derived. Neither side auto-corrects the other. A person-set state
without an A12 reference is a defect, not an established setting.

## 9. Evidence references

Each reference carries: evidence kind (receipt, content identity, origin mark,
host act record, commit, supplier settlement), claimed identity, identity method
designation where applicable, resolution status at write (resolved /
unresolvable / not supplied) and at read. "Resolved" means the source was
found with the claimed identity; it does not make the referenced change or act
more than the source itself states (OE-1).

## 10. Consumer and host interface

| Consumer | Consumes (meaning) | Supplies back | Held part / limit |
|---|---|---|---|
| DEL-02-01 | Canonical act names for checkpoints; R8 dispositions; R2 | Workflow identity; checkpoint reached-when and subject referent (R-5, R-9) | Checkpoints may require A4, A5, A6, A7 or A12 (closed list) |
| DEL-02-03 | R8 waiting/performed/lapsed; R7 unknown outcomes | Hold machine, re-hold on lapse (W7) | App-side checkpoint act evidence (V1-C AB-11) at W7 |
| DEL-03-01 | R7 identity/basis; c₁ for A4/A6/A7 | Subject content identity; identity method designation; exposure element; shared fixture (R-6, R-9) | Algorithm unselected (TBD-003) |
| DEL-03-02 | §5 evidence rules | §9 outcomes; change-item content identity; origin; U-P3 | One-effect mechanism (V4-HI-23) unselected |
| DEL-04-02 | Record-out (§8); lapse, unknowns, act distinctions | Settings-in (§8) | Executable M3 trace needs candidate writer/reader |
| DEL-05-01 | R4/R5/R5a/R7 meanings; checkpoint evaluation in hosts | Loop-reported outcome unknown; origin, seat role and grant in force per dispatch (R-7) | — |
| DEL-05-02 | Act, decline and lapse display meanings | — | — |
| DEL-01-01 | R3, R13 meanings | Supplied-guidance content identity per thread/turn; A14 settlement origin (R-10) | Pin 0.158.0 is definition only (D4) |
| PKG-06 (DEL-06-01/06-02) | Act records cited by coordination; actor ≠ recorder; lapse | Decision records as act subjects | Coordination recorder never becomes actor |
| DEL-09-11 | Complete records for the week-later reconstruction | — | This format does not perform the witness |
| DEL-01-02, DEL-01-04, DEL-02-02, DEL-02-04 | R3/R4/R7/R13; act display; review/registration acts | Observation evidence; supplied role bytes | Outside this undertaking (D1); meanings retained for the later undertaking |
| External host run recording (DEP-04-03-016; DEP-001) | §§3–9 to record host-agent runs linking its receipts | Receipts, origin marks, host act records, subject content identities, host lapse, capture requirements | Adoption unclaimed; OI-013 placement |

## 11. Excluded acts and owners (REQ-006)

OI-001/OI-002 were decided at App/shared level by the Owner in DECISION-1
(D2, D3); operation-specific additions remain with the Owner via the outside
SWB session and App/shared owner (OI-021). Defining and carrying adopted
policy — DEL-04-01. Autonomy/standing UI — DEL-04-02. Reconstruction witness —
DEL-09-11. Host domain changes, receipts, domain storage, host run recording,
host enforcement of its reserved list — responsible host owner (SWBPIPE outside
session). Performing any human act — the person. Professional reliance and
certification judgments — the accountable professional. This format faithfully
records evidenced acts; it performs none of them.

## 12. Examples (fixture subjects — invented; no act was performed)

Model **FX-PIPE-01** (R-9). Operation references follow the DEL-03-01 §10
catalogue as quoted in V1-B: OP-C3 non-mutating check, OP-C4 add support,
OP-C5 model change (class *may apply within granted autonomy*, default
*propose*), OP-C6 mark row checked (*reserved to the person*). **Local
divergence, stated per R-9:** the shared v0.2 timeline was under concurrent
repair and not readable under this repair's scope, so row labels S-1…S-5,
revisions rN, proposal P-2 and basis B2 below are local illustrations to be
aligned with DEL-03-01 §10 at IR1.

**E1 — Proposal, per-item acceptance, application.** Run ⟨run:1⟩; workflow
{kind workflow, origin project, root ⟨root⟩, name supports-adjust, revision
⟨rev:w1⟩}; settings ⟨set:1⟩ effective: OP-C4/C5 → propose, scope "FX-PIPE-01,
this run". Proposal P-2 (OP-C4) with items i1 (S-3), i2 (S-4), i3 (S-5), relied
basis B2 (r12). Outcome queued (host ack). ⟨act:1⟩: **A5 accept**, actor
"fixture engineer", recorder host acceptance facility, mode direct capture,
scope {i1, i2}, c₀ = change-item identities ⟨ci:i1⟩, ⟨ci:i2⟩ with m ⟨m:ci⟩,
class "reserved to the person (D2b)". ⟨act:2⟩: **A10 reject** i3. Applied i1,
i2 with receipt ⟨rcpt:1⟩, resulting r13. ⟨act:1⟩ remains **not lapsed** after
application (L-10). No A4, A6 or A7 exists or is implied.

**E2 — Faithful recording (A9).** The engineer marked S-2 checked in the host
(OP-C6, reserved); host act record ⟨hact:9⟩. The App agent writes ⟨act:3⟩:
**A4 mark checked**, actor engineer, recorder App agent, mode faithful
recording, evidence ⟨hact:9⟩ resolved, c₀ ⟨sci:S-2@a⟩ (subject content
identity, m ⟨m:sci⟩). Conformant as shape; host capture requirement per host
(HA-7).

**E3 — Negatives.** (a) Agent drafted P-3 only → no act record. (b) OP-C3
check returned success → R7 success with observed basis; R10 findings; no A4.
(c) ⟨set:2⟩ granted direct → no act on any content. (d) Transcript says
"engineer approved" with no evidence → nothing written; R11 limit. (e) A Codex
tool-permission prompt answered by the user's own mode → R13 entry; no act.

**E4 — Lapse on rows.** ⟨act:4⟩: A4 on rows S-1 and S-2, c₀ ⟨sci:S-1@a⟩,
⟨sci:S-2@a⟩. S-2 edited (model revision advances) → ⟨act:4⟩ **partially
lapsed** (S-2), S-1 not lapsed; purpose effect U-07. Control: S-5 edited
instead → ⟨act:4⟩ not lapsed although the model revision advanced (L-1).

**E5 — Unknown outcome.** Direct OP-C4 under ⟨set:2⟩ (effective direct, scope
"S-1…S-5, this run"); acknowledgement lost at the loop. R7: outcome unknown,
reporter loop, last observed state "dispatched"; settings at route decision
⟨set:2⟩, in force at application *unconfirmed*; receipt not supplied. A later
read showing a new support is recorded as a separate read entry with its own
observed basis, not back-filled.

**E6 — Duplicate submission.** P-2 retried after E5-style loss: two R7
entries, same proposal identity, submission ordinals 1 and 2; entry 2 records
receipt ⟨rcpt:1⟩ as observed; entry 1 remains unknown. No "one effect" is
written as fact (OE-3).

**E7 — Grant change.** Person widens OP-C4 to direct within scope "S-1…S-5,
this run": ⟨act:5⟩ **A12 set grant**, bound subject ⟨set:2⟩; settings-in
carries requester = person, setting actor = person, A12 reference, then
establishment evidence. An agent's earlier A8 request appears only as
"requested by agent".

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 Operation-specific reserved additions `OI-021` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Act class may read "pending OI-021" |
| U-02 Consequence vocabulary for grant scope and classes | DEL-04-01 with host policy owner (V1-A AB-04) | Before class assignment in DEL-03-01 | Scope dimension "consequence" carried as a slot only |
| U-03 Supplier v0.2 elements taken from R1_RESOLUTIONS (R-1, R-3, R-5…R-10) | DEL-04-01, DEL-03-01, DEL-03-02, DEL-02-01, DEL-01-01 | IR1 | Names and elements confirmed or repaired at IR1 |
| U-04 Serialization, field names, content-identity algorithms, record-identity form | DEL-04-03 with DEL-03-01 (TBD-003) and affected consumers | Before OUT-001 CONFIG and writer implementation | L-2 depends on method designations only |
| U-05 Record file location in the App project/workspace | DEL-04-03 with OI-014 owners | Before writer implementation | FA-9 states only "ordinary files" |
| U-06 Host persistence/placement of host run records `OI-013` | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Host recording follows meaning only |
| U-07 Purpose of a multi-row A4 after partial lapse | DEL-04-01 with Owner (R-2) | Before lapse display criteria are fixed | L-7 reports per-row lapse only |
| U-08 Whether workflow review/registration is a named act kind | DEL-04-01 with DEL-02-02 (later undertaking, D1) | DEL-02-02 definition | Not recorded in this undertaking |
| U-09 Basis fails after A5, before application (DEL-03-02 U-P3) | Host owner with DEL-03-02 and DEL-04-03 | Before stale-rule implementation | Recorded as stale refusal (L-10); disposition of A5 on that path open |
| U-10 Home of A14 settlements (R13) | DEL-04-01 with DEL-04-03 (V1-A AB-05) | IR1 | R13 proposed; never R6 |
| U-11 Host capture requirement per act kind | Host owner (DEP-001; V1-A AB-06) | Before host act-recording integration | HA-7 treats faithful records as conformant shape |
| U-12 Effect of content returning to c₀ after observed lapse (restore/revert/new generation) | Host owner (generation, U-C2) with DEL-04-03 (V1-B X-05) | Before lapse display criteria are fixed | L-11 keeps lapse visible |
| U-13 Naming of the decline event | DEL-04-01 | IR1 | §3 record kind name provisional |
| U-14 Host-stored findings as a change operation (DEL-03-01 U-C5) | Host owner | Before V4-EXM-21 fixture binding | R10 may also need an R7 entry |
| U-15 Host receipts, origin marks, subject content identities, act records, lapse, per-operation settings version `DEP-001` | SWBPIPE outside implementation session | Before corresponding connected-journey integration/examination and fallback-replacement decision | All host evidence in examples is fixture |
| U-16 Shared component placement of reader/writer `OI-014` | App/shared contract owners | Before structural/production contract allocation | No common service assumed |

## Verification cases (designed, not run)

| Case | Input (fixture subject) | Expected result | Serves |
|---|---|---|---|
| VC-01 Authority | E1; transcript and derived view claim an extra A5 on i3 | Only ⟨act:1⟩/⟨act:2⟩ shown; claim creates no act; session/view marked non-authoritative | VER-001 (AC-001) |
| VC-02 Inventory completeness | E1 run record | R1–R13 each present as value or explicit absence | VER-001 (AC-002) |
| VC-03 Link not copy | E1 with ⟨rcpt:1⟩ | Reference, claimed identity, resolution status only; no receipt body or domain values | VER-001 (AC-002) |
| VC-04 Faithful recording | E2 | A4, actor engineer, recorder App agent, mode faithful, capturing-surface evidence cited; conformant as shape | VER-002 (AC-003) |
| VC-05 Fabrication negatives | E3 (a)–(e) | No act records; (d) R11 limit; (e) R13 entry only | VER-002 (AC-003) |
| VC-06 Independent act | Engineer marks own edit checked, no proposal | A4 recorded; no A5 required or created | VER-002 (AC-003) |
| VC-07 Row lapse and control | E4 both branches | Changed row lapsed with c₀ retained; unrelated-row edit not lapsed despite model revision change | VER-003 (AC-004) |
| VC-08 Incomparable / unavailable | E2 with m₁ ≠ m₀; host unreachable | *unknown (incomparable)*; *unknown (unavailable)*; never not lapsed | VER-003 (AC-004) |
| VC-09 Model-row partial lapse (restated per R-6) | ⟨act:4⟩ A4 on S-1, S-2; then S-2 edited | Partially lapsed listing S-2; S-1 not lapsed; purpose shown as U-07 | VER-003 (AC-004) |
| VC-10 Acceptance survives application | E1 after apply | ⟨act:1⟩ not lapsed; item i1 edited later by the person → a new change, ⟨act:1⟩ still bound to ⟨ci:i1⟩ | VER-003 (AC-004) |
| VC-11 Restore after lapse | E4 then S-2 restored to c₀ | "matches c₀ again after observed lapse"; lapse interval visible | VER-003 (AC-004) |
| VC-12 Unknown outcome | E5 | Outcome unknown, reporter loop, last observed state; two settings references, second unconfirmed; no back-fill | VER-004 (AC-005) |
| VC-13 Transport-only | Proposal sent, no host ack | Not queued; unknown or drafted per evidence | VER-004 (AC-005) |
| VC-14 Duplicate submission | E6 | Two entries, same proposal identity, only observed effects | VER-004 (AC-005) |
| VC-15 Outcome vocabulary | One case each: unavailable, not exposed, channel not enabled, not permitted (direct without effective direct), invalid, stale (both bases), application error (partial), rejected (A10), withdrawn (A11) | Each recorded distinctly with its evidence and actor; none encoded as another; host refusal never "rejected" | VER-004 (AC-005) |
| VC-16 Grant change | E7; plus an A8 request only | A12 record referenced from R6; A8 alone yields "requested by agent", no A12 | VER-002 (AC-003) |
| VC-17 Coverage inventory | VC-01…VC-16 against AC-001…AC-005 | Each AC has ≥1 positive and ≥1 negative case; results name the candidate; distinct from DEL-09-11 | VER-005 (AC-006) |
| VC-18 Owner trace | §10, §11, UNRESOLVED | Each REQ-005 consumer and REQ-006 excluded act traced one-for-one; D2/D3 cited to DECISION-1; no delivery/adoption asserted | VER-006 (AC-007) |
