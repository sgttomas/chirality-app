# Decision Log — PKG-20 Field Instrumentation

## Overview

This log records all decisions made during the estimating process for PKG-20 Field Instrumentation. Each decision is assigned a unique ID (D-###) and referenced from the BOE, Detail.csv, and Assumptions_Log.

---

## Decisions

### D-001: Currency Selection

| Field | Value |
|-------|-------|
| Decision | Use CAD (Canadian dollars) for all estimate values |
| Trigger | Currency not specified in scope documents |
| Evidence | Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1) |
| Impacted WBS/CBS | All line items |
| Estimate Impact | Currency consistency maintained |
| Override | Set `currency` in _CONFIG.md to change |

---

### D-002: Instrument Supply Model

| Field | Value |
|-------|-------|
| Decision | Contractor procures instruments from qualified vendors |
| Trigger | Procurement model not specified |
| Evidence | D&B contract (decomposition Section 1.2) implies Contractor responsibility |
| Impacted WBS/CBS | MAT, P |
| Estimate Impact | Procurement costs included in estimate |
| Override | If Owner-supplied instruments, remove MAT and adjust P |

---

### D-003: Instrument Calibration Approach

| Field | Value |
|-------|-------|
| Decision | Vendor factory calibration with field verification by Contractor |
| Trigger | Calibration approach not specified |
| Evidence | Industry standard practice for new instrument installations |
| Impacted WBS/CBS | CD (calibration labor), COM |
| Estimate Impact | Field calibration included at $280/instrument |
| Override | If bench calibration only, reduce field calibration scope |

---

### D-004: Cable Supply Approach

| Field | Value |
|-------|-------|
| Decision | Contractor supplies bulk instrument cable |
| Trigger | Cable supply not specified |
| Evidence | D&B contract (decomposition Section 1.2) |
| Impacted WBS/CBS | MAT |
| Estimate Impact | 8,000 m cable at $12/m included |
| Override | If cable supplied by PKG-17/19, remove MAT allocation |

---

### D-005: Junction Box Material

| Field | Value |
|-------|-------|
| Decision | NEMA 4X stainless steel junction boxes |
| Trigger | Material specification not defined |
| Evidence | Marine/industrial environment at Fraser Surrey Terminal |
| Impacted WBS/CBS | MAT |
| Estimate Impact | SS junction boxes at $2,800/unit |
| Override | If painted steel acceptable, reduce unit cost to ~$1,500 |

---

### D-006: Location Productivity Factor

| Field | Value |
|-------|-------|
| Decision | Use productivity factor of 1.0 (baseline) |
| Trigger | No project-specific productivity data |
| Evidence | BC lower mainland has standard industrial labor availability |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | No productivity adjustment applied |
| Override | Adjust if site-specific conditions warrant |

---

### D-007: Working Hours Assumption

| Field | Value |
|-------|-------|
| Decision | Standard 8-10 hour shifts assumed |
| Trigger | Schedule and shift pattern not specified |
| Evidence | Typical for D&B industrial construction in BC |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | No premium for extended shifts |
| Override | If accelerated schedule, add shift premium |

---

### D-008: Pricing Method Selection

| Field | Value |
|-------|-------|
| Decision | All pricing uses allowances (fallback typical model) |
| Trigger | No vendor quotes or rate tables available |
| Evidence | Deliverables in INITIALIZED state; no pricing sources found |
| Impacted WBS/CBS | All |
| Estimate Impact | 100% allowance-based; LOW confidence |
| Override | Provide vendor quotes to replace allowances |

---

### D-009: Indirect Cost Factors

| Field | Value |
|-------|-------|
| Decision | Apply factor-based indirects (CI=18%, P=2%, PM=6%, COM=4%) |
| Trigger | Indirect costs not explicitly defined |
| Evidence | Fallback typical model per AGENT_ESTIMATING protocol |
| Impacted WBS/CBS | CI, P, PM, COM |
| Estimate Impact | ~$222,000 in factor-based indirects |
| Override | Provide project-specific indirect rates |

Note: Commissioning factor elevated to 4% for I&C work (loop testing and calibration intensive).

---

### D-010: Contingency Rates

| Field | Value |
|-------|-------|
| Decision | Apply elevated contingency rates due to 100% allowance basis |
| Trigger | Estimate maturity is Class 5 (order of magnitude) |
| Evidence | PCT_BY_BUCKET method per _CONFIG.md with allowance adjustment |
| Impacted WBS/CBS | All CBS buckets |
| Estimate Impact | ~$408,000 contingency (26.6% overall) |
| Override | Reduce as estimate matures with quotes/quantities |

---

### D-011: Escalation Mode

| Field | Value |
|-------|-------|
| Decision | No escalation applied |
| Trigger | escalation_mode = NONE in _CONFIG.md |
| Evidence | Pricing date is current (January 2026) |
| Impacted WBS/CBS | None |
| Estimate Impact | No escalation in estimate |
| Override | Set escalation_mode = EXPLICIT in _CONFIG.md |

---

## Decision Summary

| ID | Decision Summary | Impact Level |
|----|------------------|--------------|
| D-001 | CAD currency | Low |
| D-002 | Contractor procures instruments | Medium |
| D-003 | Factory cal + field verification | Low |
| D-004 | Contractor supplies cable | Medium |
| D-005 | NEMA 4X SS junction boxes | Low |
| D-006 | Productivity factor 1.0 | Medium |
| D-007 | Standard shifts | Low |
| D-008 | All pricing via allowances | High |
| D-009 | Factor-based indirects | Medium |
| D-010 | Elevated contingency | High |
| D-011 | No escalation | Low |

---

*Decision Log generated by ESTIMATING Agent | 2026-01-28*
