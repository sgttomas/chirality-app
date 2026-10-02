# V21b-B — recheck of V21-B's findings after the RV21 repairs (design pass 3)

- Run `APP-V4-DESIGN-PASS-3-20261001`, node **V21b-B**. Reviewer: Type 2
  TASK (Claude Opus 5.5, high effort), dispatched by HELP_HUMAN; does not
  delegate. Written 2026-10-02.
- **Candidate:** branch head `65f1d36f5a` (RP-final), after `cdf89b57ad`
  (V21-B review, R21 rulings, record corrections), `6185de63da` (RV21
  brief), `dc61150559` (RV21-B), `31d65b0be3` (RV21-A). Changes read with
  `git diff aa12160bfa..HEAD`. Inputs: `F/RV21-B.md`, `F/RV21-A.md`,
  `F/F-E2.md` "RP-final", R21-1…R21-4 (end of `R20_RESOLUTIONS.md`),
  OWNER_DECISIONS, ASSESSMENT_SIWC, DISPATCH.
- **Boundary kept.** Read-only on the repository except this file; no git
  write, no network, no Codex or model run. Reruns in a scratch extraction
  of the head (`git archive HEAD projects/chirality-app-v4 tools workflows`
  into `$TMPDIR/v21bb`), `python3 -B` / `PYTHONDONTWRITEBYTECODE=1`; outputs
  in `$TMPDIR/v21bb-out`.
- Paths relative to `projects/chirality-app-v4/execution`; RUN is this run's
  folder.

## Verdict

**MERGE AS DRAFTS.** No BLOCKING, no new MAJOR. All three MAJOR findings
are fixed. Of the eleven MINOR, nine are fixed, one is fixed differently and
one (m-3) is fixed in the run records but left in ACCESS §20, which now
reads against the corrected record. The repairs introduced one new MINOR
(n-1: first-increment texts still name `thread/read` as the supply-check
read after R21-4 moved WR to `thread/items/list`). All first-increment
prototypes rerun clean; GUIDE's pins are 25/25; DAG-003 is current.

## Disposition of V21-B's findings

| Finding | Status | Evidence |
|---|---|---|
| **M-1** delegation availability (NPTD vs EXEC/WD) | **Fixed** (R21-1) | NPTD-v0.2 §7.1 now states R21-1's order and calls itself the reference; EXEC-v0.7 EV-3a (l.948), WD-v0.9 §4.2.5, HOSTING-v0.9 HCG-A08 and GUIDE M8.3 state the same order: `disabled` → missing; `features.multi_agent = false` → missing; `namespaceTools` false → missing; any of the three not read → not established; otherwise present. EXEC's change-table J-5 row (l.86) now carries a correction note that the earlier confirmation did not hold. **Checked by script:** imported `npt_model.delegation_availability` and EXEC's `harness_presence('agent-delegation', …)` from the head and ran all 80 combinations of {version null/disabled/v1/v2} × {config unread/empty/`multi_agent` false/true} × {capabilities unread/{}/`namespaceTools` null/false/true}: **0 differ**. EXEC's prototype now carries 26 EV-3a readings (10 for delegation); `run_all.py` passes |
| **M-2** GUIDE `WD-v0.9` as declared-part value | **Fixed** | GUIDE M8.1 (l.478): "the value stays `WD-v0.8` at WD-v0.9, WD §3.3; R20-7; a declaration naming `WD-v0.9` is an unknown version, WD-EX E9 L-WDEX-33a"; §5 row (l.1075): "stays `WD-v0.8`". Word diff of GUIDE `aa12160bfa`→HEAD: only these two value corrections, M8.3's delegation clause, the RV21 and RP-final change rows, the consumed-input line and 14 re-pinned rows |
| **M-3** L-4 in-place path WR → AAC → RS | **Fixed** (R21-3, by RV21-A in AAC) | `aac.offer.schema.json` l.94 and `aac.capture-evidence.schema.json` l.99 now accept `^(draft\|entry):…`; the offer's `wording` enum adds "register workflow revisions"; the valid examples include an `entry:` instance, and all 3 + 2 valid instances validate under `jsonschema` 4.26.0 while all 16 + 12 invalid instances are refused (checked here). AAC's prototype, rerun from the head: 151 checks, 0 failed, including **K-17** (WR-v0.2's own `a15_descriptor` and `a15_multi_descriptor` through AAC's offer and capture into RS's writer) and **K-17b** (RS act-log record 4, `entry:` strings, `cap:reg-in-place-2`, has capture evidence AAC's format accepts). RS act-log record 4's purpose now reads "make them available in the project library", matching ACT §2.1. WR prototype 99/99 |
| m-1 WD/WD-EX stale S-11 failure | **Fixed** | WD §13.1 adds "Resolved (RV21 …)"; WD-EX l.1295 says the failure was withdrawn under R20-8 and rerun at 62/62; `wdproto.py selftest` here: 62/62, S-11 reads 27 groups |
| m-2 NR-L1 missing from RELAY's next-relay row | **Fixed** | RELAY l.1141 gains item (6), host plan billing NR-L1, with its sources and "information … not a requirement". One-hunk diff; §0–§3 span (from `## 0.` to before `## 4.`) sha256 prefix `9c9463e77f57` at `a38617d08b`, `aa12160bfa` and HEAD alike (my span method; RV21-B reports its own method's equal value). HANDOFF l.106's "the full list is RELAY's row" is now true |
| m-3 SIWC acceptance stated as fact | **Fixed in the run records; not fixed in ACCESS §20** | OWNER_DECISIONS now labels the arrangement "Reading (HELP_HUMAN, not owner text …)" and says the owner "did not separately answer and did not object"; ASSESSMENT_SIWC adds "*Superseded in part (2026-10-02)*" for recommendations 1–3. But ACCESS-v0.2 §20 "Decision record" (l.944–949) still says the recommendation "was accepted with L-1 and L-6 (OWNER_DECISIONS, 'Sign in with ChatGPT' exchange)", citing a record that now says otherwise. MINOR; ACCESS is outside RV21-B's fence (DEL-01-05) |
| m-4 WR supply check via deprecated read | **Fixed** (R21-4) | WR §16.6 SC-3 reads `thread/items/list {threadId, turnId}` following `nextCursor`; the method is in the 0.158.0 stable inventory (`_spike/inventory.txt`) and its params (`threadId`, optional `turnId`, `cursor`) and response (`data`, `nextCursor`) are in the committed bundle; WR U-WR-14 labels the `thread/items/list` return of the same `ThreadItem` as `observed-in-generated-types`, not observed (OBS-3 W-4 saw it via `thread/read`). See n-1 for the first-increment side |
| m-5 HOSTING "only" K-12 session flags | **Fixed** | HOSTING §4.2 step 3 (l.469–474): the K-12 settings "and, if ROLE U-R3 selects `-c` session flags as the child-role carrier, the additive `agents.<ROLE>.*` entries of §8.2; never a credential" |
| m-6 TA-5 section pairing | **Fixed** | HOSTING l.1471–1472: "(NPTD-v0.2 §6.4; §9 TA-5)" |
| m-7 F-E2 fence extension unrecorded | **Fixed** | DISPATCH row "F-E2 (record)": "V21-B m-7: F-E2 also edited ADAPTER (verification-case version list) and WR §8 (receivers) …" |
| m-8 S-1 "receiving comparison" | **Fixed** | HOSTING header Receivers line: "S-1 RECOVERY-v0.2 §1 (reconciliation with §6.5) and §4.2 (consumed)"; no "receiving comparison)" left for S-1 |
| m-9 F-E2 §4.3 leftovers | **Fixed differently / in part** | Row 7 (WR schema `selection_record` description): fixed by RV21-A ("DEL-02-04 receives no selection …"). Row 9 (HOSTING l.768–769): "this file's §6.2.1 RT-08". Row 10 (ACT §2.6): "SC2-01-04-1 as amended by SC3-01-04-1"; the FA-01 change-table row keeps the old words as history. Row 11: EXEC's `LOOP-v0.8 §2.3 E-8` gone (0 left), RS's LOOP labels moved; CA's remaining "RS-v0.8 L-13" / "EXEC-v0.6" at l.1083 sit in a finding-disposition paragraph (history) and are acceptable. None changes a meaning |
| m-10 WD vs R20-11 wording | **Fixed** | WD §3.9 (a), (b) say "last non-empty line" and "the one immediately before its proposal line"; no "the message's last line" left; EXEC RE-7 now offers "Start ‹workflow› (proposed by the agent)" |
| m-11 AAC `codexAccount` looser than RS | **Fixed** | `aac.capture-evidence.schema.json` `actor.codexAccount` now cites RS `$defs/person.codexAccount` with the same `anyOf` (email pattern or "ChatGPT account (no email reported)") |
| V21-A note (Stop Codex label) | Not rechecked here | RV21-A's scope |

## New finding from the repairs

**n-1 (MINOR). First-increment texts still name `thread/read` as the read
behind the per-run supply check.** R21-4 moved WR-v0.2 §16.6 SC-3 to
`thread/items/list`. The first-increment texts that describe the same check
still say "checked against `thread/read`" or give failure rows in its name:
EXEC-v0.7 (13 mentions, e.g. §0 table "checks it against `thread/read` (WR-v0.2
§16.2, §16.6)", §2.6 A-3's failure rows "`thread/read` does not return …",
"`thread/read` unavailable", §6.1 *supplied*, VC-E-18), WD-v0.9 (5, OS-7 and
§6.2 *supplied*), HOSTING-v0.9 §8.2 (4), CA-v0.7 §4 *supplied* (2), RS-v0.9
R3 and the `supplyCheck` description in `RS_RECORD.schema.json` (1 each),
GUIDE §5's R19-1, R19-7 row (1). R19-7 itself says "checks them against `thread/read`", so
these texts follow a ruling that R21-4 has since refined; the meaning (a
check against Codex's history) is unchanged, and the state values agree with
WR. *Fix:* "checked against Codex's history (WR-v0.2 §16.6 SC-3:
`thread/items/list`; R21-4)" at the next touch of each file, or an
integrator note that R19-7's "`thread/read`" reads as "Codex's history read"
after R21-4.

## Anything the repairs broke in scope

Nothing else found. Checks:

- **Prototype reruns at the head** (Python 3.13.7): HOSTING `run_cases.py`
  35/35, exit 0; EXEC `run_all.py` "ALL CHECKS HOLD: 0 failure(s)", 114
  "ok" lines (was 106; the EV-3a readings went from 18 to 26, as EXEC §7.4
  records); RS `run_prototype.py` 63 PASS, 0 FAIL; WD `wdproto.py selftest`
  62/62; C `run_fixture.py` 22/22 and `validate_all.py` pass; ADAPTER
  `observe_map.py` pass (34 dispatch, 11 checkpoint observations, 14 channel
  statuses); P `proposal_states.py --check` pass; CA
  `run_w14_rehearsals.py` "ALL CHECKS HOLD: 0 failure(s)" (the regenerated
  example's pin of EXEC `run_all.py` now matches); XT `run_xt_suite.py` pass;
  LOOP `assemble_tool_calls.py` 22/22 and `destination_flow.py` (68 RS
  entries, 11 request records valid); PANEL `panel_double.py` 4/4; ACT
  `validate_policy.py` and AS `validate_settings_in.py` all expectations
  held. For the joins: DEL-01-04 `run_cases.py` 151 checks, 0 failed; WR
  `wrproto.py` 99/99.
- **GUIDE pins:** script over the 25-row input table against the head's
  bytes: **25/25** equal.
- **DAG-003 currency:** `shasum -a 256 -c MANIFEST.sha256` 37/37 OK;
  `SOURCE_MANIFEST.sha256` 130/130 OK, 0 not OK;
  `tools/coordination/analyze_dep_closure.py … --include-declared true`
  exit 0, `run_status` COMPLETE, `accepted_dag.result` **NO_DEPARTURE_FOUND**.
  No register row was added, so V21-B's SCC results stand.
- **Protected files:** `git diff --name-status aa12160bfa..HEAD` shows no
  ScopeOfWork, register, `_STATUS.md`, `_DAG/`, `_Decomposition/`, `docs/`,
  `OBS_*`, `PIN_SPIKE_*`, `generated/`, `RELAY_ANSWERS_*` or `FACTS_*`
  change and no deletion. RELAY's §0–§3 are byte-identical.
- **Owner decisions:** the repairs touch no owner text; R21-1…R21-4 are
  integrator rulings recorded as such. The record corrections make
  OWNER_DECISIONS more conservative (m-3), not less.

## Scratch (not in the repository)

`$TMPDIR/v21bb` (head extraction), `$TMPDIR/v21bb-out` (prototype and DAG
outputs), the 80-combination comparison script (inline), `$TMPDIR/g6a.md`,
`$TMPDIR/g6b.md` (GUIDE before and after, for the word diff).
