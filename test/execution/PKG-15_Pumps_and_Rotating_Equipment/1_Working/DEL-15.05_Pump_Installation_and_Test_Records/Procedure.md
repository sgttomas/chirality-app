# Procedure: DEL-15.05 Pump Installation & Test Records

## Purpose

This procedure defines the process for installing, commissioning, and documenting pump equipment within **PKG-15 Pumps & Rotating Equipment** for the Canola Oil Transload Facility.

**Deliverable purpose:** Provides evidence of completion, inspection, and testing for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.05 entry

**Deliverable type:** Record (Installation and commissioning documentation)
**Responsible party:** D&B Contractor (QA/QC, Construction, Commissioning)

This procedure covers:
1. **Installation:** How to install pumps per drawings and manufacturer instructions
2. **Pre-commissioning:** Checks before first startup
3. **Performance testing:** How to conduct field performance tests
4. **Documentation:** How to complete and manage installation and test records

**Source:** API 610 Section 6 (installation, operation, and testing)

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans

**Source:** `_DEPENDENCIES.md`

### Upstream Requirements

| Requirement | Source | Status |
|------------|--------|--------|
| **Equipment delivered** | Vendor per purchase order | **TBD** |
| **Foundation ready** | PKG-05 (foundations complete and cured) | **TBD** |
| **Installation drawings** | DEL-15.01 (issued for construction) | **TBD** |
| **Vendor data** | DEL-15.04 (AFC) | **TBD** |
| **Piping system** | DEL-14 (complete and flushed) | **TBD** |
| **Electrical power** | PKG-19/20 (energized and tested) | **TBD** |

**Source:** Installation dependencies

### Personnel and Equipment

**Personnel:**
- Construction Supervisor — Overall installation responsibility
- Millwrights/Riggers — Equipment setting and alignment
- QA/QC Inspector — Installation inspection and records
- Commissioning Engineer — Performance testing and analysis
- Operations Personnel — Support during commissioning

**Equipment and Tools:**
- Mobile crane or forklift (for equipment rigging)
- Alignment tools (dial indicators or laser alignment system)
- Torque wrenches
- Grouting equipment and non-shrink grout
- Test instruments (flow meter, pressure gauges, power meter, vibration analyzer)

**Source:** Standard pump installation and commissioning requirements

## Steps

### Phase 1: Pre-Installation

#### Step 1.1: Foundation Inspection

**Action:**
- Inspect foundation per PKG-05 drawings:
  - Concrete surface level (tolerance ±3mm typical)
  - Surface finish (smooth, clean, no laitance or loose material)
  - Anchor bolt sleeves clear and clean
  - Dimensions correct per drawings

**Verification:**
- Foundation inspection checklist completed and signed by QA/QC

**Records:**
- Foundation inspection checklist with photos

**Source:** API 610 Section 6.1 (foundation requirements)

---

#### Step 1.2: Equipment Receipt Inspection

**Action:**
- Inspect equipment upon delivery:
  - Verify against packing list and purchase order
  - Check for shipping damage
  - Verify preservation (shaft locking pins, protective coatings)
  - Review vendor O&M manual and installation instructions

**Verification:**
- Receipt inspection completed; any damage documented and reported to vendor

**Records:**
- Equipment receipt inspection form

**Source:** Standard equipment receipt procedure

---

### Phase 2: Installation

#### Step 2.1: Rig and Set Equipment

**Action:**
- Review rigging plan and lifting lug locations (from DEL-15.04 vendor data)
- Rig equipment using appropriate lifting equipment
- Set equipment on foundation at correct location and elevation per DEL-15.01 drawings
- Use shims as needed to achieve correct elevation (temporary shims for grouting)

**Safety:**
- Follow WorkSafeBC rigging safety requirements
- Ensure adequate crane capacity and rigging rating

**Verification:**
- Equipment set to correct location (±10mm) and elevation (±3mm)

**Records:**
- Rigging plan and as-set survey

**Source:** API 610 Section 6.1 (equipment setting); WorkSafeBC safety requirements

---

#### Step 2.2: Rough Alignment

**Action:**
- Perform rough shaft alignment using dial indicators or laser system:
  - Measure parallel offset (horizontal and vertical)
  - Measure angular offset
  - Adjust shims to bring alignment within temporary tolerance (±0.2mm typical for grouting)

**Verification:**
- Rough alignment recorded and within temporary tolerance

**Records:**
- Rough alignment data sheet

**Source:** API 610 Section 6.3 (alignment procedure)

---

#### Step 2.3: Grouting

**Action:**
- Prepare grout per manufacturer instructions (non-shrink grout)
- Pour grout from one side to avoid voids:
  - Pour until grout flows out opposite side
  - Ensure 25–75mm grout thickness per API 610 Section 6.1.4
- Finish grout surface smooth
- Protect from rain and freezing during curing

**Verification:**
- Grout properly mixed, poured, and finished
- **Curing time: Minimum 7 days before final alignment** per ACI 318

**Records:**
- Grout pour record (date, time, weather conditions, grout mix)
- Curing log

**Source:** API 610 Section 6.1.4 (grouting); ACI 318 (curing requirements)

---

#### Step 2.4: Final Alignment

**Action:**
- After grout curing (7+ days), perform final shaft alignment:
  - Remove temporary shims if needed
  - Measure parallel and angular offset using dial indicators or laser
  - Adjust alignment by shimming under motor feet (not pump feet)
  - Target: Parallel offset < 0.05mm, Angular offset < 0.05mm per 100mm diameter (API 610 typical)
  - Torque anchor bolts to specified values

**Verification:**
- Final alignment within API 610 and manufacturer tolerance

**Records:**
- Final alignment data sheet with before/after readings
- Anchor bolt torque record

**Source:** API 610 Section 6.3 (alignment procedure and tolerances)

---

#### Step 2.5: Connect Piping

**Action:**
- Connect suction and discharge piping per DEL-14 piping drawings:
  - Ensure piping is independently supported (no weight on pump nozzles per API 610 Section 6.2)
  - Install gaskets and bolt up flanges per ASME B16.5
  - Torque flange bolts per specification
- After piping connection, re-check shaft alignment to verify piping has not imposed misalignment

**Verification:**
- Piping properly connected and supported
- Alignment still within tolerance after piping connection

**Records:**
- Piping connection checklist
- Post-piping alignment check

**Source:** API 610 Section 6.2 (piping connection requirements)

---

#### Step 2.6: Electrical Connection

**Action:**
- Coordinate with Electrical discipline (PKG-19/20) for motor electrical connections:
  - Verify motor voltage matches power supply
  - Connect motor leads per wiring diagram
  - Install conduit and terminations
  - Megger test motor windings
  - Verify motor rotation direction (before coupling pump)

**Verification:**
- Motor electrical connections complete and tested
- Rotation direction correct

**Records:**
- Motor electrical connection record
- Megger test results
- Rotation direction verification

**Source:** Motor installation requirements; coordinate with Electrical discipline

---

### Phase 3: Pre-Commissioning

#### Step 3.1: Pre-Start Inspection

**Action:**
- Perform pre-start inspection checklist:
  - [ ] Coupling aligned and coupling guard installed
  - [ ] Lubrication system filled and checked (oil level, grease packed per manufacturer)
  - [ ] Shaft rotates freely by hand (with coupling disconnected)
  - [ ] All protective devices and sensors installed (pressure switches, temperature sensors, vibration sensors)
  - [ ] Suction and discharge valves operational
  - [ ] Piping system flushed and clean
  - [ ] Safety guarding installed per WorkSafeBC
  - [ ] Personnel clear of equipment

**Verification:**
- All pre-start checklist items complete

**Records:**
- Pre-start inspection checklist with sign-offs

**Source:** API 610 Section 6 (pre-start requirements); WorkSafeBC safety requirements

---

#### Step 3.2: Rotation Check

**Action:**
- With coupling disconnected (or with coupling connected but pump isolated):
  - Jog motor briefly to verify rotation direction
  - Correct direction: Motor shaft rotates same direction as arrow on pump casing
  - If wrong direction: De-energize and swap two motor leads (3-phase motor)

**Safety:**
- Ensure personnel clear of rotating equipment
- Use proper lockout/tagout procedures

**Verification:**
- Rotation direction correct

**Records:**
- Rotation direction verification record

**Source:** API 610 Section 6 (rotation verification)

---

### Phase 4: Commissioning and Performance Testing

#### Step 4.1: Initial Startup

**Action:**
- Fill pump casing with fluid (if required by manufacturer)
- Open suction valve fully
- Throttle discharge valve to ~50% (to reduce initial load)
- Start motor and pump:
  - Monitor for abnormal noise, vibration, leaks
  - Gradually open discharge valve to increase flow
  - Monitor motor current, pump pressure, seal condition
- If any abnormal conditions: Shut down immediately and investigate

**Safety:**
- Ensure all personnel aware of startup
- Monitor equipment closely during initial operation

**Verification:**
- Pump starts and operates smoothly without abnormal conditions

**Records:**
- Initial startup log

**Source:** API 610 Section 6 (startup procedure)

---

#### Step 4.2: Performance Test Setup

**Action:**
- Install test instrumentation (if not permanently installed):
  - Flow meter (calibrated, traceable)
  - Suction pressure gauge (calibrated)
  - Discharge pressure gauge (calibrated)
  - Power meter or current/voltage meters (calibrated)
  - Vibration analyzer
- Allow pump to reach stable operating conditions (30 minutes minimum)
- Record ambient conditions (temperature, barometric pressure)

**Verification:**
- All test instruments installed, calibrated, and operational

**Records:**
- Test instrument calibration certificates
- Test setup documentation

**Source:** API 610 Section 6.9 (field performance test setup); ISO 9906 (test instrumentation)

---

#### Step 4.3: Conduct Performance Test

**Action:**
- Test at multiple operating points:
  - **Point 1:** ~70% of rated flow
  - **Point 2:** 100% of rated flow (rated point)
  - **Point 3:** ~110–120% of rated flow
- At each operating point, record:
  - Flow rate (Q)
  - Suction pressure (Ps)
  - Discharge pressure (Pd)
  - Motor power (P) or current/voltage
  - Fluid temperature and density
- Calculate for each point:
  - Head: H = (Pd - Ps) / (ρ × g) + elevation difference
  - Efficiency: η = (ρ × g × Q × H) / (P × 1,000)
- Record vibration measurements at pump and motor bearings (3 axes each)

**Verification:**
- Test data recorded for all operating points

**Records:**
- Performance test data sheets with calculations

**Source:** API 610 Section 6.9 (field performance test procedure); ISO 9906 (test methods)

---

#### Step 4.4: Analyze Test Results

**Action:**
- Compare test results to:
  - Design calculations (DEL-15.03)
  - Specification requirements (DEL-15.02)
  - Vendor data (DEL-15.04)
- Check acceptance criteria:
  - Flow within ±7% of rated (ISO 9906 Grade 2)
  - Head within ±5% of rated (ISO 9906 Grade 2)
  - Vibration within API 610 Figure 15 limits (Zone A or B)
- If test results acceptable: Proceed to acceptance sign-off
- If test results unacceptable: Investigate causes and retest after corrective action

**Verification:**
- Test results meet acceptance criteria

**Records:**
- Test results analysis report

**Source:** API 610 Section 6.9, ISO 9906 Grade 2 (acceptance criteria)

---

### Phase 5: Documentation and Acceptance

#### Step 5.1: Complete Test Records

**Action:**
- Compile complete installation and test record package:
  - Foundation inspection
  - Equipment setting and alignment records
  - Grouting records
  - Piping and electrical connection records
  - Pre-start inspection checklist
  - Performance test data and analysis
  - Vibration analysis
  - Photos of installed equipment

**Verification:**
- Record package complete

**Records:**
- Complete installation and test record package

**Source:** Project quality requirements

---

#### Step 5.2: Obtain Acceptance Sign-Offs

**Action:**
- Obtain acceptance sign-offs:
  - QA/QC Inspector — Installation quality acceptable
  - Commissioning Engineer — Performance test acceptable
  - Operations Manager — Equipment ready for turnover
  - Employer Representative (if required by contract) — Final acceptance

**Verification:**
- All required sign-offs obtained

**Records:**
- Acceptance certificates with signatures and dates

**Source:** Project quality and commissioning procedures

---

#### Step 5.3: File Records and Turnover to Operations

**Action:**
- File installation and test records in project document management system
- Provide copies to:
  - Operations (for baseline performance data)
  - Maintenance (for equipment history file)
  - Employer (per contract requirements)
- Conduct turnover meeting with operations personnel
- Provide training on equipment operation and maintenance (if required)

**Verification:**
- Records filed and distributed
- Operations personnel trained and equipment turned over

**Records:**
- Record distribution log
- Turnover meeting minutes
- Training records (if applicable)

**Source:** Project commissioning and turnover procedures

---

## Verification

### Verification Summary

| Phase | Activity | Verifier | Acceptance Criteria |
|-------|----------|----------|---------------------|
| **Installation** | Foundation | QA/QC | Level, clean, proper finish |
| **Installation** | Equipment setting | QA/QC | Location and elevation per drawings |
| **Installation** | Alignment | Millwright + QA/QC | Within API 610 tolerance |
| **Installation** | Grouting | QA/QC | Proper pour, adequate curing (7 days) |
| **Installation** | Piping connection | QA/QC | Independent support, proper gaskets/bolting |
| **Pre-Commissioning** | Pre-start checks | Commissioning Engineer | All checklist items complete |
| **Commissioning** | Performance test | Commissioning Engineer | Flow ±7%, Head ±5%, Vibration Zone A/B |
| **Acceptance** | Final acceptance | QA/QC + Operations + Employer | All records complete, equipment operational |

**Source:** Standard installation and commissioning verification process per Specification.md

## Records

### Documentation Outputs

For each pump, the following records shall be produced:

1. **Installation Records** — Foundation, setting, alignment, grouting
2. **Pre-Start Records** — Pre-commissioning inspection checklists
3. **Performance Test Records** — Test data, calculations, analysis
4. **Vibration Analysis Records** — Vibration measurements and acceptance
5. **Acceptance Certificates** — QA/QC and Employer sign-offs

**Source:** `_CONTEXT.md` (anticipated artifacts)

### Record Management

**Filing locations:**
- **During execution:** `1_Working/DEL-15.05_Pump_Installation_and_Test_Records/` organized by pump tag number
- **After acceptance:** Archive in project document management system as permanent quality records

**Retention:**
- Permanent (facility life, 25+ years)

**Distribution:**
- Operations, Maintenance, Employer per contract requirements

**Source:** Project quality and document control procedures

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Installation and testing requirements and record types
- Specification.md — Acceptance criteria for installation and performance
- Guidance.md — Installation and testing best practices and troubleshooting
- DEL-15.01 — Pump Design Drawing Set (installation per drawings)
- DEL-15.02 — Pump Technical Specification (performance requirements)
- DEL-15.03 — Pump Design Calculations (design performance for comparison)
- DEL-15.04 — Pump Data Sheet Package (vendor data baseline for testing)
