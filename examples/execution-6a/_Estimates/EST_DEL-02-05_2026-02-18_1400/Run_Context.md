# Run Context

## Run Identity

- **RunID:** EST_DEL-02-05_2026-02-18_1400
- **AsOf:** 2026-02-18T14:00:00-07:00
- **AgentType:** ESTIMATING (Type 2)

## Inputs (as provided)

- **Scope:** DEL-02-05 only (PKG-002)
- **ScopeResolvedSummary:** 1 deliverable in scope; 0 excluded; 0 blocked
- **BASIS_OF_ESTIMATE:** RATE_TABLE (validated; enum OK)
- **CURRENCY:** CAD
- **ROUNDING:** DOLLAR
- **FALLBACK_POLICY:** STRICT
- **ALLOW_MIXED_METHODS:** FALSE
- **UPDATE_LATEST_POINTER:** FALSE
- **OUTPUT_LABEL:** DEL-02-05

## Resolved Paths

- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a`
- **ESTIMATES_ROOT:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/`
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (loaded successfully)
- **DEPENDENCY_SOURCES:** AUTO -- read `Dependencies.csv` from DEL-02-05 deliverable folder (18 rows; schema v3.1)
- **PRICE_SOURCES (resolved):**
  1. `_PriceSources/Mechanical_System_Rates.csv` (rate table; 14 items MS-01 through MS-14)
  2. `_PriceSources/Equipment_Pricing.csv` (rate table; 15 items EQ-01 through EQ-15)
  3. `_PriceSources/Construction_Labour_Rates.csv` (labour rates; 15 trades T-01 through T-15)
  4. `_PriceSources/Professional_Design_Fees.csv` (fee percentages; 8 items DF-01 through DF-08)
  5. `_PriceSources/Assumed_Project_Parameters.csv` (project parameters; 29 items PP-01 through PP-29)

## Area Zoning Assumptions (for rate application)

The 18,000 sf main PSB building footprint (PP-05) is split into zones for area-based mechanical rates:

| Zone | Area (sf) | Rationale |
|------|-----------|-----------|
| Apparatus bays (4 bays) | 6,400 | 4 bays x ~1,600 sf/bay; fire apparatus drive-through sizing |
| PW shop bays (4 bays) | 6,400 | 4 bays x ~1,600 sf/bay; grader-sized drive-through |
| Institutional/shared/office | 5,200 | 18,000 - 6,400 - 6,400; office/admin/kitchen/locker areas |

These zoning splits are documented as ASM-01 in Assumptions_Log.md.

## CBS Mapping Rule

No explicit CBSHint was provided in the decomposition for DEL-02-05. The following deterministic mapping is used:

| CBS Code | Description |
|----------|-------------|
| 23-HVAC | HVAC systems (heating, ventilation, air conditioning) |
| 23-PLMB | Plumbing systems (piping, fixtures, domestic water) |
| 23-EXHS | Vehicle exhaust extraction and bay ventilation |
| 23-EQUP | Mechanical equipment (sumps, fill stations, DHW) |
| 23-CTRL | Building automation / controls |
| 23-FPRT | Fire protection (sprinkler) |
| 23-MECH-DESIGN | Mechanical engineering design fees |
| 23-COMM | System-specific commissioning labour |

CBS prefix "23" follows CSI MasterFormat Division 23 (Heating, Ventilating, and Air-Conditioning) convention, extended for this project.

## Exclusions (per brief -- cost ownership rules)

The following items are explicitly excluded from this estimate per the brief's cost ownership rules:

- Compressed air EQUIPMENT (compressor, piping, drops) -- owned by DEL-02-02
- Floor slab (structural element) -- owned by DEL-02-04
- Sump ROUGH-IN (embedded in slab) -- owned by DEL-02-04
- Electrical feeds for mechanical equipment -- owned by DEL-02-06
- Wash bay DEDICATED equipment beyond base rough-in -- owned by DEL-05-01

## Warnings

- [WARNING] RATE_TABLE basis is declared, but all price source rates carry `Basis=PARAMETRIC` in their CSV metadata. The rates are treated as rate-table entries for this run because they are structured tabular rates with units and recommended values. This is logged as DEC-01 in Decision_Log.md.
- [WARNING] Fire protection (MS-05) is conditional on AHJ requirement; priced but flagged LOW confidence.
- [WARNING] Slab rough-in for sumps excluded (DEL-02-04 owns); only sump assemblies + plumbing connections priced here.
