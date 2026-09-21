import { access, lstat, mkdtemp, readFile, realpath, rm } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { tmpdir } from 'node:os';
import path from 'node:path';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';

/**
 * `desktop:verify-dependencies` (D-GOV-43, A2): the packaged App carries the
 * App-owned Runtime layout and nothing from the retired supply model.
 *
 * Checks, against `Contents/Resources`:
 * - `app.asar` holds `next`, no development-only packages, no legacy engine
 *   packages and no monorepo `@chirality` or `@openai` package entries (the
 *   Codex binary travels as a resource, not inside the archive);
 * - the desktop main bundle embeds `electron/main.ts`,
 *   `electron/runtime-service-host.ts` and the Runtime client, and no longer
 *   embeds the Runtime daemon, the retired hosted supply-model sources or a
 *   legacy engine;
 * - the Runtime service bundle embeds the daemon, the core service and the
 *   stock Codex client sources, and none of the retired hosted composition;
 * - the Runtime CLI bundle stays a client (no daemon source);
 * - the Codex platform tree is staged at `codex/` with its two executables.
 */

const frontendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const ELECTRON_OUTPUT_DIRECTORY_ENV = 'CHIRALITY_ELECTRON_OUTPUT_DIRECTORY';
export function resolvePackagedDependencyBundlePath(env = process.env) {
  let outputDirectory = path.join(frontendRoot, 'dist');
  if (Object.prototype.hasOwnProperty.call(env, ELECTRON_OUTPUT_DIRECTORY_ENV)) {
    const candidate = env[ELECTRON_OUTPUT_DIRECTORY_ENV];
    if (typeof candidate !== 'string' || candidate.length === 0 || candidate.includes('\0')
      || !path.isAbsolute(candidate) || path.normalize(candidate) !== candidate) {
      throw new Error(`${ELECTRON_OUTPUT_DIRECTORY_ENV} must be a normalized absolute path`);
    }
    outputDirectory = candidate;
  }
  return path.join(outputDirectory, 'mac-arm64', 'Chirality.app', 'Contents', 'Resources', 'app.asar');
}
const bundlePath = path.resolve(
  process.argv[2] ?? resolvePackagedDependencyBundlePath()
);
const asarCli = path.join(frontendRoot, 'node_modules', '.bin', 'asar');
const resourcesRoot = path.dirname(bundlePath);
const packagedCliPath = path.join(resourcesRoot, 'runtime-cli', 'chirality-cli.mjs');
const packagedCliSourceMapPath = `${packagedCliPath}.map`;
const packagedServicePath = path.join(resourcesRoot, 'runtime-service', 'standalone-bin.mjs');
const packagedServiceSourceMapPath = `${packagedServicePath}.map`;

const requiredPackages = ['next'];
const forbiddenLegacyRuntimePackages = [
  '@anthropic-ai/claude-agent-sdk',
  '@anthropic-ai/sdk',
  '@earendil-works/pi-agent-core',
  '@earendil-works/pi-ai',
  '@earendil-works/pi-coding-agent',
  '@earendil-works/pi-tui'
];
const claudePlatformPackagePattern =
  /(?:^|\/)node_modules\/(@anthropic-ai\/claude-agent-sdk-[^/]+)(?:\/|$)/;
const forbiddenDevelopmentPackages = [
  'concurrently',
  'electron-builder',
  'esbuild',
  'shell-quote',
  'typescript',
  'vite',
  'vitest',
  'wait-on'
];

function containsPackage(entry, packageName) {
  const marker = `/node_modules/${packageName}`;
  return entry === marker || entry.startsWith(`${marker}/`) || entry.includes(`${marker}/`);
}

export function findForbiddenLegacyRuntimePackage(entry) {
  for (const packageName of forbiddenLegacyRuntimePackages) {
    if (containsPackage(entry, packageName)) return packageName;
  }
  return normalizeSourcePath(entry).match(claudePlatformPackagePattern)?.[1] ?? null;
}

function normalizeSourcePath(source) {
  return source.replaceAll('\\', '/');
}

function hasSource(sources, suffix) {
  const normalizedSuffix = normalizeSourcePath(suffix);
  return sources.some((source) => normalizeSourcePath(source).endsWith(normalizedSuffix));
}

/** The staged stock Codex tree: regular files, executable bits, no symlinks. */
export async function verifyPackagedCodexTree({ resourcesRoot: candidateRoot }) {
  const failures = [];
  if (typeof candidateRoot !== 'string' || candidateRoot.length === 0 || candidateRoot.includes('\0')
    || !path.isAbsolute(candidateRoot) || path.normalize(candidateRoot) !== candidateRoot) {
    return { status: 'FAIL', path: null, failures: ['Resources root must be a normalized absolute path'] };
  }
  const vendorRoot = path.join(candidateRoot, 'codex');
  for (const relativePath of ['bin/codex', 'bin/codex-code-mode-host']) {
    const target = path.join(vendorRoot, relativePath);
    try {
      const info = await lstat(target);
      if (!info.isFile() || info.isSymbolicLink()) failures.push(`packaged codex/${relativePath} must be a regular non-symlink file`);
      else if ((info.mode & 0o111) === 0) failures.push(`packaged codex/${relativePath} is not executable`);
      else if ((await realpath(target)) !== target) failures.push(`packaged codex/${relativePath} resolves outside its exact Resources path`);
    } catch (error) {
      failures.push(`unable to inspect packaged codex/${relativePath}: ${error.message}`);
    }
  }
  try {
    const manifest = JSON.parse(await readFile(path.join(vendorRoot, 'codex-package.json'), 'utf8'));
    if (manifest.entrypoint !== 'bin/codex') failures.push('codex-package.json does not name bin/codex as the entrypoint');
  } catch (error) {
    failures.push(`unable to read packaged codex/codex-package.json: ${error.message}`);
  }
  return { status: failures.length === 0 ? 'PASS' : 'FAIL', path: vendorRoot, failures };
}

export function verifyPackagedRuntimeSources({
  desktopSources,
  serviceSources,
  cliSources,
  packagedEntries
}) {
  const requiredDesktopSources = [
    'electron/main.ts',
    'electron/runtime-service-host.ts',
    'electron/runtime-service-launcher.ts',
    'chirality-runtime/packages/client/src/client.ts'
  ];
  const forbiddenDesktopSources = [
    // The daemon is a separate child now; the main bundle must not embed it.
    'chirality-runtime/packages/daemon/src/runtime-daemon.ts',
    'chirality-runtime/packages/daemon/src/standalone-bin.ts',
    // Supply-model and LaunchAgent residues.
    'electron/runtime-host.ts',
    'electron/runtime-host-legacy.ts',
    'electron/runtime-autostart.ts',
    'electron/host-account-ipc.ts',
    'chirality-runtime/packages/daemon/src/hosted-private-composition.ts',
    'chirality-runtime/packages/daemon/src/hosted-boot.ts',
    'chirality-runtime/packages/daemon/src/codex-admitted-launcher.ts',
    // Legacy engines.
    'src/lib/harness/anthropic-agent-sdk-manager.ts',
    'src/lib/harness/claude-agent-sdk-manager.ts',
    'src/lib/harness/pi-agent-engine-adapter.ts',
    'chirality-runtime/packages/engine-claude/src/index.ts',
    'chirality-runtime/packages/engine-pi-omlx/src/pi-omlx-engine.ts'
  ];
  const requiredServiceSources = [
    'chirality-runtime/packages/daemon/src/standalone-bin.ts',
    'chirality-runtime/packages/daemon/src/runtime-daemon.ts',
    'chirality-runtime/packages/core/src/runtime-service.ts',
    'chirality-runtime/packages/core/src/delegated-runtime.ts',
    'chirality-runtime/packages/daemon/src/codex-supervisor.ts',
    'chirality-runtime/packages/daemon/src/codex-app-server-client.ts'
  ];
  const forbiddenServiceSources = [
    'chirality-runtime/packages/daemon/src/hosted-private-composition.ts',
    'chirality-runtime/packages/daemon/src/hosted-private-entry.ts',
    'chirality-runtime/packages/daemon/src/hosted-boot.ts',
    'chirality-runtime/packages/daemon/src/codex-admitted-launcher.ts',
    'chirality-runtime/packages/daemon/src/codex-authenticated-transport.ts',
    'chirality-runtime/packages/daemon/src/codex-containment.ts',
    'chirality-runtime/packages/daemon/src/supervisor-server.ts',
    'chirality-runtime/packages/core/src/runtime-conformance-v2.ts',
    'chirality-runtime/packages/engine-claude/src/index.ts',
    'chirality-runtime/packages/engine-pi-omlx/src/pi-omlx-engine.ts',
    'electron/main.ts'
  ];
  const requiredCliSources = [
    'chirality-runtime/packages/cli/src/bin.ts',
    'chirality-runtime/packages/cli/src/cli.ts',
    'chirality-runtime/packages/client/src/client.ts'
  ];
  const forbiddenCliSources = [
    'chirality-runtime/packages/daemon/src/runtime-daemon.ts',
    'chirality-runtime/packages/engine-claude/src/index.ts',
    'chirality-runtime/packages/engine-pi-omlx/src/pi-omlx-engine.ts',
    'electron/main.ts',
    'electron/runtime-service-host.ts'
  ];
  const requiredPackagedEntries = ['/dist-electron/main.js', '/dist-electron/main.js.map'];
  const failures = [];

  for (const suffix of requiredDesktopSources) {
    if (!hasSource(desktopSources, suffix)) failures.push(`desktop bundle is missing source ${suffix}`);
  }
  for (const suffix of forbiddenDesktopSources) {
    if (hasSource(desktopSources, suffix)) failures.push(`desktop bundle unexpectedly embeds retired or legacy source ${suffix}`);
  }
  for (const suffix of requiredServiceSources) {
    if (!hasSource(serviceSources, suffix)) failures.push(`runtime service bundle is missing source ${suffix}`);
  }
  for (const suffix of forbiddenServiceSources) {
    if (hasSource(serviceSources, suffix)) failures.push(`runtime service bundle unexpectedly embeds retired or legacy source ${suffix}`);
  }
  for (const suffix of requiredCliSources) {
    if (!hasSource(cliSources, suffix)) failures.push(`CLI bundle is missing source ${suffix}`);
  }
  for (const suffix of forbiddenCliSources) {
    if (hasSource(cliSources, suffix)) failures.push(`CLI client bundle unexpectedly embeds server source ${suffix}`);
  }
  for (const entry of requiredPackagedEntries) {
    if (!packagedEntries.has(entry)) failures.push(`app.asar is missing ${entry}`);
  }

  return {
    failures,
    requiredDesktopSources,
    forbiddenDesktopSources,
    requiredServiceSources,
    forbiddenServiceSources,
    requiredCliSources,
    forbiddenCliSources,
    requiredPackagedEntries
  };
}

function parseSourceMapSources(sourceMap, sourceMapPath) {
  const parsed = JSON.parse(sourceMap);
  if (!Array.isArray(parsed.sources) || !parsed.sources.every((source) => typeof source === 'string')) {
    throw new Error(`Invalid source map sources: ${sourceMapPath}`);
  }
  return parsed.sources;
}

async function extractPackagedFile(entry) {
  const extractionRoot = await mkdtemp(path.join(tmpdir(), 'chirality-asar-extract-'));
  try {
    const child = spawn(asarCli, ['extract-file', bundlePath, entry], {
      cwd: extractionRoot,
      stdio: ['ignore', 'ignore', 'inherit']
    });
    const exitCode = await new Promise((resolve, reject) => {
      child.once('error', reject);
      child.once('close', (code) => resolve(code ?? 1));
    });
    if (exitCode !== 0) {
      throw new Error(`asar extract-file exited with status ${exitCode}`);
    }
    return readFile(path.join(extractionRoot, path.basename(entry)), 'utf8');
  } finally {
    await rm(extractionRoot, { recursive: true, force: true });
  }
}

async function inspectBundle() {
  await access(bundlePath);
  await access(asarCli);
  await access(packagedCliPath);
  await access(packagedCliSourceMapPath);
  await access(packagedServicePath);
  await access(packagedServiceSourceMapPath);
  const codexTree = await verifyPackagedCodexTree({ resourcesRoot });

  const requiredPresent = new Set();
  const forbiddenPresent = new Set();
  const forbiddenLegacyRuntimePresent = new Set();
  let localPackageEntries = 0;
  let codexPackageEntries = 0;
  const packagedEntries = new Set();

  const child = spawn(asarCli, ['list', bundlePath], {
    cwd: frontendRoot,
    stdio: ['ignore', 'pipe', 'inherit']
  });
  const lines = readline.createInterface({ input: child.stdout });

  for await (const entry of lines) {
    packagedEntries.add(normalizeSourcePath(entry));
    if (entry.includes('/node_modules/@chirality/')) localPackageEntries += 1;
    if (entry.includes('/node_modules/@openai/')) codexPackageEntries += 1;
    for (const packageName of requiredPackages) {
      if (containsPackage(entry, packageName)) requiredPresent.add(packageName);
    }
    for (const packageName of forbiddenDevelopmentPackages) {
      if (containsPackage(entry, packageName)) forbiddenPresent.add(packageName);
    }
    const forbiddenLegacyPackage = findForbiddenLegacyRuntimePackage(entry);
    if (forbiddenLegacyPackage) forbiddenLegacyRuntimePresent.add(forbiddenLegacyPackage);
  }

  const exitCode = await new Promise((resolve, reject) => {
    child.once('error', reject);
    child.once('close', (code) => resolve(code ?? 1));
  });
  if (exitCode !== 0) {
    throw new Error(`asar list exited with status ${exitCode}`);
  }

  const missingRequired = requiredPackages.filter((packageName) => !requiredPresent.has(packageName));
  const failures = [];
  failures.push(...codexTree.failures);
  if (localPackageEntries > 0) failures.push(`found ${localPackageEntries} monorepo-only @chirality package entries`);
  if (codexPackageEntries > 0) failures.push(`found ${codexPackageEntries} @openai package entries inside app.asar; the Codex tree belongs under Resources/codex`);
  if (forbiddenPresent.size > 0) failures.push(`found development-only packages: ${[...forbiddenPresent].sort().join(', ')}`);
  if (forbiddenLegacyRuntimePresent.size > 0) failures.push(`found legacy runtime packages: ${[...forbiddenLegacyRuntimePresent].sort().join(', ')}`);
  if (missingRequired.length > 0) failures.push(`missing runtime packages: ${missingRequired.join(', ')}`);
  const desktopSources = parseSourceMapSources(
    await extractPackagedFile('dist-electron/main.js.map'),
    `${bundlePath}:dist-electron/main.js.map`
  );
  const serviceSources = parseSourceMapSources(await readFile(packagedServiceSourceMapPath, 'utf8'), packagedServiceSourceMapPath);
  const cliSources = parseSourceMapSources(await readFile(packagedCliSourceMapPath, 'utf8'), packagedCliSourceMapPath);
  const runtimeSourceProof = verifyPackagedRuntimeSources({ desktopSources, serviceSources, cliSources, packagedEntries });
  failures.push(...runtimeSourceProof.failures);

  const summary = {
    status: failures.length === 0 ? 'PASS' : 'FAIL',
    bundlePath,
    localPackageEntries,
    codexPackageEntries,
    forbiddenDevelopmentPackagesPresent: [...forbiddenPresent].sort(),
    forbiddenLegacyRuntimePackagesPresent: [...forbiddenLegacyRuntimePresent].sort(),
    runtimeProfile: 'app-owned-codex',
    codexTree,
    requiredPackagesPresent: [...requiredPresent].sort(),
    packagedRuntimeSourceProof: {
      status: runtimeSourceProof.failures.length === 0 ? 'PASS' : 'FAIL',
      desktopSourceCount: desktopSources.length,
      serviceSourceCount: serviceSources.length,
      cliSourceCount: cliSources.length,
      requiredDesktopSources: runtimeSourceProof.requiredDesktopSources,
      requiredServiceSources: runtimeSourceProof.requiredServiceSources,
      requiredCliSources: runtimeSourceProof.requiredCliSources
    },
    failures
  };
  console.log(JSON.stringify(summary, null, 2));

  if (failures.length > 0) {
    throw new Error(failures.join('; '));
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await inspectBundle();
}
