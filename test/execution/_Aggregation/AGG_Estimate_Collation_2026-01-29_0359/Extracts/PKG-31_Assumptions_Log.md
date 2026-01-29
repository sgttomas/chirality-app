# Assumptions Log

**Snapshot ID:** EST_PKG31_DRAFT_2026-01-29_1030

**Package:** PKG-31 Documentation & Deliverables

**Date:** 2026-01-29

---

## Purpose

This log records all assumptions and allowances where scope is known but quantities, pricing, or execution details are uncertain. Each assumption is traceable to line items and identifies the resolution path.

---

## Assumption Entries

### A-001: Total Drawing Count

**Assumption:** Total project drawings estimated at 275 sheets.

**Why Needed:** Design not yet progressed; no confirmed drawing register or drawing count available.

**Impacted WBS/CBS:**
- E (Engineering)
- DEL-31.01 (Record Drawings): Line L001
- DEL-31.02 (As-Built Drawings): Line L002
- MAT (Materials): Line L012, L013 (printing/binding)

**Cost Impact:**
- Base: $75,625 (L001 + L002)
- Materials: $23,925 (L012 + L013)
- Total base impact: $99,550 (13% of total base estimate)
- **Range:** ±30% likely → $70k to $130k range

**Confidence:** MEDIUM

**Estimated Breakdown:**
- Civil & site: 40 sheets
- Structural: 35 sheets
- Marine: 30 sheets
- Process mechanical: 45 sheets
- Piping: 40 sheets
- Electrical: 35 sheets
- Instrumentation & controls: 30 sheets
- Buildings: 20 sheets

**Resolution Path:**
1. Confirm drawing count at 30% design milestone (PKG-27 deliverables)
2. Obtain drawing register from engineering team
3. Cross-check against VFPA requirements and Employer's Requirements
4. Update estimate if variance exceeds ±15%

---

### A-002: Operational Systems Count

**Assumption:** 12 operational systems for operation manual development.

**Why Needed:** System breakdown not yet defined in engineering design.

**Impacted WBS/CBS:**
- E (Engineering)
- DEL-31.03 (Operation Manuals): Line L003
- MAT (Materials): Line L014 (printing/binding)

**Cost Impact:**
- Base: $158,400 (L003)
- Materials: $4,400 (L014)
- Total base impact: $162,800 (22% of total base estimate)
- **Range:** 10-15 systems likely → $132k to $198k range

**Confidence:** MEDIUM-LOW

**Estimated Systems:**
1. Railcar unloading system
2. Product transfer & metering system
3. Storage tank system
4. Marine loading arm system
5. Heating & temperature control system
6. Nitrogen blanketing system
7. Fire protection system
8. Electrical power distribution system
9. Control & monitoring system (SCADA/PLC)
10. Utility systems (compressed air, water, etc.)
11. Cathodic protection system
12. Building HVAC & services system

**Resolution Path:**
1. Review engineering design deliverables (PKG-27) for system breakdown
2. Cross-check against commissioning scope (PKG-30 deliverables)
3. Confirm with Employer what constitutes a "system" for O&M manual purposes
4. Update estimate if actual count differs by >20%

---

### A-003: Major Equipment Count

**Assumption:** 90 major equipment items requiring maintenance manuals and vendor documentation.

**Why Needed:** Equipment list not yet finalized in engineering design.

**Impacted WBS/CBS:**
- E (Engineering): DEL-31.04 (Maintenance Manuals): Line L004
- PM (Project Management): DEL-31.05 (Vendor Documentation): Line L005
- MAT (Materials): Line L015 (printing/binding)

**Cost Impact:**
- Base: $356,400 (L004 + L005)
- Materials: $8,800 (L015)
- Total base impact: $365,200 (48% of total base estimate)
- **Range:** 70-110 equipment items likely → $285k to $450k range

**Confidence:** MEDIUM-LOW

**Estimated Equipment Breakdown:**
- Storage tanks: 3 units (15,000 MT each)
- Railcar unloading pumps: 8 units
- Transfer pumps: 12 units
- Marine loading pumps: 4 units
- Heat exchangers / heaters: 10 units
- Metering systems: 6 units
- Valves (major/control): 20 units
- Marine loading arms: 2 units
- Control panels / MCC: 8 units
- Instrumentation (major): 12 units
- Fire protection equipment: 5 units
- **Subtotal: ~90 items**

**Resolution Path:**
1. Obtain equipment list from engineering (PKG-27, typically available at 30-60% design)
2. Cross-check against procurement deliverables (PKG-15, PKG-16, etc.)
3. Confirm with Employer what level of equipment requires individual maintenance manuals (vs generic/grouped manuals)
4. Update estimate if actual count differs by >20%

---

### A-004: Printing & Binding Costs - Drawings

**Assumption:** Printing and binding allowance for large-format drawings:
- Record set: $3,850 per set (3 sets required) = $11,550 total
- As-built set: $4,125 per set (3 sets required) = $12,375 total

**Why Needed:** No vendor quotes available for large-format printing services.

**Impacted WBS/CBS:**
- MAT (Materials)
- Line L012 (Record Drawing Printing)
- Line L013 (As-Built Drawing Printing)

**Cost Impact:**
- Base: $23,925
- With contingency (25%): $29,906
- **Range:** $18k to $30k likely (depending on paper quality, binding type, delivery)

**Confidence:** LOW

**Basis:**
- Large format printing (24"×36" typical): $8-15 per sheet
- Binding/indexing: $300-500 per set
- Delivery/handling: $200-300 per set
- Record set (standard quality): ~$14/sheet avg → $3,850/set for 275 sheets
- As-built set (archival quality): ~$15/sheet avg → $4,125/set for 275 sheets

**Resolution Path:**
1. Obtain budgetary quotes from BC Lower Mainland large-format printing vendors (e.g., BluePrint, Precision Print, etc.)
2. Confirm paper quality and binding requirements with Employer (vellum vs bond, coil vs post-bound)
3. Confirm delivery location and method (pickup vs courier)
4. Update estimate with actual quotes

---

### A-005: Printing & Binding Costs - Manuals

**Assumption:** Manual printing and binding allowance:
- Operation manuals: $1,100 per set (4 sets required) = $4,400 total
- Maintenance manuals: $2,200 per set (4 sets required) = $8,800 total

**Why Needed:** No vendor quotes available for manual printing/binding services; manual page counts not yet known.

**Impacted WBS/CBS:**
- MAT (Materials)
- Line L014 (Operation Manual Printing)
- Line L015 (Maintenance Manual Printing)

**Cost Impact:**
- Base: $13,200
- With contingency (25%): $16,500
- **Range:** $10k to $18k likely

**Confidence:** LOW

**Basis:**
- Operation manuals estimated at 150-200 pages each (~1,800 pages total per set)
- Maintenance manuals estimated at 300-400 pages each (~3,000 pages total per set)
- Color printing (diagrams/photos): $0.50-0.80/page
- B&W printing (text): $0.10-0.15/page
- Binding (3-ring binders, tabs, indexing): $50-75 per manual
- Assume 60% B&W, 40% color for both manual types

**Resolution Path:**
1. Estimate page counts once manuals are drafted (or use typical page counts from similar projects)
2. Obtain quotes from printing/binding vendors
3. Confirm color vs B&W requirements with Employer
4. Update estimate with actual quotes

---

### A-006: Document Management Software/Database

**Assumption:** Asset hierarchy database software/setup allowance: $22,000.

**Why Needed:** Employer's asset hierarchy and CMMS integration requirements not yet detailed.

**Impacted WBS/CBS:**
- MAT (Materials)
- DEL-31.06 (Asset Hierarchy): Line L016

**Cost Impact:**
- Base: $22,000
- With contingency (25%): $27,500
- **Range:** $15k to $35k likely (depending on complexity and CMMS platform)

**Confidence:** LOW

**Basis:**
- Database development/structuring: included in PM effort (Line L006)
- Software licensing (if required): $5,000-10,000
- CMMS integration / data export: $10,000-15,000
- Training / documentation: $2,000-5,000
- Total allowance: $22,000 (mid-range)

**Assumptions:**
- Employer's CMMS platform is standard commercial software (e.g., Maximo, SAP PM, Infor EAM)
- Asset hierarchy delivered as structured data export (CSV/XML/SQL) compatible with CMMS
- No custom CMMS development or complex integrations required

**Resolution Path:**
1. Clarify Employer's CMMS platform and integration requirements
2. Determine if Employer requires live CMMS database or data export only
3. Obtain quote from CMMS integration specialist or database consultant
4. Update estimate based on actual requirements

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Assumptions | 6 |
| Quantity Assumptions | 3 (A-001, A-002, A-003) |
| Pricing Assumptions (Allowances) | 3 (A-004, A-005, A-006) |
| HIGH Cost Impact | 3 (A-001, A-002, A-003) |
| MEDIUM-LOW to LOW Confidence | 5 (all except A-001) |

---

## Cost Impact Summary

| Assumption | Base Cost Impact | % of Total Base | Confidence |
|------------|------------------|-----------------|------------|
| A-001 (Drawing Count) | $99,550 | 13% | MEDIUM |
| A-002 (Systems Count) | $162,800 | 22% | MEDIUM-LOW |
| A-003 (Equipment Count) | $365,200 | 48% | MEDIUM-LOW |
| A-004 (Drawing Printing) | $23,925 | 3% | LOW |
| A-005 (Manual Printing) | $13,200 | 2% | LOW |
| A-006 (Database Software) | $22,000 | 3% | LOW |
| **Total Assumptions** | **$686,675** | **91%** | **-** |

**Key Observation:** 91% of base estimate relies on assumptions (primarily quantity estimates). This is expected at Class 5 maturity with no deliverable folders initialized yet.

---

## High-Priority Assumptions (Requiring Early Resolution)

1. **A-003 (Equipment Count):** 48% cost impact; MEDIUM-LOW confidence
   - **Action:** Obtain preliminary equipment list from engineering ASAP

2. **A-002 (Systems Count):** 22% cost impact; MEDIUM-LOW confidence
   - **Action:** Confirm system breakdown with engineering and commissioning teams

3. **A-001 (Drawing Count):** 13% cost impact; MEDIUM confidence
   - **Action:** Confirm drawing count at 30% design milestone

---

**Document Control:**
- **Snapshot ID:** EST_PKG31_DRAFT_2026-01-29_1030
- **Author:** ESTIMATING Agent
- **Date:** 2026-01-29 10:30
- **Entries:** A-001 through A-006
