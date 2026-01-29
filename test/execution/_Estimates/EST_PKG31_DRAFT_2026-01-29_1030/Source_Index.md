# Source Index

**Snapshot ID:** EST_PKG31_DRAFT_2026-01-29_1030

**Package:** PKG-31 Documentation & Deliverables

**Date:** 2026-01-29

---

## Purpose

This index lists all sources used for pricing and quantities in this estimate, organized by priority tier. Each source is evaluated for availability, applicability, and usage in the estimate.

---

## Source Priority Hierarchy

Pricing sources are applied in the following priority order per estimating protocol:

1. **QUOTE** — Vendor budgetary quotes or proposals (highest priority)
2. **RATE_TABLE** — Project-specific or company rate tables
3. **PARAMETRIC** — Parametric models based on typical production rates and industry benchmarks
4. **ALLOWANCE** — Lump-sum allowances where scope is known but detailed pricing is unavailable

---

## Tier 1: Explicit Pricing Sources (QUOTE)

**Status:** ❌ None available

| Source | Description | Coverage | Status |
|--------|-------------|----------|--------|
| Printing/binding vendor quotes | Large-format printing, manual binding, delivery | 0 line items | NOT AVAILABLE |
| Document management software quotes | CMMS integration, database software | 0 line items | NOT AVAILABLE |
| Technical writing services quotes | O&M manual authoring services | 0 line items | NOT AVAILABLE |

**Usage in Estimate:** 0% (no quotes available)

**Recommended Actions:**
1. Obtain budgetary quotes from BC Lower Mainland large-format printing vendors (e.g., BluePrint, Precision Print, Reproductions)
2. Obtain quotes for CMMS integration services or database consultants
3. Consider quotes for technical writing services (if outsourcing manual development)

---

## Tier 2: Rate Tables / Cost Libraries (RATE_TABLE)

**Status:** ❌ None available

| Source | Description | Coverage | Status |
|--------|-------------|----------|--------|
| `_RateTables/Documentation_Services.csv` | Project-specific rate table for documentation services | 0 line items | NOT FOUND |
| `_RateTables/Engineering_Labor.csv` | Engineering labor rates by discipline/seniority | 0 line items | NOT FOUND |
| `_RateTables/PM_Services.csv` | PM/document control labor rates | 0 line items | NOT FOUND |

**Usage in Estimate:** 0% (no rate tables available)

**Recommended Actions:**
1. Create rate table template: `_RateTables/Documentation_Services.csv` with columns:
   - Service (e.g., CAD Drafting - Intermediate, Technical Writing - Senior, Document Control - Coordinator)
   - Unit (hours)
   - Rate_CAD ($/hr)
   - Source (company rates, market survey, historical)
2. Populate with project-specific or company-standard rates
3. Re-run estimate using rate table instead of parametric assumptions

---

## Tier 3: Parametric Models (PARAMETRIC)

**Status:** ✅ Used extensively (92% of base estimate)

### Source 3A: Decomposition

**File:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

**Section:** PKG-31: Documentation & Deliverables (lines 676-696 in decomposition)

**Content Used:**
- Deliverable descriptions (DEL-31.01 through DEL-31.11)
- Responsible party (D&B Contractor)
- Deliverable types (Drawing Set, Manual, Document Package, Document)
- Anticipated artifacts

**Usage:**
- WBS structure and deliverable identification
- Scope definition for each deliverable
- Baseline for parametric quantity estimates (drawing count, equipment count, system count)

**Limitations:**
- Decomposition provides scope definition only, not quantities or pricing
- Quantities must be estimated parametrically from typical project benchmarks

---

### Source 3B: Parametric Production Rates (Typical EPC Projects)

**Source:** Industry benchmarks and typical production rates for EPC documentation

**Basis:** Typical production rates for similar projects (industrial facilities, marine terminals, oil/chemical transload facilities)

**Production Rates Used:**

| Activity | Rate | Unit | Basis | Applied To |
|----------|------|------|-------|------------|
| Record drawing production | 12 | hrs/sheet | Multi-discipline coordination average | L001 (DEL-31.01) |
| As-built incorporation | 8 | hrs/sheet | Field markup review, updates, QA | L002 (DEL-31.02) |
| Operation manual authoring | 80 | hrs/system | System-level procedures and diagrams | L003 (DEL-31.03) |
| Maintenance manual compilation | 16 | hrs/equipment | From vendor docs + project additions | L004 (DEL-31.04) |
| Vendor doc compilation | 1320 | hrs total | For 90 equipment vendors (~15 hrs/vendor avg) | L005 (DEL-31.05) |
| Asset hierarchy development | 120 | hrs total | Database structure + population | L006 (DEL-31.06) |
| Register development | 40 | hrs each | For warranties register, H&S file | L007, L008 |
| Certificate coordination | 60-30 | hrs total | Collection, organization, verification | L009, L010, L011 |
| Document control (ongoing) | 400 | hrs total | Throughout 24-30 month project | L017 |
| Final submittal preparation | 80 | hrs total | Final assembly, indexing, delivery | L018 |

**Confidence:** MEDIUM (rates based on typical projects; may vary by ±20-30% depending on actual project complexity)

**References:**
- Decision D-006 (drawing production rates)
- Decision D-007 (manual development rates)
- Decision D-008 (PM coordination effort)
- Decision D-009 (document control and submittal)

---

### Source 3C: Parametric Labor Rates (BC Lower Mainland EPC Projects, 2026)

**Source:** Typical market rates for BC Lower Mainland engineering and PM services, January 2026

**Labor Rates Used:**

| Role | Rate (CAD/hr) | Basis | Applied To |
|------|---------------|-------|------------|
| Engineering (blended) | $165 | Senior/intermediate CAD drafting, technical writing | All E (Engineering) line items |
| Project Management | $132 | Document control, coordination, QA | All PM line items |

**Rate Inclusions:**
- Direct labor
- Benefits and payroll burden (~30-35%)
- Office overhead allocation (~15-20%)
- Small tools and consumables (~2-3%)
- General supervision (~3-5%)

**Rate Exclusions:**
- Project management fee (separate)
- Contingency (applied at CBS bucket level)
- Equipment/software (covered separately in MAT bucket)

**Confidence:** MEDIUM (rates based on typical 2026 BC market; subject to ±10-15% variance)

**Reference:** Decision D-006 (labor rates)

---

### Source 3D: Parametric Quantity Estimates

**Drawing Count:**
- **Estimate:** 275 total sheets
- **Basis:** Typical drawing count for industrial facility of this scope (1M MT/annum, 45k MT storage, railcar unloading, marine loading, utilities, buildings)
- **Breakdown:** Civil 40, Structural 35, Marine 30, Process 45, Piping 40, Electrical 35, I&C 30, Buildings 20
- **Confidence:** MEDIUM (±30% range; 190-360 sheets possible until design progresses)
- **Reference:** Assumption A-001, Risk R-001

**System Count:**
- **Estimate:** 12 operational systems for O&M manuals
- **Basis:** Decomposition scope review (rail unloading, transfer, storage, marine loading, heating, nitrogen, fire protection, electrical, control, utilities, cathodic protection, building HVAC)
- **Confidence:** MEDIUM-LOW (±25% range; 9-15 systems possible depending on system boundary definitions)
- **Reference:** Assumption A-002, Risk R-003

**Equipment Count:**
- **Estimate:** 90 major equipment items for maintenance manuals
- **Basis:** Decomposition scope review (tanks, pumps, heat exchangers, valves, marine arms, instruments, panels, etc.)
- **Confidence:** MEDIUM-LOW (±30% range; 63-117 items possible until equipment list is finalized)
- **Reference:** Assumption A-003, Risk R-002

---

## Tier 4: Allowances (ALLOWANCE)

**Status:** ✅ Used for materials and software (8% of base estimate)

### Allowance A-004: Drawing Printing & Binding

**Scope:** Large-format drawing printing and binding for record and as-built sets

**Line Items:**
- L012: Record drawing set printing (3 sets × 275 sheets) = $11,550
- L013: As-built drawing set printing (3 sets × 275 sheets) = $12,375

**Basis:**
- Large format printing (24"×36"): $8-15 per sheet (depending on paper quality)
- Binding/indexing: $300-500 per set
- Record set (standard): ~$14/sheet avg → $3,850/set
- As-built set (archival): ~$15/sheet avg → $4,125/set

**Confidence:** LOW (no quotes; market rate variance of ±20-30% possible)

**Reference:** Assumption A-004, Risk R-008

---

### Allowance A-005: Manual Printing & Binding

**Scope:** Printing and binding for operation and maintenance manuals

**Line Items:**
- L014: Operation manual printing (4 sets) = $4,400
- L015: Maintenance manual printing (4 sets) = $8,800

**Basis:**
- Operation manuals: ~1,800 pages per set → $1,100/set
- Maintenance manuals: ~3,000 pages per set → $2,200/set
- Mix of color and B&W printing, 3-ring binders, tabs, indexing

**Confidence:** LOW (no quotes; page counts and printing costs not confirmed)

**Reference:** Assumption A-005, Risk R-008

---

### Allowance A-006: Document Management Software / Database

**Scope:** Asset hierarchy database development and CMMS integration

**Line Items:**
- L016: Asset hierarchy database/software = $22,000

**Basis:**
- Software licensing (if required): $5k-10k
- CMMS integration / data export: $10k-15k
- Training / documentation: $2k-5k
- Total allowance: $22k (mid-range estimate)

**Assumptions:**
- Employer has standard commercial CMMS platform
- Asset hierarchy delivered as structured data export (CSV/XML/SQL)
- No custom CMMS development required

**Confidence:** LOW (requirements not yet detailed by Employer)

**Reference:** Assumption A-006, Risk R-007

---

## Source Coverage Summary

| Tier | Method | % of Base | $ Value | Line Items | Status |
|------|--------|-----------|---------|------------|--------|
| Tier 1 | QUOTE | 0% | $0 | 0 | ❌ Not available |
| Tier 2 | RATE_TABLE | 0% | $0 | 0 | ❌ Not available |
| Tier 3 | PARAMETRIC | 92% | $696,025 | 13 | ✅ Used extensively |
| Tier 4 | ALLOWANCE | 8% | $59,125 | 5 | ✅ Used for materials/software |
| **Total** | | **100%** | **$755,150** | **18** | |

---

## Source Quality Assessment

| Quality Metric | Rating | Notes |
|----------------|--------|-------|
| Pricing data maturity | LOW | 0% from quotes/rates; 100% parametric/allowance |
| Quantity data maturity | LOW | All quantities estimated; 0% verified from design |
| Source documentation | MEDIUM | Decomposition available; parametric basis documented |
| Source traceability | HIGH | All line items have source references (decisions/assumptions) |
| Source currency | CURRENT | All sources dated January 2026 or are current market rates |

**Overall Source Quality:** Class 5 (Order of Magnitude)

**Path to Improvement:**
1. Obtain vendor quotes → improves to Class 4
2. Create/use rate tables → improves to Class 4
3. Verify quantities from design → improves to Class 3
4. Combine all three → achieves Class 3 maturity

---

## Missing Sources (Gaps)

| Missing Source | Impact | Priority | Action Required |
|----------------|--------|----------|-----------------|
| Vendor quotes (printing/binding) | LOW-MED | MEDIUM | Obtain budgetary quotes from 3+ vendors |
| CMMS integration quote | LOW | LOW | Clarify Employer requirements; obtain quote |
| Rate table (documentation services) | HIGH | HIGH | Create template and populate with market/company rates |
| Drawing count (from design) | HIGH | HIGH | Obtain from engineering at 30% design |
| Equipment list (from design) | HIGH | HIGH | Obtain from engineering at 30% design |
| VFPA drawing standards | MEDIUM | MEDIUM | Obtain from VFPA or Employer early in design |

---

**Document Control:**
- **Snapshot ID:** EST_PKG31_DRAFT_2026-01-29_1030
- **Author:** ESTIMATING Agent
- **Date:** 2026-01-29 10:30
- **Sources Used:** Decomposition (1), Parametric models (4), Allowances (3)
- **Source Maturity:** Class 5 (Order of Magnitude)
