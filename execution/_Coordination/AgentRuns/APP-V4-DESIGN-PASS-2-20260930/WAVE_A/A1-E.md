# A1-E — alignment wave return: DEL-09-06 (CA, RELAY), DEL-09-09 (XT)

- **Run / node:** APP-V4-DESIGN-PASS-2-20260930, node A1-E. One Type 2 TASK executor (Claude Code subagent; parent HELP_HUMAN). No delegation. Read-only git; no network.
- **Date:** 2026-09-30. **Candidate:** working tree on `3dd7c22c73`, branch `claude/chirality-app-v4-60-percent-a41fd5`. The other Wave A executors were editing their files in the same tree while I worked.
- **Files written:** the three Design files below and this return file. Nothing else. `RELAY_ANSWERS_SWBPIPE.md` (`afb6e063…0e74`) and `FACTS_SQ01_SQ32.md` (`733fb88a…ab7e`) hash the same before and after. GUIDE, ScopeOfWork, registers, `_STATUS.md`, basis docs, `_Decomposition/`, `_ScopeChange/` and `_DAG/` were not touched.
- **Paths** are relative to `projects/chirality-app-v4/execution`.

| Short | File | Version | sha256 before | sha256 after |
|---|---|---|---|---|
| CA | DEL-09-06 `Design/CONNECTED_ACTIVITY_CONTRACT.md` | v0.4 → v0.5 | `1a7e2ac993e327bfd56c571c1016122baa846efa6ad378630bd3523ecbc4d421` | `6dfe1332b09f722a7d9c9fcca849ae8de58155414ff0b4252dd3f8ba20d21b2e` |
| RELAY | DEL-09-06 `Design/RELAY_QUESTIONS_SWBPIPE.md` | v0.3, metadata only | `c93f8cc52da81b5f16040dbaade7acd38fa676c2a81c86a32a7e12862c31056f` | `ce7c9e57814d784888fb1501b3ca1519d8d14a8dce4973ac03fd709483c95b3c` |
| XT | DEL-09-09 `Design/EXTERNAL_TRACE_CASES.md` | v0.4 → v0.5 | `fde79bb3170c450830cf0ca53bba8493328f2f89d47f14fed563f97dad3b2d92` | `65ec1656147191c6e66ae577a9ab3ec5f77a005461f6232c884d19006f20bfd0` |

All three computed with `shasum -a 256` after the last edit.

## 0. RELAY §0–§3: proof that the relayed body is unchanged

- **Span:** from the line that starts `## 0.` up to, and not including, the line that starts `## 4.`.
- **Extraction:** `awk '/^## 0\./{p=1} /^## 4\./{p=0} p' RELAY_QUESTIONS_SWBPIPE.md | shasum -a 256`.
- **Before editing:** `6e399c8389dc2ad991ba8b64084fee17d44ef9e8137d184dd8eb599a66340d4d` (1009 lines, 61806 bytes).
- **After editing:** `6e399c8389dc2ad991ba8b64084fee17d44ef9e8137d184dd8eb599a66340d4d` (1009 lines, 61806 bytes). `cmp` of the two extracted spans reports no difference.
- **Same span at `c6f81a4f2`** (the commit the ledger names as relayed), by `git show … | awk … | shasum`: the same value.
- `git diff -U0` on RELAY shows hunks only at old lines 2, 5, 6, 23 (header) and 1095–1136 (change table, count line, UNRESOLVED). The edit script also asserted the span hash before saving.

## 1. Changes made, per file

Method for every edit: exact-string replacement by script, each old string asserted to occur the expected number of times; a dry run on a scratch copy was diffed before the real file was written. No unaffected text was reflowed.

### 1.1 CA (34 changes)

| # | Item | Where | Change |
|---|---|---|---|
| 1 | R9-11 | Header, Contribution | CA-v0.5; supersedes CA-v0.4 with its sha256 and last commit; names this pass |
| 2 | R9-1, R9-3; survey A.8 items 2, 3 | Header, Phase line | The R9-1 summary of the amended V4-WF-05 and V4-HI-42, word for word, with "the current phase (Phase 1)" on first use. The requester (the agent; INTEGRATION, put to the owner). Observation mechanism left to EXEC in Wave B. The "first half … flagged for the next accepted-basis update" sentence is gone. Cites SoW REQ-003, AC-004, TBD-003 and DEP-09-06-034 |
| 3 | A.2 item 6 | Header, Serves | OUT-004 also names `RELAY_ANSWERS_SWBPIPE.md`, standing at *answered* (OUT-004 as revised) |
| 4 | R9-5; A.8 item 1 | Header, Basis and Consumed inputs | Basis line re-pinned (section 6 below). The v0.1–v0.4 basis line is kept verbatim as a history bullet. A "v0.5 inputs" bullet says how siblings were read |
| 5 | R9-5; A.1 row 20 | Header, answers line | Adds that SWBPIPE revised the answers to `afb6e063…` (#1048) and that RELAY §4 records no relied-on answer changed |
| 6 | R9-6; A.8 item 8 | Header, Receivers | Rebuilt from the registers: DEL-09-07 (DEP-09-07-011), DEL-03-04 (DEP-03-04-022, N-B10), SWBPIPE owner (DEP-09-06-033 for the relay; DEP-09-06-020 for the workflow). Five former "receivers" with no register row are kept as cross-references |
| 7 | R9-1, R9-2; A.8 item 3 | §1 S-5 | Rewritten: in force in every phase (request; record only when performed; reserved acts); phased (the hold); V4-HI-42's two clauses in force; who requests; R8-11 item 2 as restated by R9-2, with the owner's confirmation (OWNER_ITEMS O-25). "V4-HI-42 … plan guidance" and "second half" are gone |
| 8 | R9-4 | §1 S-12 | "The App records the destination per turn and shows it" is labelled SETTLED with OWNER_ITEMS O-10 (BASIS-ALIGN DECISION-7) and SoW TBD-003 (a); only the detail stays INTEGRATION (R4-1, R5-4) |
| 9 | R9-1; A.8 item 3 | §1 S-13 | Phase-1 part: cites the amended texts; the agent requests; the product's three parts (R9-1 (i)–(iii)); an observed arrival **is** recorded (was "may be recorded"), citing DEL-02-03 REQ-002; mechanism left to EXEC Wave B; D6 sentence cites SoW TBD-003 (b). Governance-phase part untouched |
| 10 | A.8 item 7 | §2.2 CA/E row and a new paragraph | Quotes the amended V4-HOST-02 and V4-HI-70 and names the owners of the rules (LOOP §5.1.1, PANEL §3.8, ACT §2.7, RS R15); says it governs host agents only and that no SQ asks it. Defines nothing |
| 11 | R9-1 | §2.2 Phase-1 paragraph | "The required act is requested by the agent carrying out the workflow"; observed arrivals "are recorded" |
| 12 | A.8 item 7 | §2.3 CA-0 evidence cell | On CA/E the run record also carries each network destination contacted (RS R15; V4-HI-70 as amended) |
| 13 | R9-2 | §2.3 CA-2 cell | I-7 cited "R8-11 item 2 as restated by R9-2" |
| 14 | R9-1; A.8 item 3 | §2.3 CA-H cell | The agent asks for each act; an observed arrival is recorded |
| 15 | R9-4 | §2.5 DI-5 | Same label change as S-12 |
| 16 | R9-2 | §3.1 WR-6 | The act is still requested; where the host applies directly "no A5 is forced and none is recorded" |
| 17 | R9-5, R9-11 | §5 | Lead sentence; twelve standing cells moved to the Wave A labels |
| 18 | R9-5 | §6 ST-0 | "v0.3/v0.4 and v0.2 definitions" → the sibling definitions at their current versions |
| 19 | R9-4; A.4 item 26 | §7.2 | Ladder cited to SoW OUT-004; the per-standing evidence stays PROPOSED (W9) |
| 20 | R9-1; A.8 item 2 | §8.1 | Phase reading adds the request and the SoW TBD-003 (b) sentence on W14-04 and W14-09 |
| 21 | R9-1, R9-2; A.8 item 3 | §8.2 W14-04 (i′), (ii′) | (i′): the agent asks for the A5; direct application forces and records no A5; R9-2's "*act not performed*". (ii′): the A4 is requested by the agent; cites V4-EXM-22 as amended |
| 22 | A.8 item 4 | §8.2 W14-05, -06, -07 "Built on" | CH-8 and CH-30 added to W14-06 (RT-11 lists them and W14-06's text already states their content). CH-9 and CH-20 left where they are, with a pointer to F-23 |
| 23 | A.8 item 7 | §8.2 W14-08 | Host side: run records on CA/E include destinations contacted |
| 24 | A.8 item 2 | §8.2 W14-09 | Phase note (SoW TBD-003 (b)) |
| 25 | R9-5 | §9 closing paragraph | Answers: delivered `6f01add3…`, revised to `afb6e063…` |
| 26 | A.2 (REQ-008 row) | §10 row 1 | "supplier observation" for DEL-01-01, as REQ-008 now reads |
| 27 | R9-5, R9-6; A.8 item 4 | §11.1 | Rebuilt with a register-row column. The `8fb51f07f` (v0.4/v0.2) labels are dropped. DEL-09-01's supplier-side row, the package rows, the person and DEP-09-06-034 are listed |
| 28 | R9-6; A.8 item 8 | §11.2 | Rebuilt: DEL-09-07, DEL-03-04 (new), SWBPIPE owner, the owner; "named by DEP-…; not yet defined here" for DEP-09-07-011's selection and DEP-09-06-020's workflow; cross-references in a separate table |
| 29 | R9-8; A.4 NOW items | §12.7 F-22 pointer; new §12.8 | F-2, F-3, F-8, F-17, F-22 closed with their records |
| 30 | R9-9 | new §12.9 | F-23 (RT-11 map), F-24 (register items) |
| 31 | R9-11 | new "Changes from v0.4" | Rows keyed by R9 item and survey item |
| 32 | R9-8; A.8 items 2, 8 | UNRESOLVED | The V4-WF-05 / SoW-wording row is closed (note beneath the table). D6 row cites TBD-003 (b). Host-joins row cites TBD-003 (c) and DEP-09-06-034 |
| 33 | R9-1 | VC-CA-04 | Design and expected result follow R9-1 |
| 34 | R9-5, R9-11 | §0–§11, UNRESOLVED, VC | 35 sibling labels moved: EXEC-v0.4 → v0.5, WD-v0.6 → v0.7, WD-EX-v0.6 → v0.7, C-v0.6 → v0.7. Origin labels such as "WD-v0.4's" are kept |

### 1.2 RELAY (8 changes; all outside §0–§3)

| # | Item | Where | Change |
|---|---|---|---|
| 1 | R9-10, R9-11 | Header, Contribution | Stays RELAY-v0.3; a note records this pass and the span hash |
| 2 | R9-5; survey B.8 item 1 | Header, Basis | Re-pinned (section 6). States that §0–§3 keep the wording they were relayed with and that the superseded premises are next-relay items |
| 3 | R9-5 | Header, Consumed inputs | A Wave A bullet with the current sibling labels; the earlier basis line kept verbatim as history |
| 4 | R9-6; B.2 | Header, Receivers | The relay handover is DEP-09-06-033 (it was cited as -018/-019/-020); DEL-03-04 added (DEP-03-04-022) |
| 5 | R9-11 | "Changes from v0.2" | Three rows for this pass |
| 6 | R9-8 (V6 m-3); B.8 item 2 | Count line | Composition stated: nine sub-questions, eight by R5-10 and SQ-02 (f) by R7-2. See section 2: I did not write "ten" |
| 7 | B.8 items 2, 3 | UNRESOLVED | The HANDOFF-pointer row is replaced by the next-relay row (DECISION-5 host obligations; superseded premises of SQ-02, SQ-16, SQ-30; caller naming; per-batch completion) |
| 8 | B.8 item 2 | UNRESOLVED, note | "Closed at the Wave A alignment pass", citing HANDOFF `76edf236…` sections |

### 1.3 XT (21 changes)

| # | Item | Where | Change |
|---|---|---|---|
| 1 | R9-11 | Header, Contribution | XT-v0.5; supersedes XT-v0.4 with its sha256 |
| 2 | R9-1, R9-3; survey C.8 items 2, 3 | Header, Phase line | R9-1 summary; requester; XC-10's parts per SoW TBD-005; DEP-09-09-024 |
| 3 | R9-5; C.8 item 1 | Header, Basis and Consumed inputs | Re-pinned (section 6); old line kept as history; "v0.5 inputs" bullet |
| 4 | R9-5 | Header, answers line | Revision to `afb6e063…` noted |
| 5 | R9-6; C.8 item 7 (Receivers part) | Header, Receivers | DEL-03-01 (DEP-03-01-030), DEL-03-04 (new; DEP-03-04-023), owner with host contract owner (DEP-09-09-020); four former "receivers" kept as cross-references |
| 6 | R9-4 | §1 S-9 | SETTLED with OWNER_ITEMS O-10 and SoW TBD-005; detail stays INTEGRATION |
| 7 | R9-1, R9-2; C.8 item 3 | §1 S-10 | Request clause and record clause in force; the agent requests; observed arrival recorded; "WD I-7 and V4-HI-42 are guidance" replaced by the R9-2 restatement with the O-25 citation; citation cell extended |
| 8 | R9-5, R9-6 | §2 IN-03…IN-08 | Wave A labels and register rows DEP-09-09-007…012 |
| 9 | R9-4 | §2 IN-14 | Same label change as S-9 |
| 10 | C.8 item 2 | §2 IN-22 | "Not registered" removed; DEP-09-09-021 |
| 11 | C.8 item 2 | §2 IN-25 | DEP-09-09-023 |
| 12 | C.8 item 2 | §2 IN-29 | "not registered" removed; DEP-09-09-022 |
| 13 | R9-1, R9-2 | §3.2 XC-10 | Phase-1 sentence: the act is requested by the agent and recorded only when performed; direct application forces and records no A5 |
| 14 | C.8 item 2 | §3.3 Gate | Cites SoW TBD-005 |
| 15 | C.8 item 2 | §7 | Three rows for the owners REQ-009 now names (DEL-05-01, DEL-04-02, DEL-02-03); the SWBPIPE row notes CLM-004's "coordination route" |
| 16 | R9-8; C.4 NOW items | new §9.8 | F-1, F-2, F-6, F-17 closed with their records |
| 17 | R9-6 | new §9.9 | F-23 (receivers without rows), F-24 (the §5.1 ↔ C §8 tie is Wave B) |
| 18 | R9-11 | new "Changes from v0.4" | Rows keyed by R9 item and survey item |
| 19 | C.8 item 6; item 2 | UNRESOLVED | New F-18 row (owner: the integrator when host joins resume; the act facility is SWBPIPE's). A13 row and host-joins row cite TBD-005 and DEP-09-09-024 |
| 20 | C.8 item 2 | VC-T-01 | DEP-09-09-007…024 |
| 21 | R9-5, R9-11 | §0–§8, UNRESOLVED | 8 sibling labels moved: EXEC-v0.4 → v0.5, C-v0.6 → v0.7 |

### 1.4 The four required greps, after editing

| Phrase | CA | RELAY | XT |
|---|---|---|---|
| "flagged for the next accepted-basis update" | 1 hit, l.721: the v0.5 change row that says the marker was dropped | 0 | 0 |
| "first half" | l.693 (F-22, the v0.4 finding; history, now ending "**Closed at v0.5 (§12.8)**"); l.721 (the same v0.5 change row); l.741 ("Changes from v0.3", R8-1 row; history) | 0 | 0 |
| "second half" | l.721 only (the same v0.5 change row) | 0 | 0 |
| "override autonomy" | 0 ("R8 overrides I2" at l.11 and l.737 is a different sentence) | 0 | 0 |

No active statement in §0–§11, UNRESOLVED or the verification cases carries any of the four. History rows were left as true records (R9-5).

## 2. Survey items not applied, and where I disagree with the survey

| Item | Reason |
|---|---|
| CA 5 (failure column; W14 result record), CA 6 (§2.4 as a Phase-1 sequence), CA 9 (OI-021 option sheet) | Wave B; not in the A1-E row |
| XT 5 (run order, set-up and reset, reopen table); XT 7 first part (tie §5.1 to C §8) | Wave B. The second is recorded as XT F-24 |
| RELAY 2, the count "ten" (V6 m-3; R9-8) | **Disagreement, checked against the source.** I compared the lettered sub-questions of §2 at `9fc77baa3` (RELAY-v0.2) with the current text: nine were added (SQ-03 (e); SQ-05 (g), (h), (i); SQ-07 (g), (h); SQ-18 (e); SQ-19 (d); SQ-02 (f)). V6 m-3 counts the nine V3-B items as nine sub-questions; one of them, WD U-10, is in "Not included". The line already said "nine". I added its composition instead of changing it to a wrong number, and recorded this in the change table |
| Survey A.6, "RS §10 states only R2 transfer links" | True of RS-v0.6. RS-v0.7, written in parallel by A1-A, now names the act records and the run record for DEL-09-06. I removed the finding I had drafted and CA §11.1 states the current position |
| Survey A.2, "SOW-236, -237, -240, -241 are named only in VC-CA-01" | Not a section 8 item; left. Listed in section 5 |
| Survey A.8 item 3, "must come after the EXEC node" | Not waited for, as instructed; the R9-1 text was used. EXEC-v0.5's PH-6, read at the end, says the same ("required, not optional (R9-1)") |
| Survey E.1 (HANDOFF) | Outside my write fence; see section 4 |
| Survey B.5 (VC-R-06 has no run record) | Not recorded as run: no reviewer ran it |

## 3. R10 candidates (R9-9): both texts left in place

**R10-E1. Which W14 case do EXEC CH-9 and CH-20 rehearse?**

- CA §8.2: W14-05 "Built on" — "EXEC CH-2, CH-20, CH-23, CH-28, CAP-6 …"; W14-07 — "EXEC CH-3, CH-4, CH-5, CH-9, CH-21, RP-1…RP-8, §4.9".
- EXEC RT-11 (unchanged in EXEC-v0.5): "W14-05 ← CH-2, CH-23, CH-28; W14-06 ← CH-6…CH-10, CH-30; W14-07 ← CH-3…CH-5, CH-21".
- CH-9 is "Run ended while waiting; post-end act; continuation"; CH-20 is "Prior act not counted". W14-05's text uses "prior act not counted"; W14-07's text uses "an ended run is never resumed … *continues ⟨run⟩*".
- Options: (a) RT-11 follows CA (CH-20 under W14-05; CH-9 under W14-07, range written CH-6…CH-8, CH-10); (b) CA follows RT-11 (CH-9 under W14-06; CH-20 dropped from W14-05 or moved); (c) CH-9 cited under both, since W14-06 also has an "after run end" clause.
- Recorded in CA §12.9 F-23.

**R10-E2. R9-2's "*act not performed*" against WD's disposition vocabulary.**

- R9-2: "the checkpoint's disposition stays *act not performed* unless the person performs it." CA W14-04 (i′) quotes it.
- WD §4.3.4 lists six dispositions: not reached, waiting, performed, resolved negatively, lapsed, unknown. *waiting* is "Phase 1: a record label, 'reached; act not yet recorded'".
- Options: (a) "act not performed" is read as WD's *waiting*; (b) it is added to the shared vocabulary by WD and EXEC; (c) it is a plain-language phrase and files should use the WD word.
- Owners: WD and EXEC. CA only quotes the ruling.

**R10-E3 (minor). What WD supplies to DEL-09-06 as examples.**

- WD-v0.7 §8, DEL-09-06 row: "EXAMPLES E1, E3".
- CA §3.2, §11.1 and header: E1, E1c, E1d, E8; W14-10 also cites WD-EX E4.
- DEP-09-06-025 names "portable declaration, identity and revision meaning" and no example.
- Options: (a) WD's row lists what CA cites; (b) the row is read as not exhaustive.

## 4. Proposed ScopeOfWork, register, basis and coordination items (none made)

1. **DEL-09-09 SoW REQ-001** says "Carry unresolved details at TBD-001 through TBD-004". TBD-005 was added by SCA-V4-001. Propose "through TBD-005".
2. **DEL-03-04 register, DEP-03-04-022** names only the relay questions and recorded answers. GUIDE also cites CA §2.2–§2.5, §4, §6, §7 and §8. Propose widening the statement, or a note that CA is consumed.
3. **DEL-09-06 register, mirror maturity:** DEP-09-06-015 says TBD and DEP-04-03-031 says INITIALIZED (already an open matter in DAG-003 HANDOFF_STATE).
4. **DEL-09-06 register:** the old Receivers line cited DEP-09-06-020 for the relay; the relay row is -033. No register change needed; both Design files now cite -033.
5. **Former receivers with no register row.** CA: DEL-09-09, DEL-02-03, DEL-05-01, DEL-05-02, DEL-04-03. XT: DEL-09-06, DEL-03-03, DEL-09-01. I kept them as cross-references. DAG-003 HANDOFF_STATE says a row making any of the CA five consume DEL-09-06 is an SCC-forming departure (E-1 for DEL-09-09). Proposal: confirm they stay unregistered.
6. **DEL-09-07 register, DEP-09-07-011** names "the selected useful operation, permitted autonomy and exact candidate environment". CA cannot supply it before OI-021. No change proposed; it is an owner decision (OI-021).
7. **DEL-09-06 SoW and the amended V4-HI-70 / V4-HOST-02.** No REQ or AC says whether the connected activity on CA/E must evidence host-agent network destinations. CA now points to the owners and defines nothing. If the joined witness should observe it, the SoW needs a sentence; otherwise it stays with DEL-09-07 (V4-EXM-23).
8. **`_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`** (not in any write fence): l.22 still says "local-first host operation"; l.40 says "DAG-001 is accepted" (`_DAG/_LATEST.md` reads DAG-003); the note for SWBPIPE does not mention DECISION-4 D4-3 or DECISION-5. For its editor.
9. **A successor relay.** RELAY's UNRESOLVED now lists four items it must carry. Drafting and relaying it is an owner choice and was not selected for this run.
10. **Label consistency across files.** RS-v0.7 and my two files cite OWNER_ITEMS O-10 for "record and show the destination per turn". A grep at the end still finds "DECISION-2 reading" in HOSTING, C, EXEC, AS, ACT, ADAPTER and LOOP (some of it history). For the integrator's check under R9-4.

## 5. Wave B items found beyond the survey's

1. **The request has no observable in CA or XT.** R9-1 adds "the request where it can be identified" to the record. W14-04, W14-05, CA-H and XC-10 name no evidence for it. They need EXEC's Wave B definition first, and on X also ADAPTER §7.7's observations (arc N-24).
2. **CA §2.4** still prints "[CP-accept arrives: waiting]" and "waits for A4" with a reading note after it (survey item 6). After R9-1 the sequence should also show who asks.
3. **CA/E destinations have no case.** CA now cites RS R15 in CA-0 and W14-08, but no W14 case observes a destination record, grant or decline, and no SQ asks SWBPIPE for it.
4. **CA AC-001 trace.** SOW-236, -237, -240 and -241 are named only in VC-CA-01; no body section is traced to them (survey A.2).
5. **CA §11.2, "not yet defined here" rows.** DEP-09-07-011 (the selection) and DEP-09-06-020 (the reviewed workflow) name contributions CA does not contain. The first waits for OI-021, the second for DEL-02-02 and `create-workflow`.
6. **XT IN-25** mixes phase text into its Supplier cell; a tidy-up when §2 is next developed.
7. **XT F-18** now has an owner and point of need but no option text for how §3.3 would read for a per-batch host.
8. **Depth of the citation check.** My check shows that every cited sibling section and identifier exists in the owner named. It does not compare content line by line. A reviewer should sample the §2.3 step map against the v0.7 and v0.5 texts once they are final.

## 6. Header pin tables as they now stand

"Recomputed" means `shasum -a 256` on the working-tree file at the end of the pass; a script then extracted every 64-hex string from each file's Basis line and "v0.5 / Wave A inputs" bullet and matched it to that recomputation (CA 28 of 28, XT 28 of 28, RELAY 21 of 21; no miss). Quoted requirement texts were compared with the current source after whitespace normalization (40 quotes, all found).

### 6.1 Pins common to CA and XT (RELAY carries the subset marked R)

| Pin | Value | How checked |
|---|---|---|
| `docs/PRD.md` (R) | `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` | recomputed; V4-WF-05, V4-HOST-01, V4-HOST-02 texts grepped |
| `docs/HOST_INTEGRATION.md` (R) | `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` | recomputed; V4-HI-42, V4-HI-70 texts grepped |
| `docs/EXAMINATION.md` (R) | `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` | recomputed; V4-EXM-14, V4-EXM-22 texts grepped |
| `docs/ARCHITECTURE.md` (R) | `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c` | recomputed; V4-ARC-10 present |
| Amendments named | SCA-V4-001 (`_ScopeChange/SCA-V4-001_2026-09-28_2155/`), SCA-V4-002 (`_ScopeChange/SCA-V4-002_2026-09-29_1901/`) | folders listed; `_ScopeChange/_LATEST.md` read |
| `_DAG/_LATEST.md` → DAG-003 (R) | `4d381ba4e87b41a83b9d0d2dc591c4bf04eacb84df0b5c27314091cd2a992f56` | recomputed; file reads "Latest: DAG-003"; HANDOFF_STATE.md read whole |
| First-run OWNER_DECISIONS (R) | `a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c` | recomputed |
| Intake OWNER_DECISIONS (R) | `5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2` | recomputed; DECISION-5 and its confirmation read |
| BASIS-ALIGN and SCA002 OWNER_DECISIONS | `ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b`; `36ffcbbea923504581844456751c2eb3db617b5471a3595e63f036bf0634b480` | recomputed; DECISION-7 read |
| SCA-V4-001 OWNER_ITEMS.md | `2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef` | recomputed; O-10 and O-25 read; the prefix matches the one DECISION-7 names |
| This run's OWNER_DECISIONS | `0730c6f3d174a8acddbd0c9fabb62afd4d6444847a612f0de7ff3ba584303722` | recomputed |
| R1, R2, R3, R4 (R) | `2f9c7e72…7ec4`; `77cfb845…d088`; `202d52c7…5afbf`; `50a009b2…2a24` | recomputed; equal to the v0.4 pins |
| R5, R6, R7 (R) | `254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1`; `8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841`; `1f6ab3b2355e164f803657ceae08841af92d21a821feede3800a6df861b2a1ea` | recomputed |
| R8_RESOLUTIONS.md (R) | `44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b` | recomputed; R8-11, R8-12, R8-13 read |
| INTAKE_MAP.md | `3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33` | recomputed |
| R9_RESOLUTIONS.md (R) | `c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c` | recomputed at the start and at the end (unchanged) |
| This run's BRIEFS.md; SURVEY/S1-E.md | `698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a`; `e0e9552242f567789e44a93cdf381a1a474a6acf1d8078cbad5e247ae049d6f9` | recomputed at the start and at the end |
| `RELAY_ANSWERS_SWBPIPE.md` (R) | `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74` | recomputed before and after; not edited |
| `FACTS_SQ01_SQ32.md` (R) | `733fb88a701317be8f0054937eca058774ba5f5f30c7a27233718996e8b2ab7e` | recomputed before and after; not edited |
| Sibling Design files (R) | labels only: EXEC-v0.5; WD-v0.7; WD-EX-v0.7; C-v0.7; P-v0.7; ADAPTER-v0.5; GUIDE-v0.4; ACT-POLICY-v0.7; AS-v0.7; RS-v0.7; LOOP-v0.7; PANEL-v0.7; HOSTING-BOUNDARY-v0.7; PIN-SPIKE-v0.1 | no bytes pinned (R9-5). At my last read every sibling header carried its Wave A label; GUIDE is still v0.3, by design (A1-G runs after integration) |

### 6.2 CA only

| Pin | Value | How checked |
|---|---|---|
| DEL-09-06 ScopeOfWork.md (R) | `287d47a1260e7433c3f16578c67345d067472165421c65848bd15e44d92a7923` | recomputed; read whole; AX-004's revised list copied from it |
| DEL-09-06 Dependencies.csv (R) | `0f8ecad83cca72f7c65786ff0cd0252a2b7664c145a6e39193cff332a639f2f6`; ACTIVE EXECUTION rows DEP-09-06-012…034 | recomputed; every row read by script |
| `HANDOFF_SWBPIPE_DOMAINS.md` (R) | `76edf2361f392a7eb516abb10bf0a91e59f3802388e95b0e4685009f9e0aa405` | recomputed; read whole |
| Predecessor CA-v0.4 | `1a7e2ac993e327bfd56c571c1016122baa846efa6ad378630bd3523ecbc4d421` at `f5ceef164` | recomputed before editing; `git log -1` |

### 6.3 XT only

| Pin | Value | How checked |
|---|---|---|
| DEL-09-09 ScopeOfWork.md | `e887a579f75335aa91b59ae195053eabae81ce031fe91136df5c81df2297e53a` | recomputed; claims, requirements, TBDs and AX items read; AX-005's list copied from it |
| DEL-09-09 Dependencies.csv | `e0e3297adb7350c58694aae88062d1bb35778c4440a5e91374f3d8c7c9663bb8`; ACTIVE EXECUTION rows DEP-09-09-007…024 | recomputed; every row read by script |
| SCC-CASE-002 `Case_Datasheet.md` | `a12abfaf82c34ae1e7c10d8b553d3e1a0da4772b160e02257c0bf70edce04d5c`; rows M2-A, M4-J, M4-X | recomputed; each label found once |
| DAG-003 layer statement | arcs to DEL-04-01 and DEL-09-01 admitted; seven arcs to first-increment deliverables held in SCC-002 | `DependencyEdges.csv` and `CandidateEdges.csv` read by script |
| Predecessor XT-v0.4 | `fde79bb3170c450830cf0ca53bba8493328f2f89d47f14fed563f97dad3b2d92` at `f5ceef164` | recomputed before editing; `git log -1` |

### 6.4 Sibling citation check (CA item 4; XT item 4)

| File | Region | Sibling section citations | Distinct owner/section pairs | Distinct sibling-owned identifiers | Not found |
|---|---|---:|---:|---:|---:|
| CA | §0–§11, UNRESOLVED, VC | 139, plus 5 in §5's standing cells checked by hand | 91 | 157 | 0 |
| XT | §0–§8, UNRESOLVED, VC | 47, plus 2 in IN-07's cell checked by hand | 34 | 77 | 0 |

Run twice: before editing against the v0.6/v0.4 sibling text, and at the end against the text the other executors had written by then (every header at its Wave A label). Same result both times. Section numbers were not renumbered.

## 7. What I observed and what I inferred

- **Observed:** every hash, row, quoted text and count above, by the commands named.
- **Inferred:** that the sibling files will finish at the R9-11 labels with the section numbers and identifiers I cite. I checked their text as it stood; I did not see their final bytes.
- **Not done:** no case was run, no register or ScopeOfWork was edited, nothing was relayed, and no SWBPIPE join, witness or adoption is claimed.
