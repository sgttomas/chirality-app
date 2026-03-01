# Guidance — DEL-014-06: Plumbing Fixtures

---

## Purpose

DEL-014-06 provides the point-of-use water access fixtures that make the maintenance shop functional as a working facility. The two SOW items in scope — water taps with pressure washer reel (SOW-0049) and industrial wash station (SOW-0050) — represent the final layer of the plumbing system: the interfaces between the building's water infrastructure and the people who operate it daily.

The fixtures in this deliverable are operationally significant:
- Water taps and the pressure washer reel enable equipment cleaning and general water access throughout the shop, supporting day-to-day maintenance operations at a landfill facility handling heavy tracked and packer equipment.
- The industrial wash station (wash sink) provides a dedicated handwashing and parts-washing point separate from the washroom, consistent with industrial hygiene requirements and the RFP's explicit call for a "separate industrial wash sink" (R-01 §3.1).

Without these fixtures, the cistern and distribution system (DEL-014-01) has no operable endpoints in the main shop and work area, and the facility fails its operational program.

Source: R-01 §3.1 ("The Shop shall have ... separate industrial wash sink"); R-06 (plumbing drawing showing fixture locations); Decomposition OBJ-001, OBJ-004.

---

## Principles

### 1. Fixtures Are the End of the Plumbing System — Coordinate Early with Upstream Deliverables

This deliverable is the downstream terminus of the supply and drainage system. The cistern (DEL-014-01), septic system (DEL-014-02), and floor drain rough-in (DEL-014-04) are all upstream prerequisites. Fixture installation sequencing must be planned around structure, interior fit-out, and upstream plumbing completion. Any delay in DEL-014-01 supply pressurization will block final fixture testing.

Source: _DEPENDENCIES.md; Decomposition PKG-014 package structure.

### 2. Conceptual Drawing Is Authoritative for Location Intent Only — IFC Drawings Govern

The conceptual plumbing drawing (R-06) establishes the intent and approximate locations of the water tap / pressure washer reel and the industrial wash station. This is a design-build project; the Plumbing Engineer (PKG-006) must produce IFC drawings that translate conceptual intent into buildable detail. The Plumbing Fixture Schedule (DEL-006-06) will be the authoritative source for fixture type, model, and rough-in dimensions. Do not procure or install fixtures ahead of IFC drawing approval.

Source: R-01 §3.3.2 (IFC drawings signed/stamped by P.Eng.); Decomposition PKG-006.

### 3. Industrial Context Drives Fixture Selection

This is a landfill maintenance shop — not a commercial or residential facility. Fixtures must be selected for durability under heavy-use, industrial conditions: robust mounting, resistance to impact and contamination, and compatibility with the pressure and flow characteristics of the cistern pump system (100 LPM minimum, R-01 §3.4). ASSUMPTION: stainless steel or equivalent heavy-duty materials are appropriate for the wash station; hose-bib type taps with lockable or self-closing features may be appropriate for the water taps in the shop area.

Source: R-01 §3.1, §3.4; R-06; ASSUMPTION.

### 4. Pressure Washer Reel Is an Interface Fixture Requiring Electrical Coordination

The pressure washer reel is a plumbing fixture that also depends on an electrical supply circuit (70A, per Decomposition SOW-0063/DEL-015-04). The Plumbing Contractor is responsible for the water-side connection only. The electrical circuit stub-out must be provided by the Electrical Contractor (PKG-015) before the pressure washer unit can be energized. Both contractors must coordinate rough-in timing and physical placement to avoid conflicts. This interface should be flagged on the coordination schedule.

Source: Decomposition SOW-0049, SOW-0063; _DEPENDENCIES.md.

### 5. Washroom Plumbing Is Out of Scope for DEL-014-06

The washroom and its plumbing fixtures (toilet, urinal, basin) are addressed under the Existing Building Renovation (PKG-017) and the washroom design. The water tap shown near the utility room/washroom area in R-06 is a service tap in that zone -- not a washroom fixture. This distinction must be communicated consistently: Datasheet now identifies this fixture as "Water Tap (standalone service tap)" and all documents should refer to it accordingly to prevent confusion during installation about which contractor installs which tap (E-001).

Source: R-06 (distinguishes service tap from washroom); Decomposition PKG-014 vs. PKG-017.

### 6. ASSUMPTION-Typed Requirements Are Treated as Provisionally Binding (F-001)

Multiple requirements in the Specification are typed as "ASSUMPTION" (e.g., REQ-014-06-004, -005, -006, -013, -021, -032, -033, -034). These assumptions are not arbitrary: they are inferred from the industrial maintenance shop context, cistern-fed water source configuration, and standard plumbing practice for facilities of this type. They are treated as operative and provisionally binding until the authoritative design source (DEL-006-06 Fixture Schedule and IFC drawings) confirms or overrides them.

**Rationale:** In a design-build project, detailed specifications do not yet exist at the planning stage. Treating reasonable assumptions as non-operative (optional) risks scope gaps being discovered late. Treating them as binding-without-qualification risks over-specifying beyond contract intent. The middle path -- provisionally binding pending design confirmation -- preserves scope coverage while allowing design flexibility. If an assumption is later found not to apply, the affected requirement should be revised and downstream documents (Procedure, Datasheet) updated accordingly.

**Risk if overturned:** If assumptions about industrial-grade fixtures (REQ-014-06-004, -034) are overturned, fixture procurement and installation steps would need revision. If the hot water assumption (REQ-014-06-032) is overturned, the industrial wash station design and commissioning criteria change. See CONF-014-06-01.

Source: Specification.md Requirements section; _CONTEXT.md (design-build context).

---

## Considerations

### Design-Build Context

This is a design-build project. The fixture types, model numbers, and precise rough-in dimensions do not yet exist at the time of initial planning. The Plumbing Fixture Schedule (DEL-006-06) will be produced by the Plumbing Engineer and submitted with IFC drawings for County approval. The Plumbing Contractor should participate in the preliminary design review (DEL-006-01) to flag installation constraints and preferred equipment.

### Hot Water Supply

The RFP and conceptual drawings do not specify a hot water source for the industrial wash station or water taps. ASSUMPTION: a domestic hot water heater or point-of-use heater will be required at the industrial wash station at minimum, as a handwashing facility without hot water would likely not meet Alberta Safety Code requirements for a workplace facility. This is an open design question that must be resolved during the preliminary plumbing design phase. See Conflict Table below.

### Cistern-Fed System Pressure Characteristics

Water supply in this facility originates from a cistern (not a municipal water main). The pump is rated at minimum 100 LPM at a 2.5" fill connection (R-01 §3.4; SOW-0042). System pressure at fixture outlets will depend on pump selection, pipe sizing, and pressure regulation -- all to be established by the Plumbing Engineer in the IFC design. The pressure washer reel will have minimum pressure requirements; these must be coordinated with the pump and distribution system design (DEL-014-01).

**Expected system pressure range at fixture outlets (B-004):** TBD. The cistern pump specification (100 LPM at 2.5" fill, R-01 §3.4) establishes the supply-side capacity, but delivered pressure at fixture outlets depends on pipe sizing, elevation head, friction losses, and pressure regulation -- all to be determined during IFC design by the Plumbing Engineer. Fixture selection must account for the cistern-fed pressure profile, which may differ significantly from municipal supply pressure (typically 40-80 psi). The Plumbing Engineer should provide an estimated pressure range at fixture outlets as part of the preliminary design (DEL-006-01) to inform fixture selection adequacy. Source: R-01 §3.4; Decomposition SOW-0042.

### Point-of-Use Water Heater Installation (D-002)

If a point-of-use water heater is required for the industrial wash station (pending CONF-014-06-01 resolution), the following workflow considerations apply:

- **Scope responsibility:** The water heater is a plumbing fixture under DEL-014-06 scope (Plumbing Contractor). However, the electrical supply connection for the heater unit requires coordination with PKG-015 (Electrical Contractor), similar to the pressure washer reel electrical interface.
- **Electrical coordination:** A dedicated electrical circuit for the point-of-use heater must be identified in the IFC electrical drawings. The Plumbing Contractor should flag this requirement during the preliminary design review (DEL-006-01, Step 1) so the Electrical Contractor can plan the circuit.
- **Location planning:** The heater should be located as close to the industrial wash station as practicable to minimize hot water delivery time and heat loss. Location must be coordinated with IFC plumbing and electrical drawings.
- **Design decision pathway:** The decision on heater type (tankless electric, small tank, etc.) and capacity should be made by the Plumbing Engineer during preliminary design and documented in DEL-006-06.

Source: Procedure.md Step 5c; Guidance CONF-014-06-01; ASSUMPTION.

### Freeze Protection

All fixtures are interior to the heated building. ASSUMPTION: freeze protection of fixture supply lines is not a primary concern provided building heating systems (PKG-013) are operational. Lines serving exterior-connected features (bulk water fill, DEL-014-03) are a separate concern handled in that deliverable.

### Contingency for Cistern Unavailability During Fixture Testing (E-002)

Procedure Steps 6 (pressure test) and 8 (commissioning support) require pressurized water from the cistern distribution system (DEL-014-01). If DEL-014-01 is delayed or the cistern system is not pressurized at the time of fixture installation completion, the Plumbing Contractor and Project Manager should plan a contingency for fixture leak testing. Options may include:

- **Temporary water source:** Connect a temporary pressurized water supply (e.g., water truck or portable pump) to the distribution system stub-outs for testing purposes only.
- **Phased testing:** Perform visual and mechanical checks (mounting, connection tightness, drain flow with gravity fill) at installation completion, and defer pressurized leak testing until DEL-014-01 is operational.
- **Schedule mitigation:** Coordinate installation timing with the DEL-014-01 schedule to ensure the cistern system is pressurized before fixture final connections are made.

This is a common construction sequencing risk for projects with non-municipal water sources. The contingency approach should be discussed during the preliminary design review (Step 1) and documented in the project execution plan.

Source: Procedure.md Steps 6, 8; _DEPENDENCIES.md (DEL-014-01 upstream); ASSUMPTION.

### Commissioning Integration

DEL-014-06 fixtures must be operational and leak-free before building systems commissioning (PKG-020, DEL-020-01) can be completed. The commissioning agent should include a fixture operational test (flow, drain, no leaks) in the commissioning checklist.

---

## Trade-offs

| Trade-off | Option A | Option B | Preferred / Notes |
|---|---|---|---|
| Industrial wash station fixture selection | Standard commercial-grade stainless steel utility sink | Industrial-spec stainless with integrated backsplash, heavy-duty drain | ASSUMPTION: Option B preferred for landfill maintenance context; final selection per DEL-006-06 |
| Water tap type | Standard hose bib | Frost-free hose bib | ASSUMPTION: standard interior hose bib acceptable given heated building; frost-free not required for interior locations |
| Pressure washer reel mounting | Wall-mounted retractable reel | Ceiling-mounted retractable reel | TBD — dependent on structural provisions (PKG-011) and final IFC drawing; ceiling height is 35' which may favor wall mounting |

---

## Examples

No project-specific examples are available from the accessible sources. The conceptual plumbing drawing (R-06) provides layout intent but does not include fixture specifications or model references.

ASSUMPTION: Typical industrial maintenance facility practice would use:
- Stainless steel utility sinks (e.g., single- or double-bowl, 16-gauge minimum) for wash stations in shop environments.
- Retractable hose reels for pressure washer connections mounted at approximately 1.5–2.0m height on exterior walls.
- Heavy-duty hose-bib taps with removable handles in shop areas.

These are ASSUMPTIONS only. Authoritative fixture specifications shall come from DEL-006-06.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-014-06-01 | Hot water supply for wash station not specified in any source document. Alberta workplace codes may require hot water at a handwashing facility; this would require a water heater not currently identified in the plumbing scope. | R-01 §3.1 (specifies "separate industrial wash sink" without specifying hot/cold) | Alberta Safety Codes / Plumbing Code (not directly accessible; ASSUMPTION of applicable requirement) | Specification REQ-014-06-032; Procedure Step 3 (procurement) | Plumbing Engineer to resolve during preliminary design (DEL-006-01); hot water source to be declared in IFC drawings | TBD |
| CONF-014-06-02 | Pressure washer unit supply and installation: the plumbing drawing (R-06) shows a "Water Tap & Pressure Washer Reel" as a single fixture point, but it is unclear whether the pressure washer unit itself is in scope for this deliverable or is Owner-furnished equipment. The 70A electrical circuit (SOW-0063) is in scope for PKG-015, suggesting the washer unit may be Owner-supplied. | R-06 (shows fixture point as part of plumbing drawing) | Decomposition SOW-0049 ("Install water taps and pressure washer reel(s)") — reel is in scope; pressure washer unit ownership unclear | Specification REQ-014-06-020 to -023; Procedure Steps 3 and 5 | Treat the retractable reel and water supply connection as Contractor-supplied per SOW-0049; treat pressure washer machine as TBD pending Owner clarification | TBD |
| CONF-014-06-03 | Scope boundary for water tap near washroom/utility room: Guidance Principle 5 states this is a "service tap in that zone -- not a washroom fixture," but Datasheet previously described it by proximity to the washroom without this distinction (E-001). Datasheet now updated to "Water Tap (standalone service tap)" -- confirm this scope boundary is correct and consistent with R-06 intent. | Guidance.md Principles > 5 | Datasheet.md Fixture Inventory (Water Tap standalone row) | Datasheet Fixture Inventory; Specification Scope; Procedure Step 5a | Project Manager to confirm scope boundary between DEL-014-06 service tap and PKG-017 washroom fixtures (PROPOSAL) | TBD |
