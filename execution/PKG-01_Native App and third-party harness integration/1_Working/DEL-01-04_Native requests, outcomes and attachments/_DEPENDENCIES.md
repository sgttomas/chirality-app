# Dependencies: DEL-01-04 Native requests, outcomes and attachments

## Dependency Tracking Mode
- **Mode:** FULL_GRAPH
- **Register:** the declared sections of this file together with Dependencies.csv (schema v3.1) when present (docs/SPEC.md §5.3)
- **Notes:** `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`; no individual human-declared edge yet. Accepted interface descriptions are sources for later extraction, not declarations inferred by scaffolding.

---

## Declared Upstream (I need these before I can proceed)
- None declared at initial setup.

## Declared Downstream (These need me)
- None declared at initial setup.

---

## Extracted Dependency Register

- **Status:** EXTRACTED; canonical Dependencies.csv v3.1.
- **ACTIVE:** 19 total — 6 ANCHOR, 13 EXECUTION. EXECUTION: 5 upstream deliverable inputs (DEL-01-01, DEL-01-02, DEL-02-02, DEL-04-01, DEL-04-03) and 1 downstream handover (DEL-02-02); 7 external decisions/inputs (OI-001, OI-002, OI-008, OI-012, OI-014, DEP-005, performed-act case).
- **RETIRED:** 0. **EXTERNAL (ACTIVE):** 7. **UNKNOWN (ACTIVE):** 0. **DECLARED:** 0.

| Dependency | Class / type | Direction | Target | Status |
|---|---|---|---|---|
| DEP-01-04-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-01 | ACTIVE |
| DEP-01-04-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-005 | ACTIVE |
| DEP-01-04-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-014 | ACTIVE |
| DEP-01-04-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-129 | ACTIVE |
| DEP-01-04-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | ACTIVE |
| DEP-01-04-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | ACTIVE |
| DEP-01-04-007 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-01 | ACTIVE |
| DEP-01-04-008 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-02 | ACTIVE |
| DEP-01-04-009 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-02 | ACTIVE |
| DEP-01-04-010 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-02 | ACTIVE |
| DEP-01-04-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | ACTIVE |
| DEP-01-04-012 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | ACTIVE |
| DEP-01-04-013 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 | ACTIVE |
| DEP-01-04-014 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 | ACTIVE |
| DEP-01-04-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-008 | ACTIVE |
| DEP-01-04-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-012 | ACTIVE |
| DEP-01-04-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-014 | ACTIVE |
| DEP-01-04-018 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-005 | ACTIVE |
| DEP-01-04-019 | EXECUTION / PREREQUISITE | UPSTREAM | Person performing the positive human-act case and separate faithful recorder | ACTIVE |

## Lifecycle Summary

- Register lifecycle: ACTIVE 19; RETIRED 0.
- Closure states (ACTIVE rows): NOT_APPLICABLE 6, TBD 13. No execution dependency is marked SATISFIED by this extraction.

## Run Notes

- Run APP-V4-BASIS-ALIGN-20260928, node DX-1 (Claude Code Agent subagent, Type 2 TASK; no delegation). Basis commit 557716cf7. Parameters: SCOPE DEL-01-04; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; DOC_ROLE_MAP DEFAULT; ARCHITECTURE_BASIS_POLICY NONE.
- SOURCE_DOCS explicit: ScopeOfWork.md only (run BRIEFS.md DX shared override). ANCHOR_DOC ScopeOfWork.md; EXECUTION_DOC_ORDER ScopeOfWork.md. Design/ DRAFT files are not extraction sources. ANCHOR pass completed before the EXECUTION pass.
- RUN_ROOT: projects/chirality-app-v4/execution. DECOMPOSITION_PATH: projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md (available; brief override). Companion Deliverables.csv, ScopeLedger.csv and Objectives.csv in that folder were used for ID and label resolution; the scope, objective, package and deliverable-name rows used here are identical to the GROUP3-20260928T001055Z snapshot, so anchor TargetLocation values keep the snapshot paths that the SoW cites as basis B. Open_Issues.csv was read only to resolve cited OI identities.
- Source ScopeOfWork.md SHA256 before and after: 7261a58f93d4531ca080c16d7fe088818871c3444085bade2eb2350ace94e60a (unchanged: True). No source, _REFERENCES.md, _STATUS.md, Design, decomposition or _DAG file was modified.
- Guard (BRIEFS.md DX): pointers in DEL-05-01 TBD-003, DEL-05-02 TBD-003 and DEL-09-09 CLM-004 to the DEL-09-06 relay file are coordination routes, not inputs; not applicable to this register, which has no DEL-09-06 row.
- Run record: _run_records/dependency-extract-20260929.md (read identities and read order, validator output, output hashes). Return: run folder DX/DX-1_DEL-01-04.md (comparison with the DAG_PREP expectations).
- Declared mirroring: added 0; refreshed 0; retired 0; skipped 2 placeholder entries ("None declared at initial setup."). Human-owned sections byte-identical.
- Source status: ScopeOfWork.md is unchanged since the prior extraction (same SHA256 as that run recorded; not among the 16 SoWs revised under SCA-V4-001). The full source was re-read and every ACTIVE row re-checked against it.
- UPDATE result: 0 rows added, 0 refreshed, 0 retired; 19 rows re-observed (LastSeen only).
- Observation (not acted on): TBD-001, TBD-002 and TBD-004 still describe OI-001, OI-002 and OI-012 as open and unselected, while the revised sibling SoWs record APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2/D3/D4. Rows 013, 014 and 016 mirror this source as written. Any refresh needs a SoW revision through its own route first.
- Relation to run DAG preparation: this register is the supplier endpoint of the proposed arc DEL-02-03 -> DEL-01-04 (X-1), whose row belongs to DEL-02-03. No row here is expected for it, and none was added (no source sentence names DEL-02-03).
- Checks: validate_dependencies_schema.py VALID (29 columns, 19 rows); validate_enum.py 22/22 used values VALID; validate_id_format.sh 33/33 IDs VALID. Local checks: unique IDs/semantic keys, prefix, one parent, target placement, verbatim quotes of at most 30 words, no placeholder SourceRef. Optional validate_decomposition_registers.py not run.
- Structural warnings: none (one IMPLEMENTS_NODE parent).

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:14:57+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted GROUP3-20260928T001055Z canonical SOFTWARE_DECOMP.md available; warnings 0; ACTIVE 19 (ANCHOR 6 / EXECUTION 13), RETIRED 0; no lifecycle act.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (unchanged source); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +0 / refreshed 0 / retired 0; ACTIVE 19 (ANCHOR 6 / EXECUTION 13), RETIRED 0; warnings none.
