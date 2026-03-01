# Guidance — DEL-006-04: Cistern & Pump Details

---

## Terminology Conventions [A-002, X-003]

*The following canonical terminology and notation conventions apply across all four DEL-006-04 production documents. These conventions are adopted to eliminate ambiguity in construction documents.*

| Subject | Canonical Term / Notation | Variants to Avoid | Rationale |
|---|---|---|---|
| 2.5 inch cistern connection serving the distribution pump | "cistern filling connection" | "fill connection", "filling connection" | RFP §3.4 and SOW-0042 use "cistern filling connection"; adopt this form consistently [A-002] |
| Pipe sizes in text | "2.5 inch" | "2.5\"", "2.5'" | Use spelled-out form in narrative text for clarity; use "2.5\"" notation only in drawing annotations and tables where space is constrained [X-003] |

---

## Purpose

DEL-006-04 exists because the West Dried Meat Lake Regional Landfill Maintenance Shop Addition has no municipal water connection. The entire building water supply — for washrooms, wash stations, emergency shower, pressure washers, water taps, and the wash bay — depends on an on-site cistern filled by bulk water delivery. The cistern and pump system is therefore the single point of supply for all potable and non-potable service water in the building.

This deliverable provides the engineered drawing set that defines how the cistern is constructed and integrated, how it is filled (external bulk fill), how water is pressurized and distributed internally (pump and distribution connection), and how the system is controlled and maintained. Without this drawing set, the construction package for the cistern and pump system cannot be tendered or built.

The decomposition assigns this deliverable to support OBJ-004 (Install and commission all mechanical, plumbing, and water storage systems to operational readiness), OBJ-003 (Produce complete P.Eng.-stamped IFC design documentation), and OBJ-001 (Deliver a code-compliant, fully functional maintenance shop addition). Source: WDMLRL_Decomposition_Claude.md, §7 PKG-006. ASSUMPTION: these objective associations are by package-grouping heuristic.

---

## Principles

### Cistern Sizing
The RFP mandates a minimum 50,000 L cistern (RFP §3.4; SOW-0041). The Plumbing Engineer should treat 50,000 L as a floor, not a target. Given the remote rural site with no municipal water, storage adequacy should be assessed against peak operational demand (wash bay, pressure washers, washrooms, emergency shower), fill truck cycle time, and any seasonal access constraints. The engineer should document the basis for final cistern volume in the calculation package (DEL-006-07).

**Basis-of-design methodology for cistern volume adequacy [A-006]:** The rationale for treating 50,000 L as a floor rather than a target is that the RFP states "Minimum 50,000L" (RFP §3.4) — the word "minimum" establishes a lower bound, not a design point. To determine whether 50,000 L is adequate, the Plumbing Engineer should, at minimum:
1. Estimate peak daily water demand (sum of all fixture and equipment demands from the plumbing fixture schedule, DEL-006-06).
2. Determine bulk water delivery frequency and volume (Owner input required — TBD per A-004).
3. Calculate reserve capacity needed to bridge delivery delays (seasonal road conditions, delivery truck availability).
4. Compare required storage (peak demand x delivery interval + reserve) against the 50,000 L minimum.
5. Document the calculation and final recommended volume in DEL-006-07 (Plumbing Calculation Package).
If the calculated requirement exceeds 50,000 L, the Plumbing Engineer should recommend a larger cistern. If 50,000 L provides excess capacity, the rationale for not reducing the volume is that 50,000 L is a contractual minimum. ASSUMPTION: this methodology is standard engineering practice; no specific methodology is prescribed in the RFP. [A-006]

### Pump Sizing Basis
The RFP specifies a 100 LPM pump with a 2.5" filling connection (RFP §3.4; SOW-0042). The Plumbing Engineer must size the pump to deliver 100 LPM at the design system head — not merely at zero head. The pump schedule (R-008) must document the total dynamic head (TDH) on which the selection is based. The 100 LPM value is a minimum; actual selection may exceed this based on system demand analysis.

### Bulk Fill vs. Distribution Separation
The RFP distinguishes two pump functions: (1) the internal service distribution pump (100 LPM, 2.5" fill connection — SOW-0042) and (2) the high-volume external fill pump for bulk water fill (SOW-0044). These are separate systems with different operational modes. The drawing set should clearly differentiate between the external fill circuit (truck-to-cistern) and the internal distribution circuit (cistern-to-building). ASSUMPTION: these may share piping segments in part, but controls and modes must be distinct to prevent operational conflict.

### System Pressurization
The RFP does not explicitly specify a pressure tank or hydropneumatic pressurization system. ASSUMPTION: a pressure tank or variable-frequency drive (VFD) on the distribution pump is likely required to avoid pump short-cycling and to maintain adequate pressure at all fixtures. The Plumbing Engineer should address pressurization strategy in the design and include relevant details in this drawing set or in DEL-006-02.

### Code and Stamp
All drawings must be issued for construction (IFC) with a P.Eng. stamp from an engineer licensed in Alberta (RFP §3.3.2; SOW-0018). Alberta Safety Codes apply. The Plumbing Engineer is responsible for determining the current applicable edition of the National Plumbing Code (as adopted in Alberta) and any provincial amendments.

---

## Considerations

### Cistern Material and Type
The RFP does not specify cistern material (concrete, fiberglass, polyethylene, steel). ASSUMPTION: the engineer selects material appropriate for the volume (50,000 L+), subsurface or above-grade installation, Alberta climate conditions, and water quality. If the cistern is below grade, frost protection, waterproofing, and access are key considerations. If above grade, thermal insulation may be required given Alberta climate. The conceptual drawing (App B-Plumb) shows the 50,000 L water storage in the utility room area — ASSUMPTION: this may be above-grade or partially below slab; the Plumbing Engineer should confirm with the Structural Engineer.

### Overflow and Drain Provisions
The cistern must have an overflow outlet to prevent overfill during bulk water delivery, and a cleanout/drain for maintenance. Overflow discharge location and drainage path must be coordinated with the civil/drainage design (PKG-005, PKG-018). Overflow into the building or utility room without positive drainage to an appropriate disposal point would be a design deficiency.

### Water Quality
ASSUMPTION: cistern water is non-potable service water (not for drinking). The RFP describes the cistern as serving industrial service functions (wash bay, pressure washers, wash sink, water taps). If any fixture is intended for potable use (e.g., washroom hand-washing), the Plumbing Engineer must address cross-connection control and any applicable potable water treatment requirements. No potable water treatment is mentioned in the RFP; this is a design determination to be made by the engineer.

**Water quality classification — TBD for human determination [C-003]:** The assumption that cistern water is non-potable is not confirmed by the RFP. The building includes washroom facilities (RFP §3.2 references washroom fixtures), and hand-washing stations typically require potable water under plumbing codes. The Plumbing Engineer and Owner must make a definitive determination:
- **If non-potable:** Document explicitly that no fixtures require potable water and that all users are informed of non-potable status. The applicable plumbing code (NPC, edition TBD per A-001) may impose signage and cross-connection control requirements even for non-potable systems.
- **If potable (or if any fixture requires potable water):** Water treatment provisions (filtration, disinfection), monitoring, and testing requirements must be added to the design scope. This would affect Specification requirements and add to the drawing set scope.
This determination has cascading impact on Specification (potential new requirements), Datasheet (water quality attributes), and Procedure (water quality verification steps). ASSUMPTION: this is a material design decision that remains unresolved. [C-003]

### Coordination with Electrical
The pump(s) require electrical connections. A 70A circuit is identified for the fire hose pump (SOW-0062) and a 70A circuit for the pressure washer (SOW-0063). The electrical design for the cistern distribution pump circuit is not explicitly broken out in the RFP beyond the general pump/plumbing scope. The Plumbing Engineer must provide electrical interface data (voltage, phase, amperage, motor kW) for all pumps so the Electrical Engineer can include appropriate circuits in PKG-004.

### Freeze Protection
Alberta climate creates freeze risk for outdoor piping and for cisterns in unheated or partially heated spaces. ASSUMPTION: if the cistern or bulk fill connection is in a space subject to freezing, heat tracing or other freeze protection measures are required. This is a significant design consideration that is not addressed in the RFP source documents available.

### Access for Excavator Cleanout
The RFP describes the wash bay mud sump as cleanable by excavator (RFP §3.4; SOW-0027b). This is a separate system from the cistern but illustrates the operational maintenance philosophy (heavy equipment servicing site). The cistern design should similarly account for maintenance access — the Plumbing Engineer should provide adequate man-way, clean-out, and service access consistent with the expected maintenance capability on site.

---

### Proceeding with Incomplete Prerequisites [X-001]
Procedure.md lists seven upstream deliverables as prerequisites (DEL-006-01, DEL-001-02, DEL-002, DEL-008-01, DEL-004, DEL-005-02, and RFP/Appendix B sources). In a design-build project with parallel design tracks, some of these may not be available when design work on DEL-006-04 begins. The Plumbing Engineer should be aware of the following risks if prerequisites are incomplete:
- **Geotech (DEL-008-01) unavailable:** If the cistern installation type (below-grade vs. above-grade) depends on geotechnical conditions and the geotech report is not yet available, the design cannot be finalized. The engineer may proceed with preliminary design assuming one installation type, but must flag this as a design hold point and revisit when geotech data arrives. Source: Procedure.md Step 2.2. [X-001]
- **Structural (DEL-002) unavailable:** Cistern location and structural support depend on structural coordination. If structural design is not yet advanced, the Plumbing Engineer should issue a coordination request early and document assumptions about available structural capacity. Source: Procedure.md Step 3.1. [X-001]
- **Electrical (DEL-004) unavailable:** Pump electrical interface data can be provided to the Electrical Engineer before the electrical design is complete, but circuit assignments (including resolution of CONF-002, the fire hose pump identity question) require a response. Source: Procedure.md Step 3.1, Guidance.md CONF-002. [X-001]

ASSUMPTION: parallel design is expected in a design-build context; the above guidance is standard practice, not explicitly addressed in the RFP. [X-001]

---

## Trade-offs

| Trade-off | Option A | Option B | Guidance |
|---|---|---|---|
| Cistern type | Below-grade (concrete or fiberglass) | Above-grade (polyethylene or steel tank in utility room) | ASSUMPTION: below-grade conserves utility room space and provides frost protection; above-grade is simpler to install but requires insulation and structural support. Plumbing Engineer to determine based on geotech results and structural coordination. |
| Distribution pump type | Fixed-speed centrifugal pump with pressure tank | Variable frequency drive (VFD) pump without pressure tank | ASSUMPTION: VFD approach provides better pressure control and energy efficiency but higher capital cost. Both are acceptable if flow and pressure requirements are met. |
| Bulk fill pump location | Permanent installed pump | Portable/removable pump at fill connection | ASSUMPTION: RFP implies a permanent system ("Install bulk water fill system" SOW-0044); permanent installation preferred for reliability. |

---

## Examples

*No design examples are available in the source documents for this specific system configuration. The conceptual plumbing drawing (Appendix B — Plumbing) provides a schematic plan layout only — it does not show system details.*

*The Plumbing Engineer should reference comparable industrial cistern and pump system designs from similar Alberta rural facilities as a design basis. Location TBD for any comparable project references.*

---

## Assumption Rationale Register [D-003]

*The following table consolidates assumptions made in the production documents, their basis, and the impact if the assumption proves incorrect. This register supports traceability from ASSUMPTION labels in Specification and Datasheet back to the reasoning that produced them.*

| Assumption ID | Assumption | Where Used | Basis | Impact if Wrong |
|---|---|---|---|---|
| ASM-001 | Cistern water is non-potable | Guidance §Water Quality, Specification (implicit in scope) | RFP describes industrial service functions; no potable water treatment mentioned | If potable water is required: add treatment, monitoring, and testing requirements; expand drawing set scope; likely increase cost |
| ASM-002 | Pressure tank or VFD likely required | Datasheet §Distribution Pump System, Guidance §System Pressurization | Standard practice for pressurized distribution systems to prevent pump short-cycling | If neither is required: remove pressure tank from drawing set; simplify system |
| ASM-003 | Pump schedule documentation (R-008) | Specification R-008 | Standard plumbing engineering practice | If client has different documentation requirements: revise pump schedule format |
| ASM-004 | Electrical interface documentation (R-010) | Specification R-010 | Required for design coordination per SOW-0016 scope | If electrical interface is handled differently: revise coordination approach |
| ASM-005 | Maintenance access (R-011) | Specification R-011 | Standard plumbing design practice for industrial facilities | If specific access requirements differ: revise access provisions |
| ASM-006 | Freeze protection required (R-013) | Specification R-013, Guidance §Freeze Protection | Alberta climate; rural site; outdoor/unheated components | If all components are in heated spaces: freeze protection may be reduced |
| ASM-007 | Bulk fill and distribution are separate systems | Guidance §Bulk Fill vs. Distribution Separation | RFP distinguishes two pump functions (SOW-0042, SOW-0044) | If systems are combined: revise piping diagrams and control logic |
| ASM-008 | Cistern below-grade preferred | Guidance §Trade-offs | Below-grade conserves utility room space and provides frost protection | If above-grade is selected: add insulation, structural support requirements |

*Source: Specification.md §Requirements (R-008, R-010, R-011 marked ASSUMPTION); Guidance.md §Considerations, §Trade-offs. [D-003]*

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-001 | Cistern location: conceptual drawing shows 50,000 L water storage adjacent to utility room / near stairs to mezzanine, but the cistern volume at 50,000 L is very large and may not physically fit in the utility room as shown in the conceptual plan. Final location requires structural and spatial coordination. Semantic lensing [C-001] confirms no corresponding requirement or acceptance criterion addresses resolution of this physical incompatibility. | App B-Plumb (conceptual drawing — cistern shown in utility room area) | RFP §3.4 (50,000 L minimum) | Datasheet §Attributes (cistern location, cistern installation type), Specification R-009 | PROPOSAL: Plumbing Engineer + Structural Engineer + Architect joint resolution during preliminary design phase. Conceptual drawing is schematic only. [C-001] | TBD |
| CONF-002 | Pump circuit identity: the RFP specifies a 70A circuit for the "fire hose pump" (SOW-0062 via App B-Elec) and a separate 70A circuit for the pressure washer (SOW-0063). It is unclear whether the 100 LPM internal distribution pump is the same as, or distinct from, the "fire hose pump." If they are the same pump, the 70A circuit is established. If distinct, an additional circuit must be designed. Semantic lensing [B-004] confirms this creates an incoherent signal across electrical and plumbing documents. | Decomposition SOW-0062 / App B-Elec ("70A circuit for fire hose pump") | RFP §3.4 / SOW-0042 ("Pump capable of 100 LPM... for internal service water distribution") | Specification R-010, Datasheet §Attributes (distribution pump, pressure washer circuit) | PROPOSAL: Plumbing Engineer + Electrical Engineer joint determination. Human ruling needed if these are distinct systems requiring separate circuits. [B-004] | TBD |
