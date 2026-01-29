# Specification: DEL-09.01 Marine Outfitting Design Drawing Set

## Scope

This specification defines the requirements for **Marine Outfitting Design Drawing Set** within **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Defines the design arrangement and details for marine outfitting per Employer's Requirements. (**Source:** Decomposition, DEL-09.01 row)

**Package scope (PKG-09):** Fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades and repairs. (**Source:** Decomposition, PKG-09)

**Anticipated deliverable artifacts:**
- Fender arrangement drawings
- Bollard installation details
- Ladder details

## Requirements

### 1) Deliverable Content Requirements

The drawing set shall include the decomposition-listed artifacts and any additional drawings needed to fully define the PKG-09 scope (fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades/repairs), as required by the Employer's Requirements.

**Cross-reference:** Each requirement below maps to the Content Checklist in `Datasheet.md` and has corresponding rationale in `Guidance.md` and verification steps in `Procedure.md`.

#### 1.1 Fender Arrangement Drawings

**Requirements:**
- The drawings shall show fender plan locations, elevations, and sections sufficient for construction and installation.
- Setting-out dimensions and coordinates shall be provided referenced to site datum and coordinate system (consistent with PKG-08 Marine Structures).
- Anchorage and interface details to supporting structure (PKG-08 Marine Structures) shall be shown, including connection types, fastener specifications, and load transfer mechanisms.
- Fender selection basis: per berthing energy calculations (DEL-08.06) and fender system deflection characteristics (DEL-08.07, DEL-08.08). (**TBD** — pending design inputs)
- Fender type, size, performance characteristics (rated energy absorption, reaction force), and supplier/model identification shall be noted on drawings.

**Rationale:** See `Guidance.md § Principles (Fenders)`.
**Verification:** See `Procedure.md § Steps 3, 4, 5` (develop arrangement, detailing, self-check).

#### 1.2 Bollard Installation Details

**Requirements:**
- The drawings shall show bollard locations with setting-out dimensions referenced to site datum and coordinate system.
- Installation details including foundations/anchors, base plates, and fixing methods shall be provided sufficient for construction.
- Bollard capacities (rated bollard pull in kN or tonnes) shall be noted on drawings.
- Proof load provisions shall be noted if required by Employer's Requirements or applicable port authority codes.
- Bollard capacities: per mooring analysis (DEL-08.09). (**TBD** — pending design inputs)
- Interface details to supporting structure (PKG-08) shall be shown, including embedment/anchor details.

**Rationale:** See `Guidance.md § Principles (Bollards)`.
**Verification:** See `Procedure.md § Steps 3, 4, 5` (develop arrangement, detailing, self-check).

#### 1.3 Ladder Details

**Requirements:**
- Ladder type (fixed vertical, inclined, cage ladder), materials (marine-grade stainless steel or other corrosion-resistant materials), and fixing details shall be shown sufficient for fabrication and installation.
- Safety features shall comply with Employer's Requirements and applicable occupational safety codes:
  - Safety cages for vertical ladders exceeding threshold height (**TBD** — per applicable code, typically 2.4 m / 8 ft)
  - Rest platforms for extended climbing distances (**TBD** — per applicable code)
  - Toe clearance and rung spacing per code requirements
- Access locations shall coordinate with operational requirements and emergency egress plans. (**TBD** — operational requirements to be confirmed)
- Structural attachments to supporting structure (PKG-08) shall be detailed, including fixing types and capacities.

**Rationale:** See `Guidance.md § Principles (Ladders & Access)`.
**Verification:** See `Procedure.md § Steps 3, 4, 5, 7` (arrangement, detailing, self-check, independent check for code compliance).

#### 1.4 Life-Saving Equipment

**Requirements:**
- Arrangement and mounting details for life-saving equipment shall be shown sufficient for installation.
- Equipment list per Employer's Requirements shall be included in drawing schedules or notes. (**TBD** — specific equipment types and quantities)
- Locations shall provide coverage per regulatory requirements (**TBD** — applicable port/marine safety regulations) and operational visibility/accessibility.
- Equipment types may include (subject to ER confirmation): life rings with throw lines, rescue ladders, retrieval hooks, first aid stations.
- Mounting hardware and fixing details shall be shown, including provisions for inspection and replacement.

**Rationale:** See `Guidance.md § Principles (Life-Saving Equipment)`.
**Verification:** See `Procedure.md § Steps 3, 4, 5` (arrangement, detailing, self-check).

#### 1.5 Existing Berth 10 Upgrades/Repairs

**Requirements:**
- Upgrade and repair details for existing Berth 10 infrastructure shall be shown sufficient for construction execution.
- Demolition/repair extents and tie-in constraints shall be identified, including limits of work and preservation areas.
- Scope per Employer's Requirements and condition survey inputs. (**TBD** — specific repair scope to be confirmed)
- Existing conditions shall be clearly distinguished from new work on drawings (e.g., using line types, hatching, or notation).
- Interface details between existing and new elements shall be shown, including connection methods and tolerances.

**Rationale:** See `Guidance.md § Considerations (Existing Works)`.
**Verification:** See `Procedure.md § Steps 2, 3, 4, 5` (gather survey inputs, develop arrangement, detailing, self-check).

#### 1.6 General Notes and Schedules

**Requirements:**
- Materials specifications shall be included as required by Employer's Requirements, including corrosion protection requirements (coatings, cathodic protection compatibility).
- Corrosion protection requirements shall be coordinated with PKG-08 Marine Structures materials specifications.
- Equipment schedules shall be provided where applicable (fender schedule, bollard schedule, ladder schedule, life-saving equipment schedule). (**TBD** — format per project standards)
- Installation notes and requirements shall be included as needed for construction (e.g., torque requirements, welding specifications, grouting requirements).
- Reference notes linking to technical specifications (DEL-09.02) and other relevant documents shall be included.

**Rationale:** See `Guidance.md § Principles (Design Intent)`.
**Verification:** See `Procedure.md § Steps 4, 5` (detailing, self-check).

### 2) Drawing Quality / Drafting Requirements

| Requirement | Value | Status |
|-------------|-------|--------|
| Document control / numbering | Per project document control procedure | **TBD** — procedure to be established |
| CAD/BIM/drafting standards | Per project CAD standard | **TBD** — standard to be established; **ASSUMPTION:** Industry-standard CAD software (e.g., AutoCAD, MicroStation) |
| Units, coordinate system, datums | Per site/project survey requirements | **TBD** — coordinate system to be confirmed with PKG-08; **ASSUMPTION:** SI units (meters, millimeters) |
| Scale, line weights, annotation | Appropriate for construction use | **TBD** — standard to be confirmed; **ASSUMPTION:** Scales suitable for sheet sizes (e.g., 1:50, 1:100 for arrangements; 1:10, 1:20 for details) |
| Drawing completeness | All views, sections, and details necessary for construction without ambiguity | Verified per `Procedure.md § Steps 5, 7` |

**Verification:** See `Procedure.md § Step 5` (self-check for standards compliance).

### 3) Interface / Coordination Requirements

**Interface coordination is critical for this deliverable.** The following interfaces shall be clearly shown:

#### 3.1 PKG-08 Marine Structures Interfaces

- Fender mounting interfaces: structural steel/concrete supports, pile attachments, platform/trestle interfaces
- Bollard foundation interfaces: embedment details, base plate/anchor bolt coordination, load transfer to structure
- Ladder attachment interfaces: structural supports, landing platform coordination
- Structural capacity verification: confirm that PKG-08 structural design accommodates marine outfitting loads (fender reaction forces, bollard loads, ladder live loads)

**Coordination mechanism:** Dependencies are managed externally (NOT_TRACKED). See `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`. Interface coordination to be confirmed via interdisciplinary check (IDC) per `Procedure.md § Step 6`.

**TBD:** Specific interface points and coordination protocols to be established during design development.

#### 3.2 Other Interfaces

- Process/mechanical systems: safety zones around loading arms (PKG-11) and unloading equipment (PKG-10); access clearances
- Operability constraints: clear zones for mooring operations, cargo transfer operations, vessel maneuvering
- Maintenance access: provisions for inspection, maintenance, and replacement of marine outfitting equipment

**Verification:** See `Procedure.md § Step 6 (IDC)` for interface verification process.

### 4) Review / Check Requirements

| Check Type | Requirement | Criteria | Procedure § |
|------------|-------------|----------|-------------|
| Self-check by originator | Required | Completeness vs decomposition artifacts; internal consistency; CAD standards compliance | Proc § Step 5 |
| Interdisciplinary check (IDC) | Required where interfaces exist | Interface coordination; no conflicts with PKG-08 or other packages | Proc § Step 6 |
| Independent check/verification | Required | Technical accuracy; ER compliance; completeness vs specification requirements | Proc § Step 7 |

**TBD:** Specific IDC process and independent check acceptance criteria to be established per project quality procedures.

**Verification:** See `Procedure.md § Steps 5–7` for detailed verification process.

## Standards

**Applicable standards and codes (to be confirmed from Employer's Requirements and regulatory approvals):**

- Employer's Requirements (Vol 2 Part 1–3) — applicable clauses **TBD** (see `_REFERENCES.md`).
- **ASSUMPTION:** Marine hardware to comply with applicable marine industry standards and port authority requirements, which may include:
  - PIANC (World Association for Waterborne Transport Infrastructure) guidelines for marine fender systems
  - BS EN (British/European Standards) or equivalent for bollards and mooring equipment
  - OSHA / provincial occupational safety codes for ladders and access (e.g., CSA Z259 series for fall protection)
  - Transport Canada or provincial port authority safety requirements for life-saving equipment
  - NFPA (National Fire Protection Association) or equivalent for marine safety equipment (if applicable)

**Additional codes/standards:** **TBD** — to be extracted from Employer's Requirements and regulatory approvals during design development.

**Code compliance verification:** Per `Procedure.md § Step 7` (independent check).

## Verification

**Verification methods for Drawing deliverables (per `Procedure.md`):**

| Method | Applicability | Criteria | Procedure § |
|--------|---------------|----------|-------------|
| Self-check | All drawings | Completeness, internal consistency, CAD standards compliance | Proc § Step 5 |
| Interdisciplinary check (IDC) | Drawings with interfaces | Interface coordination, no conflicts, comment resolution | Proc § Step 6 |
| Independent check | All drawings | Technical accuracy, ER compliance, code compliance, completeness | Proc § Step 7 |

**Acceptance criteria (per `Datasheet.md § Acceptance`):**
- Drawing set demonstrates coverage of all decomposition-listed artifacts for DEL-09.01.
- All Content Checklist items in `Datasheet.md` are addressed (either resolved or TBD with action owners).
- All requirements in this Specification (§ 1.1–1.6, § 2, § 3) are met or TBD with justification.
- All checks (self-check, IDC, independent check) are completed with sign-off per `Procedure.md § Verification`.
- All TBDs are tracked and dispositioned or carried forward with owners.

## Documentation

**Required documentation outputs (per decomposition and `Datasheet.md`):**
- Fender arrangement drawings
- Bollard installation details
- Ladder details
- (Additional drawings as required by Employer's Requirements to fully define PKG-09 scope)

**Documentation requirements:**
- All documents shall comply with project document control procedures.
- Revision control per project numbering system — **TBD**.
- Format: **TBD** — **ASSUMPTION:** Per project document management requirements (PDF for review/approval; native CAD files for construction and as-built).
- Records management per `Procedure.md § Records`.
