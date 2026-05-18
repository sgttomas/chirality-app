# Run Context -- EST_DEL-05-05_2026-02-18_1800

## Run Identity

| Field | Value |
|---|---|
| **RunID** | EST_DEL-05-05_2026-02-18_1800 |
| **AsOf** | 2026-02-18T18:00:00-07:00 |

## Scope

| Field | Value |
|---|---|
| **Scope (as provided)** | DEL-05-05 only (PKG-005) |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked from pricing (but BLOCKED on branding guidelines for final design) |

## Configuration

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | QUOTE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | `Optional_Items_Pricing.csv`, `Assumed_Project_Parameters.csv` |
| **DECOMPOSITION_PATH** | `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-05-05 Dependencies.csv -- 7 rows loaded) |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-05-05 |

## CBS Mapping Rule

No explicit `CBSHint` is available in the decomposition for DEL-05-05. The following deterministic mapping is applied:

- Signage fabrication (non-illuminated or illuminated) --> CBS `09-SIGNAGE-FAB`
- Signage mounting/structural --> CBS `09-SIGNAGE-MOUNT`
- Signage electrical (illuminated, conditional) --> CBS `09-SIGNAGE-ELEC`
- Signage installation (labour) --> CBS `09-SIGNAGE-INSTALL`

These CBS codes are internal to this estimate snapshot; they may be reconciled to a project-level CBS during aggregation.

## Warnings

- [WARNING] BASIS_OF_ESTIMATE is QUOTE but no vendor quotes exist for signage. FALLBACK_POLICY=ALLOW_ALLOWANCE permits fallback to ALLOWANCE using parametric data from Optional_Items_Pricing.csv. All line items use Method=ALLOWANCE (fallback). See Decision_Log.md DEC-EST-001.
- [WARNING] Town branding guidelines are PENDING (DEP-05-05-007, SatisfactionStatus=PENDING). Signage design cannot be finalized without them. Quantities, sizes, and illumination scope are TBD.
- [WARNING] Illuminated vs non-illuminated decision is TBD. Estimate carries both scenarios as separate line items (non-illuminated as primary, illuminated as alternate).

## Cost Ownership Boundary

| Scope Area | Cost Owner | NOT in DEL-05-05 |
|---|---|---|
| Branding signage (fabrication + mounting + electrical if illuminated) | DEL-05-05 | -- |
| Code-required signage (exits, accessibility, fire, room ID) | DEL-02-01 | Excluded |
| Structural provisions for signage mounting | DEL-02-04 | Excluded |
| Electrical circuit for illuminated signage | DEL-02-06 | Excluded |
