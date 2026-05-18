# Source Index

**RunID:** EST_DEL-02-05_2026-02-18_2200

---

## Pricing Sources

| # | Source File | Source Type | What It Supports | Parsing Notes |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | Hourly rates (CAD) for 30 professional roles; used as UnitRate for all line items | CSV; 30 data rows; RoleID key; HourlyRate_CAD column; Basis=MARKET; Confidence=MEDIUM |
| 2 | `_PriceSources/Level_of_Effort.csv` | Level of Effort (hours by role by deliverable) | Estimated hours per role per deliverable; used as Qty for all line items | CSV; 73 data rows; filtered to Execution=6b and DeliverableID=DEL-02-05 (2 matching rows); Basis=PARAMETRIC |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | Contextual project parameters (areas, quantities, durations, financial estimates) | CSV; 29 data rows; not directly used for pricing DEL-02-05; provides context for overall project scope |

---

## Dependency Sources

| # | Source File | Source Type | What It Supports |
|---|---|---|---|
| 4 | `DEL-02-05_ElectricalITConceptNarrative/Dependencies.csv` | Dependency Register | Blocker/readiness assessment; 15 rows (4 anchor, 11 execution); no pricing evidence extracted |

---

## Decomposition Source

| # | Source File | Source Type | What It Supports |
|---|---|---|---|
| 5 | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Decomposition (v2.3 FINAL) | Package IDs, deliverable IDs, labels, scope item mappings, objective traceability |

---

## Source Limitations

- Rate table rates are MARKET-basis with MEDIUM confidence; no firm-specific rate cards available.
- Level of effort hours are PARAMETRIC-basis; they represent estimated hours to produce the narrative, not actual tracked hours.
- No construction cost sources are relevant to this deliverable (DEL-02-05 is a proposal-production narrative, not a construction pricing item).
