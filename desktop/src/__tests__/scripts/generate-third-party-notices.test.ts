import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';

import {
  REQUIRED_FIRST_PARTY_LINKS,
  REQUIRED_NOTICE_PACKAGES,
  assertRequiredPackages,
  computeProductionClosure,
  excerptLicenseText,
  generateNotices,
  groupThirdParty,
  packageNameFromKey,
  parseArgs,
  resolveDependencyKey,
  selectLicenseFile
} from '../../../scripts/generate-third-party-notices.mjs';

type LockEntry = Record<string, unknown>;

function fixtureLock(): { lockfileVersion: number; packages: Record<string, LockEntry> } {
  return {
    lockfileVersion: 3,
    packages: {
      '': {
        name: 'fixture-app',
        version: '1.0.0',
        dependencies: {
          '@chirality/runtime-core': 'file:../runtime/core',
          zeta: '1.0.0',
          alpha: '2.0.0',
          nolicense: '1.0.0',
          undeclared: '1.0.0'
        },
        optionalDependencies: { 'optional-native': '1.0.0' },
        devDependencies: { 'dev-only': '1.0.0' }
      },
      'node_modules/@chirality/runtime-core': { resolved: '../runtime/core', link: true },
      '../runtime/core': {
        name: '@chirality/runtime-core',
        version: '0.1.0',
        dependencies: { 'core-dep': '1.0.0' }
      },
      'node_modules/core-dep': { version: '1.0.0', license: 'ISC', resolved: 'https://registry/core-dep-1.0.0.tgz' },
      'node_modules/zeta': {
        version: '1.0.0',
        license: 'MIT',
        resolved: 'https://registry/zeta-1.0.0.tgz',
        dependencies: { shared: '1.0.0' },
        peerDependencies: { 'peer-missing': '*' }
      },
      'node_modules/alpha': {
        version: '2.0.0',
        license: 'Apache-2.0',
        dependencies: { shared: '2.0.0' }
      },
      'node_modules/shared': { version: '1.0.0', license: 'MIT' },
      'node_modules/alpha/node_modules/shared': { version: '2.0.0', license: 'MIT' },
      'node_modules/optional-native': { version: '1.0.0', license: 'BSD-2-Clause', optional: true, os: ['linux'], cpu: ['x64'] },
      'node_modules/dev-only': { version: '1.0.0', license: 'MIT', dev: true },
      'node_modules/nolicense': { version: '1.0.0' },
      'node_modules/undeclared': { version: '1.0.0' }
    }
  };
}

const tempDirectories: string[] = [];

afterEach(async () => {
  await Promise.all(tempDirectories.splice(0).map((directory) => rm(directory, { recursive: true, force: true })));
});

describe('generate-third-party-notices closure logic', () => {
  it('derives package names from nested lock keys and link targets', () => {
    expect(packageNameFromKey('node_modules/alpha', {})).toBe('alpha');
    expect(packageNameFromKey('node_modules/alpha/node_modules/@scope/beta', {})).toBe('@scope/beta');
    expect(packageNameFromKey('../runtime/core', { name: '@chirality/runtime-core' })).toBe('@chirality/runtime-core');
    expect(() => packageNameFromKey('../runtime/core', {})).toThrow(/Unable to derive/);
  });

  it('resolves dependencies with npm nesting semantics', () => {
    const { packages } = fixtureLock();
    expect(resolveDependencyKey(packages, '', 'zeta')).toBe('node_modules/zeta');
    expect(resolveDependencyKey(packages, 'node_modules/alpha', 'shared')).toBe('node_modules/alpha/node_modules/shared');
    expect(resolveDependencyKey(packages, 'node_modules/zeta', 'shared')).toBe('node_modules/shared');
    expect(resolveDependencyKey(packages, '../runtime/core', 'core-dep')).toBe('node_modules/core-dep');
    expect(resolveDependencyKey(packages, '', 'absent')).toBeNull();
  });

  it('walks the production closure through links, excludes dev-only packages, and orders deterministically', () => {
    const closure = computeProductionClosure(fixtureLock());
    const keys = closure.entries.map((entry) => entry.key);
    expect(keys).toEqual([
      'node_modules/@chirality/runtime-core',
      '../runtime/core',
      'node_modules/alpha',
      'node_modules/core-dep',
      'node_modules/nolicense',
      'node_modules/optional-native',
      'node_modules/shared',
      'node_modules/alpha/node_modules/shared',
      'node_modules/undeclared',
      'node_modules/zeta'
    ]);
    expect(keys).not.toContain('node_modules/dev-only');
    const firstParty = closure.entries.filter((entry) => entry.firstParty).map((entry) => entry.key);
    expect(firstParty).toEqual(['node_modules/@chirality/runtime-core', '../runtime/core']);
    expect(closure.entries.find((entry) => entry.key === '../runtime/core')?.linkTargetOf).toEqual([
      'node_modules/@chirality/runtime-core'
    ]);
    expect(closure.unresolvedOptional).toEqual(['node_modules/zeta -> peer-missing']);
    const optional = closure.entries.find((entry) => entry.key === 'node_modules/optional-native');
    expect(optional?.optional).toBe(true);
    expect(optional?.os).toEqual(['linux']);
  });

  it('refuses non-v3 lockfiles, dev-flagged reachability, and unresolvable required dependencies', () => {
    expect(() => computeProductionClosure({ lockfileVersion: 2, packages: { '': {} } })).toThrow(/lockfileVersion 3/);
    const devReach = fixtureLock();
    devReach.packages['node_modules/zeta'].dependencies = { 'dev-only': '1.0.0' };
    expect(() => computeProductionClosure(devReach)).toThrow(/flagged dev-only/);
    const missing = fixtureLock();
    delete missing.packages['node_modules/core-dep'];
    expect(() => computeProductionClosure(missing)).toThrow(/not resolvable/);
    const badLink = fixtureLock();
    badLink.packages['node_modules/@chirality/runtime-core'] = { resolved: '../nowhere', link: true };
    expect(() => computeProductionClosure(badLink)).toThrow(/unknown lock key/);
  });

  it('groups distinct name@version records with sorted install paths', () => {
    const closure = computeProductionClosure(fixtureLock());
    const groups = groupThirdParty(closure.entries);
    expect(groups.map((group) => group.id)).toEqual([
      'alpha@2.0.0',
      'core-dep@1.0.0',
      'nolicense@1.0.0',
      'optional-native@1.0.0',
      'shared@1.0.0',
      'shared@2.0.0',
      'undeclared@1.0.0',
      'zeta@1.0.0'
    ]);
    expect(groups.every((group) => !group.id.startsWith('@chirality/'))).toBe(true);
  });

  it('asserts required packages and reports which are missing', () => {
    const closure = computeProductionClosure(fixtureLock());
    expect(assertRequiredPackages(closure, ['@chirality/runtime-core', 'zeta'])).toEqual([
      { name: '@chirality/runtime-core', version: '0.1.0', key: '../runtime/core' },
      { name: 'zeta', version: '1.0.0', key: 'node_modules/zeta' }
    ]);
    expect(() => assertRequiredPackages(closure, ['@earendil-works/pi-ai'])).toThrow(/missing from the production closure: @earendil-works\/pi-ai/);
  });

  it('defaults the required set to the Pi notice packages plus the runtime file dependencies', () => {
    const options = parseArgs([]);
    for (const name of [...REQUIRED_NOTICE_PACKAGES, ...REQUIRED_FIRST_PARTY_LINKS]) {
      expect(options.require).toContain(name);
    }
    expect(REQUIRED_NOTICE_PACKAGES).toEqual([
      '@earendil-works/pi-agent-core',
      '@earendil-works/pi-ai',
      '@earendil-works/pi-coding-agent',
      '@earendil-works/pi-tui'
    ]);
    expect(() => parseArgs(['--excerpt-lines', '0'])).toThrow(/positive integer/);
    expect(() => parseArgs(['--unknown'])).toThrow(/Unknown option/);
  });
});

describe('generate-third-party-notices license text handling', () => {
  it('selects license files case-insensitively and deterministically', () => {
    expect(selectLicenseFile(['README.md', 'license', 'LICENSE.md'])).toBe('LICENSE.md');
    expect(selectLicenseFile(['COPYING', 'LICENCE.txt'])).toBe('COPYING');
    expect(selectLicenseFile(['index.js'])).toBeNull();
  });

  it('excerpts and normalises license text without changing its identity', () => {
    const result = excerptLicenseText('MIT License\r\n\r\nCopyright (c) 2025 Example\r\n\r\nPermission granted.\r\n\r\n', 3);
    expect(result.excerpt).toBe('MIT License\n\nCopyright (c) 2025 Example');
    expect(result.truncated).toBe(true);
    expect(result.lineCount).toBe(5);
  });
});

describe('generate-third-party-notices end to end on a fixture tree', () => {
  async function writeFixtureTree(): Promise<string> {
    const root = await mkdtemp(path.join(tmpdir(), 'chirality-notices-test-'));
    tempDirectories.push(root);
    const lock = fixtureLock();
    await writeFile(path.join(root, 'package.json'), JSON.stringify({ name: 'fixture-app', version: '1.0.0' }));
    await writeFile(path.join(root, 'package-lock.json'), JSON.stringify(lock));
    const installs: Array<[string, string | null]> = [
      ['node_modules/zeta', 'MIT License\n\nCopyright (c) 2025 Zeta Authors\n'],
      ['node_modules/alpha', 'Apache License\nVersion 2.0, January 2004\n'],
      ['node_modules/shared', 'MIT License\n'],
      ['node_modules/alpha/node_modules/shared', 'MIT License\n'],
      ['node_modules/core-dep', null],
      ['node_modules/nolicense', 'BSD text\n'],
      ['node_modules/undeclared', null]
    ];
    for (const [key, license] of installs) {
      await mkdir(path.join(root, key), { recursive: true });
      const manifest: Record<string, unknown> = { name: path.basename(key) };
      if (key === 'node_modules/nolicense') {
        manifest.license = { type: 'BSD-3-Clause' };
      }
      await writeFile(path.join(root, key, 'package.json'), JSON.stringify(manifest));
      if (license !== null) {
        await writeFile(path.join(root, key, 'LICENSE'), license);
      }
    }
    return root;
  }

  it('produces byte-identical output across runs and records license identities', async () => {
    const root = await writeFixtureTree();
    const first = path.join(root, 'out', 'first.md');
    const second = path.join(root, 'out', 'second.md');
    const options = { ...parseArgs(['--root', root, '--output', first, '--summary', path.join(root, 'out', 'summary.json')]), require: ['zeta', '@chirality/runtime-core'] };
    const summary = await generateNotices(options);
    await generateNotices({ ...options, output: second, summary: null });
    const firstBytes = await readFile(first, 'utf8');
    expect(firstBytes).toBe(await readFile(second, 'utf8'));
    expect(summary.thirdPartyDistinctCount).toBe(8);
    expect(summary.firstPartyCount).toBe(2);
    expect(summary.missingLicenseFile).toEqual(['core-dep@1.0.0', 'undeclared@1.0.0']);
    expect(summary.optionalNotInstalled).toEqual(['optional-native@1.0.0']);
    expect(summary.licenseCounts).toEqual({
      'Apache-2.0': 1,
      'BSD-2-Clause': 1,
      'BSD-3-Clause': 1,
      ISC: 1,
      MIT: 3,
      UNDECLARED: 1
    });
    expect(firstBytes).toContain('### `nolicense@1.0.0`\n\n- Declared license: `BSD-3-Clause`');
    expect(firstBytes).toContain('### `undeclared@1.0.0`\n\n- Declared license: `UNDECLARED`');
    expect(summary.output.sha256).toMatch(/^[0-9a-f]{64}$/);
    expect(firstBytes).toContain('### `zeta@1.0.0`');
    expect(firstBytes).toContain('Copyright (c) 2025 Zeta Authors');
    expect(firstBytes).toContain('- License file: NOT PRESENT in the installed package');
    expect(firstBytes).toContain('OPTIONAL PACKAGE NOT INSTALLED ON THIS HOST');
    expect(firstBytes).toContain('- Packages with no license file in the installed tarball (declared license only): 2 —');
    expect(firstBytes).toContain(
      '- Platform-conditional optional packages present in the lockfile closure but not installed on the generating host (declared license only): 1'
    );
    expect(firstBytes.indexOf('declared license only): 2')).toBeLessThan(firstBytes.indexOf('## First-party'));
    expect(firstBytes).toContain('| `@chirality/runtime-core` | `0.1.0` | `../runtime/core` | link target |');
    expect(firstBytes.indexOf('### `alpha@2.0.0`')).toBeLessThan(firstBytes.indexOf('### `zeta@1.0.0`'));
    expect(firstBytes).not.toContain('dev-only');
    expect(firstBytes).not.toMatch(/\d{4}-\d{2}-\d{2}T/);
  });

  it('fails closed when a required package is absent from the closure', async () => {
    const root = await writeFixtureTree();
    const options = { ...parseArgs(['--root', root, '--output', path.join(root, 'out', 'n.md')]), require: ['@earendil-works/pi-tui'] };
    await expect(generateNotices(options)).rejects.toThrow(/@earendil-works\/pi-tui/);
  });
});
