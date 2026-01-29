# Datasheet: DEL-13.04 Storage Tank Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-13.04 |
| **Deliverable Name** | Storage Tank Data Sheet Package |
| **Package** | PKG-13 Storage Tanks |
| **Discipline** | Mechanical |
| **Type** | Data Sheet |
| **Responsible Party** | D&B Contractor |
| **Status** | INITIALIZED |

**Source:** `_CONTEXT.md`

---

## Attributes

### Package Configuration

| Attribute | Value | Source |
|-----------|-------|--------|
| **Number of Tank Data Sheets** | 3 | _CONTEXT.md (Anticipated Artifacts); Decomposition Section 1.1 (3 × 15,000 MT tanks) |
| **Number of Agitator Data Sheets** | 3 | _CONTEXT.md (Anticipated Artifacts); ASSUMPTION: One agitator per tank |
| **Overflow Protection Data Sheets** | Required | _CONTEXT.md (Anticipated Artifacts); Decomposition PKG-13 Scope |
| **Package Format** | **TBD** — Per project document management requirements |
| **Data Sheet Template** | **TBD** — Per project engineering standards |

### Tank Data Sheet Content (Per Tank)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Tank Tag Number** | **TBD** — Per project tagging system (likely TK-101, TK-102, TK-103 or similar) | |
| **Service** | CSD (Crude Super Degummed) canola oil storage | Decomposition Section 1.1 (Key Parameters) |
| **Capacity (Volume)** | **TBD** — Requires conversion from 15,000 MT using product density | |
| **Capacity (Mass)** | 15,000 MT | Decomposition Section 1.1 (Key Parameters) |
| **Product Density** | **TBD** — Requires ER extraction or product specification | |
| **Tank Type** | Vertical cylindrical atmospheric storage tank | ASSUMPTION: Based on API 650 standard and capacity |
| **Design Standard** | API 650 | Decomposition PKG-13 Scope |
| **Tank Diameter** | **TBD** — From design calculations (DEL-13.03) | |
| **Tank Height (Shell)** | **TBD** — From design calculations (DEL-13.03) | |
| **Design Pressure** | Atmospheric | ASSUMPTION: API 650 tanks are atmospheric |
| **Operating Pressure** | Atmospheric | ASSUMPTION: API 650 tanks are atmospheric |
| **Design Temperature** | **TBD** — Requires ER extraction | |
| **Operating Temperature Range** | **TBD** — Requires ER extraction and product specification | |
| **Shell Material** | **TBD** — From specification (DEL-13.02) and API 650 material selection | |
| **Bottom Material** | **TBD** — From specification (DEL-13.02) | |
| **Roof Type** | **TBD** — From design drawings (DEL-13.01) and specification (DEL-13.02) | |
| **Roof Material** | **TBD** — From specification (DEL-13.02) | |
| **Internal Coating** | **TBD** — From PKG-26 (Protective Coatings & Painting) coordination | |
| **External Coating** | **TBD** — From PKG-26 coordination | |
| **Foundation Type** | **TBD** — From design calculations (DEL-13.03) and PKG-05 coordination | |

### Tank Nozzle Summary (Per Tank)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Inlet Nozzle(s)** | **TBD** — Size, quantity, location from nozzle schedule (DEL-13.01) | |
| **Outlet Nozzle(s)** | **TBD** — Size, quantity, location from nozzle schedule (DEL-13.01) | |
| **Overflow Nozzle** | **TBD** — Size, location from nozzle schedule (DEL-13.01) | |
| **Vent Connections** | **TBD** — Size, type, location from nozzle schedule (DEL-13.01) | |
| **Drain Connection** | **TBD** — Size, location from nozzle schedule (DEL-13.01) | |
| **Water Draw-off Connection** | **TBD** — Size, location from nozzle schedule (DEL-13.01) | |
| **Instrumentation Connections** | **TBD** — Quantity, type from PKG-20 coordination | |
| **Agitator Connection** | **TBD** — Size, location from agitator data sheet | |
| **Phase 2 Connections** | **TBD** — Size, location from design (DEL-13.01) | |

### Agitator Data Sheet Content (Per Agitator)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Agitator Tag Number** | **TBD** — Per project tagging system (likely AGI-101, AGI-102, AGI-103 or similar) | |
| **Service** | CSD canola oil mixing | Decomposition Section 1.1 (Key Parameters) |
| **Tank Tag** | **TBD** — Cross-reference to tank tag number | |
| **Agitator Type** | **TBD** — Requires specification (DEL-13.02) and vendor selection (side-entry, top-entry, etc.) | |
| **Manufacturer** | **TBD** — Vendor selection | |
| **Model** | **TBD** — Vendor selection | |
| **Impeller Type** | **TBD** — Vendor specification | |
| **Impeller Diameter** | **TBD** — Vendor specification | |
| **Motor Power** | **TBD** — Vendor specification and process requirements | |
| **Motor Speed** | **TBD** — Vendor specification | |
| **Shaft Length** | **TBD** — Vendor specification; depends on tank geometry | |
| **Shaft Diameter** | **TBD** — Vendor specification | |
| **Shaft Material** | **TBD** — Vendor specification and product compatibility | |
| **Seal Type** | **TBD** — Vendor specification | |
| **Mounting Configuration** | **TBD** — From design drawings (DEL-13.01) and vendor requirements | |
| **Mixing Intensity** | **TBD** — Process requirements | |
| **Turnover Time** | **TBD** — Process requirements | |
| **Electrical Supply** | **TBD** — From PKG-17 coordination (likely 600V, 3-phase, 60Hz — ASSUMPTION) | |
| **Control Interface** | **TBD** — From PKG-19 coordination | |

### Overflow Protection Data Sheet Content

| Attribute | Value | Source |
|-----------|-------|--------|
| **System Type** | **TBD** — Requires specification (DEL-13.02) and ER extraction (level switch, overflow pipe, etc.) | |
| **Set Point** | **TBD** — Requires design calculations (DEL-13.03) and safety margin | |
| **Alarm Type** | **TBD** — From PKG-19 coordination (high level alarm, high-high level alarm) | |
| **Overflow Capacity** | **TBD** — Requires design calculations | |
| **Overflow Discharge Location** | **TBD** — Requires design and environmental coordination | |
| **Instrumentation** | **TBD** — From PKG-20 coordination | |
| **Interlock Logic** | **TBD** — From PKG-19 coordination | |

---

## Conditions

### Tank Operating Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| **Normal Operating Temperature** | **TBD** — Requires ER extraction or product specification | |
| **Maximum Operating Temperature** | **TBD** — Requires ER extraction | |
| **Minimum Operating Temperature** | **TBD** — Requires ER extraction and material brittle fracture considerations | |
| **Product Fill Rate** | **TBD** — From PKG-10 (Railcar Unloading) coordination | |
| **Product Discharge Rate** | **TBD** — From PKG-11 (Marine Loading) coordination | |
| **Normal Operating Level** | **TBD** — Process requirements | |
| **Maximum Fill Level** | **TBD** — API 650 freeboard requirements and safety considerations | |
| **Minimum Operating Level** | **TBD** — Pump NPSH and agitator submergence requirements | |

### Agitator Operating Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| **Operating Mode** | **TBD** — Continuous or intermittent operation per process requirements | |
| **Duty Cycle** | **TBD** — Process requirements | |
| **Ambient Temperature Range** | **TBD** — Fraser Surrey, BC climate data | |
| **Hazardous Area Classification** | **TBD** — Requires facility area classification study | |

### Environmental Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| **Site Location** | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | Decomposition Section 1 (Project Context) |
| **Seismic Zone** | **TBD** — Requires NBC 2020 site classification | |
| **Wind Speed** | **TBD** — Requires NBC 2020 and local data | |
| **Snow Load** | **TBD** — Requires NBC 2020 for Surrey, BC | |

---

## Construction

### Data Sheet Production

| Item | Description | Source |
|------|-------------|--------|
| **Data Source** | Design drawings (DEL-13.01), calculations (DEL-13.03), specification (DEL-13.02), vendor data | Typical data sheet workflow |
| **Template** | **TBD** — Project engineering standard data sheet template | |
| **Format** | **TBD** — Likely PDF or Excel format per project standards | |
| **Revision Control** | Per project document control procedures | ASSUMPTION |

### Data Sheet Organization

| Document | Quantity | Description |
|----------|----------|-------------|
| **Tank Data Sheets** | 3 | One per tank (TK-101, TK-102, TK-103 — tags TBD) |
| **Agitator Data Sheets** | 3 | One per agitator (AGI-101, AGI-102, AGI-103 — tags TBD) |
| **Overflow Protection Data Sheet** | 1 or 3 | **TBD** — Single system or one per tank |

### Data Sheet Validation

| Item | Description | Source |
|------|-------------|--------|
| **Technical Review** | Reviewed by discipline engineer for accuracy and completeness | Typical QA process |
| **Interdisciplinary Check** | Verified against piping (PKG-14), instrumentation (PKG-20), electrical (PKG-17) | Typical QA process |
| **Vendor Data Integration** | Agitator data sheets incorporate vendor-supplied information | Typical vendor data workflow |
| **Approval** | **TBD** — Approval authority per project procedures | |

---

## References

### Source Documents

1. `_CONTEXT.md` — Deliverable identity, description, anticipated artifacts
2. Decomposition document (`/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`):
   - Section 1.1 (Project Overview — Key Parameters): Storage capacity (3 × 15,000 MT tanks), product (CSD canola oil)
   - Section 5, PKG-13: Scope (API 650 tanks, agitators, overflow protection)
   - Section 5, DEL-13.04: Description and anticipated artifacts
3. `_REFERENCES.md` — Reference index (ER PDFs location TBD)

### Expected Reference Documents (TBD — ER Extraction Pending)

1. Volume 2 Part 2: Employer's Requirements - Civil & Process Mechanical Works — **Location TBD**
2. API 650: Welded Tanks for Oil Storage — **Location TBD** (ASSUMPTION: applicable standard)
3. Product specification for CSD canola oil — **Location TBD**

### Related Deliverables

| Deliverable | Relationship |
|-------------|-------------|
| DEL-13.01: Storage Tank Design Drawing Set | Source for tank geometry, nozzle schedule, arrangement |
| DEL-13.02: Storage Tank Technical Specification | Source for materials, standards, performance requirements |
| DEL-13.03: Storage Tank Design Calculations | Source for design basis, sizing, verification |
| DEL-13.05: Storage Tank Installation & Test Records | Installation records reference these data sheets |
| DEL-13.06: Storage Tank Fabrication Quality Documentation Package | Fabrication documentation references these data sheets |
| PKG-14: Process Piping | Nozzle connections and line sizing |
| PKG-17: Electrical Power Distribution | Agitator electrical supply |
| PKG-19: Control Systems | Agitator control and overflow protection logic |
| PKG-20: Field Instrumentation | Tank level, temperature, pressure instrumentation |
| PKG-26: Protective Coatings & Painting | Internal and external coating specifications |

---

## Cross-Document References

**For detailed requirements:** See `Specification.md`
- FR-01: Tank Data Sheet Content → Tank configuration attributes
- FR-02: Agitator Data Sheet Content → Agitator attributes
- FR-03: Overflow Protection Data Sheet Content → Overflow protection attributes
- DR-01: Data Sheet Format → Package Configuration attributes
- DR-02: Vendor Data Integration → Agitator vendor data requirements

**For data sheet development rationale:** See `Guidance.md`
- DP-01: Equipment Documentation Philosophy → Data sheet purpose and content
- DP-02: Vendor Data Integration → Agitator data incorporation principles
- DP-03: Cross-Discipline Coordination → Interface verification considerations
- Trade-offs → Template standardization vs. customization, level of detail

**For data sheet production workflow:** See `Procedure.md`
- Steps 1-3 → Produce tank, agitator, and overflow protection data sheets documented here
- Step 4 → Verify data sheet content against design deliverables
- Step 5 → Vendor coordination for agitator data sheets

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Cross-document consistency verified. All TBDs marked for design development and ER extraction. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
