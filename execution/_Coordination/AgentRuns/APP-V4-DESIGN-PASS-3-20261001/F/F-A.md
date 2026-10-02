# F-A return — HOSTING v0.8 → v0.9 (DEL-01-01)

- Run `APP-V4-DESIGN-PASS-3-20261001`, node **F-A**. Executor: Type 2 TASK (Claude Opus 5.5), harness-native descendant of the HELP_HUMAN session; did not delegate. 2026-10-02, HEAD `e4e14d6ae6`.
- Boundary kept: read-only git; no network; no Codex or model run. Written: `DEL-01-01/Design/HOSTING_BOUNDARY.md`, `hosting.server-request-entry.schema.json`, three new fixtures of that schema under `prototype/fixtures/`, and this file. No `OBS_*`, `PIN_SPIKE_*`, `generated/`, prototype program, README or results file was changed (checked with `git status`). Scratch: `$TMPDIR/fa/`.
- **Fence reading to confirm:** the brief allows the schema "and its fixtures" where FH-17/FH-18 require. I added three new fixture files for that schema rather than altering the two the prototype run uses. If only existing fixtures were meant, delete the three; nothing else depends on them.
- Inputs: BRIEFS `316ea293…`, F0_JOINS `e93608be…`, R17 `b0af81bc…`, R18 `abf5eee6…`, R19 `16930ecd…`, R20 `516d0fe0…` (arrived mid-node), OWNER_DECISIONS `ea96c557…`, DECISIONS_PENDING_2 `0ecbf87a…`, OBS-2 record `61cc34ff…`, OBS-3 record `554ac445…`, and the D1/D2/D4/D6 "Round 2" sections (§R2.3). Full hashes are in HOSTING's v0.9 inputs line. The pass-3 Design files are cited by v0.2 label and section, using section numbers as read in their working text; **F-E should check them** (notably ACCESS-v0.2 §19, §18; ROLE-v0.2 §3.1 SL-8, §4.4, CR-1a, F-1; NPTD-v0.2 §5.4, §6.4, §7.1, §12; RECOVERY-v0.2 §5 SQ-Q, F-R10).

## 1. Rows applied

Every row is listed with its location in HOSTING's "Changes from v0.8" table.

- **Header and stale pointers.** FH-44 (version step; v0.9 inputs; Receivers line); §1.14 L13, L985, L986 (with FH-38).
- **Supplier facts name their version.** R19-5: a version rule in the header, plus a version-advance check in §9.5.
- **Stop, generations and homes (L-1).**
  - FH-01 + D1 H-1: DEF-5a by quit or Stop/Restart Codex, per home; process group ended.
  - FH-06/FH-31 + D1 H-5 + D4: generation identity {App session, App-owned home, spawn counter}; §4 per home; U-12 per-home dimension.
  - FH-02 (U-10 closed); FH-03 (R3; U-11 closed); FH-04 (§6.5 reconciled; U-14 and F-01 closed).
  - FH-05 + D1 H-10 (C-03: a closed generation's events are not re-read); FH-07 + D1 H-6 (U-09 narrowed, U-16 PROPOSED policy).
  - D1 H-9 / G-5: graceful-stop history note in §4.5, citing RECOVERY §5 SQ-Q.
  - FH-08, FH-09.
- **Account home, handshake and identity.**
  - FH-10 + D4 FH-10: links for `config.toml`, `AGENTS.md` and `skills/`; OBS-2 O-6; no internal or credential environment variables.
  - FH-11: `experimentalApi: true` recorded per generation; `explicitGatewayOauth: true` PROPOSED. F0's premise note is applied: the edit is at both §4.2 step 4 and F-13.
  - FH-12, FH-13; FH-14 + D4 FH-14 (session flags carry analytics off, and `plugins = false` only in the fallback).
- **Server-request register.**
  - FH-15 (U-20 narrowed); FH-16 (RT-08 guard; `cancel` acts as decline plus interrupt).
  - **FH-17**: secret values redacted. Schema: `secretValuesPresent`, `redaction` and a conditional rule.
  - **FH-18**: `actorRef` form per C-10. Schema: a pattern.
- **Receiving sides and pointers.** FH-19 + D4 FH-19 (F-15 closed for S-1…S-4; S-4 by ACCESS-v0.2 §19); FH-20, FH-21 (+R18-5), FH-22, FH-23.
- **Access and network.** FH-24 + D4; FH-25; FH-26; FH-27 + D4; FH-28; FH-29 + D4 (R18-3, L-3); FH-30; FH-32.
- **Capability account.** FH-33 + D2 J-2: C-04 signal, "not established" otherwise, C-05 label. The "@deprecated Ignored" text was checked in the committed bundle, on thread start and turn start params.
- **Guidance carriage and observations.**
  - FH-34 + D6; FH-35 + D2 J-4.
  - FH-36 and FH-37 + D6 (see §3; R20-3 and R20-6 noted in §8.2).
  - FH-39 + D6 (CR-1a: the carrier is not observed).
  - FH-41 (new §10.2 OBS-2, §10.3 OBS-3; U-19 narrowed); FH-42; FH-43.
- **New finding.** F-33 "Accepted is not applied" (OBS-2 O-5, OBS-3 W-1, W-3, W-6).

## 2. Rows not applied, or applied in part

| Row | Status | Reason |
|---|---|---|
| FH-40 | No text change | Record only (F0). Superseded by R19-7: DEL-02-02 now composes the run-start text itself. S-6 names DEL-02-02 |
| D2 J-10 (G-3 "a goals group in Part A") | **In part** | The goals are placed in §8.4 as a note beside HCG-B04's goal methods and notifications. **No new Part A group was added.** I tried HCG-A18; it broke DEL-02-01's prototype check S-11 (VC-31), which hard-codes 27 groups (`wdproto.py` line 662; selftest went 61/62). A group with no App Server member would also add nothing to the account. If the integrator wants the group, F-D must change S-11 to 28 first, and then the row can be added (VC-30 passed with it) |
| D4 "content sent to the provider shown in the network view" | Applied as redaction categories (§9.1) plus OB2-11 | The network view itself is DEL-01-05's (ACCESS §9); HOSTING has no network-view section |

## 3. Where R19 overrides F0

- **FH-36 (S-6).** F0 asked to list `thread/fork` as a carrier and to keep "idle-boundary change policy". Applied per R19:
  - Role guidance is carried only at `thread/start`.
  - Resume and fork accept the element and ignore it (O-5, W-6), and the App sends none.
  - The role is fixed for the conversation's life (L-2, R19-3).
  - A workflow is a text element of the run-start `turn/start`, composed by DEL-02-02 (R19-7).
- **FH-37 (§8.2).** F0 asked to add `thread/fork` and `collaborationMode.settings.developer_instructions` as carriers. Applied per R19:
  - Fork is listed as "accepted, not applied", and the App sends none (R19-8).
  - `collaborationMode` and `thread/settings/update` are not used for workflows (R19-7); a non-null value is recorded if one is ever sent.
  - The `skill` and `mention` inputs are recorded as not used (R19-7).

## 4. Files and sha256

| File | sha256 |
|---|---|
| `DEL-01-01/Design/HOSTING_BOUNDARY.md` (HOSTING-BOUNDARY-v0.9; was `3cf0381c…6b1` at v0.8) | 77df7c12f7d5e1eec916ae603f261944c5e95731f8470266b9b9a1879ea97c81 |
| `DEL-01-01/Design/hosting.server-request-entry.schema.json` (`$id` …:v0.9; was `dda16758…`) | 080ccac2846b5d38d7285aa955f487756ef4bffda8c9670a131d8c747cb1d354 |
| `prototype/fixtures/server-request-entry.secret-redacted.valid.json` (new) | 3b2ee4934c74d6a58c422b090f398c987ba280cd9e729860a95cd8b987374ee4 |
| `prototype/fixtures/server-request-entry.secret-kept.invalid.json` (new) | 59d8a445e25424869ca6bcfc6743302cdcc12329f331c19cdce82d2b0d0c2c2e |
| `prototype/fixtures/server-request-entry.actor-form.invalid.json` (new) | 686bdd061b7349b67a107e69e3f6cc9a882dd396cbc6fed865bed75743f985ff |
| `prototype/fixtures/server-request-entry.valid.json`, `.invalid.json` | unchanged (0bca3b37…, 67ef44b0…) |

## 5. Rerun output

Command: `PYTHONDONTWRITEBYTECODE=1 python3 run_cases.py`, run in `DEL-01-01/Design/prototype/` on 2026-10-02 (final run started 13:01:11 MDT). Python 3.13.7, Darwin 25.6.0 arm64. Exit status 0. Lines are trimmed to 200 characters.

```
B6 supplier-double run — started 2026-10-02 13:01:11 MDT — python 3.13.7
SEED-A-bin-freshhome                   pass (model)  4/4 frames byte-identical; exit 0 (recorded 0)
SEED-A-bin-warmhome                    pass (model)  4/4 frames byte-identical; exit 0 (recorded 0)
SEED-A-bin.first-attempt               pass (model)  4/4 frames byte-identical; exit 0 (recorded 0)
SEED-A-vendor-warmhome                 pass (model)  4/4 frames byte-identical; exit 0 (recorded 0)
SEED-B-bin                             pass (model)  3/3 frames byte-identical; exit 0 (recorded 0)
SEED-C-bin                             pass (model)  3/3 frames byte-identical; exit 0 (recorded 0)
SEED-D-bin                             pass (model)  2/2 frames byte-identical; exit 0 (recorded 0)
SEED-D-vendor                          pass (model)  2/2 frames byte-identical; exit 0 (recorded 0)
SEED-X                                 pass (model)  8 transcripts equal except emittedAtMs
VC-16                                  pass (model)  notification received before `initialized` (position 2 of g1) was held and delivered right after ready(g1); not dropped
VC-08 (part: X-01 side)                pass (model)  delivered frame byte-identical to the recording incl. emittedAtMs; metadata beside; handshake identity ['codexHome', 'platformFamily', 'platformOs'
VC-16 (b: requests while handshaking)  pass (model)  two server requests sent before `initialized`: entries created at receipt (R1; positions 3, 4), the unfamiliar one errored at once (R2), the known 
VC-21                                  pass (model)  unknown client method -> response-observed(error) -32600 (recorded message, name substituted: mutated), not unknown; connection continued (second r
VC-03                                  pass (model)  entry created (R1), classified unfamiliar, explicit error written (R2, code -32601 TEST VALUE); no affirmative answer
VC-20                                  pass (model)  opt-in false: currentTime/read and attestation/generate unfamiliar -> explicit errors; experimentalApi true: currentTime/read familiar, answered by
VC-22                                  pass (model)  app-rule content answer to requestUserInput and affirmative to fileChange refused origin-not-permitted (entries stay outstanding); app-rule decline
VC-23                                  pass (model)  person's 'yes, accepted' settles the elicitation (person-via-interaction) and is written to the supplier as conversation input; the boundary emits 
VC-14 (part: X-12 with double)         pass (model)  invalid form -> refused(invalid-answer); app-rule affirmative A14 -> refused(origin-not-permitted); person accept -> accepted-for-write; second ans
VC-04                                  pass (model)  4 malformed frames counted and surfaced with generation and position (not-json, not-an-object, unclassifiable, oversize > 262144 B TEST VALUE); val
VC-06                                  pass (model)  handshake failed 3 times (child ended, exit code 0) -> restart-waiting twice, then halted-after-repeated-failure (bound 3 in 60s TEST VALUE); no au
VC-06 (b: unexpected exit)             pass (model)  exit code 0 with no stop record -> exited-unexpectedly (S-F-07); pending client request -> unknown-no-response; outstanding entry -> ended-unanswer
VC-24                                  pass (model)  status list delivered natively (runtimeStatus 'disabled' passed through as App-side configuration; no act record); agent's mcpToolCall items delive
VC-25                                  pass (model)  Phase 1: no run holding; no named-rule decline, no run-holding refusal, no turn/interrupt; App-initiated call handled by §6.8 rules; tool-permissi
VC-26 (part: constructed re-route)     pass (model)  requested and effective kept apart per turn; re-route recorded on turn-ex-1 (effective example-model-b); turn-ex-2 has no report -> unknown, not fi
VC-10 (constructed identity)           pass (model)  same label, different content identity -> refused mismatch(distribution content identity); no child started
STOP-close-input                       pass (model)  stop record written first; exit code 0 (recorded behaviour) not used to classify; deliberate from the stop record; descendants checked (0)
STOP-termination-signal                pass (model)  stop record written first; exit code 0 (recorded behaviour) not used to classify; deliberate from the stop record; descendants checked (0)
LT-extra                               pass (model)  stop injected while verifying (LT-20), spawning (LT-19, LT-23) and handshaking (LT-18, LT-23) -> stopped; stop from restart-waiting and from halted
VC-27 (tables in HOSTING)              pass (model)  HOSTING §4.7 (23 rows) and §6.2.1 (13 rows) equal the model's tables
VC-30 (capability account)             pass (model)  §8.4 places 19 item kinds, 11 server-request kinds, 170 client methods and 85 notifications each in exactly one group; variant and (obs) marks mat
OBS1-test-doubles                      pass (model)  MCP test double: initialize (version echoed), tools/list, tools/call EX-1 (structured result, _meta seen) and EX-ERR (isError), -32601 for other me
TT-coverage                            pass (model)  lifecycle rows exercised 23/23 (not exercised: none); register rows 13/13
SCHEMA-records                         pass (model)  258 records emitted by the model validated against the 3 PROPOSED schemas
SCHEMA-fixtures                        pass (model)  lifecycle-event.valid: valid | lifecycle-event.invalid: invalid ($: missing required exitFacts) | client-request-record.valid: valid | client-reque
DOUBLE-conformance                     pass (model)  78 constructed or mutated frames emitted by the double valid against the committed 0.158.0 bundle
TOTAL 35, pass (model) 35, FAIL 0
```

Fixture check of the revised schema (scratch script, `jsonschema_subset.py`):

```
server-request-entry.actor-form.invalid.json invalid ($.settlement.origin.actorRef: pattern ^person:.* \(identity not verified\)$)
server-request-entry.invalid.json invalid ($.settlement.kind: not in enum ['decline', 'error'])
server-request-entry.secret-kept.invalid.json invalid ($.settlement: missing required redaction)
server-request-entry.secret-redacted.valid.json valid
server-request-entry.valid.json valid
```

Read-only compatibility runs of other nodes' prototypes. No files were written; `git status` was the same before and after.

- **DEL-02-01 `wdproto.py selftest`: 62/62 pass.** This includes S-11, which reads HOSTING §8.4.
- **DEL-01-04 `run_cases.py`:**
  - R-16 passed: every register entry it produced is valid against the revised entry schema.
  - The run itself exited 1, on an RS writer rejection: `derivedFrom` is not allowed in `relations`. That belongs to D3 and F-C's in-progress work, not to HOSTING.

## 6. Notes for the integrator and F-E

- **Pins to update later.** ROLE-v0.2 still names `thread/resume` and `thread/fork` as carriers in v0.1's §5.2. HOSTING follows R19 and D6 round 2 (the App sends none). F-E's GUIDE re-pin should pin RECOVERY, NPTD, NIR, AAC, ACCESS, ACCOUNT-HOME-RECORD, WR and ROLE at their final v0.2 bytes.
- **D3 and D5 round-2 items for HOSTING were not received before this return.** HOSTING cites NIR-v0.2 and AAC-v0.2 as in F0 (§4.1, §4.2 LB-4, §4.3 DM, §4.4, §4.5 SE, §5.2; AAC §7), and WR-v0.2 only as "run-start supply" with no section number.
- **One element is held as the ACCESS file states it.** `explicitGatewayOauth: true` is PROPOSED by ACCESS. Whether this capability is stable or experimental-only was not checked: only the experimental bundle is committed.
