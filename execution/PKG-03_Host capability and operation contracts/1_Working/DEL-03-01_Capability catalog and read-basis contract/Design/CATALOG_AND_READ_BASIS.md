# Capability catalog and read-basis contract
- Contribution: DEL-03-01/C-v0.3
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (catalog and read-basis schema meaning), OUT-002 (three-surface responsibility map skeleton), OUT-003 (designed contract fixtures and the shared fixture catalogue); REQ-001–REQ-007; AC-001–AC-008; VER-001–VER-008
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 179a6d355d84dba915daddd746d9d62eb7c8ef483e68122a096dfbde6f6b3b84; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7d…60da) §§1–3, §5 V4-HI-30–33, §6 V4-HI-40–42, §7, §10 item 3, §11; `P/docs/PRD.md` V4-HOST-03, V4-EXT-01, V4-PAR-01–05, V4-AUT-03–05, V4-SHR-02, §9 OQ-02/OQ-10/OQ-11; `P/docs/ARCHITECTURE.md` V4-ARC-20–21; `P/docs/EXAMINATION.md` V4-EXM-20/21/24/25; DECISION_BRIEF #d2/#d3/#d4/#d5; SCC-CASE-002 Case_Datasheet rows M1-C, M3-CP, M4-X (sha256 6acdc6c4…a71a6); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f3…81f2e) D2/D3; R1_RESOLUTIONS.md (sha256 2f9c7e72…7ec4) R-1–R-9; R2_RESOLUTIONS.md (sha256 77cfb845…d088) R2-1–R2-21; comparisons V1-A (01811533…4c09), V1-B (09eebfe0…1cae), V1-C (8d46258a…94a6); reviews IR1-A (31b3c7f8…8284), IR1-B (70e4a4f6…2846), IR1-C (295e96b3…26b9)
- Consumed inputs: DEL-03-02/P-v0.3 (co-revised in this run: change-item content identity, canonical outcome taxonomy, applied-outcome association with resulting objects, retry precedence, item-left events, M3-CP return); sibling v0.2 texts read from commit `28bd00499` where an R2 ruling touches a join — DEL-04-01/ACT-POLICY-v0.2 `ACT_AND_POLICY_CONTRACT.md` (sha256 e50f1fe2…93a9: §2.1 act names, §5.1–§5.3 class vocabulary and resolution order, §6 outcome map, §8.1 decision-standing values, §8.3 records), DEL-04-03/RS-v0.2 `RECORD_SEMANTICS.md` (sha256 56a3f839…1c69: §7 L-1–L-12 and lapse states), DEL-05-01/LOOP-v0.2 `LOOP_RECEIVING_CONTRACT.md` (sha256 1151d432…62c9: §6.2 dispatch record, §12 evidence labels), DEL-02-01/WD-v0.2 `WORKFLOW_DECLARATION.md` (sha256 c25bccc5…a55c: §4.3.7, §4.4 promised standing), DEL-05-02/PANEL-v0.2 (sha256 0a8a0dbe…a700; evidence-label lines only), DEL-04-02/AS-v0.2 (F9 row only, grep); SWBPIPE host catalog: not supplied (DEP-03-01-025)
- Receivers: DEL-02-01 (OUT-002; REQ-002; VER-002) and PKG-02 via DEP-03-01-022; DEL-02-03 (OUT-001; REQ-001; VER-001); DEL-03-02 (OUT-001, OUT-002; REQ-003; VER-004) via DEP-03-01-023; DEL-03-03 (OUT-001, OUT-003; REQ-001; VER-001); DEL-05-01 (OUT-001, OUT-002; REQ-003; VER-004); DEL-05-02 (OUT-001, OUT-003; REQ-001; VER-001); DEL-09-09 (OUT-001, OUT-002; REQ-001, REQ-005; VER-001, VER-005); DEL-04-03 (content identities, method designation, read basis — unregistered join, V1-B RF-04); DEL-04-02 (standing facets — unregistered join, V1-B RF-05); DEL-04-01 (fixture re-pointing); DEL-03-04 (integrated guide, reads the map); every file citing the §10 shared fixture catalogue (R-9; R2-21)

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
rules; **INTEGRATION** values are R1/R2 integrator choices open to owner
revision; **PROPOSED** values are this contribution's proposals. Owner
rulings are credited only with what they say (R2-11).

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
| S-C10 | Reserved to the person (App/shared contracts, first increment), **adopted** by D2: A4 mark checked; A5 accept wherever the active autonomy requires a proposal; A6 approve; A7 rely; A12 changing the autonomy grant; A13 enabling external-agent access. No grant widens past a reserved act or a declared checkpoint. The host names and enforces its own list; host adoption is not evidenced. **DERIVED**: A10 reject is reserved wherever A5 is (R-1). **INTEGRATION**: disabling external access is also a person's A13 (R2-3) | D2; R-1; R2-3; V4-HI-30; DEP-001 |
| S-C11 | **Adopted** by D3: App routine tool-permission and sandbox modes remain the user's own Codex setting per project/turn, govern tool execution only (A14) and never stand in for a reserved or professional act; hosts have no classifier permission mode in the first increment; the SWB default proposal mode applies. The App-side restriction on answering A14 is R-2 INTEGRATION, not D3 | D3; R-2; R2-11; V4-HI-41 |

Act names used below are the canonical R-1 names (A1 propose … A14 answer
tool permission), as carried by DEL-04-01 §2.1.

## 1. Parties and what this contract does not do

| Party | Contribution relevant here |
|---|---|
| App/shared capability-contract owner (DEL-03-01) | This semantic definition, the responsibility map, contract fixtures and the shared fixture catalogue (§10) |
| Host owner (SWBPIPE outside session for the first host) | Actual catalog, domain objects and truth, tables/results/diagnostics, content identities, exposure, availability evaluation, validation/application, receipts, host UI and the offering/capture/recording of human acts (CLM-001) |
| DEL-03-02 | Proposal, validation and outcome meaning; canonical outcome taxonomy (P §9); consumes §§3–7 here |
| DEL-04-01 | Canonical act names, class vocabulary and records (D2/D3; P-01…P-06), treatment → outcome map; carried into §3 element 8 |
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
| Catalog edition | An identity for the whole set of entries as published at one time, so a consumer can say which catalog it generated from, offered from or checked against. The one semantic name for this element; DEL-05-01 "catalog identity" maps to it (V1-C D-27) | **PROPOSED**; not a V4-HI-02 field. Serves VER-002/VER-006 candidate recording (F-C6) |
| Entries | One entry per operation a person can perform (reads and changes) | V4-HI-01/02 |

Catalog invariants:

1. **Completeness.** Every operation available to the person in the host
   interface has an entry — including undo (§10 OP-C10) and any host check a
   person can run. An operation reachable by a person but absent from the
   catalog is a parity defect, not an agent restriction (S-C1).
2. **One meaning.** Each surface (§8) presents an entry's meaning without
   changing it. A surface may add rendering (labels, layout, gesture); it may
   not add, drop or weaken preconditions, effects, errors, standing or class.
3. **Operation identity ≠ read basis ≠ content identity.** Entry
   identity/version describe *what the operation is*. The read basis (§5)
   describes *which state a particular read observed*. Subject content
   identities (§5.3) identify *individual objects/rows* within that state.
   None substitutes for another.
4. **Open description (PROPOSED, V1-C AB-09).** Entries, their purpose text
   and their input/result/error schemas are readable by any capable consumer
   without Chirality-specific software, as the external interface already
   requires (V4-HI-50; V4-ARC-21). V4-SHR-02 states this for workflows and
   skills only; its extension to catalog descriptors is proposed (F-C9).
5. **Class never implies exposure (R2-4; IR1-B B-M4).** Exposure is element 9,
   a host-declared per-surface fact independent of class. Class alone never
   produces *unavailable*, *missing* or *not exposed on this surface*.
   **Reserved entries are always described and, where exposed, offered**;
   they are never withheld for a class reason. An agent call to a reserved
   entry returns **not permitted** and *offers* an A8 request; no A8 is
   recorded unless the agent actually issues it (IR1A-10). Loops and adapters
   never withhold an exposed entry on their own reading of its class (LOOP
   TL-5).

## 3. Catalog entry meaning (REQ-002; V4-HI-02; SOW-157–164)

Each entry carries the eight V4-HI-02 semantic elements plus the exposure
element (R-9). Element names are semantic.

| # | Semantic element | Meaning | Must distinguish | Scope row |
|---|---|---|---|---|
| 1 | Operation identity and operation version | Stable identifier for the operation, and a version that changes when any other element's meaning changes | Identity stays stable across versions; version is not model revision. Only version **equality** is defined (§3.2) | SOW-157 |
| 2 | Purpose | Plain statement of what the operation does, readable by a person and an agent alike; the same text reaches every surface | Purpose is descriptive, not a permission or a claim of result quality | SOW-158 |
| 3 | Input schema | Arguments, their meanings, units where applicable, and which argument identifies the target objects | Target identification is explicit (§4.3); a UI selection is *one way* a person supplies it, not a hidden input | SOW-159 |
| 4 | Availability | Named preconditions, each with an unavailable reason (§4) | Unavailable ≠ error ≠ empty success ≠ not permitted ≠ not exposed. See §4.4 for precondition vs validation error | SOW-160, SOW-166 |
| 5 | Effects | Kinds of objects the operation changes, or *none* | *None* ⇒ read (includes non-mutating examinations and host checks); any effect ⇒ change, routed through DEL-03-02 | SOW-161 |
| 6 | Result schema including standing | What a successful execution returns, and the standing elements (§6) that accompany it | Result ≠ acceptance; standing is part of the result | SOW-162, SOW-169 |
| 7 | Errors | Every error the operation can return, each with a stable error identity and meaning, including an effect statement (none / partial / unknown) | Error ≠ unavailable. An error at validation is P §9 *refused — invalid*; during application it is *application error*; one whose effect is unobservable routes to *outcome unknown* | SOW-163 |
| 8 | Human-act / autonomy class | §3.1 | — | SOW-164 |
| 9 | Exposure per surface | For each of H, E, X (§8): *exposed*, *not exposed on this surface*, or *unagreed*. Host-declared | Independent of class (§2 inv. 5). *Not exposed on this surface* ≠ *missing* ≠ *channel not enabled*. Tied to OI-003 | R-9; V1-C D-09 |

### 3.1 Class element (element 8)

| Sub-element | Meaning |
|---|---|
| Class value | One of five (R2-1): **none**; **may apply within granted autonomy**; **proposal only**; **reserved to the person** — the four V4-HI-02 values (vocabulary SETTLED by V4-HI-02) — and **no policy basis** (INTEGRATION, R-3.5/R2-1) |
| No-policy-basis reason | Present only with *no policy basis*: **omitted** (no class stated), **unassigned** (stated but no policy record), or **pending OI-021** (operation-specific addition awaited under `UNRESOLVED{OI-021}`) |
| Policy record reference | The DEL-04-01 policy-class record (e.g. P-01…P-06) and its policy revision identity, citing its decision basis (for D2/D3: `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`) (V1-A AB-07) |
| Value standing | Mirrors DEL-04-01 §8.1 *decision standing* (IR1-B B-m12): settled-by-basis · adopted decision · DERIVED · accepted default (host adoption unevidenced) · INTEGRATION · `UNRESOLVED{…}` |
| Consequence statement | The operation's consequence in DEL-04-01's consequence vocabulary. Vocabulary not yet defined: `UNRESOLVED` (DEL-04-01 U-02 with host policy owner) |
| Host adoption | Whether the host has adopted and enforces this value. Not evidenced for SWBPIPE (DEP-001); the host names and enforces its own list (V4-HI-30) |

Class rules:

1. **Act-performing operations are reserved (R2-2, DERIVED).** An operation
   that *performs* A4, A5, A6, A7, A10, A12 or A13 — including one that
   changes the host's own act state — is **reserved to the person** (S-C7 +
   D2; DEL-04-01 P-02 with A10 added). No faithful record (A9) is made
   through such an operation. A host-offered faithful-record operation, if
   any, must: not change act state; cite capture evidence; never satisfy a
   checkpoint; take ordinary policy. Whether any host offers one is a DEP-001
   relay question (U-C11).
2. **SWB model changes (DERIVED, R-2; DEL-04-01 P-03).** Class **may apply
   within granted autonomy**, derived from V4-HI-41 "the person may widen
   it", with the accepted default setting **propose**. Operation-specific
   additions are pending `OI-021`. Not SWBPIPE adoption (DEP-001).
3. **Acceptance checkpoints force proposal (R-5; R2-12).** Whatever the class
   and grant, an operation whose result a declared checkpoint requires A5 on
   is treated *propose* for that run; a direct request is *not permitted*,
   naming the governing checkpoint constraint (P §3.3, §4.4).
4. **No policy basis (R2-1, R2-9; DEL-04-01 P-06, INTEGRATION).** Direct
   application is **not permitted**; proposing is available but confers no
   permission — any effect requires the person's A5 and host application. An
   A12 that would widen such a class to direct is **refused** (reason: no
   policy basis). Dependent production stays held (SoW REQ-004 hold); fixtures
   report such cases as **held**, never as passes.
5. **Routine tool permission is not a class value.** A14 and App Codex
   permission/sandbox modes govern App-side tool execution only (S-C11).
   `OI-002` is not a class value; hosts have no classifier mode (D3; V1-A
   D-23).
6. **Reads and host checks.** Non-mutating reads, examinations and host
   checks carry class **none** in the fixtures as a fixture assumption
   (value standing: INTEGRATION for fixtures only); the host's adopted
   assignment governs. DEL-04-01 §5.3 rule 8 cautions that *none* does not by
   itself imply no effect.

### 3.2 Version compatibility (V1-C AB-08, PROPOSED)

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
| Subject content identity availability | Whether affected objects expose subject content identities (§5.3), which DEL-03-02 change-item content identities, the per-item basis check (R2-13) and DEL-04-03 lapse rely on |
| Resulting-object reporting | Whether the applied outcome identifies created/changed objects and their post-application subject content identities (R2-14; P §9) |

## 4. Availability and non-success results (REQ-003; V4-HI-02/04; SOW-160, SOW-166)

### 4.1 Distinct non-success results (canonical with P §9)

A request can end, before or instead of execution, in one of the following.
They must never be encoded as one another, and none may be encoded as a
successful empty result. Every one carries the **evaluated basis** where the
host evaluated one (V1-B D-21). DEL-03-02 P §9 carries the proposal/outcome
extensions; DEL-04-03, DEL-05-01 and DEL-05-02 adopt both **as of C-v0.3 /
P-v0.3** unchanged (R-7).

| Result | Reporter | Meaning | Carries |
|---|---|---|---|
| **Unavailable** | Host | A declared catalog precondition (element 4) does not hold for this basis and these arguments. The **only** result subject to HI-04 parity | Failed precondition identity; unavailable reason (4.2); evaluated basis |
| **Not permitted** | Host | Available and exposed, but the resolved treatment forbids the requested mode for this actor: a reserved act (S-C10); direct application requested without an *effective direct* treatment (never silently converted into a proposal); a *no policy basis* class requested directly; or a governing checkpoint constraint forcing *propose* (R2-12) | Governing treatment (policy record reference, or the checkpoint constraint); evaluated basis. For a reserved act or a checkpoint wait: an A8 request is *offered*, not recorded automatically. Never phrased as unavailability; never cites a classifier (S-C11) |
| **Channel not enabled** | Host (or App adapter observing the host's disabled state) | The whole channel is off: external access off unless the person enables it (V4-HI-52); A13 not performed | Channel state; no operation evaluated |
| **Not exposed on this surface** | **Host-reported** from the per-surface exposure element 9 (R2-4); relayed by loop/adapter | The entry exists in the catalog edition and element 9 says it is not exposed on the acting surface | Entry identity; surface; exposure value. A loop or adapter **relays** a host-returned *not exposed*, naming the host as reporter; it never originates it. The loop-side *not offered* failure is separate (below) |
| **Error** | Host | Evaluation started and a declared error occurred (element 7) | Error identity and meaning; effect statement; evaluated basis |

Loop- and adapter-side failures are not host results (R2-4): a call naming an
operation **absent from the catalog edition offered** to the loop is a
loop-side **not offered** failure and is never dispatched (DEL-05-01 V-2).
*Missing* (no entry in the catalog edition) is a discovery finding (DEL-02-01
required-tool outcome). Neither is labeled *not exposed*.

A denial by the App user's own Codex tool permission (A14) is App-side tool
execution and is not a host outcome (S-C11).

Treatment is resolved on the **host route**, at validation and again at
application (R-3 point 1). A loop or adapter relays the actor's intent and
any governing checkpoint constraint, and does not decide treatment.

### 4.2 Unavailable reason

| Semantic element | Meaning |
|---|---|
| Reason identity | Stable identity for the reason, shared across channels |
| Reason statement | Person-readable text; the same text reaches every channel |
| Failed precondition | Which declared precondition failed |
| Remedy (optional) | What would make it available, stated as a meaning (e.g. "a load case must be identified"), with any gesture phrasing as surface rendering only |
| Evaluated basis | The read basis (§5) against which availability was evaluated |

V4-HI-02's example reason ("Select a load case in the model tree first") is
phrased as a UI gesture (F-C4). For channel parity the precondition is
expressed in operation meaning; the gesture is one surface's remedy text.
Fixtures state remedies as meanings (IR1-B B-m11).

### 4.3 Selection-dependent preconditions

A person often satisfies a target precondition by selecting in the host UI;
an agent supplies the same target through the input schema. Both evaluate the
same precondition. The resolved target becomes part of the request; a later
selection never changes it (DEL-03-02 no-retargeting).

### 4.4 Precondition versus validation error (IR1-B B-m6)

- A condition declared as an element-4 **precondition** yields **unavailable**
  when it fails, with HI-04 parity across channels. It is evaluated before
  execution and may be evaluated at offering time (historical thereafter).
- A condition declared as an element-7 **error** raised by host validation
  yields **refused — invalid** (P §9), with its error identity.
- The host decides which conditions are preconditions and which are
  validation errors, per entry; the catalog makes the choice visible. The
  same condition is never both. Fixture: OP-C4 "location on run" is a
  precondition; "location occupied" is a validation error.

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
  one row changes that row's subject identity and the read-level identity,
  but not other rows' subject identities.
- Uses:
  - DEL-04-03 L-1 c₁ for acts on host rows/objects (A4, A6, A7); A5/A10 use
    DEL-03-02's change-item content identity (R-6);
  - the **per-item basis check** (R2-13): DEL-03-02 compares the subject
    content identities of an item's relied-on targets, not the global model
    revision;
  - **checkpoint subject binding** (R2-17): a subject of class "targets of
    the held call" binds through the subject content identities of the
    relied-on read the held call cites, never through argument text;
  - **resulting objects** of an applied item (R2-14; P §9): post-application
    subject content identities of created and changed objects.
- This is how V4-HI-32's "a row's content hash" is received. Which
  attributes a subject identity covers (e.g. whether a support row's identity
  covers its display label) is a host input (U-C3); the fixtures state their
  assumption (§10.1).

### 5.4 Citing the relied-on basis in a later action (SOW-168)

- A later action (a change submitted through DEL-03-02, or a non-mutating
  examination that relies on a prior read) carries a **relied-on basis
  reference**: the basis descriptor(s) of the read(s) it actually relied on,
  unchanged, together with the subject content identities of the relied-on
  targets.
- The reference points back to a read; it is never recomputed at queue time,
  at acceptance or at application. A host may additionally record the basis
  it observed later as a **separate** element; it never replaces the
  relied-on reference.
- An action relying on several reads cites each. Which cited bases must
  still hold is U-C4.
- **"No longer holds" (R2-13, INTEGRATION).** For a change item, the basis no
  longer holds when a subject content identity of one of the item's relied-on
  targets differs from the current one. A global revision advance alone does
  not stale an item. The **own-effect case** — applying sibling items of the
  same proposal — does not stale remaining items unless they share targets;
  a resubmission of an identity the host already holds is answered from its
  recorded state before any basis check (P §5, §7). Host confirmation of this
  rule and of subject-identity scope remains U-C3.
- **Non-mutating operations citing a basis (PROPOSED, V1-B X-07).** A read,
  examination or host check is never refused as *stale*, because nothing is
  applied. Its result carries the basis it was evaluated on. If that differs
  from the cited relied-on basis, the result states both and its standing is
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
results say **"host checks passed: ‹named checks›"**, and only a host check
(a host-defined, named check, e.g. §10 OP-C12) produces one. Agent work is
**examination / findings** (A3), including requester-parameterized
operations such as OP-C3. "Approval" means only A6.

| Semantic element | Meaning | Must not be strengthened by |
|---|---|---|
| Currency | **current** (describes the workspace's present revision) or **historical** (an earlier revision or superseded result) | Presenting a historical result as current; dropping currency |
| Host checks passed | Each named host check the result passed, **with the basis it was evaluated on**. A check evaluated on an earlier basis is shown as historical | Collapsing to "checked"; implying checks not run; showing an old-basis check as current; presenting A3 findings as a host check |
| Known limitations | Host-stated limitations (e.g. solver assumptions, incomplete inputs) | Omitting or softening limitations in an agent summary |
| Human-act evidence (faithfully carried) | References to actual human acts the host has recorded on this content, carried with at least the DEL-04-03 §6.1 act field set: act name (R-1), decision actor (the person), recorder, recording mode (direct capture / faithful recording, A9), bound subject, scope, purpose, bound content identity (c₀ with method designation), lapse state, evidence references and evidence limits (V1-B D-16) | Inventing an act; showing a lapsed act as current; attributing an agent finding to the person; showing a row-scoped act as covering a whole table |
| Lapse state | DEL-04-03 §7 vocabulary: not lapsed · lapsed · lapsed (subject absent) · partially lapsed · matches c₀ again after observed lapse · unknown (incomparable) · unknown (unavailable) · not yet evaluated; plus **superseded** for A12/A13 (R2-7, PROPOSED). *Not yet evaluated* never renders as *not lapsed* (V1-B D-14; IR1A-13; IR1-B B-m1) | — |
| Act-declined and run-ended events | An **act-declined event** (A4, A6, A7 or A12, with capture evidence) is carried as an event, never as an act; a **run-ended event** is separate (R2-5) | Rendering a decline as the act, or as a rejection (A10 is A5's pair) |
| Agent findings (A3) | Findings authored by an agent, attached by reference (V4-EXM-21), with the agent as author. Where they are held (host-stored, which may be a change, or message content) is U-C5 | Rendering a finding as checked, approved or "host checks passed" |

Rules:

1. A success value establishes execution only (S-C6).
2. One human act never implies another; no synthetic prerequisite is
   introduced (SoW REQ-005).
3. A faithfully carried act keeps the person as decision actor; the recorder
   is shown separately. Satisfaction of a checkpoint needs attributable
   evidence from the capturing surface (R-5); a carried record cites it.
4. When the bound content changes, the act is shown lapsed (S-C8), judged by
   the subject content identity (§5.3), not by the model revision. An undo
   that changes bound content lapses the act like any other change (R2-15).
5. Nothing is presented as certified, sealed, approved or code-compliant
   (V4-AUT-05).

## 7. Operation sequences (catalog view)

```text
discover entry (identity, version, purpose, schemas, availability, class, exposure)
  → request read (arguments)          → unavailable | not permitted | channel not enabled
                                        | not exposed on this surface (host) | error   (each with evaluated basis)
  → read result (content, standing, BASIS B, subject content identities)
  → [consumer reasoning; no host state]
  → request change citing relied-on basis B, relied-on target identities, any checkpoint constraint
       (DEL-03-02 route) host de-duplicates by proposal identity, resolves treatment, checks per-item basis
       → P §9 outcomes (refused — stale cites B and current basis;
          applied associates proposal/item, B, receipt, resulting revision, resulting objects)
```

Failure behavior at catalog seams:

| Situation | Required behavior |
|---|---|
| Entry version changed between offering/discovery and request | The request carries the entry version it was prepared for. A host-side mismatch is reported as an element 7 error meaning (U-C6), not re-interpreted. A loop may pre-screen for a catalog-edition change before dispatch; that is reported as loop-side, not as a host outcome (V1-C D-13) |
| Call names an operation absent from the edition offered | Loop-side *not offered*; never dispatched (R2-4) |
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
examining, not a selection. The fixture's assumed exposure (§10) does not
change this map: the map is about real host agreement.

| Catalog element / concern | H | E | X | Candidate to examine | Producing owner | Receiving point |
|---|---|---|---|---|---|---|
| Entry discovery (identity, version, purpose, open description) | unagreed | unagreed | unagreed | generated for E and X | Host owner | DEL-05-01 tool offering; DEL-03-03 native tool inspection; PKG-02 tool descriptors (DEP-03-01-022) |
| Exposure per surface (element 9) | unagreed | unagreed | unagreed | declared per entry | Host owner | DEL-02-01 required-tool outcome; DEL-05-01; DEL-03-03 |
| Input schema / argument checking | unagreed | unagreed | unagreed | generated or checked for E and X | Host owner | DEL-05-01 REQ-003 (catalog schema before domain validation) |
| Loop-side catalog-schema argument checking (DEL-05-01 candidate (b)) | — | unagreed | — | question held: shared checker or per-host (V1-C D-28) | UNRESOLVED{OI-013}/{OI-014} | DEL-05-01; DEL-10-03 |
| Availability + reason | unagreed | unagreed | unagreed | checked on all three (parity rule) | Host owner | DEL-05-02 panel; DEL-03-03 |
| Effects / affected objects / resulting objects | unagreed | unagreed | unagreed | generated metadata | Host owner | DEL-03-02 target binding and applied association |
| Result content + standing | unagreed | unagreed | unagreed | H hand-built views; E/X checked against H meaning | Host owner | DEL-05-02; DEL-04-02; DEL-09-09 VER-002 |
| Errors | unagreed | unagreed | unagreed | generated identities, hand-built texts | Host owner | DEL-03-02 outcome taxonomy |
| Class element | unagreed | unagreed | unagreed | carried from DEL-04-01 records | DEL-04-01 → host | DEL-04-02; DEL-03-03; DEL-05-01 |
| Governing checkpoint constraint (receipt on the host route) | unagreed | unagreed | unagreed | per-request carriage or host-held declaration (relay, R2-12) | Host owner with DEL-03-02 | DEL-05-01 §6.2; DEL-03-03 |
| Read basis, subject content identities, method designation | unagreed | unagreed | unagreed | one host producer for all three | Host owner | DEL-03-02; DEL-04-03 L-1/L-2 |
| Proposal views (old/new/objects/reason) | unagreed (host's own views, V4-HI-24) | n/a (agent drafts) | n/a | host-owned presentation; generation route open | Host owner | DEL-03-02 view receiving (DEP-03-02-024) |
| Shared types / components carrying the above | — | — | — | UNRESOLVED{OI-014} | App/shared contract owners | DEL-10-03 account |

Extension promise (OI-003; S-C9): the original promise that a new catalog
operation becomes available to the person and both agents **without separate
work** is preserved and **not claimed**. Its disposition — retain, narrow to
defined generated surfaces, or defer — is `UNRESOLVED{OI-003}`, owned by the
owner with the host contract owner (DEP-03-01-027). Per-surface exposure
(element 9) is where a narrowed promise would be expressed; its real values
stay *unagreed* until the ruling. The evidence route is DEL-09-09's
V4-EXM-24 trace (DEP-03-01-030; CASE-002 M4-X). No automatic availability or
maintenance saving is advertised and no narrower criterion is selected.

## 9. Proposal input this catalog needs, and the M3-CP return

Co-developed with DEL-03-02/P-v0.3 (original SCC-CASE-004 pair, carried in
CASE-002). Both files had one author through R1 and R2; C↔P agreement is not
independent evidence (IR1-B note).

**Forward (C → P, DEP-03-01-023 / DEP-03-02-016).** C supplies: operation
identity and version; input schema including target identification; effects;
errors with effect statements; the §4.1 results; the read basis descriptor
with method designation; subject content identities; exposure; and the
relied-on basis reference meaning (§5.4).

**Proposal input C needs from P** (compared at V1; repaired at R1 and R2):

| Needed from DEL-03-02 | P-v0.3 locus |
|---|---|
| Relied-on basis reference carried unchanged from drafting through outcome, with relied-on target identities | P §3.2 |
| Stale refusal reporting the relied-on and current bases, with reason and evaluated basis; per-item check on target identities | P §5, §9 |
| Re-draft as a separately identified proposal citing the new basis, with lineage | P §5 |
| Retry precedence: identity-based de-duplication before the basis check | P §5, §7 |
| **Applied-outcome association** per item: proposal/item identity, relied-on basis, host receipt reference, resulting revision, and **resulting objects** — created and changed object identities with their post-application subject content identities and method designation, or "not supplied" as an evidence limit (R2-14). Whether the host receipt *itself* carries these is a host observation, not assumed (V1-B D-22) | P §9, §11 |
| Target binding fixed at drafting | P §6 |
| Change-item content identity built from C elements | P §3.1 |

**Return (P → C, M3-CP, DEP-03-01-026).** Distinct from the forward handoff:
DEL-03-02 supplies designed refusal/application behavior and the C/P
read-then-action comparison with an intervening edit (P-v0.3 §11). DEL-03-01
uses it only to compare the basis elements across read, proposal, refusal,
re-draft and applied outcome (VC-C-04). AC-004/VER-004 cannot be claimed
complete until an actual, candidate-bound return exists (V1-B X-08). The
register lacks the DEL-03-02 DOWNSTREAM mirror of DEP-03-01-026 (V1-B RF-08;
routed to closeout C1).

## 10. Shared fixture catalogue — FX-PIPE-01 (R-9; R2-21)

This section is the **one** invented fixture catalogue and revision timeline
for the Wave-1 definitions. Other files cite its entries and steps; a
genuinely needed local case is named `L-‹file›-n` and says why. All material
is **invented fixture subject matter**. Labels (OP-C…, S-…, T…, V-…, PR-…,
RC-…, ⟨set-n⟩) are fixture labels, not operation identities, wire names or
SWBPIPE commitments. No SWBPIPE catalog has been supplied. Owning this shared
fixture is an R1/R2 integration assignment serving several deliverables; it
does not extend DEL-03-01's SoW scope (IR1-B §5). Every C-v0.2 identifier is
kept stable; v0.3 only adds identifiers.

### 10.1 Model and fixture assumptions

FX-PIPE-01: workspace **FX-W1**, generation **g1**. One run **R-100** between
nozzles N-1 and N-2; supports **S-1 … S-4** (S-2 and S-3 rigid at start);
sustained load case **LC-1**. Person: **Engineer A** (invented). Agent: the
host's single agent seat. Workflow: `supports-adjust` (invented; identity per
DEL-02-01 §6.1: kind *workflow*, origin *host*, source root ⟨fx-root⟩, name
`supports-adjust`, revision ⟨rev-3⟩), run **12**.

Fixture assumptions (labeled; host inputs in reality):

- **FA-1 Exposure.** Every entry is **exposed on H, E and X** (fixture
  assumption, R2-21). Non-exposure is demonstrated only by named variant V-X1.
- **FA-2 Subject identity scope.** A support row's subject content identity
  covers its location, type, stiffness **and display label**. A run's subject
  identity covers its geometry, not its supports' attributes.
- **FA-3 Relied-on targets.** Adding a support between two supports relies on
  those two supports (their subject identities) and on the run.
- **FA-4 Settings.** ⟨set-1⟩: for the SWB model-change class (DEL-04-01
  P-03), display state **effective (policy default)**, grant value *propose*,
  no setting actor (R2-6). ⟨set-2⟩: after T15.
- **FA-5 Checkpoints.** A named variant V-CP1 declares an A5 checkpoint
  `CP-accept` in run 12 on OP-C4 results (reached-when: proposal queued;
  subject: that proposal's change items, R2-17).

### 10.2 Entries

| Fixture | Purpose | Inputs | Availability (precondition → reason) | Effects | Result + standing | Errors (effect) | Class (§3.1) | Exposure H/E/X |
|---|---|---|---|---|---|---|---|---|
| OP-C1 v1 "Read supports table" | Lists supports on a run with type, location, stiffness, label | run | run exists → "Run not found in this workspace" | none | supports table with a subject content identity per row; currency; host checks passed (with basis); limitations | E-invalid-run (none) | none — fixture assumption | exposed ×3 (FA-1) |
| OP-C2 v1 "Read sustained-load results" | Stresses and support loads for a load case | run, load case | a load case is identified → "A load case must be identified"; a current solve exists → "No current solve for LC-1 at this revision" | none | results table; currency; host checks passed each with evaluated basis; limitation "linear supports assumed" | E-unknown-load-case (none) | none — fixture assumption | exposed ×3 |
| OP-C3 v1 "Examine support spacing" (non-mutating) | Lists spans exceeding a **requester-stated** limit, for the requester's examination | run, spacing limit | run exists | none | exceedance list as the requester's **findings (A3)**, with evaluated basis; never "host checks passed" (the limit is the requester's) | E-invalid-limit (none) | none — fixture assumption; findings are not A4 | exposed ×3 |
| OP-C4 v1 "Add support" | Adds a support at a location on a run | run, location, type | run exists; location on run → "Location is not on run R-100" (precondition, §4.4) | supports table, R-100 | applied association with **resulting objects** (new support identity and its subject identity) | E-location-occupied (validation → refused — invalid; none); E-apply-interrupted (unknown) | may apply within granted autonomy — DERIVED (P-03); default propose; OI-021 additions pending; host adoption not evidenced | exposed ×3 |
| OP-C5 v1 "Set support stiffness" | Changes a support's stiffness | support, stiffness | support exists | support row | applied association with resulting objects | E-invalid-stiffness (none) | as OP-C4 | exposed ×3 |
| OP-C6 v1 "Mark row checked" | Performs the person's A4 on a row's content | row | row exists | host act state on row | act captured, bound to the row's subject content identity | E-row-changed (none) | **reserved to the person** — DERIVED (R2-2; D2a) | exposed ×3 |
| OP-C7 v1 "Accept proposal items" | Performs the person's A5 on one or more change items | proposal, items | items queued | proposal item dispositions | A5 captured, bound to each item's change-item content identity | E-item-not-queued (none) | **reserved to the person** — DERIVED (R2-2; D2b) | exposed ×3 |
| OP-C8 v1 "Reject proposal items" | Performs the person's A10 | proposal, items | items queued | proposal item dispositions | A10 captured | E-item-not-queued (none) | **reserved to the person** — DERIVED (R2-2; R-1 A10) | exposed ×3 |
| OP-C9 v1 "Set support label" | Changes a support's display label (low consequence) | support, label | support exists | support row (label) | applied association with resulting objects | E-label-too-long (none) | as OP-C4 (model change) | exposed ×3; variant V-X1: not exposed on X |
| **OP-C10 v1 "Undo (reverse a receipt)"** (new, R2-15) | Reverses the change recorded by a receipt, through the one route | receipt | receipt exists and is reversible → "Receipt cannot be reversed" | objects changed by the reversed receipt | applied association with relation **reverses ⟨receipt⟩** and resulting objects | E-reverse-conflict (none) | governed by the **policy record of the operation whose receipt it reverses** (e.g. reversing RC-2 from OP-C9 → P-03: may apply within granted autonomy, default propose) — R3-4 (INTEGRATION; DEL-04-01 states it under P-03); undo mechanism a host input (U-P8) | exposed ×3 |
| **OP-C11 v1 "Renumber nodes"** (new, R2-21) | Renumbers node labels on a run | run, scheme | run exists | node labels on R-100 | applied association | E-invalid-scheme (none) | **no policy basis** (reason: **pending OI-021**) — INTEGRATION (R2-1) | exposed ×3 |
| **OP-C12 v1 "Run support-spacing host check"** (new, R2-21) | Runs the host's named check "support spacing" with host-defined limits | run | a current model basis exists | none | "host checks passed: support spacing" or "host check failed: support spacing" with exceedances, each with evaluated basis | E-check-unavailable (none) | none — fixture assumption | exposed ×3 |

Grant changes (A12) and enabling/disabling external access (A13) are person
acts on host/App controls, not fixture catalog entries here; they are
reserved (S-C10).

### 10.3 Timeline (one revision sequence, generation g1)

Content identities are opaque: ⟨v12⟩ is a read-level identity at r12,
⟨S-2@r12⟩ a subject identity; method designation ⟨m-fx⟩ throughout.

| Step | Revision | Event | Fixture uses |
|---|---|---|---|
| T1 | r12 | State: S-1…S-4 on R-100; LC-1 solved at r12 (host checks passed: "equilibrium", "unit consistency", evaluated at r12). Settings ⟨set-1⟩ (FA-4) | Baseline |
| T2 | r12 | Engineer A marks row S-2 checked (OP-C6; A4), bound to ⟨S-2@r12⟩, direct capture by host facility | Standing; lapse later |
| T3 | r12 | Agent reads OP-C1 → basis **B1** = FX-W1/g1/r12/⟨v12⟩/⟨m-fx⟩, with ⟨S-1…S-4@r12⟩ | Read basis |
| T4 | r12 | Agent runs OP-C3 with limit 6 m: span S-2→S-3 exceeds it (A3 findings, basis B1) | Agent findings |
| T4a | r12 | Agent runs OP-C12: "host check failed: support spacing" (span S-2→S-3), evaluated at r12 | Host check (named) |
| T5 | — | Agent drafts **PR-1** relying on B1: item 1 add guide support at 4.2 m on R-100 (OP-C4; relied-on targets R-100, S-2, S-3 per FA-3); item 2 S-3 stiffness rigid → 2.0e6 N/m (OP-C5; relied-on target S-3) | Proposal draft |
| T6 | r13 | Engineer A edits S-3 stiffness in the host UI (intervening edit). ⟨S-3⟩ changes; ⟨S-2@r12⟩ unchanged; LC-1 results become historical (no current solve at r13) | Intervening edit; unrelated-edit control for T2 |
| T7 | r13 | Agent submits PR-1 → both items **refused — stale** (each relies on ⟨S-3@r12⟩): relied B1, current **B2** = FX-W1/g1/r13/⟨v13⟩/⟨m-fx⟩, reason "S-3 changed since r12" | Stale refusal (per-item check, R2-13) |
| T8 | r13 | Any channel requests OP-C2 for LC-1 → **unavailable**, reason "No current solve for LC-1 at this revision", evaluated basis B2 | Unavailable parity |
| T9 | r13 | Agent re-reads OP-C1 (B2) and drafts **PR-2** (lineage PR-1, stale): item 1 add support (old: none; targets R-100, S-2, S-3 at r13); item 2 S-3 stiffness (old: value at r13) → 2.0e6 N/m | Re-draft |
| T10 | r13 | PR-2 validated → **queued** | Queued ≠ applied |
| T11 | r13 | Engineer A accepts item 1 (OP-C7; A5 bound to item-1 change-item content identity) and rejects item 2 (OP-C8; A10) | Item-level acts |
| T12 | r14 | Host applies item 1 → receipt **RC-1**; applied association PR-2 / item 1 / B2 / RC-1 / r14 / resulting objects: **S-5 created** ⟨S-5@r14⟩, R-100 changed ⟨R-100@r14⟩. A5 on item 1 is **not** lapsed by its application | Applied; resulting objects; no lapse on application |
| T13 | r14 | Acknowledgment of T12 lost. Agent resubmits PR-2 (same proposal identity). The host de-duplicates by identity **before** any basis check and reports the recorded state: item 1 applied RC-1, item 2 rejected (R2-13). If the loop cannot observe that report either → **outcome unknown** (observer: loop), last observed state *accepted* | Retry precedence; one effect |
| T14 | r15 | Engineer A edits S-2 stiffness → T2's A4 on S-2 **lapsed** (⟨S-2⟩ changed) | Lapse |
| T15 | r15 | Engineer A performs A12 → ⟨set-2⟩: SWB model-change class (P-03), grant value *direct*, **scope** {model/workspace: FX-W1; object set: {S-4}} (R-8 dimensions). Host control confirms → display state **effective, direct**. Because OP-C5 shares class P-03, this grant would also admit OP-C5 on S-4 directly; a consequence dimension could exclude it, but its vocabulary is open (U-02), so no fixture expectation is set for OP-C5 on S-4 under ⟨set-2⟩ (held on U-02) | Grant change (reserved act); R-8 scope |
| T16 | r16 | Agent applies OP-C9 directly (label S-4 "G-4") under ⟨set-2⟩ → receipt RC-2, origin mark, undo route; no acceptance recorded | Direct branch |
| T16a | r16 | Engineer A marks row S-4 checked (OP-C6; A4), bound to ⟨S-4@r16⟩ | Act on content the undo will change |
| T17 | r17 | Engineer A reverses RC-2 via OP-C10 → receipt RC-3, relation **reverses RC-2**; S-4 label restored. T16a's A4 **lapsed** (⟨S-4⟩ changed, FA-2). RC-2's standing: "applied, then reversed by RC-3" | Undo; lapse by undo (R2-15) |
| Tg | g2/r1 | (Separate branch) Workspace restored from an archive: new generation g2. Any basis from g1 is incomparable by revision; lapse and stale evaluation under generation change is U-C2 | Generation change |

### 10.4 Named variants

| Variant | Branches from | Event | Expected |
|---|---|---|---|
| **V-S1** Stale after acceptance | T11 | Engineer A edits S-2 before T12 (branch revision r14′) | Item 1 (relies on S-2) **refused — stale** at application; A5 not lapsed; display "accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)" (R2-16) |
| **V-CP1** Acceptance checkpoint vs direct grant | A variant of T15 granting *direct* for P-03 with scope {model/workspace: FX-W1; object set: R-100 and its supports}, plus FA-5 | Agent requests OP-C4 directly in run 12 | **not permitted**, naming the governing checkpoint constraint {run 12, CP-accept, A5, OP-C4}; the agent may then submit a proposal separately, whose items become CP-accept's subject (R2-12). Status: AWAITING INPUT (host receipt of the constraint, relay) |
| **V-NP1** No policy basis | T9 | Agent requests OP-C11 directly; then proposes it; Engineer A attempts A12 granting direct for OP-C11's class | Direct → **not permitted** (no policy basis, pending OI-021); proposal → queued, confers no permission; A12 → **refused (reason: no policy basis)**; dependent production reported **held** (R2-9) |
| **V-R1** Reserved entry call | T3 | Agent calls OP-C6 on S-1 | **not permitted** (reserved to the person, P-02) with an A8 request *offered*; no A8 recorded unless issued; never *not exposed* or *unavailable* |
| **V-X1** Not exposed | T16 | External agent (X) calls OP-C9 where element 9 = not exposed on X | Host returns **not exposed on this surface**; the adapter relays it (reporter: host). If X's channel is off instead: **channel not enabled** |
| **V-OU1** Lost outcome | T12 | Neither T12 nor T13 report observed | **outcome unknown**, observer loop, last observed *accepted*; no inferred effect |

### 10.5 Read basis vs operation identity

| Read | Operation (identity/version) | Basis |
|---|---|---|
| T3 | OP-C1 v1 | FX-W1 / g1 / r12 / ⟨v12⟩ / ⟨m-fx⟩ |
| T9 | OP-C1 v1 (same operation) | FX-W1 / g1 / r13 / ⟨v13⟩ / ⟨m-fx⟩ — different basis |
| hypothetical | OP-C1 **v2** (entry revised) | FX-W1 / g1 / r13 / ⟨v13⟩ — different operation version, same basis |

### 10.6 Unavailable example (T8, three channels)

Person (H), embedded agent (E) and external agent (X) each request OP-C2 for
LC-1 at r13. Expected on all three: *unavailable*; failed precondition
"current solve exists"; reason identity R-no-current-solve; same statement;
evaluated basis B2. Not acceptable: an empty results table, a generic error,
or the r12 result without historical currency. If X's channel is off, X
instead gets *channel not enabled* (a separate case).

### 10.7 Standing example (T4a, T12–T14)

OP-C2 after a new solve at r14 (hypothetical): currency current; host checks
passed "equilibrium", "unit consistency" evaluated at r14; limitation
"linear supports assumed". T4a's "host check failed: support spacing" is
shown historical (r12). Row S-2 at r14 carries T2's A4 (actor Engineer A,
recorded by host, direct capture, bound ⟨S-2@r12⟩): **not lapsed** (T6 edited
S-3 only). At r15 (T14) it is shown **lapsed**. T4's findings are shown as
agent findings (A3), never as checked or as a host check.

## Changes from v0.2

v0.2 = C-v0.2 (sha256 358182b1…6d82, 577 lines, committed at `c387730fb`).

| R2 / IR1 item | Change |
|---|---|
| R2-1; IR1-A IR1A-01; IR1-B B-M1; IR1-C IR1C-10 | Fifth class value renamed **no policy basis** with reason sub-element {omitted, unassigned, pending OI-021}; five values listed; fifth marked INTEGRATION |
| IR1-B B-m12 | Value standing mirrors DEL-04-01 §8.1 (adds settled-by-basis, INTEGRATION) |
| R2-2; IR1A-08 | Class rule 1: operations that *perform* A4–A7, A10, A12, A13 (incl. act-state changes) reserved; no faithful record through them; host faithful-record operation conditions and relay question (U-C11) |
| R2-3; R2-11; IR1A-16 | S-C10/S-C11 credit D2/D3 only with what they say; disabling A13 INTEGRATION; App A14 restriction attributed to R-2 |
| R2-4; IR1-B B-M4, B-M5, X-7; IR1C-11; IR1A-02, IR1A-10 | §2 inv. 5: class never implies exposure; reserved entries always offered; A8 *offered*, not auto-recorded. §4.1: reporter column; *not exposed* reported by host only and relayed; loop-side *not offered* named |
| R2-9; IR1A-17 | Class rule 4: no-policy-basis wording; A12 widening refused; fixtures report held (V-NP1) |
| R2-12 | Class rule 3 and §4.1 *not permitted* name the governing checkpoint constraint; §8 map row for its host receipt; V-CP1 |
| R2-13; IR1-B B-M7 | §5.4 "no longer holds" = per-item subject-identity check on relied-on targets; own-effect case named; dedup precedes basis check; T7 per-item; **T13 fixed** |
| R2-14; IR1-B B-M6 | §3.3 resulting-object reporting; §5.3 use; §9 forward table adds resulting objects; T12 names S-5 created |
| R2-15; IR1A-06; IR1-B X-5 | **OP-C10 Undo** added; §2 inv. 1 names undo; §6.2 rule 4 undo lapses changed content; T16a/T17 lapse demonstration; relation "reverses" |
| R2-5; IR1A-03 | §6.2 act-declined and run-ended events carried as events |
| R2-7; IR1A-13; IR1-B B-m1 | Lapse vocabulary adds "matches c₀ again after observed lapse" and *superseded* (A12/A13) |
| R2-17; IR1-C X-10 | §5.3 held-call targets bound through relied-on subject identities |
| R2-21; IR1-B X-6, B-M8, B-M10, B-m10; IR1-C IR1C-15 | §10: all v0.2 IDs kept; fixture assumptions FA-1…FA-5 (exposure = exposed ×3 as fixture assumption; §8 map stays unagreed); **OP-C11** no-policy-basis entry; **OP-C12** host check entry; OP-C3 stays Examine (A3) and clarified; T4a; T15 scope in R-8 dimensions (model/workspace + object set, compatible with DEL-04-02/04-03 aligners) with OP-C5-on-S-4 held on U-02; named settings ⟨set-1⟩/⟨set-2⟩; named variants V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1; local-label rule `L-‹file›-n`; SoW-scope note |
| R2-6 | FA-4 ⟨set-1⟩ = effective (policy default), no setting actor |
| R2-16; IR1-B X-8 | V-S1 display wording |
| IR1-B B-m6 | §4.4 precondition vs validation error rule |
| IR1-B B-m5 | One evidence-label mapping published (Verification cases) |
| IR1-B B-m11 | §4.2 fixtures state remedies as meanings |
| IR1-B §5 SoW fidelity | §10 states the shared fixture is an integration assignment, not SoW scope |
| Commit read rule | Sibling v0.2 texts read from `28bd00499`; hashes in header |
| R3-4 (R3_RESOLUTIONS.md sha256 202d52c7…afbf; in-place edit, no version bump) | OP-C10 class now cites the policy record of the operation whose receipt it reverses (INTEGRATION); closes W3 finding F-R2-4 |
| Coordinator R2 notes (DEL-04-02/03 aligner items) | §4.1 reporter of *not exposed* stated as host-reported from element 9, relayed by loop/adapter, separate from loop-side *not offered*; T15 scope reduced to model/workspace + object set for compatibility with the DEL-04-02/03 fixtures |

Fixture identifiers added: OP-C10, OP-C11, OP-C12, T4a, T16a, S-5 (created at
T12), ⟨set-1⟩, ⟨set-2⟩, FA-1…FA-5, V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1.
Changed meaning (IDs stable): T7 (explicitly per-item), T13 (dedup before
basis check), T15 (scope in R-8 dimensions), OP-C3 (result wording), all
entries' exposure (exposed ×3 by FA-1). Removed: none.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-021}` operation-specific reserved additions; first connected operation, autonomy, environment | Owner via outside SWB session and App/shared owner | Before connected SoW / live examination | Classes for OP-C4/C5/C9 carry "OI-021 additions pending"; OP-C11 is *no policy basis (pending OI-021)*; all examples invented |
| `UNRESOLVED{OI-003}` retain / narrow / defer extension promise | Owner with host contract owner (DEP-03-01-027); trace from DEL-09-09 (DEP-03-01-030) | Before claiming extension or fixing AC-007 criterion | Map (§8) stays *unagreed*; promise preserved, not claimed |
| `UNRESOLVED{OI-014}` shared contract/component placement | App/shared contract owners | Before structural/production allocation | Map rows for shared types and loop-side checking left open |
| `UNRESOLVED{OI-013}` per-host loop placement (loop-side argument checking) | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary | §8 row held as a question |
| Host adoption of D2 list, D3 rule and R2 treatments | Host owner / SWBPIPE (DEP-001) | Before host conformance | Class values are App/shared; host adoption "not evidenced" |
| Consequence vocabulary (DEL-04-01 U-02) | DEL-04-01 with host policy owner | Before class assignment for connected operations; before a consequence scope dimension is used | §3.1 consequence statement empty; T15 scope uses model/workspace + object set only; OP-C5 on S-4 under ⟨set-2⟩ held on U-02 |
| U-C1 Serialization, content-identity algorithm, method-designation scheme, catalog/schema placement, adapter realization (TBD-003) | App/shared capability-contract owner with host/consumer owners (DEP-03-01-028) | Before dependent schema implementation/conformance | All element names semantic; identities opaque |
| U-C2 Host definition of generation; lapse/stale under generation change and restore | Host owner (DEP-03-01-025) with DEL-04-03 | Before basis conformance, lapse display criteria | Tg fixture only |
| U-C3 Host confirmation of the per-item stale rule (R2-13) and subject-identity scope (FA-2/FA-3 assumed in fixtures) | Host owner with DEL-03-02 / DEL-03-01 | Before stale behavior and lapse conformance | Contract rule fixed as INTEGRATION; host behavior unevidenced |
| U-C4 Multi-read reliance: which cited bases must hold | Host owner with DEL-03-02 | Before stale implementation | §5.4 requires citing each |
| U-C5 Where agent findings are held; whether host-stored findings are a change | Host owner | Before V4-EXM-21 fixture binding | OP-C3 findings requester-authored |
| U-C6 Host behavior on entry-version mismatch | Host owner | Before adapter implementation | §7 requires explicit error meaning |
| U-C7 Actual host catalog, tables, diagnostics, availability, exposure, content identities | Host owner / SWBPIPE (DEP-03-01-025; DEP-001) | Before host conformance claim | Examples invented; exposure assumed (FA-1) |
| U-C8 Actual M3-CP executable return (V1-B X-08); reconciliation with DEL-04-01 v0.3 | DEL-03-02; DEL-04-01 | V2 comparison; AC-004 closure | AC-004 held |
| U-C9 Whether hosts publish version compatibility statements | Host owner with DEL-02-01 | Before DEL-02-03 required-tool fixtures | Equality only until then |
| U-C10 Host confirmation of non-mutating basis handling (§5.4) | Host owner | Before V4-EXM-21 binding | PROPOSED rule only |
| U-C11 Whether any host offers a faithful-record operation meeting R2-2's conditions (relay) | Host owner (DEP-001) | Before host act-recording integration | None assumed in fixtures |
| Governing-checkpoint-constraint receipt on the host route (relay, R2-12) | Host owner with DEL-03-02 | Before V-CP1 / LOOP FX-C9 / PANEL PC-24 / WD VC-11 execution | V-CP1 AWAITING INPUT |
| Register: missing DEL-03-02 mirror of DEP-03-01-026; unregistered C → DEL-04-02/04-03 joins; C → DEL-05-01/05-02 mirrors (V1-B RF-04/05/08; V1-C RF-1) | Register owner at closeout C1 | C1 | None on content |
| SoW text (REQ-002, TBD-001) still calls OI-001/OI-002 open | Closeout C1 via owning route | C1 | This design applies DECISION-1; SoW scope unchanged |

## Verification cases

Designed, **not run**. **Evidence-label mapping** (one mapping, owned here per
V1-B D-19 / IR1-B B-m5):

| C/P label | DEL-05-01 LOOP §12 | DEL-05-02 PANEL | Can support |
|---|---|---|---|
| *illustrative* | CONTRACT-REVIEWED | DEFINED | Completeness of the definition only |
| *test-double* | FIXTURE-EXECUTED | EXECUTED (on a test double, with configuration and date) | The expectation holds for that double; nothing about the host |
| *actual host* | HOST-OBSERVED | EXECUTED on an identified host candidate | That candidate only |
| (no evidence) | NOT-OBSERVED | AWAITING INPUT (named input) / HELD (named decision) | Nothing; recorded as a gap |
| (partial) | — | LIMITED | As stated in the limitation |

Fixture steps and variants refer to §10.3–§10.4.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-C-01 Entry field coverage | For OP-C1…C12 and a real host entry when supplied, check the nine §3 elements, §3.1 sub-elements and §3.3 extras against V4-HI-02, SOW-157–164, R-2, R2-1, R2-2 | Every element present; class shows adopted/DERIVED/INTEGRATION value with policy record reference, or *no policy basis* with reason; OP-C6/C7/C8 reserved; OP-C11 no policy basis (pending OI-021); no OI-002 value; value standing from the §8.1 list; exposure values present | VER-001 |
| VC-C-02 Cross-channel read parity | OP-C1 at T3 via H, E, X; compare content, subject identities, diagnostics, standing | Identical meaning and standing; mismatches listed; evidence labeled per the mapping; type match alone does not close a consumer claim | VER-002 |
| VC-C-03 Non-success parity and separation | T8 on H, E, X; V-R1; V-X1; V-NP1 direct; a loop call to an operation absent from the offered edition | T8: same *unavailable*, reason, evaluated basis B2 on all three; V-R1 → *not permitted* + A8 offered (not recorded); V-X1 → host-reported *not exposed*, relayed; channel off → *channel not enabled*; V-NP1 → *not permitted*; absent operation → loop-side *not offered*, never dispatched, never labeled *not exposed*; none is an empty success | VER-003 |
| VC-C-04 Read-to-action basis trace (M3-CP receiver) | T3 → T5 → T6 → T7 → T9 → T10 → T11 → T12 → T13 using P-v0.3 §11 | All elements incl. method designation at every read; PR-1 reference = B1 throughout; T7 refuses both items per-item with B1 and B2; PR-2 new identity citing B2; T12 association PR-2/item 1/B2/RC-1/r14 with resulting objects S-5, R-100; T13 answered from recorded state (no stale refusal from its own effect); whether RC-1 itself carries B2 recorded as a host observation; no step rewrites a reference | VER-004 |
| VC-C-05 Standing, attribution and lapse | T2, T4, T4a, T6, T12, T14, T16a, T17 | T2 A4 carried with full act fields; not lapsed after T6; lapsed after T14; A5 on item 1 not lapsed by T12; T16a A4 lapsed by the T17 undo; T4 findings never shown as checked or host check; T4a "host check failed: support spacing" with its basis, historical after r12; no act inferred from success | VER-005 |
| VC-C-06 Responsibility map review | Walk §8 against H/E/X, CLM-001–003 and receiving rows (PKG-02, DEL-03-02, DEL-04-01, DEL-04-02, DEL-04-03) | Each cell valued; no *generated/checked* without a conformance route; fixture exposure (FA-1) not used as map evidence; host implementation external | VER-006 |
| VC-C-07 Extension treatment | Compare §8 extension text and element 9 with V4-PAR-05, V4-HI-03, #d4, OI-003, V4-EXM-24 | Promise stated; `UNRESOLVED{OI-003}` with owner; trace route via DEL-09-09; no automatic availability/savings; real exposure values *unagreed* | VER-007 |
| VC-C-08 Boundary and open-input audit | Check each REQ-007 exclusion and each UNRESOLVED row; check DERIVED/INTEGRATION/PROPOSED markings against R1/R2; check D2/D3 attribution (R2-11) | Every excluded act maps to its owner; each open input has owner, point of need, effect; no host delivery, SWBPIPE adoption or joined qualification claimed; no rule credited to D2/D3 beyond their text | VER-008 |
