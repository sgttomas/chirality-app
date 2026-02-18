# Run Context

## Run Identity

| Field | Value |
|---|---|
| RunID | EST_DEL-02-03_2026-02-18_1100 |
| AsOf | 2026-02-18T11:00:00-07:00 |
| Agent | ESTIMATING (Type 2) |

## Inputs

| Parameter | Value |
|---|---|
| Scope | DEL-02-03 |
| ScopeResolvedSummary | 1 deliverable in scope; 0 excluded; 0 blocked |
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| DEPENDENCY_SOURCES | AUTO (read from DEL-02-03/Dependencies.csv) |
| FALLBACK_POLICY | ALLOW_ALLOWANCE |
| ALLOW_MIXED_METHODS | TRUE |
| UPDATE_LATEST_POINTER | FALSE |
| Rounding | DOLLAR |
| OUTPUT_LABEL | DEL-02-03 |

## Price Sources (resolved)

| # | Path | Type | Notes |
|---|---|---|---|
| 1 | Structural_Concrete_Rates.csv | Rate Table | SC-01 through SC-15; concrete, formwork, rebar, steel, foundations |
| 2 | Building_Envelope_Rates.csv | Rate Table | BE-01 through BE-15; walls, roof, glazing, doors, sealant |
| 3 | Interior_Architectural_Rates.csv | Rate Table | IA-01 through IA-25; partitions, ceilings, flooring, paint, accessories, signage |
| 4 | Mechanical_System_Rates.csv | Rate Table | MS-01 through MS-14; HVAC, plumbing, exhaust, equipment |
| 5 | Electrical_System_Rates.csv | Rate Table | ES-01 through ES-14; power, lighting, telecom, fire alarm |
| 6 | Equipment_Pricing.csv | Rate Table / Allowance | EQ-01 through EQ-15; doors, generator, lockers, workshop equip |
| 7 | Professional_Design_Fees.csv | Rate Table | DF-01 through DF-08; design fees by discipline |
| 8 | Construction_Labour_Rates.csv | Rate Table | T-01 through T-15; trade labour rates |
| 9 | Assumed_Project_Parameters.csv | Parameters | PP-01 through PP-29; areas, quantities, financial benchmarks |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-02-03 | PKG-002 | PKG-002_Main Public Services Building (PSB)/1_Working/DEL-02-03_Public Works Shop Bays, Workshop & Support Spaces | TRUE | Covers SOW-0209, SOW-0210, SOW-0211, SOW-0212 |

## Cost Ownership Rules Applied

These boundary rules were provided in the brief and applied during line item generation:

1. **PW bay functional fit-up** (workshop equip, PPE lockers, storage) -> DEL-02-03 (this estimate)
2. **Overhead doors** -> DEL-02-04 (excluded from this estimate)
3. **HVAC/ventilation** -> DEL-02-05 (excluded from this estimate)
4. **Electrical, lighting** -> DEL-02-06 (excluded from this estimate)
5. **Interior partitions, finishes, doors for shared/common areas** -> DEL-02-01 (excluded from this estimate)
6. **Bay-specific fit-up** (within PW shop zone) -> DEL-02-03 (this estimate)
7. **Bay sumps** -> DEL-02-05 (excluded; mechanical scope)
8. **Water fill stations** -> DEL-02-05 (excluded; plumbing scope)

## CBS Mapping Rule

CBS codes were assigned deterministically based on the following logic:
- `21.03.01` = PW Shop Bay Sealed Concrete / Floor Finish (bay-specific)
- `21.03.02` = PW Shop Bay Functional Fit-up (non-equipment items within bays)
- `21.03.03` = PW Workshop and Storage Areas
- `21.03.04` = PW PPE / Locker Room Fit-up
- `21.03.05` = PW Shop Office and Washroom Fit-up
- `21.03.06` = PW Equipment and Furnishings

The prefix `21` denotes PKG-002 (Main PSB), sub-code `03` denotes DEL-02-03.

## Area Assumptions

| Space | Assumed Area | Basis |
|---|---|---|
| PW Shop Bays (4 bays) | 8,400 sf (780 m2) | PP-12: 4 bays; Datasheet: 2,000-2,200 sf/bay; mid-range 2,100 sf/bay used |
| Workshop/Welding Area | 800 sf (74 m2) | Assumption ASM-003: within bay program per SOW-0212 |
| Warehouse/Parts Storage | 600 sf (56 m2) | Assumption ASM-004: within bay program per SOW-0212 |
| PPE/Locker Room | 1,200 sf (111 m2) | Assumption ASM-005: 40 lockers + showers + change area |
| PPE/First Aid Room | 125 sf (12 m2) | Datasheet: 100-150 sf; midpoint used |
| Shop Office | 200 sf (19 m2) | Assumption ASM-006: single duty office |
| Shop Washroom | 100 sf (9 m2) | Assumption ASM-007: single accessible washroom |
| **Total DEL-02-03 area** | **11,425 sf (1,061 m2)** | Sum of above |

## Warnings

- [WARNING] Mixed methods used: RATE_TABLE (primary) and ALLOWANCE (fallback for EQ-13 workshop equipment). Approved via ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_ALLOWANCE.
- [WARNING] Bay-specific fit-up scope boundary requires human validation: items like sealed concrete in bays are included here; structural slab and reinforcement may also be claimed by DEL-02-04. See Decision_Log.md DEC-RUN-001.
- [WARNING] Support space areas are assumed (no confirmed floor plan). See Assumptions_Log.md.
