# Guidance: DEL-006-06 — Plumbing Fixture Schedule

---

## Purpose

The Plumbing Fixture Schedule exists to enumerate, identify, and technically characterize every plumbing fixture and related appurtenance in the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It serves two distinct downstream consumers:

1. **Procurement and installation teams (PKG-014):** The schedule defines what is to be purchased, procured, and installed. Without it, the plumbing contractor cannot accurately price or execute the work.
2. **Design coordination (PKG-006 and cross-discipline):** The schedule acts as the binding record of fixture identity across all plumbing sub-documents (plans, details, specifications, calculations), and the interface document for architectural, structural, and mechanical coordination.

Within the project objectives, DEL-006-06 directly supports:
- **OBJ-003** — Produce complete, P.Eng.-stamped IFC design documentation. The fixture schedule is a required component of the fully coordinated plumbing design package (SOW-0016).
- **OBJ-004** — Install and commission all plumbing systems to operational readiness. The schedule defines the fixture content that PKG-014 contractors will install.

**ASSUMPTION (PACKAGE_HEURISTIC):** Association with OBJ-003 and OBJ-004 reflects the explicit objective mapping for PKG-006 deliverables in the decomposition (WDMLRL_Decomposition_Claude.md, DEL-006-06 entry). Treated as directionally relevant context.

---

## Principles

### Principle 1: The Schedule is the Single Source of Truth for Fixture Identity

The Fixture Schedule must be internally consistent with all other documents in the plumbing design package. If a floor drain appears on DEL-006-03 (Drain & Vent Plans), the same drain — same tag, same type, same specification — must appear in this schedule. Discrepancies between the schedule and the plans are a coordination failure.

**Source:** RFP §3.3.2 ("Complete final design … must be fully coordinated across … plumbing disciplines"); OBJ-003.

### Principle 2: Industrial Context Drives Fixture Selection Philosophy

This is not a commercial or residential facility. The New North Shop serves heavy equipment maintenance at a regional landfill. Fixtures must be selected for:
- **Durability:** Industrial-grade materials appropriate for shop environments (grease, oil, grit, heavy use)
- **Serviceability:** Fixtures that can be maintained with minimal downtime
- **Function over aesthetics**

The conceptual plumbing drawing (App B-Plumbing) makes the industrial character clear: floor drains are distributed across the main bays, an industrial wash sink and pressure washer reel are provided in the work area, and an emergency shower is positioned near the exterior.

**Source:** RFP §3.1, App B-Plumbing. ASSUMPTION: industrial fixture grade is implied by the building type; specific grade requirements to be confirmed by the Plumbing Engineer.

### Principle 3: Completeness Includes the Renovation Scope

The Old North Shop renovation scope (SOW-0072, SOW-0073, SOW-0074) introduces additional fixture requirements: a renovated washroom, a new urinal, and new locker/change room laundry services. These must be included in the fixture schedule. Omitting the renovation scope would produce an incomplete schedule.

**Source:** RFP §3.4; SOW-0072, SOW-0073, SOW-0074; App B-Plumbing (Old North Shop mezzanine and washroom renovation noted on drawing).

### Principle 4: Emergency Shower is a Safety-Critical Fixture

The emergency shower at the New North Shop is not a routine plumbing fixture. It is a worker safety system. Its specification must comply with applicable emergency shower standards (ASSUMPTION: ANSI/ASSE 1009 or equivalent; location TBD). Its location on the conceptual drawing (App B-Plumbing, labeled "Emergency Shower" near the exterior wall) should be preserved unless a safety analysis by the engineer of record justifies relocation.

**Source:** SOW-0048; App B-Plumbing.

---

## Considerations

### Consideration A: Fixture Count Uncertainty at Conceptual Stage

The Appendix B (Plumbing) conceptual drawing provides schematic fixture locations but is not a detailed design. Several fixture quantities shown are minimum counts. For example, floor drain placement in the main bays may change when the Plumbing Engineer performs hydraulic design and drain sizing. The schedule produced at IFC stage will reflect the final engineered layout.

**Implication for this document set:** Floor drain quantities stated in this document set are based on the conceptual drawing and are labeled as ASSUMPTION where counts are inferred. The IFC schedule will be authoritative.

### Consideration B: Washroom Fixture Scope Split Between New and Existing

The RFP and conceptual drawing establish that:
- The New North Shop includes a washroom area (shown in the floor plan)
- The Old North Shop has an existing washroom below the mezzanine that is being renovated (SOW-0072) and expanded with a urinal (SOW-0074)
- A new locker/change room with laundry services is being added (SOW-0073)

The Fixture Schedule must clearly distinguish between new fixtures in the New North Shop and renovation fixtures in the Old North Shop renovation scope. Both areas are within the PKG-006 design scope.

**Source:** App B-Plumbing; RFP §3.1; SOW-0072, SOW-0073, SOW-0074.

### Consideration C: Cistern and Pump Equipment Scheduling Boundary

The 50,000 L cistern (SOW-0041), the 100 LPM pump (SOW-0042), and bulk water fill (SOW-0044) are plumbing system equipment items. The typical practice in plumbing design is to schedule such equipment items either within the Fixture Schedule or in a separate Equipment Schedule. For this project, the Plumbing Engineer must decide whether these items appear in DEL-006-06 or are handled under DEL-006-04 (Cistern & Pump Details) with appropriate cross-referencing.

**Recommendation (ASSUMPTION):** At minimum, the Fixture Schedule should cross-reference DEL-006-04 for cistern and pump items rather than leaving a gap. Detailed equipment specifications for those items live under DEL-006-04.

### Consideration D: Accessibility Requirements for Industrial Washrooms

Alberta Building Code accessibility requirements apply to washroom facilities. The washroom renovation in the Old North Shop and any new washroom in the New North Shop may require accessible fixture specifications (accessible lavatory height, clearances, grab bar rough-ins). The Plumbing Engineer should verify accessibility requirements for the occupancy classification.

**Source:** ASSUMPTION — Alberta Building Code accessibility provisions (location TBD). RFP §3.3.2 requires adherence to all applicable building codes.

### Consideration E: Fixture Lifecycle and Maintenance Value (Enrichment C-003)

For a rural landfill facility near Ferintosh, Alberta (Camrose County), fixture lifecycle cost and maintenance burden are material to fixture selection. Considerations include:

- **Replacement parts availability:** Industrial fixtures from widely distributed manufacturers are preferable to specialty items with limited supplier networks. The rural location limits access to rapid replacement parts.
- **Industrial-grade warranty expectations:** Fixtures in heavy-use industrial environments should carry warranties appropriate to the use condition. Standard commercial warranties may not cover industrial wear patterns.
- **Long-term cost implications:** Higher initial cost for industrial-grade fixtures may be offset by longer service life, lower maintenance frequency, and reduced downtime. The Plumbing Engineer should consider total cost of ownership, not just procurement cost.

**ASSUMPTION:** These lifecycle considerations are implied by the industrial context (RFP §3.1) and rural location (project at SW 14-44-21-W4). Specific lifecycle cost analysis methodology is TBD. **ProposedAuthority:** Plumbing Engineer / Owner (Camrose County). **HumanRuling:** TBD.

### Consideration F: Cold Climate Implications for Fixture Schedule

Emergency showers may require electrical connections for heat tracing in cold climates (Alberta winters). The Plumbing Engineer and Electrical Engineer (PKG-004) should coordinate on whether the emergency shower requires heat tracing, and if so, the electrical loads must be captured in DEL-004.

**Broader Cold Climate Considerations (Enrichment E-001):** Beyond emergency shower heat tracing, the following cold climate implications affect the fixture schedule and should be addressed by the Plumbing Engineer:

- **Cistern freeze protection:** The 50,000 L cistern (SOW-0041) and associated piping require freeze protection in Alberta winter conditions. The cistern location (interior vs. exterior/buried) and insulation/heating approach affect fixture supply reliability. TBD — to be coordinated with DEL-006-04.
- **Exposed piping freeze protection:** Any piping in unheated or partially heated shop areas (35 ft ceiling height, overhead crane bay) may be subject to freeze risk. Floor drain trap seal maintenance in cold conditions should be considered.
- **Floor drain trap primers:** Floor drains in low-use areas of the shop may experience trap seal evaporation, particularly in heated/dry winter conditions. Trap primers or trap seal primers may be required to maintain drain trap integrity. TBD — Plumbing Engineer to assess whether trap primers should be scheduled for specific floor drain locations.
- **Freeze-protected floor drains:** Floor drains near exterior roll doors or in areas subject to cold drafts may require freeze-protected drain bodies. TBD — Plumbing Engineer to assess based on final layout.

**Source:** ASSUMPTION — climate-related considerations implied by Alberta location (SW 14-44-21-W4) and industrial building type (35 ft structure with roll doors). Specific requirements TBD by Plumbing Engineer and Mechanical Engineer. **ProposedAuthority:** Plumbing Engineer / Mechanical Engineer. **HumanRuling:** TBD.

---

## Trade-offs

### Trade-off 1: Manufacturer Specification vs. Performance Specification

The fixture schedule can specify fixtures by:
- **Named manufacturer and model** — provides certainty but may limit procurement options
- **Performance specification** — defines minimum performance criteria and allows equivalent substitutions

For an industrial shop in a rural location (near Ferintosh, Alberta), supply chain access may be a practical consideration. ASSUMPTION: The Plumbing Engineer should consider specifying "or approved equal" provisions for non-safety-critical fixtures. The emergency shower should be specified by performance standard (ANSI/ASSE or equivalent) given its safety-critical nature.

**Decision Criteria (Enrichment A-005):** The following factors should inform the manufacturer-named vs. performance specification choice for each fixture category. These criteria are TBD pending Plumbing Engineer input:

| Factor | Favors Named Manufacturer | Favors Performance Specification |
|---|---|---|
| Safety criticality | -- | Emergency shower — must meet certified standard regardless of manufacturer |
| Procurement lead time | Shorter if stocked locally | Longer if equivalents must be evaluated |
| Rural supply chain access | Risk if sole-source unavailable | Wider availability from multiple suppliers |
| Warranty / support | Known manufacturer support path | May vary by supplier |
| Cost certainty | Known unit cost | Competitive pricing possible |
| Interchangeability | Replacement parts locked to manufacturer | Standard fittings more interchangeable |

**ASSUMPTION:** These criteria represent general considerations; specific weighting factors TBD by Plumbing Engineer in consultation with project procurement approach. **ProposedAuthority:** Plumbing Engineer / project procurement. **HumanRuling:** TBD.

### Trade-off 2: Fixture Schedule Granularity

A highly detailed schedule (including all piping accessories, cleanouts, and minor fittings) increases completeness but also increases schedule maintenance burden during design development. A leaner schedule focused on primary fixtures is easier to maintain but may miss scope items.

**Guidance:** Include all fixtures identified on the conceptual drawing plus those explicitly called out in the RFP design requirements and SOW items. Cleanouts and minor accessories may be addressed in the Specification (DEL-006-08) rather than the schedule.

**Scope Boundary Clarification (Enrichment X-002):** The boundary between fixtures scheduled in DEL-006-06 and minor fittings/accessories addressed in DEL-006-08 (Plumbing Specification) is currently undefined. The Plumbing Engineer shall define what constitutes "cleanouts and minor accessories" excluded from this schedule. TBD items requiring clarification:
- Cleanout access fittings: in schedule or specification?
- Hose bibbs not shown on conceptual drawing: in schedule or specification?
- Trap primers for floor drains: in schedule or specification?
- Backflow prevention devices: in schedule or specification?

**ASSUMPTION:** Primary fixtures (those with a unique location on the drawing or explicitly named in SOW items) belong in DEL-006-06. Ancillary fittings may be addressed in DEL-006-08. Final boundary TBD. **ProposedAuthority:** Plumbing Engineer. **HumanRuling:** TBD.

---

## Examples

### Fixture Types Expected on This Project

The following fixture types are expected on this project based on the sources reviewed. This is not an exhaustive list; the Plumbing Engineer will confirm during detailed design.

| Category | Examples Expected | Source |
|---|---|---|
| Floor Drains — Shop | Cast iron floor drain with sediment bucket, shop/industrial type | App B-Plumbing; SOW-0046 |
| Sump Drains — Repair Bays | Industrial sump drain / trench drain system | SOW-0045; RFP §3.4 |
| Wash Bay Floor Drain | Heavy-duty floor drain connecting to mud sump system | App B-Plumbing; SOW-0027b |
| Emergency Shower | ANSI-compliant combination shower/eyewash unit (ASSUMPTION) | SOW-0048; App B-Plumbing |
| Water Tap — Service | Industrial hose bibb or service faucet | App B-Plumbing; SOW-0049 |
| Pressure Washer Reel | Hose reel station with water connection | App B-Plumbing; SOW-0049 |
| Industrial Wash Sink | Stainless or cast iron wash sink / trough | SOW-0050; RFP §3.1 |
| Washroom — Toilet (WC) | Flush valve toilet, floor or wall mounted | App B-Plumbing (washroom area); ASSUMPTION |
| Washroom — Lavatory | Wall-hung or counter lavatory | ASSUMPTION |
| Washroom — Urinal | Wall-hung urinal (urinal addition per §3.4) | SOW-0074; RFP §3.4 |
| Laundry — Washer/Dryer Rough-in | Floor drain, hot/cold supply, gas (if applicable) rough-in | SOW-0073; RFP §3.4 |

---

## Conflict Table (for human ruling)

No unresolvable conflicts were identified during Pass 1 + Pass 2 from the available sources. The following items are noted as requiring design decisions rather than conflicts:

| Item | Issue | Source A | Source B | Impacted Sections | PROPOSAL | Human Ruling |
|---|---|---|---|---|---|---|
| C-001 | Cistern/pump equipment scheduling boundary: whether 50,000L cistern and pump are scheduled in DEL-006-06 or DEL-006-04 | _CONTEXT.md (anticipated artifacts) | Decomposition — DEL-006-04 (Cistern & Pump Details exists as separate deliverable) | Datasheet Attributes; Specification REQ-010 | Cross-reference in DEL-006-06; primary scheduling in DEL-006-04 | TBD |
| C-002 | Floor drain quantities: conceptual drawing shows 4–5 floor drains; final count depends on detailed hydraulic design | App B-Plumbing (conceptual) | SOW-0046 ("as shown on plumbing drawing") | Datasheet Attributes; Specification REQ-003 | Use conceptual count as minimum; IFC drawing governs | TBD |
| C-003 | Washroom fixture scope in New North Shop: plan shows "Washroom" area in New North Shop with a drain but no fixture detail; scope of new washroom fixtures unclear | App B-Plumbing (New North Shop — washroom area labeled with drain) | RFP §3.1 ("shop shall have a washroom") | Specification REQ-008; Procedure Step 3; Datasheet Fixture Table | Plumbing Engineer to confirm fixture count for New North Shop washroom during design | TBD |
| C-004 | Eyewash station requirement: is a standalone eyewash required, or is a combination shower/eyewash unit sufficient? (Enrichment C-002) | SOW-0048 (emergency shower) | Guidance Examples ("ANSI-compliant combination shower/eyewash unit — ASSUMPTION") | Specification REQ-005; Guidance Examples table | Plumbing Engineer / safety codes officer to confirm | TBD |
| C-005 | Canonical fixture term: "industrial wash sink" vs. "wash station" vs. "wash sink" — normalization proposed as "industrial wash sink" (Enrichment B-003) | RFP §3.1 ("separate industrial wash sink") | App B-Plumbing (labeled "Wash Station") | All four documents — terminology consistency | Plumbing Engineer to confirm preferred canonical term | TBD |
| C-006 | DEL-006-06 / DEL-006-08 scope boundary: which minor fittings/accessories (cleanouts, trap primers, hose bibbs, backflow preventers) belong in this schedule vs. the plumbing specification? (Enrichment X-002) | Trade-off 2 (this document) | DEL-006-08 Plumbing Specification scope | Specification scope; Datasheet fixture table | Plumbing Engineer to define boundary | TBD |
| C-007 | Building occupancy classification: TBD. Required to determine code-mandated minimum fixture counts and accessibility provisions. (Enrichment C-001) | RFP §3.1 (building use: industrial maintenance shop) | Alberta Building Code (occupancy classification — edition TBD) | Specification Standards, REQ-012, REQ-013; Datasheet Design Conditions | Architect / Plumbing Engineer to confirm | TBD |
