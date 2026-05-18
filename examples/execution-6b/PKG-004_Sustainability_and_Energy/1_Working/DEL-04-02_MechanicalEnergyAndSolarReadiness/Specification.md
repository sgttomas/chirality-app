# Specification — DEL-04-02: Mechanical Energy and Solar Readiness

---

## Scope

### What This Deliverable Covers

DEL-04-02 is the **mechanical engineer's energy efficiency and solar readiness narrative** for the Penhold PSB proposal. It forms part of the Design Brief (RFP Section 7.1.2, discipline sub-brief 4 — Mechanical), which is evaluated as part of OBJ-004 (5 pts). The narrative must explain the *why* behind mechanical system choices from an energy performance perspective, not just enumerate systems.

**In scope:**

1. High-efficiency HVAC system selection rationale — equipment types, efficiency targets (COP, SEER, AFUE equivalents), and zone-specific strategies
2. Heat recovery opportunities — apparatus bay exhaust heat recovery, ventilation heat recovery (HRV/ERV), domestic hot water heat recovery
3. Ventilation energy optimization — demand-controlled ventilation (DCV), HRV/ERV coverage, zone-specific ventilation strategies per Addendum 03 requirements
4. Domestic hot water efficiency — high-efficiency water heater selection rationale; solar thermal rough-in provisions
5. Solar-ready roof provisions — structural and mechanical rough-in for future solar PV or solar thermal; orientation rationale per Addendum 03 (flat/south/west/southwest)
6. Energy metering and monitoring — whole-building metering; sub-metering strategy; building controls provisions
7. Energy code compliance pathway — NECB or equivalent; efficiency targets relative to code baseline
8. Cross-discipline coordination notes — alignment with DEL-04-01 (envelope), DEL-04-03 (electrical solar), and DEL-02-04 (mechanical concept)
9. Maintainability tie-in — noting how energy-efficient systems are designed for practical maintenance (coordinated with DEL-05-03)

### What This Deliverable Excludes

- Detailed HVAC design (sizing calculations, duct layout, equipment schedules) — belongs to 100% Detailed Design phase
- Detailed structural design for solar panel mounting — belongs to DEL-02-03 (Structural Concept Narrative) and subsequent detailed structural design
- Electrical solar provisions detail (inverter specifications, combiner boxes, disconnect sizing, wiring) — belongs to DEL-04-03 (Electrical Energy Efficiency)
- Building envelope thermal performance targets and air barrier detail — belongs to DEL-04-01 (Building Envelope and Energy Strategy)
- Life cycle assessment (LCA) or embodied carbon analysis — not required by RFP SOW-0012
- Mechanical systems maintainability detail (equipment access clearances, maintenance schedules) — belongs to DEL-05-03 (Mechanical Maintainability)
- Cold Storage building mechanical energy provisions — Cold Storage is intentionally unheated; not in scope for this narrative

**Boundary note — Generator energy interaction:** The backup generator (diesel standby, per Addendum 03) interacts with the overall facility energy budget (generator fuel consumption, generator-served loads during outages, and potential impact on energy metering strategy). Datasheet Conditions acknowledges this interaction. The narrative should include a brief statement of how the generator's energy interaction is addressed (e.g., whether generator fuel consumption is included in or excluded from the energy efficiency analysis, and whether generator-served loads affect the baseline energy budget). ASSUMPTION: a brief scoping statement is sufficient at proposal stage; detailed generator energy analysis is deferred to detailed design. Source: Datasheet.md Conditions "Backup Generator" row; Addendum 03 §1; Decomposition §4.

---

## Requirements

| Req ID | Requirement Statement | Source | Verification Method |
|---|---|---|---|
| **R-MEL-01** | The narrative shall address high-efficiency HVAC equipment selection, including the basis for equipment type selection (e.g., heat pump vs. gas furnace) and target efficiency ratings (COP, SEER, or AFUE as applicable) | RFP SOW-0012; OBJ-004; Decomposition DEL-04-02 description | Narrative review: equipment type and efficiency rationale present |
| **R-MEL-02** | The narrative shall address heat recovery opportunities specific to this facility type, including at minimum: (a) ventilation heat recovery for occupied zones, and (b) the energy trade-off in apparatus bay exhaust streams (contamination limits HRV applicability) | Addendum 03 §1 (apparatus bay direct exhaust); Decomposition DEL-04-02 description | Narrative review: heat recovery opportunities identified with rationale for applicability or exclusion |
| **R-MEL-03** | The narrative shall address apparatus bay ventilation energy strategy per Addendum 03 — direct exhaust ventilation (2 apparatus per bay) — and explain how energy losses are minimized or offset given contamination constraints | Addendum 03 §1; Decomposition §4 | Narrative review: apparatus bay exhaust energy strategy explicitly addressed |
| **R-MEL-04** | The narrative shall address PW bay ventilation energy strategy per Addendum 03 — general ventilation for occasional vehicle idling and very occasional welding — including demand-controlled ventilation approach | Addendum 03 §1; Decomposition §4 | Narrative review: PW bay demand-controlled ventilation strategy present |
| **R-MEL-05** | The narrative shall address domestic hot water efficiency, including water heater type, target efficiency rating, and solar thermal rough-in provisions (pipe sleeves or conduit pathways from roof to mechanical room for future solar thermal loop) | Decomposition DEL-04-02 description (DHW efficiency; solar-ready provisions) | Narrative review: DHW efficiency rationale and solar thermal rough-in described |
| **R-MEL-06** | The narrative shall address solar-ready roof provisions per Addendum 03, specifically: (a) structural loading allowance for future solar panels coordinated with DEL-02-03, (b) mechanical rough-in provisions (pipe sleeves, conduit pathways), and (c) roof orientation rationale aligned to flat/south/west/southwest per Addendum 03 | Addendum 03 §1 (solar-capable roofing); Decomposition §4 Addendum 03 summary and DEL-04-02 description | Narrative review: all three solar-ready elements present (structural, rough-in, orientation); Addendum 03 requirement explicitly cited |
| **R-MEL-07** | The narrative shall address energy metering and monitoring provisions, including at minimum: (a) whole-building metering (electricity and gas), and (b) a statement of sub-metering strategy and building controls/BEMS provisions | Decomposition DEL-04-02 description (energy metering and monitoring provisions) | Narrative review: metering and monitoring approach described |
| **R-MEL-08** | The narrative shall reference the applicable energy code compliance pathway (NECB or equivalent), state the presumed edition (ASSUMPTION: NECB 2020 as adopted by Alberta), and state the design's relationship to the code baseline (prescriptive compliance, performance pathway, or enhancement beyond code). If pursuing a performance pathway or claiming enhancement beyond code, the narrative shall state the target percentage improvement over the NECB baseline (e.g., "X% improvement over NECB prescriptive baseline") so the claim is verifiable, not only a statement of intent. | RFP SOW-0012; Decomposition DEL-04-02 description; Semantic lensing items A-002, F-001 | Narrative review: (a) code reference and compliance approach present; (b) if enhancement beyond code is claimed, a quantitative or semi-quantitative target is stated; (c) the stated pathway is technically credible for the proposed systems (reviewer confirms the pathway is achievable, not merely aspirational) |
| **R-MEL-09** | The narrative shall include explicit cross-references to DEL-02-04 (Mechanical Concept Narrative), DEL-04-01 (Building Envelope and Energy Strategy), and DEL-04-03 (Electrical Energy Efficiency), noting alignment and any coordination dependencies | RFP Section 7.1.2 multi-discipline brief requirement; Decomposition _REFERENCES.md | Narrative review: cross-references to three related deliverables present |
| **R-MEL-10** | The narrative shall be written in clear, professional language suitable for a multi-disciplinary RFP evaluation committee, including non-technical reviewers; technical terms shall be defined on first use; the emphasis shall be on rationale ("why") not only description ("what") | RFP Section 7 presentation; OBJ-004 evaluation context | Readability review by proposal manager: language appropriate for target audience |
| **R-MEL-11** | All assumptions made in the narrative (e.g., NECB edition, equipment type, solar technology preference) shall be explicitly labeled ASSUMPTION | SPEC invariant (source-anchored with explicit assumptions) | Narrative review: ASSUMPTION labels present for all inferred or unconfirmed content |
| **R-MEL-12** | The narrative shall address fill station DHW interaction: whether the two 2-inch water fill stations (one per bay type, per Addendum 03) require warm-water service and, if so, how fill station hot water demand is accounted for in the DHW efficiency analysis. If warm-water service is not required, the narrative shall state this explicitly. | Addendum 03 §1 (fill stations); Datasheet.md Conditions "Fill Stations" row | Narrative review: fill station DHW interaction addressed (either demand included in DHW analysis or explicitly excluded with rationale) |
| **R-MEL-13** | The narrative shall address bay sump energy implications: whether bay sumps (required in all bays per Addendum 03 for snow melting and minor washing) are actively heated and, if so, how sump heating energy is accounted for in the energy efficiency analysis. If sumps are passively drained (no active heating), the narrative shall state this explicitly. | Addendum 03 §1 (sumps); Datasheet.md Conditions "Bay Sumps" row | Narrative review: bay sump energy interaction addressed (either heating load included or passive drainage stated) |

---

## Standards

| Standard | Applicability | Reference Status |
|---|---|---|
| **NECB (National Energy Code of Canada for Buildings)** | Primary energy code compliance baseline for Alberta commercial buildings; specific edition TBD at detailed design — ASSUMPTION: NECB applicable | ASSUMPTION: applicable; edition TBD |
| **Alberta Building Code (ABC)** | Provincial building code; adopts and may modify NECB provisions; AHJ-specific requirements apply | ASSUMPTION: applicable; clause-level requirements location TBD |
| **ASHRAE 62.1** | Ventilation and indoor air quality — minimum ventilation rates for apparatus bays, PW bays, offices, residential quarters | ASSUMPTION: likely applicable as reference standard; clause-level requirements location TBD |
| **ASHRAE 90.1** | Energy standard for buildings — reference for HVAC and water heating efficiency targets where NECB prescriptive may be supplemented | ASSUMPTION: likely applicable as reference standard; location TBD |
| **NFPA 1 / NFPA 13** | Fire station apparatus bay requirements — may impose ventilation requirements superseding energy optimization; coordination with fire protection design required | ASSUMPTION: NFPA standards applicable to fire station apparatus bay design; clause-level requirements location TBD |

---

## Verification

| Verification Check | What to Verify | Responsibility | Acceptance Criteria |
|---|---|---|---|
| **Requirements Coverage** | All R-MEL-01 through R-MEL-13 addressed in the narrative. Each requirement's verification method must produce a recorded pass/fail result (not only a qualitative review). For R-MEL-06 (solar-ready provisions), acceptance requires individually verifying three sub-elements: (a) structural loading allowance, (b) mechanical rough-in provisions, (c) orientation rationale. | Mechanical Lead + Design Manager | All 13 requirements confirmed covered with pass/fail recorded for each; no gaps. R-MEL-06 sub-elements (structural, rough-in, orientation) each individually verified. |
| **Addendum 03 Integration** | Solar-capable roof orientation, apparatus bay direct exhaust strategy, PW bay general ventilation, fill station DHW implications all addressed | Proposal Manager + Mechanical Lead | Addendum 03 checklist: all relevant items explicitly addressed |
| **Cross-Discipline Alignment** | Narrative is consistent with DEL-02-04 (mechanical concept), DEL-04-01 (envelope targets), DEL-04-03 (electrical solar provisions); no terminology or value conflicts. Per R-MEL-09, verify that explicit cross-references to all three deliverables (DEL-02-04, DEL-04-01, DEL-04-03) are present by ID and that each cross-reference confirms alignment or identifies coordination dependencies. | Design Manager | Cross-reference check: (a) DEL-02-04 cross-reference present and aligned; (b) DEL-04-01 cross-reference present and aligned; (c) DEL-04-03 cross-reference present and aligned; each verified individually by deliverable ID. Conflict Table in Guidance.md updated if unresolved conflicts found |
| **Code Compliance Credibility** | NECB compliance pathway is credible and feasible; the stated pathway (prescriptive vs. performance) is technically achievable for the proposed systems and climate zone; efficiency targets cited are achievable with commercially available equipment; if enhancement beyond code is claimed, the percentage improvement target is realistic | Mechanical Lead | Technical review: (a) code reference correct (NECB edition stated); (b) equipment specs realistic; (c) compliance pathway technically credible for the proposed building type, climate, and systems |
| **Assumption Labeling** | All inferred or unconfirmed content is labeled ASSUMPTION | Design Manager | Review: no unsupported assertions presented as facts |
| **Readability and Audience Fit** | Language is clear, professional, and appropriate for a multi-disciplinary evaluation committee | Proposal Manager | Readability review: pass |

---

## Documentation

### Required Artifacts

| Artifact | Format | Status |
|---|---|---|
| **Mechanical Energy Efficiency and Solar Readiness Narrative** | Markdown (.md) or equivalent — submitted as part of proposal PDF | To be produced by Mechanical Engineer |

### Source Materials Required for Production

| Material | Format | Source Location | Notes |
|---|---|---|---|
| RFP — Owner Statement of Requirements (Appendix A) | PDF | Project source documents | Reference OSR energy/sustainability clauses |
| Addendum 03 (Jul 31, 2024) | PDF | Project source documents | Reference solar-capable roof provisions; ventilation requirements |
| Functional Program (Appendix B) | PDF | Project source documents | Reference operational profile (apparatus bay occupancy, DHW demand, etc.) |
| DEL-02-04 (Mechanical Concept Narrative) | Markdown | PKG-002 deliverable folder | Cross-reference for mechanical systems baseline |
| DEL-04-01 (Building Envelope and Energy Strategy) | Markdown | PKG-004 sibling deliverable | Cross-reference for envelope thermal targets driving mechanical loads |
| DEL-04-03 (Electrical Energy Efficiency) | Markdown | PKG-004 sibling deliverable | Cross-reference for solar-ready electrical provisions to coordinate with mechanical rough-in |
