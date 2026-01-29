# Guidance: DEL-08.10 Current Assessment Basis Report

## Purpose

Provide engineering guidance for producing **Current Assessment Basis Report** with appropriate data sources, methodology, and clear design values for downstream use.

**Deliverable intent:** Documents analysis and results for current assessment basis report required for design verification and approvals. *(Source: Decomposition line 290)*

---

## Principles

### Source Fidelity
- Use measured data, published values, or calibrated models — do not invent
- Distinguish measured vs derived/assumed values

### Traceability
- Link: data sources → methodology → design current values
- Document assumptions and limitations

### Conservative Practice
- Design values appropriately conservative
- Consider combined tidal and river flow for Fraser River

---

## Requirement Rationale Map

| Req ID | Requirement | Rationale |
|---|---|---|
| R-001 | Minimum content | Decomposition artifacts |
| R-002 | Current data | Design values for mooring/structural analysis |
| R-003 | Data source/quality | Reliability assessment |
| R-004 | Methodology | Verification and future updates |
| R-005 | ER alignment | Requirements met |
| R-006 | Control and QA | Professional practice |

---

## Engineering Considerations

### Fraser River Current Regime

*ASSUMPTION:*

**1. Tidal Currents:**
- Semi-diurnal tidal influence from Strait of Georgia
- Flood (incoming) and ebb (outgoing)
- Spring vs neap tides

**2. River Flow:**
- Fraser River discharge superimposed
- Freshet (May-July): elevated river flow
- Normal period: lower base flow

**3. Combined Regime:**
- Ebb currents dominate (tidal ebb + river flow)
- Flood currents reduced (tidal flood − river flow)

### Typical Current Sources

| Source Type | Examples | Notes |
|---|---|---|
| CHS Tide Tables | Canadian Hydrographic Service | Tidal predictions |
| ADCP measurements | Site-specific current meter | Best if available |
| Historical studies | Port or previous projects | Fraser Surrey area |
| Numerical models | Hydrodynamic simulations | Spatial coverage |

### Design Current Selection

*ASSUMPTION:*

| Approach | Description |
|---|---|
| Extreme value analysis | Fit distribution, extract return period value |
| Maximum observed | Conservative if long data period |
| Published design values | If available from codes/authority |
| Percentile approach | 95th or 99th percentile |

*Confirm return period from ER.*

### Fraser River Freshet

*ASSUMPTION: Freshet period is critical for Fraser River:*
- Peak flows May–July
- River velocities significantly higher
- Design should consider freshet + spring tide combination

---

## Production Checklist

| Item | Check | Spec Link |
|---|---|---|
| Data sources identified/referenced | ☐ | R-003 |
| Data quality/reliability assessed | ☐ | R-003 |
| Methodology described | ☐ | R-001, R-004 |
| Statistical methods documented | ☐ | R-004 |
| Flood and ebb currents quantified | ☐ | R-002 |
| Freshet conditions addressed | ☐ | R-002 |
| Design return period stated | ☐ | R-002 |
| Depth profile addressed | ☐ | R-002 |
| Assumptions listed | ☐ | R-004 |
| Limitations stated | ☐ | R-004 |
| Design current summary table | ☐ | R-001 |
| QA/QC review | ☐ | R-006 |

---

## Trade-offs

| Trade-off | Considerations |
|---|---|
| Conservatism vs realism | Higher values → higher loads → cost; lower → risk |
| Site vs published data | Site data more accurate but may be unavailable |
| Single value vs range | Range provides flexibility but complicates analysis |
| Return period | Higher → more extreme values |

---

## Design Current Summary Format

| Condition | Direction | Velocity (m/s) | Return Period | Notes |
|---|---|---|---|---|
| Ebb (normal) | Downstream | **TBD** | **TBD** | Normal river flow |
| Ebb (freshet) | Downstream | **TBD** | **TBD** | Peak river flow |
| Flood (spring tide) | Upstream | **TBD** | **TBD** | Maximum flood |
| Design current | **TBD** | **TBD** | **TBD** | For mooring/structural |

---

## Sources

- Decomposition line 290
- ER Vol 2 Parts 1-2 *(TBD)*
- Fraser River hydrology (ASSUMPTION)
