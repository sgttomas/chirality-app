# RVG2 review of SCC-CASE-006 (SCC-005, DEL-10-02 ↔ DEL-10-04) — APP-V4-GRAPH-CLOSURE-20261004

- **Reviewer:** RVG2, a second standing independent reviewer. Type 2 TASK executor, Claude Opus 5.5 (`claude-opus-5-5`), dispatched by HELP_HUMAN on 2026-10-04. No delegation. I authored none of the subject or its Designs. Read-only git, no network.
- **Subject** (committed at `c9885b8f71`, unchanged at HEAD `c5ca7ee0c9`), by design agent O-E:
  - `E/_DAG/cases/SCC-CASE-006/PAIR_ANALYSIS_2026-10-04.md`, sha256 `4024c924c4c3f2e15d97b7ea9eaad7bdf3fa9f46fd1f1204934af8ec2309488f`;
  - `E/_DAG/cases/SCC-CASE-006/MOVES_PROPOSED_2026-10-04.csv`, sha256 `25dbe7d578d4cf5294809e592cde4ee28d30e256066e81b5ab50adb2bcdf6c88`.
- **Basis read:** `docs/CYCLE_DRIVEN_RESOLUTION.md` §2; `CASE_BRIEF_COMMON.md`; `GC_RULINGS.md` (now sha256 `7fcbb551…`; GC-1…GC-4 unchanged since the subject's `27265cc9…`; GC-5 appended later at `35f2d2ca38`, applied here as current basis); `SURVEY/G1.md` r3 (`3d6543bc…`); `reviews/RVG-C2.md` with Addenda A and B; `workflows/dependency-extract/WORKFLOW.md` (Functions 1–3, match/merge precedence, "Information Flow Only") and `resources/checks.md`.
- **Sources checked at their hashes (all equal the subject's §0):** DEL-10-02 and DEL-10-04 `ScopeOfWork.md` and `Dependencies.csv`; UC-v0.2 (`da0176cb…`); DA-v0.3 (`faffae81…`); EB-v0.4 (`b12c55c7…`); `dag_reach.py` (`63259575…`); DAG-004 `DependencyEdges.csv` (`c4303374…`) and `CandidateEdges.csv` (`2bfff10e…`); DEL-10-04 `_DEPENDENCIES.md` run notes; `APP-V4-DESIGN-PASS-4-20261003/R23_RESOLUTIONS.md` (R23-31) and `SURVEY/S2-E.md` (E2-9); DAG-004 `ACCEPTANCE_RECORD.md`.
- **Scripts:** my own, in `$TMPDIR/rvg2/` (`kinds.py` parses G1 r3's kinds for all 212 arcs; `g.py` Tarjan plus an exact subset-DP minimum feedback arc set; `q.py` quote checker). `E/` is `projects/chirality-app-v4/execution/`.

## 1. What holds

- **Rows and quotes.** DEP-10-02-012, DEP-10-04-006 and mirror DEP-10-04-014 match DAG-004 exactly (Direction, Type, Statement, EvidenceQuote, SourceRef). DEP-10-04-006's EQ is shared verbatim by DEP-10-04-005 and -007 (checked in the live register), so K-1's Statement reading is right. Every ScopeOfWork and Design quote in §1.2–§1.3 occurs at source (script check, whitespace and mark-normalised), including both `project-dag` resource quotes.
- **Kinds.** DEP-10-02-012 L and DEP-10-04-006 P/E follow G1 r3 (K-6, K-1/K-4).
- **Isolation.** Over all 212 arcs, no deliverable other than DEL-10-04 consumes DEL-10-02, and none other than DEL-10-02 consumes DEL-10-04. The §0 isolation claim holds, so the component's result does not depend on other arcs' kinds.
- **Closure table (§5).** Every cell reproduces from my code, including the A9 columns ({10-01…10-04} under O-1…O-3 with no move; {10-01, 10-03, 10-04} with M-01; acyclic under O-4).
- **R23-31 and E2-9.** R23-31 rules E1-1…E4-5, SQ-E1 and SQ-E3 and does not rule E2-9 (S2-E l.302: "No ruling needed"). The reversal of UC §8 and DA §6 therefore amends no integrator ruling, as §4 says. The reversal is disclosed in the header and §3.
- **Projection verdict.** The part order in §3 (controls settled by Root practice → graph production → selection under the accepted DAG) is supported by DEL-10-02 REQ-001 and DEL-10-04 REQ-008. I agree the 2-cycle is version feedback at deliverable resolution.
- **Owner acts listed.** M-02 (cut) and the further merge/decomposition alternatives are presented as the owner's; M-01's SoW wording is routed through an owner-accepted SCA. No reserved act is presented as an agent move.

## 2. Findings

### C6-M1 — MAJOR. M-01 models the whole of DEP-10-04-006 as deleted. Its runtime (E) part remains, by G1 r3's own reading and by DA's own text

- **What the subject says.** M-01 Residual: "None that sequences"; the only residual it considers is V. The CSV's `KindConfirmed` for M-01 nevertheless reads "P (secondary E)", and §2 confirms "P/E … as written".
- **What remains after the rewording.** M-01 removes the production part (records as graph input). It does not remove DEL-10-04's runtime use of undertaking records for its OUT-002 evidence, which DA itself records:
  - DA §2, column "Recorder of the act → record writer": DAG-004's acceptance custody runs "Run `APP-V4-SCA003-20261002` DECISION-3 → node D2"; DAG-002 and DAG-003 likewise through run DECISION records.
  - DA §3, REQ-005 row: the checkpoint packages, review packets and separate reviewers are taken from the runs' `DAG_PREP/` folders.
  - These are undertaking records kept under DEL-10-02's controls: UC §1 ("Owner acts | Transcribed by HELP_HUMAN into OWNER_DECISIONS files"), UC §2 (work graphs, briefs, "Candidate-bound capability and check account" bound to DISPATCH), R23-31.1 ("Outputs live in the existing records: … the work graphs and run records") and R23-31.6. DEL-10-04 CLM-002's unchanged first sentence still names DEL-10-02 as "the undertaking manager's current work-graph/control … contribution, with human stage decisions", and DEL-10-04 REQ-006 requires the relay provenance these records carry.
- **Kind.** DEL-10-04 needs instances only and defines its own acceptance-record format (project-dag), so the residual is E under K-3 (or P under K-4, if the relay records are read as evidence needed to produce OUT-002). This is RVG-C2 B2-M1's pattern.
- **Computed (my script).** With DEP-10-04-006 kept as E instead of removed: O-1 and O-2 keep {DEL-10-02, DEL-10-04}, 1 row; O-3 and O-4 are acyclic. With A9 also added: {10-01…10-04} under O-1…O-3 (2, 2, 1 rows).
- **Consequence.** §5's "acyclic" under O-1 and O-2 and §6's "Owner acts O-1, O-2: None beyond accepting the S1 wording" are not established. Under O-1/O-2 one owner per-edge cut (of the E residual or of DEP-10-02-012, i.e. M-02) is still needed unless a source-supported S1 wording removes the receipt itself.
- **Repair.** Record the E residual in §4 and the CSV; restate §5/§6 for O-1/O-2; or name the S1 wording that makes DEL-10-04's OUT-002 evidence independent of undertaking records, and show a source for it.

### C6-M2 — MAJOR. The proposed S1 sentence itself states a reliance on DEL-10-02, so "dependency-extract then retires DEP-10-04-006" is not supported

- **The rule.** DEL-10-04's register is extracted from `ScopeOfWork.md` only (`_DEPENDENCIES.md` run notes: SOURCE_DOCS / EXECUTION_DOC_ORDER `ScopeOfWork.md`, CONSERVATIVE). Pass 2 extracts "constraints explicitly framed as requirements"; match/merge rule 2 keeps a row's ID when class, direction, type, target and a near-equivalent Statement recur; unseen extracted rows are RETIRED.
- **The proposed text.** "It runs its graph undertakings under the accepted undertaking practice that `DEL-10-02` indexes, and takes no `DEL-10-02` record as a graph input." The first clause names DEL-10-02 as the source of a practice DEL-10-04 must run under; the CLM-002 sentence "App `DEL-10-02` is the undertaking manager's current work-graph/control and practice-feedback contribution, with human stage decisions" stays unchanged.
- **Consequence.** A conservative extractor has an explicit UPSTREAM constraint on DEL-10-02 to record (kind I: a practice DEL-10-04 does not define; computed effect identical to C6-M1: 2-cycle under O-1/O-2). "Takes no record as a graph input" negates only the graph-input reading. Under GC-5 item 3, a reliance stated in the ScopeOfWork is carried into the register.
- **Repair.** Cite the Root sources directly (SPEC §9.8; `project-dag`; `construct-local-work-graph`) without "that `DEL-10-02` indexes", and say plainly what DEL-10-04 does not receive from DEL-10-02. The subject's §7 already lists this as not established; it should be resolved before the move is presented as closing O-1/O-2.

### Minor findings

| ID | Severity | Finding | Evidence | Consequence |
|---|---|---|---|---|
| C6-m1 | MINOR | M-01 is labelled IV, but nothing reverses and no contract is interposed. It is a withdrawal of a consumer-side statement, re-targeting the content to Root practice (a third party) | §4 M-01; the arc DEL-10-02 → DEL-10-04 already exists (DEP-10-02-012); CSV MoveCode `IV` | The owner should read M-01 as an SCA that removes a stated input of DEL-10-04, not as an agent-only design refinement. §6 does route it through the owner's SCA acceptance, so no reserved act is bypassed |
| C6-m2 | MINOR | M-03's GC-3 basis is misapplied. A9 is E, not I, and EB's B-rows take content from DEL-10-04's records, not only an identifier: B-11's "Subject" ("The 33 files of `REVIEW_PACKET.md` …") and "What it did not decide (as the record states)" come from `ACCEPTANCE_RECORD.md` ("This acceptance does not:", l.75). The runtime flow DEL-10-04 → EB remains; the rewording keeps A9 out of the registers only because DEL-10-01's SoW states no such need. Separately, M-03 deletes DEL-10-01 from DA §6's consumer (handoff) table while EB still reads the acceptance records | EB-v0.4 §2 B-7, B-11; DAG-004 `ACCEPTANCE_RECORD.md` l.75; G1 r3 §2b.1 A9 (E, secondary L) | The A9 result is unchanged (§4 already names the E/L fallback). The text should not claim "takes no structure" or rely on GC-3; it should say A9 stays an E flow that is not a register row, and keep DEL-10-01 visible in DA §6 as a reader |

### Notes

| ID | Note |
|---|---|
| C6-n1 | Under O-3 and O-4 the component is already absent (DEP-10-02-012 is L); M-01 is then optional, as §5 says |
| C6-n2 | No existing check is narrowed: DEL-10-04 REQ-009/VER-009 still map DEL-10-02's undertaking controls through CLM-002's unchanged first sentence. DEP-10-04-005/-007 keep their IDs under match rule 2 but need their EvidenceQuote refreshed, because the shared EQ text changes |
| C6-n3 | Self-review. O-E reverses its own UC §8 / DA §6 statements and says so. The reversal is not a softening of a check, but it under-reads O-E's own DA §2–§3 evidence base (C6-M1) |
| C6-n4 | GC-5 (later than the subject) item 4 makes every "no new row" conclusion provisional until G2b reports; that applies to M-03's "A9 stays a non-row" |

## 3. Verdict

**REPAIR.** Rows, quotes, kinds, isolation, the projection verdict and every closure number hold. The move does not yet close the component under O-1 and O-2 as claimed:
- the E part of DEP-10-04-006 is modelled as deleted (C6-M1);
- the proposed S1 sentence re-states a reliance on DEL-10-02 that the extractor would keep (C6-M2).

Either repair both and show the residual-free wording at source, or present M-01 with an E residual and M-02 (owner cut) as the closing act under O-1/O-2.

**Counts.** BLOCKING 0, MAJOR 2, MINOR 2, NOTE 4.

---

## Addendum A — review of the §9 repair (2026-10-04)

- **Subject:** HEAD `c2931f954d` (repair commit `eb59468020`), by O-E.
  - `PAIR_ANALYSIS_2026-10-04.md`, sha256 `2216bff17fce3b624198755d8b69dca2bfb43f323b7309aee0f0af8151e28a2c`. Append-only: the diff from `c9885b8f71` adds §9 (162 lines) and deletes nothing.
  - `MOVES_PROPOSED_2026-10-04.csv`, sha256 `a672dbd4712af9f57fa23c0fa1448f202879ed522f4cb98f34b6fd139a4e7b82`. Append-only, with rows M-01-R, M-04, M-02-R and M-03-R.
  - No PKG-10 file changed.
- **Also rechecked:** DA-v0.3 for every use of work graphs, practice notes and capability accounts (§2, §3, §6); DEL-10-04 REQ-005, REQ-009, OUT-002; DEL-10-02 REQ-008; UC §1.

### A.1 Disposition of the findings

| Finding | §9 | Status |
|---|---|---|
| C6-M1, the E part | §9.1 accepts it from DA §2–§3 and keeps DEP-10-04-006 as E. M-04 (cut of the E residual) or M-02-R closes the component under O-1 and O-2 | **Resolved** |
| C6-M2, the S1 sentence | §9.2 takes the second repair route: the row stays, worded as E. "Practice … that `DEL-10-02` indexes" is replaced by direct Root citations (`project-dag`, SPEC §9.8), so no I row to DEL-10-02 arises from it | **Resolved**, subject to A.2 C6A-m1 |
| C6-m1, the "IV" label | Re-coded `NARROW (P→E; SCA)`; not presented as closing | Resolved |
| C6-m2, A9 and GC-3 | M-03 withdrawn. A9 is carried as an E row under GC-5 item 3 (M-03-R), DA §6 keeps DEL-10-01 as a reader, and EB's content use is stated as a GC-5 item-1 dependency | Resolved |

**Closure, reproduced.** Every cell of §9.5 reproduces from my code (G1 r3 kinds, 212 arcs).
- **SCC-005 alone, after M-01-R:** {10-02, 10-04}, 1 row under O-1 and O-2; acyclic under O-3 and O-4. M-04 or M-02-R makes it acyclic.
- **With A9 as an E row:**
  - O-1 and O-2: 4 members, minimum 2. Both {M-04, A9} and {M-02-R, A9} close it. A9 alone, M-04 alone or M-02-R alone does not.
  - O-3: 4 members, 1 row. A9 alone closes it.
  - O-4: acyclic.
- **Residual read as P:** the same figures, with M-02-R the cut. §9.5's fallback is right.
- **§9.4's EB claim:** sourcing EB from run OWNER_DECISIONS would close 10-01 → 10-02 against DEP-10-02-011 (P). This holds.

**Owner acts are now correct.** O-1 and O-2 need one cut, or two with A9 carried. O-3 needs none, or one (A9) when it is carried. O-4 needs none. Each cut is the owner's. M-04's recommendation is labelled as agent opinion, and its doctrine basis ("runtime/test/optional") fits an E row. M-02-R stays available.

### A.2 The five narrowings (§9.6), and whether "NARROW P→E" is truthful

- **The five corrections are genuine.** Each listed narrowing is real and is reversed in §9.2–§9.4:
  - the S1 sentence;
  - the DA §6 rewording;
  - the UC §8 rewording;
  - the practice-feedback consumption;
  - the M-03 deletion and GC-3 note.
- **No check is narrowed.** DEL-10-04 REQ-005, REQ-006, VER-005, VER-006 and VER-009, and DEL-10-02 REQ-001 and VER-001 are intact.
- **"NARROW (P→E; SCA)" is truthful.** It narrows a row's stated content from production input to evidence handoff, not a check. It is routed through an owner-accepted SCA. §9.3 and the CSV say it closes nothing by itself. It is not presented as one of the doctrine's four moves.

Two residual points remain in the new wording:

| ID | Severity | Finding | Evidence | Consequence |
|---|---|---|---|---|
| C6A-m1 | MINOR | The §9.2 S1 sentence names "checkpoint packages" and "review records" among what DEL-10-04 **receives from** DEL-10-02's records. Their content is DEL-10-04's own OUT-002: REQ-005 "Prepare the selected project-dag checkpoints as concrete decision packages … An instance that did not assemble the graph independently examines it"; AC-005 and VER-005. DEL-10-02 REQ-008 excludes "production-DAG construction". What DEL-10-04 does take from DEL-10-02's records is narrower: the owner-act transcriptions (UC §1), the work-graph node identities that carry custody (DA §2 "node D2"), and the capability and check accounts (DEL-10-02 OUT-002; UC §2, §4). **My own C6-M1 listed the packages and review packets loosely as undertaking records; that imprecision is mine** | DEL-10-04 REQ-005, OUT-002; DEL-10-02 REQ-008; DA §2, §3 | No closure effect: the row is E either way. But as worded, the Statement an extractor writes would attribute DEL-10-04's own packages and reviews to DEL-10-02, against both deliverables' REQ-008/REQ-009. Reword to receipt of "the owner-act transcriptions, work-graph node and custody records, and capability and check accounts of its graph undertakings", and keep packages and reviews as DEL-10-04's own records kept in those runs |
| C6A-m2 | MINOR | §9.6 row 4 says practice-feedback consumption is "Kept: practice notes … among the applicable records DEL-10-04 may cite as evidence (E)". The §9.2 sentence does not mention practice-feedback records. DA uses none today (checked: no practice-note use in DA-v0.3) | §9.2 text; §9.6 row 4; DA-v0.3 grep | Small residual inconsistency in the narrowing account. Either add practice-feedback records to the §9.2 evidence list, or state in §9.6 that DEL-10-04 does not consume them and that CLM-002's first sentence (unchanged) keeps DEL-10-02's ownership visible for VER-009. Either is truthful; the current pair is not |

**Notes.**
- C6A-n1: M-03-R's DEL-10-01 S1 sentence ("from `DEL-10-04`'s acceptance records, as evidence") reads as E under K-3: EB defines its basis-chain format and takes instances. Under GC-5 item 4 it stays provisional until G2b reports, as §9.4 says.
- C6A-n2: Self-review. O-E reports and reverses its own narrowings, including one I had not raised (UC §8). Apart from C6A-m2, I found no remaining narrowing.

### A.3 Verdict

**READY.** C6-M1, C6-M2 and both minors are resolved. Every closure figure reproduces, and the owner acts per option are complete and correctly attributed. Apply the two wording corrections (C6A-m1, C6A-m2) when the S1 sentence is drafted for the SCA. Neither affects closure.

**Addendum counts.** BLOCKING 0, MAJOR 0, MINOR 2, NOTE 2.
