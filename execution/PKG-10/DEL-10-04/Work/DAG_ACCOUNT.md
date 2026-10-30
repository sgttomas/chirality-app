# Project production dependency DAG — evidence account over DAG-001…DAG-004

- **Contribution:** DEL-10-04/DA-v0.3. It supersedes DA-v0.2 (`738f8287…`, committed at `8525b7fa53`; RV3: READY with DA2-R1 MINOR and one note), which superseded DA-v0.1 (`611adec3…`, committed at `68f83d6b20`); see "Changes". It serves OUT-001 and OUT-002 by
  mapping every obligation to the records that already meet it (§2–§4), and
  sets the currency procedure for the rest of this pass (§5).
- **Status: DRAFT DEFINITION, frozen for RV3** with UC-v0.2 and EB-v0.4.
  Owner O-E (Type 2 TASK, Claude Opus 5.5), run
  `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-04.
- **What it is (R23-31.1):** an index. The graph, its cases and its currency
  records are the authority. This file writes nothing under `_DAG/`,
  `_Evaluation/`, registers or ScopeOfWork.
- **Basis:**
  - this deliverable's `ScopeOfWork.md`, sha256
    `fb62502a0f59b226607ed6a04cbbd9ffbafab35edcfe45a1a7307cfcc80d2177` (INIT
    contract; no SCA block changed it);
  - the method `chirality-root:bundled:workflow:project-dag`, WORKFLOW.md
    `e5db3660…` (pinned in CURRENT_EXECUTION_BASIS and bound in
    `RUN/BASIS_BINDING.md`), with resources contract `a55edc3b…`, method
    `4a5566bf…`, graph-version `ff6b7ba5…` and currency `d2927ed4…`;
  - Root SPEC §5.4 and §11.2.
- **Rulings:** R23-2 (reach before any proposed row), R23-21, R23-31 (items 1
  and 9), R23-38.
- **Labels:** SETTLED, DERIVED, INTEGRATION and PROPOSED. **States**,
  **Inference** and **Checked by O-E** are kept apart.
- **Paths:** `E/` = `projects/chirality-app-v4/execution/`.

## 1. Standing (states)

- **The contract's result exists, four times over.** The SoW defines "one
  identified, examined and human-accepted project production dependency DAG
  before the 30% position".
  - DAG-001 was accepted in the act that completed the 30% gate.
  - DAG-002, DAG-003 and DAG-004 are accepted successors.
  - `E/_DAG/_LATEST.md` names DAG-004 (SPEC §11.2 form), accepted 2026-10-03:
    "I accept DAG-004."
- **Inference.** What remains of DEL-10-04 is maintenance: currency
  (REQ-007), any successor a departure requires, and keeping the records
  their consumers rely on findable (§6).

## 2. The versions

| Version | Accepted | Owner's words (exact, as recorded) | Recorder of the act → record writer | Admitted / held / excluded / nodes | Independent review | Strict audit, rerun by O-E 2026-10-04 |
|---|---|---|---|---|---|---|
| DAG-001 | With the 30% gate (`E/_DAG/DAG-001/ACCEPTANCE_RECORD.md`) | "I have reviewed and now approve the 30% package, marking the gate complete and opening up the next phase of work towards the 60% gate." Also the hold: "DO NOT BEGIN THE WORK TOWARDS 60%.  We are handing that off." | Chat transcribed by `/root` (taking over WORKING_ITEMS' closeout) | 109 / 52 / 242 / 41 | `INDEPENDENT_REVIEW.md`: "PASS — no unresolved blocking finding …" | exit 0; 109 edges, 0 SCCs, 0 duplicates |
| DAG-002 | 2026-09-29, checkpoints 1 and 2 together | "Accept DAG-002 (Recommended)", plus the N-18/N-21/N-24/X-1 answer | Run `APP-V4-BASIS-ALIGN-20260928` DECISION-10 → node D2, which did not witness the chat | 124 / 74 / 264 / 41 | "READY FOR CHECKPOINT C" | exit 0; 124, 0 SCCs |
| DAG-003 | 2026-09-29, checkpoints 1 and 2 together | "Accept DAG-003 (Recommended)" | Run `APP-V4-SCA002-20260929` DECISION-4 → node D2 | 124 / 78 / 263 / 41 | "READY FOR CHECKPOINT C" | exit 0; 124, 0 SCCs |
| DAG-004 | 2026-10-03, checkpoints 1 and 2 together | "I accept DAG-004." | Run `APP-V4-SCA003-20261002` DECISION-3 → node D2, which "did not witness the chat" | 129 / 83 / 355 / 41 | V25: "READY FOR CHECKPOINT C", 0 BLOCKING, 0 MAJOR | exit 0; 129, 0 SCCs |

How these columns were checked by O-E:
- **Counts:** CSV records, parsed with Python's `csv` module. Line counts
  overstate them because cells span lines.
- **Integrity:** each version's `MANIFEST.sha256` passes `shasum -c` with no
  failures (61, 37, 37 and 37 entries).
- **Audit:** `tools/coordination/audit_dag.py` (sha256 `830d0d53…`) was run
  with `--canonical --strict --dag-dir <version>`, writing its JSON and
  Markdown output only to scratch.
- **Quotes:** from each `ACCEPTANCE_RECORD.md`.

**Inference.** The counts agree with each handoff (DAG-004: "129 admitted
arcs … 83 held … 355 exclusions").

## 3. Obligation → evidence (OUT-001, OUT-002; REQ-001…REQ-009)

| Obligation | Where it is met | Standing |
|---|---|---|
| REQ-001 objective, semantics, direction, tracking, completeness, frozen inventory (AC-001; VER-001) | Each version's `GRAPH_BASIS.md`. DAG-004 `HANDOFF_STATE.md` "Objective, semantics, direction and completeness": FULL under FULL_GRAPH; 41 nodes, no exemptions; inventory GROUP3 `Deliverables.csv` | Met (states) |
| REQ-002 relationship fields and provenance; DECLARED vs extracted; mirrors (AC-002; VER-002) | Edge CSVs with `SourceRegister`, `SourceRegisterSHA256`, `SourceRecord`, `SelectionRule`; `ExcludedRows.csv` dispositions (MIRROR, NOT_TOPOLOGICAL, SAME_ARC); `SOURCE_MANIFEST.sha256` (130 entries) | Met (states); fidelity reviewed per version (V25 and earlier) |
| REQ-003 external contributions and open matters at their point of need; pending delivery does not block acceptance (AC-003; VER-003) | The SoW's own DEP-001…DEP-006 account; non-topological exclusions keep them visible; DAG-004 was accepted with every row's satisfaction TBD or PENDING | Met. §4 rechecks the account against today's External_Dependencies |
| REQ-004 coverage before topology; acyclic admitted layer; strict audit; each active row once; cycles held and non-gating (AC-004; VER-004) | `E/_Evaluation/DepClosure/` (five closure snapshots); strict audit on each version (§2); candidate edges with `SCCRef` and `CaseRef`; seven cases under `E/_DAG/cases/` | Met. O-E reran the strict audit: all four exit 0 |
| REQ-005 basis and version checkpoints as decision packages; examiner ≠ assembler (AC-005; VER-005) | DAG-001: `E/_DAG/_Candidates/DAG-001/BASIS_DECISION.md` (checkpoint 1), `BASIS_REVIEW.md`, `REVIEW_PACKET.md`, `GATE_READER.md`. Successors, each with `CHECKPOINT_C.md` and `REVIEW_PACKET.md` and a separate reviewer: DAG-002 in `E/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/` (`CHECKPOINT_C.md` `6ff6dd96…`); DAG-003 in `…/APP-V4-SCA002-20260929/DAG_PREP/` (`f8f63e80…`); DAG-004 in `…/APP-V4-SCA003-20261002/DAG_PREP/` (`710de584…`). Each hash equals the "Package presented" row of that version's `ACCEPTANCE_RECORD.md` (checked by O-E) | Met (states and checked) |
| REQ-006 decision records with actor, custody, subject hashes; immutable version; pointer only to the accepted version (AC-006; VER-006) | `ACCEPTANCE_RECORD.md` per version (custody tables; actor ≠ recorder); `MANIFEST.sha256`; `_LATEST.md` names only DAG-004 | Met. Integrity checked by O-E (§2) |
| REQ-007 currency: unchanged, evidence drift, departure, incomplete; DAG pending; successor or rejection (AC-007; VER-007) | `E/_Evaluation/DAGCurrency/`: eight observations. Three DEPARTUREs (BASISALIGN, SCA002, SCA003), each followed by an accepted successor; CURRENT after each acceptance; latest CURRENT_WITH_EVIDENCE_DRIFT (DEL-01-03 TargetLocation repair) | Met to date. Ongoing: §5 |
| REQ-008 INITIALIZED is contract maturity only; no self-bootstrap; acceptance passes nothing else (AC-008; VER-008) | DAG-004 handoff "Reading rule"; DAG-001 "Reliance boundary"; DAG-004 "This acceptance does not" | Met (states) |
| REQ-009 no act owned by others (AC-009; VER-009) | The human decided every version; the one source repair since DAG-004 (DEL-01-03's 14 absolute TargetLocation values) was made after acceptance under DECISION-3 effect 4, as the latest currency observation records; no cut or merge ruling exists. Each case's `Ruling_Register.csv` holds one row, `CP1-20260928` ("Confirm full contribution/default selection; characterize unresolved S…"), status `RECORDED_ACTUAL_BASIS_ONLY` | Met (states). VER-009: `check_boundary_owner_resolution.py` (`22ef57e0…`) on this SoW checks 1 boundary requirement, 0 failing, 0 citing no claim (O-E, 2026-10-04). Semantic follow-up: §3 and §5 leave every act named in CLM-001…003 with its owner |

## 4. Interface account recheck (REQ-003; VER-003)

**Method.** The frozen Group3 `canonical/External_Dependencies.csv` was
compared field by field with today's
`E/_Decomposition/External_Dependencies.csv` (`055703d9…`; last commit
`941c4d35f9`), by script, on 2026-10-04 (checked by O-E).

| Row | Changed since frozen? | Present satisfaction now | Later facts, from run records | Effect on an arc |
|---|---|---|---|---|
| DEP-001 SWBPIPE | No | OWNER_REPORTED_BUILDING_BEFORE_AGENT_ACTION_INTEGRATION | Host joins deferred (DECISION-3 of `APP-V4-SWBPIPE-INTAKE-20260928`) | None |
| DEP-002 PEC | **Yes:** PresentSatisfaction, SourceRef, BoundaryAndFallback | OPTIONAL_RECEIVING_QUALIFICATION_UNESTABLISHED_AT_ffb2b6289 | D108 receiving metadata (a later fact; the Group3 decision says so). R23-34 H-1/H-2/H-7 (consumption only through the person's own Codex MCP configuration; adoption is two facts) | None |
| DEP-003 Domains | No | OWNER_REPORTED_KNOWLEDGE_OUTSIDE_REPO_PARALLEL_LATER_JOIN | OI-023 and OI-026 open; R23-34 places the start of the Domains-enabled increment with the person | None |
| DEP-004 distribution terms | No | UNCONFIRMED | — | None |
| DEP-005 pinned suppliers | No | VERSION_AND_ENVIRONMENT_TO_DEFINE | **The row lags later decisions.** First increment D4 pinned Codex 0.158.0 for definition and generation. R23-22 recorded 0.160.0 as checked, with the qualification pin chosen when a candidate is built | None. **Observation:** the row's text predates D4 and R23-22. Updating it is its owner's act at the next amendment (R23-11 practice); DEL-10-04 records it and writes nothing |
| DEP-006 consumer adoption | No | NOT_ADOPTED_BY_THIS_DRAFT | D-GOV-52: App v4 adopted (R23-30); App v3 and Runtime "notice delivered; receiving decision not recorded" (R23-32 F-R16) | None |

**Result.** No change to an external row alters an arc or a reading rule.
DAG-004's acceptance did not wait on any external delivery, and none is
claimed (REQ-003, AC-003).

## 5. Currency through the rest of this pass (REQ-007; DERIVED from SPEC §5.4, `project-dag` currency resource, R23-2)

1. **Before a row is proposed (R23-2).**
   - **The test, in arc terms.** A proposed row C → S (C consumes S's
     contribution) forms a cycle exactly when S already reaches C over the
     accepted DAG's admitted and held layers. The row is then an SCC-forming
     departure for its owner and `scc-resolution-case`.
   - **Other outcomes.** A row whose arc C → S already exists adds no arc.
     A row where S does not reach C adds an arc and forms no cycle; it is
     still an added-arc departure for the next currency audit.
   - **The script (the project's reach script, R23-51).**
     `prototype/dag_reach.py CONSUMER SUPPLIER` performs this check against
     the version `_DAG/_LATEST.md` names, or against a version given with
     `--dag`. It prints the version it read. It exits 2 for
     SCC-forming and 0 otherwise. Its `--self-test` always reads DAG-004,
     whose facts its five cases record, and skips with a notice if DAG-004
     is absent. Cases include for example DEL-02-04 → DEL-10-03 is SCC-forming and
     DEL-06-01 → DEL-10-02 is not.
2. **At the pass closeout.** Rerun `shasum -c _DAG/DAG-004/SOURCE_MANIFEST.sha256`
   from `E/`, and run the currency audit if any source differs beyond the
   recorded DEL-01-03 drift.
   - **Checked by O-E 2026-10-04:** 128 of 130 OK; the two failures are the
     DEL-01-03 files the latest observation already records.
3. **On a departure.**
   - The affected deliverables are DAG pending; dependencies give them no
     ready or blocked verdict.
   - A successor is prepared, and only the decisions it affects reopen.
   - The successor's acceptance, or the rejection of the change, is
     **reserved to the person**. SPEC §5.4: "Authority comes from the
     human's acceptance". SoW CLM-001: "The human owner decides … acceptance
     or rejection of departures."
4. **What does not trigger a successor.** A new session, a rearranged
   assignment, satisfaction progress, or a further row on a represented arc.
   DAG-004 handoff: "A new session is not, by itself, a reason to rebuild";
   SPEC §5.4.

## 6. Consumers (handoff)

| Consumer | Uses | Record |
|---|---|---|
| `construct-local-work-graph`, every undertaking graph | Accepted pointer, handoff reading rules, currency | `_DAG/_LATEST.md`; DAG-004 `HANDOFF_STATE.md`; `_Evaluation/DAGCurrency/_LATEST.md` |
| DEL-10-02 (held arc DEP-10-02-012, SCC-005) | Graph-based selection uses the accepted current version | DEL-10-02 UC §8 |
| DEL-10-01 | Basis chain rows B-7 and B-11 | EB §2 |
| DEL-06-01 (FR's `projectDagRef`) | A reference string only; the App reading a user's DAG is unowned and not added (R23-31.10) | FR-v0.1 |

**The SCC-CASE-006 pair (R1; S2-E E2-9).** Graph production consumes, from
DEL-10-02, the subset UC §8 names:
- the current work graphs;
- the controls map;
- the capability account.

Graph-based selection consumes this file's §5 and the accepted pointer. No
cut or merge is proposed.

## 7. Cases (REQ-004; checked by O-E from `E/_DAG/cases/`)

- **Where the state is read.** "State" comes from each case's
  `Case_Datasheet.md`, written after CP1. Each `Case_Contract.md` still reads
  `HUMAN_RULINGS_PENDING` from before CP1 (RV3 DA1 N1).
- **Recommendations are not rulings.** "Recommended treatment" quotes the
  datasheet's own recommendation, which stays unruled in every case. The
  only ruling recorded is CP1-20260928, the basis-only ruling.

| Case | Members (DAG-004 handoff) | State (datasheet) | Recommended treatment (datasheet; unruled) | Rulings | Last committed change |
|---|---|---|---|---|---|
| SCC-CASE-001 | DEL-01-01, DEL-01-05 | EVIDENCE_ACCUMULATING | R1, "retaining R3 wherever a required input remains absent" | CP1-20260928 (basis only) | `0139b067dc` (2026-09-27) |
| SCC-CASE-002 | 13 (SCC-002) | EVIDENCE_ACCUMULATING | R-01 and the targeted R-03 limitations; R-02 only as a limited alternative | CP1-20260928 | `b547125dbe` (2026-09-29) |
| SCC-CASE-003 | 2 (SCC-003) | EVIDENCE_ACCUMULATING | R1, "coordinate explicit support and candidate-return contributions under existing owners" | CP1-20260928 | `0139b067dc` |
| SCC-CASE-004 | DEL-03-01, DEL-03-02 (history under CASE-002) | EVIDENCE_ACCUMULATING | R004-A (coordinate C and P under both owners); R004-B an objective-dependent alternative. **Per the datasheet's later lineage section ("Refreshed observation and proposed case lineage — ruling pending"):** R004-A/C "remain useful **local** inquiry for the expanded CASE-002 account"; "R004-B's conditional pair-view alternative cannot stand as a remedy for the 13-member component" (ruling pending) | CP1-20260928 | `0139b067dc` |
| SCC-CASE-005 | 3 (SCC-004) | EVIDENCE_ACCUMULATING | R1, "with R3 applied only at a demonstrable missing-input point" | CP1-20260928 | `0139b067dc` |
| SCC-CASE-006 | DEL-10-02, DEL-10-04 (SCC-005) | EVIDENCE_ACCUMULATING | R1, "coordinated contributions, unresolved candidate topology" | CP1-20260928 | `0139b067dc` |
| SCC-CASE-007 | DEL-11-01, DEL-11-03 (SCC-006) | EVIDENCE_ACCUMULATING | R1 (the treatment R23-32 F-R8 relies on for DEL-11-03's design) | CP1-20260928 | `0139b067dc` |

- **Observation (states).** DAG-004's handoff says CASE-002's evidence update
  for this version "is drafted
  (`…/APP-V4-SCA003-20261002/DAG_PREP/CASE-002_EVIDENCE_UPDATE.proposed.md`)
  and is applied separately through `scc-resolution-case`". CASE-002's last
  committed change is `b547125dbe` (2026-09-29), before DAG-004. **The update
  is not yet applied.** Applying it is the maintainer's act, through
  `scc-resolution-case`. DEL-10-04 records the fact and writes nothing.
- **No case needs a ruling** for DAG-004 ("No SCC needed a ruling", DAG-004
  acceptance). Cut and merge rulings stay reserved to the person if one is
  ever proposed (CLM-001).

## 8. Open

| Item | Owner | Point of need |
|---|---|---|
| Apply CASE-002's drafted evidence update for DAG-004 | HELP_HUMAN, through `scc-resolution-case` | Before the next closure or currency observation relies on CASE-002 |
| DEP-005's row text lags D4 and R23-22 | The row's owner, at the next amendment (R23-11 practice) | Next amendment |
| Currency at the pass closeout (§5 step 2) | HELP_HUMAN or the closeout node | Pass closeout |

## Changes

**DA-v0.3 (2026-10-04), after RV3-DA1 addendum (DA-v0.2 READY):**

| Change | Cause |
|---|---|
| §7 CASE-004 row adds the datasheet's later lineage update: R004-A/C local inquiry for CASE-002; R004-B "cannot stand as a remedy for the 13-member component" (ruling pending) | DA2-R1 |
| `dag_reach.py` prints the DAG version it read and how it was chosen. `--dag` names a version. The self-test is pinned to DAG-004 and skips with a notice if DAG-004 is absent. §5 names the script as the project's reach script | Note; R23-51 |

**DA-v0.2 (2026-10-04), after RV3-DA1 (READY; 2 MINOR, notes):**

| Change | Cause |
|---|---|
| §5 step 1 states the cycle test in arc terms (C → S forms a cycle iff S already reaches C over both layers), and names the new `prototype/dag_reach.py`, with a self-test | DA1-R1 |
| §7 gives each case's recommended treatment from its datasheet (R1 for 001, 003, 005, 006 and 007; R-01/R-03 for 002; R004-A for 004), all unruled. It names the datasheet as the source of the state | DA1-R2; N1 |

