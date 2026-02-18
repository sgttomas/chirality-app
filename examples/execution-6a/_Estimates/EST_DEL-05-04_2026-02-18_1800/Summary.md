# Estimate Summary: DEL-05-04 -- Option -- Security & Camera System

## Run Identity

- **Snapshot:** EST_DEL-05-04_2026-02-18_1800
- **Deliverable:** DEL-05-04_Optional-Security-and-Cameras (PKG-005)
- **Scope Item:** SOW-0503

## Basis of Estimate

- **Declared basis:** QUOTE
- **Actual method used:** PARAMETRIC (fallback -- no vendor quote available)
- **Fallback authority:** FALLBACK_POLICY=ALLOW_ALLOWANCE; ALLOW_MIXED_METHODS=TRUE
- **All line items require vendor quote replacement before final submission.**

## Totals

| CBS | Description | Amount (CAD) | Method | Confidence |
|---|---|---|---|---|
| 26-SECURITY | Camera system -- equipment, cabling, installation, commissioning (16 cameras assumed) | $50,000 | PARAMETRIC | LOW |
| 26-SECURITY-MONITORING | Monitoring service -- annual subscription | $5,400 | PARAMETRIC | LOW |
| **TOTAL** | **DEL-05-04 combined** | **$55,400** | | |

### Cost Separation (per RFP OSR 12.4)

| Cost Category | Amount (CAD) | Notes |
|---|---|---|
| Installation cost (equipment + install) | $50,000 | One-time capital cost |
| Monitoring cost (annual) | $5,400 | Recurring operating cost |

### Price Ranges (from source data)

| Line | Min (CAD) | Recommended (CAD) | Max (CAD) |
|---|---|---|---|
| Camera system (OPT-08) | $40,000 | $50,000 | $60,000 |
| Monitoring (OPT-09) | $3,600 | $5,400 | $7,200 |
| **Range total** | **$43,600** | **$55,400** | **$67,200** |

## Key Warnings

1. **No vendor quote exists.** All pricing is parametric placeholder from Optional_Items_Pricing.csv. LOW confidence on all lines.
2. **Camera count is assumed at 16 locations** (PP-29, LOW confidence). Actual count depends on finalization of DEL-02-01 (architectural layout).
3. **Scope boundary with DEL-02-06** (IT/telecom) requires coordination to avoid double-counting network equipment.
4. **Monitoring cost is Year 1 only.** Multi-year contract terms not addressed.

## Blockers to QUOTE-Basis Rerun

- Obtain vendor quotes for camera system (2-3 competitive quotes recommended)
- Finalize architectural layout (DEL-02-01) to confirm camera locations
- Confirm IT/network scope split with DEL-02-06

## Scope Coverage

- **In scope:** 1 deliverable (DEL-05-04)
- **Line items:** 2
- **Provenance completeness:** 100% (all lines have traceable SourceRef)

## Cost Ownership Verification

- Camera equipment, wiring, and installation: **included** (L-0504-01)
- Monitoring service: **included** (L-0504-02)
- IT network backbone, electrical circuits, exterior lighting: **excluded** (owned by DEL-02-06)
