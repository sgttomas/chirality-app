# A1-D — alignment wave return: LOOP, PANEL, HOSTING

- Run / node: `APP-V4-DESIGN-PASS-2-20260930`, node **A1-D** (Wave A). Type 2 TASK executor (Claude Code subagent; parent HELP_HUMAN). No delegation. Read-only git, no network.
- Date: 2026-09-30. Worktree HEAD at the edit: `3dd7c22c73`.
- Files written: the three Design files below and this return file. Nothing else. `PIN_SPIKE_0.158.0.md` is unchanged (sha256 `0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115`, recomputed after the edits).
- Inputs read whole: BRIEFS.md ("Common rules", "A1"), R9_RESOLUTIONS.md, SURVEY/S1-D.md, the three Design files, the three `ScopeOfWork.md`. Read in part: the three `Dependencies.csv` and every other register row naming these deliverables (by script); `_DAG/DAG-003/DependencyEdges.csv`, `CandidateEdges.csv`, `HANDOFF_STATE.md`; the amended requirement texts in the four basis docs; R8-11…R8-13; SCA-V4-001 `OWNER_ITEMS.md` (O-10, O-25, O-29 and the item table); the two amendment runs' OWNER_DECISIONS; DEL-04-03's and DEL-02-01's ScopeOfWork (the passages cited); RS R3/R5/R13 rows; EXEC §2.3 HP-2.
- Method. Edits were made by exact-string replacement, each required to match exactly once. After editing: every quoted requirement text was compared with its current source (32 quotes, whitespace-normalized, all found in both the file and the source); every full sha256 in the new header text was recomputed with `shasum -a 256` and matched; table rows were checked for cell count against the pre-edit files (no new inconsistent row).

## 1. Changes made, per file

### 1.1 LOOP_RECEIVING_CONTRACT.md — LOOP-v0.6 → LOOP-v0.7

New sha256: `0c201a6133fb2ea758d5d2f65e6049c2f337390b998d492ed9028df3cd400b57` (was `246f4636…5767`). 66 diff hunks; 237 lines added, 119 removed.

| Item | Change | Where (v0.7 line) |
|---|---|---|
| R9-11 | Version label; "supersedes" line carries the v0.6 hash and commit | L2 |
| R9-1, R9-3; S1-D LOOP 2, 3 | Phase line rewritten with the R9-1 summary; "the current phase (Phase 1)" on first use | L4 |
| R9-4; LOOP 2 | Model-access and network-destination header lines cite the amended texts; both "flagged" markers removed | L5, L6 |
| R9-5; LOOP 1 | Basis line re-pinned (four docs, SoW, DAG-003); DECISION_BRIEF suffix corrected | L8 |
| R9-5; LOOP 1 | New first "Consumed inputs" bullet: R9, briefs, survey, owner records, R8, answers at `afb6e063…`, siblings by Wave A label; OWNER_DECISIONS pin tied to `3733b1421` (V10 N-1) | L10 |
| R9-6; LOOP 4 | Receivers line rebuilt from the registers | L31 |
| R9-4, R9-3 | §0 standing labels and Phases note | L46–L60 |
| — | New "Changes from v0.6" table (12 rows) | L121–L141 |
| R9-4 | §1 consequence 5: "record and show" SETTLED (owner item O-10); V4-HOST-02 cited as amended; ARCH §4 scope sentence cited | L265–L278 |
| R9-1 | §2.3 "A8 request issued": at a checkpoint it is the required request | L449 |
| LOOP 2 | E-4 cites the amended V4-HI-70 | L469 ff. |
| R9-1; LOOP 3 | §2.4 lead replaced by the R9-1 summary, with the "in force / phased" split | L501–L517 |
| R9-1 | §2.4.0 lead; LP-1 (points to LP-5); LP-2 (cites V4-WF-05); **LP-5** retitled "Act requested; recorded only when performed" and states who requests (R9-1, INTEGRATION) | L549–L563 |
| R9-2, R9-4 | LP-6: R8-11 item 2 restated; owner item O-25 cited | L564 |
| R9-2 | C-1 Phase-1 sentence; C-6 Phase-1 paragraph ("no A5 is forced and none is recorded") | L668, L769 ff. |
| R9-4; LOOP 2 | NW-1, NW-2 (quote now the accepted text, ending "(D-18; DEC-5)"), NW-3: both "Accepted-basis note" passages removed | L955–L978 |
| R9-4; LOOP 2 | NW-4…NW-7 each carry their own label: NW-5 and NW-7 SETTLED; NW-6 SETTLED for the script only; NW-4 PROPOSED | L979–L999 |
| LOOP 6 (note only) | N-OPEN-4 stated as an open owner question: open list, NW-8 (interim reading and the other option), MS-15 marked, UNRESOLVED row | L1010, L1053 ff., L1155, L1669 |
| R9-4 | §5.1.1 standing and scope cite the accepted texts; NW-15 qualifier sentence; enforcement bullet SETTLED by V4-ARC-12 | L1031 ff., L1101, L1113 |
| LOOP 2 | §5.2 lead cites the amended V4-EXM-23 for MS-14…MS-23; MS-01 and MS-06 cite V4-HOST-02 as amended | L1131 ff. |
| LOOP 4 | **MS-23** added (disallowed destination; SoW AC-001) | L1163 |
| R9-8; LOOP 4 | §10.1 "Register gap (C1)" → DEP-05-01-025; sibling labels and own version in the standing column | L1400–L1411 |
| R9-6; LOOP 4 | §10.3 rebuilt with register rows and DAG-003 layer, plus a row for DEP-01-05-014; **new §10.4** receivers table (11 rows) | L1427–L1467 |
| LOOP 4 | §11: FX-N range extended to N23 (OUT-002 destination fixtures) | L1506 |
| R9-2 | FX-C9 Phase-1 text | L1518 |
| R9-5 | §13 names the current answers hash beside the delivered one | L1551 ff. |
| R9-8 | G-4 note; G-6 closed; **G-9** (R10 candidate), **G-10** (register and Wave B returns) added | L1605–L1652 |
| R9-8 | UNRESOLVED: three rows CLOSED with citation; two rows added (who requests; FX-C9 wording) | L1670–L1676 |
| LOOP 4 | VC-01 (amended texts, MS-23, "the grants in force"), VC-04, VC-08, VC-09 | L1695–L1703 |
| R9-5 | Live body citations of siblings moved to Wave A labels | §0, §2.4, §2.4.4, §10, §11, UNRESOLVED, VCs |

### 1.2 PANEL_RECEIVING_CONTRACT.md — PANEL-v0.6 → PANEL-v0.7

New sha256: `449a354329766b0f9257563ccee89943675e253fcf4d4c951cc71b5ea0672b34` (was `dd71e11d…5658`). 39 diff hunks; 142 lines added, 50 removed.

| Item | Change | Where (v0.7 line) |
|---|---|---|
| R9-11 | Version label; "supersedes" line | L2 |
| R9-1, R9-3; PANEL 3 | Phase line rewritten with the R9-1 summary | L4 |
| R9-4; PANEL 2 | Model-access and network-destination header lines; "flagged" marker removed; pointer to the §3.8 scope standing | L5, L6 |
| R9-5; PANEL 1 | Basis line re-pinned; V4-HOST-02 and V4-EXM-23 added; DECISION_BRIEF suffix corrected | L8 |
| R9-5; PANEL 1 | New first "Consumed inputs" bullet | L10 |
| R9-6; PANEL 6 | Receivers line rebuilt (DEL-03-04, DEL-09-06, DEL-10-03 added; DEP-05-01-020 marked "not yet defined here"); own input rows listed | L30 |
| R9-4, R9-3 | §0 standing labels and Phases note | L41–L52 |
| — | New "Changes from v0.6" table (11 rows) | L88–L107 |
| R9-1 | §3.1 "A8 requests" cell; model setting indicator cites V4-HOST-01/02 as amended | L264 |
| R9-1 | §3.2 "Checkpoints as plan guidance" cites V4-WF-05 | L276 |
| R9-2 | §3.3 "Direct autonomy and checkpoints" | L295 |
| R9-1; PANEL 3 | §3.5 Phase-1 lead; **W-5a "Act request" bullet** | L335–L348, L380–L391 |
| R9-8; PANEL 2 | §3.6 line on DEL-04-02 (now in SoW CLM-002/REQ-006 and DEP-05-02-019) | L519 |
| R9-4; PANEL 4 | §3.8 lead cites the accepted texts; **"Standing against this deliverable's ScopeOfWork"** paragraph | L566–L600 |
| PANEL 6 | ND-4 cites the amended V4-HI-70 | L604 |
| PANEL 6 | §5 act table: row for the A12 network-destination grant and its decline | L649 |
| R9-2 | PC-24 Phase-1 text | L782 |
| PANEL 6 | "Present state": PC-30…PC-37 cite V4-EXM-23; note on LOOP MS-23 | L802 ff. |
| R9-5 | §8 current answers hash | L820 ff. |
| R9-8; PANEL 2 | F-1 note; F-3, F-4, F-5, F-9 closed with their records; **F-12** (scope standing), **F-13** (DEP-05-01-020) added | L870–L928 |
| R9-8; PANEL 2, 4 | UNRESOLVED: four rows CLOSED (V4-WF-05, V4-HOST-01, V4-HOST-02, DEL-04-02); two rows added (who requests; scope of §3.8); N-OPEN-4 row says "open owner question" | L944–L956 |
| R9-5, R9-1 | VC-01, VC-03 | L967, L969 |
| R9-5 | Live body citations of siblings moved to Wave A labels | §0, §1, §3.1, §3.2, §3.5, §3.8, §7, §8, UNRESOLVED, VCs |

### 1.3 HOSTING_BOUNDARY.md — HOSTING-BOUNDARY-v0.6 → v0.7

New sha256: `fe09bf9456210e6068cd0299ad3cdc3f9b6ccd05dd830252689d6387cdb417e4` (was `d11d4c57…d0b9`). 28 diff hunks; 128 lines added, 35 removed.

| Item | Change | Where (v0.7 line) |
|---|---|---|
| R9-11 | Version label; "supersedes" line | L2 |
| R9-1, R9-3 | Phase line cites the amended V4-WF-05; "no act request in an agent's place" | L4 |
| R9-4 | Model-access and network-destination header lines cite the amended texts and the ARCH §4 scope sentence | L5, L6 |
| R9-5; HOSTING 1 | Basis line re-pinned (four docs, SoW `9945e72b…`, DAG-003) | L8 |
| R9-5, R9-10; HOSTING 1; PIN_SPIKE 2 | New leading "v0.7 inputs" text in Consumed inputs: R9, owner records, answers at `afb6e063…`, **PIN-SPIKE standing**, siblings by Wave A label, corrected statement on the other deliverables' SoWs | L9 |
| R9-6; HOSTING 3 | Receivers line rebuilt (own rows; six admitted first-increment consumers with arc labels; outside consumers) | L10 |
| — | New "Changes from v0.6" table (10 rows) | L35–L53 |
| R9-4; HOSTING 2 | §2 DECISION-5 scope note quotes the ARCH §4 scope sentence; three bullets updated | L205–L222 |
| R9-7 | §6.4 "read settlement" caller cell | L552 |
| R9-1 | §6.7 Phase-1 lead | L586–L594 |
| HOSTING 1; R9-5 | §6.7: "EXEC-v0.2 HP-2" → EXEC-v0.5 §2.3; other live EXEC labels | L607–L632 |
| R9-7, R9-6; HOSTING 3 | S-7 row: DEL-04-03 directly; DEL-09-06 added; DEL-01-02's custody named as separate | L777 |
| R9-6; HOSTING 3 | **New receivers table** after the seams table (11 rows); the inventory paragraph keeps its place as §8's closing paragraph and says what DEP-02-01-025 names | L779–L807 |
| HOSTING 2 | L-4 renamed and restated against the amended priority 3; L-5 cites V4-HOST-01 as amended | L816, L817 |
| R9-7 | §8.2 route sentence | L832 ff. |
| R9-4 | §8.3 "record and show" SETTLED (owner item O-10) | L853 |
| R9-6, R9-7, R9-8; HOSTING 2, 3 | F-07, F-14, F-16, F-24, F-25 updated; **F-26** (evidence route), **F-27** (harness-capability meaning) added | L1094–L1203 |
| HOSTING 2 | U-18 restated | L1226 |

R9-7 check before editing: DEL-01-01's own ScopeOfWork (`9945e72b…`) states no evidence route. CLM-004 gives DEL-01-02 "durable sessions, outstanding-request recovery, reconnect/relaunch and explicit stop behavior"; CLM-005 gives DEL-04-03 "content-bound records". Nothing says evidence passes through DEL-01-02, so the item was applied, not stopped.

### 1.4 Leftover-phrase grep (as instructed)

`grep -n -i -F` on each file after editing.

| Phrase | LOOP | PANEL | HOSTING |
|---|---|---|---|
| "flagged for the next accepted-basis update" | L132 (new change row, quoting what was removed); L153, L167 (history rows of "Changes from v0.5") | L99 (new change row, quoting); L119, L133 (history rows) | none |
| "first half" | L132 (new change row, quoting); L153 (history row) | L99 (new change row, quoting); L119 (history row) | none |
| "second half" | L132 (new change row, quoting); L153 (history row) | none | none |
| "override autonomy" | none | none | none |

Every remaining hit is either a history row that R9-5 says is not rewritten, or the new change row that names the phrase it removed. No live rule carries any of the four.

## 2. Survey items not applied, or applied differently

| Survey item | Disposition | Reason |
|---|---|---|
| LOOP 5, 7, 8, 9 | Not started | Wave B (brief) |
| LOOP 6: rule N-OPEN-1 and release MS-11 | Not applied | The brief forbids ruling N-OPEN-1. MS-11 stays held |
| LOOP 6: put N-OPEN-4 to the owner | Applied as a note only | Stated as an open owner question with its interim reading and the two options; not ruled |
| LOOP 2: relabel NW-6 from the amended V4-ARC-12 | **Applied in part; I disagree with the survey here** | V4-ARC-12 and SoW REQ-001/AC-002 state only that credentials stay "outside the interface's script". NW-6 also lists messages, events, records, the panel and errors. That wider list has no accepted text, so it stays PROPOSED |
| LOOP 2: "delete the two accepted-basis notes", "close UNRESOLVED rows" | Notes replaced by citations; rows kept and marked CLOSED | R9-8 says "closed with the citation"; the file's own style keeps closed rows |
| LOOP 4: "one case for a destination neither allowed nor requested" | Applied as MS-23, with one part left open | The refusal and its record follow existing rules (§2.3 "destination refused at boundary"; NW-7; NW-15). What the requesting call receives among TL-2's result classes is not defined anywhere, so MS-23 says so and leaves it to Wave B |
| PANEL 2: "remove the three obsolete UNRESOLVED rows and F-9" | Rows and F-9 kept, marked CLOSED with citation | R9-8; traceability |
| PANEL 5, 7, 8 | Not started | Wave B |
| HOSTING 2: "restate L-4, F-14 and U-18 against the amended priority 3" | Applied as a statement of fact, not a new rule | The amended priority 3 speaks of a host's agent. No accepted text now frames the supplier's start-up traffic in the App. The three passages say that and leave the question with the owner (U-18) |
| HOSTING 4, 5, 6, 7 | Not started | Wave B |
| PIN_SPIKE 1–3 | No edit; standing stated in HOSTING's header | R9-10 |
| S1-D §1 LOOP pin 15 / V10 N-1 ("at `1528a5033`") | History line left as written; the new v0.7 input line ties `5fd780bf…` to `3733b1421` and records that the file was `9903bfe0…7fbf` at `1528a5033` | R9-5: history lines are not rewritten |
| S1-D PANEL §2 remark on "The sibling v0.3 elements were confirmed by V2" (§7) | Left | A true historical statement; not in the item list |

Sibling labels in live body text (for example "EXEC-v0.4 §2.1") were moved to the Wave A labels. The survey did not ask for this; the brief's rule "cite siblings at their Wave A versions" does. History tables and consumed-input history lines keep the old labels.

## 3. R10 candidates (R9-9)

1. **FX-C9 / PC-24 disposition wording.**
   - Passage A, R9_RESOLUTIONS R9-2: "its act is still requested, no act is recorded by reason of the direct application, and the checkpoint's disposition stays *act not performed* unless the person performs it."
   - Passage B, LOOP §2.4 and §2.4.1: "Dispositions (shared): waiting · performed · resolved negatively · lapsed · not reached · unknown"; "If the run ends without the condition having been observed, the checkpoint is **not reached**." FX-C9's A5 checkpoint has reached-when kind (c) *proposal queued*; under a direct application nothing is queued.
   - Options: (a) "act not performed" is a plain description and the shared disposition is *not reached*; (b) the direct application counts as an arrival, labelled *waiting*, which changes a reached-when rule owned by DEL-02-01 and DEL-02-03; (c) keep *not reached* and add a record annotation for "requested, not performed".
   - State now: LOOP FX-C9 carries both wordings (G-9); PANEL PC-24 says "shows no act performed". C, ADAPTER and CA (other executors) use R9-2's words.

No other disagreement without a deciding text was found in these three files. Two things that look like candidates are not:

- N-OPEN-4 (V4-HOST-02 "by category … or by named destination" against ARCH §4 "named destinations within each category") is already an owner question; stated, not ruled.
- DEP-02-01-025 "harness capability meaning" against HOSTING's inventory: WD (Wave A) and HOSTING now say the same thing (inventory supplied; names and portable meaning not yet defined in either file). It is a Wave B item, not a disagreement.

## 4. Proposed ScopeOfWork, register or basis items (for a later amendment; none made)

| # | Kind | Item |
|---|---|---|
| 1 | ScopeOfWork, DEL-05-02 | **Scope question, returned.** PANEL §3.8, PC-30…PC-37 and F-11 define network-destination surfaces. The SoW does not name them ("destination" occurs 0 times; AX-004 omits DECISION-5; "recorded and shown" is SOW-017, assigned to DEL-05-01). Owner choice: amend DEL-05-02's SoW to name the display of destinations, or leave §3.8 as PANEL's receiving of DEL-05-01's obligation (PANEL F-12) |
| 2 | Register, DEL-05-01 | No DOWNSTREAM relay row to DEP-001 (closeout R5-1-3). The Receivers line had cited DEP-05-01-021, which is an UPSTREAM row |
| 3 | Register, DEL-05-01 | No mirror of DEP-01-05-014 (DEL-01-05 supplies local-server capability requirements; closeout R5-1-2) |
| 4 | Register, DEL-01-01 | No DOWNSTREAM rows for its admitted consumers DEL-02-01, DEL-02-03, DEL-02-04, DEL-03-03, DEL-03-04, DEL-04-03, DEL-09-06 (HANDOFF_STATE "Deferred supplier-side mirror rows") |
| 5 | Register / ScopeOfWork, DEL-02-01 | DEP-02-01-025 says "harness capability **meaning** supplied through DEL-01-01"; its SoW CLM-002 says DEL-01-01 "supplies the harness capability **inventory**". One wording should be chosen |
| 6 | Basis | ARCH §1 priority 3 as amended speaks only of a host's agent. If the owner wants a rule for the App supplier's own start-up traffic (HOSTING U-18), no accepted text states one |
| 7 | Basis | V4-HOST-02 ("or by named destination") and ARCH §4 ("named destinations within each category") should read alike once N-OPEN-4 is decided |
| 8 | Basis (observation) | R9-5 names SCA-V4-002 for the four basis docs. Their headers name only SCA-V4-001; SCA-V4-002 changed only HOST_INTEGRATION's line layout (`70376aff2`) |

## 5. Wave B items found beyond the survey's

1. **Link between an A8 and the arrival it answers (LOOP).** R9-1 says the product records "the request where it can be identified". LOOP has the "A8 request issued" event and the "checkpoint reached" event, but no rule for when an A8 counts as the request for a given arrival (for example an A8 issued before the arrival event). For App runs this is EXEC's; host loops need the same statement.
2. **MS-23's result to the agent (LOOP).** A specific of survey LOOP 5: the refusal of an unrequested, disallowed destination has no place among TL-2's four result classes.
3. **PANEL has no case for a boundary refusal.** ND-4 shows "boundary refusals, shown apart from contacts", but no PC case exercises it (LOOP MS-06, MS-20, MS-23).
4. **Panel-needs list (PANEL).** DEP-05-01-020 asks for it; PANEL has none (F-13). The survey noted the gap in §6 but its item 5 lists only "return inputs".
5. **R9-2's "act not performed".** If kept as a term, it needs a place in the shared vocabulary (EXEC §4.3, WD, RS), see R10 candidate 1.
6. **HOSTING U-18's point of need** reads "Before any local-operation claim". After the amendment no accepted text defines such a claim for the App; the point of need should be restated when the owner rules.
7. **Outside consumers.** DEL-08-01 (DEP-08-01-008) expects the destination constraint a Domains query must meet, and LOOP leaves that traffic open (N-OPEN-3). DEL-09-02 (DEP-09-02-009) expects "scoped feature checks", and HOSTING §9 is designed only.
8. **Sibling section numbers.** The three files cite siblings by Wave A label with section numbers checked against the pre-Wave-A texts. They need one pass against the integrated Wave A bytes (with GUIDE, A1-G).
9. **Independent pair check.** LOOP G-4 and PANEL F-1 now also cover the v0.7 edits (one executor again).

## 6. Pin tables as they now stand

Checked means: `shasum -a 256` of the working-tree file, after the edits, equals the value written. "Label only" means a sibling cited by version label and section (R9-5), with no byte pin.

### 6.1 Common to the three headers

| Pin | Value | How checked |
|---|---|---|
| `docs/PRD.md` | `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` | shasum; header names SCA-V4-001 |
| `docs/ARCHITECTURE.md` | `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c` | shasum |
| `docs/HOST_INTEGRATION.md` | `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` | shasum; last changed by SCA-V4-002 (`70376aff2`) |
| `docs/EXAMINATION.md` | `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` | shasum |
| `_DAG/_LATEST.md` → DAG-003 | label (file sha256 `4d381ba4…2f56`, not written in the headers) | read: "Latest: DAG-003", accepted 2026-09-29 |
| R9_RESOLUTIONS.md | `c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c` | shasum |
| This run's BRIEFS.md | `698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a` | shasum |
| This run's OWNER_DECISIONS.md | `0730c6f3d174a8acddbd0c9fabb62afd4d6444847a612f0de7ff3ba584303722` | shasum |
| SURVEY/S1-D.md | `a3b0546af4131e0302520bc0dbaad8d6d5587e91d896fb8aa559e32768b19419` | shasum |
| R1–R7 | by file name (`APP-V4-FIRST-INCREMENT-20260928/R1_RESOLUTIONS.md` … `R7_RESOLUTIONS.md`) | files exist (ls); abbreviated hashes in the older Basis text match the files' prefixes |
| R8_RESOLUTIONS.md | `44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b` | shasum; equal at `1528a5033` and `3733b1421` (`git show … | shasum`) |
| Intake OWNER_DECISIONS.md | `5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2` | shasum; equals `3733b1421`; at `1528a5033` the file was `9903bfe0…7fbf` (`git show`) |
| First-increment OWNER_DECISIONS.md | `a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c` | shasum |
| BASIS-ALIGN OWNER_DECISIONS.md | `ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b` | shasum |
| BASIS-ALIGN `AMENDMENT_PACKET/OWNER_ITEMS.md` | `2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef` | shasum; equals the prefix DECISION-7 records ("`2b90eb4a…`") |
| SCA002 OWNER_DECISIONS.md | `36ffcbbea923504581844456751c2eb3db617b5471a3595e63f036bf0634b480` | shasum |
| `RELAY_ANSWERS_SWBPIPE.md` | `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74` | shasum; `git diff f5ceef164 HEAD` shows three changed lines (SQ-04, SQ-09, SQ-27) |
| `FACTS_SQ01_SQ32.md` | `733fb88a701317be8f0054937eca058774ba5f5f30c7a27233718996e8b2ab7e` | shasum |
| DECISION_BRIEF.html (LOOP, PANEL) | `02d38cb1…c4420e8` (abbreviated) | shasum of `_Coordination/Acceptances/APP-V4-BASIS-20260926/DECISION_BRIEF.html` = `02d38cb18041…bbc100c4420e8` |
| Siblings | EXEC-v0.5, WD-v0.7, WD-EX-v0.7, C-v0.7, P-v0.7, ADAPTER-v0.5, GUIDE-v0.4, ACT-POLICY-v0.7, AS-v0.7, RS-v0.7, CA-v0.5, XT-v0.5, RELAY-v0.3, PIN-SPIKE-v0.1 | label only (R9-11 table) |

### 6.2 Per file

| File | Pin | Value | How checked |
|---|---|---|---|
| LOOP | ScopeOfWork.md (DEL-05-01) | `9b2379a14e2c9da4310f62e72d83a6e7506ef37f70c4a38b41d76908bca985ed`; revised under SCA-V4-001 (AX-004) at `340ecf341` | shasum; `git log` |
| LOOP | Superseded version | LOOP-v0.6 `246f4636166c67250f73862de586afef3cad91ba538272880a80c2fd657a5767`, last changed `caa4334ca` | shasum of the pre-edit copy; `git log -1` |
| LOOP | Siblings of the pair | PANEL-v0.7, HOSTING-BOUNDARY-v0.7 | label only; sections cited were read in the v0.7 texts |
| PANEL | ScopeOfWork.md (DEL-05-02) | `beb9c66c38161cbb00d1040e294aa9dfd04af953f9bf539121fcda44356dc82c`; revised under SCA-V4-001 (AX-004) at `340ecf341` | shasum; `git log` |
| PANEL | Superseded version | PANEL-v0.6 `dd71e11dbe0d9872727524aef69ef80ba118980533148c2aa7453d1176165658`, last changed `caa4334ca` | as above |
| PANEL | Basis line additions | V4-HOST-02; V4-EXM-23 | grep in PRD and EXAMINATION |
| HOSTING | ScopeOfWork.md (DEL-01-01) | `9945e72b04b4f45c4c641a5248cca8bc2ac40bf4897d1018c5ab59eba307cc75`; revised under SCA-V4-001 (AX-005, `340ecf341`) and SCA-V4-002 (AX-006, `1efd4bcda`) | shasum; `git log` |
| HOSTING | Superseded version | HOSTING-BOUNDARY-v0.6 `d11d4c574aa3c342bfac9c1d1e9bf3746aa885baafd17eaa296a79a523e3d0b9`, last changed `3733b1421` | as above |
| HOSTING | PIN-SPIKE-v0.1 | `0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115`, unchanged; its own basis pins (`eddd122c…4773`, `f3f8e5f3…1f2e`) read from its line 5 | shasum before and after |
| HOSTING | MANIFEST.sha256, COMMITTED_STATE.md | unchanged history text (`42b95826…569e`, `2cb7f1d2…2608`) | not re-verified by me; the survey recomputed both as current |
| HOSTING | Other deliverables' ScopeOfWork | DEL-01-02, -03, -05, -06 and DEL-02-04 byte-identical to `6e18505e3`; DEL-04-01 changed at `340ecf341`; DEL-01-04 at `1efd4bcda` | `git diff --stat 6e18505e3 HEAD` per file |

Historical pins in the older header text (LOOP-v0.5 `0ec980b5…`, PANEL-v0.5 `ac47abf0…`, HOSTING-v0.5 `f1a23022…`, intake OWNER_DECISIONS `a5ccab0d…` at `94aa9181b`, R8 `d4c34233…` and `1770c96e…`, BRIEFS `3e33ba26…`, EXEC-v0.4 `d32be377…`, WD-v0.6 `fce565ed…`, the delivered answers `6f01add3…`) were not rewritten and not re-verified by me; the survey classed each as historical-true.

Register facts used for the Receivers lines were read by script from every `Dependencies.csv` under `PKG-*/1_Working/` (ACTIVE rows whose target is DEL-05-01, DEL-05-02 or DEL-01-01), and the layer from `_DAG/DAG-003/DependencyEdges.csv` (admitted) and `CandidateEdges.csv` (held). Arc labels N-15, N-16, N-23, N-B4, N-B9 and N-C5 were checked by grep across `_DAG/DAG-003/` and `APP-V4-BASIS-ALIGN-20260928/DAG_PREP/`; R8-A, R8-B and N-C6 in that `DAG_PREP/` folder.
