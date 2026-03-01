# Guidance — DEL-014-02: Septic System

---

## Purpose

DEL-014-02 exists to provide a code-compliant, fully functional wastewater holding and treatment system for the new West Dried Meat Lake Regional Landfill Maintenance Shop Addition. The septic system supports the facility's operational program by safely collecting and containing sanitary wastewater from the shop's washroom, wash station, and other plumbing fixtures, allowing periodic pump-out by a waste haulage service.

This deliverable directly supports:
- **OBJ-001**: Deliver a code-compliant, fully functional maintenance shop addition and associated renovations that satisfy the County's operational program.
- **OBJ-004**: Install and commission all mechanical, plumbing, and water storage systems to operational readiness — explicitly includes the septic system. (Source: Decomposition, Objectives section)

ASSUMPTION (PACKAGE_HEURISTIC): OBJ-001 and OBJ-004 are associated with this deliverable based on explicit mapping in the Decomposition (DEL-014-02 row and Objective-to-Package mapping table). This is confirmed at the deliverable-ID level and does not require additional inference.

---

## Principles

### 1. Holding Tank, Not a Treatment System
The RFP specifies a 2,000 US gal septic **holding** tank (RFP §3.4), not a full treatment system (e.g., with a drain field). This is appropriate given the remote landfill site context and the likely need for periodic pump-out by vacuum truck. (Source: RFP §3.4; SOW-0043). The design implication is that the system must provide adequate holding volume between pump-out cycles, and convenient vacuum truck access must be planned.

### 2. Removal Before Installation
The existing septic tank must be removed as part of this scope (SOW-0043; D-002). The removal must occur in coordination with the installation of the new tank to avoid service interruption during construction — or, where no active connection exists, as a site clearing activity. The existing tank's contents and structure must be disposed of in accordance with the Alberta Environmental Protection and Enhancement Act (EPEA) and the Alberta Waste Control Regulation (see Specification REQ-014-02-03).

### 3. Scope Boundary: No Relocation
Decision D-002 (Decomposition Decision Log) explicitly resolved that relocation of the existing septic tank is OUT of scope. SOW-0043 was updated accordingly. Contractors and designers must not include relocation work. Only removal (and off-site disposal or decommissioning) is included.

### 4. Design Dependency
The IFC installation drawings (DEL-006-05, produced by PKG-006 Plumbing Design) govern the precise location, connection details, invert elevations, bedding specifications, and access provisions. Installation must not begin until DEL-006-05 is approved and on file. The conceptual drawing (Appendix B — Plumbing, R-06) shows the tank located at the north end of the New North Shop building and is indicative only.

### 5. Interface Coordination
The septic system receives wastewater from two downstream systems:
- DEL-014-04 (Floor Drains & Sump Drains): floor drain connections must be coordinated so drainage flows correctly to the holding tank.
- DEL-014-06 (Plumbing Fixtures): fixture connections (washroom, wash station) must drain to the holding tank.

Both of these are listed as downstream dependencies in _DEPENDENCIES.md. Sequencing and pipe routing must be coordinated with DEL-014-04 and DEL-014-06 to avoid rework.

---

## Considerations

### Site Conditions
The project site is at SW 14–44–21–W4, near Ferintosh, Alberta. The site is remote and served by the County-owned landfill property. Ground conditions must be assessed via the geotechnical investigation (required per RFP §3.3.2) to determine appropriate bedding, embedment depth, and frost protection requirements for the holding tank.

ASSUMPTION: Frost depth in this region of central Alberta typically exceeds 1.5 m; tank installation depth and insulation requirements must be confirmed by the Plumbing Engineer of Record. (Source: ASSUMPTION — specific frost depth TBD pending geotechnical investigation.)

### Winterization and Frost Protection [B-005]
Given the central Alberta climate, winterization and frost protection are essential considerations for a buried holding tank. The following measures should be evaluated by the Plumbing Engineer of Record in conjunction with the geotechnical investigation report:
- **Minimum burial depth:** Tank crown and all inlet/outlet connections must be installed below the frost line or be adequately insulated to prevent freezing. The applicable Alberta Plumbing Code requirements for minimum burial depth of sewage piping and tanks shall govern (specific clause TBD — location TBD).
- **Insulation:** If the installation depth is insufficient to place all components below the frost line, rigid board insulation or equivalent thermal protection may be required around the tank and connecting pipes. ASSUMPTION: standard practice for cold-climate holding tanks.
- **Heat trace:** In extreme cases, electric heat trace on inlet/outlet piping may be needed; coordinate with PKG-015 (Electrical) if applicable. ASSUMPTION: unlikely for a holding tank at adequate depth, but should be evaluated.
- **Access riser protection:** The access manway riser extending to grade is exposed to frost; insulated or frost-resistant riser materials should be specified.
PROPOSAL: Plumbing Engineer of Record + geotechnical report to specify winterization requirements [B-005]. See also Specification REQ-014-02-10.

### Pump-Out Access and Frequency
A 2,000 US gal holding tank will require periodic vacuum truck pump-out. The tank location on the north side of the building (per R-06) must allow unobstructed vehicle access. The final site layout, grading, and drive surface design (PKG-018) must accommodate vacuum truck approach and egress.

**Pump-out frequency and lifecycle cost considerations [A-005]:** The expected pump-out frequency depends on the facility's daily wastewater generation rate, which is TBD pending confirmation of fixture count and usage patterns (see DEL-014-06 Plumbing Fixtures). ASSUMPTION: for a maintenance shop with washroom and wash station facilities serving a limited number of personnel, pump-out frequency is likely in the range of monthly to quarterly — but this must be confirmed by the Plumbing Engineer of Record based on estimated daily flows. The Owner should consider the ongoing operational cost of periodic pump-out service when evaluating tank sizing (see Trade-offs table — tank size option). PROPOSAL: Plumbing Engineer of Record or Owner operations staff to estimate expected pump-out frequency and approximate annual cost prior to final tank sizing decision [A-005].

### Alarm / Monitoring
ASSUMPTION: A high-level alarm (audible or visual) may be required by Alberta plumbing regulations for holding tanks to prevent overflow. Specific requirements TBD pending confirmation by the Plumbing Engineer of Record and review of applicable Alberta Safety Codes.

### Environmental and Regulatory
Disposal of the existing septic tank's contents and structure is subject to Alberta Environmental Protection and Enhancement Act (EPEA) and Alberta Waste Control Regulation requirements, and potentially Camrose County bylaws. The Contractor must confirm disposal requirements prior to demolition. (Source: ASSUMPTION — specific requirements TBD; general regulatory framework identified; see Specification REQ-014-02-03 [C-001].)

**Environmental stewardship beyond regulatory compliance [E-001]:** As this installation occurs on a County-owned landfill property, the following environmental stewardship measures should be considered:
- **Groundwater protection during existing tank removal:** Ensure that no contaminated liquids are released to the ground during pump-out and removal. Spill containment measures (e.g., containment berms, absorbent materials) should be on-site during pump-out operations.
- **Spill containment during vacuum truck operations:** Both during existing tank pump-out and future operational pump-outs, spill prevention and containment provisions should be in place at the pump-out access point.
- **Site restoration quality:** Disturbed areas should be restored to a condition consistent with or better than pre-construction conditions, taking into account the landfill site context and County environmental policies.
ASSUMPTION: these measures are consistent with good practice for a County-owned facility on a landfill site; specific County environmental policies TBD. PROPOSAL: Owner/County environmental policy to confirm stewardship expectations [E-001].

### Lifecycle and Maintenance [C-003]
A comprehensive appraisal of the septic system's value should include lifecycle considerations beyond the installation phase:
- **Expected tank service life:** TBD — depends on tank material selection (see Trade-offs table). ASSUMPTION: typical service life for a polyethylene or fiberglass holding tank is 20–30 years; concrete tanks may last longer but are subject to corrosion from hydrogen sulfide. Specific service life data should be obtained from the tank manufacturer's data sheet.
- **Manufacturer warranty vs. project warranty:** The project warranty (2 years post-CCC per RFP §2.10.2) is shorter than typical manufacturer warranties for tank vessels. The Owner should retain the manufacturer's warranty documentation separately for the full manufacturer-warranted period.
- **Periodic inspection requirements:** The holding tank should be inspected periodically (frequency TBD — ASSUMPTION: annually at minimum) for structural integrity, access manway condition, and inlet/outlet connection integrity. Alberta Private Sewage Systems Standard of Practice may specify inspection frequency requirements (TBD — location TBD).
- **Long-term pump-out contract:** The Owner should establish a standing service contract with a licensed waste haulage provider for regular pump-out service. Contract terms should include emergency pump-out provisions and response time commitments appropriate for a remote landfill site.
PROPOSAL: Plumbing Engineer of Record + Owner operations staff to define lifecycle maintenance plan [C-003].

### Coordination with Plumbing Design Package
DEL-006-05 (Septic System Details, PKG-006) is the design deliverable that directly feeds this installation deliverable. The Plumbing Contractor should engage with the Plumbing Engineer of Record during design development to ensure constructability and access provisions are incorporated into the IFC drawings.

---

## Trade-offs

| Trade-off | Option A | Option B | Recommended Direction | Rationale |
|---|---|---|---|---|
| Tank material (fiberglass vs. concrete/polyethylene) | Fiberglass or polyethylene — lighter, easier to install | Concrete — heavier, may require larger equipment | TBD (defer to Plumbing Engineer of Record, DEL-006-05) | Material selection affects installation equipment, bedding requirements, and longevity; must be confirmed by engineer per Alberta code |
| Tank size (exactly 2,000 US gal vs. larger) | Exactly 2,000 US gal as specified in RFP §3.4 | Larger capacity to reduce pump-out frequency | 2,000 US gal minimum per RFP §3.4; larger may be proposed if cost-effective | RFP §3.4 states minimum; larger capacity is a design decision for the Plumbing Engineer and Owner |
| Removal timing (remove existing tank before or during new tank install) | Remove existing before new installation (sequential) | Remove and install simultaneously | ASSUMPTION: Coordinate to minimize service disruption | Sequencing should be confirmed with Owner and existing site conditions |

---

## Examples

No project-specific examples are available from accessible sources at this stage. The following reference context is noted for future enrichment [X-001]:

- **Comparable installations:** Rural Alberta municipal maintenance facilities and County-owned utility buildings commonly use septic holding tanks in the 2,000–5,000 US gal range where municipal sewer service is not available. The Plumbing Engineer of Record may be able to provide reference examples from comparable installations in central Alberta.
- **Precedent for cold-climate holding tanks:** The Alberta Private Sewage Systems Standard of Practice (TBD — location TBD) may include reference installation details for holding tanks in frost-prone regions.

PROPOSAL: Plumbing Engineer of Record to provide one or more reference examples of comparable rural Alberta holding tank installations during design development to inform constructability and operational planning [X-001].

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-014-02-01 | RFP §3.4 states "2,000 US Gallon Septic holding tank. (potentially removal and relocate existing septic tank)" — suggesting possible relocation. Decision D-002 in the Decomposition resolves this as removal IN, relocation OUT. This conflict should be resolved before installation commences [D-003]. | RFP §3.4 (R-01, page 13) | Decomposition D-002; SOW-0043 | Specification REQ-014-02-03; Procedure Step 2 | PROPOSAL: Accept D-002 resolution — removal IN, relocation OUT. The Decomposition's Decision Log represents the proponent's interpretation and should govern. If Owner/County requires relocation, a scope change order is needed. Resolution required before installation [D-003]. | TBD |
