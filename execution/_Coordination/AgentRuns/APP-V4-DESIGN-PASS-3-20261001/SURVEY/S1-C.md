# S1-C — scoping survey: DEL-02-02 and DEL-02-04

- **Run / node:** `APP-V4-DESIGN-PASS-3-20261001`, node S1-C (brief: [BRIEFS.md](../BRIEFS.md) "Common rules" and "S1 — scoping survey").
- **Executor:** Type 2 TASK (Claude Opus 5.5, high effort), harness-native descendant of the HELP_HUMAN session. No delegation.
- **Date:** 2026-10-01. Repository HEAD `bdba4771c4` (branch `claude/chirality-app-v4-60-percent-a41fd5`).
- **Write fence:** this file only. No git writes, no network. Read-only on every project file.
- **Standing:** a survey. It decides nothing, changes no contract, register, graph or Design file, and claims no join, witness or adoption. "States" marks what a file says; "Inference" marks my reading.

Paths are relative to `projects/chirality-app-v4/execution` unless they start with `docs/` (then `projects/chirality-app-v4/docs/`) or are marked Root (repository root).

---

## 0. What was read, and how

Hashes are sha256, first 16 hex digits, computed with `shasum -a 256` in the working tree at `bdba4771c4`.

| Source | Hash | How read |
|---|---|---|
| Run `BRIEFS.md`, `OWNER_DECISIONS.md`, `DISPATCH.md` | `7ac504fb23ca97f3`, `ce37656640b824fd` | Whole |
| DEL-02-02 `ScopeOfWork.md` | `5814116909db8120` | Whole |
| DEL-02-02 `Dependencies.csv` | `be14a079c872695e` | Whole (19 rows) |
| DEL-02-02 `_DEPENDENCIES.md`, `_CONTEXT.md`, `_REFERENCES.md`, `_STATUS.md`, `MEMORY.md` | — | Whole |
| DEL-02-04 `ScopeOfWork.md` | `3acfaa62a3bbf003` | Whole |
| DEL-02-04 `Dependencies.csv` | `0cb255b3270dfe61` | Whole (16 rows, parsed by script) |
| DEL-02-04 `_DEPENDENCIES.md`, `_CONTEXT.md`, `_REFERENCES.md`, `_STATUS.md` | — | Whole |
| `_DAG/DAG-003/HANDOFF_STATE.md` | `56d849b6d078d8d5` | Whole |
| `_DAG/DAG-003/DependencyEdges.csv`, `CandidateEdges.csv`, `ExcludedRows.csv` | `4716ca287d23835c`, `07b969209e273310`, — | Every row naming DEL-02-02 or DEL-02-04, by script |
| All 41 live `Dependencies.csv` | — | Every row whose target or statement names either deliverable, by script |
| `_Decomposition/Open_Issues.csv`, `External_Dependencies.csv` | `a11782181531ce77`, — | All OI rows (relevant ones whole); DEP-001, DEP-006 |
| Pass 2 `closeout/C1-A.md`, `C1-B.md`, `C1-C.md`, `CLOSEOUT_ACCOUNT.md` | `e2cb79e22ea5cf75`, `c819ba9be9b92577`, `9c4b9a37a738740a`, `703cd4bf5a7f280c` | CLOSEOUT_ACCOUNT whole; C1-A/B/C: every passage naming either deliverable, A15, registration or role supply, plus their SoW-proposal and register-proposal tables |
| Pass 2 `R12_RESOLUTIONS.md` | `5cf5f574bd736b3c` | Whole |
| Pass 2 `SURVEY/S1-F.md` | `a504772d2a5af4e6` | §1–§2 arcs I-3, I-4, I-13, I-14, §2.3, §3.6, §4 whole |
| Pass 2 `DECISIONS_DRAFT.md` | `4b34c24f52a63d59` | Choice 10 whole; "Also parked"; "Where the records disagree" |
| Pass 2 `OWNER_DECISIONS.md` (DECISION-K1) | `b2fa81871cbf44b9` | K1-1…K1-6 |
| Earlier OWNER_DECISIONS: `APP-V4-FIRST-INCREMENT-20260928` (DECISION-1, -2), `APP-V4-SWBPIPE-INTAKE-20260928` (DECISION-3, -4, -5) | — | Whole for the decision tables and effects |
| `docs/PRD.md`, `ARCHITECTURE.md`, `OPERATING_METHOD.md`, `EXAMINATION.md`, `HOST_INTEGRATION.md` | `bb6e786f7a6c01dc`, `317d5789272c5206`, `98836b5240ed235e`, `471798bc2f2dc020`, `d4331c39db7f452c` | The requirements each SoW cites (§2.1, §2.2, §2.4, §4.1, §4.2, §4.5, §4.7; ARCH §3, §5; OPS §2–§5; EXM-10…14) |
| First-increment Design files (below) | as listed | By `grep` for DEL-02-02, DEL-02-04, A15, registration, role; then the cited sections read whole |
| Root `AGENTS.md` ("Skills and workflows"), Root `workflows/create-workflow/WORKFLOW.md` | `c8ce87ef342902cb`, `f1a3d3abf35c119c` | Whole for the workflow-authoring rules; evidence of current practice only |
| App v3 exemplar `projects/chirality-app-dev` and v3 Runtime `projects/chirality-runtime` | — | The draft-store, route, review component, role materialization and role-config code named in §A.5 and §B.5; evidence only |
| Generated protocol types at 0.158.0 (scratch folder named by PIN_SPIKE: session scratchpad `codex-0.158.0/gen/`) | — | `ThreadStartParams`, `ThreadResumeParams`, `ThreadStartResponse`, `TurnStartParams`, `MultiAgentMode`, `Model` (stable and experimental TS, run1) |

First-increment Design files and their mention counts (DEL-02-02 / DEL-02-04, `grep -c` lines): HOSTING_BOUNDARY (HOSTING-BOUNDARY-v0.8, `3cf0381c42358fec`) 1/10; PIN_SPIKE_0.158.0 (`0e090a4ca14e3ec3`) 0/2; OBS_1_0.158.0 (`7b984b541edca0b1`) read for supplied instructions; WORKFLOW_DECLARATION (WD-v0.8, `517821d18fc95830`) 20/13; EXAMPLES (WD-EX-v0.8, `275ea54d32cd8f48`) 5/2; EXECUTION_COMPATIBILITY (EXEC-v0.6, `64e732d502d0b91d`) 24/3; ACT_AND_POLICY_CONTRACT (ACT-POLICY-v0.8, `6fb6b9e883fa8d20`) 12/0; RECORD_SEMANTICS (RS-v0.8, `b25cc90e9e252f50`) 8/2; HOST_INTEGRATION_GUIDE (GUIDE-v0.5, `5b87996d9c16d5d2`) 6/5; LOOP_RECEIVING_CONTRACT (LOOP-v0.8, `f8b7776c82614738`) 1/1; PANEL_RECEIVING_CONTRACT (PANEL-v0.8, `70d9a23ed45def4e`) 2/0; CONNECTED_ACTIVITY_CONTRACT (CA-v0.6, `58167f7accaf356e`) 20/0; RELAY_QUESTIONS_SWBPIPE 3/0. Every other Design file: 0/0.

Neither deliverable has a `Design/` folder. Both `_STATUS.md` read INITIALIZED (2026-09-27).

**SoW revision history (checked with `git log` on each `ScopeOfWork.md`).** DEL-02-02: `ddd721a90a` (initialization) and `1efd4bcdad` (SCA-V4-002: TBD-001, TBD-002 revised; AX-004 added). DEL-02-04: `ddd721a90a` only; revised by neither amendment. `grep -c -E 'DECISION-1|0.158.0'` on the DEL-02-04 SoW returns 0.

---

# Part A — DEL-02-02 Workflow-making workspace and registration

SOFTWARE `UX_UI_SLICE`; owner: App workflow-experience integration owner; scope SOW-002, 046–050, 127; objectives OBJ-001…003.

## A.1 Obligations

26 items: 4 OUT, 8 REQ, 8 AC, 6 VER. "Basis" names the accepted texts each rests on (as amended by SCA-V4-001/002). "Overtaken or qualified" names later amendments, owner decisions or integrator rulings that change how the item reads; "—" means none found.

| Item | One line | Basis | Overtaken or qualified by |
|---|---|---|---|
| OUT-001 | CODE: one conversational workspace joining planning, trial, draft review, explicit registration, catalog use and refinement | V4-APP-01, V4-WF-01…03, V4-EXM-10; SOW-002/046/047/127 | — |
| OUT-002 | CODE: source-qualified selection and collision behaviour across project, user, bundled, host-supplied origins | V4-WF-02, V4-WF-03 | WD §3.6/§6.1: the origin value is `host`; "host-supplied" is not a value (terminology only) |
| OUT-003 | TEST: creation/revision/registration/reuse and collision fixtures, candidate-bound, supplied to DEL-09-02 | V4-EXM-10; V4-WF-02/03 | — |
| OUT-004 | DOC: native interaction receiving and optional catalog-reuse decisions, owners, identity boundaries, open means | ARCH §3 (reuse candidates "workflow catalog and draft registration"), V4-ARC-20; clarification C1 | — |
| REQ-001 | Plan and revise, trial with real Codex tools, turn the method into a draft, review and register, reuse, refine; declaration visible in the journey | V4-APP-01, V4-WF-01…03, V4-EXM-10 | Bears on the open question whether a draft can be trial-run (§A.4 item 3; EXEC HR-3 says it cannot) |
| REQ-002 | New or changed workflow stays a draft until the person reviews the identified content and explicitly registers it; no stand-in | V4-WF-02, V4-AUT-03 | **R12-5** (INTEGRATION): registration is human act **A15**, not lapse-evaluated, an earlier A15 never carries to a new revision (ACT §2.5; RS HA-10). **K1-1**: the agent may ask (A8); the product does not ask in its place |
| REQ-003 | No silent overwrite; collision and disposition visible; existing content kept unless the disposition authorizes change; no new overwrite policy selected here | V4-WF-02 | Slot/revision policy left to DEL-02-02 by WD C-4/U-10 and EXEC U-E19 (§A.4 item 1) |
| REQ-004 | Source-qualified identity across four origins; no silent rebinding on discovery change | V4-WF-03 | WD §6.1 tuple {kind, origin, source root, name, revision} + derived-from; holding library outside identity (WD C-6) |
| REQ-005 | Receive declaration, capability/checkpoint and record behaviour; keep resolved, supplied/adopted and observed apart; missing capability, required checkpoint, unknown outcome visible; registration is not execution compatibility | ARCH §3 property; V4-WF-04; V4-WF-05; V4-EXM-14 | **V4-WF-05 as amended by SCA-V4-001 (DECISION-4 D4-1)**: in the current phase a declared checkpoint is plan guidance; "required human checkpoint" shows as guidance and a recorded arrival, never a hold |
| REQ-006 | Review/registration distinct from execution success, acceptance, checking, approval, reliance; faithful recording keeps actor apart from recorder; no invented ordering | V4-AUT-03, V4-REC-05; V4-HI-25, -30, -31 | **K1-4**: App-captured actor identity is the name set in the App, the OS account and the Codex account when reported, marked "identity not verified". R12-5 names the act A15 |
| REQ-007 | Keep catalog, reviewed draft-registration and native interaction behaviour; prior code optional reuse; stock Codex integration; open placement stays explicit | ARCH §3, V4-ARC-01, V4-ARC-20; C1 | TBD-002 revised by SCA-V4-002: D4 pin 0.158.0 for definition/generation |
| REQ-008 | Perform no act owned by DEL-01-03, 01-04, 02-01, 02-03, 04-01, 04-03, 09-02, PKG-03, SWBPIPE; the person performs review/registration | Accepted Deliverables.csv allocation | Proposed SC2-01-04-1 (DEL-01-04 act control) may move the capturing control for A15; §A.4 item 4 |
| AC-001 | On a candidate: plan, real tools, draft, actual review/registration, reuse on new inputs, two refinements; declared part and native transitions observable; join gaps evidenced | V4-EXM-10 | — |
| AC-002 | New/changed definitions stay drafts without both review and registration; a later change needs its own reviewed registration | V4-WF-02 | Consistent with ACT FX-56 (c) and RS VC-37 |
| AC-003 | Collision gives explicit disposition, no silent overwrite; retained/changed content agrees with disposition | V4-WF-02 | — |
| AC-004 | Four origins keep identity; same-name discovery changes never change an existing selection | V4-WF-03 | — |
| AC-005 | Selected/draft identity, supply/adoption and observed behaviour distinguishable; missing-capability, checkpoint, unknown-outcome conditions keep true standing | ARCH §3; V4-EXM-14 | "pending human checkpoint" reads as the EXEC §2.4 recorder's *waiting* label (current phase), not a hold (D4-1) |
| AC-006 | Actual review/registration faithfully recorded, actor distinct from recorder, bound to content, scope, purpose; negatives cannot fabricate; no invented order | V4-WF-02, V4-AUT-03, V4-REC-05 | R12-5 (A15, RS HA-10); K1-4 (identity); source of A15 per R12-5 |
| AC-007 | Receiving/reuse account covers every join and owner, optional reuse, open placement, Codex integration | ARCH §3; C1 | — |
| AC-008 | Fixtures and account bind candidate and scope; evidence handed to DEL-09-02 without claiming others' work | Deliverables.csv | — |
| VER-001 | Journey from an empty folder: revise plan, real tools, draft, review/registration, reuse, refine twice; record transitions and identities | V4-EXM-10 | — |
| VER-002 | New/changed-definition fixtures with review absent, registration absent, both present; no carried-forward act | V4-WF-02 | ACT FX-56, RS VC-37 already design the A15 side |
| VER-003 | Collisions and selection across four origins; same-name additions; discovery change after selection; no-overwrite and no-rebind checked separately | V4-WF-02/03 | EXEC RT-7, WD-EX E4 exist as fixtures to reuse |
| VER-004 | Receiving fixtures with actual identities: missing capability, pending checkpoint, unknown outcome; no external live round trip claimed | ARCH §3; V4-EXM-14 | Current-phase reading per D4-1 |
| VER-005 | Positive faithful review/registration act with separate actor/recorder; negatives (no act, mismatched content, execution success, agent recommendation) | V4-AUT-03, V4-REC-05 | A15 capture surface depends on §A.4 item 4; positive case needs a person-operated control (cf. EXEC CH-23 AWAITING INPUT) |
| VER-006 | Review the receiving/reuse account and results against row, sources and ownership | Deliverables.csv; C1 | — |

Not affecting this deliverable: V4-HOST-01's "no default" model options (DECISION-4 D4-3) and DECISION-5 destinations concern host agents; the App's model choice is per conversation (D5). No item here names a model.

## A.2 Joins

### A.2.1 Every ACTIVE register row, in and out

Arc layer from DAG-003 (`DependencyEdges.csv` = admitted; `CandidateEdges.csv` = held in SCC-002; `ExcludedRows.csv` = MIRROR of the named representative). Direction consumer → supplier.

| Row (register) | Arc | Layer | Other end | Contribution |
|---|---|---|---|---|
| DEP-02-02-012 (own) | DEL-02-02 → DEL-01-03 | **admitted** | DEL-01-03 (standalone, this pass, S1-A) | Native plans, revisions, tool and delegation presentation |
| DEP-01-03-013 (DEL-01-03) | same arc | MIRROR of -012 | DEL-01-03 | Supply of plan/tool interaction to DEL-02-02 |
| DEP-02-02-013 (own) | DEL-02-02 → DEL-01-04 | held (SCC-002) | DEL-01-04 (standalone, this pass, S1-B) | Native requests, outcomes, attachments and draft-UI receiving interface |
| DEP-01-04-010 (DEL-01-04) | same arc | MIRROR of -013 | DEL-01-04 | Attachment and draft-transition receiving interactions |
| DEP-01-04-009 (DEL-01-04) | DEL-01-04 → DEL-02-02 | held (SCC-002) | DEL-01-04 | Source-qualified draft identity and draft/registration/collision/refusal transitions, for native presentation (reciprocal of -013) |
| DEP-02-02-014 (own) | DEL-02-02 → DEL-02-01 | held | DEL-02-01 (first increment) | Portable declaration and shared allocation |
| DEP-02-02-015 (own) | DEL-02-02 → DEL-02-03 | held | DEL-02-03 (first increment) | Capability/checkpoint execution, round-trip support |
| DEP-02-03-010 (DEL-02-03) | DEL-02-03 → DEL-02-02 | held | DEL-02-03 | Workflow-making, reviewed-registration and source-qualified selection contract; changed drafts routed through it (reciprocal of -015) |
| DEP-02-02-016 (own) | DEL-02-02 → DEL-04-01 | **admitted** | DEL-04-01 (first increment) | Adopted operation-policy and human-act distinctions |
| DEP-02-02-017 (own) | DEL-02-02 → DEL-04-03 | held | DEL-04-03 (first increment) | Content-bound decision and compact run-record behaviour |
| DEP-02-02-018 (own) | DEL-09-02 → DEL-02-02 | MIRROR of DEP-09-02-016 | DEL-09-02 | Candidate-bound fixture results to the joined standalone qualification |
| DEP-09-02-016 (DEL-09-02) | DEL-09-02 → DEL-02-02 | **admitted** | DEL-09-02 (outside both increments) | Complete workflow-making contribution and focused evidence, PREREQUISITE before the joined witness |
| DEP-09-06-026 (DEL-09-06) | DEL-09-06 → DEL-02-02 (**N-C1**) | **admitted** | DEL-09-06 (first increment) | Review and registration for the connected round trip |

DEP-02-02-019 (person performing review/registration) is RETIRED (fidelity repair, 2026-09-27). Anchors -001…-011 are not arcs. No first-increment supplier carries a DOWNSTREAM row to DEL-02-02 (DEL-02-01, 02-03, 04-01, 04-03); C1-A lists these as "outside mirrors noted, not proposed".

**Graph reading.** Admitted suppliers: DEL-01-03 and DEL-04-01. Admitted consumers: DEL-09-02 and DEL-09-06. Every other arc is held in SCC-002 and gates nothing (HANDOFF_STATE reading rule 3). Two reciprocal pairs sit inside SCC-002: DEL-02-02 ↔ DEL-01-04 and DEL-02-02 ↔ DEL-02-03.

### A.2.2 What the first-increment Design files already assume of DEL-02-02

**DEL-02-01 WD-v0.8 (arc DEP-02-02-014, held).**
- §3.9 OS-1 "App drafts are DEL-02-02's (later)"; OS-2 Register: "The draft becomes a revision with an identity tuple (§6.1); registration is a recorded human act, A15"; failure "package holds a non-regular entry: revision not established (RV-2)", reported by DEL-02-02; OS-3 Select: the person selects a full tuple; DEL-02-02 reports a collision (FB-09).
- §6.1 RV-1…RV-5: revision = every regular file in the package, bytes as stored; "Whether registration refuses them [OS files such as `.DS_Store`] is DEL-02-02's".
- §6.2 listed/selected links: evidence owner "Discovery (DEL-02-02 App)", "Selection (DEL-02-02 …)".
- §6.3 C-1…C-6 collision and rebinding; **C-4**: whether a selection follows a new revision of the same slot "is a selection policy of DEL-02-02 (App) and the host"; **C-5** host position in unqualified precedence UNRESOLVED (U-10).
- §6.4: host workflow refined in the App "is a draft (DEL-02-02) and, once registered, a new identity with derived-from = the host tuple".
- §7 Root conventions: "Drafts in `.chirality/workflow-drafts/`, panel registration, no overwrite — Not part of this contract; DEL-02-02".
- §8: DEL-02-02 receives §3, §6, §4.6 ("Not exercised in this undertaking"); §9 rows A-1, A-2, A-5 name DEL-02-02 (later) as consumer; §10 "App workflow workspace and registration — DEL-02-02 … §6.3 C-4/C-5; §7"; U-10 owner "DEL-02-02 (later undertaking) with DEL-02-01 and host owner", point of need "Before host-origin discovery in App"; U-17 asks DEL-02-02 to confirm §9 rows.
- §8 table "New at v0.8": FB-03 treats A1…A15 as recognized codes.

**DEL-02-03 EXEC-v0.6 (arcs DEP-02-02-015 and DEP-02-03-010, held).**
- §6.1 links *listed*, *selected* and *opened / drafted / registered* (host → App) owned by DEL-02-02; absent meaning "draft only — not a workflow identity".
- §6.3 TR-1: "Drafts are not carried: a draft has no workflow identity (DEL-02-02)"; §2.6 T-1 "Select a registered revision … A draft is chosen · DEL-02-02 · … register it first".
- §6.5 HR-1…HR-7: listing with origin *host* and App-side holding library (HR-1), read-only opening (HR-2), refinement is a draft whose **draft base** is the host tuple, "cannot be selected for a run" (HR-3), review and registration giving a new tuple, origin *project* or *user*, derived-from = host tuple, never silent overwrite (HR-4), collisions never rebind (HR-7). "The changed-draft return path belongs to DEL-02-02 and is not compared in this undertaking (D1); see finding F-12."
- §7.3 RT-6 (host → App refinement, LIB-A2 → LIB-A1 as ⟨rev-A3⟩, "registration is DEL-02-02's (later)"); RT-7 collision, "slot policy DEL-02-02, U-10".
- U-E19: "Selection slot policy and host precedence (WD U-10); registration as an act (AP U-08) — DEL-02-02 (later) with DEL-02-01, DEL-04-01". **The second half is stale**: ACT closed U-08 at R12-5 (A15).
- §9.2/§10 rows: DEL-02-02 receives §3, §4.12, §6.5.

**DEL-04-01 ACT-POLICY-v0.8 (arc DEP-02-02-016, admitted).**
- §2.1 A15 **register workflow revision**: decision actor the person; subject a workflow revision; content "the revision identity and the draft it derives from"; purpose "make it available in the project"; evidence "Capture evidence from the registration control (DEL-02-02, later undertaking, D1)"; not a D2 reserved act; not checkpoint-requirable in this increment.
- §2.1 alias exclusions: A15 is not accept/approve/mark checked, "and a draft's review is not A15 (DEL-02-02 REQ-002)".
- §2.5: A15 bound content is the revision identity with *derived from ⟨draft⟩*; not lapse-evaluated, never superseded.
- §2.6: capturing surface "The App's registration control, operated by the person (DEL-02-02 …)"; never evidence: draft creation, a successful trial run, an agent's recommendation, review of other content, an earlier revision's registration, "a file an agent wrote into a workflow catalog".
- §4.1: A15 outside the closed checkpoint list; a later extension PROPOSED without definition.
- §4.7: "A15 runs RC-2…RC-5 with no arrival: the agent may ask the person to register a revision (A8); the registration control captures the A15".
- §13 FX-56 (a)…(d) and L-ACT-9 fixture identities.
- §10.3 row "DEL-02-02 | DEP-02-02-016 | none | Not mapped in detail (U-08)" — stale pointer after U-08 closed.

**DEL-04-03 RS-v0.8 (arc DEP-02-02-017, held).**
- §6.1/§6.2 **HA-10**: A15 written only from capture evidence at "the registration control (DEL-02-02's …)"; bound content its revision identity with method; relation *derived from ⟨draft⟩*; purpose as ACT. RX row: "A15's `relations.derivedFrom` names a draft, not a workflow identity, and stays a reference".
- R2 workflow identity and trace links (listed/selected/resolved with holding library; transfer links).
- §10 row: DEL-01-02, 01-04, 02-02, 02-04 receive "review/registration, recorded as A15 … the registration control that captures A15" — outside this undertaking.
- `RS_RECORD.valid.act-log.example.jsonl` record 1: an A15 outside any run, `boundSubject` "workflow revision project:supports-adjust@rev-4", `relations.derivedFrom` "draft:supports-adjust@d-12", `evidenceLimits` ["identity not verified"]. VC-37.

**DEL-09-06 CA-v0.6 (arc N-C1, admitted).**
- "Workflow maker" party: authors, reviews and registers the connected workflow in the App (DEL-02-02, later).
- §3 / UNRESOLVED: the reusable workflow (OUT-002 artifact) is authored "under the `create-workflow` method and reviewed/registered through DEL-02-02".
- §4 round-trip table: App library LIB-A1 ⟨fx-proj⟩ holds ⟨rev-A2⟩/⟨rev-A3⟩ under one name; relayed host copy in LIB-A2 ⟨fx-app-import⟩; "draft base ⟨rev-3⟩ → registered with derived-from".
- §6 ST-5 needs "DEL-02-02 registration"; §8.2 W14-01 and W14-09 list DEL-02-02 as missing input; F-1 "OUT-003 cannot complete in this undertaking (DEL-02-02 registration outside D1)".

**Others (no arc to DEL-02-02, but naming it).** PANEL-v0.8 §6 names the App workflow experience (DEL-02-02) as possible second consumer of identity/holding-library presentation; PANEL and LOOP list A15 as not a host act. GUIDE-v0.5 M8.2, M8.5, M8.7, HC-8.6 mark DEL-02-02's part "outside undertaking (D1)". HOSTING-v0.8 §11: "Workflow semantics / making / registration — DEL-02-01 / DEL-02-02 — S-6 carriage". WD-EX E3 (last column), E4 step 3 (revision following, U-10). RELAY lines 1022–1024: host precedence asked "when DEL-02-02 is defined".

**Summary (inference).** The first increment has already designed most of DEL-02-02's interfaces from the consumer side: the identity tuple, the trace links, the host → App refinement steps, the A15 act and record. What it leaves to DEL-02-02 is the library and draft model itself: the slot/revision policy, draft identity and storage, the registration control and sequence, collision dispositions, package hygiene, and the native-UI joins with DEL-01-03/01-04.

## A.3 Proposed contract changes already collected (pass 2 closeout; none applied)

| ID (record) | Target | What it says about DEL-02-02 |
|---|---|---|
| SC2-04-01-4 (C1-A; optional) | DEL-04-01 REQ-002 | Append: registering a workflow revision is a person's act with its own actor, subject and evidence, citing DEL-02-02 REQ-002, AC-006 (A15 rests on a sibling SoW only) |
| SC2-04-03-1 (C1-A) | DEL-04-03 REQ-005 | Names DEL-02-02 among consumers declaring DEL-04-03 upstream in their own registers |
| SC2-02-01-2 (C1-A) | DEL-02-01 CLM-002 | Names DEL-02-02 (and DEL-02-04) as receivers of the portable contract |
| SC2-02-03-6 (C1-A) | DEL-02-03 CLM-003 | Names DEL-02-02 as receiver of the report, recording meanings and transfer contract |
| SC2-01-04-1 (C1-A; = C1-B X-1) | DEL-01-04, new REQ/OUT/AC/VER | The App act control (K1-4): person-only, one act kind at a time on App content, direct-capture record, "identity not verified", standing facility. Its consumer list (DEL-02-03, DEL-04-03, DEL-04-01) does **not** name DEL-02-02 or A15 — bears on §A.4 item 4 |
| Register note (C1-A, after R2 table) | DEL-02-02 register | "DEL-02-02's register should name A15 and its RS record kind at its next revision (B4 §7)" |
| Outside mirrors (C1-A; noted, not proposed, D1) | DEL-04-01, DEL-04-03, DEL-02-01, DEL-02-03 registers | DOWNSTREAM mirrors toward DEL-02-02 |

C1-B and C1-C contain no proposal naming DEL-02-02 (C1-C names it only as the missing input for DEL-09-06 OUT-002/OUT-003).

## A.4 Open items and owner choices

"Shapes now": does the Design text differ by answer?

| # | Item | Where open | Shapes now? | Options and what the files say | Owner? |
|---|---|---|---|---|---|
| 1 | **Library slot and revision policy; collision disposition** — what happens when a reviewed draft has the name of a registered workflow, and whether a selection follows a new revision | WD C-4, U-10; EXEC U-E19, RT-7; SoW REQ-003 ("this contract does not select a new overwrite policy") | **Yes** — library layout, identity of revisions, disposition states, A15 subject, the catalog view | (a) **refuse same name**, register under a new name (Root `create-workflow` and App v3: `WORKFLOW_EXISTS` 409, "Choose a new name"); (b) **revision series per slot**: a changed definition registered under the same name becomes a new revision, earlier revisions kept and selectable; selections pinned or following (C-4); (c) **explicit authorized replacement** with the prior copy retained outside discovery (Root `create-workflow`'s second path). CA §4 (LIB-A1 holds ⟨rev-A2⟩ and ⟨rev-A3⟩ under one name), EXEC RT-7 and WD-EX E4 assume (b)-like behaviour | **Owner**: REQ-003 withholds an overwrite policy; (b) and (c) choose one. Follow-or-pin can be PROPOSED by the integrator |
| 2 | Host origin in unqualified precedence | WD C-5, U-10; RELAY "Not included" | Little — correctness rests on source-qualified selection | Before or after project/user/bundled; or never resolved unqualified | Integrator (PROPOSED); host part waits with DECISION-3 |
| 3 | **Can a draft be trial-run before registration?** | EXEC HR-3 and TR-1/T-1 ("a draft … cannot be selected for a run"); WD OS-2/OS-3; SoW REQ-001, V4-EXM-10 ("refine twice"); SOW-002 "trying a method through real execution and refining it" | **Yes** — journey states, run identity of a trial, records | (a) only registered revisions run; refinements are tried in conversation before re-registration; (b) a draft may be run as a *trial* identified by its draft content identity, recorded as a draft trial and never as a run of a workflow identity; (c) the trial precedes the draft only (V4-EXM-10's order), refinements are registered then reused. Files state (a) for host-origin refinements only; V4-EXM-10 does not say | **Owner confirmation of a reading** (product behaviour); integrator can prepare |
| 4 | **The registration control** — same facility as DEL-01-04's App act control, or a separate DEL-02-02 control; how "not operable by automation" is made true | ACT §2.1/§2.6 ("registration control (DEL-02-02)"); SC2-01-04-1 (act control, consumers exclude DEL-02-02); EXEC CAP-2/CAP-4; OI-008 | **Yes** — sequence, ownership, failure rows; and the wording of SC2-01-04-1 before SCA-V4-003 | (a) one App act control serving A4/A6/A7/A12 and A15 (extend SC2-01-04-1's consumers and act kinds); (b) a DEL-02-02 control meeting CAP-4's guarantee by the same placement rule. App v3 evidence: registration is an ordinary local HTTP POST with a review token returned by GET, so any local caller holding the token can register (inference from `route.ts`/`workflow-draft-store.ts`) — not a CAP-4 control | Integrator for the design; **owner** if SC2-01-04-1's owner-directed wording (K1-4) changes |
| 5 | **Review as evidence** — is review recorded apart from A15, or does A15 bind the exact reviewed bytes? | SoW REQ-002/AC-006 ("review/registration … faithfully recorded"); ACT §2.1 ("a draft's review is not A15") | **Yes** — record kinds, sequence, VER-005 positive case | (a) A15 binds the content the person was shown (v3 analogue: review token = sha256 over root, source, name and package bytes; "DRAFT_CHANGED" 409 on mismatch); review is evidenced by that binding, not by a separate act; (b) a separate act kind for review (would change ACT's act table and RS) | Integrator for (a); (b) needs DEL-04-01 with the owner |
| 6 | Draft identity and storage | EXEC TR-1/HR-3 ("a draft has no workflow identity"); ACT/RS *derived from ⟨draft⟩*; Root AGENTS.md and `create-workflow` (`.chirality/workflow-drafts/<name>/`, project or user) | Yes (data) | A draft reference = {draft location (project/user), name, draft content identity, draft base tuple where refined}; storage as Root practice or other | Integrator (PROPOSED) |
| 7 | Revision identity algorithm and method designation | WD U-03; RS; HOSTING U-08 | Partly — A15 bound content and review binding need *a* method; design can carry a method-designation slot | WD prototype `proto-sha256-list-0` is an illustration only | DEL-02-01 with DEL-04-03; not owner |
| 8 | Package hygiene at registration (OS files, symlinks, hard links, modes) | WD §6.1 RV-2 and "Whether registration refuses them is DEL-02-02's" | Yes (failure rows) | Refuse non-regular entries (WD RV-2; v3 rejects symlinks and hard links; Root `create-workflow` same); refuse or warn on OS files | Integrator |
| 9 | Library content without a registration record (an agent wrote into `.chirality/workflows`) | ACT §2.6 (not A15 evidence); D3 leaves sandbox to the user, so the App cannot prevent the write | Yes (catalog listing standing) | List it with a standing such as "present in library, no registration record"; or hide it; or refuse to select it | Integrator; owner only if hiding/refusing is chosen |
| 10 | A15 purpose wording "make it available in the project" vs registration into the user library | ACT §2.1, RS HA-10; EXEC HR-4 (origin *project* or *user*) | Small | Word the purpose per library | Integrator (edit to ACT/RS) |
| 11 | Where an act record outside a run is written | RS U-05 record location; act-log example | Small for DEL-02-02 (sequence cites it) | — | DEL-04-03 |
| 12 | Process placement (registration control, library writer) | OI-008 (App implementation owner; "Before architecture production contracts"); HOSTING §12 proposal | Placement statements only | — | App implementation owner |
| 13 | Shared types (identity tuple A-2, reader A-1, outcome vocabulary A-5) | OI-014; WD §9 | No (allocation, not behaviour) | — | App/shared contract owners |
| 14 | Checkpoint requiring A15 | ACT §4.1 (possible later extension) | No | — | Later |
| 15 | OI-001/OI-002 | Ruled by D2/D3 (SoW TBD-001 revised) | No | — | Closed for this scope |
| 16 | OI-003 automatic catalog extension | Host catalog (PKG-03) | No | — | Owner with host contract owner; not this deliverable |
| 17 | DEL-09-06 OUT-002 authoring path (connected workflow authored under `create-workflow` with DEL-02-02) | CA §3, UNRESOLVED | No for design; yes for the joined witness | — | Later witness |

## A.5 What exists to build on

**Supplier facts (DEL-01-01).**
- HOSTING §8 S-6/S-7 and §11: workflow making and registration are DEL-02-02's; the boundary carries guidance and records evidence only.
- S-2 (DEL-01-03 seam): plan updates carry the whole plan, no revision identity; plan mode is experimental-only at 0.158.0 (S-F-13). DEL-01-03 derives revision identity (S1-A's matter); DEL-02-02 receives it.
- HCG-A08 delegation and HCG-A09 planning item kinds (HOSTING §8.4) give the native items the journey shows.
- Generated types at 0.158.0: `ThreadStartResponse.instructionSources` ("Environment-native paths to instruction source files currently loaded for this thread") lets the App see which native instruction files Codex loaded (read in the scratch TS; OBS-1 observed `instructionSources []` for an empty cwd).
- No supplier surface concerns workflow registration.

**First-increment designs to reuse unchanged.** WD §3.5–§3.9 (carriage in one fenced `workflow-declaration` JSON block; reading order VO-1…VO-10; operating sequence OS-1…OS-10), `workflow-declaration.schema.json` and its prototype (`prototype/wdproto.py`, two extractors agree on E1); WD §6.1 RV-1…RV-5 and §6.3 C-1…C-6; EXEC §6.1, §6.5, §7.3 RT-6/RT-7, the compatibility report schema (registration ≠ compatibility); ACT A15, FX-56; RS HA-10 and act-log example; C fixtures LIB-A1/LIB-A2 (CA §4); WD-EX E3, E4.

**Root current practice (evidence, not a v4 commitment).** Root `AGENTS.md`: App creation writes a draft under `.chirality/workflow-drafts/<name>/WORKFLOW.md`; the human inspects and registers it through the Workflows panel; registration "without running it or overwriting an existing workflow". Root `create-workflow`: drafts listed as **Ready for review**; **Request changes in chat**; **Register workflow** "publishes the exact reviewed draft; a changed draft requires another inspection"; existing names not overwritten; revision either under a new name or explicit authorized replacement with the prior copy kept outside discovery; no symbolic or hard links; do not auto-run the new workflow; unqualified lookup project → user → bundled.

**App v3 exemplar (evidence only; `projects/chirality-app-dev/frontend/src`).**
- `app/api/working-root/workflow-drafts/workflow-draft-store.ts` (181 lines): lists drafts from project and user; per-file sha256 inventory; **review token** = sha256 over (root, source, name, captured bytes); `registerDraft` re-captures and compares (`DRAFT_CHANGED` 409), stages, makes an **exclusive** `mkdir` reservation (`WORKFLOW_EXISTS` 409, "Choose a new name"), hard-links files and publishes `WORKFLOW.md` last "so Runtime cannot discover an incomplete package. Never overwrite bytes"; 100-draft and 16 MB listing bounds; reports `destinationExists` and `registered`.
- `components/woven-dialogue/workflow-draft-review.tsx`: "Ready for review", "Request changes in chat", "Register workflow" disabled when stale or the name exists.
- No act record of the registration and no actor identity (inference from reading the store and route: neither writes a record). Registration is a local HTTP POST; not a person-only control (§A.4 item 4).
- Reuse standing (ARCH §3; C1): candidate only; v4's Tauri/Rust shell and V4-ARC-03 (no v3 Runtime service) mean the Next.js route itself is not the target.

## A.6 Design scope for this pass (toward the 60% description in `loop/LOOP_INIT.md`)

1. **`Design/WORKSPACE_AND_REGISTRATION.md` (WR-v0.1).**
   - Interfaces: a receiving table per join (DEL-01-03 plan/tool items; DEL-01-04 draft UI and transitions, both directions; DEL-02-01 reading and identity; DEL-02-03 compatibility report and HR steps; DEL-04-01 A15; DEL-04-03 HA-10 and R2; DEL-09-02 evidence bundle; DEL-09-06 N-C1), each with condition of use and failure behaviour.
   - States: the journey (plan → trial → draft → under review → registered → selected → reused → refined draft …); a draft state table (written, changed since review, refused, registered, abandoned); a library-entry state table (registered with record; present without record; not established).
   - Data: draft reference, library entry, collision report, selection record — PROPOSED schemas beside the file (R12-1 form), Chirality names only.
   - Sequences with failures: create draft from conversation; review; register (changed since review, collision, non-regular entry, interrupted write, control closed without act); select; reuse; refine; host-origin open → draft → register (EXEC HR-1…HR-7 consumed unchanged).
   - Policy sections written against the owner's answers to §A.4 items 1 and 3, or with options carried as PROPOSED if unanswered.
   - OUT-004 reuse account against the v3 code above.
   - Verification cases VER-001…VER-006 with what each needs (test double, candidate, person-operated control).
2. **Schemas and conformance instances** for the draft reference, library entry and collision/disposition report; reference WD's `$defs/workflow_identity` rather than redefining it.
3. **Prototype** (Python standard library, R12-3 form): draft capture, review binding, registration with exclusive reservation, collision and changed-since-review cases, non-regular-entry refusal, over WD-EX E1/E3/E4 packages; output recorded as observed.
4. **Edits returned to first-increment owners, not made here:** EXEC U-E19's stale "AP U-08"; ACT §10.3's "Not mapped in detail (U-08)"; A15 purpose wording (§A.4 item 10); the "derived from" naming (§C.2 S-3).

**Leave out, and why.** Visual components and native draft UI (DEL-01-04 OUT-004); plan revision identity (DEL-01-03); revision algorithm (U-03, DEL-02-01/DEL-04-03); act-control construction and placement (DEL-01-04; OI-008); shared placement (OI-014); host libraries and host precedence evidence (DECISION-3); a checkpoint requiring A15 (ACT §4.1); the joined V4-EXM-10 witness (DEL-09-02).

---

# Part B — DEL-02-04 Additive role selection and supply

SOFTWARE `BACKEND_FEATURE_SLICE`; owner: App role-guidance owner; scope SOW-013, 057, 058, 059, 126; objectives OBJ-001…003.

## B.1 Obligations

21 items: 3 OUT, 6 REQ, 6 AC, 6 VER.

| Item | One line | Basis | Overtaken or qualified by |
|---|---|---|---|
| OUT-001 | CODE: four-role selection and additive supply, role configuration, TASK restriction, through the native supplier and portable contracts | V4-APP-03, V4-ROLE-01…03, V4-SHR-01/02; ARCH §3 (reuse candidates "instruction composition and role configuration") | — |
| OUT-002 | DOC: source identity, actual supplied bytes and enforcement limits, for record and adoption owners | V4-ROLE-02/03; ARCH §3; V4-OPS-14, -30; V4-EXM-14 | — |
| OUT-003 | TEST: role-selection and supplied-basis fixtures, including unsupported enforcement and reuse | as above | — |
| REQ-001 | Exactly four relationships with their meanings; domain expressions (SWB Piping Designer) add no fifth role | V4-APP-03, V4-ROLE-01, -03 (U3); V4-OPS-03 | WD §5.1 settles the meanings |
| REQ-002 | Supply the selected role additively through the native receiving contract, preserving the harness's own instructions; no historical Root default as v4 authority | V4-ROLE-02; ARCH §3 | D4 pin 0.158.0 gives the receiving inputs (`baseInstructions`, `developerInstructions` on thread start/resume; HOSTING S-6); SoW does not say so (lag, below) |
| REQ-003 | TASK guidance prohibits further delegation; actual enforcement described separately; other roles keep native delegation | V4-ROLE-03; V4-OPS-30; V4-APP-01 | **D3** (and Root AGENTS.md doctrine): approval and sandbox are the user's own Codex setting, so role selection cannot set them as enforcement (§B.4 item 3) |
| REQ-004 | Trace guidance to source identity and bytes; distinguish selection, supply, provider adoption, behaviour, consumer adoption; feed PKG-04/PKG-11 | ARCH §3/§5; V4-OPS-14; decision 07 | RS R3 is the record element; HOSTING §8.2 supplies per-thread/turn evidence |
| REQ-005 | Preserve behaviour whether old composition code is reused or replaced; reuse must meet the new contract; no common service | ARCH §3/§5, V4-ARC-20; C clarification | — |
| REQ-006 | Perform no act owned by DEL-01-01, 02-01, 04-01, 04-03, 11-02, host owners, the human | Deliverables.csv | — |
| AC-001 | Four relationships offered; selection traces to supplied guidance; domain expression keeps a standing role | V4-ROLE-01/03 | — |
| AC-002 | At the supplier boundary: additive guidance, harness's own instructions intact; source identity and bytes inspectable | V4-ROLE-02 | OBS-1 (one observation) shows both reached a model (§B.5) |
| AC-003 | TASK prohibits delegation; candidate reports observed behaviour and enforcement; other roles keep delegation | V4-ROLE-03 | §B.4 item 3 |
| AC-004 | Unenforceable limits stated; docs match actual controls; no brief or worktree reported as isolation | V4-ROLE-03; V4-OPS-30 | — |
| AC-005 | Account separates source, supplied bytes, provider adoption, behaviour, consumer adoption; adoption attributed to its actor; usable by PKG-04/PKG-11 | ARCH §3; V4-OPS-14; decision 07 | — |
| AC-006 | Reuse account: reused code meets the contract, or replacement covers the same behaviour; owners preserved; no common service, precedence tree or extra UI | ARCH §3/§5; C | — |
| VER-001 | Exercise each role selection; check domain expression | V4-ROLE-01/03 | — |
| VER-002 | Exercise actual additive supply per role against DEL-01-01's contract; compare selected source with supplied bytes; check no loss of harness instructions | V4-ROLE-02; ARCH §3 | Needs a live turn (P-15 resume behaviour not observed) |
| VER-003 | TASK further-delegation attempt; record response, enforcing mechanism or none; other roles' delegation available | V4-ROLE-03; V4-OPS-30 | Needs a live turn with delegation |
| VER-004 | Configuration where a limit is unenforced; compare presented account with actual controls | V4-ROLE-03; V4-OPS-30 | — |
| VER-005 | Trace selected source → supply → provider adoption → behaviour; positive consumer adoption and a supply-only negative | V4-OPS-14; V4-EXM-14 | Positive case needs DEP-006 / OI-024 evidence |
| VER-006 | Review reuse decision and owner mapping | A, C, D, E | — |

**The SoW lags later rulings (states, then inference).** Its open-matter table lists OI-001 and OI-002 with their original points of need, OI-012 with "historical version examples are not v4 pins", and OI-017 as open. Since then: D2 ruled OI-001 and D3 ruled OI-002 for the first increment's App/shared contracts; D4 selected 0.158.0 as definition and generation pin; OI-017 is `RESOLVED_FOR_CURRENT_DEFINITION_RUN` (`_REFERENCES.md` points to `CURRENT_EXECUTION_BASIS.md`). The SoW was revised by neither amendment (S1-F §4.2 found the same). Inference: design work can carry a stated reading now; SCA-V4-003 should carry SoW items updating that table and TBD-001, as SCA-V4-002 did for DEL-02-02.

Not affecting this deliverable: V4-HOST-01 "no default" (host agents); DECISION-5 destinations; K1-1…K1-3 (checkpoint acts). K1-4's identity scheme applies to App-captured acts; consumer adoption (REQ-004) is the consumer owner's act through DEL-11-02, not captured by App controls.

## B.2 Joins

### B.2.1 Every ACTIVE register row, in and out

| Row (register) | Arc | Layer | Other end | Contribution |
|---|---|---|---|---|
| DEP-02-04-010 (own) | DEL-02-04 → DEL-01-01 | **admitted** | DEL-01-01 (first increment) | Identified supported supplier receiving contract for additive role supply (RequiredMaturity INITIALIZED; PENDING). No mirror in DEL-01-01 (HOSTING F-16; C1-B R-11-1 proposes one) |
| DEP-02-04-011 (own) | DEL-02-04 → DEL-02-01 | held (SCC-002) | DEL-02-01 (first increment) | Portable four-role receiving contract and applicable shared allocation |
| DEP-02-04-012 (own) | DEL-04-03 → DEL-02-04 | held (SCC-002) | DEL-04-03 (first increment) | Role-specific source identity, supplied bytes and enforcement-limit evidence (DOWNSTREAM HANDOVER); DEL-04-03 has no consumer row |
| DEP-02-04-013 (own) | DEL-11-02 → DEL-02-04 | **admitted** | DEL-11-02 (outside both increments) | The same evidence for consumer-specific adoption; DEL-11-02 has no consumer row |
| DEP-03-04-010 (DEL-03-04) | DEL-03-04 → DEL-02-04 | **admitted** | DEL-03-04 (first increment) | Additive role guidance and supply receiving semantics for the guide entry and completeness comparison |
| DEP-10-03-010 (DEL-10-03) | DEL-10-03 → DEL-02-04 | **admitted** | DEL-10-03 (outside) | Compatible additive role supply obligations for the responsibility and promise trace |
| DEP-02-04-014 (own) | — | NOT_TOPOLOGICAL | DEP-006 (owners of affected Root/Runtime/App/Piping consumers) | Actual consumer-adoption evidence for VER-005's positive case |
| DEP-02-04-015 (own) | — | NOT_TOPOLOGICAL | OI-008 | Process division before architecture production contracts |
| DEP-02-04-016 (own) | — | NOT_TOPOLOGICAL | OI-018 | Instruction distribution/adoption mechanism before instruction changes or dependent supply |

Anchors -001…-009 are not arcs. No register row joins DEL-02-04 to DEL-02-02, DEL-01-04 or DEL-04-01.

### B.2.2 What the first-increment Design files already assume of DEL-02-04

**DEL-01-01 HOSTING-v0.8 (admitted arc).**
- §8 S-6 "additive guidance": receiver "DEL-02-04 (inputs from DEL-02-01/02-02)"; supplied: "Carriage unchanged through the supplier's supported inputs (at 0.158.0 `baseInstructions` and `developerInstructions` on thread start and resume); per-thread/turn content-identity evidence (§8.2)"; not supplied: "Guidance composition, role files, workflow semantics, idle-boundary change policy".
- §8.2: per guidance-carrying request the boundary records request identity and generation, which element carried it, the content identity of each input (algorithm U-08), and "the source identity supplied by the composing owner (DEL-02-04; workflow identity per R-9 where applicable)". Named limitation P-15: supplied ≠ adopted; whether resume overrides apply to an already-loaded thread is not observed.
- §11: "Additive guidance production — DEL-02-04 — S-6 carriage, §8.2 evidence — Composition". F-16: no DEL-01-01 → DEL-02-04 DOWNSTREAM row. VC-19 designs the supplied-guidance case.
- PIN_SPIKE P-15: "`personality` deprecated … open for DEL-02-04".

**DEL-02-01 WD-v0.8 (held arc).**
- §5.1 meanings settled; "supply is DEL-02-04's". §5.2: App "Person selects a role (DEL-02-04)"; guidance files "Product `AGENTS.md` plus role guidance"; distribution `UNRESOLVED{OI-018}`.
- §5.3 SEAT-1…3; SEAT-2/U-09 host seat mapping, owner "DEL-02-01 with SWB implementation owner and DEL-02-04".
- §4.7 compatible roles (Root `compatible_roles` retained); delegation-requiring workflow compatible only with a delegating role; FB-22 on a mismatch with `execution.json`.
- §3.9 **OS-7 Supply**: "The agent is given `WORKFLOW.md` (prose and block together) with its role guidance — App: DEL-02-04 and HOSTING §8.2"; failure "revision not verified (HL-3)".
- §6.2 *supplied* link evidence owner "App: DEL-02-04 / DEL-01-01 (HOSTING §8.2)".
- §7 Root conventions: four-section `AGENT_<ROLE>.md` files "Leave to DEL-02-04 / OI-018".
- §9 A-6 role meaning and compatible roles: consumers DEL-02-04 (later), DEL-02-03, DEL-05-01; placement `UNRESOLVED{OI-014}`. U-14 = OI-018.

**DEL-04-03 RS-v0.8 (held arc).** R3 "Supplied guidance identity and limits": per thread and turn, source and content identity of each guidance input; supplier DEL-01-01 (App), host loop (relay); *unknown* where not recordable. R5a seat role meaning (host). §10 row: DEL-02-04 "Role-specific source identity, supplied bytes and enforcement-limit evidence (outside this undertaking)"; "role bytes" listed as outside input.

**DEL-03-04 GUIDE-v0.5 (admitted arc).** Row 8 "Host methods and roles"; M8.6 "Four roles behind a single host seat; seat role meaning on every dispatch; additive role guidance with per-thread/turn supplied-guidance evidence"; X-06 additive role supply "App DEL-02-04 (CLM-003) — outside D1"; G-1: DEL-02-04 "has no Design file; M8.6 rests on SoW meaning plus HOSTING S-6". C1-B: row 8 cannot complete until DEL-02-04 is defined.

**DEL-02-03 EXEC-v0.6 (no arc to DEL-02-04).** §2.6 A-3: "The workflow, with its checkpoints, is supplied to the agent through the supplier's additive guidance inputs (HOSTING S-6; DEL-02-04)". §6.1 *supplied* link: "App: DEL-01-01 HOSTING §8.2 via DEL-02-04".

**DEL-05-01 LOOP-v0.8.** U-09 seat mapping row names DEL-02-04 (host side; deferred with host joins).

**Summary (inference).** Four first-increment files (WD OS-7, EXEC A-3 and §6.1, HOSTING S-6/§8.2) assume that DEL-02-04 composes and supplies **the workflow** as well as the role, through `developerInstructions`. DEL-02-04's SoW speaks of role guidance only, and no register row joins it to DEL-02-02 (whose workflow it would supply). See §C.2 S-1.

## B.3 Proposed contract changes already collected (none applied)

| ID (record) | Target | What it says about DEL-02-04 |
|---|---|---|
| SC2-02-01-2 (C1-A) | DEL-02-01 CLM-002 | Names DEL-02-04 as a receiver of the portable contract |
| R-11-1 (C1-B) | DEL-01-01 register | Mirror DOWNSTREAM row toward DEL-02-04 (of DEP-02-04-010); mirror only |
| Outside mirrors (C1-A; noted, not proposed) | DEL-02-01 register | DOWNSTREAM toward DEL-02-04 |
| C1-B §4.3 (no proposal) | DEL-03-04 | Row 8 waits for DEL-02-04's definition |
| S1-F §4.2 (advice) | DEL-02-04 SoW | The open-matter table lags D2/D3/D4; carry a stated reading or fix by scope change |

No pass-2 proposal changes DEL-02-04's own SoW.

## B.4 Open items and owner choices

| # | Item | Where open | Shapes now? | Options and what the files say | Owner? |
|---|---|---|---|---|---|
| 1 | **Where role guidance comes from and how changes reach a conversation** | OI-018 (owner with shared/project instruction owners; "Before instruction changes or dependent supply"); WD U-14; DEP-02-04-016 | **Yes** — source identity form, file locations, change policy, adoption account | (a) guidance bundled with the App release, read-only; (b) a bundled default seeded into an editable copy in the App's user-data folder (Root AGENTS.md describes this for the App's shared guidance: seeded editable copy, common guidance plus active role, changes at a verified idle boundary); (c) project-local guidance overriding or adding. V4-OPS-14: publication or relocation never proves adoption; no new precedence tree | **Owner** |
| 2 | **Supply route and composition** — which supplier input carries what, in which order; whether the selected workflow is composed in or read by the agent as a file | HOSTING S-6, §8.2; WD OS-7, CR-7 ("The agent receives the prose and the block together when it reads the file"); EXEC A-3 | **Yes** — composition spec, RS R3 shape, who owns workflow supply | (a) `developerInstructions` = product guidance + role (+ workflow), `baseInstructions` never set; (b) role as Codex native agent-role configuration (v3: `agents.<ROLE>.config_file` TOML holding `developer_instructions`), used for delegated children; (c) workflow not composed: the agent reads `WORKFLOW.md` with a file tool, so *supplied* is observed as a tool item, not guidance evidence. Root AGENTS.md: roles supplied "through supported additive instruction inputs that preserve Codex's own base instructions" | Integrator with DEL-01-01, DEL-02-01, DEL-02-02; owner only for the workflow-supply ownership question (§C.2 S-1) |
| 3 | **TASK nondelegation: enforce or state the limit** | SoW REQ-003, AC-003/004; HOSTING §8.4 HCG-A08; D3; Root AGENTS.md ("does not … veto the user's Codex configuration, pin approval or sandbox policy") | **Yes** — enforcement account, VER-003/004 text | (a) instruction-only, labelled "instruction-asserted, not enforced"; (b) a per-thread configuration override disabling delegation for a TASK thread (v3 evidence: config overrides `features.multi_agent`, `agents.max_depth=2`); not observed at 0.158.0; may conflict with the "no veto of user configuration" doctrine. Supplier facts: the only signal HOSTING names is `multiAgentMode` (experimental-only); the generated TS marks it "@deprecated Ignored" (read in scratch `ts-experimental/run1/v2/ThreadStartParams.ts`); `Model.multiAgentVersion` is `disabled`/`v1`/`v2` | **Owner** for (b) (it overrides user configuration); (a) needs none |
| 4 | **Changing role in an existing conversation** | P-15 (resume override on a loaded thread not observed); Root AGENTS.md ("verified idle boundary"; "A full-history fork alone does not establish a different role"); HOSTING S-6 "idle-boundary change policy" not supplied | **Yes** — selection state machine and evidence | (a) a role change starts a new thread; (b) apply at an idle boundary through `thread/resume` overrides, if observation shows they take effect; (c) fork with new guidance. Needs a live observation to choose (b) | Integrator; **owner authorization** for a live Codex observation (as K1-6 did for one turn) |
| 5 | No-role ("untyped") session and default role | V4-APP-03; SoW REQ-001 ("exactly the four"); Root registry (`HELP_HUMAN` `default_for_new_chat: true`); Root AGENTS.md ("untyped session or directly select"); v3 `requestedRole` "untyped" | Yes (selection states) | No-role allowed or not; a default role or none | **Owner** (product behaviour; small text) |
| 6 | Native child roles for delegation | SoW REQ-003 ("preserve the required native delegation capability"); Root AGENTS.md ("Fresh named children receive the shared product guidance and their intended full role"); DEL-01-03 delegation views | Yes | Configure the four roles as native agent roles (v3 approach) or let children inherit the parent's guidance | Integrator, with S1-A (DEL-01-03) |
| 7 | Source identity and content identity method for guidance inputs | HOSTING §8.2 (U-08); RS R3 | Partly (data slot) | Path/release identity + content hash with method designation | Integrator; algorithm with DEL-01-01/DEL-04-03 |
| 8 | Codex native instruction discovery vs Chirality guidance | Root AGENTS.md ("Codex owns native global and project instruction discovery"); `ThreadStartResponse.instructionSources` | Yes (what counts as "the harness's own instructions" to preserve, and what is reported) | Treat natively discovered `AGENTS.md` files as part of the harness's own instructions, recorded from `instructionSources` | Integrator |
| 9 | Workflow compatible roles vs the selected role | WD §4.7, FB-22 | Small | Report unsupported; warn; allow | Integrator |
| 10 | Host seat mapping | WD U-09, SEAT-2; LOOP | No for the App | — | DEL-02-01 with SWB owner and DEL-02-04; deferred (DECISION-3) |
| 11 | Process placement of composition | OI-008; DEP-02-04-015; HOSTING §12 proposal | Placement only | — | App implementation owner |
| 12 | Shared role identity set placement | OI-014; WD §9 A-6 | No | — | App/shared contract owners |
| 13 | Consumer adoption evidence and staged retirement | OI-024; DEP-006; DEP-02-04-014 | No for design; VER-005 positive case waits | — | Owner with affected consumers |
| 14 | OI-001, OI-002, OI-012, OI-017 | Ruled or resolved (D2, D3, D4; CURRENT_EXECUTION_BASIS) | No — but the SoW text lags (§B.1) | — | Amendment item (SCA-V4-003), not a choice |

## B.5 What exists to build on

**Supplier facts (DEL-01-01; standings as recorded there).**
- 0.158.0 generated types (read in the scratch folder, stable TS run1): `ThreadStartParams` and `ThreadResumeParams` carry `baseInstructions`, `developerInstructions`, a `config` override map and a deprecated `personality`; resume's overrides are documented "Configuration overrides for the resumed thread"; `TurnStartParams` has no instruction field (it notes that changing personality "does not rewrite the thread's existing instructions"). `ThreadStartResponse`/`ThreadResumeResponse` carry `instructionSources`.
- Experimental `ThreadStartParams.multiAgentMode` is marked "@deprecated Ignored. Use Ultra reasoning effort for proactive multi-agent behavior." `MultiAgentMode` = custom / `explicitRequestOnly` / `proactive`. Native delegation items: `collabAgentToolCall`, `subAgentActivity` (HCG-A08); no client method controls delegation (HOSTING §8.4 table).
- **OBS-1** (one live turn, 2026-09-30, local LM Studio model; not qualification): the prompt "contained Codex's base instructions, the invented developer instructions and prompt, the bundled skill descriptions … and the environment context"; LM Studio logged "Developer role detected - replacing it with system role"; the thread-start response reported `instructionSources []` and `multiAgentMode explicitRequestOnly`. Inference: one observation that `developerInstructions` is additive to Codex's base instructions at this pin; whether the provider kept the developer/system distinction is provider-specific.
- HOSTING §8.2 evidence design and VC-19; P-15 limitation.

**First-increment designs to reuse.** WD §5 (meanings, expressions, seat), §4.7 (compatible roles), §6.2 (*supplied* link), OS-7; RS R3/R5a; HOSTING S-6/§8.2; GUIDE M8.6/X-06 (consumer view).

**Root current practice (evidence only).** Root `agents/AGENT_<ROLE>.md` (four files) and `agents/registry.json` (roles with descriptions, `delegates_to`, `default_for_new_chat` on HELP_HUMAN, `direct_entry`); Root AGENTS.md selective-context rules (Root AGENTS.md + project instructions + the active role file; other role files only by deliberate consultation) and the App description above.

**App v3 exemplar (evidence only).**
- `projects/chirality-runtime/packages/core/src/product-native-role-config.ts`: for each role, writes a TOML file `developer_instructions = <common product guidance + "# Active role: ROLE" + role file>`, named by its sha256, exclusive-create and verified on reuse; returns config keys `agents.<ROLE>.description` and `agents.<ROLE>.config_file`. Rejects missing or mismatched role bytes (sha256 check).
- `native-role-config.ts`: loads the role registry with captured sha256; pins `agents.enabled=true`, `features.multi_agent=true`, `features.multi_agent_v2=false`, `agents.max_depth=2` ("Two descendant edges support HELP_HUMAN -> manager -> TASK"); digest over pins and role bytes.
- `delegated-runtime.ts`: turn envelope carries `developerInstructions` (≤ 1 MiB), `nativeRoleConfig` restricted to the four role keys, `requestedRole` (including "untyped").
- v3 test names (`agent-instruction-conformance`, `verify-instruction-root-integrity`, `prepare-packaged-instruction-root`) indicate packaged-instruction-root checks.
- Reuse standing: V4-ARC-03 excludes the v3 Runtime service as hosting topology; the composition logic and role-config approach are candidates under REQ-005 only. The `agents.max_depth` and `features.*` overrides are exactly the kind of user-configuration override that §B.4 item 3 puts to the owner.

## B.6 Design scope for this pass

1. **`Design/ROLE_SUPPLY.md` (ROLE-v0.1).**
   - Interfaces: S-6 consumption (HOSTING), the four-role contract (WD §5), evidence to DEL-04-03 (R3) and DEL-11-02, consumer view for DEL-03-04 and DEL-10-03.
   - States: role selection per conversation (none or default per §B.4 item 5; selected; change pending at idle boundary; supplied; supply refused); per-thread supplied-guidance state.
   - Data: guidance source record (role file identity, product guidance identity, App release, content identity with method, composition order) and the per-role **limit account** (each limit: enforced by supplier / instruction-asserted / unknown, with evidence). PROPOSED schemas with conformance instances.
   - Sequences with failures: new conversation; role change; resume after restart (P-15 limit); delegated child start; supply mismatch ("revision not verified"-style for guidance bytes); missing or altered role file.
   - TASK restriction and enforcement account per §B.4 item 3's answer.
   - REQ-005 reuse account against the v3 code above.
   - Verification VER-001…VER-006 with needs; VER-002/003 need a live turn.
2. **Prototype** (standard library): compose guidance bytes from fixture role files, compute content identities, validate the source record and limit account against the schemas.
3. **A live observation brief** (if the owner authorizes, as K1-6): one thread start and one resume with changed `developerInstructions` (P-15), and a TASK-guided delegation attempt, at 0.158.0 with a local model.
4. **A stated reading of the SoW lag** (§B.1) in the file header, and an SCA-V4-003 SoW item proposal for the open-matter table.

**Leave out, and why.** Distribution and adoption mechanism beyond the owner's OI-018 answer; consumer adoption and retirement (DEL-11-02, OI-024); host seat mapping (U-09; DECISION-3); placement (OI-008, OI-014); permission policy (D3 settles it as the user's); any fifth role or role-picker for hosts (V4-HOST-05).

---

# Part C — Across both deliverables

## C.1 Owner choices, merged and ranked by how much design text depends on them

1. **Registration slot and revision policy** (DEL-02-02 §A.4 item 1): refuse same name / revision series per slot / authorized replacement; plus follow-or-pin. Governs the library model, collision dispositions, A15's subject, the catalog view, and agrees or disagrees with CA §4, EXEC RT-7, WD-EX E4. REQ-003 withholds the overwrite policy, so the owner decides.
2. **Role guidance source and change mechanism (OI-018)** (DEL-02-04 §B.4 item 1): bundled / seeded editable copy / project-local. Governs source identity, change policy, the adoption account and much of ROLE-v0.1.
3. **Whether a draft can be trial-run before registration** (DEL-02-02 §A.4 item 3): governs the journey states and run identities, and touches EXEC HR-3/TR-1 and RS R2 (a draft form of identity).
4. **TASK nondelegation: instruction-only, or a configuration override that enforces it** (DEL-02-04 §B.4 item 3): governs AC-003/AC-004's account and whether the App overrides user Codex configuration.
5. **Workflow supply ownership** (both; §C.2 S-1): whether DEL-02-04 composes and supplies the selected workflow (as four first-increment files assume) or DEL-02-02 does, or the agent reads it as a file. Integrator can prepare; owner only if it moves a deliverable obligation (an SCA-V4-003 item).
6. **Registration control: DEL-01-04's act control or a DEL-02-02 control** (DEL-02-02 §A.4 item 4): integrator design, owner confirmation if SC2-01-04-1's K1-4 wording changes.
7. **Authorization for a live Codex observation** (DEL-02-04 §B.4 item 4; P-15 and delegation), as K1-6 did once.
8. **No-role session and default role** (DEL-02-04 §B.4 item 5): small text.

Items the integrator can take (not owner): review-as-binding (A item 5 (a)); draft identity and storage; package hygiene; unregistered library content standing; A15 purpose wording; host precedence default; composition order; native child roles; instruction-discovery treatment; compatible-roles mismatch.

## C.2 Structural questions that could force restructuring of a first-increment Design file

- **S-1 Who supplies the workflow to the agent, and by which route.** WD §3.9 OS-7 and §6.2, EXEC §2.6 A-3 and §6.1 *supplied*, HOSTING S-6 ("inputs from DEL-02-01/02-02") and §8.2 assume DEL-02-04 composes the workflow into the additive guidance inputs. DEL-02-04's SoW covers role guidance only; no register row joins DEL-02-04 to DEL-02-02 (a new one would be inside SCC-002, held and SCC-neutral). WD CR-7 meanwhile says the agent receives the block "when it reads the file", a different route whose *supplied* evidence is a tool item, not HOSTING §8.2 evidence. Choosing the file-read route would change the *supplied* rows in WD §6.2, EXEC §6.1, HOSTING §8.2 and RS R3.
- **S-2 Drafts and runs.** EXEC HR-3/TR-1/T-1 and WD OS-2/OS-3 make "a draft has no workflow identity and cannot be selected for a run" structural. If the owner allows draft trials (§C.1 item 3), RS R2 and EXEC's run identity need a draft form, and WD §6.1 a draft reference beside the tuple.
- **S-3 Two meanings of "derived from".** WD §6.1 and EXEC HR-4 use *derived-from* for the parent **workflow tuple**; ACT §2.5 and RS HA-10 (and RS schema `relations.derivedFrom`, act-log example, VC-37) use *derived from ⟨draft⟩* for A15. A changed definition's A15 probably also needs the **prior revision**. Renaming or splitting the relation touches ACT, RS's schema and fixtures.
- **S-4 Registration control vs act control.** ACT §2.6 gives A15 to a DEL-02-02 "registration control"; EXEC §5 CAP-1…CAP-9 and SC2-01-04-1 define one App act control "for one act kind at a time" whose consumers exclude DEL-02-02. Unifying changes ACT §2.6, RS HA-10 and SC2-01-04-1; keeping two needs CAP-4's guarantee stated twice under OI-008.
- **S-5 Slot policy (a) would unsettle the round trip.** CA §4 (LIB-A1 holding ⟨rev-A2⟩ and ⟨rev-A3⟩ under one name), EXEC RT-6/RT-7 and WD-EX E4 assume a slot can hold successive revisions. If the owner chooses "refuse same name" (Root/v3 practice), those tables and WD C-4 ("follows a new revision of the same slot") need rework.
- **Minor, not structural:** EXEC U-E19 still cites "registration as an act (AP U-08)" though R12-5 closed U-08; ACT §10.3's DEL-02-02 row still says "Not mapped in detail (U-08)"; A15 purpose wording assumes a project library.

## C.3 Limits of this survey

- C1-A/B/C, S1-F and DECISIONS_DRAFT were read by search and their relevant sections, not every line; the large Design files likewise (§0 lists the sections).
- Generated-type facts are `observed-in-generated-types` only; OBS-1 is one turn at one version with one local model. Nothing is qualified.
- The v3 statements about registration recording and automation operability are inferences from reading the code, not from running it.
- No SWBPIPE join, witness or adoption is claimed; host matters stay deferred (DECISION-3).
