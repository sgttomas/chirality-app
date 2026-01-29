# Procedure: DEL-30.07 Punch Lists

## Purpose

Defines the process for managing **Punch Lists** for the Canola Oil Transload Facility commissioning.

**Context:** Provides evidence of completion, inspection, and testing for punch lists.

**Source:** Decomposition §5 PKG-30, DEL-30.07

## Prerequisites

**Dependencies:** NOT_TRACKED mode — See `_DEPENDENCIES.md`

**Upstream Requirements:**
- DEL-30.01 Commissioning Procedures — Defect identification process
- DEL-30.02 Commissioning Plan — Defect rectification phase planning
- Active commissioning activities (DEL-30.03 through DEL-30.06) — Sources of punch items

**Personnel:**
- Punch list coordinator (tracks and reports)
- Discipline leads (assign responsible parties)
- Commissioning team (identify and resolve defects)
- QC inspectors (closure verification)
- Employer representative (acceptance)

**Tools:**
- Punch list database or tracking spreadsheet — **TBD**
- Camera for defect documentation
- Site access for inspections and verification

**Source:** **ASSUMPTION**

## Steps

**Step 1: Establish Punch List System**
- Set up punch list database or register — **TBD: project tool**
- Define punch item fields: ID, description, location, discipline, identified by, responsible party, priority (A/B/C), due date, status, closure verification
- Define punch list categories and prioritization criteria
- Communicate punch list process to commissioning team

**Step 2: Identify and Document Punch Items**
- During commissioning activities: Identify deficiencies, incomplete work, defects
- Document punch item:
  - Assign unique ID
  - Write clear description
  - Identify location (system, equipment tag, drawing reference)
  - Assign discipline
  - Record identified by (inspector name, date)
  - Take photographs of deficiency
  - Assign priority category (A, B, or C) based on impact
- Enter punch item into punch list database

**Step 3: Assign Responsibility and Due Date**
- Assign responsible party (contractor trade, vendor, subcontractor)
- Assign due date based on:
  - Category A: Before operational handover (hard deadline)
  - Category B: Before final acceptance or with deferral approval
  - Category C: Before closeout or with deferral approval
  - Schedule constraints and resource availability
- Communicate punch item to responsible party

**Step 4: Track Punch Item Resolution**
- Responsible party executes corrective work
- Update punch item status: Open → In Progress → Resolved
- Resolved items ready for closure verification

**Step 5: Verify Punch Item Closure**
- QC inspector verifies corrective work complete
- Take photographs of completed work
- If verification fails: Return to In Progress status; responsible party reworks
- If verification passes: Update status to Closed
- Obtain Employer acceptance for Category A/B items — **TBD**

**Step 6: Manage Deferrals (if required)**
- For items proposed for deferral:
  - Conduct operability assessment (confirm no impact on OBJ-1 through OBJ-10)
  - Document justification for deferral
  - Develop deferral plan (target closure date, responsible party, interim mitigation)
  - Obtain Employer approval for deferral
  - Track deferred items in defect register

**Step 7: Report Punch List Status**
- Generate periodic punch list status reports (weekly recommended during active commissioning)
- Report content: Total items, open items, closed items, deferred items, Category A status, overdue items
- Distribute to project management, Employer, commissioning team
- Escalate overdue Category A items

**Step 8: Close Punch List for Handover**
- Verify all Category A items closed
- Verify Category B items closed or deferred with approval
- Verify Category C items closed or deferred with approval
- Compile final punch list closeout report
- Obtain Employer acceptance of punch list status for operational handover

**Step 9: Final Punch List Closeout**
- Track deferred items to closure
- Verify all deferred items resolved per deferral plan
- Compile final defect register
- Submit final closed punch list for project closeout
- File in `3_Issued/DEL-30.07/`

**Source:** **ASSUMPTION** — Punch list management process

## Verification

- All punch items documented
- Priority categorization assigned
- Closure verification complete for closed items
- Deferred items have Employer approval and deferral plan
- Category A items all closed before handover

**Source:** Specification.md

## Records

**Outputs:**
- Master punch list register
- Punch lists by phase, system, discipline
- Open items reports (periodic)
- Closed items reports (verification evidence)
- Deferred items register with approvals
- Defect register with statistics
- Final punch list closeout report

**Management:**
- Filed in `3_Issued/DEL-30.07/`
- Periodic updates throughout commissioning
- Final closeout submittal
- Retention: **TBD** — Permanent project records

**Source:** Decomposition §5 DEL-30.07

---

## Document Cross-References

- **← Datasheet / Specification / Guidance:** Procedure implements punch list management requirements
- DEL-30.03 through DEL-30.06 provide sources of punch items
- Punch list status affects operational handover and project closeout
