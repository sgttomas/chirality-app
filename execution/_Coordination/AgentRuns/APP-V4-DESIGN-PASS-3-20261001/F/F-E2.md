# F-E2 — GUIDE re-pinned last, and the run's citation check (design pass 3)

- Run `APP-V4-DESIGN-PASS-3-20261001`, node **F-E2**. Executor: Type 2 TASK
  (Claude Opus 5.5), dispatched by the HELP_HUMAN session; does not delegate.
  Written 2026-10-02 at HEAD `52af6fd86e` (branch
  `claude/chirality-app-v4-60-percent-a41fd5`).
- Brief: `BRIEFS.md` (sha256 `d6ce0247…77eb`) "Common rules", "F —
  first-increment edits", and the F-E2 paragraph of "RX … then F-E2"; the
  dispatch message (items 1–3). Binding read: R17…R20, `OWNER_DECISIONS.md`
  (`ea96c557…e015`; DECISION-K3 revised, DECISION-L), DECISION-3.
- **Boundary kept.** Files written: GUIDE (DEL-03-04
  `HOST_INTEGRATION_GUIDE.md`, → v0.6), two in-place items the brief names
  (ADAPTER's verification-case version list; WR §8's receivers), each with an
  "F-E2" change row, and this return file. No schema, example, prototype,
  ScopeOfWork, register, `_STATUS.md`, `OBS_*`, `PIN_SPIKE_*`, `generated/`,
  DAG or SWBPIPE file was edited. Read-only git; no network; no Codex or model
  run. Scratch: `…/scratchpad/fe2/` (scripts, outputs, a copy of GUIDE-v0.5).
  `git status --untracked-files=all` after the last edit shows only the three
  Design files modified (plus this file).
- GUIDE-v0.5 was read whole (1,083 lines, sha256 `5b87996d…9f08`, equal to
  F0's pin); the targets of every changed line were read in the cited file.

Paths are relative to `projects/chirality-app-v4/execution`. RUN =
`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001`.

## 1. Rows applied

| Row / item | File → version | What changed | Cited basis |
|---|---|---|---|
| **FG-01** (D6 J-13; F0 §1.12; §1.14 L58, L343) | GUIDE-v0.5 → **v0.6** | M8.6 rests on ROLE-v0.2 §3–§6 with HOSTING-v0.9 §8 S-6, §8.2, WD-v0.9 §5 and WR-v0.2 §16: the App's role is fixed per conversation and supplied once at its start; a workflow is supplied per run as run-start text (L-2; R19-1, R19-7). Open choices: role supply designed, not built; ROLE U-R3 (child-role carrier); OI-018 answered for the App by K-9, open for hosts. Row 8 summary, X-06, §4.2 row 8, CC-2, G-1 (role half) and the header follow. F0's note that D6 quoted a paraphrase was checked: G-1's text differs from D6's quote; the premise held | ROLE-v0.2 §3–§7 (O-4 offers DEL-03-04 §3–§6); HOSTING-v0.9 §8 S-6, §8.2 (FH-36, FH-37); RS-v0.9 R3, R5a; WD-v0.9 §5.2 (FW-11, FW-13) |
| **FG-02** (F0 gap G-2 as ruled by R18 G-2; D3 §R2.3: cite AAC-v0.2) | GUIDE-v0.6 | M5.3: App act control for App content **and A15**, designed in AAC-v0.2 (PROPOSED, not built); RC-4 (opened from an arrival only on the person's click, R18-5), RC-6, CAP-3 (capture evidence in AAC's format); AAC §0, §1.1, §1.2, §4.1, §4.2, §5.2, §6, §7; NIR §9 PD-5. Open choice: obligation proposed for SCA-V4-003 (SC2-01-04-1 as amended by SC3-01-04-1); placement OI-008 (AAC §6.2). X-1: fixtures still AWAITING INPUT for a candidate and the person; AE-2 and CH-23 (ii) DESIGNED on AAC's model (VC-AAC-04). L399 pointer refreshed; G-1 (act-control half) closed; row 5 summary | AAC-v0.2; EXEC-v0.7 FE-06, FE-08, FE-10, FE-11, FE-13 (§2.4.1, §2.5.2 AE-2, §5, §7.4); ACT-v0.9 FA-01, FA-02 |
| **FG-03** (D5 note; F0 §1.12; §1.14 L439–441, L771) | GUIDE-v0.6 | M8.2 (WR §2.2 ID-1, §4.1; host precedence: App side PROPOSED in WR SL-3, host open), M8.5 (WR §4.1–§4.4, §6 SQ-H; EXEC §6.5 HR-4), M8.7 and HC-8.6 (registration designed, not built; V4-EXM-14 cannot complete until built, CA-v0.7 §12.12; not against SWBPIPE, SQ-17) | WR-v0.2 §4, §6; EXEC-v0.7 FE-14…FE-18; CA-v0.7 FC-01; WD-v0.9 FW-04, FW-05 |
| Re-pin (item 1) | GUIDE-v0.6 | 25-row input table re-pinned last with B8's script; 7 new rows (RECOVERY, NPTD, NIR, AAC, ACCESS, WR, ROLE); version cells moved to the design-pass-3 labels; "Design pass 3 re-pin" paragraph; consumed-input line, column heading and §4.5 record it (§3 below) | Brief item 1 |
| Labels (pass-2 method, B8) | GUIDE-v0.6 | 190 sibling labels in live text moved (ACT, AS, RS, WD, WD-EX, LOOP, PANEL, HOSTING → v0.9; EXEC, ADAPTER, CA, XT → v0.7); C and P stay v0.8. History labels kept: CA-v0.3 (F-11), WD-v0.5 (G-11), LOOP/PANEL-v0.8 in §5's R16 row, the v0.5 and older Basis bullets and change tables | — |
| Lines whose cited text changed in pass 3 | GUIDE-v0.6 | M4.6 (RECOVERY §8.2 custody events via ADAPTER PI-6; HOSTING §10.2 OB2-2, OB2-3); M5.1 (A15 relations *reviewed draft* / *prior revision*, multi-entry, captured at the act control); M5.6 (RS R3's two App forms; *follows ⟨run⟩*; R13's two settlements); M5.8 (*the person* = DEF-4; no *observed end* in App runs; *follows* ≠ *continues*); M7.2 (LOOP NR-L1 host plan billing); M8.1 (declared-part value stays `WD-v0.8`, R20-7); M8.3 (`agent-delegation` signal, HCG-A08); M9.3 (delegation tools also dropped on the stock pairing, OB2-4); §2.11 (HOSTING row; new row for the pass-3 Design files); header model-access line (DEL-01-05's App side) | RS-v0.9 FR-01, FR-02, FR-06, FR-09, R19-2 row; ACT-v0.9 FA-03, FA-04; EXEC FE-01, FE-05; HOSTING FH-33, FH-41; LOOP CH-8; WD R20-7 row; ADAPTER FD-01 |
| Header, §0, §4–§6, UNRESOLVED | GUIDE-v0.6 | v0.6 Basis bullet (basis pins recomputed equal; DAG-003 currency; run records by sha256; OBS-2/OBS-3 named); "outside this undertaking (D1)" now DEL-07/08 only; Receivers line (DEP-03-04-010 joins; review status); "Changes from v0.5" table; CC-1…CC-11 rerun (CC-7 VER-007 rerun, report sha256 `72737740…3f58`, unchanged; CC-8 23/23); G-1 closed; §5 rows for R17…R20, K3, L; F-1, F-7, F-9, F-15, F-17 updated, F-19 added; UNRESOLVED: review row, SCA-V4-003 row, ROLE U-R3 row | — |
| ADAPTER verification-case versions (item 2) | ADAPTER-v0.7, in place | "current at this revision C-v0.8, P-v0.8, EXEC-v0.6 and WD-v0.8, with ACT-POLICY as then current" → "C-v0.8, P-v0.8, EXEC-v0.7, WD-v0.9 and ACT-POLICY-v0.9" (C and P were not stale: unchanged in pass 3). F-E2 row in "Changes from v0.6"; the "Not changed" note says it was corrected | F-E1 §2, §6 item 4 |
| WR §8 receivers (item 2) | WR-v0.2, in place | `library_entry` and `selection_record` no longer list DEL-02-04 as a receiver. Checked: R19-7 drops the row DEL-02-04 → DEL-02-02 and says DEL-02-04 composes role guidance only; WR §1 and §7's DEL-02-04 row ("Nothing flows for workflows") and ROLE §7.1 ("C-6 (DEL-02-02's registered revision) is withdrawn (R19-7)") agree. F-E2 row in "Changes from v0.1" | R19-7; WR §1, §7; ROLE §7.1, §7.3 |

Round-2 and RX items aimed at GUIDE: searched D1…D6 §R2.x and all F returns
for GUIDE / DEL-03-04 / M5.3 / M8.6. Only D3 §R2.3 FG-02 ("Cite AAC-v0.2
(label change only)") and F-A's pin note (pin the pass-3 files at their final
v0.2 bytes) exist; both applied. ACCOUNT-HOME-RECORD-v0.2, also named in
F-A's note, is not pinned: no GUIDE line relies on it beyond ACCESS, and the
brief's label list omits it (stated in GUIDE's re-pin paragraph and F-1).

## 2. Not applied, returned

| Item | Why | To |
|---|---|---|
| WR schema `workspace-registration.schema.json`: the `selection_record` description still says it is handed to "DEL-02-04 (workflow supply, R17-8)" | Same stale receiver as WR §8, but the schema is outside F-E2's fence (only WR §8 named) | DEL-02-02 / integrator |
| Label lags in other files (§4.3 below) | The cited sections and identifiers exist in the current files; only GUIDE is fixed here | Each file's owner |
| HOSTING l.14 and l.1195: "S-1 RECOVERY-v0.2 §1 (receiving comparison)" | RECOVERY has no section titled so; its S-1 receiving is §1's reconciliation with HOSTING §6.5 (closing U-14, F-01) plus §4.2's consumed DEL-01-01 row. Imprecise, not wrong | DEL-01-01 |
| HOSTING l.765: "(NIR-v0.2 §4.3 DM-1…DM-6, §6.2.1 RT-08)" | §6.2.1 RT-08 is HOSTING's own register transition, but reads as NIR's (NIR has no §6.2.1) | DEL-01-01 |
| ACT §2.6 and FA-01 say "until SCA-V4-003 carries SC2-01-04-1"; EXEC, AAC and D3 name the amended item SC3-01-04-1 | SC3-01-04-1 amends SC2-01-04-1 (D3 §SCA); naming differs, meaning agrees. GUIDE writes "SC2-01-04-1 as amended by SC3-01-04-1" | DEL-04-01 / SCA-V4-003 node |

## 3. Pin table (item 1)

Script: B8's `pins.py` (sha256
`b943319dc4a00bd79e79dde5c0a629e4026d56f099389ee7321cb2763f275423`, found
unchanged at `$TMPDIR/b8/pins.py` and `$TMPDIR/c0/pins.py`), used as is. It
parses the rows `  | **Short** | ver | `File` | sha |`, resolves each basename
to exactly one path under the execution root (excluding `_Coordination`) and
compares or writes `shasum -a 256`. New rows were inserted with a 64-zero
placeholder before the write.

- Run 1 (check, after GUIDE's text edits): **6/25** match (C, P, SPIKE,
  RELAY, ANS, FACTS).
- Run 2: `--write` ("match 6/25 (before write)").
- Run 3 (check, final GUIDE bytes, after the last GUIDE edit): **25/25**.

| Short | Label | File | sha256 (pinned = current) | Against RV20 |
|---|---|---|---|---|
| C | C-v0.8 | `CATALOG_AND_READ_BASIS.md` | `eae7369fc0109f4c4238308ef2cde7a189d83bd0669a78f01b9800d5a30ddf90` | unchanged |
| P | P-v0.8 | `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | `f432356d054cb784ded51325de25ef945ddf29e9843cc187e3576841bac6533f` | unchanged |
| ADAPTER | ADAPTER-v0.7 | `ADAPTER_ENABLEMENT_AND_RECEIVING.md` | `71a397d918319ff884141d7849c342adae73251dd317377ea8cc3825157a8992` | changed (was `7cad04c873c0…`) |
| ACT | ACT-POLICY-v0.9 | `ACT_AND_POLICY_CONTRACT.md` | `3d9f3ee2c9e1683944afa20409b904bd5a0bcd04ce419c170867a778b3c5fd57` | changed (was `6fb6b9e883fa…`) |
| AS | AS-v0.9 | `AUTONOMY_AND_STANDING_EXCHANGE.md` | `dc3fd0b68406fc0fa329b94d3bf3e82d3268584629d97d58f1b568265cbbc5e0` | changed (was `d6f26801b014…`) |
| RS | RS-v0.9 | `RECORD_SEMANTICS.md` | `6c6408d8c10a9a7e5aea0c6a5fe91e30374cf99ef9f919983cdafafb3818739f` | changed (was `b25cc90e9e25…`) |
| WD | WD-v0.9 | `WORKFLOW_DECLARATION.md` | `b1a647290b966f1bb97697ad435650ba76e29cfd3fd39ee160e58cf076742e9f` | changed (was `517821d18fc9…`) |
| WD-EX | WD-EX-v0.9 | `EXAMPLES.md` | `50efea247c08abb0e6816dface33bbe67e59b70658d7b458b079ff7d83b73c7d` | changed (was `275ea54d32cd…`) |
| EXEC | EXEC-v0.7 | `EXECUTION_COMPATIBILITY.md` | `8337b1d594292d16d93785263cb38462c34f54eb47443ea5566e2b9dff49bc2a` | changed (was `64e732d502d0…`) |
| LOOP | LOOP-v0.9 | `LOOP_RECEIVING_CONTRACT.md` | `d47d2249eb5f863aea640f582893b6861fc5a019d600412de7f3ac2e58cc429a` | changed (was `f8b7776c8261…`) |
| PANEL | PANEL-v0.9 | `PANEL_RECEIVING_CONTRACT.md` | `4898b6f80832b3baae9fd7e2e24e2fe6141a0d2b12359f1c0dce5647ccee6999` | changed (was `70d9a23ed45d…`) |
| HOSTING | HOSTING-BOUNDARY-v0.9 | `HOSTING_BOUNDARY.md` | `a4619e33f83886cbf98a6fd632ab2281454c38bb1a693649f979b8490e0f51a6` | changed (was `3cf0381c4235…`) |
| SPIKE | PIN-SPIKE-v0.1 | `PIN_SPIKE_0.158.0.md` | `0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115` | unchanged |
| CA | CA-v0.7 | `CONNECTED_ACTIVITY_CONTRACT.md` | `148687e71fd8a464952b096e868e9f7615a3d6e849b8ecc050744746a3811b5a` | changed (was `58167f7accaf…`) |
| RELAY | RELAY-v0.3 | `RELAY_QUESTIONS_SWBPIPE.md` | `71ac39b4ece59ec8fda564d9148d56c32f6ed75c78c1127e4a9cbba3d5c4dad3` | unchanged |
| XT | XT-v0.7 | `EXTERNAL_TRACE_CASES.md` | `d973677bab5abdc03b170e10c0ad52a1135cc8dd5ad24afc7886271c97e7f456` | changed (was `daf6c9c946ec…`) |
| ANS | SWBPIPE answers | `RELAY_ANSWERS_SWBPIPE.md` | `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74` | unchanged |
| FACTS | SWBPIPE fact sheet | `FACTS_SQ01_SQ32.md` | `733fb88a701317be8f0054937eca058774ba5f5f30c7a27233718996e8b2ab7e` | unchanged |
| RECOVERY | RECOVERY-v0.2 | `EXECUTION_AND_RECOVERY.md` | `c528b47627ea116c1b56eaf9399e967fbcd247653189aa31d3771d4b7994dde1` | new row |
| NPTD | NPTD-v0.2 | `NATIVE_PLANS_TOOLS_DELEGATION.md` | `5cfda3ac81b3d202b28435554ebff7262e4c4ebb1478d6a8b69cb54d0b71396b` | new row |
| NIR | NIR-v0.2 | `NATIVE_INTERACTION_RECEIVING.md` | `d56830e7274be4d2fb814b7d93b405f9b4093f59626c0533d2d5a818bb2b2f2f` | new row |
| AAC | AAC-v0.2 | `APP_ACT_CONTROL.md` | `38cb681ec435312b1c5111dc1ec993abc5c537d3ec35179238450cf3a0bf31df` | new row |
| ACCESS | ACCESS-v0.2 | `ACCOUNT_AND_PROVIDER_ACCESS.md` | `8cc7a60f755070c297f28e5a34ff37965654daeff529aa6c5f6b77fba14ee9cf` | new row |
| WR | WR-v0.2 | `WORKSPACE_AND_REGISTRATION.md` | `8df3a942e7f0132d5a8f7a6be52529b1fdc3515274788b4ff7ad6be7c03eb82d` | new row (bytes after F-E2's §8 edit) |
| ROLE | ROLE-v0.2 | `ROLE_SUPPLY.md` | `45a748697cf8fca8625a6927417647a30f90e60e0c3020f93fd22bcfc4cd2f3a` | new row |

Every pinned file except ADAPTER and WR is byte-equal to its committed state
at HEAD `52af6fd86e` (`git status` shows no other change); ADAPTER and WR
include F-E2's own in-place edits (before them: ADAPTER `9b9a4319…`, as
F-E1 reported; WR `f1ca71b9…`, as committed by RX2).

**Basis pins recomputed** (v0.6 Basis bullet): PRD `bb6e786f…`,
ARCHITECTURE `317d5789…`, HOST_INTEGRATION `d4331c39…`, EXAMINATION
`471798bc…`, ScopeOfWork `895f004e…`, Dependencies.csv `977d8712…`,
`_REFERENCES.md` `1279ea22…`, `_DAG/_LATEST.md` `4d381ba4…`: all equal to
v0.5's. Run records pinned in full in that bullet (OWNER_DECISIONS,
R17…R20, BRIEFS, F0) and by prefix (D3, D5, D6, F-A…F-E1, RX); OBS-2
`61cc34ff…`, OBS-3 `554ac445…`, OBS-1 `7b984b54…` (unchanged).

## 4. Citation check (item 2)

### 4.1 Method

- **Scope.** Every line added or changed since the run base `a38617d08b`
  (`git diff -U0 a38617d08b`, the `+` lines) in the 20 Design files the run
  touched (HOSTING, RECOVERY, NPTD, AAC, NIR, ACCESS, ACCOUNT-HOME-RECORD,
  WD-EX, WD, WR, EXEC, ROLE, ADAPTER, ACT, AS, RS, LOOP, PANEL, CA, XT), and
  GUIDE after F-E2. This over-includes (a changed long line counts whole)
  and covers the change tables, so it covers F-E1 §5's list and every other
  node's.
- **Checker.** B8's `cite.py` / `cite2.py` logic (found at `$TMPDIR/b8/`,
  sha256 `3af3b96c…`, `47cf4f7c…`), with the short-name map extended to the
  pass-3 files and label aliases (HOSTING-BOUNDARY, ACT-POLICY, PIN-SPIKE),
  and the `Contribution:` parse made to accept `**Contribution:**`. A § must
  match a heading of the cited file; an ID must occur as a token in it; a
  label older than the cited file's current label is a "lag". Self-citations
  skipped. Scripts in scratch: `runcite.py` (strict), `runcite2.py` (broad),
  `meaning.py` (meaning table), `paths.py`, `cite.py`.
- **Meaning.** For the 605 citations from the first-increment files into the
  eight pass-3 Design files (144 distinct sections/IDs), `meaning.py` printed
  each target's heading or defining row beside every citing context; I read
  all of them. Spot greps (`where.py`) confirmed the section an ID sits in
  where a citation pairs them (e.g. NPTD §5.2 RV-1, RECOVERY §4.1 tag,
  WR §16.2 TX-5, §16.5 PR-5/FN-3, ROLE §4.2 GS-7, NIR §4.3 DM-6, AAC §1.1 AK-a,
  ACCESS §6 Q-1, RECOVERY §5 SQ-R R-2, HOSTING §10.2 OB2-2…OB2-4, LOOP §13
  NR-L1). GUIDE's own new citations were checked the same way while writing.

### 4.2 Results

| File | Added/changed lines | Cross-file items (strict) | Missing | Label lags |
|---|---|---|---|---|
| HOSTING | 561 | 186 | 0 (1 parse artefact: "ACCESS-v0.2 §3 and ROLE-v0.2") | 2 |
| RECOVERY | 881 | 93 | 0 | 0 |
| NPTD | 783 | 32 | 0 | 1 |
| AAC | 368 | 60 | 0 | 6 |
| NIR | 828 | 114 | 0 | 3 |
| ACCESS | 1,046 | 49 | 0 | 2 |
| ACCOUNT-HOME-RECORD | 161 | 18 | 0 | 0 |
| WD-EX | 43 | 32 | 0 | 0 |
| WD | 181 | 124 | 0 | 3 |
| WR | 590 | 118 | 0 | 0 |
| EXEC | 305 | 198 | 0 | 4 |
| ROLE | 565 | 28 | 0 | 1 |
| ADAPTER | 92 | 37 | 0 | 0 |
| ACT | 51 | 49 | 0 | 0 |
| AS | 29 | 9 | 0 | 0 |
| RS | 161 | 108 | 0 | 2 |
| LOOP | 59 | 17 | 0 | 0 |
| PANEL | 20 | 13 | 0 | 0 |
| CA | 85 | 62 | 0 | 2 |
| XT | 18 | 12 | 0 | 0 |
| **20 files** | | **1,360** (1,357 before F-E2's edits) | **0** | **26** |
| GUIDE-v0.6 (changed lines) | 194 | 814 | 0 | 1 (the v0.5 Basis history bullet) |

- **Broad pass** (every § and ID up to the next `;`, `|` or short name): 1,650
  items (1,648 before F-E2's edits), 46 flagged, all read by hand: each is
  an identifier of the citing file or of another source that follows a
  cross-file citation in the same clause (e.g. HOSTING's own §6.2.1, §8.2,
  §9.1; EXEC's RE-6/RE-7/RC-5; ACT's V-01; WR's LS-8/RB-4a; node labels F-B,
  F-C; "S1-C"). None is a missing section or identifier.
- **Whole GUIDE** (B8 strict, §0 onward): 1,172 citations, 1,169 resolved;
  the 3 misses are the placeholders "ACT RC-n", "ANS SQ-nn" and GUIDE's own
  F-18 in §5 (as at v0.5). Labels differing from current: 4, all history
  (CA-v0.3 F-11; WD-v0.5 G-11; LOOP/PANEL-v0.8 in §5's R16 row). Broad pass:
  1,599 items, 21 flags, all attribution noise (the 15 of v0.5 plus six in
  G-1's new cell: M8.6, M5.3, SC2/SC3-01-04-1, SCA-V4-003 after "ROLE-v0.2
  §3–§6").

### 4.3 Mismatches

| # | Where | Mismatch | Disposition |
|---|---|---|---|
| 1 | GUIDE-v0.5 (FG-01…FG-03; §1.14 L58, L343, L399, L439–441, L771) | DEL-01-04, DEL-02-02, DEL-02-04 "outside undertaking (D1)", "no Design file", "offers nothing yet" | **Fixed** (GUIDE-v0.6) |
| 2 | GUIDE-v0.5 M5.1 | A15 "recorded with *derived from ⟨draft⟩*": RS-v0.9 FR-06 removed `derivedFrom` from act records (now *reviewed draft*, *prior revision*) | **Fixed** |
| 3 | GUIDE-v0.5 M5.8 | `run_ended` *the person* / *observed end* read without RECOVERY DEF-4 (EXEC FE-01) | **Fixed** |
| 4 | GUIDE-v0.5, 164 stale labels (v0.6/v0.8 siblings) | Label lag | **Fixed** (190 moves; 4 history labels kept) |
| 5 | ADAPTER-v0.7 Verification cases | "current" EXEC-v0.6, WD-v0.8, "ACT-POLICY as then current" (C-v0.8, P-v0.8 were current) | **Fixed** in place (F-E2 row) |
| 6 | WR-v0.2 §8 | DEL-02-04 listed as receiver of `library_entry`, `selection_record` against R19-7 | **Fixed** in place (F-E2 row) |
| 7 | WR `workspace-registration.schema.json` `selection_record` description | Still "DEL-02-04 (workflow supply, R17-8)" | **Left** — outside fence; DEL-02-02 |
| 8 | HOSTING l.14, l.1195 | "S-1 RECOVERY-v0.2 §1 (receiving comparison)": no such-titled part; S-1 receiving is §1's §6.5 reconciliation and §4.2 | **Left** — DEL-01-01 (wording) |
| 9 | HOSTING l.765 | "NIR-v0.2 §4.3 DM-1…DM-6, §6.2.1 RT-08" reads §6.2.1 as NIR's; it is HOSTING's | **Left** — DEL-01-01 (wording) |
| 10 | ACT §2.6 / FA-01 vs EXEC, AAC | "SC2-01-04-1" vs "SC3-01-04-1" (the amended item) | **Left** — DEL-04-01 / SCA-V4-003 (naming) |
| 11 | Body label lags (section present in current file) | AAC l.84, l.111, l.165 (WR-v0.1 §4.3, §5.2, RB-4, SQ-G); NIR l.130 (ACT-POLICY-v0.8 §2.1), l.187, l.573 (WR-v0.1 §5.1, §8); EXEC l.565, l.1258, l.1472 (LOOP-v0.8 §2.3 E-8; LOOP stepped after EXEC); RS l.318, l.329 (LOOP-v0.8 §3.1, §5.2, §5.3); ROLE l.64 (WD-v0.8 §5.1); CA l.717 (RS-v0.8 L-13; EXEC-v0.6 CH-31); ACCESS l.891 (HOSTING-v0.8 §8 S-4); HOSTING l.1019 (EXEC-v0.5 §2.3 HP-2), l.1467 (WD-v0.8 §4.2.5, deliberately the v0.8 group set) | **Left** — each owner; no meaning change found |
| 12 | Header/input-line lags (name the version read) | NPTD l.5 (ROLE-v0.1), AAC l.19, l.20, l.63 (EXEC-v0.6, ACT-POLICY-v0.8), ACCESS l.62 (RS-v0.8 "were read"), WD l.1618 (history), EXEC l.2165 (closed-at-v0.3 history) | Not mismatches (record what was read) |

No citation in the run names a section or identifier that is missing from
the cited file, and in the 605 first-increment → pass-3 citations read for
meaning none cites a section for a different meaning than the section has,
beyond rows 8–10.

## 5. DAG-003 (item 3)

Run 2026-10-02 from the repository root at HEAD `52af6fd86e` (working tree:
the three F-E2 edits only):

| Check | Result |
|---|---|
| `shasum -a 256 -c MANIFEST.sha256` (in `_DAG/DAG-003/`) | exit 0; 37/37 OK |
| `shasum -a 256 -c _DAG/DAG-003/SOURCE_MANIFEST.sha256` (from the execution root, where its paths resolve) | exit 0; 130/130 OK |
| `python3 tools/coordination/analyze_dep_closure.py projects/chirality-app-v4/execution --scope ALL --filter-active-only true --normalize-ids true --dependency-class EXECUTION --target-type DELIVERABLE --hub-threshold 20 --max-cycles 200 --include-declared true` | exit 0; `run_status` COMPLETE; **`accepted_dag.result` NO_DEPARTURE_FOUND** (version DAG-003; added/removed arcs and deliverables none; `dag_pending_count` 0); 41 nodes, 202 edges, 6 SCCs, issues none, `declared_disagreement_count` 0. Output sha256 `c6121d5a…bc03b` (scratch) |

No register or ScopeOfWork changed in this run, so DAG-003 stays current.

## 6. Other checks run

| What | Command | Result |
|---|---|---|
| VER-007 (GUIDE CC-7) | `python3 tools/scope_of_work/check_boundary_owner_resolution.py --json ‹scratch› ‹DEL-03-04 ScopeOfWork.md›` | exit 0; 1 boundary requirement checked, 0 citing no claim, 0 failing; report sha256 `72737740…3f58` (= RV-3, B8) |
| WR prototype (after §8 edit) | `python3 -B wrproto.py` (DEL-02-02 `Design/prototype/`) | exit 0; 98 checks, 98 passed |
| SH-1 then ADAPTER (after the verification-case edit) | `python3 -B run_fixture.py --out ‹scratch›` (DEL-03-01); `python3 -B observe_map.py --run ‹scratch›` (DEL-03-03) | exit 0, 22 of 22; exit 0, "Records: 34 dispatch, 11 checkpoint observations, 14 channel statuses … RESULT: all checks passed" |
| GUIDE | no prototype (as RX found) | — |

`git status --untracked-files=all` after the runs: no new file outside this
return; the prototypes wrote only to scratch.

## 7. New sha256 (after the last edit)

| File | Version | Before | After |
|---|---|---|---|
| `PKG-03…/DEL-03-04…/Design/HOST_INTEGRATION_GUIDE.md` | GUIDE-v0.6 (1,145 lines) | `5b87996d9c16d5d27b9fe2d3d2c37a0856baf9fa9624ccfe8a10670830549f08` | `15e43dc1aeeba1f4e10621c59b8186aa1c1407c52c418aebef72a1fd95fd3644` |
| `PKG-03…/DEL-03-03…/Design/ADAPTER_ENABLEMENT_AND_RECEIVING.md` | ADAPTER-v0.7, in place | `9b9a4319d2db1156cb28a837591740fbf2fcf4253fb377f779383cfb50163f0d` | `71a397d918319ff884141d7849c342adae73251dd317377ea8cc3825157a8992` |
| `PKG-02…/DEL-02-02…/Design/WORKSPACE_AND_REGISTRATION.md` | WR-v0.2, in place | `f1ca71b92bdc5e26…` | `8df3a942e7f0132d5a8f7a6be52529b1fdc3515274788b4ff7ad6be7c03eb82d` |
| `RUN/F/F-E2.md` (this file) | — | — | reported in the hand-back |

GUIDE pins ADAPTER and WR at their "after" bytes (25/25 rechecked after
GUIDE's last edit).

## 8. For the integrator

1. WR's schema description of `selection_record` (DEL-02-04, R17-8): one
   word-level fix, outside this fence (§4.3 row 7).
2. Label lags (§4.3 row 11) and the two HOSTING wordings (rows 8, 9): owners'
   choice; none changes a meaning.
3. GUIDE-v0.6 asks for its independent review with the design-pass-3
   candidate (GUIDE F-9; UNRESOLVED).
4. Scratch scripts (not in the repository; sha256): `pins.py` `b943319d…`
   (B8's, unchanged), `cite.py` `17b234d2…` (B8's, map and parse adapted),
   `cite2.py` `47cf4f7c…` (B8's), `paths.py` `741f7058…`, `runcite.py`
   `340e1170…`, `runcite2.py` `d5e5d9b6…`, `meaning.py` `e55ee916…`, the
   GUIDE edit `g6.py` `7d2b55d4…`.

---

## RP-final — after repairs RV21-A and RV21-B

Node **RP-final** (HELP_HUMAN's message to F-E2, 2026-10-02), at HEAD
`31d65b0be3` (RV21-A on RV21-B on `6185de63da`). Read first: `F/RV21-A.md`
and `F/RV21-B.md`. Fence: GUIDE (pins and labels), DEL-09-06 CA (examples,
change row, l.717), DEL-04-03 RS act-log example record 4. Read-only git; no
network; no Codex or model run. Scratch: `…/scratchpad/fe2/rp/`.

### What changed

| Item | File | Change | Check |
|---|---|---|---|
| CA examples | `w14-result-record.example.valid.json`, `.invalid.json` (DEL-09-06) | Regenerated with `PYTHONDONTWRITEBYTECODE=1 python3 -B prototype/run_w14_rehearsals.py --out ‹scratch› --write-examples` at 21:49 UTC. Before: exit 1, 43 passed, 1 failed ("valid example … equals the regenerated W14-05 record"), as RV21-B §3 item 1 said. A field-by-field comparison of the valid example before and after shows one difference: `/subject_of_run/files/4/sha256` `b770bb42…` → `3fc0d650…` (DEL-02-03 `prototype/run_all.py`, changed by RV21-B for R21-1); the invalid example is derived from it | `--write-examples` run: exit 0, "ALL CHECKS HOLD"; rerun without it (also after the CA text edits): exit 0, 44 passed, "ALL CHECKS HOLD: 0 failure(s)" |
| CA l.717 (F-E2 §4.3 row 11, left with DEL-09-06) | `CONNECTED_ACTIVITY_CONTRACT.md` §8.2 W14-05 | "(RS-v0.8 L-13): EXEC-v0.6 **CH-31**" → "(RS-v0.9 L-13): EXEC-v0.7 **CH-31**"; "(EXEC-v0.6 CH-32)" → "(EXEC-v0.7 CH-32)". Kept as provenance: "CH-32 (v0.6)" and "from EXEC-v0.6, CH-31 here" | RS-v0.9 L-13 and EXEC-v0.7 CH-31, CH-32 present with the cited meanings (L-13 "Earlier acts"; CH-31 "Earlier act not counted"; CH-32 "Checking, approval and reliance kept apart") |
| CA §8.5 note and change table | same | "**Regenerated at RP-final** …" paragraph after RX's; "RP-final" row after the RX row of "Changes from v0.6". No rule, case, outcome or identifier changed | — |
| RS act-log record 4 | `RS_RECORD.valid.act-log.example.jsonl` (DEL-04-03) | Record 4 (`rec:app:acts:0004`) is the L-4 multi-entry act (`relations.registeredEntries`, two entries, `entry:` strings, `cap:reg-in-place-2`): purpose "make it available in the project library" → "make them available in the project library", as WR ME-3, RS §6.2 (l.573) and AAC's multi-entry examples say. Records 1–3 unchanged. RECORD_SEMANTICS.md is not edited (it already states the plural form), so no RS change-table row | `run_prototype.py ‹scratch›`: exit 0, 63 PASS, 0 FAIL, "RESULT: all expectations held". Consumer check: DEL-01-04 `run_cases.py` (K-17b reads record 4): exit 0, 151 checks, 0 failed |
| GUIDE labels | `HOST_INTEGRATION_GUIDE.md` | No sibling version label changed in RV21 (in place, no steps); GUIDE's strict citation check still shows only the 4 history labels. RELAY's row: "unchanged in design pass 3" was no longer true (RV21-B added next-relay item (6)); the version cell now says so | B8 `cite.py`: 1,176 citations, 1,173 resolved; the 3 misses are the v0.5 placeholders |
| GUIDE pins | same | Consumed-input line (re-pinned last at RP-final; F-E2 kept as the earlier re-pin), column heading "sha256 at node RP-final", "RP-final re-pin" paragraph, §4.5 sentence, "RP-final" row in "Changes from v0.5", and an "At RP-final" sentence in F-19 | below |

### Pin check (B8's `pins.py`, sha256 `b943319d…5423`, unchanged)

- Before the write: **11/25** (unchanged: C, P, ADAPTER, AS, LOOP, PANEL,
  SPIKE, XT, ANS, FACTS, ROLE). The 14 that differed: ACT, RS, WD, WD-EX,
  EXEC, HOSTING, RELAY (RV21-B); RECOVERY, NPTD, NIR, AAC, ACCESS, WR (RV21-A);
  CA (RP-final).
- `--write`, then check after GUIDE's last edit: **25/25**.

| Short | New pin (sha256) |
|---|---|
| ACT | `4ef8c0428d42fbe37be634d79296d7ec80860308345bf4826650fef1739b2229` |
| RS | `d3db9b97ab1d90bf222bda5bdfc16fb2e2f0514c89891dcedfa52d0bd8a62a98` |
| WD | `1abe72e3f546676cd73308f9d349ad164462a3bd9bf6114ed0a8874be0664e18` |
| WD-EX | `85fa5a3f9200cef893789165515eafe8aff653f6357135cf7575c6eacd83a361` |
| EXEC | `fa8226c60417fb8c011a67111f1e0fb13338230ac384805addefcfcf6e9033b5` |
| HOSTING | `bcad280f204172385367f21f5cbf7c978da1a1984ccce28f5b8240174c2d8301` |
| CA | `7ff38bf0d08c23f52822bdd154b08b1a7eb8fa6893ac0837917808eaceef99c5` |
| RELAY | `6e726be9ae39e8a8b5ec39b38984081339bac5bee52ce88fc8739a298801ae92` |
| RECOVERY | `678042beae0327e6fcbabb99eaea746d46c843198238ac4dfc67690ea26149c1` |
| NPTD | `6eed39dcee4acf4b8b986cdd9e09c460a8fa53571973cb5c826acce37d644a72` |
| NIR | `7144aebd4a72522d156ea6bae21db78da9343565d68f3f5688a46b35a2f50576` |
| AAC | `062ce28c8a4ec0bc79fc6b6c421245057a59815df14b88fa779b61eeb98be7d7` |
| ACCESS | `929bd07b32f40fc6f65b6df6ce5b7aebe6cd91a89866525a981e5cbe11c4ffa0` |
| WR | `5b522ce626dcaadd73e5abb46b9db1303d45a9cf2307feface5920d831d056dd` |

Every new pin except CA equals the "after" value RV21-A §4 or RV21-B §4
reports (and the committed bytes at `31d65b0be3`); CA's is RP-final's.

### Citation check on the repaired lines

Same scripts as §4 (base made a parameter, `CITE_BASE`), over every `+` line
of `git diff -U0 ‹base›` in the 15 Design files changed since `6185de63da`
(HOSTING, RECOVERY, NPTD, AAC, NIR, ACCESS, WD-EX, WD, WR, EXEC, GUIDE, ACT,
RS, CA, RELAY), working tree after RP-final:

| Base | Strict items | Missing | Label lags |
|---|---|---|---|
| `6185de63da` (RV21-B + RV21-A + RP-final) | 207 | 0 | 2 |
| `dc61150559` (RV21-A + RP-final) | 73 | 0 | 0 |

- The two lags are provenance, not errors: HOSTING l.111 (the RV21 row
  quoting "the group set WD-v0.8 §4.2.5", kept deliberately) and RELAY
  l.1141 (item (5), "XT-v0.6 IN-30, F-26; added at node G", unchanged text on
  the line RV21-B extended; IN-30 and F-26 are present in XT-v0.7).
- Broad pass: 282 items, 19 flags, all read: each is an identifier of the
  citing file after a cross-file citation (HOSTING's own §6.1, §6.2.1, §6.5,
  §6.7, §8.2, §8.4; NIR's own TC-2, RN-2, VC-NIR-23, AT-9, AT-10; WR's RB-4a;
  AAC's §1.2 in ACT). None missing.
- Meaning: the 129 distinct cross-file targets were printed beside their
  citing lines (`rp/meaning.txt`) and read. All agree, including the RV21
  re-pointings (RECOVERY-v0.2 §1 "reconciliation with §6.5" and §4.2;
  "this file's §6.2.1 RT-08"; NPTD-v0.2 §6.4 and §9 TA-5; ACCESS-v0.2 CS-18
  and Q-11 with RECOVERY §4.1 and ROLE §5.5; WR §4.7 ME-3 with AAC §1.2,
  §4.2; LOOP-v0.9 §13 NR-L1 and ACCESS §11 CH-8 in RELAY item (6)).
- Remaining label lags since the run base (a38617d08b), all with the cited
  section present: AAC l.85 (WR-v0.1), NIR l.131 (ACT-POLICY-v0.8), l.188,
  l.600 (WR-v0.1), ROLE l.64 (WD-v0.8), ACCESS l.898 (HOSTING-v0.8); the
  rest are header "read at" lines or history. Left with their owners, as
  GUIDE F-19 now records. Closed since F-E2: WR schema description (RV21-A),
  HOSTING S-1 and §6.2.1 wordings, ACT's SC naming, EXEC/RS/HOSTING label
  lags (RV21-B), CA l.717 (here).

### DAG-003 currency (rerun after RP-final's edits)

| Check | Result |
|---|---|
| `shasum -a 256 -c MANIFEST.sha256` (in `_DAG/DAG-003/`) | exit 0; 37/37 OK |
| `shasum -a 256 -c _DAG/DAG-003/SOURCE_MANIFEST.sha256` (execution root) | exit 0; 130/130 OK |
| `analyze_dep_closure.py` (the brief's arguments, from the repository root) | exit 0; `run_status` COMPLETE; **`accepted_dag.result` NO_DEPARTURE_FOUND** (DAG-003; `dag_pending_count` 0); 41 nodes, 202 edges, 6 SCCs; issues none; output sha256 `c6121d5a…` (identical to F-E2's run) |

### New sha256 (RP-final)

| File | Before (HEAD `31d65b0be3`) | After |
|---|---|---|
| DEL-03-04 `HOST_INTEGRATION_GUIDE.md` (GUIDE-v0.6) | `017849e4790b5ed9…` | `4ab688f95e5bf9dd41fe2538e7d450f4ecc50bdecfe0e3deb8562d6f1e70a0e2` |
| DEL-09-06 `CONNECTED_ACTIVITY_CONTRACT.md` (CA-v0.7) | `148687e71fd8a464…` | `7ff38bf0d08c23f52822bdd154b08b1a7eb8fa6893ac0837917808eaceef99c5` |
| DEL-09-06 `w14-result-record.example.valid.json` | `1997107397a444b4…` | `a14c5934cd47d74e6665857d66f4e485b29ca8ba7b7c37be54579971cbfb432b` |
| DEL-09-06 `w14-result-record.example.invalid.json` | `0c28e970792b7a45…` | `1a1eacac7b8177691c127d3a6abf7a8056195b4e437d86b7b7ac806d2a675fb0` |
| DEL-04-03 `RS_RECORD.valid.act-log.example.jsonl` | `b202e850d7a966a8…` | `5b34591e25051486102681083fbe1e1e59d890dcbcc28f0ccccad585651a4e51` |
| `RUN/F/F-E2.md` (this file) | — | reported in the hand-back |

`git status --untracked-files=all` after RP-final: only these five files and
this one modified; prototype runs wrote to scratch only.
