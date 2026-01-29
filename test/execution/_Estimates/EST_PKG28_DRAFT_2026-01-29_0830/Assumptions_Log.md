# Assumptions Log — PKG-28 Design Verification Estimate

**Snapshot ID:** EST_PKG28_DRAFT_2026-01-29_0830
**Package Scope:** PKG-28 Design Verification
**Date:** 2026-01-29

---

## Assumption Summary

This log documents all assumptions and allowances used in the PKG-28 estimate where explicit quantities, rates, or pricing were not available from project-specific sources.

**Context:** No vendor quotes, budgetary proposals, or project rate tables were available for design verification services (see Source_Index.md). All cost estimates use fallback allowances based on typical EPC design-build project experience.

---

## A-001: Independent Design Verification (IDV) Services — DEL-28.01

**Assumption:** IDV services across all disciplines and submission stages estimated at $350,000 CAD allowance.

**Why Needed:** No vendor quotes from independent design verification firms. IDV scope (disciplines, review depth, iteration requirements) not specified in decomposition.

**Impacted WBS/CBS:** PKG-28 / DEL-28.01 / Engineering (E)

**Cost Impact:** $350,000 CAD
- **Range:** $250,000 - $500,000 (±43%)
- **Basis:** Typical IDV cost for multi-discipline industrial design-build project:
  - 8 major disciplines requiring IDV (Civil, Structural, Marine, Process, Mech, Elec, I&C, Specialty)
  - 4 submission stages per discipline (30%, 60%, 90%, IFC)
  - 32 reviews total at $10,000-$12,000 per review average
  - Range reflects review complexity variation by discipline

**Confidence:** LOW

**Resolution Path:**
1. Clarify IDV requirements with Employer (which disciplines require third-party vs. internal review)
2. Obtain budgetary quotes from independent engineering review firms
3. Define review scope and depth expectations per discipline

---

## A-002: Design Coordination Activities — DEL-28.03

**Assumption:** Inter-discipline design coordination activities estimated at $150,000 CAD allowance.

**Why Needed:** No project rate tables for coordination effort. Design duration and coordination complexity not specified in decomposition.

**Impacted WBS/CBS:** PKG-28 / DEL-28.03 / Project Management (PM)

**Cost Impact:** $150,000 CAD (split: $80k coordination meetings + $45k clash detection + $25k RFI management)
- **Range:** $100,000 - $200,000 (±33%)
- **Basis:** Typical design coordination cost for 210-deliverable project:
  - Design duration: 18-24 months active design
  - Coordination effort: 1 coordinator FTE equivalent ($4,000-$5,000/month)
  - Clash detection: BIM coordination for 36 packages
  - RFI management: 200-400 RFIs over design duration

**Confidence:** LOW

**Resolution Path:**
1. Develop design schedule with coordination milestones
2. Define clash detection frequency and model complexity
3. Estimate RFI volume based on similar projects

---

## A-003: VFPA IP Review Responses (Technical) — DEL-28.02

**Assumption:** VFPA IP review technical response preparation estimated at $95,000 CAD allowance.

**Why Needed:** No cost data for VFPA project review process. IP review submission count and complexity not specified.

**Impacted WBS/CBS:** PKG-28 / DEL-28.02 / Engineering (E)

**Cost Impact:** $95,000 CAD
- **Range:** $60,000 - $140,000 (±47%)
- **Basis:** Typical port authority IP review response effort:
  - 4-6 major submission cycles (align with design milestones)
  - Technical response effort: $15,000-$25,000 per cycle
  - Response documentation: formal written responses to VFPA comments
  - Iteration: assume 1-2 rounds of clarification per submission

**Confidence:** LOW

**Resolution Path:**
1. Obtain VFPA project review requirements and typical comment volume
2. Clarify submission schedule and response expectations
3. Review historical IP review effort for similar VFPA projects

---

## A-004: VFPA IP Review Coordination — DEL-28.02

**Assumption:** VFPA IP review coordination and scheduling effort estimated at $42,300 CAD allowance.

**Why Needed:** No project data for authority coordination effort. VFPA interface requirements not detailed.

**Impacted WBS/CBS:** PKG-28 / DEL-28.02 / Project Management (PM)

**Cost Impact:** $42,300 CAD
- **Range:** $30,000 - $60,000 (±42%)
- **Basis:** Typical authority coordination effort:
  - Coordination meetings: monthly coordination over 18-24 month design (18-24 meetings)
  - Scheduling: submission tracking, review window management
  - Interface management: VFPA liaison, comment distribution, response tracking

**Confidence:** LOW

**Resolution Path:**
1. Clarify VFPA meeting requirements and interface expectations
2. Define coordination staffing model (dedicated coordinator vs. part-time allocation)
3. Establish submission schedule and review windows

---

## A-005: Clash Detection & Resolution — DEL-28.03

**Assumption:** BIM coordination and clash detection services estimated at $45,000 CAD allowance (included in A-002 total).

**Why Needed:** No rate tables for BIM coordination services. Model complexity and clash detection frequency not specified.

**Impacted WBS/CBS:** PKG-28 / DEL-28.03 / Project Management (PM)

**Cost Impact:** $45,000 CAD
- **Range:** $30,000 - $65,000 (±44%)
- **Basis:** Typical BIM coordination for industrial facility:
  - Model coordination: 36 packages requiring model integration
  - Clash detection cycles: bi-weekly during active design (40-50 cycles)
  - Resolution tracking: clash report maintenance and closeout

**Confidence:** LOW

**Resolution Path:**
1. Define BIM coordination requirements and model complexity
2. Establish clash detection frequency and review cycle
3. Clarify software/platform requirements (Navisworks, Revit, etc.)

---

## A-006: RFI Management — DEL-28.03

**Assumption:** RFI log maintenance, response coordination, and tracking estimated at $25,000 CAD allowance (included in A-002 total).

**Why Needed:** No historical data on RFI volume or response effort.

**Impacted WBS/CBS:** PKG-28 / DEL-28.03 / Project Management (PM)

**Cost Impact:** $25,000 CAD
- **Range:** $15,000 - $40,000 (±60%)
- **Basis:** Typical RFI management for multi-discipline project:
  - RFI volume: 200-400 RFIs over design duration (typical for 210 deliverables)
  - Tracking effort: $75-$125 per RFI for logging, routing, response coordination
  - Documentation: RFI log maintenance, status tracking, closeout

**Confidence:** LOW

**Resolution Path:**
1. Estimate RFI volume based on similar project historical data
2. Define RFI management system and workflow
3. Clarify response turnaround expectations

---

## A-007: IDV Report Documentation — DEL-28.01

**Assumption:** Final compilation and archival of IDV reports included in IDV services allowance (A-001); no separate cost line.

**Why Needed:** Documentation effort typically included in IDV service provider scope.

**Impacted WBS/CBS:** PKG-28 / DEL-28.01 / Engineering (E)

**Cost Impact:** $0 (included in A-001)
- **Basis:** IDV report compilation and archival typically included in IDV service contract
- No separate documentation allowance required

**Confidence:** MED

**Resolution Path:** Confirm IDV documentation requirements are included in service provider scope.

---

## A-008: Design Duration — 18-24 Months

**Assumption:** Active design phase duration of 18-24 months for time-based cost calculations.

**Why Needed:** Design schedule not available in decomposition. Duration affects coordination effort, staffing, and meeting costs.

**Impacted WBS/CBS:** All PM line items (time-based coordination costs)

**Cost Impact:** Affects A-002, A-004, A-005, A-006 (total ~$192k PM costs)
- **Range:** Duration could be 15-30 months depending on project schedule
- **Sensitivity:** ±20% duration variance = ±$25-40k PM cost impact

**Confidence:** MED

**Resolution Path:**
1. Obtain project master schedule with design milestones
2. Clarify design phase duration from notice to proceed to IFC
3. Adjust coordination effort based on actual duration

---

## Assumption Summary Table

| Assumption ID | Description | Impacted CBS | Amount (CAD) | Range (CAD) | Confidence | Resolution Path |
|---------------|-------------|--------------|--------------|-------------|------------|-----------------|
| A-001 | IDV services (all disciplines/stages) | E | $350,000 | $250k-$500k | LOW | IDV vendor quotes |
| A-002 | Design coordination (18-24 mo) | PM | $150,000 | $100k-$200k | LOW | Design schedule |
| A-003 | VFPA IP review technical responses | E | $95,000 | $60k-$140k | LOW | VFPA requirements |
| A-004 | VFPA IP coordination effort | PM | $42,300 | $30k-$60k | LOW | VFPA interface plan |
| A-005 | Clash detection & resolution | PM | $45,000 | $30k-$65k | LOW | BIM requirements |
| A-006 | RFI management | PM | $25,000 | $15k-$40k | LOW | Historical RFI data |
| A-007 | IDV documentation | E | $0 | Incl. A-001 | MED | Confirm in contract |
| A-008 | Design duration (18-24 mo) | All PM | N/A | 15-30 mo | MED | Project schedule |

**Total Direct Allowances:** $664,000 CAD (base, before indirects/contingency)

**Allowance Range:** $485,000 - $905,000 CAD (Low to High scenarios)

**Overall Confidence:** LOW — All line items use fallback allowances without project-specific vendor quotes or detailed scope definition.

---

**Assumptions Log Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete (all allowances documented)
