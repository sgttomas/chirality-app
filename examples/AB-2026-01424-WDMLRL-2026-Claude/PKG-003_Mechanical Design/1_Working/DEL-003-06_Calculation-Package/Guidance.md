# Guidance — DEL-003-06 Mechanical Calculation Package

---

## Purpose

DEL-003-06 exists to provide the **engineering basis of record** for the mechanical systems of the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It is a calculation-first document: it must exist and be approved before the HVAC layout plans (DEL-003-02), ductwork plans (DEL-003-03), exhaust plans (DEL-003-04), and equipment schedule (DEL-003-05) can be finalized with confidence.

The calculation package serves two primary project objectives:

- **OBJ-003:** Produce complete, P.Eng.-stamped IFC design documentation before construction begins. The calculation package is the engineering foundation that makes all mechanical IFC drawings defensible and code-compliant.
- **OBJ-004:** Install and commission all mechanical systems to operational readiness. Correct sizing in the calculation package directly determines whether the as-installed systems perform as intended.

Without this package, the mechanical contractor (PKG-013) risks installing equipment that is over-sized (cost and energy waste) or under-sized (occupant safety risk, regulatory non-compliance, and commissioning failure).

Source: Decomposition S5 (OBJ-003, OBJ-004); R-01 S3.3.2, S3.4.

---

## Principles

### P-01: Size for the Worst Case, Document All Assumptions
Industrial maintenance shops are demanding environments. The repair bays will intermittently contain large diesel-powered equipment with running engines; the wash bay will create humidity loads; the welding station produces fumes requiring active capture; the service pit creates a potential confined-space atmosphere. The calculation package shall use conservative design conditions and document every assumption explicitly, including design outdoor temperature, occupancy schedules, and equipment operating assumptions.

**Rationale:** If assumptions are later challenged (e.g., during permitting, commissioning, or Owner inspection), an explicit assumptions register allows targeted revision rather than a full recalculation.

Source: R-01 S3.3.2 (County rep present at all inspections); SOW-0008, SOW-0009; ASSUMPTION (engineering best practice).

### P-02: Balance Before You Size Equipment
The single most important coordination task in this calculation package is establishing the system-level air balance: the sum of all exhaust flows must be matched by supply (makeup air + infiltration + any other supply). An unbalanced building causes negative pressure, which forces unconditioned air infiltration through every gap — degrading heating efficiency and creating potential freeze risk on a 35 ft ceiling structure.

**Rationale:** The RFP specifies both a high-volume air exchanger and a forced-air makeup air unit as separate items (R-01 S3.4; R-04 App B), suggesting the design intent involves coordinated supply and exhaust. The calculation package must clarify which system handles which role and how they interact.

Source: R-01 S3.4; R-04 App B; ASSUMPTION (system integration methodology).

### P-03: Welding Exhaust Depends on County-Supplied Specifications
The County is responsible for supplying welding equipment specifications (SOW-0204; R-01 S3.4). The welding exhaust system sizing (REQ-M-006) cannot be finalized until those specifications are received. The calculation package shall include a placeholder calculation based on assumed typical equipment (ASSUMPTION), clearly flagged for revision when County specifications are received. See Procedure Step 6 for the corresponding production step.

**Rationale:** Proceeding with a clearly labeled assumption avoids blocking the rest of the calculation package while ensuring the County understands the outstanding action item.

Source: R-01 S3.4; SOW-0039; SOW-0204 (OUT — County supply).

### P-04: Service Pit Ventilation Is a Safety-Critical Calculation
The service pit/trench (SOW-0028) is a below-grade space where workers will be present while equipment is overhead. Carbon monoxide and hydrocarbon accumulation are credible hazards. The ventilation calculation for the service pit shall be treated as safety-critical and shall reference applicable Alberta OH&S requirements, not merely general building code minimums.

**Rationale:** The RFP explicitly requires the service pit to be "ventilated and lighted" (R-01 S3.4; SOW-0028). This is an explicit design requirement, not merely good practice.

Source: R-01 S3.4; SOW-0028; ASSUMPTION (Alberta OH&S Code applies).

### P-05: The Calculation Package Is a Living Document Through IFC
The calculation package will be produced in draft form during design development, then finalized to IFC quality when all inputs are confirmed (including geotech, building envelope design, County welding specs, and County approval of preliminary design). The document shall clearly indicate its revision status.

Source: R-01 S3.3.2 (preliminary design approval before final design); SOW-0010c, SOW-0013.

---

## Considerations

### C-01: Climate Severity
The project site is near Ferintosh, Alberta (Camrose County), in Alberta's central region. Alberta design heating temperatures are severe (ASSUMPTION: approximately -35C or colder for design day; specific value to be confirmed from NBCC climate data for the nearest weather station). The 35 ft ceiling height of the main shop creates significant stratification potential, which affects both the heating system design and the justification for 6 ceiling fans. The ceiling fans (SOW-0040) serve a destratification function, reducing effective heating load at the occupied zone.

Source: R-01 S1.0 (location); R-04 App B (6 ceiling fans noted); ASSUMPTION (design temperature, destratification rationale).

### C-02: Large Overhead Doors and Infiltration
The building has multiple large overhead doors: at least two 24 ft drive-through repair bay doors, one 24 ft wash bay door, and a 16 ft parts room roll-up door (per App B drawing dimensions). These doors represent the dominant infiltration path during operation. The heating load calculation must account for door open time (ASSUMPTION: intermittent — doors open when equipment enters/exits) and the makeup air system must be capable of handling the resulting infiltration without creating unacceptable thermal comfort issues.

Source: R-04 App B (door widths visible on drawing); ASSUMPTION (door operation pattern).

### C-03: Multiple Exhaust Systems Competing for Makeup Air
The building has at least three distinct exhaust systems: (1) heavy equipment exhaust at the repair bays, (2) welding station exhaust, and (3) the high-volume air exchanger (general exhaust). All three must be supplied by the forced-air makeup air unit and/or passive infiltration. The total flow balance is the critical coordination calculation. If the heavy equipment exhaust system is operated while overhead doors are closed, the makeup air demand will be at its highest.

Source: R-01 S3.4; R-04 App B; SOW-0036, SOW-0037, SOW-0038, SOW-0039.

### C-04: Wash Bay Humidity and Drainage Interaction
The enclosed wash bay (SOW-0027a) will generate significant moisture from equipment washing. The mechanical design for the wash bay must address moisture control — either through dedicated exhaust, the high-volume air exchanger, or a combination. The wash bay mud sump (SOW-0027b) is exterior, but floor drains inside the wash bay connect to it. The calculation package should address wash bay ventilation as a distinct zone. **See REQ-M-012 for the corresponding requirement.**

Source: R-01 S3.4; R-04 App B; SOW-0027a, SOW-0027b. [Enrichment C-002 added REQ-M-012 in Specification.]

### C-05: Natural Gas Tie-In Dependency
The high-recovery heating system and makeup air unit are expected to be gas-fired (ASSUMPTION — based on the natural gas tie-in being in scope at SOW-0080; three-phase power alone is less typical for large industrial heaters in Alberta). The calculation package sizing must be coordinated with the natural gas supply sizing (PKG-018 / DEL-018-06 — Utility Tie-Ins). If electric heating is selected instead, the electrical calculation package (DEL-004-08) will be affected. **If gas-fired equipment is selected, a combustion air supply calculation is required per code — see REQ-M-013.**

Source: SOW-0080; SOW-0035; SOW-0037; ASSUMPTION (fuel type). [Enrichment X-002 added REQ-M-013 in Specification.]

### C-06: Mezzanine Zone
The mezzanine (above parts room, utility room, and wash bay) is a storage area. The RFP notes it is load-bearing (oil totes, pump equipment — SOW-0033). Mechanical ventilation or heating of the mezzanine zone is not explicitly required by the RFP. ASSUMPTION: basic ventilation may be required by code; the calculation package should identify whether a separate mezzanine HVAC zone is required or whether it can be served by carryover from adjacent zones.

Source: R-01 S3.4; R-04 App B; ASSUMPTION.

### C-07: Energy Performance Expectations

**TBD — Owner's energy performance expectations beyond code minimum are not documented in accessible sources.** The calculation package currently focuses on sizing correctness and code compliance. Trade-off T-01 mentions "life-cycle cost considerations," but no principle or consideration establishes whether the Owner values energy efficiency beyond code minimum (e.g., ASHRAE 90.1 compliance, high-efficiency equipment targets, or utility incentive program participation).

If the Owner has energy performance targets beyond code minimum, these would affect equipment selection (e.g., high-efficiency condensing heaters vs. standard-efficiency), MUA unit heat recovery provisions, and potentially the role of the air exchanger (HRV/ERV for heat recovery vs. simple exhaust). Resolution of ASHRAE 90.1 applicability (Specification REQ-M-010, Enrichment F-001) may partially address this consideration.

> **[Enrichment D-003]:** Energy efficiency objectives are absent from the Guidance principles. Source: Guidance.md Principles; Guidance.md Trade-offs T-01. PROPOSAL: Confirm code-minimum-only approach with Owner, or add energy performance targets.

Source: ASSUMPTION; Specification.md REQ-M-010. PROPOSAL: Clarify with Owner whether code-minimum-only is acceptable or whether higher energy performance targets apply.

### C-08: Unit Convention for Airflow Values

**The calculation package shall establish a primary unit convention for airflow values and apply it uniformly across all documents.** Currently, documents use both "CFM or L/s" and "L/s or CFM" interchangeably (e.g., Procedure Step 3 uses "L/s or CFM"; Specification REQ-M-008 uses "CFM or L/s"). Mixed unit references risk transcription errors when values flow from calculations to equipment schedules and drawings.

ASSUMPTION: Canadian practice typically uses L/s for design calculations and CFM for equipment catalog data. The Mechanical Engineer should establish and document the primary convention in Section 1 (Design Basis) of the calculation package, and apply it consistently. Where dual units are needed, establish which is primary and which is parenthetical.

> **[Enrichment F-004]:** Unit normalization across all documents. Source: Specification.md REQ-M-008; Procedure.md Step 3; Procedure.md Step 9. PROPOSAL: Establish primary unit convention (likely L/s per Canadian practice or CFM per equipment catalogs) in Guidance and apply uniformly.

Source: ASSUMPTION (engineering best practice).

---

## Trade-offs

### T-01: High-Recovery Heating System — Unit Heaters vs. Radiant vs. Overhead Air Handling
The RFP specifies a "high-recovery heating system" (R-01 S3.4; SOW-0035) without prescribing the type. Common options for Alberta industrial shops at this scale include:
- Gas-fired unit heaters (overhead, high-efficiency)
- Infrared radiant heaters (tube or spot)
- Overhead forced-air makeup air unit with heating coil (combined MUA + heat)

**Trade-off:** Radiant systems heat objects/people directly and are less affected by air stratification, but are typically more expensive and may conflict with the crane envelope (two 5-tonne overhead cranes on trolley — SOW-0067). Unit heaters are cost-effective but require ceiling fan destratification at 35 ft height. Combining heating into the MUA unit is efficient but creates a single-point-of-failure for both heating and ventilation.

**Crane envelope constraint:** The crane envelope clearance is a critical constraint for any overhead mechanical equipment placement. The Mechanical Engineer shall confirm crane rail height, trolley height, and required clearance zone from structural drawings (PKG-016) before positioning overhead heaters, MUA discharge, or any equipment that could interfere with crane travel. **Methodology: confirm crane envelope dimensions from structural/crane package and overlay with proposed equipment locations; minimum clearance per crane manufacturer requirements or Alberta OH&S.**

> **[Enrichment X-001]:** Crane envelope guidance expanded. Guidance T-01 mentioned crane conflict briefly but did not provide methodology for confirming adequate clearance. Source: Guidance.md T-01; Procedure.md PR-04; Procedure.md Step 8. PROPOSAL: Added methodology guidance for crane envelope clearance confirmation.

**Proposal:** The Mechanical Engineer should evaluate all three options with life-cycle cost considerations. The crane envelope must be confirmed before overhead equipment positions are fixed. This trade-off is unresolved; **Human Ruling: TBD.**

Source: R-01 S3.4; SOW-0035, SOW-0040, SOW-0067; ASSUMPTION.

### T-02: Air Exchanger vs. Makeup Air — Overlap and Delineation
The RFP specifies both a "high volume air exchanger" (SOW-0036) and a "forced-air makeup air" unit (SOW-0037) as separate items. These may serve overlapping functions (general building exhaust and tempered supply). The calculation package must clearly define what each unit does so that specifications and equipment schedules are not internally contradictory.

**Trade-off:** If the air exchanger provides both supply and exhaust (heat recovery ventilator / energy recovery ventilator), the MUA unit may serve as supplemental capacity or be the primary unit with the air exchanger as supplemental. If the air exchanger is exhaust-only, the MUA unit provides all supply. This delineation affects capacity sizing significantly.

**Proposal:** Treat as an open design question for the Mechanical Engineer to resolve; document the selected interpretation in the calculation package assumptions. **Human Ruling: TBD if Owner has a preference.**

Source: R-01 S3.4; SOW-0036, SOW-0037; ASSUMPTION.

### T-03: Heating Load Safety Factor Selection

**TBD — The basis and specific value for the heating load safety factor are not established.** Specification REQ-M-002 and Procedure Step 2.4 reference "ASSUMPTION: 10-15% or per engineering judgment," but the choice between 10% and 15% could change equipment selection by tens of kW for a building of this size.

The Mechanical Engineer shall document the selected safety factor value and its engineering basis in the calculation package (Section 2). Considerations include:
- Industry standard practice for Alberta industrial shops
- Whether the factor accounts for infiltration uncertainty (particularly with large overhead doors)
- Whether a lower factor is acceptable if infiltration is calculated explicitly rather than estimated
- Whether the Owner or authority having jurisdiction mandates a specific factor

> **[Enrichment F-002]:** Safety factor basis and range were stated as assumption without defensible justification. Source: Specification.md REQ-M-002; Procedure.md Step 2. PROPOSAL: Mechanical Engineer to document selected factor and engineering basis in calculation package.

Source: Specification.md REQ-M-002; Procedure.md Step 2.4; ASSUMPTION. **Human Ruling: TBD.**

---

## Examples

No worked examples are available from accessible sources. The following are placeholder descriptions of what the calculation package should contain:

- **Heating load example format:** ASSUMPTION — calculation sheet showing zone-by-zone heat loss using ASHRAE or NBCC method, with inputs for U-values, areas, design temperature differential, and infiltration.
- **Exhaust sizing example format:** ASSUMPTION — fan selection table showing required CFM, estimated static pressure, selected fan model (TBD from manufacturer data), and performance curve intersection point.

Actual worked examples will be populated by the Mechanical Engineer during design development.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-M-001 | Heating system type is unspecified — "high-recovery heating system" could mean unit heaters, radiant heaters, or a combined MUA+heating unit. Selection affects crane envelope compatibility, ceiling fan need, and cost. | R-01 S3.4 (high-recovery heating system) | R-04 App B (Forced Air Makeup listed separately, implying distinct system) | REQ-M-002; Trade-off T-01; Datasheet (System Inventory); Specification Verification | PROPOSAL: Mechanical Engineer to evaluate and document chosen system type in Calculation Package before equipment schedule (DEL-003-05) is finalized. | TBD |
| CON-M-002 | Role delineation between "high volume air exchanger" (SOW-0036) and "forced-air makeup air unit" (SOW-0037) is ambiguous — both could be interpreted as serving general building ventilation. **Note: Procedure Step 9 system balance table lists both "Air Exchanger -- Supply" and "Air Exchanger -- Exhaust" as separate line items, implying bidirectional operation. This pre-decides the question that CON-M-002 leaves open. The system balance table shall be treated as conditional on the resolution of this conflict.** | R-01 S3.4 (SOW-0036 and SOW-0037 listed as separate items) | R-04 App B (Forced Air Makeup noted; air exchanger not separately called out on drawing) | REQ-M-003; REQ-M-004; Trade-off T-02; system balance (REQ-M-009); **Procedure Step 9 system balance table [Enrichment E-005]** | PROPOSAL: Mechanical Engineer to define each system's role explicitly in the calculation package assumptions. If the Owner has a preference (e.g., HRV vs. separate ERV), obtain confirmation before final sizing. **Align Procedure Step 9 table with the resolution of this conflict.** | TBD |
| CON-M-003 | Welding exhaust sizing cannot be finalized until County supplies welding equipment specifications (SOW-0204 — County responsibility). Risk of under-sizing if interim ASSUMPTION is used in IFC drawings. | R-01 S3.4 (welding exhaust required) | SOW-0204 (County to supply welding equipment specs — OUT of Design-Builder supply scope) | REQ-M-006; Guidance P-03; Procedure Step 6 | PROPOSAL: Flag welding exhaust calculation as PRELIMINARY in the calculation package; include a formal RFI to County requesting welding specifications; do not finalize IFC exhaust drawings until specs received. | TBD |
