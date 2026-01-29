# Source Index

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG12_DRAFT_2026-01-28_2341 |
| Estimate Label | PKG12_DRAFT |
| Package Scope | PKG-12 Product Transfer & Metering (5 deliverables) |
| Date | 2026-01-28 |

## Source Discovery Summary

This index documents all sources reviewed for PKG-12 Product Transfer & Metering estimate development.

### Deliverable Folder Sources

| Deliverable | Folder Path | Status | Documents Available |
|-------------|-------------|--------|-------------------|
| DEL-12.01 | test/execution/PKG-12_Product_Transfer_and_Metering/1_Working/DEL-12.01_Metering_Design_Drawing_Set/ | INITIALIZED | Datasheet.md, Specification.md, Guidance.md, Procedure.md |
| DEL-12.02 | test/execution/PKG-12_Product_Transfer_and_Metering/1_Working/DEL-12.02_Metering_Technical_Specification/ | INITIALIZED | Datasheet.md, Specification.md, Guidance.md, Procedure.md |
| DEL-12.03 | test/execution/PKG-12_Product_Transfer_and_Metering/1_Working/DEL-12.03_Metering_Design_Calculations/ | INITIALIZED | Datasheet.md, Specification.md, Guidance.md, Procedure.md |
| DEL-12.04 | test/execution/PKG-12_Product_Transfer_and_Metering/1_Working/DEL-12.04_Metering_Data_Sheet_Package/ | INITIALIZED | Datasheet.md, Specification.md, Guidance.md, Procedure.md |
| DEL-12.05 | test/execution/PKG-12_Product_Transfer_and_Metering/1_Working/DEL-12.05_Metering_Installation_and_Test_Records/ | INITIALIZED | Datasheet.md, Specification.md, Guidance.md, Procedure.md |

### Decomposition Source

| Source | Location | Content Used |
|--------|----------|--------------|
| Project Decomposition | test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md | PKG-12 scope definition (line 102), deliverable definitions (lines 356-360), facility parameters (throughput: 1,000,000 MT/a; railcar stations: 32; product: CSD canola oil), objective mappings (OBJ-2 line 781, OBJ-10 line 789) |

### Configuration and Rate Tables

| Source | Location | Status | Notes |
|--------|----------|--------|-------|
| Estimate Config | test/execution/_Estimates/_CONFIG.md | Found | Currency: CAD, Pricing date: 2026-01, Rounding: 1000, Contingency method: PCT_BY_BUCKET |
| Rate Tables | test/execution/_Estimates/_RateTables/ | Not found | No project-specific rate tables available |

### Pricing Sources (Priority Order)

#### 1. Explicit Pricing Sources (Quotes/Budgets)
**Status:** None available

**Impact:** All pricing will use allowances

#### 2. Rate Tables
**Status:** None available

**Search performed:**
- test/execution/_Estimates/_RateTables/ — not found
- Deliverable `_REFERENCES.md` files — no rate table references identified

**Impact:** Fallback to allowances required

#### 3. Embedded Typical Model (Fallback)
**Status:** Will be used as primary pricing basis

**Basis:** AGENT_ESTIMATING.md STRUCTURE section "Fallback Typical Model"

**Application:**
- Engineering deliverables: LS allowances based on typical custody transfer metering engineering effort
- Materials: Parametric allowances based on typical custody transfer flow meter costs, transmitter costs, metering system components
- Construction: Parametric allowances based on typical installation manhours and equipment
- Indirects/Services: Factor-based per fallback model

**Decision Reference:** D-001

## Sources Used for Quantities

| Quantity Source | Description | Evidence |
|----------------|-------------|----------|
| Decomposition | Facility parameters: 1,000,000 MT/a throughput, 32 railcar unloading stations, CSD canola oil product | Lines 41, 43, 44 |
| DEL-12.01 Datasheet.md | Metering points: rail unloading custody transfer, marine loading custody transfer; anticipated drawing count (3 sheets minimum) | DEL-12.01 Datasheet.md lines 36-37, 26 |
| DEL-12.02 Datasheet.md | Equipment types: custody transfer flow meters (×2), temperature transmitters (×2+), pressure transmitters (×2) | DEL-12.02 Datasheet.md line 24 |
| DEL-12.04 Datasheet.md | Data sheet count: minimum 4 data sheets (flow meters ×2, temperature transmitters, pressure transmitters) | DEL-12.04 Datasheet.md line 24 |
| Typical Custody Transfer Metering Systems | Parametric quantities for metering equipment, proving equipment, instrumentation based on industry-typical custody transfer installations | Fallback model (A-001 through A-020) |

## Sources Used for Pricing

All pricing based on **Fallback Typical Model** per AGENT_ESTIMATING.md due to absence of vendor quotes and rate tables.

| Cost Element | Pricing Basis | Confidence | Notes |
|--------------|---------------|------------|-------|
| Engineering (E) | Allowances per deliverable | LOW | Typical custody transfer metering engineering effort; no project-specific rates |
| Materials (MAT) | Allowances per equipment type | LOW | Typical custody transfer flow meter costs ($100k-300k/meter), transmitter costs ($2k-8k/unit), proving equipment costs |
| Construction Directs (CD) | Parametric manhours × assumed labor rate ($120/hr all-in) | LOW | Typical installation effort for metering systems; no project labor rates |
| Indirects/Services | Factors per fallback model | MED | CI = 18% CD, P = 2% MAT, PM = 6% (CD+CI+MAT), COM = 3% (CD+CI+MAT) |
| Contingency | PCT_BY_BUCKET per fallback model | MED | Bucket baseline + allowance-heavy adjustment |

## Known Gaps

| Gap | Impact on Estimate | Resolution Path |
|-----|-------------------|-----------------|
| No ER Vol 2 Part 2 (metering requirements) | Flow rates, accuracy requirements, proving method assumed | Provide ER Vol 2 Part 2 for metering technical requirements |
| No flow rate specifications | Flow meter sizing and cost based on throughput parametrics | Provide design flow rates for rail unloading and marine loading from PKG-10/PKG-11 or ER |
| No vendor quotes | All equipment costs as allowances with wide ranges | Obtain budgetary quotes from custody transfer metering suppliers (Emerson, Endress+Hauser, Krohne, etc.) |
| No rate tables | Labor and material rates assumed | Provide project rate library for BC lower mainland labor, equipment, materials |
| No proving method selection | Proving equipment cost uncertain (in-line vs. portable vs. master meter) | Confirm proving method in DEL-12.02 specification |
| No meter technology selection | Flow meter cost range depends on technology (Coriolis vs. ultrasonic vs. turbine vs. PD) | Confirm meter technology selection in DEL-12.02 specification |
| Deliverables in INITIALIZED state | Limited scope definition; quantities and requirements are assumptions | Progress deliverables to IN_PROGRESS with defined scope |

## Decision Impact on Pricing

| Decision | Choice Made | Impact on Estimate | Decision Ref |
|----------|-------------|-------------------|--------------|
| Currency selection | CAD | All costs in Canadian dollars | D-001 |
| Pricing basis hierarchy | Allowances (no quotes/rates available) | All line items priced via fallback model | D-002 |
| Meter technology assumption | Coriolis mass flowmeter (typical for custody transfer accuracy) | Flow meter cost range $150k-250k/unit | D-003, A-001 |
| Proving method assumption | Portable prover (typical for dual-service installations) | Portable prover cost ~$80k-120k | D-004, A-010 |
| Labor rate assumption | $120/hr all-in (BC lower mainland typical) | CD labor costs based on assumed rate | D-005 |
| Metering point configuration | Separate meters for rail and marine (not shared) | 2 flow meters required | D-006, A-001 |

---

*Source index prepared per AGENT_ESTIMATING PROTOCOL Function 2 (Source Discovery + Indexing). All sources documented for estimate traceability.*
