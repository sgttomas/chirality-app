# Decision Log: DEL-07-02 Key Team Members and Resumes

**Snapshot ID:** EST_DEL-07-02_2026-02-04_1323

---

## Decision Register

### D-001: Currency Selection
**Decision Statement:** Use CAD (Canadian Dollars) as estimate currency

**Trigger:** Task brief specified CAD; needed to confirm currency basis

**Evidence:**
- Task brief explicitly stated "Currency: CAD"
- Project located in Alberta, Canada
- RFP issued by Town of Penhold (Canadian municipality)
- Decomposition Section 1 references Alberta jurisdiction

**Impacted WBS/CBS:** All line items

**Estimate Impact:** None - currency was specified in brief

**How to Override:** Provide different currency specification in task brief or _CONFIG.md

---

### D-002: Pricing Method Selection
**Decision Statement:** Use ALLOWANCE method for all line items due to absence of rate tables or quotes

**Trigger:** No rate tables in _RateTables/ directory; no vendor quotes available for professional services

**Evidence:**
- Checked /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Estimates/_RateTables/ - empty directory
- No external quotes obtained (professional services work)
- DEL-07-02 is internal proposal preparation, not external procurement

**Impacted WBS/CBS:** All CBS categories (E, PM, CI)

**Estimate Impact:** HIGH - 100% ALLOWANCE pricing increases uncertainty; higher contingency applied

**How to Override:** Provide rate tables in _RateTables/ directory with professional labor rates (CAD/hr by role)

---

### D-003: Key Team Member Count
**Decision Statement:** Estimate based on 10 key team members (midpoint estimate)

**Trigger:** Datasheet.md Section 2.5 lists team size as TBD; range of 9-13 members identified

**Evidence:**
- Datasheet.md Section 2.5: 9 typical roles listed (PM, Architect, Structural, Mechanical, Electrical, Civil, Construction Manager, Superintendent, Commissioning)
- Datasheet.md Section 2.5: 4 potential additional roles (Landscape Architect, Environmental Consultant, Interior Designer, Geotechnical Engineer)
- Actual team composition not finalized (TBD status)

**Impacted WBS/CBS:** E (primary impact on labor hours)

**Estimate Impact:** MEDIUM - +/- 30% variation in labor hours possible depending on final team size

**How to Override:** Finalize key team member count in Datasheet.md Section 2.5 (resolve TBD B-003)

---

### D-004: Contingency Rate Selection
**Decision Statement:** Apply 20% contingency on base estimate

**Trigger:** Standard contingency method (PCT_BY_BUCKET) required; need to select appropriate rate

**Evidence:**
- 100% of line items priced by ALLOWANCE (no quotes or rate tables)
- Key scope parameter (team size) is TBD
- Resume content gathering effort is variable (personnel responsiveness)
- Standard practice for ALLOWANCE-heavy estimates: 15-25% contingency

**Impacted WBS/CBS:** CONT category

**Estimate Impact:** CAD 1,805 added to base estimate

**How to Override:**
- Provide rate tables to convert ALLOWANCE items to RATE_TABLE pricing (reduces contingency)
- Finalize team size to remove quantity uncertainty
- Specify alternative contingency method/rate in _CONFIG.md

---

### D-005: Labor Rate Selection
**Decision Statement:** Apply standard professional labor rates as allowances

**Trigger:** No rate tables available; need labor rates for hour-based estimates

**Evidence:**
- No rate tables in _RateTables/ directory
- Rates derived from industry-typical professional services rates for Alberta market
- Rates applied:
  - Proposal Manager: CAD 150/hr
  - HR/Admin: CAD 100/hr
  - QA Reviewer: CAD 125/hr
  - Technical Lead: CAD 175/hr

**Impacted WBS/CBS:** E, PM

**Estimate Impact:** HIGH - rates are assumptions; actual firm rates may differ significantly

**How to Override:** Provide firm-specific labor rate table in _RateTables/ directory

---

### D-006: CBS Category Assignment
**Decision Statement:** Assign DEL-07-02 to Engineering & Design (E) as primary CBS, with Project Management (PM) and Construction Indirects (CI) as supporting categories

**Trigger:** Need to map deliverable to CBS for cost categorization

**Evidence:**
- DEL-07-02 is a qualifications document (proposal management discipline)
- Proposal preparation is pre-contract professional services
- Primary work is document preparation (E category)
- Technical Lead review is PM-type effort
- Coordination overhead is indirect (CI category)

**Impacted WBS/CBS:** E, PM, CI

**Estimate Impact:** None - categorization only; totals unchanged

**How to Override:** Specify alternative CBS mapping in _CONFIG.md or task brief

---

**End of Decision Log**
