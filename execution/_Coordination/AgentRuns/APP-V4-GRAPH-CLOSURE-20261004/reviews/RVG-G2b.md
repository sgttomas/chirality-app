# RVG review of SURVEY/G2b (abbreviation-aware Design-use inventory) — APP-V4-GRAPH-CLOSURE-20261004

- **Reviewer:** RVG, a Type 2 TASK executor (Claude Opus 5.5, `claude-opus-5-5`). No delegation. I did not author G2b. Read-only git, no network.
- **Subject:** `SURVEY/G2b.md` at commit `1b63ac8d60`, sha256 `499fbcd1c9928485a0051b69a9dfd704470d2306b46262c47a9f5208968cb6c7`.
- **Scripts (my own; G2b's were not read):** `$TMPDIR/rvg/g2bscan.py` (pair scan), `g2bcum.py` (cumulative sets), `g2bsens.py` (sensitivity and minimum sets). Kinds are G1 r3's, parsed from G1.
- **Paths:** `E/` is `projects/chirality-app-v4/execution/`.

## 1. Cumulative figures: reproduced exactly

G2b's §4.1 and §4.2 tables parse to 62 dependencies (I 51, P 8, V 2, L 1) and 13 unclear pairs (I 11, V 2). Added to DAG-004's 212 arcs, filtered by option:

| Added | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| nothing | 13, 3, 2, 2, 2, 2 | 12, 3, 2, 2 | 12, 3 | 12, 3 |
| the 24 confirmed G2 items | **19**, 3, 2, 2, 2 | 13, 3, 2, 2, 2 | 13, 3, 2 | 13, 3, 2 |
| all 62 | **26**, 3, 2, 2 | **16**, 3, 3, 3, 2, 2 | 16, 3, 3, 2, 2 | 16, 3, 3, 2 |
| 62 + 13 unclear | 26, 5, 2 | 25, 5, 2 | 25, 3, 2 | 25, 2, 2 |

The member sets also match §5.2, including {03-04, 09-06, 09-09} under O-2…O-4 and {09-12, 10-02, 10-04} under O-1 and O-2. The status counts reproduce: 29 new, 24 G2 N items, 9 G2 §5 items. Of the 13 "new SCC-forming", 5 only add arcs inside SCC-002, with no change of membership.

**These are pre-move figures:** DAG-004 plus the inventory, with none of the case moves applied. That matters for §4.

## 2. The five flagged judgment calls

| Call | My reading, at source | Robust? |
|---|---|---|
| **RELAY P8 (09-06 → 03-04): dependency** | RELAY l.816–819: the P8 questions "cover host-loop evidence that the integration guide's receiving map needs". GUIDE consumes the relay through the admitted DEP-03-04-022. This is **consumer-needs feedback (I/R)**, the pattern G1 counts as I in SCC-002 (P6, P7, P21) and C2 closes by IV (needs become a requirements input). | **Yes, as counted.** It is cheap to close: an IV rewording, with the relay already answered. Agent-level |
| **A7 (09-09 → 09-06): dependency, though both Designs call it a cross-reference** | XT §2: "Standing uses … the DEL-09-06 contribution ladder (CA §7.2)". That is a use. XT F-23 records that it was called a cross-reference *because* a row "would enlarge SCC-002", which is exactly what GC-5 item 3 rules out. But CA §7.2 says "The seven standings and their order are stated by SoW OUT-004" (verified, DEL-09-06 SoW l.53): the ladder is **basis-carried**. | **Counted correctly as worded; closable by citation.** If XT cites DEL-09-06 SoW OUT-004 for the ladder's names and order (GC-5 item 2), it is not a dependency. O-1-relevant only (O-2…O-4: no cycle) |
| **EXP-R9 (09-01 → 09-06, 09-09): unclear** | EXP reads receivers' schemas to check "the mapping to W14 and XT is one to one", labelled "cross-references, not reliance". That is the **supplier checking its receivers' conformance**, which GC-1 (b) assigns to the supplier. Counting the check itself as a reverse dependency would penalise the arrangement GC-1 requires. | **Resolve as not a definitional dependency (at most V).** Effect is O-1 only either way |
| **TA-4 (01-03 → 04-03): dependency, though NPTD §16.3 calls act records runtime values** | NPTD TA-4's display rule uses RS §6.1's element meanings and RS HA-2. Under GC-5 item 1, a rule-bearing use is a dependency whatever the Design calls the value. Both contents are ACT's or a ruling's: ACT §2.4 carries the element meanings ("This is the meaning DEL-04-03 receives") and the rule ("A record is non-conformant if it names the recorder as the decision actor"), and K1-4 carries "identity not verified". | **Yes, as counted.** Cheap: re-target to ACT §2.4 and K1-4. That adds 01-03 → 04-01, cycle-safe while ACT51's condition holds |
| **PKG bundle layout (01-06 → 02-02, 02-04): unclear** | PKG §4.1 P-2 and P-3 need WR's workflows and ROLE's files to produce a package candidate. By K-4 that is P. The R23-2 analogy (runtime value) fits a decision package, not build inputs. | **Lean dependency (P).** Effect is O-1 only (a merge with SCC-003); O-2…O-4 show no cycle |

## 3. The new SCC-forming dependencies (GC-5 items 1 and 2)

The four that pull members in:

| Pair | Pulls in | GC-5 reading | Robust? |
|---|---|---|---|
| D22 04-01 → 04-03 (ACT file content identity; lapse vocabulary; A16 "lapse-evaluated as an App file (RS L-1, L-6)") | DEL-04-01, and with it 01-02 and 01-03 (01-02 → 04-01 is admitted) | Item 1. The A16 rule adopts RS L-1/L-6 by citation, and no ruling carries them. "The lapse-state vocabulary is DEL-04-03's" alone would be attribution | Yes (as in RVG-ACT51 ACT-M1) |
| D01 01-03 → 04-03 (TA-4) | DEL-01-03 | Item 1 (§2) | Yes; cheap re-target |
| D36 09-06 → 03-04 (RELAY P8) | NEW {03-04, 09-06} | I/R feedback (§2) | Yes; cheap IV |
| D07 02-03 → 09-06 (EXEC RT-11 follows CA §8.2's case list, "the consumer's list governs") | DEL-09-06 (O-1 only) | V. A supplier's evidence account shaped by its consumer's list; leaves under O-2…O-4 | Yes as V |

**Others checked.**
- **D57 09-12 → 10-02.** PV's `method_note` "has exactly DEL-10-02 UC §5's fields". This is the *inverted* form: the supplier conforms to the receiver's format. The reverse arc DEP-09-12-012 is E under G1 r3, so the cycle exists only under O-1…O-3. Correct as counted, and correctly no cycle under O-4.
- **D08 03-01 → 02-01.** C's V-GR1 fixture runs WD-EX E1d's workflow. R-9 says "DEL-03-01 §10 owns the one invented fixture catalogue … Other files cite its entries", so the fixture content should be C's own, with WD-EX citing it. Counted correctly; cheap to invert.

**The unclear pair that matters most: U01, 01-01 → 01-04.**
- It alone gives a 16-member component under O-2…O-4.
- HOSTING §6.2.1 RT-08's guard names "the negative forms per kind (NIR-v0.2 §4.3 …; PROPOSED empty answer map … empty grant), or the submission says `submittedAs` *decline*". `submittedAs` is a field of NIR's `nir.answer-submission.schema.json`, and the empty forms are NIR's PROPOSED values. HOSTING's transition rule reads them.
- Under GC-5 item 1, that is a dependency (I), not unclear. The Codex-native values (`decline`, `cancel`, …) are generated types that HOSTING itself owns.
- **G2b-M1 (below).**

## 4. The "not a dependency" sampling

I scanned 19 pairs with my own alias scan, reading the use-verb lines, including the large ones G2b did not read in full. 18 agree with G2b's classification:

| Pair (uses) | G2b reason | My reading |
|---|---|---|
| 01-01 → 01-02 HOSTING → RECOVERY (95) | cross-reference | **Agree, on a better ground.** HOSTING's §4.5 and §4.6 stop rows use DEF-3…DEF-6 names. R17-3's own text states the three operations and says "DEL-01-02 owns these definitions; HOSTING … reworded … to cite them". HOSTING restates the rule in its own text (§4.5 l.572–582). It is ruling-carried plus own text (GC-5 item 2). G2b should record that reason, because R17-3 also *directs* to DEL-01-02 |
| 02-01 → 02-02 (66) | attribution | Agree: WR's proposals described; owner and receiver tables |
| 01-01 → 02-03 (61) | attribution / receivers | Agree: observe-lifecycle receiver list; HP-2 "Not adopted" |
| 09-06 → 09-09 (57) | explicit cross-reference | Agree: CA §11.1 says "A cross-reference … not a consumed input" |
| 01-01 → 02-04 (55) | attribution | Agree. Several matches are false positives on the role text "ROLE ONE" in OBS-3 |
| 03-03 → 04-03 (53) | cross-reference | Agree: "Destination per turn (RS R5)" names the record target |
| 01-02 → 01-04 (44) | receiver list | Agree: RECOVERY §4.1 "Offered" table |
| 03-01 → 02-03 (44) | attribution | Agree: C §7.1 row 4 describes EXEC's evaluator ("Per EXEC") |
| 01-01 → 01-03 (38) | ruling-carried / cross-reference | Agree: "DEL-01-03 reads the declared value" (receiver) |
| 03-02 → 02-03 (38) | ruling-carried (R5-1) | Agree. Read at source: R5-1's text carries the four hold-support values. Governance phase in any case |
| 02-01 → 02-04 (30) | ruling-carried (R17-9) / attribution | Agree: guidance composition described (K-9) |
| 04-01 → 03-03 (25) | ruling-carried (R4-13, R4-14, R5-2) | Agree on the lines read: pin and receiver lines |
| 04-01 → 05-02 (25) | cross-reference | Agree |
| 01-05 → 05-01 (22) | cross-reference ("by analogy") | Agree: the rule is stated in ACCESS's own text |
| 01-03 → 02-04 (16) | runtime value | Agree: "Dropped (C-07): DEL-02-04 consumes DEL-01-03" |
| 02-03 → 02-04 (15) | runtime value (R20-4) | Agree: the run starter's composition is EXEC's own |
| 02-02 → 02-04 (15) | ruling-carried (R20-9, R17-8/R19-7) | Agree |
| 05-01 → 01-01 (39) | corroborating observation (= G2 A5) | Agree |
| 01-01 → 04-03 (48) | receiver lists | Agree |

**On G2b's own pattern pass, a caveat.** G2b used a pattern pass for the large pairs. RVG-ACT51 showed that rule-bearing uses can sit in table cells with no use verb (ACT §2.5). My sample found none missed in these 19, but it cannot exclude them for the 232 pairs not sampled.

## 5. Findings

### G2b-M1 — MAJOR. U01 (HOSTING → NIR) is a dependency, not unclear, and it is the largest single SCC-forming item

- **Evidence:** §3 above.
- **Consequence.**
  - Registered or left in the Design, it brings DEL-01-01, 01-02, 01-03 and 01-05 into the main component under every option. The size is 16 under O-2…O-4, in G2b's own §4.2.
  - It falls in SCC-CASE-001's area. That case's "no new row" is therefore not merely provisional: it is contradicted by this pair.
- **Closing move: an invert.** HOSTING owns the server-request register and its transitions (`hosting.server-request-entry.schema.json`). NIR's submission could carry HOSTING's own value, negative or positive, in HOSTING's terms. HOSTING would then read no NIR field, and the PROPOSED empty forms would become NIR's mapping.
- **Who:** the DEL-01-01 and DEL-01-04 design agents. No ScopeOfWork ownership moves.

### G2b-M2 — MAJOR (reading, for the owner checkpoint). The headline figures are pre-move, and they overstate the structural finding

This is the coordinator's central question. I recomputed with the case moves applied: SCC-002 §23 scenario C, with its E residuals, and all 62 G2b dependencies added. Under O-4:

| Variant | Residual components (members / minimum rows / new pairs inside) |
|---|---|
| C2 moves, no G2b | {07-01, 07-02, 08-01} 3/2 only (CASE-005's, which its own moves close) |
| C2 moves + all 62 | **14/11** (14 new pairs inside), plus 3/1, 3/2, 2/1 |
| C2 moves + 62, **without the 9 DEL-04-01 pairs** | five small cycles, each 1 row (or CASE-005's 2): {01-03, 02-02, 04-03} (D01 TA-4); {02-01, 03-01, 03-02} (D08 C fixture); {03-04, 09-06, 09-09} (D36 RELAY P8 + D49 A7); {09-07, 09-11} (N13); {07-01, 07-02, 08-01} (CASE-005) |

**Reading.**

1. **The large component is DEL-04-01.**
   - Under O-4, after the SCC-002 moves, every pair beyond a few local ones that keeps the graph cyclic runs through ACT. Nine supplier pairs: AAC, WD, WR, EXEC, C, P, AS, RS, LOOP.
   - DEL-04-01 has 20 admitted consumers. Every Design-level use of a consumer's artefact therefore closes a cycle.
   - ACT51's rewordings address the §5.1 inputs (D16, D21, and parts of D18, D19 and D23).
   - The remaining ACT uses still need the same treatment, or a decomposition of DEL-04-01. Those are AAC (D15), WR (D17), P §2.5 and §9 (D20), RS (D22), EXEC's package shape and hold support (D18), and LOOP's network rules (D23).
   - **This is a real, robust structural finding,** but it sits in **one hub**, not spread across the Designs.
2. **Outside ACT, under O-4, the residue is four small local cycles,** each with one cheap named move:
   - TA-4: re-target;
   - the C fixture: invert per R-9;
   - RELAY P8: IV;
   - A7: re-anchor to SoW OUT-004.

   Plus N13 (M-01, READY) and CASE-005 (closed by its moves).
3. **Under O-1…O-3 the large figures (26, and 8 members with E residuals under O-2) are mostly the known class-choice residue.** These are the V, E and L rows the cases already list, and the other cases' moves were not applied. They do not show new coupling.
4. **U01 (G2b-M1) is the one large item outside ACT.** It is one invert.

**Answer to "coupled beyond what pair-by-pair rewording can economically close": robust only for DEL-04-01, and partly an artefact elsewhere.**
- **DEL-04-01.** It needs either one coherent ACT revision (§2.4–§2.8, §4.3/§4.6, §5, §6, §2.7, under the ACT51 pattern) or a decomposition of DEL-04-01: the act vocabulary its 20 consumers read, split from the binding, capture and resolution rules that reach into suppliers' artefacts. A decomposition is the owner's choice. It may well be the more economical route, given nine supplier pairs from one hub.
- **Everything else.** The coupling closes with about six agent-level rewordings (U01, TA-4, the C fixture, RELAY P8, A7, plus N13's M-01).
- **What the 16/26 headline mixes.** It combines the pre-move SCC-002, the class-choice residue and the ACT hub. It should not go to the owner as evidence of broad coupling.

### Minor findings and notes

| ID | Severity | Item |
|---|---|---|
| G2b-m1 | MINOR | U13 (09-12 → 11-03) should be read as not a dependency. PV owns its record and test, RP "adopts it at its next revision", and "matches" is alignment. That removes the {09-12, 11-03} cycle that G2b shows under O-3 and O-4 in its "+13 unclear" row |
| G2b-m2 | MINOR | EXP-R9 (U11, U12) should be resolved as GC-1 (b) supplier-side checking (not a dependency), or as V. Either way the effect is O-1 only |
| G2b-n1 | NOTE | 01-01 → 01-02: record the reason as ruling-carried (R17-3) with HOSTING's own text, not a bare cross-reference, since R17-3 also directs to DEL-01-02 |
| G2b-n2 | NOTE | The alias "ROLE" produces false matches on "ROLE ONE" in OBS-3. This affects use counts, not classification |
| G2b-n3 | NOTE | Not sampled: 232 of 251 "not a dependency" pairs, and the 9 rulings G2b lists as not read at source (I read R5-1 and R17-3, which support G2b's readings) |

## 6. Verdict

**READY as an inventory, with one correction before it is used at the owner checkpoint:** reclassify U01 as a dependency (G2b-M1).

- **Robust:**
  - the method;
  - the alias map's coverage;
  - the classification of the 62 (the flagged calls are correct in kind, and four are cheap to close);
  - the 19 "not a dependency" pairs I sampled;
  - every cumulative figure, as computed.
- **Not robust as an owner-facing message:** the headline "16 under O-2…O-4, 26 under O-1". It is a pre-move figure. After the cases' moves, the structural finding is **DEL-04-01 as a hub** (nine supplier pairs), plus U01, plus four small local cycles (G2b-M2).
- **For HELP_HUMAN:**
  - present the post-move reading;
  - put to the owner the choice between one ACT revision and a decomposition of DEL-04-01;
  - route U01, TA-4, the C fixture, RELAY P8 and A7 to their design agents as agent-level moves.

**Counts.** BLOCKING 0, MAJOR 2, MINOR 2, NOTE 3.
