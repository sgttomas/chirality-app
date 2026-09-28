# Host boundary and integration guide
- Contribution: DEL-03-04/GUIDE-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (new-host integration checklist, §3), OUT-002 (App/shared versus host responsibility/interface matrix, §2), OUT-003 (guide completeness checks and recorded comparison, §4); REQ-001…REQ-008; AC-001…AC-008 through designed VER-001…VER-008
- Basis:
  - Branch base 6e18505e3 (accepted basis); **inputs pinned at commit `f05c7e4cd`** (parent instruction for W10; replaces the Wave-2 brief's `ba0b37123`; every Wave-1 v0.3 blob is identical at both commits).
  - ScopeOfWork.md sha256 203c09288850d33ec3490d00da48bd6bbbc91ae395141c1374c4c6b04ad9a436 (fully read, including the 10-row minimum receiving map, CLM-001…CLM-006, REQ-001…REQ-008, AC-001…AC-008, VER-001…VER-008, TBD-001…TBD-009); Dependencies.csv sha256 b41eacd01cdef10e455017cda7afdfae85b2a2a2e989fad481d697f4e862ac17 (ACTIVE rows DEP-03-04-001…020); `_REFERENCES.md`.
  - `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7db2d74619ed47d184f44938bb06f1e2abda0a304a9e11b9230d0960da) §1, §2 (V4-HI-01…04), §3 (V4-HI-10…12), §4 (V4-HI-20…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §7 (V4-HI-50…52), §8 and §8.1 (V4-HI-60…65), §9 (V4-HI-70/71), **§10 (checklist), §11 (SWBPIPE receiving limits)**.
  - Run `APP-V4-FIRST-INCREMENT-20260928`: `OWNER_DECISIONS.md` (sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c) DECISION-1 (D1–D4) and DECISION-2 (D5, D6); `R1_RESOLUTIONS.md` (2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4); `R2_RESOLUTIONS.md` (77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088); `R3_RESOLUTIONS.md` (202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf); `R4_RESOLUTIONS.md` (50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24); `BRIEFS.md` (sha256 77a42f8a8c8260285b4142d3a6392a07daead16010b209139efc0d3efc60a21f) "Common brief" and "Wave 2 — common additions".
- Consumed inputs (all read with `git show f05c7e4cd:<path>`; none from the working tree, where v0.4 revisions under R4 are in progress). Short names are used throughout:

  | Short | Contribution / version | File | sha256 at `f05c7e4cd` |
  |---|---|---|---|
  | **C** | DEL-03-01/C-v0.3 | `CATALOG_AND_READ_BASIS.md` | ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26 |
  | **P** | DEL-03-02/P-v0.3 | `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | ec0db87f239bc42e2e3e953d660ce3c4ceddf605d7b98cf1393f97a099b699cf |
  | **ADAPTER** | DEL-03-03/ADAPTER-v0.1 | `ADAPTER_ENABLEMENT_AND_RECEIVING.md` | 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074 |
  | **ACT** | DEL-04-01/ACT-POLICY-v0.3 | `ACT_AND_POLICY_CONTRACT.md` | b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128 |
  | **AS** | DEL-04-02/AS-v0.3 | `AUTONOMY_AND_STANDING_EXCHANGE.md` | 7b634137bb8402f3eaedc943dab0c5f1114b9d4433d2b94e13540ac0bf8e0514 |
  | **RS** | DEL-04-03/RS-v0.3 | `RECORD_SEMANTICS.md` | 925f35ca27bd7d1e71a375883ada9903267408af57312eed1ae02b47776a3528 |
  | **WD** | DEL-02-01/WD-v0.3 | `WORKFLOW_DECLARATION.md` | 84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb |
  | **WD-EX** | DEL-02-01/WD-EX-v0.3 | `EXAMPLES.md` | 0f1058d7f0990e766b3effc3d3de24fc16383197874cced1f5b4212419cf018d |
  | **EXEC** | DEL-02-03/EXEC-v0.1 | `EXECUTION_COMPATIBILITY.md` | e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8 |
  | **LOOP** | DEL-05-01/LOOP-v0.3 | `LOOP_RECEIVING_CONTRACT.md` | 6b771c8027787193d536fa3507214a8cc579d6ec2f476ee880609c920b6f25c7 |
  | **PANEL** | DEL-05-02/PANEL-v0.3 | `PANEL_RECEIVING_CONTRACT.md` | 4c47764d3af434c23e63dcc2c10d28f18a4a94546d63d452855c471cfe47bee9 |
  | **HOSTING** | DEL-01-01/HOSTING-BOUNDARY-v0.3 | `HOSTING_BOUNDARY.md` | 34c3383402aabe6e9347aa2f111318538c4a2a4ca85adb8fffff7e439fdde94e |
  | **SPIKE** | DEL-01-01/PIN-SPIKE-v0.1 | `PIN_SPIKE_0.158.0.md` | 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115 |
  | **CA** | DEL-09-06/CA-v0.1 | `CONNECTED_ACTIVITY_CONTRACT.md` | 685349b25981ca8333929207890514120d63753cdedd67ae0bad986fc5d45e62 |
  | **RELAY** | DEL-09-06/RELAY-v0.1 | `RELAY_QUESTIONS_SWBPIPE.md` | 3e34575def8d1fef63b5f5e64f0f90a0984d03b8b42f61fe899dd2eab023b2d1 |
  | **XT** | DEL-09-09/XT-v0.1 | `EXTERNAL_TRACE_CASES.md` | 8f098c79f1da28af1b461210c36cca1124a25e226e802f2203b46ce7052df8cd |

  R4 rulings are applied **over** these bytes wherever they change a statement this guide relies on, and are cited as "per R4-n" (§5). DEL-02-02, DEL-02-04, DEL-01-04, DEL-07-01, DEL-07-02, DEL-08-01 and DEL-08-02 are referenced by accepted SoW meaning only; they are outside this undertaking (D1) and have no Design file. SWBPIPE answers, commitments or contributions: **none received** (DEP-001).
- Receivers: the application builder of any new host (SoW Purpose; HI §10), for SWBPIPE only through the human relay; the App/shared host-contract integration owner (this deliverable's completeness owner, CLM-001); each supplying deliverable above, to confirm its matrix row at the next comparison (DEP-03-04-005…019); DEL-09-06 (the RELAY ledger and the joined-witness step map read the same host contributions); DEL-09-09 (external-access and extension rows); closeout C1 (register and SoW-text findings, §6). SCC-CASE-002 names no M-row for DEL-03-04, so no independent receiver comparison is yet scheduled (§6 F-9).

---

## 0. How to read this guide

**What it is.** The integrated receiving guide for adding a host. For every
obligation in the SoW's minimum receiving map it names: the App/shared
contribution that defines the obligation (file, version, section); what the
host must contribute, cited by the relay question that asks for it
(`SQ-nn` from RELAY-v0.1); who decides each open choice; and the
obligation's current standing. It then restates HI §10's checklist as
checks a host answers before claiming each obligation, and records a
completeness check over both.

**What it is not.** It recreates no contributing contract; each meaning
stays in the file cited. It selects no wire field, type, transport, hash or
canonicalization algorithm, persistence, process placement or shared
component placement (OI-013, OI-014; DEL-03-01 TBD-003; DEL-03-02 TBD-002;
DEL-03-03 TBD-007). It assigns no SWBPIPE construction: the checklist states
what *any* host answers before a claim, and SWBPIPE-specific items appear only
as relay-question references. It designs no PEC or Domains path (§2 row 10 is
conditional). It performs, records or implies no human act. It runs nothing.

**Standing vocabulary (this guide).** Each matrix line carries one or more of:

| Standing | Meaning | Can support |
|---|---|---|
| **defined draft** | An App/shared v0.x definition exists at `f05c7e4cd` (evidence label *illustrative*, C §10 mapping) | Completeness of the definition only |
| **relay pending** | A host contribution is needed; the question exists in RELAY-v0.1 (ladder standing *prepared*, CA §7.2); relay, answer, commitment, delivery, adoption and examination are **not observed** | Nothing about the host |
| **owner-open** | An open choice with a named owner and point of need (OI-nnn, TBD-nnn, U-nn, D6) | Nothing; the choice is recorded, never made here |
| **host-owned** | Construction, facility or evidence that belongs to the host owner (CLM-001; HI §1); the App/shared side only receives it | Nothing until an identified host candidate supplies it |
| *outside undertaking (D1)* | Qualifier: the App/shared definer is a deliverable this undertaking does not start | Accepted SoW meaning only |

**Identifier notes.** Act names are A1–A14 (R-1). Class values are C §3.1's
five. Outcomes are P §9 and C §4.1. Dispositions are WD §4.3.4's six. Two
different "TBD-007" exist: **03-04/TBD-007** (this SoW: OI-022, PEC first
receiving envelope) and **03-03/TBD-007** (DEL-03-03 SoW: MCP-versus-CLI
and related choices, ADAPTER §9). This guide always prefixes them.
Receiving-map rows are numbered 1–10 in SoW order; matrix lines are `M<row>.<n>`;
checklist checks are `HC-<item>.<n>`; completeness checks are `CC-n`; gaps are
`G-n`.

---

## 1. Settled boundary the matrix preserves (CLM-001…CLM-006)

| # | Settled or adopted boundary | Source |
|---|---|---|
| B-1 | The host owns domain objects and truth, its catalog implementation, the one validation/application route, receipts, origin and undo, host UI, and offering, capturing, recording and presenting human acts. The person performs every decision act; the recorder is separately attributable | CLM-001; HI §1, §4–§6; P §1 |
| B-2 | App/shared deliverables own semantic definitions and App-side receiving; they do not own SWBPIPE construction (embedded loop, native layer, panel, domain connection), which stays with the outside SWBPIPE session | CLM-001, CLM-003; HI §1, §11; U1/U5 |
| B-3 | A written interface, a prepared relay file or its transmission is not agreement, delivery, integration, qualification or adoption | CLM-006; HI §1; RELAY §0; CA §7.2 |
| B-4 | DECISION-1 D2: five acts are reserved to the person for App/shared contracts in the first increment; the host names and enforces its own list (V4-HI-30); operation-specific additions await OI-021; host adoption not shown (DEP-001) | OWNER_DECISIONS D2; ACT §3, §8.3 P-01 |
| B-5 | DECISION-1 D3: App routine tool permission (A14) is the user's own Codex setting; hosts have no classifier mode; the SWB default proposal mode applies | OWNER_DECISIONS D3; ACT §8.3 P-04 |
| B-6 | DECISION-2 D5 (per R4-1): host content read through the external channel may reach the App conversation's selected model, cloud included; the App records and shows the destination and does not gate on it; a host may restrict its own channel; V4-HOST-02 still governs the host's embedded agent | OWNER_DECISIONS D5; R4-1 |
| B-7 | DECISION-2 D6 (per R4-2): App-side run holds stay `UNRESOLVED{D6}` pending SQ-02; drafts carry per-checkpoint hold support, record "action during hold", and adopt neither interposed App code (HP-1) nor reliance on `turn/interrupt` (HP-2) | OWNER_DECISIONS D6; R4-2; EXEC §2, §3.6 |
| B-8 | Codex `0.158.0` is a definition/generation pin only; it establishes no qualification | OWNER_DECISIONS D4; HOSTING §7, §10; SPIKE |

---

## 2. OUT-002 — App/shared versus host responsibility/interface matrix

### 2.0 Row summary

| Row | Receiving-map obligation | Primary App/shared definitions | Host contribution (RELAY) | Principal open choices | Standing (summary) |
|---|---|---|---|---|---|
| 1 | Catalog and read meaning | C §2–§4, §6, §8; ACT §5.1, §8 | SQ-04 (a)(b), SQ-11, SQ-12, SQ-24, SQ-26 | OI-003 (03-04/TBD-003); representation and identity algorithm 03-01/TBD-003 (C U-C1); OI-021 | defined draft; relay pending; three-surface map owner-open |
| 2 | Single validation/application route | P §1–§2, §9; ACT §5.3, §6; C §4.1; LOOP §6 | SQ-05 (d), SQ-06, SQ-09 | OI-013/OI-014 (loop-side checking) | defined draft; host-owned; relay pending |
| 3 | Basis | C §5; P §3.2, §5, §6, §11, §12 | SQ-03 (a)(b), SQ-07, SQ-08 (b) | Host generation meaning (C U-C2); subject-identity scope (C U-C3) | defined draft (rule INTEGRATION); relay pending |
| 4 | Origin, undo and proposal presentation | P §3, §4, §7, §8, §9; AS §7; ADAPTER §5 | SQ-03 (c)(d), SQ-08, SQ-09 (c)(f), SQ-10, SQ-14, SQ-22 | DEL-03-02 TBD-002 mechanisms; undo mechanism (P U-P8) | defined draft; host-owned; relay pending |
| 5 | Human acts and compact records | ACT §2–§4, §8–§9; RS §2–§10; EXEC §5 | SQ-01, SQ-03, SQ-05 (b)(c), SQ-19, SQ-21, SQ-23, SQ-25 | OI-021 additions; ACT U-03 multi-row A4; OI-013/OI-014 record placement | defined draft; relay pending (SQ-01 blocks every positive host-content case) |
| 6 | Autonomy | ACT §4.4, §5–§8; AS §2–§6; P §3.3, §4.4 | SQ-02, SQ-05 | D6 (deferred to SQ-02); consequence vocabulary (ACT U-02); host defaults (ACT U-06) | defined draft; relay pending; owner-open |
| 7 | Loop and panel | LOOP §1–§10; PANEL §1–§6 | SQ-20 (informational), SQ-22, SQ-23; **no SQ for model interface, endpoint/key, responsiveness** (G-3) | OI-013; OI-014; LOOP N-OPEN-1…3; DEP-05-01-024 | defined draft; host-owned; owner-open |
| 8 | Host methods and roles | WD §3–§6, §9; WD-EX; EXEC §3, §4, §6; HOSTING §8 S-6, §8.2 | SQ-01, SQ-02 (d), SQ-11, SQ-17, SQ-18, SQ-19 | D6; WD U-09 seat mapping; DEL-02-02 / DEL-02-04 (D1) | defined draft; relay pending; partly outside undertaking (D1) |
| 9 | Optional external catalog access (conditional) | ADAPTER §1–§10; ACT V-10; HOSTING §3, §6; XT §3 | SQ-02, SQ-06, SQ-08, SQ-12…SQ-16 | 03-03/TBD-007 (OC-1…OC-12); ADAPTER U-X1 (per R4-13), U-X3 | defined draft; relay pending; owner-open |
| 10 | Selected connectors (conditional) | None in this undertaking (DEL-07-01/07-02, DEL-08-01/08-02 outside D1); staging in CA §6 | None by design (RELAY §3 "Not included") | 03-04/TBD-007 (OI-022), 03-04/TBD-008 (OI-023), 03-04/TBD-009 (OI-026) | outside undertaking (D1); owner-open |

Every row keeps the supplier/receiver pair the SoW names; the file cited is
where the meaning lives. "Host contribution" names what the host supplies,
never how.

### 2.1 Row 1 — Catalog and read meaning (HI §2, §3; HI §10 item 1)

| # | Obligation (receiving meaning) | App/shared definition (file, version, §) | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M1.1 | Every person-available operation (reads, changes, host checks, undo) described once, in an identified **catalog edition**; completeness is a parity rule | C-v0.3 §2 (invariants 1–5) | The actual catalog and edition identity (SQ-04 (a); SQ-12) | Representation and placement: C U-C1 (03-01/TBD-003) — App/shared capability-contract owner with host/consumer owners | defined draft; host-owned; relay pending |
| M1.2 | Nine entry elements: identity/version (equality only), purpose, input schema with explicit target identification, availability with reasons, effects, result with standing, errors with effect statements, class, exposure per surface | C-v0.3 §3, §3.2, §3.3; consumed by LOOP-v0.3 §2.2 and ADAPTER-v0.1 §4.2 | Entry content per operation (SQ-04 (a)); version compatibility statements if any (SQ-18 (d)) | C U-C9 (host owner with DEL-02-01) | defined draft; relay pending |
| M1.3 | Distinct non-success results — unavailable (HI-04 parity only), not permitted, channel not enabled, not exposed on this surface (host-reported), error — each with evaluated basis; never empty success; loop-side *not offered* and *missing* are not host results | C-v0.3 §4.1–§4.4; ACT-v0.3 §6 rows 1–2, 8–11; **per R4-16** the App reports *channel not enabled* when its own configuration is off, the host when its channel is off | Unavailable reasons with the same meaning on every surface; result statements mappable to these terms (SQ-09 (a)); exposure reporting (SQ-11) | — | defined draft; relay pending |
| M1.4 | Class element: five values (none; may apply within granted autonomy; proposal only; reserved to the person; no policy basis with reason) with policy-record reference, value standing and host adoption | C-v0.3 §3.1; ACT-v0.3 §5.1, §8.1, §8.3 | The host's own class per operation and its reserved list (SQ-05 (a)–(c)) | Operation-specific additions and first operation's class: `UNRESOLVED{OI-021}` — owner via outside SWB session with App/shared owner; consequence vocabulary ACT U-02 — DEL-04-01 with host policy owner | defined draft (D2 adopted; P-03 DERIVED); relay pending; owner-open |
| M1.5 | Read results return the same meaningful content and standing marks the person sees: currency, "host checks passed: ‹named checks›" with evaluated basis, limitations, faithfully carried act evidence, lapse state, agent findings (A3) — never "checked" | C-v0.3 §6.1–§6.2; AS-v0.3 §8; ACT-v0.3 §9 (R-4 label rule) | Views, results, diagnostics and standing (SQ-04 (b) which check the activity uses); where findings are held and whether storing them is a change (SQ-24) | C U-C5 (host owner) | defined draft; host-owned; relay pending |
| M1.6 | Three-surface responsibility (H, E, X): which parts are generated from, checked against, or hand-built beside the catalog, recorded before any conformance claim; extension promise preserved and **not claimed** | C-v0.3 §8 (every cell *unagreed*); XT-v0.1 §4 (V4-EXM-24 trace plan, CMP-01…CMP-15), §5 (work account, OI-003 disposition record); ADAPTER-v0.1 §9 OC-8 | Per-surface production route (SQ-12); the one new operation for the trace (SQ-26) | `UNRESOLVED{OI-003}` retain/narrow/defer — owner with host contract owner (03-04/TBD-003) | owner-open; relay pending |
| M1.7 | Catalog received by the three consumers: workflow required-tool references (opaque catalog identity), loop tool offering (all nine elements, reserved entries always offered), external native-tool mapping | WD-v0.3 §4.2.1–§4.2.4; LOOP-v0.3 §2.2 TL-1…TL-5; ADAPTER-v0.1 §4.1–§4.2 (NM-1…NM-4); EXEC-v0.1 §3 | Exposure per surface and first-activity entries on E and X (SQ-11); native-to-catalog mapping (SQ-12) | Shared catalog-schema checker: `UNRESOLVED{OI-014}` (C §8 row; WD §9 A-11; LOOP §10.2 (b)) | defined draft; relay pending; owner-open |
| M1.8 | Operations used by the first connected activity (read, change, non-mutating check) | CA-v0.1 §2.3, §2.5 DI-1…DI-3; fixture FX-PIPE-01 (C-v0.3 §10) is invented and proposed only | Candidate operations, check and environment (SQ-04) | `UNRESOLVED{OI-021}` — owner via outside SWB session with App/shared owner (03-04/TBD-006) | owner-open; relay pending |

### 2.2 Row 2 — Single validation/application route (HI §4 V4-HI-20, -25; HI §10 item 2)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M2.1 | One route for person, embedded agent and external agent; channel is attribution only; equivalence rule (same outcome and error meaning for equivalent requests); the only permitted difference is authority, reported as *not permitted* naming the governing treatment | P-v0.3 §1, §2; ADAPTER-v0.1 §6 RP-1, RP-2; LOOP-v0.3 §6 V-4, V-5 | The route itself (host-owned); outcome statements distinct from transport status (SQ-09 (a)); whether a validation refusal and an application refusal are distinguished (SQ-09 (d)(e)) | — | defined draft; host-owned; relay pending |
| M2.2 | Treatment resolved on the host route at validation and again at application; loop and adapter relay intent and any constraint, never decide; direct without an effective direct treatment → *not permitted*, never converted into a proposal | ACT-v0.3 §5.3, §5.5, §6; P-v0.3 §2; C-v0.3 §4.1 (closing rule); R-3 | Settings reference in force at application (SQ-05 (d)); adoption of P-01…P-06 and the R2 treatments (SQ-05 (c); ACT U-04 (d)) | Host adoption and enforcement (DEP-001) — host owner | defined draft; relay pending |
| M2.3 | Canonical outcome taxonomy per item, including refused — invalid, refused — stale, queued, accepted, rejected, withdrawn, applied (receipt) with applied-outcome association, application error with effect statement, outcome unknown (observer-attributed); success ≠ acceptance; queued ≠ applied | P-v0.3 §9, §10; C-v0.3 §4.1; RS-v0.3 §5; ADAPTER-v0.1 §4.5 (M-1…M-5); AS-v0.3 §8 "route and outcome" | Result forms mapped to these terms; item application grouping (SQ-09 (a)(b)(f)) | P U-P4, U-P5, U-P7 — host owner | defined draft; relay pending |
| M2.4 | App-side and loop-side pre-route failures: catalog-schema checking before host domain validation; malformed or truncated calls never executed with empty arguments; *not offered* never dispatched | LOOP-v0.3 §6 V-1…V-3, §7 MC-1…MC-9 | Host-loop construction of these checks (host-owned; no SQ — see G-3) | Loop placement and parsing `UNRESOLVED{OI-013}` — shared contract owner with SWB implementation owner; any shared checker `UNRESOLVED{OI-014}`; LOOP T-OPEN-1 (DEL-05-01 with DEL-03-02 and host owner); DEP-05-01-024 model interface (supplier UNKNOWN) | defined draft; host-owned; owner-open |
| M2.5 | No second agent route: no fixture, adapter or loop defines an alternate mutation path or applies outside the host route | P-v0.3 §2 (last bullets); ADAPTER-v0.1 RP-1; PANEL-v0.3 §4 H-4 | Confirmation that the external seam uses the one route (SQ-12) | — | defined draft; relay pending |

### 2.3 Row 3 — Basis (HI §3 V4-HI-11; §4 V4-HI-23; HI §10 item 3)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M3.1 | Every read returns one basis descriptor: workspace identity, generation (host lineage epoch), model revision, canonical content identity, identity method designation; a read lacking any element is *basis incomplete* | C-v0.3 §5.1, §5.2 (the SoW's "canonical content hash" is received as canonical content identity plus method designation, R-6) | Full descriptor on every read; meaning of a new generation (SQ-07 (a)(b)) | Algorithm and canonicalization: C U-C1 (03-01/TBD-003); generation meaning C U-C2 — host owner with DEL-04-03 | defined draft; relay pending |
| M3.2 | Per-row/object **subject content identity** with method designation, distinct from the read-level identity; used for act binding, per-item staleness, held-call subject binding and resulting objects | C-v0.3 §5.3; RS-v0.3 §7 (L-1, L-2); P-v0.3 §3.1, §3.4 | Subject identities per object kind and their attribute scope (SQ-03 (a)(b)) | Subject-identity scope C U-C3 — host owner with DEL-03-01/DEL-03-02 | defined draft; relay pending |
| M3.3 | A later action cites the relied-on basis unchanged, with relied-on target identities; never recomputed or replaced by a queue-time, acceptance-time or application-time basis (a later observed basis is a separate element) | C-v0.3 §5.4; P-v0.3 §3.2; HI §11 risk recorded in C §5.4 and P §12 | Whether a submission keeps the originally inspected basis rather than a queue-time basis (SQ-07 (c)) | Multi-read reliance C U-C4 — host owner with DEL-03-02 | defined draft; relay pending (HI §11 risk) |
| M3.4 | Stale refusal per item, reporting relied and current bases and failing targets; identity-based de-duplication precedes the basis check (a retry is never stale by its own effect); re-draft is a new proposal with lineage; no retargeting | P-v0.3 §5, §6; C-v0.3 §5.4 ("no longer holds", R2-13 INTEGRATION); CA-v0.1 §2.3 CA-4 | Per-item check on relied-on targets; re-check after acceptance; which changes invalidate a proposal (SQ-07 (d)(e)(f)); de-duplication order (SQ-08 (b)) | Host confirmation of the rule (C U-C3; P U-P3 narrowed) — host owner | defined draft (rule INTEGRATION); relay pending |
| M3.5 | Non-mutating reads, examinations and host checks citing a basis are never refused stale; they state both bases when they differ | C-v0.3 §5.4 (PROPOSED) | Confirmation (C U-C10) | Host owner | defined draft (PROPOSED); relay pending |
| M3.6 | Read-then-action comparison with an intervening edit (M3-CP): the relied-on reference equals the read basis at every step; refusal shows both; applied association references the new basis and resulting objects | P-v0.3 §11; C-v0.3 §9 (VC-C-04) | A candidate-bound observation (SQ-27) | — | defined draft (designed); DEL-03-01 AC-004 held until an actual return exists |

### 2.4 Row 4 — Origin, undo and proposal presentation (HI §4 V4-HI-21, -22, -23, -24; HI §10 item 4)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M4.1 | Origin on every change: author type, author identity (**per R4-15** the value *unverified* is allowed), seat role meaning, channel, conversation, workflow identity tuple and run, standing at drafting, both settings references, governing checkpoint constraint (**per R4-14** with a carriage assurance: App-assured, host-held, model-supplied or absent), reason; the host origin mark is linked, not copied; a mismatch is an evidence limit | P-v0.3 §3.3; ADAPTER-v0.1 §5.1–§5.5; LOOP-v0.3 §6.2; RS-v0.3 R7, R11 | Recorded origin elements, which are verified, readability of the origin mark, caller authentication (SQ-14) | Caller identity mechanism: ADAPTER OC-6 — host owner with App owner | defined draft; relay pending |
| M4.2 | Proposal identity (retry keeps it; re-draft gets a new one), change items, change-item content identity; acceptance unit = change item; row / multi-row / batch acceptance as one A5 per item or one A5 listing items | P-v0.3 §3.1, §3.4, §4.1–§4.3; ACT-v0.3 §7 | Who mints the proposal identity and when; read by identity (SQ-08 (a)(d)); A5 bound to change-item content (SQ-03 (c)) | Identity representation and mechanics: DEL-03-02 TBD-002 / P U-P1 — relevant contract and host owners | defined draft; relay pending |
| M4.3 | Direct application (only in an effective direct grant state, no governing constraint) carries receipt, origin mark, undo route and later-check route; no acceptance is recorded or implied | P-v0.3 §4.4; AS-v0.3 §7 (abstract host contribution: origin reference, undo route, later-check route, receipt reference) | These four host elements per applied change; resulting objects (SQ-03 (d); SQ-09; SQ-10) | Host availability of each (AS U-05) — host owner | defined draft; host-owned; relay pending |
| M4.4 | Undo is a change through the one route with its own origin, basis, treatment, outcome and receipt; the relation *reverses ⟨receipt⟩*; governed by the policy record of the reversed operation; acts on changed content lapse normally | P-v0.3 §4.5; AS-v0.3 §7 "undo interaction"; C-v0.3 §10 OP-C10; ACT-v0.3 §8.3 P-03 (R3-4); ADAPTER-v0.1 RP-6 | Undo route, scope, receipt relation, meaning of "publication" (SQ-10) | Undo mechanism P U-P8 — host owner | defined draft; host-owned; relay pending |
| M4.5 | Repeated submission of one proposal identity → at most one effect per item: a **host obligation to be evidenced**, not a recorded fact; each submission recorded separately with only observed effects | P-v0.3 §7; ADAPTER-v0.1 §5.6 (PI-1…PI-4); RS-v0.3 §5 | De-duplication durability across restart and the domain evidence of one effect (SQ-08 (c)(e)) | Mechanism: DEL-03-02 TBD-002 — relevant contract and host owners | defined draft; relay pending (HI §11: no durable exactly-once outcome established) |
| M4.6 | Outcome unknown: reported by whoever lost observation; last observed state only; recovery by read or retry with the same identity; nothing back-filled | P-v0.3 §9; ADAPTER-v0.1 §7.4; LOOP-v0.3 §6.3; EXEC-v0.1 §4.12 (RP-1…RP-8) | Receipt durability and resolution of an unknown by later read (SQ-09 (c)) | — | defined draft; relay pending |
| M4.7 | Proposals shown in the host's own views: old/new values, affected objects, reason, origin, per-item disposition with actor, stale indication, lineage, item-left events; the control says "accept", never "approve" | P-v0.3 §8; PANEL-v0.3 §3.3, §4 H-1…H-6; ACT-v0.3 §9 | Which views, and how the panel references a position in them (SQ-22) | — | defined draft; host-owned; relay pending |

### 2.5 Row 5 — Human acts and compact records (HI §5, §9; HI §10 item 5)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M5.1 | Canonical acts A1–A14 with actor, subject and evidence; execution distinct from acceptance, checking, approval and reliance; one act never implies another; no synthetic prerequisite | ACT-v0.3 §2.1–§2.4, §3 (S1–S12); P-v0.3 §10; HOSTING-v0.3 §11 | — | — | defined draft (settled distinctions cited) |
| M5.2 | Reserved acts (D2: A4, A5 where a proposal is required, A6, A7, A12, A13 enabling); A10 DERIVED; A13 disabling INTEGRATION; operations that perform reserved acts are reserved (P-02) | ACT-v0.3 §3, §8.3 P-01, P-01a, P-02; C-v0.3 §3.1 rule 1; AS-v0.3 §2 | The host's own named list and its enforcement (V4-HI-30); operation-specific additions (SQ-05 (b)(c)) | Operation-specific additions `UNRESOLVED{OI-021}` (03-04/TBD-001 residue) — owner via outside SWB session with App/shared owner | defined draft (adopted decision, App/shared); relay pending (host adoption not evidenced) |
| M5.3 | Checkpoint satisfaction needs attributable **capture evidence** from the capturing surface (host act facility for host content; App interface for App content); **per R4-5** an act counts only if captured at or after the checkpoint's arrival; **per R4-12** user-input and elicitation answers are never act evidence | ACT-v0.3 §4.5; RS-v0.3 §6.1 ("capture evidence references"), §6.2 HA-1, HA-7; EXEC-v0.1 §4.5 (SP), §5 CAP-1…CAP-9; HOSTING-v0.3 §6 (R9) | A stable capture-evidence reference per act kind and for act-declined events, its elements, surfaces and durability; no elicitation or prompt capture (**SQ-01**, priority P1); whether any App-captured act on host content is accepted (SQ-25) | App act control construction: DEL-01-04 (outside D1); App person identity EXEC U-E8 | relay pending (**blocks every positive host-content checkpoint**); App side outside undertaking (D1) |
| M5.4 | Faithful recording (A9): recorder ≠ decision actor, cites capture evidence, is a record shape and never satisfies a checkpoint by itself; no faithful record through a reserved act-performing operation; a host faithful-record operation, if any, meets the four R2-2 conditions | ACT-v0.3 §2.4, §8.3 P-02; RS-v0.3 §6.2 HA-2, HA-7, HA-9 | Whether any such host operation exists and meets the conditions (SQ-21) | — | defined draft; relay pending |
| M5.5 | Acts bind to content (A5/A10 → change-item content identity; A4/A6/A7 on host content → subject content identity; App files → file content identity; A12/A13 → setting content) and lapse visibly on change; applying an accepted item does not lapse its A5; **per R4-6** a later A12 supersedes only when established | ACT-v0.3 §2.5; RS-v0.3 §7 (L-0…L-12); C-v0.3 §5.3, §6.2 rule 4; P-v0.3 §3.1 rules 2–3; AS-v0.3 §8 | Subject/change-item identities (SQ-03); host display of lapse, supersession, stale after acceptance and reversal (SQ-23) | Multi-row A4 purpose after partial lapse: ACT U-03 / RS U-07 — DEL-04-01 with the owner; return to c₀ after lapse RS U-12 — host owner with DEL-04-03 | defined draft; relay pending; owner-open |
| M5.6 | Compact run record R1–R13 with the host project for host-agent runs: workflow identity and revision, conversation, settings, requested operations and outcomes, receipts by reference, human acts, model; **per R4-11** RS adds arrival/performance ordinals, run-resumed event, re-held/replaced annotations, A12 control effect, "prior act not counted", *continues ⟨run⟩*, action during hold, transfer links, revision verification, compatibility-report reference and **model destination (R4-1)** | RS-v0.3 §2 (FA-1…FA-9), §3, §4, §9; HOSTING-v0.3 §8 S-7, §8.2 (App side) | Host run recording in the shared meaning; full workflow identity in host records; relay of records and history by reference (SQ-19 (b)(c)) | Host persistence and placement `UNRESOLVED{OI-013}` (RS U-06); App record location with `OI-014` owners (RS U-05); serialization RS U-04 (DEL-04-03 with DEL-03-01, TBD-003) | defined draft (v0.4 additions pending under R4-11); host-owned; relay pending |
| M5.7 | Settings-in / record-out exchange between autonomy display and records (CASE-002 M3) | RS-v0.3 §8; AS-v0.3 §6 (byte-identical sections) | — | Record representation RS U-04 / AS U-10 | defined draft (single executor; independent check pending) |
| M5.8 | Act-declined event (A4, A6, A7, A12) resolves a checkpoint negatively; run-ended event leaves it *waiting*; **per R4-4** an ended run is never resumed — acts after run end are shown "after run end" and change nothing; continuation is a new run with *continues ⟨run⟩* | ACT-v0.3 §2.3; RS-v0.3 §3; EXEC-v0.1 §4.8, §4.9 | Capture of decline events (SQ-01) | — | defined draft; relay pending |

### 2.6 Row 6 — Autonomy (HI §6; HI §10 item 6)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M6.1 | Per operation class, a grant value (direct / propose) within a representation-neutral scope, set by the person through A12; governs host operations only; visible, changeable during work, recorded per run | ACT-v0.3 §5.1, §5.2, §5.4; AS-v0.3 §2; RS-v0.3 R6 | Host controls that establish and report the grant (host-owned); presentation of grant states (SQ-05 (e)) | Consequence dimension of scope: ACT U-02 — DEL-04-01 with host policy owner; ask host participation (SQ-05 (f)) | defined draft; host-owned; relay pending; owner-open |
| M6.2 | Seven grant display states (effective; effective (policy default); requested by agent; set by person, not yet confirmed; unconfirmed; not set; refused (reason)); two settings references per operation (at route decision; in force at application, host-reported or *unconfirmed*) | AS-v0.3 §3; ACT-v0.3 §5.4; P-v0.3 §3.3 | Settings reference at application (SQ-05 (d)); host enforcement of *unconfirmed* and re-resolution at application (AS U-04, U-06) | — | defined draft; relay pending |
| M6.3 | Conservative defaults for consequential classes; SWB model changes (P-03): *may apply within granted autonomy*, default *propose*, row / multi-row / batch acceptance, the person may widen; widening bounded (W-a…W-j); narrowing and widening never convert a queued proposal | ACT-v0.3 §5.5, §5.6, §7, §8.3 P-03; AS-v0.3 §2 | Class and default per host operation; host adoption of P-03 (SQ-05 (a)(c)) | Defaults for other consequential classes ACT U-06 — host policy owner (DEP-001) | defined draft (class DERIVED, default accepted); relay pending |
| M6.4 | Declared checkpoints override autonomy; an A5 checkpoint forces *propose* for that operation in that run (P-05); a direct request under the constraint is *not permitted* naming it, never converted; **per R4-14** carriage is assurance-rated and model-supplied carriage alone does not satisfy R2-12 | ACT-v0.3 §4.4, §8.3 P-05; P-v0.3 §3.3, §4.4; WD-v0.3 §4.2.2, I-7; ADAPTER-v0.1 §5.3 GC-1…GC-5 | Per-request constraint receipt, or a host-held copy of the declaration / run association; *not permitted* naming the constraint; host holds before dispatch per surface (**SQ-02**, priority P1) | App-side hold points `UNRESOLVED{D6}` — owner, deferred to the SQ-02 answer (R4-2); GC-3/GC-5 held for DEL-02-03 with host owner (ADAPTER U-X3) | relay pending (V-CP1, LOOP FX-C9, PANEL PC-24, WD VC-11, EXEC CH-27, ADAPTER XF-25 AWAITING INPUT); owner-open |
| M6.5 | No policy basis (P-06): direct not permitted, proposing confers no permission, A12 widening refused, dependent production held; fixtures report *held*, never pass | ACT-v0.3 §8.3 P-06; C-v0.3 §3.1 rule 4; AS-v0.3 §2 | Classing the first operation (SQ-05 (a)) | `UNRESOLVED{OI-021}` (C OP-C11) | defined draft (INTEGRATION); owner-open |
| M6.6 | Routine tool permission (A14) is not autonomy: App side is the user's Codex setting (D3), recorded only in RS R13; hosts have no classifier mode and no separate routine permission layer | ACT-v0.3 §8.3 P-04; RS-v0.3 R13; HOSTING-v0.3 §6.6, §11; LOOP-v0.3 §1; PANEL-v0.3 §1 | None | — | defined draft (adopted decision D3) |

### 2.7 Row 7 — Loop and panel (HI §1; HI §10 item 7)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M7.1 | The host embedded loop is replaceable behind a four-subject boundary (messages and run association, tools, events, checkpoints); it has host consumers only and is never merged with the App's Codex path | LOOP-v0.3 §1, §2 (§2.1–§2.4), §3 | Loop construction (host-owned; DEP-001); intended placement, informational (SQ-20) | Loop placement, parsing, persistence and panel assembly `UNRESOLVED{OI-013}` (03-04/TBD-004) — shared contract owner with SWB implementation owner | defined draft; host-owned; owner-open |
| M7.2 | Model interface: OpenAI-compatible Chat Completions with tool calls; detailed representation waits for its supplier | LOOP-v0.3 §1, §4; LOOP UNRESOLVED DEP-05-01-024 | The model interface basis the host loop uses — **no relay question exists (G-3)** | DEP-05-01-024 supplier UNKNOWN; App/shared embedded-integration owner receives or agrees | defined draft; owner-open |
| M7.3 | Native endpoint and key boundary: local server by default, cloud only by the person's choice plus a key, no cloud fallback, key never visible to the script, native layer enforces the endpoint; local operation's only destination is the configured server (V4-HOST-02) | LOOP-v0.3 §5.1 (N-1…N-7), §5.2 (MS-01…MS-11) | Native layer and endpoint enforcement (host-owned) — **no relay question exists (G-3)** | LOOP N-OPEN-1…3 — App/shared embedded-integration owner with SWBPIPE owner; the owner if V4-HOST-02 is affected | defined draft; host-owned; owner-open |
| M7.4 | Validation order (parse → offered → schema → host validation → treatment); malformed and truncated calls reported, never executed | LOOP-v0.3 §6, §7 (see M2.4) | Host-loop realization (host-owned) | As M2.4 | defined draft; host-owned |
| M7.5 | Responsiveness: the loop does not block the host interface; observation protocol without numeric thresholds | LOOP-v0.3 §8 (RS-1…RS-4) | Placement choice and candidate observations (host-owned) — **no relay question exists (G-3)** | Quantitative criterion LOOP R-OPEN-1 — the owner, if wanted | defined draft; host-owned |
| M7.6 | Checkpoint evaluation in host loops: reached-when observation, declared subject class binding, dispositions, hold semantics from EXEC §4 | LOOP-v0.3 §2.4 (§2.4.1–§2.4.3); EXEC-v0.1 §4 (per R4-3, R4-4, R4-5, R4-6, R4-7); WD-v0.3 §4.3 | Whether the host holds a call before dispatch on the embedded surface (SQ-02 (d)); placement of the hold machine (SQ-20) | EXEC U-E2 `UNRESOLVED{OI-013}` / `{OI-014}` | defined draft; relay pending; owner-open |
| M7.7 | Panel: conversation, workflow selection, proposal queue and checks, plus declared checkpoints and the active grant; agent results appear in host tables and views; no agent-private surface; "accept" wording; lapse and supersession visible | PANEL-v0.3 §3.1–§3.6, §4 (H-1…H-6), §5 | Panel assembly, tables and views (host-owned); proposal views (SQ-22); lapse/supersession/stale/reversal display (SQ-23); grant presentation (SQ-05 (e)) | Which party evaluates required-tool outcomes in the host (PANEL UNRESOLVED) — host owner; DEL-02-03 only under OI-014 | defined draft; host-owned; relay pending |
| M7.8 | Reusable panel/components only where a repeated responsibility is agreed; no common loop or service presumed | PANEL-v0.3 §6; LOOP-v0.3 §10.1–§10.2; WD-v0.3 §9 (A-1…A-12) | — | `UNRESOLVED{OI-014}` (03-04/TBD-005) — App/shared contract owners; host side `UNRESOLVED{OI-013}` | owner-open (every confirmation "None") |

### 2.8 Row 8 — Host methods and roles (HI §10 item 8; V4-WF-01…06)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M8.1 | Portable declared part: expected inputs, required tools by catalog identity (never an adapter tool name), checkpoints naming a closed-list act (A4, A5, A6, A7, A12), returned outputs with promised standing, returned evidence by reference; requirement ≠ restriction | WD-v0.3 §3, §4.1–§4.7; WD-EX-v0.3 E1–E7 | Host workflows and skills authored by the host/method owner (SQ-18 (a)); reading the declared part at the App's declaration contract version (SQ-17 (b)) | Physical carriage of the declared part WD U-01 — DEL-02-01 with consumers | defined draft; host-owned; relay pending |
| M8.2 | Source-qualified identity {kind, origin, source root, name, revision} + derived-from; holding library as a non-identity fact; promised vs observed chain (listed, selected, resolved, supplied, adopted, observed) | WD-v0.3 §6.1–§6.3; EXEC-v0.1 §6.1, §6.2 (holding library resolved at W7); RS-v0.3 R2 | Listing carried workflows unadapted with original origin and host holding library (SQ-17 (a)); host identity display (SQ-18 (a)) | Revision algorithm WD U-03 — DEL-02-01 with DEL-04-03 | defined draft; relay pending |
| M8.3 | Required-tool compatibility report and pass rule, including *unsupported* for "checkpoint hold not enforceable on this surface" (**per R4-8**) and *not holdable* harness-capability kind (a) in App runs (**per R4-21**) | WD-v0.3 §4.2.4; EXEC-v0.1 §3 (§3.1–§3.8), §3.6 hold support | Exposure per surface (SQ-11); who evaluates compatibility and holds for host runs and how unsupported outcomes are shown (SQ-17 (c)) | Harness capability naming WD U-08 — DEL-02-01 with DEL-01-01 and DEL-02-03 | defined draft; relay pending |
| M8.4 | Checkpoint semantics and hold machine: arrival, satisfaction predicate, dispositions, re-hold after resume (**per R4-3**), no resumption of ended runs (**R4-4**), capture after arrival (**R4-5**), mixed items MX-3/MX-6/MX-8 (**R4-7**); App-side holds never claimed where not enforceable | WD-v0.3 §4.3 (§4.3.1–§4.3.7); EXEC-v0.1 §4 (§4.1–§4.14); ACT-v0.3 §4 | Host capture evidence (SQ-01); host-held evaluation or constraint receipt, host holds before dispatch (SQ-02) | `UNRESOLVED{D6}` App hold points (R4-2); EXEC U-E4 (SP-6 vs counting prior acts) — owner may prefer to count prior acts (R4-5); ACT U-03 | defined draft; relay pending; owner-open |
| M8.5 | Transfer App → host (package plus carriage manifest; no transport assumed) and host → App refinement; adaptation creates a new identity with host origin and derived-from; no identity or act inheritance | EXEC-v0.1 §6.3–§6.7; WD-v0.3 §6.4; CA-v0.1 §4 | Relay form needed (SQ-17 (d)); adaptation as new revision with derived-from; checkpoint comparison (SQ-18 (b)(c)) | Registration, drafts and selection policy: DEL-02-02 *(outside undertaking, D1)* | defined draft; relay pending; partly outside undertaking (D1) |
| M8.6 | Four roles behind a single host seat; seat role meaning carried on every dispatch; additive role guidance supplied, with per-thread/turn supplied-guidance evidence ("supplied ≠ adopted") | WD-v0.3 §5 (§5.1–§5.3, SEAT-1…3); HOSTING-v0.3 §8 S-6, §8.2; RS-v0.3 R3, R5a | Per-turn guidance source and content identity in host loops (SQ-19 (a)) | Host seat → role mapping WD U-09 — DEL-02-01 with SWB implementation owner and DEL-02-04; role supply DEL-02-04 *(outside undertaking, D1)*; guidance distribution `UNRESOLVED{OI-018}` (WD U-14) | defined draft (WD, HOSTING); role supply outside undertaking (D1); relay pending |
| M8.7 | Host methods can be tested and refined in the App: App runs go through stock Codex; the host revision is opened read-only and refined as a draft | HOSTING-v0.3 §1; EXEC-v0.1 §6.5; CA-v0.1 §8 W14-09 | Host revision relayed with identity (SQ-18 (a); SQ-27 (a)) | DEL-02-02 *(outside undertaking, D1)*; CA F-1: V4-EXM-14 cannot complete in this undertaking | defined draft; outside undertaking (D1) |

### 2.9 Row 9 — Optional external catalog access (HI §7; HI §10 item 9) — conditional

This row applies only where a host chooses to expose its catalog to an
external agent. It is never a startup input for a host without it (REQ-001).

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M9.1 | External access is off unless the person enables it (A13) through a capturing surface; disabling is also A13; an agent may only request (A8); host enablement is authoritative; **per R4-13** an App-side Codex configuration an agent could write is never A13 evidence, and the host's refusal is the authoritative "off"; enablement grants no autonomy | ADAPTER-v0.1 §3.1–§3.3 (E-1…E-9); ACT-v0.3 §2.1 (A13), §10 V-10; R2-3 | Off by default; A13 capture with reference; readable enablement state; *channel not enabled* when off; disable behavior for queued proposals (SQ-13) | Where A13 is captured App-side: ADAPTER U-X1 — set by DEL-04-01 (per R4-13) with the owner and host owner; enablement loci OC-4 | defined draft; relay pending; owner-open |
| M9.2 | Channel states disabled / enabled / endpoint-unavailable / operation-unavailable, never replacing C §4.1 outcomes; *enablement unconfirmed* treated as disabled | ADAPTER-v0.1 §3.2; C-v0.3 §4.1 (R4-16 reporter rule) | Enablement read (SQ-13) | — | defined draft; relay pending |
| M9.3 | The host selects the seam (MCP server, CLI over the live controller, or both), built from the catalog; the App receives it | ADAPTER-v0.1 §2, §4.1 (NM-1…NM-4), §9 OC-1, OC-2, OC-8; HOSTING-v0.3 §3, §6 (App's Codex at pin 0.158.0); SPIKE §4–§6 | Seam choice; derivation (generated / checked / hand-built); native-to-catalog mapping (SQ-12) | 03-03/TBD-007 (OC-1…OC-12) — App external-host integration owner with external host owner; derivation evidence feeds `UNRESOLVED{OI-003}` | defined draft; relay pending; owner-open |
| M9.4 | Same route, same validation, same grant and reserved acts as the host UI; a channel-specific host rule is stated by the host as a governing treatment, never as a class value or grant | ADAPTER-v0.1 §6 (RP-1…RP-6); ACT-v0.3 §5.3, §6 | Whether "apply stays in the human review route" is a class, a channel rule or a fixed policy, and the outcome of a direct external request (SQ-06) | — | defined draft; relay pending |
| M9.5 | Carriage of origin, grant in force, governing checkpoint constraint and proposal identity on retry, each with its carriage assurance (**per R4-14**) | ADAPTER-v0.1 §5.1–§5.6 (GC-1…GC-5, PI-1…PI-4) | Constraint receipt or host-held declaration (SQ-02); identity minting and durable de-duplication (SQ-08); origin elements (SQ-14) | Carriage mechanism OC-7 and realization family OC-2 — 03-03/TBD-007 owners; D6 (R4-2) | defined draft; relay pending; owner-open |
| M9.6 | Machine-local endpoint (local process, local socket or loopback origin); the App never changes the person's sandbox or permission settings | ADAPTER-v0.1 §3.3 E-7, §3.5; HI V4-HI-52 | Transport and locality; sandbox reach (SQ-15) | OC-5 — host owner with App owner | defined draft; relay pending |
| M9.7 | Data boundary: **per R4-1 (DECISION-2 D5)** content read over the channel may reach the App conversation's selected model, cloud included; the App records the run's model destination (RS) and shows it in the channel status (ADAPTER) as information only; no gating; the host may restrict its own channel. ADAPTER §3.4's "U-X2 open" and XF-36 HELD are superseded | ADAPTER-v0.1 §3.4 as amended by R4-1; RS-v0.3 R5 plus the R4-1/R4-11 destination element | Whether the host imposes its own destination rule (SQ-16, now a host-side question only) | Host channel policy (DEP-001) — host owner | defined draft (App side settled by D5); relay pending (host side) |
| M9.8 | External control witness (inspect → submit → engineer accepts → receipt, with stale, duplicate, interruption and unknown cases) and adapter fixture inventory | XT-v0.1 §2 (IN-01…IN-29), §3 (V4-EXM-25); ADAPTER-v0.1 §10 (XF-01…XF-39) | Identified candidate, host checks and the engineer's actual act (SQ-27; SQ-01) | — | defined draft (designed, not run); relay pending |

### 2.10 Row 10 — Selected connectors (HI §8, §8.1; HI §10 item 10) — conditional, not designed here

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M10.1 | PEC, where selected: consumed through its own interface; examined-through pin, source reference, coverage and freshness; operational reliance only on qualified/released coverage adopted by the consumer; qualified/current, limited/stale/failing and absent distinguished | DEL-07-01 and DEL-07-02 accepted SoW meaning only *(outside undertaking, D1)*; HI V4-HI-61…63 | Host integration of PEC use, if selected (host-owned); PEC provider construction by the PEC owning project | 03-04/TBD-007 (OI-022) — App consumer owner and PEC owner; point of need: before operational consumer reliance | outside undertaking (D1); owner-open |
| M10.2 | Domains, in the later research-to-design increment: provider/query, admission/source basis, freshness, research workflow, host use and the human's candidate approval, each separately evidenced | DEL-08-01 and DEL-08-02 accepted SoW meaning only *(outside undertaking, D1)*; HI §8.1 | Host use and approval route (external SWBPIPE owner and the human), later | 03-04/TBD-008 (OI-023) — owner with Domains/SWB/App receiving owners; 03-04/TBD-009 (OI-026) provider ownership — owner with App/Domains/SWB definition owners | outside undertaking (D1); owner-open |
| M10.3 | Independent absent/limited paths: first connected work proceeds without PEC or Domains; a missing feed never implies empty work, readiness or permission | CA-v0.1 §6 (ST-0…ST-5, "Later"); HI V4-HI-62, -64; RELAY §3 "Not included" (PEC and Domains excluded with reasons) | None for the first activity | — | defined draft (staging only) |

### 2.11 Supporting contributions that serve several rows

| Contribution | Role in this guide | Rows served |
|---|---|---|
| HOSTING-v0.3 (DEL-01-01) and SPIKE-v0.1 | The App's own Codex boundary: stock App Server owned by the App process; server-request register (every request answered, declined or errored); A14 origins; supplied-guidance evidence; supplier facts at the definition pin | 5 (S-7 evidence), 6 (A14), 8 (S-6, §8.2), 9 (App's Codex receives the host seam) |
| CA-v0.1 (DEL-09-06) | First connected activity step map (CA-0…CA-5, CA-H, CA-R), each step's App contributions and host contributions by SQ; owner/check allocation (§5); staging (§6); evidence standing ladder (§7.2); V4-EXM-14 witness design (§8) | All rows (joined use) |
| RELAY-v0.1 (DEL-09-06) | The only channel for host questions: SQ-01…SQ-27, priority groups P1…P7, source-to-question map, return ledger (all *not observed*) | Host-contribution column of every row |
| XT-v0.1 (DEL-09-09) | V4-EXM-25 external control suite, V4-EXM-24 three-surface trace, generated-versus-adapted work account, OI-003 disposition record (recorded, never performed) | 1, 9 |
| C-v0.3 §10 FX-PIPE-01 | The one invented fixture catalogue and timeline; every example here that names OP-Cn, T-n, PR-n or RC-n means C's invented material, not SWBPIPE behavior | All rows (examples only) |

### 2.12 Excluded acts one-for-one (REQ-008; AC-007)

| # | Excluded act or production (REQ-008) | Owner (claim) | This guide's part |
|---|---|---|---|
| X-01 | Catalog/schema construction | App DEL-03-01 (CLM-002) | Cites C; builds nothing |
| X-02 | Proposal/outcome schema construction | App DEL-03-02 (CLM-002) | Cites P |
| X-03 | App external receiving implementation | App DEL-03-03 (CLM-002) | Cites ADAPTER |
| X-04 | Portable workflow contract production | App DEL-02-01 (CLM-003) | Cites WD, WD-EX |
| X-05 | Execution-compatibility implementation | App DEL-02-03 (CLM-003) | Cites EXEC |
| X-06 | Additive role supply | App DEL-02-04 (CLM-003) — outside this undertaking (D1) | Names the row (M8.6); no definition exists to cite |
| X-07 | Loop receiving definition | App DEL-05-01 (CLM-003) | Cites LOOP |
| X-08 | Panel receiving definition | App DEL-05-02 (CLM-003) | Cites PANEL |
| X-09 | Adopted policy definition | App DEL-04-01 (CLM-004) | Cites ACT; decides no policy |
| X-10 | Autonomy receiving implementation | App DEL-04-02 (CLM-004) | Cites AS |
| X-11 | Record writer/reader construction | App DEL-04-03 (CLM-004) | Cites RS |
| X-12 | PEC receiving and fallback | App DEL-07-01, DEL-07-02 (CLM-005) — outside D1 | Row 10 conditional only |
| X-13 | Domains receiving and later-activity production | App DEL-08-01, DEL-08-02 (CLM-005) — outside D1 | Row 10 conditional only |
| X-14 | Host domain, catalog, validation, application, receipts, origin, undo, UI, loop, native layer, panel construction | Host owner; SWBPIPE outside session (CLM-001) | Host-contribution column; relay references only |
| X-15 | Human decisions (A4, A5, A6, A7, A10, A12, A13) and professional reliance | The actual human actor; the accountable professional (CLM-001, CLM-004) | Never performed, recorded or implied |
| X-16 | PEC provider production | PEC owning project (CLM-005) | Not addressed beyond M10.1 |
| X-17 | Domains provider allocation | Owner decision retained in 03-04/TBD-009 (CLM-005) | Carried as owner-open |
| X-18 | Actual external relay | The human (CLM-006) | RELAY ledger is DEL-09-06's; this guide never claims relay |
| X-19 | Commitments and adoption | Each receiver (CLM-006) | Standing "relay pending" never promoted |
| **Retained** | Guide integration, the interface matrix and their completeness checks | **DEL-03-04** (App/shared host-contract integration owner) | §2–§4 of this file |

### 2.13 Open issues carried at their owners and points of need (TBD-001…TBD-009; AC-006)

| SoW item | Open issue | Owner (literal, SoW) | Point of need (literal, SoW) | Current standing in this guide |
|---|---|---|---|---|
| TBD-001 | OI-001 reserved acts | Owner with App/SWB contract owners | Before operation-policy production contracts | **Adopted at App/shared level** by DECISION-1 D2 (ACT P-01); operation-specific residue `UNRESOLVED{OI-021}`; host list and enforcement relay pending (SQ-05). SoW text still reads open (C1 pointer, F-5) |
| TBD-002 | OI-002 classifier routine permissions | Owner with App/SWB contract owners | Before permission-policy implementation | **Adopted** by DECISION-1 D3 (ACT P-04). SoW text still reads open (C1 pointer, F-5) |
| TBD-003 | OI-003 automatic catalog extension | Owner with host contract owner | Before claiming extension capability or fixing its acceptance criterion | owner-open; evidence route XT §4–§5; SQ-26 (M1.6) |
| TBD-004 | OI-013 per-host loop placement and persistence | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | owner-open (M2.4, M5.6, M7.1, M7.6, M7.8); SQ-20 informational only |
| TBD-005 | OI-014 shared contract/component placement | App/shared contract owners | Before structural/production contract allocation | owner-open (M1.7, M7.8; WD §9 rows all "None") |
| TBD-006 | OI-021 first connected activity | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution; host evidence before corresponding connected-journey integration/examination and fallback-replacement decision | owner-open (M1.8, M6.5); SQ-04/SQ-05 inform it; neither timing blocks this guide's definition |
| TBD-007 | OI-022 PEC first receiving envelope | App consumer owner and PEC owner | Before operational consumer reliance | owner-open; outside undertaking (M10.1) |
| TBD-008 | OI-023 Domains receiving contract and timing | Owner with Domains/SWB/App receiving owners | Before later Domains-enabled design increment | owner-open; outside undertaking (M10.2) |
| TBD-009 | OI-026 Domains provider ownership | Owner with App/Domains/SWB definition owners | Before allocating Domains provider production and committing its integration | owner-open; outside undertaking (M10.2) |
| — (added) | D6 App-side hold points | Owner (DECISION-2), deferred to SQ-02 | Before App-side hold fixtures | `UNRESOLVED{D6}` (M6.4, M8.4, M9.5) |

---

## 3. OUT-001 — New-host integration checklist (HI §10 restated against these contracts)

**How to use it.** For each HI §10 item, a host that wants to claim the
corresponding receiving obligation (a) **supplies** the listed contribution
and (b) **answers** the listed questions with identified evidence. Each check
is phrased so that a reviewer can mark it *answered with evidence*, *answered
without evidence*, *not answered* or *not applicable*. The "Evidence before a
claim" line states the minimum that must exist before the claim is made. The
checklist adds no human checkpoint and authorizes no App implementation of a
host (HI §10 closing sentence). For SWBPIPE, the questions are carried by
RELAY-v0.1 (referenced as SQ-nn); for any other host they are the same checks.

### HC-0 Preconditions for any claim

| Check | Supply / answer | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-0.1 | Which identified host candidate (source revision, build, configuration, date) does the claim concern? | CA §7.1 labels; XT §2 IN-02; SQ-27 (a) | A candidate identity; a claim without it is *illustrative* only |
| HC-0.2 | Which operation(s), check and acting surface does the first activity use, and under which autonomy? | CA §2.2, §2.5; SQ-04; `UNRESOLVED{OI-021}` | The owner's OI-021 selection; until then fixture FX-PIPE-01 only |
| HC-0.3 | How will host answers and evidence reach the App, with custody? | RELAY §4 ledger; CA §7.2 ladder; SQ-27 (c) | A recorded return with source, revision, date and custody |

### HC-1 Describe every operation once in a capability catalog (HI §2; matrix row 1)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-1.1 | Does every operation a person can perform — reads, changes, host checks and undo — have exactly one entry in an identified catalog edition? | C §2 invariants 1–3 | Catalog edition identity; comparison of person-available operations against entries |
| HC-1.2 | Does each entry state all nine elements as meanings (not gestures), with target identification explicit in the input schema and every error carrying an effect statement? | C §3, §3.3, §4.2 | Entry texts for the claimed operations (SQ-04 (a)) |
| HC-1.3 | Are *unavailable*, *not permitted*, *channel not enabled*, *not exposed on this surface* and *error* stated distinctly, each with the evaluated basis, and never as an empty success? Is the unavailable reason the same on every surface? | C §4.1–§4.4; ACT §6 | A three-surface comparison of one failed precondition (C §10.6 pattern) on the candidate |
| HC-1.4 | Does each entry carry a class with its policy basis, and are reserved entries always described and, where exposed, offered? | C §3.1, §2 invariant 5; ACT §8 | The host's class per operation (SQ-05 (a)) |
| HC-1.5 | Is exposure declared per surface (exposed / not exposed / unagreed), independently of class? | C §3 element 9 | Exposure values for the claimed entries (SQ-11) |
| HC-1.6 | Do reads return the same content, diagnostics and standing marks the person sees, with host checks named and based, and agent findings never shown as checks? | C §6; AS §8; ACT §9 | Side-by-side read on the candidate; where findings are held (SQ-24) |
| HC-1.7 | For each surface, is each catalog element generated, checked or hand-built? | C §8; XT §5.1 | Per-cell production route (SQ-12). **A claim that the three surfaces are "generated from, or checked against, one catalog" is not made while any cell is *unagreed*; no automatic-extension claim is made while `UNRESOLVED{OI-003}`** (SQ-26; XT §5.2) |

### HC-2 Route every change through one validation and application path (HI §4; row 2)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-2.1 | Do the person, the embedded agent and any external agent submit to the same route, with the channel recorded as attribution only? | P §2; ADAPTER RP-1 | Route identity; equivalent-request comparison across channels |
| HC-2.2 | Is treatment resolved on the host route at validation and again at application, and is a direct request without an effective direct treatment answered *not permitted* (never converted)? | ACT §5.3, §6; P §2 | Treatment outcome observations; settings reference at application (SQ-05 (d)) |
| HC-2.3 | Do results state outcomes in terms that map to P §9 and C §4.1, distinct from transport status, including application error effect and outcome unknown? | P §9; ADAPTER §4.5 | A mapping of result forms (SQ-09) |
| HC-2.4 | Does the embedded loop check catalog schema before host domain validation, and report malformed or truncated calls without executing them? | LOOP §6, §7 | Loop observations on the candidate (no SQ yet, G-3) |

### HC-3 Return a basis with every read; check it on every change (HI §3–§4; row 3)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-3.1 | Does every read return workspace identity, generation, model revision, canonical content identity and method designation? What starts a new generation? | C §5.1–§5.2 | Sample reads (SQ-07 (a)(b)) |
| HC-3.2 | Does every row/object carry a subject content identity with method designation, and what does it cover per object kind? | C §5.3 | Sample reads; scope statement (SQ-03 (a)(b)) |
| HC-3.3 | Does a submission keep the originally inspected basis, never a queue-time basis? | C §5.4; P §3.2, §12 | The M3-CP comparison on the candidate (P §11) (SQ-07 (c)) |
| HC-3.4 | Is staleness judged per item against the relied-on targets, with both bases reported; does de-duplication by proposal identity precede the basis check; is a later selection never retargeting? | P §5, §6; C §5.4 | Intervening-edit case (CA-4) observed (SQ-07 (d)–(f); SQ-08 (b)) |

### HC-4 Mark origins; offer undo; show proposals in the host's own views (HI §4; row 4)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-4.1 | Which origin elements are recorded for each change, which are verified, and can the App read the origin mark to link it? | P §3.3; ADAPTER §5.4 | Origin record sample (SQ-14) |
| HC-4.2 | Who mints the proposal identity, is it readable by identity, and is acceptance per change item (row, multi-row, batch)? | P §3.1, §4.3; ACT §7 | Identity and per-item decision observations (SQ-08 (a)(d); SQ-03 (c)) |
| HC-4.3 | Does each direct application carry a receipt, origin mark, undo route and later-check route, and report resulting objects? | P §4.4, §9; AS §7 | Applied association on the candidate (SQ-03 (d); SQ-10) |
| HC-4.4 | Is undo a change through the one route whose receipt records what it reverses, governed by the reversed operation's policy? | P §4.5; ACT P-03 (R3-4) | Undo observation (SQ-10) |
| HC-4.5 | What domain evidence shows one effect per item when the same proposal is submitted twice, including across a restart? | P §7 | Domain evidence, not transport or session de-duplication (SQ-08 (c)(e)) |
| HC-4.6 | Do the host's own views show old/new values, affected objects, reason, origin, per-item disposition, stale indication and lineage, with "accept" (never "approve") on the control? | P §8; PANEL §3.3, §4 | View identification (SQ-22) |

### HC-5 Name the reserved human acts and bind them to content (HI §5, §9; row 5)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-5.1 | Which reserved-act list does the host name and enforce, and does it add operation-specific acts? | ACT §3, §8.3 P-01/P-01a/P-02; V4-HI-30 | The host's list and enforcement evidence (SQ-05 (b)(c)); D2 does not show host adoption |
| HC-5.2 | For each act the host's facility captures (and for act-declined events), is there a stable capture-evidence reference with actor, kind, bound content identity and method, scope, purpose and time, readable on the relevant surfaces and durable across restart? Is any act ever captured through an elicitation or agent-mediated prompt? | ACT §4.5; RS §6; EXEC §5 CAP-6 (R4-12) | **SQ-01**. Without it, no host-content checkpoint reaches *performed*, and no act-recording claim is made |
| HC-5.3 | Does the host offer any operation that stores an agent's faithful record, and if so does it meet all R2-2 conditions? | ACT P-02; RS HA-9 | SQ-21 |
| HC-5.4 | Does each act bind to content and lapse visibly when that content changes, with supersession, stale-after-acceptance and reversal shown distinctly? | ACT §2.5; RS §7; AS §8 | Lapse display observation (SQ-23; SQ-03) |
| HC-5.5 | Does each workflow run leave a compact record with the host project (workflow identity and revision, conversation, settings, operations and outcomes, receipts by reference, acts performed, model), linking host receipts rather than copying them? | RS §4 (R1–R13, with R4-11 additions); V4-HI-70/71 | Host run record sample (SQ-19 (b)(c)) |
| HC-5.6 | Will the host accept any person's act on host content captured by the App, or only its own facility? | EXEC §5 CAP-1 | SQ-25 |

### HC-6 Choose autonomy defaults for consequential operations (HI §6; row 6)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-6.1 | For each consequential class, what is the default grant value, is it visible and changeable by the person during work, and is it recorded with each run? | ACT §5, §7; AS §3; RS R6 | Grant presentation and settings reference at application (SQ-05 (d)(e)) |
| HC-6.2 | For model changes, is the default *propose* with row, multi-row or batch acceptance, widenable only by the person within the §5.6 bounds? | ACT §7, §5.6; P-03 | SQ-05 (a)(c); host adoption of P-03 |
| HC-6.3 | When a workflow declares an A5 checkpoint on an operation, does the route receive a per-request constraint or evaluate its own copy of the declaration, return *not permitted* naming it for a direct request, and hold "before dispatch" checkpoints itself on each surface? | ACT §4.4; P §3.3, §4.4; WD I-7; ADAPTER §5.3 | **SQ-02**. Until answered, the checkpoint-under-direct-grant case is AWAITING INPUT and App-side holds stay `UNRESOLVED{D6}` (R4-2) |
| HC-6.4 | Does the host present grant states including a policy default and a refused setting, and would it take part in a consequence vocabulary? | AS §3; ACT U-02 | SQ-05 (e)(f) |

### HC-7 Select reusable panel/components where they fit; implement the loop/catalog/model connection under the host's ownership and data boundary (row 7)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-7.1 | Does the embedded loop preserve the four-subject boundary (messages, tools, events, checkpoints) and stay separate from the App's Codex path? | LOOP §1, §2 | Loop observation on the candidate |
| HC-7.2 | Which model interface does the loop use, and how are "no arguments", truncation and malformed calls expressed? | LOOP §4, §7; DEP-05-01-024 | Model-interface basis (**no relay question yet, G-3**) |
| HC-7.3 | Does the native layer enforce the endpoint, keep the key out of the script, default to the configured local server and never fall back to cloud? | LOOP §5 (N-1…N-7; MS-01…MS-11) | Observed destinations with configuration (**no relay question yet, G-3**) |
| HC-7.4 | Does the host interface stay usable during long streams and large reads? | LOOP §8 | RS-1…RS-4 observations (**no relay question yet, G-3**) |
| HC-7.5 | Does the panel provide conversation, workflow selection, proposal queue and checks, plus declared checkpoints and the active grant, with results in host tables and no agent-private surface? | PANEL §3, §4, §5 | View and panel observations (SQ-22; SQ-23) |
| HC-7.6 | Which reusable component, if any, is used, and has its responsibility been agreed? Where will the loop, panel assembly, persistence, hold machine and required-tool check live? | PANEL §6; LOOP §10; WD §9 | Agreement record under OI-014; host placement under OI-013 (SQ-20, informational). No reuse is presumed |

### HC-8 Write the host's own workflows and skills; test them in the Chirality App (row 8)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-8.1 | Does each host workflow declare inputs, required tools by catalog identity, checkpoints with closed-list acts, outputs with promised standing and evidence by reference? | WD §3, §4 | Host workflow list or sample (SQ-18 (a)) |
| HC-8.2 | Does the host carry full source-qualified identity with derived-from and holding library, and can it list an App-carried workflow unadapted with its original origin? | WD §6; EXEC §6.2 | SQ-17 (a); SQ-18 (a) |
| HC-8.3 | Can the host read the App's declared part at its declaration contract version, evaluate required tools and holds for host runs, and report *unsupported* explicitly? | WD §4.2.4; EXEC §3, §3.6 (R4-8) | SQ-17 (b)(c) |
| HC-8.4 | Is an adaptation a new revision with host origin, derived-from and a checkpoint comparison, never inheriting the original's identity or acts? | EXEC §6.4, §6.6; WD §6.4 | SQ-18 (b)(c) |
| HC-8.5 | Can the host loop record, per turn, the source and content identity of each guidance input it supplies? | HOSTING §8.2 (App side); RS R3; WD §6.2 | SQ-19 (a); otherwise *supplied* is recorded **unknown** |
| HC-8.6 | Can a host revision be relayed to the App, opened read-only and refined? | EXEC §6.5; CA §8 W14-09 | Needs DEL-02-02 (outside D1); no claim of V4-EXM-14 completion in this undertaking (CA F-1) |

### HC-9 Optionally expose the catalog to external agents (HI §7; row 9) — only if the host offers external access

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-9.1 | Is external access off by default, enabled and disabled only by the person's A13 captured by the host, readable by the App, and answered *channel not enabled* when off? | ADAPTER §3; ACT A13; R4-13 | SQ-13; an App-side configuration is never A13 evidence |
| HC-9.2 | Which seam (MCP, CLI or both) does the host offer, is it derived from the catalog, and is the native-to-catalog mapping supplied? | ADAPTER §4.1, §9; C §8 X column | SQ-12 |
| HC-9.3 | Does the external channel use the same route, validation, grant and reserved acts, and is any channel-specific rule stated as a governing treatment? | ADAPTER §6 | SQ-06 |
| HC-9.4 | Is the endpoint strictly local, and what sandbox access does it need? | ADAPTER E-7, §3.5 | SQ-15 |
| HC-9.5 | Does the host restrict which model destinations may receive content read over its channel? | R4-1 (D5); ADAPTER §3.4 | SQ-16; the App records and shows the destination and applies no gate |
| HC-9.6 | Are origin, constraint, grant and proposal identity carried or host-held, and with which assurance? | ADAPTER §5 (R4-14) | SQ-02; SQ-08; SQ-14 |

### HC-10 Where a connector is selected, define its receiving/qualification and unavailable paths; stage the later Domains increment (HI §8; row 10) — only if selected

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-10.1 | Is the connector selected at all for this host and activity? If not, is its absence shown without implying empty work, readiness or permission? | HI V4-HI-62; CA §6 | Statement of selection; the first connected activity needs neither PEC nor Domains |
| HC-10.2 | For PEC: which qualified/released coverage is relied on, and has the consumer adopted it? | DEL-07-01/07-02 SoWs (outside D1); HI V4-HI-61 | 03-04/TBD-007 (OI-022) owner answer; qualified release and receiving adoption |
| HC-10.3 | For Domains (later increment): which admitted sources, query interface, research workflow and approval route? | DEL-08-01/08-02 SoWs (outside D1); HI §8.1 | 03-04/TBD-008, TBD-009 owner answers; no initial-activity gate |

---

## 4. OUT-003 — Completeness checks and recorded comparison

**Candidate examined:** this file (DEL-03-04/GUIDE-v0.1) against the inputs
at `f05c7e4cd` listed in the header. **Evidence standing:** *illustrative*
(definition completeness only). No result below is product, host, delivery,
adoption or joined-witness evidence.

### 4.1 Check results

| Check | What is compared | Result | Notes |
|---|---|---|---|
| CC-1 | Every row of the SoW minimum receiving map has a matrix home | **pass** — 10/10 rows (§2.1–§2.10) | Rows 9 and 10 marked conditional (REQ-001) |
| CC-2 | Every obligation stated in each map row's "required evidence" column has a matrix line | **pass with limits** — see table 4.2 | Row 8 "additive role guidance" and row 10 have homes but no App/shared definition in this undertaking (G-1, G-2) |
| CC-3 | Every HI §10 item has a checklist entry | **pass** — 10/10 (HC-1…HC-10), plus HC-0 preconditions | HC-9, HC-10 conditional |
| CC-4 | Every relay question SQ-01…SQ-27 has at least one matrix home | **pass** — 27/27 (table 4.3) | SQ-04 and SQ-27 are cross-cutting (homes M1.8, HC-0; evidence columns) (G-5) |
| CC-5 | Every receiving-map obligation that needs host evidence has an SQ | **fail (gap)** — row 7's model interface, endpoint/key boundary, local default, local-data constraint and responsiveness have no SQ | G-3 |
| CC-6 | Every TBD-001…TBD-009 is carried with its literal owner and point of need | **pass** — §2.13 | TBD-001/002 now adopted at App/shared level; SoW text still reads open (F-5) |
| CC-7 | Every REQ-008 excluded act maps one-for-one to its owner | **pass** — X-01…X-19 (§2.12) | The registered boundary-owner checker named by VER-007 was **not run** (no tool run in this task) |
| CC-8 | Every consumed Design file is cited in the matrix | **pass** — 16/16 files (C, P, ADAPTER, ACT, AS, RS, WD, WD-EX, EXEC, LOOP, PANEL, HOSTING, SPIKE, CA, RELAY, XT) | SPIKE cited through M9.3 and §2.11 only |
| CC-9 | R4 rulings that change a relied-on statement are applied | **pass** — §5 (R4-1…R4-8, R4-11…R4-16, R4-21) | Section numbers remain v0.3/v0.1; v0.4 re-point needed (F-12) |
| CC-10 | No line claims relay, answer, commitment, delivery, adoption, host behavior, a human act, a selected transport or placement | **pass** (self-review) | Independent review not yet performed (F-9) |
| CC-11 | Conflicts between inputs that affect a guide statement | **3 found** — G-4, G-6, G-7 | Recorded, not resolved here |

### 4.2 Receiving-map evidence obligations → matrix lines

| Map row | Obligations named in the SoW's "required evidence and point of use" | Matrix lines |
|---|---|---|
| 1 Catalog and read meaning | identity/version; purpose; input schema; preconditions/reasons; effects; result/standing; errors; adopted class; generated versus checked/adapter portions before claiming host conformance | M1.1–M1.8 |
| 2 Single route | named route; validation/outcome/error comparison and host evidence; no second agent route | M2.1–M2.5 |
| 3 Basis | workspace identity, generation, model revision, canonical content hash (received as identity + method designation); read-to-action original basis trace; refusal on stale basis; no silent substitution | M3.1–M3.6 |
| 4 Origin, undo and proposal presentation | conversation/workflow origin; available undo; lifecycle and receipt references; stale/refusal; unchanged targets; duplicate-one-effect (received as a host obligation to be evidenced, R-7); unknown outcome | M4.1–M4.7 |
| 5 Human acts and compact records | actual actor/subject/content evidence; recorder identity; visible lapse; run links workflow/version, conversation, settings, requests/outcomes, receipt references, actual acts and model | M5.1–M5.8 |
| 6 Autonomy | visible changeable settings recorded per run; conservative defaults; SWB proposal default with row/multi-row/batch acceptance and widening; declared checkpoints still wait; unresolved classes stay open | M6.1–M6.6 |
| 7 Loop and panel | agreed contribution allocation; native endpoint/key boundary; local-server default and local-data constraint; malformed-call and schema-before-domain validation; responsiveness; host-owned results/views without an agent-private surface | M7.1–M7.8 (host evidence questions missing: G-3) |
| 8 Host methods and roles | identified method and receiving compatibility; missing-tool handling; actual checkpoint act; source-preserving App/host adaptation; tested/refined in App; additive role guidance | M8.1–M8.7 (role supply outside D1: G-1) |
| 9 Optional external catalog access | disabled/unavailable path; enabled same-basis/validation/autonomy/reserved-act semantics; endpoint and candidate evidence before claiming connection; historical no-external-apply policy not a universal ruling | M9.1–M9.8 |
| 10 Selected connectors | PEC pin, standing, coverage/freshness/limits, release, adoption; Domains admitted sources/query/provenance/freshness and research workflow later; independent absent/limited paths | M10.1–M10.3 (no in-undertaking definition: G-2) |

### 4.3 Relay questions → homes

| SQ | Topic | Matrix home(s) | Checklist |
|---|---|---|---|
| SQ-01 | Capture-evidence reference (P1) | M5.3, M5.8, M8.4, M9.8 | HC-5.2 |
| SQ-02 | Governing checkpoint constraint (P1) | M6.4, M7.6, M8.4, M9.5 | HC-6.3, HC-9.6 |
| SQ-03 | Content identities (P1) | M3.2, M4.2, M4.3, M5.5 | HC-3.2, HC-4.2, HC-4.3, HC-5.4 |
| SQ-04 | First activity, check, environment | M1.2, M1.5, M1.8 | HC-0.2, HC-1.2 |
| SQ-05 | Policy for the selected operation | M1.4, M2.2, M5.2, M6.1–M6.3, M6.5, M7.7 | HC-1.4, HC-2.2, HC-5.1, HC-6.1, HC-6.2, HC-6.4 |
| SQ-06 | Direct application on the external channel | M9.4 | HC-9.3 |
| SQ-07 | Basis and staleness | M3.1, M3.3, M3.4 | HC-3.1, HC-3.3, HC-3.4 |
| SQ-08 | Proposal identity and repeated submission | M3.4, M4.2, M4.5, M9.5 | HC-3.4, HC-4.2, HC-4.5, HC-9.6 |
| SQ-09 | Outcome statements and unknown | M1.3, M2.1, M2.3, M4.3, M4.6 | HC-2.3 |
| SQ-10 | Undo and publication | M4.3, M4.4 | HC-4.3, HC-4.4 |
| SQ-11 | Exposure per surface | M1.3, M1.7, M8.3 | HC-1.5 |
| SQ-12 | External seam and derivation | M1.1, M1.6, M1.7, M2.5, M9.3 | HC-1.7, HC-9.2 |
| SQ-13 | Enablement | M9.1, M9.2 | HC-9.1 |
| SQ-14 | Origin and caller identity | M4.1, M9.5 | HC-4.1, HC-9.6 |
| SQ-15 | Locality and sandbox | M9.6 | HC-9.4 |
| SQ-16 | Data boundary (host side only, per R4-1) | M9.7 | HC-9.5 |
| SQ-17 | Receiving App workflows | M8.1–M8.3, M8.5 | HC-8.2, HC-8.3 |
| SQ-18 | Adaptation and library identity | M1.2, M8.1, M8.2, M8.5, M8.7 | HC-8.1, HC-8.2, HC-8.4 |
| SQ-19 | Host run records and supplied guidance | M5.6, M8.6 | HC-5.5, HC-8.5 |
| SQ-20 | Host-side placement (informational) | M7.1, M7.6 | HC-7.6 |
| SQ-21 | Host faithful-record operation | M5.4 | HC-5.3 |
| SQ-22 | Proposal views | M4.7, M7.7 | HC-4.6, HC-7.5 |
| SQ-23 | Display of lapse, supersession, stale-after-acceptance, reversal | M5.5, M7.7 | HC-5.4, HC-7.5 |
| SQ-24 | Where findings are held | M1.5 | HC-1.6 |
| SQ-25 | App capture of acts on host content | M5.3 | HC-5.6 |
| SQ-26 | One new operation for the extension trace | M1.6 | HC-1.7 |
| SQ-27 | Candidates, host evidence, relay of returns | M3.6, M8.7, M9.8; evidence column of every row | HC-0.1, HC-0.3 |

### 4.4 Gaps and conflicts found

| # | Kind | Gap or conflict | Where | Proposed disposition (owner) |
|---|---|---|---|---|
| G-1 | Missing definition (outside D1) | Additive role supply (DEL-02-04) and App act control (DEL-01-04) have no Design file; M8.6 and M5.3 rely on accepted SoW meaning plus HOSTING S-6 and EXEC §5 only | M5.3, M8.6 | None in this undertaking; guide rows stay "outside undertaking (D1)" (owner of D1 scope) |
| G-2 | Missing definition (outside D1) | PEC and Domains receiving (DEL-07-01/02, DEL-08-01/02) not started; row 10 has homes but no definition | M10.1, M10.2 | By design (conditional; first activity needs neither) |
| G-3 | Missing host question | No relay question asks the host about the embedded loop's model interface (DEP-05-01-024), native endpoint/key boundary, local default and no-fallback (LOOP §5, N-OPEN-1…3), malformed-call handling or responsiveness observation — all required by receiving-map row 7 | M2.4, M7.2, M7.3, M7.5; HC-2.4, HC-7.2–HC-7.4 | Add a question (for example a P8 "host loop model connection" group) at RELAY v0.2, or record why these are only observed at DEL-09-07 qualification (DEL-09-06 with DEL-05-01) |
| G-4 | Stale standing after R4 | RELAY SQ-16's App assumption ("XF-36 HELD"; D5 "pending"), CA DI-5/DI-6 and §12 F-6, and XT IN-14/IN-25 still describe D5/D6 as pending. DECISION-2 settles D5 App-side (R4-1) and defers D6 to SQ-02 (R4-2). R4 bumps Wave-1 files to v0.4 and W7/W8 to v0.2 but does not name the W9 files | M9.7, M6.4 | Extend the R4 sweep to CA/RELAY/XT (DEL-09-06, DEL-09-09) |
| G-5 | Map shape | SQ-04 (activity selection) and SQ-27 (candidate identification, host-owned checks, relay form) belong to no single receiving-map row | HC-0; M1.8 | Treat as cross-cutting preconditions (HC-0); no SoW change proposed |
| G-6 | Conflict with SoW wording | Map row 7 says "local-server default and local-data constraint" without distinguishing the host embedded loop (V4-HOST-02, unchanged) from App conversations reading host content (D5: flexible, recorded, not gated) | M7.3, M9.7 | The guide applies both, each to its own path (B-6). C1 may add a SoW wording note; no scope change |
| G-7 | Conflict with SoW wording | Map rows 3–4 use "canonical content hash" and "duplicate-one-effect". R-6 adds subject and change-item content identities with method designations; R-7 makes one effect a host obligation to be evidenced, not a recorded fact | M3.1, M3.2, M4.5 | Guide carries the refined meanings; C1 wording note |

---

## 5. R4 rulings applied over the pinned inputs

| R4 | Changes which pinned statement | Applied at |
|---|---|---|
| R4-1 (D5) | ADAPTER §3.4 and U-X2 (open data boundary; XF-36 HELD); RELAY SQ-16 App assumption; CA DI-5; XT IN-14 | B-6; M5.6; M9.7; HC-9.5; G-4 |
| R4-2 (D6) | EXEC §2 HP-1/HP-2 as candidate hold points; every App-hold reliance | B-7; M6.4; M8.4; M9.5; HC-6.3; §2.13 |
| R4-3 | WD I-4, ACT §4.3, RS L-12, AS §4, LOOP C-4, PANEL W-5e interim "performed + act-lapsed" display | M7.6; M8.4 |
| R4-4 | "Unless DEL-02-03 defines resumption" (WD U-21, ACT §2.3, LOOP, PANEL) | M5.8; M8.4 |
| R4-5 | Acts captured before arrival (LOOP FX-C4; WD-EX R-16) | M5.3; M8.4 |
| R4-6 | "A later A12 supersedes" (ACT §2.5, RS L-0, AS, WD, LOOP C-8, PANEL W-5g) | M5.5 |
| R4-7 | WD §4.3.7 confirmed with MX-3, MX-6, MX-8 | M8.4 |
| R4-8 | WD §4.2.4 *unsupported* reasons | M8.3; HC-8.3 |
| R4-11 | RS element list (including model destination) | M5.6; HC-5.5 |
| R4-12 | HOSTING R9 and §6.1 (elicitation/user-input standing) | M5.3; HC-5.2 |
| R4-13 | ADAPTER U-X1 (A13 locus); App-side configuration as evidence | M9.1; HC-9.1 |
| R4-14 | P §3.3, ACT §4.4, WD §4.2.2 "the external adapter carries" | M4.1; M6.4; M9.5; HC-9.6 |
| R4-15 | P §3.3 author identity | M4.1 |
| R4-16 | C §4.1 reporter of *channel not enabled* | M1.3; M9.2 |
| R4-21 | WD reached-when kind (a) on a harness capability | M8.3 |

R4-9, R4-10, R4-17…R4-20 change fixture labels, subject-class lists or
fixture content that this guide does not restate; they need no guide change.

---

## 6. Findings (reported; scope unchanged)

| # | Where | Finding | Proposed disposition |
|---|---|---|---|
| F-1 | Parent instruction | The instruction speaks of "all 11 v0.x Design files" but names 13 deliverables. At `f05c7e4cd` there are 16 Design files (excluding the generated tree): 11 main contract files (C, P, ADAPTER, ACT, AS, RS, WD, EXEC, LOOP, PANEL, HOSTING), two companions (WD-EX, SPIKE) and three W9 files (CA, RELAY, XT). All 16 are consumed | None; recorded for traceability |
| F-2 | G-3 | Receiving-map row 7 host evidence has no relay question | RELAY v0.2 (DEL-09-06 with DEL-05-01) |
| F-3 | G-4 | W9 files outside the R4 sweep keep D5/D6 "pending" | Extend the sweep |
| F-4 | Dependencies.csv (DEP-03-04-005…020) | No rows to DEL-01-01 (App's Codex receiving the host seam; supplied guidance), DEL-09-06 (relay SQ identifiers, which this guide cites for every host contribution) or DEL-09-09 (external witness, extension trace). Only DEL-03-02 carries a mirror (DEP-03-02-021); the other suppliers' registers carry no DOWNSTREAM row to DEL-03-04 | Register repair at closeout C1 (mirror rows; genuinely new relationships via `project-dag` departure) |
| F-5 | SoW TBD-001, TBD-002; REQ-004 | Still read OI-001/OI-002 as open. DECISION-1 D2/D3 adopt them at App/shared level; the residue is operation-specific (OI-021) and host adoption (DEP-001) | C1 pointer, as for other SoWs |
| F-6 | G-6, G-7 | SoW map wording predates R-6/R-7 and D5 | C1 wording note; no scope change |
| F-7 | D1 | Rows 8 and 10, App act capture and V4-EXM-14 completion depend on deliverables outside this undertaking (DEL-02-02, DEL-02-04, DEL-01-04, DEL-07-*, DEL-08-*) | Record as completeness limits (G-1, G-2; CA F-1) |
| F-8 | C §8 | Every three-surface cell is *unagreed*, so no host can yet claim HC-1.7 | Consistent with OI-003; no action |
| F-9 | SCC-CASE-002; VER-007 | No CASE-002 M-row names DEL-03-04, so no independent receiver comparison of this guide is scheduled; the registered boundary-owner checker named by VER-007 was not run here | Schedule an independent review of GUIDE-v0.1 before v0.2; run the checker in closeout |
| F-10 | R4-2; ADAPTER GC-5; EXEC F-10 | For App-run workflows over the external channel, the acceptance-checkpoint-under-direct-grant case has no enforceable route until SQ-02 is answered | Carried as `UNRESOLVED{D6}`; M6.4 |
| F-11 | Concurrent v0.4 revision | Section numbers here are those of v0.3/v0.1 at `f05c7e4cd`. The v0.4 drafts under R4 may renumber sections | Re-point this guide at v0.2 against the merged v0.4 bytes |
| F-12 | Identifier collision | "TBD-007" means OI-022 (PEC) in this SoW and MCP-versus-CLI in DEL-03-03's SoW | Prefixing rule (§0); C1 may note it |

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-021}` first connected operation, check, autonomy, environment; operation-specific reserved additions (03-04/TBD-006; TBD-001 residue) | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution; host evidence before connected-journey integration/examination and fallback-replacement decision | M1.8, M5.2, M6.5 open; all examples are FX-PIPE-01 fixture subjects |
| `UNRESOLVED{OI-003}` automatic catalog extension (03-04/TBD-003) | Owner with host contract owner | Before claiming extension capability or fixing its acceptance criterion | M1.6 owner-open; HC-1.7 claim barred |
| `UNRESOLVED{OI-013}` per-host loop placement and persistence (03-04/TBD-004) | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | M2.4, M5.6, M7.1, M7.6, M7.8 describe outcomes only |
| `UNRESOLVED{OI-014}` shared contract/component placement (03-04/TBD-005) | App/shared contract owners | Before structural/production contract allocation | No common component or service presumed (M1.7, M7.8) |
| 03-04/TBD-007 (OI-022) PEC first receiving envelope | App consumer owner and PEC owner | Before operational consumer reliance | M10.1 conditional; not designed |
| 03-04/TBD-008 (OI-023) Domains receiving contract and timing | Owner with Domains/SWB/App receiving owners | Before later Domains-enabled design increment | M10.2 conditional; not designed |
| 03-04/TBD-009 (OI-026) Domains provider ownership | Owner with App/Domains/SWB definition owners | Before allocating Domains provider production and committing its integration | M10.2 conditional |
| `UNRESOLVED{D6}` App-side hold points | Owner (DECISION-2), deferred to SQ-02 | Before App-side hold fixtures | M6.4, M8.4, M9.5 claim no App hold |
| Every SQ-01…SQ-27 answer (DEP-001) | SWBPIPE outside implementation owner, through the human relay | As stated per question in RELAY | Every "relay pending" line stays *prepared*; no host behavior assumed |
| G-3 missing host questions (model interface, endpoint/key boundary, local default, malformed calls, responsiveness) | DEL-09-06 with DEL-05-01 | Before host loop integration and DEL-09-07 qualification | M7.2, M7.3, M7.5 have no host-question route |
| 03-03/TBD-007 MCP-versus-CLI and related choices (OC-1…OC-12) | App external-host integration owner with external host owner | Before the App receiving implementation depends on the interface; before DEL-09-09 qualification | Row 9 selects nothing |
| ADAPTER U-X1 A13 capturing surface (per R4-13, set by DEL-04-01) and U-X3 GC-3/GC-5 | DEL-04-01 with the owner and host owner; DEL-02-03 with host owner | Before enablement implementation; before hold fixtures on X | M9.1, M9.5 owner-open |
| ACT U-03 multi-row A4 purpose after partial lapse | DEL-04-01 with the owner | At its point of need (EXEC whole-scope request satisfies every option, R4 "carried") | M5.5 owner-open |
| ACT U-02 consequence vocabulary; ACT U-06 other host defaults | DEL-04-01 with host policy owner; host policy owner | Before class assignment for connected operations | M1.4, M6.1, M6.3 scope slot only |
| DEP-05-01-024 host-loop model interface | Supplier UNKNOWN; App/shared embedded-integration owner receives or agrees | At fixture/conformance use | M7.2 semantic only |
| Register and SoW-text findings F-4, F-5, F-6, F-12 | Register owner / closeout C1 | C1 | None on content |
| Independent review of this guide (F-9) | App manager (review dispatch) | Before GUIDE-v0.2 | Completeness results are self-review only |
| v0.4 re-point (F-11) | This deliverable | After the R4 sweep merges | Section references may need updating |

---

## Verification cases

Designed, **not run**. Passing them later shows guide completeness only; they
never substitute for host conformance, a joined witness or a human act.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-G-01 Checklist coverage | Compare §3 with HI §10 items 1–10 and the ten map rows; trace each to SOW-156/SOW-187 and OBJ-004; inspect each check for supplier, receiver, evidence and point of use; confirm HC-9 and HC-10 are conditional | 10/10 items and rows covered; every check names its receiving definition and evidence; conditional paths are not startup inputs | VER-001 (AC-001) |
| VC-G-02 Catalog/basis/route/proposal fidelity | Compare rows 1–4 (M1.x–M4.x) element by element with C-v0.3 §2–§9 and P-v0.3 §1–§12 and HI §§2–4: same-catalog reads, unavailable reasons, original basis, one route, origin/undo, proposal views, stale/no-retarget/duplicate/unknown, receipts | No meaning weakened or added; no wire field; no automatic-extension or joined-outcome claim; every host-evidence need names an SQ; no host mutation executed | VER-002 (AC-002) |
| VC-G-03 Acts and autonomy | Review rows 5–6 against HI §§5–6, §9 and ACT-v0.3, AS-v0.3, RS-v0.3 with illustrative cases: execution-only success (no act); fabricated act (rejected); a positive faithful record of an evidenced decision with a named recorder; content change and lapse; "accept" versus approval; direct versus proposal settings; a declared A5 checkpoint under a direct grant (AWAITING SQ-02) | Each act distinct; faithful recording allowed with actor ≠ recorder; lapse visible; adopted versus open policy kept apart; illustrative cases claim no act occurred | VER-003 (AC-003) |
| VC-G-04 Receiving path | Walk method → tool → checkpoint → record → loop → panel through rows 7–8 using WD, EXEC, LOOP, PANEL, RS and HI §10, A §§4–5 | Each receiver named; source-qualified identity preserved; local network constraint for the host loop carried; host views host-owned; OI-013/OI-014 placement open; SWB construction external; G-3 recorded | VER-004 (AC-004) |
| VC-G-05 Connectors | Inspect row 10 and HC-10 against HI §8, §8.1, DEP-002/DEP-003 and EXAMINATION V4-EXM-30/32 | PEC and Domains independent and conditional; qualification/adoption and source limits named; later Domains inputs traced without an initial gate; nothing designed | VER-005 (AC-005) |
| VC-G-06 Open inputs and custody | Compare §2.13 literally with the SoW TBD rows and current `Open_Issues.csv`; inspect claimed coordination states: a prepared-but-unrelayed file (RELAY), a received answer without delivery (none yet — case stays illustrative), a checked definition without host adoption (ACT P-01) | Owners and points of need match literally; no state above *prepared*; D2/D3 shown as App/shared adoption only | VER-006 (AC-006) |
| VC-G-07 Boundary owners | Enumerate REQ-008 excluded acts against §2.12 and CLM-001…CLM-006; run the registered boundary-owner checker; inspect NOT_CHECKABLE items and human/external owners by hand | One-for-one mapping; guide integration retained by DEL-03-04 | VER-007 (AC-007) |
| VC-G-08 Completeness result | Re-run §4.1 CC-1…CC-11 against the identified guide candidate and the merged v0.4/v0.2 inputs; record pass, fail, blocked, not run or inconclusive with source revisions | Result bound to named revisions; gaps G-1…G-7 either closed or still visible; no product, delivery or joined-witness claim | VER-008 (AC-008) |
