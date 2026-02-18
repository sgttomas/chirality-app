# Blockers Report: EST_DEL-03-02_2026-02-18_1130

## Summary

| Metric | Value |
|---|---|
| Total dependencies reviewed | 11 (DEP-0302-001 through DEP-0302-011) |
| Blocking prerequisites affecting estimate | 2 |
| Non-blocking interfaces | 2 |
| Satisfied prerequisites | 2 |
| Anchor/traceability rows | 3 |
| External constraints | 2 |

## Blocking Prerequisites (Affecting Estimate Quality)

### BLOCKER-1: Cut/Fill Quantities Not Available

| Field | Value |
|---|---|
| Source | Datasheet.md item B-001; REQ-3216 |
| Related Dependency | DEP-0302-005 (interface with DEL-03-01 for site plan/building locations affecting grading) |
| Impact on Estimate | Cut volume (L-003) and fill volume (L-004) are assumptions. Combined $105,000 of the $472,062 total (22%) is based on assumed quantities rather than measured takeoff. |
| Mitigation Applied | Conservative mid-range quantities assumed (ASM-001, ASM-002). |
| Resolution Path | Civil engineer to extract from TPN46 drawings or perform independent quantity takeoff from post-award topographic survey. |

### BLOCKER-2: Stormwater Pond Sizing Criteria TBD

| Field | Value |
|---|---|
| Source | REQ-3212 / Specification item F-001; DEP-0302-004 (prerequisite from DEL-03-05 for flood fringe/environmental approvals) |
| Related Dependency | DEP-0302-004 (DEL-03-05 environmental/flood approvals required before pond construction) |
| Impact on Estimate | Pond excavation (L-010) and outlet (L-011) total $52,500 (11% of total) based on assumed pond volume. Design storm return period, pond capacity, and outlet flow rate are all TBD. |
| Mitigation Applied | Conservative pond volume assumed (ASM-005); outlet priced as lump sum (ASM-006). |
| Resolution Path | Civil engineer to determine sizing per municipal development standards; AEPA Water Act approval (external gate) may affect design. |

## Non-Blocking Interfaces (Noted, Not Preventing Estimate)

### INTERFACE-1: DEL-03-01 Site Plan Input

| Field | Value |
|---|---|
| Dependency | DEP-0302-005 |
| Description | DEL-03-02 requires site plan, building locations, and pond location from DEL-03-01 as inputs affecting grading and drainage layout. |
| Impact on Estimate | Topsoil restoration area (L-012, ASM-008) and drainage swale lengths (L-009, ASM-004) may change once site plan is finalized. |
| Status | DEL-03-01 estimate exists (EST_DEL-03-01_2026-02-18_1900); site plan layout is a design-phase deliverable, not yet finalized. |

### INTERFACE-2: Downstream Deliverables (DEL-03-03, DEL-03-04)

| Field | Value |
|---|---|
| Dependencies | DEP-0302-006, DEP-0302-007 |
| Description | DEL-03-02 provides subgrade specs and S-2 sulphate resistance requirement downstream to DEL-03-03 (pavements/aprons) and DEL-03-04 (utility structures). |
| Impact on Estimate | No cost impact on DEL-03-02 estimate; these are outgoing information flows. |

## Satisfied Prerequisites

| Dependency | Description | Status |
|---|---|---|
| DEP-0302-008 | Geotechnical Investigation Report (USG1123, Feb 2021) | SATISFIED -- document available in _Sources/references/ |
| DEP-0302-009 | Site Grading drawings (Tagish Engineering TPN46) | SATISFIED -- document available in _Sources/references/ |

## External Constraints (Noted)

| Dependency | Description | Status |
|---|---|---|
| DEP-0302-010 | Geotechnical services retention (OSR 10.3.6 / REQ-3214) | PENDING -- DB must retain geotech; cost included in L-014 |
| DEP-0302-011 | Alberta OHS Code 2009 Part 32 (excavation safety) | PENDING -- compliance requirement; no direct cost line item (safety costs in PKG-001 H&S scope) |
