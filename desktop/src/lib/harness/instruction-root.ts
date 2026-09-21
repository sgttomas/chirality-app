import { constants as fsConstants, existsSync } from 'node:fs';
import { access, stat } from 'node:fs/promises';
import path from 'node:path';
import { HarnessError } from '@chirality/runtime-contracts/errors';

const REQUIRED_FILE_ENTRIES = [
  'AGENTS.md',
  'README.md',
  path.join('docs', 'DIRECTIVE.md'),
  path.join('docs', 'CONTRACT.md'),
  path.join('docs', 'SPEC.md'),
  path.join('docs', 'TYPES.md'),
  path.join('docs', 'PLAN.md')
] as const;

const REQUIRED_DIRECTORY_ENTRIES = ['agents', 'docs'] as const;

function resolveInstructionRootFromEnv(): string | undefined {
  const override = process.env.CHIRALITY_INSTRUCTION_ROOT?.trim();
  if (!override) {
    return undefined;
  }
  return path.resolve(override);
}

function hasRequiredInstructionRootEntries(candidateRoot: string): boolean {
  return (
    REQUIRED_DIRECTORY_ENTRIES.every((entry) => existsSync(path.join(candidateRoot, entry))) &&
    REQUIRED_FILE_ENTRIES.every((entry) => existsSync(path.join(candidateRoot, entry)))
  );
}

function resolveInstructionRootFromWorkspace(): string {
  const candidates = [
    path.resolve(process.cwd(), '..'),
    path.resolve(process.cwd(), '..', '..', '..')
  ];

  return candidates.find(hasRequiredInstructionRootEntries) ?? candidates[0];
}

export function resolveInstructionRootPath(): string {
  return resolveInstructionRootFromEnv() ?? resolveInstructionRootFromWorkspace();
}

export function instructionRootContainsPath(
  targetPath: string,
  instructionRoot = resolveInstructionRootPath()
): boolean {
  const normalizedRoot = path.resolve(instructionRoot);
  const normalizedTarget = path.resolve(targetPath);
  const relative = path.relative(normalizedRoot, normalizedTarget);
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

export async function assertInstructionRootReadable(): Promise<string> {
  const instructionRoot = resolveInstructionRootPath();
  const missingEntries: string[] = [];
  const invalidEntries: string[] = [];

  for (const relativeEntry of REQUIRED_DIRECTORY_ENTRIES) {
    const absoluteEntry = path.join(instructionRoot, relativeEntry);
    try {
      const entryStat = await stat(absoluteEntry);
      if (!entryStat.isDirectory()) {
        invalidEntries.push(relativeEntry);
        continue;
      }
      await access(absoluteEntry, fsConstants.R_OK | fsConstants.X_OK);
    } catch {
      missingEntries.push(relativeEntry);
    }
  }

  for (const relativeEntry of REQUIRED_FILE_ENTRIES) {
    const absoluteEntry = path.join(instructionRoot, relativeEntry);
    try {
      const entryStat = await stat(absoluteEntry);
      if (!entryStat.isFile()) {
        invalidEntries.push(relativeEntry);
        continue;
      }
      await access(absoluteEntry, fsConstants.R_OK);
    } catch {
      missingEntries.push(relativeEntry);
    }
  }

  if (missingEntries.length > 0 || invalidEntries.length > 0) {
    throw new HarnessError(
      'INSTRUCTION_ROOT_INVALID',
      500,
      'Instruction root is missing required resources',
      {
        instructionRoot,
        missingEntries,
        invalidEntries
      }
    );
  }

  return instructionRoot;
}
