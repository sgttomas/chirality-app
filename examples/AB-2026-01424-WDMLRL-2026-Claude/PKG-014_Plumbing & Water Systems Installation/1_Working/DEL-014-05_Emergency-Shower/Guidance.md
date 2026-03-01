# Guidance — DEL-014-05 Emergency Shower

---

## Purpose

The emergency shower exists to protect workers at the West Dried Meat Lake Regional Landfill Maintenance Shop from serious injury in the event of chemical or hazardous substance exposure. The landfill maintenance shop environment involves fuels, lubricants, hydraulic fluids, solvents, and potentially other industrial chemicals. Rapid and effective decontamination — within seconds of exposure — is a life-safety function.

This deliverable directly supports:

- **OBJ-007**: Maintain safe site operations under Prime Contractor designation for the full project duration with zero lost-time incidents. (Decomposition §5)
- **OBJ-001**: Deliver a code-compliant, fully functional maintenance shop addition. (Decomposition §5)
- **OBJ-004**: Install and commission all mechanical, plumbing, and water storage systems to operational readiness. (Decomposition §5)

The RFP does not describe the emergency shower in detail beyond its inclusion in SOW-0048 and its appearance on the conceptual plumbing drawing (App B-Plumb, R-06). The Plumbing Contractor and plumbing designer are responsible for ensuring the installation meets all applicable codes and standards in the IFC design.

---

## Terminology Note (Enriched per B-004)

Throughout the deliverable documents, the term **"emergency shower"** is used as the primary name for this unit. The unit is assumed to be a **combination shower/eyewash** (ASSUMPTION) pending resolution of Conflict Table entry CF-002. Until CF-002 is resolved:

- Use **"emergency shower"** as the default short-form reference across all documents.
- Where the combination nature is relevant to a specific discussion (e.g., flow rate calculations that must account for both shower and eyewash heads, or procurement specifications), use **"emergency shower (combination shower/eyewash — ASSUMPTION; see CF-002)"**.
- Do not use "shower-only" or "combination unit" in isolation without referencing the CF-002 status.

This convention applies to: Datasheet.md (Attributes row "Unit type"), Specification.md (Scope), and Procedure.md (Steps 1, 6, 9).

---

## Principles

**P-1 — Safety equipment must always be operational.**
An emergency shower that is installed but non-functional provides no protection. The unit must be fully operational at or before occupancy. All upstream dependencies (cistern fill, distribution pump, drainage) must be confirmed operational before the emergency shower is commissioned.

Source: OBJ-007; ASSUMPTION — consistent with Alberta OH&S Code requirements for emergency washing facilities (location TBD in accessible sources).

**P-2 — Location determines accessibility.**
The value of an emergency shower depends entirely on a worker being able to reach it within 10 seconds (ASSUMPTION: per ANSI/ISEA Z358.1, approximately 15-16 m / 50-55 ft unobstructed travel distance; location TBD in accessible sources). The conceptual drawing places the unit near the south shop area adjacent to the wash station. The IFC design must confirm this location provides adequate coverage of the main work areas.

Source: App B-Plumb (R-06); ASSUMPTION re: 10-second rule.

**P-3 — The water supply system is a limiting upstream dependency.**
This emergency shower draws from the cistern-fed distribution system (DEL-014-01). If the cistern is empty or the distribution pump is not running, the emergency shower cannot function. This is a design constraint that must be addressed in the facility operating procedures and maintenance program.

**Consequence of unavailability (Enriched per F-004):** If the emergency shower becomes non-functional (cistern empty, pump failure, supply line damage, freeze event), the facility may be in non-compliance with Alberta OH&S Code requirements (ASSUMPTION; location TBD in accessible sources). Potential consequences include: (a) regulatory shutdown risk — the OH&S authority could order work to stop if no emergency washing facility is available for chemical hazard areas; (b) worker safety exposure — personnel handling hazardous substances would lack immediate decontamination capability; (c) liability exposure for the Owner under occupational health and safety legislation. These consequences reinforce the importance of redundancy or backup planning in the facility operating procedures. The Owner should consider whether a backup water supply protocol or portable emergency eyewash station is warranted during periods when the cistern system is unavailable.

Source: _DEPENDENCIES.md; Decomposition §7 (PKG-014 deliverable relationships); ASSUMPTION re: OH&S regulatory consequences.

**P-4 — Tepid water is a design requirement, not an option.**
Cold water can cause hypothermia during a 15-minute flush in an Alberta climate, and may cause involuntary curtailment of flushing before the required duration is complete. The plumbing designer must confirm whether the cistern water temperature is adequate or whether a thermostatic mixing valve is required. See Conflict Table entry CF-001.

Source: ASSUMPTION — ANSI/ISEA Z358.1 and Alberta OH&S Code Part 16 tepid water requirements (location TBD in accessible sources).

**P-5 — This is a Safety Code permit item.**
Plumbing work requires Alberta Safety Code permits. All inspections must be coordinated with the County project representative. Non-permitted work will not be accepted.

Source: RFP §3.3.2 (SOW-0007, SOW-0084, SOW-0085).

---

## Considerations

**C-1 — Combination shower/eyewash unit.**
The conceptual drawing shows a single "Emergency Shower" symbol. The applicable standard (ASSUMPTION: ANSI/ISEA Z358.1) recommends that an emergency shower be co-located with an emergency eyewash where the hazard warrants it. In an industrial maintenance shop environment, a combination unit is the common practice. The plumbing designer should confirm whether a combination unit (shower + eyewash) is required by Alberta OH&S Code Part 16 for this facility type. If a combination unit is required, the flow rates and supply connection must account for both shower and eyewash simultaneous flow.

Source: ASSUMPTION; App B-Plumb (R-06) shows shower only; Alberta OH&S Code Part 16 (location TBD).

**C-2 — Non-potable water supply.**
The emergency shower is supplied from the cistern (non-potable water system). Alberta OH&S Code and ANSI/ISEA Z358.1 generally permit non-potable water for emergency shower use, provided water quality does not itself pose a hazard. The plumbing designer should confirm water quality acceptability for emergency shower use.

Source: ASSUMPTION — standard industry practice and code provisions (location TBD in accessible sources).

**C-3 — Freeze protection.**
While the building is heated, supply piping in unheated wall cavities or near exterior walls could be at risk of freezing. The plumbing designer must ensure the supply branch to the emergency shower is located in a heated zone or is otherwise protected.

Source: ASSUMPTION — Alberta climate requirement; building envelope heating per RFP §3.4.

**C-4 — Coordination with floor drain.**
The conceptual drawing shows a drain immediately below the emergency shower (App B-Plumb, R-06). The floor drain capacity must be adequate to handle the emergency shower flow rate (ASSUMPTION: minimum 75.7 LPM) without flooding the floor area. This should be verified in the IFC design against DEL-014-04 drain specifications.

Source: App B-Plumb (R-06); _DEPENDENCIES.md (DEL-014-04 upstream).

**C-5 — Access during construction and occupancy.**
The emergency shower must not be blocked by construction materials, equipment, or permanent fixtures. The Plumbing Contractor should flag the clearance zone early in construction coordination meetings.

Source: REQ-ES-009; ASSUMPTION.

**C-6 — Annual testing obligations.**
After handover, the Owner will likely be required under Alberta OH&S Code to test the emergency shower at regular intervals (ASSUMPTION: weekly activation and annual performance test). The Contractor should provide the Owner with operating and maintenance instructions that include the recommended testing protocol.

Source: ASSUMPTION — Alberta OH&S Code Part 16 (location TBD in accessible sources); OBJ-007.

**C-7 — Upstream readiness signaling (Enriched per B-003).**
Procedure prerequisites require DEL-014-01 (Cistern & Distribution) to be roughed-in and pressure tested before the emergency shower supply branch can be connected. However, no formal mechanism currently exists for confirming that DEL-014-01 has reached the required readiness state. The project management team should define an upstream-ready signal or handoff protocol — for example, a written confirmation or status update from the DEL-014-01 responsible party that rough-in is complete and pressure testing has passed. Without a defined handoff protocol, the emergency shower installation team may commence work prematurely or experience delays waiting for informal confirmation.

Source: Procedure.md Prerequisites (DEL-014-01 row); _DEPENDENCIES.md; ASSUMPTION re: sequencing protocol.

**C-8 — Post-commissioning monitoring period (Enriched per D-003).**
The current documents proceed from commissioning test (Procedure Step 9) directly to Owner orientation (Step 10) with no defined period to confirm sustained performance. For life-safety equipment, a post-commissioning monitoring period may be warranted — for example, a 30-day period during which the emergency shower is activated weekly and performance is logged, before the unit is considered fully accepted by the Owner. This is particularly relevant given the cistern-fed supply system, which introduces variables (cistern level, pump reliability, temperature consistency) that a single commissioning test may not fully validate. The Owner and contract terms should determine whether such a monitoring period is required.

Source: ASSUMPTION — industry best practice for life-safety equipment acceptance; Specification Verification table; Guidance P-1.

---

## Trade-offs

**T-1 — Combination unit vs. shower-only unit.**
A combination shower/eyewash unit costs more but provides eye and face protection in addition to full-body decontamination. In an industrial maintenance environment, the combination unit is almost always warranted. If the OH&S Code requires it, there is no trade-off — it is mandatory. The guidance is to default to a combination unit unless the code review confirms it is not required.

Source: ASSUMPTION; C-1 above.

**T-2 — Tepid water system cost vs. OH&S compliance risk.**
Installing a thermostatic mixing valve adds cost and complexity to the supply system. Not installing one creates a compliance risk if the cistern water temperature falls below the required tepid range. The guidance is that the designer should specify a thermostatic mixing valve unless it can be demonstrated that the cistern water consistently remains within the tepid range under all operating conditions. See CF-001.

Source: ASSUMPTION; P-4 above.

**T-3 — Location flexibility.**
The conceptual drawing shows a single location. If the IFC design determines that coverage of all hazard areas requires a different or additional location, the scope may need to be adjusted. The Plumbing Contractor should raise this with the plumbing designer at IFC design stage.

Source: App B-Plumb (R-06); P-2 above.

**T-4 — Lifecycle cost implications (Enriched per C-003).**
The documents above address installation cost trade-offs (T-1, T-2), but the Owner should also consider ongoing lifecycle costs post-handover: (a) annual performance testing labor (ASSUMPTION: required per Alberta OH&S Code; location TBD), (b) weekly activation testing labor, (c) replacement parts and consumables (e.g., eyewash head covers, activation valve seals), (d) thermostatic mixing valve maintenance (if installed per CF-001), and (e) potential water treatment or filtration costs if water quality degrades. These ongoing costs may influence the choice of unit (premium vs. basic models), the selection of a thermostatic mixing valve with accessible maintenance features, and the Owner's maintenance budget planning. This consideration is relevant for Owner orientation (Procedure Step 10).

Source: ASSUMPTION — standard lifecycle cost considerations for installed safety equipment; Guidance C-6.

---

## Examples

No worked examples are available from accessible sources. TBD — examples of compliant emergency shower installation configurations may be documented here once IFC design drawings are issued.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CF-001 | Tepid water delivery requirement: the RFP and conceptual drawings do not specify whether a thermostatic mixing valve is required. Alberta OH&S Code Part 16 and ANSI/ISEA Z358.1 (both ASSUMPTION — location TBD) require tepid water. The cistern is a cold-water source and may not consistently deliver tepid water without a mixing valve. | Specification.md REQ-ES-005; Guidance.md T-2 | App B-Plumb (R-06) — no mixing valve shown; RFP §3.4 — no specific mention | Specification REQ-ES-005; Datasheet Attributes row "Water supply temperature"; Procedure Steps 2 and 7; Specification Documentation item 7 (TMV documentation) | Plumbing designer to confirm in IFC design; if OH&S Code requires tepid water (ASSUMPTION: it does), a thermostatic mixing valve shall be included in the IFC drawings and procurement | TBD |
| CF-002 | Combination shower/eyewash vs. shower only: the conceptual drawing (App B-Plumb, R-06) shows a single emergency shower symbol. Alberta OH&S Code Part 16 (ASSUMPTION — location TBD) may require a combination shower/eyewash unit for an industrial shop environment. | App B-Plumb (R-06) — "Emergency Shower" label, single symbol | Alberta OH&S Code Part 16 (ASSUMPTION — location TBD) | Specification REQ-ES-001; Datasheet Attributes row "Unit type"; Procedure Steps 1, 2, 6, 9; Guidance Terminology Note | Plumbing designer to confirm unit type in equipment submittal; default to combination unit unless code review confirms shower-only is sufficient | TBD |
| CF-003 | Standards hierarchy when ANSI/ISEA Z358.1 and Alberta OH&S Code Part 16 differ on specific numeric requirements (e.g., tepid water range, flow rate, flush duration): the hierarchy statement ("Alberta OH&S Code governs") appears in REQ-ES-001 but was not consistently reinforced in downstream requirements prior to enrichment. Enrichment has added Standards Hierarchy cross-references to REQ-ES-004, REQ-ES-005, REQ-ES-006, REQ-ES-007, and REQ-ES-009. The conflict remains open until the applicable standards are confirmed and any actual discrepancies are identified. (Enriched per F-001) | Specification.md REQ-ES-001 (Alberta governs) | Specification.md REQ-ES-004, REQ-ES-005 (cite ANSI/ISEA Z358.1 values as ASSUMPTION) | Specification Requirements section (all ASSUMPTION-based numeric thresholds); Specification Standards table | Plumbing designer or Alberta OH&S authority to confirm applicable standards and identify any actual discrepancies | TBD |
