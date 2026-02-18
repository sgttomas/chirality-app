# Dependencies: DEL-05-02 Option - Yard Lighting (Per Light)

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** `Dependencies.csv` (7 rows)
- **Schema Version:** v3.1
- **Last Run:** 2026-02-17

### Summary

| Class | Count (ACTIVE) |
|---|---|
| ANCHOR | 2 |
| EXECUTION | 5 |
| **Total** | **7** |

### ANCHOR Rows

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-0502-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0501 | HIGH |
| DEP-0502-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-010 | HIGH |

### EXECUTION Rows

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-0502-003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-01 (Site Plan, Circulation, Parking & Operational Layout) | HIGH |
| DEP-0502-004 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-06 (Electrical Power, Lighting, IT-Telecom & PA) | HIGH |
| DEP-0502-005 | UPSTREAM | CONSTRAINT | DOCUMENT | RFP 2024_004 OSR (Appendix A) | HIGH |
| DEP-0502-006 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-07 (Commissioning, Training, Closeout & Warranty) | HIGH |
| DEP-0502-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-04 (Permitting, Inspections & AHJ Coordination) | MEDIUM |

## Run Notes

### Run: 2026-02-17

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Specification.md, Guidance.md, Procedure.md)
- ANCHOR_DOC: AUTO (resolved to: Datasheet.md -- contains `datasheet` keyword; has Identification table with Scope Coverage and Objective Support fields)
- EXECUTION_DOC_ORDER: AUTO (resolved to: Procedure.md, Specification.md, Guidance.md -- Procedure contains explicit prerequisites/upstream dependencies section)
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (available; used for anchor validation and target resolution)
- _REFERENCES.md: Present (used for document target location resolution)

**Defaults applied:**
- All source docs in deliverable folder scanned (excluding dependency artifacts and generated files)
- Datasheet.md selected as ANCHOR_DOC per heuristic (filename match + traceability fields present)
- Procedure.md prioritized as first EXECUTION_DOC due to explicit prerequisites section

**Anchor validation (decomposition lookup):**
- SOW-0501: Confirmed in scope ledger. Maps to PKG-005 / DEL-05-02_Optional-Yard-Lighting / OBJ-010. Statement: "Optional priced item: Yard lighting for Public Works yard (price per light incl. install); fence line approx. 100 m from nearest proposed structure."
- OBJ-010: Confirmed in objectives table. Statement: "Provide transparent, separable pricing for optional scope items."

**Target resolution (decomposition lookup):**
- DEL-03-01: Confirmed as DEL-03-01_Site-Plan-Circulation-and-Parking in PKG-003.
- DEL-02-06: Confirmed as DEL-02-06_Electrical-Lighting-IT-and-PA in PKG-002.
- DEL-01-07: Confirmed as DEL-01-07_Commissioning-Handover-and-Closeout in PKG-001.
- DEL-01-04: Confirmed as DEL-01-04_Permitting-and-Inspections-Coordination in PKG-001.

**Warnings:** None.

**Quality checks (all passed):**
- Required columns present: PASS
- CSV parseable: PASS
- DependencyID uniqueness: PASS (7 unique of 7)
- ACTIVE rows have EvidenceFile + SourceRef: PASS
- Enum values canonical: PASS
- Parent anchor count: 1 (PASS -- exactly one IMPLEMENTS_NODE)
- FromDeliverableID consistency: PASS (all rows = DEL-05-02)
- No obvious duplicates: PASS
- Counts consistent with _DEPENDENCIES.md: PASS

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Available (FINAL v1.0 Phase 7) | None | 2 | 5 | 7 |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 7 |
| RETIRED | 0 |

**Closure-state breakdown (ACTIVE rows):**

| SatisfactionStatus | Count |
|---|---|
| TBD | 7 |
