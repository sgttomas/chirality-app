# Run Context — EST_DEL-01-02_2026-02-18_1430

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-01-02_2026-02-18_1430 |
| **AsOf** | 2026-02-18T14:30:00-07:00 |
| **Scope** | DEL-01-02 (Formal Submission Package) |
| **ScopeResolvedSummary** | 1 deliverable in scope; 1 resolved; 0 excluded |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| **DEPENDENCY_SOURCES** | AUTO (read from DEL-01-02/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | EST_DEL-01-02 |

---

## Scope Resolution

| DeliverableID | PackageID | Name | Path | InScope |
|---------------|-----------|------|------|---------|
| DEL-01-02 | PKG-01 | Formal Submission Package | PKG-01_Compliance & Submission/1_Working/DEL-01-02_FormalSubmissionPackage | TRUE |

---

## Resolved Inputs

### Decomposition
- Source: `_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
- DEL-01-02 confirmed as PKG-01 deliverable; implements SOW-001 and SOW-002
- Tier: T5 (TERMINAL -- depends on all 20 other deliverables)

### Dependencies
- Source: `DEL-01-02_FormalSubmissionPackage/Dependencies.csv` (31 rows)
- 20 upstream PREREQUISITE deliverables (all other DELs in the decomposition)
- 4 ANCHOR rows (PKG-01 node, SOW-001, SOW-002, OBJ-001)
- 3 INTERFACE rows (RFP, Addenda 01-03)
- 1 CONSTRAINT row (submission deadline: Aug 30 2024 @ 2:00 PM MST)
- 1 HANDOVER row (downstream to Town of Penhold Procurement)
- All 20 prerequisite deliverables at SatisfactionStatus=PENDING

### Pricing Sources
- **Professional_Staff_Rates.csv**: 30 roles; R-22 ($105/hr), R-02 ($175/hr) applicable to DEL-01-02
- **Level_of_Effort.csv**: 2 rows for DEL-01-02: R-22 (14h), R-02 (4h)
- **Assumed_Project_Parameters.csv**: PP-04 (proposal preparation = 6 weeks) provides timeline context

### CBS Mapping Rule
- DEL-01-02 is classified as Administrative + Production per BOE Section 4
- CBS assigned: `ADMIN_PRODUCTION` (proposal assembly and submission logistics)
- Deterministic rule: Administrative/production deliverables in PKG-01 map to CBS=ADMIN_PRODUCTION

---

## Warnings

- [WARNING] TERMINAL_DELIVERABLE: DEL-01-02 is Tier 5 (depends on all 20 other deliverables being complete). All 20 upstream prerequisites are currently PENDING.
- [INFO] Estimate covers proposal production cost only (hours to assemble the final PDF submission package). No construction pricing content applies to this deliverable.
