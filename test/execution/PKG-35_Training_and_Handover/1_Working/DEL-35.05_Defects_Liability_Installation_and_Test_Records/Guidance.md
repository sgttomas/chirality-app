# Guidance: DEL-35.05 Defects Liability Installation & Test Records

## Purpose

Defects liability records document defects identified during warranty period after handover (cross-reference DEL-35.03) and their rectification, demonstrating Contractor fulfillment of warranty obligations.

*Source: _CONTEXT.md; cross-reference DEL-35.03*

## Principles

**Principle 1: Warranty Obligation Fulfillment**
Defects liability period (typically 12 months from Taking Over) is Contractor's warranty period to rectify defects in design, materials, or workmanship at no cost to Employer (per contract).

*Source: **ASSUMPTION** — typical Design & Build warranty provisions*

**Principle 2: Operational Facility Context**
Defects liability occurs while facility is operational under Employer control — different dynamics than construction phase:
- Contractor is visitor requiring site access permission
- Work must minimize operational disruption (per **OBJ-5: Terminal Continuity**)
- Safety-critical defects require immediate response (per **OBJ-1: Safe & Reliable Operation**)

*Source: Decomposition Section 2 (OBJ-1, OBJ-5)*

**Principle 3: Lifecycle Cost Optimization (OBJ-9)**
Effective defects liability management supports **OBJ-9: Lifecycle Cost Optimization** by:
- Rectifying defects before Employer incurs operational costs
- Preventing defect escalation (small issues becoming major failures)
- Maintaining facility reliability during critical early operations period
- Building Employer confidence in facility quality and Contractor support

*Source: Decomposition Section 2 (OBJ-9), Section 6 (DEL-35.01-35.05 support OBJ-9)*

**Principle 4: Customer Relationship Management**
Defects liability period is opportunity to build positive post-handover relationship with Employer through responsive defect rectification, or risk damaging relationship through poor responsiveness.

*Source: **ASSUMPTION** — customer satisfaction principle per ISO 10002*

## Considerations

**Consideration 1: Defect vs. Employer Issue**
Distinguish between:
- **Defects** (Contractor design/materials/workmanship deficiencies) — Contractor rectifies at no cost
- **Employer operational issues** (misuse, lack of maintenance, modifications) — not Contractor responsibility
- **OEM/supplier warranty issues** — Contractor may coordinate but OEM/supplier performs warranty work
Clear warranty determination process prevents disputes.

**Consideration 2: Response Time Management**
Contract typically specifies response times by defect severity:
- Emergency (safety-critical): Immediate response (hours)
- Urgent (operational impact): Rapid response (days)
- Routine: Normal response (weeks)
Track response times; late responses may result in contractual penalties or Employer performing work and back-charging Contractor.

**Consideration 3: Site Access Coordination**
Facility is operational — Contractor requires:
- Site access authorization (Employer controls site)
- Work permits (hot work, confined space, etc. per Employer procedures)
- Coordination with operations (schedule work during low-activity periods, shutdowns)
- Safety briefing/orientation (Employer site safety rules)
Proactive coordination prevents access delays.

**Consideration 4: Outstanding Defects from Handover**
Handover punch list (DEL-35.03) forms initial defects liability workload — prioritize completion of known outstanding items early in defects liability period.

*Cross-reference DEL-35.03 Outstanding Defects List*

**Consideration 5: Defects Liability Period Closure**
At end of defects liability period:
- Prepare closure report (summary of defects rectified, Employer satisfaction, any unresolved items)
- Obtain Employer acceptance that warranty obligations fulfilled
- Release retention (if contract holds retention until defects liability period end)
- Address any disputed items through contract dispute resolution process

## Trade-offs

**Trade-off 1: Rapid Rectification vs. Root Cause Analysis**
Urgent defects require rapid fix (minimize operational disruption), but hasty fixes may not address root cause (defect recurs). Balance speed vs. thoroughness based on severity and operational impact.

**Trade-off 2: Contractor Resources vs. Subcontractor Resources**
Contractor can use own staff (faster mobilization, lower cost) or subcontractors/OEMs (specialized expertise, warranty pass-through). Balance cost, speed, and quality.

**Trade-off 3: Temporary Fix vs. Permanent Fix**
Safety-critical defects may require immediate temporary fix (make safe) followed by planned permanent fix (requires shutdown). Balance immediate safety vs. permanent solution.

## Examples

**Example: Defect Notification Form**
```
DEFECT NOTIFICATION

Defect ID: DL-2026-001
Reported Date: [date]
Reported By: [Employer representative name]

Defect Description: [detailed description]
Location: [system, equipment tag, area]
Severity: □ Emergency  □ Urgent  □ Routine
Safety Impact: □ Yes  □ No  (If yes, describe: _______)
Operational Impact: [downtime, reduced capacity, etc.]

Photographs: [attached/referenced]

Contractor Response Required By: [date per contract]
```

**Example: Defects Liability Register**
| Defect ID | Description | Reported | Severity | Status | Target Complete | Actual Complete | Employer Accept |
|-----------|-------------|----------|----------|--------|----------------|-----------------|-----------------|
| DL-001 | Pump seal leak | 2026-02-15 | Urgent | Completed | 2026-02-20 | 2026-02-18 | 2026-02-19 |
| DL-002 | Control alarm false | 2026-03-01 | Routine | In Progress | 2026-03-15 | - | - |
| ... |

*See Procedure.md for detailed defects liability management process.*
