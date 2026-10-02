# F-E1 — first-increment edits: ADAPTER, XT, LOOP, PANEL (design pass 3)

- Run `APP-V4-DESIGN-PASS-3-20261001`, node **F-E1**. Executor: Type 2 TASK
  (Claude Opus 5.5), dispatched by the HELP_HUMAN session; does not delegate.
  Written 2026-10-02 at HEAD `83a3989850`.
- Brief: `BRIEFS.md` (sha256 `d6ce0247…77eb`) "Common rules", "F —
  first-increment edits", "RX … and F-E1" (the F-E1 paragraph). Binding read:
  R17…R20, `OWNER_DECISIONS.md` (`ea96c557…e015`; DECISION-K3 revised,
  DECISION-L), DECISION-3 (host joins deferred), V4-ARC-10 / R12-11 (LOOP
  keeps Chat Completions).
- **Boundary kept.** Files written: the four Design files below and this
  return file. No schema, example, prototype, ScopeOfWork, register,
  `_STATUS.md`, `OBS_*`, `PIN_SPIKE_*`, `generated/` or SWBPIPE file was
  edited. RX's files (WR, ROLE, NIR, HOSTING, EXEC, CA) were read only; they
  changed in the working tree during this node (RX in parallel), so they are
  cited by label and section only. Read-only git; no network; no Codex or
  model run. Prototype runs wrote only to my scratch folder
  (`…/scratchpad/fe1/`); `git status --untracked-files=all` showed no new
  file after the runs.
- Each target was read whole before editing (ADAPTER 1,783 lines, XT 948,
  LOOP 2,733, PANEL 1,235 at their v0.6/v0.6/v0.8/v0.8 bytes, which equal
  the hashes F0 records: `7cad04c8…`, `daf6c9c9…`, `f8b7776c…`, `70d9a23e…`).

## 1. Rows applied

| Row | File → version | What changed (sections) | Cited basis |
|---|---|---|---|
| **FD-01** (D1 J-AD-1; F0 §1.9; F0 §1.14 L101, L1238) | ADAPTER-v0.6 → **v0.7** | **PI-6**: custody no longer "DEL-01-02's (later undertaking, D1)". RECOVERY-v0.2 §8.2 `observation_lost` (`inFlightItems`: thread, turn, item) and `app_restart_interruption` are mapped (PROPOSED): native status *interrupted*; a submission or observation *outcome unknown*, observer App, last observed *submitted*, "lost acknowledgement" (OM-6), plus "App-restart interruption" after a relaunch (OM-9); a read is read again (RD-4); Codex's recovered status shown beside the record, never in its place. OBS-2 O-2/O-3: an item absent from history is read **not recovered**, never *completed*; no inference that a command did not run; a `cancel` answer is OM-7 (item `declined`). Losses are per App-owned home's process (L-1; C-12 Stop/Restart Codex). Also: §1 owner/act row (L101); CT-9, CT-10; S-7 step 1; OC-3 owner cell (L1238; ACCESS-v0.2 I-2 and §3: the App homes link the person's `config.toml`); XF-41 state "defined"; UNRESOLVED row closed as defined; §11 "Expect from DEL-01-02/RECOVERY-v0.2" (by join; NR-02 proposed); Receivers line; header inputs; "Changes from v0.6" | RECOVERY-v0.2 §2 (DEF-3, DEF-5, DEF-6, DEF-7), §3.4, §5 SQ-R, SQ-X, §8.2; custody-event schema; HOSTING-v0.9 §4, §10.2 OB2-2, OB2-3; NIR-v0.2 §4, §5.2; ACCESS-v0.2 §1 I-2, §3; R17-10; R18-1 C-12; R18-7 G-4; DECISION-L L-1 |
| **FT-01** (D1 J-XT-1; F0 §1.10) | XT-v0.6 → **v0.7** | XC-06 State cell: "App-restart custody DEL-01-02 (later, D1)" → RECOVERY-v0.2 §5 SQ-R and §8.2, mapped for XF-41 by ADAPTER-v0.7 PI-6; optional row NR-03 (= D1 NR-D1-3) noted for SCA-V4-003. §3.6 row 8 (XC-06) pointer likewise, with "SH-1 simulates no restart". Header inputs; "Changes from v0.6". No case state value, expected result or completion rule changed (XC-06 stays AWAITING INPUT) | RECOVERY-v0.2 §5 SQ-R, §8.2; ADAPTER-v0.7 PI-6 |
| **FL-01** (D4 #17; F0 §1.11) | LOOP-v0.8 → **v0.9** | §10.3 "Local-server capability requirements": "Not supplied … later undertaking (D1)" → **supplied (PROPOSED)** at ACCESS-v0.2 §11 CH-1…CH-8 (I-8; schema and fixture), read as information with no requirement taken; bearing of each item stated (CH-4 to be checked on Chat Completions; CH-6/CH-7 agree with NW-3, NW-6, §12). The consumer row stays a register proposal (F0 §3 M-5 = pass-2 R-0501-4 = D4 NR-3); G-10 notes it | ACCESS-v0.2 §1 I-8, §11; F0 §3 M-5 |
| **CH-8** (D4 §R2.3 on FL-01; R19-4; ASSESSMENT_SIWC.md rec. 6) | LOOP-v0.9 | Host plan billing recorded as a **next-relay item, not a requirement**: the "Sign in with ChatGPT" plan grant is Responses-only, so a host could use it only through a Responses interface behind §4's one boundary (R12-11). Note under §4's boundary paragraph; new **NR-L1** in §13 (prepared, not relayed); header model-interface line. V4-ARC-10 stands; nothing selected; host joins deferred | ACCESS-v0.2 §11 CH-8, §20; ASSESSMENT_SIWC.md; R12-11; DECISION-3 |
| **FL-02** (D4 #18; F0 §1.11; OBS-2 O-4) | LOOP-v0.9 | §1 App "Model interface": "**unobserved** on an identified candidate" → observed at one pair, not qualified (OBS-1 OB-8; HOSTING-v0.9 §8.1 L-2; ACCESS CH-1), Chat Completions refused for Codex providers (`strings-in-binary`); LM Studio drops `namespace` tools, so neither MCP tools (OB-1) nor delegation tools (OBS-2 O-4 on the stock pairing; HOSTING-v0.9 §10.2 OB2-4; ACCESS CH-2) reach the model; "not a Chat Completions finding". VC-03's "(Responses API unobserved)" follows | HOSTING-v0.9 §8.1, §10.1, §10.2; ACCESS-v0.2 §11 |
| **FP-01** (D5 note; F0 §1.13, §1.14 L842, L881) | PANEL-v0.8 → **v0.9** (optional step taken) | §5 A15 row capture cell: "The App's registration control (DEL-02-02, later undertaking)" → DEL-01-04's App act control (AAC-v0.2 §4.2) presenting DEL-02-02's A15 descriptor (WR-v0.2 §4.3 RB-4; several entries per act, §4.7) per K-8, L-4, ACT-POLICY-v0.9 §2.6. §6 row: "App workflow experience (DEL-02-02, later undertaking per D1)" → WR-v0.2 §4.4, §4.6 and NIR-v0.2 §5.7. Pointer refresh only. **Why taken:** both pointers had become untrue (ACT-POLICY-v0.9 already re-points A15's capturing surface, F-C FA-02), so leaving PANEL would have left a contradiction for F-E2 | AAC-v0.2 §4.2; WR-v0.2 §4.3, §4.4, §4.6, §4.7; NIR-v0.2 §5.7; ACT-POLICY-v0.9 §2.6 |

Each file has a "Changes from ‹previous›" table keyed by these row IDs
(ADAPTER "Changes from v0.6" before UNRESOLVED; XT, LOOP and PANEL newest
first, as each file orders them).

**Round-2 items (D1…D6 §R2.3) aimed at these four files** — checked by
reading each section and by `grep` of the D files for ADAPTER, XT, LOOP,
PANEL, DEL-03-03, DEL-09-09, DEL-05-01, DEL-05-02 and CH-8:

| D file | Item for ADAPTER/XT/LOOP/PANEL | Disposition |
|---|---|---|
| D1 §R2.3 | None new; it states "Items not listed are unchanged", so J-AD-1 and J-XT-1 stand as FD-01/FT-01 | Applied as FD-01, FT-01 |
| D2 | Its join items are §R2.4 (§R2.3 is the prototype rerun); none names these files | — |
| D3 §R2.3 | None | — |
| D4 §R2.3 | "FL-01 (LOOP §10.3): the handoff now has CH-8"; FL-02 "unchanged from round 1" | Applied (FL-01, CH-8, FL-02) |
| D5 §R2.3 | None (its §2 note on PANEL §6 is FP-01) | Applied as FP-01 |
| D6 §R2.3 | None | — |

## 2. Not applied, with reason

| Item | Reason |
|---|---|
| A prototype change for PI-6 (for example a self-check mapping RECOVERY's `observation_lost` valid example into dispatch records) | No row requires it; FD-01 adds no schema element (the external dispatch record already has native status *interrupted* and the limits used). Offered for a later node; not done |
| ADAPTER Verification cases' list of contract versions "current at this revision" (C-v0.8, P-v0.8, EXEC-v0.6, WD-v0.8) | Not an FD-01 locus; stale labels, not "later" pointers. Left for F-E2's citation check; noted in ADAPTER's change table |
| XT §2 IN-04…IN-08 Standing labels (Wave A labels, e.g. ADAPTER-v0.5) | XT §2 states those cells keep their Wave A labels by design; no row asks to change them |
| Adding NR-L1 to the RELAY file's "next relay" row (DEL-09-06) | Outside this fence (RELAY is DEL-09-06's; not RX's either). LOOP §13 records the item and says the list is DEL-09-06's. **Returned to the integrator** |
| Register rows NR-02 (DEL-03-03 → DEL-01-02), NR-03 (DEL-09-09 → DEL-01-02, optional), M-5 (DEL-05-01 → DEL-01-05 mirror) | Registers are not written by executors; each file names the proposal for SCA-V4-003 |
| ADAPTER L1589 (R4-20 history row, "DEL-01-02, later") | Change history; kept, as F0 §1.14 says |

## 3. New sha256 (after the last edit)

| File | Version | sha256 |
|---|---|---|
| `PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/ADAPTER_ENABLEMENT_AND_RECEIVING.md` | ADAPTER-v0.7 (1,857 lines) | `9b9a4319d2db1156cb28a837591740fbf2fcf4253fb377f779383cfb50163f0d` |
| `PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Design/EXTERNAL_TRACE_CASES.md` | XT-v0.7 (963 lines) | `d973677bab5abdc03b170e10c0ad52a1135cc8dd5ad24afc7886271c97e7f456` |
| `PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/LOOP_RECEIVING_CONTRACT.md` | LOOP-v0.9 (2,787 lines) | `d47d2249eb5f863aea640f582893b6861fc5a019d600412de7f3ac2e58cc429a` |
| `PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Design/PANEL_RECEIVING_CONTRACT.md` | PANEL-v0.9 (1,252 lines) | `4898b6f80832b3baae9fd7e2e24e2fe6141a0d2b12359f1c0dce5647ccee6999` |
| `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/F-E1.md` (this file) | — | reported in the hand-back |

Previous: ADAPTER-v0.6 `7cad04c8…acca0c` and XT-v0.6 `daf6c9c9…cb5777`
(last changed at `fffae12915`); LOOP-v0.8 `f8b7776c…250e61` and PANEL-v0.8
`70d9a23e…eaf3cd` (last changed at `b6db949c84`).

## 4. Prototype reruns (2026-10-02, 19:34–19:36 UTC; Python 3.13.7, macOS; `-B`, outputs to scratch)

No prototype file was changed, so each run checks that the unchanged
prototypes still pass against the current sibling files (RS-v0.9's schema
after F-C included).

| Deliverable | Command (cwd) | Result |
|---|---|---|
| ADAPTER (SH-1 driver first) | `python3 -B run_fixture.py --out ‹scratch›/sh1-run` (DEL-03-01 `Design/prototype/`) | exit 0; "22 of 22 checks passed; items recorded: 34; host documents: 30" |
| ADAPTER | `python3 -B observe_map.py --run ‹scratch›/sh1-run` (DEL-03-03 `Design/prototype/`) | exit 0; 15 PASS, 0 FAIL: the nine named mappings (T10 *queued*, T13 *outcome_unknown*, T13o *recorded_state*, PM-3 *refused_identity_conflict*, XF-34 *tool_execution_declined*, OM-CLI-2 *error*, XF-06 *endpoint_unavailable*, CH-0 *channel_not_enabled*, V-R1 *not_permitted*); OM-1 OBS-1b item, compound and `userShell` checks; CO-10/CO-11 shapes; "34 dispatch records -> 43 of 43 RS entries … valid against RS_RECORD.schema.json"; "every schema value -- 21 outcomes, 8 request kinds, 18 evidence limits -> 48 of 48 RS entries valid"; "Records: 34 dispatch, 11 checkpoint observations, 14 channel statuses"; "RESULT: all checks passed" |
| XT | `python3 -B prototype/run_xt_suite.py --out ‹scratch›/xt` (DEL-09-09 `Design/`) | exit 0; 59 PASS, 0 FAIL; cases in the §3.5 order with the same outcomes as XT §3.6 (e.g. XC-06 *inconclusive* 3/2/0; XC-07, XC-08, XC-05 L-XT-2 *passed*; XC-04 and TR-02…TR-10 *not run*); 24 records valid; evidence limits are RS R11 labels; work account 39 rows; both valid examples equal the regenerated instances (date aside); invalid examples rejected (3 and 4 errors); "ALL CHECKS HOLD: 0 failure(s)". No `--write-examples` was needed |
| LOOP | `python3 -B assemble_tool_calls.py` (DEL-05-01 `Design/prototype/`) | exit 0; "22/22 cases as expected; every record checked against LOOP_TOOL_CALL.schema.json" |
| LOOP | `python3 -B schema_subset.py ../LOOP_TOOL_CALL.schema.json ../LOOP_TOOL_CALL.example.valid.json ../LOOP_TOOL_CALL.example.invalid.json` | VALID / INVALID ("oneOf matched 0 branches"); exit 1 by design (README) |
| LOOP | `python3 -B destination_flow.py` | exit 0; 17 PASS, 0 FAIL (MS-14…MS-27 with sub-cases; examples); "RS entries validated: 68; loop request records validated: 11"; "RESULT: all expectations held" |
| LOOP | `python3 -B schema_subset.py ../LOOP_DESTINATION_REQUEST.schema.json …valid.json …invalid.json` | VALID / INVALID (oneOf, anyOf); exit 1 by design |
| PANEL | `python3 -B panel_double.py` (DEL-05-02 `Design/prototype/`) | exit 0; "4/4 scripts as expected" (PC-38…PC-41) |
| PANEL | `python3 -B schema_subset.py ../PANEL_RETURN_INPUT.schema.json …valid.json …invalid.json` | VALID / INVALID; exit 1 by design |

## 5. How checked

- Every replaced passage was matched exactly once before replacement (a
  script asserting `count == 1`), so no unintended locus changed;
  `git diff --stat` per file: ADAPTER +87/−13, XT +18/−3, LOOP +59/−5,
  PANEL +20/−3.
- Every section newly cited was confirmed to exist by `grep` of headings
  in the current files at about 19:30 UTC: RECOVERY-v0.2 §2, §3.2, §3.4,
  §5 SQ-R/SQ-X, §8.2; ACCESS-v0.2 §1, §3, §11, §20; HOSTING-v0.9 §4, §8.1,
  §10.1, §10.2; NIR-v0.2 §4, §5.2, §5.7; WR-v0.2 §4.3, §4.4, §4.6, §4.7;
  AAC-v0.2 §4.2; ACT-POLICY-v0.9 §2.1, §2.6. Line numbers in HOSTING and
  NIR moved during the node (RX editing); section numbers did not.
- Facts carried from other files were read in their source, not from F0:
  the custody-event schema's `observation_lost.inFlightItems` and
  `app_restart_interruption` required fields; ACCESS CH-1…CH-8 and the
  handoff fixture; HOSTING §10.1 OB-8 and §10.2 OB2-2…OB2-4; AAC §4.2 steps
  1–8; ACT-POLICY-v0.9's FA-02 (A15 capturing surface already re-pointed).
- What is inference here is labelled in the files: the PI-6 mapping and the
  "not recovered" reading are PROPOSED; LOOP's reading of CH-1…CH-8 takes
  no requirement; NR-L1 asks for no decision.

## 6. For the integrator and F-E2

1. **RELAY next-relay row** (DEL-09-06): add LOOP-v0.9 §13 NR-L1 (host plan
   billing needs a Responses interface; CH-8). Not in any current fence.
2. **GUIDE re-pin (F-E2):** new labels ADAPTER-v0.7, XT-v0.7, LOOP-v0.9,
   PANEL-v0.9 with the hashes in §3. Citations added in this node that
   F-E2's check should cover are listed in §5.
3. **SCA-V4-003 rows** named in the files: NR-02 (DEL-03-03 → DEL-01-02),
   NR-03 (DEL-09-09 → DEL-01-02, optional), M-5 (DEL-05-01 → DEL-01-05
   mirror); all admitted layer, no SCC change (F0 §3).
4. **Stale but unrowed:** ADAPTER's Verification-cases list of "current"
   contract versions (C-v0.8, P-v0.8, EXEC-v0.6, WD-v0.8) now lags EXEC-v0.7
   and WD-v0.9.
