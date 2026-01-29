# Datasheet: DEL-13.03 Storage Tank Design Calculations

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-13.03 |
| **Deliverable Name** | Storage Tank Design Calculations |
| **Package** | PKG-13 Storage Tanks |
| **Discipline** | Mechanical |
| **Type** | Calculation |
| **Responsible Party** | D&B Contractor |
| **Status** | INITIALIZED |

**Source:** `_CONTEXT.md`

---

## Attributes

### Calculation Package Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Calculation Numbers** | **TBD** — Per project calculation numbering system | |
| **Calculation Format** | **TBD** — Handwritten, spreadsheet, or software output per project standards | |
| **Software/Tools Used** | **TBD** — May include Excel, MathCAD, specialized tank design software, FEA software for seismic | |
| **Primary Design Code** | API 650: Welded Tanks for Oil Storage | Decomposition PKG-13 Scope |
| **Seismic Code** | API 650 Appendix E; NBC 2020 | ASSUMPTION based on BC location |
| **Revision** | **TBD** — Initial issue or current revision | |
| **Classification** | **TBD** — Per project document control procedures | |

### Calculation Scope

| Calculation Package | Quantity | Description | Source |
|---------------------|----------|-------------|--------|
| **API 650 Tank Design Calculations** | 3 (one per tank) | Shell thickness, bottom design, roof design, wind/seismic stability, nozzle reinforcement | _CONTEXT.md (Anticipated Artifacts) |
| **Foundation Calculations** | **TBD** (may be 1 common or 3 individual) | Foundation type selection, bearing pressure, settlement, anchor bolt design | _CONTEXT.md (Anticipated Artifacts) |
| **Seismic Calculations** | 3 (one per tank) or combined | Seismic analysis per API 650 Appendix E: base shear, overturning, sloshing, anchorage | _CONTEXT.md (Anticipated Artifacts) |

**Note:** Foundation structural design calculations may be performed by PKG-05 (Concrete Structures); this deliverable focuses on tank-to-foundation loading and interface requirements.

**Source:** _CONTEXT.md; ASSUMPTION based on typical responsibility split

### Calculation Types and Methods

| Calculation Type | Method | Standard | Source |
|------------------|--------|----------|--------|
| **Shell Thickness** | Hydrostatic pressure method per API 650 Section 5.6 | API 650 | API 650 standard |
| **Bottom Design** | Bottom plate thickness and annular plate requirements per API 650 Section 5.4 and 5.5 | API 650 | API 650 standard |
| **Roof Design** | Roof plate thickness and structural design per API 650 Section 5.10 | API 650 | API 650 standard |
| **Wind Stability** | Shell stability and stiffener requirements per API 650 Section 5.9 | API 650 | API 650 standard |
| **Seismic Analysis** | Base shear, overturning, sloshing, anchorage per API 650 Appendix E | API 650 Appendix E; NBC 2020 | ASSUMPTION based on BC location |
| **Foundation Loading** | Dead load, live load, seismic loads, wind loads transmitted to foundation | API 650; typical structural practice | ASSUMPTION |
| **Nozzle Reinforcement** | Reinforcement area method per API 650 Section 5.7 | API 650 | API 650 standard |
| **Settlement Analysis** | Maximum allowable settlement per API 650 Appendix B | API 650 | API 650 standard |

---

## Conditions

### Design Input Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| **Tank Capacity** | 3 × 15,000 MT (total 45,000 MT) | Decomposition document, Section 1.1 |
| **Product** | CSD (Crude Super Degummed) canola oil | Decomposition document, Section 1.1 |
| **Product Specific Gravity** | **TBD** — Required for capacity-to-volume conversion and hydrostatic pressure calculation | |
| **Product Temperature Range** | **TBD** — Affects material selection and thermal loads | |
| **Operating Pressure** | Atmospheric (internal pressure ~0 psig, slight vacuum or pressure from venting) | ASSUMPTION based on API 650 scope |
| **Design Liquid Level** | **TBD** — Typically full capacity for design purposes | |

### Environmental Loads

| Load Type | Value | Source |
|-----------|-------|--------|
| **Site Location** | Fraser Surrey Terminal, Surrey, BC | Decomposition document, Section 1 |
| **Seismic Parameters** | **TBD** — Site-specific PGA, spectral acceleration per NBC 2020 or site study | |
| **Design Wind Speed** | **TBD** — Per NBC 2020 for Surrey, BC location | |
| **Snow Load** | **TBD** — Per NBC 2020 for Surrey, BC location (roof loading) | |
| **Ambient Temperature Range** | **TBD** — Affects material selection and thermal loads | |
| **Soil Bearing Capacity** | **TBD** — From geotechnical report (DEL-02.04) | |

### Load Cases

| Load Case | Description | Source |
|-----------|-------------|--------|
| **LC-01: Operating (Full)** | Tank full, normal operating conditions, no seismic/wind | API 650 normal condition |
| **LC-02: Operating (Empty)** | Tank empty, normal conditions (for uplift/stability check) | API 650 normal condition |
| **LC-03: Hydrostatic Test** | Tank full of water to test level, test condition | API 650 Section 7 |
| **LC-04: Wind** | Operating + design wind loads | API 650 Section 5.9; NBC 2020 |
| **LC-05: Seismic** | Operating (varying fill levels) + seismic loads per Appendix E | API 650 Appendix E |
| **LC-06: Wind + Seismic** | **TBD** — Load combination per NBC 2020 if required | |
| **LC-07: Thermal** | **TBD** — Thermal expansion/contraction if heating system provided | |

**Source:** API 650 load cases; NBC 2020 load combinations

---

## Construction

### Calculation Inputs

**Geometric Inputs:**
- Tank diameter, height, shell course configuration — **TBD** (optimized during calculation process)
- Roof type and configuration — **TBD** (cone, dome, floating)
- Nozzle sizes, quantities, locations — **TBD** (from process requirements and P&IDs)
- Foundation type and dimensions — **TBD** (from geotechnical recommendations)

**Material Inputs:**
- Shell material grade and allowable stress — **TBD** (API 650 Table 4-1)
- Bottom material grade — **TBD**
- Roof material grade — **TBD**
- Minimum design metal temperature (MDMT) — **TBD** (affects material selection per API 650 Appendix D)

**Source:** DEL-13.01 (drawings provide geometry after optimization); DEL-13.02 (specification provides materials)

### Calculation Outputs

**Primary Outputs:**
- Shell course thicknesses (bottom course, intermediate courses, top course)
- Bottom plate thickness and annular plate requirements
- Roof plate thickness and structural member sizes
- Wind girder requirements (if needed)
- Stiffening ring requirements (if needed)
- Anchor chair and anchor bolt requirements (if seismic anchorage required)
- Foundation loading (vertical load, overturning moment, base shear)
- Nozzle reinforcement pad dimensions

**Verification Outputs:**
- Tank stability ratios (overturning, buckling)
- Settlement analysis results
- Stress checks and utilization ratios
- Compliance statements for API 650 requirements

**Source:** API 650 output requirements; typical calculation deliverables

### Calculation Documentation

| Document Component | Description | Source |
|--------------------|-------------|--------|
| **Cover Sheet** | Calculation title, number, project, date, revision, preparer, checker, approver | Project calculation format |
| **Scope and Objective** | What is being calculated and why | Calculation best practice |
| **Design Basis** | Codes, standards, references, input parameters, assumptions | Calculation best practice |
| **Methodology** | Calculation approach and methods used | Calculation best practice |
| **Calculations** | Detailed calculations with formulas, values, and results | Calculation content |
| **Results Summary** | Tabulated results and key findings | Calculation best practice |
| **Conclusions** | Compliance statements, recommendations, actions required | Calculation best practice |
| **Appendices** | Supporting data, software outputs, charts, tables | Calculation best practice |
| **References** | List of referenced documents and standards | Calculation best practice |

---

## References

### Source Documents

1. `_CONTEXT.md` — Deliverable identity, description, anticipated artifacts
2. Decomposition document (`/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`):
   - Section 1.1 (Key Parameters): Capacity, product, location
   - Section 5, PKG-13: Scope (API 650 tanks)
   - Section 5, DEL-13.03: Description and anticipated artifacts
3. `_REFERENCES.md` — Reference index (ER PDFs location TBD)

### Expected Reference Documents (TBD — ER Extraction Pending)

1. API 650: Welded Tanks for Oil Storage — **Location TBD** (primary design standard)
2. API 650 Appendix E: Seismic Design of Storage Tanks — **Location TBD**
3. API 650 Appendix D: Rules for Designing Tanks for Small Internal Pressures — **Location TBD** (if applicable)
4. API 650 Appendix B: Settlement — **Location TBD**
5. NBC 2020: National Building Code of Canada — **Location TBD** (wind, snow, seismic loads)
6. Volume 2 Part 2: Employer's Requirements - Civil & Process Mechanical Works — **Location TBD** (design criteria)
7. DEL-02.04: Geotechnical Reports — Bearing capacity, settlement characteristics
8. Product specification for CSD canola oil — **Location TBD** (specific gravity, temperature range)

### Related Deliverables

| Deliverable | Relationship |
|-------------|-------------|
| DEL-13.01: Storage Tank Design Drawing Set | Drawings implement geometry determined by these calculations |
| DEL-13.02: Storage Tank Technical Specification | Specification references these calculations for design verification |
| DEL-13.04: Storage Tank Data Sheet Package | Data sheets reference calculation results |
| DEL-02.04: Geotechnical Reports | Provides soil bearing capacity and settlement inputs |
| DEL-05.03: Concrete Structures Design Calculations | Foundation structural design (coordinates with tank foundation loading from this deliverable) |

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Calculation scope, methods, inputs/outputs defined. Cross-document consistency verified. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
