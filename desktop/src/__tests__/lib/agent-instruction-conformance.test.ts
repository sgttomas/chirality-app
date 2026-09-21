import { describe, expect, it } from 'vitest';
import { validateAgentInstructionConformance } from '../../lib/harness/agent-instruction';

function instructionFixture(overrides?: {
  frontmatter?: string;
  header?: string;
  tableRows?: string;
  sections?: string;
}): string {
  return `${overrides?.frontmatter ?? '---\ndescription: test agent\n---'}
${overrides?.header ?? `[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS - TASK (Bounded Test Agent)
AGENT_TYPE: 2`}

## Agent Type

| Property | Value |
|---|---|
${overrides?.tableRows ?? `| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK |
| **WRITE_SCOPE** | deliverable-local |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Test output |`}

${overrides?.sections ?? `[[BEGIN:PROTOCOL]]
protocol
[[END:PROTOCOL]]

[[BEGIN:SPEC]]
spec
[[END:SPEC]]

[[BEGIN:STRUCTURE]]
structure
[[END:STRUCTURE]]

[[BEGIN:RATIONALE]]
rationale
[[END:RATIONALE]]`}
`;
}

describe('validateAgentInstructionConformance', () => {
  it('accepts a complete AGENT_*.md instruction contract', () => {
    const report = validateAgentInstructionConformance({
      fileName: 'AGENT_TASK.md',
      content: instructionFixture()
    });

    expect(report).toEqual({ passed: true, issues: [] });
  });

  it('rejects nonconforming filenames and missing AGENT_TYPE declarations', () => {
    const report = validateAgentInstructionConformance({
      fileName: 'TASK.md',
      content: instructionFixture({
        header: `[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS - TASK (Bounded Test Agent)`,
        tableRows: `| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK |
| **WRITE_SCOPE** | deliverable-local |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Test output |`
      })
    });

    expect(report.passed).toBe(false);
    expect(report.issues).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ code: 'INVALID_AGENT_FILENAME', severity: 'error' }),
        expect.objectContaining({ code: 'MISSING_AGENT_TYPE', severity: 'error' })
      ])
    );
  });

  it('rejects invalid Agent Type table class values', () => {
    const report = validateAgentInstructionConformance({
      fileName: 'AGENT_TASK.md',
      content: instructionFixture({
        tableRows: `| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | WORKER |
| **INTERACTION_SURFACE** | INIT-TASK |
| **WRITE_SCOPE** | deliverable-local |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Test output |`
      })
    });

    expect(report.passed).toBe(false);
    expect(report.issues).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          code: 'INVALID_AGENT_CLASS',
          field: 'AGENT_CLASS',
          severity: 'error'
        })
      ])
    );
  });

  it('warns, but does not fail, when a Type 2 candidate is not classed as TASK', () => {
    const report = validateAgentInstructionConformance({
      fileName: 'AGENT_TASK.md',
      content: instructionFixture({
        tableRows: `| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | PERSONA |
| **INTERACTION_SURFACE** | INIT-TASK |
| **WRITE_SCOPE** | deliverable-local |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Test output |`
      })
    });

    expect(report.passed).toBe(true);
    expect(report.issues).toEqual([
      expect.objectContaining({
        code: 'TYPE2_NON_TASK_CLASS',
        field: 'AGENT_CLASS',
        severity: 'warning'
      })
    ]);
  });

  it('rejects missing required section marker pairs', () => {
    const report = validateAgentInstructionConformance({
      fileName: 'AGENT_TASK.md',
      content: instructionFixture({
        sections: `[[BEGIN:PROTOCOL]]
protocol
[[END:PROTOCOL]]`
      })
    });

    expect(report.passed).toBe(false);
    expect(report.issues).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ code: 'MISSING_SECTION_MARKER', field: 'SPEC' }),
        expect.objectContaining({ code: 'MISSING_SECTION_MARKER', field: 'STRUCTURE' }),
        expect.objectContaining({ code: 'MISSING_SECTION_MARKER', field: 'RATIONALE' })
      ])
    );
  });

  it('warns on unknown runtime metadata frontmatter keys', () => {
    const report = validateAgentInstructionConformance({
      fileName: 'AGENT_TASK.md',
      content: instructionFixture({
        frontmatter: `---
description: test agent
experimental_mode: true
---`
      })
    });

    expect(report.passed).toBe(true);
    expect(report.issues).toEqual([
      expect.objectContaining({
        code: 'UNKNOWN_FRONTMATTER_KEY',
        field: 'experimental_mode',
        severity: 'warning'
      })
    ]);
  });
});
