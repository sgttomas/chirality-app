# Workflow execution compatibility, checkpoint hold and round trip
- Contribution: DEL-02-03/EXEC-v0.2 (supersedes DEL-02-03/EXEC-v0.1, committed at `e20a3ae8d`, file sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (required-tool check and checkpoint receiving behavior — definition only, no code), OUT-002 (App/host transfer and adaptation contract), OUT-003 (missing-tool, checkpoint-hold and round-trip fixture design — none run); REQ-001…REQ-007; AC-001…AC-007 through designed VER-001…VER-007
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 9a921ba500271c441e64db2e1f34acf41c95fa7821d6dff3d8659352bb4db7fb; `P/docs/PRD.md` V4-WF-01…06, V4-AUT-03, V4-AUT-05, V4-EXE-01, V4-EXE-03, V4-REC-03, V4-REC-05; `P/docs/HOST_INTEGRATION.md` V4-HI-02, -04, -23, -25, -30…32, -40…42, -50…52, -70/71; `P/docs/EXAMINATION.md` V4-EXM-14, V4-EXM-22; `P/docs/ARCHITECTURE.md` V4-ARC-20/21; SCC-CASE-002 `Case_Datasheet.md` sha256 6acdc6c4e484ab7b46ba7d45a347961bc69b3e624bd29ef58a613ec6c66a71a6 (M1 rows naming DEL-02-03 as producer and receiver); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e) D1–D4; owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (OWNER_DECISIONS.md at `f05c7e4cd`, sha256 a9869129…8ad2c) D5, D6
- Consumed inputs:
  - **Integration rulings.** R1_RESOLUTIONS.md sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4 (R-1…R-10); R2_RESOLUTIONS.md sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088 (R2-1…R2-21); R3_RESOLUTIONS.md sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf (R3-1…R3-4). Brief: BRIEFS.md (working copy, sha256 58de4a2c48f651391383aecf85fa5e9073d2cc34240c37cdab216a16481c698f) "Common brief", "Owner rulings now in force", "Wave 2 — common additions", "W7".
  - **Wave-1 v0.3 files at commit `ba0b37123`** (read with `git show`, not the working tree):
    - DEL-02-01/WD-v0.3 `WORKFLOW_DECLARATION.md` sha256 84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb (§3.4, §4.2, §4.3, §4.4, §4.6, §4.7, §6, §11, §12);
    - DEL-02-01/WD-EX-v0.3 `EXAMPLES.md` sha256 0f1058d7f0990e766b3effc3d3de24fc16383197874cced1f5b4212419cf018d (E1–E7, L-WDEX-1…15);
    - DEL-03-01/C-v0.3 `CATALOG_AND_READ_BASIS.md` sha256 ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26 (§2, §3, §3.1, §3.2, §4, §5.3, §5.4, §10 FX-PIPE-01);
    - DEL-03-02/P-v0.3 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` sha256 ec0db87f239bc42e2e3e953d660ce3c4ceddf605d7b98cf1393f97a099b699cf (§3.1, §3.3, §4.1–§4.5, §5, §9, §10, §13);
    - DEL-04-01/ACT-POLICY-v0.3 `ACT_AND_POLICY_CONTRACT.md` sha256 b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128 (§2.1–§2.5, §4, §5.4–§5.6, §12);
    - DEL-04-02/AS-v0.3 `AUTONOMY_AND_STANDING_EXCHANGE.md` sha256 7b634137bb8402f3eaedc943dab0c5f1114b9d4433d2b94e13540ac0bf8e0514 (§4 checkpoint indicator; U-09, U-11, U-13, U-14);
    - DEL-04-03/RS-v0.3 `RECORD_SEMANTICS.md` sha256 925f35ca27bd7d1e71a375883ada9903267408af57312eed1ae02b47776a3528 (§3, §4 R2/R3/R8/R9/R11/R13, §5, §6, §7 L-0…L-12, §10);
    - DEL-05-01/LOOP-v0.3 `LOOP_RECEIVING_CONTRACT.md` sha256 6b771c8027787193d536fa3507214a8cc579d6ec2f476ee880609c920b6f25c7 (§2.1, §2.3, §2.4, §6.3, §11 FX-C1…C13, §13);
    - DEL-05-02/PANEL-v0.3 `PANEL_RECEIVING_CONTRACT.md` sha256 4c47764d3af434c23e63dcc2c10d28f18a4a94546d63d452855c471cfe47bee9 (§3.2, W-5a…W-5g, PC-20…PC-29);
    - DEL-01-01/HOSTING-BOUNDARY-v0.3 `HOSTING_BOUNDARY.md` sha256 34c3383402aabe6e9347aa2f111318538c4a2a4ca85adb8fffff7e439fdde94e (§6.1 request kinds, R9, §8, §8.2); generated `json-schema/experimental/codex_app_server_protocol.v2.schemas.json` sha256 34f28a486d00fbd20e5da0b0da3422d1d6e20ec897d12b31408f87499198f458 (presence of `turn/interrupt` only).
  - DEL-02-02, DEL-01-04, DEL-02-04: accepted SoWs only (later undertaking, D1). SWBPIPE host evidence: none received (DEP-001).
  - **v0.2 inputs (sweep A1).**
    - R4_RESOLUTIONS.md at commit `f05c7e4cd`, sha256 50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24 (R4-1…R4-21; binding).
    - OWNER_DECISIONS.md at `f05c7e4cd`, sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c: `APP-V4-FIRST-INCREMENT-20260928-DECISION-2`, D5 (user flexibility on model destination) and D6 (App hold deferred to SWBPIPE SQ-02).
    - DEL-09-06 at commit `b4030fe4b`: CA-v0.1 `CONNECTED_ACTIVITY_CONTRACT.md` sha256 685349b25981ca8333929207890514120d63753cdedd67ae0bad986fc5d45e62 (W14-00…W14-10, DI-7); RELAY-v0.1 `RELAY_QUESTIONS_SWBPIPE.md` sha256 3e34575def8d1fef63b5f5e64f0f90a0984d03b8b42f61fe899dd2eab023b2d1 (SQ-01…SQ-27; §3 map of EXEC host items).
    - DEL-03-03/ADAPTER-v0.1 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` at `e20a3ae8d`, sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074 (§5.1–§5.3 carriage assurance and GC-1…GC-5; §7.7; OC-11; U-X3; XF-25, XF-26).
    - DEL-03-01 C at `f05c7e4cd`: unchanged from C-v0.3. The R4-20 App-file subject and App-side library are **not yet present**, so the local labels L-EXEC-19 and ⟨fx-app-import⟩/⟨rev-A3⟩ stay, with their reasons.
    - Wave-1 v0.3 files: unchanged from `ba0b37123` at `f05c7e4cd`. Their v0.4 revisions under R4 are concurrent and not read; R4 text is cited instead.
- Receivers: DEL-03-03 (answer to ADAPTER U-X3, §3.6); DEL-02-01 (WD confirmations and amendments requested in §11; CASE-002 M1 workflow-contract row); DEL-05-01 (hold-machine semantics for host loops; CASE-002 M1 execution-owner row, OUT-001/OUT-003, REQ-007, VER-008); DEL-04-03 (R8 checkpoint events and transfer records; RS §10 DEL-02-03 row; RS U-17/U-18/U-22/U-23/U-24); DEL-09-06 (local transfer/adaptation evidence account, DEP-02-03-014; VER-004/VER-007). Named but outside this undertaking (D1): DEL-02-02 (CASE-002 M1 workspace row, changed-draft return, VER-004/VER-005 of DEL-02-02). Also read by DEL-05-02 and DEL-04-02 for display of the resolved W7 items.

---

## Changes from v0.1

| R4 ID (source finding) | Change in v0.2 | Where |
|---|---|---|
| R4-1 (D5, SETTLED by DECISION-2) | The App run's **model destination** is recorded and shown as information only. It never gates enablement, a check or a transfer. Report element CR-14; *supplied* and *observed behavior* links name it for App runs | §3.3, §6.1, RT-5 |
| R4-2 (D6 deferred to SWBPIPE SQ-02) | HP-1 (interposed App code) and HP-2 (reliance on `turn/interrupt`) are **not adopted**. HP-3 remains a permitted best effort (D3). New HP-4: the App initiates nothing for a holding run. New HP-H: a host-side hold, pending SQ-02. App-side holds are `UNRESOLVED{D6}`. Hold support is re-valued: App-run holds without host enforcement are **not enforceable**. *Action during hold* is always recorded. U-E1 is restated as `UNRESOLVED{D6}`; U-E20 is withdrawn (nothing relies on `turn/interrupt`). F-10 is carried to C1 | §2, §3.6, §4.2 HD-4, MT-2, CH-22, UNRESOLVED |
| R4-3 (F-2) | Resume point HD-5 and re-hold RH-1…RH-9 **adopted** across the set | §4.2, §4.7 |
| R4-4 (F-4) | No resumption, post-end acts and *continues ⟨run⟩* **adopted** (PROPOSED standing kept per R4-4) | §4.9 |
| R4-5 (F-3) | SP-6 **adopted as PROPOSED**; U-E4 stays open for the owner | §4.5, UNRESOLVED |
| R4-6 (F-5) | Refused, pending and unconfirmed A12 rules and "supersedes only when established" **adopted**; U-E6 closed | §4.10 |
| R4-7 (F-1) | MX-3, MX-6 and MX-8 **adopted** into WD §4.3.7; R2-18/R3-3 **CONFIRMED** by DEL-02-03 | §4.11 |
| R4-8 (F-8) | "Checkpoint hold not enforceable on this surface" **adopted** as a WD §4.2.4 *unsupported* reason | §3.6 |
| R4-9 (F-13) | Grant-setting subject without an A8 = the setting content the declaration names. A declaration naming none is **invalid** for A12 (INTEGRATION). U-E5 closed; new case CH-29 | §4.10, §4.14, CH-29 |
| R4-10, R4-11 (F-6, F-7) | RS elements requested here are adopted into RS v0.4 by R4; the findings are closed | §11 |
| R4-12 (F-9) | Elicitation and user-input answers are not act evidence: CAP-6 **adopted**; HOSTING updated by R4 | §5 |
| R4-13 (ADAPTER F-4) | CAP-1: where A13 is captured App-side is set by DEL-04-01 (U-X1). An App-side Codex configuration an agent could write is never A13 evidence | §5 |
| R4-14 (ADAPTER F-1) | The constraint travels with a **carriage assurance**. For App runs only *host-held* counts (App-assured requires HP-1, not adopted under R4-2). Model-supplied carriage alone makes the A5 hold support *not established*. This answers ADAPTER U-X3 for GC-3 and GC-5 | §3.6, §8 |
| R4-15 (ADAPTER F-8) | Author identity may be *unverified*. A transfer's *exported* link names the exporter as observed, not as verified | §6.3 TR-4 |
| R4-19 (V2 minors) | R3 and R4 added to Consumed inputs. CH-10 already uses T16a | Header |
| R4-20 (F-15) | C at `f05c7e4cd` has no App-file subject or App-side library yet. The L-EXEC-19, ⟨fx-app-import⟩ and ⟨rev-A3⟩ local labels stay with their reasons, to be re-pointed when C adds them | §7, F-15 |
| R4-21 (F-16) | Reached-when kind (a) on a harness capability is **not holdable** in App runs pending D6; hold support reports *not enforceable*. F-16 closed | §3.6, MT-15 |
| DEL-09-06 citation request | Host-dependent items and cases cite RELAY-v0.1 SQ IDs; evidence account RT-11 maps to CA-v0.1 W14 cases | §7, §8, UNRESOLVED |
| C1 carry (R4 "Carried to closeout C1") | F-10, F-11, F-12 and U-E3 (U-03) carried to closeout C1 | §11, UNRESOLVED |

---

## 0. Reading this definition

**What it defines.** Three things this deliverable owns (SoW OUT-001, OUT-002;
WD §10 "Checkpoint hold machine, re-hold, ended-run resumption, required-tool
check, transfer"):

1. the **required-tool compatibility report** (§3);
2. the **checkpoint hold machine**, including interruption and replay (§4) and
   App-side act capture (§5);
3. the **App→host transfer and host→App refinement trace** (§6);

plus fixture design (§7) and the resolution of every item Wave-1 held for W7
(§8).

**What it does not define.** Declaration meaning (DEL-02-01), catalog meaning
(DEL-03-01), proposal outcomes (DEL-03-02), act names and policy (DEL-04-01),
record fields (DEL-04-03), host-loop receiving (DEL-05-01), panel receiving
(DEL-05-02), registration (DEL-02-02), native act controls (DEL-01-04), the
external adapter (DEL-03-03) and the joined witness (DEL-09-06). It selects no
wire field, type, transport, hash or canonicalization algorithm, persistence,
process/thread placement or shared-component placement (OI-013, OI-014,
TBD-003, TBD-004).

**Naming.** Bold phrases are *semantic element names*, not wire names. Act
names are canonical A1–A14 (R-1). Dispositions are the six shared values
(WD §4.3.4). Class values are the five of C §3.1 (R2-1). Supplier method names
such as `turn/interrupt` are cited as observed facts about Codex 0.158.0 in
generated types (W11); citing one selects nothing.

**Labels.** SETTLED (accepted basis or owner ruling, cited), DERIVED,
INTEGRATION (R1/R2/R3/R4 integrator rulings, cited). **PROPOSED (W7)** marks a
design choice made here, open to comparison and to owner revision.
**ADOPTED (R4-n)** marks a PROPOSED (W7) rule that R4 adopted across the set,
keeping any standing R4 gives it (e.g. R4-4 and R4-5 stay PROPOSED).
`UNRESOLVED{…}` is an open owner choice, never a permission or default.
Local fixture cases are `L-EXEC-n`, each with its reason.

---

## 1. Settled distinctions this contribution relies on

| # | Distinction | Citation | Use here |
|---|---|---|---|
| E-A | The product checks a selected workflow's required tools against the current host and tells the person which are missing | V4-WF-04; SoW REQ-001 | §3 |
| E-B | At a declared checkpoint the act is requested and the run does not record it as done until the person performs it; checkpoints override autonomy | V4-WF-05; V4-HI-42; D2 "No autonomy grant widens past … a declared checkpoint" | §4 |
| E-C | Success, a queued proposal, a receipt or findings supply no human act | V4-HI-25; V4-AUT-03; WD I-2 | §4.5 |
| E-D | A human act binds to content, scope and purpose, and lapses visibly when content changes | V4-REC-05; V4-HI-32 | §4.5, §4.7 |
| E-E | Only observed events are shown as having happened; unobserved outcomes are unknown | V4-EXE-03; P §4.1 rule 3 | §4.12 |
| E-F | Source-qualified identity; no silent rebinding | V4-WF-03; WD §6 | §6 |
| E-G | App workflows can be carried into a host and adapted; host workflows can be opened and refined in the App | V4-WF-06 | §6 |
| E-H | Round trip observes selected/resolved bytes, what was supplied, provider-adopted and observed behavior separately; portability or registration alone proves nothing | V4-EXM-14 | §3.5, §6.1 |
| E-I | Reserved to the person: A4, A5 (where a proposal is required), A6, A7, A12, A13 (enabling) | D2 (SETTLED); R-1, R2-2, R2-3 | §4, §5 |
| E-J | App routine tool permission (A14) is the user's own Codex setting and never stands in for a reserved act; hosts have no classifier mode | D3 (SETTLED); R2-8 | §4.2, §5 |
| E-K | The standalone App executes through stock Codex; no other App engine or presumed common service | SoW CLM-003; V4-ARC-20 | §4.2 enforcement boundary |
| E-L | Host execution, catalog, act facility, receipts and library are the external host owner's; files are human-relayed | SoW CLM-002/003, DEP-001 | §3, §6 |

Canonical checkpoint rules consumed unchanged: the closed act list A4, A5, A6,
A7, A12 (WD §4.3.1; AP §4.1); reached-when kinds (a)/(b)/(c) and the
independent subject class with its validity rules (WD §4.3.1, R2-17, R3-1,
R3-2); independence rules I-1…I-7 (WD §4.3.3); subject binding SB-1…SB-4
(WD §4.3.6); act-declined and run-ended events (R2-5); lapse sequence before
resume (R2-19); capture-evidence requirement (R-5, R2-20); governing
checkpoint constraint (R2-12).

---

## 2. Parties, execution placement and the enforcement boundary

| Concern | Owner | This contribution |
|---|---|---|
| Check meaning (outcome vocabulary, pass rule) | DEL-02-01 (WD §4.2.4) | Consumes unchanged; defines the report and evaluation order (§3) |
| Check execution for App-selected workflows and App-carried runs | DEL-02-03 | §3 |
| Check execution inside a host | Host owner; a DEL-02-03 checker only if OI-014 allocates one (PANEL §3.2) | Supplies the same meaning |
| Hold machine in App runs | DEL-02-03 | §4 |
| Hold machine in host loops | DEL-05-01 receiving; external construction; `UNRESOLVED{OI-013}`; sharing `UNRESOLVED{OI-014}` (WD §9 A-4) | Supplies the semantics; placement not proposed |
| Act capture on host content | Host act facility (V4-HI-31); capture-evidence reference is a relay question (R2-20; DEP-001) | Consumes |
| Act capture in the App | App interface (WD I-5); control construction DEL-01-04 (later, D1); record DEL-04-03 | §5 defines requirements |
| Transfer procedure and trace | DEL-02-03 (WD U-18) | §6 |
| Draft, review, registration, selection policy | DEL-02-02 (later, D1) | Routed to, never performed |
| Joined round-trip witness | DEL-09-06 | Receives §7 evidence account |

**Enforcement boundary for App runs (`UNRESOLVED{D6}`; R4-2).** The App runs
workflows through stock Codex (E-K), and routine tool permission is the user's
own setting (E-J). How the App holds its own runs was deferred by the owner to
the SWBPIPE answer to RELAY SQ-02 (DECISION-2 D6). Until then, the hold points
stand as follows:

| Hold point | Mechanism (semantic) | Where it can act | Standing (v0.2) |
|---|---|---|---|
| **HP-1 Interposed App code before dispatch** | An App component in the dispatch path to the host's external surface holds the call undispatched | Kind (a) on a host operation | **Not adopted** (R4-2; D6). Kept only as the v0.1 option record |
| **HP-2 Reliance on turn interruption** | The App interrupts a running turn after observing an arrival (supplier `turn/interrupt`, generated types at 0.158.0) | Kinds (b), (c) | **Not adopted** (R4-2; D6). Nothing in this file relies on it |
| **HP-3 Named-rule decline of a tool-permission request** | While holding, an App named rule may *decline* a tool-permission request that reaches the App, with truthful origin (R-2; HOSTING R7). It never answers affirmatively | Native tools whose requests reach the App under the user's mode | **Permitted best effort** (R4-2; D3). Tools the user's mode auto-settles are not held. HP-3 never makes a hold *enforceable* |
| **HP-4 App initiates nothing for a holding run** | While a run holds, the App starts no turn and issues no App-initiated call (e.g. `mcpServer/tool/call`, where the App is the caller) for that run | App-initiated actions only | PROPOSED (W7). This is App behavior, not interposition. It does not stop actions Codex takes inside a turn already running |
| **HP-H Host-side hold** | The host holds or refuses the run's host operations itself: host-held constraint, host-held declaration or run association, or a host hold before dispatch | Host operations of the run, on E and X | **Pending SQ-02 (b)–(d)**. When evidenced, it enforces holds for host operations only |

A checkpoint that no enforcing point covers on the acting surface is **not
enforceable** there; the check reports it (§3.6; R4-8). Every run action
observed while holding is recorded as **action during hold** (RS R11; R4-2,
R4-11). The machine never claims a hold it did not enforce (S-N; AX-002).

---

## 3. Required-tool compatibility report (REQ-001; AC-001; VER-001)

### 3.1 When a check is evaluated

| Occasion | Subject | Catalog edition used |
|---|---|---|
| **CK-1 Selection** — a workflow is selected or offered for a run | The selected identity tuple (WD §6.1), with holding library | The current host's current edition on the acting surface |
| **CK-2 Run start** — immediately before the run's first action | As CK-1 | The edition the run will be offered (LOOP: offered edition) |
| **CK-3 Edition change** — the host publishes a new edition while a report is shown or a run is live | As CK-1 | The new edition; the earlier report is kept, marked *not current* |
| **CK-4 Transfer** — before or after carriage into a host (§6.3), when the destination catalog is available | The carried identity | The destination edition; otherwise the report says *destination catalog not available* |

A report is evidence of one evaluation. It is never re-labelled, and a new
occasion produces a new report (E-E).

### 3.2 Inputs consumed

| Input | From | Rule |
|---|---|---|
| Declared part status; required tool references (reference, class, necessity, version compatibility, purpose, stage); compatible roles; delegation need | WD §3.4, §4.2.1–§4.2.2, §4.7 | Consumed unchanged; restriction ≠ requirement (WD §4.2.3) |
| Host identity; **catalog edition**; entries with operation identity and version | C §2, §3 #1 | Version **equality** only (C §3.2) unless the host publishes a compatibility statement (U-C9) |
| **Exposure** per surface (element 9) | C §3 #9 | Read directly at discovery; *unagreed* → not established |
| Availability preconditions, unavailable reason, evaluated basis | C §3 #4, §4.2 | Evaluated only when the check is asked for run-time readiness |
| Channel state (external access; A13) | C §4.1; V4-HI-52 | Surface-level, never per requirement |
| Acting surface and seat | App: external surface X; host: embedded surface E (C §8); seat role meaning (WD SEAT-1) | One report per acting surface |
| Harness capability inventory | DEL-01-01 (HOSTING §8; 0.158.0 inventory) | Names unresolved (WD U-08) → not established |

### 3.3 Report elements (semantic)

| # | Element | Meaning |
|---|---|---|
| CR-1 | **Report identity** | Identity of this evaluation |
| CR-2 | **Workflow identity evaluated** | Full tuple {kind, origin, source root, name, revision} + derived-from, with holding library (R-9, R2-20) |
| CR-3 | **Declared-part status** | declared · declared empty (required tools) · undeclared · not established (unreadable, newer contract version, unrecognized element in the category) (WD §3.4) |
| CR-4 | **Host and catalog edition** | Host identity; catalog edition; "catalog unreadable" if so |
| CR-5 | **Acting surface and channel state** | H / E / X; *channel not enabled* stated at this level (WD §4.2.4) |
| CR-6 | **Occasion and time** | CK-1…CK-4; when evaluated |
| CR-7 | **Per-requirement rows** | For each reference: reference; class (host operation / harness capability); necessity; purpose line; declared version(s); entry found (identity, version) or none; exposure value on the acting surface; availability result and reason with evaluated basis (only when evaluated); **outcome** (WD §4.2.4); reason |
| CR-8 | **Workflow-level result** | *unsupported* (with reason: role, delegation, or hold not enforceable, §3.6) or none |
| CR-9 | **Checkpoint hold support** | Per declared checkpoint: hold point and support value (§3.6) |
| CR-10 | **Pass result** | passes · does not pass · not established (undeclared), by the WD pass rule |
| CR-11 | **Run-time holds** | Required references *present, currently unavailable*, each with reason |
| CR-12 | **Limitations** | E.g. "exposure is a fixture assumption (FA-1)"; "version compatibility: equality only"; "destination catalog not available"; "evaluated on a test double" |
| CR-13 | **Evidence standing** | C's evidence-label mapping (illustrative / test-double / actual host) |
| CR-14 | **Model destination** (App runs on X) | The model the App conversation has selected, local or cloud, shown as **information only**. Host content read over X may flow to it (D5, R4-1). It is never an outcome, a gate or a pass condition |

### 3.4 Evaluation order per required tool reference

Evaluated in this order; the first matching step gives the outcome.

| Step | Condition | Outcome |
|---|---|---|
| EV-1 | Declared part undeclared, unreadable, or the category is undeclared | Whole check **not established** (FB-01, FB-02, FB-05) |
| EV-2 | Element in the required-tool category unrecognized | That reference **not established**; never skipped (WD §3.4) |
| EV-3 | Class *harness capability* | **not established** until portable names exist (WD U-08) |
| EV-4 | Catalog unreadable, or reference cannot be resolved against it | **not established** (FB-06) |
| EV-5 | No entry in the edition | **missing** (FB-06) |
| EV-6 | Declared version(s) and entry version unequal, with no host compatibility statement covering them | **version mismatch** (C §3.2) |
| EV-7 | Exposure on the acting surface *unagreed* | **not established** |
| EV-8 | Exposure *not exposed on this surface* | **not exposed on this surface** |
| EV-9 | Acting surface's channel not enabled | the reference is reported under the surface-level **channel not enabled**; never *missing* or *unavailable* |
| EV-10 | Readiness asked and a precondition fails now | **present, currently unavailable** with reason and evaluated basis |
| EV-11 | Otherwise | **present** |

Class never produces *missing*, *unavailable* or *not exposed* (C §2
invariant 5; R2-4). A reserved entry is reported present when present; its
class matters at run time only (*not permitted* for an agent call, A8
offered).

### 3.5 Pass rule and person-facing statement

The pass rule is WD §4.2.4's, consumed unchanged, extended only by CR-8's
hold-support reason (§3.6, ADOPTED (R4-8)).

Rules for what the person is told:

- **PS-1** Every required reference that blocks a pass is listed with its
  purpose line and reason (S-E).
- **PS-2** A pass is stated as "requirement check passes against ‹catalog
  edition› on ‹surface› at ‹time›". It never says "compatible", "will run" or
  "runnable" (V4-EXM-14: a portable file or registration proves nothing).
- **PS-3** A registered or selected workflow whose check does not pass stays
  registered and selectable; the report says so (VER-001 "registration
  succeeds but a requirement is unavailable").
- **PS-4** An undeclared workflow is shown "requirements undeclared — check
  not established", never "no requirements" (WD §3.4).
- **PS-5** Optional references never block; their outcomes and stated
  fallback are shown.
- **PS-6** A run-time hold (*present, currently unavailable*) is shown as a
  hold with its reason, not as missing.

### 3.6 Checkpoint hold support (ADOPTED (R4-8); values under R4-2, R4-14, R4-21)

For each declared checkpoint and acting surface the report states one value:

| Value | Meaning | Effect on the check |
|---|---|---|
| **enforced by the host loop** | Host runs on surface E: the host loop holds per DEL-05-01 (kind (a) before dispatch; stops acting after (b)/(c)) | None |
| **host-enforced for host operations** | App runs on X: HP-H evidenced — the host holds or refuses the run's host operations (kind (a) before dispatch of a host operation; for A5, a constraint carried **host-held**, R4-14). Native tool actions in the App remain observed only and are recorded as *action during hold* | None; that residual limit is listed in CR-12 |
| **not enforceable** | No enforcing point covers the checkpoint on this surface. In App runs pending `UNRESOLVED{D6}` (R4-2) this includes: every kind (b)/(c) run halt; kind (a) on a harness capability (R4-21); any checkpoint whose only coverage would be HP-1 or HP-2 (not adopted) or HP-3 (best effort only) | Workflow **unsupported**, reason "checkpoint hold not enforceable on this surface" (R4-8); check does not pass |
| **not established** | (i) Declaration invalid (FB-03, FB-13, FB-16; A12 naming no setting, R4-9) or not established (FB-04). (ii) Enforcement depends on a host answer not yet received: HP-H awaiting SQ-02 (b)–(d). (iii) An A5 constraint available only as **model-supplied** or **absent** carriage (R4-14; ADAPTER GC-3) | Check does not pass; the checkpoint is reported; cases AWAITING INPUT (SQ-02) |

An App run is *not enforceable* for a checkpoint whenever HP-H does not
cover it. This is the truthful consequence of D6's deferral; it is not a
design preference (finding F-17). HP-3 and HP-4 are applied as best effort
in every App run, and neither changes the value.

**Answer to ADAPTER U-X3 (R4-14, R4-2, R4-21).**
- **GC-3 adopted.** An A5 checkpoint on an operation used over X counts as
  enforced only with **host-held** carriage. App-assured carriage needs
  interposed code, which is not adopted. With model-supplied or absent
  carriage the value is *not established*.
- **GC-5 adopted.** Kind (a) over X is *not established* until the host holds
  the call (SQ-02 (d)); it becomes *host-enforced for host operations* once
  evidenced.

This makes S-N ("unenforced limits are stated, not implied") and V4-EXM-14's
"explicit unsupported-capability outcome" hold for checkpoints as well as for
tools. It is **ADOPTED (R4-8)** as a WD §4.2.4 *unsupported* reason.

### 3.7 Run-time divergence and report currency

- **CC-1** A report is bound to its catalog edition. On CK-3 the earlier
  report is marked *not current* and a new one is produced; neither is
  rewritten.
- **CC-2** Run-time results are recorded as their own events and never
  back-filled into the report: a loop-side *not offered* failure, a
  host-reported *not exposed on this surface* (relayed), *unavailable*,
  *channel not enabled*, *not permitted* (C §4.1; LOOP §2.3).
- **CC-3** A run whose check did not pass may still be started by the person
  (the check informs; it grants and forbids nothing). The run record carries
  the report reference; every later failure is reported as observed.
  *Unsupported* for a non-enforceable checkpoint is shown at run start; the
  run's checkpoint then records "hold not enforceable" on every arrival.
- **CC-4** A *no policy basis* entry (OP-C11) is *present*; dependent
  production is reported **held** (R2-9), never as a pass of that production.

### 3.8 Failure behavior

| ID | Condition | Behavior |
|---|---|---|
| CF-1 | Catalog unreadable | Whole check **not established**; reason shown |
| CF-2 | Workflow revision no longer resolvable (WD FB-08) | No report on substituted content; "selected revision not resolvable" |
| CF-3 | Evaluation interrupted | No partial pass; report absent or *not established* |
| CF-4 | Two surfaces give different outcomes | Two reports; never merged |
| CF-5 | Host publishes a compatibility statement | Cited in CR-7; equality otherwise (U-C9) |

---

## 4. Checkpoint hold machine (REQ-002, REQ-003; AC-002, AC-003; VER-002, VER-003)

### 4.1 Identities

| Element | Meaning |
|---|---|
| **Run identity** | The workflow run (RS R1) |
| **Checkpoint identity** | {workflow identity tuple as resolved for the run, checkpoint name}. Stable across interruption and replay (SoW REQ-002; WD §4.3.1) |
| **Arrival** | One observed reaching of a checkpoint in a run, identified by {run identity, checkpoint identity, **arrival ordinal**}. A checkpoint may arrive more than once (WD RW-4) |
| **Arrival event** | The observed event that met reached-when, with its own evidenced time (host outcome time for kind (c); output production for kind (b); the hold of the call for kind (a)) |
| **Bound subject** | The referents the declared subject class names, bound at arrival (WD §4.3.6) |
| **Performance ordinal** | Counts the satisfying acts an arrival has had (1 on first *performed*; +1 after each re-hold) |

### 4.2 What "holding" means

- **HD-1** A run is **holding** while any current arrival is *waiting*, or a
  kind (a) call is held undispatched.
- **HD-2** While holding, the run dispatches no operation and produces no
  declared output. The agent may still explain the request and may issue an
  A8 request (LOOP §2.3); conversation is not run progress.
- **HD-3** Host lifecycle continues independently: after the person's A5 the
  host may apply an item while the run holds (V4-HI-23). That is the host's
  action, not the run's.
- **HD-4** In App runs, holding is `UNRESOLVED{D6}` (R4-2). The App applies
  HP-4 and, as a best effort, HP-3. It relies on HP-H only where the host has
  evidenced it (SQ-02). Every run action observed while holding is recorded as
  **action during hold**, with its reference, never hidden. The disposition
  logic of §4.3–§4.13 is unchanged: an arrival stays *waiting* whether or not
  the hold is enforced. Only the claim of a hold depends on enforcement.
- **HD-5 Resume point.** When a current arrival becomes *performed*, or
  *resolved negatively* with a proceed or return path, the first run action
  after that change is the **resume point**. It is recorded as a
  **run-resumed event** {arrival, time, first action reference}. For kind (a)
  the first action is the dispatch of the **same** held call, unchanged
  (WD RW-2). "Before resume" and "after resume" in R2-19 are measured against
  this event (ADOPTED (R4-3)).

### 4.3 States per arrival

The disposition is always one of the six shared values. Everything else is
an **annotation** (never a seventh disposition, R2-18).

| Disposition | Annotations that may accompany it |
|---|---|
| **not reached** (checkpoint-level, before any arrival) | "run ended without arrival" |
| **waiting** | requested (purpose, scope); **lapsed at ‹t›** (before resume, R2-19); **re-held — lapsed at ‹t› after resume** (§4.7); **no items remain** (§4.11); **A12 awaiting control confirmation** / **A12 refused by control: ‹reason›** (§4.10); **act on other content** (SB-2); **prior act on this subject, not counted** (§4.5 SP-6); **act order unknown**; **subject absent** (§4.7); **hold not enforceable** / **action during hold**; **run ended** |
| **performed** | performance ordinal; per-item "accepted by ‹person›" (A5); **accepted — not applied: refused — stale** or **— application error (effect …)** (§4.11); **superseded by ‹act›** (A12); **resumed at ‹t›** |
| **resolved negatively** | A10 per item or act-declined event; **partial** (A5); path taken |
| **lapsed** | Only for an arrival whose run has ended and whose performing act lapsed after the end (R2-19); per referent |
| **unknown** | Which observation was lost; last observed state |

A checkpoint's displayed disposition is that of its **current arrivals**
(§4.13); earlier arrivals remain history.

### 4.4 Events consumed

| Event | Supplier | Effect class |
|---|---|---|
| Arrival (reached-when observed) | App observation / loop (LOOP §2.4.1); host outcome (P §9) | Creates an arrival |
| Human act observed (with capture evidence) | Capturing surface; faithful record citing it (RS §6) | Candidate satisfying act |
| A10 per item; item-left event; all-items-decided | Host via P §4.3 | A5 evaluation |
| Act-declined event | Capturing surface (R2-5) | Negative |
| Act-lapsed event | Host / record reader (RS L-6) | Lapse |
| Act superseded (A12) | Control (R2-7) | Annotation |
| A12 control relation: established ⟨version⟩ / refused ⟨reason⟩ / pending | Control surface (AP §2.1 A12; AS) | A12 evaluation |
| Applied outcome with resulting objects | Host (P §9, R2-14) | Binding for "objects changed by a named outcome" |
| Observation lost / recovered | Executor (App or loop) | Unknown handling |
| Run-resumed | Executor | Resume point |
| Run-ended | Run owner (R2-5) | Finality |
| Declaration invalid / not established | Executor on reading WD | No machine |

### 4.5 Satisfaction predicate (SP)

An observed act record *a* satisfies a waiting arrival *X* with required kind
*K* iff all hold:

| # | Condition | Source |
|---|---|---|
| SP-1 | Kind of *a* is *K* | I-1 |
| SP-2 | Decision actor is the person (for A7: the accountable professional as evidenced); in faithful recording the recorder is distinct and not named as actor | I-1; HA-2 |
| SP-3 | Capture evidence from the capturing surface for this subject, with a resolvable capture-evidence reference (host act facility for host content; App interface for App content, §5; the control surface for A12). An agent-authored record, a conversation statement or an A9 record without that reference never qualifies | I-5; R-5; FB-15 |
| SP-4 | Bound content c₀ equals the current content identity of every bound referent in scope, same method designation (A5: per item, the change-item content identity) | SB-1…SB-3; RS L-1/L-2 |
| SP-5 | Scope of *a* covers the referents (A5 evaluated per item, §4.11) | WD §4.3.1 scope |
| SP-6 | **Captured at or after the arrival event** (ADOPTED (R4-5) with standing PROPOSED; U-E4 open): ordering by a request relation where the capturing surface records one, otherwise by evidenced times. If the order cannot be established, *a* does not satisfy and *X* shows "act order unknown" | V4-REC-05 purpose binding; below |
| SP-7 | For A12: the control relation is **established** (§4.10) | ADOPTED (R4-6) |
| SP-8 | *a* is none of: act-declined event, A8, A3 findings, A14 settlement, success, receipt, host checks passed | I-2; R2-8 |

**Why SP-6.** A checkpoint requests an act *with its declared purpose and
scope* (WD §4.3.1; IR1C-14), and an act binds to its purpose (V4-REC-05). An
act captured before the arrival was not made in answer to that request, so
its purpose is not the checkpoint's. It is shown as "prior act on this
subject, not counted" so the person can repeat it knowingly. SP-6 adds no
ordering *between act kinds* (I-3 stands): it orders the act only against its
own arrival. For A5 at kind (c) *queued* SP-6 always holds, because A5 can
only follow *queued*. The alternative — counting a prior act bound to current
content — is listed in U-E4 for V2.

### 4.6 Transition table (per arrival)

| From | Event / condition | To | Also recorded |
|---|---|---|---|
| (none) | Arrival event observed | **waiting** | "checkpoint reached" with bound subject, purpose, scope; act request issued; run holds |
| (none) | Run ends, reached-when never observed | checkpoint **not reached** | Run-ended event lists it |
| (none) | Deciding observation for arrival lost | **unknown** | Last observed state |
| waiting | Act satisfying SP-1…SP-8 (A4/A6/A7/A12) | **performed** (ordinal n) | Act reference |
| waiting | A5 evaluation gives *performed* (§4.11) | **performed** | Per-item acts |
| waiting | A5 evaluation gives *resolved negatively* | **resolved negatively** | Partial annotation if mixed |
| waiting | Act-declined event on this subject (A4/A6/A7/A12) | **resolved negatively** | Declared path follows (§4.8) |
| waiting | A12 refused / pending / on other content / prior act / order unknown | waiting | Annotation (§4.3) |
| waiting | Observation of acts lost during the wait | waiting (the run holds; §4.12) | "act observation interrupted" |
| waiting | Run ends | waiting (final) | Run-ended event (R2-5) |
| performed | Act-lapsed event **before** resume point | **waiting** "lapsed at ‹t›" | R2-19 |
| performed | Act-lapsed event **after** resume point, run live | **waiting** "re-held — lapsed at ‹t› after resume" | §4.7 |
| performed | Later established A12 on overlapping setting | performed | "superseded by ‹act›" (R2-7) |
| performed | Run ends | performed (final) | — |
| performed (run ended) | Act-lapsed event | **lapsed** (per referent) | R2-19 |
| unknown | Deciding observation recovered | as the observation determines | Recovered event with its own time; no back-fill (§4.12) |
| any | Later act after run end | unchanged | Act recorded and shown against the bound subject (R2-5; §4.9) |
| waiting (no items remain) | New arrival of the same checkpoint | waiting (final for this arrival) | "replaced by arrival n+1" (§4.11) |

Precedence when two events are evidenced for one arrival: the first in
evidenced order decides; later decisions are recorded and shown and do not
change a decided arrival. Evidenced order that cannot be established →
**unknown** for that arrival.

### 4.7 Lapse and re-hold (resolves W7 hold: WD U-22; AP U-10; RS U-24; AS U-13; LOOP C-4; PANEL W-5e) — ADOPTED (R4-3)

Before resume the R2-19 sequence applies unchanged. **After resume**, while
the run is live:

- **RH-1** The act-lapsed event is recorded and presented (always).
- **RH-2** The arrival returns to **waiting**, annotated "re-held — lapsed at
  ‹t› after resume". It is the **same** arrival (same bound referent
  identities), now requiring an act on their *current* content. It is not a
  new arrival.
- **RH-3** The run holds at its **next action boundary** (HD-2). Dispatches
  already in flight complete and are observed; nothing is recalled or undone.
  A kind (a) call already dispatched stays dispatched.
- **RH-4** Actions between the resume point and the lapse observation stay
  recorded as taken under the then-current performance. Outputs whose
  promised standing names this checkpoint as **gating checkpoint** (WD §4.4)
  show that standing lapsed for the affected referents.
- **RH-5** The act request is re-issued with the declared purpose and scope,
  identifying the lapsed referents.
- **RH-6** A satisfying act makes the arrival *performed* with the next
  performance ordinal; a new resume point follows.
- **RH-7** If the run ends while re-held, the final disposition is
  **waiting** with the run-ended event (not *lapsed*: the lapse was observed
  while the run was live).
- **RH-8** A lapse caused by the run's own later action (e.g. a later stage
  editing rows already marked checked) re-holds the same way. A workflow that
  means to change such content should place the checkpoint after the change.
- **RH-9** A5 never re-holds: applying the item does not lapse A5, and a
  basis failure after A5 is the stale rule (R-6). A12 never re-holds:
  supersession is not lapse (R2-7).

**Why re-hold rather than report only.** V4-WF-05 and V4-HI-42 make the run
wait for the person's act; SoW AC-002 keeps it waiting "until evidence shows
that required act actually occurred". Continuing on an act whose bound
content changed would let later work rest on an act that no longer covers
current content (V4-HI-32). RH-3/RH-4 keep history truthful without
rewriting it.

**Partial lapse (carries WD U-05c / AP U-03 / RS U-07, owner DEL-04-01 with
the Owner).** When only some referents lapse, before or after resume:

- the request covers the **whole** bound scope, with the lapsed referents
  marked;
- a new act over the whole current scope satisfies under every option of
  U-03;
- whether an act on the lapsed referents alone satisfies, with the earlier
  act still covering the unchanged referents, depends on U-03. Until it is
  ruled, such an act is recorded and shown, and the arrival stays waiting.
  Case CH-8 is **HELD** on U-03 for that variant only.

**Subject absent (RS L-4).** If a bound referent no longer exists, the
arrival is waiting with "subject absent"; no act can satisfy it. An
act-declined event resolves it negatively, or the run ends. Whether the
declaration should carry an "on subject absent" path is for DEL-02-01 (U-E7).

### 4.8 Negative decisions and paths

- **NG-1** A5: A10 per item (§4.11). A4/A6/A7/A12: act-declined event
  (R2-5). Both give **resolved negatively**; never counted as performed.
- **NG-2** The declared **on negative decision** path governs: *stop* → a
  run-ended event with cause "stopped by declared negative path"; *return to
  a named stage* → the run resumes there, and a later reaching is a new
  arrival (RW-4); *proceed on a branch* → resume point on the branch.
  Absent path → stop.
- **NG-3** A resolved-negatively arrival is final. A positive act captured
  later is recorded and shown and does not change it.
- **NG-4** A run-ended event is never a negative decision; the arrival stays
  waiting (R2-5).

### 4.9 Run end, finality and continuation (resolves W7 hold: WD U-21; AP U-10; RS U-23; AS U-11; LOOP §2.4.1; PANEL W-5b) — ADOPTED (R4-4), standing PROPOSED

- **RE-1 No resumption of an ended run.** A run with a run-ended event is
  closed. Its arrivals' dispositions are final, except the R2-19 change from
  *performed* to *lapsed* on a later lapse. This confirms R2-5's default as
  the rule.
- **RE-2 Post-end acts.** An act performed after run end is recorded
  (DEL-04-03) and shown against the ended arrival's bound subject, marked
  "after run end". It changes no disposition of the ended run.
- **RE-3 Continuation is a new run.** To carry work on, the person starts a
  new run. It may record the relation **continues ⟨run⟩** (new record
  relation, finding F-4). Nothing carries into it: no arrival, no
  disposition, no act. Its checkpoints start *not reached*; its arrivals bind
  their own referents from events observed **in the continuation**. For
  example, "objects changed by a named outcome" binds only outcomes the
  continuation itself observes. By SP-6, acts made before its arrivals
  (including RE-2 post-end acts) are shown as "prior act on this subject, not
  counted".
- **RE-4 Interruption is not run end.** Loss of observation, an App restart
  or a loop restart without a run-ended event leaves the run **interrupted**
  and resumable as the same run (§4.12). If recovery is impossible, the run
  owner records a run-ended event with cause "interruption not recovered";
  dispositions are as reconstructed, and *unknown* stays unknown.
- **RE-5 Starting a run** is not an act in R-1's list and is not reserved; the
  run record names who started it.

**Why no resumption.** An ended run's record is evidence for later
reconstruction (DEL-09-11). Reopening it would let a later act rewrite a
closed disposition, and bind an act made without the run's request to it
(V4-REC-05). A continuation keeps both runs truthful and linked.

### 4.10 A12 refused by the control (resolves W7 hold: WD U-27; AP U-13, §12 item 5; RS U-17; AS U-14; LOOP C-8, FX-C11; PANEL W-5g) — ADOPTED (R4-6); subject rule R4-9

An A12 checkpoint's subject is a grant setting (WD §4.3.6; AP §4.2), and its
purpose is that the person's setting governs the operation the run is about
to request. The act binds to setting content; the control's response is a
relation on the act (R2-7).

**Subject (R4-9, INTEGRATION).** The bound setting content is the one an A8
names at arrival. When no A8 names a setting, it is the setting content the
checkpoint's own declaration names: the classes, grant values and scope it
states. A declaration of an A12 checkpoint that names none is **invalid**
(§4.14; CH-29). An A12 on other setting content satisfies nothing (SB-2);
AR-2's "narrower setting" counts only where it is the content named.

| Control relation on the A12 | Arrival effect | Shown |
|---|---|---|
| **established ⟨settings version⟩** (display *effective*, person-set) | Counts (with SP-1…SP-6) → **performed** | A12 reference and version |
| **pending** (*set by person, not yet confirmed*) | **waiting** | "A12 awaiting control confirmation" |
| **refused ⟨reason⟩** (e.g. "no policy basis", R2-9; W-e) | **waiting**; the refused A12 does not satisfy | "A12 by ‹person› refused by control: ‹reason›" |
| confirmation observation lost (*unconfirmed*) | **unknown** until observed | Last observed state |

- **AR-1** The refused A12 remains a recorded human act (HA-5). It establishes
  nothing (AP U-13) and is never shown as the checkpoint performed.
- **AR-2** The held call (kind (a)) stays undispatched while the arrival
  waits. The person may perform another A12 on the named setting content
  once the control can establish it (R4-9), decline (act-declined →
  *resolved negatively*), or stop the run (run-ended; stays waiting).
- **AR-3** A refused A12 does **not supersede** an earlier established A12:
  the earlier setting stays in force (finding F-5 for DEL-04-01 §2.5 and
  DEL-04-03 L-0).
- **AR-4** Counting a refused A12 would release a held call on the premise of
  a setting that is not in force. The host would still resolve treatment from
  the grant actually in force (R-3), but the record would show the person's
  setting as governing when it did not. Hence *waiting*.

### 4.11 Confirmation of WD §4.3.7 (resolves W7 hold: WD U-20; AP U-09; RS U-18; AS U-09; P §4.3; LOOP C-7; PANEL W-5f)

**CONFIRMED by DEL-02-03 (R4-7)**, all five rows as written,
including the R3-3 accepted-then-stale row. Clarifications and additions:

| # | Item situation | Arrival effect | Status |
|---|---|---|---|
| MX-1 | Per-item states considered: A5 · A10 · undecided · left (item-left event) · **unknown** (decision observation lost) | — | Addition |
| MX-2 | Any bound item undecided | **waiting** (as WD row 2), even if others are unknown | Confirms |
| MX-3 | No item undecided; at least one **unknown** | **unknown** | **Addition** (WD has no row) |
| MX-4 | All remaining items A5, at least one remaining | **performed** over the remaining items; never "all items accepted" when any left (WD rows 1 and 4) | Confirms |
| MX-5 | All remaining items decided, at least one A10 | **resolved negatively**; "partial" annotation if any A5; on-mixed path if declared (WD row 3) | Confirms |
| MX-6 | No items remain (all left) | **waiting** "no items remain". When a new arrival of the same checkpoint occurs (e.g. a re-draft queued), this arrival is closed "replaced by arrival n+1" and keeps final *waiting*. The run holds until then or run end | **Clarification** of WD row 4 |
| MX-7 | An item with A5 later refused at application (stale; R2-16) | Unchanged: the item remains a **decided** member of the subject. Annotated "accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)" | Confirms R3-3 row |
| MX-8 | An item with A5 later meets **application error** (effect none / partial / unknown) or **outcome unknown** at application | Unchanged, annotated "accepted — not applied: application error (effect …)" or "accepted — application outcome unknown (observer …)" | **Addition** |

Consequences for the hold machine (answering P §4.3's "how the hold machine
treats that is DEL-02-03's"):

- **MC-1** MX-7/MX-8 never re-hold the A5 arrival and never trigger its
  negative or mixed path: the person's decision was positive.
- **MC-2** The declared output is not produced for that item (WD §4.6).
  Checkpoints whose reached-when is that item's applied outcome never arrive
  for it; a checkpoint binding "objects changed by a named outcome" binds
  only the objects of items actually applied (WD-EX R-14).
- **MC-3** A re-draft (new proposal identity, P §5) that reaches *queued* is a
  **new arrival** of the A5 checkpoint (RW-4). No acceptance carries over.
- **MC-4** *Performed* at an A5 arrival does not wait for application;
  application is the host's lifecycle (HD-3).

### 4.12 Interruption, recovery and replay (REQ-002 "interrupted or replayed history")

**Principle (PROPOSED (W7)).** Arrival dispositions are a function of the
recorded events: arrivals, act records, A10 and item-left events,
act-declined, act-lapsed and supersession events, control relations,
run-resumed and run-ended events, and observation-lost and recovered events.
The executor's working state is disposable. Everything needed to rebuild it
is in the run record (DEL-04-03 R7–R9, R11) and in host evidence by reference.

| # | Rule |
|---|---|
| RP-1 **Recovery (same run).** | After an interruption the executor (a) rebuilds every arrival's disposition from the record; (b) re-observes before acting: host outcomes of dispatched calls (seek observation before any resubmission, LOOP R-d; a retry keeps the proposal identity, R2-13), acts captured since the last observation, lapse state of performed acts, A12 control relations; (c) records every recovered observation as a new event with its observation time and the source's evidenced time. Nothing is back-filled (P §4.1 rule 3) |
| RP-2 **Arrivals during interruption.** | An arrival whose event occurred while observation was lost is recorded on recovery with the event's own evidenced time. SP-6 compares against that time, so an act captured after the event but before recovery counts |
| RP-3 **Unknown.** | An arrival whose deciding observation stays lost is *unknown*. It may later become waiting, performed or resolved negatively on a recovered observation, recorded as a later event. It is never shown as performed meanwhile (S-K) |
| RP-4 **Held call after recovery.** | A kind (a) call held and performed but not yet dispatched is dispatched **unchanged from the record**. If its dispatch outcome is unknown, observation is sought first; it is never re-dispatched as a new call |
| RP-5 **Declaration source.** | Recovery and replay read the declaration of the **resolved revision recorded for the run**, never the library's current content (WD C-2; FB-08). If those bytes cannot be resolved, recorded dispositions are shown as recorded, marked "declaration not resolvable — reconstruction not verified", and the run stays holding |
| RP-6 **Inspection replay** (read-only, e.g. DEL-09-11) | Rebuilds the same arrival identities and dispositions from the same record. It issues no request, dispatches nothing and records no act. Lapse shown at inspection time is labelled with its evaluation time, separate from the dispositions at run end |
| RP-7 **Re-execution** | Running the workflow again is a new run (RE-3). It inherits no arrival or act |
| RP-8 **Order ambiguity** | Events whose relative order cannot be established from evidence are reported. An arrival decided only by such an order is *unknown* (§4.6 precedence) |

### 4.13 Several checkpoints and several arrivals

- **MA-1** Several checkpoints may have current arrivals at once. The run
  holds while any is waiting (HD-1).
- **MA-2** Arrivals of the same checkpoint coexist unless one is replaced
  (MX-6). The panel shows each current arrival with its ordinal.
- **MA-3** An arrival produced by a run action taken during a hold (possible
  only where the hold is not enforced) is recorded as a separate arrival, with
  the "action during hold" limit on the action that produced it.

### 4.14 Invalid or not-established declarations

A checkpoint that is invalid (FB-03, FB-13, FB-16, R3-2; an A12 checkpoint
whose declaration names no setting content, R4-9) or not established
(FB-04) is reported and never evaluated. The machine creates no arrivals for
it, and it is never shown *not reached* as though valid. The compatibility
report shows it (§3.6), so the person sees before the run that it cannot be
held. The run does not proceed past the prose position as though the
checkpoint were satisfied (WD FB-13).

---

## 5. App-side act capture (resolves W7 hold: WD U-25; HOSTING §6.1 "standing as act evidence") — PROPOSED (W7); CAP-6 ADOPTED (R4-12); CAP-1 amended (R4-13)

The App interface is the capturing surface for acts **in the App** (WD I-5;
AP §4.5). This section states what makes App capture evidence, so that App
runs can reach *performed* truthfully.

| # | Requirement |
|---|---|
| CAP-1 **Scope.** | App capture applies to acts on **App content**: App project files and App-side outputs, bound by file content identity (RS L-1). It also covers A12 where an App control is the control that establishes the setting. Where A13 is captured App-side is set by DEL-04-01 (U-X1; R4-13). An App-side Codex configuration that an agent could write is **never** A13 evidence, and the host's refusal is the authoritative "off". It does **not** apply to acts on host content: those are captured by the host act facility (V4-HI-31), and the App faithfully records them citing the host's capture-evidence reference (U-05b; SQ-01). The App offers no proxy control for host-content acts in this increment (U-E9; SQ-25) |
| CAP-2 **Act control.** | A dedicated App control, operated by the person, for one act kind at a time. It presents: the act kind with the R-4 wording ("mark checked" for A4; "accept" only for A5; "approve" only for A6, engineering approval; "rely" for A7; "set grant" for A12); the bound subject with its content identity; the declared scope and purpose; the actor requirement; and the arrival it answers. The same control offers the **decline** that produces an act-declined event |
| CAP-3 **Direct capture record.** | Operating the control makes a human-act record with recording mode *direct capture* and a **capture-evidence reference** {act identity, actor, act kind, bound content identity with method designation, scope, purpose, time, capturing surface "App interface", arrival reference}. The record meaning is DEL-04-03's (RS §6) |
| CAP-4 **Not operable by automation.** | No agent tool, MCP operation, App rule or supplier request can operate the control or produce its record (D2; R-2). An agent may *request* the act (A8) |
| CAP-5 **Not capture evidence: tool permission.** | An A14 settlement from any origin (the person, the user's Codex mode, an App named-rule decline) is never act evidence (D3; R2-8) |
| CAP-6 **Not capture evidence: user-input and elicitation answers.** | Answers to supplier person-input requests (at 0.158.0 `item/tool/requestUserInput`, `mcpServer/elicitation/request`; HOSTING R9) are **input to the agent**, not act evidence, even when the person gives them. Their wording is authored by the agent or an MCP server, they cannot guarantee the kind/subject/scope/purpose binding of CAP-2, and their content goes to the agent. They are conversation (WD I-5). A question the agent asks this way may be an A8 request, if it names kind, subject and purpose. The App may respond by presenting its own CAP-2 control |
| CAP-7 **Not capture evidence: conversation.** | A chat statement ("I checked it") never satisfies (I-5; FB-15) |
| CAP-8 **Person identity.** | The record names the App's person identity. How the App identifies and verifies the person is `UNRESOLVED` (U-E8). A7's "accountable professional" is recorded as the person's own statement, with an evidence limit |
| CAP-9 **Presenting is not answering.** | Showing a CAP-2 control answers no pending supplier request. The outstanding-request register rules (HOSTING §6) are unaffected |

Construction of the control is DEL-01-04's (later undertaking, D1). App-side
positive capture cases are therefore **AWAITING INPUT** (CH-23).

---

## 6. Transfer and refinement trace (REQ-004, REQ-005; AC-004, AC-005; VER-004, VER-005; WD U-18)

### 6.1 Trace links (original and revised identities)

Each link is a separate fact with its own evidence. A match at one link
establishes nothing about another (WD §6.2; V4-EXM-14).

| Link | Fact | Identity carried | Evidence owner | Absent means |
|---|---|---|---|---|
| **listed** | A library reports the workflow | Tuple + holding library | App library (DEL-02-02); host library (external) | "not listed" |
| **selected** | The person (or brief) chose a full tuple | Tuple + holding library | DEL-02-02 (App); host panel (DEL-05-02, external) | "no selection" |
| **resolved** | The tuple resolved to package bytes whose recomputed content identity **equals the revision** (method-designated) | Tuple + holding library + verification result | Resolver (App: DEL-02-03 for runs and transfer; host: external) | "revision not verified"; never substitute (FB-08) |
| **exported** (transfer) | The resolved package and a **carriage manifest** (§6.3) were prepared for carriage | Source tuple | DEL-02-03 | "not exported" |
| **relayed** (transfer) | The files were carried to the destination (human relay, DEP-001) | Source tuple | The person / relay record | "relay not evidenced" |
| **received** (transfer) | The destination library listed the carried package | Original tuple unchanged (unadapted) + destination holding library | Destination library (host: relay evidence) | "receipt not observed" |
| **adapted** | A new revision was made in the destination | **Revised** tuple (host origin, new revision) + **derived-from** = original tuple | Host (external) | — |
| **opened / drafted / registered** (host→App) | Host workflow opened read-only; refined as a draft; registered after review | Host tuple → draft base → new App tuple with derived-from = host tuple | DEL-02-02 | "draft only — not a workflow identity" |
| **supplied** | These bytes were supplied to the agent or loop, per thread/turn, with source and content identity | Tuple and content identity | App: DEL-01-01 HOSTING §8.2 via DEL-02-04, with the run's **model destination** (R4-1; information only); host: loop run association (SQ-19 (a)) | **unknown** (R2-20; U-29) |
| **provider-adopted** | The model/harness took them up | — | Usually unobservable | **unknown** (supplied ≠ adopted) |
| **observed behavior** | What runs of this identity did | Run records naming the tuple; for App runs also the model destination (R4-1) | DEL-04-03 (App); host run records (external; SQ-19 (b), (c)) | "no run observed" |

Every link records whether it concerns the **original** or the **revised**
identity. A trace never lets a revised identity inherit a link observed for
the original.

### 6.2 Holding library (resolves W7 hold: WD U-24; RS U-22; R2-20 "PROPOSED until W7")

**Confirmed as ruled in R2-20** (PROPOSED (W7) confirmed), with three
precisions:

- **HL-1** The holding library is recorded at *listed*, *selected* and
  *resolved*, shown beside the origin, and carried in the loop's run
  association. It never takes part in identity equality (WD C-6).
- **HL-2** In a transfer, the *received* link records the **destination**
  holding library and the *exported* link the **source** one. A move between
  libraries without a content change creates no new identity.
- **HL-3** It is not recorded at *supplied*. Supply is identified by tuple and
  content identity, and equal revisions mean equal content wherever held. If
  the bytes supplied do not match the resolved revision, that is a revision
  defect ("revision not verified"), not a holding-library fact.

### 6.3 App → host carriage procedure (SOW-054; REQ-004) — PROPOSED (W7)

| Step | Action (semantic) | Owner | Result or failure |
|---|---|---|---|
| TR-1 | The person selects a **registered** App workflow revision to carry. Drafts are not carried: a draft has no workflow identity (DEL-02-02) | Person; DEL-02-02 selection | Source tuple |
| TR-2 | Resolve and verify the package bytes (§6.1 *resolved*) | DEL-02-03 | "revision not verified" stops the transfer |
| TR-3 | Evaluate the compatibility report against the destination catalog if available (CK-4); otherwise record "destination catalog not available" | DEL-02-03 | Report reference |
| TR-4 | Prepare the **carriage manifest**: source tuple; revision content identity and method; declaration contract version; summary of required tool references and checkpoints (name, act kind, reached-when kind, subject class); compatibility report reference; exporter as observed (a Codex-seat exporter is *unverified*, R4-15); time; **transfer identity**. No model-destination restriction is carried or implied (D5, R4-1). The package's own declared part stays the authority (WD R-3); the manifest is a convenience and never overrides it | DEL-02-03 | *exported* |
| TR-5 | The person relays the package and manifest to the host (DEP-001: files human-relayed). No transport is selected | Person | *relayed* |
| TR-6 | The host lists the package, **unadapted**, with the original tuple and its own holding library. Whether the host can read the declared part at that contract version is its receiving capability (SQ-17 (a), (b), (d)) | Host (external) | *received*, or a §6.7 outcome |
| TR-7 | Adaptation, if any, by the host (§6.4) | Host (external) | *adapted* |
| TR-8 | Host evidence (listing, adaptation, runs) returns by relay to the App and to DEL-09-06 (SQ-18, SQ-19; RELAY §4 ledger) | Person; host | Evidence references |

### 6.4 Adaptation receiving (host side, receiving meaning)

- **AD-1** Adaptation creates a new identity: origin *host*, host source root,
  new revision, derived-from = the full original tuple (WD §6.4). The
  original's history is never edited.
- **AD-2 Adaptation difference.** The trace carries a comparison of original
  and adapted declared parts: inputs, required tool references, outputs and
  evidence, and each checkpoint's name, act kind, reached-when, subject class,
  scope, purpose and negative path. Each checkpoint is **preserved**,
  **changed** (listing the changed elements), **removed** or **added**.
- **AD-3** A removed checkpoint, or a changed act kind or subject class, is
  shown as "checkpoint meaning changed". It is not prevented: the host owner
  may adapt. It is never hidden (V4-EXM-14 "checkpoint identity").
- **AD-4 Checkpoint identity across adaptation.** The adapted workflow's
  checkpoints are new checkpoint identities {adapted tuple, name}. Where a
  name is kept, the trace records **derived-from checkpoint** ⟨original
  tuple, name⟩ with the AD-2 classification.
- **AD-5 No act inheritance.** Acts and dispositions from runs of the
  original never carry to runs of the adapted workflow, and the reverse is
  also true (REQ-005: never manufacture past checkpoint acts). Each run's
  replay uses its own resolved revision (RP-5).
- **AD-6** Selections of the original are never rebound to the adaptation
  (C-2). The host library may then show a collision (E4), reported with
  holding libraries.

### 6.5 Host → App opening and refinement (SOW-055; REQ-005) — PROPOSED (W7)

| Step | Action (semantic) | Owner | Identity |
|---|---|---|---|
| HR-1 | Host workflow files are relayed to the App and listed with origin *host*, the host source root, and the App-side holding library where the copy sits | Person; DEL-02-02 listing | Host tuple unchanged |
| HR-2 | Opening is read-only and keeps the host identity (WD §6.4) | DEL-02-02 | Host tuple |
| HR-3 | Refinement is a **draft** whose **draft base** is the host tuple. A draft is not a workflow identity and cannot be selected for a run | DEL-02-02 | — |
| HR-4 | The person reviews and registers it (V4-WF-02). Registration never overwrites silently | Person; DEL-02-02 | New tuple: origin *project* or *user*, new revision, derived-from = host tuple |
| HR-5 | Return to the host is an App→host carriage (§6.3) of the new tuple. Adaptation there creates another derived-from link | As §6.3 | Chain by following derived-from links |
| HR-6 | **History.** Host run records of the host identity (relayed) are referenced from the App trace under the **host** identity. They are displayed as history and never become acts or dispositions of App runs (AD-5). Interruption/revision/replay history is preserved by reference, not copied (V4-HI-71) | DEL-02-03 trace; DEL-04-03 | — |
| HR-7 | Same-name collisions in the App library expose every origin with its holding library and never rebind (C-1, C-2) | DEL-02-02 | — |

The changed-draft return path belongs to DEL-02-02 and is not compared in this
undertaking (D1); see finding F-12.

### 6.6 Derived-from chain

`derived-from` names only the immediate parent's full tuple (WD §6.1). The
lineage is reconstructed by following the links; a broken link (parent not
resolvable) is shown as "lineage incomplete at ‹tuple›", never guessed.

### 6.7 Transfer outcomes and failure behavior

| ID | Condition | Outcome |
|---|---|---|
| TF-1 | Relayed bytes do not recompute to the claimed revision | **revision not verified**; not listed as that revision |
| TF-2 | Relay incomplete or interrupted | **not received (incomplete)**; no partial listing or registration; a new attempt keeps the same source tuple and a new transfer identity |
| TF-3 | Host cannot receive workflows from outside its library, or cannot list another origin | **receiving capability unavailable** (explicit; REQ-004) |
| TF-4 | Host cannot read the declaration contract version | **declared part not established** at the destination; the host's required-tool check and checkpoint holds are not established (WD §3.4) |
| TF-5 | Destination catalog lacks required tools | Reported by the CK-4 report; carriage still possible |
| TF-6 | Host adaptation evidence not relayed | *adapted* link **not observed** |
| TF-7 | Host listing drops the original origin (lists it as host origin without derived-from) | **origin not preserved** — a trace defect (R-9), reported |
| TF-8 | App-side App reads a host workflow whose declared part is at a newer contract version | Listed; declared part **not established**; opening allowed |

---

## 7. Fixture cases on FX-PIPE-01 (OUT-003 design; none run)

All material is invented fixture subject matter from C §10 (FX-PIPE-01: FX-W1,
g1, R-100, S-1…S-5, LC-1, Engineer A, OP-C1…OP-C12, T1…T17, Tg, B1/B2,
PR-1/PR-2, RC-1…RC-3, FA-1…FA-5, V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1) and
WD-EX (E1, E1b, E1c, E1d, E3–E7; E2 runs R-1…R-17, R-E1b, R-E1b′;
L-WDEX-n). Exposure is FA-1 (fixture assumption). C at `f05c7e4cd` does not yet carry the App-file subject and App-side library that R4-20 adds, so L-EXEC-19, ⟨fx-app-import⟩ and ⟨rev-A3⟩ remain local labels with their reasons and will be re-pointed to C's identifiers. Case states: **DESIGNED**,
**AWAITING INPUT** (named input), **HELD** (named decision).

### 7.1 Missing-tool (VER-001)

| Case | Input | Expected report | State |
|---|---|---|---|
| MT-1 | E1 ⟨rev-3⟩ on surface E against FX-W1's edition (WD-EX E7 base) | OP-C1, OP-C3, OP-C4, OP-C5 **present**; passes; PS-2 wording; limitation "FA-1 exposure assumed" | DESIGNED |
| MT-2 | E1 ⟨rev-A2⟩ carried unadapted, App run on X (L-EXEC-1: App-side acting surface, which C §10 does not describe) | As MT-1 on X; CR-14 shows the model destination (information only). Hold support: `CP-accept` and `CP-check` **not enforceable** in the App run pending `UNRESOLVED{D6}`, so the check does not pass (unsupported). The person may still start the run (CC-3) | DESIGNED; would change only when SQ-02 is answered (U-E1) |
| MT-3 | **Registered but missing**: ⟨rev-A2⟩ registered in ⟨fx-proj⟩; OP-C4 absent from the edition (L-WDEX-10) | Registration unchanged; OP-C4 **missing** with purpose line; does not pass; "registered ≠ compatible" (PS-3) | DESIGNED |
| MT-4 | OP-C5 absent (L-WDEX-11) | OP-C5 **missing**, optional; passes; fallback shown | DESIGNED |
| MT-5 | E1c `supports-label` on X with V-X1 (OP-C9 not exposed on X) | OP-C9 **not exposed on this surface** on X; passes on E | DESIGNED |
| MT-6 | Workflow requiring OP-C2 at r13 (WD-EX E7 T8 analogue) | **present, currently unavailable**, reason "No current solve for LC-1 at this revision", basis B2; passes as a run-time hold | DESIGNED |
| MT-7 | L-EXEC-2: E1 declares OP-C1 v1; the edition carries OP-C1 **v2** (C §10.5 hypothetical); no compatibility statement. Needed because C has no version-mismatch entry | **version mismatch**; does not pass; limitation "equality only (U-C9)" | DESIGNED |
| MT-8 | L-EXEC-3: E1 variant adding a required harness capability "file writing". Needed because C covers host operations only | That reference **not established** (U-08); does not pass | DESIGNED |
| MT-9 | E5 `create-workflow` (undeclared) | **not established**; selectable; never "runnable" (PS-4) | DESIGNED |
| MT-10 | E6 `project-dag` in a host seat without delegation | Required tools not established; workflow **unsupported** (delegation) | DESIGNED |
| MT-11 | L-EXEC-4: MT-1 passed on edition E; at run time the loop's offered edition lacks OP-C5. Needed to separate report time from run time | Report unchanged; run records the loop-side **not offered** failure (CC-2) | DESIGNED |
| MT-12 | L-EXEC-5: the host publishes a new edition after MT-1. Needed for CK-3 | MT-1 report marked *not current*; new report produced | DESIGNED |
| MT-13 | Workflow requiring OP-C11 (L-WDEX-14) | **present**; passes; dependent production **held** (CC-4) | HELD (R2-9; `UNRESOLVED{OI-021}`) |
| MT-14 | L-WDEX-13: external access off | Surface-level **channel not enabled** on X; never missing | DESIGNED |
| MT-15 | L-EXEC-6: E1d on X in an App run whose Codex mode auto-settles native tools, with CP-grant kind (a) declared on a harness capability instead of OP-C9. Needed to show §3.6 *not enforceable* | CP-grant hold **not enforceable** (R4-21); workflow **unsupported** (reason); does not pass | DESIGNED |

### 7.2 Checkpoint hold (VER-002, VER-003)

| Case | Input | Expected | State |
|---|---|---|---|
| CH-1 **Direct autonomy, no act** | E1c; T15 (⟨set-2⟩ direct for S-4) → T16 RC-2 | Direct application proceeds; `CP-check` arrival (kind (c), applied RC-2) **waiting** on S-4 (post-application identity); run holds; nothing releases it without A4 | DESIGNED |
| CH-2 **Unrelated success** | E2 R-1 (PR-2 queued, T10); L-EXEC-7: while `CP-accept` waits, OP-C12 host check and another run's RC-2 are observed. Needed because C has no concurrent-run step | `CP-accept` stays **waiting**; no success, receipt or host check changes it (I-2) | DESIGNED |
| CH-3 **Interruption while waiting** | L-EXEC-8: loop observation lost after T10; T11 A5 (item 1) and A10 (item 2) captured by the host during the loss; recovery. Needed because C has no loss at T10–T11 | On recovery (RP-1): arrival waiting, then T11 events recorded at recovery with their host times → **resolved negatively**, partial; no back-fill | DESIGNED |
| CH-4 **Lost deciding observation** | E2 R-6 (L-WDEX-3), then L-EXEC-9: *queued* observed later. Needed to show unknown → waiting | **unknown**, then a later recovered event → **waiting**; the earlier *unknown* stays in history | DESIGNED |
| CH-5 **Inspection replay** | Record of E2 R-2 replayed read-only after E4 step 3 (⟨rev-4⟩ registered) | Same arrival identities and dispositions; declaration read from ⟨rev-3⟩ (RP-5); no request or dispatch | DESIGNED |
| CH-6 **Lapse before resume** | E2 R-4 (i) | Act-lapsed event; **waiting — lapsed at ‹t›** | DESIGNED |
| CH-7 **Lapse after resume → re-hold** | L-EXEC-10: after E2 R-3, `CP-check` performed by A4 on the new support S-5 and S-3; run resumes at the "Return" step (run-resumed event); Engineer A edits S-5 before the run ends. Needed because WD-EX R-4 covers only before-resume and after-end | Act-lapsed event; **waiting "re-held — lapsed at ‹t› after resume"**; run holds at next boundary; `checked-rows` standing shown lapsed for S-5; new A4 on the whole current scope → **performed** (ordinal 2) | DESIGNED |
| CH-8 **Partial lapse** | CH-7 with only S-3 edited | Request covers S-5 and S-3, S-3 marked. (i) A4 over both → **performed**. (ii) A4 on S-3 only → recorded and shown; arrival stays waiting | (i) DESIGNED; (ii) **HELD** on U-03 |
| CH-9 **Run ended while waiting; post-end act; continuation** | E2 R-12b for E1. Then L-EXEC-11: an E1b run stopped after `CP-review` arrives at T4; Engineer A then marks S-2 and S-3 checked; a continuation run *continues ⟨run⟩* re-reads (OP-C1) and re-examines (OP-C3), producing `findings`. Needed because a continuation of E1 applies nothing, so `CP-check` would bind no objects (RE-3) | R-12b: `CP-check` final **waiting** with run-ended; post-end A4 shown "after run end". L-EXEC-11: ended `CP-review` final **waiting**; the continuation's own `CP-review` arrival binds S-2 and S-3 as read; the post-end A4s predate it → "prior act, not counted" (SP-6); new A4s → **performed** | DESIGNED |
| CH-10 **Lapse after run end** | E2 R-4 (ii); E2 R-17 (T16a, T17) | **lapsed** per referent (S-3; S-4 under FA-2) | DESIGNED |
| CH-11 **Refused A12** | L-EXEC-12: workflow `renumber-with-grant` (fixture) declaring `CP-grant` A12, kind (a) before dispatch of OP-C11, subject grant setting; Engineer A performs A12 widening OP-C11's class to direct (V-NP1). Needed because E1d's OP-C9 class can be established | Control **refused (no policy basis)**; `CP-grant` **waiting** "A12 refused by control"; held call not dispatched; then (a) act-declined → **resolved negatively**, or (b) run stopped → final waiting | DESIGNED; production HELD (R2-9) |
| CH-12 **A12 pending, then established** | E1d with T15, with the control confirmation observed after a delay (L-EXEC-13: timing variant of T15) | **waiting** "awaiting control confirmation", then **performed**; held OP-C9 call dispatched unchanged | DESIGNED |
| CH-13 **Refused A12 does not supersede** | L-EXEC-14: after CH-12, Engineer A performs a later A12 for OP-C11's class that is refused | CH-12's A12 stays in force and not superseded; `CP-grant` stays **performed** | DESIGNED (finding F-5) |
| CH-14 **A12 supersession** | E2 R-16 (E1d; L-WDEX-9 order: arrival before the A12) | **performed**, then "superseded by ‹later A12›"; not lapsed; no re-hold | DESIGNED |
| CH-15 **Mixed items** | LOOP FX-C5 / E2 R-2 (T11) | MX-5: **resolved negatively**, partial (item 1 A5); on-mixed path: continue with item 1 | DESIGNED |
| CH-16 **Item left** | LOOP FX-C12 | MX-4: **performed** over item 1; item 2 shown with item-left event; never "all accepted" | DESIGNED |
| CH-17 **All items left, re-draft** | L-EXEC-15: after T10, Engineer A edits S-3 before any decision; the host refuses both PR-2 items stale (item-left); the agent re-drafts a new proposal (local label L-EXEC-15-P, lineage PR-2), queued. Needed because C's T7 staleness occurs before *queued* | Arrival 1 **waiting** "no items remain", closed "replaced by arrival 2"; arrival 2 waiting on L-EXEC-15-P items; no acceptance carried | DESIGNED |
| CH-18 **Accepted then stale** | V-S1 and E2 R-14 (L-WDEX-7) | MX-7: disposition unchanged (V-S1: resolved negatively, partial; R-14: performed); annotation with both bases; `CP-check` binds only objects of applied items | DESIGNED |
| CH-19 **Unknown item decision** | L-EXEC-16: at T11 item 1's A5 is observed; item 2's decision observation is lost. Needed for MX-3 | **unknown**; never performed or resolved negatively until item 2 is observed | DESIGNED |
| CH-20 **Prior act not counted** | E1b along T2–T4: T2's A4 on S-2 precedes `CP-review`'s arrival at T4 | S-2's T2 A4 shown "prior act, not counted"; waiting until A4 on S-2 and S-3 after T4 (then E2 R-E1b → performed) | DESIGNED (SP-6 PROPOSED) |
| CH-21 **Held call across recovery** | LOOP FX-C8 variant L-EXEC-17: A4 performed on S-3 at B2; interruption before dispatch | Recovery dispatches the same held OP-C5 call unchanged from the record; if its outcome is unknown, observation is sought and there is no new call (RP-4) | DESIGNED |
| CH-22 **App-side hold, not enforced** | L-EXEC-18: App run of E1 ⟨rev-A2⟩ on X; `CP-check` kind (b); in the same turn that produces `examination-report`, Codex also writes a file and calls OP-C1. Needed because C describes no App-run turn | Arrival **waiting**, hold support *not enforceable* (R4-2). HP-4: the App starts nothing further. No interruption is relied on (HP-2 not adopted). The file write and the OP-C1 call are recorded as **action during hold**. HP-3 declines any permission request that reaches the App, with origin recorded in R13. No hold is claimed | DESIGNED |
| CH-23 **App-side capture** | L-EXEC-19: App-side workflow with an A4 checkpoint on an App report file (App content; C has no App-file subject). (i) The agent asks through a user-input request and the person answers "yes". (ii) The person marks it checked in the App act control (CAP-2) | (i) Conversation; **waiting** (CAP-6). (ii) Direct capture with a capture-evidence reference → **performed** | (i) DESIGNED; (ii) AWAITING INPUT (DEL-01-04 control; U-E8) |
| CH-24 **Subject absent** | L-EXEC-20: after CH-7's performance, S-5 is deleted before resume | Act lapsed (subject absent); **waiting "subject absent"**; only an act-declined event or run end closes it | DESIGNED (U-E7) |
| CH-25 **Tool permission during hold** | E2 R-15 during a hold, plus HP-3 | A14 changes no disposition; an App named-rule decline, if used, is recorded with truthful origin in R13 only | DESIGNED |
| CH-26 **Invalid declarations** | LOOP FX-C13; WD VC-29 variants | Reported; no arrival; check shows hold support **not established** | DESIGNED |
| CH-27 **Constraint forced proposal** | V-CP1 / LOOP FX-C9 / WD VC-11; over X also ADAPTER XF-25/XF-26 | As those cases. Over X, with model-supplied carriage only, hold support is *not established* (R4-14; GC-3); if the call is dispatched anyway, "omitted governing checkpoint constraint" is recorded (R11) | AWAITING INPUT (SQ-02; U-E13) |
| CH-29 **A12 checkpoint naming no setting** | L-EXEC-25: E1d variant whose `CP-grant` declaration states no classes, grant value or scope, and no A8 names a setting. Needed for R4-9 | Checkpoint **invalid** (R4-9); never evaluated; hold support *not established*; check does not pass | DESIGNED |
| CH-28 **Host capture reference absent** | E2 R-9 (iii) | **waiting** (I-5) | DESIGNED; host side AWAITING INPUT (SQ-01; U-05b) |

### 7.3 Round trip (VER-004, VER-005)

| Case | Input | Expected trace | State |
|---|---|---|---|
| RT-1 **App→host unadapted** | E3 "carried unadapted": ⟨rev-A2⟩ exported with manifest, relayed, listed in ⟨fx-root⟩ | Links selected → resolved (verified) → exported → relayed → received; origin *project* kept; holding library ⟨fx-proj⟩ at export and ⟨fx-root⟩ at receipt; no "App-origin" | DESIGNED (test double); host side AWAITING INPUT (SQ-17) |
| RT-2 **Adaptation preserving checkpoints** | E3 adapted ⟨rev-3⟩ | New host tuple, derived-from ⟨rev-A2⟩ tuple; AD-2: `spacing-limit` necessity changed; `CP-accept` and `CP-check` **preserved**, each with derived-from checkpoint | DESIGNED; host side AWAITING INPUT (SQ-18 (b), (c)) |
| RT-3 **Adaptation changing a checkpoint** | L-EXEC-21: host variant ⟨rev-3x⟩ that removes `CP-check` and changes `CP-accept`'s on-negative path. Needed because E3 preserves all checkpoints | AD-2: `CP-check` **removed**, `CP-accept` **changed** (on negative decision); "checkpoint meaning changed" shown; not blocked | DESIGNED |
| RT-4 **Unsupported receiving capability** | L-EXEC-22: host library that cannot list a *project*-origin workflow (TF-3), and a variant that cannot read contract version WD-v0.3 (TF-4). Needed because C describes no receiving capability | TF-3: **receiving capability unavailable**. TF-4: listed; declared part **not established**; required-tool check and holds **not established** | DESIGNED; host side AWAITING INPUT (SQ-17 (a), (b)) |
| RT-5 **Supplied / adopted / observed** | Run 12 on ⟨rev-3⟩ (C §10.1) in the host; an App run of ⟨rev-A2⟩ | Host: *supplied* **unknown** without a per-turn record; adopted **unknown**; observed from the run record. App: *supplied* from HOSTING §8.2 evidence, with the model destination recorded (R4-1), e.g. a cloud model, without any gate; adopted **unknown** | DESIGNED; host AWAITING INPUT (SQ-19 (a), (b); U-29) |
| RT-6 **Host→App refinement** | E3 last column: ⟨rev-3⟩ relayed to the App (holding library ⟨fx-app-import⟩, a local label because C has no App-side library); opened; draft with base ⟨rev-3⟩; registered as ⟨rev-A3⟩ (local label) | Opening keeps host tuple; draft is not selectable; registration gives origin *project*, derived-from ⟨rev-3⟩ tuple; lineage ⟨rev-A3⟩ → ⟨rev-3⟩ → ⟨rev-A2⟩ | DESIGNED; registration is DEL-02-02's (later) |
| RT-7 **Collision without rebinding** | E4 steps 1–4; plus ⟨rev-A3⟩ registration while ⟨rev-A2⟩ holds the name in ⟨fx-proj⟩ | All origins with holding libraries; no rebinding; no silent overwrite (slot policy DEL-02-02, U-10) | DESIGNED |
| RT-8 **History preserved, no act inheritance** | RT-6 with run 12's history (T10–T13 `CP-accept` arrivals) | App trace references run 12 under the host tuple; a run of ⟨rev-A3⟩ starts with every checkpoint **not reached**; no act imported | DESIGNED |
| RT-9 **Revision mismatch** | L-EXEC-23: relayed files whose recomputed content identity ≠ ⟨rev-3⟩ | **revision not verified**; not listed as ⟨rev-3⟩ (TF-1) | DESIGNED |
| RT-10 **Interrupted relay** | L-EXEC-24: package partially relayed | **not received (incomplete)**; no registration; retry with a new transfer identity (TF-2) | DESIGNED |
| RT-11 **Evidence account for DEL-09-06** | All MT/CH/RT cases, joined by CA-v0.1 W14 cases: W14-01 ← RT-1; W14-02 ← RT-2, RT-3; W14-03 ← MT-1, MT-3, MT-10, MT-15; W14-04 ← CH-1, CH-27; W14-05 ← CH-2, CH-23, CH-28; W14-06 ← CH-6…CH-10; W14-07 ← CH-3…CH-5, CH-21; W14-08 ← RT-5; W14-09 ← RT-6, RT-8; W14-10 ← RT-7 | Inventory with candidate and source versions, case states, labels (C mapping), limitations and missing external inputs (SQ IDs as cited per case); names DEL-09-06 as joined-witness owner; claims no witness | DESIGNED |

---

## 8. Resolution register for items held for W7

| Held item (sources) | Resolution | Section | Standing at v0.2 |
|---|---|---|---|
| Re-hold after a lapse following resume (WD U-22; AP U-10; RS U-24; AS U-13; LOOP C-4, FX-C3; PANEL W-5e, PC-20) | Same arrival re-held: waiting "re-held — lapsed at ‹t› after resume"; hold at next action boundary; history kept; whole-scope request; ended while re-held → waiting | §4.2 HD-5, §4.7 | **ADOPTED (R4-3)**; partial-lapse satisfaction **carried** on U-03 (C1) |
| Resumption of an ended run; post-end acts (WD U-21; AP U-10, §2.3; RS U-23; AS U-11; LOOP §2.4.1, FX-C7b; PANEL W-5b, PC-21d; WD-EX R-12b) | No resumption; ended dispositions final (except R2-19 lapse); post-end acts shown "after run end"; continuation is a new run *continues ⟨run⟩* with nothing inherited; interruption ≠ run end | §4.9 | **ADOPTED (R4-4)**, standing PROPOSED |
| Refused A12 at a checkpoint (WD U-27, SB-4; AP U-13, §12.5; RS U-17; AS U-14; LOOP C-8, FX-C11; PANEL W-5g) | Refused → does not count, stays waiting with refusal shown; pending → waiting; unconfirmed → unknown; refused A12 does not supersede; subject per R4-9 | §4.10 | **ADOPTED (R4-6; R4-9)** |
| Confirmation of WD §4.3.7, mixed items and accepted-then-stale (WD U-20; R2-18; R3-3; AP U-09; RS U-18; AS U-09; P §4.3; LOOP C-7; PANEL W-5f) | **Confirmed**, with MX-3 (unknown item), MX-6 (replaced empty arrival), MX-8 (application error / unknown after A5) and MC-1…MC-4 | §4.11 | **CONFIRMED; additions ADOPTED (R4-7)** |
| Holding library (WD U-24; RS U-22; R2-20 "PROPOSED until W7"; LOOP §2.1; PANEL §3.2) | **Confirmed** as R2-20, plus HL-2 (source/destination at transfer) and HL-3 (not at *supplied*) | §6.2 | Confirmed; carried into RS by R4-11 (transfer links) |
| App-side capture (WD U-25; HOSTING §6.1, R9 "standing as act evidence") | CAP-1…CAP-9; user-input and elicitation answers are **not** act evidence; A13 locus per DEL-04-01; App control construction and person identity carried | §5 | CAP-6 **ADOPTED (R4-12)**; CAP-1 per **R4-13**; rest PROPOSED (W7); construction **carried** (DEL-01-04, later; U-E8) |
| Transfer/adaptation procedure (WD U-18) | TR-1…TR-8, AD-1…AD-6, HR-1…HR-7, TF-1…TF-8; model destination recorded, never gated (R4-1) | §6 | PROPOSED (W7); host links AWAITING INPUT (SQ-17…SQ-19) |
| Hold machine (WD §4.3.4 "DEL-02-03's (W7)"; §9 A-4; LOOP §10.1) | §4 | §4 | Disposition logic PROPOSED (W7), with R4-3…R4-7 adopted. App-side enforcement `UNRESOLVED{D6}` (R4-2; SQ-02). Host placement `UNRESOLVED{OI-013}` (SQ-20), sharing `UNRESOLVED{OI-014}` |
| ADAPTER U-X3: GC-3 constraint assurance, GC-5 kind (a) on X (held for DEL-02-03) | GC-3 and GC-5 adopted into hold support: only host-held carriage or a host hold counts; otherwise *not established* | §3.6 | **Resolved** under R4-14, R4-2 and R4-21; host side AWAITING INPUT (SQ-02) |
| Multi-row A4 purpose after partial lapse, point of need "before DEL-02-03 re-hold design" (WD U-05c; AP U-03; RS U-07; CA DI-7) | Not decided here (owner DEL-04-01 with the Owner). Carried: whole-scope request satisfies under every option; narrower-act variant HELD | §4.7 | **Carried** to C1 (R4) |
| Version ordering, point of need "before DEL-02-03 required-tool fixtures" (WD U-07; C U-C9) | Equality only; MT-7 expects *version mismatch* | §3.4 EV-6 | **Carried** (SQ-18 (d)) |
| Harness capability names, point of need "before App-side required-tool check" (WD U-08) | *not established* until named; kind (a) on them not holdable (R4-21) | §3.4 EV-3; §3.6 | **Carried** |
| Constraint receipt, point of need "before W7 host-side fixtures" (WD U-19; P U-P10) | CH-27 AWAITING INPUT | §7.2 | **Carried** (SQ-02) |

---

## 9. Interfaces

### 9.1 Expected from suppliers

| Supplier | Element | State | Used in |
|---|---|---|---|
| DEL-02-01 (WD) | Declared-part status; required tool reference elements; §4.2.4 vocabulary and pass rule (with the R4-8 reason); checkpoint elements, validity rules (with R4-9, R4-21), I-1…I-7, dispositions, §4.3.7 (with R4-7); identity tuple, chain, holding library, §6.4 | v0.3 read at `ba0b37123`; v0.4 under R4 concurrent (not read) | §3, §4, §6 |
| DEL-03-01 (C) | Catalog edition; entry identity/version (equality); exposure element 9; availability and reason; §4.1 results (App reporter of *channel not enabled*, R4-16); subject content identity; FX-PIPE-01; R4-20 App-file subject and App library | v0.3 read; R4-20 additions pending | §3, §4.5, §7 |
| DEL-03-02 (P) | Per-item dispositions; item-left events; all-items-decided; change-item content identity; applied outcome with resulting objects; stale and application-error outcomes; retry precedence; governing checkpoint constraint with **carriage assurance** (R4-14); author identity possibly *unverified* (R4-15) | v0.3 read; R4 amendments cited | §3.6, §4.4, §4.11, §4.12 |
| DEL-04-01 (ACT) | A1–A14; closed list; act-declined event; A12 binding and supersession (R4-6); grant-setting subject (R4-9); A13 capture locus (U-X1; R4-13); U-03 ruling (pending) | v0.3 read; R4 cited | §4.5, §4.7, §4.10, §5 |
| DEL-04-02 (AS) | Grant display states incl. *set by person, not yet confirmed*, *unconfirmed*, *refused (reason)* | Read | §4.10 |
| DEL-04-03 (RS) | Human-act record, recording mode, capture-evidence reference; events; lapse rules; R8 with the R4-10/R4-11 additions (ordinals, run-resumed, re-held/replaced, A12 control effect, prior act not counted, continues ⟨run⟩, action during hold, transfer links, revision verification, report reference, model destination) | v0.3 read; v0.4 under R4 | §4, §5, §6 |
| DEL-05-01 (LOOP) | Arrival observation (§2.4.1), binding (§2.4.2), events (§2.3), retry rules (§6.3) | Read | §4 |
| DEL-01-01 (HOSTING) | Supplied-guidance evidence (§8.2); request kinds and R9 (R4-12) | Read | §5, §6.1 |
| DEL-03-03 (ADAPTER-v0.1) | Carriage assurance (§5.1–§5.2); GC-1…GC-5; §7.7 checkpoint observation on X; model destination in channel status (R4-1) | Read at `e20a3ae8d` | §3.6, CH-22, CH-27 |
| DEL-01-04 (later, D1) | App act control (CAP-2) and person identity | Not in this undertaking | §5 |
| DEL-02-02 (later, D1) | Listing, selection, draft, review, registration, slot policy | Not in this undertaking | §6.5 |
| Host owner (DEP-001), via DEL-09-06 RELAY-v0.1 | SQ-01 capture-evidence reference; SQ-02 constraint receipt and host holds (decides D6); SQ-11 exposure; SQ-17 receiving App workflows; SQ-18 adaptation, library identity, version statements; SQ-19 run records and supplied guidance; SQ-20 host placement; SQ-25 proxy control | Prepared for relay, not delivered (RELAY §4 ledger) | §2, §3.6, §4, §6 |

### 9.2 Provided to receivers

| Receiver | Provided | Expected check at next comparison |
|---|---|---|
| DEL-02-01 | Resolutions of U-18, U-20, U-21, U-22, U-24, U-25, U-27 (now adopted under R4-3…R4-9); SP-6 (R4-5, PROPOSED); §3.6 hold-support values under D6; AD-2 checkpoint comparison | WD v0.4 carries R4-3…R4-9 and R4-21 consistently with §3.6 and §4 |
| DEL-05-01 | Hold-machine semantics (§4) for host loops | LOOP C-4, C-7, C-8, §2.4.1, FX-C3/C7b/C11, FX-C4 re-pointed per R4-3…R4-6 |
| DEL-04-03 | Record needs, adopted by R4-10/R4-11 | RS v0.4 elements match §4 and §6 |
| DEL-03-03 | Answer to U-X3 (§3.6, §8); hold-support values for X; CH-22/CH-27 expectations | ADAPTER v0.2 closes U-X3 against §3.6 |
| DEL-09-06 | Transfer trace (§6.1), carriage manifest meaning (§6.3), RT/MT/CH fixture design and the RT-11 W14 map; SQ citations per host item | CA W14 rows and RELAY §3 map stay consistent with the SQ references here |
| DEL-05-02, DEL-04-02 | Display meanings of the §4.3 annotations, §3.3 report and hold-support values | PANEL W-5b/e/f/g and AS §4 re-pointed |

---

## 10. Excluded acts and owners (REQ-006; AC-006)

| Excluded act | Owner | Interface here |
|---|---|---|
| Declaration and shared-allocation design | DEL-02-01 | §3.2, §4 consume |
| Review, registration, selection policy, drafts | DEL-02-02 (later, D1) | §6.5 routes |
| Catalog semantics | DEL-03-01 | §3.2 |
| Proposal and outcome semantics | DEL-03-02 | §4.11 |
| Operation-policy definition; adopted D2/D3 carriage; U-03 | DEL-04-01; the Owner for U-03 | §4.5, §4.7 |
| Record format, writer and reader | DEL-04-03 | §4, §5 needs |
| Host-loop receiving design | DEL-05-01 | §9.2 |
| External adapter construction; carriage realization | DEL-03-03 | §3.6 (carriage assurance, R4-14) |
| App act control construction | DEL-01-04 (later, D1) | §5 |
| Joined round-trip witness and external contribution record | DEL-09-06 | RT-11 |
| Host catalog, library, loop, panel, act facility, receipts, run records | External SWBPIPE owner (DEP-001) | §6.3 TR-6…TR-8 |
| Every human act (A4–A7, A10, A12, A13), professional reliance, review and registration decisions, relay of files | The person; the accountable professional | Never performed or inferred here |
| OI-013, OI-014, OI-021, OI-003 decisions | Their owners | UNRESOLVED |

Nothing here promotes a carrier into a decision actor, or implies an external
commitment (VER-006).

---

## 11. Findings

### 11.1 v0.1 findings and their R4 disposition

| # | Where | Finding (v0.1, condensed) | Disposition |
|---|---|---|---|
| F-1 | WD §4.3.7, U-20 | Missing rows: unknown item decision, empty-subject closure, application error or unknown after A5 | Closed: R4-7 |
| F-2 | WD I-4; AP §4.3; RS L-12; AS §4; LOOP C-4; PANEL W-5e | After-resume branch deferred; interim display conflicted | Closed: R4-3 |
| F-3 | WD I-1; AP §4.2/§4.5; LOOP C-2, FX-C4; WD-EX R-16 | No rule relating capture time to arrival | R4-5 adopts SP-6 as PROPOSED; U-E4 open; FX-C4 and R-16 repaired by their owners |
| F-4 | WD U-21; AP §2.3; RS; LOOP; PANEL | Resumption deferral; continuation link missing | Closed: R4-4 |
| F-5 | AP §2.5; RS L-0; LOOP; PANEL W-5g | A refused later A12 would supersede | Closed: R4-6 |
| F-6 | RS R8; AS §4 | R3-1 class missing | Closed: R4-10 |
| F-7 | RS §3, R8, R11 | Record elements missing | Closed: R4-11 |
| F-8 | WD §4.2.4 | No *unsupported* reason for a checkpoint hold | Closed: R4-8 |
| F-9 | HOSTING §6.1, R9 | Elicitation standing undefined | Closed: R4-12 |
| F-10 | SoW REQ-002 vs CLM-003 | No App hold point allocated | **Carried to C1** as a SoW gap; home `UNRESOLVED{D6}` (R4-2) |
| F-11 | SoW TBD-001/002; DEP-02-03-015/016 | OI-001/002 still called open | **Carried to C1** |
| F-12 | CASE-002 M1 DEL-02-02 row | Changed-draft return uncompared | **Carried to C1** (out-of-scope receiver, D1) |
| F-13 | AP §4.2 | Grant-setting referent undefined without A8 | Closed: R4-9 |
| F-14 | WD U-05c / AP U-03 | Point of need reached without ruling | **Carried to C1** as an open owner question (R4); U-E3 |
| F-15 | C §10 | No App-file subject or App library | R4-20 adds them to C; not yet present at `f05c7e4cd`; local labels kept |
| F-16 | WD §4.3.1 kind (a) on harness capability | Not holdable in App runs | Closed: R4-21 |

### 11.2 New findings at v0.2

| # | Where | Finding | Proposed change |
|---|---|---|---|
| F-17 | R4-2 with R4-8; this file §3.6; CA-v0.1 W14-03/W14-04 | With D6 deferred and HP-1/HP-2 not adopted, **every** checkpoint in an App run that HP-H does not cover is *not enforceable*. R4-8 then makes every checkpointed workflow *unsupported* on the App surface, and its check does not pass. Examples: E1 on X (MT-2); App-side runs with kind (b) or (c) checkpoints. This is truthful but strong. It should be visible to the owner as a consequence of D6 before SQ-02 is answered | Present to the owner with D6. The alternative is a "not enforceable — run at the person's discretion" value that passes with a stated limitation. That would need an owner ruling, since it weakens R4-8 |
| F-18 | R4-14 vs HP-1 | R4-14 lists *App-assured* carriage as a valid assurance, but App-assured needs interposed App code (ADAPTER §5.2 I-DT/I-PX), which R4-2 does not adopt. For the first increment, only *host-held* carriage can satisfy R2-12 | State in P §3.3 / ACT §4.4 v0.4 that App-assured is unavailable while HP-1 is not adopted |
| F-19 | CA-v0.1 W14-04 (i) | V-CP1 over X presupposes a hold on the host route; under R4-2 and R4-14 it depends wholly on SQ-02 (a)–(c) | None needed: CA already cites SQ-02 for W14-04. Recorded so the joined witness does not count W14-04 (i) toward App-side hold evidence |
| F-20 | C at `f05c7e4cd` | R4-20 additions are not yet in C, so v0.2 still uses local labels | Re-point L-EXEC-19, ⟨fx-app-import⟩ and ⟨rev-A3⟩ when C-v0.4 lands |
| F-21 | RS R5 / R4-1 | The model destination (R4-1) is recorded per run. HOSTING records supplied guidance per thread and turn. Whether the destination can change mid-run (a model switch between turns) is not stated | DEL-04-03 with DEL-01-01: record the destination per turn, or state that a change starts a new run |

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-E1 App-side run holds `UNRESOLVED{D6}` (DECISION-2), deferred to SWBPIPE **SQ-02** ((a)–(d)); HP-1 and HP-2 not adopted (R4-2) | The owner, on the SWBPIPE answer to SQ-02; then App/shared owners (OI-014) | Before any App-side positive hold case; before the App fixes its realization family | §3.6 values App holds *not enforceable* or *not established*; action during hold recorded; F-10 at C1 |
| U-E2 Host placement of the hold machine and required-tool check `UNRESOLVED{OI-013}` / `{OI-014}` | Shared contract owner with SWB implementation owner (SQ-20); App/shared owners | Before shared/host implementation boundary contracts | Semantics supplied; no placement |
| U-E3 Multi-row A4 purpose after partial lapse (WD U-05c; AP U-03; CA DI-7) | DEL-04-01 with the Owner (C1 carry) | Before re-hold and lapse fixtures run | Whole-scope request; CH-8 (ii) HELD |
| U-E4 Arrival-order rule SP-6 versus counting a prior act on current content (R4-5 keeps it open) | The owner, with DEL-02-01 and DEL-04-01 | Before hold-machine fixtures run | SP-6 applied as ADOPTED (R4-5), standing PROPOSED |
| U-E7 "On subject absent" path in the declaration | DEL-02-01 | Next comparison | Waiting "subject absent" |
| U-E8 App person identity scheme; App act control construction | DEL-01-04 (later, D1) with DEL-04-03 | Before App capture fixtures | CH-23 (ii) AWAITING INPUT |
| U-E9 Person-attributed acts on host content through the App (proxy control) | Host owner (DEP-001), **SQ-25** | Before any App proxy is offered | None offered |
| U-E10 Harness capability names (WD U-08) | DEL-02-01 with DEL-01-01 | Before App-side required-tool check | *not established*; not holdable (R4-21) |
| U-E11 Version compatibility statements (C U-C9; WD U-07) | Host owner with DEL-02-01, **SQ-18 (d)** | Before version fixtures against a real host | Equality only |
| U-E12 Host capture-evidence reference (WD U-05b; AP U-04a) | Host owner (DEP-001), **SQ-01** | Before host act-recording integration | No host-content arrival can be performed |
| U-E13 Constraint receipt on the host route (WD U-19; P U-P10) | Host owner with DEL-03-02, **SQ-02** | Before CH-27 | AWAITING INPUT |
| U-E14 Host library receipt of other origins, adaptation evidence with derived-from, holding library and run records (TR-6…TR-8) | Host owner (DEP-001), **SQ-17, SQ-18, SQ-19** | Before RT host-side cases | RT host links AWAITING INPUT |
| U-E15 Per-turn supplied guidance in host loops (WD U-29; LOOP Q-4) | Host owner, **SQ-19 (a)** | Before host supplied-link evidence | *supplied* **unknown** |
| U-E16 Physical carriage of the declared part (WD U-01) and carriage-manifest representation; revision algorithm (WD U-03) | DEL-02-01 with DEL-04-03; TBD-003 | Before OUT-002 schema and transfer code | All semantic; verification uses method designations |
| U-E17 First connected operation `UNRESOLVED{OI-021}` | Owner via outside SWB session with App/shared owner, **SQ-04, SQ-05** | Before connected-activity SoW | FX-PIPE-01 only; MT-13, CH-11 production HELD |
| U-E18 Extension promise `UNRESOLVED{OI-003}` and real exposure (C U-C7; WD U-23) | Owner with host contract owner; exposure **SQ-11** | Before exposure claims | FA-1 fixture assumption |
| U-E19 Selection slot policy and host precedence (WD U-10); registration as an act (AP U-08) | DEL-02-02 (later) with DEL-02-01, DEL-04-01 | Before host-origin discovery in the App | RT-6/RT-7 registration side not exercised |
| U-E21 App-file subject and App-side library in the shared fixture (R4-20) | DEL-03-01 (C-v0.4) | Before App-capture and host→App cases run | Local labels kept |
| U-E22 Model destination per run versus per turn (F-21) | DEL-04-03 with DEL-01-01 | Before App run-record writer | Recorded per run (R4-1) |

Closed at v0.2: U-E5 (R4-9), U-E6 (R4-6). Withdrawn: U-E20 (live `turn/interrupt` behavior), because nothing relies on it (R4-2).

## Verification cases

Designed, **not run**. No code, fixture runner, host or act exists. Labels use
C's evidence mapping; all current states are DESIGNED, AWAITING INPUT or HELD.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-E-01 Report completeness and outcomes | MT-1…MT-15 against §3.3, §3.4, §3.5 | Every CR element present, including CR-14 as information only; each outcome distinct; pass rule applied; PS-2 wording; registered ≠ compatible (MT-3) | VER-001 (AC-001) |
| VC-E-02 Hold under direct autonomy | CH-1, CH-2, CH-27 | Waiting persists; no success, receipt, grant or host check releases it; CH-27 AWAITING INPUT (SQ-02) | VER-002 (AC-002) |
| VC-E-03 Interruption and replay | CH-3, CH-4, CH-5, CH-21 | Same arrival identities; recovered events not back-filled; unknown never performed; held call dispatched unchanged; replay issues nothing | VER-002 (AC-002) |
| VC-E-04 Lapse, re-hold and finality | CH-6…CH-10, CH-24 | R2-19 before resume; re-hold after resume (R4-3); ended runs final and continuation inherits nothing (R4-4); subject-absent path | VER-002, VER-003 |
| VC-E-05 Act evidence and fabrication negatives | CH-20, CH-23, CH-25, CH-26, CH-28; WD VC-21/VC-22 | Only SP-satisfying acts count; conversation, elicitation answers (R4-12), A14, agent records and prior acts (R4-5) do not; decision actor ≠ recorder | VER-003 (AC-003) |
| VC-E-06 A5 item rules | CH-15…CH-19 | MX-1…MX-8 and MC-1…MC-4 as tabulated (R4-7); never "all accepted" over a reduced subject | VER-003 |
| VC-E-07 A12 rules | CH-11…CH-14, CH-29 | Refused → waiting; pending → waiting; established → performed; refused never supersedes (R4-6); declaration naming no setting invalid (R4-9); supersession not lapse | VER-003 |
| VC-E-08 App→host trace | RT-1…RT-5, RT-9, RT-10 | Original and revised identities kept apart; links separate; derived-from correct; holding library per HL-1…HL-3; unsupported receiving explicit; model destination recorded, never gated (R4-1); host links AWAITING INPUT with SQ IDs | VER-004 (AC-004) |
| VC-E-09 Host→App refinement | RT-6…RT-8 | Host identity kept on opening; draft not selectable; registered identity derived from the host tuple; no rebinding or overwrite; history referenced, no act imported | VER-005 (AC-005) |
| VC-E-10 Ownership and open items | §2, §8, §10, UNRESOLVED against SoW CLM-001…003, REQ-006/007, TBD-001…005, DEP-001, DECISION-2 | Every excluded act has an owner; every held item resolved or carried with owner, point of need and SQ ID where host-dependent; no external commitment or joined qualification claimed | VER-006 (AC-006) |
| VC-E-11 Evidence account | RT-11 inventory for this file (EXEC-v0.2) and its source versions; W14 map | Candidate and source identities listed; states truthful; DEL-09-06 named as joined-witness owner; no witness claimed | VER-007 (AC-007) |
| VC-E-12 Hold support under D6 | MT-2, MT-15, CH-22, CH-27, CH-29 against §2 and §3.6 | No App hold is claimed without HP-H evidence; HP-1/HP-2 appear nowhere as enforcement; HP-3/HP-4 are best effort only; *action during hold* is recorded; model-supplied constraint → *not established*; values change only on an SQ-02 answer | VER-002, VER-006 |

Limit: passing these later would show local contract and fixture conformance
only. It would establish no host implementation, round-trip execution,
provider adoption or human act (SoW VER-007; AX-002).
