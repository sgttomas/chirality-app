# Estimate Summary -- DEL-05-05 Option -- Town Branding Signage

**Snapshot:** EST_DEL-05-05_2026-02-18_1800
**RUN_STATUS:** WARNINGS

---

## BasisOfEstimate_Used

| Field | Value |
|---|---|
| **Declared Basis** | QUOTE |
| **Actual Method Used** | ALLOWANCE (fallback) |
| **Reason for Fallback** | No vendor quote exists for signage; Town branding guidelines are PENDING (not in RFP). FALLBACK_POLICY=ALLOW_ALLOWANCE authorized the fallback. Parametric data from Optional_Items_Pricing.csv used as allowance. |
| **ALLOW_MIXED_METHODS** | TRUE (brief-authorized) |
| **Currency** | CAD |
| **Rounding** | DOLLAR |

---

## Totals by Deliverable

### Primary Scenario (Non-Illuminated)

| WBS_PackageID | WBS_DeliverableID | Description | Amount (CAD) |
|---|---|---|---|
| PKG-005 | DEL-05-05 | Town branding signage -- non-illuminated | $12,000 |

### Alternate Scenario (Illuminated)

| WBS_PackageID | WBS_DeliverableID | Description | Amount (CAD) |
|---|---|---|---|
| PKG-005 | DEL-05-05 | Town branding signage -- illuminated | $22,000 |

**Note:** The two scenarios are mutually exclusive (either/or), not additive. The illumination decision is TBD.

### Range Summary

| Scenario | Low | Recommended | High |
|---|---|---|---|
| Non-illuminated (OPT-10) | $8,000 | **$12,000** | $18,000 |
| Illuminated (OPT-11) | $15,000 | **$22,000** | $30,000 |

---

## Totals by CBS

| CBS | Description | Primary Amount (CAD) | Alternate Amount (CAD) |
|---|---|---|---|
| 09-SIGNAGE-FAB | Signage fabrication (supply + mount + install) | $12,000 | $22,000 |

---

## Key Warnings

1. **BLOCKED on branding guidelines (DEP-05-05-007).** Town branding guidelines have not been provided. Signage design, dimensions, materials, and illumination decision cannot be finalized. This is the single largest risk to estimate accuracy.
2. **Illumination decision TBD.** The $10,000 delta between non-illuminated ($12,000) and illuminated ($22,000) scenarios is material. Owner decision is required.
3. **Quantity assumed as 1 sign.** The parametric source prices per sign unit. If multiple signs are required (e.g., different facades), the total will increase proportionally. Quantity is TBD pending branding guidelines.
4. **No vendor quote.** All pricing is allowance-grade parametric. Confidence is LOW. Repricing with vendor quotes is recommended once branding guidelines are received.

## Blockers (from Dependency Evidence)

| DependencyID | Target | Status | Impact on Estimate |
|---|---|---|---|
| DEP-05-05-007 | Town of Penhold branding guidelines | PENDING | Cannot finalize sign design, dimensions, materials, or illumination scope; estimate is provisional |
| DEP-05-05-006 | DEL-02-06 (Electrical) | TBD (conditional) | Electrical coordination required only if illuminated signage is selected |
| DEP-05-05-004 | DEL-02-01 (Architectural) | TBD | Building exterior concept needed for sign placement; does not affect pricing range |
| DEP-05-05-005 | DEL-02-04 (Envelope/Structure) | TBD | Facade geometry needed for mounting; does not affect pricing range |

## Cost Ownership Exclusions (Double-Count Prevention)

The following costs are explicitly excluded from this estimate and are owned by other deliverables:

- Code-required signage (exits, accessibility, fire, room ID) --> DEL-02-01
- Structural provisions for signage mounting (base building) --> DEL-02-04
- Electrical circuit for illuminated signage (branch circuit from panel) --> DEL-02-06
