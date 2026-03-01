# Estimate Summary

**RunID:** EST_DEL-012-01_2026-02-27_0901
**Scope:** DEL-012-01 -- Parts Storage Room
**Package:** PKG-012 -- Interior Construction & Fit-Out
**Currency:** CAD
**Basis of Estimate:** PARAMETRIC
**RUN_STATUS:** WARNINGS

---

## Basis of Estimate Used

- **Primary Method:** PARAMETRIC -- all line items derived from parametric rates, labour rate tables, and level-of-effort allocations.
- **Fallback Applied:** ALLOW_PARAMETRIC -- parametric derivations used for items without direct rate evidence (roll-up door, shelving, anchoring, door framing).
- **Mixed Methods:** TRUE -- all items are PARAMETRIC; no method mixing required in this run.
- **Price Sources Used:** Interior_Architectural_Rates.csv, Construction_Labour_Rates.csv, Professional_Staff_Rates.csv, Level_of_Effort.csv, Building_Envelope_Rates.csv (scaling reference).

---

## Total Estimated Cost

| | Amount (CAD) |
|---|---|
| **TOTAL -- DEL-012-01 Parts Storage Room** | **$40,695.60** |

---

## Breakdown by Cost Breakdown Structure (CBS)

| CBS | Description | Amount (CAD) | % of Total | Line Count |
|---|---|---|---|---|
| 01-Management | Professional staff (PM, CPM, Superintendent, Estimator, QA/QC, HSE) | $5,590.00 | 13.7% | 6 |
| 02-Labour | Construction trade labour (Carpenter, Drywaller, Painter, Labourer) | $7,613.60 | 18.7% | 4 |
| 03-Partitions | Interior partitions + door opening framing | $7,860.00 | 19.3% | 2 |
| 03-Doors | 6-ft motorized insulated roll-up door | $5,500.00 | 13.5% | 1 |
| 03-Finishes | Wall paint + floor sealer | $1,332.00 | 3.3% | 2 |
| 03-FitOut | Shelving racking (8 bays) + anchoring | $12,800.00 | 31.5% | 2 |
| **TOTAL** | | **$40,695.60** | **100%** | **17** |

---

## Breakdown by Deliverable

| WBS_DeliverableID | Name | Amount (CAD) |
|---|---|---|
| DEL-012-01 | Parts Storage Room | $40,695.60 |

(Single-deliverable scope; no package-level rollup required.)

---

## Key Warnings and Coverage Gaps

| Warning | Description | Impact |
|---|---|---|
| W-001 | Finish schedule (DEL-001-08) not yet available; wall and floor finishes are parametric assumptions | Finish costs ($1,332) could change materially if specialty finishes specified |
| W-002 | Shelving type/capacity TBD in design; 8 bays at $1,500/bay is a parametric assumption (LOW confidence) | Shelving cost ($12,000) could range $6,400-$24,000 |
| W-003 | Roll-up door priced by scaling from 24-ft class overhead door (LOW confidence) | Door cost ($5,500) is a rough parametric derivation; supplier quote recommended |
| W-004 | Potential labour double-count: IA-01 composite rate may include installation labour that overlaps with trade labour lines L-014/L-015 | If double-counted, estimate is overstated by up to $4,935 |
| W-005 | Ceiling assumed exposed (no finish cost); if ceiling finish required, add ~$2,960+ | Could increase total by ~7% |
| W-006 | Partition height assumed 10 ft to mezzanine underside; actual TBD | Partition area and cost scale proportionally |
| W-007 | Electrical (PKG-015) and HVAC (PKG-013) costs excluded per scope boundary | These costs appear in their respective package estimates |

---

## Confidence Assessment

- **Management costs (01-Management):** MED confidence -- based on validated LOE allocations and published staff rates.
- **Trade labour (02-Labour):** MED confidence -- parametric hour estimates with validated trade rates.
- **Material/construction (03-*):** LOW to MED confidence -- significant TBDs remain in finish schedule, shelving specification, and roll-up door selection.
- **Overall:** MED-LOW confidence aggregate. Key cost driver (shelving at 31.5% of total) is LOW confidence.
