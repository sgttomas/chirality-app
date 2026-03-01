# Specification — DEL-015-03 Receptacle Installation

---

## Scope

### Included

This deliverable covers the supply and installation of all electrical receptacles (outlets) in the New North Shop addition at the West Dried Meat Lake Regional Landfill Maintenance Shop, as defined by:

- SOW-0057: Installation of multiple high-voltage welding-grade electrical receptacles throughout the shop area (assumed 50A/240V per Decomposition D-009). [Source: Decomposition §3, Scope Ledger §8]
- SOW-0058: Installation of 15A/120V, 20A/120V, 20A/240V, 30A/240V, and 50A/240V receptacles per the electrical drawing layout. [Source: Decomposition §3; App B-Elec]

This deliverable includes:
- All receptacle devices and associated rough-in wiring from panelboard to device
- Circuit breaker assignments as required for receptacle circuits not covered by DEL-015-01 (see Scope Boundary Note below)
- Outlet boxes, conduit, wire, and terminations for all receptacle circuits
- GFCI protection where required by code
- AFCI protection where required by the applicable CEC edition (TBD — see REQ-015-03-07) [Ref: B-003]
- Cover plates and device trim

**Scope Boundary Note [Ref: F-001]:** The boundary between DEL-015-03 and DEL-015-01 for circuit breaker assignments requires clarification. DEL-015-01 covers main distribution and three-phase service. DEL-015-03 covers branch circuit breakers dedicated to receptacle circuits. Where a breaker serves both receptacle and non-receptacle loads, assignment shall be coordinated with the Project Manager and confirmed against DEL-015-01 Specification. This boundary is TBD pending IFC panel schedule (DEL-004-06) finalization.

### Excluded

- Three-phase power service and main distribution (DEL-015-01)
- Lighting circuits and fixtures (DEL-015-02)
- Equipment power circuits for cranes, overhead doors, compressor, fire hose pump, pressure washer, and low-voltage systems (DEL-015-04, DEL-015-05)
- Electrical design and IFC drawing production (PKG-004)
- Procurement of welding equipment (County-supplied per RFP §3.4)
- Receptacles or receptacle-style connectors serving fixed equipment assigned to DEL-015-04 (e.g., compressor, pressure washer connections) — see Scope Boundary Note for DEL-015-04 below [Ref: E-002]

**Scope Boundary Note — DEL-015-04 [Ref: E-002]:** Any receptacles that may serve dual purposes as equipment power connections (e.g., compressor, pressure washer using receptacle-style connectors) must be clearly assigned to either DEL-015-03 or DEL-015-04. The current decomposition places 40A compressor, 70A fire hose pump, and 70A pressure washer circuits under DEL-015-04. If any receptacle-style connections for these loads exist, scope assignment is TBD — to be confirmed by the Project Manager / decomposition authority. Source: Guidance — Sequencing with Other PKG-015 Deliverables; Decomposition §7 PKG-015 table.

---

## Requirements

### REQ-015-03-01: Welding-Grade Receptacles — Rating

Multiple welding-grade receptacles shall be installed throughout the main shop area suitable for connecting high-voltage welding equipment.

**ASSUMPTION:** Rating is 50A/240V industrial-grade, consistent with the conceptual electrical drawing legend and Decomposition Decision D-009. If County-supplied welder specifications differ, this requirement shall be revised as a scope change.

**NEMA Configuration (TBD) [Ref: A-002]:** The specific NEMA receptacle configuration for welding-grade 50A/240V receptacles (e.g., NEMA 6-50 for 250V or NEMA 14-50 for 125/250V) shall be confirmed against County welder specifications and DEL-004-09 before device procurement. Source: _SEMANTIC_LENSING.md A-002; Procedure Step 1.1.

Source: RFP §3.4; SOW-0057; Decomposition D-009

---

### REQ-015-03-02: Receptacle Type Mix

Receptacles of the following types shall be installed in quantities and locations per the IFC electrical drawings (DEL-004-05):

| Type | Rating | NEMA Configuration |
|---|---|---|
| General-purpose | 15A/120V | NEMA 5-15 (ASSUMPTION) |
| General-purpose | 20A/120V | NEMA 5-20 (ASSUMPTION) |
| Industrial | 20A/240V | TBD — confirm per DEL-004-09 |
| Heavy-duty | 30A/240V | TBD — confirm per DEL-004-09 |
| Welding-grade | 50A/240V | TBD — confirm per County welder specs and DEL-004-09 |

**NOTE [Ref: A-002]:** NEMA configuration for each rating above 15A/120V must be confirmed against DEL-004-09 and, for welding receptacles, against County welder specifications. Source: _SEMANTIC_LENSING.md A-002.

Source: SOW-0058; App B-Elec (legend); Decomposition §3

---

### REQ-015-03-03: Layout Conformance

Receptacle locations, quantities, and circuit assignments shall conform to the Issued for Construction (IFC) electrical drawings, including:
- DEL-004-05: Receptacle Layout Plans
- DEL-004-06: Panel Schedules

Source: RFP §3.3.2 (IFC drawings requirement); Decomposition DEL-004-05, DEL-004-06

---

### REQ-015-03-04: Code Compliance

All receptacle installation work shall comply with:
- Canadian Electrical Code (CEC) Part I — TBD: confirm specific edition year adopted in Alberta for this project, or confirm by cross-reference to DEL-004-09 (IFC Electrical Specification) [Ref: A-001]
- Alberta Safety Codes Act and applicable Safety Code Permits
- All other applicable provincial and municipal regulations

**NOTE [Ref: A-001]:** The phrase "current edition adopted in Alberta" is insufficient for a binding requirement. The specific CEC edition year must be confirmed against DEL-004-09 or the Alberta Safety Codes Council adoption schedule. Until confirmed, this is marked as ASSUMPTION: applicable edition TBD. Source: _SEMANTIC_LENSING.md A-001.

Source: RFP §3.3.2 ("The proposed building must adhere to all Alberta Safety Codes"); RFP §3.3.1 (permit responsibility)

---

### REQ-015-03-05: Three-Phase Supply Compatibility

All receptacle circuits shall be designed and installed compatible with the three-phase power supply established by DEL-015-01.

**Verification Detail [Ref: X-004]:** Verification of three-phase compatibility shall include measured phase identification at representative receptacle circuits (not only panel schedule review). The energized circuit test shall include phase rotation verification (for three-phase receptacles, if any) and voltage measurement between phases to confirm correct phase assignment per the panel schedule. Source: _SEMANTIC_LENSING.md X-004.

Source: RFP §3.4 ("The proposed building shall run on three-phase power"); Decomposition DEL-015-01

---

### REQ-015-03-06: Inspection

All electrical installation work shall be subject to inspection by the applicable Safety Codes Officer (Alberta). The County project representative shall be present for all inspections and provided a copy of all inspection reports.

Source: RFP §3.3.2

---

### REQ-015-03-07: GFCI and AFCI Protection

GFCI protection shall be provided for receptacle circuits in locations required by the CEC, including but not limited to the wash bay and other wet or damp locations.

**AFCI Protection [Ref: B-003]:** If the applicable CEC edition requires Arc-Fault Circuit Interrupter (AFCI) protection for any zone in this facility (e.g., office areas), AFCI protection shall be provided in accordance with the code. AFCI applicability is TBD — confirm against the specific CEC edition adopted for this project and DEL-004-09 (IFC Electrical Specification). Source: _SEMANTIC_LENSING.md B-003.

**ASSUMPTION:** Specific GFCI zone requirements to be confirmed in IFC electrical specification (DEL-004-09).

Source: ASSUMPTION based on CEC general requirements for wet/damp locations; App B-Elec (wash bay zone identified)

---

### REQ-015-03-08: Permanent Installation

All receptacles shall be permanently installed, properly secured, labelled, and terminated. Temporary power arrangements do not satisfy this deliverable.

**Workmanship Acceptance Criteria [Ref: D-003, A-003]:** The following measurable criteria shall apply to verification of permanent installation:
- **Securement:** Devices firmly attached to outlet box; no movement when plug is inserted or removed. TBD: confirm specific securement test criteria per DEL-004-09.
- **Labelling:** Circuit identification labels at each device and at the panelboard shall be legible, permanent (not handwritten unless specified), and match the as-built panel schedule.
- **Termination:** All terminations torqued to manufacturer-specified values; torque values documented.
- **Device alignment:** Devices installed plumb and flush with the wall surface. TBD: confirm alignment tolerance per DEL-004-09 or industry workmanship standards.
- **Cover plate fit:** Cover plates flush to wall, no gaps exceeding TBD mm (confirm per DEL-004-09 or industry standard).

Source: ASSUMPTION based on deliverable type (Installation) and OBJ-001 (code-compliant, fully functional facility); _SEMANTIC_LENSING.md D-003, A-003

---

### REQ-015-03-09: Device Grade (NEW) [Ref: C-002]

All receptacle devices shall be of a minimum grade appropriate for the installation environment. TBD: confirm whether specification-grade or industrial-grade devices are required per DEL-004-09 (IFC Electrical Specification).

**ASSUMPTION:** Specification-grade or industrial-grade devices are expected for a maintenance shop environment, based on the demanding physical conditions (mechanical damage risk, dust, moisture in wash bay). The device grade must be confirmed as a normative requirement once DEL-004-09 is available.

Source: _SEMANTIC_LENSING.md C-002; Datasheet Construction (Device Grade row)

---

### REQ-015-03-10: Cover Plate Environmental Ratings (NEW) [Ref: F-004]

Cover plates for receptacles in wet or hazardous locations (including but not limited to the wash bay) shall be rated for the environmental conditions. TBD: confirm required NEMA rating for weatherproof covers (e.g., NEMA 3R for raintight, or in-use rated covers per CEC) per DEL-004-09.

**ASSUMPTION:** Weatherproof/in-use covers are required in the wash bay zone based on CEC general requirements for wet/damp locations and the facility type (maintenance shop with wash-down operations).

Source: _SEMANTIC_LENSING.md F-004; Datasheet Construction (Cover Plates row); CEC Part I (general requirements for wet/damp locations)

---

## Standards

| Standard | Description | Status |
|---|---|---|
| Canadian Electrical Code (CEC) Part I | Governing electrical installation standard in Alberta | ASSUMPTION: applicable; specific edition year TBD — confirm per DEL-004-09 or Alberta Safety Codes Council adoption schedule [Ref: A-001] |
| Alberta Safety Codes Act | Provincial authority for safety code compliance and permits | Applicable (RFP §3.3.2) |
| CCDC 14–2013 | Design-Build Stipulated Price Contract form | Governing contract (Decomposition §1) |
| IFC Drawings (DEL-004-05, DEL-004-06) | Final authority on receptacle layout and circuit assignments | Required — location TBD pending PKG-004 completion |
| Electrical Specification (DEL-004-09) | Installation specification authority | Required — location TBD pending PKG-004 completion |

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-015-03-01: Welding receptacle rating | Confirm device rating (50A/240V) and NEMA configuration against IFC drawings and County welder specs; physical inspection of installed devices [Ref: A-002] |
| REQ-015-03-02: Receptacle type mix | Check-off against IFC receptacle layout plan (DEL-004-05); verify NEMA configuration for each rating; visual inspection [Ref: A-002] |
| REQ-015-03-03: Layout conformance | As-built comparison to IFC drawings (DEL-004-05, DEL-004-06) with defined acceptance protocol — see REQ-015-03-03 Verification Protocol below [Ref: D-002] |
| REQ-015-03-04: Code compliance | Safety Codes inspection and permit sign-off; inspection reports |
| REQ-015-03-05: Three-phase compatibility | Verify circuit phase assignments in panel schedule (DEL-004-06); energized circuit test including measured phase identification and voltage between phases at representative receptacle circuits [Ref: X-004] |
| REQ-015-03-06: Inspection | Inspection records showing County representative presence and copies received |
| REQ-015-03-07: GFCI and AFCI protection | GFCI outlet test (push-button test) or breaker test at all required locations; AFCI breaker test if applicable per CEC edition [Ref: B-003] |
| REQ-015-03-08: Permanent installation | Visual inspection per workmanship acceptance criteria (securement, labelling, termination torque, device alignment, cover plate fit); torque documentation reviewed [Ref: D-003, A-003] |
| REQ-015-03-09: Device grade | Confirm installed devices match specified grade per DEL-004-09; visual inspection of device markings [Ref: C-002] |
| REQ-015-03-10: Cover plate ratings | Confirm cover plate NEMA ratings in wet/hazardous locations per DEL-004-09; visual inspection [Ref: F-004] |

### REQ-015-03-03 Verification Protocol — As-Built Comparison [Ref: D-002]

The as-built comparison to IFC drawings shall include:
- **Reviewer:** TBD — confirm whether the Electrical Designer, Project Manager, or both review the as-built drawings.
- **Acceptance tolerance for location deviations:** TBD — define acceptable deviation from IFC drawing locations (e.g., within TBD mm unless approved by designer via field change authorization).
- **Sign-off authority:** TBD — confirm who signs off on as-built acceptance (Project Manager, Designer, or both).
- **Process:** Compare as-built drawings against IFC DEL-004-05 and DEL-004-06; document all deviations; obtain sign-off from the designated authority.

Source: _SEMANTIC_LENSING.md D-002; Procedure Step 5.3.

---

## Documentation

| Artifact | Description | Notes |
|---|---|---|
| Electrical Safety Code Permit | Permit issued for receptacle/electrical installation work | Required prior to energization |
| Inspection Reports | Safety Codes Officer reports for all electrical inspections | County rep to receive copies (RFP §3.3.2) |
| As-Built Drawings | Marked-up drawings showing installed receptacle locations and circuit IDs | Required for project closeout |
| Panel Schedule (as-built) | Updated circuit assignments as installed | Required for project closeout |
| Construction Completion Certificate (CCC) | Owner-issued upon final inspection and deficiency resolution | Required for contract closeout (RFP §2.14.3) |
| Torque Documentation | Record of termination torque values per manufacturer specification | Required for REQ-015-03-08 verification [Ref: A-004, D-003] |
| AFCI Test Records (if applicable) | Record of AFCI breaker test results, if AFCI protection is required | Required if CEC edition mandates AFCI [Ref: B-003] |
