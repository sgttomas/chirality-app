# Guidance: DEL-08.08 Fender Supplier Design Verification Letter/Report

## Purpose

Provide engineering guidance for obtaining and reviewing **Fender Supplier Design Verification Letter/Report** to ensure adequate confirmation of fender suitability.

**Deliverable intent:** Documents analysis and results for fender supplier design verification letter/report required for design verification and approvals. *(Source: Decomposition line 288)*

---

## Principles

### Third-Party Verification Value
- Supplier verification provides independent confirmation
- Transfers design responsibility to supplier/OEM for product performance

### Traceability
- Verification must state what was verified and against which inputs
- Enables audit trail: energy → selection → confirmation

### Professional Accountability
- P.Eng. stamps provide professional accountability
- Required in some jurisdictions for structural adequacy

---

## Requirement Rationale Map

| Req ID | Requirement | Rationale |
|---|---|---|
| R-001 | Minimum content | Decomposition artifacts |
| R-002 | Verification statement | Clear verification required |
| R-003 | Input traceability | Correct inputs essential |
| R-004 | Engineering certification | Professional accountability |
| R-005 | ER alignment | ER-driven acceptance |
| R-006 | Document control | Controlled documentation |

---

## Good Verification Letter Elements

*ASSUMPTION:*

1. **Specific** — Exact fender model/size/configuration
2. **Design Basis Clear** — Energy demand and conditions stated
3. **Unconditional** (or conditions stated clearly)
4. **Supporting Analysis** — Calculations included or referenced
5. **Professionally Signed** — Engineer credentials and accountability

---

## Example Verification Structure

```
[Supplier Letterhead]

Subject: Design Verification for [Fender Model] — [Project]

We confirm that [Fender Model, Size], when installed per [Drawing],
is suitable for:

- Design berthing energy: [X] kN·m (from DEL-08.06)
- Temperature: [X]°C to [Y]°C
- Approach velocity: [X] m/s

The fender provides:
- Energy absorption: [Y] kN·m at [Z]% deflection
- Maximum reaction: [W] kN

Capacity exceeds demand with factor of safety [N] per [Standard].

[Limitations if any]

Verified by: [Name], [P.Eng. #], [Date]
[Stamp if required]
```

---

## Professional Engineering Requirements

*ASSUMPTION for BC:*
- Structural adequacy statements may require P.Eng. under EGBC
- Verifying engineer takes professional responsibility
- Confirm from ER and provincial regulations

---

## Review Checklist

| Item | Check | Spec Link |
|---|---|---|
| Fender model/config identified | ☐ | R-002 |
| Design energy stated with source | ☐ | R-002, R-003 |
| Operating conditions specified | ☐ | R-002, R-003 |
| Explicit compliance statement | ☐ | R-002 |
| Safety factor/margin stated | ☐ | R-002 |
| Standard(s) referenced | ☐ | R-002 |
| Limitations clearly stated | ☐ | R-002 |
| Engineer signature and date | ☐ | R-002 |
| P.Eng. stamp (if required) | ☐ | R-004 |
| Inputs traceable | ☐ | R-003 |
| Calculations attached (if required) | ☐ | R-001 |

---

## Trade-offs

| Trade-off | Considerations |
|---|---|
| Detailed calcs vs summary | Full calcs provide assurance but may be proprietary |
| Single vs multiple load cases | Multiple cases more complete but add effort |
| Supplier P.Eng. vs D&B P.Eng. review | Both may be required depending on ER/jurisdiction |

---

## Common Issues

| Issue | Prevention |
|---|---|
| Generic verification | Require project-specific inputs |
| Missing/unclear design basis | Require explicit energy/conditions |
| No professional sign-off | Confirm P.Eng. requirement first |
| Outdated fender data | Verify letter references current DEL-08.07 |
| Vague compliance | Require explicit "meets requirements" statement |

---

## Sources

- Decomposition line 288
- ER Vol 2 Parts 1-2 *(TBD)*
- EGBC practice (ASSUMPTION)
