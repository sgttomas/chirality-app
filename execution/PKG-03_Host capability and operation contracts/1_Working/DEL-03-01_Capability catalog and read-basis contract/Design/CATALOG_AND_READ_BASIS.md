# Capability catalog and read-basis contract
- Contribution: DEL-03-01/C-v0.2
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (catalog and read-basis schema meaning), OUT-002 (three-surface responsibility map skeleton), OUT-003 (designed contract fixtures and the shared fixture catalogue); REQ-001–REQ-007; AC-001–AC-008; VER-001–VER-008
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 179a6d355d84dba915daddd746d9d62eb7c8ef483e68122a096dfbde6f6b3b84; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7d…60da) §§1–3, §5 V4-HI-30–33, §6 V4-HI-40–42, §7, §10 item 3, §11; `P/docs/PRD.md` V4-HOST-03, V4-EXT-01, V4-PAR-01–05, V4-AUT-03–05, V4-SHR-02, §9 OQ-02/OQ-10/OQ-11; `P/docs/ARCHITECTURE.md` V4-ARC-20–21; `P/docs/EXAMINATION.md` V4-EXM-20/21/24/25; DECISION_BRIEF #d2/#d3/#d4/#d5; SCC-CASE-002 Case_Datasheet rows M1-C, M3-CP, M4-X (sha256 6acdc6c4…a71a6); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f3…81f2e) D2/D3; R1_RESOLUTIONS.md (sha256 2f9c7e72…7ec4) R-1–R-9; comparisons V1-A (01811533…4c09), V1-B (09eebfe0…1cae), V1-C (8d46258a…94a6)
- Consumed inputs: DEL-03-02/P-v0.2 (co-revised in this run: change-item content identity, canonical outcome taxonomy, applied-outcome association, M3-CP return); DEL-04-01 policy meaning as fixed by R1_RESOLUTIONS R-1 (canonical act names A1–A14), R-2 (D2/D3 adopted records and derived class values), R-3 (treatment → runtime outcome map) and R-4 (label rule) — DEL-04-01/ACT-POLICY-v0.2 itself not read here (concurrent repair), to be reconciled at V2; DEL-04-03 record semantics referenced for act-field set and lapse vocabulary per V1-B D-14/D-16, by R1 meaning; SWBPIPE host catalog: not supplied (DEP-03-01-025)
- Receivers: DEL-02-01 (OUT-002; REQ-002; VER-002) and PKG-02 via DEP-03-01-022; DEL-02-03 (OUT-001; REQ-001; VER-001); DEL-03-02 (OUT-001, OUT-002; REQ-003; VER-004) via DEP-03-01-023; DEL-03-03 (OUT-001, OUT-003; REQ-001; VER-001); DEL-05-01 (OUT-001, OUT-002; REQ-003; VER-004); DEL-05-02 (OUT-001, OUT-003; REQ-001; VER-001); DEL-09-09 (OUT-001, OUT-002; REQ-001, REQ-005; VER-001, VER-005); DEL-04-03 (content identities, method designation, read basis — unregistered join, V1-B RF-04); DEL-04-02 (standing facets — unregistered join, V1-B RF-05); DEL-03-04 (integrated guide, reads the map); all files citing the §10 shared fixture catalogue (R-9)

## 0. How to read this definition

This is the 60% semantic definition of one host capability catalog and of
the basis every read describes. It fixes meanings, states, sequences, failure
behavior and verification cases. It does **not** select wire field names,
JSON/TypeScript types, MCP versus CLI transport, a hash or canonicalization
algorithm, persistence, process placement or shared-component placement
(TBD-003; OI-014; DEP-03-01-028). Every element name in this file is a
**semantic label**, not a wire name. Where a meaning depends on a host fact
not yet supplied (DEP-03-01-025), it is marked as a host input.

Unruled policy appears only as `UNRESOLVED{OI-nnn}`. It is never a
permission, a default or a pass. Values marked **DERIVED** follow from cited
rules; values marked **INTEGRATION** are R1 integrator choices open to owner
revision (R1_RESOLUTIONS preamble).

Settled distinctions relied on here (cited, not re-decided):

| Id | Settled distinction | Source |
|---|---|---|
| S-C1 | One catalog describes every operation a person can perform, reads and changes alike | V4-HI-01; V4-PAR-01 |
| S-C2 | Human interface, embedded agent and external agent act through that one catalog; equal UI gestures are unnecessary, equal meaning and standing are essential | V4-PAR-02; V4-HOST-03; #d4 |
| S-C3 | Unavailable to the person ⇒ unavailable to the agent, with the same reason | V4-HI-04 |
| S-C4 | Every read returns its basis; a later action cites the basis it relied on; the basis is checked on every change | V4-HI-11; HI §10 item 3 |
| S-C5 | Results carry standing; an agent never presents more confidence than the host gives | V4-HI-12; V4-PAR-03 |
| S-C6 | Operation success means it ran; execution, checking, acceptance, approval and professional reliance are separate acts | V4-HI-25; V4-AUT-03; #d3 |
| S-C7 | Agents never record a human act as performed when it was not; faithful recording (A9) of an actual act is a conformant record shape | V4-HI-31; SoW REQ-005; R-5 |
| S-C8 | A human act binds to the content it concerns and lapses visibly when that content changes | V4-HI-32 |
| S-C9 | The all-actor/no-separate-work extension promise is preserved and undecided | V4-PAR-05; V4-HI-03; OI-003 |
| S-C10 | Reserved to the person (App/shared contracts, first increment): A4 mark checked; A5 accept wherever the active autonomy requires a proposal; A6 approve; A7 rely; A12 set grant and A13 enable external access. No grant widens past a reserved act or a declared checkpoint. The host names and enforces its own list; host adoption is not evidenced | DECISION-1 D2; V4-HI-30; DEP-001 |
| S-C11 | App routine tool-permission and sandbox modes are the user's own Codex setting and govern tool execution only (A14); hosts have no classifier permission mode in the first increment; the SWB default proposal mode applies | DECISION-1 D3; V4-HI-41 |

Act names used below are the canonical R-1 names (A1 propose … A14 answer
tool permission).

## 1. Parties and what this contract does not do

| Party | Contribution relevant here |
|---|---|
| App/shared capability-contract owner (DEL-03-01) | This semantic definition, the responsibility map, contract fixtures and the shared fixture catalogue (§10) |
| Host owner (SWBPIPE outside session for the first host) | Actual catalog, domain objects and truth, tables/results/diagnostics, content identities, availability evaluation, validation/application, receipts, host UI and the offering/recording of human acts (CLM-001) |
| DEL-03-02 | Proposal, validation and outcome meaning; canonical outcome taxonomy (P §9); consumes §§3–7 here |
| DEL-04-01 | Canonical act names, adopted class records (D2/D3), treatment → outcome map; carried into §3 element 8 |
| DEL-04-02 | Autonomy grant display states and standing display; consumes §6 |
| DEL-04-03 | Content-bound human-act and run-record format; consumes §5 content identities and §6 act fields |
| DEL-03-03 / DEL-05-01 / DEL-05-02 | External, embedded and panel receiving; they consume, not redefine, these meanings |
| DEL-09-09 | Extension trace (V4-EXM-24) and joined external witness (V4-EXM-25) |
| The person | Every actual human act |

REQ-007 exclusions are preserved: this contract builds no host catalog,
computes no domain result, validates or applies nothing, produces no receipt
and performs no human act.

## 2. The catalog as a whole

| Semantic element | Meaning | Source / status |
|---|---|---|
| Host identity | Which host application publishes the catalog | V4-HI-01 |
| Catalog edition | An identity for the whole set of entries as published at one time, so a consumer can say which catalog it generated from, offered from or checked against. This is the one semantic name for this element; DEL-05-01 "catalog identity" maps to it (V1-C D-27) | **Proposed**; not a V4-HI-02 field. Serves VER-002/VER-006 candidate recording (F-C6) |
| Entries | One entry per operation a person can perform (reads and changes) | V4-HI-01/02 |

Catalog invariants:

1. **Completeness.** Every operation available to the person in the host
   interface has an entry. An operation reachable by a person but absent from
   the catalog is a parity defect, not an agent restriction (S-C1).
2. **One meaning.** Each surface (§8) presents an entry's meaning without
   changing it. A surface may add rendering (labels, layout, gesture); it may
   not add, drop or weaken preconditions, effects, errors, standing or class.
3. **Operation identity ≠ read basis ≠ content identity.** Entry
   identity/version describe *what the operation is*. The read basis (§5)
   describes *which state a particular read observed*. Subject content
   identities (§5.3) identify *individual objects/rows* within that state.
   None substitutes for another.
4. **Open description (proposed, V1-C AB-09).** Entries, their purpose text
   and their input/result/error schemas are readable by any capable consumer
   without Chirality-specific software, as the external interface already
   requires (V4-HI-50; V4-ARC-21). V4-SHR-02 states this for workflows and
   skills; its extension to catalog descriptors is proposed here (F-C9).
5. **Reserved entries are not hidden.** An entry whose class is *reserved to
   the person* remains described to every consumer. An agent request for it
   yields *not permitted* (§4.1), never *unavailable*, *missing* or *not
   exposed* (V1-C AB-06; R-3 point 4). Whether a loop offers such an entry
   as a callable tool or only as an A8 request is DEL-05-01's, with
   DEL-04-01.

## 3. Catalog entry meaning (REQ-002; V4-HI-02; SOW-157–164)

Each entry carries the eight V4-HI-02 semantic elements plus the exposure
element (R-9). Element names are semantic.

| # | Semantic element | Meaning | Must distinguish | Scope row |
|---|---|---|---|---|
| 1 | Operation identity and operation version | Stable identifier for the operation, and a version that changes when any other element's meaning changes | Identity stays stable across versions; version is not model revision. Only version **equality** is defined; see §3.2 for compatibility | SOW-157 |
| 2 | Purpose | Plain statement of what the operation does, readable by a person and an agent alike; the same text reaches every surface | Purpose is descriptive, not a permission or a claim of result quality | SOW-158 |
| 3 | Input schema | Arguments, their meanings, units where applicable, and which argument identifies the target objects | Target identification is explicit (§4.3); a UI selection is *one way* a person supplies it, not a hidden input | SOW-159 |
| 4 | Availability | Named preconditions, each with an unavailable reason (§4) | Unavailable ≠ error ≠ empty success ≠ not permitted ≠ not exposed | SOW-160, SOW-166 |
| 5 | Effects | Kinds of objects the operation changes, or *none* | *None* ⇒ read (includes non-mutating examinations); any effect ⇒ change, routed through DEL-03-02 | SOW-161 |
| 6 | Result schema including standing | What a successful execution returns, and the standing elements (§6) that accompany it | Result ≠ acceptance; standing is part of the result | SOW-162, SOW-169 |
| 7 | Errors | Every error the operation can return, each with a stable error identity and meaning, including an effect statement (none / partial / unknown) | Error ≠ unavailable. An error raised during application is P §9 *application error*; one whose effect is unobservable routes to P *outcome unknown* | SOW-163 |
| 8 | Human-act / autonomy class | See §3.1 | — | SOW-164 |
| 9 | Exposure per surface | For each of H, E, X (§8): *exposed*, *not exposed on this surface*, or *unagreed* | *Not exposed on this surface* ≠ *missing* (no entry in the catalog edition) ≠ *channel not enabled* (whole channel off). Tied to OI-003 | R-9; V1-C D-09 |

### 3.1 Class element (element 8)

| Sub-element | Meaning |
|---|---|
| Class value | One of: **none**; **may apply within granted autonomy**; **proposal only**; **reserved to the person**; or **policy basis pending** (operation-specific addition awaited under `UNRESOLVED{OI-021}`) |
| Policy record reference | The DEL-04-01 policy-class record and its revision identity, citing its decision basis (for D2/D3: `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`) (V1-A AB-07) |
| Value standing | *adopted* (owner ruling), *DERIVED* (with the rule cited), *accepted default setting* (autonomy setting, not class), or *policy basis pending* |
| Consequence statement | The operation's consequence in DEL-04-01's consequence vocabulary. Vocabulary not yet defined: `UNRESOLVED` (DEL-04-01 with host policy owner, V1-A AB-04) |
| Host adoption | Whether the host has adopted and enforces this value. Not evidenced for SWBPIPE (DEP-001); the host names and enforces its own list (V4-HI-30) |

Class rules:

1. **Reserved-act operations (DERIVED, R-2).** An operation whose effect is
   to perform or record A4, A5, A6, A7, A12 or A13 as the person's act has
   class **reserved to the person** (S-C7 + D2). A10 *reject* is reserved
   wherever A5 is (R-1, DERIVED).
2. **SWB model changes (DERIVED, R-2).** Class **may apply within granted
   autonomy**, derived from V4-HI-41 "the person may widen it", with the
   accepted default setting **propose** (V4-HI-41). Operation-specific
   additions for the first connected operation are pending `OI-021`. This is
   not SWBPIPE adoption (DEP-001).
3. **Acceptance checkpoints force proposal (R-5).** Whatever the class and
   grant, an operation whose result a declared checkpoint requires A5 on is
   treated *propose* (DEL-03-02 §4.4).
4. **No policy basis (R-3 point 5, INTEGRATION).** A class value of *policy
   basis pending* admits no direct application; proposing remains available.
5. **Routine tool permission is not a class value.** A14 and App Codex
   permission/sandbox modes govern App-side tool execution only (S-C11).
   `OI-002` is not a class value; hosts have no classifier mode (D3; V1-A
   D-23).
6. **Reads.** Non-mutating reads and examinations carry class **none** in
   the fixtures as a fixture assumption; the host's adopted assignment
   governs.

### 3.2 Version compatibility (V1-C AB-08, proposed)

Only version equality is defined. No ordering or range is implied by a
version value. A consumer requiring version *v* accepts only *v* unless the
host publishes an explicit **compatibility statement** for the entry (e.g.
"v3 accepts arguments and yields results meaningful to v2 consumers"). The
statement is host-authored; whether hosts provide one is U-C9.

### 3.3 Change-entry extras (for DEL-03-02)

| Semantic element | Meaning |
|---|---|
| Relied-basis requirement | The change must cite the basis it relied on (S-C4); DEL-03-02 defines how |
| Old/new value reporting | Which attributes of affected objects the host view will show as old and new (V4-HI-24), so the proposal can carry them |
| Subject content identity availability | Whether affected objects expose subject content identities (§5.3), which DEL-03-02 change-item content identities and DEL-04-03 lapse rely on |

## 4. Availability and non-success results (REQ-003; V4-HI-02/04; SOW-160, SOW-166)

### 4.1 Distinct non-success results (canonical with P §9)

A request can end, before or instead of execution, in one of the following.
They must never be encoded as one another, and none may be encoded as a
successful empty result. Every one carries the **evaluated basis** where the
host evaluated one (V1-B D-21). DEL-03-02 P §9 carries the proposal/outcome
extensions; DEL-04-03, DEL-05-01 and DEL-05-02 adopt both unchanged (R-7).

| Result | Meaning | Carries |
|---|---|---|
| **Unavailable** | A declared catalog precondition does not hold for this basis and these arguments. The **only** result subject to HI-04 parity | Failed precondition identity; unavailable reason (4.2); evaluated basis |
| **Not permitted** | Available, but the resolved treatment forbids the requested mode for this actor: a reserved act (S-C10), direct application requested without an *effective direct* treatment (never silently converted into a proposal), or a *policy basis pending* class requested directly | Governing treatment; policy record reference (§3.1); evaluated basis. For a reserved act: an A8 *request* is offered (R-3 point 4). Never phrased as unavailability; never cites a classifier (S-C11) |
| **Channel not enabled** | The whole channel is off: external access off unless the person enables it (V4-HI-52); A13 not performed | Channel state; no operation evaluated |
| **Not exposed on this surface** | The entry exists in the catalog edition but is not exposed on the acting surface (element 9) | Entry identity; surface; exposure value |
| **Error** | Evaluation started and a declared error occurred (element 7) | Error identity and meaning; effect statement; evaluated basis |

*Missing* (no entry in the catalog edition) is a discovery finding
(DEL-02-01 required-tool outcome), not a host response.

A denial by the App user's own Codex tool permission (A14) is App-side tool
execution and is not a host outcome (V1-B §5; S-C11).

Treatment is resolved on the **host route**, at validation and again at
application (R-3 point 1). A loop or adapter relays the actor's intent and
does not decide treatment.

### 4.2 Unavailable reason

| Semantic element | Meaning |
|---|---|
| Reason identity | Stable identity for the reason, shared across channels |
| Reason statement | Person-readable text; the same text reaches every channel |
| Failed precondition | Which declared precondition failed |
| Remedy (optional) | What would make it available, stated as a meaning (e.g. "a load case must be identified"), with any gesture phrasing as surface rendering |
| Evaluated basis | The read basis (§5) against which availability was evaluated |

V4-HI-02's example reason ("Select a load case in the model tree first") is
phrased as a UI gesture (F-C4). For channel parity the precondition is
expressed in operation meaning; the gesture is one surface's remedy text.

### 4.3 Selection-dependent preconditions

A person often satisfies a target precondition by selecting in the host UI;
an agent supplies the same target through the input schema. Both evaluate the
same precondition. The resolved target becomes part of the request; a later
selection never changes it (DEL-03-02 no-retargeting).

## 5. Read basis and content identities (REQ-004; V4-HI-11/32; SOW-167)

### 5.1 Read basis descriptor

Every read result carries one basis descriptor with four elements plus the
method designation of its content identity. Semantic labels only.

| Element | Meaning (contract level) | Host input still needed |
|---|---|---|
| Workspace identity | Which host workspace/project the read observed | Host's workspace identity scheme |
| Generation | A **host lineage epoch**: revisions are comparable only within one generation (e.g. a restore, re-import or reopen that starts a new lineage yields a new generation). An ordinary intervening edit does **not** change generation; it changes model revision (R-9) | Host definition (U-C2) |
| Model revision | The revision of the model within that generation that the read observed. Every intervening edit advances it | Host revision scheme |
| Canonical content identity | An identity of the content actually read, by a host canonicalization, so equal content yields equal identity independent of presentation | Algorithm and canonicalization unselected (TBD-003); scope of the read-level identity is a host input (U-C3) |
| Identity method designation | Names the method that produced the content identity, so two identities can be judged comparable (same method) or incomparable | Designation scheme unselected; values host-supplied (R-6; V1-B D-03) |

### 5.2 Rules

1. **All elements, every read.** A read lacking any element is *basis
   incomplete* and cannot be cited as a relied-on basis. Historical reads
   carry the historical revision's basis.
2. **Basis ≠ operation identity** (§2 invariant 3).
3. **Basis is observed, not chosen.** A consumer never fills in, updates or
   copies a later basis over it.
4. **Every non-success result** carries the basis it was evaluated against
   when the host evaluated one (§4.1).
5. **Multi-view reads.** A read returning several views states whether they
   share one basis; if not, each view carries its own descriptor.
6. **Comparability.** Two content identities are comparable only when their
   method designations are the same (or the host states them comparable).
   Otherwise a consumer reports *unknown (incomparable)* (DEL-04-03 L-2),
   never *unchanged* or *changed*.

### 5.3 Subject content identity (R-6; V1-B D-02)

- Each object/row in a read result carries a **subject content identity**:
  host-supplied, per subject, with its method designation.
- It is distinct from the read-level canonical content identity. An edit to
  one row changes that row's subject identity, and the read-level identity,
  but not other rows' subject identities.
- DEL-04-03 L-1 uses it as c₁ for acts on host rows/objects (A4, A6, A7).
  DEL-03-02's change-item content identity is used for A5/A10 (R-6). This is
  how V4-HI-32's "a row's content hash" is received.
- Which attributes a subject identity covers (e.g. whether a support row
  covers its location and stiffness but not a display label) is a host input
  (U-C3).

### 5.4 Citing the relied-on basis in a later action (SOW-168)

- A later action (a change submitted through DEL-03-02, or a non-mutating
  examination that relies on a prior read) carries a **relied-on basis
  reference**: the basis descriptor(s) of the read(s) it actually relied on,
  unchanged.
- The reference points back to a read; it is never recomputed at queue time,
  at acceptance or at application. A host may additionally record the basis
  it observed later as a **separate** element; it never replaces the
  relied-on reference.
- An action relying on several reads cites each. Which cited bases must
  still hold is U-C4.
- How the host decides a cited basis "no longer holds" (any revision change
  vs a change to relied-on content, e.g. by subject identities) is U-C3.
  §5.1 and §5.3 make either rule checkable.
- **Non-mutating operations citing a basis (proposed, V1-B X-07).** A read
  or examination is never refused as *stale*, because nothing is applied.
  Its result carries the basis it was evaluated on. If that differs from the
  cited relied-on basis, the result states both and its standing is
  *historical relative to the cited basis* or *current*, as applicable. Host
  confirmation: U-C10.
- The catalog exposes this association to DEL-03-02 (DEP-03-01-023). Stale
  refusal, re-draft and application behavior belong to DEL-03-02 and are
  *received* here for the M3-CP comparison (§9; DEP-03-01-026).

Receiving risk (HI §11, SWBPIPE at `e548d4cf`): the observed piping
controller path uses a queue-time basis that differs from the original
external inspection basis. Carried unchanged into integration, it would
substitute a later basis for the relied-on one, contrary to rule 3 and
REQ-004. This is a risk for the joined witness (DEL-09-09), not an
assignment to the host.

## 6. Read results and standing (REQ-003, REQ-005; V4-HI-10/12; SOW-069, SOW-169)

### 6.1 Read result content

A successful read returns the same meaningful content the person sees for the
same operation and basis: tables, results and diagnostics, with the same
standing marks (V4-HI-10; V4-PAR-03). Presentation may differ; content,
diagnostics and standing may not be filtered, summarized upward or omitted
for an agent channel. An empty table is a successful read with zero rows
*and* its basis, distinct from every §4.1 result.

### 6.2 Standing elements

Label rule (R-4): unqualified "checked" means only A4 *mark checked*. Host
results say **"host checks passed: ‹named checks›"**. Agent work is
**examination / findings** (A3). "Approval" means only A6.

| Semantic element | Meaning | Must not be strengthened by |
|---|---|---|
| Currency | **current** (describes the workspace's present revision) or **historical** (an earlier revision or superseded result) | Presenting a historical result as current; dropping currency |
| Host checks passed | Each named host check the result passed, **with the basis it was evaluated on**. A check evaluated on an earlier basis is shown as historical | Collapsing to "checked"; implying checks not run; showing an old-basis check as current |
| Known limitations | Host-stated limitations (e.g. solver assumptions, incomplete inputs) | Omitting or softening limitations in an agent summary |
| Human-act evidence (faithfully carried) | References to actual human acts the host has recorded on this content. Carried by reference with at least the DEL-04-03 act field set: act name (R-1), decision actor (the person), recorder, recording mode (direct capture / faithful recording, A9), bound subject, scope, purpose, bound content identity (c₀ with method designation), lapse state, evidence references and evidence limits (V1-B D-16) | Inventing an act; showing a lapsed act as current; attributing an agent finding to the person; showing a row-scoped act as covering a whole table |
| Lapse state | DEL-04-03 vocabulary: not lapsed · lapsed · lapsed (subject absent) · partially lapsed · unknown (incomparable) · unknown (unavailable) · not yet evaluated. *Not yet evaluated* never renders as *not lapsed* (V1-B D-14) | — |
| Agent findings (A3) | Findings authored by an agent, attached by reference (V4-EXM-21), with the agent as author. Where they are held (host-stored, which may be a change, or message content) is U-C5 | Rendering a finding as checked or approved |

Rules:

1. A success value establishes execution only (S-C6).
2. One human act never implies another; no synthetic prerequisite is
   introduced (SoW REQ-005).
3. A faithfully carried act keeps the person as decision actor; the recorder
   is shown separately. Satisfaction of a checkpoint needs attributable
   evidence from the capturing surface (R-5); a carried record cites it.
4. When the bound content changes, the act is shown lapsed (S-C8), judged by
   the subject content identity (§5.3), not by the model revision.
5. Nothing is presented as certified, sealed, approved or code-compliant
   (V4-AUT-05).

## 7. Operation sequences (catalog view)

```text
discover entry (identity, version, purpose, schemas, availability, class, exposure)
  → request read (arguments)          → unavailable | not permitted | channel not enabled
                                        | not exposed on this surface | error   (each with evaluated basis)
  → read result (content, standing, BASIS B, subject content identities)
  → [consumer reasoning; no host state]
  → request change citing relied-on basis B        (DEL-03-02 route)
       host resolves treatment and checks B → P §9 outcomes (refused — stale cites B and current basis;
                                               applied associates proposal/item, B, receipt, resulting revision)
```

Failure behavior at catalog seams:

| Situation | Required behavior |
|---|---|
| Entry version changed between offering/discovery and request | The request carries the entry version it was prepared for. A host-side mismatch is reported as an element 7 error meaning (U-C6), not re-interpreted. A loop may pre-screen for a catalog-edition change before dispatch; that is reported as loop-side, not as a host outcome (V1-C D-13) |
| Read returns without full basis | Consumers mark it *basis incomplete* and do not cite it for a change |
| Lost read response | No content is invented; the consumer re-reads and obtains a new basis. Reads have no effects, so no model outcome-unknown applies |
| Availability evaluated earlier than the request | Availability is re-evaluated at request; the earlier evaluation is historical |

## 8. Three-surface responsibility map — skeleton (OUT-002; REQ-006; SOW-072, SOW-165)

Surfaces: **H** = host human interface; **E** = embedded-agent tools (host
loop, received by DEL-05-01/05-02); **X** = external interface (host-built
MCP server or CLI over the live controller, V4-HI-50/V4-ARC-21; App side
received by DEL-03-03).

Cell values: **generated**, **checked**, **hand-built**, **unagreed**. No
generation or check route has been agreed with the host owner, so every cell
is **unagreed**; the *candidate* column records what #d4 and V4-HI-03 suggest
examining, not a selection.

| Catalog element / concern | H | E | X | Candidate to examine | Producing owner | Receiving point |
|---|---|---|---|---|---|---|
| Entry discovery (identity, version, purpose, open description) | unagreed | unagreed | unagreed | generated for E and X | Host owner | DEL-05-01 tool offering; DEL-03-03 native tool inspection; PKG-02 tool descriptors (DEP-03-01-022) |
| Exposure per surface (element 9) | unagreed | unagreed | unagreed | declared per entry | Host owner | DEL-02-01 required-tool outcome; DEL-05-01; DEL-03-03 |
| Input schema / argument checking | unagreed | unagreed | unagreed | generated or checked for E and X | Host owner | DEL-05-01 REQ-003 (catalog schema before domain validation) |
| Loop-side catalog-schema argument checking (DEL-05-01 candidate (b)) | — | unagreed | — | question held: shared checker or per-host (V1-C D-28) | UNRESOLVED{OI-013}/{OI-014} | DEL-05-01; DEL-10-03 |
| Availability + reason | unagreed | unagreed | unagreed | checked on all three (parity rule) | Host owner | DEL-05-02 panel; DEL-03-03 |
| Effects / affected objects | unagreed | unagreed | unagreed | generated metadata | Host owner | DEL-03-02 target binding |
| Result content + standing | unagreed | unagreed | unagreed | H hand-built views; E/X checked against H meaning | Host owner | DEL-05-02; DEL-04-02; DEL-09-09 VER-002 |
| Errors | unagreed | unagreed | unagreed | generated identities, hand-built texts | Host owner | DEL-03-02 outcome taxonomy |
| Class element | unagreed | unagreed | unagreed | carried from DEL-04-01 records | DEL-04-01 → host | DEL-04-02; DEL-03-03; DEL-05-01 |
| Read basis, subject content identities, method designation | unagreed | unagreed | unagreed | one host producer for all three | Host owner | DEL-03-02; DEL-04-03 L-1/L-2 |
| Proposal views (old/new/objects/reason) | unagreed (host's own views, V4-HI-24) | n/a (agent drafts) | n/a | host-owned presentation; generation route open | Host owner | DEL-03-02 view receiving (DEP-03-02-024) |
| Shared types / components carrying the above | — | — | — | UNRESOLVED{OI-014} | App/shared contract owners | DEL-10-03 account |

Extension promise (OI-003; S-C9): the original promise that a new catalog
operation becomes available to the person and both agents **without separate
work** is preserved and **not claimed**. Its disposition — retain, narrow to
defined generated surfaces, or defer — is `UNRESOLVED{OI-003}`, owned by the
owner with the host contract owner (DEP-03-01-027). Per-surface exposure
(element 9) is where a narrowed promise would be expressed; its values stay
*unagreed* until the ruling. The evidence route is DEL-09-09's V4-EXM-24 trace
(DEP-03-01-030; CASE-002 M4-X). No automatic availability or maintenance
saving is advertised and no narrower criterion is selected.

## 9. Proposal input this catalog needs, and the M3-CP return

Co-developed with DEL-03-02/P-v0.2 (original SCC-CASE-004 pair, carried in
CASE-002).

**Forward (C → P, DEP-03-01-023 / DEP-03-02-016).** C supplies: operation
identity and version; input schema including target identification; effects;
errors with effect statements; the §4.1 results; the read basis descriptor
with method designation; subject content identities; and the relied-on basis
reference meaning (§5.4).

**Proposal input C needs from P** (compared at V1, repaired at R1):

| Needed from DEL-03-02 | P-v0.2 locus |
|---|---|
| Relied-on basis reference carried unchanged from drafting through outcome | P §3.2 |
| Stale refusal reporting the relied-on and current bases, with reason and evaluated basis | P §5, §9 |
| Re-draft as a separately identified proposal citing the new basis, with lineage | P §5 |
| **Applied-outcome association**: proposal/item identity, relied-on basis, host receipt reference, resulting revision. Whether the host receipt *itself* carries the basis is a host observation, not assumed (V1-B D-22) | P §9, §11 |
| Target binding fixed at drafting | P §6 |
| Change-item content identity built from C elements | P §3.1 |

**Return (P → C, M3-CP, DEP-03-01-026).** Distinct from the forward handoff:
DEL-03-02 supplies designed refusal/application behavior and the C/P
read-then-action comparison with an intervening edit (P-v0.2 §11). DEL-03-01
uses it only to compare the basis elements across read, proposal, refusal,
re-draft and applied outcome (VC-C-04). AC-004/VER-004 cannot be claimed
complete until an actual, candidate-bound return exists (V1-B X-08). The
register lacks the DEL-03-02 DOWNSTREAM mirror of DEP-03-01-026 (V1-B RF-08;
routed to closeout C1).

## 10. Shared fixture catalogue — FX-PIPE-01 (R-9; V1-B D-20)

This section is the **one** invented fixture catalogue and revision timeline
for the Wave-1 definitions. Other files cite its entries and steps; where a
fixture must diverge they say why. All material is **invented fixture
subject matter**. Labels (OP-C…, S-…, T…, PR-…, RC-…) are fixture labels,
not operation identities, wire names or SWBPIPE commitments. No SWBPIPE
catalog has been supplied.

### 10.1 Model

FX-PIPE-01: workspace **FX-W1**, generation **g1**. One run **R-100** between
nozzles N-1 and N-2; supports **S-1 … S-4** (S-2 and S-3 rigid at start);
sustained load case **LC-1**. Person: **Engineer A** (invented). Agent: the
host's single agent seat. Workflow: `supports-adjust` (invented; identity per
DEL-02-01 §6.1: kind *workflow*, origin *host*, source root ⟨fx-root⟩, name
`supports-adjust`, revision ⟨rev-3⟩).

### 10.2 Entries

| Fixture | Purpose | Inputs | Availability (precondition → reason) | Effects | Result + standing | Errors (effect) | Class (§3.1) | Exposure H/E/X |
|---|---|---|---|---|---|---|---|---|
| OP-C1 v1 "Read supports table" | Lists supports on a run with type, location, stiffness | run | run exists → "Run not found in this workspace" | none | supports table with a subject content identity per row; currency; host checks passed; limitations | E-invalid-run (none) | none — fixture assumption for reads | unagreed ×3 |
| OP-C2 v1 "Read sustained-load results" | Stresses and support loads for a load case | run, load case | a load case is identified → "A load case must be identified"; a current solve exists → "No current solve for LC-1 at this revision" | none | results table; currency; host checks passed each with evaluated basis; limitation "linear supports assumed" | E-unknown-load-case (none) | none — fixture assumption | unagreed ×3 |
| OP-C3 v1 "Examine support spacing" (non-mutating) | Compares spacing to a stated limit and lists exceedances | run, spacing limit | run exists | none | findings authored by the requester (A3); no human-act standing | E-invalid-limit (none) | none — fixture assumption; findings are not A4 | unagreed ×3 |
| OP-C4 v1 "Add support" | Adds a support at a location on a run | run, location, type | run exists; location on run → "Location is not on run R-100" | supports table, R-100 | new support identity; applied-outcome association | E-location-occupied (none); E-apply-interrupted (unknown) | may apply within granted autonomy — DERIVED (V4-HI-41; R-2); default setting propose; OI-021 additions pending; host adoption not evidenced | unagreed ×3 |
| OP-C5 v1 "Set support stiffness" | Changes a support's stiffness | support, stiffness | support exists | support row | revised row; applied-outcome association | E-invalid-stiffness (none) | as OP-C4 | unagreed ×3 |
| OP-C6 v1 "Mark row checked" | Records the person's A4 on a row's content | row | row exists | checked-state on row | recorded act bound to the row's subject content identity | E-row-changed (none) | **reserved to the person** — DERIVED (R-2 rule; D2a) | unagreed ×3 |
| OP-C7 v1 "Accept proposal items" | Records the person's A5 on one or more change items | proposal, items | items queued | proposal item dispositions | recorded A5 bound to each item's change-item content identity | E-item-not-queued (none) | **reserved to the person** — DERIVED (D2b) | unagreed ×3 |
| OP-C8 v1 "Reject proposal items" | Records the person's A10 | proposal, items | items queued | proposal item dispositions | recorded A10 | E-item-not-queued (none) | **reserved to the person** — DERIVED (R-1 A10) | unagreed ×3 |
| OP-C9 v1 "Set support label" | Changes a support's display label (low consequence) | support, label | support exists | support label | revised label; applied-outcome association | E-label-too-long (none) | as OP-C4 (model change). Used for the direct-branch fixture only | unagreed ×3 |

Grant changes (A12) and enabling external access (A13) are person acts on
host/App controls, not fixture catalog entries here; they are reserved
(S-C10).

### 10.3 Timeline (one revision sequence, generation g1)

Content identities are opaque: ⟨v12⟩ is a read-level identity at r12,
⟨S-2@r12⟩ a subject identity, method designation ⟨m-fx⟩ throughout.

| Step | Revision | Event | Fixture uses |
|---|---|---|---|
| T1 | r12 | State: S-1…S-4 on R-100; LC-1 solved at r12 (host checks passed: "equilibrium", "unit consistency", evaluated at r12) | Baseline |
| T2 | r12 | Engineer A marks row S-2 checked (OP-C6; A4), bound to ⟨S-2@r12⟩, captured by host facility | Standing; lapse later |
| T3 | r12 | Agent reads OP-C1 → basis **B1** = FX-W1/g1/r12/⟨v12⟩/⟨m-fx⟩ | Read basis |
| T4 | r12 | Agent runs OP-C3 examination: span S-2→S-3 exceeds limit | Agent findings (A3) |
| T5 | — | Agent drafts **PR-1** relying on B1: item 1 add guide support at 4.2 m on R-100 (OP-C4); item 2 S-3 stiffness rigid → 2.0e6 N/m (OP-C5) | Proposal draft |
| T6 | r13 | Engineer A edits S-3 stiffness in the host UI (intervening edit). ⟨S-3⟩ changes; ⟨S-2@r12⟩ unchanged; LC-1 results become historical (no current solve at r13) | Intervening edit; unrelated-edit control for T2 |
| T7 | r13 | Agent submits PR-1 → **refused — stale**: relied B1, current **B2** = FX-W1/g1/r13/⟨v13⟩/⟨m-fx⟩, reason "S-3 changed since r12" | Stale refusal |
| T8 | r13 | Any channel requests OP-C2 for LC-1 → **unavailable**, reason "No current solve for LC-1 at this revision", evaluated basis B2 | Unavailable parity |
| T9 | r13 | Agent re-reads OP-C1 (B2) and drafts **PR-2** (lineage PR-1, stale): item 1 add support (old: none); item 2 S-3 stiffness (old: value at r13) → 2.0e6 N/m | Re-draft |
| T10 | r13 | PR-2 validated → **queued** | Queued ≠ applied |
| T11 | r13 | Engineer A accepts item 1 (OP-C7; A5 bound to item-1 change-item content identity) and rejects item 2 (OP-C8; A10) | Item-level acts |
| T12 | r14 | Host applies item 1 → receipt **RC-1**; applied-outcome association PR-2/item 1/B2/RC-1/r14. A5 on item 1 is **not** lapsed by its application | Applied; no lapse on application |
| T13 | r14 | Acknowledgment of T12 lost; agent resubmits PR-2 (same proposal identity) → repeat reports RC-1, or **outcome unknown** (observer: agent/loop) if unobservable | One effect; retry keeps identity |
| T14 | r15 | Engineer A edits S-2 stiffness → T2's A4 on S-2 **lapsed** (⟨S-2⟩ changed) | Lapse |
| T15 | r15 | Engineer A performs A12: grant *direct* for OP-C9 class scope "support labels on R-100"; host control confirms → display state *effective, direct* | Grant change (reserved act) |
| T16 | r16 | Agent applies OP-C9 directly (label S-4 "G-4") → receipt RC-2, origin mark, undo route; no acceptance recorded | Direct branch |
| T17 | r17 | Engineer A undoes RC-2 via the host undo route → a change through the one route, receipt RC-3 "reverses RC-2" | Undo |
| Tg | g2/r1 | (Separate branch) Workspace restored from an archive: new generation g2. Any basis from g1 is incomparable by revision; lapse and stale evaluation under generation change is U-C2/X-05 | Generation change |

### 10.4 Read basis vs operation identity

| Read | Operation (identity/version) | Basis |
|---|---|---|
| T3 | OP-C1 v1 | FX-W1 / g1 / r12 / ⟨v12⟩ / ⟨m-fx⟩ |
| T9 | OP-C1 v1 (same operation) | FX-W1 / g1 / r13 / ⟨v13⟩ / ⟨m-fx⟩ — different basis |
| hypothetical | OP-C1 **v2** (entry revised) | FX-W1 / g1 / r13 / ⟨v13⟩ — different operation version, same basis |

### 10.5 Unavailable example (T8, three channels)

Person (H), embedded agent (E) and external agent (X) each request OP-C2 for
LC-1 at r13. Expected on all three: *unavailable*; failed precondition
"current solve exists"; reason identity R-no-current-solve; same statement;
evaluated basis B2. Not acceptable: an empty results table, a generic error,
or the r12 result without historical currency. If X's channel is off, X
instead gets *channel not enabled* (a separate case).

### 10.6 Standing example (T12–T14)

OP-C2 after a new solve at r14 (hypothetical): currency current; host checks
passed "equilibrium", "unit consistency" evaluated at r14; limitation
"linear supports assumed". Row S-2 at r14 carries T2's A4 (actor Engineer A,
recorded by host, direct capture, bound ⟨S-2@r12⟩): **not lapsed** (T6 edited
S-3 only). At r15 (T14) it is shown **lapsed**. T4's finding is shown as an
agent finding, never as checked.

## Changes from v0.1

v0.1 = C-v0.1 (sha256 c13518c9…0b72, 423 lines).

| V1 / R1 item | Change |
|---|---|
| R-1 (V1-A D-01) | Canonical act names A1–A14 used throughout |
| R-2; V1-A D-02, D-03, D-23; V1-B D-08, §5 rows | §3.1 class sub-elements; D2/D3 as adopted; reserved-act operations reserved (OP-C6/C7/C8); SWB model change *may apply within granted autonomy* DERIVED with default propose, OI-021 pending; `OI-002` removed as a class value; S-C10/S-C11 added |
| R-3; V1-A D-05 | §4.1 *not permitted* per the outcome map (never silently converted; A8 request for reserved acts; policy basis pending → propose only); treatment resolved on host route |
| V1-A D-04 | Channel-off kept as *channel not enabled*, distinct from unavailable (C unchanged in meaning; confirmed) |
| R-4; V1-A D-12; V1-B D-15 | §6.2 label rule: "host checks passed" with per-check evaluated basis; OP-C3 renamed "Examine…"; A3 findings |
| R-5 | Class rule 3: acceptance checkpoint forces proposal; §6.2 rule 3 capturing-surface evidence |
| R-6; V1-B D-02, D-03 | §5.1 identity method designation; §5.3 subject content identity; §5.2 rule 6 comparability |
| R-7 | §4.1 declared canonical with P §9; evaluated basis on every non-success (V1-B D-21); element 7 effect statement and *application error* routing (V1-B D-05) |
| R-9; V1-C D-09 | Element 9 exposure per surface; *not exposed on this surface* result; *missing* distinguished |
| R-9; V1-C D-10 | Fixture workflow carries full identity {kind, origin, source root, name, revision} (§10.1) |
| R-9; V1-C D-14 | Generation defined as host lineage epoch; intervening edit changes model revision; Tg branch fixture |
| R-9; V1-B D-20 | §10 rebuilt as the shared FX-PIPE-01 catalogue with one timeline (T1–T17, Tg); S-2/S-3 contradiction removed; OP-C5 redefined as "Set support stiffness" to match the stiffness item (v0.1 "Adjust run node elevation" had no fixture use); OP-C7/C8/C9 added; fixture proposals renamed PR-1/PR-2 |
| V1-A AB-04 | Consequence statement sub-element (vocabulary UNRESOLVED) |
| V1-A AB-07 | Policy record reference with revision identity |
| V1-B D-14, D-16 | §6.2 act field set and lapse vocabulary by DEL-04-03 reference |
| V1-B D-19 | Evidence labels aligned: *illustrative*, *test-double*, *actual host* (mapping in Verification cases) |
| V1-B D-22 | §9 applied-outcome association; receipt content not assumed |
| V1-B X-07 | §5.4 non-mutating operations citing a basis are not refused as stale (proposed; U-C10) |
| V1-C D-13, D-27 | "Catalog edition" is the one name; version-mismatch handling split host error vs loop pre-screen (§7) |
| V1-C D-15 | Agent-finding location routed to U-C5 (§6.2) |
| V1-C D-28 | Map row for loop-side catalog-schema argument checking held as a question |
| V1-C AB-06 | §2 invariant 5: reserved entries not hidden; request → not permitted + A8 |
| V1-C AB-08 | §3.2 version compatibility: equality only; host compatibility statement proposed |
| V1-C AB-09 | §2 invariant 4 open description (proposed) |
| V1-B X-05 | Restore/generation lapse recorded as open (U-C2, Tg) |
| V1-B X-08; RF-08 | AC-004 held; missing mirror row noted for C1 |

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-021}` operation-specific reserved additions; first connected operation, autonomy, environment | Owner via outside SWB session and App/shared owner | Before connected SoW / live examination | Class values for OP-C4/C5/C9 carry "OI-021 additions pending"; all examples invented |
| `UNRESOLVED{OI-003}` retain / narrow / defer extension promise | Owner with host contract owner (DEP-03-01-027); trace from DEL-09-09 (DEP-03-01-030) | Before claiming extension or fixing AC-007 criterion | Map (§8) and exposure element stay *unagreed*; promise preserved, not claimed |
| `UNRESOLVED{OI-014}` shared contract/component placement | App/shared contract owners | Before structural/production allocation | Map rows for shared types and loop-side checking left open |
| `UNRESOLVED{OI-013}` per-host loop placement (loop-side argument checking) | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary | §8 row held as a question |
| Host adoption of D2 list and D3 rule | Host owner / SWBPIPE (DEP-001) | Before host conformance | Class values are App/shared; host adoption column "not evidenced" |
| Consequence vocabulary (V1-A AB-04) | DEL-04-01 with host policy owner | Before class assignment for connected operations | §3.1 consequence statement empty |
| U-C1 Serialization, content-identity algorithm, method-designation scheme, catalog/schema placement, adapter realization (TBD-003) | App/shared capability-contract owner with host/consumer owners (DEP-03-01-028) | Before dependent schema implementation/conformance | All element names semantic; identities opaque |
| U-C2 Host definition of generation; lapse/stale under generation change and restore (V1-B X-05) | Host owner (DEP-03-01-025) with DEL-04-03 | Before basis conformance, lapse display criteria | Tg fixture only; no rule selected |
| U-C3 Rule for "basis no longer holds"; scope of read-level and subject content identities | Host owner with DEL-03-02 / DEL-03-01 | Before stale behavior and lapse conformance | Both rules checkable; neither selected |
| U-C4 Multi-read reliance: which cited bases must hold | Host owner with DEL-03-02 | Before stale implementation | §5.4 requires citing each |
| U-C5 Where agent findings are held; whether host-stored findings are a change (V1-C D-15) | Host owner | Before V4-EXM-21 fixture binding | OP-C3 shown as read with requester-authored findings |
| U-C6 Host behavior on entry-version mismatch | Host owner | Before adapter implementation | §7 requires explicit error meaning |
| U-C7 Actual host catalog, tables, diagnostics, availability, content identities | Host owner / SWBPIPE (DEP-03-01-025; DEP-001) | Before host conformance claim | Examples invented |
| U-C8 Actual M3-CP executable return (V1-B X-08); DEL-04-01 v0.2 reconciliation | DEL-03-02; DEL-04-01 | V2 comparison; AC-004 closure | AC-004 held |
| U-C9 Whether hosts publish version compatibility statements | Host owner with DEL-02-01 | Before DEL-02-03 required-tool fixtures | Equality only until then |
| U-C10 Host confirmation of non-mutating basis handling (§5.4) | Host owner | Before V4-EXM-21 binding | Proposed rule only |
| Register: missing DEL-03-02 mirror of DEP-03-01-026; unregistered C → DEL-04-02/04-03 joins; C → DEL-05-01/05-02 mirrors (V1-B RF-04/05/08; V1-C RF-1) | Register owner at closeout C1 | C1 | None on content; listed receivers include them |

## Verification cases

Designed, **not run**. Evidence labels at execution (V1-B D-19):
*illustrative* (design tables), *test-double* (App-side fixture or adapter
against a simulated host; v0.1 "schema fixture"/"adapter result"), *actual
host* (candidate-bound host observation). Fixture steps refer to §10.3.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-C-01 Entry field coverage | For OP-C1…C9 and a real host entry when supplied, check the nine §3 elements, §3.1 sub-elements and §3.3 extras against V4-HI-02, SOW-157–164 and R-2 | Every element present; class shows adopted/DERIVED value with policy record reference, or *policy basis pending (OI-021)*; OP-C6/C7/C8 reserved; no OI-002 value; exposure values present (may be *unagreed*) | VER-001 |
| VC-C-02 Cross-channel read parity | OP-C1 at T3 via H, E, X; compare content, subject identities, diagnostics, standing | Identical meaning and standing; mismatches listed; evidence labeled; type match alone does not close a consumer claim | VER-002 |
| VC-C-03 Non-success parity and separation | T8 on H, E, X; plus separate runs: X with channel off; OP-C6 requested by agent; OP-C1 on a surface where not exposed | T8: same *unavailable*, reason identity, statement, evaluated basis B2 on all three; channel-off → *channel not enabled*; OP-C6 by agent → *not permitted* + A8 request, citing reserved class and policy record; not-exposed → *not exposed on this surface*; none is an empty success | VER-003 |
| VC-C-04 Read-to-action basis trace (M3-CP receiver) | T3 → T5 → T6 → T7 → T9 → T10 → T11 → T12 → T13 using P-v0.2 §11 | All elements incl. method designation at every read; PR-1 reference = B1 throughout; refusal shows B1 and B2; PR-2 new identity citing B2; applied-outcome association PR-2/item 1/B2/RC-1/r14; whether RC-1 itself carries B2 recorded as a host observation; no step rewrites a reference; U-C1–U-C4 named | VER-004 |
| VC-C-05 Standing, attribution and lapse | T2, T4, T6, T12, T14 | T2 A4 carried with actor, recorder, recording mode, subject, scope, purpose, c₀; not lapsed after T6 (unrelated edit control); lapsed after T14; A5 on item 1 not lapsed by T12; T4 finding never shown as checked; "host checks passed" each with evaluated basis; no act inferred from success | VER-005 |
| VC-C-06 Responsibility map review | Walk §8 against H/E/X, CLM-001–003 and receiving rows (PKG-02, DEL-03-02, DEL-04-01, DEL-04-02, DEL-04-03) | Each cell valued; no *generated/checked* without a conformance route; host implementation external; no type-compatibility pass | VER-006 |
| VC-C-07 Extension treatment | Compare §8 extension text and element 9 with V4-PAR-05, V4-HI-03, #d4, OI-003, V4-EXM-24 | Promise stated; `UNRESOLVED{OI-003}` with owner; trace route via DEL-09-09; no automatic availability/savings; exposure values *unagreed* | VER-007 |
| VC-C-08 Boundary and open-input audit | Check each REQ-007 exclusion and each UNRESOLVED row; check DERIVED/INTEGRATION markings against R1_RESOLUTIONS | Every excluded act maps to its owner; each open input has owner, point of need, effect; no host delivery, SWBPIPE adoption of D2, or joined qualification claimed | VER-008 |
