# Specification: DEL-30.08 Cathodic Protection Test & Commissioning Installation & Test Records

## Scope

Defines requirements for **Cathodic Protection Test & Commissioning Installation & Test Records** for the Canola Oil Transload Facility — Phase 1.

**Purpose:** Provides evidence of completion, inspection, and testing for cathodic protection test & commissioning.

**Artifacts:** CP commissioning test sheets, rectifier settings, baseline potentials, acceptance records

**Source:** Decomposition §5 PKG-30, DEL-30.08

## Requirements

### Functional Requirements

**FR-1: CP System Scope**
- CP commissioning shall cover all cathodically protected structures:
  - Underground product piping
  - Marine structures (steel piles, sheet piling, submerged steel)
  - Buried steel structures (if applicable)
  - Storage tank bottoms (if in soil/groundwater contact)
- **Source:** **ASSUMPTION** — CP system scope for marine terminal facility

**FR-2: Pre-Commissioning Electrical Tests**
- CP commissioning shall include pre-energization tests:
  - Anode-to-structure electrical continuity
  - Structure electrical isolation from foreign structures
  - Stray current surveys
  - Short circuit detection
- **Source:** **ASSUMPTION** — CP pre-commissioning tests per NACE SP0169

**FR-3: Rectifier Commissioning**
- Rectifier commissioning shall document:
  - Nameplate data verification
  - Output settings (voltage, current, tap position)
  - Output verification under load
  - Automatic controls testing
  - Safety features (overcurrent, lightning protection)
- **Source:** **ASSUMPTION** — Rectifier commissioning scope

**FR-4: Baseline Potential Survey**
- Baseline potential survey shall measure and document:
  - CP-off potentials (native structure potentials before CP energization)
  - CP-on potentials (potentials after CP system energization)
  - Polarization shift verification (CP effectiveness)
  - Protective criteria met per NACE SP0169 or project standard — **TBD**
- **Source:** NACE SP0169; **ASSUMPTION: likely applicable**; **location TBD**

**FR-5: CP System Acceptance**
- CP commissioning shall demonstrate:
  - Protective potentials achieved on all structures
  - Rectifier output adequate and stable
  - No adverse effects (stray current interference, coating damage)
  - System ready for service and ongoing monitoring
- **Source:** **ASSUMPTION** — CP acceptance criteria

### Performance Requirements

**PR-1: Protective Criteria Achievement**
- CP system shall achieve protective criteria per NACE SP0169 or project standard:
  - -850 mV criterion (copper-copper sulfate reference electrode), or
  - 100 mV polarization shift from native potential, or
  - Other criteria per design — **TBD**
- Protective potentials shall be achieved on all protected structures
- **Source:** NACE SP0169; **ASSUMPTION: likely applicable**; **location TBD**

**PR-2: Long-Term Reliability (OBJ-1, OBJ-9)**
- CP commissioning establishes baseline for lifecycle corrosion management
- Baseline potentials enable future monitoring and CP effectiveness verification
- Supports facility long-term integrity (OBJ-1) and lifecycle cost optimization (OBJ-9)
- **Source:** Decomposition §2 OBJ-1 (Reliability), OBJ-9 (Lifecycle Cost Optimization)

### Interface Requirements

**IR-1: CP System Design Interface**
- CP commissioning shall verify installation per CP design (PKG-03, PKG-08, PKG-14)
- **Source:** Decomposition §4, §5 (PKG-03: Underground Utilities, PKG-08: Marine Structures, PKG-14: Process Piping)

**IR-2: Regulatory Interface**
- CP commissioning may require regulatory authority witness or acceptance
- **Source:** **ASSUMPTION** — Regulatory requirements for CP systems; **location TBD**

**IR-3: Operations and Maintenance Interface**
- CP commissioning records provide baseline for ongoing CP monitoring (covered in PKG-31 O&M Manuals)
- **Source:** Decomposition §4 PKG-31; **ASSUMPTION**

### Quality Requirements

**QR-1: CP Specialist Qualification**
- CP commissioning shall be performed by or supervised by qualified CP specialist (NACE certification or equivalent)
- **Source:** **ASSUMPTION** — CP specialist qualification requirements; NACE standards

**QR-2: Approval and Sign-off**
- CP commissioning records require: CP specialist, commissioning engineer, corrosion engineer, QC inspector sign-offs
- Regulatory authority acceptance if required
- **Source:** **ASSUMPTION**

**QR-3: Baseline Data Quality**
- Baseline potential data critical for future CP monitoring
- Data shall be accurate, complete, and properly documented
- **Source:** **ASSUMPTION** — CP monitoring baseline criticality

## Standards

- **NACE SP0169** — Control of External Corrosion on Underground or Submerged Metallic Piping Systems — **ASSUMPTION: likely applicable** — **location TBD**
- **CSA Z662** — Cathodic protection requirements for oil and gas pipelines — **location TBD**
- **ISO 15589** — Petroleum, petrochemical and natural gas industries — Cathodic protection of pipeline systems — **ASSUMPTION: may apply** — **location TBD**
- Employer's Requirements — **TBD: location**

**Source:** **ASSUMPTION: likely applicable** standards for CP systems

## Verification

- CP system electrical tests complete
- Rectifier commissioning complete and settings documented
- Baseline potential survey complete
- Protective criteria achieved on all structures
- Sign-offs obtained
- Acceptance criteria met

**Acceptance:** CP system commissioned, protective potentials achieved, baseline established, corrosion engineer and regulatory authority acceptance obtained

## Documentation

**Outputs:** CP commissioning test sheets, rectifier settings records, baseline potential survey data, acceptance records

**Format:** CP test datasheets and survey records — **TBD**

**Submittal:** Upon CP commissioning completion; stored in `3_Issued/DEL-30.08/`

**Source:** Decomposition §5 DEL-30.08

---

## Document Cross-References

- **← Datasheet.md:** Requirements for CP commissioning scope and testing
- **→ Guidance.md:** Rationale for CP system commissioning
- **→ Procedure.md:** CP commissioning test execution process
