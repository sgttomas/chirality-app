# Basis of Estimate (BOE)

## Snapshot Information

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-05-02_2026-02-04_1322 |
| **Estimate Label** | DEL-05-02_AppendixH_ScheduleB_CostBreakdown |
| **Deliverable** | DEL-05-02 AppendixH ScheduleB CostBreakdown |
| **Package** | PKG-02 Financial Proposal (Appendix H) |
| **Pricing Date** | 2026-02 (dollars of February 2026) |
| **Currency** | CAD |
| **RUN_STATUS** | WARNINGS |

---

## Scope Inclusions

This estimate covers the cost breakdown components for Schedule B of Appendix H, specifically:

### Base Scope
1. **General Requirements** - Project management, supervision, mobilization, temporary facilities, project closeout
2. **Building** - Foundation, structure, envelope, roofing, interior finishes, mechanical, electrical, plumbing, fire protection, specialties (including Addendum 03 technical items: 16ft overhead doors, bay sumps, fire apparatus exhaust, emergency generator, fill stations, solar-ready provisions)
3. **Sitework** - Earthwork, grading, utilities (water, sanitary, storm), paving, landscaping, site lighting (12-acre developable area per Addendum 03)

### Additional Options (6 items)
- Option 1: Built-in wash bay (capital cost)
- Option 2: Yard lighting (capital cost)
- Option 3: Building access control (capital cost)
- Option 4: Security/cameras (capital cost + monitoring fee SEPARATED)
- Option 5: Exterior signage/branding (capital cost)
- Option 6: Appliances (capital cost)

---

## Scope Exclusions

| Exclusion | Rationale | Source |
|-----------|-----------|--------|
| Pickled sand storage building | Removed from RFP scope per Addendum 03 | Decomposition Section 4; D-001 |
| Land and real estate costs | Owner cost; out of contractor scope | Standard exclusion |
| Financing costs | Owner cost | Standard exclusion |
| FF&E (Furniture, Fixtures & Equipment) | May be separate additional item, NOT in base cost | Decomposition Section 4; OI-004 |
| Owner's soft costs | Owner cost | Standard exclusion |
| Flood fringe development (8 acres) | Only 12-acre developable area in scope | Addendum 03; D-002 |
| Operating costs (except Option 4 monitoring) | Operating budget items | Guidance.md Principle 4 |

---

## Contracting Assumptions

| Assumption ID | Assumption | Impact |
|---------------|------------|--------|
| A-001 | Design-Build delivery method with single-point responsibility | General Requirements includes design coordination costs |
| A-002 | Competitive lump-sum pricing basis | Markups reflect competitive market conditions |
| A-003 | Self-perform and subcontract mix assumed typical for Design-Build contractor | Labor productivity and overhead rates reflect hybrid delivery |

---

## Location and Productivity Assumptions

| Assumption ID | Assumption | Impact |
|---------------|------------|--------|
| A-004 | Project location: Penhold, Alberta | Alberta labor rates and material costs apply |
| A-005 | Construction season: Standard Alberta climate constraints | Productivity factors account for weather windows |
| A-006 | Labor availability: Competitive Alberta market conditions | Rates reflect current market |

---

## Pricing Sources Hierarchy

This estimate was developed using the following priority hierarchy:

1. **QUOTE**: No vendor quotes available (0% of estimate)
2. **RATE_TABLE**: No project rate tables available in _RateTables/ (0% of estimate)
3. **ALLOWANCE/PARAMETRIC**: 100% of estimate based on parametric/allowance approach

**Note:** All pricing is based on allowances and parametric methods due to:
- No Appendix H template available for detailed line item structure
- No concept design quantities available (DEL-02-01 not complete)
- No rate tables provided
- Preliminary estimate for proposal budgeting purposes

---

## Indirects Model

| Category | Method | Rate/Factor | Source |
|----------|--------|-------------|--------|
| General Requirements | Percentage of direct construction | 10% of Building + Sitework | D-003; industry standard |
| Contractor OH&P | Embedded in unit rates | 15% markup assumed | D-004; industry standard |
| Design Contingency | Explicit allowance | 10% of base construction | D-005; early-stage estimate |

---

## Contingency Method and Rationale

**Method:** PCT_BY_BUCKET (percentage by cost bucket)

| CBS Category | Contingency % | Rationale |
|--------------|---------------|-----------|
| General Requirements | 5% | Lower uncertainty; management-related |
| Building | 10% | Moderate uncertainty; concept stage |
| Sitework | 15% | Higher uncertainty; site conditions unknown |
| Additional Options | 10% | Moderate uncertainty; scope not fully defined |

**Total Contingency:** Applied as explicit line item (see Detail.csv)

**Rationale:** Early-stage Design-Build proposal with limited design development. Contingency reflects:
- Concept-level scope definition
- Unknown site conditions (geotechnical, utilities)
- Pending Addendum 03 technical clarifications

---

## Escalation Method and Rationale

**Mode:** NONE

**Rationale:** Pricing date is current (2026-02); construction assumed within 12-18 months. Escalation not separated; assumed captured in unit rates.

---

## Rounding Policy

| Policy | Value |
|--------|-------|
| Line item rounding | Nearest $1,000 CAD |
| Summary rounding | Nearest $1,000 CAD |
| Totals precision | 3 significant figures for amounts > $100,000 |

---

## Completeness Metrics Summary

| Metric | Value |
|--------|-------|
| % priced by QUOTE | 0% |
| % priced by RATE_TABLE | 0% |
| % priced by ALLOWANCE/PARAMETRIC | 100% |
| % of deliverables with explicit quantities | 0% (quantities TBD pending DEL-02-01) |
| Data confidence level | LOW |

---

## Known Gaps

| Gap ID | Description | Impact | Resolution Path |
|--------|-------------|--------|-----------------|
| G-001 | No Appendix H template available | Cannot confirm exact line item structure | Obtain template from Proposal Manager |
| G-002 | DEL-02-01 Concept Design not complete | Building area and scope quantities unknown | Complete DEL-02-01; update estimate |
| G-003 | No vendor quotes for major equipment | Pricing based on parametric assumptions | Obtain budgetary quotes |
| G-004 | Site conditions not surveyed | Sitework costs are allowances | Complete geotechnical investigation |
| G-005 | Additional Options scope not detailed | Option costs are allowances | Confirm scope with Design Lead |
| G-006 | No rate tables provided | 100% allowance-based pricing | Provide firm rate tables |

---

## References

- **Decision_Log.md**: Decisions D-001 through D-010
- **Assumptions_Log.md**: Assumptions A-001 through A-015
- **Risk_Register.md**: Risks R-001 through R-008
- **Source_Index.md**: Source documents and references

---

## Document Information

| Field | Value |
|-------|-------|
| Created | 2026-02-04 |
| Agent | ESTIMATING (Type 2) |
| Snapshot Path | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Estimates/EST_DEL-05-02_2026-02-04_1322/ |
