#!/usr/bin/env node
/**
 * verify-version-identity.mjs
 *
 * Enumerates every surface that carries or derives the product version
 * identity and checks each one against an expected identity
 * (`--expect 3.0.0-rc.1`), printing a dry-run report. Optionally emits a
 * staged unified-diff patch (`--stage-patch <file>`) that shows exactly
 * which declared bytes would change to apply the expected identity; the
 * patch is never applied by this script.
 *
 * Surfaces (AT-043 identity set, App carrier DEL-09-05):
 *   declared   package.json version; package-lock.json top-level version;
 *              package-lock.json packages[""].version
 *   constant   electron-builder build.productName and build.appId
 *   derived    electron-builder artifact name template and the resulting
 *              macOS arm64 DMG filename for the current package.json version;
 *              bundle metadata (CFBundleShortVersionString / CFBundleVersion,
 *              which electron-builder derives from package.json) — inspected
 *              directly when --app-path names a staged .app
 *   inspected  --dmg-path filename; --app-path Info.plist
 *   scanned    source-tree version-reporting surfaces (UI/about strings,
 *              runtime reports) and release-manifest fields written by
 *              existing scripts — reported ABSENT when no such surface exists
 *
 * Exit codes: 0 when no surface mismatches; 1 when any surface mismatches
 * (or, with --require-all, when any surface is ABSENT/NOT_INSPECTED);
 * 2 on refused arguments or unreadable inputs.
 *
 * This tool changes no product byte. It performs no signing, notarization,
 * publication, distribution, or release act and makes no release-readiness
 * claim.
 */

import { createHash } from 'node:crypto';
import { existsSync } from 'node:fs';
import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const SCRIPT_DIRECTORY = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_FRONTEND_ROOT = path.resolve(SCRIPT_DIRECTORY, '..');

export const DEFAULT_ARTIFACT_NAME_TEMPLATE = '${productName}-${version}-${arch}.${ext}';
export const EXPECTED_PRODUCT_NAME = 'Chirality';
export const EXPECTED_APP_ID = 'com.chirality.app';
export const RELEASE_ARCH = 'arm64';

export const STATUS = Object.freeze({
  MATCH: 'MATCH',
  MISMATCH: 'MISMATCH',
  DERIVED: 'DERIVED',
  NOT_INSPECTED: 'NOT_INSPECTED',
  ABSENT: 'ABSENT',
  PRESENT_UNCHECKED: 'PRESENT_UNCHECKED'
});

const VERSION_REPORTING_PATTERNS = Object.freeze([
  { id: 'electron-app-getVersion', pattern: /\bapp\.getVersion\s*\(/u },
  { id: 'npm-package-version-env', pattern: /npm_package_version/u },
  { id: 'next-public-app-version', pattern: /NEXT_PUBLIC_APP_VERSION/u },
  { id: 'product-version-token', pattern: /\b(?:productVersion|appVersion|releaseVersion|CHIRALITY_APP_VERSION)\b/u }
]);

const SEMVER_IDENTITY = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/u;

export function sha256Hex(input) {
  return createHash('sha256').update(input).digest('hex');
}

export function assertIdentity(value, label) {
  if (typeof value !== 'string' || !SEMVER_IDENTITY.test(value)) {
    throw new Error(`${label} must be a semantic-version identity such as 3.0.0-rc.1`);
  }
  return value;
}

/** Resolves an electron-builder artifact-name template. */
export function resolveArtifactName(template, { productName, version, arch, ext }) {
  return template
    .replaceAll('${productName}', productName)
    .replaceAll('${version}', version)
    .replaceAll('${arch}', arch)
    .replaceAll('${ext}', ext);
}

export function expectedDmgFilename(productName, version, arch = RELEASE_ARCH) {
  return resolveArtifactName(DEFAULT_ARTIFACT_NAME_TEMPLATE, { productName, version, arch, ext: 'dmg' });
}

/** Reads `<key>string</string>` pairs from an XML property list; sufficient for Info.plist identity keys. */
export function readPlistStrings(xml, keys) {
  const result = {};
  for (const key of keys) {
    const pattern = new RegExp(`<key>${key.replace(/[.*+?^${}()|[\]\\]/gu, '\\$&')}</key>\\s*<string>([^<]*)</string>`, 'u');
    const match = xml.match(pattern);
    result[key] = match ? match[1] : null;
  }
  return result;
}

function surface(id, description, observed, expected, status, note = '') {
  return { id, description, observed, expected, status, note };
}

function compare(id, description, observed, expected, note = '') {
  return surface(
    id,
    description,
    observed,
    expected,
    observed === expected ? STATUS.MATCH : STATUS.MISMATCH,
    note
  );
}

/**
 * Builds the surface list from already-read inputs. Pure: no filesystem access.
 *
 * @param {{ expected: string, packageJson: object, packageLock: object|null,
 *   infoPlist?: object|null, dmgBasename?: string|null,
 *   sourceScan?: Array<{file: string, patternId: string}>, scriptScan?: Array<{file: string, patternId: string}> }} input
 */
export function collectIdentitySurfaces(input) {
  const expected = assertIdentity(input.expected, '--expect');
  const packageJson = input.packageJson ?? {};
  const build = packageJson.build ?? {};
  const productName = typeof build.productName === 'string' ? build.productName : null;
  const declaredVersion = typeof packageJson.version === 'string' ? packageJson.version : null;
  const surfaces = [];

  surfaces.push(compare('package.json:version', 'package.json `version` (declared)', declaredVersion, expected));

  if (input.packageLock) {
    const lock = input.packageLock;
    surfaces.push(
      compare(
        'package-lock.json:version',
        'package-lock.json top-level `version` (declared)',
        typeof lock.version === 'string' ? lock.version : null,
        expected
      )
    );
    const rootEntry = lock.packages && lock.packages[''];
    surfaces.push(
      compare(
        'package-lock.json:packages[""].version',
        'package-lock.json `packages[""].version` (declared)',
        rootEntry && typeof rootEntry.version === 'string' ? rootEntry.version : null,
        expected
      )
    );
  } else {
    surfaces.push(
      surface('package-lock.json:version', 'package-lock.json versions', null, expected, STATUS.NOT_INSPECTED, 'package-lock.json not found')
    );
  }

  surfaces.push(
    compare(
      'package.json:build.productName',
      'electron-builder `build.productName` (identity constant)',
      productName,
      EXPECTED_PRODUCT_NAME
    )
  );
  surfaces.push(
    compare(
      'package.json:build.appId',
      'electron-builder `build.appId` (identity constant)',
      typeof build.appId === 'string' ? build.appId : null,
      EXPECTED_APP_ID
    )
  );

  const template =
    (build.mac && typeof build.mac.artifactName === 'string' && build.mac.artifactName) ||
    (typeof build.artifactName === 'string' && build.artifactName) ||
    DEFAULT_ARTIFACT_NAME_TEMPLATE;
  const templateExplicit = template !== DEFAULT_ARTIFACT_NAME_TEMPLATE || typeof build.artifactName === 'string' || Boolean(build.mac && build.mac.artifactName);
  const expectedDmg = expectedDmgFilename(EXPECTED_PRODUCT_NAME, expected);
  const currentDmg =
    productName && declaredVersion
      ? resolveArtifactName(template, { productName, version: declaredVersion, arch: RELEASE_ARCH, ext: 'dmg' })
      : null;
  surfaces.push(
    surface(
      'electron-builder:artifactName',
      'electron-builder artifact-name template',
      template,
      DEFAULT_ARTIFACT_NAME_TEMPLATE,
      template === DEFAULT_ARTIFACT_NAME_TEMPLATE ? STATUS.MATCH : STATUS.MISMATCH,
      templateExplicit ? 'explicit template in package.json' : 'electron-builder default (no explicit template)'
    )
  );
  surfaces.push(
    compare(
      'dmg:filename(derived)',
      `macOS ${RELEASE_ARCH} DMG filename derived from package.json version`,
      currentDmg,
      expectedDmg,
      'derived: electron-builder names the DMG from productName, version, and arch'
    )
  );

  if (input.infoPlist) {
    const plist = input.infoPlist;
    surfaces.push(
      compare('app:CFBundleShortVersionString', 'staged app Info.plist `CFBundleShortVersionString`', plist.CFBundleShortVersionString ?? null, expected)
    );
    surfaces.push(compare('app:CFBundleVersion', 'staged app Info.plist `CFBundleVersion`', plist.CFBundleVersion ?? null, expected));
    surfaces.push(compare('app:CFBundleIdentifier', 'staged app Info.plist `CFBundleIdentifier`', plist.CFBundleIdentifier ?? null, EXPECTED_APP_ID));
    surfaces.push(compare('app:CFBundleName', 'staged app Info.plist `CFBundleName`', plist.CFBundleName ?? null, EXPECTED_PRODUCT_NAME));
  } else {
    surfaces.push(
      surface(
        'app:bundle-metadata',
        'staged app Info.plist `CFBundleShortVersionString`/`CFBundleVersion` (bundle metadata; `app.getVersion()` source)',
        null,
        expected,
        STATUS.DERIVED,
        'no --app-path given; electron-builder derives both keys from package.json `version`, so this surface follows package.json:version'
      )
    );
  }

  if (typeof input.dmgBasename === 'string') {
    surfaces.push(compare('dmg:file', 'named DMG file basename (--dmg-path)', input.dmgBasename, expectedDmg));
  } else {
    surfaces.push(surface('dmg:file', 'named DMG file basename', null, expectedDmg, STATUS.NOT_INSPECTED, 'no --dmg-path given'));
  }

  const sourceScan = input.sourceScan ?? [];
  surfaces.push(
    sourceScan.length === 0
      ? surface(
          'source:version-reporting',
          'UI/about string or runtime report that prints the product version (electron/**, src/**)',
          'none found',
          expected,
          STATUS.ABSENT,
          'no `app.getVersion()`, `npm_package_version`, `NEXT_PUBLIC_APP_VERSION`, or product-version token in product source; AT-043 UI/runtime surfaces do not yet exist'
        )
      : surface(
          'source:version-reporting',
          'UI/about string or runtime report that prints the product version (electron/**, src/**)',
          sourceScan.map((hit) => `${hit.file} [${hit.patternId}]`).join('; '),
          expected,
          STATUS.PRESENT_UNCHECKED,
          'surface exists; verify its rendered value manually on the staged bytes'
        )
  );

  const scriptScan = input.scriptScan ?? [];
  surfaces.push(
    scriptScan.length === 0
      ? surface(
          'scripts:release-manifest-version',
          'release-manifest / proof-summary version field written by existing scripts (scripts/**)',
          'none found',
          expected,
          STATUS.ABSENT,
          'existing summaries carry digests, source revisions, and posture only; no script writes the product version'
        )
      : surface(
          'scripts:release-manifest-version',
          'release-manifest / proof-summary version field written by existing scripts (scripts/**)',
          scriptScan.map((hit) => `${hit.file} [${hit.patternId}]`).join('; '),
          expected,
          STATUS.PRESENT_UNCHECKED,
          'surface exists; verify the emitted value on a real run'
        )
  );

  return surfaces;
}

export function evaluateSurfaces(surfaces, { requireAll = false } = {}) {
  const mismatches = surfaces.filter((item) => item.status === STATUS.MISMATCH);
  const incomplete = surfaces.filter(
    (item) => item.status === STATUS.ABSENT || item.status === STATUS.NOT_INSPECTED || item.status === STATUS.PRESENT_UNCHECKED
  );
  const pass = mismatches.length === 0 && (!requireAll || incomplete.length === 0);
  return {
    result: pass ? 'PASS' : 'MISMATCH',
    mismatchCount: mismatches.length,
    incompleteCount: incomplete.length,
    mismatches: mismatches.map((item) => item.id),
    incomplete: incomplete.map((item) => item.id)
  };
}

export function renderReport({ expected, frontendRoot, surfaces, evaluation, stagedPatch }) {
  const lines = [];
  lines.push('Version identity dry-run report');
  lines.push(`expected identity : ${expected}`);
  lines.push(`frontend root     : ${frontendRoot}`);
  lines.push('mode              : dry-run (no product byte changed)');
  lines.push('');
  lines.push('| # | surface | observed | expected | status | note |');
  lines.push('|---|---|---|---|---|---|');
  surfaces.forEach((item, index) => {
    const cell = (value) => (value === null || value === undefined ? '—' : String(value).replaceAll('|', '\\|'));
    lines.push(
      `| ${index + 1} | ${cell(item.description)} | ${cell(item.observed)} | ${cell(item.expected)} | ${item.status} | ${cell(item.note)} |`
    );
  });
  lines.push('');
  lines.push(
    `Result: ${evaluation.result} (${evaluation.mismatchCount} mismatching surface(s); ${evaluation.incompleteCount} absent/not-inspected/unchecked surface(s))`
  );
  if (stagedPatch) {
    lines.push(`Staged patch: ${stagedPatch.path} (${stagedPatch.bytes} bytes, SHA-256 ${stagedPatch.sha256}); NOT applied`);
  }
  lines.push('Boundary: evidence only; no version byte changed; no signing, notarization, publication, distribution, or release act.');
  return `${lines.join('\n')}\n`;
}

/** Replaces exact `"version": "<current>"` lines at the given indentation; returns the edited text and changed line indices. */
export function stageVersionLines(text, { current, next, indent, occurrences }) {
  const lines = text.split('\n');
  const needle = `${' '.repeat(indent)}"version": "${current}",`;
  const replacement = `${' '.repeat(indent)}"version": "${next}",`;
  const changed = [];
  for (let index = 0; index < lines.length && changed.length < occurrences; index += 1) {
    if (lines[index] === needle) {
      lines[index] = replacement;
      changed.push(index);
    }
  }
  if (changed.length !== occurrences) {
    throw new Error(
      `expected ${occurrences} line(s) equal to ${JSON.stringify(needle)} but found ${changed.length}`
    );
  }
  return { text: lines.join('\n'), changed };
}

/** Builds a unified diff for equal-length line replacements (in-place edits only). */
export function buildUnifiedDiff(relativePath, before, after, context = 3) {
  const beforeLines = before.split('\n');
  const afterLines = after.split('\n');
  if (beforeLines.length !== afterLines.length) {
    throw new Error('buildUnifiedDiff supports in-place line replacements only');
  }
  const changed = [];
  beforeLines.forEach((line, index) => {
    if (line !== afterLines[index]) {
      changed.push(index);
    }
  });
  if (changed.length === 0) {
    return '';
  }
  const trailingNewline = before.endsWith('\n');
  const lineCount = trailingNewline ? beforeLines.length - 1 : beforeLines.length;
  const hunks = [];
  let start = Math.max(0, changed[0] - context);
  let end = Math.min(lineCount - 1, changed[0] + context);
  for (const index of changed.slice(1)) {
    if (index - context <= end + 1) {
      end = Math.min(lineCount - 1, index + context);
    } else {
      hunks.push([start, end]);
      start = Math.max(0, index - context);
      end = Math.min(lineCount - 1, index + context);
    }
  }
  hunks.push([start, end]);
  const out = [`diff --git a/${relativePath} b/${relativePath}`, `--- a/${relativePath}`, `+++ b/${relativePath}`];
  for (const [hunkStart, hunkEnd] of hunks) {
    const length = hunkEnd - hunkStart + 1;
    out.push(`@@ -${hunkStart + 1},${length} +${hunkStart + 1},${length} @@`);
    for (let index = hunkStart; index <= hunkEnd; index += 1) {
      if (beforeLines[index] === afterLines[index]) {
        out.push(` ${beforeLines[index]}`);
      } else {
        out.push(`-${beforeLines[index]}`);
        out.push(`+${afterLines[index]}`);
      }
    }
  }
  return `${out.join('\n')}\n`;
}

/** Produces the staged patch text for package.json and package-lock.json. Pure. */
export function buildStagedPatch({ current, next, packageJsonText, packageLockText, pathPrefix }) {
  assertIdentity(current, 'current identity');
  assertIdentity(next, 'next identity');
  if (current === next) {
    throw new Error('current and next identities are equal; nothing to stage');
  }
  const prefix = pathPrefix.length > 0 && !pathPrefix.endsWith('/') ? `${pathPrefix}/` : pathPrefix;
  const files = [];
  const packageJsonStaged = stageVersionLines(packageJsonText, { current, next, indent: 2, occurrences: 1 });
  files.push({ path: `${prefix}package.json`, before: packageJsonText, after: packageJsonStaged.text });
  if (typeof packageLockText === 'string') {
    const top = stageVersionLines(packageLockText, { current, next, indent: 2, occurrences: 1 });
    const root = stageVersionLines(top.text, { current, next, indent: 6, occurrences: 1 });
    files.push({ path: `${prefix}package-lock.json`, before: packageLockText, after: root.text });
  }
  return files.map((file) => buildUnifiedDiff(file.path, file.before, file.after)).join('');
}

const SELF_BASENAME = path.basename(fileURLToPath(import.meta.url));

async function scanFiles(root, subdirectories, patterns, { skipTests = true, excludeBasenames = [SELF_BASENAME] } = {}) {
  const hits = [];
  async function walk(directory) {
    let entries;
    try {
      entries = await readdir(directory, { withFileTypes: true });
    } catch {
      return;
    }
    for (const entry of entries.sort((left, right) => (left.name < right.name ? -1 : left.name > right.name ? 1 : 0))) {
      const absolute = path.join(directory, entry.name);
      if (entry.isDirectory()) {
        if (entry.name === 'node_modules' || (skipTests && entry.name === '__tests__')) {
          continue;
        }
        await walk(absolute);
      } else if (
        /\.(?:ts|tsx|mjs|js|cjs)$/u.test(entry.name) &&
        !excludeBasenames.includes(entry.name) &&
        !(skipTests && /\.test\.[cm]?[jt]sx?$/u.test(entry.name))
      ) {
        const text = await readFile(absolute, 'utf8');
        for (const { id, pattern } of patterns) {
          if (pattern.test(text)) {
            hits.push({ file: path.relative(root, absolute), patternId: id });
          }
        }
      }
    }
  }
  for (const subdirectory of subdirectories) {
    await walk(path.join(root, subdirectory));
  }
  hits.sort((left, right) => (left.file < right.file ? -1 : left.file > right.file ? 1 : left.patternId < right.patternId ? -1 : 1));
  return hits;
}

function findGitRoot(start) {
  let current = start;
  while (true) {
    if (existsSync(path.join(current, '.git'))) {
      return current;
    }
    const parent = path.dirname(current);
    if (parent === current) {
      return null;
    }
    current = parent;
  }
}

function printUsage(write) {
  write(`Usage: node ./scripts/verify-version-identity.mjs --expect <identity> [options]

Options:
  --expect <identity>     Expected product identity, e.g. 3.0.0-rc.1 (required)
  --root <dir>            Frontend root (default: the directory above scripts/)
  --app-path <dir>        Staged .app to inspect (Info.plist identity keys)
  --dmg-path <file>       DMG file whose basename is checked
  --require-all           Treat ABSENT / NOT_INSPECTED / PRESENT_UNCHECKED surfaces as failures
  --stage-patch <file>    Write a unified diff staging the expected identity into
                          package.json and package-lock.json; never applied
  --patch-prefix <path>   Path prefix for the staged patch (default: frontend root relative to the git root)
  --json <file>           Also write the report as JSON
  --help                  Show this message

Exit: 0 no mismatch; 1 mismatch (or incomplete with --require-all); 2 refused.
Evidence only: changes no product byte; performs no signing, notarization, publication, or release act.
`);
}

export function parseArgs(argv) {
  const options = {
    expect: null,
    root: DEFAULT_FRONTEND_ROOT,
    appPath: null,
    dmgPath: null,
    requireAll: false,
    stagePatch: null,
    patchPrefix: null,
    json: null,
    help: false
  };
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    const takeValue = () => {
      const value = argv[index + 1];
      if (value === undefined || value.startsWith('--')) {
        throw new Error(`Missing value for ${token}`);
      }
      index += 1;
      return value;
    };
    if (token === '--help') {
      options.help = true;
    } else if (token === '--expect') {
      options.expect = takeValue();
    } else if (token === '--root') {
      options.root = path.resolve(takeValue());
    } else if (token === '--app-path') {
      options.appPath = path.resolve(takeValue());
    } else if (token === '--dmg-path') {
      options.dmgPath = path.resolve(takeValue());
    } else if (token === '--require-all') {
      options.requireAll = true;
    } else if (token === '--stage-patch') {
      options.stagePatch = path.resolve(takeValue());
    } else if (token === '--patch-prefix') {
      options.patchPrefix = takeValue();
    } else if (token === '--json') {
      options.json = path.resolve(takeValue());
    } else {
      throw new Error(`Unknown option: ${token}`);
    }
  }
  if (!options.help) {
    assertIdentity(options.expect, '--expect');
  }
  return options;
}

export async function verifyVersionIdentity(options) {
  const packageJsonPath = path.join(options.root, 'package.json');
  const packageLockPath = path.join(options.root, 'package-lock.json');
  const packageJsonText = await readFile(packageJsonPath, 'utf8');
  const packageJson = JSON.parse(packageJsonText);
  const packageLockText = existsSync(packageLockPath) ? await readFile(packageLockPath, 'utf8') : null;
  const packageLock = packageLockText === null ? null : JSON.parse(packageLockText);

  let infoPlist = null;
  if (options.appPath) {
    const plistPath = path.join(options.appPath, 'Contents', 'Info.plist');
    infoPlist = readPlistStrings(await readFile(plistPath, 'utf8'), [
      'CFBundleShortVersionString',
      'CFBundleVersion',
      'CFBundleIdentifier',
      'CFBundleName'
    ]);
  }

  const sourceScan = await scanFiles(options.root, ['electron', 'src'], VERSION_REPORTING_PATTERNS);
  const scriptScan = await scanFiles(options.root, ['scripts'], [
    { id: 'product-version-token', pattern: /\b(?:productVersion|appVersion|releaseVersion|CHIRALITY_APP_VERSION)\b/u }
  ]);

  const surfaces = collectIdentitySurfaces({
    expected: options.expect,
    packageJson,
    packageLock,
    infoPlist,
    dmgBasename: options.dmgPath ? path.basename(options.dmgPath) : null,
    sourceScan,
    scriptScan
  });
  const evaluation = evaluateSurfaces(surfaces, { requireAll: options.requireAll });

  let stagedPatch = null;
  if (options.stagePatch) {
    const gitRoot = findGitRoot(options.root);
    const prefix =
      options.patchPrefix ?? (gitRoot ? path.relative(gitRoot, options.root).split(path.sep).join('/') : '');
    const current = typeof packageJson.version === 'string' ? packageJson.version : null;
    const patchText = buildStagedPatch({
      current,
      next: options.expect,
      packageJsonText,
      packageLockText,
      pathPrefix: prefix
    });
    await mkdir(path.dirname(options.stagePatch), { recursive: true });
    await writeFile(options.stagePatch, patchText, 'utf8');
    stagedPatch = { path: options.stagePatch, bytes: Buffer.byteLength(patchText), sha256: sha256Hex(patchText), applied: false };
  }

  const report = {
    schema: 'chirality-version-identity-report/v1',
    expected: options.expect,
    frontendRoot: options.root,
    inputs: {
      packageJson: { path: packageJsonPath, sha256: sha256Hex(packageJsonText) },
      packageLock: packageLockText === null ? null : { path: packageLockPath, sha256: sha256Hex(packageLockText) },
      appPath: options.appPath,
      dmgPath: options.dmgPath
    },
    surfaces,
    evaluation,
    stagedPatch,
    boundary:
      'Evidence only: no product byte changed; no signing, notarization, publication, distribution, or release act; no release-readiness claim.'
  };
  return report;
}

/**
 * @param {{
 *   argv?: string[],
 *   stdout?: { write(text: string): unknown },
 *   stderr?: { write(text: string): unknown }
 * }} options
 */
export async function runCli({ argv = process.argv.slice(2), stdout = process.stdout, stderr = process.stderr } = {}) {
  let options;
  try {
    options = parseArgs(argv);
  } catch (error) {
    stderr.write(`version identity: ${error.message}\n`);
    printUsage((text) => stderr.write(text));
    return 2;
  }
  if (options.help) {
    printUsage((text) => stdout.write(text));
    return 0;
  }
  let report;
  try {
    report = await verifyVersionIdentity(options);
  } catch (error) {
    stderr.write(`version identity check could not run: ${error.message}\n`);
    return 2;
  }
  stdout.write(
    renderReport({
      expected: report.expected,
      frontendRoot: report.frontendRoot,
      surfaces: report.surfaces,
      evaluation: report.evaluation,
      stagedPatch: report.stagedPatch
    })
  );
  if (options.json) {
    await mkdir(path.dirname(options.json), { recursive: true });
    await writeFile(options.json, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
  }
  return report.evaluation.result === 'PASS' ? 0 : 1;
}

const isMain =
  process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;
if (isMain) {
  process.exitCode = await runCli();
}
