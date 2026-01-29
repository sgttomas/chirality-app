# Guidance: DEL-10.05 Railcar Unloading Installation & Test Records

## Purpose

This guidance document supports the development of the **Railcar Unloading Installation & Test Records** for **PKG-10 Railcar Unloading System**.

The Installation & Test Records provide evidence of completion, inspection, and testing for the railcar unloading system, demonstrating that the 32 unloading stations and associated equipment have been properly manufactured, installed, and tested in accordance with design requirements.

**Deliverable Classification:**
- Type: Record
- Discipline: Process
- Responsible: D&B Contractor (QA/QC)

## Principles

**Project Objective Alignment:**

This deliverable supports the following project objectives (per decomposition §6 Objective Mapping):

| Objective | ID | Relevance to DEL-10.05 |
|-----------|-----|------------------------|
| Safe & Reliable Operation | OBJ-1 | Records demonstrate equipment meets safety and reliability requirements |
| Throughput Capacity (1,000,000 MT/annum) | OBJ-2 | FAT records verify equipment capacity |
| Operational Flexibility | OBJ-4 | Installation records verify correct configuration |
| Environmental Protection | OBJ-7 | Test records verify containment integrity |

**Quality Record Principles:**

| Principle | Application | Specification Link |
|-----------|-------------|-------------------|
| Traceability | Every record traceable to specific equipment by tag | FN-05; IF-04 |
| Completeness | All required fields populated; no missing data | QA-02 |
| Accuracy | Records accurately reflect inspection/test results | FAT-03; IR-03; HT-03 |
| Timeliness | Records completed contemporaneously with work | QA-04 |
| Accountability | Proper signatures and witness as required | FAT-05; IR-05; HT-05 |

**Record Content Principles:**

| Principle | Rationale | Quality Link |
|-----------|-----------|--------------|
| Equipment identification | Clear identification enables traceability | FN-05; FAT-01; IR-01; HT-01 |
| Reference to specifications | Links test/inspection to requirements | FN-06; FAT-02; IR-02; HT-02 |
| Pass/fail determination | Clear acceptance decision | FAT-04; HT-04 |
| Evidence preservation | Attachments (photos, charts, certificates) support record | FAT-06; HT-06 |
| Retention | Records archived for required retention period | QA-05 |

## Considerations

**FAT Record Considerations:**

| Factor | Consideration | Guidance |
|--------|---------------|----------|
| Test scope | Define what tests are required per DEL-10.02 | Coordinate with specification requirements |
| Witness requirements | Determine if employer witness required | **TBD** — per ER/project |
| Test location | Vendor facility or third-party test house | Coordinate with procurement |
| Documentation | Ensure vendor provides required documentation format | Specify in purchase order |
| Timing | FAT must be complete before shipping | Schedule coordination |

**Installation Record Considerations:**

| Factor | Consideration | Guidance |
|--------|---------------|----------|
| Installation checklist | Define checklist items per DEL-10.02 | Alignment, supports, connections, clearances |
| Inspection hold points | Identify mandatory inspection points | **TBD** — per ER/project |
| As-built documentation | Capture any deviations from design | Link to as-built drawings |
| Photo documentation | Photos for key installation stages | Support future reference |
| NCR handling | Process for non-conformances | Per project quality procedures |

**Hydrostatic Test Considerations:**

| Factor | Consideration | Guidance |
|--------|---------------|----------|
| Test boundaries | Define test sections per header layout | Coordinate with DEL-10.01 |
| Test pressure | Per DEL-10.02 specification / code requirements | Typically 1.5x design pressure |
| Test duration | Per DEL-10.02 specification / code requirements | Typically minimum hold time |
| Test medium | Water or other suitable medium | Consider product compatibility, disposal |
| Ambient conditions | Temperature limits for testing | Per code requirements |
| Witness requirements | Determine if employer witness required | **TBD** — per ER/project |

**Equipment-Specific Considerations:**

| Equipment | Key Test/Inspection Focus |
|-----------|--------------------------|
| Unloading Arms | Articulation, reach, seal integrity, quick-connect operation |
| Quick-Connects | Connection/disconnection, seal integrity, drip-free operation |
| Header Piping | Hydrostatic test, support installation, slope verification |
| Containment | Leak test, drainage test, structural inspection |
| Sump Pumps | Motor/electrical, flow/head performance, controls |

## Trade-offs

**Record Documentation Trade-offs:**

| Trade-off | Option A | Option B | Considerations |
|-----------|----------|----------|----------------|
| Record detail | Minimal required content | Comprehensive documentation | Effort vs. future reference value |
| Photo documentation | Key stages only | Extensive photo record | Storage vs. completeness |
| Electronic vs. paper | Electronic records | Paper originals | Accessibility vs. authentication |
| Individual vs. combined | Separate record per item | Combined records per system | Traceability vs. volume |

**ASSUMPTION:** Trade-off decisions to be documented in project quality procedures.

**Schedule vs. Quality Trade-offs:**
- Concurrent testing with installation vs. sequential
- Batch testing vs. individual equipment testing
- **ASSUMPTION:** Quality records must be complete regardless of schedule pressure

## Examples

**Reference Examples and Precedents:**

| Example Type | Source | Application |
|--------------|--------|-------------|
| FAT record templates | **TBD** — project standards, vendor examples | Format and content |
| Installation checklist templates | **TBD** — project quality procedures | Inspection items |
| Hydrostatic test templates | ASME / code examples | Test record format |
| Project quality procedures | **TBD** — Employer's Requirements / contractor | Process and sign-offs |

**Typical FAT Record Workflow:**

```
1. Pre-FAT: Confirm test procedure, witness requirements
2. FAT execution: Vendor performs tests per procedure
3. Documentation: Vendor completes test record
4. Review: Contractor reviews and signs
5. Witness: Employer witness signs (if required)
6. Acceptance: Pass/fail determination
7. Archive: Record filed in project DMS
```

**Typical Installation Record Workflow:**

```
1. Pre-installation: Obtain drawings, prepare checklist
2. Installation: Contractor installs equipment
3. Inspection: QA/QC inspects per checklist
4. Documentation: Complete installation record
5. As-built: Note any deviations
6. Sign-off: Inspector, QA/QC sign
7. Archive: Record filed in project DMS
```

**Typical Hydrostatic Test Workflow:**

```
1. Pre-test: Define boundaries, prepare system, notify witness
2. Fill and pressurize: Fill with test medium, raise to test pressure
3. Hold: Maintain test pressure for required duration
4. Inspect: Check for leaks during hold
5. Documentation: Record pressure readings, observations
6. Accept/reject: Pass/fail determination
7. Depressurize and drain: Safe depressurization
8. Sign-off: Test engineer, QA/QC, witness sign
9. Archive: Record filed in project DMS
```

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | No conflicts identified | — | — | — | — | — |

*Note: `_REFERENCES.md` is not yet populated with specific Employer's Requirements clauses. Conflicts may emerge when ER content is reviewed. Update this table as needed during WORKING_ITEMS sessions.*

**Cross-Document Consistency Check:**

| Check | Status |
|-------|--------|
| Datasheet equipment list matches Specification requirements | Verified — 32 arms, pumps, header, containment covered |
| Specification content requirements have guidance | Verified — considerations address all record types |
| Specification requirements have verification in Procedure | Verified — Procedure.md steps include completeness check |
| Equipment tags link to DEL-10.04 data sheets | To be verified during execution |
| Test criteria link to DEL-10.02 specification | To be verified during execution |
| Terminology consistent across documents | Verified — consistent record type naming |
