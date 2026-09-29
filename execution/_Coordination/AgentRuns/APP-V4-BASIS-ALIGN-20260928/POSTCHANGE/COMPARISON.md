# Pre/post comparison — SCA-V4-001 candidate (node AK1)

Compares `POSTCHANGE/coverage_summary.json` (sha256 `4b6d9622…9ca7`) and its issue log with
`BASELINE/coverage_summary.json` (sha256 `d8ac5c4d…20f9`). Both runs use the same seven packages, the same check
script (two label lines differ) and the same inventory. A control run of the same script on the pre-application tree
at `f4ba34c2c` separates the two causes of difference:

- **basis drift** `306291bdd` → `f4ba34c2c`: only the 14 `_STATUS.md` files recorded IN_PROGRESS under owner
  DECISION-6 (commit `67a2fac4b`) changed an audit input;
- **the SCA-V4-001 candidate**: the 15 files written after checkpoint group 2.

## 1. Headline

| Measure | BASELINE | Control (`f4ba34c2c`) | POSTCHANGE |
|---|---|---|---|
| BLOCKER / WARNING / INFO / EXPECTED_CONSEQUENCE | 0 / 2 / 126 / 0 | 0 / 39 / 89 / 0 | 0 / 38 / 94 / 0 |
| Total findings | 128 | 128 | 132 |
| `overall_status` / `closure_readiness` | WARNINGS / WARN | WARNINGS / WARN | WARNINGS / WARN |
| Lifecycle (scoped) | INITIALIZED 30 | INITIALIZED 16, IN_PROGRESS 14 | INITIALIZED 16, IN_PROGRESS 14 |
| Lifecycle (all 41) | INITIALIZED 41 | INITIALIZED 27, IN_PROGRESS 14 | INITIALIZED 27, IN_PROGRESS 14 |
| `extensions.working_vs_group3_differences` | 3 files | 3 files | 8 files |

Unchanged in all three runs: partitions 7/7; production units 30/30; reverse coverage, context fidelity and objective
coverage 100 %; artifact presence 11.22 % (11/98); deliverables and IN rows without an objective mapping 0;
`package_shape_conformance` WARN; `objective_evidence_integrity` PASS; Checks 9, 10 and handoff state SKIPPED;
`repository_topology` 11 / 41 / 10 / 262 / 262; the 30 scoped `ScopeOfWork.md` hashes and frontmatter;
`open_issue_status_counts`; the 30 context-match results (all MATCH).

## 2. Every difference and its cause

Issue IDs are sequential per run, so matching is by check, entity and description.

### 2a. Caused by basis drift (DECISION-6 lifecycle), not by the amendment

| # | BASELINE | POSTCHANGE | Cause |
|---|---|---|---|
| D1 | 37 Check-6 findings at INFO ("lifecycle INITIALIZED") for DEL-01-01 (4), DEL-02-01 (3), DEL-02-03 (3), DEL-03-01 (1), DEL-03-02 (2), DEL-03-03 (2), DEL-03-04 (2), DEL-04-01 (2), DEL-04-02 (1), DEL-04-03 (4), DEL-05-01 (3), DEL-05-02 (3), DEL-09-06 (4), DEL-09-09 (3) | the same 37 at WARNING ("lifecycle IN_PROGRESS") | The Check-6 rule escalates an absent anticipated artifact to WARNING for IN_PROGRESS units. The 14 units moved INITIALIZED → IN_PROGRESS at `67a2fac4b` (DECISION-6). The control run shows the identical 37 escalations before any amendment edit. The artifact counts are unchanged (11/98) |
| D2 | `lifecycle_distribution` INITIALIZED 30 | INITIALIZED 16, IN_PROGRESS 14 | Same cause |

### 2b. Caused by the SCA-V4-001 candidate

| # | BASELINE | POSTCHANGE | Cause |
|---|---|---|---|
| D3 | COV-121 WARNING (Check 9): `SOFTWARE_DECOMP.md` says no folders or SoWs exist | **closed** | D-16 replaced the stale sentence (accepted, candidate edit). Expected by IMPACT_ASSESSMENT §9 |
| D4 | COV-064 (Check 6) artifact text "TEST: missing-tool, checkpoint hold and source-preserving round-trip fixtures" | COV-064 same finding, text "TEST: missing-tool, checkpoint recording (governance-phase hold retained) and source-preserving round-trip fixtures" | D-10b changed DEL-02-03 `AnticipatedArtifacts`. Same finding; its severity moved INFO → WARNING by D1 |
| D5 | COV-083 (Check 6) artifact text "TEST: malformed-call, endpoint and responsiveness conformance cases" | COV-083 text "TEST: malformed-call, destination and responsiveness conformance cases" | D-11d changed DEL-05-01 `AnticipatedArtifacts`. Same finding; severity by D1 |
| D6 | — | 5 new INFO (Check 9): `Consolidated_Coverage.csv` (COV-122), `Deliverables.csv` (COV-123), `Packages.csv` (COV-126), `ScopeLedger.csv` (COV-128), `Vocabulary_Map.csv` (COV-129) differ from GROUP3 canonical | The accepted candidate edits D-01…D-13 and the B8 recompute. The issue text is the baseline script's fixed wording ("later standing/receiving-currency update, not a scope/structure change"); for these five the actual cause is SCA-V4-001 (MODIFY of text and bound hashes; no ID, mapping, count or structure change) |
| D7 | COV-124/COV-125 INFO: `Open_Issues.csv` `77ecfea2…` and `SOFTWARE_DECOMP.md` `5b66fefd…` differ from GROUP3 | COV-125/COV-127 INFO: same files, now `f6b92362…` and `98e8bc4b…` | Pre-existing differences; the hashes changed by D-14a/b and D-16 |
| D8 | `extensions.working_vs_group3_differences` 3 files | 8 files | D6 plus the unchanged `External_Dependencies.csv` |
| D9 | Check 5: 30/30 MATCH | 30/30 MATCH | No difference. It confirms the B7 mirrors: the four edited `_CONTEXT.md` still equal `Deliverables.csv` and `Packages.csv` field for field |

### 2c. Expected changes that did not occur (not caused by a failure of the candidate)

| # | Packet expectation (IMPACT_ASSESSMENT §9) | POSTCHANGE | Cause |
|---|---|---|---|
| D10 | The Change Register part of COV-127 closes | Still open: COV-131 WARNING (Check 9b), "Decision Log" and "Revision History" get no heading hit | D-15, which adds `## Decision Log`, carries `{ACCEPT_DATE}` and `{AMENDMENT_SNAPSHOT}` and is acceptance-conditional (BASIS_AMENDMENT D-15; scope-change method, "Acceptance-conditional edits"). It is not applied before group-3 acceptance. `projections.json`: with D-15 applied, "Decision Log" binds at rank exact, 1 hit. The rest of COV-131 (Ledger, Objectives, Partitions, Production Units) is pre-existing and stays |
| D11 | COV-119 and COV-120 close on the telemetry recompute | Still open (COV-119, COV-120 INFO) | `Coverage_Telemetry.json` was not rewritten. The accepted packet routes its recompute to "the post-change baseline" (owner audit-decomp, which is read-only), and the O-3 write boundary, "named exactly", does not list the file. `projections.json` gives the register-derivable recompute: `OpenIssuesByType`, `ActiveOpenIssueCount` (24 → 23), `ResolvedIssueIDs` (adds OI-017), `checks.no_production_folders_or_SoWs_created` (true → false; 41 folders with a ScopeOfWork.md) and `inputs` (new Packages/Deliverables/ScopeLedger hashes) differ; the counts are unchanged. `standing`, `Revision` and `Date` are not derivable and the packet gives no text for them. Group 3 decides |

## 3. Classification for group 3 (method step 5)

| Finding(s) | Severity | Classification | Basis |
|---|---|---|---|
| 37 Check-6 WARNINGs (D1) | WARNING | Not an SCA-V4-001 effect; present at the application basis (control run). Not `EXPECTED_CONSEQUENCE` of this amendment | DECISION-6 lifecycle; artifacts not yet produced |
| COV-131 (Check 9b) | WARNING | Change Register part: `EXPECTED_CONSEQUENCE` of the group-2 decision holding D-15 (`SCA-V4-001_GROUP-2_2026-09-28`, BASIS_AMENDMENT D-15). Other headings: pre-existing | One finding with both parts; it stays WARNING |
| COV-119, COV-120 | INFO | Pre-existing (IMPACT_ASSESSMENT §9) | Telemetry not rewritten (D11) |
| COV-122, 123, 126, 128, 129 and the rehashed COV-125, 127 | INFO | Intended consequence of the accepted candidate edits | Group-2 register rows 18–31 |
| All other INFO | INFO | Unchanged from BASELINE | — |

- `AuditState` (raw): **WARNINGS** (0 BLOCKER, 38 WARNING).
- `AdjustedAuditState` (excluding `EXPECTED_CONSEQUENCE`): **WARNINGS**. The Change Register part of COV-131 is
  expected, but the finding also carries pre-existing heading bindings, and the 37 lifecycle WARNINGs are not caused by
  this amendment.
- No new orphan, parentless deliverable or ledger row; no ID, mapping, count or objective change; no BLOCKER.
