# Dependencies: DEL-001-06 Reflected Ceiling Plans

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema)
- **Total ACTIVE rows:** 11
- **Total RETIRED rows:** 0

### ANCHOR rows (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-06-A01 | IMPLEMENTS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-06-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-06-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION rows (8 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetDeliverableID | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|---|
| DEP-001-06-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 | Preliminary Architectural Design | HIGH | BLOCKING |
| DEP-001-06-E02 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-04 | Lighting Plans | HIGH | ADVISORY |
| DEP-001-06-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-03 | Structural Framing Plans | HIGH | ADVISORY |
| DEP-001-06-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-003-02 | HVAC Layout Plans | HIGH | ADVISORY |
| DEP-001-06-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 | Architectural Floor Plans | HIGH | BLOCKING |
| DEP-001-06-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-04 | Building Sections | MEDIUM | ADVISORY |
| DEP-001-06-E07 | UPSTREAM | CONSTRAINT | DOCUMENT | -- | Alberta Safety Codes (building, electrical, fire) | HIGH | ADVISORY |
| DEP-001-06-E08 | UPSTREAM | CONSTRAINT | REQUIREMENT | -- | P.Eng. stamp required for IFC (REQ-RCP-015) | HIGH | BLOCKING |

---

## Run Notes

### Run: 2026-02-26

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved below)
- ANCHOR_DOC: AUTO (resolved to Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved to Procedure.md, Specification.md, Guidance.md)
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25)

**Source documents scanned:**
1. `Datasheet.md` -- ANCHOR_DOC (definition/traceability signal: SOW, OBJ identifiers)
2. `Procedure.md` -- EXECUTION_DOC (prerequisite table, procedural steps with input references)
3. `Specification.md` -- EXECUTION_DOC (requirements with cross-discipline coordination statements)
4. `Guidance.md` -- EXECUTION_DOC (principles and considerations referencing coordination)

**Read-only inputs used:**
- `_REFERENCES.md` -- consulted for document location pointers
- `_CONTEXT.md` -- consulted for deliverable identity confirmation

**Decomposition validation:**
- SOW-0011 confirmed in decomposition Section 3, SSOW C (Final Design): maps to PKG-001, DEL-001-02 through DEL-001-08, DEL-001-11
- OBJ-001 confirmed in decomposition Section 5: "Deliver a code-compliant, fully functional maintenance shop addition..."
- OBJ-003 confirmed in decomposition Section 5: "Produce complete, P.Eng.-stamped IFC design documentation across all disciplines..."
- DEL-001-01 confirmed in decomposition Section 7, PKG-001: "Preliminary Architectural Design"
- DEL-001-02 confirmed in decomposition Section 7, PKG-001: "Architectural Floor Plans"
- DEL-001-04 confirmed in decomposition Section 7, PKG-001: "Building Sections"
- DEL-002-03 confirmed in decomposition Section 7, PKG-002: "Structural Framing Plans"
- DEL-003-02 confirmed in decomposition Section 7, PKG-003: "HVAC Layout Plans"
- DEL-004-04 confirmed in decomposition Section 7, PKG-004: "Lighting Plans"

**Defaults applied:**
- DOC_ROLE_MAP: DEFAULT heuristic used. Datasheet.md matched ANCHOR_DOC by filename pattern "datasheet." Procedure.md matched EXECUTION_DOC by pattern "procedure." Specification.md matched by pattern "spec." Guidance.md matched by pattern "guidance."
- All target deliverable IDs resolved via decomposition lookup.

**Decisions and assumptions:**
- Procedure references "DEL-002 series" generically for structural inputs; resolved to DEL-002-03 (Structural Framing Plans) as the primary structural ceiling interface per REQ-RCP-013 and Procedure B-01.
- Procedure references "DEL-004 series" generically for electrical inputs; resolved to DEL-004-04 (Lighting Plans) as the primary electrical ceiling interface per REQ-RCP-012 and Procedure B-02.
- Procedure references "DEL-003 series" generically for mechanical inputs; resolved to DEL-003-02 (HVAC Layout Plans) as the primary mechanical ceiling interface per REQ-RCP-014 and Procedure B-03.
- The geotechnical report (listed in Procedure Prerequisites) is noted "for project schedule awareness" and described as "not directly RCP"; no dependency row emitted per CONSERVATIVE strictness (not a direct information/artifact input to RCP production).
- No DOWNSTREAM execution edges emitted: source documents describe this deliverable as a consumer of other discipline inputs; no explicit statements of other deliverables consuming RCP output were found in the scanned documents.
- DEP-001-06-E07 (Alberta Safety Codes): TargetType=DOCUMENT because the constraint references external regulatory documents. TargetLocation set to "location TBD" per Specification Standards table C-001.
- DEP-001-06-E08 (P.Eng. stamp): TargetType=REQUIREMENT because this is an IFC gate constraint traceable to REQ-RCP-015 and RFP S3.3.2.

**Warnings:**
- None. Parent anchor (IMPLEMENTS_NODE) found: exactly 1. No integrity warnings triggered.

---

## Run History

| Run Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (R1) | None | 3 | 8 | 11 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 11 |
| RETIRED | 0 |

### Closure state breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 11 |

All 11 ACTIVE dependencies have SatisfactionStatus=TBD; none have been evaluated for closure.

---

## Downstream Handoff Notes

**Consumer context: TASK_ESTIMATING**

The following dependencies are flagged as relevant to task estimating readiness:

**BLOCKING (3 rows):**
- **DEP-001-06-E01** (PREREQUISITE, DEL-001-01 Preliminary Architectural Design): County approval of the preliminary design is an explicit IFC gate. Estimating for this deliverable should account for the approval cycle duration and any rework from County feedback.
- **DEP-001-06-E05** (INTERFACE, DEL-001-02 Architectural Floor Plans): The floor plan is the base file for RCP production. RCP drawing effort cannot begin without a confirmed floor plan. Estimating should sequence RCP production after floor plan readiness.
- **DEP-001-06-E08** (CONSTRAINT, REQ-RCP-015 P.Eng. stamp): IFC issue requires P.Eng. stamp. Estimating should include time for engineer review and stamping at the end of the RCP production sequence.

**ADVISORY (5 rows):**
- **DEP-001-06-E02** (INTERFACE, DEL-004-04 Lighting Plans): Lighting fixture locations and counts from the electrical engineer affect RCP content. Changes in lighting layout will require RCP updates. Estimating should consider coordination iteration time.
- **DEP-001-06-E03** (INTERFACE, DEL-002-03 Structural Framing Plans): Crane rail positions, mezzanine framing, and concrete ceiling configuration affect RCP content. Estimating should consider coordination iteration time with the structural engineer.
- **DEP-001-06-E04** (INTERFACE, DEL-003-02 HVAC Layout Plans): Forced air makeup unit and exhaust fan positions affect RCP content. Estimating should consider coordination iteration time with the mechanical engineer.
- **DEP-001-06-E06** (INTERFACE, DEL-001-04 Building Sections): Ceiling height confirmation from building sections. Lower impact than floor plan base but still affects content accuracy.
- **DEP-001-06-E07** (CONSTRAINT, Alberta Safety Codes): Regulatory compliance constraint. Code text has not been obtained (Specification TBD C-001). Estimating should note that code review effort is TBD until applicable code sections are identified.
