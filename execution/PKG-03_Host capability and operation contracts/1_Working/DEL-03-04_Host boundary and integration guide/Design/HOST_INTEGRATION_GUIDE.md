# Host boundary and integration guide
- Contribution: DEL-03-04/GUIDE-v0.2. It supersedes GUIDE-v0.1 (sha256 fc96d285a3512065ede29394fe4ef4c5eafc6ccbd08213396826a0bab517afb8, pinned to inputs at `f05c7e4cd`). Refreshed **in place** under R6 and R7 (no version bump); R6 and R7 changes are recorded under R6 and R7 IDs in "Changes from v0.1".
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (new-host integration checklist, §3), OUT-002 (App/shared versus host responsibility/interface matrix, §2), OUT-003 (guide completeness checks and recorded comparison, §4); REQ-001…REQ-008; AC-001…AC-008 through designed VER-001…VER-008
- Basis:
  - Branch base 6e18505e3 (accepted basis); **inputs pinned at the R7 working state (post-2f42fba02)**: the working-tree bytes after the R7 in-place repair of candidate `2f42fba02` (R7_RESOLUTIONS.md R7-4 m-1). The first v0.2 text was pinned at `d3cebd1cc`; the R6 refresh at `375c3970c`.
  - ScopeOfWork.md sha256 203c09288850d33ec3490d00da48bd6bbbc91ae395141c1374c4c6b04ad9a436 (10-row minimum receiving map, CLM-001…CLM-006, REQ-001…REQ-008, AC-001…AC-008, VER-001…VER-008, TBD-001…TBD-009); Dependencies.csv sha256 b41eacd01cdef10e455017cda7afdfae85b2a2a2e989fad481d697f4e862ac17 (DEP-03-04-001…020); `_REFERENCES.md`. All three unchanged since v0.1.
  - `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7db2d74619ed47d184f44938bb06f1e2abda0a304a9e11b9230d0960da) §1–§9, **§10 (checklist), §11 (SWBPIPE receiving limits)**.
  - Run `APP-V4-FIRST-INCREMENT-20260928` at `375c3970c`: `OWNER_DECISIONS.md` (sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c) DECISION-1 (D1–D4), DECISION-2 (D5, D6); `R1_RESOLUTIONS.md` (2f9c7e72…7ec4), `R2_RESOLUTIONS.md` (77cfb845…d088), `R3_RESOLUTIONS.md` (202d52c7…afbf), `R4_RESOLUTIONS.md` (sha256 50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24), **`R5_RESOLUTIONS.md` (sha256 254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1)**; `reviews/V3-B.md` (sha256 5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3; MAJOR-2 and m-6, m-12, m-13 address this file); **`R6_RESOLUTIONS.md` (sha256 8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841; R6-1, R6-3, R6-5)**; `reviews/V4-A.md` (sha256 121deafc40c4baf0dec71f96eb449083b0d93456c2bd448f89a279951ca2eab1; m-14); `reviews/V4-B.md` (sha256 1569cd15b490a07c1fda44114fd6d017f794c16dfe533c65a27d04aad02c2cfc; first independent review of GUIDE-v0.2: m-7, m-9); **R7 inputs (working tree, uncommitted at repair):** `R7_RESOLUTIONS.md` (sha256 1f6ab3b2355e164f803657ceae08841af92d21a821feede3800a6df861b2a1ea; R7-2, R7-3, R7-4 m-1, m-6) and `reviews/V5.md` (sha256 0a4010e82363ac7d4ae6e61ad70125b3e9b8d5dd5937fd0f8c607d7b9e491a87; MAJOR-2, MAJOR-3, m-1, m-6).
- Consumed inputs (re-pinned under R7-4 m-1: every sha256 below is computed from the working-tree bytes at the R7 working state (post-2f42fba02), after every other Design file's R7 edits and before this guide's re-pin; GUIDE cannot pin itself. At R6 they were read with `git show 375c3970c:<path>`). Short names are used throughout:

  | Short | Contribution / version | File | sha256 at the R7 working state (post-2f42fba02) |
  |---|---|---|---|
  | **C** | DEL-03-01/C-v0.5 | `CATALOG_AND_READ_BASIS.md` | 72ac4f0f853213f9778d69c4b3eb84d6b19d1bab80a147d98b7bc5068bb0eacf |
  | **P** | DEL-03-02/P-v0.5 | `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | 6ab94fd10166cf78cda014a2f28ebf4726ce9f82a1c2f180044093b4bbb137e0 |
  | **ADAPTER** | DEL-03-03/ADAPTER-v0.3 | `ADAPTER_ENABLEMENT_AND_RECEIVING.md` | 8ef2126df2b9afff0a70b36e5b4eed8492eaae0baf6563ce422d3b9d05170f5a |
  | **ACT** | DEL-04-01/ACT-POLICY-v0.5 | `ACT_AND_POLICY_CONTRACT.md` | 0057593adfde52044b70ccee1a85892754c2c9a62cf452214e94d810c6c43bd9 |
  | **AS** | DEL-04-02/AS-v0.5 | `AUTONOMY_AND_STANDING_EXCHANGE.md` | df0e31ea7d33a3224df0b5d292d35675a55e8e325898cb28b64a1f709f7d72f0 |
  | **RS** | DEL-04-03/RS-v0.5 | `RECORD_SEMANTICS.md` | 2939eb092839a5d6984c984a2aedcb6308f1776276314a79fa1e8edc67c36398 |
  | **WD** | DEL-02-01/WD-v0.5 | `WORKFLOW_DECLARATION.md` | e55d69cbd25922efa5c25f3349c60dbdaaa7cb3e30ef14c9482fddeb18d76c66 |
  | **WD-EX** | DEL-02-01/WD-EX-v0.5 | `EXAMPLES.md` | 67e2d8ed187ad7f2134592f4f9ec744d9af33c49882d772648d42c340f531d42 |
  | **EXEC** | DEL-02-03/EXEC-v0.3 | `EXECUTION_COMPATIBILITY.md` | 03b2fd48e14dd21ee6f29bc8e5e19221a771f788aa6c1482810b8bc0671d61e2 |
  | **LOOP** | DEL-05-01/LOOP-v0.5 | `LOOP_RECEIVING_CONTRACT.md` | 0ec980b53c4dd473b365f7e8407593a218023ad2277da7680694c852808bd737 |
  | **PANEL** | DEL-05-02/PANEL-v0.5 | `PANEL_RECEIVING_CONTRACT.md` | ac47abf0974d5d68386ca713f09fc1478b205545754e8c93c74993977173ebb4 |
  | **HOSTING** | DEL-01-01/HOSTING-BOUNDARY-v0.5 | `HOSTING_BOUNDARY.md` | f1a23022df76fe04bfc5ad2220b57d2cdebc101f8d791b4edb163aea6109e11b |
  | **SPIKE** | DEL-01-01/PIN-SPIKE-v0.1 | `PIN_SPIKE_0.158.0.md` | 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115 |
  | **CA** | DEL-09-06/CA-v0.3 | `CONNECTED_ACTIVITY_CONTRACT.md` | 67dde29553325271cc3e3a08591177e6628a659966b13b4bbd93920cdf7d0aa5 (fourth byte state of CA-v0.3, R7 in place; earlier: `3bf6653c…` at `d3cebd1cc`, `28a5cb80…` at `816c917f0`/`c7f5513db`, `1db06a29…` at `375c3970c`/`2f42fba02`) |
  | **RELAY** | DEL-09-06/RELAY-v0.3 (32 SQs, with sub-questions) | `RELAY_QUESTIONS_SWBPIPE.md` | a8cae06fd4b208087614e9c4cc7e2b91e36f3b98cd11e6f4093fd946d1177f2b (fifth byte state of RELAY-v0.3, R7 in place; earlier: `82dcaca5…` at `d3cebd1cc`, `89b6b9c9…` at `816c917f0`/`c7f5513db`, `f815adbf…` at `375c3970c`, `4db4906d…` at `2f42fba02`, as recorded in RELAY's change rows) |
  | **XT** | DEL-09-09/XT-v0.3 | `EXTERNAL_TRACE_CASES.md` | 992906e6e8e16fdfae68e02938ba9c440192f86318bb70b487270af52529dbfa |

  **Hold support** is taken from EXEC-v0.3 §3.5–§3.6 (the value-set owner, R5-1), which governs where another file differs; at the R7 working state EXEC §3.6 classifies **by held actions** (R6-1), WD §4.3.1 declares the **held actions** element that feeds it, and both derive the held actions of an A5 or kind (a) checkpoint whose element is absent (R7-3). sha256 comparison against `2f42fba02`: SPIKE, HOSTING, P, LOOP and PANEL unchanged; C, ADAPTER, ACT, AS, RS, WD, WD-EX, EXEC, CA, RELAY and XT changed by the R7 in-place repair (each records its R7 rows). Against `375c3970c` WD and RELAY also changed at `2f42fba02`. DEL-02-02, DEL-02-04, DEL-01-04, DEL-07-01, DEL-07-02, DEL-08-01 and DEL-08-02 are referenced by accepted SoW meaning only; they are outside this undertaking (D1) and have no Design file. SWBPIPE answers, commitments or contributions: **none received** (DEP-001).
- Receivers: the application builder of any new host (SoW Purpose; HI §10), for SWBPIPE only through the human relay; the App/shared host-contract integration owner (CLM-001); each supplying deliverable above, to confirm its matrix row at the next comparison (DEP-03-04-005…019); DEL-09-06 (RELAY ledger; joined-witness step map); DEL-09-09 (external-access and extension rows); closeout C1 (register and SoW-text findings, §6). SCC-CASE-002 names no M-row for DEL-03-04; V3-B reviewed GUIDE-v0.1 and V4-B reviewed GUIDE-v0.2 (first v0.2 independent read: fit as the integrated index, defects m-7 and m-9 only).

---

## Changes from v0.1

| Source | Change |
|---|---|
| Coordinator instruction; R5-9 ("GUIDE's matrix: GUIDE v0.2") | Every matrix line, checklist check and completeness row re-derived against the `d3cebd1cc` set: current versions (C/P/ACT/AS/RS/WD/WD-EX/LOOP/PANEL/HOSTING v0.5; EXEC/ADAPTER/CA/RELAY/XT v0.3) and current section numbers (e.g. ACT §2.6, §4.6; RS §4.1, R14; WD §4.3.8; LOOP §2.4.4; HOSTING §6.7, §6.8, §8.3; ADAPTER §3.4 "Model destination", §12; WD-EX E8) |
| V3-B MAJOR-2; RELAY-v0.3 P8 | "No relay question exists (G-3)" removed: M2.4, M7.2, M7.3, M7.5, HC-2.4, HC-7.2…HC-7.4 now cite **SQ-29…SQ-32**. G-3 closed |
| V3-B MAJOR-2; RELAY SQ-28 | A13 enablement facility and its capture-evidence reference cited as **SQ-28** (M9.1, HC-9.1); SQ-13 kept for enablement *behavior* only |
| V3-B MAJOR-2; ADAPTER-v0.3 UNRESOLVED | Retired ADAPTER U-X3 replaced by `UNRESOLVED{D6}` (EXEC U-E1) and **EXEC U-E23** (App-only checkpoints). ADAPTER U-X1 recorded as closed by ACT-v0.5 §2.6 (PROPOSED under R4-13) |
| V3-B m-6 | RS FA-1…FA-9 → **OF-1…OF-9**; fixture assumptions cited as **FXA-n**; LOOP N-n → **NW-1…NW-7** |
| RELAY-v0.3 sub-questions (R5-10 coverage) | New citations: SQ-03 (e), SQ-05 (g)(h)(i), SQ-07 (g)(h), SQ-18 (e), SQ-19 (d); M3.5 (C U-C10), M3.3 (C U-C4), M1.2 (C U-C6), M4.2/M6.2 (P U-P6, AS U-04), M5.5 (RS U-12), M8.6 (WD U-09), M6.3 (ACT U-06) now have host questions. WD U-10 recorded as "Not included" (D1) |
| R5-1 | New §2.14 hold-support map with the four ruled values and EXEC §3.6 HS-1…HS-5; M6.4, M7.6, M8.3, M8.4, M9.5, HC-6.3, HC-8.3 use them. "Held after observation" and other retired values are not used |
| R5-2 | Carriage assurance: only **host-held** satisfies R2-12; a host loop's own evaluation is host-held; App-assured is not available in this increment; a merely received constraint keeps its source's assurance (M4.1, M6.4, M9.5) |
| R5-4 | D5 attribution split: "may flow, no gate" SETTLED by DECISION-2; "record per turn and show" INTEGRATION (DECISION-2 reading) (B-6, M5.6, M9.7, HC-9.5) |
| R5-10 | D6 scope: SQ-02 decides only **host-operation** checkpoints; App-only checkpoints stay *not enforceable* whatever SWBPIPE answers (owner follow-up EXEC U-E23) (B-7, M8.4, §2.13, G-8) |
| R5-3, R5-5, R5-6, R5-7 | Grant-setting subject always declared (M8.4); undo re-holds whatever it lapses, never an A5 arrival (M4.4); person's own A1/A2 are R7 operations (M5.1); V-GR1 variant (C §10.4) cited for grant-after-arrival (M8.4) |
| V3-B MAJOR-2 (stale CC results) | §4 rerun: CC-4 32/32 SQs; CC-5 pass; CC-8 16 inputs (17-file set with this guide, V3-B m-12); CC-10 records V3-B as the first independent check (m-13) |
| Gaps | G-3, G-4 closed; G-8 (App-only checkpoints, owner follow-up) and G-9 (ADAPTER §12 mapping header labelled RELAY-v0.2) added; F-2, F-3 closed |
| **R6-1** (V4-A MAJOR-1/2, m-14) — in place | §0, §2.14, B-7, M8.1, M8.4, §2.13, HC-6.3, HC-8.1, G-8, F-10 classify hold support **by held actions** (EXEC-v0.3 §3.6 order HS-1, HS-2, HS-5, HS-4, HS-3; WD-v0.5 §4.3.1 *held actions* element, §4.3.8). §2.14 adds the fixture classification: E1, E1c and E1d via X **unsupported**; E1d `CP-grant` via X **not established** (HS-3; C V-GR1 per R6-2); SQ-02 can move only checkpoints whose every held action is a host operation |
| **R6-3** (V4-A m-4) — in place | §0 and §2.14 state what "held" means per value: host loop → the run stops at its next action; host route → the host refuses the held host operations, other actions are *action during hold*; not established / not enforceable → nothing is stopped, actions are *action during hold* |
| **R6-4** — in place | LOOP-local labels HS-0…HS-4 cited as **LH-0…LH-4** (M2.4, M7.6, HC-2.4) |
| **R6-5** (V4-B m-7, m-9) — in place | Every pinned input hash updated to the bytes at `375c3970c` (superseded by R7-4 m-1); CA and RELAY rows record their three in-place byte states under v0.3. CC-1…CC-11 rerun; CC-11 conflict list refreshed (V4-B MAJOR-1 V-GR1 conflict resolved by R6-2; G-9 closed — ADAPTER §12 now RELAY-v0.3; residual RELAY "LOOP HS-0" labels and WD I-4 wording recorded). F-11 closed: CA-H now reads "on E; in App runs only as hold support allows". F-9, CC-10 and UNRESOLVED record V4-B as v0.2's first independent review |
| **R7-3** (V5 MAJOR-3; INTEGRATION, option (a)) — in place, echo | §2.14 HS-5 row: the conservative default applies only to a kind (b)/(c) checkpoint with no held-actions element or whose declared held actions do not show host operations only; an A5 or kind (a) checkpoint with no element takes its derived held actions (governed operation(s); held call) and is valued by them (WD §4.3.1; EXEC §3.6). Fixture table adds "L-WDEX-17 with its held-actions element absent": HS-3 → *not established* today; workflow result by EXEC §3.5 precedence with the run's other checkpoints — none, so *not established* today. Header hold-support note updated |
| **R7-4 m-6** (V5 m-6) — in place, echo | §2.13 D6 follow-up row point of need: "any App-side workflow with a kind (b)/(c) run halt" → "any workflow with a checkpoint with any App-side held action (including an App-content checkpoint)", as EXEC U-E23 |
| **R7-2** (V5 MAJOR-2) — in place, echo | New RELAY SQ-02 (f) given homes: M8.4 host contribution, HC-6.3 and the §4.3 SQ-02 row; CC-4 counts it. No value changes |
| **R7-4 m-1** (V5 m-1) — in place, last | Every pinned input re-pinned to the **R7 working state (post-2f42fba02)**: sha256 computed from the working-tree bytes after every other Design file's R7 edits (GUIDE cannot pin itself). Unchanged against `2f42fba02`: SPIKE, HOSTING, P, LOOP, PANEL; changed by R7: C, ADAPTER, ACT, AS, RS, WD, WD-EX, EXEC, CA, RELAY, XT. CA and RELAY rows list their byte-state histories. R7 inputs (R7_RESOLUTIONS.md, reviews/V5.md) added to Basis. §4 rerun at the R7 in-place state: CC-4 includes SQ-02 (f); CC-9 includes R7; **CC-11 refreshed — G-10 and G-11 closed**, 2 remain (G-6, G-7); §4.4 G-10/G-11 and F-14 marked closed; F-1, F-9, F-15 updated; §5 R7 rows added |
| **R7 integrator close** — in place | After the repair, the integrator qualified PANEL §3.2 (model-supplied, per R6-5) and ACT FX-39 (re-hold per R6-3), and replaced RELAY's "uncommitted at repair" placeholders. The PANEL, ACT and RELAY pins were re-pinned to those bytes. No value changes |

---

## 0. How to read this guide

**What it is.** The integrated receiving guide for adding a host. For every
obligation in the SoW's minimum receiving map it names: the App/shared
contribution that defines the obligation (file, version, section); what the
host must contribute, cited by the relay question that asks for it (`SQ-nn`,
with sub-question letters, from RELAY-v0.3); who decides each open choice; and
the obligation's current standing. It then restates HI §10's checklist as
checks a host answers before claiming each obligation, and records a
completeness check over both.

**What it is not.** It recreates no contributing contract; each meaning stays
in the file cited. It selects no wire field, type, transport, hash or
canonicalization algorithm, persistence, process placement or shared
component placement (OI-013, OI-014; 03-01/TBD-003; 03-02/TBD-002;
03-03/TBD-007). It assigns no SWBPIPE construction: the checklist states what
*any* host answers before a claim, and SWBPIPE items appear only as
relay-question references. It designs no PEC or Domains path (row 10 is
conditional). It performs, records or implies no human act. It runs nothing.

**Standing vocabulary (this guide).**

| Standing | Meaning | Can support |
|---|---|---|
| **defined draft** | An App/shared definition exists at the R7 working state (post-2f42fba02) (evidence label *illustrative*, C §10 mapping) | Completeness of the definition only |
| **relay pending** | A host contribution is needed; the question exists in RELAY-v0.3 (ladder standing *prepared*, CA §7.2); relay, answer, commitment, delivery, adoption and examination are **not observed** | Nothing about the host |
| **owner-open** | An open choice with a named owner and point of need (OI-nnn, TBD-nnn, U-nn, D6) | Nothing; recorded, never made here |
| **host-owned** | Construction, facility or evidence that belongs to the host owner (CLM-001; HI §1) | Nothing until an identified host candidate supplies it |
| *outside undertaking (D1)* | Qualifier: the App/shared definer is a deliverable this undertaking does not start | Accepted SoW meaning only |

**Hold-support vocabulary (R5-1; owner EXEC §3.6).** Each checkpoint on each
acting surface takes exactly one of: **enforced by the host loop** (check
passes; host evidence DEP-001) · **enforced on the host route** (check
passes; host-held constraint evidenced by the SQ-02 answer and a candidate) ·
**not established** (check *not established*; never a pass, never
"unsupported") · **not enforceable** (workflow *unsupported*, "checkpoint hold
not enforceable on this surface", R4-8). An invalid or not-established
declaration takes no value (EXEC HS-1). No other value is used.
The value is decided by the checkpoint's **held actions** — what the run must
not do until the act (WD §4.3.1) — not by how it arrives (R6-1). What "held"
means per value (R6-3): *enforced by the host loop* — the run stops at its
next action; *enforced on the host route* — the host refuses the held host
operations, and any other action is recorded as *action during hold*; *not
established* / *not enforceable* — nothing is stopped, and actions are
recorded as *action during hold*.

**Identifier notes.** Acts A1–A14 (R-1); class values C §3.1's five; outcomes
P §9 and C §4.1; dispositions WD §4.3.4's six. Two different "TBD-007" exist:
**03-04/TBD-007** (this SoW: OI-022 PEC) and **03-03/TBD-007** (DEL-03-03:
MCP-versus-CLI, ADAPTER §9). Matrix lines are `M<row>.<n>`; checks
`HC-<item>.<n>`; completeness checks `CC-n`; gaps `G-n`.

---

## 1. Settled boundary the matrix preserves (CLM-001…CLM-006)

| # | Settled or adopted boundary | Source |
|---|---|---|
| B-1 | The host owns domain objects and truth, its catalog implementation, the one validation/application route, receipts, origin and undo, host UI, and offering, capturing, recording and presenting human acts. The person performs every decision act; the recorder is separately attributable | CLM-001; HI §1, §4–§6; P §1 |
| B-2 | App/shared deliverables own semantic definitions and App-side receiving; SWBPIPE construction (embedded loop, native layer, panel, domain connection) stays with the outside SWBPIPE session | CLM-001, CLM-003; HI §1, §11 |
| B-3 | A written interface, a prepared relay file or its transmission is not agreement, delivery, integration, qualification or adoption | CLM-006; HI §1; RELAY §0; CA §7.2 |
| B-4 | DECISION-1 D2: five acts reserved to the person for App/shared contracts in the first increment; the host names and enforces its own list (V4-HI-30); operation-specific additions await OI-021; host adoption not shown (DEP-001) | D2; ACT §3, §8.3 P-01 |
| B-5 | DECISION-1 D3: App routine tool permission (A14) is the user's own Codex setting; hosts have no classifier mode | D3; ACT §8.3 P-04 |
| B-6 | **SETTLED by DECISION-2 (D5):** host content read through the external channel may flow to the App conversation's selected model, cloud included; no App gate. **INTEGRATION (DECISION-2 reading; R4-1, R5-4):** the App records the destination per turn where the supplier reports it (requested and effective kept apart; unobserved turns *unknown*; the run-level value is the observed set) and shows it in the channel status, as information only. A host may restrict its own channel (SQ-16); V4-HOST-02 still governs the host's embedded agent (SQ-30) | D5; R4-1; R5-4; HOSTING §8.3; RS R5 |
| B-7 | **DECISION-2 (D6), deferred:** App-side run holds are `UNRESOLVED{D6}`. HP-1 (interposed App code) and HP-2 (reliance on `turn/interrupt`) are not adopted (R4-2); HP-3 is best effort; HP-4 (the App initiates nothing for a holding run) applies; every run action while a checkpoint waits is recorded as *action during hold*. **Scope (R5-10, R6-1):** the SQ-02 answer can settle only checkpoints whose **every held action is a host operation**; a checkpoint with any App-side held action stays *not enforceable* whatever SWBPIPE answers — a separate owner follow-up (EXEC U-E23) | D6; R4-2; R5-10; R6-1; EXEC §2, §3.6, U-E1, U-E23; ACT §4.6 |
| B-8 | Codex `0.158.0` is a definition/generation pin only; no qualification | D4; HOSTING §7, §10; SPIKE |
| B-9 | **Carriage assurance (R5-2):** only *host-held* carriage satisfies R2-12. A host loop's own evaluation of the declaration is host-held. A constraint the host merely received keeps its source's assurance (model-supplied or App-assured). App-assured is not available in this increment (R4-2) | R5-2; P §3.3; ACT §4.4; ADAPTER §5.2–§5.3 |

---

## 2. OUT-002 — App/shared versus host responsibility/interface matrix

### 2.0 Row summary

| Row | Receiving-map obligation | Primary App/shared definitions | Host contribution (RELAY-v0.3) | Principal open choices | Standing (summary) |
|---|---|---|---|---|---|
| 1 | Catalog and read meaning | C §2–§4, §6, §8; ACT §5.1, §8 | SQ-04 (a)(b), SQ-05 (a), SQ-11, SQ-12, SQ-18 (d)(e), SQ-24, SQ-26 | OI-003 (03-04/TBD-003); representation 03-01/TBD-003 (C U-C1); OI-021 | defined draft; relay pending; three-surface map owner-open |
| 2 | Single validation/application route | P §1–§2, §9; ACT §5.3, §6; C §4.1; LOOP §6–§7 | SQ-05 (d)(h), SQ-06, SQ-09, SQ-31 | OI-013/OI-014 (loop-side checking) | defined draft; host-owned; relay pending |
| 3 | Basis | C §5; P §3.2, §5, §6, §11, §12 | SQ-03 (a)(b), SQ-07 (a)–(h), SQ-08 (b) | Generation meaning (C U-C2); subject-identity scope (C U-C3) | defined draft (rule INTEGRATION); relay pending |
| 4 | Origin, undo and proposal presentation | P §3, §4, §7, §8, §9; AS §7; ADAPTER §5 | SQ-03 (c)(d), SQ-05 (g), SQ-08, SQ-09 (c)(f), SQ-10, SQ-14, SQ-22 | 03-02/TBD-002 mechanisms; undo mechanism (P U-P8) | defined draft; host-owned; relay pending |
| 5 | Human acts and compact records | ACT §2–§4, §8–§9; RS §2–§10; EXEC §5 | SQ-01, SQ-03 (e), SQ-05 (b)(c), SQ-19 (b)(c), SQ-21, SQ-23, SQ-25 | OI-021 additions; ACT U-03; OI-013/OI-014 record placement | defined draft; relay pending (SQ-01 blocks every positive host-content case) |
| 6 | Autonomy | ACT §4.4, §4.6, §5–§8; AS §2–§7; P §3.3, §4.4 | SQ-02, SQ-05 (a)(c)–(f)(h)(i) | D6 (host-operation held actions deferred to SQ-02; App-side held actions U-E23); ACT U-02; ACT U-06 | defined draft; relay pending; owner-open |
| 7 | Loop and panel | LOOP §1–§10; PANEL §1–§6 | SQ-02 (d), SQ-05 (e), SQ-20 (informational), SQ-22, SQ-23, **SQ-29…SQ-32** | OI-013; OI-014; DEP-05-01-024; N-OPEN-1…3; T-OPEN-1; R-OPEN-1 | defined draft; host-owned; relay pending; owner-open |
| 8 | Host methods and roles | WD §3–§6, §9; WD-EX; EXEC §3, §4, §6; HOSTING §8 S-6, §8.2 | SQ-01, SQ-02, SQ-11, SQ-17, SQ-18, SQ-19 (a)(d) | D6/U-E23; WD U-09; DEL-02-02 / DEL-02-04 (D1) | defined draft; relay pending; partly outside undertaking (D1) |
| 9 | Optional external catalog access (conditional) | ADAPTER §1–§10; ACT §2.6, V-10; HOSTING §6.7–§6.8, §8.3; XT §3 | **SQ-28**, SQ-02, SQ-06, SQ-08, SQ-12…SQ-16 | 03-03/TBD-007 (OC-1…OC-12); D6 | defined draft; relay pending; owner-open |
| 10 | Selected connectors (conditional) | None in this undertaking (DEL-07/08 outside D1); staging CA §6 | None by design (RELAY §3 "Not included") | 03-04/TBD-007, TBD-008, TBD-009 | outside undertaking (D1); owner-open |

### 2.1 Row 1 — Catalog and read meaning (HI §2, §3; HI §10 item 1)

| # | Obligation (receiving meaning) | App/shared definition (file, version, §) | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M1.1 | Every person-available operation (reads, changes, host checks, undo) described once, in an identified **catalog edition**; completeness is a parity rule | C-v0.5 §2 (invariants 1–5); editions e1/e2 and the edition-addition event (C §10.1, V-ED1 §10.4) | The actual catalog and edition identity (SQ-04 (a); SQ-12); edition-addition event form (SQ-26) | Representation and placement: C U-C1 (03-01/TBD-003) — App/shared capability-contract owner with host/consumer owners | defined draft; host-owned; relay pending |
| M1.2 | Nine entry elements: identity/version (equality only), purpose, input schema with explicit target identification, availability with reasons, effects, result with standing, errors with effect statements, class, exposure per surface | C-v0.5 §3, §3.2, §3.3; consumed by LOOP-v0.5 §2.2 and ADAPTER-v0.3 §4.2 | Entry content per operation (SQ-04 (a)); version compatibility statements (SQ-18 (d)); outcome of an entry-version mismatch (SQ-18 (e), C U-C6) | C U-C9 (host owner with DEL-02-01) | defined draft; relay pending |
| M1.3 | Distinct non-success results — unavailable (HI-04 parity only), not permitted, channel not enabled (App reports when its own configuration is off, host when its channel is off, R4-16), not exposed on this surface (host-reported), error — each with evaluated basis; never empty success; loop-side *not offered* and *missing* are not host results | C-v0.5 §4.1–§4.4; ACT-v0.5 §6 rows 1–2, 8–11 | Unavailable reasons with the same meaning on every surface; result statements mappable to these terms (SQ-09 (a)); exposure reporting (SQ-11) | — | defined draft; relay pending |
| M1.4 | Class element: five values with policy-record reference, value standing and host adoption | C-v0.5 §3.1; ACT-v0.5 §5.1, §8.1, §8.3 | The host's own class per operation and its reserved list (SQ-05 (a)–(c)) | `UNRESOLVED{OI-021}` operation-specific additions and first operation's class — owner via outside SWB session with App/shared owner; consequence vocabulary ACT U-02 — DEL-04-01 with host policy owner (SQ-05 (f)) | defined draft (D2 adopted; P-03 DERIVED); relay pending; owner-open |
| M1.5 | Read results return the same meaningful content and standing marks the person sees: currency, "host checks passed: ‹named checks›" with evaluated basis, limitations, faithfully carried act evidence, lapse state, agent findings (A3) — never "checked" | C-v0.5 §6.1–§6.2; AS-v0.5 §8; ACT-v0.5 §9 | Views, results, diagnostics and standing (SQ-04 (b) which check the activity uses); where findings are held and whether storing them is a change (SQ-24) | C U-C5 (host owner) | defined draft; host-owned; relay pending |
| M1.6 | Three-surface responsibility (H, E, X): generated, checked or hand-built, recorded before any conformance claim; extension promise preserved and **not claimed** | C-v0.5 §8 (every cell *unagreed*); XT-v0.3 §4 (V4-EXM-24 trace plan on V-ED1, CMP-01…CMP-15), §5 (work account; OI-003 disposition record); ADAPTER-v0.3 §9 OC-8 | Per-surface production route (SQ-12); the one new operation for the trace (SQ-26) | `UNRESOLVED{OI-003}` retain/narrow/defer — owner with host contract owner (03-04/TBD-003) | owner-open; relay pending |
| M1.7 | Catalog received by the three consumers: required-tool references (opaque catalog identity), loop tool offering (all nine elements; reserved entries always offered), external native-tool mapping | WD-v0.5 §4.2.1–§4.2.4; LOOP-v0.5 §2.2 (TL-1…TL-5); ADAPTER-v0.3 §4.1–§4.2 (NM-1…NM-4); EXEC-v0.3 §3 | Exposure per surface and first-activity entries on E and X (SQ-11); native-to-catalog mapping (SQ-12) | Shared catalog-schema checker `UNRESOLVED{OI-014}` (C §8 row; WD §9 A-11; LOOP §10.2 (b)) | defined draft; relay pending; owner-open |
| M1.8 | Operations used by the first connected activity (read, change, non-mutating check) | CA-v0.3 §2.3, §2.5 (DI-1…DI-3); FX-PIPE-01 (C-v0.5 §10) invented and proposed only | Candidate operations, check and environment (SQ-04) | `UNRESOLVED{OI-021}` (03-04/TBD-006) | owner-open; relay pending |

### 2.2 Row 2 — Single validation/application route (HI §4 V4-HI-20, -25; HI §10 item 2)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M2.1 | One route for person, embedded agent and external agent; channel is attribution only; equivalence rule; the only permitted difference is authority, reported as *not permitted* naming the governing treatment | P-v0.5 §1, §2; ADAPTER-v0.3 §6 (RP-1, RP-2); LOOP-v0.5 §6 (V-4, V-5) | The route itself (host-owned); outcome statements distinct from transport status (SQ-09 (a)); validation versus application refusals (SQ-09 (d)(e)) | — | defined draft; host-owned; relay pending |
| M2.2 | Treatment resolved on the host route at validation and again at application; loop and adapter relay intent and any constraint, never decide; direct without an effective direct treatment → *not permitted*, never converted | ACT-v0.5 §5.3, §5.5, §6; P-v0.5 §2; C-v0.5 §4.1; R-3 | Settings reference in force at application (SQ-05 (d)); treatment from the grant actually in force when the App saw *unconfirmed*, re-resolved at application (SQ-05 (h), AS U-04); adoption of P-01…P-06 (SQ-05 (c)) | Host adoption and enforcement (DEP-001) — host owner | defined draft; relay pending |
| M2.3 | Canonical outcome taxonomy per item (refused — invalid/stale, queued, accepted, rejected, withdrawn, applied (receipt) with applied-outcome association, application error with effect statement, outcome unknown for submissions only, observer-attributed); success ≠ acceptance; queued ≠ applied | P-v0.5 §9, §10; C-v0.5 §4.1; RS-v0.5 §5; ADAPTER-v0.3 §4.5 (M-1…M-5; a read with no stated result is an *error* as observed, M-3); AS-v0.5 §8 | Result forms mapped to these terms; item application grouping (SQ-09 (a)(b)(f)) | P U-P4, U-P5, U-P7 — host owner | defined draft; relay pending |
| M2.4 | Loop-side pre-route failures: catalog-schema checking before host domain validation; malformed or truncated calls never executed with empty arguments; *not offered* never dispatched; undispatched siblings held at a checkpoint (LH-0) | LOOP-v0.5 §6 (V-1…V-3), §7 (MC-1…MC-9), §2.4.4 LH-0 | Host-loop realization (host-owned): validation order, malformed/truncated handling, sibling behavior (**SQ-31** (a)–(d)); model-interface expression of "no arguments" and truncation (**SQ-29** (c)) | Loop placement and parsing `UNRESOLVED{OI-013}`; any shared checker `UNRESOLVED{OI-014}`; LOOP T-OPEN-1 (DEL-05-01 with DEL-03-02 and host owner); DEP-05-01-024 (supplier UNKNOWN) | defined draft; host-owned; relay pending; owner-open |
| M2.5 | No second agent route | P-v0.5 §2; ADAPTER-v0.3 RP-1; PANEL-v0.5 §4 H-4 | Confirmation that the external seam uses the one route (SQ-12) | — | defined draft; relay pending |

### 2.3 Row 3 — Basis (HI §3 V4-HI-11; §4 V4-HI-23; HI §10 item 3)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M3.1 | Every read returns one basis descriptor: workspace identity, generation (host lineage epoch), model revision, canonical content identity, identity method designation; a read lacking any element is *basis incomplete* | C-v0.5 §5.1–§5.2 (the SoW's "canonical content hash" is received as canonical content identity plus method designation, R-6) | Full descriptor on every read; meaning of a new generation (SQ-07 (a)(b)) | Algorithm C U-C1 (03-01/TBD-003); generation meaning C U-C2 — host owner with DEL-04-03 | defined draft; relay pending |
| M3.2 | Per-row/object **subject content identity** with method designation, distinct from the read-level identity | C-v0.5 §5.3; RS-v0.5 §7 (L-1, L-2); P-v0.5 §3.1, §3.4 | Subject identities per object kind and attribute scope (SQ-03 (a)(b)) | C U-C3 — host owner with DEL-03-01/DEL-03-02 | defined draft; relay pending |
| M3.3 | A later action cites the relied-on basis unchanged, with relied-on target identities; never replaced by a queue-, acceptance- or application-time basis | C-v0.5 §5.4; P-v0.5 §3.2, §12 (HI §11 risk) | Original inspected basis kept (SQ-07 (c)); which cited bases must hold for multi-read reliance (SQ-07 (g), C U-C4) | — | defined draft; relay pending (HI §11 risk) |
| M3.4 | Stale refusal per item, reporting relied and current bases and failing targets; de-duplication by proposal identity precedes the basis check; re-draft with lineage; no retargeting | P-v0.5 §5, §6; C-v0.5 §5.4 (R2-13 INTEGRATION); CA-v0.3 §2.3 CA-4 | Per-item check; re-check after acceptance; invalidating changes (SQ-07 (d)(e)(f)); de-duplication order (SQ-08 (b)) | Host confirmation (C U-C3; P U-P3) — host owner | defined draft (rule INTEGRATION); relay pending |
| M3.5 | Non-mutating reads, examinations and host checks citing a basis are never refused stale; they state both bases | C-v0.5 §5.4 (PROPOSED) | Confirmation (SQ-07 (h), C U-C10) | Host owner | defined draft (PROPOSED); relay pending |
| M3.6 | Read-then-action comparison with an intervening edit (M3-CP) | P-v0.5 §11; C-v0.5 §9 (VC-C-04) | A candidate-bound observation (SQ-27) | — | defined draft (designed); DEL-03-01 AC-004 held until an actual return exists |

### 2.4 Row 4 — Origin, undo and proposal presentation (HI §4 V4-HI-21…24; HI §10 item 4)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M4.1 | Origin on every change: author type, author identity (value *unverified* allowed, R4-15), seat role meaning, channel, conversation, workflow identity tuple and run, standing at drafting, both settings references, governing checkpoint constraint with its **carriage assurance** (host-held · App-assured (not available this increment) · model-supplied · absent; only host-held satisfies R2-12, R5-2), reason; the host origin mark is linked, not copied | P-v0.5 §3.3; ADAPTER-v0.3 §5.1–§5.5; LOOP-v0.5 §6.2; RS-v0.5 R7, R11 | Recorded origin elements, which are verified, readable origin mark, caller authentication (SQ-14) | Caller identity mechanism ADAPTER OC-6 — host owner with App owner | defined draft; relay pending |
| M4.2 | Proposal identity (retry keeps it; re-draft gets a new one), change items, change-item content identity; acceptance unit = change item; row / multi-row / batch acceptance; proposer alone withdraws, rejection is the person's wherever acceptance is | P-v0.5 §3.1, §3.4, §4.1–§4.3; ACT-v0.5 §7 | Identity minting and read by identity (SQ-08 (a)(d)); A5 bound to change-item content (SQ-03 (c)); operation-specific withdraw/reject rules (SQ-05 (g), P U-P6) | Identity mechanics 03-02/TBD-002 (P U-P1) — relevant contract and host owners | defined draft; relay pending |
| M4.3 | Direct application (effective direct grant state, no governing constraint) carries receipt, origin mark, undo route and later-check route; no acceptance recorded or implied | P-v0.5 §4.4; AS-v0.5 §7 | These four host elements; resulting objects (SQ-03 (d); SQ-09; SQ-10) | Host availability of each (AS U-05) — host owner | defined draft; host-owned; relay pending |
| M4.4 | Undo is a change through the one route with *reverses ⟨receipt⟩*, governed by the reversed operation's policy; acts on changed content lapse normally; a lapse re-holds whatever caused it, including the person's own undo, which is never "action during hold"; an undo never re-holds an A5 arrival (R5-5) | P-v0.5 §4.5; AS-v0.5 §7; C-v0.5 §10 OP-C10; ACT-v0.5 §8.3 P-03 (R3-4); ADAPTER-v0.3 RP-6; EXEC-v0.3 §4.7 | Undo route, scope, receipt relation, "publication" (SQ-10) | Undo mechanism P U-P8 — host owner | defined draft; host-owned; relay pending |
| M4.5 | Repeated submission → at most one effect per item: a host obligation to be evidenced, not a recorded fact | P-v0.5 §7; ADAPTER-v0.3 §5.6 (PI-1…PI-6); RS-v0.5 §5 | De-duplication durability and domain evidence of one effect (SQ-08 (c)(e)) | 03-02/TBD-002 | defined draft; relay pending (HI §11) |
| M4.6 | Outcome unknown (submissions only): reported by whoever lost observation; last observed state; recovery by read or same-identity retry; nothing back-filled | P-v0.5 §9; ADAPTER-v0.3 §7.4; LOOP-v0.5 §6.3; EXEC-v0.3 §4.12 | Receipt durability; resolution by later read (SQ-09 (c)) | — | defined draft; relay pending |
| M4.7 | Proposals shown in the host's own views: old/new values, affected objects, reason, origin, per-item disposition with actor, stale indication, lineage, item-left events; "accept", never "approve" | P-v0.5 §8; PANEL-v0.5 §3.3, §4 (H-1…H-6); ACT-v0.5 §9 | Which views, and how the panel references a position (SQ-22) | — | defined draft; host-owned; relay pending |

### 2.5 Row 5 — Human acts and compact records (HI §5, §9; HI §10 item 5)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M5.1 | Canonical acts A1–A14; execution distinct from acceptance, checking, approval and reliance; one act never implies another; a person's own A1/A2 are run-record (R7) operations, while an operation that performs a reserved act produces the human-act record the R7 entry references (R5-6) | ACT-v0.5 §2.1–§2.4, §3; P-v0.5 §10; RS-v0.5 §3, R7; HOSTING-v0.5 §11 | — | — | defined draft |
| M5.2 | Reserved acts (D2; A10 DERIVED; A13 disabling INTEGRATION); operations that perform reserved acts are reserved (P-02) | ACT-v0.5 §3, §8.3 (P-01, P-01a, P-02); C-v0.5 §3.1 rule 1; AS-v0.5 §2 | The host's own list and enforcement; operation-specific additions (SQ-05 (b)(c)) | `UNRESOLVED{OI-021}` (03-04/TBD-001 residue) | defined draft (adopted decision, App/shared); relay pending |
| M5.3 | Capturing surfaces and capture evidence: host act facility for host content; App act control for App content (built by DEL-01-04, D1); the A12 control that establishes the setting; the host enablement facility for A13; an act counts only if captured at or after the arrival (R4-5); user-input/elicitation answers, A14 settlements and conversation are never act evidence | ACT-v0.5 §2.6, §4.5; RS-v0.5 §6.1–§6.2 (HA-1, HA-7); EXEC-v0.3 §4.5 (SP), §5 (CAP-1…CAP-9); HOSTING-v0.5 §6 (R9), §6.8 | Stable capture-evidence reference per act kind and for act-declined events (**SQ-01**, P1); A13 facility reference (SQ-28); whether App-captured acts on host content are accepted (SQ-25) | App act control DEL-01-04 (outside D1); App person identity EXEC U-E8 | relay pending (SQ-01 blocks every positive host-content checkpoint); App side outside undertaking (D1) |
| M5.4 | Faithful recording (A9): recorder ≠ decision actor, cites capture evidence, never satisfies a checkpoint by itself; no faithful record through a reserved act-performing operation; a host faithful-record operation, if any, meets the R2-2 conditions | ACT-v0.5 §2.4, §8.3 P-02; RS-v0.5 §6.2 (HA-2, HA-7, HA-9) | SQ-21 | — | defined draft; relay pending |
| M5.5 | Acts bind to content (change-item / subject / file / setting content) and lapse visibly; applying an accepted item does not lapse its A5; a later A12 supersedes only when established (R4-6); return to c₀ after an observed lapse | ACT-v0.5 §2.5; RS-v0.5 §7 (L-0…L-13); C-v0.5 §5.3, §6.2 rule 4; P-v0.5 §3.1; AS-v0.5 §8 | Subject/change-item identities (SQ-03 (a)–(d)); identity after return to exact prior content (SQ-03 (e), RS U-12); host display of lapse, supersession, stale-after-acceptance, reversal (SQ-23) | Multi-row A4 purpose after partial lapse ACT U-03 / RS U-07 — DEL-04-01 with the owner | defined draft; relay pending; owner-open |
| M5.6 | Compact run record R1–R14 with the host project for host-agent runs: workflow identity and revision, conversation, settings, operations and outcomes, receipts by reference, human acts, model and **model destination per turn** (R5, INTEGRATION DECISION-2 reading), v0.4 additions (ordinals, run-resumed, re-held/replaced, A12 control effect, prior act not counted, continues ⟨run⟩, action during hold, transfer links, compatibility-report reference R14) | RS-v0.5 §2 (OF-1…OF-9), §3, §4, §4.1, §9; HOSTING-v0.5 §8 S-7, §8.2, §8.3 (App side) | Host run recording in the shared meaning; full workflow identity; relay of records by reference (SQ-19 (b)(c)) | Host persistence `UNRESOLVED{OI-013}` (RS U-06); App record location with OI-014 owners (RS U-05); serialization RS U-04 | defined draft; host-owned; relay pending |
| M5.7 | Settings-in / record-out exchange (CASE-002 M3) | RS-v0.5 §8; AS-v0.5 §6 | — | Record representation RS U-04 | defined draft |
| M5.8 | Act-declined event resolves negatively; run-ended leaves *waiting*; an ended run is never resumed; continuation is a new run with *continues ⟨run⟩* (R4-4) | ACT-v0.5 §2.3; RS-v0.5 §3; EXEC-v0.3 §4.8, §4.9 | Capture of decline events (SQ-01) | — | defined draft; relay pending |

### 2.6 Row 6 — Autonomy (HI §6; HI §10 item 6)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M6.1 | Per class, a grant value (direct / propose) within a representation-neutral scope, set by the person through A12; governs host operations only; visible, changeable, recorded per run | ACT-v0.5 §5.1, §5.2, §5.4; AS-v0.5 §2; RS-v0.5 R6 | Host controls (host-owned); grant presentation (SQ-05 (e)) | Consequence dimension ACT U-02 — DEL-04-01 with host policy owner (SQ-05 (f)) | defined draft; host-owned; relay pending; owner-open |
| M6.2 | Seven grant display states; two settings references (route decision; in force at application, host-reported or *unconfirmed*) | AS-v0.5 §3; ACT-v0.5 §5.4; P-v0.5 §3.3 | Settings reference at application (SQ-05 (d)); enforcement of *unconfirmed* and re-resolution at application (SQ-05 (h), AS U-04) | — | defined draft; relay pending |
| M6.3 | Conservative defaults; SWB model changes (P-03) default *propose* with row / multi-row / batch acceptance, widenable by the person within W-a…W-j; queued proposals never converted | ACT-v0.5 §5.5, §5.6, §7, §8.3 P-03; AS-v0.5 §2 | Class and default per operation (SQ-05 (a)(c)); defaults for other consequential classes (SQ-05 (i), ACT U-06) | — | defined draft (class DERIVED, default accepted); relay pending |
| M6.4 | Declared checkpoints override autonomy; an A5 checkpoint forces *propose* (P-05); a direct request under the constraint is *not permitted* naming it; only **host-held** carriage satisfies R2-12 (R5-2) | ACT-v0.5 §4.4, §8.3 P-05; P-v0.5 §3.3, §4.4; WD-v0.5 §4.2.2, I-7; ADAPTER-v0.3 §5.3 (GC-1…GC-5) | Per-request receipt verified against the host's own declaration copy, a host-held declaration, or a host-held run association; *not permitted* naming it; host holds before dispatch per surface (**SQ-02** (a)–(e), P1) | Host-operation checkpoints in App runs: `UNRESOLVED{D6}` — owner, deferred to SQ-02 (EXEC U-E1); checkpoints with any App-side held action: owner follow-up **EXEC U-E23** (R6-1) | relay pending (V-CP1, LOOP FX-C9, PANEL PC-24, WD VC-11, EXEC CH-27, ADAPTER XF-25 AWAITING INPUT); owner-open |
| M6.5 | No policy basis (P-06): direct not permitted; proposing confers no permission; A12 widening refused; dependent production held | ACT-v0.5 §8.3 P-06; C-v0.5 §3.1 rule 4; AS-v0.5 §2 | Classing the first operation (SQ-05 (a)) | `UNRESOLVED{OI-021}` (C OP-C11) | defined draft (INTEGRATION); owner-open |
| M6.6 | Routine tool permission (A14) is not autonomy: App side the user's Codex setting (D3), recorded only in RS R13; hosts have no classifier mode | ACT-v0.5 §8.3 P-04; RS-v0.5 R13; HOSTING-v0.5 §6.6, §11; LOOP-v0.5 §1; PANEL-v0.5 §1 | None | — | defined draft (adopted decision D3) |

### 2.7 Row 7 — Loop and panel (HI §1; HI §10 item 7)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M7.1 | Replaceable four-subject boundary (messages and run association, tools, events, checkpoints); host consumers only; never merged with the App's Codex path | LOOP-v0.5 §1, §2 (§2.1–§2.4), §3 | Loop construction (host-owned; DEP-001); intended placement, informational (SQ-20) | `UNRESOLVED{OI-013}` (03-04/TBD-004) — shared contract owner with SWB implementation owner | defined draft; host-owned; owner-open |
| M7.2 | Model interface: OpenAI-compatible Chat Completions with tool calls; representation waits for its supplier | LOOP-v0.5 §1, §4, §11 (fixture basis); UNRESOLVED DEP-05-01-024 | Interface, servers and versions; tool-call expression; recorded exchanges as fixture basis (**SQ-29** (a)–(d)) | DEP-05-01-024 supplier UNKNOWN; App/shared embedded-integration owner receives or agrees | defined draft; relay pending; owner-open |
| M7.3 | Native endpoint and key boundary: local default, cloud only by choice plus key, no cloud fallback, key never visible to the script, native layer enforces; local operation's only destination is the configured server (V4-HOST-02) | LOOP-v0.5 §5.1 (NW-1…NW-7), §5.2 (MS-01…MS-11) | Native layer and endpoint enforcement; definitions for N-OPEN-1…3; endpoint-redirect refusal (**SQ-30** (a)–(e)) | LOOP N-OPEN-1…3 — App/shared embedded-integration owner with SWBPIPE owner; the owner if V4-HOST-02 is affected | defined draft; host-owned; relay pending; owner-open |
| M7.4 | Validation order; malformed and truncated calls reported, never executed | LOOP-v0.5 §6, §7 (as M2.4) | SQ-31 | As M2.4 | defined draft; host-owned; relay pending |
| M7.5 | Responsiveness: the loop does not block the host interface; qualitative observation protocol | LOOP-v0.5 §8 (RS-1…RS-4) | Placement, cancel behavior, relayed observations, threshold wish (**SQ-32**) | LOOP R-OPEN-1 — the owner, if wanted | defined draft; host-owned; relay pending |
| M7.6 | Checkpoint evaluation in host loops: reached-when observation, declared subject class binding, dispositions; hold support **enforced by the host loop** with residual limits recorded as evidence limits (action during hold), not as separate values | LOOP-v0.5 §2.4 (§2.4.1–§2.4.4, LH-0…LH-4); EXEC-v0.3 §3.6 (HS-2), §4; WD-v0.5 §4.3 | Host holds before dispatch on the embedded surface (SQ-02 (d)); sibling holding (SQ-31 (d)); placement (SQ-20) | EXEC U-E2 `UNRESOLVED{OI-013}` / `{OI-014}` | defined draft; relay pending (host evidence DEP-001); owner-open |
| M7.7 | Panel: conversation, workflow selection (with hold support per checkpoint), proposal queue and checks, declared checkpoints and the active grant; results in host tables and views; no agent-private surface; "accept" wording; lapse and supersession visible | PANEL-v0.5 §3.1–§3.6, §4 (H-1…H-6), §5 | Panel assembly, tables and views (host-owned); SQ-22; SQ-23; grant presentation (SQ-05 (e)); who evaluates required-tool outcomes in the host (SQ-17 (c)) | DEL-02-03 checker only under OI-014 | defined draft; host-owned; relay pending |
| M7.8 | Reusable components only where a repeated responsibility is agreed; no common loop or service presumed | PANEL-v0.5 §6; LOOP-v0.5 §10.1–§10.2; WD-v0.5 §9 (A-1…A-12) | — | `UNRESOLVED{OI-014}` (03-04/TBD-005); host side `UNRESOLVED{OI-013}` | owner-open (every confirmation "None") |

### 2.8 Row 8 — Host methods and roles (HI §10 item 8; V4-WF-01…06)

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M8.1 | Portable declared part: inputs, required tools by catalog identity, checkpoints naming a closed-list act (A4, A5, A6, A7, A12) and their **held actions** (host operations only, or listed steps with App-side steps marked; conservative default HS-5; R6-1), outputs with promised standing, evidence by reference; requirement ≠ restriction | WD-v0.5 §3, §4.1–§4.7 (§4.3.1 *held actions*); WD-EX-v0.5 E1–E8 | Host workflows authored by the host/method owner (SQ-18 (a)); reading the declared part at the App's declaration contract version (SQ-17 (b)) | Physical carriage WD U-01 — DEL-02-01 with consumers | defined draft; host-owned; relay pending |
| M8.2 | Source-qualified identity + derived-from; holding library as a non-identity fact; promised versus observed chain | WD-v0.5 §6.1–§6.4; EXEC-v0.3 §6.1, §6.2; RS-v0.5 R2; C-v0.5 §10.1 (LIB-A1, LIB-A2) | Listing carried workflows unadapted, original origin, host holding library (SQ-17 (a)); host identity display (SQ-18 (a)) | Revision algorithm WD U-03; host precedence WD U-10 (DEL-02-02, D1; RELAY "Not included") | defined draft; relay pending |
| M8.3 | Required-tool compatibility report with the three-value check result (does not pass incl. *unsupported* / not established / passes) and multi-checkpoint precedence; *unsupported* for "checkpoint hold not enforceable on this surface" (R4-8); harness-capability kind (a) not holdable in App runs (R4-21) | WD-v0.5 §4.2.4, §4.3.8; EXEC-v0.3 §3 (§3.5 pass rule, §3.6 hold support); WD-EX-v0.5 E7, E8 | Exposure per surface (SQ-11); who evaluates compatibility and holds for host runs and how unsupported outcomes are shown (SQ-17 (c)) | Harness capability naming WD U-08 / EXEC U-E10 | defined draft; relay pending |
| M8.4 | Checkpoint semantics and hold machine: arrival, SP (capture after arrival, R4-5), dispositions, re-hold after resume (R4-3; generalized R5-5), no resumption of ended runs (R4-4), mixed items MX-3/MX-6/MX-8 (R4-7); grant-setting subject always declared and never chosen by an A8 (R5-3); grant change after arrival shown by C V-GR1 (R5-7); hold support by held actions (R6-1) with per-value meaning of "held" (R6-3) | WD-v0.5 §4.3 (§4.3.1 incl. *held actions*, §4.3.8; I-9); EXEC-v0.3 §4 (§4.1–§4.14); ACT-v0.5 §4, §4.6; C-v0.5 §10.4 V-GR1 | Host capture evidence (SQ-01); host-held evaluation or constraint receipt; host holds before dispatch (SQ-02 (d)); refusal of the run's further host operations after an arrival until the act (SQ-02 (f)) | `UNRESOLVED{D6}`: checkpoints whose every held action is a host operation to SQ-02 (EXEC U-E1); any App-side held action **EXEC U-E23** (owner); EXEC U-E4 (SP-6 versus counting prior acts; cost recorded under R5-7); ACT U-03 | defined draft; relay pending; owner-open |
| M8.5 | Transfer App → host (package plus carriage manifest) and host → App refinement; adaptation is a new identity with host origin and derived-from; no identity or act inheritance | EXEC-v0.3 §6.3–§6.7; WD-v0.5 §6.4; CA-v0.3 §4 | Relay form (SQ-17 (d)); adaptation as new revision; checkpoint comparison (SQ-18 (b)(c)) | Registration, drafts and selection policy DEL-02-02 *(outside undertaking, D1)* | defined draft; relay pending; partly outside undertaking (D1) |
| M8.6 | Four roles behind a single host seat; seat role meaning on every dispatch; additive role guidance with per-thread/turn supplied-guidance evidence ("supplied ≠ adopted") | WD-v0.5 §5 (§5.1–§5.3); HOSTING-v0.5 §8 S-6, §8.2; RS-v0.5 R3, R5a | Per-turn guidance source and content identity in host loops (SQ-19 (a)); seat → role mapping (SQ-19 (d), WD U-09) | Role supply DEL-02-04 *(outside undertaking, D1)*; guidance distribution `UNRESOLVED{OI-018}` (WD U-14) | defined draft (WD, HOSTING); relay pending; role supply outside undertaking (D1) |
| M8.7 | Host methods tested and refined in the App: App runs go through stock Codex; host revision opened read-only and refined | HOSTING-v0.5 §1; EXEC-v0.3 §6.5; CA-v0.3 §8 W14-09 | Host revision relayed with identity (SQ-18 (a); SQ-27 (a)) | DEL-02-02 *(outside undertaking, D1)*: V4-EXM-14 cannot complete in this undertaking | defined draft; outside undertaking (D1) |

### 2.9 Row 9 — Optional external catalog access (HI §7; HI §10 item 9) — conditional

Applies only where a host exposes its catalog externally; never a startup
input (REQ-001). **SQ-28 gates the whole external channel**: without an
evidenced A13, the channel stays *not enabled* for every live CA/X and XC case
(R5-10).

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M9.1 | External access off unless the person enables it (A13) through the **host's enablement facility**; disabling also A13; an agent may only request (A8); App-side configuration an agent could write is never A13 evidence; the host's refusal is the authoritative "off"; enablement grants no autonomy | ACT-v0.5 §2.1 (A13), §2.6 (closes ADAPTER U-X1, PROPOSED under R4-13), §10 V-10; ADAPTER-v0.3 §3.1–§3.3 (E-1…E-9) | Enablement facility with a capture-evidence reference, readable state (**SQ-28**); off by default, *channel not enabled*, disable behavior for queued proposals (SQ-13) | Whether a given host requires its own facility (ACT §2.6 "still open", DEP-001) | defined draft; relay pending |
| M9.2 | Channel states disabled / enabled / endpoint-unavailable / operation-unavailable, never replacing C §4.1 outcomes; *enablement unconfirmed* treated as disabled | ADAPTER-v0.3 §3.2; C-v0.5 §4.1 | Enablement read (SQ-28; SQ-13) | — | defined draft; relay pending |
| M9.3 | The host selects the seam (MCP, CLI or both), built from the catalog; the App receives it; the App-initiated `mcpServer/tool/call` is App-origin, never used to act as the agent or for anyone's act | ADAPTER-v0.3 §2, §4.1, §9 (OC-1, OC-2, OC-8), §12; HOSTING-v0.5 §3, §6.8; SPIKE §4–§6 | Seam; derivation; native-to-catalog mapping (SQ-12) | 03-03/TBD-007 (OC-1…OC-12) — App external-host integration owner with external host owner; interposed families not adopted (R4-2) | defined draft; relay pending; owner-open |
| M9.4 | Same route, validation, grant and reserved acts as the host UI; a channel-specific host rule stated as a governing treatment | ADAPTER-v0.3 §6 (RP-1…RP-6); ACT-v0.5 §5.3, §6 | SQ-06 | — | defined draft; relay pending |
| M9.5 | Carriage of origin, grant in force, governing checkpoint constraint and proposal identity, each with its carriage assurance; hold support on X per EXEC §3.6 HS-3…HS-5 (§2.14) | ADAPTER-v0.3 §5.1–§5.6 (GC-1…GC-5, PI-1…PI-6), §7.7; EXEC-v0.3 §3.6 | Host-held constraint or host hold (SQ-02); identity minting and durable de-duplication (SQ-08); origin elements (SQ-14) | OC-7 carriage mechanism (03-03/TBD-007); `UNRESOLVED{D6}` (EXEC U-E1, U-E23) | defined draft; relay pending; owner-open |
| M9.6 | Machine-local endpoint; the App never changes the person's sandbox or permission settings | ADAPTER-v0.3 §3.3 E-7, §3.5; HI V4-HI-52 | SQ-15 | OC-5 — host owner with App owner | defined draft; relay pending |
| M9.7 | Model destination: may flow to the selected model, cloud included, no App gate (**SETTLED**, D5); recorded per turn (requested/effective apart; unobserved *unknown*) and shown in channel status (**INTEGRATION, DECISION-2 reading**; R4-1, R5-4); a host may restrict its own channel | ADAPTER-v0.3 §3.4; HOSTING-v0.5 §8.3; RS-v0.5 R5; EXEC-v0.3 CR-14 | Whether the host restricts its own channel by destination, how a refusal is reported, what the App must state (SQ-16) | Host channel policy (DEP-001) — host owner | defined draft (App side settled); relay pending (host side) |
| M9.8 | External control witness and adapter fixture inventory | XT-v0.3 §2 (IN-01…IN-29), §3 (V4-EXM-25, XC-01…XC-12); ADAPTER-v0.3 §10 (XF-01…XF-42) | Identified candidate, host checks, the engineer's actual act (SQ-27; SQ-01; SQ-28) | — | defined draft (designed, not run); relay pending |

### 2.10 Row 10 — Selected connectors (HI §8, §8.1; HI §10 item 10) — conditional, not designed here

| # | Obligation | App/shared definition | Host contribution required | Open choices — who decides | Standing |
|---|---|---|---|---|---|
| M10.1 | PEC, where selected: own interface; pin, source reference, coverage, freshness; reliance only on qualified/released coverage adopted by the consumer; qualified, limited and absent distinguished | DEL-07-01/07-02 accepted SoW meaning *(outside undertaking, D1)*; HI V4-HI-61…63 | Host integration of PEC use, if selected (host-owned); provider by the PEC owning project | 03-04/TBD-007 (OI-022) — App consumer owner and PEC owner | outside undertaking (D1); owner-open |
| M10.2 | Domains in the later research-to-design increment: provider/query, admission, freshness, research workflow, host use and the human's candidate approval, each separately evidenced | DEL-08-01/08-02 accepted SoW meaning *(outside undertaking, D1)*; HI §8.1 | Host use and approval route, later | 03-04/TBD-008 (OI-023); 03-04/TBD-009 (OI-026) | outside undertaking (D1); owner-open |
| M10.3 | Independent absent/limited paths: first connected work proceeds without PEC or Domains | CA-v0.3 §6 (ST-0…ST-5); HI V4-HI-62, -64; RELAY §3 "Not included" | None for the first activity | — | defined draft (staging only) |

### 2.11 Supporting contributions that serve several rows

| Contribution | Role in this guide | Rows served |
|---|---|---|
| HOSTING-v0.5 and SPIKE-v0.1 (DEL-01-01) | The App's Codex boundary: register (every request answered, declined or errored); A14 origins; run holds and the supplier (§6.7, HP-4); MCP surfaces (§6.8); supplied-guidance evidence (§8.2); observed model destination (§8.3); supplier facts at the definition pin | 5, 6, 8, 9 |
| CA-v0.3 (DEL-09-06) | Step map CA-0…CA-5, CA-H, CA-R with host contributions by SQ; hold support by variant (§2.2); owner/check allocation (§5); staging (§6); standing ladder (§7.2); V4-EXM-14 witness design (§8) | All rows |
| RELAY-v0.3 (DEL-09-06) | SQ-01…SQ-32 with sub-questions, priority groups P1…P8, source-to-question map and "Not included" list, return ledger (all *not observed*) | Host column of every row |
| XT-v0.3 (DEL-09-09) | V4-EXM-25 suite, V4-EXM-24 trace on V-ED1, work account, OI-003 disposition record | 1, 9 |
| C-v0.5 §10 FX-PIPE-01 | The one invented fixture catalogue (FXA-1…FXA-5, LIB-A1/A2, AF-1, e1/e2, V-CP1, V-ED1, V-GR1); never SWBPIPE behavior | All rows (examples) |

### 2.12 Excluded acts one-for-one (REQ-008; AC-007)

| # | Excluded act or production (REQ-008) | Owner (claim) | This guide's part |
|---|---|---|---|
| X-01 | Catalog/schema construction | App DEL-03-01 (CLM-002) | Cites C |
| X-02 | Proposal/outcome schema construction | App DEL-03-02 (CLM-002) | Cites P |
| X-03 | App external receiving implementation | App DEL-03-03 (CLM-002) | Cites ADAPTER |
| X-04 | Portable workflow contract production | App DEL-02-01 (CLM-003) | Cites WD, WD-EX |
| X-05 | Execution-compatibility implementation | App DEL-02-03 (CLM-003) | Cites EXEC |
| X-06 | Additive role supply | App DEL-02-04 (CLM-003) — outside D1 | Names the row (M8.6) |
| X-07 | Loop receiving definition | App DEL-05-01 (CLM-003) | Cites LOOP |
| X-08 | Panel receiving definition | App DEL-05-02 (CLM-003) | Cites PANEL |
| X-09 | Adopted policy definition | App DEL-04-01 (CLM-004) | Cites ACT; decides no policy |
| X-10 | Autonomy receiving implementation | App DEL-04-02 (CLM-004) | Cites AS |
| X-11 | Record writer/reader construction | App DEL-04-03 (CLM-004) | Cites RS |
| X-12 | PEC receiving and fallback | App DEL-07-01, DEL-07-02 (CLM-005) — outside D1 | Row 10 only |
| X-13 | Domains receiving and later-activity production | App DEL-08-01, DEL-08-02 (CLM-005) — outside D1 | Row 10 only |
| X-14 | Host domain, catalog, validation, application, receipts, origin, undo, UI, loop, native layer, panel construction | Host owner; SWBPIPE outside session (CLM-001) | Relay references only |
| X-15 | Human decisions (A4, A5, A6, A7, A10, A12, A13) and professional reliance | The actual human actor; the accountable professional (CLM-001, CLM-004) | Never performed, recorded or implied |
| X-16 | PEC provider production | PEC owning project (CLM-005) | Not addressed beyond M10.1 |
| X-17 | Domains provider allocation | Owner decision retained in 03-04/TBD-009 (CLM-005) | Carried as owner-open |
| X-18 | Actual external relay | The human (CLM-006) | Never claims relay |
| X-19 | Commitments and adoption | Each receiver (CLM-006) | "Relay pending" never promoted |
| **Retained** | Guide integration, the interface matrix and their completeness checks | **DEL-03-04** | §2–§4 |

### 2.13 Open issues carried at their owners and points of need (TBD-001…TBD-009; AC-006)

| SoW item | Open issue | Owner (literal, SoW) | Point of need (literal, SoW) | Current standing in this guide |
|---|---|---|---|---|
| TBD-001 | OI-001 reserved acts | Owner with App/SWB contract owners | Before operation-policy production contracts | **Adopted at App/shared level** by DECISION-1 D2 (ACT P-01); residue `UNRESOLVED{OI-021}`; host list relay pending (SQ-05). SoW text still reads open (F-5) |
| TBD-002 | OI-002 classifier routine permissions | Owner with App/SWB contract owners | Before permission-policy implementation | **Adopted** by DECISION-1 D3 (ACT P-04). SoW text still reads open (F-5) |
| TBD-003 | OI-003 automatic catalog extension | Owner with host contract owner | Before claiming extension capability or fixing its acceptance criterion | owner-open; XT §4–§5; SQ-26 (M1.6) |
| TBD-004 | OI-013 per-host loop placement and persistence | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | owner-open (M2.4, M5.6, M7.1, M7.6, M7.8); SQ-20, SQ-32 informational |
| TBD-005 | OI-014 shared contract/component placement | App/shared contract owners | Before structural/production contract allocation | owner-open (M1.7, M7.8) |
| TBD-006 | OI-021 first connected activity | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution; host evidence before corresponding connected-journey integration/examination and fallback-replacement decision | owner-open (M1.8, M6.5); SQ-04/SQ-05 inform it |
| TBD-007 | OI-022 PEC first receiving envelope | App consumer owner and PEC owner | Before operational consumer reliance | owner-open; outside undertaking (M10.1) |
| TBD-008 | OI-023 Domains receiving contract and timing | Owner with Domains/SWB/App receiving owners | Before later Domains-enabled design increment | owner-open; outside undertaking (M10.2) |
| TBD-009 | OI-026 Domains provider ownership | Owner with App/Domains/SWB definition owners | Before allocating Domains provider production and committing its integration | owner-open; outside undertaking (M10.2) |
| — (added) | D6 App-side holds, checkpoints whose **every held action is a host operation** (EXEC U-E1; HS-3) | Owner (DECISION-2), on the SQ-02 answer | Before any App-side positive hold case; before the App fixes its realization family | `UNRESOLVED{D6}` (M6.4, M8.4, M9.5) |
| — (added) | D6 follow-up, checkpoints with **any App-side held action** in App runs (EXEC U-E23; HS-5) | The owner (separate D6 follow-up; no SWBPIPE answer can settle it, R5-10, R6-1) | Before any workflow with a checkpoint with any App-side held action (including an App-content checkpoint) is offered as supported in App runs (EXEC U-E23, as amended by R7-4 m-6) | *not enforceable* → *unsupported* (M8.4; G-8) |

### 2.14 Hold-support map (R5-1, R6-1, R6-3; EXEC-v0.3 §3.6, authoritative)

The value is decided by the checkpoint's **held actions** (WD-v0.5 §4.3.1),
not by how it arrives. Rows are evaluated in the order **HS-1, HS-2, HS-5,
HS-4, HS-3**; the first match decides. For App runs, HS-3/HS-4 and HS-5 form
an exhaustive partition: either every held action is a host operation, or at
least one is App-side.

| Order | Surface and checkpoint | Hold support | What "held" means (R6-3) | Workflow check effect | Changes when |
|---|---|---|---|---|---|
| HS-1 | Any surface; invalid or not-established declaration (FB-03, FB-04, FB-13, FB-16; A12 declaration naming no setting content) | **No value**; reported invalid / not established | — | *not established* via the declaration | Declaration fixed |
| HS-2 | Host run on E, any valid checkpoint | **enforced by the host loop** (LOOP §2.4.4; the loop's own evaluation is host-held, R5-2) | The run stops at its next action; residual in-flight actions are *action during hold* (evidence limits, not a separate value) | passes (holds subject to host evidence, DEP-001) | Host evidence observed on a candidate |
| HS-5 | App run; **at least one held action is App-side** (an App agent turn such as Return or a summary, an App tool or harness action incl. kind (a) on a harness capability, an App file write, any action on App content such as A4 on AF-1), or — for a kind (b)/(c) checkpoint only — the declaration has no held-actions element or does not show host operations only (conservative default; R7-3). An A5 or kind (a) checkpoint with no held-actions element takes its derived held actions (the governed operation(s); the held call; WD-v0.5 §4.3.1, EXEC-v0.3 §3.6) and is valued by them | **not enforceable** whatever SQ-02 returns (D6; R5-10) | Nothing is stopped; actions are *action during hold* | *unsupported* ("checkpoint hold not enforceable on this surface") | Only the owner's D6 follow-up (EXEC U-E23) |
| HS-4 | App run on X; every held action is a host operation, one with unagreed exposure | **not established** | Nothing is stopped; actions are *action during hold* | *not established* | Exposure agreed (SQ-11) |
| HS-3 | App run on X; **every held action is a host operation** on the external channel (the governed operation of an A5 constraint; the call a kind (a) checkpoint holds; host operations after arrival until the act) | **not established** today (SQ-02 unanswered); → **enforced on the host route** once host-held carriage or a host hold is evidenced on a candidate; → **not enforceable** if SQ-02 is answered with no host-held route. Never assumed | Today nothing is stopped; once enforced on the host route, the host refuses the held host operations and other actions are *action during hold* | *not established* today; passes, or *unsupported* | SQ-02 answer and candidate evidence |

**Fixture classification (EXEC-v0.3 §3.6 table; WD-EX-v0.5 E8; C-v0.5 V-GR1).**

| Workflow via X (App run) | Checkpoint (declared held actions) | Value | Workflow result (EXEC §3.5 precedence) |
|---|---|---|---|
| E1 ⟨rev-A2⟩ | `CP-accept` (governed OP-C4/OP-C5) | HS-3 → **not established** | **unsupported** (any *not enforceable* decides), whatever SQ-02 returns (MT-2) |
| | `CP-check` (Return, App-side) | HS-5 → **not enforceable** | |
| E1c | `CP-check` (returning the result, App-side; no host operation declared) | HS-5 → **not enforceable** | **unsupported** |
| E1d | `CP-grant` (the held OP-C9 call) | HS-3 → **not established** (C V-GR1 corrected by R6-2) | **unsupported**, whatever SQ-02 returns; SQ-02 can move only `CP-grant` (MT-16) |
| | `CP-check` (from E1c; Return, App-side) | HS-5 → **not enforceable** | |
| L-WDEX-17 (E1d variant with `CP-grant` only) | `CP-grant` (OP-C9) | HS-3 → **not established** today | *not established* today; passes once SQ-02 is evidenced with a host-held route |
| L-WDEX-17 with its held-actions element absent | `CP-grant` (held actions derived: the held OP-C9 call, kind (a); R7-3) | HS-3 → **not established** today | By §3.5 precedence with the run's other checkpoints: L-WDEX-17 has none, so *not established* today; passes once SQ-02 is evidenced with a host-held route; *unsupported* if answered with none |

The same workflows in the host on E: every checkpoint **enforced by the host
loop**, check passes (MT-1). An author who needs a checkpoint enforceable from
the App keeps **all its held actions on host operations** (R6-1; CA WR-11).
The person may still start an unsupported run; HP-3 and HP-4 apply as best
effort and never change a value; every governed action while a checkpoint
waits is recorded as *action during hold* (RS R11, with turn initiator, R6-5).

---

## 3. OUT-001 — New-host integration checklist (HI §10 restated against these contracts)

**How to use it.** For each HI §10 item, a host that wants to claim the
corresponding receiving obligation (a) **supplies** the listed contribution
and (b) **answers** the listed questions with identified evidence. A reviewer
marks each check *answered with evidence*, *answered without evidence*, *not
answered* or *not applicable*. The checklist adds no human checkpoint and
authorizes no App implementation of a host (HI §10 closing sentence). For
SWBPIPE the questions are carried by RELAY-v0.3 (SQ-nn); for any other host
they are the same checks.

### HC-0 Preconditions for any claim

| Check | Supply / answer | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-0.1 | Which identified host candidate (source revision, build, configuration, date)? | CA §7.1; XT §2 IN-02; SQ-27 (a) | A candidate identity; otherwise *illustrative* only |
| HC-0.2 | Which operation(s), check, acting surface and autonomy does the first activity use? | CA §2.2, §2.5; SQ-04; `UNRESOLVED{OI-021}` | The owner's OI-021 selection; until then FX-PIPE-01 only |
| HC-0.3 | How will host answers and evidence reach the App, with custody? | RELAY §4 ledger; CA §7.2; SQ-27 (c) | A recorded return with source, revision, date and custody |

### HC-1 Describe every operation once in a capability catalog (HI §2; row 1)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-1.1 | Does every person-available operation — reads, changes, host checks, undo — have exactly one entry in an identified catalog edition, and how is an edition addition published? | C §2; C §10.4 V-ED1 | Edition identity; entry comparison; SQ-26 |
| HC-1.2 | Does each entry state all nine elements as meanings, with target identification explicit and every error carrying an effect statement? What happens on an entry-version mismatch? | C §3, §3.3, §4.2 | Entry texts (SQ-04 (a)); SQ-18 (e) |
| HC-1.3 | Are unavailable / not permitted / channel not enabled / not exposed / error distinct, each with evaluated basis, never an empty success, with the same unavailable reason on every surface? | C §4.1–§4.4; ACT §6 | Three-surface comparison (C §10.6 pattern) on the candidate |
| HC-1.4 | Does each entry carry a class with its policy basis; are reserved entries always offered where exposed? | C §3.1, §2 invariant 5; ACT §8 | SQ-05 (a) |
| HC-1.5 | Is exposure declared per surface, independently of class? | C §3 element 9 | SQ-11 |
| HC-1.6 | Do reads return the same content and standing marks, with host checks named and based and findings never shown as checks? | C §6; AS §8; ACT §9 | Side-by-side read; SQ-24 |
| HC-1.7 | For each surface, is each element generated, checked or hand-built? | C §8; XT §5.1 | SQ-12. **No "generated from or checked against one catalog" claim while any cell is *unagreed*; no automatic-extension claim while `UNRESOLVED{OI-003}`** (SQ-26; XT §5.2) |

### HC-2 Route every change through one validation and application path (HI §4; row 2)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-2.1 | Do all actors submit to the same route, channel recorded as attribution only? | P §2; ADAPTER RP-1 | Equivalent-request comparison across channels |
| HC-2.2 | Is treatment resolved at validation and again at application, from the grant actually in force; is a direct request without an effective direct treatment *not permitted*, never converted? | ACT §5.3, §6; P §2 | SQ-05 (d)(h) |
| HC-2.3 | Do results map to P §9 and C §4.1, distinct from transport status (outcome unknown for submissions only)? | P §9; ADAPTER §4.5 | SQ-09 |
| HC-2.4 | Does the embedded loop check catalog schema before host validation, never execute malformed or truncated calls, and hold undispatched siblings at a checkpoint? | LOOP §6, §7, §2.4.4 LH-0 | **SQ-31**; SQ-29 (c) |

### HC-3 Return a basis with every read; check it on every change (HI §3–§4; row 3)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-3.1 | Does every read return the five-element basis descriptor; what starts a new generation? | C §5.1–§5.2 | SQ-07 (a)(b) |
| HC-3.2 | Does every row/object carry a subject content identity with method; what does it cover; what identity follows a return to prior content? | C §5.3; RS §7 | SQ-03 (a)(b)(e) |
| HC-3.3 | Does a submission keep the originally inspected basis; which cited bases must hold for multi-read reliance? | C §5.4; P §3.2, §12 | M3-CP on the candidate (P §11); SQ-07 (c)(g) |
| HC-3.4 | Is staleness per item against relied-on targets, with both bases; does de-duplication precede the basis check; is retargeting impossible; are non-mutating operations never refused stale? | P §5, §6; C §5.4 | CA-4 observed; SQ-07 (d)–(f)(h); SQ-08 (b) |

### HC-4 Mark origins; offer undo; show proposals in the host's own views (HI §4; row 4)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-4.1 | Which origin elements are recorded and verified; can the App read the origin mark? | P §3.3; ADAPTER §5.4 | SQ-14 |
| HC-4.2 | Who mints the proposal identity; is it readable by identity; is acceptance per change item; are there operation-specific withdraw/reject rules? | P §3.1, §4.3; ACT §7 | SQ-08 (a)(d); SQ-03 (c); SQ-05 (g) |
| HC-4.3 | Does each direct application carry receipt, origin mark, undo route and later-check route, and report resulting objects? | P §4.4, §9; AS §7 | SQ-03 (d); SQ-10 |
| HC-4.4 | Is undo a change through the one route whose receipt records what it reverses? | P §4.5; ACT P-03 (R3-4) | SQ-10 |
| HC-4.5 | What domain evidence shows one effect per item on repeated submission, including across a restart? | P §7 | SQ-08 (c)(e) |
| HC-4.6 | Do the host's own views show the P §8 information with "accept", never "approve"? | P §8; PANEL §3.3, §4 | SQ-22 |

### HC-5 Name the reserved human acts and bind them to content (HI §5, §9; row 5)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-5.1 | Which reserved-act list does the host name and enforce; which operation-specific additions? | ACT §3, §8.3 | SQ-05 (b)(c); D2 does not show host adoption |
| HC-5.2 | Is there a stable capture-evidence reference per captured act and for act-declined events, readable and durable; is any act captured through elicitation or an agent-mediated prompt? | ACT §2.6, §4.5; RS §6; EXEC §5 (CAP-6) | **SQ-01**. Without it no host-content checkpoint reaches *performed* and no act-recording claim is made |
| HC-5.3 | Does any host operation store an agent's faithful record, and does it meet R2-2? | ACT P-02; RS HA-9 | SQ-21 |
| HC-5.4 | Do acts lapse visibly when content changes, with supersession, stale-after-acceptance and reversal distinct? | ACT §2.5; RS §7; AS §8 | SQ-23; SQ-03 |
| HC-5.5 | Does each run leave a compact record with the host project, linking receipts rather than copying them? | RS §4 (R1–R14); V4-HI-70/71 | SQ-19 (b)(c) |
| HC-5.6 | Will the host accept any App-captured act on host content? | EXEC §5 CAP-1 | SQ-25 |

### HC-6 Choose autonomy defaults for consequential operations (HI §6; row 6)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-6.1 | For each consequential class, what default, visible and changeable by the person, recorded per run? | ACT §5, §7; AS §3; RS R6 | SQ-05 (d)(e)(i) |
| HC-6.2 | For model changes, is the default *propose* with row / multi-row / batch acceptance, widenable only by the person within ACT §5.6? | ACT §7, §5.6 | SQ-05 (a)(c) |
| HC-6.3 | For an A5 checkpoint, does the host hold the constraint (verified against its own declaration copy, or from a host-held declaration or run association), answer a direct request *not permitted* naming it, and hold "before dispatch" checkpoints itself per surface? After a checkpoint arrives on an observed output or host outcome, does it refuse the run's further host operations until the act, per surface? | ACT §4.4, §4.6; P §3.3, §4.4; EXEC §3.6 | **SQ-02** (incl. (d), (f)). Until answered, checkpoints on X whose every held action is a host operation are *not established*; any App-side held action → *not enforceable* whatever the answer (§2.14) |
| HC-6.4 | Does the host present grant states including a policy default and a refused setting; will it join a consequence vocabulary? | AS §3; ACT U-02 | SQ-05 (e)(f) |

### HC-7 Select reusable panel/components where they fit; implement the loop/catalog/model connection under the host's ownership and data boundary (row 7)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-7.1 | Does the embedded loop preserve the four-subject boundary and stay separate from the App's Codex path? | LOOP §1, §2 | Loop observation on the candidate |
| HC-7.2 | Which model interface and servers; how are tool calls, "no arguments" and truncation expressed; are exchanges recorded as fixture basis? | LOOP §4, §7, §11; DEP-05-01-024 | **SQ-29** |
| HC-7.3 | Does the native layer enforce the endpoint, hold the key outside the script, default to local, never fall back to cloud, and refuse model-requested redirects? | LOOP §5 (NW-1…NW-7; MS-01…MS-11) | **SQ-30**; V4-EXM-23 observation (DEL-09-07, outside D1) |
| HC-7.4 | Does the host interface stay usable during long streams and large reads; can a stream be cancelled? | LOOP §8 | **SQ-32**; RS-1…RS-4 observations |
| HC-7.5 | Does the panel provide the four interactions plus checkpoints (with hold support) and the active grant, with results in host tables and no agent-private surface? | PANEL §3, §4, §5 | SQ-22; SQ-23; SQ-17 (c) |
| HC-7.6 | Which reusable component, if any, with agreed responsibility; where will loop, panel, persistence, hold machine and check live? | PANEL §6; LOOP §10; WD §9 | OI-014 agreement; SQ-20 (informational). No reuse presumed |

### HC-8 Write the host's own workflows and skills; test them in the Chirality App (row 8)

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-8.1 | Does each host workflow declare inputs, required tools by catalog identity, closed-list checkpoints with their held actions (a grant checkpoint always naming its setting content, R5-3; R6-1), outputs and evidence? | WD §3, §4 | SQ-18 (a) |
| HC-8.2 | Does the host carry full identity with derived-from and holding library, and list an App-carried workflow unadapted? | WD §6; EXEC §6.2 | SQ-17 (a); SQ-18 (a) |
| HC-8.3 | Can the host read the App's declared part, evaluate required tools and hold support for host runs, and report *unsupported* explicitly? | WD §4.2.4, §4.3.8; EXEC §3 | SQ-17 (b)(c) |
| HC-8.4 | Is an adaptation a new revision with host origin, derived-from and a checkpoint comparison, inheriting no identity or act? | EXEC §6.4, §6.6; WD §6.4 | SQ-18 (b)(c) |
| HC-8.5 | Can the host loop record per-turn guidance source and content identity; how does the single seat map to role meanings? | HOSTING §8.2; RS R3, R5a; WD §5 | SQ-19 (a)(d); otherwise *supplied* **unknown** |
| HC-8.6 | Can a host revision be relayed, opened read-only and refined in the App? | EXEC §6.5; CA §8 W14-09 | Needs DEL-02-02 (outside D1); no V4-EXM-14 completion claim in this undertaking |

### HC-9 Optionally expose the catalog to external agents (HI §7; row 9) — only if offered

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-9.1 | Does the host have an enablement facility that captures the person's A13 (enable and disable) with a readable capture-evidence reference? Is access off by default, with *channel not enabled* when off? | ACT §2.6; ADAPTER §3 | **SQ-28** (gates the whole channel); SQ-13. App-side configuration is never A13 evidence |
| HC-9.2 | Which seam; derived from the catalog; mapping supplied? | ADAPTER §4.1, §9; C §8 | SQ-12 |
| HC-9.3 | Same route, validation, grant and reserved acts; channel rule stated as a governing treatment? | ADAPTER §6 | SQ-06 |
| HC-9.4 | Strictly local endpoint; sandbox needs? | ADAPTER E-7, §3.5 | SQ-15 |
| HC-9.5 | Does the host restrict its own channel by model destination, and how is a refusal reported? | ADAPTER §3.4; HOSTING §8.3; B-6 | SQ-16; the App applies no gate (D5) and records/shows the destination (INTEGRATION) |
| HC-9.6 | Are origin, constraint, grant and proposal identity host-held or carried, and with which assurance? | ADAPTER §5; P §3.3 (R5-2) | SQ-02; SQ-08; SQ-14 |

### HC-10 Where a connector is selected, define its receiving/qualification and unavailable paths; stage the later Domains increment (HI §8; row 10) — only if selected

| Check | The host supplies / answers | Receiving definition | Evidence before a claim |
|---|---|---|---|
| HC-10.1 | Is the connector selected; if not, is its absence shown without implying empty work, readiness or permission? | HI V4-HI-62; CA §6 | Selection statement; the first activity needs neither PEC nor Domains |
| HC-10.2 | PEC: which qualified/released coverage is relied on, adopted by the consumer? | DEL-07-01/07-02 SoWs (outside D1); HI V4-HI-61 | 03-04/TBD-007 owners' answer |
| HC-10.3 | Domains (later): admitted sources, query interface, research workflow, approval route? | DEL-08-01/08-02 SoWs (outside D1); HI §8.1 | 03-04/TBD-008, TBD-009 owners' answers; no initial gate |

---

## 4. OUT-003 — Completeness checks and recorded comparison

**Candidate examined:** DEL-03-04/GUIDE-v0.2 (R7 in-place state) against the inputs at
the R7 working state (post-2f42fba02) listed in the header. **Evidence standing:** *illustrative*
(definition completeness only). No result below is product, host, delivery,
adoption or joined-witness evidence.

### 4.1 Check results (rerun at the R7 in-place state)

| Check | What is compared | Result | Notes |
|---|---|---|---|
| CC-1 | Every row of the SoW minimum receiving map has a matrix home | **pass** — 10/10 (§2.1–§2.10) | Rows 9, 10 conditional (REQ-001) |
| CC-2 | Every obligation in each row's "required evidence" column has a matrix line | **pass with limits** — table 4.2 | Row 8 role supply and row 10 rely on SoW meaning only (G-1, G-2) |
| CC-3 | Every HI §10 item has a checklist entry | **pass** — 10/10 (HC-1…HC-10) plus HC-0 | HC-9, HC-10 conditional |
| CC-4 | Every relay question SQ-01…SQ-32 (with its sub-questions) has at least one matrix home | **pass** — 32/32 (table 4.3); the nine R5-10 sub-questions (SQ-03 (e), SQ-05 (g)(h)(i), SQ-07 (g)(h), SQ-18 (e), SQ-19 (d)) and the R7-2 sub-question SQ-02 (f) each have a home | SQ-04, SQ-27 cross-cutting (G-5) |
| CC-5 | Every receiving-map obligation that needs host evidence has an SQ, or a stated reason why none is asked | **pass** — row 7 host evidence now asked in SQ-29…SQ-32; WD U-10 is in RELAY "Not included" with its D1 reason; enforcement of checkpoints with App-side held actions is not a host question (owner follow-up U-E23, G-8; R6-1) | G-3 closed |
| CC-6 | Every TBD-001…TBD-009 carried with literal owner and point of need | **pass** — §2.13 (plus the two D6 rows) | TBD-001/002 SoW text still reads open (F-5) |
| CC-7 | Every REQ-008 excluded act maps one-for-one to its owner | **pass** — X-01…X-19 (§2.12) | The registered boundary-owner checker (VER-007) **not run** |
| CC-8 | Every consumed Design file is cited in the matrix | **pass** — 16/16 inputs (the R7 working-state set has 17 non-generated Design files including this guide, V3-B m-12) | SPIKE cited through M9.3 and §2.11 |
| CC-9 | R4, R5, R6 and R7 rulings that change a relied-on statement are applied | **pass** — §5 | R6-2, R6-4 and R6-5 items owned by other files verified at the candidate (C V-GR1, LOOP LH-n, CA/RELAY/XT D5 wording); R7-1…R7-4 items owned by other files read at the R7 working state (ADAPTER GC-5; RELAY SQ-02 (f), answer options (i)–(iv), LH-0; WD §4.3.1 derivation; C/RS V-GR1 via X *unsupported*) |
| CC-10 | No line claims relay, answer, commitment, delivery, adoption, host behavior, a human act, an App hold it cannot enforce, a selected transport or placement | **pass** — confirmed independently by **V4-B** (first independent review of GUIDE-v0.2: no over-claim; fit as the integrated index; defects m-7, m-9 only, both addressed here). V3-B reviewed v0.1 | The R6 and R7 in-place states are self-reviewed (F-9) |
| CC-11 | Conflicts between inputs that affect a guide statement | **2 remain, none changing a guide statement** — G-6, G-7 (SoW wording). **Resolved at the candidate:** V4-B MAJOR-1 (C V-GR1 `CP-grant` via X) by R6-2; G-9 (ADAPTER §12 now RELAY-v0.3); CA-H surface qualifier (F-11); **G-10 closed** — RELAY no longer uses "LOOP HS-0" outside retirement notes and change rows (SQ-31 (d) at `2f42fba02`; SQ-31 "App assumes meanwhile" and the §3 map by R7-4 m-2); **G-11 closed** — WD-v0.5 I-4 carries the R6-3 per-value qualification (fixed at `2f42fba02`). Also resolved by R7: ADAPTER GC-5 run-halt exception (R7-1); the absent-held-actions reading (R7-3; WD, WD-EX, EXEC and §2.14 agree) | None blocks the owner's relay of RELAY on this check |

### 4.2 Receiving-map evidence obligations → matrix lines

| Map row | Obligations named in the SoW's "required evidence and point of use" | Matrix lines |
|---|---|---|
| 1 Catalog and read meaning | identity/version; purpose; input schema; preconditions/reasons; effects; result/standing; errors; adopted class; generated versus checked/adapter portions | M1.1–M1.8 |
| 2 Single route | named route; validation/outcome/error comparison and host evidence; no second agent route | M2.1–M2.5 |
| 3 Basis | basis elements (canonical content hash received as identity + method, R-6); original basis trace; stale refusal; no silent substitution | M3.1–M3.6 |
| 4 Origin, undo and proposal presentation | origin; undo; lifecycle and receipts; stale/refusal; unchanged targets; duplicate-one-effect (host obligation to be evidenced, R-7); unknown outcome | M4.1–M4.7 |
| 5 Human acts and compact records | actor/subject/content evidence; recorder; visible lapse; run links workflow/version, conversation, settings, requests/outcomes, receipts, acts, model | M5.1–M5.8 |
| 6 Autonomy | visible changeable settings per run; conservative defaults; SWB proposal default and widening; checkpoints still wait; unresolved classes open | M6.1–M6.6; §2.14 |
| 7 Loop and panel | allocation; endpoint/key boundary; local default and local-data constraint; malformed-call and schema-before-domain validation; responsiveness; host views, no agent-private surface | M7.1–M7.8 (SQ-29…SQ-32) |
| 8 Host methods and roles | method and compatibility; missing-tool handling; actual checkpoint act; source-preserving adaptation; tested/refined in App; additive role guidance | M8.1–M8.7; §2.14 (role supply outside D1: G-1) |
| 9 Optional external catalog access | disabled/unavailable path; enabled same semantics; endpoint and candidate evidence; historical no-external-apply not a universal ruling | M9.1–M9.8 |
| 10 Selected connectors | PEC and Domains conditions; independent absent/limited paths | M10.1–M10.3 (G-2) |

### 4.3 Relay questions → homes

| SQ | Topic | Matrix home(s) | Checklist |
|---|---|---|---|
| SQ-01 | Capture-evidence reference (P1) | M5.3, M5.8, M8.4, M9.8 | HC-5.2 |
| SQ-02 | Governing constraint; host holds (P1), (a)–(f); (f) refusal of the run's further host operations after an arrival until the act (R7-2) | M6.4, M7.6, M8.4, M9.5, §2.14 (HS-3) | HC-6.3, HC-9.6 |
| SQ-03 | Content identities (a)–(e) | M3.2, M4.2, M4.3, M5.5 | HC-3.2, HC-4.2, HC-4.3, HC-5.4 |
| SQ-04 | First activity, check, environment | M1.2, M1.5, M1.8 | HC-0.2, HC-1.2 |
| SQ-05 | Policy (a)–(i) | M1.4, M2.2, M4.2, M5.2, M6.1–M6.3, M6.5, M7.7 | HC-1.4, HC-2.2, HC-4.2, HC-5.1, HC-6.1, HC-6.2, HC-6.4 |
| SQ-06 | Direct on the external channel | M9.4 | HC-9.3 |
| SQ-07 | Basis and staleness (a)–(h) | M3.1, M3.3, M3.4, M3.5 | HC-3.1, HC-3.3, HC-3.4 |
| SQ-08 | Proposal identity, repeated submission | M3.4, M4.2, M4.5, M9.5 | HC-3.4, HC-4.2, HC-4.5, HC-9.6 |
| SQ-09 | Outcome statements, unknown | M1.3, M2.1, M2.3, M4.3, M4.6 | HC-2.3 |
| SQ-10 | Undo, publication | M4.3, M4.4 | HC-4.3, HC-4.4 |
| SQ-11 | Exposure per surface | M1.3, M1.7, M8.3 | HC-1.5 |
| SQ-12 | Seam and derivation | M1.1, M1.6, M1.7, M2.5, M9.3 | HC-1.7, HC-9.2 |
| SQ-13 | Enablement behavior | M9.1, M9.2 | HC-9.1 |
| SQ-14 | Origin, caller identity | M4.1, M9.5 | HC-4.1, HC-9.6 |
| SQ-15 | Locality, sandbox | M9.6 | HC-9.4 |
| SQ-16 | Host restriction by destination | M9.7 | HC-9.5 |
| SQ-17 | Receiving App workflows | M7.7, M8.1–M8.3, M8.5 | HC-7.5, HC-8.2, HC-8.3 |
| SQ-18 | Adaptation, library identity, version (a)–(e) | M1.2, M8.1, M8.2, M8.5, M8.7 | HC-1.2, HC-8.1, HC-8.2, HC-8.4 |
| SQ-19 | Run records, supplied guidance, seat mapping (a)–(d) | M5.6, M8.6 | HC-5.5, HC-8.5 |
| SQ-20 | Placement (informational) | M7.1, M7.6 | HC-7.6 |
| SQ-21 | Faithful-record operation | M5.4 | HC-5.3 |
| SQ-22 | Proposal views | M4.7, M7.7 | HC-4.6, HC-7.5 |
| SQ-23 | Lapse and related display | M5.5, M7.7 | HC-5.4, HC-7.5 |
| SQ-24 | Findings location | M1.5 | HC-1.6 |
| SQ-25 | App capture on host content | M5.3 | HC-5.6 |
| SQ-26 | Extension-trace operation; edition event | M1.1, M1.6 | HC-1.1, HC-1.7 |
| SQ-27 | Candidates, evidence, relay | M3.6, M8.7, M9.8; evidence column of every row | HC-0.1, HC-0.3 |
| SQ-28 | A13 enablement facility (gates the channel) | M5.3, M9.1, M9.2, M9.8 | HC-9.1 |
| SQ-29 | Host-loop model interface, fixture basis | M2.4, M7.2 | HC-2.4, HC-7.2 |
| SQ-30 | Endpoint and key boundary | M7.3 | HC-7.3 |
| SQ-31 | Malformed calls, validation order, sibling hold | M2.4, M7.4, M7.6 | HC-2.4 |
| SQ-32 | Responsiveness | M7.5 | HC-7.4 |

### 4.4 Remaining gaps and conflicts

| # | Kind | Gap or conflict | Where | Proposed disposition (owner) |
|---|---|---|---|---|
| G-1 | Missing definition (outside D1) | Additive role supply (DEL-02-04) and the App act control (DEL-01-04) have no Design file; M8.6 and M5.3 rest on SoW meaning plus HOSTING S-6 and EXEC §5 | M5.3, M8.6 | None in this undertaking |
| G-2 | Missing definition (outside D1) | PEC and Domains receiving not started | M10.1, M10.2 | By design (conditional) |
| G-5 | Map shape | SQ-04 and SQ-27 belong to no single row | HC-0; M1.8 | Cross-cutting preconditions; no SoW change |
| G-6 | SoW wording | Row 7 "local-server default and local-data constraint" does not separate the host loop (V4-HOST-02, SQ-30) from App conversations (D5, SQ-16) | M7.3, M9.7 | Guide applies each to its path; C1 wording note |
| G-7 | SoW wording | "Canonical content hash" and "duplicate-one-effect" predate R-6/R-7 | M3.1, M3.2, M4.5 | Guide carries refined meanings; C1 wording note |
| G-8 | Owner-open, no host route | Checkpoints with any App-side held action are *not enforceable* in App runs whatever SWBPIPE answers; E1, E1c and E1d via X are therefore *unsupported* (R6-1). Only the owner's D6 follow-up can change this | M8.4; §2.14 | Owner (EXEC U-E23), before any App-side workflow with an App-side held action is offered as supported |
| G-10 | Label currency (RELAY) — **closed (R7)** | RELAY-v0.3 SQ-31 (d) and §3 said "LOOP HS-0"; LOOP renamed it **LH-0** (R6-4). Fixed in SQ-31 (d) at `2f42fba02` and in SQ-31 "App assumes meanwhile" and the §3 map by R7-4 m-2 | M2.4; HC-2.4 | None |
| G-11 | Wording (WD) — **closed (R7 refresh)** | WD-v0.5 I-4 re-hold text "the run stops at its next action boundary" was unqualified; it now carries R6-3's per-value qualification (fixed at `2f42fba02`), as I-9 and §4.3.8 do | M8.4 | None |

Closed since v0.1: **G-3** (SQ-29…SQ-32), **G-4** (W9 files swept under R4/R5: RELAY SQ-02, SQ-16; CA §2.2; XT IN-14, IN-25), **G-9** (ADAPTER §12 re-headed RELAY-v0.3 under R6), **G-10** and **G-11** (closed at the R7 working state; rows kept above for traceability).

---

## 5. R4 and R5 rulings applied

| Ruling | Effect in this guide | Applied at |
|---|---|---|
| R4-1 / R5-4 | D5 attribution split; destination per turn, requested/effective apart, run-level set | B-6; M5.6; M9.7; HC-9.5 |
| R4-2 / R5-10 | D6 deferral; host-operation versus App-side held actions (R6-1); HP-4 | B-7; M6.4; M8.4; M9.5; §2.13; §2.14; G-8 |
| R4-3, R4-4, R4-5, R4-6, R4-7 | Re-hold, no resumption, capture after arrival, A12 supersession when established, mixed items | M5.3, M5.5, M5.8, M8.4 |
| R4-8, R4-21 | *Unsupported* reason; harness kind (a) not holdable | M8.3; §2.14 |
| R4-11 | RS additions (R14, §4.1) | M5.6 |
| R4-12, R4-13 | Elicitation not act evidence; App-side configuration never A13; ACT §2.6 capturing surfaces | M5.3; M9.1 |
| R4-14 / R5-2 | Carriage assurance; only host-held counts; host loop host-held; App-assured unavailable | B-9; M4.1; M6.4; M9.5 |
| R4-15, R4-16 | Unverified author identity; *channel not enabled* reporter | M4.1; M1.3 |
| R5-1 | Four hold-support values; EXEC §3.6 HS-1…HS-5 | §0; §2.14; M7.6; M8.3; HC-6.3; HC-8.3 |
| R5-3 | Grant-setting subject always declared | M8.4; HC-8.1 |
| R5-5 | Undo re-holds; never "action during hold"; never re-holds A5 | M4.4 |
| R5-6 | Person's own A1/A2 are R7 operations | M5.1 |
| R5-7 | V-GR1 variant; owner-visible cost under U-E4 | M8.4 |
| R5-8 | No App-run "held after observation" or "run stops" | §2.14 |
| R5-9 | Citation and staleness pass (this revision) | Whole file |
| R6-1 | Hold support by held actions; order HS-1, HS-2, HS-5, HS-4, HS-3; E1/E1c/E1d via X unsupported; E1d `CP-grant` not established | §0; B-7; §2.13; §2.14; M8.1; M8.4; HC-6.3; HC-8.1; G-8; F-10 |
| R6-2 | C V-GR1 `CP-grant` via X *not established* (owned by C) | §2.14 fixture table; CC-11 |
| R6-3 | What "held" means per value | §0; §2.14; M8.4 |
| R6-4 | LOOP LH-0…LH-4 | M2.4; M7.6; HC-2.4; G-10 |
| R6-5 | Pinned hashes to `375c3970c`; CC-11 and F-11 refreshed; CA/RELAY byte states; RS R11 turn initiator | Header; §2.14; §4.1; §6 |
| R7-1 | ADAPTER GC-5: a kind (b)/(c) run halt is HS-5 only when its held actions include an App-side step (owned by ADAPTER) | §2.14 (unchanged; already so); CC-9; CC-11 |
| R7-2 | RELAY SQ-02 (f) (host refusal of the run's further host operations after an arrival until the act) and answer options (i)–(iv) (owned by RELAY) | M8.4; HC-6.3; §4.3; CC-4 |
| R7-3 | Held actions of an A5 or kind (a) checkpoint are derived when the element is absent; the HS-5 default covers kind (b)/(c) only; L-WDEX-17-absent → HS-3 *not established* | §0 header note; §2.14 HS-5 row and fixture table |
| R7-4 | m-6 D6 follow-up point of need by App-side held action; m-1 re-pin at the R7 working state, CC-11 refreshed (G-10, G-11 closed). m-2…m-5 and m-8 owned by other files | Header; §2.13; §4.1; §4.4; §6 |

---

## 6. Findings (reported; scope unchanged)

| # | Where | Finding | Proposed disposition |
|---|---|---|---|
| F-1 | Input count | 16 inputs consumed; the R7 working-state set has 17 Design files including this guide | Recorded (V3-B m-12) |
| F-4 | Dependencies.csv (DEP-03-04-005…020) | No rows to DEL-01-01, DEL-09-06 (RELAY SQ ids cited throughout) or DEL-09-09; only DEL-03-02 carries a mirror (DEP-03-02-021) | Register repair at closeout C1 |
| F-5 | SoW TBD-001, TBD-002; REQ-004 | Still read OI-001/OI-002 as open despite DECISION-1 D2/D3 | C1 pointer |
| F-6 | G-6, G-7 | SoW map wording predates R-6/R-7 and D5 | C1 wording note |
| F-7 | D1 | Rows 8 and 10, App act capture and V4-EXM-14 completion depend on deliverables outside this undertaking | Completeness limits (G-1, G-2; CA F-1) |
| F-8 | C §8 | Every three-surface cell *unagreed*; no host can yet claim HC-1.7 | Consistent with OI-003 |
| F-9 | Review | V3-B reviewed v0.1 and V4-B reviewed v0.2 independently (MERGE AS DRAFTS; m-7, m-9 applied here). The R6 and R7 in-place refreshes are self-reviewed, and the VER-007 checker has not been run | Run the checker in C1; a light re-read of the R6 changes if the coordinator wants one |
| F-10 | EXEC §3.6; WD-EX E8 | The first activity's fixture workflows E1, E1c and E1d, run from the App via X, are *unsupported* on hold support whatever SQ-02 returns (their `CP-check` holds an App-side Return step, R6-1). The embedded route (CA/E) is the only route on which they pass hold support in this increment | Carry to the owner with U-E23; relevant to the OI-021 choice of acting surface (CA §2.2) |
| F-11 | CA-v0.3 §2.3 CA-H | **Closed (R6-5; V4-B m-9 (a)).** CA-H now reads "The run holds (on E; in App runs only as hold support allows, S-13)" and records *action during hold* otherwise | None |
| F-12 | Identifier collision | "TBD-007" differs between this SoW (OI-022) and DEL-03-03's (MCP/CLI) | Prefixing rule (§0) |
| F-13 | G-9 | **Closed:** ADAPTER §12 now reads RELAY-v0.3 | None |
| F-14 | G-10, G-11 | **Closed (R7).** The residual label (RELAY "LOOP HS-0") and wording (WD I-4) lags after R6 are fixed (R7-4 m-2; WD I-4 at `2f42fba02`) | None |
| F-15 | Version identity | CA-v0.3 now has four byte states and RELAY-v0.3 five (V4-B m-7; R7); the guide pins the latest, at the R7 working state (post-2f42fba02). A file about to be relayed is identified here by sha256, not by version label alone | Coordinator: consider v0.3.1 or recording the final hash at relay |

Closed since v0.1: F-2 (RELAY P8 added), F-3 (W9 files swept), F-11 of v0.1 (re-pointed to the final set).

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-021}` first connected operation, check, autonomy, environment, acting surface; operation-specific reserved additions (03-04/TBD-006; TBD-001 residue) | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution; host evidence before connected-journey integration/examination and fallback-replacement decision | M1.8, M5.2, M6.5 open; examples are FX-PIPE-01 fixture subjects |
| `UNRESOLVED{OI-003}` automatic catalog extension (03-04/TBD-003) | Owner with host contract owner | Before claiming extension capability or fixing its acceptance criterion | M1.6 owner-open; HC-1.7 claim barred |
| `UNRESOLVED{OI-013}` per-host loop placement and persistence (03-04/TBD-004) | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Outcomes only (M2.4, M5.6, M7.1, M7.6, M7.8) |
| `UNRESOLVED{OI-014}` shared contract/component placement (03-04/TBD-005) | App/shared contract owners | Before structural/production contract allocation | No common component presumed |
| 03-04/TBD-007 (OI-022) PEC | App consumer owner and PEC owner | Before operational consumer reliance | M10.1 conditional; not designed |
| 03-04/TBD-008 (OI-023) Domains receiving | Owner with Domains/SWB/App receiving owners | Before later Domains-enabled design increment | M10.2 conditional |
| 03-04/TBD-009 (OI-026) Domains provider | Owner with App/Domains/SWB definition owners | Before allocating provider production and committing integration | M10.2 conditional |
| `UNRESOLVED{D6}` checkpoints in App runs whose every held action is a host operation (EXEC U-E1; HS-3) | Owner (DECISION-2), on the SQ-02 answer | Before any App-side positive hold case; before the App fixes its realization family | HS-3 *not established* |
| D6 follow-up: checkpoints with any App-side held action in App runs (EXEC U-E23; HS-5) | The owner | Before any such workflow is offered as supported | HS-5 *not enforceable* → *unsupported* (G-8, F-10) |
| Every SQ-01…SQ-32 answer (DEP-001) | SWBPIPE outside implementation owner, through the human relay | As stated per question in RELAY | Every "relay pending" line stays *prepared* |
| 03-03/TBD-007 MCP-versus-CLI and related choices (OC-1…OC-12) | App external-host integration owner with external host owner | Before the App receiving implementation depends on the interface; before DEL-09-09 qualification | Row 9 selects nothing |
| ACT U-02 consequence vocabulary; ACT U-03 multi-row A4 purpose; EXEC U-E4 SP-6 versus counting prior acts | DEL-04-01 with host policy owner; DEL-04-01 with the owner; the owner with DEL-02-01/DEL-04-01 | Before class assignment; before lapse/re-hold fixtures run | M1.4, M5.5, M6.1, M8.4 owner-open |
| DEP-05-01-024; LOOP N-OPEN-1…3, T-OPEN-1, R-OPEN-1 | Supplier UNKNOWN / App/shared embedded-integration owner with SWBPIPE owner; the owner for R-OPEN-1 | At loop fixture and conformance use; before endpoint cases; before responsiveness claims | M2.4, M7.2–M7.5 await SQ-29…SQ-32 |
| Register and SoW-text findings F-4, F-5, F-6, F-12 | Register owner / closeout C1 | C1 | None on content |
| VER-007 checker run; optional re-read of the R6 in-place changes (F-9) | App manager | Before closeout acceptance of the guide | v0.2 reviewed independently by V4-B; R6 changes self-reviewed |

---

## Verification cases

Designed, **not run**. Passing them later shows guide completeness only; they
never substitute for host conformance, a joined witness or a human act.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-G-01 Checklist coverage | Compare §3 with HI §10 items 1–10 and the ten map rows; trace each to SOW-156/SOW-187 and OBJ-004; confirm HC-9 and HC-10 are conditional | 10/10 covered; every check names its receiving definition, SQ and evidence | VER-001 (AC-001) |
| VC-G-02 Catalog/basis/route/proposal fidelity | Compare rows 1–4 element by element with C-v0.5 §2–§10 and P-v0.5 §1–§12 and HI §§2–4 | No meaning weakened or added; no wire field; no extension or joined-outcome claim; every host need names an SQ | VER-002 (AC-002) |
| VC-G-03 Acts and autonomy | Review rows 5–6 and §2.14 against HI §§5–6, §9, ACT-v0.5, AS-v0.5, RS-v0.5, EXEC-v0.3 §3.6 with illustrative cases: execution-only success (no act); fabricated act (rejected); faithful record of an evidenced decision with a named recorder; lapse; "accept" versus approval; a declared A5 checkpoint under a direct grant (host loop: *enforced by the host loop*; App via X: *not established*) | Acts distinct; faithful recording with actor ≠ recorder; four hold-support values only; no App hold claimed | VER-003 (AC-003) |
| VC-G-04 Receiving path | Walk method → tool → checkpoint → record → loop → panel through rows 7–8 with WD, EXEC, LOOP, PANEL, RS, HI §10 and A §§4–5 | Receivers named; identity preserved; host-loop network constraint carried (SQ-30); OI-013/OI-014 open; SWB construction external | VER-004 (AC-004) |
| VC-G-05 Connectors | Inspect row 10 and HC-10 against HI §8, §8.1, DEP-002/DEP-003, V4-EXM-30/32 | Independent and conditional; nothing designed; no initial gate | VER-005 (AC-005) |
| VC-G-06 Open inputs and custody | Compare §2.13 literally with the SoW TBD rows and `Open_Issues.csv`; inspect claimed states (RELAY *prepared*; ACT P-01 without host adoption) | Owners and points of need match; nothing above *prepared*; D2/D3 shown as App/shared adoption only | VER-006 (AC-006) |
| VC-G-07 Boundary owners | Enumerate REQ-008 against §2.12 and CLM-001…CLM-006; run the registered checker; hand-inspect NOT_CHECKABLE and human/external owners | One-for-one; integration retained by DEL-03-04 | VER-007 (AC-007) |
| VC-G-08 Completeness result | Re-run CC-1…CC-11 against the identified guide candidate and its pinned inputs; record pass, fail, blocked, not run or inconclusive with revisions | Result bound to named revisions; G-1, G-2, G-5…G-9 visible or closed; no product, delivery or witness claim | VER-008 (AC-008) |
