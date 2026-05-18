# Blockers Report

## Run: EST_DEL-02-03_2026-02-18_1100

## Critical Blockers for Estimating: NONE

No critical blockers prevented the generation of this estimate. All required pricing sources were available and sufficient to produce line-item estimates (with allowance fallback where needed).

## Execution Dependencies (Informational)

The following dependencies from `Dependencies.csv` are noted for awareness. They do not block estimating but will affect design development and may refine quantities in future estimate iterations.

### Upstream Prerequisites

| DependencyID | Target | Statement | Impact on Estimate |
|---|---|---|---|
| DEP-0203-006 | DEL-02-01 (Architectural Program) | DEL-02-03 requires overall building layout and footprint concept from DEL-02-01 to establish PW shop zone boundary | Area assumptions (ASM-001 through ASM-007) will be refined once DEL-02-01 layout is available |
| DEP-0203-007 | DEL-02-04 (Structure/Envelope) | DEL-02-03 requires structural bay dimensions, overhead door specification basis, and clear height confirmation | Bay areas and wall quantities may change; scope boundary for slab (DEC-RUN-001) requires coordination |
| DEP-0203-008 | DEL-02-05 (Mechanical) | DEL-02-03 requires bay sump locations, ventilation interface points, water fill station rough-in | No direct cost impact on DEL-02-03 (mechanical items excluded per cost ownership) |
| DEP-0203-009 | DEL-02-06 (Electrical) | DEL-02-03 requires lighting levels, electrical outlet positions, key fob access points | No direct cost impact on DEL-02-03 (electrical items excluded per cost ownership) |

### Constraints

| DependencyID | Constraint | Statement | Impact on Estimate |
|---|---|---|---|
| DEP-0203-014 | Owner scope selections | Owner must confirm whether optional wash bay (SOW-0500) is included, which impacts PW bay count | If wash bay replaces 1 PW bay: bay count drops from 4 to 3; bay-area-driven lines decrease by ~25% ($13,000 reduction) |
| DEP-0203-016 | Alberta Building Code | Support spaces must comply with ABC for occupancy, fire separation, accessibility, plumbing fixture counts | Partitions (L-013, L-025) and accessibility items (L-018, L-029) are included; fixture counts may increase if ABC requires more than assumed |
