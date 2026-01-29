# Guidance: DEL-30.05 Integrated Systems Test Installation & Test Records

## Purpose

Supports development of **Integrated Systems Test Installation & Test Records** for PKG-30 Commissioning.

**Context:** Provides evidence of completion, inspection, and testing for integrated systems test. IST verifies systems work together before product introduction and operational handover.

**Source:** Decomposition §5 PKG-30, DEL-30.05

## Principles

**P-1: Integration Reveals Interface Issues**

Individual system commissioning (DEL-30.04) verifies systems work independently. Integrated systems testing reveals:
- Interface mismatches and communication issues
- Control logic errors across system boundaries
- Sequencing and timing issues
- Interlock conflicts
- Operational workflows and transitions

IST is essential for identifying and resolving integration issues before start-up.

**Source:** **ASSUMPTION** — IST rationale

**P-2: End-to-End Verification**

IST demonstrates complete operational scenarios:
- Product can flow from source (railcar) through entire path to destination (tank or ship)
- Control systems manage the entire transfer process
- Safety systems protect across all systems
- Operators can execute complete operations from HMI

This end-to-end verification builds confidence for operational readiness.

**Source:** **ASSUMPTION** — End-to-end testing rationale

**P-3: Operational Flexibility Demonstration**

IST specifically verifies OBJ-4 (Operational Flexibility):
- Tank storage mode: Railcar → Tank, Tank → Ship (two-step)
- Direct rail-to-ship mode: Railcar → Ship (one-step, bypassing tank storage)
- Valve lineup changes and routing verification

Operational flexibility is critical business requirement that must be demonstrated.

**Source:** Decomposition §2 OBJ-4 (Operational Flexibility)

## Considerations

**C-1: Test Scenarios**

Define comprehensive IST scenarios covering:
- **Normal operations:** All standard transfer paths
- **Abnormal operations:** Alarm responses, interlock trips, emergency shutdowns
- **Operational transitions:** Mode changes, routing changes
- **Material balance:** Product accountability through metering systems

Scenarios should represent actual operational use cases.

**Source:** **ASSUMPTION** — IST scenario coverage

**C-2: Operations Involvement**

Operations personnel should:
- Participate in IST execution (training opportunity)
- Verify operational workflows are practical
- Provide acceptance sign-off

IST is transition point from commissioning to operations.

**Source:** **ASSUMPTION** — Operations transition

**C-3: IST Without Product**

IST typically performed with water or air (not actual CSD canola oil product):
- Water testing for liquid systems (flow paths, metering, pumps)
- Air testing for vapor spaces and instruments
- Simulated product introduction scenarios

Actual product introduction occurs during start-up phase after IST complete.

**Source:** **ASSUMPTION** — IST test medium

## Trade-offs

**T-1: IST Comprehensiveness vs. Schedule**

**Trade-off:** Comprehensive IST scenarios provide high confidence but extend schedule; streamlined IST enables faster start-up but may miss integration issues.

**Recommendation:** Risk-based IST scope; comprehensive scenarios for safety-critical and revenue-critical paths; streamlined for less critical scenarios.

**Source:** **ASSUMPTION**

## Examples

**Anticipated Artifacts:**
- IST test protocols with acceptance criteria
- End-to-end scenario test records (railcar → tank, tank → ship, direct rail → ship)
- Control system integration test results
- Safety interlock integration test results
- Emergency shutdown verification records

**Source:** Decomposition §5 DEL-30.05; Datasheet.md

## Conflict Table (for human ruling)

No conflicts identified during document enrichment. If conflicts arise during IST execution, they will be documented here:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none) | | | | | | |

**Note:** Cross-deliverable conflicts are handled by RECONCILIATION agent when requested; this table captures only local conflicts within DEL-30.05 scope.

---

## Document Cross-References

- **← Datasheet.md / Specification.md:** Rationale for IST requirements
- **→ Procedure.md:** Considerations inform IST execution
