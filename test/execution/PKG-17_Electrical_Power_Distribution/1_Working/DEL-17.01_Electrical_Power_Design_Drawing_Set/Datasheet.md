# Datasheet: DEL-17.01 Electrical Power Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-17.01 |
| Name | Electrical Power Design Drawing Set |
| Package | PKG-17 Electrical Power Distribution |
| Discipline | Electrical |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Number | **TBD** — To be assigned per project drawing numbering system |
| Sheet Size | **ASSUMPTION**: ANSI D (24" × 36") or ISO A1 as per project CAD standard |
| Scale | Various — Typical: 1:100, 1:50, 1:200 (as appropriate per drawing type) |
| CAD Standard | **TBD** — To be defined per project CAD manual |
| Revision | 0 (Initial issue) |
| Classification | For Construction |
| Drawing Set Contents | Single line diagrams (SLDs), MV/LV distribution drawings, cable schedules, grounding drawings |

### Drawing Types and Quantities

**ASSUMPTION**: Typical drawing set for canola oil transload facility with 1,000,000 MT/a capacity includes:

| Drawing Type | Estimated Quantity | Purpose | Specification Reference | Guidance Reference | Procedure Step |
|--------------|-------------------|---------|------------------------|-------------------|----------------|
| Single Line Diagrams (SLDs) | 3-5 sheets | Overall electrical distribution architecture, primary and secondary distribution | FR-1 (Specification.md) | Principle 1 (Guidance.md) | Step 3 (Procedure.md) |
| MV Distribution Drawings | 2-4 sheets | Medium voltage (25 kV or 13.8 kV class) incoming service and distribution | FR-2 (Specification.md) | Principle 2 (Guidance.md) | Step 4 (Procedure.md) |
| LV Distribution Drawings | 8-12 sheets | Low voltage (600V/480V/208V-120V) distribution, panel locations, load assignments | FR-3 (Specification.md) | Principle 2 (Guidance.md) | Step 4 (Procedure.md) |
| Cable Schedules | 4-8 sheets | Power cable routing, sizing, terminations for MV and LV circuits | FR-4 (Specification.md) | Consideration 4 (Guidance.md) | Step 5 (Procedure.md) |
| Grounding Drawings | 2-4 sheets | Grounding grid, equipment grounding, lightning protection, bonding details | FR-5 (Specification.md) | Principle 4 (Guidance.md) | Step 6 (Procedure.md) |

**Source**: _CONTEXT.md (anticipated artifacts); quantities are ASSUMPTION based on facility scope (Decomposition Section 4 — PKG-17).
**Cross-Reference**: See Specification.md for functional requirements (FR-1 through FR-6) and Procedure.md Steps 3-6 for drawing production procedures.

## Conditions

**Operating / Environmental Context:**

This drawing set defines the design arrangement and details for electrical power distribution serving the canola oil transload facility per Employer's Requirements.

**Project Context** (Source: Decomposition Section 1):
- **Location**: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Facility Type**: Canola oil transload (rail-to-storage-to-ship)
- **Throughput**: 1,000,000 MT per annum (permitted capacity)
- **Storage**: 45,000 MT total (3 × 15,000 MT tanks)
- **Key Loads**: Railcar unloading system (32 positions), transfer pumps, marine loading system, tank heating, control/instrumentation

**Environmental Conditions:**
- **Climate Zone**: **ASSUMPTION**: CSA Climate Zone 2 (coastal British Columbia) — outdoor equipment rated for -20°C to +40°C ambient
- **Hazardous Area Classification**: **TBD** — To be confirmed per facility hazardous area classification study (anticipated: Class I Division 2 or Zone 2 in specific areas per CEC Section 18)
- **Seismic Requirements**: **ASSUMPTION**: High seismic zone (coastal BC) — CSA C22.3 No. 7 anchorage and seismic restraints required
- **Corrosion Environment**: **ASSUMPTION**: Marine/industrial atmosphere (proximity to waterfront) — outdoor equipment shall be suitable for C4 or C5 corrosivity per ISO 12944
- **Design Life**: **TBD** — **ASSUMPTION**: 25 years minimum per facility operational life expectancy

**Electrical System Parameters** (Source: PKG-17 scope description — Decomposition Section 4):
- **Utility Service**: **TBD** — Medium voltage service from BC Hydro (anticipated: 25 kV or 13.8 kV class)
- **Primary Distribution**: Medium voltage (MV) switchgear and transformers
- **Secondary Distribution**: Low voltage (600V/480V for motors and large loads; 208V-120V for lighting, receptacles, small loads)
- **Emergency/Standby Power**: **TBD** — Backup generator or UPS requirements per ER (location TBD)
- **Load Categories**: Motor loads (pumps, heating circulation), process control systems, instrumentation, lighting (interior/exterior), HVAC, marine loading arms, railcar unloading equipment

## Construction

**Materials / Configuration:**

Anticipated drawing set artifacts (Source: _CONTEXT.md and Decomposition DEL-17.01 entry):
1. **Single Line Diagrams (SLDs)**: One-line representation of electrical distribution from utility point of connection through MV switchgear, transformers, LV switchgear/MCCs, major load centers
2. **MV/LV Distribution Drawings**: Physical layout and arrangement of electrical distribution equipment (transformers, switchgear, MCCs, panels) on site plan and within buildings
3. **Cable Schedules**: Tabulated listings of all power cables with circuit ID, size, type, length, routing, termination points, protection device sizing
4. **Grounding Drawings**: Site grounding grid, equipment grounding connections, lightning protection system, bonding details for tanks and structures

**Drawing Content Requirements** (ASSUMPTION — typical electrical drawing set per CSA and IEEE practice):

| Drawing Type | Typical Content |
|--------------|-----------------|
| Single Line Diagrams | Utility incoming service, main switchgear, transformers, secondary switchgear/MCCs, major feeders, protection devices (breakers, fuses), metering, CT/PT locations |
| MV Distribution | Switchgear lineup, cable routing (underground duct banks or overhead), transformer locations, sectionalizing switches, feeder routes to buildings/equipment |
| LV Distribution | Panel locations (floor plans), load assignments, branch circuit routing (conduit/cable tray), receptacle and disconnect locations, equipment connections |
| Cable Schedules | Circuit number, voltage level, cable size (AWG/kcmil), insulation type, number of conductors, cable length, source/destination, protection device rating, conduit/tray assignment |
| Grounding | Grounding grid layout (buried grid conductors), ground rod locations, grounding electrode connections, equipotential bonding, lightning down-conductors, exothermic weld details |

**Construction Method**: Design-build electrical installation per project specifications and CEC requirements.

**Installation Requirements**:
- **TBD** — Conduit and cable tray routing details (coordinate with civil, structural, architectural, mechanical disciplines)
- **TBD** — Concrete pad and foundation requirements for outdoor equipment (coordinate with civil/structural)
- Cable installation per CEC Section 12 (wiring methods)
- Underground duct banks per CEC Section 12-012 and local utility standards
- **TBD** — Equipment access and clearance requirements per CEC Section 2 (spacing and working clearances)

**Commissioning Requirements**: See DEL-17.05 (Installation and Test Records) for commissioning test procedures.

## References

**Primary References**:
- **Decomposition Document**: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4 — PKG-17, DEL-17.01 entry)
- **_CONTEXT.md**: Deliverable identity and anticipated artifacts
- **Employer's Requirements**: **TBD** — Volume 2 Parts 1-3 (electrical sections) — **location TBD**

**Applicable Standards** (Electrical discipline — Canadian jurisdiction):
- **CSA C22.1 (Canadian Electrical Code, Part I)** — Primary electrical safety code for BC installations
- **CSA C22.2** — Canadian electrical equipment standards
- **CSA C22.3 No. 7** — Underground systems, seismic requirements
- **IEEE C2 (NESC)** — National Electrical Safety Code (reference for utility coordination)
- **CSA Z462** — Workplace electrical safety
- **NFPA 70E** — Electrical safety in the workplace (reference standard)
- **BC Safety Standards Act** and **BC Electrical Safety Regulation** — Provincial regulatory authority

**Additional References**:
- **TBD** — BC Hydro service requirements and specifications
- **TBD** — Project CAD manual and drawing standards
- **TBD** — Facility hazardous area classification drawing (for electrical area classification)
- See DEL-17.02 (Electrical Power Technical Specification) for equipment specifications
- See DEL-17.03 (Electrical Power Design Calculations) for load analysis, short circuit, voltage drop, protection coordination
- See DEL-17.04 (Electrical Power Data Sheet Package) for equipment data sheets

**Cross-references**:
- Dependencies coordinated externally (per _DEPENDENCIES.md — NOT_TRACKED mode)
- Interface with PKG-18 (Lighting) for lighting load allocations
- Interface with PKG-19 (Control & Instrumentation) for control system power requirements
- Interface with PKG-14 (Process Piping), PKG-15 (Pumps), PKG-13 (Storage Tanks) for process equipment power connections
- Interface with PKG-02 (Site Civil Works) for underground duct bank routing and grounding grid installation
