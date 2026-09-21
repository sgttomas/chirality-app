#!/usr/bin/env node
/**
 * generate-sbom.mjs
 *
 * Emits a CycloneDX JSON SBOM with an exactly pinned Syft release.
 *
 * Posture:
 *   - The Syft release is pinned in `SYFT_PIN`; the script never downloads
 *     or installs Syft. A locally installed `syft` binary (or one named with
 *     `--syft-bin`) must report exactly the pinned version, verified with
 *     `syft version` before any scan runs. Any other version, an unparsable
 *     version report, or a missing binary is a refusal (exit 2).
 *   - `--artifact <path>` scans a named artifact (a directory such as a
 *     staged `Chirality.app`, or a regular file). A DMG must be mounted and
 *     its app directory named; Syft is not asked to open disk images.
 *   - `--closure` scans `package-lock.json` for the installed production
 *     dependency closure (Syft's JavaScript lock cataloger with development
 *     dependencies excluded).
 *   - `--dry-run` prints the exact command, arguments, and environment that
 *     would run, without executing Syft. It still refuses unpinnable
 *     arguments, but does not require Syft to be installed.
 *
 * This tool produces evidence only. It performs no signing, notarization,
 * publication, distribution, or release act and makes no release-readiness
 * claim.
 */

import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const SCRIPT_DIRECTORY = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_FRONTEND_ROOT = path.resolve(SCRIPT_DIRECTORY, '..');

/**
 * Exact Syft release pin. Changing this pin is a recorded evidence-tooling
 * change, not a runtime configuration; the tag and version must agree.
 */
export const SYFT_PIN = Object.freeze({
  tag: 'v1.18.1',
  version: '1.18.1',
  releaseUrl: 'https://github.com/anchore/syft/releases/tag/v1.18.1'
});

export const EXIT_OK = 0;
export const EXIT_SCAN_FAILED = 1;
export const EXIT_REFUSED = 2;

const EXACT_SEMVER = /^\d+\.\d+\.\d+$/;

/** @param {{ tag: string, version: string }} pin */
export function assertPinIsExact(pin = SYFT_PIN) {
  if (!pin || typeof pin.version !== 'string' || !EXACT_SEMVER.test(pin.version)) {
    throw new Error('SYFT_PIN.version must be an exact semantic version (x.y.z)');
  }
  if (pin.tag !== `v${pin.version}`) {
    throw new Error(`SYFT_PIN.tag "${String(pin.tag)}" must equal "v${pin.version}"`);
  }
  return pin;
}

/**
 * Parses the output of `syft version`. Accepts the multi-line report
 * (`Application: syft` / `Version: 1.18.1`) and the single-line form
 * (`syft 1.18.1`). Returns `null` when no version can be read.
 */
export function parseSyftVersionOutput(text) {
  if (typeof text !== 'string') {
    return null;
  }
  const multiLine = text.match(/^\s*Version:\s*v?(\d+\.\d+\.\d+)\s*$/mu);
  if (multiLine) {
    return { version: multiLine[1] };
  }
  const singleLine = text.match(/^\s*syft\s+v?(\d+\.\d+\.\d+)\b/mu);
  if (singleLine) {
    return { version: singleLine[1] };
  }
  return null;
}

/**
 * @param {{ version: string } | null} reported
 * @param {{ tag: string, version: string }} pin
 */
export function assertPinnedSyftVersion(reported, pin = SYFT_PIN) {
  assertPinIsExact(pin);
  if (!reported || typeof reported.version !== 'string') {
    throw new Error(`unable to read a Syft version; refusing to scan (pinned ${pin.tag})`);
  }
  if (reported.version !== pin.version) {
    throw new Error(
      `Syft version mismatch: installed ${reported.version}, pinned ${pin.version} (${pin.tag}); refusing to scan`
    );
  }
  return reported.version;
}

/** Maps a filesystem kind to Syft's explicit source scheme. */
export function syftSourceFor(kind, absolutePath) {
  if (!path.isAbsolute(absolutePath)) {
    throw new Error('artifact path must be absolute');
  }
  if (kind === 'directory') {
    return `dir:${absolutePath}`;
  }
  if (kind === 'file') {
    return `file:${absolutePath}`;
  }
  throw new Error(`unsupported artifact kind "${String(kind)}"`);
}

/** @param {{ source: string, outputPath: string, sourceName?: string | null, sourceVersion?: string | null }} plan */
export function buildSyftScanArgs({ source, outputPath, sourceName = null, sourceVersion = null }) {
  if (typeof source !== 'string' || !/^(dir|file):/u.test(source)) {
    throw new Error('Syft source must use an explicit dir: or file: scheme');
  }
  if (typeof outputPath !== 'string' || !path.isAbsolute(outputPath)) {
    throw new Error('SBOM output path must be absolute');
  }
  const args = ['scan', source, '--output', `cyclonedx-json=${outputPath}`, '--quiet'];
  if (typeof sourceName === 'string' && sourceName.length > 0) {
    args.push('--source-name', sourceName);
  }
  if (typeof sourceVersion === 'string' && sourceVersion.length > 0) {
    args.push('--source-version', sourceVersion);
  }
  return args;
}

/**
 * Minimal, reviewed environment for Syft: no update checks, no dev dependencies, no ambient config.
 * @param {Record<string, string | undefined>} env
 */
export function buildSyftEnvironment(env = process.env) {
  const minimal = {
    SYFT_CHECK_FOR_APP_UPDATE: 'false',
    SYFT_JAVASCRIPT_INCLUDE_DEV_DEPENDENCIES: 'false'
  };
  for (const key of ['PATH', 'HOME', 'TMPDIR', 'LANG', 'LC_ALL']) {
    if (typeof env[key] === 'string') {
      minimal[key] = env[key];
    }
  }
  return minimal;
}

function printUsage(write) {
  write(`Usage: node ./scripts/generate-sbom.mjs (--artifact <path> | --closure) [options]

Modes (exactly one):
  --artifact <path>       Scan a named artifact: a directory (for example a staged
                          Chirality.app, or a mounted DMG's app directory) or a file.
  --closure               Scan package-lock.json for the production dependency closure.

Options:
  --output <file>         CycloneDX JSON output path (required unless --dry-run)
  --root <dir>            Frontend root (default: the directory above scripts/)
  --syft-bin <path>       Syft executable (default: "syft" on PATH)
  --source-name <name>    CycloneDX metadata component name (default: package.json name)
  --source-version <v>    CycloneDX metadata component version (default: package.json version)
  --dry-run               Print the exact command and environment; do not run Syft
  --help                  Show this message

Pinned Syft release: ${SYFT_PIN.tag} (${SYFT_PIN.releaseUrl}). The script never downloads Syft.
Evidence only: performs no signing, notarization, publication, or release act.
`);
}

export function parseArgs(argv) {
  const options = {
    artifact: null,
    closure: false,
    output: null,
    root: DEFAULT_FRONTEND_ROOT,
    syftBin: 'syft',
    sourceName: null,
    sourceVersion: null,
    dryRun: false,
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
    } else if (token === '--artifact') {
      options.artifact = path.resolve(takeValue());
    } else if (token === '--closure') {
      options.closure = true;
    } else if (token === '--output') {
      options.output = path.resolve(takeValue());
    } else if (token === '--root') {
      options.root = path.resolve(takeValue());
    } else if (token === '--syft-bin') {
      options.syftBin = takeValue();
    } else if (token === '--source-name') {
      options.sourceName = takeValue();
    } else if (token === '--source-version') {
      options.sourceVersion = takeValue();
    } else if (token === '--dry-run') {
      options.dryRun = true;
    } else {
      throw new Error(`Unknown option: ${token}`);
    }
  }
  if (options.help) {
    return options;
  }
  if ((options.artifact === null) === !options.closure) {
    throw new Error('exactly one of --artifact <path> or --closure is required');
  }
  if (options.output === null) {
    if (!options.dryRun) {
      throw new Error('--output <file> is required');
    }
    options.output = path.join(options.root, 'artifacts', 'sbom', 'sbom.cdx.json');
  }
  return options;
}

function runProcess(command, args, { env, cwd }, spawnProcess) {
  return new Promise((resolve, reject) => {
    let child;
    try {
      child = spawnProcess(command, args, { cwd, env, shell: false, stdio: ['ignore', 'pipe', 'pipe'] });
    } catch (error) {
      reject(error);
      return;
    }
    let stdout = '';
    let stderr = '';
    child.stdout?.on('data', (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr?.on('data', (chunk) => {
      stderr += chunk.toString();
    });
    child.once('error', reject);
    child.once('close', (code, signal) => {
      resolve({ code: code ?? (signal ? 128 : 1), signal, stdout, stderr });
    });
  });
}

export async function readSyftVersion({ syftBin, env, cwd, spawnProcess = spawn }) {
  let result;
  try {
    result = await runProcess(syftBin, ['version'], { env, cwd }, spawnProcess);
  } catch (error) {
    if (error && error.code === 'ENOENT') {
      throw new Error(
        `Syft binary not found ("${syftBin}"); install Syft ${SYFT_PIN.tag} locally — this script does not download it`
      );
    }
    throw error;
  }
  if (result.code !== 0) {
    throw new Error(`"${syftBin} version" exited with status ${result.code}: ${result.stderr.trim()}`);
  }
  return parseSyftVersionOutput(result.stdout);
}

export async function planScan(options) {
  assertPinIsExact(SYFT_PIN);
  const packageJson = JSON.parse(await readFile(path.join(options.root, 'package.json'), 'utf8'));
  const sourceName = options.sourceName ?? (typeof packageJson.name === 'string' ? packageJson.name : null);
  const sourceVersion =
    options.sourceVersion ?? (typeof packageJson.version === 'string' ? packageJson.version : null);
  let source;
  let subject;
  if (options.closure) {
    const lockPath = path.join(options.root, 'package-lock.json');
    await stat(lockPath);
    source = syftSourceFor('file', lockPath);
    subject = { mode: 'closure', path: lockPath };
  } else {
    const info = await stat(options.artifact);
    const kind = info.isDirectory() ? 'directory' : info.isFile() ? 'file' : null;
    if (kind === null) {
      throw new Error(`artifact "${options.artifact}" is neither a directory nor a regular file`);
    }
    source = syftSourceFor(kind, options.artifact);
    subject = { mode: 'artifact', path: options.artifact, kind };
  }
  return {
    subject,
    command: options.syftBin,
    args: buildSyftScanArgs({ source, outputPath: options.output, sourceName, sourceVersion }),
    env: buildSyftEnvironment(),
    cwd: options.root,
    pin: SYFT_PIN,
    output: options.output
  };
}

export async function runSbom(options, { spawnProcess = spawn } = {}) {
  const plan = await planScan(options);
  if (options.dryRun) {
    return { status: 'DRY_RUN', ...describePlan(plan) };
  }
  const reported = await readSyftVersion({
    syftBin: plan.command,
    env: plan.env,
    cwd: plan.cwd,
    spawnProcess
  });
  const syftVersion = assertPinnedSyftVersion(reported, SYFT_PIN);
  const result = await runProcess(plan.command, plan.args, { env: plan.env, cwd: plan.cwd }, spawnProcess);
  if (result.code !== 0) {
    const error = new Error(`Syft scan exited with status ${result.code}: ${result.stderr.trim()}`);
    error.exitCode = EXIT_SCAN_FAILED;
    throw error;
  }
  const bytes = await readFile(plan.output);
  const parsed = JSON.parse(bytes.toString('utf8'));
  if (parsed.bomFormat !== 'CycloneDX') {
    const error = new Error('Syft output is not a CycloneDX document');
    error.exitCode = EXIT_SCAN_FAILED;
    throw error;
  }
  return {
    status: 'PASS',
    syftVersion,
    ...describePlan(plan),
    sbom: {
      path: plan.output,
      bytes: bytes.length,
      sha256: createHash('sha256').update(bytes).digest('hex'),
      bomFormat: parsed.bomFormat,
      specVersion: parsed.specVersion ?? null,
      componentCount: Array.isArray(parsed.components) ? parsed.components.length : 0
    }
  };
}

const HOST_INHERITED_ENV_KEYS = Object.freeze(['PATH', 'HOME', 'TMPDIR', 'LANG', 'LC_ALL']);

/** Reports the effective environment with host-specific values replaced so the record stays portable. */
export function describeEnvironment(env) {
  const described = {};
  for (const key of Object.keys(env).sort()) {
    described[key] = HOST_INHERITED_ENV_KEYS.includes(key) ? '<inherited from host>' : env[key];
  }
  return described;
}

function describePlan(plan) {
  return {
    pinnedSyft: plan.pin,
    subject: plan.subject,
    command: plan.command,
    args: plan.args,
    cwd: plan.cwd,
    env: describeEnvironment(plan.env),
    output: plan.output,
    boundary:
      'Evidence only: no signing, notarization, publication, distribution, or release act; no release-readiness claim.'
  };
}

/**
 * @param {{
 *   argv?: string[],
 *   stdout?: { write(text: string): unknown },
 *   stderr?: { write(text: string): unknown },
 *   spawnProcess?: typeof spawn
 * }} options
 */
export async function runCli({
  argv = process.argv.slice(2),
  stdout = process.stdout,
  stderr = process.stderr,
  spawnProcess = spawn
} = {}) {
  let options;
  try {
    options = parseArgs(argv);
  } catch (error) {
    stderr.write(`sbom: ${error.message}\n`);
    printUsage((text) => stderr.write(text));
    return EXIT_REFUSED;
  }
  if (options.help) {
    printUsage((text) => stdout.write(text));
    return EXIT_OK;
  }
  try {
    const summary = await runSbom(options, { spawnProcess });
    stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
    return EXIT_OK;
  } catch (error) {
    stderr.write(`sbom generation refused or failed: ${error.message}\n`);
    return error.exitCode === EXIT_SCAN_FAILED ? EXIT_SCAN_FAILED : EXIT_REFUSED;
  }
}

const isMain =
  process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;
if (isMain) {
  process.exitCode = await runCli();
}
