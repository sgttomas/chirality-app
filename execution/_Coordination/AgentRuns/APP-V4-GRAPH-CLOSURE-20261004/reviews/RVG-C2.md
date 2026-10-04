# RVG review of the SCC-002 early-path analysis (C2) — APP-V4-GRAPH-CLOSURE-20261004

- **Reviewer:** RVG, a Type 2 TASK executor (Claude Opus 5.5, `claude-opus-5-5`), dispatched by HELP_HUMAN on 2026-10-04. No delegation. I did not author the subject. Read-only git, no network.
- **Subject:** the latest committed version, HEAD `ca63f1cea9`, including the §20 extension:
  - `E/_DAG/cases/SCC-CASE-002/PAIR_ANALYSIS_2026-10-04.md`, sha256 `0106118a3e60246a3c23476799a9c616e30f32c83891de3c258c0ab0e414fefe`;
  - `MOVES_PROPOSED_2026-10-04.csv`, sha256 `3c2c91811512c2e03f780c86af0a43bf88fb3ea119cdf2c3e913cd25e4cbf91b`.
- **Earlier version.** I first reviewed `01fdfd598f`. Diffing the two commits shows §1–§19 unchanged apart from two pointer lines, so that review carries forward.
- **Also read:**
  - `workflows/dependency-extract/WORKFLOW.md` (Pass 2 row rules; "Dependency Model: Information Flow Only") and `resources/checks.md`;
  - DAG-004 `GRAPH_BASIS.md`;
  - `APP-V4-SCA003-20261002/OWNER_DECISIONS.md` (Q-5), `DISPATCH.md` (P2-A) and `AMENDMENT_PACKET/IMPACT_ASSESSMENT.md` (M-2);
  - G1 r2 (`SURVEY/G1.md` sha256 `8afa6093…`).
- **Design passages read:**
  - ACT-POLICY-v0.11 §2.4–§2.6 and §5.1–§5.4;
  - EXEC-v0.7 §2.5 (header and R12-4 row l.113), §4.10, §9.1, §9.2, l.1255;
  - ADAPTER-v0.7 §7.7 and `checkpoint_observation.schema.json`;
  - AS-v0.9 §2, §3, §12.1;
  - LOOP-v0.9 l.2072 (grant in force) and the schema listing;
  - C-v0.8 §6.2;
  - RS-v0.10 §3, §7 and `RS_RECORD.schema.json`;
  - WD-v0.9 §4.3.4 and §6.4;
  - WR-v0.2 §7 and §16;
  - NIR-v0.3 §7;
  - LOOP §10.5;
  - P-v0.8 §3.3.
- **Paths and scripts.** `E/` is `projects/chirality-app-v4/execution/`. My scripts are in `$TMPDIR/rvg/` (`rvg_c2b.py`).

## 1. What holds

- **Closure arithmetic.** It reproduces exactly from my own code: Kosaraju plus a subset-DP minimum feedback arc set, with each move modelled as arc removal or a residual kind.

  | Scenario | O-1 | O-2 | O-3 | O-4 |
  |---|---|---|---|---|
  | §15, G1 r1 kinds, 13 moves | 12 members / 12 rows | 5/5 + 2/1 | 5/5 | acyclic |
  | §15, RVG kinds, 13 moves | — | — | — | 5 members / 1 row |
  | §15, with the three registry moves | 12/9 | 4/3 + 2/1 | 4/3 | acyclic |
  | §20.6, r2 kinds, 17 pair moves | 12/8 | 5/2 + 2/1 | 5/2 | 5/1 |
  | §20.6, r2 kinds, 17 pair moves + M-X2 | 12/7 | 2/1 + 2/1 | 2/1 (P13 only) | acyclic |

  The §20.6 check rows also reproduce:
  - P19 closed by DEP-04-02-018 instead of DEP-05-01-025 still closes O-4;
  - P18 closed by DEP-04-02-008 instead of DEP-04-03-022 leaves 4 members and 1 row under O-4.

  §20.2's "P18 must close through DEP-04-03-022" is therefore right.
- **Quotes.** The Design quotes I spot-checked occur verbatim:
  - WR: "Control not built: nothing is registered", "DEL-02-03 asks DEL-02-02 for the text after it opens the run", "Report not established: shown so";
  - NIR: "Accepted transitions … are WR §5.1's";
  - LOOP §10.5: "DEP-05-01-020 has this deliverable consume DEL-05-02's statement";
  - P §3.3: "In Phase 1 the App carries none";
  - DEL-02-01 TBD-004 and AC-005;
  - ACT §2.4: "This is the meaning DEL-04-03 receives. DEL-04-03 owns the format.";
  - ADAPTER §7.7: "The adapter observes and reports".
- **Artefact verdicts (brief item 3).** In every one of the 17 pairs, the quoted Designs show a part-level order with no contradiction. I found no pair that is a real part-level contradiction. What does not hold everywhere is the claim that the deliverable-level cycle closes **without** a structural or ownership change. That is a property of the moves, examined below.
- **Moves supported as stated:**
  - P6, P7 and P21: IV of consumer-needs feedback. DEL-02-01 AC-005 allows "confirmation or its absence"; LOOP §10.5 is already a conformance check.
  - P5's act-meaning re-target: ACT §2.4; DEL-02-01 REQ-003, "PKG-04 receiving contract". The G1-m5 caveat applies.
  - P3: TBD-004 states the current-phase content itself. See C2-m1 for the residual.
  - P18 and P20: the registry pattern. See C2-m2 for the form it must take.

## 2. Findings

### C2-M1 — MAJOR. IV-S (seven pairs) removes the contract input only under three conditions. C2 names a different test, and three of the seven fail one of the conditions today

**The test.**
- The edge semantics are part-level: "the consumer requires the supplier's stated contribution … before the stated part of its work" (GRAPH_BASIS).
- `dependency-extract` extracts "Explicit interfaces where one deliverable requires specific data/artifacts from another". UPSTREAM means "requires information/asset FROM the target".
- C2 frames IV-S as conditional on `dependency-extract` "accepting that carriage by reference is not a contract input". Carriage itself is not the issue. A slot removes the input only if **all** of these hold:
  - **(a) Opaque reference.** The consumer's schema and rules contain no supplier-defined element: no field set, state value or identity scheme of the supplier. A reference "by identity" of the supplier's records needs the supplier's identity scheme, which is I under K-2 in G1 r1 and r2. One example is RS §3 "Common identity elements: *record identity*, *record kind*, *format version* …". A third party's scheme, such as DEL-03-01 §5.3 content identity, does not create the input.
  - **(b) Who checks conformance.** C2 says validation "becomes a conformance check". If the consumer performs that check, it needs the supplier's schema first. That is an UPSTREAM V row on the same arc, which still sequences under O-1. The check must belong to the supplier or a third party, or the residual must be recorded as V.
  - **(c) No stated requirement.** The consumer's ScopeOfWork no longer states a requirement. C2 provides for this through S1 wording.

**Per pair, against the current Designs.**

| Pair (row) | (a) opaque? | (b) | Reading |
|---|---|---|---|
| P1 (DEP-02-02-013) | Yes. WR's intake is "a built view, plus a capture report whose fields are WR's own descriptor identity and references" | V residual recorded by C2 | Holds as stated (closes O-2…O-4) |
| P8 (DEP-02-02-015) | Plausible. WR shows EXEC's report "labelled", and it gates nothing (CC-3) | V residual recorded | Holds as stated |
| P9 (part of DEP-02-02-017) | **No.** The WR ledger "cites it by record identity", and the row also receives "the record kind for the registration act (A15)". Both are RS's (ACT §2.4: "DEL-04-03 owns the format") | Unstated | Fails (a) unless the reference is made opaque or third-party |
| P10 (DEP-02-03-026) | **No**: see C2-M5 | — | Fails |
| P15 (DEP-03-01-031) | **No.** C §6.2 is rule-bearing on RS's lapse vocabulary: rule 4 ("When the bound content changes, the act is shown lapsed"), the "Must not be strengthened by" column, and "*Not yet evaluated* never renders as *not lapsed*". C carries RS record references | Unstated | Fails today. Holds only if C withdraws these rules (C CLM-002 already "does not define" them, so no ScopeOfWork ownership moves) and its references are opaque. DEP-03-01-031 is in every minimum set |
| P17 (part of DEP-03-02-034) | **No.** P §3.3 "Standing at drafting" enumerates AS's seven display states with grant value and scope | — | Holds only by C2's alternative: move the attribution to the record (RS §5) |
| P19 (DEP-05-01-025) | **Not yet.** LOOP l.2072's grant in force carries "grant value, display state (O-6), scope and policy-class record reference". AS §12.1 says the loop only "relays intent" | Unstated | Holds if LOOP's dispatch record shrinks to an opaque settings-version reference. That is feasible, because LOOP is carry-only |

**Consequence (computed, r2 kinds, the §20.6 move set plus M-X2).**
- If P9 and P15 keep an I residual (condition (a) not met), O-4 does **not** close. Two components remain: 6 members needing 2 rows, and 2 members needing 1.
- If every IV-S consumer keeps the conformance check (condition (b)), O-2…O-4 are unaffected. O-1 rises from 7 to 12 remaining rows.
- **IV-S is sound as a design pattern.** It is an "invert behind a contract" in the doctrine's sense. It is not a relabelling when (a) and (b) hold. As C2 states it, it would be accepted on the wrong test.

### C2-M2 — MAJOR. The re-targets rest on a "Q-5" the owner did not decide, and ACT's own text gives DEL-04-01 suppliers

- **Evidence: Q-5's scope.**
  - The owner's Q-5 reads: "the App act control in DEL-01-04, with REQ-008 as adjusted and the drafted OUT-005, AC-008 and VER-008, as worded" (`APP-V4-SCA003-20261002/OWNER_DECISIONS.md` l.53).
  - "DEL-04-01 gains no supplier" is the drafter's description of that one REQ-008 adjustment (DISPATCH P2-A; IMPACT_ASSESSMENT M-2), carried into GRAPH_BASIS l.44.
  - It is not a standing owner rule. C2 (§1 RT, §16, §20.7 "Four rely on Q-5") and G1 (r1 and r2) both present it as one. I did not catch this in RVG-G1.
- **Evidence: what ACT says.**
  - ACT §5.1 "Inputs (semantic)" lists "*grant state* for the class … DEL-04-02 (R-8; R2-6)", with AS §3's seven states, and "*checkpoint state* … DEL-02-01; DEL-02-03; DEL-05-01".
  - §5.3 rule 7 is rule-bearing on DEL-04-02's states: "effective (person-set) with grant value direct … → apply directly".
  - ACT does not define what it receives, so by G1 r2's K-3 this is I.
  - Read so, A3's grant-state input alone (DEL-04-01 → DEL-04-02) forms an SCC containing DEL-04-01: 15 members under O-4 and 16 under O-1, with r2 kinds.
- **Consequence.**
  - P5, P9, P11 and P17 are cycle-safe only while this design-stated input stays unregistered. No owner decision covers that; it is a guard, and G2 lists it as ambiguous item A3.
  - For P17, C2 says so itself ("launder"): the re-target relocates the cycle into ACT §5.1 rather than removing it.
- **Repair.**
  - State Q-5's actual scope.
  - Put the condition to the owner as a question: should DEL-04-01's semantic inputs (ACT §5.1) stay out of the registers, and on what basis?
  - Where an alternative exists, prefer it. For P11, see C2-M3.

### C2-M3 — MAJOR. P11's re-target anchor is reversed. As written, it moves a definition to DEL-04-01

- **Evidence: where the table comes from.**
  - ACT §2.5's control-relation table carries the heading "A12 and the control relation (R4-6; EXEC §4.10 AR-1…AR-4)".
  - EXEC §4.10 is the "ADOPTED (R4-6)" source of the same table (established / pending / refused / unconfirmed, with the arrival effects).
  - C2 §10's order "ACT §2.5 → EXEC §4.10" is the reverse of what the texts show.
- **Evidence: what DEP-02-03-029 actually needs.** EXEC needs AS's display labels from DEL-04-02 ("display *effective*, person-set"; "*set by person, not yet confirmed*").
- **Consequence.**
  - The re-target either has EXEC consume its own adopted rule back from ACT, an unrecorded DEL-02-03 ⇄ DEL-04-01 reliance, or makes ACT the definer of the A12 control relation. The second contradicts "No ownership moves".
  - A plain IV closes the same arc: EXEC keeps §4.10, and drops or cites AS's labels. Closure is unaffected, but the move and anchor must change.

### C2-M4 — MAJOR. "P4 needs a decomposition change under O-1 and O-2" is not established. One owner cut of its residual closes it

- **Evidence.**
  - After M-03a, the arc DEL-03-02 → DEL-02-01 carries only the governance-phase constraint derivation, an L residual (P §3.3 "In Phase 1 the App carries none").
  - An owner per-edge cut of that arc (doctrine §2 rule 3; SR-4) closes P4. Computed under r2 with the §20.6 set plus that cut: O-1 has 12 members and 6 rows; O-2 and O-3 have P13 only; O-4 is acyclic.
  - C2 lists DEC (preferred), IV-O and MRG, and omits CUT.
  - A re-target of the residual to ACT §4.4 ("Acceptance-checkpoint constraint (DERIVED …; R2-12)") is conceivable, under the C2-M2 caveat.
- **What is right.** "Only under O-1 and O-2" is correct.
- **Consequence.** The owner should read this as: P4 needs one owner act under O-1 or O-2 — a cut, or decomposition, IV-O or merge. It should not read "G1's decomposition flag is confirmed". This matters directly to the "no broad structural change" premise.

### C2-M5 — MAJOR (§20.1). P10's IV-S condition cannot be met as written. P10 needs IV-O or decomposition, and O-4 closure depends on it

- **Evidence: the condition.** C2's condition is that EXEC §2.5's X-path rows "must become citations of ADAPTER §7.7's CO→CE mapping".
- **Evidence: what EXEC §2.5 is.**
  - EXEC §2.5 is "App-run reached-when evaluation", placed in EXEC by the binding resolution R12-4 (EXEC l.113, "App-run reached-when table AW-1…AW-12 per kind and native path (N-MCP, N-CLI)").
  - On X it uses ADAPTER's native-path semantics: §9.1, "using ADAPTER §4.1 NM-1/NM-2, §4.5 and OC-9".
  - EXEC l.1255 creates arrivals from "DEL-03-03's observations … `checkpoint_observation.schema.json`".
- **Why citation does not help.** A citation that EXEC's own evaluation rules use is still a requirement for ADAPTER's definition. That is condition (a) of C2-M1.
- **Why the alternative is blocked.** The evaluation cannot move the other way without conflicting with ADAPTER's own text: its schema says "The adapter observes and reports; it evaluates no reached-when, disposition or hold".
- **The real choice.**
  - Move the X-path reached-when evaluation from EXEC to ADAPTER. That is a Design-responsibility move against R12-4 and ADAPTER's stated boundary. It is consistent with DEL-02-03 CLM-002 ("`DEL-03-03` owns external-channel receiving"), so it is IV-O at the Design level, not a ScopeOfWork S2.
  - Or decompose EXEC's X-path evaluation.
  - Or an owner cut or merge.
- **Consequence.** Computed under r2 with the §20.6 move set plus M-X2 but without P10, O-4 does **not** close: 4 members, 1 row. So:
  - "16 close by moves that move no definitional ownership" becomes at most 15 (with P11 per C2-M3 as IV);
  - the IV-S count falls to six;
  - P10 joins P4 as needing an owner-level act.

### Minor findings

| ID | Severity | Finding | Evidence | Consequence |
|---|---|---|---|---|
| C2-m1 | MINOR | P3's IV withdraws DEP-02-01-026, but WD keeps other design reliance on EXEC. §4.3.4 has "Run end and continuation (R4-4; EXEC §4.9 …)"; §6.4 is "confirmed by DEL-02-03 EXEC §6.2"; WD names EXEC on 56 lines | WD-v0.9 l.1089, l.1498 | The CSV puts this under Conditions but gives Residual "None". Unless these are re-anchored to the rulings (R4-4, R-9, …), a currency check finds WD → EXEC reliance with no row and the arc returns |
| C2-m2 | MINOR | The registry moves (P12, P18, P20, M-X2). RS §13.3 enumerates one kind per EXEC event ("Every CE has an RS kind", EXEC R14-1), and R15's kinds hold LOOP's DF-6 values. For RS to define the kinds, suppliers must register their kinds into an RS mechanism. Otherwise the enumerated list still needs the supplier's event set (I residual), and RS reader validation is a V residual | EXEC R14-1; `RS_RECORD.schema.json` (19 `$ref`s into EXEC; one `$ref` to DEL-04-02 settings-in) | The moves are sound in registry form only. Say so in M-10, M-15, M-17 and M-X2r2 |
| C2-m3 | MINOR | P9's re-target covers act meaning only. The A15 record kind is RS format, which falls under C2-M1 | Row Statement; ACT §2.4 | The format part stays on DEL-04-03 |
| C2-m4 | MINOR (resolved by §20) | The first version had no moves for P10 and P19 under r2. §20 adds them (M-14, M-16), and M-15/M-17 supersede M-X1/M-X3 | §20.1, §20.3; CSV | Closed, subject to C2-M5 for P10 |

### Notes

| ID | Note |
|---|---|
| C2-n1 | Ownership (brief item 6). Apart from P11 (C2-M3) and P10 (C2-M5), the proposed S1 wordings move no ScopeOfWork-assigned ownership: DEL-02-01 CLM-002 "`DEL-04-03` owns human-act/run record fields"; DEL-04-03 CLM-004 "owns this format"; DEL-02-03 CLM-002 "`DEL-04-02` owns grant display states" and "`DEL-03-03` owns external-channel receiving". The remaining ownership risk is at Design level, in conditions (a)–(b) |
| C2-n2 | P17 reverses an optional item the owner accepted (Q-11). C2 flags this fairly |
| C2-n3 | Under O-3 only P13 (DEP-02-03-022, E/L) remains. It is correctly E under r2's K-3: EXEC §9.1 supplies DEL-05-01 "the current-phase recorder (§2.4), whose event meanings LP-3 shares". It is the only IMPLICIT/MEDIUM held row, so register-owner confirmation or an owner cut is the right route |
| C2-n4 | The boundary kinds DEP-04-02-008 (I/V) and DEP-05-01-019 (I/V) follow the K-1 precedence correctly and do not affect closure |

## 3. Verdict

**REPAIR.** The artefact verdicts hold for all 17 pairs, and every closure number reproduces. The consequential premise "no broad structural change needed" is not yet supported as stated:
- IV-S, which now carries seven pairs, closes only under conditions (a) and (b). P9, P10, P15 and P17 fail condition (a) today, and P19 needs LOOP's record shrunk to a reference (C2-M1).
- The four re-targets depend on an unregistered design input (ACT §5.1) that no owner decision covers (C2-M2).
- P11's anchor is reversed (C2-M3).
- P10 needs IV-O or decomposition, and O-4 closure depends on it (C2-M5).
- P4 needs one owner act, not necessarily a decomposition (C2-M4).

Read correctly, the evidence suggests:
- a small number of owner-level acts: P4, P10, P13, and the ACT §5.1 registration question;
- several Design rewordings beyond S1: C §6.2, P §3.3, LOOP's grant in force, WD §4.3.4 and §6.4, and RS's kind registry;
- no evidence of a broad decomposition.

Repair needs:
- the conditions (a)–(c), applied pair by pair;
- Q-5 at its real scope;
- P11 as IV;
- P10 reclassified as IV-O/DEC with its owner question;
- CUT among P4's alternatives;
- the residuals for P3 and the registry moves.

**Counts.** BLOCKING 0, MAJOR 5, MINOR 4 (one resolved by §20), NOTE 4.

---

## Addendum A — review of the C2 repair, §21 (2026-10-04)

- **Subject:** HEAD `5c3d6b50cf`.
  - `PAIR_ANALYSIS_2026-10-04.md`, sha256 `55be9211f88acbdf5c78b43306dc84d77f0b97cd4a73e1c30c0fd477a1196a78`, append-only: the diff from `ca63f1cea9` deletes nothing;
  - `MOVES_PROPOSED_2026-10-04.csv`, sha256 `d28ad430aabfa496cc24f5ebbbc18d078686caa76b5e38406ef9262407a86061`, with 12 new rows;
  - `GC_RULINGS.md`, sha256 `dd92df36…`.
- **Also read:**
  - the integrator rulings at source: R-3, R-8 and R-9 (`APP-V4-FIRST-INCREMENT-20260928/R1_RESOLUTIONS.md`), R2-6 (`R2_RESOLUTIONS.md`), R12-4 (`APP-V4-DESIGN-PASS-2-20260930/R12_RESOLUTIONS.md`) and R14-1 (`R14_RESOLUTIONS.md`);
  - EXEC-v0.7 §2.5 and §2.5.1;
  - C's `read_result.schema.json`;
  - LOOP-v0.9 l.210, l.2045–2050 and l.2072.
- **Scripts:** `$TMPDIR/rvg/c2r.py`.

### A.1 Closure and ACT §5.1 table: reproduced exactly

- **Every §21.8 scenario** reproduces from my own code, with G1 r2/r3 held kinds:
  - A0: O-4 10 members / 6 rows;
  - A: O-4 4/1;
  - B and C: O-4 acyclic; O-3 P13 only;
  - C: O-1 12/6; D: O-1 12/4;
  - C without the P3 re-anchoring: O-4 5/1;
  - C with V residuals on the registry moves: O-1 12/9.
- **§21.2's table** reproduces over all 212 arcs, with admitted arcs held fixed:

  | ACT §5.1 inputs registered as I | O-4 | O-1 |
  |---|---|---|
  | grant state | 12 members / 1 row | 15 / 7 |
  | checkpoint state | 11 / 3 | 15 / 9 |
  | all five | 12 / 5 | 15 / 11 |

- **One addition.** The operation-identity input alone (DEL-04-01 → DEL-03-01) closes a 2-cycle with the admitted DEP-03-01-024 under every option. The table should show it: even the least contested ACT §5.1 input is cycle-forming.

### A.2 Disposition of RVG-C2's findings

| Finding | §21 | Status |
|---|---|---|
| C2-M1 IV-S conditions | §21.1 re-tests every IV-S pair against GC-1, including P4's identity part, which I had not tested. It names a rewording, a file, a section and a design agent for each | **Resolved**, subject to A.3 B-M1 |
| C2-M2 Q-5 | §21.2 quotes Q-5 correctly. Re-targets add no new arc (verified: DEP-02-01-018, -02-02-016, -03-02-017 admitted). M-Q-ACT records the owner question | **Resolved** |
| C2-M3 P11 | Plain IV, anchored on EXEC §4.10 and SP-7 | **Resolved** |
| C2-M4 P4 | CUT is listed as the smallest act. "Decomposition confirmed" is withdrawn | **Resolved** |
| C2-M5 P10 | Accepted as I wrote it (IV-O or DEC) | **My finding was wrong in part. Reclassified: see B-M3** |
| C2-m1 P3 residual | M-02-R, with the WD §4.3.4 and §6.4 re-anchoring named | Resolved |
| C2-m2 registry form | M-REG-R, with the RS registry form and V residuals stated | Resolved, subject to B-M2 |
| C2-m3, C2-m4 | Covered | Resolved |

### A.3 New findings on the repair

**B-M1 — MAJOR. GC-1 (a) is silent on an uninterpreted identifier of a supplier-defined scheme. Five rewordings depend on that reading.**

- **The test.** GC-1 (a) says "The consumer's Design uses no field, state value or identity scheme that the supplier defines".
- **What the rewordings carry.** Each carries an "opaque" reference whose values the supplier's scheme defines:
  - P9: an RS record identity in the WR ledger;
  - P15: RS record references;
  - P19: AS's settings-version identity on LOOP's dispatch record;
  - P4: a workflow-run reference resolved through the RS record;
  - P1: an RS record identity, but there it comes from a third party, not P1's supplier, so it is fine.
- **Two readings.**
  - If an identifier typed as an uninterpreted string, and resolved only by its owner, does not "use" the scheme, the rewordings pass. This reading is consistent with the doctrine's "invert behind a contract".
  - If it does use the scheme, none of the five passes, and A0's 10-member component remains.
- **Consequence.** The "15/17 by rewordings" claim turns on this reading.
- **Repair.** HELP_HUMAN should rule on it as a GC-1 clarification (INTEGRATION). Each rewording should then state "typed as an uninterpreted string; resolved by ⟨owner⟩".

**B-M2 — MAJOR. Two integrator rulings must be amended for "rewordings alone". R-8, R2-6 and R12-4 allow the rewordings.** The brief asked about this, and §21.10 left it open. The rulings are INTEGRATION rulings ("not owner policy acts … open to owner revision", R1 header). Amending them is therefore HELP_HUMAN's act, visible to the owner, not an owner decision.

| Ruling | Text (source) | Effect on the rewording |
|---|---|---|
| R-8 + R2-6 (+ R-3 point 6) | R-8: "Two settings references are recorded per operation"; R-3.6: "Record both the standing **at drafting** and the treatment **at resolution**"; R2-6 adds *effective (policy default)* | **Allow** P17's rewording. They require the references to be *recorded*, not held by P. Recording them in RS §5 and settings-in satisfies them. §21.1's "revisits R-8 and R2-6" is overcautious; only the Q-11 owner visibility remains |
| R-9 | "Workflow identity is carried everywhere as {kind, origin, source root, name, revision} … The P, LOOP and PANEL 'identity/version' elements are replaced by it." | **Conflicts** with P4's identity rewording (an opaque run reference in P). R-9 must be amended, or P4 needs an owner act under every option (§21.4) |
| R12-4 | "ADAPTER maps each path's observed items to record elements." | **Allows**, and supports, a P10 rewording (B-M3) |
| R14-1 | "Every CE kind gets an RS entry kind …"; "LOOP §2.3's checkpoint events map to the same RS kinds (RS states the mapping; LOOP cites it)" | **Conflicts** with the registry form (P12, P18, P20, M-X2). In registry form RS stops enumerating supplier kinds, and the supplier states its own mapping. R14-1 must be amended |

- **Consequence.** The bottom line's group 1 needs two named integrator amendments (R-9, R14-1), in addition to the design rewordings and S1 wording.

**B-M3 — MAJOR (RVG self-correction). P10 can close by a design rewording that R12-4 already allows. My C2-M5 was overstated.**

- **What I relied on.** C2-M5 relied on EXEC's own Changes row (l.113) attributing the per-path AW table to R12-4.
- **What R12-4 says.** "ADAPTER maps each path's observed items to record elements."
- **What EXEC's per-path rows do.** EXEC §2.5.1's rows restate ADAPTER's mappings:
  - AW-1 uses NM-1;
  - AW-2 uses OM-1 ("removing the one shell wrapper Codex adds");
  - AW-4 uses NM-2;
  - AW-8 uses §4.5;
  - AW-9 uses OC-9;
  - AW-10 uses §7.7.

  The reached-when *evaluation* itself (whether an observed event matches WD §4.3.1's kind) is EXEC's.
- **The rewording.** EXEC §2.5.1 (AW-1, AW-2, AW-4, AW-8…AW-10) and §9.1's DEL-03-03 row would consume ADAPTER-mapped observations in an input form EXEC defines: "operation call started", "outcome observed", "not evaluable", each with ADAPTER's limit label. ADAPTER §4.1, §4.5, §4.6 and §7.7 emit them. `checkpoint_observation.schema.json` already names `exec_event`.
- **Does it pass?**
  - Evaluation stays in EXEC, so ADAPTER's "evaluates no reached-when" holds.
  - The mapping is ADAPTER's per R12-4, so no responsibility moves.
  - GC-1 (a) holds for EXEC once its rows cite no NM, OM or OC semantics.
  - Design agents: DEL-02-03 and DEL-03-03, with S1 on DEL-02-03 CLM-002.
- **Consequence.** P10 moves to group 1. Scenario B is then reached by rewordings alone:
  - O-4 is acyclic with **no owner act** on SCC-002's I–I pairs;
  - O-3 leaves P13;
  - O-2 leaves P4 and P13;
  - O-1 needs 7 rows.

  M-14-R should become this rewording, with IV-O, DEC, CUT and MRG as fallbacks. The C2 author followed my finding here; the error was mine.

**B-m1 — MINOR. P15's rewording does not name the schema field.** C's `read_result.schema.json` has `act_evidence_ref.lapse_state`, which carries an RS §7 state value. The rewording must remove it from that file, not only from the §6.2 text. `act_kind`'s enum is DEL-04-01's (admitted DEP-03-01-024) and can stay.

**B-n1 — NOTE. The checkpoint-state input of ACT §5.1 is a fair boundary call.** ACT §5.3 rule 2 needs "whether a declared checkpoint applies, the act it requires, and any governing checkpoint constraint", which reads WD's declaration. I would class it I. It does not change the owner question.

### A.4 Bottom line, as corrected

1. **Group 1, by design rewordings, S1 and two integrator amendments (R-9, R14-1), given the B-M1 ruling:**
   - all 17 I–I pairs under O-3 and O-4;
   - 16 under O-1 and O-2, where P4 needs one owner act (CUT smallest).
2. **Group 2, owner acts:**
   - P4 under O-1/O-2;
   - the non-I–I rows: P13 under O-1…O-3; P2, P14 and P16, and the V residuals of P1 and P8, under O-1;
   - M-Q-ACT. If ACT §5.1's inputs are registered as I, they become the cycle-closing rows. Even operation identity alone forms a cycle, with the admitted DEP-03-01-024.
3. **Group 3, per option (my recomputation):**

   | Option | Remaining |
   |---|---|
   | O-4 | acyclic |
   | O-3 | P13 |
   | O-2 | P13, plus P4 without its cut |
   | O-1 | 12 members / 6 rows with the P4 cut (7 without) |

   No decomposition is required anywhere.

### A.5 Verdict

**REPAIR (narrow, text and one ruling).** The repair resolves C2-M1 to M4 and every minor finding, and every number reproduces. Before the premise "no broad structural change" goes to the owner:
- HELP_HUMAN rules on B-M1 (GC-1 and identifiers);
- §21 records the R-9 and R14-1 amendments, and drops "revisits R-8 and R2-6" (B-M2);
- P10 moves to group 1, as rewritten in B-M3, which also corrects my own C2-M5;
- P15's rewording names `lapse_state` (B-m1);
- §21.2's table gains the operation-identity row.

None of these needs new analysis beyond the texts cited here.

**Addendum counts.** BLOCKING 0, MAJOR 3 (one a self-correction), MINOR 1, NOTE 1.

---

## Addendum B — review of C2's §22 narrow repair (2026-10-04)

- **Subject:** HEAD `c6c1fd74b2`.
  - `PAIR_ANALYSIS_2026-10-04.md`, sha256 `ad196971250aacb14f1eb5b8381549014615e23f606b06b96a7c8c44588f8250`, append-only: the diff from `5c3d6b50cf` deletes nothing;
  - `MOVES_PROPOSED_2026-10-04.csv`, sha256 `c9bd426b90c2b54426c3321c673bfbfe1016596a484dcb2af2eec7187bba31c9`, with 8 new "-N" rows;
  - `GC_RULINGS.md`, sha256 `27265cc9…`, with GC-3 and GC-4.
- **Also read at source:**
  - P-v0.8 l.224 (§3.3 workflow identity) and l.806 (§8 Origin row);
  - DEL-03-02 ScopeOfWork REQ-003, AC-004 and VER-004;
  - C's `read_result.schema.json` `$defs/act_evidence_ref`;
  - LOOP-v0.9 l.210, l.2045–2050 and l.2072;
  - ADAPTER-v0.7 l.364–366, l.420 (NM-1) and l.559 (OM-1);
  - DAG-004's admitted arcs touching DEL-03-03.
- **Scripts:** `$TMPDIR/rvg/c2r.py`.

### B.1 Repair list items 1–5: done

| Addendum A item | §22 | Status |
|---|---|---|
| 1 B-M1, uninterpreted identifiers | GC-3 ruled; §22.1 applies it to each identifier | **Done** (B.2) |
| 2 B-M2, R-9 / R14-1 amendments; drop "revisits R-8, R2-6" | GC-4; §22.2; M-12-N | **Done** |
| 3 B-M3, P10 into group 1 | §22.3; M-14-N | **Done** (B.3) |
| 4 B-m1, `lapse_state` | §22.4; M-11-N | **Done**: the field is in the schema's `required` list today, and §22.4 removes it from both |
| 5 Operation-identity row | §22.5 | **Done**: it reproduces as a 2-cycle {DEL-03-01, DEL-04-01} under O-2…O-4, inside the 15-member component under O-1 |

### B.2 The GC-3 passes, checked against the three conditions

| Pair | Uninterpreted string | Not constructed, parsed or validated | Resolver named, and not the consumer | Conditions honest? |
|---|---|---|---|---|
| P4 | Yes, once `proposal.schema.json` drops the `origin` enumeration | Yes, once P §3.3's adapted-identity sentences (l.224, WD's rules) are withdrawn. P §8's "Origin (author, seat role, conversation, workflow identity and run)" row (l.806) must show the run reference only | DEL-04-03's record, with the run issued by DEL-02-03's run starter: both third parties to the pair | **Yes.** The pass depends on the §8 change, and §22.1 and §22.7 say so. P's own ScopeOfWork asks only for "workflow-run attribution" (REQ-003, AC-004, VER-004), so nothing in an accepted text needs the tuple's parts. GC-3 item 3 does not bite |
| P9 | Yes | Yes: whole-string comparison only | DEL-04-03's reader; DEL-01-04 maps | Yes |
| P15 | Yes. C's `#/$defs/identity` is already `{"type":"string","minLength":1}` | Yes, once rule 4, the act-evidence "Must not be strengthened by" column and `lapse_state` go. `act_kind`'s enumeration is DEL-04-01's (admitted DEP-03-01-024), not the pair supplier's | DEL-04-03, or the host (RS L-9) | Yes |
| P19 | Yes | Yes, once LOOP drops grant value, display state (O-6), scope, the policy-class reference and "grant in force: unconfirmed", and O-5 hands the comparison to the record or display owner | DEL-04-02 and the host route | **Yes.** All three removals are named, and "stays I if LOOP keeps an AS state value" is stated |

### B.3 P10: no responsibility moves

- R12-4 assigns the mapping of observed items to ADAPTER.
- ADAPTER already consumes DEL-01-01's MCP and command-execution surfaces through the admitted DEP-03-03-013, and recognizes dispatch at `item/started` (§4.6 OM-1, l.559). So ADAPTER can emit "operation call started" and "outcome observed" with no new input and no new arc.
- EXEC keeps the reached-when evaluation, and ADAPTER's "evaluates no reached-when" holds.
- **Confirmed.**

### B.4 Finding

**B2-M1 — MAJOR. The inverts leave a runtime flow, which is an E row under K-3. The per-option table models these rows as removed, so its O-1…O-3 columns are understated. O-4 is unaffected.**

- **What G1 r2/r3's K-3 says.** It reads a row as E when "the consumer needs runtime instances and has no definitional need". After the rewordings, that is exactly what remains on several arcs:
  - **P10.** EXEC still records ADAPTER's observations at runtime, now in EXEC's own input form.
  - **P18.** RS's writer still receives settings-in at runtime (AS §6 / RS §8 exchange).
  - **P12, P20 and M-X2.** In registry form, RS's reader still takes EXEC, LOOP and ADAPTER entries, unless the S1 wording makes them supplier-written entries in RS's container with no receipt by DEL-04-03.
  - **P19.** LOOP still receives the settings-version identity on each dispatch.
- **Why the rows remain.** `dependency-extract` records information flow ("Information flow only"). Unless the S1 wording removes the runtime receipt from the consumer's ScopeOfWork, these remain rows of kind E. That is the same treatment §21 gives P1 and P8, whose residuals are V.
- **Computed** (G1 r2/r3 held kinds; §21.8 scenarios B and C, with those rows as E rather than removed):

  | Scenario | O-1 | O-2 | O-3 | O-4 |
  |---|---|---|---|---|
  | §22.6 table, C | 12 members / 6 rows | P13 | P13 | acyclic |
  | C, with E residuals on P10, P12, P18, P20, M-X2 | 12 / 10 | 5 members / 5 rows | 5 / 5 | **acyclic** |
  | as above, + P19 | 12 / 11 | 5 / 6 | 5 / 6 | acyclic |
  | B (no P4 cut), with the five E residuals | 12 / 11 | 5 / 5 + 2 / 1 | 5 / 5 | acyclic |

- **Consequence.**
  - §22.6's group 3 holds for O-4 ("acyclic, no owner act on any I–I pair").
  - It does not hold for O-1…O-3. There, the E residuals stay cycle-closing and need either the class choice (O-4) or per-edge owner cuts. O-3 is about five E cuts plus P13, not "P13 only".
  - So the owner's class choice weighs more after the moves than G1 r3's pre-move "O-4 differs from O-3 by one cycle-closing row" suggests.
  - I reproduced the table in Addendum A without testing this assumption. The omission is mine as well as C2's.
- **Repair** (text and table):
  - record E residuals on the IV and registry moves where a runtime flow remains, as §21 does with V for P1 and P8;
  - restate group 3's O-1…O-3 columns, noting that each E residual is a per-edge cut candidate, or leaves under O-4;
  - alternatively, name the S1 wording that removes the runtime receipt from the consumer's ScopeOfWork for any arc where that is genuinely the design.

### B.5 Verdict

**REPAIR (narrow, one table).**
- **Confirmed:** items 1–5, the GC-3 passes and their stated conditions (P4 and P19 are honest), P10's no-responsibility rewording, the operation-identity row, and §22.6's O-4 column and group-1/group-2 structure.
- **Still required:** the O-1…O-3 columns of §22.6 need the E residuals (B2-M1).

**Addendum counts.** BLOCKING 0, MAJOR 1, MINOR 0, NOTE 0.
