# Agent and Workflow Review Rubric

Use the [component standard](../WORKFLOW_COMPONENT_STANDARD.md) and
[runtime contract](../AGENT_WORKFLOW_RUNTIME.md) as the design basis. Record the
reviewed revision, files, evidence boundary, and applicable human decisions.
Run the role and workflow validators to establish structural findings before
reviewing the substance.

## Roles

Read each role as a way of participating in the work. Assess:

- The characteristic attention and judgment are clear and distinct.
- PROTOCOL, SPEC, STRUCTURE, and RATIONALE contribute to that role without
  repeating one another.
- The role’s relationship to the human and other roles is coherent with the
  four-role design.
- Specialized methods, machine metadata, and run-specific contracts have their
  appropriate homes in workflows, runtime configuration, or briefs.
- The instruction is concise enough that its prominent commitments remain clear.

Review HELPS_HUMANS for making intention inspectable through inquiry and concrete
proposals, including correction of its own framing. Review WORKING_ITEMS for
integration of the undertaking and TASK for a usable bounded contribution.

## Workflows and tools

Follow the method from input through return, including branches and recovery.
Assess whether:

- Participating roles, delegation, review independence, and human decisions
  support the actual undertaking.
- Inputs, outputs, source authority, and acceptance checks agree with their
  consumers and current tools.
- Detailed resources are selected where needed rather than loaded by default.
- Claims have support proportional to their strength; gaps and conflicting
  evidence remain visible.
- Partial execution, subject defects, and tool failures have distinct returns.
- Snapshot, pointer, and handoff rules match the artifact’s authority class.
- Capabilities and write targets remain within the effective run contract.
- Repeated deterministic operations have reliable tool implementations and
  regression evidence appropriate to their consequences.

A workflow can coordinate many contributions. Its orchestration belongs to
WORKING_ITEMS; TASK receives a bounded workflow or brief. A tool performs a
defined operation, whose successful execution does not establish acceptance of
its subject.

## Findings and disposition

For every finding record the observed excerpt or behavior, applicable contract,
practical impact, proposed correction, and unresolved decision. Use these levels:

| Severity | Meaning |
|---|---|
| BLOCKER | Invalid authority, capability, scope, or executable contract |
| HIGH | Changes substantive results, decisions, or reliable handoff |
| MEDIUM | Material ambiguity, duplication, or compatibility drift |
| LOW | Local clarity or hygiene defect |
| INFO | Relevant observation without a demonstrated defect |

Distinguish structural validation from semantic review. Neither establishes an
unobserved host enforcement claim or comparative model-performance result.

A migration review accounts for every source component, verifies destination
interfaces, and records compatibility and downstream adoption work. Historical
records retain their original bytes; amendments identify what supersedes their
live architectural prescriptions. Proposals alone do not supply human acceptance.
