# Guidance — DEL-013-06: Ceiling Fans

---

## Purpose

DEL-013-06 exists to deliver six ceiling fans that provide supplemental air circulation in the main shop area of the New North Shop. The fans serve two primary functional roles:

1. **Destratification in winter**: The 35 ft ceiling (structure type TBD per Conflict Table CF-013-06-03; App B-Shop, R-04) creates significant thermal stratification in a heated industrial space. A high-recovery heating system (DEL-013-01) and forced-air makeup system (DEL-013-03) deliver heated air, but without circulation the warm air pools at ceiling level, wasting energy and leaving the occupied zone cold. Ceiling fans in reverse (pushing air upward, forcing warm ceiling air down the walls) break this stratification.

2. **Air movement / perceived cooling in summer / shoulder seasons**: In warmer periods, fans circulating air downward create a wind-chill effect at the occupied floor level, improving worker comfort without additional mechanical cooling.

The fans also support the function of the exhaust systems (DEL-013-04, DEL-013-05) by maintaining general air movement that assists in drawing vehicle and welding exhaust toward the exhaust pick-up points.

Source: _CONTEXT.md Description; _DEPENDENCIES.md Support Functions; OBJ-004 (commission all mechanical systems to operational readiness).

---

## Principles

### P1: Fans are a supplement, not a substitute, for the primary HVAC systems
The ceiling fans assist air distribution and comfort but do not replace the heating (DEL-013-01), makeup air (DEL-013-03), or air exchange (DEL-013-02) functions. They operate in coordination with those systems, not independently. Operational modes (all fans on, fans off, fans at low speed) should be documented in the O&M manual so operators understand the intended coordination.

Source: _CONTEXT.md Key Requirements ("Integration with overall HVAC system"); _DEPENDENCIES.md Support Functions.

### P2: The 35 ft ceiling height demands a purpose-selected, high-ceiling fan
Standard residential or light commercial fans are not appropriate. A 35 ft installation height requires fans with sufficient blade area and motor power to move meaningful air volumes down to the 8-12 ft occupied zone. HVLS (High Volume, Low Speed) fans are the standard industrial solution for spaces of this ceiling height and floor area.

**Note (A-001):** This principle strongly implies HVLS is the correct product type, but Specification REQ-013-06-08 currently says "industrial or heavy-commercial grade" without mandating HVLS. The normative requirement should either mandate HVLS specifically or state minimum performance criteria (e.g., minimum airflow volume, minimum effective coverage area per fan) that effectively select the appropriate fan type. This is a decision for the Mechanical Engineer.

**Note (B-002):** If HVLS fans are selected, the electrical power assumption (120V single-phase per Datasheet) is likely invalid. HVLS fans typically require 208V/240V or 480V three-phase power. This materially changes the DEL-015 electrical interface.

Source: App B-Shop (R-04) — 35 ft ceiling height; industry practice (ASSUMPTION: HVLS or large-diameter industrial fans are appropriate; specific model TBD from mechanical engineer specification).

### P3: Overhead crane clearance is the primary safety constraint
The two 5-tonne overhead cranes (App B-Shop, R-04; App B-Elec, R-05) operate in the same main shop airspace as the ceiling fans. Fan mounting positions and downrod lengths must be coordinated with crane rail height and maximum hook elevation to eliminate collision risk. This coordination requires IFC crane drawings (DEL-016) and structural drawings (DEL-002) to be available before final fan positions are set.

Source: _DEPENDENCIES.md Constraint Notes; App B-Elec (R-05) crane locations.

### P4: Structural attachment must be engineer-approved
Ceiling fans generate both static dead load and dynamic cyclic loading from motor vibration and blade rotation. Industrial fans at 35 ft ceiling height are typically larger and heavier than residential fans. The structural attachment must be designed and approved by the Structural Engineer of Record. **Note (B-003):** The actual ceiling structure type (concrete vs. steel purlin/beam) is unresolved — see Conflict Table CF-013-06-03. Mounting hardware selection (concrete anchors vs. beam clamps) depends on this determination.

Source: _DEPENDENCIES.md Constraint Notes ("Ceiling structure must support fan weight and vibration"); _REFERENCES.md Approval Documents ("Structural engineer approval (load-bearing)").

### P5: Electrical scope interface requires early coordination
Fan branch circuits are in DEL-015 (Electrical Contractor scope). Fan mounting and junction box rough-in must be coordinated with the Electrical Contractor before drywall/ceiling closure (if any) and before crane installation. Sequencing: structural attachment confirmed --> electrical rough-in (DEL-015) --> fan installation --> electrical connection --> commissioning.

Source: _DEPENDENCIES.md External Dependencies ("Electrical power distribution finalization"); App B-Elec (R-05).

---

## Considerations

### Fan Layout
No individual fan positions are shown on App B-Elec (R-05) — the drawing notes "6 Ceiling Fans for Main Shop" but does not plot individual symbols. Layout should be determined by the Mechanical Engineer during design, considering:
- Even distribution across the ~13,000 sq ft main shop footprint (RFP §3.1, R-01)
- Avoidance of crane operating envelopes
- Proximity to high-bay lighting rows (5 rows of 4 lights per App B-Elec) to avoid interference
- Makeup air supply and exhaust extract locations to avoid short-circuiting airflow

ASSUMPTION: A grid of 6 fans (e.g., 2 rows x 3, or 3 rows x 2) distributed evenly across the main bay is the likely layout, subject to crane clearance constraints.

### HVLS vs. Standard Industrial Fan
For a 35 ft ceiling in a ~13,000 sq ft shop (RFP §3.1), HVLS (High Volume Low Speed) fans with large blade diameters (8-24 ft) are the most energy-efficient and effective option. They move large volumes of air at low rotational speed, producing minimal noise and vibration. Standard high-speed smaller-diameter fans are an alternative but require more units to achieve equivalent coverage and generate more noise.

ASSUMPTION: HVLS fans are the appropriate product type. Final selection is the Mechanical Contractor's responsibility, subject to Mechanical Engineer review and Owner acceptance.

### Winter Destratification Savings
At 35 ft ceiling height, temperature differentials between floor and ceiling in an unassisted heated space can exceed 10-15 degrees C (industry rule of thumb). Ceiling fans running in reverse mode (pushing air upward against ceiling, returning warm air along walls) can eliminate most of this differential, potentially reducing heating energy consumption.

**Note (F-004):** The energy savings claim is qualitative only. No specific energy model, calculation, or published industry study has been cited from available project sources. This should be treated as a **qualitative expectation based on general industry practice**, not a quantified benefit. If the Proponent wishes to include energy savings claims in the design rationale, they should reference published industry data on destratification energy savings in high-ceiling industrial spaces (e.g., ASHRAE or fan manufacturer case studies) or perform a project-specific energy analysis. ASSUMPTION: Energy savings are expected but unquantified.

### Welding Fumes Interaction
Fan operation in the welding station zone (northeast corner per App B-Elec, R-05) must not direct air currents that disperse welding fumes horizontally across the shop before the dedicated welding exhaust system (DEL-013-05) can capture them. Fan mode and speed near the welding station should be addressed in the O&M documentation.

Source: App B-Elec (R-05) welding station location; _DEPENDENCIES.md ("Support removal of welding fumes").

### Maintenance Access
At 35 ft ceiling height, fan maintenance (blade cleaning, balancing adjustment, motor service) requires elevated access equipment. The O&M manual should specify maintenance intervals, access requirements, and recommended access equipment for the 35 ft ceiling height (E-004). ASSUMPTION: Permanent gantry cranes in the shop may provide maintenance access, but this is TBD. See Specification Documentation section — O&M Manuals must include maintenance access method.

### Control Type Decision (D-003)
The trade-off between individual wall switches and centralized/grouped control panel (see Trade-offs table below) requires resolution. The following evaluation criteria should be considered:
- **Operational simplicity**: Centralized control is simpler for operators managing all 6 fans
- **Cost**: Wall switches are lower initial cost; centralized panel adds wiring and controller cost
- **Maintainability**: Wall switches are individually replaceable; centralized panel is a single point of failure
- **Integration**: Centralized control is more compatible with future BMS integration
- **Decision-maker**: Owner and/or Mechanical Engineer should make this determination based on operational preferences and budget

Source: _CONTEXT.md Scope ("Control system integration"); ASSUMPTION: evaluation criteria inferred from standard practice.

---

## Trade-offs

| Decision Point | Option A | Option B | Recommended Direction | Basis |
|---|---|---|---|---|
| Fan type | HVLS (large-diameter, low-speed) | Standard industrial high-speed fans | HVLS preferred for this ceiling height and coverage area | Industry practice; 35 ft ceiling, large floor area |
| Quantity distribution | Symmetric grid (e.g., 2x3) | Asymmetric placement around crane obstacles | Asymmetric if crane envelopes require it | Crane clearance is the primary constraint (P3) |
| Control type | Individual wall switches per fan | Centralized or grouped control panel | TBD — centralized preferred for operator ease; see Considerations "Control Type Decision" (D-003) for evaluation criteria | Convenience; _CONTEXT.md Scope ("Control system integration"). Decision-maker: Owner/Mechanical Engineer. |
| Direction reversal | Fixed direction only | Reversible motor (summer/winter modes) | TBD — reversibility status (mandatory vs. recommended) requires resolution per Specification REQ-013-06-11 (C-001) | Destratification benefit in 35 ft space; ASSUMPTION |

---

## Examples

No project-specific examples are available from sources. TBD — Mechanical Engineer to reference comparable industrial maintenance shop installations in Alberta climate conditions if available.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CF-013-06-01 | Ceiling fans are listed in App B-Elec (R-05) Electrical Notes but are NOT listed in RFP §3.4 Design Requirements text (R-01). It is unclear whether this is an intentional omission or oversight, and whether fans are a firm mandatory requirement or an Owner preference expressed via conceptual drawing only. (D-001: this remains unresolved and could be used to argue fans are optional if a dispute arises.) | R-05 App B-Elec Electrical Notes: "6 Ceiling Fans for Main Shop" | R-01 RFP §3.4 Design Requirements: no explicit mention of ceiling fans | Specification REQ-013-06-01 (quantity); overall deliverable scope | Fans are in-scope based on SOW-0040 explicitly listing "Install 6 ceiling fans in main shop area" (Decomposition §8, citing App B-Elec as source). SOW-0040 is a firm decomposed scope item. PROPOSAL: treat as mandatory; obtain Owner written confirmation. | TBD |
| CF-013-06-02 | Appendix B (Electrical) attributes ceiling fans to Electrical Notes on the electrical conceptual drawing, which may suggest the Electrical Contractor supplies/installs fans. SOW-0040 is assigned to PKG-013 (Mechanical Contractor). Interface boundary for fan procurement and installation (Mechanical vs. Electrical Contractor) is not explicitly stated in sources. | R-05 App B-Elec (fans in electrical notes/drawing) | Decomposition PKG-013 DEL-013-06 (Mechanical Contractor) | Procedure Step assignments; contractor coordination | PROPOSAL: Mechanical Contractor supplies and installs fan assemblies; Electrical Contractor provides branch circuit to junction box (as is standard practice). Confirm with Owner and Design-Builder at contract scope clarification. | TBD |
| CF-013-06-03 | Ceiling structure type is inconsistent across documents. Datasheet Conditions originally stated "Concrete structure" (sourced to App B-Shop R-04), but Guidance P4 references "structural ceiling/purlin/beam," Specification REQ-013-06-05 says "ceiling mounting structure (structural attachment point)," and Procedure Step 3.1 references "structural ceiling attachment points" and "purlin." A concrete ceiling and a steel purlin/beam structure require different mounting hardware (concrete anchors/expansion bolts vs. beam clamps/welded brackets). (B-003) | App B-Shop (R-04) building notes: "Concrete structure" | Guidance P4; Specification REQ-013-06-05; Procedure Step 3.1: references to "purlin/beam" and "structural ceiling attachment points" | Datasheet Conditions "Ceiling Structure Type"; Specification REQ-013-06-05; Procedure Step 3 (mounting hardware); Construction in Datasheet | PROPOSAL: Verify against structural drawings (DEL-002) to confirm actual ceiling structure type and update Datasheet and all dependent references accordingly. | TBD |

---

## Semantic Lensing Enrichment Log (Pass 3)

The following warranted items from `_SEMANTIC_LENSING.md` were incorporated into this document during Pass 3:

| ItemID | Type | Action Taken |
|---|---|---|
| A-001 | WeakStatement | Added note to P2 clarifying HVLS vs. general industrial ambiguity; cross-referenced to Specification |
| B-002 | WeakStatement | Added note to P2 about HVLS power requirements potentially invalidating 120V assumption |
| B-003 | Conflict | Updated P4 with note about unresolved ceiling structure type; added new CF-013-06-03 to Conflict Table |
| C-001 | WeakStatement | Updated Trade-offs table direction reversal row to reference TBD mandatory/recommended status |
| D-001 | Conflict | Enhanced CF-013-06-01 with note about dispute risk if fans argued to be optional |
| D-003 | RationaleGap | Added new Considerations subsection "Control Type Decision" with evaluation criteria and decision-maker identification |
| F-004 | RationaleGap | Reworked Winter Destratification Savings to explicitly label energy savings claim as qualitative only with no cited evidence; added guidance on how to substantiate |
| E-004 | Normalization | Enhanced Maintenance Access consideration to cross-reference Specification Documentation O&M manual requirement |
