# Run Context — EST_DEL-001-09_2026-02-27_0546

| Field | Value |
|---|---|
| **RunID** | EST_DEL-001-09_2026-02-27_0546 |
| **AsOf** | 2026-02-27T05:46Z |
| **Scope** | DEL-001-09 (Old North Shop Demolition Plans) |
| **ScopeResolvedSummary** | 1 deliverable, 1 package (PKG-001 Architectural Design) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Professional_Design_Fees.csv, Parametric_Building_Rates.csv — all under `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/` |
| **DECOMPOSITION_PATH** | `_Decomposition/WDMLRL_Decomposition_Claude.md` |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **OUTPUT_LABEL** | DEL-001-09 |
| **Warnings** | (1) Mezzanine area (SOW-0071) is TBD — no measured area available from sources. (2) Washroom area (SOW-0072) is TBD — no measured area available from sources. (3) No as-built drawings confirmed for existing Old North Shop. (4) Hazardous materials assessment status is TBD. |

## Scope Resolution

DEL-001-09 is a Drawing Set deliverable under PKG-001 (Architectural Design), covering demolition plans for the three renovation areas of the existing Old North Shop:

- SOW-0070: Kitchenette area (~250 sq ft)
- SOW-0071: Mezzanine / 2nd-level coffee room (area TBD)
- SOW-0072: Washroom below mezzanine (area TBD)

Responsible party: Architect. Deliverable type: Drawing Set.

## Pricing Strategy

This is a **design deliverable** (architectural drawing set). The primary cost driver is **professional staff effort** (hours x rates), not construction material/labour. The Level_of_Effort.csv provides parametric hour allocations per role for DEL-001-09. Professional_Staff_Rates.csv provides hourly rates. The estimate is computed as: hours x rate per role, summed across all roles assigned to DEL-001-09.

Construction cost items (demolition labour, waste disposal, hazmat abatement) are **not within scope of this deliverable** — those belong to PKG-017 (Existing Building Renovation) construction deliverables (DEL-017-01, DEL-017-02, DEL-017-03).
