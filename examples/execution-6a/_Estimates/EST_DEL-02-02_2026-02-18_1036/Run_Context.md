# Run Context: EST_DEL-02-02_2026-02-18_1036

## Run Identity

| Field | Value |
|---|---|
| **RunID** | EST_DEL-02-02_2026-02-18_1036 |
| **AsOf** | 2026-02-18T10:36:00-07:00 |
| **Agent** | ESTIMATING (Type 2) |
| **Invoked By** | INIT-TASK brief (Orchestrator) |

## Inputs (as provided)

| Parameter | Value |
|---|---|
| **SCOPE** | DEL-02-02 |
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| **BASIS_OF_ESTIMATE** | RATE_TABLE (validated: PASS) |
| **CURRENCY** | CAD |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md (loaded: PASS) |
| **DEPENDENCY_SOURCES** | AUTO (resolved: Dependencies.csv loaded for DEL-02-02; 15 rows, 15 ACTIVE) |
| **PRICE_SOURCES** | 9 files (see Source_Index.md for details) |

## Optional Controls (resolved)

| Parameter | Value |
|---|---|
| **OUTPUT_LABEL** | DEL-02-02 |
| **UPDATE_LATEST_POINTER** | FALSE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ROUNDING** | DOLLAR |
| **RUN_TIMESTAMP** | 2026-02-18T10:36:00-07:00 |

## Scope Resolution Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-02-02) |
| Package | PKG-002 -- Main Public Services Building (PSB) |
| Scope items covered | SOW-0202, SOW-0203, SOW-0205, SOW-0206 |
| Objective supported | OBJ-002 |
| Tier | T2 (depends on T1 area/quantity basis) |
| Substance | Construction + Equipment |

## Cost Ownership Rules Applied

These rules govern what is priced under DEL-02-02 vs. other deliverables:

| Scope Element | Owner | NOT Owned By |
|---|---|---|
| Fire bay functional fit-up (gear lockers, decon, breathing air, compressed air equip) | DEL-02-02 | DEL-02-05, DEL-02-06 |
| Compressed air EQUIPMENT (compressor, piping, drops) | DEL-02-02 | DEL-02-05 (resolves CON-M-01) |
| Compressed air ELECTRICAL FEED | DEL-02-06 | DEL-02-02 |
| Overhead doors (hardware, frames, openers) | DEL-02-04 | DEL-02-02 |
| HVAC system | DEL-02-05 | DEL-02-02 |
| Apparatus bay exhaust SYSTEMS (extraction units) | DEL-02-05 | DEL-02-02 |
| Bay display systems (screens + mounting + connectivity) | DEL-02-06 | DEL-02-02 |
| Electrical distribution, lighting | DEL-02-06 | DEL-02-02 |
| Interior partitions, finishes, doors (general) | DEL-02-01 | DEL-02-02 |
| Bay-specific fit-up items | DEL-02-02 | DEL-02-01 |

## CBS Mapping Rule

CBS codes are assigned deterministically based on the cost category of each line item:

| CBS Code | Category |
|---|---|
| 03-CONCRETE | Concrete and slab work |
| 05-METALS | Structural/misc metals |
| 10-SPECIALTIES | Lockers, accessories, specialties |
| 11-EQUIPMENT | Mechanical/fire service equipment |
| 09-FINISHES | Interior finishes (paint, tile, flooring, ceilings) |
| 07-THERMAL | Insulation and moisture protection |
| 22-PLUMBING | Plumbing fixtures and piping for fire support rooms |
| 23-MECH | Compressed air distribution piping |

## Warnings

- [INFO] ALLOW_MIXED_METHODS=TRUE: Detail.csv may contain both RATE_TABLE and ALLOWANCE methods.
- [INFO] FALLBACK_POLICY=ALLOW_ALLOWANCE: Items lacking direct rate table evidence may be priced as ALLOWANCE where an allowance basis exists.
- [WARNING] Some support room areas are approximate ranges from Functional Program; quantities derived using midpoint assumptions (see Assumptions_Log.md).
- [WARNING] Compressed air distribution piping quantity is an assumption based on typical bay layout geometry; no detailed routing available at proposal stage.
