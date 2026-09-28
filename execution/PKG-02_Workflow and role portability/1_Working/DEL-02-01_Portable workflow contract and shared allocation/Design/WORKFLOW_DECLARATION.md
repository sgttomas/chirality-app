# Portable workflow declaration, roles, source identity and shared allocation
- Contribution: DEL-02-01/WD-v0.2 (supersedes DEL-02-01/WD-v0.1, file sha256 `bacfcb71ca9585b950444c0218fdd5283f5b2f5d0c8f981411395278b286fc5e`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003 (map version), OUT-004 (fixture design only); REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; AC-001…AC-007 by designed verification; VER-001…VER-007 (cases designed, none run)
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 080d7f5a8e55d93c06f51e5332b53954deb03e0877b1ee49be3011e3de14a294; P/docs/PRD.md §2.2 (V4-HOST-05/06), §2.4 (V4-SHR-01…03), §4.1 (V4-WF-01…06), §4.2 (V4-ROLE-01…03), §4.3 (V4-EXE-03), §4.5 (V4-AUT-01…05), §4.7 (V4-REC-01…05); P/docs/ARCHITECTURE.md §1 (M-1, M-3, M-5), §4, §5 (V4-ARC-20/21); P/docs/HOST_INTEGRATION.md §1, §2 (V4-HI-02…04), §3 (V4-HI-11/12), §4 (V4-HI-20…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §9 (V4-HI-70/71); P/docs/EXAMINATION.md V4-EXM-10, -14, -21, -22; DECISION_BRIEF.html #d2, #d3, #d5; SCC-CASE-002 Case_Datasheet M1 rows; Open_Issues.csv OI-003, OI-013, OI-014, OI-018, OI-021; owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 `f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e`), rulings D1 (scope), D2 (OI-001), D3 (OI-002). Root reuse sources read (not adopted): `workflows/WORKFLOW_TEMPLATE.md`, `workflows/*/execution.json` (66 companions surveyed), `workflows/catalog.yaml`, `workflows/catalog.schema.json`, `workflows/index.json`, `workflows/create-workflow/WORKFLOW.md`, `docs/SPEC.md` §9.1–9.8, `docs/AGENT_WORKFLOW_RUNTIME.md`.
- Consumed inputs:
  - R1_RESOLUTIONS.md (sha256 `2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4`) R-1, R-2, R-3, R-4, R-5, R-6, R-7, R-9. Elements taken from sibling v0.2 drafts through these rulings are marked "per R1_RESOLUTIONS R-n; to be confirmed at IR1".
  - V1-A.md (sha256 `01811533bf0aedad5326d1517561187682a572ae3f47c5f8b8637e48cfe04c09`) items addressed to DEL-02-01; V1-C.md (sha256 `8d46258ad0120067f6472442de67feacba8405462b78abb8bac34be28a4a94a6`) items addressed to DEL-02-01.
  - DEL-04-01 canonical act names A1–A14 per R1_RESOLUTIONS R-1 (DEL-04-01 v0.2 not read). DEL-03-01 outcomes (C §4.1), subject content identity, identity method designation, per-surface exposure element and the FX-PIPE-01 fixture catalogue per R-6/R-9 (C v0.2 not read). DEL-03-02 outcome taxonomy (P §9) and change-item content identity per R-6/R-7 (P v0.2 not read). DEL-04-03 L-1 content-identity sources per R-6 (not read).
  - DEL-05-01 LOOP-v0.1 and DEL-05-02 PANEL-v0.1 consumer needs known only as quoted in V1-C (files not read). DEL-02-02, DEL-02-03, DEL-02-04: accepted SoWs only. SWBPIPE consumer needs: none received.
- Receivers: CASE-002 M1 "Workflow-contract owner" row: DEL-02-03 (OUT-001, OUT-002; REQ-001, REQ-002, REQ-004; VER-001, VER-002, VER-004; W7 in this undertaking); DEL-05-01 (OUT-001, OUT-004; REQ-005, REQ-007; VER-008); DEL-05-02 (OUT-001; REQ-001; VER-001); DEL-02-01 self-check (OUT-004; REQ-004, REQ-005; VER-004, VER-005). DEL-02-02 (OUT-001, OUT-004; REQ-005; VER-004) and DEL-02-04 (OUT-001, OUT-002; REQ-001, REQ-002, REQ-004; VER-001, VER-005) remain named receivers but are outside this undertaking per owner ruling D1. Later: DEL-03-04 (W10), DEL-09-06 (W9).

Companion: [EXAMPLES.md](EXAMPLES.md) (DEL-02-01/WD-EX-v0.2).

---

## Changes from v0.1

Each change names the V1 item(s) it addresses. "R-n" is the binding
R1_RESOLUTIONS ruling applied.

| V1 item | Change in v0.2 | Where |
|---|---|---|
| V1-A D-01, V1-C D-17 (R-1) | Canonical act names adopted (A4 mark checked, A5 accept, A6 approve, A7 rely, A10 reject, A12 set grant, …). V4-CON-05 removed from the basis of *approve*; design-candidate approval is a separate later-increment act. "Accept professional reliance" replaced by A7 *rely*. | §2, §4.3.1, §4.3.2 |
| V1-A D-20 (R-1) | Closed list of acts a checkpoint may require: A4, A5, A6, A7, A12. | §4.3.1, FB-03 |
| V1-C D-01 BLOCKING (R-5) | New **reached-when** element: an observable condition of one of three kinds; prose position kept as explanation; unobserved → **not reached**. | §4.3.1, §4.3.5 |
| V1-C D-02 (R-5, R-6) | **Subject** now names a run-observable referent class; the satisfying act must be bound to that referent's content (change-item, subject or file content identity). | §4.3.1, §4.3.6 |
| V1-A D-10, V1-C D-03 (R-5) | Negative decision separated from *performed*: A10 → **resolved negatively**; for A4/A6/A7/A12 a person's decline is a recorded decline/stop event, not an act of that kind. | §4.3.4, §4.3.3 I-6 |
| V1-C D-04 (R-5) | Disposition vocabulary replaced by the shared one: waiting · performed · resolved negatively · lapsed · not reached · unknown. "awaiting act" → waiting; "run stopped" removed. | §4.3.4 |
| V1-A AB-03, V1-C D-05 (R-5) | Lapse may occur at any time after performance and is always recorded and presented; whether a lapse re-holds a run is owned by DEL-02-03. | §4.3.3 I-4 |
| V1-A D-09, V1-C D-07 (R-5, R-3) | New rule: a checkpoint requiring A5 on an operation's result forces that operation's treatment to *propose*, regardless of the grant; a direct request is **not permitted**, never silently converted. E2 R-5 and VC-11 rewritten. | §4.3.3 I-7, §4.2.2, EXAMPLES E2 |
| V1-A D-11, V1-C D-06 (R-5) | Evidence rule: satisfaction requires attributable act evidence from the capturing surface; faithful recording (A9) by another recorder is a conformant record that must cite that evidence; an agent-authored record alone never satisfies. | §4.3.3 I-5 |
| V1-C AB-01 (R-6) | Rule for item-level decisions at an A5 checkpoint (acceptance unit = change item). Proposed by DEL-02-01; confirmation by DEL-02-03 and DEL-03-02. | §4.3.7 |
| V1-A D-12, V1-C D-17 (R-4) | "agent-checked (non-mutating)" → "agent-examined (non-mutating)"; host results "host checks passed: ‹named checks›"; unqualified "checked" reserved for A4. | §4.4, EXAMPLES |
| V1-A §5, V1-C §6 (R-2; D2, D3) | D2 reserved acts applied; `UNRESOLVED{OI-001}` narrowed to operation-specific additions (OI-021) and host capture (DEP-001); `UNRESOLVED{OI-002}` closed by D3; A14 tool permission never satisfies a checkpoint. | §2, §4.3.2, §12 |
| V1-C D-09 (R-9, R-3) | Required-tool outcomes add **not exposed on this surface** and **channel not enabled**, distinct from **missing**; per-entry per-surface exposure element comes from DEL-03-01. | §4.2.4 |
| V1-C D-10 (R-9) | Identity carried as {kind, origin, source root, name, revision} (+ derived-from). A workflow carried unadapted keeps its original origin; "App-origin" is not an origin class. | §6.1, §6.4 |
| V1-C D-08 | Workflow-level **unsupported** (role/seat) outcome added beside the tool outcomes so the panel can present it. | §4.2.4, §4.7 |
| V1-C D-28 | §9 need sources updated to cite LOOP-v0.1/PANEL-v0.1 as quoted in V1-C; pointer row A-11 for catalog-schema argument checking (held by DEL-03-01). | §9 |
| V1-C AB-08 | Version compatibility limited to exact-version equality until DEL-03-01 supplies an ordering or range. | §4.2.2, U-07 |
| V1-B D-20 (R-9) | Examples re-labelled to the shared fixture FX-PIPE-01 (DEL-03-01 §10); divergences stated. | EXAMPLES |
| V1-C AB-10 | U-08 reassigned to after the W11 observations at pin 0.158.0 (D4). | §12 |

Not repaired here (routed to closeout C1 per R1_RESOLUTIONS): V1-C RF-3
(DEL-02-01 has no DOWNSTREAM rows) and RF-7 (U-08 co-owner row).

---

## 1. Reading this definition

**What it defines.** The meaning of a portable workflow's *declared part* and
its relation to the prose method. The four roles and the single host seat as
App and host consumers receive them. Workflow source identity and the
promised-versus-observed distinction. The shared-contract responsibility map
(OUT-003), with each consumer need and each open allocation labeled.

**What it does not define.** It does not choose a wire format, field names,
where the declared part is carried, JSON or TypeScript types, a parser, a
content-identity algorithm, a transport (MCP or CLI), persistence,
process/thread placement or shared-component placement. It does not define
catalog entries (DEL-03-01), act kinds or policy (DEL-04-01), proposal
outcomes (DEL-03-02), record fields (DEL-04-03), the checkpoint hold machine
or transfer behavior (DEL-02-03), registration (DEL-02-02), role supply
(DEL-02-04), loop events (DEL-05-01) or panel interactions (DEL-05-02).

**Naming convention.** Bold phrases such as **expected input** or
**reached-when** are *semantic element names*. They are not wire names, keys,
headings or type names. Act kinds use the canonical names A1–A14 per
R1_RESOLUTIONS R-1.

**Normative words.** "Shall" marks a meaning this contribution proposes.
"Settled" marks an accepted-basis distinction or an owner ruling, cited.
`UNRESOLVED{…}` marks an open owner choice, which is neither a permission nor
a default.

---

## 2. Settled distinctions this definition carries

| # | Settled distinction | Citation | Consequence for the declaration |
|---|---|---|---|
| S-A | A workflow is prose method guidance plus a declared part: expected inputs, host tools needed, checkpoints requiring a human act, returned outputs and evidence. | PRD V4-WF-01 | Five declared categories, prose retained (§3–4). |
| S-B | Workflows, skills and role guidance are ordinary open files (`WORKFLOW.md`, `SKILL.md`, `AGENTS.md`) readable by any capable harness; tool schemas stay open. | PRD V4-SHR-02; ARCH M-3 | The declared part must be readable without Chirality software (§3.2). |
| S-C | One workflow format and one set of four roles across the App and every host. | PRD V4-SHR-01, V4-ROLE-01 | No host-specific declaration dialect (§5). |
| S-D | Source-qualified identity: project, user, bundled or host-supplied; a selection is never silently rebound to a same-named workflow from another source. | PRD V4-WF-03 | Four origin classes; collisions exposed (§6). |
| S-E | The product can check that a selected workflow's required tools exist in the current host and tell the person when they do not. | PRD V4-WF-04 | Required tools are referenceable against the host catalog (§4.2). |
| S-F | At a declared checkpoint the required human act is requested; the run does not record it as done until the person performs it; checkpoints override autonomy. | PRD V4-WF-05; HI V4-HI-42 | Checkpoint hold is independent of the grant (§4.3). |
| S-G | `success` means the operation ran; a submitted proposal reports "queued" until the host records acceptance and application. | HI V4-HI-25 | Success never satisfies a checkpoint (I-2). |
| S-H | Applying a change, accepting an edit, marking work checked, engineering approval and professional reliance are distinct; agents may prepare but must not represent an unperformed human act as performed. | PRD V4-AUT-03; HI V4-HI-30/31; d3 | Each checkpoint names one act kind; evidence of one kind satisfies no other (I-1). |
| S-I | Proposals say "accept", never "approve". | HI V4-HI-33 | "Accept" wording stays with A5 only (R-1). |
| S-J | A human act binds to identified content, scope and purpose and lapses visibly when that content changes. | PRD V4-REC-05; HI V4-HI-32 | Checkpoint subjects are bound to observable referents (§4.3.6). |
| S-K | Only observed events are shown as having happened; unobserved outcomes are unknown. | PRD V4-EXE-03 | Promises are kept apart from observations (§4.6). |
| S-L | Nothing the agent produces is presented as certified, sealed, approved or code-compliant. | PRD V4-AUT-05 | Outputs cannot promise approval standing (§4.4). |
| S-M | Roles recede in hosts behind one agent seat and the selected workflow; each host carries its own workflows, skills and tools. | PRD V4-HOST-05/06 | Host seat and host origin (§5, §6). |
| S-N | Roles are supplied additively; a bounded executor does not delegate; unenforced limits are stated, not implied. | PRD V4-ROLE-02/03 | Role compatibility is declared, not claimed as enforced (§4.7, §5). |
| S-O | Shared meaning does not prescribe a common executable service; shared implementation needs a concrete repeated responsibility; placement is open. | ARCH V4-ARC-20; PRD V4-SHR-03; d2; OI-014 | Map records needs and leaves placement open (§9). |
| S-P | A run leaves a compact record linking host receipts rather than copying them. | PRD V4-REC-04; HI V4-HI-70/71 | Declared evidence is by reference (§4.5). |
| S-Q | Reserved to the person (App/shared contracts, first increment): (a) marking work checked (A4); (b) accepting a proposal wherever the active autonomy requires a proposal (A5); (c) engineering approval (A6); (d) relying on a result for a professional purpose (A7); (e) changing the autonomy grant or enabling external access (A12, A13). No grant widens past a reserved act or a declared checkpoint. The host names and enforces its own list; host adoption is not shown (DEP-001). | Owner ruling D2 (DECISION-1) | Every act a checkpoint may require is reserved to the person (§4.3.2). |
| S-R | App routine tool-permission and sandbox modes (including any classifier mode) are the user's own Codex setting; they govern tool execution only and never stand in for a reserved or professional act. Hosts have no classifier permission mode in the first increment; the SWB default proposal mode applies. | Owner ruling D3 (DECISION-1) | A14 never satisfies a checkpoint; a checkpoint is not a permission prompt (§4.3.2). |

---

## 3. The workflow package and its two parts

### 3.1 Parts

A portable workflow is one package whose entrypoint is `WORKFLOW.md` (S-B).

| Part | Job | Who reads it | Authority |
|---|---|---|---|
| **Prose method** | Explains purpose, applicability, method, branches, recovery, judgment and handoff. | People and agents. | Method guidance; it grants no permission (Root `create-workflow`, retained). |
| **Declared part** | States, in a form a product can observe, what the method expects, needs, stops for and returns. | People, agents and product consumers (requirement check, checkpoint hold, records, panel). | A declaration of expectations. It is not evidence that any expectation was met and grants no host permission. |

Both parts are required for a *declared* workflow. Where they disagree, the
consumer reports the inconsistency (FB-07) and does not silently prefer
either.

### 3.2 Readability obligations (OUT-001, OUT-002; REQ-001, REQ-002)

- **R-1** The declared part shall be readable as ordinary text by a person
  opening the package in an ordinary editor, without Chirality software,
  generated indexes or a running host (S-B).
- **R-2** Every declared element shall carry, or sit beside, a short
  human-readable statement of its meaning. An opaque reference alone, such as
  a catalog operation identity, is not enough.
- **R-3** The declared part shall live inside the package and travel with it.
  A derived index, registry or host database may reflect it but is not its
  authority.
- **R-4** Physical carriage is `UNRESOLVED` (U-01). Every option must satisfy
  R-1…R-3.

### 3.3 Declaration contract version

- **declaration contract version** identifies which version of this meaning
  the declared part is written against. Representation unselected.

### 3.4 Absent, partial and unrecognized declared parts

| Condition | Consumer meaning (all consumers) |
|---|---|
| No declared part (all current Root bundled workflows; any prose-only package) | The workflow is **undeclared**. It remains a readable, selectable method. Consumers report "requirements undeclared", never "no requirements". The required-tool check cannot pass, checkpoints cannot be product-held, and outputs/evidence carry no declared promise. |
| Declared part present, a category omitted | That category is **undeclared**. This differs from **declared empty** (an explicit statement that none are expected). Only "declared empty" supports "this workflow declares no checkpoints". |
| Unrecognized element or newer contract version | Preserve it unchanged and report it as unrecognized. An unrecognized element in the required-tool or checkpoint category makes the corresponding result **not established**, never a pass. |

---

## 4. Declared-part meaning

### 4.1 Expected inputs (SOW-042)

| Element | Meaning |
|---|---|
| **input name** | Local name, unique within the workflow. |
| **input meaning** | What the input is and why the method needs it. |
| **input kind** | One of: a host object or view obtained through a catalog read (see **required tool reference**); a file or document supplied to the run; a value or choice supplied by the person; an output of another identified workflow run. |
| **necessity** | Required, or optional with the effect of its absence stated. |
| **quality or basis requirement** | What must hold for the input to be usable. For a host read, the relied-on basis is DEL-03-01's read-basis descriptor (workspace identity, generation, model revision, canonical content identity; V4-HI-11). Generation is a host lineage epoch; an intervening edit changes the model revision, not the generation (per R1_RESOLUTIONS R-9; to be confirmed at IR1). |
| **stage** | Where in the method the input is needed, anchored to the prose. |

An expected input is a need, not a fetched value. Whether and on what basis it
was supplied is an observation (§4.6).

### 4.2 Required tools (SOW-043, SOW-039)

#### 4.2.1 Two tool classes

| Class | What it refers to | Supplier of meaning |
|---|---|---|
| **host operation requirement** | An operation in a host's capability catalog, referenced by its operation identity. | DEL-03-01 catalog C (V4-HI-02). The reference is **opaque** here. |
| **harness capability requirement** | A capability of the agent's harness that is not a host catalog operation (e.g., file writing or native delegation in the App's Codex). | `UNRESOLVED` (U-08). |

A workflow designed for a host names host operations. An external agent (the
App's Codex through a host's MCP or CLI surface, V4-HI-50) reaches the same
catalog operations, and the declaration still references the catalog
identity, never an adapter-specific tool name.

#### 4.2.2 Elements of a required tool reference

| Element | Meaning |
|---|---|
| **tool reference** | Opaque reference to a DEL-03-01 operation identity (host class) or to a harness capability. |
| **version compatibility** | Optional. At v0.2 only an exact version (or set of exact versions) can be stated, because C defines version equality but no ordering or range (V1-C AB-08; U-07). |
| **purpose of use** | Readable: what the method uses the operation for. It does **not** restate the operation's class or treatment; those come from the catalog entry, adopted policy (DEL-04-01) and the person's grant (V4-HI-40). |
| **necessity** | Required, or optional with a stated fallback or limitation. |
| **stage** | Where in the method the tool is used. |
| **checkpoint-forced treatment** (derived, not authored) | If any checkpoint in the workflow requires A5 on this operation's result, consumers shall treat the operation as *propose* for that run regardless of the grant (I-7). The declaration does not state a treatment; this element is derived from the checkpoint declaration so consumers can see it. How it reaches the host route is U-19. |

#### 4.2.3 Requirement is not restriction

Root `execution.json` `tools.capabilities` and `tools.commands` are
**restrictions**: a ceiling that intersects outer policy ("empty restriction
lists deny rather than grant"; AGENT_WORKFLOW_RUNTIME.md). V4-WF-01 "the host
tools it needs" is a **requirement**: a floor the current host must meet.
These shall remain distinct. A consumer shall not read one as the other
(FB-05; EXAMPLES E6).

#### 4.2.4 Compatibility outcomes a consumer may report (meaning only)

The check itself is DEL-02-03's (its REQ-001). This contract supplies the
vocabulary. The runtime non-success outcomes *unavailable*, *channel not
enabled*, *not permitted* and *error* are C §4.1's, used unchanged (per
R1_RESOLUTIONS R-3/R-9; to be confirmed at IR1).

| Outcome | Level | Meaning |
|---|---|---|
| **present** | per requirement | The operation exists in the current host's catalog and is exposed on the acting surface. |
| **missing** | per requirement | Not in the current host's catalog. Reported with the requirement's purpose line (S-E). |
| **not exposed on this surface** | per requirement | In the catalog, but DEL-03-01's per-entry, per-surface exposure element says it is not exposed on the acting surface. If that element's value is "unagreed", the outcome is **not established** (per R1_RESOLUTIONS R-9). |
| **channel not enabled** | per surface | The surface itself is off (external access not enabled; A13 not performed). Never encoded as missing or unavailable (C §4.1). |
| **version mismatch** | per requirement | Present, but not at a declared compatible version. |
| **present, currently unavailable** | per requirement, at run time | Present, but preconditions do not hold now; reported with the catalog's unavailable reason (V4-HI-04). A run-time condition, not a missing requirement. |
| **not established** | per requirement | Cannot be evaluated: undeclared, unrecognized element, catalog unreadable, reference unresolved, or exposure unagreed. Never reported as present. |
| **unsupported** | per workflow | The workflow's compatible roles or delegation need cannot be met by the acting seat (§4.7, §5.3). |

Whether a newly added operation becomes available on all three surfaces
without separate work is `UNRESOLVED{OI-003}`; the declaration never assumes
it (U-16).

### 4.3 Checkpoints requiring human acts (SOW-044; REQ-003)

#### 4.3.1 Elements

| Element | Meaning |
|---|---|
| **checkpoint name** | Stable within the workflow's revision; identifies the checkpoint across interruption, replay and adaptation (DEL-02-03 REQ-002). |
| **required act kind** | Exactly one of the closed list **A4 mark checked**, **A5 accept**, **A6 approve**, **A7 rely**, **A12 set grant** (per R1_RESOLUTIONS R-1; to be confirmed at IR1). *Approve* means engineering approval only (V4-HI-30/33); design-candidate approval (V4-CON-05, V4-HI-65) is a separate later-increment act and cannot be required here. |
| **reached-when** | The observable condition that marks arrival, of one of three kinds: (a) before dispatch of a named **required tool reference**; (b) on observed production of a named **declared output**; (c) on an observed host outcome of a named operation (e.g., *proposal queued*). Meaning only; how a consumer observes it is DEL-05-01 (host) and DEL-02-03 (App) (per R1_RESOLUTIONS R-5). |
| **position** | Where in the method the checkpoint sits, anchored to the prose. Explanation only; arrival is decided by **reached-when**. |
| **subject** | A run-observable referent class, e.g., "the change items of the proposal(s) this run submitted through ‹required tool reference›", "the rows affected by the receipt of output ‹name›", "declared output ‹name›", "the grant proposed at stage ‹x›". Bound at run time to concrete referents (§4.3.6). |
| **scope** | The extent of the subject covered, e.g., one item, several items or a whole proposal (V4-HI-41 granularity; acceptance unit = change item, R-6). |
| **purpose** | Why the act is requested here, in words the person reads when asked (bound with the act, V4-REC-05). |
| **actor requirement** | "The person" by default; "the accountable professional" for A7 (V4-AUT-05). A class, never an identity. |
| **on negative decision** | What the method does after a negative resolution (A10 for A5) or a decline/stop event (A4, A6, A7, A12): stop, return to a named stage, or proceed on a stated branch. Absent this element, the run stops at the checkpoint. It never proceeds as if the act were positive. |
| **on mixed decision** (A5 only, optional) | What the method does when some items are accepted and some rejected (§4.3.7). Absent, the mixed case follows **on negative decision** for the rejected items. |
| **expected act evidence** | The act record expected (DEL-04-03 human-act record meaning), with its capturing surface (I-5). A declaration, not a record. |

#### 4.3.2 What a checkpoint is and is not

- A checkpoint **names** a human act the run waits for. It does not perform,
  record or imply the act.
- Every act kind in the closed list is reserved to the person under D2 (S-Q).
  A checkpoint does not extend or narrow that list. Operation-specific
  additions for the first connected operation remain `UNRESOLVED{OI-021}`.
- Naming A1 propose, A2 apply, A3 examine, A8 request, A9 record, A10 reject,
  A11 withdraw, A13 enable external access or A14 answer tool permission as a
  checkpoint's required act is invalid (FB-03). An agent's examination
  findings are not an A4 act (V4-EXM-21; R-4).
- A checkpoint is not a tool-permission prompt. An A14 answer, whether from the
  person or from the user's own Codex mode, never satisfies a checkpoint (S-R).
  Hosts have no classifier mode (D3).

#### 4.3.3 Independence rules

- **I-1 One kind, one evidence.** A checkpoint is satisfied only by evidence
  of its own act kind, by a qualifying actor, bound to its bound subject's
  current content. Evidence of another kind satisfies nothing here (S-H).
- **I-2 No success inference.** Operation success, a queued proposal, a
  receipt of application, host checks passed or an agent's examination
  supplies no human act (S-G; d3).
- **I-3 No synthetic ordering.** The contract imposes no rule that A5 must
  precede A4, A6 or A7. An independently evidenced act counts on its own
  evidence. A workflow may place checkpoints in a method order; that order is
  the workflow's visible declared method. The proposal lifecycle's
  accepted → applied sequence (V4-HI-23) is an operation lifecycle, not a
  checkpoint ordering rule.
- **I-4 Lapse at any time.** If bound content changes after the act, at any
  time after performance, the act lapses visibly and the disposition becomes
  **lapsed**. Lapse is always recorded and presented. Whether and how a lapse
  re-holds a run that has already passed the checkpoint is owned by DEL-02-03
  (per R1_RESOLUTIONS R-5; U-22). Applying an accepted change item does not
  lapse its A5, because A5 binds to the change-item content identity; a basis
  failure between acceptance and application falls under the stale rule, not
  lapse (per R1_RESOLUTIONS R-6).
- **I-5 Capturing-surface evidence.** Satisfaction requires attributable act
  evidence from the **capturing surface**: the host's act facility for acts
  on host content (V4-HI-31), or the App interface for acts in the App.
  Faithful recording (A9) by any identified recorder distinct from the
  decision actor is a conformant record shape (settled; V4-AUT-03), but such
  a record must cite the capturing surface's evidence. An agent-authored
  record, or a statement in conversation, never satisfies a checkpoint by
  itself. Any host-specific capture requirement is the host's (DEP-001) (per
  R1_RESOLUTIONS R-5).
- **I-6 Negative decisions.** For A5 the negative decision is A10 reject,
  itself a human act reserved to the person wherever A5 is (per
  R1_RESOLUTIONS R-1). For A4, A6, A7 and A12 there is no negative act kind:
  a person's decision not to act is a recorded decline/stop event, which does
  not satisfy the checkpoint. Its recording is also subject to I-5.
- **I-7 An acceptance checkpoint forces a proposal.** If a checkpoint requires
  A5 on an operation's result, that operation's treatment is *propose*
  regardless of the grant (DERIVED from V4-HI-42 and D2(b), per
  R1_RESOLUTIONS R-5). A request to apply it directly is **not permitted**
  (naming the governing treatment); it is never silently converted into a
  proposal (per R1_RESOLUTIONS R-3). A workflow that wants direct application
  under a grant with a later human act declares a checkpoint on the applied
  result instead (e.g., A4 on applied rows).

#### 4.3.4 Disposition vocabulary (shared; per R1_RESOLUTIONS R-5)

| Disposition | Meaning |
|---|---|
| **not reached** | The reached-when condition has not been observed. If the run ends without observing it, the final disposition is **not reached**, never performed. |
| **waiting** | Reached; the act is requested; the run holds. If the run ends while waiting, the final disposition stays **waiting** with a run-ended event (U-21). |
| **performed** | Capturing-surface evidence of the required act kind, by a qualifying actor, bound to the current content of every bound referent in scope. |
| **resolved negatively** | For A5: A10 evidence covers the bound items (fully or, under §4.3.7, in part). For A4/A6/A7/A12: a recorded decline/stop event (placing the decline under this disposition is DEL-02-01's reading of R-5; confirm at IR1). The **on negative decision** path governs. Never counted as performed. |
| **lapsed** | A performed act's bound content changed afterwards (I-4), for all or some referents. |
| **unknown** | Whether the act was performed cannot be established (e.g., record unavailable after interruption). Never presented as performed (S-K). |

The hold state machine, re-hold and replay behavior are DEL-02-03's (W7).

#### 4.3.5 Reached-when evaluation rules (meaning only)

- **RW-1** Arrival is observed, never inferred from model text or prose
  stage (V1-C D-01; LOOP E-1 as quoted in V1-C).
- **RW-2** Kind (a) is evaluated before the named operation is dispatched;
  the dispatch waits. Kind (b) needs the output's production to be observed
  (e.g., host result returned). Kind (c) needs the named host outcome as
  reported under P §9 (e.g., *queued*).
- **RW-3** If a reached-when names a tool or output that this workflow does
  not declare, the checkpoint is invalid (FB-13).
- **RW-4** A checkpoint may be reached more than once in a run (e.g., after a
  re-draft). Each arrival binds its own referents (§4.3.6); earlier
  dispositions remain history.

#### 4.3.6 Subject binding

- **SB-1** At arrival, the subject class is bound to concrete referents
  observed in this run: proposal change items (by proposal and item
  identity), rows/objects (by the receipt that produced or changed them), a
  declared output, or a grant setting.
- **SB-2** The satisfying act must be bound to the same referents' content.
  The content-identity source follows the referent (per R1_RESOLUTIONS R-6;
  to be confirmed at IR1): the **change-item content identity** (DEL-03-02:
  operation identity and version, bound targets, old/new values, relied-on
  basis) for A5/A10; the **subject content identity** (DEL-03-01, per row or
  object, host-supplied) for A4, A6, A7 on host content; the **file content
  identity** for App files. Each identity carries its **identity method
  designation**. Algorithms remain unselected.
- **SB-3** An act on other content, another proposal or another row set does
  not satisfy the checkpoint, even if its kind matches (VC-21).
- **SB-4** For A12 the referent is the grant setting the checkpoint concerns.
  Its content identity and lapse meaning are not yet defined by any supplier
  (U-27).

#### 4.3.7 Item-level decisions at an A5 checkpoint (proposed; U-20)

The acceptance unit is the change item. Row-by-row acceptance is one A5 per
item; batch or multi-row acceptance is one A5 act listing several items, each
item-bound, with per-item lapse (per R1_RESOLUTIONS R-6). For a checkpoint
whose subject is the items of one or more proposals:

| Item state at evaluation | Checkpoint disposition |
|---|---|
| Every bound item has A5 on current content | **performed** |
| At least one bound item has neither A5 nor A10 yet | **waiting** |
| Every bound item has A5 or A10, and at least one has A10 | **resolved negatively** (partial if some A5). **on mixed decision** governs if declared. Accepted items keep their A5 and proceed through the host lifecycle unaffected. |
| An item leaves the queue without a decision (stale refusal, A11 withdrawal, host refusal) | The item leaves the bound subject with a recorded event. If no bound items remain, the checkpoint stays **waiting** until a new arrival binds new items (RW-4) or the run ends (U-21). |

This rule is DEL-02-01's v0.2 proposal. DEL-02-03 (hold machine, W7) and
DEL-03-02 (item dispositions, P §9) confirm or return a finding.

### 4.4 Returned outputs (SOW-045)

| Element | Meaning |
|---|---|
| **output name / meaning** | Local name and readable description. |
| **output form** | A change to host objects (always through the host's one route: proposal, or direct application under an effective direct treatment, V4-HI-20…23); a file or document; a report or message to the person; an input to another workflow. |
| **destination** | Host tables/views, the project, or the conversation. Host-changing outputs appear in the host's own views; there is no agent-private surface (V4-HOST-04). |
| **promised standing** | From the non-approval vocabulary, aligned with P §9 (per R1_RESOLUTIONS R-7): *queued*; *applied (receipt)*; *agent-prepared*; *agent-examined (non-mutating)*; *host checks passed: ‹named checks›* (only as the host reports, each with its evaluated basis). Never *approved*, *certified*, *sealed* or *code-compliant* (S-L). Unqualified "checked" is used only for A4 (R-4). A human-act standing (e.g., *marked checked by the person*) can only be promised conditional on a named checkpoint. |
| **gating checkpoint** | Optional reference to the checkpoint whose act the promised standing depends on. |

### 4.5 Returned evidence (SOW-045)

| Element | Meaning |
|---|---|
| **evidence name / meaning** | What the evidence shows and for which output or checkpoint. |
| **evidence kind** | Host receipt reference; relied-on read-basis reference (V4-HI-11/21); evaluated basis of a non-success outcome; host check result reference; human-act record reference (with capturing surface); run record reference. |
| **by reference** | Host receipts, hashes and origin marks remain host-owned; declared evidence names a link, not a copy (S-P). |
| **supports** | Which output(s) or checkpoint(s) it supports. Evidence for one act supports no other (I-1). |

### 4.6 Promised versus observed (REQ-004; AC-004)

| Declared promise | Observed counterpart | Observation owner | Absent observation means |
|---|---|---|---|
| expected input | input actually supplied, with its basis | run record (DEL-04-03); read basis (DEL-03-01) | "not supplied" / "basis unknown" |
| required tool reference | compatibility outcome (§4.2.4), then operations requested and their P §9 outcomes | DEL-02-03 check; run record | "not established" |
| checkpoint | disposition (§4.3.4), bound referents and act record references | DEL-02-03 (App) / DEL-05-01 (host); DEL-04-03 | "not reached", "waiting" or "unknown", never "performed" |
| output with promised standing | produced output and actual standing (queued, applied (receipt), refused, stale, application error, outcome unknown …) | host; run record | "not produced" or "outcome unknown", attributed to the observer that lost observation (R-7) |
| evidence | linked receipt or record actually present | host; run record | "missing"; never a pass |

### 4.7 Compatible roles and restrictions (retained from Root)

| Element | Meaning |
|---|---|
| **compatible roles** | Which of the four roles the method is written for (Root `compatible_roles`, retained). Omission inherits compatibility; it never expands a role. |
| **tool restriction** | Optional ceiling narrowing the tools the method may use (Root `tools`, retained as a restriction, distinct from §4.2). |
| **enforcement statement** | None in the declaration. Metadata never proves enforcement. Where a harness or host cannot enforce a restriction, the consumer reports it as instruction-asserted (S-N). |

A workflow requiring delegation is compatible only with a role and seat that
can delegate. In a host seat without delegation, it is **unsupported**
(§4.2.4), never silently run without delegation.

---

## 5. The four roles and the single host seat (SOW-021, SOW-022; REQ-001; AC-001)

### 5.1 Common meaning (settled)

| Role | Meaning (V4-ROLE-01) |
|---|---|
| HELP_HUMAN | Alignment with the human |
| HELPS_HUMANS | Design |
| WORKING_ITEMS | Managed execution |
| TASK | Bounded execution; does not delegate (V4-ROLE-03) |

No fifth role: a domain expression such as the SWB Piping Designer
specializes context, tools and workflows within these roles (V4-ROLE-03).
Role guidance is supplied additively (V4-ROLE-02); supply is DEL-02-04's.

### 5.2 Expressions

| Aspect | Chirality App | Host application (e.g., SWBPIPE) |
|---|---|---|
| Role presence | Person selects a role (DEL-02-04). | Roles recede behind **one agent seat** and the selected workflow (S-M). The host need not present a role choice (REQ-001). |
| Guidance files | Product `AGENTS.md` plus role guidance. | The host's own `AGENTS.md` and `SKILL.md` (V4-HOST-06), open and readable (S-B). Distribution/adoption is `UNRESOLVED{OI-018}`. |
| Workflows | Project, user, bundled; host-origin when opened in App (V4-WF-06). | The host's own library (origin *host*); App workflows carried in unadapted keep their origin, adapted ones become host-origin (§6.4). |
| Tools | Codex native tools; host operations through an external surface (V4-HI-50). | The host's capability catalog (V4-HI-01). |
| Permission modes | Routine tool permission and sandbox are the user's own Codex setting (D3). | No classifier permission mode; SWB default proposal mode (D3; V4-HI-41). |
| Delegation | Native delegation for roles permitted to delegate. | Host-defined; absent it, delegation-requiring workflows are **unsupported**. |

### 5.3 What the single seat must still carry

- **SEAT-1** The role meaning under which the seat operates for a run shall
  be determinable from the host's guidance and the selected workflow's
  **compatible roles**, and recorded with the run. Every dispatch carries it
  (per R1_RESOLUTIONS R-7; loop element is DEL-05-01's). If it cannot be
  determined, the record says **unknown**.
- **SEAT-2** The mapping from the host's single seat to the four role
  meanings is `UNRESOLVED` (U-09). Options: (a) the seat always runs as a
  TASK-equivalent bounded executor of the selected workflow; (b) the seat
  takes the role named by the workflow's compatible roles; (c) host guidance
  names one standing role per conversation. No option is chosen.
- **SEAT-3** Receding does not remove the distinctions: the seat's acts
  remain execution; the person's acts remain the person's (S-H, S-Q).

---

## 6. Source identity (REQ-001, REQ-004; AC-004)

### 6.1 The identity tuple (per R1_RESOLUTIONS R-9)

Workflow identity is carried everywhere as {**kind**, **origin**, **source
root**, **name**, **revision**}, plus **derived-from** where applicable.

| Element | Meaning |
|---|---|
| **kind** | Workflow (distinct from skill; Root `kind`, retained). |
| **origin** | *project*, *user*, *bundled* or *host* (S-D). "App-origin" is not an origin class. |
| **source root** | Which library within the origin: the project root, the user's library, the App bundle and its release, or the host application and its library. Root `sourceRootId` meaning retained; values unselected. |
| **name** | Package name, matching its folder. |
| **revision** | Identity of the exact package content selected (all files in the package), with its identity method designation. Algorithm and multi-file canonicalization `UNRESOLVED` (U-03). A name plus origin without revision identifies a library slot, not selected content. |
| **derived-from** | For an adapted workflow: the full identity tuple of the workflow it was adapted from. Adaptation creates a new identity; it never edits the original's history. |

Other contracts that carry a workflow "identity/version" (P origin, LOOP run
association, PANEL selection) replace it with this tuple, per R1_RESOLUTIONS
R-9.

### 6.2 The identity chain: promised versus observed

| Link | Fact | Typical owner of evidence |
|---|---|---|
| **listed** | A library reports the workflow exists. | Discovery (DEL-02-02 App; host library) |
| **selected** | The person (or brief) chose a full identity tuple. | Selection (DEL-02-02; host panel DEL-05-02) |
| **resolved** | That identity resolved to specific revision content. | Resolver (placement open, §9) |
| **supplied** | Those bytes were actually supplied to the agent/loop, with their content identity per thread/turn. | App: DEL-02-04 / DEL-01-01 (supplied-guidance evidence per R1_RESOLUTIONS R-10); host: host loop (DEL-05-01 receiving) |
| **adopted by provider** | The model/harness took it up. Often unobservable; then **unknown**. | Stated as a limit |
| **observed behavior** | What the run actually did. | Run record (DEL-04-03); host evidence |

A matching name at two links establishes nothing about the others (AX-002).

### 6.3 Collision and rebinding rules

- **C-1** Every discovery that finds more than one origin for a name exposes
  all origins (Root runtime, retained).
- **C-2** A selection holds its full identity tuple. Later discovery of a
  same-named workflow in any origin is reported as a collision and never
  rebinds the selection (S-D).
- **C-3** Only an explicit new selection by the person changes what is
  selected; that is a new selection event, not a rebinding.
- **C-4** Whether a selection follows a new revision of the same slot or
  stays pinned is a selection policy of DEL-02-02 (App) and the host; the
  chain shall make visible which occurred (U-10).
- **C-5** Where *host* sits in unqualified-name precedence is `UNRESOLVED`
  (U-10). Source-qualified selection makes precedence irrelevant to
  correctness.

### 6.4 Carried and adapted workflows (V4-WF-06; per R1_RESOLUTIONS R-9)

| Case | Identity | Holding library |
|---|---|---|
| Carried **unadapted** into a host | Unchanged: original origin, source root, name, revision. | The host library now holding the copy is recorded as a **holding library** fact beside the identity, not as part of it (proposal, U-24). |
| **Adapted** in a host | New identity: origin *host*, host source root, revised revision, **derived-from** = the original tuple. | Same as source root. |
| Host workflow opened and refined in the App | Opening keeps the host identity. A refinement is a draft (DEL-02-02) and, once registered, a new identity with derived-from = the host tuple. | App library where registered. |

Examples: EXAMPLES E3, E4.

---

## 7. Root conventions: keep, change or leave open

Root material is a reuse source, not v4 authority (PRD V4-CST-04; ARCH §5).

| Root convention (source) | v4 declaration | Why |
|---|---|---|
| Package = immediate folder containing `WORKFLOW.md`; name matches folder (SPEC §9.3; runtime "Workflow packages") | **Keep** | Satisfies V4-SHR-02; existing consumers read it. |
| Name rule 1–64 lowercase letters/digits in hyphen-separated segments (`catalog.schema.json`; `create-workflow`) | **Keep as reuse candidate**; confirm in OUT-004 fixtures | Source compatibility; no v4 reason to differ. |
| YAML front matter `name`, `description` (`WORKFLOW_TEMPLATE.md`) | **Keep**; declared-part carriage **open** (U-01) | Description supports selection; carriage is a representation choice. |
| Free prose body, no prescribed headings | **Keep** | V4-WF-01 retains prose. |
| Inputs, outputs, checks and human checkpoints stated only in prose | **Change**: add the declared part, keep the prose | V4-WF-01 requires an observable declared part. |
| `execution.json` `compatible_roles` | **Keep** (§4.7) | Four roles are common. |
| `execution.json` `tools.capabilities` | **Keep as restriction only**; not reused as required tools | Restriction ≠ requirement (§4.2.3). |
| `execution.json` `tools.commands` | **Leave out** of the portable declaration | Repository-specific; not portable. |
| "Metadata never proves host enforcement" | **Keep** | S-N. |
| Origins `project`/`user`/`bundled` and `sourceRootId` | **Change**: add *host*; add revision and derived-from; carried-unadapted keeps origin | V4-WF-03/06; REQ-004; R-9. |
| Unqualified precedence project → user → bundled | **Leave open** for *host* (U-10) | Not decided by the basis. |
| Source-qualified identity; no silent rebinding; all collision origins exposed | **Keep** | Same as V4-WF-03. |
| `selected-context` fingerprints | **Keep the idea** as revision; algorithm open (U-03) | Needed for promised-vs-observed. |
| Drafts in `.chirality/workflow-drafts/`, panel registration, no overwrite | **Not part of this contract**; DEL-02-02 | V4-WF-02 is DEL-02-02's. |
| `catalog.yaml` navigation, `centralWorkflowNames` | **Leave out** | Library navigation, not declaration meaning. |
| Derived `index.json` | **Keep principle**: derived, never authority | R-3 (§3.2). |
| Legacy `TaskSkill`, `legacy-methods.json` | **Leave out** | Root compatibility only. |
| Four-section role files `AGENT_<ROLE>.md` | **Leave to DEL-02-04 / OI-018** | Role-guidance structure and distribution are not this contract's. |
| Human checkpoints in Root prose (e.g., `create-workflow` review before registration) | **Change**: product-held only when declared with reached-when, subject and act kind | Prose alone cannot be observed (RW-1). |

---

## 8. What each receiver receives from this contribution

| Receiver | Receives from WD-v0.2 | Expected check at IR1 / next comparison |
|---|---|---|
| DEL-02-03 execution (W7) | §4.2 references, derived forced treatment and outcome vocabulary; §4.3 checkpoint elements incl. reached-when, subject binding, I-1…I-7, §4.3.4 dispositions, §4.3.7 item rule; §6.4 carried/adapted identity | Hold machine, re-hold on lapse (U-22), item rule (U-20), run-end disposition (U-21), App-side capture (U-25) |
| DEL-05-01 loop | §4.3.1 reached-when kinds, §4.3.5, §4.3.6 subject binding, §4.3.4 dispositions, I-5 capturing surface, I-7 forced treatment; §5.3 SEAT-1; §6.1 tuple | Loop evaluates reached-when and binding; carries seat role meaning and identity tuple |
| DEL-05-02 panel | §4.2.4 outcomes incl. undeclared/declared empty/unsupported/not exposed/channel not enabled; §4.3.4 dispositions; §4.4 standing labels; §6.1 and §6.3 | Workflow selection, checks and wording |
| DEL-02-02, DEL-02-04 (later undertaking per D1) | §3, §6, §4.6; §5 | Not exercised in this undertaking |
| DEL-02-01 self | Whole contribution | §13 cases |

Expected **from** suppliers:

| Supplier | Element | State at v0.2 | Used in |
|---|---|---|---|
| DEL-04-01 | Canonical act names A1–A14, checkpoint-requirable closed list, decision pairs, decline/stop event, D2/D3 adopted records | Per R1_RESOLUTIONS R-1, R-2, R-5; DEL-04-01 v0.2 not read; confirm at IR1 | §4.3 |
| DEL-03-01 | Operation identity/version (equality only), per-entry per-surface exposure, C §4.1 outcomes, subject content identity, identity method designation, read basis, FX-PIPE-01 catalogue | Per R-3, R-6, R-9; C v0.2 not read | §4.1, §4.2, §4.3.6, EXAMPLES |
| DEL-03-02 | P §9 outcome taxonomy, change-item content identity, item dispositions | Per R-6, R-7; P v0.2 not read | §4.3.6, §4.3.7, §4.4, §4.6 |
| DEL-04-03 | Human-act record with capturing surface and recording mode; L-1 content-identity sources | Per R-5, R-6, R-8; not read | §4.3, §4.6 |
| DEL-05-01, DEL-05-02 | Loop/panel consumer needs | As quoted in V1-C only | §9 |
| DEL-01-01 | Supplied-guidance identity evidence; harness capability inventory at 0.158.0 (W11) | Per R-10; not read | §6.2, U-08 |
| SWBPIPE owner (external) | Host library, seat conduct, host act facility and capture requirements | None received | §5, §6, I-5, U-09 |

---

## 9. Shared contract/component responsibility map (OUT-003; REQ-005; AC-005)

Columns as in v0.1: consumers and need source; repeated responsibility;
maintenance rationale (d2: local implementations need conformance work; a
library couples releases; a service adds process, availability and upgrade
coordination); candidate (semantic, not a decision); confirmation (actual
owner response); placement. A V1 comparison is a review record, not an owner
confirmation, so every Confirmation cell remains "None".

| # | Contract part (semantic owner) | Consumers and need source | Repeated responsibility | Maintenance rationale | Candidate | Confirmation | Placement |
|---|---|---|---|---|---|---|---|
| A-1 | Declared-part meaning (DEL-02-01) | DEL-02-03 (SoW; W7 pending), DEL-05-01 (LOOP-v0.1 §2.4 checkpoint consumption, as quoted in V1-C J1/J2), DEL-05-02 (PANEL-v0.1 §3.2 selection, as quoted in V1-C J3/D-08), DEL-02-02 (SoW; later undertaking), host loop/panel (external; none received) | Read the five categories, undeclared/empty states and reached-when | Divergent readers would disagree on undeclared vs empty and on arrival; a correctness risk | Shared declared-part reading type(s) and parser/validator; conformance fixtures regardless | None | `UNRESOLVED{OI-014}` |
| A-2 | Workflow identity tuple and chain (DEL-02-01) | DEL-02-03, DEL-03-02 (P origin, per R-9), DEL-04-03, DEL-05-01 (run association), DEL-05-02 (PANEL §6 "Source-qualified workflow identity presentation … Plausible", as quoted in V1-C D-28), DEL-02-02/02-04 (later), host library (external) | Carry the tuple; detect collisions; never rebind | Identity drift silently breaks V4-WF-03; a shared type is low-coupling | Shared workflow identity type; collision report meaning | None | `UNRESOLVED{OI-014}` |
| A-3 | Checkpoint declaration meaning (DEL-02-01) with act names (DEL-04-01) | DEL-02-03, DEL-05-01 (LOOP C-1…C-4 as quoted in V1-C), DEL-05-02 (PANEL W-5), DEL-04-03, host (external) | Name act kind, reached-when, subject class; apply I-1…I-7 | Independence rules erode locally (success→act); shared definition and shared negative fixtures limit that | Shared checkpoint declaration type; shared negative fixtures | None | `UNRESOLVED{OI-014}` |
| A-4 | Checkpoint hold machine (DEL-02-03) | App run (DEL-02-03), host loop (DEL-05-01 receiving; external construction) | Wait/advance/lapse/unknown/re-hold | Shared execution couples App and host loop lifecycles; d2 needs a concrete shared stateful responsibility first | Possibly shared; not proposed | None | `UNRESOLVED{OI-014}`; host side `UNRESOLVED{OI-013}` |
| A-5 | Compatibility outcome vocabulary (DEL-02-01) over C identities and exposure (DEL-03-01) | DEL-02-03 (check), DEL-05-02 (PANEL consumes §4.2.4 per V1-C D-08), DEL-02-02 (later), host (external) | Report §4.2.4 outcomes truthfully | Vocabulary must match C exactly; checker code may stay local | Shared outcome vocabulary type; checker placement open | None | `UNRESOLVED{OI-014}` |
| A-6 | Role meaning and compatible roles (DEL-02-01; supply DEL-02-04) | DEL-02-04 (later), DEL-02-03, DEL-05-01 (seat role on dispatch, R-7), host seat (external) | Name four roles; read compatible roles; report unsupported | Tiny, stable meaning; cheap to share; enforcement stays per harness | Shared role identity set | None | `UNRESOLVED{OI-014}` |
| A-7 | Human-act and run record (DEL-04-03) | All above | Semantic owner is DEL-04-03 | Recorded here to keep the owner visible | Owned by DEL-04-03's allocation | n/a | DEL-04-03 / `UNRESOLVED{OI-014}` |
| A-8 | Catalog entry, exposure and read basis (DEL-03-01) | All above | Semantic owner is DEL-03-01 | As A-7 | Owned by DEL-03-01's allocation | n/a | DEL-03-01 / `UNRESOLVED{OI-014}` |
| A-9 | Host loop use of declarations (external construction; DEL-05-01 receiving) | Host loop (LOOP-v0.1 §10.1 rows, per V1-C D-21) | Parse the declared part in the host; evaluate reached-when; persist runs | Loop placement, parsing and persistence are host choices | None proposed | None | `UNRESOLVED{OI-013}` |
| A-10 | Panel workflow selection and checks (external construction; DEL-05-02 receiving) | Host panel; possibly App views (PANEL §6, per V1-C D-28) | Present selection, identity, collisions, checkpoint requests with "accept" wording and shared dispositions | Reusable components only on agreed repeated purpose (DEL-05-02 OUT-004) | Possibly shared presentational components; not proposed | None | `UNRESOLVED{OI-014}`, `UNRESOLVED{OI-013}` |
| A-11 | Catalog-schema argument checking (DEL-03-01; raised as LOOP §10.2 candidate (b), per V1-C D-28) | DEL-05-01, host (external), external adapter (DEL-03-03) | Check call arguments against the catalog schema before host domain validation | Pointer row only: DEL-03-01 holds it as a question in its C §8 map | Held by DEL-03-01 | None | `UNRESOLVED{OI-014}` |

Allocation result at v0.2: the map names every row's consumers and open
placement. **No** common implementation or service is proposed, and no row is
represented as agreed (AC-005).

---

## 10. Excluded acts and their owners (REQ-006; AC-006)

| Act excluded from DEL-02-01 | Owner | Receiving interface in this contract |
|---|---|---|
| Catalog-semantic definition (identity, version, exposure, availability, standing, read basis, content identities) | DEL-03-01 | §4.2 opaque references; §4.1; §4.3.6 |
| Proposal/outcome definition (P §9, change items) | DEL-03-02 | §4.3.6, §4.3.7, §4.4, §4.6 |
| Operation-policy definition; canonical act names; carrying adopted D2/D3 | DEL-04-01 | §4.3.1 closed list; §2 S-Q/S-R |
| Operation-specific reserved additions | Owner via outside SWB session (`UNRESOLVED{OI-021}`) | §4.3.2 |
| Human-act and run-record field definition; record implementation | DEL-04-03 | §4.3.1 expected act evidence; §4.5; §4.6; §5.3 |
| Checkpoint hold machine, re-hold, required-tool check, transfer | DEL-02-03 | §4.2.4, §4.3.4, §4.3.7, §6.4 |
| Loop receiving design (arrival observation, binding step) | DEL-05-01 | §4.3.5, §4.3.6, §9 A-9 |
| Panel receiving design | DEL-05-02 | §9 A-10 |
| App workflow workspace and registration | DEL-02-02 (later undertaking, D1) | §6.3 C-4/C-5; §7 |
| Role selection and supply | DEL-02-04 (later undertaking, D1) | §5 |
| Host catalog, domain validation/application, receipts, loop, panel, tables, views, act facility and capture requirements | External SWBPIPE implementation owner | §4.5; I-5; §5.2 |
| Performing marking checked, acceptance, rejection, approval, reliance, grant change | The person; professional assertions by the accountable professional | §4.3 (declaration names, never performs) |
| Shared placement decisions | App/shared contract owners (OI-014); with SWB implementation owner (OI-013) | §9 |

---

## 11. Failure behavior (consumer-facing meaning)

| ID | Condition | Required behavior |
|---|---|---|
| FB-01 | Declared part absent or a category omitted | Report **undeclared**; never "none". |
| FB-02 | Declared part unreadable or malformed | Workflow stays a prose method; declared part **not established**; report the defect; no partial interpretation that could pass a check. |
| FB-03 | Checkpoint names an act kind outside {A4, A5, A6, A7, A12}, or none | Invalid checkpoint; report; no execution outcome can satisfy it. |
| FB-04 | Checkpoint names an act kind the consumer does not recognize | Preserve; **not established**; never substitute a nearby kind. |
| FB-05 | Root `tools` restriction present, required tools undeclared | Required-tool check **not established**; restriction honored as ceiling. |
| FB-06 | Tool reference does not resolve against the current catalog | **missing** (or **not established** if the catalog is unreadable); never dropped. |
| FB-07 | Prose and declared part disagree (e.g., prose describes a human checkpoint the declared part lacks) | Report; do not auto-add or auto-remove a checkpoint. |
| FB-08 | Selected revision no longer resolvable | Report; do not substitute current same-named content; the record keeps the selected tuple. |
| FB-09 | Collision discovered after selection | Report all origins; keep selection (C-2). |
| FB-10 | Output promises approval, certified or unqualified "checked" standing | Invalid element (S-L; R-4); report. |
| FB-11 | Declared evidence has no observed counterpart after the run | **missing**; never a pass. |
| FB-12 | Seat role meaning undeterminable | Record **unknown** (SEAT-1). |
| FB-13 | Reached-when names an undeclared tool or output, or is absent | Invalid checkpoint; the consumer cannot hold on it truthfully and reports it; the run does not proceed past the prose position as if the checkpoint were satisfied. |
| FB-14 | Direct application requested for an operation whose result an A5 checkpoint concerns | **not permitted** naming the checkpoint-forced treatment (I-7); no silent conversion to a proposal. |
| FB-15 | Only an agent-authored record or a conversation statement of the act exists | Checkpoint stays **waiting** (I-5). |

---

## 12. UNRESOLVED

| ID | Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|---|
| U-01 | Physical carriage of the declared part (front matter, delimited body section, or package companion file) | DEL-02-01, with consumer confirmation | Before OUT-002 schema and OUT-004 parser fixtures | Examples use an illustrative rendering. Options: (a) front matter (one file; long YAML); (b) delimited body section (readable; needs a stable delimiter); (c) companion file (mirrors `execution.json`; two files to keep consistent). Recommendation deferred until DEL-02-03 (W7) and DEL-05-01 parsing needs are received. |
| U-02 | Wire field names, value encodings, schema language | DEL-02-01 with consumers | Before OUT-002 schema | All names are semantic. |
| U-03 | Revision algorithm and multi-file canonicalization | DEL-02-01 with DEL-04-03 | Before revision comparison claims | Meaning defined, with identity method designation; comparison untestable. |
| U-05 | Operation-specific reserved additions: `UNRESOLVED{OI-021}` | Owner via outside SWB session with App/shared owner | Before connected-activity SoW | D2 list applies; additions not assumed. |
| U-05b | Host capture requirement per act kind | Host owner (DEP-001) | Before host act-recording integration | I-5 names the capturing surface; host specifics not assumed. |
| U-05c | Multi-row A4 purpose after partial lapse (R-2 owner question) | DEL-04-01 with Owner | Before DEL-02-03 re-hold design | E2 R-4 shows partial lapse; its effect on the purpose of the remaining rows' act is open. |
| U-07 | Operation version ordering or range | DEL-03-01 | Before DEL-02-03 required-tool fixtures | Exact-version equality only. |
| U-08 | Portable naming of harness capability requirements | DEL-02-01 with DEL-01-01 (W11 observations at 0.158.0) and DEL-02-03 | After W11; before App-side required-tool check | Class defined; names open; register row question RF-7 at C1. |
| U-09 | Host single seat → role meaning mapping (options in SEAT-2) | DEL-02-01 with SWB implementation owner and DEL-02-04 | Before host role-guidance supply and host receiving fixtures | SEAT-1…3 hold for any option. |
| U-10 | Host origin in unqualified precedence; whether a selection follows new revisions | DEL-02-02 (later undertaking) with DEL-02-01 and host owner | Before host-origin discovery in App | Correctness rests on source-qualified selection. |
| U-11 | Record fields for identity tuple, seat role, checkpoint disposition, bound referents, capturing surface | DEL-04-03 | IR1 | Referenced per R-5/R-6/R-8. |
| U-12 | Placement of shared parts: `UNRESOLVED{OI-014}` | App/shared contract owners | Before structural/production contract allocation | Map rows exist; no placement proposed. |
| U-13 | Host loop placement/parsing/persistence and panel assembly: `UNRESOLVED{OI-013}` | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Rows A-4, A-9, A-10. |
| U-14 | Guidance distribution/adoption: `UNRESOLVED{OI-018}` | Owner with shared/project instruction owners | Before instruction changes or dependent supply | Readability required; distribution not decided. |
| U-15 | First connected operation, autonomy and environment: `UNRESOLVED{OI-021}` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW | Fixture operations are FX-PIPE-01 entries, not the selected operation. |
| U-16 | Automatic catalog extension: `UNRESOLVED{OI-003}` | Owner with host contract owner | Before claiming extension capability | Never assumed. |
| U-17 | Owner confirmations for §9 rows; SWBPIPE consumer needs | DEL-02-03, DEL-05-01, DEL-05-02 (this undertaking); DEL-02-02, DEL-02-04 (later); SWBPIPE owner via relay | IR1 (internal); relay (external) | Every row "None". |
| U-18 | Transfer/adaptation procedure producing derived-from identities | DEL-02-03 | W7 | §6.4 meaning defined; procedure not. |
| U-19 | How a checkpoint-forced *propose* treatment (I-7) reaches the host route, given that treatment is resolved on the host route and the loop does not decide it (R-3.1) | DEL-04-01 with DEL-05-01, DEL-03-02 and the host (DEP-001) | Before W7 and loop fixtures | I-7 holds as meaning; mechanism absent (finding F-1). |
| U-20 | Item-level decision rule at an A5 checkpoint (§4.3.7) | DEL-02-01 proposes; DEL-02-03 and DEL-03-02 confirm | W7 | Rule stated as proposal. |
| U-21 | Final disposition when the run ends while waiting, or with an emptied subject | DEL-02-03 | W7 | "waiting" + run-ended event used; not in the R-5 list as a separate state (finding F-3). |
| U-22 | Re-hold after a lapse that occurs after the run passed the checkpoint | DEL-02-03 | W7 | Lapse recorded; re-hold not asserted. |
| U-23 | Per-entry, per-surface exposure element | DEL-03-01 (per R-9) | IR1 | "unagreed" → not established. |
| U-24 | Holding-library fact for a carried unadapted workflow | DEL-02-01 with DEL-02-03 and host owner | IR1 | Proposed as non-identity element (finding F-2). |
| U-25 | How an App-side checkpoint act is captured (not a Codex tool-permission answer) | DEL-02-03 with DEL-01-04 and DEL-04-03 | W7 | I-5 names the App interface as capturing surface; mechanism open. |
| U-26 | FX-PIPE-01 row and read-entry identifiers | DEL-03-01 §10 | IR1 | Examples use placeholders where identifiers are not known from R1_RESOLUTIONS/V1 text. |
| U-27 | Content identity and lapse meaning for an A12 subject (grant setting) | DEL-04-01 with DEL-04-02 | Before any workflow declares an A12 checkpoint | A12 is in the closed list; binding undefined (finding F-4). |

Closed since v0.1: U-04 (act names; R-1, confirm at IR1); U-06 (classifier
permissions; D3).

---

## 13. Verification cases (designed, not run)

None has been executed; no parser, consumer or host exists. Inputs are the
fixture examples in EXAMPLES (FX-PIPE-01 material, invented).

| Case | Serves | Input | Expected result |
|---|---|---|---|
| VC-01 Four roles and host seat | VER-001 (AC-001) | E1 read in App and host single-seat contexts | Same four role meanings; host needs no role-selection UI; seat role recorded or **unknown**. |
| VC-02 Host-owned library | VER-001 (AC-001) | A host-origin workflow plus host `SKILL.md`/`AGENTS.md` | Origin *host* and its source root; all files readable as text. |
| VC-03 Five categories recovered | VER-002 (AC-002) | E1 | Every input, tool reference, checkpoint (incl. reached-when and subject), output and evidence item recovered; prose intact. |
| VC-04 Undeclared vs empty | VER-002 (AC-002) | E5; variant declaring "no checkpoints" | E5 → all **undeclared**; variant → checkpoints **declared empty**. |
| VC-05 Tool references stay opaque | VER-002 (AC-002) | E1 references vs DEL-03-01 C v0.2 | Each compared with C; gaps recorded; no wire field invented. |
| VC-06 Restriction not requirement | VER-002 (AC-002) | E6 | Required-tool check **not established**; restriction retained. |
| VC-07 Success is not an act | VER-003 (AC-003) | E2 R-1 | `CP-accept` **waiting**; `adjustment` *queued*; a consumer reporting "accepted" is incompatible. |
| VC-08 Independent A4 without acceptance | VER-003 (AC-003) | E1b run | `CP-review` **performed** on its own capturing-surface evidence; no prior A5 required (I-3). |
| VC-09 Distinct acts | VER-003 (AC-003) | E2 R-2 | `CP-accept` **performed**; `CP-check` **waiting** after arrival (I-1). |
| VC-10 Partial lapse on rows | VER-003 (AC-003) | E2 R-4 | A4 lapses for the edited row only; `CP-check` **lapsed**; re-hold not asserted (I-4; U-22); A5 on the applied item not lapsed (R-6). |
| VC-11 Acceptance checkpoint forces proposal | VER-003 (AC-003) | E2 R-5a/R-5b/R-5c | R-5a: under a direct grant the agent submits a proposal; `CP-accept` waits and is performed on A5. R-5b: a direct request → **not permitted** naming the forced treatment; nothing applied; no silent conversion. R-5c (E1c, A4 on applied rows): direct application proceeds with origin/undo; `CP-check` waits for A4 on the applied rows. |
| VC-12 Closed act list | VER-003 | Variants of E1 naming A2 apply, A3 examine, A14 or V4-CON-05 design-candidate approval | Each invalid (FB-03). |
| VC-13 Collision without rebinding | VER-004 (AC-004) | E4 | All origins exposed; selection keeps its tuple; only explicit reselection changes it. |
| VC-14 Adapted revision | VER-004 (AC-004) | E3 adapted row | New identity with derived-from = original tuple; original unchanged. |
| VC-15 Promised vs observed | VER-004 (AC-004) | E2 R-6 | `adjustment` **outcome unknown**, attributed to the observer that lost observation; `EV-receipt` **missing**; `CP-accept` **waiting** or **unknown**, never performed. |
| VC-16 Reserved acts under D2 | VER-003, VER-004 | E2 R-10: agent attempts to perform A4 through the catalog's mark-checked entry (FX-PIPE-01 OP-C6) | Host outcome **not permitted** (class reserved to the person, per R-2); `CP-check` stays **waiting**; operation-specific additions still reported `UNRESOLVED{OI-021}` where needed. |
| VC-17 Map rows name consumers | VER-005 (AC-005) | §9 | Every row has consumers, responsibility, rationale, confirmation "None" and placement; no row marked agreed. |
| VC-18 Excluded acts mapped | VER-006 (AC-006) | §10 vs SoW REQ-006 | Every excluded act with owner and interface; host-vs-person distinction present. |
| VC-19 Fixture inventory bound to candidate | VER-007 (AC-007) | WD-v0.2, WD-EX-v0.2 | Inventory VC-01…VC-28 with candidate identity, all "designed, not run"; missing inputs listed; no joined host witness claimed. |
| VC-20 Reached-when not observed | VER-003 | E2 R-7′: run ends before any proposal is queued | `CP-accept` **not reached**; never performed. |
| VC-21 Subject binding | VER-003 | E2 R-8: A5 on a different proposal (not this run's) | `CP-accept` stays **waiting** (SB-3). |
| VC-22 Capturing surface | VER-003 | E2 R-9: agent writes "engineer accepted in chat"; then a faithful App record citing the host act facility's evidence | First: **waiting** (FB-15). Second: **performed** on the cited host evidence; record shape conformant; recorder ≠ decision actor. |
| VC-23 Negative decisions | VER-003 | E2 R-11: A10 on all items; E2 R-12: person declines A4 | R-11: **resolved negatively**; on-negative path taken. R-12: decline/stop event recorded; `CP-check` **resolved negatively**; never performed. |
| VC-24 Mixed items | VER-003 | E2 R-13: two items, A5 on one, A10 on the other | **resolved negatively (partial)**; accepted item keeps A5 and proceeds through the host lifecycle (§4.3.7). |
| VC-25 Exposure outcomes | VER-002 | E7 | Missing, not exposed on this surface, channel not enabled and not established are reported as four distinct outcomes. |
| VC-26 Carried unadapted keeps origin | VER-004 | E3 unadapted row | Tuple unchanged; holding library recorded beside it; no "App-origin" value. |
| VC-27 Stale between acceptance and application | VER-003 | E2 R-14: basis fails after A5, before application | Stale refusal under the P stale rule; A5 not lapsed by it; `adjustment` not applied. |
| VC-28 Tool permission is not an act | VER-003 | E2 R-15: in the App, the user's Codex mode auto-answers a tool permission (A14) during the run | A14 settles tool execution only; no checkpoint disposition changes (S-R). |

Limit: passing these later would show local contract/fixture conformance
only. It would not establish host implementation, round-trip execution,
adoption or any human act (SoW VER-007).
