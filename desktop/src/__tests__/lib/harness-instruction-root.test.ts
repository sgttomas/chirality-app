import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import {
  assertInstructionRootReadable,
  instructionRootContainsPath,
  resolveInstructionRootPath
} from '../../lib/harness/instruction-root';

let tmpRoot = '';
let instructionRoot = '';

async function writeInstructionRootFixture(root: string): Promise<void> {
  const agentsDir = path.join(root, 'agents');
  const docsDir = path.join(root, 'docs');
  await mkdir(agentsDir, { recursive: true });
  await mkdir(docsDir, { recursive: true });

  await writeFile(path.join(root, 'AGENTS.md'), '# agents index\n', 'utf8');
  await writeFile(path.join(root, 'README.md'), '# instruction root\n', 'utf8');
  await writeFile(path.join(agentsDir, 'AGENT_WORKING_ITEMS.md'), '# persona fixture\n', 'utf8');
  await writeFile(path.join(docsDir, 'DIRECTIVE.md'), '# directive\n', 'utf8');
  await writeFile(path.join(docsDir, 'CONTRACT.md'), '# contract\n', 'utf8');
  await writeFile(path.join(docsDir, 'SPEC.md'), '# spec\n', 'utf8');
  await writeFile(path.join(docsDir, 'TYPES.md'), '# types\n', 'utf8');
  await writeFile(path.join(docsDir, 'PLAN.md'), '# plan\n', 'utf8');
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-instruction-root-'));
  instructionRoot = path.join(tmpRoot, 'instruction-root');
  await writeInstructionRootFixture(instructionRoot);
  process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;
});

afterEach(async () => {
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  if (tmpRoot) {
    await rm(tmpRoot, { recursive: true, force: true });
  }
  tmpRoot = '';
  instructionRoot = '';
});

describe('instruction-root helpers', () => {
  it('resolves and validates configured instruction root paths', async () => {
    expect(resolveInstructionRootPath()).toBe(path.resolve(instructionRoot));
    await expect(assertInstructionRootReadable()).resolves.toBe(path.resolve(instructionRoot));
  });

  it('reports missing required resources with typed failure details', async () => {
    await rm(path.join(instructionRoot, 'docs', 'PLAN.md'));

    await expect(assertInstructionRootReadable()).rejects.toMatchObject({
      type: 'INSTRUCTION_ROOT_INVALID',
      details: expect.objectContaining({
        instructionRoot: path.resolve(instructionRoot),
        missingEntries: expect.arrayContaining(['docs/PLAN.md'])
      })
    });
  });

  it('detects whether a path overlaps instruction root', () => {
    const nested = path.join(instructionRoot, 'execution', 'PKG-01');
    const sibling = path.join(tmpRoot, 'outside-root');

    expect(instructionRootContainsPath(instructionRoot, instructionRoot)).toBe(true);
    expect(instructionRootContainsPath(nested, instructionRoot)).toBe(true);
    expect(instructionRootContainsPath(sibling, instructionRoot)).toBe(false);
  });
});
