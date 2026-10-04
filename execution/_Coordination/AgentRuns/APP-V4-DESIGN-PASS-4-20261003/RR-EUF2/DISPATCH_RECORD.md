# RR-EUF2 — second isolated reader for O-F's EU-F1 (RP-v0.2, IS-FX-RP1-2)

- **Why:** RP-v0.2 changed the packet's rules and its legibility for the
  person deciding (O-F's repairs after RR-EUF1). The package is the
  presentation to that person, so the repaired version is read cold again.
- **Dispatcher:** HELP_HUMAN, 2026-10-04. **Reader:** a fresh
  `type2-opus-high` instance with no prior part in this work.
- **Supplied:** exactly the files in [SUPPLIED.sha256](SUPPLIED.sha256),
  staged by `F/stage_is.py --set 2` (all hashes matched). The key
  `F/EU-F1-2.answer-key.json` is withheld.
- **Enforcement limit:** the host does not restrict reads. Separation rests
  on the brief and on the reader's own report.
