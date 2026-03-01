# DEL-008-03 Dependencies

## Upstream Dependencies
- **DEL-008-02**: Preliminary Survey (control points and baseline data required)
- **Design Packages**: Construction plans and specifications required
- **DEL-002-11**: Foundation Design Package (final foundation IFC drawings gate final staking)
- **DEL-008-01**: Geotechnical Investigation (constrains foundation design timing)
- **PKG-005 / DEL-005-02**: Civil Grading Design (grade control must match civil design)
- **PKG-019**: Construction schedule (required to sequence survey activities)
- **County / Landfill Operations**: Site access confirmation
- **Prime Contractor**: OH&S framework and safety orientation
- **County**: Brushing/clearing and bulk cut/fill status (affects monument placement)
- **County / Owner**: Approval for construction layout approach

## Downstream Dependencies
- **DEL-008-04**: As-Built Survey (control data handoff package)
- **PKG-010**: Foundation Construction (layout staking for excavation and forming)
- **PKG-011**: Building Structure & Envelope (structural alignment, column setting-out, grade control)
- **PKG-018**: Sitework & Civil Construction (grade control for grading, driving surface, pads)

## External Dependencies
- Construction schedule confirmation (PKG-019)
- Site access during construction (County / landfill operations)
- OH&S / Prime Contractor framework compliance
- Client approvals for construction layout
- County brushing/clearing and bulk cut/fill status

## Tracking Status
**TRACKED** -- Dependencies extracted and registered in Dependencies.csv (v3.1 schema).

## Notes
Construction survey is dependent on preliminary survey completion and is a precursor to construction execution and as-built documentation.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total rows:** 17 (ACTIVE: 17, RETIRED: 0)

| Class | Count |
|-------|-------|
| ANCHOR | 3 |
| EXECUTION | 14 |

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-008-03-A01 | IMPLEMENTS_NODE | SOW-0003 | Conduct construction survey | HIGH |
| DEP-008-03-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Code-compliant functional delivery | HIGH |
| DEP-008-03-A03 | TRACES_TO_REQUIREMENT | OBJ-002 | Completion by December 31 2026 | HIGH |

### EXECUTION Rows (14 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-008-03-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 Preliminary Site Survey | HIGH | BLOCKING |
| DEP-008-03-E02 | UPSTREAM | PREREQUISITE | PACKAGE | IFC Drawings (PKG-001 through PKG-007) | HIGH | BLOCKING |
| DEP-008-03-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-005-02 Site Grading Plan | HIGH | ADVISORY |
| DEP-008-03-E04 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-002-11 Foundation Design Package | HIGH | BLOCKING |
| DEP-008-03-E05 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-008-01 Geotech Investigation | HIGH | ADVISORY |
| DEP-008-03-E06 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-019 Construction Schedule | MEDIUM | ADVISORY |
| DEP-008-03-E07 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-008-04 As-Built Survey | HIGH | INFO |
| DEP-008-03-E08 | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-010-01 Foundation Construction | HIGH | INFO |
| DEP-008-03-E09 | DOWNSTREAM | ENABLES | PACKAGE | PKG-011 Building Structure & Envelope | HIGH | INFO |
| DEP-008-03-E10 | DOWNSTREAM | ENABLES | PACKAGE | PKG-018 Sitework & Civil Construction | HIGH | INFO |
| DEP-008-03-E11 | UPSTREAM | CONSTRAINT | EXTERNAL | Site access confirmation (County) | HIGH | BLOCKING |
| DEP-008-03-E12 | UPSTREAM | CONSTRAINT | EXTERNAL | OH&S / Prime Contractor Framework | MEDIUM | ADVISORY |
| DEP-008-03-E13 | UPSTREAM | CONSTRAINT | EXTERNAL | County Brushing/Clearing and Bulk Cut/Fill Status | HIGH | ADVISORY |
| DEP-008-03-E14 | UPSTREAM | PREREQUISITE | EXTERNAL | Client/County Approval for Construction Layout | MEDIUM | ADVISORY |

---

## Run Notes

### Defaults and Paths Used
- **RUN_ROOT:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- **DELIVERABLE_FOLDER:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-008_Geotechnical Investigation & Surveying/1_Working/DEL-008-03_Construction-Survey/
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (located and readable; validated)
- **SOURCE_DOCS (AUTO):** Datasheet.md, Guidance.md, Procedure.md, Specification.md
- **ANCHOR_DOC (AUTO):** Datasheet.md (contains Identification table with SOW Reference, Objectives Supported)
- **EXECUTION_DOC_ORDER (AUTO):** Procedure.md, Specification.md, Guidance.md, Datasheet.md
- **_REFERENCES.md:** Read; used for target resolution context
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING

### Assumptions
- IFC drawings dependency (DEP-008-03-E02) spans PKG-001 through PKG-007 as a composite source. TargetType=PACKAGE is approximate; the actual sources span seven design packages. Each package produces IFC drawings consumed by this deliverable for staking purposes.
- PKG-019 construction schedule (DEP-008-03-E06): No single deliverable ID for "construction schedule" exists in the decomposition. TargetDeliverableID left empty; the schedule is a management artifact from PKG-019.
- Downstream ENABLES rows (DEP-008-03-E08 through E10) use package-level targets where the source documents reference the package rather than a specific deliverable within it.
- County clearing status (DEP-008-03-E13): TargetType=EXTERNAL because the County's brushing/clearing work is outside the Design-Builder's scope (OUT items SOW-0200, SOW-0201 per decomposition section 4). The dependency is on confirmation of status, not on performing the work.
- Client layout approval (DEP-008-03-E14): Procedure P-06 qualifies this with "where required," indicating it may not always be an active gate. Confidence=MEDIUM reflects this conditionality.

### Warnings
(none)

### Quality Check Results
- Schema: All 31 columns present; CSV parseable
- DependencyID: 17 unique IDs, no duplicates
- Evidence: All ACTIVE rows have EvidenceFile and SourceRef populated
- Parent anchor: Exactly 1 ACTIVE IMPLEMENTS_NODE row (DEP-008-03-A01 -> SOW-0003) -- PASS
- FromDeliverableID: All rows = DEL-008-03 -- PASS
- Enum normalization: All values are canonical write-form
- Extension columns: EstimateImpactClass and ConsumerHint populated for all EXECUTION rows per CONSUMER_CONTEXT=TASK_ESTIMATING
- TargetDeliverableID placement: Non-deliverable targets (WBS_NODE, REQUIREMENT, PACKAGE, EXTERNAL) have empty TargetDeliverableID -- PASS
- Referential integrity: All deliverable target IDs (DEL-008-02, DEL-005-02, DEL-002-11, DEL-008-01, DEL-008-04, DEL-010-01) confirmed in decomposition section 7 -- PASS

---

## Run History

| Timestamp | Mode | Strictness | ConsumerContext | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26T00:00 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Located and validated | (none) | 3 | 12 | 15 |
| 2026-02-26T21:00 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Located and validated | (none) | 3 | 14 | 17 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 17 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 3 (ANCHOR rows) |
| PENDING | 14 (EXECUTION rows) |

---

## Downstream Handoff Notes

**Consumer context: TASK_ESTIMATING**

The following dependencies are flagged as potentially relevant to task estimating readiness:

### BLOCKING (4 upstream execution dependencies)
These dependencies gate meaningful estimating because scope or key quantities are unknown without them:
1. **DEP-008-03-E01** (DEL-008-02 Preliminary Site Survey): Control points and baseline data are prerequisite inputs. Without these, the survey control network cannot be established and the scope of control verification work is uncertain.
2. **DEP-008-03-E02** (IFC Design Drawings, PKG-001-007): P.Eng.-stamped IFC drawings define what elements must be staked. Without IFC drawings, the staking scope and element count are not finalized.
3. **DEP-008-03-E04** (DEL-002-11 Foundation Design Package): The foundation design is variable-price and geotech-dependent. Foundation staking scope and complexity depend on the final foundation design.
4. **DEP-008-03-E11** (Site access confirmation): Without confirmed site access, field mobilization cannot be planned and site-specific conditions affecting survey methodology are unknown.

### ADVISORY (6 upstream execution dependencies)
These dependencies likely affect quantities, specifications, or approach but are not hard gates:
1. **DEP-008-03-E03** (DEL-005-02 Site Grading Plan): Civil grading design determines the grade control scope and complexity.
2. **DEP-008-03-E05** (DEL-008-01 Geotech Investigation): Geotech results affect foundation design timing, which affects the phasing of construction survey work.
3. **DEP-008-03-E06** (PKG-019 Construction Schedule): The construction schedule determines survey phasing and frequency of progress surveys.
4. **DEP-008-03-E12** (OH&S / Prime Contractor Framework): Safety requirements may affect field methodology and mobilization planning.
5. **DEP-008-03-E13** (County Brushing/Clearing Status): The status of County earthwork affects where permanent control monuments can be safely placed. If clearing is incomplete, monument placement must be deferred or adjusted.
6. **DEP-008-03-E14** (Client/County Layout Approval): County approval for the construction layout approach may be required before survey mobilization. Conditional prerequisite.

### INFO (4 downstream execution dependencies)
These are informational for estimating; they describe who consumes this deliverable's output:
1. **DEP-008-03-E07** (DEL-008-04 As-Built Survey): Control data handover.
2. **DEP-008-03-E08** (DEL-010-01 Foundation Construction): Layout staking consumer.
3. **DEP-008-03-E09** (PKG-011 Building Structure & Envelope): Alignment and grade control consumer.
4. **DEP-008-03-E10** (PKG-018 Sitework & Civil Construction): Grade control consumer.
