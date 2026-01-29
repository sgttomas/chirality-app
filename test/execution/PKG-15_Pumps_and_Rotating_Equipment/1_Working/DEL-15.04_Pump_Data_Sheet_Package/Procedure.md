# Procedure: DEL-15.04 Pump Data Sheet Package

## Purpose

This procedure defines the process for managing the **Pump Data Sheet Package** within **PKG-15 Pumps & Rotating Equipment** for the Canola Oil Transload Facility.

**Deliverable purpose:** Defines and substantiates pumps in accordance with ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.04 entry

**Deliverable type:** Data Sheet (Vendor-supplied equipment data)
**Responsible party:** D&B Contractor (Mechanical discipline) — review and approval; Vendor — data preparation

This procedure covers:
1. **Data submittal:** Vendor data package requirements and submittal process
2. **Data review:** How to review vendor data for compliance and suitability
3. **Data approval:** How to approve data for construction use (AFC)

**Source:** Standard EPC vendor data management process

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans

**Source:** `_DEPENDENCIES.md`

### Upstream Requirements

| Requirement | Source | Status |
|------------|--------|--------|
| **Equipment specification** | DEL-15.02 (issued for procurement) | **TBD** |
| **Design calculations** | DEL-15.03 (NPSH, system curves) | **TBD** |
| **Purchase order** | Procurement (vendor contract awarded) | **TBD** |

**Source:** Vendor data follows equipment procurement

### Personnel and Tools

**Personnel:**
- Mechanical Engineer — Data review and coordination
- Checker (Independent) — Critical items verification (NPSH, operating point)
- Lead Mechanical Engineer — Approval

**Tools:**
- Document management system for vendor data tracking
- Spreadsheet for NPSH and operating point calculations/verification

**Source:** Standard vendor data review requirements

## Steps

### Phase 1: Vendor Data Submittal

#### Step 1.1: Request Vendor Data Submittal

**Action:**
- After purchase order issued, request vendor data per specification (DEL-15.02 Section 7: Documentation Requirements)
- Provide vendor with:
  - Specification requirements (DEL-15.02)
  - Design calculations for reference (DEL-15.03)
  - Data submittal schedule
  - Data format requirements (if any)

**Verification:**
- Vendor acknowledges data submittal requirements and schedule

**Records:**
- Data request transmittal

**Source:** Standard vendor data request process

---

#### Step 1.2: Receive Vendor Data (Rev 0)

**Action:**
- Receive initial vendor data submittal (typically designated "Rev 0")
- Log submittal in document management system
- Assign for review

**Verification:**
- Submittal is complete (per checklist: pump data sheet, motor data sheet, performance curves, outline drawings, foundation loads)
- If incomplete, return to vendor for completion before review

**Records:**
- Vendor data submittal log

**Source:** Standard document control procedure

---

### Phase 2: Vendor Data Review

#### Step 2.1: Perform Completeness Check

**Action:**
- Verify all required documents are included:
  - [ ] Pump performance data sheet
  - [ ] Pump construction data sheet
  - [ ] Motor data sheet
  - [ ] Performance curves (head-flow-efficiency-power-NPSH)
  - [ ] Outline drawing
  - [ ] Foundation loads

**Verification:**
- All items checked off

**Records:**
- Completeness checklist

**Source:** API 610 Section 8.2 (technical data requirements)

---

#### Step 2.2: Review Performance Data

**Action:**
- Review pump performance data sheet:
  - Rated flow matches specification (**TBD** m³/hr)
  - Rated head matches specification (**TBD** m)
  - Efficiency meets specification minimum
  - NPSHR is provided at rated flow and other points
  - Minimum continuous stable flow is defined

**Verification:**
- Performance data is within specification tolerances (ISO 9906 Grade 2: Flow ±7%, Head ±5%)

**Records:**
- Performance data review notes

**Source:** DEL-15.02 (specification requirements), ISO 9906 (tolerance)

---

#### Step 2.3: Verify NPSH Margin

**Action:**
- Extract vendor NPSHR at rated flow from data sheet or performance curve
- Compare to calculated NPSHA (from DEL-15.03)
- Calculate NPSH margin: **Margin = NPSHA - NPSHR**
- Verify margin ≥ 0.5m (API 610 minimum)

**Example:**
- NPSHA (DEL-15.03) = 9.8m
- Vendor NPSHR = 8.5m
- Margin = 9.8 - 8.5 = 1.3m ✓ (acceptable)

**Verification:**
- NPSH margin meets requirement

**Records:**
- NPSH margin calculation and verification

**Source:** API 610 Section 3.8 (NPSH), DEL-15.03 (calculated NPSHA)

---

#### Step 2.4: Verify Operating Point

**Action:**
- Plot vendor pump head-flow curve
- Overlay calculated system curve (from DEL-15.03)
- Identify operating point (intersection)
- Identify vendor pump best efficiency point (BEP) from performance curve
- Calculate: Operating point as % of BEP = (Q_operating / Q_BEP) × 100%
- Verify operating point is within 70–120% of BEP (API 610 preferred operating region)

**Verification:**
- Operating point is within preferred region

**Records:**
- Operating point plot and verification

**Source:** API 610 Section 3 (preferred operating region), DEL-15.03 (system curve)

---

#### Step 2.5: Review Construction Data

**Action:**
- Review pump construction data sheet:
  - Pump type matches specification (e.g., API 610 OH2)
  - Materials match specification (casing, impeller, shaft, seal per API 610 Annex G)
  - Mechanical seal type matches specification (API 682 Type 2, single seal, Plan 11)
  - Coupling type is appropriate
  - Baseplate type matches specification

**Verification:**
- Construction data complies with specification (DEL-15.02)

**Records:**
- Construction data review notes

**Source:** DEL-15.02 (specification materials and construction requirements)

---

#### Step 2.6: Review Motor Data

**Action:**
- Review motor data sheet:
  - Motor power is adequate (≥115% of pump BHP per DEL-15.03)
  - Voltage matches electrical system (coordinate with Electrical discipline) — **TBD**
  - Efficiency class is NEMA Premium or IEC IE3 minimum (per DEL-15.02)
  - Enclosure type is appropriate (TEFC, ODP, explosion-proof per hazardous area classification) — **TBD**

**Verification:**
- Motor data is suitable for application

**Records:**
- Motor data review notes; coordination with Electrical discipline

**Source:** DEL-15.02 (motor requirements), DEL-15.03 (pump power calculation)

---

#### Step 2.7: Review Dimensional Data

**Action:**
- Review outline drawing:
  - Pump and motor envelope dimensions are clear
  - Nozzle locations (suction, discharge) are dimensioned relative to pump centerline/baseplate
  - Baseplate dimensions are provided
  - Anchor bolt pattern is dimensioned
  - Lifting lug locations are shown (if applicable)

**Verification:**
- Dimensional data is adequate for installation design (DEL-15.01) and foundation design (PKG-05)

**Records:**
- Dimensional data review notes

**Source:** DEL-15.01 uses outline drawings for arrangement

---

#### Step 2.8: Review Foundation Loads

**Action:**
- Review foundation loads data:
  - Pump, motor, and baseplate weights are provided (dry and operating)
  - Static loads (vertical, horizontal, moments) are provided
  - Dynamic loads (if applicable) are provided
  - Anchor bolt requirements (number, size) are stated

**Verification:**
- Foundation loads are adequate for foundation design (PKG-05)

**Records:**
- Foundation loads data review notes; coordinate with Structural discipline

**Source:** PKG-05 uses foundation loads for foundation design

---

#### Step 2.9: Prepare Review Comments

**Action:**
- Compile review comments:
  - **Category A (Major):** Non-compliance with specification; inadequate NPSH margin; unacceptable operating point; missing critical data
  - **Category B (Minor):** Clarifications; minor dimensional discrepancies; formatting issues

- Transmit comments to vendor via procurement

**Verification:**
- All review issues documented as comments

**Records:**
- Vendor data review comment log

**Source:** Standard vendor data review comment categories

---

### Phase 3: Vendor Data Approval

#### Step 3.1: Receive Vendor Resubmittal

**Action:**
- Vendor incorporates comments and resubmits data (typically "Rev A")
- Review vendor comment responses
- Verify all Category A comments are resolved
- Verify Category B comments are addressed or explained

**Verification:**
- All comments satisfactorily addressed

**Records:**
- Comment response review

**Source:** Standard vendor data resubmittal process

---

#### Step 3.2: Perform Independent Check

**Action:**
- Checker (independent engineer) verifies critical items:
  - NPSH margin calculation is correct
  - Operating point verification is correct
  - Performance data compliance verified

**Verification:**
- Checker sign-off obtained

**Records:**
- Check sign-off documentation

**Source:** Quality requirement for critical vendor data review items

---

#### Step 3.3: Approve Data for Construction (AFC)

**Action:**
- If data is acceptable:
  - Lead Mechanical Engineer approves data
  - Stamp data as "APPROVED FOR CONSTRUCTION (AFC)"
  - Assign final revision (e.g., Rev A-AFC)
  - Transmit AFC data to:
    - DEL-15.01 (for arrangement drawings)
    - PKG-05 (for foundation design)
    - PKG-19/20 (for electrical design)
    - DEL-15.05 (for commissioning baseline)

**Verification:**
- AFC stamp and sign-off obtained
- AFC data distributed to downstream users

**Records:**
- AFC approval documentation
- AFC data distribution log

**Source:** Standard vendor data approval process

---

#### Step 3.4: Manage Subsequent Revisions (if needed)

**Action:**
- If vendor issues revised data after AFC (e.g., due to manufacturing changes):
  - Review revision for impact on downstream design
  - If minor change with no impact: Approve as revised AFC
  - If major change with impact: Coordinate with affected disciplines; may require design rework

**Verification:**
- Impact assessment performed
- Affected parties notified

**Records:**
- Revision impact assessment
- Change notification

**Source:** Configuration management for vendor data revisions

---

## Verification

### Verification Summary

| Activity | Verifier | Criteria |
|----------|----------|----------|
| **Completeness** | Reviewer | All required documents included |
| **Performance compliance** | Reviewer | Flow, head, efficiency within tolerance |
| **NPSH margin** | Reviewer + Checker | Margin ≥ 0.5m |
| **Operating point** | Reviewer + Checker | Within 70–120% of BEP |
| **Materials compliance** | Reviewer | Materials match specification |
| **Dimensional adequacy** | Reviewer | Dimensions suitable for installation/foundation design |
| **Critical items** | Checker | NPSH, operating point, major dimensions verified |
| **Approval** | Lead Engineer | Data acceptable for construction use |

**Source:** Standard vendor data verification process per Specification.md

## Records

### Documentation Outputs

The following vendor data shall be managed:

1. **Pump Data Sheets** (performance and construction) — One per pump unit
2. **Motor Data Sheets** — One per motor
3. **Performance Curves** — One set per pump model
4. **Outline Drawings** — One per pump model
5. **Foundation Loads** — One per pump model

**Source:** `_CONTEXT.md` (anticipated artifacts), API 610 Section 8.2

### Record Management

**Filing locations:**

- **Vendor submittals:** `1_Working/DEL-15.04_Pump_Data_Sheet_Package/Vendor_Submittals/` organized by pump tag and revision (Rev 0, Rev A, AFC)
- **Review records:** `1_Working/DEL-15.04_Pump_Data_Sheet_Package/Review_Records/` (review checklists, comment logs, approvals)
- **AFC data distribution:** Copies provided to downstream disciplines via transmittal

**Document control:**
- Track vendor data revisions (Rev 0, Rev A, Rev B, AFC status)
- Maintain comment log and response tracking
- Distribute AFC data to all affected disciplines

**Retention:**
- Retain vendor data for facility life (25+ years typical)

**Source:** Project document control procedures

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Vendor data content and structure
- Specification.md — Vendor data requirements and acceptance criteria
- Guidance.md — Review principles and common issues
- DEL-15.02 — Pump Technical Specification (vendor data verified against spec)
- DEL-15.03 — Pump Design Calculations (NPSH and operating point source data)
- DEL-15.01 — Pump Design Drawing Set (receives vendor outline drawings)
- DEL-15.05 — Pump Installation & Test Records (vendor data baseline for commissioning)
