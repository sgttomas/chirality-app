import { rm } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { build } from 'esbuild';

const frontendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repositoryRoot = path.resolve(frontendRoot, '..', '..', '..');
const runtimeRoot = path.join(repositoryRoot, 'projects', 'chirality-runtime');

export function resolveRuntimeContractsSource(subpath = '') {
  if (subpath.length === 0) {
    return path.join(runtimeRoot, 'packages', 'contracts', 'src', 'index.ts');
  }
  return path.join(
    runtimeRoot,
    'packages',
    'contracts',
    'src',
    subpath === 'v3' ? 'v3.ts' : path.join('harness', `${subpath}.ts`)
  );
}

export function resolveRuntimePhysicalFilesystemSource() {
  return path.join(runtimeRoot, 'packages', 'core', 'src', 'physical-filesystem.ts');
}

/** The App-owned Runtime service entry (`chirality-runtime-service daemon --config`). */
export function resolveRuntimeServiceEntrySource() {
  return path.join(runtimeRoot, 'packages', 'daemon', 'src', 'standalone-bin.ts');
}

export function resolveRuntimeCliEntrySource() {
  return path.join(runtimeRoot, 'packages', 'cli', 'src', 'bin.ts');
}

/** Output layout consumed by `package.json` `build.extraResources`. */
export const RUNTIME_BUNDLE_OUTPUTS = Object.freeze({
  service: path.join('dist-runtime', 'runtime-service', 'standalone-bin.mjs'),
  cli: path.join('dist-runtime', 'runtime-cli', 'chirality-cli.mjs')
});

const runtimeEntries = {
  '@chirality/runtime-contracts': resolveRuntimeContractsSource(),
  '@chirality/runtime-core': path.join(runtimeRoot, 'packages', 'core', 'src', 'index.ts'),
  '@chirality/runtime-core/physical-filesystem': resolveRuntimePhysicalFilesystemSource(),
  '@chirality/runtime-daemon': path.join(runtimeRoot, 'packages', 'daemon', 'src', 'index.ts'),
  '@chirality/runtime-client': path.join(runtimeRoot, 'packages', 'client', 'src', 'index.ts'),
  '@chirality/runtime-cli': path.join(runtimeRoot, 'packages', 'cli', 'src', 'index.ts')
};

export const runtimePackagePlugin = {
  name: 'chirality-runtime-workspace',
  setup(buildApi) {
    buildApi.onResolve(
      { filter: /^@chirality\/runtime-contracts(?:\/(.+))?$/ },
      (args) => {
        const subpath = args.path.slice('@chirality/runtime-contracts'.length + 1);
        return {
          path: resolveRuntimeContractsSource(subpath)
        };
      }
    );
    for (const [packageName, entry] of Object.entries(runtimeEntries)) {
      if (packageName === '@chirality/runtime-contracts') continue;
      buildApi.onResolve(
        { filter: new RegExp(`^${packageName.replaceAll('/', '\\/')}$`) },
        () => ({ path: entry })
      );
    }
  }
};

/**
 * ESM bundles of the Runtime workspace still reach a few CommonJS-only
 * dependencies through `require`; give them a real one.
 */
const esmRequireBanner = {
  js: "import { createRequire as __chiralityCreateRequire } from 'node:module'; const require = __chiralityCreateRequire(import.meta.url);"
};

export async function buildElectron() {
  await rm(path.join(frontendRoot, 'dist-electron'), { recursive: true, force: true });
  await rm(path.join(frontendRoot, 'dist-runtime'), { recursive: true, force: true });

  await build({
    entryPoints: [path.join(frontendRoot, 'electron', 'main.ts')],
    outfile: path.join(frontendRoot, 'dist-electron', 'main.js'),
    bundle: true,
    platform: 'node',
    target: 'node24',
    format: 'cjs',
    sourcemap: true,
    plugins: [runtimePackagePlugin],
    external: ['electron', 'next'],
    logLevel: 'info'
  });

  await build({
    entryPoints: [path.join(frontendRoot, 'electron', 'preload.ts')],
    outfile: path.join(frontendRoot, 'dist-electron', 'preload.js'),
    bundle: true,
    platform: 'node',
    target: 'node24',
    format: 'cjs',
    sourcemap: true,
    external: ['electron'],
    logLevel: 'info'
  });

  // The Runtime service bundle is what the packaged App launches as its owned
  // child (`Contents/Resources/runtime-service/standalone-bin.mjs`).
  await build({
    entryPoints: [resolveRuntimeServiceEntrySource()],
    outfile: path.join(frontendRoot, RUNTIME_BUNDLE_OUTPUTS.service),
    bundle: true,
    platform: 'node',
    target: 'node24',
    format: 'esm',
    sourcemap: true,
    banner: esmRequireBanner,
    plugins: [runtimePackagePlugin],
    logLevel: 'info'
  });

  await build({
    entryPoints: [resolveRuntimeCliEntrySource()],
    outfile: path.join(frontendRoot, RUNTIME_BUNDLE_OUTPUTS.cli),
    bundle: true,
    platform: 'node',
    target: 'node24',
    format: 'esm',
    sourcemap: true,
    banner: esmRequireBanner,
    plugins: [runtimePackagePlugin],
    logLevel: 'info'
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  await buildElectron();
}
