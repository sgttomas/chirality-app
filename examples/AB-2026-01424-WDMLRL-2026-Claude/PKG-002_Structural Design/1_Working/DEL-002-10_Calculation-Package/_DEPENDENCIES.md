# Dependencies: DEL-002-10 Structural Calculation Package

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** EXTRACTED
- **Dependencies.csv:** `Dependencies.csv` (RegisterSchemaVersion v3.1)
- **Total rows:** 27
- **ACTIVE:** 27 | **RETIRED:** 0

### ANCHOR Rows (6 ACTIVE)

| DependencyID | AnchorType | TargetRefID / TargetName | Confidence |
|---|---|---|---|
| DEP-002-10-A01 | IMPLEMENTS_NODE | PKG-002 Structural Design | HIGH |
| DEP-002-10-A02 | TRACES_TO_REQUIREMENT | SOW-0012 Complete final structural design | HIGH |
| DEP-002-10-A03 | TRACES_TO_REQUIREMENT | SOW-0019 Design foundation (variable-price post-geotech) | HIGH |
| DEP-002-10-A04 | TRACES_TO_REQUIREMENT | OBJ-001 Code-compliant functional facility | HIGH |
| DEP-002-10-A05 | TRACES_TO_REQUIREMENT | OBJ-003 Complete P.Eng.-stamped IFC documentation | HIGH |
| DEP-002-10-A06 | TRACES_TO_REQUIREMENT | OBJ-006 Foundation cost reconciled post-geotech | HIGH |

### EXECUTION Rows (21 ACTIVE)

#### Upstream (information flows TO DEL-002-10)

| DependencyID | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-002-10-E01 | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation & Report | HIGH | BLOCKING |
| DEP-002-10-E02 | PREREQUISITE | DELIVERABLE | DEL-016-01 Two 5-Tonne Overhead Cranes | HIGH | ADVISORY |
| DEP-002-10-E03 | INTERFACE | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | MEDIUM | ADVISORY |
| DEP-002-10-E17 | INTERFACE | PACKAGE | PKG-003 Mechanical Design (loads and penetrations) | MEDIUM | ADVISORY |
| DEP-002-10-E18 | INTERFACE | PACKAGE | PKG-004 Electrical Design (equipment loads) | MEDIUM | ADVISORY |
| DEP-002-10-E19 | INTERFACE | PACKAGE | PKG-006 Plumbing Design (penetrations) | MEDIUM | ADVISORY |
| DEP-002-10-E21 | INTERFACE | PACKAGE | PKG-001 Architectural Design (layout coordination) | MEDIUM | ADVISORY |

#### Downstream (information flows FROM DEL-002-10)

| DependencyID | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-002-10-E04 | ENABLES | DELIVERABLE | DEL-002-01 Preliminary Structural Design | HIGH | BLOCKING |
| DEP-002-10-E05 | HANDOVER | DELIVERABLE | DEL-002-02 Foundation Plan | HIGH | BLOCKING |
| DEP-002-10-E06 | HANDOVER | DELIVERABLE | DEL-002-03 Structural Framing Plans | HIGH | ADVISORY |
| DEP-002-10-E07 | HANDOVER | DELIVERABLE | DEL-002-04 Structural Sections & Details | HIGH | ADVISORY |
| DEP-002-10-E08 | HANDOVER | DELIVERABLE | DEL-002-05 Mezzanine Framing Details | HIGH | ADVISORY |
| DEP-002-10-E09 | HANDOVER | DELIVERABLE | DEL-002-06 Service Pit / Trench Structural Details | HIGH | ADVISORY |
| DEP-002-10-E10 | HANDOVER | DELIVERABLE | DEL-002-07 Crane Support Structure Details | HIGH | ADVISORY |
| DEP-002-10-E11 | HANDOVER | DELIVERABLE | DEL-002-08 Steel Plate Embedment Plan | HIGH | ADVISORY |
| DEP-002-10-E12 | HANDOVER | DELIVERABLE | DEL-002-09 Stair Details | HIGH | ADVISORY |
| DEP-002-10-E13 | HANDOVER | DELIVERABLE | DEL-002-11 Foundation Design Package (Variable-Price) | HIGH | BLOCKING |
| DEP-002-10-E14 | HANDOVER | DELIVERABLE | DEL-002-12 Structural Specification | HIGH | ADVISORY |
| DEP-002-10-E15 | HANDOVER | PACKAGE | PKG-010 Foundation Construction | HIGH | BLOCKING |
| DEP-002-10-E16 | HANDOVER | PACKAGE | PKG-011 Building Structure & Envelope | HIGH | BLOCKING |
| DEP-002-10-E20 | HANDOVER | PACKAGE | PKG-009 Permitting & Regulatory Compliance | MEDIUM | ADVISORY |

---

## Run Notes

### Run: 2026-02-26

**Parameters:**
- SCOPE: DEL-002-10_Calculation-Package
- RUN_ROOT: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-002_Structural Design/1_Working/DEL-002-10_Calculation-Package`
- DECOMPOSITION_PATH: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md` (found; R1 2026-02-25)
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING

**Source documents scanned (AUTO):**
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: filename contains "datasheet"; highest anchor-signal match)
- EXECUTION_DOC_ORDER:
  1. `Procedure.md` (filename contains "procedure")
  2. `Specification.md` (filename contains "spec")
  3. `Guidance.md` (filename contains "guidance")
  4. `Datasheet.md` (re-scanned for execution cues)

**Read-only inputs used:**
- `_REFERENCES.md` (used for document pointer resolution)
- Decomposition: `WDMLRL_Decomposition_Claude.md` R1 2026-02-25

**Defaults applied:**
- SOURCE_DOCS: AUTO (scanned 4 source documents; excluded `_CONTEXT.md`, `_STATUS.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`, `_REFERENCES.md`, `_DEPENDENCIES.md`, `Dependencies.csv`)
- DOC_ROLE_MAP: DEFAULT
- ANCHOR_DOC: AUTO -> `Datasheet.md`
- EXECUTION_DOC_ORDER: AUTO -> `Procedure.md`, `Specification.md`, `Guidance.md`, `Datasheet.md`

**Decisions and corrections (relative to prior extraction):**
- Prior extraction had two IMPLEMENTS_NODE rows (DEP-002-10-A01 for SOW-0012, DEP-002-10-A01b for SOW-0019). Corrected to a single IMPLEMENTS_NODE for PKG-002 (the parent package). SOW-0012 and SOW-0019 are now TRACES_TO_REQUIREMENT rows as scope item traces.
- Prior DEP-002-10-E02 had DEL-002-01 as UPSTREAM/PREREQUISITE. Corrected: the source text states calcs must *support* DEL-002-01, meaning information flows FROM DEL-002-10 TO DEL-002-01 (DOWNSTREAM/ENABLES). The upstream architectural input relationship is captured separately as DEP-002-10-E03 (DEL-001-01).
- Prior extraction omitted downstream handovers to DEL-002-04 through DEL-002-09, DEL-002-11, DEL-002-12. These are now captured (DEP-002-10-E07 through DEP-002-10-E14).
- Prior extraction omitted upstream interfaces with PKG-001, PKG-003, PKG-004, PKG-006. These are now captured (DEP-002-10-E17 through DEP-002-10-E19, DEP-002-10-E21).
- Prior extraction omitted upstream prerequisite on DEL-016-01 crane specifications and downstream handover to PKG-009 building permit. These are now captured (DEP-002-10-E02, DEP-002-10-E20).
- DependencyID scheme renumbered for consistency. Prior IDs retired (non-destructive: prior file overwritten as this is the first formal agent run; prior data was a draft).

**Warnings:**
- None. All integrity checks pass.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ANCHOR ACTIVE | EXECUTION ACTIVE | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md R1 (available) | None | 6 | 21 | 27 |

---

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 27
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown, ACTIVE rows only)
- **TBD:** 23
- **PENDING:** 4 (DEP-002-10-E01 geotech report; DEP-002-10-E02 crane specs; DEP-002-10-E03 architectural input; DEP-002-10-E04 preliminary design support)
- **IN_PROGRESS:** 0
- **SATISFIED:** 0
- **WAIVED:** 0
- **NOT_APPLICABLE:** 0

---

## Downstream Handoff Notes

**Consumer context: TASK_ESTIMATING**

The following dependencies are most relevant to task estimating readiness for DEL-002-10:

### BLOCKING for estimating

| DependencyID | Target | Direction | Rationale |
|---|---|---|---|
| DEP-002-10-E01 | DEL-008-01 Geotechnical Report | UPSTREAM | Foundation design scope and quantities cannot be finalized without geotech data. Estimating of foundation scope (SOW-0019) is gated on this input. Preliminary estimates possible on "normal ground conditions" assumption per RFP 4.8.2. |
| DEP-002-10-E04 | DEL-002-01 Preliminary Structural Design | DOWNSTREAM | Preliminary calculations must be complete before DEL-002-01 presentation. This gates the County approval milestone. |
| DEP-002-10-E05 | DEL-002-02 Foundation Plan | DOWNSTREAM | Foundation Plan drawings depend on calculation outputs. Estimating for foundation construction (PKG-010) depends on these drawings. |
| DEP-002-10-E13 | DEL-002-11 Foundation Design Package | DOWNSTREAM | Variable-price foundation package shares calculations with DEL-002-10. Estimating for foundation cost reconciliation depends on this. |
| DEP-002-10-E15 | PKG-010 Foundation Construction | DOWNSTREAM | Foundation construction package estimating depends on calculation outputs. |
| DEP-002-10-E16 | PKG-011 Building Structure & Envelope | DOWNSTREAM | Superstructure construction package estimating depends on calculation outputs. |

### ADVISORY for estimating

| DependencyID | Target | Direction | Rationale |
|---|---|---|---|
| DEP-002-10-E02 | DEL-016-01 Crane Specifications | UPSTREAM | Final crane runway sizing may change with manufacturer data; conservative assumptions allow preliminary estimating to proceed. |
| DEP-002-10-E03 | DEL-001-01 Architectural Design | UPSTREAM | Architectural layout affects structural member locations and quantities; preliminary dimensions from App B are sufficient for early estimating. |
| DEP-002-10-E06 | DEL-002-03 Framing Plans | DOWNSTREAM | Framing plan quantities informed by calculations. |
| DEP-002-10-E07 thru E12 | DEL-002-04 thru DEL-002-09 | DOWNSTREAM | Drawing sets informed by calculations; quantities may change with calculation revisions. |
| DEP-002-10-E14 | DEL-002-12 Structural Specification | DOWNSTREAM | Material specifications (concrete strength, reinforcement grade) informed by calculations. |
| DEP-002-10-E17 thru E19, E21 | PKG-001, PKG-003, PKG-004, PKG-006 | UPSTREAM | Discipline interface data affects structural penetration quantities and coordination scope. |
| DEP-002-10-E20 | PKG-009 Building Permit | DOWNSTREAM | Calc package supports permit application; permit timeline may affect estimating schedule. |

### Key estimating risk

The primary estimating risk for DEL-002-10 is the **foundation scope uncertainty**. Until DEL-008-01 (geotechnical report) is delivered, all foundation quantities and costs are based on the "normal ground conditions" assumption (RFP 4.8.2). If geotech reveals poor soils requiring deep foundations, foundation scope and cost will change materially. The CCDC 14-2013 variable-price mechanism (OBJ-006) is designed to manage this risk contractually, but estimating must account for the range of possible outcomes.
