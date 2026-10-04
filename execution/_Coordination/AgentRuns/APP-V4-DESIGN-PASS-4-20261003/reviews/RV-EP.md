# RV-EP: review of EP-05 (DEL-09-05, FW-04) and EP-11 (DEL-09-11 reader method), owner O-C

- **Reviewer:** RV (Type 2 TASK, Claude Opus 5.5), run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-03.
- **Method:** `coordinated-knowledge-work` §3.
- **Basis:** rulings R23-6 (as revised), R23-8, R23-10, R23-19, R23-20, R23-21, R23-23, R23-24 and R23-25, cited by ID. The R23 file is append-only.
- **Owner's record:** `OWNERS/O-C.md`, "EP — refrozen".
- **Scope:** under R23-24, FX-DP1 will change shape. So I reviewed EP-05's and EP-11's design now and judged the fixture-dependent results against the current FX-DP1 (manifest `346191ff…`).

**Bytes reviewed.** Each was recomputed with `shasum -a 256` and matches O-C.md.

| File | sha256 |
|---|---|
| DEL-09-05 `DECISION_ATTRIBUTION_CASE.md` (DAC-v0.1) | `52224eae0d2b7386cf8e1ecbbd751f3d536cca0a976165b61352bc7f3173fa3c` |
| DEL-09-05 `prototype/fw04_check.py` | `4b54169825db7000…` |
| DEL-09-05 `prototype/fixtures/examiner_observation.FX-DP1.json` | `afc9df9d08748868…` |
| DEL-09-11 `READER_METHOD.md` (RRM-v0.1) | `5ca52e23d000250235da3c1f4430dab4a3dfc212e13dccbf6148e978f4c22faf` |
| DEL-09-11 `rrm.input-set-manifest.schema.json` | `a1f03a374b5b69d2…` |
| DEL-09-11 `rrm.reconstruction-account.schema.json` | `26d0d2e08e06c8cf…` |
| DEL-09-11 `prototype/rrm_compare.py` | `80410be423f39345…` |
| DEL-09-11 `prototype/run_standing_check.py` | `f480aaf7dc74ee81…` |
| DEL-09-11 `IS-FX-DP1-2.input-set.json` | `e615aeeeaa1d5db3…` |
| DEL-09-11 `definitions/aac-offer-digest-0.1.md` | `832d67c73a8492d7…` |
| DEL-09-11 `READER_BRIEF.FX-DP1.md` (v0.2) | `9b7d6a0ee4d875e2…` |

## Verdict: **READY**

There are no BLOCKING or MAJOR findings: 3 MINOR and 4 NOTE.

The fixture-dependent results hold on the current FX-DP1 and must be rerun on the R23-24 manifest. The MINOR findings can be repaired at that rerun.

## Findings

### EP-R1 — MINOR — an examiner judgment is not bound to the account it judges (RRM §5 RC-9; `rrm_compare.py`)

- **What the method requires.** RRM §5: "The examiner's recorded judgment decides: *absence* holds, *unsupported* fails."
- **What the file contains.** The judgment file `judgments.independent.RR-E.json` names its account and hash in an `account` string and its maker in the `basis` prose.
- **What the code does.** `rrm_compare.py` reads only `judgments[claim_id]`. It never compares `account` with the account given, and records no examiner identity.
- **Probe.** A judgment file naming "some other account" still turned RC-9 for C-09 from REFER to HOLDS (9 checks, 0 referred).
- **Consequence.** A judgment can be applied to an account it was never made on, for example a later account that reuses the claim id C-09, with nothing recorded to show the mismatch.
- **Repair.**
  - Require `account` as the account's sha256, and check it in `rrm_compare`.
  - Require an `examiner` identity in the judgment format.
  - Put the judgment's reference and hash into the EXP record's evidence.
  - Add a mismatched-judgment case to the standing check (SC-2).

### EP-R2 — MINOR — FW-04's agent-actor rule tests a shape RS refuses, and misses the shape RS allows (DAC §3 R-3; P04-C N-1; `fw04_check.py` `decision_for`)

- **What RS allows.** RS's `decisionActor` is `$defs/person`, with `additionalProperties: false`. It has no `kind` element.
- **What R-3 tests.** R-3 detects an agent only when `actor.get('kind') == 'agent'` or the display name is missing.
- **What N-1 builds.** N-1 builds `{'kind': 'agent', …}`, which the RS schema would reject. So N-1's expectation, "an act whose actor is the agent decides nothing", holds only for a record that cannot be written.
- **Probe on the current fixture.** I gave PKG-1's A16 the RS-valid actor `{'displayName': 'thread:fx-u1-manager', 'identityVerified': false}`, the requesting agent's own thread, with capture evidence agreeing. FW-04 counted it as the decision. Without agreeing capture evidence it fails only at R-5.
- **Consequence.** On a candidate, R-7 (the examiner's observation) would still catch it. P04-C's mechanical negative does not.
- **Repair.**
  - Make R-3 compare the actor with the package's requester and the run's agent identities.
  - Validate the mutated records against RS before applying the rules.
  - Rewrite N-1 in an RS-valid shape.

### EP-R3 — MINOR — open-matter tables still list closed matters

- **RRM.** UNRESOLVED still lists "`offerDigest` serialization … O-A" and "A16 rows refrozen (E-1)" as open. RRM's own header says AAC-v0.3 §5.1 answers the first and that E-1's versions are adopted.
- **DAC.** §6 calls the EXP result schema "O-B's repair in progress", and its UNRESOLVED lists "EXP refrozen | O-B". EXP-v0.2 is refrozen and confirmed READY (`reviews/RV-EXP-U1.md`). DAC §7's DEL-09-01 row also reads "EXP repair in progress".
- **Consequence.** A reader cannot tell which matters are actually open.
- **Repair.** Close the rows, cite where each was answered, and pin EXP-v0.2 as DOS does.

### EP-R4 — NOTE — P04-A finds the reserving basis by a phrase in `purpose`

- **The check.** P04-A requires the package to name "the reserving instrument". `fw04_check.py` checks for the substring "reserved to the person by" in the request's `purpose`. Neither CE-4 nor RS had an element for it.
- **What R23-24 changes.** R23-24 item 1 puts "the basis that reserves the decision" into the package file's new `$def`. Item 2 does not list it among the record's elements.
- **At the rerun.** FW-04 should read the basis from that element, through the package file the request cites. If O-A adds it to the record, FW-04 reads it there. The purpose phrase should not remain the basis of the check.

### EP-R5 — NOTE — FW-04 is independent of the decision view in code, but shares one unratified choice

- **Code independence.**
  - `fw04_check.py` imports nothing from `decision_view.py`; I grepped for imports and DV references and found none.
  - Its control flow and data structures differ.
  - It adds rules the view does not have: R-3 actor and recorder, R-5 capture agreement, R-7 examiner observation.
- **Rule correspondence.** R-1, R-2, R-4, R-6 and R-8 express the same semantics as DV-4…DV-7. Both rest on the shared basis (RS §6.1 and §7, the ACT A16 rows). That is expected, and DAC §6 correctly calls the agreement "consistency … not that the basis is sound".
- **R-6.** R-6 ("the latest in written order is shown") repeats DV-6's choice, which no basis text makes. R23-25 now gives that decision to O-A. Until O-A states it, agreement on R-6 is not independent evidence. R-6 should cite O-A's ruling when it lands.

### EP-R6 — NOTE — the `definition` item keeps the reader separate; one rule is not enforced

- **Separation holds.**
  - The definition is a verbatim excerpt of AAC-v0.3 §5.1. I compared lines 240–255 of `APP_ACT_CONTROL.md` (`45b13f15…`) with the excerpt body: 16 lines, equal.
  - It names its source path and hash, and the input-set schema requires `source` for a `definition`: removing it makes the set invalid.
  - It is published contract text, not run content, an author's working context or a derived view. So R23-10's separation and REQ-004 are kept.
  - Its provenance line mentions "E/RR-E" and `nir_model.canonical()`. These are pointers to material that is not supplied and gives no content about the run, so they are harmless.
  - All seven items of IS-FX-DP1-2 hash-match the current FX-DP1 and the definition file.
  - Both input sets validate against the input-set schema, and both DEL-09-11 schemas pass `check_schema`.
- **Not enforced.** RRM §3 says a definition "may support a check, never an act or an outcome". `rrm_compare` does not enforce that for decision claims.
  - Mitigation: RC-6 and RC-7 compare decisions with the records anyway, and RC-9 refers an outcome claim citing a definition.
  - Repair: a one-line RC-5 extension would make the rule mechanical.
- **No reader has run on IS-FX-DP1-2 yet,** so the digest check has not been exercised by a reader. RRM states this.

### EP-R7 — NOTE — RC-9 refers more than it needs to

`outcome_record` counts only `host_evidence` items as outcome records. A `change` or `outcome` claim sourced from an RS outcome entry (standing `record`) is therefore always referred. This errs on the safe side: no claim holds without an examiner. On a host journey it will refer many claims, so the examiner's workload should be expected.

## Probes the coordinator named

| Probe | Result | How |
|---|---|---|
| **RC-9 referral: is it sound, and is "with no judgment the check is never held" enforced?** | **Sound and enforced; one gap (EP-R1)** | Without a judgment, the code appends `ok=None`, and RC-9 is never a HOLDS. I ran `rrm_compare.py` on the RR-E account and inputs without judgments: RC-1…RC-8 hold, RC-9 is REFER (C-09), exit 2, and the EXP record's outcome is `inconclusive` (schema-valid). With the judgment file: 9/9 hold, exit 0. An unknown judgment value ("maybe") keeps the check referred. The referral is the right design: a statement of absence filed under `outcome` is indistinguishable by mechanism. The gap is that the judgment is not bound to the account it judges |
| **C-09 attributed to HELP_HUMAN?** | **Yes** | The judgment file's `basis` says: "Judged by HELP_HUMAN in RR-E/RESULT.md ('a truthful statement of absence') and confirmed independently by O-C against the log". `E/RR-E/RESULT.md` is headed "(HELP_HUMAN)" and contains that phrase once. The claim C-09 in the RR-E account reads "The record log has nothing after seq 3 …", and the supplied log has exactly 3 lines (`wc -l`). The attribution is in prose only; see EP-R1 |
| **Digest rule as a `definition` item: is separation kept?** | **Yes** | EP-R6 |
| **FW-04 rules independent of DEL-06-02's view rules?** | **Yes in code and derivation; shared semantics on the common basis; R-6 is a shared unratified choice** | EP-R5 |

## Owner checks rerun (not rebuilt), against the current FX-DP1 (`346191ff…`)

- **`fw04_check.py`.**
  - Run from the DEL-09-05 folder with `--criterion ScopeOfWork.md` (sha256 `35c8ea5a…`, matches DAC).
  - Result: **19 expectations, 0 failed**. The fixture was unchanged afterwards, and five EXP records are schema-valid against EXP-v0.2 (`f7871c96…`).
  - Correction to DAC §6: the documented command passes `--criterion ScopeOfWork.md`, which resolves only from the deliverable folder, not from `Design/`.
- **`run_standing_check.py`:** **12 cases, 0 unexpected**.
- **RR-E inputs.** `fixtures/RR-E-input/` matches `E/RR-E/SUPPLIED.sha256` (9/9 OK). `account.independent.RR-E.json` is byte-identical to `E/RR-E/account.json` (`cmp`).
- **`rrm_compare.py` on the RR-E account:** without the judgment, 8 hold, 1 referred, exit 2, outcome `inconclusive`. With the judgment: 9/9, exit 0.

## Design checks (by reading)

- **FW-04 against VER-004 and REQ-004.**
  - The positive record (P04-B) is checked against an examiner's native observation (R-7). FF-4 makes it *inconclusive* without that observation, never a pass from the record alone.
  - The negatives (P04-C) cover message text, success, timeout, returns, silence and wrong-kind acts.
  - P04-E imposes no order on separate acts.
  - Outcomes follow R23-19 and R23-20: no part is declared not applicable, and P04-B without the person is *not run* or *blocked*.
  - P04-E's in-memory A4 carries no `requestRef`, so it shows independence trivially. It does not show that "not required before" holds when a real A4 shares the undertaking. That is acceptable for a rehearsal.
- **RRM against R23-6, R23-10 and REQ-004.**
  - The three roles (assembler, reader, examiner) are kept apart.
  - Separation evidence is stated for a person reader and an agent reader, and the host's enforcement limit is stated (RR-E's dispatch record says it was not enforced).
  - Timing adds no calendar arithmetic, and a synthetic clock or reread does not count.
  - RC-10 and AC-002 are honestly stated as unpassable against SWBPIPE's session-only receipts.
  - The withheld list now uses DOS's `derived_view` class, which matches the repaired DOS §5 and DJ-1 (`reviews/RV-LHQ-U2.md`).

## Not checked

- The R23-24 refreeze of FX-DP1, which does not exist yet. O-C reruns on the new manifest, and I confirm that rerun when it is sent.
- A reader run on IS-FX-DP1-2. None has been made.
- DEL-09-05's later units: the V4-EXM-13 undertaking and the delegations.
