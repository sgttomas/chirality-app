# O-C — owner notes and returns (DEL-09-05, DEL-09-07, DEL-09-11)

Owner: O-C (Type 2 TASK, Claude Opus 5.5, high effort; the S1-C survey agent). Method: `coordinated-knowledge-work` (workflow sha256 `44049bcd38b88378cd757ea34516f01edb0b0e93d8e9e3ac2b47ac61c9271b18`) under this run's work graph "Coordination". Pin basis for every unit: written for either Codex pin (R23-3).

## Units

| Unit | Deliverable | Path (from `projects/chirality-app-v4/execution/`) | sha256 | State |
|---|---|---|---|---|
| LHQ-U1 | DEL-09-07 | `…/DEL-09-07_Local host candidate qualification/Design/LOCAL_HOST_QUALIFICATION.md` | `4ee7de2630b7ed9ea1870bca938c434971f71e5413b60bb2e3247c5fc73931bc` | READY (RV); header wording fixed (R23-23) |
| LHQ-U2 | DEL-09-07 | TOP, DOS and three schemas with examples | see "Minor repairs after RV's confirmations" | READY (RV); U2-R10…R12 repaired, for RV's confirmation |
| EP-05 | DEL-09-05 | DAC-v0.1 and prototype | see "Minor repairs after RV's confirmations" | READY (RV); EP-R2…R5 repaired, rerun on the R23-24 fixture: 22/22 |
| EP-11 | DEL-09-11 | RRM-v0.1, schemas and prototype | see "Minor repairs after RV's confirmations" | READY (RV); EP-R1, R3, R6 repaired, rerun on `IS-FX-DP1-3` |

## LHQ-U1 — frozen

**Claims.**

1. Four cases, LHQ-20…LHQ-23 (V4-EXM-20…23 on the embedded variant CA/E), are written step by step against DEL-09-06's step map (CA-0…CA-R) and the FX-PIPE-01 timeline. Each step states its stimulus, its expected observation, the evidence that must exist and the contract the expectation comes from (§5).
2. The operation is a parameter. Thirteen slots carry fixture bindings, and binding rules BR-1…BR-4 keep the cases unchanged when OI-021 is decided (§2.1).
3. Two local cases fill fixture gaps, returned to the C owner as F-1 and F-2. L-LHQ-1 adds the solve that V4-EXM-20 requires. L-LHQ-2 adds a third PR-2 item so that "accepts some row by row" can be shown with two individual acceptances.
4. The candidate-identification record has 14 elements, each with source and standing, under rules CI-1…CI-4 (§3).
5. The external-contribution ladder is CA §7.2's, consumed unchanged. HC-1…HC-13 list the host contributions the cases need. All stand at *answered*; none is committed, delivered, adopted or examined (§4).
6. Failure behaviour: the applicable CA rows are named, the inapplicable ones are excluded with reasons, and 13 rows of this deliverable's own are added (LF-1…LF-13). Outcome rules LR-1…LR-7 follow CA W-R1…W-R7 (§6).
7. The per-case SWBPIPE gap sheet uses only the answers' own labels. Against SWBPIPE now, 0 of 4 cases can start, and V4-EXM-20 as written cannot pass against its current product: Apply works per batch and keeps no reject record (§7). No SWBPIPE observation is claimed.
8. LHQ-23 adds in-run stimuli taken from LOOP's MS cases, so that V4-EXM-23's four properties are exercised during V4-EXM-20 (F-3, open to the integrator). A completeness rule makes partial capture *inconclusive*, never *passed*.

**Checks run.**

- Every 64-hex pin in the file (20 of them) was recomputed against the current files with Python `hashlib` over the project tree: 20 of 20 match the file each one names.
- Cited identifiers were spot-checked in their sources by script: ACT §2.2, §2.7, §5.4; RS R10, R15, R16, `act_request`, HA-1, `destination_declined`; EXEC RP-1, PH-2, PH-10; GUIDE HC-7.3; WD-EX E1c and `CP-check`.
- The CA rows CAF-1…CAF-39, LOOP NW-8…NW-16 and MS-01…MS-27, AS §3, §3.2, §5 and §7, C §10.1–§10.3, and P §4.3 were read in full before citing.
- No home path is written in the file.
- No JSON was written in this unit, so there was nothing to validate.

**Open.**

- The observation method, its privilege and its blind spots; the dossier; the handoffs to DEL-11-03 and DEL-09-11; the schemas. These are LHQ-U2.
- OI-021 slot binding.
- HC-1…HC-13 (host joins deferred).
- The A12 mapping and boundary-refusal recording, in the deferred queue (R23-14).
- S-01-4.
- OI-013/014: what the App candidate contributes to an embedded journey.
- DEP-05-01-024.
- DEL-09-01's record form (O-B).
- Findings F-1, F-2 (C owner), F-3 (integrator), F-4 (receivers sentence; next amendment, R23-11), F-6 (W14-04 overlap noted).

**Adoption of R23 at freeze.** R23_RESOLUTIONS.md is pinned at `793de2b2…` (R23-1, R23-3, R23-5, R23-7, R23-11, R23-14). R23-8 and R23-10 do not bear on DEL-09-07; they are for EP-05 and EP-11. R23-6 as revised is for EP-11.

**Write fence.** I wrote only this file and the one Design file above.

## LHQ-U1 repair (review `reviews/RV-LHQ-U1.md`, verdict REPAIR: 4 MAJOR, 7 MINOR, 2 NOTE)

Repaired in place; the table of repairs is the file's last section ("Changes at repair"). Summary:
- R1: §5.0 places every requirement V4-EXM-20…23 verify; LHQ-20 gains 20-4a, 20-4b and part P20-E (parity, P §2).
- R2: the completeness rule covers every capture-based part, including P23-B.
- R3: slot `WF-22` = WD-EX E1d; LHQ-22 chains E1d then E1 (L-2 (a)).
- R4: BR-3 needs two classes on a candidate; the fixture's scope separation is a labelled stand-in; U-02 is in UNRESOLVED; LF-16 added.
- R5: R23 re-pinned; R23-15/R23-16 cited; F-1…F-3 closed.
- R6: CAF exceptions are listed per row; LF-14 added.
- R7: lost acknowledgement now comes before the solve; P20-A does not depend on it.
- R8: stimuli come from the person's request and examiner test endpoints; LF-15 added.
- R9: outside-process traffic is reported under 23-7.
- R10: LHQ-21's standing and lapse subject are named.
- R11: BR-4 and the precondition now agree.
- R12: capture and recording are worded apart.

**Pins after repair.**
- R23 is re-pinned to `e4be2c2a…`; its later addition, R23-17, concerns O-B only.
- ACT and RS are pinned at their committed bytes (commit `cec590c5c3`). O-A's working-tree A16 rows change them; the sections cited are not affected, and this is noted in the header.
- All other pins match their current files (script).

**LHQ-U2 alignment with the repairs.**
- TOP gains the outside-process attribution class and the extended completeness rule.
- The traffic schema gains `outside_process_unsandboxed` / `reported_within_limit`, with a new invalid example.
- The CIR schema gains slot `WF-22`.
- All three schemas pass `Draft202012Validator.check_schema`. Every valid example validates and every invalid example is rejected, under both `jsonschema` 4.26 and DEL-01-01's subset validator.

## Replies to RV-LHQ-U1 (review file sha256 `10d451f7…66d1`), one per finding

Repaired file: `LOCAL_HOST_QUALIFICATION.md` sha256 `2f648e5bb09d3727fad991fa84e6d3392d3a2a739ed3c16ad2b228cbcbfa1457`. The file's last section, "Changes at repair", carries the same table.

| Finding | Reply | Where to check |
|---|---|---|
| LHQ-R1 MAJOR | Accepted. Every requirement V4-EXM-20…23 verify is placed in a part. Parity is examined: one catalog, same views and marks, same route, validation, outcomes and errors (P §2) | §5.0; steps 20-2, 20-4, 20-4a, 20-4b, 20-10; part P20-E |
| LHQ-R2 MAJOR | Accepted. The completeness rule covers every part that uses the capture, including P23-B and P23-E as far as its traffic is used; a failed observation still fails | §5.4 rule; LF-9; TOP §7 (U2) |
| LHQ-R3 MAJOR | Accepted. New slot `WF-22` = WD-EX E1d `label-with-grant` (with E1c's `CP-check`); run 1 observes `CP-grant` (22-1) and `CP-check` on the OP-C9 receipt (22-3); run 2 (E1) requests `OP-GEOM` (22-6), chained sequentially (L-2 (a)) | §2.1 table; §5.3 "Workflows" and steps |
| LHQ-R4 MAJOR | Accepted. On a candidate, BR-3 requires `OP-LOW` and `OP-GEOM` in different classes. The fixture's scope separation is labelled "fixture stand-in" and cannot pass P22-B. U-02 is listed with its owner and point of need | BR-3; §5.3 "Class separation"; 22-0, 22-1, 22-6; LF-16; UNRESOLVED |
| LHQ-R5 MINOR | Accepted. Rulings are now cited by ID (R23-21) instead of by file hash. R23-15 is cited for the added stimuli, now called "added stimuli"; R23-16 for L-LHQ-1/2 as local additions. F-1…F-3 are closed | Header; §2.2; §5.4; Findings |
| LHQ-R6 MINOR | Accepted. CAF-6, CAF-7 and CAF-34 are not applicable on E, with reasons. The reporter for CAF-11, CAF-15 and CAF-32 is restated as the host loop. LF-14 replaces CAF-34 | §6.1 |
| LHQ-R7 MINOR | Accepted. 20-11 is now the lost acknowledgement of 20-10's application and its recovery; the solve moves to 20-12, after the application is observed. P20-A takes 20-10 from its direct or recovered observation and does not depend on 20-11 | §5.1 steps and parts; L-LHQ-1; §7 rows |
| LHQ-R8 MINOR | Accepted. Each stimulus is produced by the person's request and served by examiner-run test endpoints, declared by fixture tools; no third party is contacted. 23-3 has two concurrent calls and a later second need. 23-2's named entry is an API, not MCP. LF-15 records an unproduced stimulus as *not run* | §5.4 stimuli; 23-2, 23-3; LF-15 |
| LHQ-R9 MINOR | Accepted. 23-9 compares the host process's own contacts; an unsandboxed outside process's traffic is reported under 23-7 and not counted against P23-A or P23-D | 23-9; TOP §3, §7; traffic schema `outside_process_unsandboxed` |
| LHQ-R10 MINOR | Accepted. 21-1 expects *unavailable* or historical results (or current results after a solve); 21-2 requires the referent's standing; 21-7 names T2's A4 lapsed by T14, with T6 as the unrelated-edit control | §5.2 |
| LHQ-R11 MINOR | Accepted. The LHQ-20 precondition allows BR-4; BR-4 states what LHQ-22 needs | BR-4; §5.1 preconditions |
| LHQ-R12 NOTE | Accepted. The act is captured by the host's act facility and recorded by the host run recording (RS §3) | §5 lead; 20-9 |
| LHQ-R13 NOTE | No change | — |
| LHQ-R14 MINOR (cross-owner; ruled R23-19, R23-20) | Adopted. LR-4: not-applicable parts are declared in the case binding before the run, with reason, and left out of aggregation; an applicable part not run makes the case unable to pass. P22-G and P23-E state their declaration rule; an outside process starting when undeclared makes LHQ-23 *inconclusive*. LR-3, LF-1, LF-2 and CI-3 use R23-20's definitions; every planned case gets a record | LR-3, LR-4; LF-1, LF-2; CI-3; P22-G; P23-E |

**Pins after the repair (script, 2026-10-03).**
- `LOCAL_HOST_QUALIFICATION.md`: 19 pins. Every one matches a current file, except ACT `4ef8c042…` and RS `a91882e7…`. Those two are the versions relied on: their bytes at commit `cec590c5c3`, checked with `git show`. They stay under R23-21 item 3, because nothing in DEL-09-07 relies on the A16 rows.

## LHQ-U2 — frozen (2026-10-03)

| File | sha256 |
|---|---|
| `TRAFFIC_OBSERVATION_PLAN.md` (DEL-09-07/TOP-v0.1) | `73fac0c06e500f4e516dbe423dcafb85b3799405d63e1107329999b1e968f78a` |
| `QUALIFICATION_DOSSIER.md` (DEL-09-07/DOS-v0.1) | `301e52909894ea1711fb0bc03a8754b1dcb3c4e03b4a95f0b48c722afa55e148` |
| `lhq.candidate-identification.schema.json` | `194f8419ab5e72d070ac5b0cef44338a53b5547230f9d1ea73a6214de57c50dd` |
| `lhq.candidate-identification.valid.examples.json` | `dcb9f4a047d279588ec9aab9df125a506443b205e11bb4935867807b4c8f474a` |
| `lhq.candidate-identification.invalid.examples.json` | `c501cab667524bdbb322a9e411349f78da28f45b09bd70e8e9c6119992348a79` |
| `lhq.traffic-observation.schema.json` | `edafac0a8e7f36dd562f6a88156ba329c802be52af94e705bf4ce12f67802615` |
| `lhq.traffic-observation.valid.examples.json` | `a2b62020185664fbe800b6f9c7d8108385c86234dc1c6d33cbb9941328ceefa8` |
| `lhq.traffic-observation.invalid.examples.json` | `9e1b6bad021a2fd3a79bf9498a7ee303ace2ac6ab1ba2deb1eeb7e303249ea70` |
| `lhq.dossier-manifest.schema.json` | `d39c1a7b50b2691133ae8bd834d9cf560a9e87f1a23488c6fc6d79eb9e2a57d3` |
| `lhq.dossier-manifest.valid.examples.json` | `64c5886e651ec98612586bde53da1ed6c58fc9716444a15f959beee4d6caa7b1` |
| `lhq.dossier-manifest.invalid.examples.json` | `d3b44cfe9abc1280c2890ae57aa15550db9797f03a78871c0589c115404f2827` |

**Claims.**
1. **The V4-EXM-23 observation method (TOP).** An all-interface pktap capture with per-packet process and effective-process metadata. Its facts are stated by `man tcpdump` on macOS 26.6.2 (tcpdump 4.99.1, Apple version 158); no capture was run.
   - **Privilege.** Administrator rights are needed: `/dev/bpf*` is `crw------- root wheel`, observed. The privilege is asked for when the capture runs and granted by the person's own authentication (R23-14).
   - **Supporting parts.** Name resolution, process lineage and a snapshot cross-check.
   - **Five attribution classes.**
   - **Nine named blind spots** (BS-1…BS-9), each with its limit.
   - **Four calibration checks** (OV-1…OV-4) on the candidate, and a run sequence.
   - **Handling.** The raw capture stays on the examination machine; no payloads are kept; other applications are kept only as counts.
   - **Comparison rules,** with the completeness rule.
   - **Native enforcement** joins three pieces of evidence, none sufficient alone.
2. **The dossier (DOS).**
   - Its manifest, made of DEL-09-01 EXP records, consumed and not redefined.
   - An applicability map onto EXP change kinds.
   - The independent examination (VER-007).
   - The handoff to DEL-11-03, with rules DH-1 and DH-2.
   - The source-journey handoff to DEL-09-11, with rules DJ-1…DJ-3: run authors and session identities named, never supplied as content; receipts carry their resolution at write.
   - Failure rows DF-1…DF-5.
3. **Three PROPOSED schemas** with examples. The valid examples are illustrative: the CIR example records today's real state, with everything *not supplied* and HC-1…HC-13 *answered*; the other two are invented.

**Checks.**
- All three schemas pass `check_schema` (Draft 2020-12).
- Every valid example validates under `jsonschema` 4.26 and under DEL-01-01's subset validator.
- Each of the 14 invalid examples is rejected with exactly one error, for the stated rule.
- Every pin in TOP matches its current file.
- DOS pins EXP-v0.1 at the bytes relied on. O-B's in-progress v0.2 was read; it keeps everything relied on (noted in DOS).
- No home path is written.

**Open.**
- D-F1 and D-F2 for O-B: host-loop configuration, now perhaps covered by `host_profile`, and a change kind for an operation binding.
- Calibration OV-2 at run time.
- Snap length.
- Boundary-refusal recording (R23-14).
- Host joins (SQ-30, SQ-19).

## Early path: EP-05 and EP-11 (drafted against FX-DP1)

Fixture: FX-DP1 frozen by O-A (`MANIFEST.sha256` `e3c8c5ea…3b6f`; every file verified with `shasum -a 256 -c`). Both units rely on the A16 rows (R23-18). They cite those rows by label and pin none of their in-progress bytes, and will adopt O-A's refrozen versions at E-1 (R23-21 item 3).

**EP-05 (DEL-09-05 FW-04, VER-004).**
- The case on a candidate, in nine steps (04-0…04-8).
- Comparison rules R-1…R-8, written independently of DEL-06-02's DV rules.
- Parts P04-A…P04-E, and failure rows FF-1…FF-6.
- Rehearsal on FX-DP1 with a constructed examiner observation: 19 expectations, 0 failed. This covers the positive record, five negatives, the lapse and the independence of other acts.
- The five EXP records it writes are valid against the EXP result schema present now (`format` EXP-v0.2, O-B's repair; the check reads the format from the schema).
- My derivation agrees with DV-v0.1's on FX-DP1. That is consistency, not soundness; the soundness check is RV's review of E-1.

**EP-11 (DEL-09-11 reader method).**
- Roles: assembler, reader and examiner.
- Separation evidence for a person reader and for an agent reader (R23-10).
- Input-set manifest, with `not_authority` items and withheld identities.
- Reading protocol RD-0…RD-6, account schema, and examiner checks RC-1…RC-10.
- Timing per R23-6 as revised (dates evidenced; no arithmetic).
- A host-journey section: against SWBPIPE's answers, AC-002 cannot pass, because receipts are session-only.
- Rehearsal RR-E. The timing part and RC-10 are declared not applicable before the run (R23-19). Results:
  - constructed good account: 9 of 9 checks hold;
  - three bad accounts each fail the named check;
  - one account is rejected by its schema.
- **Request:** dispatch a fresh reader with `prototype/fixtures/READER_BRIEF.FX-DP1.md`, the input-set manifest and copies of the six files, and record what you supplied. Its account is then checked with `rrm_compare.py`. That is the early path's "isolated reader" consumption check, which I cannot run myself (a Type 2 executor does not delegate).

**Cross-owner observation for O-B.** EXP v0.2 forbids `case.scenario` on rehearsal records. My checks follow this.

## RR-E: checker repair (RC-6, RC-9) and the standing check

The reader's account (`E/RR-E/account.json` `637e234c…4cee`) is kept unchanged as the evidence. Both failures were checker defects, as HELP_HUMAN found.

- **RC-6 (subject rule).** The checker's `about`-equals-path convention came from my constructed accounts and was stated nowhere. Now `about` names the subject by any identifier in the input set (package id, file path or request record id); when `about` names no package, the package files among the sources do. This is stated in brief v0.2 and in the schema's descriptions. **No required key is added, so the account still validates.**
- **RC-7** now accepts added detail in actor and recorder ("identity not verified"). It also fails a denial: `no_decision` on a decided package.
- **RC-9.** A `change` or `outcome` claim that cites no change or outcome record is **referred to the examiner**: an absence written under those kinds cannot be told apart mechanically from an unsupported claim. The examiner's recorded judgment decides (*absence* holds; *unsupported* fails). With no judgment the check is never held, and the EXP outcome is `inconclusive`. A `no_outcome` kind is added for absences.
- **Rerun on the RR-E account, on the exact nine files the reader was given.** O-A regenerated the offer and capture at E-1, so those bytes are preserved in `DEL-09-11 Design/prototype/fixtures/RR-E-input/`, verified against `RR-E/SUPPLIED.sha256`.
  - Without a judgment: 8 checks held, RC-9 referred for C-09.
  - With `fixtures/judgments.independent.RR-E.json` (C-09 *absence*: HELP_HUMAN's judgment in RESULT.md, which I confirmed against the three-entry log): **9 of 9 held**, and the EXP record is schema-valid.
- **Standing check of the comparison** (`prototype/run_standing_check.py`, RRM §5.1): **12 cases, 0 unexpected.**
  - SC-1: the independent RR-E account, with and without the judgment.
  - SC-2: four mutations of it — an altered alternative, a decision on the pending package, the decision filed under the wrong package, and the decision denied.
  - SC-3: my five constructed accounts.
  - It is to be rerun after any change to the checker, the brief or the schema. A fresh independent reader is needed if the independent account stops validating.

## EP — frozen (2026-10-03): EP-05 and EP-11 together

| File (from each deliverable's `Design/`) | sha256 |
|---|---|
| DEL-09-05 `DECISION_ATTRIBUTION_CASE.md` (DAC-v0.1) | `384e08044f1f71da8dd1c4d79f92b55f95bb6a419a7f42960c419a0a517753a3` |
| DEL-09-05 `prototype/fw04_check.py` | `4b54169825db70006c115b44fecb71bf18a3ab6d9695afe75158c74e1edd51f9` |
| DEL-09-05 `prototype/fixtures/examiner_observation.FX-DP1.json` | `afc9df9d087488680a3624bb01ba88df3583ab3cb9ad98eb013b73acb6301716` |
| DEL-09-11 `READER_METHOD.md` (RRM-v0.1) | `b884018863aeedf8b8f1522ba6f60d8534ca85e1f0216f62ecaf7af5fd2f650e` |
| DEL-09-11 `rrm.input-set-manifest.schema.json` | `5262a76a48c0ba4460a7a977fc172c30572232032fa4a7c0f7dbed3212723e4d` |
| DEL-09-11 `rrm.reconstruction-account.schema.json` | `26d0d2e08e06c8cf74cccd537474e096e17848bf0a3c06b10b0486e29341791e` |
| DEL-09-11 `prototype/rrm_compare.py` | `80410be423f393452f5fdf2f1b7b0316b60220c1fc8d25614beb6ea9fd435a75` |
| DEL-09-11 `prototype/run_standing_check.py` | `f480aaf7dc74ee81ba05754b64b4d71f5a31a4fb95eede80165f248e74d45ef0` |
| DEL-09-11 `prototype/fixtures/READER_BRIEF.FX-DP1.md` (v0.2) | `9b7d6a0ee4d875e20a664db2396904beedfcb8df83ad856fc6da229f85979951` |
| DEL-09-11 `prototype/fixtures/IS-FX-DP1.input-set.json` / `IS-FX-DP1-2.input-set.json` | `f1174586…a63a` / `26609d1c92212bab3cbc9eeaabe02d00e7bf46d704670c3a1e9b28f3c7637028` |
| DEL-09-11 `prototype/fixtures/account.independent.RR-E.json` and the two judgments files | `637e234c…4cee`, `f0464d05…b777`, `dcfe27c4…93ed9` |
| DEL-09-11 `prototype/fixtures/RR-E-input/` (9 files) | as `E/RR-E/SUPPLIED.sha256` |

**Claims.**
- **EP-05.**
  - FW-04 is DEL-09-05's VER-004 case on a candidate, in nine steps.
  - Comparison rules R-1…R-8 are written independently of DEL-06-02's DV rules.
  - It has parts P04-A…P04-E and failure rows FF-1…FF-6.
  - It adopts E-1: ACT-POLICY-v0.10, RS-v0.10, RS schema, CE-4 schema 0.7, AAC-v0.3 and its schemas, DV-v0.1, and FX-DP1 at `346191ff…`.
- **EP-11.**
  - The reader method: three roles, separation evidence, the input set, the protocol, the account, comparison checks RC-1…RC-10, the standing check, timing per R23-6 as revised, and the host-journey limits.
  - The RR-E evidence and its repaired comparison, as above.

**Checks.**
- `fw04_check.py` on the E-1 fixture: 19 of 19 held, and its five EXP records are valid against the current EXP result schema (format read from the schema).
- O-A's `run_e.py` (`11ccd319…`), rerun by me into scratch: 47/47. This covers record validity against the refrozen schemas; I reused it rather than re-deriving it.
- Standing check: 12/12.
- RR-E comparison: 9/9 with the judgment.
- Both DEL-09-11 schemas pass `check_schema`.
- Every pin in DAC and RRM matches a current file, except FX-DP1's first-freeze manifest `e3c8c5ea…`, which E-1 superseded on disk; the supplied files themselves are verified.

**Open.**
- The EXP pin follows O-B's refrozen v0.2 (to be adopted with the U2 repair).
- The V4-EXM-13 undertaking fixture (a later unit).
- Candidate-only inputs: the person, the examiner's observation form, the App candidate, and the host journey for DEL-09-11.

## Replies to RV-LHQ-U1's confirmation items

| Item | Reply | Where |
|---|---|---|
| LHQ-R15 MINOR | Accepted. LF-5 is *blocked* when the step was reached and the act requested, and *not run* only when the case was never attempted. LF-10 is *blocked* at 23-0, with the cause recorded (R23-20 item 2; R23-14 item 1) | §6.1 LF-5, LF-10 |
| LHQ-R16 NOTE | Accepted. §5.0 places V4-HI-22 under LHQ-22 (22-2, P22-A). §5.3 marks the use of L-2 (a) for a host loop as an inference: L-2 is the owner's choice for App conversations | §5.0; §5.3 "Workflows" |

`LOCAL_HOST_QUALIFICATION.md` is now `430539276f6232f1b052346e29b6587376b8b902ab91716d7dc19cdea8166a71`. The header also notes that EXEC is pinned, like ACT and RS, at its committed bytes (`cec590c5c3`); its working tree changed one line under R23-23, which nothing cited relies on.

## LHQ-U2 — repaired for RV-LHQ-U2 (review `RV-LHQ-U2.md`)

| Finding | Reply | Where |
|---|---|---|
| U2-R1 MAJOR | Accepted. The completeness rule needs all of OV-1…OV-5 (aligned with LHQ §5.4). P23-C needs no unresolved flagged annex entry, and P23-A none whose destination is outside the allowed set. The baseline window B-0 can resolve a flag but never adds a pass. BS-1 and BS-8 state their effect on outcomes | TOP §4, §5, §7 |
| U2-R2 MAJOR | Accepted. The record set holds the run's primary project records only, each with its input-set standing. The dossier's case results, the examiner's reconstruction and its review are withheld as `derived_view`, and the agent's summary is supplied only as `not_authority`. In the schema, `withheld` (RRM kinds) replaces `session_identities`, and every record-set item requires a standing. Two invalid examples are added | DOS §5, DJ-1; dossier schema |
| U2-R3 MINOR | Accepted. EXP-v0.2 is adopted and pinned (protocol `fc5b8230…`, result `f7871c96…`, change-impact `b8fcb458…`, review `b3294a40…`). D-F1 is closed by `host_profile`; D-F2 by `case_definition` | DOS header; Findings; UNRESOLVED |
| U2-R4 MINOR | Accepted. The map is derived from the elements each record carries. The model row reopens all four cases. A case-definition row is added, and an operation-binding change is reported as `case_definition`. The schema's change kinds equal EXP-v0.2's (checked) | DOS §2; dossier schema |
| U2-R5 MINOR | Accepted. Per-packet metadata is marked as an inference. The effective-process extraction method is stated (filtered `-Q "epid = …"` passes, with flow joins). New BS-10 (packets without metadata) and BS-11 (proxy or relay, checked by OV-5) | TOP §2.1, §4, §5 |
| U2-R6 MINOR | Accepted. Calibration is an object with one entry per check (OV-1…OV-5, B-0). Any check not held forces `complete: false` with `calibration_not_held`. A flagged annex entry requires its limit and resolution. RV's probes T1…T3 are now invalid examples; T1 is rejected with two errors from the same rule | Traffic schema and examples |
| U2-R7 MINOR | Accepted. A declined privilege is *blocked* at the start (TOP §2.1 = LHQ LF-10) | TOP §2.1 |
| U2-R8 NOTE | Accepted: "the operating system asks for" | TOP §2.1 |
| U2-R9 NOTE | No change | — |

**Files.**

| File | sha256 |
|---|---|
| `TRAFFIC_OBSERVATION_PLAN.md` | `9126e9a197474f674266c93aeaea4f0b16dc8b4ed43de216981002e08b5ce208` |
| `QUALIFICATION_DOSSIER.md` | `08430bb6e0029e755fdf13452d46b64aa46e98096ae1d38f4526506aa23c1659` |
| `lhq.traffic-observation.schema.json` | `0b3f9fddfe0b317a880ebc0caf9d7a28b61a19514c28216ef97d659027691e56` |
| `lhq.traffic-observation.valid.examples.json` | `bf60f943367277e8897c8baa0dd1cb674245bf593dabf96bcde91bc1109b96f8` |
| `lhq.traffic-observation.invalid.examples.json` | `f3a38b8b99155953c75b6cea04531f97d15b3d7fbe3bf65f1d1316f12fdb2bab` |
| `lhq.dossier-manifest.schema.json` | `0e8e8917e0ac52c7c5b2e16db3db2d0517eccf3261f476bf7b4193c85b740cff` |
| `lhq.dossier-manifest.valid.examples.json` | `4d659926675a5c7e4bad32a627a7aef738fd0c9fb5aa606abe9314271784f9bd` |
| `lhq.dossier-manifest.invalid.examples.json` | `8dce976dab589b46f10045aaa3f8672fe291a16658f0b43500dcc8a558721294` |
| CIR schema and examples | Unchanged |

**Checks.**
- All three schemas pass `check_schema`.
- Every valid example validates under `jsonschema` and under DEL-01-01's subset validator.
- All 19 invalid examples are rejected under both validators.
- All pins in the three Markdown files match current files, or the committed bytes named for ACT, RS and EXEC.
- The offer digest recomputes from the refrozen offer under the AAC-v0.3 §5.1 rule (`c346f3ca…`).

## EP — refrozen (EP-05 + EP-11; supersedes "EP — frozen" above)

The earlier freeze came before HELP_HUMAN's ordering note. Since then:
- **EP-05 and EP-11 adopt ACT-POLICY-v0.10 at its current bytes** `d8e7449c…f268`. It now carries the §2.5 A16 content binding (R23-23 item 2), on which FW-04's lapse rule R-8 relies.
- **EP-11 has a new input set `IS-FX-DP1-2`** for the refrozen FX-DP1 (R23-23 item 4). RR-E's account stays evidence for `IS-FX-DP1-1`.
- **Decision: the new input set carries the digest rule.** It is a new item standing, `definition` (with its repository `source` and hash), holding a verbatim excerpt of AAC-v0.3 §5.1 lines 240–255. The reason: the RR-E reader could not check the digest from the files alone. I recomputed the refrozen offer's digest from the rule alone, and it matches.
- **EP-11 cites the repaired DOS** for the handoff it receives.

| File | sha256 |
|---|---|
| DEL-09-05 `DECISION_ATTRIBUTION_CASE.md` | `52224eae0d2b7386cf8e1ecbbd751f3d536cca0a976165b61352bc7f3173fa3c` |
| DEL-09-05 `prototype/fw04_check.py` | `4b54169825db70006c115b44fecb71bf18a3ab6d9695afe75158c74e1edd51f9` |
| DEL-09-05 `prototype/fixtures/examiner_observation.FX-DP1.json` | `afc9df9d087488680a3624bb01ba88df3583ab3cb9ad98eb013b73acb6301716` |
| DEL-09-11 `READER_METHOD.md` | `5ca52e23d000250235da3c1f4430dab4a3dfc212e13dccbf6148e978f4c22faf` |
| DEL-09-11 `rrm.input-set-manifest.schema.json` (adds `definition` and `source`) | `a1f03a374b5b69d267b9dd6a0b4c2ccee3fe52ca306c2b2efe420b06b07ad15e` |
| DEL-09-11 `rrm.reconstruction-account.schema.json` | `26d0d2e08e06c8cf74cccd537474e096e17848bf0a3c06b10b0486e29341791e` |
| DEL-09-11 `prototype/rrm_compare.py` | `80410be423f393452f5fdf2f1b7b0316b60220c1fc8d25614beb6ea9fd435a75` |
| DEL-09-11 `prototype/run_standing_check.py` | `f480aaf7dc74ee81ba05754b64b4d71f5a31a4fb95eede80165f248e74d45ef0` |
| DEL-09-11 `prototype/fixtures/IS-FX-DP1-2.input-set.json` | `e615aeeeaa1d5db3eaddab50179acae93714d56f40b126e08525a5bcd474156f` |
| DEL-09-11 `prototype/fixtures/definitions/aac-offer-digest-0.1.md` | `832d67c73a8492d70e6545dd925c78b46a014c5e87ba7aefc51246fed27aaa1a` |
| DEL-09-11 `prototype/fixtures/READER_BRIEF.FX-DP1.md` (v0.2) | `9b7d6a0ee4d875e20a664db2396904beedfcb8df83ad856fc6da229f85979951` |
| DEL-09-11 other fixtures (IS-FX-DP1-1, five constructed accounts, the independent account, judgments, `RR-E-input/`) | Unchanged from "EP — frozen" |

**Checks at refreeze.**
- `fw04_check.py` on the E-1 fixture: 19/19.
- O-A's `run_e.py`: 47/47 (record validity, reused).
- Standing check: 12 cases, 0 unexpected.
- RR-E on its supplied bytes: 9/9 with the judgment.
- Both input sets validate against the extended input-set schema.
- Every pin in DAC and RRM matches a current file.

**Open, carried.**
- The V4-EXM-13 undertaking fixture (a later unit).
- The candidate-only inputs.
- No reader has yet run on `IS-FX-DP1-2`. Not required: RR-E stands for the method. A run would test the digest check.

## Minor repairs after RV's confirmations, and the rerun on the R23-24 fixture (2026-10-03)

**Replies.**

| Finding | Reply | Where |
|---|---|---|
| U2-R10 MINOR | Accepted. The host is launched after B-0 and before OV-1…OV-4, inside the capture window. Calibration contacts are recorded in a marked calibration interval, carry their check, and are excluded from the §7 comparison | TOP §5; traffic schema `calibration_check` |
| U2-R11 MINOR | Accepted. A flag resolved "by baseline" requires B-0 *held*. The new invalid example (RV's probe P1) is rejected under both validators | Traffic schema `allOf`; invalid examples |
| U2-R12 NOTE | Accepted. The duplicate enum value is removed | Dossier schema |
| LHQ header | Accepted. The EXEC change is attributed to R23-23 item 2 | LHQ header |
| EP-R1 MINOR | Accepted. Judgment format 0.2 binds a judgment to its account by id and file sha256, and names the examiner. An unbound file is ignored, with the reason recorded as a limit. The judgment's hash goes into the EXP evidence. The standing check gains two unbound-judgment cases | `rrm_compare.py` `bind_judgments`; RRM §5 RC-9; judgments files |
| EP-R2 MINOR | Accepted. R-3 compares the actor's names with the run's agent identities and the requester. Every constructed `human_act` is validated against RS (DEL-04-03 `minischema.py`, with the AS and CE-4 references). N-1 is RS-valid, with agreeing capture evidence, and is stopped only by R-3 | DAC §3 R-3, §6; `fw04_check.py` |
| EP-R3 MINOR | Accepted. Stale rows are removed from both files. DAC pins EXP-v0.2 | DAC header, §7, UNRESOLVED; RRM UNRESOLVED |
| EP-R4 NOTE | Adopted after R23-24. P04-A reads `reservedBy` from the package file and checks that the file's alternatives match its request | DAC §4, `fw04_check.py` |
| EP-R5 NOTE | Adopted after R23-25. R-6 follows O-A's decision: a later A16 supersedes for current standing, and a correction is not a decision. Exercised both ways | DAC §3 R-6, §6 |
| EP-R6 NOTE | Adopted. RC-5 refuses a decision, acceptance, change or outcome claim resting on a `definition` item. A standing-check case covers it | RRM §5; `rrm_compare.py` |
| EP-R7 NOTE | Kept as designed. On a host journey, expect the examiner's referral workload to grow | RRM changes table |
| DAC §6 command path | Accepted. The command now runs from the deliverable folder | DAC §6 |

**Rerun on FX-DP1 `9501ef81…` (R23-24).**
- **EP-05:** `fw04_check.py` gives **22 expectations, 0 failed**.
  - It now includes RS validation of the fixture records and of every constructed act, P04-A from `reservedBy`, and R-6 both ways.
  - O-A's `run_e.py` (`81c973de…`) gives 56/56, rerun by me.
- **EP-11:**
  - New input set **`IS-FX-DP1-3`** (`18b9e49b…`): all six fixture files plus a refreshed digest definition (AAC-v0.3 §5.1 lines 240–273, `ad6a148d…`). It is assembled for a reader in `prototype/fixtures/IS-FX-DP1-3-input/`, every item hash-checked.
  - The digest recomputes from the rule.
  - Subject rule: a namespaced `packageId` is also named by its last segment, when that segment is unique among the packages.
- **Results.**
  - Constructed good account on `IS-FX-DP1-3`: 9/9.
  - RR-E-shaped account re-pointed at `IS-FX-DP1-3`: no failures; C-09 referred, because the judgment is bound to RR-E's own account.
  - RR-E evidence on its supplied bytes, with its bound judgment: 9/9.
  - **Standing check: 17 cases, 0 unexpected.**
- No independent reader has run on `IS-FX-DP1-3`.

**Files now (sha256).**
- DEL-09-07: `LOCAL_HOST_QUALIFICATION.md` `4ee7de26…31bc`, `TRAFFIC_OBSERVATION_PLAN.md` `49f028bc…b125`, `QUALIFICATION_DOSSIER.md` `83101523…50d1`, `lhq.traffic-observation.schema.json` `f0886d5f…1f89`, its invalid examples `4d549b5f…a3a2`, `lhq.dossier-manifest.schema.json` `88cd9948…7e88`. The other example files and the CIR schema are unchanged.
- DEL-09-05: `DECISION_ATTRIBUTION_CASE.md` `bf0ddb6a…8d62`, `prototype/fw04_check.py` `e57359d3…29b9`.
- DEL-09-11: `READER_METHOD.md` `7446d056…c343`, `prototype/rrm_compare.py` `d445740e…a8d8`, `prototype/run_standing_check.py` `6ff45447…13d6`, `fixtures/judgments.independent.RR-E.json` `1b2952bf…ac24`, `fixtures/judgments.bad2.json` `c22e0ab1…eb99`, `fixtures/IS-FX-DP1-3.input-set.json` `18b9e49b…c17f`, `fixtures/account.good.IS-FX-DP1-3.json` `f977804d…b01`, `fixtures/account.rre-shape.IS-FX-DP1-3.json` `0aece549…d7a`. The schemas are unchanged.

**Checks.**
- Every pin in the five Design files matches a current file, or the committed bytes named for ACT, RS and EXEC in LHQ.
- All DEL-09-07 schemas: valid examples validate and invalid examples are rejected, under `jsonschema` and DEL-01-01's subset validator.
- The DEL-09-11 input sets and accounts validate.

## RR-F and RV's two hardenings (2026-10-03)

| Item | Reply | Where |
|---|---|---|
| RR-F as a second independent case | Done. `E/RR-F/account.json` (`8188caba…92c0`) is kept byte-identical as `fixtures/account.independent.RR-F.json`. RR-F's `SUPPLIED.sha256` verifies against `fixtures/IS-FX-DP1-3-input/`. On that input it holds 9/9 with nothing referred, and it is SC-1's second independent case | RRM §8; `run_standing_check.py` |
| Last-segment rule | Hardened. A namespaced id's last segment is admitted only when it is distinctive: unique, not contained in any identifier of another package, and containing none of them nor another package's segment. Identifiers now match only as whole identifiers (`-`, `_` and `:` continue an identifier), so `pkg:t:PKG-1` is not found inside `pkg:t:PKG-1-b`. A new SC-2 case covers overlapping tails (PKG-1 / PKG-1-b admit no short form; PKG-1 / PKG-2 do) | `rrm_compare.py` `package_identifiers`, `mentions`; RRM §4 |
| `calibration_check` binding | Bound. The traffic schema requires `calibration_setup` (declared test endpoints and the marked calibration interval) and keeps calibration contacts in the subject class. New rule CB-1 (TOP §7): a tagged contact is calibration only if its destination is a declared endpoint and its times lie within the interval. Otherwise it is mis-tagged and compared as a run contact. The new `Design/prototype/top_check.py` applies it: the valid example passes with 4 of 5 contacts compared, and two schema-valid violation examples (a run contact tagged as calibration; an endpoint contact outside the interval) are both reported. A schema-invalid example (no `calibration_setup`) is added | TOP §5, §7; traffic schema; `lhq.traffic-observation.cb1-violations.examples.json` |
| Supplier drift found by the pin check | RS changed after the checkpoint commit: §7 L-0 now states A16 supersession (R23-25), which R-6 relies on. DAC and RRM adopt the current RS, `2e7afb1b…30ff`, and FW-04 reruns 22/22 on it. EXP's protocol changed only to close U-EXP-1. DAC, RRM and DOS keep `fc5b8230…`, the bytes committed at `09ca67d094` (checked with `git show`) | DAC and RRM headers |

**Checks.**
- Standing check: **19 cases, 0 unexpected**. That includes RR-E (with its bound judgment), RR-F, the overlap case and the definition case.
- FW-04: 22/22 on FX-DP1 `9501ef81…`.
- DEL-09-07 schemas: all three pass `check_schema`. Valid examples validate and invalid examples are rejected, under both `jsonschema` and DEL-01-01's subset validator. The CB-1 violation examples are schema-valid, and `top_check.py` reports both.
- Every pin in the five Design files matches a current file, or committed bytes named in the file.

**Files now (sha256).**
- DEL-09-07: `TRAFFIC_OBSERVATION_PLAN.md` `a4cd945f…0189`; `lhq.traffic-observation.schema.json` `25afd32d…ba01`; its valid examples `d17ed0b0…c43a`, invalid examples `829bc8d6…2815`, CB-1 violations `419d329d…651c`; `prototype/top_check.py` `c767c3fa…b650`. LHQ, DOS, the CIR and the dossier schemas are unchanged.
- DEL-09-05: `DECISION_ATTRIBUTION_CASE.md` `77991d61…1521` (RS re-pin only); `fw04_check.py` unchanged.
- DEL-09-11: `READER_METHOD.md` `3a4a1462…7673`; `prototype/rrm_compare.py` `48630745…57be8`; `prototype/run_standing_check.py` `8eb1bd19…3b46`; `fixtures/account.independent.RR-F.json` `8188caba…92c0`.

**FV-4a (coordinator).** No current DEL-09-05 code reads DEL-06-02's waiting rows: FW-04 reads only decision records. So DAC §6.1 now states rule **RW-1** for the V4-EXM-13 joined witness. Wherever DEL-09-05 reads a waiting row, it treats both *ready* and *ready (qualified)* (and `readinessQualified`) as ready. It keeps the qualifier and its first cause in its observations and result records, never reports a qualified row as bare *ready*, and names the expected label in any expected rebuilt state. The rule cites DEL-06-02 `FLEET_VIEWS.md` (FV-v0.1, `15e25a24…1b85`). `DECISION_ATTRIBUTION_CASE.md` is now `1fc4fd272c4f155c04f6367fb2e2562071536c78dea579dd1cfedbb889d5756c`.

**Time form (RV note).**
- TOP §6 states one ISO-8601 UTC form, `YYYY-MM-DDThh:mm:ss[.fraction]Z`. The traffic schema enforces it with a pattern on every time field: window, calibration interval, contacts, annex entries and privilege grant. A new invalid example is rejected under both validators.
- `top_check.py` now parses times as instants rather than comparing strings, and refuses a time without an offset.
- Rerun: the valid example is OK (4 of 5 contacts compared). Both CB-1 violation examples are reported mis-tagged; both remain schema-valid.

| File | sha256 |
|---|---|
| `prototype/top_check.py` | `cf128073437772b3f14f2d7f5c42b2043087f19a1f4a9b82ba487a839b135139` |
| `lhq.traffic-observation.schema.json` | `b7401e1f1e0e1b010bba2c2ac3c3c32a0f281db0e10a40ea19ef8a9bea4eab95` |
| invalid examples | `0a651f0f5e97a8d1f5fbb629b15b108dbc72054d211b435e27f9812e681e0fe0` |
| `TRAFFIC_OBSERVATION_PLAN.md` | `5d147be4c0b441b34017933c84a195b905c24f01d2764e4fc669e36aef6d0324` |

## Tranche 2: RQ-LHQ-1 under R23-36 (2026-10-04), for RV3

**Change.**
- LHQ is now **LHQ-v0.2**. It supersedes LHQ-v0.1 at `20361a0be76904d4b8ac745f055755cd27455d13d7625a559de1b44ff386e8f8`, the version committed at `d150856784`.
- §3 gains rule **CI-5** and a pointer from the App candidate row. The CIR may carry an optional `app_candidate_subject` with `revision`, `build_identity`, `packaged`, and `package_record` when packaged. This is exactly EXP-v0.2's `candidate_subject.app_candidate` (`exam.result-record.schema.json` `f7871c96…1f9`); the CIR maps to EXP's identity and does not define it (R23-33).
- It is present only while the App candidate element is supplied; the schema refuses it when the element is *not supplied*.
- Nothing else changed. The record format label stays `LHQ-v0.1`: the change is additive (R23-21, AAC/RS precedent).

**Additivity.**
- The original valid example is unchanged and still validates.
- All three earlier invalid examples are still rejected, each with one error.
- New examples: one valid example with the mapping (packaged, with its package record), and two invalid examples — a mapping while the candidate is *not supplied*, and packaged without a package record. Each invalid example is rejected with one error under both `jsonschema` and DEL-01-01's subset validator.

**Checks.**
- All three DEL-09-07 schemas pass `check_schema`, and every valid and invalid example behaves as expected under both validators.
- The schema's `$defs/app_candidate_subject` equals EXP-v0.2's definition (compared by script).
- The new example's mapping validates as an EXP `candidate_subject` against EXP's own schema.
- `top_check.py` rerun, unchanged at `cf128073…5139`: the valid example passes (4 of 5 contacts compared), and both CB-1 violation examples are reported mis-tagged.

**Dependents.** TOP and DOS pin LHQ-v0.1 at `20361a0b…`, the committed bytes. Neither relies on CI-5, so under R23-21 item 3 their pins stay and are not edited. They are listed for the closeout's stale-pin script (R23-21 item 4).

| File (DEL-09-07 `Design/`) | Before | After |
|---|---|---|
| `LOCAL_HOST_QUALIFICATION.md` | `20361a0be76904d4b8ac745f055755cd27455d13d7625a559de1b44ff386e8f8` | `5cd31e097a8faae46298202d854b9bb9cba27e8355c31fef997310b49c15f07b` |
| `lhq.candidate-identification.schema.json` | `194f8419ab5e72d070ac5b0cef44338a53b5547230f9d1ea73a6214de57c50dd` | `3fb8f586b0bc1ca32c2ba4e82008e384109d3adc1189a0bf5091d598c46b5fc5` |
| `lhq.candidate-identification.valid.examples.json` | `dcb9f4a047d279588ec9aab9df125a506443b205e11bb4935867807b4c8f474a` | `c7684ee595bcb1e91a6a3b86bb4a37022a0c4c57dfcacc3ffad8326b41b2d9d4` |
| `lhq.candidate-identification.invalid.examples.json` | `c501cab667524bdbb322a9e411349f78da28f45b09bd70e8e9c6119992348a79` | `b823d54b4627f25e543b88d7d5c06d0560124274005c0072ac3cbc694749ceed` |
| `prototype/top_check.py` | `cf128073437772b3f14f2d7f5c42b2043087f19a1f4a9b82ba487a839b135139` | unchanged |

## Tranche 2: EUF1-S1 (DOS example consistency) and LHQ2-R1 (RV3; R23-42 item 3)

### EUF1-S1

**Finding.** DOS's example dossier named receipt RC-1 in its DEL-09-11 hand-over, while its host-evidence index and its DEL-11-03 hand-over were empty.

**Rule.** DOS §1 already required the index to list every receipt the results cite, with its resolution at write. The prose rule allowed the inconsistency only because nothing checked it.

**Example fix.** `DOS-EXAMPLE-INVENTED` ran no case, so it now names no receipt anywhere. A second example, `DOS-EXAMPLE-INVENTED-POPULATED`, shows the consistent form:
- RC-1 is listed *unresolvable* in the index and in both hand-overs;
- LHQ-20's result is `inconclusive`;
- a limitation states why RC-1 cannot be resolved.

**Check added.** DOS §1 now states DX-1 and DX-2:
- **DX-1:** every hand-over receipt is in the index, with the same resolution.
- **DX-2:** both hand-overs carry the same receipt set.

`prototype/dos_check.py` (new) enforces both. `lhq.dossier-manifest.dx-violations.examples.json` (new) holds three schema-valid violations:
- the old example;
- a resolution that differs from the index;
- a receipt missing from the DEL-11-03 hand-over.

The schema-invalid examples, which were derived from the old example, no longer carry the inconsistency, so each fails only for its stated rule. The DOS changes table has an EUF1-S1 row. The dossier schema is unchanged.

### LHQ2-R1

**Rule.** CI-5 now states three things:
- `app_candidate_subject` and the element's `value` describe the same build where both are given;
- a disagreement is a CIR defect for the examiner;
- consumers reconcile on the mapping.

**Check added.** A schema cannot express this rule. `prototype/cir_check.py` (new) checks the mechanical part: the mapping's `revision` and `build_identity` must each occur in `value`. It ignores the example marker " (invented)". Passing it is necessary, not sufficient.

**Invalid example.** `lhq.candidate-identification.ci5-violations.examples.json` (new) holds two schema-valid records that `cir_check` rejects:
- RV3's tested case, a different `revision`;
- a different `build_identity`.

They sit in their own file, not in the schema-invalid file, because the schema accepts them.

**Scope.** The change is a repair in place under LHQ-v0.2, with a changes row. The CIR schema and its valid and invalid example files are unchanged. LHQ2-R2, DOS's pinned CIR schema, is held for the closeout as directed and was not touched.

### Checks rerun

All three DEL-09-07 schemas were checked with `jsonschema` 4.26 (Draft 2020-12) and with DEL-01-01's subset validator.

| Schema | Valid examples (errors) | Invalid examples (rejected) | Violation examples (schema-valid) |
|---|---|---|---|
| dossier | 2 (0) | 7 (all) | 3 DX (all) |
| CIR | 2 (0) | 5 (all) | 2 CI-5 (all) |
| traffic | 1 (0) | 12 (all) | 2 CB-1 (all) |

The prototype checks give the expected exit codes:

| Check | Exit 0 (passes) | Exit 1 (reports a violation) |
|---|---|---|
| `dos_check` | valid examples | DX violations |
| `cir_check` | valid examples; the schema-invalid file does not trip it | CI-5 violations |
| `top_check` | valid examples | CB-1 violations |

CIR `$defs/app_candidate_subject` still equals EXP-v0.2's definition (compared by script). EXP is still at `f7871c96…2081`. Each prototype hash embedded in the DOS and LHQ texts was grepped and matches the file.

### Hashes

| File (DEL-09-07 `Design/`) | Before | After |
|---|---|---|
| `QUALIFICATION_DOSSIER.md` | `b2ffba7135652c9e5d2ebaece3d1b002a4aef6f394f9f876dc2b3600cdde0ccd` | `687032c0036cc83ef4d82170112f209ad5d6e99a161267a8b82e3cb8ef1e8465` |
| `lhq.dossier-manifest.valid.examples.json` | `4d659926675a5c7e4bad32a627a7aef738fd0c9fb5aa606abe9314271784f9bd` | `9873df65c9b481728d0043b0db8ea109ada5f4fdec0d8e2dc9cf2ef292068a6f` |
| `lhq.dossier-manifest.invalid.examples.json` | `8dce976dab589b46f10045aaa3f8672fe291a16658f0b43500dcc8a558721294` | `d0d28015b59f2f0d3dfdfec910a43017c7724408fe5c90630b7880e392543bd9` |
| `lhq.dossier-manifest.dx-violations.examples.json` | new | `de54af74203bc763230be2f00b9c33ced8159c7873f5cae9749417dfdd1652a3` |
| `prototype/dos_check.py` | new | `07bc7791d517ade2f56c3d8c97548025e15fcdb47e8dd6cd323027549e6f2903` |
| `lhq.dossier-manifest.schema.json` | `88cd994821c25422507ca45a901e4cd8ed5c31d847ecdbbd8475ad1ebd7d7e88` | unchanged |
| `LOCAL_HOST_QUALIFICATION.md` | `5cd31e097a8faae46298202d854b9bb9cba27e8355c31fef997310b49c15f07b` | `90f461cbbe98de20cdd19e13be6adb82818fa23ea55166cab04833108df8523e` |
| `lhq.candidate-identification.ci5-violations.examples.json` | new | `e8102cb7b8386bb3eab7e2f73702057bc2043fac99c00887e567299c70200aa4` |
| `prototype/cir_check.py` | new | `6f32a9511acc505b074cc6983589c790900832f36dfc5fa8669850bbffbd2bad` |
| `lhq.candidate-identification.schema.json` | `3fb8f586b0bc1ca32c2ba4e82008e384109d3adc1189a0bf5091d598c46b5fc5` | unchanged |
| `lhq.candidate-identification.valid.examples.json` | `c7684ee595bcb1e91a6a3b86bb4a37022a0c4c57dfcacc3ffad8326b41b2d9d4` | unchanged |
| `lhq.candidate-identification.invalid.examples.json` | `b823d54b4627f25e543b88d7d5c06d0560124274005c0072ac3cbc694749ceed` | unchanged |
| `lhq.traffic-observation.schema.json` | `b7401e1f1e0e1b010bba2c2ac3c3c32a0f281db0e10a40ea19ef8a9bea4eab95` | unchanged |
| `prototype/top_check.py` | `cf128073437772b3f14f2d7f5c42b2043087f19a1f4a9b82ba487a839b135139` | unchanged |

**Pin note.** RV3 confirmed LHQ-v0.2 READY at `5cd31e09…`. The LHQ2-R1 repair moves the file to `90f461cb…`, so RV3's confirmation of LHQ2-R1 should be made against the new hash.

**Not done.** No other file was written. No git writes and no network.

## Tranche 2: RR-EUF3 item (R23-49): a not-run case names no run

**Finding.** RR-EUF3 found that `DOS-EXAMPLE-INVENTED` records LHQ-20 as not run (`EXP-LHQ-20-not-run-example`), yet its DEL-09-11 hand-over named a journey run (`LHQ-20-EXAMPLE-RUN`), a record set with placeholder hashes, and run authors. DX-1 and DX-2 did not cover this, because they only compare receipts.

**Example repair.**
- `DOS-EXAMPLE-INVENTED` no longer has a DEL-09-11 hand-over. The hand-over is optional in the schema, and its required fields would name a run. A limitation now states why. Its DEL-11-03 hand-over already named no run: no acts, no receipts, not the witness.
- `DOS-EXAMPLE-INVENTED-POPULATED` has LHQ-20 run (inconclusive). Two of its labels still said otherwise and are fixed:
  - its limitation said "no case has run" and now says only LHQ-20 has run;
  - its withheld item named the other dossier's case results and now names its own.
- The schema-invalid examples carry a DEL-09-11 hand-over, and two count as the witness. They now cite the run (inconclusive) LHQ-20 result, with the same label fixes. Each still fails `jsonschema` with exactly one error, for its stated rule.
- The two derived DX violation examples get the same label fixes.

**Check added.** DX-3 is a new rule in `prototype/dos_check.py`, stated in DOS §1, with a changes row. When every EXP result cited for LHQ-20 is `not-run`:
- there is no DEL-09-11 hand-over;
- the DEL-11-03 hand-over has no acceptance act and no receipt, and does not count as the completed witness.

The script reads outcomes from EXP result records passed with `--outcomes`. When an outcome is not supplied, it says "DX-3 not checked"; it never passes the rule silently.

**New and updated example files.**
- `lhq.dossier-manifest.exp-outcomes.examples.json` (new) holds invented outcome stubs for the example refs. Each carries only `record_id` and `outcome`; the stubs are not EXP records.
- `dx-violations` gains two violations:
  - `DX-VIOL-not-run-names-run`: the example as it stood before this repair;
  - `DX-VIOL-not-run-11-03-names-acts`: a not-run LHQ-20 whose DEL-11-03 hand-over names an act and a receipt. That receipt is indexed, so DX-3 is the only rule it breaks.
- The first violation example (EUF1-S1) is now noted as breaking DX-3 as well.
- The dossier schema is unchanged.

### Checks rerun

Schemas were checked with `jsonschema` 4.26 and DEL-01-01's subset validator.

| Schema | Valid examples (errors) | Invalid examples (rejected) | Violation examples (schema-valid) |
|---|---|---|---|
| dossier | 2 (0) | 7 (all) | 5 DX (all) |
| CIR | 2 (0) | 5 (all) | 2 CI-5 (all) |
| traffic | 1 (0) | 12 (all) | 2 CB-1 (all) |

Prototype checks, run with the outcome stubs where they apply:

| Check | Exit 0 (passes) | Exit 1 (reports a violation) |
|---|---|---|
| `dos_check --outcomes` | valid examples; schema-invalid examples (no DX finding) | all 5 DX violations |
| `cir_check` | valid examples | CI-5 violations |
| `top_check` | valid examples | CB-1 violations |

The `dos_check` and outcome-file hashes quoted in DOS were checked by grep.

### Hashes

| File (DEL-09-07 `Design/`) | Before (after EUF1-S1) | After |
|---|---|---|
| `QUALIFICATION_DOSSIER.md` | `687032c0036cc83ef4d82170112f209ad5d6e99a161267a8b82e3cb8ef1e8465` | `8c4f4fa1593a22bdce93ff59c647785b0e81c72627a5aa4b07d253c4f13f6d7d` |
| `lhq.dossier-manifest.valid.examples.json` | `9873df65c9b481728d0043b0db8ea109ada5f4fdec0d8e2dc9cf2ef292068a6f` | `dbf8463f45dc2b9cad657fbe81a614d761f7cc8002a21e6e65bf58139730b666` |
| `lhq.dossier-manifest.invalid.examples.json` | `d0d28015b59f2f0d3dfdfec910a43017c7724408fe5c90630b7880e392543bd9` | `571e7ddb9db6a303efe4646e1d3462d5bd127f3370f9e13b6612bcc23f809d73` |
| `lhq.dossier-manifest.dx-violations.examples.json` | `de54af74203bc763230be2f00b9c33ced8159c7873f5cae9749417dfdd1652a3` | `8a183339a8880359f2f7f3ccb1dac4a03ecab51865fafe02fedba2b11e16e0f9` |
| `lhq.dossier-manifest.exp-outcomes.examples.json` | new | `15d9ae2d1a1698a13a75d18c7fbc1c614d84f4b9969c1bf99a5cf26abd2880b8` |
| `prototype/dos_check.py` | `07bc7791d517ade2f56c3d8c97548025e15fcdb47e8dd6cd323027549e6f2903` | `bf20d8fca2623c6fb1d4036ba4b59074dd32ed8dbb8345e298ce6a98ecfe84b1` |
| `lhq.dossier-manifest.schema.json` | `88cd994821c25422507ca45a901e4cd8ed5c31d847ecdbbd8475ad1ebd7d7e88` | unchanged |

These files are unchanged since LHQ2-R1:

| File | sha256 |
|---|---|
| `LOCAL_HOST_QUALIFICATION.md` | `90f461cb…523e` |
| `prototype/cir_check.py` | `6f32a951…2bad` |
| CIR schema | `3fb8f586…` |
| CIR valid examples | `c7684ee5…` |
| CIR invalid examples | `b823d54b…` |
| `…ci5-violations` | `e8102cb7…` |
| traffic schema | `b7401e1f…` |
| `top_check.py` | `cf128073…` |

**For O-F, not edited (their files are data to me).** O-F's packet holds copies of the old `DOS-EXAMPLE-INVENTED`, which still has the DEL-09-11 hand-over and RC-1:
- `F/fixtures/FX-RP1/supplied/`, `FX-RP1-2/supplied/` and `FX-RP1-3/supplied/`, each with `lhq-dossier-manifest.DOS-EXAMPLE-INVENTED.json`;
- `F/vendor/lhq.dossier-manifest.valid.examples.json`.

Any fixture that relies on that example's hand-over to DEL-09-11 should take `DOS-EXAMPLE-INVENTED-POPULATED` instead.

**Frozen.** All DEL-09-07 files listed above are frozen at these hashes for the coordinator to commit and for RV3 to confirm. No git writes and no network.
