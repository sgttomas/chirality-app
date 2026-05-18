# Guidance — DEL-006-05 Septic System Details

---

## Purpose

This deliverable exists to provide the complete engineered drawing set for the septic holding tank system serving the New North Shop Addition at the West Dried Meat Lake Regional Landfill. The septic system is a fundamental infrastructure element at a rural site with no municipal sewer connection. Without a code-compliant, engineered septic system, the building cannot receive Safety Code permits or achieve operational readiness.

The drawing set produced here directly enables:
- Safety Code permit application for the private sewage system (DEL-009-03) (Source: SOW-0007; RFP §3.3.2)
- Construction by the Plumbing Contractor (DEL-014-02) (Source: SOW-0043)
- Commissioning confirmation that all mechanical and plumbing systems are operational (DEL-020-01) (Source: SOW-0090; OBJ-004)

This deliverable supports OBJ-001 (code-compliant, fully functional facility), OBJ-003 (complete P.Eng.-stamped IFC documentation), and OBJ-004 (install and commission all plumbing and water systems to operational readiness). (Source: Decomposition §7, PKG-006 row for DEL-006-05)

---

## Principles

**1. Holding tank, not a treatment system.**
The RFP specifies a 2,000 US gallon "septic holding tank" — not a septic field or treatment system. (Source: RFP §3.4) This distinction is significant: a holding tank collects sewage for periodic pump-out rather than dispersing treated effluent into the soil. This is appropriate for a landfill site where ground contamination risk is a governing concern. The Plumbing Engineer should confirm this interpretation against applicable Alberta Safety Codes requirements and the Authority Having Jurisdiction (AHJ) before finalizing design.

**2. Existing tank removal is in scope; relocation is not.**
Decision D-002 in the project decomposition explicitly resolved that the existing septic tank is to be removed (IN scope, SOW-0043) but that any relocation to another site position is OUT of scope and the County's responsibility (SOW-0205). (Source: Decomposition D-002) The drawing set must clearly annotate which tank is being removed and must not depict or imply a relocation sequence.

**3. Location is established conceptually; IFC must confirm.**
The conceptual plumbing drawing (Appendix B — Plumbing) shows the new septic tank as a symbol on the exterior north side of the New North Shop. (Source: App B — Plumbing) This is a conceptual position. The IFC drawing must establish the precise tank location with full setback dimensions conforming to applicable Alberta Safety Codes requirements. The Plumbing Engineer must coordinate with the civil grading design (PKG-005) to ensure there is no conflict with drainage patterns or driving surfaces.

**4. P.Eng. stamp is mandatory.**
All IFC drawings must be signed and stamped by a P.Eng. licensed in Alberta. (Source: RFP §3.3.2; SOW-0018) This is a non-negotiable project-wide requirement. The Plumbing Engineer of record for DEL-006-05 must be identified and confirmed before IFC issue.

**5. Geotechnical findings inform the design.**
Bedding, backfill, and any subsurface conditions affecting the tank installation are dependent on the geotechnical investigation (DEL-008-01). (Source: SOW-0001; Decomposition PKG-008) The Plumbing Engineer should not finalize tank installation details until the geotech report is available, or should issue IFC with conservative assumptions that are explicitly noted for revision if geotech results differ.

---

## Considerations

### Coordination Dependencies

| Dependency | Nature | Impact on DEL-006-05 |
|---|---|---|
| DEL-008-01 Geotech Report | Subsurface soil conditions | Bedding, backfill, and bearing capacity for tank |
| DEL-006-03 Drain & Vent Plans | Building drain connection to tank | Pipe routing, invert elevations, slope |
| DEL-006-06 Fixture Schedule | Fixture unit count | Confirms adequacy of 2,000 US gal tank size |
| PKG-005 Civil Design | Site grading, drainage, driving surfaces | Tank location and pump-out access route |
| PKG-004 Electrical Design | Alarm/level indicator if required | Coordinate any electrical connection requirements |
| DEL-009-03 Safety Code Permits | Permit authority review | Submit drawings to AHJ; may trigger design revisions |

### Pump-Out Access
A holding tank requires regular pump-out by a service vehicle. The drawing set should confirm that a vacuum truck can access the tank fill/vent/cleanout points from the site driveway. ASSUMPTION: the north side of the building per the conceptual drawing is accessible from the site circulation. Confirm with civil grading plan (PKG-005). (Source: ASSUMPTION based on building program context)

### Sizing Rationale
The RFP specifies 2,000 US gallons. ASSUMPTION: this was sized by the Owner based on anticipated occupancy and pump-out frequency. The Plumbing Engineer should verify this is adequate under the applicable Alberta Safety Codes given the fixture unit count from DEL-006-06 and expected occupancy. If the engineer determines a larger tank is required by code, a scope change discussion with the Owner would be required.

**Decision escalation threshold** (Lensing A-005): The Plumbing Engineer should formally escalate to the Owner/Project Manager if any of the following conditions are identified during design:
- The applicable Alberta code or AHJ requires a tank capacity exceeding 2,000 US gallons based on fixture unit count or occupancy calculation;
- The AHJ requires a treatment system (drain field or equivalent) rather than a holding tank;
- Site constraints (setbacks, soil conditions, access) make the specified 2,000 US gallon holding tank infeasible at the designated location.

ASSUMPTION: these escalation thresholds are inferred from standard engineering practice; the specific contractual mechanism for scope changes is governed by CCDC 14-2013 (RFP §2.7).

### Existing Tank
The existing septic tank location is not explicitly shown on the conceptual drawings accessible in the sources. Its precise location should be confirmed during site investigation. Removal scope must include disconnection, pumping out of contents, and disposal in accordance with applicable Alberta environmental regulations. ASSUMPTION: the Plumbing Engineer and Contractor will coordinate existing tank removal with applicable environmental requirements; specific environmental regulations are TBD.

### Anticipated Artifacts Reconciliation (Lensing B-004)

The `_CONTEXT.md` anticipated artifacts list includes items that are **not applicable** to the holding-tank-only scope established by RFP §3.4:

| _CONTEXT.md Artifact | Applicability to DEL-006-05 |
|---|---|
| Septic tank plan and section details | **Applicable** — core deliverable |
| Drain field layout and design | **Not applicable** — holding tank has no drain field |
| Soil absorption system details | **Not applicable** — holding tank does not use soil absorption |
| Distribution box and manifold details | **Not applicable** — holding tank has no distribution system |
| Pump station details (if applicable) | **Not applicable** unless pump-out infrastructure requires one; TBD |
| Electrical and control system diagrams | **TBD** — alarm/level indicator may be required (coordinate with PKG-004) |
| Site plan showing system location and clearances | **Applicable** — core deliverable |
| Installation notes and soil testing references | **Applicable** — core deliverable |

This discrepancy between the anticipated artifacts list and the actual holding-tank scope should be resolved by the Project Manager / Plumbing Engineer. The production documents (Specification, Datasheet, Procedure) are drafted to the holding-tank-only scope per RFP §3.4. If the AHJ or Owner requires a treatment/drain-field system, this would constitute a scope change.

### Lifecycle and Operating Cost Considerations (Lensing D-003)

TBD: No lifecycle or operating cost information is present in the accessible sources. For a holding tank requiring periodic pump-out at a rural site, the following are material value considerations that the Owner may wish to evaluate:

- **Pump-out frequency estimate:** TBD — dependent on fixture unit count (DEL-006-06), building occupancy patterns, and tank capacity. ASSUMPTION: a maintenance shop with intermittent occupancy may have lower sewage volumes than a continuously occupied building.
- **Annual operating cost implication:** TBD — dependent on pump-out frequency and local service provider rates.
- **Whether lifecycle cost was factored into the Owner's decision to specify a holding tank** (vs. a treatment system): TBD — not documented in accessible sources.

The Plumbing Engineer or Owner should confirm whether these lifecycle considerations require documentation in the deliverable or are addressed separately in the project's operational planning.

---

## Trade-offs

| Trade-off | Option A | Option B | Proposed Direction | Source |
|---|---|---|---|---|
| Tank material | Precast concrete | Polyethylene/fibreglass | TBD — confirm with AHJ and manufacturer availability in region | ASSUMPTION |
| Tank location (final) | Exactly per conceptual drawing (north exterior) | Adjusted to optimize pump-out access or setbacks | Plumbing Engineer to confirm at IFC; must comply with setback requirements | App B (Plumbing); ASSUMPTION |
| Sizing confirmation | Accept 2,000 US gal as specified | Engineer-verify against fixture unit count | Engineer must verify; raise flag if code requires larger | RFP §3.4; ASSUMPTION |

---

## Examples

No project-specific examples are available in the accessible sources. General industry practice for rural Alberta holding tank installations is referenced as context only (ASSUMPTION); specific examples are TBD.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-001 | RFP §3.4 states "2,000 US Gallon Septic holding tank. (potentially removal and relocate existing septic tank)" — parenthetical suggests relocation may be in scope. Decomposition D-002 explicitly resolves this as removal IN, relocation OUT (SOW-0205 assigns relocation to County). **This is the only identified conflict between primary sources.** All four production documents currently follow the Decomposition D-002 interpretation. Human ruling required to confirm this resolution is authoritative. (Lensing D-001) | RFP §3.4 (parenthetical) | Decomposition D-002; SOW-0205 | Specification REQ-002 and Excluded list; Datasheet — Existing tank disposition; Procedure Step 1; Guidance Principle 2 | Decomposition D-002 (explicit decision record) (PROPOSAL) | TBD |
