# Guidance: DEL-30.08 Cathodic Protection Test & Commissioning Installation & Test Records

## Purpose

Supports development of **Cathodic Protection Test & Commissioning Installation & Test Records** for PKG-30 Commissioning.

**Context:** Provides evidence of completion, inspection, and testing for cathodic protection test & commissioning. CP systems protect underground and submerged steel from corrosion, critical for long-term facility integrity.

**Source:** Decomposition §5 PKG-30, DEL-30.08

## Principles

**P-1: Corrosion Protection is Lifecycle Asset Management**

Cathodic protection prevents external corrosion on buried and submerged steel:
- Underground piping corrodes without protection (soil corrosivity)
- Marine structures corrode rapidly in seawater (highly aggressive environment)
- Corrosion leads to leaks, failures, safety hazards, environmental incidents
- CP systems provide continuous protection throughout facility life

CP commissioning establishes protection and baseline for lifecycle monitoring. This supports:
- **OBJ-1:** Safe & Reliable Operation (prevent corrosion failures)
- **OBJ-7:** Environmental Protection (prevent leaks and spills)
- **OBJ-9:** Lifecycle Cost Optimization (prevent costly corrosion repairs)

**Source:** Decomposition §2 OBJ-1, OBJ-7, OBJ-9; **ASSUMPTION** — CP criticality

**P-2: Protective Criteria Verification**

CP commissioning verifies protective potentials achieved:
- **Native potential:** Structure potential before CP (typically -500 to -700 mV vs. CSE for steel in soil/water)
- **Protective potential:** Structure potential with CP active (typically -850 mV or more negative vs. CSE, or 100 mV polarization)
- **Criteria per NACE SP0169 or project standard** — **TBD**

Baseline potential survey provides objective evidence of CP effectiveness and baseline for future monitoring.

**Source:** NACE SP0169; **ASSUMPTION: likely applicable**; **location TBD**

**P-3: Marine Environment Corrosivity**

Fraser Surrey Terminal is marine environment (coastal, seawater exposure):
- Highly corrosive to steel structures (marine piles, sheet piling)
- Submerged zone, splash zone, tidal zone all require protection
- Seawater conductivity enables effective impressed current CP
- Marine CP requires specialized design and commissioning

CP commissioning for marine structures requires marine corrosion expertise.

**Source:** Decomposition §1.1 (Location: Fraser Surrey Terminal, coastal); **ASSUMPTION** — Marine corrosion considerations

## Considerations

**C-1: CP System Types**

CP systems may include:
- **Galvanic (Sacrificial) Anodes:** Magnesium or zinc anodes for localized protection
- **Impressed Current CP (ICCP):** Rectifier-driven systems for large structures
- **Hybrid systems:** Combination of galvanic and impressed current

Commissioning approach depends on CP system type.

**Source:** **ASSUMPTION** — CP system types

**C-2: Test Equipment and Methods**

CP commissioning requires specialized equipment:
- High-impedance voltmeter for potential measurements
- Reference electrodes (copper-copper sulfate or silver-silver chloride for seawater)
- Test stations (permanent monitoring points)
- Interruption equipment for "CP-off" potential measurement

Qualified CP technician required for accurate measurements.

**Source:** NACE SP0169; **ASSUMPTION: likely applicable**

**C-3: Baseline Data for Future Monitoring**

CP commissioning baseline critical for operations:
- Baseline potentials enable trend analysis
- Future surveys compare to baseline to verify continued protection
- Rectifier settings documented for maintenance reference
- Baseline informs ongoing CP monitoring program

High-quality baseline data supports lifecycle corrosion management.

**Source:** **ASSUMPTION** — CP monitoring baseline importance

**C-4: Regulatory Requirements**

CP systems may require regulatory oversight:
- Pipeline CP systems subject to CSA Z662 and regulatory authority requirements
- Marine structure CP may require Transport Canada or environmental authority acceptance
- Documentation requirements for regulatory compliance (OBJ-6)

Verify regulatory requirements and witness/acceptance needs.

**Source:** Decomposition §2 OBJ-6 (Regulatory Compliance); **ASSUMPTION**; **location TBD**

## Trade-offs

**T-1: CP Commissioning Timing vs. System Availability**

**Trade-off:** Early CP commissioning protects structures sooner but may occur before backfill/coating cure complete; delayed CP commissioning allows construction completion but exposes structures to corrosion during delay.

**Recommendation:** Commission CP systems as soon as practical after structure installation and coating cure; balance protection with construction access needs.

**Source:** **ASSUMPTION**

**T-2: Baseline Survey Comprehensiveness vs. Efficiency**

**Trade-off:** Comprehensive baseline survey (all test stations, detailed profiling) provides better monitoring baseline but takes more time; streamlined survey enables faster commissioning but may lack detail for future troubleshooting.

**Recommendation:** Comprehensive baseline for critical structures (marine structures, large diameter piping); streamlined for less critical structures.

**Source:** **ASSUMPTION**

## Examples

**Anticipated Artifacts:**

1. **CP Commissioning Test Sheets:** System ID, test date, test equipment, continuity test results, isolation test results, stray current survey results, energization data, potential measurements

2. **Rectifier Settings:** Rectifier ID, nameplate data, initial settings (voltage, current, taps), output verification, controls testing

3. **Baseline Potentials:** Test station locations, reference electrode type, CP-off potentials, CP-on potentials, polarization shift, protective criteria verification

4. **Acceptance Records:** CP specialist certification, corrosion engineer acceptance, regulatory authority acceptance (if required), commissioning completion certificate

**Source:** Decomposition §5 DEL-30.08; Datasheet.md

## Conflict Table (for human ruling)

No conflicts identified during document enrichment. If conflicts arise during CP commissioning, they will be documented here:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none) | | | | | | |

**Note:** Cross-deliverable conflicts are handled by RECONCILIATION agent when requested; this table captures only local conflicts within DEL-30.08 scope.

---

## Document Cross-References

- **← Datasheet.md / Specification.md:** Rationale for CP commissioning requirements
- **→ Procedure.md:** Considerations inform CP commissioning execution
