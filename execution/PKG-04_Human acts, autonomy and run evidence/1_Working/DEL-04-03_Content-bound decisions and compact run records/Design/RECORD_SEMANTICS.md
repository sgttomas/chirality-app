# Record Semantics
- Contribution: DEL-04-03/RS-v0.3
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 and OUT-004 (definition content); OUT-002 and OUT-003 (behaviour and fixture design only — no writer, reader or fixture exists); REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; AC-001…AC-007 via designed VER-001…VER-006
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 74d42c38eaf2a6638b75bc5184f1741bc7d4f17171662a05a233d40f245340c1; `P/docs/PRD.md` §4.3 V4-EXE-01…03, §4.5 V4-AUT-01…05, §4.6 V4-PM-06, §4.7 V4-REC-01…05, §10; `P/docs/HOST_INTEGRATION.md` §1, V4-HI-04, V4-HI-11/12, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-52, V4-HI-70/71, §11; `P/docs/ARCHITECTURE.md` §4, V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-21/22/31; `P/docs/OPERATING_METHOD.md` V4-OPS-30…32; `DECISION_BRIEF.html` d2, d3; `OWNER_DIRECTIONS.md` J, O; `SCC-CASE-002/Case_Datasheet.md` M1, M2, M3, M3-CP; `_Decomposition/Open_Issues.csv` OI-001/002/013/014/021; `External_Dependencies.csv` DEP-001. Run folder `APP-V4-FIRST-INCREMENT-20260928`: `OWNER_DECISIONS.md` (DECISION-1; sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e); `R1_RESOLUTIONS.md` (2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4); `R2_RESOLUTIONS.md` (77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088); `reviews/IR1-A.md` (31b3c7f8493f05ee5fed6a11208f6811d2449d8a4fe72aae6300c2850b648284), `IR1-B.md` (70e4a4f6d88f475687a9fde56a566a6913081dd3dd560402c1db8996dffd2846), `IR1-C.md` (295e96b3f5871cdf4142df169dc8811cef0aa38e7a7eb1930b246f60f0a426b9); V1-A/B/C as cited in RS-v0.2
- Consumed inputs: DEL-04-03/RS-v0.2 (sha256 56a3f839f5133813d18fe630bcedf7b30cab8f72e815e9d174f87b0994e21c69, commit c387730fb). Sibling v0.2 text read from commit **28bd00499** (`git show`, not the working tree): DEL-03-01/C-v0.2 `CATALOG_AND_READ_BASIS.md` sha256 358182b18b1fe13f9af6e6f5a61c9ed57f91b6ab29ea0c9adab06fe0081d6d82 (§4.1, §5.3, §5.4, §6.2, §9, §10); DEL-03-02/P-v0.2 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` sha256 942c1a3ab5ad7bda865640067f0fd550d7cfd1acd8f6ee228f6906452adf8c89 (§3, §4, §5, §7, §9); DEL-04-01/ACT-POLICY-v0.2 `ACT_AND_POLICY_CONTRACT.md` sha256 e50f1fe2f5bb2e3280bc62175e5aeeaa4508eed713424d82c54536a9fb5993a9 (§2, §4, §5.4–§6, §8). Where R2 amends those v0.2 texts (R2-1…R2-21), the R2 ruling is applied and marked "per R2-n"; the amended sibling v0.3 text was not read. DEL-04-02/AS-v0.3 was aligned concurrently by the same executor; §8 here and its §6 are byte-identical.
- Receivers: CASE-002 M1 — DEL-02-01 (OUT-001/002; REQ-003; VER-003), DEL-02-03 (OUT-001/002; REQ-003; VER-003), DEL-04-02 (OUT-001/002; REQ-002/004; VER-002/004), DEL-05-01 (OUT-001/004; REQ-005/007; VER-008), DEL-05-02 (OUT-001/003; REQ-001/003; VER-001/003); DEL-01-04 and DEL-02-02 are outside this undertaking (D1). CASE-002 M3 — DEL-04-02 (OUT-001/003; REQ-002/004/005; VER-002/004/005). Dependencies.csv DEP-04-03-011…016 — PKG-02, PKG-03, PKG-06, DEL-04-02, DEL-09-11, external host run recording.

## Changes from v0.2

The v0.1 → v0.2 change table is preserved in RS-v0.2 at commit `c387730fb`.

| Item | Change in v0.3 |
|---|---|
| R2-1; IR1A-01 | Five class values incl. **no policy basis** with *reason* ∈ {omitted, unassigned, pending OI-021}, labelled INTEGRATION (§0, §6.1) |
| R2-2; IR1A-08 | Reserved operations are those that **perform** A4, A5, A6, A7, A10, A12 or A13; no faithful record is made through them; host faithful-record operation conditions (§6.2 HA-9) |
| R2-3; IR1A-16 | Disabling external access is recorded as A13, labelled INTEGRATION, not credited to D2e (§0) |
| R2-4; IR1A-02, IR1A-10 | Reserved entries always offered; agent call → *not permitted* with an A8 **offered** (an A8 exists only if issued); *not exposed on this surface* is host-reported and relayed; loop-side *not offered* entry (§5) |
| R2-5; IR1A-03, IR1A-18; IR1C-06, IR1C-08 | **Act-declined event** for A4, A6, A7 or A12 with capture evidence (§3); separate **run-ended event**; waiting checkpoint stays *waiting* at run end; post-end acts recorded without changing the ended run's disposition (R8) |
| R2-6; IR1A-05 | Display state **effective (policy default)**; settings-in slot for policy-class record and default; *not set* = no setting and no default (R6, §8) |
| R2-7; IR1A-04, IR1A-13 | A12 binds to **setting content** (classes, grant values, scope); established version / refusal is a relation; later A12 **supersedes**, never lapses (L-0); *superseded* added to state list; E7 fixed |
| R2-8; IR1A-19, X-3 | A14 only in R13; never R6, never a human-act record, never a grant; *not applicable* in host-loop runs; feed = DEL-01-01 observed facts in this undertaking. **U-10 closed**; feed hold is U-20 |
| R2-9 | No-policy-basis wording; A12 widening such a class refused; fixtures report **held** (§5, E9, VC-19) |
| R2-10 | Checkpoint act kind outside the closed list → *invalid*; unrecognized → *not established* (R8) |
| R2-11; IR1A-16 | Attribution hygiene: D2/D3 credited only with what they say; R-2/R2 restrictions labelled INTEGRATION or DERIVED (§0, §1 D15, R13) |
| R2-12; IR1-B X-9 | Request-side origin gains **governing checkpoint constraint**; an App-carried run omitting a declared constraint is an R11 limit; host receipt of it is a relay question (U-19) |
| R2-13; IR1-B M7 | Identity de-duplication precedes the basis check; a retry returns the recorded state/outcome and is never refused stale because of its own effects; per-item basis check by subject content identities of relied-on targets (OE-4) |
| R2-14; IR1-B M6 | Applied outcome records **resulting objects**: created/changed object identities and their subject content identities after application; used for R8 subject binding (§5) |
| R2-15; IR1A-06; IR1-B B-m3 | Relation renamed **reverses ⟨receipt⟩ (entry ⟨ref⟩)**; acts bound to content the undo changes lapse normally; A5/A10 on the reversed item not lapsed (OE-6, L-10) |
| R2-16; IR1A-11; IR1-B B-m2 | Stale after acceptance: A5 record and application-time *refused — stale* entry both present, A5 not lapsed; **U-09 narrowed** to host evidence (DEP-001) |
| R2-17; IR1C-01/05 | R8 subject class is its own element; classes incl. **targets of the held call** and **grant setting** |
| R2-18; IR1C-02 | Mixed item decisions: per-item *partial* annotation, item-left events, never "all accepted" over a reduced subject (R8); PROPOSED, U-18 |
| R2-19; IR1A-09; IR1C-07 | Lapse before resume: **act-lapsed event** recorded, disposition returns to "waiting — lapsed at ‹t›"; *lapsed* as standing disposition only for ended runs (L-12) |
| R2-20; IR1C X-11, X-17, X-18 | Holding library recorded as non-identity fact (R2); capture-evidence reference relay (U-11); per-turn guidance source + content identity or *unknown* (R3) |
| R2-21; IR1A-07; IR1-B X-6 | Fixtures re-pointed to C-v0.2 §10 (T1–T17, PR-1/PR-2, RC-1…RC-3, B1/B2, OP-C1…C9) plus OP-C10 Undo and OP-C11 (no policy basis); local cases named `L-RS-n` with reasons (§12). "B2 (r12)" error removed |
| IR1-B B-m4 | "stale (refused)" → **refused — stale**; "reporter" → **observer** |
| IR1-B B-m8 | Author identity (seat instance) and seat role meaning kept separate (§5) |
| IR1A-12 | Act kind excludes A9 and A14; A11 is a human act only when the person is the proposer; act class covers A10 and states A5 conditionally; self-recording is *direct capture* by the capturing surface |
| IR1A-14 | Grant value (direct / propose) distinguished from host-resolved *treatment* |
| IR1A-15 | R3, R5a, R13 marked as additions with sources; VC-02 accepts *not applicable* with reason |
| IR1A-20 | SoW TBD-001 still reads OI-001/OI-002 as open — pointer reconciliation for C1 (finding, no SoW edit) |
| IR1A-21 | U-03 (R1-sourced supplier elements) closed as confirmed by IR1, except as amended by R2 |

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
  external access · A14 answer tool permission. A9 is a recording act, not a
  decision act. A14 is never a human-act record (R2-8).
- **Class values (DEL-04-01 §8.1; R2-1):** none · may apply within granted
  autonomy · proposal only · reserved to the person (the four V4-HI-02 values,
  SETTLED) · **no policy basis**, with *reason* ∈ {omitted, unassigned, pending
  OI-021} (INTEGRATION, R-3.5).
- **Reserved to the person.** ADOPTED by D2 (DECISION-1): A4; A5 wherever the
  active autonomy requires a proposal; A6; A7; A12; enabling external access
  (A13). DERIVED (R-1, R2-2): A10 wherever A5 is; operations that perform any
  of these. INTEGRATION (R2-3): disabling external access is also a person's
  A13. The SWB model-change class is *may apply within granted autonomy*
  (DERIVED from V4-HI-41) with default *propose* (DEL-04-01 P-03).
  Operation-specific additions await OI-021. Host adoption is not shown
  (DEP-001).
- **Grant value** (direct / propose) is what the person sets. **Treatment** is
  what the host route resolves at validation and application (IR1A-14).
- Examples are **fixture subjects** from DEL-03-01 §10 (FX-PIPE-01).

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

## 2. Ordinary-file authority rules

| Rule | Statement | Serves |
|---|---|---|
| FA-1 | The authority for "person P performed act K on content C for purpose U" is an **act record** in an ordinary project/workspace file together with the evidence it references. Nothing else supplies a missing act. | REQ-001, REQ-003; AC-001 |
| FA-2 | Harness session content, transcripts, agent memory, derived views, search indexes, PEC projections and A14 settlements may **locate** evidence. Their assertion that an act occurred creates none. | REQ-001; D2; D15 |
| FA-3 | Host domain truth, receipts, hashes and origin marks stay with the host. A record holds **references** plus what is needed to resolve and compare them: reference, claimed identity, identity method designation, resolution status. Never a substitute copy. | REQ-002; D3, D4 |
| FA-4 | Workflow definitions and accepted records remain owned by their producing deliverables; this format supplies the act and run records that refer to them. | REQ-001, REQ-005 |
| FA-5 | A written act record is not edited to change actor, act kind, bound content, scope or purpose. A correction is a new record naming the corrected one; both remain readable. Supersession of A12/A13 (L-0) is a relation, not an edit. (Proposed; mechanism unselected.) | REQ-003, REQ-004 |
| FA-6 | Git history is the primary change record for the files (D13); records cite a repository revision where their own revision matters. | AX-003 |
| FA-7 | Each record identifies its **format version** and **record kind**; a reader refuses or limits an unknown version. | OUT-001 |
| FA-8 | The **recorder** is always identified and is never the decision actor merely by having written the record. A person's own act captured in a surface is *direct capture* by that surface, not self-recording. | REQ-003; D10 |
| FA-9 | App runs keep records with the user's project/workspace; host-agent runs keep records with the host project (V4-HI-70). Path and host persistence are not selected (U-05, U-06). | REQ-001, REQ-005 |

## 3. Record kinds and identity

| Record kind | Authority for | Produced by |
|---|---|---|
| Run record | That a workflow run occurred with the identified workflow, conversation, model, settings, requested operations and observed outcomes, linking host evidence | App writer (OUT-002) for App runs; host run recording (external owner, DEP-04-03-016) for host-agent runs, in the shared meaning |
| Human-act record | That an identified person performed A4, A5, A6, A7, A10, A12 or A13 — or A1/A2 when the person performs them, or A11 when the person is the proposer — on identified content, scope and purpose, with capture evidence | A recorder: capturing surface, App, host facility, or an agent performing A9 |
| **Act-declined event** | That a person decided **not** to perform a required A4, A6, A7 or A12 on an identified subject, with capture evidence (R2-5). It is not an act of that kind, never records the declined act as performed, and satisfies nothing that requires the act | Same recorders |
| **Run-ended event** | That the run stopped (V4-EXE-01), who stopped it (person, or the observer reporting an end), and which checkpoints were then *waiting* (R2-5) | Run writer |
| **Act-lapsed event** | That a performed act was observed lapsed at ‹t›, with c₀/c₁ (R2-19) | Record reader/writer on evaluation |
| Decision / accepted record | A PKG-06 or workflow-owned record an act record may cite | Its owning deliverable |

Common identity elements: *record identity*, *record kind*, *format version*,
*recorder identity*, *recording context* (App, or host identity),
*written-at order*, *corrects* (optional).

## 4. Run-record inventory

Every element named in REQ-002 / SOW-186 / V4-HI-70 is present. "Required"
means present as a value or as an explicit absence statement; *not
applicable* is allowed only with its reason. Elements marked **addition** go
beyond the SoW inventory and name their source (IR1A-15).

| # | Element (semantic) | Meaning | Supplier | Absent / unknown handling |
|---|---|---|---|---|
| R1 | Run identity | Stable identity of this run, distinct from conversation, proposal and operation identities | Record writer | Required |
| R2 | Workflow identity as observed | {kind, origin (project / user / bundled / host), source root, name, revision} + derived-from; promised vs observed separate. An unadapted carried workflow keeps its original origin; host adaptation → host origin + derived-from. **Holding library** recorded at the listed, selected and resolved links as a non-identity fact; never part of identity equality (R2-20; PROPOSED until W7) | DEL-02-01 §6.1 (R-9); DEL-05-01 run association | Selection alone does not show supply or adoption |
| R3 | Supplied guidance identity and limits — **addition** (R-10; R2-20) | Per thread and turn, the **source identity** (origin and name, or workflow identity tuple) and **content identity** (with method designation) of each guidance input supplied; "supplied ≠ adopted" | DEL-01-01 (App); host loop (relay question) | Where not recordable: *unknown*; never inferred from configuration |
| R4 | Conversation reference | Reference to the harness conversation/session | Harness | Reference only — operational, not authority |
| R5 | Model used | Model identity and serving endpoint class (local / user-chosen cloud) as observed, separate from configured | DEL-01-01; DEL-05-01 | "Requested X; observed unknown" is valid |
| R5a | Seat role meaning — **addition** (R-7; V1-C AB-02) | The role meaning in force for the acting seat | DEL-05-01 / DEL-02-01 | *unknown* where not determinable |
| R6 | Autonomy settings | Every settings version in force, requested or refused for the run: scope; per-class grant value and class value; display state (§8 list); requester; setting actor; A12 act reference for person-set states; **policy-class record reference and default** for *effective (policy default)*; establishment evidence or refusal reason | DEL-04-02 settings-in (§8); DEL-04-01 | Never shown effective without its evidence |
| R7 | Requested operations | One entry per submission, read, examination, or loop-side refusal (§5) | Loop/adapter trace; DEL-03-01; DEL-03-02 | Required per request made |
| R8 | Checkpoint events | Per declared checkpoint: required act kind (closed list A4, A5, A6, A7, A12; outside the list → *invalid*; unrecognized → *not established*, R2-10); **subject class** (own element, independent of reached-when, R2-17: change items of a named proposal · named output · objects changed by a named outcome · targets of the held call · grant setting); *reached-when* observation; bound subject referent and its content identities; disposition (waiting · performed · resolved negatively · lapsed · not reached · unknown); satisfying act / A10 / act-declined event references; per-item decisions with *partial* annotation and item-left events (R2-18); act-lapsed events; run-ended event if the run ended while waiting; governing checkpoint constraint issued (R2-12) | DEL-02-01 declares; DEL-05-01 evaluates in hosts; DEL-02-03 hold machine | Not observed → *not reached*, never satisfied. Run ended while waiting → stays *waiting* with run-ended event |
| R9 | Human acts | References to human-act records, act-declined events and act-lapsed events | §6 | None created without capture evidence |
| R10 | Agent examination findings | References to A3 findings (e.g. OP-C3) | Agent output | Never "host checks passed", never A4. If the host stores findings through a change operation, also an R7 entry (U-14) |
| R11 | Evidence limits | Lost acknowledgement, missing receipt, unresolvable reference, origin mismatch, omitted governing checkpoint constraint, unobserved adoption | Record writer | Required |
| R12 | Record identity elements | §3 common elements | Record writer | Required |
| R13 | Tool-permission settlements (A14) — **addition** (D3; R2-8) | Each tool-permission request and its settlement origin: the person via interaction; the user's own Codex mode inside the supplier; an App named-rule decline or explicit error (R-2, INTEGRATION: the App never answers affirmatively by rule) | DEL-01-01 observed facts in this undertaking; DEL-01-02 later (D1) | **Only here** — never R6, never a human-act record, never a grant. *Not applicable* in host-loop runs (hosts have no classifier mode, D3) |

## 5. Operation entries and outcome evidence

**Entry elements (semantic).** Operation identity and version (DEL-03-01);
**request-side origin** per DEL-03-02 §3.3: author type (person / agent),
author identity (the person, or the agent seat instance), seat role meaning,
channel, conversation, workflow identity (R2), workflow run, standing at
drafting, settings reference at route decision, settings reference at
application (host-reported, otherwise *unconfirmed*), reason, and the
**governing checkpoint constraint** {workflow run, checkpoint name, required
act A5, operation} where one applies (R2-12); **host origin-mark reference**
(linked; mismatch → R11); **relied-on basis** (workspace identity,
generation, model revision, canonical content identity, method designation;
never a later queue-time basis); **observed basis** for reads and
examinations; **evaluated basis** on every non-success; route (direct /
proposal); treatment at resolution where it differs from standing at drafting
(R-3.6); **proposal identity**, lineage, and per-item **change-item content
identity**; item dispositions with actors; **outcome**; receipt references;
**resulting objects** (R2-14); standing received; **submission ordinal**;
**reverses ⟨receipt⟩ (entry ⟨ref⟩)** for an undo (R2-15); **observer** for
outcome unknown.

**Outcome vocabulary** is DEL-03-02 §9 and DEL-03-01 §4.1, adopted unchanged
(R-7), with R2 amendments:

| Outcome as recorded | Minimum evidence referenced | Actor / observer | May NOT be inferred from |
|---|---|---|---|
| not offered (loop-side, never dispatched) | Operation absent from the catalog edition offered to the loop (R2-4) | Loop | Any host response |
| unavailable | Failed precondition, reason, evaluated basis (HI-04 parity) | Host | Channel off; a class reason |
| not exposed on this surface | Host-declared per-surface exposure element, relayed (R2-4) | Host (relayed by loop/adapter) | *unavailable*, *missing*, *channel not enabled*, or any class reason |
| channel not enabled | External access off; A13 not performed | Host / adapter | *unavailable* |
| not permitted | Governing treatment and policy record — or the **governing checkpoint constraint** (R2-12) — and evaluated basis. Reserved entry: an A8 is **offered**; an A8 record exists only if the agent issues it (R2-4). A direct request without an effective direct treatment is never converted into a proposal | Host route | A class reason rendered as unavailable or not exposed |
| error | Error identity, evaluated basis, effect statement | Host | — |
| drafted / validated | Host validation result (validated) with treatment and settings reference | Proposer (A1) / host | Agent assertion |
| refused — invalid | Host validation refusal with catalog error | Host | — (never "rejected") |
| refused — stale | Reason; **relied-on and current bases**; affected items | Host | Local comparison alone; a retry's own effects (R2-13) |
| queued | Host acknowledgement | Host | Transport completion |
| accepted (per item) | A5 human-act record bound to the item's change-item content identity | Person (A5) | Success, receipt, agent statement |
| rejected (per item) | A10 human-act record | Person (A10) | Host refusal; silence |
| withdrawn | A11 record | Proposer (A11) | A person removing another's proposal (that is A10) |
| applied (receipt) | Applied-outcome association: proposal/item, relied-on basis, receipt, resulting revision, branch (after acceptance / direct under grant with settings references), **resulting objects** and their subject content identities after application (R2-14) | Host | `success`, queued, accepted |
| application error | Error identity; effect *none* / *partial* (receipt references) / *unknown* (→ overlay) | Host | Any unstated effect |
| outcome unknown (overlay) | Observation gap; **last observed state** | The **observer** that lost observation: loop, App adapter or host | — (default when evidence is missing) |
| success (operation ran) | Result reference and observed basis (reads, examinations) | Host | Any human act |

Rules. **OE-1** Transport success, a tool-call return, source resolution or a
resolvable receipt *reference* never upgrades an outcome. **OE-2** A re-draft
after *refused — stale* is a new entry with a new proposal identity and
lineage. **OE-3** Each submission is its own entry, recording only the effects
actually observed; "one effect per proposal identity" is a host obligation to
be evidenced (DEP-001), not a recorded fact. **OE-4** A retry keeps the same
proposal identity. Identity-based de-duplication precedes the basis check:
the retry entry records the recorded state or outcome the host returned, and
is never recorded as *refused — stale* because of the proposal's own effects.
The per-item basis check compares the subject content identities of the
item's relied-on targets; applying sibling items does not stale remaining
items unless they share targets (R2-13; host behaviour DEP-001). **OE-5** A
derived proposal state is never stronger than its items. **OE-6** An undo is a
change through the one route with its own entry, origin, basis check and
outcome; *undone* is recorded as *applied (receipt)* with **reverses
⟨receipt⟩ (entry ⟨ref⟩)**. It erases no act record. A5/A10 on the reversed
item are not lapsed by it; acts bound to subject content the undo changes
lapse under §7 (R2-15). **OE-7** Accepted then refused stale: the A5 record
and the application-time *refused — stale* entry are both present; the A5 is
not lapsed; the item is not applied; a re-draft carries no acceptance
(R2-16; DEL-03-02 §4.2).

## 6. Human-act record

### 6.1 Elements (semantic)

| Element | Meaning | Required |
|---|---|---|
| Act identity | Identity of this record | Yes |
| Act kind | A4, A5, A6, A7, A10, A12, A13; A1/A2 when the person performs them; A11 when the person is the proposer. Never A9 (carried by recording mode) or A14 (R13 only) | Yes |
| Act class | As applicable: "reserved to the person" for A4, A6, A7, A12, A13 (D2; disabling A13 INTEGRATION) and for A5/A10 where the active autonomy requires a proposal (D2b; A10 DERIVED); for acts through a catalog operation, the operation's class from the DEL-04-01 policy-class record, including *no policy basis* with its reason | As applicable |
| Governing policy reference | Policy-class record and **policy revision identity** (DEL-04-01 §8.1); DECISION-1 for D2/D3 | With act class |
| Decision actor | The person who performed the act | Yes |
| Recorder | Capturing surface, App, host facility, or agent | Yes |
| Recording mode (sub-element of A9) | *direct capture* (the capturing surface wrote it, including the person's own act in that surface) or *faithful recording* (recorder ≠ capturing surface; cites capture evidence) | Yes |
| Bound subject | Change item(s) (A5/A10); host row/object (A4/A6/A7); App file; **setting content** (A12/A13) | Yes |
| Bound content c₀ with method m₀ | A5/A10: change-item content identity (DEL-03-02 §3.1); A4/A6/A7 on host content: subject content identity (DEL-03-01 §5.3); App files: file content identity; A12/A13: the setting content itself — classes, grant values, scope (R2-7) | Yes, or "not obtainable" → lapse permanently *unknown* |
| Scope | Change-item identities (a batch A5 lists several, each item-bound); row/object identities; setting scope | Yes |
| Purpose | What the act was for, in the actor's terms | Yes |
| Capture evidence references | From the capturing surface (host act facility for host content; App interface for App acts), each with resolution status | At least one; without it the record is non-conformant |
| Evidence limits | What the evidence does not show | Yes |
| Relations | Run, operation entry, checkpoint, workflow, decision record; for A12: **established settings version** or **control refusal**; **superseded by ⟨act⟩** (L-0) | As applicable; no required prior act |
| Order | Sequence/time as evidenced | Yes |
| Lapse evaluation | Latest state with compared c₀/c₁ and m₀/m₁ (§7); derived. Not evaluated for A12/A13 | Derived |

### 6.2 Rules

- **HA-1** Written only from capture evidence that the person performed the
  act. A proposal, success, grant, receipt, A3 findings, A8 request, A14
  settlement, silence or timeout is not such evidence.
- **HA-2** Decision actor and recorder are separate elements. A record naming
  the recorder as decision actor of A4–A7, A10, A12 or A13 is non-conformant.
- **HA-3** One record, one act kind. A5 never produces A4, A6 or A7. An
  independently evidenced act is recordable without any A5.
- **HA-4** A6 and A7 name the accountable person and scope only as evidenced;
  no certification, sealing or code-compliance label. A6 is engineering
  approval only; V4-HI-65 design-candidate approval is a separate later act.
- **HA-5** A12 and A13 are human-act records; R6 references A12. An agent's A8
  request for a grant change creates no A12.
- **HA-6** Act class is carried, never computed here. *No policy basis* is
  shown as "no policy basis — held (reason)", never as permission (R2-9).
- **HA-7** Faithful recording (A9) by any identified recorder distinct from
  the decision actor is a conformant record shape. It satisfies a checkpoint
  only through the capture evidence it cites (R-5). Host-specific capture
  requirements and a capture-evidence reference are relay questions (U-11).
- **HA-8** For A5 the negative decision is A10. For A4, A6, A7 or A12 it is an
  act-declined event. Stopping the run is a separate run-ended event (R2-5).
- **HA-9** No faithful record is made through a catalog operation that
  performs A4, A5, A6, A7, A10, A12 or A13 (reserved, R2-2). App-side A9
  records are DEL-04-03 files, not catalog operations. A host-offered
  faithful-record operation, if any, must not change act state, must cite
  capture evidence, never satisfies a checkpoint and takes ordinary policy;
  whether any host offers one is a relay question (DEP-001).

## 7. Content binding and lapse comparison rule

Notation: *S* bound subject; *c₀*, *m₀* bound content identity and method
designation; *c₁*, *m₁* the current identity of the same subject and scope.

| Step | Rule |
|---|---|
| L-0 | **A12/A13 are not lapse-evaluated.** A later A12 on an overlapping class and scope (or a later A13 on the same interface) **supersedes** the earlier act; the record shows *superseded by ⟨act⟩*. A checkpoint the earlier act performed stays *performed*, with the supersession shown. Operations are governed by the grant state at route decision and application (R2-7; PROPOSED). |
| L-1 | Obtain c₁ for exactly the bound subject and scope from one of three sources: **change-item content identity** (DEL-03-02 §3.1) for A5/A10; **subject content identity** (DEL-03-01 §5.3) for A4/A6/A7 on host content; **file content identity** for App files. Never the workspace generation or model revision. |
| L-2 | Compare method designations. m₁ ≠ m₀ or comparability not shown → **unknown (incomparable)**. |
| L-3 | c₁ not obtainable → **unknown (unavailable)**. |
| L-4 | S no longer exists → **lapsed (subject absent)**. |
| L-5 | c₁ = c₀ → **not lapsed**. |
| L-6 | c₁ ≠ c₀ → **lapsed**, retaining c₀, scope and purpose; not carried to the new content. An **act-lapsed event** is recorded. |
| L-7 | Multi-element scope: evaluate per element. A batch A5 lapses per item. A multi-row A4 with some rows changed is **partially lapsed**, listing them; its purpose for unchanged rows is an owner question (U-07). |
| L-8 | Lapse never deletes or edits the act record. |
| L-9 | Host-presented lapse (V4-HI-32) is linked where supplied; an App/host disagreement is shown and is an R11 limit. |
| L-10 | Applying an accepted change item does not lapse its A5. A basis failure between A5 and application is *refused — stale* (OE-7), not lapse. An undo does not lapse A5/A10 on the reversed item; acts bound to subject content the undo changes lapse under L-6 (R2-15). |
| L-11 | Content returning to c₀ after an observed lapse is shown "matches c₀ again after observed lapse", keeping the lapse interval visible; whether the act is effective again is U-12. |
| L-12 | **Checkpoint effect (R2-19).** A performed checkpoint's act lapses → act-lapsed event recorded. Before the run resumes, the disposition returns to **waiting**, shown "waiting — lapsed at ‹t›", for a new act on current content. After resume, re-hold belongs to DEL-02-03 (W7); the record shows the performed disposition with the act-lapsed event until DEL-02-03 defines it (U-24). *Lapsed* as a standing disposition is used only for a checkpoint whose run has ended. |

Lapse states: not lapsed · lapsed · lapsed (subject absent) · partially
lapsed · matches c₀ again after observed lapse · unknown (incomparable) ·
unknown (unavailable) · not yet evaluated. For A12/A13: current · superseded.
*Not yet evaluated* never renders as *not lapsed*.

## 8. Settings-in / record-out exchange with DEL-04-02 (CASE-002 M3)

Identical in DEL-04-02/AS-v0.3 §6. A data exchange, not an ordering between
human acts and not a second authority.

**Settings-in (DEL-04-02 → DEL-04-03 writer), per run and per change:** run
identity; settings version identity; **scope** (representation-neutral
dimensions, e.g. model/workspace, object set, run, period, consequence); per
operation class — **grant value** (direct / propose) and **class value**
(DEL-04-01 policy-class record reference; for *no policy basis*, its reason);
display state (effective · effective (policy default) · requested by agent ·
set by person, not yet confirmed by control · unconfirmed · not set · refused
(reason)); **requester** (person; agent via A8; *none — policy default*);
**setting actor** (the person, only where an A12 exists; *none — policy
default*); **setting act reference** (A12 record) — or, for *effective (policy
default)*, the **policy-class record reference and its default value** in its
place; **establishment evidence** (control confirmation) or refusal reason;
order relative to operation entries; source of control (App or host).

**Record-out (DEL-04-03 reader → DEL-04-02), per run:** record identity and
format version; recorded settings versions with the fields above; per
operation entry the two settings references, route, treatment at resolution,
governing checkpoint constraint, outcome, item dispositions with actors,
receipt/origin references, resulting objects, *reverses* relations and
evaluated/relied/current bases; human-act records, act-declined events and
act-lapsed events with actor, recorder, recording mode, kind, act class, bound
subject, scope, purpose, c₀/c₁ with method designations, lapse or supersession
state and capture evidence references with resolution status; checkpoint
events with subject class, disposition and run-ended events; evidence limits.

**Comparison (DEL-04-02)** per settings version: displayed vs recorded →
*match* · *mismatch* · *missing in record* · *missing in display*. Mismatch is
shown to the person and returned as a defect observation. The record is
authoritative for what was recorded; the control for the current grant; the
display is derived. Neither side auto-corrects the other. A person-set state
without an A12 reference, or an *effective (policy default)* state without a
policy-class record reference, is a defect, not an established setting.

## 9. Evidence references

Each reference carries: evidence kind (receipt, content identity, origin
mark, capture evidence, commit, supplier settlement), claimed identity,
identity method designation where applicable, and resolution status at write
(resolved / unresolvable / not supplied) and at read. "Resolved" means the
source was found with the claimed identity; it does not make the referenced
change or act more than the source states (OE-1).

## 10. Consumer and host interface

| Consumer | Consumes (meaning) | Supplies back | Held part / limit |
|---|---|---|---|
| DEL-02-01 | Act names; R8 subject classes and dispositions; R2 | Workflow identity; checkpoint reached-when, subject class, §4.3.7 mixed-item rule | Closed act list A4/A5/A6/A7/A12 |
| DEL-02-03 | R8 waiting / performed / lapsed events; run-ended; R7 unknown outcomes | Hold machine; re-hold after resume; resumption of ended runs (W7) | U-17, U-18, U-23, U-24 |
| DEL-03-01 | R7 identity/basis; c₁ for A4/A6/A7 | Subject content identity; method designation; exposure element; shared fixture §10 | Algorithm unselected (TBD-003); U-C3 attribute coverage |
| DEL-03-02 | §5 evidence rules | §9 outcomes; change-item content identity; origin incl. governing checkpoint constraint; resulting objects; item-left events | One-effect mechanism unselected |
| DEL-04-02 | Record-out (§8) | Settings-in (§8) | Executable M3 trace needs candidate writer/reader |
| DEL-05-01 | R3/R4/R5/R5a/R7/R8 meanings | Observer-attributed unknown; origin, seat role, grant in force, constraint per dispatch; loop-side *not offered*; run-ended | — |
| DEL-05-02 | Act, act-declined, lapse, supersession display meanings | — | — |
| DEL-01-01 | R3, R13 meanings | Supplied-guidance identities; A14 settlement origin (observed facts) | Pin 0.158.0 is definition only (D4) |
| PKG-06 (DEL-06-01/06-02) | Act records cited by coordination; actor ≠ recorder; lapse | Decision records as act subjects | Coordination recorder never becomes actor |
| DEL-09-11 | Complete records for the week-later reconstruction | — | This format does not perform the witness |
| DEL-01-02, DEL-01-04, DEL-02-02, DEL-02-04 | R3/R4/R7/R13; act display; review/registration acts | Observation evidence; role bytes | Outside this undertaking (D1) |
| External host run recording (DEP-04-03-016; DEP-001) | §§3–9 | Receipts, origin marks, subject content identities, capture evidence and its reference, lapse, per-operation settings version, constraint receipt, per-turn guidance identities | Adoption unclaimed; OI-013 placement |

## 11. Excluded acts and owners (REQ-006)

OI-001/OI-002 were decided at App/shared level by the Owner in DECISION-1
(D2, D3); operation-specific additions remain with the Owner via the outside
SWB session and App/shared owner (OI-021). The SoW's TBD-001 still reads them
as open — a pointer reconciliation for closeout C1 (IR1A-20). Defining and
carrying policy — DEL-04-01. Autonomy/standing UI — DEL-04-02. Reconstruction
witness — DEL-09-11. Host domain changes, receipts, storage, host run
recording, host enforcement of its reserved list — responsible host owner
(SWBPIPE outside session). Performing any human act — the person.
Professional reliance and certification — the accountable professional. This
format faithfully records evidenced acts; it performs none.

## 12. Examples (fixture subjects — invented; no act was performed)

All identifiers are DEL-03-01/C-v0.2 §10 (commit 28bd00499) unless marked:
FX-PIPE-01, workspace FX-W1, generation g1, run R-100, supports S-1…S-4,
Engineer A, workflow `supports-adjust` (origin *host*, root ⟨fx-root⟩,
revision ⟨rev-3⟩), bases B1 (r12) and B2 (r13), proposals PR-1/PR-2, receipts
RC-1…RC-3, steps T1–T17, method ⟨m-fx⟩. **OP-C10 Undo** and **OP-C11** (class
*no policy basis*, reason pending OI-021) are fixed by R2-21 and not yet in
C-v0.2. Local cases are `L-RS-n`, each saying why.

**E1 — Stale, re-draft, per-item decisions, application (T3–T12).** T3 read
OP-C1 → B1. T5 PR-1 relies on B1: item 1 add guide support at 4.2 m (OP-C4),
item 2 S-3 stiffness (OP-C5). T6 Engineer A edits S-3 (r13). T7 R7 entry:
**refused — stale**, relied B1, current B2, reason "S-3 changed since r12".
T9 PR-2 (lineage PR-1) relies on B2; T10 queued (host ack). T11 ⟨act:1⟩ **A5**
on item 1: actor Engineer A, recorder host facility, direct capture, c₀ =
change-item identity ⟨ci:PR-2/1⟩ with ⟨m-fx⟩, class "reserved to the person
(D2b)"; ⟨act:2⟩ **A10** on item 2. T12 applied item 1: RC-1, resulting r14,
resulting objects {new support ⟨S-new⟩ with its subject content identity}.
⟨act:1⟩ stays **not lapsed** (L-10). No A4, A6 or A7 exists or is implied.

**E2 — Faithful recording (T2).** Engineer A marks S-2 checked via OP-C6
(reserved; host capture ⟨cap:T2⟩). The App agent writes ⟨act:3⟩: A4, actor
Engineer A, recorder App agent, mode faithful recording, c₀ ⟨S-2@r12⟩,
evidence ⟨cap:T2⟩ resolved. Conformant as shape (HA-7); it is an App file, not
a catalog operation (HA-9).

**E3 — Negatives.** (a) T5 PR-1 drafted only → no act record. (b) T4 OP-C3
examination → R7 *success* with observed basis B1 and R10 findings; never "host
checks passed", never A4. (c) T15 grant alone → no act on any content. (d)
Transcript says "Engineer A approved" with no capture evidence → nothing
written; R11 limit. (e) A Codex tool-permission prompt answered by the user's
mode → R13 entry only. (f) Agent calls OP-C6 → *not permitted*, A8 offered;
no A8 record unless the agent issues one.

**E4 — Lapse and control (T2, T6, T14).** ⟨act:3⟩ bound ⟨S-2@r12⟩. T6 edits
S-3 → ⟨act:3⟩ **not lapsed** although the model revision advanced. T14 edits
S-2 → **lapsed**, act-lapsed event recorded, c₀ retained.
**L-RS-1** (why: C has only a single-row A4) — A4 on S-1 and S-2 at r12; T14 →
**partially lapsed** (S-2); purpose U-07.

**E5 — Retry and unknown (T13).** Acknowledgement of T12 lost; the agent
resubmits PR-2 (same identity). Entry 2 records what the host returned — RC-1
(de-duplication before basis check; never *refused — stale* because of item
1's own application, R2-13) — or **outcome unknown**, observer agent/loop,
last observed state "submitted". Entry 1 stays as observed. No "one effect" is
written as fact.

**E6 — Direct and undo (T15–T17).** T16 OP-C9 applied directly (label S-4
"G-4"): RC-2, origin mark, undo route; settings at route decision ⟨set-T15⟩,
at application host-reported or *unconfirmed*; no acceptance. T17 **OP-C10**
undo → applied, RC-3, **reverses RC-2** (entry T16). **L-RS-2** (why: the
undo-lapse rule needs an act on the changed row) — an A4 on S-4 captured
between T16 and T17 lapses at T17 if S-4's subject identity covers its label
(host input U-C3).

**E7 — Grant change and supersession (T15).** Engineer A performs ⟨act:5⟩
**A12**: bound setting content {class of OP-C9, grant value direct, scope:
object set "support labels on R-100", model/workspace FX-W1}; relation:
established as ⟨set-T15⟩. **L-RS-3** (why: supersession has no C step) — a
later A12 narrowing the same class to propose → ⟨act:5⟩ *superseded by*
⟨act:6⟩, not lapsed.

**E8 — Stale after acceptance. L-RS-4** (why: declared local divergence per
IR1A-07; not on C's timeline) — after T11, an intervening edit to the target of
PR-2 item 1 before application → R7 *refused — stale* (relied B2, current
basis) at application; ⟨act:1⟩ present and **not lapsed**; item not applied.

**E9 — No policy basis (OP-C11).** Agent requests OP-C11 directly → *not
permitted* naming the class *no policy basis* (pending OI-021). An A12 widening
the class → refused (reason: no policy basis). Fixture result: **held**.

**E10 — Checkpoint events. L-RS-5** (why: C has no declared checkpoints) — an
A4 checkpoint with subject class "objects changed by a named outcome" (T12
resulting objects) reached; Engineer A records an **act-declined event** →
*resolved negatively*. Variant: nobody acts and the run ends → **run-ended
event**, checkpoint stays **waiting**.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 Operation-specific reserved additions `OI-021` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Class may be *no policy basis (pending OI-021)*; fixtures held |
| U-02 Consequence vocabulary | DEL-04-01 with host policy owner | Before class assignment in DEL-03-01 | Scope dimension "consequence" is a slot only |
| U-04 Serialization, field names, identity algorithms, record-identity form | DEL-04-03 with DEL-03-01 (TBD-003) | Before OUT-001 CONFIG and writer implementation | L-2 depends on method designations only |
| U-05 App record location | DEL-04-03 with OI-014 owners | Before writer implementation | "Ordinary files" only |
| U-06 Host persistence/placement `OI-013` | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Host recording follows meaning only |
| U-07 Purpose of a multi-row A4 after partial lapse | DEL-04-01 with Owner | Before lapse display criteria are fixed | Per-row lapse only |
| U-08 Workflow review/registration as act kind | DEL-04-01 with DEL-02-02 (later undertaking, D1) | DEL-02-02 definition | Not recorded here |
| U-09 (narrowed) Host evidence that application re-checks the basis after acceptance | Host owner (DEP-001) | Before connected integration | OE-7 records both entries; contract rule settled by DEL-03-02 §4.2 |
| U-11 Host capture requirement per act kind; capture-evidence reference | Host owner (DEP-001; R2-20 relay) | Before host act-recording integration | Without a reference, no host-content checkpoint reaches *performed* |
| U-12 Content returning to c₀ after observed lapse | Host owner (U-C2) with DEL-04-03 | Before lapse display criteria are fixed | L-11 keeps lapse visible |
| U-14 Host-stored findings as a change operation (C U-C5) | Host owner | Before V4-EXM-21 fixture binding | R10 may also need an R7 entry |
| U-15 Host receipts, origin marks, subject identities, resulting objects, lapse, per-operation settings version, de-duplication before basis check `DEP-001` | SWBPIPE outside implementation session | Before corresponding connected-journey integration/examination and fallback-replacement decision | All host evidence in examples is fixture |
| U-16 Reader/writer placement `OI-014` | App/shared contract owners | Before structural/production contract allocation | No common service assumed |
| U-17 Whether an A12 the control refused can count at a checkpoint (R2-7) | DEL-02-03 | W7 | Recorded with *refused* relation; checkpoint effect held |
| U-18 Mixed item decisions at an A5 checkpoint (R2-18, PROPOSED per WD §4.3.7) | DEL-02-01 with DEL-02-03 and DEL-03-02 | W7 | R8 records per-item decisions, partial annotation and item-left events |
| U-19 Whether the host receives the governing checkpoint constraint or evaluates its own copy (R2-12) | Host owner (relay) | Before connected integration | Omission is an R11 limit App-side |
| U-20 R13 feed beyond DEL-01-01 observed facts | DEL-01-02 (later undertaking, D1) | DEL-01-02 definition | R13 fed by DEL-01-01 only here |
| U-21 Host loop per-turn guidance source/content identity (R2-20) | Host owner (relay) | Before connected integration | R3 *unknown* where absent |
| U-22 Holding library element (R2-20, PROPOSED) | DEL-02-03 | W7 | Non-identity fact in R2 |
| U-23 Resumption of an ended run; effect of post-end acts | DEL-02-03 | W7 | Post-end acts recorded; ended-run disposition unchanged |
| U-24 Checkpoint display after a lapse following resume | DEL-02-03 | W7 | Performed + act-lapsed event shown |

Closed in v0.3: U-03 (IR1A-21); U-10 (R2-8); U-13 (R2-5 name).

## Verification cases (designed, not run)

| Case | Input (fixture subject) | Expected result | Serves |
|---|---|---|---|
| VC-01 Authority | E1; transcript and derived view claim an A5 on PR-2 item 2 | Only ⟨act:1⟩/⟨act:2⟩; the claim creates no act | VER-001 (AC-001) |
| VC-02 Inventory completeness | E1 run record (App run) and a host-loop run | R1–R13 each present as value, explicit absence, or *not applicable* with reason (R13 in the host-loop run) | VER-001 (AC-002) |
| VC-03 Link not copy | E1 with RC-1 | Reference, claimed identity, method, resolution status only | VER-001 (AC-002) |
| VC-04 Faithful recording | E2 | A4, actor Engineer A, recorder App agent, faithful recording, capture evidence cited; conformant as shape | VER-002 (AC-003) |
| VC-05 Fabrication negatives | E3 (a)–(f) | No act records; (d) R11 limit; (e) R13 only; (f) no automatic A8 | VER-002 (AC-003) |
| VC-06 Independent act | Engineer A marks own edit checked, no proposal | A4 recorded; no A5 required | VER-002 (AC-003) |
| VC-07 Row lapse and control | E4 | T6: not lapsed; T14: lapsed with act-lapsed event, c₀ retained | VER-003 (AC-004) |
| VC-08 Incomparable / unavailable | E2 with m₁ ≠ m₀; host unreachable | *unknown (incomparable)*; *unknown (unavailable)* | VER-003 (AC-004) |
| VC-09 Model-row partial lapse | L-RS-1 | Partially lapsed (S-2); S-1 not lapsed; purpose U-07 | VER-003 (AC-004) |
| VC-10 Acceptance survives application and undo | E1, then an OP-C10 undo of RC-1 (local variant of L-RS-2; C has no undo of RC-1) | ⟨act:1⟩ not lapsed after T12 and after the undo | VER-003 (AC-004) |
| VC-11 Undo lapses row-bound act | L-RS-2 | A4 on S-4 lapsed at T17 (given U-C3 coverage); RC-3 *reverses RC-2* | VER-003 (AC-004) |
| VC-12 Restore after lapse | E4 then S-2 restored | "matches c₀ again after observed lapse" | VER-003 (AC-004) |
| VC-13 A12 supersession | L-RS-3 | *superseded by ⟨act:6⟩*; never lapsed; earlier-performed checkpoint stays performed | VER-003 (AC-004) |
| VC-14 Retry vs stale | E5 | Entry 2 records RC-1 or unknown (observer named); never *refused — stale* from its own effect | VER-004 (AC-005) |
| VC-15 Stale after acceptance | E8 | A5 present, not lapsed; *refused — stale* with both bases; item not applied | VER-004 (AC-005) |
| VC-16 Outcome vocabulary | One case each: not offered, unavailable (T8), not exposed (host-reported variant), channel not enabled, not permitted (E3f; E9; checkpoint constraint), refused — invalid, refused — stale (T7), application error (E-apply-interrupted), rejected (A10), withdrawn (A11) | Each distinct with evidence and actor/observer; host refusal never "rejected" | VER-004 (AC-005) |
| VC-17 Checkpoint events | E10 both branches; act kind outside list; unrecognized kind | *resolved negatively* with act-declined event; *waiting* + run-ended; *invalid*; *not established* | VER-002 (AC-003) |
| VC-18 Lapse before resume | E4 T14 while an A4 checkpoint on S-2 is performed and the run not resumed | Act-lapsed event; "waiting — lapsed at T14" | VER-003 (AC-004) |
| VC-19 No policy basis | E9 | *not permitted*; A12 refused; fixture reported **held**, not pass | VER-004 (AC-005) |
| VC-20 Grant change | E7; an A8 request alone; a policy-default state | A12 referenced from R6; A8 → "requested by agent"; default → policy-class record reference, no A12 | VER-002 (AC-003) |
| VC-21 Coverage inventory | VC-01…VC-20 against AC-001…AC-005 | Each AC has ≥1 positive and ≥1 negative case; candidate named; distinct from DEL-09-11 | VER-005 (AC-006) |
| VC-22 Owner trace | §10, §11, UNRESOLVED | Each REQ-005 consumer and REQ-006 excluded act traced; D2/D3 cited only for what they say; no delivery/adoption asserted | VER-006 (AC-007) |
