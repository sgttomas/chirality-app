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
