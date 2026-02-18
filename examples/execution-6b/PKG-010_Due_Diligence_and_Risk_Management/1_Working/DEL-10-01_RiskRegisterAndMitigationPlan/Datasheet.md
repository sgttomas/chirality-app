# Datasheet — Risk Register and Mitigation Plan

**Deliverable ID:** DEL-10-01
**Deliverable Name:** Risk Register and Mitigation Plan
**Package:** PKG-010 — Due Diligence & Risk Management
**Type:** Risk / Register + Narrative
**Responsible Party:** PM + Technical Leads
**Date Generated:** 2026-02-17

---

## Identification

| Attribute | Value |
|-----------|-------|
| **Deliverable ID** | DEL-10-01 |
| **Name** | Risk Register and Mitigation Plan |
| **Parent Package** | PKG-010 — Due Diligence & Risk Management |
| **Discipline(s)** | Project Management, Risk Management |
| **Type** | Risk Register (tabular) + Risk Mitigation Narrative |
| **Responsible Party** | PM + Technical Leads |
| **Anticipated Artifacts** | Risk register (tabular format); risk mitigation narrative |
| **SOW Coverage** | SOW-0028 — Risk register & mitigations |
| **Objective Alignment** | OBJ-008: Manage risk and unknowns transparently |

---

## Attributes

| Attribute | Value |
|-----------|-------|
| **Format** | Tabular register + narrative |
| **Risk Categories** | Design, Site/Environmental, Cost, Schedule, Procurement, Permitting |
| **Risk Rating Scale** | Likelihood: Low / Medium / High; Impact: Low / Medium / High / Critical. Risk Level is a composite L x I rating mapped via the following 3x4 matrix: |

**Risk Level Matrix (L x I):**

| | Low Impact | Medium Impact | High Impact | Critical Impact |
|---|------------|--------------|-------------|----------------|
| **High Likelihood** | Amber | Red | Red | Red |
| **Medium Likelihood** | Green | Amber | Red | Red |
| **Low Likelihood** | Green | Green | Amber | Red |

**Color interpretation:** Red = immediate attention, priority mitigation required; Amber = active monitoring, mitigation planned; Green = accepted, standard monitoring. (See also Procedure Step 2.3.)

| Attribute | Value |
|-----------|-------|
| **Risk Response Types** | Avoid, Reduce, Transfer, Accept |
| **Register Columns** | Risk ID, Category, Risk Description, Likelihood, Impact, Risk Level (L×I), Mitigation Strategy, Residual Risk, Owner, Status |
| **Source Basis** | RFP 2024_004 (Sections 2–9), Addenda 01–03, Decomposition v2.3 (reference report findings as summarized therein) |
| **Governing Scope Item** | SOW-0028 — Produce risk register with mitigation plan |

---

## Conditions

| Condition | Details |
|-----------|---------|
| **Project Type** | Design-Build per CCDC 14-2013 with Supplementary Conditions (Appendix J) |
| **Project Context** | Public Services Building — combined Fire Hall + Public Works Operations facility + Cold Storage building; 12-acre developable site on 20-acre total parcel, Waskasoo Avenue North, Penhold, Alberta |
| **Deliverable Trigger** | Proposal submission requirement under OBJ-008; multi-category risk assessment expected to support evaluator confidence |
| **RFP Authority** | RFP 2024_004 (Jul 10, 2024) with Addenda 01 (Jul 11), 02 (Jul 15), 03 (Jul 31, 2024). Addendum 03 governs where conflicts exist. (Source: Decomposition v2.3 §2) |
| **Program Complexity** | Addendum 03 introduced: 16 ft overhead doors, bay sumps, direct exhaust ventilation, backup generator, 2" fill stations, solar-capable roof, 40 bunker gear lockers, room size ranges, second-storey option — all increasing design and coordination risk surface |
| **Site Constraints** | 12 functional acres; 8 acres in flood fringe (storm pond + dog park); flood zone constraints reduce effective layout area. Wetland boundary constraints from assessment. (Source: Decomposition v2.3 §4) |
| **Geotechnical Basis** | Foundation design and site risk assessment grounded in existing 2021 Geotechnical Investigation Report only; no additional investigation (DEC-013). Full report text not accessible; findings referenced as summarized in Decomposition v2.3. |
| **Environmental Basis** | Desktop Environmental Assessment (Ghostpine); Wetland Assessment and Impact Report available as reference. Full report texts not accessible; implications referenced through Decomposition v2.3 §3. |
| **Key Decision: No Additional Geotech** | DEC-013: No additional geotechnical investigation at proposal stage; risk accepted; no pricing allowance for future investigation. (Source: Decomposition v2.3 §13) |
| **Pickled Sand Storage Removed** | C-10/Addendum 03 §1.2: Pickled sand storage building excluded from this proposal. Reduces one scope/cost risk. |
| **FF&E Treatment** | FF&E not in base cost (Addendum 03 §1.18; DEC-012); $20K cash allowance on Additional Option 6. Pricing risk managed via defined allowance. |
| **Insurance Approach** | CCIP confirmed (DEC-011); contractor arranges and carries project insurance per Appendix J. |
| **Interface Dependencies** | DEL-10-02 (Site Conditions and Due Diligence Summary) provides site/environmental risk inputs to this register |
| **Interface Dependencies** | DEL-01-06 (Pricing Narrative and Assumptions) aligns pricing risks with cost register entries |

---

## Construction

### Risk Register — Column Schema

The tabular Risk Register (final artifact) uses the following column schema:

| Column | Description |
|--------|-------------|
| **Risk ID** | Unique identifier (format: RISK-CCC-NN where CCC = category abbreviation) |
| **Category** | Design / Site-Environmental / Cost / Schedule / Procurement / Permitting (implicit from section headers in register tables below; Category is determined by the section header under which the entry appears rather than a repeated column in each row) |
| **Risk Description** | Factual statement of the risk event and its potential consequence |
| **Likelihood** | Low / Medium / High |
| **Impact** | Low / Medium / High / Critical |
| **Risk Level** | Combined L×I rating (e.g., High-Critical = red; Medium-High = amber; Low-Low = green) |
| **Mitigation Strategy** | Proactive measures to reduce likelihood or impact |
| **Residual Risk** | Likelihood-Impact after mitigation (notation: "Likelihood-Impact" dash-separated, e.g., "Low-Medium" means post-mitigation Likelihood=Low, Impact=Medium) |
| **Owner** | Party accountable for monitoring and executing mitigation |
| **Status** | Active / Mitigated / Closed |

### Risk Register — Current Entries

The following entries are derived from RFP requirements, Addenda 01–03 context, and reference report findings as summarized in Decomposition v2.3. Specific reference report data (geotechnical parameters, wetland boundary coordinates, environmental findings) are noted as **location TBD** pending direct access to source reports.

#### Category: Design

| Risk ID | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Residual Risk | Owner | Status |
|---------|-----------------|-----------|--------|------------|---------------------|---------------|-------|--------|
| RISK-DES-01 | Addendum 03 program additions (16 ft doors, sumps, direct exhaust, generator, fill stations, 40 lockers, solar-ready roof) create coordination complexity across all five disciplines, increasing design iteration risk | High | High | Red | Explicit coordination matrix distributed at project kickoff; lead architect chairs weekly discipline coordination; Addendum 03 requirements mapped to responsible discipline in Decomposition v2.3 SOW-0010 | Medium-Medium | Lead Architect | Active |
| RISK-DES-02 | Room sizing ranges from Addendum 03 leave design latitude but may result in Owner rejection if preliminary layouts fall below the minimum program requirements | Medium | High | Red | Apply minimum sizing as floor constraint; track compliance table against Addendum 03 ranges per room type at each design milestone | Low-Medium | Architect | Active |
| RISK-DES-03 | Second-storey option for shared spaces introduces structural interface complexity; stair/elevator provisions may affect footprint and cost | Medium | Medium | Amber | Evaluate second-storey massing in concept; confirm structural approach with engineer before schematic freeze; document decision and rationale | Low-Low | Architect + Structural Engineer | Active |
| RISK-DES-04 | Intentionally missing functional program dimensions (Addendum 01) may result in undersized spaces if designer assumptions deviate from Owner intent during review | Medium | High | Red | Apply building-code minimum as floor; propose to Owner at concept review stage; document assumptions in design narrative | Low-Medium | Architect | Active |
| RISK-DES-05 | Solar-capable roof orientation requirement (flat/south/west/southwest per Addendum 03 §1.16) may conflict with site layout or building geometry if design is not optimized early | Low | Medium | Green | Confirm solar orientation during site concept design; coordinate roof geometry between architectural and electrical disciplines | Low-Low | Architect + Electrical Engineer | Active |

#### Category: Site/Environmental

| Risk ID | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Residual Risk | Owner | Status |
|---------|-----------------|-----------|--------|------------|---------------------|---------------|-------|--------|
| RISK-SIT-01 | 8 acres of parcel in flood fringe (storm pond + dog park area) reduces functional site area; if flood mapping boundaries are more restrictive than assumed, building footprint may require relocation | Medium | High | Red | Design building and Civil layout on confirmed 12-acre developable envelope per Addendum 03 §1.1; verify flood fringe extents from flood zone mapping reference document (location TBD) | Low-Medium | Civil Engineer + PM | Active |
| RISK-SIT-02 | Wetland constraints from Wetland Assessment may impose buffer requirements that further restrict site layout or access routing | Medium | High | Red | Review Wetland Assessment summary (location TBD; findings referenced in Decomposition v2.3 §3); design site access and parking to respect buffer setbacks; include in civil site concept assumptions | Low-Medium | Civil Engineer | Active |
| RISK-SIT-03 | Desktop Environmental Assessment (Ghostpine) may identify residual contamination or soil quality concerns affecting grading, excavation, or disposal plans | Low | High | Amber | Note findings from Desktop Environmental Assessment (location TBD; referenced in Decomposition v2.3 §3); include soil disposal assumption in pricing narrative; alert PM if findings suggest Phase 2 ESA needed. (Source for risk: secondary source -- Decomposition v2.3 §3 summary; full report location TBD) | Low-Medium | PM + Civil Engineer | Active |
| RISK-SIT-04 | Geotechnical conditions from 2021 report may have changed, or original report may not cover all planned building footprint areas on the 12-acre site | Low | High | Amber | Design based on 2021 Geotechnical Investigation Report findings (DEC-013); document reliance in pricing narrative (DEL-01-06); accept risk of unknown ground conditions at proposal stage. (Source for risk: secondary source -- Decomposition v2.3 §13; full report location TBD) | Low-High | Structural Engineer + PM | Active |
| RISK-SIT-05 | Site grading conditions may require more substantial cut/fill than anticipated, increasing earthworks cost and schedule | Medium | Medium | Amber | Review existing Site Grading documentation (Appendix E; location TBD); include grading assumptions in pricing narrative; include earthworks contingency in cost estimate. (Source for risk: secondary source -- Decomposition v2.3 §3; full report location TBD) | Low-Medium | Civil Engineer + Estimator | Active |
| RISK-SIT-06 | Utility service tie-in complexity (water, sewer, electrical, communications) to site services from Waskasoo Avenue North may exceed allowance | Medium | Medium | Amber | Cash allowance acceptable per Addendum 03 §1.7 (DEC-012); quantify cash allowance in pricing narrative; obtain utility locates early in detailed design. (Source for risk: secondary source -- Decomposition v2.3 §4; Addendum 03 §1.7) | Low-Low | Civil Engineer + Estimator | Active |
| RISK-SIT-07 | Construction-phase safety hazards arising from specialized Addendum 03 installations (apparatus bay direct exhaust at height, sump construction in confined spaces, 16 ft overhead door installation) may require additional safety planning or specialized equipment | Low | High | Amber | Develop construction safety plan addressing specialized installation hazards; confirm subtrade safety certifications for exhaust installation and sump construction; include safety provisions in construction methodology (DEL-07-01). **ASSUMPTION**: Alberta OH&S Legislation applicable for construction-phase safety risk context; not specifically cited in RFP for this deliverable. (Source: Specification Standards table -- Alberta OH&S; Addendum 03 §1.3–§1.5) | Low-Medium | Construction Manager + PM | Active |

#### Category: Cost

| Risk ID | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Residual Risk | Owner | Status |
|---------|-----------------|-----------|--------|------------|---------------------|---------------|-------|--------|
| RISK-CST-01 | Addendum 03 program enhancements (sumps, direct exhaust, generator minimum loads, 40 lockers, fill stations, solar-ready roof) are not fully costed by all estimators, leading to budget underrun vs. actual construction scope | High | High | Red | Reconcile Addendum 03 scope item checklist against estimate line items before pricing submission; confirm all enhancements are costed, even if individual items are small | Low-Medium | Estimator + PM | Active |
| RISK-CST-02 | Market escalation during design and construction phases may erode budget margin | Medium | High | Red | Include escalation contingency in estimate; note in pricing narrative that proposal pricing is valid for the submission period; include escalation assumption in DEL-01-06 | Low-Medium | Estimator | Active |
| RISK-CST-03 | CCIP insurance cost quantification may be imprecise at proposal stage; underpricing CCIP costs reduces margin | Medium | Medium | Amber | Obtain CCIP premium indication from insurer before proposal submission; include in Schedule B General Requirements; note approach in DEL-01-03 | Low-Low | Commercial Lead | Active |
| RISK-CST-04 | Bond cost (Performance Bond 50% + L&M Bond 50%) represents significant line item; surety premium rate changes may affect margin | Low | Medium | Green | Confirm bond cost with surety before submission; include in Schedule B General Requirements; check bond cost inclusion per C-08 | Low-Low | Commercial Lead | Active |
| RISK-CST-05 | Site servicing cash allowance may be insufficient if tie-in costs are higher than assumed (Addendum 03 §1.7 allows cash allowance but does not cap it) | Medium | Medium | Amber | Establish realistic cash allowance based on utility distances; note assumption in DEL-01-06; flag as contingent item for Owner awareness | Low-Low | Estimator | Active |

#### Category: Schedule

| Risk ID | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Residual Risk | Owner | Status |
|---------|-----------------|-----------|--------|------------|---------------------|---------------|-------|--------|
| RISK-SCH-01 | Owner's "not schedule-driven" flexibility may not apply post-award; contractual milestone expectations may be more rigid than anticipated | Low | High | Amber | Clarify schedule expectations at pre-award clarification; include schedule assumptions in DEL-09-01; document design milestone sequence per RFP 7.1.9 | Low-Medium | PM | Active |
| RISK-SCH-02 | Permitting timeline for Alberta occupancy and building permit may be longer than estimated, delaying construction start | Medium | High | Red | Identify AHJ permitting requirements early in detailed design; include permitting lead time in project schedule (DEL-09-01); use concurrent permit review where feasible | Low-Medium | PM | Active |
| RISK-SCH-03 | Discipline coordination delays (5 disciplines producing concept and design brief deliverables in parallel) may compress design review windows | Medium | Medium | Amber | Establish discipline coordination protocol at project kickoff; use BIM or common drawing platform; assign lead architect as coordination single point of contact | Low-Low | Lead Architect | Active |
| RISK-SCH-04 | Long-lead procurement items (overhead doors, generator, HVAC equipment) may delay construction if procurement is not initiated at detailed design stage | Medium | High | Red | Identify long-lead items during mechanical/electrical concept design; flag in procurement plan; initiate procurement at 60% detailed design review milestone | Low-Medium | Construction Manager | Active |

#### Category: Procurement

| Risk ID | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Residual Risk | Owner | Status |
|---------|-----------------|-----------|--------|------------|---------------------|---------------|-------|--------|
| RISK-PRO-01 | Subcontractor availability for specialized trades (apparatus bay exhaust, generator installation, fill station piping, sump construction) may be limited in central Alberta market | Medium | High | Red | Identify and pre-qualify specialty subtrades before proposal submission; confirm availability commitments; list in Appendix I (DEL-01-09) | Low-Medium | Construction Manager | Active |
| RISK-PRO-02 | Material supply chain disruptions for structural steel, overhead doors, or mechanical equipment may cause schedule delay or cost premium | Medium | Medium | Amber | Monitor supply chain conditions; include procurement lead time buffer in schedule; consider allowance for substitution in specification | Low-Low | Construction Manager | Active |
| RISK-PRO-03 | Subtrade pricing provided for proposal may not hold at contract execution due to market conditions | Medium | Medium | Amber | Obtain firm or short-validity subtrade pricing close to submission date; note pricing validity period in DEL-01-06 | Low-Low | Estimator | Active |

#### Category: Permitting

| Risk ID | Risk Description | Likelihood | Impact | Risk Level | Mitigation Strategy | Residual Risk | Owner | Status |
|---------|-----------------|-----------|--------|------------|---------------------|---------------|-------|--------|
| RISK-PER-01 | Building permit application requires complete IFC Detailed Design Package; delays in design completion or AHJ review may push occupancy date | Medium | High | Red | Sequence 100% IFC package per design milestone schedule (DEL-06-02); engage AHJ for pre-application meeting early in detailed design phase | Low-Medium | PM | Active |
| RISK-PER-02 | Environmental or wetland buffer compliance may require additional permitting (Environmental Protection Order, DFO authorization) depending on wetland assessment findings | Low | High | Amber | Confirm regulatory requirements with AHJ and environmental consultant based on Wetland Assessment findings (location TBD); allow permitting lead time in schedule | Low-Medium | PM + Civil Engineer | Active |
| RISK-PER-03 | Occupancy permit and substantial performance certification timing must align with 12-month warranty commencement (RFP 7.6; SC54–SC55) | Low | Medium | Green | Include occupancy permit milestone in project schedule; align commissioning and deficiency closeout sequence with warranty trigger | Low-Low | PM | Active |

---

## References

| Source | Access Status |
|--------|---------------|
| RFP 2024_004 (Jul 10, 2024) — Sections 2–9 (risk themes) | Referenced via Decomposition v2.3 |
| Addendum 01 (Jul 11, 2024) | Referenced via Decomposition v2.3 §4 |
| Addendum 02 (Jul 15, 2024) | Referenced via Decomposition v2.3 §4 |
| Addendum 03 (Jul 31, 2024) | Referenced via Decomposition v2.3 §4 |
| 2021 Geotechnical Investigation Report | Location TBD — not directly accessed; findings context from Decomposition v2.3 |
| Wetland Assessment and Impact Report | Location TBD — not directly accessed; referenced in Decomposition v2.3 §3 |
| Desktop Environmental Assessment (Ghostpine) | Location TBD — not directly accessed; referenced in Decomposition v2.3 §3 |
| Site Grading Documentation (Appendix E) | Location TBD — not directly accessed; referenced in Decomposition v2.3 §3 |
| Flood Zone Mapping for Parcel | Location TBD — not directly accessed; referenced in Decomposition v2.3 §4 |
| Penhold PSB Project Decomposition v2.3 | Fully accessible — primary synthesis source |

---

## TBD Items

- Quantitative risk ratings (numeric probability x consequence) if Owner/proposal team adopts semi-quantitative approach
- **TBD (high priority):** Specific geotechnical parameters (soil bearing capacity, groundwater depth, frost depth) from 2021 Geotechnical Investigation Report -- not directly accessed. These essential facts would materially change the risk assessment for RISK-SIT-04 and should be obtained from the report when accessible. (Source: 2021 Geotechnical Investigation Report; referenced via Decomposition v2.3 §13)
- Specific wetland buffer setback distances -- not directly accessed from Wetland Assessment
- Specific environmental findings from Desktop Environmental Assessment
- Site servicing cash allowance dollar amount (to be set by Estimator based on utility distance assumption)

### Source Basis Note

Site/Environmental risk entries (RISK-SIT-01 through RISK-SIT-07) rely on Decomposition v2.3 as a secondary source for reference report findings. The five underlying reference reports (2021 Geotechnical Investigation Report, Wetland Assessment, Desktop Environmental Assessment, Site Grading Documentation, Flood Zone Mapping) have not been directly accessed. All risk assessments, likelihood ratings, and impact ratings for site entries are therefore based on Decomposition v2.3 summaries of those reports, not on primary source review. Source citations within individual entries note "location TBD" where direct report access is pending. Risk ratings may require revision upon direct report access.

---

*Source: Decomposition v2.3 §9 (DEL-10-01); SOW-0028; OBJ-008. Risk entries derived from RFP and addenda context embedded in Decomposition v2.3.*
*ASSUMPTION: Risk categories (Design, Site/Environmental, Cost, Schedule, Procurement, Permitting) are interpreted from SOW-0028 decomposition context and are consistent with standard Design-Build risk management practice.*
