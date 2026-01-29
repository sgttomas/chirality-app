# Guidance: DEL-12.05 Metering Installation & Test Records

## Purpose

This guidance document supports the development of **Metering Installation & Test Records** for **PKG-12 Product Transfer & Metering**.

DEL-12.05 provides evidence of completion, inspection, and testing for custody transfer metering (Source: Decomposition:360). The deliverable is classified as a **Record** under the **Process** discipline, produced by the **D&B Contractor (QA/QC)**.

### Deliverable Intent

The metering installation and test records serve as auditable evidence that custody transfer metering equipment was:
1. **Properly specified** — equipment meets DEL-12.02 specification requirements
2. **Correctly installed** — installation per DEL-12.01 drawings and manufacturer requirements
3. **Accurately calibrated** — calibration traceable to national measurement standards (Measurement Canada, NIST, or equivalent)
4. **Performance verified** — accuracy verification through proving or testing demonstrates meters meet accuracy requirements

These records close the quality loop from specification (DEL-12.02) through design (DEL-12.01), sizing (DEL-12.03), procurement (DEL-12.04), installation, and testing, demonstrating compliance with project requirements, ER requirements, and regulatory requirements (Measurement Canada if applicable).

### Downstream Use

The record package serves multiple critical purposes:

- **Project closeout** — records demonstrate completion and acceptance of metering scope; required for project handover to client
- **Regulatory compliance** — records may be required for Measurement Canada approval for custody transfer in Canada; calibration traceability and proving records demonstrate regulatory compliance
- **Commercial confidence** — records provide buyer and seller confidence in measurement accuracy for custody transfer transactions; third-party witness signatures (if required) provide independent verification
- **Operational reference** — records provide baseline data for ongoing operations: initial meter factors for comparison to future proving results, calibration intervals for maintenance scheduling, acceptance criteria for ongoing proving
- **Audit trail** — records provide auditable evidence for client audit, third-party audit, or regulatory audit (Measurement Canada inspection)
- **Warranty and claims** — records document equipment condition and performance at installation; baseline for warranty claims or performance disputes

## Principles

### Record Development Rationale

| Principle | Rationale |
|-----------|-----------|
| Evidence of Compliance | Records demonstrate that custody transfer metering meets DEL-12.02 specification acceptance criteria (per Specification.md REQ-05): proving results verify accuracy, calibration certificates verify traceability, test records verify functionality; without records, compliance cannot be demonstrated even if equipment is correctly installed |
| Traceability | Each record must be traceable to specific equipment (tag number and serial number per Specification.md REQ-02, REQ-10, REQ-11) and to acceptance criteria (from DEL-12.02 and DEL-12.03): tag numbers link records to P&IDs and drawings; serial numbers link records to physical equipment; acceptance criteria link records to requirements; traceability enables audit and future reference |
| Auditability | Records must be complete, legible, and organized for third-party audit (per Specification.md REQ-17): complete (all required fields populated, signatures obtained), legible (readable text, clear scans), organized (structured package with index and sections); auditors (client, third-party, Measurement Canada) must be able to verify compliance from records |
| Regulatory Support | Custody transfer calibration and proving records may be required for regulatory compliance (per Specification.md REQ-06): Measurement Canada approval for custody transfer in Canada may require specific calibration traceability and proving documentation; records demonstrate compliance with Weights and Measures Act and regulations (ASSUMPTION; TBD verification from Measurement Canada requirements) |
| No Fabrication | Records must be actual test results, not fabricated or assumed values; each record must be signed by authorized personnel who performed or witnessed test; fabricated records undermine compliance demonstration and may have legal implications for custody transfer |

### Custody Transfer Record Principles

Custody transfer metering requires specific attention to calibration traceability and accuracy verification:

| Principle | Application |
|-----------|-------------|
| Calibration Traceability | Calibration certificates must show unbroken traceability chain to national measurement standards (per Specification.md REQ-06): certificate states "Traceable to Measurement Canada" (for Canada) or "Traceable to NIST" (for US) or equivalent; traceability is through calibration standard (reference standard) which itself has calibration certificate traceable to national standard; unbroken chain: equipment → calibration standard → national standard; traceability is essential for custody transfer approval and commercial confidence; Measurement Canada may require specific traceability for approval |
| Proving Documentation | Proving records must document method, results, and acceptance verification per applicable standard (per Specification.md REQ-08): proving method per DEL-12.02 (in-line prover, portable prover, master meter), proving run data (individual runs for repeatability verification; typical 3-5 runs per API MPMS Chapter 4), meter factor calculation (meter factor = true volume from prover / indicated volume from meter), acceptance verification (compare to acceptance criteria from DEL-12.03: meter factor within range, repeatability acceptable, drift acceptable), signature (authorized personnel confirm acceptance) |
| Witnessing | Third-party or client witnessing may be required for custody transfer verification (per Specification.md REQ-16): ER may specify witnessing for hold points (FAT, installation inspection, proving); Measurement Canada may require witnessed verification for approval; witness signature provides independent verification; witness qualifications may be specified (certified inspector, Measurement Canada representative); witnessing adds cost and coordination but provides assurance and regulatory compliance |

### Objective Alignment

| Objective | Record Guidance |
|-----------|-----------------|
| OBJ-10 Custody Transfer Accuracy (Commercial Transactions) | Records provide auditable evidence of calibration and accuracy verification; demonstrate that installed metering meets custody transfer accuracy requirements (per Specification.md REQ-05, REQ-06, REQ-07, REQ-08): **Calibration certificates** demonstrate measurement traceability to national standards (Measurement Canada, NIST); traceability is foundation of custody transfer confidence; **Proving records** demonstrate meters meet accuracy class per DEL-12.02 (e.g., ±0.15%, ±0.25%; TBD); proving verifies accuracy at operating conditions; **Uncertainty documentation** from DEL-12.03 links to proving acceptance criteria; **Regulatory compliance** records enable Measurement Canada approval or equivalent for custody transfer; records provide commercial confidence for custody transfer transactions (Source: Decomposition:789) |
| OBJ-6 Regulatory Compliance | Records demonstrate compliance with regulatory requirements for custody transfer in Canada: Measurement Canada approval may require calibration traceability, proving records, periodic verification records; records provide evidence for regulatory inspection or audit (ASSUMPTION based on Canadian location and custody transfer application; TBD verification from Measurement Canada requirements or ER Vol 2 Part 2) |

## Considerations

### Record Content Considerations

Factors affecting record package content:

| Factor | Consideration |
|--------|---------------|
| Minimum Content | At minimum per Decomposition:360: calibration certificates and accuracy verification records; **Calibration certificates** for all custody transfer equipment (flow meters, temperature transmitters, pressure transmitters if applicable); **Accuracy verification** through proving for flow meters; minimum content satisfies decomposition but may not satisfy all ER or regulatory requirements |
| Equipment Coverage | Records required for all custody transfer metering equipment per Specification.md REQ-01: **Flow meters** (2): rail unloading and marine loading; comprehensive records (calibration, FAT if applicable, installation verification, SAT if applicable, initial proving, periodic proving per frequency); **Temperature transmitters**: calibration certificates (may not require proving; transmitter accuracy verified through calibration); **Pressure transmitters** (if applicable): calibration certificates; **Density transmitters** (if separate from Coriolis integral density): calibration certificates; equipment list from DEL-12.04 data sheets |
| Acceptance Criteria | Each verification record must state acceptance criteria and demonstrate compliance per Specification.md REQ-05, REQ-09: acceptance criteria from DEL-12.02 specification (accuracy class, repeatability) and DEL-12.03 calculations (meter factor range, drift limits, proving repeatability); test results must be compared to criteria with pass/fail determination; acceptance statement signed by authorized personnel; if test fails, NCR required documenting corrective action |
| Witnessing Requirements | Confirm witnessing requirements from ER Vol 2 Part 1 and applicable standards per Specification.md REQ-16: ER may specify hold points requiring client witness (FAT, installation inspection, proving); Measurement Canada may require witnessed verification for custody transfer approval; third-party inspection may be required for high-value or critical installations; witness signatures demonstrate independent verification; coordinate witnessing schedule with client and inspector availability; witnessing adds cost and schedule coordination |

### Calibration Certificate Considerations

Calibration certificates must contain specific information for custody transfer traceability per Specification.md REQ-06, REQ-07:

| Field | Guidance |
|-------|----------|
| Equipment Identification | **Tag number**: Equipment tag number per project tag numbering system (must match DEL-12.04 data sheets and DEL-12.01 drawings); **Serial number**: Manufacturer serial number from equipment nameplate (must match DEL-12.04 data sheets and vendor documentation); **Manufacturer and model**: Must match DEL-12.04 data sheets; enables verification that correct equipment was tested; **Service description**: Rail unloading or marine loading custody transfer metering; provides context for calibration |
| Calibration Date | Date calibration was performed; calibration date establishes calibration interval (next calibration due = calibration date + calibration interval per DEL-12.02 or Measurement Canada); for factory calibration, date is typically before shipment; for field calibration, date is during commissioning or periodic verification |
| Calibration Standard / Traceability | **Reference standard identification**: Reference standard (prover, master meter, or other) used for calibration with serial number and calibration certificate number; **Traceability statement**: Statement of traceability to national metrology institute (e.g., "Traceable to Measurement Canada Certificate [Number]" or "Traceable to NIST Certificate [Number]"); **Calibration laboratory accreditation**: Laboratory accreditation (ISO/IEC 17025 accredited laboratory preferred or required for custody transfer; accreditation number and scope); **Unbroken traceability chain**: Equipment → Reference Standard → National Standard; each link in chain documented with certificate numbers |
| Calibration Range | **Range calibrated**: Flow range (for flow meters), temperature range (for temperature transmitters), pressure range (for pressure transmitters) over which equipment was calibrated; **Comparison to operating range**: Verify calibration range encompasses operating range from DEL-12.04 data sheets (e.g., if meter operates 50-500 m³/h, calibration should cover at least 50-500 m³/h, preferably wider) |
| As-Found and As-Left Values | **As-found**: Equipment accuracy before calibration adjustment (if equipment drifted since previous calibration, as-found shows drift; important for custody transfer confidence); **As-left**: Equipment accuracy after calibration adjustment (should meet specified accuracy class; e.g., ±0.15%); **Adjustments made**: Document any calibration adjustments or corrections applied; **Out-of-tolerance**: If as-found is out of tolerance, document and investigate (may indicate equipment problem or excessive drift) |
| Calibration Uncertainty | **Calibration uncertainty statement**: Document measurement uncertainty of calibration (calibration uncertainty should be ≤1/3 of specified measurement uncertainty per ISO/IEC 17025; e.g., if meter accuracy is ±0.15%, calibration uncertainty should be ≤±0.05%); **Expanded uncertainty**: Uncertainty with coverage factor (typically k=2 for 95% confidence); **Contributors**: Major uncertainty contributors (reference standard, calibration method, environmental conditions, operator technique) |
| Calibrator Identification | **Calibrating organization**: Company or laboratory that performed calibration (vendor factory, independent calibration lab, contractor calibration team, or Measurement Canada-approved service provider); **Technician**: Name and certification of technician who performed calibration (certification may be required: Measurement Canada authorized person, manufacturer-trained technician, certified calibration technician); **Certifications**: Technician certifications or qualifications |
| Next Calibration Due | **Calibration interval**: Recommended or required recalibration interval (e.g., 12 months, 24 months, per Measurement Canada regulations, per DEL-12.02 specification); **Next calibration date**: Calibration date + interval; enables maintenance scheduling; for custody transfer, calibration interval may be regulatory requirement (Measurement Canada) or commercial requirement |

### Accuracy Verification / Proving Record Considerations

Proving records document meter accuracy verification per Specification.md REQ-05, REQ-08:

| Field | Guidance |
|-------|----------|
| Proving Method | **Method identification**: In-line prover (sphere or piston), portable prover (volumetric or gravimetric), master meter, or other method per DEL-12.02 specification; **Prover identification**: Prover serial number, calibration certificate number (prover must be calibrated and traceable to national standards); **Prover uncertainty**: Document prover uncertainty (typical in-line prover ±0.02% to ±0.05%, portable prover ±0.05% to ±0.1%; from prover calibration certificate) |
| Proving Date and Personnel | **Proving date**: Date proving was performed; **Personnel**: Technician who performed proving (name, certification if required); **Witness**: Client or third-party witness signature if witnessing required per ER or Measurement Canada (witness name, organization, signature, date) |
| Proving Conditions | **Flow rate**: Flow rate during proving (m³/h or kg/h; should be within meter's accurate range; may perform proving at multiple flow rates to verify accuracy across range); **Temperature**: Product temperature during proving (affects density and viscosity; temperature measurement uncertainty contributes to proving uncertainty); **Pressure**: Product pressure during proving; **Product**: Verify product is CSD canola oil (same product as will be measured in operation; proving with substitute fluid may not be valid for custody transfer) |
| Proving Runs | **Number of runs**: Typically 3-5 proving runs for repeatability verification per API MPMS Chapter 4; **Individual run data**: For each proving run, document: prover volume or indicated volume, meter indicated volume, calculated meter factor for run, temperature and pressure during run; **Run repeatability**: Verify individual runs agree within acceptable repeatability (e.g., ±0.02% for in-line prover, ±0.05% for portable prover; from DEL-12.03 or API MPMS Chapter 4); if repeatability not achieved, proving is invalid and must be repeated |
| Meter Factor | **Meter factor definition**: MF = true volume (from prover) / indicated volume (from meter); ideal MF = 1.000; actual MF accounts for meter calibration offset; **Average meter factor**: Average of accepted proving runs; **Meter factor range**: Compare to acceptable range from DEL-12.03 (e.g., 0.995-1.005); **Meter factor drift** (for periodic proving): Compare to baseline meter factor (from initial proving) or previous proving; verify drift is within acceptable limit (e.g., <±0.05% from DEL-12.03); excessive drift indicates meter degradation |
| Acceptance Criteria and Verification | **Acceptance criteria statement**: Clearly state acceptance criteria from DEL-12.03 calculations: proving repeatability limit (e.g., "Repeatability shall be ±0.02% or better"), meter factor range (e.g., "Meter factor shall be 0.995 to 1.005"), meter factor drift limit (e.g., "Meter factor drift from baseline shall be <±0.05%"); **Results comparison**: Compare actual proving results to acceptance criteria; **Pass/fail determination**: Clear statement "PASS — Meter meets acceptance criteria" or "FAIL — Meter does not meet criteria; see NCR [Number]"; **Signature**: Authorized signature confirming acceptance (process engineer, QA/QC lead, client representative) |
| Witness Signature | **Witness requirement**: If ER or Measurement Canada requires witnessed proving, obtain witness signature; **Witness identification**: Witness name, organization (client representative, third-party inspector, Measurement Canada representative), date; **Witness statement**: Witness confirms proving was performed per procedure and results are valid |

### Service-Specific Considerations

Rail unloading and marine loading metering have different service characteristics affecting records:

| Service | Record Considerations |
|---------|----------------------|
| Rail Unloading Metering | **Batch operation**: Railcar unloading is batch custody transfer; each railcar is separate transaction; consider whether batch proving records are required (prove meter before each batch, after each batch, or periodic proving independent of batches; TBD from ER or DEL-12.02); **Multiple meters**: If 32 unloading stations have individual meters (vs. single meter for manifold), 32 sets of records required (calibration, proving for each meter); record package may be voluminous; **Proving coordination**: Proving must be coordinated with rail unloading operations; portable prover may be more suitable for multiple meters (one prover can prove all meters sequentially); **Lower criticality** (possibly): Rail unloading may have less stringent proving requirements than marine loading if rail unloading is not final custody transfer point (product is re-measured at marine loading for export) |
| Marine Loading Metering | **High-value export transactions**: Marine loading is final custody transfer point for export; measurement accuracy is critical for commercial settlement with international buyers; higher accuracy and more frequent proving may be justified; **In-line prover** (possibly): In-line prover may be specified for marine loading for higher accuracy and online proving capability (proving during loading operations without disruption); in-line prover records more comprehensive (prover calibration, sphere or piston inspection, proving procedure); **Continuous operation**: Vessel loading is continuous operation; proving may be performed before loading, during loading (if in-line prover), or after loading; proving must not delay vessel departure; **Regulatory approval** (possibly): Marine loading export metering may require specific Measurement Canada approval or equivalent; approval certificate may be required record |

## Trade-offs

### Competing Factors

| Trade-off | Options | Guidance |
|-----------|---------|----------|
| Proving Depth vs. Schedule | Comprehensive proving (multiple flow rates, multiple runs, detailed documentation) takes time and may delay commissioning; limited proving (single flow rate, minimum runs) is faster but may not fully verify accuracy across range | Comply with ER and DEL-12.02 specification requirements; do not shortcut proving to save schedule; proving is essential for custody transfer confidence; if schedule is critical, coordinate proving timing with commissioning schedule (prove critical equipment first, less critical equipment later); escalate to project management if schedule conflicts with proving requirements |
| Vendor Certificates vs. Project Templates | Vendor-provided calibration certificates may not include all project-required fields or may use different format than project templates; using vendor certificates as-is saves effort but may not satisfy project requirements; reformatting vendor certificates to project templates adds effort but ensures consistency | Supplement vendor certificates with project cover sheets or transmittal forms mapping vendor certificate content to project requirements per Specification.md REQ-07; accept vendor certificate format if content is complete (all required fields present); use project template to cross-reference vendor certificate to requirements; do not reformat unnecessarily |
| Third-Party Witnessing vs. Cost and Schedule | Third-party witnessing (independent inspector, client representative, Measurement Canada representative) adds cost (inspector fees, travel, coordination) and schedule (witness availability may delay activities); contractor self-verification reduces cost and schedule but may not satisfy regulatory or commercial confidence requirements | Confirm witnessing requirements from ER Vol 2 Part 1 (hold points, witness points) and Measurement Canada if applicable; implement witnessing where required per Specification.md REQ-16; do not eliminate required witnessing to save cost; coordinate witness schedule early to avoid delays; self-verification acceptable where witnessing is not required |
| Comprehensive Records vs. Minimum Records | Comprehensive record package (FAT, installation verification, SAT, proving, MTRs, NCRs, all supporting documentation) provides complete quality evidence but is voluminous and costly to compile; minimum record package (calibration certificates and proving records per Decomposition:360) is simpler but may not satisfy all stakeholders | Include minimum records per Decomposition:360 and Specification.md REQ-01; add additional records as required by ER Vol 2 Part 1 (QA requirements), ER Vol 2 Part 2 (testing requirements), DEL-12.02 specification (FAT, SAT, MTRs), or project Quality Management Plan; balance completeness vs. effort; comprehensive records provide better protection for warranty claims and future disputes |

### Timing Considerations

Record collection and compilation progresses through project phases per Guidance.md in Pass 1 (expanded here):

| Stage | Record Status | Records Available | Actions |
|-------|---------------|-------------------|---------|
| **Factory Acceptance Test (FAT)** | Vendor calibration certificates, FAT records | **Calibration certificates**: Factory calibration certificates from meter and transmitter manufacturers (certificates may be dated weeks or months before FAT; verify calibration is current); **FAT protocols and results**: FAT test procedures, test data (flow tests at multiple flow rates, accuracy verification, functional tests, signal tests), FAT acceptance (pass/fail with signature), FAT witness report (if FAT was witnessed), FAT NCRs (if issues identified) | Collect vendor calibration certificates during FAT or before shipment; witness FAT if required; review FAT results for compliance with DEL-12.02 acceptance criteria; resolve FAT NCRs before shipment; file FAT records in record package |
| **Shipment and Receiving** | Vendor packing lists, receiving inspection | **Packing lists**: Verify equipment tag numbers and serial numbers match purchase order and DEL-12.04 data sheets; **Receiving inspection**: Visual inspection for shipping damage; verify equipment condition upon receipt | Perform receiving inspection; document equipment condition; resolve any shipping damage before installation; file receiving inspection records |
| **Site Installation** | Installation verification records, as-built documentation | **Installation checklists**: Verify installation per DEL-12.01 drawings (orientation, elevations, straight-runs, connections); **Dimensional verification**: Measure actual straight-run lengths (upstream and downstream) and compare to drawing requirements; **Piping connection verification**: Verify flange torques per specification, gasket installation, alignment; **Electrical connection verification**: Verify power supply connections, signal wiring, grounding, cable routing; **As-built verification**: Document any deviations from drawings (if field changes required, update drawings or document as NCR) | Perform installation inspections per project ITP; witness hold points if required; document installation verification; resolve installation NCRs; verify installation quality before proceeding to commissioning |
| **Pre-Commissioning / Loop Checks** | Field calibration verification, loop checks | **Field calibration verification**: If field calibration is performed (not common for custody transfer meters which are factory-calibrated), document field calibration results; **Loop checks**: Verify signals from transmitters to control system (temperature, pressure signals; verify 4-20 mA signals, HART communication, Modbus communication); verify totalizer pulse outputs; **Functional tests**: Verify meter displays (if local display), verify control system receives and displays signals | Perform loop checks per commissioning plan; verify all signals functional before commissioning; document loop check results; resolve signal issues |
| **Commissioning / Initial Proving** | Site acceptance test (SAT) records, initial proving records | **SAT protocols and results** (if SAT specified in DEL-12.02): Functional testing of installed metering system; proving upon installation to verify accuracy; SAT acceptance; **Initial proving**: Prove both flow meters (rail and marine) upon commissioning per DEL-12.02 proving method; establish baseline meter factors; verify accuracy meets acceptance criteria from DEL-12.03; witness proving if required per ER or Measurement Canada; proving results critical for custody transfer acceptance | Perform SAT per DEL-12.02; perform initial proving using method per DEL-12.02 (in-line prover, portable prover, master meter); coordinate witness for proving if required; document proving results per Specification.md REQ-08; verify acceptance per DEL-12.03 criteria; obtain signatures and witness; resolve proving NCRs if results do not meet acceptance; initial proving establishes baseline for future proving comparisons |
| **Handover / Closeout** | Complete record package compilation and issue | **All records collected**: Verify all required records are collected from factory through commissioning; **Completeness verification**: Verify record index shows all records complete; **Traceability verification**: Verify all equipment has required records (calibration, proving); **NCR closure**: Verify all NCRs are closed with verified corrective actions and client acceptance; **Approvals**: Obtain QA/QC lead approval, project manager approval, client acceptance if required | Compile complete record package per Specification.md Documentation section structure; perform final completeness review per Procedure.md Step 5; obtain all required signatures and approvals; issue record package per project document control; archive in approved format and location per ER Vol 2 Part 1; handover to client with record package as evidence of completion and compliance |

## Examples

### Record Content Reference

The anticipated artifacts provide guidance on expected content (Source: Decomposition:360):

| Artifact | Expected Content |
|----------|------------------|
| Calibration Certificates | **Flow meter calibration certificate example**: Equipment tag FT-1201, serial number [SN], manufacturer [Vendor], model [Model]; Calibration date [Date]; Calibration standard: Master meter [SN] with Measurement Canada certificate [Cert #]; Traceability: "Traceable to Measurement Canada"; Calibration range: 50-500 m³/h; As-found accuracy: ±0.14%; As-left accuracy: ±0.12%; Calibration uncertainty: ±0.04% (k=2); Calibrator: [Lab name], ISO/IEC 17025 accredited, technician [Name]; Next calibration: [Date + 12 months] |
| Accuracy Verification / Proving Records | **Proving record example**: Equipment tag FT-1201 Rail Unloading Flow Meter; Proving date [Date]; Proving method: Portable prover [SN] calibrated [Date] traceable to Measurement Canada; Proving conditions: Flow rate 300 m³/h, temperature 25°C, pressure 5 bar; Proving runs: Run 1 MF=0.9985, Run 2 MF=0.9988, Run 3 MF=0.9986, Run 4 MF=0.9987, Run 5 MF=0.9989; Average MF=0.9987; Repeatability=±0.02%; Acceptance criteria: MF 0.995-1.005, repeatability ±0.05%, drift <±0.05% (from DEL-12.03); Result: PASS — MF within range, repeatability acceptable; Signature: [Process Engineer]; Witness: [Client Rep] |

### Record Index Example

Record index per Specification.md REQ-04 (ASSUMPTION):

| Tag Number | Serial Number | Service | Equipment | Record Type | Record Date | Record Ref | Witness | Status |
|------------|---------------|---------|-----------|-------------|-------------|------------|---------|--------|
| FT-1201 | SN-12345 | Rail Unloading | Coriolis Flow Meter | Cal Cert (Factory) | 2026-01-15 | Section 1.1 | N/A | Complete |
| FT-1201 | SN-12345 | Rail Unloading | Coriolis Flow Meter | FAT Record | 2026-01-20 | Section 2.1 | Client | Complete |
| FT-1201 | SN-12345 | Rail Unloading | Coriolis Flow Meter | Installation Verification | 2026-03-10 | Section 3.1 | N/A | Complete |
| FT-1201 | SN-12345 | Rail Unloading | Coriolis Flow Meter | SAT Record | 2026-04-05 | Section 4.1 | N/A | Complete |
| FT-1201 | SN-12345 | Rail Unloading | Coriolis Flow Meter | Initial Proving | 2026-04-12 | Section 5.1 | Client | Complete |
| FT-1202 | SN-12346 | Marine Loading | Coriolis Flow Meter | Cal Cert (Factory) | 2026-01-18 | Section 1.1 | N/A | Complete |
| FT-1202 | SN-12346 | Marine Loading | Coriolis Flow Meter | Initial Proving | 2026-04-15 | Section 5.1 | Meas. Canada | Complete |
| TT-1201 | SN-78901 | Rail Unloading | Temperature Transmitter | Cal Cert (Factory) | 2026-02-01 | Section 1.2 | N/A | Complete |
| TT-1202 | SN-78902 | Marine Loading | Temperature Transmitter | Cal Cert (Factory) | 2026-02-01 | Section 1.2 | N/A | Complete |
| PT-1201 | SN-45678 | Rail Unloading | Pressure Transmitter | Cal Cert (Factory) | 2026-02-05 | Section 1.3 | N/A | Complete |

**Note:** Actual tag numbers, serial numbers, dates, and witness requirements TBD from DEL-12.04 data sheets, equipment delivery, testing schedule, and ER requirements.

## Conflict Table

### Local Conflicts (for Human Ruling)

No conflicts identified from accessible sources at this stage.

| Conflict ID | Conflict | Source A (File § Section) | Source B (File § Section) | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|---------------------------|---------------------------|-------------------|-------------------|--------------|
| — | — | — | — | — | — | TBD |

### Conflict Recording Instructions

When conflicts are discovered during record compilation, record them in this table with:
- **Conflict ID:** Sequential identifier (e.g., DEL-12.05-C01)
- **Conflict:** Clear statement of the conflicting requirements or test results
- **Source A/B:** File path and section reference for each conflicting source (e.g., "DEL-12.03 § Acceptance Criteria (meter factor 0.995-1.005)" or "Proving Record [Date] (meter factor 0.9945)")
- **Impacted Sections:** Which sections of DEL-12.05 documents or record package are affected
- **Proposed Authority:** Which source should govern or proposed resolution (PROPOSAL label)
- **Human Ruling:** Resolution decision and date (TBD until ruled)

### Potential Conflicts to Monitor

| Potential Conflict | Trigger Condition | Sources to Compare | Impacted Documents |
|--------------------|-------------------|--------------------|--------------------|
| Specification acceptance vs. actual proving results | DEL-12.02 or DEL-12.03 specifies meter factor 0.995-1.005 but actual proving shows meter factor outside range | DEL-12.03 acceptance criteria vs. actual proving record results | Specification.md REQ-05; Procedure.md Step 4.3 |
| ER witnessing vs. vendor practice | ER requires client witness for FAT but vendor standard practice is factory testing without witness | ER Vol 2 Part 1 hold point requirements vs. vendor standard practice | Specification.md REQ-16; Procedure.md Step 1.7 |
| Calibration traceability vs. vendor capability | ER or Measurement Canada requires traceability to Measurement Canada but vendor calibration is traceable to NIST | ER/Measurement Canada traceability requirement vs. vendor calibration certificate | Specification.md REQ-06; Procedure.md Step 3.3 |
| Proving frequency vs. commissioning schedule | DEL-12.02 requires quarterly proving and first periodic proving would be due during commissioning | DEL-12.02 proving frequency vs. commissioning schedule | Specification.md REQ-05; Procedure.md Step 4.1 |
| Record format vs. vendor certificate format | Project requires specific record format but vendor certificates use different format | ER Vol 2 Part 1 document control vs. vendor certificate format | Specification.md REQ-17; Procedure.md Step 3.2 |

## Cross-Document Traceability

| Document | Section | Traceability Points |
|----------|---------|---------------------|
| Datasheet.md | § Identification | DEL-12.05 identity referenced in Guidance § Purpose deliverable definition |
| Datasheet.md | § Conditions | Design context (service application, record scope, equipment covered) driving Guidance § Considerations; record requirements context (TBD items) informing Guidance § Calibration/Proving Considerations |
| Datasheet.md | § Construction | Anticipated record content informing Guidance § Examples; record package structure per Guidance § Purpose (audit trail organization); equipment-to-record traceability per Guidance § Principles (traceability) |
| Specification.md | § Scope | Inclusions that Guidance § Purpose downstream use addresses |
| Specification.md | § Requirements | REQ-01 through REQ-19 that Guidance § Principles rationale supports; REQ-05/06 objective alignment per Guidance § Objective Alignment |
| Specification.md | § Standards | Custody transfer standards that Guidance § Principles (calibration traceability, proving documentation) addresses |
| Specification.md | § Verification | Verification methods that Guidance § Principles (auditability) supports |
| Procedure.md | § Prerequisites | Inputs that Guidance § Timing Considerations identifies (DEL-12.02, DEL-12.03, DEL-12.04, vendor certificates, proving results) |
| Procedure.md | § Step 1 | Record set definition that Guidance § Considerations (minimum content, equipment coverage) informs |
| Procedure.md | § Step 3 | Calibration certificate collection per Guidance § Calibration Certificate Considerations (field guidance) |
| Procedure.md | § Step 4 | Proving record collection per Guidance § Proving Record Considerations (field guidance) |
| Procedure.md | § Step 5 | Verification that Guidance § Principles (evidence, traceability, auditability) supports |
| DEL-12.01 | Drawings | Installation verification records demonstrate installation per drawings per Guidance § Purpose (correct installation) |
| DEL-12.02 | Specification | Acceptance criteria per Guidance § Purpose (properly specified); records demonstrate specification compliance |
| DEL-12.03 | Calculations | Proving criteria per Guidance § Proving Record Considerations (acceptance criteria from calculations); records use calculation-derived criteria |
| DEL-12.04 | Data Sheets | Equipment tags, serial numbers per Guidance § Principles (traceability); records reference data sheet parameters
