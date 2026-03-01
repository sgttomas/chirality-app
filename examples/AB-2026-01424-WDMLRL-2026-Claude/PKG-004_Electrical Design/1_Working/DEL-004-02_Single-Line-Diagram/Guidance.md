# Guidance — DEL-004-02 Single-Line Diagram

**Document Type:** Guidance (directional)
**Deliverable ID:** DEL-004-02
**Deliverable Name:** Single-Line Diagram
**Package:** PKG-004 Electrical Design
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Responsible Party:** Electrical Engineer
**Last Updated:** 2026-02-26

---

## Purpose

The Single-Line Diagram (SLD) is the foundational power distribution document for the New North Shop electrical system. Its purpose is to:

1. **Communicate the distribution hierarchy** — show how power flows from the utility service entrance through the main distribution panel (MDP), sub-panels, feeders, and branch circuits to all loads.
2. **Serve as the authority document** for panel schedule numbering (DEL-004-06), circuit sizing in the calculation package (DEL-004-08), and the physical routing shown on power distribution plans (DEL-004-03).
3. **Support regulatory approval** — the SLD, stamped by a P.Eng. licensed in Alberta (REQ-SLD-007), is typically reviewed by the Safety Codes Officer as part of the electrical permit inspection process (SOW-0007).
4. **Enable cost estimation, construction scheduling, and procurement** — the SLD allows the electrical contractor (PKG-015) to understand service sizing, panel quantities, and major feeder runs before physical plans are detailed. Early SLD issuance supports construction scheduling by enabling the electrical contractor to identify long-lead items (main switchgear, transformers, sub-panels), sequence rough-in work relative to structural and mechanical trades, and coordinate utility service tie-in timing (SOW-0081) with the overall project schedule. *(Rationale enriched per D-002: confirmed merit application requires connection to scheduling benefit.)*

The New North Shop is an industrial maintenance facility with a demanding electrical load profile: two 5-tonne overhead cranes, high-bay LED lighting, welding-grade 50A/240V receptacles distributed throughout the shop, and three dedicated large-load circuits (40A compressor, 70A fire hose pump, 70A pressure washer). The SLD must reflect this industrial character, which drives service sizing well above a typical commercial building of the same footprint.

**Objective alignment:**
- OBJ-003: The SLD is part of the P.Eng.-stamped IFC documentation set required before construction begins.
- OBJ-005: The SLD defines the distribution architecture that supports commissioning all electrical systems to operational readiness.

*(ASSUMPTION: Objectives OBJ-003 and OBJ-005 are associated with DEL-004-02 by package-grouping heuristic per PKG-004 in the decomposition objective-to-deliverable mapping. Best-effort association — not confirmed at deliverable-ID level.)*

---

## Principles

### 1. SLD as Single Source of Truth for Distribution Hierarchy
The SLD is the canonical document for power distribution topology. All other electrical deliverables (panel schedules, power plans, receptacle plans, calculation package) shall reference and be consistent with the SLD. Discrepancies between the SLD and other documents are to be resolved by returning to the SLD or by formal revision to it — not by silent correction in subordinate documents.
**Source:** Standard electrical engineering practice; REQ-SLD-010.

### 2. Load Inventory First
Before the SLD hierarchy is drawn, the Electrical Engineer should compile a complete load inventory from the conceptual drawing (App B — Electrical) and all other design inputs. The conceptual drawing identifies the load types and locations; the SLD formalizes the distribution grouping. Skipping the inventory step risks missing loads or under-sizing panels.
**Source:** App B (Electrical) — load types and ratings extracted directly from the conceptual drawing.

### 3. Dedicated Circuits for High-Demand Equipment
The RFP and conceptual drawing identify several loads that require dedicated circuits (not shared with lighting or general receptacles): the two 5-tonne cranes, the 40A compressor, the 70A fire hose pump, and the 70A pressure washer. These shall be shown as individually labeled dedicated feeders or branch circuits on the SLD. Grouping them with general-purpose circuits would be incorrect practice for equipment of this class.
**Source:** App B (Electrical); SOW-0059–SOW-0063; standard CEC requirements for motor and dedicated-load circuits (ASSUMPTION: CEC Part I applicable — location TBD).

### 4. Industrial Receptacle Distribution
The shop has a high density of 240V receptacles (20A, 30A, and 50A/240V), which significantly influence panel sizing and sub-panel placement. The Electrical Engineer should consider:
- Grouping 240V receptacles by zone (welding station area, repair bays, wash bay) rather than distributing them across a single overcrowded panel.
- The 50A/240V welding receptacles in the welding station area (App B — Electrical) represent a clustered high-demand zone that may warrant a dedicated sub-panel or motor control section.
- The 30A/240V receptacles near the wash bay are likely associated with the pressure washer and related equipment.
**Source:** App B (Electrical); SOW-0057, SOW-0058; D-009 (50A/240V assumption for welding receptacles).

### 5. Crane Circuit Sizing Depends on Crane Specification
The two 5-tonne overhead cranes are shown on the conceptual drawing (App B — Electrical) with power feeds, but the circuit size is not specified in the source material. The SLD cannot be finalized for crane circuits until the crane manufacturer's electrical specifications are available. The Electrical Engineer should:
- Hold a TBD placeholder for crane circuit ratings on the preliminary SLD.
- Coordinate with the crane supplier (DEL-016-01) and structural engineer (DEL-002-07 crane support details) to confirm motor ratings, locked-rotor current, and duty cycle class before finalizing the IFC SLD.
**Source:** App B (Electrical); SOW-0059; Decomposition §7 DEL-016-01, DEL-002-07.

### 6. Low-Voltage Systems — SLD Notation Only
Security camera wiring (SOW-0064) and antenna wire for 2-way radios (SOW-0065) are low-voltage systems. The SLD is not the primary document for their design (DEL-004-07 Low-Voltage System Plans covers this), but the SLD should note power supply provisions for any systems requiring 120V-class power (e.g., network switches, camera NVRs, radio base stations). If these systems are entirely passive or battery-powered, no SLD entry is needed — this is TBD pending low-voltage system design.
**Source:** App B (Electrical); SOW-0064, SOW-0065; Decomposition §7 DEL-004-07.

---

## Considerations

### Voltage System Selection (ASSUMPTION)
The appropriate system voltage (e.g., 120/208V three-phase wye vs. 347/600V three-phase wye with step-down transformers) has not been specified in the source documents beyond the requirement for three-phase power (SOW-0051). In Alberta industrial and agricultural settings, 347/600V three-phase wye is common for large-load facilities, with step-down transformers for 120V and 240V loads. However, the service authority's available voltage and the crane/HVAC equipment voltage requirements must both be confirmed. This decision has a significant downstream impact on:
- Main panel bus voltage rating
- Lighting fixture driver compatibility (347V vs. 120V drivers for high-bay LEDs)
- Receptacle circuit design (step-down transformer required for 120V if 600V system adopted)
**Recommendation:** Electrical Engineer to confirm system voltage with the local utility during preliminary design (DEL-004-01) before the SLD is drafted.
**Source:** ASSUMPTION — not specified in RFP or App B (Electrical). Location TBD in CEC.

### Service Sizing
The aggregated demand of the New North Shop is substantial. Key contributors:
- 20 high-bay LED fixtures at 150W each = 3,000W lighting load (main shop alone)
- 6 additional fixtures (wash bay) + office/utility/parts room fixtures
- 6 ceiling fans (rating TBD)
- Crane loads — potentially the dominant demand factor; 5-tonne cranes with hoist and travel motors can draw significant current, particularly at start
- 40A + 70A + 70A dedicated circuits = 180A of dedicated equipment at 240V
- Welding receptacles — multiple 50A/240V; diversity factor must be applied but demand is high
The Electrical Engineer shall size the main service based on a formal demand/load calculation (DEL-004-08). Early coordination with the utility is recommended as the calculated demand may require upgrading the incoming service capacity relative to any existing infrastructure.
**Source:** App B (Electrical); SOW-0051; load values from conceptual drawing.

### Coordination with Mechanical Electrical Loads
The mechanical systems (forced-air makeup air unit, high-recovery heating, exhaust systems) will have electrical connections that must appear somewhere in the electrical distribution. The SLD should include provisions for mechanical equipment feeds, sized in coordination with DEL-003-05 (Mechanical Equipment Schedule). If mechanical equipment electrical data is not yet available at SLD draft stage, placeholders with TBD ratings should be included.
**Source:** SOW-0013, SOW-0035–SOW-0039; Decomposition PKG-003.

### Emergency and Standby Power Provisions (TBD)
TBD — The source documents do not address emergency or standby power requirements for the New North Shop. However, an industrial maintenance facility may require emergency egress lighting at minimum (per Alberta Building Code occupancy requirements), and potentially backup power for the fire alarm panel (if installed) or other life-safety systems. The Electrical Engineer should determine:
- Whether emergency egress lighting is required by the Alberta Building Code for the building occupancy classification.
- Whether any fire alarm or detection system requires backup power.
- Whether any critical operational loads (e.g., sump pumps, heating in extreme cold) warrant standby power provisions.
If emergency or standby power is required, the SLD should include these circuits and their power source (battery backup, generator, or dual-feed arrangement).
**Source:** ASSUMPTION: Alberta Building Code likely requires emergency egress lighting for industrial occupancies (location TBD); CEC requirements for emergency circuits (location TBD). No emergency/standby power mentioned in RFP, App B (Electrical), or decomposition. *(Added per X-001: total directional coverage gap -- emergency/standby power not addressed in any document.)*

### Wash Bay Electrical Requirements
The wash bay has specific electrical considerations:
- 2 rows of 3 high-bay lights (SOW-0053) — lighting circuit
- Multiple 20A/240V and 30A/240V receptacles visible in the conceptual layout near the wash bay
- 70A pressure washer dedicated circuit (SOW-0063)
- Proximity to water — all electrical in the wash bay must meet wet-location installation requirements per CEC (ASSUMPTION: CEC applicable — location TBD)
The SLD should identify wash bay circuits and the Electrical Engineer should note wet-location designations on the distribution plans.
**Source:** App B (Electrical); SOW-0053, SOW-0063; ASSUMPTION re: CEC wet-location.

### Spare Capacity and Future Expansion Provisions
The source documents do not discuss future expansion or spare capacity requirements for the electrical system. However, for an industrial maintenance facility with a 2-year warranty period and an expected service life well beyond the project completion date, it is standard engineering practice to include provisions for future flexibility in the SLD:
- **Spare breaker spaces** — Panels should include spare breaker spaces (typically 15-25% of panel capacity, per common engineering practice) to accommodate future loads without panel replacement.
- **Main service sizing margin** — The main service ampacity should consider a reasonable growth factor beyond the calculated demand, especially given that the facility may acquire additional equipment over time.
- **Spare conduit provisions** — The SLD should note where spare conduits or pull boxes are recommended for future circuit additions, particularly for the welding station area and crane bays where operational needs may evolve.
- **Panel bus rating vs. main breaker** — Consider specifying panel bus ratings above the initial main breaker size to allow future breaker upgrades without panel replacement.
The Electrical Engineer should discuss spare capacity expectations with the Owner (Camrose County) during preliminary design.
**Source:** ASSUMPTION: standard engineering practice for industrial facilities. No spare capacity or future expansion requirement stated in RFP, App B (Electrical), or decomposition. *(Added per E-001: commanding strategic mastery gap -- no discussion of future flexibility in any document.)*

---

## Trade-offs

| Trade-off | Option A | Option B | Considerations |
|---|---|---|---|
| System voltage | 120/208V three-phase wye | 347/600V three-phase wye + step-down transformers | 347/600V is more efficient for large loads and common in Alberta industrial facilities; 120/208V simpler for receptacle distribution. Crane and HVAC equipment compatibility must drive decision. |
| Panel topology | Single MDP with all circuits | MDP + zoned sub-panels (e.g., shop sub-panel, wash bay sub-panel, office/parts/utility sub-panel) | Sub-panels add cost but reduce voltage drop over long runs in a 130' × 100' building; likely preferable given industrial load density. ASSUMPTION. **Decision criteria:** Favor zoned sub-panels when (a) voltage drop calculations (per CEC) indicate feeder runs from a single MDP exceed allowable limits for the building's longest circuits, (b) total branch circuit count at MDP would exceed practical panel capacity (typically 42-84 poles), or (c) discrete functional zones (wash bay, welding station, office) have distinct load profiles that benefit from local protection. Favor single MDP when (a) total load count is manageable within a single panel, (b) building layout results in acceptably short feeder runs, and (c) cost minimization outweighs operational flexibility. *(Rationale enriched per F-003: substantiated value judgment requires structured decision criteria.)* |
| Crane circuit approach | Separate dedicated feeders from MDP for each crane | Single feeder to crane busway | Depends on crane manufacturer's specification; separate feeders are more common for individual crane control. TBD. |
| Low-voltage power on SLD | Include power supply notation for camera/radio systems | Exclude until DEL-004-07 is developed | Safer to include TBD placeholder; avoids discovering missed circuits at installation. |

---

## Examples

No examples are available from source documents. The conceptual drawing (App B — Electrical) provides a floor plan load layout but not an SLD format example.

ASSUMPTION: The Electrical Engineer will follow standard Alberta/Canadian SLD conventions as used in industrial building electrical designs, consistent with APEGA practice guidelines and CEC requirements.

---

## Terminology Normalization Notes

The following terminology inconsistencies have been identified across the four documents and should be normalized by the Electrical Engineer during the next revision cycle:

| Item | Datasheet Term | Specification Term | Procedure Term | Proposed Canonical Term | Notes |
|---|---|---|---|---|---|
| Fire hose pump circuit | "Fire Hose Pump Circuit" | "Fire Hose Pump" (REQ-SLD-005 table) | "fire hose pump (70A)" (Step 1) | **Fire Hose Pump — 70A Dedicated Circuit** | Normalize to consistent capitalization and include rating for traceability. *(Identified per E-002.)* |
| Pressure washer circuit | "Pressure Washer Circuit" | "Pressure Washer" (REQ-SLD-005 table) | "pressure washer (70A)" (Step 1) | **Pressure Washer — 70A Dedicated Circuit** | Same normalization pattern as fire hose pump. *(Identified per E-002.)* |
| Compressor circuit | "Compressor Circuit" | "Compressor" (REQ-SLD-005 table) | "compressor (40A)" (Step 1) | **Compressor — 40A Dedicated Circuit** | Same normalization pattern. *(Identified per E-002.)* |
| Drawing revision register | N/A | "Drawing revision register" (Documentation table) | "Revision Register" (Records table) | **Drawing Revision Register** | Normalize to consistent full name across Specification and Procedure to avoid audit confusion. *(Identified per E-003.)* |

*(These are normalization recommendations for human review. The terms in the source documents refer to the same entities; adopting consistent canonical names will improve traceability and reduce confusion during construction and inspection.)*

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-SLD-001 | System voltage (120/208V vs. 347/600V) not specified in source documents. Selection affects all downstream SLD content, panel ratings, and fixture driver specifications. | App B (Electrical) — no voltage stated | RFP §3.4 — "three-phase power" only | REQ-SLD-001, REQ-SLD-002; Considerations (voltage selection) | PROPOSAL: Electrical Engineer to confirm with utility and document in DEL-004-01 Preliminary Design. SLD to remain TBD until confirmed. | TBD |
| CONF-SLD-002 | Crane circuit ratings not specified. App B (Electrical) shows crane power feeds without ampacity. | App B (Electrical) — no rating shown | SOW-0059 — "provide power for two 5-tonne overhead cranes" — no electrical specification | REQ-SLD-005; Principles §5 | PROPOSAL: Crane manufacturer specification (DEL-016-01) to govern. Hold TBD on SLD until crane spec received. | TBD |
| CONF-SLD-003 | Overhead door quantities and motor ratings not specified. App B (Electrical) shows doors but does not specify motor ampacity or quantity explicitly for SLD purposes. | App B (Electrical) — doors shown, no motor rating | SOW-0060 — "power for all overhead doors" — no quantity or rating | REQ-SLD-005 | PROPOSAL: Architectural drawing (DEL-001-07 Door & Window Schedule) to confirm door count and motor specifications. | TBD |
