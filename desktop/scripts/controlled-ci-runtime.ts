import path from 'node:path';
import { pathToFileURL } from 'node:url';
import {
  AuthRegistry,
  EngineRegistry,
  ProjectRegistry,
  ResidencyCoordinator,
  RuntimeService,
  SessionStore,
  TurnCoordinator
} from '@chirality/runtime-core';
import type { OmlxControlPort } from '@chirality/runtime-contracts';
import { RuntimeError } from '@chirality/runtime-contracts';
import { RuntimeDaemon } from '@chirality/runtime-daemon';
import { StubAgentSdkManager } from '../src/lib/harness/agent-sdk-manager';
import { LegacyAgentEngineAdapter } from '../src/lib/harness/engine-registry';

/**
 * Controlled CI Runtime fixture (D-GOV-43, A2).
 *
 * The release-quality wrapper needs a real Runtime daemon on a Unix socket so
 * the App's harness routes are exercised end to end, but CI has no Codex
 * executable and no sign-in. This entry composes `RuntimeDaemon` over
 * `RuntimeService` with the stub engine only: no `codex app-server`, no
 * App-owned composition, no Electron main. It registers one project from a
 * manifest with the fixture's own approval, then prints exactly one ready
 * line carrying the project token so the workflow needs no operator token
 * and no CLI registration step.
 */
export const CONTROLLED_CI_PURPOSE = 'chirality-controlled-ci-runtime/v1';
export const CONTROLLED_CI_APPROVED_BY = 'github-actions';
export const CONTROLLED_CI_APPROVAL_REFERENCE = 'harness-premerge-ci';

export type ControlledCiRuntimeOptions = {
  purpose: typeof CONTROLLED_CI_PURPOSE;
  runtimeDirectory: string;
  socketPath: string;
  instructionRoot: string;
  /** Absolute path of the `chirality.project.json` to register. */
  projectManifestPath: string;
  approvedBy?: string;
  approvalReference?: string;
};

export type ControlledCiRuntimeReady = {
  status: 'ready';
  purpose: typeof CONTROLLED_CI_PURPOSE;
  socketPath: string;
  /** The registered project's client token file (`project-<id>.token`). */
  tokenFile: string;
  projectId: string;
  /** The registered project's canonical working root. */
  projectRoot: string;
};

export function parseControlledCiReadyLine(line: string): ControlledCiRuntimeReady {
  const parsed: unknown = JSON.parse(line);
  if (!parsed || typeof parsed !== 'object') throw new Error('Controlled CI ready line is not an object.');
  const candidate = parsed as Partial<ControlledCiRuntimeReady>;
  if (candidate.status !== 'ready' || candidate.purpose !== CONTROLLED_CI_PURPOSE) {
    throw new Error('Controlled CI ready line does not declare the controlled purpose.');
  }
  for (const field of ['socketPath', 'tokenFile', 'projectId', 'projectRoot'] as const) {
    if (typeof candidate[field] !== 'string' || candidate[field]!.length === 0) {
      throw new Error(`Controlled CI ready line is missing ${field}.`);
    }
  }
  return candidate as ControlledCiRuntimeReady;
}

export async function startControlledCiRuntime(options: ControlledCiRuntimeOptions) {
  if (options.purpose !== CONTROLLED_CI_PURPOSE) {
    throw new Error('The controlled Runtime entry is available only for the declared CI test purpose.');
  }
  for (const [label, value] of Object.entries({
    runtimeDirectory: options.runtimeDirectory,
    socketPath: options.socketPath,
    instructionRoot: options.instructionRoot,
    projectManifestPath: options.projectManifestPath
  })) {
    if (!path.isAbsolute(value)) throw new Error(`${label} must be an absolute path.`);
  }

  const projects = new ProjectRegistry(options.runtimeDirectory, {
    CHIRALITY_INSTRUCTION_ROOT: options.instructionRoot
  });
  const sessions = new SessionStore(options.runtimeDirectory, projects);
  const engines = new EngineRegistry();
  engines.register(new LegacyAgentEngineAdapter({
    adapterId: 'stub',
    providerId: 'stub',
    capabilities: {
      credentials: false,
      tools: false,
      attachments: true,
      interruption: true,
      durableResume: false,
      compaction: false,
      runtimeControlTools: false
    }
  }, new StubAgentSdkManager()));
  const control: OmlxControlPort = {
    async listStatus() { return []; },
    async load() { throw new RuntimeError('ENGINE_UNAVAILABLE', 'Controlled CI runtime has no model control.', 503); },
    async unload() { throw new RuntimeError('ENGINE_UNAVAILABLE', 'Controlled CI runtime has no model control.', 503); }
  };
  const residency = new ResidencyCoordinator(control, options.runtimeDirectory);
  const auth = new AuthRegistry(options.runtimeDirectory);
  const turns = new TurnCoordinator(projects, sessions, engines, residency);
  const service = new RuntimeService(
    projects,
    sessions,
    engines,
    residency,
    turns,
    auth,
    {
      async get() { return undefined; },
      async status() { return { configured: false }; },
      async set() { throw new RuntimeError('ENGINE_UNAVAILABLE', 'Controlled CI runtime cannot configure credentials.', 503); },
      async remove() { throw new RuntimeError('ENGINE_UNAVAILABLE', 'Controlled CI runtime cannot configure credentials.', 503); }
    },
    undefined,
    undefined,
    undefined,
    {
      async resolve(input) {
        return {
          role: input.agentType === 0 ? 'agent0' as const : 'agent1' as const,
          engineSelection: { adapterId: 'stub', providerId: 'stub', model: 'controlled-ci' }
        };
      }
    }
  );
  const daemon = new RuntimeDaemon({
    runtimeDirectory: options.runtimeDirectory,
    socketPath: options.socketPath,
    service
  });
  const started = await daemon.start();
  try {
    const registration = await service.registerProject(
      options.projectManifestPath,
      options.approvedBy ?? CONTROLLED_CI_APPROVED_BY,
      options.approvalReference ?? CONTROLLED_CI_APPROVAL_REFERENCE
    );
    const project = await projects.requireAuthorized(registration.projectId);
    const ready: ControlledCiRuntimeReady = {
      status: 'ready',
      purpose: CONTROLLED_CI_PURPOSE,
      socketPath: started.socketPath,
      tokenFile: registration.tokenFile,
      projectId: registration.projectId,
      projectRoot: project.canonicalRoot
    };
    return { ...ready, daemon, stop: () => daemon.stop() };
  } catch (error) {
    await daemon.stop().catch(() => undefined);
    throw error;
  }
}

function requiredAbsoluteEnvironment(name: string): string {
  const value = process.env[name];
  if (!value || !path.isAbsolute(value)) throw new Error(`${name} must be an absolute path.`);
  return value;
}

/**
 * `--manifest <path>` names the project manifest to register; the only
 * argument the entry accepts. Anything else is refused so the fixture cannot
 * be mistaken for the product service or the CLI.
 */
export function parseControlledCiArguments(argv: readonly string[]): { manifestPath: string } {
  if (argv.length !== 2 || argv[0] !== '--manifest' || !argv[1]) {
    throw new Error('Usage: controlled-runtime.mjs --manifest <absolute path to chirality.project.json>');
  }
  if (!path.isAbsolute(argv[1])) throw new Error('--manifest must be an absolute path.');
  return { manifestPath: argv[1] };
}

async function main(): Promise<void> {
  if (process.env.CHIRALITY_CONTROLLED_CI_RUNTIME !== CONTROLLED_CI_PURPOSE) {
    throw new Error(`CHIRALITY_CONTROLLED_CI_RUNTIME must equal ${CONTROLLED_CI_PURPOSE}.`);
  }
  const { manifestPath } = parseControlledCiArguments(process.argv.slice(2));
  const host = await startControlledCiRuntime({
    purpose: CONTROLLED_CI_PURPOSE,
    runtimeDirectory: requiredAbsoluteEnvironment('CHIRALITY_RUNTIME_DIRECTORY'),
    socketPath: requiredAbsoluteEnvironment('CHIRALITY_RUNTIME_SOCKET_PATH'),
    instructionRoot: requiredAbsoluteEnvironment('CHIRALITY_INSTRUCTION_ROOT'),
    projectManifestPath: manifestPath
  });
  const ready: ControlledCiRuntimeReady = {
    status: 'ready',
    purpose: CONTROLLED_CI_PURPOSE,
    socketPath: host.socketPath,
    tokenFile: host.tokenFile,
    projectId: host.projectId,
    projectRoot: host.projectRoot
  };
  process.stdout.write(`${JSON.stringify(ready)}\n`);

  let stopping = false;
  const stop = (): void => {
    if (stopping) return;
    stopping = true;
    void host.stop().then(() => process.exit(0), (error) => {
      process.stderr.write(`${error instanceof Error ? error.stack ?? error.message : String(error)}\n`);
      process.exit(1);
    });
  };
  process.once('SIGINT', stop);
  process.once('SIGTERM', stop);
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  await main();
}
