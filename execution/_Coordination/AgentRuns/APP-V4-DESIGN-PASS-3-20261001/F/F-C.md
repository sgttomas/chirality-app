# F-C — RS, ACT, AS first-increment edits (design pass 3)

- Run `APP-V4-DESIGN-PASS-3-20261001`, node **F-C**. Executor: Type 2 TASK
  (Claude Opus 5.5), dispatched by HELP_HUMAN; did not delegate. 2026-10-02,
  working tree at `ac9a68a7f2`.
- Boundary kept: I wrote only inside the fence of F0 §6 for F-C: DEL-04-03
  `Design/` (RECORD_SEMANTICS.md, RS_RECORD.schema.json, the RS example and
  invalid files, `prototype/README.md`, `record_store.py`,
  `run_prototype.py`), DEL-04-01 `ACT_AND_POLICY_CONTRACT.md`, DEL-04-02
  `AUTONOMY_AND_STANDING_EXCHANGE.md`, and this file. I did not edit
  ScopeOfWork, registers, `_STATUS.md`, OBS/PIN files or other deliverables'
  files. Git was read-only. I used no network and ran no Codex or model.
  Other deliverables' prototypes ran only in scratch copies of the package
  folders under `$TMPDIR`.
- Inputs: BRIEFS (F), R17, R18, R19, **R20** (`91fff5a3f6277d78`, which
  arrived mid-node), OWNER_DECISIONS (K3 revised, L), DECISION-K1, F0 §1.3–§1.5,
  §1.14, §2, and the round-2 join lists of D1, D3, D4, D5 and D6 (§R2.3),
  which the coordinator sent mid-node. The new files are cited by v0.2
  label. RECOVERY, ACCESS, ROLE and WR were read at v0.2. AAC and NIR were
  read at v0.1, so their section numbers come from v0.1; F-E checks them.

## 1. Version steps

| File | From → to | sha256 before | sha256 after |
|---|---|---|---|
| `DEL-04-03/Design/RECORD_SEMANTICS.md` | RS-v0.8 → **RS-v0.9** | `b25cc90e9e252f50…` | `d523dc9e679701eb9eea7495f1da4d909a4c71915be324595a139ec488204ec3` |
| `DEL-04-01/Design/ACT_AND_POLICY_CONTRACT.md` | ACT-POLICY-v0.8 → **v0.9** | `6fb6b9e883fa8d20…` | `3d9f3ee2c9e1683944afa20409b904bd5a0bcd04ce419c170867a778b3c5fd57` |
| `DEL-04-02/Design/AUTONOMY_AND_STANDING_EXCHANGE.md` | AS-v0.8 → **v0.9** | `d6f26801b0146800…` | `dc3fd0b68406fc0fa329b94d3bf3e82d3268584629d97d58f1b568265cbbc5e0` |
| `RS_RECORD.schema.json` (format 0.1, in place, R13-4) | — | `b63a7e421b885854…` | `2ff3f07873d00c2ab5f921fdb096a4dafdd5d3dbf883f74183f2639a4f18c103` |
| `RS_RECORD.valid.act-log.example.jsonl` (3 → 4 entries) | — | `36a6006dd61d8017…` | `b202e850d7a966a88e68fa9f290175c3ff493540e4d8acca4a500d6f4d5b69a9` |
| `RS_RECORD.valid.app-run.example.jsonl` (records 1, 16) | — | `629cb89e63bfb66d…` | `cb9a8acf23733be0fd996d9162bb8a0ceb2d0e5344236500d45912eda7805e3e` |
| `RS_RECORD.valid.app-chained-run.example.jsonl` (**new**, 8 entries) | — | — | `eb39c986da31805136feec0f75f5daf0a62a3776708a9425665c95dad14559ce` |
| `RS_RECORD.invalid.examples.json` (15 → 24) | — | `808765dc094d4e5c…` | `d577ab6fad6edce58e931a3ba10c428614db49a0768c9d7e9a4254f15c418087` |
| `prototype/record_store.py` (A15 reader rule) | — | `aa2e27dfc06a4d5c…` | `22d3acacce2afe642b38261e62a610d234c224c18e5fac1144b669d676e82cd0` |
| `prototype/run_prototype.py` (FC-7c) | — | `631603a4693d70f7…` | `f11cecdb7a24dbd8711d8c173a1632fed6ff4f9d682d3e377249b33ac180a0a0` |
| `prototype/README.md` | — | `063acb68281e281d…` | `68d598b4c69e75cf6363a9555d68b23b23da364f953230f9934b9683030373c5` |

These files are unchanged: host-run, host-destinations and run-not-started
logs, `minischema.py`, `exec_to_rs.py`, and ACT's and AS's schemas, examples
and prototypes. AS §6 and RS §8 are still byte-identical from
"**Settings-in" to the end of the section. I checked this with a script:
`True`, 5483 characters.

## 2. Rows applied

Each file has a "Changes from v0.8" table with these row IDs.

**RS (FR-01…FR-14 and others)**
- **FR-01**: the run-ended event is RECOVERY-v0.2 DEF-4. DEF-1, 3, 5, 6 and
  7 are never a run end. **U-R6 answered**: format 0.1 has no entry for a
  turn interrupt; its effects are recorded through R13, R11 and
  `observation_lost`. R20-1's cause *completed* is noted.
- **FR-02 + J-RS-5**: R13 supplier is now DEL-01-01 plus DEL-01-02. New
  settlements:
  - *resolved by supplier*, settled by *the supplier* (OBS-2 O-3);
  - *ended unanswered (process exit)*, settled by *none — ended unanswered*,
    with `context` and `custodyEventRef`.

  The schema pairs settlement and settler with `oneOf`.
- **FR-03**: U-20 is closed.
- **FR-04 + J-RS-4**: the §10 combined row is split into four rows
  (RECOVERY, AAC/NIR, WR, ROLE), and §10.1 follows. "App-restart
  interruption" is written on the run current at the interruption.
- **FR-05**: HA-10 now names DEL-01-04's act control as the surface, built
  from WR's descriptor. Non-evidence: "trial in conversation" and "ledger
  line without a capture".
- **FR-06 (C-01) + D5 J-21 + D3 J-R2**: added `relations.reviewedDraft`
  {draft, content}. The draft pattern is `^(draft|entry):(project|user):[^@]+@.+$`,
  so WR's `entry:` form for in-place entries is accepted. `priorRevision`
  is a `workflowTuple` or null. `relations.derivedFrom` is removed, and
  these relations are allowed on A15 only.
- **L-4 (+ D3 J-A3/J-E2, D5 J-35)**: added `registeredEntries` (two or more
  entries, in order). A reader R-7 rule checks that subjects, contents and
  entries correspond, and that each bound content equals its reviewed
  content (WR ID-2). An entry byte-equal to a shipped revision takes no A15.
- **FR-07**: App capture evidence is AAC's object, referenced by `cap:`.
- **FR-09 (as changed by D6 round 2, D5 J-34; R19 and R20-3 win)**: R3 has
  these App forms, each citing its supplier's record by reference (new
  evidence kinds *supply record* and *limit account*):
  - role guidance at conversation start, or inherited at a fork;
  - the workflow's run-start text;
  - the **run-end line** of R20-3.

  The turn-text forms carry WR's `supply_check` state as `supplyCheck`
  (spelling chosen here: WR's five states plus *not checked*) and
  `supplyCheckRecord`. New kind **`role_limit_observation`**. `adoption` is
  always *unknown*.
- **FR-10**: R5a. The role is fixed for the conversation's life, comes from
  ROLE's selection or is *no role*, and a fork keeps the source role.
  `seatRole` is described accordingly.
- **FR-11**: A15 acts go to an act log per library, travelling with it. WR's
  path is only a placeholder; U-05 stays open.
- **FR-12 (C-10, D4 round 2)**: `codexAccount` is the email or "ChatGPT
  account (no email reported)", with no plan type. U-A8 is answered "email"
  for format 0.1, and a digest is left to the owner as new U-33.
- **FR-13**: no value change; the ACCESS mapping is recorded in R5.
- **FR-14**: stale pointers refreshed (Receivers line, U-08, U-28).
- **R19-2 + D5 J-34**: new relation `run_opened.follows`, meaning "follows
  ‹run› in this conversation" (spelling chosen here). It is context only and
  is not *continues*. R20-1 and R20-5 are noted.
- Also: new §4.5 element table, VC-40…VC-42, updated VC-31 and VC-37, and a
  new §15 rerun bullet.

**ACT (FA-01…FA-08)**: all applied.
- §2.6 and §2.1 now name DEL-01-04's App act control as the surface, built
  from WR's A15 descriptor.
- Content is the revision identity plus the prior revision; purpose is
  "project library" or "user library". Several entries per act are allowed,
  "as a batch A5".
- §2.5 uses the C-01 relations.
- §4.7 RC-3 and the A15 paragraph are updated, with the outcome reported
  beside the act.
- §10.3 DEL-01-04 now has its receiving side (NIR §8, §4, §9; AAC §1.2). The
  DEL-02-02 row is mapped.
- FX-56 is updated: reviewed draft d-12 and no prior revision. **New FX-58**
  covers multi-entry, shipped-revision recognition, and an entry changed
  after review.
- V-01, U-08 and §12 item 6 are refreshed. F0's "L112" is change history and
  was left as is.

**AS (FS-01, FS-02)**:
- FS-01: §13 records R17-7 for App surfaces. DEL-04-02 defines K-5 and K-6;
  DEL-01-04 places them (NIR §9). "No option is chosen" now applies only to
  hosts and code placement.
- FS-02: DEL-01-04 is added as a receiver in §12 (proposed row NR-08, held,
  SCC-neutral per F0 §3) and in §12.1, with its condition of use and its
  *unconfirmed* and *missing* behaviour. §10 gains a row.
- R18-5 is noted.

## 3. Rows not applied, or applied in another form

- **FR-09, embedding the ROLE body by relative `$ref`**: applied as a
  reference to the record, not an embedded body. There are three reasons:
  - R19-1 and R19-7 give R3 two suppliers (ROLE and WR), so F0's row, which
    rests on R17-8, is superseded. R19 wins.
  - ROLE's schema uses `if`/`then`/`else`, which is outside the minischema
    subset, so the prototype could not load it.
  - Both formats were being stepped in parallel.

  Embedding is recorded as an alternative.
- **FR-08 (SEAL-2)**: left conditional, as the brief allows. It is text only
  (§14.2 R-7, U-32), with no schema element.
- **ACT §8.1 policy revision label**: stays `ACT-POLICY-v0.8`. No policy
  record changed, and the instance file is outside my fence.
- **F-B coordination on `runEnded`**: not coordinated live. My assumption is
  that EXEC's body is unchanged. I re-checked at the end: EXEC's schema is
  still sha256 `55c65bd83908bdd3`, with `stoppedBy` (3 values), free-text
  `cause` and `waitingArrivals`. If F-B makes `cause` an enum, RS's logs need
  a re-check.

## 4. Returned to the integrator

- **Proposed register row:** DEL-04-03 UPSTREAM INTERFACE → DEL-02-02. It
  carries the `run_text` / `supply_check` records for R3 and the A15
  descriptor relations. Both ends are in SCC-002, so it is held and SCC
  membership does not change. NR-08 (DEL-01-04 → DEL-04-02) is restated in
  AS §12.
- **Peer impact:**
  - D3's prototype (K-16, 9 entries) is valid against the v0.9 schema.
  - D5's `wrproto.py` (92 of 92, P-38: 12 A15 records) passes against the v0.9
    schema in a scratch copy.
  - CA's `run_w14_rehearsals.py` currently reports 1 failure, in CA's own
    `w14-result-record` example (`counts_toward_out003`,
    `not_counted_reason`). It fails the same way with the **v0.8** RS files
    restored, so it is not caused by F-C. It probably comes from parallel
    CA or WR edits; it is for F-D or the integrator.
- **New UNRESOLVED:** U-32 (SEAL-2, conditional) and U-33 (email or digest).

## 5. Rerun output

**RS prototype**, run 2026-10-02 with Python 3.13.7 on macOS:
`python3 -B run_prototype.py "$TMPDIR/fc-final"` in DEL-04-03
`Design/prototype/`. Exit 0, 63 PASS, 0 FAIL.

```text
loaded ACT schema urn:chirality:app-v4:del-04-01:policy-class-record:0.1 (subset check passed)
loaded AS schema urn:chirality:app-v4:del-04-02:settings-in:0.1 (subset check passed)
loaded RS schema urn:chirality:app-v4:del-04-03:rs-record:0.1 (subset check passed)
== example instances ==
PASS ACT … valid; INV-ACT-1…3 invalid as expected
PASS AS VAL-AS-1, VAL-AS-2 valid; INV-AS-1…4 invalid as expected
PASS RS INV-RS-1 … INV-RS-24 invalid as expected (each one cause; e.g.
  INV-RS-16: relations: additional property 'derivedFrom' not allowed;
  INV-RS-17: relations.priorRevision matches 0 oneOf branches;
  INV-RS-22: decisionActor.codexAccount matches no anyOf branch;
  INV-RS-23: body.basis 'inherited' not in enum)
PASS RS RS_RECORD.valid.act-log.example.jsonl: 4 entries valid
PASS RS RS_RECORD.valid.app-chained-run.example.jsonl: 8 entries valid
PASS RS RS_RECORD.valid.app-run.example.jsonl: 20 entries valid
PASS RS RS_RECORD.valid.host-destinations.example.jsonl: 12 entries valid
PASS RS RS_RECORD.valid.host-run.example.jsonl: 20 entries valid
PASS RS RS_RECORD.valid.run-not-started.example.jsonl: 1 entries valid
== write and read back ==
PASS round trip … all six logs: entries equal=True bytes equal=True; no limits, nothing nonconformant
== failure cases (RS §14.3) ==
PASS FC-1 (3 checks), FC-2 (2), FC-3a, FC-3b, FC-4, FC-5a, FC-5b, FC-6, FC-7a, FC-7b
PASS FC-7c schema-valid A15 entries not bound to their reviewed content flagged by the reader:
  ['A15: entry 1 is not bound to its reviewed content (WR ID-2)', 'A15: entry 1 is not bound to its reviewed content (WR ID-2)']
== EXEC recorder outputs as RS entries (R14-1) ==
PASS R14-1 all 19 CE bodies have an RS kind referencing them: yes
PASS R14-1 EXEC's valid example: 12 of 12 entries valid, refused 0
PASS R14-1 other CH runs and samples: 40 of 40 entries valid
RESULT: all expectations held
```

The full console output (88 lines) is reproducible with the command above.
The abbreviated lines are shown in full in that output.

**Standard validator:** `jsonschema` 4.26.0 with a retrieval rule for the
relative references. Result: 65 of 65 valid entries, and 24 of 24 invalid
entries refused.

**ACT:** `python3 -B validate_policy.py` gave valid configuration PASS
(P-01…P-06), unique identities PASS, reserved not widenable PASS, INV-ACT-1…3
PASS, "RESULT: all expectations held".

**AS:** `python3 -B validate_settings_in.py` gave VAL-AS-1, VAL-AS-2 PASS,
INV-AS-1…4 PASS, 11 walks PASS, 9 forbidden transitions PASS, "RESULT: all
expectations held". Schema and examples are unchanged.

**Other RS-schema consumers**, run in scratch copies against the v0.9
schema:
- ADAPTER `observe_map.py`: 43 of 43 and 48 of 48 RS entries valid. Its SH-1
  run came from DEL-03-01 `run_fixture.py`, 22 of 22.
- LOOP `destination_flow.py`: 68 RS entries, all held.
- XT `run_xt_suite.py`: 0 failures.
- DEL-01-04 `run_cases.py`: 119 checks, 0 failed.
- DEL-02-02 `wrproto.py`: 92 passed.
- CA: 1 failure, which is not RS-caused (§4).
