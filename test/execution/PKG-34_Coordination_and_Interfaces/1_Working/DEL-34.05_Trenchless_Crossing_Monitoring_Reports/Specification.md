# Specification: DEL-34.05 Trenchless Crossing Monitoring Reports

## Scope

This specification defines the requirements for **Trenchless Crossing Monitoring Reports** within **PKG-34 Coordination & Interfaces**.

**Purpose:** Documents monitoring of trenchless utility crossings to verify settlement and infrastructure condition are within acceptable limits; supports design verification and regulatory approvals (per Decomposition line 753, `_CONTEXT.md`).

**Objective alignment:** Supports OBJ-5 "Terminal Continuity" by ensuring utility crossings do not disrupt existing infrastructure operations (Decomposition lines 63, 784).

**Anticipated deliverable artifacts:** Settlement monitoring reports, Condition monitoring reports

**Inclusions:** Pre-installation baseline surveys, monitoring during trenchless installation, post-installation monitoring, data analysis, threshold compliance assessment, recommendations

**Exclusions:** Trenchless crossing design (covered by relevant utility design packages); trenchless installation execution (construction activity)

## Requirements

### Functional Requirements

**FR-1: Monitoring Plan**
- Monitoring plan shall be developed prior to trenchless installation commencement, including:
  - Monitoring point locations (settlement monuments, condition inspection points)
  - Instrumentation types and specifications
  - Monitoring frequency (daily during installation, weekly/monthly post-installation)
  - Alert and action thresholds (settlement limits, condition triggers)
  - Reporting format and distribution
- Monitoring plan approved by geotechnical engineer and infrastructure owners (rail operators, road authorities)
- **Source:** **ASSUMPTION**: Geotechnical monitoring best practice; **TBD**: Infrastructure owner requirements

**FR-2: Settlement Monitoring**
- Settlement monitoring shall measure ground settlement above and around trenchless crossing
- Monitoring points located per geotechnical design (typically along crossing alignment and perpendicular transects)
- Instrumentation: Survey monuments (precise leveling), settlement gauges, inclinometers (lateral movement)
- Baseline measurements prior to installation; continuous monitoring during installation; post-installation monitoring until settlement stabilizes
- **Source:** **ASSUMPTION**: Geotechnical settlement monitoring standards (ASTM, ISO); Datasheet Construction section

**FR-3: Condition Monitoring**
- Condition monitoring shall document infrastructure condition (rail tracks, roads, buildings) before, during, and after trenchless installation
- Pre-installation baseline condition survey (photographs, condition ratings, existing defects)
- Monitoring during installation (daily visual inspections, weekly detailed inspections)
- Post-installation condition assessments (immediate, 1 month, 3 months, 6 months, 12 months) — **TBD**: Duration per infrastructure owner requirements
- **Source:** **ASSUMPTION**: Infrastructure condition monitoring best practice; Datasheet Construction section

**FR-4: Alert and Action Thresholds**
- Alert thresholds: Settlement or movement approaching design limits; trigger increased monitoring frequency and engineering review
- Action thresholds: Settlement or movement exceeding design limits; trigger installation suspension, corrective action, infrastructure owner notification
- Thresholds defined per geotechnical design, infrastructure owner requirements, regulatory permits
- **TBD** — Specific alert/action thresholds
- **Source:** **ASSUMPTION**: Geotechnical threshold management per infrastructure protection protocols

**FR-5: Reporting Content**
- Settlement monitoring reports shall include (per Datasheet Construction section):
  - Executive summary, monitoring data, data analysis, settlement trends, threshold compliance assessment, recommendations
- Condition monitoring reports shall include:
  - Executive summary, baseline condition, condition during/after installation, damage assessment (if any), recommendations
- **Source:** Datasheet Construction section; **ASSUMPTION**: Geotechnical reporting standards

### Performance Requirements

**PR-1: Monitoring Frequency**
- Baseline surveys completed before trenchless installation
- Daily monitoring during active trenchless installation
- Weekly comprehensive reports during active installation
- Monthly/quarterly monitoring during post-installation period (until settlement stabilizes)
- **Source:** **ASSUMPTION**: Geotechnical monitoring frequency standards; Datasheet Attributes

**PR-2: Data Accuracy**
- Settlement measurements accurate to required precision (typically ±1mm for survey monuments)
- Condition assessments documented with photographs and objective condition ratings
- Data verified and quality-checked before reporting
- **Source:** **ASSUMPTION**: Geotechnical instrumentation accuracy standards

**PR-3: Timeliness**
- Daily monitoring summaries issued same day or next business day (flag threshold exceedances immediately)
- Weekly comprehensive reports issued within 3 business days
- Final reports issued within 30 days of monitoring completion
- **TBD** — Specific reporting timelines per infrastructure owner requirements
- **Source:** **ASSUMPTION**: Timely reporting for infrastructure protection

**PR-4: Threshold Response**
- Alert threshold exceedances: Engineering review within 24 hours; increased monitoring frequency
- Action threshold exceedances: Immediate notification to project management, infrastructure owner, geotechnical engineer; installation suspension until corrective action implemented
- **Source:** **ASSUMPTION**: Infrastructure protection and safety protocols

### Interface Requirements

**IR-1: Infrastructure Owner Coordination**
- Monitoring plan coordinated with infrastructure owners (rail operators, road authorities) prior to implementation
- Monitoring reports distributed to infrastructure owners per agreed schedule
- Threshold exceedances reported immediately to infrastructure owners
- Infrastructure owner access to monitoring data (if required)
- **Source:** **ASSUMPTION**: Infrastructure owner coordination requirements; relation to DEL-34.02 (Interface Agreements)

**IR-2: Geotechnical Design Integration**
- Monitoring plan aligned with geotechnical design assumptions and settlement predictions
- Monitoring data used to verify geotechnical design performance
- Geotechnical engineer reviews monitoring data and provides interpretation/recommendations
- **Source:** **ASSUMPTION**: Integration of monitoring with geotechnical design

**IR-3: Regulatory Approvals**
- Monitoring reports submitted to regulatory authorities as required for permits (rail authority, environmental permits)
- Monitoring data supports design verification and regulatory compliance
- **TBD** — Specific regulatory submission requirements
- **Source:** **ASSUMPTION**: Regulatory approval support; Datasheet Attributes

### Quality Requirements

**QR-1: Instrumentation Calibration**
- All monitoring instrumentation calibrated per manufacturer specifications and geotechnical standards
- Calibration certificates maintained
- Regular verification of instrumentation performance
- **Source:** **ASSUMPTION**: Geotechnical instrumentation quality assurance (ISO, ASTM)

**QR-2: Data Quality Assurance**
- Monitoring data reviewed and quality-checked before reporting
- Data anomalies investigated and resolved
- Data management system with version control and backup
- **Source:** **ASSUMPTION**: ISO 9001 data quality requirements

**QR-3: Professional Oversight**
- Monitoring activities supervised by qualified geotechnical engineer or monitoring specialist
- Monitoring reports prepared by or reviewed by professional engineer (P.Eng. or equivalent)
- **Source:** **ASSUMPTION**: Professional engineering practice requirements

## Standards

**Applicable standards:**
- **Geotechnical:** ASTM geotechnical standards (settlement monitoring, instrumentation); ISO geotechnical standards
- **Railway:** AREMA (American Railway Engineering and Maintenance-of-Way Association); Transport Canada rail safety
- **Roads:** Transportation Association of Canada (TAC); Provincial highway standards
- **ISO 9001** (Quality Management — data quality, document control)
- **ISO 14001** (Environmental Management — ground disturbance, settlement impacts)
- **Employer's Requirements** — **TBD** — **location TBD**

## Verification

**Verification:**
- Monitoring plan review: Approved by geotechnical engineer and infrastructure owners
- Data accuracy: Instrumentation calibrated; data quality-checked
- Threshold compliance: Settlement and condition within alert/action thresholds (or exceedances properly managed)
- Report completeness: All required content per FR-5 included
- Professional review: Reports reviewed/signed by professional engineer

**Acceptance criteria:**
- Settlement within design limits (or exceedances managed with corrective action)
- No unacceptable damage to existing infrastructure
- Infrastructure owner acceptance of monitoring reports and results
- Regulatory approval obtained (if monitoring required for permits)

**Sign-off:**
- Originator: Geotechnical engineer or monitoring specialist
- Reviewer: D&B Contractor project engineer
- Approver: D&B Contractor project manager
- External approval: Infrastructure owners, regulatory authorities (as applicable)

## Documentation

**Required outputs:**
- Settlement monitoring reports (daily summaries, weekly comprehensive, monthly/quarterly, final)
- Condition monitoring reports (baseline, during installation, post-installation assessments, final)

**Supporting documentation:**
- Monitoring plan (instrumentation, frequencies, thresholds)
- Instrumentation calibration certificates
- Raw monitoring data (survey data, photographs, inspection checklists)
- Threshold exceedance notifications and corrective action records
- Infrastructure owner correspondence and approvals

**Documentation requirements:**
- Format: Professional engineering report format with P.Eng. seal
- Retention: Long-term (7+ years) for infrastructure monitoring records — **TBD**
- Distribution: Infrastructure owners, D&B Contractor, Employer, geotechnical engineer, regulatory authorities (as applicable)

**Cross-references:** See Datasheet.md, Guidance.md, Procedure.md
