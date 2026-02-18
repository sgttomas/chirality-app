# Decision Log: EST_DEL-09-02_2026-02-04_1323

## Snapshot Information
- **Snapshot ID:** EST_DEL-09-02_2026-02-04_1323
- **Deliverable:** DEL-09-02 Site Conditions and Due Diligence Summary
- **Package:** PKG-09 Due Diligence & Risk Register
- **Created:** 2026-02-04

---

## Decision Register

### D-001: Pricing Basis Selection
| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision Statement** | Use allowance-based pricing with fallback typical model; no rate tables or quotes available |
| **Trigger** | No explicit pricing sources (quotes, rate tables) found in project workspace |
| **Evidence** | Source Index search confirmed no `_RateTables/` content; no vendor quotes referenced |
| **Impacted WBS/CBS** | All line items for DEL-09-02; CBS categories E, PM |
| **Estimate Impact** | HIGH - All pricing derived from allowances with LOW confidence |
| **Override for Next Run** | Provide rate tables in `_Estimates/_RateTables/` or professional services quotes |

### D-002: Currency Selection
| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision Statement** | Currency set to CAD per instruction brief |
| **Trigger** | Currency must be specified for estimate validity |
| **Evidence** | User instruction explicitly states "Currency: CAD" |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | N/A - Directive compliance |
| **Override for Next Run** | Change via `_CONFIG.md` currency setting |

### D-003: Pricing Date Selection
| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision Statement** | Pricing date set to 2026-02 (February 2026 dollars) |
| **Trigger** | Pricing date required for estimate basis; no explicit pricing date in documents |
| **Evidence** | No pricing date found; default to current month per protocol |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | LOW - Pricing reflects current market conditions |
| **Override for Next Run** | Specify pricing_date in `_CONFIG.md` |

### D-004: CBS Mapping for Due Diligence Deliverable
| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision Statement** | DEL-09-02 mapped to CBS categories: Engineering & Design (E) and Project Management (PM) |
| **Trigger** | Deliverable type is "Summary Document" requiring professional services effort |
| **Evidence** | _CONTEXT.md specifies "Type: Summary Document", "Responsible: PM + Technical Leads" |
| **Impacted WBS/CBS** | PKG-09/DEL-09-02; CBS E and PM |
| **Estimate Impact** | MEDIUM - Determines which CBS buckets receive costs |
| **Override for Next Run** | Modify CBS mapping if deliverable scope changes |

### D-005: Effort Estimation Approach
| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision Statement** | Estimate effort based on: (1) number of reference reports to review, (2) number of specification requirements to address, (3) anticipated artifacts to produce |
| **Trigger** | Need quantifiable basis for allowance calculation |
| **Evidence** | Datasheet lists 11 reference documents; Specification lists 16 requirements; _CONTEXT.md lists 7 anticipated artifacts |
| **Impacted WBS/CBS** | Engineering effort allocation |
| **Estimate Impact** | MEDIUM - Drives engineering hours calculation |
| **Override for Next Run** | Provide actual effort tracking from similar past projects |

### D-006: Professional Rate Assumptions
| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision Statement** | Use typical Alberta professional services rates: PM $175/hr, Senior Engineer $150/hr, Engineer $125/hr, Technical Support $85/hr |
| **Trigger** | No rate tables available; need hourly rates for effort-based pricing |
| **Evidence** | Alberta consulting market typical rates 2024-2026; no project-specific rates |
| **Impacted WBS/CBS** | All E and PM line items |
| **Estimate Impact** | HIGH - Rate assumptions directly affect total cost |
| **Override for Next Run** | Provide project-specific rate table or actual contractor rates |

### D-007: Contingency Method Selection
| Field | Value |
|-------|-------|
| **Decision ID** | D-007 |
| **Decision Statement** | Use PCT_BY_BUCKET contingency method with 15% contingency on allowance-heavy scope |
| **Trigger** | Default contingency method per protocol; higher percentage due to LOW confidence pricing |
| **Evidence** | Protocol default is PCT_BY_BUCKET; allowance-heavy estimate warrants higher % per protocol guidance |
| **Impacted WBS/CBS** | Contingency (CONT) CBS bucket |
| **Estimate Impact** | MEDIUM - Adds ~15% to base estimate |
| **Override for Next Run** | Switch to RISK_BASED if risk register quantification available |

### D-008: Scope Exclusions
| Field | Value |
|-------|-------|
| **Decision ID** | D-008 |
| **Decision Statement** | Exclude from estimate: actual geotechnical investigation costs, environmental assessment costs, survey costs (these are separate scope items or owner-provided) |
| **Trigger** | DEL-09-02 is a summary document, not the investigations themselves |
| **Evidence** | Specification.md clearly states deliverable scope excludes detailed geotechnical design, wetland permitting applications, environmental remediation, detailed grading design, survey execution |
| **Impacted WBS/CBS** | Ensures no double-counting with other packages |
| **Estimate Impact** | N/A - Correct scope boundary |
| **Override for Next Run** | If scope changes to include investigations, add relevant line items |

---

## Decision Summary Statistics
- **Total Decisions:** 8
- **HIGH Impact Decisions:** 2 (D-001, D-006)
- **MEDIUM Impact Decisions:** 4 (D-004, D-005, D-007, D-008)
- **LOW/N/A Impact Decisions:** 2 (D-002, D-003)

---

**Decision Log Generated:** 2026-02-04
