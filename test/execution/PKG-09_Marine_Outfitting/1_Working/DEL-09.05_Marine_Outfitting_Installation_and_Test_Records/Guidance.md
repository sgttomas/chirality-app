# Guidance: DEL-09.05 Marine Outfitting Installation & Test Records

## Purpose

This guidance document supports the development of **Marine Outfitting Installation & Test Records** for **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Provides evidence of completion, inspection, and testing for marine outfitting. (**Source:** Decomposition, DEL-09.05 row)

This deliverable is classified as a **Record** under the **Marine** discipline, to be produced by **D&B Contractor (QA/QC)**.

**Downstream use:** Records provide evidence of completion, inspection, and testing for marine outfitting. They close the loop from design to construction completion, providing basis for:
- Construction completion sign-off and acceptance
- Handover documentation to Employer
- Future maintenance reference (as-installed conditions)
- Regulatory/authority compliance evidence
- Warranty claims (if applicable)

## Principles

### Records Intent

**Purpose:**
- Records are **evidence artifacts** for acceptance: they demonstrate what was installed, inspected, and tested, and who witnessed/accepted it.
- Records close the loop from design (DEL-09.01 drawings, DEL-09.02 specification, DEL-09.03 calculations, DEL-09.04 data sheets) to as-installed verification.
- Records provide the basis for:
  - **Construction completion sign-off:** Demonstrate work is complete per contract requirements
  - **Handover documentation:** Provide evidence to Employer for facility acceptance
  - **Future maintenance reference:** Document as-installed conditions, equipment specifications, test results for operations/maintenance planning
  - **Regulatory/authority compliance evidence:** Demonstrate compliance with codes, standards, permit conditions (e.g., proof load testing if required by port authority)
  - **Warranty claims (if applicable):** Provide installation evidence if equipment warranty claims arise

**Key Principles:**
- **Attributable, dated, located, legible:** Every record must clearly identify who, when, where, and what.
- **Evidence-based:** Support claims with attached evidence (photos, certificates, test data).
- **Traceability:** Equipment tags must match across DEL-09.01 drawings, DEL-09.04 data sheets, and DEL-09.05 records.
- **Transparency:** Capture deviations and nonconformances; do not hide issues; document dispositions clearly.

**Cross-reference:** Content requirements are defined in `Specification.md § 2`.

### Evidence Rules

**Source Fidelity:**
- Do not invent witness/hold point requirements or acceptance criteria — mark **TBD** until sourced from Employer's Requirements and project QA/QC procedures (Inspection and Test Plan / ITP).
- Each record must be attributable (who performed, inspected, witnessed — names, titles, signatures), dated (when inspection/test occurred — date and time), and located (which equipment tag/location).
- Support claims with attached evidence (photos showing installation stages, material certificates, test data, calibration certificates).

**Record Quality:**
- Records shall be:
  - **Clear:** Entries unambiguous; measurements with units; pass/fail clearly indicated
  - **Complete:** All checklist items addressed; no blank fields without explanation; signatures and dates present
  - **Legible:** Handwritten entries readable; signatures identifiable; scanned copies clear (if paper forms scanned)
  - **Permanent:** Use permanent ink or electronic forms; avoid pencil, erasable media, or easily altered formats

### Installation Records (supports SPEC § 2.1)

**Purpose:** Verify that marine outfitting equipment was installed correctly per DEL-09.01 drawings and DEL-09.02 specification.

**Key Record Elements:**
- **Equipment identification:** Tag, serial number (if applicable), drawing reference, location (uniquely identifies equipment item).
- **Pre-installation checks:** Receiving inspection (verify equipment matches DEL-09.04 data sheet — manufacturer, model, materials), material verification (certificate review), surface preparation (cleaning, coating touch-up if needed).
- **Installation verification:** Position/alignment (survey or measurement), fixing method (bolting, welding, grouting), torque values (where specified), interface verification (connections to marine structure per DEL-09.01 details).
- **Post-installation inspection:** Visual inspection (no damage, proper orientation, coating integrity), dimensional check (verify position within tolerances), functional check (if applicable).
- **Sign-off:** Installer (confirms installation per procedure), inspector (confirms inspection acceptance), witness (if ITP hold/witness point — may be Employer's rep, third-party, authority rep).

**Equipment-Specific Considerations (per `Specification.md § 2.1`):**

| Equipment | Key Installation Checks | Typical Hold/Witness Points |
|-----------|-------------------------|-----------------------------|
| **Fenders** | Position relative to structure (coordinates, elevation), chain installation and tensioning (if applicable), frontal frame alignment, anchor bolt torque, interface to marine structure (connection quality, load transfer) | Foundation/anchor installation (hold); final installation (witness) |
| **Bollards** | Foundation preparation (substrate condition, reinforcement if applicable), setting-out accuracy (survey verification), grouting (batch tickets, placement, strength tests), base plate alignment (level, plumb), anchor bolt torque or through-bolt installation | Foundation preparation (hold); grouting (witness); final installation (witness) |
| **Ladders** | Fixing security (bolt torques, weld inspection if welded), safety cage installation (clearances, landing platform), rest platforms (spacing, dimensions, attachment), rung spacing and toe clearance (code compliance), anti-slip features | Welding (hold if welded attachments); final installation (witness) |
| **Life-saving equipment** | Mounting security (fixing adequacy), equipment functionality (deployment test), accessibility (no obstructions), visibility (per regulations), signage/marking | Final installation (witness or inspection) |
| **Berth 10 repairs** | Repair completion vs scope, materials used, workmanship quality, tie-in to existing elements, finish condition | Repair completion (inspection); final acceptance (witness) |

**ASSUMPTION:** Hold/witness point requirements per project ITP and Employer's Requirements; typical hold points for critical activities (foundations, structural connections, grouting); typical witness points for final installations.

### Proof Load Testing (supports SPEC § 2.2)

**Purpose:** Verify that installed bollards (and other items if specified) can safely resist design loads.

**When Required:**
- Proof load testing for bollards may be required by:
  - Employer's Requirements (**TBD** — ER clauses to be extracted)
  - Technical specification (DEL-09.02 § 2.2)
  - Port authority or regulatory requirements (local port authority, Transport Canada, provincial regulations)
  - Project QA/QC procedures or ITP
- **If not explicitly required:** Document in records matrix that proof load testing not required; provide justification (e.g., "Not required per ER Vol 2 Part 1 § X.X").

**Test Procedure Elements (typical for bollard proof load testing):**

**Test Setup:**
- **Load application method:** Hydraulic jack with calibrated load cell (most common for bollards), calibrated weights, or pulling equipment (winch, vehicle).
- **Test rig:** Reaction point (adjacent structure, ground anchor, reaction frame), load transfer mechanism (cable, chain, test beam), geometry (load angle, eccentricity).
- **Test equipment:** Jack model/serial, load cell serial, gauge serial, measurement equipment (deflection gauges, surveying equipment if deflection measured).
- **Calibration:** Verify current calibration certificates for all test equipment; typical calibration interval 6-12 months.

**Test Execution:**
- **Applied load value:** Per DEL-09.02 or code requirements (**TBD**); typical proof load = 1.25× to 1.5× SWL.
  - Example: Bollard SWL = 100 tonnes → Proof load = 150 tonnes (1.5× SWL)
- **Loading procedure:** Gradual loading in increments (e.g., 25%, 50%, 75%, 100% of proof load); hold at proof load for specified duration (typically 5-10 minutes); gradual unloading.
- **Load vs time recording:** Optional but recommended — record load history during test (may use load cell data logger or manual recording at intervals).
- **Deflection/movement measurement:** If required by procedure, measure bollard deflection or movement (typically using surveying equipment, deflection gauges, or dial indicators); record values.

**Observations and Acceptance:**
- **Visual inspection during test:** Inspect bollard, base plate, anchor bolts, foundation for visible deformation, cracking, bolt slippage, foundation movement during loading and at proof load.
- **Acceptance criteria:** No visible deformation, cracking, or movement exceeding limits (limits **TBD** per DEL-09.02 or codes); bollard returns to original position after unloading (residual deflection within acceptable limits).
- **Pass/fail determination:** Compare observations to acceptance criteria; document pass/fail with justification.
- **If failure occurs:** Document failure mode (bolt failure, foundation failure, bollard deformation, etc.); issue NCR; investigate root cause; disposition (repair and retest, replace, design review).

**Witness Requirements:**
- **Witness signatures:** Tester, inspector, witness (if ITP requires witness) — may be Employer's representative, third-party inspector (if engaged), or port authority representative (if required).
- **Witness notification:** Provide advance notice per ITP requirements (typically 48-72 hours); confirm witness availability before proceeding.

**Test Documentation:**
- **Test certificate:** Formal certificate signed by tester and witness documenting test setup, applied load, observations, pass/fail determination, acceptance statement.
- **Photographic records:** Test setup, load application (bollard under load), post-test condition; photos should show load measurement equipment, test rig arrangement, bollard condition.

**ASSUMPTION:** Proof load testing methodology follows BS 6349, PIANC, or local port authority requirements unless ER specifies alternative method.

### NCR Management

**Purpose:** Nonconformances identified during installation or testing shall be documented, investigated, dispositioned, and closed.

**NCR Process:**
1. **Identification:** Installer or inspector identifies nonconformance (deviation from drawings, specification, data sheet, or acceptance criteria).
2. **Documentation:** Complete NCR form (NCR number, equipment tag, date, description of nonconformance, impact assessment).
3. **Investigation:** Determine root cause (workmanship error, material defect, design issue, vendor issue, etc.).
4. **Disposition:** QA/QC manager or authorized representative determines disposition:
   - **Use-as-is:** Accept nonconformance without correction (requires justification; typically for minor deviations with no impact)
   - **Repair:** Correct nonconformance (rework, touch-up, adjustment)
   - **Replace:** Remove and replace nonconforming item
   - **Scrap:** Remove and discard (for items that cannot be repaired)
5. **Corrective action:** If repair or replace, perform corrective action per disposition; document corrective action taken.
6. **Closure verification:** Re-inspect after corrective action; verify nonconformance resolved; obtain QA/QC sign-off.
7. **Closure:** Close NCR with sign-off; attach closure evidence (re-inspection record, photos, test results).

**NCR Status Tracking:**
- NCR register tracks all NCRs (open, closed, pending).
- NCR status summary included in records package (list open NCRs with status and planned closure; confirm all critical NCRs closed before handover).

## Considerations

### Factors to Consider During Development

| Factor | Consideration | Reference |
|--------|---------------|-----------|
| **Tag consistency** | Record tags must match DEL-09.01 drawings and DEL-09.04 data sheets; establish tagging convention early; verify tags during installation | `Specification.md § 3` |
| **ITP alignment** | Records must satisfy ITP hold and witness point requirements; coordinate with QA/QC to ensure inspector/witness available at hold points | `Specification.md § 4` |
| **As-installed vs. as-designed** | Verify installed equipment matches DEL-09.04 data sheets (manufacturer, model, capacity, materials); document deviations in NCRs; obtain disposition for deviations | `Specification.md § 3` |
| **Timing** | Records are generated during construction (real-time); ensure QA/QC personnel present for hold points; plan inspector/witness availability to avoid construction delays | `Procedure.md` |
| **Evidence quality** | Photos should be clear, dated, annotated; show relevant details (fixings, alignments, interfaces); sufficient resolution for verification; organized by equipment tag | `Specification.md § 1.3` |
| **NCR management** | Identify nonconformances early; disposition promptly; close NCRs before handover (open NCRs may delay acceptance) | `Specification.md § 4` |

### Relationship to Other Deliverables

| Deliverable | Relationship | Flow |
|-------------|--------------|------|
| DEL-09.01 Marine Outfitting Design Drawing Set | **Design baseline** — provides equipment tags and locations | DEL-09.01 establishes tags → DEL-09.05 uses tags in records; verify as-installed position matches drawing locations |
| DEL-09.02 Marine Outfitting Technical Specification | **Requirements baseline** — defines inspection/test requirements and acceptance criteria | DEL-09.02 specifies requirements → DEL-09.05 records verify compliance with requirements |
| DEL-09.03 Marine Outfitting Design Calculations | **Acceptance criteria source** — provides calculated values for test acceptance | DEL-09.03 calculates proof load values → DEL-09.05 test records verify compliance with calculated acceptance criteria |
| DEL-09.04 Marine Outfitting Data Sheet Package | **Equipment baseline** — provides as-designed specifications | DEL-09.04 defines equipment specs → DEL-09.05 records verify as-installed equipment matches data sheets |

## Trade-offs

### Competing Concerns to Evaluate

| Trade-off | Factors | Resolution Approach |
|-----------|---------|---------------------|
| **Record completeness vs. schedule** | Comprehensive records (detailed checklists, extensive photos, complete documentation) take time and resources; construction schedule pressure may push for shortcuts or minimal records; incomplete records risk rejection during handover | **Recommendation:** Define minimum required records in ITP before construction; prioritize hold points (foundation prep, grouting, final installation) with mandatory sign-off; focus documentation on critical verification points; balance completeness with construction efficiency |
| **Standardized forms vs. flexibility** | Standard forms ensure consistency and completeness but may not fit all situations (unusual equipment, special conditions, field changes); custom forms provide flexibility but risk inconsistency | **Recommendation:** Use standard forms with notes/attachments section for exceptions; allow supplemental records for special conditions; maintain core record structure (identification, checks, sign-off) consistent across all forms |
| **Photo documentation level** | More photos provide better evidence and support verification but increase file sizes, storage requirements, and photo processing effort; insufficient photos may not adequately document installation | **Recommendation:** Focus on key stages (before installation, during critical steps, after completion); capture critical details (fixings, alignments, interfaces, hold point activities); use annotations to clarify photo content; balance documentation with practical constraints |
| **Witness presence** | Having Employer's representative or authority witness for all checks is resource-intensive (witness availability, coordination, potential schedule delays); minimal witness presence may not provide adequate oversight | **Recommendation:** Focus witness attendance on ITP hold points (critical activities requiring mandatory witness); inspector covers remaining witness points with notification protocol; coordinate witness schedule in advance to minimize delays |

## Examples

### Reference Checklists

- Use `Datasheet.md` (Content Checklist) as the minimum checklist for this deliverable.
- Use the decomposition's anticipated artifacts as the baseline:
  - Installation records
  - Proof load test records
- Expand as needed based on equipment inventory from DEL-09.01 and inspection/test requirements from DEL-09.02.

### Typical Records Matrix Structure

Master index tracking all required records by equipment tag:

| Tag | Description | Location | Drawing Ref | Data Sheet Ref | Installation Record | Proof Load Test | Status | Notes |
|-----|-------------|----------|-------------|----------------|---------------------|-----------------|--------|-------|
| FEN-001 | Cone fender 800H × 1600L | Berth 10A Sta. 0+25.0 | DWG-09.01-001 | DS-FEN-001 | IRF-001 | N/A | Complete | — |
| FEN-002 | Cone fender 800H × 1600L | Berth 10A Sta. 0+35.0 | DWG-09.01-001 | DS-FEN-001 | IRF-002 | N/A | Complete | — |
| BOL-001 | 100T double horn bollard | Berth 10A Sta. 0+15.0 | DWG-09.01-002 | DS-BOL-001 | IRB-001 | PLT-001 | Complete | Proof load passed 150T |
| BOL-002 | 100T double horn bollard | Berth 10A Sta. 0+45.0 | DWG-09.01-002 | DS-BOL-001 | IRB-002 | PLT-002 | Complete | Proof load passed 150T |
| LAD-001 | SS access ladder with cage | Berth 10A Platform | DWG-09.01-003 | N/A | IRL-001 | N/A | Complete | — |
| LSE-001 | Life ring station | Berth 10A Platform | DWG-09.01-003 | N/A | IRS-001 | N/A | Complete | — |

**Note:** Table above is illustrative example; actual records matrix will reflect complete equipment inventory from DEL-09.01.

### Typical Installation Record Form Content

**Installation Record Form Structure (per `Specification.md § 1.2`):**

1. **Header**
   - Project name, package, deliverable ID
   - Equipment tag
   - Revision, date
2. **Equipment Identification**
   - Tag, description (type, manufacturer, model)
   - Location (coordinate or descriptive location)
   - Drawing reference (DEL-09.01)
   - Data sheet reference (DEL-09.04)
3. **Receiving Inspection**
   - Material certificate verification (reviewed and accepted)
   - Visual inspection (no damage, corrosion, defects)
   - Dimensional verification (if applicable)
4. **Installation Checks** (checklist items per equipment type)
   - Item-by-item checklist with pass/fail/N/A for each check
   - Measured values where applicable (positions, alignments, torques, coating thickness)
   - Reference to specification requirements (DEL-09.02 §) or vendor installation instructions
5. **Post-Installation Inspection**
   - Visual inspection results (overall condition, coating integrity)
   - Dimensional check results (position within tolerances)
   - Functional check results (if applicable)
6. **Attachments**
   - Photographic records (before, during, after)
   - Material certificates (if not previously attached)
   - Coating inspection reports (if coating touch-up performed)
7. **NCR Reference** (if any)
   - NCR number, description, disposition, closure status
8. **Sign-off Block**
   - Installer: Name, title, signature, date
   - Inspector: Name, title, signature, date
   - Witness (if required): Name, organization, signature, date

### Typical Proof Load Test Record Form Content

**Proof Load Test Record Form Structure (per `Specification.md § 2.2`):**

1. **Header**
   - Project name, package, deliverable ID
   - Equipment tag (bollard being tested)
   - Test date, revision
2. **Equipment Identification**
   - Tag, description (manufacturer, model, SWL rating)
   - Location, drawing reference, data sheet reference
3. **Test Setup**
   - Load application method (hydraulic jack, weights, etc.)
   - Test equipment (jack model/serial, load cell serial, gauge serial)
   - Calibration certificates (attached; current calibration verified)
   - Test rig arrangement (sketch or photo; reaction point, geometry)
4. **Test Procedure**
   - Test load value (kN or tonnes) — per DEL-09.02 or code (typically 1.25× to 1.5× SWL)
   - Loading sequence (increments, hold times)
   - Acceptance criteria (no visible deformation, cracking, movement; residual deflection limits)
5. **Test Execution**
   - Applied load (value, duration, load curve if recorded)
   - Measured deflection or movement (if required) — method, values
   - Observations during test (visual inspection for deformation, cracking, bolt slippage, foundation movement, unusual sounds)
6. **Pass/Fail Determination**
   - Comparison to acceptance criteria
   - Pass/fail statement with justification
   - If failed: failure mode description, NCR reference
7. **Attachments**
   - Photographic records (test setup, bollard under load, post-test condition)
   - Load vs time curve (if recorded)
   - Deflection measurements (if applicable)
   - Calibration certificates
8. **Sign-off Block**
   - Tester: Name, title, signature, date
   - Inspector: Name, title, signature, date
   - Witness (if required): Name, organization, signature, date
9. **Test Certificate**
   - Formal certificate section with test results summary and acceptance statement
   - Signed by tester and witness

### Cross-Document Consistency

**Ensure consistency with other DEL-09.05 documents:**
- **Datasheet:** Content Checklist items match Specification requirements and Procedure steps.
- **Specification:** All requirements have corresponding rationale in this Guidance document and verification steps in Procedure.
- **Procedure:** All steps reference applicable Specification requirements and Guidance considerations.

**Ensure consistency with related PKG-09 deliverables:**
- **DEL-09.01:** Equipment tags match drawings; locations verified
- **DEL-09.02:** Inspection/test requirements implemented; acceptance criteria followed
- **DEL-09.03:** Test acceptance criteria (proof load values) from calculations
- **DEL-09.04:** As-installed equipment verified to match data sheet specifications
