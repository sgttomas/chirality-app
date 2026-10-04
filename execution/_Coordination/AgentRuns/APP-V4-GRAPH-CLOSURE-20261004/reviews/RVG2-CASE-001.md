# RVG2 review of SCC-CASE-001 (SCC-001, DEL-01-01 ↔ DEL-01-05) — APP-V4-GRAPH-CLOSURE-20261004

- **Reviewer:** RVG2, a second standing independent reviewer. Type 2 TASK executor, Claude Opus 5.5 (`claude-opus-5-5`), dispatched by HELP_HUMAN on 2026-10-04. No delegation. I authored none of the subject or its Designs. Read-only git, no network.
- **Subject** (committed at `fdc713c439`, unchanged at HEAD `c5ca7ee0c9`), by the agent that analysed SCC-002 (not a design agent of either member):
  - `E/_DAG/cases/SCC-CASE-001/PAIR_ANALYSIS_2026-10-04.md`, sha256 `7f415cceee1bb1ce9ad29662b4b23a71ad36c221270bd55bf47c2e59e4005614`;
  - `E/_DAG/cases/SCC-CASE-001/MOVES_PROPOSED_2026-10-04.csv`, sha256 `33aa926053ee0fdcd3ff6bc15598b34a422a7ec9c8ef8cb5fbdedcbfff8c6fa7`.
- **Claims put by the coordinator:** M-01 moves no ownership (DEL-01-01 CLM-004 already assigns "configured-server substitution checks" to DEL-01-05); no E residual remains; and the stated interaction with G2's N08.
- **Basis read:** as in `RVG2-CASE-006.md`, plus SCC-CASE-002 §22–§23 (`139fd8ea…` at HEAD; §23 committed with this subject). GC-5 postdates the subject and is applied as current basis.
- **Sources checked:** DEL-01-01 `ScopeOfWork.md` (`bbc81a8d…`), `Dependencies.csv` (`5a5a60c5…`, equal to DAG-004's `SourceRegisterSHA256`), HOSTING-BOUNDARY-v0.9 (`5401f26d…`; §8, §8.1, §8.3, §11, VC-12, VC-26); DEL-01-05 `ScopeOfWork.md`, `Dependencies.csv`, ACCESS-v0.2 (l.63, l.910, §1 I-10, §13).
- **Scripts:** `$TMPDIR/rvg2/` (`g.py`, `g2.py`, `fast.py` with a bitmask DP for the 19-member components).

## 1. What holds

- **Rows and quotes.** DEP-01-01-024 and DEP-01-05-012 match DAG-004 (Direction, Type, maturity, satisfaction, Statement, EQ, SourceRef); mirrors DEP-01-01-022 and DEP-01-05-013 are as `ExcludedRows.csv` records. Every ScopeOfWork and ACCESS/HOSTING quote in §1.2–§1.3 and §3 occurs at source.
- **Kinds.** DEP-01-01-024 V/L and DEP-01-05-012 P follow G1 r3.
- **Ownership claim: holds.** DEL-01-01 CLM-004 reads "`DEL-01-05` (App account/provider integration owner) owns native sign-in, API-key and local-provider access and configured-server substitution checks" (verified), and REQ-007 excludes "`DEL-01-05` account/provider-access and server-substitution implementation". Withdrawing the VER-005 clause moves no ScopeOfWork-assigned ownership.
- **Withdrawal claim, for the plain withdrawal.** With the clause deleted, DEP-01-01-024's EQ no longer occurs; CLM-004 (also in its SourceRef) is an ownership statement whose consumption runs the other way. The row would be unseen and RETIRED. The "pointer" variant may be re-extracted, as §5 says.
- **Closure on DAG-004 (§2).** Reproduces: O-1 {01-01, 01-05} 1 row; O-2…O-4 none; acyclic with M-01 or M-02.
- **N08 table, against SCC-002 §22's group 1.** All four rows reproduce exactly from my code (19/23, 13/18, 13/18, 13/17; 14/21 …; 18 members / 9 rows; 13 / 7).
- **Owner acts.** M-02 (cut) is the owner's and only an alternative; M-01 goes through an SCA.

## 2. Findings

### C1-M1 — MAJOR. "No E residual" and "No HOSTING section or verification case uses sign-in or substitution evidence from DEL-01-05" are contradicted by HOSTING §8.3 and VC-26, which serves the very VER-005 being reworded

- **Evidence (HOSTING-BOUNDARY-v0.9).**
  - VC-26 "Model destination facts (R4-1)", verification column **VER-005**. Expected: "class taken from DEL-01-05's configuration". Status: "live start needs credential or local provider".
  - §8.3: the boundary supplies, per turn, "the provider and model the App **requested** (carried from the person's choice through DEL-01-05 …)", and "The destination **class** (local or cloud) is derived from the provider configuration the person chose (DEL-01-05) … DEL-01-05 derives it from the kind of access entry the conversation uses (ACCESS-v0.2 §2)".
  - §8's receiver table maps the whole DEL-01-05 relationship, including DEP-01-01-024, to "S-4; §8.1".
- **What remains after M-01.** DEL-01-01's VER-005 witness still needs DEL-01-05's sign-in (credential) or configured local server for its live part, and still takes the class from DEL-01-05's configuration. That is the clause's own content ("native sign-in and server-substitution evidence … when needed for the local qualification witness"). It remains a V need (VC-26 is a verification of VER-005; K-5) and, through §8.3's per-turn facts that HOSTING supplies to DEL-04-03, an E runtime flow (K-3: the format is the supplier pin's and RS R5's, not DEL-01-05's).
- **GC-5.** Item 1 makes this Design use a dependency (HOSTING's §8.3 output and VC-26 depend on DEL-01-05's values). Item 3 forbids leaving it in the Design while the ScopeOfWork clause and the row are withdrawn. The subject's step (i) "Design rewording. Not applicable" is therefore wrong: HOSTING §8.3 and VC-26 need rewording too (for example, the class attached by DEL-01-05 or DEL-04-03 rather than taken by HOSTING, and VC-26's live start run on DEL-01-01's own local-provider configuration, as OBS-1 was).
- **Computed.** Residual as V: O-1 still {01-01, 01-05}, 1 row. Residual as E: O-1, O-2 and O-3 each keep the 2-cycle; O-4 acyclic.
- **Consequence.** M-01 does not close SCC-001 under O-1 as stated, and it would leave an unregistered dependency that GC-5 does not allow. SCC-CASE-002 §23.3 ("SCC-001 has no E residual … Its closure table stands") rests on the same claim and falls with it.
- **Repair.** Either add the HOSTING §8.3 and VC-26 rewordings (named file, sections, DEL-01-01 design agent) and show that no V or E use remains, or record the residual and keep M-02 (owner cut) as the O-1 act, with E carried into O-2/O-3 if §8.3's flow stands.

### C1-M2 — MAJOR. The N08 interaction is stated against SCC-002's pre-§23 move set. With §23's E residuals, committed in the same commit, N08 merges DEL-01-05 into SCC-002's residual under O-2 and O-3

- **Evidence.** §3 reading 2: "Under O-2…O-4, SCC-002's group-1 moves cut every path from DEL-04-03 back to DEL-01-05, so N08 forms no cycle." The CSV row M-N08 repeats it. SCC-002 §23.2 (same commit `fdc713c439`) records that group 1 leaves a 5-member component {02-03, 03-03, 04-02, 04-03, 05-01} under O-2 and O-3. DEL-05-01 is in it, and the admitted DEP-05-01-026 (05-01 → 01-05, I) closes N08's path back.
- **Computed (G1 r3 kinds; group 1 with §23's five E residuals; N08 as I):**

  | Scenario | O-1 | O-2 | O-3 | O-4 |
  |---|---|---|---|---|
  | N08 + group 1 (E×5), without M-01 | 18 members / 14 rows | 6 / 6 {01-05 + the five} and 2 / 1 (P4) | 6 / 6 | acyclic |
  | N08 + group 1 (E×5) + M-01 | 13 / 12 | 6 / 6 and 2 / 1 | 6 / 6 | acyclic |
  | as above, with C1-M1's residual as E | 18 / 14 | 13 / 8 | 12 / 7 | acyclic |

- **Consequence.** The owner-facing reading is wrong for O-2 and O-3: N08, if registered as I without its own inversion, re-joins DEL-01-05 to the main residual there, and with C1-M1's E residual it also pulls DEL-01-01 back in. Only O-4 is unaffected. Reading 3's O-1 figure "13 members, 7 rows, the same 7 rows" becomes 13 / 12.
- **Repair.** Recompute §3 on §23's move set (with and without P19's residual) and restate readings 2 and 3; note that N08's own invert (ACCESS l.910) is then needed under O-2/O-3 as well as O-1.

### Minor findings

| ID | Severity | Finding | Evidence | Consequence |
|---|---|---|---|---|
| C1-m1 | MINOR | Withdrawing the clause narrows VER-005's stated inputs: VC-12 ("Compare claims to candidate observations") and VC-26's live part lose their named source for sign-in and local-provider observations. The "pointer" variant says outright "outside this verification" | DEL-01-01 VER-005; HOSTING VC-12, VC-26 | The brief allows no narrowed check. State the narrowing, or keep the verification and treat its input as the residual (C1-M1) |
| C1-m2 | MINOR | §3's "none" cells for O-2…O-4 in rows 3–4 mean "no component containing DEL-01-05". Group 1 still leaves P4 and P13 under O-2 and P13 under O-3 (my reproduction; SCC-002 §22.6) | §3 table rows 3–4 | Say "no N08 component", so the cells are not read as "acyclic" |
| C1-m3 | MINOR | M-01 is labelled IV. Nothing reverses and no contract is interposed; the clause is withdrawn | §1.6 item 2; CSV MoveCode `IV` | Present it as a withdrawal through an owner-accepted SCA, close to the doctrine's "test" cut, which is what CASE-001 R2 proposed |

### Notes

| ID | Note |
|---|---|
| C1-n1 | K-5 sensitivity: DEP-01-01-024's SourceRef also cites CLM-004. G1 r3 reads CLM-004 as an allocation clause and keeps V; I follow G1 |
| C1-n2 | N08's cycle indeed avoids this pair's arcs (reading 1 holds); only the merge statements are affected (C1-M2) |
| C1-n3 | GC-5 item 4: any "no new row" conclusion here is provisional until G2b reports. C1-M1 is an instance G2 did not list, because the HOSTING uses sit on an arc DAG-004 already holds |

## 3. Verdict

**REPAIR.** The rows, quotes, kinds, the ownership claim and every number on the case's own basis hold. Two claims do not:
- "no E residual": HOSTING §8.3 and VC-26 (under VER-005) still use DEL-01-05's sign-in/local-provider access and configuration (C1-M1);
- the N08 interaction under O-2/O-3, once SCC-002's §23 residuals are applied (C1-M2).

**Counts.** BLOCKING 0, MAJOR 2, MINOR 3, NOTE 3.

---

## Addendum A — review of the repair (SCC-CASE-001 §6; SCC-CASE-002 §24) (2026-10-04)

- **Subject:** HEAD `f488e61119`.
  - `SCC-CASE-001/PAIR_ANALYSIS_2026-10-04.md`, sha256 `c2e80f1d88c25d7958c98c1b7cba9a6779914e75c308990cbe38d8ea0a74e995`. Append-only: the diff from `fdc713c439` adds §6 (96 lines) and deletes nothing.
  - `SCC-CASE-001/MOVES_PROPOSED_2026-10-04.csv`, sha256 `ba61c2a2a7dcfeeebec5d74ac65071ed6bfd9321801040e65051fa355d6b24e4`. Append-only, with rows M-01-R, M-02-R and M-N08-R.
  - `SCC-CASE-002/PAIR_ANALYSIS_2026-10-04.md`, sha256 `f61761202c779161d0db358c394b1560b4eaeb7856905f7bcad816b9fd992f0d`. Append-only: §24 (12 lines) withdraws §23.3.
  - No PKG source changed.
- **Also checked at source:**
  - ACCESS-v0.2 §1 I-3 ("Conversation start: explicit `modelProvider` and `model` on `thread/start`", "DEL-01-05 → DEL-01-01 S-4");
  - ACCESS I-4 ("DEL-01-05 → DEL-01-01 §8.3 → DEL-04-03 RS R5");
  - DEL-04-03 ScopeOfWork CLM-004 (the "observed supplier facts … model and destination … from `DEL-01-01`" wording);
  - HOSTING §8.3 ("keeping requested and effective values separate (R5-4)");
  - R5-4 at source (`APP-V4-FIRST-INCREMENT-20260928/R5_RESOLUTIONS.md` l.65).

  All quotes occur at source.

### A.1 Disposition of the findings

| Finding | Repair | Status |
|---|---|---|
| C1-M1, the E/V residual | §6.1 records the residual as E (I-3 carriage and I-4 class) with V (VC-26 live part) on DEL-01-01 → DEL-01-05. It withdraws M-01 as a closing move and turns it into a GC-5 item-3 S1 carry-in (M-01-R). M-02-R, an owner per-edge cut of the whole arc, is the closing act under O-1…O-3. The reasons given for why no rewording removes the flow (DEL-01-01 sends `thread/start`; R5-4) are sound and quoted correctly. SCC-002 §24 withdraws §23.3 and states the effect on SCC-001 correctly | **Resolved** |
| C1-M2, N08 after §23 | §6.2 recomputes against group 1 with §23's E residuals, for B and C, and with and without the SCC-001 cut. Readings 2 and 3 are restated, and N08's own invert is now needed under O-1…O-3 | **Resolved** |
| C1-m1, check narrowed | No clause is withdrawn, so VER-005 keeps its named input | Resolved |
| C1-m2, "none" cells | Cells now say "no N08 component" and are defined | Resolved |
| C1-m3, "IV" label | No IV is claimed. M-01-R is coded "S1 carry-in … not a closing move" | Resolved |

**Closure, reproduced.** Every cell of §6.1 and §6.2 reproduces from my code (G1 r3 kinds, 212 arcs; group 1 = SCC-002 §22 with §23's five E residuals):
- §6.1: residual E gives a 2-cycle under O-1…O-3 and none under O-4; the arc cut gives acyclic.
- §6.2, B: 18/14, 6/6, 6/6; with the residual, 18/14, 13/8, 12/7; with the cut, 13/12, 6/6, 6/6.
- §6.2, C: 18/13, 12/7, 12/7 with the residual; 13/11, 6/6, 6/6 with the cut.
- Every O-4 cell shows no N08 component.
- Adding P19's E residual changes no cell, as §6.2 says.

**Owner acts are now correct.** O-4 needs none. O-1, O-2 and O-3 need one per-edge cut of the arc, and no agent move closes the arc. The cut is presented as the owner's.

### A.2 New observations on the repair

| ID | Severity | Finding | Evidence | Consequence |
|---|---|---|---|---|
| C1A-m1 | MINOR | The O-4 result depends on how the S1 carry-in is worded, and that wording is not drafted. M-01-R describes it as "the depended-on interface" (GC-5 item 3's phrase). If the sentence reads as DEL-01-01 depending on DEL-01-05's *definition*, for example access-entry kinds or the provider-selection contract, the extracted row is I under K-2. The 2-cycle then persists under O-4 too, through DEP-01-05-012 (P) | M-01-R; §6.1 table ("O-4: acyclic") assumes E with V; G1 K-2, K-3 | Draft the S1 sentence so it states runtime values only, with the format owners named: the supplier pin for the requested provider and model; RS R5's `destinationClass` for the class. Keep VC-26's configuration need as a verification input. Otherwise "O-4: none" does not hold |
| C1A-n1 | NOTE | M-02-R's cut must list every row on the arc. That is DEP-01-01-024 and the carried-in row, which would be a `SAME_ARC` UPSTREAM row in DEL-01-01's register under SR-6 tie-breaking, plus any DEL-01-05 DOWNSTREAM mirror | `graph-version.md` SR-6; G1 K-7 | Name them in the ruling when it is made |
| C1A-n2 | NOTE | HOSTING §8.3 restates DEL-01-05's access-entry-kind → class mapping ("`chatgpt-account` and `api-key` → `user-chosen cloud`; `local-provider` → `local model server`") while saying DEL-01-05 derives it. As written it is a cross-reference (GC-5 item 2), not a rule HOSTING applies. It would become I if HOSTING ever applied the mapping itself | HOSTING-v0.9 §8.3 | Keep it as a cross-reference when the carry-in is drafted (relates to C1A-m1) |
| C1A-n3 | NOTE | The author is not a design agent of either member, and the repair restores rather than narrows checks. I found no softening | — | — |

### A.3 Verdict

**READY.** C1-M1, C1-M2 and the three minors are resolved, and every number reproduces. The component closes only by the option choice (O-4) or one owner cut (O-1…O-3), and the repair says so. C1A-m1 is a drafting condition on the S1 carry-in: word it as runtime values with named format owners, or the O-4 result changes.

**Addendum counts.** BLOCKING 0, MAJOR 0, MINOR 1, NOTE 3.
