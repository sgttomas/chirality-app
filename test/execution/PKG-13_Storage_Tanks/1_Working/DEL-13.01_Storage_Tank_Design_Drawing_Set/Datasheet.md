# Datasheet: DEL-13.01 Storage Tank Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-13.01 |
| **Deliverable Name** | Storage Tank Design Drawing Set |
| **Package** | PKG-13 Storage Tanks |
| **Discipline** | Mechanical |
| **Type** | Drawing |
| **Responsible Party** | D&B Contractor |
| **Status** | INITIALIZED |

**Source:** `_CONTEXT.md`

---

## Attributes

### Tank Configuration

| Attribute | Value | Source |
|-----------|-------|--------|
| **Number of Tanks** | 3 | Decomposition document, Section 1.1 (Key Parameters) |
| **Capacity per Tank** | 15,000 MT | Decomposition document, Section 1.1 (Key Parameters) |
| **Total Storage Capacity** | 45,000 MT | Decomposition document, Section 1.1 (Key Parameters) |
| **Product** | CSD (Crude Super Degummed) canola oil | Decomposition document, Section 1.1 (Key Parameters) |
| **Product Specific Gravity** | **TBD** — Requires ER extraction (Volume 2 Part 2) or product data sheet |
| **Product Temperature Range** | **TBD** — Requires ER extraction (Volume 2 Part 2) for operating temperature specification |
| **Tank Type** | Atmospheric storage tank | ASSUMPTION: Based on API 650 scope (PKG-13) and product type |
| **Tank Standard** | API 650 | Decomposition document, PKG-13 Scope |

### Tank Geometry

| Attribute | Value | Source |
|-----------|-------|--------|
| **Tank Diameter** | **TBD** — Requires design calculations (DEL-13.03) based on capacity and D/H optimization | |
| **Tank Height** | **TBD** — Requires design calculations (DEL-13.03) based on capacity and D/H optimization | |
| **Shell Courses** | **TBD** — Requires design calculations (DEL-13.03) for shell plate layout | |
| **Shell Plate Thickness** | **TBD** — Requires design calculations (DEL-13.03) per API 650 hydrostatic design | |
| **Bottom Plate Thickness** | **TBD** — Requires design calculations (DEL-13.03) per API 650 | |
| **Roof Type** | **TBD** — Requires ER extraction (Volume 2 Part 2) or design selection (cone/dome/floating) | |
| **Roof Configuration** | **TBD** — Requires ER extraction or design selection (self-supporting/rafter-supported) | |

### Foundation

| Attribute | Value | Source |
|-----------|-------|--------|
| **Foundation Type** | **TBD** — Requires geotechnical report (DEL-02.04) and design calculations (DEL-13.03); typical types: ring wall, mat, piles | |
| **Foundation Design Standard** | **TBD** — Requires specification (DEL-13.02); likely API 650 Appendix B and applicable structural codes | |
| **Bearing Capacity** | **TBD** — Requires geotechnical report (DEL-02.04) for allowable bearing pressure | |
| **Seismic Requirements** | Required (BC location) | ASSUMPTION: Seismic design per NBC 2020 and API 650 Appendix E for Surrey, BC location |

### Internals and Appurtenances

| Attribute | Value | Source |
|-----------|-------|--------|
| **Agitators** | Required (3 agitators) | _CONTEXT.md (Anticipated Artifacts); ASSUMPTION: One per tank |
| **Agitator Type** | **TBD** — Requires specification (DEL-13.02) or vendor selection (side-entry, top-entry, or bottom-mounted) | |
| **Overflow Protection** | Required | Decomposition document, PKG-13 Scope |
| **Water Draw-off** | Required | Decomposition document, PKG-13 Scope |
| **Phase 2 Connections** | Required | Decomposition document, PKG-13 Scope; OBJ-8 (Future Expandability) |
| **Heating System** | **TBD** — Requires ER extraction (Volume 2 Part 2) for product viscosity management requirements | |
| **Level Instrumentation** | **TBD** — Requires coordination with PKG-20 (Field Instrumentation) for type and mounting | |
| **Temperature Instrumentation** | **TBD** — Requires coordination with PKG-20 if heating system provided | |

### Nozzles and Connections

| Attribute | Value | Source |
|-----------|-------|--------|
| **Nozzle Schedule** | Required | _CONTEXT.md (Anticipated Artifacts: nozzle schedules) |
| **Inlet Nozzles** | **TBD** — Requires P&ID coordination and process design (quantity, size, location) | |
| **Outlet Nozzles** | **TBD** — Requires P&ID coordination and process design (quantity, size, location) | |
| **Vent Connections** | **TBD** — Requires design per API 650 Appendix F and ER extraction for venting requirements | |
| **Overflow Connections** | **TBD** — Requires design and ER extraction for overflow protection system | |
| **Drain Connections** | **TBD** — Requires design for tank draining and water draw-off | |
| **Instrumentation Connections** | **TBD** — Requires coordination with PKG-20 for level, temperature, pressure nozzles | |

### Drawing Set Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Drawing Numbers** | **TBD** — Per project numbering system and document control procedures | |
| **Sheet Size** | **TBD** — Per project CAD standards (typically ISO A1 or ANSI D) | |
| **Scale** | **TBD** — Varies by drawing type (GAs: 1:50 to 1:100; details: 1:10 to 1:25) | |
| **CAD Standard** | **TBD** — Per project CAD manual (software, layers, symbology, line weights) | |
| **Drawing Format** | **TBD** — Per project document management requirements (PDF, DWG) | |
| **Classification** | **TBD** — Per project document control procedures (e.g., "Issued for Construction") | |

---

## Conditions

### Operating Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| **Operating Temperature** | **TBD** — Requires ER extraction (Volume 2 Part 2) or product specification for canola oil storage temperature | |
| **Operating Pressure** | Atmospheric | ASSUMPTION: Based on API 650 scope and product type (low volatility) |
| **Filling Rate** | **TBD** — Requires coordination with PKG-10 (Railcar Unloading System) for maximum flow rate | |
| **Turnover Rate** | **TBD** — Requires process design and throughput analysis based on 1,000,000 MT/annum facility capacity | |
| **Product Compatibility** | **TBD** — Requires material selection (DEL-13.02) for internal coating and materials | |
| **Hazardous Area Classification** | **TBD** — Requires facility hazardous area study and ER extraction | |

### Design Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| **Design Temperature Range** | **TBD** — Requires ER extraction and API 650 material selection analysis | |
| **Design Wind Speed** | **TBD** — Requires ER extraction (Volume 2 Part 2) and NBC 2020 for Surrey, BC location | |
| **Seismic Design** | Required (BC location) | ASSUMPTION: Seismic zone requires seismic design per NBC 2020 and API 650 Appendix E |
| **Seismic Parameters** | **TBD** — Requires ER extraction or site-specific seismic study for PGA, spectral acceleration | |
| **Snow Load** | **TBD** — Requires ER extraction (Volume 2 Part 2) and NBC 2020 for Surrey, BC climate | |
| **Site Location** | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | Decomposition document, Section 1 (Project Context) |
| **Design Life** | **TBD** — Requires ER extraction (Volume 2 Part 2) for facility design life specification | |

### Limiting Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| **Maximum Fill Level** | **TBD** — Requires design and safety factor per API 650 (typically 95-98% of tank height) | |
| **Minimum Operating Temperature** | **TBD** — Requires material selection and brittle fracture analysis per API 650 | |
| **Maximum Operating Temperature** | **TBD** — Requires ER extraction for product heating limits if applicable | |
| **Emergency Venting Capacity** | **TBD** — Requires design per API 650 Appendix F or API 2000 for emergency venting | |
| **Tank Spacing (Fire Protection)** | **TBD** — Requires coordination with PKG-23 (Fire Protection) for spacing requirements | |

---

## Construction

### Materials

| Material | Specification | Source |
|----------|---------------|--------|
| **Shell Plates** | **TBD** — Requires specification (DEL-13.02) and API 650 material selection (typically carbon steel per ASTM A36, A283, or A131) | |
| **Bottom Plates** | **TBD** — Requires specification (DEL-13.02) per API 650 (typically same as shell or A36) | |
| **Roof Plates** | **TBD** — Requires specification (DEL-13.02) per API 650 (typically A36 or similar) | |
| **Structural Supports** | **TBD** — Requires specification (DEL-13.02) for rafters, columns, wind girders per applicable structural codes | |
| **Nozzle Material** | **TBD** — Requires specification (DEL-13.02) per ASME B31.3 or API 650 (typically carbon steel matching shell) | |
| **Coating System (Internal)** | **TBD** — Requires coordination with PKG-26 (Protective Coatings & Painting) and product compatibility analysis | |
| **Coating System (External)** | **TBD** — Requires coordination with PKG-26 for corrosion protection and UV resistance | |

### Configuration

| Item | Description | Source |
|------|-------------|--------|
| **Tank Arrangement** | 3 tanks | Decomposition document, Section 1.1 (Key Parameters) |
| **Tank Spacing** | **TBD** — Requires site layout, fire protection coordination (PKG-23), and piping routing considerations | |
| **Access Provisions** | **TBD** — Requires ER extraction and safety requirements for personnel access during operations and maintenance | |
| **Walkways/Platforms** | **TBD** — Requires ER extraction and design for roof access, platform access, sampling points | |
| **Ladders** | **TBD** — Requires ER extraction and design per API 650 and CSA Z259 (fall protection) | |
| **Dyke/Bunding** | **TBD** — Requires ER extraction and PKG-05 (Concrete Structures) coordination for containment capacity | |

### Structural Details

| Detail | Description | Source |
|--------|-------------|--------|
| **Roof Support** | **TBD** — Requires roof type selection and design calculations (DEL-13.03) for rafter/column support if required | |
| **Wind Girders** | **TBD** — Requires design calculations (DEL-13.03) and API 650 wind stability analysis | |
| **Stiffening Rings** | **TBD** — Requires design calculations (DEL-13.03) and API 650 shell stability requirements | |
| **Anchor Chairs** | **TBD** — Requires seismic design per API 650 Appendix E if anchorage is required | |
| **Foundation Anchor Bolts** | **TBD** — Requires seismic design and foundation interface coordination with PKG-05 | |

### Anticipated Drawing Set Content

| Drawing Type | Description | Source |
|-------------|-------------|--------|
| **Tank General Arrangements (3)** | Overall tank configuration, dimensions, nozzle locations, one GA per tank | _CONTEXT.md (Anticipated Artifacts); Decomposition DEL-13.01 |
| **Foundation Drawings** | Foundation plan, details, anchor bolt arrangement, loading diagrams | _CONTEXT.md (Anticipated Artifacts); Decomposition DEL-13.01 |
| **Nozzle Schedules (3)** | Nozzle table with sizes, ratings, orientations, connections, one schedule per tank | _CONTEXT.md (Anticipated Artifacts); Decomposition DEL-13.01 |
| **Roof Details** | Roof structure, support, access, venting details | _CONTEXT.md (Anticipated Artifacts); Decomposition DEL-13.01 |
| **Agitator Drawings** | Agitator mounting, support details, clearances, loading | _CONTEXT.md (Anticipated Artifacts); Decomposition DEL-13.01 |
| **Appurtenance Details** | Overflow, water draw-off, Phase 2 connections | Decomposition PKG-13 Scope |

---

## References

### Source Documents

1. `_CONTEXT.md` — Deliverable identity, description, anticipated artifacts
2. Decomposition document (`/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`):
   - Section 1.1 (Project Overview — Key Parameters): Storage capacity (45,000 MT in 3 × 15,000 MT tanks), product type (CSD canola oil), throughput (1,000,000 MT/annum)
   - Section 1.2 (Scope Focus): Contractor's scope only, interface connections
   - Section 2 (Project Objectives): OBJ-1 (Safe & Reliable Operation), OBJ-3 (Storage Capacity), OBJ-8 (Future Expandability)
   - Section 5, PKG-13: Scope (API 650 tanks, internals, agitators, overflow protection, water draw-off, Phase 2 connections)
   - Section 5, DEL-13.01: Description ("Defines the design arrangement and details for storage tank per ER requirements") and anticipated artifacts
3. `_REFERENCES.md` — Reference index (ER PDFs location TBD)

### Expected Reference Documents (TBD — ER Extraction Pending)

1. Volume 2 Part 1: Employer's Requirements - General Requirements — **Location TBD**
2. Volume 2 Part 2: Employer's Requirements - Civil & Process Mechanical Works — **Location TBD**
3. API 650: Welded Tanks for Oil Storage — **Location TBD** (ASSUMPTION: applicable standard per PKG-13 scope)
4. API 650 Appendix E: Seismic Design of Storage Tanks — **Location TBD** (ASSUMPTION: applicable for BC seismic zone)
5. API 650 Appendix F: Recommended Practice for Atmospheric and Low-Pressure Storage Tank Venting — **Location TBD** (ASSUMPTION: applicable for venting design)
6. National Building Code of Canada 2020 — **Location TBD** (ASSUMPTION: applicable for BC location wind, snow, seismic loads)
7. CSA standards for structural steel and seismic design — **Location TBD**

### Related Deliverables

| Deliverable | Relationship |
|-------------|-------------|
| DEL-13.02: Storage Tank Technical Specification | Material and performance requirements for tank design |
| DEL-13.03: Storage Tank Design Calculations | Sizing, structural, and seismic verification basis |
| DEL-13.04: Storage Tank Data Sheet Package | Tank and agitator data sheets |
| DEL-13.05: Storage Tank Installation & Test Records | Construction records reference |
| DEL-13.06: Storage Tank Fabrication Quality Documentation Package | Fabrication quality requirements |
| DEL-02.04: Geotechnical Reports | Foundation bearing capacity and settlement analysis |
| PKG-05: Concrete Structures | Tank foundation and dyke/bunding design |
| PKG-14: Process Piping | Nozzle connections and piping interfaces |
| PKG-20: Field Instrumentation | Level, temperature, pressure instrumentation |
| PKG-23: Fire Protection | Tank spacing, foam systems, fire water requirements |
| PKG-26: Protective Coatings & Painting | Internal and external coating systems |
| PKG-27: Engineering Design | Design basis and criteria |

---

## Cross-Document References

**For detailed requirements:** See `Specification.md`
- FR-01: Storage Capacity → Tank Configuration attributes (3 × 15,000 MT)
- FR-02: Product Compatibility → Product and material attributes (CSD canola oil)
- PR-01: Design Standard (API 650) → Tank Standard attribute
- PR-02: Seismic Design → Design Conditions (Seismic) attributes
- PR-05: Agitator Performance → Internals and Appurtenances (Agitators)
- PR-06: Overflow Protection → Internals and Appurtenances (Overflow Protection)
- PR-07: Water Draw-off → Internals and Appurtenances (Water Draw-off)
- FR-05: Future Expandability → Phase 2 Connections attribute

**For design rationale and guidance:** See `Guidance.md`
- DP-01: Code Compliance First → Supports API 650 Tank Standard selection
- DP-02: Safety and Reliability → Informs overflow protection and seismic design
- Tank Sizing and Configuration considerations → Inform geometry attributes
- Agitator Integration considerations → Inform agitator attributes
- Phase 2 Provisions guidance → Inform Phase 2 Connections attributes

**For production workflow:** See `Procedure.md`
- Steps 2-4 → Tank design development and CAD drafting produce the attributes documented here
- Step 5 (Self-Check) → Verifies completeness of all attributes in drawings

---

**Document Status:** Pass 3 Complete (2026-01-28) — Cross-document consistency verified. All attributes linked to requirements (Specification.md), rationale (Guidance.md), and production workflow (Procedure.md). TBDs specify information source needed. ASSUMPTIONs explicitly labeled with basis. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
