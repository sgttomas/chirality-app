# Summary — EST_DEL-015-01_2026-02-26_2232

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| CURRENCY | CAD |
| Scope | DEL-015-01 — Three-Phase Power Service |
| Package | PKG-015 — Electrical & Low-Voltage Installation |

Methods used in this estimate:
- **PARAMETRIC**: 14 lines (primary basis — trade labour, materials, permits, inspections, commissioning)
- **RATE_TABLE**: 6 lines (professional staff hours from Level_of_Effort x Staff Rates)
- **ALLOWANCE**: 1 line (service entrance materials — service voltage/ampacity TBD)

---

## Total by Deliverable

| WBS_DeliverableID | Deliverable Name | Currency | Total |
|---|---|---|---|
| DEL-015-01 | Three-Phase Power Service | CAD | $66,061.40 |

---

## Total by CBS Category

| CBS | Currency | Amount | % of Total |
|---|---|---|---|
| ELECTRICAL-SERVICE | CAD | $28,000.00 | 42.4% |
| ELECTRICAL-LABOUR | CAD | $9,946.40 | 15.1% |
| MANAGEMENT | CAD | $5,590.00 | 8.5% |
| ELECTRICAL-DISTRIBUTION | CAD | $4,800.00 | 7.3% |
| ELECTRICAL-GROUNDING | CAD | $4,000.00 | 6.1% |
| ELECTRICAL-DEVICES | CAD | $3,800.00 | 5.8% |
| ELECTRICAL-COORDINATION | CAD | $2,500.00 | 3.8% |
| ELECTRICAL-COMMISSIONING | CAD | $2,000.00 | 3.0% |
| ELECTRICAL-PERMITS | CAD | $1,500.00 | 2.3% |
| ELECTRICAL-DOCUMENTATION | CAD | $1,500.00 | 2.3% |
| ELECTRICAL-UNDERGROUND | CAD | $1,425.00 | 2.2% |
| ELECTRICAL-INSPECTION | CAD | $1,000.00 | 1.5% |
| **TOTAL** | **CAD** | **$66,061.40** | **100.0%** |

---

## Benchmark Validation

The Electrical_System_Rates.csv provides ES-03 "3-phase service allowance" with a range of $45,000 to $95,000 (recommended $70,000). This estimate at $66,061.40 falls within the ES-03 range and below the recommended allowance. The estimate is more granular than the single-line allowance, decomposing the service into 21 distinct line items with individual provenance. The difference from the $70,000 recommended allowance ($3,938.60 lower) is attributable to the parametric decomposition being more precise than the broad allowance, and to professional staff management overhead being partially allocated at the deliverable level rather than absorbed into the contractor allowance.

---

## Key Warnings and Coverage Gaps

1. **Service voltage TBD** — The single most impactful design decision for this deliverable (208Y/120V vs 480Y/277V) is unresolved. This affects conductor sizing, MDP configuration, and potentially transformer requirements. ITEM-001 (service entrance materials) could swing significantly.

2. **Service ampacity TBD** — Panel size and service ampacity depend on the IFC load schedule from PKG-004. The MDP price (DL-002) uses a generic panelboard rate that may understate a large industrial-grade MDP.

3. **Utility provider TBD** — Utility application fees, connection costs, and lead times are unknown. The $2,500 utility coordination allowance (DL-006) may be insufficient if significant utility infrastructure extension is required.

4. **HVAC/mechanical loads not enumerated** — Downstream loads from PKG-003 (mechanical) are TBD and could affect service sizing.

5. **Welding equipment specs not received** — County has not yet provided welding equipment specifications (RFP §3.4). Welding circuit count (4 EA) is a parametric estimate.

6. **Service trench length estimated** — The 15m trench length is parametrically estimated from the conceptual drawing. Actual length per IFC may differ.

7. **LOW confidence items** — DL-001 (service entrance, $28,000), DL-002 (MDP, $4,800), and DL-006 (utility coordination, $2,500) are LOW confidence, totalling $35,300 (53.4% of total). These depend on PKG-004 design outputs that are not yet available.
