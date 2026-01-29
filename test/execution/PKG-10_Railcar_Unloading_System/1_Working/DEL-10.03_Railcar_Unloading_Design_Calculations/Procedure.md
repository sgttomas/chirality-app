# Procedure: DEL-10.03 Railcar Unloading Design Calculations

## Purpose

This procedure defines the process for producing and managing the **Railcar Unloading Design Calculations** within **PKG-10 Railcar Unloading System**.

**Scope of Procedure:**
- Development of design calculations for railcar unloading system
- Independent check and approval workflow
- Documentation and issue

**Deliverable Type:** Calculation
**Responsible Party:** D&B Contractor
**Discipline:** Process

## Prerequisites

### Dependencies

- **Dependency Tracking:** NOT_TRACKED — dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`)
- **Upstream Inputs (typical):**

  | Input | Source | Status |
  |-------|--------|--------|
  | Project design basis | Employer's Requirements | **TBD** — clauses to be identified |
  | Throughput requirements | ER; project design basis | **TBD** |
  | Product properties | Product data sheets | **TBD** |
  | Preliminary layout | DEL-10.01 Design Drawing Set | **TBD** |
  | Equipment data | DEL-10.04 Data Sheet Package | **TBD** |
  | Regulatory requirements | Environmental regulations; ER | **TBD** |

### Reference Materials

| Reference | Location | Purpose |
|-----------|----------|---------|
| Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-10 scope; DEL-10.03 definition |
| Employer's Requirements | `test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf` | Design basis (clauses **TBD**) |
| Specification.md | This deliverable folder | Requirements for calculations |
| Guidance.md | This deliverable folder | Calculation principles and methods |
| Datasheet.md | This deliverable folder | Design parameters and inputs |
| DEL-10.01 | PKG-10 folder | Layout and geometry inputs |
| DEL-10.04 | PKG-10 folder | Equipment data inputs |
| Applicable codes/standards | **TBD** — per Specification.md §Standards | Calculation methods |

### Personnel Requirements

| Role | Qualification | Responsibility |
|------|---------------|----------------|
| Calculation Author | Process discipline; **TBD** qualifications | Calculation development |
| Checker | Process discipline; independent | Calculation check |
| Discipline Lead | Process discipline; approval authority | Calculation approval |
| Document Controller | Document control procedures | Issue and transmittal |

**ASSUMPTION:** Personnel competency requirements per project quality procedures.

## Steps

### Step 1: Define Calculation Basis and Scope

**Objective:** Establish calculation scope, inputs, and acceptance criteria.

**Actions:**
1. Review Specification.md §Scope for required calculations
2. Review Datasheet.md §Conditions for design parameters
3. Confirm calculation list:

   | Calculation | Purpose | Acceptance Criterion |
   |-------------|---------|---------------------|
   | Header pipe sizing | Size gravity flow header | Capacity > design throughput + margin |
   | Unloading rate | Verify throughput capacity | ≥ 1,000,000 MT/annum |
   | Containment volume | Size spill containment | ≥ regulatory requirement |

4. Identify input sources per Datasheet.md §Construction
5. Confirm acceptance criteria with discipline lead

**Output:** Approved calculation scope and basis.

**Verification:** Discipline lead sign-off on calculation basis.

### Step 2: Gather and Document Inputs

**Objective:** Collect and record all calculation inputs with sources.

**Actions:**
1. Gather design basis parameters from ER and project design basis
2. Obtain product properties (density, viscosity, temperature range)
3. Obtain layout geometry from DEL-10.01 (preliminary or approved)
4. Obtain equipment data from DEL-10.04 or vendor data
5. Identify regulatory requirements for containment
6. Document all inputs in calculation report:

   | Input Category | Parameters | Source | Status |
   |----------------|------------|--------|--------|
   | Throughput | 1,000,000 MT/annum; operating hours | ER; decomposition | Confirmed |
   | Product | Density, viscosity, temperature | Product data | **TBD** |
   | Geometry | Header length, elevations, routing | DEL-10.01 | **TBD** |
   | Equipment | Arm flow capacity, pressure drop | DEL-10.04; vendor | **TBD** |
   | Regulatory | Containment requirements | Regulations; ER | **TBD** |

**Output:** Documented input summary with sources.

**Verification:** Input review by checker (Step 5).

### Step 3: Document Assumptions

**Objective:** Record and justify all calculation assumptions.

**Actions:**
1. Identify assumptions required where inputs are incomplete
2. Document each assumption with justification:

   | Assumption | Basis | Impact |
   |------------|-------|--------|
   | Product density 920 kg/m³ | Typical canola oil at 15°C | Mass-volume conversions |
   | **TBD** simultaneous stations | Operating scenario | Header sizing |
   | **TBD** margin on throughput | Design conservatism | Capacity verification |
   | **TBD** containment scenario | Regulatory interpretation | Volume sizing |

3. Flag assumptions requiring confirmation
4. Apply Guidance.md considerations for conservative assumptions

**Output:** Documented assumption log.

**Verification:** Assumption review by checker (Step 5).

### Step 4: Execute Calculations

**Objective:** Perform calculations per Specification.md requirements.

**Actions:**

#### 4a: Unloading Rate Calculations
1. Calculate required throughput rate:
   - Annual: 1,000,000 MT
   - Operating hours: **TBD** (e.g., 8,000 hr/yr)
   - Hourly rate: calculate
2. Determine flow rate per station
3. Determine number of simultaneous stations
4. Verify total capacity meets requirement
5. Document results and comparison to criteria

#### 4b: Header Pipe Sizing Calculations
1. Determine design flow rate from Step 4a
2. Select sizing method per Guidance.md (Manning or Darcy-Weisbach)
3. Size header pipe:
   - Calculate required diameter
   - Verify velocity within limits
   - Confirm slope achievable
4. Apply design margin
5. Document results and selected size

#### 4c: Containment Volume Calculations
1. Identify regulatory requirements per Guidance.md
2. Determine worst-case spill volume (largest railcar or header section)
3. Add rainfall allowance if applicable
4. Add freeboard
5. Calculate total required containment volume
6. Compare to containment sizing from DEL-10.01 layout
7. Document results and compliance verification

**Output:** Draft calculation package with results.

**Traceability:**

| Requirement | Calculation | Result | Status |
|-------------|-------------|--------|--------|
| FN-01: Header sizing | Header Pipe Sizing | **TBD** | Draft |
| FN-02: Unloading rate | Unloading Rate | **TBD** | Draft |
| FN-03: Containment volume | Containment Volume | **TBD** | Draft |
| PF-01: Header capacity | Header Pipe Sizing | **TBD** | Draft |
| PF-02: Throughput | Unloading Rate | ≥ 1,000,000 MT/a | Draft |
| PF-03: Containment compliance | Containment Volume | **TBD** | Draft |

### Step 5: Independent Check

**Objective:** Verify calculation accuracy and completeness.

**Actions:**
1. Issue calculation package to independent checker
2. Checker reviews:
   - Input accuracy and sources (IN-01 through IN-05)
   - Assumption validity and conservatism
   - Method appropriateness (QA-03)
   - Arithmetic accuracy
   - Software output verification if applicable (QA-04)
   - Results vs. acceptance criteria
   - Documentation completeness (FN-04)
3. Resolve checker comments
4. Update calculation package

**Output:** Checked calculation package.

**Verification:** Checker sign-off (QA-01).

### Step 6: Approval and Issue

**Objective:** Obtain approval and issue calculation package.

**Actions:**
1. Submit checked calculation package for discipline lead approval
2. Discipline lead reviews:
   - Technical completeness
   - Results acceptable
   - Checker comments resolved
3. Obtain sign-offs (author, checker, approver)
4. Finalize document metadata (Datasheet.md §Attributes):
   - Calculation number (confirmed)
   - Revision (initial issue)
   - Software used
   - Date
   - Sign-offs
5. Prepare transmittal per project document control procedure (**TBD**)
6. Issue calculation package
7. Communicate results to DEL-10.01, DEL-10.02, DEL-10.04 for incorporation

**Output:** Issued calculation package.

**Verification:**
- Discipline lead approval sign-off
- Document controller confirmation of issue

## Verification

**Verification Summary:**

| Step | Verification Activity | Responsible | Record |
|------|----------------------|-------------|--------|
| 1 | Scope/basis approval | Discipline lead | Approved basis |
| 2 | Input documentation | Author | Input summary |
| 3 | Assumption documentation | Author | Assumption log |
| 4 | Calculation completion | Author | Draft calculations |
| 5 | Independent check | Checker | Checker sign-off |
| 6 | Approval | Discipline lead | Approval sign-off |
| 6 | Issue confirmation | Document controller | Transmittal record |

**Requirement Verification Matrix:**

| Req ID | Requirement Summary | Verification Step | Method |
|--------|---------------------|-------------------|--------|
| FN-01 | Header pipe sizing | 4b, 5 | Calculation check |
| FN-02 | Unloading rate | 4a, 5 | Calculation check |
| FN-03 | Containment volume | 4c, 5 | Calculation check |
| FN-04 | Document inputs/assumptions | 2, 3, 5 | Document review |
| FN-05 | Traceability | 2, 5 | Document review |
| PF-01 | Header capacity | 4b, 5 | Results vs. criteria |
| PF-02 | Throughput capacity | 4a, 5 | Results vs. criteria |
| PF-03 | Containment compliance | 4c, 5 | Results vs. criteria |
| IN-01–05 | Input requirements | 2, 5 | Input review |
| QA-01 | Independent check | 5 | Checker sign-off |
| QA-02 | Document metadata | 6 | Document check |
| QA-03 | Reproducible methods | 4, 5 | Method review |
| QA-04 | Software verification | 4, 5 | Output review |

## Records

**Documentation Outputs:**

| Record | Description | Filing Location |
|--------|-------------|-----------------|
| Header Pipe Sizing Calculation | Gravity flow header sizing | `3_Issued/` |
| Unloading Rate Calculations | Throughput verification | `3_Issued/` |
| Containment Volume Calculations | Containment sizing | `3_Issued/` |
| Calculation basis | Approved scope and inputs | `1_Working/` |
| Assumption log | Documented assumptions | `1_Working/` (part of calc) |
| Checker comments | Review records | `1_Working/` |
| Transmittal record | Issue documentation | `1_Working/` |

**Record Management:**
- Working records: `1_Working/` in deliverable folder
- Review packages: `2_Checking/To/` during review cycle
- Issued calculations: `3_Issued/` upon approval
- Retention requirements: **TBD** — per project document control procedure
- **ASSUMPTION:** Electronic records maintained in project document management system
