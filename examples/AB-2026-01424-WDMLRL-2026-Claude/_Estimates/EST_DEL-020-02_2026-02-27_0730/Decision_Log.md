# Decision Log — EST_DEL-020-02_2026-02-27_0730

## Defaults Applied

| ID | Decision | Rationale |
|----|----------|-----------|
| DEC-001 | Rounding set to NONE (default) | ROUNDING not specified in brief; default applied per protocol |
| DEC-002 | UPDATE_LATEST_POINTER = FALSE | Explicitly set in brief; no pointer file modified |
| DEC-003 | RUN_TIMESTAMP taken from brief | 2026-02-27T07:30:00-07:00 as provided |

## Scope Resolution Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| DEC-004 | Scope resolved to single deliverable DEL-020-02 | SCOPE = DEL-020-02 in brief; resolved to DEL-020-02_Final-Inspection in PKG-020 |
| DEC-005 | All four documents present and read | Datasheet.md, Specification.md, Guidance.md, Procedure.md all found in deliverable path |

## Pricing Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| DEC-006 | Activity items (ITEM-020-02-001 through 009) not independently priced in Detail.csv | These items describe the procedural work activities (inspection checklist development, self-inspection, readiness confirmation, written request, Owner inspection facilitation, deficiency management, CCC procurement, consolidated summary, closeout). The effort for these activities is captured by the role-based labour allocations (ITEM-020-02-010 through 017). Independent pricing would double-count. Activity items retained in Items.csv for traceability. |
| DEC-007 | All labour pricing uses PARAMETRIC method | Rates from Professional_Staff_Rates.csv (Basis=PARAMETRIC) and hours from Level_of_Effort.csv (Basis=PARAMETRIC). Consistent with BASIS_OF_ESTIMATE=PARAMETRIC. |
| DEC-008 | CBS classified as Professional Services for all lines | DEL-020-02 is entirely a professional services deliverable (inspection, documentation, coordination, certification). No material, equipment, or construction trade costs identified. |
| DEC-009 | Optional_Items_Pricing.csv items (OPT-01, OPT-02) not applicable | OPT-01 (winter conditions) and OPT-02 (contaminated soils) are construction alternates not relevant to the final inspection and CCC deliverable. |

## Fallback Uses

None. All items were priced from basis evidence (PARAMETRIC). FALLBACK_POLICY = ALLOW_PARAMETRIC was not exercised.
