# Specification: DEL-10.04 Railcar Unloading Data Sheet Package

## Scope

This specification defines the requirements for the **Railcar Unloading Data Sheet Package** within **PKG-10 Railcar Unloading System**.

**Purpose:** Defines and substantiates equipment for the railcar unloading system, documenting design parameters, operating conditions, and equipment specifications for procurement, installation, and operation.

**Equipment to be Documented:**

| Equipment | Quantity | Data Sheet Type |
|-----------|----------|-----------------|
| Unloading Arms | 32 | Individual equipment data sheets |
| Quick-Connect Couplers | 32 sets | Equipment data sheets (combined or separate) |
| Sump Pumps | **TBD** | Equipment data sheet |

**Anticipated Artifacts (from decomposition):**
- Unloading arm data sheets (32)
- Quick-connect coupler data sheets
- Sump pump data sheet

**Exclusions:**
- Flow indicator data sheets (covered by PKG-20 Field Instrumentation)
- Electrical equipment data sheets (covered by PKG-17 Electrical)
- Piping material data (covered by PKG-14 Process Piping)

## Requirements

### Functional Requirements

| Req ID | Requirement | Source | Verification | Datasheet Link |
|--------|-------------|--------|--------------|----------------|
| FN-01 | Data Sheet Package shall include data sheets for all 32 unloading arms | Decomposition | Document count | §Construction |
| FN-02 | Data Sheet Package shall include data sheets for quick-connect couplers | Decomposition | Document check | §Construction |
| FN-03 | Data Sheet Package shall include data sheet(s) for sump pump(s) | Decomposition | Document check | §Construction |
| FN-04 | Each data sheet shall include equipment identification (tag, service, location) | **ASSUMPTION** — typical | Document review | §Construction |
| FN-05 | Each data sheet shall include process/operating conditions | **ASSUMPTION** — typical | Document review | §Construction |
| FN-06 | Each data sheet shall include mechanical/construction details | **ASSUMPTION** — typical | Document review | §Construction |
| FN-07 | Each data sheet shall include material specifications | **ASSUMPTION** — typical | Document review | §Construction |
| FN-08 | **TBD** — Additional data sheet requirements per Employer's Requirements | ER clauses **TBD** | **TBD** | — |

### Content Requirements (Unloading Arms)

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| UA-01 | Data sheet shall specify arm type, size, and configuration | DEL-10.02 | Document review |
| UA-02 | Data sheet shall specify process conditions (product, flow, temperature, pressure) | DEL-10.02; DEL-10.03 | Document review |
| UA-03 | Data sheet shall specify materials for wetted parts and seals | DEL-10.02 | Document review |
| UA-04 | Data sheet shall specify quick-connect coupler details | DEL-10.02 | Document review |
| UA-05 | Data sheet shall specify reach/envelope requirements | DEL-10.01 | Document review |
| UA-06 | Data sheet shall reference applicable standards | DEL-10.02 | Document review |

### Content Requirements (Sump Pumps)

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| SP-01 | Data sheet shall specify pump type, size, and driver | DEL-10.02 | Document review |
| SP-02 | Data sheet shall specify process conditions (fluid, flow, head, temperature) | DEL-10.03 | Document review |
| SP-03 | Data sheet shall specify materials for wetted parts | DEL-10.02 | Document review |
| SP-04 | Data sheet shall specify electrical data (motor, area classification) | PKG-17 interface | Document review |
| SP-05 | Data sheet shall reference applicable standards | DEL-10.02 | Document review |

### Quality Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| QA-01 | Data sheets shall use consistent tagging scheme across package | **ASSUMPTION** — typical | Tag audit |
| QA-02 | Data sheets shall use consistent units throughout | **ASSUMPTION** — typical | Unit check |
| QA-03 | Data sheet metadata shall include fields per Datasheet.md | Cross-document alignment | Document check |
| QA-04 | Data sheets shall be independently checked for completeness/accuracy | **ASSUMPTION** — typical D&B | Checker sign-off |
| QA-05 | Data sheets shall align with DEL-10.02 specification requirements | Cross-deliverable | Document review |
| QA-06 | **TBD** — Additional quality requirements per Employer's Requirements | ER clauses **TBD** | **TBD** |

### Interface Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| IF-01 | Data sheets shall reference P&ID and drawing numbers from DEL-10.01 | Cross-deliverable | Document review |
| IF-02 | Data sheet process conditions shall align with DEL-10.03 calculations | Cross-deliverable | Calculation review |
| IF-03 | Sump pump electrical data shall coordinate with PKG-17 | Interface | IDC review |
| IF-04 | **TBD** — Additional interface requirements | ER clauses **TBD** | IDC review |

*Note: Dependencies coordinated externally (see `_DEPENDENCIES.md` — NOT_TRACKED).*

## Standards

**Applicable Standards (to be confirmed per Employer's Requirements):**

| Standard | Application | Source |
|----------|-------------|--------|
| **TBD** — API standards | Pump data sheets | ER / industry practice |
| **TBD** — ISA standards | Data sheet formats | ER / industry practice |
| **TBD** — Project data sheet templates | Standard formats | ER / contractor |

**Baseline Source Documents:**
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- `test/Volume_2_Part_1_Employers_Requirements.pdf`
- `test/Volume_2_Part_2_Employers_Requirements.pdf`
- `test/Volume_2_Part_3_Employers_Requirements.pdf`

## Verification

**Verification Matrix:**

| Req Category | Verification Method | Responsible | Procedure Link |
|--------------|---------------------|-------------|----------------|
| Functional (FN-xx) | Document review; count check | Discipline lead | Procedure.md Step 5 |
| Content — Arms (UA-xx) | Data sheet review | Discipline lead | Procedure.md Step 5 |
| Content — Pumps (SP-xx) | Data sheet review | Discipline lead | Procedure.md Step 5 |
| Quality (QA-xx) | Tag audit; unit check; checker sign-off | Document control | Procedure.md Step 5 |
| Interface (IF-xx) | Cross-document review; IDC | Multi-discipline | Procedure.md Step 5 |

**Acceptance Criteria:**
- All 32 unloading arm data sheets complete and consistent
- Quick-connect coupler data sheets complete
- Sump pump data sheet(s) complete
- All data sheets aligned with DEL-10.02 specification requirements
- Tagging and units consistent throughout package
- Independent checker sign-off obtained
- **TBD** — Additional acceptance criteria per Employer's Requirements

## Documentation

**Required Documentation Outputs:**

| Document | Quantity | Datasheet Link |
|----------|----------|----------------|
| Unloading Arm Data Sheets | 32 | §Construction |
| Quick-Connect Coupler Data Sheets | 32 or combined | §Construction |
| Sump Pump Data Sheet | 1+ | §Construction |
| Equipment List | 1 | Summary of all equipment |

**Document Control Requirements:**
- Data sheet numbering per project document numbering procedure (**TBD**)
- Equipment tagging per project tagging standard (**TBD**)
- Revision control per project document control procedure (**TBD**)
- Transmittal per project document control procedure (**TBD**)
- Filing: `2_Checking/` during review; `3_Issued/` upon approval (per Procedure.md §Records)
