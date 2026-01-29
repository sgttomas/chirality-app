# Estimate Configuration

This file contains configuration overrides for the estimating pipeline.

## General Settings

| Parameter | Value | Notes |
|-----------|-------|-------|
| currency | CAD | Canadian dollars (project location: Surrey, BC) |
| pricing_date | 2026-01 | January 2026 (current date) |
| estimate_label | PKG33_DRAFT | Package 33 HSE Management estimate |
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

**Completed Packages (30 total):**
- PKG-00 Site Establishment (EST_PKG00_DRAFT_2026-01-28_2315)
- PKG-01 Demolition & Removals (EST_PKG01_DRAFT_2026-01-28_2330)
- PKG-02 Earthworks & Ground Improvement (EST_PKG02_DRAFT_2026-01-28_2330)
- PKG-03 Underground Utilities & Drainage (EST_PKG03_DRAFT_2026-01-28_2330)
- PKG-04 Pavement & Surfacing (EST_PKG04_DRAFT_2026-01-28_2350)
- PKG-05 Concrete Structures (EST_PKG05_DRAFT_2026-01-28_2400)
- PKG-07 Rail Works (EST_PKG07_DRAFT_2026-01-28_2332)
- PKG-08 Marine Structures (EST_PKG08_DRAFT_2026-01-28_2400)
- PKG-09 Marine Outfitting (EST_PKG09_DRAFT_2026-01-28_2332)
- PKG-11 Marine Loading System (EST_PKG11_DRAFT_2026-01-28_2359)
- PKG-12 Product Transfer & Metering (EST_PKG12_DRAFT_2026-01-28_2341)
- PKG-13 Storage Tanks (EST_PKG13_DRAFT_2026-01-28_2400)
- PKG-14 Process Piping (EST_PKG14_DRAFT_2026-01-28_2400)
- PKG-15 Pumps & Rotating Equipment (EST_PKG15_DRAFT_2026-01-28_2345)
- PKG-17 Electrical Power Distribution (EST_PKG17_DRAFT_2026-01-28_0005)
- PKG-18 Lighting (EST_PKG18_DRAFT_2026-01-28_2400)
- PKG-19 Control Systems (EST_PKG19_DRAFT_2026-01-28_0015)
- PKG-20 Field Instrumentation (EST_PKG20_DRAFT_2026-01-28_2400)
- PKG-21 Building Structures & Envelope (EST_PKG21_DRAFT_2026-01-28_0030)
- PKG-23 Fire Protection (EST_PKG23_DRAFT_2026-01-28_2400)
- PKG-24 Security Systems (EST_PKG24_DRAFT_2026-01-28_0030)
- PKG-25 Communications & IT (EST_PKG25_DRAFT_2026-01-29_0004)
- PKG-26 Protective Coatings & Painting (EST_PKG26_DRAFT_2026-01-29_0006)
- PKG-27 Engineering Design (EST_PKG27_DRAFT_2026-01-29_0040)
- PKG-28 Design Verification (EST_PKG28_DRAFT_2026-01-29_0830)
- PKG-29 Testing (EST_PKG29_DRAFT_2026-01-29_0100)
- PKG-30 Commissioning (EST_PKG30_DRAFT_2026-01-29_0014)
- PKG-31 Documentation & Deliverables (EST_PKG31_DRAFT_2026-01-29_1030)
- PKG-33 HSE Management (EST_PKG33_DRAFT_2026-01-29_1100)
- PKG-35 Training & Handover (EST_PKG35_DRAFT_2026-01-29_1200)

**Remaining Packages (6 total):** PKG-06, PKG-10, PKG-16, PKG-22, PKG-32, PKG-34

**Cumulative Total (30 packages):** $101,575,000 CAD
