import { Buffer } from 'node:buffer';
import path from 'node:path';
import { resolveInstructionRootPath } from './instruction-root';
import { evaluateToolPathPolicy } from './tool-path-policy';
import type { HarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';

export const HARNESS_SHELL_POLICY_VERSION = 'harness-shell.v2.managed-child-scopes';
export const DEFAULT_BASH_TIMEOUT_MS = 120_000;
export const MAX_BASH_TIMEOUT_MS = 600_000;

export type HarnessShellPolicyResult =
  | {
      allowed: true;
      metadata: Record<string, unknown>;
      updatedInput?: Record<string, unknown>;
    }
  | {
      allowed: false;
      reason: string;
      metadata: Record<string, unknown>;
    };

const NETWORK_COMMANDS = new Set([
  'curl',
  'ftp',
  'nc',
  'netcat',
  'rsync',
  'scp',
  'sftp',
  'ssh',
  'telnet',
  'wget'
]);

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function readCommand(toolInput: unknown): string | undefined {
  if (!isRecord(toolInput) || typeof toolInput.command !== 'string') {
    return undefined;
  }
  const command = toolInput.command.trim();
  return command.length > 0 ? command : undefined;
}

function readTimeout(toolInput: unknown): number | undefined {
  if (!isRecord(toolInput) || typeof toolInput.timeout !== 'number') {
    return undefined;
  }
  return toolInput.timeout;
}

function readBoolean(toolInput: unknown, key: string): boolean {
  return isRecord(toolInput) && toolInput[key] === true;
}

function isWithinRoot(root: string, candidate: string): boolean {
  const relative = path.relative(path.resolve(root), path.resolve(candidate));
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function stripQuotes(value: string): string {
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }
  return value;
}

function firstCommandWord(command: string): string | undefined {
  const match = command.match(/^\s*(?:[A-Za-z_][A-Za-z0-9_]*=\S+\s+)*([A-Za-z0-9_.-]+)/);
  return match?.[1];
}

function extractRedirectionTargets(command: string): string[] {
  const targets: string[] = [];
  const pattern =
    /(?:^|[\s;|&])(?:\d*>>?|\d*&>|&>|>>?)(?:\s*)(?:"([^"]+)"|'([^']+)'|([^\s;&|<>]+))/g;
  for (const match of command.matchAll(pattern)) {
    const target = stripQuotes(match[1] ?? match[2] ?? match[3] ?? '').trim();
    if (target.length > 0 && !target.startsWith('&')) {
      targets.push(target);
    }
  }
  return targets;
}

function extractAbsolutePathTokens(command: string): string[] {
  const tokens: string[] = [];
  const pattern = /(?:^|[\s"'=])((?:\/[A-Za-z0-9._~:+@%-]+)+\/?)(?=$|[\s"',;|)])/g;
  for (const match of command.matchAll(pattern)) {
    const token = stripQuotes(match[1] ?? '').trim();
    if (token.length > 0) {
      tokens.push(token);
    }
  }
  return Array.from(new Set(tokens));
}

function createMetadata(input: {
  command: string;
  timeout?: number;
  effectiveTimeoutMs: number;
  timeoutSource: 'defaulted' | 'requested';
  redirectionTargets: string[];
  absolutePathTokens: string[];
  extra?: Record<string, unknown>;
}): Record<string, unknown> {
  return {
    shellPolicyVersion: HARNESS_SHELL_POLICY_VERSION,
    commandByteLength: Buffer.byteLength(input.command, 'utf8'),
    commandName: firstCommandWord(input.command),
    requestedTimeoutMs: input.timeout,
    effectiveTimeoutMs: input.effectiveTimeoutMs,
    timeoutSource: input.timeoutSource,
    defaultTimeoutMs: DEFAULT_BASH_TIMEOUT_MS,
    maxTimeoutMs: MAX_BASH_TIMEOUT_MS,
    redirectionCount: input.redirectionTargets.length,
    absolutePathTokenCount: input.absolutePathTokens.length,
    ...input.extra
  };
}

function deny(input: {
  command: string;
  reason: string;
  denyClass: string;
  timeout?: number;
  effectiveTimeoutMs: number;
  timeoutSource: 'defaulted' | 'requested';
  redirectionTargets?: string[];
  absolutePathTokens?: string[];
  extra?: Record<string, unknown>;
}): HarnessShellPolicyResult {
  return {
    allowed: false,
    reason: input.reason,
    metadata: createMetadata({
      command: input.command,
      timeout: input.timeout,
      effectiveTimeoutMs: input.effectiveTimeoutMs,
      timeoutSource: input.timeoutSource,
      redirectionTargets: input.redirectionTargets ?? [],
      absolutePathTokens: input.absolutePathTokens ?? [],
      extra: {
        denyClass: input.denyClass,
        ...input.extra
      }
    })
  };
}

export async function evaluateShellCommandPolicy(input: {
  descriptor?: HarnessToolDescriptor;
  projectRoot?: string;
  instructionRoot?: string;
  toolInput: unknown;
  allowedReadScopes?: readonly string[];
  allowedWriteTargets?: readonly string[];
}): Promise<HarnessShellPolicyResult> {
  const command = readCommand(input.toolInput);
  if (!command) {
    return {
      allowed: false,
      reason: 'Bash command is missing or empty.',
      metadata: {
        shellPolicyVersion: HARNESS_SHELL_POLICY_VERSION,
        denyClass: 'missing-command'
      }
    };
  }

  const timeout = readTimeout(input.toolInput);
  const timeoutSource = timeout === undefined ? 'defaulted' : 'requested';
  const effectiveTimeoutMs = timeout ?? DEFAULT_BASH_TIMEOUT_MS;
  const redirectionTargets = extractRedirectionTargets(command);
  const absolutePathTokens = extractAbsolutePathTokens(command);

  if (!input.projectRoot) {
    return deny({
      command,
      reason: 'Bash requires an active project root.',
      denyClass: 'project-root-missing',
      timeout,
      effectiveTimeoutMs,
      timeoutSource,
      redirectionTargets,
      absolutePathTokens
    });
  }

  if (input.allowedReadScopes !== undefined || input.allowedWriteTargets !== undefined) {
    const projectRoot = path.resolve(input.projectRoot);
    const fullRead = input.allowedReadScopes?.some((scope) => path.resolve(scope) === projectRoot) ?? false;
    const fullWrite = input.allowedWriteTargets?.some((scope) => path.resolve(scope) === projectRoot) ?? false;
    if (!fullRead || !fullWrite) {
      return deny({
        command,
        reason: 'Bash is denied for a managed child unless both declared read and write scope explicitly cover the project root; use bounded file tools or a deterministic registered tool instead.',
        denyClass: 'managed-shell-scope',
        timeout,
        effectiveTimeoutMs,
        timeoutSource,
        redirectionTargets,
        absolutePathTokens,
        extra: {
          allowedReadScopes: input.allowedReadScopes?.map((scope) => path.resolve(scope)) ?? [],
          allowedWriteTargets: input.allowedWriteTargets?.map((scope) => path.resolve(scope)) ?? []
        }
      });
    }
  }

  if (!Number.isInteger(effectiveTimeoutMs) || effectiveTimeoutMs <= 0) {
    return deny({
      command,
      reason: 'Bash timeout must be a positive integer number of milliseconds.',
      denyClass: 'invalid-timeout',
      timeout,
      effectiveTimeoutMs,
      timeoutSource,
      redirectionTargets,
      absolutePathTokens
    });
  }

  if (effectiveTimeoutMs > MAX_BASH_TIMEOUT_MS) {
    return deny({
      command,
      reason: `Bash timeout exceeds the maximum ${MAX_BASH_TIMEOUT_MS} ms policy.`,
      denyClass: 'timeout-too-large',
      timeout,
      effectiveTimeoutMs,
      timeoutSource,
      redirectionTargets,
      absolutePathTokens
    });
  }

  if (readBoolean(input.toolInput, 'dangerouslyDisableSandbox')) {
    return deny({
      command,
      reason: 'Bash sandbox override is not allowed by Chirality policy.',
      denyClass: 'sandbox-override',
      timeout,
      effectiveTimeoutMs,
      timeoutSource,
      redirectionTargets,
      absolutePathTokens
    });
  }

  if (readBoolean(input.toolInput, 'run_in_background')) {
    return deny({
      command,
      reason: 'Background Bash commands are not allowed by this tranche.',
      denyClass: 'background-command',
      timeout,
      effectiveTimeoutMs,
      timeoutSource,
      redirectionTargets,
      absolutePathTokens
    });
  }

  const commandName = firstCommandWord(command);
  if (commandName && NETWORK_COMMANDS.has(commandName)) {
    return deny({
      command,
      reason: `Network-capable Bash command '${commandName}' is outside current scope.`,
      denyClass: 'network-command',
      timeout,
      effectiveTimeoutMs,
      timeoutSource,
      redirectionTargets,
      absolutePathTokens
    });
  }

  if (/\b(?:https?|wss?|ftp):\/\//i.test(command)) {
    return deny({
      command,
      reason: 'Bash commands containing network URLs require a future governed scope.',
      denyClass: 'network-url',
      timeout,
      effectiveTimeoutMs,
      timeoutSource,
      redirectionTargets,
      absolutePathTokens
    });
  }

  if (/(^|[\s"'`=])\.\.(?:\/|$)/.test(command)) {
    return deny({
      command,
      reason: 'Bash commands containing parent-directory traversal are denied.',
      denyClass: 'path-traversal',
      timeout,
      effectiveTimeoutMs,
      timeoutSource,
      redirectionTargets,
      absolutePathTokens
    });
  }

  const instructionRoot = input.instructionRoot ?? resolveInstructionRootPath();
  for (const token of absolutePathTokens) {
    const resolved = path.resolve(token);
    if (!isWithinRoot(input.projectRoot, resolved)) {
      return deny({
        command,
        reason: `Bash path '${token}' resolves outside the active project root.`,
        denyClass: 'path-containment',
        timeout,
        effectiveTimeoutMs,
        timeoutSource,
        redirectionTargets,
        absolutePathTokens,
        extra: {
          resolvedPath: resolved
        }
      });
    }
    if (isWithinRoot(instructionRoot, resolved)) {
      return deny({
        command,
        reason: `Bash path '${token}' resolves under the instruction root.`,
        denyClass: 'instruction-root',
        timeout,
        effectiveTimeoutMs,
        timeoutSource,
        redirectionTargets,
        absolutePathTokens,
        extra: {
          resolvedPath: resolved,
          instructionRoot: path.resolve(instructionRoot)
        }
      });
    }
  }

  for (const target of redirectionTargets) {
    const pathPolicy = await evaluateToolPathPolicy({
      descriptor: input.descriptor,
      projectRoot: input.projectRoot,
      instructionRoot,
      toolInput: {
        path: target
      },
      allowedReadScopes: input.allowedReadScopes,
      allowedWriteTargets: input.allowedWriteTargets
    });
    if (!pathPolicy.allowed) {
      return deny({
        command,
        reason: pathPolicy.reason,
        denyClass: 'redirection-path',
        timeout,
        effectiveTimeoutMs,
        timeoutSource,
        redirectionTargets,
        absolutePathTokens,
        extra: pathPolicy.metadata
      });
    }
  }

  const updatedInput =
    timeout === undefined && isRecord(input.toolInput)
      ? {
          ...input.toolInput,
          timeout: DEFAULT_BASH_TIMEOUT_MS
        }
      : undefined;

  return {
    allowed: true,
    metadata: createMetadata({
      command,
      timeout,
      effectiveTimeoutMs,
      timeoutSource,
      redirectionTargets,
      absolutePathTokens
    }),
    updatedInput
  };
}
