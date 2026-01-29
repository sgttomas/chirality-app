# Datasheet: DEL-11.02 Marine Loading Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-11.02 |
| Name | Marine Loading Technical Specification |
| Package | PKG-11 Marine Loading System |
| Discipline | Process |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Objectives Mapping

This deliverable contributes to the following project objectives (per decomposition Section 6):
- **OBJ-1 Safe & Reliable Operation** — specification defines ERC, leak detection, and ESD integration requirements
- **OBJ-2 Throughput Capacity (1,000,000 MT/annum)** — specification defines loading rate and system sizing requirements
- **OBJ-4 Operational Flexibility** — specification defines operating envelope for diverse vessel types
- **OBJ-7 Environmental Protection** — specification defines double-walled pipe, leak detection, and spill containment requirements

**Source:** Decomposition Section 6; objectives mapping aligns with DEL-11.01.

## Attributes

| Attribute | Value |
|-----------|-------|
| Document Number | **TBD** — per project document control |
| Specification type | Technical specification (marine loading system) |
| Revision | **TBD** |
| Applicable standards | **TBD** (confirm per ER / code register) — see §Standards below |
| Classification | **TBD** (e.g., IFC/IFA per project conventions) |
| Specification sections count | 10 sections (§1–§10 per Specification.md structure) |

## Conditions

**Operating / Environmental Context:**

Defines performance, materials, and workmanship requirements for the marine loading system per Employer's Requirements (ER).
**Source:** Decomposition DEL-11.02 description.

**Package scope (PKG-11):**
- Powered loading arm (articulated boom with powered slew/luff)
- Emergency release coupling (ERC) — quick-disconnect for vessel drift protection
- Double-walled export pipe (primary containment with leak detection annulus)
- Leak detection system (annulus monitoring, drip trays, sump instrumentation)
- Nitrogen supply (purge/blanketing for inert atmosphere)
- Operator shelter (weather protection for loading personnel)

**Source:** Decomposition PKG-11 scope statement; consistent with DEL-11.01.

**Design basis parameters (to be confirmed from ER):**

| Parameter | Value | Source |
|-----------|-------|--------|
| Product | Canola oil (refined vegetable oil) | ER **TBD** |
| Design loading rate | **TBD** m³/hr (or MT/hr) | ER **TBD** |
| Annual throughput | 1,000,000 MT/annum (OBJ-2) | Decomposition OBJ-2 |
| Operating temperature | **TBD** — typically 20–60°C for canola oil **ASSUMPTION** | ER **TBD** |
| Ambient temperature range | **TBD** — Fraser River environment (approx. –10°C to +35°C) **ASSUMPTION** | Site data |
| Design pressure (loading arm/pipe) | **TBD** | ER **TBD** |
| Environmental classification | Marine/coastal (salt spray, humidity) | Site conditions **ASSUMPTION** |
| Hazardous area classification | **TBD** — **ASSUMPTION**: Zone 2 at loading arm | PKG-27 study **TBD** |
| Seismic requirements | **TBD** — BC seismic zone | ER / PKG-06/08 **TBD** |
| Design life | **TBD** — **ASSUMPTION**: 25 years minimum | ER **TBD** |
| Site location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | Decomposition Section 1 |

**Note:** Design basis parameters align with DEL-11.01 Datasheet §Conditions and Specification.md §3.

## Construction

**Specification content structure (anticipated artifacts from decomposition):**

| Section | Content | Cross-Reference | Specification Reference |
|---------|---------|-----------------|-------------------------|
| Marine loading arm specification | Powered arm type, reach/envelope, ERC, materials, controls, safety | DEL-11.06 OEM data | Specification.md §4 (MLA-001 to MLA-032) |
| Double-walled pipe specification | Design code, materials, annulus design, testing | DEL-11.03 calcs, DEL-14 | Specification.md §5 (DWP-001 to DWP-020) |
| Leak detection specification | Detection philosophy, device types, alarm/ESD integration | DEL-19 I&C | Specification.md §6 (LDS-001 to LDS-014) |
| Nitrogen supply requirements | Purpose, capacity, pressure regulation, interfaces | **TBD** utilities package | Specification.md §7 (N2-001 to N2-007) |
| Operator shelter requirements | Functional requirements, interfaces to building works | PKG-22 | Specification.md §8 (SHL-001 to SHL-005) |

**Source:** Decomposition DEL-11.02 "Anticipated Artifacts" field; Specification.md section structure.

**Note:** This table directly corresponds to Specification.md §4–§8 requirement sections and Procedure.md §Steps 3-6.

**Key material requirements (TBD — confirm per ER):**

| Component | Material | Notes |
|-----------|----------|-------|
| Loading arm wetted parts | **TBD** — stainless steel or carbon steel per product compatibility | Confirm ER; Specification.md MLA-013, MLA-014 |
| Double-walled pipe (inner) | **TBD** — carbon steel or stainless steel | Confirm ER; Specification.md DWP-005 |
| Double-walled pipe (outer) | **TBD** — carbon steel | Confirm ER; Specification.md DWP-006 |
| Seals and gaskets | **TBD** — compatible with canola oil | Confirm ER; Specification.md MLA-014 |

**Source:** Specification.md §4.4, §5.2.

## Interfaces (Coordination Items)

Dependencies are coordinated externally (NOT_TRACKED per `_DEPENDENCIES.md`). The following interfaces are specified or referenced:

| Interface | Adjacent Package/Deliverable | Specification Section | Procedure Step |
|-----------|------------------------------|-----------------------|----------------|
| Marine loading arm OEM | DEL-11.06 OEM Qualification | §4 Loading Arm | Step 3 |
| Piping system | DEL-14.xx (PKG-14 Process Piping) | §5 Double-Walled Pipe | Step 4 |
| Instrumentation & control | DEL-19.xx (PKG-19 Control Systems) | §6 Leak Detection, §4.7 Controls | Step 3, 5 |
| ESD/safety systems | DEL-20.xx (PKG-20 **TBD**), DEL-29.xx (SIS **TBD**) | §4.8 Safety, §6.3 Alarm/ESD | Step 3, 5 |
| Utilities (nitrogen) | **TBD** utilities package | §7 Nitrogen Supply | Step 6 |
| Building works (shelter) | PKG-22 Building Works | §8 Operator Shelter | Step 6 |
| Marine structures | DEL-08.xx (PKG-08 Marine Structures) | §4 (foundation interfaces) | Step 9 (structural review) |
| Drainage/containment | DEL-03.xx (PKG-03 Underground Utilities & Drainage) | §5, §6 (containment interfaces) | Step 9 (civil review) |

**Note:** Interface list aligns with DEL-11.01 Datasheet §Interfaces; specification sections and procedure steps added for cross-document traceability.

## Cross-Document Links

| Document | Link Point |
|----------|------------|
| Datasheet.md (this file) | Summary of specification attributes and design basis |
| Specification.md (DEL-11.02) | Full requirement structure (Sections 1–10 with 58+ individual requirements) |
| Guidance.md (DEL-11.02) | Engineering rationale and trade-offs for requirement selection |
| Procedure.md (DEL-11.02) | Production workflow (11 steps) and verification checklist |
| DEL-11.01 Drawing Set | Drawings implement the requirements specified here |
| DEL-11.03 Design Calculations | Calculations demonstrate compliance with specification |
| DEL-11.04 Data Sheet Package | Equipment datasheets align with specification requirements |
| DEL-11.05 Installation & Test Records | Test records demonstrate specification compliance |
| DEL-11.06 OEM Qualification | OEM data provides input for loading arm specification §4 |

## Deliverable Acceptance (Minimum)

| Acceptance Criterion | Verification Method | Reference |
|---------------------|---------------------|-----------|
| All specification sections (1–10) populated | Completeness review | Specification.md §1–§10, Procedure.md §Steps 3-7 |
| All unknown values explicitly marked TBD | Completeness review | Specification.md (58+ TBD items), Procedure.md §Step 10 |
| Compliance matrix exists (maps requirements to ER) | Traceability review | Specification.md §Compliance Matrix, Procedure.md §Step 8 |
| Interface requirements reviewed with adjacent packages | IDC review | Procedure.md §Step 9, §Verification |
| Technical review completed and comments resolved | Review records | Procedure.md §Step 10, §Verification |

**Note:** All 5 acceptance criteria align with Procedure.md §Verification acceptance checklist and Specification.md structure.

## Standards

**Applicable standards (TBD — confirm per ER and project code register):**

| Standard | Applicability | Status | Specification Reference |
|----------|---------------|--------|-------------------------|
| OCIMF (Oil Companies International Marine Forum) | Marine loading arm design guidance | **TBD** | Specification.md §2.2, §4 |
| EN 1474 / ISO 16904 | Ship-to-shore interface for LNG (reference for arm design) | **TBD** — check applicability | Specification.md §2.2 |
| ASME B31.3 | Process piping design | **TBD** | Specification.md §2.2, §5 |
| API 2610 | Terminal piping design | **TBD** | Specification.md §2.2, §5 |
| CSA Z662 | Oil and gas pipeline systems (if applicable) | **TBD** | Specification.md §2.2 |
| IEC 61511 / IEC 61508 | Safety instrumented systems (leak detection/ESD) | **TBD** | Specification.md §2.2, §6 |
| NFPA 30 | Flammable and combustible liquids | **TBD** | Specification.md §2.2 |
| CSA / NBC | Building code (operator shelter) | **TBD** | Specification.md §2.2, §8 |

**Source:** Specification.md §2 Applicable Documents; Guidance.md §Principles.

**Note:** Standards list aligns with DEL-11.01 Datasheet §Standards and includes specification section cross-references.

## References

- `_REFERENCES.md` — applicable reference document list
- `0_References/` — package reference materials
- Decomposition: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-11 / DEL-11.02)
- Employer's Requirements: **TBD** (clause references pending extraction; see Specification.md §Compliance Matrix)
- `_DEPENDENCIES.md` — NOT_TRACKED (dependencies coordinated externally)

---

**Pass 2/3 Enrichment Notes:**
- Added "Specification sections count" attribute (10 sections)
- Added site location to Conditions for consistency with DEL-11.01
- Added "Specification Reference" column to Construction table showing requirement ID ranges
- Added note confirming Construction table corresponds to Specification §4–§8 and Procedure §Steps 3-6
- Enhanced Interfaces table with "Specification Section" and "Procedure Step" columns for full traceability
- Added note showing interface list aligns with DEL-11.01
- Enhanced Cross-Document Links with specific counts (10 sections, 58+ requirements, 11 steps)
- Enhanced acceptance criteria with specific cross-references to Procedure verification
- Added note confirming all 5 acceptance criteria align across documents
- Added "Specification Reference" column to Standards table
- Added note showing standards alignment with DEL-11.01
- All TBDs and ASSUMPTIONs preserved from Pass 1
