# Receipt — APP-V4-GRAPH-CLOSURE-20261004

The undertaking aimed to close the project graph toward 60%. It ended with
four results:
- the owner's acceptance of the 60% gate, together with development groups;
- a walking skeleton of App v4 running as tested code;
- manual guidance on the 60% transition;
- App v4's LOOP_INIT reduced to a binding pointer.

Graph: [WORK_GRAPH.md](../../WorkGraphs/APP-V4-GRAPH-CLOSURE-20261004/WORK_GRAPH.md).
Owner acts, with their exact words and custody:
[OWNER_DECISIONS.md](OWNER_DECISIONS.md).

## What landed

- **The 60% gate is accepted**, together with groups A–E for development.
  The groups and their order, A → {B, C} → D → E, are in
  [GROUPS.md](GROUPS.md). They were reproduced independently in
  SURVEY/GROUP_SORT.md, and the owner moved two deliverables after that
  check. The DAG remains DAG-004.
- **Graph evidence (records only).**
  - Surveys: G1 r3 (objective and SCC kinds), G2 (register currency) and G2b
    (design uses across deliverables).
  - The seven case analyses under `_DAG/cases/`. Each one found coupled
    definition rather than a contradiction.
  - Rulings GC-1…GC-9. The last three are the most important:
    - GC-6: no narrowing to close a cycle;
    - GC-7: recording relationships after 60%;
    - GC-8: cross-group relationships go in the work graphs of the
      affected loops.
- **Walking skeleton** (`app/`). Tauri 2 + React + Vite. It runs four steps
  as tested code:
  1. hosting stock Codex 0.158.0;
  2. the A16 decide act through the App act control;
  3. an RS record, validated against its schema;
  4. the decision view.

  Builds are offline. The first end-to-end run came about 14 minutes in.
  Implementation exposed nine contract issues, logged in
  `app/CONTRACT_ISSUES.md`.
- **Manuals.**
  - Project Management manual v8 is the current edition; v7 is archived
    unchanged.
  - The Field Book and the Agent User Manual are revised in place.

  Covered: discerning and passing the 60% gate, the handoff to 90%, recording
  found relationships, and an App v4 entry in the Agent User Manual.
  Tranche: `ROOT-MANUAL-60PCT-20261004`. The App v4 notice is
  `NOTICE_2026-10-04_ROOT_MANUAL_60PCT.md`.
- **LOOP_INIT and init prompt.**
  - The entry reading is the Agent User Manual headings plus the Field Book.
  - The methods are named, including `coordinated-knowledge-work`.
  - App v4 records and standing constraints are listed.

  The text is about 1,240 tokens, down from about 4,100.

## Checks

- **Independent reviewers:**
  - RVG on the surveys, SCC-002, N13, CASE-005, ACT51, G2b and GROUP_SORT;
  - RVG2 on CASE-001, -003, -006 and -007;
  - MR on the manuals and LOOP_INIT.

  Each reviewer confirmed the repairs to its own findings. All reviews are in
  `reviews/`.
- **Skeleton tests:** `npm test` 3/3 and `cargo test --offline`, rerun by
  HELP_HUMAN with the verified binary (sha256 `788a818f…`).
- **Manuals:** the renderer's `--check` passes on both HTML editions.
- **Tranche:** `validate_instruction_tranche_manifest.py --base origin/main`
  exits 0.
- **Export:** regenerated; `test_public_export_profile.py` passes 5/5.

## Limits

- **Merge hold.** The owner placed it on 2026-10-04 and lifted it the same
  day ("You are allowed to merge your PRs again."). While it stood, these
  commits stayed local and no PR was opened.
- **Graph status.** The SCCs are still `SCC_UNRESOLVED` in DAG-004. They are
  treated by grouping for development, which is not a merge ruling.
- **Rewordings not applied.** The case analyses' proposed rewordings are
  proposals only. The three reading-choice rewordings named by GROUP_SORT
  (D07, D49 and U08) are not yet made.
- **Nothing tested against a model.** No model turn has been exercised,
  because no model provider is available.
- **Review independence.** Every review was Claude reviewing Claude.
