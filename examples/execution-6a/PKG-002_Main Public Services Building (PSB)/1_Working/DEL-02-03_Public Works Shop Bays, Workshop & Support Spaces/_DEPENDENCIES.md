# Dependencies: DEL-02-03 Public Works Shop Bays, Workshop & Support Spaces

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETED
- **Dependencies.csv:** `Dependencies.csv` (17 rows; schema v3.1)
- **Last Run:** 2026-02-17
- **Summary:** 17 ACTIVE rows (1 ANCHOR/IMPLEMENTS_NODE, 4 ANCHOR/TRACES_TO_REQUIREMENT, 12 EXECUTION); 0 RETIRED rows.

### ANCHOR Dependencies (5 rows)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-0203-001 | IMPLEMENTS_NODE | OBJ-003 | OBJ-003: Provide operationally functional Public Works facilities | HIGH |
| DEP-0203-002 | TRACES_TO_REQUIREMENT | SOW-0209 | SOW-0209: Provide PW PPE room and locker room | HIGH |
| DEP-0203-003 | TRACES_TO_REQUIREMENT | SOW-0210 | SOW-0210: Provide PW shop side including shop office and washroom | HIGH |
| DEP-0203-004 | TRACES_TO_REQUIREMENT | SOW-0211 | SOW-0211: Provide four PW drive-through shop bays | HIGH |
| DEP-0203-005 | TRACES_TO_REQUIREMENT | SOW-0212 | SOW-0212: Provide workshop area and warehouse/storage | HIGH |

### EXECUTION Dependencies (12 rows)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-0203-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01: Architectural Program Layout & Code Planning | HIGH |
| DEP-0203-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-04: Structure Envelope Roof & Overhead Doors | HIGH |
| DEP-0203-008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-05: Mechanical Plumbing Ventilation & Exhaust | HIGH |
| DEP-0203-009 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-06: Electrical Power Lighting IT-Telecom & PA | HIGH |
| DEP-0203-010 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-07: Emergency Power & Backup Generator | MEDIUM |
| DEP-0203-011 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-05-01: Option - Built-in Wash Bay | HIGH |
| DEP-0203-012 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP 2024_004 (including OSR and Functional Program) | HIGH |
| DEP-0203-013 | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 03 (July 31 2024) | HIGH |
| DEP-0203-014 | UPSTREAM | CONSTRAINT | EXTERNAL | Owner scope selections (wash bay option SOW-0500) | HIGH |
| DEP-0203-015 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-01: Integrated Design Management & Submission Packages | MEDIUM |
| DEP-0203-016 | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta Building Code (ABC) | HIGH |
| DEP-0203-017 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Investigation Report (Appendix D to RFP) | MEDIUM |

## Run Notes

### Run 2026-02-17 (Initial Extraction)

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: AUTO (resolved: Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved: Procedure.md, Specification.md, Guidance.md)
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (AVAILABLE; validation performed)

**Defaults and Assumptions:**
- ANCHOR_DOC selected as Datasheet.md based on presence of Identification table with explicit Scope Items, Objective, and Package references.
- EXECUTION_DOC_ORDER prioritized Procedure.md (contains explicit Prerequisites section and Step-by-step workflow references), then Specification.md (contains requirements with explicit cross-deliverable interfaces), then Guidance.md (contains Considerations and Trade-offs with interface context).
- All deliverable and scope item IDs validated against decomposition document.

**Observations:**
- DEL-02-03 has a rich interface network with four other PKG-002 deliverables (DEL-02-01, DEL-02-04, DEL-02-05, DEL-02-06) plus DEL-02-07 and one PKG-005 deliverable (DEL-05-01).
- Interfaces with DEL-02-04, DEL-02-05, and DEL-02-06 are bidirectional (DEL-02-03 provides spatial framework; those deliverables provide discipline-specific design data back). Rows captured as UPSTREAM/INTERFACE from DEL-02-03's perspective since DEL-02-03 needs their data to finalize layouts.
- The Owner's post-award wash bay decision (SOW-0500) is captured as an explicit CONSTRAINT from an EXTERNAL source because it gates the final bay count determination.
- ABC is captured as an EXTERNAL CONSTRAINT given multiple specification requirements explicitly require compliance (accessibility, fire separation, fixture counts).

**Warnings:** None.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Available (v1.0 Phase 7) | None | 5 | 12 | 17 |

## Lifecycle Summary

**Extraction Lifecycle:**
- ACTIVE: 17
- RETIRED: 0

**Closure Lifecycle (SatisfactionStatus breakdown for ACTIVE rows):**
- TBD: 17
- PENDING: 0
- IN_PROGRESS: 0
- SATISFIED: 0
- WAIVED: 0
- NOT_APPLICABLE: 0

**Tree x DAG Integrity:**
- Parent anchor (IMPLEMENTS_NODE): 1 (OBJ-003) -- OK
- Requirement trace anchors (TRACES_TO_REQUIREMENT): 4 (SOW-0209, SOW-0210, SOW-0211, SOW-0212)
- No integrity warnings.
