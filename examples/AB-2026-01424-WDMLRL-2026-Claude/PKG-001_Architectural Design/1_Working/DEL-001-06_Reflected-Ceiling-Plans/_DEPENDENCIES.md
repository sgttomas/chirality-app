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

| DependencyID | Direction | DependencyType | TargetType | TargetDeliverableID | TargetName | Confidence |
|---|---|---|---|---|---|---|
| DEP-001-06-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 | Preliminary Architectural Design | HIGH |
| DEP-001-06-E02 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-04 | Lighting Plans | HIGH |
| DEP-001-06-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-03 | Structural Framing Plans | HIGH |
| DEP-001-06-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-003-02 | HVAC Layout Plans | HIGH |
| DEP-001-06-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 | Architectural Floor Plans | HIGH |
| DEP-001-06-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-04 | Building Sections | MEDIUM |
| DEP-001-06-E07 | UPSTREAM | CONSTRAINT | DOCUMENT | -- | Alberta Safety Codes (building, electrical, fire) | HIGH |
| DEP-001-06-E08 | UPSTREAM | CONSTRAINT | REQUIREMENT | -- | P.Eng. stamp required for IFC (REQ-RCP-015) | HIGH |

---

## Run Notes

### Run: 2026-03-26 (R2 refresh)

**Parameters:**
- SCOPE: DEL-001-06_Reflected-Ceiling-Plans (as part of PKG-001 full refresh)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: R2, 2026-03-26 (SCA-001)

**Extraction Decisions:**
- Pass 1: 3 ANCHOR rows confirmed. No changes.
- Pass 2: 8 prior EXECUTION rows confirmed ACTIVE; LastSeen updated to 2026-03-26.
- No new rows added. R2 changes (precast concrete walls, folding outward doors, mezzanine railing) have minimal direct impact on reflected ceiling plans -- ceiling plans are primarily driven by structural framing, lighting, and HVAC layouts, not wall material or door type.

**Warnings:** None.

### Run: 2026-02-26
- 11 rows extracted. No warnings.

## Run History

| Run Date | Mode | Strictness | Decomposition | Warnings | Total ACTIVE |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | R1 (2026-02-25) | None | 11 |
| 2026-03-26 | UPDATE | CONSERVATIVE | R2, SCA-001 (2026-03-26) | None | 11 |

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
