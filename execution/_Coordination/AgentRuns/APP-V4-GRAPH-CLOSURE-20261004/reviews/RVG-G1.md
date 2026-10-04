# RVG review of G1 and G2 — APP-V4-GRAPH-CLOSURE-20261004

- **Reviewer:** RVG, a Type 2 TASK executor (Claude Opus 5.5, model ID `claude-opus-5-5`), dispatched by HELP_HUMAN on 2026-10-04. No delegation. I did not author G1 or G2. Read-only git, no network.
- **Subject:** `SURVEY/G1.md` (sha256 `4e85ac7917178fcb4a87f3b481ac724d17deae9fe438df3c814a63879565973c`) and `SURVEY/G2.md` (sha256 `24cc2a6fcb00e466775647ce14590cb91914b6132aab6a441e79576c22efa87b`) at HEAD `c1d7eebb83`, clean tree.
- **Basis read, by sha256:** DAG-004 `CandidateEdges.csv` `2bfff10e…2fa42025`, `DependencyEdges.csv` `c4303374…90966e`, `ExcludedRows.csv` `45f55e76…65664e`, `GRAPH_BASIS.md` `21835c7b…aad79`, `SOURCE_MANIFEST.sha256` `03aa668b…3a8ef` (all equal to G1's and G2's recorded hashes); `docs/CYCLE_DRIVEN_RESOLUTION.md` `bbd41a8d…514f`; `workflows/project-dag/resources/graph-version.md` `ff6b7ba5…56bf`, `contract.md` `a55edc3b…d24d`, `method.md` (Stage 1, Checkpoint 1, Stage 3); `_DAG/DAG-001/BASIS_DECISION.md` `5a269b83…acb60`; all seven `_DAG/cases/*/Ruling_Register.csv`; the live `Dependencies.csv` files; the ScopeOfWork and Design passages cited below.
- **Paths:** `E/` is `projects/chirality-app-v4/execution/`.
- **Method.** I wrote my own scripts in `$TMPDIR/rvg/`; G1's scripts were not read or reused. SCCs came from Kosaraju, where G1 used Tarjan. The minimum cycle-closing sets came from a weighted subset DP, and I cross-checked them by an independent backtracking enumeration over the reciprocal pairs. Kinds were checked by reading each row's `Statement`, `EvidenceQuote`, `SourceRef` and `Notes` against the ScopeOfWork, and the Design where a design text bears on the call. "States" means what a file says; "I infer" marks my reasoning.

## 1. Computation: G1's numbers reproduce exactly

| Item | G1 / G2 | RVG recomputation | Agree |
|---|---|---|---|
| Arcs (consumer → supplier, DOWNSTREAM reversed) | 129 admitted + 83 held = 212 | 129 + 83 = 212; one row per arc; no arc in both layers | yes |
| Six SCC member sets | as `SCCRef` | Kosaraju over 212 arcs gives exactly the six `SCCRef` sets; no admitted arc inside an SCC; no held arc outside one | yes |
| Held rows per SCC | 2 / 71 / 2 / 4 / 2 / 2 | 2 / 71 / 2 / 4 / 2 / 2 | yes |
| Source rows incl. mirrors | 4 / 128 / 2 / 8 / 3 / 3 | Same, counting MIRROR and SAME_ARC rows on each held arc | yes |
| SCC-002 structure | 21 reciprocal pairs (42 arcs) + 29 non-pair arcs, acyclic among themselves | Same | yes |
| Minimum cycle-closing set | 1 / 21 / 1 / 2 / 1 / 1 | 1 / 21 / 1 / 2 / 1 / 1 | yes |
| SCC-002 distinct minimum sets | 609 | 609, by backtracking (one row per pair, remainder acyclic) | yes |
| SCC-002 "every" rows | DEP-02-01-019, -02-01-021, -03-01-031, -03-01-030, -04-02-008 | Same five; "none" rows within pairs: DEP-04-03-022, -04-03-023, -04-03-034, -05-02-005, -09-09-007 | yes |
| every / some / none for all 83 rows | §2 tables | 0 disagreements | yes |
| I–I pairs under G1's primary kinds | 11 (P1, P3–P8, P11, P15, P17, P21) | 11, same pairs | yes |
| Primary kinds of the 83 rows | I 50, E 15, V 12, L 3, P 3; kind × DependencyType as §1.2 point 5 | Same | yes |
| O-1 / O-2 / O-3 / O-4 under G1's kinds | 6 SCCs, 27 rows / 4, 21 / 3, 19 / 2, 12, with the members of §1.3 | Same sets and counts | yes |
| §2b single-item reach | N08, N26, N27 → 19; A2, A3 → 16; A7 → 14; A9 → {10-01…10-04}; N13 → {09-07, 09-11}; N22, A1 inside SCC-002 | Same (Tarjan-independent pass); `dag_reach.py --dag DAG-004` reports SCC-FORMING for all five G2 items | yes |
| §2b.2 option sets with all G2 rows | 5 / 4 / 4 / 2 components, with the 21-, 17- and 14-member sets | Same, using G1's 16 admitted-row kinds | yes |

**No computed number in G1 differs from mine under G1's own kinds.** The differences in §3 come from kind readings, not from arithmetic.

## 2. G2 checks

| Claim | Check | Result |
|---|---|---|
| Manifest 128/130; the 2 failures are DEL-01-03 | `shasum -a 256 -c` | 128 OK; DEL-01-03 `Dependencies.csv` and `_DEPENDENCIES.md` fail |
| 929 rows, 567 ACTIVE EXECUTION, 212 arcs | Script over the live registers | 929 / 567 / 212 |
| 211/212 matched | Seeded random sample of 20 arcs (seed 20261004), with the mention lines read at both ends | 20/20 have a Design statement naming the partner and the contribution (for example SQ I-10 for DEP-09-02-018; GUIDE X-12 for DEP-03-04-017; LHQ CI-5 for DEP-09-01-025; RS §10.1 and RRM for DEP-09-11-005) |
| Five SCC-forming items | `dag_reach.py` (sha256 `63259575…`) for N08, N13, N22, N26 and N27; controls N03 and N09 | All five SCC-FORMING, both controls "no cycle"; scope labels (merge into 19, new pair, inside SCC-002) agree with my Kosaraju pass |
| Joint check: 25 no-cycle rows plus A4, A5, A6 and A8 leave the six SCCs unchanged | Kosaraju over 212 + 29 arcs | Unchanged; none of the 29 duplicates an existing arc |
| Design citations | Read at source: ACCESS l.63 and the l.909–910 row; RS FR-13; DOS l.118 (N13); WD l.1792 (N22); EXEC l.2035 (N26); ADAPTER l.1446 (N27); NIR IF-11 l.206 (A1, A2); ACT §5.1 (A3); XT "ladder (CA §7.2)" (A7); DA l.138 (A9) | Each says what G2 and G1 quote |
| Arc ends named in their own Design | Count of full `DEL-xx-yy` strings in top-level Design files | 413 of 424 (G2: 416); see G2-n1 |

## 3. Findings on G1

### G1-M1 — MAJOR. K-3 classifies contract-maturity definition inputs as runtime evidence. O-4's figures rest on it

- **Evidence: what K-3 says.** K-3 makes runtime instances (events, entries, records, settings-in) **E** "even inside a 'consumes … does not define' list".
- **Evidence: the accepted maturity reading.** The rows require `INITIALIZED`, which DAG-004 `GRAPH_BASIS.md` reads as "defined-contract maturity only". G1 §1.2 point 4 draws the conclusion itself: the held rows "are about contract definition, not delivered artifacts". At that maturity, a consumer that "does not define" an instance format needs the supplier's definition of it before its own stated part. By K-2, that is **I**.
- **Evidence: the designs.** They show this directly for the RS consumer rows.
  - `RS_RECORD.schema.json` (DEL-04-03) states that "the bodies of the checkpoint entry kinds (EXEC CE-1…CE-19) are DEL-02-03's and are referenced by relative path to EXEC's `checkpoint-record-entries.schema.json`". It cites 10+ `$defs` there.
  - The same schema says "the settings_version body is DEL-04-02's, referenced by $id".
  - EXEC Changes row R14-1 says the same thing from DEL-02-03's side.
  - So DEP-04-03-025 (EXEC events → RS) and DEP-04-03-022 (settings-in → RS), both **E** in G1, are definitional dependencies of RS's format.
- **Evidence: the ScopeOfWork framing.** DEL-04-03 ScopeOfWork CLM-004 (l.55) lists everything the format owner "receives" in one sentence. The list mixes items G1 calls I ("the workflow identity tuple and the checkpoint disposition vocabulary", "subject content identities") with items G1 calls E (events, settings-in, entries, role-supply records). The text gives no basis for splitting them by noun class.
- **Consequence.**
  - Under G1's kinds, O-4 leaves a 10-member SCC-002 core with 11 rows to move.
    - With only DEP-04-03-025 and -022 read as I, the core is still 10 members, but needs 12 moves, and P12 becomes a 12th I–I pair.
    - With the whole RS receive list read as I, the core is 12 members (only DEL-09-09 leaves), with 13 moves. P9 and P12 join the I–I set, giving 13 pairs.
  - O-4's advantage over O-3 comes entirely from E. Its headline ("DEL-02-04, DEL-03-03, DEL-09-09 leave") is therefore not supported by the sources for the RS rows.
  - Early path C2, now analysing "the 11 I–I pairs", should take P9 and P12 into scope.
- **Repair.** Condition K-3: a row is E only where the consumer, or a third party, defines the format of the instances it receives. Where the consumer "does not define" them, the row is I. Re-run §1.3 and §2.2 with that rule, and state the sensitivity.

### G1-M2 — MAJOR. DEP-07-02-010 is classed L on point-of-need wording. Its sibling DEP-07-02-011 is classed I. SCC-004's option results depend on this

- **Evidence.**
  - DEP-07-02-010's quote, from DEL-07-02 ScopeOfWork TBD-001 (l.62), is "this deliverable defines the source route now and uses actual terms before dependent implementation/reliance". The contribution is "PEC receiving terms": response/tool contract, claim grain, and so on. Those are meanings consumed and not defined, so I by K-2.
  - "Before dependent implementation" names the consumer's part. Every row has one under the accepted part-level semantics. It is not one of K-6's phase or condition words ("for the governance phase", "when needed", "Once…", "later").
  - DEP-07-02-011 has the same structure: connector terms needed "when integrating the Domains-specific path". G1 keeps it I by K-1. Mirror DEP-07-01-015 reads as I (G1 §2.4).
- **Consequence.** Read consistently, both rows are I, or I/L.
  - SCC-004 then survives O-3 and O-4 whole: 3 members, 2 rows.
  - O-3's rows to move become 20, not 19, and O-4's become 13, not 12 (15 together with G1-M1).
  - G1 §1.3's "the choice decides five of the six SCCs" becomes four of six: SCC-001, 003, 005 and 006.
  - Case #9's note "If the owner prefers the Statement's condition (L), SCC-004 dissolves under O-3" shows the result turns on this one call. The owner should see the call itself, not only its outcome.

### G1-M3 — MAJOR. O-2…O-4 are described as objectives but realised only as cuts on held rows. Their consequences and costs are understated

- **Evidence: what the doctrine says about objectives.**
  - Doctrine §2 rule 1 says to fix the objective and semantics "before drawing edges".
  - Its §3 guardrail applies the method "per objective + edge semantics".
  - Rule 2 says "An edge in no cycle needs no adjudication".
  - So an objective that excludes verification, later-use or evidence edges excludes them everywhere. A cut (rule 3) is a per-edge move on a cycle-closing edge.
- **Evidence: what §1.3 does.** It realises O-2…O-4 as "Owner SR-4 cut rulings on 12 [15, 30] rows", all held. That is an objective change applied only where it closes cycles.
- **Evidence: the admitted layer would also change.** G1 classified 16 admitted rows in §2b.2 and found 7 E and 1 V among them. A keyword pass over all 129 admitted rows finds up to 62 V-like and 39 E-like statements. That pass is an upper bound, not a classification. 45 admitted arcs have a PKG-09 consumer.
- **Evidence: PKG-09.** For DEL-09-09 ("External control and catalog-extension trace") and DEL-09-11 ("Later run reconstruction witness"), the trace or witness is the deliverable's own output:
  - DEL-09-11 OUT-001 "TEST: a candidate-bound V4-EXM-31 reconstruction witness";
  - DEL-09-09 OUT-002, the V4-EXM-24 trace document.
  - Under O-2, as K-5 is written, their production inputs leave the build order.
- **Evidence: the "Rows to move" column.** It counts moves left after the option. It excludes the option's own cut rulings, which are themselves doctrine moves. O-4 is 30 owner cut rulings on held rows, plus the admitted-layer cuts, before its 12 remaining moves. O-1's minimum is 27 moves. O-6 shows "0" but is six merge rulings.
- **Consequence.** An owner comparing 27 against 12 is not told that O-4 is the larger owner act, or that it changes the admitted DAG. The owner's criterion is that "the DAG won't change". Nor is the owner told that O-2 unorders PKG-09's witnesses against what they examine.
- **Repair.**
  1. State that a kind-based objective applies to admitted rows, and give at least a bounded count of them.
  2. Add the cut and merge rulings to the per-option workload.
  3. State the PKG-09 consequence under O-2.

### G1-M4 — MAJOR. The "reopens CP1-20260928" label is attached asymmetrically, and "O-1 with moves" is mostly cuts

- **Evidence: what CP1 decided.**
  - CP1-20260928 (all seven `Ruling_Register.csv`) and `DAG-001/BASIS_DECISION.md` confirm "full required-contribution/default SR-1…SR-7 selection". They carry the SCCs "for later/post30 work".
  - The default rules include SR-4: "Arcs not cut by a recorded human ruling" (`graph-version.md`).
  - "No cut or formal graph merge group was accepted" records that act. It does not bar later rulings.
- **Evidence: what project-dag allows.**
  - A per-arc cut recorded in a case `Ruling_Register.csv` operates within the confirmed default rules.
  - Re-deciding the objective text is a normal checkpoint-1 element of a successor ("Reopened decisions create successors"; DAG-004's own "Reopened decisions (checkpoint 1, limited to these)").
- **Evidence: what G1's own O-1 path proposes.**
  - G1 §2's candidate moves under O-1 are mostly cuts of V, L and E rows.
  - Cut is the primary candidate in four of the five small SCCs: DEP-01-01-024 (V), DEP-09-01-016 (V), DEP-10-02-012 (L) and DEP-11-03-015 (E). SCC-004 offers invert or cut.
  - In SCC-002, cut is primary for P2, P13, P14, P16 and P18, and an alternative for P3, P9, P10, P12, P19 and P20.
- **Consequence.**
  - §1.3's framing contrasts narrowing by kind ("cut rulings, which reopen CP1") with "keeping every kind and using decompose or invert (O-5, or O-1 with moves)". It tells the owner that O-1 preserves the accepted basis.
  - Yet O-1 as G1 populates it is largely kind-based cuts applied to cycle-closing rows only.
  - Both paths encode the same subjective interpretation. The real difference is class-wide against per-edge, and whether the narrowing is applied consistently (G1-M3).
- **Answer to the brief's question.** A kind-narrowed objective is realisable through project-dag in three ways:
  - per-arc SR-4 cut rulings, recorded with evidence;
  - an objective restatement at DAG-005 checkpoint 1;
  - a checkpoint-1 selection-rule adjustment. Such a rule can act only on recorded row data, and no kind field exists.

  SR-3 cannot do it (G1 is right). Narrowing re-decides the "full required-contribution" basis at the successor's checkpoint 1. That is expected for DAG-005, and it applies equally to per-edge cuts that reclassify edges as out-of-objective.

### Minor findings on G1

| ID | Severity | Finding | Evidence | Consequence |
|---|---|---|---|---|
| G1-m1 | MINOR | K-1 departures, all toward V or E. Six rows are decided by Statement although their quote is unique in the register, not "generic": DEP-04-03-035 (E), DEP-03-01-026 (V), DEP-09-09-007 (V), DEP-04-02-008 (E/V), DEP-09-09-008 (V) and DEP-09-09-009 (V) | Quote-sharing count over the live registers. The six rows decided by ST that pass K-1 are DEP-02-02-013, -014, -015, DEP-02-01-020, -021 and DEP-09-09-022 (shared by 2–3). DEP-09-09-007's quote alone ("operation/catalog contract and model basis") reads as I | K-1 and K-5 conflict. K-5 needs the point of need, which sits in `SourceRef` or the Statement, not the quote. State the precedence (for example "quote decides content; SourceRef/Statement decide point of need"). No SCC count changes, because DEL-09-09's only incoming held arc, DEP-03-01-030, is V either way |
| G1-m2 | MINOR | K-5 is too broad for deliverables whose output is the examination, witness or trace. It is right for DEP-09-01-016: DEL-09-01 VER-008 verifies its own OUT-004 harness. It is wrong for DEP-09-11-006, an admitted §2b row: DEL-09-11's OUT-001 is the witness, so the journey evidence is a production input, P by K-4. The same applies to DEP-09-09-007, -021 and -022, whose point of need is DEL-09-09's own trace (`SourceRef` CLM-002/REQ-001, not VER) | DEL-09-11 ScopeOfWork l.33; DEL-09-09 ScopeOfWork l.56–57; DEL-09-01 ScopeOfWork l.58, l.92 | With DEP-09-11-006 as P, N13's SCC {09-07, 09-11} persists under O-1…O-4. G1 §2b reading point 4 says "only under O-1". The rule should exclude points of need that are the consumer's own OUT |
| G1-m3 | MINOR | N27 is classed E, yet G1 itself calls it a "design-time join supplying observations". ADAPTER §11 supplies "Observed MCP/dynamic-tool facts … for the classification R4-12 assigns to HOSTING". These are facts used to produce the consumer's classification, so P or I by K-4/K-2 | ADAPTER l.1446 | §2b.2's last row ("O-4, with N26 not entered … The G2 rows then add nothing") fails. With N27 as I, the O-4 core is 14 members (adds 01-01, 01-02, 01-03, 03-03). "None of the ten is a production input" is contestable for N27 |
| G1-m4 | MINOR | "Partial cut" is not a graph move. P3 offers "its governance-phase hold-support part … could be cut separately". SR-4 cuts arcs, and a row that is split stays on the same arc (SAME_ARC) | `graph-version.md` SR-4, SR-6 | It should not be offered as a cycle-closing option. Only the whole arc's cut or invert closes P3 |
| G1-m5 | MINOR | P5 "re-target to DEL-04-01" conflicts with the row's own Notes: "this row consumes record semantics separately from DEL-04-01 distinctions". DEP-02-01-018 (admitted) already carries the DEL-04-01 distinctions | DEP-02-01-019 Notes; DEP-02-01-018 Statement | The re-target would merge two obligations the register owner kept distinct. Flag it for the owner of DEL-02-01's register; the cycle safety itself is right (DEL-04-01 has 0 suppliers, verified) |
| G1-m6 | MINOR | DEP-10-02-012's cut rationale cites the condition having occurred (DAG-004 accepted). That makes the use current, not later. The loop is version feedback: DAG vN selects work whose records feed DAG vN+1. This is the pattern G1 itself identifies for SCC-006 | DEL-10-02 ScopeOfWork REQ-001; G1 §2.5, §2.6 | Restate the rationale as version feedback, so the owner rules on the real basis |
| G1-m7 | MINOR | §1.2 point 5's alternative, "a new register field that `dependency-extract` fills", is a workflow and SPEC change | AGENTS.md: "Instruction changes require their own authorized scope" | Not stated as such. The owner should see that this route needs its own authorized instruction change |

### Notes on G1

| ID | Severity | Note |
|---|---|---|
| G1-n1 | NOTE | The finding "SCC-002 needs invert, decompose or merge under every kind option" is robust in direction, and G1-M1 strengthens it (11 → 12 or 13 I–I pairs). The exact pair set is conditional on K-3 and on K-6's whole-row test. If every X/L row were primary L, O-3's core would be 12 rows to move with a different shape. Say that the count is conditional |
| G1-n2 | NOTE | Kind calls I checked and agree with: all 12 rows of SCC-001 and SCC-003…006 except DEP-07-02-010 (G1-M2). All 22 rows of the 11 I–I pairs. The boundary rows DEP-02-02-013 (I), DEP-07-02-011 (I/L), DEP-04-02-018 (E/I; defensible, and as I it adds 1 move to O-4), DEP-01-04-024 (E/I; as I, DEL-02-04 stays in the O-4 core, 11 members) and DEP-09-09-023 (E/L; any of E, V or P, with no SCC effect). 30 further rows: DEP-01-04-023, -02-03-027, -02-02-017, -04-03-035, -02-03-026, -03-03-014, -02-03-013, -04-03-025*, -02-03-022, -05-01-017, -03-01-026, -03-02-016, -04-02-008, -04-03-022*, -09-09-007†, -09-09-008†, -09-09-009†, -09-09-011, -09-09-021†, -09-09-022†, -03-01-030, -05-01-025, -04-03-028*, -05-01-019, -04-03-036*, -04-03-024*, -04-03-026*, -03-03-017, -05-02-020 and -02-03-025. * = disagreement under G1-M1; † = G1-m1/m2. G2 §2b items: N08 (I), N22 (V), N26 (I/R), A1, A2, A3 and A9 (E) agree. N13 is I, but its return path disagrees (G1-m2). N27 disagrees (G1-m3). A7 (I, boundary V) agrees |
| G1-n3 | NOTE | Options missing: none of substance. Per-SCC mixed moves are O-1 with moves. A graph-only merge group (SR-4 `MERGE_GROUP_INTERNAL`, no decomposition change) is covered by O-6's text. Version nodes for feedback loops (SCC-005, SCC-006) belong under O-5 and could be named there |
| G1-n4 | NOTE | Citations checked at source and correct: GRAPH_BASIS l.23–25; DAG-001 l.11; HANDOFF_STATE reading rule 5; CP1 text in all seven `Ruling_Register.csv`; EXEC R14-1; DEL-04-01 has 0 suppliers; every SCC-002 member except DEL-02-04 consumes DEL-04-01 (admitted) |

## 4. Owner-facing fairness (G1 §1.3)

- **Would a reader be steered?** Yes, in two opposite directions.
  - The "Rows to move" column (27 for O-1, 12 for O-4) favours narrowing, because it leaves out the option's own cut rulings (G1-M3).
  - The "reopen CP1" label, attached only to O-2…O-4, disfavours it (G1-M4).
  - Neither effect is deliberate. Both should be repaired, not left to cancel out.
- **Is "no option recommended" justified?** It is justified as to the choice itself: the doctrine reserves cut and merge, and an objective-dependent interpretation, to the owner. The sources do, however, settle more than G1 says on two points:
  - The accepted maturity reading, together with the RS and EXEC schema evidence, weighs against treating E rows as runtime handovers (G1-M1). As recorded, the held rows are contract-definition requirements.
  - The doctrine's own cut examples ("runtime/test/optional") support V-type cuts as a class, but rule 1 requires a class cut to apply to the whole graph (G1-M3).
- **What the owner should get.** G1 should present this to the owner as: a choice of which classes the objective excludes graph-wide, with the admitted consequence shown, against per-edge moves on cycle rows. It should not present it as narrowing against preserving the basis.

## 5. Findings on G2

| ID | Severity | Finding | Evidence | Consequence |
|---|---|---|---|---|
| G2-m1 | MINOR | Matching is partly circular. At least 15 Design files rebuild their receiver or supplier sections from the register rows, for example "Receivers (from the live register rows…)" and "rebuilt from the ACTIVE register rows". This includes most SCC-002 members (HOSTING, NPTD, WD, C, P, ADAPTER, EXEC, ACT, AS, RS, LOOP, PANEL, CA, XT, GUIDE). DEL-04-01 ACT lists DEP-06-02-009 and DEP-09-02-018 as "Not mapped in detail" | grep over `E/PKG-*/1_Working/DEL-*/Design/*.md` | "Register rows the Designs no longer support: 0" cannot be read as independent design support for rows these files copied. The finding direction "Design relationship missing from the register" is unaffected. §8 should state this limit |
| G2-n1 | NOTE | Arc ends named in their own Design by full ID: 413 of 424, against G2's 416. The 11 include 4 named by short form (`09-05`, `02-02`) and DRC naming DEL-05-01 as "LOOP" | Script count | G2 probably counted aliases. There is no effect on the matched count, which allows either end |
| G2-n2 | NOTE | All other G2 checks reproduce (§2 above), including the reach of the five SCC-forming items, the joint check and the Design citations. §7's "+25 arcs" balances: 24 consumer rows plus the N18 retarget | — | — |

## 6. What this review leaves untested

- The kinds of the 113 admitted rows G1 did not classify. My 62 and 39 are keyword upper bounds only.
- The 57 SCC-002 mirror rows and 12 others.
- Whether invert is acceptable to the deliverable owners for any pair.
- Whether part-level orders exist for SCC-002.
- G2's 25 non-SCC-forming items beyond reach. I did not re-read their Design sentences, only the five SCC-forming items and A1, A2, A3, A7 and A9.
- The 609 minimum sets were counted, not inspected.

## 7. Verdicts

- **G1: REPAIR.** The computation is exact and fully reproducible, and it is usable as is. The shared basis is not ready to go to case agents or the owner. Repair requires:
  1. condition K-3 on who defines the instance format, and limit K-5 to points of need that are not the consumer's own OUT (G1-M1, G1-m2);
  2. reconcile DEP-07-02-010 with DEP-07-02-011 (G1-M2);
  3. re-run §1.3, §2.2 and §2b.2 under the repaired rules, with the sensitivity stated;
  4. restate O-2…O-4 as graph-wide objectives, with the admitted-layer and PKG-09 consequences and the full ruling workload (G1-M3);
  5. make the CP1 framing symmetric (G1-M4).
- **G2: READY.** It is usable as the basis for the owner checkpoint and the register work. Add the circularity limit (G2-m1) when it is next touched.

**Counts.** BLOCKING 0, MAJOR 4, MINOR 8 (G1 7, G2 1), NOTE 6 (G1 4, G2 2).

---

## Addendum A — confirmation of G1 r2 (2026-10-04)

- **Subject.** `SURVEY/G1.md` r2, commit `c0a892137a`, sha256 `8afa6093cbd0f09dccc6ef53e1a0c6fb35efbbe17729f5b0ca0407792ffcfc61`.
- **Read.** §1, §2.2 and §2b in full, §3.1 and §6, with the kinds of all 212 rows parsed from §2 and Appendix A.
- **Same reviewer, same constraints.** Read-only. My own scripts in `$TMPDIR/rvg/` (`r2.py`, `r2opts.py`).

### A.1 What I confirmed

- **Repair map.** §6 maps every finding of this review to a change, and each mapped change is present in the body.
- **Kinds as parsed.** Held: I 71, V 5, P 3, L 3, E 1. Admitted: I 85, P 39, L 3, E 2, V 0. The 23 held kind changes from r1 are exactly those §6 describes.
- **Whole-graph option table (§1.3).** It reproduces exactly from my code over all 212 arcs with the r2 kinds:

  | Option | Arcs leaving (held + admitted) | SCCs | Moves | Interface or production | V/L/E |
  |---|---|---|---:|---:|---:|
  | O-1 | 0 + 0 | 6 | 27 | 19 | 8 |
  | O-2 | 5 + 0 | 4 | 22 | 19 | 3 |
  | O-3 | 8 + 3 | 2: 002 (12), 004 (3) | 20 | 19 | 1 |
  | O-4 | 9 + 5 | 2 | 19 | 19 | 0 |

  The three admitted arcs leaving under O-3 are DEP-06-01-011, DEP-07-02-015 and DEP-10-01-020. O-4 adds DEP-02-04-013 and DEP-09-12-012. The 17 I–I pairs are as listed.
- **The four new pairs' deciding sentences**, checked at source:
  - **P10 (DEP-02-03-026).** ADAPTER owns `checkpoint_observation.schema.json`, which has no external `$ref`, and EXEC l.1255 creates arrivals from it. The supplier defines the format, so I.
  - **P18 (DEP-04-02-008).** The SourceRef includes CLM-002 as well as VER-002 and VER-004. The lapse vocabulary is RS §7. I/V under the K-1/K-5 precedence.
  - **P19 (DEP-04-02-018).** `LOOP_DESTINATION_REQUEST.schema.json` is LOOP's, and AS §3.1 takes the request states from "DEL-05-01/LOOP-v0.8 §5.3 DF-5 and DF-6". I.
  - **P20 (DEP-04-03-028).** RS's destination bodies are RS's own, but their state values are LOOP DF-6's (schema description "LOOP-v0.8 §5.3 DF-6"). The consumer does not define the meanings it records, so I.
- **No over-correction of E.** The three remaining E rows each pass r2's own test:
  - DEP-02-03-022: EXEC §9.1 *supplies* DEL-05-01 "the current-phase recorder (§2.4), whose event meanings LP-3 shares", so the consumer defines both format and meaning;
  - DEP-02-04-013 and DEP-09-12-012 go into the consumer's existing interfaces.

  The rows that became I each have a supplier-side definition, a schema `$ref` or a cited meaning. The rule now amounts to "E only where the consumer defines both format and meaning". At INITIALIZED that is the defensible reading, and §1.3 states its consequence: O-4 differs from O-3 by one cycle-closing row.
- **No admitted V.** A SourceRef scan finds one admitted row whose only cited point of need is VER: DEP-06-01-007, "when implementing and exercising". K-5's exception makes it I. Consistent.

### A.2 Findings on r2

| ID | Severity | Finding | Evidence | Consequence |
|---|---|---|---|---|
| G1r2-M1 | MAJOR | **A2 and A3 are still E, and Q-5 is still cited as an owner decision, against r2's own K-3.** ACT §5.1 "Inputs (semantic)" takes "*grant state* for the class" from "DEL-04-02 (R-8; R2-6)", listing AS §3's seven states, and "*checkpoint state*" from DEL-02-01, DEL-02-03 and DEL-05-01. §5.3 rule 7 is rule-bearing on the grant states. ACT does not define them, so r2's K-3 makes A3 I. §2b (l.421, reading point 3) says A2 and A3 "contradict an accepted owner decision (Q-5)". The owner's Q-5 is "the App act control in DEL-01-04, with REQ-008 as adjusted …" (`APP-V4-SCA003-20261002/OWNER_DECISIONS.md` l.53). "DEL-04-01 gains no supplier" describes that one adjustment (DISPATCH P2-A); it is not an owner rule. My original review accepted that framing without checking it | Read with A3 as I, the grant-state input alone forms an SCC containing DEL-04-01: 15 members under O-4 and 16 under O-1 (r2 kinds, computed) | §2b.2 understates the exposure, and §2b reading point 3 misattributes authority. This is also the premise of C2's four re-targets (RVG-C2 C2-M2). Repair: classify A3 by K-3 (I for the grant-state and checkpoint-state inputs), state Q-5's actual scope, and add the A3-as-I line to §2b.2 |
| G1r2-m1 | MINOR | DEP-06-01-011 is L by the deciding sentence "before relying on that changed consumer path". r2's K-6 says "before … reliance" wording names the consumer's part and does not make L | Appendix A l.620; §3.1 K-6 | If the intended condition is the row's "A proposed format change shall …", cite that and say why it governs the whole row. Otherwise the row is I or P, and the admitted arcs leaving fall to 2 under O-3 and 4 under O-4. No SCC effect |
| G1r2-n1 | NOTE | K-3's text exempts DEL-04-03's whole CLM-004 list by blanket. Per item, the design test agrees: EXEC (19 `$ref`s), DEL-04-02 (`$ref`), LOOP (DF-6 cited), ROLE (§6.3 cited), ADAPTER (`external_dispatch_record.schema.json`) and WR (ID-3 string). I did not check DEP-04-03-024 (DEL-03-02 outcomes) | — | Replace the blanket with per-item bases, so case agents apply the test rather than the exemption |
| G1r2-n2 | NOTE | The "19 interface or production rows under every option" are exact minima under the r2 kinds. C2's analysis shows that most can be closed by agent moves, under conditions RVG-C2 sets out. The owner should read the 19 as the count of design moves, not of owner rulings | RVG-C2 | Presentation only |

### A.3 Verdict on r2

**REPAIR (narrow).** The computation, the four new pairs, the option table, the admitted-arc lists and the r2 rules are sound and consistently applied, with the one exception of A2/A3 in §2b (G1r2-M1).

The owner checkpoint can use §1.3 and §2 as they stand. Before G1 goes to the owner as a whole, §2b's treatment of A2/A3 and of Q-5 must be corrected, because it concerns how an owner decision is presented to the owner. The fix is local: §2b.1 rows A2 and A3, §2b.2 with an A3-as-I line, and reading point 3. G1r2-m1 can be fixed in the same pass.

**Addendum counts.** BLOCKING 0, MAJOR 1, MINOR 1, NOTE 2.
