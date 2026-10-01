# RP-4 — repairs from V18 in LOOP, PANEL, AS, ACT, CA, XT (return)

- Run `APP-V4-DESIGN-PASS-2-20260930`, repair node **RP-4**. Type 2 TASK
  (Claude Code subagent, Claude Opus 5.5; no delegation). Date 2026-09-30.
  Resumed once after a connection error; no file had been edited before it.
- Binding: R14 (R14-1, R14-3, R14-7), R13-1, R13-2, R13-5, R13-6, R12,
  DECISION-K1. Inputs read: BRIEFS.md ("Common rules", Wave B rules, RP row
  RP-4), R14, R13, R12, `comparisons/V18-1…V18-4.md`, `WAVE_B/OBS-1.md`, and
  DEL-01-01 `OBS_1_0.158.0.md` §1 and §10 (Part C; sha256 `85707703e97b…`).
  SWBPIPE's two files were not opened or edited; `RELAY_QUESTIONS_SWBPIPE.md`
  not edited.
- No version bump: each file gains rows in its Wave B change table
  ("Changes from v0.7" for LOOP, PANEL, ACT, AS; "Changes from v0.5" for CA,
  XT). Writes: the files listed in §5 and this file. No git write, no network,
  no package install. Scratch: the session scratchpad (`rp4/`).

## 1. Finding → fix → location

| Item | Fix | Where |
|---|---|---|
| **R14-7 / R13-5** (V18-1 m-14; V18-3 m-21) | LOOP §5.3 states R13-5: the carried call waits for the person's answer; that wait is the grant being sought, not a checkpoint hold, so DECISION-4 does not bear on it; other work continues; the person may end the turn and the request closes *unanswered at end* (run end likewise). NW-12 and G-8 cite it | LOOP §5.1.1 NW-12; §5.3 (new paragraph after DF-5); G-8 |
| **R14-7 / R13-6** (V18-3 m-20) | LOOP §4.1 OBS-1 column filled from Part C (C1–C3; LM Studio 0.4.16+2, `qwen/qwen3.5-9b`, 2026-09-30) beside FB-CC-1's reference: two fragments per call (id/type/name with `""`, then whole arguments), final empty delta with `tool_calls` then `[DONE]`, two calls sequential at index 0/1, `{}` for no arguments. Observation, not qualification: every rule stays PROPOSED; nothing differed from FB-CC-1. §4.2 records `reasoning_content` as outside FB-CC-1. "Until OBS-1" wording replaced (§0, §4, §7, MC-8, G-3, G-11, UNRESOLVED; the OBS-1 row closed). Prototype fixtures OBS1-C1…C3 reproduce the observed shapes | LOOP §0; §4; §4.1; §4.2; §7; §7.3; §11; Findings; UNRESOLVED; VC-05; `prototype/` |
| **R14-7 / R13-6** in CA, XT | "OBS-1 pending" in rehearsal records/W14-08 replaced (OBS-1's supplier turns were not App runs). EXEC's own "OBS-1 pending" cells (CH-32 arrival) left as EXEC states them | CA §8.5; CA/XT prototypes and examples |
| **R14-7 / R13-1** (V18-4 M-4) | CA CAF-10 states R13-1 (basis incomplete vs host-declared absence with "basis lineage not supplied"; cross-lineage *unknown (incomparable)*) | CA §2.3.1; F-29; UNRESOLVED |
| **R14-7 / R13-2** (V18-4 M-3) | CA CAF-32, CAF-34 and XT XC-06 state R13-2 (both labels RS R11, written on the resubmission's entry / on relaunch); CA F-29, XT F-27 and both UNRESOLVED rows closed; XT §3.6 drops "await R13" | CA §2.3.1; XT §3.2, §3.6, §9.11 |
| **R14-1** (V18-1 B-1) | LOOP E-8: every checkpoint event the loop emits with its EXEC-v0.6 §2.4.2 counterpart (CE-1…CE-19); the RS kind is "the one RS-v0.8 §13.3 states for that CE kind"; E-4 points to it; destination events → R15, operation events → R7 | LOOP §2.3 |
| V18-1 M-5 (R14-3) | LOOP §7 names the loop-side refusal values RS R7 is to carry | LOOP §7 |
| V18-1 m-1, V18-2 m-7 | "prior act not counted" + reason in live text | LOOP §2.3, §2.4.1, C-2, §11; PANEL W-5c, PC-19b, PC-21g, PC-21i |
| V18-1 m-5 | A15 named, not checkpoint-requirable | LOOP §0, §9; PANEL §0, §5 |
| V18-1 m-10 | No *pending* before *not granted*; already-allowed raises/records no request | LOOP §3.2, DF-5 Q-3; AS DG-15 (from "—") and prototype walk; PANEL ND-2 PS moves |
| V18-1 m-11 | F-2 recorded as `boundary_refusal` (model request); RS reason value missing — returned | LOOP §3.1 |
| V18-1 m-12 | E-6 ordinal not in the record; F-10 cites RS §14.1 W-1/W-2 | LOOP §2.3, §3.1 |
| V18-1 m-15 | §6.2 Grant in force = AS §12.1, with "unconfirmed"/"not received" and destination settings version | LOOP §6.2 |
| V18-1 m-16 | AS schema: always-off item `on` requires `settingActRef` (anyOf); INV-AS-4; §6 untouched (still = RS §8) | AS schema, invalid examples, VC-22 |
| V18-1 n-4 | ND-4 names class, stateless limit, "destinations not observed" | PANEL §3.8 |
| V18-2 m-6 | WD-v0.8 taken up: OP-1…OP-6 for kind (b) with the host-loop "completed assistant message" (PROPOSED: content of a *stop*/*tool calls* response, with or without calls); `on subject absent`, `fresh act required`; local names, production; FB-20…22; message content identity | LOOP §2.4, LP-9, §2.4.1, §2.4.2, §3.2 |
| V18-2 m-8 | PANEL §3.2: local names; *declared part not established*; new checkpoint elements; FB-20…22 | PANEL §3.2 |
| V18-2 m-11 | ACT §4.1 examples include A15 | ACT §4.1 |
| V18-3 m-10 | Operation reference = C operation identity of the offered edition; same element as `operationReference` | LOOP §2.2, §7.2 |
| V18-3 m-11 | P-v0.8: identity conflict, not known to host, PM-1/PM-2 on the dispatch record, R-d via PM-4/SQ-P6, MC-8 cites P-v0.8 | LOOP TL-2, §6.2, §6.3, MC-8, UNRESOLVED |
| V18-3 m-12; n-6 | PANEL §3.3: identity conflict, not known to host, DS-1 *mixed*, PM-1…PM-7 meanings | PANEL §3.3 |
| V18-3 m-16 | Edition held per C §2.2 with CI-4; pre-screen compares with the edition held current | LOOP §2.2, §2.3 |
| V18-4 M-1 | CAF-24 names RS R11 "act offered without a capture-evidence reference" | CA §2.3.1 |
| V18-4 m-2, m-3, m-4 | W14/XT records carry RS R11 labels in RS spelling (mapped once; checked against RS's schema list by both prototypes); "identity not verified (CAP-8)" removed from record limits (optional `record_limits` on act citations); act kinds = RS §6.1 set; EXEC reason mapping stated | CA §8.4; XT §3.4; both schemas, prototypes, examples |
| V18-4 m-9 | W14-05 needs DEL-01-04 for a joined CH-31 (ii) too | CA §8.2, §8.5 |
| V18-4 m-11 | XT IN-31 (EXEC per-surface report, DEP-09-09-023); observation kind `compatibility_report` | XT §2; schema |
| V18-4 m-12 | CA §11.1 EXEC row no longer says RT-11 and §8.2 differ | CA §11.1 |
| V18-4 m-13 | CAF-31 → SQ-P6 step 4; CAF-33 adds "de-duplication scope exceeded"; CAF-35 → SQ-P2/PT-15/PT-16 | CA §2.3.1 |
| V18-4 m-14 | CAF-16 drops XC-05 (no such variant); cites SH-1's PM-3 | CA §2.3.1 |
| V18-4 n-5, n-6 | XT §0 A1–A15; XC-07 per-item last observed state | XT §0, §3.2 |
| Not taken | V18-2 m-9 (PANEL `derived_from` as string): WD owns the tuple schema (RP-3); V18-4 m-10 (SH-1 limits): C's text; NOTEs V18-1 n-4 taken, V18-4 n-3, n-7 not taken | — |

## 2. Prototype runs (2026-09-30, Python 3.13.7, macOS, standard library)

- LOOP `python3 -B assemble_tool_calls.py`: **22/22** (19 earlier + OBS1-C1…C3), all records valid; `schema_subset.py` LOOP_TOOL_CALL examples VALID / INVALID. `destination_flow.py`: MS-06…MS-27 PASS, 68 RS entries and 11 request records valid, "RESULT: all expectations held". LOOP_DESTINATION_REQUEST examples VALID / INVALID.
- PANEL `panel_double.py`: 4/4; PANEL_RETURN_INPUT examples VALID / INVALID.
- AS `validate_settings_in.py`: VAL-AS-1, -2 valid; INV-AS-1…-4 invalid (INV-AS-4: "matches no anyOf branch"); 11 walks, 9 forbidden transitions PASS; "all expectations held". RS `run_prototype.py` (which `$ref`s AS's schema; RP-1's working state) rerun into scratch: "all expectations held", including R14-1's EXEC→RS conversion (12/12 and 40/40 valid).
- ACT `validate_policy.py`: "all expectations held".
- CA `run_w14_rehearsals.py --out <scratch>`: first failed with `'Recorder' object has no attribute 'doc'` — RP-1's R14-1 change to EXEC's recorder. Adapted to the outputs form ({kind, observedAt, body}); same 12 records and outcomes as §8.5; "every evidence limit is an RS R11 label (lost acknowledgement, unverified caller identity)"; examples regenerated with `--write-examples`, then check mode: "ALL CHECKS HOLD: 0 failure(s)".
- XT `run_xt_suite.py --out <scratch>`: same 24 records and outcomes; RS-label check held (3 labels); result-record examples regenerated; check mode "ALL CHECKS HOLD: 0 failure(s)"; work-account examples unchanged.

## 3. What other files must now say (returned; not edited here)

- **RS (RP-1):** §13.3 text must state the CE-n → RS kind mapping LOOP E-8 cites (the schema already has the kinds); R11 text for the labels CA/XT now cite ("act offered without a capture-evidence reference", "de-duplication scope exceeded", R13-1/R13-2 labels — in the schema, not yet in the text when read); a `boundary_refusal.reason` for "no model chosen"/"no credential" (LOOP F-2); R15 "each destination requested" read as each request raised (already-allowed raises none); that RS does not record LOOP's E-6 ordinal; R7 loop-side refusal values (LOOP §7).
- **P (RP-2):** §13 "Provide to DEL-05-02" should list identity conflict, not known to host and DS-1.
- **WD (RP-3):** PANEL/RS still type `derived_from` as a string (V18-2 m-9).
- **Integrator:** the W14/XT valid examples embed sha256 of C, ADAPTER and EXEC prototype files that RP-1/RP-2 are still changing; rerun both prototypes with `--write-examples` after all four nodes return.

## 4. ScopeOfWork or register items

None proposed.

## 5. Files and sha256 (12-char prefix)

Paths under `projects/chirality-app-v4/execution/`.

| File | sha256 |
|---|---|
| DEL-05-01 `LOOP_RECEIVING_CONTRACT.md` | 5528f0233cdd |
| DEL-05-01 `prototype/fixtures/stream_fixtures.json` | 6d21e1359583 |
| DEL-05-01 `prototype/assemble_tool_calls.py` | cdac36935a25 |
| DEL-05-01 `prototype/README.md` | 72eaad3ac190 |
| DEL-05-02 `PANEL_RECEIVING_CONTRACT.md` | 9654ef8488f0 |
| DEL-04-02 `AUTONOMY_AND_STANDING_EXCHANGE.md` | 8cf788401763 |
| DEL-04-02 `AS_SETTINGS_IN.schema.json` | 206045da42da |
| DEL-04-02 `AS_SETTINGS_IN.invalid.examples.json` | 8ae502e16398 |
| DEL-04-02 `prototype/validate_settings_in.py` | 4996fdae927a |
| DEL-04-02 `prototype/README.md` | 6138db04e92c |
| DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` | 3421bb3539ca |
| DEL-09-06 `CONNECTED_ACTIVITY_CONTRACT.md` | 302df238a36c |
| DEL-09-06 `w14-result-record.schema.json` | 20d3c9769123 |
| DEL-09-06 `w14-result-record.example.valid.json` | 3b3752112dc3 |
| DEL-09-06 `w14-result-record.example.invalid.json` | c8789ae3fedf |
| DEL-09-06 `prototype/run_w14_rehearsals.py` | 1c4680857856 |
| DEL-09-06 `prototype/README.md` | 5a510eee1c01 |
| DEL-09-09 `EXTERNAL_TRACE_CASES.md` | 94db99fe6824 |
| DEL-09-09 `xt-result-record.schema.json` | 3b0ff2bbd1da |
| DEL-09-09 `xt-result-record.example.valid.json` | 09ea87a5aaf6 |
| DEL-09-09 `xt-result-record.example.invalid.json` | a3c00d661cbf |
| DEL-09-09 `prototype/run_xt_suite.py` | d65c3f9ca496 |
| DEL-09-09 `prototype/README.md` | c8724e8b9fab |

`git status --short` shows these among the changes; the other changed paths
belong to RP-1, RP-2 and RP-3.
