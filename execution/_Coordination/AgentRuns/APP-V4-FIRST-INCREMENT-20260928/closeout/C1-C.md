# C1-C — bounded closeout comparisons: DEL-05-01, DEL-05-02, DEL-09-06, DEL-09-09

- **Run / node:** APP-V4-FIRST-INCREMENT-20260928, closeout node C1-C.
- **Method:** `chirality-root:bundled:workflow:bounded-reconciliation`
  (`workflows/bounded-reconciliation/WORKFLOW.md`). Used here as a read-only
  comparison. Every warranted edit is returned as a **proposed change**.
- **Executor:** Type 2 TASK (Claude Code `Agent` subagent). It delegated
  nothing, used read-only git and no network, and wrote only this file.
- **Candidate:** commit `816c917f0` (R5 final set, with the EXEC-v0.3 E1
  alignment of CA and RELAY). Every deliverable file below was read with
  `git show 816c917f0:<path>`. The registers, SoWs, `_DEPENDENCIES.md` and
  `_STATUS.md` are unchanged since base `6e18505e3`.
- **Brief:** BRIEFS.md "C1 — bounded closeout comparisons". The section was
  read from the working copy (sha256 `c85c3519…`), which differs from the
  candidate copy (`f0d5fcf7…`) only by the added C1 text. Also read:
  - OWNER_DECISIONS.md (`a9869129…`: DECISION-1 D1–D4, DECISION-2 D5/D6);
  - R1–R5 (R5_RESOLUTIONS.md `254d0b93…`);
  - V1-A/B/C §6–7;
  - IR1-A/B/C SoW-fidelity sections;
  - V2 §4;
  - V3-A/V3-B verdicts and minors;
  - the DAG-001 accepted graph files `DependencyEdges.csv` (109 arcs) and
    `CandidateEdges.csv` (52 arcs), both at the candidate.
- **Boundary (binding).** No SoW, `Dependencies.csv`, `_DEPENDENCIES.md`,
  `_STATUS.md`, `_CONTEXT.md` or `_REFERENCES.md` is edited. All changes below
  are **proposed and unapplied**. They go to a successor undertaking through
  their owning route. New arcs also need `project-dag` departure (DAG-002).

| Deliverable file at `816c917f0` | sha256 (prefix) |
|---|---|
| DEL-05-01 `ScopeOfWork.md` / `Dependencies.csv` / `_DEPENDENCIES.md` / `_STATUS.md` | `6fbbb580…` / `fd44d166…` / `46bbb080…` / `7070599f…` |
| DEL-05-01 `Design/LOOP_RECEIVING_CONTRACT.md` (LOOP-v0.5) | `43e039aa…` |
| DEL-05-02 `ScopeOfWork.md` / `Dependencies.csv` / `_DEPENDENCIES.md` / `_STATUS.md` | `5c554956…` / `92067b62…` / `abf784e0…` / `3a878534…` |
| DEL-05-02 `Design/PANEL_RECEIVING_CONTRACT.md` (PANEL-v0.5) | `e7d62bee…` |
| DEL-09-06 `ScopeOfWork.md` / `Dependencies.csv` / `_DEPENDENCIES.md` / `_STATUS.md` | `511f2c00…` / `ce3218a2…` / `0943c9be…` / `b3b29c31…` |
| DEL-09-06 `Design/CONNECTED_ACTIVITY_CONTRACT.md` (CA-v0.3) / `Design/RELAY_QUESTIONS_SWBPIPE.md` (RELAY-v0.3) | `28a5cb80…` / `89b6b9c9…` |
| DEL-09-09 `ScopeOfWork.md` / `Dependencies.csv` / `_DEPENDENCIES.md` / `_STATUS.md` | `082db8fa…` / `02d738c7…` / `bd82758a…` / `d4d8f318…` |
| DEL-09-09 `Design/EXTERNAL_TRACE_CASES.md` (XT-v0.3) | `2b2be1e1…` |

**Conventions.**
- Arcs are written **consumer → supplier**.
- **New arc**: the consumer–supplier pair appears in neither DAG-001
  `DependencyEdges.csv` nor `CandidateEdges.csv`. Adding it changes topology,
  so it needs DAG-002.
- **Mirror only (no topology change)**: either a mirror row for an arc DAG-001
  already carries, or an edit to an existing or EXTERNAL/constraint row. DAG-001
  treats those rows as non-topological (`Evidence/NonTopologicalInputs.csv`).
- Dependency IDs for new rows are provisional. The register owner's extraction
  run assigns them.
- Under CONSERVATIVE extraction a row needs positive SoW evidence. Each
  new-arc row therefore depends on its paired SoW change being applied first.
- SCC effect was computed with Tarjan's algorithm over the DAG-001 arc set plus
  the proposals. Adding all fourteen proposed new arcs leaves every SCC's
  membership unchanged. One arc that was considered and **not** proposed,
  DEL-09-09 → DEL-09-06, would pull DEL-09-06 into SCC-002 (see §4 of
  DEL-09-09).

## Summary

| DEL | OUT developed / partial / not addressed | Proposed SoW changes | Proposed register changes: mirror-only / new-arc | Lifecycle observation |
|---|---|---|---|---|
| DEL-05-01 | 3 / 1 / 0 | 4 | 3 / 1 | INITIALIZED. IN_PROGRESS would now be truthful. Not changed |
| DEL-05-02 | 2 / 2 / 0 | 6 | 5 / 2 | INITIALIZED. IN_PROGRESS would now be truthful. Not changed |
| DEL-09-06 | 0 / 4 / 0 | 4 | 5 / 8 | INITIALIZED. IN_PROGRESS would now be truthful. Not changed. OUT-003 cannot complete in this undertaking |
| DEL-09-09 | 0 / 3 / 0 | 5 | 3 / 3 | INITIALIZED. IN_PROGRESS would now be truthful. Not changed |
| **Total** | 5 / 10 / 0 | 19 | 16 / 14 | — |

---

## DEL-05-01 — Minimal-loop and model receiving contract

### 1. Commitment → result

LOOP = LOOP-v0.5. "Remaining" names the kind of work left:
- **def**: definition work;
- **input**: a supplied input or decision;
- **impl**: implementation;
- **wit**: a witness or observed host evidence.

| SoW item | Developed in | Standing | Remaining |
|---|---|---|---|
| OUT-001 receiving contract | §1, §2 (four subjects), §3, §4, §5.1, §6, §7, §8, §9 | **Developed** | input: DEP-05-01-024 representation (§4 fragments; MC-6, MC-8 held); N-OPEN-1…3 (§5.1) |
| OUT-002 tool-call/model fixtures | §11 (FX-V/S/D/U/R/NP/O/UNDO/M/N/C) on FX-PIPE-01 plus V-GR1 | **Partial** | input: model-interface basis DEP-05-01-024 is UNKNOWN, so the fixtures are case designs only and none is executable (§11 preamble). impl: a test-double run |
| OUT-003 conformance cases and evidence expectations | §5.2, §7, §8, §12 labels, VC-01…09 | **Developed** (definition) | wit: every host observation is NOT-OBSERVED (DEP-001). FX-C9 is AWAITING INPUT (SQ-02) |
| OUT-004 allocation / open-choice account | §10.1–§10.3, UNRESOLVED | **Developed** | input: OI-013, OI-014, DEP-001. §10.1/§10.3 carry stale standing text (residual D5-1-2 below) |
| REQ-001 local default, cloud by choice, native endpoint, key | §5.1 NW-1…NW-7, §5.2 MS-01…11 | Developed | input: N-OPEN-1 (MS-11 held) |
| REQ-002 minimal Chat Completions; four-subject boundary; distinct from the App path; Pi unselected | §1, §2, §4 | Developed | input: DEP-05-01-024 |
| REQ-003 schema before domain; malformed calls never empty | §6 (V-1…V-5, O-1…O-6), §7 | Developed | input: T-OPEN-1 (MC-8); U-P9 |
| REQ-004 responsiveness; no prescribed means | §8 RS-1…4, §3 | Developed | wit: host observations. R-OPEN-1 intentionally open |
| REQ-005 required inputs and standing | §10.3, UNRESOLVED | Developed | Currency residual D5-1-2 |
| REQ-006 no act owned by others | §0 "Who builds what", §10.1 | Developed | SoW clarification S5-1-2 |
| REQ-007 distinct acts; declared checkpoint waits | §2.3, §2.4 (C-1…C-8, §2.4.4), §9 | Developed | input: U-E4, U-03 (owner). Hold machine rests on EXEC §4 (PROPOSED (W7), adopted per R4-3…R4-7) |

### 2. Result → commitment (beyond or outside the SoW text)

| Design element | Authority | Assessment |
|---|---|---|
| The host loop evaluates reached-when, binds subject classes and realizes the EXEC hold machine; hold support *enforced by the host loop* (§2.4.1–§2.4.4) | R-5 allocation ("DEL-05-01 evaluates in hosts"); R2-17, R3-1/R3-2; R4-2…R4-7; R5-1/R5-3/R5-5 | Supported by rulings. SoW REQ-006 excludes "implementing workflow execution/checkpoint behavior of DEL-02-03", so a clarification is proposed (S5-1-2) |
| Governing checkpoint constraint and its carriage assurance (C-6, §6.2) | R2-12, R4-14, R5-2 | Supported |
| Five class values, the reserved-operation rule, faithful-record conditions (§2.2) | R2-1, R2-2, R2-4 | Supported |
| Grant states carried and grant in force per dispatch (O-6, §6.2, E-4) | R-8, R2-6 (DEL-04-02 meaning) | **Outside CLM-002 and the register** (X-16; LOOP §10.1 "Register gap (C1)"). S5-1-1 and R5-1-1 below |
| Per-turn supplied-guidance and model-setting records (§2.1 M-5) | R2-20, X-18, aligned with R5-4 | Supported. Host capability relayed as SQ-19 |
| Retry, de-duplication, per-item stale, undo (§6.3, FX-O1, FX-UNDO) | R-7, R2-13, R2-15, R3-4 | Supported |
| NW-4…NW-7, MC-7, the MC-8 grouping | Labeled PROPOSED (this file) | Within REQ-001/REQ-003. Awaits comparison and owner review |
| §13 relay questions | SoW Methods (human-relayed file path); consolidated in RELAY §3 | Supported. Prepared, **not delivered** |

No unsupported addition was found.

### 3. Proposed SoW corrections (`ScopeOfWork.md`, DEL-05-01)

| # | Locus | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| S5-1-1 | CLM-002; REQ-006 exclusion list | CLM-002: "…`DEL-04-03` owns shared human-act/run-record format; and `DEL-05-02` owns the App/shared panel receiving contribution." | Insert before "and `DEL-05-02`": "`DEL-04-02` owns the autonomy-grant display states and standing exchange, which this deliverable consumes as the grant in force carried on each dispatch;". In REQ-006, add "defining the autonomy-grant display states or standing exchange of `DEL-04-02`;" | V1-A RF-05; V1-C RF-5 / AB-04; R2 X-16; LOOP O-6, §6.2, §10.1; AS Receivers and U-15. Pairs with R5-1-1 |
| S5-1-2 | REQ-006, after "…implementing workflow execution/checkpoint behavior of `DEL-02-03`;" | (as quoted) | Add a sentence: "Stating the receiving obligations under which a host loop evaluates reached-when and realizes `DEL-02-03`'s hold machine and hold-support values (integration allocation R-5; R5-1) is this deliverable's receiving work, not implementation of `DEL-02-03`." | R1 R-5; R4-2; R5-1; IR1-C §4 (loop-side evaluation labeled as an addition). The wording is lifted to the ruling, not to the mechanism |
| S5-1-3 | CLM-004 (and the Issues source row) | "The person performs proposal acceptance, marking work checked, approval and professional reliance; …" | Append: "For the first increment's App/shared contracts, `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 also reserves changing the autonomy grant or enabling external access (D2(e)). D3 establishes that hosts have no classifier permission mode. Operation-specific additions remain under OI-021, and host adoption under DEP-001." Add DECISION-1 to the Issues/Acceptance source row | DECISION-1 D2/D3; R2-11 (credit the ruling only with what it says); LOOP §9 A-5 |
| S5-1-4 | TBD-003 | "…detailed protocol/fixture representation and conformance observations must be supplied or agreed at their actual points of use; …" | Append: "The questions for these inputs are consolidated in DEL-09-06 `Design/RELAY_QUESTIONS_SWBPIPE.md` (SQ-01, SQ-02, SQ-03, SQ-08, SQ-11, SQ-19, SQ-21, SQ-29…SQ-32). The file is prepared for human relay and is not delivered. SQ-29 asks for the model-interface basis of DEP-05-01-024." | Navigation pointer to an existing artifact. RELAY §3; LOOP §13 |

R-4 wording check: "checking" in CLM-004, AC-008 and VER-008 names the
person's A4. That use is consistent with R-4, so no change is proposed.
Nothing in this SoW calls OI-001 or OI-002 open.

### 4. Proposed register changes (`Dependencies.csv` / `_DEPENDENCIES.md`, DEL-05-01)

| # | Change | Kind | Grounds |
|---|---|---|---|
| R5-1-1 | New row DEP-05-01-025: UPSTREAM INTERFACE, DELIVERABLE DEL-04-02 "Visible autonomy and result standing". Statement: "Receive the adopted grant display states and settings references carried as the grant in force on each dispatch and in run evidence; this deliverable does not define them." Evidence: the amended CLM-002 (S5-1-1) | **New arc** DEL-05-01 → DEL-04-02 (inside SCC-002; no membership change) | V1-A RF-05; V1-C RF-5; X-16; LOOP §10.1 |
| R5-1-2 | New row: UPSTREAM INTERFACE, DELIVERABLE DEL-01-05, mirroring DEP-01-05-014 (DEL-01-05 supplies local-server capability requirements and qualification limits, preserving the App-provider versus host-model interface distinction) | **Mirror only** (arc DEL-05-01 → DEL-01-05 is admitted in DAG-001) | DEP-01-05-014. LOOP-v0.5 does not yet consume it. Its point of need is N-OPEN-1 (MS-11). DEL-01-05 is outside D1. Alternatively the register owner may record why no consumer row is kept |
| R5-1-3 | New EXTERNAL row: DOWNSTREAM HANDOVER → DEP-001 "External SWBPIPE owner — loop receiving questions via App manager/human relay". Statement mirrors DEP-05-02-018 and names the RELAY file | **Mirror only** (EXTERNAL; non-topological) | SoW Methods; LOOP §13; consistent with DEP-05-02-018 |
| R5-1-4 | No row for OI-001 or OI-002 (V1-A RF-04) | No change | D2/D3 decide these matters. The residual (OI-021 additions) reaches this loop through DEL-04-01 (DEP-05-01-018) |
| R5-1-5 | DEP-05-01-024: Notes add "asked as RELAY SQ-29 (prepared, not delivered)". TargetType stays UNKNOWN and the status stays PENDING | **Mirror only** (row edit) | CA EC-14; RELAY SQ-29 |
| — | Keep the mutual UPSTREAM pairs DEP-05-01-016/-020 ↔ DEP-02-01-020, DEP-05-02-010 | No change | V1-C RF-10; CASE-002 |

Counted: mirror-only 3 (R5-1-2, R5-1-3, R5-1-5); new arc 1 (R5-1-1).

The following mirrors for this deliverable's arcs sit in **other** registers
(C1-A/C1-B scope). They are listed here and not counted:
- DEL-03-01 DOWNSTREAM (V1-C RF-1);
- DEL-03-02 DOWNSTREAM (RF-2);
- DEL-02-01 DOWNSTREAM (RF-3);
- DEL-02-03 mirror of DEP-05-01-017 (RF-8);
- DEL-04-01 DOWNSTREAM for DEP-05-01-018 (V1-A RF-02).

DEL-05-01 has no DOWNSTREAM row for its six consumers:
- DEL-02-01;
- DEL-03-04;
- DEL-05-02;
- DEL-08-01;
- DEL-09-06;
- DEL-10-03.

DAG-001 represents each of those arcs from the consumer side, so supplier-side
mirrors are optional and are not counted.

### 5. Open items

| Item | Owner | Point of need |
|---|---|---|
| OI-013 loop placement, parsing, persistence, panel assembly | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts |
| OI-014 shared placement (no common loop is proposed, §10.2) | App/shared contract owners | Before structural/production allocation |
| DEP-05-01-024 model interface and fixture basis (SQ-29) | UNKNOWN supplier. The App/shared embedded-integration owner receives or agrees it | At fixture/conformance use |
| DEP-001 host evidence (SQ-01/02/03/08/11/19/21/29–32) | SWBPIPE outside implementation session, via the human | Before corresponding integration/examination and the fallback-replacement decision |
| OI-021 operation, operation-specific reserved additions, OP-C11 class | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution |
| U-E4 (SP-6 alternative); U-03 (partial-lapse purpose) | Owner; DEL-04-01 with the owner | Before hold-machine implementation; at its point of need |
| N-OPEN-1…3; T-OPEN-1; R-OPEN-1; C U-C3/U-C5/U-C6; U-P1/U-P9; U-09 | As listed in LOOP UNRESOLVED | As listed there |
| Independent check of the single-author LOOP/PANEL v0.5 pair (G-4) | Graph maintainer (a fresh reviewer) | Before either file is relied on as checked |
| Application of S5-1-1…4 and R5-1-1…5 | HELP_HUMAN / WORKING_ITEMS in a successor undertaking. R5-1-1 also needs `project-dag` (DAG-002) | Before DAG-002 or the next SoW revision |

**Design residuals.** These are production edits for the graph, not applied
here:
- **D5-1-1.** The header, §2.4, §10.1 and UNRESOLVED cite EXEC-v0.2. The
  candidate carries EXEC-v0.3 (`d3cebd1cc`). EXEC-v0.3 §3.6 already aligns
  model-supplied carriage with R5-1 (*not established* before SQ-02, *not
  enforceable* after), so G-5 can close.
- **D5-1-2.** §10.1 and §10.3 carry stale standing text:
  - "EXEC-v0.1 read at `f05c7e4cd`";
  - "ACT-v0.2 read. R2-1…R2-10 pending";
  - "PANEL-v0.3";
  - "R4-14 … pending P-v0.4";
  - "R4-9 pending WD-v0.4";
  - the column heading "Standing at v0.3".
- **D5-1-3.** The UNRESOLVED row "R5-n elements not yet in sibling text" is now
  satisfied at the candidate: C-v0.5 carries V-GR1, EXEC-v0.3 §3.6 carries the
  four values, and P-v0.5 §3.3 carries host-held. §13 cites RELAY-v0.2, but
  RELAY-v0.3 is current (SQ ids are unchanged).

### 6. Lifecycle observation

`_STATUS.md` reads **INITIALIZED** (2026-09-27). Agent production work under
the owner's D1 scope has produced LOOP-v0.1…v0.5, and warranted open scope
remains. **IN_PROGRESS** ("active human + agent work", SPEC §3.4) would
therefore be the truthful state. CHECKING is not warranted:
- OUT-002 fixtures are not executable;
- host evidence is absent;
- G-4 is open.

The transition belongs to the human or WORKING_ITEMS. It is not made here.

---

## DEL-05-02 — Host panel and shared interaction receiving

### 1. Commitment → result

PANEL = PANEL-v0.5.

| SoW item | Developed in | Standing | Remaining |
|---|---|---|---|
| OUT-001 panel interface and receiving requirements | §1–§5: the four interactions §3.1–§3.4, checkpoints §3.5, grant §3.6, host views §4, acts and wording §5 | **Developed** | input: OI-013 (assembly); DEP-001 |
| OUT-002 reusable-component allocation account | §6 (candidates, consumers, agreement "None"; host construction boundary; OI-013/014) | **Developed** | input: OI-014 agreement |
| OUT-003 receiving cases, then candidate-bound results | §7 PC-01…PC-29 with accounting states | **Partial** | wit: every case is DESIGNED — UNEXECUTED. Recording results needs a host candidate (DEP-001) and actual acts (DEP-05-02-017). PC-23/PC-28 are HELD (OI-021); PC-24 is AWAITING INPUT (SQ-02) |
| OUT-004 conditional reusable components | §6 "OUT-004 conditional state" | **Partial** (the conditional state is recorded, as AC-006 allows) | impl: no component can exist until OI-014 agrees a repeated responsibility |
| REQ-001 four interactions traced to consumed definitions | §3.1–§3.4 "Consumed definitions" / "Unresolved" rows | Developed | — |
| REQ-002 host tables and views; no agent-private surface; old/new/reason | §2 P-1…P-3, §3.3, §3.4, §4 H-1…H-6 | Developed | wit |
| REQ-003 distinct acts; "accept"; faithful record; lapse | §3.5 W-5a…g, §5 W-1…W-6, K-1…K-4 | Developed | input: U-E4, U-03; DEP-001 capture reference (SQ-01) |
| REQ-004 repeated responsibility; OI-013/014 kept separate | §6 | Developed | input |
| REQ-005 cases against checked contracts; host claims only on evidence | §7 states and preamble | Developed | wit |
| REQ-006 no act owned by others | §3 "Responsible" rows, §6 boundary, VC-07 | Developed | SoW additions S5-2-2/3 |

### 2. Result → commitment

| Design element | Authority | Assessment |
|---|---|---|
| §3.6 active autonomy grant (seven display states, including *effective (policy default)*) | R-8, R2-6, R2-9, R4-6; AS §3 | **Outside CLM-002 and the register.** PANEL flags it itself (F-3 → C1). See S5-2-2 and R5-2-1 |
| §3.2 hold support in the four R5-1 values; §3.5 W-5b/c/e/f/g hold-machine displays (re-hold, no resumption, SP-6, MX rules, A12 control relation) | R4-2…R4-7, R5-1, R5-3, R5-5. The values are owned by DEL-02-03 EXEC §3.6 (R5-1), and EXEC §4.7–§4.11 resolve PANEL's held items | **Outside CLM-002**. DEL-02-03 is not named. See S5-2-3 and R5-2-2 |
| §3.3 stale after acceptance; resubmission; undo; resulting objects | R2-13…R2-16, R3-4 | Supported (within CLM-002 P consumption) |
| §3.2 holding library; required-tool outcomes; runnable rule | R2-20, WD §4.2.4, IR1C-13 | Supported (DEL-02-01) |
| §1 permission layer (no classifier mode; no routine prompts) | D3 (SETTLED); DERIVED per R2-11 | Supported. The SoW still calls OI-002 open (S5-2-1) |
| §8 Q-1…Q-9 → RELAY SQ ids | CLM-005; DEP-05-02-018 | Supported. Prepared, not delivered |

### 3. Proposed SoW corrections (`ScopeOfWork.md`, DEL-05-02)

| # | Locus | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| S5-2-1 | TBD-004; TBD-005; REQ-003 last sentence; CLM-004 first sentence; source row I | TBD-004 "Consumed-policy issue OI-001, Reserved human acts, remains OPEN. …". TBD-005 "…OI-002, Classifier routine permissions, remains OPEN. …". REQ-003 "…without deciding OI-001/OI-002." | TBD-004: "OI-001 is ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (five reserved acts), carried through DEL-04-01. Operation-specific additions remain under OI-021, and host naming, enforcement and adoption under DEP-001 (V4-HI-30)." TBD-005: "OI-002 is ruled by D3: in the App, routine tool-permission and sandbox modes are the user's own Codex setting. Hosts have no classifier mode in the first increment, and the SWB default proposal mode applies." REQ-003: "…consuming DECISION-1 D2/D3 as carried by DEL-04-01, without deciding operation-specific additions (OI-021)." In CLM-004 add "(ruled for App/shared contracts by DECISION-1 D2/D3)" | DECISION-1 D2/D3 and its "Effects" (C1 reconciles pointers); R2 "Carried to C1"; R4 "Carried to C1"; V2 §4 residuals |
| S5-2-2 | CLM-002; REQ-006 | CLM-002 list ends "…and `DEL-05-01` supplies loop messages/tools/events/checkpoints and receiving requirements." | Add: "`DEL-04-02` supplies autonomy-grant display states and active scope." In REQ-006 add: "grant display and standing-exchange definition to App-v4 `DEL-04-02`" | PANEL §3.6, F-3; V1-C RF-4; V1-A RF-05; X-16; IR1-C §4. Pairs with R5-2-1 |
| S5-2-3 | CLM-002; REQ-006 | (as above) | Add: "`DEL-02-03` supplies the hold-support values and hold-machine meanings (resume, re-hold, run end, act ordering, mixed decisions) that the panel displays." In REQ-006 add: "workflow execution and hold-machine definition to App-v4 `DEL-02-03`." **Alternative for the owner:** state that these meanings are consumed only through DEL-05-01. That alternative adds no arc | PANEL §3.2, §3.5, §7 note; R4-3…R4-7; R5-1; EXEC §4.7–§4.11 resolve PANEL holds. V1-C RF-4 (the F-2 part was closed at v0.2 but is reopened by R4/R5) |
| S5-2-4 | P/OQ-11 paragraph (after TBD-005) | "P/OQ-11 separately leaves the first connected activity's exact operation, autonomy, environment and externally supplied interfaces with the **App manager, human and external SWBPIPE owner** …" | Insert after "P/OQ-11": "(tracked as OI-021 in `Open_Issues.csv`, owner *Owner via outside SWB session and App/shared owner*, point of need *before connected-activity SoW and execution*)". The OQ-11 owner wording differs from OI-021's; the owning route reconciles them | V1-C RF-9; PANEL F-4 |
| S5-2-5 | TBD-003 | "…For this deliverable, receive the relevant panel/view and interaction evidence; …" | Append: "This includes a stable capture-evidence reference for each host-captured act (RELAY SQ-01), host handling of the governing checkpoint constraint (SQ-02), and the host loop's actual hold behavior (DEP-001). The questions are consolidated in DEL-09-06 `Design/RELAY_QUESTIONS_SWBPIPE.md`, which is prepared and not delivered." | PANEL F-5, F-8; R2-20 / X-17; RELAY §1 P1 |
| S5-2-6 | CLM-002 "Their checked definitions…"; OUT-003 "checked interfaces"; REQ-001 "the checked workflow, … definitions"; REQ-005 "checked source contracts"; AC-005 "the checked interfaces"; Methods "checked input definitions" | "checked" used for independently compared contract versions | Replace with "identified, independently compared" (e.g. "Their identified, independently compared definitions are consumed here"). This is a lift with no change of meaning | R1 R-4: unqualified "checked" is reserved for A4 |

### 4. Proposed register changes (DEL-05-02)

| # | Change | Kind | Grounds |
|---|---|---|---|
| R5-2-1 | New row DEP-05-02-019: UPSTREAM PREREQUISITE, DELIVERABLE DEL-04-02. "Panel receiving requirements consume the checked autonomy-grant display states and active scope supplied by App-v4 DEL-04-02; the required input must be identified or recorded as unavailable." Evidence: the amended CLM-002 (S5-2-2) | **New arc** DEL-05-02 → DEL-04-02 (inside SCC-002) | V1-C RF-4; V1-A RF-05; X-16; PANEL F-3 |
| R5-2-2 | New row DEP-05-02-020: UPSTREAM PREREQUISITE, DELIVERABLE DEL-02-03 (hold-support values and hold-machine meanings). Not needed if the owner takes the S5-2-3 alternative | **New arc** DEL-05-02 → DEL-02-03 (inside SCC-002) | As S5-2-3 |
| R5-2-3 | DEP-05-02-014 (OI-001) and DEP-05-02-015 (OI-002): Notes and Statement point to DECISION-1 D2 and D3 respectively, with the residual (OI-021 operation-specific additions; host adoption DEP-001). Status stays ACTIVE. SATISFIED is not warranted, because host adoption is not evidenced | **Mirror only** (2 row edits) | V1-A RF-04; OWNER_DECISIONS "Effects" |
| R5-2-4 | DEP-05-02-016 (OQ-11): Notes add "same matter as OI-021 (Open_Issues.csv)". The register owner may instead retarget TargetRefID to OI-021 and keep OQ-11 as the source | **Mirror only** (row edit) | V1-C RF-9; PANEL F-4 |
| R5-2-5 | DEP-05-02-011 (DEP-001): Statement names the capture-evidence reference (SQ-01), constraint handling (SQ-02) and the host loop's hold behavior | **Mirror only** (row edit) | PANEL F-5, F-8 |
| R5-2-6 | DEP-05-02-018: Notes add "questions consolidated as RELAY-v0.3 SQ-02, SQ-01, SQ-22, SQ-23/SQ-10, SQ-21, SQ-18 (a), SQ-24, SQ-05 (c)/(e), SQ-20; prepared, not delivered" | **Mirror only** (row edit) | PANEL §8 |

Counted: mirror-only 5 (R5-2-3 ×2, R5-2-4, R5-2-5, R5-2-6); new arc 2.

The DEL-04-01 DOWNSTREAM mirror for DEP-05-02-008 (V1-A RF-02) and the
DEL-03-01/03-02/02-01 mirrors (V1-C RF-1…3) belong to other groups. DEL-05-02
has no DOWNSTREAM mirror for its five consumers:
- DEL-02-01;
- DEL-03-04;
- DEL-05-01;
- DEL-09-06;
- DEL-10-03.

These are optional and not counted.

### 5. Open items

| Item | Owner | Point of need |
|---|---|---|
| OI-013 panel assembly, host/common boundary, persistence | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts |
| OI-014 whether any §6 candidate becomes shared (OUT-004) | App/shared contract owners | Before structural/production allocation |
| OI-021 / OQ-11 (PC-23, PC-28 HELD) | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution / live examination |
| DEP-001 panel/views, act capture (SQ-01), constraint (SQ-02), list adoption; PC-24 | SWBPIPE outside implementation session | Before corresponding integration/examination and fallback-replacement decision |
| DEP-05-02-017 actual human acts (PC-07, PC-18, PC-19, PC-21) | The person performing the act | When those cases execute |
| U-E4; U-03; C U-C5; P U-P3; which party evaluates required-tool outcomes | As in PANEL UNRESOLVED | As there |
| Independent check of the LOOP/PANEL v0.5 pair (F-1) | Graph maintainer (a fresh reviewer) | Before either file is relied on as checked |
| Application of S5-2-1…6 and R5-2-1…6 | Successor undertaking. R5-2-1/2 need DAG-002 | Before DAG-002 or the next SoW revision |

**Design residuals** (not applied):
- **D5-2-1.** The file cites EXEC-v0.2 (header, §3.5, §7 "Present state",
  UNRESOLVED), while EXEC-v0.3 is current.
- **D5-2-2.** VC-01 cites the consumed definitions "at `28bd00499`".
- **D5-2-3.** §8 cites RELAY-v0.2. The UNRESOLVED row "R5-n elements not yet in
  sibling text" is satisfied at the candidate.

### 6. Lifecycle observation

`_STATUS.md` reads **INITIALIZED**. Production work (PANEL-v0.1…v0.5) under D1
has occurred and warranted open scope remains, so **IN_PROGRESS** would be
truthful. CHECKING is not warranted: OUT-003 results and OUT-004 are
outstanding, and F-1 is open. Not changed here.

---

## DEL-09-06 — Connected activity contract and workflow round trip

### 1. Commitment → result

CA = CA-v0.3; RELAY = RELAY-v0.3.

| SoW item | Developed in | Standing | Remaining |
|---|---|---|---|
| OUT-001 increment SoW, owner/check allocation, handoff | CA §2.1–§2.5 (four activities, CA/E and CA/X variants, step map CA-0…CA-R, fixture sequence, DI-1…DI-9), §5, §6, §10 | **Partial.** A draft increment contract exists; the final operation-specific SoW is explicitly not claimed (AC-001 permits this) | input: OI-021 (DI-1…DI-3), SQ-01/SQ-02 (DI-4), SQ-28 (DI-9); D6 follow-up (DI-6) |
| OUT-002 reusable connected workflow | CA §3.1 WR-1…WR-11, §3.2 fixture WF-1/WF-1c | **Partial.** Requirements are defined; no workflow is authored (to be done later under `create-workflow` plus DEL-02-02 review/registration, D1) | def/impl: authoring and review. input: DI-1 |
| OUT-003 V4-EXM-14 joined round-trip witness | CA §4, §8 (W14-00…W14-10), §8.1 completion rule, §8.3 | **Partial.** Designed, **not run**. **It cannot complete in this undertaking** | wit: identified App and host candidates (SQ-27; App construction later); DEL-02-02 registration (later, D1; CA F-1) for W14-01/W14-09; host inputs SQ-01/02/03/17/18/19; actual acts (DEP-09-06-024); D6 for App-side checkpoints (W14-04 (iii); W14-09 "usable in App") |
| OUT-004 human-relayed questions and contribution/evidence account | RELAY (SQ-01…SQ-32, P1…P8, §3 map, §4 ledger); CA §7.2 standing ladder, §9 EC-01…EC-14 | **Partial.** The question set and account structure are developed. RELAY is **PREPARED FOR HUMAN RELAY — not delivered**; the owner relays it after the final review. Ledger: nothing relayed, answered, committed, delivered, adopted or examined | input: relay by the human; answers from the SWBPIPE owner |
| REQ-001 complete first activity and join | CA §2 | Developed (draft) | input: OI-021 |
| REQ-002 workflow declarations; source-qualified revisions; separate evidence facts | CA §3, §4 (EXEC §6 consumed) | Developed (definition) | wit |
| REQ-003 tools, unsupported outcome, checkpoint, interruption, revision at the round trip | CA W14-03, W14-04, W14-07, W14-10 | Developed (design) | wit. On CA/X, E1 is *unsupported* whatever SQ-02 returns (CA F-15; EXEC-v0.3 MT-2) |
| REQ-004 policy, autonomy, distinct acts | CA S-4…S-14, CA-H, W14-04/05/06 | Developed | input: OI-021 residual; U-E4; U-03 |
| REQ-005 proposed / received / delivered / adopted / examined | CA §7.2, §9; RELAY §0, §4 | Developed | input: relay |
| REQ-006 staging without PEC/Domains | CA §6 ST-0…ST-5 | Developed | — |
| REQ-007 OUT-003 needs an actual joined run | CA §8.1, §8.3, §7.1 | Developed (the rule). Completion is outstanding | wit |
| REQ-008 excluded acts and owners | CA §5, §10 | Developed | — |

### 2. Result → commitment

| Design element | Authority | Assessment |
|---|---|---|
| Acting-surface variants CA/E and CA/X, and hold support by variant (§2.2, S-13) | HI §8 / C §8 (three surfaces); DECISION-2 D6; R4-2, R4-8, R5-1, R5-2, R5-10; EXEC-v0.3 HS-5, MT-2 | Supported. The consequence is a SoW gap: D6 is not in the SoW (S9-6-2) |
| Model destination per turn (S-12; W14-08) | DECISION-2 D5 (no gate, SETTLED); R4-1/R5-4 (record and show, INTEGRATION) | Supported. D5 is not in the SoW (S9-6-2) |
| External contribution standing ladder (§7.2) | PROPOSED (W9), within REQ-005 | Supported as a proposal |
| WR-11 hold support per checkpoint and surface; F-15 recommendation (keep checkpoints on host operations) | R5-1; EXEC U-E23 | Supported. The owner D6 follow-up remains |
| RELAY P8 SQ-29…SQ-32 (host-loop model and network questions) | DEL-03-04 GUIDE-v0.1 G-3/CC-5 addendum; within OUT-004 | Supported |
| Consumption of C, P, ACT, AS, WD, WD-EX, ADAPTER and HOSTING at deliverable level | SoW CLM-003 names PKG-02 (specifically DEL-02-03), PKG-03, PKG-04 (records) and PKG-05 only | **Partly outside the SoW and register** (CA F-2). See S9-6-3 and R9-6-1…3 |
| Graduated-autonomy branch (T15–T17; W14-04 (ii)) | C T15 / V2 MAJOR-1 / R4-18; V4-EXM-22 overlap with DEL-09-07 | Supported. Owned for the joined witness only |

### 3. Proposed SoW corrections (`ScopeOfWork.md`, DEL-09-06)

| # | Locus | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| S9-6-1 | TBD-002; CLM-005 second sentence | TBD-002 "Preserve relevant policy choices without deciding them: OI-001 owner with App/SWB contract owners, **before operation-policy production contracts**, chooses always-reserved acts by concrete operation/consequence; OI-002 same owners, … settles classifier routine-permission treatment." | "`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 rules OI-001 for the first increment's App/shared contracts (five reserved acts), and D3 rules OI-002 (App: the user's Codex setting; hosts: no classifier mode; SWB default proposal mode). Operation-specific reserved additions remain with the owner via the outside SWB session and the App/shared owner under OI-021, before connected-activity SoW and execution. Host adoption remains under DEP-001." In CLM-005 add "(ruled for App/shared contracts by DECISION-1 D2/D3; operation-specific additions under OI-021)" | DECISION-1; CA F-3 (v0.1); R4 "Carried to C1" |
| S9-6-2 | New TBD-003 (DECISION-2) | — | "**TBD-003** — `APP-V4-FIRST-INCREMENT-20260928-DECISION-2`. D5 is settled: host content read over the external channel may reach the model the person selected, with no App gate; the destination is recorded per turn and shown (INTEGRATION reading, R4-1/R5-4). D6 is deferred: App-side run holds await the SWBPIPE answer to relay SQ-02, and that answer can settle only checkpoints on host operations. App-only checkpoints stay *not enforceable*, so a workflow is *unsupported* on the App/external surface until a separate owner D6 follow-up (R5-1, R5-10). This affects REQ-003/AC-004 on the App route (W14-04 (iii)) and AC-003 "made usable in App" for workflows with App-only checkpoints (W14-09). Owner: the owner, on the SQ-02 answer and a separate follow-up. Point of need: before App-side checkpoint enforcement is claimed and before W14-04 (iii)/W14-09 execute." | DECISION-2; R4-2, R5-1, R5-10; CA S-12, S-13, F-10, F-15. This is the analogue of the DEL-02-03 REQ-002 gap |
| S9-6-3 | CLM-003; REQ-008 exclusion list | CLM-003 "App PKG-02 supplies workflow-making and portability, specifically App DEL-02-03 …; App PKG-03 supplies catalog meanings/tools; App PKG-04 supplies records of actual content-bound acts; App PKG-05 supplies receiving integration. …" | Name the deliverable-level suppliers the definition actually consumes: "App DEL-02-01 supplies portable declaration, identity and revision meaning; App DEL-02-02 (later undertaking) supplies review and registration; App DEL-03-01, DEL-03-02 and DEL-03-03 supply catalog/read-basis, proposal/outcome and external-receiving meanings; App DEL-04-01 carries adopted operation policy and act distinctions and App DEL-04-02 grant display, alongside DEL-04-03 records; App DEL-01-01 supplies the App-side supplied-guidance and model-destination evidence." Add the matching REQ-008 exclusions | CA F-2 (v0.1); CA §2.3, §4, §5, W14-08. Pairs with R9-6-1…3 |
| S9-6-4 | OUT-004 | "…The human-relayed external questions, proposed interfaces, received answers/commitments and contribution/evidence account…" | Append: "The question set is `Design/RELAY_QUESTIONS_SWBPIPE.md` and the account is `Design/CONNECTED_ACTIVITY_CONTRACT.md` §9. Each holds exactly one standing on the ladder prepared → relayed → answered → committed → delivered → adopted → examined." | Navigation pointer. CA §7.2, §9; RELAY §4 |

R-4 wording check: "checking" in CLM-005, REQ-004 and AC-004 names the
person's act, and "model-adjustment/checking activity" names the non-mutating
check. Both uses are consistent, so no change is proposed.

### 4. Proposed register changes (DEL-09-06)

| # | Change | Kind | Grounds |
|---|---|---|---|
| R9-6-1 | Resolve the package row DEP-09-06-012 (PKG-02) to deliverable rows, as the R5 target resolution did for DEP-09-06-015. Add UPSTREAM INTERFACE rows to **DEL-02-01** and **DEL-02-02**. DEP-09-06-013 (DEL-02-03) stays. The PKG-02 row is retired or kept as the register owner decides | **New arc** ×2: DEL-09-06 → DEL-02-01; DEL-09-06 → DEL-02-02 | CA §3.1, §4, W14-01, W14-09; CA F-1/F-2. DEL-02-02 is outside D1, so the owner may defer that row |
| R9-6-2 | Resolve DEP-09-06-014 (PKG-03) into UPSTREAM INTERFACE rows to **DEL-03-01**, **DEL-03-02** and **DEL-03-03** | **New arc** ×3 | CA §2.2, §2.3 (CA-0…CA-5); CA F-2 |
| R9-6-3 | Add UPSTREAM INTERFACE rows to **DEL-04-01**, **DEL-04-02** and **DEL-01-01** | **New arc** ×3 | CA S-8, CA-2, CA-H (ACT); CA-0/CA-H/CA-R (AS); §4 "supplied" link and W14-08 (HOSTING §8.2/§8.3); CA F-2 |
| R9-6-4 | UPSTREAM row to DEL-09-01, mirroring DEP-09-01-024 (reusable examination support and evidence interfaces) | **Mirror only** (arc admitted in DAG-001) | CA §5 "Examination infrastructure and protocol", §7; CA F-4 |
| R9-6-5 | DOWNSTREAM HANDOVER row to DEL-09-07, mirroring DEP-09-07-011 | **Mirror only** | CA Receivers, §11.2. DEL-09-07 is outside D1 |
| R9-6-6 | DEP-09-06-022 (OI-001) and DEP-09-06-023 (OI-002): point to DECISION-1 D2/D3 with the OI-021 and DEP-001 residual. SatisfactionStatus is not moved to SATISFIED | **Mirror only** (2 row edits) | As S9-6-1 |
| R9-6-7 | New EXTERNAL row: DOWNSTREAM HANDOVER → DEP-001 "External SWBPIPE owner — human-relayed question set (RELAY_QUESTIONS_SWBPIPE.md)". No row covers the OUT-004 question handoff today; DEP-09-06-020 is the workflow handoff | **Mirror only** (EXTERNAL; non-topological) | SoW OUT-004, REQ-005; RELAY header |
| — | Considered, **not proposed**: DEL-09-06 → DEL-09-09 (coordination under CLM-006; the dependency extract rightly drew no edge from the exclusions); DEL-09-06 → DEL-03-04 (GUIDE only sourced SQ-29…32) | — | Keeps DEL-09-06 outside SCC-002 |

Counted: mirror-only 5 (R9-6-4, R9-6-5, R9-6-6 ×2, R9-6-7); new arc 8.
None of the eight new arcs changes SCC membership: DEL-09-06 stays outside
SCC-002. V1-B RF-09 records that this register uses SatisfactionStatus `TBD`
where siblings use `PENDING`; that is left to the register owner.

### 5. Open items

| Item | Owner | Point of need |
|---|---|---|
| **Relay of RELAY-v0.3** to the SWBPIPE session. It is prepared, not delivered, and the ledger (§4) is empty | The owner/human relays after the undertaking's final review; the App manager records the return | Before any SQ answer can be recorded |
| SQ-01…SQ-32 answers (EC-01…EC-14) | SWBPIPE outside implementation owner (DEP-001) | Per CA §9 |
| OI-021 operation, check, autonomy, environment, surface variant (DI-1…DI-3; EC-12) | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution |
| D6 App-side holds: SQ-02 for host-operation checkpoints, plus a separate owner follow-up for App-only checkpoints (EXEC U-E23) | Owner | Before App-side checkpoint enforcement is claimed |
| **OUT-003 completion**, which cannot happen here: it needs DEL-02-02 registration (later, D1), the App candidate (later construction), the host candidate and evidence (SQ-27, DEP-09-06-019), actual acts (DEP-09-06-024), and DEL-09-01 protocol (outside D1) | DEL-09-06 integration owner, with the named suppliers | ST-5 (CA §6) |
| Reusable workflow authoring and review (OUT-002 artifact) | Workflow maker with DEL-02-02 (later) under `create-workflow` | Before W14-01 |
| U-E4 (with the V-GR1 cost); U-03; OI-003 (DI-8); OI-013/014 | As in CA UNRESOLVED | As there |
| `HANDOFF_SWBPIPE_DOMAINS.md` pointer (proposed coordination-file change; not a SoW or register change; outside this node's write scope). (a) Add a line saying the consolidated question set is DEL-09-06 `Design/RELAY_QUESTIONS_SWBPIPE.md`, to be relayed together with the HANDOFF after the final review. (b) In the "Autonomy and human acts" row, replace "how human approval/Checked/reliance differ" with the canonical terms: marking checked (A4), engineering approval (A6), professional reliance (A7). (c) The "Current App v4 standing" bullet still says the 30% package review is pending; DAG-001 was accepted and the 30% gate completed (`_DAG/DAG-001/ACCEPTANCE_RECORD.md`) | App manager / HELP_HUMAN | Before the relay. Grounds: CA F-8; RELAY UNRESOLVED "Closeout pointer"; R-4 |
| Application of S9-6-1…4 and R9-6-1…7 | Successor undertaking. R9-6-1…3 need DAG-002 | Before DAG-002 or the next SoW revision |

**Design residuals** (not applied):
- **D9-6-1.** In CA §5 and §11.1, the standing cells still read "v0.4 draft
  (v0.5 in the R5 pass)", "EXEC-v0.2 (working tree)" and "ADAPTER-v0.2 (working
  tree)". The candidate carries v0.5/v0.3. CA F-17 anticipates this re-point.
- **D9-6-2.** The RELAY §4 ledger "Prepared" row says "revised to RELAY-v0.3 in
  sweep A1 (R4; DECISION-2)". Sweep A1 produced v0.2; v0.3 is the R5 pass.
  Correct this before the relay.

### 6. Lifecycle observation

`_STATUS.md` reads **INITIALIZED**. CA-v0.1…v0.3 and RELAY-v0.1…v0.3 were
produced under D1, so **IN_PROGRESS** would be truthful. CHECKING is not
warranted, because every output remains partial and OUT-003 cannot complete in
this undertaking. Not changed here.

---

## DEL-09-09 — External control and catalog-extension trace

### 1. Commitment → result

XT = XT-v0.3.

| SoW item | Developed in | Standing | Remaining |
|---|---|---|---|
| OUT-001 V4-EXM-25 suite **and** candidate-bound evidence | §2 IN-01…IN-29, §3.1 J-1…J-8, §3.2 XC-00…XC-12, §3.3 completion rule and SQ-28 gate, §3.4 result record, §6 | **Partial.** The suite is defined; no evidence exists | wit: identified candidates, the engineer's actual A5 (DEP-09-09-016), host inputs (SQ-01/02/07/08/09/12/28 …), A13 (DEP-09-09-015). SQ-28 gates every live case |
| OUT-002 V4-EXM-24 one-operation three-channel trace document | §4 (V-ED1 fixture, TS-0…TS-5, CMP-01…15, TR-01…10, §4.5) | **Partial.** Plan and categories only | input: the one new operation (SQ-26, IN-11); wit: the trace on a candidate |
| OUT-003 generated/adapted-work account and extension disposition | §5.1 structure, §5.2 OI-003 record (recorded, never performed), §5.3 links | **Partial.** Structure only | wit: the populated account after the trace. input: OI-003 ruling (IN-12) |
| REQ-001 candidate and input binding | §2, §8 | Developed | input |
| REQ-002 enablement and the same route/policy | XC-01, XC-10, XC-12; S-1, S-2, S-11 | Developed | input: SQ-28; TBD-007 of DEL-03-03 |
| REQ-003 completed joined witness | §3.1, XC-02, §3.3 | Developed (the rule) | wit |
| REQ-004 stale, retarget, duplicate, interruption, unknown | XC-03…XC-08 | Developed | wit |
| REQ-005 one new operation across three surfaces | §4 | Developed (plan) | input/wit |
| REQ-006 original promise and OI-003 disposition | §5.2 | Developed | input: OI-003 |
| REQ-007 act distinctions | XC-09 (positive and negatives), S-6 | Developed | wit |
| REQ-008 evidence standing | §3.4, §6 | Developed | input: DEL-09-01 protocol (outside D1) |
| REQ-009 excluded acts | §7 | Developed | — |

### 2. Result → commitment

| Design element | Authority | Assessment |
|---|---|---|
| S-9 model destination; XC-01/XC-02 destination recorded per turn and never gating | DECISION-2 D5; R4-1, R5-4 | Supported. D5 is not in the SoW (S9-9-5) |
| S-10 four hold-support values; XC-10 hold parts (XF-25/26/42) | DECISION-2 D6; R4-2, R4-8, R5-1, R5-2, R5-10 | Supported. D6 is not in the SoW (S9-9-5). V4-EXM-25 itself declares no checkpoint (F-10) |
| S-11 A13 only through the host enablement facility; §3.3 SQ-28 gate | R4-13, R4-16, R5-10; ACT §2.6 | Supported. It should be reflected in DEP-09-09-014/015 (R9-9-5/6) |
| IN-22 embedded surface via DEL-05-01 LOOP; IN-29 grant states via DEL-04-02; IN-25 hold support and TS-0 compatibility reports via DEL-02-03 | XT F-2 (carried to C1 by R4) | **Outside CLM-002 and the register.** See S9-9-4 and R9-9-1…3 |
| Use of the DEL-09-06 relay file and the CA §7.2 ladder (§0, §2, §7) | CLM-004 names the App manager for the handoff; OUT-004 of DEL-09-06 owns the question file | Supported as a coordination route (S9-9-5); no arc (§4) |
| V-ED1 fixture; L-XT-2/3 = ADAPTER L-ADAPTER-11/12 | R4-20 | Supported |

### 3. Proposed SoW corrections (`ScopeOfWork.md`, DEL-09-09)

| # | Locus | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| S9-9-1 | TBD-002 | "OI-001, Reserved human acts, remains OPEN with **Owner with App/SWB contract owners**, … OI-002, Classifier routine permissions, remains OPEN with the same owner, …" | "OI-001 and OI-002 are ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (five reserved acts) and D3 (App: the user's Codex setting; hosts: no classifier mode). App DEL-04-01 carries the adopted decision. Operation-specific additions remain under OI-021 (TBD-003), and host adoption under DEP-001. This examination selects no reserved list or classifier mode." | DECISION-1; XT F-1 (v0.1); R4 "Carried to C1" |
| S9-9-2 | REQ-003 | "Preserve the original inspected workspace identity, generation, model revision and canonical content hash through the chain, …" | "…workspace identity, generation, model revision and canonical content identity with its identity method designation (DEL-03-01 read basis; the algorithm stays unselected) through the chain, …" This is a lift; ownership goes to the owning decision if contested | R1 R-6; the brief's "canonical content hash" item; XT J-2 |
| S9-9-3 | REQ-004 | "…submitting the same proposal twice has one domain effect." | "…submitting the same proposal twice has one domain effect. That is a host obligation to be evidenced from domain evidence (DEP-001); where the effect is unobserved, the record states 'one effect unevidenced'." (Aligns REQ-004 with AC-004 and VER-004) | R1 R-7; XT F-6; XC-05 |
| S9-9-4 | CLM-002; REQ-009 | CLM-002 lists DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-01, DEL-04-03 and DEL-09-01 | Add: "`DEL-05-01` owns the App/shared embedded-loop receiving contribution used for the embedded surface of the three-channel trace; `DEL-04-02` owns grant display states; `DEL-02-03` owns the per-surface compatibility report and hold-support values." Add the matching REQ-009 exclusions | XT F-2; IN-22, IN-25, IN-29; TS-0. Pairs with R9-9-1…3 |
| S9-9-5 | New TBD-005; CLM-004 | CLM-004 "The App manager owns the handoff/dependency account and the human relays files …" | TBD-005: "`APP-V4-FIRST-INCREMENT-20260928-DECISION-2`. D5 is settled: the App does not gate by model destination; the destination is recorded per turn and shown. D6 is deferred to SWBPIPE SQ-02 for checkpoints on host operations (this affects only XC-10's checkpoint parts). Every live external case also needs the host's A13 enablement facility with a capture-evidence reference (SQ-28, a DEP-001 input)." In CLM-004 add: "The consolidated question set is DEL-09-06 `Design/RELAY_QUESTIONS_SWBPIPE.md`, which is prepared and not delivered." | DECISION-2; R5-10; XT S-9, S-10, S-11, §3.3; F-9, F-10 |

R-4 wording check: "checking" in CLM-003, REQ-007 and AC-007 names the
person's act, and "non-mutating checks" (REQ-005) names host checks. Both uses
are consistent, so no change is proposed.

### 4. Proposed register changes (DEL-09-09)

| # | Change | Kind | Grounds |
|---|---|---|---|
| R9-9-1 | UPSTREAM PREREQUISITE row to **DEL-05-01** (embedded-surface receiving for the V4-EXM-24 trace; CMP-03 validation order) | **New arc** DEL-09-09 → DEL-05-01 (inside SCC-002) | XT F-2; IN-22 ("Not registered") |
| R9-9-2 | UPSTREAM PREREQUISITE row to **DEL-04-02** (grant display and states) | **New arc** DEL-09-09 → DEL-04-02 (inside SCC-002) | XT F-2; IN-29 ("not registered"); CMP-07; XC-10 |
| R9-9-3 | UPSTREAM PREREQUISITE row to **DEL-02-03** (compatibility report per surface and hold-support values) | **New arc** DEL-09-09 → DEL-02-03 (inside SCC-002) | XT F-2; IN-25; TS-0 (EXEC EV-5, CR-7) |
| R9-9-4 | DOWNSTREAM HANDOVER row to **DEL-03-01**, mirroring DEP-03-01-030 (trace and generated/adapted-work account before any extension claim) | **Mirror only** | XT Receivers, §5.3; CASE-002 M4-X. The CASE-002 R-02 limited alternative is unaffected |
| R9-9-5 | DEP-09-09-014: Statement adds the capture-evidence reference for acts (SQ-01), constraint handling (SQ-02), and the A13 enablement facility with its capture-evidence reference (SQ-28). Notes: "questions carried by DEL-09-06 RELAY-v0.3 (coordination route; prepared, not delivered)" | **Mirror only** (row edit) | XT §2, §3.3; R5-10 |
| R9-9-6 | DEP-09-09-015: Statement "…enable access … through the host's enablement facility, captured with a capture-evidence reference; App-side configuration is never A13 evidence" | **Mirror only** (row edit) | R4-13; ACT §2.6; XT S-11 |
| — | Considered, **not proposed**: **DEL-09-09 → DEL-09-06**. XT uses the relay file and the CA §7.2 ladder, but its real inputs are the SWBPIPE answers (DEP-001, DEP-09-09-014). Adding this arc would **pull DEL-09-06 into SCC-002** (14 members) through DEL-09-06 → DEL-05-01. R9-9-5 records the route instead. Also not proposed: DEL-09-09 → DEL-05-02 (PANEL is no longer an XT input at v0.3; IN-23 is the SWBPIPE owner's) and DEL-09-09 → DEL-01-01 (alignment only) | — | Tarjan check over DAG-001 plus the proposals |

Counted: mirror-only 3 (R9-9-4…6); new arc 3. No OI-001/OI-002 rows are
needed: policy is consumed through DEP-09-09-010.

### 5. Open items

| Item | Owner | Point of need |
|---|---|---|
| OI-003 retain / narrow / defer (IN-12) | Owner with host contract owner | Before claiming extension capability or fixing its criterion |
| OI-021 operation, autonomy, environment (IN-10) | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and live examination |
| OI-005 additional essential hosts (IN-13) | Owner | Before freezing wider examination scope |
| DEL-03-03 TBD-007 MCP versus CLI and realization family | App external-host integration owner with the external host owner | Before App receiving implementation and qualification |
| DEP-001 host inputs IN-02, IN-09, IN-11, IN-14…IN-20, IN-23, IN-24, IN-26…IN-28; SQ-28 gates every live XC case | SWBPIPE owner, via the human | Before corresponding examination |
| Actual acts: A13 (DEP-09-09-015); the engineer's A5 (DEP-09-09-016) | The person | At live execution |
| D6 for XC-10 checkpoint parts | Owner, on SQ-02 | Before XC-10 checkpoint parts |
| DEL-09-01 protocol (IN-03; outside D1); App candidate IN-01 (later construction) | Their owners | Before candidate-bound results |
| Application of S9-9-1…5 and R9-9-1…6 | Successor undertaking. R9-9-1…3 need DAG-002 | Before DAG-002 or the next SoW revision |

**Design residuals** (not applied):
- **D9-9-1.** §0 and UNRESOLVED cite "TBD-007" without a deliverable. It is
  DEL-03-03's TBD-007 and should be qualified.
- **D9-9-2.** F-15 (XF-42 state) and F-16 (V-ED1 branching) are resolved at the
  candidate: ADAPTER-v0.3 states XF-42 as DESIGNED, and C-v0.5 §10.4 states
  that V-ED1 replays T1–T15 on e1 and publishes e2 before T16. Both findings
  can close.

### 6. Lifecycle observation

`_STATUS.md` reads **INITIALIZED**. XT-v0.1…v0.3 production work under D1 has
occurred and warranted open scope remains, so **IN_PROGRESS** would be
truthful. CHECKING is not warranted, because every output is partial and the
witnesses are unrun. Not changed here.

---

## Proposed new arcs (consumer → supplier) — all need `project-dag` departure (DAG-002)

| # | Arc | Grounds | SCC effect |
|---|---|---|---|
| 1 | DEL-05-01 → DEL-04-02 | LOOP O-6, §6.2, §10.1 "Register gap (C1)"; V1-A RF-05; V1-C RF-5; X-16; AS U-15 | None (inside SCC-002) |
| 2 | DEL-05-02 → DEL-04-02 | PANEL §3.6, F-3; V1-C RF-4; V1-A RF-05; X-16; AS U-15 | None (inside SCC-002) |
| 3 | DEL-05-02 → DEL-02-03 | PANEL §3.2 (R5-1 values owned by EXEC §3.6), §3.5 (EXEC §4.7–§4.11; R4-3…R4-7). The alternative "via DEL-05-01" needs no arc | None (inside SCC-002) |
| 4 | DEL-09-06 → DEL-02-01 | CA §3.1 WR-1…WR-11, §4; CA F-2; resolves PKG-02 row DEP-09-06-012 | None |
| 5 | DEL-09-06 → DEL-02-02 | CA F-1; W14-01/W14-09 registration (DEL-02-02 later, D1) | None |
| 6 | DEL-09-06 → DEL-03-01 | CA §2.3 (C §5, §6, §10); CA F-2; resolves PKG-03 row DEP-09-06-014 | None |
| 7 | DEL-09-06 → DEL-03-02 | CA CA-2, CA-4, CA-5 (P §3–§9); CA F-2 | None |
| 8 | DEL-09-06 → DEL-03-03 | CA §2.2 CA/X; CA-0/1/2/5 (ADAPTER); CA F-2 | None |
| 9 | DEL-09-06 → DEL-04-01 | CA S-8, CA-2 (ACT §5.3, §6), CA-H (ACT §2, §4); SoW REQ-004; CA F-2 | None |
| 10 | DEL-09-06 → DEL-04-02 | CA-0 (AS §3), CA-H (AS §4), CA-R (AS §8, §9); CA F-2 | None |
| 11 | DEL-09-06 → DEL-01-01 | CA §4 "supplied" link, W14-08 (HOSTING §8.2/§8.3); CA F-2 | None |
| 12 | DEL-09-09 → DEL-05-01 | XT IN-22, CMP-03; XT F-2 | None (inside SCC-002) |
| 13 | DEL-09-09 → DEL-04-02 | XT IN-29, CMP-07, XC-10; XT F-2 | None (inside SCC-002) |
| 14 | DEL-09-09 → DEL-02-03 | XT IN-25, TS-0; XT F-2 | None (inside SCC-002) |

Considered and not proposed:
- DEL-09-09 → DEL-09-06. It would enlarge SCC-002 to include DEL-09-06, so it
  is routed as a note (R9-9-5).
- DEL-09-06 → DEL-09-09; DEL-09-06 → DEL-03-04; DEL-09-09 → DEL-05-02;
  DEL-09-09 → DEL-01-01; DEL-05-0x → DEL-01-01. These are coordination or
  alignment relationships, not consumed inputs.

## Checks performed on this return

- Each counterpart row ID cited was read from the candidate registers:
  - DEP-01-05-014;
  - DEP-02-01-020/-021;
  - DEP-02-03-014;
  - DEP-03-01-030;
  - DEP-03-02-022;
  - DEP-03-03-012;
  - DEP-03-04-014/-015;
  - DEP-08-01-008;
  - DEP-09-01-024/-026;
  - DEP-09-07-011;
  - DEP-10-03-015/-016.
- "New arc" and "mirror only" were each classified against the DAG-001 arc set
  at the candidate.
- R5 sibling elements were confirmed present at the candidate:
  - P-v0.5 §3.3 host-held;
  - C-v0.5 V-GR1 and V-ED1 branching;
  - EXEC-v0.3 §3.6 four values;
  - ADAPTER-v0.3 XF-42 DESIGNED.
- Git operations were read-only. The only write is this file. No SoW,
  register, status, context, reference, HANDOFF or Design file was changed. No
  proposal here is applied.
