# Estimate Summary — EST_DEL-04-01_2026-02-18_1200

## Deliverable

| Field | Value |
|---|---|
| DeliverableID | DEL-04-01 |
| Name | Cold Storage -- Design Basis & Configuration |
| Package | PKG-004 -- Cold Storage Building (Unheated, 60'x100') |
| Scope boundary | Building shell only (framing, cladding, roof, gutters/downspouts, anchor bolts, erection) |

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Primary model | PB-01 from Parametric_Building_Rates.csv |
| Model description | Pre-engineered metal building (60x100 ft; clear-span; unheated; shell only) |
| Unit rate used | $32/sf (recommended; range $28-35/sf) |
| Area | 6,000 sf (DEC-001; PP-07 CONFIRMED HIGH confidence) |
| Fallback method used | ALLOWANCE (for design engineering line; per FALLBACK_POLICY=ALLOW_ALLOWANCE) |
| CURRENCY | CAD |
| ROUNDING | DOLLAR |

## Totals

| CBS | Description | Amount (CAD) | Method | Confidence |
|---|---|---|---|---|
| 04.01.SHELL | Pre-engineered metal building shell | $192,000 | PARAMETRIC | MED |
| 04.01.DESIGN | Design and engineering services (allowance) | $10,000 | ALLOWANCE | LOW |
| **TOTAL** | **DEL-04-01 Total** | **$202,000** | | |

## Cost Ownership (Scope Boundaries)

The following items are explicitly EXCLUDED from DEL-04-01 and priced under other deliverables:

| Excluded Item | Owner Deliverable | Reason |
|---|---|---|
| Doors, openings, hardware | DEL-04-02 | Cost Ownership Rules |
| Foundation + floor system | DEL-04-03 | Cost Ownership Rules |
| Electrical + ventilation | DEL-04-04 | Cost Ownership Rules |
| Building pad preparation | PKG-003 DEL-03-02 | Cost Ownership Rules |
| Concrete aprons at cold storage doors | PKG-003 DEL-03-03 | Cost Ownership Rules |
| Site utility service to cold storage | PKG-003 DEL-03-04 | Cost Ownership Rules |

## Cross-Check (Parametric Reasonableness)

| Check | Calculation | Result | Status |
|---|---|---|---|
| PB-01 shell range | 6,000 sf x $28-35/sf | $168,000 - $210,000 | PASS ($192,000 is within range at recommended rate) |
| PB-02 turnkey comparison | 6,000 sf x $48/sf = $288,000 (includes foundation + floor + doors + basic electrical + ventilation) | DEL-04-01 shell ($192,000) = 67% of turnkey ($288,000) | REASONABLE -- shell is typically 60-70% of turnkey for PEMB |
| PP-22 project parameter | PP-22 states $290,000 for cold storage (PEMB complete turnkey) | DEL-04-01 ($202,000 with design) = 70% of PP-22 ($290,000) | REASONABLE -- PP-22 includes all PKG-004 scope |

## Key Warnings

- Design engineering line (L-0401-02, $10,000) is an ALLOWANCE with LOW confidence -- no explicit design fee source was available in PRICE_SOURCES.
- PB-01 parametric rate is MEDIUM confidence; actual DB-quoted PEMB pricing may vary based on manufacturer, delivery timing, and market conditions.

## Blockers

- No hard blockers for estimating were identified. Upstream design prerequisites (DEP-04-01-E001 through E004) are design-phase information needs, not pricing blockers.
