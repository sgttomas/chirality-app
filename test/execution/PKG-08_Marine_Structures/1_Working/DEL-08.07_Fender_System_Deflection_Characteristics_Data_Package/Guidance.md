# Guidance: DEL-08.07 Fender System Deflection Characteristics Data Package

## Purpose

Provide engineering guidance for compiling **Fender System Deflection Characteristics Data Package** with complete OEM documentation, correct performance curve interpretation, and proper traceability.

**Deliverable intent:** Defines and substantiates fender system deflection characteristics data package in accordance with ER requirements. *(Source: Decomposition line 287)*

---

## Principles

### Source Fidelity
- Include only OEM-provided data; do not invent curves/values
- Trace all data to controlled manufacturer documents with revision IDs

### Applicability Clarity
- State which fender model/type the data applies to
- Document configuration assumptions (mounting, accessories, panel)

### Condition Awareness
- Performance varies with temperature, velocity, angle
- Ensure reference conditions documented

---

## Requirement Rationale Map

| Req ID | Requirement | Rationale |
|---|---|---|
| R-001 | Minimum content | Decomposition artifacts; ensures completeness |
| R-002 | Performance curves | Curves must be interpretable; units/conditions essential |
| R-003 | Manufacturer data | Technical data for design integration/procurement |
| R-004 | Certificates | Quality evidence for acceptance |
| R-005 | ER alignment | ER-driven acceptance basis |
| R-006 | Traceability/control | Verification and future reference |

---

## Engineering Considerations

### Understanding Fender Performance Curves

*ASSUMPTION based on PIANC/BS 6349-4:*

**1. Energy-Deflection Curve:**
- Energy absorbed (kN·m) vs deflection (% or mm)
- Area under reaction-deflection curve = energy absorbed
- Design point: energy absorbed ≥ design berthing energy from DEL-08.06

**2. Reaction-Deflection Curve:**
- Reaction force (kN) vs deflection (% or mm)
- Maximum reaction determines structural load
- Design point: reaction at design deflection

### Performance Adjustments

*ASSUMPTION: OEM curves at standard conditions; adjustments may be required:*

| Factor | Effect | Typical Adjustment |
|---|---|---|
| Low temperature | Rubber stiffens → higher reaction | Ct ≈ 0.85 at -10°C |
| High temperature | Rubber softens → lower reaction | Ct ≈ 1.05 at +40°C |
| High velocity | Dynamic stiffening | Cv ≈ 1.1 for V > 0.15 m/s |
| Angular berthing | Reduced contact | Ca factor |
| Manufacturing tolerance | Variation | ±10% typical |

*Confirm factors from ER and supplier.*

### Design Point Selection

1. Required energy from DEL-08.06
2. Find deflection at required energy
3. Read reaction at that deflection
4. Verify reaction acceptable for DEL-08.03 structural design
5. Apply condition factors

---

## Checklist

| Item | Check | Spec Link |
|---|---|---|
| Energy-deflection curve included | ☐ | R-001, R-002 |
| Reaction-deflection curve included | ☐ | R-001, R-002 |
| Units labeled (SI) | ☐ | R-002 |
| Reference temperature stated | ☐ | R-002 |
| Test standard referenced | ☐ | R-002 |
| Manufacturer datasheet included | ☐ | R-001, R-003 |
| Fender dimensions documented | ☐ | R-003 |
| Material specs included | ☐ | R-003 |
| Test certificates included | ☐ | R-001, R-004 |
| Material certificates included | ☐ | R-004 |
| Documents dated and revisioned | ☐ | R-006 |
| Package index prepared | ☐ | R-006 |

---

## Trade-offs

| Trade-off | Considerations |
|---|---|
| High energy vs low reaction | Larger/softer fenders absorb more but may have space constraints |
| Standard vs project testing | Project testing adds confidence but increases cost/schedule |
| Single vs multiple types | Multiple types optimize performance but complicate procurement |

---

## Common Issues

| Issue | Prevention |
|---|---|
| Curves without reference conditions | Require OEM to state temperature, velocity basis |
| Certificates not matching product | Verify certificate batch/lot numbers |
| Outdated OEM docs | Confirm current revision from manufacturer |
| Tolerance not considered | Include tolerance band in design margin |

---

## Sources

- Decomposition line 287
- ER Vol 2 Parts 1-2 *(TBD)*
- PIANC WG 33 (ASSUMPTION)
