import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';

import {
  DEFAULT_ARTIFACT_NAME_TEMPLATE,
  EXPECTED_APP_ID,
  EXPECTED_PRODUCT_NAME,
  STATUS,
  assertIdentity,
  buildStagedPatch,
  buildUnifiedDiff,
  collectIdentitySurfaces,
  evaluateSurfaces,
  expectedDmgFilename,
  parseArgs,
  readPlistStrings,
  renderReport,
  resolveArtifactName,
  runCli,
  stageVersionLines,
  verifyVersionIdentity
} from '../../../scripts/verify-version-identity.mjs';

const PACKAGE_JSON_TEXT = `{
  "name": "fixture-app",
  "version": "2.0.0",
  "private": true,
  "build": {
    "appId": "com.chirality.app",
    "productName": "Chirality",
    "mac": {
      "target": [{ "target": "dmg", "arch": ["arm64"] }]
    }
  }
}
`;

const PACKAGE_LOCK_TEXT = `{
  "name": "fixture-app",
  "version": "2.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "fixture-app",
      "version": "2.0.0",
      "dependencies": {}
    }
  }
}
`;

const tempDirectories: string[] = [];

afterEach(async () => {
  await Promise.all(tempDirectories.splice(0).map((directory) => rm(directory, { recursive: true, force: true })));
});

async function makeFrontendRoot(): Promise<string> {
  const root = await mkdtemp(path.join(tmpdir(), 'chirality-version-identity-'));
  tempDirectories.push(root);
  await writeFile(path.join(root, 'package.json'), PACKAGE_JSON_TEXT);
  await writeFile(path.join(root, 'package-lock.json'), PACKAGE_LOCK_TEXT);
  return root;
}

describe('verify-version-identity pure helpers', () => {
  it('accepts semantic identities and refuses others', () => {
    expect(assertIdentity('3.0.0-rc.1', 'x')).toBe('3.0.0-rc.1');
    expect(assertIdentity('2.0.0', 'x')).toBe('2.0.0');
    expect(() => assertIdentity('v3', 'x')).toThrow(/semantic-version identity/);
    expect(() => assertIdentity(undefined, '--expect')).toThrow(/--expect/);
  });

  it('derives the electron-builder DMG filename from the identity constants', () => {
    expect(DEFAULT_ARTIFACT_NAME_TEMPLATE).toBe('${productName}-${version}-${arch}.${ext}');
    expect(expectedDmgFilename(EXPECTED_PRODUCT_NAME, '3.0.0-rc.1')).toBe('Chirality-3.0.0-rc.1-arm64.dmg');
    expect(resolveArtifactName('${productName}_${version}.${ext}', { productName: 'X', version: '1.2.3', arch: 'arm64', ext: 'dmg' })).toBe('X_1.2.3.dmg');
    expect(EXPECTED_APP_ID).toBe('com.chirality.app');
  });

  it('reads identity keys from an XML property list', () => {
    const xml = `<?xml version="1.0"?><plist version="1.0"><dict>
      <key>CFBundleIdentifier</key><string>com.chirality.app</string>
      <key>CFBundleShortVersionString</key>
      <string>3.0.0-rc.1</string>
      <key>CFBundleVersion</key><string>3.0.0-rc.1</string>
    </dict></plist>`;
    expect(readPlistStrings(xml, ['CFBundleIdentifier', 'CFBundleShortVersionString', 'CFBundleVersion', 'CFBundleName'])).toEqual({
      CFBundleIdentifier: 'com.chirality.app',
      CFBundleShortVersionString: '3.0.0-rc.1',
      CFBundleVersion: '3.0.0-rc.1',
      CFBundleName: null
    });
  });
});

describe('verify-version-identity surface collection', () => {
  const packageJson = JSON.parse(PACKAGE_JSON_TEXT) as object;
  const packageLock = JSON.parse(PACKAGE_LOCK_TEXT) as object;

  it('passes when every declared surface carries the expected identity', () => {
    const surfaces = collectIdentitySurfaces({ expected: '2.0.0', packageJson, packageLock });
    const byId = Object.fromEntries(surfaces.map((item) => [item.id, item]));
    expect(byId['package.json:version']?.status).toBe(STATUS.MATCH);
    expect(byId['package-lock.json:version']?.status).toBe(STATUS.MATCH);
    expect(byId['package-lock.json:packages[""].version']?.status).toBe(STATUS.MATCH);
    expect(byId['package.json:build.productName']?.status).toBe(STATUS.MATCH);
    expect(byId['package.json:build.appId']?.status).toBe(STATUS.MATCH);
    expect(byId['dmg:filename(derived)']?.observed).toBe('Chirality-2.0.0-arm64.dmg');
    expect(byId['dmg:filename(derived)']?.status).toBe(STATUS.MATCH);
    expect(byId['app:bundle-metadata']?.status).toBe(STATUS.DERIVED);
    expect(byId['dmg:file']?.status).toBe(STATUS.NOT_INSPECTED);
    expect(byId['source:version-reporting']?.status).toBe(STATUS.ABSENT);
    expect(byId['scripts:release-manifest-version']?.status).toBe(STATUS.ABSENT);
    const evaluation = evaluateSurfaces(surfaces);
    expect(evaluation.result).toBe('PASS');
    expect(evaluation.mismatchCount).toBe(0);
    expect(evaluateSurfaces(surfaces, { requireAll: true }).result).toBe('MISMATCH');
  });

  it('reports every declared and derived surface that disagrees with 3.0.0-rc.1', () => {
    const surfaces = collectIdentitySurfaces({ expected: '3.0.0-rc.1', packageJson, packageLock });
    const evaluation = evaluateSurfaces(surfaces);
    expect(evaluation.result).toBe('MISMATCH');
    expect(evaluation.mismatches).toEqual([
      'package.json:version',
      'package-lock.json:version',
      'package-lock.json:packages[""].version',
      'dmg:filename(derived)'
    ]);
    const dmg = surfaces.find((item) => item.id === 'dmg:filename(derived)');
    expect(dmg?.expected).toBe('Chirality-3.0.0-rc.1-arm64.dmg');
    const report = renderReport({ expected: '3.0.0-rc.1', frontendRoot: '/x', surfaces, evaluation, stagedPatch: null });
    expect(report).toContain('Result: MISMATCH (4 mismatching surface(s)');
    expect(report).toContain('| MISMATCH |');
    expect(report).toContain('no version byte changed');
  });

  it('inspects staged bundle metadata and DMG names when provided', () => {
    const surfaces = collectIdentitySurfaces({
      expected: '3.0.0-rc.1',
      packageJson: { ...(packageJson as Record<string, unknown>), version: '3.0.0-rc.1' },
      packageLock: null,
      infoPlist: {
        CFBundleShortVersionString: '3.0.0-rc.1',
        CFBundleVersion: '2.0.0',
        CFBundleIdentifier: 'com.chirality.app',
        CFBundleName: 'Chirality'
      },
      dmgBasename: 'Chirality-3.0.0-rc.1-arm64.dmg',
      sourceScan: [{ file: 'electron/about.ts', patternId: 'electron-app-getVersion' }]
    });
    const byId = Object.fromEntries(surfaces.map((item) => [item.id, item]));
    expect(byId['app:CFBundleShortVersionString']?.status).toBe(STATUS.MATCH);
    expect(byId['app:CFBundleVersion']?.status).toBe(STATUS.MISMATCH);
    expect(byId['app:CFBundleIdentifier']?.status).toBe(STATUS.MATCH);
    expect(byId['dmg:file']?.status).toBe(STATUS.MATCH);
    expect(byId['package-lock.json:version']?.status).toBe(STATUS.NOT_INSPECTED);
    expect(byId['source:version-reporting']?.status).toBe(STATUS.PRESENT_UNCHECKED);
    expect(evaluateSurfaces(surfaces).mismatches).toEqual(['app:CFBundleVersion']);
  });

  it('flags a non-default artifact-name template and a wrong product identity', () => {
    const surfaces = collectIdentitySurfaces({
      expected: '2.0.0',
      packageJson: { version: '2.0.0', build: { appId: 'com.example.other', productName: 'Other', artifactName: '${productName}.${ext}' } },
      packageLock: null
    });
    const byId = Object.fromEntries(surfaces.map((item) => [item.id, item]));
    expect(byId['package.json:build.productName']?.status).toBe(STATUS.MISMATCH);
    expect(byId['package.json:build.appId']?.status).toBe(STATUS.MISMATCH);
    expect(byId['electron-builder:artifactName']?.status).toBe(STATUS.MISMATCH);
    expect(byId['dmg:filename(derived)']?.observed).toBe('Other.dmg');
  });
});

describe('verify-version-identity staged patch', () => {
  it('replaces exactly the declared version lines and refuses unexpected counts', () => {
    const staged = stageVersionLines(PACKAGE_JSON_TEXT, { current: '2.0.0', next: '3.0.0-rc.1', indent: 2, occurrences: 1 });
    expect(staged.changed).toEqual([2]);
    expect(staged.text.split('\n')[2]).toBe('  "version": "3.0.0-rc.1",');
    expect(() => stageVersionLines(PACKAGE_JSON_TEXT, { current: '9.9.9', next: '3.0.0-rc.1', indent: 2, occurrences: 1 })).toThrow(/expected 1 line/);
  });

  it('builds a unified diff with context hunks for in-place replacements', () => {
    const before = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', ''].join('\n');
    const after = ['a', 'B', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'K', 'l', ''].join('\n');
    const diff = buildUnifiedDiff('x/file.txt', before, after, 2);
    expect(diff).toBe(
      [
        'diff --git a/x/file.txt b/x/file.txt',
        '--- a/x/file.txt',
        '+++ b/x/file.txt',
        '@@ -1,4 +1,4 @@',
        ' a',
        '-b',
        '+B',
        ' c',
        ' d',
        '@@ -9,4 +9,4 @@',
        ' i',
        ' j',
        '-k',
        '+K',
        ' l',
        ''
      ].join('\n')
    );
    expect(buildUnifiedDiff('x', before, before)).toBe('');
    expect(() => buildUnifiedDiff('x', 'a\nb\n', 'a\n')).toThrow(/in-place/);
  });

  it('stages package.json and both lockfile version lines without touching anything else', () => {
    const patch = buildStagedPatch({
      current: '2.0.0',
      next: '3.0.0-rc.1',
      packageJsonText: PACKAGE_JSON_TEXT,
      packageLockText: PACKAGE_LOCK_TEXT,
      pathPrefix: 'projects/chirality-app-dev/frontend'
    });
    expect(patch).toContain('diff --git a/projects/chirality-app-dev/frontend/package.json b/projects/chirality-app-dev/frontend/package.json');
    expect(patch).toContain('diff --git a/projects/chirality-app-dev/frontend/package-lock.json b/projects/chirality-app-dev/frontend/package-lock.json');
    const removed = patch.split('\n').filter((line) => line.startsWith('-') && !line.startsWith('---'));
    const added = patch.split('\n').filter((line) => line.startsWith('+') && !line.startsWith('+++'));
    expect(removed).toEqual(['-  "version": "2.0.0",', '-  "version": "2.0.0",', '-      "version": "2.0.0",']);
    expect(added).toEqual(['+  "version": "3.0.0-rc.1",', '+  "version": "3.0.0-rc.1",', '+      "version": "3.0.0-rc.1",']);
    expect(() => buildStagedPatch({ current: '2.0.0', next: '2.0.0', packageJsonText: PACKAGE_JSON_TEXT, packageLockText: null, pathPrefix: '' })).toThrow(/equal/);
  });
});

describe('verify-version-identity CLI', () => {
  it('parses arguments and refuses a missing or malformed --expect', () => {
    const parsed = parseArgs(['--expect', '3.0.0-rc.1', '--root', '/tmp/x', '--require-all', '--stage-patch', '/tmp/p.diff']);
    expect(parsed.expect).toBe('3.0.0-rc.1');
    expect(parsed.requireAll).toBe(true);
    expect(parsed.stagePatch).toBe('/tmp/p.diff');
    expect(() => parseArgs([])).toThrow(/--expect/);
    expect(() => parseArgs(['--expect', 'latest'])).toThrow(/semantic-version/);
    expect(() => parseArgs(['--expect', '1.0.0', '--bogus'])).toThrow(/Unknown option/);
  });

  it('exits 0 on the fixture tree for the current identity and 1 with a staged patch for the next one', async () => {
    const root = await makeFrontendRoot();
    const stdoutPass: string[] = [];
    const passCode = await runCli({
      argv: ['--expect', '2.0.0', '--root', root],
      stdout: { write: (text: string) => stdoutPass.push(text) },
      stderr: { write: () => undefined }
    });
    expect(passCode).toBe(0);
    expect(stdoutPass.join('')).toContain('Result: PASS');

    const patchPath = path.join(root, 'evidence', 'staged.diff');
    const jsonPath = path.join(root, 'evidence', 'report.json');
    const stdoutMismatch: string[] = [];
    const mismatchCode = await runCli({
      argv: ['--expect', '3.0.0-rc.1', '--root', root, '--stage-patch', patchPath, '--patch-prefix', 'fixture', '--json', jsonPath],
      stdout: { write: (text: string) => stdoutMismatch.push(text) },
      stderr: { write: () => undefined }
    });
    expect(mismatchCode).toBe(1);
    expect(stdoutMismatch.join('')).toContain('Result: MISMATCH');
    expect(stdoutMismatch.join('')).toContain('NOT applied');
    const patch = await readFile(patchPath, 'utf8');
    expect(patch).toContain('--- a/fixture/package.json');
    expect(patch).toContain('+  "version": "3.0.0-rc.1",');
    expect(await readFile(path.join(root, 'package.json'), 'utf8')).toBe(PACKAGE_JSON_TEXT);
    expect(await readFile(path.join(root, 'package-lock.json'), 'utf8')).toBe(PACKAGE_LOCK_TEXT);
    const report = JSON.parse(await readFile(jsonPath, 'utf8')) as {
      evaluation: { result: string; mismatches: string[] };
      stagedPatch: { applied: boolean; sha256: string };
    };
    expect(report.evaluation.result).toBe('MISMATCH');
    expect(report.evaluation.mismatches).toContain('package.json:version');
    expect(report.stagedPatch.applied).toBe(false);
    expect(report.stagedPatch.sha256).toMatch(/^[0-9a-f]{64}$/);
  });

  it('fails with --require-all when absent or not-inspected surfaces remain', async () => {
    const root = await makeFrontendRoot();
    const stdout: string[] = [];
    const code = await runCli({
      argv: ['--expect', '2.0.0', '--root', root, '--require-all'],
      stdout: { write: (text: string) => stdout.push(text) },
      stderr: { write: () => undefined }
    });
    expect(code).toBe(1);
    expect(stdout.join('')).toContain('Result: MISMATCH (0 mismatching surface(s)');
  });

  it('returns the structured report through the library entry point', async () => {
    const root = await makeFrontendRoot();
    const report = await verifyVersionIdentity(parseArgs(['--expect', '2.0.0', '--root', root]));
    expect(report.schema).toBe('chirality-version-identity-report/v1');
    expect(report.inputs.packageJson.sha256).toMatch(/^[0-9a-f]{64}$/);
    expect(report.stagedPatch).toBeNull();
  });
});
