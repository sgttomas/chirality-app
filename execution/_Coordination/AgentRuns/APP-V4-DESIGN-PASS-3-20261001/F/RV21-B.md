# RV21-B — repairs from V21 to the first-increment files (design pass 3)

- Run `APP-V4-DESIGN-PASS-3-20261001`, node **RV21-B**. Executor: Type 2 TASK
  (Claude Opus 5.5, high effort), dispatched by the HELP_HUMAN session; does
  not delegate. Written 2026-10-02.
- Brief: BRIEFS.md "RV21", row RV21-B. Binding: R21-1…R21-4
  (R20_RESOLUTIONS.md), R17…R20, OWNER_DECISIONS.md, review `reviews/V21-B.md`.
- Boundary kept: read-only git, no network, no Codex or model run. Written
  only inside the fence: HOSTING, EXEC and its prototype, WD, WD-EX, GUIDE
  content (not its pins), RS and ACT (each for one finding), and the one
  next-relay row of DEL-09-06 `RELAY_QUESTIONS_SWBPIPE.md`. Not touched: the
  six new Design folders (RV21-A works there in parallel), `OBS_*`,
  `PIN_SPIKE_*`, `generated/`, `RELAY_ANSWERS_*`, `FACTS_*`, RELAY §0–§3,
  ScopeOfWork, registers, `_STATUS.md`. Scratch: `$TMPDIR/rv21b`.
- In place, no version steps; an "RV21" row in each touched file's change
  table naming the findings, except RELAY (see m-2).
- Paths are relative to `projects/chirality-app-v4/execution`.

## 1. Findings fixed

| Finding | Files and places | What changed | How checked |
|---|---|---|---|
| **M-1** (R21-1) | EXEC §3.4 EV-3a `agent-delegation` row and closing note; EXEC D round 2 (J-5) row corrected; §7.4; `prototype/required_tool_check.py` `_delegation` and `harness_presence`; `prototype/run_all.py`; `prototype/README.md`; WD §4.2.5 standing cell; HOSTING §8.4 HCG-A08 (one sentence); GUIDE M8.3 | Readings in R21-1's order: `multiAgentVersion` `disabled` → missing; effective `features.multi_agent = false` → missing; `namespaceTools` false → missing; any of the three not read (or the version null) → not established; otherwise present. Each *missing* reading decides even when another signal is not read. `namespaceTools` false is now *missing* in EXEC and WD (was *not established* with a delegation limit in EXEC; WD's "otherwise not established"). The prototype's two delegation readings became ten (present; `disabled` with and without other reads; `multi_agent = false` with and without; `namespaceTools` false with and without; config, capabilities and version each not read). A version outside the 0.158.0 enum reads not established, as NPTD's prototype does. EXEC's J-5 row ("confirmed … no further change") carries a correction note | Exhaustive scratch comparison (`$TMPDIR/rv21b/cmp.py`) of EXEC `harness_presence` against NPTD `delegation_availability` over 4 version × 4 configuration × 4 capability readings: 62 of 64 agree. The two others: configuration **not read** with v1/v2 and `namespaceTools` true. R21-1 ("any of the three not read → not established") and NPTD §7.1's text ("a value not read … → not established") give not established; NPTD's prototype gives present, because its `effective_features=None` is taken as "nothing set". Returned below (§3) |
| **M-2** | GUIDE M8.1; §5 "R20-1, R20-7" row | `WD-v0.9` → `WD-v0.8` as the declared-part value (R20-7; WD §3.3). M8.1 adds that a declaration naming `WD-v0.9` reads as an unknown version (WD-EX E9 L-WDEX-33a) | Scan of every backticked `‹LABEL›-v0.N` token in GUIDE: only `WD-v0.8` (rows 97, M8.1, §5) and the two in the new RV21 row remain; no other value token found. GUIDE's pins were not touched |
| **m-1** | WD §13.1; WD-EX "Verification cases" paragraph | Both record that the 61-of-62 S-11 result was overtaken by R20-8 (HOSTING-BOUNDARY-v0.9 has no HCG-A18) and give the rerun: 62 of 62 | `grep -c HCG-A18` in HOSTING: 0. `wdproto.py selftest` rerun after all WD and HOSTING edits: 62/62, S-11 "27 groups read from HOSTING" |
| **m-2** | DEL-09-06 `RELAY_QUESTIONS_SWBPIPE.md` UNRESOLVED, the "Items a successor relay must carry" row only | Item (6) added: host plan billing, NR-L1, worded from LOOP-v0.9 §13 NR-L1 (information for the host owner, not a requirement; no decision asked), citing LOOP-v0.9 §13 NR-L1, ACCESS-v0.2 §11 CH-8 and R19-4, and saying in the row that RV21-B added it in place (App metadata only, §0–§3 untouched) | §0–§3 span sha256 (from `## 0.` to before `## 4.`) `6e399c8389dc…0d4d` before and after, the value RELAY's earlier rows record. `diff`: one line changed (l.1141). No change-table row was added: the brief limits this edit to that one row, so the row carries its own provenance (§3) |
| **m-5** | HOSTING §4.2 step 3 | "carry only the K-12 traffic settings" → the K-12 settings and, if ROLE U-R3 selects `-c` session flags as the child-role carrier, the additive `agents.<ROLE>.*` entries of §8.2; never a credential | Read against HOSTING §8.2 ("Per-thread `config` from role supply") and ROLE U-R3 |
| **m-6** | HOSTING §8.4 goals note | "(NPTD-v0.2 §6.4 TA-5)" → "(NPTD-v0.2 §6.4; §9 TA-5)" | NPTD: §6.4 Goals at l.331; TA-5 at l.474 inside §9 (l.462) |
| **m-8** | HOSTING Receivers line, §8 S-1 row, §13 F-15 | S-1's receiving side cites RECOVERY-v0.2 §1 (reconciliation with §6.5) and §4.2 (consumed), replacing "§1 (receiving comparison)" and bare "§1" | RECOVERY §1 holds "Reconciliation with HOSTING §6.5"; §4.2 "Consumed" has the DEL-01-01 (HOSTING S-1) row. HOSTING's other three "RECOVERY-v0.2 §1" citations (FH-04 row, §6.5, U-14) cite the reconciliation and were left |
| **m-10** | WD §3.9 (a), (b); EXEC §4.9 RE-7 | WD: "the message's last line" → "last non-empty line" in (a) and (b), and "just before its proposal line" → "the one immediately before its proposal line" (R20-11 (2)); (b) offers "Start ‹workflow› (proposed by the agent)" with no run in force, citing EXEC RE-7 and NIR §5.7 RN-3. EXEC RE-7's agent-proposal offer reads "Start ‹workflow› (proposed by the agent)" (R20-5) with no run in force | NIR-v0.2 §5.7 RN-3 already shows **"Start ‹workflow› (proposed by the agent)"** when no run is in force; R20-5 gives the same words |
| **m-9 row 9** (F-E2 §4.3) | HOSTING §6.1 (decline-form sentence) | "(NIR-v0.2 §4.3 DM-1…DM-6, §6.2.1 RT-08)" → "(NIR-v0.2 §4.3 DM-1…DM-6; this file's §6.2.1 RT-08)" | NIR has no §6.2.1 heading; RT-08 is HOSTING §6.2.1's row |
| **m-9 row 10** | ACT §2.6 (App-content row) | "until SCA-V4-003 carries SC2-01-04-1" → "… SC2-01-04-1 as amended by SC3-01-04-1, D3 §5" (GUIDE's and EXEC's naming). FA-01 keeps the words then used | D/D3.md §5 (Proposals for SCA-V4-003) row SC3-01-04-1 "amends SC2-01-04-1" |
| **m-9 row 11** (my fence only) | EXEC §2.4.2, §4.4, §4.9 (LOOP-v0.8 §2.3 E-8 ×3); HOSTING §6.7 (EXEC-v0.5 §2.3 HP-2); RS §4 R1, R11, R15, §8 (×2), §14.1, §15, VC-38 | Labels moved to LOOP-v0.9 / EXEC-v0.7. RS: all nine body citations of LOOP moved, not only F-E2's two (l.318, l.329), so one table does not mix labels; kept as provenance: RS header "from v0.8 (node B5)", §4.4 "Elements added in v0.8", §13's example origin, change-history rows. HOSTING "the group set WD-v0.8 §4.2.5 resolves against" kept (deliberately the v0.8 set, F-E2) | `git diff a38617d08b` of LOOP: pass 3 changed only the header, change table, §1's model-interface row, a new next-relay paragraph and two appendix rows; §2.3 E-8, §3.1, §3.2, §5.2, §5.3 are unchanged, and every cited ID (E-8, F-2, MS-02, DF-1, DF-5, Q-3, DF-6, DF-7, DF-10) is present. EXEC-v0.7 §2.3 still has HP-2 "Not adopted" (l.489) |

RV21 change-table rows were added to HOSTING ("Changes from v0.8"), EXEC
("Changes from v0.6"), WD and WD-EX ("Changes from v0.8"), GUIDE ("Changes
from v0.5"), RS ("Changes from v0.8") and ACT ("Changes from v0.8").

## 2. Not fixed, with reason

| Item | Reason | To |
|---|---|---|
| m-9 row 7: WR `workspace-registration.schema.json` `selection_record` description still names DEL-02-04 | In DEL-02-02's Design folder, RV21-A's fence | RV21-A or the integrator |
| m-9 row 11, label lags outside this fence: AAC l.84, l.111, l.165; NIR l.130, l.187, l.573; ROLE l.64; ACCESS l.891 (F-E2 line numbers) | RV21-A's folders | RV21-A |
| m-9 row 11: CA l.717 (RS-v0.8 L-13; EXEC-v0.6 CH-31) | CA is DEL-09-06; this fence holds only RELAY's next-relay row there | DEL-09-06 owner |
| m-3, m-7 | Not in this node's list (run records: OWNER_DECISIONS and DISPATCH are the integrator's; OWNER_DECISIONS already carries the m-3 correction) | Integrator |
| M-3, m-4, m-11 | RV21-A's (R21-3, R21-4) | RV21-A |

## 3. Consequences outside this fence (returned)

1. **CA's W14-05 example pin of EXEC `run_all.py` is now stale.**
   `run_w14_rehearsals.py` (DEL-09-06) pins `prototype/run_all.py` of
   DEL-02-03 in the regenerated W14-05 record and compares it with the
   committed `w14-result-record.example.valid.json`. With `run_all.py`
   changed for M-1 the rehearsal exits 1 with one failure: "example.valid.json
   validates and equals the regenerated W14-05 record". I checked the
   difference field by field: the only one is
   `/subject_of_run/files/4/sha256` `b770bb42…adc3` → `3fc0d650…f4ae`.
   Repair (DEL-09-06, outside this fence): in DEL-09-06 `Design/`,
   `PYTHONDONTWRITEBYTECODE=1 python3 -B prototype/run_w14_rehearsals.py --out <scratch> --write-examples`,
   then a CA change-table row as RX did (CA l.858 records the previous
   regeneration). I did not do this, because the brief limits the DEL-09-06
   fence to the RELAY row. Keeping `run_all.py` unchanged would have required
   treating "configuration not read" as "nothing set", against R21-1.
2. **NPTD prototype, one edge (for RV21-A / DEL-01-03).**
   `npt_model.delegation_availability` treats an unread configuration
   (`effective_features=None`) as "nothing set" and returns present for
   v1/v2 with `namespaceTools` true. R21-1 and NPTD §7.1's own text read
   not established. These are the only 2 of 64 combinations where it differs
   from EXEC's prototype. NPTD is the reference and was not touched.
3. **LOOP-v0.9 §13** still says "adding NR-L1 there is DEL-09-06's", and
   `_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` (l.106) still says the full
   list is RELAY's row and then lists plan billing separately. Both are now
   true as written and need no change. Their owners may want a pointer to
   item (6).
4. **RELAY has no change-table row for item (6).** The brief allows only
   that one row, so the row records its own provenance (RV21-B, V21-B m-2,
   §0–§3 untouched). If the integrator wants a RELAY change-table row as at
   R16-3, it is one line outside this fence.
5. **GUIDE re-pin (the following node).** B8's `pins.py`
   (`$TMPDIR/b8/pins.py`, sha256 `b943319d…5423`, unchanged), run
   **check-only** at this node's end: 17/25 match. The rows that differ are
   ACT, RS, WD, WD-EX, EXEC, HOSTING and RELAY (this node's) and AAC
   (RV21-A's, in progress). GUIDE's own bytes also changed (M8.1, M8.3, §5,
   change table).

## 4. New sha256 (`shasum -a 256`, final bytes of this node)

| File | Before (HEAD `6185de63da`) | After |
|---|---|---|
| DEL-01-01 `Design/HOSTING_BOUNDARY.md` | `a4619e33f838…51a6` | `bcad280f204172385367f21f5cbf7c978da1a1984ccce28f5b8240174c2d8301` |
| DEL-02-03 `Design/EXECUTION_COMPATIBILITY.md` | `8337b1d59429…bc2a` | `fa8226c60417fb8c011a67111f1e0fb13338230ac384805addefcfcf6e9033b5` |
| DEL-02-03 `Design/prototype/required_tool_check.py` | `defa897000b5…3569` | `3d889b5477535c8973c83e1bf83ac3ceb9390648d3b2450109ae235faf88f0c7` |
| DEL-02-03 `Design/prototype/run_all.py` | `b770bb42d409…adc3` | `3fc0d650f5cdb3c5d6adf350664164a1eb5c3e2cacf69e1d2a7ffc005dbff4ae` |
| DEL-02-03 `Design/prototype/README.md` | `99ed803f6ec9…4df7` | `03d53193f8ff31e466ebc89671344db24008bccc048ec1797bc44ba54f34c826` |
| DEL-02-01 `Design/WORKFLOW_DECLARATION.md` | `b1a647290b96…2e9f` | `1abe72e3f546676cd73308f9d349ad164462a3bd9bf6114ed0a8874be0664e18` |
| DEL-02-01 `Design/EXAMPLES.md` | `50efea247c08…3c7d` | `85fa5a3f9200cef893789165515eafe8aff653f6357135cf7575c6eacd83a361` |
| DEL-03-04 `Design/HOST_INTEGRATION_GUIDE.md` | `15e43dc1aeeb…3644` | `017849e4790b5ed99bef5587ff672101979694d16e2a8a8d48453f3de3b5e248` |
| DEL-04-01 `Design/ACT_AND_POLICY_CONTRACT.md` | `3d9f3ee2c9e1…fd57` | `4ef8c0428d42fbe37be634d79296d7ec80860308345bf4826650fef1739b2229` |
| DEL-04-03 `Design/RECORD_SEMANTICS.md` | `6c6408d8c10a…739f` | `d3db9b97ab1d90bf222bda5bdfc16fb2e2f0514c89891dcedfa52d0bd8a62a98` |
| DEL-09-06 `Design/RELAY_QUESTIONS_SWBPIPE.md` | `71ac39b4ece5…dad3` | `6e726be9ae39e8a8b5ec39b38984081339bac5bee52ce88fc8739a298801ae92` |

"Before" values were computed at the start of this node (`$TMPDIR/rv21b/before.sha`); the five Design files among them equal GUIDE-v0.6's pins.

## 5. Reruns (2026-10-02, Python 3.13.7, node v24.5.0; `python3 -B`, no bytecode written; `git status` showed no prototype output written into the repository)

| Deliverable | Command | Result |
|---|---|---|
| DEL-02-03 EXEC | `prototype/run_all.py` (before and after) | exit 0, "ALL CHECKS HOLD: 0 failure(s)" both times. 106 → 114 "ok" lines: the EV-3a readings went from 18 to 26. Apart from the `agent-delegation` readings, every output line is identical (`diff` with those lines excluded) |
| DEL-02-01 WD/WD-EX | `prototype/wdproto.py selftest` (before; after the WD text edits; after the HOSTING edits) | exit 0, 62 checks, 62 passed every time; S-11 reads 27 groups from HOSTING |
| DEL-01-01 HOSTING | `prototype/run_cases.py` | exit 0; TOTAL 35, pass (model) 35, FAIL 0 |
| DEL-04-03 RS | `prototype/run_prototype.py $TMPDIR/rv21b/rs-out` | exit 0; 63 PASS, 0 FAIL; "RESULT: all expectations held" |
| DEL-04-01 ACT | `prototype/validate_policy.py` | exit 0; "RESULT: all expectations held" |
| DEL-09-06 CA (affected, not edited) | `prototype/run_w14_rehearsals.py --out $TMPDIR/rv21b/w14` | exit 1, 43 PASS, 1 FAIL (the stale example pin, §3 item 1) |
| DEL-03-04 GUIDE | no prototype; `pins.py` check-only | 17/25 (§3 item 5) |
