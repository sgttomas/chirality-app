# DEL-019-04: Dependencies

**Deliverable ID:** DEL-019-04_QC-Management
**Dependency Tracking Status:** TRACKED
**Register Schema:** v3.1

## Upstream Dependencies
- **DEL-019-01** (Prime-Contractor): QC authority structure established under prime contractor oversight
- **DEL-019-02** (Weekly-Coordination): QC status and deficiency reports presented in weekly meetings
- **DEL-019-03** (Subcontractor-Mgmt): QC activities inform subcontractor performance evaluations

## Internal Package Dependencies
None identified beyond upstream dependencies.

## External Package Dependencies
- **PKG-020** (Commissioning & Closeout): QC activities transition to commissioning and closeout phases

## Cross-Project Dependencies
None currently identified.

## Dependency Notes
Quality control is integrated throughout PKG-019 management activities. QC results inform subcontractor performance evaluations and are reported in weekly coordination meetings. Transition to commissioning (PKG-020) requires completion of construction QC activities.

## Monitoring
Dependencies will be monitored through weekly coordination meetings and QC status reports.

---

## Extracted Dependency Register

**Total rows:** 11 (11 ACTIVE, 0 RETIRED)

### ANCHOR edges (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-019-04-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0089 | SOW-0089 -- Provide construction quality control management | HIGH |
| DEP-019-04-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | OBJ-001 -- Design & Specification Compliance | HIGH |
| DEP-019-04-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-007 | OBJ-007 -- OH&S Program Implementation | HIGH |

### EXECUTION edges (8 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-019-04-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-019-01 -- Prime Contractor Designation & OH&S Program | HIGH | BLOCKING |
| DEP-019-04-005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-019-02 -- Weekly Meetings & Billing Coordination | HIGH | ADVISORY |
| DEP-019-04-006 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-019-03 -- Subcontractor Management | HIGH | ADVISORY |
| DEP-019-04-007 | DOWNSTREAM | HANDOVER | PACKAGE | PKG-020 -- Commissioning & Closeout | HIGH | BLOCKING |
| DEP-019-04-008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-009-04 -- Code Compliance Register & Inspection Log | MEDIUM | ADVISORY |
| DEP-019-04-009 | UPSTREAM | PREREQUISITE | DOCUMENT | IFC Drawings (Issued for Construction) | HIGH | BLOCKING |
| DEP-019-04-010 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 Design-Build Stipulated Price Contract | HIGH | ADVISORY |
| DEP-019-04-011 | UPSTREAM | CONSTRAINT | DOCUMENT | AB-2026-01424-WDMLRL RFP.pdf | HIGH | BLOCKING |

---

## Run Notes

**Run date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

### Paths and defaults used

| Setting | Value | Resolution |
|---|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude | Provided by invoker |
| DECOMPOSITION_PATH | _Decomposition/WDMLRL_Decomposition_Claude.md | Provided by invoker; file found and used |
| SOURCE_DOCS | AUTO | Resolved to: Datasheet.md, Specification.md, Guidance.md, Procedure.md |
| DOC_ROLE_MAP | DEFAULT heuristic | Applied |
| ANCHOR_DOC | Datasheet.md | AUTO: highest-confidence match (contains "datasheet", has Identification table with SOW/OBJ references) |
| EXECUTION_DOC_ORDER | Procedure.md, Guidance.md, Specification.md, Datasheet.md | AUTO: Procedure has explicit prerequisites section; Guidance has considerations/interface sections; Specification has requirements; Datasheet has attribute/condition tables |
| _REFERENCES.md | Present; used for RFP document pointer resolution (R-01) | Read-only |

### Extraction notes

- **Pass 1 (ANCHOR):** 3 anchors extracted from Datasheet.md Identification table. All explicit. 1 parent anchor (SOW-0089 via "Covers SOW" field), 2 trace anchors (OBJ-001, OBJ-007 via "Supports Objectives" field). All confirmed against decomposition scope ledger and deliverable table.
- **Pass 2 (EXECUTION):** 8 execution edges extracted across all four source documents. 4 deliverable-to-deliverable (DEL-019-01, DEL-019-02, DEL-019-03, DEL-009-04), 1 deliverable-to-package (PKG-020), 3 document dependencies (IFC Drawings, CCDC 14-2013, RFP). All explicit in source text.
- **Decomposition validation:** Decomposition file located and used for anchor validation and target ID resolution. All referenced deliverable IDs (DEL-019-01, DEL-019-02, DEL-019-03, DEL-009-04), package IDs (PKG-019, PKG-020, PKG-009), and SSOW/objective IDs (SOW-0089, OBJ-001, OBJ-007) confirmed present in decomposition.
- **Parent anchor check:** PASSED (exactly 1 IMPLEMENTS_NODE).
- **Extension columns:** EstimateImpactClass and ConsumerHint populated for all EXECUTION rows per CONSUMER_CONTEXT=TASK_ESTIMATING. 4 rows BLOCKING, 4 rows ADVISORY. No rows marked INFO or TBD (all had sufficient evidence).

### Warnings

None.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (found, used) | None | 3 | 8 | 11 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 11 |
| RETIRED | 0 |

### Satisfaction status breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 6 |
| PENDING | 5 |

### Confidence breakdown (ACTIVE rows)

| Confidence | Count |
|---|---|
| HIGH | 10 |
| MEDIUM | 1 |

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Estimating-relevant summary

This deliverable (DEL-019-04: Construction Quality Control) has **4 BLOCKING dependencies** that gate meaningful estimating:

1. **DEP-019-04-004 (BLOCKING):** DEL-019-01 (Prime Contractor Designation & OH&S Program) must be established before the QC authority structure and program scope can be confirmed. Without this, the QC Manager role definition, escalation paths, and oversight structure are undefined -- affecting effort and resource estimation.

2. **DEP-019-04-007 (BLOCKING):** PKG-020 (Commissioning & Closeout) requires completed QC activities and full QC documentation package before CCC can be issued. This downstream gate means QC scope must be fully estimated to understand the critical path to project completion.

3. **DEP-019-04-009 (BLOCKING):** IFC Drawings are required before each construction phase inspection can proceed. Until IFC drawings are available, the specific testing protocols, acceptance criteria, and inspection scope cannot be defined -- directly affecting QC effort estimation for materials testing and inspection frequency.

4. **DEP-019-04-011 (BLOCKING):** The RFP (AB-2026-01424-WDMLRL RFP.pdf) is the primary governing document defining all QC requirements. It is available and referenced extensively, so this dependency is satisfied for estimating purposes (SatisfactionStatus=PENDING indicates the relationship is tracked, not that the document is missing).

### Advisory dependencies for estimating awareness

- **DEP-019-04-005 (ADVISORY):** Weekly meeting cadence (DEL-019-02) is the QC reporting forum. Does not gate QC scope definition but affects ongoing resource allocation for reporting.
- **DEP-019-04-006 (ADVISORY):** QC data flows to subcontractor performance evaluations (DEL-019-03). Affects scope of documentation but not core QC program estimation.
- **DEP-019-04-008 (ADVISORY):** Interface with DEL-009-04 (Code Compliance Register) needed to align QC hold points with Safety Code inspection points. May affect inspection scheduling but not fundamental QC scope.
- **DEP-019-04-010 (ADVISORY):** CCDC 14-2013 contract defines QC-related provisions. Contract form is known (RFP 2.7) but specific QC clauses not yet verified against contract text. Unlikely to change total QC scope but may affect specific obligations.
