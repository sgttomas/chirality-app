# BASIS OF ESTIMATE — EPREP_BOE_WDMLRL_2026-02-26_2131

## 1. Purpose

This Basis of Estimate (BOE) defines the estimation strategy, PRICE_SOURCES posture, and dependency-informed run sequence for the WDMLRL Maintenance Shop Addition project. It does not compute totals; ESTIMATING consumes the input package to produce estimates.

## 2. Project Context

- Project: 2026 Design Build of West Dried Meat Lake Regional Landfill Maintenance Shop Addition
- Owner: Camrose County
- Location: near Ferintosh, Alberta (Central Alberta)
- Contract form: CCDC 14–2013 Design-Build Stipulated Price
- Contract completion deadline: 2026-12-31
- Key features: 35' ceiling concrete structure; (2) 5-ton overhead cranes; wash bay + mud sump; 50,000L cistern; septic holding tank; commissioning + closeout

## 3. Estimation Scope

- Scope baseline: `_Decomposition/WDMLRL_Decomposition_Claude.md` (Packages PKG-001..PKG-021; 117 deliverables).
- Variable-price scope: foundation pricing is negotiated post-geotechnical report; carry allowances until geotech confirms soil/frost conditions.
- Permit fee payment responsibility requires confirmation (Owner vs Proponent).

## 4. Estimation Strategy

### 4.1 Default methods

- **Design packages (PKG-001..PKG-007):** effort-based costing using `Professional_Staff_Rates.csv` × `Level_of_Effort.csv` (default). `Professional_Design_Fees.csv` is provided as an optional cross-check method.
- **Pre-construction (PKG-008..PKG-009):** effort-based costing; permit fees carried as allowances only where Proponent-paid.
- **Construction/installation (PKG-010..PKG-018):** parametric unit-rate libraries + construction labour rates + equipment allowances, with explicit LOW-confidence items prioritized for quotes.
- **Management/OH&S (PKG-019):** staff effort + allowances for bonding/insurance/permit fees as applicable.
- **Commissioning/closeout (PKG-020):** staff effort + optional allowances register.
- **Bonding/insurance/warranty (PKG-021):** allowances + admin effort.

### 4.2 PRICE_SOURCES posture

- Approved scaffold snapshot: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035`
- Pricing library entrypoint: `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/INDEX.md`
- Replace LOW-confidence allowances with quotes as soon as feasible (cranes, overhead doors, MUA, 3-phase power).

### 4.3 Package cost ownership rules (anti-double-counting)

- Treat each `PKG-XXX` as the primary cost ownership boundary; do not duplicate cross-cutting compliance (PKG-009) inside discipline packages.
- Where a package contains multiple deliverables that collectively form one integrated drawing/spec package, allocate setup/coordination overhead once and distribute remaining effort logically across the set.
- Coordinate crane (PKG-016) with structural runway/support (PKG-011) and electrical power feeds (PKG-015) to avoid duplicate carry.
- Foundation scope (PKG-010) is allowance/variable until geotech results; do not embed hard foundation totals elsewhere.

## 5. Per-Deliverable Estimation Plan

Every deliverable is assigned a tier (T0..Tn) derived from blocking dependencies. Basis/fallback/mixed-method fields come from the approved scaffold.

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

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-001-01 | Preliminary Architectural Design | T1 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-02 | Architectural Floor Plans | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-03 | Exterior Elevations | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-04 | Building Sections | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-05 | Interior Elevations | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-06 | Reflected Ceiling Plans | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-07 | Door & Window Schedule | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-08 | Finish Schedule | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-09 | Old North Shop Demolition Plans | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-10 | Old North Shop Renovation Plans | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-001-11 | Architectural Specification | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-002 — Structural Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-002-01 | Preliminary Structural Design | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-02 | Foundation Plan | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-03 | Structural Framing Plans | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-04 | Structural Sections & Details | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-05 | Mezzanine Framing Details | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-06 | Service Pit / Trench Structural Details | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-07 | Crane Support Structure Details | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-08 | Steel Plate Embedment Plan | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-09 | Stair Details | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-10 | Structural Calculation Package | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-11 | Foundation Design Package (Variable-Price) | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-002-12 | Structural Specification | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-003 — Mechanical Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-003-01 | Preliminary Mechanical Design | T0 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-02 | HVAC Layout Plans | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-03 | Ductwork & Distribution Plans | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-04 | Exhaust System Plans | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-05 | Mechanical Equipment Schedule | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-06 | Mechanical Calculation Package | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-003-07 | Mechanical Specification | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-004 — Electrical Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-004-01 | Preliminary Electrical Design | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-02 | Single-Line Diagram | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-03 | Power Distribution Plans | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-04 | Lighting Plans | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-05 | Receptacle Layout Plans | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-06 | Panel Schedules | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-07 | Low-Voltage System Plans | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-08 | Electrical Calculation Package | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-004-09 | Electrical Specification | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-005 — Civil Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-005-01 | Preliminary Civil Design | T1 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-02 | Site Grading Plan | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-03 | Drainage Plan | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-04 | Driving Surface & Pad Layout Plan | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-05 | Civil Sections & Details | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-06 | Civil Calculation Package | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-005-07 | Civil Specification | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-006 — Plumbing Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-006-01 | Preliminary Plumbing Design | T1 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-02 | Water Distribution Plans | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-03 | Drain & Vent Plans | T1 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-04 | Cistern & Pump Details | T0 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-05 | Septic System Details | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-06 | Plumbing Fixture Schedule | T0 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-07 | Plumbing Calculation Package | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-006-08 | Plumbing Specification | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-007 — Landscape Architectural Design

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-007-01 | Preliminary Design | T2 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-007-02 | Landscape Plans | T3 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-007-03 | Planting Plans | T4 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |
| DEL-007-04 | Specification | T5 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Design |

#### PKG-008 — Geotechnical Investigation & Surveying

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-008-01 | Geotech Investigation | T0 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-008-02 | Preliminary Survey | T0 | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-008-03 | Construction Survey | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-008-04 | As Built Survey | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |

#### PKG-009 — Permitting & Regulatory Compliance

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-009-01 | Development Permit | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-009-02 | Building Permit | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-009-03 | Safety Code Permits | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |
| DEL-009-04 | Code Compliance Register | TBD | PARAMETRIC | PARAMETRIC; upgrade with QUOTE/HUMAN_PROVIDED when available | YES | Preconstruction |

#### PKG-010 — Foundation Construction

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-010-01 | Foundation Construction | TBD | PARAMETRIC | ALLOWANCE (variable-price foundation pending geotech) | YES | Construction |

#### PKG-011 — Building Structure & Envelope

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-011-01 | Concrete Superstructure | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-02 | Steel Plate Floor Embedments | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-03 | Drive-Through Repair Bays | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-04 | Entrance/Exit Doors | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-05 | Wash Bay Enclosure | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-06 | Service Pit/Trench | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-011-07 | Mezzanine Structure & Stairs | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-012 — Interior Construction & Fit-Out

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-012-01 | Parts Storage Room - Context | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-012-02 | Utility Room - Context | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-012-03 | Office Space - Context | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-013 — Mechanical & HVAC Installation

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-013-01 | High-Recovery Heating System - Context | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-013-02 | High-Volume Air Exchanger - Context | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-013-03 | Forced-Air Makeup System - Context | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-013-04 | Heavy Equipment Exhaust System - Context | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-013-05 | Welding Station Exhaust System - Context | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-013-06 | Ceiling Fans - Context | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-014 — (Plumbing & Water Systems Installation)

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-014-01 | Cistern | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-014-02 | Septic | T3 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-014-03 | Bulk Water | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-014-04 | Floor Drains | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-014-05 | Emergency Shower | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-014-06 | Fixtures | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-015 — (Electrical & Low-Voltage Installation)

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-015-01 | Power Service | T0 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-015-02 | Lighting | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-015-03 | Receptacles | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-015-04 | Equipment Power | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-015-05 | Low Voltage | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-016 — (Crane & Lifting Equipment)

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-016-01 | Overhead Cranes | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-017 — (Existing Building Renovation - Old North Shop)

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-017-01 | Kitchenette Reno | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-017-02 | Mezzanine Reno | T0 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-017-03 | Washroom Reno | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-017-04 | Locker Room | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-018 — (Sitework & Civil Construction)

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-018-01 | Topsoil Strip | T3 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-018-02 | Grading Landscape | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-018-03 | Driving Surface | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-018-04 | Pads | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-018-05 | Wash Bay Drainage | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-018-06 | Utility Tieins | TBD | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-019 — — Construction Management & OH&S

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-019-01 | Prime Contractor Designation & OH&S Program | T3 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-019-02 | Weekly Meetings & Billing Coordination | T4 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-019-03 | Subcontractor Management | T4 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |
| DEL-019-04 | Construction Quality Control | T4 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Construction |

#### PKG-020 — — Commissioning & Closeout

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-020-01 | Building Systems Commissioning | T0 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Commissioning/Closeout |
| DEL-020-02 | Final Inspection & CCC | T0 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Commissioning/Closeout |
| DEL-020-03 | Closeout Documentation | T1 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Commissioning/Closeout |

#### PKG-021 — — Bonding, Insurance & Warranty

| DeliverableID | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Notes |
|---|---|---:|---|---|---|---|
| DEL-021-01 | Bid Security Package | T0 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Contract/Insurance/Warranty |
| DEL-021-02 | Performance & Payment Bonds | T1 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Contract/Insurance/Warranty |
| DEL-021-03 | Insurance Package | T0 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Contract/Insurance/Warranty |
| DEL-021-04 | CCDC 14-2013 Contract Execution | T2 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Contract/Insurance/Warranty |
| DEL-021-05 | Guarantee Period Obligations | T3 | PARAMETRIC | ALLOWANCE for vendor/unknown items; PARAMETRIC otherwise | YES | Contract/Insurance/Warranty |

## 6. Dependency-Informed Run Sequence

Tiering is derived from the blocking dependency DAG (see `Tier_Analysis.md`). Use tiers to sequence estimation and document production readiness checks.

### 6.1 Tier summary

| Tier | Count | Representative deliverables |
|---|---:|---|
| T0 | 11 | DEL-003-01, DEL-006-04, DEL-006-06, DEL-008-01, DEL-008-02, DEL-015-01, DEL-017-02, DEL-020-01, DEL-020-02, DEL-021-01 … |
| T1 | 6 | DEL-001-01, DEL-005-01, DEL-006-01, DEL-006-03, DEL-020-03, DEL-021-02 |
| T2 | 13 | DEL-001-03, DEL-001-05, DEL-001-07, DEL-001-09, DEL-001-11, DEL-004-01, DEL-005-02, DEL-005-04, DEL-005-06, DEL-005-07 … |
| T3 | 8 | DEL-001-10, DEL-004-08, DEL-005-03, DEL-007-02, DEL-014-02, DEL-018-01, DEL-019-01, DEL-021-05 |
| T4 | 5 | DEL-005-05, DEL-007-03, DEL-019-02, DEL-019-03, DEL-019-04 |
| T5 | 1 | DEL-007-04 |

### 6.2 Notable gating chains (best-effort)

- Early tiers are expected to include geotechnical/survey and preliminary design approvals that unlock IFC design packages.
- Construction packages are sequenced after design deliverables where explicit blocking prerequisites exist; otherwise they remain parallelizable by tier.

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

- Primary rollups: by Package (PKG-XXX) and by Deliverable (DEL-XXX-YY).
- Cost components: design effort (staff rates × LOE), construction allowances (unit-rate/equipment/labour), fees/permits/insurance, and optional/contingency allowances.
- Maintain provenance: carry `Basis`/`Confidence`/`Source` fields through to estimate detail outputs.

## 9. Assumptions and Constraints Log

See scaffold snapshot logs for baseline assumptions. BOE-specific assumptions include:

- Tiering uses **BLOCKING** deliverable-to-deliverable EXECUTION dependencies only; advisory/interface coordination edges not marked BLOCKING are not enforced by tiers.
- External constraints (e.g., County approval gates) are tracked as constraints but do not appear as deliverable nodes in the tier DAG.

## 10. Document Control

- Generated: `2026-02-26T21:35:27-07:00`
- Source scaffold: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035`
- Dependency source: per-deliverable `Dependencies.csv` (AUTO)
- Status: `DRAFT — requires human review`

