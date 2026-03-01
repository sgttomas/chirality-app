# DEL-005-06 Dependencies

## Upstream Dependencies

### DEL-008-01 -- Geotechnical Investigation & Report (PKG-008)
- **Type:** PREREQUISITE (Hold Point HP-02)
- **Statement:** Geotechnical investigation report required before driving surface design (Step 4) and slope stability calculations (Step 5). Subgrade bearing capacity, soil classification, and groundwater data are critical inputs. Foundation pricing variable until geotech complete.
- **Impact if unavailable:** Cannot finalize driving surface thickness calculations, slope stability assessment, or pavement design. Preliminary design may proceed with interim conservative values per Guidance Principle 3 but must be labeled PRELIMINARY.
- **Estimate Impact:** BLOCKING -- scope and key quantities for driving surface and slope stability unknown without this deliverable.

### DEL-008-02 -- Preliminary Site Survey (PKG-008)
- **Type:** PREREQUISITE (Hold Point HP-01)
- **Statement:** Existing grades, drainage patterns, and site boundaries required before grading and drainage calculations can be performed (Step 3). Drainage basin delineation cannot proceed without survey data.
- **Impact if unavailable:** Cannot begin Step 2 (drainage basin establishment) or Step 3 (grading and drainage calculations). Total development area TBD pending this survey.
- **Estimate Impact:** BLOCKING -- grading volume calculations and drainage sizing depend entirely on this input.

### DEL-005-01 -- Preliminary Civil Design (PKG-005)
- **Type:** CONSTRAINT (Hold Point HP-03)
- **Statement:** County preliminary civil design approval required before final IFC calculations are completed (Step 9). This is an approval gate, not a data dependency.
- **Impact if unavailable:** Cannot finalize and seal calculation package for IFC submission.
- **Estimate Impact:** BLOCKING -- IFC finalization is gated.

### DEL-006-05 -- Septic System Details (PKG-006)
- **Type:** INTERFACE
- **Statement:** Septic system drainage envelope required as civil design input per REQ-011. Drainage interface coordination between civil site drainage and septic outfall/drainage field.
- **Impact if unavailable:** Drainage calculations may not fully account for septic system constraints; may require revision when septic design is available.
- **Estimate Impact:** ADVISORY -- likely to change drainage layout details but not a hard gate.

### R-01 -- AB-2026-01424-WDMLRL RFP.pdf
- **Type:** CONSTRAINT (governing document)
- **Statement:** RFP sections 3.3.2 and 3.4 are governing scope and design requirements. Available.

### R-04 -- AB-2026-01424-Appendix B (Shop).pdf
- **Type:** PREREQUISITE (available)
- **Statement:** Conceptual floor plan / building footprint for initial layout and drainage area delineation. Available.

### R-07 -- AB-2026-01424-Appendix C - Site Maps.pdf
- **Type:** PREREQUISITE (available)
- **Statement:** Site location map and expansion area aerial for site context and drainage basin identification. Available.

### County Preliminary Design Approval (External)
- **Type:** CONSTRAINT (external decision gate)
- **Statement:** County must approve preliminary civil design before final calculations are completed (REQ-008). This is an external approval action.
- **Estimate Impact:** BLOCKING -- gates IFC finalization.

## Downstream Dependencies

### DEL-005-02 -- Site Grading Plan (PKG-005)
- **Type:** HANDOVER
- **Statement:** Calculation package provides the engineering calculation basis supporting the Site Grading Plan drawing.

### DEL-005-03 -- Drainage Plan (PKG-005)
- **Type:** HANDOVER
- **Statement:** Calculation package provides the engineering calculation basis supporting the Drainage Plan drawing.

### DEL-005-04 -- Driving Surface & Pad Layout Plan (PKG-005)
- **Type:** HANDOVER
- **Statement:** Calculation package provides the engineering calculation basis supporting the Driving Surface & Pad Layout drawing.

### DEL-005-05 -- Civil Sections & Details (PKG-005)
- **Type:** HANDOVER
- **Statement:** Calculation package provides the engineering calculation basis supporting the Civil Sections & Details drawing.

### DEL-005-07 -- Civil Specification (PKG-005)
- **Type:** INTERFACE
- **Statement:** Calculation package must be cross-document consistent with the Civil Specification. Driving surface calculations (Step 4.3) must be consistent with DEL-005-07.

### PKG-007 -- Landscape Architectural Design
- **Type:** HANDOVER
- **Statement:** Transmit final civil grades, drainage outfall locations, and erosion control requirements to Landscape Architect after preliminary grading established and before IFC lock.

### PKG-018 -- Sitework & Civil Construction
- **Type:** ENABLES
- **Statement:** Civil design deliverables (PKG-005) must be complete and issued before PKG-018 construction can begin.

## Internal Dependencies

No internal task-level dependencies extracted. All sequencing is captured in the Procedure step ordering and hold points (HP-01 through HP-04).

## External Dependencies

### County Preliminary Design Approval
- Per REQ-008 (Specification) and Hold Point HP-03 (Procedure): County must approve preliminary civil design before IFC calculations are finalized.
- Status: PENDING

### Applicable Alberta Safety Codes and Camrose County Standards
- Per REQ-006 (Specification) and Procedure Step 1.7: Specific code clauses are TBD. The Civil Engineer must research and identify applicable code/bylaw references.
- Status: TBD (identified as a known gap in source documents)

## NOT_TRACKED Dependencies

### Structural Calculation Package (DEL-002-10)
- Reason: Specification explicitly excludes structural foundation calculations from this deliverable. No information flow extracted.
- Reference: Specification > Scope > What This Deliverable Excludes

### Interior Plumbing/Drainage (DEL-006 series except DEL-006-05)
- Reason: Specification explicitly excludes interior plumbing/drainage calculations. Only the septic interface (DEL-006-05) is tracked.
- Reference: Specification > Scope > What This Deliverable Excludes

## Tracking Notes

Dependencies will be updated as project progresses and scope is refined.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 22 (7 ANCHOR + 15 EXECUTION)
**Total RETIRED rows:** 0

### ANCHOR Rows (7 ACTIVE)

| DependencyID | AnchorType | TargetRefID / TargetName | Confidence |
|---|---|---|---|
| DEP-005-06-A001 | IMPLEMENTS_NODE | PKG-005 -- Civil Design | HIGH |
| DEP-005-06-A002 | TRACES_TO_REQUIREMENT | SOW-0015 | HIGH |
| DEP-005-06-A003 | TRACES_TO_REQUIREMENT | SOW-0020 | HIGH |
| DEP-005-06-A004 | TRACES_TO_REQUIREMENT | SOW-0021 | HIGH |
| DEP-005-06-A005 | TRACES_TO_REQUIREMENT | SOW-0077 | HIGH |
| DEP-005-06-A006 | TRACES_TO_REQUIREMENT | OBJ-001 | HIGH |
| DEP-005-06-A007 | TRACES_TO_REQUIREMENT | OBJ-003 | HIGH |

### EXECUTION Rows (15 ACTIVE)

| DependencyID | Direction | Type | Target | EstimateImpact |
|---|---|---|---|---|
| DEP-005-06-E001 | UPSTREAM | PREREQUISITE | DEL-008-01 (Geotech Report) | BLOCKING |
| DEP-005-06-E002 | UPSTREAM | PREREQUISITE | DEL-008-02 (Prelim Survey) | BLOCKING |
| DEP-005-06-E003 | UPSTREAM | CONSTRAINT | DEL-005-01 (Prelim Civil Design) | BLOCKING |
| DEP-005-06-E004 | UPSTREAM | INTERFACE | DEL-006-05 (Septic Details) | ADVISORY |
| DEP-005-06-E005 | DOWNSTREAM | HANDOVER | DEL-005-02 (Site Grading Plan) | ADVISORY |
| DEP-005-06-E006 | DOWNSTREAM | HANDOVER | DEL-005-03 (Drainage Plan) | ADVISORY |
| DEP-005-06-E007 | DOWNSTREAM | HANDOVER | DEL-005-04 (Driving Surface Layout) | ADVISORY |
| DEP-005-06-E008 | DOWNSTREAM | HANDOVER | DEL-005-05 (Civil Sections) | ADVISORY |
| DEP-005-06-E009 | DOWNSTREAM | INTERFACE | DEL-005-07 (Civil Specification) | ADVISORY |
| DEP-005-06-E010 | DOWNSTREAM | HANDOVER | PKG-007 (Landscape Arch) | ADVISORY |
| DEP-005-06-E011 | DOWNSTREAM | ENABLES | PKG-018 (Sitework & Civil Construction) | BLOCKING |
| DEP-005-06-E012 | UPSTREAM | CONSTRAINT | R-01 (RFP) | INFO |
| DEP-005-06-E013 | UPSTREAM | PREREQUISITE | R-07 (Site Maps) | INFO |
| DEP-005-06-E014 | UPSTREAM | PREREQUISITE | R-04 (Appendix B Shop) | INFO |
| DEP-005-06-E015 | UPSTREAM | CONSTRAINT | County preliminary approval (external) | BLOCKING |

---

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING

### Paths Used
- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-005_Civil Design/1_Working/DEL-005-06_Calculation-Package`
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md` (loaded successfully)

### Source Documents Scanned (AUTO)
- **ANCHOR_DOC:** `Datasheet.md` (selected by heuristic: contains `datasheet` in filename; highest anchor signal)
- **EXECUTION_DOC_ORDER:**
  1. `Procedure.md` (strongest execution/workflow signal)
  2. `Specification.md` (requirements and verification signal)
  3. `Guidance.md` (coordination and context signal)

### DOC_ROLE_MAP (DEFAULT heuristic applied)
- ANCHOR_DOC candidates matched: `Datasheet.md`
- EXECUTION_DOC candidates matched: `Procedure.md`, `Guidance.md`
- Additional source: `Specification.md` (requirements role)

### Defaults Applied
- SOURCE_DOCS: AUTO -- scanned deliverable folder, selected Datasheet.md, Procedure.md, Specification.md, Guidance.md. Excluded: `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`, `_STATUS.md` (generated/metadata files).
- ANCHOR_DOC: AUTO -- selected `Datasheet.md`
- EXECUTION_DOC_ORDER: AUTO -- Procedure.md, Specification.md, Guidance.md

### Assumptions
- ASSUMPTION: `TargetType=REQUIREMENT` used for both SOW items and OBJ items in ANCHOR trace rows. The decomposition uses SOW-prefixed IDs for scope items and OBJ-prefixed IDs for objectives; both are treated as requirement-class anchors.
- ASSUMPTION: `SatisfactionStatus=SATISFIED` set for document dependencies (R-01, R-04, R-07) because these documents are explicitly marked as "Available" in the Procedure Prerequisites table.
- ASSUMPTION: `SatisfactionStatus=PENDING` set for upstream deliverable dependencies (DEL-008-01, DEL-008-02, DEL-005-01, DEL-006-05) and external approval (County) because the source documents indicate these are not yet available.

### Warnings
- None. All quality checks passed.

### Integrity Check Results
- Parent anchor (IMPLEMENTS_NODE) count: 1 -- PASS
- DependencyID uniqueness: 22/22 -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- All enums are canonical write-form -- PASS
- CSV parseable -- PASS

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Loaded (WDMLRL_Decomposition_Claude.md R1) | None | 7 | 15 | 22 |

---

## Lifecycle Summary

### Extraction Lifecycle
| Status | Count |
|---|---|
| ACTIVE | 22 |
| RETIRED | 0 |

### Closure Lifecycle (ACTIVE rows)
| SatisfactionStatus | Count |
|---|---|
| TBD | 14 |
| PENDING | 5 |
| SATISFIED | 3 |

### Breakdown
- **TBD (14):** All ANCHOR rows (7) and downstream EXECUTION rows (7, including HANDOVER, INTERFACE, and ENABLES) -- satisfaction not yet assessed or not applicable at this stage.
- **PENDING (5):** Upstream deliverable dependencies (DEL-008-01, DEL-008-02, DEL-005-01, DEL-006-05) and external County approval (DEP-005-06-E015) -- these inputs are not yet available.
- **SATISFIED (3):** Document dependencies (R-01, R-04, R-07) -- these governing/reference documents are already available.

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are provided for downstream task estimating workflows:

### Blocking Dependencies (4 rows, EstimateImpactClass=BLOCKING)
These dependencies gate meaningful estimating because scope or key quantities are unknown without them:

1. **DEP-005-06-E001 (DEL-008-01 Geotech Report):** Driving surface thickness, subgrade parameters, and slope stability assessment cannot be finalized. This affects quantity takeoff for gravel surface and potentially drainage infrastructure sizing. Interim conservative estimates may be used per Guidance Principle 3 but carry uncertainty.

2. **DEP-005-06-E002 (DEL-008-02 Preliminary Survey):** Grading volumes, drainage basin areas, and stormwater infrastructure sizing depend on survey data. Without survey data, cut/fill volumes and drainage feature sizes cannot be estimated with confidence.

3. **DEP-005-06-E003 (DEL-005-01 Preliminary Civil Design approval) + DEP-005-06-E015 (County approval):** These represent the same approval gate from two perspectives (internal deliverable + external action). IFC finalization is blocked until County approves preliminary design. This may affect schedule estimating for the IFC package.

4. **DEP-005-06-E011 (PKG-018 Sitework downstream):** The civil calculation package must be complete before sitework construction can begin. This is a critical-path constraint for construction scheduling estimates.

### Advisory Dependencies (8 rows, EstimateImpactClass=ADVISORY)
These dependencies are likely to change quantities, specifications, or procurement approach but do not represent hard gates:

- **DEP-005-06-E004 (DEL-006-05 Septic Interface):** May affect drainage layout and sizing. Estimating should include a contingency allowance for drainage rework if septic design is not yet available.
- **DEP-005-06-E005 through E009 (downstream drawing and spec handovers):** These represent outputs from this deliverable. Estimating for downstream drawing production should account for the calculation package being a prerequisite.
- **DEP-005-06-E010 (PKG-007 Landscape coordination):** Civil-to-landscape information exchange may affect landscape scope quantities.

### Key Estimating Uncertainties
- Design storm return period is TBD (Guidance CONF-001) -- this affects drainage infrastructure sizing and therefore cost.
- Stormwater management approach (detention vs. infiltration vs. directed outfall) is TBD -- this fundamentally changes drainage infrastructure scope and cost.
- Topsoil stripping responsibility scope is conditionally stated (Guidance CONF-002) -- affects stripping volume estimates.
- Specific applicable code clauses are TBD (Specification REQ-006, Procedure Step 1.7) -- may introduce additional compliance requirements affecting scope.
