# Guidance: DEL-08.06 Berthing Energy Calculation Report

## Purpose

Provide engineering guidance for producing the **Berthing Energy Calculation Report** with clear expectations for methodology, traceability, and reviewability.

**Deliverable intent:** Documents analysis and results for berthing energy calculation report required for design verification and approvals. *(Source: Decomposition line 286)*

---

## Principles

### Source Fidelity
- Extract methods/criteria from ER; cite clause locations
- Mark inferred methodology as **ASSUMPTION** until confirmed

### Traceability
- Link: inputs → coefficients → calculations → results → fender demand
- Document all assumptions with rationale and impact

### Design Conservatism
- **ASSUMPTION:** Berthing energy calculations typically apply safety factors (1.5–2.0) for uncertainties — confirm from ER

---

## Requirement Rationale Map

| Req ID | Requirement | Rationale |
|---|---|---|
| R-001 | Minimum content | Decomposition artifacts; ensures completeness for approvals |
| R-002 | Vessel/scenario definition | Essential input; undefined vessels make calculations meaningless |
| R-003 | Methodology | Must be auditable; standards provide accepted coefficients |
| R-004 | ER alignment | ER-driven approval basis |
| R-005 | Traceability/assumptions | Enables third-party review and future design changes |
| R-006 | QA/QC and control | Professional practice; controlled issue enables tracking |

---

## Engineering Considerations

### Berthing Energy Methodology

**ASSUMPTION:** Kinetic energy method is standard:

```
E = 0.5 × M × V² × Cm × Ce × Cc × Cs
```

**Coefficients (typical ranges from PIANC/BS 6349-4):**
- **Cm (Added mass):** 1.4–1.8 for broadside berthing
- **Ce (Eccentricity):** 0.5–1.0 (bow/stern vs amidships)
- **Cc (Configuration):** 0.8–1.0 for open pile structures
- **Cs (Softness):** 0.9–1.0 for stiff structures

### Approach Velocity Selection

| Condition | Typical Velocity | Notes |
|---|---|---|
| Sheltered, assisted | 0.10–0.15 m/s | Tug-assisted, calm |
| Exposed, assisted | 0.15–0.25 m/s | Tugs, some exposure |
| Unassisted, sheltered | 0.20–0.30 m/s | No tugs, calm |
| Unassisted, exposed | 0.30–0.50 m/s | Unfavorable |

*Source: PIANC/BS 6349-4 guidance (ASSUMPTION — confirm from ER)*

### Design Cases

1. **Normal berthing** — routine, lower velocity, higher frequency
2. **Abnormal berthing** — adverse conditions, higher velocity, lower frequency
3. **Accidental/emergency** — extreme (if required by ER)

---

## Production Checklist

| Item | Check | Spec Link |
|---|---|---|
| Design vessel(s) identified with source | ☐ | R-002 |
| Scenarios defined (normal/abnormal) | ☐ | R-002 |
| Approach velocities with justification | ☐ | R-002, R-003 |
| Coefficient values with sources | ☐ | R-003 |
| Safety factor applied and justified | ☐ | R-003, R-004 |
| Governing case identified | ☐ | R-001 |
| All assumptions listed | ☐ | R-005 |
| Input register complete | ☐ | R-005 |
| QA/QC review performed | ☐ | R-006 |

---

## Trade-offs

| Trade-off | Considerations |
|---|---|
| Conservative vs economic | Higher velocity → larger fender → higher cost; balance vs risk |
| Single vs multiple vessels | Multiple vessels increase complexity but may be required |
| Deterministic vs probabilistic | Probabilistic more rigorous but may not be required |

---

## Interface Considerations

| Related Deliverable | Interface |
|---|---|
| DEL-08.07 Fender Characteristics | Energy demand drives fender selection |
| DEL-08.08 Fender Supplier Verification | Supplier verifies capacity ≥ demand |
| DEL-08.09 Mooring Analysis | Shared vessel/environmental basis |
| DEL-08.03 Structures Calculations | Fender reactions to structure |

---

## Sources

- Decomposition line 286
- ER Vol 2 Parts 1-2 *(TBD)*
- PIANC WG 33, BS 6349-4 (ASSUMPTION)
