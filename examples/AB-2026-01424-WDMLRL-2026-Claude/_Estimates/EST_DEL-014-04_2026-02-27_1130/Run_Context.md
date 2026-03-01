# Run Context — EST_DEL-014-04_2026-02-27_1130

| Field | Value |
|---|---|
| **RunID** | EST_DEL-014-04_2026-02-27_1130 |
| **AsOf** | 2026-02-27T11:30:00-07:00 |
| **Scope** | DEL-014-04 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-014-04 Floor Drains & Sump Drains), 1 package (PKG-014) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Underground_Utility_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-014-04 |

## Resolved Paths

- **ESTIMATES_ROOT:** `{RUN_ROOT}/_Estimates/`
- **DELIVERABLE_PATH:** `{RUN_ROOT}/PKG-014_Plumbing & Water Systems Installation/1_Working/DEL-014-04_Floor-Drains/`
- **Documents read:** _CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md (all 5 found)

## Warnings

- W-01: Drain type, body material, grate material, body diameter, flow rate, trap type all TBD per IFC plumbing design (DEL-006-03). Material pricing uses parametric allowances.
- W-02: Sump drain quantity stated as "per IFC plumbing design"; assumed minimum 2 (one per repair bay) for estimating.
- W-03: No dedicated plumbing fixture/drain unit cost table in PRICE_SOURCES. Material costs derived parametrically from industry norms for Alberta heavy industrial shop construction.
- W-04: Oil/grease interceptor requirement TBD (REQ-014-04-11); excluded from this estimate pending Plumbing Engineer determination.
- W-05: Wash bay drain scope boundary with DEL-018-05 is TBD; interior drain body and stub connection included, exterior drainage excluded.
