# Guidance — DEL-015-02 Lighting Installation

**Deliverable ID:** DEL-015-02
**Title:** Lighting Installation
**Package:** PKG-015 — Electrical & Low-Voltage Installation
**Document Status:** SEMANTIC_READY (Pass 3 enrichment applied)
**Prepared By:** 4_DOCUMENTS Agent
**Date:** 2026-02-26

---

## Purpose

This deliverable exists to provide a safe, effective, and code-compliant lighting system for all occupied areas of the New North Shop addition at the West Dried Meat Lake Regional Landfill. Adequate lighting directly supports the facility's operational program (OBJ-001): mechanics and staff performing vehicle and equipment maintenance require sufficient illumination for safe and productive work. The lighting system also supports OBJ-005, which requires all electrical systems to be installed and commissioned to operational readiness by December 31, 2026.

The five SOWs (SOW-0052 through SOW-0056) establish the minimum fixture counts and types for each zone. The conceptual Appendix B (Electrical) drawing establishes the intended spatial layout. The final engineered IFC drawings will be the governing installation reference.

*Sources: Decomposition §5 OBJ-001, OBJ-005; _CONTEXT.md; App B-Elec*

---

## Principles

### P-1: Source Fidelity for Fixture Counts
The fixture counts defined in App B-Elec and the SOWs are explicit owner requirements, not suggestions. The Main Shop requires exactly 20 high-bay fixtures (5 rows x 4); the Wash Bay requires exactly 6 (2 rows x 3); Office 1, Utility Room 2, Parts/Tool Room 6. The electrical engineer's IFC drawings may refine exact mounting positions but must not reduce total quantities without an owner-approved change.

*Source: SOW-0052–SOW-0056; App B-Elec Electrical Notes*

### P-2: High-Bay Selection for 35-foot Ceilings
The Main Shop has a 35-foot concrete structure ceiling. High-bay fixtures are the appropriate technology at this mounting height; standard commercial troffer or strip fixtures would be inadequate. The 150 W / 22,000-lumen specification for the Main Shop is owner-defined and establishes a minimum performance floor. Selection of specific fixtures should verify photometric compliance (uniformity, minimum maintained illuminance) against applicable standards.

*Source: RFP §3.4 ("Concrete structure 35' ceiling"); App B-Elec Electrical Notes*

### P-3: LED-Only Technology
All fixtures shall be LED. This is consistent with the owner's explicit specification of LED for all zones (App B-Elec uses "LED" and "High Bay Lights" descriptors throughout). LED technology provides energy efficiency, reduced maintenance, and long service life appropriate for an industrial maintenance facility with high ceilings where lamp replacement would otherwise require elevated access equipment.

*Source: App B-Elec; SOW-0052–SOW-0056; ASSUMPTION re: rationale*

### P-4: Wet-Location Rating for Wash Bay
ASSUMPTION: The Wash Bay is a washing environment designed for large equipment (including motor scrapers). The CSA C22.1 Canadian Electrical Code requires fixtures in wet or damp locations to be appropriately listed and rated (wet-location IP rating, e.g., IP65 or equivalent, or NEMA 4/4X). The fixture selection for Zone Z-2 should be confirmed by the Electrical Engineer of Record (EOR) for the correct environmental rating.

*Source: ASSUMPTION based on building function (App B-Elec, RFP §3.4 "Single enclosed bay dedicated for washing large equipment"); CSA C22.1 (location TBD)*

### P-5: Coordination with Overhead Cranes
The Main Shop contains two 5-tonne overhead cranes on trolleys. Lighting fixture mounting heights, suspension lengths, and lateral positions must be coordinated with the crane rail elevation, the maximum hook height, and the crane bridge clearance envelope. Fixtures mounted too low or in the crane's travel path will create a safety hazard and may require relocation during or after crane installation. This coordination should occur at the IFC drawing stage, not in the field.

*Source: App B-Elec (cranes shown on floor plan); RFP §3.4 ("2 – 5-tonne overhead cranes on a trolley"); ASSUMPTION re: coordination approach*

---

## Considerations

### C-1: Lighting Design vs. Conceptual Layout — and the Illuminance Performance Gap
The Appendix B (Electrical) drawing is a **conceptual** drawing, not an engineered design. It establishes intent (zone locations, approximate row/column layout, fixture types, quantities) but does not constitute a photometric study or a code-compliant design. The electrical engineer producing the IFC drawings should perform (or review) a photometric analysis to confirm that the specified fixture counts and arrangements achieve required maintained illuminance levels for the occupancy type.

ASSUMPTION: Alberta Safety Codes and the National Building Code of Canada (NBC) prescribe minimum maintained illuminance levels by occupancy/task type. Specific lux/footcandle targets are TBD pending the engineer's photometric study. **TBD question: What are the minimum maintained illuminance levels required by the NBC / Alberta Safety Codes for each occupancy type in this facility (industrial workshop, office, wash bay)?** Resolution authority: EOR, confirmed per NBC and applicable standards. *(Enrichment: F-001; source: Guidance C-1 existing content; NBC location TBD)*

**Rationale for system-level verification:** The current verification regime (Specification §Verification) checks fixture count and manufacturer data sheet specifications. This confirms that the correct components are installed, but does not confirm that the installed system actually delivers adequate light at task height. The difference between component compliance and system performance matters because fixture mounting height, spacing, reflectance of surrounding surfaces, and light loss factors all affect delivered illuminance. A photometric analysis by the EOR bridges this gap. *(Enrichment: X-003; source: ASSUMPTION based on lighting engineering principles; Specification REQ-L-16)*

*Source: App B-Elec drawing notes ("APPENDIX B" header indicates conceptual status); RFP §3.3.2*

### C-2: Circuit Design, Panel Capacity, and Voltage Drop Compliance
The source documents do not specify the number of lighting circuits, circuit breaker sizes, or panel assignments for the lighting system. This information is TBD and will be established in the IFC electrical drawings. The electrical designer should ensure the lighting load is accommodated within the main distribution panel capacity (DEL-015-01 scope) and that circuit lengths are appropriate for voltage drop compliance.

**Voltage drop rationale:** Excessive voltage drop on branch circuits reduces fixture light output and may cause operational issues (flicker, reduced lamp life). CSA C22.1 recommends (ASSUMPTION: typically 3% maximum on branch circuits, 5% total from service entrance to the farthest outlet — specific rule reference TBD per applicable edition). For the Main Shop with a 35-foot ceiling height and potentially long horizontal runs, voltage drop should be verified by the EOR during circuit design. *(Enrichment: F-004; source: ASSUMPTION based on CSA C22.1 general guidance; specific clause location TBD)*

*Source: App B-Elec (circuit details not shown on conceptual drawing); TBD*

### C-3: Switching Strategy
The conceptual drawing does not show switch locations for the lighting zones. The switching strategy (manual switches, occupancy sensors, daylight harvesting, zone grouping) is TBD in the final design. For an industrial maintenance shop with extended and variable hours of use, a practical switching strategy with clear zone control is recommended.

**Decision required:** Will lighting controls include occupancy sensing, daylight harvesting, or manual switching only? The Owner must select the strategy; the EOR will implement it in the IFC drawings. Resolution milestone: IFC drawing issuance. *(Enrichment: B-003; sources: App B-Elec shows no switch locations; Specification REQ-L-14 TBD; Datasheet §Construction TBD)*

*Source: App B-Elec (no switching shown); TBD*

### C-4: Emergency / Exit Lighting
Emergency lighting and exit signs are not explicitly called out in the SOWs or the Appendix B conceptual drawing. ASSUMPTION: Emergency lighting is required under the Alberta Safety Codes / National Building Code for occupied commercial/industrial buildings. The electrical engineer's design should address this. If included, emergency lighting may be a separate scope item or sub-item within this deliverable — TBD.

*Source: ASSUMPTION based on Alberta Safety Codes requirements; not specified in App B-Elec or SOWs*

### C-5: Scheduling Dependency and Ceiling Fan Coordination
Lighting installation cannot be completed (and certainly not commissioned) until:
1. The building structure and ceiling are complete (external dependency per _DEPENDENCIES.md)
2. The three-phase power service is energized (DEL-015-01 upstream dependency)

Ceiling fans (a separate scope item per App B-Elec: "6 Ceiling Fans for Main Shop") share the ceiling space with the Main Shop high-bay fixtures. Coordination of mounting locations is advisable. **The ceiling fan scope ownership is unresolved** — see CONF-L-03 in the Conflict Table below. If ceiling fans are installed in the same zone as the 20 high-bay fixtures, their mounting positions and any structural supports should be coordinated at the IFC drawing stage to avoid spatial conflicts or rework.

*Source: _DEPENDENCIES.md; App B-Elec Electrical Notes (ceiling fans noted separately)*

### C-6: Maintenance Access
At 35-foot ceiling height in the Main Shop, future lamp/fixture maintenance will require elevated access equipment (aerial work platform or scaffolding). The fixture mounting system should be compatible with safe re-lamping or fixture replacement procedures. LED fixtures with rated service lives of 50,000+ hours significantly reduce maintenance frequency at this height.

*Source: ASSUMPTION based on building height (RFP §3.4); industry practice*

### C-7: Energy Code Applicability (NECB)
ASSUMPTION: The National Energy Code for Buildings (NECB) may apply to this facility and may establish maximum lighting power density (LPD) limits for the building occupancy types present (industrial workshop, office, utility). The LED-only specification (P-3) is directionally consistent with energy efficiency, but the EOR should confirm whether NECB compliance is required and, if so, whether the specified fixture counts and wattages meet the applicable LPD limits.

**TBD question:** Does the NECB apply to this facility? If so, what are the LPD limits for each occupancy zone? Resolution authority: EOR, confirmed during IFC design.

*(Enrichment: F-005; source: ASSUMPTION; NECB applicability not addressed in RFP or App B-Elec)*

### C-8: Applicable CSA C22.1 Sections
ASSUMPTION: The following sections of CSA C22.1 (Canadian Electrical Code, Part 1) are expected to be applicable to this lighting installation. The specific edition and clause numbers shall be confirmed by the EOR during IFC design:
- **Section 30** — Installation of Lighting Equipment (general requirements for luminaire installation)
- **Section 22** — Wiring Methods (conduit, cable, conductor requirements)
- **Section 26** — Installation of Overcurrent Devices (circuit breaker sizing for lighting circuits)
- **Section 62** — Fixed Electric Heating Systems (if radiant heating interacts with ceiling fixtures — TBD)

**TBD:** EOR to identify the complete list of applicable CSA C22.1 sections and confirm the edition in use.

*(Enrichment: C-002; source: ASSUMPTION based on CSA C22.1 structure; specific clause numbers location TBD)*

---

## Trade-offs

| Trade-off | Option A | Option B | Recommendation | Source / Notes |
|---|---|---|---|---|
| Wash Bay fixture IP rating | IP65 (dust-tight, water jet resistant) | IP44 (splash-proof only) | ASSUMPTION: IP65 or higher preferred for direct wash bay use; confirm with EOR | ASSUMPTION; CSA C22.1 (location TBD) |
| High-bay mounting — Main Shop | Fixed pendant / chain mount | Adjustable aircraft cable | TBD per IFC design; aircraft cable common for large high-bay spaces | ASSUMPTION |
| Switching — Main Shop | Individual row switching | Zone-based (e.g., north half / south half) | Zone-based may reduce energy use when only part of the shop is occupied | ASSUMPTION; not specified in sources |
| Emergency lighting | Integrated into this deliverable | Separate sub-scope | TBD; to be confirmed by EOR and permit authority | ASSUMPTION |

---

## Examples

TBD — No specific fixture model examples are available in the source documents. Fixture selection will be determined during the IFC design phase by the Electrical Engineer of Record, subject to the minimum performance requirements in REQ-L-02 and the owner's approval.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-L-01 | Wash Bay fixture lumen/wattage not specified. App B-Elec specifies 150 W / 22,000 lm for Main Shop only; no equivalent specification is given for Wash Bay. It is unclear whether the Wash Bay should match Main Shop performance or use a different specification. | App B-Elec Electrical Notes (Main Shop spec explicit) | SOW-0053 (no performance spec) | Spec REQ-L-04; Datasheet Z-2; Procedure Step 4b | PROPOSAL: Electrical Engineer to specify Wash Bay fixture performance in IFC drawings based on photometric analysis of the 2-row x 3-fixture layout at the Wash Bay ceiling height. | TBD |
| CONF-L-02 | Emergency/exit lighting: not called out in SOWs or App B-Elec, but likely required by Alberta Safety Codes. Inclusion is ambiguous — could be considered implicit in "code compliance" or a separate scope gap. Now addressed normatively in Spec REQ-L-15 as a conditional requirement pending Owner/AHJ ruling. | App B-Elec (no emergency lighting shown) | RFP §3.3.2 (building must adhere to Alberta Safety Codes) | Spec §Scope, REQ-L-15; Procedure | PROPOSAL: Confirm with Owner and permit authority whether emergency/exit lighting is within this deliverable scope or a separate scope item. *(Enrichment: A-001, C-003)* | TBD |
| CONF-L-03 | Ceiling fan coordination and ownership: App B-Elec notes "6 Ceiling Fans for Main Shop" which share the Main Shop ceiling with 20 high-bay fixtures. Fan scope is not assigned to DEL-015-02 and no other deliverable is explicitly identified as the owner. Spatial coordination is necessary regardless of ownership. | App B-Elec Electrical Notes (fans noted) | Decomposition (fans not assigned to DEL-015-02; no explicit assignee identified) | Spec REQ-L-12; Procedure Steps 3, 4, 8a; Procedure new Step 3a | PROPOSAL: Owner/PM to (a) assign ceiling fan scope to a specific deliverable and (b) confirm coordination interface with DEL-015-02 in IFC drawings. *(Enrichment: E-001, C-004)* | TBD |
| CONF-L-04 | Old North Shop lighting scope: previously listed as conditionally excluded ("unless explicitly included in issued construction drawings — TBD"). Now clarified as explicitly excluded pending formal scope change. If the Owner intends to include Old North Shop lighting, a change order is required. | App B-Elec (scope limited to New North Shop) | _CONTEXT.md (no mention of Old North Shop) | Spec §Scope — Out of Scope | PROPOSAL: Owner to confirm scope exclusion. *(Enrichment: X-001)* | TBD |
