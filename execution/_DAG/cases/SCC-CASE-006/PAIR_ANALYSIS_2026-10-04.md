# SCC-CASE-006 — pair analysis of SCC-005, DEL-10-02 ↔ DEL-10-04 (2026-10-04)

- **Standing.** This is a case evidence update under
  `workflows/scc-resolution-case`. It is evidence for the owner's checkpoint,
  not a ruling. It changes no row, register, ScopeOfWork, Design file, DAG
  version or existing case file. Every move below is a **proposal**. Cut and
  merge are the owner's (`docs/CYCLE_DRIVEN_RESOLUTION.md` §2 rule 3). Any
  ScopeOfWork revision is applied by `scope-of-work`, under an amendment the
  owner accepts. CaseState stays EVIDENCE_ACCUMULATING, and CP1-20260928
  carries forward unchanged.
- **Run.** `APP-V4-GRAPH-CLOSURE-20261004`, case work under
  `CASE_BRIEF_COMMON.md` (sha256 `c83e0f86…`, commit `b459b4f2d1`).
- **Author.** O-E, a Type 2 TASK agent (Claude Opus 5.5) dispatched by
  HELP_HUMAN. It does not delegate. O-E is the design agent of both
  deliverables' Design files, DEL-10-02 UC and DEL-10-04 DA, and of DEL-10-01
  EB. **This analysis reverses statements O-E wrote** in UC-v0.2 §8 and
  DA-v0.3 §6 (§3 below), and says so.
- **Branch and HEAD.** Branch `claude/app-v4-graph-closure`, HEAD
  `b459b4f2d1`. The PKG-10 paths are clean in git.
- **Paths.** `E/` is `projects/chirality-app-v4/execution/`. **States**,
  **Inference** and **Checked by O-E** are kept apart.

## 0. Basis and checks

| File | sha256 |
|---|---|
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/SURVEY/G1.md` (r3) | `3d6543bc2a05e5e62cb9673c1d3177386f484de38d9058a0b396eee9299f0a45` |
| `…/GC_RULINGS.md` | `27265cc9245fd7c2d93096dd8f2978376b51c48daf0e77fc110ced4c7c3318dc` |
| `docs/CYCLE_DRIVEN_RESOLUTION.md` | `bbd41a8d091c7fa81fce6462c1d5e976832e5879b6ab8c3c74147e2df55e514f` |
| `E/_DAG/DAG-004/CandidateEdges.csv`, `DependencyEdges.csv`, `ExcludedRows.csv` | as G1 r3 §0 lists them |
| DEL-10-02 `ScopeOfWork.md` | `d93ec4c043b783c01675e7fe27023969ae68a6cd7907ceb76f91b426ccc20fad` |
| DEL-10-04 `ScopeOfWork.md` | `fb62502a0f59b226607ed6a04cbbd9ffbafab35edcfe45a1a7307cfcc80d2177` |
| DEL-10-02 `Dependencies.csv` | `42a7edd14cb1d48c628c1f961d59a951dfd7d62c827a7459b0c318d5d4187cdd` (= DAG-004 source hash) |
| DEL-10-04 `Dependencies.csv` | `2469ec61bdf3017d18abda563d872b9fae89c76d693e371acf0ff0095ca66011` (= DAG-004 source hash) |
| DEL-10-02 `Design/UNDERTAKING_CONTROLS.md` (UC-v0.2) | `da0176cbf2ae806dc1c4e98b9fbd8bb7af635639c7cac4e114b7da42d0d8b533` |
| DEL-10-04 `Design/DAG_ACCOUNT.md` (DA-v0.3) | `faffae8119a8e082452516a79eabf7784cb2c5127d40821f9feb708db39d2c6d` |
| DEL-10-01 `Design/EXECUTION_BASIS.md` (EB-v0.4) | `b12c55c7b585aa0b1720b0a2426693627c9439eecad5856f74acbe1d74277392` |
| DEL-10-04 `Design/prototype/dag_reach.py` | `6325957579501e50cc9b83f76984944cdd42c9296e91615bf8dccf6e76766001` (the version G1 r3 cites) |
| `workflows/project-dag/resources/contract.md`, `graph-version.md` | `a55edc3b89a2b641…`, `ff6b7ba5b455e5e2…` |

**Checks run.** The scripts are scratch files under `$TMPDIR`, not in the
repository.

| Check | Result |
|---|---|
| Live fidelity | DEP-10-02-012, DEP-10-04-006 and the mirror DEP-10-04-014 equal their live register rows (shared fields) and are ACTIVE. Each `EvidenceQuote` occurs in the ScopeOfWork beside its register (whitespace, `` ` `` and `*` normalised) |
| Graph reading | Admitted ∪ held, with DOWNSTREAM rows reversed, gives 212 rows, 212 unique arcs, no row with a non-deliverable target, and no arc carried by two rows. Tarjan gives exactly the six `SCCRef` member sets |
| Isolation of the component | Over all 212 arcs, **no deliverable outside {DEL-10-02, DEL-10-04} reaches either member**. Any cycle through them uses only the two held arcs, so the closure result below does not depend on the kinds of any other arc |
| Closure per option | §5 |

## 1. The pair (method steps 1–2)

### 1.1 Rows

| Row | Consumer → supplier | EvidenceQuote (EQ) | Statement (excerpt) | Mirror |
|---|---|---|---|---|
| DEP-10-02-012 | 10-02 → 10-04, CONSTRAINT, UPSTREAM | "Once a current DAG is accepted, selection uses its scope and currency." | "When a current production DAG has been accepted, undertaking work selection uses DEL-10-04's accepted DAG within its scope and currency; independent authorized definition remains permitted before that event." | DEP-10-04-014 (HANDOVER, DOWNSTREAM; MIRROR, SR-6). EQ: "Once available, undertaking routes use the accepted current graph and live satisfaction evidence, preserving its limits and held work." |
| DEP-10-04-006 | 10-04 → 10-02, PREREQUISITE, UPSTREAM | "This deliverable consumes their applicable records at their points of need;" | "Graph production consumes applicable current undertaking work-graph, control and practice-feedback records from App DEL-10-02 at the actual point of need." | None |

**The EQ of DEP-10-04-006 is generic.** It is shared verbatim by DEP-10-04-005
(DEL-10-01) and DEP-10-04-007 (DEL-10-03), so the Statement decides its
content (G1 K-1).

### 1.2 ScopeOfWork sentences

- **DEL-10-02 REQ-001:** "Independent authorized definition can continue
  before the future project DAG is accepted. Once a current DAG is accepted,
  selection uses its scope and currency."
- **DEL-10-02 CLM-003:** "The undertaking graph selects and records execution
  and does not establish or accept those production relationships."
- **DEL-10-04 CLM-002:** "App `DEL-10-02` is the undertaking manager's current
  work-graph/control and practice-feedback contribution, with human stage
  decisions. … This deliverable consumes their applicable records at their
  points of need; it does not replace those contributions."
- **DEL-10-04, the graph's inputs (Ontology, after CLM-003):** "The graph's
  input is accepted allocation, applicable local ScopeOfWork contracts and
  the dependency evidence derived from them, together with human
  declarations and identified external contributions. A reference or
  ownership link becomes a production dependency only when the cited source
  establishes the specific required exchange or constraint."
- **DEL-10-04 REQ-008:** "Before an accepted project DAG exists, use the
  recorded registers and actual required conditions for authorized
  preparation; do not create a dependency on an already accepted instance of
  this graph to define it. Once available, undertaking routes use the
  accepted current graph and live satisfaction evidence …"

### 1.3 Current Design text

- **UC-v0.2 §8 (DEL-10-02):** "Graph-based selection uses the accepted current
  DAG. Pass 4's graph names 'Graph basis: DAG-004'." And: "Under R1, the
  subset of control records graph production consumes is: the current work
  graphs; this file's §2 map; the capability account (§4). … No cut or merge
  is needed (R23-31; S2-E E2-9)."
- **DA-v0.3 §6 (DEL-10-04):** "Graph production consumes, from DEL-10-02, the
  subset UC §8 names: the current work graphs; the controls map; the
  capability account. Graph-based selection consumes this file's §5 and the
  accepted pointer. No cut or merge is proposed."
- **Root method `project-dag` (the selected graph method, DEL-10-04 B5):**
  - Its interfaces table names `construct-local-work-graph` as a
    **consumer** of the accepted version ("Builds a development loop's work
    graph for a tranche of work within the accepted current version"), not
    as a supplier (`contract.md`).
  - It defines its own independent review ("A TASK instance that did not
    assemble the candidate reviews it against the confirmed basis";
    `graph-version.md` "Independent review").

## 2. Kinds (confirmed)

| Row | G1 r3 | O-E | Basis |
|---|---|---|---|
| DEP-10-02-012 | L | **L confirmed** | K-6. "Once a current DAG is accepted" governs the whole row (EQ), and the Statement says "When … has been accepted". The mirror DEP-10-04-014 says "Once available". G1 notes that the condition has occurred (DAG-004 accepted 2026-10-03). K-6 classifies by the row's words, so the kind stays L; the occurrence bears on the move, not the kind |
| DEP-10-04-006 | P (secondary E) | **P/E confirmed as written** | K-1: the EQ is generic, so the Statement decides. K-4: "control records" needed to produce the consumer's output is P. §3 tests whether that need exists at part level |

## 3. Real contradiction or projection artefact? (method step 3)

**Part order, from the texts in §1 (states).**
1. **DEL-10-02's controls exist before any DAG.** REQ-001: "Independent
   authorized definition can continue before the future project DAG is
   accepted". UC §2 shows each control settled by Root texts (SPEC §9.8,
   `construct-local-work-graph`, `coordinated-knowledge-work`, V4-OPS-30/31/34).
2. **DEL-10-04's graph content does not include DEL-10-02's records.** The
   SoW enumerates the graph's input as allocation, ScopeOfWorks, dependency
   evidence, declarations and external contributions. It adds: "A reference
   or ownership link becomes a production dependency only when the cited
   source establishes the specific required exchange or constraint". The
   only source for DEP-10-04-006 is CLM-002's generic sentence, shared with
   two other rows, which names no specific exchange with DEL-10-02.
3. **What graph production does use is settled by its own method.**
   - The project-dag method defines its own independent review.
   - It names work graphs as consumers of the DAG.
   - DAG-001…004 were each assembled and reviewed within an undertaking
     whose work graph and review records were that undertaking's own records
     (DA-v0.3 §2, §3 REQ-005).
4. **DEL-10-02's graph-based selection needs an accepted DAG.** REQ-001 says
   so. That part comes after a DAG version exists.

**Inference.**
- **The 2-cycle is a projection artefact,** a version feedback loop collapsed
  onto two nodes. The parts run: controls (settled practice, no DAG
  needed) → graph production for version n, run as an undertaking under
  that practice → selection under version n → later register and ScopeOfWork
  changes → version n+1.
- **No part of DEL-10-02 that DEL-10-04 uses waits on DEL-10-04.**
- **Changes reach version n+1 through registers and ScopeOfWorks.** They go
  through `dependency-extract` and `scope-change`, which project-dag lists as
  its evidence owners, not through a DEL-10-02 record supplied to DEL-10-04.
- **DEP-10-04-006 states as a production input what is in fact two other
  things:**
  - the accepted practice that graph production applies;
  - graph production's own undertaking records.

  Neither is a DEL-10-02 contribution that DEL-10-04's SoW establishes as a
  "specific required exchange".

**Reversal of O-E's own earlier text.** UC §8 and DA §6 named a "subset of
control records graph production consumes" under R1. R1 coordinates the
contributions and keeps the cycle; the brief states that is not a
resolution. Those statements were the designs' position under R1, not a
ruling. No integrator ruling adopted them:
- R23-31 rules E1-1…E4-5, SQ-E1 and SQ-E3, but not E2-9;
- `Ruling_Register.csv` holds only CP1-20260928.

They are reworded in M-01 below.

## 4. Moves (method steps 4–5)

### M-01 — invert DEP-10-04-006 (IV, no ownership move): the proposed move under O-1 and O-2

- **Move.** Withdraw DEP-10-04-006 as a production input. Its content is
  supplied by the accepted basis (Root SPEC §9.8; `project-dag` including
  its independent review; `construct-local-work-graph`), which DEL-10-02
  indexes, and by graph production's own undertaking records. The remaining
  arc DEL-10-02 → DEL-10-04 (DEP-10-02-012, with mirror DEP-10-04-014) is the
  direction the parts run: selection uses the accepted DAG.
- **Ownership.**
  - DEL-10-02 keeps its controls (OUT-001…003).
  - DEL-10-04 keeps the graph, its examination and acceptance evidence.
  - No OUT, AC or VER obligation moves. **S1.**
- **ScopeOfWork wording (S1, one sentence, by `scope-of-work` under an
  owner-accepted SCA).**
  - DEL-10-04 CLM-002 currently reads "This deliverable consumes their
    applicable records at their points of need; it does not replace those
    contributions."
  - Proposed: "This deliverable consumes the applicable records of
    `DEL-10-01` and `DEL-10-03` at their points of need. It runs its graph
    undertakings under the accepted undertaking practice that `DEL-10-02`
    indexes, and takes no `DEL-10-02` record as a graph input. It replaces
    none of those contributions."
  - DEP-10-04-005 and DEP-10-04-007 are unaffected.
  - `dependency-extract` then retires DEP-10-04-006.
  - DEL-10-02's SoW names no supply to DEL-10-04, and no mirror exists, so
    it needs no wording.
- **Design rewording (i), by O-E as design agent of both files, reviewed.**
  - *DA-v0.3 §6, "The SCC-CASE-006 pair".* Replace with: "Graph production
    takes no DEL-10-02 record as an input. It is run as an undertaking under
    the accepted practice (SPEC §9.8; `project-dag`, whose independent
    review is its own; `construct-local-work-graph`), which DEL-10-02
    indexes. Its work graph and review records are its own undertaking's
    records. DEL-10-02 consumes this file's §5 and the accepted pointer
    (DEP-10-02-012)."
  - *UC-v0.2 §8, "The cycle with DEL-10-04".* Replace with: "DEL-10-04 takes
    no record of this deliverable as a graph input (SCC-CASE-006 M-01).
    Graph-based selection uses the accepted current DAG (DEP-10-02-012).
    Graph production runs under the same settled practice as any undertaking
    (§2)."
  - *GC-1 and GC-3.* GC-1 governs slot inversions of contract inputs, and
    this move is not one. The design text is checked against GC-1 (a)'s
    spirit: after rewording, DA uses no field, state value or identity scheme
    that DEL-10-02 defines. DA's rules come from its own SoW and
    `project-dag`. GC-3 does not apply, because no identifier is carried.
- **Residual.**
  - None that sequences.
  - If `dependency-extract` judges that a residual remains (for example
    DEL-10-04's examination record following UC §4's capability-account
    form), it is V on DEL-10-04's own check (K-5). It would leave under
    O-2…O-4 and be a per-edge cut candidate under O-1.
  - **Not established:** whether the extractor will judge so (§7).
- **Integrator rulings amended (GC-4).** None. No HELP_HUMAN ruling covers
  SCC-CASE-006, and R23-31 did not rule S2-E E2-9. The case's own R1
  recommendation (Case_Datasheet, an agent recommendation) is superseded by
  this proposal.
- **Who.**
  - The agent proposes and the design agent rewords.
  - The ScopeOfWork wording reaches the owner only as part of an SCA they
    accept, like SCC-002's IV moves.
  - No cut or merge is needed.

### M-02 — alternative: owner cut of DEP-10-02-012 (with DEP-10-04-014), as version feedback

This is G1 r3's candidate. Its rationale: "DAG vN orders the work whose
control records feed DAG vN+1 (DEP-10-04-006)".
- **Use only if M-01 is not taken.** For example, the owner or HELP_HUMAN
  may hold that graph production genuinely takes DEL-10-02's project-local
  records (practice notes, `BRIEFS_AS_SENT.md`) as graph input.
- **What it does.** It closes the component under O-1 and O-2 with no
  ScopeOfWork change.
- **The cost.**
  - It removes from the objective a row that describes the direction the
    parts actually run.
  - Selection would stop reading blocker verdicts from DEL-10-04, though the
    obligation stays in the register (HANDOFF_STATE reading rule 2).
- **Who.** The owner, recorded in `Ruling_Register.csv`, entering the next
  version through SR-4.

**Further alternatives** remain the owner's and are not proposed:
- merge (R3, a graph-only group);
- decomposition into version nodes (O-5).

### M-03 — G2's A9 (DEL-10-01 → DEL-10-04): keep it out of the registers by design rewording

- **What G2 found.**
  - G2 lists A9 as SCC-forming: "DA §6 lists 'DEL-10-01 · Basis chain rows
    B-7 and B-11 · EB §2' as a consumer … SCC-005 grows to {10-01, 10-02,
    10-03, 10-04}".
  - It says such items "need a Design-owner wording decision, not
    extraction".
  - G1 r3 classifies A9 as E (K-3), secondary L. It sequences under O-1…O-3
    and leaves under O-4.
- **Checked by O-E.** If A9 were added as an arc, {10-01, 10-02, 10-03,
  10-04} forms under O-1…O-3 with no move. With M-01 it is {10-01, 10-03,
  10-04}; with M-02 it is all four. It forms nothing under O-4. **Neither
  M-01 nor M-02 prevents it.**
- **Part order (inference).**
  - EB's rows B-7 and B-11 index the owner's acceptance acts *after they
    occur*, quoting the acceptance record.
  - No EB part waits for a DAG version: the basis chain is appended when an
    act happens.
  - The real production direction is DEL-10-04 → DEL-10-01 (DEP-10-04-005,
    admitted, P).
- **Rewording (i), by O-E as design agent of DA and EB, reviewed.**
  - *DA-v0.3 §6, consumers table.* Remove the row "DEL-10-01 | Basis chain
    rows B-7 and B-11 | EB §2". Replace it with a note: "DEL-10-01's EB
    indexes the owner's acceptance acts after the fact. That is a citation,
    not a contribution of this deliverable."
  - *EB-v0.4 §2 (note after the B-table).* Add: "B-7 and B-11 cite each
    `ACCEPTANCE_RECORD.md` by path and sha256 as an uninterpreted reference,
    resolved by DEL-10-04's records (GC-3). No basis-chain row waits for a
    DAG version; a row is added when the act has occurred."
  - The GC-3 conditions hold: EB quotes the owner's words and custody but
    takes no structure from DEL-10-04's records.
- **Effect.** `dependency-extract` has no Design statement of a DEL-10-01
  need for DEL-10-04's contribution, so A9 stays a non-row. If it were
  extracted anyway, it would be E/L, and the owner cut under O-1…O-3 would be
  the fallback.
- **Integrator rulings amended (GC-4).** None.

## 5. Closure under each option (method step 6; checked by O-E, `$TMPDIR/scc005/check.py`)

Kinds are G1 r3's (§2). The component is isolated (§0), so this result is
exact.

| Option | No move | M-01 | M-02 | A9 added, no move | A9 added, M-01 | A9 added, M-01 + M-03 (A9 not a row) |
|---|---|---|---|---|---|---|
| O-1 | {10-02, 10-04} | **acyclic** | acyclic | {10-01…10-04} | {10-01, 10-03, 10-04} | **acyclic** |
| O-2 | {10-02, 10-04} | **acyclic** | acyclic | {10-01…10-04} | {10-01, 10-03, 10-04} | **acyclic** |
| O-3 | acyclic (L leaves) | acyclic | acyclic | {10-01…10-04} | {10-01, 10-03, 10-04} | acyclic |
| O-4 | acyclic | acyclic | acyclic | acyclic (E leaves) | acyclic | acyclic |

**What remains after M-01.**
- Under O-1 and O-2: the arc DEL-10-02 → DEL-10-04 (L) sequences selection
  after an accepted current DAG. It is satisfied in fact by DAG-004.
- Under O-3 and O-4: the component dissolves even without M-01, because L
  leaves. M-01 still removes a production row that DEL-10-04's own input
  rule does not establish.

## 6. Owner acts needed

| Option | With the proposed moves (M-01, M-03) | If M-01 is declined |
|---|---|---|
| O-1, O-2 | **None** beyond accepting the S1 wording within an SCA | A cut of DEP-10-02-012 (M-02), or a merge, or a decomposition |
| O-3, O-4 | None. The choice of option is itself the owner's objective decision (G1 §1.3) | None |

## 7. Not established

- **Whether `dependency-extract` will treat M-01's S1 wording as removing
  DEP-10-04-006 without residue.** The extractor judges, not this case.
- **Whether HELP_HUMAN or the owner hold that DAG production should take
  DEL-10-02's project-local records as graph input.** For example, practice
  notes could inform a DAG basis. No text found says so; the SoW's input
  list excludes them. If they so hold, M-02 applies.
- **The reworded Design text is not yet written or reviewed.** The case brief
  forbids Design edits here; it waits for assignment.
- **Kinds of the 210 other arcs are not re-examined.** They do not affect
  this component (§0, isolation).

## 8. `dag_reach.py` and G1's reading of the graph (checked by O-E)

- **Same arcs.** `dag_reach.arcs()` over `DependencyEdges.csv` and
  `CandidateEdges.csv` gives the same 212 arcs as a row-level reading with
  DOWNSTREAM rows reversed, set-equal. Tarjan over those arcs reproduces the
  six `SCCRef` sets. No row has a non-deliverable target, so the script's
  `DEL-` filter drops nothing in DAG-004. No arc is carried by two rows.
- **Same layers.** Like G1, it reads admitted ∪ held and never
  `ExcludedRows.csv`. Mirror rows are represented by their arcs.
- **The difference: it is kind-blind.** It answers the reach question under
  O-1 only, where every arc sequences. It cannot compute O-2…O-4. G1's own
  scripts apply the kinds.
- **Version.** It follows `_DAG/_LATEST.md`, or `--dag`, and prints the
  version it read. Its self-test is pinned to DAG-004. G1 r3 cites the same
  bytes (`6325957…`).

## 9. 2026-10-04 repair (RVG2-CASE-006: REPAIR; C6-M1, C6-M2, C6-m1, C6-m2)

- **Status of earlier text.** Sections §0–§8 above are unchanged, as
  committed at `c9885b8f71` (sha256 `4024c924…`). Where this section differs,
  **it supersedes them.** The superseding CSV rows are appended to
  `MOVES_PROPOSED_2026-10-04.csv`.
- **Review read.** `reviews/RVG2-CASE-006.md`, sha256 `dc175da2…`, at HEAD
  `0d338dd7b1`.
- **Basis added.** GC-5 (`GC_RULINGS.md` now sha256 `7fcbb551…`; GC-1…GC-4
  unchanged).
- **Scratch check.** `$TMPDIR/scc005/repair.py`, sha256 `5db8ec43…`, over
  DAG-004's 212 arcs with G1 r3's kinds.

### 9.1 C6-M1 accepted: DEP-10-04-006 keeps an E part

**The reviewer is right, and the evidence is in my own Design text.** DA-v0.3
takes acceptance custody and review records from undertaking run records:
- §2's "Recorder of the act → record writer" column runs each acceptance
  through a run's DECISION record and node D2;
- §3's REQ-005 row cites the runs' `DAG_PREP/` checkpoint packages, review
  packets and separate reviewers.

Those records are kept under DEL-10-02's controls (UC §1, §2, §4; R23-31.1,
R23-31.6). DEL-10-04 REQ-006 requires the relay provenance they carry.

M-01 as first written removed the P reading (records as graph content). It
did not, and could not, remove that runtime receipt.

**Kind of the residual.** **E** under K-3. DEL-10-04 needs instances only.
The formats it records are `project-dag`'s (the acceptance record, the
independent review). If a reviewer or the owner reads the custody records as
evidence needed to produce OUT-002 (K-4, P), see §9.5.

### 9.2 C6-M2 accepted: the S1 wording keeps a row, and the row is E

**My proposed sentence restated a reliance** ("under the accepted
undertaking practice that `DEL-10-02` indexes"). A conservative extractor
would keep that row. I take the reviewer's second option: **the row stays,
as E**, and the wording says so.

**Revised S1 wording for DEL-10-04 CLM-002.** Applied by `scope-of-work`
under an owner-accepted SCA; replaces the sentence "This deliverable
consumes their applicable records at their points of need; it does not
replace those contributions":

> This deliverable consumes the applicable records of `DEL-10-01` and
> `DEL-10-03` at their points of need. From `DEL-10-02`'s undertaking
> records it receives, as evidence of actual acts, the decision
> transcriptions, checkpoint packages, review records and capability and
> check accounts of its own graph undertakings. It does not take them as
> graph content. Graph production follows the selected `project-dag`
> method and Root SPEC §9.8. It does not replace those contributions.

**Expected extraction (not established; the extractor judges).**
- DEP-10-04-006 keeps its ID under match rule 2. Its Statement narrows to
  an evidence handoff: kind E, not P.
- DEP-10-04-005 and -007 keep their IDs, but their EvidenceQuote is
  refreshed (RVG2 C6-n2).
- No row to DEL-10-02 for "practice" arises, because the wording names Root
  sources directly.

### 9.3 C6-m1 accepted: M-01 is a narrowing by SCA, not an invert

Nothing reverses, and no contract is interposed. The move now:
- removes the production (P) reading of DEP-10-04-006;
- retargets the method content to Root (`project-dag`, SPEC §9.8);
- leaves the row as E.

**Re-coded:** `NARROW (P→E; SCA)`. The owner sees it as part of an SCA they
accept, not as an agent-only refinement. It does not close the component
under O-1 or O-2 by itself (§9.5).

### 9.4 C6-m2 accepted: A9 is a real E flow; GC-3 does not carry M-03

- **EB takes content, not just identifiers.**
  - B-11's Subject ("The 33 files of `REVIEW_PACKET.md` …") comes from
    DAG-004's `ACCEPTANCE_RECORD.md`.
  - So does its "What it did not decide" cell, from "This acceptance does
    not:".
  - EB therefore needs that content to produce its rows.
- **Under GC-5 item 1, A9 is a dependency** (DEL-10-01 needs DEL-10-04's
  acceptance-record content to produce B-7 and B-11). It is not an
  attribution under item 2.
- **Under GC-5 item 3, it cannot stay a Design-only use.** It is either
  removed by an accepted move or carried into DEL-10-01's ScopeOfWork (S1)
  and so into the register.
- **EB §4's pointers stay out.** Its pointers to `_DAG/_LATEST.md` and the
  DAG-004 handoff are cross-references (GC-5 item 2) and are not counted.
- **The `ACCEPTANCE_RECORD.md` content cannot be sourced elsewhere.** Taking
  the owner's words from the run OWNER_DECISIONS transcriptions instead would
  make EB consume DEL-10-02's run records. That would close 10-01 → 10-02
  against DEP-10-02-011 (P). Not proposed.

**M-03 is withdrawn.** Its DA §6 deletion of the DEL-10-01 reader row and its
GC-3 claim for EB were both a narrowing of my own text. It is replaced by:
- **M-03-R.** Carry A9 into DEL-10-01's ScopeOfWork as an E evidence handoff
  (S1), for example:

  > It records the owner's graph acceptance acts after they occur, from
  > `DEL-10-04`'s acceptance records, as evidence.

  Under O-1…O-3, the closing move is then an **owner cut** of that E row
  (runtime, after-the-fact evidence: the doctrine's "runtime" class). Under
  O-4 it leaves with its class.
- **DA §6** keeps DEL-10-01 in its consumers table.
- **Provisional.** GC-5 item 4 makes this provisional until G2b reports.

### 9.5 Closure and owner acts, restated (supersedes §5 and §6)

**Component SCC-005 alone (A9 not yet a row):**

| Option | After M-01-R (E residual stays) | Owner act that closes it |
|---|---|---|
| O-1 | {10-02, 10-04} | **One cut:** M-04, the E residual DEP-10-04-006 (recommended), or M-02, DEP-10-02-012 with DEP-10-04-014 |
| O-2 | {10-02, 10-04} | **One cut:** M-04 or M-02, as for O-1 |
| O-3 | acyclic (L leaves) | None |
| O-4 | acyclic (L and E leave) | None |

**With A9 carried as an E row (GC-5 item 3):**

| Option | Component | Minimum owner cuts (computed) |
|---|---|---|
| O-1 | {10-01, 10-02, 10-03, 10-04} | **2:** {E residual, A9} or {DEP-10-02-012, A9} |
| O-2 | the same | **2:** as O-1 |
| O-3 | {10-01, 10-02, 10-03, 10-04} | **1:** A9 |
| O-4 | acyclic | 0 |

**Why M-04 is recommended over M-02** (both are the owner's; agent opinion):
- M-04 reclassifies a runtime, after-the-fact evidence row. That is the
  doctrine's own cut example: "runtime/test/optional".
- It keeps DEP-10-02-012, the real production direction: selection waits for
  an accepted current DAG. That is also `project-dag`'s stated interface,
  "`construct-local-work-graph` … within the accepted current version".
- If the residual is read as P (K-4), M-04 is not a doctrine cut, and M-02 is
  the cut.

### 9.6 Recheck of my own earlier design (narrowings), as asked

| Earlier text (mine) | Narrowing? | Repair |
|---|---|---|
| M-01's S1 sentence "takes no `DEL-10-02` record as a graph input" | **Yes.** It dropped CLM-002's consumption of DEL-10-02's applicable records, including custody, review and capability-account evidence that DA §2–§3 use | §9.2 wording keeps them as E evidence |
| M-01's DA §6 rewording "Graph production takes no DEL-10-02 record as an input" | **Yes**, the same | New DA §6 wording, for the design step: "From DEL-10-02's undertaking records DA takes, as evidence, the decision transcriptions, checkpoint packages, review records and capability and check accounts of the graph undertakings (DEP-10-04-006, E). None is graph content." |
| M-01's UC §8 rewording "DEL-10-04 takes no record of this deliverable as a graph input" | Partly. "As a graph input" is accurate for content, but the sentence hid the evidence flow | New UC §8 wording: "DEL-10-04 reads this deliverable's undertaking records as evidence of acts and reviews (E), never as graph content" |
| CLM-002's "practice-feedback" consumption | **Yes.** It was dropped by the original M-01 | Kept: practice notes that bear on a graph undertaking are among the applicable records DEL-10-04 may cite as evidence (E). Their dispositions remain the owner's at stage discussions (UC §7) |
| M-03's deletion of the DEL-10-01 reader row from DA §6 | **Yes** | Withdrawn (§9.4) |
| M-03's EB note relying on GC-3 ("takes no structure") | **Yes**, overstated | Withdrawn (§9.4) |
| Checks: DEL-10-04 REQ-005/006, VER-005/006/009 | No | Intact: the E row keeps the custody and review evidence those checks examine (RVG2 C6-n2) |
| DEL-10-02 REQ-001 / VER-001 (selection uses the accepted DAG) | No | Intact. DEP-10-02-012 is unchanged unless the owner takes M-02 |

**I found no other narrowing.** The kinds (§2), the isolation result (§0)
and the reading of `dag_reach.py` (§8) are unaffected.

### 9.7 Not established (adds to §7)

- **The extraction outcome of the §9.2 wording.** That it yields
  DEP-10-04-006 as E with no other row to DEL-10-02 is not established.
- **The final kind of the residual.** Whether a reviewer or the owner reads
  it as E (M-04 applies) or as P (M-02 applies) is not settled.
- **A9 is provisional under GC-5 item 4** until G2b reports.
- **The DA, UC and EB rewordings** are still unwritten. They wait for a
  design assignment.
