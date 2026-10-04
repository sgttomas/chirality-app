# RR-F result — second isolated reader (HELP_HUMAN)

- **Reader:** a fresh instance given exactly the ten files in
  `SUPPLIED.sha256` (DISPATCH_RECORD.md). By its own report it opened only
  those files, listed no directory, and wrote only its account. The host did
  not enforce this.
- **Account:** `account.json`, sha256
  `8188caba864ff83e73e9c6b99342208d6df978c70bdb7744b35991fdd6f392c0`. It is
  schema-valid (the reader's run of jsonschema 4.26.0).
- **Examiner comparison** (`rrm_compare.py` d445740e…, output in
  `COMPARE.txt`): **9 of 9 hold, 0 referred.** No examiner judgment was
  needed: the reader stated absences with the `no_outcome` and `no_change`
  kinds the repaired brief offers.
- **Substance:**
  - both packages reconstructed: PKG-1 requested and decided (ALT-2,
    Engineer A, recorded by app-interface:local), and PKG-2 requested and
    undecided;
  - the conflicting agent message was read and given no weight;
  - 10 unknowns were stated, among them the person's real identity and
    whether the offer was displayed.
- **Offer digest:** the reader recomputed it from the supplied rule alone,
  with its own canonicalizer, and matched the offer and the capture,
  including non-ASCII text and U+2028. That closes the gap RR-E found.
- **On O-C's last-segment rule:** this reader used the full namespaced ids
  (`pkg:fx-u1:PKG-1`), so the rule was not exercised; RR-E had used short
  forms. The rule stays, with RV's hardening (overlapping tails).
- **Standing:** together, RR-E and RR-F show that the early path's records
  are usable from the files alone by two independent readers, on the first
  and the revised package shape. This is fixture evidence; no App
  candidate exists yet.
