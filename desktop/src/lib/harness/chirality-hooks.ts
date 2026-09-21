import type {
  HookCallback,
  HookCallbackMatcher,
  HookEvent,
  HookInput,
  HookJSONOutput,
  PostToolUseFailureHookInput,
  PostToolUseHookInput,
  PreToolUseHookInput
} from '@anthropic-ai/claude-agent-sdk';
import { createHash } from 'node:crypto';
import { lstat, readFile } from 'node:fs/promises';
import { createHarnessEvent } from './event-factory';
import { appendHarnessEvent } from './session-events';
import {
  summarizeToolDescriptor,
  summarizeToolError,
  summarizeToolInput,
  summarizeShellResultStreams,
  summarizeToolResult,
  withToolResultPersistence
} from './tool-evidence';
import { persistToolResultArtifact } from './tool-result-artifacts';
import { evaluateToolPathPolicy, type HarnessToolPathPolicyAllow } from './tool-path-policy';
import {
  DEFAULT_BASH_TIMEOUT_MS,
  evaluateShellCommandPolicy
} from './tool-shell-policy';
import { getHarnessToolDescriptor, type HarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';
import { evaluateSubagentPreflight } from './subagent-bridge';

const WRITE_HOOK_TIMEOUT_SECONDS = 5;
const SHELL_HOOK_TIMEOUT_SECONDS = 5;
const HASH_INLINE_LIMIT_BYTES = 1024 * 1024;

type ToolAttemptRecord = {
  policyMetadata?: Record<string, unknown>;
  pathMetadata?: HarnessToolPathPolicyAllow;
  beforeState?: FileStateSummary;
  beforeTextForDiff?: string;
};

type FileStateSummary = {
  exists: boolean;
  kind?: 'file' | 'directory' | 'other';
  byteLength?: number;
  sha256?: string;
  hashOmittedReason?: string;
  error?: string;
};

type FileStateCapture = {
  summary: FileStateSummary;
  textForDiff?: string;
};

type FileDiffSummary = {
  beforeExists: boolean;
  afterExists: boolean;
  beforeByteLength?: number;
  afterByteLength?: number;
  byteDelta?: number;
  beforeLineCount?: number;
  afterLineCount?: number;
  addedLineCount?: number;
  removedLineCount?: number;
  diffAlgorithm?: 'bounded-lcs';
  diffOmittedReason?: string;
};

type ExactEditPreconditionResult =
  | {
      allowed: true;
      metadata: {
        preconditionClass: 'exact-edit';
        oldStringByteLength: number;
        oldStringMatchCount: number;
      };
    }
  | {
      allowed: false;
      reason: string;
      metadata: {
        denyClass: 'exact-edit-precondition';
        reason: string;
        oldStringByteLength?: number;
        beforeState?: FileStateSummary;
      };
    };

export type ChiralityToolHookInput = {
  sessionId: string;
  projectRoot: string;
  instructionRoot?: string;
  allowedReadScopes?: readonly string[];
  allowedWriteTargets?: readonly string[];
  delegatedSubagents?: readonly string[];
  resolveDescriptor?: (toolName: string) => HarnessToolDescriptor | undefined;
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function isWorkspaceWriteDescriptor(descriptor: HarnessToolDescriptor | undefined): boolean {
  return Boolean(descriptor?.permissions.includes('workspace-write'));
}

function isShellDescriptor(descriptor: HarnessToolDescriptor | undefined): boolean {
  return Boolean(descriptor?.permissions.includes('shell'));
}

function isSubagentDescriptor(descriptor: HarnessToolDescriptor | undefined): boolean {
  return Boolean(descriptor?.permissions.includes('subagent'));
}

function isEditFileDescriptor(descriptor: HarnessToolDescriptor | undefined): boolean {
  return descriptor?.name === 'edit_file';
}

function isGovernedHookDescriptor(descriptor: HarnessToolDescriptor | undefined): boolean {
  return (
    isWorkspaceWriteDescriptor(descriptor) || isShellDescriptor(descriptor) || isSubagentDescriptor(descriptor)
  );
}

function getHookFamily(descriptor: HarnessToolDescriptor | undefined): 'shell' | 'write' | 'subagent' {
  if (isSubagentDescriptor(descriptor)) {
    return 'subagent';
  }
  return isShellDescriptor(descriptor) ? 'shell' : 'write';
}

function readToolInput(input: HookInput): Record<string, unknown> {
  if (
    (input.hook_event_name === 'PreToolUse' ||
      input.hook_event_name === 'PostToolUse' ||
      input.hook_event_name === 'PostToolUseFailure') &&
    isRecord(input.tool_input)
  ) {
    return input.tool_input;
  }

  return {};
}

function countOccurrences(value: string, searchValue: string): number {
  let count = 0;
  let offset = 0;
  while (offset <= value.length) {
    const index = value.indexOf(searchValue, offset);
    if (index === -1) {
      break;
    }
    count += 1;
    offset = index + searchValue.length;
  }
  return count;
}

async function captureFileState(filePath: string | undefined): Promise<FileStateCapture | undefined> {
  if (!filePath) {
    return undefined;
  }

  try {
    const stats = await lstat(filePath);
    if (stats.isSymbolicLink()) {
      return {
        summary: {
          exists: true,
          kind: 'other',
          hashOmittedReason: 'symbolic-link'
        }
      };
    }
    if (stats.isDirectory()) {
      return {
        summary: {
          exists: true,
          kind: 'directory'
        }
      };
    }
    if (!stats.isFile()) {
      return {
        summary: {
          exists: true,
          kind: 'other'
        }
      };
    }
    const summary: FileStateSummary = {
      exists: true,
      kind: 'file',
      byteLength: stats.size
    };
    if (stats.size > HASH_INLINE_LIMIT_BYTES) {
      return {
        summary: {
          ...summary,
          hashOmittedReason: 'file-too-large'
        }
      };
    }
    const content = await readFile(filePath);
    return {
      summary: {
        ...summary,
        sha256: createHash('sha256').update(content).digest('hex')
      },
      textForDiff: content.toString('utf8')
    };
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
      return {
        summary: {
          exists: false
        },
        textForDiff: ''
      };
    }
    return {
      summary: {
        exists: false,
        error: error instanceof Error ? error.message : 'unknown file-state failure'
      }
    };
  }
}

function evaluateExactEditPrecondition(input: {
  toolInput: Record<string, unknown>;
  beforeCapture?: FileStateCapture;
}): ExactEditPreconditionResult {
  const oldString = input.toolInput.old_string;
  if (typeof oldString !== 'string' || oldString.length === 0) {
    return {
      allowed: false,
      reason: 'Edit old_string must be a non-empty string before Chirality can approve execution.',
      metadata: {
        denyClass: 'exact-edit-precondition',
        reason: 'missing-or-empty-old-string',
        beforeState: input.beforeCapture?.summary
      }
    };
  }

  if (typeof input.beforeCapture?.textForDiff !== 'string') {
    return {
      allowed: false,
      reason:
        'Edit old_string precondition could not be verified against the target file before execution.',
      metadata: {
        denyClass: 'exact-edit-precondition',
        reason: 'before-text-unavailable',
        oldStringByteLength: Buffer.byteLength(oldString, 'utf8'),
        beforeState: input.beforeCapture?.summary
      }
    };
  }

  const oldStringMatchCount = countOccurrences(input.beforeCapture.textForDiff, oldString);
  if (oldStringMatchCount === 0) {
    return {
      allowed: false,
      reason: 'Edit old_string was not found in the target file before execution.',
      metadata: {
        denyClass: 'exact-edit-precondition',
        reason: 'old-string-not-found',
        oldStringByteLength: Buffer.byteLength(oldString, 'utf8'),
        beforeState: input.beforeCapture.summary
      }
    };
  }

  return {
    allowed: true,
    metadata: {
      preconditionClass: 'exact-edit',
      oldStringByteLength: Buffer.byteLength(oldString, 'utf8'),
      oldStringMatchCount
    }
  };
}

function splitLinesForSummary(value: string): string[] {
  if (value.length === 0) {
    return [];
  }
  return value.endsWith('\n')
    ? value.slice(0, -1).split(/\r\n|\n|\r/)
    : value.split(/\r\n|\n|\r/);
}

function longestCommonSubsequenceLength(
  beforeLines: readonly string[],
  afterLines: readonly string[]
): number | undefined {
  const cellCount = beforeLines.length * afterLines.length;
  if (cellCount > 250_000) {
    return undefined;
  }

  let previous = new Array(afterLines.length + 1).fill(0) as number[];
  for (let beforeIndex = 0; beforeIndex < beforeLines.length; beforeIndex += 1) {
    const current = new Array(afterLines.length + 1).fill(0) as number[];
    for (let afterIndex = 0; afterIndex < afterLines.length; afterIndex += 1) {
      current[afterIndex + 1] =
        beforeLines[beforeIndex] === afterLines[afterIndex]
          ? previous[afterIndex] + 1
          : Math.max(previous[afterIndex + 1], current[afterIndex]);
    }
    previous = current;
  }
  return previous[afterLines.length];
}

function summarizeFileDiff(input: {
  beforeState?: FileStateSummary;
  beforeTextForDiff?: string;
  afterState?: FileStateSummary;
  afterTextForDiff?: string;
}): FileDiffSummary | undefined {
  const beforeState = input.beforeState;
  const afterState = input.afterState;
  if (!beforeState && !afterState) {
    return undefined;
  }

  const summary: FileDiffSummary = {
    beforeExists: beforeState?.exists ?? false,
    afterExists: afterState?.exists ?? false,
    beforeByteLength: beforeState?.byteLength,
    afterByteLength: afterState?.byteLength,
    byteDelta:
      typeof afterState?.byteLength === 'number' || typeof beforeState?.byteLength === 'number'
        ? (afterState?.byteLength ?? 0) - (beforeState?.byteLength ?? 0)
        : undefined
  };

  if (typeof input.beforeTextForDiff !== 'string' || typeof input.afterTextForDiff !== 'string') {
    return {
      ...summary,
      diffOmittedReason:
        beforeState?.hashOmittedReason ??
        afterState?.hashOmittedReason ??
        beforeState?.error ??
        afterState?.error ??
        'diff-text-unavailable'
    };
  }

  const beforeLines = splitLinesForSummary(input.beforeTextForDiff);
  const afterLines = splitLinesForSummary(input.afterTextForDiff);
  const commonLineCount = longestCommonSubsequenceLength(beforeLines, afterLines);
  if (commonLineCount === undefined) {
    return {
      ...summary,
      beforeLineCount: beforeLines.length,
      afterLineCount: afterLines.length,
      diffOmittedReason: 'line-count-diff-too-large'
    };
  }

  return {
    ...summary,
    beforeLineCount: beforeLines.length,
    afterLineCount: afterLines.length,
    addedLineCount: afterLines.length - commonLineCount,
    removedLineCount: beforeLines.length - commonLineCount,
    diffAlgorithm: 'bounded-lcs'
  };
}

async function appendHookEvent(input: {
  sessionId: string;
  type: 'hook.started' | 'hook.completed' | 'hook.failed';
  hookName: string;
  hookEvent: HookEvent;
  toolName?: string;
  toolUseId?: string;
  descriptor?: HarnessToolDescriptor;
  data?: Record<string, unknown>;
}): Promise<void> {
  await appendHarnessEvent(
    createHarnessEvent({
      sessionId: input.sessionId,
      type: input.type,
      data: {
        hookName: input.hookName,
        hookEvent: input.hookEvent,
        toolName: input.toolName,
        toolUseId: input.toolUseId,
        ...summarizeToolDescriptor(input.descriptor),
        ...input.data
      }
    })
  );
}

function allowPreToolUse(updatedInput?: Record<string, unknown>): HookJSONOutput {
  return {
    continue: true,
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'allow',
      updatedInput
    }
  };
}

function blockPreToolUse(reason: string): HookJSONOutput {
  return {
    continue: false,
    decision: 'block',
    reason,
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason: reason
    }
  };
}

export function createChiralityToolHooks(input: ChiralityToolHookInput): Partial<
  Record<HookEvent, HookCallbackMatcher[]>
> {
  const attempts = new Map<string, ToolAttemptRecord>();
  const resolveDescriptor = input.resolveDescriptor ?? getHarnessToolDescriptor;

  const preToolUse: HookCallback = async (hookInput) => {
    if (hookInput.hook_event_name !== 'PreToolUse') {
      return { continue: true };
    }

    const preInput = hookInput as PreToolUseHookInput;
    const descriptor = resolveDescriptor(preInput.tool_name);
    if (descriptor === undefined) {
      return blockPreToolUse(
        `Tool '${preInput.tool_name}' is not admitted by the current Runtime turn context.`
      );
    }
    if (!isGovernedHookDescriptor(descriptor)) {
      return { continue: true };
    }

    const hookFamily = getHookFamily(descriptor);
    const hookName = `chirality.${hookFamily}.pre_tool_use`;
    const eventBase = {
      sessionId: input.sessionId,
      hookName,
      hookEvent: 'PreToolUse' as const,
      toolName: preInput.tool_name,
      toolUseId: preInput.tool_use_id,
      descriptor
    };

    try {
      await appendHookEvent({
        ...eventBase,
        type: 'hook.started',
        data: {
          inputMetadata: summarizeToolInput(preInput.tool_input)
        }
      });

      if (isSubagentDescriptor(descriptor)) {
        const preflight = evaluateSubagentPreflight({
          toolInput: readToolInput(preInput),
          eligibleAgentNames: input.delegatedSubagents
        });

        await appendHookEvent({
          ...eventBase,
          type: 'hook.completed',
          data: {
            decision: preflight.allowed ? 'approve' : 'block',
            reason: preflight.reason,
            safeMetadata: preflight.safeMetadata
          }
        });
        return preflight.allowed ? allowPreToolUse() : blockPreToolUse(preflight.reason);
      }

      if (isShellDescriptor(descriptor)) {
        const shellPolicy = await evaluateShellCommandPolicy({
          descriptor,
          projectRoot: input.projectRoot,
          instructionRoot: input.instructionRoot,
          toolInput: readToolInput(preInput),
          allowedReadScopes: input.allowedReadScopes,
          allowedWriteTargets: input.allowedWriteTargets
        });

        if (!shellPolicy.allowed) {
          await appendHookEvent({
            ...eventBase,
            type: 'hook.completed',
            data: {
              decision: 'block',
              reason: shellPolicy.reason,
              safeMetadata: shellPolicy.metadata
            }
          });
          return blockPreToolUse(shellPolicy.reason);
        }

        attempts.set(preInput.tool_use_id, {
          policyMetadata: shellPolicy.metadata
        });

        await appendHookEvent({
          ...eventBase,
          type: 'hook.completed',
          data: {
            decision: 'approve',
            shellMetadata: shellPolicy.metadata,
            defaultTimeoutMs: DEFAULT_BASH_TIMEOUT_MS,
            resultBudget: descriptor?.resultBudget
          }
        });
        return allowPreToolUse(shellPolicy.updatedInput);
      }

      const pathPolicy = await evaluateToolPathPolicy({
        descriptor,
        projectRoot: input.projectRoot,
        instructionRoot: input.instructionRoot,
        toolInput: readToolInput(preInput),
        allowedReadScopes: input.allowedReadScopes,
        allowedWriteTargets: input.allowedWriteTargets
      });

      if (!pathPolicy.allowed) {
        await appendHookEvent({
          ...eventBase,
          type: 'hook.completed',
          data: {
            decision: 'block',
            reason: pathPolicy.reason,
            safeMetadata: pathPolicy.metadata
          }
        });
        return blockPreToolUse(pathPolicy.reason);
      }

      const beforeCapture = await captureFileState(pathPolicy.metadata.resolvedPath);
      const exactEditPrecondition = isEditFileDescriptor(descriptor)
        ? evaluateExactEditPrecondition({
            toolInput: readToolInput(preInput),
            beforeCapture
          })
        : undefined;

      if (exactEditPrecondition && !exactEditPrecondition.allowed) {
        await appendHookEvent({
          ...eventBase,
          type: 'hook.completed',
          data: {
            decision: 'block',
            reason: exactEditPrecondition.reason,
            pathMetadata: pathPolicy.metadata,
            beforeState: beforeCapture?.summary,
            safeMetadata: exactEditPrecondition.metadata
          }
        });
        return blockPreToolUse(exactEditPrecondition.reason);
      }

      attempts.set(preInput.tool_use_id, {
        pathMetadata: pathPolicy.metadata,
        beforeState: beforeCapture?.summary,
        beforeTextForDiff: beforeCapture?.textForDiff
      });

      await appendHookEvent({
        ...eventBase,
        type: 'hook.completed',
        data: {
          decision: 'approve',
          pathMetadata: pathPolicy.metadata,
          beforeState: beforeCapture?.summary,
          exactEditPrecondition: exactEditPrecondition?.metadata,
          recordsDiff: descriptor?.provenance.recordsDiff
        }
      });
      return allowPreToolUse();
    } catch (error) {
      const message = error instanceof Error ? error.message : 'unknown governed hook failure';
      try {
        await appendHookEvent({
          ...eventBase,
          type: 'hook.failed',
          data: {
            error: summarizeToolError(error),
            decision: 'block'
          }
        });
      } catch {
        // The pre-tool hook still fails closed if audit persistence is unavailable.
      }
      return blockPreToolUse(`Chirality ${hookFamily} hook failed closed. ${message}`);
    }
  };

  const postToolUse: HookCallback = async (hookInput) => {
    if (hookInput.hook_event_name !== 'PostToolUse') {
      return { continue: true };
    }

    const postInput = hookInput as PostToolUseHookInput;
    const descriptor = resolveDescriptor(postInput.tool_name);
    if (!isGovernedHookDescriptor(descriptor)) {
      return { continue: true };
    }

    const hookFamily = getHookFamily(descriptor);
    const hookName = `chirality.${hookFamily}.post_tool_use`;
    const attempt = attempts.get(postInput.tool_use_id);
    await appendHookEvent({
      sessionId: input.sessionId,
      type: 'hook.started',
      hookName,
      hookEvent: 'PostToolUse',
      toolName: postInput.tool_name,
      toolUseId: postInput.tool_use_id,
      descriptor
    });

    const afterCapture = isShellDescriptor(descriptor)
      ? undefined
      : await captureFileState(attempt?.pathMetadata?.resolvedPath);
    const artifactMetadata = await persistToolResultArtifact({
      sessionId: input.sessionId,
      toolUseId: postInput.tool_use_id,
      toolName: postInput.tool_name,
      descriptor,
      result: postInput.tool_response
    });
    const resultMetadata = withToolResultPersistence(
      summarizeToolResult(postInput.tool_response, descriptor),
      Boolean(artifactMetadata)
    );
    const diffSummary =
      descriptor?.provenance.recordsDiff === true
        ? summarizeFileDiff({
            beforeState: attempt?.beforeState,
            beforeTextForDiff: attempt?.beforeTextForDiff,
            afterState: afterCapture?.summary,
            afterTextForDiff: afterCapture?.textForDiff
          })
        : undefined;
    await appendHookEvent({
      sessionId: input.sessionId,
      type: 'hook.completed',
      hookName,
      hookEvent: 'PostToolUse',
      toolName: postInput.tool_name,
      toolUseId: postInput.tool_use_id,
      descriptor,
      data: {
        shellMetadata: attempt?.policyMetadata,
        pathMetadata: attempt?.pathMetadata,
        beforeState: attempt?.beforeState,
        afterState: afterCapture?.summary,
        durationMs: postInput.duration_ms,
        resultMetadata,
        shellResultMetadata: isShellDescriptor(descriptor)
          ? summarizeShellResultStreams(postInput.tool_response)
          : undefined,
        artifactMetadata,
        recordsDiff: descriptor?.provenance.recordsDiff,
        diffSummary
      }
    });
    attempts.delete(postInput.tool_use_id);
    return {
      continue: true,
      hookSpecificOutput: {
        hookEventName: 'PostToolUse'
      }
    };
  };

  const postToolUseFailure: HookCallback = async (hookInput) => {
    if (hookInput.hook_event_name !== 'PostToolUseFailure') {
      return { continue: true };
    }

    const failureInput = hookInput as PostToolUseFailureHookInput;
    const descriptor = resolveDescriptor(failureInput.tool_name);
    if (!isGovernedHookDescriptor(descriptor)) {
      return { continue: true };
    }

    const attempt = attempts.get(failureInput.tool_use_id);
    const hookFamily = getHookFamily(descriptor);
    await appendHookEvent({
      sessionId: input.sessionId,
      type: 'hook.failed',
      hookName: `chirality.${hookFamily}.post_tool_use_failure`,
      hookEvent: 'PostToolUseFailure',
      toolName: failureInput.tool_name,
      toolUseId: failureInput.tool_use_id,
      descriptor,
      data: {
        shellMetadata: attempt?.policyMetadata,
        pathMetadata: attempt?.pathMetadata,
        beforeState: attempt?.beforeState,
        durationMs: failureInput.duration_ms,
        error: failureInput.error,
        interrupted: failureInput.is_interrupt
      }
    });
    attempts.delete(failureInput.tool_use_id);
    return {
      continue: true,
      hookSpecificOutput: {
        hookEventName: 'PostToolUseFailure'
      }
    };
  };

  return {
    PreToolUse: [
      {
        timeout: Math.max(WRITE_HOOK_TIMEOUT_SECONDS, SHELL_HOOK_TIMEOUT_SECONDS),
        hooks: [preToolUse]
      }
    ],
    PostToolUse: [
      {
        timeout: Math.max(WRITE_HOOK_TIMEOUT_SECONDS, SHELL_HOOK_TIMEOUT_SECONDS),
        hooks: [postToolUse]
      }
    ],
    PostToolUseFailure: [
      {
        timeout: Math.max(WRITE_HOOK_TIMEOUT_SECONDS, SHELL_HOOK_TIMEOUT_SECONDS),
        hooks: [postToolUseFailure]
      }
    ]
  };
}
