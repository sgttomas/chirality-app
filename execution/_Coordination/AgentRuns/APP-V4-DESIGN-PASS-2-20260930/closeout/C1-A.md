# C1-A — bounded closeout: DEL-04-01, DEL-04-02, DEL-04-03, DEL-02-01, DEL-02-03

- Node C1-A of run `APP-V4-DESIGN-PASS-2-20260930`. Executor: Type 2 TASK
  (Claude Code subagent, Claude Opus 5.5; does not delegate), dispatched by
  HELP_HUMAN.
- Method: `chirality-root:bundled:workflow:bounded-reconciliation`
  (`workflows/bounded-reconciliation/WORKFLOW.md`, sha256 `c7798c0a…0f11bc`,
  read whole), applied read-only under [BRIEFS.md](../BRIEFS.md) "Common
  rules" and "C1 — bounded closeout" (BRIEFS sha256 `84314222…ad2b8e`).
  Owner direction: [OWNER_DECISIONS.md](../OWNER_DECISIONS.md) (sha256
  `b2fa8187…e05b`). Precedent: the first increment's
  `closeout/C1-A.md` and `CLOSEOUT_ACCOUNT.md`.
- **Candidate:** commit `a9046631c0`. While this node ran, HEAD moved to
  `41899194c4` (C0 committed; PR-2 merged). `git diff a9046631c0 41899194c4`
  touches only HOSTING, GUIDE, LOOP and run records, and
  `git diff a9046631c0` over PKG-02 and PKG-04 is empty, so every input below
  is byte-identical at the candidate and in the working tree.
- **Boundary (binding).** No ScopeOfWork.md, Dependencies.csv,
  `_DEPENDENCIES.md`, `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md` or Design
  file was edited. Every warranted change below is a **proposal** for a later
  amendment and `dependency-extract` run. This is the only file written.
- Rulings read as binding: R1–R15, DECISION-K1 (K1-1…K1-6), the
  executor-model, model-download, host-loop interface and OBS directions, and
  the predecessor runs' owner decisions (DECISION-1…DECISION-7 of their runs
  as cited by the Design files).
- Proposal sources searched: `SURVEY/S1-A`, `S1-C`, `S1-F`; `WAVE_A/*`;
  `WAVE_B/*`; `comparisons/V18-1…4`; `reviews/V17-A/B`, `V17b`, `V19-A/B`,
  `V19b`; `DECISIONS_DRAFT.md`, `DECISIONS_PENDING.md`; R9–R15; and, for arc
  history, `APP-V4-BASIS-ALIGN-20260928/DAG_PREP/ARC_ANALYSIS.md`.

## Inputs (sha256 at the candidate)

| DEL | ScopeOfWork.md | Dependencies.csv | `_DEPENDENCIES.md` | `_STATUS.md` | Design file(s) |
|---|---|---|---|---|---|
| DEL-04-01 | `ac043e54…b875` | `d3892649…c9c1` | `b504a28b…e2db6` | `4cd05ed5…b034` | ACT-POLICY-v0.8 `3333a69d…49c9` |
| DEL-04-02 | `f16ffa8a…4560` | `05ffc9c7…cb44` | `273ce824…689f` | `b429eebf…c609` | AS-v0.8 `f1618105…3ba0` |
| DEL-04-03 | `ceecddbb…aa47` | `f40bc888…70cf` | `d1235d02…1c64` | `5bb717f9…3dfb` | RS-v0.8 `1da4ad11…1d01` |
| DEL-02-01 | `ef360edf…2f17` | `d3946a9e…b10a` | `983396d0…f4dc` | `9e05735e…e7cb` | WD-v0.8 `d6ceac20…5380`; WD-EX-v0.8 `046a44fe…c57a` |
| DEL-02-03 | `0006521b…726d` | `f1a81f85…0f7e` | `84dd2315…d422` | `237e0982…9b86` | EXEC-v0.6 `4d55f0e8…1d2f` |

Each Design header's ScopeOfWork pin equals the current ScopeOfWork bytes
(checked by grepping each full SoW hash in the Design files). The registers
of DEL-02-01, DEL-02-03, DEL-03-02 and DEL-03-03 equal DAG-003's
`SourceRegisterSHA256` (V18-4 §1; D0 found both DAG-003 manifests passing).
The schemas, examples and `prototype/` folders beside each Design file were
read where a claim depended on them, and the five prototypes were rerun
(see "Checks").

## Reading conventions

- **Status** of a commitment at the 60% definition level: *developed* (the
  definable content is present), *partial* (a definition element is still
  missing; named), *named only*, *absent*. AC and VER items take the status
  of the requirement they verify, because their designed cases exist in every
  file; that no case has run against a candidate is stated separately and
  does not lower the status (implementation, a candidate, a person's act or a
  host input is needed for that).
- **Registers follow the ScopeOfWork.** Every `_DEPENDENCIES.md` Run Notes
  says the rows were extracted from `ScopeOfWork.md` only, CONSERVATIVE, and
  that ownership lists alone create no edges. A missing row therefore usually
  needs a SoW sentence first; the register proposals below name the SoW item
  they follow from.
- **Arc classes** (DAG-003 `GRAPH_BASIS.md`; consumer → supplier): *mirror
  only* (the arc already exists through some row), *new arc* (no row in
  either direction; a `project-dag` departure), *non-topological* (EXTERNAL
  target, statement or field update). SCC-002 members: DEL-01-04, 02-01,
  02-02, 02-03, 02-04, 03-01, 03-02, 03-03, 04-02, 04-03, 05-01, 05-02,
  09-09 (`HANDOFF_STATE.md`). DEL-04-01 is outside SCC-002 and, by the
  standing guard, gains no supplier row from an SCC-002 member.
- Proposal IDs are new (`SC2-…`, `R2-…`) so that they do not collide with the
  first increment's `SC-…`/`R-…`; row IDs are assigned on application.

---

## Summary

| DEL | Commitments (OUT+REQ+AC+VER) | Developed / partial / named / absent | Main reason for partial | Proposed SoW / register items | Lifecycle |
|---|---|---|---|---|---|
| DEL-04-01 | 28 | 22 / 6 / 0 / 0 | Consequence dimension unassigned (U-02); policy-record placement (OI-013/014) | 4 / 3 | IN_PROGRESS, truthful |
| DEL-04-02 | 24 | 24 / 0 / 0 / 0 | — (components defined; placement open by design, OI-014) | 1 / 3 | IN_PROGRESS, truthful |
| DEL-04-03 | 23 | 22 / 1 / 0 / 0 | OUT-001: identity algorithm, carriage manifest, record location (U-04, U-05) | 3 / 8 | IN_PROGRESS, truthful |
| DEL-02-01 | 24 | 21 / 3 / 0 / 0 | REQ-004 (and its AC/VER): revision algorithm open (U-03) | 2 / 8 | IN_PROGRESS, truthful |
| DEL-02-03 | 24 | 20 / 4 / 0 / 0 | OUT-001/REQ-001 (and AC/VER-001): harness-capability presence rule inactive (EV-3; U-E10) | 6 / 10 | IN_PROGRESS, truthful |
| DEL-01-04 (collected, K1-4) | — | — | — | 1 / 1 | not compared |

Totals: **17 ScopeOfWork items** (16 in these five deliverables, 1 for
DEL-01-04), **33 register items** (24 mirror-only rows, **1 new arc**, 8
non-topological), **0 basis items**. Three findings go back to the graph as
Design work, not as proposals (§ "Returned to the graph").

Against the first increment's C1-A (OUT developed/partial 2/1, 3/0, 3/1,
3/1, 2/1): DEL-04-03 OUT-001 is now a PROPOSED format with a schema;
DEL-02-01 OUT-002 now has a PROPOSED carriage and schema; DEL-02-03 OUT-001's
App hold gap closed with D6 for the current phase, and the remaining
partial is the harness-capability presence rule.

---

## DEL-04-01 — Operation-policy and human-act distinctions (ACT-POLICY-v0.8)

### 1. Commitment → result

| Item | Where ACT answers | Status | Still missing (definition) |
|---|---|---|---|
| OUT-001 contract | §1–§7, §9, §11; new §2.8 act-record lifecycle; new §4.7 request → capture → record | developed | — |
| OUT-002 policy-class representation and decision→consumer map | §8.1 with PROPOSED `ACT_POLICY_CLASS_RECORD.schema.json`, P-01…P-06 as instances (VC-012); §8.2–§8.4; §8.5 PROPOSED consequence draft; §10.1–§10.3 | **partial** | Consequence values assigned to no record (U-02, owner's phase review); placement (U-12; OI-013/014); operation-specific additions (U-01, OI-021) |
| OUT-003 fixtures | §13 FX-01…FX-57; VC-001…VC-012 | developed (designed) | — |
| REQ-001 | §4 (§4.0 AP-1…AP-12), §5.3–§5.6 | **partial** | The scope's consequence dimension is a slot (§5.4; U-02) |
| REQ-002 | §2.1–§2.8 (A1–A15), §3, §4.7 | developed | — |
| REQ-003 | §3 S4, §9, FX-03/05/14/15 | developed | — |
| REQ-004 | §8.3–§8.4, §5.3 rule 5, §2.6 | developed (OI-021 held, as REQ-004 itself requires) | — |
| REQ-005 | §9, FX-11…13, FX-34 | developed | — |
| REQ-006 | §7, §5.6 W-a…W-j, P-03 | developed | — |
| REQ-007 | §11 | developed | — |
| AC-001…AC-009 / VER-001…VER-009 | VC-001…VC-012 (Verification cases) | AC/VER-001 and AC/VER-007 **partial** (with REQ-001 / OUT-002); the other 14 developed (designed) | as above |

Run state: no case has run against a candidate. FX-57/VC-012 ran on the
local prototype (rerun here: "RESULT: all expectations held"). Positive act
cases need a recorded person grant and a performed act (U-05;
DEP-04-01-020/-021). Host enforcement evidence is DEP-001's.

### 2. Result → commitment (structures added in this run)

| Element | Authority | Supported by the ScopeOfWork? |
|---|---|---|
| Policy-class record schema and instances (§8.1, §8.3) | PROPOSED (R12-1, R12-2) | Yes: OUT-002, AC-007 |
| §2.8 lifecycle table; §4.7 sequence | PROPOSED over SETTLED rules | Yes: OUT-001, REQ-002 |
| §8.5 consequence vocabulary draft | PROPOSED; assigns nothing | Yes: OUT-002 "operation classes and consequences"; its open status has no TBD (SC2-04-01-3) |
| A15 register workflow revision (§2.1) | R12-5 (INTEGRATION; source DEL-02-02 AC-006) | Generally (REQ-002's distinct-act duty); not named (SC2-04-01-4, optional) |
| §2.7 network-destination grant as A12 subclass, V-28 | DECISION-5 (person-only, SETTLED); A12 mapping INTEGRATION (F-22; DECISIONS_PENDING Part 3) | **No anchor**: AC-007 admits values "beyond … DECISION-1" only through VER-007's "labeled … INTEGRATION extensions" (S1-A §1.2 lag 4) — SC2-04-01-2, conditional |
| AP-12 (the agent asks; K1-1), §4.5 earlier act counts (K1-2), §4.3 joint answer (K1-3) | DECISION-K1 | Yes: CLM-004 ("an agent may prepare or request them"), REQ-001's checkpoint override, TBD-004 |

Unsupported additions: none found.

### 3. What the 60% description still lacks

- **Data:** consequence values (U-02); concrete placement of the policy
  configuration (U-12); the first connected operation and its reserved
  additions (OI-021). The §8.3 text ↔ instance comparison is by reading, not
  scripted (VC-012).
- **Interfaces:** receivers are tabled by register row (§10.3) with values
  per consumer (§10.1); failure on a missing value is §5.3 rule 5 (never a
  permission). No per-receiver condition/failure table like AS §12.1; in my
  reading adequate at this level.
- **Verification:** candidate runs; a recorded grant and performed acts.
- **Host:** capture-evidence reference, enforcement of P-01…P-06 (U-04;
  SWBPIPE answered "none"; host joins deferred, DECISION-3).

### 4. Register observations

- Nine consumers declare DEL-04-01 upstream with no local DOWNSTREAM row:
  DEL-09-06 (DEP-09-06-030) and eight outside this undertaking (DEL-01-02,
  01-04, 02-02, 06-02, 09-02, 09-05, 09-12, 10-03) — ACT F-1; A1-A §4 item 2.
  Proposed for DEL-09-06 only (SC2-04-01-1 → R2-04-01-a).
- DEP-03-03-008 (TBD) vs DEP-04-01-023 (INITIALIZED): mirror maturity
  difference, carried in DAG-003 `HANDOFF_STATE.md` (A1-A §4 item 4); a
  DEL-03-03 register matter (C1-B).
- DEL-01-01's use of V-21/V-25 has no row (A1-A §4 item 3): **not
  proposed**, as ARC_ANALYSIS K-12 already decided (D3 reaches DEL-01-01
  through DECISION-1; DEP-01-01-021/-022/-024 suffice).
- WD §8's "DEL-04-01 policy" receiver row (A1-C §4 item 4) and ACT's
  citations of LOOP §5.3 and DEL-02-02 AC-006: **not proposed** as arcs
  (ARC_ANALYSIS K-1, K-2; the guard that DEL-04-01 gains no supplier row from
  an SCC-002 member; K-2 would enlarge SCC-002 to 16). WD-v0.8 §8 already
  labels its row a cross-check with no register row.

### 5. Lifecycle

IN_PROGRESS since 2026-09-28 (owner DECISION-6, relayed). Truthful; no change
observed as warranted.

---

## DEL-04-02 — Visible autonomy and result standing (AS-v0.8)

### 1. Commitment → result

| Item | Where AS answers | Status | Still missing (definition) |
|---|---|---|---|
| OUT-001 components (CODE) | §3–§9 behaviour; §13 components K-1…K-7 with PROPOSED options CS-1…CS-4, none chosen | developed (definition) | Construction and allocation wait for OI-014 (TBD-004), by design |
| OUT-002 contract (DOC) | §2, §6, §7, §10, §12, §12.1, UNRESOLVED | developed | — |
| OUT-003 fixtures (TEST) | §11 F1–F23; VC-01…VC-23 | developed (designed) | — |
| REQ-001 | §3, §3.1 (DG-1…DG-15), §4, §5 | developed | — |
| REQ-002 | §6 (= RS §8) with PROPOSED `AS_SETTINGS_IN.schema.json`, incl. destination settings | developed | — |
| REQ-003 | §7 | developed | Host elements fixture-only (U-05; DEP-001) |
| REQ-004 | §8 | developed | — |
| REQ-005 | §9 | developed | — |
| REQ-006 | §0, §10, §13, UNRESOLVED | developed | — |
| REQ-007 | §10 (incl. §3.2 display ownership) | developed | — |
| AC-001…AC-007 / VER-001…VER-007 | VC-01…VC-23 | developed (designed) | — |

Run state: VC-19 (state walk) and VC-22 (schema) ran on the prototype (rerun
here: "RESULT: all expectations held"); none on a candidate.

### 2. Result → commitment

| Element | Authority | Supported? |
|---|---|---|
| §3.2 display of destinations contacted | DERIVED (CLM-002; DEP-04-02-018), node B5 | Yes: CLM-002 consumes the contacted-destination record "which DECISION-5 requires to be shown" |
| §3.1 in-work grant transitions; §6 destination settings in settings-in | PROPOSED over SETTLED rules (DECISION-5; K1-5) | Yes: CLM-002 (allow list, in-work grants) |
| §12.1 provided to receivers (grant in force per dispatch) | PROPOSED | Yes: CLM-002 receivers; DEP-05-01-025 |
| §13 component options | PROPOSED; none chosen (R12-2) | Yes: OUT-001 "where justified by agreed allocation"; TBD-004 |
| Declines and refusals "recording PROPOSED" (§3, §3.1, §3.2) | R12-10 | See finding G-1: DEL-04-03's accepted SoW names "destination declined" |

Unsupported additions: none found.

### 3. What the 60% description still lacks

- Placement of K-1…K-7 (OI-014; CS-1…CS-4 unchosen).
- Host control/origin/undo/receipt elements are fixture-only (U-04…U-07).
- Two PROPOSED receiver behaviours not yet taken up on the other side: the
  wording "grant state not available", and the EXEC reading that an
  *unconfirmed* earlier A12 is not "still in force" (§12.1 DEL-02-03 row;
  EXEC §9.1 still cites AS-v0.7; G-3).
- U-20 (host without a grant model) PROPOSED, deferred with the host joins.

### 4. Register observations

- DEL-03-04 (DEP-03-04-012), DEL-09-06 (DEP-09-06-031) and DEL-09-09
  (DEP-09-09-022) declare DEL-04-02 upstream; no local mirror (A1-A §4
  item 5; AS §12). SoW CLM-002 names five receivers only (SC2-04-02-1).
- DEL-03-02, DEL-03-03 and DEL-02-03 have no UPSTREAM row for DEL-04-02; the
  arcs rest on DEP-04-02-021…023 alone (A1-A §4 item 5; V12 F6). DEL-02-03's
  is proposed here (SC2-02-03-3); DEL-03-02's and DEL-03-03's are C1-B's
  (A1-B §4 items 4, 6).
- DEP-04-02-018 statement names allow list, in-work grants and the
  contacted-destination record; the Design also consumes the destination
  request states (LOOP DF-6). The statement quotes CLM-002, which already
  covers the display; no change proposed.

### 5. Lifecycle

IN_PROGRESS since 2026-09-28. Truthful; no change.

---

## DEL-04-03 — Content-bound decisions and compact run records (RS-v0.8)

### 1. Commitment → result

| Item | Where RS answers | Status | Still missing (definition) |
|---|---|---|---|
| OUT-001 versioned format (CONFIG) and authority documentation | §2, §3, §4 R1–R16, §6, §7, §9; §13 PROPOSED format 0.1 with `RS_RECORD.schema.json`, five valid logs, 15 invalid entries; one container for EXEC's CE bodies (R14-1) | **partial** | Identity algorithms and carriage-manifest representation (U-04); App record location (U-05); a standard validator needs a loader rule for the relative `$ref` (§13 files row) |
| OUT-002 writer/reader and lapse handling (CODE) | §7 L-0…L-13; §14 writer W-0…W-3, reader R-1…R-8, FC-1…FC-9 | developed (definition) | Code; placement (U-16) |
| OUT-003 fixtures (TEST) | §12 E1–E13; VC-01…VC-39 | developed (designed) | — |
| OUT-004 interface documentation (DOC) | §10, §10.1, §11 | developed | §10.1 states that DEL-03-04's, DEL-09-02's, DEL-09-05's and DEL-10-03's consumption is "not yet stated here" (G-3) |
| REQ-001 | §2 | developed | — |
| REQ-002 | §4 R1–R16 (R5 destination per turn; R15 network destinations) | developed | — |
| REQ-003 | §6 (§6.1 actor with K1-4 identity), §5 | developed | — |
| REQ-004 | §7 | developed | — |
| REQ-005 | §10 | developed | — |
| REQ-006 | §11 | developed | — |
| AC-001…AC-007 / VER-001…VER-006 | VC-01…VC-39 | developed (designed) | — |

Run state: VC-31…VC-35 and VC-39 ran on the prototype (rerun here: 51 PASS,
0 FAIL; EXEC → RS 12/12 and 40/40 valid). FC-8, FC-9 not run. No candidate
writer or reader.

### 2. Result → commitment

| Element | Authority | Supported? |
|---|---|---|
| §13 format 0.1, changed in place (R13-4) | PROPOSED | Yes: OUT-001 leaves serialization and spellings to design |
| R16 act requests | PROPOSED representation (RS 5; K1-1; ACT AP-5) | Partly: REQ-002's inventory and CLM-004's list from DEL-02-03 do not name a request (SC2-04-03-2) |
| One record container referencing EXEC's CE bodies (R14-1) | INTEGRATION | Yes: CLM-004 (checkpoint events from DEL-02-03) |
| `workflowTuple` = WD's identity tuple; WD §4.3.4 spaced dispositions | R14-1; RX; V18-2 M-3 | **No supplier statement**: CLM-004 does not name DEL-02-01 as a supplier (ARC_ANALYSIS K-8: "No SoW grounding") — SC2-04-03-2 |
| A15 record kind (§6.1 HA-10) | R12-5 | Yes (REQ-003 generic); consumer DEL-02-02 outside |
| R15 destination requested / request closed / boundary refusal | PROPOSED (B5; R12-10) | Yes for R15 generally (REQ-002, CLM-002); see G-1 for "destination declined" |
| `run_opened.notStarted` (R15-1) | DERIVED | Yes: REQ-002 |
| App actor identity "identity not verified" (§6.1) | DECISION-K1 K1-4 | Not named (SC2-04-03-3) |

### 3. What the 60% description still lacks

U-04 identity algorithms and carriage manifest (with DEL-03-01 TBD-003 and
DEL-02-01 U-03); U-05 record location; U-16 reader/writer placement; FC-8,
FC-9 unrun; §10 rows for four registered consumers; the version step rule
takes effect only when a consumer relies on the format (R13-4). Host
evidence (receipts, capture reference, per-subject identity) none from
SWBPIPE (U-11, U-15, U-29).

### 4. Register observations

- **Package rows instead of deliverable rows:** DEP-04-03-011 (PKG-02) and
  -012 (PKG-03) stand where DEL-02-01 (DEP-02-01-019), DEL-02-03
  (DEP-02-03-013) and DEL-03-01 (DEP-03-01-031) declare deliverable-level
  UPSTREAM rows (first-increment R-04-03-d/e, not applied).
- **No local mirror** for DEL-03-04 (DEP-03-04-013) and, outside this
  undertaking, DEL-01-04, 02-02, 06-01/06-02 (package row -013), 09-02,
  09-05, 10-03.
- **New supplier relation, no row:** RS's schema now carries WD's identity
  tuple and WD's disposition spellings (R14-1; RX; V18-2 M-3). DAG-003 has no
  arc DEL-04-03 → DEL-02-01 (checked by script over both edge files);
  ARC_ANALYSIS K-8 held it back for want of SoW grounding. Both ends are in
  SCC-002, so the arc would be held and SCC-neutral.
- **DEP-04-03-025** ("checkpoint arrival, act and lapse events and
  compatibility reports") does not name the act request (R16).
- **Mirror maturity:** DEP-09-06-015 TBD vs DEP-04-03-031 INITIALIZED
  (`HANDOFF_STATE.md`; A1-A item 4; A1-E item 3; V18-4 n-4).
- **`_DEPENDENCIES.md` Run Notes label slip** (A1-A §4 item 7, re-verified):
  "the only DEL-09-06 row is DOWNSTREAM DEP-04-03-031 (DEL-09-06 consuming
  this record contract, N-08, …)". In ARC_ANALYSIS N-08 is DEL-09-06 →
  DEL-04-02; the DEL-04-03 arc is DEP-09-06-015's.

### 5. Lifecycle

IN_PROGRESS since 2026-09-28. Truthful; no change.

---

## DEL-02-01 — Portable workflow contract and shared allocation (WD-v0.8, WD-EX-v0.8)

### 1. Commitment → result

| Item | Where WD/WD-EX answer | Status | Still missing (definition) |
|---|---|---|---|
| OUT-001 contract | §2–§7 | developed | Host seat → role mapping (U-09; SWBPIPE has no seat concept) |
| OUT-002 schemas and examples | §3.5 PROPOSED carriage, §3.6 schema `workflow-declaration.schema.json`, §3.7 reading order, §4.1–§4.7; WD-EX E1–E9 | developed (PROPOSED) | Consumer confirmation of carriage and representation (U-01, U-02) |
| OUT-003 responsibility map | §9 A-1…A-12 | developed | Every Confirmation "None" (U-17), recorded as absence, as AC-005 asks |
| OUT-004 parser and consumer fixtures | §13 VC-01…VC-56; §13.1 | developed (designed) | Product parser; consumer runs |
| REQ-001 | §3.2, §5, §6 | developed | — |
| REQ-002 | §4.1–§4.5; §4.2.5 harness names (PROPOSED, pin 0.158.0) mapped to HOSTING §8.4 groups (HC-7) | developed | — |
| REQ-003 | §4.3 (incl. A6/A7: E1e, VC-53, VC-54) | developed | — |
| REQ-004 | §4.6, §6 (RV-1…RV-5) | **partial** | Revision algorithm and method designation (U-03) |
| REQ-005 | §9 | developed | — |
| REQ-006 | §10 (DEL-03-02 and DEL-03-03 rows now present) | developed | — |
| AC-001…AC-007 / VER-001…VER-007 | §13 VC-01…VC-56 | AC/VER-004 **partial**; the other 12 developed (designed) | as REQ-004 |

Run state: `wdproto.py selftest` 62/62 (rerun here); the prototype reads
declarations only. Run parts need EXEC's recorder or a LOOP double;
App-content act cases need DEL-01-04's control (AWAITING INPUT).

### 2. Result → commitment

| Element | Authority | Supported? |
|---|---|---|
| Carriage, schema, reading order, states, OS-1…OS-10 | PROPOSED (R12-1) | Yes: OUT-002, REQ-002 |
| §4.2.5 harness capability names | PROPOSED; R14-5 group mapping | Yes: REQ-002 ("supplied through DEL-01-01"); CLM-002's word "inventory" lags (SC2-02-01-1) |
| `fresh act required` (SP-6F take-up), `on subject absent`, output production OP-1…OP-6, `relies on` | PROPOSED (R12-10, U-32) | Yes: REQ-003, TBD-004 |
| `applied` outcome token (R14-6); N-18 contributions cited | DERIVED | Yes: CLM-002 consumption sentence (SCA-V4-002) |

Unsupported additions: none found.

### 3. What the 60% description still lacks

Consumer confirmation of U-01/U-02; the revision algorithm (U-03); the
presence rule for harness names (EXEC EV-3; see G-2); §9 owner confirmations
(U-17); seat mapping (U-09); the "evidence" that DEP-08-02-006 and
DEP-09-02-015 name (outside this increment; WD §8 says so).

### 4. Register observations

- **No supplier-side mirrors:** DEL-02-03 (DEP-02-03-009), DEL-03-02
  (DEP-03-02-027), DEL-03-04 (DEP-03-04-008), DEL-05-01 (DEP-05-01-016),
  DEL-05-02 (DEP-05-02-005), DEL-09-06 (DEP-09-06-025); outside: DEL-02-02,
  02-04, 08-02, 09-02, 10-03 (first-increment R-02-01-a…f not applied;
  HANDOFF "Deferred supplier-side mirror rows (P2 O-3)").
- **DEP-02-01-025** says "harness capability meaning supplied through
  DEL-01-01"; SoW CLM-002 says DEL-01-01 "supplies the harness capability
  inventory" (A1-D §4 item 5). WD now names the requirements and HOSTING
  §8.4 supplies group meanings and availability signals.
- **DEP-02-01-027** (DOWNSTREAM to DEL-03-03): RequiredMaturity and
  SatisfactionStatus TBD, where the other deliverable rows read INITIALIZED /
  PENDING; DEL-03-03 has no UPSTREAM mirror (A1-B §4 item 4; C1-B's
  register).

### 5. Lifecycle

IN_PROGRESS since 2026-09-28. Truthful; no change.

---

## DEL-02-03 — Workflow execution compatibility and round-trip support (EXEC-v0.6)

### 1. Commitment → result

| Item | Where EXEC answers | Status | Still missing (definition) |
|---|---|---|---|
| OUT-001 required-tool and checkpoint receiving behaviour (CODE) | §2.4 current-phase recorder (RC-1…RC-10, CE-1…CE-19, transition table, SD-1…SD-5); §2.5 App-run reached-when AW-1…AW-12, AE-1…AE-7; §2.6 SQ-A, SQ-T; §2.7 components; §3 with `compatibility-report.schema.json`; `checkpoint-record-entries.schema.json` | **partial** | EV-3 presence rule inactive (U-E10; G-2); MCP-path cells AW-1, AW-8 "OBS-1 pending" (U-E26) |
| OUT-002 transfer and adaptation contract | §6.1–§6.7 | developed | Carriage-manifest schema (TR-4; U-E16) |
| OUT-003 fixtures | §7 MT-1…MT-17, CH-1…CH-33, RT-1…RT-11; §7.4 | developed (designed) | — |
| REQ-001 | §3.1–§3.8 | **partial** | Harness-capability requirements stay *not established* (EV-3) |
| REQ-002 | §2.1, §2.4, §2.5, §4.12 | developed | MCP-path arrival order pending observation (a verification gap; the stated limit applies meanwhile) |
| REQ-003 | §4.5 SP-1…SP-8 (SP-6 per K1-2), §4.7 JA-1, §5 CAP-1…CAP-9 | developed | App control construction (DEL-01-04) |
| REQ-004 | §6.1–§6.4, §6.6, §6.7 | developed | Host links AWAITING INPUT (SQ-17…19: none) |
| REQ-005 | §6.5 HR-1…HR-7 | developed | Registration side DEL-02-02 (later) |
| REQ-006 | §10 (DEL-04-02 and DEL-01-01 rows now present) | developed | — |
| REQ-007 | §8, UNRESOLVED (TBD-001…TBD-006) | developed | — |
| AC-001…AC-007 / VER-001…VER-007 | VC-E-01…VC-E-16 | AC/VER-001 **partial**; the other 12 developed (designed) | as REQ-001 |

Run state: `run_all.py` "ALL CHECKS HOLD" (rerun here). CH-23 (ii), CH-31
(ii), CH-32 App-side positive capture AWAITING INPUT on DEL-01-04 (X-1).
VC-E-15 "OBS-1 pending".

### 2. Result → commitment

| Element | Authority | Supported? |
|---|---|---|
| Recorder; RC-4 "recording is not a reaction"; RC-6 means to act as a standing facility | PROPOSED; K1-1 SETTLED | Yes in substance, but REQ-002, AC-002, VER-002, the Purpose and the SOW-052 row still make the slice "request" the act (SC2-02-03-2) |
| SP-6 (earlier act counts), SP-6F option, JA-1 | DECISION-K1 K1-2, K1-3 | Yes; TBD-006 names neither (SC2-02-03-4) |
| CAP-8 person identity | DECISION-K1 K1-4 | CLM-002 still lists "person identity" as DEL-01-04's contribution (SC2-02-03-5) |
| §4.10 use of AS grant display states | R4-6; AS §12.1 | Ownership in CLM-002 only; no consumption sentence or row (SC2-02-03-3) |
| Two schemas; RS as container (R14-1) | PROPOSED; INTEGRATION | Yes: OUT-001, CLM-002 (DEL-04-03 owns the run-file meaning) |

Unsupported additions: none found.

### 3. What the 60% description still lacks

The harness-capability presence rule (G-2); the MCP-path observation
(U-E26; needs a route that offers MCP tools as functions, or a cloud turn —
an owner choice under K1-6); the App act control (DEL-01-04); carriage
manifest (U-E16); placement (U-E2; OI-013/014); the term "run owner"
(CE-17, AE-7) undefined (V19-A n-5, returned by RQ); EXEC §11.5 F-34 still
reads open although RS L-12 now states the value (V18-1 m-7, R14-1).

### 4. Register observations

- **No UPSTREAM row for DEL-04-02** (grant display states, EXEC §4.10); the
  arc rests on DEP-04-02-023 (A1-C §4 item 3; EXEC §9.1).
- **No supplier-side mirrors** for DEL-02-01 (DEP-02-01-026), DEL-03-03
  (DEP-03-03-014), DEL-03-04 (DEP-03-04-009), DEL-04-02 (DEP-04-02-017),
  DEL-04-03 (DEP-04-03-025), DEL-05-01 (DEP-05-01-017), DEL-05-02
  (DEP-05-02-020), DEL-09-09 (DEP-09-09-023); outside: DEL-02-02, 09-02,
  10-03. Only DEL-09-06 is mirrored (DEP-02-03-014).
- **DEP-02-03-027** (X-1) names "DEL-01-04's App act control and person
  identity"; K1-4 settled the identity scheme (CAP-8).
- DEL-01-01 receives EXEC's OBS list (§9.2) with no row; no row proposed
  (HOSTING §6.7 names EXEC as recorder; an observation list is not a
  consumed input).

### 5. Lifecycle

IN_PROGRESS since 2026-09-28. Truthful; no change.

---

## Proposed ScopeOfWork items (none applied)

Each amendment that applies these also adds its AX line naming the decision
records (DECISION-K1 of `APP-V4-DESIGN-PASS-2-20260930` where cited).

| ID | File, location | Old (excerpt) | New | Reason | Source |
|---|---|---|---|---|---|
| SC2-04-01-1 | DEL-04-01 CLM-002, last sentence | "…`DEL-05-01`, `DEL-05-02` and `DEL-09-09`, each of which declares it upstream in its own register." | "…`DEL-05-01`, `DEL-05-02`, `DEL-09-06` and `DEL-09-09`, each of which declares it upstream in its own register." | DEL-09-06 declares DEP-09-06-030; the first increment's R-04-01-g was not applied; enables R2-04-01-a | ACT F-1, §10.3; A1-A §4 item 2; S1-A §1.2 |
| SC2-04-01-2 | DEL-04-01 AC-007 and VER-007; new AX | AC-007: "…supplies no reserved list or classifier treatment beyond the adopted `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` rulings." | "…beyond the adopted `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` rulings and the person-only network-destination grant of `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`, carried as an A12 subclass." VER-007: add "and the DECISION-5 destination grant" after "D2/D3". **Conditional:** only if the owner confirms the A12 mapping at the phase review (DECISIONS_PENDING Part 3; OWNER_ITEMS O-15 deferred it) | ACT §2.7 and V-28 have no anchor in their own SoW | S1-A §1.2 lag 4; A1-A §4 item 1; ACT F-22; DECISIONS_PENDING Part 3 |
| SC2-04-01-3 | DEL-04-01 Axiology, new TBD-005 | — | "TBD-005 — The consequence dimension of operation classes (REQ-001, OUT-002) has no adopted vocabulary. A PROPOSED draft over the four dimensions of S/DECISION_BRIEF.html#d3 is prepared for the owner's phase review; until one is adopted no policy value assigns a consequence and the grant's consequence dimension stays a slot. **Owner:** the owner with the host policy owner. **Point of need:** before class assignment in DEL-03-01." | REQ-004/AC-007 require open values to be explicit with owner and point of need; U-02 has none in the SoW | B4 §7 item 2 (the U-02 part); ACT U-02, §8.5; DECISIONS_PENDING Part 3 |
| SC2-04-01-4 | DEL-04-01 REQ-002, after the first sentence (optional, traceability) | "…human marking checked, accepting an edit, engineering approval and professional reliance." | Append: "Registering a workflow revision is likewise a person's act with its own actor, subject (the revision) and evidence (App v4 `DEL-02-02` REQ-002, AC-006)." | A15 (R12-5) rests on a sibling SoW only | R12-5; DECISIONS_PENDING Part 2; S1-F §2.3 N-3 |
| SC2-04-02-1 | DEL-04-02 CLM-002, receivers sentence | "Its visible autonomy state is received by `DEL-05-01`, `DEL-05-02`, `DEL-03-02`, `DEL-03-03` and `DEL-02-03`." | Append: "`DEL-03-04`, `DEL-09-06` and `DEL-09-09` also declare it upstream in their own registers." | Enables R2-04-02-a…c | A1-A §4 item 5; S1-A §2.2 item 5; AS §12 |
| SC2-04-03-1 | DEL-04-03 REQ-005, after the first sentence | (consumer list by package; DEL-09-06, DEL-09-09 named) | Add: "App v4 `DEL-02-01`, `DEL-02-03` and `DEL-03-01` consume it at deliverable level, and `DEL-03-04` (integration guide) declares it upstream; outside this undertaking `DEL-01-04`, `DEL-02-02`, `DEL-09-02`, `DEL-09-05` and `DEL-10-03` do so in their own registers." | Registered consumers unnamed; enables the R2-04-03 mirror rows | A1-A §4 item 6; first-increment R-04-03-d/e; RS §10.1 |
| SC2-04-03-2 | DEL-04-03 CLM-004, supplier list | "…checkpoint arrival, act and lapse events (with hold events retained for the governance phase) and compatibility reports from `DEL-02-03`, …" | "…checkpoint arrival, act request (where it can be identified), act and lapse events (…) and compatibility reports from `DEL-02-03`, the workflow identity tuple and the checkpoint disposition vocabulary from `DEL-02-01`, …" | R16 has no SoW anchor; RS's schema carries WD's tuple and dispositions (R14-1; RX); grounds new arc K-8 | RS 5 (B4); K1-1; R14-1; V18-2 M-3; ARC_ANALYSIS K-8 |
| SC2-04-03-3 | DEL-04-03 REQ-003, after the first sentence | "Recording shall preserve the actual human actor and scope of a performed act separately from its recorder and the recorder's available evidence." | Append: "For an act captured in the App, the actor is recorded from what the App can observe — the name the person set in the App, the operating-system account and the Codex account when Codex reports one — marked *identity not verified* (DECISION-K1 K1-4); a verified identity is governance-phase work." | Owner decision governs the decision-actor element (RS §6.1) and is not in the contract | K1-4; RS U-28 closed; S1-F §2.3 N-1 |
| SC2-02-01-1 | DEL-02-01 CLM-002 | "`DEL-01-01` supplies the harness capability inventory and supplied-guidance identity evidence;" | "`DEL-01-01` supplies the harness capability inventory, the capability-group meanings and availability signals to which harness-capability requirements resolve, and supplied-guidance identity evidence; this contract names those requirements;" | One wording for SoW and DEP-02-01-025; states who names | A1-D §4 item 5; A1-C §4 item 6; WD §4.2.5 HC-7; R14-5 |
| SC2-02-01-2 | DEL-02-01 CLM-002, end | — | Add: "This contract is received by `DEL-02-03`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02` and `DEL-09-06`, and outside this undertaking by `DEL-02-02`, `DEL-02-04`, `DEL-08-02`, `DEL-09-02` and `DEL-10-03`, each of which declares it upstream in its own register." | Enables supplier-side mirrors R2-02-01-a…f | First-increment R-02-01-a…f; HANDOFF P2 O-3 |
| SC2-02-03-1 | DEL-02-03 REQ-007 and VER-006 | "TBD-001 through TBD-005" (both) | "TBD-001 through TBD-006" | TBD-006 was added by SCA-V4-001 | A1-C §4 item 1; B2 §6; S1-C §C.1 |
| SC2-02-03-2 | DEL-02-03 Purpose (first sentence), SOW-052 traceability row (local contribution), REQ-002, AC-002, VER-002 | Purpose: "…requests the human acts its declared checkpoints require…"; SOW-052: "Request each declared checkpoint act despite direct-operation autonomy;"; REQ-002: "At a declared checkpoint, request the required human act and record it as done only when the person performs it…"; AC-002: "A declared checkpoint requests its named human act, and…"; VER-002: "Inspect the request, the recorded act state…" | Purpose: "…sees that the human acts its declared checkpoints require are requested, and records them only when performed…". SOW-052: "Each declared checkpoint act is requested despite direct-operation autonomy (in the current phase by the agent, DECISION-K1 K1-1);". REQ-002: "At a declared checkpoint, the required human act is requested and is recorded as done only when the person performs it, even where… In the current phase the agent carrying out the workflow requests the act; the App and a host's embedded loop give the agent the checkpoint, offer the means to act and record the arrival, the request where it can be identified and the act, and neither requests in the agent's place nor otherwise reacts to the arrival (DECISION-K1 K1-1)." AC-002: "A declared checkpoint's named human act is requested, and…". VER-002: "Inspect the request where it can be identified, the recorded act state…" | The SoW makes the slice the requester; the owner decided the agent asks. The condition A1-A put on this item ("if the owner confirms R9-1's reading") is met | K1-1; A1-A §4 item 8; EXEC RC-1…RC-6; ACT AP-12; S1-C §C.2 lag 2 |
| SC2-02-03-3 | DEL-02-03 CLM-002, "This slice consumes, and does not define:" list | (no DEL-04-02 item) | Add: "`DEL-04-02`'s grant display states (including *set by person, not yet confirmed*, *unconfirmed* and *refused*), for recording A12 checkpoints (REQ-002, REQ-003);" | Enables R2-02-03-a (mirror of DEP-04-02-023) | A1-C §4 item 3; EXEC §4.10, §9.1; AS §12.1 |
| SC2-02-03-4 | DEL-02-03 TBD-006, append | (ends "…as an input.") | "In the current phase an earlier act of the required kind whose content is still current counts toward an arrival and is cited with its time, and several acts may answer one arrival together (DECISION-K1 K1-2, K1-3). A workflow that takes up the governance phase may require a fresh act instead, declared through the portable declaration (`DEL-02-01`)." | Owner decisions in force with no SoW pointer; names SP-6F's take-up element | B1 §5; K1-2, K1-3; EXEC SP-6, SP-6F, JA-1; WD FA-1 |
| SC2-02-03-5 | DEL-02-03 CLM-002 | "…and `DEL-01-04`'s App act control and person identity, for the App-side positive capture fixtures…" | "…and `DEL-01-04`'s App act control, which records the person's identity as DECISION-K1 K1-4 sets it, for the App-side positive capture fixtures…" | K1-4 settled the identity scheme; only the control remains DEL-01-04's | K1-4; EXEC U-E8 closed, CAP-8; V18-4 J13 |
| SC2-02-03-6 | DEL-02-03 CLM-003, end | — | Add: "This slice's report, recording meanings and transfer contract are received by `DEL-02-01`, `DEL-03-03`, `DEL-03-04`, `DEL-04-02`, `DEL-04-03`, `DEL-05-01`, `DEL-05-02`, `DEL-09-06` and `DEL-09-09`, and outside this undertaking by `DEL-02-02`, `DEL-09-02` and `DEL-10-03`, each of which declares it upstream in its own register." | Enables supplier-side mirrors R2-02-03-b…i | First-increment R-02-03-a…c; HANDOFF P2 O-3; EXEC §9.2 |
| SC2-01-04-1 | **DEL-01-04** ScopeOfWork (outside these five; collected per K1-4): a new REQ (and a matching OUT, AC, VER) | DEL-01-04's SoW names no act control or person identity (`grep` returns 0; S1-F I-12; V18-4 J13) | "Provide the App act control: a dedicated control that only the person can operate — no agent tool, MCP operation, App rule or supplier request can operate it or produce its record — for one act kind at a time on App content (and A12 where an App control establishes the setting). It shows the act kind in its canonical wording, the bound subject with its content identity, the declared scope and purpose, the actor requirement and the arrival it answers, and offers the decline. Operating it produces a direct-capture human-act record with a capture-evidence reference in `DEL-04-03`'s format. It is a standing facility, available whether or not an arrival has been recorded, and no arrival raises it. It records the person's identity from what the App can observe (the name set in the App, the operating-system account, and the Codex account when Codex reports one), marked *identity not verified*. Presenting it answers no pending supplier request. Consumers: `DEL-02-03` (App-side positive capture fixtures), `DEL-04-03`, `DEL-04-01`." Process placement that makes "not operable by automation" true stays with OI-008 | K1-4 directs that the obligation be collected for the next amendment | DECISION-K1 K1-4; A3 §4; B2 §4 and §6 (RC-6); EXEC §5 CAP-1…CAP-9; DECISIONS_PENDING K1-4 option D |

## Proposed register items (none applied)

| ID | Register | Row / change | Class | Follows |
|---|---|---|---|---|
| R2-04-01-a | DEL-04-01 | DOWNSTREAM HANDOVER → DEL-09-06 (mirror of DEP-09-06-030) | mirror only | SC2-04-01-1 |
| R2-04-01-b | DEL-04-01 | UPSTREAM CONSTRAINT EXTERNAL → DECISION-5 destination grant (conditional) | non-topological | SC2-04-01-2 |
| R2-04-01-c | DEL-04-01 | UPSTREAM CONSTRAINT EXTERNAL → owner decision on the consequence vocabulary | non-topological | SC2-04-01-3 |
| R2-04-02-a…c | DEL-04-02 | DOWNSTREAM HANDOVER → DEL-03-04, DEL-09-06, DEL-09-09 (mirrors of DEP-03-04-012, DEP-09-06-031, DEP-09-09-022) | mirror only (3) | SC2-04-02-1 |
| R2-04-03-a…d | DEL-04-03 | DOWNSTREAM INTERFACE → DEL-02-01, DEL-02-03, DEL-03-01, DEL-03-04 (mirrors of DEP-02-01-019, DEP-02-03-013, DEP-03-01-031, DEP-03-04-013); DEP-04-03-011/-012 may stay as package rows | mirror only (4) | SC2-04-03-1 |
| R2-04-03-e | DEL-04-03 | UPSTREAM INTERFACE → DEL-02-01: "Receive the workflow identity tuple and checkpoint disposition vocabulary from App DEL-02-01" | **new arc** DEL-04-03 → DEL-02-01; both in SCC-002, so held and SCC-neutral (ARC_ANALYSIS K-8 tested "none") | SC2-04-03-2 |
| R2-04-03-f | DEL-04-03 | DEP-04-03-025 Statement: add "act request (where it can be identified)" | non-topological | SC2-04-03-2 |
| R2-04-03-g | DEL-04-03 / DEL-09-06 | Reconcile RequiredMaturity DEP-04-03-031 (INITIALIZED) with DEP-09-06-015 (TBD) | non-topological | HANDOFF_STATE; A1-A item 4; A1-E item 3 |
| R2-04-03-h | DEL-04-03 `_DEPENDENCIES.md` Run Notes | "…DOWNSTREAM DEP-04-03-031 (DEL-09-06 consuming this record contract, N-08, …)" → "…(DEL-09-06 consuming this record contract; the arc of DEP-09-06-015, …)" | non-topological (label) | A1-A §4 item 7 |
| R2-02-01-a…f | DEL-02-01 | DOWNSTREAM HANDOVER → DEL-02-03, DEL-03-02, DEL-03-04, DEL-05-01, DEL-05-02, DEL-09-06 (mirrors of DEP-02-03-009, DEP-03-02-027, DEP-03-04-008, DEP-05-01-016, DEP-05-02-005, DEP-09-06-025) | mirror only (6) | SC2-02-01-2 |
| R2-02-01-g | DEL-02-01 | DEP-02-01-025 Statement aligned with SC2-02-01-1 (inventory, group meanings, availability signals; names are this contract's) | non-topological | SC2-02-01-1 |
| R2-02-01-h | DEL-02-01 | DEP-02-01-027: RequiredMaturity TBD → INITIALIZED and SatisfactionStatus TBD → PENDING, as the other deliverable rows (normalization; owner's convention) | non-topological | A1-B §4 items 2, 4 |
| R2-02-03-a | DEL-02-03 | UPSTREAM INTERFACE → DEL-04-02 (mirror of DEP-04-02-023) | mirror only | SC2-02-03-3 |
| R2-02-03-b…i | DEL-02-03 | DOWNSTREAM HANDOVER → DEL-02-01, DEL-03-03, DEL-03-04, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-09-09 (mirrors of DEP-02-01-026, DEP-03-03-014, DEP-03-04-009, DEP-04-02-017, DEP-04-03-025, DEP-05-01-017, DEP-05-02-020, DEP-09-09-023) | mirror only (8) | SC2-02-03-6 |
| R2-02-03-j | DEL-02-03 | DEP-02-03-027 Statement: "DEL-01-04's App act control and person identity" → "DEL-01-04's App act control (person identity as DECISION-K1 K1-4 sets it)" | non-topological | SC2-02-03-5 |
| R2-01-04-a | DEL-01-04 (outside) | DOWNSTREAM HANDOVER → DEL-02-03 (mirror of DEP-02-03-027, arc X-1, held) | mirror only | SC2-01-04-1 |

Counts: 24 mirror-only rows; 1 new arc (R2-04-03-e); 8 non-topological
(R2-04-01-b, -c; R2-04-03-f, -g, -h; R2-02-01-g, -h; R2-02-03-j). Any new arc
needs a `project-dag` departure; mirror rows move DAG-003 source currency
only. Outside mirrors noted, not proposed (D1): DEL-04-01 → DEL-01-02, 01-04,
02-02, 06-02, 09-02, 09-05, 09-12, 10-03; DEL-04-03 → DEL-01-04, 02-02,
06-01, 06-02, 09-02, 09-05, 10-03; DEL-02-01 → DEL-02-02, 02-04, 08-02,
09-02, 10-03; DEL-02-03 → DEL-02-02, 09-02, 10-03. DEL-02-02's register
should name A15 and its RS record kind at its next revision (B4 §7).

## Basis items

None proposed. Considered: the basis texts V4-WF-05, V4-HI-42 and V4-EXM-22
say the act "is requested" without saying by whom, which K1-1 reads without
contradiction; A1-A item 8 offered "SoW or basis", and SC2-02-03-2 takes the
SoW route. The ScopeLedger row SOW-052 ("…request the required human act…")
has no subject either; changing it is the scope-change route's and is not
needed for K1-1.

## Raised in this run and not proposed (with disposition)

| Item | Source | Disposition |
|---|---|---|
| DEL-04-03 OUT-001: name the PROPOSED format files as the CONFIG candidate; DEL-04-01 OUT-002: name the schema | B4 §7 items 1–2 | Not warranted: OUT-001 already leaves serialization and spellings to design, and LOOP_INIT keeps technical details in maintained artifacts. The U-02 part of item 2 is SC2-04-01-3 |
| DEL-04-02 ↔ DEL-05-01: "grant in force per dispatch" now defined | B4 §7 item 4 | Informational; DEP-04-02-019 / DEP-05-01-025 need no change |
| Whether *not known to host* and *identity conflict* are R7 outcomes or R11 limits | B3 §6 item 4 | Decided in Design (R14-3: outcomes; RS §5); no SoW item |
| DEL-01-01 use of D3 (V-21/V-25) without a row | A1-A §4 item 3 | Not proposed (ARC_ANALYSIS K-12) |
| DEL-04-01 as consumer of WD (row or drop WD's row) | A1-C §4 item 4 | Not proposed (K-2; guard); WD-v0.8 §8 keeps it as a cross-check |
| DEL-02-03 SoW: name ADAPTER §7.7 as the arrival supplier; "may be recorded" vs REQ-002 | S1-C §C.2 lags 1, 3 | Fixed in Design (RC-1; §4.4 cites CO-1…CO-11; §10 rows) |
| `_CONTEXT.md` of DEL-04-02, DEL-04-03, DEL-02-01 lack the "as amended by the active scope-change snapshot" sentence that DEL-04-01 and DEL-02-03 carry | this comparison | No change warranted: SCA-V4-001/-002 edited `_CONTEXT.md` only where the Deliverables.csv row changed (`Amendment_Actions.csv` row 36; SCA-V4-002 `Brief.md` rows 14, 16) |
| DEL-05-02's contract and the panel's destination surfaces; DEL-09-09 REQ-001's TBD range | brief; A1-D §4 item 1; A1-E §4 item 1 | Not these deliverables: C1-C. Nothing for DEL-04-02 (B5 §7: CLM-002 already carries the display) |

---

## Returned to the graph (Design work, not proposals)

- **G-1 — "No accepted text says a decline is recorded" is contradicted by
  DEL-04-03's ScopeOfWork.** RS (header bullet; §4 R15 "Destination
  declined"; §8; change row R12-10) and AS (§6 = RS §8, line 594; §3, §3.1,
  §3.2) say of a declined destination request that "no accepted text says it
  is recorded" and label its recording PROPOSED, following R12-10. DEL-04-03
  SoW CLM-004, revised under accepted SCA-V4-001, says the format receives
  "a host agent's network-destination events (destination contacted,
  destination grant, destination declined) from `DEL-05-01`", and
  DEP-04-03-028 repeats it. R12-10 cited V4-HI-70, V4-ARC-12 and V4-EXM-23
  only; no review or comparison cited CLM-004 (grep of `reviews/`,
  `comparisons/`). Boundary refusals are not named in CLM-004 and stay
  PROPOSED. Needed: an integrator ruling amending R12-10 for declines, then
  a relabel (DERIVED from CLM-004) in RS, AS, ACT §2.7's decline row, and
  the LOOP/PANEL/GUIDE passages that echo it (C1-B, C1-C files).
- **G-2 — EXEC's harness-capability presence rule waits for something
  HOSTING appears to supply.** EXEC EV-3 and U-E10: the PROPOSED rule "takes
  no effect until DEL-01-01 states those signals per group". HOSTING-v0.8
  §8.4 (at `a9046631c0`, line ~1158) has a table "Availability signals in
  the generated types" for HCG-A01…A17 (HCG-A07 "Not stated in the generated
  types"). Either EV-3's condition is met for the groups with signals
  (standing: generated-type, not observed) and REQ-001's check can be
  defined for them, or EXEC must say what it still needs that §8.4 lacks.
  This is what keeps DEL-02-03 OUT-001/REQ-001 partial. Owner: DEL-02-03
  with DEL-01-01.
- **G-3 — Minor bookkeeping for the next pass.** EXEC §9.1's DEL-04-02 row
  still reads "Current: AS-v0.7"; it should cite AS-v0.8 §12.1 and confirm or
  return AS's PROPOSED reading of an *unconfirmed* earlier A12 (B4 join
  note); EXEC §11.5 F-34 still reads open though RS L-12 now states the value
  (*performed* with the annotation; V18-1 m-7); RS §10 lacks rows for
  DEL-03-04, DEL-09-02, DEL-09-05, DEL-10-03 (§10.1 says so); "run owner"
  (EXEC CE-17, AE-7) is undefined (V19-A n-5).

Every other open item already has a home: an `UNRESOLVED` row with owner and
point of need, an owner decision (DECISIONS_PENDING Parts 3–4), a SWBPIPE
relay item, or a proposal above. No Task Management intake.

## Pointers for the MEMORY run entries (final PR)

One terse entry per deliverable, e.g. "2026-09-30 — APP-V4-DESIGN-PASS-2-20260930
(second design pass): Design developed to ‹version› with PROPOSED schemas
and local prototypes; draft definitions only — no implementation,
lifecycle, register or SoW change. Receipt: ‹run RECEIPT›; proposed SoW and
register changes in `closeout/C1-A.md`." Versions: ACT-POLICY-v0.8; AS-v0.8;
RS-v0.8; WD-v0.8 and WD-EX-v0.8; EXEC-v0.6.

## Checks performed and limits

- Each OUT and REQ was traced into the Design sections, and each structure
  added in this run was traced back to its ruling or decision. SoW pins in
  the Design headers equal the SoW bytes (grep of full hashes).
- Register rows were read from all five `Dependencies.csv` files; mirror
  coverage was computed by script over every ACTIVE EXECUTION deliverable row
  of all registers; arcs were checked against DAG-003 `DependencyEdges.csv`
  and `CandidateEdges.csv` by script (DEL-04-03 → DEL-02-01 absent in both).
- Prototypes rerun on 2026-10-01 with Python 3.13.7,
  `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` set to a private scratch folder:
  ACT `validate_policy.py`, AS `validate_settings_in.py` ("RESULT: all
  expectations held" each); RS `run_prototype.py` (51 PASS, 0 FAIL); WD
  `wdproto.py selftest` (62 of 62); EXEC `run_all.py` ("ALL CHECKS HOLD").
  `git status --porcelain` was identical before and after.
- Quoted SoW texts were copied from the current files. The G-1 and G-2
  passages were read at the candidate (`git show a9046631c0:…` for HOSTING).
- Not done: no re-review of design content beyond the comparisons above; no
  check that the proposed wording is final; the large Design files were read
  by section (headers, change tables, the sections each commitment maps to,
  receivers, UNRESOLVED and verification cases), not line by line.
- Read-only git; no network; no file other than this one written.
