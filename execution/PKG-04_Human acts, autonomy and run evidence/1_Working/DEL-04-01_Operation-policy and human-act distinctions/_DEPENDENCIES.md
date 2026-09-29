# Dependencies: DEL-04-01 Operation-policy and human-act distinctions

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
- **ACTIVE:** 29 total — 11 ANCHOR, 18 EXECUTION. EXECUTION: 11 downstream policy handovers; 7 upstream inputs/constraints (OI-001, OI-002, OI-021, DECISION-4 governance layer, DEP-001, recorded person-set grant, performed-human-act evidence).
- **RETIRED:** 0. **EXTERNAL (ACTIVE):** 7. **UNKNOWN (ACTIVE):** 0. **DECLARED:** 0.

| Dependency | Class / type | Direction | Target | Status |
|---|---|---|---|---|
| DEP-04-01-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-04 | ACTIVE |
| DEP-04-01-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-074 | ACTIVE |
| DEP-04-01-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-079 | ACTIVE |
| DEP-04-01-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-082 | ACTIVE |
| DEP-04-01-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-179 | ACTIVE |
| DEP-04-01-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-180 | ACTIVE |
| DEP-04-01-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-181 | ACTIVE |
| DEP-04-01-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-182 | ACTIVE |
| DEP-04-01-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-235 | ACTIVE |
| DEP-04-01-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | ACTIVE |
| DEP-04-01-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | ACTIVE |
| DEP-04-01-012 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-01 | ACTIVE |
| DEP-04-01-013 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | ACTIVE |
| DEP-04-01-014 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-01 | ACTIVE |
| DEP-04-01-015 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 | ACTIVE |
| DEP-04-01-016 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | ACTIVE |
| DEP-04-01-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 | ACTIVE |
| DEP-04-01-018 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 | ACTIVE |
| DEP-04-01-019 | EXECUTION / PREREQUISITE | UPSTREAM | projects/chirality-app-v4/execution/_Decomposition/External_Dependencies.csv#DEP-001 | ACTIVE |
| DEP-04-01-020 | EXECUTION / PREREQUISITE | UPSTREAM | Person setting operation/consequence scope — recorded grant | ACTIVE |
| DEP-04-01-021 | EXECUTION / PREREQUISITE | UPSTREAM | Person performing the human act — attributable evidence for faithful-recording case | ACTIVE |
| DEP-04-01-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-02 | ACTIVE |
| DEP-04-01-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | ACTIVE |
| DEP-04-01-024 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | ACTIVE |
| DEP-04-01-025 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | ACTIVE |
| DEP-04-01-026 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | ACTIVE |
| DEP-04-01-027 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | ACTIVE |
| DEP-04-01-028 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 | ACTIVE |
| DEP-04-01-029 | EXECUTION / CONSTRAINT | UPSTREAM | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | ACTIVE |

## Lifecycle Summary

- Register lifecycle: ACTIVE 29; RETIRED 0.
- Closure states (ACTIVE rows): NOT_APPLICABLE 11, TBD 18. No execution dependency is marked SATISFIED by this extraction.

## Run Notes

- Run APP-V4-BASIS-ALIGN-20260928, node DX-1 (Claude Code Agent subagent, Type 2 TASK; no delegation). Basis commit 557716cf7. Parameters: SCOPE DEL-04-01; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; DOC_ROLE_MAP DEFAULT; ARCHITECTURE_BASIS_POLICY NONE.
- SOURCE_DOCS explicit: ScopeOfWork.md only (run BRIEFS.md DX shared override). ANCHOR_DOC ScopeOfWork.md; EXECUTION_DOC_ORDER ScopeOfWork.md. Design/ DRAFT files are not extraction sources. ANCHOR pass completed before the EXECUTION pass.
- RUN_ROOT: projects/chirality-app-v4/execution. DECOMPOSITION_PATH: projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md (available; brief override). Companion Deliverables.csv, ScopeLedger.csv and Objectives.csv in that folder were used for ID and label resolution; the scope, objective, package and deliverable-name rows used here are identical to the GROUP3-20260928T001055Z snapshot, so anchor TargetLocation values keep the snapshot paths that the SoW cites as basis B. Open_Issues.csv was read only to resolve cited OI identities.
- Source ScopeOfWork.md SHA256 before and after: ac043e54e396f9155e3d1b02d61ca7333350a812c7db3d5bb26c80d6fc3bb875 (unchanged: True). No source, _REFERENCES.md, _STATUS.md, Design, decomposition or _DAG file was modified.
- Guard (BRIEFS.md DX): pointers in DEL-05-01 TBD-003, DEL-05-02 TBD-003 and DEL-09-09 CLM-004 to the DEL-09-06 relay file are coordination routes, not inputs; not applicable to this register, which has no DEL-09-06 row.
- Run record: _run_records/dependency-extract-20260929.md (read identities and read order, validator output, output hashes). Return: run folder DX/DX-1_DEL-04-01.md (comparison with the DAG_PREP expectations).
- Declared mirroring: added 0; refreshed 0; retired 0; skipped 2 placeholder entries ("None declared at initial setup."). Human-owned sections byte-identical.
- UPDATE result: 8 rows added (DEP-04-01-022..029), 2 refreshed in place (017, 018), 0 retired, 19 unchanged apart from LastSeen.
- Added: six DOWNSTREAM HANDOVER rows to DEL-03-02, DEL-03-03, DEL-03-04, DEL-05-01, DEL-05-02 and DEL-09-09 from the CLM-002 supply sentence added under SCA-V4-001. The prior run excluded DEL-05-01/DEL-05-02 because only ownership/exclusion text existed; the revised source now states a positive supply. Typed HANDOVER with RequiredMaturity INITIALIZED for consistency with 012..016 (the threshold is local-contract only).
- Added: UPSTREAM CONSTRAINT on OI-021 (operation-specific reserved-act additions; TBD-001, REQ-004, AC-004).
- Refreshed: 017 (OI-001) and 018 (OI-002) keep their targets; statements, evidence and TargetLocation now cite the first-increment rulings APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2/D3 named by the source. Current Open_Issues.csv still lists OI-001/OI-002 as OPEN (CLM-004: updated through their own route). SatisfactionStatus stays TBD; extraction does not assess closure.
- Added: UPSTREAM CONSTRAINT DEP-04-01-029 on the enforced-checkpoint governance layer (TBD-004; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 D4-1), as a claim gate on the same pattern as TBD-003/DEP-04-01-019. Provenance: the first extraction pass did not extract TBD-004 (read as a conditional later decision); the row was added in a second pass after the post-extraction coordinator comparison had been read, on the ground of the TBD-003 precedent in this register. Disclosed so the reviewer can weigh it.
- Not extracted: AX-005 revision provenance and the REQ-002 current-docs citations (source citations, not edges).
- Checks: validate_dependencies_schema.py VALID (29 columns, 29 rows); validate_enum.py 21/21 used values VALID; validate_id_format.sh 56/56 IDs VALID. Local checks: unique DependencyIDs and semantic keys, DEP-04-01- prefix, own FromDeliverableID, one ACTIVE parent anchor, target-ID placement, every ACTIVE EvidenceQuote verbatim in the source (markdown emphasis/code marks ignored) and at most 30 words, no placeholder SourceRef. Optional validate_decomposition_registers.py not run (brief names only the three validators).
- Structural warnings: none (one IMPLEMENTS_NODE parent).

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:25:20Z — TASK dependency-extract; UPDATE / CONSERVATIVE; decomposition projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md available; ACTIVE 21 (ANCHOR 11 / EXECUTION 10), RETIRED 0; structural warnings none; external/point-of-need inputs remain unassessed.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-001); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +8 / refreshed 2 / retired 0; ACTIVE 29 (ANCHOR 11 / EXECUTION 18), RETIRED 0; warnings none.
