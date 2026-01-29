# Source Index — PKG-35 Training & Handover Estimate

**Snapshot ID:** EST_PKG35_DRAFT_2026-01-29_1200
**Package:** PKG-35 Training & Handover
**Date:** 2026-01-29

---

## Source Discovery Summary

| Source Category | Found | Used | Notes |
|-----------------|-------|------|-------|
| Vendor quotes / budgetary proposals | 0 | 0 | None available |
| Project rate tables | 0 | 0 | None in `_Estimates/_RateTables/` |
| Deliverable documents (quantity sources) | 5 | 5 | DEL-35.01 through DEL-35.05 |
| Reference documents | 0 | 0 | Employer's Requirements not parsed |
| Historical estimates | 0 | 0 | None available for training/handover |
| Fallback typical model | 1 | 1 | AGENT_ESTIMATING embedded model |

---

## 1. Explicit Pricing Sources (Priority 1)

### 1.1 Vendor Quotes

**Status:** None found

**Search Locations:**
- `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/` — empty
- PKG-35 deliverable folders — no pricing documents
- `_REFERENCES.md` files — no pricing references

**Impact:** All pricing uses fallback allowances (Confidence = LOW)

---

### 1.2 Budgetary Proposals

**Status:** None found

**Search Locations:**
- Workspace root — no proposal documents
- PKG-35 deliverable `_REFERENCES.md` — no budgetary references

**Impact:** Cannot validate training provider or OEM training costs

---

## 2. Rate Tables / Cost Libraries (Priority 2)

### 2.1 Project Rate Tables

**Status:** None found

**Search Location:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/`

**Result:** Directory exists but contains no rate tables

**Impact:** Cannot apply project-specific labor rates for training development or site reinstatement

---

### 2.2 Historical Cost Data

**Status:** None found

**Search Locations:**
- Previous estimate snapshots — reviewed but contain package-specific data, not reusable rates
- No training/handover historical database

**Impact:** Allowances based on industry-typical values only

---

## 3. Quantity Sources (Priority 3)

### 3.1 Deliverable Documents

**Status:** Found and used

**Documents Reviewed:**

| Document | Location | Quantities Extracted |
|----------|----------|---------------------|
| DEL-35.01 Datasheet.md | PKG-35_Training_and_Handover/1_Working/DEL-35.01_Training_Materials/ | Training categories (5), artifact types |
| DEL-35.02 Datasheet.md | PKG-35_Training_and_Handover/1_Working/DEL-35.02_Training_Installation_and_Test_Records/ | Training population categories, record types |
| DEL-35.03 Datasheet.md | PKG-35_Training_and_Handover/1_Working/DEL-35.03_Handover_Documentation/ | Handover document types, certificate types |
| DEL-35.04 Datasheet.md | PKG-35_Training_and_Handover/1_Working/DEL-35.04_Site_Reinstatement_Installation_and_Test_Records/ | Reinstatement activity categories |
| DEL-35.05 Datasheet.md | PKG-35_Training_and_Handover/1_Working/DEL-35.05_Defects_Liability_Installation_and_Test_Records/ | Defects record types, warranty period (TBD) |

**Quantities Successfully Extracted:**
- Deliverable artifact types: 5 deliverables with types specified
- Training categories: 5 (process, mechanical, electrical, control/instrumentation, safety)
- Training population categories: Operations, maintenance, management, HSE
- Major systems for OEM training: 8 systems (inferred from facility scope)
- Handover document types: Certificates, checklists, indexes
- Site reinstatement categories: Temp facilities removal, cleanup, restoration, environmental closeout
- Defects record types: Notification, assessment, rectification, completion, warranty claims

**Quantities NOT Extracted:**
- Specific training hours per module
- Number of trainees by role
- Site reinstatement physical quantities (areas, volumes)
- Defects liability workload (defect count, rectification hours)

---

### 3.2 Decomposition Document

**Status:** Found and used

**Document:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

**Quantities Extracted:**
- Package scope: "Staff training, site clearance, reinstatement, handover support, defects liability support"
- Deliverable count: 5
- Facility parameters: 1,000,000 MT/a, 45,000 MT storage, 32 railcar stations, 3 tanks
- Project scale: 36 packages, 210 deliverables (indicates training complexity)

---

### 3.3 Reference Documents

**Status:** Not parsed (TBD)

**Documents Referenced:**
- Employer's Requirements Volume 2 Part 1 — `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_1_Employers_Requirements.pdf`
- Employer's Requirements Volume 2 Part 2 — `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_2_Employers_Requirements.pdf`
- Employer's Requirements Volume 2 Part 3 — `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_3_Employers_Requirements.pdf`

**Impact:** Training requirements, handover criteria, and defects liability terms from Employer's Requirements not incorporated (marked TBD in deliverables)

---

## 4. Fallback Typical Model (Priority 4)

### 4.1 Model Usage

**Status:** Primary pricing basis (no higher-priority sources available)

**Model:** AGENT_ESTIMATING embedded fallback typical model

**Components Used:**
- Indirects factors (CI, P, PM)
- Contingency baseline percentages
- Allowance sizing guidance for training and handover activities

**Decision Reference:** D-005 (Use fallback model for pricing)

---

### 4.2 Allowance Basis

Allowances sized using industry-typical values for:

| Activity | Typical Range | Selected Value | Rationale |
|----------|---------------|----------------|-----------|
| Training materials development | $150k - $400k | $285,000 | 5 major categories, multi-discipline facility |
| OEM training (per system) | $15k - $40k | $25,000 avg | 8 systems, typical OEM rates |
| Contractor training | $75k - $150k | $100,000 | Operations, maintenance, safety programs |
| Site reinstatement | $200k - $500k | $350,000 | Industrial terminal, moderate temp facilities |
| Defects liability (12 mo) | $100k - $300k | $165,000 | Typical D&B warranty support |

**Confidence:** LOW for all allowances (no project-specific validation)

---

## 5. Sources NOT Available (Gaps)

| Source Type | Expected Location | Impact |
|-------------|-------------------|--------|
| OEM training quotes | Equipment supplier proposals | Cannot validate OEM training costs |
| Training provider quotes | Procurement/tender documents | Cannot validate contractor training costs |
| Site reinstatement quotes | Construction tender documents | Cannot validate reinstatement costs |
| Project rate tables | `_Estimates/_RateTables/` | Cannot apply project-specific labor rates |
| Employer staffing plan | Employer-provided document | Training population assumed |
| Contract terms | Design & Build Contract | Defects liability period assumed |
| Handover acceptance criteria | Employer's Requirements | Handover scope assumed |

---

## 6. Recommended Sources to Obtain

### High Priority (Significant Cost Impact)

1. **OEM Training Quotes**
   - Request budgetary quotes from equipment suppliers (PKG-10 through PKG-16, PKG-19, PKG-23, PKG-24)
   - Impact: Validate $200k+ of OEM training costs

2. **Site Reinstatement Quotes**
   - Obtain contractor quotes for temp facilities removal and site restoration
   - Impact: Validate $350k site reinstatement allowance

3. **Training Provider Quotes**
   - Obtain quotes for technical writing and training delivery services
   - Impact: Validate $385k+ of training development and delivery costs

### Medium Priority (Scope Clarification)

4. **Employer Staffing Plan**
   - Confirm training population and roles
   - Impact: Scope training delivery effort

5. **Contract Terms**
   - Confirm defects liability period and response requirements
   - Impact: Scope defects liability support

6. **PKG-00 Site Establishment Scope**
   - Confirm temporary facilities to be removed
   - Impact: Scope site reinstatement work

---

## Source Index Summary

| Priority | Sources Found | Sources Used | Coverage |
|----------|---------------|--------------|----------|
| 1 - Quotes | 0 | 0 | 0% |
| 2 - Rate Tables | 0 | 0 | 0% |
| 3 - Quantity Sources | 5 | 5 | 100% (deliverable docs) |
| 4 - Fallback Model | 1 | 1 | 100% (pricing basis) |

**Overall Pricing Source Confidence:** LOW (100% fallback-based)

---

**Source Index Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Snapshot:** EST_PKG35_DRAFT_2026-01-29_1200
