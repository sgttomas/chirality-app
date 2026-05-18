# Guidance — DEL-002-12 Structural Specification

**Document Type:** Guidance (directional)
**Deliverable ID:** DEL-002-12
**Revision:** R1 — 2026-02-26
**Status:** SEMANTIC_READY (Pass 3 enrichment applied)

---

## Purpose

The Structural Specification (DEL-002-12) exists to define the normative performance, material, and execution requirements that govern the structural design of the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It serves as the written companion to the PKG-002 drawing set, establishing criteria that cannot be fully communicated through drawings alone.

Within the CCDC 14–2013 design-build contract, the Structural Specification is a key design document. It:

1. Translates RFP design requirements (§3.4, Appendix B) into enforceable technical criteria.
2. Provides the basis upon which the Structural Calculation Package (DEL-002-10) is validated.
3. Establishes material standards and workmanship requirements for use by the construction team (PKG-011 — Building Structure & Envelope).
4. Demonstrates compliance with OBJ-001 (code-compliant, functional facility) and OBJ-003 (complete, P.Eng.-stamped IFC documentation).

[Source: Decomposition §Objectives; RFP §3.3.2, §3.4]

---

## Principles

### Principle 1 — Specification Follows Function

The structural design must accommodate the County's operational program for a heavy-use landfill maintenance facility. The building will house track and packer equipment, overhead crane operations, a service pit, and a wash bay. Structural requirements must be set to handle actual operational loads, not minimum code minimums alone.

[Source: RFP §3.4 — equipment list including motor scraper, track equipment, 5-tonne cranes]

### Principle 2 — Concrete Structure is the Confirmed System

The RFP explicitly requires a concrete structure with a 35 ft clear ceiling. The Structural Specification shall be organized around this system. Alternative structural systems (e.g., steel frame) are not consistent with the RFP direction.

[Source: RFP §3.4 "Concrete structure 35' ceiling"; Appendix B notes]

### Principle 3 — Foundation Scope is Variable-Price and Separate

The foundation design and construction (SOW-0019) is a variable-price item in the CCDC 14–2013 contract, pending geotechnical investigation. The Structural Specification (SOW-0012 scope) shall state general foundation performance requirements (bearing capacity, frost depth, settlement limits — TBD), but shall cross-reference DEL-002-11 (Foundation Design Package) for the resolved foundation system. Do not import variable-price foundation cost assumptions into the firm-price Structural Specification scope.

[Source: RFP §4.8.2; Decomposition SOW-0019, PKG-002 scope description]

### Principle 4 — P.Eng. Stamp is a Hard Deliverable Requirement

All IFC structural design documents must be stamped by a P.Eng. licensed in Alberta. This is not discretionary. The specification must reference this requirement explicitly and the Proponent's organizational structure must demonstrate capacity to provide this.

[Source: RFP §3.3.2]

### Principle 5 — Coordination Across Disciplines is Structural's Responsibility to Flag

The structural system carries implications for mechanical (crane motor power, service pit ventilation penetrations), electrical (crane power, pit lighting conduit), and civil (mud sump drainage, pad loads). The Structural Specification should identify structural-discipline interface requirements and flag coordination responsibilities.

[Source: RFP §3.4 — coordinated systems list; RFP §1.0 — multi-discipline design-build scope]

---

## Considerations

### Consideration 1 — Concrete Structure Type: Tilt-Up vs. Cast-in-Place vs. Precast

The RFP requires a concrete structure but does not prescribe the concrete construction method. Common options for a building of this size and height include:

- **Tilt-up concrete:** Efficient for low-rise industrial buildings with large floor plates. May be challenging at 35 ft wall heights depending on panel thickness and crane availability.
- **Cast-in-place concrete:** More flexible for complex geometry; higher formwork cost.
- **Precast concrete:** Factory quality control; requires transport and erection crane.

ASSUMPTION: The Structural Engineer will determine the appropriate concrete system based on geotechnical conditions, site access, and cost. The Structural Specification should identify performance requirements (fire rating, wind/snow capacity, bearing capacity) and be agnostic to construction method unless a specific system is selected.

### Consideration 2 — Crane Runway Design Loads

The RFP specifies 2 × 5-tonne cranes on a trolley. Crane runway design depends on:
- Crane manufacturer specifications (wheel loads, runway gauge, bridge span)
- Dynamic impact factors
- Fatigue category (CMAA class) appropriate for landfill maintenance frequency of use

ASSUMPTION: Crane specifications are TBD at this stage. The Structural Specification should require the Proponent to obtain crane specifications and design the runway accordingly, and should reference CMAA Specification 70 or equivalent as the applicable standard.

**Rationale for CMAA fatigue class selection (TBD):** The choice between CMAA Class B/C (moderate service, 50,000-100,000 cycles) and Class D/E (heavy/severe service, 100,000-500,000+ cycles) depends on the anticipated frequency and severity of crane usage at the landfill maintenance facility. Factors to consider include:
- Number of crane lifts per day (Owner to provide operational data)
- Average load as percentage of rated capacity
- Duration of seasonal vs. year-round operations
- Whether cranes are used for routine maintenance lifting or for heavy overhaul work

ASSUMPTION: Landfill maintenance use suggests moderate-to-heavy frequency. However, the reasoning basis for class selection is thin without Owner-provided usage frequency data. The Structural Engineer should request this data from the Owner before finalizing the crane runway fatigue design. [Source: Guidance Trade-offs table; Lensing: B-004]

### Consideration 3 — Steel Embedment Plate Design

Steel plates embedded in the concrete floor at heavy equipment travel paths must be designed for:
- Track loads from packer and track-type equipment
- Impact and dynamic loads
- Differential movement between plate and concrete
- Corrosion protection (industrial environment with wash bay in proximity)

The Appendix B floor plan shows steel plate locations; final sizing is a design task for the Structural Engineer.

[Source: RFP §3.4; Appendix B]

### Consideration 4 — Mezzanine Live Load

The RFP describes the mezzanine as capable of handling "heavy items such as several oil totes and oil pumping equipment." A standard storage live load under NBC may be insufficient for this use. The Structural Engineer must assess the actual load scenario. ASSUMPTION: A heavier design live load (in the range of 4.8 kPa / 100 psf) may be appropriate; must be confirmed.

### Consideration 5 — Old North Shop Structural Assessment

Before renovating the existing mezzanine in the Old North Shop, a structural assessment of the existing structure is required to determine load capacity and any deficiencies. The Structural Specification should require a preliminary assessment as a prerequisite to renovation design.

[Source: Appendix B — "Old North Shop Mezzanine to be renovated"]

**Establishing an authoritative baseline (TBD):** When no as-built data is available for the existing Old North Shop mezzanine structure, the Structural Engineer must establish an authoritative baseline using one or more of the following methods:

1. **As-built drawings:** Request from the Owner or municipal records. If unavailable, record their absence explicitly.
2. **Field survey and measurement:** Conduct dimensional survey, member sizing, connection inventory, and material identification through visual inspection.
3. **Non-destructive testing:** Use methods such as cover meter surveys, rebound hammer testing, or ultrasonic thickness testing to assess member properties without damage.
4. **Destructive testing (limited):** Core samples or coupon removal for material strength confirmation, if non-destructive methods are inconclusive.
5. **Load testing:** If structural capacity is uncertain after analysis, a proof load test may be warranted.

The method(s) selected should be proportionate to the renovation scope and the consequences of structural inadequacy. The Structural Engineer should document the baseline establishment methodology in the structural assessment report. ASSUMPTION: The choice of baseline establishment method is a professional judgment call for the Structural Engineer. [Source: Specification REQ-008; Procedure Step 7; Lensing: E-001]

### Consideration 6 — Future Building Adaptability / Expansion (added by Pass 3 lensing)

The RFP and current documents address only the immediate building program. No document addresses whether the structural design should accommodate potential future growth or adaptability, such as:

- Additional drive-through bays
- Crane capacity upgrades (e.g., higher-tonnage cranes)
- Building extensions to the north or south
- Increased mezzanine loading for changed storage use

ASSUMPTION: The Owner's program may be fixed with no future expansion intent. However, this should be explicitly stated in the Structural Specification or confirmed with the Owner. If future expansion is a possibility, the structural system should be designed with expansion-friendly features (e.g., moment frames on expansion side rather than shear walls, foundation capacity for future additional load). If future expansion is not a consideration, the Structural Specification should note this explicitly to avoid over-design. [Source: No RFP reference to future expansion found; Lensing: E-002]

### Consideration 8 — Service Pit Edge Loads

The service pit walls and edges will be subjected to vehicle loads from equipment being driven over the pit (when the pit is bridged or during access). The pit structural design must account for these loads, not merely the self-weight of the pit structure.

[Source: RFP §3.4 — service pit for heavy equipment servicing]

### Consideration 9 — Quality Standard for the Structural Specification Document (added by Pass 3 lensing)

The Structural Specification, as a deliverable document product, should meet an explicit quality standard. The Procedure verification table lists checks, but the quality benchmark those checks serve has not been articulated. Recommended quality criteria include:

- **Completeness:** All RFP §3.4 structural requirements addressed with traceable REQ entries.
- **Internal consistency:** No contradictions between requirements, verification approaches, and standards references.
- **MasterFormat compliance:** Specification sections organized per Division 03 / Division 05 conventions (ASSUMPTION).
- **Peer review:** Independent review by a qualified P.Eng. not involved in primary authorship.
- **Coordination closure:** All multi-discipline coordination items resolved or documented as open items prior to IFC issue.

ASSUMPTION: These quality criteria represent standard Canadian structural engineering practice. The specific QA checklist to be used should be confirmed by the Structural Engineer's firm. [Lensing: C-003]

---

## Trade-offs

| Trade-off | Option A | Option B | Recommended Approach |
|---|---|---|---|
| Concrete system type | Tilt-up (lower cost, fast for large panels) | Cast-in-place or precast (more geometric flexibility) | ASSUMPTION: Structural Engineer to determine based on site conditions and cost; not resolved in Structural Specification. **Valuation criteria (TBD):** The Owner should state which factors are most important for this trade-off decision. Candidate evaluation criteria include: (a) construction cost, (b) schedule impact (December 2026 deadline), (c) quality/durability for industrial environment, (d) site access constraints (crane mobilization, panel staging area), (e) local contractor availability. The relative weighting of these factors should be confirmed by the Owner/PM before the Structural Engineer selects the system. [Lensing: F-004] |
| Mezzanine live load | Code minimum storage (e.g., 3.6 kPa) | Heavy storage (e.g., 4.8–7.2 kPa) | Design to heavier load given stated use; confirm with Owner |
| Foundation specification in DEL-002-12 | Include general performance requirements | Defer entirely to DEL-002-11 | Include performance intent (bearing capacity, settlement tolerance) in DEL-002-12 as requirements; delegate system selection to DEL-002-11 |
| Crane runway fatigue class | CMAA Class B or C (moderate service) | CMAA Class D or E (heavy service) | ASSUMPTION: Landfill maintenance use suggests moderate-to-heavy; Structural Engineer to confirm with Owner on usage frequency |

---

## Examples

No directly applicable structural specification examples are available from the accessible source set.

ASSUMPTION: The Structural Specification format should follow MasterFormat Division 03 (Concrete) and Division 05 (Metals) conventions, which are the standard organizational framework for structural specifications in Canadian construction practice. The Structural Engineer preparing DEL-002-12 should reference their firm's standard specification templates as a starting point, adapted to RFP requirements.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-001 | The RFP (§3.1) states useable area of "approximately 13,000 sq ft" while Appendix B shows a building footprint of approximately 130 ft × 100 ft = 13,000 sq ft for the New North Shop only, but the overall site plan shows 235 ft total width including Old North Shop. It is unclear whether "13,000 sq ft" refers only to the addition or includes Old North Shop area. | RFP §3.1 ("approximately 13,000 sq ft useable area") | App B floor plan (130 ft × 100 ft = 13,000 sq ft New North Shop; additional Old North Shop area) | Datasheet (building area attribute); Specification REQ-001 (structural scope boundary) | PROPOSAL: 13,000 sq ft refers to the New North Shop addition only. Old North Shop renovation is a separate scope element. | TBD |
| CON-002 | The RFP §3.4 lists steel plating in concrete "at strategic locations to accommodate track and packer type heavy equipment" while Appendix B shows specific plate locations in the floor plan. It is unclear whether the Appendix B plate pattern is prescriptive or illustrative. | RFP §3.4 (performance intent — accommodate track/packer equipment) | App B (specific plate locations shown) | Specification REQ-003; Datasheet (steel plate embedments attribute) | PROPOSAL: Treat Appendix B as illustrative/conceptual. Structural Engineer to confirm final plate locations and sizing during design, with Owner review. | TBD |
| CON-003 | The scope boundary for Old North Shop renovation work is not consistently delineated between design scope (DEL-002-12) and investigation/assessment scope. Specification REQ-008 includes the renovation; Specification Scope section excludes "construction execution" but renovation involves assessment of existing structure which blurs the line between design and investigation. Procedure Step 7 describes assessment activities that may exceed the normative specification scope. [Lensing: F-003] | Specification REQ-008 (renovation included in scope) | Specification Scope ("construction execution" excluded); Procedure Step 7 (assessment activities) | Specification REQ-008; Specification Scope; Procedure Step 7 | PROPOSAL: Clarify that the structural assessment of the existing Old North Shop mezzanine is within the design scope of DEL-002-12 (investigation necessary to inform renovation design), while physical renovation construction is excluded (covered by PKG-011). | TBD |

---

*This guidance document was enriched by Pass 3 (Semantic Lensing). Items tagged [Lensing: ...] trace to warranted items in _SEMANTIC_LENSING.md. Considerations and trade-offs are based on the accessible sources. Items labeled ASSUMPTION or TBD require human confirmation or further source information.*
