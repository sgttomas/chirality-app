# A1-C — alignment wave return: WD, WD-EX, EXEC

- Run `APP-V4-DESIGN-PASS-2-20260930`, node A1-C. Type 2 TASK executor (Claude Code subagent of the HELP_HUMAN session). No delegation, no git write, no network.
- Inputs read whole: `BRIEFS.md` (sha256 `698d91d8…469a`: "Common rules", "A1 — alignment wave"); `R9_RESOLUTIONS.md` (sha256 `c3efe2ff…9d2c`); `SURVEY/S1-C.md` (sha256 `5b60dd41…eaa0`); the three Design files; both `ScopeOfWork.md`; both `Dependencies.csv`.
- Files written: the three Design files below and this file. Nothing else. `git status` under `PKG-02…` shows only those three as modified. Scratch copies of the pre-edit bytes and the three edit scripts are in a folder under `$TMPDIR`.
- Method: every edit was an exact-string replacement that had to match once; a script aborted without writing if any did not. 50 replacement operations on WD, 17 on WD-EX, 77 on EXEC.
- Working tree when edited: branch `claude/chirality-app-v4-60-percent-a41fd5`. HEAD was `fbebb12a5` when I started and `be55f3250` when I finished: two commits of run records (`3dd7c22c7`, `be55f3250`) landed meanwhile, and `git show --stat` shows neither touches my three files, R9_RESOLUTIONS.md, BRIEFS.md or S1-C.md. The other Wave A executors were editing their own files at the same time. Siblings are cited by version label and section only.

Words used below: "states" means the file says it; "I read" or "I checked" marks what I observed and how; "inference" marks my reading.

---

## 1. Changes made, per file

### 1.1 `WORKFLOW_DECLARATION.md` — WD-v0.6 → WD-v0.7

- Before: sha256 `43a9962f025de384e1cdaedea9a648da74e20216476a04f2394cfa3851f47eb9`, 1105 lines.
- **After: sha256 `0472a48554615f98b3cdd97a1f6062ebe9a43358f4a5368d981bc45615472f47`**, 1194 lines (`git diff --numstat`: 148 added, 59 removed).
- **24 changes** (rows of the table).

| # | Item (R9 ID; survey item) | Change | Where (line in the new bytes) |
|---|---|---|---|
| 1 | R9-11 (WD 1) | Contribution line: WD-v0.7, superseding WD-v0.6 (last changed at `f5ceef164`, its sha256 recorded); companion label WD-EX-v0.7 | L2, L23 |
| 2 | R9-1, R9-3 (WD 2) | Phase line replaced by the R9-1 summary sentence, with "the current phase (Phase 1)" on first use | L4 |
| 3 | R9-5 (WD 1) | Basis line: the four basis docs at current sha256, naming SCA-V4-001 and SCA-V4-002; current SoW sha256 with the items each amendment revised (cites TBD-004, AX-005, AX-006); intake OWNER_DECISIONS at current sha256; BASIS-ALIGN DECISION-7 (O-25) added | L6 |
| 4 | R9-5 (WD 1) | New first Consumed-inputs bullet for v0.7: R9, BRIEFS, S1-C, R7 and R8 at current sha256, DAG-003, the SWBPIPE answers at `afb6e063…`, sibling labels at their Wave A versions, and the sections read directly at this pass. Older bullets kept unchanged as records | L8 |
| 5 | R9-5 (WD 1; A1-15) | V1-A abbreviation corrected: `01811533…c04c09` → `01811533…cfe04c09` | L18 |
| 6 | (WD 4) | The old "PANEL … (file not read)" bullet gets a closing pointer to the v0.7 bullet; its text is otherwise unchanged | L20 |
| 7 | R9-6 (WD 3) | Receivers line: "Later: DEL-03-04 (W10), DEL-09-06 (W9)" replaced by the list from the ACTIVE register rows, with DEP IDs, including DEL-03-03 and the outside consumers DEL-08-02, DEL-09-02, DEL-10-03 | L21 |
| 8 | R9-11 | New "Changes from v0.6" table, 12 rows keyed by R9 ID and survey item | L27–L48 |
| 9 | R9-1, R9-2, R9-4 (WD 2) | S-F row rewritten: R9-1 summary sentence; "in force in every phase" and "phased to the governance layer"; the R8-11 item 2 reading cited with the owner's confirmation (DECISION-7, O-25) and its R9-2 restatement | L187 |
| 10 | SoW REQ-002, CLM-002 (WD 3) | §4.2.1: supplier of harness-capability meaning is DEL-01-01 (was `UNRESOLVED`); names stay open (U-08) | L273 |
| 11 | R5-1, R8-11 item 3 (WD 8, D-1) | §4.2.4 pass-rule paragraph: one sentence added saying that a required reference *not established* gives the check result *not established*. The existing sentence is kept | L335–L339 |
| 12 | R9-1 (WD 2) | §4.3.0 lead re-pointed to the amended basis, SoW REQ-003 and TBD-004, and DEP-02-01-026; the amended V4-WF-05 and V4-HI-42 quoted in full; "in force / phased" statement added | L357–L388 |
| 13 | R9-1 (WD 2) | CG-4: "V4-WF-05 second half" → "the record clause of V4-WF-05 and V4-HI-42 as amended, in force in every phase" | L406–L410 |
| 14 | R9-1; R9-8 (D-3) | CG-6: "may be recorded" → recorded where the arrival is observed; PH-6 and PH-8 labelled "confirmed INTEGRATION by R8-11 item 1" | L414–L426 |
| 15 | R9-1 (WD 2) | CG-7: the "first half" sentence replaced by "Holding the run … is phased to the governance layer, not withdrawn (V4-WF-05 as amended; U-33 closed)" | L427–L433 |
| 16 | R9-1 (requester) | New paragraph after CG-7, "Who requests, in the current phase", in R9-1's words, labelled INTEGRATION and put to the owner | L435–L451 |
| 17 | R9-1 | Reached-when element and RW-2: "observed and may be recorded" → "recorded where it is observed (R9-1)" | L459, L643–L648 |
| 18 | R9-8 (WD 8, D-3) | I-4 label "PROPOSED (W7)" → "ADOPTED by R4-3"; SB-4 label → "ADOPTED by R4-6" | L518, L680 |
| 19 | R9-2 (WD 2) | I-7 closing sentences, FB-14 and VC-11 restated: request and record clauses of V4-HI-42 in force; "no A5 is forced, and none is recorded" | L584–L590, L1090, L1156 |
| 20 | R9-6; SoW CLM-002 (WD 3) | §8 receiver table: header to WD-v0.7; DEP IDs on existing rows; DEL-03-02 row completed from DEP-03-02-027; new rows for DEL-03-03, DEL-03-04, DEL-09-06 and the outside consumers; DEL-04-01 row annotated (no ACTIVE row names it as a consumer) | L992–L1004 |
| 21 | (WD 4); R9-5 | §8 supplier table: labels at Wave A versions; RS, PANEL, LOOP, P and HOSTING states replaced by section citations from direct reading; DEP IDs; the SWBPIPE answers hash pair | L1008–L1018 |
| 22 | (WD 4); R9-11 | §9 A-1 and A-10 re-pointed to LOOP-v0.7, PANEL-v0.7 and EXEC-v0.5 sections; "Allocation result at v0.7" | L1033, L1042, L1046 |
| 23 | SoW REQ-006, TBD-004 (WD 3) | §10: new DEL-03-03 row (external-channel constraint carriage); DEL-02-03 row now names the current-phase statement and the hold-support values (TBD-004) | L1061–L1062 |
| 24 | R9-8, R9-1, R9-2, R9-4 | §12: U-08 cites the supplier and DEP-02-01-025; U-11 closed (RS); U-17's internal half turned into a confirm-or-object request; U-33 closed; U-34's effect restated by R9-2 with the owner confirmation. §13 VC-19 labels → v0.7 | L1110, L1113, L1119, L1127, L1128, L1164 |

### 1.2 `EXAMPLES.md` — WD-EX-v0.6 → WD-EX-v0.7

- Before: sha256 `8d60ed7850e6935b8410217c8867c59554c7de9aec28c60514e88ff5f0cff36e`, 504 lines.
- **After: sha256 `188fa959c675b8e3ce91ebb68af68fb2535be44c2b4eae8e29ed69671a935e9f`**, 528 lines (40 added, 16 removed).
- **12 changes.**

| # | Item | Change | Where |
|---|---|---|---|
| 1 | R9-11 (WD-EX 1) | Contribution line: WD-EX-v0.7, companion to WD-v0.7, superseding WD-EX-v0.6 (sha256 recorded) | L2 |
| 2 | R9-1, R9-3 (WD-EX 1) | Phase line replaced by the R9-1 summary sentence; the hold-reading sentence kept | L4 |
| 3 | R9-5 (WD-EX 1) | Basis line: four basis docs and the SoW at current sha256 | L6 |
| 4 | R9-5 (WD-EX 1) | New leading v0.7 block in Consumed inputs (one line, as the file has it); older blocks unchanged | L7 |
| 5 | R9-6 | Receivers line follows WD-v0.7 | L8 |
| 6 | R9-11 | New "Changes from v0.6" table, 8 rows | L10–L26 |
| 7 | R9-5 (WD-EX 1) | Fixture reference table lead, V-GR1 source cell and the framing paragraph no longer name C-v0.4 or C-v0.5; they cite C §10 as read at this pass | L94, L110, L115 |
| 8 | R9-11 | E1 "Declaration contract version" label WD-v0.6 → WD-v0.7 (a label, as the v0.6 pass did) | L182–L183 |
| 9 | R9-2 (WD-EX 1) | R-5a and R-5b current-phase readings: act still requested; no A5 forced or recorded by reason of a direct application; V4-HI-42 as amended cited. No disposition changed | L319, L320 |
| 10 | (WD-EX 5; EXEC F-25) | One paragraph after the E7 table: L-WDEX-13b stays the single optional-absent example; L-EXEC-26 is not adopted | L425–L428 |
| 11 | R9-8 (WD-EX 5; V6 m-5) | E8 note: "(an A5 checkpoint takes the derivation, EXEC §3.6)" added, the fix V6 proposed | L475–L480 |
| 12 | R9-11 | UNRESOLVED lead, verification lead and inventory row → WD-v0.7 / WD-EX-v0.7 | L495, L513, L528 |

### 1.3 `EXECUTION_COMPATIBILITY.md` — EXEC-v0.4 → EXEC-v0.5

- Before: sha256 `092f248682447df74e93915527930f4b90367fac46b867dad18daef3c5c608ff`, 1347 lines.
- **After: sha256 `6632a1019625ec64ba0fc6f68d1296e9587fec7df7cbba2d555cd11270543932`**, 1452 lines (171 added, 66 removed).
- **30 changes.**

| # | Item | Change | Where |
|---|---|---|---|
| 1 | R9-11 (EXEC 1) | Contribution line: EXEC-v0.5, superseding EXEC-v0.4 (last changed at `f5ceef164`, its sha256 recorded) | L2 |
| 2 | R9-1, R9-3 (EXEC 2) | Phase line replaced by the R9-1 summary sentence | L5 |
| 3 | R9-5 (EXEC 1) | Basis line: four basis docs at current sha256; current SoW sha256 with the items each amendment revised (cites TBD-006, AX-004, AX-005); SCC-CASE-002 datasheet and intake OWNER_DECISIONS at current sha256; DECISION-7 (O-25) added | L6 |
| 4 | R9-5 (EXEC 1) | New first Consumed-inputs bullet for v0.5; older bullets unchanged | L8 |
| 5 | R9-5 (EXEC 1; C1-13, C1-14) | Two abbreviations corrected: PANEL-v0.4 `cb71bc4b…4c84419` → `…ce84419`; ADAPTER-v0.3 `977d6a26…1f44` → `…46f44` | L33, L35 |
| 6 | R9-6 (EXEC 3) | Receivers line: list from the ACTIVE register rows appended, with DEP IDs, including DEL-03-04, DEL-09-09 and the outside consumers DEL-02-02, DEL-09-02, DEL-10-03 | L36 |
| 7 | R9-11 | New "Changes from v0.4" table, 12 rows | L40–L62 |
| 8 | R9-8 | §0 Labels: PROPOSED (A1) note says both readings were confirmed by R8-11 item 1 | L184–L187 |
| 9 | R9-1, R9-2, R9-4 (EXEC 2) | E-B row rewritten as WD S-F was; citation cell adds SoW REQ-002, AC-002 | L196 |
| 10 | R9-1 (EXEC 2) | §2.1 lead re-pointed to the amended basis and the revised SoW; PH-6 and PH-8 stated as confirmed | L236–L242 |
| 11 | R9-1 | PH-4: "V4-WF-05 second half" → the record clause, in force in every phase; SoW REQ-002 cited | L249 |
| 12 | R9-1; SoW REQ-002 | **PH-6: "may be recorded" → recorded where the arrival is observed; required, not optional.** Wording only. The cell says the observation mechanism is defined in Wave B and states none. The disposition-label reading is marked confirmed INTEGRATION | L251 |
| 13 | R9-1 (EXEC 2) | PH-10 rewritten: both amended texts state the phasing; in force / phased; the awaited basis update is done | L255 |
| 14 | R9-1 | §2.1 closing paragraph: one sentence added ("this recording is required where the arrival is observed"). Then the four texts quoted in full: V4-WF-05, V4-HI-42, SoW REQ-002, SoW AC-002 | L257–L306 |
| 15 | R9-1 (requester) | New paragraph "Who requests, in the current phase", in R9-1's words | L308–L324 |
| 16 | SoW TBD-006 (EXEC 3) | GV-3 cites TBD-006; PH-9 and GV-2 cite WD-v0.7 §4.3.1 | L254, L331, L332 |
| 17 | (EXEC 4; F-27) | CR-12 lists the host-loop residual limit of LOOP §2.4.4 as a limitation | L404 |
| 18 | R9-8 (EXEC 10; V6 m-7) | §3.6: five sentences after the "exhaustive partition" claim state the one case no row values, and that the choice between the HS-5 default and HS-1 is not ruled and not made here | L498–L507 |
| 19 | R9-11 | §3.6 fixture table heading adds "and WD-EX-v0.7" | L523 |
| 20 | R9-6; SoW CLM-002 (EXEC 3) | §4.4 arrival supplier cell names DEL-03-03's observations on the external channel (DEP-02-03-026, ADAPTER §7.7) and says App observation is defined in Wave B | L689 |
| 21 | R9-1 (requester) | §4.6 first row: governance-phase "act request issued; run holds" separated from the current-phase reading (the agent asks; the request is recorded where it can be identified) | L732 |
| 22 | R9-8; R9-1 (EXEC 2) | §4.7: PH-8 label in the phase note; "Why re-hold" now rests on the holding clause as phased and quotes the revised AC-002 | L764, L804–L812 |
| 23 | R9-11 | §7 fixture sources: "carried in C-v0.7 §10", "C-v0.7 §10.4", "WD-EX-v0.7" | L1159, L1165, L1170 |
| 24 | R9-2 (EXEC 2) | CH-27 current-phase entry, closing sentence restated | L1244 |
| 25 | R9-6, R9-5; (EXEC 10, D-2) | §9.1: DEP IDs and arc labels on supplier rows; labels at Wave A versions; WD row "I-1…I-8" → "I-1…I-9" and "WD-v0.6 read whole at this pass"; ADAPTER row states the SoW contribution and what §7.7 does not cover; DEL-01-04 row says the contribution is named by DEP-02-03-027 and not yet defined by the supplier | L1293–L1303 |
| 26 | R9-6 (EXEC 3) | §9.2: DEP IDs; DEL-04-03, DEL-03-03 and the PANEL/AS rows completed from their register statements; new rows for DEL-03-04, DEL-09-09 and the outside consumers; check cells at Wave A labels | L1310–L1318 |
| 27 | SoW REQ-006 (EXEC 3) | §10: new rows "Grant display definition — DEL-04-02" and "Supplier observation — DEL-01-01" | L1331, L1332 |
| 28 | R9-8 (EXEC 4) | §11: F-10, F-11, F-24, F-28, F-29, F-31 closed from records; F-25 and F-27 dispositioned; F-30 cites the owner confirmation and R9-2. F-29's "Proposed change" cell was reworded so that it no longer carries the two dropped phrases; its meaning is kept | L1362, L1363, L1386–L1390, L1396–L1398 |
| 29 | R9-2, R9-4 | UNRESOLVED: U-E24's effect restated by R9-2 with the owner confirmation; U-E1 cites TBD-006; U-E8 cites DEP-02-03-027; a "Changed at v0.5" sentence added | L1406, L1412, L1424, L1427 |
| 30 | SoW (EXEC 2); R9-11 | VC-E-10 range → TBD-001…TBD-006, R9 added; VC-E-11 → EXEC-v0.5; VC-E-13 "recorded where observed (R9-1)" | L1445, L1446, L1448 |

### 1.4 The four phrases: every remaining hit

Checked with `grep -n -i` on the final bytes.

| Phrase | WD | WD-EX | EXEC |
|---|---|---|---|
| "flagged for the next accepted-basis update" | L62 | none | L74 |
| "first half" | L62 | L35 | L74 |
| "second half" | none | none | L74 |
| "override autonomy" | none | none | none |

All five hits are rows of an earlier "Changes from …" table (WD and WD-EX "Changes from v0.5", EXEC "Changes from v0.3"): the R8-1 rows that record what those passes did. R9-5 keeps history lines unrewritten. No hit is in a header, a rule, a case or an open item.

Related wording I also checked: "guidance in Phase 1" said of V4-HI-42 remains only in the same history tables (WD L72, EXEC L87). "PROPOSED (A1)" remains in EXEC where the text says it was the v0.4 label and is now confirmed (L184, L241, L251, L253), in history rows, and in the F-31 finding text, now marked closed.

---

## 2. Survey items not applied, or applied differently

| Survey item | What I did | Reason |
|---|---|---|
| WD 8, D-4 ("on negative decision" phase label) | Not applied. WD L465 and EXEC NG-2 (L835) unchanged | No ruling, SoW text or owner decision says how WD or EXEC should word it. V9 N-1 judged WD's row to be plan content. R10 candidate 1 |
| WD 8, D-6 (A12 and network-destination grants) | Not applied | R8-13 maps the grant to an A12 subclass and does not mention checkpoints. R10 candidate 3 |
| WD 8 / EXEC 10, V6 m-7 | Half applied: EXEC §3.6 now says the partition has one unvalued case. The fix itself (HS-5 default, or invalid) is not chosen. WD unchanged | V6 offers two fixes and R9-8 names none. R9-10 keeps governance-phase definitions as they are. R10 candidate 4 |
| WD 8, D-1 (pass-rule sentence) | Applied in WD only, as an added sentence; EXEC §3.5 unchanged | Deciding texts: R5-1 (a result *not established* is "never a pass, and never unsupported") and R8-11 item 3 (MT-15 and L-WDEX-15 "stay *not established*" on an unresolved required reference). If the integrator reads these as not deciding, the added sentence at WD L335–L339 is the only thing to remove |
| WD 8, D-3 (standing labels) | Applied for I-4 (R4-3), SB-4 (R4-6) and PH-6/PH-8 (R8-11 item 1). I-8, "Run end and continuation" and §6.4 keep "PROPOSED (W7)" | R4-4 and R4-5 rule those PROPOSED; R9-4 says PROPOSED stays PROPOSED |
| EXEC 10, D-2 (I-1…I-7 / I-8 / I-9) | §9.1 corrected to I-1…I-9. The "consumed unchanged" list at EXEC L211 still reads I-1…I-7 | WD has I-1…I-9 (I checked by grep). I-8 and I-9 state EXEC's own SP-6 and hold-claim rule (R4-5, R4-2), so "consumed unchanged: I-1…I-7" is not wrong. Noted as R10 candidate 5 (minor) |
| WD 4 (read five siblings directly) | Done for RS, PANEL, LOOP, P, HOSTING at the sections cited. The earlier state records ("header checked", hashes at `d3cebd1cc`) are kept in the cells, followed by the direct reading | The file's convention keeps earlier readings. ACT and C are not in the survey's list of five; their §8 rows got the label and DEP ID only. C §10 was read for WD-EX |
| WD-EX 1 ("re-point the fixture table to C §10 after reading it") | Applied. I checked by script that every identifier in the fixture table occurs in C §10 of the working tree (then already labelled C-v0.7) and which subsection holds it | I did not compare each identifier's content with WD-EX's gloss line by line |
| WD-EX 5 / EXEC 4 (F-25) | Dispositioned as "keep L-WDEX-13b alone; L-EXEC-26 stays EXEC's" | The other option adds a fixture case, which is new content. The integrator may reverse it: WD-EX L425–L428 and EXEC F-25 |
| A.2 lag 4, C.2 lag 6 (terminology "Phase 1" against "current phase") | "The current phase (Phase 1)" on first use in each header; new text says "current phase". Existing "Phase 1" left | R9-3 allows either form where it already stands |
| WD L144 "Not repaired here (routed to closeout C1): RF-3, RF-7, X-16" | Left | It closes the "Changes from v0.2" section (history). U-08 now cites DEP-02-01-025 for RF-7 |
| EXEC §8 register rows still reading "Carried to C1" | Left | The column is "Standing at v0.2" (history). §11 carries the closures |
| Survey NOW items U-32 / U-E7, U-08 / U-E10 naming | Not closed | WD 10 and WD 6 are Wave B |
| Survey C.3 inference (a sentence on network-destination dependence of a required tool in host loops) | Not added | Not in the A1-C list; new content |

One survey statement I could not confirm as written: S1-C §A.6 gives arc label "N-20" for DEP-02-01-027. `DAG-003/HANDOFF_STATE.md` did not show that label in the lines I searched, so the Design files cite that row by DEP ID only. The labels I did confirm there and used: N-16, N-18, N-21, N-23, N-24, X-1.

---

## 3. R10 candidates (R9-9)

Line numbers are in the new bytes of WD/EXEC and in the working-tree bytes of the sibling (labelled v0.7 when I read it).

**1. "On negative decision", element absent: phase label (D-4).**
- WD §4.3.1, L465: "Absent this element, the run stops at the checkpoint. It never proceeds as if the act were positive."
- EXEC §4.8 NG-2, L835–L839: "*stop* → a run-ended event with cause 'stopped by declared negative path' … Absent path → stop." EXEC §2.1's closing paragraph keeps "negative decisions and paths as recorded (§4.8)" for Phase 1.
- LOOP §2.4 element table, L528: "Absent: in Phase 1 the agent follows the plan it worked out with the person (LP-8); in the governance phase (governed checkpoints) the run stops at the checkpoint."
- Options: (a) label WD and EXEC by phase as LOOP does; (b) keep WD as plan content (V9 N-1's judgment) and label only EXEC NG-2, since EXEC is the execution side; (c) leave both, and have EXEC's Wave B current-phase table say that a path is what the agent follows and what is recorded.

**2. Reached-when kind (b) on a message-form output (D-5).**
- WD §4.4, L811: output form includes "a report or message to the person". WD defines no element that designates a message as a declared output. RW-1: arrival is "never inferred from model text".
- LOOP §2.4.1, L603: kind (b) counts "a completed agent message the declaration designates as that output".
- Options: (a) WD adds the designating element (survey WD 7, Wave B) and EXEC's App-side table uses it; (b) LOOP narrows kind (b) to host-outcome-produced outputs until WD defines the element; (c) state that a message-form output cannot be the subject of kind (b).

**3. May a declared A12 checkpoint require a network-destination grant? (D-6)**
- WD §4.3.1 validity row "grant setting", L480, and §4.3.6: the setting content is "classes, grant values, scope". EXEC §4.10 (L876 onward) says the same.
- ACT §2.7 (L491 onward; R8-13): A12 subclass "network-destination grant"; its setting content is "the category or named destination and the scope". ND-A1 (L518): "An operation-class A12 grants no destination."
- Options: (a) say in WD and EXEC that a checkpoint's "grant setting" is an operation-class grant only; (b) extend the subject class to the network-destination subclass with its own setting content; (c) leave it with the host joins, since DECISION-5 governs host agents only.

**4. A declared, malformed held-actions element on an A5 or kind (a) checkpoint (V6 m-7).**
- EXEC §3.6, L498–L507 (partition sentence and the note added at v0.5) and HS-5; WD §4.3.1 "held actions", L468: "consumers assume at least one App-side step (EXEC HS-5) only when a kind (b)/(c) checkpoint has no held-actions element, or when its declared held actions do not show host operations only".
- R7-3's own sentence can be read two ways: "its" may mean the kind (b)/(c) checkpoint, or any checkpoint. V6 read it the first way.
- Options: (a) the HS-5 default applies to any **declared** element that does not show host operations only (the coverage R6-1 had before R7-3); (b) such an element is invalid, HS-1, which needs a new failure row in WD §11. Governance phase only under either.

**5. EXEC §1's "consumed unchanged" list (D-2, minor).**
- EXEC L211: "independence rules I-1…I-7 (WD §4.3.3)". WD has I-1…I-9; §9.1 now says I-1…I-9.
- Options: (a) leave, because I-8 and I-9 originate in EXEC; (b) write "I-1…I-9", which would have EXEC "consume unchanged" two rules it supplies.

**Not an R10 candidate, but a wording point in R9 itself.** R9-2 says the checkpoint's disposition "stays *act not performed*". That is not one of the six shared dispositions (WD §4.3.4). I did not introduce it as a disposition word: the files say "no A5 is forced, and none is recorded by reason of a direct application", and the record label stays *waiting* ("reached; act not yet recorded").

---

## 4. Proposed ScopeOfWork, register or basis items for a later amendment

1. **DEL-02-03 SoW, REQ-007 and VER-006** still say "TBD-001 through TBD-005". The SoW has TBD-006. EXEC VC-E-10 now compares against TBD-001…TBD-006.
2. **DEL-01-04 SoW** does not name an App act control or a person identity (`grep -rniE "act control|person identity"` over its folder returned nothing). DEP-02-03-027 (X-1) and DEL-02-03 SoW CLM-002 name that contribution.
3. **DEL-02-03 register**: no row for consuming DEL-04-02's grant display states, although SoW CLM-002 and REQ-006 name DEL-04-02 for them and EXEC §4.10 uses them. The join rests on the supplier's row DEP-04-02-023 only (arc N-07).
4. **DEL-04-01 as a consumer of WD**: WD §8 has a DEL-04-01 receiver row (the mirrored closed list and referents), and no ACTIVE register row says DEL-04-01 consumes DEL-02-01. Either add the row to DEL-04-01's register or drop the WD row.
5. **DEP-03-03-014 (DEL-03-03's register)** places the required-tool check under "for the governance phase". EXEC's required-tool check is in force in both phases (PH-3; SoW REQ-001). The row's statement should separate them. EXEC §9.2 now lists the check outside the governance-phase clause.
6. **Harness capability: who names.** DEL-02-01 SoW REQ-002 says the meaning is "supplied through DEL-01-01". HOSTING §8 says the inventory "is the input to harness-capability naming owned by DEL-02-01". No SoW says which deliverable produces the names. WD §4.2.1 now states both facts and keeps the names `UNRESOLVED` (U-08).
7. **Basis docs**: nothing proposed.

---

## 5. Wave B items beyond the survey's

1. **The request as a recorded thing.** R9-1 has the product record "the request where it can be identified". EXEC §4.4's event table has no request event, and neither file says what identifies an agent's request in an App run (an A8 request? a CAP-6 question?). EXEC's Wave B recorder needs the event, its evidence and its absent case.
2. **"Recorded where the arrival is observed" needs the observed/not-observed boundary per reached-when kind.** WD CG-6, the reached-when element and RW-2, and EXEC PH-6 now depend on it. It belongs with survey item EXEC 6.
3. **No label for "reached, no request identified".** WD §4.3.4 defines *waiting* as "Reached; the act is requested". In the current phase the request is the agent's and may not be identifiable. The record-label meaning ("reached; act not yet recorded") covers it, but the first clause of the disposition row does not.
4. **Contributions named by registers and not defined (R9-6):**
   - harness capability names and their meaning as portable requirements — DEP-02-01-025 (also survey WD 6);
   - "scoped feature evidence" — DEP-09-02-015 (WD) and DEP-09-02-017 (EXEC); "evidence" — DEP-08-02-006 (WD). No case has been run, and no file says what that evidence will be;
   - the App act control and person identity — DEP-02-03-027; the supplier has no Design file.
5. **WD §4.3.7's item-leaving causes lag P §4.3.** WD L711 lists "stale refusal, A11 withdrawal, host refusal". P lists five causes, including "refused — not permitted (re-resolution at application)" and "cleared by the person with no decision record".
6. **WD §8's ACT and C rows** still rest on header checks and earlier readings; a direct reading of ACT-v0.7 §2.1, §2.7, §4.1, §4.2 and of C-v0.7 §3–§5 is outstanding.
7. **EXEC §4.6 now carries two readings in its first row** (governance phase and current phase). That is a stop-gap. The current-phase transition table of survey item EXEC 5 should replace it.

---

## 6. Header pin tables as they now stand

"Recomputed" means `shasum -a 256` on the working-tree file during this node. I also ran a script over each edited file: every 64-hex value present in the new bytes and absent from the old bytes equals the recomputed hash of the file named beside it.

### 6.1 WD-v0.7

| Pin | Value | How checked |
|---|---|---|
| PRD.md | `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` | Recomputed |
| ARCHITECTURE.md | `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c` | Recomputed |
| HOST_INTEGRATION.md | `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` | Recomputed |
| EXAMINATION.md | `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` | Recomputed |
| Amendments named | SCA-V4-001, SCA-V4-002, with their snapshot folders | Folders listed; each doc's status paragraph names SCA-V4-001 (grep) |
| DEL-02-01 ScopeOfWork.md | `ef360edf28f5f463ae961495e04e566ab9ec9d56c0a4fd4f35e67b87adb82f17` | Recomputed; revised items read from AX-005 and AX-006 |
| V4-WF-05, V4-HI-42 quotations (§4.3.0) | full amended texts | Script: each source bullet, whitespace-normalised, is a substring of the file, inside quotation marks |
| First-run OWNER_DECISIONS.md | `a9869129…ad2c` (unchanged line) | Recomputed: current |
| Intake OWNER_DECISIONS.md | `5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2` | Recomputed |
| BASIS-ALIGN OWNER_DECISIONS.md (DECISION-7) | `ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b` | Recomputed; "Effects" lists "the R8-11 reading"; OWNER_ITEMS O-25 read |
| R9_RESOLUTIONS.md | `c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c` | Recomputed |
| BRIEFS.md (this run) | `698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a` | Recomputed |
| SURVEY/S1-C.md | `5b60dd41a8c269902a9b360bf4cdc7c8106c464564bcc2fc1623948661c7eaa0` | Recomputed |
| R8_RESOLUTIONS.md | `44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b` | Recomputed |
| R7_RESOLUTIONS.md | `1f6ab3b2355e164f803657ceae08841af92d21a821feede3800a6df861b2a1ea` | Recomputed |
| R1–R6 (unchanged lines) | `2f9c7e72…`, `77cfb845…`, `202d52c7…`, `50a009b2…`, `254d0b93…`, `8703e85a…` | Recomputed: all current |
| `_DAG/_LATEST.md` | → DAG-003 | Read: "Latest: DAG-003", accepted 2026-09-29 |
| RELAY_ANSWERS_SWBPIPE.md | `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74` | Recomputed. `git diff c322826ea a999f4ba1`: 3 lines changed; the blob at `c322826ea` hashes to `6f01add3…61c7` |
| Predecessor WD-v0.6 | `43a9962f…7eb9`, last changed at `f5ceef164` | Hash of the pre-edit copy; `git log` on the file |
| V1-A abbreviation | `01811533…cfe04c09` | Recomputed `comparisons/V1-A.md` |
| Siblings | labels only: EXEC-v0.5, C-v0.7, P-v0.7, ADAPTER-v0.5, GUIDE-v0.4, ACT-POLICY-v0.7, AS-v0.7, RS-v0.7, LOOP-v0.7, PANEL-v0.7, HOSTING-BOUNDARY-v0.7, PIN-SPIKE-v0.1, CA-v0.5, XT-v0.5, RELAY-v0.3 | R9-11 table. No sibling byte is pinned |
| Older Consumed-inputs bullets | unchanged | History (R9-5) |

### 6.2 WD-EX-v0.7

| Pin | Value | How checked |
|---|---|---|
| Four basis docs | as 6.1 | Recomputed |
| DEL-02-01 ScopeOfWork.md | `ef360edf…2f17` | Recomputed |
| R9, BRIEFS, S1-C, R7, R8 | as 6.1 | Recomputed |
| Intake and BASIS-ALIGN OWNER_DECISIONS | `5fd780bf…0b2`, `ca8c4e50…254b` | Recomputed |
| RELAY_ANSWERS_SWBPIPE.md | `afb6e063…0e74` | Recomputed |
| Predecessor WD-EX-v0.6 | `8d60ed78…f36e`, last changed at `f5ceef164` | Hash of the pre-edit copy; `git log` |
| C §10 (fixture) | label C-v0.7, §10.1–§10.4; no byte pin | Script: every fixture identifier of the table is present in C §10 |
| Siblings | labels only, as 6.1, with WD-v0.7 | R9-11 |
| Root sources for E5, E6 ("repo 6e18505e3") | unchanged lines | Survey B1-11 found no diff since `6e18505e3`; I did not re-run that diff |

### 6.3 EXEC-v0.5

| Pin | Value | How checked |
|---|---|---|
| Four basis docs | as 6.1 | Recomputed |
| DEL-02-03 ScopeOfWork.md | `0006521b9bd96ea7ec98ecc5d9e6db794ecb331440c276006b444e7ee319726d` | Recomputed; revised items read from AX-004 and AX-005 |
| V4-WF-05, V4-HI-42, SoW REQ-002, SoW AC-002 quotations (§2.1) | full current texts | Script: exact substring match against each source |
| AC-002 fragment in §4.7 | "for a workflow that takes up the governance phase, the checkpoint also keeps the run waiting until that evidence" | Script: substring of the SoW |
| SCC-CASE-002 Case_Datasheet.md | `a12abfaf82c34ae1e7c10d8b553d3e1a0da4772b160e02257c0bf70edce04d5c` | Recomputed. `git diff 6e18505e3 HEAD` on the file: 54 insertions, no line removed |
| First-run OWNER_DECISIONS.md | `a9869129…8ad2c` (unchanged lines) | Recomputed: current |
| Intake and BASIS-ALIGN OWNER_DECISIONS | `5fd780bf…0b2`, `ca8c4e50…254b` | Recomputed |
| R9, BRIEFS, S1-C, R7, R8 | as 6.1 | Recomputed |
| R1–R6, INTAKE_MAP (unchanged lines) | as the file has them | Recomputed: all current |
| `_DAG/_LATEST.md` | → DAG-003 | Read |
| RELAY_ANSWERS_SWBPIPE.md | `afb6e063…0e74` | Recomputed |
| Predecessor EXEC-v0.4 | `092f2486…08ff`, last changed at `f5ceef164` | Hash of the pre-edit copy; `git log` |
| PANEL-v0.4 abbreviation | `cb71bc4b…ce84419` | `git show cc58211c5:` and `8fb51f07f:` of the file, hashed |
| ADAPTER-v0.3 abbreviation | `977d6a26…46f44` | `git show 375c3970c:` and `2f42fba02:` of the file, hashed |
| Generated schema `34f28a48…f458` (unchanged line) | — | Not rechecked by me; survey C1-12 found it current |
| Siblings | labels only: WD-v0.7, WD-EX-v0.7, and the rest as 6.1 | R9-11 |
| Older Consumed-inputs bullets | unchanged except the two abbreviations | History (R9-5) |

### 6.4 Register and sibling facts the new text relies on

| Statement in the files | How checked |
|---|---|
| Receiver rows and DEP IDs | A script listed every non-anchor ACTIVE row of both registers, and every row of any other deliverable's register that targets DEL-02-01 or DEL-02-03 |
| DEP-02-03-015 and -016 RETIRED | Same listing |
| Arc labels N-16, N-18, N-21, N-23, N-24, X-1 | `DAG-003/HANDOFF_STATE.md` |
| RS carries U-11's items and the turn initiator (F-24) | Read RS §4 rows R2, R5a, R8, R11, §6.1, §10 |
| LOOP §2.4.4 states the residual limit "not a separate value" (F-27) | Read the §2.4.4 table heading |
| ADAPTER §7.7 covers the A5 kind (c) case and a general current-phase rule | Read §7.7 |
| PANEL §3.2, §3.5, §6; LOOP §2.4–§2.4.2, §6.2, §10; P §3.1, §3.3, §4.3, §9, §13; HOSTING §8, §8.2 | Read those sections |
| Owner confirmation of the R8-11 item 2 reading | OWNER_ITEMS O-25 ("Confirm the reading") and DECISION-7's "Effects" list |
| R4-3 and R4-6 adopt; R4-4 and R4-5 stay PROPOSED; R8-11 item 1 confirms PH-6 and PH-8 | Read R4 and R8 |

### 6.5 Limits

- I read the sibling sections in the working tree while other Wave A executors were editing. C, LOOP and ACT were already labelled v0.7 when I last looked; I do not know whether RS, PANEL, P, HOSTING and ADAPTER had been edited when I read them. Section numbers cited were present in the bytes I read.
- I did not read ACT, AS, C (outside §10), CA, XT or GUIDE whole.
- No Markdown renderer was run. A script compared the pipe counts of every table row with its header, before and after: the only mismatches are one pre-existing row in WD (L86, an R6-3 history row) and one in WD-EX, both unchanged.
- Nothing here is a fixture result, a host witness or an owner act. All three files stay DRAFT.
