# Specification: DEL-30.07 Punch Lists

## Scope

Defines requirements for **Punch Lists** for the Canola Oil Transload Facility — Phase 1.

**Purpose:** Provides evidence of completion, inspection, and testing for punch lists.

**Artifacts:** Commissioning punch lists, defect registers

**Source:** Decomposition §5 PKG-30, DEL-30.07

## Requirements

### Functional Requirements

**FR-1: Punch List Item Documentation**
- Each punch item shall be documented with: ID, description, location, discipline, identified by, responsible party, priority, due date, status, closure verification
- **Source:** **ASSUMPTION** — Punch list item attributes

**FR-2: Punch List Categorization**
- Punch items shall be categorized by priority:
  - **Category A (Critical):** Safety, operational show-stoppers, regulatory — Close before operational handover
  - **Category B (Important):** Performance, quality, warranty — Close before final acceptance or with approved deferral
  - **Category C (Minor):** Cosmetic, minor deficiencies — May defer with Employer approval
- **Source:** **ASSUMPTION** — Risk-based punch list categorization

**FR-3: Defect Register**
- Defect register shall track all deficiencies by phase, system, and discipline
- Defect statistics for quality management and trend analysis
- **Source:** **ASSUMPTION** — Defect tracking requirements

**FR-4: Punch List Closure Verification**
- Each punch item closure shall be verified by QC inspection
- Photographic evidence of completed corrections
- Re-inspection if closure verification fails
- **Source:** **ASSUMPTION** — Closure verification governance

**FR-5: Deferral Management**
- Deferred punch items require:
  - Operability assessment (confirm no impact on OBJ-1 through OBJ-10)
  - Employer approval for deferral
  - Deferral plan with target closure date and responsible party
- **Source:** **ASSUMPTION** — Deferral governance

### Performance Requirements

**PR-1: Category A Closure Before Handover**
- All Category A (Critical) punch items shall be closed before operational handover
- No safety-critical or regulatory compliance deficiencies shall remain open
- **Source:** **ASSUMPTION** — Safety and compliance requirements; Decomposition §2 OBJ-1, OBJ-6

**PR-2: Punch List Closeout Timeline**
- Punch list closure shall meet project closeout schedule
- Final punch list closeout for final acceptance and payment
- **Source:** **ASSUMPTION** — Closeout governance

### Interface Requirements

**IR-1: Commissioning Activities Interface**
- Punch items identified during commissioning (DEL-30.03 through DEL-30.06)
- **Source:** DEL-30.03 through DEL-30.06

**IR-2: Construction Punch List Interface**
- Coordinate with construction punch lists to avoid duplication
- Clarify responsibility for items affecting both construction and commissioning
- **Source:** **ASSUMPTION** — Construction interface

**IR-3: Operational Handover Interface**
- Punch list status affects operational handover decision (PKG-35)
- **Source:** Decomposition §4 PKG-35

### Quality Requirements

**QR-1: Punch List Tracking and Reporting**
- Punch list status shall be tracked and reported periodically to project management and Employer
- Reporting frequency: **TBD** — Weekly during active commissioning recommended
- **Source:** **ASSUMPTION** — Punch list governance

**QR-2: Closure Verification**
- Punch item closure requires QC verification and Employer acceptance (Category A/B)
- Photographic evidence of completed work
- **Source:** **ASSUMPTION**

**QR-3: Audit Trail**
- Punch list database shall maintain complete audit trail: creation date, status changes, responsible party changes, closure date
- **Source:** **ASSUMPTION** — Traceability requirements

## Standards

- Project Quality Management Plan — Defect management and NCR procedures — **TBD: location**
- Employer's Requirements — **TBD: location** for punch list and closeout requirements

**Source:** **ASSUMPTION: likely applicable**

## Verification

- All punch items documented with required fields
- Priority categorization assigned per criteria
- Closure verification complete for closed items
- Deferred items have Employer approval and deferral plan
- Defect register complete

**Acceptance:** All Category A items closed; Category B items closed or deferred with approval; Category C items closed or deferred; final defect register submitted

## Documentation

**Outputs:** Master punch list register, punch lists by phase/system/discipline, defect registers, deferral approvals, closeout summary

**Format:** Punch list database or register — **TBD**

**Submittal:** Initial punch list early in commissioning; weekly updates; final closed punch list for project closeout; stored in `3_Issued/DEL-30.07/`

**Source:** Decomposition §5 DEL-30.07

---

## Document Cross-References

- **← Datasheet.md:** Requirements for punch list structure and categorization
- **→ Guidance.md:** Rationale for systematic defect tracking and prioritization
- **→ Procedure.md:** Punch list management process
