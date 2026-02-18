# Basis of Estimate (BOE) — Penhold Public Services Building
## Human-Authored Strategy Document for ESTIMATING Runs

**Project:** Town of Penhold — Public Services Building (PSB)
**Decomposition:** `Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md`
**Currency:** CAD
**Base Year:** 2024
**Prepared:** 2026-02-18
**Status:** DRAFT — Pending human review and approval

---

## 1. Purpose

This document is the **human-authored Basis of Estimate** that governs all ESTIMATING agent runs for the Penhold PSB project. It establishes:

- The estimation strategy (per-deliverable runs with aggregation)
- Per-deliverable `BASIS_OF_ESTIMATE` and substance classification
- Dependency-informed estimation ordering (which deliverables to estimate first)
- Cost ownership rules to prevent double-counting across deliverables
- A complete register of missing PRICE_SOURCES that must be assembled before meaningful estimates can be produced
- Aggregation strategy for rolling up deliverable-level estimates to package and project totals

This document is **not** an estimate. It is the strategy input that makes estimates producible, auditable, and free of structural double-counting.

---

## 2. Project Context

| Field | Value |
|-------|-------|
| Delivery model | Design-Build (CCDC 14-2013) |
| Owner | Town of Penhold, Alberta |
| Scope | Integrated Public Services Building (Fire + Public Works), Cold Storage Building (60'x100'), Site/Civil Works, Optional Items |
| Packages | 6 (PKG-001 through PKG-006) |
| Deliverables | 31 |
| Currency | CAD |
| Base year | 2024 |
| Decomposition source | `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` |
| Dependency evidence | `Dependencies.csv` per deliverable (31 files; DEPENDENCIES pass completed) |

### Key project decisions affecting estimating

| DecisionID | Decision | Estimating Impact |
|------------|----------|-------------------|
| DEC-001 | Cold storage size = 60'x100' clear-span | Defines building area for parametric/rate-table pricing |
| DEC-002 | Cold storage floor = DB proposes one solution | DB freedom; estimate should carry DB's preferred solution |
| DEC-003 | Cold storage foundation = DB proposes | DB freedom; estimate should carry DB's preferred solution |
| DEC-004 | Utility tie-ins = cash allowance (excluded from base, no value pre-set) | DEL-03-04 must split: design/coordination at RATE_TABLE; tie-in execution at ALLOWANCE with TBD value |
| DEC-005 | FF&E = $20,000 cash allowance, DB-allocated | Fixed allowance; DEL-05-07 = $20,000 CAD (no estimating needed beyond recording) |
| DEC-006 | Pickled sand storage removed from procurement | PKG-006 = no cost content; DEL-06-01 is a tracking register only |

---

## 3. Estimation Strategy

### 3.1 Run granularity: Per-deliverable

ESTIMATING will be run **once per deliverable** (31 runs). Results are aggregated by AGGREGATION into package-level and project-level totals.

**Rationale:**
- Per-deliverable runs align with the decomposition's "deliverable = unit of production" model
- Each deliverable has its own Dependencies.csv, enabling deliverable-specific blocker detection
- Different deliverables within the same package may require different `BASIS_OF_ESTIMATE` (e.g., DEL-03-04 mixes RATE_TABLE and ALLOWANCE)
- Per-deliverable snapshots are independently auditable and rerunnable without disturbing others
- AGGREGATION handles rollup, so no information is lost

### 3.2 Separation of base vs optional scope

| Classification | Packages | Treatment |
|----------------|----------|-----------|
| **Base scope** | PKG-001, PKG-002, PKG-003, PKG-004 | Included in base price total |
| **Optional scope** (separately priced) | PKG-005 (DEL-05-01 through DEL-05-06) | Each option priced separately; NOT included in base total |
| **Cash allowance** (fixed value, separately carried) | PKG-005 (DEL-05-07: FF&E $20k) | Fixed at $20,000 CAD; record only |
| **No cost content** | PKG-006 (DEL-06-01) | Exclusions register; no ESTIMATING run |

### 3.3 Common run parameters (all deliverables)

```
CURRENCY: CAD
RUN_ROOT: {EXECUTION_ROOT}
ESTIMATES_ROOT: {EXECUTION_ROOT}/_Estimates/
DECOMPOSITION_PATH: {EXECUTION_ROOT}/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md
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
| **T0** | No upstream cost dependencies; estimate independently | Can run immediately once PRICE_SOURCES assembled |
| **T1** | Foundational; drives quantities for downstream deliverables | Run early; outputs inform Tier 2+ estimates |
| **T2** | Depends on Tier 1 area/quantity basis | Run after Tier 1 design parameters are established |
| **T3** | Depends on Tier 2 system characterization | Run after Tier 2 outputs are available |
| **T4** | Depends on base building/site design | Run last; all base scope must be characterized |
| **N/A** | No ESTIMATING run | Tracking/register deliverable only |

---

### PKG-001 — General Requirements & Delivery Controls

**Package estimating character:** Process/management scope. All deliverables are staffing-driven (person-hours x hourly rates x project duration). No physical quantities. Independent of other packages' design outputs for cost estimation purposes.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-01-01 | Integrated Design Management & Submission Packages | T0 | RATE_TABLE | STRICT | FALSE | Management | PM + discipline lead hours; design review costs; QA/QC hours |
| DEL-01-02 | Baseline Schedule, Updates & Reporting | T0 | RATE_TABLE | STRICT | FALSE | Management | Scheduler hours; software/tools; monthly reporting hours |
| DEL-01-03 | Health & Safety Plan | T0 | RATE_TABLE | STRICT | FALSE | Management | Safety officer hours; training costs; PPE/signage supplies |
| DEL-01-04 | Permitting, Inspections & AHJ Coordination | T0 | RATE_TABLE | ALLOW_ALLOWANCE | TRUE | Management + Fees | Coordinator hours + permit fees (allowance for fees if schedule unknown) |
| DEL-01-05 | Meetings, Documentation & Change Control | T0 | RATE_TABLE | STRICT | FALSE | Management | PM + admin hours; document control system costs |
| DEL-01-06 | Site Supervision, Logistics & Housekeeping | T0 | RATE_TABLE | STRICT | FALSE | Management | Site superintendent salary; temp facilities/fencing/cleaning |
| DEL-01-07 | Commissioning, Closeout & Warranty | T0 | RATE_TABLE | STRICT | FALSE | Management | Cx coordinator hours; as-built prep; training delivery; warranty admin |

**PKG-001 PRICE_SOURCES needed:**
- [ ] DB internal rate table (PM, superintendent, scheduler, safety officer, Cx coordinator, admin — hourly or monthly rates)
- [ ] Assumed project duration (months) for duration-dependent costs
- [ ] Permit fee schedule (Town of Penhold building permit fees; utility connection fees; development permit fees)
- [ ] Temporary facilities/equipment rental rates (temp fencing, site office if applicable, temp power)

**PKG-001 cost ownership rules:**
- All project-level management and coordination costs are carried in PKG-001
- Discipline-specific design hours (architectural, structural, mechanical, electrical, civil) are NOT in PKG-001; they are embedded in PKG-002/003/004 discipline deliverables
- Commissioning costs in DEL-01-07 cover overall Cx coordination and closeout administration; system-specific commissioning labor (e.g., mechanical balancing, electrical testing) is carried in the respective PKG-002 discipline deliverable

---

### PKG-002 — Main Public Services Building (PSB)

**Package estimating character:** Core construction scope. Discipline-organized deliverables covering architectural, functional areas, structural/envelope, mechanical, electrical, and emergency power. Area-driven and system-driven quantities.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-02-01 | Architectural Program, Layout & Code Planning | T1 | RATE_TABLE | STRICT | FALSE | Design + Construction | Architectural design fees; interior partitions; doors/frames/hardware; finishes (sealed concrete floors, ceiling system); accessibility features; code-required signage |
| DEL-02-02 | Firehall Apparatus Bays & Support Spaces | T2 | RATE_TABLE | ALLOW_ALLOWANCE | TRUE | Construction + Equipment | Bay fit-up; decon area; gear lockers (40 units); breathing air compressor; equipment storage; bay display systems |
| DEL-02-03 | Public Works Shop Bays & Support Spaces | T2 | RATE_TABLE | ALLOW_ALLOWANCE | TRUE | Construction + Equipment | Shop bay fit-up; workshop equipment; PPE/locker room (40 lockers); warehouse storage; shop office/washroom |
| DEL-02-04 | Structure, Envelope, Roof & Overhead Doors | T2 | RATE_TABLE | STRICT | FALSE | Construction | Structural steel/concrete; foundations; building envelope (walls, insulation, cladding); roof system (solar-ready); overhead doors (16'x16' with windows, motorized, car-wash grade); resilient flooring strategy |
| DEL-02-05 | Mechanical, Plumbing, Ventilation & Exhaust | T3 | RATE_TABLE | STRICT | FALSE | Construction + Systems | HVAC system; apparatus bay direct exhaust; PW bay ventilation; plumbing distribution; bay sumps (all bays); water fill stations (2); fire protection if required |
| DEL-02-06 | Electrical Power, Lighting, IT/Telecom & PA | T3 | RATE_TABLE | STRICT | FALSE | Construction + Systems | Electrical distribution; panel boards; receptacles; LED lighting (IES); IT/data cabling; telecom; PA system; emergency lighting; bay display systems; meeting room 15-workstation connectivity |
| DEL-02-07 | Emergency Power & Backup Generator | T3 | QUOTE | ALLOW_ALLOWANCE | TRUE | Equipment + Installation | Diesel generator (sized to essentials); ATS; distribution; fuel tank (72-hr TBD); installation; pad; exhaust; door backup mechanism integration |

**PKG-002 PRICE_SOURCES needed:**
- [ ] Structural steel and concrete unit rates (Alberta 2024 market)
- [ ] Building envelope systems pricing (pre-engineered metal building cladding, insulation, roofing)
- [ ] Overhead door supplier quotes (16'x16', motorized, car-wash grade hardware, with windows) — 8 doors minimum for main building
- [ ] Mechanical system rates (HVAC $/sf, plumbing $/sf, apparatus bay exhaust systems, vehicle exhaust extraction systems)
- [ ] Electrical system rates ($/sf power, $/sf lighting, IT/telecom $/drop)
- [ ] Generator vendor quote (diesel genset sized for essentials: kitchen, meeting/command room, 2 bathrooms; 72-hr runtime TBD)
- [ ] ATS (automatic transfer switch) pricing
- [ ] Breathing air compressor system quote
- [ ] Bunker gear locker pricing (40 units)
- [ ] PW locker pricing (40 units)
- [ ] Bay sump assemblies pricing (8+ sumps: 4 fire + 4 PW minimum)
- [ ] Water fill station assemblies (2-inch, 2 units)
- [ ] PA system pricing (building-wide simple system)
- [ ] Display system pricing (apparatus bay wall-mounted displays)
- [ ] Architectural design fees (if not carried separately as DB internal cost)
- [ ] Structural engineering design fees
- [ ] Mechanical engineering design fees
- [ ] Electrical engineering design fees

**PKG-002 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Architectural design + interior construction (partitions, finishes, doors) | DEL-02-01 | DEL-02-02, DEL-02-03 |
| Fire bay functional fit-up (gear lockers, decon, breathing air, compressed air equip) | DEL-02-02 | DEL-02-05, DEL-02-06 |
| PW bay functional fit-up (workshop equip, PPE lockers, storage) | DEL-02-03 | DEL-02-05, DEL-02-06 |
| Compressed air EQUIPMENT (compressor, piping, drops) | DEL-02-02 | DEL-02-05 (CON-M-01 resolved: equipment with firehall) |
| Compressed air ELECTRICAL FEED | DEL-02-06 | DEL-02-02 |
| Overhead doors (hardware, frames, openers) | DEL-02-04 | DEL-02-02, DEL-02-03 |
| Overhead door BACKUP POWER mechanism | DEL-02-07 | DEL-02-04 |
| Building structure, envelope, roof, foundations | DEL-02-04 | All others |
| Floor slab (structural element) | DEL-02-04 | DEL-02-05 |
| Sump ROUGH-IN (embedded in slab) | DEL-02-04 | DEL-02-05 |
| Sump ASSEMBLIES + PLUMBING connections | DEL-02-05 | DEL-02-04 |
| HVAC system (equipment, ductwork, controls) | DEL-02-05 | DEL-02-02, DEL-02-03 |
| Apparatus bay exhaust SYSTEMS (extraction units) | DEL-02-05 | DEL-02-02 |
| Electrical distribution (panels, feeders, branch circuits) | DEL-02-06 | All others |
| Lighting (fixtures, controls) | DEL-02-06 | All others |
| IT/telecom (cabling, drops, racks, connectivity) | DEL-02-06 | DEL-02-01 |
| PA system (equipment + wiring) | DEL-02-06 | All others |
| Bay display systems (screens + mounting + connectivity) | DEL-02-06 | DEL-02-02 |
| Meeting room EM workstation infrastructure (power + data) | DEL-02-06 | DEL-02-01 |
| Generator (genset, fuel, ATS, pad, exhaust, distribution to essential loads) | DEL-02-07 | DEL-02-06 |
| Normal power distribution TO generator transfer point | DEL-02-06 | DEL-02-07 |
| System-specific commissioning labor (mechanical balancing, electrical testing) | Each discipline DEL | DEL-01-07 |
| Discipline-specific design fees | Each discipline DEL | PKG-001 |

---

### PKG-003 — Site & Civil Works

**Package estimating character:** Construction scope driven by site areas, earthwork volumes, linear quantities (utilities, paving), and regulatory compliance costs.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-03-01 | Site Plan, Circulation, Parking & Operational Layout | T1 | RATE_TABLE | STRICT | FALSE | Design + Construction | Civil design fees; site layout/survey; parking lot construction (light duty asphalt area); access road (heavy duty asphalt area for fire apparatus) |
| DEL-03-02 | Grading, Earthworks, Drainage & Stormwater | T2 | RATE_TABLE | STRICT | FALSE | Construction | Clearing/stripping; cut/fill volumes; building pad prep; drainage infrastructure; erosion control; stormwater management (no storm sewer — overland drainage) |
| DEL-03-03 | Pavements, Aggregate & Concrete Aprons | T2 | RATE_TABLE | STRICT | FALSE | Construction | Heavy duty asphalt (fire route); light duty asphalt (parking); aggregate yard areas; concrete aprons at all overhead doors |
| DEL-03-04 | Site Utilities Distribution & Allowance-Based Tie-Ins | T3 | RATE_TABLE | ALLOW_ALLOWANCE | TRUE | Construction + Allowance | On-site utility distribution (water, sewer, gas, power, telecom routing) at RATE_TABLE; tie-in to municipal stubs at ALLOWANCE (DEC-004) |
| DEL-03-05 | Environmental Constraints & Flood Hazard Compliance | T1 | RATE_TABLE | ALLOW_ALLOWANCE | TRUE | Professional Services + Compliance | Environmental consultant fees; flood hazard assessment; wetland setback compliance; AEPA coordination; regulatory application fees (allowance if unknown) |

**PKG-003 PRICE_SOURCES needed:**
- [ ] Earthwork unit rates (clearing $/acre, stripping $/m3, cut/fill $/m3, compaction $/m3) — Alberta 2024
- [ ] Heavy duty asphalt rate ($/m2, Alberta municipal spec for fire apparatus loading)
- [ ] Light duty asphalt rate ($/m2, parking lot spec)
- [ ] Aggregate surfacing rate ($/m2, yard areas)
- [ ] Concrete apron rate ($/m2, reinforced, designed for service vehicle loads)
- [ ] Underground utility rates (water main $/lm, sewer $/lm, gas $/lm, power duct bank $/lm, telecom $/lm)
- [ ] Civil engineering design fees
- [ ] Environmental consultant fees (flood hazard assessment, wetland assessment update, AEPA application)
- [ ] Survey/staking fees
- [ ] Erosion and sediment control rates
- [ ] Geotechnical investigation fees (already completed? — report exists in _Sources/references)
- [ ] Municipal permit and utility connection fees (Town of Penhold)
- [ ] **TBD: Utility tie-in allowance value** (DEC-004 states "no value pre-set" — Owner must set or DB must propose)

**PKG-003 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Site layout design (civil engineering) | DEL-03-01 | DEL-03-02, DEL-03-03 |
| Clearing, stripping, earthworks, grading, drainage | DEL-03-02 | DEL-03-01, DEL-03-03 |
| Building pad preparation (main building + cold storage) | DEL-03-02 | PKG-002, PKG-004 |
| Stormwater management infrastructure | DEL-03-02 | DEL-03-05 |
| Environmental compliance COSTS (consultant fees, regulatory fees) | DEL-03-05 | DEL-03-02 |
| Environmental constraint INTEGRATION into design (no extra cost; design constraint) | DEL-03-05 | DEL-03-02 |
| Pavement construction (all types) | DEL-03-03 | DEL-03-01, DEL-03-02 |
| Concrete aprons at overhead doors | DEL-03-03 | PKG-002, PKG-004 |
| On-site utility distribution (pipe/conduit from tie-in point to buildings) | DEL-03-04 | PKG-002 |
| Utility TIE-IN to municipal stubs (allowance) | DEL-03-04 | All others |
| Building service ENTRY (from 1.5m outside building to interior) | PKG-002 (DEL-02-05/02-06) | DEL-03-04 |
| **Demarcation point:** 1.5m outside building foundation wall | PKG-003 side = DEL-03-04 | PKG-002 side = discipline DELs |

**CRITICAL: Utility tie-in allowance (DEC-004)**
- The tie-in execution cost is explicitly excluded from base price and carried as a cash allowance
- The allowance VALUE is not pre-set — this must be established before estimating
- DB is still responsible for design coordination of tie-ins (design hours in DEL-03-04 at RATE_TABLE)
- The ESTIMATING run for DEL-03-04 should carry two line item categories:
  1. `Method=RATE_TABLE`: design coordination, on-site distribution piping/conduit
  2. `Method=ALLOWANCE`: tie-in execution labor/materials (value = TBD until Owner/DB agree)

---

### PKG-004 — Cold Storage Building (Unheated, 60'x100')

**Package estimating character:** Simpler construction scope. Pre-engineered metal building with minimal MEP. Good candidate for parametric estimating ($/sf) with rate-table backup for individual components.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-04-01 | Cold Storage — Design Basis & Configuration | T2 | PARAMETRIC | ALLOW_ALLOWANCE | TRUE | Construction | Pre-engineered clear-span metal building (6,000 sf); framing; cladding; insulation (none — unheated); coordination with main building aesthetics |
| DEL-04-02 | Cold Storage — Doors, Openings & Hardware | T2 | RATE_TABLE | STRICT | FALSE | Construction + Equipment | 2 overhead doors (16'x16', windows, motorized, standard grade); 2 person doors; hardware |
| DEL-04-03 | Cold Storage — Floor & Foundation | T2 | RATE_TABLE | STRICT | FALSE | Construction | Foundation system (DB-proposed, code-compliant, cost-effective); floor slab or gravel (DB-proposed single solution) |
| DEL-04-04 | Cold Storage — Electrical & Ventilation | T3 | RATE_TABLE | STRICT | FALSE | Construction + Systems | Basic lighting; basic power/receptacles; ventilation/air circulation (condensation/icing prevention); door opener electrical |

**PKG-004 PRICE_SOURCES needed:**
- [ ] Pre-engineered metal building pricing (60'x100' clear-span, unheated, Alberta 2024) — vendor quote preferred, or parametric $/sf
- [ ] Overhead door pricing (16'x16', motorized, standard grade, with windows) — 2 units
- [ ] Person door pricing (commercial steel, 2 units)
- [ ] Foundation system options (shallow spread footings vs slab-on-grade vs screw piles — DB to propose; need unit rates for preferred option)
- [ ] Floor system options (concrete slab vs compacted gravel — DB to propose; need $/sf for preferred option)
- [ ] Basic electrical rates (lighting + power for unheated storage; minimal fixtures)
- [ ] Ventilation/air circulation system for condensation prevention (ridge vents, gable fans, or similar)
- [ ] Geotechnical bearing capacity data (available in existing geotech report in _Sources/references)

**PKG-004 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Building shell (framing, cladding, roof) | DEL-04-01 | DEL-04-02, DEL-04-03, DEL-04-04 |
| Doors, openings, hardware | DEL-04-02 | DEL-04-01, DEL-04-04 |
| Foundation + floor system | DEL-04-03 | DEL-04-01 |
| Electrical + ventilation systems | DEL-04-04 | DEL-04-01 |
| Door opener electrical feeds | DEL-04-04 | DEL-04-02 |
| Building pad preparation and grading | PKG-003 (DEL-03-02) | PKG-004 |
| Concrete aprons at cold storage overhead doors | PKG-003 (DEL-03-03) | PKG-004 |
| Site utility service TO cold storage building | PKG-003 (DEL-03-04) | PKG-004 |
| Utility service ENTRY into cold storage building | DEL-04-04 | DEL-03-04 |

---

### PKG-005 — Optional Priced Items & Owner-Elected Additions

**Package estimating character:** Mixed. Each option is independently priced and presented separately from base scope. Options range from equipment procurement (quotes) to system installation (rates) to fixed allowances.

| DEL | Name | Tier | BASIS_OF_ESTIMATE | FALLBACK_POLICY | ALLOW_MIXED | Substance | Cost Drivers |
|-----|------|------|-------------------|-----------------|-------------|-----------|-------------|
| DEL-05-01 | Option — Built-in Wash Bay | T4 | QUOTE | ALLOW_ALLOWANCE | TRUE | Equipment + Construction | Wash bay equipment; containment system; drainage/plumbing; HVAC modifications; installation; requires PW bay layout (DEL-02-03) |
| DEL-05-02 | Option — Yard Lighting (Per Light) | T4 | RATE_TABLE | STRICT | FALSE | Equipment + Installation | Unit rate per pole/fixture installed; conduit/wiring per pole; base/foundation per pole. Price as UNIT RATE (per light) per RFP. |
| DEL-05-03 | Option — Access Control | T4 | QUOTE | ALLOW_ALLOWANCE | TRUE | System | Access control system (readers, controllers, software, wiring); zone mapping; installation; commissioning |
| DEL-05-04 | Option — Security & Camera System | T4 | QUOTE | ALLOW_ALLOWANCE | TRUE | System | Camera system (cameras, NVR, switches, cabling); installation cost SEPARATE from monitoring cost per RFP |
| DEL-05-05 | Option — Town Branding Signage | T4 | QUOTE | ALLOW_ALLOWANCE | TRUE | Equipment + Installation | Fabricated signage; mounting/structural; electrical if illuminated (TBD); installation |
| DEL-05-06 | Option — Appliances & Laundry | T4 | QUOTE | STRICT | FALSE | Equipment + Installation | 2 refrigerators w/ freezers, 2 microwaves, stove/oven/range hood, dishwasher, 2 residential laundry sets; installation/connection |
| DEL-05-07 | Cash Allowance — FF&E ($20k) | T4 | ALLOWANCE | STRICT | FALSE | Allowance | Fixed $20,000 CAD cash allowance. DB allocates: Meeting/Training $8k; Lunchroom $6k; Reception $3k; Misc $3k. No estimating required beyond recording. |

**PKG-005 PRICE_SOURCES needed:**
- [ ] Wash bay equipment vendor quote (bay equipment, containment, water treatment/recycling if required)
- [ ] Wash bay plumbing/drainage modification costs
- [ ] Environmental regulatory requirements for wash bay effluent (may affect equipment selection)
- [ ] Yard lighting unit rate (pole + fixture + base + wiring per unit, installed; LED, IES-compliant)
- [ ] Number of yard lights (site layout must define fence line perimeter and spacing — TBD from DEL-03-01)
- [ ] Access control system vendor quote (multi-zone, main building only; readers, controllers, software license, wiring)
- [ ] Number of controlled zones/doors (from DEL-02-01 floor plan — TBD)
- [ ] Security camera system vendor quote (interior + exterior, main building; cameras, NVR, network, cabling)
- [ ] Security monitoring annual cost (separately stated per RFP)
- [ ] Number of camera locations (from DEL-02-01 floor plan — TBD)
- [ ] Town of Penhold branding guidelines (logos, colors, dimensions) — **PENDING; not in RFP**
- [ ] Signage fabrication vendor quote (depends on branding guidelines)
- [ ] Illuminated vs non-illuminated signage decision (TBD)
- [ ] Appliance pricing (retail/commercial: refrigerators, microwaves, stove/oven/range hood, dishwasher, laundry sets — 2024 CAD)
- [ ] Appliance installation/connection labor rates

**PKG-005 cost ownership rules:**

| Scope Area | Cost Owner | NOT in |
|------------|-----------|--------|
| Wash bay equipment + containment + dedicated plumbing | DEL-05-01 | DEL-02-03, DEL-02-05 |
| Base building bay sumps (exist whether or not wash bay is elected) | DEL-02-05 | DEL-05-01 |
| Base building mechanical rough-in to wash bay location | DEL-02-05 | DEL-05-01 |
| Wash bay DEDICATED equipment beyond base rough-in | DEL-05-01 | DEL-02-05 |
| Yard lighting (all pole/fixture/wiring costs) | DEL-05-02 | DEL-02-06 |
| Electrical service point for yard lighting (panel/breaker at building) | DEL-02-06 | DEL-05-02 |
| Access control system (all equipment + wiring + installation) | DEL-05-03 | DEL-02-06 |
| IT network infrastructure that access control connects TO | DEL-02-06 | DEL-05-03 |
| Camera system (all equipment + wiring + installation) | DEL-05-04 | DEL-02-06 |
| Camera system monitoring service (annual) | DEL-05-04 | All others |
| Branding signage (fabrication + mounting + electrical if illuminated) | DEL-05-05 | DEL-02-01, DEL-02-04 |
| Code-required signage (exits, accessibility, fire, room ID) | DEL-02-01 | DEL-05-05 |
| Appliances (equipment purchase + delivery) | DEL-05-06 | DEL-05-07 |
| Appliance installation (plumbing/electrical connections) | DEL-05-06 | DEL-02-05, DEL-02-06 |
| Base building kitchen/laundry rough-in (plumbing stubs, electrical circuits) | DEL-02-05 / DEL-02-06 | DEL-05-06 |
| **FF&E (furniture, fixtures, equipment — loose items)** | **DEL-05-07** | **DEL-05-06** |
| **Appliances (fixed/connected equipment)** | **DEL-05-06** | **DEL-05-07** |

**CRITICAL: DEL-05-06 / DEL-05-07 boundary (explicit double-counting prevention)**
- DEL-05-06 covers **connected appliances** (items requiring plumbing or dedicated electrical connection: refrigerators, stove, dishwasher, laundry)
- DEL-05-07 covers **loose FF&E** (furniture, fixtures, equipment that plug into standard receptacles or require no connection: tables, chairs, whiteboards, coat racks, etc.)
- The $20,000 FF&E allowance in DEL-05-07 must NOT include any items that appear in the DEL-05-06 appliance list
- If an item is ambiguous (e.g., microwave — plugs in but listed in appliance spec), it belongs in DEL-05-06 per OSR S12.6

---

### PKG-006 — Exclusions & Interfaces (Tracked)

| DEL | Name | Tier | BASIS_OF_ESTIMATE | Notes |
|-----|------|------|-------------------|-------|
| DEL-06-01 | Exclusions & Interfaces Register | N/A | N/A | No ESTIMATING run. This is a tracking register for excluded scope (pickled sand storage) and interface management. Zero cost content. |

---

## 5. Dependency-Informed Run Sequence

Runs should be executed in tier order. Within a tier, runs are independent and may be parallelized.

### Sequence

```
TIER 0 (run immediately; no design dependencies):
  DEL-01-01, DEL-01-02, DEL-01-03, DEL-01-04, DEL-01-05, DEL-01-06, DEL-01-07
  [7 parallel runs]

TIER 1 (foundational — run next; drives quantities for later tiers):
  DEL-02-01, DEL-03-01, DEL-03-05
  [3 parallel runs]

TIER 2 (depends on Tier 1 area/quantity basis):
  DEL-02-02, DEL-02-03, DEL-02-04, DEL-03-02, DEL-03-03, DEL-04-01, DEL-04-02, DEL-04-03
  [8 parallel runs]

TIER 3 (depends on Tier 2 system characterization):
  DEL-02-05, DEL-02-06, DEL-02-07, DEL-03-04, DEL-04-04
  [5 parallel runs]

TIER 4 (depends on base building/site design):
  DEL-05-01, DEL-05-02, DEL-05-03, DEL-05-04, DEL-05-05, DEL-05-06, DEL-05-07
  [7 parallel runs]

NO RUN:
  DEL-06-01
```

**Total: 30 ESTIMATING runs across 5 tiers (DEL-06-01 excluded)**

### Tier dependencies (what must be resolved before next tier runs)

| Before Tier | Must Have |
|-------------|----------|
| T0 → T1 | PRICE_SOURCES for management rates; assumed project duration |
| T1 → T2 | Building footprint/area from DEL-02-01; site layout areas from DEL-03-01; environmental constraints confirmed from DEL-03-05 |
| T2 → T3 | Bay layouts from DEL-02-02/03; structural system from DEL-02-04; earthwork quantities from DEL-03-02; cold storage configuration from DEL-04-01 |
| T3 → T4 | Mechanical/electrical system definitions; utility distribution plan; generator sizing |
| T4 (run) | Base building design sufficiently characterized; Owner election decisions for optional items |

### External gates that block meaningful estimating

| Gate | Blocks | Status | Impact |
|------|--------|--------|--------|
| AEPA Water Act approval | DEL-03-02 earthwork quantities near waterway | PENDING | If unresolved, carry earthwork quantities as TBD or use conservative assumption + flag |
| Town Development Permit | All construction scope | PENDING | Typically not a cost gate (just a schedule gate) |
| Post-award survey/services drawings | DEL-03-04 utility routing | NOT AVAILABLE | Estimate utility distribution with assumed lengths based on site plan concept |
| Owner 72-hour generator runtime confirmation | DEL-02-07 fuel tank sizing | OPEN ISSUE | Assume 72 hours per functional program notes; flag as assumption |
| Town branding guidelines | DEL-05-05 signage | PENDING | Carry as allowance if guidelines not available |
| Owner election of optional items | All PKG-005 | TBD | Estimate all options regardless; Owner decision determines which are included |

---

## 6. Complete Missing PRICE_SOURCES Register

### Critical (block meaningful estimates for major cost items)

| ID | Source Needed | Affects | Priority |
|----|--------------|---------|----------|
| PS-01 | DB internal staff rate table (all roles: PM, superintendent, scheduler, safety officer, Cx coordinator, engineers, architects, admin) — hourly or monthly, CAD 2024 | All PKG-001; design fee components of PKG-002/003/004 | HIGH |
| PS-02 | Assumed project duration (months from NTP to Substantial Performance) | All PKG-001 duration-driven costs | HIGH |
| PS-03 | Structural steel/concrete unit rates (Alberta 2024) | DEL-02-04, DEL-04-03 | HIGH |
| PS-04 | Pre-engineered metal building pricing — 60'x100' clear-span unheated (vendor quote or parametric $/sf) | DEL-04-01 | HIGH |
| PS-05 | Building envelope systems pricing (cladding, insulation, roofing — $/sf by assembly) | DEL-02-04 | HIGH |
| PS-06 | Mechanical system rates (HVAC $/sf, plumbing $/sf, fire protection $/sf if required) | DEL-02-05 | HIGH |
| PS-07 | Electrical system rates (power $/sf, lighting $/sf, IT/telecom $/drop) | DEL-02-06 | HIGH |
| PS-08 | Earthwork unit rates (clearing $/acre, strip $/m3, cut/fill $/m3, compact $/m3) | DEL-03-02 | HIGH |
| PS-09 | Paving unit rates (heavy duty asphalt $/m2, light duty asphalt $/m2, aggregate $/m2, concrete apron $/m2) | DEL-03-03 | HIGH |
| PS-10 | Underground utility rates (water $/lm, sewer $/lm, gas $/lm, power $/lm, telecom $/lm) | DEL-03-04 | HIGH |

### Important (needed for specific deliverables)

| ID | Source Needed | Affects | Priority |
|----|--------------|---------|----------|
| PS-11 | Overhead door vendor quotes (16'x16', motorized, car-wash grade + standard grade, with windows) | DEL-02-04, DEL-04-02 | MEDIUM |
| PS-12 | Diesel generator vendor quote (sized for essentials, 72-hr fuel) | DEL-02-07 | MEDIUM |
| PS-13 | Vehicle exhaust extraction system pricing (per bay) | DEL-02-05 | MEDIUM |
| PS-14 | Bunker gear locker pricing (40 units) | DEL-02-02 | MEDIUM |
| PS-15 | PW locker pricing (40 units) | DEL-02-03 | MEDIUM |
| PS-16 | Breathing air compressor system quote | DEL-02-02 | MEDIUM |
| PS-17 | Bay sump assemblies pricing | DEL-02-05 | MEDIUM |
| PS-18 | Permit fee schedule (Town of Penhold: building, development, utility connection) | DEL-01-04 | MEDIUM |
| PS-19 | Environmental consultant fees (flood hazard, wetland, AEPA application) | DEL-03-05 | MEDIUM |
| PS-20 | Foundation options for cold storage (spread footing vs slab vs screw pile — unit rates) | DEL-04-03 | MEDIUM |

### Optional scope items (needed only for PKG-005 pricing)

| ID | Source Needed | Affects | Priority |
|----|--------------|---------|----------|
| PS-21 | Wash bay equipment vendor quote | DEL-05-01 | LOW (optional) |
| PS-22 | Yard lighting unit rate (pole + fixture + base + wiring, per unit installed) | DEL-05-02 | LOW (optional) |
| PS-23 | Access control system vendor quote (multi-zone) | DEL-05-03 | LOW (optional) |
| PS-24 | Security camera system vendor quote (interior + exterior) + monitoring annual cost | DEL-05-04 | LOW (optional) |
| PS-25 | Town branding guidelines + signage fabrication vendor quote | DEL-05-05 | LOW (optional; PENDING from Owner) |
| PS-26 | Appliance pricing (2024 CAD retail/commercial) | DEL-05-06 | LOW (optional) |

---

## 7. Aggregation Strategy

After all ESTIMATING runs are complete, run AGGREGATION to produce:

### 7.1 Package-level rollups

| Aggregation | Scope | Expected Output |
|-------------|-------|-----------------|
| PKG-001 total | DEL-01-01 through DEL-01-07 | General Requirements & Delivery Controls subtotal |
| PKG-002 total | DEL-02-01 through DEL-02-07 | Main PSB Building subtotal |
| PKG-003 total | DEL-03-01 through DEL-03-05 | Site & Civil Works subtotal |
| PKG-004 total | DEL-04-01 through DEL-04-04 | Cold Storage Building subtotal |
| PKG-005 options | DEL-05-01 through DEL-05-07 (each separate) | Optional items — individually priced, NOT in base total |

### 7.2 Project-level totals

| Total | Composition |
|-------|-------------|
| **Base Price** | PKG-001 + PKG-002 + PKG-003 + PKG-004 |
| **Optional Items** (separately listed) | DEL-05-01, DEL-05-02, DEL-05-03, DEL-05-04, DEL-05-05, DEL-05-06 (each separate line) |
| **Cash Allowances** (separately carried) | DEL-03-04 utility tie-in allowance (TBD) + DEL-05-07 FF&E ($20,000) |
| **Grand Total (if all options elected)** | Base + all options + all allowances |

### 7.3 WBS/CBS matrix

AGGREGATION should produce a combined WBS/CBS matrix showing cost breakdown by:
- **WBS:** Package > Deliverable
- **CBS:** Cost type (design, construction labor, materials, equipment, subcontractors, allowances, fees)

---

## 8. Assumptions and Constraints Log

| ID | Assumption/Constraint | Source | Impact if Wrong |
|----|----------------------|--------|-----------------|
| A-01 | Project duration assumed at TBD months (must be established before PKG-001 estimating) | TBD | PKG-001 costs are directly proportional to duration |
| A-02 | Generator runtime = 72 hours (per functional program notes, pending Owner confirmation) | Addendum 03 §1.15, Functional Program | Affects fuel tank size, generator pad size, cost |
| A-03 | Compressed air system scope assigned to DEL-02-02 (equipment) and DEL-02-06 (electrical feed) | BOE decision (resolves CON-M-01) | If reversed, cost lines move between deliverables but total unchanged |
| A-04 | Building service demarcation at 1.5m outside foundation wall | BOE decision | Affects PKG-003 vs PKG-002 cost split for utilities |
| A-05 | Utility tie-in allowance value = TBD (must be set by Owner/DB agreement before estimating DEL-03-04 tie-in component) | DEC-004 | Cannot produce meaningful tie-in total without this value |
| A-06 | Cold storage building is pre-engineered metal building type | Industry standard for this building type/size | If custom-designed, costs increase significantly |
| A-07 | No fire protection (sprinkler) system required for cold storage (unheated, storage use) | Code assumption — must verify with AHJ | If required, adds significant cost to DEL-04-04 |
| A-08 | All optional items (PKG-005) estimated regardless of Owner election status | BOE strategy decision | Unused option estimates have zero cost impact but provide Owner with pricing for decision-making |
| A-09 | Base year 2024; no escalation applied | Project direction | If construction extends beyond 2024, escalation may be needed on later-procured items |
| A-10 | Geotechnical investigation already completed (report in _Sources/references) | Existing reference document | If additional geotech needed, add cost to DEL-03-02 or DEL-03-05 |

---

## 9. Document Control

| Field | Value |
|-------|-------|
| Document | Basis of Estimate (BOE) |
| Version | DRAFT v0.1 |
| Prepared by | [Human operator] with HELP_HUMAN agent support |
| Date | 2026-02-18 |
| Status | DRAFT — Pending human review and approval |
| Next action | Human reviews and approves; then assemble PRICE_SOURCES per Section 6 register; then execute ESTIMATING runs per Section 5 sequence |

---

**END OF DOCUMENT**
