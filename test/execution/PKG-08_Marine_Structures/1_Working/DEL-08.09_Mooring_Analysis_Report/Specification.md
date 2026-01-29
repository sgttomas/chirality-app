# Specification: DEL-08.09 Mooring Analysis Report

## Scope

Defines requirements for **Mooring Analysis Report**: minimum content, methodology, acceptance criteria, traceability, and documentation control.

**Deliverable intent:** Documents analysis and results for mooring analysis report required for design verification and approvals. *(Source: Decomposition line 289)*

### Inclusions
- Mooring analysis for design vessel(s) under environmental conditions
- Line load calculations
- Acceptance criteria assessment
- Vessel and environmental assumptions

### Exclusions
- Current assessment methodology (DEL-08.10)
- Mooring equipment detailed design (PKG-09)
- Structural design of bollards/hooks (DEL-08.03)

---

## Requirements

### R-001 — Minimum Report Content

*(Source: Decomposition line 289)*

| Component | Required Content |
|---|---|
| Mooring analysis report | Analysis with methodology, results, conclusions |
| Vessel assumptions | Vessel particulars, windage areas, loading conditions |
| Line loads | Calculated forces in mooring lines under design conditions |
| Acceptance criteria | Limits for line loads, safety factors, pass/fail |

**Rationale:** `Guidance.md` § Requirement Rationale Map, R-001

---

### R-002 — Vessel Definition

**Document design vessel(s):**

| Parameter | Requirement |
|---|---|
| Type and size | DWT, displacement, dimensions |
| Loading conditions | Laden and/or ballast analyzed |
| Windage areas | Longitudinal and transverse, with source |
| Freeboard | For each loading condition |
| Source | ER, project basis, or assumed with rationale |

**Rationale:** `Guidance.md` § Requirement Rationale Map, R-002

---

### R-003 — Environmental Conditions

**Document environmental conditions:**

| Parameter | Requirement |
|---|---|
| Wind | Speed, duration, direction(s), reference height |
| Current | Velocity, direction(s), depth profile if applicable |
| Waves | Hs, Tp, direction (if applicable) |
| Water level | Tide range, design levels |
| Return period | Design condition return period basis |
| Source | Metocean study, ER, or DEL-08.10 for current |

**Rationale:** `Guidance.md` § Requirement Rationale Map, R-003

---

### R-004 — Analysis Methodology

**Document:**

| Element | Requirement |
|---|---|
| Analysis method | Static equilibrium, dynamic simulation, or other |
| Software/tools | If used, identify and version |
| Load cases | All vessel × environment combinations |
| Coordinate system | Axes and sign conventions |
| Assumptions | Explicitly listed with rationale |
| Limitations | Known limitations of analysis |

**Rationale:** `Guidance.md` § Requirement Rationale Map, R-004

---

### R-005 — Acceptance Criteria and Results

**Include:**

| Element | Requirement |
|---|---|
| Line load criteria | Max allowable (% MBL or absolute) |
| Safety factor | Required factor on mooring lines |
| Results summary | Max line loads for each case |
| Pass/fail assessment | Explicit compliance statement |
| Governing case | Worst-case identification |

*ASSUMPTION: Typical criteria limit to 50-60% MBL; confirm from ER/OCIMF.*

**Rationale:** `Guidance.md` § Requirement Rationale Map, R-005

---

### R-006 — ER Alignment and Document Control

| Requirement | Description |
|---|---|
| ER clauses | All applicable ER addressed |
| Standards | Referenced standards identified |
| QA/QC review | Independent check prior to issue |
| Document control | Numbering, revision, approval per procedures |

**Rationale:** `Guidance.md` § Requirement Rationale Map, R-006

---

## Standards and References

**Standards (TBD):**
- OCIMF MEG4 (Mooring Equipment Guidelines)
- PIANC WG 153 (if applicable)
- BS 6349-4
- SIGTTO (if LNG/LPG applicable)

**References:**
- ER Vol 2 Parts 1-2
- DEL-08.10 (current data)
- DEL-08.06 (shared vessel basis)
- DEL-08.03 (bollard structural design)
- PKG-09 (mooring equipment)

---

## Verification Matrix

| Req ID | Method | Evidence | Status |
|---|---|---|---|
| R-001 | Completeness | All four components | **TBD** |
| R-002 | Design basis | Vessels defined with sources | **TBD** |
| R-003 | Environmental review | Conditions documented | **TBD** |
| R-004 | Methodology review | Method appropriate | **TBD** |
| R-005 | Results review | All cases pass criteria | **TBD** |
| R-006 | ER compliance + QA | Requirements met, review complete | **TBD** |

---

## Documentation Outputs

- Mooring Analysis Report
- Input data register
- Calculation appendix
- QA/QC review record
- Transmittal

---

## Sources

- Decomposition line 289
- ER Vol 2 Parts 1-2 *(TBD)*
