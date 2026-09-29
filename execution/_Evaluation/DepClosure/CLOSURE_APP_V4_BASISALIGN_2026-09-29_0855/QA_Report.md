# QA report

RUN_STATUS = WARNINGS. Analyzer COMPLETE, exit 0, subject FAIL. Coverage PASS.

## Inventory and coverage

- **Inventory source:** `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` (sha256 `bcdf6f2f…15eb`), resolved through `_LATEST_ACCEPTED.md` (unchanged since DAG-001). 41 units in 11 packages, 41 workspace folders, no unit without a folder, no folder without a row. No exemptions.
- **Registers:** 41/41 `Dependencies.csv` present, readable and schema-valid (v3.1); 41/41 carry one `IMPLEMENTS_NODE` anchor. 41 `_DEPENDENCIES.md` read (INCLUDE_DECLARED true): 0 declared-only entries, 0 disagreements, 0 unread lines.
- **Evidence cells:** 822/822 populated. `validate_decomposition_registers.py` (SCH, EVQ, DRB, strict): 0 errors, 0 warnings; every EvidenceFile resolves deliverable-relative.
- **Rows:** 822 = 355 ANCHOR + 467 EXECUTION. EXECUTION: 462 ACTIVE, 5 RETIRED (DEP-02-02-019 as before; DEP-02-03-015, -016, DEP-05-02-014, -015 retired by DX-2, all EXTERNAL, no arc effect). Active EXECUTION by target: 254 DELIVERABLE, 150 EXTERNAL, 26 DOCUMENT, 18 PACKAGE, 14 UNKNOWN. RequiredMaturity 247 INITIALIZED / 215 TBD; SatisfactionStatus 302 TBD / 160 PENDING; none SATISFIED.

## Changes since the prior closure (source `85dcc17c` → `b585e5ebe`)

- 63 rows added, all ACTIVE EXECUTION: 53 with a Deliverable target and 10 EXTERNAL. 52 existing rows had field edits (Statement, SourceRef, EvidenceQuote, Notes, TargetName/Location; four Status → RETIRED). No row removed. No Direction, target or DependencyType changed on an existing arc row.
- Topology: 37 arcs added (161 → 198), 0 removed. 23 new rows lie outside any SCC (15 new arcs plus 8 supplier-side or same-arc rows); 30 new rows fall inside SCC-002 (22 new arcs), taking its internal account from 46 rows / 40 arcs to 76 / 62. The other five SCCs' internal accounts are unchanged.

## Limits

- `MAX_CYCLES` 200 yields one representative cycle per SCC (6); `cycles_truncated` false does not mean exhaustive enumeration.
- The accepted-DAG comparison could not run (pointer form); see `Decision_Log.md` item 5 and the currency audit.
- This run does not re-certify the semantics of each row. It reports no acceptance, lifecycle change, dependency satisfaction or ready-work verdict.
