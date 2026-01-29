# Decision Log

## Overview

This log captures all decisions made during the estimating process where the agent selected defaults, resolved ambiguities, or made choices affecting the estimate.

---

## D-001: Currency Selection

**Decision:** Use CAD (Canadian dollars) for all estimate values.

**Trigger:** No explicit currency specified in deliverable documents.

**Evidence:**
- Project location: Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- Canadian project location implies CAD currency

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** None (currency selection; does not change values)

**Override Path:** Set `currency: USD` (or other) in `_CONFIG.md` if different currency required.

---

## D-002: Rail Track Interface Assumption

**Decision:** Assume PKG-07 Rail Works provides track alignment, railcar positioning, and station spacing.

**Trigger:** PKG-07 deliverable details not yet available; station positioning required for unloading arm placement.

**Evidence:**
- Decomposition Section 5: PKG-07 Rail Works scope includes rail infrastructure
- DEL-10.01 Datasheet Section "Construction" references PKG-07 interface for track alignment

**Impacted WBS/CBS:** PKG-10 (all deliverables); affects unloading arm spacing and header routing

**Estimate Impact:** Qualitative — affects design coordination effort; no direct cost impact on this estimate

**Override Path:** Provide PKG-07 track layout drawings (DEL-07.01) for coordination verification.

---

## D-003: Header Discharge Interface Assumption

**Decision:** Assume PKG-14 Process Piping provides downstream piping connection from header discharge point.

**Trigger:** PKG-14 deliverable details not yet available; header discharge connection required for interface definition.

**Evidence:**
- Decomposition Section 5: PKG-14 Process Piping scope includes product transfer piping
- DEL-10.01 Datasheet Section "Construction" references PKG-14 interface for header discharge connection

**Impacted WBS/CBS:** PKG-10 (DEL-10.01, DEL-10.03); affects header terminus design

**Estimate Impact:** Qualitative — affects interface coordination; header piping estimate assumes connection at header terminus only

**Override Path:** Provide PKG-14 process piping layout for interface coordination.

---

## D-004: Productivity Factor Selection

**Decision:** Use productivity factor of 1.0 (baseline) for BC lower mainland.

**Trigger:** No project-specific productivity data available.

**Evidence:**
- Location: Fraser Surrey Terminal, Surrey, BC (major urban area with skilled labor availability)
- BC lower mainland is a major construction market with typical productivity

**Impacted WBS/CBS:** All construction labor (CBS = CD, CI)

**Estimate Impact:** None (baseline productivity factor); changing factor would scale labor costs proportionally

**Override Path:** Provide project productivity assessment or adjust labor rates in rate tables to account for site-specific factors.

---

## D-005: Site Access Assumption

**Decision:** Assume standard construction site access adjacent to rail tracks with no extraordinary access constraints.

**Trigger:** No site access restrictions documented in deliverable documents.

**Evidence:**
- PKG-10 scope is railcar unloading system located at rail track alignment
- DEL-10.01 Datasheet does not mention access restrictions

**Impacted WBS/CBS:** CD (construction labor productivity and mobilization)

**Estimate Impact:** Minimal — standard access assumed; extraordinary access (e.g., work within active rail corridor with frequent train traffic) would increase labor costs

**Override Path:** Provide site access constraints or rail operations coordination requirements if applicable.

---

## D-006: Working Hours Assumption

**Decision:** Assume standard 8-10 hour shifts with minimal constraints.

**Trigger:** No shift restrictions or working hour limitations documented.

**Evidence:**
- Industrial site location with no apparent shift restrictions in deliverable documents
- PKG-10 scope does not reference special working hour requirements

**Impacted WBS/CBS:** CD, CI (labor costs and schedule)

**Estimate Impact:** Minimal — standard shift assumptions; shift work premiums or restricted hours would increase labor costs

**Override Path:** Provide working hour restrictions or shift requirements if applicable (e.g., night work only, rail traffic windows).

---

## D-007: Pricing Basis Selection

**Decision:** Price all line items using allowances (fallback typical model) due to absence of vendor quotes or rate tables.

**Trigger:** No vendor quotes or project rate tables available for PKG-10 scope.

**Evidence:**
- Source search found no quotes, budgetary proposals, or rate tables for unloading arms or related equipment
- `_RateTables/` directory empty (no project rate library)

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** HIGH — all pricing is parametric/allowance-based with LOW confidence; variance likely when actual quotes obtained

**Override Path:**
1. Obtain budgetary quotes from unloading arm suppliers (TechnipFMC, OPW, Emco Wheaton, etc.)
2. Populate `_RateTables/` with project labor rates, equipment rates, material unit costs
3. Re-run estimating pipeline to replace allowances with quote/rate pricing

---

## D-008: Indirects and Services Factors

**Decision:** Apply factor-based indirects and services per fallback typical model.

**Trigger:** No project-specific indirects pricing or time-based model available.

**Evidence:**
- No schedule/duration data available for time-based indirects calculation
- Fallback typical model (AGENT_ESTIMATING Section "Fallback Typical Model") provides default factors

**Factors Applied:**
- CI (Construction Indirects) = 18% × CD
- P (Procurement Services) = 2% × MAT
- PM (EPCM/PM) = 6% × (CD + CI + MAT)

**Impacted WBS/CBS:** CI, P, PM

**Estimate Impact:** MEDIUM — factors are typical industry averages; actual project indirects may vary ±25% depending on schedule, site conditions, project complexity

**Override Path:** Provide project schedule and indirects staffing plan for time-based indirects calculation, or provide indirect cost rates in `_CONFIG.md` to override factors.

---

## D-009: Contingency Rates

**Decision:** Apply elevated contingency rates per PCT_BY_BUCKET method with allowance-heavy adjustments.

**Trigger:** 100% allowance-based estimate with no vendor quotes; specialized equipment with limited pricing data.

**Evidence:**
- All line items priced via allowances (Method = ALLOWANCE or PARAMETRIC)
- Specialized railcar unloading equipment (32 articulating arms) with vendor-specific pricing variation

**Contingency Rates Applied:**
- E: 20% (10% base + 10% allowance adjustment)
- MAT: 25% (15% base + 10% allowance adjustment)
- CD: 30% (20% base + 10% allowance adjustment)
- CI: 30% (20% base + 10% factor-derived adjustment)
- PM: 15% (10% base + 5% factor-derived adjustment)
- P: 15% (10% base + 5% factor-derived adjustment)
- COM: 30% (25% base + 5% allowance adjustment)

**Impacted WBS/CBS:** All CBS buckets (CONT)

**Estimate Impact:** HIGH — contingency totals $996,000 (25.4% of base); reflects estimate uncertainty

**Override Path:** Obtain vendor quotes and rate tables to reduce allowance share and lower contingency rates in next run.

---

## D-010: Escalation Mode

**Decision:** Do not apply escalation (escalation_mode = NONE).

**Trigger:** Config specifies NONE; pricing date is current (January 2026).

**Evidence:**
- `_CONFIG.md` specifies `escalation_mode: NONE`
- Pricing date = 2026-01 (current month)

**Impacted WBS/CBS:** All CBS buckets (no ESC bucket)

**Estimate Impact:** None for current estimate; future project execution may require escalation depending on schedule

**Override Path:** Set `escalation_mode: EXPLICIT` in `_CONFIG.md` and provide schedule/cashflow data for escalation calculation.

---

## D-011: Unloading Arm Type Selection

**Decision:** Assume articulating bottom-loading arms as the unloading arm type.

**Trigger:** Deliverable documents reference "bottom-loading" but specific arm configuration (articulating vs. fixed) not specified.

**Evidence:**
- DEL-10.01 Datasheet Section "Conditions" notes "bottom-loading type **ASSUMPTION**"
- Industry practice: articulating arms are standard for railcar bottom unloading (provides reach flexibility and operator safety)
- Gravity flow requirement (decomposition PKG-10 scope) implies bottom outlet connection

**Impacted WBS/CBS:** MAT (unloading arms), CD (installation labor)

**Estimate Impact:** MEDIUM — articulating arms are higher cost ($45k-60k/unit) than fixed arms; installation labor also higher

**Override Path:** Verify arm type requirements in Employer's Requirements or specify arm configuration in DEL-10.02 specification.

---

## D-012: Header Piping Length Estimate

**Decision:** Estimate 400 lm of header piping for 32-station layout.

**Trigger:** DEL-10.01 header layout drawings not yet available; piping length required for material and labor estimates.

**Evidence:**
- 32 stations with typical spacing of 12-14m on-center (industry standard for railcar unloading facilities)
- Header routing: main header run (~380m for 32 stations) + branch connections (~20m allowance) = ~400 lm total
- Assumption logged as A-003

**Impacted WBS/CBS:** MAT (header piping supply), CD (piping installation labor)

**Estimate Impact:** MEDIUM — header piping is ~$280k material + $180k labor; ±20% variance if actual layout differs

**Override Path:** Provide DEL-10.01 header layout drawings to verify piping length from actual routing.

---

## D-013: Sump Pump Quantity

**Decision:** Estimate 8 sump pumps for grouped containment drainage.

**Trigger:** Containment drainage configuration not yet defined in DEL-10.01; pump quantity required for estimate.

**Evidence:**
- DEL-10.04 Datasheet notes sump pump quantity as "**TBD** per containment design from DEL-10.01"
- Grouped containment zones reduce pump count vs. 32 individual pumps (1 per pan)
- Typical configuration: 4 pumps per zone with 2 zones for 32 stations (4 pumps × 2 zones = 8 total)
- Assumption logged as A-005

**Impacted WBS/CBS:** MAT (sump pumps), CD (pump installation)

**Estimate Impact:** LOW-MEDIUM — sump pumps total ~$48k material + $24k labor; quantity variance from 4 to 16 pumps would affect costs by ±50%

**Override Path:** Provide DEL-10.01 containment details drawings showing drainage configuration and pump locations.

---

## Summary

Total decisions logged: 13 (D-001 through D-013)

**Critical decisions affecting estimate significantly:**
- D-007: All allowance-based pricing (HIGH impact — entire estimate variance)
- D-009: Elevated contingency rates (HIGH impact — $996k contingency)
- D-011: Unloading arm type (MEDIUM impact — ~$1.6M equipment cost)
- D-012: Header piping length (MEDIUM impact — ~$460k header piping total)

**Decision categories:**
- Currency and config: 3 decisions (D-001, D-010, rounding per config)
- Interface assumptions: 2 decisions (D-002, D-003)
- Productivity and site: 3 decisions (D-004, D-005, D-006)
- Pricing methodology: 3 decisions (D-007, D-008, D-009)
- Technical assumptions: 2 decisions (D-011, D-013)

All decisions are recorded for audit trail and can be overridden in subsequent estimate runs by providing better inputs (quotes, rate tables, interface documents, design details).
