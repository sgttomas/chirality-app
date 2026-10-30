# EB-1 reader brief — reading the App v4 project's execution basis cold

You are an isolated reader. Only the dispatcher's message, this brief, the
manifest `IS-EB1-1.input-set.json` and the files it lists are yours to read.
The manifest's paths are relative to the folder you are given.

## Rules

1. **Check before reading.** Recompute the sha256 of every manifest item and
   compare it with the manifest. If any item is missing or differs, stop and
   report which (RD-0). Do not answer from a partial set.
2. **Read nothing else.** That excludes the repository, Git history, other
   sessions and your own background knowledge of this project. If you
   cannot answer from the supplied files, answer `unknown` and say what is
   missing.
3. **Records carry the weight.** The manifest gives each item a standing:
   - `record` and `project_file` items can support a claim;
   - `EXECUTION_BASIS.md` is an index written by an agent. Use it to find
     things. A claim that a person acted, or about who recorded an act, must
     cite the record itself, not only the index;
   - where the index and a record disagree, report the disagreement.
4. **Give each answer a standing:**
   - `from_records`: a supplied file states it; cite path and locator;
   - `inferred`: say so, and cite what you inferred it from;
   - `unknown`: the files do not settle it.

   Do not fill gaps from likelihood.
5. **Quote only what you need.** Exact words of a decision are short; give
   them exactly.

## Questions

- **Q1** Which manual editions govern the project's current work? Give each
  edition's sha256, recomputed by you from the supplied bytes. What standing
  does each have: who selected or recorded it, and for what scope? Is
  reading a manual the same as adopting it?
- **Q2** Which methods (workflows or skills) govern the current undertaking,
  `APP-V4-DESIGN-PASS-4-20261003`? For each give:
  - its identity;
  - its recomputed sha256;
  - where its selection is recorded;
  - who selected or directed it.

  Which of them, if any, are not among the methods pinned for the
  definition run?
- **Q3** What development position has the project reached, by which act
  and whose? What does the next position require, who decides it, and has it
  been decided?
- **Q4** Answer for each of three acts:
  - (a) acceptance of the final decomposition (Group3);
  - (b) acceptance of DAG-004;
  - (c) approval to apply the D-GOV-52 change to Root `AGENTS.md`.

  For each give:
  - the actor and the exact words;
  - who relayed or transcribed it, and who wrote the record you read
    (`unknown` if that record does not say);
  - the exact subject, with identifiers or hashes the record gives;
  - the custody limits the record states;
  - one thing the act did not decide.
- **Q5** Which open items bear on the execution basis? Cover manual
  editions, instruction distribution, consequential manual gaps, manual
  revision, and adoption by other consumers. Give each item's ID, owner and
  point of need as the records state them.
- **Q6** An agent arrives to start a new undertaking in this project. Which
  records must it use for:
  - (a) accepted scope;
  - (b) production order;
  - (c) whether a required input is met;
  - (d) manuals and methods;
  - (e) how to run the undertaking?

  Name three things it must not redo or re-ask, each with its source.
- **Q7** For each of the following, say whether it was an act of the owner;
  if not, say whose act it was, with the source:
  - (a) the R23 rulings;
  - (b) moving deliverables from INITIALIZED to IN_PROGRESS;
  - (c) App v4's adoption of the D-GOV-52 change;
  - (d) treating design reviews in which Claude reviewed Claude-authored work
    as sufficient for design units.
- **Q8** Which mechanisms from the manuals or the original seed has the
  project superseded or chosen not to use? Give the record that treats each.
  Does any departure now await the owner's decision?

## Return

Return one JSON file, `account.json`:

```json
{
  "input_set_id": "IS-EB1-1",
  "rd0": {"items_checked": 0, "mismatches": []},
  "answers": [
    {"q": "Q4", "part": "b", "field": "actor", "answer": "…",
     "standing": "from_records", "sources": [{"path": "…", "locator": "…"}]}
  ],
  "disagreements": [],
  "unknowns": [],
  "read_beyond_input_set": "none"
}
```

Give one entry per question part and field. Then give a short report: what
was hard to find, and anything the index got wrong or left out.
