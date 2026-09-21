import { execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { lstat, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { promisify } from 'node:util';

/**
 * `desktop:verify-codex-pin` (D-GOV-43, A2): the packaged stock Codex is the
 * one the lockfile resolved.
 *
 * Three facts are compared: the packaged `codex --version` output against the
 * lockfile-resolved `@openai/codex` version (which must also equal the exact
 * `package.json` pin); the sha256 of the packaged `codex` and
 * `codex-code-mode-host` against the binaries of the installed platform
 * package; and the `codex-package.json` staged with the tree. Signing changes
 * a Mach-O's bytes, so the digest comparison runs on the unsigned pack
 * (`desktop:pack`) and is recorded again after signing with `--after-signing`,
 * which skips the digest check and keeps the version check.
 */

const execFileAsync = promisify(execFile);
const frontendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const ELECTRON_OUTPUT_DIRECTORY_ENV = 'CHIRALITY_ELECTRON_OUTPUT_DIRECTORY';
export const CODEX_PACKAGE_NAME = '@openai/codex';
export const COMPARED_BINARIES = Object.freeze(['bin/codex', 'bin/codex-code-mode-host']);

const TARGET_TRIPLES = Object.freeze({
  'darwin-arm64': 'aarch64-apple-darwin',
  'darwin-x64': 'x86_64-apple-darwin',
  'linux-arm64': 'aarch64-unknown-linux-musl',
  'linux-x64': 'x86_64-unknown-linux-musl',
  'win32-arm64': 'aarch64-pc-windows-msvc',
  'win32-x64': 'x86_64-pc-windows-msvc'
});

export function resolveInstalledCodexVendorRoot(root, platform = process.platform, arch = process.arch) {
  const triple = TARGET_TRIPLES[`${platform}-${arch}`];
  if (!triple) throw new Error(`Unsupported Codex platform: ${platform} (${arch})`);
  return path.join(root, 'node_modules', '@openai', `codex-${platform}-${arch}`, 'vendor', triple);
}

export function resolvePackagedResourcesRoot(env = process.env, root = frontendRoot) {
  let outputDirectory = path.join(root, 'dist');
  if (Object.prototype.hasOwnProperty.call(env, ELECTRON_OUTPUT_DIRECTORY_ENV)) {
    const candidate = env[ELECTRON_OUTPUT_DIRECTORY_ENV];
    if (typeof candidate !== 'string' || candidate.length === 0 || candidate.includes('\0')
      || !path.isAbsolute(candidate) || path.normalize(candidate) !== candidate) {
      throw new Error(`${ELECTRON_OUTPUT_DIRECTORY_ENV} must be a normalized absolute path`);
    }
    outputDirectory = candidate;
  }
  return path.join(outputDirectory, 'mac-arm64', 'Chirality.app', 'Contents', 'Resources');
}

/** The lockfile-resolved version of the umbrella package and of this host's platform package. */
export function readLockfileCodexVersions(lockfile, platform = process.platform, arch = process.arch) {
  const packages = lockfile?.packages ?? {};
  const umbrella = packages[`node_modules/${CODEX_PACKAGE_NAME}`];
  if (typeof umbrella?.version !== 'string') {
    throw new Error(`package-lock.json does not resolve ${CODEX_PACKAGE_NAME}`);
  }
  const platformKey = `node_modules/@openai/codex-${platform}-${arch}`;
  const platformPackage = packages[platformKey];
  if (typeof platformPackage?.version !== 'string') {
    throw new Error(`package-lock.json does not resolve ${platformKey}`);
  }
  const expectedPlatformVersion = `${umbrella.version}-${platform}-${arch}`;
  if (platformPackage.version !== expectedPlatformVersion || platformPackage.name !== CODEX_PACKAGE_NAME) {
    throw new Error(`${platformKey} resolves ${platformPackage.name}@${platformPackage.version}, expected ${CODEX_PACKAGE_NAME}@${expectedPlatformVersion}`);
  }
  return { version: umbrella.version, platformVersion: platformPackage.version, platformKey };
}

export function parseCodexVersionOutput(output) {
  const match = /^codex-cli\s+(\S+)\s*$/mu.exec(String(output).trim());
  if (!match) throw new Error(`Unrecognised codex --version output: ${JSON.stringify(String(output).trim())}`);
  return match[1];
}

export async function hashFile(filePath) {
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(filePath)) hash.update(chunk);
  return hash.digest('hex');
}

/**
 * @param {{
 *   root?: string,
 *   resourcesRoot?: string,
 *   platform?: string,
 *   arch?: string,
 *   afterSigning?: boolean,
 *   runVersion?: (executable: string) => Promise<string>,
 *   hash?: typeof hashFile
 * }} [options]
 */
export async function verifyCodexPin({
  root = frontendRoot,
  resourcesRoot = resolvePackagedResourcesRoot(process.env, root),
  platform = process.platform,
  arch = process.arch,
  afterSigning = false,
  runVersion = async (executable) => (await execFileAsync(executable, ['--version'])).stdout,
  hash = hashFile
} = {}) {
  const failures = [];
  const packageJson = JSON.parse(await readFile(path.join(root, 'package.json'), 'utf8'));
  const lockfile = JSON.parse(await readFile(path.join(root, 'package-lock.json'), 'utf8'));
  const pinned = packageJson.dependencies?.[CODEX_PACKAGE_NAME];
  const locked = readLockfileCodexVersions(lockfile, platform, arch);
  if (pinned !== locked.version) {
    failures.push(`package.json pins ${CODEX_PACKAGE_NAME}@${String(pinned)} but the lockfile resolves ${locked.version}`);
  }

  const packagedVendorRoot = path.join(path.resolve(resourcesRoot), 'codex');
  const installedVendorRoot = resolveInstalledCodexVendorRoot(root, platform, arch);
  const packagedExecutable = path.join(packagedVendorRoot, 'bin', platform === 'win32' ? 'codex.exe' : 'codex');

  let packagedVersion = null;
  try {
    packagedVersion = parseCodexVersionOutput(await runVersion(packagedExecutable));
    if (packagedVersion !== locked.version) {
      failures.push(`packaged codex reports ${packagedVersion}, lockfile resolves ${locked.version}`);
    }
  } catch (error) {
    failures.push(`packaged codex --version failed: ${error.message}`);
  }

  let stagedManifest = null;
  try {
    stagedManifest = JSON.parse(await readFile(path.join(packagedVendorRoot, 'codex-package.json'), 'utf8'));
    if (stagedManifest.version !== locked.version) {
      failures.push(`staged codex-package.json records ${String(stagedManifest.version)}, lockfile resolves ${locked.version}`);
    }
  } catch (error) {
    failures.push(`staged codex-package.json unreadable: ${error.message}`);
  }

  const binaries = [];
  for (const relativePath of COMPARED_BINARIES) {
    const packaged = path.join(packagedVendorRoot, relativePath);
    const installed = path.join(installedVendorRoot, relativePath);
    const record = { relativePath, packagedSha256: null, installedSha256: null, matches: null };
    try {
      const info = await lstat(packaged);
      if (!info.isFile() || info.isSymbolicLink()) throw new Error('not a regular file');
      record.packagedSha256 = await hash(packaged);
    } catch (error) {
      failures.push(`packaged ${relativePath} unreadable: ${error.message}`);
    }
    try {
      record.installedSha256 = await hash(installed);
    } catch (error) {
      failures.push(`installed ${relativePath} unreadable: ${error.message}`);
    }
    if (record.packagedSha256 && record.installedSha256) {
      record.matches = record.packagedSha256 === record.installedSha256;
      if (!record.matches && !afterSigning) {
        failures.push(`packaged ${relativePath} sha256 differs from the installed ${CODEX_PACKAGE_NAME} platform package`);
      }
    }
    binaries.push(record);
  }

  return {
    status: failures.length === 0 ? 'PASS' : 'FAIL',
    afterSigning,
    packageJsonPin: pinned ?? null,
    lockfileVersion: locked.version,
    lockfilePlatformPackage: `${locked.platformKey}@${locked.platformVersion}`,
    packagedVersion,
    stagedTarget: stagedManifest?.target ?? null,
    packagedExecutable,
    installedVendorRoot,
    binaries,
    failures
  };
}

export function parseArgs(argv) {
  const parsed = { afterSigning: false };
  for (const argument of argv) {
    if (argument === '--after-signing') parsed.afterSigning = true;
    else throw new Error('Usage: node ./scripts/verify-codex-pin.mjs [--after-signing]');
  }
  return parsed;
}

const isMain =
  process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;
if (isMain) {
  try {
    const summary = await verifyCodexPin(parseArgs(process.argv.slice(2)));
    process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
    if (summary.status !== 'PASS') process.exitCode = 1;
  } catch (error) {
    process.stderr.write(`Codex pin verification failed: ${error.message}\n`);
    process.exitCode = 1;
  }
}
