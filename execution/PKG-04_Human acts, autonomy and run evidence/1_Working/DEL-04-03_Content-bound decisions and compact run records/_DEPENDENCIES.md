# Dependencies: DEL-04-03 Content-bound decisions and compact run records

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
- **ACTIVE:** 33 total — 10 ANCHOR, 23 EXECUTION. EXECUTION: 8 upstream deliverable inputs; 6 downstream deliverable consumers (DEL-04-02, DEL-09-11, DEL-05-01, DEL-05-02, DEL-09-06, DEL-09-09); 3 package consumers (PKG-02, PKG-03, PKG-06); 6 external inputs/outputs/constraints (host-run recording, DEP-001, performed-act evidence, OI-001/OI-002 rulings, OI-013/OI-014, OI-021).
- **RETIRED:** 0. **EXTERNAL (ACTIVE):** 6. **UNKNOWN (ACTIVE):** 0. **DECLARED:** 0.

| Dependency | Class / type | Direction | Target | Status |
|---|---|---|---|---|
| DEP-04-03-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-04 | ACTIVE |
| DEP-04-03-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-092 | ACTIVE |
| DEP-04-03-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-093 | ACTIVE |
| DEP-04-03-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-094 | ACTIVE |
| DEP-04-03-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-095 | ACTIVE |
| DEP-04-03-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-096 | ACTIVE |
| DEP-04-03-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-143 | ACTIVE |
| DEP-04-03-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-186 | ACTIVE |
| DEP-04-03-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | ACTIVE |
| DEP-04-03-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | ACTIVE |
| DEP-04-03-011 | EXECUTION / INTERFACE | DOWNSTREAM | PKG-02 | ACTIVE |
| DEP-04-03-012 | EXECUTION / INTERFACE | DOWNSTREAM | PKG-03 | ACTIVE |
| DEP-04-03-013 | EXECUTION / INTERFACE | DOWNSTREAM | PKG-06 | ACTIVE |
| DEP-04-03-014 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 | ACTIVE |
| DEP-04-03-015 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-11 | ACTIVE |
| DEP-04-03-016 | EXECUTION / INTERFACE | DOWNSTREAM | Responsible host implementation owner — host-agent run recording | ACTIVE |
| DEP-04-03-017 | EXECUTION / INTERFACE | UPSTREAM | DEP-001 | ACTIVE |
| DEP-04-03-018 | EXECUTION / INTERFACE | UPSTREAM | Supplied evidence of an actually performed human act | ACTIVE |
| DEP-04-03-019 | EXECUTION / CONSTRAINT | UPSTREAM | Owner with affected App/SWB contract owners — OI-001/OI-002 rulings for the first increment (APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2/D3), carried by App DEL-04-01 | ACTIVE |
| DEP-04-03-020 | EXECUTION / CONSTRAINT | UPSTREAM | Shared contract, SWB implementation and App/shared contract owners — affected implementation allocation | ACTIVE |
| DEP-04-03-021 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | ACTIVE |
| DEP-04-03-022 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | ACTIVE |
| DEP-04-03-023 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | ACTIVE |
| DEP-04-03-024 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | ACTIVE |
| DEP-04-03-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | ACTIVE |
| DEP-04-03-026 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-03 | ACTIVE |
| DEP-04-03-027 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | ACTIVE |
| DEP-04-03-028 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 | ACTIVE |
| DEP-04-03-029 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-05-01 | ACTIVE |
| DEP-04-03-030 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-05-02 | ACTIVE |
| DEP-04-03-031 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-09-06 | ACTIVE |
| DEP-04-03-032 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-09-09 | ACTIVE |
| DEP-04-03-033 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 | ACTIVE |

## Lifecycle Summary

- Register lifecycle: ACTIVE 33; RETIRED 0.
- Closure states (ACTIVE rows): NOT_APPLICABLE 10, PENDING 23. No execution dependency is marked SATISFIED by this extraction.

## Run Notes

- Run APP-V4-BASIS-ALIGN-20260928, node DX-1 (Claude Code Agent subagent, Type 2 TASK; no delegation). Basis commit 557716cf7. Parameters: SCOPE DEL-04-03; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; DOC_ROLE_MAP DEFAULT; ARCHITECTURE_BASIS_POLICY NONE.
- SOURCE_DOCS explicit: ScopeOfWork.md only (run BRIEFS.md DX shared override). ANCHOR_DOC ScopeOfWork.md; EXECUTION_DOC_ORDER ScopeOfWork.md. Design/ DRAFT files are not extraction sources. ANCHOR pass completed before the EXECUTION pass.
- RUN_ROOT: projects/chirality-app-v4/execution. DECOMPOSITION_PATH: projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md (available; brief override). Companion Deliverables.csv, ScopeLedger.csv and Objectives.csv in that folder were used for ID and label resolution; the scope, objective, package and deliverable-name rows used here are identical to the GROUP3-20260928T001055Z snapshot, so anchor TargetLocation values keep the snapshot paths that the SoW cites as basis B. Open_Issues.csv was read only to resolve cited OI identities.
- Source ScopeOfWork.md SHA256 before and after: ceecddbb67a86f744b413bb08b08c27017a82ebee8500f7600faf8d880fbaa47 (unchanged: True). No source, _REFERENCES.md, _STATUS.md, Design, decomposition or _DAG file was modified.
- Guard (BRIEFS.md DX): pointers in DEL-05-01 TBD-003, DEL-05-02 TBD-003 and DEL-09-09 CLM-004 to the DEL-09-06 relay file are coordination routes, not inputs; not applicable to this register, which has no DEL-09-06 row.
- Run record: _run_records/dependency-extract-20260929.md (read identities and read order, validator output, output hashes). Return: run folder DX/DX-1_DEL-04-03.md (comparison with the DAG_PREP expectations).
- Declared mirroring: added 0; refreshed 0; retired 0; skipped 2 placeholder entries ("None declared at initial setup."). Human-owned sections byte-identical.
- UPDATE result: 13 rows added (DEP-04-03-021..033), 2 refreshed in place (019 content; 020 SourceRef line number only), 0 retired, 18 unchanged apart from LastSeen.
- Added from CLM-004 (revised under SCA-V4-001): UPSTREAM INTERFACE from DEL-04-01 (act kinds and classes), DEL-04-02 (settings-in), DEL-03-01 (subject content identities, method designations), DEL-03-02 (outcomes, change-item content identities, receipt links), DEL-02-03 (checkpoint arrival, act and lapse events; compatibility reports; hold events retained for the governance phase), DEL-03-03 (external dispatch entries), DEL-01-01 (observed supplier facts) and DEL-05-01 (network-destination events; DECISION-5).
- Added from REQ-005 (revised): DOWNSTREAM INTERFACE record-meaning consumers DEL-05-01, DEL-05-02, DEL-09-06 and DEL-09-09, typed as the existing package consumer rows 011..013. DEL-04-02 and DEL-05-01 each appear in both directions for different content (separate stated interfaces). Package rows 011..013 are unchanged because their CLM-004 sentence is unchanged.
- Added: UPSTREAM CONSTRAINT on OI-021 (TBD-001 now leaves only the operation-specific additions open). Refreshed: 019 now cites the OI-001/OI-002 first-increment rulings (APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2/D3) that TBD-001 records; SatisfactionStatus unchanged. Current Open_Issues.csv still lists OI-001/OI-002 as OPEN.
- Not extracted: no row makes DEL-03-02 or DEL-03-03 a consumer of this deliverable (the source names none). CLM-002/REQ-002 per-turn model destination and network-destination content is covered by the DEL-01-01 and DEL-05-01 input rows. REQ-006 ownership exclusions, source keys and AX-004 provenance create no edges.
- Checks: validate_dependencies_schema.py VALID (29 columns, 33 rows); validate_enum.py 22/22 used values VALID; validate_id_format.sh 62/62 IDs VALID. Local checks: unique IDs/semantic keys, prefix, one parent, target placement, verbatim quotes of at most 30 words (markdown emphasis/code marks ignored), no placeholder SourceRef; SourceRef line numbers re-checked against the revised source. Optional validate_decomposition_registers.py not run.
- Structural warnings: none (one IMPLEMENTS_NODE parent).

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:26:48+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted Group3 decomposition resolved at `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. ACTIVE 20 (ANCHOR 10, EXECUTION 10); no integrity warnings; conditional/external input limitations retained.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-001); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +13 / refreshed 2 / retired 0; ACTIVE 33 (ANCHOR 10 / EXECUTION 23), RETIRED 0; warnings none.
