# RQ — repairs from V19 and final GUIDE re-pin (return)

Node RQ of run `APP-V4-DESIGN-PASS-2-20260930`. Executor: Type 2 TASK
(Claude Code subagent, Claude Opus 5.5), no delegation. Date 2026-09-30
local (MDT); final runs 2026-10-01 03:07 UTC. Working tree at `8c575f739e`,
clean at start. No git writes, no network, no package install. Scratch:
the session scratchpad `…/scratchpad/rq/` (below: `<scratch>`).

**Read whole before acting:** `BRIEFS.md` ("Common rules", "Wave B"
common rules, "RQ"; sha256 `1f5ed0db0086…`), `reviews/V19-A.md`
(`2c7ff2b0f208…`), `reviews/V19-B.md` (`dd467919a844…`),
`R15_RESOLUTIONS.md` (`5f63689a05e8…`), `R14_RESOLUTIONS.md`
(`c6a603303693…`), `WAVE_B/B8.md` (`e02a8e4b3df7…`). **Read in part:** each
passage a finding quotes, with its section, in the 16 Design files; their
change tables; the prototype READMEs; the relevant schemas; R9-1 and
OWNER_DECISIONS K1-1 (for V19-B n-6); `OBS_1_0.158.0.md` §5 (read only).
The Design files were not read whole (about 2.5 MB); edits are confined to
the passages read.

**Fence:** only Design files of the 16, their schemas, examples and
`prototype/` files, and this file. Not touched (checked with `git diff
--quiet HEAD`): `PIN_SPIKE_0.158.0.md`, `OBS_1_0.158.0.md`,
`prototype/obs1/`, RELAY, ANS, FACTS, `docs/`, `_DAG/`; no ScopeOfWork,
register, status, basis, decomposition or scope-change file. No version
bump; an "RQ" row in each changed file's Wave B change table (15 files).

## 1. Findings, where each was fixed

### V19-A

| Finding | Class | Fixed where |
|---|---|---|
| **M-1** ADAPTER→RS token map fails for `agent_written_configuration` | MAJOR | RS §5 "Supplier tokens" adds `agent_written_configuration` → *agent-written configuration* and states every other limit token follows the underscore rule. ADAPTER `observe_map.py`: `RS_LIMIT` gains the entry; new `vocabulary_check()` maps **every** outcome (21), request kind (8) and evidence limit (18) of `external_dispatch_record.schema.json` through `rs_entries()` and validates the RS entries: 48 of 48. Negative control (entry removed in memory): "47 of 48 … 'agent written configuration' not in enum", RESULT 1 failure. CA and XT prototype maps gain the same entry; their examples regenerated (only the recorded sha256 of `observe_map.py` differs). ADAPTER README, RS §15 |
| m-1 RS §13 overstates `$ref` resolution | MINOR | RS §13 files table, `RS_RECORD.schema.json` row: a 2020-12 validator resolves against the `$id` base (a URN), so the reference stays a bare relative path; registering EXEC's schema by its own `$id` does not help; a loader must map it (retrieval rule relative to the RS file, as `minischema.py` does, or EXEC registered under that path). Checked with jsonschema (§3). RS prototype README notes the same |
| m-2 `namespace` mechanism cited as observed | MINOR | Per the ruling: ADAPTER §3.5 (`mcpToolCall` row) and GUIDE M9.3 state the observations (LM Studio logged the `namespace` tool type as unsupported; the MCP test tool never reached the model; no `mcpToolCall`) and label the mechanism OBS-1's inference. The same wording was in HOSTING §8.1 L-3 and F-31, WD `mcp-tool-call`, EXEC AW-1 and U-E26; corrected there too for consistency (HOSTING OB-1 already said it). R13-6 itself not touched (run record) |
| m-3 stale sibling labels in live text | MINOR | ACT, AS, RS, C, P, ADAPTER: live citations moved to Wave B labels in 45 line edits (ACT 9, AS 5, RS 4, C 6, P 3, ADAPTER 18), by a line-anchored script (each old string asserted on its line): Phase header lines of C, P, ADAPTER; ACT §2.7, §4, §4.0, AP-10; RS §1, R8; AS §1, §4; C §0, §3.1, §4.1, §7.1; P §0, PM-1; ADAPTER §0, §1, §3.1, §3.3, §3.4, §9, §10, F-20 and the verification-case sentence (now EXEC-v0.6, WD-v0.8); fixture lines "carried in C-v0.8". Kept: history rows, consumed-input lines and origin citations ("C-v0.4 §10", "C-v0.5 §10.4", "through C-v0.6", F-14…F-19, F-21). Each target section was checked to exist in the Wave B text |
| m-4 ADAPTER §3.5 preamble | MINOR | Now: "…unless marked *Observed (OBS-1/OBS-1b)*, which are dated live observations at this pin (one local route, one model), not qualification" |
| m-5 identifier reuse | MINOR | Renamed while PROPOSED: ACT §8.5 CE-n/CR-n/CX-n/CD-n → CQ-E0…E5, CQ-R0…R4, CQ-X0…X4, CQ-D1…D4 (text, schema enums, invalid example); C §6.1 RC-1…RC-4 → RR-1…RR-4 (C's receipts RC-1…RC-3 unchanged). GUIDE identifier notes, M1.5 and F-17 updated (CX-n added). Grep found no other citation of either set |
| m-6 RS bookkeeping | MINOR | RS §4.4 rows for the R14-1 kinds, R14-3 labels and R15-1 `notStarted`; §14.1 run-start row names `notStarted`; VC-31 counts five logs; §15 gains the B8/RQ rerun bullet; prototype README counts five logs and INV-RS-1…15 |
| m-7 R15-1 not in LOOP §3.2 | MINOR | As V19-B B-1 below |
| n-1 ownership without label; "Decided" | NOTE (done) | AS §3.2 "Owner (DERIVED, from CLM-002 and DEP-04-02-018)"; LOOP DF-9 "(DERIVED)"; AS and RS change rows "Designed here (PROPOSED representation)" |
| n-2 RD-2 section | NOTE (done) | ADAPTER §4.3 RD-2 cites C-v0.8 §2.1 CI-3 |
| n-3 LC-2 cites FC-1 for faithful recording | NOTE (done) | ACT LC-2: FC-1 for the late write; RS §6.1 *faithful recording* for another recorder |
| n-4 two readings in GUIDE order of use | NOTE (done) | GUIDE §3 item 2: "HC-1…HC-4, checked in that order (a host may claim the four rows together, before any later row; the claim rule below)"; the duplicate sentence removed |
| n-5 "run owner" undefined | NOTE (not done) | Defining it is EXEC's (CE-17, AE-7) and outside a repair; returned |
| n-6 governance-phase annotation labels | NOTE (done) | `RS_RECORD.schema.json` annotation branch description |

### V19-B

| Finding | Class | Fixed where |
|---|---|---|
| **B-1** R15-1 not in PANEL; LOOP §3.2 row | BLOCKING | Per the ruling. PANEL §3.9 RI-1, RT-d and §7 PC-42 read **run not started — no model selected** (notice to choose, no default, no boundary refusal, message kept unsent); "model request refused at boundary" kept only for *no credential*. `PANEL_RETURN_INPUT.schema.json` refusal value "no model chosen" → "run not started — no model selected" (valid example unaffected). LOOP §3.2 turn table: the row split (no model selected → no turn, F-2 (a); no credential → *failed*, F-2 (b)). GUIDE F-18 answered; §5 R15-1 row extended |
| M-1 work graph | MAJOR | Integrator's; not touched |
| m-1 EXEC §2.5 opening paragraph | MINOR | Rewritten as the reviewer proposed (two supplier turns observed on one local route; not App runs, not qualification; remaining cells pending with their reason) |
| m-2 WD §3.6 spelling table | MINOR | EXEC column by schema: reached-when `a`/`b`/`c` in the report, WD's tokens in the record-entry bodies; capturing surface WD's tokens (the report carries none). Checked against both EXEC schemas |
| m-3 WD HC-6/HC-7 group IDs | MINOR | Written in full: HCG-A12…HCG-A17; "the subjects of act A14" kept as an act code |
| m-4 when a host-loop run is "not started" | MINOR | LOOP §3.2 workflow-run table (PROPOSED): the run opens, and `run_opened` is written, at its first turn start; with no model selected, `run_opened` with `notStarted` and nothing more (state *not started*, final); in a live run nothing is written for such a message. F-2 (a) and PANEL RI-4 follow |
| m-5 CA stale cells | MINOR | CA §2.6 CA-R "(no App run; OBS-1 observed supplier turns only)"; F-28 "**Answered (RP-1):** EXEC-v0.6 RT-11 lists MT-17, CH-32 and CH-33" (checked: EXEC RT-11 row; added in `c3d5b8d841`) |
| n-1 "Current pins" bullets | NOTE (done) | Relabelled "Pins as of node A4 …" in WD, WD-EX, EXEC, LOOP, PANEL, HOSTING, and also ACT, AS, RS, which carry the same bullet |
| n-2 redaction (time zone; brief path) | NOTE (not done) | The rollout name is in `OBS_1_0.158.0.md` and the path in `WAVE_B/OBS-1_BRIEF.md`, both outside the fence. HOSTING `prototype/results/RUN_*.txt` print "MDT"; they are recorded outputs and were not rewritten. A rerun of `run_cases.py` prints "MDT" too (it prints `date`'s local zone) |
| n-3 AW-2 and OM-1's compound limit | NOTE (done) | EXEC AW-2 cites OM-1's limit "dispatch recognized from compound command" |
| n-4, n-5 | NOTE | No fix proposed by the reviewer; none made |
| n-6 K1-1 quotation | NOTE (done) | WD §3.5 option (b) attributes the quoted words to R9-1's part (i), settled by K1-1 ("the product gives the agent the checkpoint") |
| n-7 README exit status | NOTE (done) | LOOP and PANEL prototype READMEs say `schema_subset.py` exits 1 by design on an invalid example |

Counts: BLOCKING 1 and MAJOR 1 fixed (V19-B M-1 is the integrator's);
MINOR 12 of 12 fixed (V19-A 7, V19-B 5); NOTE 9 done, 4 not done (V19-A
n-5; V19-B n-2, n-4, n-5).

## 2. Joins

- PANEL `PANEL_RETURN_INPUT.schema.json`: the loop outcome value "no model
  chosen" is now "run not started — no model selected". LOOP states no
  refusal token of its own for it (F-2 (a)); no other file uses the old
  token (grep of all Design `.md`, `.json` and `prototype/*.py`).
- LOOP §3.2: `run_opened` is written at a host-loop run's first turn
  start (PROPOSED). RS R1 and §13.3.1 already put `notStarted` on
  `run_opened` "for a host-loop run that never reaches its first turn";
  nothing in RS needed to change.
- ACT §8.5 and C §6.1 renames: no other file cited either set (grep); GUIDE
  updated.
- ADAPTER→RS token map: RS §5, `observe_map.py`, and the CA and XT copies
  now agree on `agent_written_configuration`.

## 3. Checks

**Prototype reruns** (2026-10-01 03:07 UTC; Python 3.13.7, node v24.5.0,
macOS; `PYTHONDONTWRITEBYTECODE=1`; driver `<scratch>/runall.sh`; outputs
in `<scratch>/final/`). Every output equals the baseline taken before any
edit (`<scratch>/base/`, temporary paths stripped) except the two lines
noted.

| Prototype (README command) | Result |
|---|---|
| C `run_fixture.py --out …/sh1` (SH-1) | 22 of 22 checks; 34 items; 30 host documents |
| C `validate_all.py --run …/sh1` | "RESULT: all checks passed" |
| ADAPTER `observe_map.py --run …/sh1` | 43 of 43 RS entries; **new line:** "PASS RS-v0.8 §5 token map (RQ): every schema value -- 21 outcomes, 8 request kinds, 18 evidence limits -> 48 of 48 RS entries valid"; "RESULT: all checks passed". `--write-examples` rewrote the ADAPTER examples byte-identical |
| P `proposal_states.py --check …/sh1` | 23 PASS; "RESULT: all checks passed" |
| ACT `validate_policy.py` | "RESULT: all expectations held" (after the CQ- rename) |
| AS `validate_settings_in.py` | "RESULT: all expectations held" |
| RS `run_prototype.py` | 51 PASS, 0 FAIL: five logs (3, 20, 12, 20, 1) valid and byte-equal round trips; INV-RS-1…15 rejected; FC-1…FC-7; R14-1 block 19/19, 12/12, 40/40 |
| RS `exec_to_rs.py` | "40 of 40 written and valid"; "every entry valid, none without a kind" |
| WD `wdproto.py selftest` | 62 checks, 62 passed |
| EXEC `run_all.py` | "ALL CHECKS HOLD: 0 failure(s)" |
| HOSTING `run_cases.py` | "TOTAL 35, pass (model) 35, FAIL 0" (only the start-time line differs) |
| LOOP `assemble_tool_calls.py` | 22/22 |
| LOOP `destination_flow.py` | 68 RS entries, 11 request records valid; "all expectations held"; `--emit` output `cmp`-identical to RS's host-destinations log |
| LOOP, PANEL `schema_subset.py` | each VALID example VALID, each INVALID example INVALID (exit 1 by design); PANEL's copy `cmp`-identical to LOOP's |
| PANEL `panel_double.py` | 4/4 |
| CA `run_w14_rehearsals.py` | "ALL CHECKS HOLD"; the valid example "validates and equals the regenerated W14-05 record (date aside)" |
| XT `run_xt_suite.py` | "ALL CHECKS HOLD"; both result-record and both work-account examples as claimed |

`git status` showed no untracked file after the runs.

**`$ref` resolution with jsonschema** (already installed: jsonschema
4.26.0, referencing 0.37.0; nothing installed; script
`<scratch>/js/rs_refs.py`, not product code):

```
check_schema: RS, EXEC, AS, ACT ok
1. by $id only: Unresolvable -> ../../../../PKG-02_Workflow%20and%20role%20portability/…
2. retrieval asked for (the resolved URI): ../../../../PKG-02_Workflow%20and%20role%20portability/1_Wor…/Design/checkpoint-record-entries.schema.json
3. RS_RECORD.valid.*: 3, 20, 12, 20, 1 of the same valid   (retrieval rule: path resolved against RS's directory)
3. RS_RECORD.invalid.examples.json: 15 of 15 rejected
4. EXEC registered under the resolved URI: 56 of 56 valid entries valid
RESULT: ok
```

A second script (`<scratch>/js/changed.py`) ran `check_schema` on the 11
schemas in the folders RQ touched (ACT, AS, RS, EXEC entries, PANEL, ADAPTER
×3, CA, XT ×2), every schema registered by `$id` plus the RS retrieval rule:
32 of 32 expectations held (every valid example valid, every invalid one
rejected).

## 4. GUIDE re-pin (last, after every other edit)

Script: B8's `pins.py`, copied unchanged to `<scratch>/pins.py` (sha256
`b943319dc4a00bd79e79dde5c0a629e4026d56f099389ee7321cb2763f275423`, equal to
B8's record). Run 1 (check): 4/18 (SPIKE, RELAY, ANS, FACTS). Run 2
(`--write`): "match 4/18 (before write)". Run 3 (check, final bytes):

```
C        CATALOG_AND_READ_BASIS.md                  pinned 118f48108287dce9… current 118f48108287dce9… match
P        PROPOSAL_LIFECYCLE_AND_OUTCOMES.md         pinned f432356d054cb784… current f432356d054cb784… match
ADAPTER  ADAPTER_ENABLEMENT_AND_RECEIVING.md        pinned 7cad04c873c0f115… current 7cad04c873c0f115… match
ACT      ACT_AND_POLICY_CONTRACT.md                 pinned 3333a69de2d2d472… current 3333a69de2d2d472… match
AS       AUTONOMY_AND_STANDING_EXCHANGE.md          pinned f1618105ed1ce2bd… current f1618105ed1ce2bd… match
RS       RECORD_SEMANTICS.md                        pinned 1da4ad1103e5065a… current 1da4ad1103e5065a… match
WD       WORKFLOW_DECLARATION.md                    pinned d6ceac20bd0c1bf8… current d6ceac20bd0c1bf8… match
WD-EX    EXAMPLES.md                                pinned 046a44fe0501df23… current 046a44fe0501df23… match
EXEC     EXECUTION_COMPATIBILITY.md                 pinned 4d55f0e8fcc1d98a… current 4d55f0e8fcc1d98a… match
LOOP     LOOP_RECEIVING_CONTRACT.md                 pinned f0065788b7723601… current f0065788b7723601… match
PANEL    PANEL_RECEIVING_CONTRACT.md                pinned e297960192533462… current e297960192533462… match
HOSTING  HOSTING_BOUNDARY.md                        pinned 9018828b31f39893… current 9018828b31f39893… match
SPIKE    PIN_SPIKE_0.158.0.md                       pinned 0e090a4ca14e3ec3… current 0e090a4ca14e3ec3… match
CA       CONNECTED_ACTIVITY_CONTRACT.md             pinned 332c3f25c02e1e13… current 332c3f25c02e1e13… match
RELAY    RELAY_QUESTIONS_SWBPIPE.md                 pinned 34efb532388202ab… current 34efb532388202ab… match
XT       EXTERNAL_TRACE_CASES.md                    pinned daf6c9c946ec1520… current daf6c9c946ec1520… match
ANS      RELAY_ANSWERS_SWBPIPE.md                   pinned afb6e063e7e5dfcc… current afb6e063e7e5dfcc… match
FACTS    FACTS_SQ01_SQ32.md                         pinned 733fb88a701317be… current 733fb88a701317be… match
rows 18; match 18/18
```

GUIDE's v0.5 Basis bullet (R12–R15, BRIEFS, V17, OBS pins) was not
re-pinned: outside the brief. BRIEFS now differs from GUIDE's pin
(`e3a4c4ae…` → `1f5ed0db0086…`, the RQ brief added).

## 5. Not done, returned

- V19-A n-5 (*run owner* undefined in RS and ACT): EXEC's term (CE-17,
  AE-7); for EXEC's owner.
- V19-B n-2 (redaction): `OBS_1_0.158.0.md` and `WAVE_B/OBS-1_BRIEF.md`
  are outside the fence; HOSTING's recorded run outputs were not rewritten.
- R13-6's own wording of the `namespace` mechanism (V19-A m-2's
  suggestion) is a run record; not touched.
- No ScopeOfWork, register or basis item proposed.

## 6. Changed files (sha256)

| File | sha256 |
|---|---|
| DEL-01-01 `HOSTING_BOUNDARY.md` | 9018828b31f398931aee2fa7a5fb9328069c794e2698f801b037f1bedab0c1a4 |
| DEL-02-01 `EXAMPLES.md` | 046a44fe0501df238cee06ec456ebbe652ad58544088dce5e0171e22c767c57a |
| DEL-02-01 `WORKFLOW_DECLARATION.md` | d6ceac20bd0c1bf81715d0458e330e640cbf53559e6f29aa4f86f4f01f365380 |
| DEL-02-03 `EXECUTION_COMPATIBILITY.md` | 4d55f0e8fcc1d98a558ef9cedc97ec800a98a617ebde0d789e933e0bb9fe1d2f |
| DEL-03-01 `CATALOG_AND_READ_BASIS.md` | 118f48108287dce96628d9091da1cf43134594152b8d12ccd267e19cfc6206da |
| DEL-03-02 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | f432356d054cb784ded51325de25ef945ddf29e9843cc187e3576841bac6533f |
| DEL-03-03 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` | 7cad04c873c0f1154a7a8ea8427772497a863f57167d420c485ea00373acca0c |
| DEL-03-03 `prototype/README.md` | 411e4d6634ec507d0d63b284901e8d07579bc9089151e8c4b10136a3ba663502 |
| DEL-03-03 `prototype/observe_map.py` | 1e0402c016a73920e95c5d7d5fc03b4d384f156e7286d59fd75087df2b6b971a |
| DEL-03-04 `HOST_INTEGRATION_GUIDE.md` | 4b4d43b9563e84f4d0a818b99bc39e8ddc9780001c5d9cfffa5132beb6bdfb4c |
| DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` | 3333a69de2d2d47238b3afaae6129076af5f752edd3d6609d9f564718d7849c9 |
| DEL-04-01 `ACT_POLICY_CLASS_RECORD.invalid.examples.json` | 39af33974ba7253de85274b059d43ffd159f7f7629bfd42344ac06ab4e5b4a72 |
| DEL-04-01 `ACT_POLICY_CLASS_RECORD.schema.json` | 694a284f48155ab7a7d0e24d47ec809a06ec3a909dbb104a28374164d3f6cb7e |
| DEL-04-02 `AUTONOMY_AND_STANDING_EXCHANGE.md` | f1618105ed1ce2bda88265415f54a1835c518d5bd8c60b90d93654fe22413ba0 |
| DEL-04-03 `RECORD_SEMANTICS.md` | 1da4ad1103e5065ad1a83c2aeb4dee7446b76543ac158df5444dad27d41f1d01 |
| DEL-04-03 `RS_RECORD.schema.json` | 019483497d8f9a426afdb91b65170dc9e69acc7a1be1d43d7c0f7332bacedd14 |
| DEL-04-03 `prototype/README.md` | 063acb68281e281d7a2a293404e79c05b70c6e4396f1fe8cfbce7dbbe1b196d9 |
| DEL-05-01 `LOOP_RECEIVING_CONTRACT.md` | f0065788b77236017df8573a1cb5f02fa40429fb96af3210b4582f2683097f8d |
| DEL-05-01 `prototype/README.md` | 0218e16675866b29619151999977b45754f26b6f34873a64c3ddccb6acbe28f3 |
| DEL-05-02 `PANEL_RECEIVING_CONTRACT.md` | e29796019253346268107f287f81605158b03ee5d865042efcce1489b4e7a804 |
| DEL-05-02 `PANEL_RETURN_INPUT.schema.json` | c0f7cc5d5170005a0c0fb0bca247a60ed5aa385c88b64bfc1d50a2d2cc7bc18a |
| DEL-05-02 `prototype/README.md` | 0d0b2d9b13c034d41cb7cbb6e04b3ff47c5596cd62715456434ef494536b2cf7 |
| DEL-09-06 `CONNECTED_ACTIVITY_CONTRACT.md` | 332c3f25c02e1e13f63e03a7650316b63feef3afd5645594ead15fd284bcb1aa |
| DEL-09-06 `prototype/run_w14_rehearsals.py` | f0460093ddd6305df191d40ca7da3f467e4eb0814f546d251d1a8855a81a62f8 |
| DEL-09-06 `w14-result-record.example.invalid.json` | fb1f4886bd8b55c64e38fca03601423877d53be3397f95f867fd4b26da7715d9 |
| DEL-09-06 `w14-result-record.example.valid.json` | f41928de19bd0a5128f5f53c76ee0df705684586b4bca520746a4203a134d3d8 |
| DEL-09-09 `EXTERNAL_TRACE_CASES.md` | daf6c9c946ec15207b5e10321e36301a7fc9a8e103607c8befe8133fcccb5777 |
| DEL-09-09 `prototype/run_xt_suite.py` | 06affb229178211853d8aee4ef844ee1315f7d0f45c69ab2393bbb10b331f2a6 |
| DEL-09-09 `xt-result-record.example.invalid.json` | e240b41f60a103246992c93c0650e8ae0a25a9eb742db5c3c257914f87f83f48 |
| DEL-09-09 `xt-result-record.example.valid.json` | d3d77934d739fbf4afbd3b05c2f98b26aaaf6436e785c2b525db1949aabcc2f8 |
| `WAVE_B/RQ.md` (this file) | computed by the integrator |
