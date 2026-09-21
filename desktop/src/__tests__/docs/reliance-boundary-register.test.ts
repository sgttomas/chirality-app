import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

const REGISTER_PATH = path.resolve(
  process.cwd(),
  '..',
  'docs',
  'harness',
  'reliance_boundary_register.md'
);

describe('reliance boundary register', () => {
  // The schema-field, boundary-inventory, Section 9 index, apply-behavior,
  // and governance-citation substring pins ("retains the governed schema,
  // boundary inventory, and implemented Section 9 index") moved to the
  // consolidated src/__tests__/contract-pins.manifest.ts (checked by
  // contract-pins.test.ts). This file keeps the structural assertions.

  it('keeps every cited frontend enforcement-surface path inspectable', async () => {
    const register = await readFile(REGISTER_PATH, 'utf8');
    const citedPaths = [...register.matchAll(/`(frontend\/(?:src|packages|scripts|docs)\/[^`*]+)`/g)]
      .map((match) => match[1].replace(/\s+uses\s+.*$/, ''));

    expect(citedPaths.length).toBeGreaterThan(0);
    await Promise.all(
      [...new Set(citedPaths)].map((citedPath) =>
        access(path.resolve(process.cwd(), '..', citedPath))
      )
    );
  });

  it('does not present retired PEC v0.4 adapter evidence as current PEC v2 enforcement', async () => {
    const register = await readFile(REGISTER_PATH, 'utf8');
    const pecRow = register
      .split('\n')
      .find((line) => line.startsWith('| RB-PEC-ADAPTER |'));

    expect(pecRow).toBeDefined();
    expect(pecRow).toContain('RETIRED current-evidence row');
    expect(pecRow).toContain('No current App-owned PEC v2 adapter enforcement is asserted');
    expect(pecRow).toContain('`UNKNOWN`');
    expect(pecRow).not.toContain('PEC adapter RBAC, human-only act exclusion, scratch/demo fence');
    // The register-level D-GOV-20 and PEC PRD citation pins moved to the
    // consolidated src/__tests__/contract-pins.manifest.ts.
  });
});
