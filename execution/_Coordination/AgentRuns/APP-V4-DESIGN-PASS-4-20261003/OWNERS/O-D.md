# O-D — DEL-07-01, DEL-07-02, DEL-08-01, DEL-08-02, DEL-09-10 (owner notes and returns)

Owner O-D: Type 2 TASK, Claude Opus 5.5, high effort, standing assignment
from HELP_HUMAN (run `APP-V4-DESIGN-PASS-4-20261003`), after survey S2-D.
Basis: R23-34 (H-1, H-2, H-3, H-6…H-9 ruled as proposed; H-4, H-5 not), the
coordinator's start message of 2026-10-04. Read-only git; no network. Paths
are relative to `projects/chirality-app-v4/execution`. `RUN` = the run folder.

## CURRENT — EU-D1 refrozen for RV2 after repair round 1 (RV2-EUD1; R23-37, R23-40)

This section is authoritative. The sections below it are history. Where they
say "held" or "under RV2 review", read this section instead.

### Refrozen unit (RV2 confirms the repairs)

| File | sha256 | Change |
|---|---|---|
| DEL-07-02 `Design/CONNECTOR_FALLBACK.md` (**CFB-v0.2**) | cf805bb8f67aaa2b9d3e18e148bf44a264b40f91b143054e70cf42ea7e8bc629 | R1, R2, OD-F1 |
| DEL-07-02 `Design/connector.standing.schema.json` | bf4cef4df1ef16bc4a2a8e8fbb341798a90a48abbbe3689d68d5ce9019650719 | R2 |
| DEL-07-02 `Design/connector.route-account.schema.json` | a6823eebb2872d0d563b7e77589a0cc2f7cd2545abe654e5b427af7d79365286 | R5 |
| DEL-07-01 `Design/PEC_RECEIVING.md` (**PRC-v0.2**) | f587604c41b3d39bc1702a6a236270bf3fc31c5dc7bcecde7ebaf1b290e7bdd4 | R1, R3, R4, OD-F1 |
| DEL-07-01 `Design/pec.receiving-record.schema.json` | 1d84510d14a434890e6145b85a82d15594ea99210c17211917b1b08001e3cf37 | R2 |
| DEL-08-01 `Design/DOMAINS_RECEIVING.md` (DRC-v0.1) | 098ff6a1db6fa30d4cdeb7d465764775757381e268cb732a4250508e01d36be7 | unchanged |
| DEL-08-01 `Design/domains.receiving-record.schema.json` | 4bb8dcdc0ec7d0a269c2b05f690f22aa2192a599a4d775fc09fb4a37c1a9e302 | R2 |
| DEL-09-10 `Design/CONNECTOR_WITNESS.md` (**CW-v0.2**) | 724045de890ed354f40acc8f9c258740f731b1549b46aea261fa3000b6d1f431 | R1, R5, R6, R7, OD-F1 |
| `RUN/D/README.md` | d47d72484e1cf45f318140c07ab57d0145042a47f39ef3fa4520005a6a1db4af | Files listed |
| `RUN/D/make_fixture.py` | 213d3861c4016ddf02fed6ec4d01e13acf5b73d18b404da80955fe6e784dfae9 | P7, P8; presence citation; c9 → c8 |
| `RUN/D/eud1.py` | daaa681415f8fa08bce039c71674e2cc7a59f01eeb6d83af20e59b11f14f2225 | PR-5 content test, PR-7, Q1-S, CS-R1 per connector, build constants, per-source evidence |
| `RUN/D/run_d.py` | 4b2ec67364f940e0fd0003c2314482532ef2da54f7890719941ad14ead127fa5 | P7/P8 expectations, R2 negatives, T-9…T-11, R-2 |
| `RUN/D/fixtures/FX-EUD1/MANIFEST.sha256` (18 files) | 092626b01e0bc3959f728958645c19125d787b5b38a0718d20aa3b81013937ed | P7, P8, P1/P3 presence citation |
| `RUN/D/build/reader_input/MANIFEST.sha256` (20 items) | e68154c6d83e3856aef266ac9c22332961c1c81f4d9b8267c7505f1c7bd276bc | OD-F2: adds the adoption account and RUN_LOG |
| `RUN/D/key/EUD1_KEY.json` | 7e8422b95680170043958bfe51c0105055b0d025e32b56b4535500ac19a60deb | **unchanged** (not edited, as directed) |
| `RUN/D/reader/READER_TASK.md` | 619cef4b2761b9b5c04eee9a296b58802b871a9fd07cd57d249674c92f418ec4 | unchanged |

Beside the unit, for RV2 to see:

| File | sha256 |
|---|---|
| `RUN/D/compare_eud1.py` | ab8d710b6c6b2a2f15455942622a08d6231df648bffa128ed06f30092290a2c2 |
| `RUN/D/compare_sensitivity.py` | f795c512640294d02977a83ab058cf42fb4f21b54f31094205d4ee4109869efc |
| `RUN/D/RR-EUD1_SCORE.json` | 620f266195b31ac483c2044a05f857019ed08385a27f7fec7bac2c577eeb914a |
| `RUN/D/probe/probe_model_input.py` (P-H1b) | 4a62783e07760f58c869acfd92e3bdb0497d589d429941eed79ae50a19840c16 |

### Repairs, finding by finding

| Finding | Repair | Where | Check |
|---|---|---|---|
| **EUD1-R1 MAJOR** (R23-40) | CS-R2 restated:<br>(i) absence or limitation never implies empty work, readiness, completion or permission;<br>(ii) a relied record-tier claim reports only what its cited record states at its pin.<br>CFB §3 lists the prohibited conclusions, including completion, with CS-R5. "Done" is not a CS value. Case **P7**: Q1 asked at S (`Q1-S`), adopted and current, c1 relied as "PEC reports, from the work graph recorded at e4a0c2c4c3: … O-B1 READY, O-C1 READY". The record still names "O-B1 or O-C1 may be started or dispatched now" and "any item is ready to start, complete or permitted" as unsupported. Route account `ra:EUD1-Q1S` | CFB §2.4, §3; PRC PR-6, §9; CW QA-2 | E-P7 (relied {c1}; bases; CS-R2 named); T-9…T-11 |
| **EUD1-R2** | CS-R1 per connector (PEC `record`, Domains `admitted`). The standing schema refuses cross-connector tiers. The PEC and Domains record schemas require their own connector in every standing | standing, PEC and Domains schemas; CFB §2.3 | S-neg: RV2's Q-a, Q-b and Q-c, plus a PEC claim with a Domains tier, are refused; the unaltered PR-P1 still validates (control) |
| **EUD1-R3** | PRC §7 cites R23-37 item 1. It says which observations support "no entry": no notification and the rollout, not an items read. It records P-H1b and permits App-origin reads for App views. The open table is updated | PRC §7, §10 | inspection |
| **EUD1-R4** | PR-5 compares the cited file's **content** at the citation with the asked revision. An unreadable citation revision is `unknown` | PRC PR-3, PR-5; `eud1.py` | E-P1…P8 |
| **EUD1-R5** | `BUILD_TIME` and `BUILD_DATE` are named constants. EXP dates are `record_timestamp` with a limit stating the constant. Route accounts carry `written_at_source: build_constant`. RUN_LOG says so too | `eud1.py`; route schema; CW §4 | X-1 (EXP schema) |
| **EUD1-R6** | Per-source evidence standing: receiving records `constructed`; route accounts unlabelled (derived from real bytes); work graphs `recorded`, `static_inspection`, digest of the `git show` bytes | `eud1.py`; CW §4 | X-1, X-2 |
| **EUD1-R7** | CW-QC carries "AC-001 is not examined … do not read this record as a candidate result", and the dossier carries it forward | CW §4; QC record | X-3 (still `inconclusive`) |
| **OD-F1** (owner, from RR-EUD1) | PR-7: a record-tier citation must resolve (file, readable revision, anchor heading), or the claim is `unknown`. Presence facts cite `pec-presence:…`, not a file. Case **P8**: c3's anchor is missing, so c3 is `unknown` and (c) goes to the route. Claims renumbered (presence c9 → c8) | PRC PR-4, PR-7; fixture; CW LC-5 | E-P8; mutation "PR-7 disabled" makes E-P8 and X-3 fail |
| **OD-F2** (owner) | The reader input set now includes the authority records the supplied records cite: the OUT-004 adoption account and `RUN_LOG.json`. Raw responses and the key stay out | `run_d.py` R-1, R-2 | R-2 |

### Checks run at refreeze

- `python3 -B RUN/D/run_d.py "$TMPDIR/…" --freeze` gave 296/296.
- A second run without `--freeze` gave **297/297**, including **B-2**
  (committed `build/` equals a fresh build) and F-1 (the fixture rebuilds
  byte-identically). No `__pycache__` was left.
- Mutation runs (scratch only): staleness ignored, presence promoted,
  Domains coupled to PEC (all caught in round 0) and PR-7 disabled (caught
  now).
- `compare_eud1.py` on RR-EUD1: **45 met, 0 not met, 1 referred, of 46**,
  unchanged by the repairs. `compare_sensitivity.py`: 9/9 alterations
  caught.

### RR-EUD1 and the changed input set

- RR-EUD1's account is evidence about the input set it read (manifest
  `65700ab7…`).
- The repaired set (`e68154c6…`) adds two authority records and changes
  CFB to v0.2. Nothing the reader relied on changed meaning: P1–P6 keep
  their standings, relied claims and answers.
- The key's "c9" names the presence claim as numbered in that set, and the
  key stays as the record of what was asked. No second reader is proposed:
  the score has no miss, and the two findings were traced to my files, not
  to the reader.

### FV hand-off, restated (R23-40 items 2–3; replaces the wording in the history below)

For FV's connector waiting cause (O-A), the source is CFB-v0.2 §3,
"Prohibited conclusions", together with CS-R5:
- Connector material, its limitation or its absence never establishes that
  no work remains, that an item is ready to start, dispatchable, complete or
  permitted, or that anything is correct because of presence.
- A connector need counts as met only when CS-R1 supports reliance. Meeting
  a need is not readiness: FV decides readiness by its own file-based rules
  (V4-PM-06; RF-5a, R23-39).
- "Done" is not a CS value.

### Open, with owners (current)

| Matter | Owner | Point of need |
|---|---|---|
| RV2's confirmation of round-1 repairs | RV2 | Now |
| P1 K4 "both" vs "connector" (referred) | HELP_HUMAN | When convenient; proposed reading "met" |
| HOSTING §6.8 receiver row for DEL-07-01's App-origin reads; the -32601 note (R23-37 item 2) | DEL-01-01's owner | Their next revision |
| FV's connector waiting cause against CFB-v0.2 §3 | O-A (R23-40 item 4) | Now; RV2 checks adoption |
| `outside_coverage` value has no case | O-D | Next unit |
| IA-1, IA-3; CW-RB, CW-BD detail | O-D | Next unit |
| DEL-08-02 RTD-v0.1: schema examples, RC-1 check | O-D | Before RTD freezes; not frozen while EU-D1 is in review |

## UPDATE 2026-10-04 (after R23-37 and RR-EUD1) — history; superseded by CURRENT above

### RR-EUD1 scored against the frozen key

- **Account:** `RUN/RR-EUD1/ACCOUNT.json`, sha256 `3b31e5987c225b8aa4148bd541a8608173e763976a493b302caa703e268c8273`.
  **Key:** `D/key/EUD1_KEY.json`, `7e8422b9…0deb`, unchanged.
- **Checker:** `D/compare_eud1.py` (`ab8d710b6c6b2a2f15455942622a08d6231df648bffa128ed06f30092290a2c2`).
  It was written against this real account. Its readings of the key's
  wording are stated in its docstring so that a reviewer can challenge them.
- **Sensitivity:** `D/compare_sensitivity.py` (`f795c512640294d02977a83ab058cf42fb4f21b54f31094205d4ee4109869efc`)
  makes nine defined alterations to copies of the **real** account, and all
  nine are caught. Those alterations test that each check can fail; they are
  not author-made calibration accounts. The first version scored a "Yes"
  independence answer as *referred*; it now scores it *not met*.
- **For RV2:** the checker, the sensitivity script and the score are new
  files beside the frozen unit. They are not part of EU-D1's frozen hashes.
  RV2 should see them, as the coordinator directs.
- **Score** (`D/RR-EUD1_SCORE.json`, `620f2661…e5e`): **45 met, 0 not met, 1
  referred, of 46 items.**
  - All six PEC cases and both Domains cases: standing, relied claims,
    answers, required unsupported conclusions and forbidden conclusions are
    met.
  - Independence (K9) is met. The reader reached it by inspection, not by
    re-derivation (below).
  - **Referred: P1 K4 (a) and (c).** The reader gave basis "both" where the
    key says "connector". The reader relied on exactly c1–c7 (K2 met) and
    also checked them against the files.
    - Proposed reading: met, because "both" adds file corroboration to the
      relied-on claims and does not replace them.
    - For HELP_HUMAN to rule. The key is not changed.
- **Not a miss, a correction to my own record:** my earlier note said the
  reader input set has "20 files". It has **18 items plus the manifest** (19
  files), as the dispatch record says.

### Every point traced before any repair

| # | Point | Traced to | Finding |
|---|---|---|---|
| T-1 | c9 cites `#presence` in the work graph, and no such anchor exists (reader) | **My fixture.** `make_fixture.py` gives the presence claim a citation into `WORK_GRAPH.md` with anchor `#presence` (confirmed: `fixtures/FX-EUD1/pec/P1.json` L108; `build/records/PR-P1.json` L317; 0 occurrences of "presence" in the work graph). A presence fact has no file source: PEC-K-02 says the presence tier is "not reconstructible" and is lost on rebuild. The citation is wrong in kind. **And a design gap behind it:** PRC §4's rules never check that a citation resolves. The receiving record passed the citation through without a limit. Under PR-1…PR-6, a **record-tier** claim with an unresolvable citation could still support reliance | **OD-F1, MAJOR, owner-found.** Proposed repair:<br>• add PR-7 "a citation that does not resolve at its cited revision (path absent, or anchor not found) makes the claim's condition `unknown`, with the reason, and no reliance";<br>• cite presence facts to their presence record, never to a file;<br>• a fixture case with a record-tier claim whose citation does not resolve;<br>• a `run_d` check. |
| T-2 | The reader could not re-derive the standings (no fixtures, schemas or `eud1.py`), so its independence finding rests on the citations | **My input-set rule (R-1)** excluded every `pec/` file. That also excluded two files the records cite **as authority**: the OUT-004 adoption account (`adoption.account_ref`; the `adopted` envelope rests on it) and `RUN_LOG.json` (the evidence for the "performed" locate-compare duty) | **OD-F2, MINOR, owner-found.** A decider needs every record the shown items cite as authority: the adoption account and the duty evidence. A decider does not need `eud1.py`, the schemas or the raw constructed responses: re-deriving the standings is the examiner's and reviewer's check (CS-R4 is re-derived by `run_d` I-1). Proposed repair: R-1 includes cited authority records and still excludes raw responses and the key |
| T-3 | Reader "17 listed files" | **The reader.** A miscount; the manifest lists 18, all matched | None in my files |
| T-4 | Claim numbering skips c8 | **My fixture.** Deltas are c2–c7 and presence is c9 | Cosmetic. Renumber with the T-1 repair; it has no effect on meaning |
| T-5 | P4's unsupported list omits `correct_by_presence` | **By design.** P4 has no presence claim, and its prohibited list names all four (CS-R2) | None |
| T-6 | DM-2 lists the contract as established while its envelope is `unknown` | **By design.** There is no response to assess (CFB §2.1). The reader found it consistent | None. Could be made clearer by labelling the contract field "as configured" at the next revision |

**Repairs are held.** OD-F1 and OD-F2 change frozen files (PRC §4, the
fixture, `run_d.py`, the reader input set). I hold them so that RV2 reviews
one stable candidate. They go in together with RV2's findings, and RV2
confirms them. RV2 should treat OD-F1 and OD-F2 as known findings.

### P-H1b: the model's input on the next turn (R23-37 item 1)

- **Run within the limits.** Same as P-H1: scratch Codex 0.158.0, scratch
  home `/tmp/cvx-eud1b` (removed afterwards), the MCP double, no download, no
  sign-in, the socket guard (did not fire), and user-name and host-name
  redaction (checked clean).
- **No model was needed, and LM Studio was not started.** R23-37 permits a
  model; this probe needs none. The model's input was observed with
  DEL-01-01's OBS-2 provider tap in `--capture-only` mode on loopback. The
  tap records the exact request Codex sends to the provider and answers 400
  without forwarding it.
- **Sequence:** thread start → App-origin `mcpServer/tool/call` (result
  carries the markers `P-EX-1`, `toolReceivedAtMs` and "invented example
  material") → `turn/start` with an invented prompt that names none of them.
- **Observed** (`D/probe/results_b/`, script `probe_model_input.py`
  `4a62783e…0c16`): one `POST /v1/responses`. Its `input` has three
  `message` items (developer skills text, environment context, the prompt).
  **None of the markers appears anywhere in the request body**, and there is
  no tool-call or tool-output item. The double's tool is offered in `tools`,
  which is expected because it is configured.
- **Result under R23-37:** the model's input shows no trace of the call.
  **App-origin reads may be used for App views.**
  - Scope: 0.158.0, one custom Responses provider route, and the first
    request of the next turn.
  - PRC §7 is changed accordingly at the repair round, with OD-F1/F2, so
    that the frozen file stays stable during review.
  - The HOSTING §6.8 receiver row for DEL-07-01 goes to DEL-01-01's next
    revision. I do not edit it.

### DEL-08-02 RTD-v0.1 (draft, not frozen)

| File | sha256 |
|---|---|
| DEL-08-02 `Design/RESEARCH_TO_DESIGN.md` | 376697083a889ef35d6746ec7956fbb136f0a7659e68b2a6c88cfdc226931e5e |
| DEL-08-02 `Design/research.context-account.schema.json` | 52c36fb074a81b51d7196c428abaa2523312afb410cae52fb557bcfe08f5c179 |

It contains:
- the method model (M-1…M-8; RC-1…RC-3);
- the context account schema;
- the candidate-decision requirements CA-1…CA-9 as a PROPOSED definition
  with **no shared row** (R23-34 item 4);
- a declared-part sketch with **no checkpoint**, because WD §4.3.1 excludes
  this act;
- the contribution account;
- host questions HQ-1…HQ-6, prepared and **not relayed** (DECISION-3);
- the V4-EXM-32 design with stimuli ST-D1…ST-D6;
- the carried OI-001/002 wording (R23-34 item 8).

Still to do before it can freeze: schema examples and the RC-1 check.

## EU-D1 frozen unit (2026-10-04; under RV2 review)

The frozen hashes below stand as RV2 reviews them.

### The vocabulary is frozen

**DEL-07-02's standing vocabulary (CFB-v0.1 §2; `connector.standing.schema.json`)
is frozen at EU-D1.** FV's connector waiting cause (S-3) can be routed to O-A.
What FV needs from it:
- a connector waiting cause is the item's **standing** (`connector`,
  `envelope`, `condition`, optional `claim_tier`, `supports_reliance`,
  `reasons`) plus the **route account reference** (`ra:…`);
- a connector-dependent item is never *ready* while its standing does not
  support reliance (CS-R1), and nothing about a connector, or its absence,
  makes any item *ready*, *done* or *permitted* (CS-R2);
- `unknown` stays *unknown* (CS-R5).

Example inputs for O-A: `RUN/D/build/records/PR-P6.json` (absent),
`PR-P3.json` (stale) and `RA-Q1.json`.

### Frozen unit EU-D1

| File | sha256 |
|---|---|
| DEL-07-02 `Design/CONNECTOR_FALLBACK.md` (CFB-v0.1) | ae49d6543f92c38c3c3772c39e4fa4ebfdb53f33bedae3f0f75339dd88be33c8 |
| DEL-07-02 `Design/connector.standing.schema.json` | 589f2c5da8a9b4bc8f676a90c96ca7723539f2e4fc2c13c145e7008c6f67bdfd |
| DEL-07-02 `Design/connector.route-account.schema.json` | a3fec8d9c75d82de452145840f294cdcdabcb4484112ce1187bd080f96e45496 |
| DEL-07-01 `Design/PEC_RECEIVING.md` (PRC-v0.1) | 1a8acc8593dfb5c27faa63e5306cf636717aa07a552b68115336de349ecb379d |
| DEL-07-01 `Design/pec.receiving-record.schema.json` | ca7bbd7bf059b7f9fb1621e542b4d12b474065ba65d5b6f1055434e7cc99b0c4 |
| DEL-08-01 `Design/DOMAINS_RECEIVING.md` (DRC-v0.1) | 098ff6a1db6fa30d4cdeb7d465764775757381e268cb732a4250508e01d36be7 |
| DEL-08-01 `Design/domains.receiving-record.schema.json` | d871cd4c7e5715db7e0e154ddbc8da907a00fce60f268771c0f75346a1aafa0f |
| DEL-09-10 `Design/CONNECTOR_WITNESS.md` (CW-v0.1) | f836c7462286aa3197256c75b9fbb36cdd2e465b86a694a3e05876e0834e44f3 |
| `RUN/D/README.md` | 312d8eae8bd022f1cc2933de6b506853fd7af81248d8bf468a942d274b94b402 |
| `RUN/D/make_fixture.py` | 4593bf875ba80002520c6a06a66f73bbb2e6227534bedea55b33f4047e6c1c9f |
| `RUN/D/eud1.py` | c00835bf46fc59557ef6762e001bf0a8fc4e85cc584924f6b7c8aa5d6fd0618b |
| `RUN/D/run_d.py` | 9974d76df1f7d6509dbcec9f421b11455fc4f056f22ef69baa4d1e5ca069a77e |
| `RUN/D/fixtures/FX-EUD1/MANIFEST.sha256` (16 files) | 0d23fba7b385f864d59a214fc8c0f7c210baa2dd2d9954f75e157734adef7b74 |
| `RUN/D/reader/READER_TASK.md` | 619cef4b2761b9b5c04eee9a296b58802b871a9fd07cd57d249674c92f418ec4 |
| `RUN/D/build/reader_input/MANIFEST.sha256` (the reader's whole input set: 18 items plus the manifest) | 65700ab7d580f1b552d59d15f9a72b74c84f771e6d172dd84a8ecbd813666d37 |
| **`RUN/D/key/EUD1_KEY.json` (the question key; fixed before any reader runs; not in the input set)** | **7e8422b95680170043958bfe51c0105055b0d025e32b56b4535500ac19a60deb** |

### For the isolated reader (HELP_HUMAN dispatches)

- Input set: `RUN/D/build/reader_input/` only. Its manifest is listed above.
  The task is `READER_TASK.md` in that folder, and the answer form is
  `ACCOUNT.json`.
- The input set does not contain the key, the raw constructed PEC and
  Domains inputs, the Design files other than CFB-v0.1, or the prototype
  (check R-1).
- Comparison is item by item against the key (K1…K9 per case). Each item is
  met, not met or referred. A "forbid" item fails if the reader states that
  conclusion as supported, in any wording.
- **Not yet done:** a mechanical comparison checker. Tranche 1's lesson was
  that a checker which agrees only with its author's accounts is not
  evidence. I will write it against the first real account and have it
  reviewed against that account. I will not calibrate it on accounts I
  construct.

### Claims (what EU-D1 shows, and on what basis)

1. **One vocabulary works for both connectors.** The same three facets and
   the same reliance rule (CS-R1) classify:
   - six PEC conditions: adopted-current, not adopted, stale, partial,
     failing, absent;
   - two Domains conditions: stale with an unadmitted hit, and absent.

   No connector-specific value is needed. The basis is the rehearsal on
   constructed inputs. It is not candidate evidence.
2. **The same question, answered from real files, under every PEC condition.**
   Route account `ra:EUD1-Q1` answers Q1 from this run's committed
   `WORK_GRAPH.md` at `e4a0c2c4c3` and `e086dfff32`:
   - (a) no node is READY, ACTIVE or BLOCKED;
   - (b) T2 is PLANNED;
   - (c) six changes since S.
   Only P1 relies on PEC, for parts (a) and (c). Part (b) is outside PEC's
   orientation coverage, so it always comes from the route.
3. **No "no work" trap.** At R no node is READY, ACTIVE or BLOCKED, but T2
   is PLANNED. Every record names "no work remains" as unsupported and lists
   all four prohibited conclusions.
4. **Independence (CS-R4).** Removing the Domains inputs leaves every PEC
   record byte-identical, and the reverse also holds.
5. **DEL-09-10's records validate against EXP-v0.2** and its rules (imported
   read-only):
   - CW-EUD1-LC: `pass`;
   - CW-EUD1-OC: `pass`;
   - CW-EUD1-QC: `inconclusive`. QC-1 is `not-run` with its missing inputs
     (no qualified PEC release, no App adoption), alongside rehearsed parts.

   All three are `rehearsal` records and stand for no scenario (EXP-R3).

### Checks run

| Check | Result |
|---|---|
| `python3 -B RUN/D/run_d.py "$TMPDIR/…"`, groups F, S, E, I, T, X, B, R | **221/221**. The 221 include: B-2 (committed `build/` equals a fresh build); F-1 (fixture byte-identical on rebuild); T-7 (route sources equal `git show` bytes); 8 schema negatives refused |
| Mutation runs (scratch only, not kept) | Each mutation was caught by the checks:<br>• staleness ignored → E-P3 and X-3 fail;<br>• presence promoted to record → E-P1 CS-R1 and X-3 fail;<br>• Domains standing coupled to PEC presence → I-1 fails |
| Schemas | Draft 2020-12 `check_schema` on all four; cross-file `$ref` resolved by `$id` |
| Write fence | New files only in the four `Design/` folders, `RUN/D/` and this file. No ScopeOfWork, register, `_STATUS`, `_DAG`, scope-change, shared schema or other owner's file was touched (`git status`) |

### H-1 side probe P-H1 (R23-34.3)

- **Ran within the limits:**
  - binary: the existing scratch Codex 0.158.0 vendor binary (sha256 prefix
    `788a818fbb959686`), not the `codex` on PATH;
  - home: `CODEX_HOME` and `HOME` under `/tmp/cvx-eud1`;
  - MCP server: DEL-01-01's `obs1_mcp_double.py`, copied there;
  - no model: the provider points at loopback port 9 and no turn was
    started;
  - no sign-in, no download;
  - plugins and analytics off;
  - guard: `lsof` every 250 ms on the process group stops the probe on any
    non-loopback socket or `git` process. It did not fire.
  - `/tmp/cvx-eud1` was removed afterwards.
- **Observed at 0.158.0, one route** (`RUN/D/probe/results/`, redacted;
  `probe_mcp_call.py` sha256 `d3dd3b670ff60ed95346fb5f2d975d9e975dc05c29a25cb46e04e4247309c932`):
  1. `mcpServer/tool/call` returned the tool's result (content and
     structured content) to the App.
  2. The MCP server received the call with `_meta.threadId` set to the
     thread.
  3. No notification followed the call within 3 s (no `item/*`).
  4. The thread's persisted rollout file held one line and no trace of the
     call (neither the tool name nor its result).
  5. `thread/items/list` and `thread/read` with turns answered -32601 "not
     supported yet" / "list_turns is not supported yet" for this thread,
     which had no turn (`experimentalApi: false`).
- **Not observed:** whether a later turn's model input would include the
  call. That needs a model, which the limits exclude.
- **Question for HELP_HUMAN (INTEGRATION):** does this settle HOSTING §6.8's
  "not observed" point enough to use App-origin reads for DEL-07-01's
  presentation?
  - My reading: observations 3 and 4 settle "thread items or history" as
    *no entry* on this route at 0.158.0.
  - "Model context" is settled only by inference: the history a later turn
    sends carries no trace.
  - Until the ruling, PRC §7 keeps App-origin reads unused.
- **For DEL-01-01's owner (observation only, no file changed):**
  - The -32601 answers to `thread/items/list` and `thread/read` (with turns)
    on a turnless thread bear on WR SC-3, RECOVERY R-4 and NPTD SQ-1. All
    three page with `thread/items/list`.
  - The receiving server also gets the thread id in `_meta`.
- **Run note:** the probe ran twice. The first run's scratch output carried
  the machine's host name in a `remoteControl/status/changed` notification.
  It was deleted unkept, the redaction was extended to the host name, and
  the probe was rerun. The kept results contain neither the user name nor
  the host name (checked by grep and by the script's own redaction check).

### Departures from the survey's wording (within R23-34; stated for review)

- **The Domains envelope** takes the same values as PEC's: `adopted` means
  an identified query contract with an established admission basis. The
  survey had proposed "not applicable for Domains". With that value, CS-R1
  could never allow Domains reliance. R23-34 item 1 fixes the facets and
  the rule, not the values.
- **`unknown` was added** to envelope, condition and tier. It is the value
  that is never promoted (CS-R5), as in FR and FV.

### Open, with owners

| Matter | Owner | Point of need |
|---|---|---|
| FV connector waiting cause (S-3) | O-A, routed by HELP_HUMAN | Now (vocabulary frozen) |
| P-H1 ruling | HELP_HUMAN | Before PRC §7 uses App-origin reads |
| Reader comparison checker | O-D | When the first reader account returns |
| `outside_coverage` envelope value has no EU-D1 case (part (b) is handled as "not covered" at the conclusion level) | O-D | Next unit |
| IA-1, IA-3; CW-RB, CW-BD detail | O-D | Next unit |
| DEL-08-02 RTD-v0.1 (method; act requirements as a PROPOSED definition, R23-34.4) | O-D | In parallel, not frozen while EU-D1 waits for review |
| OI-022 PEC-side terms; OI-023/OI-026 Domains | External / the person at their points of need (R23-34 preamble) | Later |

### Escalations

None. No earlier Design file is restructured, no register row is proposed,
no owner act is requested or implied, and no check is weakened.
