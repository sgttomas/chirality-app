# RVG review of SCC-CASE-005 (SCC-004: DEL-07-01, DEL-07-02, DEL-08-01; O-D) — APP-V4-GRAPH-CLOSURE-20261004

- **Reviewer:** RVG, a Type 2 TASK executor (Claude Opus 5.5, `claude-opus-5-5`). No delegation. I did not author CFB, PRC, DRC or the analysis. O-D did, and says so. Read-only git, no network.
- **Subject:** commit `bb81cedb6a`; the commit adds files only:
  - `E/_DAG/cases/SCC-CASE-005/PAIR_ANALYSIS_2026-10-04.md`, sha256 `25321a1c2231ddf45f6bcb3a4cbc062cc104b51922fa95946987046a3c0dac38`;
  - `MOVES_PROPOSED_2026-10-04.csv`, sha256 `7f1664a67944c18df9a8abcb900921b2f156bea241dd6a731e3291a9bda19834`.
- **Read at source:**
  - CFB-v0.2 §3, §4, §6, §7;
  - `connector.standing.schema.json`, `connector.route-account.schema.json` and `pec.receiving-record.schema.json` (`$id`, properties, `$ref`s);
  - DEL-09-10 `CONNECTOR_WITNESS.md` §3;
  - R23-34 item 1;
  - `APP-V4-DESIGN-PASS-4-20261003/reviews/RV2-EUD1.md`.
- **Scripts:** `$TMPDIR/rvg/`.
- **Paths:** `E/` is `projects/chirality-app-v4/execution/`.

## 1. What holds

- **Arcs and kinds.** The component's four held arcs are all I under G1 r3: DEP-07-01-014, DEP-07-02-010, DEP-07-02-011 and DEP-08-01-009, with the mirror and same-arc rows as listed.
- **Whole-graph closure.** It reproduces under the case's own model:
  - S0 is 3 members under every option;
  - S1 is 3 members under O-1 and acyclic under O-2…O-4;
  - S2 leaves {07-01, 07-02} under O-1;
  - S4 leaves {07-02, 08-01} under O-2…O-4.

  No path through a non-member re-enters the component.
- **Projection artefacts, both pairs.** CFB §2–§5 define the vocabulary and the route, and depend on no DEL-07-01 or DEL-08-01 contribution. PRC §4 and DRC §4 emit CFB values. **Confirmed.**
- **R23-34 item 1** reads: "One standing vocabulary, defined in DEL-07-02 … DEL-07-01, DEL-08-01, DEL-09-10 and FV use it. It is built under SCC-CASE-005 R1, with no new row." This confirms both that DEL-07-02 owns the vocabulary and that GC-4 lists the right clause for amendment.
- **Rows not moved.** DEP-07-01-014 and DEP-08-01-009 are correctly left alone. Both are rule-bearing on CFB's vocabulary, and reversing them would be IV-O against R23-34 item 1.

## 2. The GC-1 (b) claim: holds

- **Supplier side.** `pec.receiving-record.schema.json` (`urn:…:del-07-01:pec-receiving-record:0.1`) `$ref`s CFB's `#/$defs/standing` and `#/$defs/conclusions`. The supplier therefore validates its own records against the consumer's vocabulary. That is GC-1 (b)'s "the supplier … checks it", along the existing arc DEP-07-01-014. DRC's record schema does the same.
- **Third party.** DEL-09-10's `CONNECTOR_WITNESS.md` §3 pass conditions check the standing directly:
  - (1) "the standing has the expected envelope and condition, with reasons";
  - (6) "each connector's standing equals its standing with the other connector's inputs removed".

  DEL-09-10 consumes DEL-07-02 through the admitted DEP-09-10-006 and DEL-08-01 through DEP-09-10-007. No new arc arises.
- **Consumer-side check.** DEL-07-02 VER-006's examination of an actual join is honestly kept as a **V** residual on the same arc.

## 3. Findings

### C5-M1 — MAJOR. The rewording leaves a runtime handover on both arcs, which is an E row under K-3. So the component does not close under O-2 or O-3

This is the same pattern as RVG-C2 B2-M1, which SCC-002 §23 accepted.

- **The rewording itself keeps the runtime flow.**
  - CFB §6's proposed row reads "Receives at runtime, by reference | DEL-07-01 | Receiving records".
  - The proposed DRC §8 says "Its receiving records reach DEL-07-02's route only by reference at runtime".
- **The source text keeps it too.**
  - CFB §4's trigger records "the receiving records that sent it".
  - DEL-07-01 REQ-005 has DEL-07-01 "connect the affected coordination question to the source-file route supplied by `DEL-07-02`".
  - AC-005 hands "the agent/manager/human responsibility" to DEL-07-02. The conditional S1 rewords that hand-over but keeps it.
- **How K-3 reads it.** The consumer, DEL-07-02, defines the format: the route-account trigger is CFB's schema. That makes each arc E, not removed. `dependency-extract` records information flow, and the hand-over is the purpose of the route. No S1 wording removes it without changing what DEL-07-01 REQ-005 and DEL-07-02 CLM-003 assign.
- **Computed** (whole graph, G1 r3 kinds, both moved arcs as E):

  | Option | Result |
  |---|---|
  | O-1 | 3 members |
  | O-2 | 3 members |
  | O-3 | 3 members |
  | O-4 | **acyclic** |

  With pair A as E and pair B removed: {07-01, 07-02} under O-1…O-3, and acyclic under O-4.
- **Consequence.**
  - "Acyclic under O-2 to O-4 with no owner act" holds for **O-4 only**.
  - Under O-1…O-3, two per-edge owner cuts are needed: DEL-07-02 → DEL-07-01, which also covers VER-006's V residual on the same arc, and DEL-07-02 → DEL-08-01.
  - Those are the **same two arcs** as the case's alternative M-ALT, the owner cuts of the I arcs without rewording. So under O-1…O-3 the rewording changes what is cut (a runtime handover, not an interface), not how many owner acts are needed.
  - Under O-4 it removes both.
- **Repair.**
  - In §5, record the E residual on both arcs.
  - Restate "what remains": O-4 nothing; O-1…O-3 two arc cuts.
  - Update the CSV's Residual and ClosesArcUnder columns for M-01 and M-02 (O-4 only; E residual).

### C5-m1 — MINOR. One proposed CFB §1 sentence would itself break GC-1 (a)

- **The sentence:** "It reads only the standing those records carry, in this vocabulary."
- **The problem.** The standing sits inside DEL-07-01's record structure: its top-level fields `response_standing`, `claims` and `conclusions` are DEL-07-01's schema properties, and only their values are CFB's `$def`s. Reading them means using a field DEL-07-01 defines. GC-1 (a) excludes that ("uses no field … that the supplier defines").
- **Current design reads no such field.** CFB §4's route account cites records by identity and says "Records the account cites keep their own standing". The trigger's `why` is a free string in CFB's own schema.
- **Repair.** Replace the sentence with: "It reads no field of a receiving record. The trigger (connector, why and record identities) is supplied in this file's route-account format by the connector owner that sends the question." With that, (a) holds, on the existing arc DEP-07-01-014.

### Notes

| ID | Note |
|---|---|
| C5-n1 | **"Your earlier EU-D1 review."** I did not review EU-D1. `RV2-EUD1.md` is RV2's, and it makes no SCC or inversion call on these pairs. Its EUD1-R2 (CS-R1 per connector; the standing schema refuses another connector's tier) is consistent with this case. My own earlier call on these rows is RVG-G1 G1-M2: DEP-07-02-010 and DEP-07-02-011 are both I, as here. That call is consistent |
| C5-n2 | Under O-1, VER-006's V residual and the E residual sit on the same arc, so one arc cut covers both. "Narrowing DEL-07-02 VER-006" (§5) would remove the V part but not the E part. It no longer suffices on its own to close O-1 |
| C5-n3 | The VER-001 extraction question (S1 against S2) no longer decides anything for pair B, because the E residual is present either way |

## 4. Verdict

**REPAIR (narrow: §5 and the CSV).** The artefact verdicts hold, as do the rewordings, GC-1 (b), the GC-4 entry for R23-34 item 1, and the rows deliberately left unmoved.

The closure claim must be restated:
- **O-4:** acyclic, with no owner act.
- **O-1…O-3:** two owner arc cuts (DEL-07-02 → DEL-07-01 and DEL-07-02 → DEL-08-01). These are the same arcs as M-ALT; what the cut reclassifies is a runtime handover.

Fix the CFB §1 sentence as in C5-m1.

**Counts.** BLOCKING 0, MAJOR 1, MINOR 1, NOTE 3.

---

## Addendum A — review of the CASE-005 repair, §8 (2026-10-04)

- **Subject:** commit `d9dcee38ff`.
  - `PAIR_ANALYSIS_2026-10-04.md`, sha256 `e9805802adc8329eb178f7c36f6a13fa39ea7e2bb2a23d0094db7d392912f134`. It is append-only: the diff from `bb81cedb6a` deletes nothing.
  - `MOVES_PROPOSED_2026-10-04.csv`, sha256 `618b0a48babda7bd81447659010589a725666108ea0857b3639b424fd7c6a2f7`, with M-01-R, M-02-R and M-03-R superseding M-01…M-04.

| Finding | §8 | Status |
|---|---|---|
| C5-M1, the E residual on both arcs | §8.1 records E on both arcs, and V as well on pair A | **Resolved.** The "no S1 removes it" reasoning is sound. DEL-07-02 OUT-001, REQ-001 and AC-001 (REQ-001 verified at source, l.44) assign the runtime showing and routing to DEL-07-02. Removing the receipt would move that obligation (S2) |
| C5-m1, the CFB §1 sentence | §8.2 now reads "reads no field of a receiving record". The trigger is supplied in CFB's own route-account format, and `trigger.standing` `$ref`s CFB's own `#/$defs/standing` | **Resolved.** The connector owners write CFB's format on the existing arcs DEP-07-01-014 and DEP-08-01-009, so GC-1 (a) holds for DEL-07-02. The remaining flow is cleanly E |
| Closure | §8.3 | **Reproduced.** R1 is 3 members / 2 rows under O-1…O-3 and acyclic under O-4. R3 is {07-01, 07-02} / 1 under O-1…O-3 and acyclic under O-4. Both match my C5-M1 figures. R2 (two arc cuts) closes everywhere |
| Owner acts | §8.3 and §8.4: O-4 none; O-1…O-3 two arc cuts (the M-ALT arcs), the first also covering VER-006's V | **Confirmed**, with C5-n2 and C5-n3 carried |

**ALT-DEC (new).** It closes on the stated conservative model, because the definition part depends on no runtime part. It is correctly labelled an owner-level decomposition, listed but not recommended.

**Verdict: CONFIRMED — READY.**

**Addendum counts.** BLOCKING 0, MAJOR 0, MINOR 0, NOTE 0.
