# V1-C — Receiver comparison: workflow, loop, panel and hosting joins

- Run: APP-V4-FIRST-INCREMENT-20260928, node V1-C (CASE-002 Open_Questions Q-03)
- Reviewer: independent Type 2 (Claude Code `Agent` subagent). The reviewer did
  not author any compared design and did not delegate.
- Standing: REVIEW RECORD. It compares v0.1 draft definitions. It does not
  accept, supply or adopt any of them, and it changes none of them.
- Owner rulings applied as a reading lens: `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`
  (OWNER_DECISIONS.md sha256 `f3f8e5f3…81f2e`), D2 (OI-001) and D3 (OI-002),
  plus D4 (OI-012) where it touches a DEL-01-01 seam.
- Write scope honoured: this file only. No git or network operations.

## 1. Versions as read (identified candidates)

All six are `DRAFT DEFINITION — proposed, unsupplied, not implemented, not
accepted`. Hashes are sha256 of the file bytes as read on 2026-09-28. The
algorithm is used here only to identify what was read. It is not a
content-identity selection.

| Side | Contribution ID/version (as declared) | File | sha256 (as read) |
|---|---|---|---|
| Workflow contract | DEL-02-01/WD-v0.1 | `DEL-02-01…/Design/WORKFLOW_DECLARATION.md` | `bacfcb71…6fc5e` |
| Workflow examples | DEL-02-01/WD-EX-v0.1 | `DEL-02-01…/Design/EXAMPLES.md` | `69ac3dbf…c55a` |
| Loop | DEL-05-01/LOOP-v0.1 | `DEL-05-01…/Design/LOOP_RECEIVING_CONTRACT.md` | `fd80420c…55c4` |
| Panel | DEL-05-02/PANEL-v0.1 | `DEL-05-02…/Design/PANEL_RECEIVING_CONTRACT.md` | `07c1e1c5…6f1e` |
| Catalog | DEL-03-01/C-v0.1 | `DEL-03-01…/Design/CATALOG_AND_READ_BASIS.md` | `c13518c9…0b72` |
| Proposal | DEL-03-02/P-v0.1 | `DEL-03-02…/Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | `313487c0…bce` |
| Hosting | DEL-01-01/HOSTING-BOUNDARY-v0.1 | `DEL-01-01…/Design/HOSTING_BOUNDARY.md` | `f1da7f76…d728` |
| Reference only (act names) | DEL-04-01/ACT-POLICY-v0.1 | `DEL-04-01…/Design/ACT_AND_POLICY_CONTRACT.md` | `e6457535…3763` |

Note: `DEL-01-01…/Design/generated/` existed when this review ran (W11
in progress). W11 outputs were **not** read; statements here about DEL-01-01
rest on HOSTING-BOUNDARY-v0.1 only.

Every compared file names its counterparts "by accepted meaning, to be
reconciled at V1". None had received a supplied version of the other side.
This review supplies the first cross-version comparison. It does not turn any
`PENDING` dependency into `SATISFIED`.

## 2. Joins, receiving obligations and the check performed

| Join | Supplier → receiver (as read) | Receiver OUT/REQ/VER consuming it (CASE-002 M1 or register) | Check performed |
|---|---|---|---|
| J1 | WD-v0.1 → LOOP-v0.1 | DEL-05-01 OUT-001, OUT-004; REQ-005, REQ-007; VER-008 (M1 DEL-02-01 row; DEP-05-01-016) | Element-by-element: checkpoint elements, act kinds, dispositions, tool references, selection identity, seat/role |
| J2 | LOOP-v0.1 → WD-v0.1 | DEL-02-01 OUT-001, OUT-003; REQ-002, REQ-005; VER-005 (M1 DEL-05-01 row; DEP-02-01-020) | Loop consumer needs against WD §4.3, §6 and §9 map rows |
| J3 | WD-v0.1 → PANEL-v0.1 | DEL-05-02 OUT-001; REQ-001; VER-001 (M1; DEP-05-02-005) | Workflow selection identity, required-tool outcomes, checkpoint wording and dispositions |
| J4 | PANEL-v0.1 → WD-v0.1 | DEL-02-01 OUT-003; REQ-005; VER-005 (M1 DEL-05-02 row; DEP-02-01-021) | Panel candidates against WD §9 rows A-2, A-10 |
| J5 | LOOP-v0.1 ↔ PANEL-v0.1 | DEL-05-02 OUT-001; REQ-001; VER-001 ← LOOP (DEP-05-02-010). DEL-05-01 OUT-004; REQ-005; VER-007 ← PANEL (DEP-05-01-020) | Event-by-event and presentation-by-presentation, both directions. Needed because one executor drafted both (PANEL F-1) |
| J6 | C-v0.1 → WD-v0.1 | DEL-02-01 OUT-002; REQ-002; VER-002 (M1-C; DEP-02-01-017 / DEP-03-01-022) | Tool descriptor, identity/version, exposure, availability, basis |
| J7 | C-v0.1, P-v0.1 → LOOP-v0.1 | DEL-05-01 OUT-001, OUT-002; REQ-003; VER-004 (M1-C); OUT-001, OUT-003; REQ-003, REQ-007; VER-008 (M1-P) | Tool offering, validation order, outcomes, basis, origin, one-effect |
| J8 | C-v0.1, P-v0.1 → PANEL-v0.1 | DEL-05-02 OUT-001, OUT-003; REQ-001; VER-001 (M1-C); OUT-001, OUT-003; REQ-001–003; VER-001–003 (M1-P) | Queue states, item dispositions, old/new/reason, standing, not-permitted presentation |
| J9 | HOSTING-BOUNDARY-v0.1 seams S-6/S-7, §6 answer origin → WD, LOOP, PANEL | No CASE-002 row. Register: DEP-02-04-010 only (DEL-02-04 receives) | Additive-guidance carriage, supplied-identity evidence, answer origin versus checkpoint acts |

## 3. Agreements

| # | Meaning that agrees | Where (quoted or cited) |
|---|---|---|
| AG-01 | Success is not an act. Queued, accepted and applied are separate. Proposals say "accept". | WD S-G, I-2 ("Operation success, a queued proposal, a receipt … supplies no human act"); LOOP TL-3 ("never rewrites queued as applied, or applied as accepted"); PANEL W-1, PC-08, PC-11; P S-P7, S-P9, §9; C S-C6 |
| AG-02 | No synthetic acceptance-before-check ordering | WD I-3; LOOP C-3, FX-C4; PANEL W-4, PC-19; P §10 rules; C §6.2 rule 2; HOSTING §11 closing paragraph |
| AG-03 | A declared checkpoint overrides autonomy (but see D-07 on what that means for direct application) | WD S-F; LOOP C-1 ("No autonomy grant lets the loop pass it"); PANEL W-5; P S-P13, §4.4 |
| AG-04 | Model text, tool success and agent findings never satisfy a checkpoint | WD I-1/I-2; LOOP C-2, FX-C2; PANEL PC-16, K-1 |
| AG-05 | A required tool is an opaque reference to a catalog operation identity with a readable purpose. The human-act/autonomy class belongs to the catalog entry, not to the declaration. | WD §4.2.2 ("It does **not** restate the operation's human-act/autonomy class"); C §3 elements 1, 2, 8; LOOP TL-1 (offerings derived from the adopted catalog) |
| AG-06 | Read basis has four elements. The relied-on basis is cited unchanged. | WD §4.1 quality row, §4.5 evidence kind; LOOP TL-4; PANEL §3.3 ("relied-on basis"); P §3.2; C §5.1–5.2 |
| AG-07 | Catalog schema is checked before host domain validation | LOOP §6 O-1; P §3.2 "Arguments" row; C §8 input-schema row |
| AG-08 | Unavailable to the person means unavailable to the agent, with the same reason | LOOP TL-1, FX-U2; C S-C3, §10.3; WD §4.2.4 "present, currently unavailable … with the catalog's unavailable reason" |
| AG-09 | Source-qualified selection; collisions exposed; no silent rebinding | WD C-1…C-3; PANEL §3.2 "Must not: Silently rebind…", PC-04 |
| AG-10 | Hosts use one agent seat and impose no role-selection UI | WD §5.2 and REQ-001; PANEL §1 ("Role selection is not a panel interaction") |
| AG-11 | No agent-private surface. Old/new/objects/reason appear in the host's own views. | PANEL H-1, H-2, P-2; P §8; WD §4.4 "destination" |
| AG-12 | No common implementation is proposed. OI-013 and OI-014 remain open. | WD §9 closing ("**no** common implementation or service is proposed"); LOOP §10.2; PANEL §6 OUT-004 state |
| AG-13 | A Codex approval answer is tool-execution permission only. It is never a checkpoint act, acceptance, checking, approval or reliance. | HOSTING R8, §11; WD §4.3.2 ("A checkpoint is not a routine tool permission prompt"); DEL-04-01 A14. D3 now settles this for the App. |
| AG-14 | The App's Codex/provider interface and the host loop's Chat Completions interface stay separate | LOOP §1 consequence 1; HOSTING L-6 ("each is qualified separately") |
| AG-15 | Additive guidance is carried unchanged. Composition belongs to DEL-02-04. | HOSTING S-6, §2 last row; WD S-N, §5.1 |
| AG-16 | Acts bind to content and lapse visibly (temporal scope differs; see D-05) | WD I-4; LOOP C-4; PANEL W-3, K-3; C S-C8 |
| AG-17 | A stale proposal is refused with its reason. A re-draft is a new proposal. No retargeting. | P §5, §6; PANEL §3.3 "Must not", PC-09; WD E2 R-7; LOOP FX-D2 (intent; see D-15) |
| AG-18 | Truncated or malformed calls are never dispatched and are reported as rejected before host validation | LOOP §7 (three recipients); PANEL §3.1 "Must not … show a rejected tool call as executed", PC-03 |
| AG-19 | Decision actor and recorder are kept distinct in presentation | PANEL W-2; LOOP A-3; WD I-5; C §6.2 rule 3; HOSTING R7 |

## 4. Disagreements

Severity: **BLOCKING** means the join cannot support its receiving check
until repaired. **MAJOR** means a meaning conflict that would produce wrong
fixtures or presentation. **MINOR** means naming or completeness.

### 4.1 BLOCKING

**D-01 A checkpoint's arrival cannot be observed.** (J1, J3)
- WD §4.3.1: **position** — "Where in the method the run holds, anchored to
  the prose stage." E1 shows position as "after Propose" / "after Check".
- LOOP E-1: "Emit an event only for something the loop actually observed or
  did." LOOP §3: "checkpoint declared at this step? ─► hold (§2.4)". LOOP
  C-1: "At a declared checkpoint the loop stops acting on the run and emits
  'checkpoint reached / waiting for act'."
- Conflict: an LLM-driven loop has no observable "stage". A prose anchor
  gives the loop nothing to observe, so under E-1 it can never truthfully
  emit "checkpoint reached". It could only guess from model text, which C-2
  and FX-C2 forbid. PANEL PC-21 and LOOP FX-C1 cannot be executed as
  designed.
- Resolution: **DEL-02-01 changes.** Add a semantic **reached-when**
  condition to the checkpoint. It should be observable, stated as meaning
  only, for example: before dispatch of a named required tool reference;
  on a named output's observed production; on an observed host outcome such
  as a proposal queued. **DEL-05-01 changes** to state how the loop evaluates
  that condition and what it does if the condition is never met. DEL-02-03
  (W7) confirms against its hold machine.

### 4.2 MAJOR

**D-02 No run-time rule binds a checkpoint's subject to an act record.** (J1, J3)
- WD §4.3.1: **subject** is written in words, "stated so a recorder can bind
  the act to identified content". I-1: satisfied only "on its subject and
  scope, on the content currently bound".
- LOOP C-2: "resumes only on the host's evidence of the **specified** act".
  PANEL W-5: "clears only on the host's record of that act".
- Conflict: the loop and panel can check the act *kind*. They have no rule
  for deciding whether a host act record concerns *this run's* subject, for
  example this proposal identity or the rows this receipt changed. WD's
  subject is text only.
- Resolution: **DEL-02-01 changes.** The subject must name a run-observable
  referent class, such as "the proposal(s) this run submitted at stage X" or
  "objects affected by receipt of output Y". **DEL-05-01 changes** to state
  the matching step. Content identity stays DEL-04-03's.

**D-03 Negative decisions at a checkpoint.** (J1, J3)
- WD §4.3.1 **on negative decision**: "stop, return to a named stage, or
  proceed on a stated branch. Absent this element, the run stops." WD
  §4.3.4 **performed**: "Includes a negative decision where the act kind
  has one." E1 CP-accept: "on rejection: return to Propose once, else stop".
- LOOP C-2 resumes only on evidence of the specified act. LOOP §2.4 hold
  state has no negative outcome. PANEL W-5 clears only on the host's record
  of that act.
- Conflict: under the loop and panel text, a rejection either never clears
  the hold or is treated as "the act". Neither follows WD's declared branch.
- Resolution: **DEL-05-01 and DEL-05-02 change.** The "human act observed"
  event carries the decision polarity, including rejection (DEL-04-01 A10).
  The hold then follows the declared on-negative branch. DEL-04-01 confirms
  that reject is the negative of A5.

**D-04 The loop and panel lack WD's disposition vocabulary.** (J1, J3)
- WD §4.3.4: *not reached, awaiting act, performed, lapsed, unknown, run
  stopped*. "unknown … Never presented as performed."
- LOOP §2.4 hold state: "Waiting; satisfied by an identified act; lapsed;
  abandoned". PANEL W-5 shows only "waiting for <act kind>".
- Conflict: the loop has no *unknown*, so after an interruption the hold can
  only read waiting or satisfied, contrary to S-K. The loop has no *not
  reached*. "abandoned" and "run stopped" are not defined as the same thing.
- Resolution: **DEL-05-01 and DEL-05-02 change** to consume WD §4.3.4 as
  stated. DEL-02-03 (W7) owns the machine and confirms.

**D-05 Temporal scope of lapse.** (J1)
- WD I-4: "If the bound content changes after the act, the act lapses
  visibly and the checkpoint is again awaiting its act." E2 R-4 lapses
  CP-check after the run has passed it.
- LOOP C-4: "If the content an act concerns changes **before the run
  resumes**, the act lapses visibly. The hold returns to waiting."
- Conflict: WD re-holds at any time after the act. LOOP covers only lapse
  before resume, so post-resume lapse has no loop behavior. This also
  interacts with P U-P3, where acceptance lapses after application.
- Resolution: **both change.** Lapse is always recorded and presented. Only
  DEL-02-03 decides whether a lapse after resume re-opens a run; WD should
  not assert re-hold until then. LOOP should add an "act lapsed" event for
  any time and mark re-hold behavior as DEL-02-03-owned.

**D-06 Which recorder's record can satisfy a checkpoint.** (J1, J3, J5)
- WD I-5: "A recorder (App, host, agent) may faithfully record an act the
  person actually performed." PANEL §5 table: "Host (or a faithful
  recorder)". PANEL W-2 allows acts "that an agent or host recorded".
- LOOP E-2 / §2.3: "Human act observed | Person (actor); host (recorder)".
  LOOP C-2 accepts only "the host's evidence". PANEL W-5 accepts only "the
  host's record".
- DEL-04-01 A9: "Which recorders may record which act kinds:
  `UNRESOLVED{OI-001}`". D2 does not decide recorder allocation.
- Conflict: WD and PANEL W-2 would count an agent-recorded act. LOOP C-2 and
  PANEL W-5 would not. PANEL contradicts itself.
- Resolution: **DEL-04-01** states recorder allocation for the reserved acts
  in its v0.2 (or holds it explicitly). Until then **WD, LOOP and PANEL
  align** on the same held statement. PANEL resolves W-2 against W-5.

**D-07 Direct autonomy versus an acceptance checkpoint.** (J1, J8)
- WD E2 R-5: "Person granted direct application…; agent applies directly
  … | `CP-accept` awaiting act (run holds regardless)". WD VC-11 expects
  "Change applies with origin/undo; `CP-accept` still holds the run".
- P §4.4: "No *queued* or *accepted* state exists and **no acceptance is
  recorded or implied** … A workflow checkpoint overrides the grant: the
  run waits for the person's act."
- D2: "No autonomy grant widens past a reserved act or a declared
  checkpoint."
- Conflict: in R-5 the change the checkpoint concerns is applied **before**
  the checkpoint. CP-accept's subject ("the queued adjustment proposal")
  then never exists, so the hold cannot be satisfied. Under D2 the grant
  has widened past a declared checkpoint.
- Resolution: **DEL-02-01 changes** R-5 and VC-11. Either the checkpoint's
  subject change must go through the proposal route even under a direct
  grant, or the declaration must report the checkpoint as unreachable. The
  expected result should not be "applies, then holds". **DEL-03-02** states
  in §4.4 how a declared checkpoint constrains the direct branch.
  DEL-04-01 confirms the D2 reading.

**D-08 Required-tool outcome vocabulary.** (J3)
- WD §4.2.4 outcomes: *present, missing, version mismatch, present-currently-
  unavailable, not established*. WD §3.4: an undeclared workflow is reported
  as "requirements undeclared", never "no requirements".
- PANEL §3.2: "Required host tools, and whether each is present in this
  host"; "Must not … Present a workflow as runnable when a required tool is
  absent". PANEL shows "Declared checkpoints and the act each requires" and
  has no undeclared state. PC-05 covers only "absent".
- Conflict: PANEL's binary view collapses *not established* and *present,
  currently unavailable* into present or absent. A prose-only or
  delegation-requiring workflow (WD §4.7 "unsupported") has no truthful
  presentation.
- Resolution: **DEL-05-02 changes** to consume WD §4.2.4 and §3.4 as stated,
  including "declared empty" versus "undeclared" and "unsupported". This also
  resolves most of PANEL F-2. The host panel needs WD's outcome
  *vocabulary*, which is already a CLM-002 input. DEL-02-03's App checker is
  needed only if OI-014 allocates a shared checker (WD A-5).

**D-09 "Not exposed to this surface" versus "channel not enabled".** (J6)
- WD §4.2.4: **missing** = "Not in the catalog, or not exposed to this
  surface." **present** = "exists … and is exposed to the acting surface".
- C §4.1: "*Channel not enabled* | The channel itself is off … They must
  never be encoded as one another." C defines no per-entry, per-surface
  exposure. The §8 map cells are all "unagreed". C invariant 2 says every
  surface presents the same meaning.
- Conflict: WD folds channel-off into *missing*, which C forbids. WD also
  relies on a per-entry exposure meaning that C does not supply.
- Resolution: **DEL-02-01 changes.** Add *channel not enabled* as a distinct
  outcome, or map it to *not established* with the reason. **DEL-03-01**
  states whether per-entry surface exposure exists at all, or whether
  exposure is only whole-channel plus availability. This is tied to OI-003.

**D-10 Workflow identity carried in origin and run association.** (J1, J3, J7, J8)
- WD §6.1: identity = kind, origin class (*project/user/bundled/host*),
  source root, name, **revision**, derived-from. "A name plus origin without
  a revision identifies a *library slot*, not selected content."
- P §3.3: "Workflow run | Workflow identity and version, and run identity".
  P E-1 shows origin as `workflow "supports-adjust" v0.3 run 12`, with no
  origin class or source root.
- LOOP §2.1: "the workflow identity/version selected".
- PANEL §3.2: "(origin, name, revision)", with no source root. PANEL PC-04:
  "one host-origin and one **App-origin**". "App-origin" is not a WD origin
  class.
- WD itself never states the origin of an App workflow carried into a host
  **unadapted**. E3 covers only the adapted case (origin *host*). PANEL
  §3.2 needs that answer.
- Resolution: **DEL-03-02, DEL-05-01 and DEL-05-02 change** to cite WD §6.1
  identity in full, including revision (not "version") and source root.
  **DEL-02-01 changes** to state the identity of a carried, unadapted
  workflow in a host. PANEL PC-04 uses WD origin classes.

**D-11 Outcome taxonomy collapsed at the loop.** (J7, J5)
- LOOP §2.3 "Host outcome" row: "(ran, refused with reason, stale, queued,
  applied with receipt reference, outcome unknown)".
- P §9 lists twelve outcomes: *unavailable, not permitted, channel not
  enabled, invalid, stale, queued, accepted, applied (receipt), rejected,
  withdrawn, outcome unknown, success*. C §4.1: unavailable, not permitted,
  channel not enabled and error "must never be encoded as one another";
  "*Not permitted* … never phrased as unavailability".
- PANEL §5 separates "Direct application under granted autonomy … 'applied
  by agent', with origin and undo" from "Application of an accepted
  proposal". LOOP §9 and its events have no direct-application row, so
  "applied with receipt" cannot tell the two apart. P §4.4 requires the
  grant relied on, undo route and later-check route.
- Resolution: **DEL-05-01 changes** to carry P §9 unchanged. "Refused with
  reason" is split into unavailable, not permitted and invalid. Accepted,
  rejected and withdrawn are relayed. Applied carries the branch (direct
  under grant, or after acceptance) with P §4.4's elements.

**D-12 Who reports "outcome unknown".** (J7)
- LOOP TL-2: every tool result is "a loop-side failure (not sent to the
  host), a host refusal, or a host outcome". §2.3 lists "outcome unknown"
  under "Host outcome | … | Host".
- P §4.1: "outcome unknown (overlay) | … | Entered by: **Reporter
  (App/adapter/loop)** | Absence of observation; the last observed state".
  HOSTING H10 treats unobserved responses the same way.
- Conflict: an unknown outcome has no host actor. Attributing it to the host
  implies an observation that did not happen, contrary to E-1.
- Resolution: **DEL-05-01 changes.** Add a fourth tool-result class,
  "dispatched, outcome not observed", with the loop as reporter and the last
  observed state.

**D-13 Catalog change between offering and call.** (J7)
- LOOP O-3: "if the host's adopted catalog changed between offering and
  call, the call is reported as needing re-offer rather than validated
  against a different version." This is a loop-side, catalog-level failure.
- C §7: "Entry version changed between discovery and request | Request
  carries the version it was prepared for; host reports a version mismatch
  error meaning (element 7) … Exact rule is a host input (U-C6)". This is a
  host-side, entry-level error. C §2 "Catalog edition" is only "**Proposed**;
  not a V4-HI-02 field" (F-C6).
- Conflict: the same situation is a loop-side failure in one contract and a
  host error in the other, at different granularity. TL-2 requires one
  classification.
- Resolution: **DEL-03-01 and DEL-05-01 agree.** The loop carries the entry
  version it offered. Detection of an edition change before dispatch is
  optional pre-screening, reported as loop-side. Entry-version mismatch
  follows C element 7 and U-C6. One semantic name (edition) is used on both
  sides.

**D-14 LOOP fixture FX-D2 misuses "generation".** (J7)
- LOOP §11 FX-D2: "Proposal citing basis **generation g1** after an
  intervening edit made **g2**".
- C §5.1: generation is "the lineage epoch … (e.g. a restore, re-import or
  reopen that starts a new lineage)". C §10.2 and P §11 keep g1 fixed while
  an edit moves r12 → r13.
- Conflict: as written, FX-D2 tests a lineage change, not the
  intervening-edit staleness it names. A host that checked only generation
  would pass it.
- Resolution: **DEL-05-01 changes** FX-D2 to model revision r12 → r13 within
  g1. It may add a separate generation-change fixture.

**D-15 Where agent findings live.** (J5, J8)
- PANEL P-1: "Everything the panel shows about an agent result, proposal or
  **finding** is reachable in a host view with the same content." PANEL H-1:
  "Agent work … appear in the host's own tables/views".
- PANEL K-2: "A requested agent check produces no change to host tables."
  V4-EXM-21: findings attach "by reference without changing the tables".
- C U-C5: "Whether host-stored agent findings are a change operation" is
  open. C §6.2 carries findings only "if the host carries them".
- LOOP has no carriage for findings. §9 says "Findings by reference to
  rows/results", with no event and no statement of whether findings come as
  a host outcome or as agent message content.
- Conflict: if the host does not store findings, P-1 and H-1 fail for every
  agent check. If it does, the check is arguably a change (U-C5).
- Resolution: **DEL-05-02 changes** to separate domain tables (unchanged)
  from where findings are held, and to route that question to C U-C5 and
  the host. **DEL-05-01 changes** to state how findings reach the panel.

**D-16 Evidence of supplied guidance identity.** (J9, J1)
- WD §6.2 chain: "**supplied** | Those bytes were actually supplied to the
  agent/loop. | App: DEL-02-04 / DEL-01-01; host: host loop". REQ-004 needs
  promised and observed kept distinguishable.
- HOSTING S-6: "Carriage of instruction/role inputs … unchanged, with
  **configuration identity** recorded". §7.1 defines configuration identity
  as "Launch arguments and environment elements supplied by the App". That
  is recorded per child start, not per turn. §5 client-request records
  hold "generation, request identity, method, send position, write result"
  but no identity of the guidance content carried.
- LOOP §2.1 speaker kind includes "supplied guidance (workflow/role/host
  instructions)" but gives no revision identity for what was supplied.
- Conflict: neither the App seam nor the loop produces evidence for WD's
  *supplied* link. Configuration identity is the wrong granularity.
- Resolution: **DEL-01-01 changes.** For client requests that carry
  additive instruction input, record or expose the carried content's
  identity (or state that the recording tap is the evidence), handed to
  DEL-04-03 through DEL-01-02 (S-7). P-15 (resumed conversations) becomes
  a named limitation. **DEL-05-01 changes** to record the identity and
  revision of supplied guidance in the run association.

### 4.3 MINOR

| # | Disagreement (quotes) | Side to change |
|---|---|---|
| D-17 | Act-kind names. WD uses *accept a proposed edit*, *mark checked*, *approve*, "*accept professional reliance*". DEL-04-01 A4–A7 are **Mark checked / Accept / Approve / Rely**. LOOP §2.4 and §9 already use "accept … mark checked, approve, rely". "Accept professional reliance" reuses the proposal verb (V4-HI-33). WD output standing "*agent-checked (non-mutating)*" collides with "checked" (DEL-04-01 A3 **Examine**; PANEL "finding"). | DEL-02-01 adopts A4–A7 names and "agent finding" / "examined" standing (V1-A covers names in depth) |
| D-18 | LOOP §2.2 "**Validated call**" (schema-conformant) versus P §4.1 lifecycle state "**validated** — The host's validation route found it valid". PANEL §3.3 displays P's "validated". | DEL-05-01 renames to "schema-conformant call" |
| D-19 | Completion standing: LOOP §2.1 "Streaming, complete, truncated, interrupted, cancelled **or failed**". PANEL §3.1 omits "failed". | DEL-05-02 |
| D-20 | Model setting: LOOP §5.1 has four states (local; cloud with key; cloud, key absent; unconfigured). PANEL §3.1 indicator is only "local, or cloud chosen by the person". LOOP's "Model request refused at boundary" event (MS-05/06) has no panel presentation. | DEL-05-02 |
| D-21 | Open-issue tags. LOOP §10.1 "Checkpoint execution/hold behavior | … | Host execution | **—**" and "Workflow/role/checkpoint declarations | … | OI-014". WD A-4: "host side `UNRESOLVED{OI-013}`". WD A-9: host loop parsing is OI-013. | DEL-05-01 adds OI-013 to both rows |
| D-22 | LOOP §1 table states the App's providers use "the Responses API for local providers, ARCH §6" as fact. HOSTING L-2/P-11 lists this as "to be observed on the identified candidate". | DEL-05-01 marks it dated/unobserved and cites HOSTING L-2. D4/W11 may now observe it at 0.158.0 |
| D-23 | PANEL PC-09 "re-draft offered on the current basis". P §5: re-draft is a new proposal by the proposer, with new identity, lineage and fresh validation. PANEL does not show lineage. | DEL-05-02 states that the re-draft is the agent's new proposal with lineage, not a panel mutation |
| D-24 | PANEL §3.3 shows one "lifecycle state" per proposal. P §4.3: "Each change item carries its own disposition … The proposal's reported state is derived and never stronger than its items." PANEL H-2 omits P §8's "origin", "current state per item" and "stale indication". | DEL-05-02 |
| D-25 | Owner of accepted-then-basis-fails. PANEL: "for DEL-03-02/P at V1". P U-P3: "Host owner with DEL-03-02, DEL-04-03 (lapse)". | DEL-05-02 cites P U-P3 |
| D-26 | LOOP "Tool offering" lists identity/version, purpose, argument schema, availability and reason, and class. It omits C elements 5–7 (effects, result schema, errors), which LOOP §2.2 and D-11 need. Availability at offering conflicts with C §7: "Availability is re-evaluated at request; the earlier evaluation is historical." | DEL-05-01 |
| D-27 | Catalog naming: LOOP "Catalog identity", C "Catalog edition" (proposed, F-C6) | Both agree one name at R1 |
| D-28 | WD §9 rows A-1, A-3, A-9, A-10 still say need source "SoW only". LOOP-v0.1 and PANEL-v0.1 now exist. PANEL §6 names "Source-qualified workflow identity presentation … Plausible" (WD A-2/A-10). LOOP §10.2 raises candidate (b), catalog-schema argument checking, which has no WD or C map row. | DEL-02-01 updates need sources. DEL-03-01 holds candidate (b) as a question (C §8 map) |

## 5. Absent inputs

| # | Absent element | Owner | Point of need | Severity |
|---|---|---|---|---|
| AB-01 | Rule for mixed item-level decisions at an acceptance checkpoint: when CP-accept counts as performed, negative, or still awaiting if some items are accepted, some rejected and some still queued (WD CP-accept scope "per row, several rows, or whole proposal"; P §4.3; PANEL PC-07) | DEL-02-01 with DEL-02-03 and DEL-03-02 | R1 v0.2; before VC-07/VC-09, FX-C, PC-07 fixtures | MAJOR |
| AB-02 | Seat role meaning in the run association. WD SEAT-1: "recorded with the run … If it cannot be determined, the record says so (unknown)". LOOP §2.1 has no role element. P §3.3 author identity is "agent seat/role instance". | DEL-05-01 (element); U-09 mapping stays with DEL-02-01, SWB owner and DEL-02-04 | R1 v0.2 | MAJOR |
| AB-03 | Origin on dispatched calls. P §3.3 requires author type, author identity (seat), channel, conversation, workflow run and autonomy standing at drafting. LOOP's "Tool call dispatched" event carries only "Catalog identity; relied-on basis". V-5 does not attach origin. | DEL-05-01 | R1 v0.2 | MAJOR |
| AB-04 | Autonomy settings in the loop. LOOP E-4 claims the event set covers "autonomy settings", but no event carries the grant in force or a change during work (V4-HI-40). No register row to DEL-04-02 (RF-5). | DEL-05-01 with DEL-04-02 | R1 v0.2 | MAJOR |
| AB-05 | Proposal identity reuse on retry in the loop path. P §7: one effect "per proposal identity"; P §11 step 10 "agent resubmits P-2". LOOP MC-9: a re-issued model call "is a new call with its own identity". The loop does not say how a retry after *outcome unknown* keeps the same proposal identity, or that it must re-read before re-drafting. | DEL-05-01 with DEL-03-02 (U-P1/TBD-002) | Before FX-V2 / VC-P-09 execution | MAJOR |
| AB-06 | Treatment of reserved-class entries at offering, now concrete under D2 (e.g. C OP-C6 "Mark row checked", D2(a)). Either offer the entry and expect *not permitted*, or withhold it with a reason distinct from unavailability (C §4.1). LOOP TL-1, PANEL and C are silent. | DEL-05-01 with DEL-03-01 and DEL-04-01 v0.2 | R1 v0.2 | MAJOR |
| AB-07 | Arrival trigger and hold machine confirmation (see D-01, D-04, D-05) | DEL-02-03 | W7 | MAJOR (named input) |
| AB-08 | Version compatibility relation. C §3 #1 defines version equality only ("a version that changes when any other element's meaning changes"), with no ordering or range. WD U-07 can therefore express only exact versions. | DEL-03-01 | R1; before DEL-02-03 required-tool fixtures | MINOR |
| AB-09 | C does not state that entries and tool schemas are open and readable without Chirality software (V4-SHR-02; WD S-B). This bears on DEP-03-01-022 "identifiable capability descriptors to PKG-02". | DEL-03-01 | R1 | MINOR |
| AB-10 | Harness capability naming (WD U-08, which names DEL-01-01 as co-owner). HOSTING has nothing on it. P-04's method/request inventory at 0.158.0 (W11) is the natural input. | DEL-02-01 with DEL-01-01 | After W11 | MINOR |
| AB-11 | How an App-side checkpoint act is requested and recorded. It is not a Codex approval answer (HOSTING R8). A user-input/elicitation answer's standing as act evidence is undefined. | DEL-02-03 with DEL-01-04 and DEL-04-03 | W7 | MINOR |
| AB-12 | Loop and panel event gaps: no event for a V-2 "unknown or unoffered operation" rejection, the O-3 re-offer, reject/withdraw acts (DEL-04-01 A10/A11), or "run ended". PANEL does not present LOOP's "Act requested" event outside checkpoints (LOOP A-2). | DEL-05-01; DEL-05-02 | R1 v0.2 | MINOR |
| AB-13 | Several tool calls in one response versus one proposal with items (LOOP T-OPEN-1 names P; P says nothing) | DEL-05-01 with DEL-03-02 | Before FX-M8 | MINOR |
| AB-14 | The hosts' "no routine permission layer" is not stated. D3 settles that hosts have no classifier mode and use the SWB default proposal mode. LOOP and PANEL should say so explicitly. | DEL-05-01; DEL-05-02 | R1 | MINOR |

## 6. Where owner rulings D2, D3 and D4 change v0.1 statements

The rulings reach consumers through DEL-04-01's policy representation
(OWNER_DECISIONS "apply through the DEL-04-01 policy representation"). R1
should cite DEL-04-01 v0.2 once it carries them, not this table.

| File §/element (v0.1 text) | Ruling | Effect for R1 |
|---|---|---|
| WD §4.3.2 "that is `UNRESOLVED{OI-001}` (U-05)"; U-05; VC-16 "consumer reports `UNRESOLVED{OI-001}`" | D2 | The four checkpoint act kinds (mark checked, accept where a proposal is required, approve, rely) are reserved to the person: D2(a)–(d). U-05 narrows to operation-specific additions (OI-021), reject/withdraw membership and recorder allocation. VC-16 is re-scoped. |
| WD E2 R-5, VC-11 | D2 "No autonomy grant widens past … a declared checkpoint" | See D-07. The expected result must change. |
| WD §4.3.2 and U-06 `UNRESOLVED{OI-002}` | D3 | App: routine permission and sandbox are the user's Codex setting and govern tool execution only. Hosts: no classifier mode. "A checkpoint is not a permission prompt" becomes settled by ruling. |
| LOOP §2.2 tool offering "human-act class values `UNRESOLVED{OI-001}`"; §2.4; A-4; UNRESOLVED OI-001/OI-002 rows | D2, D3 | Class values now come from DEL-04-01 v0.2 with D2. Concrete assignments per operation still wait for OI-021. The OI-002 row closes for hosts: there is no permission layer, and the SWB default proposal mode applies. |
| PANEL K-4, W-6, PC-23 (held), UNRESOLVED OI-001/OI-002 rows; PC-22 | D2, D3 | PC-23 stays held only for operation-specific additions and concrete class assignment (OI-021). The classifier half is ruled as none in hosts. PC-22: changing the grant is a reserved act, D2(e). PANEL has no grant-change interaction (F-3). |
| C §3 element 8 and §10.1 OP-C6 "Mark row checked … `UNRESOLVED{OI-001}`" | D2(a) | OP-C6 is reserved to the person for App/shared contracts. The host names and enforces its own list (V4-HI-30), and host adoption is unevidenced (DEP-001). OP-C4/C5 stay operation-specific, with acceptance of their proposals reserved (D2(b)). |
| P §4.1 withdrawn row "`UNRESOLVED{OI-001}`, U-P6"; U-P5 | D2 (silent) | D2 does not list reject or withdraw. These stay open. P should say "not in the D2 list", not plain "unresolved". |
| HOSTING H9 "`UNRESOLVED{OI-002}` for approval/sandbox"; §2 table row; R7; U-04; F-09 | D3 | Approval and sandbox are the user's own Codex setting per project/turn. The boundary carries them (H9 is unchanged in substance) and U-04 closes. R7's OI-001 clause becomes D2: no automatic answer stands for a reserved act, and approval answers are not reserved acts (R8). |
| HOSTING header "No Codex version is selected"; §10 "W11 is BLOCKED on owner decision D4"; U-01 | D4 | 0.158.0 is the definition/generation pin, not a qualification (DEP-005). W11 is authorized. P-11/L-2 observations can now inform D-22. |

## 7. Register findings (Dependencies.csv)

Rows checked: DEL-02-01 DEP-02-01-017…024; DEL-05-01 DEP-05-01-014…024;
DEL-05-02 DEP-05-02-005…018; DEL-03-01 DEP-03-01-022…030; DEL-03-02
DEP-03-02-016…026; DEL-01-01 DEP-01-01-016…024. Also the rows in DEL-02-02,
DEL-02-03, DEL-02-04, DEL-04-02 and DEL-04-03 that target these six
deliverables (DEP-02-02-014, DEP-02-03-009, DEP-02-03-011, DEP-02-04-010,
DEP-02-04-011). ANCHOR rows were excluded. All checked execution rows are
`ACTIVE` and `PENDING`/`TBD`. This review supports no change to `SATISFIED`.

| # | Finding | Rows | Proposed register action (for the register owner; not done here) |
|---|---|---|---|
| RF-1 | DEL-03-01 has no DOWNSTREAM row to DEL-05-01 or DEL-05-02, although both declare it upstream and C's header lists both as receivers | DEP-05-01-014, DEP-05-02-006; no mirror in DEP-03-01-022…030 | Add mirror DOWNSTREAM HANDOVER rows |
| RF-2 | DEL-03-02 has no DOWNSTREAM row to DEL-05-01 or DEL-05-02, although P §13 says "Provide to DEL-05-01 / DEL-05-02" | DEP-05-01-015, DEP-05-02-007; no mirror in DEP-03-02-016…026 | Add mirrors |
| RF-3 | DEL-02-01 has **no DOWNSTREAM rows at all**, although five receivers declare it upstream. DEP-03-01-022 targets the package `PKG-02`, while DEP-02-01-017 targets `DEL-03-01` (granularity mismatch). | DEP-02-02-014, DEP-02-03-009, DEP-02-04-011, DEP-05-01-016, DEP-05-02-005; DEP-02-01-017…024 | Add DOWNSTREAM HANDOVER rows. Retarget or split DEP-03-01-022 to DEL-02-01 and DEL-02-03 (DEP-02-03-011 also consumes C) |
| RF-4 | DEL-05-02 has no row to DEL-02-03 (PANEL F-2) or DEL-04-02 (PANEL F-3) | DEP-05-02-005…018 | F-2: largely resolved by D-08 (consume WD vocabulary); add a row only if a shared checker is allocated. F-3: add an UPSTREAM row to DEL-04-02, or route through a SoW revision decision (scope unchanged here) |
| RF-5 | DEL-05-01 has no row to DEL-04-02, although V-5 and E-4 rely on grant-in-force and autonomy settings | DEP-05-01-014…024 | Add an UPSTREAM INTERFACE row to DEL-04-02 (see AB-04) |
| RF-6 | DEL-01-01 has no DOWNSTREAM row mirroring DEP-02-04-010 (DEL-02-04 consumes the supplier contract for additive supply, seam S-6). HOSTING's Receivers line omits DEL-02-04. S-7 (evidence to DEL-04-03 via DEL-01-02) has no row on either side. | DEP-02-04-010; DEP-01-01-019…024 | Add a DOWNSTREAM row DEL-01-01 → DEL-02-04. Decide whether S-7 needs a row or rides on DEP-01-01-019 |
| RF-7 | WD U-08 names DEL-01-01 as co-owner of harness-capability naming. There is no row on either side. | DEP-02-01-017…024; DEP-01-01-016…024 | Add a row, or drop DEL-01-01 from U-08 |
| RF-8 | DEP-05-01-017 (DEL-05-01 upstream from DEL-02-03) has no mirror in DEL-02-03, although CASE-002 M2 names DEL-05-01 as a DEL-02-03 receiver | DEP-05-01-017 | Add a mirror in DEL-02-03 (outside V1-C scope; noted) |
| RF-9 | Same matter under two identifiers: DEP-05-02-016 targets `OQ-11`, other registers use OI-021 (PANEL F-4) | DEP-05-02-016 | Add a cross-reference note at closeout C1 |
| RF-10 | Mutual UPSTREAM pairs: DEL-02-01 ↔ DEL-05-01 (DEP-02-01-020 / DEP-05-01-016), DEL-02-01 ↔ DEL-05-02 (DEP-02-01-021 / DEP-05-02-005), DEL-05-01 ↔ DEL-05-02 (DEP-05-01-020 / DEP-05-02-010). These are consistent with CASE-002's cyclic M1 exchange. Each pair is two distinct receipts, not a mirror defect. | as listed | None. Keep them as cycle members for project-dag treatment |

## 8. Q-03 answer per join (summary)

| Join | Version the receiver now has | Check performed | Remaining absent or disagreeing |
|---|---|---|---|
| J1 WD → LOOP | WD-v0.1 `bacfcb71…` (LOOP was drafted on accepted meaning only) | Checkpoint, act, disposition, identity and seat comparison | D-01 (BLOCKING), D-02–D-07, D-10, D-16; AB-01, AB-02, AB-07 |
| J2 LOOP → WD | LOOP-v0.1 `fd80420c…` | Consumer-need versus map rows | D-21, D-28 |
| J3 WD → PANEL | WD-v0.1 | Selection, required-tool, checkpoint presentation | D-01, D-02, D-03, D-04, D-06, D-08, D-10 |
| J4 PANEL → WD | PANEL-v0.1 `07c1e1c5…` | Candidate versus map rows | D-28 (agreement on no common component: AG-12) |
| J5 LOOP ↔ PANEL | Both v0.1 (same executor) | Event-to-presentation, both directions | D-06, D-11, D-15, D-19, D-20; AB-12, AB-14 |
| J6 C → WD | C-v0.1 `c13518c9…` | Descriptor, exposure, version, availability | D-09; AB-08, AB-09 |
| J7 C/P → LOOP | C-v0.1, P-v0.1 `313487c0…` | Offering, validation order, outcomes, origin, one-effect | D-10–D-14, D-18, D-26, D-27; AB-03, AB-05, AB-06, AB-13 |
| J8 C/P → PANEL | C-v0.1, P-v0.1 | Queue, items, standing, lineage | D-07, D-10, D-15, D-23–D-25 |
| J9 HOSTING → WD/LOOP/PANEL | HOSTING-BOUNDARY-v0.1 `f1da7f76…` | Guidance carriage, answer origin | D-16, D-22; AB-10, AB-11; AG-13–AG-15 |

## 9. Prioritized repair list for R1

1. **DEL-02-01 + DEL-05-01 (+ DEL-02-03 at W7): checkpoint arrival and
   subject binding** (D-01 BLOCKING, D-02). Add an observable reached-when
   condition and a run-observable subject referent. Make LOOP's evaluation
   explicit.
2. **DEL-05-01 + DEL-05-02: adopt WD §4.3.4 dispositions and negative
   decisions** (D-03, D-04), with lapse recorded at any time and re-hold
   owned by DEL-02-03 (D-05, both sides).
3. **DEL-05-01: carry P §9 and C §4.1 unchanged** (D-11), add the
   loop-reported *outcome unknown* class (D-12), and carry origin, seat role
   and grant in force on every dispatch (AB-02, AB-03, AB-04). Fix FX-D2's
   generation/revision confusion (D-14).
4. **DEL-02-01 + DEL-03-02 (+ DEL-04-01): direct autonomy versus a declared
   acceptance checkpoint** under D2 (D-07). Rewrite WD R-5/VC-11. P §4.4
   states the constraint.
5. **DEL-04-01 v0.2, then WD, LOOP and PANEL: recorder allocation** for
   checkpoint evidence (D-06), and PANEL resolves W-2 against W-5. Apply
   D2/D3 across every file listed in §6.
6. **DEL-05-02: consume WD §4.2.4 and §3.4 vocabulary** (D-08, which closes
   most of F-2), resolve the findings location with C U-C5 (D-15), and
   present per-item dispositions, lineage and the full model-setting states
   (D-19, D-20, D-23, D-24).
7. **DEL-02-01 / DEL-03-01: exposure versus channel not enabled** (D-09).
   Also the version relation (AB-08) and open descriptors (AB-09).
8. **DEL-03-02, DEL-05-01, DEL-05-02: full source-qualified workflow
   identity with revision**. DEL-02-01 defines the identity of a carried,
   unadapted workflow (D-10).
9. **DEL-01-01 + DEL-05-01: evidence of supplied-guidance identity** (D-16).
   Apply D3/D4 to HOSTING (§6). Mark LOOP's Responses-API statement as
   unobserved (D-22).
10. **DEL-05-01 + DEL-03-02: retry keeps proposal identity** (AB-05);
    reserved-class offering under D2 (AB-06); sibling calls versus items
    (AB-13).
11. **Naming and minor alignment**: act names A4–A7 in WD and the "agent
    finding" standing (D-17); "schema-conformant call" (D-18); catalog
    edition (D-27); offering elements (D-26); OI-013 tags (D-21); WD §9 need
    sources (D-28); event gaps (AB-12); explicit "no host permission layer"
    (AB-14).
12. **Register owner at closeout C1**: RF-1…RF-9.

## 10. Counts

- Agreements: 19 (AG-01…AG-19).
- Disagreements: 28. BLOCKING 1 (D-01); MAJOR 15 (D-02…D-16); MINOR 12
  (D-17…D-28).
- Absent inputs: 14. MAJOR 7 (AB-01…AB-07); MINOR 7 (AB-08…AB-14).
- Register findings: 10 (RF-1…RF-10; RF-10 is informational).
