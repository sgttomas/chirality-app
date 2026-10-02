# RV21-A — repairs from V21 in the six new Design folders

- Run `APP-V4-DESIGN-PASS-3-20261001`, node **RV21-A** (BRIEFS "RV21", row RV21-A). Type 2 TASK (Claude Opus 5.5), dispatched by HELP_HUMAN; no delegation. 2026-10-02, at HEAD `6185de63da`.
- Binding: R21-1…R21-4 (`R20_RESOLUTIONS.md`), R17…R20, OWNER_DECISIONS. Findings: `reviews/V21-A.md` (M-1, M-2, MINOR 1–14) and `reviews/V21-B.md` (M-3 AAC side, m-4, m-11, the Stop Codex label), plus HELP_HUMAN's mid-task note on the NPTD availability reading (R21-1).
- Fence kept: only files in the six new `Design/` folders (DEL-01-02, 01-03, 01-04, 01-05, 02-02, 02-04) and this return file. No version steps; each touched Design file has an "RV21" row in its change table. Read-only git; no network; no Codex or model run. ROLE (DEL-02-04) needed no change.
- Paths below are relative to `projects/chirality-app-v4/execution`; `DEL-xx-yy/` stands for that deliverable's `…/1_Working/DEL-xx-yy_*/Design/`.

## 1. Findings fixed

| Finding | Ruling | What changed | Where |
|---|---|---|---|
| V21-A **M-1**; V21-B **M-3** (AAC side) | R21-3 | One A15 offer is composed from exactly **one** DEL-02-02 descriptor: WR's `a15_descriptor` (one reviewed draft, `draft:`, "register workflow revision") or `a15_multi_descriptor` (two or more library entries in place, `entry:`, no prior revision, "register workflow revisions"); entries sit inside it. Reviewed-content pattern widened to RS-v0.9's `^(draft\|entry):(project\|user):[^@]+@.+$`. AAC's old "several reviewed drafts at once" reading withdrawn (several drafts are several acts, AK-d). Schemas bumped to 0.3; examples rebuilt (offer 3 valid / 16 invalid; capture 2 valid / 12 invalid). Prototype: `from_wr_descriptor` maps WR snake_case one to one; K-12b…K-12d rewritten for one multi descriptor; **K-17** runs WR-v0.2's own two descriptor examples (valid against WR's schema) through offer and capture into RS's writer (offer, capture and RS entry valid; wording, descriptor, purpose, reviewed content unchanged); **K-17b** builds capture evidence for RS act-log record 4 (`cap:reg-in-place-2`, `entry:` strings), valid against the capture schema, and the control writes the same relations, subjects, content and actor from it. WR RB-4a's stale sentence replaced (item 6); WR ME-3 cites AAC | DEL-01-04/`APP_ACT_CONTROL.md` §1.2, AI-2, AX-06, §4.2, §5.1–§5.3, §8 (VC-AAC-09b, new VC-AAC-15); `aac.offer.*`, `aac.capture-evidence.*`; `prototype/act_control.py`, `run_cases.py`; NIR IF-5; DEL-02-02/`WORKSPACE_AND_REGISTRATION.md` RB-4a, ME-3 |
| V21-A **M-2** | R21-2 | NIR §6 rewritten: OBS-3 W-3/W-1/W-4 cited; three carriers — text element (text files, the file named; "supplied"), `image`/`localImage` (images; "supplied"), named path for the agent's tools (other files; "named; read only if a tool item shows it"); `mention`, `skill`, audio inputs and `thread-attachment` not used. `supplierRead` per form; `toolReads` for named paths; AT-9, AT-10 (PROPOSED wording), AO-1/AO-2 narrowed to `localImage` and named paths; AT-8 (K-7 draft trial) follows, with a `draft` element replacing v0.1's `draft-package` form. Schema 0.2, examples 4 valid / 11 invalid (the `mention` example replaced). New U-NIR-10 (text bound PROPOSED 256 KiB; image read not observed) | DEL-01-04/`NATIVE_INTERACTION_RECEIVING.md` §6, VC-NIR-13, §14, U-NIR-10; `nir.attachment-supply-record.*`; `prototype/nir_model.py` (`carrier_for`, `attachment_input`, `supply_record`, `tool_read`), `run_cases.py` A-1…A-8 |
| V21-A MINOR 1 | — | AI-7 and §4.4's A15 exceptions deleted: A15 recorded at capture like every kind | AAC AI-7, §4.4 |
| V21-A MINOR 2 | — | §5.3 count follows the rerun: 11 entries, all valid (was 9) | AAC §5.3, VC-AAC-12 |
| V21-A MINOR 3 | — | RS-v0.9 cited as current (no "in progress") | AAC §4.2 step 6, §5.3 |
| V21-A MINOR 4; V21-B Stop Codex label | — | TO-4 adds "interrupted by Stop Codex"; §5.2 uses RECOVERY's "interrupted by quit" / "interrupted by Stop Codex"; §5.1 cites RECOVERY-v0.2 §3.4 `outcomeLabel`, not "its node-D1 draft". `turn_label` gains `codex-stop`; check O-3a | NIR §5.1, §5.2; `nir_model.py`; `run_cases.py` |
| V21-A MINOR 5 | — | IF-13 quotes NPTD §5.4's "no model selected"; R18-2's wording stays ST-3's | NIR IF-13 |
| V21-A MINOR 6 | — | TC-2 places the run-end line (R20-3; WR TX-5) first when no run starts; `compose_turn(run_end_line=…)`; check O-8a; O-9 now also validates a turn with the run-end line and all three carriers against `TurnStartParams` | NIR TC-2; prototype |
| V21-A MINOR 7 | — | RN-2 follows R20-1 (run ends only by the person or the run owner) and R20-11 (1); VC-NIR-23 expects "End ‹A› and start ‹B›" enabled during a run | NIR RN-2, VC-NIR-23 |
| V21-A MINOR 8 | — | "End run" is DEL-02-03's run end, with DEL-01-02 DEF-4 as the definition | NIR §5.2 |
| V21-A MINOR 9 | K-3 | CA-3 offers the project's last explicit choice exactly as ST-2; the source's model is not offered as such | NIR CA-3 |
| V21-A MINOR 10 | C-23 | ACCESS uses RECOVERY's `assess live work` (live turns, outstanding requests, active children) for sign-out and key removal, as a runtime value (no row) | DEL-01-05/`ACCOUNT_AND_PROVIDER_ACCESS.md` §1, AE-12, KE-13, Q-5 |
| V21-A MINOR 11 | — | One rule: `thread/resume` carries no override; a model change is per turn (ACCESS CS-18). RECOVERY drops the resume model override and the matching runtime value; ACCESS Q-11 states the rule; ROLE §5.5 already did (unchanged) | DEL-01-02/`EXECUTION_AND_RECOVERY.md` §4.1, §4.2; ACCESS Q-11 |
| V21-A MINOR 12 | R19-8, R20-6 | H-probe cited at ACCESS §3; CV-21 separates "Continue as ‹role›" (`thread/start`) from a fork (`thread/fork`, `forkedFrom`); V2-6 (a change-table row, left as history) is read with this correction, stated in the RV21 row | RECOVERY §1, CV-21 |
| V21-A MINOR 13 | C-05 | WR §7's DEL-01-03 row: only the plan-mode element needs the opt-in; §8's RS-v0.8 paragraph rewritten to the RS-v0.9 form | DEL-02-02 §7, §8 |
| V21-A MINOR 14 | R17-1 | NPTD `npt.item-anchor` and `npt.delegation-export` `$id` → `…:v0.2` (`npt.plan-revision` unchanged, stays v0.1; no reference to these `$id`s elsewhere, checked by `grep`). NIR §13.2 and the prototype README label S-4 and O-9 optional third-party cross-checks | DEL-01-03 schemas, §11; NIR §13.2; `prototype/README.md`, `run_cases.py` labels |
| V21-B **m-4** | R21-4 | Supply check reads `thread/items/list {threadId, turnId}` following `nextCursor` (HOSTING-v0.9 §4.4), not `thread/read {includeTurns: true}`; *unreadable* = a failed read or page; U-WR-14 notes the items route is `observed-in-generated-types` only (W-4 observed the text via `thread/read`). Prototype `RunDesk.check` reads pages; new **P-50a** validates params and pages against the generated `ThreadItemsListParams` / `ThreadItemsListResponse`; P-52's "items not loaded" case is now "a later page failed" | DEL-02-02 SC-3, §16.4, RN-5, §1 R19-7 row, §3, VC-14, U-WR-14; schema `supply_check` description; `prototype/wrproto.py` |
| V21-B **m-11** | — | AAC capture `actor.codexAccount` takes RS `$defs/person`'s `anyOf` (email or "ChatGPT account (no email reported)"); invalid case INV-CE-9 | `aac.capture-evidence.schema.json` |
| HELP_HUMAN note (RV21-B's finding) | **R21-1** | NPTD §7.1 now states R21-1's order and is named the reference. `delegation_availability` follows it: disabled → missing; `multi_agent = false` → missing; `namespaceTools` false → missing; any of the three not read → not established (a configuration never read, `None`, is now *not established*; `{}` is "read, nothing set"); else present. PC-16 adds the configuration-not-read case, a "missing wins over unread" case, an ordering case, and checks all 64 combinations of {missing, present, null, not read} per signal against R21-1: 0 disagreements | DEL-01-03/`NATIVE_PLANS_TOOLS_DELEGATION.md` §7.1; `prototype/npt_model.py`, `run_cases.py` |
| V21-B m-9 (F-E2 §4.3 row 7) | R19-7 | Fixed here because the file is in this fence, not RV21-B's: the WR schema's `selection_record` description no longer names DEL-02-04 (no meaning change). Tell RV21-B it is done | `workspace-registration.schema.json` |

## 2. Not fixed, and notes for others

- None of the assigned findings is left open.
- **For RV21-B / RS (outside this fence):** RS act-log example record 4 (`RS_RECORD.valid.act-log.example.jsonl`, the L-4 two-entry act) has purpose "make it available in the project library"; WR's multi descriptor uses "make them available …". RS's schema leaves purpose free, so it validates; K-17b uses RS's text as given. Aligning the example is RS's.
- **For RV21-B / EXEC:** NPTD §7.1 is now R21-1 verbatim in order; EXEC EV-3a, `_delegation` and WD §4.2.5 can follow it. In particular a configuration that was **not read** is *not established*, while a configuration read with nothing set is not a "not read" signal.
- The schema `$id` bumps (AAC 0.2 → 0.3, NIR attachment 0.1 → 0.2, NPTD two → v0.2) are schema versions, not Design-file version steps; no other file references them (`grep` over `projects/chirality-app-v4`).
- K-17 reads WR's live identity through a stub that returns WR's own example values (WR's examples carry `rev-…` values, not digests); this is stated in the check's code comment.
- I did not check which of these files GUIDE pins. The GUIDE re-pin after both RV21 nodes should recompute every pinned input: the RECOVERY, NPTD, NIR, AAC, ACCESS and WR hashes below have changed.

## 3. Reruns (2026-10-02 21:43 UTC, macOS Darwin 25.6.0 arm64, Python 3.13.7, `python3 -B`, `PYTHONDONTWRITEBYTECODE=1`, in each `Design/prototype/`)

| Deliverable | Command | Before (baseline at `6185de63da`) | After |
|---|---|---|---|
| DEL-01-02 RECOVERY | `run_cases.py` | 16/16 as expected | 16/16 as expected, exit 0 (text-only change) |
| DEL-01-03 NPTD | `run_cases.py` | 18/18 | **18/18**, exit 0; PC-16 per R21-1, 64/64 combinations; `fixtures/native/*.jsonl` rewritten byte-identical (no git change). Output `prototype/results/RUN_2026-10-02_RV21.txt` |
| DEL-01-04 NIR/AAC | `run_cases.py` | 120 checks, 0 failed | **151 checks, 0 failed**, exit 0 (A-1…A-8, O-3a, O-8a, K-12b…K-12d, K-17, K-17b; S-3 over the new invalid cases; S-4 and O-9 ran with the installed `jsonschema` 4.26.0). Output `prototype/results/RUN_2026-10-02_RV21.txt` |
| DEL-01-05 ACCESS | `run_cases.py` | TOTAL 9, FAIL 0 | TOTAL 9, FAIL 0, exit 0 (text-only change) |
| DEL-02-02 WR | `wrproto.py` | 98/98 | **99/99**, exit 0 (P-50a new; P-51, P-52 read pages) |
| DEL-02-04 ROLE | `run_cases.py` | 36 pass, 0 fail | 36 pass, 0 fail, exit 0 (no change) |

Independent schema check (scratch script, not in the repository): the changed schemas and every example instance validated with both DEL-04-03's `minischema` and `jsonschema` 4.26.0 (Draft 2020-12): every valid instance valid, every invalid instance refused, same verdicts. `git status` after the runs shows only the files listed below; no `__pycache__` (checked with `find`).

## 4. Files written (sha256 after; prefix before at HEAD)

| File | Before | After |
|---|---|---|
| DEL-01-02/`EXECUTION_AND_RECOVERY.md` | c528b47627ea116c | 678042beae0327e6fcbabb99eaea746d46c843198238ac4dfc67690ea26149c1 |
| DEL-01-03/`NATIVE_PLANS_TOOLS_DELEGATION.md` | 5cfda3ac81b3d202 | 6eed39dcee4acf4b8b986cdd9e09c460a8fa53571973cb5c826acce37d644a72 |
| DEL-01-03/`npt.delegation-export.schema.json` | cd25e78188ac6f22 | 49f32198cd8d8589593536e5abf854abef5cf109461f5983c19a23032652ac60 |
| DEL-01-03/`npt.item-anchor.schema.json` | 85953d54e969388b | d26a55d3ad77fdc5217ca515e95f1321be27023dbd54fef4a70cb3c314b38281 |
| DEL-01-03/`prototype/npt_model.py` | f64ec3dc4b4d398d | 543cffa4cec374dfa16b656e12dce6b8d5b0bc7048d1bae89b19ef5fc128bc35 |
| DEL-01-03/`prototype/run_cases.py` | 9fd9062ecbf34f06 | f3bed9012ab0517d9be2489a3a42a39a10401641973d438b439253919947b438 |
| DEL-01-03/`prototype/results/RUN_2026-10-02_RV21.txt` | new | 6046654fc9106cb5bd141c87abbc24c9d6c2071d4b6073226c73c161ac56f944 |
| DEL-01-04/`APP_ACT_CONTROL.md` | 38cb681ec435312b | 062ce28c8a4ec0bc79fc6b6c421245057a59815df14b88fa779b61eeb98be7d7 |
| DEL-01-04/`NATIVE_INTERACTION_RECEIVING.md` | d56830e7274be4d2 | 7144aebd4a72522d156ea6bae21db78da9343565d68f3f5688a46b35a2f50576 |
| DEL-01-04/`aac.offer.schema.json` | 4bfa3781d8f1d323 | 8e6acaf1fe3a6a5481168122444eb5a6d1f305a647385d90cdb0c0cb8c919eec |
| DEL-01-04/`aac.offer.example.valid.json` | d30c13b69f818d01 | 24cf7c46fb41f011fe4096204a16afc3bcf546e27ce9604246c7bc59de73a0f0 |
| DEL-01-04/`aac.offer.example.invalid.json` | e0e71d1f253d0fcd | 54c17edc2b468a20d80c8868c5ff31f9ee332cac4df6c9b01846850991a1f9bf |
| DEL-01-04/`aac.capture-evidence.schema.json` | 1c7e2336dac554e8 | 1b75bba70a9dfa6d778a7652793e37c5da5b063b955f67f1364e053d359e2a06 |
| DEL-01-04/`aac.capture-evidence.example.valid.json` | 33a16fc6ad658bbd | 7fe4092cbf758d657ed5f0872aa6deccb25e59ecf6b6f91301f43df32ce2c106 |
| DEL-01-04/`aac.capture-evidence.example.invalid.json` | bb471c5948f5f7ca | 2e5aa2d2caf8bc93831abd746be3f2890dcb24a3bdd749077a0ffc439a9af07e |
| DEL-01-04/`nir.attachment-supply-record.schema.json` | 9126f38452bdb100 | eb9e965df9f5c562b000991aaf23f2e8541f47d33d38c37910a13e95daa87850 |
| DEL-01-04/`nir.attachment-supply-record.example.valid.json` | 3e2c7fa04745edcb | 4e1cd04bd059ff75909ff9e27633d26717318e5e97888f6a5d7cec1749866b0d |
| DEL-01-04/`nir.attachment-supply-record.example.invalid.json` | 4b1b8de5c753c255 | 835cd85dcbed2f7c176e3750f430e75a183495a88d9fd2bf19302f097ef87da6 |
| DEL-01-04/`prototype/README.md` | 650cbca5dc02bd0f | 586d356f3a4ddb193ae84012f26e02396a046b5ab4193208ac0c48ffe2957d4b |
| DEL-01-04/`prototype/act_control.py` | f5e0fbee426567bd | 27e0095819ecdb165ccb317927361026a6b168a6641f4ab2b4b4a3e35e01294e |
| DEL-01-04/`prototype/nir_model.py` | 83085f636ff804d9 | d7c31ec083c72caf0e8e69f909d96c5433ee1dbf5279558fd1bed0ae604d5c01 |
| DEL-01-04/`prototype/run_cases.py` | 48607363eb964266 | 30d0cb9c2888eaa4e09c3b4efb6c37d070c8e8dc810ddba113cb78a4d6a1bada |
| DEL-01-04/`prototype/results/RUN_2026-10-02_RV21.txt` | new | 4ce71b322e0de69386fa394944432710f109c84a02d5d17d01dd3c92570a1b87 |
| DEL-01-05/`ACCOUNT_AND_PROVIDER_ACCESS.md` | 8cc7a60f755070c2 | 929bd07b32f40fc6f65b6df6ce5b7aebe6cd91a89866525a981e5cbe11c4ffa0 |
| DEL-02-02/`WORKSPACE_AND_REGISTRATION.md` | 8df3a942e7f0132d | 5b522ce626dcaadd73e5abb46b9db1303d45a9cf2307feface5920d831d056dd |
| DEL-02-02/`workspace-registration.schema.json` | 61ebfe86f973b87d | 6228a28cc1776e2e15a99cd5201eccdbe9db10e7968f7d7a67b974bae18b5928 |
| DEL-02-02/`prototype/wrproto.py` | 3c79e72b671a1658 | 256168a263f0ea5cf7af81da44ce1c21bdead70ab64205dff6e445161e4900c1 |

Unchanged: everything in DEL-02-04 (ROLE), the DEL-01-05 decision record and schemas, RECOVERY's schemas and prototype, `npt.plan-revision.schema.json`, NIR's answer-submission and draft-transition schemas, WR's examples.
