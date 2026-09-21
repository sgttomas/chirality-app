import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { evaluateSubagentGovernance } from '../../lib/harness/subagent-governance';

let tmpDir = '';

type FixtureOptions = {
  personaContent?: string;
  additionalAgents?: Array<{
    name: string;
    content: string;
  }>;
};

async function createInstructionRootFixture(options?: FixtureOptions): Promise<string> {
  tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-subagent-governance-'));
  const instructionRoot = path.join(tmpDir, 'instruction-root');
  const agentsDir = path.join(instructionRoot, 'agents');
  const docsDir = path.join(instructionRoot, 'docs');

  await mkdir(agentsDir, { recursive: true });
  await mkdir(docsDir, { recursive: true });

  await writeFile(path.join(instructionRoot, 'README.md'), '# instruction root\n', 'utf8');
  await writeFile(path.join(instructionRoot, 'AGENTS.md'), '# index\n', 'utf8');
  await writeFile(path.join(docsDir, 'DIRECTIVE.md'), '# directive\n', 'utf8');
  await writeFile(path.join(docsDir, 'CONTRACT.md'), '# contract\n', 'utf8');
  await writeFile(path.join(docsDir, 'SPEC.md'), '# spec\n', 'utf8');
  await writeFile(path.join(docsDir, 'TYPES.md'), '# types\n', 'utf8');
  await writeFile(path.join(docsDir, 'PLAN.md'), '# plan\n', 'utf8');

  await writeFile(
    path.join(agentsDir, 'AGENT_WORKING_ITEMS.md'),
    options?.personaContent ??
      `---
description: test persona
---
# AGENT WORKING_ITEMS
AGENT_TYPE: 1

| Property | Value |
|---|---|
| **AGENT_CLASS** | PERSONA |
`,
    'utf8'
  );

  if (options?.additionalAgents) {
    for (const agent of options.additionalAgents) {
      await writeFile(path.join(agentsDir, `AGENT_${agent.name}.md`), agent.content, 'utf8');
    }
  }

  return instructionRoot;
}

const validGovernance = {
  contextSealed: true,
  pipelineRunApproved: true,
  approvalRef: 'GATE-001',
  approvedBy: 'human-reviewer'
};

function withSubagentEnv(value: 'true' | 'false'): NodeJS.ProcessEnv {
  return {
    ...process.env,
    CHIRALITY_ENABLE_SUBAGENTS: value
  };
}

afterEach(async () => {
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  vi.restoreAllMocks();

  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('evaluateSubagentGovernance', () => {
  it('denies when CHIRALITY_ENABLE_SUBAGENTS is not true', async () => {
    process.env.CHIRALITY_INSTRUCTION_ROOT = await createInstructionRootFixture({
      personaContent: `---
description: test persona
subagents: TASK
---
# AGENT WORKING_ITEMS
AGENT_TYPE: 1
`
    });
    const infoSpy = vi.spyOn(console, 'info').mockImplementation(() => {});

    const result = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      validGovernance,
      withSubagentEnv('false')
    );

    expect(result).toMatchObject({
      allowed: false,
      gate: 'ENVIRONMENT'
    });
    expect(infoSpy).toHaveBeenCalled();
  });

  it('denies when the persona is not allowlisted for subagents', async () => {
    process.env.CHIRALITY_INSTRUCTION_ROOT = await createInstructionRootFixture();

    const result = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      validGovernance,
      withSubagentEnv('true')
    );

    expect(result).toMatchObject({
      allowed: false,
      gate: 'PERSONA_ALLOWLIST'
    });
  });

  it('denies when governance metadata is missing or invalid', async () => {
    process.env.CHIRALITY_INSTRUCTION_ROOT = await createInstructionRootFixture({
      personaContent: `---
description: test persona
subagents: TASK
---
# AGENT WORKING_ITEMS
AGENT_TYPE: 1
`
    });

    const result = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      undefined,
      withSubagentEnv('true')
    );

    expect(result).toMatchObject({
      allowed: false,
      gate: 'METADATA_PRESENCE'
    });
  });

  it('denies when strict governance booleans are not true', async () => {
    process.env.CHIRALITY_INSTRUCTION_ROOT = await createInstructionRootFixture({
      personaContent: `---
description: test persona
subagents: TASK
---
# AGENT WORKING_ITEMS
AGENT_TYPE: 1
`
    });

    const contextDenied = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      {
        ...validGovernance,
        contextSealed: 'true'
      },
      withSubagentEnv('true')
    );
    const pipelineDenied = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      {
        ...validGovernance,
        pipelineRunApproved: 1
      },
      withSubagentEnv('true')
    );

    expect(contextDenied).toMatchObject({
      allowed: false,
      gate: 'CONTEXT_SEALED'
    });
    expect(pipelineDenied).toMatchObject({
      allowed: false,
      gate: 'PIPELINE_RUN_APPROVED'
    });
  });

  it('denies when approvalRef is empty', async () => {
    process.env.CHIRALITY_INSTRUCTION_ROOT = await createInstructionRootFixture({
      personaContent: `---
description: test persona
subagents: TASK
---
# AGENT WORKING_ITEMS
AGENT_TYPE: 1
`
    });

    const result = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      {
        ...validGovernance,
        approvalRef: '   '
      },
      withSubagentEnv('true')
    );

    expect(result).toMatchObject({
      allowed: false,
      gate: 'APPROVAL_REF'
    });
  });

  it('allows and resolves only TYPE 2 delegated subagents', async () => {
    process.env.CHIRALITY_INSTRUCTION_ROOT = await createInstructionRootFixture({
      personaContent: `---
description: test persona
subagents: TASK, CHANGE
---
# AGENT WORKING_ITEMS
AGENT_TYPE: 1
`,
      additionalAgents: [
        {
          name: 'TASK',
          content: `---
description: task
---
# AGENT TASK
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | TASK |
`
        },
        {
          name: 'CHANGE',
          content: `---
description: change
---
# AGENT CHANGE
AGENT_TYPE: 1

| Property | Value |
|---|---|
| **AGENT_CLASS** | PERSONA |
`
        }
      ]
    });
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    const result = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      validGovernance,
      withSubagentEnv('true')
    );

    expect(result).toMatchObject({
      allowed: true,
      gate: 'ALLOW',
      delegatedSubagents: ['TASK']
    });
    expect(errorSpy).toHaveBeenCalledWith(
      expect.stringContaining(
        'Candidate subagent rejected: CHANGE declares AGENT_TYPE=TYPE 1; expected TYPE 2.'
      )
    );
  });

  it('allows configured Agent 0 managers and TASK while rejecting other Agent 2 roles', async () => {
    process.env.CHIRALITY_INSTRUCTION_ROOT = await createInstructionRootFixture({
      personaContent: `---
description: test Agent 0
subagents: PROJECT_SETUP, TASK, SPECIALIST
---
# AGENT HELP_HUMAN
AGENT_TYPE: 0
`,
      additionalAgents: [
        {
          name: 'PROJECT_SETUP',
          content: `---
description: manager
---
# AGENT PROJECT_SETUP
AGENT_TYPE: 1

| Property | Value |
|---|---|
| **AGENT_CLASS** | PERSONA |
`
        },
        {
          name: 'TASK',
          content: `---
description: task
---
# AGENT TASK
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | TASK |
`
        },
        {
          name: 'SPECIALIST',
          content: `---
description: dedicated specialist
---
# AGENT SPECIALIST
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | PERSONA |
`
        }
      ]
    });
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    const result = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      validGovernance,
      withSubagentEnv('true')
    );

    expect(result).toMatchObject({
      allowed: true,
      gate: 'ALLOW',
      delegatedSubagents: ['PROJECT_SETUP', 'TASK']
    });
    expect(result.delegatedAgentInstructions?.TASK?.agentType).toBe(2);
    expect(errorSpy).toHaveBeenCalledWith(
      expect.stringContaining(
        'Candidate subagent rejected: SPECIALIST declares AGENT_TYPE=TYPE 2; expected TYPE 1 or TASK Agent 2.'
      )
    );
  });

  it('does not synthesize TASK eligibility for Agent 0 when TASK is absent from its allowlist', async () => {
    process.env.CHIRALITY_INSTRUCTION_ROOT = await createInstructionRootFixture({
      personaContent: `---
description: current-shaped Agent 0
subagents: PROJECT_SETUP
---
# AGENT HELP_HUMAN
AGENT_TYPE: 0
`,
      additionalAgents: [
        {
          name: 'PROJECT_SETUP',
          content: `---
description: manager
---
# AGENT PROJECT_SETUP
AGENT_TYPE: 1
`
        },
        {
          name: 'TASK',
          content: `---
description: task
---
# AGENT TASK
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | TASK |
`
        }
      ]
    });

    const result = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      validGovernance,
      withSubagentEnv('true')
    );

    expect(result).toMatchObject({
      allowed: true,
      allowlistedSubagents: ['PROJECT_SETUP'],
      delegatedSubagents: ['PROJECT_SETUP']
    });
    expect(result.delegatedAgentInstructions).not.toHaveProperty('TASK');
  });

  it('warns but allows TYPE 2 subagents that are not TASK class', async () => {
    process.env.CHIRALITY_INSTRUCTION_ROOT = await createInstructionRootFixture({
      personaContent: `---
description: test persona
subagents:
  - ALPHA
---
# AGENT WORKING_ITEMS
AGENT_TYPE: 1
`,
      additionalAgents: [
        {
          name: 'ALPHA',
          content: `---
description: alpha
---
# AGENT ALPHA
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | PERSONA |
`
        }
      ]
    });
    const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

    const result = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      validGovernance,
      withSubagentEnv('true')
    );

    expect(result).toMatchObject({
      allowed: true,
      gate: 'ALLOW',
      delegatedSubagents: ['ALPHA']
    });
    expect(warnSpy).toHaveBeenCalledWith(
      expect.stringContaining(
        'Candidate subagent warning: ALPHA declares AGENT_CLASS=PERSONA; TASK is preferred.'
      )
    );
  });

  it('records evaluation duration and emits slow-evaluation warnings when threshold is exceeded', async () => {
    process.env.CHIRALITY_INSTRUCTION_ROOT = await createInstructionRootFixture({
      personaContent: `---
description: test persona
subagents:
  - TASK
---
# AGENT WORKING_ITEMS
AGENT_TYPE: 1
`,
      additionalAgents: [
        {
          name: 'TASK',
          content: `---
description: task
---
# AGENT TASK
AGENT_TYPE: 2

| Property | Value |
|---|---|
| **AGENT_CLASS** | TASK |
`
        }
      ]
    });
    const infoSpy = vi.spyOn(console, 'info').mockImplementation(() => {});
    const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const hrtimeSpy = vi.spyOn(process.hrtime, 'bigint');
    hrtimeSpy.mockReturnValueOnce(1_000_000n);
    hrtimeSpy.mockReturnValueOnce(12_500_000n);

    const result = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      validGovernance,
      {
        ...withSubagentEnv('true'),
        CHIRALITY_SUBAGENT_GOVERNANCE_WARN_MS: '5'
      }
    );

    expect(result.allowed).toBe(true);
    expect(result.evaluationMs).toBeCloseTo(11.5, 3);
    expect(infoSpy).toHaveBeenCalled();
    expect(warnSpy).toHaveBeenCalledWith(
      expect.stringContaining('SLOW_EVALUATION persona=WORKING_ITEMS')
    );
  });

  it('fails closed on instruction-root errors', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-subagent-governance-bad-root-'));
    process.env.CHIRALITY_INSTRUCTION_ROOT = path.join(tmpDir, 'missing-root');
    const infoSpy = vi.spyOn(console, 'info').mockImplementation(() => {});
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    const result = await evaluateSubagentGovernance(
      'WORKING_ITEMS',
      validGovernance,
      withSubagentEnv('true')
    );

    expect(result).toMatchObject({
      allowed: false,
      gate: 'INTERNAL_ERROR'
    });
    expect(result.evaluationMs).toBeGreaterThanOrEqual(0);
    expect(errorSpy).toHaveBeenCalledWith(
      expect.stringContaining(
        '[harness/subagent-governance] INTERNAL_ERROR persona=WORKING_ITEMS gate=INTERNAL_ERROR'
      )
    );
    expect(infoSpy).toHaveBeenCalled();
  });
});
