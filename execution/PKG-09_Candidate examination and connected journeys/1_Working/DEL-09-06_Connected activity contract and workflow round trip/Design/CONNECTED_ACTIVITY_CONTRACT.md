# Connected activity contract — first App/host increment
- Contribution: DEL-09-06/CA-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (draft increment contract: four activities, named expressions, one complete first activity, owner/check allocation, staging, decision/input account — *not* the final operation-specific SoW, which awaits OI-021); OUT-002 (requirements on the reusable connected workflow and its source-qualified revision history — the workflow itself is not authored here); OUT-003 (design of what the V4-EXM-14 joined witness needs — designed, **not run**); OUT-004 (external contribution/evidence account; the question set is `RELAY_QUESTIONS_SWBPIPE.md`); REQ-001…REQ-008; AC-001…AC-008 through designed VER-001…VER-008
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 511f2c0016920cbf67476f1b8d911ed85d6cfa419e7a6b15f3c7e20457779b37; Dependencies.csv sha256 ce3218a22a8629a731a05f5d24093e9aee6660b011a63414b1589c828e4297ed (ACTIVE EXECUTION rows DEP-09-06-012…024); `P/docs/PRD.md` (sha256 657593ce12a9a6da9f8b6c66579945499d909a8b6272d919d2d14a3db4538573) §2.3, §3–3.1, V4-WF-01…06, V4-AUT-01…05, V4-EXT-01, V4-REP-01, OQ-02, OQ-11; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7db2d74619ed47d184f44938bb06f1e2abda0a304a9e11b9230d0960da) §1, V4-HI-25, V4-HI-30…33, V4-HI-40…42, V4-HI-70/71, §11; `P/docs/EXAMINATION.md` (sha256 1b156553dec7eb103dbb1166f5c0dbe9c719d26630d2fcace26c28b3ef54ee19) §1–2, V4-EXM-14, §4; `HANDOFF_SWBPIPE_DOMAINS.md` (sha256 6e7a2f0427acdc0553bd5ea9cceaeceeff5bd82bf1165ed5930c389532e15ef4); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e) D1–D4; R1 (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4), R2 (sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088), R3 (sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf); `reviews/V2.md` MAJOR-1 (T15 re-point); BRIEFS.md working copy sha256 77a42f8a8c8260285b4142d3a6392a07daead16010b209139efc0d3efc60a21f ("Common brief", "Owner rulings now in force", "Wave 2 — common additions", "W9")
- Consumed inputs (read with `git show`; not the working tree):
  - **Wave-1 v0.3 at `ba0b37123`.** The brief names `main` merge `98b1723b`, which is not present in this clone. DISPATCH.md records it as the merge of head `1c36b6d97`; every Wave-1 Design blob is identical at `ba0b37123`, `1c36b6d97` and `e20a3ae8d` (verified by blob id). Short names used below:
    - **C** = DEL-03-01/C-v0.3 `CATALOG_AND_READ_BASIS.md` sha256 ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26 (§4.1, §5, §6, §8, §10 FX-PIPE-01 incl. T15 per V2 MAJOR-1);
    - **P** = DEL-03-02/P-v0.3 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` sha256 ec0db87f239bc42e2e3e953d660ce3c4ceddf605d7b98cf1393f97a099b699cf (§3–§11);
    - **ACT** = DEL-04-01/ACT-POLICY-v0.3 `ACT_AND_POLICY_CONTRACT.md` sha256 b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128 (§2, §4, §5, §6, §7, §12);
    - **AS** = DEL-04-02/AS-v0.3 `AUTONOMY_AND_STANDING_EXCHANGE.md` sha256 7b634137bb8402f3eaedc943dab0c5f1114b9d4433d2b94e13540ac0bf8e0514 (§3, §4, §8);
    - **RS** = DEL-04-03/RS-v0.3 `RECORD_SEMANTICS.md` sha256 925f35ca27bd7d1e71a375883ada9903267408af57312eed1ae02b47776a3528 (§3, §4 R1–R13, §6, §7);
    - **LOOP** = DEL-05-01/LOOP-v0.3 `LOOP_RECEIVING_CONTRACT.md` sha256 6b771c8027787193d536fa3507214a8cc579d6ec2f476ee880609c920b6f25c7 (§2, §6, §10, §11, §12, §13);
    - **PANEL** = DEL-05-02/PANEL-v0.3 `PANEL_RECEIVING_CONTRACT.md` sha256 4c47764d3af434c23e63dcc2c10d28f18a4a94546d63d452855c471cfe47bee9 (§3, §5, §7, §8);
    - **WD** = DEL-02-01/WD-v0.3 `WORKFLOW_DECLARATION.md` sha256 84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb (§4, §6) and **WD-EX** = DEL-02-01/WD-EX-v0.3 `EXAMPLES.md` sha256 0f1058d7f0990e766b3effc3d3de24fc16383197874cced1f5b4212419cf018d (E1, E1c, E2, E3, E4);
    - **HOSTING** = DEL-01-01/HOSTING-BOUNDARY-v0.3 `HOSTING_BOUNDARY.md` sha256 34c3383402aabe6e9347aa2f111318538c4a2a4ca85adb8fffff7e439fdde94e (§3, §6, §8.2) and PIN-SPIKE-v0.1 `PIN_SPIKE_0.158.0.md` sha256 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115 (pin facts only).
  - **Wave-2 at `e20a3ae8d`:** **EXEC** = DEL-02-03/EXEC-v0.1 `EXECUTION_COMPATIBILITY.md` sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8 (§2–§8, RT-11); **ADAPTER** = DEL-03-03/ADAPTER-v0.1 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074 (§2–§10).
  - Pending owner questions `DECISIONS_PENDING_2.md` D5, D6 (working tree, uncommitted): cited as **pending**, never as ruled.
  - SWBPIPE contributions, answers or evidence: **none received** (DEP-001). DEL-09-07, DEL-09-01, DEL-09-02, DEL-02-02, DEL-01-04: accepted SoW meaning only (outside this undertaking, D1).
- Receivers: DEL-09-07 (local host qualification V4-EXM-20…23 — shares the activity; outside this undertaking, D1); DEL-09-09 (V4-EXM-24/25; `EXTERNAL_TRACE_CASES.md`); DEL-02-03 (RT-11 evidence account consumer; §4, §8); DEL-05-01, DEL-05-02, DEL-04-03 (joined observation needs, §8); the external SWBPIPE owner via the human (OUT-004; DEP-09-06-020); the owner and App/shared owner for OI-021 (§2.5); closeout C1 (findings §12).

---

## 0. Reading this definition

**What it defines.** The *draft* increment contract for the first connected
activity (SoW OUT-001): which App/shared contributions each step uses, which
host contribution it needs, who checks what, how the work is staged without
PEC or Domains, what standing each piece of evidence has, and what the
V4-EXM-14 round-trip witness will need. It also states the requirements the
reusable connected workflow must meet (OUT-002) and keeps the external
contribution account (OUT-004).

**What it does not do.** It selects no operation, autonomy or environment:
each stays `UNRESOLVED{OI-021}`. The supports/run adjustment on FX-PIPE-01 is
a **proposed fixture only**. It authors no workflow (authoring follows the
`create-workflow` method and DEL-02-02 review/registration, later
undertaking). It runs nothing. It assigns no SWBPIPE construction. It selects
no wire field, type, transport, hash or canonicalization algorithm,
persistence, process placement or shared-component placement (OI-013, OI-014).

**Naming.** Bold element names are semantic labels, not wire names. Acts are
A1–A14 (R-1); class values are C §3.1's five; outcomes are P §9 and C §4.1;
dispositions are WD §4.3.4's six; checkpoint vocabulary is WD-v0.3's. Fixture
identifiers are C §10's (FX-PIPE-01). Local labels are `L-CA-n`, each with its
reason. External questions are `SQ-nn` from `RELAY_QUESTIONS_SWBPIPE.md`.

**Labels.** SETTLED (accepted basis or owner ruling, cited); DERIVED;
INTEGRATION (R1/R2/R3, cited); **PROPOSED (W9)** for a choice made here, open
to comparison and owner revision. Case states: DESIGNED · AWAITING INPUT
(named input) · HELD (named decision).

---

## 1. Settled distinctions relied on

| # | Distinction | Citation |
|---|---|---|
| S-1 | The first connected activity is: inspect a model, propose an adjustment, request a non-mutating check, meet an intervening edit, recover the actual outcome and receipt; it uses invented engineering material | HANDOFF; EXAMINATION §4 intro; SoW REQ-001 |
| S-2 | Exact operation, autonomy and environment are chosen by the owner via the outside SWB session with the App/shared owner, before connected-activity SoW and execution | OI-021; PRD OQ-11; SoW TBD-001 |
| S-3 | SWBPIPE implementation is the external session's; files are human-relayed; a prepared handoff is not a commitment, delivery or adoption | V4-EXT-01; HI §1, §11; SoW CLM-004, REQ-005 |
| S-4 | Execution, edit acceptance, checking, approval and professional reliance are distinct acts with their own actor and evidence; success establishes none of them | V4-HI-25; V4-AUT-03; #d3; SoW REQ-004 |
| S-5 | A declared checkpoint waits for its act even under direct autonomy | V4-HI-42; V4-WF-05; D2 |
| S-6 | Selected/resolved bytes, what was supplied, provider adoption and observed behavior are separate; registration or a portable file proves nothing | V4-EXM-14; SoW REQ-002 |
| S-7 | Initial activity requires neither PEC nor Domains; independent App work need not wait for the joined witness | SoW REQ-006; PRD §2.3/§8 |
| S-8 | Reserved to the person (App/shared contracts, first increment): A4; A5 where autonomy requires a proposal; A6; A7; A12; A13 enabling. DERIVED: A10 wherever A5 is. INTEGRATION: disabling access is also A13 | D2; R-1; R2-3 |
| S-9 | App routine tool permission is the user's own Codex setting (A14); never a reserved or professional act; hosts have no classifier mode | D3; R2-8 |
| S-10 | Checkpoint satisfaction needs attributable evidence from the capturing surface; a faithful record cites it | R-5; R2-20 |
| S-11 | Every result names its candidate, configuration and date; changed code reopens affected checks; criteria are not weakened | V4-EXM-01/03/05 |

---

## 2. The first connected activity

### 2.1 Four user activities and the two named expressions (AC-001; SOW-040/041)

| User activity | Its part in the first connected activity | Expression | App/shared contributions | External / other |
|---|---|---|---|---|
| **Practitioner** (engineer): model changes and checks; results/report work | Performs CA-H acts: accepts or rejects proposed items (A5/A10), marks changed rows checked (A4); may change the grant (A12) and enable external access (A13); reads the return | SWBPIPE (host UI, panel); the App for App-side acts | ACT, AS, RS, PANEL (receiving), EXEC §5 | Host act facility, views, receipts (DEP-001); the person |
| **Workflow maker** | Authors, reviews and registers the connected workflow in the App; carries it to the host; opens and refines the host's adaptation back in the App | Chirality App | WD, EXEC §6 (transfer trace); DEL-02-02 (later, D1) | Host library, adaptation (DEP-001) |
| **Application builder** | Realizes catalog entries and tools on the host's three surfaces; supplies the App's receiving side | SWBPIPE (catalog, loop, external interface); the App (adapter) | C, P, LOOP, ADAPTER, HOSTING | Host catalog, route, endpoint (DEP-001) |
| **Coordinator** | Bounds the work, relays questions and returns, records decisions and evidence, keeps the witness honest | The App manager and the human | This file; `RELAY_QUESTIONS_SWBPIPE.md`; DEL-09-07/09-09 examination | The human relays; the owner decides |

The App's standalone workflow-making loop (OBJ-001, DEL-09-02) proceeds
independently of this activity and is not reassigned here (SoW CLM-006).

### 2.2 Acting-surface variants (`UNRESOLVED{OI-021}` environment)

The accepted basis names two routes to the same host operations. Which the
first increment uses is part of the OI-021 environment choice (SQ-04 (c)).
This contract defines both, so neither is presumed.

| Variant | Agent | Surface (C §8) | Receiving contributions | Examination owner |
|---|---|---|---|---|
| **CA/E** | The host's embedded agent through the minimal loop | E | LOOP, PANEL (receiving); construction external (OI-013) | DEL-09-07 (V4-EXM-20…23) |
| **CA/X** | The Chirality App's Codex through the host's external interface | X | ADAPTER, HOSTING | DEL-09-09 (V4-EXM-25) |

In both variants the person's acts on host content are captured by the host's
act facility (V4-HI-31; EXEC CAP-1). The V4-EXM-14 round trip (§8) uses the
host's run of the carried or adapted workflow, whichever variant the host run
uses; the workflow's App side always runs through stock Codex (HOSTING).

### 2.3 Step map (REQ-001; AC-001)

Fixture steps are C §10.3's timeline. Host contributions name the relay
question that asks for them.

| Step | Fixture steps | What happens (semantic) | App/shared contributions used | Host contribution needed | Evidence the step yields |
|---|---|---|---|---|---|
| **CA-0 Prepare** (frame) | T1; ⟨set-1⟩; E1 ⟨rev-3⟩ selected | Workflow selected by full identity tuple; required-tool check on the acting surface; grant displayed; for CA/X the person enables external access (A13) | WD §6, §4.2.4; EXEC §3 (CK-1/CK-2, CR-1…CR-13), §3.6 hold support; AS §3; ADAPTER §3 (channel states, E-1…E-9), §8 S-1; HOSTING §8.2 (App supplied guidance) | Catalog edition with exposure (SQ-11); workflow listing and declared-part reading (SQ-17); enablement facility (SQ-13); grant presentation (SQ-05) | Compatibility report; grant display state; channel state; run record R1, R2, R6 |
| **CA-1 Inspect** | T3 (basis B1), T9 (B2) | Agent reads the supports table; the read carries its basis and per-row subject content identities | C §5, §6; LOOP §2.2 (FX-V1); ADAPTER §4.3 RD-1…RD-5, XF-11; RS R7 | Read results with full basis and subject identities (SQ-03, SQ-07); mapping on X (SQ-12) | Read entry with basis; standing from host result |
| **CA-2 Propose** | T5 (PR-1), T9–T10 (PR-2 queued) | Agent drafts one proposal, one item per change, citing the relied-on basis; the host validates and queues; queued ≠ applied | P §3, §4.1, §9; ACT §5.3, §6 (treatment → outcome); AS §3; LOOP §6 (FX-V2, FX-V3); ADAPTER §5, §6 (RP-3), XF-16, XF-22; WD I-7 / R2-12 constraint | Route, treatment resolution, queue acknowledgment (SQ-09); proposal identity (SQ-08); policy for the operation (SQ-05, SQ-06); constraint receipt (SQ-02) | Dispatch record with origin, grant in force, constraint; *queued* outcome |
| **CA-3 Request a non-mutating check** | T4 (OP-C3 findings), T4a (OP-C12 host check); re-examination after T12 | Agent examines (A3 findings, requester-stated limit) and/or requests the host's named check ("host checks passed/failed: ‹named checks›" with evaluated basis); neither is A4 | C OP-C3, OP-C12, §6.2; R-4 label rule; ADAPTER §4.4, XF-12; RS R10; WD §4.4 promised standing | Which check the activity uses (SQ-04 (b)); where findings are held (SQ-24) | Findings reference (A3); host check result with basis |
| **CA-4 Meet an intervening edit** | T6 (Engineer A edits S-3, r13), T7 (PR-1 refused — stale), T9 (re-draft PR-2, lineage PR-1) | The person edits the model; submission relying on B1 is refused per item with both bases; no retargeting; a re-draft is a new proposal on the new basis | C §5.3/§5.4; P §5, §6; R2-13; LOOP FX-D2; ADAPTER §7.1, §7.2, XF-14, XF-17; EXEC MX-6 (if items leave after queueing) | Per-item stale check on original inspected basis, not queue-time basis (SQ-07); no retargeting | Refusal with relied and current basis; item-left events; lineage |
| **CA-H Human acts at checkpoints** (frame, interleaved) | T11 (A5 item 1, A10 item 2); A4 on changed rows after T12; T2 independent A4; T14 lapse | The run holds at `CP-accept` (A5, kind (c) *queued*) and `CP-check` (A4 on objects changed by the applied outcome); acts are captured by the host facility; the App/loop faithfully records them citing capture evidence | WD §4.3; EXEC §4 (hold machine, SP-1…SP-8, MX rules), §5; ACT §2, §4; RS §6, §7; AS §4; PANEL §3.5, §5; LOOP §2.4 | Capture-evidence reference (SQ-01); content identities and resulting objects (SQ-03); constraint receipt (SQ-02); host enforcement of its reserved list (SQ-05) | Checkpoint arrivals and dispositions (RS R8); human-act records (R9) with actor ≠ recorder |
| **CA-5 Recover the actual outcome and receipt** | T12 (RC-1, resulting objects S-5, R-100), T13 (lost ack; retry same identity), V-OU1, T16–T17 (direct under ⟨set-2⟩, undo) | Application yields a receipt; a lost acknowledgment leads to seeking observation, then a retry with the same identity; de-duplication precedes the basis check; unknown stays unknown; undo reverses a receipt | P §4.4, §4.5, §5, §7, §9; C T12–T13; LOOP §6.3 (FX-O1); ADAPTER §5.6 PI-1…PI-4, §7.3, §7.4, XF-19…XF-21; EXEC §4.12 RP-1…RP-8; RS R7, R11 | Durable receipts, read by identity, de-duplication order and durability (SQ-08); outcome statements and unknown (SQ-09); undo (SQ-10) | Applied association with receipt link and resulting objects; *outcome unknown* with observer; evidence limits |
| **CA-R Return** (frame) | After CA-5 | Summary of what changed (receipt references), findings, acts actually performed, and unknowns; standings never strengthened | WD §4.4–§4.6; AS §8, §9; RS §4 | Receipt and act references readable (SQ-01, SQ-09) | `summary` output (*agent-prepared*); promised-versus-observed account |

### 2.4 Operating sequence on the proposed fixture (FX-PIPE-01; invented material)

```text
CA-0  select E1 supports-adjust ⟨rev-3⟩ (host) or ⟨rev-A2⟩ (App-carried); CK-2 report
      grant ⟨set-1⟩ effective (policy default): propose        [CA/X: A13 by the person]
CA-1  T3 read OP-C1 → B1 = FX-W1/g1/r12/⟨v12⟩/⟨m-fx⟩, ⟨S-1…S-4@r12⟩
CA-3  T4 OP-C3 (limit 6 m) → findings (A3); T4a OP-C12 → "host check failed: support spacing" @r12
CA-2  T5 draft PR-1 (item 1 OP-C4 add support; item 2 OP-C5 S-3 stiffness), relying on B1
CA-4  T6 Engineer A edits S-3 (r13) → T7 submit PR-1 → both items refused — stale (B1 vs B2)
      T9 re-read (B2) → PR-2 (lineage PR-1) → T10 queued        [CP-accept arrives: waiting]
CA-H  T11 Engineer A: A5 item 1, A10 item 2 (host facility, capture evidence SQ-01)
      → CP-accept resolved negatively, "partial" (EXEC MX-5); on-mixed path: continue with item 1
CA-5  T12 host applies item 1 → RC-1; resulting objects S-5 (created), R-100 (changed)
      T13 ack lost → seek observation by identity → if never received, retry PR-2 same identity
      → host answers recorded state (RC-1; item 2 rejected); else outcome unknown (observer)
CA-3  re-examine: OP-C1 read at r14, OP-C3 → examination-report   [CP-check arrives: waiting on S-5, R-100]
CA-H  Engineer A marks S-5 and R-100 checked (A4, SQ-01) → CP-check performed
CA-R  summary: RC-1, findings, acts performed (A5 item 1, A10 item 2, A4 S-5/R-100), unknowns
```

Graduated-autonomy branch (V4-EXM-22 overlap; used by W14-04): T15 A12 →
⟨set-2⟩ (class **P-03**, grant *direct*, scope {FX-W1; {S-4}}, per C T15 and
V2 MAJOR-1) → T16 OP-C9 applied directly (RC-2, origin mark, undo route, no
acceptance) → E1c `CP-check` waits for A4 on S-4 → T17 undo RC-3 *reverses
RC-2*.

### 2.5 Decision and input account needed to finalize the increment SoW (OUT-001; TBD-001/002)

The final operation-specific increment SoW is **not** claimed. It needs:

| # | Decision or input | Owner | Point of need | Current standing |
|---|---|---|---|---|
| DI-1 | The useful operation(s), including the non-mutating check | Owner via outside SWB session with App/shared owner (OI-021); informed by SQ-04 | Before connected-activity SoW and execution | `UNRESOLVED{OI-021}`; fixture only |
| DI-2 | Permitted autonomy for it; operation-specific reserved additions | Same owners (OI-021); host names its list (V4-HI-30); SQ-05, SQ-06 | Same | D2/D3 adopted for App/shared contracts; host adoption not evidenced (DEP-001) |
| DI-3 | Exact candidate environment (host candidate, configuration, model server) and acting-surface variant (§2.2) | Same owners (OI-021); SQ-04 (c)(d), SQ-27 | Before execution | Not supplied |
| DI-4 | Host act capture and constraint receipt | SWBPIPE owner (SQ-01, SQ-02) | Before any positive checkpoint case | Not supplied |
| DI-5 | Data boundary for App conversations reading host content (CA/X only) | Owner (pending D5); host side SQ-16 | Before enabling a live CA/X candidate | Pending; not ruled |
| DI-6 | App-side hold points for App runs | Owner (pending D6); DEL-03-03/DEL-02-03 | Before App-side hold fixtures | Pending; not ruled |
| DI-7 | Multi-row A4 purpose after partial lapse (ACT U-03; EXEC U-E3) | DEL-04-01 with the owner | Before re-hold and lapse fixtures run | Open; EXEC carries it conservatively |
| DI-8 | Extension promise (not needed for the first activity; needed before any extension claim) | Owner with host contract owner (OI-003) | Before extension claim | Open; DEL-09-09 |

---

## 3. The reusable connected workflow (OUT-002; REQ-002; AC-002)

### 3.1 Requirements on the workflow (PROPOSED (W9))

The workflow is authored later under the `create-workflow` method and
reviewed/registered through DEL-02-02 (later undertaking, D1). This section
states what it must declare so that the activity and the round trip can be
examined. Meanings are WD-v0.3's.

| # | Requirement | WD locus |
|---|---|---|
| WR-1 | Full source-qualified identity {kind, origin, source root, name, revision} and derived-from; holding library recorded at listed/selected/resolved | WD §6.1; R-9; EXEC §6.2 |
| WR-2 | Declared part at a stated declaration contract version; every category declared (an undeclared category makes the check *not established*) | WD §3.4 |
| WR-3 | Assumptions stated in prose and as expected inputs with quality/basis requirements (the complete five-element read basis for host reads) | WD §4.1 |
| WR-4 | Required tools by **catalog operation identity and version**, class *host operation*; one per step of §2.3 that calls the host; necessity and fallback for optional ones; never an adapter-specific tool name | WD §4.2; ADAPTER NM-1 |
| WR-5 | Checkpoints with the closed-list act, reached-when kind, subject class, scope, purpose, actor requirement, negative/mixed path and expected act evidence; A5 only with kind (c) *queued* on that proposal's change items | WD §4.3.1, validity rules |
| WR-6 | A governing checkpoint constraint on every change request whose result an A5 checkpoint governs | WD I-7; R2-12 |
| WR-7 | Returned outputs with promised standing from the non-approval vocabulary; human-act standing only conditional on a named checkpoint | WD §4.4 |
| WR-8 | Returned evidence by reference (receipts, bases, findings, act records) | WD §4.5 |
| WR-9 | No A6 (approve) or A7 (rely) checkpoint unless the owner asks for one; reliance stays with the accountable professional outside the workflow | WD-EX E1 note; V4-AUT-05 |
| WR-10 | Revision history kept by identity: every revision a new identity; adaptation a new identity with derived-from; no same-name rebinding | WD §6.3; EXEC §6.4, §6.6 |

### 3.2 Proposed fixture candidate

- **WF-1 = WD-EX E1 `supports-adjust`** ⟨rev-A2⟩ (App, origin *project*) and
  its host adaptation ⟨rev-3⟩ (origin *host*, derived-from ⟨rev-A2⟩). It
  already covers CA-1, CA-2, CA-4 (re-draft), CA-5 (re-examine after
  application), `CP-accept` and `CP-check`.
- **L-CA-1** (local variant, PROPOSED (W9)): WF-1 plus OP-C12 *Run
  support-spacing host check* as an **optional** required tool at Inspect and
  Re-examine. **Reason:** the accepted activity names "a non-mutating check",
  and E1 declares only the agent's examination (OP-C3). C supplies OP-C12 as
  the host-named check; the variant lets CA-3 show both standings side by
  side.
- **WF-1c = WD-EX E1c `supports-label`** for the direct-autonomy checkpoint
  case (W14-04 (ii)).
- These are **fixture subjects**. The real workflow's operations follow DI-1.

---

## 4. Round trip App → host → App (REQ-002, REQ-003; SOW-238)

The trace meaning is EXEC §6, consumed unchanged. This contribution joins it
to host evidence; it adds no link.

| Link (EXEC §6.1) | Original ⟨rev-A2⟩ | Revised ⟨rev-3⟩ (host) | Refined ⟨rev-A3⟩ (App; EXEC local label) | Evidence owner | Host input |
|---|---|---|---|---|---|
| listed / selected / resolved | App library | host library | App library | DEL-02-02 (later); host | SQ-17, SQ-18 |
| exported / relayed / received | App → host; manifest (TR-4) | — | — | DEL-02-03; the person; host | SQ-17 |
| adapted | — | new identity, derived-from ⟨rev-A2⟩; checkpoint comparison (AD-2) | — | host | SQ-18 |
| opened / drafted / registered | — | host tuple opened read-only | draft base ⟨rev-3⟩ → registered with derived-from | DEL-02-02 (later) | — |
| supplied | App: HOSTING §8.2 | host loop per turn | App: HOSTING §8.2 | DEL-01-01; host | SQ-19 |
| provider-adopted | unknown | unknown | unknown | — | — |
| observed behavior | App run records (RS) | host run records | App run records | DEL-04-03; host | SQ-19, SQ-27 |

Rules carried: each link is separate evidence; a revised identity never
inherits an original's link; acts and dispositions never carry across
identities (EXEC AD-5); history is referenced, not copied (V4-HI-71).

---

## 5. Owner and check allocation (OUT-001; AC-001, AC-008)

"Focused check" is the producing owner's own verification, in its file.
"Joined check" is the candidate-bound examination that joins contributions.

| Contribution | Producing owner | Focused check (designed) | Joined check owner | Standing now |
|---|---|---|---|---|
| Catalog and read basis (C) | DEL-03-01 | C VC-C-01…; M3-CP with P | DEL-09-07; DEL-09-09 | v0.3 draft |
| Proposal and outcomes (P) | DEL-03-02 | P VC-P-… | DEL-09-07; DEL-09-09 | v0.3 draft |
| Act policy (ACT) | DEL-04-01 | ACT FX-/VC- cases | DEL-09-06 (W14-04/05); DEL-09-09 (XC-09/10) | v0.3 draft; D2/D3 adopted |
| Grant display (AS) | DEL-04-02 | AS VC cases | DEL-09-07 (V4-EXM-22) | v0.3 draft |
| Records (RS) | DEL-04-03 | RS VC cases | DEL-09-06 (W14-05/07) | v0.3 draft |
| Loop receiving (LOOP) | DEL-05-01 (receiving); construction external | LOOP VC-01…09 | DEL-09-07 | v0.3 draft |
| Panel receiving (PANEL) | DEL-05-02 (receiving); construction external | PANEL VC-01…07 | DEL-09-07 | v0.3 draft |
| Declaration (WD) | DEL-02-01 | WD §13 | DEL-09-06 (W14-01…03) | v0.3 draft |
| Execution compatibility, hold machine, transfer trace (EXEC) | DEL-02-03 | VC-E-01…11 | DEL-09-06 (W14-*) | v0.1 draft |
| External adapter (ADAPTER) | DEL-03-03 | VC-X-01…08 | DEL-09-09 | v0.1 draft |
| Hosting boundary (HOSTING) | DEL-01-01 | HOSTING VC | DEL-09-06 (W14-08 App side) | v0.3 draft; pin 0.158.0 (definition pin only) |
| Review, registration, drafts | DEL-02-02 | — | DEL-09-06 (W14-09) | **Not in this undertaking (D1)** |
| App act control | DEL-01-04 | — | — | **Not in this undertaking (D1)** |
| Examination infrastructure and protocol | DEL-09-01 | — | all examiners | **Not in this undertaking (D1)** |
| Local host qualification V4-EXM-20…23 | DEL-09-07 | — | DEL-09-07 | **Not in this undertaking (D1)** |
| External control; extension trace V4-EXM-24/25 | DEL-09-09 | — | DEL-09-09 | XT-v0.1 draft |
| **V4-EXM-14 joined round trip** | **DEL-09-06** | — | **DEL-09-06** | Designed (§8); not run |
| Host catalog, route, receipts, loop, panel, views, act facility, library, endpoint | SWBPIPE owner (DEP-001) | Host-owned checks (SQ-27) | Joined by DEL-09-06/07/09 | Owner-reported building; nothing received |
| Human acts A4, A5, A10, A12, A13 | The person (Engineer A in fixtures) | — | Observed, never performed, by examiners | None performed |
| OI-021, OI-003, U-03, D5, D6 | The owner (with named co-owners) | — | — | Open or pending |

---

## 6. Staging without PEC or Domains (REQ-006; AC-006)

| Stage | Content | Needs | Does not need | Output standing |
|---|---|---|---|---|
| **ST-0 Definitions** (now) | v0.3/v0.1 definitions; this contract; relay file; DEL-09-09 cases | Accepted basis | Any host input | *illustrative* |
| **ST-1 App-local executable fixtures** | C/P/ACT/RS/AS/WD/EXEC/ADAPTER fixture runs on test doubles; App run through stock Codex for the App side of the workflow | App construction (later undertaking); DEL-09-01 protocol | Host, OI-021 | *test-double* per file |
| **ST-2 Relay and answers** | `RELAY_QUESTIONS_SWBPIPE.md` relayed; answers recorded | The human; SWBPIPE session | PEC, Domains | Answers with custody; not delivery |
| **ST-3 Activity selection** | OI-021 decided; increment SoW finalized (DI-1…DI-3) | Owner; SQ-04/SQ-05 answers | PEC, Domains | Final increment SoW (future) |
| **ST-4 Host contributions and focused host examination** | Host candidate identified; CA/E (and/or CA/X) exercised; V4-EXM-20…23 by DEL-09-07; V4-EXM-25 by DEL-09-09 | DEP-001 contributions; SQ-01/SQ-02; person's acts | PEC, Domains | *actual host*, candidate-bound |
| **ST-5 Joined V4-EXM-14 round trip** | §8 witness on identified App and host candidates | ST-4 plus DEL-02-02 registration (later undertaking) | PEC, Domains | Completion evidence for OUT-003 (future) |
| **Later** | Domains research/design-candidate increment; PEC coordination | Their own contracts | — | Outside this activity |

Rules: ST-1 and independent App construction never wait for ST-4/ST-5
(REQ-006). A stage's output never claims a later stage. A first-host pass is
not evidence of longer-work recovery (DEL-09-05). Each stage that depends on
an input names it; a defined contract is not treated as an available input
(AC-006).

---

## 7. Evidence standing (REQ-005, REQ-007; AC-005, AC-007)

### 7.1 Examination evidence labels (C-v0.3 mapping, consumed)

| Label | Can support |
|---|---|
| *illustrative* (CONTRACT-REVIEWED / DEFINED) | Completeness of the definition only |
| *test-double* (FIXTURE-EXECUTED / EXECUTED on a double) | That expectation on that double; nothing about the host |
| *actual host* (HOST-OBSERVED / EXECUTED on an identified candidate) | That candidate, configuration and date only |
| AWAITING INPUT / HELD / NOT-OBSERVED | Nothing; recorded as a gap |
| LIMITED (partial) | As stated in the limitation |

Replay of recorded exchanges supports seam checks (V4-EXM-02) and never
substitutes for the live joined witness or a real act. Browser evidence never
replaces required native observation (V4-EXM-04).

### 7.2 External contribution standing ladder (REQ-005; PROPOSED (W9))

Each external item holds exactly one standing, each claimed only with its
evidence:

**prepared** (App file exists) → **relayed** (delivery to the SWBPIPE session
observed) → **answered** (a returned answer, with source and custody) →
**committed** (an explicit statement of commitment by the SWBPIPE owner) →
**delivered** (an identified contribution: revision, candidate) →
**adopted** (the App receiving side records use of it, per file/version) →
**examined** (candidate-bound observation, with outcome).

Unknown custody or absent evidence is shown as such. A stated intention is
**answered**, not **committed**. Nothing moves up the ladder by inference.

---

## 8. What the V4-EXM-14 joined witness will need (OUT-003; REQ-002, REQ-003, REQ-007; AC-003, AC-004, AC-007) — designed, not run

### 8.1 Completion rule

OUT-003 is complete only when an **actual** joined round trip has run on
**identified** App and host candidates: the reviewed workflow carried to the
host, adapted/refined there, and made usable in the App, with each case below
observed and its outcome recorded as passed, failed, blocked, not run or
inconclusive. Definitions, fixtures, test-double runs, registration, partial
or unrun records, and honest absence reports do not complete it
(SoW AC-003, AC-007; VER-007). No favorable human approval is a completion
condition (REQ-007).

### 8.2 Cases

| Case | What is observed | Built on | Inputs still needed | State |
|---|---|---|---|---|
| **W14-00 Identification** | App candidate (build, stock Codex version actually used, model/server), host candidate (source revision, build, configuration), date, invented material identity | V4-EXM-01 | SQ-27 (a); App candidate (later undertaking) | AWAITING INPUT |
| **W14-01 Transfer App → host, unadapted** | exported → relayed → received links; origin *project* kept; holding library per link | EXEC RT-1, TR-1…TR-6 | SQ-17 (a), (d); DEL-02-02 registration (later) | AWAITING INPUT |
| **W14-02 Adaptation** | New host identity with derived-from; checkpoint comparison preserved/changed/removed/added; no identity or act inheritance | EXEC RT-2, RT-3, AD-1…AD-6 | SQ-18 (b), (c) | AWAITING INPUT |
| **W14-03 Required tools and unsupported capability** | Compatibility report on the host's actual edition (available tools **present**); one explicit unsupported/missing outcome observed and shown to the person, with no fabricated tool execution | EXEC MT-1, MT-3, MT-10, MT-15; TF-3/TF-4 | SQ-11; SQ-17 (b), (c) | AWAITING INPUT |
| **W14-04 Checkpoint hold under direct autonomy** | (i) A5 `CP-accept` with a direct grant for the operation's class (V-CP1): direct request *not permitted* naming the constraint; separate proposal queued; waits for A5. (ii) E1c `CP-check` after direct application under ⟨set-2⟩: run waits for A4 on S-4; nothing releases it without A4 | EXEC CH-1, CH-27; WD I-7; C V-CP1, T15–T16 | (i) SQ-02; (ii) SQ-01, SQ-03; SQ-05; the person's A12 and A4 | AWAITING INPUT |
| **W14-05 Real act, faithfully recorded; fabrication negatives** | Engineer's actual A5/A10 (T11) or A4 captured by the host facility; App/loop record with actor ≠ recorder, bound content identity, capture-evidence reference. Negatives: success, *queued*, receipt, A14, model text, elicitation answer → no act | EXEC CH-2, CH-28, CAP-6; WD-EX R-9; ADAPTER XF-31, XF-33 | SQ-01; an actual person performing the act on invented material (DEP-09-06-024) | AWAITING INPUT |
| **W14-06 Content change after an act** | Edit to bound content → act-lapsed event; before resume "waiting — lapsed"; after resume re-held (EXEC §4.7); history preserved; no invented current act | EXEC CH-6, CH-7, CH-10; T14 | SQ-03 (b); host lapse display (SQ-23) | AWAITING INPUT (CH-8 (ii) HELD on U-03) |
| **W14-07 Interruption and replay** | Observation lost while waiting; recovery rebuilds dispositions from the record; recovered events not back-filled; held call dispatched unchanged; inspection replay issues nothing | EXEC CH-3, CH-4, CH-5, CH-21, RP-1…RP-8 | SQ-09 (c); SQ-19 (c) | AWAITING INPUT |
| **W14-08 Supplied / adopted / observed** | App side: supplied guidance per thread/turn (HOSTING §8.2); host side: per-turn guidance if recordable, else *unknown*; adoption *unknown*; observed behavior from run records | EXEC RT-5 | SQ-19 (a), (b) | AWAITING INPUT |
| **W14-09 Host → App refinement usable in App** | Host revision relayed, opened read-only, refined as a draft, registered with derived-from; a run of the refined identity starts with every checkpoint *not reached* and imports no act | EXEC RT-6, RT-8, HR-1…HR-7 | SQ-18 (a); DEL-02-02 (later undertaking) | AWAITING INPUT (DEL-02-02) |
| **W14-10 Revision and replay history** | Several revisions and a same-name collision shown with origins and holding libraries; replay reads the resolved revision recorded for the run | EXEC RT-7, RP-5; WD-EX E4 | SQ-18 (a) | AWAITING INPUT |

### 8.3 What cannot substitute

- A test-double run, a recorded replay, or a DEL-09-07/09-09 component pass
  for any W14 case (V4-EXM-14: "a portable file or successful registration
  alone does not prove compatible execution").
- An agent-authored or conversation statement for W14-05.
- Transport acknowledgment or session de-duplication for a one-effect claim.
- A pass on an earlier candidate after the candidate changes (V4-EXM-03);
  affected cases reopen without weaker criteria (V4-EXM-05).

---

## 9. External contribution and evidence account (OUT-004; REQ-005; AC-005)

| # | Contribution needed | Supplier | Relay question | Point of need | Standing |
|---|---|---|---|---|---|
| EC-01 | Capture-evidence references for host-captured acts | SWBPIPE owner | SQ-01 | Before positive checkpoint cases | prepared |
| EC-02 | Constraint receipt or host-held declaration | SWBPIPE owner | SQ-02 | Before V-CP1 family | prepared |
| EC-03 | Subject/change-item identities; resulting objects | SWBPIPE owner | SQ-03 | Before binding/lapse cases on a host | prepared |
| EC-04 | Candidate operations, check and environment | SWBPIPE owner (input to OI-021) | SQ-04 | Before connected-activity SoW | prepared |
| EC-05 | Policy for the operation; host reserved list; adoption of treatments | SWBPIPE owner | SQ-05, SQ-06 | Before operation-policy production contracts | prepared |
| EC-06 | Basis, staleness, identity, outcomes, undo, exposure | SWBPIPE owner | SQ-07…SQ-11 | Before integrating an actionable host operation | prepared |
| EC-07 | External seam, enablement, origin, locality, data rule | SWBPIPE owner | SQ-12…SQ-16 | Before CA/X live examination | prepared |
| EC-08 | Workflow receiving, adaptation, run records, supplied guidance | SWBPIPE owner | SQ-17…SQ-20 | Before W14 host-side cases | prepared |
| EC-09 | Views, act display, findings, faithful-record operation, proxy capture | SWBPIPE owner | SQ-21…SQ-25 | Before panel receiving | prepared |
| EC-10 | One new operation for the extension trace | SWBPIPE owner | SQ-26 | Before any extension claim (DEL-09-09) | prepared |
| EC-11 | Identified candidates; host-owned checks and witnesses; relay form; actual engineer for joined witnesses | SWBPIPE owner; the person | SQ-27 | Before any candidate-bound result | prepared |
| EC-12 | The OI-021 selection | Owner via outside SWB session with App/shared owner | — | Before connected-activity SoW | open |

"prepared" means the question exists in `RELAY_QUESTIONS_SWBPIPE.md`; relay is
**not observed**. DEP-001 standing remains *owner-reported building before
agent-action integration* — not delivery, adoption or live readiness.

---

## 10. Excluded acts and their owners (REQ-008; AC-008)

| Excluded act | Owner | This contribution's part |
|---|---|---|
| Catalog, proposal, policy, grant display, record, loop, panel, declaration, execution-compatibility, adapter and hosting construction and focused checks | DEL-03-01, DEL-03-02, DEL-04-01, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-02-01, DEL-02-03, DEL-03-03, DEL-01-01 (CLM-003) | Joins their meanings in §2–§4; performs none |
| Review, registration, selection policy, drafts | DEL-02-02 (later, D1) | Named in W14-01/W14-09 |
| SWB domain objects, catalog, route, receipts, views, loop, panel, act facility, library, endpoint, host execution | External SWBPIPE owner (CLM-004; DEP-001) | Questions only (relay file) |
| OI-021 operation/autonomy/environment; OI-003 extension; U-03; D5; D6 | The owner with named co-owners (CLM-005) | Recorded as open; never decided |
| Every human act (A4, A5, A6, A7, A10, A12, A13); professional reliance; engineering approval | The person; the accountable professional | Never performed, inferred or recorded without capture evidence |
| Standalone qualification; local host qualification; external control and extension examination; longer-work recovery; replacement packet | DEL-09-02; DEL-09-07; DEL-09-09; DEL-09-05; DEL-11-03 (CLM-006) | Coordinated through §5 and §6; not performed |
| Relay of files | The human | §4 ledger in the relay file |
| **Retained here** | **DEL-09-06**: the complete activity definition, its joining, and OUT-003 | — |

---

## 11. Interfaces

### 11.1 Expected from suppliers

| Supplier | Element | State |
|---|---|---|
| C, P, ACT, AS, RS, LOOP, PANEL, WD, WD-EX, HOSTING | As cited per step in §2.3 | Read at `ba0b37123` |
| EXEC | Compatibility report; hold machine; transfer trace; RT fixture design; RT-11 evidence account | Read at `e20a3ae8d`; RT-11 names DEL-09-06 as joined-witness owner |
| ADAPTER | Channel states; carriage assurance; XF inventory | Read at `e20a3ae8d` |
| DEL-09-09 | V4-EXM-25 joined cases XC-*; extension trace | `EXTERNAL_TRACE_CASES.md` (this run) |
| DEL-09-07 | V4-EXM-20…23 on CA/E | Not in this undertaking |
| DEL-02-02 | Registration, drafts | Not in this undertaking |
| SWBPIPE owner | EC-01…EC-11 | None received |
| The owner | DI-1…DI-8 | Open or pending |

### 11.2 Provided to receivers

| Receiver | Provided |
|---|---|
| DEL-09-07 | Step map §2.3 for CA/E; staging §6; evidence ladder §7 |
| DEL-09-09 | Step map for CA/X; W14-04/05 act cases shared with XC-09/10; relay file SQ-12…SQ-16, SQ-26 |
| DEL-02-03 | W14 case needs against RT/CH/MT cases; confirmation that RT-11 is received as an evidence account, not a witness |
| DEL-05-01, DEL-05-02, DEL-04-03 | Joined observation needs (W14-04…W14-08) |
| SWBPIPE owner (via the human) | `RELAY_QUESTIONS_SWBPIPE.md` |
| The owner | §2.5 decision/input account |

---

## 12. Findings (reported; scope and Wave-1/W7/W8 text unchanged)

| # | Where | Finding | Proposed disposition |
|---|---|---|---|
| F-1 | SoW REQ-003/AC-003; EXAMINATION V4-EXM-14; D1 | V4-EXM-14 completion needs host→App refinement "made usable in App", which needs DEL-02-02 registration. D1 leaves DEL-02-02 for a later undertaking, so OUT-003 cannot complete within this undertaking even with every host input (W14-09) | Record at C1 as a staging fact; no scope change |
| F-2 | Dependencies.csv (DEP-09-06-012…024) | Only package-level rows exist for PKG-03 and PKG-02; there are no deliverable rows to DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-01, DEL-04-02, DEL-01-01 or DEL-02-01, all of which this contract consumes; nor coordination rows with DEL-09-07/09-09/09-02 (CLM-006) | Register repair at C1 (mirror rows; new relationships via `project-dag` departure) |
| F-3 | SoW TBD-002, DEP-09-06-022/-023 | Still call OI-001/OI-002 open; DECISION-1 D2/D3 now rule them for App/shared contracts, leaving operation-specific additions under OI-021 | C1 pointer, as for other SoWs |
| F-4 | D1 scope; SoW CLM-006 | DEL-09-07 (local host qualification with the same activity) and DEL-09-01 (examination infrastructure) are outside this undertaking. The step map for CA/E has no in-undertaking joined examiner, and the evidence protocol (V4-EXM-04) has no supplier yet | Record at C1; DEL-09-06 keeps the joined responsibility (CLM-002) |
| F-5 | WD-EX E1 | E1 declares only the agent's examination (OP-C3), while the accepted activity names "a non-mutating check" and C supplies a host check (OP-C12). If the real workflow is to show both standings, WD-EX could add L-CA-1's optional OP-C12 | DEL-02-01 may adopt; otherwise L-CA-1 stays local |
| F-6 | EXEC §2 HP-1…HP-3; ADAPTER GC-3/GC-5; DECISIONS_PENDING_2 D6 | For CA/X and for App runs, the checkpoint-hold-under-direct case (W14-04) depends on either host-held evaluation (SQ-02) or an App hold point (D6, pending). Neither is available, so the SoW's AC-004 on the App side has no enforceable route yet | Keep W14-04 on the host run (CA/E) first; carry D6 |
| F-7 | ACT FX-20, AS F2, RS E7, PANEL PC-22, WD-EX R-5a (V2 MAJOR-1) | These still scope T15 as "OP-C9 class / support labels"; this file uses C T15 (class P-03; scope {FX-W1; {S-4}}) | Consumers re-point in their Wave-2 sweep, as V2 assigns |
| F-8 | HANDOFF_SWBPIPE_DOMAINS.md | Its "Autonomy and human acts" row asks how "human approval/Checked/reliance differ". Under R-4, "approval" means only A6; the relay (SQ-05) uses canonical names | C1 pointer from HANDOFF to the relay file (brief) |
| F-9 | Brief inputs | Merge `98b1723b` is absent from this clone; blob identity was verified at `ba0b37123`/`1c36b6d97`/`e20a3ae8d` instead | None; recorded in header |

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-021}` operation(s), non-mutating check, autonomy, environment, acting-surface variant (DI-1…DI-3) | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Draft contract only; FX-PIPE-01 proposed fixture; OP-C11-dependent production HELD |
| Operation-specific reserved additions (OI-021 residue of OI-001) | Same owners; host names its list (V4-HI-30) | Before operation-policy production contracts | D2 applied to App/shared contracts only |
| Host adoption of D2/D3 and treatments (DEP-001) | SWBPIPE owner | Before any enforcement claim | Treatment behavior is receiving meaning |
| DEP-001 contributions EC-01…EC-11 | SWBPIPE owner via the human | Per §9 | All W14 cases AWAITING INPUT |
| Actual human acts for W14-04/05/06 (DEP-09-06-024) | The person performing them | At witness execution | Positive cases defined only |
| D5 data boundary (pending) | Owner | Before enabling a live CA/X candidate | CA/X live stage blocked |
| D6 App hold points (pending) | Owner; DEL-03-03 with DEL-02-03 | Before App-side hold fixtures | W14-04 on the host run first (F-6) |
| U-03 multi-row A4 purpose after partial lapse | DEL-04-01 with the owner | Before re-hold/lapse fixtures run | W14-06 partial-lapse variant HELD |
| DEL-02-02 registration (later undertaking, D1) | DEL-02-02 owner | Before W14-01/W14-09 | OUT-003 cannot complete in this undertaking (F-1) |
| DEL-09-01 evidence protocol; DEL-09-07 local qualification (outside D1) | Their owners | Before candidate-bound results | Labels per C mapping only |
| `UNRESOLVED{OI-013}` / `UNRESOLVED{OI-014}` placement | Shared contract owner with SWB implementation owner; App/shared owners | Before implementation boundary contracts | No placement implied |
| `UNRESOLVED{OI-003}` extension promise | Owner with host contract owner | Before extension claim | Not part of the first activity; DEL-09-09 |
| Reusable workflow authoring and review (OUT-002 artifact) | Workflow maker with DEL-02-02 (later) under `create-workflow` | Before W14-01 | §3 requirements only; WF-1 fixture |

## Verification cases

Designed, **not run**. Passing them later shows definition completeness only;
the witness itself is §8.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-CA-01 Scope and activity coverage | Trace §2.1–§2.3 against the DEL-09-06 row, SOW-040/041/236/237/238/240/241, OBJ-001/004/008 and decision 05 | Four user activities, two named expressions and all five activity steps (plus frame steps) mapped to contributions, owners and checks; OI-021 shown open, no final operation-specific SoW claimed | VER-001 (AC-001) |
| VC-CA-02 Workflow requirements | Check §3 against V4-WF-01…06 and WD-v0.3; check the fixture candidate and L-CA-1 reason | Identity, assumptions, inputs/tools, checkpoints, outputs/evidence, revision history required; incompatible/missing tools and checkpoints treated explicitly; no workflow claimed authored | VER-002 (AC-002) |
| VC-CA-03 Round trip design | Check §4 and §8 against V4-EXM-14 and EXEC §6 | Every link separate; original and revised identities kept apart; W14-00…W14-10 cover transfer, adaptation, tools, checkpoints, interruption, revision/replay, supplied/adopted/observed | VER-003 (AC-003) — design only |
| VC-CA-04 Act distinctions | Check W14-04/05/06 and §2.3 CA-H against V4-HI-25/31/32/42, D2, R-5, R2-20 | Hold under direct autonomy; faithful record with actor ≠ recorder and capture evidence; fabrication negatives; lapse preserves history; no always-reserved list created; no favorable decision required | VER-004 (AC-004) |
| VC-CA-05 External account | Check §9 and the relay file against DEP-001, OI-021 and REQ-005 | Every external item has owner, point of need and a single standing; nothing beyond *prepared*; custody unknown shown | VER-005 (AC-005) |
| VC-CA-06 Staging | Check §6 against decision 05, PRD §2.3/§3.1/§8 and CLM-006 | No PEC/Domains prerequisite; ST-1 independent; each stage names its inputs; no stage claims a later one | VER-006 (AC-006) |
| VC-CA-07 Evidence standing | Check §7 and §8.1/§8.3 against EXAMINATION §1–2 | Candidate/configuration/date required; replay, test double and component passes cannot complete OUT-003 | VER-007 (AC-007) |
| VC-CA-08 Ownership | Check §5 and §10 one-for-one against REQ-008 and CLM-002…006 | Every excluded act has its owner; DEL-09-06 keeps joining and OUT-003; no policy decided; no shared construction assumed; no acceptance, release, replacement or reliance claimed | VER-008 (AC-008) |
