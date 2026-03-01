# DEL-007-02 Landscape Site Plans — Dependencies

## Tracking Status
- **Dependency Tracking**: ACTIVE
- **Register Schema**: v3.1
- **Register File**: Dependencies.csv

## Upstream Dependencies
- **DEL-007-01**: Preliminary Landscape Design (must be approved by County before IFC)
- Site maps and expansion area documentation (R-07)
- RFP landscape design requirements (R-01)
- Site survey and existing conditions documentation

## Internal Dependencies
- Coordination with project site planning and grading
- Landscape architect design development process completion

## Downstream Dependencies
- **DEL-007-03**: Planting & Restoration Plans (uses site plan framework)
- **DEL-007-04**: Landscape Specification (references plan callouts and details)

## External Dependencies
- Landscape Architect discipline assignment
- CAD standards and drawing template availability
- Coordination with other design disciplines
- Stakeholder review and approval availability

## Blocking Issues
- None currently identified

## Notes
Dependency tracking will activate once DEL-007-01 is approved and plan development begins. Current status reflects preliminary planning stage.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 20 (9 ANCHOR + 11 EXECUTION)
**RETIRED rows:** 0

### Anchor Edges (Tree -- Definition Traceability)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-007-02-A01 | IMPLEMENTS_NODE | SOW-0017 | Complete landscape architectural design | HIGH |
| DEP-007-02-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver code-compliant functional maintenance shop addition | HIGH |
| DEP-007-02-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-007-02-A04 | TRACES_TO_REQUIREMENT | SOW-0075 | Strip topsoil from all driving surfaces | HIGH |
| DEP-007-02-A05 | TRACES_TO_REQUIREMENT | SOW-0076 | Grade and landscape the proposed lot | HIGH |
| DEP-007-02-A06 | TRACES_TO_REQUIREMENT | SOW-0077 | Construct gravel driving surface for heavy equipment | HIGH |
| DEP-007-02-A07 | TRACES_TO_REQUIREMENT | SOW-0078 | Construct cement pads as shown on conceptual drawings | HIGH |
| DEP-007-02-A08 | TRACES_TO_REQUIREMENT | SOW-0079 | Construct gravel pad as shown on conceptual drawings | HIGH |
| DEP-007-02-A09 | TRACES_TO_REQUIREMENT | SOW-0018 | Produce all IFC drawings signed/stamped by P.Eng. | HIGH |

### Execution Edges (DAG -- Information Flow)

| DependencyID | Direction | DependencyType | TargetID | TargetName | Confidence | EstimateImpact |
|---|---|---|---|---|---|---|
| DEP-007-02-E01 | UPSTREAM | PREREQUISITE | DEL-007-01 | Preliminary Landscape Design | HIGH | BLOCKING |
| DEP-007-02-E02 | UPSTREAM | PREREQUISITE | DEL-008-01 | Geotechnical Investigation & Report | HIGH | BLOCKING |
| DEP-007-02-E03 | UPSTREAM | PREREQUISITE | DEL-008-02 | Preliminary Site Survey | HIGH | BLOCKING |
| DEP-007-02-E04 | UPSTREAM | INTERFACE | DEL-005-02 | Site Grading Plan | MEDIUM | ADVISORY |
| DEP-007-02-E05 | UPSTREAM | INTERFACE | DEL-005-03 | Drainage Plan | MEDIUM | ADVISORY |
| DEP-007-02-E06 | UPSTREAM | INTERFACE | DEL-005-04 | Driving Surface & Pad Layout Plan | MEDIUM | ADVISORY |
| DEP-007-02-E07 | UPSTREAM | CONSTRAINT | R-01 | AB-2026-01424-WDMLRL RFP.pdf | HIGH | INFO |
| DEP-007-02-E08 | UPSTREAM | CONSTRAINT | R-04 | AB-2026-01424-Appendix B (Shop).pdf | HIGH | BLOCKING |
| DEP-007-02-E09 | UPSTREAM | CONSTRAINT | R-07 | AB-2026-01424-Appendix C - Site Maps.pdf | HIGH | INFO |
| DEP-007-02-E10 | DOWNSTREAM | HANDOVER | DEL-007-03 | Planting & Restoration Plans | HIGH | ADVISORY |
| DEP-007-02-E11 | DOWNSTREAM | HANDOVER | DEL-007-04 | Landscape Specification | HIGH | ADVISORY |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE** | 20 |
| **RETIRED** | 0 |
| **ANCHOR (ACTIVE)** | 9 |
| -- IMPLEMENTS_NODE | 1 |
| -- TRACES_TO_REQUIREMENT | 8 |
| **EXECUTION (ACTIVE)** | 11 |
| -- UPSTREAM | 9 |
| -- DOWNSTREAM | 2 |

### Closure Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 12 |
| PENDING | 8 |

---

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

The following rows are flagged for task estimating consumption:

**BLOCKING dependencies (4):** These gate meaningful estimating -- scope or key quantities are unknown without them.
- DEP-007-02-E01: DEL-007-01 Preliminary Landscape Design (County approval gates IFC; design basis uncertain without approval)
- DEP-007-02-E02: DEL-008-01 Geotechnical Investigation & Report (grading assumptions and surface treatment dependent on geotech findings)
- DEP-007-02-E03: DEL-008-02 Preliminary Site Survey (existing conditions data required for accurate site layout and quantities)
- DEP-007-02-E08: R-04 Appendix B Shop conceptual drawing (spatial baseline defining building footprints and site features -- available in _Sources/)

**ADVISORY dependencies (5):** These may change quantities/specs or approach but are not hard gates.
- DEP-007-02-E04: DEL-005-02 Site Grading Plan (civil grading interface)
- DEP-007-02-E05: DEL-005-03 Drainage Plan (drainage coordination)
- DEP-007-02-E06: DEL-005-04 Driving Surface & Pad Layout Plan (civil driving surface interface)
- DEP-007-02-E10: DEL-007-03 Planting & Restoration Plans (downstream consumer of spatial framework)
- DEP-007-02-E11: DEL-007-04 Landscape Specification (downstream consumer of plan callouts)

**INFO dependencies (2):** Informational context; low likelihood of changing totals.
- DEP-007-02-E07: R-01 RFP (primary design-basis document -- available)
- DEP-007-02-E09: R-07 Appendix C Site Maps (site location reference -- available)

**Estimating readiness assessment:** DEL-007-02 has 3 BLOCKING deliverable prerequisites (DEL-007-01, DEL-008-01, DEL-008-02) whose status directly affects estimating confidence. The Appendix B spatial baseline (E08) is available in _Sources/. Until preliminary design approval and geotech/survey data are confirmed, estimating should treat grading scope and site layout quantities as provisional.

---

## Run Notes

**Run date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING
**Decomposition path:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md
**Decomposition status:** Available; validation and label resolution performed successfully.

**Source documents scanned (DOC_ROLE_MAP=DEFAULT):**
- ANCHOR_DOC: Datasheet.md (matched: "datasheet" pattern)
- EXECUTION_DOCS (in order): Procedure.md, Guidance.md, Specification.md
- Additional read-only inputs: _CONTEXT.md, _REFERENCES.md, _DEPENDENCIES.md (declared sections)

**Defaults applied:**
- SOURCE_DOCS=AUTO: all .md files in deliverable folder (excluding dependency artifacts and generated files)
- ANCHOR_DOC=AUTO: Datasheet.md selected by heuristic
- EXECUTION_DOC_ORDER=AUTO: Procedure.md > Guidance.md > Specification.md

**Assumptions recorded:**
- ANCHOR rows use SOW item IDs as TargetRefID; these are SSOW identifiers from the decomposition, not requirement IDs in the traditional sense. Treated as WBS_NODE targets for the parent SOW and contributing SOW items.
- SOW-0018 (P.Eng. stamp) is treated as a quality attribute trace anchor per decomposition decision D-008, not an execution prerequisite.
- PKG-018 construction execution deliverables (DEL-018-01 through DEL-018-04) were considered but NOT extracted as downstream edges because no explicit information/artifact handover from DEL-007-02 to specific PKG-018 deliverables was stated in sources. The Procedure states IFC distribution "to the project team" generically; this is insufficient for a CONSERVATIVE extraction.

**Warnings:** None.

**Quality check results:**
- Parent anchor check: 1 IMPLEMENTS_NODE row (DEP-007-02-A01) -- PASS
- Schema check: All required columns present -- PASS
- DependencyID uniqueness: All 20 IDs unique -- PASS
- Evidence check: All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- Enum normalization: All values canonical -- PASS
- FromDeliverableID consistency: All rows = DEL-007-02 -- PASS

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | Available (WDMLRL_Decomposition_Claude.md R1) | None | 20 (9A + 11E) |
