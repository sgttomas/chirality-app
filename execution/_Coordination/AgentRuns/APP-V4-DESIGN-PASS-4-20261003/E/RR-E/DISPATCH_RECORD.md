# RR-E — isolated reader dispatch (early path consumption check)

- **Dispatcher:** HELP_HUMAN (Claude Code session), 2026-10-04 UTC.
- **Reader:** a fresh `type2-opus-high` instance (Claude Opus 5.5, high
  effort) with no prior context in this session's work. Mechanism:
  harness-native descendant (Agent tool), D-GOV-35.
- **Supplied:** the brief text below (verbatim in the dispatch prompt), and a
  folder `<session scratchpad>/rr-e/in/` holding exactly the nine files in
  [SUPPLIED.sha256](SUPPLIED.sha256): the six input-set items, the
  input-set manifest, the account schema and the reader brief. Their
  hashes match `IS-FX-DP1.input-set.json` and O-C's fixtures.
- **Withheld:** everything else, including the repository, the fixture
  author's notes and DEL-06-02's view output.
- **Enforcement limit:** the host does not restrict the reader's file
  reads. Separation rests on the brief and on the reader's own report of
  each file it opened. This is stated as a limit, not as an enforced
  boundary.
- **Account:** written to `<session scratchpad>/rr-e/out/account.json`,
  then copied here as `account.json` and checked with DEL-09-11's
  `prototype/rrm_compare.py`.
