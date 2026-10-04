# RVG review of ACT51_ANALYSIS (SCC-CASE-002, ACT §5.1; O-A) — APP-V4-GRAPH-CLOSURE-20261004

- **Reviewer:** RVG, a Type 2 TASK executor (Claude Opus 5.5, `claude-opus-5-5`). No delegation. I did not author ACT, AS or the analysis. Read-only git, no network.
- **Subject:** commit `10f4dd3444`:
  - `E/_DAG/cases/SCC-CASE-002/ACT51_ANALYSIS_2026-10-04.md`, sha256 `88823b1a7e0c4c8fa4e21194ad2d7bf04f039e64e6aa6ff2c1684d76bdc94c45`;
  - `ACT51_MOVES_2026-10-04.csv`, sha256 `5f40970475a8560170bcd98365b3593620872bbb0edd49a64de7dd35b48dc038`.
- **Read at source:**
  - ACT-POLICY-v0.11 (sha256 `597f13bd…`): §2.4–§2.6, §2.8 and §5.1–§5.4, plus a per-section count of its citations of sibling Designs;
  - AS-v0.9 §2–§3;
  - R-3, R-5 and R-7 (`R1_RESOLUTIONS.md`); R4-6 and R4-7 (`R4_RESOLUTIONS.md`); R8-1 and R8-11 (`R8_RESOLUTIONS.md`); R9-1 and R9-2 (`R9_RESOLUTIONS.md`).
- **Scripts:** `$TMPDIR/rvg/`.
- **Paths:** `E/` is `projects/chirality-app-v4/execution/`.

## 1. What holds

- **The closure tables reproduce exactly.** I used the SCC-002 §23 model (C, with the five E residuals) and held admitted arcs fixed.

  | ACT §5.1 input added as I | O-1 | O-2 | O-3 | O-4 |
  |---|---|---|---|---|
  | Reworded (no row) | DEL-04-01 in no SCC | same | same | same |
  | Operation identity | 15/11 | 2/1 | 2/1 | 2/1 |
  | Grant state | 15/11 | 13/6 | 13/6 | 12/1 |
  | Checkpoint, DEL-02-01 only | 15/11 | 4/1 | 4/1 | 4/1 |
  | Checkpoint ×3 | 15/13 | 13/8 | 13/8 | 11/3 |
  | All five | 15/15 | 13/10 | 13/10 | 12/5 |
  | P §3.3 as L | 15/11 | 3/1 | acyclic | acyclic |

  DEL-04-01 has 20 admitted consumers and no supplier.
- **Kinds today.**
  - Grant state is I: ACT's rule 7 is rule-bearing on AS §3's states.
  - Checkpoint state is I ×3.
  - P §3.3 is L.
  - Operation identity is I by text only, and already meets GC-3 conditions 1–2 in the schema.
- **The operation-identity rewording** is the smallest and is sound: the identifiers are uninterpreted, compared whole, with their resolvers named, and the `kind` enumeration is ACT's own.
- **The fallback analysis** is right: a refused input needs an owner act under every option. "Registering as E" is worse than no row, because E sequences under O-1…O-3.

## 2. The standings: genuine inversion or relabelling? (N13 tests)

| Test | Grant standing | Checkpoint standing |
|---|---|---|
| **(i) Own terms** | **Yes.** "Direct in force" is built from grant value, scope and A12. AS §2 receives exactly these "from DEL-04-01 §5 and §8". The *established* control relation is anchored on R4-6 (below), not EXEC. "Default in force" and "unassigned" are ACT's §8 terms | **Not yet.** "open arrival … not yet *performed* in §4.3's sense" ties the value to ACT §4.3. §4.3 adopts WD §4.3.7 and EXEC's disposition rules "by citation" (F-14), and R4-7 itself directs that "WD §4.3.7 adds MX-3, MX-6, MX-8". So ACT would still evaluate *performed* by WD's and EXEC's rules |
| **(ii) Grounding in basis** | **Yes.** R-3 (owner DEL-04-01): "A request to apply directly without an effective *direct* treatment → **not permitted**". R-8: "The direct branch applies only in the **effective** direct state". R2-6 adds the default rule. Each is ruling text, not Design | **Partly.** The R-5 text carries reached-when kinds and the six dispositions. R8-1 makes `governed` "a new optional declaration flag in WD", so DEL-02-01 mapping `governed` onto ACT's *binding* agrees with R8-1. R9-1 and R9-2 keep the request with the agent and the recording with the product |
| **(iii) Change direction** | **Right way.** A new AS display state needs only AS's "Direct branch?" column; ACT is unchanged | **Wrong way, as worded.** A change to WD §4.3.7's item rule changes what ACT's *performed* means |

**Verdict on the standings.**
- **Grant standing is a genuine inversion.**
- **Checkpoint standing becomes genuine only with one change: ACT-m1 (MINOR).** Define "open arrival requiring ⟨act⟩" as a value **reported by the executor under its own disposition rules** (R-5's *waiting*), not as ACT's own evaluation of §4.3. ACT then reads a value it does not compute. Otherwise this rewording depends on §6's §4.3 re-anchoring, which, as A.4 shows, cannot be done for the R4-7 item rules.
- **Precondition.** Both standings rely on ACT §2.4/§2.5's A12 relation being anchored on R4-6, not EXEC §4.10. That is §6 row 1.
  - R4-6's text does carry it: "A refused A12 does not count … A pending A12 leaves the checkpoint *waiting*. A lost confirmation makes it *unknown*".
  - EXEC §4.10 (the case for P11's invert) cites the same ruling.
  - The two files must then both cite R4-6 as the source. Neither should claim the other's ownership.
- **"Requested by agent" conflict.** It is correctly flagged as a design reading. AS's reading matches R-8 ("A8; no person act").

## 3. "No E residual" for the §5.1 inputs: sound

- **DEL-04-01 is a contract** (ScopeOfWork l.16 "API_CONTRACT"; CLM-001 artefacts). It has no reader or writer.
- **Treatment is resolved on the host route.** R-3 point 1 is verified at source: "The loop and the external adapter relay the actor's intent and do not decide treatment". AS §2 adds "Governs host operations only".
- No App component therefore receives grant, checkpoint or operation instances on DEL-04-01's behalf. This matches SCC-002 §23.1's P4 reasoning.
- **The one limit is real, and correctly flagged.** DEL-04-01 REQ-007's "receiving attributable evidence" is a stated receipt in DEL-04-01's **own ScopeOfWork**, so a default `dependency-extract` run could extract it. Against DEL-01-04 (G2 A2) it forms a cycle with admitted DEP-01-04-011 under O-1…O-3. It needs its own disposition (ACT-M1 (b)).

## 4. Wider exposure (§6): not bounded by the inventory

### ACT-M1 — MAJOR. ACT relies on more sibling Designs than §6 inventories, and the re-anchoring remedy works only where a ruling carries the content

**(a) The inventory is incomplete.** A per-section count of ACT's citations of sibling Designs (EXEC, WD, LOOP, AS, RS, P, C, ADAPTER, AAC/NIR, HOSTING, PANEL, WR, RECOVERY), outside its Changes history, finds them in 26 sections. Among those §6 does not list are uses that are rule-bearing or definitional, for example:
- **§2.4 and §2.5.**
  - "The lapse-state vocabulary is DEL-04-03's".
  - A16 "Lapse-evaluated as an App file (RS L-1, L-6)".
  - A15's bound content is "WR ID-2" and "RS-v0.9 §6.1".
- **§2.6.** Capturing surfaces "designed in DEL-01-04/AAC-v0.2"; EXEC CAP-1…CAP-3.
- **§2.8.** "RS-v0.8 §3 gives the states of a written entry".
- **§4.7 RC-3.** AAC and EXEC CAP-2.
- **§4.6.** EXEC §3.6 hold-support values (L, governance phase).

Each of these suppliers consumes DEL-04-01 through an admitted row. Computed on the same model:

| Added as I | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| DEL-04-01 → DEL-04-03 (RS lapse) | 15/11 | 13/6 | 13/6 | 9/1 |
| DEL-04-01 → DEL-01-04 (AAC) | 15/11 | 14/6 | 14/6 | 13/1 |
| DEL-04-01 → DEL-02-02 (WR ID-2) | 15/11 | 7/1 | 7/1 | 7/1 |

So "DEL-04-01 gains no supplier" holds today only because none of this is in a ScopeOfWork or register. §6's own "Consequence" paragraph says this, but the exposure is wider than its table.

**(b) Re-anchoring: a real fix only where the ruling carries the content.** Checked at source:

| Ruling | What its text carries | Re-anchoring |
|---|---|---|
| R-5 | The six dispositions and the reached-when kinds | Real |
| R4-6 | The A12 effects | Real |
| R-3 point 2 | The four non-success values with their meanings | Real |
| R-7 | Only "P §9 is the canonical … taxonomy", without the list | Would **hide** the dependency. O-A says so ("may need amendment"). Correct |
| R4-7 | Directs that "WD §4.3.7 adds MX-3 … MX-8", so the content is WD's | Would **hide** the dependency |
| §2.4/§2.5's RS and WR uses; §2.6's AAC | No ruling carries the lapse vocabulary, the WR identity or the capturing-surface design | Cannot be re-anchored. These need invert (the supplier maps onto ACT terms), GC-3 opacity, or an owner act |

- **Test to adopt:** re-anchoring is a fix exactly when the ruling's own text states the rule or vocabulary, so that a change can only come by amending the ruling (GC-4). Where the ruling points to a Design, re-anchoring is a relabelling.

**(c) Consequence beyond this case.**
- G2 matched relationships by `DEL-` ID and section labels, and its §8 states the limit: "a relationship stated only in prose, without a `DEL-` ID or a section's own label (for example 'RS R3' with no ID), could be missed". ACT shows that limit is material.
- Sibling Designs cite one another by abbreviation throughout, as RVG-G2's circularity note also observed. The 60% premise, "the DAG won't change", therefore needs either:
  - an abbreviation-aware scan of all 55 Designs, mapping EXEC→02-03, RS→04-03 and so on; or
  - an integrator ruling on whether a Design's citation of a sibling Design, not stated in either ScopeOfWork, is a dependency for the graph. The `dependency-extract` default (ScopeOfWork as source) implies it is not. G2's method and N13 (O-C §4: "A missing ScopeOfWork sentence is not a reason to keep the relationship") imply it is.
- I recommend HELP_HUMAN rules on this (a GC-5) before the case work is integrated, because every case's "no new row" conclusion depends on it.

## 5. The unread rulings, checked

| Ruling | What it says (verbatim, at source) | Effect on the analysis |
|---|---|---|
| **R8-11 item 5** | "Fixture values read as if governed. The governance-phase values on X read the fixture's checkpoints as if they were governed. Say so where the values are stated." | **Mis-cited.** It is about fixtures, not about who owns `governed`. The ruling that allows §2.2's AP-10 rewording is **R8-1**: "A workflow opts in by declaring its checkpoints **governed**, a new optional declaration flag in WD … Phase 1 honours the flag only as guidance. The governance phase enforces it." That supports DEL-02-01 mapping `governed` onto ACT's *binding* (ACT-m2) |
| **R8-11 item 2** | Reserved acts bind; a declared checkpoint is guidance in Phase 1, binding "only for governed checkpoints in the governance phase" | Consistent with checkpoint standing's *binding: yes/no* |
| **R9-1** | The agent carrying out the workflow requests the act. The product gives the agent the checkpoint, offers the means, and records; neither the App nor the loop reacts | Consistent. The rule 2 rewording must keep "request the person's act" as the agent's act in every phase (ACT AP-12, SETTLED by K1-1), not a host-route treatment |
| **R9-2** | R8-11 item 2 restated: request and record clauses in force; the host's own treatment decides | Consistent |

No integrator amendment is needed for §2.2.

## 6. Other findings

| ID | Severity | Finding |
|---|---|---|
| ACT-m1 | MINOR | Checkpoint standing's definition must not evaluate ACT §4.3 (A.2). As worded it is a relabelling |
| ACT-m2 | MINOR | Replace "R8-11 item 5" with R8-1 as the basis for *binding*, in §2.2 and §7 |
| ACT-m3 | MINOR | §1's short-answer table says "Yes … None" for checkpoint state with no condition. Its "provided the §6 items on §4.0 and §4.3 are also re-anchored" appears only in §2.2's tests. Carry the condition, or ACT-m1's alternative, into §1 and §5 |
| ACT-n1 | NOTE | R-8's header assigns owners "DEL-04-02, DEL-04-03", yet its direct-branch sentence is policy. R-3 (owner DEL-04-01) carries the same rule ("effective *direct* treatment"), so anchor grant standing on R-3 point 3, with R-8 and R2-6 as corroboration |

## 7. Verdict

**REPAIR.**
- **Sound:** the computations; the grant-standing and operation-identity inversions; the "no E residual" reasoning for the §5.1 inputs; and the fallback analysis.
- **Before "M-Q-ACT becomes a design outcome" can stand:**
  - checkpoint standing reworded per ACT-m1;
  - the R8-1 citation (ACT-m2);
  - the condition carried into §1 and §5 (ACT-m3);
  - §6 extended to the uses ACT-M1 (a) lists, with the re-anchoring test of ACT-M1 (b) applied row by row;
  - REQ-007's receipt (A2) given a disposition.
- **For HELP_HUMAN:** ACT-M1 (c) is a cross-case question. Rule on Design-to-Design citations (a proposed GC-5), or commission the abbreviation-aware scan.

**Counts.** BLOCKING 0, MAJOR 1, MINOR 3, NOTE 1.
