# C1 — integration closeout, design pass 4, tranche 1

- **Node:** C1, Type 2 TASK (Claude Opus 5.5, `type2-opus-high`), dispatched
  by HELP_HUMAN for run `APP-V4-DESIGN-PASS-4-20261003`. No delegation.
- **Basis:** branch `claude/app-v4-design-pass-4`. Merge base with
  `origin/main` is `13b07065e1`, which equals `origin/main`. HEAD is
  `09ca67d094`, and the working tree carries the owners' later work. "Changed
  under pass 4" means a change between `13b07065e1` and the working tree,
  including untracked files. Paths are relative to
  `projects/chirality-app-v4/execution` (E), with `PKG-*/1_Working/` dropped.
- **Method:** `coordinated-knowledge-work` §3 and §6. I checked only what the
  unit reviews did not establish: sibling pins, ScopeOfWork pins,
  cross-owner interfaces, one rerun of every prototype, and the fences. I did
  not repeat any unit review. I used read-only git, no network, and scratch
  under `$TMPDIR/c1`. I made no commit.
- **Write record:** pin lines in 26 Design files (listed in §7) and this
  file. Nothing else.

## 1. Stale sibling pins (R23-21 item 4)

**How it was established.**

- **Old hashes.** For each of the 160 tracked changed files and the 20
  untracked ones, I took the sha256 of every version at `13b07065e1`,
  `e4a0c2c4c3` and `09ca67d094` that differs from the working file. That gave
  85 old hashes.
- **Intermediate hashes.** I took every 64-hex value in the run folder's
  records that matches no current file. That gave 87 recorded intermediate
  hashes.
- **Search.** A script searched every file under `E/**/Design/` for each of
  those hashes as the full 64 hex or as any prefix of 8 or more characters. A
  second pass searched every pass-4 Design file for hex strings that match no
  current file.
- **Re-pins.** After each round of re-pins, a cascade script listed every pin
  of the bytes I had just changed, and I repeated the rounds until none was
  left.
- **Final check.** Every pin C1 wrote (40 in the Markdown files) resolves to a
  current file hash. The GUIDE table is checked separately below.

### 1.1 Re-pinned: the pass-4 change does not touch the reliance

| Pinning file and line | Pinned file | Old → new | Reason |
|---|---|---|---|
| DEL-03-04 GUIDE input table, row **EXEC** | DEL-02-03 `EXECUTION_COMPATIBILITY.md` | `69e6e79af078…` → `138b04eb0fe7…` | Since `13b07065e1`, two lines changed: L3, which corrects the schema-version statement in place (R23-23 item 2), and L6, C1's ScopeOfWork pin line. GUIDE cites EXEC §2–§6, none of which changed. Label kept as EXEC-v0.7 |
| DEL-03-04 GUIDE input table, row **NIR** | DEL-01-04 `NATIVE_INTERACTION_RECEIVING.md` | `49e180907d39…` → `aca40c0e326d…` | v0.3 changes only the header and §5.1 (the `Turn.error` source line and TO-4). GUIDE cites NIR §4, §5.2 and §9 PD-5, none of which changed. Label is now NIR-v0.3 |
| DEL-09-07 `QUALIFICATION_DOSSIER.md` L8 | DEL-09-01 `EXAMINATION_PROTOCOL.md` | `fc5b8230ec2a…` → `ff0187dafd9e…` | DOS relies on `parts_not_applicable` and the change kind `case_definition`. Two changes followed. First, U-EXP-1 was closed in place after `09ca67d094`: `git diff` shows header lines, the AAC commit wording, the §13 U-EXP-1 row and a change-table row, with no rule, schema or example changed. Second, C1 changed three pin lines. No commit was named, so this is not an R23-21 item 3 pin |
| DEL-09-06 `w14-result-record.example.valid.json` L31 and `.invalid.json` L31 | DEL-02-03 `prototype/run_all.py` | `3fc0d650f5cd…` → `0bc95d07799c…` | **A cross-owner break that no unit review covered.** Pass 4 changed `run_all.py`, and DEL-09-06's `run_w14_rehearsals.py` failed 43/1 ("valid example equals the regenerated W14-05 record"). I diffed the regenerated record against the example: only this sha256 differed, apart from the date. After the re-pin the check gives 44 passed, 0 failures. The JSON has no room for a ruling ID, so this table records it |

These pins were also re-pinned because C1's own pin-line edits changed the
bytes they pin. I call them cascade re-pins. A pin-line change touches no
reliance. Each is marked "(C1 re-pin, R23-21 item 4)", or in GUIDE's version
cell "(ScopeOfWork pin line only, R23-5; re-pinned at pass-4 closeout C1,
R23-21 item 4)". Old and new full hashes are in §7.

| Pinning file | Pins re-pinned |
|---|---|
| DEL-03-04 GUIDE input table | C, P, ADAPTER, AS, WD, WD-EX, LOOP, HOSTING, CA, RELAY, XT, RECOVERY, NPTD, WR, ROLE (15 rows) |
| DEL-01-06 `PACKAGING_AND_DISTRIBUTION.md` | L30 HOSTING, L37 EXP, L42 WR, L45 ROLE |
| DEL-09-01 `EXAMINATION_PROTOCOL.md` | L34 HOSTING, L39 CA, L43 XT |
| DEL-09-02 `STANDALONE_QUALIFICATION.md` | L36 RECOVERY, L38 NPTD, L54 WD, L56 WR, L67 HOSTING, L69 EXP |
| DEL-09-07 `LOCAL_HOST_QUALIFICATION.md` L10 | CA, C, P, AS, LOOP, HOSTING, GUIDE |
| DEL-09-07 `TRAFFIC_OBSERVATION_PLAN.md` L7 | LOOP, AS, LHQ |
| DEL-09-07 `QUALIFICATION_DOSSIER.md` L9 | LHQ |
| DEL-09-11 `READER_METHOD.md` L15 | DOS |

### 1.2 Deliberate pins at committed bytes (R23-21 item 3): checked, unchanged

Each named commit was checked with `git show <commit>:<path> | shasum -a 256`.
All of them hold.

| Pin | Named commit | Holds |
|---|---|---|
| AAC-v0.2 `062ce28c…` in PKG L47, EXP L48 and SQ L46 | `31d65b0be3` | yes. The relied-on lines SEAL-2, NA-3 and VC-AAC-03/07/08/13 are textually identical in the current AAC |
| EXEC `69e6e79a…` in SQ L58 | `61e7a0afec` | yes |
| ACT-v0.9 `4ef8c042…` in SQ L61 | `dc61150559` | yes |
| RS-v0.9 `a91882e7…` in SQ L64 | `61e7a0afec` | yes |
| ACT, RS and EXEC in LHQ L10; RS in DOS L9 and TOP L7 | `cec590c5c3` | yes (all three files) |
| EXP `fc5b8230…` in DAC L18 | `09ca67d094` | yes. U-EXP-1's later closure is outside what DAC relies on |

### 1.3 Not re-pinned

| Pin | Reason |
|---|---|
| GUIDE input table, rows **ACT** (`4ef8c042…`, ACT-POLICY-v0.9), **RS** (`a91882e7…`, RS-v0.9) and **AAC** (`062ce28c…`, AAC-v0.2) | **The change touches GUIDE's reliance.** GUIDE M5.1 states "Canonical acts A1–A15". It rests on ACT §2.1–§2.4, RS §6.1 and AAC §1.2, and each of those sections gained an A16 row. ACT §10.1 V-01 now reads A1–A16. M5.5 also rests on RS §7 L-0, which gained A16 supersession. Bringing M5.1 (and, if wanted, M5.3 and M5.5) up to date is a content edit. All three old pins remain verifiable at `13b07065e1` |
| DEL-01-01 `VERSION_ADVANCE_0.160.0.md` §7.1: 21 file rows (16-hex) | **A dated inventory.** Each row binds line-numbered statement classes to the bytes VC read, so re-pinning a row would claim VC read bytes it did not read. NIR changed for VC's own Δ3, and EXP, LHQ and TOP changed after VC. **Six rows pin working-tree bytes that are in no commit:** AAC `eca9a079…`, ACT `e5bf830c…`, RS `1068e295…`, EXP `dc6b6a0c…`, LHQ `2668d955…` and TOP `cf0b65f2…` (checked against every commit in `git log --all` for each path). Those six rows cannot be re-verified from git. Listed in §6 |
| DEL-01-02 RECOVERY L34; RS L47 and L1343; CA L872 | History rows that record what was read or run at an earlier node. They are not current pins |
| Self-history lines (the "supersedes … sha256" headers of ACT, RS, NIR, AAC, PKG, SQ and EXP); "frozen as LHQ-U1 at `2668d955…`"; the FX-DP1 manifests `e3c8c5ea…` and `346191ff…` in DAC and RRM | History, stated as such |
| DEL-09-11 frozen input sets and fixtures (`IS-FX-DP1*.input-set.json`, `RR-E-input/`, `definitions/aac-offer-digest-0.1.md`, the accounts) | Byte-frozen evidence for their input sets (R23-21 item 3; R23-23 item 4). `IS-FX-DP1-3-input/definitions/…` cites AAC `de39976e…` L240–273. That is the current AAC, and the excerpt equals those lines byte for byte (`diff`) |
| `f0d825711252…` in the AAC examples and the FX-DP1-3 offer and capture | An offer digest value, not a file pin |

**GUIDE pin check.** I used B8's `pins.py` (sha256 `b943319d…5423`, the copy
outside the repository, unchanged).

- **Before C1:** 20/25. The five that differed were ACT, RS, EXEC, NIR and
  AAC.
- **After C1:** 22/25. ACT, RS and AAC still differ, for the reason given in
  the table above.
- **Why not 25/25:** the brief expected the full count. It cannot be reached
  without the GUIDE content decision in §6 item 1.

## 2. ScopeOfWork re-pins (R23-5; SCA-V4-003 derivative closure)

**How it was established.**

- **Finding the pins.** A script hashed every version of every
  `ScopeOfWork.md` in git history. It then searched `E/**/Design/` for any
  prefix of 8 or more characters of a non-current version. The 23 current
  Design files that pin their own SoW at a pre-SCA-V4-003 hash are the 19
  listed in the table below, plus O-A's ACT, RS, NIR and AAC, which already
  pin the current SoW.
- **Each SoW changed once.** It changed exactly once since the block basis
  `40e04273da`, in commit `2d5e6845c5` (REVISE). Its prior hash is the one
  each Design file pins.
- **None of the re-pinned files changed since the blocks were traced.** None
  of the 17 re-pinned files changed between `40e04273da` and the working tree
  before C1 (`git diff --stat`), apart from EXEC L3. So the SCA-V4-003 traces
  ("verbatim" from these files' sections, reviewed at V23–V26) apply to the
  same bytes.
- **Reading the blocks.** I read every block for each deliverable in
  `AgentRuns/APP-V4-SCA003-20261002/AMENDMENT_PACKET/SOW_REVISIONS_A.md` and
  `_B.md` (sha256 `42c9167a…fc07` and `d7b5cb24…94df`), along with the
  Handoff_State and Impact_Assessment entries on design re-pins.
- **Keyword check.** For each substantive block, a check confirmed that the
  design file already states the content: 62 block groups, all present. One
  apparent miss was a capitalisation difference ("Stated, not enforced" in
  ROLE).

**Criterion, stated plainly.** A block bears on a file when it requires a
change to that file's design text. It does not bear when it does any of the
following:

- restates the file's own text, or an owner decision the file already
  applies;
- adds the amendment reference (AX);
- names receivers, which ground register rows.

The amendment record classes this derivative as a pin update only:
Impact_Assessment, "same class as SCA-V4-001's 17 re-pins", plus the ACCESS
§13 follow-up.

**Re-pinned (17).** Each change is made on the header line that holds the SoW
pin, and no line is inserted, so line-number citations stay valid. The note
reads "(SCA-V4-003 revision; re-pinned at pass-4 closeout C1 under R23-5, was
`<old>`; SCA-V4-003 blocks read: G-…, none requiring a change to this file's
design text)".

| File (line) | Old SoW → current SoW | Blocks read |
|---|---|---|
| DEL-01-01 HOSTING (L8) | `9945e72b…cc75` → `bbc81a8d…5d02` | G-0101-01…04 |
| DEL-01-02 RECOVERY (L8) | `057ae2fd…c6b4` → `6c62de1d…6a07` | G-0102-01…18 |
| DEL-01-03 NPTD (L9) | `b5d533cb…05f2` → `0056ec19…6069` | G-0103-01…11 |
| DEL-02-01 WD (L6) | `ef360edf…2f17` → `9479fc88…bd49` | G-0201-01…03 |
| DEL-02-01 WD-EX (L6) | `ef360edf…2f17` → `9479fc88…bd49` | G-0201-01…03 |
| DEL-02-02 WR (L32, 16-hex form) | `5814116909db8120` → `fe9f9bd923f94ed3` | G-0202-01…09 |
| DEL-02-03 EXEC (L6) | `0006521b…726d` → `625b299e…6e5f` | G-0203-01…13 |
| DEL-02-04 ROLE (L47 table row, 16-hex form) | `3acfaa62a3bbf003` → `2327508f2290e7cf` | G-0204-01…13 |
| DEL-03-01 C (L7) | `9ada531b…9449` → `48f0496c…1b6c` | G-0301-01…08 |
| DEL-03-02 P (L7) | `35609151…4d0f` → `e2f8d49d…a21f` | G-0302-01…04 |
| DEL-03-03 ADAPTER (L6) | `93faf918…1a93` → `d76b053f…2e7a` | G-0303-01…05 |
| DEL-03-04 GUIDE (L9, the v0.6 basis line) | `895f004e…7c28` → `aac10af8…761d` | G-0304-01…04 |
| DEL-04-02 AS (L8) | `f16ffa8a…4460` → `e130ef7d…3fc5` | G-0402-01…02 |
| DEL-05-01 LOOP (L9) | `9b2379a1…85ed` → `6fdf4d59…4fa1` | G-0501-01…04 |
| DEL-09-06 CA (L8) | `287d47a1…7923` → `8edc7b3c…61a3` | G-0906-01…05 |
| DEL-09-06 RELAY (L5, metadata) | `287d47a1…7923` → `8edc7b3c…61a3` | G-0906-01…05. §0–§3 span sha256 `6e399c83…` is unchanged before and after |
| DEL-09-09 XT (L8) | `e887a579…e53a` → `fafd126f…786f` | G-0909-01…04 |

The full current SoW hashes are in the files. RECOVERY's and NPTD's
"(INIT, unrevised)" qualifiers were replaced, because they described the old
hash.

**Not re-pinned (2).**

- **DEL-01-05 `ACCOUNT_AND_PROVIDER_ACCESS.md` (L27, `baf68c79…a6`).**
  G-0105-02 bears on it. CLM-004 now names DEL-09-02 as the receiver of
  V4-EXM-12 inputs. The amendment record (Impact_Assessment m-7; R22-7) says
  that ACCESS's §13 register table gains DEP-09-02-013's supplier-side row at
  the same touch. That is a content edit. I read G-0105-01…16, and every other
  block is already stated in ACCESS.
- **DEL-01-01 `PIN_SPIKE_0.158.0.md` (L5, INIT `eddd122c…`).** A dated
  observation record whose stated basis is the INIT SoW. HOSTING L13 records
  that it is not edited (R9-10).

**Already current (O-A, R23-5):** ACT, RS, NIR and AAC. DEL-05-02's SoW was
not revised, and PANEL already pins it.

## 3. Cross-owner interfaces (current bytes)

| Interface | What was checked | Result |
|---|---|---|
| EXP-v0.2 → DOS | DOS pins EXP and its three schemas; after C1, all four are current. `parts_not_applicable`, `case_definition`, `host_profile` and `codex_pin` are in the current schemas. DOS's withheld and record-set enums were compared with EXP and RRM | Holds |
| EXP-v0.2 → DAC | DAC pins EXP at committed bytes (§1.2) and `exam.result-record.schema.json` `f7871c96…` (current). `fw04_check.py` writes EXP records and validates them against the current schema: 22/0 | Holds |
| EXP-v0.2 → PKG | Every EXP section and rule PKG cites resolves (12/12). The packaged subject carries `packaged` → required `package_record`, and route `native_packaged` comes with EXP-R2. PKG's check outcome enum equals EXP's `$defs/outcome` (`pass`, `fail`, `blocked`, `not-run`, `inconclusive`) | Holds |
| EXP-v0.2 → SQ | SQ pins EXP (current after C1). Its EXP §/rule citations resolve (29/29). The outcome enum is identical. The route kinds `native_development` and `native_packaged` exist in EXP's schema | Holds |
| DEL-09-02 → DEL-01-06 | SQ cites PKG-v0.2 by section, and the citations resolve. Both I-6 rows name DEP-09-02-014, admitted. SQ falls back to `native_development`, and PKG leaves packaged cases `not-run` until the package exists (EXP U-EXP-5). These do not conflict. SQ L443 already lists the missing supplier-side counterpart of DEP-09-02-014 in DEL-01-06's register, for the next amendment | Holds; register gap already recorded |
| DEL-09-05 RW-1 → DEL-06-02 FV-4a | DAC pins FV `15e25a24…` (current). FV-4a, the label "ready (qualified)", the qualifier first and `readinessQualified` are all in FV and in `fleet_views.py`. RW-1 recognizes both labels and keeps the qualifier | Holds |
| DEL-09-07 → DEL-09-11 (withheld classes) | DOS's `withheld.kind` enum equals RRM's exactly (`harness_session`, `host_agent_conversation`, `app_conversation`, `author_memory`, `derived_view`). DJ-1 withholds derived views. RRM pins DOS (current after C1) | Holds. **NOTE:** DOS's record-set standings (`record`, `project_file`, `host_evidence`, `not_authority`) omit RRM's later `definition` standing, so a definition item, such as a digest rule, would be added by DEL-09-11 when it builds the input set, not by the handoff. This is no conflict, but the two owners may want it stated |
| NIR-v0.3 consumers | SQ adopts v0.3 for S11-1, and TO-4's new clause is present. GUIDE cites only unchanged sections (§1.1). VA is in §1.3 | Holds |
| AAC-v0.3 consumers | DV §5 and AAC §2 AI-9 agree (the package as a runtime value, opened only by the person). DAC and RRM pin the current AAC. RRM's digest definition equals AAC L240–273. EXP, PKG and SQ keep AAC-v0.2 deliberately (§1.2) | Holds |

## 4. Prototype checks, rerun once (final state, after C1's edits)

Each script was run from its `prototype/` folder with
`PYTHONDONTWRITEBYTECODE=1`, scratch under `$TMPDIR`, using the command its
Design file documents. A baseline run before C1's edits gave the same counts,
except where noted.

| Check | Command (from its Design file) | Result |
|---|---|---|
| DEL-04-03 `run_prototype.py` | `python3 -B run_prototype.py $TMPDIR/…` | 67 PASS, "all expectations held" |
| DEL-02-03 `run_all.py` | `python3 -B run_all.py` | 126 ok, "ALL CHECKS HOLD: 0 failure(s)" |
| DEL-01-04 `run_cases.py` | `python3 -B run_cases.py` | 159 checks, 0 failed |
| DEL-04-01 `validate_policy.py` | `python3 -B validate_policy.py` | 6 PASS, "all expectations held" |
| `E/run_e.py` | `python3 -B run_e.py $TMPDIR/…` | 56/56 |
| DEL-06-01 `run_fleet.py` | `python3 -B run_fleet.py $TMPDIR/…` | 34/34 (the committed FX-FL1 fixture rebuilds identically) |
| DEL-06-02 `run_views.py` | `python3 -B run_views.py $TMPDIR/…` | 23/23 |
| DEL-09-01 `check_exp.py` | `python3 -B check_exp.py` | TOTAL 77, FAIL 0 |
| DEL-01-06 `check_pkg.py` | `python3 -B check_pkg.py --tree <VC's 0.160.0 vendor directory in the session scratchpad>` | TOTAL 66, FAIL 0. Without `--tree`: 59/0. Tree mode runs only `/usr/bin/codesign -d` and hashing on the binaries; no Codex binary was executed |
| DEL-09-02 `check_sq.py` | `python3 -B check_sq.py` | TOTAL 114, FAIL 0 (65 supplier case citations checked) |
| DEL-09-05 `fw04_check.py` | Its docstring command, with FX-DP1, the examiner observation, the EXP schema, the DEL-09-05 SoW, and the RS and AS Design folders | 22 expectations, 0 failed |
| DEL-09-11 `run_standing_check.py` | `python3 -B run_standing_check.py` | 19 cases, 0 unexpected |
| DEL-09-07 `top_check.py` | On `lhq.traffic-observation.valid.examples.json`; on `…cb1-violations.examples.json` | Valid example OK (4 of 5 compared, exit 0); both CB-1 violations reported (exit 1, as designed) |
| DEL-09-06 `run_w14_rehearsals.py` (added: cross-owner) | `python3 -B run_w14_rehearsals.py --out $TMPDIR/…` | Before the re-pin: 43 passed, 1 FAIL. After: 44 passed, "ALL CHECKS HOLD" (§1.1) |
| Schema checks (independent, `jsonschema` 4.26.0, Draft 2020-12) | `check_schema` on the 17 schemas changed or added in pass 4; LHQ examples; RRM input sets and accounts | 17/17 schemas valid. LHQ: 27 instances, 0 unexpected (valid accepted, invalid rejected, CB-1 examples schema-valid). RRM: 4 input sets valid; 9 accounts, of which 8 are valid and `account.bad4.json` is invalid as the standing check expects |

`git status` was compared before and after every run. No prototype wrote into
the repository. Nothing in DEL-01-01's `prototype/version_advance/` was run.

## 5. Fences and hygiene

The branch file set is `git diff --name-only 13b07065e1` (working tree)
together with the untracked files: 200 files.

| Fence | Result |
|---|---|
| No ScopeOfWork, `Dependencies.csv`, `_DEPENDENCIES.md`, `_DAG/`, `_ScopeChange/`, `_Decomposition/` or Open_Issues file changed | **0** of 200 |
| Only the eight `_STATUS.md` files changed (R23-28) | **8**: DEL-01-06, 06-01, 06-02, 09-01, 09-02, 09-05, 09-07 and 09-11. Each changes `INITIALIZED` → `IN_PROGRESS`, the date, and one history line citing R23-28 |
| No `/Users/<name>` or `-Users-<name>-` home paths | **0** of the 200 branch files, this file included. In the committed app-v4 tree, 191 files contain such paths at `origin/main` and 191 now, all unchanged by the branch |
| `docs/governance_harness/_PROPOSALS/D-GOV-52_*` untracked and untouched | Untracked: three files, no index entry, no commit in `git log --all`. Modified 21:41–21:43 on 2026-10-03, before the owners' work. sha256: `AGENTS.proposed.patch` `8cad21a7…5b24`, `PACKET.md` `ba9fe6c3…96ef`, `ROOT-DGOV52-PROPOSAL-20261003.yaml` `dc7ffbac…4980`. `AGENTS.md` and `CLAUDE.md` are unchanged against `origin/main` |
| Outside `projects/chirality-app-v4/execution/` | Only the three D-GOV-52 files |

## 6. Remaining for HELP_HUMAN

1. **GUIDE and A16 (blocks 25/25).** M5.1 says "Canonical acts A1–A15", while
   ACT-v0.10, RS-v0.10 and AAC-v0.3 now carry A16. A GUIDE content edit,
   presumably GUIDE-v0.7, is needed before ACT, RS and AAC can be re-pinned.
   M5.3 (capture surfaces) and M5.5 (supersession) may want the same edit. The
   same step can record C1's row re-pins in the header's re-pin narrative and
   in §4.5. Today the version cells carry them.
2. **ACCESS.** Its SoW re-pin, plus the R22-7 / m-7 §13 register-table row
   (DEP-09-02-013, supplier side).
3. **VERSION_ADVANCE §7.1.** Its 21 rows pin earlier bytes, and six of them
   pin bytes that no commit holds (§1.3). Decide whether VA gets a note, a
   refresh, or stays as it is as a dated record. None of the later changes
   alters a Codex fact, except NIR's Δ3 rewording, which VC itself asked for.
4. **Register pins and Receivers lines.** The 17 re-pinned files still pin
   their `Dependencies.csv` at pre-UPDATE bytes. Their dated "Receivers"
   lines predate SCA-V4-003's register UPDATE. The amendment record does not
   require a refresh, and it was outside this brief.
5. **PIN_SPIKE** stays on the INIT SoW under R9-10. Please confirm.
6. **NOTE, DOS → RRM:** the `definition` standing (§3). Owner O-C, if
   wanted.
7. **DEL-09-06:** the W14 examples now pin the current `run_all.py`. CA's
   narrative at L866–874 still describes the 2026-10-02 regeneration as
   history. A one-line note is the DEL-09-06 owner's choice.
8. **Commit.** All C1 edits are in the working tree only. The pre-merge review
   should cover these pin lines; each one is listed in §1, §2 and §7.

## 7. Files C1 edited (pin lines only) and their sha256 before → after

| File | Before C1 | After C1 |
|---|---|---|
| DEL-01-01 `HOSTING_BOUNDARY.md` | `ce235650e8a9494c66ccd08677556e56a88983aa641b5ff22c576328bd8a93b6` | `5401f26d9a2a739a725771c8ce83c62ac5fa07be69b0338ee5670b9453d76d87` |
| DEL-01-02 `EXECUTION_AND_RECOVERY.md` | `d84c7e26f4342d261f385877ddea78a9c935c5f561b5b91602d93d9db49fe2cb` | `b4b6211d2be41e49f755e627283925db6424cdb290d4062b79b5c69e99378f32` |
| DEL-01-03 `NATIVE_PLANS_TOOLS_DELEGATION.md` | `6eed39dcee4acf4b8b986cdd9e09c460a8fa53571973cb5c826acce37d644a72` | `64e4e26de483ce1e6742e172846e2a238f401850a416ff0744c490a4b039cfbd` |
| DEL-01-06 `PACKAGING_AND_DISTRIBUTION.md` | `95722979a8fe963782702e4ca459bc124556c43c0a5c4e0ba439559bed7077fa` | `33aa12a57bf373c8e31bdc1c6e43458ccd2f19093dd34afc320cece608017d68` |
| DEL-02-01 `EXAMPLES.md` | `85fa5a3f9200cef893789165515eafe8aff653f6357135cf7575c6eacd83a361` | `3e5477d4ee7c2ab72c2f97e0d936aab5a7f02797b9c61726851382ad91590de2` |
| DEL-02-01 `WORKFLOW_DECLARATION.md` | `d752810933510d0f814b87005222dc85658b08828221190f2571383bb6e07da4` | `262c9e5417cf67b56cf7c3678128ad406e8b4e2fda7057a07bebf04254ab2f31` |
| DEL-02-02 `WORKSPACE_AND_REGISTRATION.md` | `c5332e9333ccb18c5b4a2a3d633e9d643362b88d0f87187c762a86b5317953c4` | `5ed5da8842b32b87ae68db3476192a55fc8ff151802684b10bdca16eaa8b8d8b` |
| DEL-02-03 `EXECUTION_COMPATIBILITY.md` | `3add943d047bb249b7135a03fedd864ec964447bcd06cd37115a0c0f9ac2eb84` | `138b04eb0fe716321ec11b2ead8f58f012885a3007fffdf2d6e943f6402d0962` |
| DEL-02-04 `ROLE_SUPPLY.md` | `92bb421b7bccee9a02d33a037736a97bb4d4b1e2136246fa83f75c49291c7e2a` | `c8474d919bceec7d6b5b9dc328b03569b2c64f9d849ff950a2e33062cc1034cf` |
| DEL-03-01 `CATALOG_AND_READ_BASIS.md` | `eae7369fc0109f4c4238308ef2cde7a189d83bd0669a78f01b9800d5a30ddf90` | `0e3ba39cd926a2063fc93621c17ed39d1fc8622b2256f08005d1286e99795294` |
| DEL-03-02 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | `f432356d054cb784ded51325de25ef945ddf29e9843cc187e3576841bac6533f` | `ad6a3083e7b808e247562fa0cc3762192b121ff99e75e8ac8167ab25da555eb3` |
| DEL-03-03 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` | `71a397d918319ff884141d7849c342adae73251dd317377ea8cc3825157a8992` | `eed1d912df333822c172593ea81a244661dab305b81c6295493802f252eda761` |
| DEL-03-04 `HOST_INTEGRATION_GUIDE.md` | `8ca61f2de236427984460f807596ef0971418c2db46913ba7df2f06d3eedd1ce` | `3a4f07af1a02f54d7e3e1a35b4161eb4da8bc94b3a62bb24f7005870f97bc034` |
| DEL-04-02 `AUTONOMY_AND_STANDING_EXCHANGE.md` | `dc3fd0b68406fc0fa329b94d3bf3e82d3268584629d97d58f1b568265cbbc5e0` | `4eca598f13c8c0745f94c605b8940a094b55e57b9f7478c989824af229085857` |
| DEL-05-01 `LOOP_RECEIVING_CONTRACT.md` | `d47d2249eb5f863aea640f582893b6861fc5a019d600412de7f3ac2e58cc429a` | `2bac33a883b176e24cd17e6fb78361efea63ce4c254810dcf8ab6e1d13cd7004` |
| DEL-09-01 `EXAMINATION_PROTOCOL.md` | `1371ddb22f72e80aef6dcac734ae6cf288fa3a478bbac5cc607be9e7814a6b9e` | `ff0187dafd9e1f0268a19f9266914bdba64f39e0c8befdcaf20d3da7a7206a93` |
| DEL-09-02 `STANDALONE_QUALIFICATION.md` | `a2ad48cf6803c9e9690e89672582b1a5228ed771fdeb7176968cb88453af552e` | `c317a92547ec17e09dc81802ef2a39af9c8e0fd7f2337dca5e9e82ac062d9688` |
| DEL-09-06 `CONNECTED_ACTIVITY_CONTRACT.md` | `eb133d4101ea50133e1c324dbc3d920faba93d6c89de4bd122cb572e110ee84f` | `44a9b288291c0716ba34945aae46163b69f5af96d0292ca03d343eec5811a9ee` |
| DEL-09-06 `RELAY_QUESTIONS_SWBPIPE.md` | `6e726be9ae39e8a8b5ec39b38984081339bac5bee52ce88fc8739a298801ae92` | `cd74b53dfc46f3477756c723987a5aa85af3fcf6d24ff2292809a838e92b067c` |
| DEL-09-06 `w14-result-record.example.invalid.json` | `1a1eacac7b8177691c127d3a6abf7a8056195b4e437d86b7b7ac806d2a675fb0` | `0e1f215920b4fb0761180394fc1e3b57a0904973d146901d571f5440ce092dd9` |
| DEL-09-06 `w14-result-record.example.valid.json` | `a14c5934cd47d74e6665857d66f4e485b29ca8ba7b7c37be54579971cbfb432b` | `f968a3fa46ea20f7b59a9e5e487307ea51384e2cb721dba39717cbd11826faa9` |
| DEL-09-07 `LOCAL_HOST_QUALIFICATION.md` | `4ee7de2630b7ed9ea1870bca938c434971f71e5413b60bb2e3247c5fc73931bc` | `fa2e306ffdc7211c79973797005c7ba55555b242570761e1029e4d6171d84536` |
| DEL-09-07 `QUALIFICATION_DOSSIER.md` | `83101523d9c16d0a097629e3a63b03d46efa4b67c01a66981da274ab4be750d1` | `16e41fbef6f2b7851f7d11c752886d144e3caa84e1062569fc477afd4b74c81a` |
| DEL-09-07 `TRAFFIC_OBSERVATION_PLAN.md` | `5d147be4c0b441b34017933c84a195b905c24f01d2764e4fc669e36aef6d0324` | `5b0250f1b97509162ecbbc78aa1d5d3eeb6caa18f1c6666e5ffdf7521d8ffe6e` |
| DEL-09-09 `EXTERNAL_TRACE_CASES.md` | `d973677bab5abdc03b170e10c0ad52a1135cc8dd5ad24afc7886271c97e7f456` | `cc1543619b767ede6af9fb614c82faa7430da634b4846fa263a1da619383808a` |
| DEL-09-11 `READER_METHOD.md` | `3a4a1462285fc91a15835346e7ebd1c21d344ff386ac35ac64ef4e7d081e7673` | `d696077cad5caeb09b9d339d99b7220eca58db691c32e6451b13a63ac49c4276` |

`git diff --numstat HEAD` shows a one-line change in each of the 17 pass-3
files that were otherwise unchanged in the working tree. GUIDE shows 18 lines:
L9 and 17 table rows. No line was added to or removed from any of those 17
files, so line-number citations of them stay valid.
