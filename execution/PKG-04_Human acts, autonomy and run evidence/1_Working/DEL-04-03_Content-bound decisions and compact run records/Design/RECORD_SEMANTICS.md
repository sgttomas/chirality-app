# Record Semantics
- Contribution: DEL-04-03/RS-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 and OUT-004 (definition content); OUT-002 and OUT-003 (behaviour and fixture design only — no writer, reader or fixture exists); REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; AC-001…AC-007 via designed VER-001…VER-006
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 74d42c38eaf2a6638b75bc5184f1741bc7d4f17171662a05a233d40f245340c1; `P/docs/PRD.md` §4.3 V4-EXE-03, §4.5 V4-AUT-01…05, §4.6 V4-PM-06, §4.7 V4-REC-01…05, §10; `P/docs/HOST_INTEGRATION.md` §1, V4-HI-11/12, V4-HI-21…25, V4-HI-30…33, V4-HI-40…42, V4-HI-70/71, §11; `P/docs/ARCHITECTURE.md` §4 (host-agent record property), V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-21/22/31; `P/docs/OPERATING_METHOD.md` V4-OPS-30…32; `DECISION_BRIEF.html` d2, d3; `OWNER_DIRECTIONS.md` J, O; `SCC-CASE-002/Case_Datasheet.md` M1 (DEL-04-03 row), M2 (DEL-02-04 row), M3 (both rows); `_Decomposition/Open_Issues.csv` OI-001/002/013/014/021; `External_Dependencies.csv` DEP-001
- Consumed inputs: accepted basis only. DEL-04-01 (act kinds, act classes), DEL-03-01 (read basis, canonical content identity), DEL-03-02 (proposal lifecycle and outcomes), DEL-02-01 (workflow source identity, checkpoints), DEL-02-04 (supplied role identity/limits) and DEL-04-02 (settings-in) are referenced by accepted meaning, to be reconciled at V1. DEL-04-02/AS-v0.1 was drafted concurrently by the same W2 executor; §8 below and its §6 state the same exchange.
- Receivers: CASE-002 M1 — DEL-02-01 (OUT-001/002; REQ-003; VER-003), DEL-01-04 (OUT-002/004; REQ-005; VER-005), DEL-02-02 (OUT-001/004; REQ-005/006; VER-005), DEL-02-03 (OUT-001/002; REQ-003; VER-003), DEL-04-02 (OUT-001/002; REQ-002/004; VER-002/004), DEL-05-01 (OUT-001/004; REQ-005/007; VER-008), DEL-05-02 (OUT-001/003; REQ-001/003; VER-001/003). CASE-002 M3 — DEL-04-02 (OUT-001/003; REQ-002/004/005; VER-002/004/005). Dependencies.csv DEP-04-03-011…016 — PKG-02, PKG-03, PKG-06, DEL-04-02, DEL-09-11, external host run recording.

## 0. Reading this definition

- Element names in this file (for example *bound content identity*) are
  **semantic names, not wire names**. No serialization, field spelling, JSON
  or TypeScript type, file path, persistence mechanism, transport, hash or
  canonicalization algorithm, process placement or shared-component placement
  is selected (SoW TBD-002; OI-013; OI-014; DEL-03-01 TBD-003).
- `⟨…⟩` denotes an opaque identity token in examples. It is not a hash, and
  equality of two tokens stands for "the identity method reports the same
  identity".
- Act kinds are named by their accepted-basis names (PRD V4-AUT-03; HI
  V4-HI-30/31/33; d3; DEL-04-01 SoW REQ-002): **propose**, **apply**,
  **examine** (agent examination), **mark checked** (human checking),
  **accept an edit** (proposal acceptance), **approve** (engineering
  approval), **rely** (professional reliance), and **faithful recording**
  where the actor is not the recorder. They will be reconciled with
  DEL-04-01 v0.1 at the V1 comparison. Act-class values (none / may apply /
  proposal only / reserved, V4-HI-02) are `UNRESOLVED{OI-001}` throughout.
- Examples use an invented piping model and are labelled **fixture
  subjects**. They record no act that anyone performed.

## 1. Settled distinctions relied on

Stated as settled with citation; this file adds no policy.

| # | Settled distinction | Citation |
|---|---|---|
| D1 | Workflow definitions, the person's decisions and accepted records are ordinary files in the user's project or workspace | V4-REC-02 |
| D2 | A harness session store is operational, not the authority for any human act; coordination views are derived and rebuildable, never the authority | V4-REC-03; V4-PM-06 |
| D3 | Host domain truth stays in the host's own store | V4-REC-01 |
| D4 | The host's receipts, hashes and origin marks are the evidence of what changed; the run record links them and does not copy them | V4-HI-71; V4-REC-04 |
| D5 | Operation `success` means it ran, never that a person accepted anything; a submitted proposal is "queued" until the host records acceptance and application | V4-HI-25 |
| D6 | Proposal lifecycle drafted → validated → queued → accepted → applied (receipt), with rejected / withdrawn / stale, and outcome unknown when the outcome cannot be observed | V4-HI-23 |
| D7 | Only observed events are shown as having happened; an unobserved outcome is shown as unknown | V4-EXE-03; V4-EXM-31 |
| D8 | A human act binds to the content it concerns and lapses visibly when that content changes | V4-HI-32; V4-REC-05 |
| D9 | Accepting a proposed edit is not engineering approval; proposals say "accept", never "approve" | V4-HI-33 |
| D10 | Agents may prepare decisions and ask for an act; they do not record a human act as performed when it was not. Faithful recording of an actually performed act is permitted; false attribution is prohibited | V4-HI-31; V4-AUT-03; d3; SoW CLM-003 |
| D11 | Propose, apply, examine, mark checked, accept an edit, approve and rely are different subjects; evidence of one establishes none of the others; no universal acceptance-first chain | d3; V4-AUT-03; SoW REQ-003 |
| D12 | Nothing the agent produces is presented as certified, sealed, approved or code-compliant | V4-AUT-05 |
| D13 | Git history and reviewed pull requests are primary change records; do not duplicate them in parallel evidence systems | V4-OPS-31 |

## 2. Ordinary-file authority rules

| Rule | Statement | Serves |
|---|---|---|
| FA-1 | The authority for "person P performed act K on content C for purpose U" is an **act record** in an ordinary project/workspace file together with the evidence it references. Nothing else supplies a missing act. | REQ-001, REQ-003; AC-001 |
| FA-2 | Harness session content, transcripts, agent memory, derived coordination views, search indexes and PEC projections may **locate** evidence. Their assertion that an act occurred is not an act record and creates none. | REQ-001; D2 |
| FA-3 | Host domain truth, receipts, hashes and origin marks stay with the host. A record holds **references** to them plus the minimum needed to resolve and compare them (the reference, the identity it claims, and the resolution status observed at write time). It never holds a copy that could stand in for host truth. | REQ-002; D3, D4 |
| FA-4 | Workflow definitions and accepted records remain ordinary files owned by their producing deliverables (DEL-02-01/02-02 for workflows; PKG-06 for decisions). This format supplies the act and run records that refer to them; it does not re-home them. | REQ-001, REQ-005 |
| FA-5 | A written act record is not later edited to change its actor, act kind, bound content, scope or purpose. A correction is a new record that names the record it corrects and why; both remain readable. (Proposed; the supersession mechanism is unselected.) | REQ-003, REQ-004 |
| FA-6 | Git history remains the primary change record for the files themselves (D13). A record does not duplicate commit history; where a record's own revision matters, it is cited by the repository's revision identity. | AX-003; V4-OPS-31 |
| FA-7 | Each record identifies its **format version** and **record kind** so a reader can refuse or limit an unknown version rather than guess. | OUT-001 |
| FA-8 | The **recorder** (agent, App component or host facility that wrote the record) is always identified and is never the decision actor merely by having written it. | REQ-003; D10 |
| FA-9 | Record location: runs performed in the App keep records with the user's project/workspace; host-agent runs keep records with the host project (V4-HI-70). Exact folder/path and host persistence are **not** selected here (`UNRESOLVED` U-05, U-06). | REQ-001, REQ-005 |

## 3. Record kinds and identity

| Record kind | What it is the authority for | Produced by |
|---|---|---|
| Run record | That a workflow run occurred with the identified workflow, conversation, model, settings, requested operations and observed outcomes, linking host evidence | App record writer (OUT-002) for App runs; host run recording (external owner, DEP-04-03-016) for host-agent runs, in the shared meaning |
| Human-act record | That an identified person performed an identified act kind on identified content, scope and purpose, with its evidence | Written by a recorder: the App, the host facility, or an agent faithfully recording |
| Decision / accepted record | A PKG-06 or workflow-owned record that an act record may cite as its subject or purpose | Its owning deliverable (DEL-06-01/06-02, DEL-02-02); only consumed here |

Common identity elements (semantic): *record identity*, *record kind*,
*format version*, *recorder identity*, *recording context* (App, or host
identity), *written-at order* (sequence or time as available), *corrects*
(optional reference to a superseded record).

## 4. Run-record inventory

Every element named in REQ-002 / SOW-186 / V4-HI-70 is present. "Required"
means the element must be present **as a value or as an explicit absence
statement**; an omitted element is a defect, never "none".

| # | Element (semantic) | Meaning | Supplier (by accepted meaning) | Absent / unknown handling |
|---|---|---|---|---|
| R1 | Run identity | Stable identity of this run, distinct from conversation and operation identities | Record writer | Required |
| R2 | Workflow identity as observed | Origin (project / user / bundled / host), source root, name, revision of the workflow actually selected and supplied; **promised vs observed** kept separate | DEL-02-01 source-identity meaning; DEL-02-03 execution | If only the selection is known, say so; supply/adoption not inferred from selection |
| R3 | Supplied guidance identity and limits | Role/guidance sources and bytes actually supplied, and where provider adoption/enforcement is unobservable | DEL-02-04 REQ-004 (CASE-002 M2) | "Not observed" stays explicit; no adoption claim |
| R4 | Conversation reference | Reference to the harness conversation/session in which the run occurred | Harness (Codex in App; host loop in host) | Reference only — operational, not authority (D2) |
| R5 | Model used | Model identity and serving endpoint class (local server / user-chosen cloud) **as observed**, separated from configured/requested | Harness/loop reports; DEL-01-01, DEL-05-01 | "Requested X; observed unknown" is a valid value |
| R6 | Autonomy settings | Settings version(s) in force for the run: initial settings and every during-work change, each with state (effective / requested-unestablished / unconfirmed), the person as setting actor, and establishing evidence reference | DEL-04-02 settings-in (§8); policy meaning from DEL-04-01 | Unconfirmed or missing settings recorded as such, never as effective |
| R7 | Requested operations | One entry per requested operation (§5) | Loop/agent request trace; DEL-03-01 identities; DEL-03-02 lifecycle | Required per request made |
| R8 | Checkpoint events | Declared checkpoints reached, waiting state, and — if discharged — the act record that discharged them | DEL-02-01 declaration; DEL-02-03 hold behaviour | A checkpoint without an act record is "waiting" or "not discharged", never discharged |
| R9 | Human acts | References to human-act records (§6) performed within or concerning this run | §6 | No reference is created without an act record |
| R10 | Agent examination findings | References to agent findings (V4-EXM-21) attached to rows/results | Agent output | Findings are **examine**, never a human act |
| R11 | Evidence limits | Explicit list of what the recorder could not observe (lost acknowledgement, missing receipt, unresolvable reference, unobserved adoption) | Record writer | Required, may be empty only if the writer asserts nothing was unobserved |
| R12 | Record identity elements | §3 common elements | Record writer | Required |

## 5. Operation entries and outcome evidence

Each R7 entry (semantic elements): *operation identity and version* (catalog
reference, DEL-03-01); *origin* (agent author type, conversation and run —
V4-HI-21); *relied-on read basis* (workspace identity, generation, model
revision, canonical content identity as cited by the action — V4-HI-11, not a
later queue-time basis, HI §11 limit); *route* (direct under the settings
version in force, or proposal); *proposal reference* where a proposal;
*outcome* (below); *receipt references*; *origin-mark reference*; *standing
received* (V4-HI-12); *settings version governing the route decision*.

Outcome vocabulary is DEL-03-02's (reconciled at V1). The record may state an
outcome only with the evidence in the third column:

| Outcome as recorded | Meaning | Minimum evidence the record must reference | May NOT be inferred from |
|---|---|---|---|
| drafted / validated | Proposal prepared / passed host validation | Host validation result reference (validated) | Agent assertion alone (validated) |
| queued | Host holds the proposal for the person | Host queue acknowledgement | Transport completion |
| accepted | The person accepted the edit in the host | Human-act record, kind **accept an edit** (§6) | Operation success, receipt of a later application, agent statement |
| applied | Host applied the change | Host receipt reference | `success`, queued, accepted |
| applied (direct) | Applied under granted autonomy without a proposal | Host receipt + origin-mark reference + settings version | Absence of error |
| rejected / withdrawn | Person rejected / proposer withdrew | Rejection act record / host withdrawal record | Silence, timeout |
| stale (refused) | Host refused because the basis no longer holds; reason retained | Host refusal with reason | Local basis comparison alone |
| outcome unknown | Outcome could not be observed (applied or not) | The observation gap itself (R11) | — (this is the default when evidence is missing) |

Rules: OE-1 transport success, tool-call return, source resolution or a
resolvable receipt *reference* never upgrades an outcome (REQ-002; V4-EXM-31).
OE-2 a re-drafted proposal after stale refusal is a **new** entry with its own
basis; it does not overwrite the stale entry (V4-HI-23). OE-3 duplicate
submission produces one entry with one effect reference; the mechanism is
DEL-03-02's (unselected).

## 6. Human-act record

### 6.1 Elements (semantic)

| Element | Meaning | Required |
|---|---|---|
| Act identity | Identity of this act record | Yes |
| Act kind | One accepted-basis name (§0); to be reconciled with DEL-04-01 v0.1 | Yes |
| Act class | The operation's policy class at the time (none / may apply / proposal only / reserved) — `UNRESOLVED{OI-001}`; the record carries the adopted value with its decision-basis reference when one exists, otherwise "unresolved" | Yes (value or "unresolved") |
| Decision actor | The person who performed the act | Yes |
| Recorder | The software, host facility or agent that wrote the record | Yes |
| Recording mode | *direct capture* (recorder captured the person's act in its own interface) or *faithful recording* (recorder ≠ capturing surface; records an act evidenced elsewhere) | Yes |
| Bound subject | Identity of what the act concerns (proposal, row set, result, workflow draft, decision record) | Yes |
| Bound content identity | Content identity of the subject at the moment of the act, by an identified identity method | Yes, or "not obtainable" — then lapse state is permanently *unknown* |
| Scope | Which parts of the subject the act covers (e.g. rows 3, 5; whole batch; one file) | Yes |
| Purpose | What the act was for, in the actor's terms (e.g. "accept these rows for application") | Yes |
| Evidence references | Host act record, UI event, receipt, signed file — each with resolution status | At least one |
| Evidence limits | What the evidence does not show | Yes (may be "none known") |
| Relations | Run, operation entry, checkpoint, workflow, decision record | As applicable; **no required prior act** |
| Order | Sequence/time of the act as evidenced | Yes |
| Lapse evaluation | Latest lapse state with the compared identities (§7); derived, re-computable | Derived |

### 6.2 Rules

- HA-1 An act record is written only from evidence that the person performed
  the act. A proposal, an operation success, a permission/autonomy grant, a
  receipt, agent findings, silence or timeout is not such evidence (D5, D10;
  AC-003).
- HA-2 Decision actor and recorder are separate elements even when the same
  surface captured the act; an agent recorder never appears as decision actor
  for a human act kind.
- HA-3 One act record states one act kind. Evidence of **accept an edit**
  never produces **mark checked**, **approve** or **rely**, and vice versa
  (D11). An independently evidenced act (e.g. mark checked on content the
  person edited themselves) is recordable without any accept record (SoW
  REQ-003 last clause).
- HA-4 **rely** and **approve** records name the accountable person and scope
  only as evidenced; the format supplies no certification, sealing or
  code-compliance label (D12; V4-AUT-05).
- HA-5 Setting or changing the autonomy grant is the person's act (DEL-04-02
  CLM-004; V4-HI-40). It is recorded in R6 with the person as setting actor.
  Whether it is also a named act kind is a DEL-04-01 reconciliation point
  (U-08).
- HA-6 Act class values are carried, never computed here; an unresolved class
  is shown as unresolved, never treated as permission (`UNRESOLVED{OI-001}`).

## 7. Content binding and lapse comparison rule

Representation-neutral rule. Notation: *S* bound subject; *c₀* bound content
identity recorded with the act; *m₀* identity method used for c₀; *c₁* current
content identity of the same subject and scope obtained by method *m₁*.

| Step | Rule |
|---|---|
| L-1 | Obtain c₁ for exactly the bound subject and scope — not the workspace generation or model revision (an unrelated edit elsewhere must not lapse a row-bound act). For host content, c₁ comes from the host's read basis (DEL-03-01 canonical content identity); for App files, from the file content identity. |
| L-2 | If m₁ ≠ m₀ or the methods cannot be shown comparable → **unknown (incomparable)**. Never "not lapsed". |
| L-3 | If c₁ cannot be obtained (host unreachable, reference unresolvable) → **unknown (unavailable)**. |
| L-4 | If S no longer exists → **lapsed (subject absent)**. |
| L-5 | If c₁ = c₀ → **not lapsed**: the act remains associated with that same content. |
| L-6 | If c₁ ≠ c₀ → **lapsed**: the act is shown as lapsed for the changed content, retaining c₀, scope and purpose; it is not carried to the new content. |
| L-7 | Scope with several elements (multi-row / batch): evaluate L-1…L-6 per element; if some elements lapse, the act is **partially lapsed**, listing which. Whether the act's purpose survives for unchanged elements is `UNRESOLVED` U-07. |
| L-8 | Lapse never deletes or edits the act record (FA-5). The historical fact "P performed K on c₀" remains true; lapse concerns effectiveness for current content. |
| L-9 | The host may present its own lapse (e.g. SWBPIPE checked tag, V4-HI-32). The record links the host's lapse evidence where supplied; if the App's comparison and the host's disagree, both are shown and the disagreement is an evidence limit, not silently resolved. |

Lapse states: not lapsed · lapsed · lapsed (subject absent) · partially
lapsed · unknown (incomparable) · unknown (unavailable) · not yet evaluated.

## 8. Settings-in / record-out exchange with DEL-04-02 (CASE-002 M3)

Identical in DEL-04-02/AS-v0.1 §6. It is a runtime exchange of data, not an
ordering between human acts and not a second authority.

**Settings-in (DEL-04-02 → DEL-04-03 writer), per run and per change:**
run identity; settings version identity; per operation class — treatment
(direct / propose / class unresolved) and display state (effective /
requested-unestablished / unconfirmed); setting actor (the person); establishing
evidence reference (App control event or host confirmation); order relative to
operation entries; source of control (App or host).

**Record-out (DEL-04-03 reader → DEL-04-02), per run:** record identity and
format version; recorded settings versions with their states; each operation
entry's governing settings version, route, outcome and receipt/origin
references; act records with actor, recorder, kind, scope, purpose and lapse
evaluation; evidence limits.

**Comparison performed by DEL-04-02:** for each settings version, displayed vs
recorded → *match* / *mismatch* / *missing in record* / *missing in display*.
A mismatch is surfaced to the person and returned as a defect observation. The
record is the authority for what was recorded; the control (App or host) is
the authority for the current grant; the display is derived (D2). Neither side
auto-corrects the other.

## 9. Evidence references

Each reference carries: *referenced evidence kind* (receipt, content hash,
origin mark, host act record, commit), *claimed identity*, *resolution status
at write* (resolved / unresolvable / not supplied) and *resolution status at
read* (re-checked by the reader). "Resolved" means the source was found with
the claimed identity; it does not make the referenced change or act more than
the source itself states (OE-1).

## 10. Consumer and host interface

| Consumer | Consumes (meaning) | Supplies back to this format | Held part / limit |
|---|---|---|---|
| PKG-02: DEL-02-01 | Act kind names for checkpoint declarations; checkpoint event (R8) meaning; workflow identity element R2 | Source-identity meaning (origin/root/name/revision; promised vs observed) | V1 reconciliation of R2 with W4 declaration |
| PKG-02: DEL-02-02 | Act records for workflow review and explicit registration (subject = draft content identity; lapse on changed draft) | Draft/registration subject identities | Whether "review/registration" are act kinds: U-08 |
| PKG-02: DEL-02-03 | R8 checkpoint wait/discharge by act reference; R7 unknown outcomes | Hold/replay observations | — |
| PKG-02: DEL-02-04 | R3 supplied guidance identity/limits | Actual supplied bytes/identity/limits (M2) | No adoption claim from supply |
| PKG-03: DEL-03-01 | R7 operation identity; relied-on read basis; c₁ for lapse | Canonical content identity method (m) | Method unselected (DEL-03-01 TBD-003); L-2 applies until then |
| PKG-03: DEL-03-02 | §5 outcome evidence rules | Outcome vocabulary; proposal identity | V1 reconciliation of §5 table |
| PKG-06: DEL-06-01/06-02 | Act records cited by coordination records; faithful presentation with actor ≠ recorder and lapse | Decision records as act subjects | Coordination recorder never becomes actor |
| DEL-04-02 | Record-out (§8); standing inputs: lapse, unknowns, act distinctions | Settings-in (§8) | M3 executable trace needs candidate writer/reader |
| DEL-09-11 | Complete records for the week-later reconstruction by a separate reader | — | This format does not perform the witness |
| DEL-01-02, DEL-01-04, DEL-05-01, DEL-05-02 | R4/R5/R7 meanings; act display | Observation evidence (DEL-01-02 CLM-003) | See finding F-02 |
| External host run recording (DEP-04-03-016; DEP-001) | Shared meaning of §§3–9 to record host-agent runs linking its own receipts | Receipts, origin marks, host act records, host lapse | Adoption and receipt availability unclaimed; OI-013 placement |

## 11. Excluded acts and owners (REQ-006)

Deciding OI-001/OI-002 — Owner with App/SWB contract owners. Defining and
carrying adopted policy — DEL-04-01. Autonomy/standing UI — DEL-04-02.
Reconstruction witness — DEL-09-11. Host domain changes, receipts, domain
storage, host run-recording implementation — responsible host owner (SWBPIPE
outside session). Performing any human act — the person. Professional
reliance/certification judgments — the accountable professional. This format
faithfully records evidenced acts; it performs none of them.

## 12. Examples (fixture subjects — invented; no act was performed)

Fixture model `FX-PIPE-01`, table *Supports*, rows S-101…S-105. Operation
`op:add-support` and `op:adjust-run` are placeholders pending OI-021.

**E1 — Proposal, partial acceptance, application.** Run ⟨run:1⟩, workflow
`project/supports-adjust` revision ⟨rev:w1⟩ (observed = selected), model
"local server, model id as reported", settings version ⟨set:1⟩ effective:
model changes → propose (SWB accepted default, V4-HI-41). R7: proposal
⟨prop:1⟩ for rows S-103…S-105, basis ⟨ws:1, gen:7, rev:m7, cid:b7⟩, outcome
queued (host ack). Act record ⟨act:1⟩: kind **accept an edit**, actor
"fixture engineer", recorder "host acceptance facility", mode direct capture,
subject ⟨prop:1⟩ rows S-103/S-104, c₀ ⟨cid:p1-103,104⟩, purpose "accept these
rows for application". S-105 rejected → ⟨act:2⟩ kind reject (see U-08).
Outcome for S-103/S-104: applied, receipt ⟨rcpt:1⟩ (reference only).
*No* mark-checked, approve or rely record exists or is implied.

**E2 — Faithful recording.** The engineer marked S-102 checked in the host;
the host act record ⟨hact:9⟩ exists. The App agent writes ⟨act:3⟩: kind
**mark checked**, actor "fixture engineer", recorder "App agent", mode faithful
recording, evidence ⟨hact:9⟩ resolved, c₀ ⟨cid:r102a⟩. Valid.

**E3 — Negatives.** (a) Agent drafted ⟨prop:2⟩ only → no act record.
(b) `op:adjust-run` returned success → outcome at most "ran"; no accept record.
(c) Settings ⟨set:2⟩ granted direct application → no act on any content.
(d) Agent examination ⟨find:4⟩ on S-101 → R10 entry, kind examine; no mark
checked. (e) Transcript says "engineer approved" with no evidence → nothing
written; evidence limit noted.

**E4 — Lapse.** After E2, S-102 is edited; host read basis gives
c₁ ⟨cid:r102b⟩ ≠ c₀ → ⟨act:3⟩ lapsed, retaining c₀, scope, purpose. Control:
S-101 edited instead → ⟨act:3⟩ not lapsed (subject-scoped comparison, L-1).
Model revision changed in both cases.

**E5 — Unknown outcome.** Direct `op:add-support` under ⟨set:2⟩; the
acknowledgement is lost. R7 outcome unknown; R11 "application acknowledgement
not observed"; receipt "not supplied". A later read showing a new support row
is recorded as a separate observation with its own basis, not back-filled as
the receipt.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 Act-class values (reserved list) `UNRESOLVED{OI-001}` | Owner with App/SWB contract owners; carried by DEL-04-01 | Before operation-policy production contracts | Act class element carries "unresolved"; no class example is a permission |
| U-02 Routine classifier permissions `UNRESOLVED{OI-002}` | Owner with App/SWB contract owners | Before permission-policy implementation | Routine tool permission is not recorded as a human act; whether it appears in R6 is open |
| U-03 Act-kind names and granularity | DEL-04-01 (v0.1, reconciled at V1) | V1 comparison | §0 names are accepted-basis names, may be renamed |
| U-04 Serialization, field names, content-identity method, record-identity form | DEL-04-03 with DEL-03-01 (TBD-003) and affected consumers | Before OUT-001 CONFIG and writer implementation | L-2 yields *unknown* until methods are identified |
| U-05 Record file location in the App project/workspace | DEL-04-03 with DEL-02-02 / OI-014 owners | Before writer implementation | FA-9 states only "ordinary project/workspace files" |
| U-06 Host persistence/placement of host run records `OI-013` | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Host recording follows the meaning only |
| U-07 Partial-lapse effect on a multi-element act's purpose | DEL-04-01 with Owner; host (SWBPIPE DEC-104 semantics) | Before lapse display criteria are fixed | L-7 reports per-element lapse; no whole-act rule chosen |
| U-08 Whether *reject*, *workflow review/registration* and *autonomy grant/change* are named act kinds | DEL-04-01 (with DEL-02-02, DEL-04-02) | V1 comparison | Recorded as acts with the person as actor; kind naming open |
| U-09 First connected operation `OI-021` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Examples use placeholder operations |
| U-10 Host receipts, origin marks, host act records, host lapse `DEP-001` | SWBPIPE outside implementation session | Before corresponding connected-journey integration/examination and fallback-replacement decision | All host evidence in examples is fixture; nothing received |
| U-11 Shared component placement of reader/writer `OI-014` | App/shared contract owners | Before structural/production contract allocation | No common service assumed |

## Verification cases (designed, not run)

| Case | Input (fixture subject) | Expected result | Serves |
|---|---|---|---|
| VC-01 Authority | E1 run; transcript and derived view both claim an extra acceptance of S-105 | Reader shows only ⟨act:1⟩/⟨act:2⟩; extra claim not an act; session/view marked non-authoritative | VER-001 (AC-001) |
| VC-02 Inventory completeness | E1 run record | R1–R12 each present as value or explicit absence; no element silently omitted | VER-001 (AC-002) |
| VC-03 Link not copy | E1 with ⟨rcpt:1⟩ | Record holds reference, claimed identity, resolution status; no receipt body or domain values reproduced as authority | VER-001 (AC-002) |
| VC-04 Faithful recording | E2 | Actor = engineer, recorder = App agent, mode faithful, evidence resolved | VER-002 (AC-003) |
| VC-05 Fabrication negatives | E3 (a)–(e) | No act records written; (e) produces an evidence-limit entry only | VER-002 (AC-003) |
| VC-06 Independent act | Engineer marks own edit checked, no proposal | ⟨act⟩ mark checked recorded; no accept record required or created | VER-002 (AC-003) |
| VC-07 Lapse and control | E4 both branches | Changed-subject branch lapsed with c₀ retained; unrelated-edit branch not lapsed | VER-003 (AC-004) |
| VC-08 Incomparable / unavailable | E2 with m₁ ≠ m₀; then host unreachable | *unknown (incomparable)*; *unknown (unavailable)*; never not lapsed | VER-003 (AC-004) |
| VC-09 Partial lapse | ⟨act:1⟩ then S-104 edited | Partially lapsed listing S-104; S-103 not lapsed; purpose effect shown as unresolved (U-07) | VER-003 (AC-004) |
| VC-10 Unknown outcome | E5 | Outcome unknown; receipt not supplied; later read not back-filled | VER-004 (AC-005) |
| VC-11 Transport-only | Proposal submitted, transport ok, no host ack | Outcome not queued; unknown or drafted per evidence | VER-004 (AC-005) |
| VC-12 Coverage inventory | VC-01…VC-11 against AC-001…AC-005 | Each AC has ≥1 positive and ≥1 negative case; results name candidate; distinct from DEL-09-11 witness | VER-005 (AC-006) |
| VC-13 Owner trace | §10, §11, UNRESOLVED | Each consumer in REQ-005 and each excluded act in REQ-006 traced one-for-one; no delivery/adoption asserted | VER-006 (AC-007) |
