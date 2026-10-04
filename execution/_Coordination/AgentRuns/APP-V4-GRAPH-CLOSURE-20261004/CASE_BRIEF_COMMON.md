# Common brief for SCC case work (graph closure)

Every case agent works from this text, together with its own short
assignment message.

**Purpose.** The owner's 60% gate: "the DAG won't change and all SCCs have
been resolved, so that work can proceed enmass in parallel". The doctrine
is `docs/CYCLE_DRIVEN_RESOLUTION.md` §2. An SCC is resolved only by one of
four named moves:
- decompose or invert, which an agent may propose;
- cut or merge, which the owner rules.

"Coordinate the contributions" keeps the cycle and is not a resolution.

**Basis.** Read these; they are committed on branch
`claude/app-v4-graph-closure`.
- `SURVEY/G1.md` r3. Use its kinds rules K-1…K-7, its §2 rows for your SCC,
  its exact minimum cycle-closing sets, and its objective options O-1…O-4.
  RVG confirmed it as READY.
- `GC_RULINGS.md`:
  - GC-1: a slot inversion removes a contract input only with an opaque
    reference and conformance checked outside the consumer;
  - GC-2: Q-5 says nothing about DEL-04-01's suppliers;
  - GC-3: an uninterpreted identifier is opaque, under its conditions;
  - GC-4: integrator rulings a rewording would amend are listed, and
    amended by HELP_HUMAN at application.
- The method example is `_DAG/cases/SCC-CASE-002/PAIR_ANALYSIS_2026-10-04.md`
  (§1–§22) and `MOVES_PROPOSED_2026-10-04.csv`, with RVG's reviews in
  `reviews/RVG-C2.md`.

**Method.** For each cycle-closing row in your component:
1. Quote both rows of the reciprocal exchange: the DEP-id, the
   EvidenceQuote and Statement, and the ScopeOfWork sentence.
2. Quote the current Design text on both sides.
3. Decide whether the cycle is a real part-level contradiction or a
   projection artefact.
4. Propose the smallest move that closes it, preferring, in order:
   - (i) a design rewording that meets GC-1 and GC-3, naming the file,
     section and design agent;
   - (ii) an invert that moves no ScopeOfWork-assigned ownership;
   - (iii) an owner act: cut, merge, an ownership-moving inversion or a
     decomposition.
5. List any integrator ruling the move would amend, as GC-4 requires.
6. Check, with your own script in `$TMPDIR`, that your moves make the
   component acyclic under each of O-1…O-4, using G1 r3's kinds. Report
   what remains under each option.

**Output.** Write two new files in your case folder `_DAG/cases/<CASE-ID>/`:
- `PAIR_ANALYSIS_2026-10-04.md`;
- `MOVES_PROPOSED_2026-10-04.csv`, with the same columns as SCC-CASE-002's.

Do not modify existing case files, registers, ScopeOfWorks, Design files
or any `_DAG` version. Use read-only git and no network. Keep scratch work
in `$TMPDIR`.

**Return.** Report:
- both paths and their sha256 hashes;
- a one-line verdict per pair;
- the owner acts needed under each option;
- whether the component closes under each option;
- anything not established.

"Owner" means the person; call agents agents.
