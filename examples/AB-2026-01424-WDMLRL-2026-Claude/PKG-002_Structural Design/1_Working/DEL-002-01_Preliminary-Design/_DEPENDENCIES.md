# Dependencies: DEL-002-01 Preliminary Structural Design

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending — to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) — human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) — human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema, 22 rows)
- **RegisterSchemaVersion:** v3.1

### Summary

| Category | Count |
|---|---|
| Total ACTIVE rows | 22 |
| Total RETIRED rows | 0 |
| ANCHOR rows (ACTIVE) | 3 |
| EXECUTION rows (ACTIVE) | 19 |
| UPSTREAM rows | 9 |
| DOWNSTREAM rows | 13 |

### ANCHOR Register (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-002-01-A01 | IMPLEMENTS_NODE | SOW-0010b | Deliver preliminary structural design for County approval | HIGH |
| DEP-002-01-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant fully functional maintenance shop addition | HIGH |
| DEP-002-01-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |

### EXECUTION Register — Upstream (6 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | SatisfactionStatus | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-002-01-E01 | PREREQUISITE | DOCUMENT | R-01 — RFP Document | SATISFIED | BLOCKING |
| DEP-002-01-E02 | PREREQUISITE | DOCUMENT | R-04 — App B (Shop) Conceptual Floor Plan | SATISFIED | BLOCKING |
| DEP-002-01-E03 | INTERFACE | DELIVERABLE | DEL-001-01 — Preliminary Architectural Design | TBD | ADVISORY |
| DEP-002-01-E04 | INTERFACE | DELIVERABLE | DEL-008-01 — Geotechnical Investigation and Report | TBD | ADVISORY |
| DEP-002-01-E05 | INTERFACE | DELIVERABLE | DEL-008-02 — Preliminary Site Survey | TBD | TBD |
| DEP-002-01-E06 | PREREQUISITE | EXTERNAL | AHJ-CAMROSE — Authority Having Jurisdiction | TBD | BLOCKING |

### EXECUTION Register — Downstream (13 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | EstimateImpactClass |
|---|---|---|---|---|
| DEP-002-01-E07 | ENABLES | DELIVERABLE | DEL-002-02 — Foundation Plan | BLOCKING |
| DEP-002-01-E08 | ENABLES | DELIVERABLE | DEL-002-03 — Structural Framing Plans | BLOCKING |
| DEP-002-01-E09 | ENABLES | DELIVERABLE | DEL-002-04 — Structural Sections and Details | BLOCKING |
| DEP-002-01-E10 | ENABLES | DELIVERABLE | DEL-002-05 — Mezzanine Framing Details | BLOCKING |
| DEP-002-01-E11 | ENABLES | DELIVERABLE | DEL-002-06 — Service Pit Structural Details | BLOCKING |
| DEP-002-01-E12 | ENABLES | DELIVERABLE | DEL-002-07 — Crane Support Structure Details | BLOCKING |
| DEP-002-01-E13 | ENABLES | DELIVERABLE | DEL-002-08 — Steel Plate Embedment Plan | BLOCKING |
| DEP-002-01-E14 | ENABLES | DELIVERABLE | DEL-002-09 — Stair Details | BLOCKING |
| DEP-002-01-E15 | ENABLES | DELIVERABLE | DEL-002-10 — Structural Calculation Package | BLOCKING |
| DEP-002-01-E16 | ENABLES | DELIVERABLE | DEL-002-11 — Foundation Design Package (Variable-Price) | BLOCKING |
| DEP-002-01-E17 | ENABLES | DELIVERABLE | DEL-002-12 — Structural Specification | BLOCKING |
| DEP-002-01-E18 | ENABLES | PACKAGE | PKG-010 — Foundation Construction | BLOCKING |
| DEP-002-01-E19 | ENABLES | PACKAGE | PKG-011 — Building Structure and Envelope | BLOCKING |

---

## Run Notes

### Run: 2026-02-26

**Parameters:**
- SCOPE: DEL-002-01_Preliminary-Design
- RUN_ROOT: `PKG-002_Structural Design/1_Working/DEL-002-01_Preliminary-Design`
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved below)
- ANCHOR_DOC: AUTO (resolved to `Datasheet.md`)
- EXECUTION_DOC_ORDER: AUTO (resolved to `Procedure.md`, `Guidance.md`, `Specification.md`)

**Decomposition:**
- PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md`
- STATUS: Available, R1 — 2026-02-25. Validation and label resolution performed successfully.

**Source documents scanned (AUTO resolution):**
- `Datasheet.md` (ANCHOR_DOC) — contains deliverable identification, attributes, conditions, references
- `Procedure.md` (EXECUTION_DOC, primary) — contains prerequisites, steps, verification
- `Guidance.md` (EXECUTION_DOC) — contains purpose, principles, considerations, trade-offs
- `Specification.md` (EXECUTION_DOC) — contains scope, requirements, standards, verification

**Read-only inputs used:**
- `_REFERENCES.md` — used for document pointer resolution (R-01, R-04 locations)
- `_Decomposition/WDMLRL_Decomposition_Claude.md` — used for anchor validation, target ID resolution, and label resolution

**Defaults applied:**
- ANCHOR_DOC heuristic selected `Datasheet.md` (filename contains "datasheet" — highest-priority ANCHOR_DOC candidate)
- EXECUTION_DOC_ORDER heuristic: `Procedure.md` (contains "procedure"), then `Guidance.md` (contains "guidance"), then `Specification.md` (contains "spec")

**Extraction decisions and assumptions:**
- Geotechnical report (DEL-008-01) classified as INTERFACE not PREREQUISITE because Procedure §2.1 explicitly states "NOT required to complete preliminary design concept." It is required for foundation finalization, making it an interface rather than a hard prerequisite for this deliverable.
- Preliminary Site Survey (DEL-008-02) retained as INTERFACE with TBD satisfaction status because Procedure §2.1 explicitly flags it as requiring a Project Manager decision (F-003).
- AHJ contact (AHJ-CAMROSE) extracted as EXTERNAL PREREQUISITE because Procedure §2.1 explicitly lists it as "Required for code framework establishment" and Specification §3 note A-003 confirms the AHJ identity is TBD.
- Downstream ENABLES rows expanded from 2 (DEL-002-02, DEL-002-03) to 11 (DEL-002-02 through DEL-002-12) because Guidance §2.4 explicitly states "Every structural detail deliverable downstream (DEL-002-02 through DEL-002-09) derives from decisions made in this preliminary design" and "the calculation package (DEL-002-10)" and the full range "DEL-002-02 through DEL-002-12."
- Procedure Step 5 coordination items (Architect grid sharing, Mechanical crane clearance, Electrical service pit lighting) were NOT extracted as dependencies because they describe coordination process steps without the "required before / cannot proceed without" framing needed under CONSERVATIVE strictness. The explicit prerequisite relationship with DEL-001-01 (Architectural) is already captured in E03.
- R-01 and R-04 SatisfactionStatus set to SATISFIED because Procedure §2.1 explicitly marks both as "Available."

**Previous run rows — disposition:**
- DEP-002-01-A01 through A03: matched, updated (evidence paths refined)
- DEP-002-01-E01 through E03 (old): renumbered E01 through E03; matched by class+type+target
- DEP-002-01-E04 through E07 (old): renumbered and expanded; old E04/E05 (DEL-002-02, DEL-002-03 downstream) became E07/E08; old E06/E07 (PKG-010, PKG-011) became E18/E19
- New rows: E04 (geotech), E05 (survey), E06 (AHJ), E09-E17 (remaining downstream deliverables)

**Warnings:**
- None. Parent anchor (IMPLEMENTS_NODE) present and unique. No integrity issues detected.

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Available (R1) | None | 3 | 19 | 22 |

---

## Lifecycle Summary

### Extraction Lifecycle

| Status | Count |
|---|---|
| ACTIVE | 22 |
| RETIRED | 0 |

### Closure Lifecycle (ACTIVE rows only)

| SatisfactionStatus | Count |
|---|---|
| TBD | 20 |
| SATISFIED | 2 |
| PENDING | 0 |
| IN_PROGRESS | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |

### Closure Detail

- **SATISFIED (2):** DEP-002-01-E01 (RFP document in hand), DEP-002-01-E02 (App B Shop in hand)
- **TBD (20):** All anchor rows (satisfaction not applicable to traceability anchors but tracked as TBD per schema); all remaining execution rows pending work/decisions

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are relevant for task estimating workflows consuming this dependency register:

### Blocking Dependencies for Estimating Readiness

1. **AHJ Contact (DEP-002-01-E06):** The governing code editions (NBC, ABC, CSA standards) cannot be confirmed until the Authority Having Jurisdiction is identified. This is a prerequisite for establishing the code framework, which influences structural system selection, seismic design parameters, and therefore the scope and complexity of the preliminary design effort. **Impact on estimating:** Code framework uncertainty may affect the level of effort estimate for the preliminary design task.

2. **Geotechnical Report (DEP-002-01-E04):** While the preliminary design can proceed without the geotech report (per Guidance §2.2), the foundation section of the preliminary design is explicitly conditional. **Impact on estimating:** The preliminary design task estimate should account for the foundation section being provisional and potentially requiring revision. The variable-price foundation scope (RFP §4.8.2) cannot be estimated until geotech is available.

3. **Preliminary Site Survey (DEP-002-01-E05):** Status TBD pending Project Manager decision. **Impact on estimating:** If the survey is determined to be a prerequisite, this could affect the start date for the preliminary design task.

### Downstream Blocking Fan-Out

DEL-002-01 is a **critical-path gate** for the entire PKG-002 Structural Design package. County approval of this deliverable is explicitly required before any of the 11 downstream structural deliverables (DEL-002-02 through DEL-002-12) can proceed. It also gates the two downstream construction packages (PKG-010 Foundation Construction, PKG-011 Building Structure and Envelope).

**Estimating implication:** The duration and approval cycle time of DEL-002-01 directly affects the critical path for the structural design phase and, transitively, the construction phase.

### Advisory Dependencies

- **DEL-001-01 Preliminary Architectural Design (DEP-002-01-E03):** Sequencing between architectural and structural preliminary design is TBD. Concurrent development with coordination checkpoints is assumed (Procedure Step 5). **Impact on estimating:** If concurrent, minimal schedule impact; if sequential (architectural first), adds lead time.
