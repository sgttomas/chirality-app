# Guidance — DEL-014-01: 50,000L Cistern & Distribution

**Document Type:** Guidance (directional)
**Deliverable ID:** DEL-014-01
**Package:** PKG-014 — Plumbing & Water Systems Installation
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Prepared By:** 4_DOCUMENTS Agent (Pass 1); enriched Pass 3
**Date:** 2026-02-26
**Status:** DRAFT

---

## Purpose

The 50,000L cistern and distribution system is the primary on-site service water supply for the WDMLRL New North Shop. Because the site is a rural landfill location (SW 14–44–21–W4, near Ferintosh, Alberta), there is no stated municipal water connection. The cistern stores water that is brought to site via the bulk water fill system (DEL-014-03) and then distributes it internally for equipment washing, pressure washing, and facility service purposes.

**Note on emergency shower (Lensing Item E-003):** The original draft stated the emergency shower was fed from the cistern supply network (ASSUMPTION). However, Specification Scope explicitly excludes emergency shower plumbing (DEL-014-05). Whether the cistern distribution system feeds the emergency shower is unresolved. See Conflict Table CONF-014-01-03 below.

**Note on water classification (Lensing Items B-003, B-004):** The system is described as "service water distribution" in the RFP. Whether this constitutes potable or non-potable water is unresolved and affects applicable Alberta Safety Code requirements. See Conflict Table CONF-014-01-01 and CONF-014-01-02 below. Until the Owner declares the water quality classification, this document uses the term "service water" consistently.

This deliverable is critical to OBJ-004 (install and commission all mechanical, plumbing, and water storage systems to operational readiness) and contributes to OBJ-001 (fully functional facility that satisfies the County's operational program).

Sources: RFP §3.4; Decomposition §5 (OBJ-001, OBJ-004); _CONTEXT.md

---

## Principles

1. **Minimum volume is a hard floor, not a target.** The RFP specifies "Minimum 50,000 L" (RFP §3.4). The IFC plumbing design should evaluate whether operational demands — particularly wash bay and bulk fill operations — justify a larger cistern. ASSUMPTION: given the industrial nature of the facility (motor scrapers, heavy equipment washing), water demand may be substantial; the minimum should be confirmed against operational duty cycles.

2. **Pump sizing must match distribution demand.** The 100 LPM minimum pump capacity (RFP §3.4) must be sufficient to serve simultaneous service points (pressure washer reel, water taps, and any other downstream users). ASSUMPTION: if multiple service points are used concurrently, the 100 LPM minimum may be a single-point floor; the IFC plumbing design should confirm total simultaneous demand. **Lensing note (Item C-003):** TBD — a demand calculation basis or reference to confirm whether 100 LPM is adequate for simultaneous multi-point demand (pressure washer reel + water taps + emergency shower concurrently) has not been provided. This is a critical operational capacity question. **Proposed authority: IFC Plumbing Designer.**

3. **2.5-inch filling connection is explicitly specified.** This dimension is an Owner-stated requirement (RFP §3.4) and must not be changed without written Owner approval. It likely corresponds to the fill hose or hydrant connection on the bulk water fill truck or system (DEL-014-03). Coordination with DEL-014-03 is essential to confirm coupling compatibility.

4. **Cistern placement drives coordination complexity.** The plumbing drawing (R-06) shows the cistern adjacent to the Utility Room stairwell area. This placement must be coordinated with: structural provisions for tank weight (PKG-002/PKG-011), electrical power supply to the pump (PKG-015/DEL-015-01), and the bulk water fill inlet location (DEL-014-03). Early multi-discipline coordination is important.

5. **Freeze protection is non-negotiable in Alberta.** ASSUMPTION: the cistern and all distribution piping must be protected against freezing. Options include locating the cistern within the heated building envelope, insulating exposed piping, and using heat trace on vulnerable sections. The IFC plumbing design must address this; construction documents must demonstrate compliance with applicable Alberta codes.

Sources: RFP §3.4; R-06 (Plumbing Drawing); Decomposition §7 PKG-014; _DEPENDENCIES.md

---

## Considerations

### Coordination with Bulk Water Fill System (DEL-014-03)
The cistern is filled by the bulk water fill system. The fill inlet must be accessible from the external fill point and the 2.5-inch fill connection must be compatible with the bulk fill pump connection (DEL-014-03). Misalignment between these two deliverables on coupling type or location would prevent the cistern from being filled. This interface must be coordinated at the IFC design stage.

### Coordination with Electrical (DEL-015-01)
The distribution pump requires an electrical power supply. This must be a dedicated circuit confirmed in the electrical design (PKG-004/PKG-015). The pump motor voltage, amperage, and starter requirements are TBD and must be provided to the electrical designer early in the design phase. Failure to coordinate this in time could result in a delay to pump commissioning.

### Cistern Access, Cleaning, and Maintenance
ASSUMPTION: The cistern requires periodic inspection and cleaning. Access provisions (manholes, cleanouts) should be included in the IFC design. The cistern should be sized and positioned to allow future cleaning with standard maintenance equipment. This is not stated in the RFP but is standard practice for potable/service water storage.

**Lensing note (Item X-001):** TBD — guidance on specific access provisions is needed: manhole sizing (e.g., minimum 600 mm per AWWA or applicable standard), cleanout locations, and recommended maintenance/inspection frequency. The current text identifies the need but provides no sizing guidance or standard reference. **Proposed authority: IFC Plumbing Designer / O&M standards.**

### Water Quality
ASSUMPTION: Because this is a service water system at a landfill maintenance shop (not potable drinking water in the traditional sense), full potable water treatment may not be required. However, Alberta Health Services and Alberta Safety Code provisions for non-potable industrial water should be consulted. The cistern supply should not be cross-connected with any potable drinking water supply. Human clarification requested on intended uses (equipment washing vs. washroom fixtures).

**Lensing note (Items B-003, B-004):** The water quality classification question is the most significant unresolved issue for this deliverable. If the cistern feeds washroom fixtures (water tap shown near washroom on R-06), potable water standards may apply, bringing additional treatment, testing, and cross-connection control obligations. Resolution by the Owner / Alberta Health Services is required. See Conflict Table CONF-014-01-01 and CONF-014-01-02.

### Structural Loading
The cistern, when full, represents a significant dead load (50,000L of water = approximately 50 metric tonnes). The structural design (PKG-002/PKG-011) must account for this load whether the tank is above-grade or below-grade. This constraint must be communicated to the structural engineer at the earliest design stage.

### Sequence of Installation
ASSUMPTION: The cistern vessel typically must be placed before floor/wall construction closes around it (if recessed or semi-recessed). The general contractor (building structure, PKG-011) and plumbing contractor must coordinate installation sequence to avoid rework.

### Backflow Prevention and Cross-Connection Control (Lensing Item F-001)
ASSUMPTION: Alberta plumbing code requires backflow prevention on water storage and distribution systems. The IFC design must identify the specific backflow prevention device type(s) and installation locations (e.g., on cistern fill connection, at distribution points). This is a mandatory legal requirement that is not yet addressed in the specification requirements. See REQ-014-01-011 in Specification.

### Cistern Overflow Management (Lensing Item F-002)
ASSUMPTION: Bulk water fill operations create a risk of cistern overflow if the tank is filled beyond capacity. The IFC design should address overflow management through an overflow pipe (routed to the floor drain system, DEL-014-04), a high-level alarm, or both. This is standard practice for bulk water storage installations. See REQ-014-01-012 in Specification.

---

## Trade-offs

| Decision Area | Option A | Option B | Guidance |
|---|---|---|---|
| Cistern sizing | 50,000L (minimum per RFP) | Larger volume for operational buffer | ASSUMPTION: Evaluate water consumption per shift for wash bay and pressure washing before finalizing size. Larger cistern increases cost but reduces fill frequency. **Lensing note (Item C-004):** TBD — a quantitative water demand estimate (litres per shift, fill frequency analysis) is needed to support this trade-off decision. No quantitative basis is currently available. **Proposed authority: Owner / Operations Manager.** Human ruling recommended. |
| Cistern location (above vs. below grade) | Above-grade tank in Utility Room | Partially or fully below-grade | Above-grade simplifies structural loading coordination; below-grade may aid freeze protection but requires excavation and waterproofing. TBD in IFC design. |
| Pump configuration | Single pump (100 LPM) | Duplex pump (redundancy) | RFP mandates single-pump minimum; duplex provides operational redundancy for a working landfill facility. ASSUMPTION: Recommend considering duplex configuration for operational continuity. **Lensing note (Item D-003):** TBD — the trade-off recommendation does not quantify downtime cost or provide a decision framework for single vs. duplex. At a working landfill, loss of service water could affect equipment washing and potentially regulatory compliance (emergency shower, if fed from cistern). **Proposed authority: Owner / Operations Manager.** Human ruling recommended. |
| Fill connection location | Single 2.5" inlet at cistern | Multiple inlets for flexibility | RFP specifies 2.5" connection; number of inlets not specified. Coordinate with DEL-014-03. |

---

## Examples

No worked examples are available from accessible project sources. TBD — examples of comparable rural industrial cistern installations may be provided at human discretion.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-014-01-01 | The intended water quality classification of the cistern system (potable vs. non-potable service water) is not stated. This affects applicable Alberta Safety Code requirements and any treatment requirements. (Lensing Items B-003, B-004) | RFP §3.4 (no water quality classification stated) | Standard Alberta plumbing code practice (location TBD) | Specification REQ-014-01-005, REQ-014-01-006; Guidance Considerations (Water Quality); Datasheet (Downstream consumers) | Owner / Alberta Health Services to declare intended use classification. If washroom fixtures are fed from this cistern, potable water standards likely apply. | TBD |
| CONF-014-01-02 | Whether the distribution system from the cistern feeds the washroom fixtures (which would imply potable standard) or only industrial service points is ambiguous from the plumbing drawing. (Lensing Items B-003, B-004) | R-06 Plumbing Drawing (water tap shown near washroom) | RFP §3.4 (cistern described as "service water distribution") | Specification REQ-014-01-005; Guidance Water Quality | IFC plumbing design to clarify and segregate systems if needed. | TBD |
| CONF-014-01-03 | Whether the emergency shower is fed from the cistern distribution system or from a separate supply is unresolved. Datasheet lists emergency shower as a downstream consumer (ASSUMPTION: combined cold water supply); Guidance Purpose originally assumed cistern supply; but Specification Scope explicitly excludes emergency shower plumbing (DEL-014-05). If DEL-014-05 handles emergency shower plumbing independently, the cistern documents should not assume it as a distribution point. (Lensing Item E-003) | Specification Scope (Out of Scope: "Emergency shower plumbing DEL-014-05") | Datasheet Conditions (Downstream consumers: "emergency shower ASSUMPTION"); original Guidance Purpose (ASSUMPTION: fed from cistern supply network) | Datasheet (Distribution Points, Conditions); Specification Scope; Procedure (commissioning scope) | IFC Plumbing Designer / PM to confirm whether emergency shower is fed from cistern or is an independent system under DEL-014-05. | TBD |
| CONF-014-01-04 | The RFP text "Pump capable of 100 LPM complete with a 2.5 inch cistern filling connection for internal service water distribution" is ambiguous: it is unclear whether the 2.5-inch connection is the external bulk-fill inlet to the cistern (from DEL-014-03) or a pump-side connection. REQ-014-01-003 currently interprets this as the external cistern fill inlet. (Lensing Item E-002) | RFP §3.4 ("Pump capable of 100 LPM complete with a 2.5 inch cistern filling connection") | Specification REQ-014-01-002 and REQ-014-01-003 (current interpretation) | Specification REQ-014-01-002, REQ-014-01-003; Datasheet (Fill connection diameter) | Owner / P.Eng. (RFP interpretation) | TBD |

---

## Lensing Enrichment Traceability (Pass 3)

The following _SEMANTIC_LENSING.md items were applied to this document:

| Item ID | Type | Action Taken |
|---|---|---|
| B-003 | Conflict | Updated Purpose notes and Conflict Table CONF-014-01-01/02 with water quality classification context |
| B-004 | Normalization | Added terminology standardization note to Purpose; aligned "service water" usage |
| C-003 | RationaleGap | Added lensing note to Principle 2 on simultaneous demand calculation gap |
| C-004 | RationaleGap | Added lensing note to Trade-offs row 1 on quantitative demand data gap |
| D-003 | WeakStatement | Added lensing note to Trade-offs row 3 on pump configuration decision framework gap |
| E-003 | Conflict | Added new Conflict Table entry CONF-014-01-03 (emergency shower feed); updated Purpose |
| X-001 | RationaleGap | Added lensing note to Considerations (Cistern Access) on manhole sizing and maintenance rationale gap |
| E-002 | Normalization | Added new Conflict Table entry CONF-014-01-04 (2.5" connection ambiguity) |
| F-001 | MissingSlot | Added new Considerations section on backflow prevention |
| F-002 | MissingSlot | Added new Considerations section on cistern overflow management |
