# Run Context — EST_DEL-02-01_2026-02-18_0800

## Run Identity

| Field | Value |
|---|---|
| RunID | EST_DEL-02-01_2026-02-18_0800 |
| AsOf | 2026-02-18T08:00:00-07:00 |
| Agent | ESTIMATING (Type 2) |

## Brief Inputs (as provided)

| Parameter | Value |
|---|---|
| SCOPE | DEL-02-01 |
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| OUTPUT_LABEL | DEL-02-01 |
| UPDATE_LATEST_POINTER | FALSE |
| ALLOW_MIXED_METHODS | FALSE |
| FALLBACK_POLICY | STRICT |
| ROUNDING | DOLLAR |

## Resolved Inputs

| Parameter | Resolved Value |
|---|---|
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| DECOMPOSITION_STATUS | Found and loaded (FINAL v1.0, 2026-02-17) |
| DEPENDENCY_SOURCES | AUTO (resolved to: DEL-02-01 Dependencies.csv, 23 rows) |
| PRICE_SOURCES | See Source_Index.md (8 files loaded) |

## Scope Resolution

| Field | Value |
|---|---|
| ScopeResolvedSummary | 1 deliverable in scope; 0 excluded; 0 blocked |
| DeliverableID | DEL-02-01 |
| PackageID | PKG-002 |
| DeliverableName | Architectural Program, Layout & Code Planning |
| DeliverablePath | PKG-002_Main Public Services Building (PSB)/1_Working/DEL-02-01_Architectural Program, Layout & Code Planning |
| Tier | T1 (foundational) |
| Substance | Design + Construction |

## Cost Ownership Boundaries (critical for double-count prevention)

DEL-02-01 OWNS:
- Architectural design fees for this deliverable scope
- Interior partitions (non-structural demising walls, corridor walls, office partitions)
- Interior doors, frames, and hardware (office/admin/shared areas)
- Interior finishes: sealed concrete floors (shared/office areas), ceiling system, wall finishes (paint)
- Accessibility features (ramps, signage, tactile indicators, accessible hardware)
- Code-required signage (exit signs, room identification, accessibility, fire, wayfinding)

DEL-02-01 DOES NOT OWN:
- Fire bay functional fit-up (DEL-02-02)
- PW bay functional fit-up (DEL-02-03)
- Building structure, envelope, roof, foundations, overhead doors (DEL-02-04)
- HVAC, plumbing, exhaust systems (DEL-02-05)
- Electrical distribution, lighting, IT/telecom (DEL-02-06)
- Emergency power and generator (DEL-02-07)
- Meeting room workstation infrastructure — power + data (DEL-02-06)

## Key Parameters Used

| ParameterID | Parameter | Value | Unit | Source |
|---|---|---|---|---|
| PP-05 | Main PSB building footprint | 18,000 | sf | Assumed_Project_Parameters.csv |
| PP-11 | Fire apparatus bays | 4 | each | Assumed_Project_Parameters.csv |
| PP-12 | PW shop bays | 4 | each | Assumed_Project_Parameters.csv |

## Area Breakdown (derived; see Assumptions_Log.md ASM-003)

| Zone | Area (sf) | Basis |
|---|---|---|
| Fire apparatus bays | 8,400 | 4 bays x 2,100 sf avg (Datasheet) |
| PW shop bays | 8,400 | 4 bays x 2,100 sf avg (Datasheet) |
| Office/admin/shared spaces | 5,200 | Balance of 18,000 sf footprint minus circulation (see ASM-003) |
| Circulation/corridors/mechanical | 2,000 | See ASM-003 |
| Total (single-storey, excluding 2nd floor option) | 18,000 | PP-05 minus 6,000 sf overlap; reconciled |

**Note:** The 18,000 sf footprint encompasses bays + shared areas. For DEL-02-01 interior construction pricing, the relevant area is primarily the office/admin/shared zone (~5,200 sf) where partitions, finishes, doors, and ceiling apply. Bay areas receive sealed concrete floor finish but partitions/ceiling are minimal in bays and are attributed to DEL-02-02/DEL-02-03 functional fit-up where applicable.

## CBS Mapping Rule

CBS codes are assigned using the following deterministic mapping:
- `3100` = Architectural design fees (professional services)
- `3200` = Interior partitions and framing
- `3300` = Interior doors, frames, hardware
- `3400` = Interior finishes (flooring, ceiling, paint)
- `3500` = Accessibility and code compliance features
- `3600` = Code-required signage

This mapping is specific to this run and documented here for traceability.

## Warnings

- [WARNING] Multiple shared-space areas are TBD pending Functional Program (Appendix B) access. Quantities for partitions, doors, and finishes are estimated using assumed area breakdowns (see ASM-003).
- [WARNING] No direct rate table entries exist for ceiling systems, accessibility features, or code-required signage. Under STRICT fallback policy, these are priced as TBD where no rate table evidence supports them. See Decision_Log.md DEC-R-003 through DEC-R-005.
- [WARNING] Architectural design fee (DF-01) is expressed as a percentage of construction cost, not as a unit rate. Treated as RATE_TABLE method since DF-01 is a rate table entry expressing the fee rate. See DEC-R-001.
