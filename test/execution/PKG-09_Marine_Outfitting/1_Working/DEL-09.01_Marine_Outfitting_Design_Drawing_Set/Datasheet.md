# Datasheet: DEL-09.01 Marine Outfitting Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-09.01 |
| Name | Marine Outfitting Design Drawing Set |
| Package | PKG-09 Marine Outfitting |
| Discipline | Marine |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Scope (Decomposition)

**Package scope (PKG-09):** Fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades and repairs. (**Source:** Decomposition, PKG-09)

**Deliverable intent (DEL-09.01):** Defines the design arrangement and details for marine outfitting per Employer's Requirements. (**Source:** Decomposition, DEL-09.01 row)

**Anticipated artifacts (from decomposition):**
- Fender arrangement drawings
- Bollard installation details
- Ladder details

## Deliverable Attributes (Drawing Set)

| Attribute | Value |
|-----------|-------|
| Drawing / sheet numbering system | **TBD** — per project document control procedure |
| Sheet sizes | **TBD** — **ASSUMPTION:** ANSI D or ISO A1 for general arrangements; smaller sizes for details |
| CAD / BIM standard | **TBD** — project CAD standard to be established |
| Coordinate / datum requirements | **TBD** — consistent with site survey basis and PKG-08 Marine Structures coordination |
| Revision scheme | **TBD** — per project document control procedure |
| IFC / issue format | **TBD** — **ASSUMPTION:** PDF for review/approval; native CAD files for construction |

## Content Checklist (Minimum)

This datasheet defines the expected **content** of the drawing set (not the final design values). Each item corresponds to requirements in `Specification.md § 1` and has verification steps in `Procedure.md`.

| Content Item | Specification § | Procedure Step | Status |
|--------------|-----------------|----------------|--------|
| Fender arrangement and setting-out | SPEC § 1.1 | Proc Step 3, 4 | **TBD** — layout, elevations/sections, anchor details, interfaces to marine structures (PKG-08) |
| Bollard arrangement and installation details | SPEC § 1.2 | Proc Step 3, 4 | **TBD** — locations, foundations/anchors, proof-load provisions per ER or codes |
| Ladder details | SPEC § 1.3 | Proc Step 3, 4 | **TBD** — type, fixing, safety features (cages, rest platforms) per ER and safety codes |
| Life-saving equipment arrangement/details | SPEC § 1.4 | Proc Step 3, 4 | **TBD** — scope included in PKG-09; equipment list and mounting details per ER |
| Existing Berth 10 upgrade/repair details | SPEC § 1.5 | Proc Step 3, 4 | **TBD** — specific repairs per ER and condition survey; tie-in constraints |
| General notes (materials, corrosion protection) | SPEC § 1.6 | Proc Step 4 | **TBD** — as required by ER; coordinate with PKG-08 materials specifications |
| Interfaces and references | SPEC § 3 | Proc Step 6 (IDC) | **TBD** — tie-ins to PKG-08 Marine Structures; process/mechanical safety zone interfaces |

## Inputs / Dependencies (NOT_TRACKED)

Dependencies are coordinated externally (see `execution/_Coordination/_COORDINATION.md`). Typical inputs for this deliverable:

| Input | Source | Specification § | Guidance § | Status |
|-------|--------|-----------------|------------|--------|
| Employer's Requirements and permitting constraints | Employer | SPEC § Standards | — | **TBD** — clauses applicable to marine outfitting to be extracted |
| Marine structure design basis and geometry | PKG-08 outputs (DEL-08.01, DEL-08.03) | SPEC § 3 | Guidance § Principles (Fenders, Bollards) | **TBD** — interface locations and structural capacities |
| Berthing energy calculation results | DEL-08.06 | SPEC § 1.1 | Guidance § Principles (Fenders) | **TBD** — informs fender selection/arrangement |
| Fender system deflection characteristics | DEL-08.07 | SPEC § 1.1 | Guidance § Principles (Fenders) | **TBD** — reaction force vs deflection data |
| Fender supplier design verification | DEL-08.08 | SPEC § 1.1 | Guidance § Principles (Fenders) | **TBD** — confirmation of fender performance |
| Mooring analysis results | DEL-08.09 | SPEC § 1.2 | Guidance § Principles (Bollards) | **TBD** — informs bollard locations and capacities |
| Site survey / as-built information for existing Berth 10 | Survey | SPEC § 1.5 | Guidance § Considerations (Existing Works) | **TBD** — condition assessment and tie-in constraints |
| Vendor data for selected fender/bollard systems | Vendor | SPEC § 1.1, 1.2 | — | **TBD** — installation requirements, fixing details |

## Acceptance (Definition of Done)

- Drawing set content matches the decomposition "anticipated artifacts" list for DEL-09.01.
- All Content Checklist items (above) are either resolved with cited design data, or explicitly carried as TBD with an action owner.
- Cross-reference verification completed against `Specification.md` requirements (all SPEC § 1.1–1.6 requirements addressed).
- Cross-document consistency verified with `Guidance.md` (design intent) and `Procedure.md` (verification steps).
- Interdisciplinary check completed for interfaces affecting other disciplines/packages (**TBD**: project IDC procedure per `Procedure.md § Step 6`).
- All drawings comply with `Specification.md § 2` quality/drafting requirements.

## References

- `Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-09 scope; DEL-09.01 definition)
- `_REFERENCES.md` (this deliverable) — lists applicable reference documents
- `Specification.md` (DEL-09.01) — requirements governing this datasheet
- `Guidance.md` (DEL-09.01) — rationale and design considerations
- `Procedure.md` (DEL-09.01) — production/verification process
