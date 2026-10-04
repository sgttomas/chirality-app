# EB-1 comparison — RR-EB1's account against the frozen key

- **Examiner:** O-E, 2026-10-04.
- **Inputs, each re-hashed before scoring:**
  - `RUN/RR-EB1/account.json` sha256 `018ebe7b2e60cfacefcff5e7638d0ebc3c107580bcb1f70abb4fadffd4148f7e`;
  - `RUN/RR-EB1/DISPATCH_RECORD.md` `427cd9ed…`;
  - `RUN/RR-EB1/SUPPLIED.sha256` `7057e452…`;
  - the frozen key `eb1/EB1_QUESTION_KEY.md` `0ef838449736e0442761309968c53c2e1aee661001e3088724f56df63d2e1f23`, unchanged.
- **The supplied set equals the frozen manifest.** In `SUPPLIED.sha256` the
  manifest (`907709e5…`), the brief (`3a9d2529…`) and the account
  (`e24101b2…`) equal the frozen hashes. So do `OWNER_DECISIONS_2.md`
  (`3a861c52…`) and `R23_RESOLUTIONS.md` (`d044bb92…`), which equal the
  manifest's items. The reader's RD-0 reports 44 items checked and 0
  mismatches. It reports reading nothing beyond the set.
- **Method:** each key item is marked as the key defines. Where the reader
  diverges from the key, the supplied record decides. Every miss or
  divergence is traced before any repair: to the **index** (my account), to
  the **records**, to the **reader**, or to the **key/brief** (my examiner
  design), the last recorded as a finding as directed.

## 1. Score

| Key items | Mark |
|---|---|
| K1.1, K1.2, K1.4 (crit); K1.5 (answered under Q8 "earlier_pins") | MATCH |
| K1.3 | MATCH against the frozen key, **but the key item is wrong** (finding KF-1) |
| K2.1, K2.2 (crit); K2.3; K2.4 (bounded-reconciliation, cited to LOOP_INIT §3) | MATCH |
| K3.1, K3.2 (crit) | MATCH |
| K3.3 | **MISS** (non-critical). Traced to key/brief: Q3 never asked about effort or uneven maturity (finding KF-3) |
| K4a.1, K4a.2 (crit; writer correctly `unknown`); K4a.3–K4a.5 | MATCH |
| K4b.1, K4b.2 (crit); K4b.3–K4b.5 | MATCH |
| K4c.1, K4c.2, K4c.5 (crit); K4c.3, K4c.4 | MATCH |
| K5.1–K5.6 (K5.3, K5.4 crit) | MATCH |
| K6.1, K6.3 (crit; the amendment reading rule is included); K6.2, K6.4–K6.6 | MATCH |
| K7.a, K7.b, K7.c (crit) | MATCH |
| **K7.d (crit)** | **DIVERGES from the key; the reader is right.** The key expects "not the owner's: HELP_HUMAN's ruling R23-31.5, an observation". The supplied `OWNER_DECISIONS_2.md`, at its frozen hash, records the owner's act of 2026-10-04: "Same-session review is acceptable.  It's a practical concession to making the logistics easier." Its effect: "R23-31.5 is confirmed as the owner's practice for design units". The reader answered exactly that, from records. This is not CONTRADICTED, which the key defines as conflict with the records. It is a key error (finding KF-2) |
| K8.1; K8.2 (crit) | MATCH |

**Totals.** 45 items, 23 of them critical.

| Reading | Critical | Non-critical | CONTRADICTED | Rule |
|---|---|---|---|---|
| **Literal, against the frozen key** | 22 of 23 MATCH (K7.d diverges) | 21 of 22 MATCH, 1 MISS (K3.3) | 0 | **Fails the pass rule** on one critical item |
| **Adjudicated** (each divergence decided by the supplied record) | 23 of 23 | 21 of 22 (95%) | 0 | **Meets the pass rule** |

I report both readings. The literal failure comes from a wrong key item,
not from a reader error and not from a gap in the records. Whether EB-1
counts as passed on the adjudicated score is HELP_HUMAN's call. I do not
decide it, and I have not used it to expand DEL-10-02 or DEL-10-04.

**Critical misses:** one. K7.d diverges from the key; the key is wrong and
the reader matches the records.

## 2. The reader's five disagreements, scored against the records

| # | Disagreement | Verdict | Traced to |
|---|---|---|---|
| D-1 | Review independence was settled by the owner, but the index treats it as HELP_HUMAN's observation | **Reader right.** `OWNER_DECISIONS_2.md` §"Review independence for design units" | **Index:** §2 has no row for the act; §2.1 and §6 say "observation for the 60% discussion". **Key:** K7.d (KF-2). Root cause in §3 below |
| D-2 | The human selected the manuals; WORKING_ITEMS only recorded the editions | **Reader right.** CURRENT_EXECUTION_BASIS: "The human selected the three manuals as core practice"; WORKING_ITEMS "records the following existing edition choices"; the scope phrase is "a parent clarification" by HELP_HUMAN | **Index:** §3.1 "records these as selected by WORKING_ITEMS". The key's K1.2 is right on who selected. It loosely attributes the scope phrase to WORKING_ITEMS rather than to HELP_HUMAN's confirmation that the record carries (KF-4, minor; no score effect) |
| D-3 | R23-31.3 conflicts with CURRENT_EXECUTION_BASIS l.11 ("a later undertaking or changed source must bind its own applicable basis before reliance") and with OI-017 | **Reader right.** R23-35 now supersedes R23-31.3 | **Index:** §3.3 followed R23-31.3; in the survey I proposed the reading that became that ruling. **Records:** the gap was real. Pass 4 had no basis binding; `RUN/BASIS_BINDING.md` (`93160e1d…`) now supplies it. **Key:** K1.3 (KF-1) |
| D-4 | Omissions: B-12 lists only part of the direction; the download approval; R23-32 F-R16; R23-34 item 9; §4 cites DEL-10-04 REQ-007, which was not supplied | **Reader right on all five.** None contradicts a record | **Index** (incompleteness). The input-set design adds one: the index relied on a source it did not supply |
| D-5 | Seven `unknown` answers | **Each is a correct `unknown`.** Group3's writer (the key expects `unknown`). The transcriber of SCA003's OWNER_DECISIONS (not supplied). LOOP_INIT's approver: no decision record exists; commit `afc65e2b22`'s message says "Owner-directed manual-led loop adaptation" (author Codex HELP_HUMAN; merged in PR #1037), so it is an author's statement, not an owner record. Pass 4's selection of bounded-reconciliation: no pass-4 record names it; BASIS_BINDING lists only the two methods. The A/C direction text (in `DECISION_BRIEF.html`, not supplied). The Git-based claims (the index stated them; they are O-E's checks and not in the set). A 60% assessment outside the set | Not reader faults. **Index:** it presented Git checks as if they were record facts and should label them as O-E's tool checks. **Input-set design:** A/C not supplied. **Records:** LOOP_INIT's owner direction has no decision record (carried as a limit) |

## 3. Root cause of KF-1 and KF-2, and of D-1 and D-4

I built the manifest from the working bytes at freeze. Those bytes already
held `OWNER_DECISIONS_2.md` §"Review independence" and R23-32…R23-34. But I
wrote the account and the key from my earlier reads (the survey, and R23-31
only), and I did not re-read the supplied records' changed sections before
freezing. My checker verified the hashes, not the content against the hashed
bytes.

**Practice observation, for DEL-10-02 (R23-31.4):** at freeze, re-read every
changed section of every supplied record that the key or the index relies
on. A hash check does not detect a stale reading. This is the
"stale-reading" counterpart of tranche 1's "checker agreed only with its
own author".

## 4. Key findings (the key is not changed)

| ID | Item | Finding | Effect |
|---|---|---|---|
| KF-1 | K1.3 | It expects R23-31.3's rule, which R23-35 supersedes. The correct expectation is CURRENT_EXECUTION_BASIS l.11 and OI-017: each later undertaking binds its own basis before reliance, possibly by reference after re-hashing (R23-35) | The literal MATCH stands; the reader also exposed the conflict |
| KF-2 | K7.d | It was written without the supplied record's owner act. The correct expectation: an owner act of 2026-10-04 confirming R23-31.5 as practice for design units (a logistics concession, not a claim of model-family independence) | Literal divergence on a critical item; adjudicated MATCH |
| KF-3 | K3.3 | Q3 did not ask about effort or uneven maturity, so the key item was never elicited | MISS is not attributable to the reader |
| KF-4 | K1.2 | The scope phrase belongs to HELP_HUMAN's confirmation recorded in CURRENT_EXECUTION_BASIS | None |

## 5. Repairs made (index only; records are HELP_HUMAN's)

The account goes from EB-v0.1 to EB-v0.2. The repairs are listed in its
"Changes" section and in `RUN/OWNERS/O-E.md`.

## 6. Corrections after RV3 (dated 2026-10-04; earlier sections left as written)

- **D-5, LOOP_INIT's approver: my trace to "Records" was wrong (RV3 EB2-R1;
  R23-42.1).** A decision record exists outside the input set:
  `docs/governance_harness/tranche_manifests/APP-V4-LOOP-ENTRY-20260928.yaml`
  `m2_gate`. It records:
  - the owner's request ("Owner copied init/ and loop/ … and requested:
    Revise the documents accordingly for the new project folder.");
  - `authorized_by: Ryan`;
  - integration owner Codex HELP_HUMAN `/root`, self-merged under the
    owner-authorized PR gate.

  No record shows the owner reviewed the resulting text. The reader's
  `unknown` stays correct for IS-EB1-1, which did not supply that file. The
  miss is traced to the **index and the input-set design**, not the
  records. EB-v0.3 adds it as B-19.
- **Further key findings** (the key is unchanged; no score effect):

| ID | Item | Finding (from RV3) | Effect on RR-EB1's score |
|---|---|---|---|
| KF-5 | K8.2 (critical) | It rests on the index's own inference ("no departure awaits the owner"; OI-019/020 "not triggered"). No primary record states that. Carried amendment wording reaches the owner at the next amendment's checkpoints (R23-11), so naming it would not be a contradiction. It should have been non-critical, or restated from the records | None: the reader answered "none recorded … (inferred)", with sources |
| KF-6 | K3.1, K4c.2 (critical) | They require elements the question did not ask for (the recorder `/root`; the tranche manifest). These should have been optional | None: the reader gave both |
| KF-7 | K2.2 (critical) | The pass-4 work graph's header says "(owner's selection …)", while `OWNER_DECISIONS.md` separates the owner's direction from HELP_HUMAN's selection. A reader who reports both wordings should MATCH | None: the reader reported direction and selection |

The totals in §1 stand: literally 22/23 critical, and 23/23 when each
divergence is decided by the records.
