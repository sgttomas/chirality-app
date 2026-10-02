# RX — residual sweep (design pass 3)

- Run `APP-V4-DESIGN-PASS-3-20261001`, node **RX**. Executor: Type 2 TASK
  (Claude Opus 5.5), dispatched by HELP_HUMAN; no delegation. 2026-10-02,
  working tree at HEAD `83a3989850`, in parallel with F-E1.
- Brief: `BRIEFS.md` "RX — residual sweep" items 1–5 (sha256
  `d6ce024766624728`). Binding: `OWNER_DECISIONS.md` (`ea96c55710af41c9`;
  DECISION-K3 revised, DECISION-L); R17 (`b0af81bcbad9bc52`), R18
  (`abf5eee6324647ff`), R19 (`16930ecdcead7511`), R20 (`5e68574054a3353e`;
  R20-1, R20-3, R20-5, R20-9); `F/F0_JOINS.md` (`e93608be1c6e3eb0`); D returns
  §R2.3, of which D3 (`5c0fdcdab9ba1f0e`) and D5 (`332bc81ff1851551`) carry the
  items used here; F returns F-A (`bf4e329b2babbf42`), F-B (`1fa85535ba916128`),
  F-C (`95362fef71da6700`), F-D (`ba9e15fd7363f9dd`).
- Boundary kept. Edits were made in place, with no version step. Files
  written: WR (the Design file, schema, both example files, `prototype/wrproto.py`),
  `ROLE_SUPPLY.md`, `NATIVE_INTERACTION_RECEIVING.md` (NIR only; AAC and the
  DEL-01-04 prototype untouched), `HOSTING_BOUNDARY.md` only, `EXECUTION_COMPATIBILITY.md`,
  and `CONNECTED_ACTIVITY_CONTRACT.md` with its two example files. Nothing
  else was written, including ADAPTER, XT, LOOP, PANEL, GUIDE, WD, `FACTS_*` and
  `RELAY_*`. Git was read-only, with no network and no Codex or model run.
  Scratch is under `$TMPDIR/.../scratchpad`. No `__pycache__` was left (checked
  with `find`).
- How the edits were checked:
  - Each edit was a scripted replacement of a string that had to occur
    exactly once; the script stopped otherwise.
  - Table column counts were compared before and after for every edited
    file. No new mismatched row: HOSTING still has its one older mismatch,
    and every other file has none.
  - Each touched file has an "RX" row in its change table.

## 1. Items done

### Item 1 — R20-9 (the two agent lines)

**WR-v0.2** (`DEL-02-02/Design/`):

- §16.2 line 3: the proposal line now tells the model
  `"Workflow finished: ‹origin›:‹name›"` for the run in force, using the
  run's own tuple origin, so a shipped revision reads `bundled`. It also gives
  `"Next workflow: <origin>:<name>"`, each on a line of its own. This is
  "WR-FRAME-1 repeats them for the run in force".
- §16.5:
  - PR-1: the proposal is exactly `Next workflow: ‹origin›:‹name›`. A line
    without an origin is not a proposal.
  - PR-2: the pair is resolved inside the named origin to exactly one
    registered workflow, as NIR RN-3 reads R20-5. Previously the name was
    unqualified and the person chose among candidates.
  - PR-3: there are now notices for a draft, for an unknown pair and for a
    pair that matches several workflows.
  - FN-1: the finished report is exactly `Workflow finished: ‹origin›:‹name›`
    and must name the run in force.
- Other text: the §8 count and reader check, §12 WR-VC-11 and WR-VC-15, the
  §13 rerun note, and §15 U-WR-20, which is closed because ROLE GS-7 now
  carries both lines.
- Schema: `frame_lines.proposal_line` changed from a constant to a pattern,
  and `proposal.proposed_name` now has the pattern
  `^(project|user|bundled|host):name$`.
- Examples:
  - The valid run_text and the confirmed-proposal selection
    (`project:supports-adjust`) are aligned.
  - INV-12 and INV-13 have their proposal line updated.
  - INV-16 is new: an old-form proposal line, rejected because it does not
    match the pattern.
  - INV-17 is new: `proposed_name` without an origin, rejected because it does
    not match the pattern.
- Prototype:
  - `proposal_line(t)`, and the `PROPOSAL_RE` and `FINISHED_RE` patterns,
    now include the origin.
  - New `resolve_pair` restricts resolution to the named origin.
  - P-56, P-58 and P-60 were rewritten. P-58 now also checks that a line
    without an origin, or with an unknown origin, is not a proposal, and that
    the origin selects among same-name workflows.
  - New P-62 checks the finished line in the run text, including `bundled`
    for a shipped revision.
- Inherited, not fixed: the valid run_text example's `text_identity` and
  `text_bytes` are illustrative. They did not recompute from the example's
  lines before this edit either: I checked by recomposition, which gives
  985 bytes against the 812 recorded. They were left as they are.

**ROLE-v0.2**:

- §4.2 GS-7 is now "Proposal and finished lines". The shipped guidance states
  both exact lines. NIR §5.7 offers "End run" on the finished line, and
  "End ‹A› and start ‹B›" when both lines arrive together. The person's
  choice gives cause `completed`. The run text repeats both lines.
- The header names R20-9 (RX). An RX row is added.

**NIR-v0.2** §5.7:

- New RN-7: "End run" on the exact finished line naming the run in force,
  plus "End ‹A› and start ‹B›" when RN-3 also accepts a proposal in the same
  message. The press is DEF-4 with cause `completed`. The line itself ends
  nothing, and R18-5's rule applies.
- RN-4: the exception for a finished report is added.
- RN-6: records both forms as ruled (R20-5, R20-9), with their owners (ROLE
  GS-7; WR §16.2, TX-5).
- U-NIR-8 is marked ruled.
- An RX row is added to "Changes from v0.1", and a line to "Changes".
- The prototype was not changed (fence: NIR only), so RN-7 is designed and
  not prototyped.

### Item 2 — D3 and D5 round-2 joins for HOSTING and EXEC

| Join | Status before RX | Applied at RX |
|---|---|---|
| D3 J-H11 (supports FH-43) | FH-43 had recorded RT-10. R4 did not say why `already-resolved` matters | HOSTING §6.3 R4: Codex 0.158.0 silently ignores an answer made after its own resolution (OBS-2 O-3), so the register's refusal keeps the view honest. DEL-01-04 withdraws the controls (NIR §4.4 CS-6) |
| D5 J-28 (FH-40) | S-6 and §11 already applied by F-A. §8.2's first paragraph still named DEL-02-04 as the only composing owner | HOSTING §8.2: composing owners named per carrier. DEL-02-04 composes role guidance. DEL-02-02 composes the run-start text and the run-end line (WR §16.2) |
| D3 J-E2; D5 J-17 (FE-07) | J-E2 applied by F-B (CAP-1 multi-entry). J-17's wording missing | EXEC §5 CAP-2: adds "register workflow revisions" when one act registers several entries |
| D3 J-E8 (FE-13) | Applied by F-B (RC-4) | No change (checked) |
| D5 J-29 | A-3 cited WR-v0.2 without a section, and had the run starter keep the supply record and check | EXEC §2.6 A-3 now cites WR-v0.2 §16.2 (WR-FRAME-1) and §16.6. The supply evidence is DEL-02-02's `run_text` and `supply_check`, which RS R3 takes. The failure row is reported by DEL-02-02's check. The run-starter row (§2.7) hands over the run identity. The §2 table row follows |
| D5 J-30 | §6.1 *supplied* named "the run starter's per-run supply record" | EXEC §6.1 *supplied*: DEL-02-02's run text and supply check (WR §16.6), taken by RS R3, with HOSTING §8.2's per-turn record |
| D5 J-31 | RE-7 already had R20-1, one run at a time, and the prior-run citation | EXEC §4.9 RE-7 adds: the two exact lines with WR §16.5 PR-1…PR-5 and FN-1…FN-3 and NIR §5.7 (RN-3, RN-7), citing R20-5 and R20-9; RS-v0.9 `run_opened.follows`; the run-end line recorded and checked by DEL-02-02 (WR §16.2 TX-5, §16.6) |

The D3 and D5 items that target other files were not applied. They are J-A3,
J-R2, FG-02, J-21, J-32…J-36 and the parallel-node notes. Most belong to
F-C, F-D and F-E. J-36 (CA) is covered under item 3.

### Item 3 — citations "WR-v0.2 … run-start supply" become "WR-v0.2 §16"

- **HOSTING:**
  - Receivers line: "WR-v0.2 §16".
  - §2 table.
  - §8 S-6: §16.2, supply check §16.6.
  - §8.2: intro §16.2; the carriers row §16.2, TX-5 and §16.6.
  - §11 row.
  - F-15.
- **EXEC:** A-3, the run starter, the §2 table, RE-7, §6.1, the §9.1
  DEL-02-02 row and §10.
- **CA, beyond the item list.** The CA file is inside RX's fence. Its §4
  *supplied* row cited `WR-v0.2 "run-start supply"`; it now cites
  "WR-v0.2 §16, composition §16.2 and supply check §16.6".

**WD (read-only check; for F-E2).** `WORKFLOW_DECLARATION.md`, sha256
`a53a1be461ff634a8cde8089851c690015987052a7ee72a6d9e29ff98c3e1696`, still
cites the section by name:

| WD line | Text | Should read |
|---|---|---|
| L8 (inputs) | WR-v0.2 (its "run-start supply" section, §16 at reading …) | §16 (history line; may stay) |
| L63 (change table) | WR-v0.2 "run-start supply" (§16 at reading; F-E checks) | WR-v0.2 §16 |
| L549 (OS-7), twice | (WR-v0.2, section "run-start supply": framing WR-FRAME-1 …); (… WR-v0.2 "run-start supply", supply check; RS R3) | WR-v0.2 §16.2 (framing); §16.6 (supply check) |
| L572 (§3.9 (b)) | WR-v0.2 "run-start supply", agent proposals | WR-v0.2 §16.5 |
| L583 (§3.9 one run at a time) | … framing, WR-v0.2 "run-start supply" | WR-v0.2 §16.2 TX-5 |
| L1578 (§13 or verification row) | WR-v0.2 "run-start supply" (§16 at reading) | WR-v0.2 §16 |

Also for F-E2 or the integrator: WD §3.9 (a), lines 558–562, still says "when
the agent reports the workflow finished" without the R20-9 form
`Workflow finished: ‹origin›:‹name›`. WD is outside RX's fence.

### Item 4 — CA examples and the `run_w14_rehearsals.py` failure

**Investigation.** Before regenerating, I ran
`python3 -B prototype/run_w14_rehearsals.py --out …`: exit 1, "FAILED: 1
failure(s)". The only FAIL line was "w14-result-record.example.valid.json
validates and equals the regenerated W14-05 record (date aside)".

- A structural diff of the example against the regenerated W14-05 record
  shows three differences: `record_id` and `date` (expected), and
  `subject_of_run.files[4].sha256`, the pin of DEL-02-03's
  `prototype/run_all.py`. That pin changed from `42c0b496…` to `b770bb42…`;
  F-B changed the file under R20-2.
- F-C's report quotes `counts_toward_out003` and `not_counted_reason`. Those
  are the indented lines printed under the next check, and they are the
  **expected** three errors of the *invalid* example. They are not the cause
  of the failure.
- This agrees with F-C's own finding that the failure is not caused by RS,
  and with F-D's diagnosis.

**Regeneration.** At 2026-10-02T19:36:49Z I ran `--write-examples`, then the
same command without it:

- Both exited 0 with "ALL CHECKS HOLD: 0 failure(s)": 44 PASS lines and the
  same twelve records and outcomes (W14-00 1/2/0 … W14-10 not run).
- Diff of the valid example: only `record_id`, `date` and the `run_all.py`
  pin. The invalid example is derived from it.
- CA §8.5 gains a note, and "Changes from v0.6" gains an RX row.

**Caveat.** The example pins five prototype files: DEL-03-01 `simhost.py` and
`run_fixture.py`, DEL-03-03 `observe_map.py`, and DEL-02-03
`checkpoint_recorder.py` and `run_all.py`. F-E1 may change ADAPTER's
`observe_map.py`. At my last check (§4 below) none of the five had changed.
If any changes later, rerun `--write-examples` (F-E2 or the integrator).

### Item 5 — prototype reruns

Every prototype in the twenty Design folders was rerun; DEL-03-04 GUIDE has
no prototype.

- **Snapshot.** Runs used a scratch copy of the `PKG-0*` folders taken at
  2026-10-02T19:38:38Z, after all RX edits. The `git status` at that moment
  listed RX's files, F-E1's four docs and `F/F-E1.md`, and no prototype file
  of F-E1. The copy keeps outputs that some prototypes write (for example
  DEL-01-03 `fixtures/native`) out of the repository.
- **After the runs**, `diff -rq` between the copy and the working tree showed
  no difference. So no run produced bytes different from those committed,
  and nothing changed in the tree during the runs.
- **Exception, DEL-02-01.** `wdproto.py selftest` reads the Root
  `workflows/create-workflow/WORKFLOW.md`, which is outside the copy, so it
  ran in place. It writes only to a temporary directory.
- **Environment.** Python 3.13.7, node v24.5.0, Darwin 25.6.0 arm64.
  `PYTHONDONTWRITEBYTECODE=1` and `-B` were used.

| Folder (Design/…) | Command (in `prototype/` unless noted) | Result |
|---|---|---|
| DEL-01-01 HOSTING | `python3 -B run_cases.py` | exit 0; TOTAL 35, pass (model) 35, FAIL 0 (VC-27 tables and VC-30 account hold after RX's HOSTING edits) |
| DEL-01-02 RECOVERY | `python3 -B run_cases.py` | exit 0; 16 results, 16 as expected |
| DEL-01-03 NPTD | `python3 -B run_cases.py` | exit 0; SUMMARY 18/18 cases gave their expected result |
| DEL-01-04 NIR/AAC | `python3 -B run_cases.py` | exit 0; 119 checks, 0 failed (K-16: 9 RS entries valid against RS_RECORD `2ff3f07873d00c2a`) |
| DEL-01-05 ACCESS | `python3 -B run_cases.py` | exit 0; TOTAL 9, FAIL 0 |
| DEL-02-01 WD | `python3 -B wdproto.py selftest` (in place) | exit 0; 62 checks, 62 passed (S-11: 10 names to HOSTING §8.4 groups, 27 groups) |
| DEL-02-02 WR | `python3 -B wrproto.py` (copy, and in place at 19:31Z) | exit 0; **95 checks, 95 passed, 0 failed** (was 92; new INV-16, INV-17, P-62) |
| DEL-02-03 EXEC | `python3 -B run_all.py` | exit 0; "ALL CHECKS HOLD: 0 failure(s)", 116 lines; output sha256 `2e2a275737c1e529…`, identical to F-B's round-2 output |
| DEL-02-04 ROLE | `python3 -B run_cases.py` (no `--record`) | exit 0; TOTAL pass=36 fail=0 |
| DEL-03-01 C | `python3 -B run_fixture.py --out $SH`; `python3 -B validate_all.py --run $SH` | exit 0, 22 of 22 checks passed; exit 0, "RESULT: all checks passed" |
| DEL-03-02 P | `python3 -B proposal_states.py --check $SH` | exit 0; "RESULT: all checks passed" |
| DEL-03-03 ADAPTER | `python3 -B observe_map.py --run $SH` | exit 0; "RESULT: all checks passed" |
| DEL-03-04 GUIDE | — | no prototype folder |
| DEL-04-01 ACT | `python3 -B validate_policy.py` | exit 0; "RESULT: all expectations held" |
| DEL-04-02 AS | `python3 -B validate_settings_in.py` | exit 0; "RESULT: all expectations held" |
| DEL-04-03 RS | `python3 -B run_prototype.py <scratch>`; `python3 -B exec_to_rs.py <scratch>` | exit 0, 63 PASS, "all expectations held"; exit 0, 40 of 40 written and valid |
| DEL-05-01 LOOP | `python3 -B assemble_tool_calls.py`; `python3 -B destination_flow.py`; `python3 -B schema_subset.py ../LOOP_TOOL_CALL.*` and `../LOOP_DESTINATION_REQUEST.*` | exit 0, 22/22 cases as expected; exit 0, 68 RS entries and 11 loop request records validated, "all expectations held"; schema checks exit 1 **by design** (README: exit 1 whenever an instance given is invalid): VALID for valid, INVALID for invalid |
| DEL-05-02 PANEL | `python3 -B panel_double.py`; `python3 -B schema_subset.py ../PANEL_RETURN_INPUT.*` | exit 0, 4/4 scripts as expected; schema check exit 1 by design, VALID and INVALID as expected |
| DEL-09-06 CA | `python3 -B prototype/run_w14_rehearsals.py --out <scratch>` (from `Design/`) | exit 0; 44 PASS, "ALL CHECKS HOLD: 0 failure(s)" (after item 4's regeneration) |
| DEL-09-09 XT | `python3 -B prototype/run_xt_suite.py --out <scratch>` (from `Design/`) | exit 0; 59 PASS, "ALL CHECKS HOLD: 0 failure(s)"; the four XT examples still equal their regenerated instances |

`$SH` is one SH-1 run directory shared by the four DEL-03 commands, as
DEL-03-01's README describes. Full outputs are kept in scratch only.

## 2. Items not done, and residuals found (not fixed: outside the items or the fence, or a design choice)

1. **WR PR-4 against NIR RN-4.** When a proposal arrives with no finished
   report while a run is in force:
   - WR PR-4, and its prototype `offers`, offer "End ‹A› and start ‹B›".
   - NIR RN-4 shows "Start ‹workflow› — end run ‹A› first", disabled.
   - R20-1 rules only the finished-report case, where both files now agree.
   This needs an integrator choice.
2. **Where the proposal line may appear.** WR PR-1 requires the last
   non-empty line, and FN-1 one of the last two. NIR RN-3 accepts "exactly
   one line" anywhere in the message. R20-9 fixes only the forms, so the
   placement rule differs between the two files.
3. **The supply check's *unreadable* state.** WR §16.6 SC-4 reads every
   state except *verified* as "supplied — not verified". EXEC A-3 and §6.1
   read `thread/read` unavailable as *supplied* **unknown**.
4. **The cause recorded for "End ‹A› and start ‹B›".** On a selection while A
   is live, EXEC RE-7 records cause "ended to start ‹B›". WR CH-1 records
   A "ended by the person" (and the chain line's `ended` enum has only *ended
   by the person* and *completed*).
5. **Stale R17-8 references in WR, not in the RX items.** The header's
   Receivers line still lists "DEL-02-04 through the row R17-8 proposes",
   and the §1 table row R17-8 says DEL-02-04 composes the workflow. R19-7
   dropped that row and R19-1 superseded the composition.
6. **NIR §5.8 CA-2 against R20-6.** R20-6 says the App asks the source
   agent, in a visible turn, to draft the handoff summary. CA-2 still offers
   that only as the person's own option, and U-NIR-9 is not marked ruled.
   This was not in RX's items.
7. **WD citations and §3.9 (a) wording** (item 3 table above). These are WD's,
   for F-E2 or the integrator.
8. **CA example pins** may need regenerating again if F-E1 changes a pinned
   prototype (item 4 caveat).

## 3. sha256 of files written

| File | Before RX | After RX |
|---|---|---|
| `PKG-02…/DEL-02-02…/Design/WORKSPACE_AND_REGISTRATION.md` (WR-v0.2) | `1a7b3cbd0c4167a658313864bfbf0c58582ef1eebe84a35444bd9d9f58786110` | `ecf85cd94275e21a5600021fcb8b5f2d66e605b67f3040a0be293a8c88e1bc53` |
| `…/DEL-02-02…/Design/workspace-registration.schema.json` | `98197077f6081edbd99a08da1837dce02b67ddb06497fb073d3c34885fbfbc27` | `28488f5172013e03f7af58a48edf96d880baa17bfc236cc1749f52ab45ba5e45` |
| `…/DEL-02-02…/Design/workspace-registration.valid.examples.jsonl` | `fe4a0e955a47e3336b3053825d17530bc2863d2243179f819d0ec27c4bac0c2b` | `81fcf8cf5f81e5059b5c4e22cc47bbf3a2d43622fe87551a50b4ae14dfeae7b7` |
| `…/DEL-02-02…/Design/workspace-registration.invalid.examples.json` | `3d866acca8bdcb5f4694cf1f21176d140e21866f157ef8b3f06c750102728fbb` | `6c1d05a7f2f2be532aab86a79250ee03442b403e88e8751059143a838ed31429` |
| `…/DEL-02-02…/Design/prototype/wrproto.py` | `6b61c172c666582c278fdb4edcc4d69e53ddbb87c4c805fd49634e4b753897d5` | `46ec3d12ddeecae02fca54585bdba2f3f25c2d0c4527c79e873f24d032cec1bb` |
| `PKG-02…/DEL-02-04…/Design/ROLE_SUPPLY.md` (ROLE-v0.2) | `b7e073b4de7fb28d9c290a0bfbbeebc21ede23dfcfd560d6574d6b2f1b298863` | `ec345158db604fdca27cfbd821a22242a3e8f8d09129b9c1d455e7f185347035` |
| `PKG-01…/DEL-01-04…/Design/NATIVE_INTERACTION_RECEIVING.md` (NIR-v0.2) | `ca9d31e4aba7e6ba3a25b6066061fc949a750f710bbb7d9fb7a60ac7ac8cd820` | `7133abcee034ecd9d0267df5da6d91babb5bc836d252765f21ae4a580360ba3e` |
| `PKG-01…/DEL-01-01…/Design/HOSTING_BOUNDARY.md` (HOSTING-BOUNDARY-v0.9) | `77df7c12f7d5e1eec916ae603f261944c5e95731f8470266b9b9a1879ea97c81` | `a4619e33f83886cbf98a6fd632ab2281454c38bb1a693649f979b8490e0f51a6` |
| `PKG-02…/DEL-02-03…/Design/EXECUTION_COMPATIBILITY.md` (EXEC-v0.7) | `70120eb1987b5e5fca298eb23888fc77e50600db059dacc56a41fa3e3892a086` | `3188d23e4815acf830c8c4af84d63519107c37f909c672fd1298fb6f844fe729` |
| `PKG-09…/DEL-09-06…/Design/CONNECTED_ACTIVITY_CONTRACT.md` (CA-v0.7) | `7eda8d31e2fa81703e405fd9e7ba7a30825c283572030e3e190c7f46048b5303` | `148687e71fd8a464952b096e868e9f7615a3d6e849b8ecc050744746a3811b5a` |
| `…/DEL-09-06…/Design/w14-result-record.example.valid.json` | `c9d5c19830b45aa76fbe28f279b7a61a5ede7c9abdba1d128486f8799c91dc31` | `1997107397a444b46e7fa922739e70899f8980544c895ce43bfe6b3dbb9364c9` |
| `…/DEL-09-06…/Design/w14-result-record.example.invalid.json` | `dd6e6ace452ea01dddb55e7967d8faafa377730c6d7965fd375eb6517cca47ed` | `0c28e970792b7a45edd96bd231f41a65421fdfaac755e2aca528cc63c7d87613` |
| `F/RX.md` (this file) | — | reported in the hand-back |

## 4. Last check before return

At 2026-10-02T19:43:36Z I recomputed the five files the CA valid example
pins (`simhost.py`, `run_fixture.py`, `observe_map.py`,
`checkpoint_recorder.py`, `run_all.py`). All five equal the example's pins.

`git status` then showed `wrproto.py` as the only modified prototype file,
and that one is RX's. F-E1 had changed no prototype file. No `__pycache__`
was present under the execution root.

---

# RX2 — residual sweep 2 (2026-10-02)

- **Brief:** HELP_HUMAN's message after RX was committed at `a8eb3765be`.
- **Rules:** in place, no version steps, an "RX2" row in each touched file's
  change table.
- **Fence:** WR; NIR and the DEL-01-04 prototype; EXEC; ROLE; RS (the
  `RECORD_SEMANTICS.md` file only); WD (the `WORKFLOW_DECLARATION.md` file
  only); CA only if a pinned file changed. None did, so CA was not touched.
- **Binding:** `R20_RESOLUTIONS.md` R20-11 (sha256 `b52e0347ad91ba42`) and
  R20-6.
- **Limits:** read-only git; no network; no Codex or model run.
- **How I edited and checked:** exact-once scripted replacements; table
  column counts compared before and after (no new mismatched row); no
  `__pycache__` left.

## RX2.1 Items done

**1. R20-11, all four rulings.**

- **(1) A proposal during a run.** It is offered only as "End ‹A› and start
  ‹B›". A plain "Start ‹B›" is offered only when no run is in force.
  - WR: CH-1 and PR-4.
  - NIR: RN-3; RN-4 is rewritten so the one step is enabled.
  - EXEC: RE-7, the "sequential" bullet.
  - ROLE: GS-7.
- **(2) Where the lines sit.** The proposal line is the message's last
  non-empty line. The finished line is the last non-empty line, or the line
  immediately before the proposal line. Each appears at most once.
  - Placement and the at-most-once rule are in WR PR-1 and FN-1, NIR RN-3,
    RN-5 and RN-7, EXEC RE-7, and WD §3.9.
  - The run text and ROLE GS-7 tell the model the placement. So WR §16.2's
    third framing line now says to end the message with the finished line,
    and to put it just before the proposal line when both are written.
  - Following from that, the schema pattern, the example lines and the
    prototype's `proposal_line()` all changed.
- **(3) An unreadable supply check.** The reading is "supplied — not
  verified": the App observed its own send, and Codex's copy could not be
  read.
  - WR SC-4.
  - EXEC: A-3's failure cell (was *supplied* **unknown**) and §6.1's
    *supplied* row.
  - RS R3: one sentence added stating the reading. The recorded `supplyCheck`
    value stays WR's state, so the schema is unchanged.
- **(4) The cause for "End ‹A› and start ‹B›".** It is "ended to start ‹B›",
  EXEC's wording, which WR now records as well.
  - WR: CH-1, CH-2 and FN-2. The chain line's third cause is added in §16.2
    and in the schema (chain-line pattern, and the two `ended` value lists).
  - NIR: RN-4.
  - EXEC: RE-7 cites R20-11 (4).
  - **My reading:** on a finished report the cause stays *completed* (R20-1),
    as EXEC RE-7 already says. R20-11 (4) is read as adopting EXEC's wording,
    which keeps *completed* for that case.

**2. WR's stale R17-8 references.**

- The header Receivers line no longer lists DEL-02-04. It now notes that R19-7
  dropped the row.
- The §1 row now reads "R17-8 as amended by R19-1, R19-7": role guidance only,
  with the workflow supplied per run by DEL-02-02 (§16).

**3. NIR §5.8 CA-2 and U-NIR-9 (R20-6).**

- CA-2: the App asks the source conversation's agent, in a visible turn
  there, to draft the handoff summary. The person edits it in the new
  conversation under one App header that names the source; the header gives
  no instruction. Nothing is sent until the person sends it.
- PROPOSED fallback: if the source turn fails, the composer holds the header
  only.
- U-NIR-9 is marked ruled.

**4. WR run_text example with real identities.**

- New fixture `prototype/fixtures/review-pack/WORKFLOW.md`, the prototype's own
  review-pack body (85 bytes), plus `resources/checklist.md`.
- In the valid examples, these values are now computed from the fixture:
  - the `workflow_file` content and size, `other_files`, and the
    `files_line` digest;
  - `text_identity` = `ac3f264b52a0…`, with `text_bytes` 1149;
  - the end-notice record's `text_identity` and `text_bytes`, which were
    illustrative too;
  - the supply-check example's expected, observed and workflow identities.
- The invalid examples' copies carry the same values.
- New check P-63 recomputes all of these from the lines and the fixture bytes.
- Also new: P-64, for R20-11 (1) and (4) through a new `end_and_start`, and
  P-65, for R20-11 (2).

**5. WD.**

- The six citations from the RX table now give the section number: L8 and L63
  (§16), L549 (§16.2 and §16.6), L572 (§16.5), L583 (§16.2 TX-5), L1578 (§16).
  Line numbers are from before the edit.
- §3.9 (a) gains `Workflow finished: ‹origin›:‹name›` with its placement.
- §3.9 (b) gains the placement and the during-a-run rule.
- An RX2 row is added to "Changes from v0.8". No declared-part meaning
  changed. The only remaining "run-start supply" string in WD is the quote
  inside that row.

**6. CA.** No CA example pins a file that RX2 changed. CA pins
`simhost.py`, `run_fixture.py`, `observe_map.py`, `checkpoint_recorder.py` and
`run_all.py`, and all five still equal their pins (rechecked after the rerun).
Nothing was regenerated.

## RX2.2 Prototype reruns

- **Snapshot:** all prototypes ran on a scratch copy of the `PKG-0*` folders
  taken at 2026-10-02T19:57:17Z, after every RX2 edit. Afterwards,
  `diff -rq` between the copy and the working tree showed no difference.
- **Where the copy differs:** WD's self-test reads the Root `workflows/` folder,
  which is outside the copy, so it fails there by construction. The result
  below is from the in-place run.
- **Environment:** the same Python, node and host as in RX.

| Folder | Result (commands as in RX §1 item 5) |
|---|---|
| DEL-01-01 HOSTING | exit 0; 35/35 |
| DEL-01-02 RECOVERY | exit 0; 16/16 |
| DEL-01-03 NPTD | exit 0; 18/18 |
| DEL-01-04 NIR/AAC | exit 0; **120 checks, 0 failed** (was 119). O-11 and O-12 rewritten, O-13 new. Recorded in `prototype/results/RUN_2026-10-02_RX2.txt`; NIR §13.2 and the README note it |
| DEL-01-05 ACCESS | exit 0; 9/9 |
| DEL-02-01 WD | in place: exit 0; 62/62 (S-11 holds) |
| DEL-02-02 WR | exit 0; **98 checks, 98 passed, 0 failed** (was 95). New P-63, P-64, P-65; P-37 has 137 records conforming |
| DEL-02-03 EXEC | exit 0; "ALL CHECKS HOLD: 0 failure(s)"; output byte-identical to RX's run |
| DEL-02-04 ROLE | exit 0; pass=36, fail=0 |
| DEL-03-01, DEL-03-02, DEL-03-03 | exit 0; 22/22; "all checks passed" (×3) |
| DEL-04-01 ACT, DEL-04-02 AS | exit 0; "all expectations held" |
| DEL-04-03 RS | exit 0; 63 PASS; `exec_to_rs` 40/40 |
| DEL-05-01 LOOP | exit 0; 22/22; destination flow "all expectations held" |
| DEL-05-02 PANEL | exit 0; 4/4 |
| DEL-05-01, DEL-05-02 schema checks | exit 1 by design: VALID for the valid example, INVALID for the invalid one |
| DEL-09-06 CA | exit 0; 44 PASS, 0 failures |
| DEL-09-09 XT | exit 0; 59 PASS, 0 failures |
| DEL-03-04 GUIDE | no prototype |

## RX2.3 Not done and residuals

- **No schema change in RS.** R3's recorded `supplyCheck` keeps WR's state
  values, and the reading is stated in text.
- **Wording that stays PROPOSED:**
  - the request text that CA-2's source turn sends;
  - the header-only fallback;
  - the "End ‹A› and start ‹B›" button label.
- **Reading to confirm:** the R20-11 (4) and R20-1 reading above (*completed*
  on a finished report).
- **WR §8 receiver cells, not changed.** `library_entry` and
  `selection_record` still list DEL-02-04 as a receiver; only the header and
  the §1 row were in scope.

## RX2.4 sha256

| File | Before RX2 | After RX2 |
|---|---|---|
| WR `WORKSPACE_AND_REGISTRATION.md` | `ecf85cd94275e21a5600021fcb8b5f2d66e605b67f3040a0be293a8c88e1bc53` | `f1ca71b92bdc5e26757234f6f3adda1a9407e87f6fc188f23a6b9b905ce22424` |
| WR `workspace-registration.schema.json` | `28488f5172013e03f7af58a48edf96d880baa17bfc236cc1749f52ab45ba5e45` | `61ebfe86f973b87da0fb72e43dbea71f652256587233e7c52b35480b4bbf13d4` |
| WR `workspace-registration.valid.examples.jsonl` | `81fcf8cf5f81e5059b5c4e22cc47bbf3a2d43622fe87551a50b4ae14dfeae7b7` | `9b21cc8b5860c4b312ab0a8f091fff394b0db86368e199d34b472e7828e1b063` |
| WR `workspace-registration.invalid.examples.json` | `6c1d05a7f2f2be532aab86a79250ee03442b403e88e8751059143a838ed31429` | `2a2f2afccd9f6d11391228e738587a77406bc6c9857ea1ad467d88797b863866` |
| WR `prototype/wrproto.py` | `46ec3d12ddeecae02fca54585bdba2f3f25c2d0c4527c79e873f24d032cec1bb` | `3c79e72b671a16589591023e0ad6a1935ff04d33ae955cbefa4c3d1eaa7ea9d4` |
| WR `prototype/fixtures/review-pack/WORKFLOW.md` (new) | — | `d7d8b6e0d5989b431dc22b51b72acad90cac2825bd1efc070a37c9e4f8e08088` |
| WR `prototype/fixtures/review-pack/resources/checklist.md` (new) | — | `c989b2391e00effe3c225b9dee35e27d7a40a47fe40563e8efe2185bb6ec8a70` |
| ROLE `ROLE_SUPPLY.md` | `ec345158db604fdca27cfbd821a22242a3e8f8d09129b9c1d455e7f185347035` | `45a748697cf8fca8625a6927417647a30f90e60e0c3020f93fd22bcfc4cd2f3a` |
| NIR `NATIVE_INTERACTION_RECEIVING.md` | `7133abcee034ecd9d0267df5da6d91babb5bc836d252765f21ae4a580360ba3e` | `d56830e7274be4d2fb814b7d93b405f9b4093f59626c0533d2d5a818bb2b2f2f` |
| DEL-01-04 `prototype/nir_model.py` | `2b040e01277ab69c06c296cf10df28038307a88aff3cd8239e20391d4ba09575` | `83085f636ff804d9cc496259b8b46e82efee1b83202b09bb9bf2913ff8cbaaad` |
| DEL-01-04 `prototype/run_cases.py` | `c4c9c8474ecfaf4786c579cb9a53cb65854eed6692452c01d08513c1e2a57346` | `48607363eb9642661ce32efd91f0128cd479350e065e66e5ac9fb719f9127d74` |
| DEL-01-04 `prototype/README.md` | `a63a0004049851594097931b9fbd97ecc0441c9d0349d14c4a3bebbfadb03665` | `650cbca5dc02bd0f8be542c65b5efb8182226e83302be25494501a60b2397369` |
| DEL-01-04 `prototype/results/RUN_2026-10-02_RX2.txt` (new) | — | `a81c7a9705f06870fc5f8c39db48dda6e95ba67ab18c3c80f1f632f8aae347ed` |
| EXEC `EXECUTION_COMPATIBILITY.md` | `3188d23e4815acf830c8c4af84d63519107c37f909c672fd1298fb6f844fe729` | `8337b1d594292d16d93785263cb38462c34f54eb47443ea5566e2b9dff49bc2a` |
| RS `RECORD_SEMANTICS.md` | `d523dc9e679701eb9eea7495f1da4d909a4c71915be324595a139ec488204ec3` | `6c6408d8c10a9a7e5aea0c6a5fe91e30374cf99ef9f919983cdafafb3818739f` |
| WD `WORKFLOW_DECLARATION.md` | `a53a1be461ff634a8cde8089851c690015987052a7ee72a6d9e29ff98c3e1696` | `b1a647290b966f1bb97697ad435650ba76e29cfd3fd39ee160e58cf076742e9f` |
