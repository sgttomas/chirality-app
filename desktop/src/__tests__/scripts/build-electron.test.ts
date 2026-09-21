import path from 'node:path';
import { build } from 'esbuild';
import { describe, expect, it } from 'vitest';

import {
  RUNTIME_BUNDLE_OUTPUTS,
  resolveRuntimeCliEntrySource,
  resolveRuntimeContractsSource,
  resolveRuntimePhysicalFilesystemSource,
  resolveRuntimeServiceEntrySource,
  runtimePackagePlugin
} from '../../../scripts/build-electron.mjs';

describe('build Electron Runtime contract aliases', () => {
  it('resolves the v3 package export from the contracts source root', () => {
    expect(resolveRuntimeContractsSource('v3')).toBe(
      path.resolve(process.cwd(), '../../chirality-runtime/packages/contracts/src/v3.ts')
    );
  });

  it('keeps established Harness subpath exports under the Harness source directory', () => {
    expect(resolveRuntimeContractsSource('errors')).toBe(
      path.resolve(process.cwd(), '../../chirality-runtime/packages/contracts/src/harness/errors.ts')
    );
  });

  it('bundles the Runtime service from the standalone entry and the CLI from its bin', () => {
    expect(resolveRuntimeServiceEntrySource()).toBe(
      path.resolve(process.cwd(), '../../chirality-runtime/packages/daemon/src/standalone-bin.ts')
    );
    expect(resolveRuntimeCliEntrySource()).toBe(
      path.resolve(process.cwd(), '../../chirality-runtime/packages/cli/src/bin.ts')
    );
    expect(RUNTIME_BUNDLE_OUTPUTS).toEqual({
      service: path.join('dist-runtime', 'runtime-service', 'standalone-bin.mjs'),
      cli: path.join('dist-runtime', 'runtime-cli', 'chirality-cli.mjs')
    });
  });

  it('bundles the physical filesystem adapter in CJS and ESM while retaining Electron original-fs as a runtime lookup', async () => {
    expect(resolveRuntimePhysicalFilesystemSource()).toBe(
      path.resolve(process.cwd(), '../../chirality-runtime/packages/core/src/physical-filesystem.ts')
    );

    for (const format of ['cjs', 'esm'] as const) {
      const result = await build({
        stdin: {
          contents: "export { runtimePhysicalFilesystem } from '@chirality/runtime-core/physical-filesystem';",
          loader: 'ts',
          resolveDir: process.cwd(),
          sourcefile: `physical-filesystem-${format}.ts`
        },
        bundle: true,
        format,
        platform: 'node',
        target: 'node24',
        plugins: [runtimePackagePlugin],
        write: false
      });
      const output = result.outputFiles[0]?.text ?? '';
      expect(output).toContain('node:module');
      expect(output).toContain('process.execPath');
      expect(output).toContain('"original-fs"');
      expect(output).not.toContain('require("original-fs")');
      expect(output).not.toContain('from "original-fs"');
    }
  });
});
