# Specification: DEL-02-07 Emergency Power & Backup Generator

## Scope

### In Scope
This deliverable covers the design basis for the emergency power system for the Penhold Public Services Building (PSB) main building, including:
- Essential loads identification and list
- Generator sizing basis (diesel standby unit)
- Automatic Transfer Switch (ATS) and essential loads distribution design
- Runtime and fuel capacity assumptions
- Bay door secondary opening mechanism integration

### Out of Scope
- Generator installation construction drawings (these follow from the design basis established here)
- General electrical distribution for non-essential loads (see DEL-02-06)
- Overhead door specification and structural installation (see DEL-02-04)
- Site utilities and electrical service tie-in (see DEL-03-04)
- Optional scope items (access control, security/cameras — see RFP §12)

---

## Requirements

### REQ-01: Generator Provision
**Requirement:** A diesel backup generator shall be provided to supply electrical power to essential building loads during utility power interruptions.

**Source:** Addendum 03 §1.15; SOW-0222 (Decomposition PKG-002 table)

**Notes:** Generator is confirmed diesel-fuelled per SOW-0222 and Functional Program Appendix B (location TBD — exact wording partially obscured in accessed copy).

---

### REQ-02: Minimum Essential Loads
**Requirement:** At minimum, the following loads shall be served by the backup generator:
1. Kitchen (main building kitchen/breakroom area)
2. Meeting room / Incident Command Post (doubles as emergency management ICP)
3. Two (2) bathrooms

**Source:** Addendum 03 §1.15 (explicit); SOW-0222

**Notes:** The Design-Builder shall produce a complete essential loads list. Additional loads beyond the minimum above (e.g., fire alarm, communications, SCBA room, emergency lighting, PA system) shall be evaluated and included as appropriate per applicable codes and good engineering practice. **ASSUMPTION:** Code-required life-safety loads (fire alarm, emergency lighting) will be included in the essential loads list per ABC/NBCC requirements even if not explicitly enumerated in Addendum 03.

**Adequacy evaluation criteria [A-005]:** The essential loads list scope shall be evaluated against the following criteria to determine acceptability:
- (a) All code-required minimum loads (ABC/NBCC life-safety provisions) are included
- (b) All Owner-specified minimum loads (kitchen, ICP room, two bathrooms) are included
- (c) All loads necessary for Fire Department emergency operations (per OBJ-002) have been evaluated and included or explicitly excluded with documented rationale
- (d) The Owner has confirmed acceptance of the scope and any trade-offs (see Guidance Trade-off 2)

---

### REQ-03: Bay Door Secondary Opening Mechanism
**Requirement:** Overhead bay doors shall be equipped with a secondary opening mechanism operable when the building is on generator power. The secondary opening mechanism shall be either:
- (a) Powered by the generator (i.e., the door operator circuit is on the essential loads panel), OR
- (b) A manual override mechanism that permits door operation independent of electrical power.

**Source:** Addendum 03 §1.15; SOW-0216

**Notes:** Doors affected are the motorized 16 ft × 16 ft overhead doors in the fire apparatus bays and public works bays (OSR §10.3.9). The Design-Builder shall select the approach and document the design in this deliverable's artifacts, coordinating with DEL-02-04 and DEL-02-06.

---

### REQ-04: Generator Runtime
**Requirement:** The generator shall be sized to support the confirmed runtime duration. The Functional Program notes a 72-hour runtime target.

**Source:** SOW-0222 open issue note; Functional Program Appendix B row 30.0 (location TBD — text partially obscured)

**Status:** OPEN ISSUE — 72-hour runtime is noted as the Functional Program target but has not been formally confirmed by the Owner in Addendum 03. The Design-Builder shall confirm this requirement with the Owner prior to finalizing generator sizing. Until confirmed, 72 hours shall be used as the design basis assumption.

**ASSUMPTION:** Generator fuel tank shall be sized to deliver full essential-load output for the confirmed runtime duration without refuelling.

---

### REQ-05: Generator Location and Anchorage
**Requirement:** The generator shall be located in an outdoor area. The generator shall be anchored to its foundation/pad in accordance with applicable seismic and structural requirements, or a documented exemption shall be confirmed based on the post-disaster importance category ruling for this facility.

**Source:** Functional Program Appendix B row 30.0 (location TBD — row label confirms "Generator (Outdoor area)"); OSR §10.3.5 (post-disaster importance category exemption).

**Seismic anchorage requirement [F-001]:** Seismic anchorage requirements may or may not apply depending on the AHJ ruling on post-disaster importance category (see Guidance, Post-Disaster Importance Category consideration). The responsible engineer shall confirm with the AHJ whether seismic anchorage is required or exempted, and document the ruling. If required, generator anchorage shall be designed per applicable structural code provisions; if exempted, the exemption ruling shall be cited in the design basis documentation.

**ASSUMPTION:** Generator placement shall allow for safe exhaust dispersion, refuelling access, and maintenance clearance in accordance with manufacturer requirements and applicable codes.

**Cold-start reliability [F-003]:** The generator shall be capable of reliable cold-start at the design ambient temperature for Penhold, Alberta (currently TBD — expect -30C or colder). The responsible engineer shall confirm with the generator manufacturer that the selected unit is rated for the design temperature and that block heater and battery heater provisions are adequate. Generator selection, derating curves, and cold-start verification shall be documented in the detailed design phase.

---

### REQ-06: ATS and Distribution
**Requirement:** An Automatic Transfer Switch (ATS) shall be provided to automatically transfer essential loads from the utility supply to the generator upon utility failure, and to retransfer upon utility restoration.

**Source:** **[A-001] Normative source to be confirmed.** This requirement is currently sourced from ASSUMPTION and standard practice for diesel standby generator installations of this type. No explicit ATS requirement is stated in accessible sources, but the emergency operational requirement of Addendum 03 §1.15 and OBJ-002 imply it. The responsible engineer should confirm whether CSA C282 or the Canadian Electrical Code (CEC) mandate ATS for standby systems of this type. If a normative source (CSA C282 or CEC) confirms the requirement, cite it to strengthen enforceability.

**Notes:** The ATS rating, location, and sequencing shall be determined during design. Essential loads shall be served from a dedicated essential loads panel or clearly identified sub-panel.

**ATS Transfer Time Requirement [C-003, F-002]:** The maximum allowable time from utility failure to generator power on essential loads shall be specified in the verification table below. **Current status: TBD.** The responsible engineer shall confirm the applicable acceptance criterion from CSA C282 or CEC standards (text not yet accessed). Standard practice for standby systems typically specifies a maximum transfer time (e.g., 4-10 seconds depending on load sensitivity); the applicable threshold shall be determined and documented.

**ATS Location Coordination [X-002]:** The ATS location shall be confirmed as physically coordinated with the electrical room layout in DEL-02-06. This coordination shall go beyond a coordination meeting record to include a documented site plan or one-line diagram showing the ATS location and confirming spatial/routing compatibility with the electrical distribution design.

---

### REQ-07: Fuel Storage
**Requirement:** Diesel fuel storage shall be sufficient to support the confirmed runtime. Fuel storage shall comply with applicable codes for flammable liquid storage in the jurisdiction.

**Source:** ASSUMPTION — derived from REQ-04 runtime requirement and standard practice; no explicit fuel storage specification found in accessed sources.

**Notes:** Applicable codes include Alberta Fire Code and applicable CSA/NFPA standards for diesel fuel storage (location TBD).

**Fuel Storage Code Compliance [C-002, D-001]:** The design shall identify and address all applicable Alberta Fire Code provisions for diesel fuel storage above the applicable threshold (secondary containment, venting, environmental protection, labelling). For verification purposes, the responsible engineer shall explicitly cite which specific code provisions apply to the selected tank volume and design a compliant solution for each. Simply stating "code compliance confirmed by responsible engineer" is insufficient; the specific code requirements and the design approach for each shall be documented.

---

### REQ-08: Code Compliance
**Requirement:** The emergency power system shall comply with all applicable codes and standards including but not limited to: Alberta Building Code, National Building Code of Canada, and CSA C282 (Emergency Electrical Power Supply for Buildings).

**Source:** OSR §10.3.2 (general code compliance requirement for all systems); RFP §1 Definitions (CSA reference); CSA C282 — **ASSUMPTION: likely applicable** to emergency generator systems (standard text not accessed).

---

### REQ-09: Coordination with Electrical Distribution
**Requirement:** The emergency power system design shall be coordinated with the general electrical distribution design (DEL-02-06) to ensure:
- Essential loads panel is properly fed and rated
- ATS is integrated with the main electrical distribution
- Door operator circuits are incorporated in the essential loads panel if the generator-powered door option is selected

**Source:** OSR §10.4 (electrical systems coordination); ASSUMPTION for specific panel/ATS interface.

---

## Standards

| Standard | Applicability | Accessibility | Notes |
|---|---|---|---|
| Alberta Building Code (ABC) — current edition | Governing building code for Alberta; all electrical and mechanical systems | Not directly accessible — location TBD | — |
| National Building Code of Canada (NBCC) | Referenced in RFP §1; governs structural, electrical, and safety requirements | Not directly accessible — location TBD | — |
| CSA C22.1 Canadian Electrical Code (CEC) | Electrical installation standard; governs generator, ATS, panel, and wiring installation | Not directly accessible — ASSUMPTION: applicable | — |
| CSA C282 Emergency Electrical Power Supply for Buildings | Standard governing emergency generator systems in buildings | Not directly accessible — ASSUMPTION: likely applicable [A-003] | **[A-003]:** Applicability not yet confirmed. Responsible electrical engineer to confirm with AHJ and document whether CSA C282 applies to this standby generator installation. If applicable, will provide normative source for ATS requirements, transfer time acceptance criteria, cold-start parameters, generator performance thresholds, and load bank test duration [A-001, A-004, C-003, D-002, F-002]. |
| NFPA 110 Standard for Emergency and Standby Power Systems | Reference standard for standby generator systems; may be referenced in ABC/CSA | Not directly accessible — ASSUMPTION: may be referenced. [C-001] | **[C-001]:** Applicability unclear. Responsible engineer to confirm whether NFPA 110 is required or advisory for this installation; if required, will provide normative basis for generator sizing and performance parameters. |
| Alberta Fire Code | Governs diesel fuel storage on site | Not directly accessible — location TBD | **[D-001]:** Design-Builder to obtain applicable Alberta Fire Code provisions for fuel storage verification and cite specific code sections in design compliance documentation. |
| Alberta environmental/emission standards | Diesel exhaust emission standards and environmental protection requirements for permanently installed outdoor diesel generators in Alberta | Not directly accessible — location TBD | **[E-001]:** Environmental or emission standards may apply. Responsible engineer to confirm with Alberta Environment and Parks and applicable municipal bylaws; add relevant standards to the Standards table if applicable. |
| Municipal Noise Bylaws (Penhold) | Potential noise limits for outdoor diesel generator operation | Not directly accessible — location TBD | **[C-004]:** Generator noise and vibration impact on facility operations to be evaluated against Penhold municipal noise bylaws (location TBD); generator noise rating and proposed noise abatement measures to be documented. |
| CCDC 14 – 2013 (Design-Build contract) | Contract framework; Appendix J Supplementary Conditions | Referenced in RFP §1; text not accessed for this deliverable | — |

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-01: Generator provision | Design submission includes generator specification sheet and sizing basis document. **Generator start time acceptance criterion [F-002]:** TBD — maximum seconds from ATS signal to generator reaching rated voltage/frequency shall be specified per CSA C282 or manufacturer specs. **Voltage/frequency regulation [D-002]:** Generator output shall maintain voltage within TBD (+/- X%) and frequency within TBD (+/- Y Hz) under load. Acceptable ranges to be confirmed from CSA C282 and generator manufacturer specifications. |
| REQ-02: Minimum essential loads | Essential loads list submitted; all three minimum loads explicitly enumerated; demand calculations provided. **Simultaneous service criterion [X-003]:** Demand calculations shall demonstrate that the generator can serve all listed loads simultaneously (i.e., not assuming any demand diversity reduction that would prevent any essential load from being energized). |
| REQ-03: Bay door secondary opening | Design narrative or schematic shows door circuits on essential panel OR manual override confirmation from door manufacturer; coordinated with DEL-02-04. **Door count clarification [X-001]:** Exact number of overhead doors requiring secondary opening mechanism shall be confirmed and documented (coordinate with DEL-02-04 door schedule). |
| REQ-04: Runtime | Fuel tank sizing calculation demonstrates runtime meets confirmed target (72 hr or Owner-confirmed value) |
| REQ-05: Generator location and anchorage | Site/floor plan shows generator location in outdoor area with maintenance access and code clearances. **Seismic anchorage [F-001]:** Documentation confirming anchorage design meets applicable requirements, or documented AHJ exemption based on post-disaster importance category ruling. **Cold-start verification [F-003]:** Manufacturer cold-start data confirming operation at design ambient temperature (Penhold winter design temperature TBD); block heater and battery heater specifications documented. |
| REQ-06: ATS and distribution | One-line electrical diagram or schematic shows ATS, essential panel, and transfer logic; ATS specifications submitted. **ATS transfer time acceptance criterion [C-003, F-002]:** Transfer shall complete within TBD seconds per CSA C282 or CEC (acceptance threshold to be confirmed). **ATS location coordination [X-002]:** Documented site plan or one-line diagram confirming ATS location is physically coordinated with electrical room layout in DEL-02-06. |
| REQ-07: Fuel storage | Fuel storage specification shows volume sufficient for runtime. **Code compliance specificity [C-002, D-001]:** Design documentation shall cite specific applicable Alberta Fire Code provisions for the selected tank volume (secondary containment threshold, venting, environmental protection, labelling) and demonstrate compliance approach for each. |
| REQ-08: Code compliance | Design-Builder's responsible electrical engineer stamps and seals design documents per Alberta Engineering Act. Sealed documents shall reference all governing standards (ABC, NBCC, CSA C282 if confirmed applicable, etc.) and cite any AHJ exemptions or confirmations obtained during design. |
| REQ-09: Electrical coordination | Design coordination meeting record or coordination matrix shows DEL-02-06 and DEL-02-07 interfaces resolved. **ATS physical location coordination [X-002]:** ATS location shall be confirmed as physically coordinated (not merely that a coordination meeting occurred); documented via site plan or one-line diagram showing spatial resolution. |

---

## Documentation

### Required Artifacts (from _CONTEXT.md Anticipated Artifacts)

| Artifact | Description | Notes |
|---|---|---|
| Essential loads list | Enumerated list of all generator-served loads with demand (kW) values | Minimum loads per REQ-02; additional loads per code |
| Generator sizing basis | Calculation or narrative supporting generator kW rating selection | Reference to essential loads list |
| ATS/distribution design | Schematic or narrative for ATS, essential panel, and transfer arrangement | Coordinate with DEL-02-06 one-line diagram |
| Runtime/fuel assumptions | Documented runtime target, fuel consumption rate basis, and fuel tank volume | Note open issue on 72-hr runtime until confirmed |
| Bay door secondary opening mechanism integration | Design narrative or schematic showing door circuit inclusion on essential panel or manual override approach | Coordinate with DEL-02-04 door schedule [B-005 normalized] |

### Submission Format
- Format: TBD (to be consistent with Design-Builder's proposal submission requirements per RFP §4)
- As part of the proposal Design Brief narrative for this deliverable
