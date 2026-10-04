# Brief — scope closure audit, SCA-V4-003

Node CA of run `APP-V4-SCA003-20261002`, a Type 2 TASK (Claude Code
subagent dispatched by the HELP_HUMAN session; no delegation). Method:
`workflows/audit-scope-closure/` (`WORKFLOW.md`, `resources/contract.md`,
`resources/method.md`), bundled Root source. Model: SCA-V4-002's closure
audit `ScopeClosure_SCA-V4-002_2026-09-29_2233/` and that run's DISPATCH row
CA2. Evidence base: `HEAD` `90d3a5b6a7655e4b4829dd53b265c1b8c6e45181`
("DEL-01-03 TargetLocation made relative …; currency
CURRENT_WITH_EVIDENCE_DRIFT"), working tree clean at the start. Read-only
git; no network.

```
PURPOSE: Verify closure of scope change amendment
AMENDMENT_ID: SCA-V4-003
EXECUTION_ROOT: projects/chirality-app-v4/execution
SCOPE_CHANGE_ROOT: projects/chirality-app-v4/execution/_ScopeChange/
DECOMPOSITION_PATH: projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md (companion registers per Companion_Inventory.csv)
DECOMP_VARIANT: SOFTWARE
CONSTRAINTS:
  - Read-only on project state. Writes: this snapshot folder and _Evaluation/ScopeClosureAudit/_LATEST.md only.
  - Scratch: the session scratchpad, folder CA (accumulator outputs copied here).
NOTES:
  - Bind the 23 accepted actions to: the candidate application at fa16393978 (records 388fc730b9); the group-3 snapshot at c8ae213134 and H-1..H-3 at a44252d103; the 19 SoW REVISEs at 2d5e6845c5 (RV/RA.md, RV/RB.md); the 20 register UPDATEs at 0e3c55eec5 (DX/); the currency audit and DAG-004 candidate at 4ca22437f7; V25 at 6358ce132d; DECISION-3 at ad16b789ec; DAG-004 publication and CURRENT audit at c147bb3abe; the DEL-01-03 TargetLocation repair (FX) and CURRENT_WITH_EVIDENCE_DRIFT audit at HEAD.
  - Known open and expected: Coverage_Telemetry.json (STALE_REBUILD_REQUIRED) and the Design re-pins after the REVISEs.
```

**Concurrent writes observed.** During this run another writer (not this
node) added one uncommitted line to the `MEMORY.md` of each of the 20
register-named deliverables (an SCA-V4-003 receipt line). `MEMORY.md` is
not an amendment target, a register input or any file this audit relies
on; this node did not read it as evidence and did not touch it. Every
audited input is hashed in `INPUT_MANIFEST.sha256` and equals its blob at
`HEAD`.

Snapshot folder: `ScopeClosure_SCA-V4-003_2026-10-03_2028` (local time
20:28 MDT, 2026-10-03; the contract's
`ScopeClosure_{AMENDMENT_ID}_{YYYY-MM-DD}_{HHMM}` form).
