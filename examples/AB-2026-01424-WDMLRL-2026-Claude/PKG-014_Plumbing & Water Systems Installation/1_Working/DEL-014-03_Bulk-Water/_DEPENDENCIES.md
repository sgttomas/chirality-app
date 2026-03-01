# DEL-014-03_Bulk-Water Dependencies

## Dependency Status
**Tracking**: ACTIVE
**Register Schema Version**: v3.1

## Upstream Dependencies
- DEL-014-01: Cistern & Distribution (must be installed first; physical interface at cistern)
- Bulk water supply line assessment (external)

## Downstream Dependencies
- DEL-014-06: Plumbing Fixtures (water supply integration)

## Notes
Detailed dependency tracking managed within project execution framework.

---

## Extracted Dependency Register

**Total rows:** 12
**ACTIVE:** 12 | **RETIRED:** 0

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-014-03-001 | IMPLEMENTS_NODE | SOW-0044 | Install bulk water fill system with high-volume pump for external filling | HIGH | ACTIVE |
| DEP-014-03-002 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant fully functional maintenance shop addition | HIGH | ACTIVE |
| DEP-014-03-003 | TRACES_TO_REQUIREMENT | OBJ-004 | Install and commission all mechanical plumbing and water storage systems | HIGH | ACTIVE |

### EXECUTION Rows (9 ACTIVE)

| DependencyID | Direction | DependencyType | TargetDeliverableID | TargetName | Confidence | Status | EstimateImpactClass |
|---|---|---|---|---|---|---|---|
| DEP-014-03-004 | UPSTREAM | PREREQUISITE | DEL-006-04 | Cistern & Pump Details (IFC Drawings) | HIGH | ACTIVE | BLOCKING |
| DEP-014-03-005 | UPSTREAM | PREREQUISITE | DEL-014-01 | 50,000L Cistern & Distribution | HIGH | ACTIVE | BLOCKING |
| DEP-014-03-006 | UPSTREAM | INTERFACE | DEL-015-04 | Equipment Power Circuits | HIGH | ACTIVE | ADVISORY |
| DEP-014-03-007 | UPSTREAM | CONSTRAINT | DEL-019-01 | Prime Contractor Designation & OH&S Program | HIGH | ACTIVE | INFO |
| DEP-014-03-008 | DOWNSTREAM | HANDOVER | DEL-020-01 | Building Systems Commissioning | HIGH | ACTIVE | ADVISORY |
| DEP-014-03-009 | UPSTREAM | INTERFACE | DEL-018-03 | Gravel Driving Surface | MEDIUM | ACTIVE | ADVISORY |
| DEP-014-03-010 | UPSTREAM | CONSTRAINT | (doc) R-01 | AB-2026-01424-WDMLRL RFP | HIGH | ACTIVE | INFO |
| DEP-014-03-011 | UPSTREAM | CONSTRAINT | (doc) R-06 | AB-2026-01424-Appendix B (Plumbing) | HIGH | ACTIVE | INFO |
| DEP-014-03-012 | DOWNSTREAM | INTERFACE | DEL-014-01 | 50,000L Cistern & Distribution | HIGH | ACTIVE | ADVISORY |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE | 12 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| PENDING | 7 |
| SATISFIED | 2 |
| NOT_APPLICABLE | 3 |

**Notes:**
- SATISFIED rows (DEP-014-03-010, DEP-014-03-011) are document constraints where the source documents have been received and requirements extracted.
- NOT_APPLICABLE rows (DEP-014-03-001, DEP-014-03-002, DEP-014-03-003) are the IMPLEMENTS_NODE anchor and two trace anchors to objectives; satisfaction is tracked at the definition/objective level, not the anchor level.

---

## Run Notes

**Run date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING
**Decomposition path:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md`
**Decomposition status:** AVAILABLE (R1, 2026-02-25)

### Defaults and Chosen Paths

| Setting | Value |
|---|---|
| SOURCE_DOCS | AUTO -- scanned deliverable folder; identified Datasheet.md, Guidance.md, Procedure.md, Specification.md |
| DOC_ROLE_MAP | DEFAULT heuristic applied |
| ANCHOR_DOC | Datasheet.md (matched on "datasheet" keyword; contains Identification table with SOW Reference and Objectives Supported) |
| EXECUTION_DOC_ORDER | Procedure.md (strongest execution signals: prerequisites table, step sequence), Guidance.md (considerations with cross-deliverable references), Specification.md (requirements with scope boundary and code citations) |
| _REFERENCES.md | Read; used for document target resolution (R-01, R-06) |

### Extraction Summary

- **Pass 1 (ANCHOR):** Extracted 1 IMPLEMENTS_NODE (SOW-0044) and 2 TRACES_TO_REQUIREMENT (OBJ-001, OBJ-004) from Datasheet.md Identification table. All confirmed against decomposition SSOW, S5, and S7.
- **Pass 2 (EXECUTION):** Extracted 9 execution edges from Procedure.md prerequisites table, Procedure.md steps, Guidance.md considerations, and Specification.md requirements. 7 UPSTREAM, 2 DOWNSTREAM.
- **Target resolution:** All deliverable targets resolved against decomposition S7. Document targets (R-01, R-06) resolved against _REFERENCES.md. No UNKNOWN targets.
- **Duplicate check:** DEL-014-01 appears in two rows (DEP-014-03-005 upstream prerequisite, DEP-014-03-012 downstream interface). These are distinct edges: the upstream edge captures the prerequisite that the cistern must be at rough-in stage before connection; the downstream edge captures the interface where DEL-014-03 delivers its fill line connection to the cistern. Justified and retained as separate rows.

### Warnings

No warnings. Parent anchor (IMPLEMENTS_NODE) present and unique. All evidence locations resolved.

### Items Not Extracted (with justification)

- **DEL-014-06 (Plumbing Fixtures):** Listed in _DEPENDENCIES.md declared downstream section. No explicit information/artifact transfer from DEL-014-03 to DEL-014-06 found in any source document. The declared relationship is preserved in the declared section above but no extracted row is emitted (CONSERVATIVE strictness; no evidence of information flow).
- **"Bulk water supply line assessment (external)":** Listed in _DEPENDENCIES.md declared upstream section. No concrete deliverable ID or evidence in source documents. Preserved in declared section.
- **DEL-014-01 overflow/level protection status (Procedure prerequisite):** This is an intra-prerequisite within the DEL-014-01 relationship, not a separate dependency edge. Covered by DEP-014-03-005 notes.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | AVAILABLE (R1) | None | 3 | 9 | 12 |

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Estimating-Critical Dependencies

The following dependencies are most relevant to task estimating readiness for DEL-014-03:

1. **DEP-014-03-004 (DEL-006-04 IFC Drawings) -- BLOCKING:** This is the most critical upstream dependency. The plumbing IFC design governs pump sizing, pipe sizing, connection type, freeze protection method, and backflow device type. Without IFC drawings, procurement cannot begin and multiple Datasheet attributes remain TBD (pump flow rate, fill connection size, pipe material, fill connection hardware, freeze protection details, backflow device type). Estimating without IFC completion requires significant contingency or parametric assumptions.

2. **DEP-014-03-005 (DEL-014-01 Cistern) -- BLOCKING:** The cistern must be at rough-in stage before the bulk fill line can be connected. This is a physical sequencing dependency that affects installation scheduling. For estimating, the cistern installation timeline directly constrains when DEL-014-03 work can proceed at the cistern interface.

3. **DEP-014-03-006 (DEL-015-04 Electrical) -- ADVISORY:** Electrical coordination must occur before rough-in. The pump motor specifications (voltage, phase, amperage) are TBD pending design. This dependency is unlikely to change total cost significantly but could affect scheduling if not coordinated early.

4. **DEP-014-03-009 (DEL-018-03 Gravel Driving Surface) -- ADVISORY:** Site access for water delivery vehicles must be coordinated with the fill point location. This is a layout/access coordination item that could affect fill point positioning or access route design.

### Unresolved Design TBDs Affecting Estimating

Multiple critical parameters remain TBD pending PKG-006 IFC design completion (see Guidance C-7):
- Pump flow rate (LPM) -- blocks pump selection and procurement cost
- Fill connection size and type -- blocks hardware procurement cost
- Freeze protection method -- blocks material procurement cost
- Backflow device type -- blocks device procurement cost
- Fill line pipe material -- blocks piping material cost

These items represent the primary source of estimating uncertainty for DEL-014-03. Early resolution through PKG-006 design completion is recommended.
