# Decision Log

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG12_DRAFT_2026-01-28_2341 |
| Estimate Label | PKG12_DRAFT |
| Package | PKG-12 Product Transfer & Metering |
| Date | 2026-01-28 |

---

## D-001: Currency Selection

**Decision:** Use CAD (Canadian dollars) for all estimate values

**Trigger:** Config file specifies CAD; project location is Surrey, BC, Canada

**Evidence:**
- `_CONFIG.md` line 9: `currency | CAD`
- Decomposition line 10: "Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC"

**Impacted WBS/CBS:** All packages, all CBS buckets

**Estimate Impact:** All costs denominated in CAD; no currency conversion required

**Override Path:** Edit `_CONFIG.md` to change currency parameter

---

## D-002: Pricing Basis Selection (Allowances)

**Decision:** Use allowances for all line items due to absence of vendor quotes and rate tables

**Trigger:** Source discovery found no vendor quotes or project-specific rate tables

**Evidence:**
- Rate table directory search: `test/execution/_Estimates/_RateTables/` — not found
- Deliverable `_REFERENCES.md` files reviewed — no vendor quote references
- Source_Index.md: "Explicit Pricing Sources: None available"

**Impacted WBS/CBS:** All PKG-12 deliverables, all CBS buckets

**Estimate Impact:** All pricing uses fallback typical model; estimate confidence is LOW; cost ranges are wide

**Override Path:** Provide vendor budgetary quotes for custody transfer metering equipment, or populate `_RateTables/` with project-specific labor/equipment/material rates

---

## D-003: Meter Technology Assumption

**Decision:** Assume Coriolis mass flowmeter technology for custody transfer flow meters

**Trigger:** Meter technology not specified in available deliverable documents (deliverables in INITIALIZED state)

**Evidence:**
- DEL-12.02 Datasheet.md line 69: "Technology selection (Coriolis mass flowmeter, ultrasonic flowmeter, turbine flowmeter, positive displacement flowmeter, or other)"
- Typical custody transfer practice: Coriolis offers direct mass measurement, high accuracy (±0.15% typical), integral density measurement, good for viscous products

**Impacted WBS/CBS:** MAT (flow meters), CD (installation)

**Estimate Impact:** Flow meter unit cost ~$150k-250k/unit (Coriolis typical range); higher than turbine (~$30k-80k) or ultrasonic (~$80k-150k), but better accuracy and integrated density

**Override Path:** Confirm meter technology selection in DEL-12.02 specification; adjust flow meter costs if different technology selected

---

## D-004: Proving Method Assumption

**Decision:** Assume portable prover for custody transfer meter proving

**Trigger:** Proving method not specified in available deliverable documents

**Evidence:**
- DEL-12.02 Datasheet.md line 71: "Proving method (in-line prover with sphere or piston, portable prover, master meter, or combination)"
- Typical for dual-service installations (rail + marine): Portable prover provides flexibility to prove both meters without dedicated in-line provers

**Impacted WBS/CBS:** MAT (proving equipment), COM (proving labor)

**Estimate Impact:** Portable prover cost ~$100k-150k; lower than dual in-line provers (~$150k-250k each), higher than master meter approach (~$50k-80k for master meter + periodic external calibration)

**Override Path:** Confirm proving method in DEL-12.02 specification; adjust proving equipment cost if in-line prover or master meter selected

---

## D-005: Labor Rate Assumption

**Decision:** Use $120/hr all-in labor rate for construction direct labor

**Trigger:** No project-specific labor rates available in rate tables

**Evidence:**
- Rate table search: No rate tables found
- Typical BC lower mainland labor rates for industrial/process work: $100-140/hr all-in (direct wage + fringes + burden + contractor markup)

**Impacted WBS/CBS:** CD (construction directs)

**Estimate Impact:** All CD labor priced at $120/hr; actual rates may vary based on trade (pipefitter, instrument tech, electrician, etc.)

**Override Path:** Provide project labor rate table in `_RateTables/` with craft-specific rates

---

## D-006: Metering Point Configuration

**Decision:** Assume separate dedicated meters for rail unloading and marine loading (not shared/manifolded)

**Trigger:** Configuration not explicitly stated; typical custody transfer practice

**Evidence:**
- DEL-12.01 Datasheet.md line 36: "Metering Points: Two primary custody transfer locations: (1) Rail unloading custody transfer; (2) Marine loading custody transfer"
- Typical practice: Separate meters for independent operations and custody transfer integrity

**Impacted WBS/CBS:** MAT (2 flow meters required), E (separate sizing/design for each service)

**Estimate Impact:** Requires 2 flow meters (~$150k-250k each) vs. 1 shared meter; provides operational flexibility and redundancy

**Override Path:** Confirm metering configuration in DEL-12.01 drawings and DEL-12.02 specification

---

## D-007: Indirects and Services Factors

**Decision:** Apply factor-based indirects and services per fallback typical model

**Trigger:** Default estimating method per AGENT_ESTIMATING.md; no project-specific schedule or duration data available

**Evidence:**
- AGENT_ESTIMATING.md lines 665-673: Default factors for CI (18% CD), P (2% MAT), PM (6% CD+CI+MAT), COM (3% CD+CI+MAT)
- No schedule or cashflow data available for time-based indirects model

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:**
- CI = 18% of CD = ~$77k
- P = 2% of MAT = ~$54k
- PM = 6% of (CD+CI+MAT) = ~$216k
- COM base (factor) = 3% of (CD+CI+MAT) = ~$108k

**Override Path:** Provide project schedule and duration estimates for time-based indirects calculation, or override factors in `_CONFIG.md`

---

## D-008: Contingency Method (PCT_BY_BUCKET)

**Decision:** Use PCT_BY_BUCKET contingency method with allowance-heavy adjustment

**Trigger:** Config specifies `contingency_method = PCT_BY_BUCKET`; 100% allowance-based estimate

**Evidence:**
- `_CONFIG.md` line 35: `contingency_method | PCT_BY_BUCKET`
- AGENT_ESTIMATING.md lines 676-689: Contingency baseline by CBS + allowance-heavy adjustment (+0.10 for >80% allowance share)

**Impacted WBS/CBS:** All CBS buckets (contingency applied to each)

**Estimate Impact:**
- E: 10% base + 10% allowance adjustment = 20%
- MAT: 15% base + 10% allowance adjustment = 25%
- CD: 20% base + 10% allowance adjustment = 30%
- CI: 20% base + 10% (factor-derived) = 30%
- PM: 10% base + 5% (factor-derived) = 15%
- P: 10% base + 5% (factor-derived) = 15%
- COM: 25% base + 5% (factor-derived) = 30%

**Override Path:** Change `contingency_method` to `RISK_BASED` in `_CONFIG.md`, or provide risk register with quantified risk impacts

---

## D-009: Escalation Mode

**Decision:** No escalation applied (escalation_mode = NONE)

**Trigger:** Config specifies NONE; pricing date is current (2026-01)

**Evidence:**
- `_CONFIG.md` line 36: `escalation_mode | NONE`
- Pricing date 2026-01 is current month

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Estimate is in January 2026 dollars; no escalation to project midpoint or cashflow-weighted average date

**Override Path:** Change `escalation_mode` to `EXPLICIT` in `_CONFIG.md` and provide escalation factors or schedule/cashflow curve

---

## D-010: Rounding Policy

**Decision:** Round all summary values to nearest $1,000 CAD

**Trigger:** Config specifies rounding = 1000

**Evidence:**
- `_CONFIG.md` line 13: `rounding | 1000`

**Impacted WBS/CBS:** Summary.md totals (Detail.csv line items not rounded)

**Estimate Impact:** Summary totals rounded to $1k; minor differences may appear between Detail.csv sum and Summary.md due to rounding

**Override Path:** Change `rounding` parameter in `_CONFIG.md`

---

## Summary

| Decision Count | 10 |
|----------------|-----|
| Currency/Config Decisions | D-001, D-009, D-010 |
| Pricing Basis Decisions | D-002, D-003, D-004, D-005 |
| Scope/Config Decisions | D-006, D-007, D-008 |

All decisions are recorded with evidence and override path for next run transparency.

---

*Decision log prepared per AGENT_ESTIMATING SPEC requirements. All defaults and ambiguities documented for auditability.*
