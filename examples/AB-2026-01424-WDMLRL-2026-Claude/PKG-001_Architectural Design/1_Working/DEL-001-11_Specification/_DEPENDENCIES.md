# Dependencies: DEL-001-11 Architectural Specification

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (v3.1 schema)
- **Total rows:** 21
- **ACTIVE:** 21
- **RETIRED:** 0

### ANCHOR Rows (8 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-11-A01 | IMPLEMENTS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-11-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-11-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-001-11-A04 | TRACES_TO_REQUIREMENT | SOW-0070 | Renovate 250 sq ft kitchenette area | HIGH |
| DEP-001-11-A05 | TRACES_TO_REQUIREMENT | SOW-0071 | Renovate Old North Shop mezzanine | HIGH |
| DEP-001-11-A06 | TRACES_TO_REQUIREMENT | SOW-0072 | Renovate existing washroom below mezzanine | HIGH |
| DEP-001-11-A07 | TRACES_TO_REQUIREMENT | SOW-0073 | Construct new locker/change room with laundry services | HIGH |
| DEP-001-11-A08 | TRACES_TO_REQUIREMENT | SOW-0074 | Expand washroom facilities to include urinal | HIGH |

### EXECUTION Rows (13 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-001-11-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | HIGH | BLOCKING |
| DEP-001-11-E02 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 Architectural Floor Plans (representative of DEL-001-02 through DEL-001-10) | HIGH | ADVISORY |
| DEP-001-11-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-12 Structural Specification | HIGH | ADVISORY |
| DEP-001-11-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-003-07 Mechanical Specification | HIGH | ADVISORY |
| DEP-001-11-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-09 Electrical Specification | HIGH | ADVISORY |
| DEP-001-11-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-08 Plumbing Specification | HIGH | ADVISORY |
| DEP-001-11-E07 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-005-07 Civil Specification | HIGH | ADVISORY |
| DEP-001-11-E08 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation and Report | HIGH | BLOCKING |
| DEP-001-11-E09 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 Preliminary Site Survey | HIGH | BLOCKING |
| DEP-001-11-E10 | UPSTREAM | PREREQUISITE | EXTERNAL | County welding equipment specifications | HIGH | BLOCKING |
| DEP-001-11-E11 | UPSTREAM | PREREQUISITE | EXTERNAL | Existing conditions survey -- Old North Shop | HIGH | BLOCKING |
| DEP-001-11-E12 | UPSTREAM | CONSTRAINT | DOCUMENT | Alberta Building Code (current edition) | HIGH | BLOCKING |
| DEP-001-11-E13 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-09 Old North Shop Demolition Plans | MEDIUM | ADVISORY |

## Run Notes

### Run Parameters
- **Run date:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS:** AUTO (resolved to: Datasheet.md, Specification.md, Guidance.md, Procedure.md)
- **ANCHOR_DOC:** AUTO (resolved to: Datasheet.md -- highest-confidence anchor source per filename heuristic "datasheet")
- **EXECUTION_DOC_ORDER:** AUTO (resolved to: Procedure.md, Guidance.md, Specification.md)
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (R1 -- 2026-02-25)
- **_REFERENCES.md:** Present; used for document pointer resolution.

### Defaults and Assumptions
- ANCHOR_DOC selected as Datasheet.md (contains Identification table with SOW and OBJ mappings).
- EXECUTION_DOC_ORDER: Procedure.md first (contains explicit Prerequisites table), then Guidance.md (contains Principles and Considerations with dependency signals), then Specification.md (contains scope boundaries and requirement-level coordination statements).
- All anchor targets (SOW-0011, SOW-0070 through SOW-0074, OBJ-001, OBJ-003) confirmed against decomposition section 7 PKG-001 deliverable table.
- All deliverable targets (DEL-001-01, DEL-001-02, DEL-001-09, DEL-002-12, DEL-003-07, DEL-004-09, DEL-005-07, DEL-006-08, DEL-008-01, DEL-008-02) confirmed against decomposition section 7.
- E02 direction corrected from UPSTREAM to DOWNSTREAM: the specification provides normative requirements consumed by the drawing set, not the other way around.
- Discipline interface rows (E03 through E07) each capture an explicit scope exclusion boundary plus coordination requirement stated across multiple source documents.
- E10 (County welding equipment specifications) and E11 (existing conditions survey) are EXTERNAL targets with no deliverable ID because they originate from the Owner/County or field activities not tracked as project deliverables.
- E12 (Alberta Building Code) is a DOCUMENT constraint: the code must be obtained and its applicable edition confirmed as a prerequisite for specification finalization.

### Warnings
- (none)

### Quality Check Results
- Parent anchor check: 1 ACTIVE IMPLEMENTS_NODE row (DEP-001-11-A01). PASS.
- All ACTIVE rows have EvidenceFile and SourceRef. PASS.
- DependencyID uniqueness: 21 unique IDs for 21 rows. PASS.
- Schema version: all rows set to v3.1. PASS.
- Enum normalization: all values canonical. PASS.
- EstimateImpactClass and ConsumerHint populated for all EXECUTION rows per CONSUMER_CONTEXT=TASK_ESTIMATING. PASS.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ANCHOR ACTIVE | EXECUTION ACTIVE | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (R1) | (none) | 8 | 13 | 21 |

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 21
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown, ACTIVE rows only)
- **TBD:** 8 (all ANCHOR rows plus E02)
- **PENDING:** 12 (E01, E03 through E13 -- upstream inputs not yet received)
- **SATISFIED:** 0

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Estimating-Relevant Summary

**BLOCKING dependencies (6):** These gate meaningful estimating for DEL-001-11. Until resolved, scope or key quantities remain unknown.

1. **DEP-001-11-E01** -- County approval of Preliminary Architectural Design (DEL-001-01). Without preliminary design approval, the specification cannot be finalized and its scope cannot be estimated with confidence.
2. **DEP-001-11-E08** -- Geotechnical Investigation Report (DEL-008-01). Foundation and floor slab design inputs affect specification scope.
3. **DEP-001-11-E09** -- Preliminary Site Survey (DEL-008-02). Siting data affects specification coordination scope.
4. **DEP-001-11-E10** -- County welding equipment specifications (EXTERNAL). Required to finalize electrical receptacle and steel plate requirements; affects quantities.
5. **DEP-001-11-E11** -- Existing conditions survey for Old North Shop (EXTERNAL). Required to finalize renovation specification sections ARCH-040 through ARCH-044; without this, renovation scope cannot be quantified.
6. **DEP-001-11-E12** -- Alberta Building Code (DOCUMENT). Drives occupancy classification, fixture counts, accessibility, and envelope requirements. Must be confirmed before specification content can be scoped.

**ADVISORY dependencies (7):** These may change quantities, specifications, or procurement approach but are not hard gates for estimating.

1. **DEP-001-11-E02** -- Drawing set (DEL-001-02 through DEL-001-10) depends on this specification for materials and standards.
2. **DEP-001-11-E03** -- Structural Specification (DEL-002-12) interface for steel plates, mezzanine loads, floor slab.
3. **DEP-001-11-E04** -- Mechanical Specification (DEL-003-07) interface for service pit ventilation, heating, exhaust.
4. **DEP-001-11-E05** -- Electrical Specification (DEL-004-09) interface for service pit lighting, receptacles.
5. **DEP-001-11-E06** -- Plumbing Specification (DEL-006-08) interface for washroom fixtures, cistern, wash bay drains.
6. **DEP-001-11-E07** -- Civil Specification (DEL-005-07) interface for driving surface, mud sump, grading.
7. **DEP-001-11-E13** -- Demolition Plans (DEL-001-09) coordination for renovation selective removal scope.

### Estimating Readiness Assessment
DEL-001-11 has **6 BLOCKING upstream dependencies** that are all in PENDING satisfaction status. Estimating this deliverable with confidence requires resolution of at minimum E01 (preliminary design approval) and E11 (existing conditions survey), which together define the full scope envelope. The remaining BLOCKING items (E08, E09, E10, E12) affect specific specification sections but may allow partial estimating if the new addition scope is separated from the renovation scope.
