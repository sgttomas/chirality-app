# _DEPENDENCIES.md
## DEL-009-02 | Building Permit Application & Approval

### Dependency Status
- **Tracking Status**: TRACKED
- **Last Updated**: 2026-02-26
- **Owner**: Project Manager

### Upstream Dependencies (Inputs Required)
| Dependency | Source | Type | Status | Impact |
|------------|--------|------|--------|--------|
| DEL-009-01 Completion | Development Permit | Deliverable | NOT_STARTED | CRITICAL - Sequential predecessor |
| Design Documentation | Design Team | Document | NOT_STARTED | CRITICAL - Required for application |
| Building Authority Standards | Regulatory Authority | Document | NOT_STARTED | CRITICAL - Defines compliance criteria |
| Development Permit Conditions | DEL-009-01 | Document | NOT_STARTED | HIGH - Conditions flow into building permit |
| Budget Approval | Finance | Approval | NOT_STARTED | HIGH - Permit fees and contingency |

### Downstream Dependencies (Work Dependent on This)
| Dependent | Type | Relationship | Status |
|-----------|------|--------------|--------|
| Construction Phase | Project Phase | Gate - Building permit required before construction | BLOCKED |
| DEL-009-04_Code-Compliance-Register | Deliverable | Tracking - Logs all permit conditions | BLOCKED |
| Inspection Schedule | Project Phase | Depends on - Inspection conditions from permit | BLOCKED |

### External Dependencies
| Entity | Dependency | Status |
|--------|-----------|--------|
| Building Authority | Permit processing timeline | PENDING |
| Design Team | Final design documentation | PENDING |
| Development Authority | Development permit approval | PENDING |

### Constraint Dependencies
- Project schedule phases (TBD)
- Building authority processing SLAs (TBD)
- Construction start date (TBD)
- Design finalization date (TBD)

### Risk Dependencies
- Regulatory authority design interpretation disputes (external risk)
- Design non-compliance with building code (internal risk)
- Delayed design finalization (internal risk)
- Building authority staffing delays (external risk)

### Notes
- Sequential dependency on DEL-009-01 critical for project timeline
- Design finalization is critical path item
- Building permit triggers construction phase commencement
- All dependencies marked as NOT_TRACKED pending project initialization

---

## Extracted Dependency Register

**Register file:** `Dependencies.csv` (Schema v3.1)
**Total rows:** 9 | **ACTIVE:** 9 | **RETIRED:** 0

### ANCHOR Rows (3)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-009-02-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0006: Obtain building permit from the County | HIGH |
| DEP-009-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001: Regulatory-Compliant Delivery | HIGH |
| DEP-009-02-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002: Schedule (Complete by Dec 31 2026) | HIGH |

### EXECUTION Rows (6)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-009-02-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-009-01: Development Permit | HIGH | BLOCKING |
| DEP-009-02-005 | UPSTREAM | PREREQUISITE | DOCUMENT | IFC Drawing Set (all disciplines) stamped by P.Eng. | HIGH | BLOCKING |
| DEP-009-02-006 | UPSTREAM | PREREQUISITE | EXTERNAL | Camrose County Building Authority -- Application Requirements | HIGH | BLOCKING |
| DEP-009-02-007 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-04: Code Compliance Register & Inspection Log | HIGH | ADVISORY |
| DEP-009-02-008 | DOWNSTREAM | ENABLES | UNKNOWN | Construction Phase (PKG-010 through PKG-018) | HIGH | BLOCKING |
| DEP-009-02-009 | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta Building Codes and Safety Codes | HIGH | ADVISORY |

---

## Run Notes

**Run date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

### Paths and defaults used
- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- **DECOMPOSITION_PATH:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (provided; validated -- DEL-009-02 confirmed in decomposition §7 PKG-009 table and §8 Scope Ledger)
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder, identified 4 source documents: `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md`
- **DOC_ROLE_MAP:** DEFAULT heuristic applied
- **ANCHOR_DOC:** `Datasheet.md` (AUTO -- matched `datasheet` pattern; highest traceability signal)
- **EXECUTION_DOC_ORDER:** `Procedure.md`, `Guidance.md`, `Specification.md` (AUTO -- `procedure` matched first, then `guidance`, then `spec`)
- **_REFERENCES.md:** Present; used for document pointer resolution (limited -- most regulatory references listed as TBD)

### Assumptions
- OBJ-001 and OBJ-002 trace anchors are based on explicit text in Datasheet.md and confirmed against decomposition §7 and §9. These objectives are treated as REQUIREMENT-type targets because they are definition-level nodes that this deliverable traces to.
- IFC Drawing Set dependency (DEP-009-02-005) is recorded as a single composite DOCUMENT row rather than six separate package-level rows. The Procedure Step 4 explicitly enumerates PKG-001 through PKG-006 as discipline sources; these are noted in the row but not individually split. Under CONSERVATIVE strictness, a single composite row reduces false precision.
- Construction Phase downstream gate (DEP-009-02-008) uses TargetType=UNKNOWN because the target spans multiple packages (PKG-010 through PKG-018) and no single deliverable is the recipient. The text is explicit that the permit is a hard gate for the entire construction phase.
- DEL-009-03 (Safety Code Permits) was evaluated as a potential dependency. Under CONSERVATIVE strictness, the relationship is characterized as coordination/clarification (Guidance says "clarify relationship"), not an explicit information transfer or prerequisite. Not extracted. If future evidence surfaces an explicit information flow, it should be added.

### Warnings
- None. All quality checks passed.

---

## Run History

| Run Date | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Notes |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Available (validated) | None | 3 | 6 | Initial extraction. CONSUMER_CONTEXT=TASK_ESTIMATING. |

---

## Lifecycle Summary

**Extraction lifecycle:**
- ACTIVE: 9
- RETIRED: 0

**Closure lifecycle (SatisfactionStatus breakdown, ACTIVE rows only):**
- TBD: 5 (DEP-009-02-001, DEP-009-02-002, DEP-009-02-003, DEP-009-02-007, DEP-009-02-008)
- PENDING: 4 (DEP-009-02-004, DEP-009-02-005, DEP-009-02-006, DEP-009-02-009)
- IN_PROGRESS: 0
- SATISFIED: 0
- WAIVED: 0
- NOT_APPLICABLE: 0

**Tree x DAG integrity:**
- Parent anchor (IMPLEMENTS_NODE): 1 (SOW-0006) -- OK
- Trace anchors (TRACES_TO_REQUIREMENT): 2 (OBJ-001, OBJ-002) -- OK

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Estimating-relevant observations

1. **Three BLOCKING upstream prerequisites** gate this deliverable's execution:
   - **DEP-009-02-004** (DEL-009-01 Development Permit): Hard sequential gate. Estimating cannot finalize DEL-009-02 timeline without an estimate of DEL-009-01 duration and approval date.
   - **DEP-009-02-005** (IFC Drawing Set): All six design discipline packages (PKG-001 through PKG-006) must produce complete, P.Eng.-stamped IFC drawings before application assembly can begin. This is the primary schedule risk for DEL-009-02.
   - **DEP-009-02-006** (Camrose County Building Authority -- application requirements): External dependency; forms and submission requirements must be obtained from the authority. Processing timeline is TBD (Datasheet notes 4-12 week ASSUMPTION range for Alberta municipal processing -- not Camrose-specific).

2. **One BLOCKING downstream gate** affects estimating of all construction packages:
   - **DEP-009-02-008** (Construction Phase PKG-010 through PKG-018): Building permit is a hard gate before construction may commence. Any delay in DEL-009-02 directly compresses the available construction window against the December 31, 2026 deadline.

3. **One ADVISORY downstream handover:**
   - **DEP-009-02-007** (DEL-009-04 Code Compliance Register): Permit conditions flow into DEL-009-04. Conditions may impose additional inspection hold points or specialized material requirements that affect construction estimates.

4. **One ADVISORY upstream constraint:**
   - **DEP-009-02-009** (Alberta Building Codes and Safety Codes): Compliance constraint. Specific code editions TBD. May affect design scope and thus indirectly affect estimating of design packages.

5. **Key TBDs affecting estimating readiness:**
   - Camrose County building authority processing timeline (best/expected/worst case)
   - Specific Alberta code editions and application form requirements
   - Whether building permit and Safety Code permits (DEL-009-03) are submitted together or separately (CONF-009-02-01 and CONF-009-02-02 unresolved)
