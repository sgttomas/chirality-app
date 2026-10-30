# EB-1 question key (examiner only; frozen before any reader runs)

- **Unit:** EB-1 (DEL-10-01 EB-v0.1). Input set: `IS-EB1-1`. Brief:
  `EB1_READER_BRIEF.md`.
- **Withheld from the reader:** the manifest lists this file under
  `withheld`. Its sha256 is recorded at freeze in `RUN/OWNERS/O-E.md`.
- **Written by O-E** on 2026-10-04 from the records named per item. A key
  item names the **primary record** that must appear among the reader's
  sources.

## Scoring

| Mark | Meaning |
|---|---|
| MATCH | The substance agrees and a primary record is cited |
| PARTIAL | The substance agrees but only the index (`EXECUTION_BASIS.md`) is cited, or a required element is missing |
| MISS | No answer, or `unknown` where the records do settle it |
| CONTRADICTED | The answer conflicts with the records, or an absence is filled with an invented fact |

- **`unknown` can be correct.** Where the key says the records are silent,
  `unknown` (or a clearly labelled inference) is a MATCH. Asserting a fact
  `from_records` there is CONTRADICTED.
- **Pass requires all three:**
  1. no CONTRADICTED;
  2. every **critical** item is MATCH;
  3. at least 80% of the non-critical items are MATCH or PARTIAL.
- **Not applicable:** nothing in this key is declared not applicable (the
  R23-19 principle: such declarations are made before the run, and none is
  made).
- **Tracing misses.** Each miss is traced before any repair to one of:
  (i) an index defect, repaired in `EXECUTION_BASIS.md`; (ii) a gap in the
  underlying records, proposed to HELP_HUMAN; (iii) the reader, reported with
  evidence, never assumed.
- **Consequence for the premise.** A miss traced to (ii) on a critical item
  means the existing records do not carry the basis on their own, which is
  the premise EB-1 tests. That result goes to HELP_HUMAN before DEL-10-02 or
  DEL-10-04 expands.

## Key

### Q1 Manual editions

| ID | Expected | Primary record | Critical |
|---|---|---|---|
| K1.1 | Consolidated v7 `0aafefb12e9aa728…`, Field Book v1 `cf4bd6c237f614ab…`, Agent User Manual v3 `df0297c5d77440df…`, each recomputed and equal to the record | `CURRENT_EXECUTION_BASIS.md` "Selected core editions" | Yes |
| K1.2 | Standing: the human selected the three manuals as core practice in the accepted basis. WORKING_ITEMS, as "Owning project-definition manager" (OI-017's owner), recorded the edition choices and identities for "this App-v4 definition run/current execution basis". The record says it is not broader program or other-loop adoption | `CURRENT_EXECUTION_BASIS.md` "Authority and subject"; `Open_Issues.csv` OI-017 | Yes |
| K1.3 | Later undertakings rely on the same pins while the bytes are unchanged; a changed edition needs a deliberate re-pin first | `R23_RESOLUTIONS.md` R23-31 item 3 (or OI-017's "A later or changed basis needs its own deliberate pins before reliance") | No |
| K1.4 | Reading is not adoption. The record makes the selection explicit "rather than treating a file read as adoption"; task ledgers record actual reads | `CURRENT_EXECUTION_BASIS.md` | Yes |
| K1.5 | Revision `e548d4cf…` and the seed's earlier pins are historical, not adopted | `OPERATING_METHOD.md` V4-OPS-11 | No |

### Q2 Methods of the current undertaking

| ID | Expected | Primary record | Critical |
|---|---|---|---|
| K2.1 | `construct-local-work-graph` (`chirality-root:bundled:workflow:construct-local-work-graph`, sha256 `fa04e1347f859465…`), under `loop/LOOP_INIT.md` | Pass-4 `WORK_GRAPH.md` header line "Method" | Yes |
| K2.2 | `coordinated-knowledge-work` (`bundled:chirality-root/coordinated-knowledge-work`, sha256 `44049bcd38b88378…`). The owner directed its use; HELP_HUMAN selected and recorded the source-qualified identity with its hash. "Owner selected" alone is PARTIAL; "HELP_HUMAN selected" with no owner direction is PARTIAL | `OWNER_DECISIONS.md` "Coordination method" | Yes |
| K2.3 | `coordinated-knowledge-work` is not among the definition-run pins, and neither is `construct-local-work-graph`; CURRENT_EXECUTION_BASIS pins neither | `CURRENT_EXECUTION_BASIS.md` "Selected route" table | No |
| K2.4 | Any further method the reader names (for example `project-dag` for the DAG) is cited to a record that names it | as cited | No |

### Q3 Position

| ID | Expected | Primary record | Critical |
|---|---|---|---|
| K3.1 | 30% gate complete. The owner (Ryan) said "I have reviewed and now approve the 30% package, marking the gate complete and opening up the next phase of work towards the 60% gate." Recorder `/root` | `_DAG/DAG-001/ACCEPTANCE_RECORD.md` | Yes |
| K3.2 | Next is 60%: developed design and interfaces, and a route to completion for which further structural changes are no longer anticipated. The human assesses it, and no record shows it assessed. Saying 60% is reached or passed is CONTRADICTED | `loop/LOOP_INIT.md` ("The human assesses the 60% position …") | Yes |
| K3.3 | Positions are not effort percentages; parts may be at different positions | `OPERATING_METHOD.md` V4-OPS-04, or the index §5 with its Field Book citation | No |

### Q4 Three acts

| ID | Expected | Primary record | Critical |
|---|---|---|---|
| K4a.1 | Actor: the owner ("the human"). Words: "The human accepts it as the basis for downstream use." | Group3 `DECISION.md` | Yes |
| K4a.2 | Relayed by HELP_HUMAN ("the parent"). **Record writer: not named in the record.** `unknown`, or an inference clearly labelled, is MATCH; a writer stated `from_records` is CONTRADICTED | Group3 `DECISION.md` | Yes |
| K4a.3 | Subject `APP-V4-GROUP3-20260927-CANDIDATE-1` (reader `b5bd5ca2…` or manifest `7ad67229…`) | Group3 `DECISION.md` | No |
| K4a.4 | Custody: parent-transcribed, not a raw platform export or independent authentication; no platform identifier or timestamp; the snapshot time is a recording time | Group3 `DECISION.md` | No |
| K4a.5 | Not decided (any one): coordination policy; dependencies or a future DAG; the 30% position; implementation | Group3 `DECISION.md` "Downstream authority and limits" | No |
| K4b.1 | Actor: the owner. Words: "I accept DAG-004." Date 2026-10-03 | `_DAG/DAG-004/ACCEPTANCE_RECORD.md` | Yes |
| K4b.2 | Transcribed in run `APP-V4-SCA003-20261002`'s OWNER_DECISIONS, DECISION-3. Record written by node D2 (Type 2), which "did not witness the chat" | DAG-004 `ACCEPTANCE_RECORD.md` custody table | Yes |
| K4b.3 | Subject: the 33 files of `REVIEW_PACKET.md`, candidate assembled on basis `75764184…`; covers project-dag checkpoints 1 and 2 together | DAG-004 `ACCEPTANCE_RECORD.md` | No |
| K4b.4 | Custody: a transcription, not a raw platform export | same | No |
| K4b.5 | Not decided (any one stated limit): for example, that any input is satisfied or any work ready (handoff reading rules); no SCC ruling was needed | DAG-004 `ACCEPTANCE_RECORD.md` or `HANDOFF_STATE.md` | No |
| K4c.1 | Actor: the owner (named "Ryan Tufts" in the tranche manifest). Words: "I approve A1 and B1, go ahead". Date 2026-10-04 | `OWNER_DECISIONS_2.md`; tranche manifest `m2_gate` | Yes |
| K4c.2 | Recorder: HELP_HUMAN, in `OWNER_DECISIONS_2.md` (custody: the session transcript). The tranche manifest also records it | `OWNER_DECISIONS_2.md` header; manifest | Yes |
| K4c.3 | Subject: `AGENTS.proposed.patch` (A1 + B1) applied to Root `AGENTS.md`; resulting sha256 `f96feb19…` | Tranche manifest; notice | No |
| K4c.4 | Custody: "A record here is not a claim that the owner reviewed any file" (or the equivalent statement) | `OWNER_DECISIONS_2.md` | No |
| K4c.5 | Not decided (any one): App v4's adoption, which is HELP_HUMAN's R23-30; U-A9, ruled by HELP_HUMAN; other loops' adoption ("Your loop decides whether to adopt, amend or decline") | `OWNER_DECISIONS_2.md`; R23-30; notice | Yes |

### Q5 Open items

| ID | Expected | Primary record | Critical |
|---|---|---|---|
| K5.1 | OI-017: owning project-definition manager; "Before dependent execution relies on manual editions"; status RESOLVED_FOR_CURRENT_DEFINITION_RUN | `Open_Issues.csv` | No |
| K5.2 | OI-018: Owner with shared/project instruction owners; "Before instruction changes or dependent supply"; the App part is answered (K3 K-9, L-2) | `Open_Issues.csv` | No |
| K5.3 | OI-019: Owner with execution manager; "When consequential gap affects selected work" | `Open_Issues.csv` | Yes |
| K5.4 | OI-020: Owner; "Before revising manuals from feedback" | `Open_Issues.csv` | Yes |
| K5.5 | OI-024: Owner with affected consumers; "Before each adoption/retirement decision" | `Open_Issues.csv` | No |
| K5.6 | DEP-006: owners of affected Root/Runtime/App/Piping consumers; "Before each consumer transitions or old arrangement retires"; NOT_ADOPTED_BY_THIS_DRAFT | `External_Dependencies.csv` | No |

### Q6 Arriving agent

| ID | Expected | Primary record | Critical |
|---|---|---|---|
| K6.1 | (a) `_LATEST_ACCEPTED.md` → Group3, read **as amended** by the snapshot `_ScopeChange/_LATEST.md` names (SCA-V4-003). Omitting the amendment rule is PARTIAL | `_LATEST_ACCEPTED.md` "Reading rule" | Yes |
| K6.2 | (b) `_DAG/_LATEST.md` → DAG-004 and its handoff, with currency from `_Evaluation/DAGCurrency/_LATEST.md` (no deliverable DAG pending) | `_DAG/_LATEST.md`; currency `_LATEST.md` | No |
| K6.3 | (c) The live local `Dependencies.csv` and `_DEPENDENCIES.md`; the DAG promotes no satisfaction | DAG-004 `HANDOFF_STATE.md` "Reading rule" 2 | Yes |
| K6.4 | (d) `CURRENT_EXECUTION_BASIS.md` (plus the undertaking's own records for later methods) | itself; LOOP_INIT "Project pointers" | No |
| K6.5 | (e) `loop/LOOP_INIT.md` and the undertaking's current work graph | LOOP_INIT | No |
| K6.6 | Any three of these, each with its source: do not re-ask whether the manuals are core governance or whether decomposition may proceed (OPS §7); no repeated preparation-stage permission question (`_COORDINATION.md`); INITIALIZED is not delivered input (`_COORDINATION.md`, LOOP_INIT); no DAG rebuild merely for a new session (LOOP_INIT §1: "Graph revision is driven by changed relationships or scope, not session entry") | as listed | No |

### Q7 Whose act

| ID | Expected | Primary record | Critical |
|---|---|---|---|
| K7.a | Not the owner's: HELP_HUMAN's rulings. The owner returned K-1…K-10 to HELP_HUMAN | `R23_RESOLUTIONS.md` header; `OWNER_DECISIONS.md` "Scope of owner questions" | Yes |
| K7.b | Not the owner's: the WORKING_ITEMS function (HELP_HUMAN), R23-28 and R23-31 item 9 | `R23_RESOLUTIONS.md` | Yes |
| K7.c | Not the owner's: HELP_HUMAN's ruling R23-30 ("App v4 adopts the changed Root text") | `R23_RESOLUTIONS.md` R23-30 | Yes |
| K7.d | Not the owner's: HELP_HUMAN's ruling R23-31 item 5, recorded as an observation for the 60% discussion, "not as a departure" | `R23_RESOLUTIONS.md` R23-31 | Yes |

### Q8 Superseded or unused mechanisms

| ID | Expected | Primary record | Critical |
|---|---|---|---|
| K8.1 | At least three of: the Root-first hierarchy (V4-OPS-12); the thin-loop-file default (V4-OPS-14); dated App-v3 entry pointers (LOOP_INIT); the legacy four-document kit, semantic-lensing pipeline, schedules or unsolicited MEMORY at setup (`_COORDINATION.md`); per-manual-rule features or a copied corpus | `OPERATING_METHOD.md`; LOOP_INIT; `_COORDINATION.md` | No |
| K8.2 | No departure now awaits the owner. OI-019 and OI-020 are open but not triggered. Naming a specific pending owner departure is CONTRADICTED | Index §6; `Open_Issues.csv` | Yes |

**Counts:** 45 key items, of which 23 are critical.
