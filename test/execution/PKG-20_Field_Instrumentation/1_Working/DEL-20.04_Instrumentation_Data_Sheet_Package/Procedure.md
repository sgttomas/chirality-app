# Procedure: DEL-20.04 Instrumentation Data Sheet Package

## Purpose

Defines process for **producing** Instrumentation Data Sheet Package within **PKG-20 Field Instrumentation**.

**Deliverable Scope:** Defines and substantiates instrumentation in accordance with ER requirements.

**Source:** Decomposition document, DEL-20.04 (line 499)

## Prerequisites

**Dependencies:** See `_DEPENDENCIES.md` — **NOT_TRACKED**

**Typical Inputs:**
- P&IDs and instrument list (tag numbers, service descriptions)
- DEL-20.02 specification (requirements)
- DEL-20.03 calculations (ranges, parameters)
- Procurement requirements (vendor list, delivery schedule)

**Personnel:** I&C Engineer (originator), Procurement Coordinator (vendor interface), Independent Checker (reviewer), I&C Lead (approver)

**Source:** **ASSUMPTION** based on typical data sheet input requirements

## Steps

**Overview:** Implements Specification.md requirements through three-phase lifecycle (design, procurement, as-built).

### Step 1: Template Development

**Objective:** Create data sheet templates aligned with DEL-20.02 specification.

**Activities:**
- Develop templates by instrument type (level, pressure, temperature, flow)
- Include all specification requirements (ranges, accuracy, materials, hazardous area, electrical)
- Add fields for vendor information (manufacturer, model, certifications)
- Coordinate format with procurement (usable for RFQs)

**Deliverable:** Data sheet templates

**Source:** Specification FR-1, FR-2

### Step 2: Design Data Sheet Population

**Objective:** Complete design data sheets with engineering requirements.

**Activities:**
- Extract tag numbers and service descriptions from P&IDs
- Populate ranges and parameters from DEL-20.03 calculations
- Populate requirements from DEL-20.02 specification
- Add environmental and hazardous area requirements
- Mark vendor-to-complete fields (manufacturer, model, price, delivery)

**Deliverable:** Design data sheets (ready for RFQ issuance)

**Verification:** Independent check, cross-check with specifications and calculations

**Source:** Specification FR-2, FR-3

### Step 3: Vendor Solicitation and Evaluation

**Objective:** Obtain vendor quotations and evaluate compliance.

**Activities:**
- Issue data sheets to vendors with RFQ packages (procurement responsibility)
- Vendors complete data sheets with proposed equipment specifications
- Review vendor data sheets for compliance with requirements
- Document non-compliances and request clarifications
- Evaluate vendor proposals (technical + commercial)
- Approve vendor data sheets for procurement

**Deliverable:** Approved vendor data sheets, purchase orders

**Source:** Specification INT-1; **ASSUMPTION** based on typical procurement workflow

### Step 4: As-Built Update

**Objective:** Update data sheets with actual installed equipment data.

**Activities:**
- Update data sheets with equipment serial numbers (from field installation)
- Update with test results from DEL-20.05 (calibration data, loop checks)
- Update with field modifications (if installation differs from design)
- Verify as-built data matches installed equipment
- Issue final as-built data sheets

**Deliverable:** As-built data sheets (final facility records)

**Verification:** Field verification, cross-check with DEL-20.05 test records

**Source:** Specification QR-3; **ASSUMPTION** based on typical as-built documentation

### Step 5: Handover to Operations

**Objective:** Provide final data sheets to facility operations.

**Activities:**
- Compile complete data sheet package (all instruments)
- Include in operations and maintenance (O&M) manuals
- Integrate with facility asset management system (**TBD**: System and format)
- Provide to operations for maintenance planning and spare parts procurement

**Deliverable:** Final data sheet package delivered to Owner

**Source:** **ASSUMPTION** based on typical facility turnover; supports OBJ-9 (Lifecycle Cost Optimization)

## Verification

**Verification Activities:**

- Design data sheets: independent check, specification compliance review
- Vendor data sheets: technical compliance review, bid evaluation
- As-built data sheets: field verification, test record cross-check

**Acceptance Criteria:**

Design phase: Complete, compliant with specification and calculations, approved for RFQ. Procurement phase: Vendor data compliant, approved for purchase. As-built phase: Matches installed equipment, includes test data.

**Source:** Specification Verification section

## Records

**Documentation Outputs:**

- Level transmitter data sheets
- Pressure transmitter data sheets
- Flow instrument data sheets
- Temperature element data sheets

**Organization:** **TBD** — By instrument type, by area, or by tag number

**Record Management:**

- Design data sheets in `1_Working/`
- Vendor submittals tracked separately (procurement folder structure)
- As-built data sheets in `3_Issued/` as permanent records
- Retention: **TBD** — Permanent facility records

**Source:** README.md lifecycle folder structure; **ASSUMPTION** on permanent record retention

**Project Objective Alignment:**

Supports **OBJ-1: Safe & Reliable Operation** and **OBJ-9: Lifecycle Cost Optimization** (data sheets enable proper procurement, installation, and lifecycle maintenance).

**Source:** Decomposition Section 6 (lines 780, 788)

## Cross-Document Traceability

This Procedure defines the production workflow for DEL-20.04. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Datasheet.md | Factual identification, attributes, conditions, references | Conditions § defines data sheet purpose; Construction § defines three-phase workflow |
| Specification.md | Requirements and verification criteria | FR-1 to FR-4 define what to produce; QR-1 to QR-3 define quality requirements |
| Guidance.md | Engineering rationale and decision context | Principles explain three-phase lifecycle; Trade-off informs standardization decisions |

**Procedure-to-Specification Mapping:**

| Procedure Step | Specification Requirement | What Is Implemented |
|----------------|--------------------------|---------------------|
| Step 1 | FR-1, PR-1 | Template development |
| Step 2 | FR-2, FR-3, PR-2 | Design data sheet population |
| Step 3 | FR-4, INT-1, QR-2 | Vendor solicitation and evaluation |
| Step 4 | INT-2, QR-3 | As-built update |
| Step 5 | INT-3, Documentation | Handover to operations |
