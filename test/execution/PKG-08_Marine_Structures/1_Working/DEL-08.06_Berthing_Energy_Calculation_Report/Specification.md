# Specification: DEL-08.06 Berthing Energy Calculation Report

## Scope

Defines requirements for the **Berthing Energy Calculation Report**: minimum content, methodology, traceability, review, and documentation control for design verification and approvals.

**Deliverable intent:** Documents analysis and results for berthing energy calculation report required for design verification and approvals. *(Source: Decomposition line 286)*

### Inclusions
- Berthing energy calculations for design vessel(s) and scenarios
- Design basis (vessel particulars, approach conditions, coefficients)
- Assumptions register
- Summary report with governing case

### Exclusions
- Fender selection/sizing (DEL-08.07)
- Supplier verification (DEL-08.08)
- Structural design of fender supports (DEL-08.03)

---

## Requirements

### R-001 — Minimum Report Content

The deliverable shall include *(Source: Decomposition line 286)*:

| Component | Required Content |
|---|---|
| Berthing energy calculations | Kinetic energy for each design case |
| Design basis | Vessel particulars, velocities, coefficients |
| Assumptions | Explicit list with rationale |
| Summary report | Governing case, energy demand, recommendations |

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-001
**Verification:** See `Procedure.md` § Requirement Coverage Matrix, R-001

---

### R-002 — Design Vessel and Scenario Definition

**Requirement:** Document:
- Design vessel(s): type, displacement, dimensions
- Berthing scenarios: approach angle, velocity, frequency
- Source of vessel/scenario data

**Source:** **TBD** *(from ER or project basis)*
**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-002
**Verification:** See `Procedure.md` § Requirement Coverage Matrix, R-002

---

### R-003 — Calculation Methodology

**Requirement:** Document methodology including:
- Energy formula (e.g., E = 0.5 × M × V² × Cm × Ce × Cc × Cs)
- Coefficient definitions and values with justification
- Applicable standards/codes (e.g., PIANC, BS 6349-4)
- Safety factor application

**ASSUMPTION:** Kinetic energy method per PIANC or BS 6349-4; confirm from ER
**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-003
**Verification:** See `Procedure.md` § Requirement Coverage Matrix, R-003

---

### R-004 — ER Alignment

**Requirement:** Method, criteria, acceptance per ER.

**Applicable ER clauses:** **TBD**
**Referenced standards:** **TBD**
**Acceptance criteria:** **TBD**

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-004
**Verification:** See `Procedure.md` § Requirement Coverage Matrix, R-004

---

### R-005 — Traceability and Assumptions

**Requirement:** Provide:
- Input data register with sources and revisions
- Assumptions table (ID, statement, basis, impact if changed)

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-005
**Verification:** See `Procedure.md` § Requirement Coverage Matrix, R-005

---

### R-006 — QA/QC Review and Document Control

**Requirement:**
- Independent check of calculations and methodology
- Document control per project procedures

**ASSUMPTION:** QA/QC review required; confirm from ER/QA plan
**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-006
**Verification:** See `Procedure.md` § Requirement Coverage Matrix, R-006

---

## Standards and References

**Standards (TBD, confirm from ER):**
- PIANC WG 33 (2002) — Guidelines for Design of Fenders
- BS 6349-4 — Code of Practice for Fendering and Mooring
- OCIMF MEG4 — Mooring Equipment Guidelines

**References:**
- ER Vol 2 Parts 1-2
- DEL-08.07, DEL-08.08 (fender system deliverables)
- DEL-08.03 (structural calculations)
- DEL-08.09 (mooring analysis - shared vessel basis)

---

## Verification and Acceptance

**Verification Matrix:**

| Req ID | Method | Evidence | Status |
|---|---|---|---|
| R-001 | Completeness check | All four components present | **TBD** |
| R-002 | Design basis review | Vessels/scenarios defined with sources | **TBD** |
| R-003 | Methodology review | Method consistent with standards | **TBD** |
| R-004 | ER compliance | ER clauses addressed | **TBD** |
| R-005 | Traceability audit | Input/assumptions registers complete | **TBD** |
| R-006 | QA review | Review sign-off, comments closed | **TBD** |

**Acceptance Criteria (TBD):** All reviews complete, ER requirements met, suitable for approval submission

---

## Documentation Outputs

- Berthing Energy Calculation Report
- Input register
- Assumptions register
- QA/QC review record
- Transmittal

---

## Sources

- Decomposition line 286
- ER Vol 2 Parts 1-2 *(clause locations TBD)*
