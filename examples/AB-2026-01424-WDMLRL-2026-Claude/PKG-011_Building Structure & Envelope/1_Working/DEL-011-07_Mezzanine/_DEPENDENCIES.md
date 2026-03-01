# Dependencies: DEL-011-07 Mezzanine Structure & Stairs

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- DEL-011-01 Superstructure -- Main structural frame must support mezzanine loads
- DEL-011-02 Steel Embedments -- Mezzanine attachment points may use floor embedments
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- PKG-012 Interior Construction & Fit-Out -- Mezzanine flooring and interior finishes
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (18 rows, schema v3.1)
- **Last Run:** 2026-02-26
- **Summary:** 5 ANCHOR + 13 EXECUTION = 18 total ACTIVE rows

### ANCHOR Edges (5 rows)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-011-07-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-011 Building Structure & Envelope | HIGH |
| DEP-011-07-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0032 Mezzanine storage construction | HIGH |
| DEP-011-07-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0033 Load-bearing capability | HIGH |
| DEP-011-07-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0034 Stairs to mezzanine | HIGH |
| DEP-011-07-005 | TRACES_TO_REQUIREMENT | WBS_NODE | OBJ-001 Functional maintenance shop addition | HIGH |

### EXECUTION Edges (13 rows)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-011-07-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-011-01 Concrete Superstructure | HIGH | BLOCKING |
| DEP-011-07-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-011-02 Steel Plate Floor Embedments | HIGH | BLOCKING |
| DEP-011-07-008 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-05 Mezzanine Framing Details (IFC) | HIGH | BLOCKING |
| DEP-011-07-009 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-09 Stair Details (IFC) | HIGH | BLOCKING |
| DEP-011-07-010 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-10 Structural Calculation Package | MEDIUM | ADVISORY |
| DEP-011-07-011 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-12 Structural Specification | HIGH | BLOCKING |
| DEP-011-07-012 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-009-02 Building Permit | HIGH | BLOCKING |
| DEP-011-07-013 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-009-03 Safety Code Permits | HIGH | BLOCKING |
| DEP-011-07-014 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-019-04 Construction Quality Control Plan | MEDIUM | ADVISORY |
| DEP-011-07-015 | DOWNSTREAM | HANDOVER | PACKAGE | PKG-012 Interior Construction & Fit-Out | HIGH | BLOCKING |
| DEP-011-07-016 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-010-01 Foundation Construction | MEDIUM | ADVISORY |
| DEP-011-07-017 | UPSTREAM | CONSTRAINT | DOCUMENT | R-01 RFP (design requirements source) | HIGH | INFO |
| DEP-011-07-018 | UPSTREAM | CONSTRAINT | DOCUMENT | R-04 Appendix B Shop (conceptual drawing) | HIGH | INFO |

## Run Notes

### Run: 2026-02-26

- **Mode:** UPDATE
- **Strictness:** CONSERVATIVE
- **Consumer Context:** TASK_ESTIMATING
- **Decomposition Path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25) -- located and used successfully.
- **Source Documents Scanned:**
  - ANCHOR_DOC: `Datasheet.md` (selected by DOC_ROLE_MAP heuristic: contains "datasheet")
  - EXECUTION_DOCS (in order): `Procedure.md`, `Specification.md`, `Guidance.md`
- **_REFERENCES.md:** Read; used to resolve R-01 and R-04 document locations to `_Sources/`.
- **Defaults Applied:**
  - SOURCE_DOCS=AUTO (4 source documents identified; excluded `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_STATUS.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`)
  - DOC_ROLE_MAP=DEFAULT
  - ANCHOR_DOC=AUTO (selected `Datasheet.md`)
  - EXECUTION_DOC_ORDER=AUTO (selected `Procedure.md` first -- strongest prerequisite/workflow signal; then `Specification.md`, then `Guidance.md`)
- **Warnings:** None.
- **Integrity Checks:**
  - Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE row -- PASS
  - DependencyID uniqueness: all 18 IDs unique -- PASS
  - Required columns present: PASS
  - EvidenceFile + SourceRef for all ACTIVE rows: PASS
  - No legacy direction values: PASS
  - No duplicate extracted rows: PASS

### Extraction Notes

- Human-declared upstream dependencies (DEL-011-01, DEL-011-02) are corroborated by extracted evidence from Procedure.md and Guidance.md. Extracted rows carry richer detail (specific prerequisite conditions).
- Human-declared downstream dependency (PKG-012) is corroborated by extracted evidence. Scope boundary between structural deck and wearing surface is unresolved (CFT-011-07-02).
- DEP-011-07-016 (Foundation interface) is IMPLICIT -- derived from Guidance discussion of load path engineering coordination, not a direct prerequisite gate. Marked ASSUMPTION with MEDIUM confidence.
- DEP-011-07-010 (Calculation Package) is conditional ("if required by Safety Codes Officer"). Classified as INTERFACE rather than PREREQUISITE.
- Document dependencies (R-01 RFP, R-04 App B) are included as CONSTRAINT/DOCUMENT edges because they are contractually binding sources of design requirements, not merely informational references.

## Run History

| Run Date | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Rows |
|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Located (R1) | None | 18 (5A + 13E) |

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE** | 18 |
| **RETIRED** | 0 |
| **Total** | 18 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 5 | 0 |
| EXECUTION | 13 | 0 |

### SatisfactionStatus Breakdown (ACTIVE rows)

| Status | Count |
|---|---|
| PENDING | 13 |
| NOT_APPLICABLE | 5 |

### EstimateImpactClass Breakdown (ACTIVE EXECUTION rows)

| Class | Count |
|---|---|
| BLOCKING | 8 |
| ADVISORY | 3 |
| INFO | 2 |

## Downstream Handoff Notes (CONSUMER_CONTEXT = TASK_ESTIMATING)

The following observations are relevant for task estimating consumers:

1. **8 BLOCKING upstream dependencies** must be tracked for estimating readiness. Until these are satisfied (or their maturity is confirmed), DEL-011-07 estimates should be flagged as contingent:
   - 2 construction prerequisites (superstructure DEL-011-01, embedments DEL-011-02) -- these gate physical construction start.
   - 3 design prerequisites (IFC drawings DEL-002-05, DEL-002-09; structural specification DEL-002-12) -- these gate both procurement and construction. Material quantities and specifications cannot be finalized until IFC drawings are issued.
   - 2 permit constraints (building permit DEL-009-02, safety code permits DEL-009-03) -- these gate construction commencement.
   - 1 downstream handover (PKG-012 fit-out) -- scope boundary at the mezzanine deck surface is TBD (CFT-011-07-02). Estimators should note this scope boundary ambiguity; it may shift cost items between PKG-011 and PKG-012.

2. **Key TBD items affecting estimates:**
   - Mezzanine floor area (exact dimensions TBD per IFC drawings and CFT-011-07-01 resolution)
   - Structural system (steel framing assumed but TBD per structural engineer)
   - Floor deck type (concrete-topped steel deck assumed but TBD)
   - Design live load (TBD per structural engineer; 4.8-7.2 kPa range cited as general guidance)

3. **3 ADVISORY interfaces** provide supporting context but are not hard gates:
   - DEL-002-10 (calculation package) -- conditionally required
   - DEL-019-04 (QC plan) -- format alignment for deficiency tracking
   - DEL-010-01 (foundation) -- load path coordination interface
