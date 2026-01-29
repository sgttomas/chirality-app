# Estimate Summary

## PKG-12 Product Transfer & Metering

### Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG12_DRAFT_2026-01-28_2341 |
| Estimate Label | PKG12_DRAFT |
| Pricing Date | 2026-01 |
| Currency | CAD |
| Run Status | WARNINGS |

### Summary by CBS

| CBS | Description | Base Amount | Contingency % | Contingency | Total |
|-----|-------------|-------------|---------------|-------------|-------|
| E | Engineering & Design | $138,000 | 20% | $28,000 | $166,000 |
| MAT | Equipment & Materials | $717,000 | 25% | $179,000 | $896,000 |
| CD | Construction Directs | $311,000 | 30% | $93,000 | $404,000 |
| CI | Construction Indirects | $56,000 | 30% | $17,000 | $73,000 |
| PM | Project Management / EPCM | $71,000 | 15% | $11,000 | $82,000 |
| P | Procurement Services | $13,000 | 15% | $2,000 | $15,000 |
| COM | Commissioning / Testing | $120,000 | 30% | $36,000 | $156,000 |
| **SUBTOTAL** | | **$1,426,000** | | **$366,000** | **$1,792,000** |

### Summary by WBS (Deliverable)

| WBS ID | Deliverable | CBS | Base Amount |
|--------|-------------|-----|-------------|
| DEL-12.01 | Metering Design Drawing Set | E | $28,000 |
| DEL-12.02 | Metering Technical Specification | E | $38,000 |
| DEL-12.03 | Metering Design Calculations | E | $42,000 |
| DEL-12.04 | Metering Data Sheet Package | E | $18,000 |
| DEL-12.05 | Metering Installation & Test Records | E | $12,000 |
| N/A | Custody Transfer Flow Meter - Rail Unloading (6") | MAT | $180,000 |
| N/A | Custody Transfer Flow Meter - Marine Loading (10") | MAT | $230,000 |
| N/A | Temperature Transmitters (4 units) | MAT | $24,000 |
| N/A | Pressure Transmitters (2 units) | MAT | $10,000 |
| N/A | Portable Prover System | MAT | $120,000 |
| N/A | Metering Skid Structural Steel | MAT | $55,000 |
| N/A | Meter Run Piping (Stainless Steel) | MAT | $35,000 |
| N/A | Metering System Installation Consumables | MAT | $15,000 |
| N/A | Flow Computers / Totalizers (2 units) | MAT | $36,000 |
| N/A | Junction Boxes and Marshalling | MAT | $12,000 |
| N/A | Metering System Installation Labor | CD | $288,000 |
| N/A | Survey and Setting Out | CD | $5,000 |
| N/A | Specialist Installation Equipment | CD | $18,000 |
| N/A | Construction Indirects | CI | $56,000 |
| N/A | Procurement Services | P | $13,000 |
| N/A | Project Management / EPCM | PM | $71,000 |
| N/A | Factory Acceptance Test (FAT) - Flow Meters | COM | $32,000 |
| N/A | Site Acceptance Test (SAT) - Metering System | COM | $28,000 |
| N/A | Initial Proving (Commissioning) | COM | $48,000 |
| N/A | Calibration Verification and Record Compilation | COM | $12,000 |
| | **TOTAL** | | **$1,426,000** |

### Cost Breakdown

| Category | Amount | % of Base |
|----------|--------|-----------|
| Engineering (Deliverables) | $138,000 | 9.7% |
| Materials | $717,000 | 50.3% |
| Construction Directs | $311,000 | 21.8% |
| Indirects & Services | $140,000 | 9.8% |
| Commissioning | $120,000 | 8.4% |
| **Base Estimate** | **$1,426,000** | **100%** |
| Contingency | $366,000 | 25.7% |
| **Total Estimate** | **$1,792,000** | **125.7%** |

### Major Cost Drivers

| Item | Amount | % of Base | Notes |
|------|--------|-----------|-------|
| Custody Transfer Flow Meter - Marine Loading (10") | $230,000 | 16.1% | Large Coriolis mass flowmeter for high-flow marine loading service |
| Metering System Installation Labor (2,400 MH) | $288,000 | 20.2% | Precision installation of meters, piping, electrical/instrument connections |
| Custody Transfer Flow Meter - Rail Unloading (6") | $180,000 | 12.6% | Coriolis mass flowmeter for rail unloading custody transfer |
| Portable Prover System | $120,000 | 8.4% | Proving equipment with Measurement Canada certification |
| Commissioning (FAT + SAT + Proving) | $120,000 | 8.4% | Factory testing, site testing, initial proving for custody transfer accuracy verification |

### Confidence Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| Quantities | LOW | Equipment counts parametric from typical custody transfer systems; flow rates not specified |
| Pricing | LOW | All allowances; no vendor quotes or rate tables |
| Scope definition | LOW | Deliverables in INITIALIZED state; meter technology, proving method, flow rates TBD |
| Interface assumptions | MED | Interfaces with PKG-06, PKG-14, PKG-17, PKG-19, PKG-20 assumed per typical metering installations |
| **Overall** | **LOW** | Placeholder estimate only; requires vendor quotes and defined scope |

### Key Assumptions

1. Two separate custody transfer flow meters: 6" for rail unloading, 10" for marine loading
2. Coriolis mass flowmeter technology with integral density measurement
3. Portable prover system for proving both meters (vs. in-line provers or master meter)
4. Temperature transmitters (4 units) for custody transfer compensation
5. Pressure transmitters (2 units) for compensation if required
6. Flow computers/totalizers (2 units) or integration with PKG-19 control system
7. Metering skids with structural steel supports and access platforms
8. Stainless steel meter run piping with straight-run requirements
9. Factory acceptance testing at vendor facility
10. Site acceptance testing and initial proving during commissioning
11. BC lower mainland labor rates ($120/hr all-in)
12. Measurement Canada approval required for custody transfer in Canada

### Exclusions

- Owner's costs
- Land acquisition
- Permits obtained by Employer
- Process piping beyond meter runs (PKG-14)
- P&IDs (PKG-14)
- Control system architecture (PKG-19)
- Field instrumentation general (PKG-20)
- Electrical power distribution (PKG-17)
- Structural foundations (PKG-05)
- Structural steelwork general (PKG-06)
- Nitrogen supply skid (Employer-supplied)
- Escalation
- Taxes

### Recommendations

1. **Priority:** Obtain design flow rates for rail unloading and marine loading from ER Vol 2 Part 2 or PKG-10/PKG-11 hydraulics
2. **Priority:** Obtain budgetary quotes from custody transfer metering suppliers (Emerson Micro Motion, Endress+Hauser Proline Promass, Krohne Optimass)
3. **Priority:** Confirm meter technology selection and proving method in DEL-12.02 specification
4. Obtain portable prover quotes from proving equipment suppliers
5. Confirm Measurement Canada approval requirements and certification costs
6. Coordinate metering skid structural design with PKG-06
7. Coordinate meter run piping and P&ID integration with PKG-14
8. Coordinate electrical/controls interfaces with PKG-17, PKG-19, PKG-20
9. Progress deliverables from INITIALIZED to IN_PROGRESS with defined scope
10. Develop project labor rate table for BC lower mainland

---

*Estimate prepared per AGENT_ESTIMATING straight-through pipeline. All amounts in CAD, rounded to nearest $1,000.*
