# S1-C — scoping survey: DEL-09-05, DEL-09-07, DEL-09-11

- Node: S1-C of run `APP-V4-DESIGN-PASS-4-20261003` (Type 2 TASK, Claude Opus 5.5, high effort). Read-only on project state; this file is the only write.
- Brief: `BRIEFS.md` (sha256 prefix `3fe0abc84d6abe2e`), "Common rules" and "S1 — scoping survey". Owner record: `OWNER_DECISIONS.md` (`0883eb7d8b88be7c`).
- Paths are relative to `projects/chirality-app-v4/execution` unless they start with `docs/` (= `projects/chirality-app-v4/docs/`).
- **How observed.** Files were read directly. Register rows, DAG-004 arcs and SCA-V4-003 ledger rows were filtered by script over the CSVs (Python `csv`). Counts below were taken by `grep` over each `ScopeOfWork.md`. SoW and register hashes were recomputed with `shasum -a 256` and match the hashes DAG-004 and the run records bind: DEL-09-05 SoW `35c8ea5ae68d6568`, register `eeb2059436caa01f`; DEL-09-07 SoW `813ef0f3ebcbc000`, register `9010b0aa3e1c7d1e`; DEL-09-11 SoW `e4ee1a5779af66fe`, register `ccc0817502711be6`. Basis documents were read at `docs/PRD.md` `bb6e786f7a6c01dc`, `docs/EXAMINATION.md` `471798bc2f2dc020`, `docs/HOST_INTEGRATION.md` `d4331c39db7f452c` and `docs/ARCHITECTURE.md` `317d5789272c5206`, the pins the first-increment Design files carry.
- **Labels.** *States* means a file says it. *Inference* marks this survey's own reading. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` (`afb6e063e7e5dfcc`) is cited as data about SWBPIPE's state, never as a commitment or join. No SWBPIPE join, witness or adoption is claimed.
- **Amendment history of the three contracts** (`git log`). DEL-09-05 and DEL-09-11 are the INIT contracts of 2026-09-27; no amendment revised them. DEL-09-07 was revised under SCA-V4-001 (AX-004) and SCA-V4-002 (AX-005). SCA-V4-003 touched none of the three.

---

## Part A — DEL-09-05 Fleet coordination and longer-work recovery witness

TEST_SUITE. Owner: App fleet integration owner with an independent examiner. Scope SOW-198, SOW-243; objectives OBJ-006, OBJ-008. It joins App-side contributions only; **no host is involved** (V4-EXM-13 is an App scenario), so DECISION-3's deferral of host joins does not reach it.

### A1. Obligations (2 OUT, 6 REQ, 7 AC, 7 VER; also 3 CLM, 3 AX, 5 TBD)

| ID | One line | Rests on |
|---|---|---|
| OUT-001 | TEST: bounded V4-EXM-13 fixture (two delegations, work graph, queue, one decision, interruption) on an identified candidate | EXM V4-EXM-13 (unamended); PRD V4-PM-01…06 |
| OUT-002 | DOC: joined return/review/worker/ownership/pending-choice evidence, outcomes, independent findings, limits of first-host and conversation-only evidence | EXM §§1–2, V4-EXM-13; ARCH §3 recovery properties |
| REQ-001 | Two bounded delegations, graph, queue, one decision from an exact-act package; briefs carry the V4-PM-01 fields | V4-PM-01…04; V4-EXM-13 |
| REQ-002 | Dependent and independent ready work, a return awaiting review, actual worker ownership, changed basis, interrupted review/integration; rebuilt state distinguishes executing/returned/reviewed/integrated, active descendants, findings, pending choices, waiting causes | V4-EXM-13; ARCH §3 ("Conversation recovery alone does not establish recovery of a branching undertaking…"); HTML decision 05 |
| REQ-003 | Graph and coordination records stay files; views rebuild; views never authority; unknowns kept; basis change exposed against affected judgments | V4-PM-02…06; V4-EXE-03; V4-OPS-02 |
| REQ-004 | Execution, checking, acceptance, approval and reliance kept apart; faithful recording allowed; no attribution from tool success, a return, silence or timeout; no invented ordering | V4-AUT-03…05; V4-EXE-02; HTML decision 03 |
| REQ-005 | Each outcome binds candidate, configuration, date and standing; evidence names actual worker mechanism and parentage, supplied basis, scopes, enforced vs instructional limits, returns; changed candidates reopen checks; a first-host pass or conversation recovery does not claim this coverage | V4-EXM-01/03/05; V4-OPS-30…34 |
| REQ-006 | Performs no act owned by DEL-06-01, 06-02, 01-03, 04-01, 04-03, 09-01, 09-11, 09-12, 11-03 or SWBPIPE | CLM-001…003 |
| AC-001…AC-007 | Two delegations and one decision with real child execution (AC-001); every REQ-002 condition observable through the basis change and interruption (AC-002); file-derived reconstruction with unknowns kept (AC-003); actor ≠ recorder and no unsupported attribution (AC-004); candidate/worker/basis account with reopened checks (AC-005); coverage beyond first-host, conversation, file-native and component evidence (AC-006); owners and open choices at their points of need (AC-007) | As REQ-001…006 |
| VER-001…VER-007 | One VER per AC, in the same order. VER-001 links actual launches and returns rather than inferring them from briefs; VER-002 observes before, interruption and resumption states; VER-003 rebuilds views across sessions and compares with retained evidence; VER-004 compares the observed decision with its record; VER-005 independent examination with criterion protection; VER-006 coverage comparison; VER-007 ownership/open-input account | As above |

**Overtaken or lagging text** (inference; the SoW is the unrevised INIT contract):

- **TBD-002** says OI-001 and OI-002 "remain OPEN". Both were ruled for App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3. `Open_Issues.csv` keeps status OPEN with those rulings in the Consequence column. Same pattern as DEL-09-02's OI-009 item the owner carried ("1 yes").
- **TBD-003** says "No supplier version is selected here". D4 selected 0.158.0 as the definition and generation pin; the qualification pin stays under OI-012. The 0.160.0 version-advance check (node VC) is running now.
- **The decision package's act.** REQ-001/AC-004 need "one exact-act decision package". DEL-04-01 ACT-POLICY-v0.9 §2.1 lists "reserved coordination decisions (V4-PM-04)" among acts that have **no canonical name** (lines 348–353). RS-v0.9 §3 defines human-act records for A4, A5, A6, A7, A10, A12, A13, A15 (and A11) only. DEL-01-04 AAC-v0.2 (the App act control, in DEL-01-04's contract since SCA-V4-003 Q-5) covers App-content acts and A15. No file names the act kind, capturing surface or record kind for this decision. See Part D, S-1.
- **K1-4, K-10, L-2, K-4** bear on the fixture though the SoW predates them: the person's identity is recorded "identity not verified" (K1-4); a task agent's delegation is "stated, not enforced" and recorded (K-10); a conversation's role is fixed for its life, a different role is a new conversation (L-2); quitting with live work asks first and records "interrupted by quit" (K-4).

### A2. Joins

Admitted arcs in DAG-004 (`DependencyEdges.csv`), all consumer → supplier with DEL-09-05's own UPSTREAM row as representative (SR-6), RequiredMaturity INITIALIZED, SatisfactionStatus TBD:

| Row | Supplier | Supplier's mirror (MIRROR in DAG-004) | Supplier Design |
|---|---|---|---|
| DEP-09-05-006 | DEL-06-01 | DEP-06-01-010 | none yet (tranche 1, S1-A) |
| DEP-09-05-007 | DEL-06-02 | DEP-06-02-011 | none yet (tranche 1, S1-A) |
| DEP-09-05-008 | DEL-01-03 | DEP-01-03-021 (added by SCA-V4-003 R3-01-03-a…c) | NPTD-v0.2 (pass 3) |
| DEP-09-05-009 | DEL-04-01 | **none** (ACT §10.3 row: "none") | ACT-POLICY-v0.9 (first increment) |
| DEP-09-05-010 | DEL-04-03 | DEP-04-03-044 (added by SCA-V4-003 RP1-MX-0403) | RS-v0.9 (first increment) |
| DEP-09-05-011 | DEL-09-01 | DEP-09-01-023 | none yet (tranche 1, S1-B) |

Non-topological (EXTERNAL, SR-2): DEP-09-05-012 (the human decision actor for VER-004), DEP-09-05-013 (DEP-005 supplier pin and environment). No held arc and no downstream consumer. No row to DEL-09-11, DEL-09-12, DEL-11-03 or SWBPIPE (the register's run notes say none was inferred).

What the Design files already assume of DEL-09-05:

- **DEL-01-03 NPTD-v0.2** (`6eed39dcee4acf4b`). Header "Receivers": "DEL-09-02 via DEP-09-02-011 and DEL-09-05 via DEP-09-05-008 (both admitted): fixtures, designed cases and the descendant presentation (§15)". §10.2 Offered: "fixtures and designed cases | DEL-09-02, DEL-09-05 | §15". §7.3 DR-2: "Parent completion says nothing about children … return, review and integration are never inferred." §7.6: "DEL-01-03 exports; it imports nothing from PKG-06 … and adds no fleet feature". §15.2 NV-04 "Primary completed, descendant active" is **not observed** ("OBS-2's parent waited for its child"); U-P4 holds the child-interrupt and NV-04 observation open. §7.1 and F-9: delegation is unavailable on stock LM Studio 0.4.16 (namespace tools dropped); delegation was observed only "through an adapter (OBS-2), not stock behaviour".
- **DEL-04-03 RS-v0.9** (`a91882e74064495c`). §10 row: "DEL-09-05 (node G; DEP-09-05-010) | The decision and run formats and App recording for its joined witness … §6 (actor ≠ recorder; capture evidence), §7 (content binding and lapse), §3 (separate acts and standings kept apart) | — | Not covered by this undertaking (D1); stated from the register row only". §10 PKG-06 row: "Act records; actor ≠ recorder; lapse | Decision records as act subjects | Coordination recorder never becomes actor". §10.1 lists DEL-09-05 as admitted, "added at node G … outside D1".
- **DEL-04-01 ACT-POLICY-v0.9.** §10.3: "DEL-09-05 | DEP-09-05-009 | none | Not mapped in detail". §2.1 closing list as quoted above.
- **DEL-01-02 RECOVERY-v0.2** §0 "What this file does not contain": "recovery of a branching undertaking (REQ-006 forbids the claim; PKG-06, DEL-09-05)". Its custody events (`request_ended_unanswered`, `acknowledgment_not_observed`, `app_restart_interruption`, `observation_lost`/`observation_recovered`; RS §10 row DEL-01-02) are the evidence an interruption case can observe.
- **DEL-09-06 CA-v0.7** (`eb133d4101ea5013`) §6 rules: "A first-host pass is not evidence of longer-work recovery (DEL-09-05)." §10: longer-work recovery excluded, owner DEL-09-05.
- **Pass-2/3 closeouts.** P2 C1-A G-3 and RS §10.1 record that DEL-09-05's consumption of DEL-04-03 was "not yet stated" and was added at node G; SCA-V4-003 applied the receivers sentence and the mirror rows.

### A3. Proposed contract changes still open

No SCA-V4-003 DEFER or carried item names DEL-09-05 (`LEDGER.csv` `e28661cdf3375e15`: the five rows naming it, SC2-04-03-1, SC3-01-03-8, R3-01-03-a…c, RP1-MX-0403, are INCLUDE and applied; checked against the live registers). The closure audit (`ScopeClosure_SCA-V4-003_2026-10-03_2028`) raises nothing on it. Open candidates for a later amendment (inference): TBD-002/TBD-003 wording (A1), and a mirror row DEL-04-01 → DEL-09-05 (no graph effect).

### A4. Open items and owner choices

| Item | Shapes design now? | Options and what the files say | Owner? |
|---|---|---|---|
| **Act kind and capture of the one decision** (V4-PM-04; ACT §2.1; RS §3) | **Yes**: VER-004's positive and negative cases, the record compared, and which surface captures | (a) new canonical act kind (as R12-5 added A15) captured by DEL-01-04's act control and recorded under RS §6; (b) map the decision onto an existing kind; (c) record the decision as a coordination record that is not a human-act record. No file chooses | Integrator ruling could add a name (precedent R12-5); **owner** if it changes which coordination decisions are reserved to the person (D2 did not cover them) |
| **Delegation mechanism of the two delegations** (DEL-06-01 OUT-002 "native-delegation association"; L-2; Root AGENTS.md D-GOV-35) | **Yes**: worker identity, parentage evidence, interruption cases | Native Codex children (NPTD §7.2 identity model), separate TASK-role conversations the App starts (L-2: a different role is a new conversation), or both. DEL-06-01's design decides (S1-A) | Probably not; DEL-06-01 design. Owner only if it reopens L-2 or K-10 |
| Model route for the live witness | No (execution environment only) | At 0.158.0 delegation needs `namespace` tools; stock LM Studio drops them (NPTD F-9). A live witness needs a cloud model by sign-in or a namespace-capable route. L-6: "no sign-in or API-key observation now" | **Owner**, at execution |
| TBD-001 OI-006 further fleet scope | No (option B carried) | Open with Owner, "During FEED before corresponding production contracts" | Owner, later |
| TBD-002 OI-001/002 | No for design (ruled D2/D3); wording lags | Carry wording to next amendment or read as ruled | Owner (wording, low) |
| TBD-003 OI-012 pin | Little (fixtures name their version) | 0.158.0 definition pin; VC check of 0.160.0 running | No |
| TBD-004 OI-005 / OI-021 | No (no host in V4-EXM-13) | — | No |
| TBD-005 OI-016 validation period | No | Validation ≠ this verification | No |
| Kinds of interruption to include | Yes (case list) | Window close, App relaunch, quit (K-4), Codex exit with an active child (NPTD SQ-3), observation loss (RECOVERY custody events) | No (design) |

### A5. What exists to build on

- **Supplier facts at 0.158.0** (read in the committed bundle `DEL-01-01/Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json`, sha256 `34f28a48…f458`, by script): `Thread` carries `parentThreadId`, `agentNickname`, `agentRole`, `forkedFromId`, `source`, `status`; item `collabAgentToolCall` carries `senderThreadId`, `receiverThreadIds`, `agentsStates`, `prompt`, `model`, `status`; item `subAgentActivity` carries `agentThreadId`, `agentPath`, `kind`. OBS-2 (via NPTD §7.2, §7.4): children are not in `thread/list`, are readable by `thread/read`, frames arrive on the same connection; a TASK-guided parent delegated and every call was recorded (O-4b, adapter). The TS output folder HOSTING names in the session scratchpad exists in this session but its generation folders are empty (checked with `find`); the committed JSON bundle is the readable source.
- **First-increment and pass-3 contributions:** NPTD §7 (availability, identity model, display rules, states), §7.7 delegation export schema, §12 SQ-3/SQ-4/SQ-8, §15 NV-04/NV-05 and its prototype (18/18 constructed cases, "passes no VER criterion"); RS §3, §6, §7, §13–§14 and its example JSONL files; RECOVERY custody events; ACT §2.1 act table; EXEC §4.12 RP-1…RP-8 recovery rules.
- **The repository's own file-native practice** (AgentRuns briefs, DISPATCH records, WorkGraphs, this run): live evidence of the method, which REQ-005 says is not product execution evidence.
- **App v3 exemplar** (`projects/chirality-app-dev`; evidence only, never a v4 commitment): `frontend/src/lib/harness/managed-delegation.ts` (Chirality-managed `delegate_agent` with orchestration records `chirality-agent-runs/v2`, return markers, update/acknowledgment events, versioned replans); `subagent-bridge.ts` (the SDK sub-agent tool kept disabled after managed delegation, "D-APP-10 Option C"); `mcp/coordination-tools.ts`; v3 PRD lines 1595–1612 ("preserve the initial plus amended work graphs for restart reconstruction"; "Parent and child sessions retain reconstructible lifecycle, output, and coordination evidence"); v3 CONTRACT K-SUBAGENT-3; a selected-session replay lens test.

### A6. Design scope for this pass (to the 60% level)

1. `Design/FLEET_WITNESS.md` — the fixture FX-FLEET-01 on invented material: an undertaking graph with one independent ready contribution, one dependent contribution waiting on the other's return, an integration step and one decision node; the two briefs field by field against V4-PM-01 (by label against DEL-06-01's record definitions, tranche 1).
2. The witness state model: planned, launched, executing (last observed, sourced), returned, awaiting review, reviewed, integrated, waiting by cause, pending decision, decided, unknown; which source evidences each state (native frames from DEL-01-03, files from DEL-06-01, views from DEL-06-02, records from DEL-04-03, custody events from DEL-01-02), and the transitions an observation may and may not cause (DR-2 style rules).
3. Operating sequence with interruption and basis-change points (window close, quit per K-4, App relaunch, Codex exit with an active child, observation loss; basis change during review and during integration), each with the expected rebuilt state and failure behaviour.
4. The decision case: the exact-act package, the performed act, the record compared (actor ≠ recorder, content binding, lapse), and negative attribution cases (tool success, return arrival, silence, timeout). Its act kind is written as `UNRESOLVED` until S-1 is ruled.
5. The joined result record per VER, consuming DEL-09-01's evidence protocol (tranche 1; DEL-09-06's `w14-result-record.schema.json` is a precedent), plus an expected-state oracle schema and a local prototype on constructed inputs (test-double standing).
6. The coverage and ownership account (VER-006/VER-007): what this witness adds beyond first-host, conversation-only, file-native and component evidence; each excluded act with its owner.

Leave out: fleet product features (OI-006), staffing, duration or throughput numbers (AX-003), PEC adoption, any live run (no App candidate exists), and the delegation mechanism itself (DEL-06-01's).

---

## Part B — DEL-09-07 Local host candidate qualification

TEST_SUITE plus dossier. Owner: App connected-activity examination owner; the external SWB owner supplies execution, traffic and receipts; an independent examiner checks the dossier. Scope SOW-199, 200, 201, 202 (as amended by SCA-V4-001), 239; objectives OBJ-004, 005, 008, 009. **Host joins stay deferred (DECISION-3 of `APP-V4-SWBPIPE-INTAKE-20260928`).** The SoW itself says "Definition is possible before the live witness is available; definition alone does not qualify the candidate."

### B1. Obligations (2 OUT, 9 REQ, 8 AC, 8 VER; also 5 CLM, 5 AX, 3 TBD)

| ID | One line | Rests on (amended where noted) |
|---|---|---|
| OUT-001 | Candidate-specific cases for V4-EXM-20/21/22/23 | EXM §4 (V4-EXM-22/23 amended by SCA-V4-001) |
| OUT-002 | One durable dossier linking cases, basis, rows, solve, checks, policy, traffic, origins/undo, receipts, human acts; supplies DEL-11-03 | HI-70 (amended)/71; EXM §§2, 4, 7 |
| REQ-001 | Identify App/host candidate, date, configuration, harness/model versions, local model server, adopted policy, external contribution received and its standing, agreed activity | V4-EXM-01/03; HI §11; CLM-004 |
| REQ-002 | V4-EXM-20: invented piping model; catalog reads; proposal; per-row review with old/new values; some rows accepted individually, one rejected; application; solve; objects, reasons, origins, receipts. Operation via TBD-001 | V4-EXM-20; HI-20…25 |
| REQ-003 | Original read basis (workspace identity, generation, model revision, content hash) through intervening edit, stale refusal, redraft, application, receipt recovery; no retargeting; unknown stays unknown | SOW-239; HI-11/21/23/25/70/71 |
| REQ-004 | V4-EXM-21: findings by reference, no table mutation; never a Checked/approval/certification; faithful recording of actual acts permitted | V4-EXM-21; HI-10…12/31/32; AUT-03/05; REC-05 |
| REQ-005 | V4-EXM-22 (amended): one low-consequence class direct with origin/undo; geometry as proposals; per-class setting visible and recorded; checkpoint act requested and recorded only when performed; hold examined only for a governance-phase workflow | V4-EXM-22, V4-WF-05, V4-HI-42 (all amended SCA-V4-001); DECISION-4 D4-1 |
| REQ-006 | V4-EXM-23 (amended): all host traffic observed; only the selected model service and allowed destinations; decline reaches nothing and is reported "destination not allowed by the person"; nothing else unless turned on; every destination recorded and shown; actual native enforcement evidence; no schema/mock/browser/selected-log substitute | V4-HOST-02, V4-ARC-12, V4-EXM-23 (amended SCA-V4-001); DECISION-5 |
| REQ-007 | Dossier joins requested operations, authority, bases, outcomes, decision actors, recorder, origins, receipts by reference; workflow/version, conversation, autonomy, model; lapse; positive and negative records distinguishable | HI-31…33/70/71; REC-01…05 |
| REQ-008 | Standings passed/failed/blocked/not run/inconclusive; replay where possible; WebKit, Chromium and packaged smoke; V4-EXM-20 must pass live on the identified App and SWBPIPE candidate with a local model | EXM V4-EXM-01…05, §7; PRD V4-REP-01; OI-015 |
| REQ-009 | Performs no act of DEL-09-06, DEL-11-03, the owner, SWB, PKG-02…05 feature owners, policy owners, the person | CLM-001…005 |
| AC-001…AC-008 | Candidate/activity/open-choice identification (AC-001); completed live V4-EXM-20 (AC-002); basis-to-receipt trace (AC-003); V4-EXM-21 (AC-004); V4-EXM-22 (AC-005); V4-EXM-23 with native enforcement evidence (AC-006); independently examined dossier usable by DEL-11-03 (AC-007); act/owner account (AC-008) | As REQ |
| VER-001…VER-008 | One per AC in order; VER-006 compares every observed destination with the selected service, allow list, in-work grants and the destination record; VER-007 is "not the separate week-later V4-EXM-31 assignment" | As REQ |

**Overtaken or carried items** (inference unless a file is named):

- TBD-002/TBD-003 already carry D2/D3 (revised by SCA-V4-002). No lag there.
- **SCA-V4-003 DEFER rows that bear on REQ-006/AC-006 without naming DEL-09-07:** SC2-04-01-2 and R2-04-01-b (the DECISION-5 destination grant as an A12 subclass; condition "owner confirms the A12 mapping" not met); S-0502-1 and R-0502-2 (panel destination rules and displays; option B stands); P2-C1-C-B-1 (the K1-5 allow-list rule into the basis); P2-C1-C-B-2 (whether a boundary refusal the loop makes without asking is recorded; R12-10 keeps it PROPOSED). Note: ACT-POLICY-v0.9 §2.1 already lists A12's "network-destination grant" subclass (R8-13) in its own text; the DEFER concerns the contract wording.
- **S-01-4 (DEFER):** a read whose host declares no workspace identity or generation ("basis lineage not supplied") against DEL-03-01's protected AC-004. REQ-003 defines read basis with all four elements; SWBPIPE main has no workspace identity or generation (SQ-07 (a)); DRAFT #885 has them. Point of need is the host join.
- **S-0906-4 (DROP), names DEL-09-07:** "V4-EXM-23 sits with DEL-09-07" was the reason for dropping the DEL-09-06 destination wording.
- **R9-6-5 (carried since the first increment, unapplied, not in the SCA-V4-003 ledger):** a DEL-09-06 DOWNSTREAM mirror to DEL-09-07 (P2 C1-C §7). No graph effect.
- **Missing receivers statement (inference).** DEL-09-11 consumes DEL-09-07 (DEP-09-11-006, admitted), but DEL-09-07's SoW names only DEL-11-03 as receiver and its register has no row to DEL-09-11.

### B2. Joins

| Row | Direction / other end | DAG-004 | Notes |
|---|---|---|---|
| DEP-09-07-011 | UPSTREAM → DEL-09-06 (PREREQUISITE) | admitted | the agreed activity and round trip; "selected useful operation, permitted autonomy and exact candidate environment" (OI-021) |
| DEP-09-01-025 (DEL-09-01's row) | DEL-09-01 → DEL-09-07 HANDOVER | admitted (representative) | DEL-09-07 has no UPSTREAM row of its own to DEL-09-01 |
| DEP-11-03-007 (DEL-11-03's row) / DEP-09-07-025 (MIRROR) | DEL-11-03 consumes DEL-09-07 | admitted | the joined dossier for one live local-model journey |
| DEP-09-11-006 (DEL-09-11's row) | DEL-09-11 consumes DEL-09-07 | admitted | no mirror on DEL-09-07's side |
| DEP-09-07-012…015 | UPSTREAM → PKG-02, 03, 04, 05 (INTERFACE) | NOT_TOPOLOGICAL (package) | contracts consumed by package, not by deliverable |
| DEP-09-07-016…024 | EXTERNAL: DEP-001; the App/SWBPIPE candidate and local model; the person's row decisions; the engineer-edited model; the adopted autonomy policy; the checkpoint act; OI-001; OI-002; the independent examiner | NOT_TOPOLOGICAL | inputs at their own points of need |

DAG-004 HANDOFF_STATE (`3c374f5e9fa4cfaa`): DEL-09-07 is among the ten deliverables that reach the four new SCC-002 consumers through admitted arcs; "the new arcs add paths, not suppliers". DEL-09-06's guard: DEL-09-06 "is consumed only by DEL-03-04 and DEL-09-07"; a row making DEL-09-06 consume DEL-09-07 would be an SCC-forming departure.

What the Design files assume of DEL-09-07:

- **DEL-09-06 CA-v0.7.** §2.2: variant **CA/E** (the host's embedded agent through the minimal loop) has examination owner "DEL-09-07 (V4-EXM-20…23)"; "SWBPIPE has no live agent and no embedded loop exists or is selected, so CA/E has no SWBPIPE counterpart now". §5: DEL-09-07 is the joined check owner for C (DEL-03-01), P (DEL-03-02), AS grant display "(V4-EXM-22)", LOOP and PANEL receiving; "Local host qualification V4-EXM-20…23 | DEL-09-07 | … **Not in this undertaking (D1)**". §6 ST-4: "V4-EXM-20…23 by DEL-09-07 … ST-4 cannot start against SWBPIPE as its answers stand; host joins are deferred (DECISION-3)". §8.3: "A test-double run, a recorded replay, or a DEL-09-07/09-09 component pass" cannot substitute for the V4-EXM-14 witness. §11.2: "DEL-09-07 | DEP-09-07-011 | Step map §2.3 for CA/E; staging §6; evidence ladder §7 … not yet defined here (`UNRESOLVED{OI-021}`)". UNRESOLVED: "DEL-09-07 local qualification (outside D1) | Their owners | Before candidate-bound results". §2.3–§2.6 give the step map CA-0…CA-R, failure rows CAF-1…CAF-39, the FX-PIPE-01 sequence with the graduated-autonomy branch (V4-EXM-22 overlap, W14-04), and the option sheet: "Against SWBPIPE now: 0 of 10 rows are examinable … On SH-1: 9 of 10".
- **DEL-09-06 RELAY_QUESTIONS** SQ-30 "Endpoint and key boundary in the host's native layer": the V4-EXM-23 observation is "(DEL-09-07, outside this undertaking)".
- **DEL-03-04 GUIDE** HC-7.3 (native layer enforces the endpoint, holds the credential, refuses redirects) and HC-7.9 (MCP and outside processes, record and show): both name "V4-EXM-23 observation (DEL-09-07, outside D1)".
- **DEL-05-01 LOOP-v0.9** §5.1.1 NW-1…NW-16 and §5.2 MS-14…MS-23 "cite the amended V4-EXM-23"; §5.3 the destination flow; R11-5 / R12-10: recording the person's decline is SETTLED (RS CLM-004), a refusal without asking stays PROPOSED; NW-16's limit "process network not observed" for an unsandboxed outside process. UNRESOLVED: "DEP-001 … All host conformance NOT-OBSERVED".
- **DEL-05-02 PANEL** §3.3 ("Proposed items appear in host tables as proposed (V4-EXM-20)"), §3.8 ND-4 and PC-30…PC-37 (destinations shown; V4-EXM-23), §4 H-3 (V4-EXM-21), VC-02.
- **DEL-03-01 C** §4.1 "Destination not allowed by the person" (wording SETTLED by DECISION-5 and V4-EXM-23); U-C5 findings location and U-C10 non-mutating basis handling, both "Before V4-EXM-21 binding"; §10.8 the simulated host SH-1.
- **DEL-03-02 P** §4.3 item-level acceptance (V4-EXM-20); **DEL-04-01 ACT** §5.4 grant value *propose* "as in V4-EXM-22", VC-011 traced to V4-EXM-23; **DEL-04-03 RS** R15 destination entries, §10 external host run recording row; **DEL-09-09 XT** F-8 "V4-EXM-25 and V4-EXM-24 comparison overlap | Unchanged; noted for DEL-09-07".
- **First-increment R4** (`R4_RESOLUTIONS.md` line 154): "Out-of-scope receivers: DEL-02-02, DEL-09-01, DEL-09-07 (D1)".

### B3. Proposed contract changes still open

None of the ten SCA-V4-003 DEFER rows names DEL-09-07; the bearing DEFERs and the carried R9-6-5 are listed in B1. The closure audit raises nothing on DEL-09-07.

### B4. Open items and owner choices (what can be designed without the host joins)

| Item | Shapes design now? | Options and what the files say | Owner? |
|---|---|---|---|
| **TBD-001 / OI-021**: useful operation, permitted autonomy class, candidate environment (CA DI-1…DI-3) | **Partly**: case steps take an operation parameter; FX-PIPE-01 "add supports, adjust a run" is the proposed fixture; V4-EXM-22's "one low-consequence class" | SWBPIPE candidates (data): 27 change kinds on main; Node `position.x` set_field on DRAFT #885 (CA/X, not CA/E); checks: validate-only preview, solve with integrity standing, rule checks. CA §2.5: "Stays open (R8-10)". | Owner via the outside SWB session, at the execution point; not needed to design |
| **Embedded route availability** (SQ-20, SQ-29: no loop, no model interface; D-58 successor; DECISION-4 D4-2) | No (DEL-09-07 is CA/E by definition) | Decides *when* V4-EXM-20 can run, not its design. SWBPIPE records name a development Codex over the CLI first, an embedded agent later | Owner as SWBPIPE owner, when UI-SUCCESSOR resumes |
| **V4-EXM-23 observation method and privilege** | **Yes**: VER-006's completeness argument, observation boundary, process attribution | OBS-1 used 250 ms socket snapshots, Codex logs and the kernel sandbox log, and missed a ~30 ms process (OBS-1 B.5). Packet-level capture or a packet filter log on macOS needs administrator rights. Inference: the design should name the method, its blind spots and the privileges it needs; the person grants or runs the privileged part | Design choice; **owner's permission** for any privileged capture at execution |
| A12 mapping of destination grants; recording boundary refusals (DEFERs above) | Partly (which grant and decline evidence VER-006 expects) | Confirm the mapping (SC2-04-01-2 include) or keep it deferred; boundary refusal recorded or not | **Owner** (A12 mapping); integrator otherwise |
| S-01-4 basis lineage not supplied | Partly (REQ-003's basis definition at a host without lineage) | Keep the protected criterion and record a host non-conformance (P2 C1-B B-3), or amend | Owner at the host join |
| OI-001 residue / OI-002 residue (TBD-002/003) | No | Operation-specific additions under OI-021 | Owner with App/SWB owners, at OI-021 |
| SWBPIPE host gaps (data, SWBPIPE owner decisions): A10 reject record (G-18); per-row accept (Apply is per batch); capture evidence with person and time (SQ-01); durable receipts (SQ-09 (c)); undo with receipt (SQ-10); per-class autonomy (OI-016); findings storage (SQ-24); Checked mark (DEC-104); workspace identity on main (SQ-07); host run records (SQ-19); network enforcement in a native layer (none, SQ-30); DEC-051 residency | No (the App criteria stand; AX-003, REQ-002) | V4-EXM-20 as written cannot pass against SWBPIPE today (per-row accept and one rejection have no counterpart). The design records each gap per case | **Owner as SWBPIPE owner**; inference: candidates for the next relay list |
| OI-013 / OI-014 loop placement and shared component | Partly: what "the identified App … candidate" means in an embedded journey (REQ-001, REQ-008) | Host-specific construction external; shared loop contract IN; no common service presumed | Shared contract owner with SWB owner |

**Designable now without host joins** (inference, grounded in CA §2.6 and §6): the four case definitions against the CA step map with the operation as a parameter; expected observations and evidence per step; failure behaviour per step (CAF rows); the candidate-identification record and the external-contribution ladder (CA §7.2); the V4-EXM-23 observation plan and comparison method; the dossier structure and its handoffs to DEL-11-03 and DEL-09-11; the per-case SWBPIPE gap sheet; and rehearsals on SH-1 for the steps SH-1 supports (test-double standing, "say nothing about SWBPIPE"). **Not designable as evidence:** any SWBPIPE observation, receipt, act capture or traffic capture; the live V4-EXM-20 pass.

### B5. What exists to build on

- **DEL-01-01:** HOSTING-v0.8 boundary; PIN_SPIKE; OBS-1 (one local LM Studio turn: Codex start-up traffic to chatgpt.com and github.com with analytics off; the snapshot method and its miss of a short-lived process; kernel sandbox denial of a local socket under read-only); OBS-1 Part C (Chat Completions representation points, LOOP's FB-CC-1 fixture basis); OBS-2/OBS-3. OBS-1 is the only traffic-observation precedent in the project. It concerns the App's Codex, not a host agent; K-12 makes Codex's own start-up traffic a recorded supplier behaviour, which an all-traffic host observation on the same Mac must attribute by process.
- **Protocol types at 0.158.0:** marginal here; the host agent is the minimal loop over Chat Completions (V4-ARC-10), not Codex.
- **First-increment contracts consumed at package level:** C (catalog, read basis, SH-1, FX-PIPE-01), P (lifecycle, item-level acceptance, outcomes), ACT (act kinds, A12 destination grant subclass), AS (grant display), RS (R7, R8, R15, §6, §7), LOOP (§5 destinations, §6 dispatch, §7 malformed calls), PANEL (§3.3, §3.8, §4), WD/EXEC (Phase 1 checkpoints), GUIDE (HC-7), CA (step map, CAF rows, option sheet, W14 rehearsals on SH-1).
- **SWBPIPE answers** (data): A-1…A-5, SQ-01…SQ-32, ANS §3's twelve contradicted assumptions.
- **App v3 exemplar:** no host qualification or traffic observation found; v3 PRD FR-076 replay lens is the nearest reconstruction precedent (relevant to Part C).

### B6. Design scope for this pass

1. `Design/LOCAL_HOST_QUALIFICATION.md` — cases LHQ-20, LHQ-21, LHQ-22, LHQ-23 against the CA step map (CA-0…CA-R) with the operation as a parameter slot (FX-PIPE-01 as the proposed fixture), each with preconditions, steps, required observations, the contributing contract by label and section, and pass/fail/blocked/not-run/inconclusive rules per criterion.
2. Candidate identification and the external-contribution ladder (prepared → … → examined) for each host contribution, with "received", "adopted" and "examined" kept apart (REQ-001, VER-008).
3. The V4-EXM-23 observation design: observation points (process tree of the host, its loop and outside processes; the App's Codex excluded or attributed), method options and blind spots, privileges, the comparison with the host's destination record, allow list and in-work grants (LOOP MS-14…MS-23), and what makes the capture "incomplete".
4. The dossier structure (OUT-002): case results, links by reference to host receipts and records, the act/owner account, the handoff record to DEL-11-03, and a source-journey record for DEL-09-11 (journey identity, date, run author, record set).
5. The SWBPIPE gap sheet per case (answers of 2026-09-28; data, not commitments) and a candidate relay list, without sending anything.
6. SH-1 rehearsal plan: which case steps SH-1 supports (CA §2.6 says 9 of 10 rows, 3 fully), labelled test-double. Optional schemas: case result and traffic observation record, reusing DEL-09-01's protocol when it lands.

Leave out: operation, autonomy or environment selection (OI-021); SWBPIPE construction; any live run or claim of a join; V4-EXM-31 (DEL-09-11); V4-EXM-25 (DEL-09-09); the replacement packet (DEL-11-03).

---

## Part C — DEL-09-11 Later run reconstruction witness

TEST_SUITE. Owner: App evidence examination owner, with a separate named reconstructing reader. Scope SOW-206; objectives OBJ-005, OBJ-008. It consumes DEL-09-07's V4-EXM-20 journey, so its **execution** waits on the deferred host join; its definition does not.

### C1. Obligations (2 OUT, 6 REQ, 6 AC, 6 VER; also 3 CLM, 3 AX, 3 TBD)

| ID | One line | Rests on |
|---|---|---|
| OUT-001 | TEST: V4-EXM-31 witness by a named reader separate from the run author, a week after the identified V4-EXM-20 journey | EXM V4-EXM-31 |
| OUT-002 | DOC: the reader's reconstruction (request, proposal, actual acceptance, actual change), receipt references, acts with content/scope/purpose, lapse, unknowns | REC-01…05; HI-70 (amended)/71 |
| REQ-001 | One identified V4-EXM-20 record set from DEL-09-07 plus DEL-04-03 compact records; named reader ≠ author; both dates recorded; a plan, an immediate reread or elapsed time alone does not fulfil | V4-EXM-31 |
| REQ-002 | Recover request, proposal, acceptance, change; trace workflow identity/version, conversation, model, autonomy, operations, outcomes to receipts, hashes, origin marks; keep references, never a copy of host truth | REC-01…05; HI-70/71 |
| REQ-003 | Each act: actor ≠ recorder, content/scope/purpose, visible lapse; separate acts; no promotion of tool, silence, source resolution or transport success | AUT-01…05; REC-03/05; HI-25, HI-30…33 |
| REQ-004 | Project source records and linked host evidence are the authority; private memory, transcripts and derived views only locate; gaps stay gaps; partial results reported but do not fulfil | REC-01…04; EXM §§1–2 |
| REQ-005 | Candidate, configuration, date, reader, source run; observations vs inferences; reopen on change; no favourable approval or reliance demanded | EXM §§1–2; AUT-02…05 |
| REQ-006 | Performs no act of DEL-04-03, DEL-09-07, SWBPIPE, the person or the open-policy owners | CLM-001…003 |
| AC-001…AC-006 | Actual week-later reconstruction (AC-001); request-to-change account with resolvable references (AC-002); faithful act record and fabrication negatives (AC-003); unknowns kept (AC-004); candidate/result metadata and reopening (AC-005); input and responsibility account (AC-006) | As REQ |
| VER-001…VER-006 | One per AC in order; VER-001 rejects "a schedule, test definition or synthetic clock advancement" as the witness | As REQ |

**Overtaken or lagging text** (inference; the SoW is the unrevised INIT contract):

- **TBD-002** states OI-001 and OI-002 as wholly open; D2/D3 ruled them (as for DEL-09-05).
- **Amended V4-HI-70 not carried.** SCA-V4-001 added to V4-HI-70 "for a host's agent, each network destination contacted". V4-EXM-31 verifies V4-HI-70…71. REQ-002's list of traced elements does not name destinations, and SCA-V4-001 did not revise this SoW (its coverage files list DEL-09-11 only as an unaffected row). The design can read the amended basis directly; a later amendment can align the text.
- **S2 cites `OWNER_DIRECTIONS.md` J/U1, M/U4, O/U5 and "original human-act defaults"**; later DECISION-4 D4-1 (phased checkpoints) and K1-2 (earlier acts count on current content) affect which checkpoint dispositions a reconstruction meets. Not contradicted; not stated.

### C2. Joins

| Row | Direction / other end | DAG-004 | Mirror |
|---|---|---|---|
| DEP-09-11-005 | UPSTREAM → DEL-04-03 (PREREQUISITE) | admitted | DEP-04-03-015 (MIRROR) |
| DEP-09-11-006 | UPSTREAM → DEL-09-07 (PREREQUISITE) | admitted | none on DEL-09-07's side |
| DEP-09-01-028 (DEL-09-01's row) | DEL-09-01 → DEL-09-11 HANDOVER | admitted (representative) | DEL-09-11 has no row of its own |
| DEP-09-11-007…010 | EXTERNAL: SWBPIPE owner (authoritative journey receipts); the separate named reader; OI-001/OI-002 owners; OI-021 owners | NOT_TOPOLOGICAL | — |

DAG-004: DEL-09-11 is in the route re-examination list (reaches the new SCC-002 consumers through admitted arcs; "add paths, not suppliers").

What the Design files assume of DEL-09-11:

- **DEL-04-03 RS-v0.9.** §10: "DEL-09-11 | Complete records for the week-later reconstruction (inspection replay, EXEC RP-6) | — | This format does not perform the witness". §10.1: DEP-04-03-015 / DEP-09-11-005 admitted. §11: "Reconstruction witness — DEL-09-11". §2 ordinary-file authority rules, §3 record kinds (the run record for a host-agent run is produced by "host run recording (external owner, DEP-04-03-016)"), §9 evidence references with resolution status "at write (resolved / unresolvable / not supplied) and at read", §13 format, §14 writer and reader sequences, §12 examples and the valid JSONL examples (`RS_RECORD.valid.host-run.example.jsonl`, `…host-destinations…`). VC-24: "distinct from DEL-09-11".
- **DEL-02-03 EXEC-v0.7** §4.9 "Why no resumption": "An ended run's record is evidence for later reconstruction (DEL-09-11). Reopening it would let a later act rewrite a closed disposition (V4-REC-05)." §4.12 RP-5 (declaration of the resolved revision recorded for the run; otherwise "declaration not resolvable — reconstruction not verified") and RP-6: "**Inspection replay** (read-only, e.g. DEL-09-11) | Rebuilds the same arrival identities and dispositions from the same record. It issues no request, dispatches nothing and records no act. Lapse shown at inspection time is labelled with its evaluation time".
- **DEL-09-06 CA-v0.7** §2.3 CA-5/CA-R: SWBPIPE "receipts session-only; no act references (SQ-01, SQ-09 (c))".
- RS §10's external host recording row (data from SWBPIPE): "no capture-evidence reference (SQ-01) … whole-model identity only (SQ-03) … session-only receipts (SQ-09), receiptless session undo (SQ-10)".

### C3. Proposed contract changes still open

None in the SCA-V4-003 ledger or closure audit names DEL-09-11. Candidates for a later amendment (inference): TBD-002 wording; REQ-002 destinations per amended V4-HI-70; a receivers sentence or mirror on DEL-09-07's side.

### C4. Open items and owner choices

| Item | Shapes design now? | Options and what the files say | Owner? |
|---|---|---|---|
| **Who may be the reconstructing reader** | **Yes**: the isolation protocol, what counts as "private memory", the separation evidence | V4-EXM-31 says "someone"; the SoW says "a named reader, separate from the host-run author". Options: the owner or another person; an agent instance given only the input-set manifest and no access to the run's conversation or harness store; either, with the evidence each needs. No file decides | **Owner** |
| **Durable host receipts** | Partly: the failure path. Under SWBPIPE's answers every host receipt is session-only, so a week later RS §9 resolution reads *unresolvable* and AC-002 ("resolvable host receipt/hash/origin references") cannot pass | V4-HI-71 and V4-REC-04 forbid copying receipts into the run record. A durable receipt carrier is a SWBPIPE owner decision (ANS §2) | **Owner as SWBPIPE owner**; inference: next-relay candidate |
| Producer of the V4-EXM-20 host-run record | Partly: which compact record the reader starts from | RS §3: external host run recording (DEP-04-03-016); SWBPIPE has no host run records (SQ-19) and no loop (SQ-20) | SWB owner; OI-013 |
| Actor in host acts | Partly: AC-003's actor ≠ recorder check on host acts | SWBPIPE's Apply receipt "names no person … and no time field" (SQ-01) | SWBPIPE owner (PB-TBD-002, DEL-16-03) |
| "A week later" | Minor (date evidence rule) | Inference: at least seven calendar days between the journey date and the reconstruction date, both evidenced; a synthetic clock is excluded by VER-001 | Integrator |
| TBD-001/003 (inputs; OI-021) | No | Execution needs the actual journey and settled criterion | Owners named |
| TBD-002 wording | No | Carry to next amendment | Owner (low) |

### C5. What exists to build on

RS-v0.9's format, writer/reader sequences, example records and local prototype; EXEC RP-1…RP-8 (RP-6 inspection replay); CA §2.3 CA-5/CA-R and the W14 result record; RECOVERY custody events (unknown outcomes); the option sheet's SH-1 rehearsals (receipts readable on the double, which is durable). App v3 exemplar (evidence only): the Runtime Audit Mirror (`.chirality/sessions/<sessionId>/events.jsonl`, v3 TYPES line 54), FR-076's provenance-labelled replay ("without replacing the mounted primary dialogue or canonical evidence store"), and a selected-session replay lens test.

### C6. Design scope for this pass

1. `Design/RECONSTRUCTION_WITNESS.md` — the reader protocol: identity and separation evidence; permitted sources (project files, host evidence by reference) and excluded authorities (harness store, private memory, derived views), with how exclusion is evidenced; the input-set manifest (source journey identity, record set and hashes, journey date).
2. The reconstruction account format: per claim (request, proposal, acceptance, change, act, outcome), its source, reference, resolution status at read, standing, observation vs inference, and unknowns; the examiner's comparison against the run evidence (VER-002…VER-004), using RP-6 inspection replay and RS §14.2.
3. Outcome rules: completed witness vs partial, blocked, not-run, inconclusive; how unresolvable receipts, a missing actor, a lapse found at inspection time (labelled with its evaluation time) and an unresolvable declaration (RP-5) affect the verdict.
4. Fabrication negatives and the lapse case, with supporting fixtures kept distinct from the live journey (fixtures from RS examples, a reader rehearsal on SH-1 or RS example records, test-double standing).
5. Date and applicability rules (week-later evidence; reopening on candidate or basis change), and the input and responsibility account (VER-006).
6. Optional schemas: input manifest and reconstruction account.

Leave out: the record format and writer (DEL-04-03), producing the source journey (DEL-09-07), host receipts (SWBPIPE), any live witness or date choice.

---

## Part D — Merged results

### D1. Owner choices across the three, ranked by how much design text depends on them

1. **DEL-09-11 reader identity** (person, isolated agent, or either with stated evidence). The whole reader protocol depends on it. Owner.
2. **The act kind of a coordination decision on a decision package** (DEL-09-05 VER-004, with DEL-06-02, DEL-04-01, DEL-04-03, DEL-01-04). Shapes the decision case and the record compared. An integrator ruling can name it (R12-5 precedent); the owner decides if it changes which coordination decisions are reserved to the person. See S-1.
3. **V4-EXM-23 observation method and its privilege** (DEL-09-07 VER-006). The method is design; any administrator-level capture at execution needs the person's permission and act. Shapes the completeness argument and limits.
4. **The A12 mapping of destination grants and the recording of boundary refusals** (SCA-V4-003 DEFERs SC2-04-01-2, S-0502-1, P2-C1-C-B-2). Shapes what V4-EXM-23 evidence expects for grants and declines. Owner.
5. **SWBPIPE-side items, decided by the owner as SWBPIPE owner** (durable receipt carrier; per-row accept and a reject record; act capture with person and time; per-class autonomy, OI-016; host run records; embedded loop, D-58; native network enforcement; DEC-051). They shape no App design text (the criteria stand), but they decide whether DEL-09-07 AC-002…AC-006 and DEL-09-11 AC-002/AC-003 can ever pass. The owner choice now is only whether they go on the next relay list; host joins stay deferred.
6. **OI-021 operation, autonomy class and environment** (DEL-09-07, DEL-09-11). Parameterized in the design; needed at execution. No action now (CA DI-1…DI-3 "stays open").
7. **Live-witness model route for DEL-09-05** (sign-in or a namespace-capable local route). Execution only.
8. **Carrying lagging SoW wording to the next amendment**: DEL-09-05 TBD-002/TBD-003, DEL-09-11 TBD-002 and REQ-002 (amended V4-HI-70), DEL-09-07's missing receivers sentence for DEL-09-11, R9-6-5. Same pattern as the owner's "1 yes" for DEL-09-02. No design text depends on them.

### D2. Structural questions that could force a later restructuring

- **S-1 Coordination decisions have no act kind or record kind.** ACT §2.1 leaves "reserved coordination decisions (V4-PM-04)" unnamed; RS §3 and §6.1 define human-act records for a closed list of kinds; AAC covers App-content acts and A15; RS §10's PKG-06 row says "Decision records as act subjects". Adding a kind would revise ACT §2.1 (first increment), RS §3/§6/§13 entry kinds and the schema enum (first increment), and AAC (pass 3). Treating the decision as a non-act coordination record would instead constrain DEL-06-02 and DEL-09-05 VER-004. Best decided before DEL-06-02 and DEL-09-05 designs fix their record references.
- **S-2 Who writes the run record of a host-agent run.** RS §3 assigns it to external host run recording; SWBPIPE has none (SQ-19), and if the minimal loop is shipped as a shared component (OI-013/OI-014 open), the App's writer may write it. That would move RS §3's producer column and LOOP's event-to-entry mapping (LOOP E-4 says "the field mapping is DEL-04-03's"), and it changes what DEL-09-07's dossier links and DEL-09-11 reads.
- **S-3 Receipt durability against "link, don't copy".** V4-HI-71 and V4-REC-04 have the run record link host receipts. With session-only receipts every week-later reference is unresolvable. Unless the host supplies durable receipts, the only App-side remedy (keeping receipt content) contradicts the basis. This is a basis-level tension for DEL-09-11 and DEL-11-03, not an App file defect; it should be on the record before DEL-09-11's design fixes its outcome rules.
- **S-4 Delegation mechanism.** NPTD §7 (identity model, export to DEL-06-01) and DEL-02-04's per-thread K-10 label assume native Codex children. If DEL-06-01 also delegates by App-started TASK-role conversations (L-2), NPTD §7.6–§7.7 would not cover those workers and the association model changes (NPTD is pass 3, not first increment). This is shared with S1-A.
- **S-5 Per-row versus per-batch acceptance.** V4-EXM-20 requires row-by-row acceptance and one rejection; P §4.3 defines item-level acceptance; SWBPIPE's Apply is per batch with no reject record. No App file needs restructuring, but CA §2.4's partial disposition and P's item-left events have no host counterpart; the gap is the host's.
- Observation only, no restructuring expected: mirror rows missing on the supplier side (DEL-04-01 → DEL-09-05; DEL-09-07 → DEL-09-11; DEL-09-06 → DEL-09-07, R9-6-5; DEL-09-07 and DEL-09-11 have no UPSTREAM row of their own to DEL-09-01). Each arc exists through the other end's row; DAG-004 is unaffected.
