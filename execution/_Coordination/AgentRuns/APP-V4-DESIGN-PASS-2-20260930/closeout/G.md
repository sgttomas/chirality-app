# G — items the closeout returned to the graph (return)

Node G, Type 2 TASK (Claude Code subagent, Claude Opus 5.5), dispatched by
HELP_HUMAN; no delegation. Written 2026-09-30 (local; runs ended about
2026-10-01 04:20 UTC). Working tree on `db6662d06c`. Read-only git; no
network; no install; no commit. Scratch: the session scratchpad
`…/scratchpad/nodeG/` and `$TMPDIR/g*`.

**Inputs read** (sha256 at this node): `BRIEFS.md` `32c89059…b348`
("Common rules", "Wave B" common rules, "G"); `R16_RESOLUTIONS.md`
`55444aa1…70ee` (binding); `closeout/C1-A.md` `e2cb79e2…6f73` (G-1…G-3);
`closeout/C1-B.md` `c819ba9b…34c8` (§9 G-1, G-2); `closeout/C1-C.md`
`9c4b9a37…dcb20` (§6 GW-1…GW-4); DEL-04-03 `ScopeOfWork.md` `ceecddbb…aa47`
(CLM-004); DEL-05-01 `Dependencies.csv` `6c86f226…03e6` (DEP-05-01-020,
read by script); `WAVE_B/RQ.md` §4 and `WAVE_B/B8.md` §3 (pin method). The
large Design files were read by section (headers, change tables, every
passage edited and the sections they join), not whole: LOOP §2.1–§3.2,
§5.1.1, §5.3, §9–§10, Findings, UNRESOLVED; PANEL §0–§3.10, §5, §7, Findings,
UNRESOLVED, VCs; EXEC §2.5–§2.7, §3, §4.9–§4.10, §7.1, §7.4, §8–§9, §11.5;
HOSTING §8.4; RS §4, §8, §10, §13.3, §14.1; AS §3–§3.2, §6, §12.1; GUIDE
header, §4.5, §5, F-9, UNRESOLVED. That is less than the Wave B rule "read
each file whole"; reviewers should know it.

## 1. Items, what was done and where

| Item | Done | Where |
|---|---|---|
| **R16-1** declined destination recorded (SETTLED by DEL-04-03 CLM-004); refusals without asking stay PROPOSED | Relabelled in all six files; history rows kept | RS header, §4 R15, §8, E13 example, §13.3, §14.1, VC-38, `RS_RECORD.schema.json` (two descriptions only); AS header, §3 *Declines*, DG-11, §3.2, §6 (= RS §8, checked identical after line 1), VC-23; ACT §2.7 *Decline*; LOOP header, §2.3 (two rows), E-4, NW-13, NW-15, §3.2, MS-19, §5.3 opening, Q-8, DF-8; PANEL header, ND-4, §5 A12 row; GUIDE M7.9 |
| **R16-2** panel-needs list | PANEL writes it; LOOP confirms or names gaps | PANEL new §3.11 (LN-1…LN-17, incl. FD-3's replay request as LN-16, and what the panel reads elsewhere), Receivers, F-13 closed, VC-08; LOOP new §10.5, §10.3 cell, G-10, UNRESOLVED row, VC-11 |
| **R16-3** IN-30 | Metadata only | RELAY UNRESOLVED next-relay row item (5) and change row R16-3; HANDOFF unrelayed list bullet |
| **R16-3** GUIDE review status | V19-A and V19b recorded; C0/G edits self-reviewed, V20 next | GUIDE Receivers, CC-10, F-9, UNRESOLVED; §5 R16 row; CC-9 |
| **R16-3** OBS redaction | Rollout file-name time redacted; change note | `OBS_1_0.158.0.md` §B.7; new "Change note (node G)" (old sha256 recorded) |
| **R16-3 / C1-A G-2** EXEC EV-3 | Rule active for 7 names with a §8.4 signal, inactive for 3 (person-input-request, image-view, plan-update); host loop on E has no supplier account → not established | EXEC EV-3, new EV-3a, §3.2, AW-3, MT-8, MT-15, new MT-18, §7.4, §8, U-E10; prototype `required_tool_check.py` (`harness_presence`), `run_all.py`, README. Follow-on wording: WD HC-4, §8 row, VC-50; WD-EX E1e, E8 L-WDEX-15, U-08 row; GUIDE M8.3 |
| **C1-A G-3** bookkeeping | Done | EXEC §9.1 DEL-04-02 row → AS-v0.8 §12.1, AS's *unconfirmed* reading confirmed (§4.10; SP-6); EXEC F-34 closed (RS L-12); "run owner" defined (EXEC RE-6; AE-7; shared spellings); RS §10 rows for DEL-03-04, DEL-09-02, DEL-09-05, DEL-10-03 and §10.1 cells |
| **C1-C GW-3** stale cells | Done | LOOP §10.1 and §10.3 at Wave B labels; LOOP G-12; PANEL VC-01 labels; PANEL §7 preamble; CA scope-item trace after §2.1 (SOW-040…241) |
| Pair check (GW-4) | **Not done** (brief: V20's) | Recorded as such in PANEL and LOOP G rows |

Every changed Design file has a "G" row in its Wave B change table (RELAY:
in its in-place change table); no version bump.

## 2. Panel-needs list and LOOP's confirmation

PANEL §3.11 has **17 rows** (LN-1…LN-17). LOOP §10.5: 14 supplied as
stated (LN-3 in part), 3 not supplied, **four gaps named, not closed**:
- **PG-1** §2.3 has no rows for "run started, checkpoints listed" (CE-1)
  and "declaration finding" (CE-2), which E-8 names.
- **PG-2** no §2.3 event for *run not started — no model selected* and its
  notice (F-2 (a) states the outcome).
- **PG-3** no statement of the loop's answer to a return input; the
  refusals *turn not active*, *run already ended*, *selection not
  established* exist only in PANEL §3.9.
- **PG-4** the replay request's form and answer, incl. events no longer
  held (E-6, F-12).
Owner DEL-05-01 (with DEL-05-02 for PG-3/PG-4); LOOP UNRESOLVED.

## 3. Prototypes (rerun 2026-09-30, Python 3.13.7, node v24.5.0, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` under the system temp folder)

| Prototype | Command (in its folder) | Result |
|---|---|---|
| HOSTING | `python3 run_cases.py` | 35/35 (one long-TMPDIR run gave `AF_UNIX path too long`; rerun with a short TMPDIR, 35/35) |
| ACT | `python3 -B validate_policy.py` | all expectations held |
| AS | `python3 -B validate_settings_in.py` | all expectations held |
| RS | `python3 -B run_prototype.py "$TMPDIR/b4-proto"` | 51 PASS, 0 FAIL |
| RS chain | `python3 -B exec_to_rs.py "$TMPDIR/exec-to-rs"` | 12/12 and 40/40 valid; 11 samples valid; none without a kind |
| EXEC | `python3 run_all.py` | ALL CHECKS HOLD, 0 failures: 20 MT case runs (new MT-18), 40 reports valid, 18 EV-3a readings as expected; examples unchanged |
| WD | `python3 wdproto.py selftest` | 62/62 (incl. `extract.mjs`) |
| LOOP | `assemble_tool_calls.py`; `destination_flow.py`; both `schema_subset.py` runs | 22/22; all expectations held (68 RS entries, 11 request records); VALID/INVALID as intended (exit 1 by design) |
| PANEL | `panel_double.py`; `schema_subset.py …` | 4/4; VALID/INVALID as intended |
| CA | `python3 -B prototype/run_w14_rehearsals.py --out …` | first rerun FAILED 1 (the W14 example pins EXEC `run_all.py`'s sha256, which node G changed); `--write-examples` regenerated both examples (diff: that one sha256 only); rerun ALL CHECKS HOLD |

The SH-1 chain was not rerun: C, P and ADAPTER did not change.

## 4. RELAY span check

`awk '/^## 0\./{f=1} /^## 4\./{f=0} f' RELAY_QUESTIONS_SWBPIPE.md | shasum -a 256`:
`6e399c8389dc2ad991ba8b64084fee17d44ef9e8137d184dd8eb599a66340d4d` before
and after (equal to the A1-E/A4 value). ANS `afb6e063…` and FACTS
`733fb88a…` unchanged.

## 5. GUIDE re-pin (last)

B8's `pins.py` copied unchanged from `$TMPDIR/c0/` (sha256
`b943319dc4a00bd79e79dde5c0a629e4026d56f099389ee7321cb2763f275423`). Run 1
(check): 8/18 (ACT, AS, RS, WD, WD-EX, EXEC, LOOP, PANEL, CA, RELAY
differed). Run 2 (`--write`): "match 8/18 (before write)". Run 3 (check,
final bytes): **rows 18; match 18/18**.

## 6. Changed files (sha256)

| File | sha256 |
|---|---|
| DEL-01-01 `OBS_1_0.158.0.md` | 7b984b541edca0b14534d29115e77642c587a32f830bdf25a94a7ecca882cc43 |
| DEL-02-01 `WORKFLOW_DECLARATION.md` | 517821d18fc958301d3adaeb63caf11ab50f7e1ca3ec5a644a3bb4ec78b25b0e |
| DEL-02-01 `EXAMPLES.md` | 275ea54d32cd8f487ec9a0f017aaa33b01ee43c79d7a675b53a7652c3519e2fd |
| DEL-02-03 `EXECUTION_COMPATIBILITY.md` | 64e732d502d0b91da00e62069be1b77b61d1e84986b3744bc117b6e67524fa38 |
| DEL-02-03 `prototype/required_tool_check.py` | d4503a184d3360fa4ab4f03b481f6f493c23f0cc281ab35e5cf07990fa32b6ef |
| DEL-02-03 `prototype/run_all.py` | 42c0b49606790d847b9f9d1d981446f53fbd7c1827422040a00939d98edeb5fc |
| DEL-02-03 `prototype/README.md` | 680d21691cf215f405e4a9d088a151b178cea60c123331fddc2acbc45196d98f |
| DEL-03-04 `HOST_INTEGRATION_GUIDE.md` | 5078aed9e22f82a3bbdd94af59a9204185ac109c917e52daddf8f6001fff4829 |
| DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` | 6fb6b9e883fa8d20da42c659de0485de0cb2a109a94c94364f16abde1dcc2b4a |
| DEL-04-02 `AUTONOMY_AND_STANDING_EXCHANGE.md` | d6f26801b0146800f685043b4c3e1fd208127f485379fc368194ec300249e42d |
| DEL-04-03 `RECORD_SEMANTICS.md` | c7f2eb15189d5fa5a3e235ba182419dd7d540876ba67169ad44332c78b80d067 |
| DEL-04-03 `RS_RECORD.schema.json` | b63a7e421b8858543c7bf58ba5e6c52cf3052a5d47cfd61f4eb0f498a8faa0bc |
| DEL-05-01 `LOOP_RECEIVING_CONTRACT.md` | 6cfcbcecdb98b33b41c47024719a60deb63d58560d6b5238930ecab674a0cacc |
| DEL-05-02 `PANEL_RECEIVING_CONTRACT.md` | 08229850140e0f1e7fceb85bdaabfec8f83f4956b2405368fa7d86912d3b5611 |
| DEL-09-06 `CONNECTED_ACTIVITY_CONTRACT.md` | 87f2923dc859611978d9311a6666fba80980ce47f912c9a00ff8d24141b48244 |
| DEL-09-06 `RELAY_QUESTIONS_SWBPIPE.md` | 0fe187b0edd1831d2ab2910b25890318a33118d51f93825898890294da33478d |
| DEL-09-06 `w14-result-record.example.valid.json` | c9d5c19830b45aa76fbe28f279b7a61a5ede7c9abdba1d128486f8799c91dc31 |
| DEL-09-06 `w14-result-record.example.invalid.json` | dd6e6ace452ea01dddb55e7967d8faafa377730c6d7965fd375eb6517cca47ed |
| `_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` | 3f39c129f22501203011347458c3f278e688570c6e1f2ae2178f74dcc5bd4552 |

Unchanged (checked by hash against the node's start): PIN_SPIKE, HOSTING,
C, P, ADAPTER, XT and their schemas/prototypes; ANS; FACTS. No ScopeOfWork,
register, status, basis, decomposition, scope-change or DAG file was
written.

## 7. Beyond the fence or returned (not done)

- **Stale pins, by design:** HOSTING, GUIDE and LOOP headers pin
  `OBS_1_0.158.0.md` at `85707703…` (pre-redaction; the OBS change note
  records it); RELAY's Basis line and CA pin HANDOFF at `92f6e45a…`.
- **Unredacted rollout name in run records** (outside the fence):
  `closeout/C1-B.md` and `reviews/V19-B.md` quote it.
- **EXEC §9.1** other "Current:" labels (C, ACT, RS, LOOP, HOSTING) still
  name Wave A versions; only the DEL-04-02 row was in G-3.
- **For DEL-01-01:** whether HCG-A07, HCG-A09 and image viewing (HCG-A11)
  have an availability signal (EXEC U-E10).
- **Joins:** WD HC-4 and WD-EX now match EXEC EV-3a; HOSTING §8.4 is cited
  unchanged.
- **Observed, not mine:** while this node ran, 14 `MEMORY.md` files,
  `RECEIPT.md` and `closeout/CLOSEOUT_ACCOUNT.md` were changed or created
  in the working tree by another writer (present before my first edit).
