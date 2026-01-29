# Decision Log

## PKG-13 Storage Tanks Estimate

### Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG13_DRAFT_2026-01-28_2400 |
| Estimate Label | PKG13_DRAFT |
| Date | 2026-01-28 |

---

## Decisions

### D-001: Currency Selection

| Field | Value |
|-------|-------|
| Decision | Use CAD (Canadian dollars) as estimate currency |
| Trigger | Currency not specified in config for this package |
| Evidence | Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1) |
| Impacted WBS/CBS | All |
| Estimate Impact | All pricing in CAD |
| Override | Set currency in _CONFIG.md if USD or other currency required |

---

### D-002: Tank Supply Method

| Field | Value |
|-------|-------|
| Decision | Assume field-erected tanks by qualified tank fabricator |
| Trigger | Tank erection method not specified |
| Evidence | 15,000 MT capacity (~16,300 m³) typical for field erection; shop-built would be impractical |
| Impacted WBS/CBS | MAT, CD |
| Estimate Impact | Pricing based on field erection with shop-fabricated courses |
| Override | Confirm erection method in DEL-13.02 specification |

---

### D-003: Tank Fabrication Method

| Field | Value |
|-------|-------|
| Decision | Shop-fabricated shell courses with field erection |
| Trigger | Fabrication approach not specified |
| Evidence | Typical practice for large API 650 tanks; quality control advantages |
| Impacted WBS/CBS | MAT, CD |
| Estimate Impact | Included in tank supply and erection allowances |
| Override | Confirm fabrication approach in DEL-13.02 specification |

---

### D-004: Agitator Supply Approach

| Field | Value |
|-------|-------|
| Decision | OEM supply with Contractor installation |
| Trigger | Agitator procurement approach not specified |
| Evidence | Typical for mechanical equipment; vendor design for tank geometry |
| Impacted WBS/CBS | MAT, CD |
| Estimate Impact | Separate supply and installation line items |
| Override | Confirm procurement approach in project execution plan |

---

### D-005: Internal Coating Responsibility

| Field | Value |
|-------|-------|
| Decision | Internal coating by tank vendor as part of tank supply |
| Trigger | Coating responsibility not specified |
| Evidence | Typical for food-grade applications; vendor warranty considerations |
| Impacted WBS/CBS | MAT |
| Estimate Impact | Coating included in MAT allowance |
| Override | Confirm with PKG-26 scope definition |

---

### D-006: External Coating Responsibility

| Field | Value |
|-------|-------|
| Decision | External coating by tank vendor or coating contractor |
| Trigger | Coating responsibility not specified |
| Evidence | Can be tank vendor scope or separate coating contract |
| Impacted WBS/CBS | MAT |
| Estimate Impact | Coating included in MAT allowance |
| Override | Confirm with PKG-26 scope definition |

---

### D-007: Productivity Factor

| Field | Value |
|-------|-------|
| Decision | Use 1.0 productivity factor for BC lower mainland |
| Trigger | Site-specific productivity data not available |
| Evidence | BC lower mainland has adequate skilled labor pool; baseline assumption |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | Direct and indirect labor costs at baseline rates |
| Override | Adjust if site conditions warrant premium (access, congestion, etc.) |

---

### D-008: Working Hours

| Field | Value |
|-------|-------|
| Decision | Standard 8-10 hour shifts |
| Trigger | Work schedule not specified |
| Evidence | Default for industrial construction in BC |
| Impacted WBS/CBS | CD, CI |
| Estimate Impact | No shift premium included |
| Override | If extended hours or shifts required, adjust labor rates |

---

### D-009: Pricing Basis

| Field | Value |
|-------|-------|
| Decision | All line items priced via allowances (fallback typical model) |
| Trigger | No vendor quotes or rate tables available |
| Evidence | No pricing sources discovered during source indexing |
| Impacted WBS/CBS | All |
| Estimate Impact | All line items marked ALLOWANCE or PARAMETRIC; confidence LOW |
| Override | Provide vendor quotes or rate tables for next estimate run |

---

### D-010: Indirects Factor Method

| Field | Value |
|-------|-------|
| Decision | Use factor-based indirects model (fallback typical) |
| Trigger | Project-specific indirects data not available |
| Evidence | CI=18% of CD, P=2% of MAT, PM=6% of base, COM=3% of base |
| Impacted WBS/CBS | CI, P, PM, COM |
| Estimate Impact | Indirects derived from direct cost base |
| Override | Provide project-specific indirects breakdown or schedule-based model |

---

### D-011: Contingency Rates

| Field | Value |
|-------|-------|
| Decision | Elevated contingency rates due to 100% allowance-based estimate |
| Trigger | No quotes available; all pricing via allowances |
| Evidence | Fallback typical model with AllowanceShare adjustment |
| Impacted WBS/CBS | CONT |
| Estimate Impact | Contingency ~25.9% of base ($5.235M on $20.245M) |
| Override | Reduce contingency as vendor quotes replace allowances |

---

### D-012: Escalation Mode

| Field | Value |
|-------|-------|
| Decision | No escalation applied (NONE mode) |
| Trigger | Config default; pricing date is current |
| Evidence | Pricing date 2026-01 is current month |
| Impacted WBS/CBS | None |
| Estimate Impact | No escalation reserve included |
| Override | Enable EXPLICIT escalation in _CONFIG.md if project schedule extends pricing validity |

---

## Decision Summary

| ID | Decision | Impact |
|----|----------|--------|
| D-001 | CAD currency | All pricing |
| D-002 | Field-erected tanks | MAT/CD split |
| D-003 | Shop-fabricated courses | Quality/cost basis |
| D-004 | OEM agitator supply | Procurement approach |
| D-005 | Tank vendor internal coating | MAT scope |
| D-006 | Tank vendor external coating | MAT scope |
| D-007 | 1.0 productivity factor | Labor rates |
| D-008 | Standard shift hours | No premium |
| D-009 | Allowance-based pricing | LOW confidence |
| D-010 | Factor-based indirects | CI/P/PM/COM |
| D-011 | Elevated contingency | 25.9% reserve |
| D-012 | No escalation | Current pricing |
