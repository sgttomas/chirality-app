# Estimate Summary — EST_DEL-013-06_2026-02-27_0201

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **Scope** | DEL-013-06: Ceiling Fans |
| **Package** | PKG-013: Mechanical & HVAC Installation |

## Total Estimated Cost

| | Amount (CAD) |
|---|---|
| **Grand Total** | **$70,234.40** |

## Breakdown by Cost Breakdown Structure (CBS)

| CBS Category | Amount (CAD) | % of Total | Line Count |
|---|---|---|---|
| Equipment (fans, mounting, controls, access) | $44,950.00 | 64.0% | 4 |
| Labour (installation + electrical) | $6,105.60 | 8.7% | 2 |
| Design (ME + SE + EE coordination) | $6,640.00 | 9.5% | 3 |
| Management (PM, CPM, Super, Est, QA, HSE) | $5,590.00 | 8.0% | 1 |
| Commissioning (testing + balancing) | $4,019.20 | 5.7% | 1 |
| Documentation (as-builts, O&M, close-out) | $1,929.60 | 2.7% | 1 |
| Permits (safety code) | $1,000.00 | 1.4% | 1 |
| **Total** | **$70,234.40** | **100.0%** | **13** |

## Breakdown by WBS

| Package | Deliverable | Amount (CAD) |
|---|---|---|
| PKG-013 | DEL-013-06 (Ceiling Fans) | $70,234.40 |

## Key Cost Drivers

1. **HVLS ceiling fan supply ($33,000)** — 47% of total. Fan model, diameter, and power are TBD. Parametric estimate assumes industrial HVLS fans at $5,500/unit. Actual quotes could range $3,500-$8,000/unit ($21,000-$48,000 for 6 units).
2. **Mounting hardware ($6,600)** — 9.4% of total. Extended downrods for 35 ft ceiling; mounting type dependent on unresolved ceiling structure type (CF-013-06-03).
3. **Design engineering ($6,640)** — 9.5% of total. Mechanical engineer layout design, structural engineer approval, electrical coordination.

## Key Warnings and Coverage Gaps

| ID | Warning | Impact |
|---|---|---|
| W-01 | No explicit ceiling fan unit pricing in PRICE_SOURCES | Equipment costs (ITEM-01, ITEM-02, ITEM-05) are parametric with LOW confidence |
| W-02 | Fan model/diameter/power all TBD | Equipment pricing has wide uncertainty range ($21k-$48k for fans alone) |
| W-03 | Ceiling structure type unresolved (CF-013-06-03) | Mounting hardware approach and cost could change materially |
| W-04 | Control type TBD (D-003) | Centralized panel would increase ITEM-05 cost significantly |
| W-05 | Multiple TBD acceptance criteria in Specification | Commissioning scope could expand based on final requirements |
| W-06 | HVLS voltage assumption may be invalid (B-002) | If HVLS requires 208V/480V 3-phase, electrical connection scope increases |
| W-07 | No scaffolding/lift rates in PRICE_SOURCES | Access equipment cost ($2,500) is parametric LOW confidence |

## Confidence Assessment

- **Overall Confidence: LOW** — The dominant cost driver (HVLS fan supply at 47% of total) has no quote or rate table basis; multiple TBD design parameters remain unresolved.
- **Items with PRICE_SOURCE backing: 3 of 13** (L-03, L-04, and L-13 partial — labour rates and LOE hours)
- **Items fully parametric without source: 5 of 13** (L-01, L-02, L-05, L-10, L-12)
- **Items parametric with partial source: 5 of 13** (L-06, L-07, L-08, L-09, L-11 — hours parametric, rates from source)
