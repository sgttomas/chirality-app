# Estimate Summary

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG23_DRAFT_2026-01-28_2400 |
| Estimate Label | PKG23_DRAFT |
| Package | PKG-23 Fire Protection |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Date | 2026-01-28 |
| Run Status | WARNINGS |

## Cost Breakdown Structure (CBS) Summary

| CBS | Description | Base Cost | Contingency % | Contingency | Total Cost |
|-----|-------------|-----------|---------------|-------------|------------|
| E | Engineering & Design | $175,000 | 20% | $35,000 | $210,000 |
| MAT | Equipment & Materials | $1,045,000 | 25% | $261,000 | $1,306,000 |
| CD | Construction Directs | $600,000 | 30% | $180,000 | $780,000 |
| CI | Construction Indirects | $108,000 | 30% | $32,000 | $140,000 |
| P | Procurement Services | $21,000 | 15% | $3,000 | $24,000 |
| PM | EPCM / Project Management | $106,000 | 15% | $16,000 | $122,000 |
| COM | Commissioning | $53,000 | 30% | $16,000 | $69,000 |
| **SUBTOTAL** | | **$2,108,000** | | **$543,000** | **$2,651,000** |

**Rounded Estimate Total:** **$2,480,000 CAD** (rounded to nearest $10,000 per rounding policy)

---

## Work Breakdown Structure (WBS) Summary

| Deliverable ID | Name | CBS Buckets | Base Cost | Notes |
|----------------|------|-------------|-----------|-------|
| DEL-23.01 | Fire Protection Design Drawing Set | E, MAT, CD | $640,000 | Fire water loop layout; hydrant locations; fire alarm drawings; foam system layouts |
| DEL-23.02 | Fire Protection Technical Specification | E | $40,000 | Fire water piping spec; fire hydrant spec; fire alarm spec; foam system spec |
| DEL-23.03 | Fire Protection Design Calculations | E | $50,000 | Fire water demand; hydraulic calcs; foam system sizing |
| DEL-23.04 | Fire Protection Data Sheet Package | E, MAT, CD | $780,000 | Equipment data sheets; materials procurement support; installation |
| DEL-23.05 | Fire Protection Installation & Test Records | CI, COM | Included in factors | QA/QC records; testing; commissioning (captured in CI and COM buckets) |
| **Directs/Indirects/Services** | Construction Indirects, Procurement, PM | CI, P, PM | $235,000 | Factor-based services supporting all deliverables |

---

## Key Cost Drivers

| Driver | Base Cost | % of Base | Notes |
|--------|-----------|-----------|-------|
| Equipment & Materials (MAT) | $1,045,000 | 50% | Largest cost driver; includes fire water piping ($230k), hydrants ($120k), fire alarm ($215k), foam systems ($425k) |
| Construction Directs (CD) | $600,000 | 28% | Second largest driver; includes fire water loop installation ($300k), fire alarm installation ($95k), foam installation ($150k), hydrant installation ($55k) |
| Engineering & Design (E) | $175,000 | 8% | Design deliverables (5 total); fire protection engineering and calculations |
| Construction Indirects (CI) | $108,000 | 5% | Factor-based at 18% of CD |
| EPCM / PM | $106,000 | 5% | Factor-based at 6% of (CD+CI+MAT) |
| Commissioning (COM) | $53,000 | 3% | Factor-based at 3% of (CD+CI+MAT); includes testing per DEL-23.05 |
| Procurement Services (P) | $21,000 | 1% | Factor-based at 2% of MAT |

---

## Cost by Fire Protection System

| System | Materials (MAT) | Construction (CD) | Subtotal | % of MAT+CD |
|--------|-----------------|-------------------|----------|-------------|
| Fire Water Distribution | $285,000 | $300,000 | $585,000 | 36% |
| Fire Hydrants & FDC | $120,000 | $55,000 | $175,000 | 11% |
| Fire Alarm & Detection | $215,000 | $95,000 | $310,000 | 19% |
| Foam Suppression System | $425,000 | $150,000 | $575,000 | 35% |
| **Total MAT + CD** | **$1,045,000** | **$600,000** | **$1,645,000** | **100%** |

---

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Total line items | 22 |
| Lines priced by QUOTE | 0% (0 lines) |
| Lines priced by RATE_TABLE | 0% (0 lines) |
| Lines priced by ALLOWANCE | 82% (18 lines) |
| Lines priced by PARAMETRIC (factors) | 18% (4 lines) |
| Deliverables with explicit quantities | 0% (0 of 5) |
| Overall confidence | LOW |

---

## Estimate Basis Summary

| Parameter | Value |
|-----------|-------|
| Estimate type | Order-of-magnitude allowance-based estimate |
| Pricing method | 100% allowances for directs/materials; factor-based for indirects/services |
| Quantity basis | Engineering judgment; no design quantities available (all deliverables INITIALIZED status) |
| Pricing basis | Typical market rates for BC Lower Mainland fire protection systems; no vendor quotes |
| Indirects model | Factor-based per fallback typical model |
| Contingency method | PCT_BY_BUCKET with allowance-heavy adjustments (20-30% by bucket) |
| Escalation | None (current January 2026 dollars) |
| Accuracy class | Class 5 / Order of Magnitude (-30% to +50% typical range) |

---

## Fire Protection Scope Summary

| Fire Protection Element | Scope Basis | Assumption |
|-------------------------|-------------|------------|
| Fire Water Loop | 500-800 LM underground (ductile iron DN150-DN300); 200-400 LM above-ground (steel DN100-DN200) | A-001 |
| Fire Hydrants | 8-12 dry-barrel hydrants rated -40°C; 2 fire department connections | A-002 |
| Fire Alarm System | Addressable FACP; 60-100 detection devices; 40-60 notification devices | A-004, A-005 |
| Tank Foam System | 3 × 15,000 MT tanks; foam chambers or foam makers per NFPA 11 | A-006, A-007 |
| Marine Loading Foam | Foam monitors/nozzles on loading platform per NFPA 11/16 | A-008 |
| Foam Concentrate Storage | 2,000-4,000 gal tank; AR-AFFF 3% concentrate | A-006 |

---

## Next Estimate Iteration Requirements

To improve estimate accuracy for PKG-23:

1. **Complete design quantities:**
   - DEL-23.01 drawings with fire water loop routing, hydrant locations, pipe sizes
   - DEL-23.03 fire water demand calculation per NFPA 30
   - DEL-23.03 hydraulic calculations for pipe sizing and pressure

2. **Obtain vendor pricing:**
   - Fire hydrant budgetary quotes (dry-barrel, -40°C rated)
   - Fire alarm panel and devices pricing
   - Foam proportioning system budgetary quotes
   - Foam concentrate pricing (AR-AFFF 3%)

3. **Provide project data:**
   - Fire protection zone plan
   - Fire water supply source confirmation (municipal or dedicated)
   - Fire pump requirement determination
   - Insurance/AHJ requirements

4. **Expected accuracy improvement:** Class 4 (-20% to +30%) with design quantities and vendor quotes; Class 3 (-15% to +20%) with final design and firm quotes

---

## Reconciliation with Previous Packages

| Package | Deliverables | Base Total | Contingency | Estimate Total | Cost/Deliverable |
|---------|--------------|------------|-------------|----------------|------------------|
| PKG-00 Site Establishment | 8 | (prior estimate) | (prior) | (prior) | (prior) |
| PKG-01 Demolition & Removals | 4 | (prior estimate) | (prior) | (prior) | (prior) |
| PKG-02 Earthworks | 9 | $3,545,000 | $950,000 | $4,495,000 | $499k/del |
| PKG-03 Underground Utilities | 6 | $2,119,000 | $568,000 | $2,687,000 | $448k/del |
| **PKG-23 Fire Protection** | **5** | **$2,108,000** | **$543,000** | **$2,480,000** | **$496k/del** |

**Notes:**
- PKG-23 cost per deliverable ($496k) is comparable to PKG-02/PKG-03, consistent with specialty systems complexity
- PKG-23 is materials-heavy (50% MAT vs 27% for PKG-03) reflecting fire protection equipment costs
- Foam suppression system ($575k total) is significant driver due to 3 × 15,000 MT tank coverage requirement
- Both packages show ~27% contingency rate due to 100% allowance-based pricing (see Risk_Register.md)

---
