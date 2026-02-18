# Basis of Estimate (BOE) — Penhold Public Services Building
## Proposal Production Cost Strategy Document for ESTIMATING Runs

**Project:** Town of Penhold — Public Services Building (PSB)
**Decomposition:** `Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` (Consolidated Proposal Response)
**Currency:** CAD
**Base Year:** 2024
**Prepared:** 2026-02-18
**Status:** DRAFT — Pending human review and approval

---

## 1. Purpose

This document is the **human-authored Basis of Estimate** that governs all ESTIMATING agent runs for the Penhold PSB project under the **consolidated proposal-response decomposition** (execution-6c). It establishes:

- The estimation strategy (per-deliverable runs with aggregation)
- Per-deliverable `BASIS_OF_ESTIMATE` and substance classification
- Dependency-informed estimation ordering (which deliverables to estimate first)
- Cost ownership rules to prevent double-counting across deliverables
- A complete register of missing PRICE_SOURCES that must be assembled before meaningful estimates can be produced
- Aggregation strategy for rolling up deliverable-level estimates to package and project totals

### Critical distinction: consolidated proposal-response structure

This decomposition is organized as a **consolidated proposal-response structure** (9 packages aligned to RFP evaluation sections, 21 deliverables representing proposal documents). Design content is consolidated — one concept package, one design brief, one sustainability narrative — rather than one per engineering discipline. This means:

- **All 21 deliverables are proposal documents** — their cost is professional hours to write, draw, and coordinate
- **The estimation subject is proposal production cost**, not construction cost
- **DEL-05-01 (Schedule A) and DEL-05-02 (Schedule B) are exceptions** — these embed the actual construction pricing
- **Consolidated deliverables require multi-discipline coordination** within a single deliverable (e.g., DEL-02-02 Design Brief covers all 5 discipline sub-briefs, durability, accessibility, and adaptability in one deliverable)

### Decomposition maturity notes

This decomposition has **2 open issues** that affect estimating:

| Open Issue | Impact on Estimating |
|------------|---------------------|
| **OI-001:** Intent to Propose (Appendix C) — submit or not? | LOW: if submitted, adds minor administrative hours |
| **OI-004:** FF&E treatment — what to include and how to price | MEDIUM: affects DEL-05-01/05-02 (Schedule A/B pricing lines) and DEL-05-03 (pricing narrative). Recommend resolving before ESTIMATING runs for PKG-02 |

This document is **not** an estimate. It is the strategy input that makes estimates producible, auditable, and free of structural double-counting.

---

## 2. Project Context

| Field | Value |
|-------|-------|
| Delivery model | Design-Build (CCDC 14-2013) |
| Owner | Town of Penhold, Alberta |
| Scope | Integrated Public Services Building (Fire + Public Works), Cold Storage Building (60'x100'), Site/Civil Works, Optional Items |
| Decomposition type | **Consolidated proposal response** (packages = RFP evaluation sections; deliverables = proposal documents — not discipline-split) |
| Packages | 9 (PKG-01 through PKG-09) |
| Deliverables | 21 |
| Scope items | 28 |
| Currency | CAD |
| Base year | 2024 |
| Decomposition source | `_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` |
| Dependency evidence | `Dependencies.csv` per deliverable (21 files; DEPENDENCIES pass completed) |
| Open issues | 2 (OI-001, OI-004) |

### Key project decisions affecting estimating

| DecisionID | Decision | Estimating Impact |
|------------|----------|-------------------|
| DEC-001 | 9-package / 21-deliverable structure | Consolidated deliverables mean multi-discipline hours bundled within single DELs |

### Open issues affecting estimating

| OI ID | Issue | Estimating Impact | Recommended Resolution |
|-------|-------|-------------------|----------------------|
| OI-001 | Submit Intent to Propose (Appendix C)? | If yes: add ~2-4 hours admin to PKG-01 | Decide before T0 runs |
| OI-004 | FF&E treatment — what to include, where to price | Affects Schedule A line items, Schedule B breakdown, and pricing narrative | **Must resolve before PKG-02 ESTIMATING runs** — recommend $20,000 cash allowance as Additional Option 6 |

### Evaluation scoring context (affects effort allocation)

| Evaluation Category | Points | Primary Packages | Primary Deliverables |
|---------------------|--------|------------------|--------------------|
| Proposed Conceptual Design | 20 | PKG-04 | DEL-02-01 |
| Building Durability / Maintenance | 15 | PKG-04 | DEL-02-02 |
| Project Team & Firms | 15 | PKG-03 | DEL-07-01, DEL-07-02, DEL-07-03 |
| Proposal Price | 35 | PKG-02 | DEL-05-01, DEL-05-02, DEL-05-03 |
| Project Delivery Plan | 10 | PKG-05, PKG-06, PKG-07, PKG-08 | DEL-03-01, DEL-04-01/02/03, DEL-06-01, DEL-08-01 |
| Design Brief | 5 | PKG-04 | DEL-02-02, DEL-02-03 |

### DEL-to-PKG numbering note

The deliverable numbering in this decomposition does NOT follow a sequential PKG→DEL pattern. The mapping is:

| Package | Deliverables |
|---------|-------------|
| PKG-01 (Compliance) | DEL-01-01, DEL-01-02, DEL-01-03 |
| PKG-02 (Financial) | DEL-05-01, DEL-05-02, DEL-05-03 |
| PKG-03 (Team) | DEL-07-01, DEL-07-02, DEL-07-03 |
| PKG-04 (Design) | DEL-02-01, DEL-02-02, DEL-02-03 |
| PKG-05 (Delivery Plan) | DEL-03-01, DEL-03-02 |
| PKG-06 (Construction) | DEL-04-01, DEL-04-02, DEL-04-03 |
| PKG-07 (Commissioning) | DEL-06-01 |
| PKG-08 (Schedule) | DEL-08-01 |
| PKG-09 (Due Diligence) | DEL-09-01, DEL-09-02 |

---

## 3. Estimation Strategy

### 3.1 Run granularity: Per-deliverable

ESTIMATING will be run **once per deliverable** (21 runs). Results are aggregated by AGGREGATION into package-level and project-level totals.

**Rationale:**
- Per-deliverable runs align with the decomposition's "deliverable = unit of production" model
- Each deliverable has its own Dependencies.csv, enabling deliverable-specific blocker detection
- Consolidated deliverables (e.g., DEL-02-02 covering 5 scope items) need single-deliverable estimates that account for multi-discipline coordination overhead
- Per-deliverable snapshots are independently auditable and rerunnable
- AGGREGATION handles rollup

### 3.2 Dual cost nature of this decomposition

| Cost Type | Deliverables | Treatment |
|-----------|-------------|-----------|
| **Proposal production costs** (professional hours to produce documents) | All 21 deliverables | RATE_TABLE: hours x rates per role |
| **Construction pricing content** (the actual prices in the proposal) | DEL-05-01 (Schedule A), DEL-05-02 (Schedule B) | MIXED: production hours (RATE_TABLE) + embedded construction pricing (independent construction pricing exercise using PARAMETRIC/RATE_TABLE/QUOTE methods) |

**CRITICAL:** Production cost of DEL-05-01/05-02 (hours to FILL IN the forms) is separate from the construction pricing CONTENT. Both must be estimated but are fundamentally different cost types.

### 3.3 Common run parameters (all deliverables)

```
CURRENCY: CAD
RUN_ROOT: {EXECUTION_ROOT}
ESTIMATES_ROOT: {EXECUTION_ROOT}/_Estimates/
DECOMPOSITION_PATH: {EXECUTION_ROOT}/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md
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
| **T0** | No upstream production dependencies; estimate independently | Can run immediately once PRICE_SOURCES assembled |
| **T1** | Foundational; its outputs inform effort for downstream deliverables | Run early; outputs shape T2+ estimates |
| **T2** | Depends on T1 concept/methodology outputs | Run after T1 deliverables are characterized |
| **T3** | Depends on T2 narratives or cross-package coordination | Run after T2 outputs available |
| **T4** | Depends on substantial completion of all technical content | Run last; all technical deliverables must be characterized |

---

### PKG-01 — Compliance & Submission

**Package estimating character:** Administrative/compliance scope. DEL-01-01 and DEL-01-03 are independent checklist/documentation work. DEL-01-02 is the terminal aggregation deliverable — depends on ALL other deliverables being complete.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-01-01 | Compliance Matrix & Checklist | T0 | RATE_TABLE | STRICT | FALSE | Administrative | Proposal coordinator hours; compliance mapping across RFP Sections 6-9; addenda integration checklist |
| DEL-01-02 | Formal Submission Package | T4 | RATE_TABLE | STRICT | FALSE | Administrative + Production | Proposal coordinator hours; final PDF assembly (<15MB); submission QA; revision control. **MUST BE LAST** — depends on all 20 other deliverables |
| DEL-01-03 | Bonding & Insurance Evidence | T4 | RATE_TABLE | ALLOW_ALLOWANCE | TRUE | Administrative + Legal | Surety broker coordination; Agreement to Bond documentation; insurance approach summary; legal review. Bond premium = percentage of contract price (ALLOWANCE until Schedule A priced) |

**PKG-01 PRICE_SOURCES needed:**
- [ ] Proposal coordinator hourly rate (CAD 2024)
- [ ] Legal review hourly rate (for bond/insurance documentation)
- [ ] Surety broker fee/commission structure
- [ ] Bond premium rate (percentage of contract price)

**PKG-01 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Compliance checking + addenda tracking | DEL-01-01 | DEL-01-02 |
| Final PDF assembly + submission logistics | DEL-01-02 | All others |
| Bond/insurance documentation + premiums | DEL-01-03 | DEL-05-01, DEL-05-02 |
| Bond COST FIGURE (included in proposal price) | DEL-01-03 (documents it) + DEL-05-01/05-02 (carries it in pricing) | Other DELs |

---

### PKG-02 — Financial Proposal (Appendix H)

**Package estimating character:** Construction pricing embedded in proposal forms. DEL-05-01/05-02 have dual cost nature (production hours + construction pricing content). DEL-05-03 is a narrative with extensive cross-deliverable interfaces (6+ upstream dependencies). **OPEN ISSUE OI-004 (FF&E treatment) must be resolved before these runs.**

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-05-01 | Schedule A — Pricing Summary | T4 | RATE_TABLE | ALLOW_ALLOWANCE | TRUE | Financial + Construction Pricing | Estimator hours to compile Schedule A (base + options 1-6, taxes separated, addenda acknowledged). **PLUS:** construction pricing content — sourced from an independent construction pricing exercise |
| DEL-05-02 | Schedule B — Cost Breakdown | T4 | RATE_TABLE | ALLOW_ALLOWANCE | TRUE | Financial + Construction Pricing | Estimator hours for detailed breakdown + QA. **PLUS:** construction pricing detail. Must reconcile to Schedule A. Depends on DEL-02-01 for GFA/scope |
| DEL-05-03 | Pricing Narrative & Assumptions | T4 | RATE_TABLE | STRICT | FALSE | Narrative | PM + estimator hours; allowances (site servicing per Addendum 03; FF&E per OI-004), exclusions (pickled sand), addenda pricing impacts, value alternatives per RFP §8.5 |

**PKG-02 PRICE_SOURCES needed:**
- [ ] Estimator hourly rate (CAD 2024)
- [ ] PM hourly rate
- [ ] **For DEL-05-01/05-02 construction pricing content:** an independent construction pricing exercise (requires a full construction-level PRICE_SOURCES register: structural/mechanical/electrical system rates, earthwork rates, material pricing, vendor quotes, etc.)
- [ ] FF&E treatment decision (OI-004 — recommended: $20,000 cash allowance on Additional Option 6)

**PKG-02 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Construction pricing COMPILATION (estimator hours) | DEL-05-01 (summary), DEL-05-02 (detail) | All others |
| Construction pricing CONTENT (the actual prices) | DEL-05-01/05-02 | All other DELs (their estimates cover PRODUCTION cost only) |
| Pricing narrative + assumptions writing | DEL-05-03 | DEL-05-01, DEL-05-02 |
| Value alternatives analysis | DEL-05-03 | DEL-05-01 |
| Schedule A ↔ Schedule B reconciliation effort | Split between DEL-05-01 and DEL-05-02 | DEL-05-03 |

**CRITICAL: DEL-05-01/05-02 dual-nature estimation**
Production cost (hours to prepare forms) must be separated from construction pricing content. ESTIMATING runs should produce two line groups per deliverable.

**CRITICAL: OI-004 (FF&E) must be resolved**
Without a decision on FF&E treatment, Schedule A line items and Schedule B breakdown cannot be finalized. The recommended approach: **$20,000 cash allowance as Additional Option 6**.

---

### PKG-03 — Team Qualifications (Appendix I + resumes)

**Package estimating character:** 3 deliverables covering firm profile, resumes, and subtrade list. DEL-07-01 is independent; DEL-07-02 depends on DEL-07-01; DEL-07-03 depends on DEL-02-01 and DEL-05-02 for scope/discipline alignment. Cross-document consistency required across all three.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-07-01 | DB Firm Experience Profile | T0 | RATE_TABLE | STRICT | FALSE | Narrative | Proposal writer hours; project summaries of relevant DB experience on comparable municipal facilities; reference compilation |
| DEL-07-02 | Key Team Members & Resumes | T1 | RATE_TABLE | STRICT | FALSE | Administrative | HR/proposal coordinator hours; resume formatting; availability confirmations; role descriptions |
| DEL-07-03 | Appendix I — Subtrade & Consultant List | T3 | RATE_TABLE | STRICT | FALSE | Administrative | PM hours; subtrade/consultant procurement coordination; Appendix I form completion. Depends on DEL-02-01 (concept informs required specialties) and DEL-05-02 (pricing scopes must align) |

**PKG-03 PRICE_SOURCES needed:**
- [ ] Proposal writer hourly rate
- [ ] HR/admin hourly rate
- [ ] PM hourly rate
- [ ] Estimated hours per deliverable (firm profile = research + writing; resumes = formatting + coordination; Appendix I = procurement coordination)

**PKG-03 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Firm experience narrative writing | DEL-07-01 | DEL-07-02 |
| Resume assembly + formatting | DEL-07-02 | DEL-07-01 |
| Subtrade/consultant list compilation | DEL-07-03 | DEL-07-01, DEL-07-02 |
| Cross-document consistency checking (all 3 must align) | Shared coordination overhead in each DEL | — |

---

### PKG-04 — Design Proposal (Concept + Design Brief + Sustainability)

**Package estimating character:** Highest-effort technical package. 3 consolidated deliverables covering the proposal's design content. DEL-02-01 is the foundational concept (drawings + site plan); DEL-02-02 is a large consolidated narrative (design brief + durability + accessibility + adaptability — covers SOW-010 through SOW-015); DEL-02-03 is the sustainability/energy narrative. **Multi-discipline coordination is embedded within each deliverable**, not split across separate discipline-level deliverables.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-02-01 | Concept Design Package | T1 | RATE_TABLE | STRICT | FALSE | Design + Drawings | Architect hours (concept, floor plans, elevations, sections, site concept); CAD/BIM production; civil engineer hours (12-acre site plan, parking, grading concept); structural/mechanical/electrical engineer input hours; all Addendum 03 program requirements integrated |
| DEL-02-02 | Design Brief Narrative | T2 | RATE_TABLE | STRICT | FALSE | Narrative (multi-scope) | Architect-led narrative covering: design brief (SOW-011), durability/maintenance (SOW-013), adaptability/expansion (SOW-014), accessibility (SOW-015), embedded Addendum 03 requirements (SOW-010). Multi-discipline input: structural, mechanical, electrical, civil |
| DEL-02-03 | Sustainability & Energy Narrative | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Architect/building science + mechanical + electrical engineer hours; energy efficiency approach; solar-ready provisions; code compliance |

**PKG-04 PRICE_SOURCES needed:**
- [ ] Architect hourly rate (principal + project architect + CAD technician — CAD 2024)
- [ ] Civil engineer hourly rate
- [ ] Structural engineer hourly rate
- [ ] Mechanical engineer hourly rate
- [ ] Electrical engineer hourly rate
- [ ] Estimated hours per discipline per deliverable (DEL-02-01 highest: concept drawings; DEL-02-02 largest scope: 5+ SOW items)
- [ ] CAD/BIM software costs if not embedded in hourly rates
- [ ] Optional 3D rendering costs (DEL-02-01)

**PKG-04 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Concept DRAWINGS (floor plans, elevations, sections, site plan) | DEL-02-01 | DEL-02-02, DEL-02-03 |
| Building program integration + Addendum 03 technical requirements IN DRAWINGS | DEL-02-01 | DEL-02-02 |
| Design Brief NARRATIVE (design rationale for all disciplines) | DEL-02-02 | DEL-02-01 |
| Durability/maintenance NARRATIVE (materials, detailing, operations) | DEL-02-02 | DEL-02-01, DEL-02-03 |
| Accessibility NARRATIVE | DEL-02-02 | DEL-02-01 |
| Adaptability/expansion NARRATIVE | DEL-02-02 | DEL-02-01 |
| Addendum 03 technical requirements IN NARRATIVES | DEL-02-02 | DEL-02-01 (drawings have them; narrative explains them) |
| Sustainability/energy strategy NARRATIVE | DEL-02-03 | DEL-02-02 |
| Solar-ready provisions description | DEL-02-03 | DEL-02-01 (concept shows orientation; DEL-02-03 narrates strategy) |

**CRITICAL: DEL-02-02 is a large consolidated deliverable**

DEL-02-02 covers 5 scope items (SOW-010, SOW-011, SOW-013, SOW-014, SOW-015) — the design brief, durability, accessibility, and adaptability narratives consolidated into a single deliverable. This means:
- DEL-02-02 requires input from ALL disciplines (architect, civil, structural, mechanical, electrical)
- Coordination overhead within DEL-02-02 is significantly higher than a single-discipline narrative
- The effort estimate must account for multi-discipline writing, cross-review, and integration — not just one author
- Do NOT underestimate this deliverable — it is the largest single narrative production effort in the decomposition

**CRITICAL: DEL-02-01 / DEL-02-02 boundary (concept vs narrative)**
- DEL-02-01 = WHAT the design is (drawings, layouts, system descriptions embedded in concept)
- DEL-02-02 = WHY the design works (rationale, durability justification, accessibility compliance)
- The same engineers contribute to BOTH, but concept production hours (drawing/modeling) are in DEL-02-01 and narrative writing hours are in DEL-02-02
- Do NOT double-count: design development time is in DEL-02-01; narrative explanation time is in DEL-02-02

**CRITICAL: DEL-02-02 / DEL-02-03 boundary (design brief vs sustainability)**
- The sustainability/energy narrative (DEL-02-03) is a SEPARATE deliverable from the design brief (DEL-02-02)
- Durability/maintenance content stays in DEL-02-02 — only energy/sustainability goes in DEL-02-03
- If a topic spans both (e.g., insulation: durability + energy), the ENERGY argument goes in DEL-02-03 and the DURABILITY argument goes in DEL-02-02

---

### PKG-05 — Delivery Plan (Design Methodology + Docs Plan)

**Package estimating character:** 2 narrative deliverables. DEL-03-01 is relatively independent (design methodology). DEL-03-02 depends on DEL-03-01, DEL-08-01 (schedule milestones), and DEL-07-03 (team/discipline responsibilities).

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-03-01 | Design Methodology Narrative | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Design manager/PM hours; design approach, stakeholder engagement, decision-making, approvals, controls, innovation/value |
| DEL-03-02 | Detailed Design & Construction Docs Plan | T3 | RATE_TABLE | STRICT | FALSE | Narrative | Design manager hours; discipline deliverables, QA/QC checkpoints, review cycles, coordination approach. Depends on DEL-03-01 + DEL-08-01 (schedule milestones) |

**PKG-05 PRICE_SOURCES needed:**
- [ ] Design manager/PM hourly rate
- [ ] Estimated hours per deliverable

**PKG-05 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Design methodology narrative (process, engagement, innovation) | DEL-03-01 | DEL-03-02 |
| Design documents plan (milestones, coordination, QA/QC) | DEL-03-02 | DEL-03-01 |
| Design QC NARRATIVE | DEL-03-02 | DEL-09-01 (quality management plan for construction QC is in PKG-09) |

---

### PKG-06 — Construction Methodology + Administration

**Package estimating character:** 3 narrative deliverables. DEL-04-01 is the foundation (methodology). DEL-04-02 (budget control) has the most upstream dependencies (7 deliverables including pricing). DEL-04-03 (communications) coordinates with DEL-04-01 and DEL-04-02.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-04-01 | Construction Methodology Narrative | T2 | RATE_TABLE | STRICT | FALSE | Narrative | Construction manager hours; staging, logistics, site safety, H&S plan, permits/inspections, sequencing. Depends on DEL-02-01 (concept) and DEL-09-02 (site conditions) |
| DEL-04-02 | Budget Control & Change Management Plan | T3 | RATE_TABLE | STRICT | FALSE | Narrative | PM/construction manager hours; cost reporting, change management workflow, contingency approach. Heavy upstream dependencies: DEL-05-01/02 (budget baseline), DEL-08-01 (schedule), DEL-09-01 (risk) |
| DEL-04-03 | Communications & Reporting Plan | T3 | RATE_TABLE | STRICT | FALSE | Narrative | PM/construction manager hours; meeting structure, frequency, reporting cadence, stakeholder touchpoints. Depends on DEL-04-01 and DEL-03-01 |

**PKG-06 PRICE_SOURCES needed:**
- [ ] Construction manager hourly rate
- [ ] PM hourly rate (may be same person as other packages)
- [ ] Estimated hours per narrative section

**PKG-06 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Construction methodology (staging, logistics, safety, sequencing) | DEL-04-01 | DEL-04-02, DEL-04-03 |
| Construction administration (cleaning, transport, site services — SOW-020) | DEL-04-01 | DEL-04-02, DEL-04-03 |
| Budget control + change management | DEL-04-02 | DEL-04-01, DEL-05-03 |
| Communications + reporting protocol | DEL-04-03 | DEL-04-01 |
| Subconsultant approach (SOW-021) | DEL-04-03 | DEL-07-03 (Appendix I is the LIST; DEL-04-03 is the APPROACH) |

**NOTE:** SOW-019 (construction methodology) and SOW-020 (construction administration) are BOTH mapped to DEL-04-01 in this decomposition. This is a consolidated delivery — the estimating run for DEL-04-01 must account for BOTH scope items.

---

### PKG-07 — Commissioning, Closeout & Warranty

**Package estimating character:** Single consolidated deliverable covering commissioning, training, closeout, deficiencies management, AND warranty (SOW-022 covers all). Extensive upstream interface network (7 deliverables feed into it per dependency analysis).

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-06-01 | Commissioning, Training, Closeout & Warranty Narrative | T3 | RATE_TABLE | STRICT | FALSE | Narrative | Commissioning lead/PM hours; commissioning approach, training documentation, O&M manuals, as-built process, deficiencies management (punch lists, valuation, holdback), 12-month warranty, SC provisions |

**PKG-07 PRICE_SOURCES needed:**
- [ ] Commissioning lead hourly rate
- [ ] PM hourly rate
- [ ] Estimated hours for consolidated narrative (note: this single deliverable covers commissioning, training, closeout, deficiencies management, and warranty)

**PKG-07 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| All commissioning/training/closeout/deficiencies/warranty narrative content | DEL-06-01 | PKG-06 (construction methodology is separate from commissioning) |
| Commissioning COMMUNICATION protocols | DEL-04-03 (authoritative source) | DEL-06-01 (references DEL-04-03) |

---

### PKG-08 — Schedule & Milestones

**Package estimating character:** Single deliverable requiring Gantt chart production. Multiple upstream dependencies (concept, methodology, pricing, commissioning, risk, site conditions).

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-08-01 | Detailed Project Schedule | T2 | RATE_TABLE | STRICT | FALSE | Schedule + Narrative | Scheduler/PM hours; Gantt chart production; critical path analysis; milestone dates; schedule assumptions |

**PKG-08 PRICE_SOURCES needed:**
- [ ] Scheduler hourly rate
- [ ] Scheduling software costs (if not embedded)
- [ ] Estimated hours (higher than typical narrative — requires Gantt production)

**PKG-08 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Gantt chart + critical path + milestones + assumptions | DEL-08-01 | DEL-04-01 (construction schedule CONTROL is methodology; DEL-08-01 is the SCHEDULE itself) |

**NOTE on circular dependency:** DEL-08-01 depends on DEL-04-01 (construction methodology for sequencing), and DEL-04-01 depends on DEL-08-01 (schedule for feasibility). In practice these are co-developed iteratively. For estimating purposes, both are placed in T2 and can be estimated in parallel, with a note that their production overlaps.

---

### PKG-09 — Due Diligence & Risk Register

**Package estimating character:** 2 deliverables based primarily on reference document analysis. DEL-09-02 (site conditions) is a critical feeder hub — its outputs inform concept design, pricing, construction methodology, and schedule. DEL-09-01 (risk register) also includes quality management plan (SOW-027).

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-09-01 | Risk Register & Mitigation Plan | T0 | RATE_TABLE | STRICT | FALSE | Register + Narrative | PM + technical lead hours; risk identification across all categories; quality management plan (SOW-027: design QC + construction QC + documentation QC). Based on reference documents + RFP analysis |
| DEL-09-02 | Site Conditions & Due Diligence Summary | T0 | RATE_TABLE | STRICT | FALSE | Narrative | PM + technical lead hours; geotech summary, wetland assessment, environmental assessment, flood zone, site grading, survey approach (files after award per Addendum 03) |

**PKG-09 PRICE_SOURCES needed:**
- [ ] PM hourly rate
- [ ] Technical lead hourly rates (for review/input from civil, structural, environmental disciplines)
- [ ] Estimated hours for reference document review and analysis

**PKG-09 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Risk register (all categories) | DEL-09-01 | DEL-05-03 (pricing ASSUMPTIONS are in PKG-02; RISKS are in PKG-09) |
| Quality management plan (SOW-027) | DEL-09-01 | DEL-03-02 (design docs plan covers design QC; DEL-09-01 covers overall QMP) |
| Site conditions summary | DEL-09-02 | DEL-02-01 (concept USES site data; PKG-09 SUMMARIZES it) |
| Survey approach/assumptions | DEL-09-02 | DEL-08-01 (schedule notes survey timing; PKG-09 documents the approach) |

**NOTE:** DEL-09-01 carries both the risk register (SOW-026) AND the quality management plan (SOW-027) in this decomposition. The effort estimate must cover both scope items.

---

## 5. Dependency-Informed Run Sequence

Runs should be executed in tier order. Within a tier, runs are independent and may be parallelized.

### Sequence

```
TIER 0 (run immediately; no production dependencies):
  DEL-01-01  (Compliance Matrix)
  DEL-07-01  (Firm Experience)
  DEL-09-01  (Risk Register + QMP)
  DEL-09-02  (Site Conditions)
  [4 parallel runs]

TIER 1 (foundational — run next; outputs shape all technical narratives):
  DEL-02-01  (Concept Design Package — needs DEL-09-02 site data)
  DEL-07-02  (Key Team Resumes — needs DEL-07-01 firm profile)
  [2 parallel runs]

TIER 2 (depends on T1 concept/methodology outputs):
  DEL-02-02  (Design Brief — consolidated narrative, depends on DEL-02-01)
  DEL-02-03  (Sustainability — depends on DEL-02-01, DEL-02-02)
  DEL-03-01  (Design Methodology — depends on DEL-02-01, DEL-02-02)
  DEL-04-01  (Construction Methodology — depends on DEL-02-01, DEL-09-02)
  DEL-08-01  (Schedule — co-developed with DEL-04-01)
  [5 parallel runs, noting DEL-02-03 and DEL-03-01 may lag slightly within tier]

TIER 3 (depends on T2 narratives + cross-package coordination):
  DEL-03-02  (Design Docs Plan — depends on DEL-03-01, DEL-08-01, DEL-07-03)
  DEL-04-02  (Budget Control — depends on DEL-05-01/02, DEL-08-01, DEL-09-01)
  DEL-04-03  (Communications — depends on DEL-04-01, DEL-03-01)
  DEL-06-01  (Commissioning — depends on DEL-04-01, DEL-08-01, DEL-03-01)
  DEL-07-03  (Appendix I — depends on DEL-02-01, DEL-05-02)
  [5 parallel runs, noting DEL-04-02 depends on T4 pricing — see note below]

TIER 4 (pricing + compliance — depends on all technical content):
  DEL-05-01  (Schedule A — requires all technical packages + construction pricing)
  DEL-05-02  (Schedule B — must reconcile to DEL-05-01)
  DEL-05-03  (Pricing Narrative — depends on DEL-05-01/02)
  DEL-01-03  (Bonding — depends on DEL-05-01 for contract value)
  [DEL-05-01 first → DEL-05-02 → DEL-05-03/DEL-01-03 in parallel]

TIER 5 (final assembly — terminal):
  DEL-01-02  (Formal Submission Package — depends on ALL other 20 deliverables)
  [1 run]

Total: 21 ESTIMATING runs across 6 tiers
```

**NOTE on T3/T4 circular dependency:** DEL-04-02 (Budget Control) depends on DEL-05-01/05-02 (pricing), but those are T4. In practice, DEL-04-02 can be estimated for production hours without final pricing — the budget control METHODOLOGY doesn't require knowing the actual numbers. The cost of producing the plan is independent of the budget it describes.

### Tier dependencies (what must be resolved before next tier runs)

| Before Tier | Must Have |
|-------------|----------|
| T0 → T1 | PRICE_SOURCES for design discipline hourly rates; reference documents reviewed (DEL-09-02 site conditions) |
| T1 → T2 | DEL-02-01 concept characterized (building footprint, site layout, system selections); DEL-07-01 firm profile established |
| T2 → T3 | DEL-02-02 design brief scope defined; DEL-04-01 construction methodology framework; DEL-08-01 schedule framework |
| T3 → T4 | All technical narratives complete; construction pricing from independent exercise available; OI-004 (FF&E) resolved |
| T4 → T5 | All 20 deliverables complete and finalized |

### External gates that block meaningful estimating

| Gate | Blocks | Status | Impact |
|------|--------|--------|--------|
| Construction estimates for Schedule A/B content | DEL-05-01, DEL-05-02 construction pricing content | TBD | Without construction pricing, Schedule A/B content cannot be completed |
| **OI-004 resolution (FF&E treatment)** | DEL-05-01, DEL-05-02, DEL-05-03 | **OPEN** | Must decide what FF&E includes and how it's priced before PKG-02 runs |
| OI-001 resolution (Intent to Propose) | Minor: PKG-01 admin hours | OPEN | Low impact; ~2-4 hours if submitted |
| Reference document accessibility | DEL-09-01, DEL-09-02, DEL-02-01 | Multiple documents flagged as inaccessible in Dependencies.csv | If unavailable, DELs proceed with assumptions per decomposition procedure |
| RFP §5.3.1 bond requirements extraction | DEL-01-03 | Flagged as not extracted | If unclear, carry standard bond rate assumption |
| RFP §7.3.4 communications requirements | DEL-04-03 | Flagged as not accessible | If unclear, proceed with standard practice narrative |
| Subtrade availability confirmations | DEL-07-03 | TBD | May require follow-up coordination |
| Proposal submission timeline | All | TBD | Compressed timeline increases parallel effort overhead |

---

## 6. Complete Missing PRICE_SOURCES Register

### Critical (block meaningful estimates for most deliverables)

| ID | Source Needed | Affects | Priority |
|----|--------------|---------|----------|
| PS-01 | Proposal production staff rate table — ALL roles: Architect (principal, project architect, CAD tech), Civil Engineer, Structural Engineer, Mechanical Engineer, Electrical Engineer, PM, Design Manager, Construction Manager, Commissioning Lead, Scheduler, Estimator, Proposal Coordinator/Writer, Quality Lead, HR/Admin, Legal — hourly rates, CAD 2024 | All 21 deliverables | HIGH |
| PS-02 | Estimated production hours per deliverable per discipline (level-of-effort matrix) | All 21 deliverables | HIGH |
| PS-03 | Proposal preparation timeline (weeks from start to submission) | All deliverables — affects coordination overhead | HIGH |

### Important (needed for specific deliverables or cost types)

| ID | Source Needed | Affects | Priority |
|----|--------------|---------|----------|
| PS-04 | Construction pricing for Schedule A/B content — independent construction pricing exercise | DEL-05-01, DEL-05-02 | HIGH (for pricing content; production hours estimated without this) |
| PS-05 | Bond premium rate (percentage of contract price) | DEL-01-03, DEL-05-02 | MEDIUM |
| PS-06 | Insurance approach and premium estimate | DEL-01-03, DEL-05-02 | MEDIUM |
| PS-07 | Surety broker fee/commission structure | DEL-01-03 | MEDIUM |
| PS-08 | Legal review hourly rate | DEL-01-03 | MEDIUM |
| PS-09 | **FF&E treatment decision (OI-004)** | DEL-05-01, DEL-05-02, DEL-05-03 | MEDIUM (BLOCKING for PKG-02) |

### Low priority

| ID | Source Needed | Affects | Priority |
|----|--------------|---------|----------|
| PS-10 | CAD/BIM software costs (if not in hourly rates) | DEL-02-01 | LOW |
| PS-11 | Scheduling software costs (if not in hourly rate) | DEL-08-01 | LOW |
| PS-12 | Optional 3D rendering/visualization costs | DEL-02-01 | LOW |

---

## 7. Aggregation Strategy

After all ESTIMATING runs are complete, run AGGREGATION to produce:

### 7.1 Package-level rollups

| Aggregation | Scope | Expected Output |
|-------------|-------|-----------------|
| PKG-01 total | DEL-01-01, DEL-01-02, DEL-01-03 | Compliance & Submission production costs |
| PKG-02 total (production) | DEL-05-01, DEL-05-02, DEL-05-03 | Financial Proposal production costs (EXCLUDING construction pricing content) |
| PKG-02 construction pricing | DEL-05-01, DEL-05-02 (content only) | Construction pricing — reported SEPARATELY |
| PKG-03 total | DEL-07-01, DEL-07-02, DEL-07-03 | Team Qualifications production costs |
| PKG-04 total | DEL-02-01, DEL-02-02, DEL-02-03 | Design Proposal production costs |
| PKG-05 total | DEL-03-01, DEL-03-02 | Delivery Plan production costs |
| PKG-06 total | DEL-04-01, DEL-04-02, DEL-04-03 | Construction Methodology production costs |
| PKG-07 total | DEL-06-01 | Commissioning/Closeout production costs |
| PKG-08 total | DEL-08-01 | Schedule production costs |
| PKG-09 total | DEL-09-01, DEL-09-02 | Due Diligence production costs |

### 7.2 Project-level totals

| Total | Composition |
|-------|-------------|
| **Total Proposal Production Cost** | Sum of all 9 package production cost totals |
| **Construction Pricing Content** (separately reported) | DEL-05-01/05-02 construction pricing — the PROPOSAL PRICE, not a production cost |
| **Grand Total Proposal Effort** | Production cost + construction pricing compilation effort |

### 7.3 Effort matrix (hours by role x package)

AGGREGATION should produce a combined effort matrix showing:
- **Rows:** Role (architect, civil engineer, structural engineer, mechanical engineer, electrical engineer, PM, design manager, construction manager, scheduler, estimator, proposal coordinator, commissioning lead, quality lead, legal, admin)
- **Columns:** Package (PKG-01 through PKG-09)
- **Cells:** Hours per role per package
- **Totals:** Row totals (total hours per role) and column totals (total hours per package)

### 7.4 Evaluation-weight-adjusted view

| Evaluation Category | Points | Total Estimated Hours | Cost | $/Point |
|---------------------|--------|----------------------|------|---------|
| Mandatory Compliance | Pass/Fail | (PKG-01) | | N/A |
| Proposed Conceptual Design (20 pts) | 20 | (DEL-02-01) | | (cost/20) |
| Design Brief + Sustainability (5 pts) | 5 | (DEL-02-02 + DEL-02-03) | | (cost/5) |
| Durability/Maintenance (15 pts) | 15 | (DEL-02-02 portion) | | (cost/15) |
| Delivery Plan (10 pts) | 10 | (PKG-05 + PKG-06 + PKG-07 + PKG-08) | | (cost/10) |
| Team/Firms (15 pts) | 15 | (PKG-03) | | (cost/15) |
| Proposal Price (35 pts) | 35 | (PKG-02) | | (cost/35) |

**NOTE:** DEL-02-02 contributes to BOTH "Design Brief" (5 pts) and "Durability/Maintenance" (15 pts) because it is a consolidated deliverable. The effort-to-points allocation must split DEL-02-02 hours proportionally.

---

## 8. Assumptions and Constraints Log

| ID | Assumption/Constraint | Source | Impact if Wrong |
|----|----------------------|--------|-----------------|
| A-01 | All professional hourly rates are internal DB rates (not external consultant fees unless stated) | BOE assumption | If external consultants used, rates may be higher |
| A-02 | Consolidated deliverables (DEL-02-02, DEL-06-01, DEL-09-01) require multi-discipline coordination overhead beyond sum-of-parts writing hours | Decomposition structure (fewer DELs = more content per DEL) | If underestimated, these deliverables will exceed budget |
| A-03 | DEL-05-01/05-02 construction pricing content sourced from an independent construction pricing exercise | BOE strategy decision | If construction estimates are not available, DEL-05-01/05-02 cannot be completed for pricing content — production hours can still be estimated |
| A-04 | OI-004 (FF&E) will be resolved as $20,000 cash allowance as Additional Option 6 | Recommended resolution | If different treatment, Schedule A/B line items and narrative change |
| A-05 | OI-001 (Intent to Propose) will not be submitted — zero cost | Recommended resolution | If submitted, minor administrative cost addition to PKG-01 |
| A-06 | Proposal submission is digital only (email PDF <15MB) | RFP 4.2, 5.3 | Minimal cost impact |
| A-07 | Bond and insurance premium rates are standard market rates until actual quotes obtained | BOE assumption | Actual premiums may vary |
| A-08 | Base year 2024; no escalation applied to professional rates | Project direction | If preparation extends, rates may escalate |
| A-09 | All 21 deliverables estimated regardless of evaluation weight | BOE strategy | Low-weight items naturally have lower hours |
| A-10 | Reference documents flagged as inaccessible in Dependencies.csv (geotech, wetlands, environmental, site grading) will be available for production — if not, deliverables proceed with assumptions and flag gaps | Decomposition procedure | If permanently unavailable, some narrative content will be thinner |
| A-11 | Decomposition telemetry states "14 deliverables" but 21 are defined in Section 8 — this BOE uses the actual count of 21 | Document discrepancy | No impact; 21 is the correct count per the section definitions |

---

## 9. Document Control

| Field | Value |
|-------|-------|
| Document | Basis of Estimate (BOE) — Proposal Production (Consolidated) |
| Version | DRAFT v0.1 |
| Prepared by | [Human operator] with HELP_HUMAN agent support |
| Date | 2026-02-18 |
| Status | DRAFT — Pending human review and approval |
| Next action | Human reviews and approves; resolve OI-004 (FF&E) and OI-001 (Intent to Propose); then assemble PRICE_SOURCES per Section 6; then execute ESTIMATING runs per Section 5 sequence |

---

**END OF DOCUMENT**
