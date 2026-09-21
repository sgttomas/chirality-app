import { spawn } from 'node:child_process';
import { lstat, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

import { verifyElectronDist } from './verify-electron-dist.mjs';

/**
 * Plain Electron packaging for the App-owned Runtime (D-GOV-43, A2).
 *
 * Replaces the supply-model pack (`pack-electron-with-supply.mjs`): no
 * supplier staging, no dependency or supplier digests, no native addon, no
 * nested/outer signing phases. The inputs are the built renderer, the Electron
 * bundle, the two Runtime bundles, the staged instruction root and the
 * lockfile-pinned stock `@openai/codex` platform tree declared in
 * `package.json` `build.extraResources`. Signing, when an identity is
 * supplied, happens inside electron-builder through
 * `scripts/sign-electron-runtime-v2.mjs`.
 */

const SUPPORTED_TARGETS = new Set(['dir', 'dmg']);
export const ELECTRON_OUTPUT_DIRECTORY_ENV = 'CHIRALITY_ELECTRON_OUTPUT_DIRECTORY';
export const SIGNING_IDENTITY_SHA1_ENV = 'CHIRALITY_SIGNING_IDENTITY_SHA1';
const frontendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

/** Files that must exist before electron-builder runs (relative to the frontend root). */
export const REQUIRED_BUILD_INPUTS = Object.freeze([
  'dist-electron/main.js',
  'dist-electron/preload.js',
  'dist-runtime/runtime-service/standalone-bin.mjs',
  'dist-runtime/runtime-cli/chirality-cli.mjs',
  'node_modules/.cache/chirality-instruction-root/instruction-bundle-manifest.json',
  '.next/BUILD_ID'
]);

function validateTarget(target) {
  if (!SUPPORTED_TARGETS.has(target)) {
    throw new Error(`Unsupported Electron packaging target: ${String(target)}`);
  }
  return target;
}

export function resolveElectronOutputDirectory(env = process.env, root = frontendRoot) {
  if (!Object.prototype.hasOwnProperty.call(env, ELECTRON_OUTPUT_DIRECTORY_ENV)) {
    return path.join(root, 'dist');
  }
  const candidate = env[ELECTRON_OUTPUT_DIRECTORY_ENV];
  if (
    typeof candidate !== 'string' ||
    candidate.length === 0 ||
    candidate.includes('\0') ||
    !path.isAbsolute(candidate) ||
    path.normalize(candidate) !== candidate
  ) {
    throw new Error(`${ELECTRON_OUTPUT_DIRECTORY_ENV} must be a normalized absolute path`);
  }
  return candidate;
}

export function expectedPackagedAppPath(outputDirectory) {
  return path.join(outputDirectory, 'mac-arm64', 'Chirality.app');
}

export function buildElectronBuilderArgs(electronDistDirectory, target = 'dir', outputDirectory) {
  if (typeof electronDistDirectory !== 'string' || electronDistDirectory.length === 0) {
    throw new Error('Verified Electron distribution directory is required');
  }
  const validatedTarget = validateTarget(target);
  return [
    '--mac',
    ...(validatedTarget === 'dir' ? ['--dir'] : ['dmg']),
    '--arm64',
    '--publish',
    'never',
    `-c.electronDist=${electronDistDirectory}`,
    ...(outputDirectory ? [`-c.directories.output=${outputDirectory}`] : [])
  ];
}

/**
 * Signing posture from the environment: an explicit identity SHA-1 selects
 * Developer ID signing through electron-builder (`CSC_NAME`); otherwise the
 * build is unsigned and automatic identity discovery is disabled so a
 * developer keychain can never be picked up by accident.
 */
export function signingEnvironment(env) {
  const identity = env[SIGNING_IDENTITY_SHA1_ENV];
  if (identity !== undefined && identity !== '') {
    if (!/^[A-F0-9]{40}$/u.test(identity)) {
      throw new Error(`${SIGNING_IDENTITY_SHA1_ENV} must be an uppercase SHA-1 identity`);
    }
    return { CSC_NAME: identity, CSC_IDENTITY_AUTO_DISCOVERY: 'true' };
  }
  return { CSC_IDENTITY_AUTO_DISCOVERY: 'false' };
}

async function isRegularFile(filePath) {
  const info = await lstat(filePath).catch(() => undefined);
  return Boolean(info?.isFile() && !info.isSymbolicLink());
}

/**
 * Fail before electron-builder when an input is missing: every
 * `extraResources.from` must exist, the Codex tree must carry its executable,
 * and the built bundles must be present.
 */
export async function assertPackagingInputs({ root = frontendRoot, packageJson } = {}) {
  const manifest = packageJson ?? JSON.parse(await readFile(path.join(root, 'package.json'), 'utf8'));
  const failures = [];
  for (const relativePath of REQUIRED_BUILD_INPUTS) {
    if (!(await isRegularFile(path.join(root, relativePath)))) {
      failures.push(`missing build input ${relativePath}`);
    }
  }
  const extraResources = manifest?.build?.extraResources ?? [];
  for (const resource of extraResources) {
    const from = typeof resource === 'string' ? resource : resource?.from;
    if (typeof from !== 'string') {
      failures.push('extraResources entry without a source path');
      continue;
    }
    const info = await lstat(path.join(root, from)).catch(() => undefined);
    if (!info) failures.push(`missing extraResources source ${from}`);
  }
  const codexResource = extraResources.find((resource) => resource?.to === 'codex');
  if (!codexResource) {
    failures.push('extraResources does not stage the Codex platform tree at "codex"');
  } else {
    const executable = path.join(root, codexResource.from, 'bin', 'codex');
    const info = await lstat(executable).catch(() => undefined);
    if (!info?.isFile() || info.isSymbolicLink() || (info.mode & 0o111) === 0) {
      failures.push(`Codex executable is missing or not executable: ${path.join(codexResource.from, 'bin', 'codex')}`);
    }
    if (!(await isRegularFile(path.join(root, codexResource.from, 'bin', 'codex-code-mode-host')))) {
      failures.push(`Codex code-mode host is missing: ${path.join(codexResource.from, 'bin', 'codex-code-mode-host')}`);
    }
  }
  const pinned = manifest?.dependencies?.['@openai/codex'];
  if (typeof pinned !== 'string' || !/^\d+\.\d+\.\d+$/u.test(pinned)) {
    failures.push('package.json must pin @openai/codex to an exact version');
  }
  if (failures.length > 0) {
    throw new Error(`Packaging inputs are incomplete: ${failures.join('; ')}`);
  }
  return { extraResources, codexVersion: pinned };
}

function spawnAndWait(command, args, options, spawnProcess) {
  return new Promise((resolve, reject) => {
    const child = spawnProcess(command, args, options);
    child.once('error', reject);
    child.once('exit', (code, signal) => {
      if (code === 0) {
        resolve();
        return;
      }
      reject(
        new Error(
          signal
            ? `electron-builder terminated by signal ${signal}`
            : `electron-builder exited with status ${String(code)}`
        )
      );
    });
  });
}

/**
 * @param {{
 *   verify?: typeof verifyElectronDist,
 *   spawnProcess?: typeof spawn,
 *   assertInputs?: typeof assertPackagingInputs,
 *   env?: NodeJS.ProcessEnv,
 *   target?: string
 * }} [options]
 */
export async function runElectronPack({
  verify = verifyElectronDist,
  spawnProcess = spawn,
  assertInputs = assertPackagingInputs,
  env = process.env,
  target = 'dir'
} = {}) {
  const validatedTarget = validateTarget(target);
  const outputDirectory = resolveElectronOutputDirectory(env);
  const signing = signingEnvironment(env);
  await assertInputs();
  const electronDistDirectory = await verify();
  const args = buildElectronBuilderArgs(electronDistDirectory, validatedTarget, outputDirectory);
  await spawnAndWait('electron-builder', args, {
    stdio: 'inherit',
    shell: false,
    env: { ...env, ...signing }
  }, spawnProcess);
  return { appPath: expectedPackagedAppPath(outputDirectory), target: validatedTarget, signed: 'CSC_NAME' in signing };
}

export function parseArgs(argv) {
  const parsed = { target: 'dir' };
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (flag === '--target' && value !== undefined) parsed.target = validateTarget(value);
    else throw new Error('Usage: node ./scripts/pack-electron.mjs [--target dir|dmg]');
  }
  return parsed;
}

const isMain =
  process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;
if (isMain) {
  try {
    const result = await runElectronPack(parseArgs(process.argv.slice(2)));
    process.stdout.write(`${JSON.stringify(result)}\n`);
  } catch (error) {
    process.stderr.write(`Electron packaging failed: ${error.message}\n`);
    process.exitCode = 1;
  }
}
