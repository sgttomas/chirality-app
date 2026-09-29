# Dependencies: DEL-02-02 Workflow-making workspace and registration

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
- **ACTIVE:** 18 total — 11 ANCHOR, 7 EXECUTION. EXECUTION: 6 upstream deliverable inputs (DEL-01-03, DEL-01-04, DEL-02-01, DEL-02-03, DEL-04-01, DEL-04-03) and 1 downstream handover (DEL-09-02).
- **RETIRED:** 1. **EXTERNAL (ACTIVE):** 0. **UNKNOWN (ACTIVE):** 0. **DECLARED:** 0.

| Dependency | Class / type | Direction | Target | Status |
|---|---|---|---|---|
| DEP-02-02-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-02 | ACTIVE |
| DEP-02-02-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-002 | ACTIVE |
| DEP-02-02-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-046 | ACTIVE |
| DEP-02-02-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-047 | ACTIVE |
| DEP-02-02-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-048 | ACTIVE |
| DEP-02-02-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-049 | ACTIVE |
| DEP-02-02-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-050 | ACTIVE |
| DEP-02-02-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-127 | ACTIVE |
| DEP-02-02-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | ACTIVE |
| DEP-02-02-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | ACTIVE |
| DEP-02-02-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-003 | ACTIVE |
| DEP-02-02-012 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-03 | ACTIVE |
| DEP-02-02-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-04 | ACTIVE |
| DEP-02-02-014 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | ACTIVE |
| DEP-02-02-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | ACTIVE |
| DEP-02-02-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | ACTIVE |
| DEP-02-02-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | ACTIVE |
| DEP-02-02-018 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | ACTIVE |
| DEP-02-02-019 | EXECUTION / CONSTRAINT | UPSTREAM | Person performing workflow review and explicit registration | RETIRED |

## Lifecycle Summary

- Register lifecycle: ACTIVE 18; RETIRED 1.
- Closure states (ACTIVE rows): NOT_APPLICABLE 11, TBD 7. No execution dependency is marked SATISFIED by this extraction.

## Run Notes

- Run APP-V4-BASIS-ALIGN-20260928, node DX-1 (Claude Code Agent subagent, Type 2 TASK; no delegation). Basis commit 557716cf7. Parameters: SCOPE DEL-02-02; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; DOC_ROLE_MAP DEFAULT; ARCHITECTURE_BASIS_POLICY NONE.
- SOURCE_DOCS explicit: ScopeOfWork.md only (run BRIEFS.md DX shared override). ANCHOR_DOC ScopeOfWork.md; EXECUTION_DOC_ORDER ScopeOfWork.md. Design/ DRAFT files are not extraction sources. ANCHOR pass completed before the EXECUTION pass.
- RUN_ROOT: projects/chirality-app-v4/execution. DECOMPOSITION_PATH: projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md (available; brief override). Companion Deliverables.csv, ScopeLedger.csv and Objectives.csv in that folder were used for ID and label resolution; the scope, objective, package and deliverable-name rows used here are identical to the GROUP3-20260928T001055Z snapshot, so anchor TargetLocation values keep the snapshot paths that the SoW cites as basis B. Open_Issues.csv was read only to resolve cited OI identities.
- Source ScopeOfWork.md SHA256 before and after: b0a1a8a4aa6f53057c8db4bb33c65c5e697f45ae509088a570a70ff8cee295ec (unchanged: True). No source, _REFERENCES.md, _STATUS.md, Design, decomposition or _DAG file was modified.
- Guard (BRIEFS.md DX): pointers in DEL-05-01 TBD-003, DEL-05-02 TBD-003 and DEL-09-09 CLM-004 to the DEL-09-06 relay file are coordination routes, not inputs; not applicable to this register, which has no DEL-09-06 row.
- Run record: _run_records/dependency-extract-20260929.md (read identities and read order, validator output, output hashes). Return: run folder DX/DX-1_DEL-02-02.md (comparison with the DAG_PREP expectations).
- Declared mirroring: added 0; refreshed 0; retired 0; skipped 2 placeholder entries ("None declared at initial setup."). Human-owned sections byte-identical.
- Source status: ScopeOfWork.md is unchanged since the prior extraction (same SHA256 as that run recorded; not among the 16 SoWs revised under SCA-V4-001). The full source was re-read and every row re-checked against it.
- UPDATE result: 0 rows added, 0 refreshed, 0 retired this run; 18 ACTIVE rows re-observed (LastSeen only). DEP-02-02-019 stays RETIRED: the source still states the review/registration rule as runtime product behavior (REQ-002), not a production input, so the prior repair stands.
- Observation (not acted on): TBD-001 and TBD-002 still describe OI-001/OI-002 and the OI-012 pin as open, while revised sibling SoWs record APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2/D3/D4. This register has no OI rows (the prior run treated them as points of need, not inputs); no change follows.
- Relation to run DAG preparation: this register is the supplier endpoint of the proposed arc DEL-09-06 -> DEL-02-02 (N-C1), whose row belongs to DEL-09-06. No row here is expected for it, and none was added (the source does not name DEL-09-06).
- Checks: validate_dependencies_schema.py VALID (29 columns, 19 rows); validate_enum.py 22/22 used values VALID; validate_id_format.sh 41/41 IDs VALID. Local checks: unique IDs/semantic keys, prefix, one parent, target placement, verbatim quotes of at most 30 words on ACTIVE rows, no placeholder SourceRef. Optional validate_decomposition_registers.py not run.
- Structural warnings: none (one IMPLEMENTS_NODE parent).

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27T21:05:38-06:00 — TASK dependency-extract UPDATE / CONSERVATIVE; accepted snapshot available; 19 ACTIVE (11 ANCHOR / 8 EXECUTION), 0 RETIRED; local checks PASS; no extraction integrity warnings.
- 2026-09-27T21:08:32-06:00 — Bounded source-extraction fidelity repair: DEP-02-02-019 RETIRED as runtime product behavior without a separately established production input; 18 ACTIVE (11 ANCHOR / 7 EXECUTION), 1 RETIRED. ID/history/source/declared sections preserved; affected checks PASS. No scope, policy or graph-cut decision.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (unchanged source); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +0 / refreshed 0 / retired 0; ACTIVE 18 (ANCHOR 11 / EXECUTION 7), RETIRED 1; warnings none.
