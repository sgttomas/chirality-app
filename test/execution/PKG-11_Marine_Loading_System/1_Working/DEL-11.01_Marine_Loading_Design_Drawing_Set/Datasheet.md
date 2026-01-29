# Datasheet: DEL-11.01 Marine Loading Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-11.01 |
| Name | Marine Loading Design Drawing Set |
| Package | PKG-11 Marine Loading System |
| Discipline | Process |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Objectives Mapping

This deliverable contributes to the following project objectives (per decomposition Section 6):
- **OBJ-1 Safe & Reliable Operation** — drawings must communicate safety-critical interfaces (emergency release coupling, leak detection, ESD interfaces)
- **OBJ-2 Throughput Capacity (1,000,000 MT/annum)** — loading arm envelope and pipe sizing must support design throughput
- **OBJ-4 Operational Flexibility** — drawings must show operating envelope and access for diverse vessel sizes
- **OBJ-7 Environmental Protection** — drawings must show spill containment, double-walled pipe, and leak detection provisions

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing register / index | **TBD** — drawing list and numbering per document control |
| Sheet sizes | **TBD** — **ASSUMPTION**: A1/A3 per project CAD standards |
| Scales | **TBD** — typical 1:50 for GA, 1:20 for details (**ASSUMPTION**) |
| CAD standard | **TBD** — confirm per project procedures |
| Revision scheme | **TBD** — per project document control |
| Classification | **TBD** (e.g., IFC/IFA/As-Built per project conventions) |
| Drawing count (anticipated) | 4+ drawing types (see §Construction table) |

## Conditions

**Operating / Environmental Context:**

Defines the design arrangement and details for the marine loading system per Employer's Requirements (ER).
**Source:** Decomposition PKG-11 / DEL-11.01 description.

**Package scope (PKG-11):**
- Powered loading arm (articulated boom with powered slew/luff)
- Emergency release coupling (ERC) — quick-disconnect for vessel drift scenarios
- Double-walled export pipe (primary containment with leak detection annulus)
- Leak detection system (annulus monitoring, drip trays, sump instrumentation)
- Nitrogen supply (purge/blanketing for inert atmosphere)
- Operator shelter (weather protection for loading personnel)

**Source:** Decomposition PKG-11 scope statement.

**Design conditions (to be confirmed from ER):**

| Parameter | Value |
|-----------|-------|
| Operating temperature range | **TBD** — canola oil typically 20–60°C (ambient to heated) **ASSUMPTION** |
| Ambient temperature range | **TBD** — Fraser River environment (approx. –10°C to +35°C) **ASSUMPTION** |
| Environmental classification | **TBD** — marine/coastal (salt spray, humidity) **ASSUMPTION** |
| Hazardous area classification | **TBD** — **ASSUMPTION**: Zone 2 at loading arm (confirm per PKG-27 hazardous area study) |
| Seismic requirements | **TBD** — BC seismic zone (confirm per PKG-06/PKG-08 structural deliverables) |
| Design life | **TBD** — **ASSUMPTION**: 25 years minimum (confirm per ER) |
| Site location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC **Source:** Decomposition Section 1 |

## Construction

**Materials / Configuration:**

Anticipated drawing set contents (from decomposition and scope inference):

| Drawing Topic | Content | Cross-Reference |
|---------------|---------|-----------------|
| Loading arm GA | Plan/elevation showing arm reach envelope, slew/luff range, ERC location, piping connections | DEL-11.03 (envelope calcs), DEL-11.06 (OEM data) |
| Double-walled export pipe arrangement | Routing from storage tanks to loading arm, annulus leak detection tap points, expansion provisions | DEL-11.02 (pipe spec), DEL-14.xx (piping package) |
| Leak detection layout | Sensor locations (annulus, drip trays, sump), signal routing to ESD/PLC, alarm/trip setpoints reference | DEL-11.02 (leak detection spec), DEL-19.xx (I&C) |
| Operator shelter | Location relative to loading arm, access/egress, HVAC/lighting interfaces, control panel location | DEL-11.02 (shelter spec), PKG-22 (building works) |

**Source:** Decomposition DEL-11.01 "Anticipated Artifacts" field.

**Typical drawing-set contents (PROPOSAL — confirm against ER):**
- Plan/elevation/section views and key dimensions
- Operating envelope with clearance zones (maintenance, emergency access)
- Piping arrangement and tie-in locations (process flanges, drain/vent connections)
- Instrumentation locations and interfaces (leak detection, ESD, PLC I/O points)
- Civil/structural interface points (supports, foundations, shelter pads)
- Access platforms, stairs, ladders where applicable

**ASSUMPTION:** Drawing content based on good engineering practice for marine loading systems.

**Materials:** **TBD** — confirm material specs in DEL-11.02
**Construction method:** **TBD** — confirm in DEL-11.05 installation records
**Commissioning requirements:** **TBD** — confirm in DEL-11.05 test records

## Interfaces (Coordination Items)

Dependencies are coordinated externally (NOT_TRACKED per `_DEPENDENCIES.md`). The following interfaces shall be identified on drawings or in drawing notes:

| Interface | Adjacent Package/Deliverable | Coordination Item |
|-----------|------------------------------|-------------------|
| Marine loading arm OEM | DEL-11.06 OEM Qualification | Vendor GA, connection details, envelope data |
| Double-walled export pipe | DEL-14.xx (PKG-14 Process Piping) | Pipe routing, tie-in flanges, support locations |
| Leak detection system | DEL-19.xx (PKG-19 Control Systems) | Device locations, signal list, ESD interface |
| Nitrogen supply | DEL-18.xx (PKG-18 Utilities) — **TBD** correct package | Supply point, pressure/flow requirements |
| Operator shelter | PKG-22 Building Works | Shelter foundation, services interfaces |
| Spill containment / drainage | DEL-03.xx (PKG-03 Underground Utilities & Drainage) | Secondary containment, sump locations |
| Marine structures | DEL-08.xx (PKG-08 Marine Structures) | Jetty/wharf platform interface, loading arm foundation |
| Metering system | DEL-12.xx (PKG-12 Product Transfer & Metering) | Metering skid location, pipe tie-ins |

**Note:** Interface package references updated for consistency with decomposition structure.

## Cross-Document Links

| Document | Link Point |
|----------|------------|
| Specification.md (DEL-11.01) | Drawing requirements baseline — verification criteria trace here |
| Guidance.md (DEL-11.01) | Engineering rationale and trade-offs for drawing development |
| Procedure.md (DEL-11.01) | Step-by-step production workflow and verification checklist |
| DEL-11.02 Technical Specification | System performance requirements governing drawing content |
| DEL-11.03 Design Calculations | Sizing/envelope calculations supporting drawing dimensions |
| DEL-11.06 OEM Qualification | Vendor data inputs for loading arm GA |

## Deliverable Acceptance (Minimum)

| Acceptance Criterion | Verification Method | Reference |
|---------------------|---------------------|-----------|
| Drawing list/register provided with titles and revision status | Document review | Specification.md §Requirements REQ-01 |
| Each drawing includes title block, scale, north arrow (if applicable), key notes, revision block | CAD standards check | Specification.md §Quality QA-02, Procedure.md §Verification |
| Operating envelope and clearance zones shown for loading arm | Design review | Specification.md §Requirements REQ-06, Guidance.md §Considerations |
| Interface points identified with adjacent package references | IDC review | Specification.md §Interface Requirements INT-01 through INT-05 |
| Assumptions and TBDs explicitly highlighted | Completeness check | Specification.md §Requirements REQ-05, §Quality QA-04 |
| IDC completed per project QA/QC process | IDC sign-off | Specification.md §Quality QA-03, Procedure.md §Steps Step 8 |

## References

- `_REFERENCES.md` — applicable reference document list
- `0_References/` — package reference materials
- Decomposition: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-11 / DEL-11.01)
- Employer's Requirements: **TBD** (clause references pending extraction)
- Applicable standards: **TBD** (confirm per ER and project code register)
- `_DEPENDENCIES.md` — NOT_TRACKED (dependencies coordinated externally)

---

**Pass 2/3 Enrichment Notes:**
- Added drawing count attribute
- Added site location to Conditions
- Updated nitrogen supply package reference with TBD note (decomposition does not show PKG-18 as Utilities)
- Updated interface package references for consistency with decomposition
- Enhanced cross-references between Datasheet acceptance criteria and Specification/Procedure sections
- All TBDs and ASSUMPTIONs preserved from Pass 1
