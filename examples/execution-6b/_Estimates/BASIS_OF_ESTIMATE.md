# Basis of Estimate (BOE) — Penhold Public Services Building
## Proposal Production Cost Strategy Document for ESTIMATING Runs

**Project:** Town of Penhold — Public Services Building (PSB)
**Decomposition:** `Penhold_PSB_Project_Decomposition_v2.md` (Proposal Response Decomposition)
**Currency:** CAD
**Base Year:** 2024
**Prepared:** 2026-02-18
**Status:** DRAFT — Pending human review and approval

---

## 1. Purpose

This document is the **human-authored Basis of Estimate** that governs all ESTIMATING agent runs for the Penhold PSB project under the **proposal-response decomposition** (execution-6b). It establishes:

- The estimation strategy (per-deliverable runs with aggregation)
- Per-deliverable `BASIS_OF_ESTIMATE` and substance classification
- Dependency-informed estimation ordering (which deliverables to estimate first)
- Cost ownership rules to prevent double-counting across deliverables
- A complete register of missing PRICE_SOURCES that must be assembled before meaningful estimates can be produced
- Aggregation strategy for rolling up deliverable-level estimates to package and project totals

### Critical distinction: proposal-response structure

This decomposition is organized as a **proposal-response structure** (10 packages aligned to RFP evaluation sections, 38 deliverables representing proposal documents), NOT a physical-scope construction decomposition. This means:

- **Most deliverables (33 of 38) are proposal documents** — their cost is professional hours to write, draw, and coordinate
- **The estimation subject for most deliverables is proposal production cost**, not construction cost
- **DEL-01-04 (Schedule A) and DEL-01-05 (Schedule B) are the exceptions** — these deliverables EMBED the actual construction pricing that the proposal must contain
- The construction pricing within Schedule A/B must be sourced from an independent construction pricing exercise using construction-focused methods (PARAMETRIC, RATE_TABLE, QUOTE, ALLOWANCE)

This document is **not** an estimate. It is the strategy input that makes estimates producible, auditable, and free of structural double-counting.

---

## 2. Project Context

| Field | Value |
|-------|-------|
| Delivery model | Design-Build (CCDC 14-2013) |
| Owner | Town of Penhold, Alberta |
| Scope | Integrated Public Services Building (Fire + Public Works), Cold Storage Building (60'x100'), Site/Civil Works, Optional Items |
| Decomposition type | **Proposal response** (packages = RFP evaluation sections; deliverables = proposal documents) |
| Packages | 10 (PKG-001 through PKG-010) |
| Deliverables | 38 |
| Scope items | 32 |
| Currency | CAD |
| Base year | 2024 |
| Decomposition source | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` |
| Dependency evidence | `Dependencies.csv` per deliverable (40 files; DEPENDENCIES pass completed) |

### Key project decisions affecting estimating

| DecisionID | Decision | Estimating Impact |
|------------|----------|-------------------|
| DEC-010 | Intent to Propose (App C) will not be submitted | No cost for App C preparation |
| DEC-011 | Insurance = CCIP (Contractor Controlled) | CCIP costs must be included in proposal pricing; premium estimate needed for Schedule A/B |
| DEC-012 | FF&E = $20,000 cash allowance (Additional Option 6) | Fixed allowance on Schedule A line 1-7; no estimating beyond recording |
| DEC-013 | No additional geotechnical investigation | No cost for additional geotech; existing 2021 report is basis for all foundation/site narratives |

### Evaluation scoring context (affects effort allocation)

| Evaluation Category | Points | Primary Packages | Effort Implication |
|---------------------|--------|------------------|--------------------|
| Proposed Conceptual Design | 20 | PKG-002 | Highest technical weight — invest heavily in design hours |
| Building Durability / Maintenance | 15 | PKG-005 | Second-highest — needs strong discipline narratives |
| Project Team & Firms | 15 | PKG-001 | Moderate effort — resume assembly + firm profile |
| Proposal Price | 35 | PKG-001 | Highest overall — Schedule A/B must be defensible |
| Design Brief | 5 | PKG-003 | Lower weight but mandatory 5-discipline coverage |
| Delivery Plan | 3+2 | PKG-006, PKG-009 | Lower weight; methodology + schedule |
| Construction Methodology | 3 | PKG-007 | Lower weight |
| Commissioning/Closeout | 2 | PKG-008 | Lowest weight |

---

## 3. Estimation Strategy

### 3.1 Run granularity: Per-deliverable

ESTIMATING will be run **once per deliverable** (38 runs). Results are aggregated by AGGREGATION into package-level and project-level totals.

**Rationale:**
- Per-deliverable runs align with the decomposition's "deliverable = unit of production" model
- Each deliverable has its own Dependencies.csv, enabling deliverable-specific blocker detection
- Different deliverables within the same package require different effort levels (e.g., PKG-002 drawings vs narratives)
- Per-deliverable snapshots are independently auditable and rerunnable without disturbing others
- AGGREGATION handles rollup, so no information is lost

### 3.2 Dual cost nature of this decomposition

| Cost Type | Deliverables | Treatment |
|-----------|-------------|-----------|
| **Proposal production costs** (professional hours to produce documents) | All 38 deliverables | RATE_TABLE: hours × rates per role |
| **Construction pricing content** (the actual prices that go INTO the proposal) | DEL-01-04 (Schedule A), DEL-01-05 (Schedule B) | MIXED: production hours (RATE_TABLE) + embedded construction pricing (independent construction pricing exercise using PARAMETRIC/RATE_TABLE/QUOTE methods) |

**CRITICAL:** The proposal production cost of DEL-01-04/05 (hours to FILL IN the pricing forms) is separate from the construction pricing CONTENT of those forms. Both must be estimated, but they are fundamentally different cost types:
- **Production cost of Schedule A/B** = estimator hours + review cycles + QA ≈ RATE_TABLE
- **Content of Schedule A/B** = actual construction pricing (base + 6 options) ≈ requires construction-level estimating methods (PARAMETRIC, RATE_TABLE, QUOTE, or ALLOWANCE)

### 3.3 Separation of proposal production cost vs construction pricing

| Classification | Treatment |
|----------------|-----------|
| **Proposal production costs** (all 38 deliverables) | Estimated per this BOE; rolled up to total proposal production cost |
| **Construction pricing within Schedule A/B** | Sourced from an independent construction pricing exercise; carried as a separate line in DEL-01-04/05 ESTIMATING runs |
| **CCIP insurance premium** | Percentage of construction contract value; dependent on Schedule A base price |
| **Bonding costs** | Percentage of contract price; dependent on Schedule A base price |

### 3.4 Common run parameters (all deliverables)

```
CURRENCY: CAD
RUN_ROOT: {EXECUTION_ROOT}
ESTIMATES_ROOT: {EXECUTION_ROOT}/_Estimates/
DECOMPOSITION_PATH: {EXECUTION_ROOT}/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md
DEPENDENCY_SOURCES: AUTO
UPDATE_LATEST_POINTER: FALSE
ROUNDING: DOLLAR
EXCLUSIONS:
  - "{RUN_ROOT}/_Estimates/**"
  - "{RUN_ROOT}/_Aggregation/**"
  - "{RUN_ROOT}/_Reconciliation/**"
  - "{RUN_ROOT}/_Archive/**"
```

---

## 4. Per-Deliverable Estimation Plan

### Estimation Tier Legend

| Tier | Meaning | Implication |
|------|---------|-------------|
| **T0** | No upstream production dependencies; can estimate independently | Can run immediately once PRICE_SOURCES assembled |
| **T1** | Foundational; its outputs inform how much effort downstream deliverables require | Run early; outputs shape effort estimates for T2+ |
| **T2** | Depends on T1 design concept outputs to scope narrative content | Run after T1 concept deliverables are characterized |
| **T3** | Depends on T2 narrative scope or cross-package coordination | Run after T2 outputs are available |
| **T4** | Depends on substantial completion of all technical content | Run last; all technical deliverables must be characterized |

---

### PKG-001 — Proposal Compliance, Commercial & Team Qualifications

**Package estimating character:** Mixed — 9 deliverables spanning compliance checklists, formal submission documents, financial forms, pricing narratives, firm qualifications, and team resumes. Most are administrative/professional hours. DEL-01-04/05 are uniquely complex because they embed construction pricing. DEL-01-02 depends on ALL other packages (final assembly).

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-01-01 | Compliance Matrix & Checklist | T0 | RATE_TABLE | STRICT | FALSE | Administrative | Proposal coordinator hours; compliance review against all RFP sections; addenda integration checklist |
| DEL-01-02 | Formal Submission Package (Final PDF Assembly) | T4 | RATE_TABLE | STRICT | FALSE | Administrative + Production | Proposal coordinator hours; PDF assembly; submission QA; revision control. **MUST BE LAST** — depends on all other packages being complete |
| DEL-01-03 | Bonding & Insurance Evidence | T0 | RATE_TABLE | ALLOW_ALLOWANCE | TRUE | Administrative + Legal | Surety broker coordination hours; CCIP insurance documentation; legal review hours; bond premium (percentage of contract — ALLOWANCE until Schedule A is priced) |
| DEL-01-04 | Schedule A — Pricing Summary | T4 | RATE_TABLE | ALLOW_ALLOWANCE | TRUE | Financial + Construction Pricing | Estimator hours to compile Schedule A form + QA review cycles. **PLUS:** embedded construction pricing content (base price + 6 options) — sourced from an independent construction pricing exercise |
| DEL-01-05 | Schedule B — Cost Breakdown | T4 | RATE_TABLE | ALLOW_ALLOWANCE | TRUE | Financial + Construction Pricing | Estimator hours to complete detailed cost breakdown + QA. **PLUS:** embedded construction pricing detail. **BLOCKS on DEL-01-04** (Schedule A totals must be established first) |
| DEL-01-06 | Pricing Narrative & Assumptions | T4 | RATE_TABLE | STRICT | FALSE | Narrative | PM + estimator hours; documents allowances (site servicing, FF&E $20K), exclusions (pickled sand, no addl geotech), CCIP inclusion, value alternatives. Depends on DEL-01-04/05 pricing being finalized |
| DEL-01-07 | DB Firm Experience Profile | T0 | RATE_TABLE | STRICT | FALSE | Narrative | Proposal writer hours; project summary compilation; reference gathering |
| DEL-01-08 | Key Team Members & Resumes | T0 | RATE_TABLE | STRICT | FALSE | Administrative | HR/proposal coordinator hours; resume formatting (max 2 pages each); availability confirmations |
| DEL-01-09 | Appendix I — Subtrade & Consultant List | T0 | RATE_TABLE | STRICT | FALSE | Administrative | PM hours; subtrade procurement coordination; form completion |

**PKG-001 PRICE_SOURCES needed:**
- [ ] Proposal production staff rate table (proposal coordinator, estimator, PM, legal reviewer — hourly rates, CAD 2024)
- [ ] Surety broker fee/commission structure
- [ ] CCIP insurance premium rate (percentage of construction contract value — TBD until Schedule A base price is established)
- [ ] Bond premium rate (percentage of contract price)
- [ ] Estimated proposal preparation timeline (weeks) — drives duration-dependent coordination costs
- [ ] **For DEL-01-04/05 construction pricing content:** an independent construction pricing exercise (requires a full construction-level PRICE_SOURCES register: structural/mechanical/electrical system rates, earthwork rates, material pricing, vendor quotes, etc.)

**PKG-001 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Compliance checking + addenda integration | DEL-01-01 | DEL-01-02 |
| Final PDF assembly + submission logistics | DEL-01-02 | All others |
| Bond/insurance documentation + premiums | DEL-01-03 | DEL-01-04, DEL-01-05 |
| Construction pricing COMPILATION (estimator hours to fill forms) | DEL-01-04, DEL-01-05 | All others |
| Construction pricing CONTENT (the actual prices) | DEL-01-04 (summary), DEL-01-05 (detail) | All other DELs (their estimates cover PRODUCTION cost only) |
| Pricing narrative + assumptions writing | DEL-01-06 | DEL-01-04, DEL-01-05 |
| Firm profile writing | DEL-01-07 | DEL-01-08 |
| Resume assembly + formatting | DEL-01-08 | DEL-01-07 |
| Subtrade list compilation | DEL-01-09 | DEL-01-07 |

**CRITICAL: DEL-01-04/05 dual-nature estimation**
- The PRODUCTION cost (hours to prepare Schedule A/B) is estimated by this BOE using RATE_TABLE
- The CONTENT (construction pricing) requires construction-level estimating — an independent construction pricing exercise using PARAMETRIC, RATE_TABLE, QUOTE, and/or ALLOWANCE methods as appropriate to each construction scope area
- These two cost types must be separated in the ESTIMATING run output: one line group for production hours, another for the construction pricing content

---

### PKG-002 — Conceptual Design

**Package estimating character:** Highest-effort technical package. 5 discipline deliverables producing the proposal's conceptual design — drawings (architect) and narratives (engineers). All SOW-0009/SOW-0010 requirements distributed across disciplines. Strong handover to PKG-003 (Design Brief depends on concept).

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-02-01 | Architectural Concept Package (Drawings) | T1 | RATE_TABLE | STRICT | FALSE | Design + Drawings | Architect hours (concept development, floor plans, elevations, sections, optional renderings); CAD/BIM production hours; Addendum 03 program integration (16ft doors, 40 lockers, room sizes, 2nd storey option) |
| DEL-02-02 | Civil/Site Concept Plan | T1 | RATE_TABLE | STRICT | FALSE | Design + Drawings | Civil engineer hours; site plan drawing (12-acre site, building placement, parking, circulation, drainage concept, utility connection points, Cold Storage placement); reference to Appendix E site grading |
| DEL-02-03 | Structural Concept Narrative | T1 | RATE_TABLE | STRICT | FALSE | Narrative | Structural engineer hours; foundation approach per existing 2021 geotech; framing system selection; floor slab design (bay sumps); expansion provisions |
| DEL-02-04 | Mechanical Concept Narrative | T1 | RATE_TABLE | STRICT | FALSE | Narrative | Mechanical engineer hours; HVAC system selection; fire bay direct exhaust; PW bay ventilation; plumbing (fill stations, sumps); generator sizing; fire protection approach |
| DEL-02-05 | Electrical/IT Concept Narrative | T1 | RATE_TABLE | STRICT | FALSE | Narrative | Electrical engineer hours; power distribution; LED lighting; generator connection; IT/telecom; access control/security provisions; solar-ready electrical; fire alarm |

**PKG-002 PRICE_SOURCES needed:**
- [ ] Architect hourly rate (principal + project architect + CAD technician — CAD 2024)
- [ ] Civil engineer hourly rate
- [ ] Structural engineer hourly rate
- [ ] Mechanical engineer hourly rate
- [ ] Electrical engineer hourly rate
- [ ] Estimated hours per discipline for concept-level design (varies by discipline; architect highest due to drawings)
- [ ] CAD/BIM software costs if not embedded in hourly rates
- [ ] Rendering/visualization costs if optional 3D renderings are included

**PKG-002 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Architectural concept DRAWINGS (floor plans, elevations, sections) | DEL-02-01 | DEL-02-02 through DEL-02-05 |
| Architectural program integration (room layout, adjacencies, code compliance) | DEL-02-01 | DEL-02-02 through DEL-02-05 |
| Civil/site DRAWINGS and civil concept narrative | DEL-02-02 | DEL-02-01, DEL-02-03 through DEL-02-05 |
| Structural concept NARRATIVE | DEL-02-03 | DEL-02-01 |
| Mechanical concept NARRATIVE | DEL-02-04 | DEL-02-01 |
| Electrical/IT concept NARRATIVE | DEL-02-05 | DEL-02-01 |
| Addendum 03 requirements: doors/lockers/room sizes (architectural) | DEL-02-01 | DEL-02-03, DEL-02-04 |
| Addendum 03 requirements: sumps/slab (structural) | DEL-02-03 | DEL-02-01 |
| Addendum 03 requirements: exhaust/generator/fill stations (mechanical) | DEL-02-04 | DEL-02-01, DEL-02-05 |
| Addendum 03 requirements: solar electrical (electrical) | DEL-02-05 | DEL-02-01 |
| Addendum 03 requirements: site area (civil) | DEL-02-02 | DEL-02-01 |
| Cross-discipline COORDINATION hours (architect leading discipline integration) | DEL-02-01 | DEL-02-02 through DEL-02-05 |

**CRITICAL: SOW-0009/SOW-0010 multi-mapping (double-counting prevention)**
- SOW-0009 (conceptual design) and SOW-0010 (program clarifications) are both mapped to ALL 5 PKG-002 deliverables
- This does NOT mean each deliverable carries the full SOW scope — each discipline carries ONLY its portion:
  - DEL-02-01 (Architect): drawings + architectural program integration + coordination leadership
  - DEL-02-02 (Civil): site plan + civil narrative
  - DEL-02-03 (Structural): structural narrative only
  - DEL-02-04 (Mechanical): mechanical narrative only
  - DEL-02-05 (Electrical): electrical/IT narrative only
- Do NOT estimate "full concept design hours" in each deliverable — estimate only that discipline's contribution

---

### PKG-003 — Design Brief

**Package estimating character:** 6 narrative deliverables — one per RFP-required discipline sub-brief plus a cross-cutting accessibility/adaptability narrative. All depend on PKG-002 concept being sufficiently developed (briefs describe WHY the concept works). Moderate effort per deliverable.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-03-01 | Architectural Design Brief | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Architect hours; site plan rationale, architectural plan rationale, exterior elevation design intent, interior finishes approach, code compliance narrative |
| DEL-03-02 | Civil Design Brief | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Civil engineer hours; parking rationale, access, drainage, stormwater, grading, utility connections, site servicing (cash allowance notation) |
| DEL-03-03 | Structural Design Brief | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Structural engineer hours; system selection rationale, expansion provisions, foundation approach, load path narrative |
| DEL-03-04 | Mechanical Design Brief | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Mechanical engineer hours; systems selection rationale, heating/cooling, ventilation by zone, plumbing, fire protection, generator philosophy |
| DEL-03-05 | Electrical/IT Design Brief | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Electrical engineer hours; power distribution philosophy, lighting approach, controls, telecom/data, access control/security design approach, fire alarm, solar-readiness |
| DEL-03-06 | Accessibility & Adaptability Narrative | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Architect hours (coordinating structural/mechanical input); accessibility per Alberta Building Code; adaptability/expansion provisions |

**PKG-003 PRICE_SOURCES needed:**
- [ ] Same discipline hourly rates as PKG-002 (architect, civil, structural, mechanical, electrical)
- [ ] Estimated hours per discipline for design brief writing (generally lower than concept production since briefs are narrative descriptions of already-developed concepts)

**PKG-003 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Architectural design brief narrative | DEL-03-01 | DEL-03-06 |
| Civil design brief narrative | DEL-03-02 | DEL-02-02 (concept is separate) |
| Structural design brief + expansion provisions narrative | DEL-03-03 | DEL-02-03 (concept is separate) |
| Mechanical design brief narrative | DEL-03-04 | DEL-02-04 (concept is separate) |
| Electrical/IT design brief narrative | DEL-03-05 | DEL-02-05 (concept is separate) |
| Accessibility narrative | DEL-03-06 | DEL-03-01 |
| Adaptability/expansion narrative | DEL-03-06 | DEL-03-03 (structural expansion provisions are in DEL-03-03; overall adaptability narrative is DEL-03-06) |

**CRITICAL: SOW-0011 multi-mapping (double-counting prevention)**
- SOW-0011 (Design Brief — 5 sub-briefs) is mapped to DEL-03-01 through DEL-03-05
- Each deliverable covers ONLY its discipline sub-brief, not the full Design Brief
- DEL-03-06 covers the cross-cutting accessibility (SOW-0015) and adaptability (SOW-0014) narratives that are NOT sub-briefs but are Design Brief-adjacent content

**CRITICAL: PKG-003 vs PKG-002 boundary (concept vs brief)**
- PKG-002 = WHAT the concept is (drawings, specifications, system selections)
- PKG-003 = WHY the concept works (rationale, design intent, compliance narrative)
- The HOURS to produce a design brief assume the concept is already developed — brief writing is a follow-on activity, not a standalone design exercise
- Do NOT double-count design hours: concept development hours are in PKG-002; brief writing hours are in PKG-003

---

### PKG-004 — Sustainability & Energy

**Package estimating character:** 3 narrative deliverables — building envelope/energy, mechanical energy/solar, electrical energy/lighting. Tightly coupled internally (bidirectional interfaces between all 3). All depend on PKG-002 concept for building envelope and systems definitions.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-04-01 | Building Envelope & Energy Strategy | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Architect/building science hours; thermal performance targets, air barrier continuity, thermal bridging, energy code compliance, overall energy philosophy |
| DEL-04-02 | Mechanical Energy & Solar Readiness | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Mechanical engineer hours; high-efficiency equipment, heat recovery, ventilation optimization, DHW efficiency, solar-ready provisions, energy metering |
| DEL-04-03 | Electrical Energy Efficiency | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Electrical engineer hours; LED lighting controls, motor efficiency, solar-ready electrical provisions, metering/sub-metering strategy |

**PKG-004 PRICE_SOURCES needed:**
- [ ] Architect/building science consultant hourly rate
- [ ] Same mechanical and electrical engineer rates as PKG-002/003
- [ ] Estimated hours per discipline for sustainability narrative writing

**PKG-004 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Building envelope energy strategy narrative | DEL-04-01 | DEL-03-01 (design brief is separate), DEL-05-01 (durability is separate) |
| Mechanical energy efficiency narrative | DEL-04-02 | DEL-03-04 (mech brief is separate), DEL-05-03 (mech maintainability is separate) |
| Electrical energy efficiency narrative | DEL-04-03 | DEL-03-05 (elec brief is separate), DEL-05-04 (elec maintainability is separate) |
| Solar-ready STRUCTURAL provisions | DEL-04-02 (describes need) | DEL-02-03 (structural concept owns the design) |
| Solar-ready ELECTRICAL provisions | DEL-04-03 | DEL-02-05 (concept owns design), DEL-04-02 (mechanical solar is separate) |

**CRITICAL: SOW-0012 multi-mapping (double-counting prevention)**
- SOW-0012 (sustainability/energy narrative) is mapped to all 3 PKG-004 deliverables
- Each deliverable covers ONLY its discipline portion of the sustainability story
- Cross-discipline COORDINATION hours for sustainability belong in DEL-04-01 (architect/building science leads)

---

### PKG-005 — Building Durability & Maintenance

**Package estimating character:** 4 narrative deliverables by discipline. Second-highest technical evaluation weight (15 pts). All depend on PKG-002 concept for materials/systems being described. Deep cross-discipline coordination required.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-05-01 | Architectural Durability & Maintenance | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Architect hours; cladding, roofing, interior finishes lifecycle, flooring by zone, doors/hardware durability, moisture management |
| DEL-05-02 | Structural Durability & Maintenance | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Structural engineer hours; corrosion protection, concrete durability (freeze-thaw, chloride), foundation longevity, slab durability, inspection accessibility |
| DEL-05-03 | Mechanical Maintainability | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Mechanical engineer hours; equipment access, serviceability, maintenance schedule framework, lifecycle cost considerations, ventilation filter access |
| DEL-05-04 | Electrical Maintainability | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Electrical engineer hours; panel accessibility, lighting fixture replacement, control system serviceability, IT infrastructure maintainability, security system lifecycle |

**PKG-005 PRICE_SOURCES needed:**
- [ ] Same discipline hourly rates as PKG-002/003/004
- [ ] Estimated hours per discipline for durability/maintenance narrative writing

**PKG-005 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Architectural durability narrative | DEL-05-01 | DEL-04-01 (energy is separate), DEL-03-01 (brief is separate) |
| Structural durability narrative | DEL-05-02 | DEL-03-03 (brief is separate) |
| Mechanical maintainability narrative | DEL-05-03 | DEL-04-02 (energy is separate), DEL-03-04 (brief is separate) |
| Electrical maintainability narrative | DEL-05-04 | DEL-04-03 (energy is separate), DEL-03-05 (brief is separate) |

**CRITICAL: SOW-0013 multi-mapping (double-counting prevention)**
- SOW-0013 (durability/maintenance narrative) is mapped to all 4 PKG-005 deliverables
- Each deliverable covers ONLY its discipline portion

**CRITICAL: PKG-003/004/005 boundary (brief vs sustainability vs durability)**
- These three packages cover the SAME building systems from three different perspectives:
  - PKG-003 = WHY we selected these systems (design rationale)
  - PKG-004 = HOW these systems achieve energy efficiency (sustainability)
  - PKG-005 = HOW these systems achieve longevity (durability)
- The same engineer may write all three narratives for their discipline, but the HOURS for each are separate production efforts
- Do NOT assume "the engineer already knows the building from PKG-003, so PKG-004/005 takes no time" — each narrative requires distinct research, analysis, and writing

---

### PKG-006 — Delivery Plan (Design Methodology + Documents Plan)

**Package estimating character:** 2 narrative deliverables — design methodology and detailed design/construction documents plan. Moderate effort. Bidirectional dependency between the two (DEL-06-01 ↔ DEL-06-02).

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-06-01 | Design Methodology Narrative | T0 | RATE_TABLE | STRICT | FALSE | Narrative | Design manager/PM hours; design approach, stakeholder engagement, Owner review process, design phase sequencing, permitting, innovation/value approach |
| DEL-06-02 | Detailed Design & Construction Documents Plan | T0 | RATE_TABLE | STRICT | FALSE | Narrative | Design manager hours; 5 design submission milestones, discipline deliverables list, coordination approach, QA/QC checkpoints, Owner review cycles |

**PKG-006 PRICE_SOURCES needed:**
- [ ] Design manager/PM hourly rate
- [ ] Estimated hours for methodology and documents plan writing

**PKG-006 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Design methodology narrative (approach, stakeholder, innovation) | DEL-06-01 | DEL-06-02 |
| Design documents plan (milestones, coordination, QA/QC) | DEL-06-02 | DEL-06-01 |
| Design QC NARRATIVE | DEL-06-02 | DEL-07-05 (construction QC is in PKG-007) |

---

### PKG-007 — Construction Methodology & Administration

**Package estimating character:** 5 narrative deliverables covering construction approach. Internal hub pattern with DEL-07-01 (methodology) as foundation. Moderate effort per deliverable.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-07-01 | Construction Methodology Narrative | T0 | RATE_TABLE | STRICT | FALSE | Narrative | Construction manager hours; H&S plan, staging, permits/inspections, budget control, schedule control, communications, QA/QC framework |
| DEL-07-02 | Construction Administration Narrative | T3 | RATE_TABLE | STRICT | FALSE | Narrative | Construction manager hours; supervision approach, document management, shop drawings, cleaning, transport/storage, site services. Depends on DEL-07-01 methodology framework |
| DEL-07-03 | Subconsultant Approach Narrative | T3 | RATE_TABLE | STRICT | FALSE | Narrative | PM/construction manager hours; discipline listing, management approach, geotech review protocol (existing 2021 report only). Depends on DEL-07-01 |
| DEL-07-04 | Meetings & Reporting Narrative | T3 | RATE_TABLE | STRICT | FALSE | Narrative | PM/construction manager hours; meeting structure, frequency, agenda/minutes, progress reporting. Depends on DEL-07-01 |
| DEL-07-05 | Quality Management Narrative | T3 | RATE_TABLE | STRICT | FALSE | Narrative | PM/quality lead hours; design QC, construction QC, commissioning QC, documentation QC, NMS recommendation. Depends on DEL-07-01 |

**PKG-007 PRICE_SOURCES needed:**
- [ ] Construction manager hourly rate
- [ ] PM hourly rate (may be same person as other packages)
- [ ] Estimated hours per narrative section

**PKG-007 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Construction methodology framework (H&S, staging, permits, budget/schedule control) | DEL-07-01 | DEL-07-02 through DEL-07-05 |
| Construction phase administration (supervision, documents, shop drawings, cleaning) | DEL-07-02 | DEL-07-01 |
| Subconsultant management approach | DEL-07-03 | DEL-01-09 (Appendix I is a LIST; DEL-07-03 is the APPROACH narrative) |
| Meeting/reporting protocol | DEL-07-04 | DEL-07-01 (methodology mentions communications; details are in DEL-07-04) |
| Quality management narrative | DEL-07-05 | DEL-06-02 (design QC plan is in PKG-006; construction QC is in DEL-07-05) |

---

### PKG-008 — Commissioning, Closeout & Warranty

**Package estimating character:** 3 narrative deliverables in a vertical flow (DEL-08-01 → DEL-08-02 → DEL-08-03). Lowest evaluation weight (2 pts) but mandatory coverage.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-08-01 | Commissioning, Training & Closeout Narrative | T3 | RATE_TABLE | STRICT | FALSE | Narrative | Commissioning lead/PM hours; commissioning approach, handover process, training documentation, O&M manuals, as-built drawings |
| DEL-08-02 | Deficiencies Management Narrative | T3 | RATE_TABLE | STRICT | FALSE | Narrative | PM/quality lead hours; punch lists, formal review, monetary valuation, holdback, 12-month warranty review, Owner 6-week deficiency right. Depends on DEL-08-01 |
| DEL-08-03 | Warranty Requirements Narrative | T3 | RATE_TABLE | STRICT | FALSE | Narrative | PM hours; 12-month warranty, manufacturer warranties, SC54-SC55 provisions. Depends on DEL-08-01 |

**PKG-008 PRICE_SOURCES needed:**
- [ ] Commissioning lead hourly rate
- [ ] PM hourly rate
- [ ] Estimated hours per narrative section

**PKG-008 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Commissioning approach + training + closeout narrative | DEL-08-01 | DEL-08-02, DEL-08-03 |
| Deficiencies management process narrative | DEL-08-02 | DEL-08-01 |
| Warranty provisions narrative | DEL-08-03 | DEL-08-01, DEL-08-02 |

---

### PKG-009 — Schedule & Milestones

**Package estimating character:** Single high-effort deliverable requiring Gantt chart production. Depends on multiple upstream packages for activity definitions and sequencing.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-09-01 | Detailed Project Schedule | T3 | RATE_TABLE | STRICT | FALSE | Schedule + Narrative | Scheduler/PM hours; Gantt chart production; critical path analysis; schedule assumptions; design-through-closeout timeline. Scheduling software costs if applicable |

**PKG-009 PRICE_SOURCES needed:**
- [ ] Scheduler hourly rate
- [ ] Scheduling software costs (if not embedded in hourly rate)
- [ ] Estimated hours for schedule development (higher than typical narrative — requires Gantt production)

**PKG-009 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Gantt chart + critical path + assumptions | DEL-09-01 | DEL-07-01 (construction schedule control narrative is separate) |
| Schedule milestone dates | DEL-09-01 | DEL-06-02 (design submission milestones are defined in PKG-006; schedule PLACES them in time) |

---

### PKG-010 — Due Diligence & Risk Management

**Package estimating character:** 2 deliverables — risk register and site conditions summary. DEL-10-02 is a critical feeder hub (its outputs inform many other packages). These can start early because they are based on reference documents, not on design production.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-10-01 | Risk Register & Mitigation Plan | T0 | RATE_TABLE | STRICT | FALSE | Register + Narrative | PM + technical lead hours; risk identification, likelihood/impact assessment, mitigation strategies; grounded in RFP/addenda/reference reports |
| DEL-10-02 | Site Conditions & Due Diligence Summary | T0 | RATE_TABLE | STRICT | FALSE | Narrative | PM + technical lead hours; geotech summary, wetland assessment, environmental assessment, flood zone analysis, site grading review, survey approach (files after award) |

**PKG-010 PRICE_SOURCES needed:**
- [ ] PM hourly rate
- [ ] Technical lead hourly rates (for review/input)
- [ ] Estimated hours for risk register compilation and site conditions narrative

**PKG-010 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Risk register (all categories) | DEL-10-01 | DEL-01-06 (pricing ASSUMPTIONS are in PKG-001; RISKS are in PKG-010) |
| Site conditions summary | DEL-10-02 | DEL-02-02 (civil concept references site conditions; summary is in PKG-010) |
| Geotech implications for design | DEL-10-02 (summary) | DEL-02-03 (structural concept uses geotech for DESIGN; PKG-010 SUMMARIZES it) |
| Survey approach/assumptions | DEL-10-02 | DEL-02-02 (civil concept USES survey data; PKG-010 documents the APPROACH) |

---

## 5. Dependency-Informed Run Sequence

Runs should be executed in tier order. Within a tier, runs are independent and may be parallelized.

### Sequence

```
TIER 0 (run immediately; no production dependencies):
  DEL-01-01, DEL-01-03, DEL-01-07, DEL-01-08, DEL-01-09
  DEL-06-01, DEL-06-02
  DEL-07-01
  DEL-10-01, DEL-10-02
  [10 parallel runs]

TIER 1 (foundational design — run next; outputs shape all technical narratives):
  DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-02-05
  [5 parallel runs]

TIER 2 (depends on Tier 1 concept outputs for narrative scope):
  DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-03-05, DEL-03-06
  DEL-04-01, DEL-04-02, DEL-04-03
  DEL-05-01, DEL-05-02, DEL-05-03, DEL-05-04
  [13 parallel runs]

TIER 3 (depends on Tier 2 narratives or internal sequencing):
  DEL-07-02, DEL-07-03, DEL-07-04, DEL-07-05
  DEL-08-01, DEL-08-02, DEL-08-03
  DEL-09-01
  [8 parallel runs]

TIER 4 (depends on substantial completion of all technical content):
  DEL-01-04 (Schedule A — requires all technical packages + construction pricing)
  DEL-01-05 (Schedule B — BLOCKS on DEL-01-04)
  DEL-01-06 (Pricing Narrative — depends on DEL-01-04/05)
  DEL-01-02 (Final Assembly — depends on ALL other deliverables)
  [4 sequential runs: DEL-01-04 → DEL-01-05 → DEL-01-06 → DEL-01-02]

Total: 38 ESTIMATING runs across 5 tiers (2 unavoidable sequential chains in T4)
```

### Tier dependencies (what must be resolved before next tier runs)

| Before Tier | Must Have |
|-------------|----------|
| T0 → T1 | PRICE_SOURCES for design discipline hourly rates; reference documents reviewed (DEL-10-02) |
| T1 → T2 | PKG-002 concept outputs characterized (building footprint, system selections, site layout); these define the SCOPE of narrative writing in T2 |
| T2 → T3 | PKG-003/004/005 narrative scope characterized; DEL-07-01 methodology framework established |
| T3 → T4 | All technical narrative deliverables complete; DEL-09-01 schedule available; construction pricing from independent exercise available |
| T4 internal | DEL-01-04 → DEL-01-05 → DEL-01-06 → DEL-01-02 (strict sequential chain) |

### External gates that block meaningful estimating

| Gate | Blocks | Status | Impact |
|------|--------|--------|--------|
| Construction estimates for Schedule A/B content | DEL-01-04, DEL-01-05 construction pricing content | TBD | Without construction pricing, Schedule A/B cannot be completed; proposal production hours can still be estimated |
| CCIP insurance premium quotation | DEL-01-03, DEL-01-05 (Schedule B insurance line) | TBD | If unavailable, carry as percentage allowance |
| Bond premium quotation | DEL-01-03, DEL-01-05 (Schedule B bonding line) | TBD | If unavailable, carry as percentage of contract price (standard industry rates) |
| Subtrade availability confirmations | DEL-01-09 | TBD | If pending, may require follow-up coordination hours |
| Team member availability confirmations | DEL-01-08 | TBD | If pending, may delay resume compilation |
| Proposal submission timeline confirmation | All | TBD | Compressed timeline increases hours (overtime/parallel effort); extended timeline allows sequential production |

---

## 6. Complete Missing PRICE_SOURCES Register

### Critical (block meaningful estimates for most deliverables)

| ID | Source Needed | Affects | Priority |
|----|--------------|---------|----------|
| PS-01 | Proposal production staff rate table — ALL roles: Architect (principal, project architect, CAD tech), Civil Engineer, Structural Engineer, Mechanical Engineer, Electrical Engineer, PM, Design Manager, Construction Manager, Commissioning Lead, Scheduler, Estimator, Proposal Coordinator, Quality Lead, HR/Admin — hourly rates, CAD 2024 | All 38 deliverables | HIGH |
| PS-02 | Estimated production hours per deliverable per discipline (level-of-effort matrix) | All 38 deliverables | HIGH |
| PS-03 | Proposal preparation timeline (weeks from start to submission) | All deliverables — affects coordination overhead and sequential vs parallel production | HIGH |

### Important (needed for specific deliverables or cost types)

| ID | Source Needed | Affects | Priority |
|----|--------------|---------|----------|
| PS-04 | Construction pricing for Schedule A/B content — independent construction pricing exercise | DEL-01-04, DEL-01-05 | HIGH (for pricing content; production hours can be estimated without this) |
| PS-05 | CCIP insurance premium rate (percentage of construction contract value) | DEL-01-03, DEL-01-05 | MEDIUM |
| PS-06 | Bond premium rate (percentage of contract price; Performance 50% + Labour & Materials 50%) | DEL-01-03, DEL-01-05 | MEDIUM |
| PS-07 | Surety broker fee/commission structure | DEL-01-03 | MEDIUM |
| PS-08 | Legal review hourly rate (for bond/insurance documentation review) | DEL-01-03 | MEDIUM |
| PS-09 | CAD/BIM software costs (if not embedded in discipline hourly rates) | DEL-02-01, DEL-02-02 | LOW |
| PS-10 | Scheduling software costs (if not embedded in scheduler hourly rate) | DEL-09-01 | LOW |
| PS-11 | Optional 3D rendering/visualization costs | DEL-02-01 | LOW (optional) |
| PS-12 | Printing/reproduction costs for proposal PDF (digital submission — minimal) | DEL-01-02 | LOW |

---

## 7. Aggregation Strategy

After all ESTIMATING runs are complete, run AGGREGATION to produce:

### 7.1 Package-level rollups

| Aggregation | Scope | Expected Output |
|-------------|-------|-----------------|
| PKG-001 total | DEL-01-01 through DEL-01-09 | Compliance, Commercial & Team production costs (EXCLUDING construction pricing content in DEL-01-04/05) |
| PKG-001 construction pricing | DEL-01-04, DEL-01-05 (content only) | Construction pricing from independent exercise — reported SEPARATELY |
| PKG-002 total | DEL-02-01 through DEL-02-05 | Conceptual Design production costs |
| PKG-003 total | DEL-03-01 through DEL-03-06 | Design Brief production costs |
| PKG-004 total | DEL-04-01 through DEL-04-03 | Sustainability & Energy production costs |
| PKG-005 total | DEL-05-01 through DEL-05-04 | Durability & Maintenance production costs |
| PKG-006 total | DEL-06-01, DEL-06-02 | Delivery Plan production costs |
| PKG-007 total | DEL-07-01 through DEL-07-05 | Construction Methodology production costs |
| PKG-008 total | DEL-08-01 through DEL-08-03 | Commissioning/Closeout production costs |
| PKG-009 total | DEL-09-01 | Schedule production costs |
| PKG-010 total | DEL-10-01, DEL-10-02 | Due Diligence production costs |

### 7.2 Project-level totals

| Total | Composition |
|-------|-------------|
| **Total Proposal Production Cost** | Sum of all 10 package production cost totals |
| **Construction Pricing Content** (separately reported) | DEL-01-04/05 construction pricing — this is the PROPOSAL PRICE, not a production cost |
| **Grand Total Proposal Effort** | Production cost + construction pricing compilation effort |

### 7.3 Effort matrix (hours by role x package)

AGGREGATION should produce a combined effort matrix showing:
- **Rows:** Role (architect, civil engineer, structural engineer, mechanical engineer, electrical engineer, PM, design manager, construction manager, scheduler, estimator, proposal coordinator, commissioning lead, quality lead, admin)
- **Columns:** Package (PKG-001 through PKG-010)
- **Cells:** Hours per role per package
- **Totals:** Row totals (total hours per role) and column totals (total hours per package)

### 7.4 Evaluation-weight-adjusted view

| Evaluation Category | Points | Total Estimated Hours | Cost | $/Point |
|---------------------|--------|----------------------|------|---------|
| Mandatory Compliance | Pass/Fail | (from PKG-001 compliance DELs) | | N/A |
| Proposed Conceptual Design (20 pts) | 20 | (from PKG-002) | | (cost/20) |
| Design Brief (5 pts) | 5 | (from PKG-003) | | (cost/5) |
| Durability/Maintenance (15 pts) | 15 | (from PKG-005) | | (cost/15) |
| Delivery Plan (3 pts) | 3 | (from PKG-006) | | (cost/3) |
| Construction Methodology (3 pts) | 3 | (from PKG-007) | | (cost/3) |
| Commissioning (2 pts) | 2 | (from PKG-008) | | (cost/2) |
| Schedule (2 pts) | 2 | (from PKG-009) | | (cost/2) |
| Team/Firms (15 pts) | 15 | (from PKG-001 team DELs) | | (cost/15) |
| Proposal Price (35 pts) | 35 | (from PKG-001 pricing DELs) | | (cost/35) |

This view helps optimize effort allocation: investing more hours in high-point categories yields better ROI.

---

## 8. Assumptions and Constraints Log

| ID | Assumption/Constraint | Source | Impact if Wrong |
|----|----------------------|--------|-----------------|
| A-01 | All professional hourly rates are internal DB rates (not external consultant fees unless explicitly stated) | BOE assumption | If external consultants are more expensive, production costs increase proportionally |
| A-02 | Each discipline engineer produces their own concept narrative, design brief, sustainability narrative, and durability narrative — 4 writing tasks per discipline | Decomposition structure (DEC-006 through DEC-009) | If consolidated (one person writes all 4 for their discipline), total hours may be lower due to context familiarity — but each narrative still requires distinct production effort |
| A-03 | Architect leads coordination for PKG-002, PKG-003, PKG-005 — coordination hours are in the architectural deliverable of each package | Decomposition (Owner role assignments) | If coordination is more distributed, hours shift but total should be similar |
| A-04 | DEL-01-04/05 construction pricing content sourced from an independent construction pricing exercise | BOE strategy decision | If construction estimates are not available, DEL-01-04/05 cannot be completed for pricing content — production hours can still be estimated |
| A-05 | Proposal submission is digital only (email PDF < 15MB) — no printing/binding costs | RFP 4.2, 5.3 | If physical copies required, minimal cost impact |
| A-06 | No additional geotechnical investigation — existing 2021 report is sufficient | DEC-013 | No geotech cost in any deliverable; if additional investigation needed later, it's out of scope |
| A-07 | CCIP insurance and bonding premium rates are standard market rates until actual quotes obtained | BOE assumption | Actual premiums may vary; carry as allowance percentages |
| A-08 | Base year 2024; no escalation applied to professional rates | Project direction | If proposal preparation extends beyond 2024, rate escalation may be needed |
| A-09 | All 38 deliverables will be estimated regardless of evaluation weight — even low-weight items get ESTIMATING runs | BOE strategy decision | Ensures complete coverage; low-weight items will naturally have lower production hours |
| A-10 | Intent to Propose (Appendix C) will not be submitted — zero cost | DEC-010 | No impact |

---

## 9. Document Control

| Field | Value |
|-------|-------|
| Document | Basis of Estimate (BOE) — Proposal Production |
| Version | DRAFT v0.1 |
| Prepared by | [Human operator] with HELP_HUMAN agent support |
| Date | 2026-02-18 |
| Status | DRAFT — Pending human review and approval |
| Next action | Human reviews and approves; then assemble PRICE_SOURCES per Section 6 register (primarily PS-01 staff rate table and PS-02 level-of-effort matrix); then execute ESTIMATING runs per Section 5 sequence |

---

**END OF DOCUMENT**
