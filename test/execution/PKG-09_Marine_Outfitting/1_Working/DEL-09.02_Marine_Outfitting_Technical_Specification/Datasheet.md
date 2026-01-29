# Datasheet: DEL-09.02 Marine Outfitting Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-09.02 |
| Name | Marine Outfitting Technical Specification |
| Package | PKG-09 Marine Outfitting |
| Discipline | Marine |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Scope (Decomposition)

**Package scope (PKG-09):** Fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades and repairs. (**Source:** Decomposition, PKG-09)

**Deliverable intent (DEL-09.02):** Defines performance, materials, and workmanship requirements for marine outfitting per Employer's Requirements. (**Source:** Decomposition, DEL-09.02 row)

**Anticipated artifacts (from decomposition):**
- Fender specification
- Bollard specification
- Marine hardware specification

## Deliverable Attributes (Technical Specification)

| Attribute | Value |
|-----------|-------|
| Document number | **TBD** — per project document control procedure |
| Specification template/structure | **TBD** — **ASSUMPTION:** Industry-standard technical specification format with sections for scope, standards, requirements, quality, submittals |
| Revision | **TBD** — per project revision scheme |
| Classification | **TBD** — **ASSUMPTION:** Project-specific or contractor-generated document (unless ER specifies format) |
| Governing standards list | **TBD** — to be extracted from Employer's Requirements and applicable authority requirements |
| Issue format | **TBD** — **ASSUMPTION:** PDF for review/approval; editable format for internal development |

## Content Checklist (Minimum)

This datasheet defines the expected **content** of the technical specification. Each item corresponds to requirements in `Specification.md § 1–2` and has corresponding rationale in `Guidance.md` and procedural steps in `Procedure.md`.

| Content Item | Specification § | Guidance § | Procedure Step | Status |
|--------------|-----------------|------------|----------------|--------|
| Scope/definitions aligned to PKG-09 | SPEC § 1.1 | Guidance § Principles | Proc Step 1, 3 | **TBD** — define inclusions/exclusions consistent with decomposition |
| Applicable codes and standards | SPEC § 1.2 | Guidance § Principles | Proc Step 2 | **TBD** — extract from ER and regulatory requirements |
| Design basis (vessel, environment, service life) | SPEC § 1.3 | Guidance § Considerations | Proc Step 2 | **TBD** — obtain from DEL-08.06, DEL-08.09, and ER |
| Corrosion protection requirements | SPEC § 1.4 | Guidance § Considerations (Corrosion) | Proc Step 3 | **TBD** — define exposure classification, coating systems, galvanizing requirements |
| Installation requirements (tolerances, interfaces) | SPEC § 1.5 | Guidance § Considerations (Interface Coordination) | Proc Step 3 | **TBD** — setting-out tolerances, interface with PKG-08 |
| Quality/inspection requirements (hold points, certs) | SPEC § 1.6 | Guidance § Principles | Proc Step 4 | **TBD** — define hold/witness points, certification requirements |
| Submittal requirements (datasheets, certs, calcs, ITPs) | SPEC § 1.7 | — | Proc Step 4 | **TBD** — cross-reference DEL-09.03, DEL-09.04, DEL-09.05 |
| Fender requirements (performance, materials, workmanship, testing) | SPEC § 2.1 | Guidance § Principles (Fenders) | Proc Step 3 | **TBD** — energy absorption, reaction limits, materials, testing per DEL-08.06, DEL-08.07, DEL-08.08 |
| Bollard requirements (performance, materials, workmanship, testing) | SPEC § 2.2 | Guidance § Principles (Bollards) | Proc Step 3 | **TBD** — SWL, load factors, materials, proof load testing per DEL-08.09 and codes |
| Marine hardware requirements (ladders, life-saving, misc.) | SPEC § 2.3 | Guidance § Principles (Marine Hardware) | Proc Step 3 | **TBD** — ladder safety features, life-saving equipment list, Berth 10 upgrades |

## Related Deliverables (PKG-09)

This specification establishes requirements that are implemented/substantiated by other PKG-09 deliverables:

| Deliverable | Relationship | Interface Point |
|-------------|--------------|-----------------|
| DEL-09.01 Marine Outfitting Design Drawing Set | Drawings implement requirements from this specification | Drawing details shall comply with materials, installation, and quality requirements specified herein |
| DEL-09.03 Marine Outfitting Design Calculations | Calculations verify compliance with specification performance requirements | Performance requirements (energy absorption, SWL, structural adequacy) substantiated by calculations |
| DEL-09.04 Marine Outfitting Data Sheet Package | Data sheets substantiate equipment per specification requirements | Vendor datasheets shall demonstrate compliance with performance, materials, and testing requirements |
| DEL-09.05 Marine Outfitting Installation & Test Records | Records document compliance with specification installation/test requirements | Installation and test records shall verify compliance with tolerances, quality, and proof load testing requirements |

## Inputs / Dependencies (NOT_TRACKED)

Dependencies are coordinated externally (see `execution/_Coordination/_COORDINATION.md`). Typical inputs:

| Input | Source | Specification § | Guidance § | Status |
|-------|--------|-----------------|------------|--------|
| Employer's Requirements and permitting constraints | Employer | SPEC § 1.1, 1.2, Standards | — | **TBD** — clauses applicable to marine outfitting to be extracted |
| Berthing energy calculation results | DEL-08.06 | SPEC § 1.3, 2.1 | Guidance § Principles (Fenders) | **TBD** — energy absorption capacity, vessel characteristics, approach velocity |
| Mooring analysis results | DEL-08.09 | SPEC § 1.3, 2.2 | Guidance § Principles (Bollards) | **TBD** — bollard capacities, mooring line loads, environmental conditions |
| Fender system deflection characteristics | DEL-08.07 | SPEC § 2.1 | Guidance § Principles (Fenders) | **TBD** — reaction force vs deflection data for specification performance criteria |
| Fender supplier design verification | DEL-08.08 | SPEC § 2.1 | Guidance § Principles (Fenders) | **TBD** — supplier confirmation of performance compliance |
| Marine structure interface and load assumptions | PKG-08 outputs (DEL-08.01, DEL-08.03) | SPEC § 3 | Guidance § Considerations (Interface Coordination) | **TBD** — structural capacity, connection details, load transfer requirements |
| Vendor/OEM data for candidate systems | Vendor | SPEC § 2.1, 2.2, 2.3 | — | **TBD** — technical data for fenders, bollards, ladders, life-saving equipment |
| Applicable codes and standards | Employer / Regulatory Authority | SPEC § 1.2, Standards | — | **TBD** — PIANC, BS 6349, OSHA/CSA safety codes, marine safety regulations |

## Acceptance (Definition of Done)

- Specification explicitly covers all decomposition-listed artifacts for DEL-09.02 (fender specification, bollard specification, marine hardware specification).
- All Content Checklist items (above) are either resolved with cited requirements, or explicitly carried as TBD with an action owner and rationale.
- Each non-trivial requirement is traceable to a source (Employer's Requirements clause, applicable standard/code, design calculation, or documented project decision).
- Cross-document consistency verified:
  - Requirements align with design intent in `Guidance.md`
  - Requirements have verification steps in `Procedure.md`
  - Requirements are implementable via DEL-09.01 drawings
  - Requirements are substantiable via DEL-09.03 calculations and DEL-09.04 datasheets
  - Requirements have compliance verification via DEL-09.05 installation/test records
- All interfaces to PKG-08 Marine Structures and other packages are identified and coordinated (per `Specification.md § 3` and `Procedure.md § Step 6 IDC`).
- Requirements are written in verifiable terms (performance criteria, acceptance criteria, test methods clearly stated).

## References

- `Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-09 scope; DEL-09.02 definition)
- `_REFERENCES.md` (this deliverable) — lists applicable reference documents
- `Specification.md` (DEL-09.02) — meta-requirements governing this datasheet
- `Guidance.md` (DEL-09.02) — rationale and design considerations
- `Procedure.md` (DEL-09.02) — production/verification process
