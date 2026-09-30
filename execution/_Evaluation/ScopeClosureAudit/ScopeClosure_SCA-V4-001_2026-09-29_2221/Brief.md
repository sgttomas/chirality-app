# Brief — scope closure audit of SCA-V4-001 (superseding snapshot)

```
PURPOSE: Verify closure of scope change amendment
AMENDMENT_ID: SCA-V4-001
EXECUTION_ROOT: projects/chirality-app-v4/execution
SCOPE_CHANGE_ROOT: projects/chirality-app-v4/execution/_ScopeChange/
DECOMPOSITION_PATH: projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md
DECOMP_VARIANT: SOFTWARE
CONSTRAINTS:
  - Read-only on project state. Write only this snapshot and ScopeClosureAudit/_LATEST.md.
  - Git read-only; no network.
  - Scratch: session scratchpad CA3/.
NOTES:
  - Run APP-V4-SCA002-20260929, node CA3 (Type 2 TASK, Claude Code subagent; no delegation),
    dispatched by the HELP_HUMAN integrator. This is a superseding snapshot of
    ScopeClosure_SCA-V4-001_2026-09-29_1222 (node CA1, verdict OPEN, ASC-ISS-001
    provisional CRITICAL). See SUPERSESSION_NOTE.md.
  - Changed inputs since CA1: SCA-V4-002 accepted (DECISION-2, DECISION-3), its
    Supersession_Delta adding 17 DL-SCA-V4-001 rows and D-014 (owner ruling on
    ASC-ISS-001, option a); the SCA-V4-001 effective-state record (ASC-ISS-003);
    the reading-rule notes (ASC-ISS-006), the DEL-04-01 qualifier (ASC-ISS-002),
    the DEP-09-07-016 restatement (ASC-ISS-007), the 34 re-quoted cells
    (ASC-ISS-008); DAG-003 accepted (DECISION-4) and published in parallel.
  - Coverage_Telemetry (ASC-ISS-004) and the Design re-pins (ASC-ISS-005) remain
    owner-deferred.
```

## Basis

| Item | Value |
|---|---|
| Repository commit | `a254be16060692633600bcb5c5aab925f4d26926` (working tree clean apart from this snapshot). The node started at `b99df0989`; commit `a254be160` ("DAG-003 published and current") landed during the run and is the state bound here |
| Workflow | `workflows/audit-scope-closure` (WORKFLOW.md, resources/contract.md, resources/method.md; hashes in `INPUT_MANIFEST.sha256`) |
| Amendment snapshot | `_ScopeChange/SCA-V4-001_2026-09-28_2155/` (accepted predecessor named by `_ScopeChange/_LATEST.md`, which now names `SCA-V4-002_2026-09-29_1901`) |
| Accepted register | `Amendment_Actions.csv`, SHA-256 `069645d979efa1e0a20f50194acca08afa8715ce647f36ad507c5bf2b76f14d2`, bound in `checkpoint_snapshots/SCA-V4-001_GROUP-2_2026-09-28/ACCEPTED_MANIFEST.csv` (role `action register`); hash verified again |
| Variant detection | SOFTWARE (`SOFTWARE_DECOMP.md`; Handoff_State "KTY remediation … do not apply (SOFTWARE)") |
| Superseded snapshot | `ScopeClosure_SCA-V4-001_2026-09-29_1222/` (bytes unchanged; hashes in SUPERSESSION_NOTE.md) |

## Snapshot custody

This snapshot folder was created at 2026-09-29 22:21 (-0600) by node CA3 in one
uninterrupted pass. Nothing else was written outside it except
`ScopeClosureAudit/_LATEST.md`.
