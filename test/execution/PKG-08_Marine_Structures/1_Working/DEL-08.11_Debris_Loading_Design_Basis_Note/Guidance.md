# Guidance: DEL-08.11 Debris Loading Design Basis Note

## Purpose

Provide engineering guidance for developing **Debris Loading Design Basis Note** with appropriate debris characterization, impact methodology, and clear load case definitions.

**Deliverable intent:** Provides project management/control documentation for debris loading design basis note required by the ERs. *(Source: Decomposition line 291)*

---

## Principles

### Source Fidelity
- Extract debris scenarios from ER or cite standards
- Mark inferred parameters as **ASSUMPTION**

### Clarity
- Load cases clear and unambiguous
- Applicability identifies affected structures/zones

### Conservatism
- Debris loading difficult to quantify; conservative assumptions appropriate
- Consider combined conditions

---

## Requirement Rationale Map

| Req ID | Requirement | Rationale |
|---|---|---|
| R-001 | Minimum content | Decomposition artifacts |
| R-002 | Debris characterization | Design requires defined parameters |
| R-003 | Load case definitions | Enables consistent analysis |
| R-004 | Applicability | Clarifies design scope |
| R-005 | ER alignment | Requirements met |
| R-006 | Control and QA | Professional practice |

---

## Engineering Considerations

### Fraser River Debris

*ASSUMPTION:*

**Freshet Period (May–July):** High flows transport logs, trees downstream

**Storm Events:** Bank erosion, urban debris

**Normal Operations:** Lower frequency but not zero

### Debris Types

| Type | Mass | Notes |
|---|---|---|
| Logs | 500–5000 kg | Common |
| Trees | 1000–10000 kg | Freshet/storms |
| Root wads | 500–3000 kg | Irregular |
| Floating debris | Variable | Less common |

### Impact Load Methodology

*ASSUMPTION:*

```
F = m × v / Δt   (simplified)
```

Or energy-based:

```
F = k × δ
```

*CSA S6 or AASHTO may provide specific methods — confirm from ER.*

### Impact Velocity

*ASSUMPTION:*
- ≈ Current velocity (from DEL-08.10)
- Debris carried with current

### Impact Duration

*ASSUMPTION:*
- Typical: 0.1–1.0 seconds for log impact
- Depends on debris/structure stiffness

---

## Production Checklist

| Item | Check | Spec Link |
|---|---|---|
| Debris type(s) identified | ☐ | R-002 |
| Mass with basis | ☐ | R-002 |
| Dimensions | ☐ | R-002 |
| Velocity from DEL-08.10 | ☐ | R-002 |
| Duration with basis | ☐ | R-002 |
| Impact height | ☐ | R-002 |
| Load cases uniquely identified | ☐ | R-003 |
| Load cases described | ☐ | R-003 |
| Concurrent conditions | ☐ | R-003 |
| Applicable structures | ☐ | R-004 |
| Exposure zones | ☐ | R-004 |
| Assumptions listed | ☐ | R-001 |
| QA/QC review | ☐ | R-006 |

---

## Load Case Example

| Load Case | Description | Debris | Velocity | Concurrent |
|---|---|---|---|---|
| DEB-01 | Normal, operating | Log, 1000 kg | Normal current | Normal water |
| DEB-02 | Extreme, freshet | Tree, 5000 kg | Freshet current | High water |
| DEB-03 | Accumulation | Multiple logs | Sustained | Normal-high water |

*Designations per project conventions — TBD.*

---

## Trade-offs

| Trade-off | Considerations |
|---|---|---|
| Conservative vs economic | Higher mass → higher loads → cost |
| Single vs multiple | Multiple simultaneous is conservative but may be unrealistic |
| Impact vs accumulation | Both may be needed |
| Deterministic vs probabilistic | Probabilistic better characterizes uncertainty |

---

## Sources

- Decomposition line 291
- ER Vol 2 Parts 1-2 *(TBD)*
- CSA S6 (ASSUMPTION)
