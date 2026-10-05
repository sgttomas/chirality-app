# DEL-01-04 prototype — request cards, outcomes, attachments, drafts, act control

**This is a design prototype, not product code.** It belongs to
DEL-01-04/NIR-v0.2 (`../NATIVE_INTERACTION_RECEIVING.md`, §13.2) and
DEL-01-04/AAC-v0.2 (`../APP_ACT_CONTROL.md`, §8), written by node D3 of run
`APP-V4-DESIGN-PASS-3-20261001` under R17-1 (R12-3 limits). It is not an App
candidate and not the OI-008 placement; nothing in it is qualified or
selected. Python 3 standard library for every check except two optional
third-party cross-checks (S-4, O-9; see below); no package is installed; no
network is used; the Codex binary is never started; all content is invented.

## Files

| File | Role |
|---|---|
| `nir_model.py` | The card model per 0.158.0 server-request kind (NIR §4.1–§4.3); a register double applying HOSTING-BOUNDARY-v0.8 §6.2.1 RT-01…RT-13 and the U-26 refusal order, used only to drive card states (NIR §4.4); card states; turn/outcome labels and the start display (NIR §5); attachment supply records (NIR §6); the draft view (NIR §7) |
| `act_control.py` | The App act control (AAC §1–§5): offers, native-only operation, stale binding, capture evidence, RS entries written through DEL-04-03's writer, A15 with a stub workspace registrar, late write and relaunch recovery |
| `run_cases.py` | Runs every check; exit status 0 when all are as expected |
| `results/RUN_2026-10-02.txt` | The recorded output of the round-2 run below (`RUN_2026-10-01.txt`: round 1, kept) |

**Read-only imports of first-increment prototypes** (located by path from this
folder; nothing in them is changed): DEL-04-03's `minischema.py` (validator)
and `record_store.py` (the PROPOSED writer and reader), so the act control's
entries are validated by RS's own schema before they are written; DEL-01-01's
`jsonschema_subset.py`, so every register entry the walk produces is checked
against HOSTING's PROPOSED entry schema; and, at RV21, DEL-02-02's
`workspace-registration.schema.json` with its valid examples and DEL-02-01's
`workflow-declaration.schema.json`, so that K-17 runs WR's own A15 descriptors
through the act control into RS's writer (R21-3). **Optional third-party
cross-checks:** if the already-installed `jsonschema` package is importable,
the five DEL-01-04 schemas are cross-checked with it (S-4) and composed
`turn/start` parameters are checked against the committed 0.158.0
`TurnStartParams` (O-9); otherwise both are skipped and say so.

## How to run

```sh
cd "<this folder>"
python3 run_cases.py      # one line per check; exit status 0 = all as expected
```

Logs written by the act control go to a temporary folder under `$TMPDIR`
(`d3-del-01-04-*`).

## Run recorded

- Date: 2026-10-02 (round 2); host: macOS (Darwin 25.6.0, arm64); Python 3.13.7.
- Command: `python3 run_cases.py` in this folder.
- Output: `results/RUN_2026-10-02.txt` — 119 checks, 0 failed, exit status 0.
  Round 2 adds turn composition (checked against the committed 0.158.0
  `TurnStartParams` with the installed `jsonschema`), the start display's
  wording and role, the waiting indicator, the start offer, "Continue as",
  items never completed, the C-02 read side, and several-entry A15.
- Round 1: `results/RUN_2026-10-01.txt` — 103 checks, 0 failed.
- RX2 (residual sweep 2, 2026-10-02): `results/RUN_2026-10-02_RX2.txt` — 120
  checks, 0 failed. `start_offer` follows R20-11 (only "End ‹A› and start ‹B›"
  during a run; the proposal line last and once), new `finished_offer` (NIR
  RN-7) and `handoff_composer` (CA-2, R20-6); O-11, O-12 rewritten, O-13 new.

- RV21 (repairs from V21, 2026-10-02): `results/RUN_2026-10-02_RV21.txt` —
  151 checks, 0 failed. Attachments per R21-2 (A-1…A-8: text element, image,
  named path with tool reads, `mention`/`skill` refused, a draft's
  `WORKFLOW.md`); the Stop Codex label (O-3a); the run-end line and attachment
  order (O-8a); one A15 descriptor per act with the multi-entry in-place case
  (K-12b…K-12d) and the WR → AAC → RS cross-check (K-17, K-17b) per R21-3.

A "pass" means the rules ran as written on this model. It is evidence about
the design, never a VER pass: no App candidate exists.

## CC-A candidate (2026-10-04)

`cc_a_sequence.py` is a standalone standard-library state model for frozen
A16 selection, immutable capture facts, writer-minted record identity and
add-once backlink recovery. Run `PYTHONDONTWRITEBYTECODE=1 python3 cc_a_sequence.py`.
It checks 20 cases; canonical output is `results/RUN_2026-10-04_CC-A.txt`.
Atomic publication/replacement and exclusive serialization are model assumptions,
not demonstrated filesystem/native behavior. The old act_control model still
pre-mints recordId; its results do not establish CC-A's persistence sequence.

CI-1 consumer propagation: `run_cases.py` explicitly registers EXEC's committed
checkpoint schema by its declared `$id` before validating RS entries. No URI
rewrite or hidden path fallback is used. The first failed run is retained in
`results/RUN_2026-10-04_CC-A_LEGACY.txt`; after registration it completes
159 checks with one R-16 failure (NIR generation integers versus concurrently
revised HOSTING generation objects), retained in
`results/RUN_2026-10-04_CC-A_REGISTRY.txt`. Reconciliation is pending with CC-H;
no combined prototype pass is claimed from these two outputs.

CC-H/CI-2 consumer propagation subsequently replaces the NIR register double's
integer generation with the hosting owner's invented full tuple
`{appSession: "aac-fixture-session", home: "account", spawnCounter: 1}`;
closed-generation keys use all three fields. This is not an observed host.
The combined rerun `results/RUN_2026-10-04_CC-A_INTEGRATED.txt` passes 161 checks
with 0 failures, exit 0; earlier failure outputs remain retained.

R-16a additionally checks equal spawn counters with different App sessions or
homes: both are refused without settling the pending request.

## CC-NIR-ATTACHMENT-REF prepared candidate (2026-10-05)

`attachment_submission.py` checks29 invented cases for the ordinary
implementation-owned262144 original-file-byte carrier bound, lossless
native-path/display separation, immutable ordered submission/supply refs,
record-before-send failures, full-generation/RPC/expected-steer correlation
and cold prepared-state uncertainty/no resend. Persistence/transport are
callback doubles, not native/durable witnesses. Existing NIR supply schema
shape/ID0.2 stays unchanged; descriptions and one prepared-submission example
are candidates. No new companion schema/store was created.

Run `PYTHONDONTWRITEBYTECODE=1 python3 attachment_submission.py`; retained output
`results/RUN_2026-10-05_ATTACHMENT_SUBMISSION.txt` also contains the existing
`run_cases.py` rerun (162 checks/0 failures). Joined actual HOSTINGv0.10
association validation and independent review are still pending; these local
model passes do not prove consumer adoption, native send or provider receipt.

Joined review repair (2026-10-05): original three correlation defects are
retained in `results/RUN_2026-10-05_ATTACHMENT_REVIEW_REPRO.json`. The candidate
now requires written/pending owning RPC, rejects contradictory result thread,
handles malformed/null turn safely, preserves the first settled source/turn on
repeats, and retains errors as refusal. The positive steer case uses a fresh
owning pending RPC after the wrong-target case settles; a separate regression
asserts that a repeated correct reply cannot replace that settled wrong-target
source. No acceptance criterion is relaxed.

`results/RUN_2026-10-05_ATTACHMENT_SUBMISSION_REPAIR.txt`:54/54 focused cases
plus162/162 existing cases pass, exit0. Focused model now consumes the actual
HOSTINGv0.10 client schema and validates9 receiving states. Original source
frames remain owned by HOSTING; the model references them, never persists a
second raw payload/transcript. Native/durable/provider witnesses and independent
backcheck remain pending; actual supplier state is not established by callbacks.
