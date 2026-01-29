# Source Index — PKG-20 Field Instrumentation

## Overview

This index catalogs the pricing and quantity sources discovered and used for the PKG-20 Field Instrumentation estimate.

---

## Source Hierarchy

Sources are prioritized in the following order:

1. **Explicit Pricing Sources** (quotes, vendor budgets) — Highest priority
2. **Rate Tables / Cost Libraries** — Second priority
3. **Quantity Sources** (specifications, data sheets) — For quantities
4. **Fallback Typical Model** — Last resort

---

## Sources Discovered

### 1. Explicit Pricing Sources

| Status | Source Type | Location | Notes |
|--------|-------------|----------|-------|
| NOT FOUND | Vendor quotes | — | No instrument vendor quotes available |
| NOT FOUND | Budgetary quotes | — | No budgetary quotes on file |
| NOT FOUND | Budget sheets | — | No previous project budgets |

**Impact:** All pricing uses fallback allowances (Decision D-008)

### 2. Rate Tables / Cost Libraries

| Status | Source Type | Location | Notes |
|--------|-------------|----------|-------|
| NOT FOUND | Project rate tables | `execution/_Estimates/_RateTables/` | Directory exists but empty |
| NOT FOUND | I&C unit rates | — | No instrument installation rates |
| NOT FOUND | Cable installation rates | — | No cable rates available |

**Impact:** Installation rates use industry typical values

### 3. Quantity Sources

| Status | Source Type | Location | Usage |
|--------|-------------|----------|-------|
| AVAILABLE | Decomposition | `Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | Facility scope, deliverable list |
| PARTIAL | PKG-13 Scope | Decomposition Section PKG-13 | Tank count (3 units) |
| PARTIAL | PKG-10 Scope | Decomposition Section PKG-10 | Railcar unloading (32 stations) |
| PARTIAL | PKG-11 Scope | Decomposition Section PKG-11 | Marine loading scope |
| NOT FOUND | P&IDs | — | Instrument list not available |
| NOT FOUND | Instrument Index | — | No preliminary instrument list |
| NOT FOUND | Cable Schedule | — | No cable schedule available |

**Impact:** Instrument counts estimated parametrically from facility scope

### 4. Deliverable Documents (PKG-20)

| Deliverable | Status | Content Available | Notes |
|-------------|--------|-------------------|-------|
| DEL-20.01 | INITIALIZED | Minimal | No instrument location plans available |
| DEL-20.02 | INITIALIZED | Minimal | No instrument specifications issued |
| DEL-20.03 | INITIALIZED | Minimal | No sizing calculations available |
| DEL-20.04 | INITIALIZED | Minimal | No instrument data sheets issued |
| DEL-20.05 | INITIALIZED | Minimal | No test procedures available |

**Impact:** Deliverables provide scope definition only; no detailed quantities

### 5. Related Package Sources

| Package | Relevance | Content Used |
|---------|-----------|--------------|
| PKG-13 Storage Tanks | High | Tank count, instrumentation provisions |
| PKG-10 Railcar Unloading | High | Unloading station count, flow monitoring |
| PKG-11 Marine Loading | High | Loading arm instrumentation scope |
| PKG-14 Process Piping | Medium | Piping instrumentation interface |
| PKG-15 Pumps | Medium | Pump instrumentation requirements |
| PKG-19 Control Systems | High | DCS/PLC interface (not detailed) |

---

## Fallback Typical Model Usage

Due to absence of pricing sources, the following fallback values were applied:

### Instrument Unit Costs (Typical Industry Values)

| Instrument Type | Unit Cost | Basis |
|-----------------|-----------|-------|
| Level transmitter (GWR) | $8,500 | Industry typical for guided wave radar |
| Level switch | $3,500 | Vibrating fork type |
| Temperature element (RTD) | $2,800 | PT100 with thermowell |
| Temperature transmitter | $2,200 | HART protocol |
| Pressure transmitter | $4,200-4,500 | HART protocol, various ranges |
| Flow indicator | $650 | Sight glass type |
| Vibration transmitter | $5,500 | Predictive maintenance type |
| Process switches | $1,800 | Alarm switches |

### Installation Rates (Typical Industry Values)

| Activity | Rate | Unit | Basis |
|----------|------|------|-------|
| Instrument installation | $850 | per instrument | Average installation labor |
| Cable installation | $18 | per meter | Tray/conduit installation |
| Junction box installation | $1,200 | per JB | Field installation |
| Calibration | $280 | per instrument | Field calibration |
| Loop testing | $350 | per loop | Point-to-point verification |

### Material Costs (Typical Industry Values)

| Material | Rate | Unit | Basis |
|----------|------|------|-------|
| Instrument cable | $12 | per meter | Multi-pair shielded |
| Junction box (SS) | $2,800 | each | NEMA 4X stainless |
| Instrument tubing | $35,000 | lot | SS tubing and fittings |
| Mounting hardware | $28,000 | lot | Brackets, stands |
| Conduit system | $42,000 | lot | Rigid and flex conduit |

### Indirect Factors (Fallback Model)

| Factor | Rate | Basis |
|--------|------|-------|
| Construction indirects | 18% of CD | Field supervision, QA/QC |
| Procurement services | 2% of MAT | Vendor management |
| EPCM/PM | 6% of (CD+CI+MAT) | Project management |
| Commissioning | 4% of (CD+CI+MAT) | Loop testing, I&C intensive |

---

## Source Quality Assessment

| Category | Quality | Notes |
|----------|---------|-------|
| Scope definition | MEDIUM | Decomposition provides scope outline |
| Quantity data | LOW | Parametric estimates only |
| Pricing data | LOW | No quotes or rate tables |
| Interface data | LOW | PKG-19 interface not defined |
| Overall | LOW | Class 5 estimate basis |

---

## Recommended Sources to Obtain

| Priority | Source | Purpose | Vendor/Source |
|----------|--------|---------|---------------|
| 1 | Instrument vendor quotes | MAT pricing | Emerson, Endress+Hauser, Siemens |
| 2 | P&IDs (draft) | Instrument count | PKG-14 DEL-14.01 |
| 3 | Cable schedule | Cable quantities | DEL-20.01 development |
| 4 | I&C contractor rates | Installation costs | Local I&C contractors |
| 5 | PKG-19 I/O list | Interface definition | Control system vendor |
| 6 | Hazardous area study | Instrument ratings | Process safety consultant |

---

*Source Index generated by ESTIMATING Agent | 2026-01-28*
