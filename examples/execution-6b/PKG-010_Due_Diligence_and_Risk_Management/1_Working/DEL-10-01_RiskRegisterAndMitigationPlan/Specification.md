# Specification — Risk Register and Mitigation Plan

**Deliverable ID:** DEL-10-01
**Deliverable Name:** Risk Register and Mitigation Plan
**Package:** PKG-010 — Due Diligence & Risk Management
**Type:** Risk / Register + Narrative
**Responsible Party:** PM + Technical Leads
**Date Generated:** 2026-02-17

---

## Scope

### What This Deliverable Covers

DEL-10-01 produces two co-dependent artifacts for the Penhold PSB Design-Build proposal:

1. **Tabular Risk Register** — a structured register of identified risks organized across six categories (Design, Site/Environmental, Cost, Schedule, Procurement, Permitting), with likelihood, impact, risk level, mitigation strategy, residual risk, responsible owner, and status for each risk. (Source: Decomposition v2.3 §7, SOW-0028; §9, DEL-10-01 description)

2. **Risk Mitigation Narrative** — a written narrative contextualizing the register, explaining the risk management approach, category-level risk summaries, mitigation philosophy, and how the risk posture supports proposal credibility. (Source: Decomposition v2.3 §9, DEL-10-01 description)

The register and narrative are grounded in: RFP 2024_004 (Sections 2–9 risk themes), Addenda 01–03 clarifications, and the reference report findings (2021 Geotechnical Investigation Report, Wetland Assessment, Desktop Environmental Assessment, Site Grading documentation, and Flood Zone Mapping — full texts not directly accessed; referenced via Decomposition v2.3 §2–3).

This deliverable directly supports **OBJ-008: Manage risk and unknowns transparently** (Source: Decomposition v2.3 §6).

### What This Deliverable Excludes

- Site conditions summary narrative — owned by DEL-10-02 (Site Conditions and Due Diligence Summary)
- Pricing assumptions, allowances, and contingency quantification — owned by DEL-01-06 (Pricing Narrative and Assumptions)
- Construction methodology and schedule content — owned by DEL-07-01 and DEL-09-01
- Quality management and commissioning risk tracking — owned by DEL-07-05 and DEL-08-01
- Quantitative Monte Carlo or probabilistic simulation (**ASSUMPTION**: qualitative-to-semi-quantitative register sufficient for proposal purposes; RFP does not specify format)
- Post-occupancy operational risks unrelated to design and construction delivery

---

## Requirements

### R-001 — Multi-Category Coverage

The Risk Register shall address risks in all six categories identified in SOW-0028: Design, Site/Environmental, Cost, Schedule, Procurement, and Permitting.

- **Minimum entries:** At least two (2) substantive risk entries per category in the proposal-stage register.
- **Verification:** Audit register — confirm 6 categories present with >= 2 entries each.
- **Source:** Decomposition v2.3 §7, SOW-0028; Datasheet §Construction.

### R-002 — Register Entry Format

Each risk register entry shall include all of the following columns, populated and non-blank for Active risks:

| Column | Required for Active Risks |
|--------|--------------------------|
| Risk ID | Yes |
| Category | Yes |
| Risk Description | Yes |
| Likelihood (Low/Medium/High) | Yes |
| Impact (Low/Medium/High/Critical) | Yes |
| Risk Level (L×I composite) | Yes |
| Mitigation Strategy | Yes |
| Residual Risk (post-mitigation) | Yes |
| Owner (responsible party) | Yes |
| Status (Active/Mitigated/Closed) | Yes |

- **Verification:** Spot-check three entries from different categories; confirm all columns populated.
- **Source:** ASSUMPTION — format derived from standard Design-Build risk management practice; RFP does not prescribe column schema (SOW-0028).

### R-003 — RFP and Addenda Grounding

Risk entries shall be traceable to at least one RFP requirement, addendum provision, or reference report finding. Entries derived solely from general practice shall be labeled **ASSUMPTION**.

- **Verification:** Each entry can be linked to RFP section, addendum §, or reference report (directly accessed or noted as location TBD).
- **Source:** Decomposition v2.3 §2 (authority order: addendum governs where conflict exists); OBJ-008.

### R-004 — Addendum 03 Special Requirements Coverage

The register shall explicitly address risks arising from Addendum 03 program enhancements. The following Addendum 03 items shall each be covered by at least one risk entry:

| Addendum 03 Item | Source |
|-----------------|--------|
| 16 ft overhead door height (all bays) | Addendum 03 §1.4 (via Decomposition v2.3 §4) |
| Bay sumps (all bays, snow melting and washing) | Addendum 03 §1.3 (via Decomposition v2.3 §4) |
| Fire apparatus direct exhaust (2 apparatus per bay) | Addendum 03 §1.5 (via Decomposition v2.3 §4) |
| Backup generator minimum loads (kitchen, ICP room, 2 bathrooms, bay door secondary opening) | Addendum 03 §1.9 (via Decomposition v2.3 §4) |
| 2" fill stations (1 fire bay, 1 PW bay) | Addendum 03 §1.10 (via Decomposition v2.3 §4) |
| Solar-capable roof orientation (flat/south/west/southwest) | Addendum 03 §1.16 (via Decomposition v2.3 §4) |
| 40 bunker gear lockers with room-level ventilation | Addendum 03 §1.12 (via Decomposition v2.3 §4) |
| Room sizing ranges (apparatus bays, workshop, gear storage, etc.) | Addendum 03 §1.20 (via Decomposition v2.3 §4) |

- **Verification:** Cross-reference Addendum 03 item checklist against register entries; confirm each item appears in at least one risk description or mitigation.
- **Source:** Decomposition v2.3 §4 (Addendum 03 integration); SOW-0010.

### R-005 — Reference Report Grounding

Site/Environmental risk entries shall reference findings from the provided reference reports. At least one risk entry shall correspond to each of the following report types:

| Reference Report | Risk Relevance |
|-----------------|----------------|
| 2021 Geotechnical Investigation Report | Foundation design assumptions; soil conditions |
| Wetland Assessment and Impact Report | Wetland buffer constraints; site layout |
| Desktop Environmental Assessment (Ghostpine) | Soil/groundwater contamination potential |
| Site Grading Documentation (Appendix E) | Earthworks and drainage implications |
| Flood Zone Mapping | 8-acre flood fringe constraint on site layout |

- **Verification:** Confirm at least one risk entry per report type in the Site/Environmental category.
- **Source:** Decomposition v2.3 §2 (reference/background appendices); DEL-10-01 _CONTEXT.md description.
- **Note:** Full report texts are not directly accessible at this stage; risk entries reference report type and context as summarized in Decomposition v2.3 §2–4, with source noted as "location TBD."

### R-006 — DEC-013 Risk Acceptance (No Additional Geotech)

The register shall include a risk entry explicitly acknowledging the accepted decision (DEC-013) that no additional geotechnical investigation is conducted at proposal stage, and that foundation design relies on the existing 2021 report only.

- **Risk Response:** Accept, with contingency response documented.
- **Verification:** Confirm RISK-SIT-04 (or equivalent entry) exists with risk response = Accept and rationale stated.
- **Source:** Decomposition v2.3 §13, DEC-013; SOW-0027.

### R-007 — Mitigation Strategy for All Active Risks

Every risk entry with Status = Active shall have a non-blank, specific mitigation strategy. Strategies of the form "we will monitor" or "we will manage carefully" are insufficient; strategies shall name an action, trigger, or checkpoint.

- **Verification:** Review all Active entries; flag any with generic mitigation text.
- **Source:** ASSUMPTION — standard risk management requirement (ISO 31000 convention; not cited by RFP).

### R-008 — Residual Risk Statement

Each Active risk entry shall include a residual risk rating (post-mitigation Likelihood / Impact) to demonstrate that mitigation has a measurable effect. At least three entries shall retain a non-trivial residual risk (Medium or above) to avoid the appearance of false certainty.

- **Verification:** Check residual risk column; confirm at least 3 entries show non-trivial residual.
- **Source:** OBJ-008 (transparency principle); ASSUMPTION (standard practice).

### R-009 — Risk Mitigation Narrative Content

The Risk Mitigation Narrative shall include five identifiable elements:

| Element | Description |
|---------|-------------|
| (a) Purpose | Why risk management is material to this proposal and project delivery |
| (b) Risk Assessment Philosophy | How risks are identified, categorized, rated, and prioritized |
| (c) Category Summaries | High-level narrative per category (Design, Site-Environmental, Cost, Schedule, Procurement, Permitting) referencing key register entries |
| (d) Mitigation Response Philosophy | Description of Avoid / Reduce / Transfer / Accept response types with project-specific examples |
| (e) Contingency Approach | How the team approaches contingency reserve allocation; alignment with pricing narrative (DEL-01-06) |

- **Verification:** Review narrative for five elements; confirm each is present as an identifiable section or subsection. Beyond presence, verify quality depth: each category summary (element c) shall reference at least one specific Risk ID; the mitigation response philosophy (element d) shall include at least one project-specific example per response type; the contingency approach (element e) shall cross-reference DEL-01-06 explicitly.
- **Quality acceptance criteria:** Each of the five elements shall be substantive (not placeholder text); category summaries shall demonstrate consistent depth and tone across all six categories; the narrative as a whole shall be legible as a standalone document for an evaluator unfamiliar with the register tables. (**ASSUMPTION**: Quality criteria inferred from OBJ-008 evaluation expectations.)
- **Source:** Decomposition v2.3 §9, DEL-10-01 description.

### R-010 — Owner Assignment

Every risk entry shall have an assigned Owner party. The Owner identifies the individual or role accountable for monitoring and executing the mitigation strategy.

- **Verification:** No blank Owner fields in Active register entries.
- **Source:** ASSUMPTION — standard risk management practice (Design-Build PM responsibility framework).

### R-011 — Long-Lead Procurement Risk

The register shall include at least one risk entry in the Procurement or Schedule category that explicitly addresses long-lead procurement items arising from Addendum 03 requirements (16 ft overhead doors, backup generator, fire apparatus direct exhaust equipment, HVAC for apparatus bays).

- **Verification:** Confirm RISK-SCH-04 (or equivalent) addresses long-lead procurement risk tied to Addendum 03 items.
- **Source:** Addendum 03 (via Decomposition v2.3 §4); SOW-0010.

### R-012 — Consistency with DEL-10-02

Site/Environmental risk entries shall be consistent with the site conditions summary produced in DEL-10-02. No contradictions shall exist between the two deliverables' characterization of site risk (flood fringe extents, wetland constraints, geotechnical reliance, environmental findings).

- **Verification:** Cross-check site risk descriptions in this register against DEL-10-02 at pre-submission QA; document any conflicts in Guidance.md Conflict Table.
- **Source:** _REFERENCES.md (DEL-10-02 cross-reference); Decomposition v2.3 §9.

### R-013 — Proposal Positioning Alignment

The Risk Register and Narrative shall be framed to support the proposal evaluation objective (OBJ-008). The tone shall be professional, credible, and confident — demonstrating that the team has identified real risks and has specific plans to address them, without being defensive or suggesting inability to deliver.

- **Verification:** Proposal Manager review confirms tone and positioning.
- **Source:** Decomposition v2.3 §6, OBJ-008 ("credibility across all scored areas").

---

## Standards

| Standard / Reference | Applicability | Access Status |
|---------------------|---------------|---------------|
| RFP 2024_004 §2–§9 | Primary risk identification authority | Referenced via Decomposition v2.3 |
| Addendum 03 (Jul 31, 2024) | Special requirements risk surface | Referenced via Decomposition v2.3 §4 |
| CCDC 14-2013 with Appendix J (Supplementary Conditions) | Risk allocation framework for Design-Build delivery. Appendix J supplementary conditions may define specific risk allocation between Owner and DB contractor (e.g., foundation risk, latent defects, unforeseen site conditions) that should inform which risk entries carry "Transfer" vs. "Accept" responses. Specific supplementary condition clauses affecting risk register content are TBD pending direct document access. | Location TBD -- not directly accessed |
| ISO 31000:2018 (Risk Management — Guidelines) | Risk management process framework | **ASSUMPTION**: Applicable by industry convention; not cited by RFP; location TBD |
| National Building Code of Canada (NBCC) | Design risk context (code compliance risks). Note: NBCC is cited as contextual for design risk identification (e.g., code interpretation uncertainty for room sizing, occupancy classification, fire separation requirements). While no risk entry in the current register explicitly addresses NBCC compliance as a standalone risk, code compliance considerations are embedded in design risk entries RISK-DES-02 (room sizing) and RISK-DES-04 (building-code minimum as floor constraint). If NBCC interpretation poses material risk beyond these entries, consider adding a dedicated code compliance risk entry. | **ASSUMPTION**: Applicable; referenced in Decomposition vocabulary map |
| Alberta OH&S Legislation | Safety risk context for construction phase | **ASSUMPTION**: Applicable; not specifically cited in RFP for this deliverable |

---

## Verification

| Req ID | Requirement | Verification Method | Responsible Party | Stage |
|--------|-------------|---------------------|-------------------|-------|
| R-001 | Multi-category coverage | Audit: 6 categories present, >= 2 entries each | PM | Pre-submission QA |
| R-002 | Entry format completeness | Spot-check 3 entries across categories | PM | Internal review |
| R-003 | RFP/Addenda grounding | Trace each entry to source document | PM | Internal review |
| R-004 | Addendum 03 item coverage | Cross-reference Addendum 03 checklist | Lead Architect + PM | Design coordination |
| R-005 | Reference report grounding | Confirm 1 entry per reference report type | PM + Technical Leads | Internal review |
| R-006 | DEC-013 compliance | Confirm geotech reliance risk entry exists | Structural Engineer + PM | Internal review |
| R-007 | Mitigation specificity | Review all Active entries for specific mitigations | PM | Pre-submission QA |
| R-008 | Residual risk statement | Confirm >= 3 entries with non-trivial residual | PM | Internal review |
| R-009 | Narrative completeness | Review narrative for five elements | PM | Pre-submission QA |
| R-010 | Owner assignment | No blank Owner fields | PM | Pre-submission QA |
| R-011 | Long-lead risk coverage | Confirm Procurement/Schedule entry for long-lead | Construction Manager | Pre-submission QA |
| R-012 | DEL-10-02 consistency | Cross-check site risk entries vs. DEL-10-02 | PM | Consistency review |
| R-013 | Proposal positioning | Proposal Manager review of tone/credibility; verify via structured checklist: (1) risk descriptions are project-specific, (2) mitigations name actions/owners/triggers, (3) tone is confident without being defensive, (4) residual risk acknowledgments demonstrate maturity | Proposal Manager | Final review |

---

## Documentation

### Required Artifacts (from _CONTEXT.md)

1. **Risk register (tabular)** — final tabular register; Markdown tables for working documents; exportable to Excel/CSV for internal use
2. **Risk mitigation narrative** — written narrative; included in proposal submission package

### Supporting References to Cite

- RFP 2024_004 Sections 2–9 (risk themes)
- Addenda 01, 02, 03 (specific §citations per risk)
- 2021 Geotechnical Investigation Report (location TBD)
- Wetland Assessment and Impact Report (location TBD)
- Desktop Environmental Assessment — Ghostpine (location TBD)
- Site Grading Documentation — Appendix E (location TBD)
- Flood Zone Mapping (location TBD)
- Penhold PSB Project Decomposition v2.3

### Downstream Alignment

- Risk entries for RISK-CST-* shall be reconciled with DEL-01-06 (Pricing Narrative) cost assumptions before submission
- Risk entries for RISK-SCH-* shall be reflected in DEL-09-01 (Detailed Project Schedule) schedule buffer assumptions
- Risk entries for RISK-SIT-* shall be consistent with DEL-10-02 (Site Conditions) characterization of reference report findings

---

*Source: Decomposition v2.3 §7 (SOW-0028), §9 (DEL-10-01), §6 (OBJ-008), §4 (Addendum 03), §13 (DEC-013).*
