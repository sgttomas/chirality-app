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

This estimate covers **PKG-00 Site Establishment only** (8 deliverables: DEL-00.01 through DEL-00.08).

This is a phased estimating approach where each package is estimated separately.
