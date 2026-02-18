# Estimating Configuration

This file provides configuration overrides for the ESTIMATING agent. Edit these values to customize the next estimate run.

---

## Configuration Keys

| Key | Current Value | Default | Description |
|-----|---------------|---------|-------------|
| **currency** | CAD | CAD | Estimate currency (single currency per snapshot) |
| **pricing_date** | 2026-02 | Current month | Pricing basis date (YYYY-MM) |
| **estimate_label** | AUTO_DRAFT | AUTO_DRAFT | Label prefix for snapshot ID |
| **include_scopes** | Engineering, Procurement, Construction, Indirects, Commissioning | All | CBS categories to include |
| **exclude_scopes** | Owner costs, Land, Financing | Owner costs, Land, Financing | CBS categories to exclude |
| **contingency_method** | PCT_BY_BUCKET | PCT_BY_BUCKET | Contingency calculation method (PCT_BY_BUCKET or RISK_BASED) |
| **escalation_mode** | NONE | NONE | Escalation handling (NONE or EXPLICIT) |
| **rounding** | 1000 | 1000 | Rounding precision (nearest $X) |

---

## Rate Tables

If rate tables are provided, place them in:
```
_Estimates/_RateTables/
```

Supported formats: CSV, XLSX, MD

Rate tables take priority over allowance-based pricing.

---

## Override Instructions

To override default values for the next estimate run:

1. Edit the "Current Value" column above
2. Save this file
3. Run the ESTIMATING agent

The agent will read this configuration and apply overrides.

---

## Notes

- This is a template configuration file
- All values shown are defaults used for EST_DEL-05-02_2026-02-04_1322
- Currency must be single currency per snapshot (no mixing)
- Contingency methods:
  - PCT_BY_BUCKET: Apply percentage by CBS category
  - RISK_BASED: Three-point estimate with P50/P80 ranges
- Escalation modes:
  - NONE: No explicit escalation (assume captured in rates)
  - EXPLICIT: Calculate escalation based on schedule/cashflow

---

## Document Information

| Field | Value |
|-------|-------|
| Created | 2026-02-04 |
| Last Updated | 2026-02-04 |
| Template Version | 1.0 |
