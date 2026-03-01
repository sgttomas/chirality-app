# _DEPENDENCIES.md
## DEL-009-01 | Development Permit Application & Approval

### Dependency Status
- **Tracking Status**: ACTIVE
- **Last Updated**: 2026-02-26
- **Owner**: Project Manager
- **Register Schema**: v3.1

---

### Upstream Dependencies (Inputs Required)
| Dependency | Source | Type | Status | Impact |
|------------|--------|------|--------|--------|
| Final RFP Requirements | R-01, R-02 | Document | NOT_STARTED | CRITICAL - Defines permit scope |
| Project Specifications | Project Charter | Document | NOT_STARTED | CRITICAL - Required for application |
| Regulatory Authority Contact | Regulatory Affairs | Information | NOT_STARTED | CRITICAL - Submission requirement |
| Development Standards | Legal/Compliance | Document | NOT_STARTED | HIGH - Defines compliance criteria |
| Budget Approval | Finance | Approval | NOT_STARTED | HIGH - Permit fees and contingency |

### Downstream Dependencies (Work Dependent on This)
| Dependent | Type | Relationship | Status |
|-----------|------|--------------|--------|
| DEL-009-02_Building-Permit | Deliverable | Sequential - Building permit follows development permit | BLOCKED |
| DEL-009-03_Safety-Code-Permits | Deliverable | Parallel - Coordinates with development permit conditions | BLOCKED |
| DEL-009-04_Code-Compliance-Register | Deliverable | Tracking - Logs all permit conditions | BLOCKED |

### External Dependencies
| Entity | Dependency | Status |
|--------|-----------|--------|
| Regulatory Authority | Permit processing timeline | PENDING |
| Legal Department | Regulatory interpretation | PENDING |
| Finance Department | Budget authorization | PENDING |

### Constraint Dependencies
- Project schedule start date (TBD)
- Regulatory authority processing SLAs (TBD)
- Client approval authority (TBD)

### Risk Dependencies
- Regulatory authority changes (external risk)
- Additional permit requirements discovered (external risk)
- Budget constraints (internal risk)

### Notes
- All dependencies marked as NOT_TRACKED pending project initialization
- Dependencies will be updated as project schedule is finalized
- Critical path analysis pending SOW-0005 detailed planning

---

## Extracted Dependency Register

**Source:** `Dependencies.csv` (v3.1)
**Total ACTIVE rows:** 16
**Total RETIRED rows:** 0

### ANCHOR rows (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID / TargetName | Confidence | Notes |
|---|---|---|---|---|
| DEP-009-01-001 | IMPLEMENTS_NODE | SOW-0005 | HIGH | FACT. Parent anchor confirmed in Decomposition Scope Ledger. |
| DEP-009-01-002 | TRACES_TO_REQUIREMENT | OBJ-001 | MEDIUM | ASSUMPTION. Via PKG-009 grouping. |
| DEP-009-01-003 | TRACES_TO_REQUIREMENT | OBJ-002 | MEDIUM | ASSUMPTION. Via PKG-009 grouping. |

### EXECUTION rows (13 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-009-01-004 | UPSTREAM | PREREQUISITE | DOCUMENT | R-01 (RFP) | HIGH | BLOCKING |
| DEP-009-01-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | HIGH | BLOCKING |
| DEP-009-01-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-01 Preliminary Structural Design | HIGH | BLOCKING |
| DEP-009-01-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-003-01 Preliminary Mechanical Design | MEDIUM | ADVISORY |
| DEP-009-01-008 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-004-01 Preliminary Electrical Design | MEDIUM | ADVISORY |
| DEP-009-01-009 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-005-01 Preliminary Civil Design | HIGH | BLOCKING |
| DEP-009-01-010 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-006-01 Preliminary Plumbing Design | MEDIUM | ADVISORY |
| DEP-009-01-011 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-007-01 Preliminary Landscape Design | MEDIUM | ADVISORY |
| DEP-009-01-012 | UPSTREAM | CONSTRAINT | EXTERNAL | Camrose County Permitting Authority | HIGH | BLOCKING |
| DEP-009-01-013 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-02 Building Permit | HIGH | BLOCKING |
| DEP-009-01-014 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-009-03 Safety Code Permits | MEDIUM | ADVISORY |
| DEP-009-01-015 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-04 Code Compliance Register | HIGH | BLOCKING |
| DEP-009-01-016 | UPSTREAM | PREREQUISITE | DOCUMENT | P.Eng. Stamped IFC Drawings | HIGH | ADVISORY |

---

## Run Notes

### Defaults and Paths Used
- **SCOPE:** DEL-009-01
- **RUN_ROOT:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (found and used)
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS (AUTO):** Datasheet.md, Guidance.md, Procedure.md, Specification.md
- **DOC_ROLE_MAP (DEFAULT):**
  - ANCHOR_DOC: Datasheet.md (matched: `datasheet`)
  - EXECUTION_DOCS: Procedure.md (primary), Guidance.md, Specification.md
- **ANCHOR_DOC:** Datasheet.md
- **EXECUTION_DOC_ORDER:** Procedure.md, Guidance.md, Specification.md
- **_REFERENCES.md:** Present; used for document pointer resolution.

### Assumptions and Warnings
- Decomposition located and used for anchor validation and target resolution.
- No `[WARNING] MISSING_DECOMPOSITION` required.
- Parent anchor (IMPLEMENTS_NODE) found: exactly 1 (SOW-0005). No FLOATING_NODE or AMBIGUOUS_ANCHOR warnings.
- OBJ-001 and OBJ-002 traces confirmed in Decomposition Scope Ledger at PKG/deliverable level but Datasheet itself labels these as ASSUMPTION-level associations. Recorded as MEDIUM confidence.
- Design package prerequisites (DEL-001-01 through DEL-007-01): source collectively references "PKG-001 through PKG-007." Individual rows created per package for traceability. Architectural (PKG-001), Structural (PKG-002), and Civil (PKG-005) designs are HIGH confidence (site plan, footprint, building description are explicitly required per Procedure Step 3.1). Mechanical, Electrical, Plumbing, and Landscape designs are MEDIUM confidence with ASSUMPTION label because their specific relevance to a development permit application (vs. building permit) is not confirmed in sources.
- P.Eng. IFC stamp requirement (DEP-009-01-016): included because Guidance P-5 explicitly cites it as a constraint for permit submissions citing R-01 s3.3.2. Classified as ADVISORY for estimating because it applies to IFC-level drawings which may be a later-stage requirement than the development permit application itself.
- No rows were emitted for "Budget Approval" or "Legal Department" external dependencies from the declared section because these do not represent explicit information-flow or artifact-transfer edges stated in the source documents; they are coordination/administrative dependencies.

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomp Status | Warnings | ACTIVE Anchors | ACTIVE Execution | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Located and used | None | 3 | 13 | Initial extraction run. 16 total ACTIVE rows. |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 16 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 16 |
| PENDING | 0 |
| IN_PROGRESS | 0 |
| SATISFIED | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |

---

## Downstream Handoff Notes (CONSUMER_CONTEXT: TASK_ESTIMATING)

The following observations are relevant to downstream task estimating workflows:

1. **BLOCKING upstream prerequisites (5 items):** The RFP document (R-01), three design deliverables (DEL-001-01 Architectural, DEL-002-01 Structural, DEL-005-01 Civil), and Camrose County Permitting Authority contact/requirements resolution are classified as BLOCKING for estimating. Without these, the scope, content, and timeline of the development permit application cannot be reliably estimated.

2. **ADVISORY upstream prerequisites (5 items):** Mechanical (DEL-003-01), Electrical (DEL-004-01), Plumbing (DEL-006-01), and Landscape (DEL-007-01) preliminary designs, plus the P.Eng. IFC stamp requirement, are classified as ADVISORY. These may or may not be required specifically for the development permit (vs. building permit); the authority's specific requirements are TBD. They are unlikely to change the overall estimate significantly but may affect scope.

3. **BLOCKING downstream handovers (2 items):** DEL-009-02 (Building Permit) and DEL-009-04 (Code Compliance Register) depend on outputs from this deliverable. Estimating for those deliverables should account for the sequential dependency.

4. **Key TBD items affecting estimating readiness:** The Camrose County permitting authority's application form, processing timeline, and specific requirements are all TBD. These directly affect the effort estimate for application preparation and the duration estimate for the review period. Resolution of these TBDs (via pre-application consultation per Procedure Step 1.3) is a precondition for reliable estimating of this deliverable.

5. **External constraint (BLOCKING):** The regulatory authority's processing timeline is a schedule constraint that cannot be influenced by the Proponent and is currently unknown. This is the single largest source of duration uncertainty for this deliverable.
