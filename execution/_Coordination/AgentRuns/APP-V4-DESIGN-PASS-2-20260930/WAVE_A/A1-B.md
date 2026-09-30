# A1-B — alignment wave return: DEL-03-01, DEL-03-02, DEL-03-03

- Run `APP-V4-DESIGN-PASS-2-20260930`, node **A1-B**. Type 2 TASK executor (Claude Code subagent); no delegation. No git writes. No network.
- Working tree at `3dd7c22c73` (branch `claude/chirality-app-v4-60-percent-a41fd5`), 2026-09-30.
- Written: the three Design files below and this file. Nothing else. No ScopeOfWork, register, `_STATUS.md`, basis, decomposition, scope-change or DAG file was edited.
- Inputs read whole: this run's `BRIEFS.md` ("Common rules", "A1"), `R9_RESOLUTIONS.md`, `SURVEY/S1-B.md`; the three Design files; the three `ScopeOfWork.md`; `_DAG/DAG-003/HANDOFF_STATE.md`. Read in part: the three `Dependencies.csv` and every register row that targets DEL-03-01/02/03 (by script); `R8_RESOLUTIONS.md` R8-10…R8-12; R2-7 and R4-2…R4-6; SCA-V4-001 `OWNER_ITEMS.md` O-4, O-10, O-25; the four `OWNER_DECISIONS.md` files; `reviews/V10.md` S-2, N-1 and V10b; RS-v0.6 §4 R11, §6.1, §7, §10; ACT-v0.6 §8.1; AS-v0.6 §3.
- Method: each edit was an exact-string replacement, asserted to match once, applied by script (scripts and the three pre-edit copies are in the session scratch folder). Every pinned sha256 was recomputed with `shasum -a 256`. Every quoted requirement text was compared with its current source after whitespace normalization.

| Short | File (under `PKG-03*/1_Working/`) | From → to | Lines | New sha256 |
|---|---|---|---|---|
| **C** | `DEL-03-01*/Design/CATALOG_AND_READ_BASIS.md` | C-v0.6 → C-v0.7 | 968 → 1027 | `6ebdf94d25b4e31cee6c7da8dc9e60d0a5157b9bcac07bce8a60ddd61002f709` |
| **P** | `DEL-03-02*/Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | P-v0.6 → P-v0.7 | 878 → 941 | `5ee6c5b416f869e526e92afe4e3c9b2b5c6abd23bce7d4b15880a996a9a95b1c` |
| **ADAPTER** | `DEL-03-03*/Design/ADAPTER_ENABLEMENT_AND_RECEIVING.md` | ADAPTER-v0.4 → ADAPTER-v0.5 | 1352 → 1429 | `41a24c9376f298ec3db2cf984b6b892901a30352ba60243d3df3c32e3a9bcbf6` |

Pre-edit hashes equalled the survey's (`8282c003…`, `410fb289…`, `6e13ab11…`) and the bytes at `HEAD`. All three files stay DRAFT.

## 1. Changes made

Each file also carries a new "Changes from ‹previous›" table with the same content, keyed by R9 ID and survey item.

### 1.1 C — 29 changes

| # | Item | Change | Where |
|---|---|---|---|
| 1 | R9-11 | Version and supersession line | Header, Contribution |
| 2 | R9-1, R9-3 | Phase line: "first half" and "flagged" dropped; "the current phase (Phase 1)"; request and record in force, hold phased | Header, Phase |
| 3 | R9-5 | Basis re-pinned (four docs, SoW with AX-004, DAG-003, Case_Datasheet, OWNER_DECISIONS, R6…R9); v0.6 pins kept as history | Header, Basis |
| 4 | R9-5 | Consumed inputs: Wave A paragraph (siblings by label; RELAY_ANSWERS `afb6e063…`); earlier passes marked history | Header |
| 5 | V10 N-1 | R8-13 sentence reordered so only R8_RESOLUTIONS is placed at `1528a5033` | Header |
| 6 | R9-6 | Receivers rebuilt from ACTIVE rows, with row IDs; DEL-03-04, DEL-09-06, DEL-10-03 added; "unregistered join" notes removed; DEP-05-01-014 schemas "not yet defined here" | Header |
| 7 | R9-1 | Phase paragraph: R9-1 summary verbatim; in force / phased; who requests (INTEGRATION), pointing to EXEC Wave B | §0 |
| 8 | R9-2, R9-4 (O-25) | S-C10 restated | §0 table |
| 9 | S1-B 1.2, 1.6 | DEL-04-03 row: C consumes the act field set and lapse vocabulary (CLM-002; DEP-03-01-031) | §1 |
| 10 | R9-4 | Invariant 5 cites SoW REQ-002 | §2 |
| 11 | R9-4 | Exposure element cited to REQ-002 (quoted) | §3 intro; element 9 |
| 12 | R9-4 | *no policy basis* cited to REQ-002; INTEGRATION label dropped on the value | §3.1 |
| 13 | S1-B 1.8 item 3 | Value standing adds PROPOSED (ACT §8.1) | §3.1 |
| 14 | R9-2 | Class rule 3, Phase 1: direct application — act still requested, no A5 forced or recorded, *act not performed* | §3.1 |
| 15 | S1-B pin 22 | "as of C-v0.5 / P-v0.5, carried in C-v0.7 / P-v0.7" | §4.1 |
| 16 | R9-4 (O-10) | Model destination: record-per-turn-and-show SETTLED; R5-4 detail stays INTEGRATION | §4.1 |
| 17 | R9-1 | V4-HOST-02 "flagged" → "as amended by SCA-V4-001"; quote unchanged | §4.1 |
| 18 | R9-4 | Subject identity and whole-model identity cited to REQ-004; INTEGRATION dropped on the latter | §5.3 |
| 19 | S1-B 1.8 item 3 | Human-act evidence row: "act kind"; consumed, not defined; RS §6.1 elements not listed here are named | §6.2 |
| 20 | S1-B 1.8 item 3 | Lapse-state row: "current · superseded" for A12/A13 (R2-7 stays PROPOSED) | §6.2 |
| 21 | R9-6 | Mirror note restated | §9 |
| 22 | R9-1 | FXA-5 Phase 1: the act is requested | §10.1 |
| 23 | R9-2 | V-CP1 Phase 1: the R9-2 sentence | §10.4 |
| 24 | R9-1 | V-GR1 Phase 1: the A12 is requested | §10.4 |
| 25 | S1-B 1.2 item 6 | U-C8 names the current ACT version | UNRESOLVED |
| 26 | R9-8 (C23) | Register row restated against current registers | UNRESOLVED |
| 27 | R9-8 (C24) | SoW-text row closed (SCA-V4-001), struck through | UNRESOLVED |
| 28 | R9-5, R9-11 | Sibling labels: P-v0.7 (×4), WD-v0.7, LOOP-v0.7, EXEC-v0.5 | §0, §4.1, §9, VC-C-04, header |
| 29 | R9-11 | "Changes from v0.6" table | new section |

### 1.2 P — 27 changes

| # | Item | Change | Where |
|---|---|---|---|
| 1 | R9-11 | Version and supersession line | Header |
| 2 | R9-1, R9-3 | Phase line, as C | Header |
| 3 | R9-5 | Basis re-pinned (SoW with AX-004; V4-HI-42, V4-HI-70, V4-EXM-22 marked amended; R6…R9) | Header |
| 4 | R9-5 | Consumed inputs: Wave A paragraph; R8 and intake OWNER_DECISIONS at current sha256; earlier passes marked history | Header |
| 5 | R9-6 | Receivers rebuilt with row IDs; N-18, N-21, DEL-09-06, DEL-10-03 added | Header |
| 6 | R9-1 | Phase paragraph, as C | §0 |
| 7 | R9-1, R9-2, R9-4 | S-P13 opens with the amended V4-HI-42 (quoted), not "Workflow checkpoints override autonomy" | §0 table |
| 8 | R9-4 | "never silently converted": DEL-03-03 SoW REQ-003 cited for the external channel; INTEGRATION kept for the general rule | §2 |
| 9 | R9-4 | Change-item content identity cited to SoW OUT-001 | §3.1 |
| 10 | R9-4 | Workflow identity cited to SoW CLM-003 / DEP-03-02-027 | §3.3 |
| 11 | S1-B 2.6 | First grant state named "effective (person-set)" | §3.3 |
| 12 | R9-4 | Constraint element cited to SoW OUT-001, CLM-003 (governance phase only) | §3.3 |
| 13 | R9-8 (R8-12 item 5) | "constraint not carriable on this host": PROPOSED → adopted in RS R11 | §3.3 |
| 14 | R9-4 | Per change item; *rejected* only A10; host refusal is *refused*: cited to REQ-004 | §4.1 (3 edits) |
| 15 | R9-4 | Cleared-queue row: "never read as A10 or A11" cited to REQ-004; the mapping stays INTEGRATION | §4.2 |
| 16 | R9-1, R9-2 | Acceptance-checkpoint bullet: derivation re-grounded; request and record clauses in force; direct application sentence | §4.4 |
| 17 | R9-1 | Other checkpoints, Phase 1: the act is requested | §4.4 |
| 18 | R9-4 | One effect per item cited to REQ-008 | §7 |
| 19 | R9-8 (R8-12 item 5) | "host reachable without evidenced A13" named at the A13 row | §10 |
| 20 | R9-6 | §13: note; row IDs; N-18/N-21 contributions named; rows for DEL-09-06 and DEL-10-03 | §13 |
| 21 | R9-2 | E-2, V-CP1 Phase 1 row | §14 |
| 22 | R9-8 (P16) | Register row restated | UNRESOLVED |
| 23 | R9-8 (P17) | SoW-text row closed | UNRESOLVED |
| 24 | R9-4 | VC-P-09 cites AC-009 | VC |
| 25 | R9-8 (P26) | VC-P-14 follows VER-014, names the checker, records one tool observation | VC |
| 26 | R9-5, R9-11 | Sibling labels: C-v0.7 (16 places), WD-v0.7 | body, VC |
| 27 | R9-11 | "Changes from v0.6" table | new section |

### 1.3 ADAPTER — 29 changes

| # | Item | Change | Where |
|---|---|---|---|
| 1 | R9-11 | Version and supersession line | Header |
| 2 | R9-1, R9-3 | Phase line | Header |
| 3 | R9-5 | Basis re-pinned (SoW with AX-004 and AX-005; DAG-003; R6…R9); the v0.1–v0.4 pins kept and labelled history | Header |
| 4 | R9-5 | Consumed inputs: Wave A bullet; the earlier bullets labelled history | Header |
| 5 | V10 N-1 | R8-13 sentence reordered | Header |
| 6 | DECISION-6 (N-B8) | Note on the RS "for joins only" input: read as the destination of this file's evidence | Header |
| 7 | R9-6 | Receivers rebuilt: DEL-02-03 (N-24), DEL-04-03, DEL-09-06 by their own rows; DEL-01-01 and DEL-02-03 now registered suppliers; supply-only toward DEL-04-03 | Header |
| 8 | R9-1, R9-2, R9-4 | S-X10 opens with the amended V4-HI-42 (quoted), not "Checkpoints override autonomy" | §0 table |
| 9 | R9-1, R9-4 (O-10) | S-X11: record-and-show SETTLED; V4-HOST-02 "as amended" | §0 table |
| 10 | S1-B 3.2 item 5 | New row: host adoption and enforcement of its reserved list (REQ-005, SCA-V4-002) | §1 |
| 11 | R9-8 (A2) | Realization families: interposed not adopted, by record | §2 |
| 12 | R9-4 | Model-destination row label | §3.1 |
| 13 | R9-4 | E-2 cites SoW AC-002, which now states the R4-13 reading (quoted) | §3.3 |
| 14 | S1-B 3.3 | §3.4 heading: V4-HOST-02 and V4-EXM-23 "for the host's own agent only" | §3.4 |
| 15 | R9-4 | "Recorded and shown" label | §3.4 |
| 16 | R9-1, R9-8 (V10b S-2) | V4-HOST-02 bullet: "flagged" removed; "The owner's revised wording:" → "The amended text:"; V4-EXM-23 pointer | §3.4 |
| 17 | S1-B 3.2 | Supplier facts "consumed from DEL-01-01" (CLM-002; DEP-03-03-013) | §3.5 |
| 18 | R9-1, R9-2 | Phase paragraph: request and record in force on X; direct-application sentence | §5.3 |
| 19 | R9-4 | One effect per item cited to REQ-004 | §7.3 |
| 20 | R9-1 | Phase 1: who requests; what the product records; pointer to EXEC Wave B; N-24 row | §7.7 |
| 21 | R9-8 (A2) | §9 intro and OC-2: decided for this increment by record (native) | §9 |
| 22 | R9-2 | XF-25 Phase 1 | §10.2 |
| 23 | R9-6 | §11: note; row IDs; DEL-09-06 row; N-24 "prose only"; RELAY row marked "by citation" with the K-11 guard | §11 |
| 24 | R9-5 | RELAY-v0.3 cited by label; former byte pin kept as history | §12 |
| 25 | R9-8 | F-10, F-13, F-14 closed; F-11 partly closed | §13.1, §13.2 |
| 26 | R9-8 (A28) | UNRESOLVED: TBD-007 row effect; register/SoW row restated, SoW parts closed | UNRESOLVED |
| 27 | R9-4 | VC-X-02: AC-002; record-and-show label | VC |
| 28 | R9-5, R9-11 | Sibling labels in body and VC (27 places) | body, VC |
| 29 | R9-11 | "Changes from v0.4" table | new section |

### 1.4 Leftover-wording check (after editing)

`grep` for "flagged for the next accepted-basis update", "first half", "second half", "override autonomy":

| File | Hits | Account |
|---|---|---|
| C | L855 (new "Changes from v0.6" row, quoting the dropped words); L879 and L893 ("Changes from v0.5" rows R8-1, R8-13) | History rows and the row that records the removal. None in live text |
| P | L798, L800 (new change rows, quoting the dropped words); L820 ("Changes from v0.5" R8-1 row) | Same |
| ADAPTER | L1339, L1351 ("Changes from v0.3" rows R8-1, R8-13); L1370, L1371, L1373 (new change rows) | Same |

"second half": no hit in any file. The R8-11 history rows that say "V4-HI-42 are guidance in Phase 1" (C L889, P L828, ADAPTER L1348) are left as history. No live sentence says V4-HI-42 is guidance.

## 2. Survey items not applied, and where I differ from the survey

| Item | What I did | Reason |
|---|---|---|
| C 1.8 item 7: C10 (U-C4) | Not closed | The survey marks it its own inference. No record states it. R9-8 closes only rows a record has closed |
| C 1.8 item 7: C25 (catalog edition) | Left PROPOSED | Needs an integration ruling. R9 gives none; R9-4 keeps PROPOSED |
| C 1.8 item 7: C27 (*superseded*) | Vocabulary aligned to RS ("current · superseded"); label kept | R2-7 is itself labelled PROPOSED in `R2_RESOLUTIONS.md` |
| C 1.8 item 7: C6 | No edit | Carried to the DEL-04-01 node (section 5 below) |
| C 1.8 item 7: C24 "delete" | Row struck through and marked Closed | The file's convention keeps closed rows |
| C 1.8 item 1: "current EXEC, WD, WD-EX bytes" | Not pinned by bytes | R9-5: siblings by label and section only |
| P 2.8 item 3, second half ("settle which phase") | Not settled | No deciding text: R10 candidate 1 |
| P 2.8 item 6: P8, P13, P19, P21, P22 | Left PROPOSED | P's own proposals (U-P4, withdrawal before queueing, sibling drafts) have no ruling; R2-7, R4-4 and R4-5 are PROPOSED in their rulings. R9-4 |
| P 2.8 item 6: P26 "run the checker" | Wording fixed; the tool was run once, read-only, and the result recorded in VC-P-14 | `check_boundary_owner_resolution.py` on the SoW `35609151…`: 1 boundary requirement checked, 0 unresolved, 0 NOT_CHECKABLE, 0 NO_CITED_CLAIM, exit 0. The one-for-one review against §1 and §13 is not run |
| ADAPTER 3.8 item 9: A29 (PROPOSED App-side rules) | Left PROPOSED | R9-4. Two readings did lose INTEGRATION because a revised SoW now states them: E-2 (AC-002) and record-and-show (REQ-002, O-10) |
| ADAPTER 3.8 item 2: "re-word L18" | Annotated, not rewritten | L18 records what was read (history, R9-5). The note says RS was read as the destination of this file's evidence |
| ADAPTER 3.8 optional: move old input lists to a history note | Not done | Optional; would reflow unaffected text |
| All Wave B items (C 4–6, 8; P 4, 5, 7; ADAPTER 3–8) | Not started | Brief |

Differences from the survey:

- **R9-8 "two evidence-limit labels in P".** P-v0.6 carried only one ("constraint not carriable on this host"). I added a one-clause pointer to the second ("host reachable without evidenced A13") at the §10 A13 row, citing C §4.1 and RS R11.
- **V10 N-1** is not in the listed items for C. I applied it in C and ADAPTER together, because it is the same sentence and survey §1.7 lists it open for C.
- **R9-4 changes** (the O-10 model-destination reading; REQ-002/REQ-004/AC-002 citations) are not in the survey, which preceded R9. I applied them and kept INTEGRATION on the parts no text states (the R5-4 per-turn detail; class rule 4's treatment; the §5.4 staleness rule; the R8-5 mappings).
- **A first draft of my own history clause was wrong** and is corrected: the first-increment `OWNER_DECISIONS.md` state `f3f8e5f3…` did not exist at `6e18505e3`; it was committed at `be8bb46dd3`. C and P now say so.

## 3. R10 candidates (R9-9)

1. **Phase of "constraint not carriable on this host".**
   - RS §4 R11: "constraint not carriable on this host (governance phase; R8-10)"; RS U-19 puts it under "Governance phase".
   - P §3.3 Phase-1 bullet and ADAPTER §5.3 GC-4 ("*Phase 1:* the expected constraint is recorded only; where the host schema defines no element for it, the record carries the evidence limit").
   - R8-12 item 5 adopts the label and names no phase. Options: (a) current phase, RS relabels; (b) governance phase only, P and ADAPTER move it; (c) both phases, since GC-4 records the expected constraint in both.
2. **R9-2's "*act not performed*" against the disposition vocabulary and the reached-when kind.**
   - R9-2, now in C §3.1 rule 3 and V-CP1, P §4.4 and E-2, ADAPTER §5.3 and XF-25: on a direct application the act "is still requested" and the disposition "stays *act not performed*".
   - C FXA-5: `CP-accept` is reached-when kind (c) *queued*; on a direct application nothing queues. ADAPTER §7.7: dispositions are waiting · performed · resolved negatively · lapsed · not reached · unknown.
   - Options: (a) *act not performed* is *not reached* and the request is made without an arrival; (b) the direct application counts as the arrival and the disposition is *waiting*; (c) a new record label. I used R9-2's words and chose none. This belongs with EXEC in Wave B.
3. **Which act fields a read result carries.**
   - C §6.2: "at least" eleven fields. RS §6.1: sixteen elements, including act identity, act class, governing policy reference, relations and order. SoW CLM-002: C "consumes the DEL-04-03 act field set".
   - Options: (a) the whole RS §6.1 set; (b) C's subset stands. C now names the difference and decides nothing.
4. **ADAPTER §11 "Expect from DEL-09-06/RELAY" against the registers.**
   - ADAPTER §11 lists RELAY as an expected input. No register row exists in either direction, and DAG-003 HANDOFF names DEL-03-03 → DEL-09-06 as reverse arc K-11 (SCC-002 grows to 14).
   - Options: (a) reword as citation only; (b) register it, which is an SCC-forming departure for the owner. The row is annotated; the text is kept.
5. **A host read without workspace identity or generation** (survey 3.6; also Wave B item ADAPTER 8).
   - C §5.2 rule 1: "A read lacking any element is *basis incomplete* and cannot be cited". ADAPTER RD-2: a whole-model-identity read "satisfies RD-2 and can be cited (R8-12 item 6)", and records that SWBPIPE main has no workspace identity or generation.
   - R8-12 item 6 decides the subject-identity part only. Options: (a) such a read is *basis incomplete*; (b) it is citable with the missing elements recorded *not supplied*.

## 4. Proposed ScopeOfWork, register and basis items (none made)

**Registers**

1. DEL-03-01: add the supplier-side DOWNSTREAM mirrors (C1-B M-01-1…M-01-8) for DEL-02-01, DEL-02-03, DEL-03-03, DEL-03-04, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-09-06, DEL-09-09, DEL-10-03; retire or retarget package-level DEP-03-01-022.
2. DEL-03-02: add the DOWNSTREAM mirror of DEP-03-01-026 (M-02-1) and mirrors to DEL-05-01, DEL-05-02, DEL-02-01 (N-18), DEL-02-03 (N-21), DEL-09-06, DEL-10-03; settle the SatisfactionStatus TBD/PENDING convention.
3. DEL-03-03: add the DOWNSTREAM mirror to DEL-03-04 (M-03-1) and mirrors to DEL-02-03 (N-24), DEL-04-03, DEL-09-06; reconcile DEP-03-03-008 (TBD) with DEP-04-01-023 (INITIALIZED).
4. DEL-03-02 and DEL-03-03 have no UPSTREAM row for DEL-04-02's visible autonomy state (supplier rows DEP-04-02-021, -022 only); DEL-03-03 has none for DEL-02-01's checkpoint constraints (supplier row DEP-02-01-027 only).

**ScopeOfWork**

5. DEL-03-03 VER-002 still says "Confirm no host call while disabled"; AC-002 now says "no App-originated host request". Align VER-002.
6. DEL-03-02 and DEL-03-03: a "consumes DEL-04-02's visible autonomy state" sentence, if the owner wants arcs N-05/N-07 grounded on the consumer side (V12 F6, advice); DEL-03-03 likewise for DEL-02-01's declared constraints (governance phase).
7. DEL-03-01: OUT-001 and DEP-05-01-014 both ask for "schemas". If the first increment stays at semantic meanings, say so in the SoW or the register row; otherwise Wave B item C 6 must produce the schema form.

**Basis**

8. None needed by these three files. Observation only: HOST_INTEGRATION V4-HI-02 lists eight entry fields; the revised DEL-03-01 REQ-002 adds per-surface exposure, and four consumers rely on a *catalog edition* that neither text names.

## 5. Wave B items found beyond the survey's, and notes for other nodes

1. **Observing the agent's request on X.** R9-1 has the product record "the request where it can be identified". ADAPTER §7.7 now points to EXEC for this. Nothing says which native item or message identifies a request on the external channel.
2. **A fixture case for a direct application at a declared checkpoint in the current phase.** V-CP1's Phase-1 result covers it only as "if made". No VC row in C, P or ADAPTER exercises the R9-2 outcome; P E-2 has one sentence.
3. **C §6.2 against RS §6.1** (R10 candidate 3): the act fields a read result must carry.
4. **VC-P-14** is now partly observed (the tool run). The one-for-one review of REQ-013 against P §1 and §13 remains to be run.
5. **ADAPTER §11 "Provide to DEL-01-01 (by join; no register row)".** A DEL-01-01 row consuming DEL-03-03 would be one of the reverse rows DAG-003 HANDOFF guards against (K-3…K-5 merge three SCCs). The Design statement is left as it is.
6. **Pre-existing table defects, not touched:** C has three change-table rows with two cells in a three-column table ("V9 N-2", "R8-13 close", "V10 S-1…S-4"); ADAPTER has one. Cosmetic.

Notes for other nodes (no edit by me):

- **A1-C (WD, EXEC):** WD §4.3.7's table row for an item leaving lists three causes ("stale refusal, A11 withdrawal, host refusal"; grep, L711). P's fifth cause, "cleared by the person with no decision record" (R8-5; P §4.3), appears there only in the SWBPIPE note below the table. The survey (2.6, 3.6) says EXEC §9.1 records "P-v0.4 read" and "ADAPTER-v0.2 read"; I did not re-check that, because EXEC was under edit by A1-C. P is now P-v0.7 and ADAPTER is ADAPTER-v0.5; their sections and identifiers are unchanged.
- **A1-A (ACT, RS):** the consequence vocabulary (ACT U-02; C6/A27) is still empty in C §3.1. RS §10 says DEL-03-02 "Consumes §5 evidence rules" and DEL-03-03 "Consumes R5 destination; R7 external entries; R9; R11; R13"; P §13 has no "Expect from DEL-04-03" row, and ADAPTER now states supply only (N-12 and N-B8 not proposed, DECISION-6). RS R11's phase tag on "constraint not carriable" is R10 candidate 1.
- **A1-G (GUIDE):** the three hashes above replace GUIDE-v0.3's input pins for C, P and ADAPTER.

## 6. Header pin tables as they now stand

"Recomputed" means `shasum -a 256` on the working tree, 2026-09-30, compared with the value written. "History" means the file labels the pin as an earlier state and I did not re-pin it.

### 6.1 Pins common to the three headers

| Pin | Value written | Check |
|---|---|---|
| `docs/PRD.md` | `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` | Recomputed: equal |
| `docs/ARCHITECTURE.md` | `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c` | Recomputed: equal |
| `docs/HOST_INTEGRATION.md` | `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` | Recomputed: equal |
| `docs/EXAMINATION.md` | `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` | Recomputed: equal |
| "as amended by SCA-V4-001 and SCA-V4-002 (HOST_INTEGRATION line layout only)" | — | `git log` on the four docs: all four changed at `230bf1e646` and `a0af39f8cc` (SCA-V4-001); only HOST_INTEGRATION at `70376aff2f` (SCA-V4-002) |
| `_DAG/_LATEST.md` → DAG-003 | label | Read: "Latest: DAG-003", accepted 2026-09-29 |
| SCC-CASE-002 `Case_Datasheet.md` | `a12abfaf82c34ae1e7c10d8b553d3e1a0da4772b160e02257c0bf70edce04d5c`, "additions only" | Recomputed: equal. `git diff --numstat 94aa9181b HEAD`: 54 added, 0 deleted. Rows M1-C, M1-P, M2-A, M3-CP, M4-X present (grep) |
| First-increment `OWNER_DECISIONS.md` | `a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c` | Recomputed: equal. `f3f8e5f3…` was the state at `be8bb46dd3` (`git show`) |
| R1…R5 (abbreviated, unchanged) | `2f9c7e72…7ec4`, `77cfb845…d088`, `202d52c7…afbf`, `50a009b2…2a24`, `254d0b93…d6f1` | Recomputed: prefix and suffix equal |
| R6, R7 | `8703e85a…b841`, `1f6ab3b2…a1ea` (written in full) | Recomputed: equal |
| R8 | `44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b` | Recomputed: equal |
| R9 | `c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c` | Recomputed at the start and at the end of the work: equal |
| This run's `BRIEFS.md` | `698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a` | Recomputed at start and end: equal |
| `SURVEY/S1-B.md` | `eae76ecf9e941bb841fbc3a655a8e887c7684b8d47ef7728f4809992b0b6587d` | Recomputed: equal |
| SCA-V4-001 `OWNER_ITEMS.md` | `2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef` | Recomputed: equal; it is the revision DECISION-7 names (`2b90eb4a…`) |
| BASIS-ALIGN `OWNER_DECISIONS.md` | `ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b` | Recomputed: equal |
| `RELAY_ANSWERS_SWBPIPE.md` | `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74`, "three lines differ" from `6f01add3…` | Recomputed: equal. `git diff --numstat 94aa9181b HEAD`: 3 / 3 |
| `FACTS_SQ01_SQ32.md` | `733fb88a701317be8f0054937eca058774ba5f5f30c7a27233718996e8b2ab7e` | Recomputed: equal |
| Siblings | Labels only: EXEC-v0.5, WD-v0.7, WD-EX-v0.7, C-v0.7, P-v0.7, ADAPTER-v0.5, GUIDE-v0.4, ACT-POLICY-v0.7, AS-v0.7, RS-v0.7, LOOP-v0.7, PANEL-v0.7, HOSTING-BOUNDARY-v0.7, PIN-SPIKE-v0.1, CA-v0.5, XT-v0.5, RELAY-v0.3 | From the R9-11 table. **Not checked against bytes:** the other nodes edit in parallel. The headers say so, and name the versions actually read (RS-v0.6, ACT-v0.6, AS-v0.6) |
| R8-13 pass: R8 `44bc9a8d…` at `1528a5033`; intake OWNER_DECISIONS `5fd780bf…` "in its later state" | History | `git show`: R8 is `44bc9a8d…` at `1528a50334`; OWNER_DECISIONS is `9903bfe0…` there and `5fd780bf…` at `3733b14218` |
| Earlier-pass pins (R8 `d4c34233…`, `1770c96e…`; intake OWNER_DECISIONS `a5ccab0d…`; intake BRIEFS `3e33ba26…`; INTAKE_MAP; RELAY_ANSWERS `6f01add3…`; EXEC/WD/WD-EX byte pins at `94aa9181b`; all v0.1–v0.5 sibling pins) | History | Not re-pinned. The survey checked them true at their commits; I re-checked RELAY_ANSWERS (`6f01add3…` at `94aa9181b` and `7a1508452`) |

### 6.2 Pins specific to each header

| File | Pin | Value written | Check |
|---|---|---|---|
| C | Predecessor C-v0.6 | `8282c003024e54708f3b9842e04b6b0dc8c4e1c496027afae582eb6387675ce4`, last changed `caa4334ca1`, unchanged at `3dd7c22c73` | `git log` on the file; `git show HEAD:` hash equal |
| C | Predecessor C-v0.5 | `72ac4f0f…eacf` | History |
| C | `ScopeOfWork.md` | `9ada531b59a6efc007c273f131a8d51df390994ef5f379b1d523d635d3849449`; AX-004 list | Recomputed: equal. AX-004 read: OUT-001, CLM-002, REQ-002, REQ-004, VER-004, TBD-001 |
| C | v0.6 pins in the history clause | repo `6e18505e3`; SoW `179a6d35…`; HOST_INTEGRATION `08c8fc7d…`; Case_Datasheet `6acdc6c4…` | `git show 6e18505e3:` each: equal |
| P | Predecessor P-v0.6 | `410fb289e16177e11190db45be37e02b5d82ebf7a9fcff8676e938bb23a51af9`, last changed `f5ceef164a`, unchanged at `3dd7c22c73` | `git log`; `git show HEAD:` equal |
| P | Predecessor P-v0.5 | `6ab94fd1…37e0` | History |
| P | `ScopeOfWork.md` | `3560915142ebfbf3fa7197008ea3b0660584665c9d86260b22b550c5c2354d0f`; AX-004 list | Recomputed: equal. AX-004 read: OUT-001, CLM-003, REQ-004, REQ-008, REQ-012, AC-009, AC-013, TBD-001 |
| P | Intake `OWNER_DECISIONS.md` (current) | `5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2` | Recomputed: equal |
| P | v0.6 pins in the history clause | SoW `42328987…` and the others as C | `git show 6e18505e3:` SoW: equal |
| ADAPTER | Predecessor ADAPTER-v0.4 | `6e13ab117271b12512f64aab82e99839d1884abb4a43481f7382b67faf253043`, last changed `caa4334ca1`, unchanged at `3dd7c22c73` | `git log`; `git show HEAD:` equal |
| ADAPTER | Predecessors v0.3, v0.2, v0.1 | as before | History |
| ADAPTER | `ScopeOfWork.md` | `93faf918ce5d2d4eb14f0ecd1b20831a164a8c55a8b47cad26880818251b1a93`; AX-004 and AX-005 lists | Recomputed: equal. AX-004 and AX-005 read |
| ADAPTER | "Earlier basis pins" (SoW `5ac5db97…`; HOST_INTEGRATION `08c8fc7d…`; PRD `657593ce…`; ARCHITECTURE `c3ae766e…`; EXAMINATION `1b156553…`; Case_Datasheet `6acdc6c4…`) | History, "each true at `6e18505e3`" | `git show 6e18505e3:` each: equal |
| ADAPTER | First-increment BRIEFS `58de4a2c…` | History, "true at `1c36b6d975`" | `git show 1c36b6d975:`: equal |
| ADAPTER | RELAY-v0.3 former byte pin `89b6b9c9…8bdd7` at `816c917f0` (§12) | History; now cited by label | Not recomputed (RELAY is A1-E's file). V9 records the §0–§3 span hash as unchanged |
| ADAPTER | PIN-SPIKE-v0.1 `0e090a4c…b115`; generated bundles `aa5cb3fb…`, `34f28a48…` | Unchanged lines | Survey found them current; PIN-SPIKE recomputed: `0e090a4c…` |
| ADAPTER | PR #885 head `12907f393f5e…` | Unchanged | Not checked (no network) |

Quoted requirement texts, each compared with the current source (whitespace-normalized, exact): PRD V4-HOST-02 (C §4.1, ADAPTER §3.4); HOST_INTEGRATION V4-HI-42 clause and heading sentence (P S-P13, ADAPTER S-X10); the R9-1 summary (C §0, P §0); DEL-03-01 REQ-002, two phrases (C §3, §3.1); DEL-03-03 AC-002, VER-002, VER-003 and the REQ-003 sentence (ADAPTER E-2, F-13). ADAPTER F-13 and F-14 still show the pre-amendment VER-003 and REQ-002 wording; each now carries a closing note that says so.
