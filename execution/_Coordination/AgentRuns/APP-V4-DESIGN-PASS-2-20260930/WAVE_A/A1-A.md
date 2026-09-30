# A1-A — alignment wave return: ACT, AS, RS

- Run `APP-V4-DESIGN-PASS-2-20260930`, node **A1-A**. Executor: Type 2 TASK
  (Claude Code subagent; no delegation). No git write, no network.
- Files edited (the write fence): the three Design files below, and this
  return file. No ScopeOfWork, register, `_STATUS.md`, basis, decomposition,
  scope-change or DAG file was touched.
- Started on commit `3dd7c22c73`. The integrator committed `be55f32502`
  during the work (owner decision package); it does not touch these files.
- Inputs read whole: `BRIEFS.md` ("Common rules", "A1"), `R9_RESOLUTIONS.md`,
  `SURVEY/S1-A.md`, the three Design files, the three `ScopeOfWork.md`, the
  three `Dependencies.csv`. Read in part, for the item checked: the four basis
  docs, every other deliverable's `Dependencies.csv` (rows targeting
  DEL-04-01/02/03), DAG-003 `DependencyEdges.csv`, `CandidateEdges.csv` and
  `HANDOFF_STATE.md`, R8 (R8-11…R8-13), R4-11, the BASIS-ALIGN and SCA002
  `OWNER_DECISIONS.md` and `OWNER_ITEMS.md` (O-4, O-10, O-11, O-14, O-15,
  O-17, O-25, O-29; Q-5, Q-11), ARC_ANALYSIS §3, V6 (m-3…m-7), and the
  committed sibling texts for the citations I rely on (GUIDE, CA, XT, PANEL,
  LOOP, ADAPTER, WD, EXEC).
- Method of edit: exact-string replacements, each asserted to match once,
  run first on a scratch copy and then on the file. Text outside the
  replaced strings is byte-identical to v0.6.

| Short | File | Version | sha256 after the edit | sha256 before | Edits | Lines +/− |
|---|---|---|---|---|---:|---|
| ACT | DEL-04-01 `Design/ACT_AND_POLICY_CONTRACT.md` | ACT-POLICY-v0.6 → v0.7 | `1186ed4276ab037c00b1fb5955b2983ac2b55ceedf11e6be32c10d365b3ebd6b` | `6889003e…4815` | 52 | +190 / −84 |
| AS | DEL-04-02 `Design/AUTONOMY_AND_STANDING_EXCHANGE.md` | AS-v0.6 → v0.7 | `8ddf0150a171789e6a6b6676ff8cfbf7b72d90452d9876eaa876195dff83ddb5` | `52d1341b…a33d` | 26 | +73 / −24 |
| RS | DEL-04-03 `Design/RECORD_SEMANTICS.md` | RS-v0.6 → v0.7 | `339cccdf8bcb1c14bdb67c6103b547aef2fd91a9d00b8de769fd9a337f7e41c6` | `96b1aeeb…f666` | 25 | +95 / −25 |

All three stay DRAFT. "Edits" counts exact-string replacements.

---

## 1. Changes made

Line numbers are lines of the files as they now stand.

### 1.1 ACT (items ACT 1–6)

| Item | Change | Where |
|---|---|---|
| ACT 1 · R9-11 | Version v0.7; v0.6 recorded as predecessor with its sha256 | l.2 |
| ACT 1 · R9-5 | Basis re-pinned: four basis docs by sha256 (SCA-V4-001, SCA-V4-002 named); ScopeOfWork `ac043e54…`; PRD §2.2 V4-HOST-02, ARCHITECTURE §4 and V4-EXM-23 added to the cited sections; intake `OWNER_DECISIONS.md` at its current hash with DECISION-5; BASIS-ALIGN and SCA002 owner records; `_DAG/_LATEST.md` → DAG-003 | l.7–19 |
| ACT 1 · R9-5 | New "Consumed inputs for v0.7" block: R9, this BRIEFS, the survey, R1–R8 by file with R8 at its current sha256, ANS at `afb6e063…`, siblings by Wave A label only. The older consumed-input lines are left as history and said to be so | l.20–25 |
| ACT 1 · R9-6 | Receivers line rebuilt: eleven local DOWNSTREAM rows; nine consumers with their own row only; the retired DEP-05-02-014/-015 dropped; DEL-01-01's use has no row | l.69–77 |
| R9-11 | New "Changes from v0.6" table (11 rows) | l.96–114 |
| R9-4, R9-3 | Label table: SETTLED covers the amended basis and owner-confirmed readings; Phase 1 = "the current phase" | l.243, l.249 |
| ACT 2 · R9-1, R9-3 | Header Phase line: halves and the basis-update marker removed; the two R9-1 lists used verbatim | l.4 |
| R9-4 | Header and §2.7 Standing: the person-only grant cited to PRD V4-HOST-02 and ARCHITECTURE §4; the A12 mapping stays INTEGRATION | l.5, l.497–499 |
| ACT 1 · TBD-004 | Serves line cites ScopeOfWork TBD-004 | l.6 |
| R9-5 | Sibling labels in the body: LOOP-v0.7, EXEC-v0.5, WD-v0.7, C-v0.7 | l.504, 617, 625–626, 663, 1249, 1263, 1597, 1605 |
| ACT 1 (A-P1) | §3 "checked against … 6e18505e3" now says S9 is re-quoted from the amended basis | l.539–541 |
| ACT 2 · R9-1 | S9 quotes V4-HI-42 as amended; consequence column uses the R9-1 lists and R9-2 | l.553 |
| ACT 4 · R9-2, R9-4 | §3 D2 reading: relabelled SETTLED (O-25, DECISION-7), restated per R9-2 | l.577–588 |
| ACT 2 · R9-1, R9-4 | §4.0 lead: phasing cited to the amended texts and TBD-004; both amended texts quoted in full; the two R9-1 lists | l.622–650 |
| ACT 2 | AP-3 quotes V4-WF-05 in place of "second half" | l.656 |
| ACT 2 · R9-2 | AP-8 restated (renamed "Checkpoint clause of D2") | l.661 |
| ACT 2 · R9-1 | AP-11 restated without halves or marker | l.664 |
| ACT 3 · R9-1 | New **AP-12 Who requests** (INTEGRATION; points to EXEC, Wave B; no mechanism) | l.665 |
| R9-2 | §4.4 Phase-1 paragraph: "no A5 is forced, and none is recorded"; the act is still requested | l.818–826 |
| ACT 2 · R9-1, R9-2 | §5.3 rule 2, Phase-1 bullet | l.1084–1091 |
| ACT 2 · R9-2 | §5.6 W-b basis | l.1184 |
| R9-11 | §8.1 policy revision identity → ACT-POLICY-v0.7 | l.1292 |
| ACT 4 | §8.2 "Not established": the `Open_Issues.csv` pointer replaced by the owner's decision | l.1322 |
| ACT 2 · R9-2 | P-01 and P-05 phase sentences | l.1335–1337, l.1398–1402 |
| ACT 2 | V-09 basis and value text | l.1456 |
| ACT 4 · R9-4 | V-10: model-destination reading SETTLED (O-10; DEL-04-03 REQ-002) | l.1457 |
| ACT 5 | New **V-28** row for §2.7; note that DEL-03-04 and DEL-09-06 are mapped in §10.3 | l.1464–1468 |
| ACT 5 · R9-6 | §10.3 rebuilt as "Receivers by register row": 20 consumers, both rows, what is mapped | l.1480–1516 |
| ACT 4 · R9-8 | F-1 and F-8 rewritten; F-10, F-18, F-19, F-20 closed by record; F-16 cites amended V4-EXM-22 | l.1698–1718 |
| R9-8 | "Closed" list gains a v0.7 line | l.1743 |
| ACT 6 | VC-001 and VC-010 cite TBD-004; VC-006 in two parts; VC-007 traces V-28; VC-009 → FX-01…55, "No results at v0.7"; VC-010 → AP-1…AP-12; VC-011 traces to V4-EXM-23 | l.1765–1775 |

### 1.2 AS (items AS 1, 2, 6 and the Receivers part of 5)

| Item | Change | Where |
|---|---|---|
| AS 1 · R9-11 | Version v0.7; v0.6 recorded as predecessor | l.2 |
| AS 2 · R9-1, R9-3 | Header Phase line; TBD-006 cited | l.4 |
| AS 2 · R9-4 | Header: V4-HOST-02 cited from the amended PRD | l.5 |
| AS 1 · R9-5 | Basis re-pinned (four docs; ScopeOfWork `f16ffa8a…`, SCA-V4-001 and SCA-V4-002); DECISION-4, DECISION-5 and the owner confirmations named; DAG pointer; PRD §2.2 V4-HOST-02 and §4.1 V4-WF-05 added to the cited sections | l.7 |
| AS 1 · R9-5 | New "Consumed inputs for v0.7" line | l.8 |
| AS 1 · R9-6 | Receivers line rebuilt; "pending at C1" removed | l.13 |
| R9-11 | New "Changes from v0.6" table (7 rows) | l.15–30 |
| R9-5 | Sibling labels: C-v0.7, EXEC-v0.5, WD-v0.7, RS-v0.7 | l.96, 118–119, 260, 271, 401, 548 |
| AS 2 · R9-1 | S3 quotes V4-HI-42 as amended, with the R9-1 lists | l.104 |
| R9-2, R9-4 | S13: R8-11 item 2 restated; owner confirmation cited | l.114 |
| AS 2 · R9-4 | S15: PRD V4-HOST-02 quoted with its "(D-18; DEC-5)" suffix; marker removed; destination reading SETTLED (O-10) | l.116 |
| AS 6 | §1 Phase-1 paragraph cites TBD-006 | l.118 |
| R9-2 | §2 constraint bullet | l.176–183 |
| R9-1 | OV-1: who requests; no display of the request defined (points to EXEC, Wave B) | l.265 |
| AS 2 · R9-1, R9-2 | OV-4 | l.268 |
| AS 6 | §10 D6 row: stale ScopeOfWork parenthetical removed; TBD-006 cited | l.540 |
| AS 2 · R9-4 | F19: "(INTEGRATION, DECISION-2 reading)" → SETTLED (O-10) | l.586 |
| AS 5 (Receivers part) · R9-6 | New **§12 Receivers**: nine named receivers, local row, own row, DAG-003 layer, contribution named, where defined. One register-named contribution marked "not yet defined here" | l.589–613 |
| AS 1 | U-15 closed; U-16 point of need follows TBD-006; "Closed in v0.7" | l.631, 632, 639 |

§6 was changed in its lead sentence only ("RS-v0.7"). Its body is still
byte-identical to RS §8: 2744 characters each, compared by script from
"**Settings-in" to the end of the section, after the edit.

### 1.3 RS (items RS 1–4)

| Item | Change | Where |
|---|---|---|
| RS 1 · R9-11 | Version v0.7; v0.6 recorded as predecessor | l.2 |
| RS 2 · R9-1, R9-3 | Header Phase line | l.4 |
| RS 2 · R9-4 | Header: "new element R15" → "element R15"; V4-HOST-02 from the amended PRD; R15 within the inventory | l.5 |
| RS 1 · R9-5 | Basis re-pinned (four docs; ScopeOfWork `ceecddbb…`, SCA-V4-001); DECISION-4, DECISION-5, DECISION-6 (N-12, N-15), DECISION-7 (O-10, O-14, O-25); DAG pointer | l.7 |
| RS 1 · R9-5 | New "Consumed inputs for v0.7" line (adds ARC_ANALYSIS §3.3) | l.8 |
| RS 1 · R9-6 | Receivers line rebuilt; "By join (not registered)" removed | l.13 |
| R9-11 | New "Changes from v0.6" table (8 rows) | l.15–31 |
| R9-5 | Sibling labels: C-v0.7, EXEC-v0.5, WD-v0.7, AS-v0.7 | l.106, 130, 215, 416, 549 |
| R9-2, R9-4 | D14 restated | l.125 |
| RS 2 · R9-4 | D16: PRD V4-HOST-02 quoted with its suffix; marker removed; destination reading SETTLED (REQ-002; O-10) | l.127 |
| RS 2 · R9-1 | §1 Phase-1 paragraph: V4-HI-42 quoted in place of "second half"; who requests and what is recorded; no record element for the request defined (points to EXEC, Wave B) | l.129–143 |
| RS 2 · R9-4 | §4 lead: R15 and the R5 destination are within the inventory | l.199–202 |
| RS 2 · R9-4 | R5: "INTEGRATION, DECISION-2 reading" → REQ-002 and O-10 | l.211 |
| RS 2 · R9-4 | R15: "addition" removed; cited to REQ-002, CLM-002, V4-HI-70, V4-HOST-02 | l.222 |
| RS 3 | §10 DEL-03-02 cell restated (N-12 not proposed) | l.477 |
| RS 3 | §10 DEL-03-03 cell marked the same way (N-B8); the two ADAPTER limits noted as not yet defined here | l.478 |
| RS 3 | §10 DEL-05-02 cell widened (R15; R11 "process network not observed") | l.481 |
| RS 3 | §10 DEL-09-06 cell widened (R2, R7, R8, R10, §6, §4) | l.483 |
| RS 3 · R9-6 | §10 new DEL-09-09 row | l.484 |
| RS 1 · R9-6 | New **§10.1** receivers (15 rows) and suppliers (10 rows) by register row | l.490–529 |
| RS 4 | §11 stale ScopeOfWork sentence removed | l.536–537 |
| RS 2 | VC-02 → R1–R15 | l.742 |

Checked, no edit: R11 already lists "host reachable without evidenced A13"
and "constraint not carriable on this host" (R9-8, R8-12 item 5). R3, R5,
R13 and the §10 DEL-01-01 row already take supplier facts from DEL-01-01
directly (R9-7).

### 1.4 The required greps, after the edit

`flagged for the next accepted-basis update`, `first half`, `second half`,
`override autonomy`:

| File | Line | Hit | Account |
|---|---|---|---|
| ACT | 127 | "V4-WF-05's first half …", "… next accepted-basis update" | Row of "Changes from v0.5" (history; R9-5: not rewritten) |
| AS | 42 | "V4-WF-05's first half phased" | Row of "Changes from v0.5" (history) |
| AS | 53 | "flagged for the next accepted-basis update" | R8-13 row of "Changes from v0.5" (history) |
| RS | 55 | "flagged for the next accepted-basis update" | R8-13 row of "Changes from v0.5" (history) |

No other hit. "override autonomy": none in any file. Related wording left on
purpose:

- ACT l.29, l.48, l.136, l.149; AS l.50, l.66; RS l.51, l.67: consumed-input
  and change-table history ("checkpoint half", "INTEGRATION (DECISION-2
  reading)", "guidance in Phase 1").
- ACT §4.6 last bullet ("In the governance phase a governed checkpoint also
  overrides any grant (S9)") and VC-001 ("… override the grant"): governance-
  phase statements, retained under R9-10. See §5 item 2.

---

## 2. Survey items not applied, or applied differently

| Survey item | What I did | Reason |
|---|---|---|
| ACT 1 "current sibling bytes (or GUIDE's table only)" | Siblings cited by Wave A label only | R9-5 |
| ACT 2, locations l.100, l.122 (v0.6 numbering) and header l.38 | Not edited | History lines (R9-5). The header history line on D5/D6 (now l.48) still says "INTEGRATION (DECISION-2 reading)" and "D6 is deferred to SWBPIPE SQ-02" as facts of the v0.4 inputs |
| ACT 3 "Settle, with DEL-02-03's file" | Stated the R9-1 ruling as AP-12 and pointed to EXEC | EXEC is not my file; the mechanism is Wave B (R9-1) |
| ACT 5 "map DEL-03-04, add DEL-09-06" | Mapped in the §10.3 table and named under §10.1; the individual §10.1 consumer cells were not extended | Precise edit; GUIDE cites §2–§9 as a whole. Extending each cell is Wave B detail |
| AS 5 | Receivers table only | As briefed |
| RS 1 "rebuild Receivers from rows 014 and 021–032" | Receivers from the DOWNSTREAM rows 011–016 and 029–032 and the consumers' registers; rows 021–028 tabled as suppliers | Rows 021–028 are UPSTREAM (supplier) rows. I disagree with the survey's wording here |
| RS 3 "settle with ADAPTER the two R11 limits" | Not settled. RS §10 now says the two limits are not yet defined here | No ruling, ScopeOfWork or owner text decides (R4-11 lists RS elements and names neither). R9-9; see R10-1 |
| Survey §1.4 F-6 (NOW; "keep as a note") | Not edited | Nothing to change |
| Survey §1.4 F-18 (NOW, partly left to S1-D) | Closed | I checked all four consumers in the committed texts: WD §4.3.1, EXEC §4.10, LOOP §2.4 (l.616), PANEL §3.5 (l.343–346) |
| Survey §1.7 V10 N-1 (hash sentence readable as "at `1528a5033`") | History sentence not edited | It is a consumed-input history line. The new v0.7 block pins the current intake `OWNER_DECISIONS.md` unambiguously |
| Survey §1.7 V10 N-5 | Not edited | V10 asked for no change |
| Survey §2.4 / §3.4 "carried to C1" in AS U-19 and RS U-07 | Not edited | Owner-class items, not classed NOW |
| Survey §2.3, §3.3: AS F21/VC-18 and RS E13/VC-30 do not trace to V4-EXM-23 | Not edited | Not in the AS or RS item lists for Wave A. Returned in §5 |

Everything else in section 8 of the survey (ACT 7–8; AS 3, 4, 7, 8 and the
rest of 5; RS 5–8) is Wave B and was not started.

---

## 3. R10 candidates (R9-9)

**R10-1 — two evidence limits between ADAPTER and RS.**
- ADAPTER §11, row "Provide to DEL-04-03": "evidence limits for R11 (cited
  basis not observed; omitted constraint; origin mismatch; agent-written
  configuration; unverified identity; native hint mismatch; resubmission
  without prior observation; App-restart interruption; …)".
- RS §4 R11: the list of evidence limits contains neither "resubmission
  without prior observation" nor "App-restart interruption" (it has "Lost
  acknowledgement" and "cited basis not observed").
- Options: (a) RS R11 adopts the two labels; (b) ADAPTER maps the two onto
  existing R11 limits and the *outcome unknown* overlay, and drops the
  labels; (c) leave both until the RS writer and failure sequences are
  written (Wave B, RS 7), then decide with them.
- Both texts left. RS §10 (DEL-03-03 row) states the gap.

**R10-2 — R9-2's "act not performed" against the closed disposition list.**
- R9-2: "If the workflow declares a checkpoint there, its act is still
  requested, no act is recorded by reason of the direct application, and the
  checkpoint's disposition stays *act not performed* unless the person
  performs it."
- ACT §4.3 (shared with WD §4.3.4): "**waiting · performed · resolved
  negatively · lapsed · not reached · unknown**". ACT §4.2: an A5 checkpoint
  must use reached-when kind (c) *proposal queued*; "If the run ends without
  observing it, the disposition is **not reached**." LOOP FX-C9 (committed
  text): "If the host applies directly, no proposal is queued, so the A5
  checkpoint (kind (c) *queued*) is not reached".
- Options: (a) "act not performed" is a description, the disposition is *not
  reached*, and "still requested" means the agent's plan, not an observed
  arrival; (b) the arrival is taken as observed at the direct application
  and the label is *waiting*; (c) a seventh label is added (WD owns the
  vocabulary).
- In ACT I applied R9-2 without the disposition word (§4.4, P-05: "no A5 is
  forced, and none is recorded"; "its act is still requested").

No other disagreement between two files was found in these three that lacks
a deciding text. Two near cases are returned elsewhere: the owner of the
contacted-destination display (the DEL-04-02 ScopeOfWork decides that AS
consumes it; §5 item 5), and the A12 mapping (owner item F-22; §4 item 1).

---

## 4. Proposed ScopeOfWork, register or basis items (none made)

1. **DEL-04-01 ScopeOfWork, AC-007 and AX-005.** AC-007 says OUT-002
   supplies no reserved list "beyond the adopted
   `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` rulings". ACT §2.7 and the
   new V-28 carry DECISION-5's person-only destination grant as an A12
   subclass. The person-only grant is now in the accepted basis; the A12
   mapping is INTEGRATION (F-22; OWNER_ITEMS O-15 deferred it). If the owner
   confirms the mapping, AC-007 and AX-005 need a DECISION-5 sentence.
2. **DEL-04-01 register.** Nine consumers declare DEL-04-01 upstream with no
   local DOWNSTREAM mirror: DEL-09-06 (DEP-09-06-030), DEL-01-02, DEL-01-04,
   DEL-02-02, DEL-06-02, DEL-09-02, DEL-09-05, DEL-09-12, DEL-10-03. Decide
   whether the supplier register mirrors them (ACT F-1).
3. **DEL-04-01 / DEL-01-01 registers.** DEL-01-01's use of the D3 value
   (ACT V-21, V-25) has no row in either register.
4. **Mirror maturity.** DEP-03-03-008 is RequiredMaturity TBD against
   DEP-04-01-023 INITIALIZED; DEP-09-06-015 is TBD against DEP-04-03-031
   INITIALIZED (both are HANDOFF open matters).
5. **DEL-04-02 ScopeOfWork CLM-002.** It names five receivers. Three more
   deliverables declare DEL-04-02 upstream: DEL-03-04 (DEP-03-04-012),
   DEL-09-06 (DEP-09-06-031), DEL-09-09 (DEP-09-09-022). The register has no
   local mirror for them. Conversely DEL-03-02, DEL-03-03 and DEL-02-03 have
   no UPSTREAM row for DEL-04-02 in their own registers; those three arcs
   rest on DEP-04-02-021…023 alone (V12 F6).
6. **DEL-04-03 ScopeOfWork REQ-005.** Its consumer list does not name
   DEL-03-04, DEL-09-02, DEL-09-05, DEL-10-03, DEL-01-04 or DEL-02-02, whose
   registers declare DEL-04-03 upstream (DEP-03-04-013, DEP-09-02-019,
   DEP-09-05-010, DEP-10-03-014, DEP-01-04-012, DEP-02-02-017).
7. **DEL-04-03 `_DEPENDENCIES.md`, Run Notes (l.78).** It calls the DEL-09-06
   row DEP-04-03-031 "N-08". In ARC_ANALYSIS, N-08 is DEL-09-06 → DEL-04-02;
   the DEL-04-03 arc is DEP-09-06-015. A label slip.
8. **Basis or ScopeOfWork, if the owner confirms R9-1's reading.** V4-WF-05,
   V4-HI-42 and V4-EXM-22 say the act "is requested" and do not say by whom.
   AP-12 (ACT), OV-1 (AS) and §1 (RS) carry the reading as INTEGRATION. A
   confirmed reading would want one sentence in DEL-02-03's ScopeOfWork or
   in the basis.

---

## 5. Wave B items found beyond the survey's section 8

1. **The request has no home in these three files.** AP-12 says the product
   records "the request where it can be identified". ACT has no rule for an
   observed arrival with no identified request; AS defines no display of a
   checkpoint-act request; RS has no record element for it. All three point
   to EXEC. (The survey has the RS half as RS 5.)
2. **Governance-phase wording against the amended V4-HI-42.** ACT §4.6 last
   bullet ("a governed checkpoint also overrides any grant (S9)"), VC-001
   ("override the grant"), the §4.4 heading and P-05 ("DERIVED from V4-HI-42
   + D2b") read the pre-amendment sentence. They are governance-phase
   definitions, kept under R9-10. When the governance phase is written, the
   derivation should be restated from the amended text.
3. **ACT §10.1 cells and §11.** DEL-03-04 and DEL-09-06 are mapped in §10.3
   only; §11's "Supply V-…" cells do not list V-28.
4. **AS: "the grant in force carried on each loop dispatch".**
   DEP-05-01-025 names it; AS §12 marks it "not yet defined here".
5. **AS: the contacted-destination record.** DEL-04-02 ScopeOfWork CLM-002
   and DEP-04-02-018 have AS consume it; LOOP assigns "AS §3 (display)"; AS
   defines no display; PANEL ND-4 shows one. The ScopeOfWork decides that AS
   consumes it, so this is a missing definition, not an R10 item. (Survey AS
   3; restated because AS §12 now says so in the file.)
6. **V4-EXM-23 traces.** AS F21/VC-18 and RS E13/VC-30 cover V4-EXM-23's
   behaviour and do not cite it. ACT VC-011 now does.
7. **RS §10 rows missing for registered consumers.** DEL-03-04, DEL-09-02,
   DEL-09-05 and DEL-10-03 have no §10 row; §10.1 says so.
8. **Cross-executor checks for the integrator.**
   - CA (A1-E): the working text I saw while checking citations carries a
     finding that RS §10 names only "R2 transfer links" for DEL-09-06.
     RS-v0.7 §10 now names R2, R7, R8, R10, §6 and §4. I did not rely on
     CA's Wave A text; the RS cell is built from CA's committed §2.3.
   - XT (A1-E): XT IN-29 (committed text) says the AS consumption is "not
     registered in DEL-09-09 Dependencies.csv"; DEP-09-09-022 exists.
   - WD/EXEC (A1-C): if V6 m-7 is applied (a declared held-actions element
     that fits no HS row becomes HS-5 or HS-1), ACT §4.6's HS list must echo
     the choice. Not edited here.
   - LOOP/PANEL (A1-D): the R9-2 label question (R10-2) arises in FX-C9 and
     PC-24.
9. **Pre-existing table defects (history, not touched).** The "Changes from
   v0.5" tables have two-cell rows in a three-column table: ACT l.139–140,
   AS l.54–55, RS l.54, l.56–57.
10. **"Carried to C1".** AS U-19 and RS U-07 still give "carried to C1" as
    routing; C1 is closed. The items themselves are the owner's (multi-row
    A4 after partial lapse).

---

## 6. Header pins as they now stand

Checked on the working tree after the edit. "Recomputed" means
`shasum -a 256` (and a second pass in Python `hashlib`) equals the value in
the header.

### 6.1 Pins common to the three headers

| Pin | Value in the header | How checked |
|---|---|---|
| `docs/PRD.md` | `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` | Recomputed |
| `docs/ARCHITECTURE.md` | `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c` | Recomputed |
| `docs/HOST_INTEGRATION.md` | `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` | Recomputed |
| `docs/EXAMINATION.md` | `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` | Recomputed |
| Amendments named | SCA-V4-001 (`_ScopeChange/SCA-V4-001_2026-09-28_2155/`), SCA-V4-002 (`_ScopeChange/SCA-V4-002_2026-09-29_1901/`) | Folders exist; `_ScopeChange/_LATEST.md` names SCA-V4-002 with SCA-V4-001 as predecessor |
| "Others unchanged since `6e18505e3`" | statement | `git diff -U0 6e18505e3 HEAD -- docs/`: hunks touch only V4-WF-05, V4-HOST-01/02, V4-HI-42, V4-HI-70, V4-EXM-22/23, V4-ARC-11/12 with the §4 properties, PRD §1.1/§2.2 intro/OQ-03, HOST_INTEGRATION §8.1 and status notes |
| Intake `OWNER_DECISIONS.md` (DECISION-3/-4/-5) | `5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2` | Recomputed |
| BASIS-ALIGN `OWNER_DECISIONS.md` (DECISION-6, -7) | `ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b` | Recomputed; DECISION-7's list of accepted items read |
| BASIS-ALIGN `AMENDMENT_PACKET/OWNER_ITEMS.md` | `2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef` | Recomputed; equals the `2b90eb4a…` that DECISION-7 records; O-10, O-11, O-14, O-15, O-17, O-25 read |
| `_DAG/_LATEST.md` → DAG-003 | `4d381ba4e87b41a83b9d0d2dc591c4bf04eacb84df0b5c27314091cd2a992f56` | Recomputed; first line reads "Latest: DAG-003" |
| `R9_RESOLUTIONS.md` | `c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c` | Recomputed (also after `be55f32502`) |
| This run's `BRIEFS.md` | `698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a` | Recomputed |
| `SURVEY/S1-A.md` | `87baa03d7cbc9b0a6b8e8543d8cd80a7d71c754da80fbfdc053c8e6ef21045f6` | Recomputed |
| R1–R7 | by file name only | Files exist in `APP-V4-FIRST-INCREMENT-20260928/` |
| `R8_RESOLUTIONS.md` | `44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b` | Recomputed |
| `RELAY_ANSWERS_SWBPIPE.md` | `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74` | Recomputed. `git diff 94aa9181b HEAD` on the file: three lines differ (SQ-04 integrity-standing list; SQ-09 evaluated basis; P7 T9 check). None is cited by ACT, AS or RS. The file was not edited |
| Siblings | Wave A labels of R9-11 (EXEC-v0.5, WD-v0.7, WD-EX-v0.7, C-v0.7, P-v0.7, ADAPTER-v0.5, GUIDE-v0.4, LOOP-v0.7, PANEL-v0.7, HOSTING-BOUNDARY-v0.7, PIN-SPIKE-v0.1, CA-v0.5, XT-v0.5, RELAY-v0.3, and the two of ACT-POLICY-v0.7 / AS-v0.7 / RS-v0.7 that are not the file itself) | Labels copied from the R9-11 table. No byte pin. Section anchors cited in the body were checked in the committed (pre-Wave-A) sibling texts only |
| Older consumed-input lines | unchanged | History. Each header now says they are records of earlier passes, not current pins |

### 6.2 Pins particular to one header

| File | Pin | Value | How checked |
|---|---|---|---|
| ACT | Predecessor v0.6 | `6889003e6c1c2dd6d58b7145dd7955651debcc7b705a84e63aa6cd4e596e4815`, last changed `caa4334ca1`, unchanged at `3dd7c22c73` | sha256 of the file before the edit; `git log` on the path; the tree was clean at start |
| ACT | ScopeOfWork | `ac043e54e396f9155e3d1b02d61ca7333350a812c7db3d5bb26c80d6fc3bb875` (SCA-V4-001; unchanged by SCA-V4-002) | Recomputed; AX-005 names SCA-V4-001 only |
| ACT | SCA002 `OWNER_DECISIONS.md` | `36ffcbbea923504581844456751c2eb3db617b5471a3595e63f036bf0634b480` | Recomputed; DECISION-2 read (Q-5 option A) |
| ACT | SCA002 `AMENDMENT_PACKET/OWNER_ITEMS.md` | `1d46458c966b6cc41be361eb2ddbc75df409bcc43202aff17478b81438ca51a8` | Recomputed; equals the `1d46458c…` that DECISION-2 records |
| ACT | `DECISION_BRIEF.html#d3` | `02d38cb1…20e8` (unchanged line) | Recomputed; current |
| AS | Predecessor v0.6 | `52d1341bb475f0a7de4b986b905e2986aa0e0a4e04e8b1783a6a83174eb6a33d` | As ACT |
| AS | ScopeOfWork | `f16ffa8a33cbfb2e78a8e916e90aff9fb44ad20adf94fe61a559a213f5564460` (SCA-V4-001 and SCA-V4-002) | Recomputed; AX-004 and AX-005 read |
| AS | §6 ≡ RS §8 | statement | Script comparison of the two bodies after the edit: equal, 2744 characters |
| RS | Predecessor v0.6 | `96b1aeeb120be597c4f35eea13f6a60ce20783e555c918521aacee38c5bcf666` | As ACT |
| RS | ScopeOfWork | `ceecddbb67a86f744b413bb08b08c27017a82ebee8500f7600faf8d880fbaa47` (SCA-V4-001) | Recomputed; AX-004 read |
| RS | ARC_ANALYSIS §3.3 | by path and section | Read; no hash pinned |

The R1–R5, V2, V3-A, V3-B, IR1-A, `INTAKE_MAP.md` and first-run
`OWNER_DECISIONS.md` hashes in the older Basis text of AS and RS, and in
ACT's history lines, were left as they were. I recomputed them: each equals
the current file.

### 6.3 Quoted requirement and register texts

Each was compared with its source by a whitespace-normalised containment
check (Python), after the edit:

- V4-WF-05 (PRD l.254–264): ACT §4.0 — match.
- V4-HI-42 (HOST_INTEGRATION l.139–144): ACT S9 and §4.0, AS S3 — match.
- V4-HOST-02 (PRD l.120–126, with "(D-18; DEC-5)"): AS S15, RS D16 — match.
- "the run does not record the act as done until the person performs it"
  (PRD): ACT AP-3, AS OV-4 — match.
- "recorded as done only when the person performs it" (HOST_INTEGRATION):
  RS §1 — match.
- ARCHITECTURE §4: "the agent may ask for a destination during its work, and
  only the person grants it": ACT §2.7 — match.
- V4-EXM-22 and V4-EXM-23 phrases: ACT F-16, VC-011 — match.
- DEL-04-03 ScopeOfWork REQ-002 "model used with its observed destination
  per turn": ACT V-10, RS D16 and R5 — match.
- DEL-04-01 ScopeOfWork TBD-004 "autonomy never records or substitutes that
  act": the phrase is in the ScopeOfWork; ACT W-b and VC-006 paraphrase it
  ("never records or substitutes") and cite TBD-004.
- Register statements quoted in AS §12 (DEP-05-01-025, DEP-05-02-019,
  DEP-03-04-012, DEP-09-06-031, DEP-09-09-022) — match.
- ADAPTER §11 labels quoted in RS §10 — match.
