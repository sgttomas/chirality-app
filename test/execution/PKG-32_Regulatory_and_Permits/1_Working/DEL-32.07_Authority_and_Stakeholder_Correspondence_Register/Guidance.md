# Guidance: DEL-32.07 Authority & Stakeholder Correspondence Register

## Purpose

Supports **Authority & Stakeholder Correspondence Register** for **PKG-32**.

**Purpose:** Tracking log for authority/stakeholder correspondence (Source: _CONTEXT.md)
**Type:** Record | **Discipline:** Project Delivery | **Responsible:** D&B Contractor
**Objective:** OBJ-6: Regulatory Compliance (audit trail, compliance tracking)

## Principles

### 1. Centralized Correspondence Tracking
The register provides a single source of truth for all authority and stakeholder correspondence. Avoids correspondence being lost or forgotten.

### 2. Audit Trail for Compliance
Regulatory compliance often requires demonstrating timely response to authority requests and fulfillment of permit conditions. The register provides an audit trail.

### 3. Paired with Correspondence Copies (DEL-32.08)
Register (DEL-32.07) is the **index/log**. Correspondence Copies (DEL-32.08) are the **actual documents**. Together they form complete correspondence management system.

## Considerations

### Register Structure (Typical Columns)

**Essential columns:**
- **Entry Date:** Date correspondence logged in register
- **Correspondence Date:** Date of correspondence occurrence
- **Authority/Stakeholder:** VFPA, DFO, Transport Canada, City of Surrey, fire authority, etc.
- **Correspondence Type:** Application, RFI, response, permit receipt, submittal, inspection, approval, meeting minutes, etc.
- **Reference Number:** Authority reference number or internal project reference number
- **Subject:** Brief description of correspondence subject
- **Action Required:** Action needed (respond by date X, provide document Y, schedule inspection Z)
- **Responsible Party:** Person/team responsible for action
- **Status:** Submitted, under review, response received, closed, etc.
- **Link to DEL-32.08:** File path or reference to correspondence copy in DEL-32.08

**Optional columns:**
- **Priority:** High/medium/low
- **Deadline:** Action deadline date
- **Notes:** Additional context

### Correspondence Types Logged

(See Datasheet Conditions for comprehensive list; key types below)

- **Permit-related:** Applications (DEL-32.01), permit receipts (DEL-32.02), permit amendments
- **Compliance-related:** VFPA submittals (DEL-32.03), DFO submittals (DEL-32.04), Transport Canada submittals (DEL-32.05), code compliance inspections (DEL-32.06)
- **RFIs:** Authority requests for information; Contractor responses
- **Inspections:** Inspection requests, inspection reports, inspection deficiencies, re-inspections
- **Approvals:** Authority approvals, confirmations, acknowledgments
- **Meetings:** Meeting invitations, meeting minutes (authority meetings)
- **Incidents:** Incident notifications (spills, work stoppages, etc.)
- **Stakeholder:** Stakeholder correspondence (if in register scope — **TBD**)

### Interface with DEL-32.01 through DEL-32.06

All permit and compliance deliverables (DEL-32.01-32.06) reference the correspondence register (DEL-32.07) in their procedures. Key interface points:

- **DEL-32.01 Step 5.5:** Log permit application submission in DEL-32.07
- **DEL-32.02 Steps 2.3, 3.2:** Log permit receipt in DEL-32.07
- **DEL-32.03-32.06 Steps 4, various:** Log compliance submittals and inspections in DEL-32.07

**Consistency required:** Ensure all procedures that reference DEL-32.07 are followed; correspondence is logged per procedures.

### Interface with DEL-32.08 (Correspondence Copies)

- **Register entry created (DEL-32.07)** → **Correspondence copy filed (DEL-32.08)** → **Register entry updated with link to DEL-32.08 copy**
- **Two-way linkage:** Register entry links to DEL-32.08 file path; DEL-32.08 file name includes register entry reference number
- **Audit efficiency:** Register provides searchable index; DEL-32.08 provides actual documents for review

## Trade-offs

### Real-Time Logging vs Batch Logging
**Trade-off:** Log correspondence immediately as it occurs (real-time, most accurate) vs log in batches (e.g., weekly, more efficient but risk of missed items).
**Recommendation:** Real-time or daily logging; correspondence can be forgotten if not logged promptly.

### Comprehensive Logging vs Selective Logging
**Trade-off:** Log all authority/stakeholder correspondence (comprehensive audit trail, higher effort) vs log only formal submissions/approvals (less effort, potential gaps).
**Recommendation:** Comprehensive logging; audit and compliance requirements typically require full correspondence trail.

## Examples

**Example Register Entries:**

| Entry Date | Corr. Date | Authority | Type | Ref # | Subject | Action Required | Responsible | Status | DEL-32.08 Link |
|------------|------------|-----------|------|-------|---------|-----------------|-------------|--------|----------------|
| 2026-03-15 | 2026-03-15 | VFPA | Application | PER-2026-123 | VFPA PER Application Submitted | Track application review | Permit Coord. | Under Review | DEL-32.08/VFPA/2026-03-15_PER_Application.pdf |
| 2026-04-10 | 2026-04-09 | VFPA | RFI | PER-2026-123-RFI-01 | VFPA requests additional marine env. info | Respond by 2026-04-24 | Env. Lead | In Progress | DEL-32.08/VFPA/2026-04-09_RFI-01.pdf |
| 2026-04-22 | 2026-04-22 | VFPA | Response | PER-2026-123-RFI-01-RESP | Response to VFPA RFI-01 submitted | Track VFPA acknowledgment | Permit Coord. | Submitted | DEL-32.08/VFPA/2026-04-22_RFI-01_Response.pdf |
| 2026-05-01 | 2026-05-01 | VFPA | Approval | PER-2026-123-APPROVAL | VFPA PER Approval Received | File in DEL-32.02; extract conditions for DEL-32.03 | Permit Coord. | Closed | DEL-32.08/VFPA/2026-05-01_PER_Approval.pdf |
| 2026-06-10 | 2026-06-10 | DFO | Submittal | DFO-MON-202606 | Marine mammal monitoring report (June) | Track DFO acknowledgment | QA/QC Mgr. | Submitted | DEL-32.08/DFO/2026-06-10_Monitoring_Report_June.pdf |
| 2026-07-15 | 2026-07-15 | City Surrey | Inspection | BLDG-INS-2026-045 | Foundation inspection passed | Proceed to framing | Construction Mgr. | Closed | DEL-32.08/Building/2026-07-15_Foundation_Inspection.pdf |
