# Intake map — SWBPIPE answers traced into the App v4 definitions (I2)

- **Run / node:** APP-V4-SWBPIPE-INTAKE-20260928, node **I2** (one Type 2 TASK
  executor; Claude Code `Agent` subagent; parent HELP_HUMAN; no delegation).
- **Date:** 2026-09-28.
- **Standing:** an intake **map and proposal** for the I3 R8 rulings. It
  decides nothing, edits no Design file, and claims no SWBPIPE join, witness,
  commitment or adoption (DECISION-3). Every SWBPIPE statement below is quoted
  as SWBPIPE's *answer about its current state*, with its SWBPIPE standing
  label; items SWBPIPE marks OWNER DECISION stay open.
- **Candidate commit:** `git rev-parse HEAD` =
  `948f4a308acf43c950504b286b1efaea4661aa62` (branch
  `claude/chirality-app-v4-60-percent-a41fd5`). The 17 Design files and the
  answers file are clean at HEAD. In the run folder, `DISPATCH.md` is modified
  and `BRIEFS.md` is untracked; both were read as working-tree bytes (hashes
  below).

## Inputs (sha256 of the bytes read)

| Input | Path (under `projects/chirality-app-v4/execution/`) | sha256 |
|---|---|---|
| Brief (working tree) | `_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/BRIEFS.md` | `3603a42856cf02cbb9f7163b4d7ec1bbbee58f6873d071142481810697d50ac6` |
| DECISION-3 | `…/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md` | `af62d252fd59bccaed4f7c3b7827323ae8bae695440c7a74abaa86951f97282f` |
| Dispatch (working tree) | `…/APP-V4-SWBPIPE-INTAKE-20260928/DISPATCH.md` | `d522ef65a49888645364594e849312077d28b1ac69ec4774f0d00c1340cee764` |
| **ANS** — SWBPIPE answers | `PKG-09_…/DEL-09-06_…/Design/RELAY_ANSWERS_SWBPIPE.md` | `64ea4e596b314cc1db93915bb3292415c7f017caa62613ec610233c3328c0689` (matches the RELAY §4 ledger and the WORK_GRAPH pin) |
| R1 | `_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/R1_RESOLUTIONS.md` | `2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4` |
| R2 | `…/APP-V4-FIRST-INCREMENT-20260928/R2_RESOLUTIONS.md` | `77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088` |
| R3 | `…/R3_RESOLUTIONS.md` | `202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf` |
| R4 | `…/R4_RESOLUTIONS.md` | `50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24` |
| R5 (read in full) | `…/R5_RESOLUTIONS.md` | `254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1` |
| R6 (read in full) | `…/R6_RESOLUTIONS.md` | `8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841` |
| R7 | `…/R7_RESOLUTIONS.md` | `1f6ab3b2355e164f803657ceae08841af92d21a821feede3800a6df861b2a1ea` |
| DECISION-1/2 | `…/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` | `a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c` |

**The 17 Design files at HEAD** (short name → path under
`projects/chirality-app-v4/execution/`, sha256):

| Short | File | sha256 |
|---|---|---|
| HOSTING | `PKG-01_…/DEL-01-01_…/Design/HOSTING_BOUNDARY.md` | `f1a23022df76fe04bfc5ad2220b57d2cdebc101f8d791b4edb163aea6109e11b` |
| SPIKE | `PKG-01_…/DEL-01-01_…/Design/PIN_SPIKE_0.158.0.md` | `0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115` |
| WD-EX | `PKG-02_…/DEL-02-01_…/Design/EXAMPLES.md` | `67e2d8ed187ad7f2134592f4f9ec744d9af33c49882d772648d42c340f531d42` |
| WD | `PKG-02_…/DEL-02-01_…/Design/WORKFLOW_DECLARATION.md` | `e55d69cbd25922efa5c25f3349c60dbdaaa7cb3e30ef14c9482fddeb18d76c66` |
| EXEC | `PKG-02_…/DEL-02-03_…/Design/EXECUTION_COMPATIBILITY.md` | `03b2fd48e14dd21ee6f29bc8e5e19221a771f788aa6c1482810b8bc0671d61e2` |
| C | `PKG-03_…/DEL-03-01_…/Design/CATALOG_AND_READ_BASIS.md` | `72ac4f0f853213f9778d69c4b3eb84d6b19d1bab80a147d98b7bc5068bb0eacf` |
| P | `PKG-03_…/DEL-03-02_…/Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | `6ab94fd10166cf78cda014a2f28ebf4726ce9f82a1c2f180044093b4bbb137e0` |
| ADAPTER | `PKG-03_…/DEL-03-03_…/Design/ADAPTER_ENABLEMENT_AND_RECEIVING.md` | `8ef2126df2b9afff0a70b36e5b4eed8492eaae0baf6563ce422d3b9d05170f5a` |
| GUIDE | `PKG-03_…/DEL-03-04_…/Design/HOST_INTEGRATION_GUIDE.md` | `7dd9a0012b1de0c6118ea0d67b55aec2f00062233b359ab8f8eb926cb4a478d6` |
| ACT | `PKG-04_…/DEL-04-01_…/Design/ACT_AND_POLICY_CONTRACT.md` | `0057593adfde52044b70ccee1a85892754c2c9a62cf452214e94d810c6c43bd9` |
| AS | `PKG-04_…/DEL-04-02_…/Design/AUTONOMY_AND_STANDING_EXCHANGE.md` | `df0e31ea7d33a3224df0b5d292d35675a55e8e325898cb28b64a1f709f7d72f0` |
| RS | `PKG-04_…/DEL-04-03_…/Design/RECORD_SEMANTICS.md` | `2939eb092839a5d6984c984a2aedcb6308f1776276314a79fa1e8edc67c36398` |
| LOOP | `PKG-05_…/DEL-05-01_…/Design/LOOP_RECEIVING_CONTRACT.md` | `0ec980b53c4dd473b365f7e8407593a218023ad2277da7680694c852808bd737` |
| PANEL | `PKG-05_…/DEL-05-02_…/Design/PANEL_RECEIVING_CONTRACT.md` | `ac47abf0974d5d68386ca713f09fc1478b205545754e8c93c74993977173ebb4` |
| CA | `PKG-09_…/DEL-09-06_…/Design/CONNECTED_ACTIVITY_CONTRACT.md` | `67dde29553325271cc3e3a08591177e6628a659966b13b4bbd93920cdf7d0aa5` |
| RELAY | `PKG-09_…/DEL-09-06_…/Design/RELAY_QUESTIONS_SWBPIPE.md` | `dfb625875400431141df784e3587f8e84f96f4c63b1f0328810449e950bcd14c` |
| XT | `PKG-09_…/DEL-09-09_…/Design/EXTERNAL_TRACE_CASES.md` | `992906e6e8e16fdfae68e02938ba9c440192f86318bb70b487270af52529dbfa` |

The generated schema and spike files under `DEL-01-01/Design/generated/` are
not counted among the 17 and carry no SQ dependency.

## Method

1. Read BRIEFS.md ("Common rules", "I2"), DECISION-3, DISPATCH, WORK_GRAPH;
   R5 and R6 in full; R2, R3, R4, R7 and DECISION-1/2 for the rulings the
   answers touch (R2-2, -4, -12, -13, -14, -15, -17, -18, -20; R3-1, -4;
   R4-1, -2, -5, -8, -13, -14, -16; R7-3, R7-4 m-5).
2. Read ANS in full, and RELAY in full (§1 priority groups, each SQ's
   "Depends" line and "App assumes meanwhile", §3 map, §4 ledger,
   UNRESOLVED).
3. For each dependent named by RELAY, located the section or case ID in its
   file at HEAD (grep plus reading of the sections that carry values: EXEC
   §2, §3.5, §3.6, §7; WD §4.3.8, §12, §13; WD-EX E1c, E1d, E2, E8; C §4.1,
   §5.3, §5.4, §10.1, §10.4; P §3.3, §4, §5, §7, §9, §12; ACT §2.6, §4.4,
   §4.6, §6, §7, §12–§14, UNRESOLVED; AS F6–F18, U-list, VCs; RS E7, E10, U-list,
   VCs; ADAPTER §2–§7, §9, §10, §12, §13.3, UNRESOLVED; GUIDE §0, §2.9, §2.13,
   §2.14, §4.3, §4.4, UNRESOLVED; LOOP §1, §2.4.4, §13, UNRESOLVED; PANEL §8,
   UNRESOLVED; CA §1, §2, §3, §6, §8, §9, §12, UNRESOLVED; XT §1–§3, §9,
   UNRESOLVED; HOSTING §6.7, U-23). Every cited ID was checked to exist.
4. Scanned all 17 files for every "not established" whose context is SQ-02,
   HS-3, a constraint or "unanswered" (script in the I2 scratch folder) and
   dispositioned each hit in Part 2.3.
5. Classified each dependent: **V** value change; **A** assumption
   contradicted or qualified; **C** confirms current text; **N** no effect
   while host joins are deferred.
6. "Changes from …" tables are history and are **not** proposed for edit; each
   edited file adds one R8 row to its latest change table (I4).

**Standard edits used below** (each row that says "STD-n" applies the text
given here, with the row's SQ id and gist substituted):

- **STD-1 Answered standing.** A ledger or standing cell that says the host
  input is *prepared* (CA §9), *relay pending* (GUIDE), *Not received* (XT §2),
  *none received* (Consumed-inputs lines) or *SWBPIPE answers … none received
  (DEP-001)* becomes: **"answered 2026-09-28 (RELAY_ANSWERS_SWBPIPE.md SQ-nn:
  ‹gist›); an answer about SWBPIPE's current state — not a commitment,
  delivery or adoption"** (ladder CA §7.2: *prepared → relayed → answered*).
- **STD-2 AWAITING INPUT answered "no/none".** Keep the token (pending ruling
  R8-Q4) and append: **"— SQ-nn answered 2026-09-28: ‹gist› (not offered);
  a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3)"**. The
  case does not move: the answer does not supply the named input (RELAY §0
  "Answer handling").
- **STD-3 HS-3 value.** "HS-3 → **not established** (SQ-02 unanswered)" (and
  equivalents "awaiting SQ-02", "today", "until SQ-02 is answered") becomes
  **"HS-3 → **not enforceable** (SQ-02 answered 2026-09-28: route (iv), none
  planned; HS-3 (c))"**; the workflow result follows EXEC §3.5 (any *not
  enforceable* → *unsupported*, reason naming every not-enforceable
  checkpoint).
- **STD-4 D6 row.** In a `UNRESOLVED{D6}` row: Owner "Owner, deferred to the
  SWBPIPE answer to SQ-02 …" → **"Owner (DECISION-2 D6): the SQ-02 answer
  (route (iv), none planned) returns D6 to the owner (R8)"**; Effect "…
  host-operation checkpoints *not established* …" → **"… host-operation
  checkpoints *not enforceable* (HS-3 (c)); App-side ones *not enforceable*
  (HS-5); every checkpointed workflow run from the App on X is
  *unsupported*"**. Point of need unchanged.
- **STD-5 DEP-001 standing.** "owner-reported building before agent-action
  integration" → append **"; SWBPIPE answers (2026-09-28): no live agent in
  the product (A-1); agent-facing work (UI-SUCCESSOR) deferred by the owner;
  draft PR #885 unmerged and deferred (A-2)"**.
- **STD-6 RELAY body is relayed text.** RELAY §0–§3 (questions, "App assumes
  meanwhile", §3 map) are the bytes relayed to SWBPIPE and are **not**
  edited; only the header status, UNRESOLVED rows and a change row are
  (pending R8-Q5).

---

## Part 1 — Per-SQ table

Columns: **Dependent** (file, section / case ID); **Cl** (V/A/C/N);
**Proposed edit** (old → new, or "add note ‹text›"). "Depends" means the SQ's
RELAY "Depends" line names the dependent. Row numbers are for counting and
citation (`SQ-nn.k`).

### SQ-01 Capture-evidence reference

**Gist.** Only **Apply** (A5, the person's review-and-apply; accept and apply
are one step, no accepted-but-not-applied state) is captured — **FACT**; on
main its receipt is session memory only, basis
`user_initiated_apply_in_local_session`, `acceptance_is_professional_approval:
false`, **no person identity, no time**, lost on restart. **DRAFT #885**:
receipt readable through CLI `status` within one controller session, still no
person or time. A4 Checked mark: **DESIGN** (DEC-104, gap G-08). A10: none
("Clear" discards without record; G-18 DESIGN). A12: no grants. A6/A7: not
software acts. Act-declined: no. Elicitation/prompt capture: **No** (agent
Apply, browser tests, computer-use clicks are not human acceptance). Storage
and actor identity: **OWNER DECISION** (PB-TBD-002; DEL-16-03).

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 01.1 | WD I-5; §4.3.4 *performed* (Depends) | C | None. "No host-content checkpoint reaches *performed*" stands; add to U-05b effect: "SQ-01 answered: no durable reference; no person identity or time even in DRAFT #885". |
| 01.2 | EXEC §4.5 SP-3; CH-3; CH-7; CH-28; U-E12 (Depends) | A | CH-28 state "host side AWAITING INPUT (SQ-01; U-05b)" → STD-2 (gist "no capture-evidence reference; Apply receipt names no person or time and does not survive restart"). U-E12 Owner "Host owner (DEP-001), **SQ-01**" → "SWBPIPE owner decision (PB-TBD-002 acceptance-record storage; DEL-16-03 actor identity; ANS §2)". |
| 01.3 | LOOP §13 Q-2; FX-C1, FX-C5, FX-C8 (Depends) | N | None (host-loop fixtures; SWBPIPE has no loop, SQ-20). |
| 01.4 | PANEL §8 Q-2; PC-07, PC-18, PC-19, PC-21 (Depends) | N | None; add to PANEL UNRESOLVED DEP-001 row effect: "Q-2 answered (SQ-01): no reference". |
| 01.5 | ACT U-04(a); FX-29; §2.6 row "A4, A5, A6, A7, A10 on host content" (Depends) | A | §2.6 row A4…A10: add note "SWBPIPE (SQ-01, 2026-09-28): only A5 is captured, as **Apply**, which is acceptance and application in one step; no A10 record; A4 is DESIGN; A6/A7 are not software acts. No capture-evidence reference is exposed." U-04 effect: "FX-29, FX-47(c) and FX-50 await input" → "(a), (c), (e) answered 2026-09-28: none offered (SQ-01, SQ-02, SQ-28); FX-29, FX-47(c) and FX-50 stay AWAITING INPUT per STD-2". |
| 01.6 | ACT §7 "Acceptance is not application"; P §4.1 states, §4.2 row "relied-on target no longer holds after *accepted*"; R2-16 display (and C V-S1, WD-EX R-14, ADAPTER XF-30, XT XC-08) | A | Add note to P §4.2 (after that row): "SWBPIPE (SQ-01, SQ-23, 2026-09-28): the host's A5 is Apply, which applies at once; a stale Apply is refused and records no acceptance, so *accepted — not applied: refused — stale* does not arise on SWBPIPE. V-S1/XF-30/XC-08 remain App receiving cases with no SWBPIPE counterpart." See R8-Q13. |
| 01.7 | RS HA-7; §6.1 "capture evidence references"; U-11 (Depends) | A | U-11 Owner "Host owner (DEP-001; relay)" → "SWBPIPE owner decision (PB-TBD-002; ANS §2)"; effect unchanged. |
| 01.8 | AS U-07 | A | Same owner change as 01.7. |
| 01.9 | ADAPTER §7.6; XF-18; XF-33 (Depends) | A | XF-18 "— **AWAITING INPUT** (SQ-01) for the reference" → STD-2. XF-33: C (elicitation is not capture — SWBPIPE agrees); no edit. |
| 01.10 | ADAPTER UNRESOLVED "Capture-evidence reference for host-captured acts (R2-20; SQ-01)" | A | Owner "Host owner (DEP-001)" → "SWBPIPE owner decision (PB-TBD-002; ANS §2)". |
| 01.11 | CA W14-04, W14-05; EC-01; DI-4 (Depends) | V | EC-01 standing "prepared" → STD-1. DI-4 "Not supplied" → "Answered (SQ-01, SQ-02): no capture-evidence reference; no host-held route; SWBPIPE owner decisions". W14-05 state → STD-2. |
| 01.12 | XT XC-02, XC-09; IN-16 (Depends) | V | IN-16 "Not received" → STD-1 (gist "no reference; Apply receipt has no person/time and is session-only"). XC-02 and XC-09 (+) states → STD-2. |
| 01.13 | GUIDE M5.3, M5.8, HC-5.2 (§4.3 homes) | V | "relay pending" → STD-1 in those lines. |
| 01.14 | EXEC CAP-6; ADAPTER L-ADAPTER-4; HOSTING R9 (elicitation never capture) | C | None: SWBPIPE records say agent-driven Apply and computer-use clicks are not acceptance, and the CLI exposes no Apply. |

### SQ-02 Governing checkpoint constraint

**Gist.** **Route (iv), none planned** — FACT: no workflow run, declaration,
checkpoint, run association or hold machine; no record plans (i)–(iii);
planning one is an **OWNER DECISION** with no open item. (a) An extra
constraint field would be **refused as an unknown field** (strict batch
preflight). (c) No. (d) No / No. (f) No / No. (e) none. Related fact (not an
answer to D6): every host operation today resolves *propose* (all changes wait
for Apply); SWBPIPE says this **must not be counted as host-held carriage under
R2-12**.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 02.1 | EXEC §3.6 HS-3 row; fixture table rows `CP-accept`, `CP-grant`; "Consequences" bullets; MT-2; MT-16; CH-27; §8 register rows (U-X3, constraint receipt); U-E1; U-E13; VC-E-02; VC-E-12 | V | Per Part 2 (P2.1–P2.4, P2.12, P2.17). |
| 02.2 | EXEC §2 HP-H "Standing (v0.2)" | V | "**Pending SQ-02 (a)–(d)**. When evidenced, the value is **enforced on the host route** …" → "**Not offered by SWBPIPE** (SQ-02 answered 2026-09-28: route (iv), none planned; (a) No, (c) No, (d) No/No, (f) No/No). Would give *enforced on the host route* for host operations only if a host offered and evidenced it. It never covers App-only steps (R5-10)". |
| 02.3 | EXEC §2 enforcement-boundary paragraph "How the App holds its own runs was deferred … Until then, the hold points stand as follows" | V | → "… was deferred by the owner to the SWBPIPE answer to RELAY SQ-02 (DECISION-2 D6). SWBPIPE answered on 2026-09-28 that no host-held route exists or is planned (route (iv)); D6 returns to the owner (R8). The hold points stand as follows:". |
| 02.4 | WD §4.3.8 HS-3 row; "Authoring advice"; closing paragraph; U-19; U-30; VC-11; VC-37; VC-43 (Depends: I-7, U-19, VC-11) | V | Per Part 2 (P2.5, P2.13, P2.16). |
| 02.5 | WD-EX E8 rows E1-via-X, E1d-via-X, L-WDEX-17 (both); closing paragraph; U-19, U-30; E2 R-5a/R-5b | V | Per Part 2 (P2.1, P2.3, P2.5, P2.6); R-5a/R-5b "**AWAITING INPUT** (U-19)" → STD-2 (host-loop fixtures; SWBPIPE has no host loop, SQ-20). |
| 02.6 | C §10.1 FXA-5; §10.4 V-GR1; V-CP1 status (Depends: V-CP1) | V | Per Part 2 (P2.1, P2.4); V-CP1 "Status: AWAITING INPUT (host receipt of the constraint, relay)" → STD-2 (gist "route (iv): no receipt, no host copy; a constraint field is refused as unknown"). |
| 02.7 | P §3.3 constraint paragraph; §4.4 bullets; U-P10 (Depends) | V | §3.3: "…is **not established** while SQ-02 is unanswered, and **not enforceable** only once SQ-02 is answered with no host-held route (R6-1, R6-5; EXEC HS-3)." → "…is **not enforceable**: SQ-02 was answered on 2026-09-28 with no host-held route (route (iv); R6-1, R6-5; EXEC HS-3 (c))." Add: "SWBPIPE's batch preflight refuses unknown fields, so a constraint carried as a request field is refused as `invalid_request` rather than honoured (SQ-02 (a)); see R8-Q12." U-P10 effect → STD-2 for V-CP1/FX-C9/PC-24/VC-11. |
| 02.8 | ACT §4.4 "Relay question (DEP-001)" bullet; §4.6 consequences, "Enforced on the host route … awaits"; §12 item 4 (c), (f); FX-48 (b)(c); FX-50; U-04; U-D6; F-16 | V | Per Part 2 (P2.1, P2.7, P2.14). §4.4 bullet → append "Answered 2026-09-28 (SQ-02): neither; route (iv), none planned. FX-29 stays AWAITING INPUT (STD-2)." |
| 02.9 | AS §4 hold-support text; F6d; F18 variant; F6b; U-12; U-16; VC-03; VC-16 | V | Per Part 2 (P2.8); F6b and U-12 → STD-2; U-16 → STD-4. |
| 02.10 | RS E7 (V-GR1 via X); E10 (vii); U-19; U-25; VC-17; VC-28 | V | Per Part 2 (P2.4, P2.9); U-19 effect add "SQ-02 answered: none"; U-25 → STD-4. |
| 02.11 | LOOP §13 Q-1; FX-C9; §2.4.4 row "A5 checkpoint … AWAITING INPUT (§13 Q-1 → SQ-02; DEP-001)"; §2.4.4 App-run classification row; UNRESOLVED D6 row (Depends) | A | FX-C9 / §2.4.4 A5 row: "AWAITING INPUT (§13 Q-1 → SQ-02; DEP-001)" → STD-2 (gist "no host loop and no host-held evaluation; SQ-02 route (iv), SQ-20"). D6 row → STD-4. The App-run classification text stays (generic). |
| 02.12 | PANEL §8 Q-1; PC-24; UNRESOLVED D6 and DEP-001 rows (Depends) | A | PC-24 "**AWAITING INPUT** (R2-12; host constraint handling, §8 Q-1)" → STD-2. D6 row → STD-4. |
| 02.13 | ADAPTER §2 "When an adapter is needed" paragraph; §5.3 GC-3 table, GC-5; "Until host evidence … V-CP1 over X is AWAITING INPUT"; §7.7; OC-7, OC-11; XF-25; XF-26; XF-42; UNRESOLVED D6 row; U-P10 row (Depends) | V | Per Part 2 (P2.10, P2.11, P2.15). OC-11 Relay cell "SQ-02" → "SQ-02 (answered: route (iv), none planned)". XF-42: C (a recording case; unchanged). |
| 02.14 | CA S-13; §2.2; §2.3 CA-0/CA-2/CA-H host contribution cells; DI-4; DI-6; WR-6; WR-11; ST-4; W14-03; W14-04; F-10; F-15; §5 row "OI-021, OI-003, U-03, D6"; §10 row; UNRESOLVED D6 row; EC-02 (Depends) | V | Per Part 2 (P2.1, P2.3, P2.13, P2.16). EC-02 → STD-1. §5 row cell "D6 (deferred to SQ-02)" → "D6 (SQ-02 answered: none; returned to the owner)"; same in §10 row. |
| 02.15 | XT S-10; IN-17; IN-25; XC-10; F-10; UNRESOLVED D6 row (Depends) | V | Per Part 2 (P2.11). IN-17 "Not received" → STD-1 (gist "route (iv), none planned"). |
| 02.16 | GUIDE §0 hold vocabulary; §2.13 D6 rows; §2.14 HS-3 row and fixture table; M6.4, M7.6, M8.4, M9.5; HC-6.3; HC-9.6; UNRESOLVED D6 row | V | Per Part 2 (P2.1–P2.6, P2.16). |
| 02.17 | HOSTING §6.7 lead paragraph and HP-H bullet; U-23 | A | §6.7 "App-side run holds at checkpoints are `UNRESOLVED{D6}` pending the SWBPIPE answer to SQ-02 (DECISION-2)." → "… are `UNRESOLVED{D6}`; SWBPIPE answered SQ-02 on 2026-09-28 with no host-held route (route (iv)), and D6 returns to the owner (R8)." HP-H bullet "(pending SQ-02)" → "(not offered by SWBPIPE, SQ-02 route (iv))". U-23 → STD-4. |
| 02.18 | RELAY SQ-02 body, "App assumes meanwhile" | N | STD-6: not edited. |
| 02.19 | RELAY UNRESOLVED row `UNRESOLVED{D6}` | V | → STD-4. |

### SQ-03 Content identities used to bind acts

**Gist.** (a) **No** per-row/per-object subject identity — FACT; the only
identity is `ModelHashEvidence` {sha256, rfc8785_jcs, scope `model_payload`}
over the whole model. (b) N/A; FXA-2 has no host counterpart. (c) Partly: an
Apply binds to its operation by id, and to the model by an optional claimed
whole-model hash plus per-field before-values (stale → `OP-STALE-BEFORE-VALUE`,
`OP-CLAIMED-MODEL-HASH-MISMATCH`). (d) Partly: `target_ref`, diff rows, new
whole-model hash; created objects appear as target ids; no post-application
per-object identities. (e) Same identity value (pure content hash), but in
DRAFT #885 the revision advances on every commit (Undo included), so an earlier
proposal stays stale. T3 solver receipts identify **analysis results**, not
rows.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 03.1 | C §5.3 (subject content identity "host-supplied, per subject"); U-C3 (Depends) | A | Add note under §5.3: "SWBPIPE (SQ-03, 2026-09-28): no per-row or per-object identity; only a whole-model hash (sha256 over RFC 8785 JCS of the model payload). Receiving rule per R8-Q3." U-C3 effect "Contract rule fixed as INTEGRATION; host behavior unevidenced" → "…; SWBPIPE answered: whole-model identity and whole-model staleness only (SQ-03, SQ-07 (d)); see R8-Q2/Q3". |
| 03.2 | C §10.1 FXA-2, FXA-3 (Depends) | A | Add to FXA-2: "No SWBPIPE counterpart (SQ-03 (b)): SWBPIPE has no per-object identity. FXA-2 stays a fixture assumption." |
| 03.3 | P §3.1; §9 "applied (receipt)" resulting objects; U-P2 (Depends) | A | §9 applied row: keep "or 'not supplied' as an evidence limit"; add note "SWBPIPE supplies `target_ref`, per-field diffs and the new whole-model hash; created objects appear only as target ids of `create_*` operations; no post-application per-object identity (SQ-03 (d))". U-P2 effect: "resulting objects may be 'not supplied'" → "…; SWBPIPE: target ids and diffs only (SQ-03 (d))". |
| 03.4 | WD §4.3.6 SB-1…SB-3 (Depends) | A | Add note: "Against SWBPIPE, subject binding can bind only to the whole-model identity (SQ-03 (a)); see R8-Q3." |
| 03.5 | RS L-1/L-2, L-11, U-12 (Depends) | C | L-11 (keep an observed lapse visible either way) holds: SWBPIPE (e) gives "same identity value; revision advances". U-12: add effect "SWBPIPE: same content ⇒ same whole-model hash; DRAFT #885 revision still advances (SQ-03 (e))". |
| 03.6 | EXEC SP-4, CH-1, CH-7, MC-2 (Depends) | N | None while fixture-only (FXA-2/FXA-3 labeled). |
| 03.7 | LOOP §13 Q-3; FX-C1 (Depends) | N | None (host-loop). |
| 03.8 | WD-EX E1 `CP-check` (subject: objects changed by the applied outcome); E1c FXA-2 note (Depends) | A | E1c note "By FXA-2 a support's subject content identity covers its display label …": append "(fixture assumption; SWBPIPE has no per-object identity, SQ-03)". |
| 03.9 | ADAPTER RD-2 (Depends); XF-11 ("subject identities ⟨S-1…S-4@r12⟩ … identical to H and E") | A | Add to RD-2: "SWBPIPE reads carry no subject identities (SQ-03 (a)); a host read without them is received with subject identities *not supplied* (evidence limit), never App-computed." |
| 03.10 | CA W14-04, W14-06; EC-03 (Depends) | V | EC-03 → STD-1 (gist "whole-model identity only"). W14-06 inputs "SQ-03 (b)" → add "(answered: no per-object identity)"; state → STD-2. |
| 03.11 | GUIDE M3.2, M4.2, M4.3, M5.5; HC-3.2, HC-4.2, HC-4.3, HC-5.4 | V | STD-1 in those lines. |
| 03.12 | ACT §2.5 content binding (A5 binds change-item content identity) | C | SQ-03 (c) partly confirms: Apply binds operation id + claimed whole-model hash + per-field before-values; no edit beyond 01.5's note. |

### SQ-04 First connected activity

**Gist.** **Selection: none** — choosing is an **OWNER DECISION** (with the
App/shared owner). Candidates on main (FACT): 27 change kinds through
`operation_applier`; reads (model read; DRAFT #885 `inspect`); checks
(validate-only preview; mechanics solve with host-named integrity standing
Passed/Sensitive/`NUMERICAL_INTEGRITY_*`; user rule checks). DRAFT #885
external-wires one change: Node `position.x` modify/set_field (single and
ordered atomic batch). Expression: a **development Codex controller via the
CLI first, an embedded agent later**; the App's Codex is not named.
Environment: macOS only; PR #885 head `12907f393` unmerged; desktop with
`SWBPIPE_LIVE_CONTROL=1`; CLI feature `live-control-cli`; clean DEC-025 sweep,
native I1/I2, actual-human H1/H2 and final review outstanding; deferred to
UI-SUCCESSOR; no date.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 04.1 | CA §2.5 DI-1 (Depends: §2, §3, TBD-001) | A | Current standing "`UNRESOLVED{OI-021}`; fixture only" → "`UNRESOLVED{OI-021}`; fixture only. SQ-04 answered: no selection (owner decision). Candidates on SWBPIPE main: 27 change kinds via one engine route; reads; validate-only preview, solve integrity standing, user rule checks; DRAFT #885 wires only Node `position.x` set_field on X". |
| 04.2 | CA DI-3; §2.2 variant table | A | DI-3 "Not supplied" → "Answered (SQ-04 (c)(d)): SWBPIPE's first expression is a development Codex controller over the CLI, the App's Codex is not named; environment macOS-only, PR #885 unmerged, `SWBPIPE_LIVE_CONTROL=1`, feature `live-control-cli`; deferred to UI-SUCCESSOR, no date". §2.2: add note under the variant table: "SWBPIPE (SQ-04 (c), SQ-20): no embedded agent exists (CA/E has no host counterpart now); CA/X's named caller in SWBPIPE records is a development Codex, not the App's Codex (DECISION-3 defers naming)". |
| 04.3 | CA EC-04, EC-12; ST-3 | V | EC-04 → STD-1. EC-12 unchanged (open). |
| 04.4 | ACT U-01; EXEC U-E17; LOOP/PANEL OI-021 rows; C OP-C11 (Depends) | C | None: OI-021 stays open; OP-C11 stays *no policy basis (pending OI-021)*. |
| 04.5 | XT IN-10 (Depends) | N | None (`UNRESOLVED{OI-021}`). |
| 04.6 | GUIDE M1.2, M1.5, M1.8; HC-0.2, HC-1.2 | V | STD-1. |

### SQ-05 Policy for the selected operation

**Gist.** (a) **No class system**; every change requires Apply
(`requires_user_acceptance: true`, `direct_model_mutation_allowed: false`
hard-coded) — FACT. (b) none. (c) No named reserved list; D2 table: checked =
engineer-only DESIGN; accepting = Apply; approval and reliance = not software
acts; grant change = no grants; external access = a launch environment
variable, not a captured act. (d) no settings reference; (e) no grant states;
(f), (i) **OWNER DECISION** OI-016; (g) no withdraw/reject operation on main;
#885 `withdrawn` = the person cleared the queue (`cleared_in_review`); (h) N/A.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 05.1 | ACT §7 SWB model-change class ("Host adoption is **not evidenced** (DEP-001)"); §8.3 P-01…P-06 (Depends) | A | §7 quote block: append "SWBPIPE (SQ-05, 2026-09-28): no class system and no grants; every change requires the person's Apply (hard-coded). The App's DERIVED class and default stand as App/shared meaning; the host's own autonomy is SWBPIPE owner decision OI-016." |
| 05.2 | ACT U-01, U-02, U-04(d), U-06 (Depends) | A | U-06 Owner "Host policy owner (V4-HI-41; DEP-001)" → "SWBPIPE owner decision OI-016 (ANS §2)"; U-04(d) → answered: no settings reference. |
| 05.3 | AS §3 grant display; U-04; U-06 (Depends) | A | Add note to §3: "SWBPIPE has no grant states (SQ-05 (e)); a display rule for a host with no grant model is R8-Q16." U-04 effect add "SQ-05 (h): not applicable (no grants; Apply always revalidates)". U-06 "*unconfirmed* unless reported" → add "SWBPIPE reports no settings reference (SQ-05 (d))". |
| 05.4 | P U-P6 (Depends) | A | Effect "A11 proposer-only; A10 reserved wherever A5 is" → add "SWBPIPE: no withdraw or reject operation; DRAFT #885 `withdrawn` = the person cleared the queue (R8-Q10)". |
| 05.5 | PANEL §8 Q-8 (Depends) | N | None. |
| 05.6 | ADAPTER UNRESOLVED "Host adoption of D2, D3, P-01…P-06 …" | A | Effect add "SWBPIPE (SQ-05): no class system, no named reserved list; every change waits for Apply". |
| 05.7 | C T15 class P-03; U-02 (Depends) | N | None (fixture). |
| 05.8 | CA §2 row CA-2; W14-04 (ii); EC-05; DI-2 | V | EC-05 → STD-1. DI-2 standing "host adoption not evidenced (DEP-001)" → "host: no class system, no grants, no named reserved list (SQ-05); autonomy is SWBPIPE owner decision OI-016". W14-04 (ii) (direct under ⟨set-2⟩): add "no SWBPIPE counterpart (no grants, SQ-05)". |
| 05.9 | GUIDE §2.13 TBD-001 "host list relay pending (SQ-05)"; M1.4, M2.2, M4.2, M5.2, M6.1–M6.3, M6.5, M7.7; HC-1.4, HC-2.2, HC-4.2, HC-5.1, HC-6.1, HC-6.2, HC-6.4 | V | STD-1. |
| 05.10 | XT IN-07, IN-29 | V | IN-07 "host adoption not evidenced (SQ-05)" → "host: no class system or reserved list; every change waits for Apply (SQ-05)". IN-29 add "host: no grant states (SQ-05 (e))". |

### SQ-06 Direct application on the external channel

**Gist.** **Not (a)**. SWBPIPE records word the no-Apply rule as both (b) a
channel rule and (c) a first-journey property; which governs is an **OWNER
DECISION**. A direct/Apply request over DRAFT #885 is refused as
**`unsupported_method`** ("Only inspect, preview, submit and status are
supported"), **not** *not permitted* naming a rule.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 06.1 | ADAPTER §6 RP-4; XF-24 (Depends) | A | Per Part 3 item 1. RP-4: append "SWBPIPE (SQ-06, 2026-09-28): the host states no treatment; Apply is not a method on X and a request for it is refused `unsupported_method`. The App relays that as host-reported and, per R8-Q-item-1, classifies it *not exposed on this surface*; it never shows a channel rule, class value or grant (S-X3)." XF-24 state: add "variant; not SWBPIPE's behavior (SQ-06)". |
| 06.2 | ADAPTER OC-7 (Depends) | N | None. |
| 06.3 | ACT §6 rows 6–8 (Depends) | A | Add note after the table: "Against SWBPIPE's X, rows 6–8 do not arise as written: there is no direct mode and no Apply method; a request for Apply is refused `unsupported_method` (SQ-06). R2-4 'reserved entries always offered' is not met by that host (DEP-001, recorded, not repaired App-side)." |
| 06.4 | XT XC-10 (Depends) | A | XC-10 XF-24 item: "(host channel rule variant)" → "(host channel rule variant; SWBPIPE instead returns `unsupported_method`, SQ-06)". |
| 06.5 | GUIDE M9.4; HC-9.3 | V | STD-1 (gist "`unsupported_method`; no stated channel treatment; label (b)/(c) is a SWBPIPE owner decision"). |
| 06.6 | CA EC-05 (with SQ-05) | V | Covered by 05.8. |

### SQ-07 Read basis, generation and staleness

**Gist.** (a) Main: no (read and hash separate; no workspace identity or
generation); **DRAFT #885**: `inspect` returns `basis_identity` {app instance,
controller session, workspace, project generation, project, model revision,
model hash}. (b) #885 mints a new workspace id and generation when the
published project changes; cross-workspace reuse is rejected. (c) Main: **no**
(offline intake captures basis at queue time); #885 **yes** (preview freezes
the inspected basis). (d) **No: staleness is whole-model** — any revision
change stales every queued proposal (main and #885); R2-13 does not hold;
per-field before-values also checked. (e) Yes (Apply re-runs full validation
against the claimed hash). (f) Any model commit (edit, apply, undo, redo,
open, create); selection does not stale. (g) Not found. (h) Solve and rule
checks run on the current model; results cleared on any model change; no
cited-versus-evaluated statement.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 07.1 | C §5.4 "No longer holds" (R2-13, INTEGRATION); U-C3 (Depends) | A | Per Part 3 item 2 and R8-Q2. Add note after the bullet: "SWBPIPE (SQ-07 (d), 2026-09-28): staleness is whole-model; any model commit stales every queued proposal. The App relays that refusal as host-stated with scope 'whole model' (R8-Q2); it never re-evaluates it per item." |
| 07.2 | C §5.4 receiving-risk paragraph (queue-time basis; HI §11 `e548d4cf`) | A | Per Part 3 item 5: append "SWBPIPE (SQ-07 (c)): true of main's offline intake (queue-time basis); DRAFT #885 freezes the inspected basis at preview and keeps it at submit — unmerged and deferred". |
| 07.3 | C §5.1 Generation; U-C2; Tg (Depends) | C | U-C2 effect add "SWBPIPE #885: new workspace id and generation on a published-project change; cross-workspace reuse rejected; archive restore not addressed (SQ-07 (b))". Confirms *unknown (incomparable)*. |
| 07.4 | C U-C4 (Depends) | N | Effect add "SWBPIPE: no multi-read reliance concept (SQ-07 (g), not found)". |
| 07.5 | C U-C10; §5.4 non-mutating bullet (Depends) | A | U-C10 effect add "SWBPIPE: solve and rule checks run on the current model; results are cleared on any change; no cited-versus-evaluated statement (SQ-07 (h))". |
| 07.6 | P §5 Trigger; §12 row 1; U-P3 (Depends) | A | §5 Trigger: append "SWBPIPE's trigger is any model revision change (whole-model; SQ-07 (d)); per R8-Q2 the App reports the host's scope." §12 row 1: as 07.2. U-P3: C — "SWBPIPE Apply re-runs full engine validation against the claimed hash (SQ-07 (e))". |
| 07.7 | LOOP §13 Q-6 (per-item part); FX-D2; FX-D3 (Depends) | N | None (host-loop fixtures). |
| 07.8 | ADAPTER RD-2, RD-5; XF-14; XF-39 (Depends) | A | XF-14 expected "Both PR-1 items **refused — stale** per item: failing target S-3 …" — add "(fixture; SWBPIPE reports whole-model staleness without failing targets, SQ-07 (d))". |
| 07.9 | EXEC MX-7 (Depends) | N | None. |
| 07.10 | XT XC-03, XC-08; IN-19 (Depends) | V | IN-19 → STD-1 (gist "#885 freezes inspected basis; staleness whole-model; per-item rule not held"). XC-03 expected: add "failing target reported *not supplied* where the host's scope is whole-model (R8-Q2)". |
| 07.11 | CA CA-4 (host contribution "Per-item stale check on original inspected basis"); EC-06 | V | EC-06 → STD-1. CA-4 cell: append "(SWBPIPE: whole-model staleness; original basis frozen only in DRAFT #885)". |
| 07.12 | GUIDE M3.1, M3.3, M3.4, M3.5; HC-3.1, HC-3.3, HC-3.4 | V | STD-1. |
| 07.13 | ADAPTER XF-17; XT XC-04 (no retargeting) | C | SQ-07 (f): selection changes do not stale; no edit. |

### SQ-08 Proposal identity and repeated submission

**Gist.** Main: submitter supplies `batch_id`; no de-duplication; state not
readable outside the UI. **DRAFT #885**: (a) controller mints `preview_ref`
at preview; caller supplies `idempotency_key` at submit; controller returns a
`ticket`. (b) **Yes**, key lookup before the basis check; same key + different
content → `idempotency_conflict`. (c) **No** (restart expires handles or
yields `outcome_unknown`). (d) Yes within session (`status` by ticket).
(e) receipt binds one model transition; one undo checkpoint per batch;
duplicate-submission witnesses not yet performed. Durable de-duplication:
**OWNER DECISION** ("durable receipt carrier").

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 08.1 | P §5 Precedence; §7; U-P1; C T13 (Depends: R2-13) | C | R2-13's de-duplication-first half holds in DRAFT #885. U-P1 effect add "SWBPIPE #885: caller-supplied `idempotency_key`, controller `preview_ref` and `ticket`; key lookup before basis check; not durable across restart (SQ-08)". |
| 08.2 | ADAPTER §5.6 PI-1, PI-2, PI-4 (Depends) | C | PI-4's durability limit is confirmed (SQ-08 (c)). Add "(confirmed by SQ-08 (c))" after "PR #885"; PI-2 read-by-identity exists within session only. |
| 08.3 | ADAPTER OC-7, OC-10 (Depends) | A | OC-10 evidence: append "SQ-08: `status` by `ticket`, within one controller session". OC-7: append "SQ-08: identity = caller `idempotency_key`; host `preview_ref` precedes submit; SQ-14: caller-supplied origin fields rejected". |
| 08.4 | ADAPTER XF-19, XF-21, XF-40, XF-41; UNRESOLVED identity row (Depends) | A | XF-21, XF-40 "**AWAITING INPUT** (SQ-08)" → STD-2 (gist "durable de-duplication not offered; 'durable receipt carrier' is a SWBPIPE owner decision"). UNRESOLVED row Owner "Host owner with DEL-03-02" → "SWBPIPE owner decision (durable receipt carrier; ANS §2) with DEL-03-02". |
| 08.5 | LOOP §13 Q-6; FX-O1 (Depends) | N | None. |
| 08.6 | XT XC-05, XC-06; IN-18 (Depends) | V | IN-18 → STD-1. XC-05/XC-06 states → STD-2 (gist "within-session only"). |
| 08.7 | CA CA-5; EC-06 | V | Covered by 07.11 (EC-06). CA-5 host cell: append "(#885: within-session de-duplication and status only; SQ-08)". |
| 08.8 | GUIDE M3.4, M4.2, M4.5, M9.5; HC-3.4, HC-4.2, HC-4.5, HC-9.6 | V | STD-1. |

### SQ-09 Outcome statements, errors and unknown outcomes

**Gist.** SWBPIPE maps (main / DRAFT #885): refused invalid → `blocked` /
`invalid_request`, `unsupported_change`; refused stale → `OP-STALE-…`,
`OP-CLAIMED-MODEL-HASH-MISMATCH` / `stale_basis`, `expired`; queued → `queued`
(only after the controller observes publication); applied → 
`applied_to_session_model` / `committed`; rejected → none on main; #885
`rejected: validation_rejected` = **the engine** rejected at Apply, not a
person; withdrawn → #885 = the person cleared the queue; **channel not
enabled → no code** (`controller_unavailable` or attachment failure); not
exposed → `unsupported_change`/`unsupported_method`; outcome unknown →
`outcome_unknown`; unavailable/not permitted/error → `busy`, `capacity`,
`not_ready`, `unauthorized`, `wrong_app`, `wrong_workspace`, `internal_error`,
… each with `retryable` and `next_action`. Transport status separate.
(b) batches atomic. (c) no durable receipt; unknown resolvable only within the
controller session. (d) validation failure before queueing = blocking, nothing
queued. (e) same engine codes at validate and Apply; #885 distinguishes
`validation_rejected` at Apply. (f) one batch = one application = one undo
checkpoint.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 09.1 | ADAPTER §4.5 M-1…M-5; OC-9 (Depends) | A | Add after M-5: "**Received host vocabulary (SWBPIPE, SQ-09; evidence only — DRAFT #885 unmerged).** A mapping table from the SQ-09 answer (as in ANS §1 SQ-09), with these App rulings (R8-Q1, Q4, Q10): `unsupported_method`/`unsupported_change` → *not exposed on this surface* (host-reported); `controller_unavailable` or attachment failure → *endpoint-unavailable* (App-observed), never *channel not enabled*; `rejected: validation_rejected` → *refused — invalid* at application, never A10; `withdrawn`/`cleared_in_review` → item left, cleared by the person without a decision record, never A10 or A11; `outcome_unknown` → *outcome unknown* (reporter host); `expired` → *refused — stale* (reason 'expired'); `retryable`/`next_action` recorded, never acted on as a treatment." OC-9: append "SQ-09: CLI JSON with named codes". |
| 09.2 | P §9 rows *rejected*, *withdrawn*, *channel not enabled*; U-P4, U-P5, U-P7 (Depends) | A | U-P4 effect "PROPOSED: refused, stays drafted" → add "confirmed by SWBPIPE (SQ-09 (d))" (C). U-P5 → "SWBPIPE #885 distinguishes `validation_rejected` at Apply (SQ-09 (e))". U-P7 → "SWBPIPE: one batch = one application = one undo checkpoint; atomic (SQ-09 (b), (f))". Add note under §9: rows *rejected* and *withdrawn* as in 09.1. |
| 09.3 | P §4.3 item-level acceptance; R2-18 mixed decisions; C T11 | A | Add note to P §4.3: "SWBPIPE Apply applies a batch atomically and Clear discards without record (SQ-09 (b)/(f), SQ-01); per-item A5/A10 decisions (C T11) and mixed-item dispositions (R2-18, WD §4.3.7) have no SWBPIPE counterpart." |
| 09.4 | C §4.1 "Channel not enabled" reporter host (Depends) | A | Per Part 3 item 4: add "SWBPIPE has no *channel not enabled* code; off appears as `controller_unavailable` or an attachment failure (SQ-09, SQ-13) — the App reports *endpoint-unavailable* with that reason, and the channel state stays *disabled* because A13 is never evidenced (R8-Q4)". |
| 09.5 | EXEC MX-8 (Depends) | N | None. |
| 09.6 | XT XC-06, XC-07; IN-20 (Depends) | V | IN-20 → STD-1. XC-07 state → STD-2 (gist "`outcome_unknown` exists; resolvable within controller session only"). |
| 09.7 | CA CA-5, CA-R host cells ("Receipt and act references readable (SQ-01, SQ-09)") | A | Append "(SWBPIPE: receipts session-only; no act references; SQ-01, SQ-09 (c))". |
| 09.8 | GUIDE M1.3, M2.1, M2.3, M4.3, M4.6; HC-2.3 | V | STD-1. |
| 09.9 | RELAY SQ-09 assumption ("outcome unknown" for submissions only) | C | STD-6. SWBPIPE's `outcome_unknown` is a submission outcome; consistent. |

### SQ-10 Undo and publication

**Gist.** Undo: a **session** Undo/Redo stack of whole-model snapshots (25
deep) — **not an operation through the engine**, **no receipt**, no reference
to the reversed change, not governed by operation policy; one checkpoint per
batch; cleared on project open or create. #885 records `undo_checkpoint_id`;
Undo not on the CLI. "Publication": two unrelated meanings (controller
observing visibility; public-repository release); neither affects standing.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 10.1 | P §4.5; U-P8 (Depends: R2-15, R3-4) | A | U-P8 effect: append "SWBPIPE (SQ-10): session snapshot undo, not through the route, no receipt, not policy-governed; *reverses ⟨receipt⟩* cannot be shown for it; acts bound to content it changes still lapse (R2-15) — lapse is observed from the model identity". See R8-Q15. |
| 10.2 | C OP-C10, T17 (Depends) | N | None (fixture; mechanism was a host input). |
| 10.3 | ADAPTER RP-6; XF-38 (Depends) | A | RP-6: append "SWBPIPE Undo is not exposed on the CLI (SQ-10)". |
| 10.4 | PANEL §8 Q-4 (reversed display) (Depends) | N | None. |
| 10.5 | AS F7; WD-EX R-17 ("applied, then reversed by RC-3") | A | Add note to AS §8 or F7: "SWBPIPE undo writes no receipt (SQ-10); 'applied, then reversed by ⟨receipt⟩' needs a host receipt and is *not supplied* there". |
| 10.6 | CA CA-5 ("undo reverses a receipt"); XT CMP-14; IN-26 | V | IN-26 → STD-1. CA-5: append "(SWBPIPE: session undo, no receipt; SQ-10)". |
| 10.7 | GUIDE M4.3, M4.4; HC-4.3, HC-4.4 | V | STD-1. |
| 10.8 | "Publication" (RELAY SQ-10 question) | C | No App text relies on publication affecting standing; no edit. |

### SQ-11 Exposure per surface

**Gist.** **No** per-surface exposure element; the desktop toolkit's
capability `status` describes UI routes only. DRAFT #885 offers exactly one
entry on the CLI (Node `position.x` set_field); everything else is refused as
`unsupported_change`; there is no embedded surface. "Not exposed" is reported
through `unsupported_change`/`unsupported_method`.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 11.1 | C §3 element 9; §8; U-C7; FXA-1; V-X1 (Depends: R2-4) | A | U-C7 effect add "SWBPIPE: no exposure element; 'not exposed' via `unsupported_change`/`unsupported_method` (SQ-11)". FXA-1: add "(fixture assumption; SWBPIPE exposes one entry on X and has no E surface, SQ-11)". |
| 11.2 | ADAPTER XF-09 (Depends) | A | Expected "Host-reported **not exposed on this surface**, relayed (reporter host)" — add "(SWBPIPE form: `unsupported_change`, mapped per 09.1)". |
| 11.3 | EXEC EV-7/EV-8; MT-5; U-E18 (Depends) | N | None now (fixture FXA-1). Note for R8-Q-HS4: every real SWBPIPE entry has *unagreed* exposure (EV-7). |
| 11.4 | WD §4.2.4 (Depends); U-23 | N | U-23 effect add "SWBPIPE: no exposure element (SQ-11)". |
| 11.5 | LOOP §13 Q-7; FX-U3 (Depends) | N | None. |
| 11.6 | XT IN-24; XC-11 | V | IN-24 → STD-1. |
| 11.7 | GUIDE M1.3, M1.7, M8.3; HC-1.5; §2.14 HS-4 "Changes when: Exposure agreed (SQ-11)" | V | STD-1 in M-lines; HS-4 row per R8-Q-HS4. |

### SQ-12 External seam and derivation

**Gist.** Seam: the **CLI (DRAFT #885), not MCP**. MCP only if the actual
Codex client meets the owner's modern stateless MCP condition of 2026-07-28;
the tested bundled client failed it; any MCP choice is an **OWNER DECISION**.
Derivation: **hand-built and narrow**; method set fixed in code, not generated
from or checked against a catalog. **No** per-operation identity or version
(one engine crate version).

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 12.1 | ADAPTER §9 OC-1, OC-8; §4.1 NM-1…NM-4 (Depends) | A | OC-1 evidence: append "SQ-12 (2026-09-28): SWBPIPE offers the CLI (DRAFT #885), not MCP; MCP only under the owner's modern-client condition (SWBPIPE owner decision)". OC-8: "derivation not stated" → "hand-built, narrow; not generated from or checked against a catalog (SQ-12)". NM-2: add "SWBPIPE supplies no mapping and has no per-operation identity or version (SQ-12); every requirement on X is *not established* against it". |
| 12.2 | C §8 X column (Depends) | A | X-column derivation value: *unagreed* → "SWBPIPE: hand-built (SQ-12)". |
| 12.3 | WD §4.2.1 / CA WR-4 ("Required tools by **catalog operation identity and version**") | A | Add note to CA WR-4: "SWBPIPE has no per-operation identity or version (SQ-12); against it WR-4 references cannot resolve (EXEC EV-4 *not established*)". See Part 4.7. |
| 12.4 | XT §4, §5 (generated versus adapted); IN-09 (Depends) | V | IN-09 "Not received; PR #885 is evidence only" → STD-1 (gist "CLI, hand-built, no mapping"). §5.1: add "SWBPIPE's answer (hand-built surface) is evidence for the OI-003 work account; it decides nothing". |
| 12.5 | GUIDE M1.1, M1.6, M1.7, M2.5, M9.3; HC-1.7, HC-9.2 | V | STD-1. |

### SQ-13 Enablement behaviour

**Gist.** Off by default: yes (#885). Opt-in = **launch environment variable
`SWBPIPE_LIVE_CONTROL=1` + build feature `live-control-cli`**, **not** a
person's act. When off: no descriptor, no socket; CLI fails
`controller_unavailable`; **no explicit "channel not enabled" code**;
non-macOS → `unsupported_host`. State readable: **no**. Queued proposals when
disabled: not addressed (restart expires handles or yields
`outcome_unknown`).

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 13.1 | ADAPTER §3.2 channel states; "enablement unconfirmed" qualifier; E-1…E-9; OC-4 (Depends) | A | Per Part 3 item 4 and R8-Q4. OC-4 evidence "PR #885 'opt-in': nature not stated" → "SQ-13: a launch environment variable plus a build feature, not a captured act; no *channel not enabled* code; state not readable". §3.2 qualifier: add "Against SWBPIPE there is no host enablement record at all (SQ-28), so the state is *disabled* (sub-case 'host has no A13 facility'), not *unconfirmed*". |
| 13.2 | ADAPTER XF-01…XF-07, XF-35; UNRESOLVED "Enablement read and disable behavior" (Depends) | A | XF-02 expected "Host-reported **channel not enabled**" — add "(SWBPIPE form: `controller_unavailable`, App-reported *endpoint-unavailable*; no host code, SQ-13)". UNRESOLVED row effect "E-8 PROPOSED" → add "SWBPIPE: disable behavior for queued proposals not addressed (SQ-13)". |
| 13.3 | C §4.1 (Depends); R4-16 | A | Covered by 09.4. |
| 13.4 | XT XC-01, XC-12 (Depends) | V | XC-01 (b) "App configured, host off → host-reported *channel not enabled*" → add "(SWBPIPE: no such code; `controller_unavailable`)". States → STD-2. |
| 13.5 | GUIDE M9.1, M9.2; HC-9.1 | V | STD-1. |
| 13.6 | ACT §2.6 A13 row; R4-13 | C | "App-side configuration is never A13 evidence" unaffected; SWBPIPE's opt-in is host-side but not a captured act (see SQ-28). |

### SQ-14 Origin and caller identity

**Gist.** DRAFT #885 records, all controller-assigned (caller-supplied
author/source/acceptance fields rejected): `author_type: agent`; `source`
{`source_ref: local_json_cli:<session>:<request>`, `source_channel`,
`source_role: external_agent_proposal`}; receipt `origin` {actor type,
channel, request id}. Verified: **none** ("not verified Codex identity"; MCP
clientInfo "is not authentication"). Main: `source_identity_verification:
"not_performed_asserted_metadata_only"`. Conversation and workflow run: not
recorded. Authentication: random local capability in a 0600 descriptor in a
0700 directory; native side validates the app and registration identity. Any
descriptor holder; up to 16 concurrent connections.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 14.1 | P §3.3 author identity *unverified* (R4-15) (Depends) | C | Confirmed; add "(SWBPIPE records identity as not verified, SQ-14)". |
| 14.2 | P §3.3 origin elements conversation / workflow run | A | Add "SWBPIPE records neither conversation nor workflow run (SQ-14); the App records them App-side and links by request id". |
| 14.3 | ADAPTER §5.4; OC-6; XF-37 (Depends) | C | OC-6: append "SQ-14: local capability in 0600 descriptor; up to 16 concurrent callers; identity not verified". §5.4 unchanged. |
| 14.4 | RS R11 (Depends) | C | None. |
| 14.5 | XT IN-27 | V | STD-1. |
| 14.6 | GUIDE M4.1, M9.5; HC-4.1, HC-9.6 | V | STD-1. |

### SQ-15 Locality and sandbox

**Gist.** **Strictly local** (DRAFT #885): macOS Unix domain socket and
descriptor in a randomly named private directory under the system temporary
directory (0700/0600); no network listener. Sandbox: **not addressed**; by
construction a sandbox forbidding that path would block the CLI — an
inference, **not observed**.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 15.1 | ADAPTER E-7; §3.5; OC-5; OC-12 (Depends) | C | OC-5 evidence: append "SQ-15: UDS + descriptor under the macOS temp directory; no network listener". Sandbox effect stays *not observed* (§3.5 unchanged). |
| 15.2 | ADAPTER XF-07 (Depends) | N | None. |
| 15.3 | XT IN-28 | V | STD-1. |
| 15.4 | GUIDE M9.6; HC-9.4 | V | STD-1. |

### SQ-16 Host restriction by model destination

**Gist.** **No restriction**; the #885 wire has no destination field; **the
App need state nothing**. Related: SWBPIPE DEC-051 (open residency) gives an
owner-configured provider for SWBPIPE's **embedded** agent no guard "for now";
revisiting is an **OWNER DECISION**; it does not address the external CLI.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 16.1 | ADAPTER §3.4; S-X11; XF-05; XF-36; UNRESOLVED "Host channel restriction …" (Depends) | C | UNRESOLVED row: close — "Answered (SQ-16): no restriction; the App states nothing". XF-36 variant: add "(not SWBPIPE's behavior)". |
| 16.2 | EXEC CR-14; HOSTING §8.3 (Depends) | C | None. |
| 16.3 | XT IN-14, XC-01 (Depends) | V | IN-14 "Not received; no restriction presumed" → "Answered (SQ-16): no restriction; nothing to state". |
| 16.4 | CA DI-5 ("Open only: whether the host restricts its own channel (SQ-16)"); UNRESOLVED host-restriction row; EC-07 | V | DI-5 → "App side settled as stated; host side answered: no restriction (SQ-16)". UNRESOLVED row: close. EC-07 → STD-1. |
| 16.5 | RELAY UNRESOLVED "Host restriction of its own channel by model destination" | V | Close: "Answered 2026-09-28: no restriction (SQ-16)". |
| 16.6 | GUIDE B-6; M9.7; HC-9.5 | V | M9.7 standing "relay pending (host side)" → "answered: no restriction (SQ-16)". |
| 16.7 | C §4.1 model-destination paragraph "A host may restrict its own channel"; UNRESOLVED row "Host restriction … (R4-1)" | C | UNRESOLVED row: close as 16.1. |

### SQ-17 Receiving App workflows

**Gist.** (a) **No**, (b) **No** — the product has no workflow library,
reader or declaration parser; in SWBPIPE product code "workflow" means a user
journey. (c) N/A (no host runs). (d) Not decided.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 17.1 | EXEC §6.3 TR-5, TR-6; §6.7 TF-2…TF-4, TF-7; RT-1, RT-4; U-E14 (Depends) | A | RT-1, RT-4 "host side AWAITING INPUT (SQ-17 …)" → STD-2 (gist "no workflow library or declaration reader"). U-E14 Owner "Host owner (DEP-001)" → "SWBPIPE owner decision (a work item to receive App workflows; ANS §4)". |
| 17.2 | WD §3.4, §6.4 (Depends) | N | None. |
| 17.3 | PANEL UNRESOLVED "which party evaluates required-tool outcomes in the host" (Depends) | N | Effect add "SWBPIPE: not decided (SQ-17 (c), SQ-20)". |
| 17.4 | CA W14-01, W14-03; EC-08; §8.1 completion rule (Depends) | V | EC-08 → STD-1. W14-01/W14-03 states → STD-2. §8.1: add "SWBPIPE has no workflow library (SQ-17), so no host side of the V4-EXM-14 round trip exists until a SWBPIPE work item creates one (ANS §4); see Part 4.8". |
| 17.5 | GUIDE M7.7, M8.1–M8.3, M8.5; HC-7.5, HC-8.2, HC-8.3 | V | STD-1. |

### SQ-18 Adaptation and library identity

**Gist.** (a) No host workflows. (b)–(d) No. (e) N/A: operation intents carry
no operation version.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 18.1 | EXEC §6.2 HL-1…HL-3; §6.4 AD-1…AD-6; RT-2, RT-3, RT-7; U-E11; U-E14 (Depends) | A | RT-2 "host side AWAITING INPUT (SQ-18 (b), (c))" → STD-2. U-E11 Owner "Host owner with DEL-02-01, **SQ-18 (d)**" → add "(answered: no; no operation versions)". |
| 18.2 | C U-C6, U-C9; LIB-A1, LIB-A2 (Depends) | A | U-C6 effect add "SWBPIPE: no per-entry versions; one engine crate version (SQ-12, SQ-18 (e))". U-C9 effect add "SWBPIPE: none (SQ-18 (d))". |
| 18.3 | WD §6.4; WD-EX E3, E4 (Depends) | N | None. |
| 18.4 | PANEL §8 Q-6 (Depends) | N | None. |
| 18.5 | CA W14-02, W14-10; EC-08 | V | States → STD-2. |
| 18.6 | GUIDE M1.2, M8.1, M8.2, M8.5, M8.7; HC-1.2, HC-8.1, HC-8.2, HC-8.4 | V | STD-1. |

### SQ-19 Host run records and supplied guidance

**Gist.** (a)–(c) **No** — no host loop; SWBPIPE "run records" are solver
analysis run records. (d) **The premise is not established**: no agent "seat"
or role meanings in SWBPIPE records; the UX design has one agent panel with
Conversation, Proposals, Checks and Accepted tabs (persistence gap G-17); not
decided.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 19.1 | WD §5.3 SEAT-1…SEAT-3; U-09; S-M (Depends) | A | Per Part 3 item 9. U-09 effect: add "SWBPIPE: no seat concept; one agent panel in its UX design (SQ-19 (d)); not decided". |
| 19.2 | EXEC §6.1 *supplied* host column; HR-6; RT-5, RT-8; U-E15 (Depends) | A | U-E15 Owner "Host owner, **SQ-19 (a)**" → add "(answered: no host loop; D-58 successor is a SWBPIPE owner decision)". RT-5 host side → STD-2. |
| 19.3 | RS R2, R3, R5a (Depends) | N | None. |
| 19.4 | LOOP §13 Q-4 (Depends) | N | None. |
| 19.5 | HOSTING §8.2 (Depends) | N | None (App side). |
| 19.6 | CA W14-07, W14-08 (Depends) | V | States → STD-2. |
| 19.7 | C §10.1 "Agent: the host's single agent seat" | A | Append "(fixture; SWBPIPE has no seat concept, SQ-19 (d))". |
| 19.8 | GUIDE M5.6, M8.6; HC-5.5, HC-8.5 | V | STD-1. |

### SQ-20 Host-side placement (informational)

**Gist.** **Not decided** for the loop, panel assembly, persistence, hold
machine and required-tool check. Recorded direction: a later **"embedded
Runtime" adoption** (RUNTIME-ADOPT, planned) requiring immutable catalog
registration before the first turn, rebind and resume, and the modern MCP
condition if selected; the successor embedded mechanism is unresolved under
D-58: **OWNER DECISION**. #885 placement: native bridge in Rust; controller in
the desktop frontend; validation in the shared engine.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 20.1 | LOOP §1 "Minimal Chirality agent loop in the host (V4-ARC-10)"; §10.1 (Depends) | A | Per Part 3 item 7: add note after §1 Consequences: "SWBPIPE (SQ-20, SQ-29): no embedded loop exists or is selected; SWBPIPE records plan a later 'embedded Runtime' adoption (RUNTIME-ADOPT) with its successor unresolved under D-58 (SWBPIPE owner decision). This contract remains the App's receiving contract for a host loop under V4-ARC-10; whether that basis still describes SWBPIPE's direction is an owner question (R8-Q7)". |
| 20.2 | PANEL §8 Q-9 (Depends) | N | None. |
| 20.3 | EXEC U-E2 (Depends) | N | Effect add "SWBPIPE: not decided (SQ-20)". |
| 20.4 | GUIDE §2.13 TBD-004 "SQ-20, SQ-32 informational"; M7.1, M7.6; HC-7.6 | V | STD-1. |
| 20.5 | CA §2.2 CA/E | A | Covered by 04.2. |

### SQ-21 Faithful-record operation

**Gist.** **No.**

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 21.1 | ACT U-04(b), P-02; RS HA-9; C U-C11; LOOP Q-5; PANEL Q-5 (Depends) | C | U-C11 effect "None assumed in fixtures" → add "SWBPIPE: none (SQ-21)". Others: none. |
| 21.2 | GUIDE M5.4; HC-5.3 | V | STD-1. |

### SQ-22 Proposal views

**Gist.** Batch review (Operations → Review) shows steps as `field: before →
after`, diagnostics and the submitted JSON (rationale, source); Operation
apply, Operation ledger and Diff preview panels exist. **No stable external
reference scheme** (internal element and test ids only). Proposal cards and
table/canvas ghosts: DESIGN.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 22.1 | PANEL §8 Q-3; §4 (Depends) | A | Add to §4: "SWBPIPE views show old/new values per field (Batch review, Operation ledger, Diff preview), but offer no stable external reference to a position in them (SQ-22); panel references to host views are *not supplied* until one exists". |
| 22.2 | P §8; C §8 "proposal views" (Depends) | C | None: old/new values in host views exist. |
| 22.3 | XT IN-23; XC-02 J-7 | V | IN-23 → STD-1. |
| 22.4 | GUIDE M4.7, M7.7; HC-4.6, HC-7.5 | V | STD-1. |

### SQ-23 Display of lapse and related standings

**Gist.** Exists: a stale batch shows "The model changed. Prepare a new batch
from the current model."; Undo shows a session message. Not applicable: grant
supersession (no grants); "accepted, not applied: stale" (Apply is the
acceptance). DESIGN only: stale wording for the Checked mark, "superseded by"
rows. Not designed: a reversal marker.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 23.1 | PANEL §8 Q-4; §5 (Depends) | A | §5: add "SWBPIPE (SQ-23): stale batch message exists; lapse wording is DESIGN; supersession and accepted-then-stale do not arise; no reversal marker". |
| 23.2 | AS §3, §8 (Depends: R2-7, R2-15, R2-16) | A | §8: add the same note; R2-16 display has no SWBPIPE counterpart (see 01.6). |
| 23.3 | CA W14-06 host display input (SQ-23) | V | W14-06 inputs: "host lapse display (SQ-23)" → add "(answered: DESIGN only)". |
| 23.4 | GUIDE M5.5, M7.7; HC-5.4, HC-7.5 | V | STD-1. |

### SQ-24 Findings

**Gist.** No findings storage on main. DESIGN: agent cards (Check, Open
issue, Evidence summary) by reference, open/resolved, persisted with the
project (G-19, G-21). Whether storing a finding is a change: not decided.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 24.1 | C U-C5 (Depends) | C | Effect add "SWBPIPE: none on main; DESIGN cards by reference; change-or-not undecided (SQ-24)". |
| 24.2 | RS R10; PANEL §8 Q-7 (Depends) | N | None. |
| 24.3 | CA CA-3 host cell "where findings are held (SQ-24)" | A | Append "(answered: not stored on main; DESIGN only)". |
| 24.4 | GUIDE M1.5; HC-1.6 | V | STD-1. |

### SQ-25 Acts on host content captured through the App

**Gist.** **Host facility only.** The bridge assigns actor = agent; human
acceptance is recorded separately in the app; external tools cannot Apply;
computer-use clicks are not human acceptance. No proxy.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 25.1 | EXEC §5 CAP-1; U-E9 (Depends) | C | U-E9 effect "None offered" → add "SWBPIPE: host facility only, no proxy (SQ-25)"; Owner → "(answered)". |
| 25.2 | ADAPTER §7.6 (Depends) | C | None. |
| 25.3 | GUIDE M5.3; HC-5.6 | V | STD-1. |

### SQ-26 The extension-trace operation

**Gist.** **Not chosen.** SWBPIPE has **no catalog editions and no
edition-addition event**. Participation in the App's OI-003 decision:
**OWNER DECISION**. **Id collision:** SWBPIPE's OI-003 is a different item
(legal review of component and material data).

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 26.1 | C §8; editions e1/e2; V-ED1; UNRESOLVED "catalog-edition addition reported as an identified event" (Depends) | A | UNRESOLVED row effect "V-ED1 is a fixture; host event form unknown" → "V-ED1 is a fixture; SWBPIPE has no catalog editions and no edition-addition event (SQ-26)". |
| 26.2 | ADAPTER NM-4, OC-8 (Depends) | N | None beyond 12.1. |
| 26.3 | XT §4.1; IN-11; §5.2 (Depends) | V | IN-11 → STD-1 (gist "not chosen; no editions"). §5.2 "Current status `UNRESOLVED{OI-003}`" → "`UNRESOLVED{OI-003}` (App v4; distinct from SWBPIPE's own OI-003, SQ-26)". |
| 26.4 | RELAY and every file citing "OI-003" | A | Per Part 3 item 12. |
| 26.5 | CA EC-10; DI-8 | V | EC-10 → STD-1. |
| 26.6 | GUIDE §2.13 TBD-003; M1.1, M1.6; HC-1.1, HC-1.7 | V | STD-1. |

### SQ-27 Candidates, examination evidence and relay

**Gist.** (a) Contributions identified by commit SHA and PR merge commit, with
hosted CI run ids (full-SHA E2E dispatch), the DEC-025 local sweep, T9 byte
identity (Mac-only), native witness records and executable hashes, in
AgentRuns `_run_records` with SHA256SUMS. (b) Checks for first-activity work:
the operation contract corpus (81 invented cases) and #885's focused tests;
outstanding: clean sweep, native I1/I2, actual-human H1/H2; for any solve: T3
frozen references, both-entry gate, T9. (c) No relay form agreed; files with
hashes relayed by the human. (d) LIVE-HUMAN blocked until live implementation
and owner participation; deferred. (e) **Nothing needed from the App side**;
what moves the answers is the owner's direction.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 27.1 | CA §9; EC-11; §7.2 ladder; §8 W14-00 (Depends) | V | EC-11 → STD-1. W14-00 inputs: append "(SWBPIPE identifies contributions by commit/merge SHA, CI run ids, DEC-025 sweep, T9, witness records with SHA256SUMS — SQ-27 (a))"; state → STD-2. |
| 27.2 | CA "DEP-001 standing" (§9 closing paragraph; §5 host row "Owner-reported building; nothing received") | A | STD-5. §9 closing: "relay is **not observed**" → "relay recorded from the owner's statement; answers received 2026-09-28 (RELAY §4)". |
| 27.3 | EXEC TR-8, RT-11 (Depends) | N | None. |
| 27.4 | XT §2 IN-02; XC-00 (Depends) | V | IN-02 → STD-1. |
| 27.5 | XT §3.3 completion; IN-21; XC-02 | A | IN-21 "Not performed": add "(SWBPIPE LIVE-HUMAN witness blocked and deferred, SQ-27 (d))". |
| 27.6 | GUIDE M3.6, M8.7, M9.8; HC-0.1, HC-0.3; "evidence column of every row" | V | STD-1. |
| 27.7 | CA §6 ST-2 ("Answers with custody; not delivery") | C | ST-2 reached; add "(answers received 2026-09-28)". |

### SQ-28 Enablement facility for A13

**Gist.** **Facility exists: No** — not on main, not in #885, no plan found.
Reference exposed: No. State readable: No. Disable captured: No. **So under
the App's contracts the external channel stays *not enabled*.** Whether to
build one is an **OWNER DECISION**; no open item exists.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 28.1 | ACT §2.6 A13 row; "Still open" bullet 1; F-15; FX-47(c); U-04(e) (Depends) | V | Per Part 2 (P2.18). §2.6 "Still open: whether a given host requires its own facility to capture A13 (DEP-001, within U-04)" → append "SWBPIPE (SQ-28, 2026-09-28): no facility exists or is planned; A13 cannot be evidenced there; the channel stays *not enabled* (a SWBPIPE owner decision; ANS §2)". F-15: add "Confirmed by SQ-28: V4-EXM-25 cannot run against SWBPIPE until its owner adds a facility". |
| 28.2 | ADAPTER §3.1 host enablement record; §3.2; E-1…E-4, E-9; XF-01…XF-05; UNRESOLVED SQ-28 row; F-20 (Depends) | V | Per Part 2 (P2.18). UNRESOLVED SQ-28 row: Owner "Host owner (DEP-001)" → "SWBPIPE owner decision (A13 enablement facility; ANS §2)"; Point of need add "; when the owner resumes UI-SUCCESSOR (DECISION-3)"; Effect "XF-01…XF-05 host variants AWAITING INPUT" → STD-2. |
| 28.3 | CA CA-0; DI-9; EC-13; F-11; UNRESOLVED A13 row (Depends) | V | DI-9 "Not supplied; channel stays *not enabled* meanwhile" → "Answered (SQ-28): no facility exists or is planned; channel stays *not enabled*; a SWBPIPE owner decision". EC-13 → STD-1. F-11: add disposition "Confirmed by SQ-28 (2026-09-28)". UNRESOLVED row → owner as 28.2. |
| 28.4 | XT IN-15; XC-01, XC-12; §3.3 Gate; F-9 (Depends) | V | IN-15 "Not received / not performed" → "Answered (SQ-28): no facility, no plan; A13 cannot be evidenced; every live XC case is blocked until a SWBPIPE owner decision (§3.3 Gate)". F-9: disposition "Confirmed by SQ-28". XC-01, XC-12 → STD-2. |
| 28.5 | GUIDE §2.9 lead; M5.3, M9.1, M9.2, M9.8; HC-9.1 | V | STD-1; §2.9 lead: append "SWBPIPE answered SQ-28: no facility; the channel stays *not enabled*". |
| 28.6 | RELAY SQ-28 body | N | STD-6. |

### SQ-29 Model interface

**Gist.** **None exists, none selected.** Historically a Claude Agent SDK Node
sidecar (DEC-041), retired by D-58. The owner has reported a local model on
the Mac (oMLX), with "no silent cloud fallback" noted for a later check.
Recorded exchanges: none. Successor: **OWNER DECISION**.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 29.1 | LOOP §1, §4, §7 MC-6, MC-8, §11 fixture basis; UNRESOLVED DEP-05-01-024 (Depends) | A | DEP-05-01-024 row effect: add "SWBPIPE: no model interface exists or is selected; successor under SWBPIPE D-58 is an owner decision (SQ-29)". |
| 29.2 | GUIDE M2.4, M7.2; HC-2.4, HC-7.2; G-3 (Depends) | V | STD-1. |
| 29.3 | HOSTING §9 (Depends) | N | None. |
| 29.4 | CA EC-14 | V | STD-1. |

### SQ-30 Endpoint and key boundary

**Gist.** (a) No endpoint configuration and no key custody (`api_key` only as
a redaction key name). (b)–(e) Not decided; endpoint-redirect refusal not
decided. **Conflict for the App to note:** SWBPIPE DEC-051 open residency
allows an owner-configured provider, cloud included, with no app-side guard
"for now"; SPEC §4.4 lists key management, secret storage and egress
configuration as TBD — differs from the App's V4-HOST-02 local-only
expectation. **Reconciling them is an OWNER DECISION.**

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 30.1 | LOOP §5.1 NW-1…NW-7; N-OPEN-1…3; §5.2 MS-01…MS-11 (Depends) | A | Per Part 3 item 8. §5.1: add note "SWBPIPE DEC-051 (open residency, 'for now') differs from V4-HOST-02; reconciliation is an owner decision (SQ-30; R8-Q8). NW-1…NW-3 stay SETTLED from the App's accepted basis". N-OPEN rows Owner: add "; SWBPIPE DEC-051 owner decision". |
| 30.2 | GUIDE M7.3; HC-7.3; G-6; B-6 (Depends) | V | M7.3 standing → STD-1; G-6 add "SQ-30 surfaced DEC-051 vs V4-HOST-02 — an owner reconciliation (Part 4.2)". |
| 30.3 | V4-EXM-23 (DEL-09-07, outside) | N | None. |

### SQ-31 Malformed calls and validation order

**Gist.** No loop, so (a)–(d) not decided. Engine-side analogues (FACT):
strict preflight (exact keys, required fields, unknown fields rejected,
unsupported kinds refused) before simulation; malformed input → structured
error, "never a silent fallback"; nothing repaired or defaulted. #885 refuses
unknown or missing params (`invalid_request`) and any change other than
`position.x` (`unsupported_change`).

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 31.1 | LOOP §6 V-1…V-5, O-1; §7 MC-1…MC-9; T-OPEN-1; LH-0; FX-M1…M9 (Depends) | C | Engine posture agrees with MC "never coerced; never repaired". Add to T-OPEN-1 row effect "SWBPIPE: not decided (no loop; SQ-31)". |
| 31.2 | P §3.1 rule 5; U-P9 (Depends) | N | None. |
| 31.3 | GUIDE M2.4, M7.4, M7.6; HC-2.4 | V | STD-1. |
| 31.4 | WD I-7 / CA WR-6 constraint on the change request | A | Engine rejects unknown fields (SQ-31, SQ-02 (a)) — see R8-Q12. |

### SQ-32 Responsiveness

**Gist.** Placement not decided. FACT: the solve already runs as a background
job with poll and cancel. Observations can be relayed once a loop exists.
Numeric threshold not decided; the owner decides R-OPEN-1.

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| 32.1 | LOOP §8 RS-1…RS-4; R-OPEN-1; OI-013 (Depends) | C | R-OPEN-1 owner "Owner, if wanted" is consistent with SWBPIPE's answer; add "(SQ-32: SWBPIPE solve is a background job with poll/cancel)". |
| 32.2 | GUIDE M7.5; HC-7.4 | V | STD-1. |

### Cross-SQ rows (one row each, applying across SQ-01…SQ-32)

| # | Dependent | Cl | Proposed edit |
|---|---|---|---|
| X.1 | CA §9 "prepared" standings EC-01…EC-11, EC-13, EC-14 (all) and VC-CA-05 expected "nothing beyond *prepared*" | V | Every EC standing → STD-1; VC-CA-05 → "nothing beyond *answered*; no commitment, delivery or adoption". |
| X.2 | GUIDE standing vocabulary table (§0) and the 67 "relay pending" cells | V | Add a standing row **answered** ("A host answer about its current state was received (RELAY §4; ladder *answered*, CA §7.2); not a commitment, delivery, adoption or examination"); replace each "relay pending" with "answered (SQ-nn)" per its §4.3 home; UNRESOLVED row "Every SQ-01…SQ-32 answer (DEP-001) … Every 'relay pending' line stays *prepared*" → "Answered 2026-09-28 (RELAY §4); SWBPIPE owner decisions listed in ANS §2 remain open". |
| X.3 | XT §2 standing column "Not received" (IN-02, IN-09, IN-11, IN-14…IN-20, IN-23, IN-24, IN-26…IN-28) | V | STD-1 per row (gists in the SQ tables above). |
| X.4 | Consumed-inputs lines "SWBPIPE answers … none received (DEP-001)" (RELAY header line 21; EXEC "SWBPIPE host evidence: none received (DEP-001)"; CA; LOOP "DEP-001 host evidence has not been received"; PANEL line 16) | V | → "SWBPIPE answers received 2026-09-28 (RELAY_ANSWERS_SWBPIPE.md, sha256 64ea4e59…0689); no host evidence, commitment or contribution received (DEP-001)". |
| X.5 | EXEC §9.1 host-owner row "Prepared for relay, not delivered (RELAY §4 ledger)"; ACT/AS/RS/PANEL/LOOP DEP-001 standing text | A | → "Relayed; answered 2026-09-28; no commitment or contribution (RELAY §4)"; STD-5 where "owner-reported building" appears. |
| X.6 | ADAPTER §9 "Observed context — draft PR #885" | A | Append "SWBPIPE's answers (2026-09-28): PR #885 head `12907f393` is open, unmerged and **deferred** to UI-SUCCESSOR; the work graph's deferral governs over the PR description's 'reconfirmed proceeding' (ANS §3 item 11)". |
| X.7 | RELAY header status; UNRESOLVED rows "Delivery of this file" and "Every SQ-01…SQ-32 answer" | V | UNRESOLVED "Delivery" → closed ("relayed 2026-09-28, owner's statement"). "Every SQ answer" → "Answered 2026-09-28 (§4); remaining: SWBPIPE owner decisions (ANS §2), owner: SWBPIPE owner; point of need: when the owner resumes UI-SUCCESSOR". Header status "intake in progress" → on I4 completion "intake applied (R8)". |
| X.8 | SPIKE | N | No SQ dependency; no edit. |

---

## Part 2 — Value recomputation (SQ-02 and SQ-28)

### 2.0 The rules applied

- **R5-1** (value set) and **R6-1** (assignment by held actions), as written
  in EXEC §3.6 (owner of values):
  > "**HS-3** | App run on X; **every held action is a host operation** on the
  > external channel … | Depends on the status of SQ-02 … **(a)** SQ-02
  > answered, and host-held carriage or a host hold evidenced on a candidate →
  > **enforced on the host route**. **(b)** SQ-02 unanswered (today) → **not
  > established**. **(c)** SQ-02 answered with no host-held route, so the
  > constraint is only model-supplied or merely received → **not
  > enforceable** → *unsupported*."
  
  R6-1: "answered with no host-held route → *not enforceable*". HS-5 (any
  App-side held action) → *not enforceable* whatever SQ-02 returns.
- **EXEC §3.5 precedence** (INTEGRATION): any *not enforceable* → workflow
  *unsupported* ("checkpoint hold not enforceable on this surface: ‹name›");
  otherwise any *not established* → *not established*; otherwise passes.
- **R6-3**: under *not enforceable* nothing is stopped; actions are recorded as
  *action during hold*.
- **SQ-28 rule** (ACT §2.6, F-15; ADAPTER §3.2, E-1, E-3; R4-13; R5-10): A13
  is captured only by the host's enablement facility with a capture-evidence
  reference; without it no enablement is evidenced and the channel stays
  *disabled / not enabled*; SQ-28 gates every live CA/X and XC case.
- **Answer-handling rule** (RELAY §0): a case leaves AWAITING INPUT only when
  the answer supplies the named input.

**Reading applied.** SWBPIPE answered SQ-02 with **route (iv), none
planned**, (a) No, (c) No, (d) No/No, (f) No/No. That is "SQ-02 answered with
no host-held route" → **HS-3 (c)**. RELAY's answer form anticipated exactly
this: "If none of options (i)–(iii) is planned for the first increment, please
say so plainly: the App will then report checkpoints on host operations as not
enforceable on its surface rather than claim a hold."

**Reading question for the integrator (R8-Q1).** SWBPIPE says none is
planned, and that *whether to plan one* is an OWNER DECISION with no open item.
Does "none planned, owner may decide later" count as "answered with no
host-held route" (HS-3 (c)), or does the open owner decision keep it "a host
answer not yet given" (*not established*, HS-3 (b))? **Recommendation: HS-3
(c).** (1) The question asked what is planned for the first increment, and
the answer is plain; (2) *not enforceable* is defined as "no mechanism exists
on this surface **in this increment**", which is true; (3) *not established*
is reserved for "a host answer not yet given", and the answer has been given;
a later owner decision is a revision trigger (ANS §4), handled like any
changed answer; (4) both values fail the check, so no hold is claimed either
way, but (c) states the limit truthfully as *unsupported*. SWBPIPE's "related
fact" (every host operation resolves *propose* today) is **not** host-held
carriage (SWBPIPE says so; R2-12, R5-2) and moves no value. Integrator-level.

**Secondary question (R8-Q-HS4).** EXEC evaluates HS-4 (a held host operation
with *unagreed* exposure → *not established*) **before** HS-3. SWBPIPE has no
exposure element (SQ-11), so every real SWBPIPE entry is *unagreed*; HS-4
would keep real host-operation checkpoints *not established* although no
exposure answer could make them enforceable. The fixture is unaffected (FXA-1:
exposed on all surfaces). **Recommendation:** once SQ-02 is answered with no
host-held route, HS-3 (c) decides regardless of exposure (add to HS-4: "…
unless SQ-02 is answered with no host-held route, when HS-3 (c) applies").
Integrator-level.

### 2.1 Recomputed checkpoints and cases

"Old" is the value at HEAD; "New" applies HS-3 (c) (SQ-02) or the SQ-28 rule.
Workflow result per EXEC §3.5.

| P2 # | Case (surface X unless stated) | Checkpoint | Old → New hold support | Old → New workflow result | Where stated (each to edit) |
|---|---|---|---|---|---|
| P2.1 | **E1** ⟨rev-A2⟩ run from the App | `CP-accept` (held: OP-C4/OP-C5) | not established → **not enforceable** | unsupported → **unsupported** (unchanged); reason "…: CP-check" → "…: CP-accept, CP-check". "whatever SQ-02 returns; SQ-02 can move only `CP-accept`" → "SQ-02 answered (route (iv)); neither checkpoint can be enforced from the App on SWBPIPE's X" | EXEC §3.6 fixture table row `CP-accept`, Consequences bullet 1, MT-2; WD-EX E8 row E1-via-X; WD VC-37; C FXA-5; CA §2.2 ("Only `CP-accept` … is *not established*, and SQ-02 can move only that one" → "`CP-accept` is also *not enforceable* (SQ-02 answered, HS-3 (c))"), S-13, DI-6, ST-4, W14-04 (iii), F-15, UNRESOLVED D6; ACT §4.6 Consequences (E1 bullet), FX-48 (b); AS F18 variant; GUIDE §2.14 E1 row, HC-6.3; RS E10 intro not affected |
| P2.2 | E1 | `CP-check` (held: Return) | not enforceable → not enforceable (unchanged, HS-5) | — | no edit |
| P2.3 | **E1c** | `CP-check` | not enforceable (unchanged) | unsupported (unchanged) | no edit |
| P2.4 | **E1d** and **C V-GR1 via X** (run 13 carried to X) | `CP-grant` (held: the OP-C9 call) | not established → **not enforceable** | unsupported → **unsupported** (unchanged); reason now names `CP-grant` and `CP-check`; drop "SQ-02 can move only `CP-grant`" | EXEC §3.6 fixture row `CP-grant`, Consequences bullet 3; MT-16 (expected "`CP-grant` **not established** (HS-3 (b), awaiting SQ-02 (d))" → "`CP-grant` **not enforceable** (HS-3 (c): SQ-02 (d) answered No/No)"; state "DESIGNED (R6-1); `CP-grant`'s value AWAITING INPUT (SQ-02)" → "DESIGNED (R6-1; R8)"); WD-EX E8 row E1d-via-X; WD VC-37; C V-GR1 last sentence and FXA-5; RS E7 ("`CP-grant` hold support is **not established** (HS-3 on OP-C9, SQ-02 unanswered; R6-2)" → "**not enforceable** (HS-3 (c) on OP-C9; SQ-02 answered 2026-09-28)"); AS F14 ("From the App via X, `CP-grant` is **not established** (R6-2)" → "**not enforceable** (HS-3 (c); R8)"); GUIDE §2.14 E1d row; CA §2.2 ("E1d's `CP-grant` alone is *not established*" → "*not enforceable*"), W14-03 ("`CP-grant` not established" → "not enforceable"). On E: *enforced by the host loop* unchanged in meaning; SWBPIPE has no host loop (SQ-20), so no host evidence can exist now. |
| P2.5 | **L-WDEX-17** (E1d variant, `CP-grant` only) | `CP-grant` (OP-C9) | not established → **not enforceable** | **not established → unsupported** (value change) | WD-EX E8 row: hold cell → "HS-3 (c): **not enforceable** (SQ-02 answered 2026-09-28: no host-held route); would be *enforced on the host route* only if a host offered and evidenced one"; result cell "today **not established**; then passes or **unsupported** accordingly" → "**unsupported** — 'checkpoint hold not enforceable on this surface: CP-grant'"; GUIDE §2.14 L-WDEX-17 row; WD VC-43 ("**not established** today; **enforced on the host route** after an evidenced SQ-02 answer" → "**not enforceable** (SQ-02 answered, no host-held route); *enforced on the host route* only with a host-held route evidenced") |
| P2.6 | **L-WDEX-17 with held-actions element absent** | `CP-grant` (derived: the held OP-C9 call, R7-3) | not established → **not enforceable** | **not established → unsupported** (value change) | WD-EX E8 row (hold cell as P2.5; result "…so today **not established**; then passes or **unsupported** accordingly" → "…L-WDEX-17 has none, so **unsupported**"); GUIDE §2.14 row ("*not established* today; passes once SQ-02 is evidenced …; *unsupported* if answered with none" → "**unsupported** (SQ-02 answered with none)"); WD VC-43 tail ("→ HS-3 **not established** today … (L-WDEX-17 has none: **not established** today)" → "→ HS-3 **not enforceable** … (L-WDEX-17 has none: **unsupported**)") |
| P2.7 | **ACT `CP-L4`** (L-ACT-4), App run | `CP-L4` (held: the run's host operations after T16 until the A4) | not established → **not enforceable** | not established → **unsupported** (value change) | ACT §4.6 Consequences ("App run over X: *not established* until SQ-02 is answered;" → "App run over X: **not enforceable** (HS-3 (c); SQ-02 answered 2026-09-28) → workflow *unsupported*;"); FX-48 (c) ("`CP-L4` is HS-3, so it is *not established* while SQ-02 is unanswered." → "`CP-L4` is HS-3 (c): **not enforceable** (SQ-02 answered with no host-held route); the workflow is *unsupported*."). Host loop: unchanged. |
| P2.8 | **AS F6d** (L-AS-4 variant, App run) | the A4 checkpoint (held: host operations on S-4) | not established → **not enforceable** | requirement check not established → **unsupported** (value change) | AS F6d cell → "HS-3 (c): **not enforceable** (SQ-02 answered 2026-09-28: no host-held route) → requirement check *unsupported* ('checkpoint hold not enforceable on this surface'); nothing is stopped; run actions shown as action during hold. Counterpart: ACT `CP-L4`"; VC-03 ("host-operation-only → not established (F6d)" → "host-operation-only → not enforceable → unsupported (F6d; SQ-02 answered)"); VC-16 check wording (keep; add F6d expected *not enforceable*) |
| P2.9 | **RS E10 (vii)** (kind (a), only held action a host operation) | that checkpoint | not established → **not enforceable** | not established → **unsupported** (value change) | RS E10 (vii) ("→ HS-3: **not established** while SQ-02 is unanswered … ; *enforced on the host route* once …; *not enforceable* if answered with no host-held route." → "→ HS-3 (c): **not enforceable** — SQ-02 was answered on 2026-09-28 with no host-held route; requirement check *unsupported*; nothing stopped; action during hold recorded. (Would be *enforced on the host route* only with an evidenced host-held route.)"); VC-17 ("(vii) host operation only → **not established** now (never a pass), with its SQ-02-dependent alternatives" → "(vii) host operation only → **not enforceable** → *unsupported* (SQ-02 answered)"); VC-28 host-operation-only variant idem. RS E10 (i)–(vi): unchanged (HS-5). |
| P2.10 | **ADAPTER XF-25** (V-CP1 over X) | `CP-accept` | not established → **not enforceable** | *unsupported* on X | XF-25 ("Today: hold support **not established** (SQ-02 unanswered). Host-held variant: …" → "Hold support **not enforceable** (SQ-02 answered 2026-09-28: route (iv)), so the workflow is *unsupported* on X. Host-held variant (test double only; not offered by SWBPIPE): …"; state "— **AWAITING INPUT** (U-P10; SQ-02)" → "— DESIGNED (test double); host variant not offered (SQ-02)"); XT XC-10 Expected ("XF-25's `CP-accept` is *not established* until SQ-02 is answered, then *enforced on the host route* once …" → "XF-25's `CP-accept` is *not enforceable* (SQ-02 answered: no host-held route)"; state "XF-25 AWAITING INPUT (SQ-02)" → "XF-25 DESIGNED (SQ-02 answered)") |
| P2.11 | **ADAPTER XF-26** (model-supplied only) | `CP-accept` | not enforceable (expected; precondition now real) | unsupported (unchanged) | XF-26 state "DESIGNED; on a host candidate AWAITING INPUT (SQ-02)" → "DESIGNED; its precondition now holds for SWBPIPE (SQ-02 answered with no host-held route); on a host candidate HELD — host joins deferred (DECISION-3)". XT XC-10 (XF-26 clause "the variant in which SQ-02 is answered with no host-held route") — add "(the actual state since 2026-09-28)". XT IN-25 → "SQ-02 answered 2026-09-28: route (iv), none planned → HS-3 checkpoints *not enforceable* (*unsupported*); any App-side held action → *not enforceable*". |
| P2.12 | **EXEC CH-27** (V-CP1 family) | `CP-accept` over X | "before SQ-02 **not established**" → **not enforceable** | unsupported | CH-27 ("Over X: before SQ-02 **not established**; with host-held carriage evidenced **enforced on the host route**; with only model-supplied carriage **not enforceable** → unsupported" → "Over X: **not enforceable** → unsupported (SQ-02 answered 2026-09-28: no host-held route; HS-3 (c)); *enforced on the host route* would need an evidenced host-held route"); state "AWAITING INPUT (SQ-02; U-E13)" → "Over X: DESIGNED (value determined). On E: STD-2 (no SWBPIPE host loop, SQ-20)"; VC-E-02 "CH-27 per HS-3 (a)–(c), AWAITING INPUT (SQ-02)" → "CH-27 per HS-3 (c) (SQ-02 answered)"; VC-E-12 unchanged |
| P2.13 | **CA WR-11 / authoring advice** (not a case; the advice's premise) | — | "it can then become *enforced on the host route* once SQ-02 is evidenced" is no longer reachable on SWBPIPE | — | CA WR-11; WD §4.3.8 "Authoring advice"; EXEC §3.6 author bullet; WD-EX E8 last paragraph; ACT §4.6 "Advice to workflow authors"; GUIDE §2.14 last paragraph; CA F-15 remedy / §12.5: append "Against SWBPIPE (SQ-02 answered: route (iv)) this route is not available, so **no checkpoint is enforceable from the App on X in this increment**; every checkpointed workflow run from the App on X is *unsupported*. The advice stands for a host that offers a host-held route." |
| P2.14 | **ACT FX-50** | `CP-accept` (model-supplied) | "**not established** while SQ-02 is unanswered; **not enforceable** if the host holds no copy" → **not enforceable** | unsupported | FX-50 → "`CP-accept` hold support: **not enforceable** (SQ-02 answered 2026-09-28: the host holds no copy; model-supplied only). App side: `UNRESOLVED{D6}`." Remove "**HELD** on SQ-02". U-D6 "FX-48 and FX-50 are HELD" → "FX-48 and FX-50 are DESIGNED with determined values; App-side enforcement is `UNRESOLVED{D6}` (returned to the owner)". |
| P2.15 | **ADAPTER GC-3 / GC-5 / §2 outline** | A5 constraint; host-operation holds | the "(the state today)" marker moves to the *not enforceable* row | — | GC-3 table: row 2 "SQ-02 not yet answered, … (the state today)" → drop "(the state today)"; row 3 "SQ-02 answered and no host-held route exists …" → add "(the state since 2026-09-28: SQ-02 route (iv))". GC-5 HS-3 bullet ("*not established* while SQ-02 is unanswered; … *not enforceable* if SQ-02 is answered with no host-held route") → append "— the latter applies (SQ-02 answered 2026-09-28)". §2 "While SQ-02 is unanswered, the hold support is *not established*; if the answer leaves no host-held carriage or host hold, it is *not enforceable* (R5-1)." → "SQ-02 was answered on 2026-09-28 with no host-held carriage or host hold (route (iv)), so the hold support is *not enforceable* (R5-1)." Line "Until host evidence of constraint receipt exists, V-CP1 over X is **AWAITING INPUT** (U-P10; SQ-02)" → "V-CP1 over X is *not enforceable* → *unsupported* (SQ-02 answered)". UNRESOLVED D6 row → STD-4. |
| P2.16 | **Value-table and HS-3 "today" markers** (definitions, not cases) | — | "(today)" moves from (b) to (c) | — | EXEC §3.6 HS-3 row: "**(b)** SQ-02 unanswered (today) → **not established**." → "**(b)** SQ-02 unanswered → **not established**."; append after (c): "**Current state (SWBPIPE): (c)** — SQ-02 answered 2026-09-28, route (iv), none planned (R8)." WD §4.3.8 HS-3 row: "unanswered (today) → **not established**; answered with no host-held route → **not enforceable**" → "unanswered → **not established**; answered with no host-held route (**SWBPIPE, 2026-09-28**) → **not enforceable**". GUIDE §2.14 HS-3 row: "**not established** today (SQ-02 unanswered); …; → **not enforceable** if SQ-02 is answered with no host-held route" → "**not enforceable** (SQ-02 answered 2026-09-28 with no host-held route); *enforced on the host route* only with a host-held route evidenced on a candidate; never assumed"; its "What held means" "Today nothing is stopped; once enforced …" → "Nothing is stopped; actions are *action during hold*"; its effect "*not established* today; passes, or *unsupported*" → "*unsupported*"; "Changes when" → "A host offers a host-held route and it is evidenced". Value-definition rows "**not established** | Depends on a host answer not yet given (SQ-02), or on unagreed exposure" in EXEC §3.6, ACT §4.6, WD §4.3.8, GUIDE §0, AS §4, CA S-13, XT S-10: keep (generic), append "(SQ-02 was answered on 2026-09-28; for SWBPIPE only unagreed exposure, HS-4, can still give this value)". |
| P2.17 | **UNRESOLVED / D6 rows** | — | "HS-3 … *not established* until answered" | — | STD-4 in: EXEC U-E1 (effect "HS-3 values *not established* until answered" → "HS-3 values *not enforceable* (SQ-02 answered: none)"), U-E13 (STD-2); WD U-19 ("host-operation checkpoints in App runs are *not established* until answered" → "… are *not enforceable*: SQ-02 answered 2026-09-28, none"), U-30 ("App runs: HS-3 checkpoints *not established*" → "*not enforceable*"); WD-EX U-30 ("host-operation rows *not established*" → "*not enforceable*"), U-19 ("E8 App `CP-accept` and `CP-grant` *not established*" → "*not enforceable*"); ADAPTER D6 row; CA DI-6 ("on X, host-operation checkpoints *not established* until SQ-02" → "on X, host-operation checkpoints *not enforceable* (SQ-02 answered: none)") and D6 row; XT D6 row; GUIDE §2.13 D6 row and UNRESOLVED D6 row ("HS-3 *not established*" → "HS-3 *not enforceable*"); ACT U-D6; AS U-16; RS U-25; HOSTING U-23; LOOP and PANEL D6 rows; RELAY UNRESOLVED D6 row ("`CP-accept` on X *not established* until answered" → "`CP-accept` on X *not enforceable* (answered: none)") |
| P2.18 | **SQ-28: channel state for CA/X and every live XC/XF host case** | — (channel) | "*disabled* / enablement unconfirmed; AWAITING INPUT (SQ-28)" → **disabled (not enabled): no host A13 facility exists or is planned** | every live CA/X and XC case: AWAITING INPUT → STD-2 (**cannot run against SWBPIPE** until its owner provides a facility; host joins deferred, DECISION-3) | ACT §2.6, F-15, FX-47(c) ("A13, captured by the host with a capture-evidence reference, which is required (U-04e)" → add "— SWBPIPE has no facility (SQ-28); (c) cannot occur there; AWAITING INPUT per STD-2"); ADAPTER §3.1 (host enablement record supplier "relay **SQ-28**" → "SWBPIPE: none (SQ-28)"), §3.2 qualifier (13.1), XF-01…XF-05 host variants, UNRESOLVED SQ-28 row, F-20 (add "Confirmed by SQ-28"); CA CA-0 ("for CA/X the person enables external access (A13) in the host's enablement facility" → append "(SWBPIPE has none, SQ-28: CA/X cannot be enabled)"), §2.2 last paragraph ("CA/X also needs … (SQ-28); without it the external channel stays *not enabled*" → "… SWBPIPE answered SQ-28: no facility exists or is planned, so the external channel stays *not enabled*"), DI-9, EC-13, F-11, ST-4, UNRESOLVED; XT IN-15, §3.3 Gate (append "SWBPIPE answered SQ-28: no facility; the suite cannot run against it until a SWBPIPE owner decision"), XC-01, XC-12, F-9; GUIDE §2.9 lead, M9.1, M9.2, HC-9.1 |

**Cases whose value does not change** (for completeness): E1/E1c/E1d/V-GR1 on
E (*enforced by the host loop*, subject to host evidence; SWBPIPE has no host
loop, so that evidence cannot arrive now — see Part 4.6); every HS-5
checkpoint (E1 `CP-check`, E1c/E1d `CP-check`, AS F6c, RS E10 (i)–(vi), ACT
FX-48 (a)/(d), L-WDEX-15); HS-1 invalid declarations; HS-4 (fixture: no
unagreed exposure). Host-loop constraint fixtures (C V-CP1 on E, LOOP FX-C9,
PANEL PC-24, WD VC-11, WD-EX R-5a/R-5b, AS F6b, ACT FX-29) keep their
*meaning*; their status takes STD-2 (no SWBPIPE host loop or host-held
evaluation exists).

### 2.2 Every SQ-02 "not established" occurrence (17 files, body text)

Disposition codes: **VAL** a case/checkpoint value — edit per the P2 row
cited; **DEF** a value-set definition — keep, append P2.16 note; **HIST** a
finding or ruling-history row — keep, add disposition only where named;
**OTHER** not an SQ-02 value (declaration, exposure, mapping, harness) — no
edit. (Scan hits in "Changes from …" tables are HIST by rule and not listed.)

| File | Location | Code | Row |
|---|---|---|---|
| ACT | §4.3 R6-3 sentence ("under *not established* or *not enforceable* nothing is stopped") | DEF | — |
| ACT | §4.6 value table row *not established*; row *not enforceable* ("…once SQ-02 is answered…") | DEF | P2.16 |
| ACT | §4.6 HS-3 bullet "unanswered → *not established*" | DEF | keep; append "(SWBPIPE: answered with no host-held route, 2026-09-28)" |
| ACT | §4.6 Consequences: E1 `CP-accept` "**not established**, awaiting SQ-02" | VAL | P2.1 |
| ACT | §4.6 Consequences: `CP-L4` "App run over X: *not established* until SQ-02 is answered" | VAL | P2.7 |
| ACT | §4.6 "*Enforced on the host route* for the A5 constraint awaits host evidence and the SQ-02 answer (§4.4; U-04)" | VAL | → "SQ-02 answered 2026-09-28: no host-held route; *enforced on the host route* is not available against SWBPIPE (§4.4; U-04)" |
| ACT | FX-44 (iii) "sign-off" not established | OTHER | — |
| ACT | FX-48 (b), (c) | VAL | P2.1, P2.7 |
| ACT | FX-50 | VAL | P2.14 |
| ACT | §4.1 "An unrecognized name … **not established**" | OTHER | — |
| ADAPTER | §2 "While SQ-02 is unanswered, the hold support is *not established* …" | VAL | P2.15 |
| ADAPTER | §5.3 GC-3 table row 2 "(the state today)" | VAL | P2.15 |
| ADAPTER | §5.3 GC-3 note "before that answer the value is *not established* (R6-5)" | DEF | keep |
| ADAPTER | §5.3 GC-5 HS-3 bullet | VAL | P2.15 |
| ADAPTER | §5.3 "(HS-1: no value; the check is *not established*)" | OTHER | — |
| ADAPTER | §7.7 R6-3 sentence | DEF | — |
| ADAPTER | XF-25 "Today: hold support **not established**" | VAL | P2.10 |
| ADAPTER | §11 provide-to DEL-02-03 list "(channel not enabled; not established; unsupported …)" | DEF | — |
| ADAPTER | §13.2/§13.3 findings (F-16 area, F-18, F-19) | HIST | F-19: add "Applied: SQ-02 answered with no host-held route → *not enforceable* (R8)" |
| ADAPTER | UNRESOLVED D6 row "today *not established* for host-operation checkpoints" | VAL | P2.17 |
| ADAPTER | UNRESOLVED OC-8 row "NM-2: *not established* without a mapping"; XF-06, XF-07; §3.2 operation-unavailable | OTHER | — |
| ADAPTER | VC-X-03 ("model-supplied → *not enforceable* only once SQ-02 is answered …; *not established* before") | DEF | keep; append "(answered 2026-09-28)" |
| AS | §4 value list "**not established** (awaiting a host answer such as SQ-02, or unagreed exposure)" | DEF | P2.16 |
| AS | §4 HS-3 sentence "unanswered → *not established*; answered with no host-held route → *not enforceable*" | DEF | keep; append "(SWBPIPE: answered with none, 2026-09-28)" |
| AS | §4 R6-3 sentences | DEF | — |
| AS | F6d | VAL | P2.8 |
| AS | F14 last sentence | VAL | P2.4 |
| AS | F18 variant ("`CP-accept` **not established** (HS-3, SQ-02 unanswered)") | VAL | P2.1 → "`CP-accept` **not enforceable** (HS-3 (c), SQ-02 answered)" |
| AS | VC-03 ("host-operation-only → not established (F6d)") | VAL | P2.8 |
| AS | VC-16 | DEF | keep |
| C | §10.1 FXA-5 ("`CP-accept` **not established** (awaiting SQ-02)") | VAL | P2.1 → "`CP-accept` **not enforceable** (HS-3 (c): SQ-02 answered 2026-09-28)" |
| C | §10.4 V-GR1 last sentence ("`CP-grant` … is **not established** until SQ-02 is answered") | VAL | P2.4 → "…is **not enforceable** (EXEC HS-3 (c); SQ-02 answered 2026-09-28; R8)" |
| CA | S-13 | DEF | P2.16 + STD-4 wording ("deferred to the SWBPIPE answer to SQ-02" → "SWBPIPE answered SQ-02 with no host-held route (2026-09-28); D6 returns to the owner") |
| CA | §2.2 HS-3 bullet ("the value is **not established** while SQ-02 is unanswered …") | VAL | → "the value is **not enforceable**: SQ-02 was answered on 2026-09-28 with no host-held route (route (iv)); *enforced on the host route* would need a host-held route evidenced on a candidate" |
| CA | §2.2 "Only `CP-accept` (a host operation) is *not established*, and SQ-02 can move only that one." | VAL | P2.1 |
| CA | §2.2 "E1d's `CP-grant` alone is *not established*" | VAL | P2.4 |
| CA | DI-6 | VAL | P2.17 |
| CA | WR-2 (undeclared category) | OTHER | — |
| CA | WR-11 | VAL | P2.13 (and value words: "*not established* means the check does not pass yet" — keep as definition) |
| CA | ST-4 ("host-operation checkpoints stay *not established* until SQ-02 is evidenced") | VAL | → "host-operation checkpoints are *not enforceable* (SQ-02 answered: none), App-only checkpoints *not enforceable*: every checkpointed workflow on CA/X is *unsupported*" |
| CA | W14-03 ("`CP-grant` not established") | VAL | P2.4 |
| CA | W14-04 (iii) ("`CP-accept` (host operation) *not established* until SQ-02") | VAL | P2.1 → "`CP-accept` *not enforceable* (SQ-02 answered)"; (i) "depends wholly on the host route (SQ-02 (a)–(c))" → add "SQ-02 answered (a) No, (c) No: (i) has no SWBPIPE host route on X, and no SWBPIPE host loop on E (SQ-20)"; inputs "(iii) SQ-02 for `CP-accept` only" → "(iii) none (values determined)"; state → STD-2 |
| CA | F-10 (§12.3 disposition) | HIST | add "§12.6 R8: SQ-02 answered with no host-held route; the v0.2 finding ('every checkpointed workflow is *unsupported* on the App/external surface') holds again for SWBPIPE" |
| CA | F-15 | HIST | add R8 disposition per P2.13 |
| CA | UNRESOLVED D6 row | VAL | P2.17 |
| WD-EX | E8 precedence sentence | DEF | — |
| WD-EX | E8 row E1-via-X `CP-accept` | VAL | P2.1 |
| WD-EX | E8 row E1d-via-X `CP-grant` | VAL | P2.4 |
| WD-EX | E8 rows L-WDEX-17 (both) | VAL | P2.5, P2.6 |
| WD-EX | E8 R6-3 paragraph | DEF | — |
| WD-EX | UNRESOLVED U-30, U-19 | VAL | P2.17 |
| WD-EX | E5/E7 "undeclared → not established" | OTHER | — |
| EXEC | §3.5 check-result row *not established* | DEF | — |
| EXEC | §3.6 value table rows | DEF | P2.16 |
| EXEC | §3.6 HS-1, HS-4 | OTHER / R8-Q-HS4 | HS-4 per R8-Q-HS4 |
| EXEC | §3.6 HS-3 row "(b) SQ-02 unanswered (today)" | VAL | P2.16 |
| EXEC | §3.6 fixture table rows E1 `CP-accept`, E1d `CP-grant` | VAL | P2.1, P2.4 |
| EXEC | §3.6 Consequences bullets 1 and 3 | VAL | P2.1, P2.4 |
| EXEC | §3.6 GC-3/GC-5 paragraph ("Before that answer, the value is **not established**") | DEF | keep; append "(answered 2026-09-28: *not enforceable*)" |
| EXEC | MT-2 | VAL | P2.1 |
| EXEC | MT-16 | VAL | P2.4 |
| EXEC | CH-27 | VAL | P2.12 |
| EXEC | §8 register row "ADAPTER U-X3 … *not established* before SQ-02" | VAL | → "GC-3 and GC-5 follow §3.6 HS-3: SQ-02 answered 2026-09-28 with no host-held route → *not enforceable*"; status "**Resolved** … host side AWAITING INPUT (SQ-02)" → "**Resolved** (R5-1, R5-2, R8); host side answered: none" |
| EXEC | U-E1 | VAL | P2.17 |
| EXEC | VC-E-12 ("model-supplied carriage → *not enforceable* after SQ-02, *not established* before") | DEF | keep |
| EXEC | CR-3, CR-10, EV-1…EV-4, EV-7, CF-1, CF-3, TF-4, TF-8, MT-8…MT-10, CH-26, CH-29, RT-4, U-E10, U-E18, §4.14 | OTHER | — |
| XT | S-10 | DEF | P2.16; STD-4 wording |
| XT | IN-25 | VAL | P2.11 |
| XT | XC-10 | VAL | P2.10, P2.11 |
| XT | F-10 (§9.3) | HIST | add "R8: SQ-02 answered: XC-10's A5 case is *not enforceable*" |
| XT | UNRESOLVED D6 row | VAL | P2.17 |
| GUIDE | §0 hold vocabulary | DEF | P2.16 |
| GUIDE | M8.3 | DEF | — |
| GUIDE | §2.14 HS-1, HS-4 | OTHER / R8-Q-HS4 | — |
| GUIDE | §2.14 HS-3 row | VAL | P2.16 |
| GUIDE | §2.14 fixture rows E1, E1d, L-WDEX-17 (both) | VAL | P2.1, P2.4, P2.5, P2.6 |
| GUIDE | HC-6.3 ("Until answered, checkpoints on X whose every held action is a host operation are *not established*") | VAL | → "Answered 2026-09-28: none; such checkpoints are *not enforceable*" |
| GUIDE | §5 rulings-applied table (R6-1, R6-2, R7-3 rows) | HIST | — |
| GUIDE | UNRESOLVED D6 row "HS-3 *not established*" | VAL | P2.17 |
| GUIDE | VC-G-03 | DEF | — |
| LOOP | §2.4.4 value list; invalid-declaration row; App-run classification row | DEF | keep |
| LOOP | Findings G-? line ("*not enforceable* after SQ-02 and *not established* only before") | HIST | — |
| LOOP | FX-C13; required-act-kind row | OTHER | — |
| P | §3.3 ("**not established** while SQ-02 is unanswered, and **not enforceable** only once SQ-02 is answered …") | VAL | 02.7 |
| P | §4.4 value list | DEF | — |
| P | VC-P-06 (b) | OTHER | — |
| PANEL | §3.2 rows | OTHER | — |
| RS | E7 V-GR1 via X | VAL | P2.4 |
| RS | E10 (vii) | VAL | P2.9 |
| RS | VC-17 (vii); VC-28 | VAL | P2.9 |
| RS | R8, R11 inventory, L-12 | OTHER / DEF | — |
| RELAY | SQ-02 "App assumes meanwhile" (three occurrences) | — | STD-6 (not edited) |
| RELAY | UNRESOLVED D6 row | VAL | P2.17 |
| WD | §4.3.3 R6-3 sentence; §4.3.8 value rows; "What held means" | DEF | P2.16 |
| WD | §4.3.8 HS-3 row | VAL | P2.16 |
| WD | §4.3.8 closing ("SQ-02's answer can move *not established* rows to *enforced on the host route* …") | VAL | → "SQ-02 was answered on 2026-09-28 with no host-held route, so HS-3 rows are *not enforceable* against SWBPIPE; checkpoints holding any App-side step stay *not enforceable* (R5-10; R6-1; U-30); D6 returns to the owner" |
| WD | U-19, U-30 | VAL | P2.17 |
| WD | VC-37 ("E1 `CP-accept` … HS-3 **not established**"; "E1d `CP-grant` … HS-3 **not established**") | VAL | P2.1, P2.4 |
| WD | VC-43 | VAL | P2.5, P2.6 |
| WD | VC-33 ("no hold support is *not established*") | DEF | — |
| WD | §3.4 table, §4.2.4, FB-02/04/05/06, VC-06, VC-12, VC-25, U-23, §8 row | OTHER | — |
| HOSTING | §6.7 lead; HP-H bullet; U-23 | VAL (wording) | 02.17 |
| HOSTING, SPIKE | "attribution … not established"; "not established and not indicated" | OTHER | — |

---

## Part 3 — The 12 contradicted or qualified assumptions (ANS §3)

Each row: what is affected; options; recommendation and reason; level.
"Integrator" = R8 can decide; "Owner" = bring to the owner.

**1. Direct external apply returns `unsupported_method`, not *not permitted*
naming a rule (SQ-06).**
- *Affected:* ADAPTER RP-3 (rows "Direct requested …", "Operation performs A4,
  A5 …"), RP-4, M-2, XF-24, XF-27; ACT §6 rows 6–8; R2-4 ("reserved entries are
  always offered … never reported 'not exposed on this surface'"); R2-12
  (direct under constraint → *not permitted*); XT XC-10; GUIDE M9.4, HC-9.3.
- *Options:* (a) relay `unsupported_method` as host-reported and classify it
  *not exposed on this surface* (SWBPIPE's own SQ-09 mapping), recording that
  the host offers no Apply/direct method on X and that R2-4 is not met by that
  host (DEP-001); (b) classify it *not permitted* with a governing treatment
  "host channel rule" — the App would be authoring a host treatment the host did
  not state (contradicts M-2, RP-4, S-X3); (c) *missing*/*error*.
- *Recommendation:* **(a)**. It relays exactly what the host said, keeps
  *not permitted* reserved for host-stated treatments, and never presents the
  no-Apply rule as a class value or grant. Whether SWBPIPE's rule is a channel
  rule or a first-journey property is SWBPIPE's owner decision; the App needs
  nothing from it now. Note also: SWBPIPE has no direct mode at all (SQ-05), so
  RP-3's direct rows and R2-12's "not permitted naming the constraint" have no
  SWBPIPE occasion.
- *Level:* **Integrator** (receiving mapping; ADAPTER/ACT owners apply).

**2. Staleness is whole-model; applying one proposal stales all others; R2-13
per-item does not hold (SQ-07 (d)).**
- *Affected:* **R2-13** (second half: per-item trigger by relied-on targets'
  subject identities; siblings not staled); C §5.4 "No longer holds"
  (INTEGRATION), U-C3; P §5 Trigger; ADAPTER XF-14; LOOP FX-D2, §6.3; XT XC-03;
  CA CA-4; WD-EX R-7. R2-13's first half (de-duplication before the basis
  check) **holds** in DRAFT #885 (SQ-08 (b)).
- *Options:* (a) keep R2-13 as the contract rule and record SWBPIPE as
  non-conforming (DEP-001), relaying its stale refusals unchanged; (b) amend
  R2-13: the per-item rule applies where a host supplies subject identities;
  otherwise the App receives the host's declared staleness **scope** (e.g.
  "whole model") and shows it ("refused — stale (host scope: whole model;
  relied ⟨rev/hash⟩, current ⟨rev/hash⟩); failing targets not supplied");
  (c) adopt whole-model as the contract rule.
- *Recommendation:* **(b)**. It keeps the stronger rule for hosts that can meet
  it, receives SWBPIPE truthfully without the App recomputing staleness, and
  leaves the de-duplication precedence untouched. (c) would weaken the
  contract for every host because of one host's current state.
- *Level:* **Integrator** (R2-13 is an INTEGRATION ruling); inform the owner
  because V4-EXM-25's stale case (XC-03) will show whole-model staleness on
  SWBPIPE.

**3. No per-row/per-object subject identities; only the whole-model hash
(SQ-03).**
- *Affected:* R-6 (content identities and acceptance binding), R2-14
  (resulting objects with post-application subject identities), R2-17 / R3-1
  / R3-2 (subject binding through subject identities), C §5.3, FXA-2, FXA-3,
  P §9 applied row, RS L-1/L-2, WD §4.3.6 SB-1…SB-3; accepted basis V4-HI-32
  ("a row's content hash").
- *Options:* (a) keep; record SWBPIPE as not supplying subject identities;
  host-content binding and lapse cases stay fixture-only; (b) receiving rule:
  where a host supplies only a whole-model identity, the App receives it as
  the subject content identity of **every** subject read (method designation
  and scope as the host states them), so acts lapse and items stale on any
  model change — conservative, never under-reporting a lapse; resulting objects
  beyond target ids are *not supplied*; (c) the App computes per-row identities
  from host reads.
- *Recommendation:* **(b)**, with (a)'s DEP-001 record. (c) is rejected: C §5.3
  requires host-supplied identities, and an App-computed one is App-assured,
  not host evidence. SWBPIPE's DESIGN Checked mark (DEC-104) carries a
  row-content hash, so per-row identity may arrive with that tranche (a
  SWBPIPE owner decision).
- *Level:* **Integrator** (receiving rule; V4-HI-32 is not changed); owner
  notice that SWBPIPE does not yet meet V4-HI-32.

**4. "Opt-in" is an environment variable plus a build feature; not a person's
act; no "channel not enabled" code; state not readable (SQ-13, SQ-28).**
- *Affected:* ACT §2.6, F-15; ADAPTER §3.1–§3.3 (E-1…E-9), OC-4, XF-01…XF-07,
  XF-35; C §4.1 *channel not enabled* (host reporter; R4-16); R4-13; XT S-11,
  IN-15, XC-01, XC-12, §3.3 Gate; CA CA-0, DI-9, EC-13; GUIDE M9.1, M9.2.
- *Options:* (a) keep the App contract: A13 is never evidenced on SWBPIPE, the
  channel stays *not enabled*, live CA/X and XC cases cannot run until a
  SWBPIPE facility exists; SWBPIPE's "off" (`controller_unavailable`, no
  socket) is App-reported *endpoint-unavailable*, and the host is never the
  reporter of *channel not enabled*; (b) the owner accepts a person-set launch
  environment variable as A13 evidence for development candidates (changes the
  reading of D2e and R4-13); (c) App-side A13 capture (rejected by R4-13: an
  agent could write the configuration).
- *Recommendation:* **(a) now**. Host joins are deferred (DECISION-3), so
  nothing is blocked today; (b) is an owner option to revisit when UI-SUCCESSOR
  resumes. Also record: with the variable set, the SWBPIPE CLI answers requests
  even though the App shows the channel *disabled*; an agent-originated native
  call that reaches it is recorded as observed with the evidence limit "host
  reachable without evidenced A13", never shown as *enabled* and never counted
  as an examination result (ADAPTER E-2, E-3).
- *Level:* (a) **Integrator**; (b) **Owner** (not needed now).

**5. Queue-time basis is true of main's offline intake; PR #885 freezes the
inspected basis but is unmerged (SQ-07 (c)).**
- *Affected:* C §5.4 receiving-risk paragraph; P §12 row 1; XT XC-03; CA CA-4.
- *Options:* (a) no change; (b) annotate the risk: confirmed on main; DRAFT
  #885 would retire it if merged and qualified.
- *Recommendation:* **(b)** (edits 07.2, 07.6). No value changes.
- *Level:* **Integrator**.

**6. The caller: SWBPIPE records name a development Codex, not the App's
Codex.**
- *Affected:* CA §2.2 CA/X, S-3; XT §3; ADAPTER §5.4; SQ-04 (c); DECISION-3
  (defers naming the App's Codex as a caller).
- *Options:* (a) record the fact; naming the App's Codex is the owner's
  (already deferred by DECISION-3); App records keep "external agent
  (unverified identity)"; (b) adopt "development Codex" as the App's
  expression — no, the App's expression is the App's Codex.
- *Recommendation:* **(a)** — notes 04.2 and Part 4.5. No new owner decision is
  needed now; DECISION-3 already holds it.
- *Level:* **Integrator** (note); the naming itself is **Owner** (deferred).

**7. The embedded direction: SWBPIPE plans a later "embedded Runtime"
adoption, successor unresolved; the App's "minimal host loop" does not appear
in SWBPIPE records (SQ-20, SQ-29).**
- *Affected:* LOOP (whole; §1 on V4-ARC-10), PANEL, CA §2.2 CA/E, GUIDE row 7
  (M7.x), HC-7, EXEC U-E2, LOOP DEP-05-01-024.
- *Options:* (a) keep LOOP/PANEL as the App's receiving contracts for any host
  loop under V4-ARC-10 and add the SWBPIPE note (20.1); (b) re-scope DEL-05-01
  to be mechanism-neutral ("an embedded agent in the host", covering an
  embedded Chirality Runtime with immutable catalog registration, rebind and
  resume); (c) pause DEL-05-01/05-02.
- *Recommendation:* **(a) now**, and bring the question to the owner:
  V4-ARC-10 (minimal Chat-Completions loop) is accepted basis, and SWBPIPE's
  D-58 successor is SWBPIPE's owner decision; only the owner can reconcile
  them. The four-subject boundary (LOOP §2) is already fairly neutral, so (b)
  is a later, small change if the owner chooses Runtime adoption.
- *Level:* **Owner** (information and choice; no change forced now).

**8. Local-only: SWBPIPE DEC-051 allows cloud providers with no guard "for
now" (SQ-30).**
- *Affected:* LOOP §5.1 NW-1…NW-7, §5.2 MS-01…MS-11, N-OPEN-1…3; GUIDE B-6,
  G-6, M7.3, HC-7.3; accepted basis V4-HOST-02 (and V4-EXM-23, DEL-09-07).
- *Options:* (a) keep V4-HOST-02 for the host embedded agent's receiving
  contract; record the conflict; (b) the owner revises V4-HOST-02 toward open
  residency (consistent with the flexibility he chose for the App in D5);
  (c) the owner revisits DEC-051 toward local-only.
- *Recommendation:* **(a) meanwhile**; the reconciliation is the owner's and
  is not needed until an embedded host agent exists (SQ-29: none). Present (b)
  and (c) side by side, noting D5's emphasis on user flexibility.
- *Level:* **Owner** (both records are the owner's).

**9. "Single agent seat" is not a SWBPIPE concept (SQ-19 (d)).**
- *Affected:* WD S-M, §5.3 SEAT-1…SEAT-3, U-09, FB-12; C §10.1 "the host's
  single agent seat"; PANEL §1; PRD V4-HOST-05/06 (roles recede behind one
  agent seat).
- *Options:* (a) keep SEAT-1…3 as App receiving obligations (they hold for any
  mapping; FB-12 records *unknown*), and note SWBPIPE's one agent panel as
  the likely counterpart; (b) drop the seat concept (would depart from PRD
  basis).
- *Recommendation:* **(a)** (edits 19.1, 19.7).
- *Level:* **Integrator**.

**10. `withdrawn` in PR #885 means the person cleared the queue, not the
proposer withdrawing (SQ-05 (g), SQ-09).**
- *Affected:* P §4.1 *withdrawn* (A11, proposer), §9 row; ACT A11; U-P6;
  ADAPTER E-8 and XF-35 ("never *withdrawn*"); RELAY SQ-09 mapping.
- *Options:* (a) map #885 `withdrawn`/`cleared_in_review` to an **item-left
  event "cleared by the person in host review, without a decision record"**
  (reporter host) — never A10 (no rejection record), never A11 (not the
  proposer); (b) map to *rejected* — fabricates A10; (c) map to *withdrawn* —
  wrong actor.
- *Recommendation:* **(a)**; add it to P §4.2 transitions and the ADAPTER
  received-vocabulary table (09.1). Likewise `rejected: validation_rejected`
  → *refused — invalid* at application, never A10.
- *Level:* **Integrator** (P owner DEL-03-02 applies).

**11. PR #885's readiness: its description's "reconfirmed proceeding" predates
the work graph's deferral, which governs.**
- *Affected:* ADAPTER §9 "Observed context"; XT IN-09; CA DEP-001 standing;
  C/P receiving-risk rows citing `e548d4cf`.
- *Options:* (a) annotate PR #885 evidence as deferred (X.6) and update the
  DEP-001 standing (STD-5); (b) leave.
- *Recommendation:* **(a)**.
- *Level:* **Integrator**.

**12. Id collision: SWBPIPE's OI-003 is a different item from the App's
OI-003 (SQ-26).**
- *Affected:* every App file citing `OI-003` / `UNRESOLVED{OI-003}` (C U-C7,
  §8; ADAPTER NM-4, OC-8, UNRESOLVED; XT §4–§5, IN-12; GUIDE TBD-003, M1.6;
  EXEC U-E18; WD U-23; CA DI-8; RELAY SQ-11, SQ-26).
- *Options:* (a) project-qualify the App's identifier where text crosses
  projects or is relayed ("App v4 OI-003"); (b) rename the App's item.
- *Recommendation:* **(a)**: add one line to each file's identifier notes (or
  first use): "OI-003 here is the App v4 open issue (extension promise); it is
  unrelated to SWBPIPE's OI-003". Renaming would break register pointers.
- *Level:* **Integrator**.

---

## Part 4 — Other consequences

**4.1 OI-021 remains open.** SQ-04 selects nothing; choosing is the owner's
with the App/shared owner. The answers supply a candidate list (27 change
kinds; DRAFT #885's `position.x` set_field; validate-only preview; solve
integrity standing; user rule checks) and show that FX-PIPE-01's operations
(supports, stiffness, labels) are not SWBPIPE catalog identities (SWBPIPE has
no per-operation identity, SQ-12). Keep `UNRESOLVED{OI-021}` everywhere; add
the candidate note to CA DI-1 (04.1). No owner decision is needed now (host
joins deferred). **Integrator** (note only).

**4.2 V4-HOST-02 vs DEC-051.** See Part 3 item 8. The App's D5 (App
conversations may use cloud models, no gate) and V4-HOST-02 (host embedded
agent local-only) are different paths (GUIDE G-6); SWBPIPE's DEC-051 concerns
the host embedded path and conflicts with V4-HOST-02. **Owner**, when an
embedded host agent is selected (SQ-29: none now).

**4.3 Whole-model identity vs subject content identity (R2/R3 content
identities).** Part 3 items 2 and 3. Additional points: (i) SWBPIPE binds an
Apply by operation id + claimed whole-model hash + per-field before-values
(SQ-03 (c)) — close to R-6's change-item content identity (target, old/new
values, relied basis), so A5 binding is *partly* supported; (ii) R3-1's
subject class "objects a named output concerns" and R3-2's "targets of the
held call" bind through subject identities as read — under R8-Q3 they bind to
the whole-model identity on SWBPIPE; (iii) T3 solver receipts (receipt and
publication sha256 over the published result envelope) identify analysis
results and could later serve as the content identity of a *named output*
(host check result, C OP-C12-like) — a note for C §6.2, not a ruling now.
**Integrator** (R8-Q2, R8-Q3).

**4.4 `unsupported_method` vs *not permitted*.** Part 3 item 1 (R8-Q-item-1).
Consequence for V4-EXM-25 design: XC-10's "authority differences reported as
*not permitted* naming the treatment" (ADAPTER RP-2) will show *not exposed on
this surface* on SWBPIPE; XC-10's expected text should add "or a host-reported
refusal of the method (`unsupported_method`) where the host offers no such
method". **Integrator**.

**4.5 The caller naming.** SWBPIPE names a development Codex controller first
and an embedded agent later; the App's Codex is not named (A-4, SQ-04 (c)).
DECISION-3 defers naming the App's Codex as a caller. Effect: every CA/X and
XC case depends on that owner decision **and** on SQ-28's facility. No App
edit beyond 04.2 and the XT §3.3 Gate note. **Owner** (already deferred).

**4.6 The embedded direction.** Part 3 item 7. Additional consequence: every
"enforced by the host loop" value (HS-2) and every CA/E case (W14-04 (i)/(ii)
"run it first on the host loop (CA/E)") depends on a host loop that SWBPIPE
does not have and has not selected. CA F-10's fallback ("the first activity's
checkpoint cases therefore run on the host loop (CA/E) first") is therefore
not available against SWBPIPE now. Combined with P2.13 (no enforceable
checkpoint on X), **no checkpointed workflow can be examined as enforced
against SWBPIPE in this increment** on either surface. This is the owner-facing
consequence of SQ-02 + SQ-20 and belongs with the D6 return (R8-Q-D6).
**Owner**.

**4.7 No capability catalog in SWBPIPE (added).** SWBPIPE has one engine
route with 27 change kinds, no per-operation identity or version (SQ-12,
SQ-18 (e)), no catalog editions (SQ-26), no exposure element (SQ-11) and a
hand-built CLI (SQ-12). HI §2 / V4-HI-02 (catalog) is accepted basis for new
hosts; SWBPIPE's current state does not meet it. Consequences: WD required-tool
references (catalog identity and version, CA WR-4) cannot resolve against
SWBPIPE (EXEC EV-4 → *not established*); C's contract, V-ED1 and the OI-003
extension trace have no SWBPIPE counterpart. Recommendation: record (12.1,
12.3, 26.1); no App rule change. **Integrator** (record); owner notice.

**4.8 V4-EXM-14 round trip has no host side (added).** SQ-17…SQ-19: no
workflow library, no declaration reader, no host runs. OUT-003 of DEL-09-06
cannot complete against SWBPIPE until a SWBPIPE work item receives App
workflows (ANS §4). CA F-1 already says OUT-003 cannot complete in this
undertaking; add this second reason (17.4). **Integrator** (record); owner
notice.

**4.9 Accept = apply; batch-level decisions; session undo (added).** SWBPIPE's
A5 is Apply (acceptance and application together), per batch, atomic; Clear
discards without a record; undo is a session snapshot without receipt
(SQ-01, SQ-09, SQ-10, SQ-23). App receiving meanings that have no SWBPIPE
counterpart: accepted-then-stale (R2-16), per-item A5/A10 and mixed items
(R2-18, C T11), A10 records, *reverses ⟨receipt⟩* (R2-15, R3-4). Keep them as
App/shared meaning; record the gaps (01.6, 09.3, 10.1). **Integrator**
(R8-Q13, R8-Q15).

**4.10 Grant display for a host with no grant model (added).** SWBPIPE has no
classes and no grants (SQ-05). AS §3's display states assume a host grant
(R2-6 *effective (policy default)* needs a policy record). Proposed rule for
when joins resume: show "host fixed treatment: every change waits for the
person's Apply (host-stated)", never a grant state, never "not set". Not
needed now (host joins deferred). **Integrator** (R8-Q16, may defer).

**4.11 UNRESOLVED rows whose owner or point of need should change.**

| File: row | Change |
|---|---|
| RELAY: "Delivery of this file to the SWBPIPE session" | Close (relayed 2026-09-28, owner's statement). |
| RELAY: "Every SQ-01…SQ-32 answer" | Close as answered; new residual row "SWBPIPE owner decisions (ANS §2)": owner **SWBPIPE owner**; point of need **when the owner resumes UI-SUCCESSOR** (DECISION-3). |
| RELAY, CA, XT, ADAPTER, C: "Host restriction of its own channel by model destination (SQ-16)" | Close: answered, no restriction. |
| D6 rows — EXEC U-E1; WD U-19/U-30; WD-EX U-19/U-30; ACT U-D6; AS U-12/U-16; RS U-19/U-25; ADAPTER D6 and U-P10 rows; CA DI-6 and D6 row; XT D6 row; GUIDE §2.13 D6 row and UNRESOLVED D6 row; HOSTING U-23; LOOP and PANEL D6 rows; RELAY D6 row; P U-P10 | STD-4: owner "Owner, deferred to SWBPIPE SQ-02" → "Owner (D6 returned: SQ-02 answered, none planned)"; effect per P2.17. Point of need unchanged. |
| SQ-28 rows — ADAPTER UNRESOLVED SQ-28; CA A13 row, DI-9; XT IN-15; ACT U-04(e); GUIDE M9.1 | Owner "Host owner (DEP-001)" → "SWBPIPE owner decision (A13 enablement facility; ANS §2)"; point of need add "when the owner resumes UI-SUCCESSOR (DECISION-3); before any live CA/X case". |
| Durable de-duplication — ADAPTER identity row; P U-P1 | Owner → "SWBPIPE owner decision (durable receipt carrier)". |
| Capture-evidence reference — EXEC U-E12; WD U-05b; RS U-11; AS U-07; ACT U-04(a); ADAPTER capture row | Owner → "SWBPIPE owner decision (PB-TBD-002; DEL-16-03 actor identity)". |
| Autonomy — ACT U-01 residue, U-06; AS U-04; P U-P6 | Add "SWBPIPE autonomy is owner decision OI-016". |
| Host loop / model side — LOOP DEP-05-01-024, N-OPEN-1…3, T-OPEN-1; EXEC U-E2, U-E15; GUIDE TBD-004 and the DEP-05-01-024 row | Add "SWBPIPE successor embedded mechanism is owner decision D-58 (SQ-20, SQ-29)"; N-OPEN rows add DEC-051 (SQ-30). Point of need unchanged. |
| Workflow receiving — EXEC U-E14; CA "DEP-001 contributions EC-01…" row | Owner → "SWBPIPE owner decision (a work item to receive App workflows; ANS §4)". |
| MCP choice — ADAPTER OC-1 (UNRESOLVED TBD-007 row) | Add "SWBPIPE: CLI; any MCP adapter is a SWBPIPE owner decision (modern-client condition)". |
| OI-003 rows — C, ADAPTER, XT IN-12/§5.2, GUIDE TBD-003, EXEC U-E18, WD U-23, CA DI-8 | Qualify "App v4 OI-003" (Part 3 item 12). |
| C U-C3, U-C4, U-C5, U-C6, U-C9, U-C10, U-C11; P U-P2, U-P3, U-P4, U-P5, U-P7, U-P8 | Effects updated per rows 03.1, 07.3–07.5, 18.2, 21.1, 24.1, 03.3, 07.6, 09.2, 10.1 (owners unchanged). |
| U-09 seat (WD, LOOP) | Effect add "SWBPIPE: no seat concept (SQ-19 (d))"; owner and point of need unchanged. |

---

## Part 5 — Rulings needed (for I3 / R8), with recommendations

| ID | Question | Recommendation | Level |
|---|---|---|---|
| **R8-Q1** | Does "route (iv), none planned; planning one is an OWNER DECISION" count as "SQ-02 answered with no host-held route" (HS-3 (c))? | **Yes → *not enforceable***; value changes per Part 2 (P2.1–P2.17). A later owner decision to plan a route is a revision trigger. | Integrator |
| **R8-Q-HS4** | Once SQ-02 is answered with no route, may HS-4 (unagreed exposure → *not established*) still pre-empt HS-3? | **No**: HS-3 (c) decides regardless of exposure (EXEC §3.6, WD §4.3.8, GUIDE §2.14 HS-4 rows). | Integrator |
| **R8-Q-D6** | D6 returns to the owner: with no host-held route and no host loop, no checkpoint is enforceable from the App on SWBPIPE. Options: (A) accept — checkpointed workflows on X are *unsupported*, runs remain possible with *action during hold* recorded; (B) adopt App interposition (HP-1 / App-assured carriage), reopening R4-2; (C) ask the SWBPIPE owner to plan a host-held route when UI-SUCCESSOR resumes; (D) the "run at the person's discretion" alternative (EXEC F-17). | **(A) now**, optionally **(C)** when UI-SUCCESSOR resumes. The D6 follow-up for App-only checkpoints (EXEC U-E23) folds into the same presentation. | **Owner** |
| **R8-Q2** | R2-13 per-item staleness vs SWBPIPE's whole-model staleness. | Amend R2-13: per-item where the host supplies subject identities; otherwise receive and show the host's staleness scope; de-duplication precedence unchanged (Part 3 item 2). | Integrator (owner notice) |
| **R8-Q3** | Receiving rule for a host with only a whole-model identity. | Receive it as every subject's identity (host's method and scope); over-lapse, never under; resulting objects beyond target ids *not supplied*; never App-computed (Part 3 item 3). | Integrator (owner notice: V4-HI-32 not met by SWBPIPE) |
| **R8-Q-item-1** | Mapping of `unsupported_method` / `unsupported_change`. | *not exposed on this surface*, host-reported; never *not permitted* or a class/grant; record R2-4 not met by the host (Part 3 item 1). | Integrator |
| **R8-Q4** | (i) Status token for AWAITING INPUT cases answered "no/none" (STD-2); (ii) SQ-28 handling: `controller_unavailable` → *endpoint-unavailable*, channel *disabled* ("no host A13 facility"), host reachable without A13 → evidence limit. | (i) Keep the token with the STD-2 annotation (no status machinery change; the answer does not supply the input). (ii) As stated (Part 3 item 4 (a)). | Integrator |
| **R8-Q4b** | Accept a person-set launch environment variable as A13 evidence for development candidates? | **Not now**; revisit when UI-SUCCESSOR resumes. | **Owner** (deferred) |
| **R8-Q5** | May RELAY's relayed body (§0–§3, "App assumes meanwhile") be edited after relay? | **No** (STD-6): edit only header status, UNRESOLVED rows and a change row. | Integrator |
| **R8-Q6** | Standing vocabulary for answered inputs (CA §9 *prepared*, GUIDE *relay pending*, XT *Not received*). | Move each to **answered** (STD-1); add the *answered* standing to GUIDE §0. | Integrator |
| **R8-Q7** | "Embedded Runtime" (SWBPIPE D-58/RUNTIME-ADOPT) vs the App's minimal host loop (V4-ARC-10). | Keep LOOP/PANEL under V4-ARC-10 with a note now; bring the choice to the owner; re-scope DEL-05-01 only if he chooses Runtime adoption (Part 3 item 7). | **Owner** |
| **R8-Q8** | V4-HOST-02 local-only vs SWBPIPE DEC-051 open residency. | Keep V4-HOST-02 meanwhile; present options (b)/(c) to the owner when an embedded host agent is selected (Part 3 item 8). | **Owner** (not urgent) |
| **R8-Q9** | Single seat not a SWBPIPE concept. | Keep SEAT-1…3; note the one-agent-panel counterpart (Part 3 item 9). | Integrator |
| **R8-Q10** | #885 `withdrawn` (person cleared queue) and `rejected: validation_rejected`. | Item-left "cleared by the person without a decision record"; *refused — invalid* at application; never A10/A11 (Part 3 item 10). | Integrator |
| **R8-Q11** | PR #885 readiness / DEP-001 standing. | Annotate PR #885 as deferred; STD-5 (Part 3 item 11). | Integrator |
| **R8-Q12** | A constraint carried as a request field is refused by SWBPIPE's strict preflight (SQ-02 (a), SQ-31); WR-6 / WD I-7 require carrying it. | App guidance never has the agent add fields a host's schema does not define; the expected constraint is recorded App-side (ADAPTER GC-4) with the evidence limit "constraint not carriable on this host"; WR-6 applies where the host defines the element. | Integrator |
| **R8-Q13** | Accept = apply; per-batch Apply; no A10 record (SQ-01, SQ-09). | Keep App meanings; record no SWBPIPE counterpart for accepted-then-stale, per-item A5/A10 and mixed items (Part 4.9). | Integrator |
| **R8-Q14** | OI-003 id collision. | Qualify "App v4 OI-003" where text crosses projects (Part 3 item 12). | Integrator |
| **R8-Q15** | SWBPIPE session undo (no receipt, not through the route, not policy-governed) vs R2-15/R3-4. | Keep R2-15/R3-4 as App meaning; show lapses from identity change; "reverses ⟨receipt⟩" *not supplied* on SWBPIPE (Part 4.9). | Integrator |
| **R8-Q16** | Grant display for a host with no grant model. | "host fixed treatment: every change waits for the person's Apply (host-stated)"; may be deferred with the joins (Part 4.10). | Integrator (deferrable) |

---

## Counts by effect class (Part 1 rows)

| Class | Rows |
|---|---|
| **V** value change | 86 |
| **A** assumption contradicted or qualified | 71 |
| **C** confirms current text | 27 |
| **N** no effect while joins are deferred | 37 |
| **Total** | 221 |

Counting note: one row per dependent group in Part 1 (the 32 SQ tables and
the cross-SQ table; counted by script over the Part 1 table rows). V includes
ledger-standing moves (*prepared / relay pending / Not received* → *answered*)
as well as hold-support, workflow-result and channel-state changes. The
hold-support and workflow-result changes proper are the 18 rows of Part 2.1.
**Five cases change their workflow result** from *not established* to
*unsupported*: L-WDEX-17, L-WDEX-17 with held actions absent, ACT `CP-L4`,
AS F6d and RS E10 (vii). The other SQ-02 changes flip a checkpoint from *not
established* to *not enforceable* inside workflows that were already
*unsupported* (E1, E1d, V-GR1 via X, V-CP1/XF-25, CH-27, FX-50). SQ-28 changes
the channel state's reason (no host A13 facility) and moves every live CA/X
and XC case to STD-2; no workflow result changes from it.
