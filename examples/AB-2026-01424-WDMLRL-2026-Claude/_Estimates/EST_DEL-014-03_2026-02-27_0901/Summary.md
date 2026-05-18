# Estimate Summary — EST_DEL-014-03_2026-02-27_0901

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Scope | DEL-014-03 — Bulk Water Fill System |
| Package | PKG-014 — Plumbing & Water Systems Installation |
| SOW | SOW-0044 |

All 23 line items are priced using PARAMETRIC method. Two pricing source files provided direct rate evidence (Construction_Labour_Rates.csv for trade labour and Underground_Utility_Rates.csv for piping). Professional staff costs are derived from Level_of_Effort.csv hours combined with Professional_Staff_Rates.csv rates. Equipment and specialty items are parametrically derived from comparable industry pricing in the absence of vendor quotes.

---

## Totals by CBS Category

| CBS | Amount (CAD) | Line Count | Notes |
|---|---|---|---|
| EQUIPMENT | $8,500.00 | 1 | High-volume pump — parametric; no quote |
| MATERIAL | $11,075.00 | 10 | Piping, fittings, valves, connections, freeze protection, wall sleeve, pump mount, conduit stub, cistern connection, bollard |
| LABOUR | $6,759.20 | 3 | Plumber (56 hr) + labourer (24 hr) — burdened rates |
| TESTING | $750.00 | 2 | Pressure test + system flush |
| COMMISSIONING | $2,550.00 | 4 | Pump test, backflow verification, freeze check, cistern integration |
| REGULATORY | $1,500.00 | 1 | Plumbing permit and inspection fees |
| CLOSEOUT | $1,600.00 | 1 | As-built drawings, O&M manual, warranty docs |
| MANAGEMENT | $5,590.00 | 1 | Professional staff (38 hr from LOE) |
| **GRAND TOTAL** | **$38,324.20** | **23** | |

---

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) |
|---|---|---|
| PKG-014 | DEL-014-03 | $38,324.20 |

---

## Key Warnings and Coverage Gaps

1. **Pump specification TBD.** The pump flow rate (LPM) is not specified in available sources. The $8,500 pump cost is a parametric estimate based on comparable industrial transfer pumps. Actual cost may range from $5,000 to $12,000+ depending on specified flow rate. This is the single largest uncertainty in the estimate.

2. **Fill connection size TBD.** The 2.5" connection in RFP S3.4 is for the internal distribution pump (DEL-014-01), not the bulk fill point. Pipe sizing assumption (2-3 inch) drives the piping rate used.

3. **Freeze protection method TBD.** Heat trace + insulation assumed; drain-back design could be lower cost. Freeze protection accounts for $1,275 of material cost.

4. **Backflow device type TBD.** DCVA assumed; an RPZ device or other type could change cost significantly.

5. **Bidirectional operation ambiguity (Conflict C-003).** Estimate prices cistern replenishment direction only. If extraction (cistern-to-vehicle) is also required, additional piping, valves, and potentially a different pump configuration would increase cost.

6. **Fill line run length assumed at 15 m.** Actual routing TBD in IFC design. Piping and heat trace costs scale linearly with length.

7. **No vendor quotes available.** All items are PARAMETRIC with LOW to MEDIUM confidence. A rerun with vendor quotes would materially improve accuracy.

8. **Plumbing permit fee is a jurisdictional allowance.** Actual fee depends on Camrose County / Alberta Safety Codes fee schedule.

---

## Confidence Assessment

- **Overall confidence: LOW-MEDIUM.** The estimate is based entirely on parametric methods without vendor quotes. Multiple critical design parameters are TBD. The estimate is suitable for order-of-magnitude budgeting but should be refined when IFC design (PKG-006) is complete and vendor quotations are obtained.
- **Highest confidence items:** Labour rates (from rate tables) and professional staff costs (from LOE + staff rate tables).
- **Lowest confidence items:** Pump equipment, backflow device, and regulatory fees.
