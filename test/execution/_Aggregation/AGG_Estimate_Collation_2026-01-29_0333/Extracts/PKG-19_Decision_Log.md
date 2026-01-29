# Decision Log

## Snapshot: EST_PKG19_DRAFT_2026-01-28_0015

This log records all decisions made during estimate preparation for PKG-19 Control Systems.

---

## Decisions

### D-001: Currency Selection

| Field | Value |
|-------|-------|
| ID | D-001 |
| Decision | Use CAD (Canadian dollars) as estimate currency |
| Trigger | Currency not explicitly specified in config |
| Evidence | Project location: Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1) |
| Impacted WBS/CBS | All line items |
| Estimate Impact | None (single currency) |
| Override | Set `currency: USD` in _CONFIG.md if USD required |

---

### D-002: Single-Vendor DCS/PLC Solution

| Field | Value |
|-------|-------|
| ID | D-002 |
| Decision | Assume single-vendor integrated DCS/PLC solution |
| Trigger | Vendor strategy not defined |
| Evidence | No evidence; default assumption for D&B projects |
| Impacted WBS/CBS | MAT (control system equipment) |
| Estimate Impact | Affects system integration complexity and pricing; single-vendor typically lower integration cost |
| Override | Define vendor strategy in DEL-19.02 specification |

---

### D-003: Control System Platform Class

| Field | Value |
|-------|-------|
| ID | D-003 |
| Decision | Assume modern mid-tier DCS/PLC platform (Honeywell, Emerson, ABB, Siemens class) |
| Trigger | Platform selection not defined |
| Evidence | No evidence; default for industrial terminal of this size |
| Impacted WBS/CBS | MAT (controllers, I/O, software licenses) |
| Estimate Impact | +/- 20% depending on vendor; high-end DCS higher, PLC-based lower |
| Override | Select vendor and obtain budgetary quote |

---

### D-004: HMI Platform Integration

| Field | Value |
|-------|-------|
| ID | D-004 |
| Decision | Assume vendor-integrated HMI platform with DCS/PLC |
| Trigger | HMI vendor strategy not defined |
| Evidence | No evidence; typical for integrated systems |
| Impacted WBS/CBS | MAT (HMI workstations, software) |
| Estimate Impact | Integrated HMI typically lower cost vs. third-party |
| Override | Define HMI platform in DEL-19.02 specification |

---

### D-005: Historian Platform

| Field | Value |
|-------|-------|
| ID | D-005 |
| Decision | Assume vendor-integrated historian or OSIsoft PI class |
| Trigger | Historian vendor not specified |
| Evidence | No evidence; typical for process facilities |
| Impacted WBS/CBS | MAT (historian server, software) |
| Estimate Impact | OSIsoft PI typically higher cost; vendor-integrated lower |
| Override | Select historian platform based on Employer requirements |

---

### D-006: Software Development Responsibility

| Field | Value |
|-------|-------|
| ID | D-006 |
| Decision | Software development by control system vendor or qualified integrator |
| Trigger | Software development responsibility not defined |
| Evidence | D&B contract structure per decomposition |
| Impacted WBS/CBS | E (software development) |
| Estimate Impact | Vendor software typically more structured pricing |
| Override | Define development approach in contracting strategy |

---

### D-007: Productivity Factor

| Field | Value |
|-------|-------|
| ID | D-007 |
| Decision | Use productivity factor of 1.0 (BC lower mainland baseline) |
| Trigger | Location-specific productivity not defined |
| Evidence | Project location: Surrey, BC |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | Could vary +/- 10% based on actual site conditions |
| Override | Provide site-specific productivity assessment |

---

### D-008: Working Hours

| Field | Value |
|-------|-------|
| ID | D-008 |
| Decision | Assume standard 8-10 hour shifts |
| Trigger | Work schedule not defined |
| Evidence | No evidence; default assumption |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | Shift premium for extended hours would increase labor costs |
| Override | Define work schedule in project execution plan |

---

### D-009: Pricing Basis - Allowances

| Field | Value |
|-------|-------|
| ID | D-009 |
| Decision | All line items priced via allowances (fallback typical model) |
| Trigger | No vendor quotes or rate tables available |
| Evidence | No pricing sources found in Source_Index search |
| Impacted WBS/CBS | All |
| Estimate Impact | Estimate confidence LOW; +/- 30-50% accuracy range |
| Override | Obtain vendor budgetary quotes for control system equipment |

---

### D-010: Indirects Factor Model

| Field | Value |
|-------|-------|
| ID | D-010 |
| Decision | Use fallback typical model for indirects calculation |
| Trigger | Project-specific indirects data not available |
| Evidence | Default factors per AGENT_ESTIMATING.md |
| Impacted WBS/CBS | PM, P, CI, COM |
| Estimate Impact | Factors: CI=18% of CD, P=2% of MAT, PM=6% of CD+CI+MAT, COM=3% of CD+CI+MAT |
| Override | Provide project-specific indirects rates in _CONFIG.md |

---

### D-011: Contingency Rates Elevated

| Field | Value |
|-------|-------|
| ID | D-011 |
| Decision | Apply elevated contingency rates due to 100% allowance-based pricing |
| Trigger | All pricing via allowances; high uncertainty |
| Evidence | Fallback typical model contingency adjustment (+5% to +10% for allowance-heavy buckets) |
| Impacted WBS/CBS | CONT applied to all CBS |
| Estimate Impact | Base contingency + allowance adjustment = 15-30% by bucket; weighted average ~25% |
| Override | Reduce contingency when vendor quotes obtained |

---

### D-012: Escalation Not Applied

| Field | Value |
|-------|-------|
| ID | D-012 |
| Decision | No escalation applied; pricing in January 2026 dollars |
| Trigger | escalation_mode = NONE in _CONFIG.md |
| Evidence | Config file setting |
| Impacted WBS/CBS | None |
| Estimate Impact | Future spending would be subject to escalation in actual project |
| Override | Set escalation_mode = EXPLICIT in _CONFIG.md with escalation factors |

---

## Decision Summary

| ID | Short Description | Primary Impact |
|----|-------------------|----------------|
| D-001 | CAD currency | Currency |
| D-002 | Single-vendor DCS/PLC | MAT pricing |
| D-003 | Mid-tier platform class | MAT pricing |
| D-004 | Integrated HMI | MAT pricing |
| D-005 | Vendor/OSIsoft historian | MAT pricing |
| D-006 | Vendor software development | E pricing |
| D-007 | Productivity factor 1.0 | CD/CI pricing |
| D-008 | Standard work hours | CD/CI pricing |
| D-009 | Allowance-based pricing | Overall confidence |
| D-010 | Indirects factor model | PM/P/CI/COM |
| D-011 | Elevated contingency | CONT |
| D-012 | No escalation | ESC |
