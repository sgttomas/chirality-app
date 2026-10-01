# RP-1 — return (Type 2 TASK, 2026-09-30)

Node RP-1 of run `APP-V4-DESIGN-PASS-2-20260930`: the record join across RS
(DEL-04-03), EXEC (DEL-02-03) and ADAPTER (DEL-03-03). Executor: Claude Code
subagent (Claude Opus 5.5), no delegation. The node resumed after a
connection error with no edits made; the coordinator relayed this.

**Read, whole.** `BRIEFS.md` ("Common rules", "Wave B" common rules, row
RP-1), `R14_RESOLUTIONS.md` (binding), `R13_RESOLUTIONS.md`,
`R12_RESOLUTIONS.md`, `OWNER_DECISIONS.md` (DECISION-K1), all four
`comparisons/V18-n.md`, `WAVE_B/OBS-1.md`, `WAVE_B/OBS-1b.md`. Read in part:
the relevant sections of the three Design files, their schemas and
prototypes; DEL-01-01 `OBS_1_0.158.0.md` facts, through the OBS returns;
LOOP §2.3, §3.1 and §7; WD §4.3.1 and §4.4; P §9 and `proposal_state.schema.json`
in the working tree, where RP-2 was editing in parallel.

**Rules kept.** No version bump. Every change is a row in the file's Wave B
change table. Edits stay inside the fence. No git writes, no network, no
installs. Scratch is under `$TMPDIR/rp1/`.

## 1. Per R14 item

| Item | Status | Fix and location |
|---|---|---|
| **R14-1** | Done | See below |
| **R14-2** | Done | See below |
| **R14-3** | Done | See below |
| **R14-4** | Done | See below |
| **R14-7** (R13 and the OBS observations, in these files) | Done | See below |
| **R14-8** | Done; nothing returned | See below |
| R14-5 (EV-3 only, which is in EXEC) | Done on EXEC's side | See below |

### R14-1 — one record container (done)

EXEC's schema:

- `checkpoint-record-entries.schema.json` no longer defines a container.
- It defines the bodies of CE-1…CE-19 in camelCase, matching RS's record convention.
- Its root validates one recorder output: {RS kind, observedAt, body}.

RS's schema:

- Twelve new kinds: `checkpoint_listed`, `declaration_finding`, `act_counted`, `act_not_counted`, `item_decision`, `arrival_declined`, `control_relation`, `continued_past`, `observation_lost`, `observation_recovered`, `arrival_replaced`, `act_after_run_end`.
- These kinds now `$ref` EXEC's bodies by relative, percent-encoded path: `checkpoint_arrival`, `act_request`, `act_lapsed`, `run_resumed`, `run_ended`, `disposition_change`. `disposition_change` takes the body through `allOf`, which adds RS's annotation objects.
- CE-19 is written as `evidence_limit` "record write failed", after the late entries.

Shared spellings: spaced dispositions; the ordinal starts at 1; annotations
are structured objects; "run owner"; "replaced by next arrival". WD tokens
are used for the reached-when kind and the capturing surface.

Locations:

- **RS:** §13.3, with a CE→RS table and a new §13.3.1 that maps LOOP §2.3's events; §4 R8; §7 L-12.
- **EXEC:** §2.4.2, §2.4.3 and §2.4.5 (F-35 closed); §2.6; §2.7.

Supporting changes:

- RS `minischema.py` now resolves relative file references. RS's `$id` is a URN, and RS §13 states the consequence.
- RS's three example logs were rewritten into the referenced bodies.
- New INV-RS-12…15.
- EXEC's recorder now emits recorder outputs; its examples were regenerated (12 valid; INV-EXEC-1…7).
- New `exec_to_rs.py`.

### R14-2 — act requests (done)

- RS no longer accepts "agent message naming kind, subject and purpose" as a way of identifying a request.
- The App-run example's request is now a supplier person-input request that names nothing.
- `actKind`, `subject` and `purpose` can each be "not named by the request".
- The forms now include EXEC's forms and the host-recorded request, with the arrival association.
- EXEC RC-5 states the same. ADAPTER §7.7 cites RC-5.

### R14-3 — record vocabulary (done)

RS adopts the supplier vocabularies, with one token table in RS §5 "Supplier tokens":

- **Outcomes:** P's two new outcomes; ADAPTER's values; and the loop's own refusals, *rejected before host validation* and *not dispatched: turn cancelled*.
- **Operation entries:** new elements `requestKind` and `reason`.
- **R11 labels:** "basis lineage not supplied" (R13-1), "resubmission without prior observation" and "App-restart interruption" (R13-2), "host result not isolated", "dispatch recognized from compound command", "de-duplication scope exceeded", and "act offered without a capture-evidence reference".
- **R14:** the value *does not pass*.
- **Workflow origin:** `host`, with `sourceRoot` required.
- **Boundary refusal:** the reason "no credential" (m-11).
- **R5:** thread-scope model report (m-13).

U-31 is closed.

### R14-4 — ADAPTER's observations carry what EXEC needs (done)

Act observations (CO-2, CO-3) now carry:

- the host's act reference;
- the capture time, or *not_supplied_by_host*;
- the RS identity of the faithful record, or *not_written*.

New observations:

- CO-10: an accepted item that is then not applied (PT-15, PT-16).
- CO-11: a request recorded by the host.

OM-1 now recognises a dispatch at `item/started` from its start-time source, and removes the one shell wrapper. The record keeps `native_source`. EXEC AW-2 says the same.

Both schemas and `observe_map.py` were changed, and the examples regenerated.

### R14-7 — R13 and the OBS observations (done)

- **R13-1:** ADAPTER RD-2 and RS R11.
- **R13-2:** RS R11, FC-9 and U-31; ADAPTER OM-9 and §11.
- **R13-6, MCP path:** pending, with the `namespace` reason, in EXEC AW-1, AW-8, AE-5 and U-E26, and in ADAPTER §3.5.
- **OBS-1b:** EXEC AW-2 and AW-9; ADAPTER §3.5, OC-5 and the UNRESOLVED row.
- **OBS-1 Part D:** ADAPTER OC-3 (b).
- **OBS-1 O-5 and O-6:** EXEC AW-6.

### R14-8 — the SCA-V4-002 arcs (done; nothing returned)

- **N-21:** EXEC cites P-v0.8. The `itemDecision` body keeps `leftCause`. A resulting object P does not supply is recorded "not supplied by host".
- **N-24:** EXEC and ADAPTER cite each other at v0.6, and each CO names the CE event it feeds.
- **F-32:** settled from the existing texts, so it is not returned. ADAPTER §4.6 and §7.7 derive every observation from the agent's own calls. The required-tool check's catalog read is named as the only App-origin read.
- **X-1:** EXEC §7.4 lists CH-31 (ii).

### R14-5 — EV-3 only (EXEC's side done)

EV-3 now has a PROPOSED presence rule that reads WD's group column against
HOSTING §8.4. The rule takes no effect until DEL-01-01 states the signals.

### V18 MINOR findings, also fixed

- **V18-1:** m-2, m-3, m-4, m-5, m-6, m-7, m-8, m-9, m-11, m-12, m-13.
- **V18-2:** m-1 (U-E27 closed), m-2 (F-33 closed), m-3 (U-E7 closed), m-4, m-5, m-12.
- **V18-3:** m-1, m-2, m-3, m-5, m-7, m-8 (SH-n → SD-n; CF-n → RF-n), m-9, m-10, m-14 (`proposal_minted_by`; the identity stays a string because XT reads it), m-18, n-8.
- **V18-4:** m-1, m-5, m-6, m-7.

V18-1 m-16 is left to AS's schema, which RP-4 edited. RS §8 is unchanged, so it stays identical to AS §6.

## 2. The conversion (EXEC → RS)

`exec_to_rs.py` results:

- 19 of 19 CE bodies have an RS kind that references them; none is without a kind.
- EXEC's valid example: **12 of 12 entries valid**, none refused, and the reader found no limits.
- EXEC's other CH runs plus one sample of each remaining kind: 40 of 40 valid.

## 3. Prototypes rerun

Run on 2026-10-01 at 01:50 UTC (2026-09-30 local), Python 3.13.7. Output is in `$TMPDIR/rp1/final/`.

| Prototype | Command | Result |
|---|---|---|
| EXEC | `PYTHONDONTWRITEBYTECODE=1 python3 run_all.py` | ALL CHECKS HOLD, 0 failures (85 ok) |
| RS | `python3 -B run_prototype.py` | 49 PASS, 0 FAIL: 4 logs, INV-RS-1…15, FC-1…FC-7, the R14-1 checks |
| SH-1 | `run_fixture.py --out` | 22 of 22 checks passed; then `validate_all.py --run`: all checks passed |
| ADAPTER | `observe_map.py --run` (check mode) | All passed. Includes the OBS-1b-shape checks, CO-10/CO-11 shapes, and **34 records → 43 of 43 RS entries valid** against RS's schema |
| P | `proposal_states.py --check` | Passed |
| LOOP | `destination_flow.py` | 68 RS entries valid; passed |
| AS | `validate_settings_in.py` | Held |
| ACT | `validate_policy.py` | Held |
| XT (outside the fence) | `run_xt_suite.py` | Holds |
| CA (outside the fence) | `run_w14_rehearsals.py` | 1 FAIL: "valid example equals regenerated W14-05". It already failed before my edits; RP-4 has already adapted CA to the recorder outputs |

## 4. What other files must now say (for the integrator)

- **LOOP:**
  - §2.3 and E-4 cite RS §13.3.1 for the event mapping.
  - Record the "Run interrupted / observation recovered" event as `observation_lost` / `observation_recovered`.
  - F-10 cites RS W-1.
  - A loop-side refusal uses the R7 outcomes *rejected before host validation* and *not dispatched: turn cancelled*.
- **CA (RP-4):**
  - Regenerate `w14-result-record.example.valid.json`.
  - Change the act citations from `A4-T2` etc. to `rec:` identifiers.
  - Spell the evidence limits with RS's words (V18-4 m-2).
- **WD (RP-3):**
  - The capturing-surface and reached-when tokens are canonical; EXEC now uses them.
  - §4.3.4 reads "replaced by next arrival".
- **P (RP-2):** `act_ref.captured_at` is consumed. When it is absent, the consumer writes "not supplied by host".
- **HOSTING (RP-3):**
  - §6.8 should name the required-tool check's catalog read as an App-origin read, or say how the checker obtains the edition.
  - LT-12 should name DEL-03-03 and DEL-02-03 as receivers (V18-3 m-17).
- **XT and CA:** read ADAPTER's `exec_event` as CE-n, not as the old row tokens.
- **GUIDE (B8):** cite the RS kinds and the EXEC-body arrangement.

## 5. Files (sha256, first 12 hex)

EXEC (DEL-02-03):

| File | sha256 |
|---|---|
| `EXECUTION_COMPATIBILITY.md` | 6c43aca4cb0f |
| `checkpoint-record-entries.schema.json` | 03fb0dbac1f3 |
| `checkpoint-record-entries.example.valid.json` | 1575558fb932 |
| `checkpoint-record-entries.example.invalid.json` | 09763173be0e |
| `compatibility-report.schema.json` | 15daee8102a0 |
| `prototype/README.md` | b301c1dd5035 |
| `prototype/checkpoint_recorder.py` | 303ff2de49f2 |
| `prototype/fx_double.py` | 97e1cb1ab652 |
| `prototype/required_tool_check.py` | c8118fa39bae |
| `prototype/run_all.py` | 3808fb9bdc55 |

ADAPTER (DEL-03-03):

| File | sha256 |
|---|---|
| `ADAPTER_ENABLEMENT_AND_RECEIVING.md` | 09f8aa31f7bf |
| `checkpoint_observation.schema.json` | 5d17aa548789 |
| `checkpoint_observation.example-valid.json` | 69a033a7323c |
| `checkpoint_observation.example-valid-2.json` | 20f92dbd98e7 |
| `checkpoint_observation.example-invalid.json` | dd519fe6fe73 |
| `external_dispatch_record.schema.json` | 726d8787d1b9 |
| `external_dispatch_record.example-valid.json` | 69b496d5f1c0 |
| `external_dispatch_record.example-valid-2.json` | 8e2240355766 |
| `external_dispatch_record.example-invalid.json` | 2c4c89736698 |
| `prototype/observe_map.py` | a0b0174799b1 |

RS (DEL-04-03):

| File | sha256 |
|---|---|
| `RECORD_SEMANTICS.md` | 83896f4dac6e |
| `RS_RECORD.schema.json` | 76d473ac792a |
| `RS_RECORD.invalid.examples.json` | 808765dc094d |
| `RS_RECORD.valid.app-run.example.jsonl` | 629cb89e63bf |
| `RS_RECORD.valid.host-run.example.jsonl` | b990fc7ea64e |
| `RS_RECORD.valid.act-log.example.jsonl` | 36a6006dd61d |
| `prototype/README.md` | 9f1d240673e7 |
| `prototype/minischema.py` | 2851bb7cd497 |
| `prototype/run_prototype.py` | 631603a4693d |
| `prototype/exec_to_rs.py` (new) | 8e3970089127 |

`git status --short` shows no change of mine outside these files. The other
changes in the tree come from RP-2, RP-3 and RP-4.
