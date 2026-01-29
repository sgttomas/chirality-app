# Specification: DEL-11.03 Marine Loading Design Calculations

## Scope

This specification defines the requirements for **Marine Loading Design Calculations** within **PKG-11 Marine Loading System**.

**Purpose:** Provides the engineering basis and sizing/verification calculations for the marine loading system, demonstrating compliance with design requirements and deriving constraints for layout drawings and equipment specifications.

**Package scope (PKG-11):**
- Powered loading arm (articulated boom with powered slew/luff)
- Emergency release coupling (ERC)
- Double-walled export pipe
- Leak detection system
- Nitrogen supply provisions
- Operator shelter

**Anticipated deliverable artifacts:**
- Loading arm reach/envelope calculations
- Drainage calculations
- Nitrogen purge calculations

**Objectives served (per decomposition Section 6):**
- OBJ-1 Safe & Reliable Operation
- OBJ-2 Throughput Capacity (1,000,000 MT/annum)
- OBJ-4 Operational Flexibility
- OBJ-7 Environmental Protection

## Related Deliverables (PKG-11)

| Deliverable | Relationship |
|-------------|--------------|
| DEL-11.01 Marine Loading Design Drawing Set | Receives envelope/clearance constraints from calculations |
| DEL-11.02 Marine Loading Technical Specification | Provides design basis; receives verified sizing outputs |
| DEL-11.04 Marine Loading Data Sheet Package | Receives duty points and verified requirements |
| DEL-11.05 Marine Loading Installation & Test Records | Test records verify calculated values |
| DEL-11.06 Marine Loading Arm OEM Qualification Package | Provides OEM arm data as calculation inputs |

## Requirements

### General Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| CALC-001 | Each calculation shall be uniquely identified (calculation ID) and revision controlled | Document review |
| CALC-002 | Each calculation shall include originator, checker, and approver sign-off | Check records |
| CALC-003 | Calculation register shall be provided listing all calculations with IDs, titles, and revision status | Document review |
| CALC-004 | All calculations shall comply with project QA/QC procedures | QA records |

### Calculation Content Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| CALC-005 | Each calculation shall clearly state objective/scope | Completeness check |
| CALC-006 | Each calculation shall identify governing codes/standards and acceptance criteria | Completeness check |
| CALC-007 | Each calculation shall document all inputs with source references | Traceability review |
| CALC-008 | Each calculation shall explicitly label assumptions as **ASSUMPTION** | Completeness check |
| CALC-009 | Each calculation shall state methodology and tool/software versions | Completeness check |
| CALC-010 | Each calculation shall present results with units and appropriate precision | Technical review |
| CALC-011 | Each calculation shall include conclusions and implications | Technical review |
| CALC-012 | Each calculation shall identify output constraints for drawings/specifications | Cross-reference check |

### Loading Arm Reach/Envelope Calculations

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| ENV-001 | Calculate required loading arm reach (outboard and inboard) to accommodate design vessel range | Technical review |
| ENV-002 | Determine operating envelope (slew/luff limits) at berth location | Technical review |
| ENV-003 | Verify clearance to marine structures, fenders, and vessel hull at all operating positions | Technical review |
| ENV-004 | Confirm ERC activation envelope allows safe vessel drift limits | Technical review |
| ENV-005 | Document envelope constraints for inclusion on DEL-11.01 GA drawings | Cross-reference check |

**Inputs (TBD until available):**

| Input | Source | Status |
|-------|--------|--------|
| Berth geometry (platform level, edge location) | PKG-08 Marine Structures | **TBD** |
| Design vessel parameters (manifold height range, beam, approach angles) | ER / marine studies | **TBD** |
| Fender deflection at design berthing energy | DEL-08.06/08.07 | **TBD** |
| OEM arm envelope data (reach, slew, luff limits) | DEL-11.06 OEM data | **TBD** |
| Tidal range | Site data | **TBD** |

**Outputs:**
- Operating envelope plot (plan and elevation)
- Minimum/maximum reach requirements
- Clearance requirements for layout
- ERC drift limit verification

### Drainage Calculations

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| DRN-001 | Determine catchment areas for marine loading containment | Technical review |
| DRN-002 | Calculate design rainfall runoff (storm event criteria per project basis) | Technical review |
| DRN-003 | Size drainage channels/pipes for design flow (if in scope) | Technical review |
| DRN-004 | Size containment sump capacity for design spill volume plus rainfall | Technical review |
| DRN-005 | Size sump pump (if required) for emptying within acceptable time | Technical review |
| DRN-006 | Document drainage constraints for DEL-11.01 layout and PKG-03 coordination | Cross-reference check |

**Inputs (TBD until available):**

| Input | Source | Status |
|-------|--------|--------|
| Containment area footprint | DEL-11.01 layout | **TBD** |
| Design rainfall intensity (return period) | Site data / ER | **TBD** |
| Design spill volume (ERC release + drip tray capacity) | DEL-11.02 | **TBD** |
| Discharge point / OWS interface | PKG-03 Drainage | **TBD** |

**Outputs:**
- Design flow rates
- Drain/channel sizing
- Sump capacity requirements
- Pump sizing (if required)

### Nitrogen Purge Calculations

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| N2-001 | Determine volume to be purged (loading arm + header pipe) | Technical review |
| N2-002 | Calculate nitrogen flow rate to achieve target O₂ concentration in acceptable time | Technical review |
| N2-003 | Verify nitrogen supply capacity is adequate | Technical review |
| N2-004 | Document nitrogen supply requirements for DEL-18 utilities coordination | Cross-reference check |

**Inputs (TBD until available):**

| Input | Source | Status |
|-------|--------|--------|
| System volume (loading arm + pipe header) | DEL-11.01 / OEM data | **TBD** |
| Target O₂ concentration | DEL-11.02 / ER | **TBD** |
| Maximum acceptable purge time | DEL-11.02 / ER | **TBD** |
| Nitrogen supply pressure and temperature | DEL-18 utilities | **TBD** |

**Outputs:**
- Required nitrogen flow rate
- Purge time at design flow
- Supply capacity confirmation

### Interface Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| INT-001 | Calculations shall identify and document all interface assumptions | Completeness check |
| INT-002 | Output constraints shall be formally communicated to DEL-11.01 and DEL-11.02 | Cross-reference check |
| INT-003 | Calculations requiring vendor/OEM data shall document data source, revision, and date | Traceability review |

**Note:** Dependency tracking is NOT_TRACKED; interfaces are coordinated externally per `_DEPENDENCIES.md`.

### Quality Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| QA-001 | Independent check required for each calculation prior to issue | Check records |
| QA-002 | Checker shall verify input sources, methodology, arithmetic, and conclusions | Check records |
| QA-003 | TBD items that materially affect design shall be tracked to closure | TBD register |
| QA-004 | Software calculations shall include output verification (spot checks, reasonableness) | Check records |

## Standards

| Standard | Applicability | Status |
|----------|---------------|--------|
| Employer's Requirements (ER) | Design basis and acceptance criteria | Clause references **TBD** |
| ASME B31.3 | Pipe sizing/stress (if applicable) | **TBD** |
| Project calculation standards | Format and content | **TBD** |
| Project QA/QC procedures | Check and approval | **TBD** |

## Verification

**Verification methods for Calculation deliverables:**

| Method | Description | Applies To |
|--------|-------------|------------|
| Independent check | Qualified checker reviews inputs, methodology, results | All calculations |
| Software verification | Spot checks of software outputs | ENV-001, DRN-003, N2-002 |
| Reasonableness review | Sanity check of results against expectations | All calculations |
| Cross-reference check | Confirm outputs reflected in drawings/specifications | CALC-012, INT-002 |

**Acceptance criteria:**
- Calculation package complete with register and sign-offs
- All inputs traceable to sources
- All assumptions labeled and tracked
- Outputs/constraints reflected in DEL-11.01 and DEL-11.02

## Documentation

**Required documentation outputs:**
- Loading arm reach/envelope calculations
- Drainage calculations
- Nitrogen purge calculations
- Calculation register/index

**Documentation requirements:**
- All documents shall comply with project document control procedures
- Revision control per project numbering system — **TBD**
- Format: **TBD** (project document management requirements)

---

**Pass 3 Enrichment Notes (Final Quality Check):**
- Verified all 34 requirements have unique IDs: CALC-001 to CALC-012 (12), ENV-001 to ENV-005 (5), DRN-001 to DRN-006 (6), N2-001 to N2-004 (4), INT-001 to INT-003 (3), QA-001 to QA-004 (4)
- Verified all requirements include verification method column
- Verified calculation topics (3: envelope, drainage, nitrogen) align with Datasheet §Construction and Procedure §Steps 3-5
- Verified inputs tables (ENV: 5 inputs, DRN: 4 inputs, N2: 4 inputs) align with Procedure §Prerequisites (10 inputs)
- Verified outputs lists specify constraints for DEL-11.01 and DEL-11.02
- Verified Related Deliverables table (5 deliverables) consistent with Datasheet §Cross-Document Links
- Verified Standards table (4 entries) and Verification methods (4 methods)
- Verified acceptance criteria (4 items) align with Datasheet §Deliverable Acceptance (6 criteria)
- Confirmed terminology consistent with DEL-11.01/11.02: loading arm envelope, drainage, nitrogen purge
- All TBDs and ASSUMPTIONs retained with proper labeling
- Pass 3 complete — document ready for WORKING_ITEMS session
