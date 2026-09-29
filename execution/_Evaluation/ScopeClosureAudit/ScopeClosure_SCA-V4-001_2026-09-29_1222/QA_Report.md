# QA — Scope Closure Audit SCA-V4-001

## Coverage

| Check | Checked | Detail |
|---|---|---|
| Actions | 47 of 47 | Byte-for-byte reconstruction from the accepted packet: 5 Markdown targets, 16 SoWs (162 pairs), 21 Part B rows, 11 B7 mirrors, 144 `Consolidated_Coverage.csv` rows |
| Downstream reruns | 6 of 6 recommended | 4 COMPLETED, 2 DEFERRED_BY_HUMAN. The SETUP_LOG line was also checked |
| `Dependencies.csv` files scanned for orphans | 41 | 822 rows, through `analyze_dep_closure.py` |
| Deliverable `_CONTEXT.md` files checked | 41 | 16 affected; the other 25 checked for mirror drift. All `_STATUS.md` files compared with `67a2fac4b` |
| Supersession | 22 YES rows and 11 delta rows | Accumulator check mode |
| KTY remediation manifest rows | 0 | NOT_APPLICABLE (SOFTWARE) |
| `.Archive/` scanner exclusion surfaces | 0 | None present |
| Design files scanned for stale pins | 37 | 17 are stale |

## Tool runs

All tools ran read-only against the working tree at `102f09c1a`. Outputs
went to this snapshot or to the session scratchpad.

**Registered tools:**
- `tools/coordination/accumulate_supersession_map.py` (`d967144d…`): exit 0,
  0 findings. Output in this snapshot.
- `tools/coordination/analyze_dep_closure.py` (`2b8de3cb…`): exit 0,
  `NO_DEPARTURE_FOUND`. Stdout, in the scratchpad (`d56753aa…`), is identical
  to the recorded currency evidence.
- `tools/coordination/audit_dag.py --dag-dir …/_DAG/DAG-002 --canonical --strict`:
  exit 0.
- `tools/scope_of_work/validate_scope_of_work.py`: 16/16 PASS.
- `tools/scope_of_work/check_boundary_owner_resolution.py`: 16/16 exit 0.
- `shasum -a 256 -c`:
  - DAG-002 `SOURCE_MANIFEST.sha256`: 130/130;
  - DAG-002 `MANIFEST.sha256`: 37/37;
  - DAG-001 `MANIFEST.sha256`: 61/61;
  - the group-1, group-2 and group-3 `ACCEPTED_MANIFEST.csv` rows: see the
    report's "Manifests" note.

**Own scripts,** in the scratchpad `CA1/`:
- `verify_pass1.py` (`3291e34f…`);
- `verify_partB.py` (`03aeb822…`);
- inline Python checks for the DX and RV hash bindings, context mirrors,
  lifecycle, Design pins, supersession texts and coverage recompute.

## Limitations

- **Scripts are not in the repository.** The CA1 scripts stay in the session
  scratchpad, because the contract's snapshot layout has no evidence folder.
  Their hashes are above, and their method is stated in the report, so the
  checks can be reproduced.
- **Handoff records.** The accepted Handoff_State was taken as the latest
  applicable record, because no later closeout or effective-state record
  exists under `_ScopeChange/`.
- **Two items rest on interpretation:**
  - the Design re-pin deferral is inferred from the owner's acceptance of the
    group-3 Handoff_State (ASC-ISS-005);
  - the DEL-04-01 phrase (ASC-ISS-002) is a semantic judgement.

  Both are marked UNKNOWN.
- **ASC-ISS-001 severity** is the method's table value. It conflicts with an
  owner-accepted record and is flagged for human triage, not resolved here.
- **Audit-decomp scope.** It covers the seven baseline packages only (O-20,
  accepted). PKG-06, 07, 10 and 11 had no amendment action; DEL-10-03's
  residual is recorded (ASC-ISS-007).
- **Snapshot custody.** The run was interrupted once, by a transient API
  connection error. It was resumed in the same never-committed snapshot
  folder; see Brief.md "Snapshot custody".

## Self-Assessment

- All passes completed: yes. Passes 0–6 were run; Pass 7 is NOT_APPLICABLE
  with the reason recorded.
- All findings have evidence: yes. Each issue-log row has an `EvidenceFile`
  and a `SourceRef`.
- No silent resolutions: yes. ASC-ISS-001 reports both the method and
  contract side and the accepted-record side. The understated handoff records
  are reported (ASC-ISS-003), not edited.
- Read-only on project state: yes. Only this snapshot and
  `ScopeClosureAudit/_LATEST.md` were written.
