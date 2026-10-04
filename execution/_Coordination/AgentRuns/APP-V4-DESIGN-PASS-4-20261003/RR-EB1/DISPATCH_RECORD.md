# RR-EB1 — isolated reader for O-E's EB-1 (DEL-10-01 execution basis)

- **Dispatcher:** HELP_HUMAN, 2026-10-04. **Reader:** a fresh
  `type2-opus-high` instance with no prior part in this work (Agent tool,
  D-GOV-35).
- **Supplied:** the dispatch prompt and exactly the 46 files in
  [SUPPLIED.sha256](SUPPLIED.sha256), at `<session scratchpad>/rr-eb1/in/`
  under their repository-relative paths. They are the 44 items of
  `IS-EB1-1`, the manifest and `EB1_READER_BRIEF.md`. O-E's `eb1_check.py
  --verify-dir` gave PASS 138, FAIL 0 on that folder before dispatch.
- **Withheld:** the question key, `SURVEY/S2-E.md`, `OWNERS/O-E.md`, and
  everything else.
- **Enforcement limit:** the host does not restrict reads. Separation rests
  on the brief and on the reader's own report of the files it opened.
