# Basis of Estimate Collection -- Project Level

## Overview

This document collects the basis-of-estimate evidence from all 30 deliverable-level estimate snapshots. The authoritative per-deliverable source is each snapshot's `Run_Context.md`. This collection is a convenience index for project-level review.

**Project:** Town of Penhold -- Public Services Building (PSB)
**Currency:** CAD
**Base Year:** 2024
**BOE Strategy Document:** `_Estimates/BASIS_OF_ESTIMATE.md`

---

## Basis Summary by Package

### PKG-001 -- General Requirements & Delivery Controls

All 7 deliverables use `BASIS_OF_ESTIMATE = RATE_TABLE` with rates from `Professional_Staff_Rates.csv` and hours from `Level_of_Effort.csv`. Permit fees in DEL-01-04 use ALLOWANCE method (authorized by `FALLBACK_POLICY=ALLOW_ALLOWANCE`).

**Update (2130 snapshot):** DEL-01-02, DEL-01-03, and DEL-01-06 were re-estimated with `FALLBACK_POLICY=ALLOW_ALLOWANCE` to resolve previously-TBD line items. DEL-01-02 added 1 ALLOWANCE line (scheduling software $3,500). DEL-01-03 added 2 ALLOWANCE lines (training $4,500 + PPE/signage $3,500). DEL-01-06 added 2 ALLOWANCE lines (temporary facilities $35,000 + site cleaning $25,000). All 5 ALLOWANCE lines are LOW confidence parametric allowances authorized by DEC-EST-005 in the source snapshots.

| DEL | Declared Basis | Actual Methods | Fallback Policy | Run Status |
|---|---|---|---|---|
| DEL-01-01 | RATE_TABLE | RATE_TABLE | STRICT | OK |
| DEL-01-02 | RATE_TABLE | ALLOWANCE, RATE_TABLE | ALLOW_ALLOWANCE | WARNINGS |
| DEL-01-03 | RATE_TABLE | ALLOWANCE, RATE_TABLE | ALLOW_ALLOWANCE | WARNINGS |
| DEL-01-04 | RATE_TABLE | ALLOWANCE, RATE_TABLE | ALLOW_ALLOWANCE | WARNINGS |
| DEL-01-05 | RATE_TABLE | RATE_TABLE | STRICT | WARNINGS |
| DEL-01-06 | RATE_TABLE | ALLOWANCE, RATE_TABLE | ALLOW_ALLOWANCE | WARNINGS |
| DEL-01-07 | RATE_TABLE | RATE_TABLE | STRICT | OK |

**Key price sources:** Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Fees_Permits_Insurance.csv

---

### PKG-002 -- Main Public Services Building

6 of 7 deliverables use `BASIS_OF_ESTIMATE = RATE_TABLE`. DEL-02-07 declares `QUOTE` but falls back to `ALLOWANCE` (no vendor quote available).

**Update (2130 snapshot):** DEL-02-01 was re-estimated with the new `Interior_Architectural_Rates.csv` price source (PS-27). All 7 previously-TBD lines (partitions, floor finishes, ceiling, accessibility, wayfinding signage, paint, and interior design fees) are now priced using RATE_TABLE method. DEL-02-01 total increased from $47,200 to $168,329 (+$121,129 / +256%). Fallback policy remains STRICT as all lines use RATE_TABLE.

| DEL | Declared Basis | Actual Methods | Fallback Policy | Run Status |
|---|---|---|---|---|
| DEL-02-01 | RATE_TABLE | RATE_TABLE | STRICT | WARNINGS |
| DEL-02-02 | RATE_TABLE | ALLOWANCE, RATE_TABLE | ALLOW_ALLOWANCE | WARNINGS |
| DEL-02-03 | RATE_TABLE | ALLOWANCE, RATE_TABLE | ALLOW_ALLOWANCE | WARNINGS |
| DEL-02-04 | RATE_TABLE | RATE_TABLE | STRICT | WARNINGS |
| DEL-02-05 | RATE_TABLE | RATE_TABLE | STRICT | OK |
| DEL-02-06 | RATE_TABLE | RATE_TABLE | STRICT | OK |
| DEL-02-07 | QUOTE | ALLOWANCE | ALLOW_ALLOWANCE | WARNINGS |

**Key price sources:** Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Interior_Architectural_Rates.csv, Equipment_Pricing.csv, Mechanical_System_Rates.csv, Electrical_System_Rates.csv, Construction_Labour_Rates.csv, Professional_Design_Fees.csv

---

### PKG-003 -- Site & Civil Works

All 5 deliverables use `BASIS_OF_ESTIMATE = RATE_TABLE`. Several include ALLOWANCE fallback lines for fees and tie-in costs.

| DEL | Declared Basis | Actual Methods | Fallback Policy | Run Status |
|---|---|---|---|---|
| DEL-03-01 | RATE_TABLE | RATE_TABLE | STRICT | WARNINGS |
| DEL-03-02 | RATE_TABLE | RATE_TABLE | STRICT | WARNINGS |
| DEL-03-03 | RATE_TABLE | RATE_TABLE | STRICT | WARNINGS |
| DEL-03-04 | RATE_TABLE | ALLOWANCE, RATE_TABLE | ALLOW_ALLOWANCE | WARNINGS |
| DEL-03-05 | RATE_TABLE | ALLOWANCE, RATE_TABLE | ALLOW_ALLOWANCE | WARNINGS |

**Key price sources:** Earthwork_Civil_Rates.csv, Paving_Surfacing_Rates.csv, Underground_Utility_Rates.csv, Fees_Permits_Insurance.csv, Professional_Design_Fees.csv

---

### PKG-004 -- Cold Storage Building

4 deliverables. DEL-04-01 uses PARAMETRIC basis (shell rate x area). Others use RATE_TABLE.

| DEL | Declared Basis | Actual Methods | Fallback Policy | Run Status |
|---|---|---|---|---|
| DEL-04-01 | PARAMETRIC | ALLOWANCE, PARAMETRIC | ALLOW_ALLOWANCE | OK |
| DEL-04-02 | RATE_TABLE | RATE_TABLE | STRICT | OK |
| DEL-04-03 | RATE_TABLE | RATE_TABLE | STRICT | WARNINGS |
| DEL-04-04 | RATE_TABLE | RATE_TABLE | STRICT | OK |

**Key price sources:** Parametric_Building_Rates.csv, Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Equipment_Pricing.csv, Construction_Labour_Rates.csv, Electrical_System_Rates.csv, Mechanical_System_Rates.csv

---

### PKG-005 -- Optional Priced Items

Mixed basis across deliverables. Several use QUOTE with ALLOWANCE fallback. DEL-05-03 and DEL-05-04 use PARAMETRIC.

| DEL | Declared Basis | Actual Methods | Fallback Policy | Run Status |
|---|---|---|---|---|
| DEL-05-01 | QUOTE | ALLOWANCE | ALLOW_ALLOWANCE | WARNINGS |
| DEL-05-02 | RATE_TABLE | RATE_TABLE | STRICT | WARNINGS |
| DEL-05-03 | QUOTE | PARAMETRIC | ALLOW_ALLOWANCE | WARNINGS |
| DEL-05-04 | QUOTE | PARAMETRIC | ALLOW_ALLOWANCE | WARNINGS |
| DEL-05-05 | QUOTE | ALLOWANCE | ALLOW_ALLOWANCE | WARNINGS |
| DEL-05-06 | QUOTE | QUOTE | STRICT | WARNINGS |
| DEL-05-07 | ALLOWANCE | ALLOWANCE | STRICT | OK |

**Key price sources:** Optional_Items_Pricing.csv

---

## Method Mix Summary (All 266 Priced Lines)

| Method | Lines | Amount (CAD) | % of Amount |
|---|---|---|---|
| RATE_TABLE | 220 | $6,216,696 | 86.1% |
| ALLOWANCE | 36 | $692,150 | 9.6% |
| PARAMETRIC | 4 | $292,400 | 4.1% |
| QUOTE | 6 | $18,600 | 0.3% |
| TBD (unpriced) | 0 | -- | -- |

---

## Confidence Summary (266 Priced Lines)

| Confidence | Lines | Amount (CAD) |
|---|---|---|
| HIGH | 2 | $30,770 |
| MED / MEDIUM | 216 | $6,118,156 |
| LOW | 48 | $1,070,920 |

The LOW-confidence lines are concentrated in:
- PKG-005 optional items (ALLOWANCE/PARAMETRIC; no vendor quotes)
- DEL-02-07 emergency generator (ALLOWANCE; no vendor quote)
- DEL-03-02 earthwork quantities (assumed cut/fill volumes)
- DEL-03-04 utility connection fees and tie-in allowances
- DEL-01-02 scheduling software allowance ($3,500)
- DEL-01-03 training and PPE allowances ($8,000)
- DEL-01-06 temporary facilities and site cleaning allowances ($60,000)
