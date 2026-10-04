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

## Repair confirmation and rerun on FX-DP1 `9501ef81…` (2026-10-03)

- **Bytes reviewed.** Recomputed with `shasum -a 256`; all match O-C.md "Minor repairs after RV's confirmations…":
  - DAC `bf0ddb6a…7a808d62`, `fw04_check.py` `e57359d3…2a5229b9`
  - RRM `7446d056…bfcec343`, `rrm_compare.py` `d445740e…daa5e8d8`, `run_standing_check.py` `6ff45447…938113d6`
  - `judgments.independent.RR-E.json` `1b2952bf…f726ac24`, `judgments.bad2.json` `c22e0ab1…6416eb99`
  - `IS-FX-DP1-3.input-set.json` `18b9e49b…6978c17f`, `account.good.IS-FX-DP1-3.json` `f977804d…57b6eb01`, `account.rre-shape.IS-FX-DP1-3.json` `0aece549…d8eecd7a`
- **Owner checks rerun, not rebuilt:**

| Check | Result |
|---|---|
| `fw04_check.py` (DAC §6 command, run from the deliverable folder, with `--rs-design` and `--as-design`) | **22 expectations, 0 failed**, including "every fixture record is valid against RS (with its CE-4 and AS references)" |
| `run_standing_check.py` | **17 cases, 0 unexpected** |
| O-A's `E/run_e.py` | **56/56** |

### Verdict: **CONFIRMED — READY**

No finding of mine is open. One NOTE follows on the new subject rule; it is not blocking.

| Finding | Status | Confirmed against |
|---|---|---|
| EP-R1 MINOR | **Repaired** | `bind_judgments` (`rrm_compare.py`) applies a judgment file only if it names `account` {account_id, sha256 of the given account file} and an `examiner`. Otherwise the file is ignored, with the reason recorded as a limit. The RR-E judgment file (format 0.2) names `RR-E-FX-DP1-ACCOUNT-1`, `637e234c…`, and examiner "HELP_HUMAN (Claude Code session), confirmed by O-C". Standing check SC-2 covers a judgment bound to another account and the judgment file of another account: both are ignored and C-09 stays referred. A mutated account no longer inherits the judgment |
| EP-R2 MINOR | **Repaired** | R-3 (DAC L62; `decision_for`) refuses an actor whose `displayName`, `osAccount` or `codexAccount` equals the package's requester or any agent requester in the record set. Every constructed `human_act` is validated against RS. N-1 is now RS-valid, with agreeing capture evidence, and is stopped by R-3 alone ("decision actor is an agent of the run or the requester"). **Limit, noted:** "agent identities" are taken only from `act_request` requesters. On a candidate, other agent identities in the run (children, recorders) are not in that set. R-7, the examiner's observation, still covers that case; on a candidate the run-author list would be a fuller source |
| EP-R3 MINOR | **Repaired** | DAC pins EXP-v0.2 (`fc5b8230…`, `f7871c96…`; header L18, §7 L148), and its UNRESOLVED has no EXP row. RRM's UNRESOLVED no longer lists the digest serialization or the A16 refreeze |
| EP-R4 NOTE | **Adopted** | P04-A reads `reservedBy` from the package file and checks that the file's alternatives equal its request's. Both packages hold |
| EP-R5 NOTE (R-6 and R23-25) | **Adopted** | DAC R-6 (L65) matches ACT, RS HA-11, DV-6 and FR RF-6. It is exercised both ways (22-run lines "R-6: a later A16 … supersedes (ALT-1) … earlier stays listed" and "a correction … is not a new decision"). The correction chain is applied before kind and alternative checks |
| EP-R6 NOTE | **Adopted** | RC-5 (RRM L82; `rrm_compare.py` L66–70) refuses a decision, acceptance, change or outcome claim resting on a `definition` item. Standing-check case SC-2 "a decision claim resting only on a definition item" → RC-5 fails |
| EP-R7 NOTE | Kept, as stated | — |
| DAC §6 command path | **Repaired** | The command runs from the deliverable folder, and the documented flags are complete |

**The new subject rule (a namespaced `packageId` also matched by its unique last segment): sound, with one gap.**
- **What is sound.**
  - The rule is stated where readers and examiners look: RRM §4 L70, the brief and the schema description.
  - It only widens how the *examiner* recognises a subject the reader named. It grants no claim content.
  - Its uniqueness guard compares tails exactly.
  - A wrong assignment fails toward RC-6 or RC-7 failures rather than toward false passes, because a claim assigned to two packages is compared against both.
- **The gap.** `mentions()` treats `-` (and `.`, `:`) as a boundary.
  - So the tail `PKG-1` also matches the text `PKG-1-b`. I checked this directly: `mentions("PKG-1-b decision", "PKG-1")` is True.
  - So two packages with tails `PKG-1` and `PKG-1-b` both pass the exact-uniqueness check, yet a claim about `PKG-1-b` is also assigned to `PKG-1`.
  - A short generic tail would match ordinary words: a tail `a` matches "a decision".
- **Suggested hardening** (NOTE, not blocking):
  - Admit a tail only if it mentions no other package's identifiers and none of theirs mentions it.
  - Or require a tail to contain a digit, or be at least some length.
  - Add a standing-check case with overlapping tails.
- **When RR-F lands.** I will judge the rule against its real account: whether the reader used tails at all, and whether any claim was assigned to an unintended package.

## Hardenings confirmation: subject rule, RR-F, RW-1 and re-pins (2026-10-03)

**Bytes reviewed.** Recomputed with `shasum -a 256`; all match O-C.md "RR-F and RV's two hardenings" and "FV-4a":

| File | sha256 |
|---|---|
| DAC | `1fc4fd272c4f155c04f6367fb2e2562071536c78dea579dd1cfedbb889d5756c` |
| `fw04_check.py` | `e57359d3…29b9`, unchanged |
| RRM | `3a4a1462…7673` |
| `rrm_compare.py` | `48630745…7be8` |
| `run_standing_check.py` | `8eb1bd19…3b46` |
| `account.independent.RR-F.json` | `8188caba…92c0` |

`account.independent.RR-F.json` is byte-identical to `E/RR-F/account.json` (checked with `cmp`).

**Checks rerun, not rebuilt.**
- `fw04_check.py`, from the deliverable folder with the RS and AS design flags: **22 expectations, 0 failed**.
- `run_standing_check.py`: **19 cases, 0 unexpected**. These include:
  - RR-F as SC-1's second independent case: no failure, nothing referred;
  - the new overlap case.

### Verdict: **CONFIRMED**. Nothing is open from me on EP-05 or EP-11.

| Item | Result | Evidence |
|---|---|---|
| **Subject-rule hardening** | **Sound.** No longer over-lenient on the cases I raised | `mentions()` (L38–41) now treats `-`, `_` and `:` as continuing an identifier, so `pkg:t:PKG-1` is not found inside `pkg:t:PKG-1-b`. A trailing `:` or `.` still ends one, so "PKG-1: request" and "PKG-1.json" match as intended. `package_identifiers()` (L43–56) admits a tail only if it is unique, not contained in any other package's identifier, and contains none of them. That is a substring test, so a short generic tail (e.g. `a`) is also refused, because it occurs inside the file paths. The SC-2 case shows PKG-1 / PKG-1-b admitting no short form and PKG-1 / PKG-2 admitting theirs. RR-F used full ids, so the rule was not exercised by an independent reader, as the coordinator said |
| **RW-1 (DAC §6.1)** | **Adopted** | It states that the V4-EXM-13 joined witness treats *ready* and *ready (qualified)* (and `readinessQualified`) as ready, keeps the qualifier and its first cause, never reports a qualified row as bare *ready*, and names the expected label in rebuilt states. It cites `FLEET_VIEWS.md` at `15e25a24…1b85`, the version I confirmed. §7's DEL-06-02 row names it |
| **Re-pins** | **Correct** | DAC (L13) and RRM pin RS at `2e7afb1b…30ff`, and DAC states that R-6 relies on the new L-0 A16 sentence. I checked every 64-hex pin in DAC and RRM against current files. RRM: all match. DAC: all match except `fc5b8230…` (EXP-v0.2). Its `git show 09ca67d094:` bytes give `fc5b8230…`, and the working-copy diff from that commit is the U-EXP-1 closure only (6+/4− lines; no rule, schema or example). So keeping that pin is right under R23-21 item 3 |

**Note on the RR-F evidence I relied on.** `rrm_compare` gives 9/9 with nothing referred on RR-F. I relied on the standing check's SC-1 case for this and did not re-read RR-F's account claim by claim.
