# Dependencies: DEL-001-09 Old North Shop Demolition Plans

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (v3.1, 15 rows, 15 ACTIVE / 0 RETIRED)
- **Summary:** 3 ANCHOR + 12 EXECUTION edges extracted from 4 source documents.

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-09-A01 | IMPLEMENTS_NODE | SOW-0070; SOW-0071; SOW-0072 | Renovate Old North Shop (kitchenette, mezzanine, washroom) | HIGH |
| DEP-001-09-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition and associated renovations | HIGH |
| DEP-001-09-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION Edges -- UPSTREAM (7 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | EstimateImpactClass | Confidence |
|---|---|---|---|---|---|
| DEP-001-09-E01 | PREREQUISITE | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | BLOCKING | HIGH |
| DEP-001-09-E03 | PREREQUISITE | EXTERNAL | Old North Shop Field Survey Data | BLOCKING | HIGH |
| DEP-001-09-E04 | PREREQUISITE | EXTERNAL | Old North Shop Existing As-Built Drawings | ADVISORY | MEDIUM |
| DEP-001-09-E05 | INTERFACE | PACKAGE | PKG-002 Structural Engineering -- Mezzanine Coordination | BLOCKING | HIGH |
| DEP-001-09-E06 | INTERFACE | PACKAGE | PKG-003/004/006 MEP Disciplines -- Demolition Scope Split | ADVISORY | HIGH |
| DEP-001-09-E07 | CONSTRAINT | EXTERNAL | Hazardous Materials Assessment | BLOCKING | HIGH |
| DEP-001-09-E08 | PREREQUISITE | DOCUMENT | R-04 Appendix B -- Shop Conceptual Floor Plan | INFO | HIGH |

### EXECUTION Edges -- DOWNSTREAM (5 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | EstimateImpactClass | Confidence |
|---|---|---|---|---|---|
| DEP-001-09-E02 | HANDOVER | DELIVERABLE | DEL-001-10 Old North Shop Renovation Plans | BLOCKING | HIGH |
| DEP-001-09-E09 | HANDOVER | DELIVERABLE | DEL-017-01 Kitchenette Renovation | ADVISORY | HIGH |
| DEP-001-09-E10 | HANDOVER | DELIVERABLE | DEL-017-02 Old North Shop Mezzanine Renovation | ADVISORY | HIGH |
| DEP-001-09-E11 | HANDOVER | DELIVERABLE | DEL-017-03 Washroom Renovation & Expansion | ADVISORY | HIGH |
| DEP-001-09-E12 | ENABLES | DELIVERABLE | DEL-009-02 Building Permit Application & Approval | ADVISORY | HIGH |

---

## Run Notes

### Run: 2026-02-26

**Parameters:**
- SCOPE: DEL-001-09_Demolition-Plans
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Specification.md, Procedure.md, Guidance.md)
- ANCHOR_DOC: AUTO (resolved to: Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved to: Procedure.md, Specification.md, Guidance.md, Datasheet.md)
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (available; R1 2026-02-25)
- _REFERENCES.md: available (used for R-04 TargetLocation resolution)

**Defaults applied:**
- ANCHOR_DOC resolved to Datasheet.md (contains `Identification` table with explicit Scope Items and Objectives fields -- highest anchor-signal density).
- EXECUTION_DOC_ORDER resolved by DOC_ROLE_MAP heuristic: Procedure.md (primary workflow/procedure), Specification.md (requirements/scope), Guidance.md (considerations/principles), Datasheet.md (downstream use context table).

**Assumptions:**
- None. All extracted rows are grounded in explicit source statements.

**Warnings:**
- (none)

**Integrity checks:**
- Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE row (DEP-001-09-A01) -- PASS.
- All 15 ACTIVE rows have EvidenceFile and SourceRef -- PASS.
- DependencyID uniqueness: 15 unique IDs -- PASS.
- All enums canonical (v3.1 write-form) -- PASS.
- TargetDeliverableID placement: correct for all rows (populated only for TargetType=DELIVERABLE) -- PASS.
- Extension columns (EstimateImpactClass, ConsumerHint) populated for all EXECUTION rows per CONSUMER_CONTEXT=TASK_ESTIMATING -- PASS.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Available (R1 2026-02-25) | (none) | 3 | 12 | 15 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 15 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 14 |
| SATISFIED | 1 |

**Note:** DEP-001-09-E08 (R-04 Appendix B) is marked SATISFIED because the document is confirmed available per _REFERENCES.md. All other dependencies have SatisfactionStatus=TBD pending project execution.

---

## Downstream Handoff Notes (CONSUMER_CONTEXT: TASK_ESTIMATING)

### Estimating-Critical Dependencies

The following dependencies are classified as **BLOCKING** for task estimating -- they gate meaningful scope definition or quantity takeoff for this deliverable:

1. **DEP-001-09-E03 -- Field Survey Data (BLOCKING).** Mezzanine and washroom renovation areas have TBD dimensions pending field survey. Until survey data is obtained, the demolition scope cannot be quantified for these two areas. The kitchenette area (~250 sq ft) has a stated area from R-01.

2. **DEP-001-09-E07 -- Hazardous Materials Assessment (BLOCKING).** If hazardous materials are present, demolition scope, method, and regulatory requirements may change materially. The Procedure includes a formal hold point (Step 1.3a) gating Phase 2 on this assessment.

3. **DEP-001-09-E05 -- Structural Coordination with PKG-002 (BLOCKING).** The mezzanine renovation may involve structural elements. Until the Structural Engineer confirms structural vs. non-structural classification, the architectural demolition scope boundary for the mezzanine cannot be finalized.

4. **DEP-001-09-E01 -- Preliminary Architectural Design Approval (BLOCKING).** County approval of preliminary design (DEL-001-01) is a contractual gate before IFC issue. This affects the overall timeline and milestone sequencing for estimating.

5. **DEP-001-09-E02 -- Handover to DEL-001-10 Renovation Plans (BLOCKING downstream).** The renovation design cannot proceed without the demolition plans, making this a critical-path handover. Estimating for DEL-001-10 and downstream PKG-017 construction deliverables depends on this handover completing.

### Advisory Dependencies

- **DEP-001-09-E04 -- As-Built Drawings (ADVISORY).** If as-built drawings are available, they reduce field survey effort and improve base plan accuracy. If unavailable (likely), field survey serves as primary source. Low impact on estimating totals.
- **DEP-001-09-E06 -- MEP Scope Split (ADVISORY).** The agreed scope division between architectural and MEP demolition drawings may shift quantities between disciplines. Does not block estimating for DEL-001-09 but may affect cross-discipline estimating.
- **DEP-001-09-E09/E10/E11 -- Construction Handovers (ADVISORY).** These affect PKG-017 construction estimating more than DEL-001-09 design estimating.
- **DEP-001-09-E12 -- Building Permit (ADVISORY).** Permit-readiness is a quality attribute of the drawing set; it does not change the estimating scope for producing the drawings.

### Key Estimating Uncertainties

- **Mezzanine area (SOW-0071):** TBD -- requires field survey. This is the largest dimensional unknown for demolition scope quantification.
- **Washroom area (SOW-0072):** TBD -- requires field survey.
- **Hazardous materials:** If present, may add abatement documentation requirements to the drawing set scope.
- **SOW-0073/0074 scope boundary:** Guidance CONF-002 flags an unresolved question about whether demolition for SOW-0073 (locker room) and SOW-0074 (washroom expansion) should be shown in DEL-001-09 or DEL-001-10. This decision could increase the sheet count and scope of this deliverable.
