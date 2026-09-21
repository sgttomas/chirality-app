#!/usr/bin/env node
/**
 * generate-third-party-notices.mjs
 *
 * Walks the production dependency closure recorded in `package-lock.json`
 * (lockfile v3), reads license metadata and license text from the installed
 * `node_modules` tree, and emits a deterministic `THIRD_PARTY_NOTICES.md`
 * plus an optional machine-readable summary.
 *
 * Closure semantics:
 *   - starts at the root package's `dependencies` and `optionalDependencies`
 *     (never `devDependencies`);
 *   - follows `dependencies`, `optionalDependencies`, and `peerDependencies`
 *     of every reached entry using npm's nested `node_modules` resolution;
 *   - follows `link: true` entries (the `@chirality/*` `file:` runtime
 *     packages and the workspace facade) to their target entries so their
 *     transitive closure is included; link targets are reported as
 *     first-party, not third-party;
 *   - refuses if the lockfile is not v3, if a reached entry is flagged
 *     `dev: true`, or if a required notice package is missing.
 *
 * Output is deterministic: ordering is by package name, then version, then
 * lock key; no timestamps are written; the lockfile SHA-256 is recorded so
 * the output can be recomputed by an independent verifier.
 *
 * This tool produces evidence only. It performs no signing, notarization,
 * publication, distribution, or release act and makes no release-readiness
 * claim.
 */

import { createHash } from 'node:crypto';
import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const SCRIPT_DIRECTORY = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_FRONTEND_ROOT = path.resolve(SCRIPT_DIRECTORY, '..');
export const DEFAULT_OUTPUT_RELATIVE = path.join(
  'artifacts',
  'third-party-notices',
  'THIRD_PARTY_NOTICES.md'
);
export const DEFAULT_EXCERPT_LINES = 8;

/** Packages already noticed in THIRD_PARTY_NOTICES_PI.md; they must remain in the closure. */
export const REQUIRED_NOTICE_PACKAGES = Object.freeze([
  '@earendil-works/pi-agent-core',
  '@earendil-works/pi-ai',
  '@earendil-works/pi-coding-agent',
  '@earendil-works/pi-tui'
]);

/** Runtime file-dependency packages whose transitive closure must be walked. */
export const REQUIRED_FIRST_PARTY_LINKS = Object.freeze([
  '@chirality/engine-claude',
  '@chirality/engine-pi-omlx',
  '@chirality/runtime-cli',
  '@chirality/runtime-client',
  '@chirality/runtime-contracts',
  '@chirality/runtime-core',
  '@chirality/runtime-daemon'
]);

const LICENSE_FILE_PATTERN = /^(licen[cs]e|copying)(\.|-|$)/i;

export function sha256Hex(input) {
  return createHash('sha256').update(input).digest('hex');
}

function compareStrings(left, right) {
  if (left === right) {
    return 0;
  }
  return left < right ? -1 : 1;
}

/** Derives the package name from a lockfile key such as `node_modules/a/node_modules/@s/b`. */
export function packageNameFromKey(key, entry) {
  const marker = 'node_modules/';
  const index = key.lastIndexOf(marker);
  if (index >= 0) {
    return key.slice(index + marker.length);
  }
  if (entry && typeof entry.name === 'string' && entry.name.length > 0) {
    return entry.name;
  }
  throw new Error(`Unable to derive a package name for lock key "${key}"`);
}

/** Resolves `name` as npm would from the package at lock key `fromKey`. */
export function resolveDependencyKey(packages, fromKey, name) {
  const candidates = [];
  if (fromKey === '') {
    candidates.push(`node_modules/${name}`);
  } else {
    let current = fromKey;
    while (current.length > 0) {
      candidates.push(`${current}/node_modules/${name}`);
      const nested = current.lastIndexOf('/node_modules/');
      if (nested >= 0) {
        current = current.slice(0, nested);
        continue;
      }
      const slash = current.lastIndexOf('/');
      current = slash >= 0 ? current.slice(0, slash) : '';
    }
    candidates.push(`node_modules/${name}`);
  }
  for (const candidate of candidates) {
    if (Object.hasOwn(packages, candidate)) {
      return candidate;
    }
  }
  return null;
}

function normalizeDeclaredLicense(value) {
  if (typeof value === 'string') {
    return value.trim().length > 0 ? value.trim() : null;
  }
  if (Array.isArray(value)) {
    const types = value
      .map((item) => (typeof item === 'string' ? item : item?.type))
      .filter((item) => typeof item === 'string' && item.length > 0);
    return types.length > 0 ? types.join(' OR ') : null;
  }
  if (value && typeof value === 'object' && typeof value.type === 'string') {
    return value.type;
  }
  return null;
}

/**
 * Computes the production closure from a parsed lockfile.
 *
 * @returns {{ entries: Array<{key: string, name: string, version: string|null, license: string|null,
 *   resolved: string|null, firstParty: boolean, link: boolean, optional: boolean, os: string[]|null,
 *   cpu: string[]|null, linkTargetOf: string[]}>, unresolvedOptional: string[] }}
 */
export function computeProductionClosure(lock) {
  if (!lock || typeof lock !== 'object' || lock.lockfileVersion !== 3) {
    throw new Error('package-lock.json must be lockfileVersion 3');
  }
  const packages = lock.packages;
  if (!packages || typeof packages !== 'object' || !Object.hasOwn(packages, '')) {
    throw new Error('package-lock.json is missing the root "" package entry');
  }

  const reached = new Map();
  const unresolvedOptional = [];
  const queue = [];
  const linkTargetOf = new Map();

  function enqueue(key, viaKey) {
    if (reached.has(key)) {
      return;
    }
    const entry = packages[key];
    if (entry.dev === true) {
      throw new Error(
        `lock entry "${key}" is flagged dev-only but was reached from production entry "${viaKey}"`
      );
    }
    reached.set(key, entry);
    queue.push(key);
  }

  reached.set('', packages['']);
  queue.push('');

  while (queue.length > 0) {
    const key = queue.shift();
    const entry = packages[key];
    if (entry.link === true) {
      const target = entry.resolved;
      if (typeof target !== 'string' || !Object.hasOwn(packages, target)) {
        throw new Error(`link entry "${key}" resolves to an unknown lock key "${String(target)}"`);
      }
      const owners = linkTargetOf.get(target) ?? [];
      owners.push(key);
      linkTargetOf.set(target, owners);
      enqueue(target, key);
      continue;
    }
    const requiredNames = Object.keys(entry.dependencies ?? {});
    const optionalNames = new Set(Object.keys(entry.optionalDependencies ?? {}));
    const peerNames = Object.keys(entry.peerDependencies ?? {});
    const peerMeta = entry.peerDependenciesMeta ?? {};
    const optionalPeers = new Set(
      peerNames.filter((name) => peerMeta[name] && peerMeta[name].optional === true)
    );
    const names = new Set([...requiredNames, ...optionalNames, ...peerNames]);
    for (const name of [...names].sort(compareStrings)) {
      const resolvedKey = resolveDependencyKey(packages, key, name);
      if (resolvedKey === null) {
        const isPeer = peerNames.includes(name);
        if (optionalNames.has(name) || optionalPeers.has(name) || isPeer) {
          unresolvedOptional.push(`${key === '' ? '(root)' : key} -> ${name}`);
          continue;
        }
        throw new Error(`dependency "${name}" of "${key === '' ? '(root)' : key}" is not resolvable in package-lock.json`);
      }
      enqueue(resolvedKey, key);
    }
  }

  const entries = [];
  for (const [key, entry] of reached) {
    if (key === '') {
      continue;
    }
    const isLink = entry.link === true;
    const isWorkspaceOrFileTarget = !key.includes('node_modules/');
    entries.push({
      key,
      name: packageNameFromKey(key, entry),
      version: typeof entry.version === 'string' ? entry.version : null,
      license: isLink ? null : normalizeDeclaredLicense(entry.license),
      resolved: typeof entry.resolved === 'string' ? entry.resolved : null,
      firstParty: isLink || isWorkspaceOrFileTarget,
      link: isLink,
      optional: entry.optional === true,
      os: Array.isArray(entry.os) ? entry.os.slice().sort(compareStrings) : null,
      cpu: Array.isArray(entry.cpu) ? entry.cpu.slice().sort(compareStrings) : null,
      linkTargetOf: (linkTargetOf.get(key) ?? []).slice().sort(compareStrings)
    });
  }
  entries.sort(
    (left, right) =>
      compareStrings(left.name, right.name) ||
      compareStrings(left.version ?? '', right.version ?? '') ||
      compareStrings(left.key, right.key)
  );
  unresolvedOptional.sort(compareStrings);
  return { entries, unresolvedOptional };
}

/** Groups closure entries into distinct third-party `name@version` records. */
export function groupThirdParty(entries) {
  const groups = new Map();
  for (const entry of entries) {
    if (entry.firstParty) {
      continue;
    }
    const id = `${entry.name}@${entry.version ?? 'unknown'}`;
    const group = groups.get(id) ?? {
      id,
      name: entry.name,
      version: entry.version,
      license: entry.license,
      resolved: entry.resolved,
      optional: entry.optional,
      os: entry.os,
      cpu: entry.cpu,
      keys: []
    };
    group.keys.push(entry.key);
    if (group.license === null && entry.license !== null) {
      group.license = entry.license;
    }
    groups.set(id, group);
  }
  const list = [...groups.values()];
  for (const group of list) {
    group.keys.sort(compareStrings);
  }
  list.sort(
    (left, right) =>
      compareStrings(left.name, right.name) || compareStrings(left.version ?? '', right.version ?? '')
  );
  return list;
}

export function excerptLicenseText(text, maxLines = DEFAULT_EXCERPT_LINES) {
  const normalized = text.replaceAll('\r\n', '\n').replaceAll('\r', '\n');
  const lines = normalized.split('\n');
  while (lines.length > 0 && lines[lines.length - 1].trim() === '') {
    lines.pop();
  }
  const excerpt = lines.slice(0, maxLines).map((line) => line.replace(/\s+$/u, ''));
  return {
    excerpt: excerpt.join('\n'),
    truncated: lines.length > maxLines,
    lineCount: lines.length,
    normalized
  };
}

export function selectLicenseFile(fileNames) {
  return fileNames.filter((name) => LICENSE_FILE_PATTERN.test(name)).sort(compareStrings)[0] ?? null;
}

async function readLicenseArtifacts(rootDirectory, group, excerptLines) {
  const installDirectory = path.join(rootDirectory, group.keys[0]);
  let fileNames = [];
  try {
    fileNames = await readdir(installDirectory);
  } catch (error) {
    return { status: 'INSTALL_DIRECTORY_MISSING', detail: error.message };
  }
  let declaredFallback = null;
  if (group.license === null) {
    try {
      const manifest = JSON.parse(await readFile(path.join(installDirectory, 'package.json'), 'utf8'));
      declaredFallback = normalizeDeclaredLicense(manifest.license ?? manifest.licenses);
    } catch {
      declaredFallback = null;
    }
  }
  const licenseFile = selectLicenseFile(fileNames);
  if (licenseFile === null) {
    return { status: 'NOT_PRESENT', declaredFallback };
  }
  const bytes = await readFile(path.join(installDirectory, licenseFile));
  const { excerpt, truncated, lineCount } = excerptLicenseText(bytes.toString('utf8'), excerptLines);
  return {
    status: 'PRESENT',
    declaredFallback,
    fileName: licenseFile,
    byteLength: bytes.length,
    sha256: sha256Hex(bytes),
    lineCount,
    truncated,
    excerpt
  };
}

function fenceSafe(text) {
  return text.replaceAll('```', "'''");
}

export function renderNotices({
  rootName,
  rootVersion,
  lockSha256,
  excerptLines,
  closure,
  thirdParty,
  licenseArtifacts,
  requiredPackages
}) {
  const firstParty = closure.entries.filter((entry) => entry.firstParty);
  const missingLicenseFileCount = thirdParty.filter((group) => {
    const artifacts = licenseArtifacts.get(group.id);
    return artifacts && artifacts.status === 'NOT_PRESENT';
  }).length;
  const optionalNotInstalledCount = thirdParty.filter((group) => {
    const artifacts = licenseArtifacts.get(group.id);
    return group.optional && (!artifacts || artifacts.status === 'INSTALL_DIRECTORY_MISSING');
  }).length;
  const lines = [];
  lines.push(`# Third-party notices — ${rootName}@${rootVersion} (production dependency closure)`);
  lines.push('');
  lines.push(
    'Generated by `scripts/generate-third-party-notices.mjs` from `package-lock.json` ' +
      `(SHA-256 \`${lockSha256}\`) and the installed \`node_modules\` tree. ` +
      'The closure starts at the root `dependencies` and `optionalDependencies`, follows ' +
      '`dependencies`, `optionalDependencies`, and `peerDependencies`, and follows `file:`/workspace ' +
      'links to their targets. Development-only packages are excluded.'
  );
  lines.push('');
  lines.push(
    'This document is evidence produced during release preparation. It is not a signing, ' +
      'notarization, publication, distribution, or release act and makes no release-readiness claim.'
  );
  lines.push('');
  lines.push('## Summary');
  lines.push('');
  lines.push(`- Root package: \`${rootName}@${rootVersion}\``);
  lines.push(`- Closure entries (lock keys, excluding root): ${closure.entries.length}`);
  lines.push(`- Distinct third-party \`name@version\` records: ${thirdParty.length}`);
  lines.push(`- First-party workspace/file entries (not third-party): ${firstParty.length}`);
  lines.push(
    `- License-text excerpt: first ${excerptLines} lines; the full text is identified by file name, byte length, and SHA-256`
  );
  lines.push(
    `- Required notice packages present: ${requiredPackages
      .map((item) => `\`${item.name}@${item.version}\``)
      .join(', ')}`
  );
  lines.push(
    `- Packages with no license file in the installed tarball (declared license only): ${missingLicenseFileCount} — see \`## Third-party packages\` entries marked NOT PRESENT`
  );
  lines.push(
    `- Platform-conditional optional packages present in the lockfile closure but not installed on the generating host (declared license only): ${optionalNotInstalledCount}`
  );
  if (closure.unresolvedOptional.length > 0) {
    lines.push(`- Unresolved optional dependencies (not installed): ${closure.unresolvedOptional.length}`);
  }
  lines.push('');
  lines.push('## First-party workspace and file dependencies (not third-party)');
  lines.push('');
  lines.push('| Package | Version | Lock key | Kind |');
  lines.push('|---|---|---|---|');
  for (const entry of firstParty) {
    const kind = entry.link ? `link → \`${entry.resolved}\`` : 'link target';
    lines.push(`| \`${entry.name}\` | \`${entry.version ?? '—'}\` | \`${entry.key}\` | ${kind} |`);
  }
  lines.push('');
  lines.push('## Third-party packages');
  lines.push('');
  for (const group of thirdParty) {
    const artifacts = licenseArtifacts.get(group.id);
    const declared = group.license ?? artifacts?.declaredFallback ?? 'UNDECLARED';
    lines.push(`### \`${group.id}\``);
    lines.push('');
    lines.push(`- Declared license: \`${declared}\``);
    lines.push(`- Install path(s): ${group.keys.map((key) => `\`${key}\``).join(', ')}`);
    if (group.resolved) {
      lines.push(`- Resolved: \`${group.resolved}\``);
    }
    if (group.optional && (group.os || group.cpu)) {
      lines.push(
        `- Platform-conditional optional package: os ${group.os ? group.os.join('/') : 'any'}, cpu ${group.cpu ? group.cpu.join('/') : 'any'}`
      );
    }
    if (!artifacts || artifacts.status === 'INSTALL_DIRECTORY_MISSING') {
      lines.push(
        group.optional
          ? '- License file: OPTIONAL PACKAGE NOT INSTALLED ON THIS HOST (declared license taken from `package-lock.json`)'
          : '- License file: INSTALL DIRECTORY MISSING (package not installed in `node_modules`)'
      );
    } else if (artifacts.status === 'NOT_PRESENT') {
      lines.push('- License file: NOT PRESENT in the installed package');
    } else {
      lines.push(
        `- License file: \`${artifacts.fileName}\` (${artifacts.byteLength} bytes, ${artifacts.lineCount} lines, SHA-256 \`${artifacts.sha256}\`)` +
          (artifacts.truncated ? ' — excerpt truncated' : '')
      );
      lines.push('');
      lines.push('```text');
      lines.push(fenceSafe(artifacts.excerpt));
      lines.push('```');
    }
    lines.push('');
  }
  if (closure.unresolvedOptional.length > 0) {
    lines.push('## Unresolved optional dependencies');
    lines.push('');
    for (const item of closure.unresolvedOptional) {
      lines.push(`- \`${item}\``);
    }
  }
  while (lines.length > 0 && lines[lines.length - 1] === '') {
    lines.pop();
  }
  return `${lines.join('\n')}\n`;
}

export function buildSummary({
  rootName,
  rootVersion,
  lockSha256,
  closure,
  thirdParty,
  licenseArtifacts,
  requiredPackages,
  outputPath,
  outputSha256
}) {
  const licenseCounts = {};
  const missingLicenseFile = [];
  const optionalNotInstalled = [];
  for (const group of thirdParty) {
    const artifacts = licenseArtifacts.get(group.id);
    const declared = group.license ?? artifacts?.declaredFallback ?? 'UNDECLARED';
    licenseCounts[declared] = (licenseCounts[declared] ?? 0) + 1;
    if (!artifacts || artifacts.status === 'INSTALL_DIRECTORY_MISSING') {
      (group.optional ? optionalNotInstalled : missingLicenseFile).push(group.id);
    } else if (artifacts.status !== 'PRESENT') {
      missingLicenseFile.push(group.id);
    }
  }
  return {
    schema: 'chirality-third-party-notices-summary/v1',
    rootPackage: { name: rootName, version: rootVersion },
    lockfileSha256: lockSha256,
    closureEntryCount: closure.entries.length,
    thirdPartyDistinctCount: thirdParty.length,
    firstPartyCount: closure.entries.filter((entry) => entry.firstParty).length,
    firstPartyEntries: closure.entries
      .filter((entry) => entry.firstParty)
      .map((entry) => ({ name: entry.name, version: entry.version, key: entry.key, link: entry.link })),
    requiredPackages,
    licenseCounts: Object.fromEntries(
      Object.entries(licenseCounts).sort(([left], [right]) => compareStrings(left, right))
    ),
    missingLicenseFile,
    optionalNotInstalled,
    unresolvedOptional: closure.unresolvedOptional,
    output: { path: outputPath, sha256: outputSha256 },
    boundary:
      'Evidence only: no signing, notarization, publication, distribution, or release act; no release-readiness claim.'
  };
}

export function assertRequiredPackages(closure, required) {
  const found = [];
  const missing = [];
  for (const name of required) {
    const candidates = closure.entries.filter((item) => item.name === name);
    const entry = candidates.find((item) => !item.link) ?? candidates[0];
    if (entry) {
      found.push({ name, version: entry.version, key: entry.key });
    } else {
      missing.push(name);
    }
  }
  if (missing.length > 0) {
    throw new Error(`required notice packages are missing from the production closure: ${missing.join(', ')}`);
  }
  return found;
}

function printUsage(write) {
  write(`Usage: node ./scripts/generate-third-party-notices.mjs [options]

Options:
  --root <dir>            Frontend root containing package.json, package-lock.json, node_modules
                          (default: the directory above scripts/)
  --output <file>         Notices output path (default: ${DEFAULT_OUTPUT_RELATIVE} under root)
  --summary <file>        Machine-readable summary JSON path (optional)
  --excerpt-lines <n>     License-text excerpt length in lines (default: ${DEFAULT_EXCERPT_LINES})
  --require <package>     Additional package that must be present (repeatable)
  --help                  Show this message

Evidence only: performs no signing, notarization, publication, or release act.
`);
}

export function parseArgs(argv) {
  const options = {
    root: DEFAULT_FRONTEND_ROOT,
    output: null,
    summary: null,
    excerptLines: DEFAULT_EXCERPT_LINES,
    require: [...REQUIRED_NOTICE_PACKAGES, ...REQUIRED_FIRST_PARTY_LINKS],
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
    } else if (token === '--root') {
      options.root = path.resolve(takeValue());
    } else if (token === '--output') {
      options.output = path.resolve(takeValue());
    } else if (token === '--summary') {
      options.summary = path.resolve(takeValue());
    } else if (token === '--excerpt-lines') {
      const parsed = Number.parseInt(takeValue(), 10);
      if (!Number.isInteger(parsed) || parsed < 1) {
        throw new Error('--excerpt-lines must be a positive integer');
      }
      options.excerptLines = parsed;
    } else if (token === '--require') {
      options.require.push(takeValue());
    } else {
      throw new Error(`Unknown option: ${token}`);
    }
  }
  if (options.output === null) {
    options.output = path.join(options.root, DEFAULT_OUTPUT_RELATIVE);
  }
  return options;
}

export async function generateNotices(options) {
  const packageJsonPath = path.join(options.root, 'package.json');
  const lockPath = path.join(options.root, 'package-lock.json');
  const packageJson = JSON.parse(await readFile(packageJsonPath, 'utf8'));
  const lockBytes = await readFile(lockPath);
  const lock = JSON.parse(lockBytes.toString('utf8'));
  const lockSha256 = sha256Hex(lockBytes);
  const closure = computeProductionClosure(lock);
  const requiredPackages = assertRequiredPackages(closure, [...new Set(options.require)].sort(compareStrings));
  const thirdParty = groupThirdParty(closure.entries);
  const licenseArtifacts = new Map();
  for (const group of thirdParty) {
    licenseArtifacts.set(group.id, await readLicenseArtifacts(options.root, group, options.excerptLines));
  }
  const rootName = typeof packageJson.name === 'string' ? packageJson.name : 'unknown';
  const rootVersion = typeof packageJson.version === 'string' ? packageJson.version : 'unknown';
  const notices = renderNotices({
    rootName,
    rootVersion,
    lockSha256,
    excerptLines: options.excerptLines,
    closure,
    thirdParty,
    licenseArtifacts,
    requiredPackages
  });
  await mkdir(path.dirname(options.output), { recursive: true });
  await writeFile(options.output, notices, 'utf8');
  const outputSha256 = sha256Hex(notices);
  const summary = buildSummary({
    rootName,
    rootVersion,
    lockSha256,
    closure,
    thirdParty,
    licenseArtifacts,
    requiredPackages,
    outputPath: options.output,
    outputSha256
  });
  if (options.summary) {
    await mkdir(path.dirname(options.summary), { recursive: true });
    await writeFile(options.summary, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
  }
  return summary;
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
    stderr.write(`third-party notices: ${error.message}\n`);
    printUsage((text) => stderr.write(text));
    return 2;
  }
  if (options.help) {
    printUsage((text) => stdout.write(text));
    return 0;
  }
  try {
    const summary = await generateNotices(options);
    stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
    return 0;
  } catch (error) {
    stderr.write(`third-party notices generation failed: ${error.message}\n`);
    return 1;
  }
}

const isMain =
  process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;
if (isMain) {
  process.exitCode = await runCli();
}
