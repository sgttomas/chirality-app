# Guidance — DEL-006-07 Plumbing Calculation Package

---

## Purpose

DEL-006-07 exists to provide the engineered justification for all plumbing and water system design decisions made under SOW-0016 (Complete final plumbing design — water supply, drainage, septic). The calculation package:

1. Demonstrates that the systems sized in the IFC plumbing drawings (DEL-006-02 through DEL-006-05) meet the explicit design requirements of the RFP.
2. Provides the evidentiary basis for P.Eng. certification of the plumbing design (OBJ-003 — stamped IFC documentation across all disciplines). **Certification scope note:** The P.Eng. certification boundary for this deliverable should be clarified — specifically whether the P.Eng. stamps the calculation package only, or also the IFC drawings, or both. The certification scope affects what "evidentiary basis" this package must provide. ASSUMPTION: P.Eng. stamps both the calculation package cover sheet and the IFC plumbing drawings (REQ-011); the Plumbing Engineer should confirm the certification scope with the project manager. Source: R-01 §3.3.2; _SEMANTIC_LENSING.md item C-002.
3. Supports commissioning and operational readiness of all plumbing and water storage systems to operational readiness by December 31, 2026 (OBJ-004).
4. Establishes the design assumptions record that will be referenced during the 2-year guarantee period (R-01 §2.10).

This calculation package is a **design-phase deliverable**, not a construction or commissioning record. Its outputs feed the IFC drawing set and specification (DEL-006-08). It is produced before construction begins.

Source: WDMLRL_Decomposition_Claude.md (DEL-006-07 entry, OBJ-003, OBJ-004); R-01 §3.3.2, §3.4.

---

## Principles

### Principle 1 — Off-Grid Water System Design

The New North Shop has no municipal water or sewer connections. All water supply is sourced from the on-site cistern; all sanitary waste discharges to the on-site septic holding tank. This fundamentally shapes the calculation approach:

- Water demand analysis must be conservative: the cistern (50,000 L) is the sole water reserve. Demand calculations should identify the fill cycle frequency to support operations.
- Pump sizing must balance peak simultaneous demand (pressure washer reels, wash station, emergency shower, washroom) against cistern drawdown.
- Septic loading calculations must account for limited holding capacity (2,000 US gallon tank); design should flag expected pump-out frequency for Owner awareness.

Source: R-01 §3.4 (cistern 50,000 L; pump 100 LPM; septic 2,000 US gallon); R-06 drawing.

### Principle 2 — Industrial Load Profile

The building serves heavy equipment maintenance (motor-scraper class) and wash operations. The plumbing system is designed for industrial, not residential, demands:

- The pressure washer reel and wash bay represent high instantaneous flow demands.
- Floor drains must accommodate wash-down volumes, not just incidental leakage.
- The mud sump is sized for motor-scraper wash volumes and must be accessible by excavator for cleanout.
- Occupancy fixture count for washroom/wash station sizing is secondary to process water demands in this facility type.

Source: R-01 §3.1 (wash bay for motor-scraper class), §3.4 (sump drains, pressure washer, bulk water fill); R-06 drawing.

### Principle 3 — Code Compliance is Non-Negotiable

Alberta Safety Code permit is required (SOW-0007). All calculations must be consistent with the governing Plumbing Safety Code order. Where code editions are uncertain at this stage, engineering judgment based on current NPC and Alberta amendments shall be applied and documented as an assumption. The responsible P.Eng. shall confirm applicable code at permit submission.

Source: R-01 §3.3.2 (SOW-0008, SOW-0009); R-01 §3.3.2 (SOW-0018, P.Eng. stamp requirement).

### Principle 4 — Assumptions Must Be Explicit

Because this is a design-build project with a conceptual-level owner brief (R-01 §3.4), multiple design parameters are not defined in the RFP. The calculation package must clearly distinguish:
- Values specified by Owner (e.g., 50,000 L cistern, 100 LPM, 2,000 US gallon septic)
- Values determined by engineering (e.g., pipe diameters, slopes, vent sizes)
- Values assumed by the Design-Builder (e.g., occupancy count, simultaneous demand factor, septic pump-out frequency)

All engineering and Design-Builder assumptions must be listed in the design assumption documentation sub-artifact.

Source: R-01 §3.4 (design-build framing: "The County only has a concept in mind"); WDMLRL_Decomposition_Claude.md (D-005 decision log precedent for explicit assumption documentation).

---

## Considerations

### Consideration 1 — Existing Septic Tank Removal

The RFP requires removal of the existing septic tank and installation of a new 2,000 US gallon holding tank (R-01 §3.4, SOW-0043). The decomposition notes that relocation of the existing tank to a new site location is OUT of scope — this is the County's responsibility (Decomposition §4, SOW-0205). The calculation package should document this boundary: the Plumbing Engineer designs for the new holding tank only; decommissioning/relocation of the existing tank is excluded from the plumbing design scope.

Source: WDMLRL_Decomposition_Claude.md (SOW-0043, SOW-0205, D-002).

### Consideration 2 — Cistern Location and Fill Connection

The cistern (50,000 L) is shown on the R-06 drawing at the east side of the building. The 2.5" fill connection (R-01 §3.4) serves as the cistern fill inlet from the bulk water fill truck/system. Calculations should confirm that the fill connection diameter and pump capacity are compatible. The internal distribution pump (100 LPM) draws from the cistern to supply building services. These are two distinct pump systems; the calculation package should clearly differentiate them.

Source: R-01 §3.4 (SOW-0041, SOW-0042, SOW-0044); R-06 drawing.

### Consideration 3 — Emergency Shower Supply

Emergency showers have minimum flow and duration requirements under applicable safety standards. Because the water supply is cistern-fed (no municipal pressure), the design must verify that the pump system (or a dedicated supply arrangement) can deliver adequate pressure and flow to the emergency shower without interruption for the required minimum duration. If a dedicated supply is needed, this should be flagged as a design decision.

Source: R-01 §3.4 (SOW-0048); R-06 drawing; ASSUMPTION: ANSI Z358.1 or equivalent Alberta OHS standard applies.

### Consideration 4 — Washroom Renovation in Old North Shop

The scope includes renovation of the existing washroom in the Old North Shop and construction of a new locker/change room with laundry services (SOW-0073, SOW-0074). It is not explicit in the RFP whether DEL-006-07 covers plumbing calculations for the Old North Shop renovation or only the New North Shop addition. This is flagged as an open scope boundary question (see Conflict Table below).

Source: R-01 §3.4 (SOW-0073, SOW-0074); WDMLRL_Decomposition_Claude.md (PKG-006 scope description: "Cistern and distribution, pump systems, septic, floor/sump drains, mud sump connection, emergency shower, fixtures, wash sink, bulk water fill, washroom plumbing").

### Consideration 5 — Oil/Water Separator for Repair Bay Sump Drains

The repair bays service heavy diesel-powered equipment. Sump drains in these bays may require an oil/water separator before discharge to the septic system or holding tank. This is not explicitly stated in the RFP but is a common regulatory requirement for vehicle maintenance facilities in Alberta. The Plumbing Engineer should confirm regulatory requirements with the relevant authority and document the decision.

Source: R-01 §3.4 (SOW-0045 — "sump drains in repair bays"); ASSUMPTION: Alberta Environment or applicable regulation may require oil/water separation; specific requirement TBD.

### Consideration 6 — Booster Pump / Pressure Tank Decision

The cistern-fed water supply system has no municipal pressure. The internal distribution pump (100 LPM per R-01 §3.4) provides the primary pressure source, but the design should evaluate whether a booster pump or pressure tank is needed to maintain adequate pressure at all points of use, particularly during peak simultaneous demand scenarios (emergency shower + pressure washer reel + washroom fixtures). Procedure Step 4.5 flags this as an ASSUMPTION. The Plumbing Engineer should frame this as an explicit design decision with documented rationale, considering:
- Cost and complexity of a pressure tank vs. a higher-capacity pump
- Reliability implications of a single-pump vs. pump-and-tank configuration
- Emergency shower pressure requirements (which may mandate a dedicated or redundant supply arrangement — see Consideration 3)

Source: Procedure.md Step 4.5; _SEMANTIC_LENSING.md item E-003.

---

## Trade-offs

### Trade-off 1 — Cistern Volume vs. Fill Frequency

A 50,000 L cistern is specified by the Owner. The Plumbing Engineer should calculate whether this volume is adequate for the anticipated operational pattern (e.g., daily wash bay use, pressure washing cycles, washroom demand). If the estimated consumption indicates high fill frequency relative to available fill logistics, this should be documented as an operational note for the Owner. The calculation package cannot change the 50,000 L requirement (it is explicitly specified in R-01 §3.4) but can characterize the operational implication.

**Owner communication:** The cistern fill frequency analysis results should be formally communicated to the Owner (Camrose County) as an operational planning deliverable, not merely documented internally within the calculation package. The Plumbing Engineer should confirm the communication protocol for transmitting operational findings to the Owner (e.g., included in the design report, separate letter, or noted on IFC drawings). Source: _SEMANTIC_LENSING.md item D-003.

### Trade-off 2 — Septic Holding Tank Capacity

A 2,000 US gallon holding tank is specified. For a facility with washroom, wash station, and potentially laundry services, pump-out frequency is a critical operational consideration. The calculation package should estimate expected pump-out intervals to allow the Owner to plan accordingly. This is an Owner-information deliverable, not a design change.

### Trade-off 3 — Simultaneous Demand vs. Pipe Size

Larger distribution pipes reduce pressure drop but increase cost and installation complexity. The calculation package should identify the design simultaneous demand scenario (e.g., emergency shower active + pressure washer reel active + washroom fixture active) and size the distribution system for that worst-case scenario. The Plumbing Engineer shall document the simultaneous demand assumptions adopted.

---

## Examples

No worked examples from project sources are available at this stage (the RFP and conceptual drawing do not contain calculation examples). Worked examples will emerge from the engineering process itself and are not reproduced here.

TBD — Plumbing Engineer will populate engineering examples in the calculation package as produced.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CFT-001 | Scope of DEL-006-07: does the calculation package cover Old North Shop plumbing renovation (washroom, locker room, laundry) or only the New North Shop addition? | _CONTEXT.md (description focuses on New North Shop plumbing systems) | WDMLRL_Decomposition_Claude.md (PKG-006 scope includes "washroom plumbing" broadly; SOW-0016 covers "water supply, drainage, septic" without building-specific exclusion) | Specification.md §Scope; Procedure.md §Prerequisites | PROPOSAL: Include Old North Shop renovation plumbing in this package unless a separate deliverable is defined by the Plumbing Engineer. | TBD |
| CFT-002 | Bulk water fill pump flow rate: the RFP specifies "high volume pump" for external filling (SOW-0044) but does not state a target flow rate. The internal distribution pump is specified at 100 LPM (SOW-0042). It is unclear if both pumps are the same or separate systems, and what flow rate the bulk fill pump must achieve. | R-01 §3.4 (SOW-0042: "100 LPM with 2.5" cistern filling connection for internal service water distribution") | R-01 §3.4 (SOW-0044: "bulk water fill system with high volume pump for external filling" — no LPM stated) | Specification.md REQ-002, REQ-003; Datasheet.md §Plumbing Systems | PROPOSAL: Treat as two separate systems. Internal pump: 100 LPM for building distribution. Bulk fill pump: Plumbing Engineer to size based on tanker truck fill rates (ASSUMPTION: target TBD). | TBD |
| CFT-003 | Oil/water separator requirement for repair bay sump drains: not stated in RFP; may be required by Alberta Environment regulation for vehicle maintenance facilities. | R-01 §3.4 (SOW-0045: "sump drains in repair bays") — no separator mentioned | ASSUMPTION: Alberta environmental regulation may require oil/water separation before discharge to holding tank/ground | Specification.md REQ-005; Procedure.md §Steps | PROPOSAL: Plumbing Engineer to confirm with AEP or local authority whether separator is required and document in compliance matrix. | TBD |
