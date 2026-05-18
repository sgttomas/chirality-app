# Guidance — DEL-006-08 Plumbing Specification

---

## Purpose

DEL-006-08 (Plumbing Specification) exists to translate the plumbing intent embedded in the RFP and conceptual drawings into a normative, enforceable document that governs:

1. **Design quality** — What the Plumbing Engineer must specify to satisfy the County's operational program.
2. **Construction quality** — The standards, materials, and workmanship PKG-014 (Plumbing & Water Systems Installation) must meet.
3. **Regulatory compliance** — Alignment with Alberta Safety Codes and all applicable Alberta building codes.

The RFP describes a rural, off-grid industrial maintenance facility. The plumbing systems are therefore not connected to municipal water or sewer — they rely on a cistern for water supply and a septic holding tank for waste. This self-contained character is the dominant design context for the entire specification.

This deliverable also directly supports:
- **OBJ-003** — Complete, P.Eng.-stamped IFC design documentation across all disciplines before construction begins, fully coordinated across disciplines. (Source: Decomposition §5)
- **OBJ-004** — Install and commission all mechanical, plumbing, and water storage systems to operational readiness, including the 50,000L cistern, septic system, wash bay drainage, and bulk water fill. (Source: Decomposition §5)

---

## Principles

### Off-Grid Water and Waste

The building is a rural landfill maintenance facility with no municipal water or sewer connection indicated in the RFP or conceptual drawings. (Source: RFP §3.4 (R-01); App B–Plumbing (R-06).) This means:

- The cistern is the sole water supply. All service demands (pressure washing, wash station, washroom, laundry, emergency shower) must be sized against cistern capacity and pump throughput.
- The septic holding tank is the sole waste destination for sanitary drainage. The specification must address emptying/pumping frequency provisions relative to anticipated use.
- Industrial drainage (floor drains, sump drains, wash bay drainage to mud sump) may not co-mingle with sanitary waste — drainage routing and disposal destinations must be explicitly specified. ASSUMPTION: industrial floor drain destination is separate from the sanitary septic tank; the Plumbing Engineer must confirm and specify.

### Cistern-Centric System Design

The 50,000 L cistern and 100 LPM pump are the heart of the water supply system. (Source: RFP §3.4 (R-01).) Key design considerations:

- **Cistern sizing adequacy:** Storage volume should be sized against daily/weekly operational demands including pressure washing, wash bay operations, cistern filling turnaround, and emergency shower reserve. ASSUMPTION: 50,000 L represents the Owner's minimum; the Plumbing Engineer should validate adequacy for the full operational demand profile. The Plumbing Engineer should reference or produce a demand analysis (see DEL-006-07 Calculation Package) documenting whether 50,000 L meets full operational demand including: pressure washing, wash bay, washroom, laundry, emergency shower reserve, and refill turnaround time. If 50,000 L is insufficient, this should be flagged to the Owner before final design. [Enrichment: F-003]
- The 2.5-inch fill connection must be coordinated with the bulk water fill system (external fill pump) — both connect to the cistern. (Source: RFP §3.4 (R-01).)
- **Simultaneous demand scenarios:** Pump selection should account for simultaneous demand scenarios (e.g., pressure washer and wash station operating concurrently). ASSUMPTION: simultaneous demand analysis to be confirmed in DEL-006-07 Calculation Package. The Plumbing Engineer should document expected concurrent water demands and bounding scenarios — for example, pressure washer + wash station + washroom in simultaneous operation — and demonstrate that pump sizing addresses peak simultaneous demand. This analysis should be recorded in DEL-006-07 and the results referenced in the specification. [Enrichment: X-001]

### Industrial-Grade Drainage

The maintenance shop services heavy landfill equipment (motor scraper class). Drainage must be designed for:

- High-volume, high-solids wash water from the wash bay (mud, debris from equipment clean-out).
- The exterior mud sump allows excavator access for clean-out — this is an unusual but explicitly required feature. (Source: RFP §3.4 (R-01); App B–Plumbing (R-06).) The sump must be sized and positioned to permit excavator bucket access.
- **Freeze protection for drain traps:** Floor drain traps must be suitable for an Alberta climate (freeze protection in an unheated or intermittently heated environment). The Plumbing Engineer shall evaluate and recommend a freeze protection method from among the following options (or equivalent): trap primers, glycol traps, or heated drain bodies. The selection should consider: (a) maintenance burden (trap primers require plumbing connection; glycol traps require periodic refilling), (b) reliability in extended cold periods, (c) coordination with the mechanical/HVAC heating design (PKG-003) to understand which zones are heated vs. unheated. ASSUMPTION: freeze protection measures are required; specific approach TBD at design stage. [Enrichment: A-004]

### Coordinated Disciplines

The plumbing design must interface with:

- **Structural (PKG-002):** Cistern support structure, sump pit construction, floor penetrations for drains, roof penetrations for plumbing vent system.
- **Mechanical/HVAC (PKG-003):** The forced-air makeup system and heating system affect whether plumbing in unheated zones (e.g., near exterior walls) requires freeze protection measures. Vent system routing must be coordinated to avoid conflicts with HVAC ventilation and exhaust systems.
- **Electrical (PKG-004):** Pump motor power circuits; emergency shower alarm (if required by Safety Codes); bulk fill pump power; hot water heater power (if electric).
- **Civil (PKG-005):** Mud sump location relative to site grading; exterior drainage away from sump.
- **Architecture (PKG-001):** Washroom layout, locker/change room layout, fixture locations, drain rough-in coordination.

### P.Eng. Stamp Requirement

All IFC plumbing drawings must be signed and stamped by a P.Eng. licensed in Alberta. (Source: RFP §3.3.2 (R-01); SOW-0018.) The specification document itself does not require a stamp, but the associated IFC drawing set (DEL-006-02 through DEL-006-05) does. The specification must be internally consistent with those drawings.

---

## Considerations

### Regulatory Framework (Alberta)

The applicable regulatory framework for plumbing in Alberta is the Alberta Safety Codes Act and its associated Safety Codes (including the Plumbing Code, which adopts and amends the National Plumbing Code of Canada). ASSUMPTION: The specific edition in effect at the time of permit application governs; the Plumbing Engineer must confirm the current adopted edition. No direct access to the Safety Code text was available; no clause-level requirements are asserted here.

### Septic Holding Tank vs. Treatment System

The RFP specifies a 2,000 US gallon septic "holding tank" — not a treatment system (e.g., no mention of a field or treatment unit). (Source: RFP §3.4 (R-01).) A holding tank requires regular pumping. The Plumbing Engineer should:

- **Confirm regulatory permissibility:** Confirm that a holding tank (vs. a septic field or treatment system) is permissible under Alberta Environmental Protection and Enhancement Act / Safety Code requirements at this specific site location (SW 14–44–21–W4, near Ferintosh). ASSUMPTION: holding tank is permissible; the County has indicated this as the intended solution in the RFP. However, absolute compliance requires documented confirmation from the Plumbing Engineer that the chosen waste disposal method is legally permissible at this site under provincial regulations. This confirmation should be recorded and referenced in the specification. [Enrichment: F-001]
- Specify pumping access, manhole locations, and overflow provisions.
- Consider whether the existing septic infrastructure (being removed) provided any field or treatment capacity that must be accounted for in the replacement design.

### Emergency Shower Compliance

Emergency showers at industrial facilities in Alberta must comply with applicable Safety Code requirements. ASSUMPTION: ANSI Z358.1 or an equivalent provincial standard applies; the Plumbing Engineer must confirm the applicable Alberta Safety Code citation. Key design considerations include:

- Water temperature range for tepid water delivery (typically 16–38°C per ANSI Z358.1 — ASSUMPTION: confirm under applicable Alberta standard).
- Flow rate and duration requirements.
- Location within 10 seconds of reach from hazard area (ASSUMPTION: per typical industrial safety standards; confirm under applicable Alberta code).
- Annual testing requirements to be included in the specification's testing section.

### Laundry Services

The locker/change room is specified to include laundry services. (Source: RFP §3.4 (R-01); SOW-0073.) This introduces:

- Hot water demand (if hot water is provided from cistern system or a local water heater). Hot water source TBD — not explicitly specified in sources. ASSUMPTION: a local water heater is likely required; type and location TBD.
- Drain connection from laundry equipment to the sanitary system.
- ASSUMPTION: Laundry wastewater routes to the septic holding tank (sanitary). Confirm at design stage.

### Water Treatment / Conditioning

The _CONTEXT.md anticipated artifacts include "Water treatment and conditioning specifications." No explicit water treatment requirement appears in the RFP or conceptual drawings for the new building. ASSUMPTION: Water quality at the site (from bulk delivery to cistern) may not require treatment; however, the Plumbing Engineer should assess whether filtration, UV treatment, or pressure regulation is appropriate for the anticipated uses (pressure washing, wash station, washroom). If not required, this section may be omitted with a documented rationale.

### Plumbing Vent System

Plumbing vent systems are required by the National Plumbing Code of Canada for all drainage installations. Although no explicit reference to venting appears in the RFP or conceptual drawings, this is a mandatory code-required element. The Plumbing Engineer shall design the vent system in accordance with the adopted NPC edition and coordinate roof penetrations with Structural (PKG-002) and routing with Mechanical/HVAC (PKG-003). ASSUMPTION: venting is a code requirement; specific design to be determined during detailed design. [Enrichment: C-002]

---

## Trade-offs

| Trade-off | Option A | Option B | Proposed Direction | Basis |
|-----------|----------|----------|-------------------|-------|
| Cistern material | Polyethylene (PE) tank | Reinforced concrete vault | ASSUMPTION: PE is common for above-grade cisterns; concrete may be preferred for below-grade or higher-load applications. Decision to Plumbing Engineer in coordination with Structural Engineer (PKG-002). | Not specified in sources |
| Drain routing — floor drains | Gravity to septic tank | Gravity to separate collection with pump-out | ASSUMPTION: Industrial drains likely require separate collection from sanitary (environmental considerations); Plumbing Engineer to confirm and specify. See CON-PLB-001 below. | Not specified in sources |
| Freeze protection — drainage | Trap primers / glycol traps | Heated drain bodies | ASSUMPTION: Method TBD; Alberta climate requires attention to this. Plumbing Engineer to evaluate each option per Guidance > Industrial-Grade Drainage and specify. | Not specified in sources — [Enrichment: A-004] |
| Hot water supply | Centralized tank water heater | Point-of-use heaters | ASSUMPTION: Hot water source not specified in RFP; Plumbing Engineer to determine based on demand profile and system layout. See SPEC-PLB-025. | Not specified in sources |
| Emergency shower water supply | Connected to main cistern/pump system | Dedicated supply (self-contained unit) | ASSUMPTION: Connection to main system is the likely approach; confirm flow rate and temperature compliance per SPEC-PLB-072 criteria. | Not specified in sources |

---

## Examples

No direct examples or precedent projects were accessible in the available source documents. The following contextual notes are drawn from the RFP scope description only:

- The wash bay is explicitly described as serving "large equipment such as a motor scraper." (Source: RFP §3.4 (R-01).) This is unusually large equipment for a wash bay and implies high-flow drainage and a large mud sump.
- The pressure washer reel shown on App B–Plumbing (R-06) is a common feature in municipal/landfill maintenance shops and implies at least one 3/4-inch or 1-inch service water connection at that reel location. (ASSUMPTION: connection size TBD at design stage.)

---

## Conflict Table (for human ruling)

The following items are open interpretation questions that should be addressed during detailed design and resolved before IFC issue.

### Conflict Resolution Process

When a CON-PLB item requires a human ruling, the following process shall apply: [Enrichment: E-003]

1. **Escalation:** The Plumbing Engineer raises the item to the PM with a written recommendation (the "Proposed Direction" column below).
2. **Decision authority:** The PM coordinates with the Owner (Camrose County) where the decision involves Owner preference, regulatory interpretation, or cost implications. For purely technical decisions within the Plumbing Engineer's professional scope, the P.Eng. may resolve directly and record the rationale.
3. **Recording:** The Human Ruling column shall be updated with the decision, the date, the deciding authority, and a brief rationale. The corresponding specification requirement(s) in Specification.md shall then be updated to reflect the ruling.
4. **Timeline:** All CON-PLB items should be resolved before preliminary design submission (Procedure Phase 2, Step 2.1) where feasible, and must be resolved before IFC issue (Procedure Phase 3, Step 3.5).

| Item | Question | Source A | Source B | Proposed Direction | Human Ruling |
|------|----------|----------|----------|--------------------|--------------|
| CON-PLB-001 | Routing destination for shop floor drains and sump drains (septic vs. dedicated industrial collection) | RFP §3.4 (R-01) implies drainage to sump/exterior mud sump for wash bay; floor drains in shop bays not explicitly routed | App B–Plumbing (R-06) shows floor drain locations without specifying routing | ASSUMPTION: Wash bay drains to mud sump; shop floor drains to TBD (likely separate from sanitary; Plumbing Engineer to specify). Impact: SPEC-PLB-042, Procedure Step 3.2. | TBD |
| CON-PLB-002 | Hot water provision: source and type not stated anywhere in RFP or conceptual drawings | RFP §3.4 (R-01) / SOW-0073 implies laundry services (hot water demand) | No water heater shown on App B–Plumbing (R-06) | ASSUMPTION: Local water heater(s) required; type and location TBD at design stage. Impact: SPEC-PLB-025, Datasheet Hot Water Supply row. | TBD |
| CON-PLB-003 | Existing septic: "removal and relocation" wording in RFP §3.4 (R-01) vs. decomposition D-002 decision (removal IN, relocation OUT) | RFP §3.4 (R-01): "potentially removal and relocate existing septic tank" | Decomposition D-002: resolved as removal IN, relocation OUT | Follow decomposition D-002 resolution: remove existing septic tank only. Note: this conflict between RFP wording and decomposition resolution must be confirmed with Owner (Camrose County) before specification is finalized, as the RFP language is ambiguous and the decomposition interpretation may not reflect Owner intent. Impact: SPEC-PLB-031, Procedure Step 1.5. | TBD — confirm with Owner — [Enrichment: E-004 — conflict explicitly surfaced for Owner confirmation] |

---

## Pass 3 Enrichment Log

| Lensing Item | Action Taken |
|---|---|
| A-004 | Expanded freeze protection discussion in Industrial-Grade Drainage: added evaluation framework with options, maintenance considerations, and HVAC coordination directive; updated Trade-offs table |
| B-004 | Normalized terminology: "wash sink" / "wash station" standardized to "wash station" throughout |
| C-002 | Added new Considerations subsection for Plumbing Vent System; updated Coordinated Disciplines to reference vent system coordination |
| E-001 | Added (R-01)/(R-06) reference identifiers to source citations throughout for consistency |
| E-003 | Added Conflict Resolution Process section defining escalation, decision authority, recording, and timeline for CON-PLB items |
| E-004 | Strengthened CON-PLB-003: explicitly surfaced that the RFP/decomposition conflict requires Owner confirmation before specification finalization |
| F-001 | Expanded Septic Holding Tank vs. Treatment System: added directive for Plumbing Engineer to confirm regulatory permissibility with documented evidence at specific site location |
| F-003 | Expanded Cistern-Centric System Design: added directive for demand analysis referencing DEL-006-07 and specific demand categories to validate |
| X-001 | Expanded Cistern-Centric System Design: added directive for simultaneous demand scenario documentation with bounding scenarios and pump sizing demonstration |
