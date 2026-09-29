# REGISTER_CHANGES: refreshed C1 register proposals (node P2)

This record prepares the register changes that the successor DAG (DAG-002) needs. It changes no register. The C1 proposals are re-checked against the current Design files and the R8 intake, and the result is given as exact rows.

- **Run and node:** `APP-V4-BASIS-ALIGN-20260928`, node P2 (DAG successor preparation). This is **preparation only**.
- **Executor:** Type 2 TASK, a Claude Code `Agent` subagent dispatched by HELP_HUMAN. It does not delegate.
- **Basis:** commit `874508f16`, with a clean working tree. Git was read-only and no network was used.
- **Methods loaded:**
  - `chirality-root:bundled:workflow:project-dag`: `WORKFLOW.md`, `contract.md`, `method.md`, `graph-version.md` and `currency.md`;
  - `chirality-root:bundled:workflow:dependency-extract`: `WORKFLOW.md` and `resources/brief.md`;
  - `docs/SPEC.md` §5 (§5.1–§5.4) and §6.8.
- **Inputs:**
  - C1 records `closeout/C1-A.md`, `C1-B.md` and `C1-C.md`, and `CLOSEOUT_ACCOUNT.md` (run `APP-V4-FIRST-INCREMENT-20260928`);
  - DAG-001 (`_DAG/_LATEST.md` → `DAG-001/`);
  - all 41 `Dependencies.csv` and the in-scope `_DEPENDENCIES.md` at `874508f16`;
  - the current Design files (post-R8 and R8-13);
  - `APP-V4-SWBPIPE-INTAKE-20260928` `OWNER_DECISIONS.md` (DECISION-3, DECISION-4 and DECISION-5), `R8_RESOLUTIONS.md` and `RECEIPT.md`;
  - `_Coordination/_COORDINATION.md` (the accepted dependency rules).
- **Written:** only files under this `DAG_PREP/` folder. No register, `_DEPENDENCIES.md`, ScopeOfWork, `_STATUS`, `_DAG`, `_Evaluation` or Design file was edited.
- **Companions:**
  - [ARC_ANALYSIS.md](ARC_ANALYSIS.md): arcs, SCCs, the disputed arc and layer placement;
  - [SUCCESSOR_PLAN.md](SUCCESSOR_PLAN.md): currency, TRIGGER=SUCCESSOR, reviews and owner items;
  - [`proposed_rows/`](proposed_rows/): exact rows in the 29 canonical columns;
  - [`evidence/`](evidence/): the scripts and outputs, which can be rerun from the repository root.

## 1. What was checked

**The current registers are the DAG-001 evidence.**
- `shasum -a 256 -c _DAG/DAG-001/SOURCE_MANIFEST.sha256`, run from the execution root, passes for all 130 files.
- Re-deriving the arcs from the 41 live registers gives exactly DAG-001's 161 arcs: 109 admitted and 52 candidates (`evidence/scc_result.json`, `S0_equals_DAG001: true`).
- No register, SoW or `_DEPENDENCIES.md` has changed since DAG-001. R6, R7, R8 and R8-13 changed Design files only.

**Every C1 row was checked by script** (`evidence/verify.py`, `evidence/verified.json`):
- **Mirror rows:** the counterpart `DependencyID` exists, is `ACTIVE`, and lies on the same consumer → supplier arc (55 of 55).
- **New-arc rows:** the arc is absent from both DAG-001 layers (all 40 C1 arcs).
- **Row edits:** the named row exists.
- **Evidence:** each kept deliverable-target row has a corroborating line in the host's current Design file, located by pattern, with line number and quote.

**The C1 counts reconcile.** C1's "about 76 mirror rows" are:
- 55 distinct mirror rows;
- 9 duplicates, where C1-B restates C1-A rows (M-02-5, M-02-6, M-02-7 and M-03-2, plus 5 of the 12 DEL-03-04 supplier mirrors);
- 12 C1-C row edits and EXTERNAL rows that C1-C counted as "mirror only".

All 156 distinct items are dispositioned below.

## 2. Rules applied in this refresh

### 2.1 Grounding: which rows extraction may write

The accepted coordination rule (`_Coordination/_COORDINATION.md`, "Accepted rules") reads:

> "Agent-proposed candidates derive from local SoWs and accepted interfaces."

DAG-001's registers were extracted from `ScopeOfWork.md` alone. The DEL-04-02 Run Notes, for example, record `SOURCE_DOCS=ScopeOfWork.md` and "Sibling source contracts were not read". Every Design file is marked "DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted". A Design file therefore **corroborates** a row but does not **ground** it.

A row is marked **extraction** (`dependency-extract`, `MODE=UPDATE`, `CONSERVATIVE`) only when one of these puts the relationship into the host's SoW:
- a C1 SoW correction, applied through `scope-of-work` REVISE after K1 (P1 prepares these); or
- the current SoW text.

The grounding correction is named on every row.

Where no SoW sentence grounds an arc, the row is marked **"extraction after P1 wording, else declaration"**. There are two ways to ground it:
- P1 adds a consumption sentence to the host SoW, traced to the accepted C1 arc proposal; or
- the owner declares the relationship in the human-owned `_DEPENDENCIES.md` section, and `dependency-extract` mirrors it as `Origin=DECLARED`.

Which way is used is owner item **O-2** (SUCCESSOR_PLAN §4). Nine arcs are in this state. They are listed in ARC_ANALYSIS §2.3.

Two consequences follow:
- **Optional supplier-side mirrors** whose receiver no SoW sentence names are **DEFER**. They cannot be extracted under the accepted rule. The consumer's row already represents the arc under SR-6, and DAG-001's reading rule already sends readers to the consumer registers. The owner may declare them instead (**O-3**).
- **Rows in registers outside the first increment** (DEL-02-04, DEL-07-01, DEL-07-02, DEL-08-01 and DEL-08-02) are **DEFER**. This matches C1-A's "noted but not proposed (D1)".

### 2.2 Refresh against R6–R8 and DECISION-3/4/5

- **D6 and SQ-02.** C1's EXTERNAL rows targeting "DECISION-2 D6 / relay SQ-02" are **retargeted**. D6 is closed for Phase 1 by DECISION-4 D4-1 and re-opens with the governance phase (R8-2); SQ-02 is answered: route (iv), none planned. Each row becomes a CONSTRAINT to the governance-phase re-opening (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4`).
- **Hold support.** Arcs grounded on hold-support values are kept, with their Statements **amended** to two phases. The values are retained as the governance-phase definition, not deleted (R8-1), and each consumer still reads the Phase-1 statement, the compatibility report or the annotations. This covers N-02, N-13, N-17, N-25, N-26 and N-27.
- **Relay standing.** Rows that said "prepared, not delivered" now say *relayed and answered 2026-09-28*. The answers are not commitments (DECISION-3). This covers R5-1-3, R5-1-5, R5-2-5, R5-2-6, R9-6-7 and R9-9-5.
- **New rows from R8-13 (DECISION-5).**
  - **R8-A** (DEL-04-02 → DEL-05-01): AS §3 takes its network-destination display from LOOP §5.1.1.
  - **R8-B** (DEL-04-03 → DEL-05-01): RS R15 names its source as "through DEL-05-01 events (LOOP §2.3, §5.1.1)".
  - **R8-LOOP-1**: an EXTERNAL CONSTRAINT in DEL-05-01 for the V4-HOST-02 basis revision and LOOP N-OPEN-4.
- **OI-021 remains open** (R8-10), so the OI-021 rows are kept. DECISION-1 (D2/D3) is ruled, so it is carried in Notes and no longer held as an open constraint (R-02-01-l amended).

### 2.3 Currency classes (project-dag `currency.md`)

| Class used below | Meaning for the successor |
|---|---|
| **creates N-xx (admitted / candidate)** | Adds an arc. This is a **DEPARTURE**, and both endpoints become `DAG pending` |
| **drift (MIRROR)** | A further row on an arc DAG-001 already represents. `CURRENT_WITH_EVIDENCE_DRIFT` |
| **drift; new SR-6 representative** | A consumer `UPSTREAM` row on an arc that DAG-001 represents with a supplier `DOWNSTREAM` row. The arc set is unchanged, but the representative row in DAG-002 changes: R-04-02-a, R-04-03-a, R-04-03-b and R-04-03-c. Drift |
| **drift (non-topological)** | A row edit, an EXTERNAL row or a package row. Drift |
| **none (not applied)** | DEFER or DROP |

No proposed row **removes** an arc. The package rows DEP-03-01-022, DEP-04-03-012, DEP-09-06-012 and DEP-09-06-014 are **kept**, because their SoW sentences are unchanged. They stay non-topological, and the new deliverable rows carry their content. A retirement would be a register-owner choice with no DAG effect, and happens only if P1 rewrites the package sentence.

### 2.4 Cautions for the application briefs

Each of these would silently change the arc set if missed. The application briefs in §6 carry them.

1. **SC-02-01-1 wording (DEL-02-01).** As C1-A wrote it, "`DEL-03-03` carries constraints on the external channel" sits in CLM-002. DAG-001 extraction read CLM-002 names as UPSTREAM inputs, so it would produce the **unevidenced reverse arc DEL-02-01 → DEL-03-03**. That arc sits inside SCC-002 and changes no membership, but it is not supported. P1 should word DEL-03-03 as a receiver. The same wording then grounds N-20 (R-02-01-k).
2. **SC-02-03-4 (DEL-02-03)** names "`DEL-01-04` (later undertaking) constructs the App act control" in CLM-002. Extraction will write **X-1, DEL-02-03 → DEL-01-04**. This arc is not among C1's 40. It is corroborated by EXEC §9.1, lies inside SCC-002 and changes no membership, but it makes DEL-01-04 `DAG pending`. It is included below as grounded. If the owner does not want it, P1 moves the sentence to REQ-006 (exclusions), which DAG-001 extraction did not read as inputs.
3. **DEL-04-01 must not be extracted from ACT.** The runtime resolution inputs in ACT §5.1 (DEL-03-01, DEL-04-02, DEL-02-01, DEL-02-03, DEL-05-01, P) and the ACT §2.7 citation of LOOP §5.1.1 would each pull DEL-04-01 into SCC-002 (ARC_ANALYSIS §4). The DEL-04-01 brief keeps `SOURCE_DOCS=ScopeOfWork.md`.
4. **Withheld rows.**
   - The disputed **N-12** (DEL-03-02 → DEL-04-03) and **N-B8** (DEL-03-03 → DEL-04-03) are not written in any register.
   - RS §10 contains cells that an extractor reading Design files could turn into these arcs. The DEL-04-03 and DEL-03-03 briefs say so.
5. **One row per ungrounded arc** is proposed, on the side where P1 has a natural hook. The other side is DEFER.

## 3. Summary by deliverable

"Apply" counts rows that `dependency-extract` would write, as **grounded** / **needing P1 wording or a declaration**. "Edit / package items" counts C1 items that refresh existing rows in place.

| Deliverable | C1 items | Apply: mirror | Apply: new-arc rows | Apply: non-deliverable | Edit / package items | Defer | Drop | Arcs created (grounded + needing P1) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| DEL-04-01 | 11 | 6 / 0 | 0 / 0 | 2 / 0 | 2 | 0 | 1 | none |
| DEL-04-02 | 15 | 1 / 0 | 7 / 1 | 2 / 0 | 1 | 1 | 2 | N-01, N-02, N-03, N-04, N-05, N-06, N-07 + R8-A |
| DEL-04-03 | 19 | 7 / 0 | 4 / 1 | 0 / 0 | 2 | 4 | 1 | N-10, N-13, N-14, N-15 + R8-B |
| DEL-02-01 | 15 | 0 / 0 | 2 / 2 | 3 / 0 | 0 | 8 | 0 | N-16, N-18 + N-17, N-20 |
| DEL-02-03 | 17 | 0 / 0 | 5 / 1 | 1 / 0 | 1 | 7 | 2 | N-21, N-07, N-23, N-24, X-1 + N-22 |
| DEL-03-01 | 13 | 0 / 0 | 0 / 1 | 0 / 0 | 2 | 10 | 0 | + N-11 |
| DEL-03-02 | 10 | 0 / 0 | 0 / 1 | 0 / 0 | 1 | 6 (+1 normalization) | 1 | + N-B3 |
| DEL-03-03 | 9 | 0 / 0 | 0 / 2 | 0 / 0 | 1 | 5 | 1 | + N-B4, N-27 |
| DEL-03-04 | 4 | 0 / 0 | 3 / 0 | 0 / 0 | 1 | 0 | 0 | N-B9, N-B10, N-B11 |
| DEL-01-01 | 6 | 0 / 0 | 0 / 0 | 0 / 0 | 2 | 1 | 3 | none (supplier of N-15, N-16, N-23, N-B4, N-B9, N-C5) |
| DEL-05-01 | 6 | 0 / 0 | 1 / 0 | 1 / 1 | 1 | 0 | 2 | N-03 |
| DEL-05-02 | 7 | 0 / 0 | 2 / 0 | 0 / 0 | 4 | 0 | 1 | N-04, N-25 |
| DEL-09-06 | 13 | 0 / 0 | 8 / 0 | 1 / 0 | 2 | 2 | 0 | N-08, N-19, N-28, N-C1…N-C5 |
| DEL-09-09 | 6 | 0 / 0 | 3 / 0 | 0 / 0 | 2 | 1 | 0 | N-09, N-26, N-C6 |
| DEL-02-04, 07-01, 07-02, 08-01, 08-02 | 5 | 0 / 0 | 0 / 0 | 0 / 0 | 0 | 5 | 0 | none |
| **Total** | **156** | **14 / 0** | **35 / 9** | **10 / 1** | **22** | **50** (+1 normalization) | **14** | **41 arcs** (32 grounded, 9 needing P1 or a declaration) |

In short:
- **Rows to add:** 69 in total. 59 are grounded (14 mirror, 35 new-arc, 10 non-deliverable). 10 need P1 wording or a declaration (9 new-arc, 1 non-deliverable).
- **Edits:** 22 items: 19 edits refresh 23 existing rows in place, and 3 package items keep 4 package rows. Row edits change Statement and Notes only; SatisfactionStatus is never moved.
- **The 55 C1 mirror rows:** 14 kept, 33 deferred, 8 dropped. In total, 50 items are deferred and 14 dropped.
- **Evidence drift only:** every kept mirror row, edit, EXTERNAL row and package row.
- **DAG departure:** only the new-arc rows (ARC_ANALYSIS).

Proposed `DependencyID`s continue each register's sequence in the §6.8 form, in the order listed. The next free IDs are:

| Register | Next free ID |
|---|---|
| DEL-04-01 | DEP-04-01-022 |
| DEL-04-02 | DEP-04-02-015 |
| DEL-04-03 | DEP-04-03-021 |
| DEL-02-01 | DEP-02-01-025 |
| DEL-02-03 | DEP-02-03-022 |
| DEL-03-01 | DEP-03-01-031 |
| DEL-03-02 | DEP-03-02-027 |
| DEL-03-03 | DEP-03-03-013 |
| DEL-03-04 | DEP-03-04-021 |
| DEL-05-01 | DEP-05-01-025 |
| DEL-05-02 | DEP-05-02-019 |
| DEL-09-06 | DEP-09-06-025 |
| DEL-09-09 | DEP-09-09-021 |

The extraction run assigns the final IDs. The IDs above are exact only if rows are added in this order and no other row is added first.

**Field conventions in `proposed_rows/`:**
- `Origin=EXTRACTED`, `Explicitness=EXPLICIT` and `Confidence=HIGH`.
- `RequiredMaturity=INITIALIZED` for deliverable targets (the accepted default, meaning defined-contract maturity only) and `TBD` for external targets.
- `SatisfactionStatus` follows the host register's convention for unfulfilled execution inputs: `PENDING` in DEL-04-02, 04-03, 02-01, 03-01, 03-03, 05-01, 05-02 and 09-09; `TBD` in the others.
- `EvidenceFile=ScopeOfWork.md`, with `SourceRef` naming the SoW locus and the grounding C1 correction.
- `EvidenceQuote` is the C1-proposed sentence fragment, flagged `quote_status` in Notes. It is **re-quoted from the applied SoW bytes**, never taken from this file.
- `FirstSeen` and `LastSeen` hold `<application date>`.
- `Notes` records the arc and its layer, and the Design corroboration line.

All proposed rows pass `tools/validation/validate_dependencies_schema.py` (29 columns) and `tools/validation/validate_enum.py` for every enum column (`evidence/row_validation.txt`).

## 4. Per deliverable: every C1 item, refreshed

### DEL-04-01 — Operation-policy and human-act distinctions

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| R-04-01-a | mirror: DOWNSTREAM HANDOVER | DEL-03-02 | KEEP | extraction | SC-04-01-2 | drift (MIRROR) | Proposed ID DEP-04-01-022. Counterpart DEP-03-02-017 verified ACTIVE on the same arc. |
| R-04-01-b | mirror: DOWNSTREAM HANDOVER | DEL-05-01 | KEEP | extraction | SC-04-01-2 | drift (MIRROR) | Proposed ID DEP-04-01-023. Counterpart DEP-05-01-018 verified ACTIVE on the same arc. |
| R-04-01-c | mirror: DOWNSTREAM HANDOVER | DEL-05-02 | KEEP | extraction | SC-04-01-2 | drift (MIRROR) | Proposed ID DEP-04-01-024. Counterpart DEP-05-02-008 verified ACTIVE on the same arc. |
| R-04-01-d | mirror: DOWNSTREAM HANDOVER | DEL-03-03 | KEEP | extraction | SC-04-01-2 | drift (MIRROR) | Proposed ID DEP-04-01-025. Counterpart DEP-03-03-008 verified ACTIVE on the same arc. |
| R-04-01-e | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | KEEP | extraction | SC-04-01-2 | drift (MIRROR) | Proposed ID DEP-04-01-026. Counterpart DEP-03-04-011 verified ACTIVE on the same arc. |
| R-04-01-f | mirror: DOWNSTREAM HANDOVER | DEL-09-09 | KEEP | extraction | SC-04-01-2 | drift (MIRROR) | Proposed ID DEP-04-01-027. Counterpart DEP-09-09-010 verified ACTIVE on the same arc. |
| R-04-01-g | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-09-06 | DROP | — | — | none (not applied) | Optional supplier-side mirror of N-28. ACT names DEL-09-06 only as a source of SWBPIPE answers in its consumed-inputs list, not as a consumer, so DEL-04-01 extraction would not support it. The representative row is DEL-09-06 UPSTREAM (R9-6-3). |
| DEP-04-01-017 | field edit | DEP-04-01-017 | AMEND | extraction | SC-04-01-8 | drift (non-topological) | C1 pointer update; depends on P1 SC-04-01-8 revising TBD-001. Evidence drift only. |
| DEP-04-01-018 | field edit | DEP-04-01-018 | AMEND | extraction | SC-04-01-9 | drift (non-topological) | C1 pointer update; P1 SC-04-01-9. Evidence drift only. |
| R-04-01-h | non-deliverable row: UPSTREAM CONSTRAINT | OI-021 | KEEP | extraction | SC-04-01-8 | drift (non-topological) | Proposed ID DEP-04-01-028.  |
| R-04-01-i | non-deliverable row: UPSTREAM CONSTRAINT | DECISION-4-GOV | AMEND | extraction | SC-04-01-10 (P1 refresh for DECISION-4) | drift (non-topological) | Proposed ID DEP-04-01-029. C1 targeted "DECISION-2 D6 / relay SQ-02". SQ-02 is now answered and D6 is closed for Phase 1 (R8-2), so the constraint is retargeted to the governance-phase re-opening. |

Rows to add (29 canonical columns in [`proposed_rows/DEL-04-01_proposed_rows.csv`](proposed_rows/DEL-04-01_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-04-01-022 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-03-02 | INITIALIZED | TBD | Supplies the adopted class vocabulary, resolution order, grant model and outcome map (ACT §10.1 V-02, V-03, V-04, V-05, V-14) to the proposal contract. | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-01-2) | It also supplies policy meaning to App v4 `DEL-03-02`, `DEL-03-03`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02` and `DEL-09-09`, each of which declares it upstream in its own register. |
| DEP-04-01-023 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-01 | INITIALIZED | TBD | Supplies act names, class values, grant model, outcome map and checkpoint rules (ACT §10.1 V-01…V-05, V-09, V-21) to the host-loop receiving contract. | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-01-2) | It also supplies policy meaning to App v4 `DEL-03-02`, `DEL-03-03`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02` and `DEL-09-09`, each of which declares it upstream in its own register. |
| DEP-04-01-024 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-02 | INITIALIZED | TBD | Supplies act names, outcome map, label rules and A3≠A4 display rules (ACT §10.1 V-01, V-05, V-07, V-12) to the panel receiving contract. | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-01-2) | It also supplies policy meaning to App v4 `DEL-03-02`, `DEL-03-03`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02` and `DEL-09-09`, each of which declares it upstream in its own register. |
| DEP-04-01-025 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-03-03 | INITIALIZED | TBD | Supplies class values, resolution order and the external-access rules including A13 (ACT §10.1 V-02, V-03, V-10, V-14) to the external receiving adapter. | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-01-2) | It also supplies policy meaning to App v4 `DEL-03-02`, `DEL-03-03`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02` and `DEL-09-09`, each of which declares it upstream in its own register. |
| DEP-04-01-026 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-03-04 | INITIALIZED | TBD | Declared consumer of the operation-policy contract for the integrated host guide (ACT §10.3). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-01-2) | It also supplies policy meaning to App v4 `DEL-03-02`, `DEL-03-03`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02` and `DEL-09-09`, each of which declares it upstream in its own register. |
| DEP-04-01-027 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-09-09 | INITIALIZED | TBD | Supplies professional-standing, external-access, record-shape and reserved-operation values (ACT §10.1 V-08, V-10, V-11, V-13, V-14) to the external trace cases. | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-01-2) | It also supplies policy meaning to App v4 `DEL-03-02`, `DEL-03-03`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02` and `DEL-09-09`, each of which declares it upstream in its own register. |
| DEP-04-01-028 | UPSTREAM | CONSTRAINT | EXTERNAL | OI-021 | TBD | TBD | Operation-specific reserved additions and the first connected operation remain UNRESOLVED{OI-021} (owner via the outside SWB session and App/shared owner); still open after R8-10. | ScopeOfWork.md#TBD-001 (as revised per C1 SC-04-01-8) | Operation-specific additions remain OPEN under OI-021 (owner via the outside SWB session and App/shared owner; before the connected-activity SoW). |
| DEP-04-01-029 | UPSTREAM | CONSTRAINT | EXTERNAL | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | TBD | TBD | App-side run holds are governance-phase only: D6 is closed for Phase 1 by APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-1 and re-opens when the governance phase is taken up (R8-2; SQ-02 answered: route (iv), none planned). | ScopeOfWork.md#TBD-004 (new) (as revised per C1 SC-04-01-10) | <quote the applied SC-04-01-10 sentence> |

### DEL-04-02 — Visible autonomy and result standing

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| R-04-02-a | mirror: UPSTREAM INTERFACE | DEL-03-02 | KEEP | extraction | SC-04-02-2 | drift; new SR-6 representative | Proposed ID DEP-04-02-015. Counterpart DEP-03-02-018 verified ACTIVE on the same arc. |
| R-04-02-b | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-04-02-c | new arc (consumer row): UPSTREAM INTERFACE | DEL-03-01 | KEEP | extraction | SC-04-02-2 (its direct-consumption option) | creates N-01 (candidate) | Proposed ID DEP-04-02-016.  |
| R-04-02-d | new arc (consumer row): UPSTREAM INTERFACE | DEL-02-03 | AMEND | extraction | SC-04-02-2 (P1 refresh for R8-1) | creates N-02 (candidate) | Proposed ID DEP-04-02-017. Amended for R8-1: the overlay is observation in Phase 1; hold values are governance phase (retained). |
| R-04-02-e | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-05-01 | KEEP | extraction | SC-04-02-2 | creates N-03 (candidate) | Proposed ID DEP-04-02-018.  |
| R-04-02-f | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-05-02 | KEEP | extraction | SC-04-02-2 | creates N-04 (candidate) | Proposed ID DEP-04-02-019.  |
| R-04-02-g | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-03-02 | KEEP | extraction | SC-04-02-2 | creates N-05 (candidate) | Proposed ID DEP-04-02-020.  |
| R-04-02-h | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-03-03 | KEEP | extraction | SC-04-02-2 | creates N-06 (candidate) | Proposed ID DEP-04-02-021.  |
| R-04-02-i | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-02-03 | KEEP | extraction | SC-04-02-2 | creates N-07 (candidate) | Proposed ID DEP-04-02-022.  |
| R-04-02-j | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-09-06 | DROP | — | — | none (not applied) | Optional supplier mirror. AS names DEL-09-06 only in version-citation lines; extraction of DEL-04-02 would not support it. Representative row is DEL-09-06 UPSTREAM (R9-6-3). |
| R-04-02-k | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-09-09 | DROP | — | — | none (not applied) | Optional supplier mirror. AS does not name DEL-09-09 as a receiver. Representative row is DEL-09-09 UPSTREAM (R9-9-2). |
| DEP-04-02-011/-012 | field edit | DEP-04-02-011;DEP-04-02-012 | AMEND | extraction | SC-04-02-5 | drift (non-topological) | Pointer update (V1-A RF-04). Evidence drift only. |
| R-04-02-l | non-deliverable row: UPSTREAM CONSTRAINT | OI-021 | KEEP | extraction | SC-04-02-5 | drift (non-topological) | Proposed ID DEP-04-02-023.  |
| R-04-02-m | non-deliverable row: UPSTREAM CONSTRAINT | DECISION-4-GOV | AMEND | extraction | SC-04-02-6 (P1 refresh for DECISION-4) | drift (non-topological) | Proposed ID DEP-04-02-024. Retargeted from DECISION-2 D6 / SQ-02 as for R-04-01-i. |
| R8-AS-1 | new arc (consumer row): UPSTREAM INTERFACE | DEL-05-01 | ADD | extraction after P1 wording, else declaration | P1 | creates R8-A (candidate) | Proposed ID DEP-04-02-025. New relationship written by the R8-13 pass (DECISION-5). |

Rows to add (29 canonical columns in [`proposed_rows/DEL-04-02_proposed_rows.csv`](proposed_rows/DEL-04-02_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-04-02-015 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 | INITIALIZED | PENDING | Receives the proposal outcome taxonomy, direct-branch entry condition and origin semantics (P §4.4, §9) for the result standing model (AS §8). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-02-2) | It also consumes App v4 `DEL-03-02` proposal/outcome and direct-application origin semantics, |
| DEP-04-02-016 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-01 | INITIALIZED | PENDING | Receives the catalog standing facets and read-result standing (C §6.2) for the temporal facet of result standing (AS §8). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-02-2) | `DEL-03-01` read-basis and standing facets, |
| DEP-04-02-017 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-03 | INITIALIZED | PENDING | Receives the display meanings of the EXEC annotations and compatibility report (Phase 1) and, for the governance phase, the hold-machine and hold-support values (EXEC §2.1, §2.2, §3.6, §4) for the checkpoint overlay (AS §4). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-02-2) | and `DEL-02-03` hold-support values and checkpoint annotations. |
| DEP-04-02-018 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-01 | INITIALIZED | PENDING | Supplies grant display states, grant value and scope and settings references (AS §3); named receiver in AS Receivers ("register edges pending at C1"). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-02-2) | Its visible autonomy state is received by `DEL-05-01`, `DEL-05-02`, `DEL-03-02`, `DEL-03-03` and `DEL-02-03`. |
| DEP-04-02-019 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-02 | INITIALIZED | PENDING | Supplies grant display states, grant value and scope and settings references (AS §3); named receiver in AS Receivers ("register edges pending at C1"). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-02-2) | Its visible autonomy state is received by `DEL-05-01`, `DEL-05-02`, `DEL-03-02`, `DEL-03-03` and `DEL-02-03`. |
| DEP-04-02-020 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-03-02 | INITIALIZED | PENDING | Supplies grant display states, grant value and scope and settings references (AS §3); named receiver in AS Receivers ("register edges pending at C1"). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-02-2) | Its visible autonomy state is received by `DEL-05-01`, `DEL-05-02`, `DEL-03-02`, `DEL-03-03` and `DEL-02-03`. |
| DEP-04-02-021 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-03-03 | INITIALIZED | PENDING | Supplies grant display states, grant value and scope and settings references (AS §3); named receiver in AS Receivers ("register edges pending at C1"). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-02-2) | Its visible autonomy state is received by `DEL-05-01`, `DEL-05-02`, `DEL-03-02`, `DEL-03-03` and `DEL-02-03`. |
| DEP-04-02-022 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-02-03 | INITIALIZED | PENDING | Supplies grant display states, grant value and scope and settings references (AS §3); named receiver in AS Receivers ("register edges pending at C1"). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-04-02-2) | Its visible autonomy state is received by `DEL-05-01`, `DEL-05-02`, `DEL-03-02`, `DEL-03-03` and `DEL-02-03`. |
| DEP-04-02-023 | UPSTREAM | CONSTRAINT | EXTERNAL | OI-021 | TBD | PENDING | Operation-specific reserved additions remain UNRESOLVED{OI-021} (AS U-01). | ScopeOfWork.md#TBD-001/TBD-002 (as revised per C1 SC-04-02-5) | <quote the applied SC-04-02-5 sentence> |
| DEP-04-02-024 | UPSTREAM | CONSTRAINT | EXTERNAL | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | TBD | PENDING | App-side run-hold display is governance-phase only: D6 closed for Phase 1 by DECISION-4 D4-1; re-opens with the governance phase (R8-2). | ScopeOfWork.md#TBD-006 (new) (as revised per C1 SC-04-02-6) | <quote the applied SC-04-02-6 sentence> |
| DEP-04-02-025 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-01 | INITIALIZED | PENDING | Receives the host-agent network rules (LOOP §5.1.1 NW-8…NW-16: category switches, named entries, in-work grant scopes, always-off items) that the grant display shows (AS §3, R8-13; DECISION-5). | ScopeOfWork.md#<section of the P1 SoW sentence, if P1 adds one> | <quote the applied P1 sentence; if P1 adds none, record as a human declaration (see route)> |

### DEL-04-03 — Content-bound decisions and compact run records

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| R-04-03-a | mirror: UPSTREAM INTERFACE | DEL-04-01 | KEEP | extraction | SC-04-03-1 | drift; new SR-6 representative | Proposed ID DEP-04-03-021. Counterpart DEP-04-01-016 verified ACTIVE on the same arc. |
| R-04-03-b | mirror: UPSTREAM INTERFACE | DEL-03-02 | KEEP | extraction | SC-04-03-1 | drift; new SR-6 representative | Proposed ID DEP-04-03-022. Counterpart DEP-03-02-019 verified ACTIVE on the same arc. |
| R-04-03-c | mirror: UPSTREAM INTERFACE | DEL-04-02 | KEEP | extraction | SC-04-03-1 | drift; new SR-6 representative | Proposed ID DEP-04-03-023. Counterpart DEP-04-02-009 verified ACTIVE on the same arc. |
| R-04-03-d | mirror: DOWNSTREAM INTERFACE | DEL-02-01 | DEFER | — | — | none (not applied) | Package-level only in the SoW (DEP-04-03-011 → PKG-02). Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-04-03-e | mirror: DOWNSTREAM INTERFACE | DEL-02-03 | DEFER | — | — | none (not applied) | Package-level only in the SoW (DEP-04-03-011 → PKG-02). Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-04-03-f | mirror: DOWNSTREAM HANDOVER | DEL-05-01 | KEEP | extraction | SC-04-03-2 | drift (MIRROR) | Proposed ID DEP-04-03-024. Counterpart DEP-05-01-019 verified ACTIVE on the same arc. |
| R-04-03-g | mirror: DOWNSTREAM HANDOVER | DEL-05-02 | KEEP | extraction | SC-04-03-2 | drift (MIRROR) | Proposed ID DEP-04-03-025. Counterpart DEP-05-02-009 verified ACTIVE on the same arc. |
| R-04-03-h | mirror: DOWNSTREAM HANDOVER | DEL-09-06 | KEEP | extraction | SC-04-03-2 | drift (MIRROR) | Proposed ID DEP-04-03-026. Counterpart DEP-09-06-015 verified ACTIVE on the same arc. |
| R-04-03-i | mirror: DOWNSTREAM HANDOVER | DEL-09-09 | KEEP | extraction | SC-04-03-2 | drift (MIRROR) | Proposed ID DEP-04-03-027. SC-04-03-2 names DEL-09-09 as a consumer of the record meaning, so the mirror is grounded. Counterpart DEP-09-09-011 verified ACTIVE on the same arc. |
| R-04-03-j | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-04-03-k | new arc (consumer row): UPSTREAM INTERFACE | DEL-03-01 | KEEP | extraction | SC-04-03-1 | creates N-10 (candidate) | Proposed ID DEP-04-03-028.  |
| R-04-03-l | new arc (consumer row): UPSTREAM INTERFACE | DEL-02-03 | AMEND | extraction | SC-04-03-1 (P1 refresh for R8-1) | creates N-13 (candidate) | Proposed ID DEP-04-03-029. Amended for R8-1 phasing. |
| R-04-03-m | new arc (consumer row): UPSTREAM INTERFACE | DEL-03-03 | KEEP | extraction | SC-04-03-1 | creates N-14 (candidate) | Proposed ID DEP-04-03-030.  |
| R-04-03-n | new arc (consumer row): UPSTREAM INTERFACE | DEL-01-01 | KEEP (confirm at K1) | extraction | SC-04-03-1 | creates N-15 (admitted) | Proposed ID DEP-04-03-031. Conditional in C1 (alternative: S-7 through DEL-01-02). Recommendation: keep; checkpoint 1 confirms. |
| R-04-03-o | new arc (supplier row): DOWNSTREAM INTERFACE | DEL-03-01 | DEFER | — | — | none (not applied) | Supplier side of N-11. One row per ungrounded arc is enough; the consumer row N-B1 carries it. If instead P1 refines SC-04-03-2's "PKG-03 basis/receipts" to name DEL-03-01, extraction yields this DOWNSTREAM row, which also establishes N-11. It also partly resolves package row DEP-04-03-012. |
| R-04-03-p | new arc (supplier row): DOWNSTREAM INTERFACE | DEL-03-02 | DROP | — | — | none (not applied) | Disputed arc N-12. Recommendation: not proposed (ARC_ANALYSIS §3). The RS §10 cell "DEL-03-02 consumes §5 evidence rules" goes to DEL-04-03's owner as a wording finding, and the DEL-04-03 extraction brief withholds this row. |
| DEP-04-03-012 | package row | DEP-04-03-012 | KEEP | extraction | SOW-NOW | drift (non-topological) | C1 proposed retarget/split. A retire is not needed for DAG-002 and would be a register-owner choice. If P1 rewrites the SoW package reference, extraction retires it. |
| DEP-04-03-019 | field edit | DEP-04-03-019 | AMEND | extraction | SC-04-03-4 | drift (non-topological) |  |
| R8-RS-1 | new arc (consumer row): UPSTREAM INTERFACE | DEL-05-01 | ADD | extraction after P1 wording, else declaration | P1 | creates R8-B (candidate) | Proposed ID DEP-04-03-032. R15 (R8-13, DECISION-5) names DEL-05-01 as the source of destination events. |

Rows to add (29 canonical columns in [`proposed_rows/DEL-04-03_proposed_rows.csv`](proposed_rows/DEL-04-03_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-04-03-021 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-01 | INITIALIZED | PENDING | Receives act names A1–A14, act-declined and run-ended events, the A12 network-destination grant subclass and content-binding/lapse rules (ACT §2, §2.5, §2.7) for the human-act and run records. | ScopeOfWork.md#CLM-004 (as revised per C1 SC-04-03-1) | This format receives act kinds and classes from App `DEL-04-01`, settings-in from `DEL-04-02`, |
| DEP-04-03-022 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 | INITIALIZED | PENDING | Receives §9 outcomes, change-item content identity, origin incl. constraint and author identity, resulting objects and item-left events from the proposal contract (RS §10). | ScopeOfWork.md#CLM-004 (as revised per C1 SC-04-03-1) | operation outcomes, change-item content identities and receipt links from `DEL-03-02`, |
| DEP-04-03-023 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-02 | INITIALIZED | PENDING | Receives settings-in (RS §8; CASE-002 M3) from the autonomy and standing exchange. | ScopeOfWork.md#CLM-004 (as revised per C1 SC-04-03-1) | This format receives act kinds and classes from App `DEL-04-01`, settings-in from `DEL-04-02`, |
| DEP-04-03-024 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-01 | INITIALIZED | PENDING | Supplies R3/R4/R5/R5a/R7/R8 record meanings (RS §10) to the host-loop receiving contract. | ScopeOfWork.md#REQ-005 (as revised per C1 SC-04-03-2) | PKG-05 loop and panel receiving (`DEL-05-01`, `DEL-05-02`), PKG-06 decisions and the PKG-09 connected-activity and trace contracts (`DEL-09-06`, `DEL-09-09`) consume the record meaning |
| DEP-04-03-025 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-02 | INITIALIZED | PENDING | Supplies act, act-declined, lapse, supersession and annotation display meanings (RS §10) to the panel receiving contract. | ScopeOfWork.md#REQ-005 (as revised per C1 SC-04-03-2) | PKG-05 loop and panel receiving (`DEL-05-01`, `DEL-05-02`), PKG-06 decisions and the PKG-09 connected-activity and trace contracts (`DEL-09-06`, `DEL-09-09`) consume the record meaning |
| DEP-04-03-026 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-09-06 | INITIALIZED | PENDING | Supplies R2 transfer links (RS §10) to the connected activity contract. | ScopeOfWork.md#REQ-005 (as revised per C1 SC-04-03-2) | PKG-05 loop and panel receiving (`DEL-05-01`, `DEL-05-02`), PKG-06 decisions and the PKG-09 connected-activity and trace contracts (`DEL-09-06`, `DEL-09-09`) consume the record meaning |
| DEP-04-03-027 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-09-09 | INITIALIZED | PENDING | Supplies the record meaning consumed by the external trace cases (SoW REQ-005 as revised per SC-04-03-2). | ScopeOfWork.md#REQ-005 (as revised per C1 SC-04-03-2) | PKG-05 loop and panel receiving (`DEL-05-01`, `DEL-05-02`), PKG-06 decisions and the PKG-09 connected-activity and trace contracts (`DEL-09-06`, `DEL-09-09`) consume the record meaning |
| DEP-04-03-028 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-01 | INITIALIZED | PENDING | Receives subject content identity, method designation, exposure element and the shared fixture (C §5.3, §10) used by R7 and the lapse rules (RS §10, L-1). | ScopeOfWork.md#CLM-004 (as revised per C1 SC-04-03-1) | subject content identities and method designations from `DEL-03-01`, |
| DEP-04-03-029 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-03 | INITIALIZED | PENDING | Receives the Phase-1 recording rules and, for the governance phase, the hold machine, resume point, re-hold and refused-A12 effect, plus compatibility reports, transfer trace and App capture requirements (EXEC §2.1, §2.2, §4, §5, §6; RS §10). | ScopeOfWork.md#CLM-004 (as revised per C1 SC-04-03-1) | hold-machine events and compatibility reports from `DEL-02-03`, |
| DEP-04-03-030 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-03 | INITIALIZED | PENDING | Receives external dispatch entries, model destination class and evidence limits from the external receiving adapter (RS §10; ADAPTER §11 "Provide to DEL-04-03"). | ScopeOfWork.md#CLM-004 (as revised per C1 SC-04-03-1) | external dispatch entries from `DEL-03-03`, |
| DEP-04-03-031 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-01 | INITIALIZED | PENDING | Receives supplied-guidance identities, per-turn requested/effective model and re-routes (HOSTING §8.3) and A14 settlement origin for R3, R5 and R13 (RS §10). | ScopeOfWork.md#CLM-004 (as revised per C1 SC-04-03-1) | and observed supplier facts (supplied guidance, model and destination, tool-permission settlements) from `DEL-01-01`. |
| DEP-04-03-032 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-01 | INITIALIZED | PENDING | Receives host-loop events and the network rules through DEL-05-01 (LOOP §2.3, §5.1.1) for R15 network destinations, and observer-attributed unknown, run-resumed/run-ended (RS §10). | ScopeOfWork.md#<section of the P1 SoW sentence, if P1 adds one> | <quote the applied P1 sentence; if P1 adds none, record as a human declaration (see route)> |

### DEL-02-01 — Portable workflow contract and shared allocation

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| R-02-01-a | mirror: DOWNSTREAM HANDOVER | DEL-02-02 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-01-b | mirror: DOWNSTREAM HANDOVER | DEL-02-03 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-01-c | mirror: DOWNSTREAM HANDOVER | DEL-02-04 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-01-d | mirror: DOWNSTREAM HANDOVER | DEL-05-01 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-01-e | mirror: DOWNSTREAM HANDOVER | DEL-05-02 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-01-f | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-01-g | new arc (consumer row): UPSTREAM INTERFACE | DEL-01-01 | KEEP | extraction | SC-02-01-1, SC-02-01-2 | creates N-16 (admitted) | Proposed ID DEP-02-01-025.  |
| R-02-01-h | new arc (consumer row): UPSTREAM INTERFACE | DEL-02-03 | AMEND | extraction after P1 wording, else declaration | P1 (SC-02-01-6 refreshed to state consumption of DEL-02-03) | creates N-17 (candidate) | Proposed ID DEP-02-01-026. Amended for R8-1 phasing. |
| R-02-01-i | new arc (consumer row): UPSTREAM INTERFACE | DEL-03-02 | KEEP | extraction | SC-02-01-1, SC-02-01-3 | creates N-18 (candidate) | Proposed ID DEP-02-01-027.  |
| R-02-01-j | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-09-06 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). The representative row (DEL-09-06, R9-6-1a) is grounded by S9-6-3. |
| R-02-01-k | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-03-03 | KEEP | extraction after P1 wording, else declaration | P1 (SC-02-01-1 must name DEL-03-03 as a receiver, not as a supplier) | creates N-20 (candidate) | Proposed ID DEP-02-01-028. As C1 words it, SC-02-01-1 ("DEL-03-03 carries constraints on the external channel") would be extracted from CLM-002 as an UPSTREAM input. That is the unevidenced reverse arc DEL-02-01 → DEL-03-03. |
| R-02-01-k2 | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-03-02 | DEFER | — | — | none (not applied) | Supplier side of N-B3; optional. The consumer row N-B3 carries the arc if P1 grounds it. |
| R-02-01-l | non-deliverable row: UPSTREAM CONSTRAINT | OI-021 | AMEND | extraction | SC-02-01-5 | drift (non-topological) | Proposed ID DEP-02-01-029. C1 combined DECISION-1 and OI-021. DECISION-1 is ruled, so it is carried in Notes and not held as an open constraint. |
| R-02-01-m | non-deliverable row: UPSTREAM CONSTRAINT | DECISION-4-GOV | AMEND | extraction | SC-02-01-6 (P1 refresh for DECISION-4) | drift (non-topological) | Proposed ID DEP-02-01-030. Retargeted from DECISION-2 D6 / SQ-02. |
| R-02-01-n | non-deliverable row: UPSTREAM CONSTRAINT | OI-018 | KEEP | extraction | SOW-NOW | drift (non-topological) | Proposed ID DEP-02-01-031.  |

Rows to add (29 canonical columns in [`proposed_rows/DEL-02-01_proposed_rows.csv`](proposed_rows/DEL-02-01_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-02-01-025 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-01 | INITIALIZED | PENDING | Receives supplied-guidance identity evidence (HOSTING §8.2) and the harness capability inventory at 0.158.0 for harness-capability naming (WD §8; U-08). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-02-01-1) | `DEL-01-01` supplies the harness capability inventory and supplied-guidance identity evidence; |
| DEP-02-01-026 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-03 | INITIALIZED | PENDING | Receives the Phase-1 statement (EXEC §2.1), governance-phase scope (§2.2), report and hold support (§3.6, governance phase), hold machine (§4), App capture (§5) and transfer (§6) (WD §8). | ScopeOfWork.md#<section of the P1 SoW sentence, if P1 adds one> | <quote the applied P1 sentence; if P1 adds none, record as a human declaration (see route)> |
| DEP-02-01-027 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 | INITIALIZED | PENDING | Receives P §9, change-item content identity, item dispositions, all-decided and item-left events, governing checkpoint constraint and applied-outcome object identities (WD §8). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-02-01-1) | `DEL-03-02` owns proposal/outcome semantics, including the governing checkpoint constraint, item dispositions and item-left events; |
| DEP-02-01-028 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-03-03 | INITIALIZED | PENDING | Supplies the governing checkpoint constraint derivation rule to the external adapter (WD §9 A-12: consumers DEL-05-01, DEL-03-03). | ScopeOfWork.md#<section of the P1 SoW sentence, if P1 adds one> | <quote the applied P1 sentence; if P1 adds none, record as a human declaration (see route)> |
| DEP-02-01-029 | UPSTREAM | CONSTRAINT | EXTERNAL | OI-021 | TBD | PENDING | Operation-specific reserved additions remain UNRESOLVED{OI-021}; DECISION-1 D2/D3 carried (WD §2 S-Q/S-R/S-S). | ScopeOfWork.md#TBD-003 (as revised per C1 SC-02-01-5) | OI-001 and OI-002 were ruled for the first increment by DECISION-1 D2/D3 (carried by DEL-04-01). |
| DEP-02-01-030 | UPSTREAM | CONSTRAINT | EXTERNAL | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | TBD | PENDING | Hold support and App-side holds are governance-phase only: D6 closed for Phase 1 by DECISION-4 D4-1; re-opens with the governance phase (WD U-30, U-33; R8-2). | ScopeOfWork.md#TBD-004 (new) (as revised per C1 SC-02-01-6) | <quote the applied SC-02-01-6 sentence> |
| DEP-02-01-031 | UPSTREAM | CONSTRAINT | EXTERNAL | OI-018 | TBD | PENDING | SoW TBD-003 names OI-018; the register has no row. | ScopeOfWork.md#TBD-003 | <quote from current SoW at application> |

### DEL-02-03 — Workflow execution compatibility and round-trip support

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| R-02-03-a | mirror: DOWNSTREAM HANDOVER | DEL-05-01 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-03-b | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DROP | — | — | none (not applied) | Optional mirror. EXEC does not name DEL-03-04 as a receiver (only a version citation); arc represented by DEP-03-04-009. |
| R-02-03-c | mirror: DOWNSTREAM HANDOVER | DEL-02-02 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-03-d | new arc (consumer row): UPSTREAM INTERFACE | DEL-03-02 | KEEP | extraction | SC-02-03-4 | creates N-21 (candidate) | Proposed ID DEP-02-03-022.  |
| R-02-03-e | new arc (consumer row): UPSTREAM INTERFACE | DEL-05-01 | KEEP | extraction after P1 wording, else declaration | P1 | creates N-22 (candidate) | Proposed ID DEP-02-03-023. N-22 has no grounded row. The current CLM-003 ownership sentence about DEL-05-01 was not extracted as an input in DAG-001. |
| R-02-03-f | new arc (consumer row): UPSTREAM INTERFACE | DEL-04-02 | KEEP | extraction | SC-02-03-4 | creates N-07 (candidate) | Proposed ID DEP-02-03-024.  |
| R-02-03-g | new arc (consumer row): UPSTREAM INTERFACE | DEL-01-01 | KEEP | extraction | SC-02-03-4 | creates N-23 (admitted) | Proposed ID DEP-02-03-025.  |
| R-02-03-h | new arc (consumer row): UPSTREAM INTERFACE | DEL-03-03 | KEEP | extraction | SC-02-03-4 | creates N-24 (candidate) | Proposed ID DEP-02-03-026.  |
| R-02-03-i | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-02-01 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-03-j | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-04-03 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-03-k | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-04-02 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-03-l | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-05-02 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R-02-03-n | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-03-03 | DEFER | — | — | none (not applied) | Supplier side of N-27; optional. The consumer row N-B7 carries the arc if P1 grounds it. |
| R-02-03-m | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-09-09 | DROP | — | — | none (not applied) | Optional supplier mirror. EXEC does not name DEL-09-09 as a receiver; representative row is DEL-09-09 UPSTREAM (R9-9-3). |
| DEP-02-03-015/-016 | field edit | DEP-02-03-015;DEP-02-03-016 | AMEND | extraction | SC-02-03-5 | drift (non-topological) |  |
| R-02-03-o | non-deliverable row: UPSTREAM CONSTRAINT | DECISION-4-GOV | AMEND | extraction | SC-02-03-1, SC-02-03-3 (P1 refresh for DECISION-4) | drift (non-topological) | Proposed ID DEP-02-03-027. Retargeted from DECISION-2 D6 / SQ-02. |
| X-1 | new arc (consumer row): UPSTREAM INTERFACE | DEL-01-04 | ADD | extraction | SC-02-03-4 | creates X-1 (candidate) | Proposed ID DEP-02-03-028. Not in C1's 40 arcs. C1-A SC-02-03-4 adds "DEL-01-04 (later undertaking) constructs the App act control" to CLM-002, and DAG-001 extraction read CLM-002 names as UPSTREAM inputs, so applying SC-02-03-4 produces this arc. EXEC §9.1 corroborates. Both endpoints are in SCC-002. |

Rows to add (29 canonical columns in [`proposed_rows/DEL-02-03_proposed_rows.csv`](proposed_rows/DEL-02-03_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-02-03-022 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 | INITIALIZED | TBD | Receives per-item dispositions, item-left events, change-item content identity, applied outcomes, stale/application-error outcomes and the governing constraint with carriage assurance (governance phase) (EXEC §9.1). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-02-03-4) | `DEL-03-02` owns proposal item dispositions, item-left events and the governing checkpoint constraint; |
| DEP-02-03-023 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-01 | INITIALIZED | TBD | Receives arrival observation, binding, events, dispatch record and retry rules, and host-loop hold support for the governance phase (EXEC §9.1). | ScopeOfWork.md#<section of the P1 SoW sentence, if P1 adds one> | <quote the applied P1 sentence; if P1 adds none, record as a human declaration (see route)> |
| DEP-02-03-024 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-02 | INITIALIZED | TBD | Receives grant display states incl. set by person, not yet confirmed, unconfirmed and refused (EXEC §9.1; §4.10). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-02-03-4) | `DEL-04-02` owns grant display states; |
| DEP-02-03-025 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-01 | INITIALIZED | TBD | Receives supplied-guidance evidence (§8.2), observed model destination per turn (§8.3), request kinds and R9, and the HP-4 scope ruling (EXEC §9.1). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-02-03-4) | `DEL-01-01` supplies observed supplier facts; |
| DEP-02-03-026 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-03 | INITIALIZED | TBD | Receives carriage assurance, GC-1…GC-5, §7.7 checkpoint observation on X and model destination in channel status (EXEC §9.1). | ScopeOfWork.md#CLM-002 (as revised per C1 SC-02-03-4) | `DEL-03-03` owns external-channel carriage and its assurance; |
| DEP-02-03-027 | UPSTREAM | CONSTRAINT | EXTERNAL | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | TBD | TBD | App-side holds and App-only checkpoints are governance-phase only: D6 closed for Phase 1 by DECISION-4 D4-1 (EXEC U-E1, U-E23 re-pointed; R8-2). | ScopeOfWork.md#CLM-003 (as revised per C1 SC-02-03-1) | <quote the applied SC-02-03-1 sentence> |
| DEP-02-03-028 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-04 | INITIALIZED | TBD | Receives the App act control (CAP-2) and person identity from the later App act-control construction (EXEC §9.1; §5); outside D1. | ScopeOfWork.md#CLM-002 (as revised per C1 SC-02-03-4) | `DEL-01-04` (later undertaking) constructs the App act control. |

### DEL-03-01 — Capability catalog and read-basis contract

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| M-01-1 | mirror: DOWNSTREAM HANDOVER | DEL-05-01 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-01-2 | mirror: DOWNSTREAM HANDOVER | DEL-05-02 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-01-3 | mirror: DOWNSTREAM HANDOVER | DEL-02-01 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-01-4 | mirror: DOWNSTREAM HANDOVER | DEL-02-03 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-01-5 | mirror: DOWNSTREAM HANDOVER | DEL-03-03 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-01-6 | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-01-7 | mirror: DOWNSTREAM HANDOVER | DEL-09-09 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-01-8 | mirror: DOWNSTREAM HANDOVER | DEL-10-03 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-01-3-pkg | package row | DEP-03-01-022 | KEEP | extraction | SOW-NOW | drift (non-topological) | C1 proposed retiring it. Retirement is a register-owner choice with no DAG effect. Extraction retires it only if P1 changes the SoW reference. |
| DEP-03-01-024 | field edit | DEP-03-01-024 | AMEND | extraction | S-01-2 | drift (non-topological) |  |
| N-B1 | new arc (consumer row): UPSTREAM INTERFACE | DEL-04-03 | KEEP | extraction after P1 wording, else declaration | P1 | creates N-11 (candidate) | Proposed ID DEP-03-01-031. N-11 has no grounded row on either side. The current SoW names DEL-04-03 only as an owner, which DAG-001 extraction did not treat as an input. |
| N-01-mir | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-04-02 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| N-10-mir | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-04-03 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |

Rows to add (29 canonical columns in [`proposed_rows/DEL-03-01_proposed_rows.csv`](proposed_rows/DEL-03-01_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-03-01-031 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-03 | INITIALIZED | PENDING | Receives the DEL-04-03 §6.1 act field set and §7 lapse vocabulary carried in read-result standing (C §6.2). | ScopeOfWork.md#<section of the P1 SoW sentence, if P1 adds one> | <quote the applied P1 sentence; if P1 adds none, record as a human declaration (see route)> |

### DEL-03-02 — Proposal, validation and outcome contract

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| M-02-1 | mirror: DOWNSTREAM INTERFACE | DEL-03-01 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-02-2 | mirror: DOWNSTREAM HANDOVER | DEL-05-01 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-02-3 | mirror: DOWNSTREAM HANDOVER | DEL-05-02 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-02-4 | mirror: DOWNSTREAM HANDOVER | DEL-10-03 | DROP | — | — | none (not applied) | Observed-only mirror; P does not name DEL-10-03. Arc represented by DEP-10-03-012 (consumer UPSTREAM). DEL-10-03 is outside D1. |
| DEP-03-02-017 | field edit | DEP-03-02-017 | AMEND | extraction | S-02-1 | drift (non-topological) |  |
| NORM-03-02 | value normalization | DEP-03-02-016…026 | DEFER | human (register owner) | — | none (not applied) | SatisfactionStatus TBD vs PENDING is a register-owner convention. Both values are valid, no row is SATISFIED, and DAG-002 is unaffected. Owner item O-6. |
| N-B2 | new arc (consumer row): UPSTREAM INTERFACE | DEL-04-02 | DEFER | — | — | none (not applied) | Consumer-side representative of N-05. No C1 SoW correction for DEL-03-02 states consumption of DEL-04-02 (its SoW names DEL-04-02 only as an owner, which was extracted DOWNSTREAM as DEP-03-02-018). N-05 is established by the grounded supplier row R-04-02-g (SC-04-02-2). Add later if P1 adds the sentence. |
| N-B3 | new arc (consumer row): UPSTREAM INTERFACE | DEL-02-01 | KEEP | extraction after P1 wording, else declaration | P1 | creates N-B3 (candidate) | Proposed ID DEP-03-02-027. Neither SoW grounds N-B3. |
| N-18/N-21-mir | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-02-01 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| N-21-mir | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-02-03 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |

Rows to add (29 canonical columns in [`proposed_rows/DEL-03-02_proposed_rows.csv`](proposed_rows/DEL-03-02_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-03-02-027 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-01 | INITIALIZED | TBD | Receives workflow identity, checkpoint declarations (required act, subject class, reached-when) and the §4.3.7 item rule (P §13). | ScopeOfWork.md#<section of the P1 SoW sentence, if P1 adds one> | <quote the applied P1 sentence; if P1 adds none, record as a human declaration (see route)> |

### DEL-03-03 — Local external-agent receiving adapter

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| M-03-1 | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| DEP-03-03-008 | field edit | DEP-03-03-008 | AMEND | extraction | S-03-1 | drift (non-topological) |  |
| N-B4 | new arc (consumer row): UPSTREAM INTERFACE | DEL-01-01 | KEEP | extraction after P1 wording, else declaration | P1 | creates N-B4 (admitted) | Proposed ID DEP-03-03-013. Neither the DEL-03-03 nor the DEL-01-01 C1 SoW corrections name the other deliverable. |
| N-B5 | new arc (consumer row): UPSTREAM INTERFACE | DEL-04-02 | DEFER | — | — | none (not applied) | Consumer-side representative of N-06. No DEL-03-03 SoW correction; N-06 is established by the grounded supplier row R-04-02-h (SC-04-02-2). |
| N-B6 | new arc (consumer row): UPSTREAM INTERFACE | DEL-02-01 | DEFER | — | — | none (not applied) | Consumer side of N-20; optional. N-20 is carried by the supplier row R-02-01-k once P1 words SC-02-01-1 with DEL-03-03 as a receiver. |
| N-B7 | new arc (consumer row): UPSTREAM INTERFACE | DEL-02-03 | AMEND | extraction after P1 wording, else declaration | P1 (S-03-4 refreshed for R8-1 and naming DEL-02-03) | creates N-27 (candidate) | Proposed ID DEP-03-03-014. Amended for R8-1 phasing. S-03-4 cites "EXEC §3.6" without the deliverable ID, and R8-1 supersedes its hold wording. |
| N-B8 | new arc (consumer row): UPSTREAM INTERFACE | DEL-04-03 | DROP | — | — | none (not applied) | C1-B conditional. ADAPTER-v0.4 §11 has no "Expect from DEL-04-03" row. RS is read "for joins only" to name where the adapter's evidence lands (the record destination). Dropped for the same reason as N-12; N-14 carries the relationship. |
| N-14-mir | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-04-03 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| N-24-mir | new arc (supplier row): DOWNSTREAM HANDOVER | DEL-02-03 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |

Rows to add (29 canonical columns in [`proposed_rows/DEL-03-03_proposed_rows.csv`](proposed_rows/DEL-03-03_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-03-03-013 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-01 | INITIALIZED | PENDING | Receives supplier surfaces at 0.158.0 (§3.5), A14 origins (R7–R9) and native delivery (H6) from HOSTING and the pin record (ADAPTER §11). | ScopeOfWork.md#<section of the P1 SoW sentence, if P1 adds one> | <quote the applied P1 sentence; if P1 adds none, record as a human declaration (see route)> |
| DEP-03-03-014 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-03 | INITIALIZED | PENDING | Receives Phase-1 guidance and recording (EXEC §2.1) and, for the governance phase, the hold machine and per-checkpoint hold support (EXEC §2.2, §3.6) (ADAPTER §11). | ScopeOfWork.md#<section of the P1 SoW sentence, if P1 adds one> | <quote the applied P1 sentence; if P1 adds none, record as a human declaration (see route)> |

### DEL-03-04 — Host boundary and integration guide

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| DEP-03-04-011 | field edit | DEP-03-04-011 | AMEND | extraction | S-04-1 | drift (non-topological) |  |
| N-B9 | new arc (consumer row): UPSTREAM INTERFACE | DEL-01-01 | KEEP | extraction | S-04-6 | creates N-B9 (admitted) | Proposed ID DEP-03-04-021. Pairs with P1 SoW correction S-04-6. |
| N-B10 | new arc (consumer row): UPSTREAM INTERFACE | DEL-09-06 | KEEP | extraction | S-04-6 | creates N-B10 (admitted) | Proposed ID DEP-03-04-022.  |
| N-B11 | new arc (consumer row): UPSTREAM INTERFACE | DEL-09-09 | KEEP | extraction | S-04-6 | creates N-B11 (admitted) | Proposed ID DEP-03-04-023.  |

Rows to add (29 canonical columns in [`proposed_rows/DEL-03-04_proposed_rows.csv`](proposed_rows/DEL-03-04_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-03-04-021 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-01 | INITIALIZED | TBD | Receives the App's Codex boundary facts (HOSTING §6.7, §6.8, §8.2, §8.3; SPIKE) for rows 5, 6, 8 and 9 (GUIDE §2.11). | ScopeOfWork.md#CLM-002 or CLM-003 (as revised per C1 S-04-6) | The guide also consumes App v4 DEL-01-01's supplier boundary (native surfaces for optional external access), DEL-09-06's relay questions (the host-contribution column) and DEL-09-09's external trace cases, |
| DEP-03-04-022 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-09-06 | INITIALIZED | TBD | Receives the CA step map and staging, RELAY-v0.3 question identities and the SWBPIPE answers held in DEL-09-06 (GUIDE §2.11: host column of every row). | ScopeOfWork.md#CLM-002 or CLM-003 (as revised per C1 S-04-6) | The guide also consumes App v4 DEL-01-01's supplier boundary (native surfaces for optional external access), DEL-09-06's relay questions (the host-contribution column) and DEL-09-09's external trace cases, |
| DEP-03-04-023 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-09-09 | INITIALIZED | TBD | Receives the V4-EXM-25 suite, extension trace and OI-003 disposition record for rows 1 and 9 (GUIDE §2.11). | ScopeOfWork.md#CLM-002 or CLM-003 (as revised per C1 S-04-6) | The guide also consumes App v4 DEL-01-01's supplier boundary (native surfaces for optional external access), DEL-09-06's relay questions (the host-contribution column) and DEL-09-09's external trace cases, |

### DEL-01-01 — Stock Codex hosting and supplier contract

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| M-11-1 | mirror: DOWNSTREAM HANDOVER | DEL-02-04 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| M-11-2 | mirror: DOWNSTREAM HANDOVER | DEL-06-01 | DROP | — | — | none (not applied) | Observed-only optional mirror. Neither HOSTING nor the DEL-01-01 SoW names this receiver, so a CONSERVATIVE extraction would not emit it. The arc is represented by the consumer's UPSTREAM row, and the target is outside D1. |
| M-11-3 | mirror: DOWNSTREAM HANDOVER | DEL-09-01 | DROP | — | — | none (not applied) | Observed-only optional mirror. Neither HOSTING nor the DEL-01-01 SoW names this receiver, so a CONSERVATIVE extraction would not emit it. The arc is represented by the consumer's UPSTREAM row, and the target is outside D1. |
| M-11-4 | mirror: DOWNSTREAM HANDOVER | DEL-09-02 | DROP | — | — | none (not applied) | Observed-only optional mirror. Neither HOSTING nor the DEL-01-01 SoW names this receiver, so a CONSERVATIVE extraction would not emit it. The arc is represented by the consumer's UPSTREAM row, and the target is outside D1. |
| DEP-01-01-017 | field edit | DEP-01-01-017 | AMEND | extraction | S-11-2 | drift (non-topological) |  |
| DEP-01-01-018 | field edit | DEP-01-01-018 | AMEND | extraction | S-11-2 | drift (non-topological) |  |

### DEL-05-01 — Minimal-loop and model receiving contract

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| M-04-05-01 | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DROP | — | — | none (not applied) | Optional mirror. LOOP names DEL-03-04 only in a version citation. C1-C counted supplier mirrors for DEL-05-01 as optional and not proposed. |
| R5-1-1 | new arc (consumer row): UPSTREAM INTERFACE | DEL-04-02 | KEEP | extraction | S5-1-1 | creates N-03 (candidate) | Proposed ID DEP-05-01-025.  |
| R5-1-2 | mirror: UPSTREAM INTERFACE | DEL-01-05 | DROP | — | — | none (not applied) | LOOP-v0.6 does not name DEL-01-05 (C1-C: "LOOP-v0.5 does not yet consume it"). A consumer row would also replace DAG-001's representative with an unevidenced row. Record in DEL-05-01 Run Notes why no consumer row is kept. |
| R5-1-3 | non-deliverable row: DOWNSTREAM HANDOVER | DEP-001-RELAY | AMEND | extraction | S5-1-4 | drift (non-topological) | Proposed ID DEP-05-01-026. C1 wording said "prepared"; the questions are now relayed and answered. |
| R5-1-5 | field edit | DEP-05-01-024 | AMEND | extraction | S5-1-4 | drift (non-topological) |  |
| R8-LOOP-1 | non-deliverable row: UPSTREAM CONSTRAINT | DECISION-5-OPEN | ADD | extraction after P1 wording, else declaration | P1 (DECISION-5 wording) | drift (non-topological) | Proposed ID DEP-05-01-027. R8-13 (DECISION-5). Non-topological. |

Rows to add (29 canonical columns in [`proposed_rows/DEL-05-01_proposed_rows.csv`](proposed_rows/DEL-05-01_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-05-01-025 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-02 | INITIALIZED | PENDING | Receive the adopted grant display states and settings references carried as the grant in force on each dispatch and in run evidence; this deliverable does not define them (LOOP §10.3). | ScopeOfWork.md#CLM-002 (as revised per C1 S5-1-1) | `DEL-04-02` owns the autonomy-grant display states and standing exchange, which this deliverable consumes as the grant in force carried on each dispatch; |
| DEP-05-01-026 | DOWNSTREAM | HANDOVER | EXTERNAL | DEP-001 | TBD | PENDING | External SWBPIPE owner — loop receiving questions relayed through DEL-09-06 RELAY-v0.3; answered 2026-09-28 (SWBPIPE has no embedded loop; none selected); host joins deferred (DECISION-3). | ScopeOfWork.md#TBD-003 (as revised per C1 S5-1-4) | <quote the applied S5-1-4 sentence> |
| DEP-05-01-027 | UPSTREAM | CONSTRAINT | EXTERNAL | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5 | TBD | PENDING | Owner — how a category switch combines with its named entries (LOOP N-OPEN-4) and the accepted-basis revision of V4-HOST-02 per DECISION-5; point of need before §5.1.1 implementation. | ScopeOfWork.md#<section of the P1 SoW sentence, if P1 adds one> | <quote the applied P1 sentence; if P1 adds none, record as a human declaration (see route)> |

### DEL-05-02 — Host panel and shared interaction receiving

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| M-04-05-02 | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DROP | — | — | none (not applied) | Optional mirror. PANEL names DEL-03-04 only in a version citation (C1-C: optional, not counted). |
| R5-2-1 | new arc (consumer row): UPSTREAM PREREQUISITE | DEL-04-02 | KEEP | extraction | S5-2-2 | creates N-04 (candidate) | Proposed ID DEP-05-02-019.  |
| R5-2-2 | new arc (consumer row): UPSTREAM PREREQUISITE | DEL-02-03 | AMEND | extraction | S5-2-3 (main option; P1 refresh for R8-1) | creates N-25 (candidate) | Proposed ID DEP-05-02-020. The condition is removed. R4 re-pointed PANEL W-5 to EXEC and R8 made PANEL read EXEC §2.1–§2.2 directly, so the "via DEL-05-01" alternative no longer describes the text. |
| R5-2-3 | field edit | DEP-05-02-014;DEP-05-02-015 | AMEND | extraction | S5-2-1 | drift (non-topological) |  |
| R5-2-4 | field edit | DEP-05-02-016 | KEEP | extraction | SOW-NOW | drift (non-topological) |  |
| R5-2-5 | field edit | DEP-05-02-011 | AMEND | extraction | S5-2-5 | drift (non-topological) | C1 wording predates the answers and R8-1. |
| R5-2-6 | field edit | DEP-05-02-018 | AMEND | extraction | Notes refresh (no SoW change needed) | drift (non-topological) | "prepared, not delivered" is superseded. |

Rows to add (29 canonical columns in [`proposed_rows/DEL-05-02_proposed_rows.csv`](proposed_rows/DEL-05-02_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-05-02-019 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-02 | INITIALIZED | PENDING | Panel receiving requirements consume the checked autonomy-grant display states, active scope and network-destination grants supplied by DEL-04-02 (PANEL §3.6, ND-5). | ScopeOfWork.md#CLM-002 (as revised per C1 S5-2-2) | `DEL-04-02` supplies autonomy-grant display states and active scope. |
| DEP-05-02-020 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-03 | INITIALIZED | PENDING | Panel receiving requirements consume the Phase-1 statement and compatibility report meanings (EXEC §2.1, §3.3 CR-8/CR-9) and, for the governance phase, the hold-support values and hold-machine meanings (EXEC §2.2, §3.6, §4). | ScopeOfWork.md#CLM-002 (as revised per C1 S5-2-3) | `DEL-02-03` supplies the hold-support values and hold-machine meanings (resume, re-hold, run end, act ordering, mixed decisions) that the panel displays. |

### DEL-09-06 — Connected activity contract and workflow round trip

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| R9-6-1a | new arc (consumer row): UPSTREAM INTERFACE | DEL-02-01 | KEEP | extraction | S9-6-3 | creates N-19 (admitted) | Proposed ID DEP-09-06-025.  |
| R9-6-1b | new arc (consumer row): UPSTREAM INTERFACE | DEL-02-02 | KEEP | extraction | S9-6-3 | creates N-C1 (admitted) | Proposed ID DEP-09-06-026.  |
| R9-6-2a | new arc (consumer row): UPSTREAM INTERFACE | DEL-03-01 | KEEP | extraction | S9-6-3 | creates N-C2 (admitted) | Proposed ID DEP-09-06-027.  |
| R9-6-2b | new arc (consumer row): UPSTREAM INTERFACE | DEL-03-02 | KEEP | extraction | S9-6-3 | creates N-C3 (admitted) | Proposed ID DEP-09-06-028.  |
| R9-6-2c | new arc (consumer row): UPSTREAM INTERFACE | DEL-03-03 | KEEP | extraction | S9-6-3 | creates N-C4 (admitted) | Proposed ID DEP-09-06-029.  |
| R9-6-3a | new arc (consumer row): UPSTREAM INTERFACE | DEL-04-01 | KEEP | extraction | S9-6-3 | creates N-28 (admitted) | Proposed ID DEP-09-06-030.  |
| R9-6-3b | new arc (consumer row): UPSTREAM INTERFACE | DEL-04-02 | KEEP | extraction | S9-6-3 | creates N-08 (admitted) | Proposed ID DEP-09-06-031.  |
| R9-6-3c | new arc (consumer row): UPSTREAM INTERFACE | DEL-01-01 | KEEP | extraction | S9-6-3 | creates N-C5 (admitted) | Proposed ID DEP-09-06-032.  |
| R9-6-1-pkg | package row | DEP-09-06-012;DEP-09-06-014 | KEEP | extraction | SOW-NOW | drift (non-topological) |  |
| R9-6-4 | mirror: UPSTREAM INTERFACE | DEL-09-01 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R9-6-5 | mirror: DOWNSTREAM HANDOVER | DEL-09-07 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R9-6-6 | field edit | DEP-09-06-022;DEP-09-06-023 | AMEND | extraction | S9-6-1 | drift (non-topological) |  |
| R9-6-7 | non-deliverable row: DOWNSTREAM HANDOVER | DEP-001-RELAY | AMEND | extraction | SOW-NOW (OUT-004) | drift (non-topological) | Proposed ID DEP-09-06-033. C1 wording predates delivery and answers. |

Rows to add (29 canonical columns in [`proposed_rows/DEL-09-06_proposed_rows.csv`](proposed_rows/DEL-09-06_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-09-06-025 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-01 | INITIALIZED | TBD | Receives the workflow declaration (WD §4.3.0, §4.3.1, WR-1…WR-11) and WD-EX examples cited per step (CA §3.1, §4, §11.1). | ScopeOfWork.md#CLM-003 (as revised per C1 S9-6-3) | App DEL-02-01 supplies portable declaration, identity and revision meaning; |
| DEP-09-06-026 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-02 | INITIALIZED | TBD | Receives registration and drafts for the workflow round trip (CA §11.1; W14-01, W14-09); outside D1. | ScopeOfWork.md#CLM-003 (as revised per C1 S9-6-3) | App DEL-02-02 (later undertaking) supplies review and registration; |
| DEP-09-06-027 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-01 | INITIALIZED | TBD | Receives catalog, read-basis and evidence-label meanings cited per step (CA §2.3, §7.1, §11.1). | ScopeOfWork.md#CLM-003 (as revised per C1 S9-6-3) | App DEL-03-01, DEL-03-02 and DEL-03-03 supply catalog/read-basis, proposal/outcome and external-receiving meanings; |
| DEP-09-06-028 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 | INITIALIZED | TBD | Receives proposal lifecycle and outcome meanings cited per step (CA-2, CA-4, CA-5; §11.1). | ScopeOfWork.md#CLM-003 (as revised per C1 S9-6-3) | App DEL-03-01, DEL-03-02 and DEL-03-03 supply catalog/read-basis, proposal/outcome and external-receiving meanings; |
| DEP-09-06-029 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-03 | INITIALIZED | TBD | Receives channel states, model destination, carriage assurance and the XF inventory (CA §11.1). | ScopeOfWork.md#CLM-003 (as revised per C1 S9-6-3) | App DEL-03-01, DEL-03-02 and DEL-03-03 supply catalog/read-basis, proposal/outcome and external-receiving meanings; |
| DEP-09-06-030 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-01 | INITIALIZED | TBD | Receives act and policy meanings cited per step (CA S-8, CA-2, CA-H; §11.1). | ScopeOfWork.md#CLM-003 (as revised per C1 S9-6-3) | App DEL-04-01 carries adopted operation policy and act distinctions and App DEL-04-02 grant display, |
| DEP-09-06-031 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-02 | INITIALIZED | TBD | Receives grant display and standing meanings (CA-0, CA-H, CA-R; §11.1). | ScopeOfWork.md#CLM-003 (as revised per C1 S9-6-3) | App DEL-04-01 carries adopted operation policy and act distinctions and App DEL-04-02 grant display, |
| DEP-09-06-032 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-01 | INITIALIZED | TBD | Receives HOSTING supplied-guidance and model-destination facts (CA §4 supplied link, W14-08; §11.1). | ScopeOfWork.md#CLM-003 (as revised per C1 S9-6-3) | App DEL-01-01 supplies the App-side supplied-guidance and model-destination evidence. |
| DEP-09-06-033 | DOWNSTREAM | HANDOVER | EXTERNAL | DEP-001 | TBD | TBD | External SWBPIPE owner — human-relayed question set (RELAY_QUESTIONS_SWBPIPE.md); relayed and answered 2026-09-28 (RELAY_ANSWERS_SWBPIPE.md); answers are not commitments (DECISION-3). | ScopeOfWork.md#OUT-004 | <quote from current SoW at application> |

### DEL-09-09 — External control and catalog-extension trace

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| R9-9-1 | new arc (consumer row): UPSTREAM PREREQUISITE | DEL-05-01 | KEEP | extraction | S9-9-4 | creates N-C6 (candidate) | Proposed ID DEP-09-09-021.  |
| R9-9-2 | new arc (consumer row): UPSTREAM PREREQUISITE | DEL-04-02 | KEEP | extraction | S9-9-4 | creates N-09 (candidate) | Proposed ID DEP-09-09-022.  |
| R9-9-3 | new arc (consumer row): UPSTREAM PREREQUISITE | DEL-02-03 | AMEND | extraction | S9-9-4 (P1 refresh for R8-1) | creates N-26 (candidate) | Proposed ID DEP-09-09-023. Amended for R8-1: IN-25 is governance phase; the Phase-1 input is the compatibility report per surface. |
| R9-9-4 | mirror: DOWNSTREAM HANDOVER | DEL-03-01 | DEFER | — | — | none (not applied) | Optional; not grounded by any SoW sentence, and the consumer's row represents the arc (§2.1; O-3). |
| R9-9-5 | field edit | DEP-09-09-014 | AMEND | extraction | S9-9-5 (P1 refresh: SQ answers) | drift (non-topological) | C1 wording said "prepared, not delivered". |
| R9-9-6 | field edit | DEP-09-09-015 | AMEND | extraction | Statement refresh (no SoW change needed) | drift (non-topological) |  |

Rows to add (29 canonical columns in [`proposed_rows/DEL-09-09_proposed_rows.csv`](proposed_rows/DEL-09-09_proposed_rows.csv)):

| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |
|---|---|---|---|---|---|---|---|---|---|
| DEP-09-09-021 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-01 | INITIALIZED | PENDING | Embedded-surface receiving for the V4-EXM-24 three-surface trace: App-side loop receiving (LOOP-v0.6) (XT IN-22; CMP-03). | ScopeOfWork.md#CLM-002 (as revised per C1 S9-9-4) | `DEL-05-01` owns the App/shared embedded-loop receiving contribution used for the embedded surface of the three-channel trace; |
| DEP-09-09-022 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-02 | INITIALIZED | PENDING | Grant display and grant states (AS-v0.6) (XT IN-29; CMP-07; XC-10). | ScopeOfWork.md#CLM-002 (as revised per C1 S9-9-4) | `DEL-04-02` owns grant display states; |
| DEP-09-09-023 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-03 | INITIALIZED | PENDING | Compatibility reports per surface (EXEC EV-5, CR-7) for TS-0/CMP-01, and, for the governance phase only, hold support on X (XT IN-25). | ScopeOfWork.md#CLM-002 (as revised per C1 S9-9-4) | `DEL-02-03` owns the per-surface compatibility report and hold-support values. |

### DEL-02-04 — Additive role selection and supply

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| M-04-02-04 | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DEFER | — | — | none (not applied) | Optional supplier-side mirror in a register outside the first increment (D1); these suppliers have no Design file. Same treatment as C1-A "noted but not proposed (D1)". |

### DEL-07-01 — PEC first-consumer contract and adoption evidence

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| M-04-07-01 | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DEFER | — | — | none (not applied) | Optional supplier-side mirror in a register outside the first increment (D1); these suppliers have no Design file. Same treatment as C1-A "noted but not proposed (D1)". |

### DEL-07-02 — Connector limitation and source-file recovery paths

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| M-04-07-02 | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DEFER | — | — | none (not applied) | Optional supplier-side mirror in a register outside the first increment (D1); these suppliers have no Design file. Same treatment as C1-A "noted but not proposed (D1)". |

### DEL-08-01 — Domains query, admission and freshness contract

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| M-04-08-01 | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DEFER | — | — | none (not applied) | Optional supplier-side mirror in a register outside the first increment (D1); these suppliers have no Design file. Same treatment as C1-A "noted but not proposed (D1)". |

### DEL-08-02 — Later research-to-design receiving activity

| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |
|---|---|---|---|---|---|---|---|
| M-04-08-02 | mirror: DOWNSTREAM HANDOVER | DEL-03-04 | DEFER | — | — | none (not applied) | Optional supplier-side mirror in a register outside the first increment (D1); these suppliers have no Design file. Same treatment as C1-A "noted but not proposed (D1)". |

## 5. Matching `_DEPENDENCIES.md` text

**Grounded rows.** In the extraction route, the human-owned sections do not change (Dependency Tracking Mode, Declared Upstream and Declared Downstream). `dependency-extract` refreshes the agent-owned sections under the headings each file already uses (SPEC §5.2). The expected results are below.

**Rows needing P1.** If P1 adds no SoW sentence and the owner instead declares the relationship (O-2), the owner or the recorder writes the listed §5.2 entries into the human-owned section on the owner's recorded direction. `dependency-extract` then mirrors each entry, in any MODE, as an `Origin=DECLARED` row. Per the workflow, the section heading sets the type (PREREQUISITE or ENABLES). Where the proposed INTERFACE/HANDOVER type matters, a direct `Origin=DECLARED` CSV row keeps it.

#### DEL-04-01

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route.
- **Extracted Dependency Register** after application: ACTIVE 21 → 29 with grounded rows only, or 29 with the P1-dependent rows too; ANCHOR 11 unchanged; EXECUTION 10 → 18 / 18; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-04-01-022 | EXECUTION | DOWNSTREAM | DEL-03-02 | HANDOVER |`
  - `| DEP-04-01-023 | EXECUTION | DOWNSTREAM | DEL-05-01 | HANDOVER |`
  - `| DEP-04-01-024 | EXECUTION | DOWNSTREAM | DEL-05-02 | HANDOVER |`
  - `| DEP-04-01-025 | EXECUTION | DOWNSTREAM | DEL-03-03 | HANDOVER |`
  - `| DEP-04-01-026 | EXECUTION | DOWNSTREAM | DEL-03-04 | HANDOVER |`
  - `| DEP-04-01-027 | EXECUTION | DOWNSTREAM | DEL-09-09 | HANDOVER |`
  - `| DEP-04-01-028 | EXECUTION | UPSTREAM | OI-021 | CONSTRAINT |`
  - `| DEP-04-01-029 | EXECUTION | UPSTREAM | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | CONSTRAINT |`
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-04-01-017, DEP-04-01-018.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; do not take the ACT §5.1 runtime resolution inputs, or the ACT §2.7 citation of LOOP §5.1.1, as production inputs: each would pull DEL-04-01 into SCC-002 (ARC_ANALYSIS §4); record the deferred optional mirrors (R-04-01-g) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-04-02

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route. Fallback if P1 adds no SoW sentence and the owner declares instead (1 entry):
  - under `## Declared Upstream (I need these before I can proceed)`: `- DEL-05-01 Minimal-loop and model receiving contract — Reason: Receives the host-agent network rules (LOOP §5.1.1 NW-8…NW-16: category switches, named entries, in-work grant scopes, always-off items) that the grant display shows (AS §3, R8-13; DECISION-5).` / `  - Required maturity: INITIALIZED` / `  - Location: PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract`. Mirrored by dependency-extract as an `Origin=DECLARED` row typed `PREREQUISITE` from the heading. If the owner wants `INTERFACE` kept, record a direct `Origin=DECLARED` CSV row instead.
- **Extracted Dependency Register** after application: ACTIVE 14 → 24 with grounded rows only, or 25 with the P1-dependent rows too; ANCHOR 6 unchanged; EXECUTION 8 → 18 / 19; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-04-02-015 | EXECUTION | UPSTREAM | DEL-03-02 | INTERFACE |`
  - `| DEP-04-02-016 | EXECUTION | UPSTREAM | DEL-03-01 | INTERFACE |`
  - `| DEP-04-02-017 | EXECUTION | UPSTREAM | DEL-02-03 | INTERFACE |`
  - `| DEP-04-02-018 | EXECUTION | DOWNSTREAM | DEL-05-01 | HANDOVER |`
  - `| DEP-04-02-019 | EXECUTION | DOWNSTREAM | DEL-05-02 | HANDOVER |`
  - `| DEP-04-02-020 | EXECUTION | DOWNSTREAM | DEL-03-02 | HANDOVER |`
  - `| DEP-04-02-021 | EXECUTION | DOWNSTREAM | DEL-03-03 | HANDOVER |`
  - `| DEP-04-02-022 | EXECUTION | DOWNSTREAM | DEL-02-03 | HANDOVER |`
  - `| DEP-04-02-023 | EXECUTION | UPSTREAM | OI-021 | CONSTRAINT |`
  - `| DEP-04-02-024 | EXECUTION | UPSTREAM | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | CONSTRAINT |`
  - `| DEP-04-02-025 | EXECUTION | UPSTREAM | DEL-05-01 | INTERFACE |` (P1-dependent)
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-04-02-011, DEP-04-02-012.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record the deferred optional mirrors (R-04-02-b, R-04-02-j, R-04-02-k) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-04-03

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route. Fallback if P1 adds no SoW sentence and the owner declares instead (1 entry):
  - under `## Declared Upstream (I need these before I can proceed)`: `- DEL-05-01 Minimal-loop and model receiving contract — Reason: Receives host-loop events and the network rules through DEL-05-01 (LOOP §2.3, §5.1.1) for R15 network destinations, and observer-attributed unknown, run-resumed/run-ended (RS §10).` / `  - Required maturity: INITIALIZED` / `  - Location: PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract`. Mirrored by dependency-extract as an `Origin=DECLARED` row typed `PREREQUISITE` from the heading. If the owner wants `INTERFACE` kept, record a direct `Origin=DECLARED` CSV row instead.
- **Extracted Dependency Register** after application: ACTIVE 20 → 31 with grounded rows only, or 32 with the P1-dependent rows too; ANCHOR 10 unchanged; EXECUTION 10 → 21 / 22; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-04-03-021 | EXECUTION | UPSTREAM | DEL-04-01 | INTERFACE |`
  - `| DEP-04-03-022 | EXECUTION | UPSTREAM | DEL-03-02 | INTERFACE |`
  - `| DEP-04-03-023 | EXECUTION | UPSTREAM | DEL-04-02 | INTERFACE |`
  - `| DEP-04-03-024 | EXECUTION | DOWNSTREAM | DEL-05-01 | HANDOVER |`
  - `| DEP-04-03-025 | EXECUTION | DOWNSTREAM | DEL-05-02 | HANDOVER |`
  - `| DEP-04-03-026 | EXECUTION | DOWNSTREAM | DEL-09-06 | HANDOVER |`
  - `| DEP-04-03-027 | EXECUTION | DOWNSTREAM | DEL-09-09 | HANDOVER |`
  - `| DEP-04-03-028 | EXECUTION | UPSTREAM | DEL-03-01 | INTERFACE |`
  - `| DEP-04-03-029 | EXECUTION | UPSTREAM | DEL-02-03 | INTERFACE |`
  - `| DEP-04-03-030 | EXECUTION | UPSTREAM | DEL-03-03 | INTERFACE |`
  - `| DEP-04-03-031 | EXECUTION | UPSTREAM | DEL-01-01 | INTERFACE |`
  - `| DEP-04-03-032 | EXECUTION | UPSTREAM | DEL-05-01 | INTERFACE |` (P1-dependent)
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-04-03-012, DEP-04-03-019.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record that no DOWNSTREAM row to DEL-03-02 is written: the disputed arc N-12 is withheld per the K1 ruling, and the RS §10 "DEL-03-02 consumes §5 evidence rules" cell goes to the owner as a wording finding; record the deferred optional mirrors (R-04-03-d, R-04-03-e, R-04-03-j, R-04-03-o, R-04-03-p) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-02-01

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route. Fallback if P1 adds no SoW sentence and the owner declares instead (2 entries):
  - under `## Declared Upstream (I need these before I can proceed)`: `- DEL-02-03 Workflow execution compatibility and round-trip support — Reason: Receives the Phase-1 statement (EXEC §2.1), governance-phase scope (§2.2), report and hold support (§3.6, governance phase), hold machine (§4), App capture (§5) and transfer (§6) (WD §8).` / `  - Required maturity: INITIALIZED` / `  - Location: PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support`. Mirrored by dependency-extract as an `Origin=DECLARED` row typed `PREREQUISITE` from the heading. If the owner wants `INTERFACE` kept, record a direct `Origin=DECLARED` CSV row instead.
  - under `## Declared Downstream (These need me)`: `- DEL-03-03 Local external-agent receiving adapter — Reason: Supplies the governing checkpoint constraint derivation rule to the external adapter (WD §9 A-12: consumers DEL-05-01, DEL-03-03).` / `  - Required maturity: INITIALIZED` / `  - Location: PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter`. Mirrored by dependency-extract as an `Origin=DECLARED` row typed `ENABLES` from the heading. If the owner wants `HANDOVER` kept, record a direct `Origin=DECLARED` CSV row instead.
- **Extracted Dependency Register** after application: ACTIVE 24 → 29 with grounded rows only, or 31 with the P1-dependent rows too; ANCHOR 16 unchanged; EXECUTION 8 → 13 / 15; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-02-01-025 | EXECUTION | UPSTREAM | DEL-01-01 | INTERFACE |`
  - `| DEP-02-01-026 | EXECUTION | UPSTREAM | DEL-02-03 | INTERFACE |` (P1-dependent)
  - `| DEP-02-01-027 | EXECUTION | UPSTREAM | DEL-03-02 | INTERFACE |`
  - `| DEP-02-01-028 | EXECUTION | DOWNSTREAM | DEL-03-03 | HANDOVER |` (P1-dependent)
  - `| DEP-02-01-029 | EXECUTION | UPSTREAM | OI-021 | CONSTRAINT |`
  - `| DEP-02-01-030 | EXECUTION | UPSTREAM | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | CONSTRAINT |`
  - `| DEP-02-01-031 | EXECUTION | UPSTREAM | OI-018 | CONSTRAINT |`
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record the deferred optional mirrors (R-02-01-a, R-02-01-b, R-02-01-c, R-02-01-d, R-02-01-e, R-02-01-f, R-02-01-j, R-02-01-k2) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-02-03

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route. Fallback if P1 adds no SoW sentence and the owner declares instead (1 entry):
  - under `## Declared Upstream (I need these before I can proceed)`: `- DEL-05-01 Minimal-loop and model receiving contract — Reason: Receives arrival observation, binding, events, dispatch record and retry rules, and host-loop hold support for the governance phase (EXEC §9.1).` / `  - Required maturity: INITIALIZED` / `  - Location: PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract`. Mirrored by dependency-extract as an `Origin=DECLARED` row typed `PREREQUISITE` from the heading. If the owner wants `INTERFACE` kept, record a direct `Origin=DECLARED` CSV row instead.
- **Extracted Dependency Register** after application: ACTIVE 21 → 27 with grounded rows only, or 28 with the P1-dependent rows too; ANCHOR 8 unchanged; EXECUTION 13 → 19 / 20; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-02-03-022 | EXECUTION | UPSTREAM | DEL-03-02 | INTERFACE |`
  - `| DEP-02-03-023 | EXECUTION | UPSTREAM | DEL-05-01 | INTERFACE |` (P1-dependent)
  - `| DEP-02-03-024 | EXECUTION | UPSTREAM | DEL-04-02 | INTERFACE |`
  - `| DEP-02-03-025 | EXECUTION | UPSTREAM | DEL-01-01 | INTERFACE |`
  - `| DEP-02-03-026 | EXECUTION | UPSTREAM | DEL-03-03 | INTERFACE |`
  - `| DEP-02-03-027 | EXECUTION | UPSTREAM | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | CONSTRAINT |`
  - `| DEP-02-03-028 | EXECUTION | UPSTREAM | DEL-01-04 | INTERFACE |`
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-02-03-015, DEP-02-03-016.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record the deferred optional mirrors (R-02-03-a, R-02-03-b, R-02-03-c, R-02-03-i, R-02-03-j, R-02-03-k, R-02-03-l, R-02-03-n, R-02-03-m) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-03-01

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route. Fallback if P1 adds no SoW sentence and the owner declares instead (1 entry):
  - under `## Declared Upstream (I need these before I can proceed)`: `- DEL-04-03 Content-bound decisions and compact run records — Reason: Receives the DEL-04-03 §6.1 act field set and §7 lapse vocabulary carried in read-result standing (C §6.2).` / `  - Required maturity: INITIALIZED` / `  - Location: PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records`. Mirrored by dependency-extract as an `Origin=DECLARED` row typed `PREREQUISITE` from the heading. If the owner wants `INTERFACE` kept, record a direct `Origin=DECLARED` CSV row instead.
- **Extracted Dependency Register** after application: ACTIVE 30 → 30 with grounded rows only, or 31 with the P1-dependent rows too; ANCHOR 21 unchanged; EXECUTION 9 → 9 / 10; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-03-01-031 | EXECUTION | UPSTREAM | DEL-04-03 | INTERFACE |` (P1-dependent)
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-03-01-022, DEP-03-01-024.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record the deferred optional mirrors (M-01-1, M-01-2, M-01-3, M-01-4, M-01-5, M-01-6, M-01-7, M-01-8, N-01-mir, N-10-mir) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-03-02

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route. Fallback if P1 adds no SoW sentence and the owner declares instead (1 entry):
  - under `## Declared Upstream (I need these before I can proceed)`: `- DEL-02-01 Portable workflow contract and shared allocation — Reason: Receives workflow identity, checkpoint declarations (required act, subject class, reached-when) and the §4.3.7 item rule (P §13).` / `  - Required maturity: INITIALIZED` / `  - Location: PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation`. Mirrored by dependency-extract as an `Origin=DECLARED` row typed `PREREQUISITE` from the heading. If the owner wants `INTERFACE` kept, record a direct `Origin=DECLARED` CSV row instead.
- **Extracted Dependency Register** after application: ACTIVE 26 → 26 with grounded rows only, or 27 with the P1-dependent rows too; ANCHOR 15 unchanged; EXECUTION 11 → 11 / 12; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-03-02-027 | EXECUTION | UPSTREAM | DEL-02-01 | INTERFACE |` (P1-dependent)
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-03-02-017.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record the deferred optional mirrors (M-02-1, M-02-2, M-02-3, M-02-4, N-B2, N-18/N-21-mir, N-21-mir) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-03-03

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route. Fallback if P1 adds no SoW sentence and the owner declares instead (2 entries):
  - under `## Declared Upstream (I need these before I can proceed)`: `- DEL-01-01 Stock Codex hosting and supplier contract — Reason: Receives supplier surfaces at 0.158.0 (§3.5), A14 origins (R7–R9) and native delivery (H6) from HOSTING and the pin record (ADAPTER §11).` / `  - Required maturity: INITIALIZED` / `  - Location: PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract`. Mirrored by dependency-extract as an `Origin=DECLARED` row typed `PREREQUISITE` from the heading. If the owner wants `INTERFACE` kept, record a direct `Origin=DECLARED` CSV row instead.
  - under `## Declared Upstream (I need these before I can proceed)`: `- DEL-02-03 Workflow execution compatibility and round-trip support — Reason: Receives Phase-1 guidance and recording (EXEC §2.1) and, for the governance phase, the hold machine and per-checkpoint hold support (EXEC §2.2, §3.6) (ADAPTER §11).` / `  - Required maturity: INITIALIZED` / `  - Location: PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support`. Mirrored by dependency-extract as an `Origin=DECLARED` row typed `PREREQUISITE` from the heading. If the owner wants `INTERFACE` kept, record a direct `Origin=DECLARED` CSV row instead.
- **Extracted Dependency Register** after application: ACTIVE 12 → 12 with grounded rows only, or 14 with the P1-dependent rows too; ANCHOR 5 unchanged; EXECUTION 7 → 7 / 9; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-03-03-013 | EXECUTION | UPSTREAM | DEL-01-01 | INTERFACE |` (P1-dependent)
  - `| DEP-03-03-014 | EXECUTION | UPSTREAM | DEL-02-03 | INTERFACE |` (P1-dependent)
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-03-03-008.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record that no UPSTREAM row to DEL-04-03 (N-B8) is written: it is withheld per the K1 ruling, because RS is read "for joins only" as the destination of the adapter's evidence, and N-14 carries the relationship; record the deferred optional mirrors (M-03-1, N-B5, N-B6, N-B8, N-14-mir, N-24-mir) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-03-04

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route.
- **Extracted Dependency Register** after application: ACTIVE 20 → 23 with grounded rows only, or 23 with the P1-dependent rows too; ANCHOR 4 unchanged; EXECUTION 16 → 19 / 19; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-03-04-021 | EXECUTION | UPSTREAM | DEL-01-01 | INTERFACE |`
  - `| DEP-03-04-022 | EXECUTION | UPSTREAM | DEL-09-06 | INTERFACE |`
  - `| DEP-03-04-023 | EXECUTION | UPSTREAM | DEL-09-09 | INTERFACE |`
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-03-04-011.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes.

#### DEL-01-01

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route.
- **Extracted Dependency Register** after application: ACTIVE 24 → 24 with grounded rows only, or 24 with the P1-dependent rows too; ANCHOR 15 unchanged; EXECUTION 9 → 9 / 9; RETIRED 0 unless a SoW revision removes a stated relationship.
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-01-01-017, DEP-01-01-018.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record the deferred optional mirrors (M-11-1, M-11-2, M-11-3, M-11-4) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-05-01

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route. Fallback if P1 adds no SoW sentence and the owner declares instead (1 entry):
  - `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` is not a deliverable. Record it as a direct `Origin=DECLARED` CSV row (`UPSTREAM CONSTRAINT`), because the §5.2 entry form takes deliverable IDs.
- **Extracted Dependency Register** after application: ACTIVE 24 → 26 with grounded rows only, or 27 with the P1-dependent rows too; ANCHOR 13 unchanged; EXECUTION 11 → 13 / 14; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-05-01-025 | EXECUTION | UPSTREAM | DEL-04-02 | INTERFACE |`
  - `| DEP-05-01-026 | EXECUTION | DOWNSTREAM | DEP-001 | HANDOVER |`
  - `| DEP-05-01-027 | EXECUTION | UPSTREAM | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5 | CONSTRAINT |` (P1-dependent)
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-05-01-024.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record the deferred optional mirrors (M-04-05-01, R5-1-2) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-05-02

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route.
- **Extracted Dependency Register** after application: ACTIVE 18 → 20 with grounded rows only, or 20 with the P1-dependent rows too; ANCHOR 4 unchanged; EXECUTION 14 → 16 / 16; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-05-02-019 | EXECUTION | UPSTREAM | DEL-04-02 | PREREQUISITE |`
  - `| DEP-05-02-020 | EXECUTION | UPSTREAM | DEL-02-03 | PREREQUISITE |`
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-05-02-011, DEP-05-02-014, DEP-05-02-015, DEP-05-02-016, DEP-05-02-018.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record the deferred optional mirrors (M-04-05-02) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-09-06

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route.
- **Extracted Dependency Register** after application: ACTIVE 24 → 33 with grounded rows only, or 33 with the P1-dependent rows too; ANCHOR 11 unchanged; EXECUTION 13 → 22 / 22; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-09-06-025 | EXECUTION | UPSTREAM | DEL-02-01 | INTERFACE |`
  - `| DEP-09-06-026 | EXECUTION | UPSTREAM | DEL-02-02 | INTERFACE |`
  - `| DEP-09-06-027 | EXECUTION | UPSTREAM | DEL-03-01 | INTERFACE |`
  - `| DEP-09-06-028 | EXECUTION | UPSTREAM | DEL-03-02 | INTERFACE |`
  - `| DEP-09-06-029 | EXECUTION | UPSTREAM | DEL-03-03 | INTERFACE |`
  - `| DEP-09-06-030 | EXECUTION | UPSTREAM | DEL-04-01 | INTERFACE |`
  - `| DEP-09-06-031 | EXECUTION | UPSTREAM | DEL-04-02 | INTERFACE |`
  - `| DEP-09-06-032 | EXECUTION | UPSTREAM | DEL-01-01 | INTERFACE |`
  - `| DEP-09-06-033 | EXECUTION | DOWNSTREAM | DEP-001 | HANDOVER |`
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-09-06-012, DEP-09-06-014, DEP-09-06-022, DEP-09-06-023.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record the deferred optional mirrors (R9-6-4, R9-6-5) as "not extracted: no SoW ground; consumer row represents the arc".

#### DEL-09-09

- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route.
- **Extracted Dependency Register** after application: ACTIVE 20 → 23 with grounded rows only, or 23 with the P1-dependent rows too; ANCHOR 6 unchanged; EXECUTION 14 → 17 / 17; RETIRED 0 unless a SoW revision removes a stated relationship.
- Append to the EXECUTION summary table:
  - `| DEP-09-09-021 | EXECUTION | UPSTREAM | DEL-05-01 | PREREQUISITE |`
  - `| DEP-09-09-022 | EXECUTION | UPSTREAM | DEL-04-02 | PREREQUISITE |`
  - `| DEP-09-09-023 | EXECUTION | UPSTREAM | DEL-02-03 | PREREQUISITE |`
- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): DEP-09-09-014, DEP-09-09-015.
- **Run Notes / Run History** (agent-owned): append one run entry. SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE; record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes; record the deferred optional mirrors (R9-9-4) as "not extracted: no SoW ground; consumer row represents the arc".

## 6. Application briefs (for node A*, after K1)

Use one brief per deliverable, in this order:
1. `scope-of-work` REVISE applies the accepted SoW amendment (P1).
2. `dependency-extract` runs.
3. The run's added-arc set is compared with this file before the currency audit.

An arc outside this file goes to the integrator. It is not accepted silently.

```yaml
Workflow: chirality-root:bundled:workflow:dependency-extract
SCOPE: <DEL-ID>                       # one of the 14 hosts above; one brief each
RUN_ROOT: <abs>/projects/chirality-app-v4/execution
DECOMPOSITION_PATH: <abs>/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md
SOURCE_DOCS: [ScopeOfWork.md]         # as revised; Design files corroborate only (_COORDINATION.md rule)
MODE: UPDATE
STRICTNESS: CONSERVATIVE
CONSUMER_CONTEXT: NONE
ARCHITECTURE_BASIS_POLICY: NONE
ApplyEdits: true
AllowedWriteTargets:
  - <deliverable>/Dependencies.csv
  - <deliverable>/_DEPENDENCIES.md
  - <deliverable>/_run_records/
ExpectedChanges: DAG_PREP/REGISTER_CHANGES.md §4 (<DEL-ID>) and DAG_PREP/proposed_rows/<DEL-ID>_proposed_rows.csv
ReturnCheck: >
  List every ACTIVE EXECUTION deliverable-target row added, retired or retargeted,
  as consumer -> supplier arcs, and compare them with ExpectedChanges. Report any
  difference as a finding. Keep SatisfactionStatus on matched rows. Run
  validate_dependencies_schema.py, validate_enum.py and validate_id_format.sh.
  Report EVQ/DRB (validate_decomposition_registers.py --families EVQ,DRB) for
  this register.
Withheld (K1 ruling): N-12 (no DEL-03-02<->DEL-04-03 consumption row); N-B8 (no DEL-03-03 UPSTREAM DEL-04-03)
```

Deliverable-specific notes for the briefs:
- **DEL-04-01:** SoW only. Do not take ACT §5.1 or §2.7 as production inputs (§2.4 item 3).
- **DEL-02-01:** confirm that P1's SC-02-01-1 wording names DEL-03-03 as a receiver (§2.4 item 1).
- **DEL-02-03:** X-1 (DEL-01-04) is expected from SC-02-03-4 unless P1 moves that sentence (§2.4 item 2).
- **DEL-04-03 and DEL-03-03:** see the withheld rows.
- **DEL-05-02:** S5-2-3 is applied in its main option (N-25). If the owner chooses the "via DEL-05-01" alternative, R5-2-2 is not written and N-25 drops out. That changes no SCC.
- **Rows needing P1:** each is written only if its P1 sentence was applied. Otherwise the owner's declaration route (§5) applies, or the row is left out and N-xx is recorded as not taken.

## 7. Residuals routed to owners, not applied here

- **RS-v0.6 §10, the DEL-03-02 row** ("Consumes (meaning): §5 evidence rules"), goes to DEL-04-03's owner for the next RS revision. It is the only text supporting N-12, and P-v0.6 §13 does not reflect it (ARC_ANALYSIS §3).
- **ADAPTER-v0.4 header**, "for joins only: … DEL-04-03/RS … R5, R7, R11, R13", goes to DEL-03-03's owner, with the same treatment for N-B8.
- **Deferred supplier-side mirror requests** go to the register owners. These are V1-C RF-3, RF-8; V1-B RF-08; GUIDE F-4 (supplier side); and the "observed" rows. The requests stay open for the owner to declare or defer (O-3).
- **SatisfactionStatus convention.** V1-B RF-09 found `TBD` in some registers and `PENDING` in others. The register owner decides the convention, and it has no DAG effect (O-6).
- **`Open_Issues.csv` OI-001/OI-002** are still OPEN (ACT F-8). They go to the decomposition owner through that owner's route, as C1 recorded.
