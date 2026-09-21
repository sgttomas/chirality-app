import { EventEmitter } from 'node:events';
import { writeFileSync } from 'node:fs';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';

import {
  EXIT_REFUSED,
  SYFT_PIN,
  assertPinIsExact,
  assertPinnedSyftVersion,
  buildSyftEnvironment,
  buildSyftScanArgs,
  describeEnvironment,
  parseArgs,
  parseSyftVersionOutput,
  runCli,
  syftSourceFor
} from '../../../scripts/generate-sbom.mjs';

type SpawnCall = { command: string; args: string[]; options: Record<string, unknown> };

function fakeSpawn(
  calls: SpawnCall[],
  behaviour: (command: string, args: string[]) => { code: number; stdout?: string; stderr?: string } | 'ENOENT'
) {
  return (command: string, args: string[], options: Record<string, unknown>) => {
    calls.push({ command, args, options });
    const child = new EventEmitter() as EventEmitter & { stdout: EventEmitter; stderr: EventEmitter };
    child.stdout = new EventEmitter();
    child.stderr = new EventEmitter();
    queueMicrotask(() => {
      const outcome = behaviour(command, args);
      if (outcome === 'ENOENT') {
        const error = Object.assign(new Error('spawn syft ENOENT'), { code: 'ENOENT' });
        child.emit('error', error);
        return;
      }
      if (outcome.stdout) {
        child.stdout.emit('data', Buffer.from(outcome.stdout));
      }
      if (outcome.stderr) {
        child.stderr.emit('data', Buffer.from(outcome.stderr));
      }
      child.emit('close', outcome.code, null);
    });
    return child;
  };
}

const tempDirectories: string[] = [];

async function makeFrontendRoot(): Promise<string> {
  const root = await mkdtemp(path.join(tmpdir(), 'chirality-sbom-test-'));
  tempDirectories.push(root);
  await writeFile(path.join(root, 'package.json'), JSON.stringify({ name: 'fixture-app', version: '9.9.9' }));
  await writeFile(path.join(root, 'package-lock.json'), JSON.stringify({ lockfileVersion: 3, packages: { '': {} } }));
  return root;
}

afterEach(async () => {
  await Promise.all(tempDirectories.splice(0).map((directory) => rm(directory, { recursive: true, force: true })));
});

describe('generate-sbom pin and version parsing', () => {
  it('pins an exact Syft release whose tag matches its version', () => {
    expect(SYFT_PIN.version).toMatch(/^\d+\.\d+\.\d+$/);
    expect(SYFT_PIN.tag).toBe(`v${SYFT_PIN.version}`);
    expect(assertPinIsExact(SYFT_PIN)).toBe(SYFT_PIN);
    expect(() => assertPinIsExact({ tag: 'v1.2', version: '1.2' })).toThrow(/exact semantic version/);
    expect(() => assertPinIsExact({ tag: 'v9.9.9', version: '1.2.3' })).toThrow(/must equal "v1.2.3"/);
  });

  it('parses multi-line and single-line syft version output', () => {
    expect(
      parseSyftVersionOutput(`Application: syft\nVersion:     ${SYFT_PIN.version}\nBuildDate:   2024-01-01\n`)
    ).toEqual({ version: SYFT_PIN.version });
    expect(parseSyftVersionOutput(`syft ${SYFT_PIN.version}\n`)).toEqual({ version: SYFT_PIN.version });
    expect(parseSyftVersionOutput('Version: v2.0.0')).toEqual({ version: '2.0.0' });
    expect(parseSyftVersionOutput('no version here')).toBeNull();
    expect(parseSyftVersionOutput(undefined as never)).toBeNull();
  });

  it('refuses a mismatched or unreadable Syft version', () => {
    expect(assertPinnedSyftVersion({ version: SYFT_PIN.version })).toBe(SYFT_PIN.version);
    expect(() => assertPinnedSyftVersion({ version: '0.0.1' })).toThrow(/version mismatch/);
    expect(() => assertPinnedSyftVersion(null)).toThrow(/unable to read a Syft version/);
  });
});

describe('generate-sbom scan planning', () => {
  it('uses explicit dir:/file: schemes and absolute paths only', () => {
    expect(syftSourceFor('directory', '/tmp/Chirality.app')).toBe('dir:/tmp/Chirality.app');
    expect(syftSourceFor('file', '/tmp/package-lock.json')).toBe('file:/tmp/package-lock.json');
    expect(() => syftSourceFor('directory', 'relative/path')).toThrow(/absolute/);
    expect(() => syftSourceFor('socket', '/tmp/x')).toThrow(/unsupported/);
  });

  it('builds CycloneDX JSON scan arguments in a fixed order', () => {
    expect(
      buildSyftScanArgs({
        source: 'dir:/tmp/Chirality.app',
        outputPath: '/tmp/out/sbom.cdx.json',
        sourceName: 'chirality-frontend',
        sourceVersion: '3.0.0-rc.1'
      })
    ).toEqual([
      'scan',
      'dir:/tmp/Chirality.app',
      '--output',
      'cyclonedx-json=/tmp/out/sbom.cdx.json',
      '--quiet',
      '--source-name',
      'chirality-frontend',
      '--source-version',
      '3.0.0-rc.1'
    ]);
    expect(() => buildSyftScanArgs({ source: '/tmp/x', outputPath: '/tmp/o.json' })).toThrow(/dir: or file:/);
    expect(() => buildSyftScanArgs({ source: 'dir:/tmp/x', outputPath: 'o.json' })).toThrow(/absolute/);
  });

  it('constructs a minimal environment with update checks and dev dependencies disabled', () => {
    const env = buildSyftEnvironment({ PATH: '/usr/bin', HOME: '/Users/x', SECRET_TOKEN: 'never', TMPDIR: '/tmp' });
    expect(env).toEqual({
      SYFT_CHECK_FOR_APP_UPDATE: 'false',
      SYFT_JAVASCRIPT_INCLUDE_DEV_DEPENDENCIES: 'false',
      PATH: '/usr/bin',
      HOME: '/Users/x',
      TMPDIR: '/tmp'
    });
    expect(describeEnvironment(env)).toEqual({
      HOME: '<inherited from host>',
      PATH: '<inherited from host>',
      SYFT_CHECK_FOR_APP_UPDATE: 'false',
      SYFT_JAVASCRIPT_INCLUDE_DEV_DEPENDENCIES: 'false',
      TMPDIR: '<inherited from host>'
    });
  });

  it('parses arguments and refuses ambiguous or incomplete modes', () => {
    const parsed = parseArgs(['--closure', '--output', '/tmp/o.json', '--syft-bin', '/opt/syft']);
    expect(parsed.closure).toBe(true);
    expect(parsed.output).toBe('/tmp/o.json');
    expect(parsed.syftBin).toBe('/opt/syft');
    expect(() => parseArgs(['--closure', '--artifact', '/tmp/a'])).toThrow(/exactly one/);
    expect(() => parseArgs(['--output', '/tmp/o.json'])).toThrow(/exactly one/);
    expect(() => parseArgs(['--closure'])).toThrow(/--output/);
    expect(() => parseArgs(['--closure', '--bogus'])).toThrow(/Unknown option/);
    expect(parseArgs(['--closure', '--dry-run']).output).toMatch(/sbom\.cdx\.json$/);
  });
});

describe('generate-sbom CLI refusal paths', () => {
  it('refuses when the installed Syft version does not match the pin and never scans', async () => {
    const root = await makeFrontendRoot();
    const calls: SpawnCall[] = [];
    const stdout: string[] = [];
    const stderr: string[] = [];
    const code = await runCli({
      argv: ['--closure', '--root', root, '--output', path.join(root, 'sbom.cdx.json')],
      stdout: { write: (text: string) => stdout.push(text) },
      stderr: { write: (text: string) => stderr.push(text) },
      spawnProcess: fakeSpawn(calls, () => ({ code: 0, stdout: 'Application: syft\nVersion: 0.0.1\n' })) as never
    });
    expect(code).toBe(EXIT_REFUSED);
    expect(stderr.join('')).toMatch(/version mismatch/);
    expect(calls).toHaveLength(1);
    expect(calls[0]?.args).toEqual(['version']);
    expect(calls[0]?.options.shell).toBe(false);
  });

  it('refuses when Syft is not installed and states that it does not download it', async () => {
    const root = await makeFrontendRoot();
    const calls: SpawnCall[] = [];
    const stderr: string[] = [];
    const code = await runCli({
      argv: ['--closure', '--root', root, '--output', path.join(root, 'sbom.cdx.json')],
      stdout: { write: () => undefined },
      stderr: { write: (text: string) => stderr.push(text) },
      spawnProcess: fakeSpawn(calls, () => 'ENOENT') as never
    });
    expect(code).toBe(EXIT_REFUSED);
    expect(stderr.join('')).toMatch(/not found/);
    expect(stderr.join('')).toMatch(/does not download/);
    expect(calls).toHaveLength(1);
  });

  it('dry-run reports the exact pinned command without spawning anything', async () => {
    const root = await makeFrontendRoot();
    const calls: SpawnCall[] = [];
    const stdout: string[] = [];
    const code = await runCli({
      argv: ['--closure', '--root', root, '--dry-run'],
      stdout: { write: (text: string) => stdout.push(text) },
      stderr: { write: () => undefined },
      spawnProcess: fakeSpawn(calls, () => ({ code: 0 })) as never
    });
    expect(code).toBe(0);
    expect(calls).toHaveLength(0);
    const summary = JSON.parse(stdout.join('')) as {
      status: string;
      pinnedSyft: { tag: string };
      args: string[];
      env: Record<string, string>;
      subject: { mode: string };
    };
    expect(summary.status).toBe('DRY_RUN');
    expect(summary.pinnedSyft.tag).toBe(SYFT_PIN.tag);
    expect(summary.subject.mode).toBe('closure');
    expect(summary.args[0]).toBe('scan');
    expect(summary.args[1]).toBe(`file:${path.join(root, 'package-lock.json')}`);
    expect(summary.args).toContain('--source-version');
    expect(summary.args).toContain('9.9.9');
    expect(summary.env.SYFT_CHECK_FOR_APP_UPDATE).toBe('false');
    expect(summary.env.PATH).toBe('<inherited from host>');
  });

  it('runs the pinned scan and reports the CycloneDX output identity when Syft matches', async () => {
    const root = await makeFrontendRoot();
    const outputPath = path.join(root, 'sbom.cdx.json');
    const calls: SpawnCall[] = [];
    const stdout: string[] = [];
    const code = await runCli({
      argv: ['--closure', '--root', root, '--output', outputPath],
      stdout: { write: (text: string) => stdout.push(text) },
      stderr: { write: () => undefined },
      spawnProcess: fakeSpawn(calls, (_command, args) => {
        if (args[0] === 'version') {
          return { code: 0, stdout: `Application: syft\nVersion: ${SYFT_PIN.version}\n` };
        }
        writeFileSync(
          outputPath,
          JSON.stringify({ bomFormat: 'CycloneDX', specVersion: '1.5', components: [{ name: 'a' }] })
        );
        return { code: 0 };
      }) as never
    });
    expect(code).toBe(0);
    expect(calls).toHaveLength(2);
    expect(calls[1]?.args).toContain(`cyclonedx-json=${outputPath}`);
    const summary = JSON.parse(stdout.join('')) as {
      status: string;
      syftVersion: string;
      sbom: { bomFormat: string; componentCount: number; sha256: string };
    };
    expect(summary.status).toBe('PASS');
    expect(summary.syftVersion).toBe(SYFT_PIN.version);
    expect(summary.sbom.bomFormat).toBe('CycloneDX');
    expect(summary.sbom.componentCount).toBe(1);
    expect(summary.sbom.sha256).toMatch(/^[0-9a-f]{64}$/);
  });
});
