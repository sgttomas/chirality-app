# Specification: DEL-10.05 Railcar Unloading Installation & Test Records

## Scope

This specification defines the requirements for the **Railcar Unloading Installation & Test Records** within **PKG-10 Railcar Unloading System**.

**Purpose:** Provides evidence of completion, inspection, and testing for the railcar unloading system, demonstrating that equipment has been properly manufactured, installed, and tested in accordance with design requirements.

**Record Types:**

| Record Type | Purpose | Equipment Covered |
|-------------|---------|-------------------|
| FAT Records | Evidence of factory acceptance testing | Unloading arms (32), sump pumps |
| Installation Records | Evidence of correct installation | All PKG-10 equipment |
| Hydrostatic Test Records | Evidence of pressure testing | Header piping, containment |

**Anticipated Artifacts (from decomposition):**
- FAT records
- Installation records
- Hydrostatic test records

**Equipment Requiring Records:**
- Unloading arms (32 units)
- Quick-connect couplers (32 sets)
- Gravity flow header
- Spill containment pans
- Collection system
- Sump pumps
- Flow indicators (records may be part of PKG-20)

## Requirements

### Functional Requirements

| Req ID | Requirement | Source | Verification | Datasheet Link |
|--------|-------------|--------|--------------|----------------|
| FN-01 | Record package shall include FAT records for all 32 unloading arms | Decomposition | Record count | §Construction |
| FN-02 | Record package shall include FAT records for sump pumps | Decomposition | Record check | §Construction |
| FN-03 | Record package shall include installation records for all PKG-10 equipment | Decomposition | Record check | §Construction |
| FN-04 | Record package shall include hydrostatic test records for header piping | Decomposition | Record check | §Construction |
| FN-05 | Each record shall be traceable to specific equipment by tag number | **ASSUMPTION** — typical QA | Traceability review | §Construction |
| FN-06 | Each record shall reference the applicable specification/drawing | **ASSUMPTION** — typical QA | Document review | §Construction |
| FN-07 | **TBD** — Additional record requirements per Employer's Requirements | ER clauses **TBD** | **TBD** | — |

### Content Requirements (FAT Records)

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| FAT-01 | FAT record shall identify equipment (tag, model, serial number) | **ASSUMPTION** — typical | Document review |
| FAT-02 | FAT record shall reference test specification/procedure | DEL-10.02 | Document review |
| FAT-03 | FAT record shall document test conditions and results | **ASSUMPTION** — typical | Document review |
| FAT-04 | FAT record shall include pass/fail determination | **ASSUMPTION** — typical | Document review |
| FAT-05 | FAT record shall include required signatures/witness | **TBD** — ER | Document review |
| FAT-06 | FAT record shall include test certificates and calibration records | **ASSUMPTION** — typical | Document review |

### Content Requirements (Installation Records)

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| IR-01 | Installation record shall identify equipment and location | **ASSUMPTION** — typical | Document review |
| IR-02 | Installation record shall reference installation drawing | DEL-10.01 | Document review |
| IR-03 | Installation record shall document inspection checklist completion | **ASSUMPTION** — typical | Document review |
| IR-04 | Installation record shall note any as-built deviations | **ASSUMPTION** — typical | Document review |
| IR-05 | Installation record shall include required signatures | **TBD** — ER | Document review |

### Content Requirements (Hydrostatic Test Records)

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| HT-01 | Test record shall identify test section/boundary | **ASSUMPTION** — typical | Document review |
| HT-02 | Test record shall specify test parameters (pressure, duration, medium) | DEL-10.02 | Document review |
| HT-03 | Test record shall document test conditions and results | **ASSUMPTION** — typical | Document review |
| HT-04 | Test record shall include pass/fail determination against specification | DEL-10.02 | Document review |
| HT-05 | Test record shall include required signatures/witness | **TBD** — ER | Document review |
| HT-06 | Test record shall include pressure charts and calibration records | **ASSUMPTION** — typical | Document review |

### Quality Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| QA-01 | Records shall use project-standard templates | **TBD** — ER/project | Template review |
| QA-02 | Records shall be complete with no missing required fields | **ASSUMPTION** — typical | Completeness check |
| QA-03 | Record metadata shall include fields per Datasheet.md | Cross-document alignment | Document check |
| QA-04 | Records shall be reviewed and approved per QA/QC procedures | **ASSUMPTION** — typical | Sign-off verification |
| QA-05 | Records shall be archived in project document management system | **TBD** — ER/project | Archive verification |
| QA-06 | **TBD** — Additional quality requirements per Employer's Requirements | ER clauses **TBD** | **TBD** |

### Interface Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| IF-01 | FAT records shall align with DEL-10.02 specification requirements | Cross-deliverable | Document review |
| IF-02 | Installation records shall align with DEL-10.01 drawing requirements | Cross-deliverable | Document review |
| IF-03 | Test records shall align with DEL-10.02 test criteria | Cross-deliverable | Document review |
| IF-04 | Equipment tags shall match DEL-10.04 data sheets | Cross-deliverable | Tag verification |
| IF-05 | **TBD** — Interface with PKG-29 Testing deliverables | Interface | IDC review |

*Note: Dependencies coordinated externally (see `_DEPENDENCIES.md` — NOT_TRACKED).*

## Standards

**Applicable Standards (to be confirmed per Employer's Requirements):**

| Standard | Application | Source |
|----------|-------------|--------|
| **TBD** — ASME B31.3 | Hydrostatic test requirements for piping | ER / codes |
| **TBD** — Project quality procedures | Record templates and sign-off requirements | ER / contractor |
| **TBD** — CSA standards | Equipment testing requirements | ER / codes |

**Baseline Source Documents:**
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- `test/Volume_2_Part_1_Employers_Requirements.pdf`
- `test/Volume_2_Part_2_Employers_Requirements.pdf`
- `test/Volume_2_Part_3_Employers_Requirements.pdf`

## Verification

**Verification Matrix:**

| Req Category | Verification Method | Responsible | Procedure Link |
|--------------|---------------------|-------------|----------------|
| Functional (FN-xx) | Record count; completeness check | QA/QC | Procedure.md Step 4 |
| Content — FAT (FAT-xx) | Document review | QA/QC | Procedure.md Step 4 |
| Content — Installation (IR-xx) | Document review | QA/QC | Procedure.md Step 4 |
| Content — Hydrostatic (HT-xx) | Document review | QA/QC | Procedure.md Step 4 |
| Quality (QA-xx) | Completeness check; sign-off verification | QA/QC | Procedure.md Step 4 |
| Interface (IF-xx) | Cross-document review | QA/QC | Procedure.md Step 4 |

**Acceptance Criteria:**
- All 32 unloading arm FAT records complete and signed
- All sump pump FAT records complete and signed
- All installation records complete for PKG-10 equipment
- All hydrostatic test records complete with pass results
- All records traceable to equipment tags
- All required signatures/witnesses obtained
- Records archived in project document management system
- **TBD** — Additional acceptance criteria per Employer's Requirements

## Documentation

**Required Documentation Outputs:**

| Document | Quantity | Datasheet Link |
|----------|----------|----------------|
| FAT Records — Unloading Arms | 32 | §Construction |
| FAT Records — Sump Pumps | Per pump count | §Construction |
| Installation Records | Per equipment | §Construction |
| Hydrostatic Test Records | Per test section | §Construction |
| Record Index | 1 | Summary of all records |

**Document Control Requirements:**
- Record numbering per project document numbering procedure (**TBD**)
- Equipment tag traceability per project tagging standard (**TBD**)
- Signature/witness requirements per project quality procedures (**TBD**)
- Retention period per Employer's Requirements / regulatory (**TBD**)
- Archive format per project document control procedure (**TBD**)
- Filing: `2_Checking/` during review; `3_Issued/` upon approval (per Procedure.md §Records)
