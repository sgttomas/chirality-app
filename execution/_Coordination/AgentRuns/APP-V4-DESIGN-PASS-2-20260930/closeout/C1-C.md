# C1-C — bounded closeout: DEL-05-01, DEL-05-02, DEL-09-06, DEL-09-09

- **Run / node:** APP-V4-DESIGN-PASS-2-20260930, closeout node C1-C.
- **Method:** `chirality-root:bundled:workflow:bounded-reconciliation`
  (`workflows/bounded-reconciliation/WORKFLOW.md`, sha256 `c7798c0ae59860f1…`,
  read whole). Used as a read-only comparison: every warranted change is a
  **proposal**, none applied.
- **Executor:** Type 2 TASK (Claude Code subagent, Claude Opus 5.5). No
  delegation, no network, read-only git. Only this file was written; scratch
  output went under `$TMPDIR`.
- **Brief:** BRIEFS.md "Common rules" and "C1 — bounded closeout" (read in
  the working copy, sha256 `84314222435108d8…`, equal to the copy committed
  at `41899194c4`); OWNER_DECISIONS.md (`b2fa81871cbf44b9…`); R9…R15; the
  first increment's `closeout/C1-C.md` (`e5750aa4a0083ee4…`) and
  `CLOSEOUT_ACCOUNT.md` as precedent; `loop/LOOP_INIT.md` "Develop the detail
  appropriate to the phase" (`3790159b4f60bb4f…`); the work graph
  (`32c89f1591e1b24b…`); DAG-003 `HANDOFF_STATE.md`.
- **Candidate:** `a9046631c0`. Every Design file below was read with
  `git show a9046631c0:<path>`. During this node HEAD moved to `41899194c4`
  (C0). Between the two, the only change in these four deliverables is LOOP
  §3.1 F-2 and §3.2 (C0, V19b m-1: a no-credential first turn opens the run
  before its refusal). It changes no commitment compared here.
- **Bound files unchanged.** `git diff --stat 74b3c73134 a9046631c0` over the
  four `ScopeOfWork.md`, `Dependencies.csv`, `_DEPENDENCIES.md`, `_STATUS.md`
  and `MEMORY.md` is empty. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and
  `FACTS_SQ01_SQ32.md` are also unchanged since the run start. Both were read
  as data only.
- **Boundary (binding).** DAG-003's `SOURCE_MANIFEST` binds every
  `ScopeOfWork.md`, `Dependencies.csv` and `_DEPENDENCIES.md`. No SoW,
  register, `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md` or Design file is
  edited here. Each item below is a proposal for a later amendment and
  `dependency-extract` run, or a residual for the graph.

| Deliverable file at `a9046631c0` | sha256 (prefix) |
|---|---|
| DEL-05-01 `ScopeOfWork.md` / `Dependencies.csv` / `_DEPENDENCIES.md` / `_STATUS.md` / `MEMORY.md` | `9b2379a1…` / `6c86f226…` / `7c1e6eec…` / `d54d0312…` / `266d34d6…` |
| DEL-05-01 `Design/LOOP_RECEIVING_CONTRACT.md` (LOOP-v0.8); `LOOP_TOOL_CALL.schema.json`; `LOOP_DESTINATION_REQUEST.schema.json`; `prototype/` (4 files) | `f0065788…`; `8cb7c315…`; `7b70146b…`; README `0218e166…` |
| DEL-05-02 `ScopeOfWork.md` / `Dependencies.csv` / `_DEPENDENCIES.md` / `_STATUS.md` / `MEMORY.md` | `beb9c66c…` / `2889aa5f…` / `db27f5bc…` / `ddaaff1f…` / `af744a88…` |
| DEL-05-02 `Design/PANEL_RECEIVING_CONTRACT.md` (PANEL-v0.8); `PANEL_RETURN_INPUT.schema.json`; `prototype/` (4 files) | `e2979601…`; `c0f7cc5d…`; README `0d0b2d9b…` |
| DEL-09-06 `ScopeOfWork.md` / `Dependencies.csv` / `_DEPENDENCIES.md` / `_STATUS.md` / `MEMORY.md` | `287d47a1…` / `0f8ecad8…` / `79e780ee…` / `c2eb59ad…` / `fa001ea4…` |
| DEL-09-06 `Design/CONNECTED_ACTIVITY_CONTRACT.md` (CA-v0.6); `RELAY_QUESTIONS_SWBPIPE.md` (RELAY-v0.3); `w14-result-record.schema.json`; `prototype/` | `332c3f25…`; `34efb532…`; `20d3c976…`; README `5a510eee…` |
| DEL-09-09 `ScopeOfWork.md` / `Dependencies.csv` / `_DEPENDENCIES.md` / `_STATUS.md` / `MEMORY.md` | `e887a579…` / `e0e3297a…` / `fb23e7bf…` / `82eba88d…` / `6d78af86…` |
| DEL-09-09 `Design/EXTERNAL_TRACE_CASES.md` (XT-v0.6); `xt-result-record.schema.json`; `xt-work-account.schema.json`; `prototype/` | `daf6c9c9…`; `3b0ff2bb…`; `ffe11271…`; README `c8724e8b…` |

**Conventions.**

- Arcs are written **consumer → supplier** and classified against DAG-003
  (`DependencyEdges.csv` = admitted; `CandidateEdges.csv` = held). **No
  proposal below adds an arc.** Two proposed new rows mirror admitted arcs,
  and one is an EXTERNAL (non-topological) row.
- "Raised in this run" means a source in this run's `SURVEY/`, `WAVE_A/`,
  `WAVE_B/`, `comparisons/`, `reviews/` or a Design file of this run.
  "C1-C" as a source means this comparison found it.
- Standing words for commitments: **developed**, **partial**, **named only**,
  **absent**.

## Summary

| DEL | OUT developed / partial / named only / absent | Proposed SoW | Proposed register (row edits / new rows) | Proposed basis | Lifecycle |
|---|---|---|---|---|---|
| DEL-05-01 | 3 / 1 / 0 / 0 | 1 | 3 / 2 | 2 | IN_PROGRESS; unchanged; CHECKING not warranted |
| DEL-05-02 | 2 / 1 / 1 / 0 | 1 (an owner choice) | 2 (one conditional) / 0 | 0 | IN_PROGRESS; unchanged |
| DEL-09-06 | 1 / 3 / 0 / 0 | 4 | 3 / 1 | 0 | IN_PROGRESS; unchanged |
| DEL-09-09 | 0 / 3 / 0 / 0 | 2 | 3 / 0 | 0 | IN_PROGRESS; unchanged |
| **Total** | 6 / 8 / 1 / 0 | **8** | **11 / 3** (14) | **2** | — |

No proposal adds an arc or changes an SCC.

**Main result.** No OUT item is absent. The partial items wait on an owner
choice (OI-021, OI-003, OI-013/014, the F-12 scope question), a host input
(DEP-001; host joins deferred by DECISION-3), a later undertaking (DEL-02-02,
DEL-01-04, DEL-09-01, App construction) or a witness. One required
contribution named by an ACTIVE register row is still undefined: DEL-05-02's
"panel receiving needs" (DEP-05-01-020). That goes back to the graph as work,
not as a proposal (§6).

---

## 1. DEL-05-01 — Minimal-loop and model receiving contract (LOOP-v0.8)

### 1.1 Commitment → result

| SoW item | Where LOOP-v0.8 answers it | Standing | What remains |
|---|---|---|---|
| OUT-001 receiving contract | §1, §2.1–§2.4 (four subjects), §3, §3.1 (F-1…F-13), §3.2 (run, turn, tool-call, destination-request state tables), §4 (with the R12-11 model-interface boundary), §5.1, §5.1.1, §5.3 (DF-1…DF-10, DF-F1…DF-F12), §6, §7, §8, §9 | **Developed** | A product model-interface basis (DEP-05-01-024 UNKNOWN); host evidence (DEP-001) |
| OUT-002 fixtures | §4.1 FB-CC-1 ("fixture basis, not a product selection", R12-8), §7.1–§7.3, §11 FX-V/S/D/U/R/NP/O/UNDO/M/N/C | **Partial** | The parse-level fixtures and the destination flow run on prototypes. The other fixtures are case designs. The basis is a fixture basis only; DEP-05-01-024 stays open for a product |
| OUT-003 conformance cases and evidence expectations | §5.2 MS-01…MS-27, §7 MC-1…MC-13, §8 RS-1…RS-4, §12 labels, VC-01…VC-10 | **Developed** (definition) | Every host observation is NOT-OBSERVED. SWBPIPE has no loop (SQ-20, SQ-29) |
| OUT-004 allocation / open-choice account | §10.1–§10.4; UNRESOLVED | **Developed** | OI-013, OI-014 open. Stale standing cells (§6, GW-3) |
| REQ-001 model choice, destinations, native layer, credentials | NW-1…NW-16; §5.3; MS-01…MS-27; R15-1 "run not started — no model selected" (F-2 (a), MS-02) | Developed | Recording declines and refusals is PROPOSED (R12-10; basis item B-2). N-OPEN-2/3 are open |
| REQ-002 Chat Completions, four subjects, App path distinct, Pi unselected | §1, §2, §4, §4.1 (FB-CC-1), §4.2 | Developed | DEP-05-01-024 for a product |
| REQ-003 schema before domain; malformed never empty | §6 V-1…V-5 and V-D; §7 MC-1…MC-13; MC-8 per R12-7 | Developed | PROPOSED until a product basis is observed (OBS-1 is one server at one version) |
| REQ-004 responsiveness; no prescribed means | §8; F-11, F-12 | Developed | Host observations. R-OPEN-1 is open by design |
| REQ-005 inputs, owners, standing | §10.3 | Developed | Panel needs (DEP-05-01-020) not defined by PANEL (GW-1) |
| REQ-006 excluded acts; current-phase recording and governance-phase hold machine | §0 "Who builds what"; §10.1; §2.4.0; §2.4.4 | Developed | — |
| REQ-007 distinct acts; declared checkpoints | §2.3 (E-8 mapping to RS kinds), §2.4, §9 | Developed | — |
| AC-001…AC-009 / VER-001…VER-009 | VC-01…VC-10 | VC-05 partly run (prototype 22/22); VC-10 run (prototype); the rest designed | Host-side execution |

### 1.2 Result → commitment

| Design element | Authority | Assessment |
|---|---|---|
| §5.3 destination flow: destination-reaching tools are host catalog entries with an external-contact declaration; the in-work request is a call to a host-supplied destination request entry (DF-1, G-13) | REQ-001; CLM-002 (DEL-03-01 owns catalog schemas); B5; C-v0.8 §3.4 | Supported. DEP-05-01-014 does not name these catalog elements (R-0501-2) |
| FB-CC-1 as the fixtures' model-interface basis (§4.1) | R12-8 (INTEGRATION); DECISION-K1 K1-6 (fetch allowed) | Supported by a ruling. SoW OUT-002 says fixtures identify their "adopted" model-interface basis, and FB-CC-1 is not adopted. Clarification proposed (S-0501-1) |
| One model-interface boundary, Responses the likely second interface (§4; R12-11) | Owner direction "Host-loop model interface" (2026-09-30): design, not a selection | Supported; no SoW change needed (REQ-002 already requires replaceability and leaves the supplier unselected) |
| State tables, E-6 event ordinal, E-7, E-8 (§2.3, §3.2) | OUT-001 events; CLM-002 (DEL-04-03 format); R14-1 | Supported; PROPOSED |
| Stateless-MCP evidence rule DF-7, with the limit "stateless revision declared, not verified" | REQ-001 (stateless MCP only); R13-3 | Supported; the rule is PROPOSED |
| Recording declined and refused requests | R11-5, R12-10: PROPOSED. V4-HI-70 and V4-ARC-12 record destinations *contacted* only | Beyond the accepted text, labelled so. Basis item B-2 (optional) |
| Prototypes `assemble_tool_calls.py`, `destination_flow.py` | R12-3 | Definition aids, not product code. Supported |

No unsupported addition was found.

### 1.3 What the 60% description still lacks

LOOP-v0.8 has interfaces, states, data (two PROPOSED schemas), sequences,
failure behaviour at each step, and verification with two runnable
prototypes. Missing:

- a **product** model-interface basis (DEP-05-01-024). The rows written from
  FB-CC-1 stay PROPOSED, and the deferred second result to an answered call
  is an inference (G-13);
- any host-loop observation. SWBPIPE has no loop, and its embedded direction
  predates D-20 (SQ-20, SQ-29; R8-8);
- the placement choices OI-013 and OI-014;
- the panel-needs list that DEP-05-01-020 names (GW-1);
- N-OPEN-2 (which endpoints a cloud sign-in service comprises) and N-OPEN-3
  (tool-caused traffic beyond declared traffic).

**Inference:** no structural change to the receiving contract itself is
anticipated from these. Host-side structure depends on SWBPIPE owner
decisions (UI-SUCCESSOR, the D-58 successor) that the App does not control.

### 1.4 Register rows the Design file shows to be stale or missing

- DEP-05-01-024: still reads as wholly unsupplied. LOOP now names a fixture
  basis for its own fixtures (R-0501-1).
- DEP-05-01-014: does not name the catalog elements the destination flow
  consumes (R-0501-2).
- DEP-05-01-025: the "grant in force per dispatch" is now defined (AS-v0.8
  §12.1; LOOP §6.2) (R-0501-3).
- Missing rows:
  - a mirror of DEP-01-05-014 (R-0501-4);
  - a DOWNSTREAM relay row (R-0501-5).

  Both were first raised at the first increment (R5-1-2, R5-1-3) and raised
  again in this run (A1-D §4 items 2–3; LOOP G-10, §10.4).

### 1.5 Proposed ScopeOfWork change (DEL-05-01)

| # | Locus | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| S-0501-1 | TBD-003, after "…so that basis stays UNKNOWN." | (as quoted) | Append: "For its own fixtures this deliverable writes against a published Chat Completions reference that it names as a fixture basis, not a product selection (Design `LOOP_RECEIVING_CONTRACT.md` §4.1, FB-CC-1; integrator ruling R12-8 of `APP-V4-DESIGN-PASS-2-20260930`). That names no adopted basis for any host, and DEP-05-01-024 stays open." **Optional, for the owning amendment:** in OUT-002, "Fixtures identify their adopted catalog and model-interface basis" → "Fixtures identify their adopted catalog basis and their model-interface basis (adopted, or until one is adopted a named fixture basis)". The second edit touches an output definition, so it follows the amendment's decision path | R12-8; LOOP §4.1, §11, G-11; C1-C. Pointer and clarification; no requirement is relaxed |

R-4 wording check: "checked" in REQ-003 is the tool-argument check, and
CLM-004 and REQ-007 name the person's A4. Both uses are consistent, so no
change is proposed.

### 1.6 Proposed register changes (DEL-05-01)

| # | Change | Kind | Grounds |
|---|---|---|---|
| R-0501-1 | DEP-05-01-024 Notes, append: "UPDATE (proposed): LOOP-v0.8 §4.1 names FB-CC-1, the published OpenAI OpenAPI specification retrieved 2026-09-30, as a fixture basis for this deliverable's own fixtures, not a product selection (R12-8; DECISION-K1 K1-6). OBS-1 recorded the four representation points on one local server, as an observation, not qualification. No adopted basis is supplied: TargetType stays UNKNOWN and SatisfactionStatus PENDING." | Row edit (UNKNOWN; non-topological) | R12-8, R13-6; LOOP §4.1; C1-C. Pairs with S-0501-1 |
| R-0501-2 | DEP-05-01-014 Notes, append: "LOOP-v0.8 §5.3 DF-1 also consumes, from the catalog schemas, an entry's external-contact declaration and the destination request entry kind (C-v0.8 §3.4) for the destination flow." Statement unchanged | Row edit (held arc in SCC-002; unchanged) | B5 §7 (its DEL-03-01 item is C1-B's); LOOP §5.3, G-13; C1-C |
| R-0501-3 | DEP-05-01-025 Notes, append: "The grant in force per dispatch is defined at AS-v0.8 §12.1 and consumed at LOOP-v0.8 §6.2 (definition only); SatisfactionStatus stays PENDING." | Row edit (held arc; unchanged) | B4 §7; LOOP §6.2 |
| R-0501-4 | New row: UPSTREAM INTERFACE, DELIVERABLE DEL-01-05, mirroring DEP-01-05-014 (local-server capability requirements and qualification limits). DEL-05-01's SoW does not name DEL-01-05, so under CONSERVATIVE extraction this would be a declared mirror (`_DEPENDENCIES.md` "Declared Upstream"). **Alternative:** the register owner records why no consumer row is kept (LOOP §10.3: "not consumed by this file") | Mirror only (arc DEL-05-01 → DEL-01-05 is admitted in DAG-003) | First increment R5-1-2; A1-D §4 item 3; LOOP G-10, §10.3. Also covered by HANDOFF_STATE "Deferred supplier-side mirror rows (P2 O-3)" |
| R-0501-5 | New EXTERNAL row: DOWNSTREAM HANDOVER → DEP-001, "External SWBPIPE owner — loop receiving questions (LOOP §13) via App-manager preparation and human file relay". This mirrors DEP-05-02-018 | New row (EXTERNAL; non-topological) | First increment R5-1-3; A1-D §4 item 2; LOOP §10.4; SoW "Production and Verification Method" (human-relayed file path) |

### 1.7 Lifecycle observation

`_STATUS.md` reads **IN_PROGRESS** (2026-09-28, owner direction
DECISION-6). That is still truthful. CHECKING is not warranted:

- the proposals are unapplied;
- the fixtures are on a fixture basis only;
- host evidence is absent;
- G-4 (the LOOP/PANEL pair check) is not closed in the file.

No change is made here.

---

## 2. DEL-05-02 — Host panel and shared interaction receiving (PANEL-v0.8)

### 2.1 Commitment → result

| SoW item | Where PANEL-v0.8 answers it | Standing | What remains |
|---|---|---|---|
| OUT-001 panel interface and receiving requirements | §1–§5; §3.1–§3.4 four interactions; §3.5 checkpoints; §3.6 grant; §3.8 destinations (receiving); §3.9 return inputs RI-1…RI-4 with sequence RT-a…RT-e and `PANEL_RETURN_INPUT.schema.json`; §3.10 failure displays FD-1…FD-4 | **Developed** | Panel-needs list (DEP-05-01-020; F-13). Per-interaction operating sequences beyond the return sequence |
| OUT-002 allocation account | §6 (six candidates; agreement "None") | **Developed** (as an account) | OI-014 agreement |
| OUT-003 receiving cases, then candidate-bound results | §7 PC-01…PC-46; accounting states; §7.1 test double; prototype `panel_double.py` | **Partial** | PC-38…PC-41 ran on the double (4/4), so they are *EXECUTED (test double)* for display rules only. Every other case is DESIGNED. No host candidate (DEP-001). Actual acts (DEP-05-02-017) |
| OUT-004 conditional reusable components | §6 "OUT-004 conditional state" | **Named only** (AC-006 allows the recorded conditional state) | An agreed repeated responsibility (OI-014) |
| REQ-001 four interactions traced to consumed definitions | §3.1–§3.4 "Consumed definitions" rows; VC-01 | Developed | VC-01 still cites the consumed definitions at Wave A labels (GW-3) |
| REQ-002 host tables and views; no private surface | §2 P-1…P-3; §4 H-1…H-6; FD-2 | Developed | Host view references (SQ-22: none supplied) |
| REQ-003 distinct acts; accept; faithful record; lapse | §3.5 W-5a…W-5g; §5 W-1…W-7, K-1…K-4 | Developed | — |
| REQ-004 repeated responsibility; OI-013/014 separate | §6 | Developed | — |
| REQ-005 cases against identified inputs | §7 states; §7.1 | Developed | — |
| REQ-006 excluded acts | "Responsible" rows; §6; VC-07 | Developed | — |

### 2.2 Result → commitment

| Design element | Authority | Assessment |
|---|---|---|
| §3.8 ND-2 in-work destination prompt with states PS-1…PS-6 (PANEL's own), and ND-1, ND-4, ND-5 receiving AS §3, §3.1, §3.2 and LOOP §5.3 | DECISION-5; V4-HOST-02 as amended; the panel's reading of CLM-002 and REQ-001 | **Not named by the SoW** ("destination" occurs 0 times; AX-004 omits DECISION-5; SOW-017 is DEL-05-01's). PANEL F-12 returns it to the owner. The owner deferred it at SCA-V4-001 OWNER_ITEMS O-15 (DECISION-7): "No other SoW change for DEL-04-01 or DEL-05-02 now … Revisit when the A12 mapping is confirmed or at implementation". The A12 mapping is still INTEGRATION (DECISIONS_PENDING Part 3: decided at the phase review). See S-0502-1 |
| §3.9 return inputs and schema; §3.10 failure displays | OUT-001 (conversation, workflow selection); REQ-001 | Supported; PROPOSED |
| §7.1 panel test double and prototype | OUT-003 accounting state *EXECUTED (test double)*; R12-3 | Supported |
| FD-3: the panel asks the loop for events from the last ordinal it holds (LOOP F-12) | LOOP E-6 (PROPOSED) | **Observed:** this request back to the loop is in neither §3.9's list of return inputs nor `PANEL_RETURN_INPUT.schema.json`. It belongs with the panel-needs list (GW-1) |

### 2.3 What the 60% description still lacks

- **The panel-needs list.** DEP-05-01-020 names "panel receiving needs and
  meaning at the loop boundary". PANEL F-13 says it is "still not written as
  one list". It should include the event-replay request (FD-3).
- **Operating sequences per interaction.** For example: queue → host view →
  item decision → host capture → application → receipt → panel. Only the
  return-input sequence RT-a…RT-e exists. S1-D PANEL §5 named this; no Wave B
  node took it.
- **A panel lifecycle** (closed, reopened, reloaded while a turn runs) beyond
  FD-3's reattach.
- **Host evidence.** None exists.
- **Owner and placement choices:**
  - F-12, whether the contract names the destination surfaces;
  - OI-013 (panel assembly) and OI-014 (shared components), which can still
    change where §3.5, §3.6 and §5 live (S1-D PANEL §5).

### 2.4 Register rows the Design file shows to be stale

The revised SoW CLM-002 says "identified, independently compared". Seven
ACTIVE Statements still use the unqualified "checked" that R-4 reserves for
A4 (R-0502-1). DEP-05-02-014 and DEP-05-02-015 are correctly RETIRED.

### 2.5 Proposed ScopeOfWork change (DEL-05-02): the network-destination surfaces

**Question (brief):** should DEL-05-02's contract name the panel's
network-destination surfaces?

**Answer:** this is an owner choice, already deferred by the owner (O-15).
Its trigger, confirmation of the A12 mapping for destination grants, has not
occurred. Node B5 narrowed it:

- the display meanings now belong to DEL-04-02 (AS §3, §3.1, §3.2), whose
  CLM-002 already names the destinations-contacted record;
- the rules and the flow belong to DEL-05-01 (§5.1.1, §5.3);
- PANEL's own content is the prompt ND-2 (PS-1…PS-6) and its must-nots.

The proposal is stated so that it can be applied when the owner decides.

| # | Locus | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| S-0502-1 (option A) | CLM-002, fourth and fifth sentences | "…and `DEL-05-01` supplies loop messages/tools/events/checkpoints and receiving requirements. `DEL-04-02` supplies autonomy-grant display states and active scope." | "…and `DEL-05-01` supplies loop messages/tools/events/checkpoints and receiving requirements, including the host agent's network-destination rules and destination request flow. `DEL-04-02` supplies autonomy-grant display states and active scope, including the display of the allow list, in-work destination grants and destinations contacted." | PANEL §3.8, F-12; LOOP §5.3, G-14; AS §3.2; S1-D PANEL §2 item 5, §4 item 13; A1-D §4 item 1; B5 §7; DECISIONS_DRAFT choice 19; O-15 |
| S-0502-1 (option A, continued) | OUT-001, after "…responsible participants." | — | Add: "It includes the host panel's in-work destination request prompt and its receiving of the allow-list, grant and destinations-contacted displays (PRD V4-HOST-02 as amended by `SCA-V4-001`; `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`)." The amendment's AX line also adds DECISION-5 to the decisions it applies | As above |
| S-0502-1 (option B) | — | — | No change. §3.8 stands as the panel's receiving of DEL-05-01's and DEL-04-02's definitions under CLM-002, as PANEL reads it. The prompt ND-2 then has no DEL-05-02 obligation. "Every destination contacted is shown" stays examined through DEL-04-02 and DEL-05-01 (SOW-017), and V4-EXM-23 sits with DEL-09-07 | O-15 as decided ("no other SoW change … now") |

**Recommendation (advice only):** carry S-0502-1 to the phase review with
DECISIONS_PENDING choice 7 (the A12 mapping), as O-15 provides. Option A
adds no arc: DEP-05-02-010 and DEP-05-02-019 already exist (held, SCC-002).

### 2.6 Proposed register changes (DEL-05-02)

| # | Change | Kind | Grounds |
|---|---|---|---|
| R-0502-1 | Statements of DEP-05-02-005, -006, -007, -008, -009, -010 and -019: "consume the actual checked … definition" → "consume the actual identified, independently compared … definition". The meaning is unchanged | Row edits ×7 (one item) | R-4 (R1_RESOLUTIONS); SoW CLM-002 as revised (first increment S5-2-6, applied by SCA-V4-001); C1-C |
| R-0502-2 (only with S-0502-1 option A) | DEP-05-02-010 Statement: add "including the host agent's network-destination rules and destination request flow". DEP-05-02-019 Statement: add "including the allow-list, in-work grant and destinations-contacted display" | Row edits; no new arc | Pairs with S-0502-1 |

### 2.7 Lifecycle observation

**IN_PROGRESS** is still truthful. CHECKING is not warranted: OUT-003
results and OUT-004 are outstanding, F-1 and F-12 are open, and the panel
needs are undefined. No change is made here.

---

## 3. DEL-09-06 — Connected activity contract and workflow round trip (CA-v0.6, RELAY-v0.3)

### 3.1 Commitment → result

| SoW item | Where answered | Standing | What remains |
|---|---|---|---|
| OUT-001 increment SoW, owner/check allocation, handoff | CA §2.1–§2.6 (step map; failure rows CAF-1…CAF-39; current-phase sequence; DI-1…DI-9; **option sheet §2.6**); §5; §6; §10 | **Partial** (a draft contract; AC-001 allows it) | OI-021 (DI-1…DI-3). AC-001's "all seven assigned scope items": SOW-236/237/240/241 are traced only in VC-CA-01, not in the body (GW-3) |
| OUT-002 reusable connected workflow | CA §3.1 WR-1…WR-11; §3.2 WF-1, WF-1c | **Partial** (requirements only) | Authoring and review under `create-workflow` with DEL-02-02 (later undertaking) |
| OUT-003 joined V4-EXM-14 witness | CA §4; §8.1–§8.3; §8.4 W14 result record (PROPOSED schema); §8.5 rehearsals (12 records on SH-1, none counted) | **Partial**; **cannot complete** in this undertaking (§3.5 below) | The App candidate (later), a host candidate, DEL-02-02, actual acts (DEP-09-06-024), host joins (DECISION-3), SWBPIPE work items (ANS §2, §4) |
| OUT-004 questions, answers, contribution account | RELAY §0–§4 (relayed body byte-identical: span sha256 `6e399c83…`, verified); RELAY_ANSWERS (data); CA §7.2, §9 EC-01…EC-14 | **Developed** | Nothing beyond *answered*. A successor relay is owner-held (RELAY UNRESOLVED) |
| REQ-001 complete first activity | CA §2 | Developed (draft, on the fixture) | OI-021 |
| REQ-002 declarations; source-qualified revisions | CA §3, §4 | Developed (definition) | Witness |
| REQ-003 tools, unsupported outcome, checkpoint, interruption, revision | W14-03, W14-04, W14-07, W14-10 (current phase and governance phase) | Developed (design); rehearsed in part | Witness |
| REQ-004 policy, autonomy, distinct acts | S-4…S-14; CA-H; W14-04/05/06 (CH-31 for "prior act not counted") | Developed | Host act facility (SQ-01: no capture-evidence reference) |
| REQ-005 proposed / received / delivered / adopted / examined | CA §7.2, §9; RELAY §4 | Developed | — |
| REQ-006 staging without PEC/Domains | CA §6 ST-0…ST-5 | Developed | ST-1 needs the DEL-09-01 protocol (not named by the SoW: S-0906-3) |
| REQ-007 OUT-003 needs an actual joined run | CA §8.1, §8.3, §8.4 W-R1…W-R7 | Developed (the rule) | Completion outstanding |
| REQ-008 excluded acts | CA §10 | Developed | — |
| AC/VER | VC-CA-01…VC-CA-11 (VC-CA-10 ran as a rehearsal) | Designed / rehearsal only | — |

### 3.2 Result → commitment

| Design element | Authority | Assessment |
|---|---|---|
| §2.6 option sheet (selects nothing; claims no join) | R12-6; DECISION-K1 Part 2; OUT-001 "decision/input account" | Supported |
| §8.4 W14 result record schema; §8.5 rehearsals on SH-1 | R12-1…R12-4; REQ-007, AC-007 (evidence content) | Supported. The SoW names no format. Pointer proposed (S-0906-2) |
| W14-08 observed behaviour on CA/E includes "each network destination the host's agent contacted (RS R15; V4-HI-70 as amended)" | V4-HI-70 as amended; REQ-002 "observed behavior … separately evidenced" | Supported as part of observed behaviour (DERIVED). The SoW is silent on destinations; optional S-0906-4 |
| ST-1 and UNRESOLVED rely on the "DEL-09-01 protocol" | Supplier-side row DEP-09-01-024 (admitted arc) | **Outside the SoW and the consumer register:** the DEL-09-06 SoW does not name DEL-09-01 (S1-F I-9). See S-0906-3, R-0906-3 |
| Use of SH-1 (C-v0.8 §10.8) and EXEC-v0.6 doubles | R12-4; DEP-09-06-027, DEP-09-06-013 | Supported. Register note proposed (R-0906-2) |

### 3.3 What the 60% description still lacks

- **A route to completion free of further structural change.** S1-E A.5
  names OI-021, the acting-surface variant and whether OUT-003 has a host
  side at all as choices that could restructure CA, and through it XT.
  They remain open. The option sheet prepares the OI-021 choice; it does not
  make it.
- **Rehearsal of the round trip itself:**
  - SH-1 has no workflow library, and there is no transfer-tracer double
    (EXEC §7.4). W14-01, -02, -09 and -10 are *not run* even on doubles;
  - SH-1 lacks the A4 control, the whole-model staleness profile, a
    non-durable de-duplication profile and undo (F-26).
- **Join keys** between the App run record and host evidence for W14-05/08
  beyond the capture-evidence reference (S1-E A.5). Also a mapping of
  SWBPIPE's identifiers onto them (S1-E C.5; B7 "not done").
- **The OUT-002 artifact.** It is not authored (later undertaking).

### 3.4 Register rows the Design files show to be stale or missing

- DEP-09-06-019: carries nothing of the option sheet's result (R-0906-1).
- DEP-09-06-027: does not name SH-1 (R-0906-2).
- No UPSTREAM row for DEL-09-01 (R-0906-3).
- DEP-09-06-015 RequiredMaturity is TBD against INITIALIZED in its mirror
  DEP-04-03-031 (R-0906-4). This is already an open matter in DAG-003
  HANDOFF_STATE.
- The relay handover is correctly DEP-09-06-033, and the DECISION-3
  constraint is DEP-09-06-034. CA and RELAY cite both.

### 3.5 The option sheet's consequence for DEL-09-06 (brief item)

**What CA §2.6 and F-25 state:**

- against SWBPIPE's answers of 2026-09-28, **0 of 10** steps are examinable
  now;
- the common blockers are B-1 (no identified SWBPIPE candidate), B-2 (the
  channel stays *not enabled*: no A13 facility), B-3 (host joins deferred;
  SWBPIPE names a development Codex as its caller), B-4 (no App candidate)
  and B-5 (no embedded loop for CA/E);
- CA-H also lacks a capture-evidence reference;
- "no row is examinable against SWBPIPE on its answers alone, whatever
  operation the owner selects";
- on SH-1, 9 of 10 are examinable (3 fully, 6 in part); the round trip is
  not.

**What follows (inference, checked against the SoW text):**

1. **No criterion changes.** REQ-007, AC-003 and VER-003 require an actual
   joined round trip. This closeout proposes no weakening, and a rehearsal
   never counts (CA §8.3, W-R1).
2. **TBD-003 (c) understates the gap.** It says only that the witness
   "cannot complete before" UI-SUCCESSOR resumes. On the answers, resuming is
   necessary but not enough. Several further SWBPIPE owner decisions or work
   items are also needed:
   - an identified candidate;
   - a workflow library or a work item to receive App workflows (SQ-17;
     ANS §4);
   - an act facility with a capture-evidence reference (SQ-01);
   - on the external channel, an A13 facility (SQ-28); or on CA/E, a host
     loop (SQ-20, SQ-29).

   S-0906-1 records this as a pointer, and R-0906-1 adds it to the register.
3. **OI-021 does not unblock it.** Selecting the operation (TBD-001) does
   not make any step examinable. The binding inputs are SWBPIPE owner
   decisions, outside App control (DECISION-3).
4. **Owner-level consequence (not a proposal).** OUT-003 cannot complete in
   the first increment unless those SWBPIPE decisions are made. Whether the
   owner accepts that standing, or seeks a scope change, is for the phase
   review. This closeout neither decides nor recommends.

### 3.6 Proposed ScopeOfWork changes (DEL-09-06)

| # | Locus | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| S-0906-1 | TBD-003 (c) | "(c) Host joins are deferred until the owner resumes SWBPIPE UI-SUCCESSOR (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3`); OUT-003's joined witness cannot complete before then." | Append: "SWBPIPE's answers of 2026-09-28 (`Design/RELAY_ANSWERS_SWBPIPE.md`; answers about its current state, not commitments) show that resumption alone does not make it completable. Set against those answers, no step of the designed activity is examinable against SWBPIPE (`Design/CONNECTED_ACTIVITY_CONTRACT.md` §2.6), whatever operation is selected under TBD-001. The joined witness also needs an identified host candidate, a host workflow library or work item to receive App workflows, a host act facility with a capture-evidence reference, and, on the external channel, an A13 enablement facility (on the embedded surface, a host loop). Each is a SWBPIPE owner decision." The point of need is unchanged | CA §2.6, F-25, §8.1, §4; B7 return; brief. A pointer; no criterion changes |
| S-0906-2 | OUT-003, after "…and received host evidence." | — | Add: "The per-case result record is drafted as a PROPOSED JSON Schema (`Design/w14-result-record.schema.json`) with conformance examples; it fixes meaning, not a selected form, and no rehearsal record counts toward this output." | B7 §6; R12-1, R12-2; CA §8.4 |
| S-0906-3 | CLM-003, after "App DEL-05-01 owns loop/model receiving requirements and App DEL-05-02 panel receiving requirements."; REQ-008 exclusion list | — | CLM-003 add: "App DEL-09-01 supplies reusable candidate-examination support and the evidence protocol (candidate, date and configuration identification; outcome states; replay, browser and native marking) that the joined witness uses." REQ-008 add: "; reusable examination support and evidence-protocol construction belong to App DEL-09-01 (CLM-003)" | S1-F I-9 ("DEL-09-06's SoW does not [name DEL-09-01]"); first increment R9-6-4; CA §6 ST-1, UNRESOLVED. Pairs with R-0906-3 |
| S-0906-4 (optional) | REQ-007, after "Record candidate, configuration/model versions/server and date;" | — | (a) Add: "on the embedded surface, the observed behavior includes each network destination the host's agent contacted, from the host run record (V4-HI-70 as amended by `SCA-V4-001`);" **or (b)** no change: REQ-002's "observed behavior" already covers the run record, and V4-EXM-23 stays with DEL-09-07 (CLM-006). This comparison finds (b) supportable | A1-E §4 item 7; CA W14-08 |

R-4 wording check: "checking" in CLM-005, REQ-004 and AC-004 names the
person's act. Both uses are consistent, so no change is proposed.

### 3.7 Proposed register changes (DEL-09-06)

| # | Change | Kind | Grounds |
|---|---|---|---|
| R-0906-1 | DEP-09-06-019 Notes, append: "Option sheet (CA-v0.6 §2.6, F-25): set against SWBPIPE's answers of 2026-09-28, 0 of 10 designed steps are examinable against SWBPIPE (blockers B-1…B-5; CA-H also lacks a capture-evidence reference); the round trip has no SWBPIPE counterpart (SQ-17). Data, not commitments; SatisfactionStatus unchanged." | Row edit (EXTERNAL) | CA §2.6; pairs with S-0906-1 |
| R-0906-2 | DEP-09-06-027 Notes, append: "Rehearsals of the W14 cases run on SH-1, the simulated host specified in C-v0.8 §10.8 (R12-4); test-double evidence only." | Row edit (admitted arc; unchanged) | B3 §6; CA §8.5 |
| R-0906-3 | New row: UPSTREAM INTERFACE, DELIVERABLE DEL-09-01, mirroring DEP-09-01-024 (reusable examination support and evidence interfaces). Evidence: the amended CLM-003 (S-0906-3) | Mirror only (arc DEL-09-06 → DEL-09-01 is admitted in DAG-003) | S1-F I-9; first increment R9-6-4; CA §11.1 row "DEL-09-01" |
| R-0906-4 | DEP-09-06-015 RequiredMaturity TBD; reconcile with DEP-04-03-031 (INITIALIZED) | Row edit | A1-E §4 item 3; DAG-003 HANDOFF_STATE open matter (owners: both register owners) |

### 3.8 Lifecycle observation

**IN_PROGRESS** is still truthful. CHECKING is not warranted:

- every output except OUT-004 is partial;
- OUT-003 cannot complete in this undertaking;
- OUT-002's artifact is unauthored.

No change is made here.

---

## 4. DEL-09-09 — External control and catalog-extension trace (XT-v0.6)

### 4.1 Commitment → result

| SoW item | Where XT-v0.6 answers it | Standing | What remains |
|---|---|---|---|
| OUT-001 V4-EXM-25 suite and candidate-bound evidence | §2 IN-01…IN-31; §3.1 J-1…J-8; §3.2 XC-00…XC-12; §3.3 completion rule and SQ-28 gate; §3.4 result record (PROPOSED schema); §3.5 run order, set-up and reset; §3.6 rehearsals (24 records on SH-1); §6.1 reopen table | **Partial** | All live cases are gated by A13 (SQ-28: no facility) and DECISION-3. No candidate. The engineer's A5 |
| OUT-002 V4-EXM-24 one-operation, three-channel trace | §4 (V-ED1; TS-0…TS-5; CMP-01…CMP-15; TR-01…TR-10) | **Partial** | The one new operation is not chosen (SQ-26). SWBPIPE has no H/E surface to compare (IN-22, IN-24), so at most two surfaces against the first host. TR-01 rehearsed on X only |
| OUT-003 work account and extension disposition | §5.1, §5.1.1 (tied to C-v0.8 §8 cell by cell; PROPOSED schema); §5.2 OI-003 record | **Partial** | OI-003 ruling. The V-ED1 account on SH-1 is test-double only |
| REQ-001…REQ-009 | §2, §8; XC-01, XC-10, XC-12; §3.3; XC-03…XC-08; §4; §5.2; XC-09; §3.4, §6; §7 (now names DEL-05-01, DEL-04-02 and DEL-02-03, the owners REQ-009 adds) | Developed | REQ-001's TBD range is stale in the SoW (S-0909-1) |
| AC/VER | VC-T-01…VC-T-12 (VC-T-11 ran as a rehearsal); VC-T-01 checks DEP-09-09-007…024, matching the register | Designed / rehearsal only | — |

### 4.2 Result → commitment

| Design element | Authority | Assessment |
|---|---|---|
| Result-record and work-account schemas; run order; reopen table | R12-1, R12-2; REQ-008, AC-008 | Supported. Pointer proposed (S-0909-2) |
| IN-30 host fixture set-up and reset (not asked) | REQ-001 ("receive the actual host contributions"); DEP-001 | Supported. The register row lacks it (R-0909-1). The relay owner must carry it (GW-2) |
| IN-31 per-surface compatibility report | DEP-09-09-023 | Supported |
| Rehearsals on SH-1 with ADAPTER's mapper | R12-4; DEP-09-09-007, -009 | Supported. Note proposed (R-0909-2) |

### 4.3 What the 60% description still lacks

- **The completion reading for SWBPIPE's act model.** How the §3.3 rule
  reads for a host whose A5 is a per-batch Apply with no A10 (F-18) has an
  owner and a point of need, but no option text.
- **Identifier mapping.** No mapping of SWBPIPE identifiers (`preview_ref`,
  `idempotency_key`, `ticket`, `basis_identity`) to J-2, J-3 and J-6 (S1-E
  C.5; B7 "not done").
- **A third surface.** The three-channel comparison has no H or E surface on
  SWBPIPE. Whether V4-EXM-24 can be met against the first host depends on
  OI-003 and OI-005, owner matters. No criterion change is proposed.
- **Open choices:**
  - DEL-03-03 TBD-007 (MCP or CLI family);
  - OI-003 (retain, narrow or defer the extension promise);
  - OI-021 (the traced operation).

  Per S1-E C.5, these could still restructure XC-02, XC-08 and §3.3.

### 4.4 Register rows the Design file shows to be stale or missing

- DEP-09-09-010 Notes still give OI-001/OI-002 the pre-ruling owner and
  point of need. The SoW TBD-002 now records D2/D3 (R-0909-3).
- DEP-09-09-014 lacks IN-30 (R-0909-1).
- DEP-09-09-007 lacks SH-1 (R-0909-2).
- DEP-09-09-021…024 are current.
- No DEL-09-09 → DEL-09-06 row exists, and none is proposed (guard E-1).

### 4.5 Proposed ScopeOfWork changes (DEL-09-09)

| # | Locus | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| S-0909-1 | REQ-001, second-to-last sentence | "Carry unresolved details at TBD-001 through TBD-004; independent definition proceeds while their dependent execution remains unclaimed." | "Carry unresolved details at TBD-001 through TBD-005; independent definition proceeds while their dependent execution remains unclaimed." | TBD-005 was added by SCA-V4-001 (AX-005). It carries the D4-1 phasing of XC-10, the A13 enablement-facility gate (SQ-28) and the DECISION-3 deferral, each an unresolved detail REQ-001 means to carry. A1-E §4 item 1; S1-E C.2 ("TBD-005 … never cited by ID"). Pointer correction; no scope change (brief item) |
| S-0909-2 | OUT-001, after "…including intervening edit and lost acknowledgment/interruption."; OUT-003, after "…its consequences." | — | OUT-001 add: "Its per-case result record is drafted as a PROPOSED JSON Schema (`Design/xt-result-record.schema.json`) with conformance examples." OUT-003 add: "The work account is drafted as a PROPOSED JSON Schema (`Design/xt-work-account.schema.json`). Each fixes meaning, not a selected form; no rehearsal record counts toward the witness." | B7 §6; R12-1, R12-2 |

R-4 wording check: "checking" in CLM-003, REQ-007 and AC-007 names the
person's act, and "non-mutating checks" (REQ-005) names host checks. Both
uses are consistent, so no change is proposed.

### 4.6 Proposed register changes (DEL-09-09)

| # | Change | Kind | Grounds |
|---|---|---|---|
| R-0909-1 | DEP-09-09-014 Statement, add to the list of host contributions: "fixture set-up and reset on the host candidate (the invented material loaded at a named revision in a fresh workspace, or a saved state restored, per suite segment; XT IN-30)" | Row edit (EXTERNAL) | B7 §6; XT IN-30, §3.5 SR-1/SR-2, F-26 |
| R-0909-2 | DEP-09-09-007 Notes, append: "Rehearsals run on SH-1, the simulated host specified in C-v0.8 §10.8 (R12-4); test-double evidence only." | Row edit (held arc; unchanged) | B3 §6; XT §3.6 |
| R-0909-3 | DEP-09-09-010 Notes: replace "OI-001 is owned by Owner with App/SWB contract owners before operation-policy production contracts; OI-002 by the same owner before permission-policy implementation." with "OI-001 and OI-002 are ruled for the first increment's App/shared contracts by APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2/D3 (SoW TBD-002); operation-specific additions remain under OI-021 (DEP-09-09-018) and host adoption under DEP-001." | Row edit (admitted arc; unchanged) | SoW TBD-002 as revised; DAG-003 HANDOFF_STATE OI-001/OI-002 consistency matter; C1-C |

### 4.7 Lifecycle observation

**IN_PROGRESS** is still truthful. CHECKING is not warranted: every output
is partial, and the witnesses are unrun. No change is made here.

---

## 5. Basis items (accepted basis docs; owner route)

| # | Item | Current text | Proposed | Grounds |
|---|---|---|---|---|
| B-1 (optional) | ARCHITECTURE §4 host-agent property, allow-list bullet | "the allow list works at two levels, a category switch (web access, MCP servers, other APIs, …) and named destinations within each category;" | Add after it: "a named destination is allowed on its own; a category switch allows everything in that category, and with it off only the named entries are allowed;" | DECISION-K1 K1-5 closed LOOP N-OPEN-4 by this rule. A1-D §4 item 7 asked that V4-HOST-02 and ARCH §4 "read alike once N-OPEN-4 is decided". The present texts do not contradict K1-5; this records it in the basis |
| B-2 (optional; owner, phase review) | V4-HI-70 / V4-HOST-02 as amended | Record "each network destination contacted"; V4-EXM-23 reports a decline to the agent | The owner decides whether declined and boundary-refused destination requests are also recorded. LOOP NW-13/NW-15, PANEL ND-4, AS and RS carry this as PROPOSED | R11-5; R12-10; V17b m-1; LOOP §5.1.1, §5.3 |

---

## 6. Work for the graph (not proposals)

| # | Item | Why it is graph work | Owner |
|---|---|---|---|
| **GW-1** | Define DEL-05-02's **panel receiving needs at the loop boundary** as one list, including FD-3's replay-from-ordinal request; update LOOP §10.3's "Panel needs" cell | **Required contribution, still missing.** ACTIVE row DEP-05-01-020 names it. R9-6 said to return it as a Wave B item. PANEL F-13 and the Receivers line still say "not yet defined". No Wave B node took it (B9 did return inputs only) | Graph maintainer; a PANEL production edit (with LOOP) |
| **GW-2** | RELAY UNRESOLVED, the next-relay row: add IN-30 (host fixture set-up and reset) | XT F-26 returned it "for the RELAY owner (DEL-09-06)". RELAY's list has four items and lacks it. A metadata-only edit; §0–§3 stay byte-identical | Graph maintainer |
| **GW-3** | Stale cells (residuals, not requirements) | Cells that describe superseded states: | Next in-place pass |
| | | - LOOP §10.1 Standing column and §10.3 "Standing at v0.7" (sibling labels v0.7, siblings now v0.8); | |
| | | - LOOP G-12 still says F-10 "needs DEL-04-03's statement", though F-10 cites RS §14.1 W-1/W-2 since RP-4; | |
| | | - PANEL VC-01 cites the consumed definitions at Wave A labels; | |
| | | - PANEL §7 preamble "The sibling v0.3 elements were confirmed by V2"; | |
| | | - CA body traces SOW-236/237/240/241 only in VC-CA-01 (AC-001). | |
| | | CA §5/§11.1 and XT §2 keep Wave A standing cells, but each file's preamble says so, so they are labelled, not false | |
| **GW-4** | LOOP G-4 / PANEL F-1: the independent pair check of LOOP and PANEL | Both files still say "retained". Partial coverage exists: V18-1 compared the joins, and V19-B and V19b reviewed parts of both files at the Wave B candidate. Whether that discharges the check is the graph maintainer's call; otherwise a review node. The files should then record it | Graph maintainer |
| GW-5 | V19b m-1 (run opening on no credential) | Done by C0 at `41899194c4` | — |

Next-pass design work (not missing required work for this run):

- the SWBPIPE identifier mapping for XT J-2/J-3/J-6 and the CA join keys;
- per-interaction sequences and a panel lifecycle in PANEL;
- SH-1 profiles (DEL-03-01's) and a transfer-tracer double (DEL-02-03's),
  which would let the round trip and the SWBPIPE-shaped profiles be
  rehearsed.

---

## 7. Collected items: index, deduplicated

**This run's items, counted:**

| Kind | Count | IDs |
|---|---|---|
| ScopeOfWork | 8 | S-0501-1; S-0502-1 (owner choice, options A/B); S-0906-1…S-0906-4 (S-0906-4 optional); S-0909-1, S-0909-2 |
| Register | 14 | R-0501-1…R-0501-5; R-0502-1, R-0502-2 (conditional on S-0502-1 A); R-0906-1…R-0906-4; R-0909-1…R-0909-3 |
| — of which new rows | 3 | R-0501-4 and R-0906-3 (mirror only, admitted arcs); R-0501-5 (EXTERNAL) |
| — of which new arcs | 0 | — |
| Basis | 2 | B-1, B-2 (both optional) |
| Graph work | 4 open (+1 done) | GW-1…GW-4 (GW-5 done by C0) |

**Duplicates merged:**

| Merged item | Sources |
|---|---|
| S-0502-1 | S1-D PANEL §2 item 5 and §4 item 13; A1-D §4 item 1; B5 §7; B9 §7; PANEL F-12; LOOP G-14; DECISIONS_DRAFT 19 |
| S-0909-1 | A1-E §4 item 1; S1-E C.2 |
| R-0501-4, R-0501-5 | A1-D §4 items 2–3; LOOP G-10, §10.3, §10.4; first increment R5-1-2/R5-1-3 |
| R-0906-3 | S1-F I-9; first increment R9-6-4 |
| R-0909-1 | B7 §6; XT IN-30, F-26 |
| R-0906-2, R-0909-2 | B3 §6 |

**Confirmations (no change):**

- **Cross-references stay unregistered.** CA keeps DEL-09-09, DEL-02-03,
  DEL-05-01, DEL-05-02 and DEL-04-03 as cross-references only. XT keeps
  DEL-09-06, DEL-03-03 and DEL-09-01 the same way. A row making any of the
  CA five consume DEL-09-06 would be an SCC-forming departure (guards E-1,
  K-6, K-7, K-11, E-5). Sources: A1-E §4 item 5; CA F-24; XT F-23.
- **DEP-09-07-011.** It names a selection that only OI-021 can supply (A1-E
  §4 item 6).
- **The model-interface boundary** (R12-11) needs no SoW change.
- **HANDOFF.** The "local-first" and DAG-001 wording (A1-E §4 item 8) was
  fixed at A2. HANDOFF line 22 now reads "on a model the person chooses,
  local or cloud, with no default".

**Carried from the first increment, unapplied, and not raised again in this
run:**

- R9-6-5 (DEL-09-06 DOWNSTREAM mirror to DEL-09-07);
- R9-9-4 (DEL-09-09 DOWNSTREAM mirror of DEP-03-01-030);
- DEL-09-06's SatisfactionStatus TBD/PENDING convention;
- optional supplier-side DOWNSTREAM mirrors for the consumers of DEL-05-01
  and DEL-05-02.

All four sit under DAG-003 HANDOFF_STATE open matters ("Deferred
supplier-side mirror rows (P2 O-3)"; "SatisfactionStatus TBD/PENDING
convention (P2 O-6)"), owned by the register owners. None is restated here.

**Seen here, owned by another closeout node (not counted):**

- **DEL-01-04 act-control obligation** (DECISION-K1 K1-4; A3 §4; B2 §6;
  CA W14-05 names it). This is C1-A's.
- **DEL-02-03 TBD range** (B2 §6). C1-A's.
- **RS R15 "each destination requested" text** (LOOP §3.2). A C1-A design
  residual.
- **DEL-03-01 items**: OUT-001 (external-contact declaration and destination
  request entry kind; B5 §7) and SH-1 custody (B3 §6). C1-B's.
- **DEP-03-04-022 widening** (A1-E §4 item 2; CA F-24). C1-B's.
- **A1-D §4 items 4, 5, 6 and 8.** DEL-01-01, DEL-02-01 and basis-header
  matters.
- **A shared examination-result form for DEL-09-01** (XT F-28). Outside the
  increment.

---

## 8. Checks performed

- **Candidate reads.** Every Design file was read from `a9046631c0` with
  `git show` into scratch and hashed (table above). Only LOOP differs from
  the working tree (C0, later committed at `41899194c4`). Its diff touches
  §3.1 F-2 and §3.2 only.
- **What was read.**
  - CA, the SoWs, the registers, `_DEPENDENCIES.md`, `_STATUS.md` and
    `MEMORY.md`: whole, the registers parsed by script.
  - LOOP: header, change tables, §3.1–§3.2, §10–§13, Findings, UNRESOLVED
    and the VCs, plus the body sections by grep.
  - PANEL: header, change tables, §3.8–§3.10, §6–§7.1, Findings, UNRESOLVED
    and the VCs.
  - XT: header, §2, §3.3, §3.6, §7–§9, change table, UNRESOLVED and the VCs.
  - RELAY: header, UNRESOLVED and the VCs.
- **RELAY relayed body.** The span from `## 0.` to `## 4.` hashes to
  `6e399c8389dc2ad9…`, as RELAY states.
- **Prototypes rerun** on 2026-09-30 (Python 3, standard library,
  `PYTHONDONTWRITEBYTECODE=1`, output under `$TMPDIR`). `git status` was
  identical before and after.

  | Prototype | Result |
  |---|---|
  | LOOP `assemble_tool_calls.py` | 22/22 as expected |
  | `LOOP_TOOL_CALL` examples | VALID / INVALID as intended |
  | LOOP `destination_flow.py` | "RESULT: all expectations held"; 68 RS entries and 11 request records validated |
  | `LOOP_DESTINATION_REQUEST` examples | VALID / INVALID as intended |
  | PANEL `panel_double.py` | 4/4 |
  | `PANEL_RETURN_INPUT` examples | VALID / INVALID as intended |
  | CA `run_w14_rehearsals.py --out` | "ALL CHECKS HOLD: 0 failure(s)" |
  | XT `run_xt_suite.py --out` | "ALL CHECKS HOLD: 0 failure(s)" |

- **Arc classification.** Checked against DAG-003. DEP-01-05-014
  (DEL-05-01 → DEL-01-05) and DEP-09-01-024 (DEL-09-06 → DEL-09-01) are
  admitted (`DependencyEdges.csv`). DEP-05-02-010, DEP-05-02-019 and
  DEP-05-01-020 are held (`CandidateEdges.csv`).
- **Quotes.** Every quoted SoW and register text was copied from the
  candidate files: DEL-09-09 REQ-001 line 66; DEL-09-06 TBD-003; DEL-05-02
  CLM-002; DEP-09-09-010 Notes; DEP-05-02-005…010, -019 Statements.
  OWNER_ITEMS O-15 was read in `APP-V4-BASIS-ALIGN-20260928/AMENDMENT_PACKET/OWNER_ITEMS.md`.
- **Inferences.** Where a statement is an inference, it is marked
  ("Inference", "advice"). Nothing here claims a SWBPIPE join, witness,
  commitment or adoption. No proposal is applied.
