# O-C — owner notes and returns (DEL-09-05, DEL-09-07, DEL-09-11)

Owner: O-C (Type 2 TASK, Claude Opus 5.5, high effort; the S1-C survey agent). Method: `coordinated-knowledge-work` (workflow sha256 `44049bcd38b88378cd757ea34516f01edb0b0e93d8e9e3ac2b47ac61c9271b18`) under this run's work graph "Coordination". Pin basis for every unit: written for either Codex pin (R23-3).

## Units

| Unit | Deliverable | Path (from `projects/chirality-app-v4/execution/`) | sha256 | State |
|---|---|---|---|---|
| LHQ-U1 | DEL-09-07 | `PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/Design/LOCAL_HOST_QUALIFICATION.md` | frozen `2668d955…0ecc`; **repaired** `21c9982f68ddc1aebafa8f24abaa4bb7856d76f6e827b5c23488493f75a7c1bb` | Repaired in place for RV-LHQ-U1 (13 findings); **awaiting RV's confirmation** |
| LHQ-U2 | DEL-09-07 | `Design/TRAFFIC_OBSERVATION_PLAN.md`, `Design/QUALIFICATION_DOSSIER.md`, `Design/lhq.{candidate-identification,traffic-observation,dossier-manifest}.schema.json` with valid/invalid examples | — | **Drafted**, schemas validated; not frozen while LHQ-U1's repair awaits confirmation (ready limit one) |
| EP-05 | DEL-09-05 | VER-004 case on O-A's early-path fixture (R23-8) | — | Queued; fixture path and hash awaited in `OWNERS/O-A.md` |
| EP-11 | DEL-09-11 | Reader method (R23-10, R23-6 as revised) on O-A's fixture | — | Queued; as EP-05 |

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
