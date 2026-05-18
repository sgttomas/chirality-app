# Guidance — DEL-016-01: Overhead Cranes (Two 5-Tonne Units)

**Document Type:** Guidance (Directional)
**Deliverable ID:** DEL-016-01
**Package:** PKG-016 — Crane & Lifting Equipment
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Revision:** R1 — 2026-02-26 (4_DOCUMENTS Pass 3 — Semantic Lensing Enrichment)

---

## 1. Purpose

This document explains why the two 5-tonne overhead cranes are required, what decisions should guide their specification and procurement, and what trade-offs and risks the project team should be aware of. It is intended for the design-builder's project manager, the crane contractor, and Camrose County's project representative.

The cranes are a critical infrastructure component of the New North Shop addition. They support shop operations by providing safe, efficient overhead lifting of heavy maintenance equipment components, engine assemblies, and large landfill machinery parts. Without operational cranes, the maintenance shop cannot function as intended for the County's heavy equipment fleet.

**Objectives served:**
- **OBJ-001:** Deliver a fully functional maintenance shop with all specified equipment operational.
- **OBJ-004:** Install and commission all mechanical systems to operational readiness (cranes are a primary material handling system).
- **OBJ-005:** Install and commission all electrical systems to operational readiness (crane power circuit is part of the electrical scope).

*(Source: Decomposition DEL-016-01 entry; Objective Mapping.)*

---

## 2. Principles

### 2.1 Cranes Are a Long-Lead Item — Procure Early

Overhead cranes, particularly 5-tonne industrial units, typically carry lead times of 8–12 weeks from order to delivery. (Source: _DEPENDENCIES.md, Critical Path Assessment.) In a project with a December 31, 2026 deadline, late procurement is among the highest risk factors for this deliverable. The crane specification and RFQ should be issued as early as possible — ideally concurrent with structural design of the runway (DEL-002-07) — rather than after the building structure is complete.

**Procurement timeline guidance:** Given the 8–12 week lead time and the December 31, 2026 completion deadline, the project team should establish procurement milestones working backwards from the required installation date. TBD: The Project Manager should establish specific target dates for the following milestones:
- RFQ issuance to crane suppliers
- Supplier selection and purchase order placement (must occur no later than 12 weeks before the target installation date to account for maximum lead time)
- Equipment delivery to site
- Installation start (dependent on structural runway and building envelope completion)

These milestones should be integrated into the overall project schedule and tracked as critical-path items.

*(Source: _DEPENDENCIES.md Critical Path Assessment; enriched per D-002: procurement timeline milestones added.)*

### 2.2 Structural and Crane Design Must Be Coordinated Before Either Is Finalized

The crane runway structural design (DEL-002-07, PKG-002) depends on crane wheel loads, span, and rail requirements. These cannot be determined without first selecting a crane model or at minimum obtaining preliminary data from candidate suppliers. A coordination loop between the structural engineer and the crane contractor/supplier is essential before the structural runway drawings are finalized for construction. Failure to do this will either result in an under-designed runway or expensive rework.

*Guidance: Issue a request for crane supplier information (RFI or pre-qualification RFQ) early enough that wheel load data can feed into structural design. Do not finalize the structural runway design without confirmed crane load data.*

### 2.3 Electrical Load Data Must Feed Electrical Design

The electrical design package (PKG-004 / DEL-004 series) must include correctly sized circuits for both cranes (SOW-0059). Crane motor power requirements are not available until a crane model is selected or at least a candidate class is established. The Crane Contractor must provide electrical load data early in the design phase.

### 2.4 The D-001 Gantry / Overhead Crane Disambiguation

Decision D-001 in the project decomposition clarifies that the "Gantry" labels visible on the Appendix B floor plan refer to the same equipment as the two 5-tonne overhead cranes on trolley (SOW-0067). The floor plan labels are a naming discrepancy in the conceptual drawings, not a separate equipment type. This deliverable is for top-running overhead cranes on a permanent structural runway — not free-standing gantry cranes. The structural design (DEL-002-07) and this deliverable must be consistent on this point.

*(Source: Decomposition Decision Log D-001.)*

### 2.5 Alberta Safety Code Compliance Is Non-Negotiable

Overhead cranes in Alberta are subject to Alberta Safety Code requirements for lifting equipment. Safety code inspections and permits must be planned as part of the installation and commissioning sequence. Non-compliance will block occupancy and commissioning sign-off.

---

## 3. Considerations

### 3.1 Crane Configuration Options

The RFP specifies "5-tonne overhead cranes on a trolley." This is consistent with a single-girder or double-girder top-running overhead bridge crane. Considerations for the detailed specification:

- **Single-girder vs. double-girder:** Single-girder cranes are lighter, lower cost, and require less headroom but typically have lower duty ratings and shorter service lives under heavy use. Double-girder cranes offer greater headroom under the hook (because the hoist rides on top of the girder), higher duty ratings, and longer service life but at higher cost and weight. ASSUMPTION: For a landfill heavy equipment maintenance shop handling large machine components, double-girder configuration may be appropriate, but this is a design decision to be made with input from the County on anticipated lift frequency and load types.

- **Duty class:** TBD — the crane duty class (CMAA Specification 70 or equivalent) must be determined with input from Camrose County on anticipated lift frequency and load types. A maintenance shop handling heavy equipment may warrant Class C (moderate service) or Class D (heavy service). Specifying too low a duty class will result in premature wear and potential safety issues. This decision cannot remain as an ASSUMPTION through procurement — it must be resolved before the RFQ is issued. (Source: ASSUMPTION; enriched per B-004: duty class decision flagged as requiring resolution before procurement.)

- **Hook height:** With a 35-foot ceiling, the effective hook height will be constrained by the depth of the runway beam and hoist. This parameter must be optimized in coordination with the structural engineer.

### 3.2 Two Cranes in One Bay — Layout Coordination

The Appendix B floor plan shows both 5-tonne cranes running on parallel tracks in the main shop area of the New North Shop (130 ft x 100 ft building). If both cranes share the same runway rails (anti-collision may be required) or run on separate independent runways, this affects the structural design significantly.

ASSUMPTION: Two separate runways (four rails total) is likely the intended configuration given the floor plan layout. This must be confirmed with the structural engineer before runway design is finalized.

**Rationale for independent runway preference:** Independent runways (four rails) are preferred over shared runways (two rails with anti-collision) for the following reasons: (a) independent runways eliminate the risk of crane-to-crane collision entirely, removing the need for anti-collision systems and their associated maintenance and potential failure modes; (b) independent operation allows both cranes to be used simultaneously without operational restrictions, which is important for a maintenance shop that may need to service multiple pieces of equipment concurrently; (c) independent runways simplify maintenance — one crane can be taken out of service without affecting the other. The trade-off is higher structural cost (four runway beams and associated columns vs. two). This cost difference must be weighed against the safety and operational benefits. (Source: ASSUMPTION — standard industrial practice; enriched per X-001: rationale for independent runway preference added.)

### 3.3 Schedule Criticality

The cranes are on the project critical path. The sequence of dependencies is:
1. Structural runway design (DEL-002-07) must incorporate crane load data.
2. Structural runway must be installed (PKG-011).
3. Building envelope must be closed (PKG-011 / SITE-001).
4. Electrical circuit must be available (PKG-015 / ELEC-001).
5. Crane installation and commissioning can then proceed.

Any delay in crane procurement or structural runway design will directly impact the December 31, 2026 project completion date.

### 3.4 Warranty and Guarantee Period

The RFP §2.10 establishes a two-year guarantee period following the Construction Completion Certificate (CCC). Crane equipment is included in this guarantee. The Crane Contractor and the overall project contractor must ensure that the crane supplier's warranty terms align with this two-year guarantee period, and that manufacturer warranty documentation is obtained at commissioning.

*(Source: RFP §2.10.)*

---

## 4. Trade-offs

| Trade-off | Option A | Option B | Guidance |
|-----------|----------|----------|----------|
| Single-girder vs. double-girder | Lower cost, less headroom under hook, lower duty ratings | Higher cost, more headroom under hook, higher duty ratings, longer life | ASSUMPTION: For a heavy equipment maintenance shop, double-girder may offer better long-term value. Confirm with County based on anticipated use frequency and load types. |
| Crane duty class | Class B (light service) — lower cost | Class C or D (moderate/heavy) — higher cost, longer life | ASSUMPTION: Specify based on realistic lift frequency. Under-specifying increases maintenance cost and safety risk over the equipment's service life. |
| Pre-engineered package vs. custom | Faster delivery, standard components | Longer lead time, can optimize for specific hook height and span | ASSUMPTION: Standard pre-engineered package likely sufficient for this application given standard 5-tonne capacity. |
| Shared runway vs. independent runways | Lower structural cost if one runway, anti-collision system needed | Higher structural cost for two runways, simpler and safer operation (see Section 3.2 rationale) | ASSUMPTION: Independent runways are safer and operationally simpler; confirm with structural engineer and County. |

---

## 5. Examples

No project-specific examples available from accessible sources. The following are provided as general industry context only and are labeled ASSUMPTION.

- ASSUMPTION: A 5-tonne, 20–25 ft span, single-girder overhead crane is a common configuration for maintenance shops of this size. Exact span to be set by structural engineer based on building column spacing.
- ASSUMPTION: Hook height with a 35-foot ceiling, allowing for runway beam depth and hoist equipment, might yield approximately 28–30 feet of hook height. This figure is illustrative only; detailed engineering is required. (Note: This estimate is also recorded in Datasheet Section 2.2 as an ASSUMPTION datum per E-001.)

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|--------------------|--------------|
| CONF-016-01-01 | Floor plan (App B) labels cranes as "Gantry" but RFP §3.4 and SOW-0067 describe them as "overhead cranes on a trolley." These are different crane types with different structural implications. | App B (Shop) floor plan — label "Gantry" / "5 Ton Crane" | RFP §3.4 "2 – 5-tonne overhead cranes on a trolley"; Decomposition SOW-0067 | Crane type selection, structural runway design (DEL-002-07), installation method | PROPOSAL: Follow Decomposition D-001 — cranes are top-running overhead bridge cranes on trolley (not free-standing gantry). Decomposition Decision D-001 was made by the decomposition author to resolve this. Confirm with County/Structural Engineer. (D-001 surfaced for human ruling.) | TBD |
| CONF-016-01-02 | Two cranes in same bay — whether they share one pair of runway rails or use two independent runway sets is not specified in RFP or App B. This significantly affects structural design and cost. | App B — two crane symbols in one bay | RFP §3.4 — "2 – 5-tonne overhead cranes on a trolley" (no further detail) | DEL-002-07 (Crane Support Structure Details), this deliverable's installation scope, anti-collision requirements (REQ-016-01-15) | PROPOSAL: Confirm with Structural Engineer and County before finalizing structural runway design. ASSUMPTION: independent runways preferred for safety (see Section 3.2 rationale). | TBD |

---

## Pass 3 Enrichment Log

The following semantic lensing items were incorporated or addressed in this revision:

| ItemID | Action Taken |
|--------|-------------|
| B-004 | Incorporated: Duty class decision in Section 3.1 flagged as TBD requiring resolution before procurement; strengthened from ASSUMPTION to explicit action required |
| D-001 | Incorporated: CONF-016-01-01 in Conflict Table updated with note that D-001 is surfaced for human ruling |
| D-002 | Incorporated: Procurement timeline milestone guidance added to Section 2.1 with TBD for specific target dates |
| X-001 | Incorporated: Rationale for independent runway preference added to Section 3.2, explaining safety and operational reasoning |
