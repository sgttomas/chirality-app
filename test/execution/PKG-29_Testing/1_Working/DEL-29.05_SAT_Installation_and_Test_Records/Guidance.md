# Guidance: DEL-29.05 SAT Installation & Test Records

## Purpose

Guidance for **SAT Installation & Test Records** for **PKG-29 Testing**.

**Deliverable Purpose:** Provides evidence of completion, inspection, and testing for SAT. **Source:** Decomposition line 650

**Type:** Record | **Discipline:** T&C | **Responsible:** D&B Contractor (QA/QC)

## Principles

### SAT Philosophy

**System Integration Focus:** While FAT proves individual equipment, SAT proves the integrated system. SAT verifies:
- Equipment works together as a system
- Control logic coordinates multiple devices correctly
- Operator interfaces provide complete system control
- Safety systems protect across system boundaries

**"Fail-safe" Testing:** SAT emphasizes abnormal and emergency conditions:
- What happens when a sensor fails?
- Does the system shut down safely?
- Do alarms annunciate correctly?
- Can operators respond effectively?

**Source:** General SAT philosophy **ASSUMPTION**

### SAT vs. Commissioning

**SAT:** Proves system functionality in steady-state or controlled transient conditions
**Commissioning:** Proves system performance under actual operating conditions (with product)

SAT is prerequisite for commissioning but not a substitute.

## Considerations

**1. SAT Timing**
- After installation and individual component tests complete
- Before introducing product (commissioning)
- Adequate time for deficiency correction before commissioning schedule
- Coordinate with operations personnel availability (for training)

**2. SAT Procedure Development**
- May be Contractor-developed or vendor-supplied (for packaged systems)
- Should cover normal, abnormal, and emergency scenarios
- Should test from operator perspective (HMI, local panels)
- Should include acceptance criteria for each test

**3. Simulation and Actual Operation**
- Some SATs use simulation (jumpers, test signals) to avoid process upsets
- Some SATs require actual operation (pumps running, valves stroking)
- Balance between proving functionality and avoiding equipment damage

**4. Operations Training Integration**
- SAT is excellent opportunity for operations training
- Operations staff observe system response to various scenarios
- Operations staff practice using HMI and controls
- Document training attendance as part of SAT record

## Trade-offs

**Comprehensive SAT vs. Schedule:**
- Thorough SAT takes time; schedule pressure may encourage shortcuts
- **Recommendation:** Don't skip safety system testing or integration scenarios; finding problems during commissioning is more disruptive

**Simulation vs. Live Testing:**
- Simulation is safer but may not reveal all issues
- Live testing is more realistic but riskier
- **Recommendation:** Simulate abnormal/emergency conditions; use live operation for normal conditions where practical

## Examples

**SAT Report Example (Marine Loading System):**

```
SITE ACCEPTANCE TEST REPORT

System: Marine Loading System
SAT Procedure: SAT-PKG11-001 Rev A
SAT Date: 2024-10-15

Prerequisites Verified:
✓ Loading arms FAT complete
✓ Metering system FAT complete
✓ Installation complete (punch list items minor only)
✓ Hydrostatic tests passed
✓ Electrical and I&C loop checks complete

Functional Tests Performed:
1. Loading arm positioning: Manual and automatic modes → Pass
2. Flow control: Setpoint tracking within ±2% → Pass
3. Metering accuracy: Verified against proving tank, within ±0.15% → Pass
4. Emergency Release System (ERS): Actuated in <10 sec → Pass
5. High-level alarm: Alarm annunciated at setpoint → Pass
6. ESD shutdown: All equipment stopped on ESD signal → Pass
7. Communications: Shore-to-ship intercom functional → Pass

Integration Tests:
✓ Loading sequence: Arm deploy → valve open → pump start → flow control → Pass
✓ Shutdown sequence: Flow ramp down → pump stop → arm retract → Pass

Deficiencies: None critical; 2 minor punch list items (HMI label corrections)

Tested by: M. Engineer, Commissioning Lead (Sign/Date)
Witnessed by: R. Employer, Operations Manager (Sign/Date)

Photographs: SAT-PKG11-001 through 025
```

**Source:** Typical SAT report format **ASSUMPTION**

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | — | — | — | — | — | **TBD** |

---

## Cross-Document Linkage

| Document | Key Sections | Relationship |
|----------|--------------|--------------|
| Datasheet.md | §Attributes, §Construction | Provides factual context for system types and SAT content |
| Specification.md | §Requirements (FR, PR, IR, QR), §Standards, §Verification | Defines normative requirements that this Guidance supports |
| Procedure.md | §Steps 1-6 | Implements this Guidance through specific SAT management steps |

**Guidance-to-Specification Traceability:**
- §Principles (SAT Philosophy) → Supports Specification FR-2 (Scope)
- §Principles (SAT vs. Commissioning) → Supports Specification IR-2 (PKG-30 interface)
- §Considerations Item 1 (Timing) → Supports Specification FR-1 (Prerequisites)
- §Considerations Item 2 (Procedure Development) → Supports Specification QR-1
- §Considerations Item 4 (Operations Training) → Supports Specification PR-2 (Witness)
- §Trade-offs → Informs engineering decisions for Specification requirements

**Guidance-to-Procedure Traceability:**
- §Considerations Item 1 (Timing) → Procedure Step 1 (Prerequisites)
- §Considerations Item 2 (Procedure Development) → Procedure Step 2
- §Considerations Item 3 (Simulation vs. Actual) → Procedure Step 4
- §Considerations Item 4 (Operations Training) → Procedure Step 3
- §Examples (SAT Report) → Procedure Steps 4, 6
