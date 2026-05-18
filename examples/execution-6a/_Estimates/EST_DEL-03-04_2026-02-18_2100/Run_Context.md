# Run Context: EST_DEL-03-04_2026-02-18_2100

## Run Parameters

| Field | Value |
|-------|-------|
| RunID | EST_DEL-03-04_2026-02-18_2100 |
| AsOf | 2026-02-18T21:00:00-07:00 |
| Scope | DEL-03-04 (Site Utilities Distribution & Allowance-Based Tie-Ins) |
| ScopeResolvedSummary | 1 deliverable in scope (DEL-03-04); Package PKG-003 |
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| PRICE_SOURCES | Underground_Utility_Rates.csv, Construction_Labour_Rates.csv, Professional_Design_Fees.csv, Fees_Permits_Insurance.csv, Assumed_Project_Parameters.csv |
| DECOMPOSITION_PATH | _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md (available; validated) |
| DEPENDENCY_SOURCES | AUTO (resolved: DEL-03-04/Dependencies.csv; 16 rows ACTIVE) |
| FALLBACK_POLICY | ALLOW_ALLOWANCE |
| ALLOW_MIXED_METHODS | TRUE |
| UPDATE_LATEST_POINTER | FALSE |
| Rounding | DOLLAR |
| OUTPUT_LABEL | DEL-03-04 |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---------------|-----------|------|---------|-------|
| DEL-03-04 | PKG-003 | PKG-003_Site & Civil Works/1_Working/DEL-03-04_Site Utilities Distribution & Allowance-Based Tie-Ins/ | TRUE | Dual-method: RATE_TABLE (distribution) + ALLOWANCE (tie-ins per DEC-004) |

## CBS Mapping Rule

CBS codes are assigned using the following deterministic mapping for DEL-03-04:

| CBS | Description | Rule |
|-----|-------------|------|
| 31.40 | Site Utilities -- Water Distribution | Water main and service connection piping from tie-in point to buildings |
| 31.41 | Site Utilities -- Sanitary Sewer Distribution | Sanitary sewer main and service connections from tie-in point to buildings |
| 31.42 | Site Utilities -- Gas Distribution | Gas service piping from tie-in point to buildings |
| 31.43 | Site Utilities -- Power Distribution | Power duct bank and conduit from tie-in point to buildings |
| 31.44 | Site Utilities -- Telecom Distribution | Telecom conduit from tie-in point to buildings |
| 31.45 | Site Utilities -- Common Trench | Shared trench where utilities are co-located |
| 31.49 | Site Utilities -- Tie-In Allowance (DEC-004) | Cash allowance for municipal tie-in execution (all utilities) |
| 31.50 | Site Utilities -- Utility Connection Fees | Municipal / provider connection fees |
| 31.00 | Site Utilities -- Design | Civil engineering design fees for utility routing |

## Quantity Derivation (Assumptions)

Utility run lengths are derived from Assumed_Project_Parameters.csv site dimensions and standard estimating practice:

- **Site developable area:** ~12 acres (PP-09); buildings + paving + yards = ~4.5 acres (PP-10)
- **Main PSB footprint:** ~18,000 sf, approximately 160 ft x 110 ft (PP-05)
- **Cold Storage footprint:** 60 ft x 100 ft (PP-07, DEC-001)
- **Assumed distance from municipal stubs to Main PSB:** 120 m (ASM-001). Basis: stubs at site corner per Addendum 03 s1.6; building located toward center of developable area; 12-acre parcel with ~4.5 acres developed suggests moderate setback from property line.
- **Assumed distance from Main PSB to Cold Storage:** 40 m (ASM-002). Basis: cold storage is a separate ancillary building on the same site; typical separation for operational layout.
- **Total distribution length (stub to Main PSB):** 120 m per utility
- **Branch to Cold Storage (from main run or building):** 40 m per applicable utility
- **Common trench:** Assumed 100 m of shared trench where water, sewer, and gas share a corridor (ASM-003). Remainder of utility lengths in separate trenches or by third-party utility installers.
- **Water service connections:** 2 (Main PSB + Cold Storage) -- Cold Storage water requirement is TBD per Datasheet (ASM-004)
- **Sanitary service connections:** 1 (Main PSB only) -- Cold Storage sanitary not confirmed required (ASM-005)
- **Power duct bank:** 120 m to Main PSB + 40 m branch to Cold Storage = 160 m total
- **Telecom conduit:** 120 m to Main PSB only (Cold Storage telecom TBD, assumed not required per Datasheet) (ASM-006)
- **Gas service:** 120 m to Main PSB only (Cold Storage is unheated; gas not required) (ASM-007)

**DEMARCATION POINT:** 1.5 m outside building foundation wall. DEL-03-04 owns from municipal stub to 1.5 m outside building. PKG-002 owns from 1.5 m outside building to interior.

## Warnings

- [WARNING] DEC-004 ALLOWANCE VALUE PENDING OWNER CONFIRMATION: UU-12 recommended value of $35,000 used; Owner must confirm or set final allowance amount.
- [WARNING] UTILITY RUN LENGTHS ARE ASSUMED: Actual lengths depend on post-award survey files (DEP-03-04-007) and underground services drawings (DEP-03-04-006), neither of which are available at proposal stage.
- [WARNING] COLD STORAGE UTILITY REQUIREMENTS PARTIALLY TBD: Water and sanitary service to Cold Storage are assumptions pending design confirmation.
- [WARNING] MIXED METHODS USED: RATE_TABLE for on-site distribution; ALLOWANCE for tie-in execution (DEC-004) and utility connection fees. Authorized by ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_ALLOWANCE.
