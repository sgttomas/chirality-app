import type { CallToolResult } from '@modelcontextprotocol/sdk/types.js';
import type {
  HarnessToolDescriptor,
  HarnessToolPermission,
  HarnessToolProvenance
} from '@chirality/runtime-contracts/tool-descriptor';
import { getHarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { readFile, realpath, stat } from 'node:fs/promises';
import path from 'node:path';
import { z } from 'zod/v4';
import { createHarnessEvent } from './event-factory';
import {
  appendHarnessPermissionDecisionEvent,
  resolveHarnessPermissionDecision
} from './permission-overlay';
import { appendHarnessEvent } from './session-events';
import {
  summarizeToolDescriptor,
  summarizeToolError,
  summarizeToolInput,
  summarizeToolResult,
  withToolResultPersistence
} from './tool-evidence';
import { evaluateToolPathPolicy } from './tool-path-policy';
import { persistToolResultArtifact } from './tool-result-artifacts';

export type ChiralityJsonSchema = Record<string, unknown>;

export type ChiralityToolExecutionContext = {
  projectRoot: string;
  sessionId: string;
  turnId?: string;
  mode?: string;
  allowedReadScopes?: readonly string[];
  allowedWriteTargets?: readonly string[];
};

export type ChiralityToolPermissionMetadata = {
  descriptorName: string;
  permissions: readonly HarnessToolPermission[];
  pathScope: HarnessToolDescriptor['pathScope'];
  humanGate: HarnessToolDescriptor['humanGate'];
};

export type ChiralityToolEvidenceMetadata = HarnessToolProvenance & {
  source: 'chirality-tool-bridge';
  redactedPersistence: true;
};

export type ChiralityToolHandlerInput<TInput> = {
  input: TInput;
  context: ChiralityToolExecutionContext;
  toolUseId?: string;
  signal?: AbortSignal;
  resolvedPath?: string;
};

export type ChiralityToolDefinition<TInput = Record<string, unknown>> = {
  name: string;
  label: string;
  description: string;
  inputSchema: ChiralityJsonSchema;
  permission: ChiralityToolPermissionMetadata;
  evidence: ChiralityToolEvidenceMetadata;
  execute: (input: unknown, options?: {
    toolUseId?: string;
    signal?: AbortSignal;
  }) => Promise<CallToolResult>;
};

type CreateChiralityToolDefinitionInput<TInput> = {
  descriptor: HarnessToolDescriptor;
  context: ChiralityToolExecutionContext;
  label?: string;
  handler: (input: ChiralityToolHandlerInput<TInput>) => Promise<CallToolResult>;
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function abortError(): Error {
  const error = new Error('Tool execution was aborted.');
  error.name = 'AbortError';
  return error;
}

function throwIfAborted(signal: AbortSignal | undefined): void {
  if (signal?.aborted) {
    throw abortError();
  }
}

function failInvalidToolInput(toolName: string, error: z.ZodError): never {
  throw new HarnessError('INVALID_REQUEST', 400, `Invalid input for Chirality tool '${toolName}'.`, {
    toolName,
    issues: error.issues.map((issue) => ({
      code: issue.code,
      path: issue.path.map(String),
      message: issue.message
    }))
  });
}

function normalizeObjectJsonSchema(
  toolName: string,
  schema: ChiralityJsonSchema
): ChiralityJsonSchema {
  if (schema.type !== 'object' || !isRecord(schema.properties)) {
    throw new Error(`Chirality tool '${toolName}' must declare an object JSON schema.`);
  }
  return {
    ...schema,
    additionalProperties: false
  };
}

function titleFromName(name: string): string {
  return name
    .split('_')
    .filter(Boolean)
    .map((part) => `${part.charAt(0).toUpperCase()}${part.slice(1)}`)
    .join(' ');
}

function eventBase(input: {
  definition: Pick<ChiralityToolDefinition, 'name' | 'permission'>;
  descriptor: HarnessToolDescriptor;
}): Record<string, unknown> {
  return {
    source: 'chirality-tool-bridge',
    adapterToolName: input.definition.name,
    toolName: input.definition.permission.descriptorName,
    ...summarizeToolDescriptor(input.descriptor)
  };
}

export function createChiralityToolDefinition<TInput>(
  input: CreateChiralityToolDefinitionInput<TInput>
): ChiralityToolDefinition<TInput> {
  const descriptor = input.descriptor;
  if (!descriptor.runtime.exposedToModel) {
    throw new Error(`Chirality tool '${descriptor.name}' is not exposed to model runtimes.`);
  }
  const inputSchema = normalizeObjectJsonSchema(descriptor.name, descriptor.inputSchema);
  const validator = z.fromJSONSchema(inputSchema);
  const definitionMetadata = {
    name: descriptor.name,
    permission: {
      descriptorName: descriptor.name,
      permissions: [...descriptor.permissions],
      pathScope: descriptor.pathScope,
      humanGate: descriptor.humanGate
    }
  } as const;

  const definition: ChiralityToolDefinition<TInput> = {
    name: descriptor.name,
    label: input.label ?? titleFromName(descriptor.name),
    description: descriptor.description,
    inputSchema,
    permission: definitionMetadata.permission,
    evidence: {
      ...descriptor.provenance,
      source: 'chirality-tool-bridge',
      redactedPersistence: true
    },
    execute: async (rawInput, options = {}) => {
      throwIfAborted(options.signal);
      const parsed = validator.safeParse(rawInput);
      if (!parsed.success) {
        failInvalidToolInput(descriptor.name, parsed.error);
      }
      const toolInput = parsed.data as TInput;
      const pathPolicy = await evaluateToolPathPolicy({
        descriptor,
        projectRoot: input.context.projectRoot,
        toolInput,
        allowedReadScopes: input.context.allowedReadScopes,
        allowedWriteTargets: input.context.allowedWriteTargets
      });
      const decision = resolveHarnessPermissionDecision({
        sessionId: input.context.sessionId,
        turnId: input.context.turnId,
        mode: input.context.mode ?? 'readOnly',
        toolName: descriptor.name,
        descriptor,
        source: 'chirality-policy',
        toolInput: isRecord(toolInput) ? toolInput : undefined,
        explicitDeny: !pathPolicy.allowed,
        explicitDenyReason: pathPolicy.allowed ? undefined : pathPolicy.reason,
        safeMetadata: {
          inputMetadata: summarizeToolInput(toolInput),
          pathMetadata: pathPolicy.metadata
        }
      });
      await appendHarnessPermissionDecisionEvent({
        decision,
        descriptor,
        sdkToolUseId: options.toolUseId
      });
      if (decision.decision !== 'allow') {
        throw new HarnessError('INVALID_REQUEST', 403, decision.reason, {
          decisionId: decision.decisionId,
          decision: decision.decision,
          safeMetadata: decision.safeMetadata
        });
      }

      throwIfAborted(options.signal);
      const startedAt = Date.now();
      const base = eventBase({ definition: definitionMetadata, descriptor });
      await appendHarnessEvent(
        createHarnessEvent({
          sessionId: input.context.sessionId,
          turnId: input.context.turnId,
          type: 'tool.started',
          data: {
            ...base,
            toolUseId: options.toolUseId,
            permissionDecisionId: decision.decisionId,
            inputMetadata: summarizeToolInput(toolInput)
          }
        })
      );

      try {
        const result = await input.handler({
          input: toolInput,
          context: input.context,
          toolUseId: options.toolUseId,
          signal: options.signal,
          resolvedPath:
            pathPolicy.allowed && typeof pathPolicy.metadata.resolvedPath === 'string'
              ? pathPolicy.metadata.resolvedPath
              : undefined
        });
        throwIfAborted(options.signal);
        const artifactMetadata = await persistToolResultArtifact({
          sessionId: input.context.sessionId,
          turnId: input.context.turnId,
          toolUseId: options.toolUseId,
          toolName: descriptor.name,
          descriptor,
          result
        });
        await appendHarnessEvent(
          createHarnessEvent({
            sessionId: input.context.sessionId,
            turnId: input.context.turnId,
            type: 'tool.completed',
            data: {
              ...base,
              toolUseId: options.toolUseId,
              permissionDecisionId: decision.decisionId,
              durationMs: Date.now() - startedAt,
              resultMetadata: withToolResultPersistence(
                summarizeToolResult(result, descriptor),
                Boolean(artifactMetadata)
              ),
              artifactMetadata
            }
          })
        );
        return result;
      } catch (error) {
        try {
          await appendHarnessEvent(
            createHarnessEvent({
              sessionId: input.context.sessionId,
              turnId: input.context.turnId,
              type: 'tool.failed',
              data: {
                ...base,
                toolUseId: options.toolUseId,
                permissionDecisionId: decision.decisionId,
                failureSource: 'handler',
                durationMs: Date.now() - startedAt,
                error: summarizeToolError(error)
              }
            })
          );
        } catch {
          // Preserve the original handler failure when evidence persistence also fails.
        }
        throw error;
      }
    }
  };
  return definition;
}

type ReadFileInput = {
  file_path: string;
};

async function readProjectTextFile(
  input: ChiralityToolHandlerInput<ReadFileInput>,
  descriptor: HarnessToolDescriptor
): Promise<CallToolResult> {
  throwIfAborted(input.signal);
  const projectRoot = await realpath(path.resolve(input.context.projectRoot));
  const resolvedPath = await realpath(
    input.resolvedPath ?? path.resolve(projectRoot, input.input.file_path)
  );
  const relativePath = path.relative(projectRoot, resolvedPath);
  if (relativePath.startsWith('..') || path.isAbsolute(relativePath)) {
    throw new HarnessError('INVALID_REQUEST', 403, 'Read path resolves outside projectRoot.', {
      denyClass: 'path-containment'
    });
  }
  const fileStat = await stat(resolvedPath);
  if (!fileStat.isFile()) {
    throw new HarnessError('INVALID_REQUEST', 400, 'read_file requires a regular file.', {
      file_path: input.input.file_path
    });
  }
  if (fileStat.size > descriptor.resultBudget.artifactByteLimit) {
    throw new HarnessError('INVALID_REQUEST', 413, 'read_file exceeds the governed result budget.', {
      file_path: input.input.file_path,
      byteLength: fileStat.size,
      artifactByteLimit: descriptor.resultBudget.artifactByteLimit
    });
  }
  const content = await readFile(resolvedPath, 'utf8');
  throwIfAborted(input.signal);
  return {
    content: [
      {
        type: 'text',
        text: content
      }
    ]
  };
}

export function createBoundedReadToolDefinitions(input: {
  context: ChiralityToolExecutionContext;
  allowedToolNames: readonly string[];
}): ChiralityToolDefinition[] {
  const definitions: ChiralityToolDefinition[] = [];
  const seen = new Set<string>();
  for (const requestedName of input.allowedToolNames) {
    const descriptor = getHarnessToolDescriptor(requestedName);
    if (!descriptor || descriptor.name !== 'read_file') {
      throw new HarnessError(
        'INVALID_REQUEST',
        400,
        `Tool '${requestedName}' is not available in the bounded local read bridge.`,
        {
          requestedTool: requestedName,
          allowedTools: ['read_file']
        }
      );
    }
    if (seen.has(descriptor.name)) {
      continue;
    }
    seen.add(descriptor.name);
    const boundedDescriptor: HarnessToolDescriptor = {
      ...descriptor,
      inputSchema: {
        ...descriptor.inputSchema,
        additionalProperties: false,
        properties: {
          ...(isRecord(descriptor.inputSchema.properties)
            ? descriptor.inputSchema.properties
            : {}),
          file_path: {
            type: 'string',
            minLength: 1
          }
        }
      }
    };
    definitions.push(
      createChiralityToolDefinition<ReadFileInput>({
        descriptor: boundedDescriptor,
        context: input.context,
        label: 'Read File',
        handler: (handlerInput) => readProjectTextFile(handlerInput, boundedDescriptor)
      })
    );
  }
  return definitions;
}

export async function executeChiralityTool(input: {
  definitions: readonly ChiralityToolDefinition[];
  toolName: string;
  args: unknown;
  toolUseId?: string;
  signal?: AbortSignal;
}): Promise<CallToolResult> {
  const definition = input.definitions.find((candidate) => candidate.name === input.toolName);
  if (!definition) {
    throw new HarnessError('INVALID_REQUEST', 400, `Unknown bound Chirality tool '${input.toolName}'.`, {
      toolName: input.toolName,
      boundTools: input.definitions.map((candidate) => candidate.name)
    });
  }
  return definition.execute(input.args, {
    toolUseId: input.toolUseId,
    signal: input.signal
  });
}
