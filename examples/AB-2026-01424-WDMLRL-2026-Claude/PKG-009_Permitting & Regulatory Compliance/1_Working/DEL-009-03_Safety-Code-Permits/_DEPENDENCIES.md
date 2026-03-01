# _DEPENDENCIES.md
## DEL-009-03 | Safety Code Permits

### Dependency Status
- **Tracking Status**: TRACKED
- **Last Updated**: 2026-02-26
- **Owner**: Project Manager
- **Register Schema Version**: v3.1

### Upstream Dependencies (Inputs Required)
| Dependency | Source | Type | Status | Impact |
|------------|--------|------|--------|--------|
| OH&S Plan | Safety Officer | Document | NOT_STARTED | CRITICAL - Defines safety requirements |
| Project Design | Design Team | Document | NOT_STARTED | CRITICAL - Design determines safety scope |
| Safety Code Requirements | Regulatory Authority | Document | NOT_STARTED | CRITICAL - Defines permit scope |
| Risk Assessment | Safety Team | Document | NOT_STARTED | HIGH - Identifies hazards and controls |
| Budget Approval | Finance | Approval | NOT_STARTED | HIGH - Safety permits and certifications |

### Downstream Dependencies (Work Dependent on This)
| Dependent | Type | Relationship | Status |
|-----------|------|--------------|--------|
| Construction Phase | Project Phase | Gate - Safety permits required before construction | BLOCKED |
| DEL-009-04_Code-Compliance-Register | Deliverable | Tracking - Logs all safety permits and certifications | BLOCKED |
| Safety Inspections | Project Phase | Depends on - Pre-construction and ongoing safety checks | BLOCKED |
| Project Operations | Project Phase | Depends on - Certifications required during operations | BLOCKED |

### External Dependencies
| Entity | Dependency | Status |
|--------|-----------|--------|
| Fire Marshal | Fire safety inspection and approval | PENDING |
| Electrical Inspector | Electrical safety inspection and approval | PENDING |
| Safety Authority | OH&S certification and compliance verification | PENDING |
| Building Inspector | Building safety requirements coordination | PENDING |

### Constraint Dependencies
- Project design finalization (TBD)
- OH&S plan development (TBD)
- Safety inspection schedules (TBD)
- Construction timeline (TBD)

### Risk Dependencies
- Design changes affecting safety (internal risk)
- Regulatory authority interpretation changes (external risk)
- Safety inspection delays (external risk)
- Additional safety requirements discovered (external risk)

### Notes
- Parallel dependency with DEL-009-01 and DEL-009-02 (can proceed simultaneously)
- Multiple regulatory authorities involved (coordination critical)
- Safety permits gate construction phase
- All dependencies marked as NOT_TRACKED pending project initialization

---

## Extracted Dependency Register

**Total rows:** 14 | **ACTIVE:** 14 | **RETIRED:** 0

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID/TargetName | Confidence |
|---|---|---|---|---|
| DEP-009-03-A01 | IMPLEMENTS_NODE | WBS_NODE | SOW-0007 | HIGH |
| DEP-009-03-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | HIGH |
| DEP-009-03-A03 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | HIGH |

### EXECUTION Rows (11 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-009-03-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-019-01 (Prime Contractor Designation & OH&S Program) | HIGH | BLOCKING |
| DEP-009-03-E02 | UPSTREAM | PREREQUISITE | PACKAGE | Design Packages PKG-001 through PKG-007 | HIGH | BLOCKING |
| DEP-009-03-E03 | UPSTREAM | PREREQUISITE | WBS_NODE | SOW-0018 (IFC Drawings) | HIGH | BLOCKING |
| DEP-009-03-E04 | UPSTREAM | CONSTRAINT | EXTERNAL | CCDC 14-2013 Contract Execution | HIGH | BLOCKING |
| DEP-009-03-E05 | UPSTREAM | PREREQUISITE | EXTERNAL | Prime Contractor Designation Form (County-issued) | HIGH | ADVISORY |
| DEP-009-03-E06 | UPSTREAM | PREREQUISITE | EXTERNAL | County Project Manager Availability | MEDIUM | ADVISORY |
| DEP-009-03-E07 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-04 (Code Compliance Register & Inspection Log) | HIGH | ADVISORY |
| DEP-009-03-E08 | DOWNSTREAM | ENABLES | UNKNOWN | Construction Phase | HIGH | BLOCKING |
| DEP-009-03-E09 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-019-01 (Prime Contractor Designation & OH&S Program) | MEDIUM | ADVISORY |
| DEP-009-03-E10 | UPSTREAM | CONSTRAINT | EXTERNAL | December 31, 2026 Completion Deadline | HIGH | INFO |
| DEP-009-03-E11 | UPSTREAM | CONSTRAINT | EXTERNAL | Permit Fee Payment by County (Excluded from Proponent Scope) | HIGH | BLOCKING |

---

## Run Notes

**Run date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

**Defaults applied:**
- SOURCE_DOCS: AUTO -- scanned deliverable folder, identified 4 source documents: Datasheet.md, Specification.md, Guidance.md, Procedure.md
- DOC_ROLE_MAP: DEFAULT heuristic applied
- ANCHOR_DOC: AUTO -- selected `Datasheet.md` (contains "datasheet" in filename; highest anchor-signal match)
- EXECUTION_DOC_ORDER: AUTO -- `Procedure.md` (procedure), `Guidance.md` (guidance), `Specification.md` (spec), `Datasheet.md` (datasheet)
- Excluded from source scan: `_DEPENDENCIES.md`, `_REFERENCES.md`, `_CONTEXT.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`, `_STATUS.md` (generated/metadata files)

**Decomposition:** AVAILABLE at `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 -- 2026-02-25). Anchor validation and label resolution performed successfully.

**_REFERENCES.md:** Read. Used to confirm document references and related deliverable pointers (DEL-009-01, DEL-009-02, DEL-009-04). No dependency rows emitted solely from _REFERENCES.md content.

**Warnings:** None.

**Extraction decisions:**
- DEL-009-01 (Development Permit) and DEL-009-02 (Building Permit) are noted in sources as parallel permits but no explicit information/artifact transfer is stated between them and DEL-009-03. Per the information-flow-only model, these are not extracted as dependency rows.
- Design dependency recorded at PACKAGE level (PKG-001 through PKG-007) because the Procedure prerequisites reference the range collectively. IFC drawings (SOW-0018) recorded separately as a more specific prerequisite.
- DEL-019-01 appears in both UPSTREAM (OH&S plan informs audit) and DOWNSTREAM (Prime Contractor designation interface) roles. Both edges are distinct information flows and are recorded separately.
- Permit fee exclusion (REQ-009-03-08) recorded as CONSTRAINT with EstimateImpactClass=BLOCKING because it directly affects estimating scope (Proponent must exclude these costs).
- Construction Phase gate recorded with TargetType=UNKNOWN because "Construction Phase" is not a single deliverable or package in the decomposition; it spans multiple packages.

---

## Run History

| Run | Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | ACTIVE Total |
|-----|-----------|------|------------|----------|---------------|----------|----------------|------------------|--------------|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | AVAILABLE (R1 2026-02-25) | None | 3 | 11 | 14 |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 14 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|--------------------|-------|
| PENDING | 7 |
| NOT_APPLICABLE | 4 |
| TBD | 3 |
| SATISFIED | 0 |
| IN_PROGRESS | 0 |
| WAIVED | 0 |

**Closure state breakdown (ACTIVE EXECUTION rows only):**
- PENDING: 7 (E01, E02, E03, E04, E05, E06, E10)
- TBD: 3 (E07, E08, E09)
- NOT_APPLICABLE: 1 (E11)

**Closure state breakdown (ACTIVE ANCHOR rows):**
- NOT_APPLICABLE: 3 (A01, A02, A03)

---

## Downstream Handoff Notes

**Consumer context: TASK_ESTIMATING**

The following observations are provided for downstream task-estimating workflows:

1. **BLOCKING dependencies (5 execution rows):**
   - **DEP-009-03-E01** (DEL-019-01 OH&S Plan): Scope of safety code audit depends on OH&S plan inputs. Estimating the audit effort requires understanding what OH&S scope is in play.
   - **DEP-009-03-E02** (Design Packages PKG-001 through PKG-007): Safety code permit categories and quantities cannot be finalized until design is sufficiently advanced. Estimating permit application effort is blocked until design package scope is known.
   - **DEP-009-03-E03** (SOW-0018 IFC Drawings): Permit applications requiring design documentation are blocked until IFC drawings are available. Estimating timeline for permit applications depends on IFC availability.
   - **DEP-009-03-E04** (CCDC 14-2013 Contract Execution): No permit activities can commence until contract award. This gates all estimating timeline assumptions.
   - **DEP-009-03-E11** (Permit Fee Exclusion): Proponent's cost estimate must explicitly exclude permit fees (County responsibility per RFP section 3.3.1). This is a scope exclusion that directly affects estimate totals.

2. **ADVISORY dependencies (4 execution rows):**
   - **DEP-009-03-E05** (Prime Contractor Designation Form): Form availability from County affects timing but not scope of estimate.
   - **DEP-009-03-E06** (County PM Availability): Inspection scheduling depends on County availability; affects timeline estimates for inspection phases.
   - **DEP-009-03-E07** (DEL-009-04 Handover): Downstream handover effort should be estimated for documentation transfer.
   - **DEP-009-03-E09** (DEL-019-01 Interface): Boundary between DEL-009-03 and DEL-019-01 for Prime Contractor designation needs clarification (Conflict C-009-03-02); may affect scope split in estimates.

3. **INFO dependency (1 execution row):**
   - **DEP-009-03-E10** (December 31, 2026 Deadline): Hard constraint on overall timeline. Informational for estimating -- does not change scope but constrains schedule.

4. **Key TBDs affecting estimating readiness:**
   - Number of permit categories is TBD pending safety code audit (Datasheet Attributes). This is a primary driver of permit application effort and inspection coordination effort.
   - Accredited agency identity is TBD (Datasheet Attributes). Agency-specific requirements and processing timelines affect effort estimates.
   - IFC drawing availability timeline is TBD (Specification REQ-009-03-11). This constrains the permit application schedule.

5. **Construction Phase gate (DEP-009-03-E08):** Safety Code Permits are a construction gate. Any delay in obtaining permits directly compresses the construction window and has cascading schedule risk across all construction packages.
