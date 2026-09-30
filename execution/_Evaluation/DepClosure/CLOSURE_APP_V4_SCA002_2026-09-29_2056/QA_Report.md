# QA report

RUN_STATUS = WARNINGS. Analyzer COMPLETE, exit 0, subject FAIL. Coverage PASS.

## Inventory and coverage

- **Inventory source:** `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` (sha256 `bcdf6f2f…15eb`, unchanged since DAG-001), resolved through `_LATEST_ACCEPTED.md`. That pointer file changed since DAG-002 (the SCA-V4-002 B-06a reading-rule note was appended), but it still names GROUP3-20260928T001055Z and the register it names is unchanged. 41 units in 11 packages, 41 workspace folders, no unit without a folder, no folder without a row. No exemptions.
- **Registers:** 41/41 `Dependencies.csv` present, readable and schema-valid (v3.1); 41/41 carry one `IMPLEMENTS_NODE` anchor. 41 `_DEPENDENCIES.md` read (INCLUDE_DECLARED true): 0 declared-only entries, 0 disagreements, 0 unread lines.
- **Evidence cells:** 826/826 populated. `validate_decomposition_registers.py` (SCH, EVQ, DRB, strict): 0 errors, 0 warnings; every EvidenceFile resolves deliverable-relative.
- **Rows:** 826 = 355 ANCHOR + 471 EXECUTION. EXECUTION: 465 ACTIVE, 6 RETIRED (the 5 of DAG-002's basis plus DEP-01-04-014, an EXTERNAL OI-002 constraint row retired `source_revised` by the DX run; no arc effect). Active EXECUTION by target: 258 DELIVERABLE, 149 EXTERNAL, 26 DOCUMENT, 18 PACKAGE, 14 UNKNOWN. RequiredMaturity 251 INITIALIZED / 214 TBD; SatisfactionStatus 304 TBD / 161 PENDING; none SATISFIED.

## Changes since the prior closure (source `b585e5ebe` → `8cd783d8d`)

- 4 rows added, all ACTIVE EXECUTION UPSTREAM INTERFACE with a Deliverable target: DEP-02-01-029 (→ DEL-03-02), DEP-02-03-025 (→ DEL-03-02), DEP-02-03-026 (→ DEL-03-03), DEP-02-03-027 (→ DEL-01-04). 1 row retired (DEP-01-04-014, EXTERNAL). No row removed. 34 rows in DEL-04-01, DEL-04-02 and DEL-04-03 had `EvidenceQuote` re-quoted exactly (ASC-ISS-008; V12 F1); a further 16 rows had SourceRef, Statement, TargetName or Notes edits; the remaining rows in the 11 refreshed registers changed `LastSeen` only. No Direction, target or DependencyType changed on an existing arc row.
- Topology: 4 arcs added (198 → 202), 0 removed. All four lie inside SCC-002, taking its internal account from 76 rows / 62 arcs / 16 reciprocal pairs to 80 / 66 / 18. The other five SCCs' internal accounts are unchanged.

## Limits

- `MAX_CYCLES` 200 yields one representative cycle per SCC (6); `cycles_truncated` false does not mean exhaustive enumeration.
- The accepted-DAG comparison ran this time (the pointer is in SPEC §11.2 form since DAG-002's publication). It is advisory; the `project-dag` currency audit governs (`Decision_Log.md` item 5).
- This run does not re-certify the semantics of each row. It reports no acceptance, lifecycle change, dependency satisfaction or ready-work verdict.
