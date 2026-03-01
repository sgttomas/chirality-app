# Guidance — DEL-004-06 Panel Schedules

---

## Purpose

DEL-004-06 Panel Schedules exists to provide a complete, circuit-by-circuit accounting of every electrical load in the New North Shop Addition, organized by panel or distribution board. The panel schedule is the primary coordination document between the electrical design and the electrical installation contractor: it drives procurement of panels and breakers, informs load balancing across phases, and establishes the naming and numbering conventions used throughout construction and the building's operational life.

Within the PKG-004 Electrical Design package, the Panel Schedules are the synthesis document — they reflect and must be consistent with every other PKG-004 deliverable. They also directly support:

- **OBJ-003:** Produce complete, P.Eng.-stamped IFC design documentation across all disciplines. The Panel Schedules are a required component of the IFC electrical drawing set. (Source: Decomposition OBJ-003; RFP §3.3.2)
- **OBJ-005:** Install and commission all electrical and low-voltage systems to operational readiness. Panel schedules are essential for correct installation of the three-phase distribution system, all circuits, and equipment connections. (Source: Decomposition OBJ-005)

---

## Principles

### P1 — Completeness Before Precision
At the conceptual stage, Appendix B (Electrical) identifies loads by type and approximate rating. The panel schedule must eventually enumerate every circuit. During preliminary design, completeness of the load list takes priority over precise circuit sizing. No load shown on the electrical drawings should be absent from the panel schedule.
Source: RFP §3.3.2 (County approval of preliminary before IFC); App B (Electrical) load notes.

### P2 — Three-Phase Load Balance
The New North Shop Addition runs on three-phase power (RFP §3.4). The Electrical Engineer shall distribute single-phase loads across the three phases to minimize imbalance. Large single-phase loads (e.g., 70A fire hose pump, 70A pressure washer, 40A compressor) require careful phase assignment to achieve balance.
Source: RFP §3.4; App B (Electrical) notes.
ASSUMPTION: Load balancing is standard engineering practice for three-phase distribution panels; the RFP does not state a specific imbalance limit (location TBD in applicable code).

### P3 — Code Governs Circuit Sizing
All breaker ratings and conductor sizes in the panel schedule shall be governed by the Canadian Electrical Code, Part I (CSA C22.1) as adopted under Alberta Safety Codes. The Electrical Calculation Package (DEL-004-08) provides the supporting load calculations. The panel schedule is the output; the calculation package is the justification.
Source: RFP §3.3.2 ("The proposed building must adhere to all Alberta Safety Codes.").
ASSUMPTION: CEC Part I governs; specific Alberta amendments not confirmed from accessible sources (location TBD).

### P4 — Naming Consistency
Panel designations, circuit numbers, and load descriptions used in the Panel Schedules must match identically those used on the Single-Line Diagram (DEL-004-02), Power Distribution Plans (DEL-004-03), Lighting Plans (DEL-004-04), and Receptacle Layout Plans (DEL-004-05). Inconsistent naming is a common source of field error.
Source: ASSUMPTION — standard coordination practice; not explicitly stated in RFP.

### P5 — Spare Capacity Planning
Industrial maintenance facilities of this type benefit from spare circuit capacity to accommodate future equipment additions. The Electrical Engineer should plan for meaningful spare positions. **Note:** The specific spare capacity target is TBD (see Specification REQ-004-06-12). The Trade-offs section below provides options; the Electrical Engineer or County must define a binding target.
Source: ASSUMPTION -- standard design practice for industrial occupancy; not stated in RFP.

### P6 — Standards Accessibility
All technical design decisions for the Panel Schedules are governed by the Canadian Electrical Code, Part I (CSA C22.1) as adopted under Alberta Safety Codes. **Neither the CEC Part I text nor the Alberta Safety Codes Act text is currently accessible in the project sources.** The Electrical Engineer must obtain or confirm access to the current edition of CEC Part I and any applicable Alberta amendments before finalizing the panel schedule design. Until accessible, clause-level requirements are recorded as TBD throughout the Specification.
Source: Specification Standards table; Procedure References Required. ASSUMPTION: CEC Part I is applicable; edition and amendments TBD. (Lensing item X-001.)

---

## Considerations

### C1 — High-Current Equipment Loads
The three highest-current named loads are the Fire Hose Pump (70A), Pressure Washer (70A), and Compressor (40A). These are listed in Appendix B (Electrical) and should be confirmed against actual equipment specifications when available. Motor-load derating rules under CEC Part I will affect breaker sizing (typically 125% of full-load current for continuous motor loads).
Source: App B (Electrical) notes; ASSUMPTION: CEC Part I motor load rules apply.

### C2 — Crane Power Requirements
The two 5-tonne overhead cranes on trolley are among the most complex electrical loads in the building. Crane circuits require careful sizing based on the crane manufacturer's specifications, duty cycle, and CEC Part I requirements for crane and hoist wiring. These specifications are not available in the accessible sources. The Electrical Engineer should obtain crane specifications early in the design process to avoid late-stage panel revisions.
Source: RFP §3.4 ("2 – 5-tonne overhead cranes on a trolley."); App B (Electrical) notes ("Will need power for crane").
ASSUMPTION: Crane electrical specifications are a design input not yet available at the RFP stage.

### C3 — Welding Station Receptacles
The Appendix B (Electrical) drawing shows multiple 50A 240V receptacles clustered at the welding station area, along with 30A 240V receptacles nearby. The RFP states "Multiple electrical plugs throughout the shop area suitable for connecting high voltage welding equipment (County to supply welding equipment specifications)" (RFP §3.4). The panel schedule for welding circuits should be confirmed against County-supplied welding equipment specifications when available. Until then, the 50A 240V receptacles shown in App B are the basis of design.
Source: RFP §3.4; App B (Electrical) drawing and legend.

### C4 — Low-Voltage Systems Interface
Security camera wiring and 2-way radio antenna wiring are called out in App B (Electrical). These are typically low-voltage systems that may not require circuit breaker positions in a power panel. However, any power supplies for these systems (e.g., PoE switches, radio power supplies) will require panel circuits. The interface between the panel schedules and the Low-Voltage Plans (DEL-004-07) must be clearly defined to avoid gaps.
Source: App B (Electrical) notes.
ASSUMPTION: Low-voltage systems are addressed primarily in DEL-004-07; panel schedule includes power circuits for associated equipment only.

### C5 — Service Trench / Service Pit Lighting and Ventilation
Appendix B (Electrical) shows a service trench in the New North Shop Addition layout. The RFP §3.4 references a "ventilated and lighted service pit area for mechanics to perform servicing under equipment." Circuits for service pit lighting and ventilation should be included in the panel schedule. The Appendix B drawing shows lights ("L" symbols) near the service trench area.
Source: RFP §3.4; App B (Electrical) drawing.
ASSUMPTION: Service pit lighting circuits are included in the scope of DEL-004-06.

### C6 — Coordination with Mechanical Design (Exhaust Systems)
Exhaust fans shown in Appendix B (Electrical) serve both the welding station and the equipment bays. The Mechanical Design (PKG-003) establishes the exhaust system layout and fan specifications. The Electrical Engineer should obtain mechanical equipment schedules to correctly size exhaust fan circuits in the panel schedule.
Source: App B (Electrical) legend (E symbol); RFP §3.4 ("Exhaust hoses and fans for heavy equipment."; "Ventilation at welding station.").
ASSUMPTION: Exhaust fan specifications are a PKG-003 deliverable that feeds into PKG-004 panel schedule sizing.

### C7 — Design-Build Context
This is a design-build project under CCDC 14-2013. The Electrical Engineer is part of the Proponent's design team and is responsible for full coordination with all other disciplines. Panel schedule revisions are expected as design progresses from preliminary to IFC. Version control and reissue procedures should be established.
Source: RFP §2.7; Decomposition project context.

### C8 — Equipment Specification Procurement Timing
Multiple equipment specifications required for panel schedule sizing are currently TBD: crane electrical specifications (2 x 5-tonne overhead cranes), County-supplied welding equipment specifications, exhaust fan specifications (from PKG-003 Mechanical Design), and overhead door operator specifications. The Electrical Engineer should establish a priority order and timeline for obtaining these specifications, considering:
- **Crane specifications** are the most complex and have the highest impact on panel sizing and circuit design. These should be obtained earliest.
- **Welding equipment specifications** are County-supplied (RFP §3.4) and depend on County procurement timeline.
- **Exhaust fan specifications** depend on PKG-003 Mechanical Design progress.
- **Fallback approach:** If specifications are not available by the preliminary design stage, the panel schedule should include conservative placeholder circuits with explicit notation that breaker sizing is pending equipment confirmation. This approach allows the preliminary design to proceed while flagging risks for County review.

ASSUMPTION: Priority order and fallback approach are inferred from standard engineering practice. Specific timeline not stated in sources. (Source: Procedure Prerequisites; Guidance C2; lensing item F-002.)

### C9 — Future Building Expansion and Phased Load Growth
The New North Shop Addition is an industrial maintenance facility with an expected long service life. The Electrical Engineer and County should consider the possibility of future building phases or expansion of the maintenance shop that could affect main panel sizing and spare capacity decisions. Factors to consider include:
- Likelihood of additional equipment or service bays in future phases
- Potential for increased electrical load from technology upgrades (e.g., electric vehicle charging, automated equipment)
- Cost differential between sizing panels for current loads only versus sizing for anticipated growth
- Main service entrance capacity implications

**This consideration is TBD -- no analysis of future expansion is available in the accessible sources.** The County should communicate any known plans for future phases or expansion to inform the spare capacity decision (see Trade-offs section and Specification REQ-004-06-12).
Source: ASSUMPTION -- forward-looking analysis inferred from the industrial facility type and long service life. Not stated in RFP or accessible sources. (Lensing item E-002.)

---

## Trade-offs

| Trade-off | Option A | Option B | Consideration |
|---|---|---|---|
| Single panel vs. distributed sub-panels | Single main distribution panel | Main panel + sub-panels (e.g., separate panel for wash bay, lighting panel) | Single panel is simpler; sub-panels may be warranted given building size (~13,000 sq ft) and distribution distances. Electrical Engineer to determine based on load calculations. ASSUMPTION. |
| Spare capacity | Minimum spare (10%) | Generous spare (25%+) | Industrial maintenance facility; future equipment loads are likely. Greater spare capacity reduces future retrofit cost but increases initial panel and bus sizing costs. **Rationale gap (TBD):** A lifecycle cost impact analysis comparing initial over-sizing cost versus future panel replacement/retrofit cost has not been performed. The industrial maintenance use case suggests a high probability of future equipment additions, but no quantitative analysis supports a specific threshold. The County's expectations regarding future expansion should inform this decision (see C9). ASSUMPTION. (Lensing item F-003.) |
| Circuit grouping (lighting vs. power) | Separate lighting and power panels | Combined panel with mixed circuits | Separate panels simplify troubleshooting; combined panels reduce hardware cost. Standard practice varies; Electrical Engineer to decide per CEC Part I. ASSUMPTION. |

---

## Examples

No worked panel schedule examples are available from the accessible sources. The following is provided as structural context only:

ASSUMPTION: A typical panel schedule for a project of this type would include:
- Panel designation (e.g., "LP-1 — Lighting Panel," "PP-1 — Power Panel," "DP — Distribution Panel")
- Panel location (e.g., "Electrical Room," "Utility Room")
- Supply: from (upstream panel or service entrance)
- Main breaker rating (e.g., 200A, 400A, 600A)
- Bus rating
- Voltage/phase/wire (e.g., 120/240V, 1Ø, 3W or 120/208V, 3Ø, 4W or 347/600V, 3Ø, 4W)
- Circuit table: ckt #, description, breaker size, poles, load (amps or VA)
- Phase totals and balance summary

Exact format to be established by the Electrical Engineer.

---

## Conflict Table (for human ruling)

The following items are flagged as conflicts or ambiguities pending human ruling:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CF-004-06-01 | Service voltage not stated: RFP requires three-phase but does not specify voltage level (120/208V, 120/240V, or 347/600V). App B (Electrical) legend shows 15A 120V, 20A 120V/240V, 30A 240V, 50A 240V receptacles, suggesting a 120/240V or 120/208V service, but this is inconclusive for the main service voltage. **Cross-referenced in:** Datasheet (Service Voltage row), Specification (REQ-004-06-01 note). (Lensing item E-001.) | RFP §3.4 (three-phase required) | App B (Electrical) legend (120V and 240V loads shown) | Datasheet -- Service Voltage; Specification -- REQ-004-06-01; panel schedule header | PROPOSAL: Electrical Engineer to confirm service voltage based on utility supply and load analysis. If 120/240V single-phase loads predominate, a 120/208V wye or 120/240V delta service is likely. | TBD |
| CF-004-06-02 | Phase imbalance limit not specified: Guidance P2 requires minimizing imbalance, Procedure verification checks "Phase imbalance within acceptable limit (per CEC Part I or Electrical Engineer's criteria)," but no specific enforceable numeric threshold (e.g., maximum percentage imbalance between phases) is stated in the Specification. Without a defined limit, the requirement is unenforceable as written. (Lensing item C-001, X-004.) | Guidance P2 (minimize imbalance) | Procedure Verification (acceptable limit per CEC Part I or EE criteria) | Specification -- REQ-004-06-01; Procedure -- Verification (Load balance acceptable) | PROPOSAL: Electrical Engineer to define an acceptable phase imbalance percentage threshold, citing CEC Part I if applicable, or establishing a project-specific criterion. | TBD |
