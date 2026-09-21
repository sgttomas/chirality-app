import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { PersonaComposer } from '../../lib/harness/persona-manager';

let tmpRoot = '';
let projectRoot = '';
let instructionRoot = '';

async function writeInstructionRootFixture(root: string): Promise<void> {
  const agentsDir = path.join(root, 'agents');
  const docsDir = path.join(root, 'docs');
  await mkdir(agentsDir, { recursive: true });
  await mkdir(docsDir, { recursive: true });

  await writeFile(
    path.join(root, 'AGENTS.md'),
    '# Agent Index\n\nGoverned agent matrix fixture.\n',
    'utf8'
  );
  await writeFile(path.join(root, 'README.md'), '# instruction root\n', 'utf8');
  await writeFile(
    path.join(agentsDir, 'AGENT_WORKING_ITEMS.md'),
    `---
description: persona fixture
tools: [read, write, bash]
---
# WORKING_ITEMS

Persona fixture must execute bounded app-integration work.
`,
    'utf8'
  );
  await writeFile(
    path.join(docsDir, 'DIRECTIVE.md'),
    '# DIRECTIVE\n\nAgents propose; humans approve.\n',
    'utf8'
  );
  await writeFile(
    path.join(docsDir, 'CONTRACT.md'),
    '# CONTRACT\n\nInstruction root and working root remain separate.\n',
    'utf8'
  );
  await writeFile(
    path.join(docsDir, 'SPEC.md'),
    '# SPEC\n\nPersona composer builds system prompt from instruction root resources.\n',
    'utf8'
  );
  await writeFile(path.join(docsDir, 'TYPES.md'), '# TYPES\n\nPersonaComposer term.\n', 'utf8');
  await writeFile(path.join(docsDir, 'PLAN.md'), '# PLAN\n\nRuntime stabilization.\n', 'utf8');
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-persona-composer-'));
  projectRoot = path.join(tmpRoot, 'project-root');
  instructionRoot = path.join(tmpRoot, 'instruction-root');
  await mkdir(projectRoot, { recursive: true });
  await writeInstructionRootFixture(instructionRoot);
  process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;
});

afterEach(async () => {
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  if (tmpRoot) {
    await rm(tmpRoot, { recursive: true, force: true });
  }
  tmpRoot = '';
  projectRoot = '';
  instructionRoot = '';
});

describe('PersonaComposer', () => {
  it('composes instruction-root governance, persona content, working root, mode, and tool surface', async () => {
    const composer = new PersonaComposer();

    const prompt = await composer.buildSystemPrompt(projectRoot, 'WORKING_ITEMS', 'workspaceWrite', [
      'read',
      'write',
      'bash'
    ]);

    expect(prompt).toContain('## Chirality Governance Preface');
    expect(prompt).toContain('### AGENTS.md');
    expect(prompt).toContain('Agents propose; humans approve.');
    expect(prompt).toContain('## Active Persona Instruction');
    expect(prompt).toContain('source: agents/AGENT_WORKING_ITEMS.md');
    expect(prompt).toContain('Persona fixture must execute bounded app-integration work.');
    expect(prompt).toContain(`projectRoot: ${path.resolve(projectRoot)}`);
    expect(prompt).toContain('normalizedMode: workspaceWrite');
    expect(prompt).toContain('allowedAdapterTools: Read, Write, Bash');
    expect(prompt).not.toContain('Persona=WORKING_ITEMS;');
  });

  it('keeps content-derived boot fingerprints stable and changes them when persona content changes', async () => {
    const composer = new PersonaComposer();
    await composer.buildSystemPrompt(projectRoot, 'WORKING_ITEMS', 'direct', ['read', 'write']);
    const firstFingerprint = composer.getBootFingerprint('WORKING_ITEMS', 'direct', projectRoot, [
      'read',
      'write'
    ]);

    await composer.buildSystemPrompt(projectRoot, 'WORKING_ITEMS', 'direct', ['read', 'write']);
    const secondFingerprint = composer.getBootFingerprint('WORKING_ITEMS', 'direct', projectRoot, [
      'read',
      'write'
    ]);
    expect(secondFingerprint).toBe(firstFingerprint);
    expect(firstFingerprint).toMatch(/^[a-f0-9]{64}$/);

    await writeFile(
      path.join(instructionRoot, 'agents', 'AGENT_WORKING_ITEMS.md'),
      '# WORKING_ITEMS\n\nChanged persona fixture.\n',
      'utf8'
    );
    await composer.buildSystemPrompt(projectRoot, 'WORKING_ITEMS', 'direct', ['read', 'write']);
    const changedFingerprint = composer.getBootFingerprint('WORKING_ITEMS', 'direct', projectRoot, [
      'read',
      'write'
    ]);
    expect(changedFingerprint).not.toBe(firstFingerprint);
  });

  it('surfaces typed instruction-root failures before composing a prompt', async () => {
    const composer = new PersonaComposer();
    await rm(path.join(instructionRoot, 'docs', 'CONTRACT.md'));

    await expect(
      composer.buildSystemPrompt(projectRoot, 'WORKING_ITEMS', 'direct', ['read'])
    ).rejects.toMatchObject({
      type: 'INSTRUCTION_ROOT_INVALID',
      details: expect.objectContaining({
        instructionRoot: path.resolve(instructionRoot),
        missingEntries: expect.arrayContaining(['docs/CONTRACT.md'])
      })
    });
  });

  it('renders denied tool posture when the current mode does not expose requested tools', async () => {
    const composer = new PersonaComposer();

    const prompt = await composer.buildSystemPrompt(projectRoot, 'WORKING_ITEMS', 'readOnly', [
      'read',
      'write',
      'bash'
    ]);

    expect(prompt).toContain('normalizedMode: readOnly');
    expect(prompt).toContain('allowedAdapterTools: Read');
    expect(prompt).toContain('write -> write_file');
    expect(prompt).toContain('bash -> shell');
    expect(prompt).toContain('disallowedAdapterTools:');
    expect(prompt).toContain('Write');
    expect(prompt).toContain('Bash');
  });
});
