# Proposal, validation and outcome contract
- Contribution: DEL-03-02/P-v0.6 (supersedes DEL-03-02/P-v0.5, last changed at `375c3970c` and unchanged at `94aa9181b`, file sha256 6ab94fd10166cf78cda014a2f28ebf4726ce9f82a1c2f180044093b4bbb137e0)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (R8-1): in Phase 1 (this increment) declared workflow checkpoints are **plan guidance** (EXEC-v0.4 §2.1; WD-v0.6 §4.3.0). The governing checkpoint constraint, its carriage assurance (R2-12) and hold support are the **governance-phase definition (retained)**, stated beside a Phase-1 statement. V4-WF-05's first half is **phased to the governance layer, not withdrawn**, and is flagged for the next accepted-basis update. SWBPIPE's answers are recorded as answers about its current state, not commitments; host joins are deferred (DECISION-3)
- Serves: OUT-001 (proposal, relied-on basis, origin, governing checkpoint constraint, change-item content identity and outcome schema meaning), OUT-002 (lifecycle, one route, actor parity, host ownership and receiving interfaces), OUT-003 (designed contract fixtures); REQ-001–REQ-013; AC-001–AC-014; VER-001–VER-014
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 42328987c71dd243323805faf2634067cca0113b81ca93d4d129193b2a71128a; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7d…60da) §1, §§3–5 (V4-HI-11, V4-HI-20–25, V4-HI-30–33), §6 V4-HI-40–42, §7 V4-HI-50–52, §9 V4-HI-70–71, §10, §11; `P/docs/PRD.md` V4-PAR-04, V4-AUT-01–05, V4-REC-01, V4-CST-05/06, §9 OQ-02/OQ-11; `P/docs/ARCHITECTURE.md` V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-20/22/25; DECISION_BRIEF #d2/#d3/#d4/#d5; SCC-CASE-002 Case_Datasheet rows M1-P, M3-CP (sha256 6acdc6c4…a71a6); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f3…81f2e) D2/D3; R1_RESOLUTIONS.md (sha256 2f9c7e72…7ec4) R-1–R-9; R2_RESOLUTIONS.md (sha256 77cfb845…d088) R2-1–R2-21; R3_RESOLUTIONS.md (sha256 202d52c7…afbf) R3-3, R3-4; R4_RESOLUTIONS.md at `f05c7e4cd` (sha256 50a009b2…2a24) R4-3–R4-7, R4-12–R4-15, R4-19; R5_RESOLUTIONS.md at `8fb51f07f` (sha256 254d0b93…d6f1) R5-1, R5-2, R5-5, R5-6, R5-9; reviews V3-A (sha256 f25f5af1…1d87) and V3-B (sha256 5662fbd0…54a3) items addressed to P; OWNER_DECISIONS DECISION-2 D5/D6 (via R4-1/R4-2); review V2 (sha256 75ba1dff…e6ef) m-3, m-9, m-11; comparisons V1-A (01811533…4c09), V1-B (09eebfe0…1cae), V1-C (8d46258a…94a6); reviews IR1-A (31b3c7f8…8284), IR1-B (70e4a4f6…2846), IR1-C (295e96b3…26b9)
- Consumed inputs: **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12: item 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3). **v0.6 inputs (R8 pass, node A3, at `94aa9181b`).** R8_RESOLUTIONS.md sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02 (R8-1…R8-11; binding); INTAKE_MAP.md (I2) sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33: rows 01.6, 02.7, 03.3, 05.4, 07.2, 07.6, 08.1, 09.2, 09.3, 10.1, 14.1, 14.2, 22.2, 31.2; Part 2.2 P rows; Part 3 items 1, 2, 5, 10, 11, 12; Part 4.9, 4.11; Part 5 R8-Q12 (R8 overrides I2 where they differ); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"); owner decisions DECISION-3 and DECISION-4 with its clarification (OWNER_DECISIONS.md sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776); SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` (DEL-09-06 `Design/`, #1047) sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7: SQ-01…SQ-10, SQ-13, SQ-14, SQ-20, SQ-23, SQ-28, SQ-31, ANS §2–§3 — data about SWBPIPE's current state, not commitments (DECISION-3). **Owner files read first (at `94aa9181b`):** DEL-02-03 EXEC-v0.4 `EXECUTION_COMPATIBILITY.md` sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4 (§2.1 PH-1…PH-10; §2.2 GV-1…GV-5; §2.3; §3.6; §3.7 CC-2; §4.5 SP-4; §4.11 receiving notes; CH-17, CH-27); DEL-02-01 WD-v0.6 `WORKFLOW_DECLARATION.md` sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28 (§4.3.0 CG-1…CG-7; §4.3.1 `governed`, PROPOSED; §4.3.7); WD-EX-v0.6 `EXAMPLES.md` sha256 950b70b2e3f7fdda9a98b13a63746b76936be490dd96cb6e47bbe6dc9c3eba3d (R-5a/R-5b). DEL-03-01/C-v0.6 is co-revised in the same pass (node A3). Earlier: DEL-03-01/C-v0.5 (co-revised in the R5 pass: FXA-5 hold support and host-held note, V-GR1); the EXEC-v0.2, ADAPTER-v0.2 and XT-v0.2 texts were **not** read for this pass — R5 fixes their meanings used here (V3-B Y-7 note). Earlier: Wave-2 sibling texts read from commit `f05c7e4cd` — DEL-03-03/ADAPTER-v0.1 (sha256 58b2409c…a074: F-1, F-3, F-8), DEL-02-03/EXEC-v0.1 (sha256 e0ede76e…18e8: §4.7 resume/re-hold, MX-3/MX-6/MX-8 confirmation, CAP-1…9), DEL-09-09/XT-v0.1 (sha256 8f098c79…f1df: L-XT-1); DEL-03-01/C-v0.5 (co-revised in this sweep: §4.1 channel reporters and model-destination note, §10 FXA-n, K-7, V-ED1); earlier: DEL-03-01/C-v0.3 (co-revised: §3 elements incl. exposure, §3.1 five class values, §4.1 results with reporters, §4.4 precondition vs validation error, §5 basis, subject content identities and per-item "no longer holds" rule, §10 FX-PIPE-01 incl. OP-C10–C12 and variants); sibling v0.2 texts read from commit `28bd00499` where an R2 ruling touches a join — DEL-04-01/ACT-POLICY-v0.2 (sha256 e50f1fe2…93a9: §2.1–§2.5, §5.1–§5.5, §6, §8.3), DEL-04-03/RS-v0.2 (sha256 56a3f839…1c69: §5 outcome entries, OE-6, §7), DEL-05-01/LOOP-v0.2 (sha256 1151d432…62c9: §6.2 dispatch record incl. checkpoint constraint, §6.3 retry, MC-8), DEL-02-01/WD-v0.2 (sha256 c25bccc5…a55c: §4.3.7 item-level rule, §4.4 promised standing); DEL-04-02 grant display states by R-8/R2-6 meaning; host facilities (route, views, receipts, act capture, constraint receipt): not supplied (DEP-03-02-023)
- Receivers: DEL-04-02 (OUT-001, OUT-002; REQ-003–005; VER-003–005) via DEP-03-02-018; DEL-04-03 (OUT-001, OUT-002, OUT-004; REQ-002, REQ-003, REQ-005; VER-001, VER-004, VER-006) via DEP-03-02-019; DEL-03-03 (OUT-001, OUT-003; REQ-001, REQ-004; VER-001, VER-004) via DEP-03-02-020; DEL-05-01 (OUT-001, OUT-003; REQ-003, REQ-007; VER-008); DEL-05-02 (OUT-001, OUT-003; REQ-001–003; VER-001–003); DEL-09-09 (OUT-001; REQ-001, REQ-004; VER-001, VER-004) via DEP-03-02-022; DEL-03-01 (OUT-001, OUT-003; REQ-001, REQ-004; VER-004) as the M3-CP return (DEP-03-01-026); DEL-03-04 responsibility map via DEP-03-02-021; DEL-02-01 / DEL-02-03 (checkpoint constraint, item dispositions, item-left events); external host proposal-view receiving via DEP-03-02-024

## 0. How to read this definition

This is the 60% semantic definition of how a change, by a person or an
agent, is proposed or applied through a host, and how its outcome is
reported. Element names are **semantic labels, not wire names**. No
proposal-identity representation, content-identity method, schema encoding,
duplicate-effect mechanism, outcome-recovery mechanism, storage engine,
transport field, retry budget or retention interval is selected (TBD-002;
DEP-03-02-026), and no component placement (OI-014; DEP-03-02-025). Unruled
policy appears only as `UNRESOLVED{OI-nnn}`. **DERIVED**, **INTEGRATION** and
**PROPOSED** markings follow R1/R2; owner rulings are credited only with what
they say (R2-11).

§9 is the **canonical outcome taxonomy** for proposals and operations
(R-7). DEL-04-03, DEL-05-01 and DEL-05-02 adopt it and C §4.1 (as of
C-v0.5; carried in C-v0.6) unchanged. Fixtures use the shared catalogue FX-PIPE-01 (C-v0.6 §10); step
labels T… and variants V-… refer to it.

**Phase (R8-1; DECISION-4 D4-1, SETTLED; framing INTEGRATION).** In Phase 1
a workflow's declared checkpoints are plan guidance. Neither the App nor a
host's embedded loop enforces a hold, blocks a run, or reports a workflow
*unsupported* because a hold cannot be enforced (EXEC PH-1…PH-3). A human
act is recorded as done only when the person performs it, and the reserved
acts stand (EXEC PH-4, PH-5). The governing checkpoint constraint (§3.3),
its carriage assurance and the treatment it forces (§4.4), and hold support
are the **governance-phase definition, retained** (EXEC GV-1), for
checkpoints declared **`governed`** (WD-v0.6 §4.3.1, PROPOSED). Where this
file states such a case, it gives the Phase-1 result and the
governance-phase value; the governance-phase values read the fixture's
checkpoints as if they were declared governed (R8-11 item 5; EXEC GV-5).
Nothing in this file's outcome taxonomy (§9) changes by phase.

**SWBPIPE answers (R8; DECISION-3).** Notes marked *SWBPIPE (SQ-nn)* record
SWBPIPE's delivered answers as data about its current state (FACT on main,
or DRAFT #885: unmerged, not qualified, deferred). They are not commitments,
deliveries or adoption. **OI-003** here is the App v4 open issue; it is
unrelated to SWBPIPE's own OI-003 (R8-7).

Settled distinctions relied on (cited, not re-decided):

| Id | Settled distinction | Source |
|---|---|---|
| S-P1 | Every change passes through the host's one validation and application route; no second route for agents | V4-HI-20; V4-PAR-04 |
| S-P2 | An agent's change carries origin (author type, conversation, workflow run) and the basis it relied on | V4-HI-21 |
| S-P3 | Under granted autonomy the agent may apply directly: origin-marked, undoable, checkable later | V4-HI-22; V4-AUT-01 |
| S-P4 | Otherwise a proposal: drafted → validated → queued → accepted → applied (receipt), with rejected / withdrawn / stale, and outcome unknown when unobservable | V4-HI-23 |
| S-P5 | Stale is refused with reason and may be re-drafted on the current basis; later selection never retargets; submitting the same proposal twice has one effect | V4-HI-23 |
| S-P6 | Host views show old and new values, affected objects and why | V4-HI-24 |
| S-P7 | `success` means it ran, never that a person accepted anything; a submitted proposal reports queued until the host records acceptance and application | V4-HI-25 |
| S-P8 | Queued ≠ applied; applied edit ≠ engineering approval; a receipt records the operation outcome, not an act of acceptance | #d3 |
| S-P9 | Acceptance of a proposed edit is not engineering approval; the interface says "accept", never "approve", for proposals | V4-HI-33 |
| S-P10 | Agents never record a human act as performed when it was not; faithful recording (A9) is a conformant record shape | V4-HI-31; V4-AUT-03; R-5 |
| S-P11 | A human act binds to content and lapses visibly when content changes | V4-HI-32 |
| S-P12 | Domain truth and validation stay in the host; Chirality never presents agent output as the host's accepted result | V4-REC-01; V4-CST-05 |
| S-P13 | Workflow checkpoints override autonomy; no grant widens past a reserved act or a declared checkpoint. **Phase 1 (R8-11 item 2):** the reserved-act half binds, and the host enforces it through its operations; the declared-checkpoint half and V4-HI-42 are guidance, and the host's own treatment decides. They bind only for governed checkpoints in the governance phase | V4-HI-42; D2; R8-11 |
| S-P14 | **Adopted** (D2): A4 mark checked, A5 accept wherever the active autonomy requires a proposal, A6 approve, A7 rely, A12 changing the autonomy grant and A13 enabling external-agent access are reserved to the person. **DERIVED**: A10 reject is reserved wherever A5 is (R-1). **INTEGRATION**: disabling external access is also a person's A13 (R2-3). The host names and enforces its own list; SWBPIPE adoption is not evidenced. SWBPIPE (SQ-05): no named reserved list; every change waits for the person's Apply, which is A5 in the person's hands | D2; R-1; R2-3; V4-HI-30; DEP-001 |
| S-P15 | **Adopted** (D3): App routine tool-permission/sandbox modes (A14) remain the user's own Codex setting, govern tool execution only and never stand in for a reserved or professional act; hosts have no classifier permission mode; the SWB default proposal mode applies. A14 is recorded only in run record R13 (R2-8, INTEGRATION) | D3; R2-8; V4-HI-41 |

## 1. Host authority map (REQ-002, REQ-013; VER-003, VER-014)

| Facility | Owner | This contract's role |
|---|---|---|
| Domain objects, store and truth | Host owner (SWBPIPE outside session) | None; reads through DEL-03-01 |
| Validation, de-duplication, treatment resolution and the one application route | Host owner | Defines the receiving meaning of its outcomes |
| Receipts, origin marks, undo | Host owner | Refers to them; never manufactures one |
| Proposal views (old/new/objects/reason) | Host owner | Supplies the information the views need (§8; DEP-03-02-024) |
| Offering, capturing, recording and presenting human acts | Host owner (facility); the person (the act) | Consumes captured acts as evidence; never creates one |
| Catalog, read basis, content identities, exposure | DEL-03-01 | Consumed (§3.2) |
| Act names, class records, treatment → outcome map | DEL-04-01; residual policy: owner with App/SWB contract owners | Consumed |
| Grant display states and settings versions | DEL-04-02 (R-8; R2-6) | Supplied: origin and direct-autonomy semantics; consumes settings references |
| Human-act and run-record format | DEL-04-03 | Supplied: outcomes, receipt links, change-item content identity, item-left events |
| Workflow identity; checkpoint declaration; hold machine | DEL-02-01 (declares); DEL-05-01 (evaluates in hosts); DEL-02-03 (Phase 1: recording, EXEC §2.1; governance phase: hold machine and hold-support values, EXEC §2.2, §3.6) | Consumed in origin; governing checkpoint constraint element supplied (§3.3; governance phase) |
| External receiving adapter | DEL-03-03 (host owns endpoint) | Supplied: this same contract, including constraint carriage assurance |
| Integrated host guide | DEL-03-04 | Supplied: §1 and §13 |
| Joined external witness, extension trace | DEL-09-09 | Supplied: fixtures and outcome expectations |

A host-accepted result exists only where the host has recorded the relevant
act. Agent output without that record retains its actual standing
(*drafted*, *queued*, *finding*), never *accepted* (SOW-091). A host refusal
is never a person's rejection (§4.1).

## 2. One route and actor parity (REQ-001; SOW-070)

- Person, embedded agent and external agent submit changes to the **same**
  host validation/application route. The channel is attribution (§3.3), never
  a route selector.
- **Treatment is resolved on the host route** at validation and again at
  application (R-3 point 1). The loop (DEL-05-01) and, where one is on the
  dispatch path, an App adapter (DEL-03-03; none adopted in this increment, R5-2) relay the actor's intent —
  *propose* or *apply directly* — and, in the governance phase, any
  governing checkpoint constraint with its carriage assurance (§3.3); they
  do not decide treatment.
- **Equivalence rule.** For equivalent operation identity/version, arguments,
  relied-on basis and applicable authority, every channel receives the same
  outcome and the same error meaning (identity and text).
- **Permitted difference is authority only** (grant, reserved acts, class,
  checkpoint constraint). It is reported as *not permitted* naming the
  governing treatment — policy-class record (C-v0.6 §3.1) or governing
  checkpoint constraint — never as a different validation error. Per the R-3
  map and R2:
  - a request to apply directly without an *effective direct* treatment →
    *not permitted*; it is never silently converted into a proposal
    (INTEGRATION);
  - **governance phase (retained; R8-1):** a request to apply directly under
    a governed checkpoint's host-held constraint → *not permitted*, naming
    the constraint (R2-12). In Phase 1 the host's own treatment decides, and
    nothing is reported *not permitted* on a checkpoint's account (R8-11
    item 2; EXEC CH-27);
  - a request to perform a reserved act (S-P14) as the person → *not
    permitted*, with an A8 request *offered*; an A8 exists only if the agent
    actually issues it, with the requester identified (IR1A-10);
  - a *no policy basis* class (C-v0.6 §3.1) → direct *not permitted*; a
    proposal is available but confers no permission — any effect requires the
    person's A5 and host application (R2-1, R2-9, INTEGRATION).
- A denial by the App user's Codex tool permission (A14) happens App-side
  before any host request and is not a host outcome (S-P15).
- **A host that offers no method (R8-5).** SWBPIPE has no direct mode and no
  external Apply. A direct external request is refused `unsupported_method`
  (SQ-06). That refusal is relayed as host-reported *not exposed on this
  surface*, never *not permitted*, and R2-4 (a named rule) is recorded as not
  met by this host. The App never presents the host's no-Apply rule as a
  class value or a grant.
- No fixture or adapter may define an alternate agent mutation path, bypass
  validation, or apply outside the host route (AC-002).
- Person-origin changes use the same route and yield the same basis check
  and outcome meanings; whether a person's direct edit is represented as a
  proposal is host practice.

## 3. Change request elements (OUT-001; REQ-003; SOW-170)

### 3.1 Identities and the acceptance unit

| Semantic element | Meaning |
|---|---|
| Proposal identity | Stable identity of *this* proposal from drafting onward; the unit for one-effect (§7). A **retry** (resubmission after a lost acknowledgment or *outcome unknown*) keeps the same identity and unchanged content (R-7; V1-C AB-05). A **re-draft** receives a new identity (§5) |
| Lineage | For a re-draft: the identity of the proposal it replaces and why (e.g. stale) |
| Change items | One or more items, each with its own item identity within the proposal |
| **Change-item content identity** | An identity of the item's content: operation identity and version, bound targets, old values, new values and the relied-on basis (with relied-on target identities). Method unselected; carries a method designation (C-v0.6 §5.1) (R-6) |

Rules (R-6):

1. **Acceptance unit = change item.** Row-by-row acceptance is one A5 per
   item. Batch or multi-row acceptance is one A5 act listing several items,
   each bound to its own change-item content identity, with per-item lapse
   (V4-HI-41).
2. **A5 and A10 bind to the change-item content identity**, not to model
   rows. Any change to an item's content (including a re-derived old value)
   is a different item content; an acceptance never carries to it.
3. **Applying the accepted item does not lapse the acceptance.** The item's
   content identity is unchanged by its own application.
4. **A host view row** presents one or more change items. The row is
   presentation; decisions are per item (V1-B D-10).
5. **Sibling drafts (PROPOSED; aligned with LOOP MC-8, IR1-B B-m7, IR1C-16).**
   Several tool calls in one model response each form their own proposal.
   The loop never merges sibling calls into one proposal; items come only from
   one call's arguments. A call that explicitly names an existing proposal it
   extends is the drafter's choice, not a loop merge. Grouping mechanics:
   U-P9 (= LOOP T-OPEN-1).

### 3.2 Consumed catalog meaning (from DEL-03-01/C-v0.6)

| Element | From C | Rule here |
|---|---|---|
| Operation identity and version | C §3 #1 | The version the request was prepared for; not re-interpreted |
| Arguments | C §3 #3 | Checked against the catalog input schema before host domain validation (DEL-05-01 REQ-003) |
| Bound targets / affected objects | C §3 #3, #5 | Fixed at drafting (§6) |
| **Relied-on basis reference** | C §5.4 | The basis descriptor(s) — workspace identity, generation, model revision, canonical content identity, method designation — of the read(s) actually relied on, and the **subject content identities of each item's relied-on targets**; carried unchanged to every outcome; never replaced by a queue-time or application-time basis, which may be recorded as a separate element |
| Errors, §4.1 results, exposure | C §3 #7, §4.1, #9 | Reused as outcome reasons (§9); no separate vocabulary. Precondition vs validation error per C §4.4 |

This contract defines no separate basis authority (CLM-003).

### 3.3 Origin, attribution and governing constraint

| Semantic element | Meaning | Source |
|---|---|---|
| Author type | person or agent | V4-HI-21 |
| Author identity | The person, or the agent seat instance; or **unverified** where the host cannot verify the caller (e.g. over the external channel). *Unverified* is never presented as a verified person or agent; DEL-04-03 R11 records it as an evidence limit. SWBPIPE records the caller's identity as not verified (SQ-14) | V4-HI-21; V4-HOST-05; R4-15 |
| Seat role meaning | The role meaning in force for the seat, or *unknown* if it cannot be determined | DEL-02-01 SEAT-1 |
| Channel | host interface, embedded agent, external agent | V4-PAR-02 (attribution only) |
| Conversation | Conversation the agent change came from | V4-HI-21 |
| Workflow identity | {kind, origin, source root, name, revision} plus derived-from where adapted. An unadapted carried workflow keeps its original origin; host adaptation creates a new identity with host origin and derived-from. "App-origin" is not an origin class | R-9; DEL-02-01 §6.1 |
| Workflow run identity | The run within that workflow. SWBPIPE records neither the conversation nor the workflow run (SQ-14): the App records both App-side and links them by the host's request id | V4-HI-21; V4-HI-70 |
| Standing at drafting | DEL-04-02 grant display state — effective · **effective (policy default)** · requested by agent · set by person, not yet confirmed · unconfirmed · not set · refused (reason) — with **grant value** (direct / propose) and scope, as known when drafted | R-8; R2-6; R-3 point 6 |
| Settings reference at route decision | The DEL-04-02 settings version identity (or, for *effective (policy default)*, the policy-class record reference and its default) used when the host resolved treatment at validation | R-8; R2-6 |
| Settings reference at application | The settings version in force at application, **host-reported**; otherwise *unconfirmed* | R-8 |
| **Governing checkpoint constraint** — governance phase (retained; R8-1) | Present when a **governed** workflow checkpoint requires A5 on this operation's result: {workflow run identity, checkpoint name, required act A5, operation identity}. Absent otherwise. In Phase 1 the App carries none, and the agent never adds a field the host schema lacks (R8-10) | R2-12; R8-1 |
| **Constraint carriage assurance** — governance phase (retained) | How the constraint reached the host route. **Host-held**: the constraint is held on the host side — derived from the host's own resolved copy of the declaration or run association, or received and then verified against that copy; the **host loop's own evaluation (DEL-05-01 §6.2) is host-held** (the host loop is host-built, OI-013). **App-assured**: App code on the dispatch path adds it from the declaration; **not available in this increment** — no interposed App code is adopted (R4-2; D6, closed for Phase 1, R8-2). **Model-supplied**: the model composed it into the call, as in native external realization. **Absent**. A constraint the host merely **received** from an outside caller keeps its source's assurance (model-supplied or App-assured). **Only host-held carriage satisfies R2-12**; the host may record other carriage but does not rely on it | R4-14; R5-2 |
| Reason | Why the change is proposed, in the proposer's words | V4-HI-24 |

Origin and constraint are preserved through submission, every lifecycle
transition and outcome reporting; every dispatch carries origin, seat role
meaning, the grant in force and (governance phase) any governing checkpoint
constraint with its carriage assurance (R-7; R2-12; R4-14). The App-side request origin is recorded by DEL-04-03; the **host
origin mark** is linked, not copied, and a mismatch between the two is an
evidence limit (V4-HI-71; V1-B D-17).

**Constraint authority limit (R2-12; IR1-B X-9; R4-14).** A dispatch-carried
constraint is supplied by the actor's side, so the host cannot tell an
omitted constraint from none. Only *host-held* carriage supports the R2-12
treatment (R5-2); with *model-supplied* or *absent* carriage an omission can
only be recorded afterwards.

- **Phase 1 (R8-1; R8-11 item 2; R8-10).** No hold-support value is
  assigned, and the App carries no constraint. The agent follows the
  declaration as plan guidance and never adds a field the host schema
  lacks. SWBPIPE's batch preflight accepts exact objects only, so a
  constraint sent as a request field would be refused as `invalid_request`
  rather than honoured (SQ-02 (a), SQ-31). The constraint the declaration
  implies may be recorded App-side (DEL-03-03 GC-4). PROPOSED (I2 R8-Q12):
  where the host schema defines no element for it, that record carries the
  evidence limit "constraint not carriable on this host".
- **Governance phase (retained; R8-1, R8-2).** For hold support, a governed
  checkpoint whose held actions are host operations and whose constraint is
  only model-supplied is **not established** while SQ-02 is unanswered, and
  **not enforceable** once SQ-02 is answered with no host-held route (R6-1,
  R6-5; EXEC HS-3). **SWBPIPE answered SQ-02 on 2026-09-28 with no host-held
  route** (route (iv), none planned), so against SWBPIPE the value is **not
  enforceable** (HS-3 (c)). A later SWBPIPE decision to plan a route is a
  revision trigger. On the embedded surface the host loop's own evaluation
  is host-held, but SWBPIPE has no host loop (SQ-20). On the external surface
  R2-12 depends on the host holding the declaration itself. Relay question
  (DEP-001, U-P10), answered by SWBPIPE with none: does the host route
  receive the per-request constraint, or evaluate its own copy of the
  selected workflow's declaration? If a host uses its own copy, the dispatch
  element is still carried for record comparison where the host schema
  defines it. Where a caller-side constraint is omitted although the
  declaration contains it, the omission is recorded as an evidence limit
  (DEL-04-03 R11).

### 3.4 Change item content

| Semantic element | Meaning |
|---|---|
| Item identity | Identity within the proposal |
| Operation | Catalog operation identity and version (C §3 #1) |
| Affected object | Identity of the object changed (bound target); for a creation, a description (the host assigns the identity, reported as a resulting object, §9) |
| Relied-on targets | The objects whose state the item relies on, with their subject content identities from the relied-on read (used by the per-item basis check, §5) |
| Attribute | What of the object changes (or *created* / *removed*) |
| Old value | Value as of the relied-on basis |
| New value | Proposed value |
| Item reason | Optional item-specific reason |
| Change-item content identity | §3.1 |

## 4. Lifecycle (REQ-004, REQ-005, REQ-011; SOW-171, SOW-172, SOW-178)

### 4.1 Proposal states (outside an effective direct treatment)

```text
drafted ─► validated ─► queued ─► accepted ─► applied (receipt)
   │           │           ├─► rejected   (A10, the person)
   │           │           ├─► withdrawn  (A11, the proposer)
   │           │           └─► refused — stale  (a relied-on target no longer holds)
   │           │  accepted ─► refused — stale (target fails before application; §4.2)
   │           │  accepted ─► application error (effect: none | partial | unknown)
   └─► refused — invalid / stale / not permitted  (before queueing; stays drafted)
overlay: any submitted step whose outcome cannot be observed ─► outcome unknown (observer-attributed)
later: applied ─► applied, then reversed by ⟨receipt⟩ (§4.5)
```

States and dispositions are **per change item**; the proposal state is
derived (§4.3).

| State / disposition | Meaning | Entered by (actor) | Evidence |
|---|---|---|---|
| drafted | Proposal composed with operation, arguments, targets, relied-on basis and targets, origin, any constraint, items | Proposer (A1) | Proposal content |
| validated | Host validation found it valid against the relied-on basis; treatment resolved | Host | Host validation outcome with treatment and settings reference |
| queued | Submitted and held by the host for the person's decision | Host (on proposer's submission) | Host queue acknowledgment |
| accepted | The person accepted the item ("accept", S-P9) | **The person (A5)**; host captures | Host-captured A5 bound to the change-item content identity |
| applied (receipt) | The host applied the accepted item through its one route | Host | Applied-outcome association (§9) incl. **receipt** reference and resulting objects |
| rejected | The person rejected the item. **Only A10**; a person removing another's proposal is A10 (R-1) | **The person (A10)**; host captures | Host-captured A10 |
| withdrawn | The proposer withdrew its own proposal before application | **The proposer (A11)** | Host record |
| refused — stale / invalid / not permitted | Host refused on its route; not a person's act | Host | Refusal with reason, evaluated basis; for stale both bases and the failing targets; for not permitted the governing treatment |
| application error | A declared error raised during application | Host | Error identity (C §3 #7) and effect statement: *none*, *partial* (with receipt references), or *unknown* (→ overlay) |
| outcome unknown (overlay) | Result of a sent step cannot be observed | **The observer that lost observation** — loop, App adapter or host — attributed to it (R-7) | Absence of observation; last observed state |

Reporting rules:

1. A submitted proposal reports **queued** until the host records acceptance
   and application (S-P7). A successful *submit* is reported as queued, never
   as accepted or applied.
2. **Accepted alone is not applied.** *Applied* is reported only with a host
   receipt reference (REQ-011).
3. **Outcome unknown** is reported whenever the outcome cannot be observed,
   including when execution may have occurred; it is never inferred to be
   applied, failed, rejected or accepted. A later observation is reported
   separately with its own basis and does not back-fill the earlier report.
   Recovery mechanics are unselected (TBD-002).
4. Accepted, rejected and withdrawn are always relayed with their actor
   (A5/A10/A11) (R-7). A host refusal, or a host-review clear with no
   decision record, is never relayed as *rejected* or *withdrawn* (R8-5;
   §4.2).

### 4.2 Transitions beyond the drawn source lifecycle

| Case | Contract handling | Status |
|---|---|---|
| Validation fails before queueing | *refused — invalid* with the catalog error; stays *drafted*; no queue entry | PROPOSED; host confirmation U-P4 |
| Stale detected at validation | *refused — stale* (§5) | Follows HI §10 item 3 |
| A relied-on target no longer holds after *accepted*, before *applied* | *refused — stale* at application under the stale rule (§5), **not** model-row lapse (R-6). The recorded A5 stays bound to its unchanged item content and is **not lapsed**; the item is not applied; a re-draft is a new item content, so the A5 does not carry. **Display (R2-16):** "accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)"; the item's derived state is never "accepted" alone, nor "applied". Checkpoint effect per §4.3 (fixture V-S1) | R-6, R2-16 (INTEGRATION); host behavior evidence DEP-001 (U-P3) |
| Withdrawal before queueing | Discarding a draft; no host record required | PROPOSED |
| Queue cleared by the person in host review, with no decision record (SWBPIPE DRAFT #885 `withdrawn` / `cleared_in_review`; SQ-05 (g), SQ-09) | **Item-left** event, cause "cleared by the person, no decision record" (§4.3). Never A10 (no rejection was recorded) and never A11 (the proposer did not withdraw) | INTEGRATION (R8-5) |
| Engine refusal at the person's Apply (SWBPIPE DRAFT #885 `rejected: validation_rejected`; SQ-09 (e)) | *refused — invalid* at application, with the host's code; never A10 | INTEGRATION (R8-5) |
| Treatment narrowed while in flight | Already-queued proposal unaffected; a not-yet-applied operation is re-resolved at application (R-3 point 6) | INTEGRATION; host enforcement DEP-001 |
| Treatment widened while in flight | Never converts a queued proposal into direct application or an acceptance (R-3 point 7) | INTEGRATION |

**SWBPIPE (SQ-01, SQ-23; R8-5).** The host's A5 is Apply, which accepts and
applies in one step, per batch, with no A10 record. A stale Apply is refused
and records no acceptance, so *accepted — not applied: refused — stale* does
not arise on SWBPIPE. The App keeps that meaning (R2-16) and records that it
has no SWBPIPE counterpart; V-S1 (C §10.4), DEL-03-03 XF-30 and XT XC-08
remain App receiving cases.

### 4.3 Item-level acceptance, item-left events and derived state (V4-HI-41; V4-EXM-20; R2-18)

- Each change item carries its own disposition.
- The proposal's reported state is derived and never stronger than its
  items, e.g. "PR-2: item 1 accepted and applied (RC-1); item 2 rejected".
- Whether accepted items are applied separately or in one host application
  is a host input (U-P7). One-effect (§7) holds per item and per proposal.
- **Item-left events (R2-18).** When an item leaves the queue without a
  person's decision, this contract supplies an **item-left event**:
  {proposal identity, item identity, cause ∈ {refused — stale, refused —
  invalid, refused — not permitted (re-resolution at application), withdrawn
  (A11), cleared by the person with no decision record (R8-5)}, time,
  evaluated basis}. An item refused after an A5 (V-S1) is **not**
  an item-left case — it had a decision — but its per-item annotation shows
  "accepted — not applied: refused — stale".
- **All items decided** indication: true when every bound item has A5, A10 or
  an item-left event.
- For a checkpoint requiring A5 on a proposal, the mapping of these data to
  checkpoint dispositions (in Phase 1, labels on the record, EXEC PH-6) is
  **WD §4.3.7**, confirmed by DEL-02-03 (R4-7;
  R5-9). "Partial" is a per-item annotation, never a seventh disposition; a
  *performed* over a reduced subject is never presented as "all items
  accepted" (R2-18). Confirmed by DEL-02-03 (R4-7), with WD §4.3.7 MX-3 (a
  lost decision observation → *unknown*), MX-6 (every item left → the arrival
  is closed "replaced" by the next arrival) and MX-8 (application error or
  *outcome unknown* after A5 → disposition unchanged, annotated). A performed
  A5 checkpoint stays performed when an accepted item is later refused stale;
  the declared output is then not produced, with an annotation (R3-3). A5
  never re-holds after resume (R4-3); re-hold is governance phase in any
  case (R8-11 item 1).
- **SWBPIPE (SQ-01, SQ-09 (b), (f); R8-5).** Apply applies a batch
  atomically, and Clear discards queued batches without a record. Per-item
  A5/A10 decisions (C T11), mixed-item dispositions (R2-18, WD §4.3.7) and
  A10 records have no SWBPIPE counterpart. The App keeps these meanings and
  records the missing counterparts; it never synthesizes a per-item decision
  from a batch Apply beyond what the host's receipt names.

### 4.4 Direct-autonomy branch (V4-HI-22; S-P3)

Entry condition (R-8; R2-6): the host resolves, at validation, that the
DEL-04-02 display state for the operation class and scope is **effective
(person-set) with grant value direct**, or **effective (policy default)
whose policy-record default is direct** — no such default exists in the
first increment — and (governance phase) that **no host-held governing
checkpoint constraint** applies. SWBPIPE has no direct branch: it has no
grants, and every change waits for the person's Apply (SQ-05, SQ-06). Every other state (requested by agent; set by person, not yet
confirmed; unconfirmed; not set; refused; class *no policy basis*) leaves the
direct branch closed, and a direct request is *not permitted* (§2). A
person-set grant requires A12 act evidence (D2).

```text
drafted ─► validated (treatment: direct) ─► applied (receipt, origin mark, undo route, later-check route)
                ├─► refused — invalid | stale | not permitted
                └─► application error (effect statement)
overlay: unobservable ─► outcome unknown (observer-attributed)
```

- No *queued* or *accepted* state exists and **no acceptance is recorded or
  implied**. Reports never say "accepted" for a direct application.
- The application carries origin (§3.3) including both settings references
  (at route decision; at application, host-reported or *unconfirmed*),
  relied-on basis, receipt, resulting objects, origin mark, undo route and
  later-check route (access for later examination or checking; implies no
  act, R-4). These are abstract host contributions, host-owned.
- The basis check applies exactly as for proposals.
- **Acceptance checkpoint constraint (R-5; R2-12, DERIVED from V4-HI-42 +
  D2b) — governance phase (retained; R8-1).** *Phase 1 (R8-11 item 2;
  EXEC CH-27):* V4-HI-42 and WD I-7 are guidance. The agent proposes the
  operation as the plan expects; a direct request, if made, meets the
  host's own treatment, and nothing is reported *not permitted* on the
  checkpoint's account. *Governance phase:* when a governed checkpoint's
  constraint applies with **host-held**
  carriage (R5-2; model-supplied or absent carriage is not relied on) — the
  host route resolves *propose* for that operation in that run. A request to
  **apply directly** is **not permitted**, naming the constraint as the
  governing treatment; it is **never converted** into a proposal (R-3.3). The
  proposer may then submit a proposal separately; that proposal's queued
  items become the checkpoint's subject (reached-when kind (c) *proposal
  queued*, R2-17). A checkpoint requiring A4 on applied rows does not force
  proposal; in the governance phase the run holds after application for the
  A4 **where hold support allows**. Until host evidence of host-held
  evaluation exists on the acting surface, the governance-phase fixtures
  exercising this (V-CP1; LOOP FX-C9; PANEL PC-24; WD VC-11) are AWAITING
  INPUT (U-P10) — SQ-02 answered 2026-09-28: route (iv), no receipt and no
  host copy (not offered); SQ-20: no host loop; a SWBPIPE owner decision
  (ANS §2); host joins deferred (DECISION-3).
- **Other checkpoints.** *Phase 1 (R8-1; EXEC PH-2):* no checkpoint holds
  the run; the arrival and the person's act are recorded as observation.
  *Governance phase (retained):* any other governed checkpoint holds the run
  for the person's act (S-P13) **where hold support allows**. Hold support
  takes one of four values per checkpoint and surface (R5-1; DEL-02-03 EXEC
  §3.6): *enforced by the host loop*; *enforced on the host route*
  (host-held constraint, evidenced via SQ-02); *not established*; *not
  enforceable* — assigned by what the checkpoint must hold, not by how it
  arrives (R6-1). Against SWBPIPE, a checkpoint holding only host operations
  on X is *not enforceable* (HS-3 (c); SQ-02 answered with route (iv)), and
  one holding any App-side action is *not enforceable* (HS-5). App-run holds
  (D6) are closed for Phase 1 and re-open only when the governance phase is
  taken up (R8-2; EXEC U-E1); nothing is ever claimed as held that is not
  enforced.

### 4.5 Undo (R2-15)

- An undo is a **change through the one route** (§2) via the catalog's undo
  operation (C-v0.6 OP-C10): its own origin, its own relied-on basis and
  basis check, its own treatment — governed by the policy record of the
  operation whose receipt it reverses (R3-4, INTEGRATION) — its own outcome and its own receipt.
- Its applied outcome carries the relation **reverses ⟨receipt⟩**, naming the
  reversed change's receipt; the run record additionally links the reversed
  entry. It may equally be *refused*, meet an *application error* or be
  *outcome unknown*.
- **Acts and undo.** An undo erases no act record. An A5/A10 on the reversed
  change item keeps its binding and is **not lapsed** by the undo, because its
  item content is unchanged. Acts bound to subject content that the undo
  changes (e.g. an A4 on the applied row) **lapse under the ordinary rule**
  (V4-HI-32; DEL-04-03 L-6) — fixture T16a/T17.
- The reversed item's standing shows "applied, then reversed by ⟨receipt⟩".
  Undo route availability, scope and mechanism are host-owned (U-P8).
- **SWBPIPE session undo (SQ-10; R8-5).** SWBPIPE's undo is a session stack
  of whole-model snapshots. It is not an operation through the route, writes
  no receipt, does not reference the reversed change and is not governed by
  operation policy. R2-15 and R3-4 stand as App meaning. For SWBPIPE,
  "reverses ⟨receipt⟩" is *not supplied*, and a lapse an undo causes is
  shown from the identity change (R8-4; C §5.3).
- **Undo and holds (R5-5) — governance phase for re-hold (R8-11 item 1).**
  *Phase 1:* a lapse caused by an undo, including the person's own undo, is
  recorded like any other lapse (V4-REC-05; EXEC PH-8), and nothing
  re-holds. *Governance phase:* such a lapse re-holds a governed checkpoint
  like any other lapse (DEL-02-03 RH-8). In both phases the person's undo is
  never recorded as "action during hold" or "continued past ‹checkpoint›",
  and an undo never re-holds an A5 arrival (A5 binds to the unchanged item
  content).

## 5. Stale refusal, re-draft and retry (REQ-006; SOW-173; R2-13)

- **Precedence (R2-13, INTEGRATION; unchanged by R8-3).** On any submission
  the host first **de-duplicates by proposal identity**. If the host already holds the
  identity (queued, decided, applied or refused), it returns that proposal's
  recorded per-item state or outcome; it does not re-validate, and a
  resubmission is **never refused as stale because of its own effects**. Only
  a first receipt, and application of a not-yet-applied item, undergo the
  basis check. SWBPIPE DRAFT #885 runs its key lookup before the basis
  check, so a retry recovers its ticket even after its own commit; the same
  key with different content returns `idempotency_conflict` (SQ-08 (b)).
- **Trigger (R2-13 as amended by R8-3; INTEGRATION).**
  - *Per item, where the host supplies subject identities.* A change item is
    stale when a **subject content identity of one of its relied-on
    targets** differs from the current one at the check (validation, queue,
    or application). A global revision advance alone does not stale an
    item; applying sibling items of the same proposal does not stale
    remaining items unless they share targets.
  - *Otherwise, the host's stated scope.* The App receives and shows the
    host's stated staleness scope and never narrows it or re-evaluates it
    per item. SWBPIPE's trigger is any model revision change: any commit
    (edit, apply, undo, redo, project open or create) stales every queued
    proposal, so one application makes every other queued item leave
    (SQ-07 (d), (f)). The engine additionally checks per-field
    before-values.
  - A generation change makes revision comparison impossible and is handled
    under U-C2. Host confirmation of the per-item rule and of
    subject-identity scope: U-C3.
- **Refusal content.** *refused — stale*; reason (what changed, where known);
  failing targets, or, on a host with a stated scope, that scope with
  "failing targets not supplied" (R8-3); **relied-on basis** (unchanged);
  **current basis** (evaluated basis); affected items. SWBPIPE's stale
  refusals are `OP-STALE-BEFORE-VALUE` and `OP-CLAIMED-MODEL-HASH-MISMATCH` on
  main, and `stale_basis` or `expired` in DRAFT #885 (SQ-09 (a)).
- **No silent refresh.** No host or consumer rewrites the relied-on basis and
  proceeds.
- **Re-draft.** Only as a **separately identified** proposal: new proposal
  identity, lineage to the stale one, a new relied-on basis and target
  identities from a new read, re-derived old values, new change-item content
  identities, fresh validation. No acceptance carries over.
- **Retry is not re-draft.** A retry resubmits the same proposal identity and
  content without a new read. If the host holds the identity, the recorded
  state is returned (precedence above). If the host never received the first
  submission, the retry is a first receipt and is checked like one.

## 6. No retargeting (REQ-007; SOW-174)

- Bound targets and affected objects are fixed at drafting from explicit
  target identification (C §4.3), including a person's selection resolved at
  drafting.
- A later selection change in any surface never changes a proposal's bound
  targets, items or reported affected objects. A change of intended target is
  a new proposal.

## 7. Repeated submission → one effect (REQ-008; SOW-175)

- **Obligation.** Submitting the same proposal identity more than once,
  including a retry after a lost acknowledgment, produces at most one
  application effect per item. This is a **host obligation to be evidenced**
  (DEP-001), not a recorded fact (R-7).
- **Precedence.** Identity-based de-duplication precedes the basis check
  (§5; R2-13).
- **Recording.** Each submission is recorded separately, referencing the same
  proposal identity, with only the effects actually observed (the same
  receipt, two receipts, or unknown) (R-7).
- **Testable form.** Effect count observed in the host model/receipts for the
  proposal identity equals 0 or 1 per item; a repeat reports the existing
  state (queued, applied with the *same* receipt, etc.).
- **Mechanism unselected** (TBD-002). Shared validation or transport
  deduplication is not evidence of a one-domain-effect outcome (V4-EXM-25).
- **Unobservable repeat.** Report *outcome unknown* (observer-attributed); do
  not infer one effect or zero.
- A re-draft is a different proposal and not a repeat.

## 8. Host proposal-view information (REQ-009; SOW-176)

The host shows, in its own tables/views (V4-HI-24; V4-HOST-04: no
agent-private surface), for each proposal and item:

| Information | Supplied by this contract | Presented by |
|---|---|---|
| Old value (as of relied-on basis) | §3.4 | Host |
| New value | §3.4 | Host |
| Affected objects; which items a view row presents | §3.4; §3.1 rule 4 | Host |
| Why (reason) | §3.3 / §3.4 | Host |
| Origin (author, seat role, conversation, workflow identity and run) | §3.3 | Host |
| Current disposition per item, with actor for A5/A10/A11, and per-item annotations (e.g. accepted — not applied: refused — stale) | §4 | Host |
| Stale indication with current value where it differs; failing targets | §5 | Host |
| Lineage for a re-draft | §3.1 | Host |
| Item-left events | §4.3 | Host |

Presentation, receipts and the acceptance control are host-owned
(DEP-03-02-024). The control says "accept", never "approve" (S-P9). A live UI
witness is host-owned evidence.

## 9. Canonical outcome taxonomy (R-7; REQ-005, REQ-010, REQ-011; SOW-172, SOW-177, SOW-178)

Every non-success outcome carries the **evaluated basis** where the host
evaluated one. Outcomes apply per change item where items exist. Reporter
rules for non-success results follow C-v0.6 §4.1.

| Outcome | Meaning | Carries | Establishes | Does **not** establish |
|---|---|---|---|---|
| unavailable | Catalog precondition failed (C §4.1, §4.4) | Reason, failed precondition, evaluated basis | Nothing executed | — |
| not permitted | Treatment forbids the requested mode (R-3; R2-12) | Governing treatment (policy record or checkpoint constraint), evaluated basis; A8 request *offered* for reserved acts | Nothing executed | — |
| channel not enabled | External access off (V4-HI-52); A13 not performed | Channel state | Nothing evaluated | — |
| not exposed on this surface | Host-reported: entry not exposed on the acting surface (C §3 #9); relayed by loop/adapter | Entry, surface | Nothing evaluated | — |
| refused — invalid | Host validation refused with a catalog error | Error identity, evaluated basis | Nothing applied | — |
| refused — stale | A relied-on target no longer holds | Reason, failing targets, relied-on basis, current (evaluated) basis | Nothing applied | — |
| queued | Host holds the item for the person's decision | Host acknowledgment | Submission received | Acceptance, application |
| accepted | Host captured the person's A5 on the item | Actor, act reference, item content identity | That act by that person on that item content | Application, checking, approval, reliance |
| rejected | Host captured the person's A10 | Actor, act reference | That rejection | — |
| withdrawn | Proposer withdrew (A11) | Actor | That withdrawal | — |
| applied (receipt) | Host applied the item. **Applied-outcome association**: proposal/item identity, relied-on basis, receipt reference, resulting revision, **resulting objects** (created and changed object identities with their post-application subject content identities and method designation, or "not supplied" as an evidence limit, R2-14; SWBPIPE supplies `target_ref`, per-field diffs and the new whole-model hash, with created objects only as the target ids of `create_*` operations and no post-application per-object identity, SQ-03 (d), R8-4); branch *after acceptance* or *direct under grant* (with settings references); relation *reverses ⟨receipt⟩* for an undo | Association | Execution, resulting revision and the reported resulting objects | Acceptance (direct branch), checking, approval, reliance |
| applied, then reversed by ⟨receipt⟩ | Standing of an applied item whose change was later reversed (§4.5) | Both receipts | Both executions | That any act on it lapsed or survived — evaluated per act (§4.5) |
| application error | Declared error during application | Error identity; effect *none* / *partial* (receipt references) / *unknown* | What the effect statement states | Any unstated effect |
| outcome unknown | Result unobservable | Observer, last observed state | Only the last observed state | Applied, failed, accepted or rejected |
| error (read/examination/host check) | Declared error in a non-mutating operation (C §4.1) | Error identity, evaluated basis | — | — |
| success (operation) | The operation ran (S-P7) | Result | Execution | Any human act |

Item-left events (§4.3) accompany the refusal/withdrawal outcomes of queued
items. Whether the host receipt *itself* carries the relied-on basis or the
resulting objects is a host observation recorded at comparison (C-v0.6
VC-C-04), not assumed.

### 9.1 Received host vocabulary: SWBPIPE (R8-5; evidence only)

SWBPIPE's terms are received as follows. The first rows are **INTEGRATION
(R8-5)**. The rest are SWBPIPE's own mapping (SQ-09 (a)), received as the
host states it. Main terms are FACT; #885 terms are DRAFT #885 (unmerged,
deferred). Nothing here is a SWBPIPE commitment (DECISION-3).

| SWBPIPE term | App term | Condition |
|---|---|---|
| `unsupported_method` / `unsupported_change` | host-reported **not exposed on this surface** | Never *not permitted*. R2-4 (a named rule) is recorded as not met by this host (R8-5) |
| #885 `withdrawn` / `cleared_in_review` (the person cleared the queue) | **item left**, "cleared by the person, no decision record" (§4.2, §4.3) | Never A10, never A11 (R8-5) |
| #885 `rejected: validation_rejected` at Apply | **refused — invalid** at application | Never A10 (R8-5) |
| Apply (the person's review-and-apply) | **accepted** and **applied (receipt)** in one step, per batch | No separate *accepted* state and no A10 record; the missing counterparts are recorded (R8-5) |
| Session undo | — | Writes no receipt; "reverses ⟨receipt⟩" is *not supplied* (R8-5; §4.5) |
| `controller_unavailable`, or an attachment failure | *endpoint unavailable* (DEL-03-03), channel *disabled* | Never host-reported *channel not enabled*; SWBPIPE has no such code (R8-6) |
| main `blocked`; #885 `invalid_request` | *refused — invalid* | Before queueing, nothing is queued (SQ-09 (d)) |
| main `OP-STALE-BEFORE-VALUE`, `OP-CLAIMED-MODEL-HASH-MISMATCH`; #885 `stale_basis`, `expired` | *refused — stale* | Host scope: whole model (§5; R8-3) |
| #885 `queued` | *queued* | Only after the controller observes publication |
| main `applied_to_session_model`; #885 `committed` | *applied (receipt)* | Main's receipt is session-only; #885's is readable by `status` within one controller session (SQ-01, SQ-08 (c)) |
| #885 `outcome_unknown` | *outcome unknown* | Reporter host; a later `status` read is reported separately |
| #885 `busy`, `capacity`, `not_ready`, `unauthorized`, `wrong_app`, `wrong_workspace`, `internal_error`, others | as the host states each (*unavailable*, *not permitted* or *error*) | `retryable` and `next_action` are recorded, never acted on as a treatment |

## 10. Execution versus human acts (REQ-010, REQ-012; SOW-177; #d3)

Canonical act names (R-1; DEL-04-01 §2.1).

| Subject | Actor | Evidence required | Never inferred from |
|---|---|---|---|
| A1 propose (draft/submit) | Agent or person | Proposal content; host queue acknowledgment | — |
| A2 apply (validation/application) | Host route on the actor's request | Validation outcome; receipt | — |
| Direct application under grant | Agent within an effective direct treatment and no governing constraint | Receipt, origin mark, settings references | — and it implies no A5 |
| A3 examine | Agent | Findings by reference | — and it is never A4 or a host check |
| A4 mark checked (reserved) | The person | Host-captured act bound to subject content identity | Findings, success, acceptance |
| A5 accept (reserved where a proposal is required) | The person | Host-captured act bound to change-item content identity | Success, submit, queue, application, agent report |
| A10 reject (reserved wherever A5 is) | The person | Host-captured act | Absence of acceptance; host refusal |
| A11 withdraw | The proposer | Host record | — |
| A6 approve (reserved) | The person/accountable professional | Its own record | A5 (S-P9) |
| A7 rely (reserved) | Accountable professional | Its own record | Any of the above |
| A8 request | Agent | Request record, only when actually issued | — it establishes nothing; a failed call is not an A8 |
| A9 record (faithful recording) | Recorder ≠ decision actor | Reference to the capturing surface's evidence of the act | — it never satisfies a checkpoint by itself (R-5); never made through a reserved act-performing operation (R2-2) |
| A12 set grant (reserved) | The person | Control act evidence, bound to the setting content (classes, grant values, scope); a later **established** A12 **supersedes** an earlier one (R2-7, PROPOSED) | Agent request (A8) |
| A13 enable / disable external access (reserved; disable INTEGRATION) | The person | Control act evidence. SWBPIPE has no enablement facility (SQ-28), and its launch environment variable is not a captured act (SQ-13), so no A13 is evidenced there; whether a person-set variable could count is deferred to the owner (R8-6) | Agent request (A8) |
| Act-declined event (A4, A6, A7, A12) | The person | Capture evidence of the decision not to act | — it is not the act and not A10 (R2-5) |
| Run-ended event | The person stopping the run, or an observed end; **reporter**: the loop (V2 m-11) | Run record | — the checkpoint stays *waiting* (R2-5). An ended run is never resumed; acts after the end are shown "after run end" and change nothing; continuation is a new run with **continues ⟨run⟩**, inheriting nothing (R4-4, PROPOSED). An interruption is not a run end |
| A14 answer tool permission | Person or the user's own Codex mode | App-side R13 record only (R2-8) | — never a professional act, A5 or a grant |

Rules: one act never establishes another; no synthetic prerequisite between
acts is introduced; checkpoint satisfaction requires attributable evidence
from the capturing surface — the host's act facility for acts on host content
(R-5). Whether a particular host exposes a capture-evidence reference is a
DEP-001 relay question (R2-20); SWBPIPE exposes none (SQ-01), and its
acceptance-record storage is SWBPIPE owner decision PB-TBD-002. Answers to Codex user-input or MCP
elicitation requests are **not act evidence** and never host act capture
(R4-12). An act counts toward a checkpoint only if captured at or after that
checkpoint's arrival; earlier acts are shown "prior act not counted" (R4-5,
PROPOSED). A refused or pending A12 supersedes nothing and does not count
(R4-6). A person's own A1/A2 are run-record (R7) operations, not human-act
records; an operation that performs a reserved act (OP-C6/C7/C8, the A12/A13
controls) produces the human-act record, and its R7 entry references it
(R5-6). Operation-specific reserved additions await `UNRESOLVED{OI-021}`.

## 11. M3-CP read-then-action comparison design (return to DEL-03-01)

This is the distinct return retained from SCC-CASE-004 (CASE-002 M3-CP;
DEP-03-01-026). It supplies DEL-03-01 with designed refusal/application
behavior and a comparison plan; DEL-03-01 compares basis elements only.
Steps are the FX-PIPE-01 timeline (C-v0.6 §10.3).

| Step | Action | Basis observed | Proposal reference | Expected P behavior |
|---|---|---|---|---|
| T3 | Agent reads supports table (OP-C1) | B1 = FX-W1/g1/r12/⟨v12⟩/⟨m-fx⟩ with ⟨S-1…S-4@r12⟩ | — | — |
| T5 | Agent drafts PR-1: item 1 add support (OP-C4; targets R-100, S-2, S-3); item 2 S-3 stiffness (OP-C5; target S-3) | — | PR-1 relies on B1 and target identities | drafted; items bound; change-item content identities include B1 |
| T6 | Engineer A edits S-3 (intervening edit) | r13 (same generation g1) | PR-1 still relies on B1 | — |
| T7 | Agent submits PR-1 | host evaluates B2 = …/g1/r13/⟨v13⟩ | B1 | first receipt → per-item check: both items **refused — stale** (⟨S-3⟩ changed): reason, failing target S-3, relied B1, current B2; item-left events for both |
| T9 | Agent re-reads; drafts PR-2 (lineage PR-1, stale) | B2 | PR-2 relies on B2 | new proposal identity; old values and target identities at r13; new item content identities |
| T10 | Submit PR-2 | B2 | B2 | validated → **queued** (not applied) |
| T11 | Engineer A accepts item 1 (A5), rejects item 2 (A10) | — | B2 | item 1 accepted (bound to its item content identity); item 2 rejected |
| T12 | Host applies item 1 | resulting r14 | B2 | **applied**: association PR-2 / item 1 / B2 / RC-1 / r14 / resulting objects S-5 created, R-100 changed; A5 not lapsed |
| T13 | Acknowledgment lost; agent retries PR-2 (same identity) | — | B2 | host de-duplicates **before** any basis check: returns recorded state (item 1 applied RC-1; item 2 rejected); second submission recorded separately; no stale refusal from its own effect. If unobservable: **outcome unknown** (observer: loop), last observed *accepted* |

**Comparison DEL-03-01 performs (C VC-C-04):** for each basis element and the
method designation, compare the value at read (T3, T9), in the proposal
reference (T5, T9), in the refusal (T7: relied and current), and in the
applied-outcome association (T12). Expected: PR-1's reference equals B1 at
every step; the refusal shows B1 and B2 distinctly; PR-2 references B2 only;
the association references B2, r14 and the resulting objects; T13 returns
recorded state; no step rewrites a reference; whether RC-1 itself carries B2
is recorded as a host observation. T7's per-item refusal is the fixture's; on
a host with a whole-model scope, such as SWBPIPE, the refusal names the host
scope and no failing target (§5; R8-3).

**Evidence labels:** per the C-v0.6 mapping — *illustrative* (this table),
*test-double*, *actual host* (candidate-bound SWBPIPE observation, DEL-09-09).
The first executable return is a candidate-bound test-double observation; it
is not host evidence (V1-B X-08).

## 12. Receiving risks from SWBPIPE source limits (HI §11, `e548d4cf`)

Recorded as risks for receiving and the joined witness, not host assignments.
SWBPIPE's answers (2026-09-28) update them as noted; they are answers about
its current state, not commitments. DRAFT PR #885 is open, unmerged and
**deferred** to UI-SUCCESSOR, with the owner's live-controller activation
still in force; the work graph's deferral governs over the PR description
(ANS §0 A-2, §3 item 11; R8-7):

| Observed limit | Risk to this contract | Where checked |
|---|---|---|
| Queue-time basis differs from original external inspection basis | Stale check against a queue-time basis would silently substitute a later basis (violates §3.2, §5). SWBPIPE (SQ-07 (c)): true of main's offline intake; DRAFT #885 freezes the inspected basis at preview and keeps it at submit, which would retire the risk if merged and qualified | DEL-09-09 VER-004; VC-P-04/07 against actual host |
| No durable exactly-once domain outcome established; runtime transport is not a joined live mutation path | §7 one-effect and §5 precedence not evidenced by transport dedup or shared validation. SWBPIPE (SQ-08 (c)): DRAFT #885's associations live only in the running controller; a restart expires handles or yields `outcome_unknown`; durable de-duplication is a SWBPIPE owner decision (durable receipt carrier) | DEL-09-09 VER-008; VC-P-09 |
| Stronger frozen-review checks not assumed for every route | Validation parity (§2) may differ by route | VC-P-02 against actual host |
| Workflow resolution ≠ provider adoption | Origin's workflow identity may not reflect adopted behavior | DEL-04-03 record comparison |

Later mainline or external-session changes need a targeted applicability
check before reliance (HI §11).

## 13. Interfaces provided and expected

| Direction | Counterpart | Content |
|---|---|---|
| Expect from | DEL-03-01/C-v0.6 | §3.2 elements; §3.1 five class values; §4.1 results and reporters; §4.4; content identities and method designation; "no longer holds" rule (per item, or the host's stated scope, R8-3); whole-model identity receiving (R8-4); exposure; FX-PIPE-01 incl. OP-C10 undo |
| Expect from | DEL-04-01 | A1–A14 names; class records P-01…P-06 with revision identity; treatment → outcome map; act-declined event; residual `UNRESOLVED{OI-021}` additions |
| Expect from | DEL-04-02 | Grant display states incl. *effective (policy default)*; grant value and scope per class; settings version identities |
| Expect from | DEL-02-01 | Workflow identity; checkpoint declarations (required act, subject class, reached-when); §4.3.7 item rule |
| Expect from | Host owner | Route, de-duplication, treatment resolution, constraint receipt (U-P10), validation outcomes, receipts, resulting objects, origin marks, undo route, views, captured acts with capture-evidence references, settings version at application, stale rule confirmation (U-C3), generation meaning (U-C2), one-effect evidence |
| Provide to | DEL-04-02 | Direct-branch entry condition and origin semantics (§4.4); standing per outcome (§9) incl. "applied, then reversed" and accepted-then-stale display |
| Provide to | DEL-04-03 | Canonical §9 taxonomy; per-submission recording and precedence (§5, §7); applied association with resulting objects; change-item content identity for A5/A10 lapse (L-1); origin and constraint (§3.3); act/evidence table (§10); undo relation *reverses ⟨receipt⟩* (§4.5); item-left events (§4.3) |
| Provide to | DEL-03-03 | This contract unchanged for the external channel; constraint carriage assurance (§3.3, governance phase; only host-held satisfies R2-12; App-assured not available in this increment); *unverified* author identity; *channel not enabled* (App or host reporter), relayed *not exposed*, *not permitted*; the received SWBPIPE vocabulary (§9.1) |
| Provide to | DEL-05-01 | §9 unchanged; observer-attributed *outcome unknown*; retry keeps identity and precedence; origin, seat role, grant in force and constraint on every dispatch; sibling-draft rule (§3.1 rule 5) |
| Provide to | DEL-05-02 | Per-item dispositions with actors and annotations, lineage, stale indication, item-left events, "accept" wording (§8) |
| Provide to | DEL-02-01 / DEL-02-03 | Governing constraint semantics and *not permitted* outcome (§4.4; governance phase); per-item dispositions, item-left events and all-items-decided indication (§4.3); resulting objects for subject binding (§9) |
| Provide to | DEL-03-04 | §1 authority map and this table |
| Provide to | DEL-09-09 | §11 scenario, §12 risks, VC-P cases and expected outcomes |
| Provide to | DEL-03-01 | M3-CP return (§11) |
| Provide to | Host proposal views | §8 information |

## 14. Examples (FX-PIPE-01 fixture subjects)

All material is **invented** and taken from the shared catalogue (C-v0.6
§10), except the rows marked SWBPIPE, which use SWBPIPE's answered terms. Labels are fixture labels, not identities, wire names or SWBPIPE
commitments.

**E-1 PR-2 in the host view after T10:**

| Row | Item | Object | Attribute | Old (at r13) | New | Why | Origin | Disposition |
|---|---|---|---|---|---|---|---|---|
| new support | 1 | new support on R-100 at 4.2 m (targets R-100, S-2, S-3) | created | — | guide support | Span S-2→S-3 exceeds 6 m (T4 findings; T4a host check failed: support spacing) | agent seat (role: host agent), conversation K-7, workflow {workflow, host, ⟨fx-root⟩, supports-adjust, ⟨rev-3⟩} run 12 | queued |
| S-3 | 2 | S-3 | stiffness | value at r13 (Engineer A's T6 edit) | 2.0e6 N/m | Reduce thermal restraint | same | queued |

**E-2 Truthful reports:**

| Situation | Correct report | Incorrect report |
|---|---|---|
| T10 submit succeeded | "PR-2 queued (2 items); awaiting your decision" | "PR-2 applied" / "accepted" |
| After T11, before T12 | "Item 1 accepted by Engineer A, not yet applied; item 2 rejected by Engineer A" | "Item 1 applied"; "item 2 refused" |
| T12 | "Item 1 applied, receipt RC-1, now r14; created support S-5" | "Item 1 approved" |
| T13 retry answered | "PR-2 already processed: item 1 applied (RC-1); item 2 rejected" | "PR-2 refused — stale" |
| T16 direct application of OP-C9 under ⟨set-2⟩ | "Applied under your grant (settings ⟨set-2⟩); origin-marked; undo available" | "Accepted" |
| T13 not observable | "Outcome unknown (observed by loop); last observed: accepted" | "Applied" or "failed" |
| OP-C4 requested directly at r13 under ⟨set-1⟩ | "Not permitted: add support requires a proposal under your current settings (policy default: propose)" | Silent conversion to a proposal; "unavailable" |
| V-CP1, Phase 1 (R8-1; R8-11 item 2): the agent follows CP-accept as plan guidance | "Add support proposed (queued, 1 item); checkpoint CP-accept in run 12 expects your acceptance". A direct request, if made anyway, is reported as the host's own outcome | "Not permitted: checkpoint CP-accept…" (no constraint is carried or enforced in Phase 1); "Accepted" |
| V-CP1, governance phase (CP-accept governed; host-held constraint): OP-C4 requested directly under a direct grant while CP-accept (run 12, A5) applies | "Not permitted: checkpoint CP-accept in run 12 requires your acceptance of this change; it must be proposed" — the agent may then submit a proposal, which queues and becomes CP-accept's subject | "Drafted as a proposal"; "Applied; checkpoint waiting" |
| V-S1 | "Item 1 accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)" | "Item 1 accepted" alone; "item 1 applied"; "acceptance lapsed" |
| V-NP1 proposal of OP-C11 | "Renumber nodes proposed (queued). This operation has no policy basis yet (pending OI-021); proposing grants nothing" | "Renumber nodes permitted" |
| T17 undo of RC-2 | "Label change RC-2 reversed by RC-3; your check mark on S-4 (T16a) has lapsed because S-4 changed" | "RC-2 deleted"; "check mark still current" |
| SWBPIPE: the person clears the queue (#885 `withdrawn`) | "The proposal left the queue: cleared by you in review; no decision was recorded" | "Rejected by you"; "Withdrawn by the agent" |
| SWBPIPE: a direct external request (`unsupported_method`) | "Not exposed on this surface (host-reported: unsupported_method)" | "Not permitted"; "Proposal required by your grant" |
| SWBPIPE: the person's Apply fails validation (#885 `rejected: validation_rejected`) | "Refused — invalid at application: ‹host code›" | "Rejected by you" |

## Changes from v0.5

v0.5 = P-v0.5 (last changed at `375c3970c`; unchanged at `94aa9181b`; sha256
6ab94fd10166cf78cda014a2f28ebf4726ce9f82a1c2f180044093b4bbb137e0). Keyed by R8
ID. Sources are I2 rows of INTAKE_MAP.md (`nn.k`, Part 2.2, Part 3/4 items);
R8 overrides I2 where they differ.

| R8 ID (I2 source) | Change in v0.6 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1) | Phase framing added. The governing checkpoint constraint, its carriage assurance, the treatment it forces and hold support are relabelled **governance phase (retained)**, with a Phase-1 statement beside each: no constraint carried by the App, no hold, nothing *not permitted* on a checkpoint's account; the host's own treatment decides. V4-WF-05's first half recorded as phased, not withdrawn. §9's taxonomy is unchanged by phase | Header, §0, §1, §2, §3.3, §4.4, §13 |
| **R8-2** (02.7; Part 2.2 P rows) | §3.3 authority limit in two parts. Governance phase: SQ-02 answered 2026-09-28 with no host-held route (route (iv), none planned), so model-supplied-only carriage against SWBPIPE is **not enforceable** (HS-3 (c)) — this replaces "*not established* while SQ-02 is unanswered" for SWBPIPE; a later decision to plan a route is a revision trigger. §4.4 hold-support bullet gives SWBPIPE's governance-phase values, and D6 is recorded closed for Phase 1. V-CP1-family fixtures stay governance-phase AWAITING INPUT with the STD-2 annotation. U-P10 restated | §3.3, §4.4, UNRESOLVED U-P10 |
| **R8-3** (07.6; Part 3 items 2, 5) | §5 Trigger: R2-13 as amended — per item where the host supplies subject identities, otherwise the host's stated scope, never narrowed (SWBPIPE: whole model); de-duplication first unchanged and confirmed for DRAFT #885 (SQ-08 (b)). Refusal content admits "failing targets not supplied". §11 and §12 row 1 annotated | §5, §11, §12, §13, UNRESOLVED |
| **R8-4** (03.3; Part 4.3) | Applied-outcome association: SWBPIPE supplies target ids, diffs and the new whole-model hash; resulting objects beyond target ids *not supplied*. Undo lapse shown from the identity change | §4.5, §9, U-P2 |
| **R8-5** (01.6, 05.4, 09.2, 09.3, 10.1; Part 3 items 1, 10; Part 4.9) | Outcome mapping: new §9.1 received-vocabulary table; `unsupported_method`/`unsupported_change` → host-reported *not exposed on this surface*, never *not permitted*, R2-4 recorded as not met (§2); #885 `withdrawn` → item left, "cleared by the person, no decision record", with a new item-left cause and §4.2 row; `validation_rejected` → *refused — invalid* at application (new §4.2 row); neither is A10 or A11. Accept-and-apply per batch with no A10 record, and accepted-then-stale not arising, recorded (§4.2, §4.3). Session undo writes no receipt: "reverses ⟨receipt⟩" *not supplied* (§4.5). E-2 gains three SWBPIPE rows | §2, §4.1–§4.5, §9, §9.1, §14 |
| **R8-6** (Part 3 item 4) | §10 A13 row: SWBPIPE has no enablement facility; the launch environment variable is not a captured act; R8-Q4b deferred to the owner. §9.1: `controller_unavailable` → *endpoint unavailable*, channel *disabled* | §9.1, §10 |
| R8-7 (Part 3 items 11, 12; Part 4.11) | Answered standings: SWBPIPE answers recorded in U-P1…U-P8 and U-C2/U-C3/U-C4 effects; U-P1's durable de-duplication and U-P2's capture-evidence storage point to SWBPIPE owner decisions. PR #885 recorded as deferred with the owner's activation in force (§12). "App v4 OI-003" qualified | §0, §10, §12, UNRESOLVED |
| **R8-10** (02.7; Part 5 R8-Q12) | Strict preflight: the agent never adds fields the host schema lacks (SWBPIPE refuses unknown fields, SQ-02 (a), SQ-31). I2 R8-Q12's evidence limit "constraint not carriable on this host" carried as PROPOSED | §3.3 |
| R8-11 (items 1, 2, 5) | S-P13: D2's reserved-act half binds in Phase 1 (host-enforced); its declared-checkpoint half, WD I-7 and V4-HI-42 are Phase-1 guidance. Lapse recording continues in Phase 1 and re-hold is governance phase (§4.3, §4.5). Governance-phase values read the fixture's checkpoints as if declared governed (§0) | S-P13, §0, §4.3, §4.4, §4.5 |
| R8-7 (14.1, 14.2) | §3.3 author identity: SWBPIPE records identity as not verified (SQ-14). SWBPIPE records neither conversation nor workflow run, so the App records them App-side and links by request id | §3.3 |
| **R8-12** (item 7; closing pass, node A6, in place) | Consumed inputs list the post-R8 sibling versions; §0's reference to C §4.1 names C-v0.6 (the list is carried unchanged) | Header, §0 |

Identifiers: new subsection **§9.1**; new item-left cause "cleared by the person, no decision record"; two new §4.2 rows; four new E-2 rows. No identifier removed. C references re-pointed from C-v0.5 to C-v0.6 where C is consumed (the fixture itself is unchanged).

## Changes from v0.4

v0.4 = P-v0.4 (committed; unchanged at `8fb51f07f`).

| R5 / V3 item | Change |
|---|---|
| **R5-2** (V3-B MAJOR-1, Y-1, Y-8) | §3.3 carriage assurance redefined: host-held includes the host loop's own evaluation and received-then-verified constraints; received-only keeps its source's assurance; App-assured not available in this increment (R4-2); only host-held satisfies R2-12. Host loop removed from App-assured. §2, §4.4, §13, U-P10, VC-P-04 aligned |
| **R5-1** (V3-B m-3) | §4.4 hold statements qualified "where hold support allows"; four hold-support values; App-only/App-run holds `UNRESOLVED{D6}` |
| **R5-5** | §4.5 undo and holds: undo lapse re-holds; the person's undo is never "action during hold"; never re-holds an A5 arrival |
| **R5-6** | §10 rules: person's own A1/A2 are R7 operations; reserved-act operations produce the human-act record referenced by R7 |
| **R5-9** (V3-B m-2, Y-7) | §4.3 and §1 "confirms at W7" → confirmed by DEL-02-03; UNRESOLVED mixed-item row closed; C citations → C-v0.5; header states EXEC/ADAPTER/XT v0.2 not read |
| R5-4 | Not applicable: P states no destination text |
| R6-1, R6-5 (V4-B m-2 context; in place, no version bump; R6_RESOLUTIONS sha256 8703e85a…b841) | §3.3 authority limit: model-supplied-only carriage gives *not established* while SQ-02 is unanswered, *not enforceable* only after SQ-02 is answered with no host-held route; §4.4 hold-support values assigned by held actions |
| R6-2, R6-4 | No P text affected; no stale markers found |

## Changes from v0.3

v0.3 = P-v0.3 (committed; unchanged at `f05c7e4cd`).

| R4 / source item | Change |
|---|---|
| **R4-14** (ADAPTER F-1) | §3.3 new element **constraint carriage assurance** {App-assured, host-held, model-supplied, absent}; model-supplied alone does not satisfy R2-12; §2, §1, §13, VC-P-04 and U-P10 no longer say "the external adapter carries" |
| **R4-15** (ADAPTER F-8) | §3.3 author identity may be **unverified**; RS R11 evidence limit named |
| R4-3, R4-7 (EXEC §4.7, F-1) | §4.3 cites DEL-02-03's confirmation with MX-3/MX-6/MX-8; A5 never re-holds |
| R4-4 (EXEC F-4) | §10 run-ended row: no resumption of an ended run; *continues ⟨run⟩* |
| R4-5, R4-6 (EXEC F-3, F-5) | §10 rules: capture after arrival; A12 supersedes only when established |
| R4-12 (EXEC F-9; ADAPTER F-3) | §10 rules: elicitation/user-input answers are not act evidence |
| **R4-19** / V2 m-3 | §4.5 and U-P8 cite **R3-4**; U-P8 narrowed to mechanism and availability |
| R4-19 / V2 m-9 | R3 and R4 hashes added to the header |
| R4-19 / V2 m-11 | Run-ended actor = the person or an observed end; reporter = the loop |
| R4-19 / V2 m-12 | Nothing in P to close |
| V2 §3 ("conversation K-7") | K-7 now declared in C-v0.4 §10.1 |
| C-v0.4 | References to C re-pointed from v0.3 to v0.4 (IDs unchanged; FXA-n rename does not affect P) |

## Changes from v0.2

v0.2 = P-v0.2 (sha256 942c1a3a…8c89, 575 lines, committed at `c387730fb`).

| R2 / IR1 item | Change |
|---|---|
| R2-1, R2-9; IR1-A IR1A-01; IR1-B B-M1 | "policy basis pending" → **no policy basis** (C §3.1 five values); proposing confers no permission; §2, §4.4, E-2 V-NP1 |
| R2-2 | §10 A9 row: never through a reserved act-performing operation |
| R2-3, R2-11; IR1A-16 | S-P14/S-P15 credit D2/D3 only with their text; disabling A13 INTEGRATION |
| R2-4; IR1A-10 | §2 A8 *offered*, not auto-recorded; §9 *not exposed* host-reported and relayed |
| R2-5; IR1A-03 | "declined the item" → A10 "rejected"; §10 act-declined and run-ended events |
| R2-6 | §3.3 *effective (policy default)* state and default-basis settings reference; §4.4 default opens direct only if the record's default is direct |
| R2-7 | §10 A12 binds to setting content; supersession |
| R2-8 | S-P15, §10 A14 recorded only in R13 |
| **R2-12**; IR1-B B-M2, B-M3, X-9; IR1-C IR1C-03 | §3.3 **governing checkpoint constraint** element {run, checkpoint, A5, operation}, carried by loop and external adapter; authority limit and relay question (U-P10); §4.4 and E-2 reworded: direct request → *not permitted* naming the constraint, never "drafted as a proposal" |
| **R2-13**; IR1-B B-M7 | §5/§7 precedence: identity-based de-duplication before basis check; per-item check on relied-on target subject identities; sibling applications do not stale unless shared targets; §3.4 relied-on targets; T13 corrected in §11 and E-2 |
| **R2-14**; IR1-B B-M6 | §9 applied association adds resulting objects; §3.4 creation affected object; E-2 T12 |
| **R2-15**; IR1-A IR1A-06; IR1-B X-5 | §4.5 reworded: relation *reverses ⟨receipt⟩*; A5/A10 on reversed item not lapsed; acts on changed subject content lapse normally; OP-C10; §9 "applied, then reversed" standing |
| **R2-16**; IR1-B X-8, B-m2, B-m13 | §4.2 accepted-then-stale display wording; U-P3 narrowed to host evidence; V-S1 |
| **R2-18**; IR1-C X-14 | §4.3 **item-left events**; all-items-decided; "partial" annotation; WD §4.3.7 cited as the rule; performed A5 checkpoint after stale refusal |
| R2-17 | §4.4 proposal items become the checkpoint subject via reached-when kind (c) |
| R2-20 | §10 capture-evidence reference relay |
| R2-21 | Fixtures re-pointed to C-v0.3 §10 incl. T4a, T16a, variants V-CP1, V-S1, V-NP1 |
| IR1-A IR1A-14 | "grant value" used for direct/propose of a grant; "treatment" for route resolution |
| IR1-B B-m7; IR1-C IR1C-16 | §3.1 rule 5 aligned with LOOP MC-8 |
| IR1-B B-m4, B-m8 | Naming confirmed ("refused — stale", "observer"; seat role separate) — no change needed |
| Commit read rule | Sibling v0.2 texts read from `28bd00499`; hashes in header |
| Coordinator R2 notes (DEL-04-02/03 aligner items) | §5 retry text no longer says a retry is refused stale like any submission (identity de-dup first, R2-13); §4.4 entry condition reads "effective (person-set) direct, or effective (policy default) whose policy-record default is direct" (R2-6) |

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-021}` operation-specific reserved additions; first connected operation, autonomy, environment | Owner via outside SWB session and App/shared owner | Before connected SoW/execution | Classes for connected operations may gain reserved additions; OP-C11 stays *no policy basis*; §11/§14 invented only |
| Host adoption and enforcement of D2, D3 and R2 treatments | Host owner / SWBPIPE (DEP-001) | Before host conformance | All treatment and act behavior is receiving meaning. SWBPIPE (SQ-05): no class system, no grants, no named reserved list; every change waits for the person's Apply; autonomy is SWBPIPE owner decision OI-016 |
| `UNRESOLVED{OI-003}` (App v4 OI-003; unrelated to SWBPIPE's OI-003) extension promise | Owner with host contract owner | Before extension claim | Not decided here; route parity (§2) required regardless |
| `UNRESOLVED{OI-014}` shared contract/component placement | App/shared contract owners (DEP-03-02-025) | Before structural/production allocation | No placement implied |
| U-P1 Proposal identity and change-item content identity representation, encoding, de-duplication enforcement, outcome-recovery mechanics (TBD-002) | Relevant contract and host owners (DEP-03-02-026); durable de-duplication across restart: SWBPIPE owner decision (durable receipt carrier; ANS §2) | Before dependent implementation | §3.1, §5, §7 obligations testable; mechanisms open. SWBPIPE DRAFT #885: caller-supplied `idempotency_key`, controller `preview_ref` and `ticket`; key lookup before the basis check; not durable across restart (SQ-08) |
| U-P2 Actual host route, views, receipts, resulting-object reporting, act capture and capture-evidence references, settings version at application | Host owner / SWBPIPE (DEP-03-02-023) | When integration/witness relies on them | Settings reference at application *unconfirmed* until host-reported; resulting objects may be "not supplied". SWBPIPE: target ids and diffs only (SQ-03 (d)); no capture-evidence reference, and acceptance-record storage is SWBPIPE owner decision PB-TBD-002 (SQ-01) |
| U-P3 (narrowed) Host evidence that application re-checks relied-on targets after acceptance | Host owner (DEP-001) | Before application-path conformance | Contract rule fixed (R-6, R2-16). SWBPIPE: Apply re-runs full engine validation against the claimed hash (SQ-07 (e)); as Apply is the acceptance, accepted-then-stale does not arise there (R8-5) |
| U-P4 Validation failure before queueing: state treatment | Host owner | Before adapter implementation | PROPOSED: refused, stays drafted; confirmed by SWBPIPE (SQ-09 (d)) |
| U-P5 Host refusal at application: whether the host distinguishes it from validation refusal in its records | Host owner | Before outcome recording | Refusals never recorded as A10. SWBPIPE DRAFT #885 distinguishes `validation_rejected` at Apply (SQ-09 (e)), received as *refused — invalid* at application (R8-5) |
| U-P6 Operation-specific withdraw/reject rules beyond R-1 | Host owner (V4-HI-30); OI-021 for the connected operation | Before withdrawal implementation | A11 proposer-only; A10 reserved wherever A5 is. SWBPIPE: no withdraw or reject operation; #885 `withdrawn` is the person clearing the queue, received as item left (R8-5); SWBPIPE autonomy is owner decision OI-016 |
| U-P7 Item application grouping | Host owner | Before application-path implementation | Item-level dispositions defined. SWBPIPE: one batch is one application and one undo checkpoint; atomic (SQ-09 (b), (f)) |
| U-P8 Undo mechanism and availability (OP-C10). Treatment is settled: governed by the policy record of the operation whose receipt it reverses (R3-4, INTEGRATION) | Host owner | Before undo implementation | §4.5 semantics; treatment per R3-4. SWBPIPE: session snapshot undo, not through the route, no receipt, not policy-governed; "reverses ⟨receipt⟩" *not supplied*; acts bound to content it changes still lapse, observed from the model identity (SQ-10; R8-5) |
| U-P9 Sibling-draft grouping mechanics (= LOOP T-OPEN-1) | DEL-05-01 with DEL-03-02 and host owner | Before FX-M8 / loop fixtures | §3.1 rule 5 PROPOSED |
| U-P10 Host receipt of the governing checkpoint constraint, or host evaluation of its own declaration copy (relay, R2-12; SWBPIPE SQ-02); which carriage assurances a host can distinguish (R4-14); only host-held satisfies R2-12 (R5-2) — governance phase (R8-1) | Host owner with DEL-03-02, DEL-05-01, DEL-03-03 (DEP-001). SWBPIPE answered SQ-02 on 2026-09-28: route (iv), none planned; planning one is a SWBPIPE owner decision (ANS §2). D6 is closed for Phase 1 and re-opens with the governance phase (R8-2) | Before the governance-phase V-CP1 / LOOP FX-C9 / PANEL PC-24 / WD VC-11 execution | Phase 1: none; the App carries no constraint (R8-10). Governance phase: those fixtures AWAITING INPUT — SQ-02 answered: no receipt, no host copy (not offered); host joins deferred (DECISION-3); omitted constraint indistinguishable from none |
| ~~Mixed item decisions → checkpoint disposition~~ **Closed**: WD §4.3.7 confirmed by DEL-02-03 (R4-7; R5-9) | — | — | P supplies item data and item-left events |
| U-C2 / U-C3 / U-C4 / U-C12 (shared with DEL-03-01) generation; host confirmation of the per-item stale rule and subject-identity scope; multi-read reliance; per-subject identity not met by SWBPIPE | Host owner with DEL-03-01/DEL-03-02; U-C12 SWBPIPE owner (PB-TBD-002 / DEL-16-03) | Before stale implementation | Contract rule fixed as INTEGRATION (R2-13 as amended by R8-3: the host's stated scope where no subject identities are supplied). SWBPIPE: whole-model identity and staleness only (SQ-03, SQ-07 (d)); new generation per published-project change (SQ-07 (b)); no multi-read reliance concept (SQ-07 (g)) |
| Register: DOWNSTREAM mirror of DEP-03-01-026; mirrors to DEL-05-01/05-02; UPSTREAM row from DEL-04-02; SatisfactionStatus TBD vs PENDING (V1-B RF-06/08/09; V1-C RF-2) | Register owner at closeout C1 | C1 | None on content |
| SoW text (AC-013, TBD-001) still calls OI-001/OI-002 open | Closeout C1 via owning route | C1 | This design applies DECISION-1; scope unchanged |

## Verification cases

Designed, **not run**. Evidence labels per the C-v0.6 mapping (*illustrative*
/ *test-double* / *actual host*, with LOOP and PANEL equivalents). Steps and
variants refer to FX-PIPE-01 (C-v0.6 §10.3–§10.4).

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-P-01 Coverage | Map §§1–13 to the twelve scope rows (SOW-070, 090, 091, 170–178), V4-HI-20–25, C-v0.6 elements, R-1–R-9 and R2-1–R2-21 | Every scope row covered; every representation choice named as open with owner; DERIVED/INTEGRATION/PROPOSED markings match R1/R2 | VER-001 |
| VC-P-02 Channel parity | Same OP-C4 proposal, arguments, basis, authority via person, embedded, external; plus invalid (E-location-occupied), stale, direct-without-grant and V-CP1 variants | One route identity; identical outcome/error meanings; direct-without-grant → *not permitted* on every channel naming the governing treatment, never converted; V-CP1 in the governance phase → *not permitted* naming the constraint, and in Phase 1 → the host's own treatment, reported as observed (R8-1) | VER-002 |
| VC-P-03 Host authority / no upgraded result | T10 with no A5 captured | Reported *queued*; never *accepted*; domain truth only in host | VER-003 |
| VC-P-04 Origin, constraint and basis preservation | Trace PR-2 from T9 to T12; V-CP1 dispatch | Author type, seat role, channel, conversation, full workflow identity and run, standing at drafting, both settings references, relied basis B2 and target identities identical at every step; governance phase: V-CP1 on E has host-held carriage (host loop evaluation), and a model-supplied-only V-CP1 variant via X is not relied on for treatment and is recorded as such; Phase 1: no constraint is carried by the App and no field the host schema lacks is added; no case is labeled App-assured; an external caller the host cannot verify shows author identity *unverified* | VER-004 |
| VC-P-05 Lifecycle branches + direct case | T10→T11→T12; item 2 rejected; a withdrawn proposal; T7 stale; T16 direct; a direct request under *unconfirmed* and under *effective (policy default)*; SWBPIPE-form variants (a queue cleared by the person; `validation_rejected` at Apply) | Each disposition with actor and evidence; applied carries association with resulting objects; T16 records no acceptance; unconfirmed / policy default (propose) → direct *not permitted*; a cleared queue → item left, "cleared by the person, no decision record"; `validation_rejected` → *refused — invalid* at application; neither is A10 or A11 (§9.1) | VER-005 |
| VC-P-06 Unknown outcomes | (a) V-OU1; (b) a submission whose application is not established; (c) application error with effect *unknown* | All report *outcome unknown*, attributed to the observer, with last observed state; no inferred success, failure or act | VER-006 |
| VC-P-07 Stale, re-draft, stale-after-accept | T5–T9; V-S1; a host-scope variant (whole model) | T7 per-item refusal with failing target S-3, B1, B2, item-left events (host-scope variant: the scope shown, "failing targets not supplied", never narrowed, R8-3); PR-2 new identity and lineage citing B2; V-S1 → *refused — stale* at application, A5 not lapsed, display per §4.2, no carry to re-draft | VER-007 |
| VC-P-08 No retargeting | Draft PR-2; person selects S-4; submit and inspect | Bound targets and affected objects remain R-100/S-2/S-3 | VER-008 |
| VC-P-09 One effect and precedence | T13 retry (same identity) at r14; variant with two host receipts observed; variant where the first submission never reached the host | T13 answered from recorded state, never stale from its own effect; each submission recorded separately; one effect → same RC-1; two receipts → both recorded (host obligation failed, not hidden); never-received first → treated as first receipt; no global exactly-once claim | VER-009 |
| VC-P-10 Host view info | Inspect E-1 against V4-HI-24 and §8 | Old, new, affected objects and targets, row/item mapping, reason, origin, per-item disposition and annotations, lineage, item-left events present; host named as producer | VER-010 |
| VC-P-11 Execution vs acts | T12 success; T16 direct; T17 undo with T16a; separately evidenced A4, A6, A7 cases; an act-declined event | Success asserts execution only; T17 lapses T16a's A4 but not T11's A5; declined event never recorded as the act; A9 records cite capturing-surface evidence; none inferred from another | VER-011 |
| VC-P-12 Queued/accepted/applied/unknown reporting | T10; after T11; T12; T13; V-S1 | queued; "accepted, not yet applied" with actor; applied with association; T13 recorded state; V-S1 "accepted — not applied: refused — stale" — compared against host records | VER-012 |
| VC-P-13 Policy interface | Review §§2, 3.3, 4.4, 9, 10 against CLM-004, #d3, D2/D3, R-2/R-3/R-5, R2-1–R2-12; V-NP1 | Routine tool permission (A14), direct application, A5 and other acts distinct; reserved acts per D2; constraint → not permitted; no policy basis → proposal confers nothing, A12 widening refused, dependent production *held*; no blanket approval policy | VER-013 |
| VC-P-14 Boundary audit | Check REQ-013 exclusions one-for-one against §1 and §13; run the registered boundary-owner checker when available | Each excluded act resolves to its owner; twelve scope rows retained; no sibling/external completion or SWBPIPE adoption claimed | VER-014 |
