---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-07-01
package_id: PKG-07
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-028, SOW-029, SOW-030, SOW-031, SOW-244, SOW-248]
package_objective_refs: [OBJ-007]
---

# DEL-07-01 — Retained PEC receiving compatibility

## Purpose and Objective Traceability

PEC is retired as an active product programme. This deliverable contributes what is left of PEC receiving in the App: the meaning of the retained PEC compatibility material, so that wherever that material is still shown or read it is understood as a constructed example with its limits and never as a live, qualified or adopted service. The App owes no PEC first-consumer adapter, provider witness, release or adoption, and nothing in the App depends on one.

It serves OBJ-007, "Consume optional PEC and later Domains capability through explicit receiving contracts with truthful fallback", as that objective now stands in PRD §2.3 and V4-CON-02, HOST_INTEGRATION V4-HI-61 and ARCHITECTURE V4-ARC-22: PEC delivery and adoption are no longer required, and existing PEC material remains for compatibility. The decomposition row DEL-07-01 and its scope items SOW-028, SOW-244 and SOW-248 describe a first-consumer contract, adapter and adoption evidence; the PRD governs, and none of those is owed. SOW-030 and SOW-031 still apply to retained material; SOW-029 applies as far as keeping source identity and limitations inspectable, and coverage and freshness of consumed PEC material are shown under `DEL-07-02`. The draft 4.0.0 release target names no exit criterion for this deliverable.

## Deliverable Definition — Ontology

- **OUT-003** — The retained PEC compatibility material: the PEC values of the connector standing (the connector value for PEC and its two claim tiers), the form of a PEC receiving record, and the constructed PEC cases that exercise them. Supports SOW-029, SOW-030 and SOW-031; OBJ-007.

Terms:

- **Retained PEC material.** PEC forms and cases kept so that what already reads them keeps working. All of it is constructed, and is marked simulated as `DEL-07-02` defines: none comes from a live PEC service, and none has an adoption behind it.
- **Record tier** (`record`). A PEC claim derived from project files, which reports what its cited file states.
- **Presence tier** (`presence_advisory`). A PEC statement that an agent or session is present. It is advisory, and is never evidence that anything is correct, ready or permitted.
- **PEC receiving record.** What is recorded for one PEC response to a question, or for no response. It carries the content `DEL-07-02` defines for every connector's receiving record.

Boundary:

- **CLM-004** — `DEL-07-02` owns the standing, the reliance rule, the prohibited conclusions and the source-file route common to every connector, and applies them to retained PEC material; this deliverable supplies only what the PEC tiers mean. `DEL-06-01` owns the fleet records a connector would observe. Execution stays with the agents and managers assigned to it, and every human decision with the person. No PEC provider, adapter, qualification, release or adoption is part of this project.

## Completion and Reliance Basis — Epistemology

- **REQ-002** — Retained PEC material is compatibility material. Nothing the App shows or records presents it as a qualified, released or adopted live PEC service, and no function of the App depends on a PEC provider. [PRD §2.3, V4-CON-02; ARCHITECTURE V4-ARC-22]
- **REQ-003** — Where retained PEC material is shown or read, its source identity and its limitations stay inspectable. [SOW-029; HOST_INTEGRATION V4-HI-61]
- **REQ-004** — PEC material confers no authority to execute and makes no human decision. A presence-tier statement never supports reliance. [SOW-030, SOW-031; PRD V4-CON-02]
- **REQ-005** — An absent PEC input never means empty work, permission or readiness. [PRD V4-CON-03]
- **REQ-007** — This deliverable performs no act owned by another (CLM-004): it defines no standing, reliance rule or route (`DEL-07-02`), writes no fleet record (`DEL-06-01`), and builds or requires no PEC provider, adapter or successor product.
- **REQ-009** — A change to retained PEC material keeps the forms that existing readers of it depend on, and keeps absence and limitations truthful.

- **AC-002** — With no PEC provider present, every function of the App works. Wherever retained PEC material appears in the App it is marked simulated, and nothing shown or recorded states that a PEC service is available, qualified, released or adopted. Verify by VER-002. [REQ-002]
- **AC-003** — Retained PEC material that is shown or read carries its source identity and its limitations, and a value it does not supply is shown as missing. Verify by VER-003. [REQ-003]
- **AC-004** — A presence-tier statement is shown as advisory and supports no reliance, whatever its envelope and condition. No reading or showing of PEC material starts, dispatches or permits work, or writes a human decision. Verify by VER-004. [REQ-004]
- **AC-005** — With the PEC input absent, the App shows it as absent, and nothing shown or recorded concludes empty work, permission or readiness. Verify by VER-005. [REQ-005]
- **AC-007** — Nothing in the retained PEC material defines a standing rule or a route of its own, writes a fleet record, or calls for a PEC provider, adapter or successor to be delivered. Verify by VER-007. [REQ-007]
- **AC-009** — After a change to retained PEC material, a standing that names PEC and a PEC receiving record written before the change are read with the same result as before it. Verify by VER-009. [REQ-009]

## Production and Verification Method — Praxeology

This deliverable has no module of its own. Its criteria are examined on the App's connector presentation, which `DEL-07-02` builds, using constructed PEC material whose expected treatment follows from the tier meanings above and the rules of `DEL-07-02`.

- **VER-002** — Executable check combined with judgment by a named role (an independent reviewer): runs the App's functions with no PEC provider present, observes that constructed PEC material is marked simulated wherever it appears, and reads what is shown and recorded for any statement of an available, qualified, released or adopted PEC service.
- **VER-003** — Executable check (observes the source identity and limitations shown for constructed PEC material, including material with a value not supplied).
- **VER-004** — Executable check (observes that a presence-tier statement supports no reliance in every combination of envelope and condition, and that reading and showing PEC material writes no record of execution, dispatch, permission or human decision).
- **VER-005** — Executable check (observes what the App shows and records with the PEC input absent).
- **VER-007** — Judgment by a named role (an independent reviewer): reads the retained PEC material against each act REQ-007 excludes and the allocation in CLM-004.
- **VER-009** — Comparison with a named reference (PEC standings and PEC receiving records saved before the change): reads them after the change and compares the results.

## Governing Values and Decisions — Axiology

- **AX-003** — PEC is retired, and what remains is kept only so that existing readers of it keep working. Better means retained PEC material that a reader mistakes for a live service less often, by plainer marking of what is constructed and what was never established; never by altering a form an existing reader depends on, and never by dropping a limit from material still shown.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-003 | SOW-028 OBJ-007 | REQ-002 | AC-002 | VER-002 | Owner ruling: PRD §2.3 and V4-CON-02 retire PEC delivery and adoption. The comparison is of what the App requires, shows and records against that ruling. |
| OUT-003 | SOW-029 OBJ-007 | REQ-003 | AC-003 | VER-003 | Outside source: the constructed input itself, which the product did not write, gives the source identity and limits that must appear. PRD V4-CON-02 states that they are exposed. |
| OUT-003 | SOW-030 SOW-031 OBJ-007 | REQ-004 | AC-004 | VER-004 | Owner ruling: the accepted decomposition's scope items SOW-030 and SOW-031, and PRD V4-CON-02. |
| OUT-003 | SOW-244 OBJ-007 | REQ-005 | AC-005 | VER-005 | Owner ruling: PRD V4-CON-03 names what a missing feed may not imply. |
| OUT-003 | SOW-248 OBJ-007 | REQ-007 CLM-004 | AC-007 | VER-007 | Owner ruling: PRD §2.3 and the accepted decomposition's allocation of each act, read against the retained material. |
| OUT-003 | SOW-029 OBJ-007 | REQ-009 | AC-009 | VER-009 | The product's own earlier output. Sameness is the commitment here; the comparison guards against change and claims no correctness. |
