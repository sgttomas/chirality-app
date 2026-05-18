# DEL-008-02 Dependencies

## Upstream Dependencies
None identified. This deliverable is a foundational site survey without upstream technical dependencies.

## Downstream Dependencies
- **DEL-008-03**: Construction Survey (uses control points from preliminary survey)
- **PKG-002**: Foundation Design (requires topographic data)
- **PKG-003+**: All downstream design packages (require site coordinate system)

## External Dependencies
- Site access for field surveying
- Client approval for survey methodology
- Weather conditions suitable for field work
- Availability of survey control references

## Tracking Status
**TRACKED** — Dependency register active. See `Dependencies.csv` for machine-readable register.

## Notes
Preliminary survey establishes spatial foundation for all subsequent work and provides control points for future surveys.

---

## Extracted Dependency Register

**Register file:** `Dependencies.csv` (v3.1 schema)
**Total ACTIVE rows:** 16 (2 ANCHOR + 14 EXECUTION)
**RETIRED rows:** 0

### ANCHOR Dependencies (Tree -- Definition Linkage)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-008-02-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0002 | SOW-0002 | HIGH |
| DEP-008-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 | OBJ-003 — Site Investigation & Environmental Assessment | HIGH |

### EXECUTION Dependencies -- UPSTREAM (Inputs / Constraints)

| DependencyID | DependencyType | TargetType | TargetName | EstimateImpact | Confidence |
|---|---|---|---|---|---|
| DEP-008-02-003 | PREREQUISITE | DOCUMENT | Appendix C — Site Maps | ADVISORY | HIGH |
| DEP-008-02-004 | PREREQUISITE | DOCUMENT | RFP (AB-2026-01424-WDMLRL) | ADVISORY | HIGH |
| DEP-008-02-005 | INTERFACE | DELIVERABLE | DEL-008-01 Geotechnical Investigation & Report | ADVISORY | HIGH |
| DEP-008-02-006 | CONSTRAINT | EXTERNAL | Owner Approval of Survey Plan | BLOCKING | HIGH |
| DEP-008-02-007 | CONSTRAINT | EXTERNAL | Site Access (WDMLRL Facility) | BLOCKING | MEDIUM |
| DEP-008-02-008 | PREREQUISITE | EXTERNAL | Mandatory Site Meeting (RFP 3.2) | BLOCKING | HIGH |
| DEP-008-02-009 | PREREQUISITE | EXTERNAL | Datum and Coordinate System Confirmation | BLOCKING | HIGH |
| DEP-008-02-015 | CONSTRAINT | EXTERNAL | County Earthworks Sequencing (RFP 3.3.1) | ADVISORY | MEDIUM |
| DEP-008-02-016 | PREREQUISITE | EXTERNAL | Existing Geodetic Control / Benchmark Availability | ADVISORY | MEDIUM |

### EXECUTION Dependencies -- DOWNSTREAM (Outputs / Handovers)

| DependencyID | DependencyType | TargetType | TargetName | EstimateImpact | Confidence |
|---|---|---|---|---|---|
| DEP-008-02-010 | HANDOVER | DELIVERABLE | DEL-008-03 Construction Survey | BLOCKING | HIGH |
| DEP-008-02-011 | HANDOVER | DELIVERABLE | DEL-008-04 As-Built Survey | ADVISORY | HIGH |
| DEP-008-02-012 | HANDOVER | PACKAGE | PKG-002 Structural Design | BLOCKING | HIGH |
| DEP-008-02-013 | HANDOVER | PACKAGE | PKG-005 Civil Design | BLOCKING | HIGH |
| DEP-008-02-014 | HANDOVER | PACKAGE | All Design Packages (PKG-001 thru PKG-007) | ADVISORY | MEDIUM |

---

## Run Notes

### Run: 2026-02-26 (Run 2)

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (found, R1 2026-02-25)
- SOURCE_DOCS: AUTO (resolved: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- DOC_ROLE_MAP: DEFAULT
- ANCHOR_DOC: Datasheet.md (matched heuristic: "datasheet")
- EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md (matched heuristic: "procedure", "spec", "guidance")

**Defaults applied:**
- Pre-existing Dependencies.csv present (15 rows from Run 1). Updated in place.
- All existing rows confirmed in source text; `LastSeen` updated to 2026-02-26.
- 1 new row added: DEP-008-02-016 (Existing Geodetic Control / Benchmark Availability).

**Anchor validation (decomposition-assisted):**
- SOW-0002 confirmed in decomposition SSOW section A (line 75) and scope ledger (line 591).
- OBJ-003 confirmed in decomposition Objectives table (line 304) and deliverable table (line 458).
- DEL-008-02 confirmed in decomposition PKG-008 deliverable table (line 458) as covering SOW-0002, supporting OBJ-003.
- Parent anchor (IMPLEMENTS_NODE): exactly 1. No warnings.

**Execution extraction notes:**
- DEL-008-01 interface: Procedure Step 1 explicitly requires coordination for control point sharing and field scheduling. Classified as INTERFACE rather than COORDINATION because specific data artifacts (control points, schedule data) are exchanged.
- Owner approval gate (R-009): Classified as CONSTRAINT/BLOCKING because it explicitly gates fieldwork commencement.
- Downstream handovers to PKG-002 and PKG-005: strongest evidence in Guidance Purpose section and Specification R-002. Both classified as BLOCKING for estimating because scope quantities (foundation design, grading design) depend on survey data.
- Broad downstream handover (PKG-001 thru PKG-007): Guidance Purpose section explicitly states "outputs are consumed by every downstream design and construction activity." Classified as ADVISORY because the specific blocking linkages are captured in individual rows.
- Weather conditions dependency from declared _DEPENDENCIES.md not extracted as an EXECUTION row because it is a general environmental condition, not an information-flow or artifact-transfer dependency. Noted here for traceability.
- **NEW (Run 2):** DEP-008-02-016 added for geodetic benchmark availability prerequisite. Procedure Technical Prerequisites (line 24, Lensing F-003) explicitly states this must be confirmed before mobilization. Classified as PREREQUISITE/EXTERNAL/UPSTREAM with ADVISORY impact (alternative methods like GNSS/PPP are available if benchmarks are unavailable, so it is not a hard gate but affects methodology and potentially cost).

**Target resolution notes (Run 2):**
- TargetRefID populated for ANCHOR rows (SOW-0002, OBJ-003) and DOCUMENT rows (R-07, R-01) to improve referential integrity.
- TargetDeliverableID set to empty for non-DELIVERABLE targets per schema rules.
- Package-level downstream targets (PKG-002, PKG-005) use TargetRefID for the package ID; TargetDeliverableID remains empty per schema rules (TargetType=PACKAGE, not DELIVERABLE).
- TargetName for DEP-008-02-014 clarified from ambiguous "PKG-001 thru PKG-007 (all design packages)" to "All Design Packages (PKG-001 thru PKG-007)" for readability.

**Warnings:** None.

### Run: 2026-02-26 (Run 1)

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (found, R1 2026-02-25)
- SOURCE_DOCS: AUTO (resolved: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- DOC_ROLE_MAP: DEFAULT
- ANCHOR_DOC: Datasheet.md (matched heuristic: "datasheet")
- EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md (matched heuristic: "procedure", "spec", "guidance")

**Defaults applied:**
- No pre-existing Dependencies.csv; file created fresh.
- All rows are Origin=EXTRACTED with FirstSeen=2026-02-26.

**Anchor validation (decomposition-assisted):**
- SOW-0002 confirmed in decomposition SSOW section A (line 75) and scope ledger (line 591).
- OBJ-003 confirmed in decomposition Objectives table (line 304).
- DEL-008-02 confirmed in decomposition PKG-008 deliverable table (line 458) as covering SOW-0002, supporting OBJ-003.
- Parent anchor (IMPLEMENTS_NODE): exactly 1. No warnings.

**Warnings:** None.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 (Run 1) | UPDATE | CONSERVATIVE | _Decomposition/WDMLRL_Decomposition_Claude.md (R1) | None | 15 (2 ANCHOR + 13 EXECUTION) |
| 2026-02-26 (Run 2) | UPDATE | CONSERVATIVE | _Decomposition/WDMLRL_Decomposition_Claude.md (R1) | None | 16 (2 ANCHOR + 14 EXECUTION) |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 16 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 2 (ANCHOR rows) |
| TBD | 12 |
| PENDING | 2 (document prerequisites: Appendix C, RFP -- documents exist but formal consumption not confirmed) |

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

The following observations are relevant for task estimating consumers:

1. **BLOCKING upstream dependencies (4):** Owner approval of survey plan (DEP-008-02-006), site access (DEP-008-02-007), mandatory site meeting (DEP-008-02-008), and datum/coordinate system confirmation (DEP-008-02-009) all gate fieldwork commencement. Estimating cannot assume survey fieldwork duration until these constraints are resolved or scheduled.

2. **BLOCKING downstream handovers (3):** DEL-008-03 (construction survey), PKG-002 (structural/foundation design), and PKG-005 (civil/grading design) are blocked on outputs from this deliverable. Survey completion is on the critical path for design disciplines.

3. **Scope uncertainty for estimating:** Multiple TBD items in the Datasheet (datum, accuracy class, mapping scale, boundary survey scope) affect survey scope and therefore cost/duration estimates. These TBDs are gated by the Owner approval constraint (DEP-008-02-006).

4. **DEL-008-01 interface (ADVISORY):** Coordination with geotechnical investigation may affect mobilization strategy (shared vs. separate site visits). Not a hard gate but affects estimating assumptions about mobilization count.

5. **County earthworks sequencing (ADVISORY):** Whether survey occurs before or after County clearing/earthworks affects field conditions and potentially survey scope (pre- vs. post-disturbance conditions). Not a hard gate but affects estimating assumptions about field productivity.

6. **Geodetic control availability (ADVISORY, NEW Run 2):** The need to confirm existing geodetic benchmarks before mobilization (DEP-008-02-016) may affect field methodology and cost. If nearby benchmarks are unavailable, GNSS/PPP or similar absolute positioning methods would be required, potentially adding equipment cost or field time. Not a hard gate (alternative methods exist) but should be factored into estimating assumptions.
