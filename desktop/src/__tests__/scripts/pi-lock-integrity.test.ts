import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

import {
  PI_ROOT,
  PI_SIBLING_PACKAGES,
  PI_VERSION,
  normalizePiLockIntegrity
} from '../../../scripts/normalize-pi-lock-integrity.mjs';

const registryEntry = (packageName: string, integrity?: string) => ({
  version: PI_VERSION,
  resolved: `https://registry.npmjs.org/${packageName}/-/${packageName.split('/')[1]}-${PI_VERSION}.tgz`,
  ...(integrity ? { integrity } : {})
});

describe('Pi lock integrity normalization', () => {
  it('copies verified root SHA-512 values to identical nested Pi artifacts', () => {
    const packages: Record<string, ReturnType<typeof registryEntry>> = {};
    for (const [index, packageName] of PI_SIBLING_PACKAGES.entries()) {
      const integrity = `sha512-root-${index}`;
      packages[`node_modules/${packageName}`] = registryEntry(packageName, integrity);
      packages[`${PI_ROOT}/node_modules/${packageName}`] = registryEntry(packageName);
    }
    const lock = { packages };

    expect(normalizePiLockIntegrity(lock)).toEqual(
      PI_SIBLING_PACKAGES.map((packageName) => `${PI_ROOT}/node_modules/${packageName}`)
    );
    for (const packageName of PI_SIBLING_PACKAGES) {
      expect(packages[`${PI_ROOT}/node_modules/${packageName}`].integrity).toBe(
        packages[`node_modules/${packageName}`].integrity
      );
    }
  });

  it('refuses conflicting nested artifacts', () => {
    const packages: Record<string, ReturnType<typeof registryEntry>> = {};
    for (const packageName of PI_SIBLING_PACKAGES) {
      packages[`node_modules/${packageName}`] = registryEntry(packageName, 'sha512-root');
      packages[`${PI_ROOT}/node_modules/${packageName}`] = registryEntry(
        packageName,
        'sha512-conflict'
      );
    }

    expect(() => normalizePiLockIntegrity({ packages })).toThrow(/conflicts/);
  });

  it('keeps every committed Pi closure artifact under SHA-512 enforcement', async () => {
    const lock = JSON.parse(
      await readFile(path.resolve(process.cwd(), 'package-lock.json'), 'utf8')
    ) as {
      packages: Record<string, { integrity?: string; resolved?: string }>;
    };
    const closure = Object.entries(lock.packages).filter(
      ([name, entry]) =>
        (name === PI_ROOT || name.startsWith(`${PI_ROOT}/node_modules/`)) &&
        typeof entry.resolved === 'string'
    );

    expect(closure.length).toBeGreaterThan(3);
    for (const [, entry] of closure) {
      expect(entry.integrity).toMatch(/^sha512-/);
    }
  });
});
