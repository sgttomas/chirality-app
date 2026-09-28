# External control and catalog-extension trace cases
- Contribution: DEL-09-09/XT-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (V4-EXM-25 external control suite — case definitions and input/limitation account; **not run**), OUT-002 (V4-EXM-24 one-new-operation three-surface trace plan and comparison categories; **not run**), OUT-003 (generated-versus-adapted work account structure and the OI-003 disposition record — recorded, never performed); REQ-001…REQ-009 (definition parts); AC-001…AC-009 through designed VER-001…VER-009
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 082db8fa70bf0ceb8c8bf3c3a7fc4a222994858c66fdc7d9e5f16909f3ed862d; Dependencies.csv sha256 02d738c7ae0cecd809bac16f8e94d67354ac95a874bd3090ef62ed6a790ffbe2 (ACTIVE EXECUTION rows DEP-09-09-007…020); `P/docs/EXAMINATION.md` (sha256 1b156553dec7eb103dbb1166f5c0dbe9c719d26630d2fcace26c28b3ef54ee19) §1–2, V4-EXM-24, V4-EXM-25; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7db2d74619ed47d184f44938bb06f1e2abda0a304a9e11b9230d0960da) §§1–7, §9, §11 (V4-HI-01…04, 10…12, 20…25, 30…33, 40…42, 50…52, 70/71); `P/docs/PRD.md` (sha256 657593ce12a9a6da9f8b6c66579945499d909a8b6272d919d2d14a3db4538573) V4-PAR-05, §4.4–4.5, §4.7, OQ-02, OQ-10, OQ-11; SCC-CASE-002 `Case_Datasheet.md` (sha256 6acdc6c4e484ab7b46ba7d45a347961bc69b3e624bd29ef58a613ec6c66a71a6) rows M2-A, M4-J, M4-X; owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e) D1–D3; R1 (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4), R2 (sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088), R3 (sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf); `reviews/V2.md` MAJOR-1; BRIEFS.md working copy sha256 77a42f8a8c8260285b4142d3a6392a07daead16010b209139efc0d3efc60a21f ("Common brief", "Owner rulings now in force", "Wave 2 — common additions", "W9")
- Consumed inputs (read with `git show`; not the working tree):
  - **Wave-1 v0.3 at `ba0b37123`** (blob-identical to the PR #1039 head `1c36b6d97`; the brief's merge `98b1723b` is absent from this clone): **C** DEL-03-01/C-v0.3 `CATALOG_AND_READ_BASIS.md` sha256 ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26 (§3, §4.1, §5, §6, §8, §10 FX-PIPE-01, evidence-label mapping); **P** DEL-03-02/P-v0.3 sha256 ec0db87f239bc42e2e3e953d660ce3c4ceddf605d7b98cf1393f97a099b699cf (§2, §5–§11, §12); **ACT** DEL-04-01/ACT-POLICY-v0.3 sha256 b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128 (§2, §5.3, §6, §9); **RS** DEL-04-03/RS-v0.3 sha256 925f35ca27bd7d1e71a375883ada9903267408af57312eed1ae02b47776a3528 (R7, R9, R11, §6); **AS** DEL-04-02/AS-v0.3 sha256 7b634137bb8402f3eaedc943dab0c5f1114b9d4433d2b94e13540ac0bf8e0514 (§3); **LOOP** DEL-05-01/LOOP-v0.3 sha256 6b771c8027787193d536fa3507214a8cc579d6ec2f476ee880609c920b6f25c7 (§2.2, §6, §11, §12); **PANEL** DEL-05-02/PANEL-v0.3 sha256 4c47764d3af434c23e63dcc2c10d28f18a4a94546d63d452855c471cfe47bee9 (§3.3, §4, §5); **WD** DEL-02-01/WD-v0.3 sha256 84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb (§4.2.4); **HOSTING** DEL-01-01/HOSTING-BOUNDARY-v0.3 sha256 34c3383402aabe6e9347aa2f111318538c4a2a4ca85adb8fffff7e439fdde94e (§3, §6).
  - **Wave-2 at `e20a3ae8d`:** **ADAPTER** DEL-03-03/ADAPTER-v0.1 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074 (§3–§10, fixture inventory XF-01…XF-39, L-ADAPTER-1…10; PR #885 cited there as evidence only); **EXEC** DEL-02-03/EXEC-v0.1 sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8 (§3 EV-1…EV-11, §7.1).
  - Same run (W9): DEL-09-06/CA-v0.1 `CONNECTED_ACTIVITY_CONTRACT.md` and DEL-09-06/RELAY-v0.1 `RELAY_QUESTIONS_SWBPIPE.md` (SQ-nn identifiers).
  - Pending owner question `DECISIONS_PENDING_2.md` D5, D6 (working tree): **pending**, not ruled.
  - SWBPIPE catalog, endpoint, candidate, receipts or acts: **none received** (DEP-001; DEP-09-09-014). DEL-09-01 (examination infrastructure): accepted SoW meaning only, outside this undertaking (D1).
- Receivers: DEL-03-01 (trace and work evidence via DEP-03-01-030 before any extension claim; CASE-002 M4-X); the owner with the host contract owner (evidence for the OI-003 ruling, DEP-09-09-020); DEL-09-06 (joined activity; shared act cases); DEL-03-03 (which ADAPTER cases the joined suite reuses); DEL-09-01 (protocol needs, when defined); the external SWBPIPE owner through the relay file.

---

## 0. Reading this definition

**What it defines.** Designed, not-run definitions of: (1) the V4-EXM-25
external control suite — the App's Codex inspects, submits a proposal, the
engineer accepts it in SWBPIPE, and the chain is traced to the host receipt,
with stale, duplicate, interruption and unknown cases (§3); (2) the
V4-EXM-24 trace plan for one newly added catalog operation across the human,
embedded and external surfaces, with comparison categories (§4); (3) the
structure of the generated-versus-adapted work account and of the OI-003
disposition record (§5). §2 lists every input and its standing; §8 lists
every input still missing.

**What it does not do.** It executes nothing and establishes no live
connection (SoW purpose). It selects no transport (TBD-007), operation
(`UNRESOLVED{OI-021}`), or extension criterion (`UNRESOLVED{OI-003}`). It
**records** the OI-003 ruling when one is supplied and **never performs** it.
It performs no human act and constructs nothing owned elsewhere (REQ-009).

**Naming.** Element names are semantic labels, not wire names. Acts A1–A14
(R-1); outcomes P §9 / C §4.1; class values C §3.1; dispositions WD §4.3.4.
Fixture material is C §10 FX-PIPE-01 and ADAPTER §10 (L-ADAPTER-n, XF-nn).
Local labels are `L-XT-n` with reasons. `SQ-nn` are relay questions in
DEL-09-06 `RELAY_QUESTIONS_SWBPIPE.md`.

**Two kinds of case.** ADAPTER's XF cases are **focused** App-side receiving
cases against a *simulated endpoint* (test double). The XC and TR cases here
are **joined** cases: they complete only on identified App and SWBPIPE
candidates with actual host behavior and, where named, an actual person's
act. An XC case may reuse an XF case as its test-double rehearsal; the
rehearsal never completes the XC case.

---

## 1. Settled distinctions relied on

| # | Distinction | Citation |
|---|---|---|
| S-1 | The host may expose its catalog to the App's Codex as an MCP server or as a CLI over its live controller; both built from the catalog, same validation, autonomy settings and reserved acts. The host chooses the seam | V4-HI-50; SoW REQ-002 |
| S-2 | External access is off unless the person enables it, and is local to the machine | V4-HI-52 |
| S-3 | Useful parity is operation meaning, truthful standing and recovery, not identical gestures | #d4; SoW AX-001 |
| S-4 | Shared schemas, a transport, common validation, transport de-duplication or component passes do not prove the joined outcome, durable duplicate safety, extension or savings | V4-EXM-24/25; HI §11; SoW REQ-005 |
| S-5 | The original all-actor "without separate work" promise stays identified; its disposition is explicit (retain / narrow / defer); no weaker criterion is adopted silently | V4-PAR-05; V4-HI-03; OQ-10; OI-003 |
| S-6 | Execution, queued proposal, edit acceptance, checking, approval and reliance are distinct; proposal UI says *accept*; acts lapse visibly when bound content changes | V4-HI-25, 30…33; #d3; R-4 |
| S-7 | Reserved to the person (App/shared contracts): A4; A5 where autonomy requires a proposal; A6; A7; A12; A13 (enable; disable INTEGRATION). A10 wherever A5 is (DERIVED) | D2; R-1; R2-3 |
| S-8 | Every result names candidate, configuration and date; outcomes are passed / failed / blocked / not run / inconclusive; changed candidates reopen affected cases; criteria are protected | V4-EXM-01…05; EXAMINATION §1 |

---

## 2. Examination input account (REQ-001; AC-001; VER-001)

Standing uses the C evidence-label mapping and the DEL-09-06 contribution
ladder (CA §7.2). "Defined" means a definition exists; it is **not** an
available input for live examination.

| # | Input | Supplier | Needed for | Standing now |
|---|---|---|---|---|
| IN-01 | App candidate identity: build, stock Codex version actually used, model and server | App construction (later undertaking) | All XC/TR | Not available. Pin 0.158.0 is a definition pin, not qualification (D4) |
| IN-02 | SWBPIPE candidate identity and configuration | SWBPIPE owner (SQ-27) | All XC/TR | Not received |
| IN-03 | Shared candidate/date/configuration protocol; WebKit/Chromium and packaged-smoke evidence protocol | DEL-09-01 (outside D1) | §6 | Not defined in this undertaking |
| IN-04 | Catalog and read-basis contract | DEL-03-01 C-v0.3 | §3, §4 | Defined (*illustrative*) |
| IN-05 | Proposal, validation and outcome contract | DEL-03-02 P-v0.3 | §3, §4 | Defined |
| IN-06 | External receiving contribution and focused fixtures | DEL-03-03 ADAPTER-v0.1 | §3 | Defined; realization family unselected (TBD-007) |
| IN-07 | Adopted operation policy and act distinctions | DEL-04-01 ACT-v0.3 (D2/D3) | XC-09, XC-10; CMP-07 | Defined; host adoption not evidenced (SQ-05) |
| IN-08 | Record semantics | DEL-04-03 RS-v0.3 | XC-09; §6 | Defined |
| IN-09 | Host external seam, native surface derivation and mapping to catalog identity | SWBPIPE owner (SQ-12) | XC-01…XC-12; TR on X | Not received; PR #885 is evidence only |
| IN-10 | Selected first operation, autonomy and environment | Owner via outside SWB session with App/shared owner (OI-021; SQ-04) | Live XC | `UNRESOLVED{OI-021}` |
| IN-11 | The one newly added catalog operation, and who adds it | SWBPIPE owner (SQ-26) | §4 | Not received; fixture L-XT-1 |
| IN-12 | OI-003 disposition | Owner with host contract owner | §5.2 | `UNRESOLVED{OI-003}` |
| IN-13 | Additional essential hosts | Owner (OI-005) | Freezing wider scope | Open; SWBPIPE only |
| IN-14 | Data boundary for content read over X | Owner (pending D5); host rule SQ-16 | XC-01 live enablement | Pending; not ruled |
| IN-15 | Host enablement facility; the person's A13 | SWBPIPE owner (SQ-13); the person (DEP-09-09-015) | XC-01, XC-12 | Not received / not performed |
| IN-16 | Capture-evidence reference for host-captured acts | SWBPIPE owner (SQ-01) | XC-02, XC-09 | Not received |
| IN-17 | Constraint receipt or host-held declaration | SWBPIPE owner (SQ-02) | XC-10 | Not received |
| IN-18 | Proposal identity, de-duplication order and durability; read by identity | SWBPIPE owner (SQ-08) | XC-05, XC-06 | Not received |
| IN-19 | Basis, generation, original-versus-queue-time basis, per-item stale rule | SWBPIPE owner (SQ-07) | XC-03, XC-08 | Not received |
| IN-20 | Outcome statements distinct from transport; errors; unknown | SWBPIPE owner (SQ-09) | XC-06, XC-07 | Not received |
| IN-21 | The engineer's actual acceptance in SWBPIPE (actor ≠ recorder) | The person (DEP-09-09-016) | XC-02 | Not performed |
| IN-22 | Embedded surface for the three-surface trace: host loop and embedded tools; App-side loop receiving | SWBPIPE owner; DEL-05-01 LOOP-v0.3 (receiving) | §4 on E | LOOP defined; host loop not received. **Not registered** in DEL-09-09 Dependencies.csv (F-2) |
| IN-23 | Host human interface and proposal views | SWBPIPE owner (SQ-22) | §4 on H; XC-02 old/new values | Not received |
| IN-24 | Exposure per surface (element 9) | SWBPIPE owner (SQ-11) | §4 CMP-04; XC-11 | Not received; FA-1 fixture assumption |
| IN-25 | Required-tool and hold treatment on X (GC-3, GC-5) | DEL-02-03 with host (ADAPTER U-X3); pending D6 | XC-10 | Proposed, not ruled |
| IN-26 | Undo route | SWBPIPE owner (SQ-10) | CMP-14 | Not received |
| IN-27 | Origin marks and caller identity | SWBPIPE owner (SQ-14) | XC-02; CMP-12 | Not received |
| IN-28 | Locality and sandbox reach | SWBPIPE owner (SQ-15) | XC-01 | Not received |
| IN-29 | Grant display and grant states | DEL-04-02 AS-v0.3; host presentation (SQ-05) | XC-10; CMP-07 | AS defined; not registered in DEL-09-09 Dependencies.csv (F-2) |

---

## 3. V4-EXM-25 external control suite (OUT-001; REQ-002…REQ-004, REQ-007, REQ-008)

### 3.1 The joined chain

The suite joins these elements, each with its own evidence, on one identified
App candidate and one identified SWBPIPE candidate. Each is **linked** to host
evidence, never copied into a replacement store (V4-HI-71).

| # | Element | Evidence owner |
|---|---|---|
| J-1 | Channel state at the time (enabled; A13 reference; locality; data destination shown) | Host facility; App observation (ADAPTER §3) |
| J-2 | The original inspected basis: workspace identity, generation, model revision, canonical content identity and method designation, plus per-row subject content identities | Host read result (C §5) |
| J-3 | The submission: proposal identity, relied-on basis (unchanged from J-2), bound targets, origin, grant in force, requested mode, constraint if any | App dispatch record (ADAPTER §5.1; RS R7) |
| J-4 | The host outcome per item: refused (stale/invalid) with both bases, or queued | Host (P §9) |
| J-5 | The engineer's act in SWBPIPE: A5 (and A10) per item, with actor, bound change-item content identity, capture-evidence reference | Host act facility (IN-16, IN-21) |
| J-6 | Application: receipt, resulting revision, resulting objects, origin mark | Host (P §9 applied association) |
| J-7 | Host views: old and new values shown for the item | Host views (IN-23) |
| J-8 | App record: faithful record of J-5 citing its reference; operation entries; evidence limits | App (RS R7, R9, R11) |

### 3.2 Cases

"Rehearsal" names the ADAPTER XF case that exercises the same meaning on a
test double. "State" is DESIGNED · AWAITING INPUT (inputs named) · HELD
(decision named).

| Case | Fixture steps | Joined observation required | Expected | Rehearsal | State | Serves |
|---|---|---|---|---|---|---|
| **XC-00 Identification** | — | IN-01, IN-02, configuration, date, invented material identity recorded before any result | Every later result cites it; a candidate change reopens affected XC cases | — | AWAITING INPUT (IN-01, IN-02, IN-03) | AC-001, AC-008 / VER-001, VER-008 |
| **XC-01 Access disabled, unavailable, enabled** | L-ADAPTER-1; T1 | (a) never enabled → App makes no host request; (b) App configured, host off → host-reported *channel not enabled*; (c) endpoint stopped / needs authentication → *endpoint-unavailable* with reason; (d) the person performs A13 → *enabled*; grant display unchanged; destination shown | Channel states as ADAPTER §3.2; enablement grants no autonomy (E-5) and no destination (E-6); agent-written configuration never enables | XF-01…XF-07 | AWAITING INPUT (IN-09, IN-15, IN-28); live enablement also IN-14 (D5 pending) | AC-002 / VER-002 |
| **XC-02 Inspect → submit → accept → receipt** | T9 read (B2); T10 PR-2 submitted over X → *queued*; T11 Engineer A accepts item 1 (A5) and rejects item 2 (A10) in SWBPIPE; T12 applied → RC-1 (S-5 created, R-100 changed) | J-1…J-8 all observed; App reports *queued*, never accepted, until J-5 is read; "accepted by Engineer A" only with host-captured A5; "applied" only with RC-1; host views show old/new values; origin mark linked | Chain unbroken from B2 to RC-1; A5 not lapsed by application; A10 distinct; no act from success | XF-11, XF-16, XF-18 | AWAITING INPUT (IN-16, IN-21, IN-23, IN-27; IN-10 for the real operation) | AC-003, AC-007 / VER-003, VER-007 |
| **XC-03 Intervening edit → stale** | T3 read (B1); T5 PR-1; T6 Engineer A edits S-3 (r13); T7 submit over X | Per-item *refused — stale*: failing target S-3; relied B1; current B2; reason; item-left events; the refusal compares against the **original** inspected basis, not a queue-time basis | Stale with both bases; no silent refresh; re-draft is a new proposal (T9) | XF-14, XF-15 | AWAITING INPUT (IN-19) | AC-004 / VER-004 |
| **XC-04 Later selection cannot retarget** | During T10, Engineer A selects S-4 in the host UI | PR-2's bound targets remain R-100, S-2, S-3 in the host's proposal view and at application | No retargeting | XF-17 | AWAITING INPUT (IN-23) | AC-004 / VER-004 |
| **XC-05 Duplicate submission** | T13: PR-2 resubmitted with the same identity; variant L-XT-2: two submissions in quick succession before any acknowledgment. **Reason:** C's T13 covers only a retry after application | Each submission recorded separately; host answers the repeat from recorded state; **one domain effect** shown from domain evidence (model history, receipts), not from transport or session de-duplication | One effect evidenced, or "one effect unevidenced" recorded; never a duplicate-safety pass from transport | XF-19 | AWAITING INPUT (IN-18) | AC-004 / VER-004 |
| **XC-06 Lost acknowledgment and interruption** | T13 ack lost → seek observation by identity → if never received, retry same identity; L-ADAPTER-5 endpoint restart between T12 and T13; App restart variant L-XT-3 (**reason:** ADAPTER covers endpoint restart only) | Actual application or refusal traced to the receipt after interruption **when observable**; retry never refused stale by its own effect; after a non-durable restart the retry is *outcome unknown* and one-effect unevidenced | Original basis → outcome → receipt joined, or explicit unknown; reconnect and queue-time basis never taken as proof | XF-19, XF-21 | AWAITING INPUT (IN-18, IN-20) | AC-004 / VER-004 |
| **XC-07 Unknown outcome** | V-OU1 over X: neither T12 nor T13 observed | *outcome unknown*, observer App, last observed *accepted*; a later observation is reported as its own event and does not back-fill | Unknown preserved; never applied/failed by inference | XF-20 | AWAITING INPUT (IN-20) | AC-004 / VER-004 |
| **XC-08 Accepted, then stale at application** | V-S1: Engineer A edits S-2 after T11 and before T12 (r14′) | "accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)"; A5 not lapsed | As R2-16 | XF-30 | AWAITING INPUT (IN-19, IN-16) | AC-004, AC-007 / VER-004, VER-007 |
| **XC-09 Acts: positive faithful record and false-attribution negatives** | (+) T11 A5 read over X and faithfully recorded (actor Engineer A; recorder App; capture-evidence reference; bound change-item identity; scope; purpose). (−) T10 *queued*; T12 receipt; an A14 answer; model text "the engineer accepted"; an elicitation answer (L-ADAPTER-4); T4 findings. (±) T2 A4 on S-2 carried with no acceptance predecessor; lapsed after T14. Label: the host proposal UI says *accept*, not *approve* | Positive record conforms; every negative establishes no act; independent A4 needs no A5; lapse visible | As ACT §2, RS §6, R-4 | XF-18, XF-31, XF-32, XF-33 | Positive: AWAITING INPUT (IN-16, IN-21); negatives: DESIGNED | AC-007 / VER-007 |
| **XC-10 Same route and policy as embedded/human** | XF-22 (direct without grant at r13 under ⟨set-1⟩); XF-23 (T15 → T16: ⟨set-2⟩ class P-03 scope {FX-W1; {S-4}} per C T15 / V2 MAJOR-1; OP-C9 applied directly); XF-25 (V-CP1 constraint); XF-27 (reserved OP-C6); XF-28 (OP-C11 no policy basis); XF-24 (host channel rule variant) | Each outcome over X equals the embedded/human route's outcome for equivalent input, except authority differences reported as *not permitted* naming the treatment (ADAPTER RP-2) | As ADAPTER RP-3; no conversion into a proposal; reserved entries offered, never withheld | XF-22…XF-29 | AWAITING INPUT (IN-07 host adoption, IN-17, IN-29); XF-28 part HELD (R2-9; OI-021); XF-26 HELD (U-X3; D6 pending) | AC-002, AC-003 / VER-002, VER-003 |
| **XC-11 Reads, checks and unavailability compared** | T3 read over X vs E vs H (XF-11); T4 OP-C3 findings and T4a OP-C12 host check (XF-12); T8 OP-C2 unavailable (XF-08); V-X1 not exposed (XF-09) | Same meaningful content, standing, subject identities, reason and evaluated basis across routes; host-reported *not exposed* relayed | Parity of meaning (S-3); findings never "checked" | XF-08, XF-09, XF-11, XF-12 | AWAITING INPUT (IN-22, IN-23, IN-24) | AC-003 / VER-003 |
| **XC-12 Disable while queued** | L-ADAPTER-6: the person disables access after T10, before T11 | New requests *channel not enabled*; PR-2 stays queued in the host; the engineer can still decide it; App shows last observed *queued*, "channel since disabled" | Nothing withdrawn by disabling | XF-35 | AWAITING INPUT (IN-15) | AC-002 / VER-002 |

### 3.3 Completion rule for the V4-EXM-25 witness (REQ-003; AC-003)

The witness is **complete** only when, on the same identified candidates,
XC-02 is observed live with the engineer's actual acceptance (J-5) and the
host receipt (J-6), and XC-03, XC-05, XC-06 and XC-07 are observed. The
other cases may complete later with their own standing. The following never
complete it: definitions; XF rehearsals on a test double; recorded replay;
Runtime or Piping component passes; a successful tool response standing in
for J-5 or J-6; an honest absence report (SoW REQ-003, REQ-008).

### 3.4 Result record per case (REQ-008)

Each executed result records: case id; candidate ids (XC-00); configuration
(realization family actually used; endpoint); date; evidence label
(*test-double* for rehearsal, *actual host* for joined); outcome (**passed ·
failed · blocked · not run · inconclusive**); observations with links to host
receipts and act records; evidence limits (RS R11); and which inputs were
missing. A failed case leads to diagnosis and repair without weakening its
criterion (V4-EXM-05).

---

## 4. V4-EXM-24 one-new-operation trace plan (OUT-002; REQ-005; AC-005)

### 4.1 The operation traced

The source requires exactly **one newly added** catalog operation, traced on
an identified candidate. Which operation is the SWBPIPE owner's and the
owner's to supply (IN-11, SQ-26). Until then the plan uses:

- **L-XT-1 (fixture addition).** Catalog edition **e1** is FX-PIPE-01's
  edition without OP-C9 *Set support label*; edition **e2** adds OP-C9 v1 as
  C §10.2 describes it. **Reason:** C §10 has a single edition and no
  addition event. OP-C9 is chosen because it is a change operation with a
  precondition ("support exists"), a validation error (E-label-too-long), the
  SWB model-change class (P-03), an undo path (OP-C10), a subject-identity
  dependency (FA-2: a label change lapses an A4 on the row), and a named
  non-exposure variant (V-X1).

### 4.2 Trace stages

| Stage | Content | Owner of the work observed | Evidence |
|---|---|---|---|
| TS-0 Baseline | On e1, each surface reports OP-C9 **missing** (a discovery finding), never *not exposed* or *unavailable* | Host; App (EXEC EV-5) | Compatibility reports per surface (EXEC CR-7) |
| TS-1 Addition | The host adds the entry to the catalog (e2). Every change made anywhere to support it is recorded in the §5 account | SWBPIPE owner | Host source revision(s) or change records (IN-11) |
| TS-2 Discovery | Each surface discovers OP-C9 with identity/version, purpose, schema, availability, effects, result, errors, class, exposure | Host (H, E, X); App (X mapping) | Per-surface discovery records |
| TS-3 Exercise | The same scenario on each surface against the same model revision (§4.4) | Host; App (X); the person (H acts) | Case results |
| TS-4 Compare | Category-by-category comparison (§4.3) | DEL-09-09 | Comparison table |
| TS-5 Account | Generated-versus-adapted work account and disposition record (§5) | DEL-09-09 records; owner rules | §5 |

### 4.3 Comparison categories

Every comparison uses the **same model revision and the same operation
identity/version** on the three surfaces. Result values: **same meaning** ·
**differs** (a defect, with detail) · **differs by authority only** (*not
permitted* naming the governing treatment; the one permitted difference,
ADAPTER RP-2) · **not exposed** (host-reported from element 9) · **not
comparable** (reason, e.g. different basis or version) · **not observed**.

| # | Category | What is compared | Source rule |
|---|---|---|---|
| CMP-01 | Discovery and identity | Entry present after addition, absent before; identity and version | V4-HI-01/02; EXEC EV-5 |
| CMP-02 | Entry elements | All nine C §3 elements reach the surface with the same meaning; open description readable without Chirality software; renderings add or drop nothing | C §2 inv. 2, 4; ADAPTER §4.2 |
| CMP-03 | Input and target identification | Same schema; schema-invalid input rejected before domain validation | C §3; LOOP V-3 |
| CMP-04 | Exposure | Element 9 per surface; *not exposed* host-reported (V-X1) | R2-4; C §8 |
| CMP-05 | Availability and reason | Precondition failure → *unavailable*, same reason identity, statement and evaluated basis on H, E and X | V4-HI-04; C §4.2 |
| CMP-06 | Meaningful reads and standing | Reads of the affected rows before and after; standing marks; currency | V4-HI-10/12; C §6 |
| CMP-07 | Class and treatment | Under ⟨set-1⟩: propose; direct *not permitted*. Under ⟨set-2⟩ (class P-03, scope {FX-W1; {S-4}}): direct applied on S-4; direct on other supports *not permitted* | ACT §5.3, §6; C T15 |
| CMP-08 | Validation error | E-label-too-long → *refused — invalid*, same error identity and text | P §2, §9; C §4.4 |
| CMP-09 | Stale refusal | Label change relying on a basis before an intervening edit to that support → *refused — stale* with both bases | P §5; R2-13 |
| CMP-10 | Non-mutating checks | Host check and examination relevant to the operation (fixture: OP-C12 and OP-C3 on the same basis) give the same results on each surface; if the host offers a preview for the new operation, it is compared too | SoW REQ-005 |
| CMP-11 | Proposal views | Old and new label values, affected object, reason, in the host's own view for a proposal from each surface | V4-HI-24; P §8 |
| CMP-12 | Application and receipt | Receipt, resulting revision, resulting objects, origin mark per channel; direct application records no acceptance | P §9; V4-HI-23 |
| CMP-13 | Recovery | Lost acknowledgment → read by identity → same-identity retry; unknown preserved | P §5, §7; R2-13 |
| CMP-14 | Undo | OP-C10 reverses the new operation's receipt, governed by its policy record (R3-4); "applied, then reversed" | R2-15; R3-4 |
| CMP-15 | Human-act separation | Success of the new operation yields no act; an A4 on S-4 bound before the label change lapses (FA-2); reserved entries are unaffected | V4-HI-25, 32; S-6 |

### 4.4 Case matrix (fixture scenario per category; all DESIGNED unless noted)

| Case | Scenario on each of H, E, X (same revision) | Categories | State |
|---|---|---|---|
| TR-01 | TS-0 then TS-2 discovery on e1 and e2 | CMP-01, 02, 04 | AWAITING INPUT (IN-11, IN-22, IN-24) |
| TR-02 | OP-C9 on a support that does not exist | CMP-05 | AWAITING INPUT (IN-22, IN-23) |
| TR-03 | OP-C9 with a label that is too long; with a schema-invalid argument | CMP-03, 08 | AWAITING INPUT (IN-22, IN-23) |
| TR-04 | Propose OP-C9 on S-4 under ⟨set-1⟩; engineer accepts in the host view; application | CMP-06, 07, 11, 12 | AWAITING INPUT (IN-16, IN-21, IN-23) |
| TR-05 | Direct OP-C9 on S-4 under ⟨set-2⟩ (T15/T16); direct on S-3 under ⟨set-2⟩ | CMP-07, 12 | AWAITING INPUT (IN-07 host adoption, IN-29) |
| TR-06 | Intervening edit to S-4 between read and submission | CMP-09 | AWAITING INPUT (IN-19) |
| TR-07 | OP-C12 and OP-C3 before and after the label change | CMP-10 | AWAITING INPUT (IN-11: which checks the host relates to the operation) |
| TR-08 | Lost acknowledgment after application; retry | CMP-13 | AWAITING INPUT (IN-18, IN-20) |
| TR-09 | Undo of the label change (T17 analogue) | CMP-14, 15 | AWAITING INPUT (IN-26) |
| TR-10 | V-X1: OP-C9 not exposed on X | CMP-04 | AWAITING INPUT (IN-24); relevant to a narrowed criterion |

### 4.5 What the trace cannot establish

A completed trace is evidence for the OI-003 decision. It does not decide it,
and it establishes no maintenance or coordination saving; no saving is
measured or estimated unless actually observed (EXAMINATION §2). Common
schemas or validation alone establish neither operational integration nor
automatic extension (REQ-005).

---

## 5. Generated-versus-adapted work account and extension disposition (OUT-003; REQ-005, REQ-006; AC-005, AC-006)

### 5.1 Work account structure

One row per **surface × element** for the traced operation. Elements follow
the C §8 three-surface map, plus the App-side receiving rows.

| Column | Meaning |
|---|---|
| Surface | H (host human interface) · E (embedded tools / host loop) · X (external interface) · App-X (App receiving side, ADAPTER) |
| Element | Entry discovery · exposure · input schema · availability and reason · effects and resulting objects · result and standing · errors · class element · constraint receipt · read basis · proposal views · native mapping (X) · loop tool offering (E) · App receiving configuration (App-X) |
| Production route before addition | generated · checked · hand-built · unagreed · not observed (C §8 values) |
| Change made for the new operation | none · generated automatically · regenerated by a step · hand change · not observed |
| Other changes required? | yes · no · unknown — the evidence for a retained "without other changes" criterion |
| Contributor | The party who made the change (host owner; App owner; named deliverable) |
| Evidence | Link to the change record, source revision or build; never copied |
| Candidate and date | As XC-00 |
| Limits | What the row does not show |

Rules: every surface and element has a row, including those with "none";
"unknown" is never read as "no"; no effort, time or cost figure is entered
unless actually observed; no savings statement is made (AX-001).

### 5.2 OI-003 disposition record (recorded, never performed)

| Field | Current value |
|---|---|
| Original promise | V4-PAR-05 / V4-HI-03 (preserved original seed): adding an operation makes it available to the person, the embedded agent and the external agent without separate work |
| Current status | `UNRESOLVED{OI-003}`, owner **Owner with host contract owner**, point of need **before claiming extension capability or fixing its acceptance criterion**; PRD OQ-10 adds App/shared-contract and external host design participation |
| Ruling (when supplied) | Option (**retain** · **narrow** to identified generated surfaces · **defer** with identified staging); decision actor; date as evidenced; source record and custody; chosen surfaces or staging; supersession statement; consequences for DEL-03-01 AC-007 |
| Criterion then examined | *Retain*: TR cases show availability on all three surfaces **without other changes** and with the same availability reasons (§5.1 column "Other changes required?" all *no*). *Narrow*: exactly the chosen surfaces, with the supersession recorded and the remaining work listed. *Defer*: the staging and the evidence named by the ruling |
| While unruled | The trace and work account are reported as evidence; **no extension criterion and no pass are established**; no weaker criterion is adopted (SoW REQ-006, AC-006) |

### 5.3 Links

The account links: the TR case results (§4.4); the joined V4-EXM-25 results
that use the same operation boundary (§3), when the traced operation is the
external-control operation; and DEL-03-01's receiving row (DEP-03-01-030).

---

## 6. Evidence protocol and standing (REQ-008; AC-008)

- **Labels** follow the C mapping: *illustrative* · *test-double* · *actual
  host* · AWAITING INPUT / HELD / NOT-OBSERVED · LIMITED.
- **Provenance** is kept distinct: test definition; recorded replay
  (V4-EXM-02); static source inspection; live observation; the person's actual
  act; the host receipt. They may share one evidence set; each keeps its own
  identity and standing (SoW OUT section note).
- **Interface evidence** follows the shared WebKit/Chromium and targeted
  packaged-smoke protocol (V4-EXM-04) through DEL-09-01. DEL-09-01 is outside
  this undertaking (IN-03); until it exists, interface observations carry the
  limit "protocol not yet defined". Browser evidence never replaces a required
  native observation.
- **Rechecks.** A changed App or host candidate reopens the affected XC and TR
  cases (V4-EXM-03).
- **Host receipts** are linked, never copied into a replacement truth store.

---

## 7. Owner and act boundary (REQ-009; AC-009)

| Excluded act or production (REQ-009) | Owner | This contribution's part |
|---|---|---|
| Catalog/read-basis contract construction | App DEL-03-01 | Consumed (IN-04) |
| Proposal/outcome contract construction | App DEL-03-02 | Consumed (IN-05) |
| External receiving implementation | App DEL-03-03 | XF cases reused as rehearsals (IN-06) |
| Adopted-policy contract construction | App DEL-04-01 | Consumed (IN-07) |
| Record implementation | App DEL-04-03 | Consumed (IN-08) |
| Reusable examination harness | App DEL-09-01 (outside D1) | Protocol need recorded (IN-03) |
| Host catalog/domain mutation, validation/application, endpoint, loop/panel/views, receipts, act facility | External SWBPIPE owner (CLM-003) | Relay questions only |
| Enabling access (A13); the engineer's actual acceptance (A5) | The person | Observed and faithfully recorded, never performed |
| Engineering approval, certification, professional reliance | The accountable professional | Not required by V4-EXM-25; never inferred |
| Unresolved operation policy (OI-021 additions) | The owner with App/SWB contract owners | `UNRESOLVED{OI-021}` |
| Extension disposition | The owner with the host contract owner | Recorded in §5.2; never performed |
| Cross-session relay; handoff and dependency coordination | The human; the App manager | Through DEL-09-06 relay file |

---

## 8. Inputs still missing (consolidated)

For the V4-EXM-25 suite: IN-01, IN-02, IN-03, IN-09, IN-10, IN-14 (pending
D5), IN-15, IN-16, IN-17, IN-18, IN-19, IN-20, IN-21, IN-23, IN-25 (pending
D6), IN-27, IN-28, and host adoption under IN-07.

For the V4-EXM-24 trace: IN-01, IN-02, IN-03, IN-11, IN-22, IN-23, IN-24,
IN-26, plus IN-16/IN-21 for the acceptance step (TR-04) and IN-18/IN-19/IN-20
for TR-06 and TR-08.

For the OI-003 disposition: IN-12 (the ruling), after the trace evidence.

For freezing any wider examination scope: IN-13 (OI-005).

No case is AWAITING only on an App definition; every AWAITING case needs at
least one external input or an App construction output from a later
undertaking.

---

## 9. Findings (reported; scope and Wave-1/W7/W8 text unchanged)

| # | Where | Finding | Proposed disposition |
|---|---|---|---|
| F-1 | SoW TBD-002; DEP-09-09-010 | Still call OI-001/OI-002 open; DECISION-1 D2/D3 now rule them for App/shared contracts | C1 pointer |
| F-2 | Dependencies.csv | The three-surface trace (REQ-005) needs the **embedded** surface: DEL-05-01 loop receiving (and DEL-05-02 for host views) — no rows exist. Also missing: DEL-04-02 (grant states, IN-29), DEL-02-03 (required-tool outcome and holds on X, IN-25), DEL-09-06 (shared activity and relay file) | Register repair at C1; new relationships via `project-dag` departure |
| F-3 | D1 scope; REQ-008; DEP-09-09-012 | DEL-09-01 (examination infrastructure and protocol) is outside this undertaking; REQ-008's protocol has no supplier yet | Record at C1; §6 carries the limit |
| F-4 | ADAPTER-v0.1 §11 "Provide to DEL-09-09" | ADAPTER lists no rehearsal for XC-05's two-submissions-before-acknowledgment variant or an App restart (XC-06 L-XT-3) | DEL-03-03 may add XF cases; otherwise the local labels stand |
| F-5 | C-v0.3 §10 | No catalog-edition addition event exists, so the extension trace needs L-XT-1 | DEL-03-01 may add an edition-addition variant to FX-PIPE-01 |
| F-6 | SoW REQ-004 ("submitting the same proposal twice has one domain effect") | Consistent with R-7 only if read as a host obligation to be evidenced; XC-05 records "one effect unevidenced" when not observed | No change; reading stated here |
| F-7 | ACT FX-20, AS F2, RS E7, PANEL PC-22, WD-EX R-5a (V2 MAJOR-1) | T15 scope diverges from C; this file uses C T15 (P-03; {FX-W1; {S-4}}) | Consumers re-point in Wave 2 |
| F-8 | EXAMINATION V4-EXM-25 wording "Compare meaningful reads, non-mutating checks, validation and outcomes with the embedded/human routes" | This comparison overlaps V4-EXM-24's categories; XC-10/XC-11 reuse CMP categories to avoid two vocabularies | None; noted for DEL-09-07 alignment |

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-003}` retain / narrow / defer | Owner with host contract owner | Before claiming extension capability or fixing its criterion | §5.2 open; no extension pass or savings |
| `UNRESOLVED{OI-021}` operation, autonomy, environment | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and live examination | All cases on FX-PIPE-01; OP-C11 cases HELD |
| OI-005 additional essential hosts | Owner | Before freezing wider examination scope | SWBPIPE only |
| TBD-007 MCP versus CLI and realization family | App external-host integration owner with external host owner | Before App receiving implementation and qualification | XC cases run per family actually selected |
| DEP-001 host contributions IN-02, IN-09, IN-11, IN-15…IN-20, IN-23, IN-24, IN-26…IN-28 | SWBPIPE owner via the human (SQ-nn) | Before corresponding examination | AWAITING INPUT |
| Actual acts: A13 enablement; the engineer's A5 (DEP-09-09-015/016) | The person | At live execution | XC-01 (d), XC-02 positive parts not observable |
| D5 data boundary (pending) | Owner | Before enabling a live candidate | XC-01 live enablement blocked |
| D6 / ADAPTER U-X3 holds on X (pending) | Owner; DEL-02-03 with host owner | Before XC-10 constraint parts | XF-26 part HELD |
| DEL-09-01 protocol (outside D1) | DEL-09-01 owner | Before candidate-bound interface evidence | §6 limit |
| Host adoption of D2/D3 and treatments | SWBPIPE owner | Before any enforcement claim (XC-10) | Receiving meaning only |

## Verification cases

Designed, **not run**. Passing them later shows definition completeness; the
witness and trace themselves are §3 and §4.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-T-01 Input account | Check §2 and §8 against the SoW, DEP-09-09-007…020, OI-001/002 (as ruled), OI-003/005/021 and DEP-001 | Every input has supplier, need and standing; defined contracts not treated as available inputs; owners and points of need kept | VER-001 (AC-001) |
| VC-T-02 Access cases | Check XC-01 and XC-12 against V4-HI-50…52 and ADAPTER §3 | Disabled/unavailable explicit; enablement by the person; same route and policy after enablement; host seam not chosen here | VER-002 (AC-002) |
| VC-T-03 Joined chain | Check §3.1, XC-02 and §3.3 against V4-EXM-25 and V4-HI-11, 20…25 | J-1…J-8 all required; engineer's actual act and receipt required; tool success never substitutes | VER-003 (AC-003) |
| VC-T-04 Adverse cases | Check XC-03…XC-08 against REQ-004 | Stale with reason and both bases; no retarget; one effect only from domain evidence; unknown preserved; transport never proof | VER-004 (AC-004) |
| VC-T-05 Trace plan | Check §4 against REQ-005 and V4-EXM-24 | Exactly one new operation; all REQ-005 categories present (CMP-01…15); same revision and operation; gaps and non-comparables kept | VER-005 (AC-005) |
| VC-T-06 Disposition | Check §5.2 against OI-003, V4-PAR-05 and REQ-006 | Original promise preserved; ruling recorded not performed; criterion per option; no pass or savings while unruled | VER-006 (AC-006) |
| VC-T-07 Acts | Check XC-09 against #d3, V4-HI-25/30…33, ACT and RS | Positive faithful record with actor ≠ recorder; negatives; accept label; lapse; no acceptance-before-checking dependency; no new reserved list | VER-007 (AC-007) |
| VC-T-08 Evidence standing | Check §3.4 and §6 against EXAMINATION §1–2 | Candidate/configuration/date; outcome values; replay/source/live/native/browser kept apart; receipts linked; rechecks on change | VER-008 (AC-008) |
| VC-T-09 Boundary | Check §7 one-for-one against REQ-009 and CLM-001…004 | Every excluded act has its owner; unresolved decisions kept with their owners; human-relayed handoffs never treated as adoption | VER-009 (AC-009) |
