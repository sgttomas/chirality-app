# Schema Annex — Canonical CSV Schemas

Companion reference for `skills/estimate-prep/SKILL.md`. The following 9 schema families cover all 18 canonical CSV files in the `_PriceSources/` library. Headers are listed in exact column order as observed on disk.

Hardened against the canonical `_PriceSources/` library **as of 2026-02-18**.

---

## Family 1 — Standard Unit-Rate (9 files)

**Header:** `ItemID,Category,Description,Unit,RateMin,RateMax,RecommendedRate,Basis,Confidence,Notes`

| File | ID Prefix | Scope |
|------|-----------|-------|
| `Structural_Concrete_Rates.csv` | SC-xx | Concrete, formwork, rebar, structural steel, foundations |
| `Building_Envelope_Rates.csv` | BE-xx | Wall/roof panels, cladding, insulation, glazing, doors |
| `Mechanical_System_Rates.csv` | MS-xx | HVAC, plumbing, fire protection, exhaust |
| `Electrical_System_Rates.csv` | ES-xx | Power, lighting, telecom, fire alarm, solar-ready |
| `Earthwork_Civil_Rates.csv` | EC-xx | Clearing, excavation, fill, compaction, drainage |
| `Paving_Surfacing_Rates.csv` | PS-xx | Asphalt, aggregate, concrete aprons, curbs |
| `Underground_Utility_Rates.csv` | UU-xx | Water, sewer, gas, power, telecom; tie-in allowances |
| `Fees_Permits_Insurance.csv` | FP-xx | Bonds, insurance, permits, utility connections, environmental fees |
| `Interior_Architectural_Rates.csv` | IA-xx | Partitions, ceilings, flooring, paint, accessibility, signage, millwork, specialties |

**Observed `Basis` values:** `MARKET`, `PARAMETRIC`, `ALLOWANCE`, `N/A`
**Observed `Confidence` values:** `HIGH`, `MEDIUM`, `LOW`, `N/A`

**ESTIMATING guidance:** Use `RecommendedRate` as point estimate. Record `RateMin`/`RateMax` for risk analysis. Flag `Confidence=LOW` items for future vendor quote replacement.

---

## Family 2 — Equipment Pricing (1 file)

**Header:** `ItemID,Category,Description,Unit,PriceMin,PriceMax,RecommendedPrice,Quantity_Assumed,Basis,Confidence,Notes`

| File | ID Prefix |
|------|-----------|
| `Equipment_Pricing.csv` | EQ-xx |

**Notes:** Uses `Price*` columns (not `Rate*`). `Quantity_Assumed` is present and may be blank for lump-sum items.

---

## Family 3 — Optional Items Pricing (1 file)

**Header:** `ItemID,Category,Description,Unit,PriceMin,PriceMax,RecommendedPrice,Basis,Confidence,Notes`

| File | ID Prefix |
|------|-----------|
| `Optional_Items_Pricing.csv` | OPT-xx |

**Notes:** Uses `Price*` columns (not `Rate*`). **No `Quantity_Assumed` column** (unlike Equipment_Pricing). Options include base scope, alternates, and items pending resolution (e.g., OPT-18 = FF&E per OI-004).

---

## Family 4 — Professional Staff Rates (1 file)

**Header:** `RoleID,Role,Category,HourlyRate_CAD,Basis,Confidence,Notes`

| File | ID Prefix |
|------|-----------|
| `Professional_Staff_Rates.csv` | R-xx |

**Notes:** Single rate per role — **no min/max/recommended pattern**. Column is `Role` (not `RoleName`). `Category` groups roles (e.g., `Design`, `Management`, `Construction`, `Admin`, `Specialty`). Currency is embedded in the column name (`HourlyRate_CAD`).

---

## Family 5 — Construction Labour Rates (1 file)

**Header:** `TradeID,Trade,HourlyRate_CAD,BurdenMultiplier,FullyBurdenedRate_CAD,Basis,Confidence,Notes`

| File | ID Prefix |
|------|-----------|
| `Construction_Labour_Rates.csv` | T-xx |

**Notes:** Single rate with burden multiplier → fully burdened rate. No min/max pattern. ID column is `TradeID` (not `ItemID`).

---

## Family 6 — Professional Design Fees (1 file)

**Header:** `ItemID,Discipline,Description,FeePercentMin,FeePercentMax,RecommendedPercent,FeeBase,Basis,Confidence,Notes`

| File | ID Prefix |
|------|-----------|
| `Professional_Design_Fees.csv` | DF-xx |

**Notes:** Uses `Discipline` (not `Category`). Fee percent columns use min/max/recommended pattern. `FeeBase` indicates the basis of the percentage (e.g., `construction_value`). Some items (DF-06/07/08) use `lump_sum` in percent fields when the fee is a fixed amount rather than a percentage.

---

## Family 7 — Parametric Building Rates (1 file)

**Header:** `ItemID,BuildingType,Description,Unit,RateMin,RateMax,RecommendedRate,Basis,Confidence,Notes`

| File | ID Prefix |
|------|-----------|
| `Parametric_Building_Rates.csv` | PB-xx |

**Notes:** Uses `BuildingType` (not `Category`). Otherwise follows the standard unit-rate column pattern. Used for parametric cross-checks and fallback estimation.

---

## Family 8 — Project Parameters (1 file)

**Header:** `ParameterID,Category,Parameter,Value,Unit,Source,Confidence,Notes`

| File | ID Prefix |
|------|-----------|
| `Assumed_Project_Parameters.csv` | PP-xx |

**Notes:** Uses `Source` column (**not** `Basis`). The `Source` enum indicates how the parameter was obtained. No rate columns — each parameter is a single `Value`.

**Observed `Source` values:** `ASSUMPTION`, `DESIGN_BASIS`, `CONFIRMED`, `DERIVED`, `PARAMETRIC`
**Observed `Confidence` values:** `HIGH`, `MEDIUM`, `LOW`

---

## Family 9 — Level of Effort (2 files)

**Header:** `Execution,DeliverableID,DeliverableName,RoleID,Role,EstimatedHours,Basis,Notes`

| File | Scope |
|------|-------|
| `Proposal_Level_of_Effort.csv` | Multi-execution shared file (filter by `Execution` column) |
| `Level_of_Effort.csv` | Execution-specific file (single execution) |

**Notes:** **No `Confidence` column.** Provenance is conveyed via `Basis` alone. All columns are required — `Execution`, `DeliverableName`, and `Role` are NOT optional. `Basis` values observed: `PARAMETRIC`.

---

## Basis and Source enum reference

| Context | Column | Observed canonical values | ENRICH additions |
|---------|--------|--------------------------|------------------|
| Rate/pricing files (Families 1-7) | `Basis` | `MARKET`, `PARAMETRIC`, `ALLOWANCE`, `N/A` | `QUOTE`, `HUMAN_PROVIDED`, `HUMAN_CONFIRMED` |
| Project parameters (Family 8) | `Source` | `ASSUMPTION`, `DESIGN_BASIS`, `CONFIRMED`, `DERIVED`, `PARAMETRIC` | `HUMAN_PROVIDED` |
| Level of effort (Family 9) | `Basis` | `PARAMETRIC` | `MARKET`, `HUMAN_PROVIDED` |

---

## Confidence level definitions

| Confidence | Meaning | Typical Source |
|-----------|---------|----------------|
| `HIGH` | Human-confirmed, vendor-quoted, or source-document-derived | Vendor quotes, confirmed rate tables, RFP requirements |
| `MEDIUM` | Parametric market rate or comparable-project benchmark | Market data, industry benchmarks, comparable project data |
| `LOW` | Allowance or assumption-based placeholder | Rules of thumb, unvalidated allowances |

---

## Override_Log.csv schema (ENRICH mode)

Minimum columns:
- `OverrideID`
- `File`
- `Key`
- `Field`
- `PriorValue`
- `PriorConfidence`
- `PriorBasis` (or `PriorSource` for Family 8 files)
- `NewValue`
- `NewConfidence`
- `NewBasis` (or `NewSource` for Family 8 files)
- `HumanSource`
- `Notes`

---

## Conflicts.csv schema (when needed)

- `ConflictID`
- `Key`
- `Description`
- `Contenders` *(paths/refs; include values where possible)*
- `ProposedAuthority` *(PROPOSAL; optional)*
- `HumanRuling` *(TBD until decided)*
- `Notes`
