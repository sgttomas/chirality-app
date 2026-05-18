# Datasheet — DEL-011-02 Steel Plate Floor Embedments

**Document Type:** Datasheet (descriptive)
**Deliverable ID:** DEL-011-02
**Revision:** R1 — 2026-02-26 (Pass 3 enrichment)
**Status:** SEMANTIC_READY

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-011-02 |
| Deliverable Name | Steel Plate Floor Embedments |
| Package | PKG-011 — Building Structure & Envelope |
| Discipline | General Contractor (construction) |
| Type | Construction |
| Responsible Party | General Contractor |
| Covers SOW | SOW-0024 |
| Supports Objective | OBJ-001 |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price |
| Owner | Camrose County |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Project Location | SW 14–44–21–W4, near Ferintosh, Alberta |
| Contract Completion Deadline | December 31, 2026 |

**Sources:** _CONTEXT.md; Decomposition §7 PKG-011; RFP R-01 §1.1, §2.7, §3.1

---

## Attributes

### Purpose
Steel plate embedments are installed in the concrete floor of the repair bays (and wash bay) at strategic locations to accommodate the weight and movement of tracked and packer-type heavy equipment such as motor scrapers, packers, and tracked excavators. They provide a durable bearing surface that prevents damage to the concrete slab where equipment is positioned or manoeuvred.

**Source:** RFP R-01 §3.4 ("Steel plating in concrete at strategic locations to accommodate track and packer type heavy equipment"); Appendix B floor plan notation ("Steel Plates in Floor as indicated").

### Material
- **Plate material:** TBD — structural steel plate (ASSUMPTION: likely A36 or equivalent ASTM/CSA grade; grade to be confirmed by structural engineer via DEL-002-12 Structural Specification). [Lensing ref: A-002]
- **Plate thickness:** TBD — to be specified by structural engineer in DEL-002-08.
- **Surface finish:** TBD — flush with finished concrete floor surface, within tolerance per DEL-002-08 (ASSUMPTION: required for equipment movement without tripping hazard or edge loading damage). [Lensing ref: E-001 — tolerance reference standardized to single source DEL-002-08]

### Quantity and Layout
- **Number of embedment zones:** Multiple — Appendix B floor plan (R-04) shows several parallel steel plate bands running transversely across the repair bay floor area and one or more bands in the wash bay.
- **Approximate locations (from Appendix B, R-04):**
  - Main repair bay (New North Shop area): minimum four (4) transverse steel plate bands spanning the full bay width, spaced at intervals along the bay length.
  - Wash bay: minimum two (2) transverse steel plate bands. Note: wash bay plate scope may overlap with SOW-0027a and DEL-018-05 — see Guidance CON-011-02-03 for scope boundary clarification needed.
  - ASSUMPTION: exact plate count, individual plate dimensions, and precise spacing are to be confirmed on DEL-002-08 Steel Plate Embedment Plan (IFC drawings).
- **Bay width:** 24' (repair bays); wash bay 24' wide (Appendix B, R-04). Note: verify unit convention consistency with DEL-002-08 structural IFC drawings; if IFC drawings use metric (SI) units, dual-state or convert dimensions accordingly. [Lensing ref: B-003]
- **Individual plate dimensions:** TBD — to be specified on structural drawings (DEL-002-08).

### Plate Dimension Table (Placeholder) [Lensing ref: B-002]

The following table is a placeholder for individual plate dimensions. Populate from DEL-002-08 when issued.

| Zone | Plate ID | Length | Width | Thickness | Anchorage Type | Notes |
|---|---|---|---|---|---|---|
| Repair Bay 1 | TBD | TBD | TBD | TBD | TBD | Per DEL-002-08 |
| Repair Bay 2 | TBD | TBD | TBD | TBD | TBD | Per DEL-002-08 |
| Wash Bay | TBD | TBD | TBD | TBD | TBD | Per DEL-002-08; scope per CON-011-02-03 resolution |

**Source for placeholder:** ASSUMPTION — standard practice to tabulate individual plate dimensions for procurement; dimensions from DEL-002-08 not yet available. [Lensing ref: B-002]

### Floor System Interface
- Embedments are cast into the concrete floor slab prior to the concrete pour (ASSUMPTION: cast-in-place method; see Guidance CON-011-02-01 for confirmation needed). [Lensing ref: B-004 — wording corrected to align with cast-in-place sequence described in Specification REQ-011-02-07 and Procedure Phase 2]
- Upstream dependency: DEL-011-01 Concrete Superstructure — slab formwork and reinforcing steel must be in place and ready for steel plate placement prior to pour. (Source: _DEPENDENCIES.md; Specification REQ-011-02-07)
- Top surface of steel plate to be flush with finished floor elevation, within tolerance per DEL-002-08. [Lensing ref: E-001 — single consistent tolerance reference]
- ASSUMPTION: Connection to slab likely via headed anchor studs, deformed bar anchors, or equivalent mechanical anchorage system; method to be confirmed by structural engineer.

---

## Conditions

### Design Loads
- Equipment type: tracked and packer-type heavy equipment (RFP §3.4, R-01).
- Specific design loads (kPa, point loads, dynamic factors): TBD — to be determined by structural engineer and documented in DEL-002-08 and DEL-002-10 (Structural Calculation Package).
- ASSUMPTION: Loading regime likely includes tracked vehicles (e.g., D-series dozers, packers, motor scrapers) with ground contact pressures exceeding standard industrial floor slab design values, necessitating the steel plate bearing surface.

### Design Load Category Table (Placeholder) [Lensing ref: B-001]

The following table is a placeholder for design load values. Populate from DEL-002-10 when issued.

| Load Category | Value | Units | Source | Notes |
|---|---|---|---|---|
| Uniformly Distributed Load (UDL) | TBD | kPa | DEL-002-10 | Floor area loading |
| Point Load — tracked equipment | TBD | kN | DEL-002-10 | Per track pad contact area |
| Point Load — packer equipment | TBD | kN | DEL-002-10 | Per wheel/roller contact area |
| Dynamic Amplification Factor | TBD | ratio | DEL-002-10 | For moving equipment |
| Impact Factor | TBD | ratio | DEL-002-10 | For equipment set-down/start-up |

**Source for placeholder:** ASSUMPTION — standard structural design practice requires these load categories for embedded steel plate design; specific values from DEL-002-10 not yet available. [Lensing ref: B-001]

### Environmental Conditions
- Interior application — enclosed maintenance shop building.
- Floor subject to petroleum product contamination, water (from wash bay proximity), and mechanical impact.
- Wash bay environment: direct exposure to water, cleaning chemicals, and potentially hydrocarbon contamination — differing materially from repair bay conditions (see Guidance for corrosion protection decision criteria). [Lensing ref: F-004]
- ASSUMPTION: Plate surface may require anti-slip texture or surface treatment to manage traction; to be confirmed on structural/architectural drawings.

### Service Life
- TBD — no explicit service life stated in RFP. ASSUMPTION: consistent with building service life (ASSUMPTION: typically 40–50 years for institutional/industrial buildings in Alberta; **location TBD** for specific code or Owner requirement). [Lensing ref: C-003]
- Service life determination has implications for material selection and corrosion protection strategy, particularly in wash bay zones. See Guidance for decision framing. [Lensing ref: C-003]

---

## Construction

### Fabrication
- Steel plates fabricated to dimensions and tolerances per structural engineer's IFC drawings (DEL-002-08).
- ASSUMPTION: Plates shop-fabricated; field cutting should be minimized.

### Sequence
1. Concrete superstructure slab design completed and approved (upstream: DEL-011-01 design phase).
2. Structural embedment plan issued (DEL-002-08, IFC).
3. Concrete forming and rebar installation in floor slab.
4. Steel plates positioned and anchorage system installed prior to concrete pour (ASSUMPTION: cast-in-place method; see Guidance CON-011-02-01).
5. Concrete poured and finished to specified tolerances around embedments.
6. Inspection and documentation completed.

### Standards and Code Requirements
- Alberta Safety Codes Act and applicable Safety Code Permits (RFP §3.3.2, R-01).
- Building permit and development permit required (RFP §3.3.2, R-01).
- IFC drawings to be signed/stamped by a P.Eng. licensed to practice in Alberta (RFP §3.3.2, R-01).
- ASSUMPTION: Applicable codes include Alberta Building Code (ABC) — edition in force at time of permit issuance — and referenced CSA/ASTM standards for structural steel and concrete construction; specific clause references TBD pending structural engineer engagement. [Lensing ref: C-001]

---

## References

| Ref ID | Document | Relevance | Accessibility |
|---|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.4 design requirement for steel plate embedments; §3.3.2 construction and permit obligations | Accessible — _Sources/ |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan showing steel plate band locations in repair bays and wash bay | Accessible — _Sources/ |
| DEL-002-08 | Steel Plate Embedment Plan (PKG-002) | IFC drawing set defining exact locations, dimensions, plate sizes, and anchorage details | Not yet issued (upstream design deliverable) |
| DEL-002-10 | Structural Calculation Package (PKG-002) | Load calculations and design basis for embedments | Not yet issued (upstream design deliverable) |
| DEL-002-12 | Structural Specification (PKG-002) | Material grades, welding standards, inspection requirements | Not yet issued (upstream design deliverable) |
| _CONTEXT.md | DEL-011-02 Context | Deliverable identity and anticipated artifacts | Accessible — deliverable folder |
| _DEPENDENCIES.md | DEL-011-02 Dependencies | Upstream/downstream coordination | Accessible — deliverable folder |
| Decomposition | WDMLRL_Decomposition_Claude.md | SOW-0024, PKG-011 scope, OBJ-001 | Accessible — _Decomposition/ |
