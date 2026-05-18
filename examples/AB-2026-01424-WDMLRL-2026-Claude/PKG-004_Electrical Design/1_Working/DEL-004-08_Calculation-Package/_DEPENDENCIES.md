# Dependencies: DEL-004-08 Electrical Calculation Package

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema)
- **Total rows:** 20
- **ACTIVE:** 20
- **RETIRED:** 0

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-004-08-A01 | IMPLEMENTS_NODE | SOW-0014 | Complete final electrical design (three-phase power distribution; lighting; receptacles) | HIGH |
| DEP-004-08-A02 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-004-08-A03 | TRACES_TO_REQUIREMENT | OBJ-005 | Install and commission all electrical and low-voltage systems | HIGH |

### EXECUTION Edges -- UPSTREAM (10 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | SatisfactionStatus | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-004-08-E01 | PREREQUISITE | DOCUMENT | AB-2026-01424-WDMLRL RFP.pdf | SATISFIED | INFO |
| DEP-004-08-E02 | PREREQUISITE | DOCUMENT | AB-2026-01424-Appendix B (Electrical).pdf | SATISFIED | INFO |
| DEP-004-08-E03 | PREREQUISITE | EXTERNAL | Canadian Electrical Code Part I (current Alberta adopted edition) | PENDING | BLOCKING |
| DEP-004-08-E04 | PREREQUISITE | EXTERNAL | Alberta Safety Code requirements (Electrical) | PENDING | ADVISORY |
| DEP-004-08-E05 | PREREQUISITE | PACKAGE | PKG-016 Crane and Lifting Equipment | PENDING | BLOCKING |
| DEP-004-08-E06 | PREREQUISITE | EXTERNAL | County welding equipment specifications | PENDING | BLOCKING |
| DEP-004-08-E07 | INTERFACE | PACKAGE | PKG-003 Mechanical Design | PENDING | BLOCKING |
| DEP-004-08-E08 | PREREQUISITE | DELIVERABLE | DEL-001-07 Door and Window Schedule | PENDING | ADVISORY |
| DEP-004-08-E09 | PREREQUISITE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | PENDING | ADVISORY |
| DEP-004-08-E10 | PREREQUISITE | EXTERNAL | Utility three-phase service voltage confirmation | PENDING | BLOCKING |

### EXECUTION Edges -- DOWNSTREAM (7 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | SatisfactionStatus | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-004-08-E11 | HANDOVER | DELIVERABLE | DEL-004-02 Single-Line Diagram | TBD | ADVISORY |
| DEP-004-08-E12 | HANDOVER | DELIVERABLE | DEL-004-03 Power Distribution Plans | TBD | ADVISORY |
| DEP-004-08-E13 | HANDOVER | DELIVERABLE | DEL-004-04 Lighting Plans | TBD | ADVISORY |
| DEP-004-08-E14 | HANDOVER | DELIVERABLE | DEL-004-05 Receptacle Layout Plans | TBD | ADVISORY |
| DEP-004-08-E15 | HANDOVER | DELIVERABLE | DEL-004-06 Panel Schedules | TBD | BLOCKING |
| DEP-004-08-E16 | HANDOVER | DELIVERABLE | DEL-004-09 Electrical Specification | TBD | ADVISORY |
| DEP-004-08-E17 | CONSTRAINT | PACKAGE | PKG-009 Permitting and Regulatory Compliance | TBD | BLOCKING |

---

## Run Notes

### Defaults and Paths Used
- **SCOPE:** DEL-004-08_Calculation-Package
- **RUN_ROOT:** `/PKG-004_Electrical Design/1_Working/DEL-004-08_Calculation-Package/`
- **DECOMPOSITION_PATH:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25) -- AVAILABLE, used for anchor validation and label resolution
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS:** AUTO -- resolved to: `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md`
- **ANCHOR_DOC:** AUTO -- resolved to: `Datasheet.md` (highest-confidence match: contains "datasheet", has explicit identification fields with WBS/SOW/OBJ IDs)
- **EXECUTION_DOC_ORDER:** AUTO -- resolved to: `Procedure.md` (primary execution doc, contains Prerequisites table and Steps), `Guidance.md` (supporting context), `Specification.md` (requirements and related deliverables)
- **_REFERENCES.md:** Present -- used for document target resolution (R-01, R-05 locations confirmed)

### Assumptions
- ANCHOR parent node set to SOW-0014 (the primary scope item assigned to DEL-004-08 in decomposition). This is the most specific parent identifier available. PKG-004 is the package container but SOW-0014 is the work-scope node.
- Mechanical data interface (DEP-004-08-E07) consolidated into a single PKG-003 INTERFACE row rather than four separate rows, because the source groups all mechanical inputs under one coordination scope (PKG-003) and the information flow is a single package-level interface.
- EstimateImpactClass populated conservatively per CONSUMER_CONTEXT=TASK_ESTIMATING. BLOCKING used only for items that gate scope definition or key quantity determination.

### Warnings
- None. All quality checks passed.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | ACTIVE Total |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (R1) -- Available | None | 3 | 17 | 20 |

---

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 20
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown, ACTIVE rows only)
- **SATISFIED:** 2 (DEP-004-08-E01, DEP-004-08-E02 -- source documents already available)
- **PENDING:** 8 (upstream inputs awaiting receipt/confirmation)
- **TBD:** 7 (downstream handover/constraint -- satisfaction depends on this deliverable's completion)
- **NOT_APPLICABLE:** 3 (ANCHOR rows -- anchors do not have closure semantics)

### Estimating Readiness (CONSUMER_CONTEXT=TASK_ESTIMATING)
- **BLOCKING upstream dependencies:** 5 (CEC edition, crane data from PKG-016, welding specs from County, mechanical data from PKG-003, utility voltage confirmation)
- **ADVISORY upstream dependencies:** 3 (Alberta Safety Codes, overhead door data from DEL-001-07, floor plans from DEL-001-02)
- **Key estimating risk:** Crane manufacturer electrical data (DEP-004-08-E05) is identified as the single most critical missing data point. It affects service entrance sizing, dedicated circuit calculations, voltage drop, and panel schedules. Without it, the total connected/demand load cannot be finalized, which propagates uncertainty to all downstream deliverables.

---

## Downstream Handoff Notes (CONSUMER_CONTEXT: TASK_ESTIMATING)

### For Task Estimating Consumers

**Estimating-blocking dependencies (5):**
These upstream inputs must be resolved before the calculation package scope and quantities can be considered stable for estimating purposes:

1. **DEP-004-08-E03 -- Canadian Electrical Code, Part I:** Without the confirmed CEC edition, conductor sizing rules, demand factors, and voltage drop limits cannot be anchored to an authoritative code text. This affects all circuit sizing calculations.

2. **DEP-004-08-E05 -- Crane manufacturer electrical data (PKG-016):** The two 5-tonne overhead cranes are the most demanding specialized loads. Without manufacturer FLA/voltage/phase data, the service entrance sizing calculation cannot be finalized. This is the single highest-impact data gap.

3. **DEP-004-08-E06 -- County welding equipment specifications:** The 50A/240V rating is currently an assumption (D-009). If County welding equipment requires different ratings, it would change receptacle circuit sizing and potentially panel capacity.

4. **DEP-004-08-E07 -- Mechanical equipment data (PKG-003):** Heating system, MUA, exhaust fans, and ceiling fan electrical data are all TBD. These loads contribute to the total connected load and affect service entrance sizing.

5. **DEP-004-08-E10 -- Utility service voltage confirmation:** The system voltage (120/208V vs 347/600V) affects the entire electrical design architecture. This must be confirmed before any meaningful estimating of electrical scope.

**Estimating-advisory dependencies (3):**
These inputs affect specific calculation sections but are unlikely to change the overall scope/quantity envelope materially:

6. **DEP-004-08-E04 -- Alberta Safety Codes:** Regulatory requirements that constrain design but are unlikely to change total quantities significantly.

7. **DEP-004-08-E08 -- Overhead door data (DEL-001-07):** Affects a limited number of circuits; assumed values are within typical range.

8. **DEP-004-08-E09 -- Architectural floor plans (DEL-001-02):** Conceptual dimensions available (130'x100') are adequate for preliminary estimating; confirmed plans needed for final calculations only.

**Downstream propagation note:** DEL-004-08 is a critical-path design deliverable. Its outputs feed 6 drawing deliverables (DEL-004-02 through DEL-004-06, DEL-004-09) and the permitting package (PKG-009). Delays in resolving upstream blocking dependencies will propagate to all downstream electrical IFC deliverables and the Safety Code permit application.
