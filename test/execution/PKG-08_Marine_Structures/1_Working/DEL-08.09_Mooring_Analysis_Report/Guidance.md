# Guidance: DEL-08.09 Mooring Analysis Report

## Purpose

Provide engineering guidance for producing **Mooring Analysis Report** with appropriate methodology, conservative assumptions, and clear acceptance assessment.

**Deliverable intent:** Documents analysis and results for mooring analysis report required for design verification and approvals. *(Source: Decomposition line 289)*

---

## Principles

### Source Fidelity
- Extract acceptance criteria from ER or cite standards (OCIMF, PIANC)
- Use documented metocean data — do not estimate

### Traceability
- Link: environmental inputs + vessel → analysis → line loads → acceptance
- Document assumptions explicitly

### Conservative Practice
- Analyze worst-case vessel × environment combinations
- Apply safety factors per standards

---

## Requirement Rationale Map

| Req ID | Requirement | Rationale |
|---|---|---|
| R-001 | Minimum content | Decomposition artifacts |
| R-002 | Vessel definition | Analysis meaningless without defined vessel |
| R-003 | Environmental conditions | Forces depend on wind/current; must be defined |
| R-004 | Methodology | Must be appropriate and documented |
| R-005 | Acceptance and results | Must demonstrate compliance |
| R-006 | ER alignment and control | Requirements met, controlled issue |

---

## Engineering Considerations

### Mooring Analysis Methodology

*ASSUMPTION:*

**1. Static Analysis:**
- Equilibrium: wind force + current force = mooring lines + fenders
- Appropriate for sheltered locations, low waves
- Simpler, widely used

**2. Dynamic Analysis:**
- Time-domain simulation of vessel motions
- Required for exposed locations with waves
- More complex, specialized software

*Confirm method from ER or site exposure.*

### Wind Force Calculation

*ASSUMPTION (OCIMF):*

```
Fw = 0.5 × ρ × Cd × A × V²
```

- ρ = air density (~1.225 kg/m³)
- Cd = drag coefficient (vessel type/angle dependent)
- A = windage area (m²)
- V = wind velocity (m/s)

### Current Force Calculation

*ASSUMPTION:*

```
Fc = 0.5 × ρw × Cd × A × V²
```

- ρw = water density (~1025 kg/m³)
- Cd = drag coefficient
- A = underwater projected area
- V = current velocity (from DEL-08.10)

### Load Case Matrix

| Condition | Wind | Current | Vessel |
|---|---|---|---|
| Operational | Design operational | Design | Laden |
| Operational | Design operational | Design | Ballast |
| Extreme | Design extreme | Extreme | Laden |
| Extreme | Design extreme | Extreme | Ballast |

*Consider multiple wind/current directions (aligned, opposing, oblique).*

### Acceptance Criteria

*ASSUMPTION (confirm from ER/OCIMF):*

| Condition | Line Load Limit | Basis |
|---|---|---|
| Normal operating | 50% MBL | OCIMF MEG4 |
| Extreme | 55-60% MBL | OCIMF MEG4 |
| Survival (storm) | 70% MBL | Some guidelines |

Where MBL = Minimum Breaking Load.

---

## Production Checklist

| Item | Check | Spec Link |
|---|---|---|
| Design vessel(s) identified | ☐ | R-002 |
| Windage areas documented | ☐ | R-002 |
| Wind conditions defined | ☐ | R-003 |
| Current conditions from DEL-08.10 | ☐ | R-003 |
| Wave (if applicable) | ☐ | R-003 |
| Analysis method stated | ☐ | R-004 |
| Load cases enumerated | ☐ | R-004 |
| Acceptance criteria with source | ☐ | R-005 |
| Results for all cases | ☐ | R-005 |
| Pass/fail explicit | ☐ | R-005 |
| Governing case identified | ☐ | R-005 |
| Assumptions listed | ☐ | R-004 |
| QA/QC review | ☐ | R-006 |

---

## Trade-offs

| Trade-off | Considerations |
|---|---|
| Static vs dynamic | Dynamic more rigorous but may not be required for sheltered site |
| Conservative vs realistic metocean | Conservative increases loads but provides margin |
| Number of load cases | More cases = thoroughness but more effort |
| Single vs multiple vessels | Multiple vessels = completeness but complexity |

---

## Sources

- Decomposition line 289
- ER Vol 2 Parts 1-2 *(TBD)*
- OCIMF MEG4 (ASSUMPTION)
