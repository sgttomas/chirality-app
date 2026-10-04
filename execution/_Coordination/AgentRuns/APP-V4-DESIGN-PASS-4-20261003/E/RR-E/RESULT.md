# RR-E result — early path consumption check (HELP_HUMAN)

**Reader:** a fresh instance given exactly the files in `SUPPLIED.sha256`
(see DISPATCH_RECORD.md). It reported opening only those nine files and
writing only its account. The host did not enforce this; it is the reader's
report.

**Account:** `account.json`, sha256
`637e234cdab95785698ab2f39275359a68e674dd9a9024fa7447cf25b3134cee`. It is
valid against `rrm.reconstruction-account.schema.json`.

**Examiner comparison** (`rrm_compare.py`, output in `COMPARE.txt`): 7 of 9
checks hold. RC-6 and RC-9 fail.

**What supports each failure (inspected before ordering any repair):**

- **RC-6 is a defect in the checker and the brief, not in the reader.** The
  account does reconstruct both packages: PKG-1 requested and decided (ALT-2,
  Engineer A, recorded by app-interface:local), and PKG-2 requested and
  undecided. The checker finds claims only by `about` equal to the package
  path, which is a convention used by O-C's constructed accounts. Neither the
  brief nor the schema states it. The reader wrote `about: "PKG-1 request"`
  and cited the path in `sources`.
- **RC-9 is a defect in the checker.** Claim C-09 says that *nothing* after
  the decision is recorded, which is a truthful statement of absence. The
  check treats every `outcome` claim not marked `unknown` as claiming
  something happened.
- **The decision itself:** RC-7 and RC-8 hold. No fabricated or altered
  decision. The agent message claiming that PKG-2 was decided was read and
  correctly given no weight.

**A gap the reader found:** it could not reproduce `offerDigest`, because no
serialization is given in the files it had. It recorded this as an unknown.
O-A is to check whether AAC/RS names the digest's serialization. If it does,
the reader simply lacked the method; if not, AAC has a gap.

**What this shows:** the early path's records are usable by an independent
reader from the files alone, which is the substantive claim. The examiner's
check had agreed with constructed accounts written by the same owner, but it
had not been tested against an independent one; this run exposed that
(coordinated-knowledge-work §3, shared basis).

**Routed:**
- O-C repairs RC-6 and RC-9 in the checker, and states any required claim
  keys in the brief and schema. The account stays as the evidence. If the
  schema changes so that this account no longer validates, a fresh reader is
  run on the same set.
- O-A takes the offerDigest serialization question.
