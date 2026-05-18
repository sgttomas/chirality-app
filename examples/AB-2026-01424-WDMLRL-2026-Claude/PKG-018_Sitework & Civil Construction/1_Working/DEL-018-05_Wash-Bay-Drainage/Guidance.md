# DEL-018-05 | Wash Bay Drainage & Mud Sump — Guidance

---

## Terminology Conventions

The following terms are used consistently throughout the four deliverable documents (Datasheet, Specification, Guidance, Procedure). Where prior drafts used variant terms, this section establishes the canonical vocabulary. [Enrichment: B-003, B-004]

| Canonical Term | Definition | Replaces / Clarifies |
|----------------|-----------|----------------------|
| **Wash water** | Water used in the wash bay to clean equipment, together with any entrained sediment, mud, equipment wash residue, or petroleum traces. This is the primary liquid managed by the drainage system. | Replaces inconsistent use of "effluent", "wash bay effluent", "discharge", and "sediment-laden water". The term "wash water" is preferred in these documents because it is descriptively neutral. Note: in regulatory submissions, the applicable regulatory term (e.g., "effluent", "wastewater", "non-domestic wastewater") should be used as required by the governing authority. |
| **Removable-cover sump** / **Open-top sump** | The two sump access configurations under consideration: (a) open-top sump with no cover, or (b) sump with a removable precast or steel cover. | Replaces inconsistent use of "open-top or removable-cover", "sump cover or top treatment", and similar variants. The specific configuration is TBD pending civil/plumbing design. |

---

## Purpose

DEL-018-05 exists to manage wash water from the enclosed wash bay (DEL-011-05) — a single 24'-wide bay designed for washing large landfill equipment such as motor scrapers. Without a functional drainage system, wash operations would result in uncontrolled water pooling inside the building, potential structural damage to the floor, and unmanaged discharge of sediment-laden wash water onto the site — which is an active landfill with environmental compliance obligations.

The mud sump performs the primary settling function: sediment, mud, and debris carried by wash water collect in the sump rather than discharging uncontrolled to the surrounding environment. The excavator-accessible design means accumulated material can be removed periodically without specialized pump equipment, using the landfill's existing heavy equipment fleet.

Sources: RFP SS3.4; OBJ-004 (Decomposition SS5); Decomposition Vocabulary Map ("Exterior sump for wash bay effluent, cleanable by excavator"); _CONTEXT.md.

---

## Principles

### 1. Exterior Sump is an Explicit Owner Requirement — Not a Design Choice

The requirement for a mud sump external to the building, accessible by excavator, is explicitly stated by the Owner in RFP SS3.4. This is not a design option to be reconsidered. The design team must locate the sump on the exterior, adjacent to the wash bay, with sufficient access clearance for an excavator bucket to reach the sump interior.

Source: RFP SS3.4: "Mud sump from wash bay on exterior of building for clean out with excavator."

### 2. Civil Design Governs Drainage Grades — This Deliverable Follows

The drainage grades, invert elevations, and swale layout that support positive flow from the wash bay floor drain to the exterior mud sump are established in the civil design package (DEL-005-02, DEL-005-03 — PKG-005). DEL-018-05 is a construction deliverable; it executes what the civil and plumbing design packages specify. The General Contractor must obtain and follow the IFC drawings before commencing this work.

Source: RFP SS3.3.2 / SOW-0018; _DEPENDENCIES.md (DRAINAGE-DESIGN-001).

### 3. Sequencing — After Site Grading

Drainage construction must follow completion of DEL-018-02 (Site Grading & Landscaping) to ensure that established site grades inform the mud sump excavation depth and drainage pipe invert levels. Installing the sump before final grades are confirmed risks misalignment with the drainage plane.

Source: _DEPENDENCIES.md: "DEL-018-02 — Site Grading & Landscaping Complete — Drainage design depends on site grades."

### 4. Environmental Compliance is a Key Driver

The project site is an active regional landfill. Environmental compliance (OBJ-004) is explicitly listed as an objective served by this deliverable. Uncontrolled discharge of wash water containing sediment, petroleum residue, or equipment fluids could create regulatory liability. Early engagement with environmental regulators regarding discharge management requirements is recommended.

**Rationale for regulatory uncertainty:** The RFP does not explicitly require an environmental discharge permit for the mud sump, and whether one is required depends on factors that have not yet been determined, including: (a) whether the wash water is classified as "non-domestic wastewater" or "stormwater" under Alberta Environment and Protected Areas (AEPA) frameworks; (b) whether the mud sump is considered a "treatment" facility or simply a containment/settlement device; (c) whether wash water from the sump (or any overflow) ultimately reaches a watercourse, groundwater, or remains contained on the landfill site; and (d) whether the landfill's existing environmental approvals already cover wash water management. These factors can only be resolved through a regulatory scoping inquiry with the applicable authority. See Conflict Table CF-002 for the specific conflict between _DEPENDENCIES.md and the RFP. [Enrichment: C-001]

Source: OBJ-004 (Decomposition SS5); _DEPENDENCIES.md: "ENV-PERMIT-001 Environmental discharge permit — Pending. May require regulatory approval."

### 5. Interface with Plumbing Scope Requires Coordination

The floor drain(s) within the wash bay connect to plumbing scope items managed under PKG-006 (Plumbing Design) and may interface with PKG-014 (Plumbing & Water Systems Installation). The boundary between DEL-018-05 (drainage infrastructure, exterior mud sump) and DEL-014-04 (floor drains and sump drains in repair bays) must be clearly established during design. The wash bay floor drain shown on App B (Plumbing) connects to the exterior mud sump and is within DEL-018-05 scope per SOW-0027b.

Source: App B (Plumbing); SOW-0027b vs. SOW-0045 (repair bay sump drains); Decomposition PKG-006 and PKG-014 descriptions.

---

## Considerations

### Sump Sizing

The RFP does not specify mud sump dimensions or capacity. ASSUMPTION: sizing should account for the volume of sediment produced by motor-scraper-class equipment washing over a reasonable cleanout interval (frequency TBD). The civil/plumbing engineer should size the sump to avoid cleanout intervals that are impractically frequent while keeping the sump excavatable by a standard hydraulic excavator bucket.

**Framework for evaluating sump sizing adequacy:** The engineer should consider the following factors when proposing a sump size, and the Owner should confirm the operational assumptions before design is finalized: [Enrichment: D-003]

- **Equipment wash frequency:** How often is the wash bay expected to be used? (e.g., daily, weekly, seasonally). The Owner should define the anticipated wash frequency based on fleet operations. TBD.
- **Sediment loading rate:** What volume of sediment per wash event is expected for motor-scraper-class equipment? ASSUMPTION: this depends on equipment type, operating conditions (landfill environment implies high soil/mud loading), and wash method (pressure washer). TBD — engineer to estimate based on industry precedent or Owner experience.
- **Target cleanout interval:** What is an acceptable interval between excavator cleanouts? The Owner should define this based on operational convenience, cost of cleanout mobilization, and seasonal access constraints (winter excavation may be impractical). TBD.
- **Sump dead volume:** The portion of sump capacity below the pipe invert that is always submerged and not available for sediment accumulation. The effective sediment storage volume is the total sump volume minus the dead volume.
- **Factor of safety:** ASSUMPTION: sump should be oversized relative to the minimum calculated volume to account for variability in wash frequency and sediment loading.

Until these inputs are resolved, the sump capacity remains TBD in the Datasheet and the adequacy of the proposed design cannot be verified per Specification REQ-001.

### Frost Protection

The site is in Alberta (Camrose County), subject to significant frost depth. ASSUMPTION: the mud sump must be constructed to withstand frost heave, and the drainage pipe connecting the floor drain to the sump must be buried below frost depth or insulated. The specific frost depth should be confirmed from the geotechnical report (required per RFP SS3.3.2 / SOW-0001).

### Excavator Access Clearance

The excavator-cleanout requirement implies spatial constraints around the sump. ASSUMPTION: a minimum clearance envelope consistent with a compact or mid-size excavator must be maintained on at least one side of the sump. The civil layout plan should confirm this clearance does not conflict with the cement pad shown on App B immediately adjacent to the east face of the building.

**Long-term access protection:** The design team should consider whether future site development could encroach on the excavator access zone around the sump. If there is a risk that future construction, storage, or grading could compromise access, a maintenance easement or exclusion zone notation on the site plan is recommended. This would protect long-term maintainability and should be coordinated with the Owner/site planner. [Enrichment: E-002]

Source: App B (Shop) — "CEMENT PAD" label shown adjacent to east face of building near wash bay mud sump position.

### Sediment Disposal

Material cleaned from the mud sump is expected to contain sediment, equipment wash residue, and potentially petroleum-bearing material given the wash bay's heavy equipment context. ASSUMPTION: disposal of sump cleanout material may be subject to environmental regulation.

**Disposal pathway considerations:** The design team and Owner should determine the disposal pathway for sump cleanout material during the design phase, not defer it entirely to operations. Key questions include: [Enrichment: X-001]

- **On-site disposal:** Can the sediment be disposed of within the landfill itself? This depends on whether the material is classified as inert fill or as regulated waste (e.g., petroleum-contaminated soil) under Alberta's waste classification framework.
- **Waste characterization:** If the wash water contacts petroleum-bearing equipment, the settled sediment may require characterization testing (e.g., leachate extraction analysis) before disposal. The frequency and trigger conditions for characterization should be defined.
- **Regulatory authority:** The applicable waste classification and disposal regulations should be identified as part of the environmental regulatory scoping recommended in Principles item 4 and Conflict Table CF-002.

The contractor should flag the sediment disposal pathway during design review so that the operational procedures can be established before the sump is placed in service.

### Water Tap in Wash Bay

The plumbing drawing (App B Plumbing) shows a water tap and pressure washer reel inside the wash bay. The wash water from pressure washing is a primary source of sump loading. ASSUMPTION: design of the floor drain and connection pipe should account for pressure washer flow rates to avoid hydraulic surcharge.

Source: App B (Plumbing).

---

## Trade-offs

| Trade-off | Option A | Option B | Evaluation Criteria | Notes |
|-----------|----------|----------|---------------------|-------|
| Sump access configuration | Open-top sump (no cover) | Removable-cover sump (precast or steel cover) | Open-top simplifies excavator access; removable-cover sump reduces odour and is safer for personnel. Decision by engineer — TBD | See Terminology Conventions for canonical terms |
| Sump construction | Cast-in-place concrete | Precast concrete structure | CIP allows custom sizing; precast is faster to install. Site conditions (geotechnical report) may influence choice — TBD | |
| Discharge arrangement | Sump with no overflow (excavator cleanout only) | Sump with engineered overflow to further treatment or approved discharge point | See evaluation rationale below [Enrichment: F-004] | Environmental permitting determines which is acceptable — TBD |
| Pipe burial depth | Minimum frost depth | Deeper with insulation | Deeper is more reliable but costlier; insulation may allow shallower burial — TBD pending geotechnical and civil design | |

**Discharge arrangement evaluation rationale:** The choice between a no-overflow sump and an engineered overflow depends on the following factors, which should be evaluated by the civil engineer in consultation with the environmental consultant: [Enrichment: F-004]

- **Hydraulic capacity under peak flow:** If the pressure washer flow rate exceeds the sump's hydraulic throughput capacity (or if stormwater enters the sump area), a no-overflow design could result in backup into the building. The engineer should assess peak inflow rates.
- **Environmental risk of overflow:** If an overflow is provided, the discharge point and any treatment requirements depend on the regulatory scoping outcome (see Principles item 4 and CF-002). Discharging to the ground surface at a landfill site may require environmental approval.
- **Operational consequence of no overflow:** If the sump has no overflow, the only management path is excavator cleanout. This means the sump must be sized to contain all wash water volume between cleanout events, including any event where the sump is near capacity. The risk of overflow during a high-volume wash event must be assessed.
- **Regulatory acceptability:** The regulatory scoping (CF-002) will determine which configuration is permissible. If the regulatory authority requires containment, a no-overflow design may be mandated regardless of hydraulic considerations.

Until the regulatory scoping is complete, neither option can be definitively selected.

---

## Examples

No project-specific examples are available in the accessible source materials for this deliverable. General design precedents for exterior mud sumps at equipment wash bays are common in the heavy civil and landfill facility sector; however, specifics for this project must derive from the civil and plumbing IFC drawings (TBD).

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|--------------------|--------------|
| CF-001 | Scope boundary of wash bay floor drain: SOW-0027b (DEL-018-05 / PKG-018, General Contractor) vs. SOW-0045/SOW-0046 (DEL-014-04 / PKG-014, Plumbing Contractor). The floor drain inside the wash bay could reasonably fall under either scope. The Specification (REQ-002) does not currently condition acceptance on CF-001 resolution, creating a potential enforcement gap. [Enrichment: D-001] | Decomposition SOW-0027b: "floor drains" listed under PKG-018 | Decomposition SOW-0045: "Install sump drains in repair bays" (PKG-014); SOW-0046: "Install floor drains throughout shop" (PKG-014) | Specification REQ-002; Procedure Step 1.3 | PROPOSAL: The wash bay floor drain and its connection to the exterior mud sump are within DEL-018-05 scope per the explicit language of SOW-0027b. General shop floor drains (SOW-0046) and repair bay sump drains (SOW-0045) are PKG-014 scope. Confirm during contract award and design coordination. Document resolution as a prerequisite to construction (Procedure Step 1.3). | TBD |
| CF-002 | Environmental discharge management requirement: _DEPENDENCIES.md lists ENV-PERMIT-001 as a pending upstream dependency, but the RFP does not explicitly require an environmental discharge permit for the mud sump. It is unclear whether a permit is legally required for this facility type in Alberta. See Principles item 4 for rationale on the factors driving this uncertainty. [Enrichment: C-001] | _DEPENDENCIES.md: ENV-PERMIT-001 listed as upstream dependency | RFP: no explicit discharge permit requirement stated | Specification REQ-009; Procedure Prerequisites | PROPOSAL: Conduct early regulatory scoping with Alberta Environment and Protected Areas (AEPA) or the applicable regulatory authority to determine if a permit or approval is required for the wash bay wash water discharge arrangement. Document the outcome before finalizing the drainage design. | TBD |
| CF-003 | ENV-PERMIT-001 conditionality inconsistency: Specification Documentation section treats the environmental permit as conditional ("if required"), while _DEPENDENCIES.md lists ENV-PERMIT-001 as a pending upstream dependency without the "if required" qualifier. This inconsistency means audit coverage for environmental compliance is ambiguous — it is unclear whether the permit is a hard prerequisite or a conditional item. [Enrichment: X-005] | Specification Documentation section: "Environmental discharge permit or equivalent regulatory confirmation (ENV-PERMIT-001) — if required" | _DEPENDENCIES.md: "ENV-PERMIT-001 Environmental discharge permit — Pending" (no conditional qualifier) | Specification Documentation; Procedure Prerequisites; Verification table REQ-009 | PROPOSAL: Resolve via the regulatory scoping recommended in CF-002. Once the scoping determines whether a permit is required, update both Specification and _DEPENDENCIES.md (by the appropriate agent) to use consistent language. Until resolved, treat ENV-PERMIT-001 as conditional in these production documents and note the inconsistency. | TBD |
