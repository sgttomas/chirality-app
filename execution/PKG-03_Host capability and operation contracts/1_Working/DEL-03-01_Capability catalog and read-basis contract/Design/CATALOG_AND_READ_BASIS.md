# Capability catalog and read-basis contract
- Contribution: DEL-03-01/C-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (catalog and read-basis schema meaning), OUT-002 (three-surface responsibility map skeleton), OUT-003 (designed contract fixtures); REQ-001–REQ-007; AC-001–AC-008; VER-001–VER-008
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 179a6d355d84dba915daddd746d9d62eb7c8ef483e68122a096dfbde6f6b3b84; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7d…60da) §§1–3, §5 V4-HI-30–33, §6 V4-HI-41, §7, §10 item 3, §11; `P/docs/PRD.md` V4-HOST-03, V4-EXT-01, V4-PAR-01–05, V4-AUT-03–05, §9 OQ-02/OQ-10/OQ-11; `P/docs/ARCHITECTURE.md` V4-ARC-20–21; `P/docs/EXAMINATION.md` V4-EXM-20/21/24/25; DECISION_BRIEF #d2/#d3/#d4/#d5; SCC-CASE-002 Case_Datasheet rows M1-C, M3-CP, M4-X (sha256 6acdc6c4…a71a6); Open_Issues OI-001/002/003/014/021
- Consumed inputs: DEL-03-02/P-v0.1 (co-developed in this run; supplies the relied-on basis reference, stale-refusal and re-draft meanings used in §7 and the M3-CP return in §9); DEL-04-01 referenced by accepted meaning only (operation classes and act names), to be reconciled at V1; SWBPIPE host catalog: not supplied (DEP-03-01-025)
- Receivers: DEL-02-01 (OUT-002; REQ-002; VER-002) and PKG-02 via DEP-03-01-022; DEL-02-03 (OUT-001; REQ-001; VER-001); DEL-03-02 (OUT-001, OUT-002; REQ-003; VER-004) via DEP-03-01-023; DEL-03-03 (OUT-001, OUT-003; REQ-001; VER-001); DEL-05-01 (OUT-001, OUT-002; REQ-003; VER-004); DEL-05-02 (OUT-001, OUT-003; REQ-001; VER-001); DEL-09-09 (OUT-001, OUT-002; REQ-001, REQ-005; VER-001, VER-005); DEL-03-04 (integrated guide, reads the map)

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
permission, a default or a pass.

Settled distinctions relied on here (cited, not re-decided):

| Id | Settled distinction | Source |
|---|---|---|
| S-C1 | One catalog describes every operation a person can perform, reads and changes alike | V4-HI-01; V4-PAR-01 |
| S-C2 | Human interface, embedded agent and external agent act through that one catalog; equal UI gestures are unnecessary, equal meaning and standing are essential | V4-PAR-02; V4-HOST-03; #d4 |
| S-C3 | Unavailable to the person ⇒ unavailable to the agent, with the same reason | V4-HI-04 |
| S-C4 | Every read returns its basis; a later action cites the basis it relied on; the basis is checked on every change | V4-HI-11; HI §10 item 3 |
| S-C5 | Results carry standing; an agent never presents more confidence than the host gives | V4-HI-12; V4-PAR-03 |
| S-C6 | Operation success means it ran; execution, checking, acceptance, approval and professional reliance are separate acts | V4-HI-25; V4-AUT-03; #d3 |
| S-C7 | Agents never record a human act as performed when it was not; faithful recording of an actual act is permitted | V4-HI-31; SoW REQ-005 |
| S-C8 | A human act binds to the content it concerns and lapses visibly when that content changes | V4-HI-32 |
| S-C9 | The all-actor/no-separate-work extension promise is preserved and undecided | V4-PAR-05; V4-HI-03; OI-003 |

## 1. Parties and what this contract does not do

| Party | Contribution relevant here |
|---|---|
| App/shared capability-contract owner (DEL-03-01) | This semantic definition, the responsibility map and contract fixtures |
| Host owner (SWBPIPE outside session for the first host) | Actual catalog, domain objects and truth, tables/results/diagnostics, availability evaluation, validation/application, receipts, host UI and the offering/recording of human acts (CLM-001) |
| DEL-03-02 | Proposal, validation and outcome meaning; consumes §§4–7 here |
| DEL-04-01 | Adopted operation classes and human-act names; carried into §3 element 8 |
| DEL-04-03 | Content-bound human-act and run-record format; its act records are what §6 carries faithfully |
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
| Catalog edition | An identity for the whole set of entries as published at one time, so a consumer can say which catalog it generated from or checked against | **Proposed**; not a V4-HI-02 field. Serves VER-002/VER-006 candidate recording. See finding F-C6 |
| Entries | One entry per operation a person can perform (reads and changes) | V4-HI-01/02 |

Catalog invariants:

1. **Completeness.** Every operation available to the person in the host
   interface has an entry. An operation reachable by a person but absent from
   the catalog is a parity defect, not an agent restriction (S-C1).
2. **One meaning.** Each surface (§8) presents an entry's meaning without
   changing it. A surface may add rendering (labels, layout, gesture); it may
   not add, drop or weaken preconditions, effects, errors, standing or class.
3. **Operation identity ≠ read basis.** Entry identity/version describe *what
   the operation is*. The read basis (§5) describes *which state a particular
   read observed*. Neither substitutes for the other; a new model revision
   never changes an operation's identity, and a new operation version never
   changes a prior read's basis.

## 3. Catalog entry meaning (REQ-002; V4-HI-02; SOW-157–164)

Each entry carries eight semantic elements. Element names are semantic.

| # | Semantic element | Meaning | Must distinguish | Scope row |
|---|---|---|---|---|
| 1 | Operation identity and operation version | Stable identifier for the operation, and a version that changes when any other element's meaning changes | Identity stays stable across versions; version is not model revision | SOW-157 |
| 2 | Purpose | Plain statement of what the operation does, readable by a person and an agent alike; the same text reaches every surface | Purpose is descriptive, not a permission or a claim of result quality | SOW-158 |
| 3 | Input schema | Arguments, their meanings, units where applicable, and which argument identifies the target objects | Target identification is explicit (see §4.3); a UI selection is *one way* a person supplies it, not a hidden input | SOW-159 |
| 4 | Availability | Named preconditions, each with an unavailable reason (§4) | Unavailable ≠ error ≠ empty success ≠ not permitted | SOW-160, SOW-166 |
| 5 | Effects | Kinds of objects the operation changes, or *none* | *None* ⇒ read (includes non-mutating checks); any effect ⇒ change, routed through DEL-03-02 | SOW-161 |
| 6 | Result schema including standing | What a successful execution returns, and the standing elements (§6) that accompany it | Result ≠ acceptance; standing is part of the result, not optional decoration | SOW-162, SOW-169 |
| 7 | Errors | Every error the operation can return, each with a stable error identity and its meaning, including whether any effect may have occurred | Error ≠ unavailable; an error whose effect is unobservable routes to DEL-03-02 *outcome unknown* | SOW-163 |
| 8 | Human-act / autonomy class | One of: **none**; **may apply within granted autonomy**; **proposal only**; **reserved to the person** — drawn from the adopted operation policy (DEL-04-01) — or `UNRESOLVED{OI-001}` / `UNRESOLVED{OI-002}` where no adopted assignment exists | An unresolved class is displayed as unresolved; it is not treated as *none*, as *may apply*, or as the historical blanket reserved list | SOW-164 |

Class handling rules:

- The four class values are the source vocabulary (V4-HI-02). Which concrete
  operations take which value is decided by the owner with App/SWB contract
  owners (OI-001/OI-002) and carried by DEL-04-01. This catalog only carries
  it (DEP-03-01-024).
- An entry whose class is `UNRESOLVED{OI-001}` is still fully describable
  (elements 1–7). Dependent implementation or conformance for that entry's
  policy behavior is held; description and fixtures are not (TBD-001).
- The accepted SWBPIPE default *autonomy setting* for model changes is
  proposal, with row-by-row, multi-row or whole-batch acceptance, widenable by
  the person (V4-HI-41). That is a default setting under DEL-04-02, not a
  class ruling; it does not settle whether any model change is reserved.
- Routine tool permission (OI-002) and a human or professional act are
  different subjects and are never encoded in the same element value.

Change entries additionally declare, for DEL-03-02's use:

| Semantic element | Meaning |
|---|---|
| Relied-basis requirement | That the change must cite the basis it relied on (S-C4); DEL-03-02 defines how |
| Old/new value reporting | Which attributes of affected objects the host view will show as old and new (V4-HI-24), so the proposal can carry them |

## 4. Availability (REQ-003; V4-HI-02/04; SOW-160, SOW-166)

### 4.1 Four distinct non-success results

A request for an operation can end, before execution, in one of four
distinct results. They must never be encoded as one another, and none of them
may be encoded as a successful empty result.

| Result | Meaning | Carries |
|---|---|---|
| **Unavailable** | A declared precondition does not hold for this basis and these arguments | Failed precondition identity; unavailable reason (4.2); the basis evaluated |
| **Not permitted for this actor** | Available, but the actor's class/autonomy standing does not permit this act (e.g. reserved to the person; outside grant) | The class element and the governing policy reference or `UNRESOLVED{OI-nnn}`; never phrased as unavailability |
| **Channel not enabled** | The channel itself is off (external access off unless the person enables it, V4-HI-52) | Channel state; no operation evaluated |
| **Error** | Evaluation started and a declared error occurred (element 7) | Error identity and meaning; any partial-effect statement |

Only *unavailable* is subject to the HI-04 parity rule. *Not permitted* is
the intended, policy-derived difference between person and agent; it must be
visible and attributable, not disguised as unavailability. *Channel not
enabled* is a DEL-03-03 enablement state.

### 4.2 Unavailable reason

| Semantic element | Meaning |
|---|---|
| Reason identity | Stable identity for the reason, shared across channels |
| Reason statement | Person-readable text; the same text reaches every channel |
| Failed precondition | Which declared precondition failed |
| Remedy (optional) | What would make it available, stated as a meaning (e.g. "a load case must be identified"), with any gesture phrasing as surface rendering |
| Evaluated basis | The read basis (§5) against which availability was evaluated |

Finding F-C4: V4-HI-02's example reason ("Select a load case in the model
tree first") is phrased as a UI gesture. For channel parity, the precondition
must be expressed in operation meaning (a load case is identified), with the
gesture as one surface's remedy text. The *same reason* (S-C3) is the same
reason identity and statement; a surface may add gesture guidance but not
change the reason.

### 4.3 Selection-dependent preconditions

A person often satisfies a target precondition by selecting in the host UI;
an agent supplies the same target through the input schema. Both evaluate the
same precondition. The resolved target becomes part of the request; a later
selection never changes it (DEL-03-02 no-retargeting).

## 5. Read basis descriptor (REQ-004; V4-HI-11; SOW-167)

### 5.1 Elements

Every read result carries one basis descriptor with four elements. Semantic
labels; no representation selected.

| Element | Meaning (contract level) | Host input still needed |
|---|---|---|
| Workspace identity | Which host workspace/project the read observed | Host's workspace identity scheme |
| Generation | The lineage epoch of that workspace's revision sequence: revisions are only comparable within one generation (e.g. a restore, re-import or reopen that starts a new lineage yields a new generation) | **Host definition of generation** — not defined in the accepted basis (F-C3) |
| Model revision | The revision of the model within that generation that the read observed | Host revision scheme |
| Canonical content identity | An identity of the content actually read, computed by a host canonicalization so that equal content yields equal identity independent of presentation | **Algorithm and canonicalization unselected** (TBD-003; DEP-03-01-028); **scope** (whole model vs the view/rows read) is a host input (F-C3) |

Rules:

1. **All four, every read.** A read result lacking any element is incomplete
   and cannot be cited as a relied-on basis. Historical reads carry the
   historical revision's basis, not the current one.
2. **Basis ≠ operation identity** (§2 invariant 3).
3. **Basis is observed, not chosen.** The basis describes the state the host
   actually read; a consumer never fills it in, updates it, or copies a later
   one over it.
4. **Unavailable and error results** carry the basis they were evaluated
   against when the host evaluated one.
5. **Multi-view reads.** A read that returns several views (e.g. a table plus
   diagnostics) states whether they share one basis; if not, each view carries
   its own descriptor.

### 5.2 Citing the relied-on basis in a later action (SOW-168)

- A later action (a change submitted through DEL-03-02, or a non-mutating
  check that relies on a prior read) carries a **relied-on basis reference**:
  the basis descriptor(s) of the read(s) it actually relied on, unchanged.
- The reference points back to a read; it is never recomputed at queue time,
  at acceptance or at application. A host may additionally record the basis
  it observed at queue or application time as a **separate** element; that
  element never replaces the relied-on reference.
- When an action relies on several reads, it cites each. Whether all cited
  bases must still hold, or only the ones covering the affected content, is a
  host/contract agreement (UNRESOLVED U-C4); DEL-03-02 applies whichever rule
  is agreed.
- How the host decides that a cited basis "no longer holds" (any revision
  change vs a change to relied-on content) is U-C3. The catalog supplies the
  elements that make either rule checkable.
- The catalog exposes this association to DEL-03-02 (DEP-03-01-023). The
  stale refusal, re-draft and application behavior belong to DEL-03-02 and
  are *received* here for the M3-CP comparison (§9; DEP-03-01-026).

Receiving risk (HI §11, SWBPIPE at `e548d4cf`): the observed piping
controller path uses a queue-time basis that differs from the original
external inspection basis. If carried unchanged into integration, it would
substitute a later basis for the relied-on one, contrary to rule 3 and
REQ-004. This is a risk for the joined witness (DEL-09-09), not an
assignment to the host.

## 6. Read results and standing (REQ-003, REQ-005; V4-HI-10/12; SOW-069, SOW-169)

### 6.1 Read result content

A successful read returns the same meaningful content the person sees for the
same operation and basis: tables, results and diagnostics, with the same
standing marks (V4-HI-10; V4-PAR-03). Presentation may differ; content,
diagnostics and standing may not be filtered, summarized upward or omitted
for an agent channel.

An empty table is a successful read with zero rows *and* its basis; it is
distinct from unavailable, not permitted and error (§4.1).

### 6.2 Standing elements

| Semantic element | Meaning | Must not be strengthened by |
|---|---|---|
| Currency | **current** (describes the workspace's present revision) or **historical** (describes an earlier revision or superseded result) | Presenting a historical result as current; dropping currency |
| Checks passed | Each named host check that the result passed, with the basis it was run against | Collapsing to "passed" without naming checks; implying checks not run |
| Known limitations | Host-stated limitations (e.g. solver assumptions, incomplete inputs) | Omitting or softening limitations in an agent summary |
| Human-act evidence (faithfully carried) | References to actual human acts the host has recorded on this content (e.g. a checked mark): act name (DEL-04-01), decision actor (the person), recorder where distinct, content binding and lapse state (DEL-04-03) | Inventing an act; showing a lapsed act as current; attributing an agent's finding to the person |
| Agent findings (if the host carries them) | Findings authored by an agent, attached by reference (V4-EXM-21), with the agent as author | Rendering a finding as a checked or approved state |

Rules:

1. A success value establishes execution only (S-C6); it establishes no check,
   acceptance, approval or reliance.
2. One human act never implies another; there is no synthetic prerequisite
   (e.g. acceptance-before-checking) introduced here (SoW REQ-005).
3. A faithfully carried act keeps the person as decision actor; the recorder
   (host, or an agent reporting what the host recorded) is shown separately.
4. When content bound to an act changes, the act is shown lapsed (S-C8).
5. Nothing is presented as certified, sealed, approved or code-compliant
   (V4-AUT-05).

## 7. Operation sequences (catalog view)

The catalog participates in every channel's sequence the same way. Proposal
lifecycle detail is DEL-03-02's; it is shown here only at the catalog seams.

```text
discover entry (identity, version, purpose, schemas, availability, class)
  → request read (arguments)            → unavailable | not permitted | channel off | error
  → read result (content, standing, BASIS B1)
  → [consumer reasoning; no host state]
  → request change citing relied-on basis B1   (DEL-03-02 route)
       host checks B1 still holds  → stale refusal (reason cites B1 and current basis)  [DEL-03-02]
                                   → validated / queued / … / applied (receipt cites B1) [DEL-03-02]
```

Failure behavior at catalog seams:

| Situation | Required behavior |
|---|---|
| Entry version changed between discovery and request | Request carries the version it was prepared for; host reports a version mismatch error meaning (element 7) rather than silently re-interpreting arguments. Exact rule is a host input (U-C6) |
| Read returns without full basis | Consumers mark the read *basis incomplete* and do not cite it for a change |
| Channel cannot observe a read's result (lost response) | No content is invented; the consumer re-reads, obtaining a new basis. Reads have no effects, so no outcome-unknown overlay applies to the model |
| Availability evaluated on a different basis than a later request | Availability is re-evaluated at request; the earlier evaluation is historical |

## 8. Three-surface responsibility map — skeleton (OUT-002; REQ-006; SOW-072, SOW-165)

Surfaces: **H** = host human interface; **E** = embedded-agent tools (host
loop, received by DEL-05-01/05-02); **X** = external interface (host-built
MCP server or CLI over the live controller, V4-HI-50/V4-ARC-21; App side
received by DEL-03-03).

Cell values: **generated** (produced from the catalog), **checked** (built
separately, checked against the catalog), **hand-built** (adapter work not
tied to the catalog), **unagreed** (no allocation agreed). At v0.1 no
generation or check route has been agreed with the host owner, so every cell
is **unagreed**; the *candidate* column records what #d4 and V4-HI-03 suggest
examining, not a selection.

| Catalog element / concern | H | E | X | Candidate to examine | Producing owner | Receiving point |
|---|---|---|---|---|---|---|
| Entry discovery (identity, version, purpose) | unagreed | unagreed | unagreed | generated for E and X | Host owner | DEL-05-01 tool list; DEL-03-03 native tool inspection; PKG-02 tool descriptors (DEP-03-01-022) |
| Input schema / argument checking | unagreed | unagreed | unagreed | generated or checked for E and X | Host owner | DEL-05-01 REQ-003 (catalog schema before domain validation) |
| Availability + reason | unagreed | unagreed | unagreed | checked on all three (parity rule) | Host owner | DEL-05-02 panel; DEL-03-03 |
| Effects / affected objects | unagreed | unagreed | unagreed | generated metadata | Host owner | DEL-03-02 target binding |
| Result content + standing | unagreed | unagreed | unagreed | H hand-built views; E/X checked against H meaning | Host owner | DEL-05-02; DEL-09-09 VER-002 comparison |
| Errors | unagreed | unagreed | unagreed | generated identities, hand-built texts | Host owner | DEL-03-02 outcome taxonomy |
| Class element | unagreed | unagreed | unagreed | carried from DEL-04-01 adopted policy | DEL-04-01 → host | DEL-04-02; DEL-03-03 |
| Read basis descriptor | unagreed | unagreed | unagreed | one host producer for all three | Host owner | DEL-03-02; DEL-04-03 run records |
| Proposal views (old/new/objects/reason) | unagreed (host's own views, V4-HI-24) | n/a (agent drafts) | n/a | host-owned presentation; generation route open | Host owner | DEL-03-02 view receiving (DEP-03-02-024) |
| Shared types / components carrying the above | — | — | — | UNRESOLVED{OI-014} | App/shared contract owners | DEL-10-03 account |

Extension promise (OI-003; S-C9): the original promise that a new catalog
operation becomes available to the person and both agents **without separate
work** is preserved verbatim in meaning and is **not claimed**. Its
disposition — retain, narrow to defined generated surfaces, or defer — is
`UNRESOLVED{OI-003}`, owned by the owner with the host contract owner
(DEP-03-01-027). The evidence route is DEL-09-09's V4-EXM-24 trace, received
via DEP-03-01-030 (CASE-002 M4-X): one new operation traced through H, E and X
recording generated behavior, additional work, availability reasons and
semantic outcomes on one model revision. Until both the trace and the ruling
exist, the map advertises neither automatic availability nor maintenance
savings, and no narrower criterion is silently selected.

## 9. Proposal input this catalog needs, and the M3-CP return

Co-developed with DEL-03-02/P-v0.1 (original SCC-CASE-004 pair, carried in
CASE-002).

**Forward (C → P, DEP-03-01-023 / DEP-03-02-016).** C supplies: operation
identity and version; input schema including target identification; effects;
errors; availability result and reason; the read basis descriptor (§5.1) and
the relied-on basis reference meaning (§5.2).

**Proposal input C needs from P** (named, to be compared at V1):

| Needed from DEL-03-02 | Why C needs it |
|---|---|
| Relied-on basis reference carried unchanged from drafting through outcome | To show a later action cites the read's basis (AC-004) |
| Stale refusal reporting both the relied-on basis and the current basis, with reason | To show an intervening change cannot silently rewrite the reference |
| Re-draft as a separately identified proposal citing the new basis, with lineage to the original | To show the new basis is not written into the original |
| Receipt reference to the relied-on basis and to the resulting revision | To close read → application trace |
| Target binding fixed at drafting | §4.3 selection-dependent preconditions |

**Return (P → C, M3-CP, DEP-03-01-026).** Distinct from the forward handoff:
DEL-03-02 supplies designed refusal/application behavior and the C/P
read-then-action comparison with an intervening edit (P-v0.1 §11). DEL-03-01
uses it only to *compare* all four basis elements across read, proposal,
refusal, re-draft and receipt (VC-C-04). C does not implement proposal
behavior. AC-004/VER-004 cannot be claimed complete until the actual,
candidate-bound return exists; this v0.1 holds only the designed comparison.

## 10. Representative examples (invented fixture subjects)

All material below is **invented fixture subject matter**: an invented piping
model, invented operations and invented values. Labels such as "OP-C3" are
fixture labels, not operation identities, wire names or SWBPIPE commitments.
No SWBPIPE catalog has been supplied; vocabulary is illustrative only.

Fixture model FX-PIPE-01: one run R-100 between nozzles N-1 and N-2, supports
S-1 … S-4, sustained load case LC-1. Workspace "FX-W1", generation "g1".

### 10.1 Entries

| Fixture | Purpose | Inputs | Availability (precondition → reason) | Effects | Result + standing | Errors | Class |
|---|---|---|---|---|---|---|---|
| OP-C1 v1 "Read supports table" | Lists supports on a run with type, location and stiffness | run identity | run exists → "Run not found in this workspace" | none (read) | supports table; currency; checks; limitations | E-invalid-run | none — fixture assumption for a non-mutating read; the host's adopted assignment governs (X also subject to V4-HI-52) |
| OP-C2 v1 "Read sustained-load results" | Returns stresses and support loads for a load case | run, load case | a load case is identified → "A load case must be identified"; a current solve exists for it → "No current solve for LC-1 at this revision" | none | results table; currency (current/historical); checks passed; limitations (e.g. "invented: linear supports assumed") | E-unknown-load-case | none — fixture assumption, as OP-C1 |
| OP-C3 v1 "Check support spacing" (non-mutating) | Compares support spacing to a stated spacing input and lists exceedances | run, spacing limit | run exists | none | findings list authored by the requester; no human-act standing | E-invalid-limit | none — fixture assumption, as OP-C1; findings are not a checked mark (V4-EXM-21) |
| OP-C4 v1 "Add support" | Adds a support at a location on a run | run, location, support type | run exists; location on run → "Location is not on run R-100" | supports table, run R-100 | new support identity; receipt reference (via DEL-03-02) | E-location-occupied; E-invalid-type | `UNRESOLVED{OI-001}`; accepted V4-HI-41 default setting = proposal (widenable by person) |
| OP-C5 v1 "Adjust run node elevation" | Moves a node elevation on a run | run, node, new elevation | node on run | run R-100 geometry | revised geometry; receipt reference | E-invalid-node | `UNRESOLVED{OI-001}`; same default setting |
| OP-C6 v1 "Mark row checked" | Records the person's checked act on a row's content | row identity | row exists | checked-state on row | recorded act bound to row content | E-row-changed | `UNRESOLVED{OI-001}`; settled: an agent never records it as the person's act (S-C7) |

### 10.2 Read basis vs operation identity

| Read | Operation (identity/version) | Basis (workspace / generation / revision / content identity) |
|---|---|---|
| R1 | OP-C1 v1 | FX-W1 / g1 / r12 / ⟨content-of-supports-at-r12⟩ |
| R2 | OP-C1 v1 (same operation) | FX-W1 / g1 / r13 / ⟨content-of-supports-at-r13⟩ — different basis, same operation |
| R3 | OP-C1 **v2** (entry revised) | FX-W1 / g1 / r13 / ⟨…⟩ — different operation version, same basis as R2 |

⟨…⟩ denotes an opaque content identity; no algorithm is implied.

### 10.3 Unavailable example (three channels)

Person (H), embedded agent (E) and external agent (X) each request OP-C2 for
LC-1 at r13, where no current solve exists. Expected on all three:
*unavailable*; failed precondition "current solve exists"; reason identity
R-no-current-solve; statement "No current solve for LC-1 at this revision";
evaluated basis FX-W1/g1/r13. Not acceptable on any channel: an empty
results table, a generic error, or a historical r11 result presented without
historical currency.

### 10.4 Standing example

OP-C2 at r13 after a solve: currency current; checks passed "equilibrium
check", "unit consistency" (invented); limitation "linear supports assumed".
Row S-2 carries a host-recorded checked act by the person "Engineer A"
(invented), recorded by the host, bound to row content at r12 → shown
**lapsed** at r13 because S-2's stiffness changed. An agent's OP-C3 finding
on S-3 is shown as an agent finding, not as checked.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-001}` concrete always-reserved acts per operation | Owner with App/SWB contract owners; carried by DEL-04-01 | Before operation-policy production contract / dependent implementation | Class element (§3 #8) shows unresolved for OP-C4/C5/C6; description and fixtures proceed; no class-dependent conformance claimed |
| `UNRESOLVED{OI-002}` classifier routine-permission treatment | Owner with App/SWB contract owners | Before permission-policy implementation | *Not permitted* result (§4.1) cannot name a classifier rule; kept distinct from human acts |
| `UNRESOLVED{OI-003}` retain / narrow / defer extension promise | Owner with host contract owner (DEP-03-01-027); trace from DEL-09-09 (DEP-03-01-030) | Before claiming extension or fixing AC-007 criterion | Map (§8) preserves promise, claims nothing |
| `UNRESOLVED{OI-014}` shared contract/component placement | App/shared contract owners | Before structural/production allocation | Map row "shared types/components" left open |
| `UNRESOLVED{OI-021}` first connected operation, autonomy, environment | Owner via outside SWB session and App/shared owner | Before connected SoW / live examination | Examples are invented fixtures only; no connected operation chosen |
| U-C1 Serialization, canonical content identity algorithm, catalog/schema placement, adapter realization (TBD-003) | App/shared capability-contract owner with host/consumer owners (DEP-03-01-028) | Before dependent schema implementation/conformance | All element names semantic; content identity opaque |
| U-C2 Host definition of "generation" | Host owner (DEP-03-01-025) | Before basis conformance or M3-CP executable return | §5.1 gives contract meaning only |
| U-C3 Rule for "basis no longer holds" (any revision vs relied-on content) and content-identity scope | Host owner with DEL-03-02/DEL-03-01 | Before stale behavior implementation | Both rules checkable with §5 elements; neither selected |
| U-C4 Multi-read reliance: which cited bases must hold | Host owner with DEL-03-02 | Before stale behavior implementation | §5.2 requires citing each |
| U-C5 Whether host-stored agent findings are a change operation (effects on an annotation object) | Host owner | Before V4-EXM-21 fixture binding | OP-C3 shown as read with requester-authored findings |
| U-C6 Behavior on entry-version mismatch between discovery and request | Host owner | Before adapter implementation | §7 requires explicit error meaning, not reinterpretation |
| U-C7 Actual host catalog, tables, diagnostics, availability semantics | Host owner / SWBPIPE (DEP-03-01-025; DEP-001) | Before host conformance claim | All examples invented; no conformance claimed |
| U-C8 Actual DEL-03-02 return (M3-CP) and DEL-04-01 adopted names | DEL-03-02; DEL-04-01 | V1 comparison; AC-004 closure | §9 names needs; AC-004 held |

## Verification cases

Designed, **not run**. Each names its expected result and the VER it serves.
Evidence class must be labeled at execution: *schema fixture*, *adapter
result* or *actual host observation* (VER-002).

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-C-01 Entry field coverage | For OP-C1…C6 and a real host entry when supplied, check all eight §3 elements and change-entry extras against V4-HI-02 and SOW-157–164 | Every element present; operation identity/version distinct from basis; class shows adopted value with policy source, or `UNRESOLVED{OI-001/002}` — never blank or defaulted | VER-001 |
| VC-C-02 Cross-channel read parity | Same OP-C2 request, same basis, via H, E, X contract fixtures; compare content, diagnostics, standing | Identical meaning and standing; mismatches listed; record whether each channel's evidence is fixture, adapter result or host observation; type match alone recorded as not closing a consumer claim | VER-002 |
| VC-C-03 Unavailable parity | §10.3 on all three channels | Same *unavailable* result, failed precondition, reason identity and statement; no empty success; *not permitted* and *channel off* cases (separate runs) are distinguishable from it | VER-003 |
| VC-C-04 Read-to-action basis trace with intervening edit (M3-CP receiver) | Read R1 (r12) → proposal cites R1 → person edits S-3 (r13) → submit → stale refusal → re-draft cites R2 (r13) → accept → apply → receipt; uses DEL-03-02 P-v0.1 §11 behavior | All four basis elements present at every read; proposal reference = R1 throughout; refusal shows R1 and current r13; re-draft is a new proposal citing R2; receipt cites the applied proposal's relied basis; no step rewrites R1. Named unresolved representation choices (U-C1–U-C4) recorded | VER-004 |
| VC-C-05 Standing and attribution | §10.4: current/historical results; checks; limitation; a successful OP-C4 execution; an agent OP-C3 finding; a host-recorded checked act with recorder distinct; its lapse after content change | No human act inferred from success or finding; faithful act keeps person as actor and recorder separate; lapsed act shown lapsed; no acceptance-before-checking dependency introduced; actual vs illustrative evidence labeled | VER-005 |
| VC-C-06 Responsibility map review | Walk §8 against H/E/X, CLM-001–003 and receiving rows (PKG-02, DEL-03-02, DEL-04-01) | Each cell has a value; *generated/checked* cells cite a conformance route (none yet → *unagreed*); host implementation shown external; no type-compatibility pass | VER-006 |
| VC-C-07 Extension treatment | Compare §8 extension text with V4-PAR-05, V4-HI-03, #d4, OI-003, V4-EXM-24 | Original promise stated; disposition `UNRESOLVED{OI-003}` with owner; trace route via DEL-09-09; no automatic availability or savings advertised; no narrower criterion adopted | VER-007 |
| VC-C-08 Boundary and open-input audit | Check each REQ-007 exclusion and each UNRESOLVED row | Every excluded act maps to its owner; each open input has owner, point of need, effect; nothing here claims host delivery, policy acceptance or joined qualification | VER-008 |
