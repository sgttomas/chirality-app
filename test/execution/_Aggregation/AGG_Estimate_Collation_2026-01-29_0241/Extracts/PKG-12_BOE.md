# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG12_DRAFT_2026-01-28_2341 |
| Estimate Label | PKG12_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-12 Product Transfer & Metering (5 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-12:

| CBS | Description | Included |
|-----|-------------|----------|
| E | Engineering & Design | Yes |
| PM | Project Management / EPCM | Yes |
| P | Procurement Services | Yes |
| MAT | Equipment & Materials | Yes |
| CD | Construction Directs | Yes |
| CI | Construction Indirects | Yes |
| COM | Commissioning / Testing | Yes |
| CONT | Contingency | Yes |

### Scope Elements (from Decomposition PKG-12)

**Package Scope:** Product Transfer & Metering (Decomposition line 102)

**Deliverables (5):**
1. **DEL-12.01** — Metering Design Drawing Set: Defines design arrangement and details for metering per ER requirements (Decomposition:356)
2. **DEL-12.02** — Metering Technical Specification: Defines performance, materials, and workmanship requirements for metering per ER requirements (Decomposition:357)
3. **DEL-12.03** — Metering Design Calculations: Provides engineering basis and sizing/verification calculations for metering (Decomposition:358)
4. **DEL-12.04** — Metering Data Sheet Package: Defines and substantiates metering in accordance with ER requirements (Decomposition:359)
5. **DEL-12.05** — Metering Installation & Test Records: Provides evidence of completion, inspection, and testing for metering (Decomposition:360)

**Technical Scope:**
- **Custody transfer flow meters:** Two metering points — (1) rail unloading custody transfer, (2) marine loading custody transfer (DEL-12.01 Datasheet.md)
- **Metering instrumentation:** Temperature transmitters, pressure transmitters (if applicable), density measurement (integral to Coriolis or separate)
- **Proving system:** In-line prover, portable prover, or master meter (TBD from DEL-12.02)
- **Metering system integration:** Flow computers/totalizers, control system integration (PKG-19), data logging
- **Installation:** Metering skids, structural supports, meter run piping, electrical/instrument connections
- **Testing/commissioning:** FAT, SAT, initial proving, calibration verification, record compilation

**Facility Parameters (from Decomposition):**
- Permitted throughput: 1,000,000 MT per annum (line 41)
- Product: CSD (Crude Super Degummed) canola oil (line 43)
- Railcar unloading: 32 stations on 2 tracks (line 44)
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC (line 10)

**Objective Alignment:**
- **OBJ-2 (Throughput Capacity):** Metering must support 1,000,000 MT/a throughput without flow constraints (Decomposition:781)
- **OBJ-10 (Custody Transfer Accuracy):** Metering must provide accurate measurement for product custody transfer (Decomposition:789)

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Process piping beyond meter runs | PKG-14 scope |
| P&IDs | PKG-14 scope |
| Control system architecture | PKG-19 scope |
| Field instrumentation general | PKG-20 scope (except metering-specific transmitters) |
| Electrical power distribution | PKG-17 scope |
| Structural foundations | PKG-05 scope |
| Structural steelwork general | PKG-06 scope (except metering skid structural supports) |
| Nitrogen supply skid | Employer-supplied per decomposition Section 1.2 |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design, procurement, installation, testing for custody transfer metering | decomposition Section 1.2 |
| Metering points | Two separate metering points: rail unloading and marine loading | A-001, D-006 |
| Meter configuration | Separate dedicated meters (not shared/manifolded) | D-006 |
| Regulatory compliance | Measurement Canada approval required for custody transfer in Canada | A-009, OBJ-10 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-005 |
| Labor rate | $120/hr all-in (process/instrument installation) | D-005, A-024 |
| Working hours | Standard 8-10 hour shifts | Typical |
| Site access | Industrial terminal site; crane/equipment access available | Typical |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-002 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Quantity Basis

Quantities are parametric estimates based on:
- Facility throughput (1,000,000 MT/a) and design flow rate estimates
- Typical custody transfer metering installations for vegetable oil terminals
- Deliverable document scope descriptions (INITIALIZED state; limited detail)
- Industry-standard custody transfer metering equipment configurations

| Item | Estimated Quantity | Basis | Assumption Ref |
|------|-------------------|-------|---------------|
| Custody transfer flow meters | 2 units (1 rail, 1 marine) | Two metering points per decomposition; separate meters typical | A-001, D-006 |
| Flow meter technology | Coriolis mass flowmeter | Typical for custody transfer accuracy; integral density | A-002, D-003 |
| Flow meter sizes | 6" rail, 10" marine | Parametric from throughput and typical flow velocities | A-003 |
| Temperature transmitters | 4 units | 2 per service for compensation/redundancy | A-004 |
| Pressure transmitters | 2 units | 1 per service (may not be required if Coriolis) | A-005 |
| Portable prover | 1 system | Flexible proving for both meters | A-008, D-004 |
| Flow computers/totalizers | 2 units | 1 per service (or integrated in PKG-19) | A-031 |
| Installation labor | 2,400 manhours | Meter installation + piping + electrical/instrument | A-024 |

## Technical Assumptions

### Meter Technology (A-002, D-003)

**Assumed:** Coriolis mass flowmeter

**Rationale:**
- Direct mass measurement (no density compensation calculation required)
- High accuracy (±0.15% typical) suitable for custody transfer
- Integral density measurement
- Good performance with viscous products (canola oil viscosity ~30-70 cP)
- Industry-standard for custody transfer of vegetable oils

**Alternatives:**
- Ultrasonic: Lower cost ($80k-150k/unit), good accuracy (±0.5%), requires separate density measurement
- Turbine: Lower cost ($30k-80k/unit), moderate accuracy (±0.25-0.5%), viscosity-sensitive
- Positive displacement: Moderate cost ($50k-120k/unit), good accuracy (±0.15%), higher pressure drop

**Cost Impact:** Coriolis selection drives flow meter costs to $150k-250k/unit (higher than alternatives)

**Verification:** Confirm technology in DEL-12.02 specification based on accuracy requirements (OBJ-10), product properties (CSD canola oil), and flow range

### Proving Method (A-008, D-004)

**Assumed:** Portable prover system

**Rationale:**
- Flexibility to prove both rail and marine meters with single prover
- Lower cost than dual in-line provers
- Suitable for periodic proving (quarterly or semi-annual typical)
- Typical for dual-service custody transfer installations

**Alternatives:**
- In-line provers (×2): Higher cost ($300k-500k total), continuous proving capability, dedicated per meter
- Master meter: Lower equipment cost ($50k-80k), requires periodic external calibration, less common for custody transfer

**Cost Impact:** Portable prover ~$120k vs. in-line provers ~$400k vs. master meter ~$60k

**Verification:** Confirm proving method in DEL-12.02 specification and DEL-12.03 calculations

### Flow Rates (A-003)

**Rail Unloading:**
- Estimated design flow rate: ~80-120 m³/h per metering point
- Basis: 32 railcar unloading stations; typical unloading rate 50-100 m³/h/station; metering may be per-station or manifolded (TBD)

**Marine Loading:**
- Estimated design flow rate: ~800-1500 m³/h
- Basis: Typical bulk vegetable oil loading rate for Panamax vessels; loading time 12-24 hours for 40,000-60,000 MT cargo

**Verification:** Obtain design flow rates from ER Vol 2 Part 2, PKG-10 railcar unloading hydraulics, or PKG-11 marine loading hydraulics

## Indirects Model

**Method:** Factor-based (fallback typical model)

| Factor | Rate | Base | Decision Ref |
|--------|------|------|--------------|
| Construction Indirects (CI) | 0.18 | CD | D-007 |
| Procurement Services (P) | 0.02 | MAT | D-007 |
| EPCM/PM | 0.06 | CD + CI + MAT | D-007 |
| Commissioning (COM) base factor | 0.03 | CD + CI + MAT | D-007 |

**Calculation:**
- CI = 18% × $311k = $56k
- P = 2% × $717k = $13k (rounded)
- PM = 6% × ($311k + $56k + $717k) = $71k (rounded)
- COM base factor = 3% × ($311k + $56k + $717k) = $33k (COM line items total $120k includes FAT/SAT/proving beyond factor)

**Note:** COM total ($120k) includes both factor-based allowance and explicit FAT/SAT/proving line items; COM factor is advisory only.

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances; scope in INITIALIZED state |
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances; custody transfer equipment without quotes |
| CD | 20% | +10% (100% allowance) | 30% | All CD allowances; precision installation for custody transfer |
| CI | 20% | +10% (factor-derived) | 30% | Derived from CD; allowance-heavy |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived + testing) | 30% | Factor-based; FAT/SAT/proving complexity |

**Decision:** D-008 — Contingency rates elevated due to 100% allowance-based estimate, custody transfer accuracy requirements, and precision installation complexity.

**Contingency Calculation:**
- E: 20% × $138k = $28k
- MAT: 25% × $717k = $179k
- CD: 30% × $311k = $93k
- CI: 30% × $56k = $17k
- PM: 15% × $71k = $11k
- P: 15% × $13k = $2k
- COM: 30% × $120k = $36k
- **Total Contingency: $366k (25.7% of base)**

## Escalation Method

- **Mode:** NONE
- **Rationale:** Pricing date is current (January 2026); no escalation applied per config
- **Decision:** D-009

## Rounding Policy

- **Rounding:** Nearest $1,000 CAD
- **Decision:** D-010 (per _CONFIG.md)

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Lines priced by QUOTE | 0% |
| Lines priced by RATE_TABLE | 0% |
| Lines priced by ALLOWANCE/PARAMETRIC | 100% |
| Deliverables with explicit quantities | 0% |
| Overall confidence | LOW |

**Analysis:**
- All 25 line items use ALLOWANCE or PARAMETRIC methods
- No vendor quotes or project rate tables available
- Deliverables in INITIALIZED state provide limited scope definition
- Equipment counts, sizes, and installation scope are parametric assumptions
- Estimate is a placeholder for budgeting; requires vendor quotes and scope refinement

## Known Gaps

| Gap | Impact | Resolution Path |
|-----|--------|-----------------|
| No ER Vol 2 Part 2 (metering requirements) | Flow rates, accuracy requirements, proving method, meter technology, operating conditions unknown | Provide ER Vol 2 Part 2 Section on custody transfer metering |
| No design flow rates | Meter sizing and cost uncertain; used parametric estimates from throughput | Obtain design flow rates from PKG-10/PKG-11 or ER; perform sizing in DEL-12.03 |
| No vendor quotes | All equipment costs as allowances with wide ranges | Obtain budgetary quotes from custody transfer metering suppliers (Emerson, Endress+Hauser, Krohne) |
| No rate tables | Labor rates assumed; no craft-specific rates | Provide project rate library for BC lower mainland |
| No meter technology selection | Technology affects cost ($150k-250k Coriolis vs. $30k-150k alternatives) and performance | Confirm technology in DEL-12.02 based on accuracy requirements and product properties |
| No proving method selection | Proving equipment cost range $100k-400k depending on method | Confirm proving method in DEL-12.02 specification |
| Deliverables in INITIALIZED state | Limited scope detail; quantities/requirements are assumptions | Progress deliverables to IN_PROGRESS with defined scope |
| No metering skid structural design | Skid size, complexity, material quantities unknown | Develop metering skid GA in DEL-12.01; coordinate with PKG-06 |
| No interface coordination results | Interfaces with PKG-06/14/17/19/20 assumed per typical practice | Coordinate interfaces per dependency mode NOT_TRACKED |
| No Measurement Canada requirements | Approval requirements, certification costs, periodic verification costs TBD | Confirm Measurement Canada requirements from ER or regulatory research |

## Estimate Development Method

### WBS → CBS Mapping (Function 3.1)

| Deliverable | Primary CBS | Rationale |
|-------------|-------------|-----------|
| DEL-12.01 (Drawing Set) | E | Design deliverable |
| DEL-12.02 (Specification) | E | Design deliverable |
| DEL-12.03 (Calculations) | E | Design deliverable |
| DEL-12.04 (Data Sheets) | E | Design deliverable |
| DEL-12.05 (Test Records) | E | QA/QC deliverable (engineering effort) |
| Metering Equipment | MAT | Flow meters, transmitters, prover, flow computers |
| Metering Skid Structures | MAT | Structural supports (coordinate PKG-06) |
| Meter Run Piping | MAT | Piping material (coordinate PKG-14) |
| Installation | CD | Field labor for installation |
| Indirects/Services | CI, P, PM | Factor-based |
| Commissioning | COM | FAT, SAT, proving, calibration verification |

### Quantity Extraction (Function 3.2)

**Sources:**
- Decomposition lines 356-360: Deliverable definitions
- DEL-12.01 Datasheet.md: Metering points (2), anticipated drawing count (3 sheets minimum)
- DEL-12.02 Datasheet.md: Meter technology options, proving options
- DEL-12.04 Datasheet.md: Data sheet count (minimum 4)
- Facility parameters: 1,000,000 MT/a, 32 railcar stations, CSD canola oil

**Method:**
- Engineering deliverables: Lump sum allowances per deliverable based on typical effort
- Equipment: Parametric quantities from metering points (2), typical custody transfer configurations, facility scale
- Installation: Parametric manhours from equipment scope and typical installation complexity
- Commissioning: Allowances for FAT, SAT, proving based on typical custody transfer commissioning

### Pricing (Function 3.3)

**Hierarchy:** Quote → Rate Table → Allowance

**Actual:** All line items priced by ALLOWANCE (no quotes or rate tables available)

**Method:**
- Engineering: LS allowances per deliverable ($12k-42k range)
- Flow meters: Typical Coriolis custody transfer meter costs ($150k-250k/unit)
- Transmitters: Typical RTD and pressure transmitter costs ($3k-8k/unit)
- Portable prover: Typical proving system cost ($100k-150k)
- Installation labor: Parametric manhours × assumed labor rate ($120/hr all-in)
- Indirects/Services: Factor-based per fallback model (D-007)

### Indirects Application (Function 3.4)

**Model:** Factor-based (no schedule/duration data available)

**Factors Applied:**
- CI = 18% of CD = $56k
- P = 2% of MAT = $13k
- PM = 6% of (CD + CI + MAT) = $71k
- COM factor = 3% of (CD + CI + MAT) = $33k (baseline; explicit COM line items add FAT/SAT/proving)

**Decision:** D-007

## Risk and Uncertainty

### Major Uncertainties

| Uncertainty | Impact | Mitigation |
|-------------|--------|------------|
| Meter technology not selected | Flow meter cost range $150k-250k (Coriolis) vs. $30k-150k (alternatives); ±$200k swing | Confirm technology in DEL-12.02 based on accuracy requirements |
| Proving method not selected | Prover cost $100k (portable) vs. $400k (in-line ×2) vs. $60k (master meter); ±$300k swing | Confirm proving method in DEL-12.02 specification |
| Flow rates not specified | Meter sizes uncertain; affects equipment cost and installation complexity | Obtain design flow rates from ER or PKG-10/PKG-11 |
| No vendor quotes | All equipment costs are parametric; actual costs may vary ±30-50% | Obtain budgetary quotes from custody transfer suppliers |
| Deliverables in INITIALIZED state | Scope definition incomplete; requirements and design details TBD | Progress deliverables to IN_PROGRESS with engineering input |
| Interface scope not coordinated | Installation scope split with PKG-06/14/17/19/20 unclear; may affect labor | Coordinate interfaces per NOT_TRACKED mode |
| Measurement Canada requirements unknown | Approval costs, certification requirements, periodic verification costs TBD | Research Measurement Canada custody transfer regulations |

### Contingency Rationale

**Baseline contingency:** PCT_BY_BUCKET method per D-008

**Allowance-heavy adjustment:** All buckets are 100% allowance-based; adjustment +5% to +10% applied per AGENT_ESTIMATING.md lines 686-689

**Justification for elevated contingency (25.7% overall):**
1. **No vendor pricing:** All equipment costs are parametric; vendor quotes may reveal ±30-50% variance
2. **Technology selection open:** Meter technology affects cost, installation, proving (±$200k swing)
3. **Proving method open:** In-line vs. portable vs. master meter affects cost (±$300k swing)
4. **Scope immaturity:** Deliverables in INITIALIZED state; requirements refinement may add scope
5. **Custody transfer precision:** Installation tolerances and accuracy verification add complexity
6. **Regulatory compliance:** Measurement Canada requirements may add testing, certification, documentation costs
7. **Interface coordination:** Scope boundaries with PKG-06/14/17/19/20 not fully defined

**Contingency provides buffer for:**
- Vendor quote variance from parametric estimates
- Scope additions during engineering (DEL-12.01 through DEL-12.05 progression)
- Interface coordination adjustments
- Regulatory compliance costs (Measurement Canada approval, certification)
- Installation complexity (precision alignment, calibration, proving)

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-010 |
| Assumptions_Log.md | All assumptions A-001 through A-032 |
| Detail.csv | Line item detail with traceability |
| Summary.md | Cost summaries and confidence metrics |
| Source_Index.md | Source discovery and pricing basis hierarchy |

---

*BOE prepared per AGENT_ESTIMATING SPEC requirements. Basis documented for auditability and reproducibility.*
