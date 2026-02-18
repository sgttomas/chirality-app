# Source Index

**RunID:** EST_DEL-02-03_2026-02-18_2100

## Indexed Price Sources

| # | Source File | Source Type | Used For | Parsing Notes |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | Hourly rates (CAD) by RoleID | 30 roles; all rates in CAD; Basis=MARKET; Confidence=MEDIUM for all professional roles |
| 2 | `_PriceSources/Level_of_Effort.csv` | Level of Effort Table | Estimated hours by DeliverableID + RoleID | 73 rows across all deliverables; Execution=6b; filtered to DEL-02-03 rows (2 rows matched) |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Parameters / Context | Background context for project scope and quantities | 29 parameters; not directly used for line-item pricing; provides context (building areas, bay counts, etc.) |

## DEL-02-03 Rows Extracted from Level_of_Effort.csv

| Row | DeliverableID | RoleID | Role | EstimatedHours | Basis | Notes |
|---|---|---|---|---:|---|---|
| 29 | DEL-02-03 | R-09 | Structural Engineer (Senior) | 16 | PARAMETRIC | Foundation approach; framing system; expansion provisions; narrative writing |
| 30 | DEL-02-03 | R-10 | Structural Engineer (Intermediate) | 8 | PARAMETRIC | Supporting calculations; sketch review |

## DEL-02-03 Rates Extracted from Professional_Staff_Rates.csv

| Row | RoleID | Role | HourlyRate_CAD | Basis | Confidence |
|---|---|---|---:|---|---|
| 10 | R-09 | Structural Engineer (Senior) | 155 | MARKET | MEDIUM |
| 11 | R-10 | Structural Engineer (Intermediate) | 125 | MARKET | MEDIUM |

## Sources NOT Used

- `Assumed_Project_Parameters.csv`: Referenced for context only (building areas, bay sump counts). No pricing was derived from this file.

## Source Limitations

- Rate table rates are MARKET basis with MEDIUM confidence. No firm-specific negotiated rates were available.
- Level of effort hours are PARAMETRIC basis with MEDIUM confidence. Hours represent an estimate of typical effort for this deliverable type on a project of this scale.
- No quote-based or historical-actual evidence was available for this deliverable.
