# RP-3 — return (Type 2 TASK, 2026-09-30)

Repair node RP-3 of run `APP-V4-DESIGN-PASS-2-20260930`: WD and WD-EX (DEL-02-01) and HOSTING (DEL-01-01), with their schemas, examples and `prototype/` folders. Brief: `BRIEFS.md` (sha256 e3f98d1c8449…) "Common rules", "Wave B" common rules, "RP — repairs from V18", row RP-3. Binding: `R14_RESOLUTIONS.md` (c6a603303693…), with R13 (d0385313660e…), R12 and DECISION-K1. Inputs: the four comparison files (V18-1 fb07e07c66c1…, V18-2 0b00e79b161b…, V18-3 68a067e26af7…, V18-4 078113d7055b…), `WAVE_B/OBS-1.md` (622c86113a19…), `WAVE_B/OBS-1b.md` (5eb680de32e2…) and DEL-01-01's `OBS_1_0.158.0.md` (85707703e97b…, read only). No version bump: each change is a row in the file's Wave B change table. Not edited: `PIN_SPIKE_0.158.0.md`, `OBS_1_0.158.0.md`, `prototype/obs1/`. No network, no install, Codex not run, no git writes. The session was interrupted once by a connection error before any edit, and resumed.

## 1. Items: finding → fix → location

| Item | Done / returned | Fix and location |
|---|---|---|
| **R14-5** (V18-2 M-1, m-10) | Done; nothing returned | WD §4.2.5 gains the column "HOSTING §8.4 group at 0.158.0" for all ten names (A02, A03, A10, A08, A05, A06, A07, A11 ×2, A09), listing the group members each name does not rely on; new **HC-7** (group mapping); HC-4 reads presence through the mapping; HC-6 follows HOSTING for the three disputed members: `functionCallOutput` → HCG-A06 (`dynamic-tool-call`), `mcpServer/elicitation/request` → HCG-A07 (`person-input-request`), `thread/shellCommand` stays an App-origin client method in HCG-A02. None makes a WD name mean something its group does not offer, so nothing is returned. WD §4.2.1, §8 (joins and supplier rows), U-08, VC-50. HOSTING closes **F-27** citing WD §4.2.5 / HC-7; §8 receivers row and closing paragraph; §8.4 "Names" bullet, new paragraphs "Client methods in Part A" and "Members WD reads differently", meaning-table notes on A02, A05, A06, A07; new VC-31 |
| **R14-6** (V18-2 M-2; V18-4 m-8) | Done | `applied_receipt` → `applied` together in WD §3.6 (the rule now says WD follows the outcome owner, P-v0.8 `item_state`), schema `host_outcome` (enum and description), `workflow-declaration.valid.example.json`, `prototype/fixtures/E1d.declaration.json`, `prototype/wdproto.py` (L-WDEX-19c) and EXAMPLES (E1, E1d JSON). No `applied_receipt` remains in DEL-02-01 except change-table history |
| **R14-8 N-18** (V18-4 J10, m-8) | Done | WD cites P-v0.8's five contributions with sections and schema members: §4.3.6 (change-item content identity §3.1, §3.4, PM-6; resulting objects §9, "not supplied" → binding *unknown*), §4.3.7 (§4.1, §4.6 PT-1…PT-19, DS-4, §4.3 item-left events, explicit in P's schema per RP-2; P-state → item-state mapping), §8 supplier row (replaces "Current: P-v0.7") and joins row |
| **R13-6 in HOSTING** (V18-2 m-13; V18-3 m-20) | Done | New **§10.1** OB-1…OB-12 (dated, one pair, not qualification): `namespace` tool dropped on the local Responses route and the consequence (an App user on that route cannot use a host's MCP tools; CLI path not so limited); the command-line path (wrapped command, `source` agent → `unifiedExecStartup`, no deltas); order around the approval; `serverRequest/resolved` observed (U-09 narrowed); the approval-setting quirk (`untrusted` refused in config.toml, accepted on `thread/start`; no `decline` offered; `availableDecisions` without the opt-in); sandbox kept after approval; start-up traffic to chatgpt.com and github.com with analytics off and no sign-in, against U-18 and the start-up item left for the phase review (DECISIONS_PENDING Part 3, standing under DECISION-K1). Carried into §6.2.1, §6.3 R5, §6.8, §7.3, §8.1 L-2/L-3/L-4, §8.3, §10 list, F-30, new F-31, F-32, U-09, U-18, U-19, U-22, U-27, VC-12, VC-26; HCG-A05 availability signals add `namespaceTools` (inference, labelled). WD's `mcp-tool-call` row cites it |
| V18-3 m-17 | Done | HOSTING §4.3 step 4, §4.6 "observe lifecycle", failure table, LT-12 and LT-23 "Told to": DEL-02-03 (EXEC AE-6, AW-12) and DEL-03-03 (ADAPTER CT-9, CT-10, S-7, S-8) added |
| V18-2 m-2 | Done (WD side) | Schema: `if form = file then required path`; VO-5: a file output without `path` is not established, so a kind (b) checkpoint on it is not established (a separate FB-13 rule would never fire after VO-5, so none was added); new variant L-WDEX-42 (E9); VC-48 |
| V18-2 m-5 | Done (WD side) | §3.6 states WD's tokens as canonical and tabulates the one-to-one mapping to EXEC's and RS's spellings; notes that reports need the tool local name |
| V18-2 m-7 | Done | One wording, "prior act not counted" with its reason (RS L-13), in WD FA-1, I-8, §4.3.4, run end, VC-31, VC-32, VC-39 and WD-EX R-9b, R-12b, R-16, R-19 (v); history rows unchanged |
| V18-2 m-9 | Done (WD side) | Schema `$defs/workflow_identity` (origin `host`, nested `derived_from`, optional `revision_method`); fixtures `prototype/fixtures/workflow-identity.examples.json` (3 valid, 3 invalid) |
| V18-2 m-11 | Done | A15 named in WD §4.3.2 |
| V18-2 m-12 | Done (WD side, option b) | HC-6 takes HOSTING §6.1's wording (prompt authored by an MCP server or the agent) |
| V18-2 n-2 | Done | WD-EX E1e cites EXEC CH-32 |
| V18-1 m-13 (U-27) | Not this node's | RS's side; HOSTING U-27 only gains the OBS observation |

## 2. Prototypes rerun (2026-09-30; Python 3.13.7, node v24.5.0)

- Baseline before edits: `wdproto.py selftest` 54/54; `run_cases.py` TOTAL 35, FAIL 0.
- After: `PYTHONDONTWRITEBYTECODE=1 python3 wdproto.py selftest` (cwd DEL-02-01 `Design/prototype`): **62 checks, 62 passed, 0 failed**. S-1a/S-1c/S-2b/S-4 pass with `applied` (schema and fixtures changed together). New: L-WDEX-42 → output `not_established (FB-02)`, `CP-approve` `not_established (§3.4)`; S-10 identity instances 6/6 as expected (`host-supplied` → `/origin enum`; string derived-from → `/derived_from type`; no source root → `required`); S-11 reads HOSTING §8.4 (27 groups) and resolves all ten names, every cited supplier name a member of its group. S-11 was also shown to fail when `shell-command`'s group is altered to HCG-A03 (in-memory negative test).
- `python3 run_cases.py` (cwd DEL-01-01 `Design/prototype`): **TOTAL 35, pass (model) 35, FAIL 0**, including VC-27 (tables), VC-30 (capability account, after the §8.4 edits) and the three schema fixture checks. Output: `prototype/results/RUN_2026-09-30_RP-3.txt`. HOSTING's schemas are unchanged.

## 3. What other files must now say

- **EXEC (RP-1):** EV-3's presence rule reads WD HC-7's mapping and HOSTING §8.4 signals and route observations (R14-5); AW-1/AW-8/U-E26 "OBS-1 pending" cite HOSTING §10.1 OB-1 as the reason; m-1, m-3, m-4 (incl. EXEC §9.1 WD-v0.7 pin, fixtures "file writing"/"shell command"), m-5 mapping, m-12 ("requester not established" or follow WD); schemas may `$ref` WD `workflow_identity` and should type derived-from as a tuple.
- **ADAPTER (RP-1):** cite HOSTING §10.1 OB-1 (namespace limit), OB-2/OB-3 (source at start), OB-10 (OC-3), OB-6 (OC-5).
- **RS (RP-1):** origin `host`, source root required (V18-2 M-3); U-27's thread-scope reading (V18-1 m-13).
- **LOOP, PANEL (RP-4):** V18-2 m-6, m-7, m-8 (WD-v0.8 elements, FB-20…22, one wording).
- **P (RP-2):** nothing further for tokens; item-left events explicit (as WD now says).

## 4. Files (sha256, 12-char prefix)

| File | sha256 |
|---|---|
| DEL-02-01 `WORKFLOW_DECLARATION.md` | d45fba6a6aa5 |
| DEL-02-01 `EXAMPLES.md` | d0a9679705cb |
| DEL-02-01 `workflow-declaration.schema.json` | 2982a1878dba |
| DEL-02-01 `workflow-declaration.valid.example.json` | b484a5a2210a |
| DEL-02-01 `prototype/fixtures/E1d.declaration.json` | a73ee448bf9e |
| DEL-02-01 `prototype/fixtures/workflow-identity.examples.json` (new) | f9973a4cfbba |
| DEL-02-01 `prototype/wdproto.py` | 570269324bf2 |
| DEL-02-01 `prototype/README.md` | 4ed75405d199 |
| DEL-01-01 `HOSTING_BOUNDARY.md` | ce3034035f79 |
| DEL-01-01 `prototype/README.md` | 902163604f49 |
| DEL-01-01 `prototype/results/RUN_2026-09-30_RP-3.txt` (new) | aa53372de745 |
| `WAVE_B/RP-3.md` (this file) | computed by the integrator |

`git status --short`: among the changes, only the files above are this node's; the others (DEL-02-03, DEL-03-01, DEL-03-02, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, `WAVE_B/RP-2.md`) are the parallel nodes'. A stray output file this node wrote by mistake into the DEL-02-01 folder (`wd_run.txt`) was moved to scratch before return. `OBS_1_0.158.0.md`, `PIN_SPIKE_0.158.0.md` and `prototype/obs1/` are byte-unchanged (`git diff --quiet`).
