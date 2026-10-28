# Handoff state — SCA-V4-003 (ACCEPTED, active snapshot)

**Status.** Accepted. The owner accepted checkpoint group 3 on 2026-10-03
(DECISION-2 of run `APP-V4-SCA003-20261002`: "I accept the audited result.";
`checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/`). This folder is the
immutable accepted amendment snapshot, and `_ScopeChange/_LATEST.md` names it
in SPEC §11.2 form. Node AK2 (part 1) applied F-1…F-4 and H-1…H-3 after the
act ("Applied after the act", below). The candidate version of this file as
presented is sha256 `4f3f31b971a8a7c817a32604a22b99697731cd18283f72de4e443d6e099ec167`,
bound in the group-3 manifest. Sections written before the act (the
acceptance-time list, "Remaining human decisions", "Next owning workflows")
are kept as presented; group 3 and steps 1–2 of the next workflows are now
done.

**Candidate and review.** The candidate was applied and committed at
`fa16393978`. Independent review `RUN/reviews/V24.md` (committed `64a01f0c4c`)
found no blocking finding: READY FOR GROUP 3 after M-1. This revision (node
AK1-R) makes the M-1 fix and the minors m-1, m-2, m-3, m-5 and m-6. It
changes only this file, `RUN_SUMMARY.md` and one note in `Decision_Log.md`,
and adds records under `RUN/Application/`. No applied, accepted or
group-bound byte changed. `RUN` = `execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002`.

**Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE`

## Candidate and pointer posture

| Item | Value |
|---|---|
| Candidate snapshot | `execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/` |
| Posture | `ACCEPTED_PREDECESSOR` |
| Accepted predecessor | `execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/`. Its closure is `OPEN_PENDING_DERIVATIVE_CLOSURE`; its effective state is updated by `_PostAcceptanceValidation/SCA-V4-002_20261004T002903Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md` |
| `ACCEPTED_GROUP2_DECISION_SNAPSHOT` | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/` (committed `ec267bdb9f`; pointer `SCA-V4-003_GROUP-2_AUTHORIZED.md`) |
| Group-1 decision snapshot | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-1_2026-10-03/` (committed `3e747b7685`) |
| Expected pre-acceptance pointer state | `_ScopeChange/_LATEST.md` sha256 `2b7938bc82aa9b08a2bd26d7f2c0169c538edb1e6ae5423d5757def968f0c2e1`, naming SCA-V4-002 (verified unchanged) |
| Candidate commit | `fa16393978`: application, C-02 and post-change audit (basis `ec267bdb9f`). Revised records follow in the commit that carries this revision |

## Authoritative action register

`Amendment_Actions.csv`, SHA-256
`9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c`, as bound
in the group-2 `ACCEPTED_MANIFEST.csv`. The copy in this folder is
byte-identical.
- 23 rows, all `MODIFY`.
- `ScopeChanging` is `YES` on rows 2, 3, 4, 5, 7, 8, 9 and 10.
- `SupersessionBindingPresent` is `YES` on row 21 only.

`Intake_Actions.csv` is group-1 evidence only.

## Authoritative truth changed in this candidate

| Edit | Target | Result |
|---|---|---|
| B-02 option B (row 21), B-03 (row 22) | `_Decomposition/Open_Issues.csv` | sha256 `9c2d916c277f8ce4b847c9c532822d0566e59517ba9e0a86b650fe0450f3515d` (was `a1178218…80f0`); OI-009 `RESOLVED_BY_OWNER_DECISION`; OI-018 pointer; OPEN 23 → 22 |
| D-021 | `Supersession_Delta.csv` (this folder) | 1 row; `Supersession_Map.csv` 30 rows (29 carried + D-021), 0 findings |
| C-02 | `_PostAcceptanceValidation/SCA-V4-002_20261004T002903Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md` | sha256 `ef2c22d74707a34b7804e2a3a6e83fa56f7f4f0219002b18e6b831e8abee6385` |

The candidate wrote nothing else: no other decomposition file, basis
document, `_CONTEXT.md`, `_STATUS.md`, ScopeOfWork, register or `_DAG` file.

## Dates and stamps used at acceptance (m-2)

- **`{ACCEPT_DATE}`** is the owner's local calendar date of the group-3 act.
  It is the date the run's `OWNER_DECISIONS.md` records in that decision's
  heading ("(owner, exact, YYYY-MM-DD)"), as DECISION-1 records 2026-10-03.
  - `OWNER_DECISIONS.md` records no time zone. This session's commits carry
    the offset `-0600` (US Mountain daylight time, America/Denver). That is
    an inference from the commit offsets, not a recorded fact.
  - The SCA-V4-002 precedent: act on 2026-09-29 local, pointer `Updated:
    2026-09-29`, post-acceptance folder `20260930T021014Z` (UTC).
  - One value fills every `{ACCEPT_DATE}` slot: B-01, C-01 (`Updated:` and the
    `**Accepted:**` line) and the group-3 folder name.
- **`{UTC}` and `{C02_UTC}`** are UTC stamps (`YYYYMMDDTHHMMSSZ`). They can
  fall on the next calendar day for an evening act.
  - `{C02_UTC}` = `20261004T002903Z`: the committed C-02 folder of a
    2026-10-03 local act.
  - `{UTC}` is the stamp of the H-3 folder, taken when it is created.

## Applied only after group-3 acceptance (acceptance-conditional), exactly

Nothing on this list is applied before the act. An edit not on this list
returns to the owner. The method calls F-1 to F-4 "output and snapshot
writing around the accepted state". They are confined to the files and
lines named here. `{CLOSURE_VERDICT}` is the verdict the owner accepts
(proposed `OPEN_PENDING_DERIVATIVE_CLOSURE`); `{DECISION_REF}` is that act's
reference in `OWNER_DECISIONS.md`; `{ACT_TEXT}` is the owner's exact words.

| # | Item | Target and before | After (exact line or fill rule) |
|---|---|---|---|
| F-1 | Group-3 decision snapshot (contract "Checkpoint snapshots"; `check_amendment_reopen.py` heading form) | New folder `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-3_{ACCEPT_DATE}/` | Three files. **`DECISION.md`**: first line exactly `# SCA-V4-003 checkpoint group 3 — accepted audited poststate`. If the owner accepts with qualifications, the word `accepted` stays directly after the dash, followed by a space. The body transcribes `{ACT_TEXT}` with custody (record path, sha256, commit) and the package presented (`fa16393978`, this revision's commit, V24). **`ACCEPTED_MANIFEST.csv`**: header `Path,SHA256,Role,AcceptanceBoundary`. It binds the 13 artifacts at the hashes in `RUN/Application/CANDIDATE_ARTIFACTS.sha256`, plus `RUN/reviews/V24.md`, `RUN/POSTCHANGE/coverage_summary.json` and `OWNER_DECISIONS.md` at the act. **`Handoff_State.md`**: next stage. Committed before propagation |
| F-2 | `Decision_Log.md` group-3 entry and standing line | Lines 3–4 now read `**Standing: CANDIDATE amendment folder (posture \`ACCEPTED_PREDECESSOR\`);` / `checkpoint group 3 not yet presented.** Human decisions are quoted exactly;` | Lines 3–4 become `**Standing: ACCEPTED amendment snapshot (posture \`ACCEPTED_PREDECESSOR\`);` / `checkpoint group 3 accepted by {DECISION_REF} on {ACCEPT_DATE}.** Human decisions are quoted exactly;`. One row is appended to "Human decisions": `\| {DECISION_REF} \| {ACCEPT_DATE} \| group 3 \| "{ACT_TEXT}" \| …record, sha256, commit… \|`. A section `## Execution-stage records (after {DECISION_REF})` is appended, one entry each for F-1, F-3, F-4 and H-1 to H-3 with result hashes. No earlier line changes |
| F-3 | This file's accepted status lines | Line 1 `# Handoff state — SCA-V4-003 (CANDIDATE, before group 3)`; the `**Status.**` paragraph; the closure-verdict line `**Closure verdict:** \`OPEN_PENDING_DERIVATIVE_CLOSURE\` (proposed, for the owner's acceptance at group 3)` | Line 1 becomes `# Handoff state — SCA-V4-003 (ACCEPTED, active snapshot)`. The `**Status.**` paragraph names `{DECISION_REF}`, `{ACCEPT_DATE}`, this folder as the accepted snapshot, and `_LATEST.md` naming it. The verdict line becomes `**Closure verdict:** \`{CLOSURE_VERDICT}\``. State fields: DecompositionTruthState INCOMPLETE → COMPLETE (after H-1); DownstreamRerunState FROZEN → IN_PROGRESS; AuditState and AdjustedAuditState take the H-3 result; the others are unchanged. Applied H-1…H-3 rows with result hashes are added. The candidate version's hash is kept in the F-1 manifest, as SCA-V4-002 did |
| F-4 | `RUN_SUMMARY.md` accepted status lines | Line 1 `# Run summary — SCA-V4-003 (CANDIDATE, before group 3)`; the bullets "Group 3 is not yet presented." and "**Pointer:** `_ScopeChange/_LATEST.md` still names SCA-V4-002 (unchanged)."; the verdict line as in F-3 | Line 1 becomes `# Run summary — SCA-V4-003 (ACCEPTED, active snapshot)`. The first bullet becomes `{DECISION_REF}, group 3, "{ACT_TEXT}" ({ACCEPT_DATE}).`; the second becomes `**Pointer:** \`_ScopeChange/_LATEST.md\` names this folder (\`Latest: SCA-V4-003_2026-10-03_1827\`).`. The verdict line and state fields change as in F-3. The candidate version's hash is kept in the F-1 manifest |
| H-1 | B-01, the Change Register entry | `_Decomposition/SOFTWARE_DECOMP.md` (now `ea3388bc…d7d5`). The old block "Snapshot: `../_ScopeChange/SCA-V4-002_2026-09-29_1901`.⏎⏎## Checkpoint and next stage" occurs once | The packet's new block. `{ACCEPT_DATE}` per the rule above; `{AMENDMENT_SNAPSHOT}` = `SCA-V4-003_2026-10-03_1827`. The clause slots were fixed by group-2 `DECISION.md`: `{Q5_CLAUSE}` = `, including the App act control in DEL-01-04`; `{OI009_CLAUSE}` = `Open_Issues OI-009 Status (RESOLVED_BY_OWNER_DECISION) and Consequence`; `{OI018_CLAUSE}` = ` and the OI-018 Consequence pointer`; `{D021_CLAUSE}` = `; and a Supersession_Delta row binding the GROUP3 OI-009 Status`. **Expected result rule:** only `{ACCEPT_DATE}` varies. The result adds exactly one entry line and one blank line, no `{` remains, and nothing else changes. The expected sha256 for each candidate date is in `RUN/Application/SIMULATED_POSTACCEPT.md`; the actual hash is recorded at application |
| H-2 | C-01, `_ScopeChange/_LATEST.md` in SPEC §11.2 form (BASIS_AMENDMENT C-01 text) | Whole file (now `2b7938bc…c2e1`) | `{AMENDMENT_SNAPSHOT}` = `SCA-V4-003_2026-10-03_1827`; `{ACCEPT_DATE}`; `{CLOSURE_VERDICT}`; `{G1_DATE}` = `{G2_DATE}` = `2026-10-03`; `{C02_UTC}` = `20261004T002903Z`; `{UTC}` = the H-3 folder's stamp. No `{` remains. The registered parser `_latest_pointer_target` must return `SCA-V4-003_2026-10-03_1827` |
| H-3 | Post-acceptance validation | New `_PostAcceptanceValidation/SCA-V4-003_{UTC}/` | Compare the applied bytes and hashes with H-1, H-2 and F-1 to F-4. Rerun `RUN/BASELINE/audit_checks.py` **unchanged** (byte-identical; m-1) with `audit_structure.py`, scope PKG-01, 02, 03, 04, 05, 09, 10. Check 10 must pass for the new active snapshot. Disclose the script's known wording limits instead of editing it (below) |

**Known wording limits of the unchanged script at H-3 (m-1).**
- COV-121 and COV-123 attribute working-vs-GROUP3 differences only to the
  SCA-V4-001 and SCA-V4-002 registers.
- `expected_source.predecessor_amendment` is hard-coded to SCA-V4-001.
- The file-parity extension compares against SCA-V4-002's accepted
  poststate, so `Open_Issues.csv` (and, after H-1 and H-2,
  `SOFTWARE_DECOMP.md` and `_ScopeChange/_LATEST.md`) show as different
  there by design.

The script resolves the active snapshot from `_LATEST.md` (its change (f))
and ignores the `**Accepted predecessor:**` line (change (g)), so Check 10
needs no edit. A simulation of the state after acceptance (H-1 and H-2
applied to a scratch copy of the candidate as revised here) is recorded in
`RUN/Application/SIMULATED_POSTACCEPT.md`.

## Applied after the act (DECISION-2, node AK2 part 1)

| # | Target | Result |
|---|---|---|
| F-1 | `checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/` (`DECISION.md`, `ACCEPTED_MANIFEST.csv` with 42 rows equal to their blobs at `84b520742d`, `Handoff_State.md`) | written; hashes in `_ScopeChange/_PostAcceptanceValidation/SCA-V4-003_20261004T005706Z/POST_ACCEPTANCE_VALIDATION.md` |
| H-1 | `_Decomposition/SOFTWARE_DECOMP.md`: B-01 with `{ACCEPT_DATE}` = `2026-10-03`, `{AMENDMENT_SNAPSHOT}` = `SCA-V4-003_2026-10-03_1827` | `ea3388bc…d7d5` → `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`, the expected result |
| H-2 | `_ScopeChange/_LATEST.md`: C-01, `{UTC}` = `20261004T005706Z` | `2b7938bc…c2e1` → `19cf31f14da259d64c52b33f52598dbe66381f0a887b34a13d3eccce9388e657`; registered parser target `SCA-V4-003_2026-10-03_1827`, match True |
| F-2…F-4 | this folder's `Decision_Log.md`, `Handoff_State.md`, `RUN_SUMMARY.md` | accepted status lines only |
| H-3 | `_ScopeChange/_PostAcceptanceValidation/SCA-V4-003_20261004T005706Z/` and `RUN/POSTACCEPT/` | post-acceptance validation; the unchanged baseline script; result in `POST_ACCEPTANCE_VALIDATION.md` there |

## Post-change validation

`RUN/POSTCHANGE/COMPARISON.md`: **0 BLOCKER, 52 WARNING, 77 INFO** (baseline
0 / 35 / 93). V24 reproduced these figures.

- **35 WARNINGs** are pre-existing.
- **16 Check 6 WARNINGs** were INFO at the baseline. They are pre-existing
  artifact absences of the six deliverables the Q-13 act moved to
  IN_PROGRESS. Their severity moved because of that separate owner act, not
  the amendment. The accepted group-2 decision did not defer or exclude
  them, so they are not `EXPECTED_CONSEQUENCE`, and they are kept in the
  adjusted state (V24 O-1).
- **COV-129** (Check 10, WARNING) was this folder before its records
  existed. It is classified **`EXPECTED_CONSEQUENCE`** of the accepted
  sequence (group-2 `Handoff_State.md` step 5; IMPACT_ASSESSMENT §10 step 3;
  DECISION-1). It is closed at `fa16393978`: the unchanged script there gives
  0 / 51 / 77, with COV-129 the only difference (AK1 control; V24).
- **COV-116 and COV-121 (INFO)** changed wording and hash, the intended
  effects of B-02 and B-03. The DEL-03-04 GUIDE change (`a68a9e06e2`) moves
  no finding.

| State | Value |
|---|---|
| `AuditState` | `WARNINGS` |
| `AdjustedAuditState` | `WARNINGS` |

The raw state counts 52 WARNINGs; the adjusted state counts 51, excluding
COV-129. DAG-003 currency: 130/130 OK (`RUN/Application/DAG_CURRENCY.txt`).

## State fields

| Field | Value |
|---|---|
| `DecompositionTruthState` | `COMPLETE` |
| `DerivativePackageState` | `INCOMPLETE` |
| `ContentRemediationState` | `NOT_REQUIRED` |
| `DownstreamRerunState` | `IN_PROGRESS` |
| `MetadataAlignmentState` | `NOT_REQUIRED` |
| `ReadyForNextPhase` | `NOT_APPLICABLE` |

`AuditState` and `AdjustedAuditState` are in the table above.
`DecompositionTruthState` is COMPLETE: B-02 and B-03 in the candidate, B-01
by H-1 after the act. `DownstreamRerunState` is IN_PROGRESS: DECISION-2
authorizes the propagation, and no rerun had completed at this record. The
audit states above are confirmed by the H-3 rerun.

## Derivative packages and propagation after acceptance (accepted route, Q-3)

| Package | Owner | Status | Next required action |
|---|---|---|---|
| 19 `ScopeOfWork.md` (DEL-01-01…01-05, 02-01…02-04, 03-01…03-04, 04-01…04-03, 05-01, 09-06, 09-09) | `project-setup` INCREMENTAL → `scope-of-work` | STALE after acceptance. Blocks: SOW_REVISIONS_A (`42c9167a…fc07`, 63) and _B (`d7b5cb24…94df`, 84) | MODE=REVISE, one deliverable per brief, then MODE=VERIFY, with `STATUS_POLICY=NO_STATUS_TOUCH`. Each brief carries `AMENDMENT_REF` (SCA-V4-003, the accepted snapshot, the register row and hash), `REVISION_SCOPE` and `PRIOR_CONTRACT_SHA256`. All 19 contracts equal their SOW_REVISIONS prior hashes now |
| 20 `Dependencies.csv` and DEL-04-03 `_DEPENDENCIES.md` | `dependency-extract` | STALE after the REVISEs | UPDATE, from `ScopeOfWork.md` only, with the guards of IMPACT §10 and ARC_EFFECT §3: DEL-04-01 gains no supplier; no SCC-002 row on DEL-09-06; R17-10; exactly the 10 new arcs; NR-03, NR-06 and NR-10 not extracted; the 15 RP1-MX mirrors added |
| DAG-003 | `project-dag` | CURRENT now (130/130). Departs after the UPDATEs: +10 arcs (5 admitted, 5 held), SCCs unchanged | Currency audit → TRIGGER=SUCCESSOR → DAG-004 (owner) |
| Design pins and GUIDE pin table (20 deliverables) | App v4 design undertaking | STALE after the REVISEs | Re-pin at the next design touch, GUIDE last, with the ACCESS §13 follow-up (R22-7) |
| `_Decomposition/Coverage_Telemetry.json` | decomposition owner | STALE_REBUILD_REQUIRED (carried from SCA-V4-001; now off by one more open issue) | Bounded rebuild, outside SCA-V4-003 |
| `_Decomposition/Consolidated_Coverage.csv` | scope-change | NO_CHANGE (no basis text changes) | None |

**Active derivative surfaces (SOFTWARE):**

| Classification | Surfaces |
|---|---|
| DIRECT_EDIT, applied | `Open_Issues.csv` |
| DIRECT_EDIT, held for group 3 | `SOFTWARE_DECOMP.md` (B-01), `_ScopeChange/_LATEST.md` (C-01) |
| RECOMPUTE, open | `Coverage_Telemetry.json` |
| NO_CHANGE | the rest (Propagation_Plan §2) |

KTY remediation and KTY metadata alignment do not apply (SOFTWARE).

## Closure

The proposed verdict is the one at the top of this file. Authoritative
truth is complete once H-1 is applied. These derivatives remain open:
- the 19 REVISEs;
- the register UPDATE;
- DAG-004;
- the Design re-pins;
- `Coverage_Telemetry.json`.

No deliverable is `ISSUED` or `CHECKING`: all 20 targets are IN_PROGRESS.
The amendment authorizes no reopening and holds nothing for a reversal.

## Remaining human decisions

- Group 3: accept or return this audited poststate, its closure verdict and
  the open obligations above.
- DAG-004 acceptance, after the REVISEs and UPDATEs.

## Next owning workflows

1. Group 3 (owner).
2. After acceptance: F-1 to F-4 and H-1 to H-3.
3. `project-setup` INCREMENTAL → `scope-of-work` REVISE (19), then
   `dependency-extract` UPDATE (20).
4. `project-dag`: currency audit and the DAG-004 candidate (owner).
5. The decomposition owner, for `Coverage_Telemetry.json`.
6. The App v4 design undertaking, for the re-pins.
7. `audit-scope-closure`, for SCA-V4-003.

## Notes for the group-3 package

- **m-3:** the SCA-V4-002 effective-state note (C-02) records the Design
  re-pins as done. It records the SWBPIPE handoff "local-first" line as
  replaced in pass 2 but not yet relayed. SCA-V4-002 remains
  `OPEN_PENDING_DERIVATIVE_CLOSURE` for `Coverage_Telemetry.json` only.
- **m-4:** Q-16's group placement differs between records:
  - the group-1 pointer omits it;
  - the group-1 `DECISION.md`, manifest and handoff include it;
  - the group-2 records also list it.

  One act covered both groups, so no authority depends on the placement.
  The committed bytes are not edited.
- **m-5:** the accepted C-02 bytes say "by HELP_HUMAN". The note was
  written by AK1, a node HELP_HUMAN dispatched for this
  (`Decision_Log.md` E-6). The accepted bytes were kept.
- **O-1:** the 16 re-graded Check 6 findings are kept in
  `AdjustedAuditState`. They are not `EXPECTED_CONSEQUENCE` because the
  group-2 decision did not defer or exclude them.
- **O-2:** the group-2 manifest binds `Open_Issues.csv` at its pre-change
  hash `a1178218…80f0` (role "pre-change bytes of the direct-write
  target"). A manifest check after the candidate therefore reports 12/13
  by design. The same row records the expected post-change hash
  `9c2d916c…515d`, which the file now has.

## Carried from the predecessor

- **Not in this amendment** (OWNER_ITEMS "Not in this amendment"):
  - the DEL-04-01 → DEL-01-02 mirror and DEL-11-02's row for DEP-02-04-013
    (register owners);
  - the root `AGENTS.md` instruction notices (they need their own scope);
  - the Codex version-advance check (needs the owner's yes).
- **Held until a later decision:** Q-7 (S-01-4), Q-9 (the four A12-mapping
  rows), Q-14 (R-02-4) and the three DEFER basis items.

## The 13 required artifacts (m-6)

All 13 hashes are listed in one place:
`RUN/Application/CANDIDATE_ARTIFACTS.sha256`, which `shasum -a 256 -c`
checks from the repository root.

**Self-hash convention:** no candidate file lists its own hash, and no two
candidate files list each other's. `CANDIDATE_ARTIFACTS.sha256` is written
last, after every candidate file is final, and covers all 13, including
this file and `RUN_SUMMARY.md`.
