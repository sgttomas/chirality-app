# GROUP_SORT — independent check of the development groups (GROUPS.md)

- **Run and author.** `APP-V4-GRAPH-CLOSURE-20261004`. RVG, a Type 2 TASK executor (Claude Opus 5.5, `claude-opus-5-5`), dispatched by HELP_HUMAN. No delegation. I did not compute the grouping. Read-only git, no network. This is the only file written.
- **Subject.** `GROUPS.md` at commit `de67cb79b9`, sha256 `7d3bfb79ae4f26882dd4297c7c03db184df46c9d6a5b325b5d51413fdec144be`.
- **Basis.**
  - DAG-004 `DependencyEdges.csv` (`c4303374…`) and `CandidateEdges.csv` (`2bfff10e…`), with arcs read consumer → supplier and DOWNSTREAM rows reversed.
  - G1 r3 kinds, where an option matters.
  - `SURVEY/G2b.md` (`499fbcd1…`), §4.1 and §4.2, with the corrections from `reviews/RVG-G2b.md`.
- **Scripts.** My own, in `$TMPDIR/rvg/`: `groups.py`, `gsort.py`.
- **Order convention.** "A → {B, C} → D → E" means suppliers come first. An arc is **in order** when the consumer's group is later than the supplier's. B and C are unordered with respect to each other.

## 1. The grouping test on DAG-004, reproduced

| Claim in GROUPS.md | Result |
|---|---|
| The five groups cover the 41 deliverables | **Confirmed.** All 41 DeliverableNodes are assigned, each once |
| All 83 held rows lie within one group | **Confirmed.** No held arc crosses a group. SCC-001 and SCC-002 are in A, SCC-003 in B, SCC-004 in C, SCC-005 and SCC-006 in E |
| Every arc between groups follows A → {B, C} → D → E | **Confirmed with two arcs named, not one.** 76 admitted arcs cross groups. 74 run in order: A→B 12, A→C 2, A→D 35, A→E 10, B→D 5, B→E 1, C→D 6, D→E 3 (supplier → consumer) |
| The only exception is DEL-09-09 → DEL-09-01 | **Partly.** There are two arcs: |
| | (1) **DEP-09-09-012**, DEL-09-09 (A) consumes DEL-09-01 (B). It is against the order. EvidenceQuote: "Interface evidence follows the shared WebKit/Chromium and targeted packaged-smoke protocol through the examination infrastructure". It is a real need: the trace uses the shared examination protocol. It forms **no cycle** on DAG-004: DEL-09-01 does not reach DEL-09-09 over either layer |
| | (2) **DEP-09-01-027** (a DOWNSTREAM row in DEL-09-01's register), DEL-09-10 (C) consumes DEL-09-01 (B): "It supplies reusable support and evidence interfaces to those owners." This arc is **not against** the stated order, but it orders C's DEL-09-10 after B, so B and C are not fully parallel. GROUPS.md does not mention it. **Smallest response:** move DEL-09-10 to D. It has no consumers, consumes only B and C deliverables, and is a witness ("Optional connector consumption witness"). Alternatively, record it as a named B → C dependency |

## 2. The G2b items, sorted

**Population.** G2b's 62 dependencies and 13 unclear pairs, with RVG-G2b's corrections applied:
- U01 counts as a dependency;
- U13 and EXP-R9 (U11, U12) are not definitional and are not sorted.

That leaves 72 items.

**How each item was classed.** Each item was added alone to DAG-004 (212 arcs) and tested under O-1…O-4.
- **(d)** if it creates or changes a strongly connected component whose members span more than one group, under any option.
- Otherwise **(a)**, **(b)** or **(c)**, by the groups of its consumer and supplier.

| Class | Count | Items |
|---|---:|---|
| **(a) Within one group** | 26 | A: D01, D02, D05, D06, D08, D09, D15–D24, D47, D48, U03, U04, U07. C: D31. D: D36, D46, D54, D56 |
| **(b) Across groups, in order** | 34 | D10–D14, D25–D30, D32–D35, D37–D45, D51–D53, D55, D58–D62, U09 |
| **(c) Across groups, against the order** | 2 | D50 (C consumes D); U10 (C consumes B: lateral, the same direction as DEP-09-01-027) |
| **(d) Forms a cycle that crosses groups** | 10 | **d1** (in order or within A, cyclic only through DEP-09-09-012 under O-1): D03, U01, U02, D04, U05, U06. **d2** (against the order and cyclic): D07, D49, U08, D57 |

The (a) items stay inside a group, so each group's work graph records them (GC-7). They include the whole DEL-04-01 hub (D15–D23), which sits wholly inside A.

### 2.1 (d1): six items whose cross-group cycle runs only through DEP-09-09-012

D03 (N08), U01 and U02 lie within A. D04, U05 and U06 run B → A, which is in order. Each forms an A–B cycle **only under O-1**, and **only through** the exception arc DEP-09-09-012:
- **Without that arc,** none forms a cross-group cycle under any option (computed).
- **With it,** the cumulative O-1 component is 20 members spanning A and B.
- **The mechanism.** DEL-09-09 enters SCC-002 only under O-1, through its one incoming held arc DEP-03-01-030 (V/L, pair P16). Under O-2…O-4 that arc leaves, and so does every A–B cycle. Under O-1, the P16 cut already listed among SCC-002's owner acts (C2 §22.6, group 2) also removes them (computed: no cross-group cycle).

**Smallest response.**
- None, under O-2…O-4.
- Under O-1, the P16 cut the human already faces.
- No regrouping is needed. These items are not against the order.

### 2.2 (c) and (d2): deciding sentences and responses

| Item | Deciding Design sentence (at source) | Effect | Real need or reading choice | Smallest response |
|---|---|---|---|---|
| **D57** 09-12 → 10-02 (D uses E) | PV §3.5: "**`method_note`** has exactly DEL-10-02 UC §5's fields, read from UC at the commit (K-11)" | Cycle {09-12, 10-02} (with SCC-005 under O-1 and O-2) under O-1…O-3, against the admitted DEP-09-12-012 (E). None under O-4 | **Real.** PV writes its hand-over record in the receiver's format | **Regrouping: move DEL-09-12 to E.** It is consumed only by E deliverables (10-02, 11-03) and consumes A, B and D. All its arcs are then in order, and the cycle becomes within-group. Alternative: a Design rewording in which UC adopts PV's form |
| **D07** 02-03 → 09-06 (A uses D), V | EXEC §7.3 RT-11: "**Evidence account for DEL-09-06** \| … following CA-v0.6 §8.2 (R10-11: the consumer's list governs; V18-4 m-1)" | Cycle A–D under O-1 only (V leaves under O-2…O-4) | **Reading choice.** R10-11 says "the consumer's list governs which supplier cases it builds on", so the consumer (CA) selects EXEC cases. EXEC's RT-11 mapping is a receiver-facing account | **Design rewording**, no ruling amendment: the W14 ← EXEC mapping lives in CA §8.2, and RT-11 names DEL-09-06 as receiver only |
| **D49** 09-09 → 09-06 (A uses D; G2 A7) | XT §2: "Standing uses the C evidence-label mapping and the DEL-09-06 contribution ladder (CA §7.2)" | Cycle A–D under O-1. With the P16 cut, still the 3-member {03-04, 09-06, 09-09} under O-1 | **Reading choice.** CA §7.2: "The seven standings and their order are stated by SoW OUT-004" (DEL-09-06 ScopeOfWork l.53). The ladder is basis-carried | **Design rewording:** XT cites DEL-09-06 SoW OUT-004 for the ladder (GC-5 item 2). It is then not a dependency |
| **U08** 04-03 → 09-06 (A uses D) | RS §4 R11: "**act offered without a capture-evidence reference** … (EXEC A-7; DEL-09-06 CAF-24; HA-1) — these seven adopted from their suppliers" | Cycle A–D under **every** option (13 members under O-2…O-4) | **Reading choice.** The label's source is R14-3 and EXEC A-7: EXEC Changes row R14-3, "RS R11 'act offered without a capture-evidence reference'". CA's own CAF-24 cites RS R11 "(R14-3)" back. So CA consumes RS (D uses A), not the reverse | **Design rewording:** RS R11 cites R14-3 and EXEC A-7 only and drops "DEL-09-06 CAF-24". It is then not a dependency |
| **D50** 09-10 → 09-07 (C uses D) | CW §5: "a PEC gap sheet … and a Domains gap sheet …, in DOS-v0.1's pattern" | Against the order. No cycle | **Reading choice:** a document pattern, not a contract input | **Regrouping: move DEL-09-10 to D** (the same move as §1, arc (2)). Or a Design rewording: drop "in DOS-v0.1's pattern" |
| **U10** 08-02 → 09-01 (C uses B: lateral) | RTD §8: "A rehearsal of RD-2…RD-4 can reuse EU-D1's Domains cases … as `rehearsal` records (EXP-R3: they stand for no scenario)" | Lateral. No cycle | **Reading choice:** an optional rehearsal, V at most | None needed if B → C is accepted as a refinement (§3). Otherwise a rewording |

### 2.3 Check of the combined responses

With DEL-09-12 in E and DEL-09-10 in D, and D07, D49 and U08 reworded as above, I recomputed everything over DAG-004 and the remaining G2b items:
- **Held rows:** none crosses a group.
- **Admitted arcs:** all 77 cross-group arcs are in order except DEP-09-09-012.
- **G2b items:** all are in order except U10 (lateral B → C).
- **Cross-group cycles:** none under O-2…O-4. Under O-1, the A–B cycle through DEP-09-09-012 remains (20 members), and it is removed by the P16 cut.

## 3. Verdict

**The group order is supported, with named exceptions.**

1. **On DAG-004**, the order holds for 74 of 76 cross-group arcs, and all 83 held rows lie within groups.
   - **DEP-09-09-012** (A uses B) is a real, acyclic exception, as GROUPS.md states.
   - **DEP-09-01-027** (C's DEL-09-10 uses B) is a second cross-group arc GROUPS.md does not name. It is not against the order, but it makes B → C a dependency. Moving DEL-09-10 to D, or reading the order as **A → B → C → D → E**, accommodates it. Every DAG-004 arc except DEP-09-09-012 fits that refinement.
2. **On G2b**, 60 of 72 items are within a group or in order. Of the remaining 12:
   - **6 (d1)** are cyclic across A–B only under O-1 and only through DEP-09-09-012. The P16 cut, already among the human's O-1 acts, removes them.
   - **D57** (09-12 → 10-02) is a **real** need against the order. The smallest response is **moving DEL-09-12 to E**.
   - **D07, D49, U08 and D50** are reading choices, each closed by a one-sentence Design rewording (or, for D50, by moving DEL-09-10 to D).
   - **U10** is an optional lateral B → C use.
3. **Your two suspects.**
   - **09-12 → 10-02 (D57):** confirmed against the order and real.
   - **02-03 → 09-06 (D07):** confirmed against the order. It is V, cyclic only under O-1, and a reading choice under R10-11.
4. **What goes to the human under GC-7.**
   - Two regroupings: DEL-09-12 to E, and DEL-09-10 to D.
   - The O-1 dependence on the P16 cut.

   The three rewordings (D07, D49, U08) are design-agent work. No exception found here needs a merge or a new decomposition.
