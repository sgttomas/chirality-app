# Dependencies: DEL-01-01 Stock Codex hosting and supplier contract

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
- **ACTIVE:** 24 total — 15 ANCHOR, 9 EXECUTION. EXECUTION: 5 downstream supplier-boundary handovers (DEL-01-02..06), 1 conditional upstream evidence input (DEL-01-05), 3 external decisions/inputs (OI-008, OI-012, DEP-005).
- **RETIRED:** 0. **EXTERNAL (ACTIVE):** 3. **UNKNOWN (ACTIVE):** 0. **DECLARED:** 0.

| Dependency | Class / type | Direction | Target | Status |
|---|---|---|---|---|
| DEP-01-01-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-01 | ACTIVE |
| DEP-01-01-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-097 | ACTIVE |
| DEP-01-01-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-099 | ACTIVE |
| DEP-01-01-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-100 | ACTIVE |
| DEP-01-01-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-101 | ACTIVE |
| DEP-01-01-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-118 | ACTIVE |
| DEP-01-01-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-119 | ACTIVE |
| DEP-01-01-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-121 | ACTIVE |
| DEP-01-01-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-128 | ACTIVE |
| DEP-01-01-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-131 | ACTIVE |
| DEP-01-01-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-135 | ACTIVE |
| DEP-01-01-012 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-149 | ACTIVE |
| DEP-01-01-013 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | ACTIVE |
| DEP-01-01-014 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | ACTIVE |
| DEP-01-01-015 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | ACTIVE |
| DEP-01-01-016 | EXECUTION / CONSTRAINT | UPSTREAM | chirality-app-v4:OI-008 | ACTIVE |
| DEP-01-01-017 | EXECUTION / CONSTRAINT | UPSTREAM | chirality-app-v4:OI-012 | ACTIVE |
| DEP-01-01-018 | EXECUTION / PREREQUISITE | UPSTREAM | chirality-app-v4:DEP-005 | ACTIVE |
| DEP-01-01-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-02 | ACTIVE |
| DEP-01-01-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-03 | ACTIVE |
| DEP-01-01-021 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-04 | ACTIVE |
| DEP-01-01-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-05 | ACTIVE |
| DEP-01-01-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-06 | ACTIVE |
| DEP-01-01-024 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-05 | ACTIVE |

## Lifecycle Summary

- Register lifecycle: ACTIVE 24; RETIRED 0.
- Closure states (ACTIVE rows): NOT_APPLICABLE 15, TBD 9. No execution dependency is marked SATISFIED by this extraction.

## Run Notes

- Run APP-V4-BASIS-ALIGN-20260928, node DX-1 (Claude Code Agent subagent, Type 2 TASK; no delegation). Basis commit 557716cf7. Parameters: SCOPE DEL-01-01; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; DOC_ROLE_MAP DEFAULT; ARCHITECTURE_BASIS_POLICY NONE.
- SOURCE_DOCS explicit: ScopeOfWork.md only (run BRIEFS.md DX shared override). ANCHOR_DOC ScopeOfWork.md; EXECUTION_DOC_ORDER ScopeOfWork.md. Design/ DRAFT files are not extraction sources. ANCHOR pass completed before the EXECUTION pass.
- RUN_ROOT: projects/chirality-app-v4/execution. DECOMPOSITION_PATH: projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md (available; brief override). Companion Deliverables.csv, ScopeLedger.csv and Objectives.csv in that folder were used for ID and label resolution; the scope, objective, package and deliverable-name rows used here are identical to the GROUP3-20260928T001055Z snapshot, so anchor TargetLocation values keep the snapshot paths that the SoW cites as basis B. Open_Issues.csv was read only to resolve cited OI identities.
- Source ScopeOfWork.md SHA256 before and after: f65dc666708dc06fbff046cf293ff529024ad9487829d2c105b3678c86a8acc9 (unchanged: True). No source, _REFERENCES.md, _STATUS.md, Design, decomposition or _DAG file was modified.
- Guard (BRIEFS.md DX): pointers in DEL-05-01 TBD-003, DEL-05-02 TBD-003 and DEL-09-09 CLM-004 to the DEL-09-06 relay file are coordination routes, not inputs; not applicable to this register, which has no DEL-09-06 row.
- Run record: _run_records/dependency-extract-20260929.md (read identities and read order, validator output, output hashes). Return: run folder DX/DX-1_DEL-01-01.md (comparison with the DAG_PREP expectations).
- Declared mirroring: added 0; refreshed 0; retired 0; skipped 2 placeholder entries ("None declared at initial setup."). Human-owned sections byte-identical.
- UPDATE result: 0 rows added, 2 refreshed in place (017, 018), 0 retired, 22 unchanged apart from LastSeen.
- SCA-V4-001 revised CLM-003, REQ-006 and TBD-002 only (owner decision APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D4 selected Codex 0.158.0 as the definition/generation pin). Refreshed 017 (OI-012) to the remaining decisions: re-examination before implementation and the qualification pin; the prior quote no longer appears. Refreshed 018 (DEP-005) Statement/SourceRef/Notes so they no longer say that no pin is adopted; its CLM-003 quote is unchanged. Provenance: the 018 Statement staleness was identified during the post-extraction coordinator comparison and repaired on its source merits in this run. SatisfactionStatus unchanged on both.
- Not extracted: the D4 selection as a separate input row (carried in 017/018 Statement and Notes); Design/PIN_SPIKE_0.158.0.md, which TBD-002 cites as where observations are recorded (a record location, not a required input; Design files are not extraction sources); AX-005 revision provenance.
- Checks: validate_dependencies_schema.py VALID (29 columns, 24 rows); validate_enum.py 22/22 used values VALID; validate_id_format.sh 45/45 IDs VALID. Local checks: unique IDs/semantic keys, prefix, one parent, target placement, verbatim quotes of at most 30 words (markdown emphasis/code marks ignored), no placeholder SourceRef. Optional validate_decomposition_registers.py not run.
- Structural warnings: none (one IMPLEMENTS_NODE parent).

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:06:28+00:00 — TASK `/root/renewal_research_strategy/dep_del_01_01`, UPDATE / CONSERVATIVE; explicit accepted decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` resolved; no integrity warnings; ACTIVE 24 (ANCHOR 15, EXECUTION 9); source unchanged; local checks PASS; fulfilment unclaimed.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-001); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +0 / refreshed 2 / retired 0; ACTIVE 24 (ANCHOR 15 / EXECUTION 9), RETIRED 0; warnings none.
