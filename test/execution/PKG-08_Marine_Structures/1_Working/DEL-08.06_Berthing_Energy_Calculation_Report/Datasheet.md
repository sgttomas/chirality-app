# Datasheet: DEL-08.06 Berthing Energy Calculation Report

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-08.06 |
| Name | Berthing Energy Calculation Report |
| Package | PKG-08 Marine Structures |
| Discipline | Marine |
| Type | Report |
| Responsible | D&B Contractor |
| Lifecycle State | INITIALIZED |

## Description

**Purpose (source-anchored):** Documents analysis and results for berthing energy calculation report required for design verification and approvals. *(Source: Decomposition line 286 + `_CONTEXT.md`)*

**Package scope context:** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

**Report objective:** Establishes berthing energy demands that the fender system must absorb when design vessels contact the berth under specified approach conditions.

## Minimum Artifact Content

*(Source: Decomposition line 286)*

| Artifact | Description | Status |
|---|---|---|
| Berthing energy calculations | Kinetic energy calculations for design vessels under berthing scenarios | Required |
| Design basis | Vessel particulars, approach velocities, berthing coefficients, environmental assumptions | Required |
| Assumptions | Explicit list of assumptions with rationale | Required |
| Summary report | Conclusions, governing case identification, fender demand summary | Required |

## Report Metadata (TBD)

| Attribute | Value |
|---|---|
| Report number | **TBD** *(e.g., RPT-MAR-08-003)* |
| Revision / issue status | **TBD** |
| Design vessel(s) | **TBD** *(from ER or project basis)* |
| Berthing configuration | **TBD** *(side-berthing assumed for product tanker; confirm from ER/project basis)* |
| Calculation methodology | **ASSUMPTION:** Kinetic energy method per PIANC WG 33 or BS 6349-4 *(confirm from ER)* |

## Key Input Parameters (TBD)

| Parameter | Description | Typical Range/Value | Status |
|---|---|---|---|
| Vessel displacement (M) | Mass for energy calculation (DWT laden/ballast) | **TBD** *(design vessel from ER)* | **TBD** |
| Approach velocity (V) | Normal velocity at contact | 0.10–0.50 m/s depending on conditions | **TBD** *(from ER, site exposure, operations basis)* |
| Added mass coefficient (Cm) | Hydrodynamic effects | 1.4–1.8 for broadside | **TBD** *(from standards: PIANC, BS 6349-4)* |
| Eccentricity coefficient (Ce) | Rotational energy dissipation | 0.5–1.0 (bow/stern vs amidships) | **TBD** *(from berthing geometry)* |
| Configuration coefficient (Cc) | Cushioning effects | 0.8–1.0 for pile structures | **TBD** *(from standards)* |
| Softness coefficient (Cs) | Relative stiffness | 0.9–1.0 for stiff structures | **TBD** *(from standards)* |
| Safety factor | Applied to calculated energy | 1.5–2.0 typical | **TBD** *(from ER or standards)* |

## Interfaces (Advisory)

*Dependencies NOT_TRACKED; interfaces for context only:*

| Related Deliverable | Interface |
|---|---|
| DEL-08.07 Fender Deflection Characteristics | Output: energy demand → fender selection input |
| DEL-08.08 Fender Supplier Verification | Output: design energy → supplier verification basis |
| DEL-08.03 Marine Structures Calculations | Fender reaction loads to structure |
| DEL-08.09 Mooring Analysis | Shared vessel/environmental basis |

## Cross-Document Links

| Document | Link |
|---|---|
| Specification.md | Requirements R-001 through R-006 |
| Guidance.md | Methodology rationale, coefficient guidance, checklist |
| Procedure.md | Step-by-step workflow aligned to requirements |

## Key TBDs

1. ER clauses for berthing energy methodology and criteria
2. Design vessel particulars and berthing scenarios
3. Applicable standards (PIANC, BS 6349, OCIMF, or other)
4. Safety factors and acceptance criteria

## Sources

- Decomposition line 286
- ER Vol 2 Parts 1-2 *(clause locations TBD)*
