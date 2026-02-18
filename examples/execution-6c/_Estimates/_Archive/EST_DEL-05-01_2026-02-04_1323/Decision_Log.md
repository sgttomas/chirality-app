# Decision Log

## Snapshot: EST_DEL-05-01_2026-02-04_1323

This log records all decisions made during estimate generation, including defaults, ambiguity resolutions, and methodology selections.

---

## D-001: Currency Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-001 |
| **Decision** | Currency set to CAD (Canadian Dollars) |
| **Trigger** | Currency must be established for estimate; RFP does not explicitly state currency |
| **Evidence** | Datasheet.md: "Currency assumed CAD - standard for Alberta municipal procurement"; RFP context (Town of Penhold, Alberta) |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | All values denominated in CAD |
| **Override Path** | Update _CONFIG.md with `currency: [value]` for next run |

---

## D-002: Pricing Method Selection (Allowances)

| Field | Value |
|-------|-------|
| **Decision ID** | D-002 |
| **Decision** | Use allowance/parametric pricing for all line items |
| **Trigger** | No vendor quotes, rate tables, or historical data available |
| **Evidence** | _RateTables/ folder empty; no quotes in _Sources/; AGENT_ESTIMATING.md Phase 3.3 allows fallback to allowances |
| **Impacted WBS/CBS** | All line items |
| **Estimate Impact** | HIGH - All costs are parametric benchmarks with -30%/+50% accuracy range |
| **Override Path** | Provide rate tables in `_Estimates/_RateTables/` or vendor quotes before next run |

---

## D-003: Contingency Percentage

| Field | Value |
|-------|-------|
| **Decision ID** | D-003 |
| **Decision** | Apply 15% contingency to base estimate (pre-contingency) |
| **Trigger** | Contingency method defaulted to PCT_BY_BUCKET; must select percentage |
| **Evidence** | AGENT_ESTIMATING.md STRUCTURE section: "allow higher % for ALLOWANCE-heavy buckets"; 100% allowance basis warrants conservative contingency |
| **Impacted WBS/CBS** | CONT (Contingency line) |
| **Estimate Impact** | $1,398,000 CAD contingency reserve |
| **Override Path** | Set `contingency_method` and percentage in _CONFIG.md |

---

## D-004: Indirects Factor

| Field | Value |
|-------|-------|
| **Decision ID** | D-004 |
| **Decision** | Apply 8% construction indirects factor to construction directs |
| **Trigger** | No time-based or detailed indirects model available |
| **Evidence** | AGENT_ESTIMATING.md Phase 3.4: "factor-based model (default) using fallback typical model"; 8% is mid-range for D-B |
| **Impacted WBS/CBS** | CI (Construction Indirects) |
| **Estimate Impact** | $584,000 CAD indirects allowance |
| **Override Path** | Provide schedule/duration data or explicit indirects rate table |

---

## D-005: Engineering & Design Percentage

| Field | Value |
|-------|-------|
| **Decision ID** | D-005 |
| **Decision** | Apply 8% engineering & design factor to estimated construction cost |
| **Trigger** | No design fee schedule or historical project data available |
| **Evidence** | Typical Design-Build range 8-12%; selected lower end as conservative for municipal institutional project |
| **Impacted WBS/CBS** | E (Engineering & Design) |
| **Estimate Impact** | $528,000 CAD E&D allowance |
| **Override Path** | Provide design services quote or historical percentage from similar projects |

---

## D-006: Project Management Percentage

| Field | Value |
|-------|-------|
| **Decision ID** | D-006 |
| **Decision** | Apply 4% project management factor |
| **Trigger** | No PM staffing plan or rate schedule available |
| **Evidence** | Typical range 3-5%; 4% selected as mid-point |
| **Impacted WBS/CBS** | PM (Project Management) |
| **Estimate Impact** | $240,000 CAD PM allowance |
| **Override Path** | Provide PM staffing plan with rates |

---

## D-007: Main Building Area Estimate

| Field | Value |
|-------|-------|
| **Decision ID** | D-007 |
| **Decision** | Estimate main building area at 15,000 SF |
| **Trigger** | No explicit building area stated in RFP; functional program has flexible room sizes |
| **Evidence** | Addendum 03 section 1.21 provides room size ranges; combined Fire Hall + Public Works facility typically 12,000-18,000 SF; selected mid-range |
| **Impacted WBS/CBS** | CD (Construction Directs - Main Building) |
| **Estimate Impact** | $5,250,000 CAD at $350/SF benchmark |
| **Override Path** | Provide design concept with actual area takeoff |

---

## D-008: Unit Cost Benchmark Selection

| Field | Value |
|-------|-------|
| **Decision ID** | D-008 |
| **Decision** | Use $350/SF for main building, $100/SF for cold storage |
| **Trigger** | No local cost data or historical comparable projects available |
| **Evidence** | Alberta institutional/industrial construction benchmarks; main building has complex program (fire apparatus, public works operations); cold storage is simple unheated structure |
| **Impacted WBS/CBS** | CD (Construction Directs) |
| **Estimate Impact** | Major cost driver - $5,250,000 + $600,000 = $5,850,000 building construction |
| **Override Path** | Provide regional cost data, RSMeans data, or comparable project costs |

---

## D-009: Tax Treatment

| Field | Value |
|-------|-------|
| **Decision ID** | D-009 |
| **Decision** | Show GST (5%) separately per RFP requirement; no PST in Alberta |
| **Trigger** | RFP Section 4.3 requires "taxes shown separately" |
| **Evidence** | RFP Section 4.3 (page 13); Alberta has no provincial sales tax; GST rate confirmed at 5% |
| **Impacted WBS/CBS** | TAX (shown separately, not in line items) |
| **Estimate Impact** | ~$539,000 GST on total |
| **Override Path** | Confirm current GST rate at time of submission |

---

## D-010: Option 4 Monitoring Fee Treatment

| Field | Value |
|-------|-------|
| **Decision ID** | D-010 |
| **Decision** | Exclude monthly monitoring fee from Schedule A Line 1-5; include installation cost only |
| **Trigger** | Guidance document Conflict-02 identifies ambiguity between Schedule A and Schedule B treatment |
| **Evidence** | Guidance.md Conflict-02 resolution: "Schedule A line 1-5 reflects installation cost only (one-time capital cost)" |
| **Impacted WBS/CBS** | CD (Option 4 line) |
| **Estimate Impact** | Monitoring fee excluded from capital cost; operational cost to be documented in Schedule B only |
| **Override Path** | Seek RFP Authority clarification if needed |

---

## D-011: Service Tie-In Treatment

| Field | Value |
|-------|-------|
| **Decision ID** | D-011 |
| **Decision** | Use cash allowance approach for service tie-ins |
| **Trigger** | Addendum 03 section 1.7 permits allowance approach; utility locations/requirements unknown |
| **Evidence** | Addendum 03 section 1.7 (page 3): "A cash allowance will be considered allowable for the service tie-in costs" |
| **Impacted WBS/CBS** | CD (Service Tie-Ins line) |
| **Estimate Impact** | $150,000 CAD allowance (risk transferred to Owner if actual costs vary) |
| **Override Path** | Provide utility company cost estimates or use firm pricing if confident |

---

## Decision Summary

| ID | Decision | Impact Level |
|----|----------|--------------|
| D-001 | Currency = CAD | LOW |
| D-002 | Allowance method | HIGH |
| D-003 | Contingency = 15% | MEDIUM |
| D-004 | Indirects = 8% | MEDIUM |
| D-005 | E&D = 8% | MEDIUM |
| D-006 | PM = 4% | LOW |
| D-007 | Main building = 15,000 SF | HIGH |
| D-008 | Unit costs = $350/$100 per SF | HIGH |
| D-009 | GST = 5% shown separately | LOW |
| D-010 | Monitoring fee excluded | LOW |
| D-011 | Service tie-in allowance | MEDIUM |

---

*Total Decisions: 11*
