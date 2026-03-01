# Guidance — DEL-014-03 Bulk Water Fill System

**Document Type:** Guidance (directional)
**Deliverable ID:** DEL-014-03
**Package:** PKG-014 — Plumbing & Water Systems Installation
**Revision:** R1 — 2026-02-26
**Status:** SEMANTIC_READY
**Enrichment Pass:** P3 (Semantic Lensing applied)

---

## Purpose

The West Dried Meat Lake Regional Landfill Maintenance Shop operates in a rural location without municipal water service. All facility water must be trucked to site and stored on-site in the 50,000L cistern (DEL-014-01). The Bulk Water Fill System (DEL-014-03) is the primary interface between bulk water delivery vehicles and the on-site cistern. Without a proper high-volume external fill capability, the County's operational program for the maintenance shop — including vehicle washing, washroom facilities, and general service water — cannot be sustained.

The explicit requirement for this system was stated in RFP S3.4: "Bulk water fill. With high volume pump for external filling." It is further captured in OBJ-004, which calls for commissioning all water storage systems to operational readiness, with the bulk water fill named explicitly.

This guidance document provides directional context for the design and installation teams. It does not replace the IFC drawings or plumbing specifications produced under PKG-006.

---

## Principles

### P-1: External Fill Is the Primary Water Supply Input
The bulk water fill system is not a secondary or convenience feature — it is the sole mechanism for replenishing the cistern at this off-grid site. Reliability, flow rate adequacy, and ease of use by water haulers are therefore primary design considerations.

**Source:** RFP S3.1 (facility context), S3.4 (design requirement); ASSUMPTION on operational criticality.

### P-2: High Volume Is the Explicit Requirement
The RFP uses the phrase "high volume pump for external filling." This implies the system must accommodate rapid fill cycles typical of bulk water delivery operations (tanker trucks). Designs that would result in slow fill rates (hours to fill a 50,000L cistern) are inconsistent with the owner's stated intent.

**Source:** RFP S3.4.

### P-3: Design Leads Installation
DEL-014-03 is an installation deliverable. The fill system design — including pump sizing, pipe sizing, connection type, backflow prevention, and freeze protection details — must be resolved in PKG-006 (Plumbing Design, DEL-006-04) before installation begins. The Plumbing Contractor shall not deviate from IFC drawings without documented approval.

**Source:** RFP S3.3.2 (IFC drawing requirement); ASSUMPTION on sequencing.

### P-4: Scope Boundary with DEL-014-01
DEL-014-03 (bulk water fill) and DEL-014-01 (cistern and distribution) share a physical interface at the cistern. The 2.5" filling connection and 100 LPM internal pump described in RFP S3.4 are assigned to DEL-014-01/SOW-0042 (internal service water distribution). The bulk fill pump and its fill line are DEL-014-03/SOW-0044 scope. The interface point (connection at cistern) must be coordinated between the two deliverables to avoid gap or overlap.

**Source:** RFP S3.4; decomposition SOW table (SOW-0042 vs SOW-0044).

### P-5: Electrical Coordination Is Pre-Condition to Rough-In
The pump motor requires a dedicated electrical circuit under DEL-015-04. Failure to coordinate motor electrical specifications (voltage, amperage, phase) before rough-in could result in a rework scenario. Coordination should occur at the subcontractor kick-off stage.

**Source:** ASSUMPTION — standard multi-trade coordination requirement.

---

## Considerations

### C-1: Freeze Protection in Alberta Climate
The exterior fill point and any exposed piping or pump components are subject to sustained sub-zero temperatures in winter. Design considerations include:
- Drain-back provision so the fill line does not hold standing water when not in use
- Heated enclosure or heat trace for the pump and exposed piping
- Insulated fill point cover or protective housing

The plumbing engineer is responsible for specifying the freeze protection strategy. Installation must comply with that strategy.

**Source:** ASSUMPTION — site location in Alberta Central region; no explicit freeze protection specification found in available RFP sources. Specification TBD in PKG-006 design.

### C-2: Access for Water Delivery Vehicles
The exterior fill point must be accessible to bulk water tanker trucks. Site planning should confirm that the truck access route and turning radius are compatible with the fill point location shown on Appendix B (Plumbing). The gravel driving surface design (DEL-018-03) and pad layout should be coordinated with the fill point location.

**Source:** R-06 (App B Plumbing — fill point shown on north face of building); ASSUMPTION on truck access coordination.

### C-3: Pump Performance Documentation
The "high volume" pump specification in the RFP is qualitative. The plumbing engineer must translate this into a quantitative pump specification (LPM, head, motor size). The selected pump's performance curve should demonstrate adequate flow for filling a 50,000L cistern within a reasonable operating window.

**Source:** RFP S3.4; ASSUMPTION on documentation requirement.

### C-4: Backflow Prevention
Where the fill system connects to the cistern (which is a non-potable service water supply), backflow prevention requirements depend on the hazard classification under the Alberta Plumbing Code (National Plumbing Code as adopted in Alberta). The plumbing engineer shall determine the required protection level. A minimum of a double-check valve assembly or equivalent is common for this type of application.

**Source:** ASSUMPTION — Alberta Plumbing Code requirement (specific clause location TBD). *(Terminology harmonized per Semantic Lensing C-002.)*

### C-5: Commissioning Alignment with DEL-020-01
The bulk water fill system must be operationally ready for inclusion in the building systems commissioning (DEL-020-01). The Plumbing Contractor shall ensure the system is test-ready before the commissioning agent's scheduled visit. The commissioning authority for DEL-014-03's performance acceptance should be clarified — see Consideration C-6 below.

**Source:** Decomposition DEL-020-01 (Building Systems Commissioning); OBJ-004.

### C-6: Commissioning Authority Clarification
Procedure.md references both "Plumbing Contractor / Commissioning Agent" (Phase 5) and DEL-020-01 (Building Systems Commissioning, Step 5.6) but does not clarify which party has final authority to issue the performance acceptance verdict for the bulk fill system. Possible models:

- **Self-commissioning by Plumbing Contractor** with results reviewed by Owner/PM
- **Independent commissioning agent** (under DEL-020-01) issues the performance verdict
- **Both:** Plumbing Contractor performs functional tests; commissioning agent validates and issues formal acceptance

**TBD — PM to clarify which model applies and confirm the authority for issuing the conclusive performance verdict for DEL-014-03.**

**Source:** Procedure.md Phase 5; Guidance C-5; Decomposition DEL-020-01. *(Semantic Lensing D-002)*

### C-7: Schedule and Cost Risk from Unresolved Design TBDs
Multiple critical design parameters remain TBD pending plumbing engineering (PKG-006 IFC design):
- Pump flow rate (LPM) — blocks pump selection and procurement
- Fill connection size and type — blocks hardware procurement
- Freeze protection method — blocks material procurement and installation planning
- Backflow device type — blocks device procurement

These unresolved items have the potential to delay procurement start and compress the installation schedule against the **December 31, 2026 project completion deadline**. Early resolution through PKG-006 design completion is recommended. The PM should track these TBDs as schedule risk items.

**Source:** Datasheet.md Attributes (multiple TBDs); Specification.md Requirements (TBD items); RFP S3.1 (completion deadline). ASSUMPTION on schedule risk implication. *(Semantic Lensing F-003)*

### C-8: Seasonal Operations and Winterization Lifecycle Concern
The bulk fill system will be used seasonally in Alberta's climate. Post-commissioning, the Owner will be responsible for operating the system, including winterization procedures (draining fill lines, protecting the pump and exterior connection from freeze damage during periods of non-use). While an O&M manual is required (Specification Documentation section), Guidance should flag that winterization is not merely a maintenance task but a **lifecycle-critical operational concern** for this system. Failure to winterize correctly could result in freeze damage requiring costly repair and loss of water supply capability.

The O&M manual should include a clear, step-by-step seasonal winterization and spring re-commissioning protocol, and the Owner should be briefed on these procedures during handoff.

**Source:** Specification.md Documentation (O&M Manual requirement); site location in Alberta Central region. ASSUMPTION on seasonal operational criticality. *(Semantic Lensing E-001)*

---

## Trade-offs

### T-1: Pump Location (Indoor vs. Outdoor)
Locating the pump indoors (inside the utility room adjacent to the cistern) provides better freeze protection and easier maintenance access, but requires longer fill line runs to the exterior connection point. Locating closer to the exterior wall reduces pipe run length but increases freeze exposure risk for the pump. The plumbing engineer should resolve this trade-off in the IFC design.

**Note:** This trade-off concerns the *pump* location. The exterior fill *connection point* location is established as the north face of the building per REQ-014-03-03 / Appendix B. These are distinct items — see Conflict Table C-004 below. *(Semantic Lensing E-003)*

**Source:** ASSUMPTION — no explicit pump location specified in RFP or Appendix B beyond "exterior filling."

### T-2: Fill Connection Type
The choice of fill connection type (cam-lock, threaded, storz, or similar) affects compatibility with local water hauling contractors' equipment. A non-standard connection could cause operational difficulty. The Owner/County should be consulted on the preferred connection standard used by local bulk water suppliers.

**Source:** ASSUMPTION — not addressed in available RFP sources. TBD — owner input recommended.

### T-3: Dedicated Fill Line vs. Shared Line with Internal Distribution
Running a dedicated fill line solely for the bulk fill function versus tying into the internal distribution piping (DEL-014-01) has implications for flow capacity, backflow prevention complexity, and future maintenance. A dedicated fill line is the cleaner design but increases material cost. The plumbing engineer should confirm the preferred approach.

**Source:** ASSUMPTION — not explicitly resolved in RFP sources.

---

## Examples

No project-specific examples are available in accessible source documents.

ASSUMPTION: For rural Alberta facilities of similar type (cistern-fed maintenance shops), a common approach is an exterior-grade pump mounted inside a heated enclosure, connected to a 2-3" fill line terminating in a cam-lock fitting at a ground-level bollard-protected fill post. This is provided for illustrative context only and is not prescriptive.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| C-001 | Bulk fill pump flow rate is unspecified. RFP S3.4 states "high volume pump for external filling" without a specific LPM figure. The 100 LPM pump stated in S3.4 is associated with the internal cistern distribution pump (SOW-0042), not the bulk fill pump. | RFP S3.4 (SOW-0042 — "100 LPM" / "2.5 inch cistern filling connection") | RFP S3.4 (SOW-0044 — "high volume pump for external filling" — no specific rate) | Specification.md REQ-014-03-02; Datasheet.md Attributes | Plumbing engineer to specify in IFC design; recommend Owner confirm minimum acceptable fill cycle time for tanker operations | TBD |
| C-002 | Fill connection size for the bulk fill exterior point is not specified in available sources. The 2.5" connection stated in RFP S3.4 is for the internal service water distribution, not the bulk fill point. | RFP S3.4 (SOW-0042 — "2.5 inch cistern filling connection") | RFP S3.4 (SOW-0044 — no connection size stated) | Specification.md REQ-014-03-03; Datasheet.md Attributes | Plumbing engineer to specify; Owner to confirm preferred connection standard matching local bulk water hauler equipment | TBD |
| C-003 | Bidirectional operation ambiguity. Datasheet Primary Function and Specification REQ-014-03-01 use language suggesting the system may support both filling the cistern AND extracting water from it to vehicles ("delivery or extraction"). Guidance P-1 frames the system exclusively as a cistern replenishment mechanism ("sole mechanism for replenishing the cistern"). The RFP language "for external filling" is ambiguous — it could mean filling *from* outside (delivery to cistern) or filling an external vehicle *from* the cistern. | Datasheet Attributes — Primary Function ("fill the cistern or take on water"); Specification REQ-014-03-01 ("delivery or extraction") | Guidance P-1 ("sole mechanism for replenishing the cistern") | Datasheet.md Primary Function; Specification.md REQ-014-03-01; Guidance.md P-1 | Owner/PM to confirm operational intent: is the system for cistern replenishment only, or must it also support water extraction to vehicles? | TBD |
| C-004 | Potential confusion between fill connection point location and pump location. REQ-014-03-03 specifies the fill connection point on the north face of the building (per Appendix B). Guidance T-1 discusses pump location as an unresolved indoor-vs-outdoor trade-off. These are distinct items, but documentation could be read as conflating them. | Specification REQ-014-03-03 ("north face of the building" — fill connection point) | Guidance T-1 ("Pump Location Indoor vs. Outdoor" — pump, not connection point) | Specification.md REQ-014-03-03; Guidance.md T-1; Datasheet.md Fill Point Location | Plumbing engineer (IFC design) to confirm pump location separately from fill point location | TBD |

---

## Semantic Lensing Enrichment Log (Pass 3)

| ItemID | Action Taken |
|---|---|
| C-002 | Plumbing code terminology harmonized to "Alberta Plumbing Code (National Plumbing Code as adopted in Alberta)" in C-4 |
| D-002 | New consideration C-6 added: commissioning authority clarification |
| E-001 | New consideration C-8 added: seasonal operations and winterization lifecycle concern |
| E-003 | Conflict Table entry C-004 added: fill point location vs. pump location clarification; T-1 annotated |
| E-004 | Conflict Table entry C-003 added: bidirectional operation ambiguity |
| F-003 | New consideration C-7 added: schedule/cost risk from unresolved design TBDs |
