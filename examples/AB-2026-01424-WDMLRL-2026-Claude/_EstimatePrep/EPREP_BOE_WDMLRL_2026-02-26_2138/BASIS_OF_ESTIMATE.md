# BASIS OF ESTIMATE — EPREP_BOE_WDMLRL_2026-02-26_2138

## 1. Purpose

This BOE defines estimation strategy, PRICE_SOURCES posture, and dependency-informed tier sequencing. It does not compute totals; ESTIMATING consumes the input package to produce estimates.

## 2. Project Context

- Project: 2026 Design Build of West Dried Meat Lake Regional Landfill Maintenance Shop Addition
- Owner: Camrose County
- Location: near Ferintosh, Alberta
- Contract form: CCDC 14–2013 Design-Build Stipulated Price
- Contract completion deadline: 2026-12-31
- Key features: 35' ceiling; (2) 5-ton overhead cranes; wash bay + mud sump; 50,000L cistern; septic holding tank; commissioning + closeout

## 3. Estimation Scope

- Scope baseline: `_Decomposition/WDMLRL_Decomposition_Claude.md` (117 deliverables).
- Foundation pricing is variable post-geotech; maintain allowances until geotechnical results confirm conditions.
- Permit fee payment responsibility requires confirmation (Owner vs Proponent).

## 4. Estimation Strategy

### 4.1 Default methods

- Design packages (PKG-001..PKG-007): effort-based costing via staff rates × LOE (default); fee-percent file provided as optional cross-check.
- Pre-construction (PKG-008..PKG-009): effort-based costing; treat permit fees as allowances only where Proponent-paid.
- Construction/installation (PKG-010..PKG-018): parametric unit rates + labour + equipment allowances; prioritize LOW-confidence items for quotes.
- Management/OH&S (PKG-019): staff effort + allowances for bonding/insurance/permits.
- Commissioning/closeout (PKG-020): staff effort + optional allowances register.
- Bonding/insurance/warranty (PKG-021): allowances + admin effort.

### 4.2 PRICE_SOURCES posture

- Scaffold snapshot: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035`
- Pricing entrypoint: `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/INDEX.md`
- Replace LOW-confidence allowances with vendor quotes early (cranes, overhead doors, MUA, 3-phase service).

### 4.3 Package cost ownership rules (anti-double-counting)

- Treat each `PKG-XXX` as the primary cost ownership boundary; avoid duplicating cross-cutting compliance (PKG-009) inside discipline packages.
- Where a package contains multiple deliverables forming one integrated drawing/spec set, allocate setup/coordination overhead once and distribute remaining effort logically.
- Coordinate crane (PKG-016) with structural runway/support (PKG-011) and electrical power feeds (PKG-015) to avoid duplicate carry.
- Foundation scope (PKG-010) remains allowance/variable until geotech; do not embed hard foundation totals elsewhere.

## 5. Per-Deliverable Estimation Plan

Every deliverable is assigned a tier (T0..Tn) derived from BLOCKING dependencies. Cyclic blocking dependencies are handled as SCC bundles (iterative, single tier).

### 5.1 Per-package PRICE_SOURCES (by file name)

All packages include base sources: `Professional_Staff_Rates.csv`, `Level_of_Effort.csv`, `Assumed_Project_Parameters.csv`. Extras are listed below.

| Package | Extra PRICE_SOURCES |
|---|---|
| PKG-001 Architectural Design | `Professional_Design_Fees.csv`, `Parametric_Building_Rates.csv` |
| PKG-002 Structural Design | `Professional_Design_Fees.csv` |
| PKG-003 Mechanical Design | `Professional_Design_Fees.csv` |
| PKG-004 Electrical Design | `Professional_Design_Fees.csv` |
| PKG-005 Civil Design | `Professional_Design_Fees.csv` |
| PKG-006 Plumbing Design | `Professional_Design_Fees.csv` |
| PKG-007 Landscape Architectural Design | `Professional_Design_Fees.csv` |
| PKG-008 Geotechnical Investigation & Surveying | `(none)` |
| PKG-009 Permitting & Regulatory Compliance | `(none)` |
| PKG-010 Foundation Construction | `Structural_Concrete_Rates.csv`, `Earthwork_Civil_Rates.csv`, `Construction_Labour_Rates.csv` |
| PKG-011 Building Structure & Envelope | `Structural_Concrete_Rates.csv`, `Building_Envelope_Rates.csv`, `Construction_Labour_Rates.csv`, `Equipment_Pricing.csv` |
| PKG-012 Interior Construction & Fit-Out | `Interior_Architectural_Rates.csv`, `Construction_Labour_Rates.csv` |
| PKG-013 Mechanical & HVAC Installation | `Mechanical_System_Rates.csv`, `Construction_Labour_Rates.csv`, `Equipment_Pricing.csv` |
| PKG-014 (Plumbing & Water Systems Installation) | `Underground_Utility_Rates.csv`, `Construction_Labour_Rates.csv`, `Equipment_Pricing.csv` |
| PKG-015 (Electrical & Low-Voltage Installation) | `Electrical_System_Rates.csv`, `Underground_Utility_Rates.csv`, `Construction_Labour_Rates.csv` |
| PKG-016 (Crane & Lifting Equipment) | `Equipment_Pricing.csv`, `Construction_Labour_Rates.csv` |
| PKG-017 (Existing Building Renovation - Old North Shop) | `Interior_Architectural_Rates.csv`, `Construction_Labour_Rates.csv` |
| PKG-018 (Sitework & Civil Construction) | `Earthwork_Civil_Rates.csv`, `Paving_Surfacing_Rates.csv`, `Underground_Utility_Rates.csv`, `Construction_Labour_Rates.csv` |
| PKG-019 — Construction Management & OH&S | `Fees_Permits_Insurance.csv` |
| PKG-020 — Commissioning & Closeout | `Optional_Items_Pricing.csv` |
| PKG-021 — Bonding, Insurance & Warranty | `Fees_Permits_Insurance.csv` |

### 5.2 Deliverables (grouped by package)


#### PKG-001 — Architectural Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-001-01 | Preliminary Architectural Design | T1 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-02 | Architectural Floor Plans | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-03 | Exterior Elevations | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-04 | Building Sections | T8 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-05 | Interior Elevations | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-06 | Reflected Ceiling Plans | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-07 | Door & Window Schedule | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-08 | Finish Schedule | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-09 | Old North Shop Demolition Plans | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-10 | Old North Shop Renovation Plans | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-11 | Architectural Specification | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-002 — Structural Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-002-01 | Preliminary Structural Design | T1 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-02 | Foundation Plan | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-03 | Structural Framing Plans | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-04 | Structural Sections & Details | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-05 | Mezzanine Framing Details | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-06 | Service Pit / Trench Structural Details | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-07 | Crane Support Structure Details | T7 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-08 | Steel Plate Embedment Plan | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-09 | Stair Details | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-10 | Structural Calculation Package | T1 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-11 | Foundation Design Package (Variable-Price) | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-12 | Structural Specification | T8 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-003 — Mechanical Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-003-01 | Preliminary Mechanical Design | T0 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-02 | HVAC Layout Plans | T8 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-03 | Ductwork & Distribution Plans | T9 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-04 | Exhaust System Plans | T8 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-05 | Mechanical Equipment Schedule | T7 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-06 | Mechanical Calculation Package | T7 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-07 | Mechanical Specification | T8 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-004 — Electrical Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-004-01 | Preliminary Electrical Design | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-02 | Single-Line Diagram | T7 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-03 | Power Distribution Plans | T7 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-04 | Lighting Plans | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-05 | Receptacle Layout Plans | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-06 | Panel Schedules | T7 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-07 | Low-Voltage System Plans | T8 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-08 | Electrical Calculation Package | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-09 | Electrical Specification | T8 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-005 — Civil Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-005-01 | Preliminary Civil Design | T1 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-02 | Site Grading Plan | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-03 | Drainage Plan | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-04 | Driving Surface & Pad Layout Plan | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-05 | Civil Sections & Details | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-06 | Civil Calculation Package | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-07 | Civil Specification | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-006 — Plumbing Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-006-01 | Preliminary Plumbing Design | T1 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-02 | Water Distribution Plans | T6 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-03 | Drain & Vent Plans | T5 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-04 | Cistern & Pump Details | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-05 | Septic System Details | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-06 | Plumbing Fixture Schedule | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-07 | Plumbing Calculation Package | T5 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-08 | Plumbing Specification | T6 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-007 — Landscape Architectural Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-007-01 | Preliminary Design | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-007-02 | Landscape Plans | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-007-03 | Planting Plans | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-007-04 | Specification | T5 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-008 — Geotechnical Investigation & Surveying

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-008-01 | Geotech Investigation | T0 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-008-02 | Preliminary Survey | T0 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-008-03 | Construction Survey | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-008-04 | As Built Survey | T5 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |

#### PKG-009 — Permitting & Regulatory Compliance

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-009-01 | Development Permit | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-009-02 | Building Permit | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-009-03 | Safety Code Permits | T5 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-009-04 | Code Compliance Register | T6 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |

#### PKG-010 — Foundation Construction

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-010-01 | Foundation Construction | T6 | PARAMETRIC | ALLOWANCE (variable-price foundation pending geotech) | YES | Construction |

#### PKG-011 — Building Structure & Envelope

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-011-01 | Concrete Superstructure | T8 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-02 | Steel Plate Floor Embedments | T9 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-03 | Drive-Through Repair Bays | T10 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-04 | Entrance/Exit Doors | T9 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-05 | Wash Bay Enclosure | T9 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-06 | Service Pit/Trench | T3 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-07 | Mezzanine Structure & Stairs | T10 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-012 — Interior Construction & Fit-Out

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-012-01 | Parts Storage Room - Context | T11 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-012-02 | Utility Room - Context | T10 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-012-03 | Office Space - Context | T4 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-013 — Mechanical & HVAC Installation

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-013-01 | High-Recovery Heating System - Context | T10 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-013-02 | High-Volume Air Exchanger - Context | T11 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-013-03 | Forced-Air Makeup System - Context | T12 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-013-04 | Heavy Equipment Exhaust System - Context | T11 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-013-05 | Welding Station Exhaust System - Context | T12 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-013-06 | Ceiling Fans - Context | T11 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-014 — (Plumbing & Water Systems Installation)

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-014-01 | Cistern | T11 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-014-02 | Septic | T3 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-014-03 | Bulk Water | T12 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-014-04 | Floor Drains | T11 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-014-05 | Emergency Shower | T12 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-014-06 | Fixtures | T12 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-015 — (Electrical & Low-Voltage Installation)

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-015-01 | Power Service | T0 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-015-02 | Lighting | T9 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-015-03 | Receptacles | T9 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-015-04 | Equipment Power | T7 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-015-05 | Low Voltage | T9 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-016 — (Crane & Lifting Equipment)

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-016-01 | Overhead Cranes | T7 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-017 — (Existing Building Renovation - Old North Shop)

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-017-01 | Kitchenette Reno | T6 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-017-02 | Mezzanine Reno | T0 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-017-03 | Washroom Reno | T6 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-017-04 | Locker Room | T6 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-018 — (Sitework & Civil Construction)

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-018-01 | Topsoil Strip | T3 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-018-02 | Grading Landscape | T6 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-018-03 | Driving Surface | T7 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-018-04 | Pads | T7 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-018-05 | Wash Bay Drainage | T10 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-018-06 | Utility Tieins | T8 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-019 — — Construction Management & OH&S

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-019-01 | Prime Contractor Designation & OH&S Program | T3 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-019-02 | Weekly Meetings & Billing Coordination | T4 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-019-03 | Subcontractor Management | T4 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-019-04 | Construction Quality Control | T4 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-020 — — Commissioning & Closeout

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-020-01 | Building Systems Commissioning | T5 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Commissioning/Closeout |
| DEL-020-02 | Final Inspection & CCC | T6 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Commissioning/Closeout |
| DEL-020-03 | Closeout Documentation | T7 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Commissioning/Closeout |

#### PKG-021 — — Bonding, Insurance & Warranty

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance |
|---|---|---:|---|---|---|---|
| DEL-021-01 | Bid Security Package | T0 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Contract/Insurance/Warranty |
| DEL-021-02 | Performance & Payment Bonds | T1 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Contract/Insurance/Warranty |
| DEL-021-03 | Insurance Package | T0 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Contract/Insurance/Warranty |
| DEL-021-04 | CCDC 14-2013 Contract Execution | T2 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Contract/Insurance/Warranty |
| DEL-021-05 | Guarantee Period Obligations | T7 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Contract/Insurance/Warranty |

## 6. Dependency-Informed Run Sequence

Use tiers to sequence estimation and readiness checks. Where a tier contains an SCC bundle (cycle), treat the bundle as an iterative coordination set within the tier.

### 6.1 Tier summary

| Tier | Count | Representative deliverables |
|---|---:|---|
| T0 | 7 | DEL-003-01, DEL-008-01, DEL-008-02, DEL-015-01, DEL-017-02, DEL-021-01, DEL-021-03 |
| T1 | 6 | DEL-001-01, DEL-002-01, DEL-002-10, DEL-005-01, DEL-006-01, DEL-021-02 |
| T2 | 18 | DEL-001-03, DEL-001-05, DEL-001-07, DEL-001-09, DEL-001-11, DEL-002-02, DEL-002-03, DEL-002-04, DEL-002-06, DEL-004-01, DEL-005-02, DEL-005-04 … |
| T3 | 12 | DEL-001-02, DEL-001-10, DEL-002-05, DEL-002-11, DEL-004-08, DEL-005-03, DEL-007-02, DEL-009-02, DEL-011-06, DEL-014-02, DEL-018-01, DEL-019-01 |
| T4 | 15 | DEL-001-06, DEL-001-08, DEL-002-08, DEL-002-09, DEL-004-04, DEL-004-05, DEL-005-05, DEL-006-04, DEL-006-06, DEL-007-03, DEL-008-03, DEL-012-03 … |
| T5 | 6 | DEL-006-03, DEL-006-07, DEL-007-04, DEL-008-04, DEL-009-03, DEL-020-01 |
| T6 | 9 | DEL-006-02, DEL-006-08, DEL-009-04, DEL-010-01, DEL-017-01, DEL-017-03, DEL-017-04, DEL-018-02, DEL-020-02 |
| T7 | 12 | DEL-002-07, DEL-003-05, DEL-003-06, DEL-004-02, DEL-004-03, DEL-004-06, DEL-015-04, DEL-016-01, DEL-018-03, DEL-018-04, DEL-020-03, DEL-021-05 |
| T8 | 9 | DEL-001-04, DEL-002-12, DEL-003-02, DEL-003-04, DEL-003-07, DEL-004-07, DEL-004-09, DEL-011-01, DEL-018-06 |
| T9 | 7 | DEL-003-03, DEL-011-02, DEL-011-04, DEL-011-05, DEL-015-02, DEL-015-03, DEL-015-05 |
| T10 | 5 | DEL-011-03, DEL-011-07, DEL-012-02, DEL-013-01, DEL-018-05 |
| T11 | 6 | DEL-012-01, DEL-013-02, DEL-013-04, DEL-013-06, DEL-014-01, DEL-014-04 |
| T12 | 5 | DEL-013-03, DEL-013-05, DEL-014-03, DEL-014-05, DEL-014-06 |

### 6.2 Cyclic SCC bundles (iterative)

- Tier T7: DEL-002-07, DEL-003-05, DEL-003-06, DEL-004-02, DEL-004-03, DEL-004-06, DEL-015-04, DEL-016-01, DEL-018-04
- Tier T1: DEL-002-01, DEL-002-10
- Tier T10: DEL-012-02, DEL-013-01
- Tier T12: DEL-013-03, DEL-013-05

## 7. Missing / Weak PRICE_SOURCES Register

LOW-confidence items from the scaffold snapshot should be prioritized for quote replacement.

| File | LOW rows | Example LOW items |
|---|---:|---|
| `Assumed_Project_Parameters.csv` | 0 | (none captured) |
| `Building_Envelope_Rates.csv` | 1 | BE-03 Overhead door, 24' class (supply + install) |
| `Construction_Labour_Rates.csv` | 0 | (none captured) |
| `Earthwork_Civil_Rates.csv` | 0 | (none captured) |
| `Electrical_System_Rates.csv` | 2 | ES-02 Panelboard supply + install, ES-03 3-phase service allowance |
| `Equipment_Pricing.csv` | 3 | EQ-01 Overhead crane, 5 ton class (supply + install), EQ-02 Pressure washer system allowance, EQ-03 Air compressor allowance |
| `Fees_Permits_Insurance.csv` | 1 | FP-05 Safety code / building permit fees allowance |
| `Interior_Architectural_Rates.csv` | 1 | IA-05 Basic casework allowance |
| `Mechanical_System_Rates.csv` | 5 | MS-01 Unit heater (gas), installed, MS-02 Make-up air unit (MUA), installed, MS-03 High-volume air exchanger, installed |
| `Optional_Items_Pricing.csv` | 2 | OPT-01 Allowance for winter conditions / heating / hoarding, OPT-02 Allowance for contaminated soils handling |
| `Parametric_Building_Rates.csv` | 1 | PB-02 Wash bay incremental premium allowance |
| `Paving_Surfacing_Rates.csv` | 0 | (none captured) |
| `Professional_Design_Fees.csv` | 0 | (none captured) |
| `Professional_Staff_Rates.csv` | 0 | (none captured) |
| `Structural_Concrete_Rates.csv` | 1 | SC-08 Embedded steel plates in slab (supply + install) |
| `Underground_Utility_Rates.csv` | 2 | UU-04 Septic holding tank (2,000 US gal) supply + set, UU-05 Cistern (50,000L) supply + set |

## 8. Aggregation Strategy

- Rollups: by Package (PKG-XXX) and by Deliverable (DEL-XXX-YY).
- Cost components: design effort (staff rates × LOE), construction allowances (unit-rate/equipment/labour), fees/permits/insurance, optional/contingency allowances.
- Maintain provenance: carry `Basis`/`Confidence`/`Source` fields through to estimate detail outputs.

## 9. Assumptions and Constraints Log

- Tiering uses BLOCKING deliverable-to-deliverable EXECUTION dependencies only.
- Package-level deliverable IDs (e.g., `DEL-003`) are mapped to representative deliverables for tiering (see Conflicts.csv).
- External constraints (e.g., County approvals) do not appear as deliverable nodes in the tier DAG.

## 10. Document Control

- Generated: `2026-02-26T21:41:34-07:00`
- Source scaffold: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035`
- Status: `DRAFT — requires human review`

