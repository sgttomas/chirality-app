# Estimate Configuration

This file contains configuration overrides for the estimating pipeline.

## General Settings

| Parameter | Value | Notes |
|-----------|-------|-------|
| currency | CAD | Canadian dollars (project location: Surrey, BC) |
| pricing_date | 2026-01 | January 2026 (current date) |
| estimate_label | PKG00_DRAFT | Package 00 Site Establishment estimate |
| rounding | 1000 | Round to nearest $1,000 |

## Scope Settings

### Include Scopes
- Engineering (E)
- Project Management (PM)
- Procurement (P)
- Materials (MAT)
- Construction Directs (CD)
- Construction Indirects (CI)
- Commissioning (COM)

### Exclude Scopes
- Owner's costs
- Land acquisition
- Financing costs
- Permits obtained by Employer

## Estimating Method

| Parameter | Value | Notes |
|-----------|-------|-------|
| contingency_method | PCT_BY_BUCKET | Apply contingency % by CBS bucket |
| escalation_mode | NONE | No escalation (current pricing) |

## Estimate Scope

This is a phased estimating approach where each package is estimated separately.

**Completed Packages:**
- PKG-00 Site Establishment (EST_PKG00_DRAFT_2026-01-28_2315)
- PKG-01 Demolition & Removals (EST_PKG01_DRAFT_2026-01-28_2330)

**Next Package:** PKG-02 Earthworks & Ground Improvement
