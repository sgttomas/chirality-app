import type {
  SDKAssistantMessage,
  SDKCompactBoundaryMessage,
  SDKMessage,
  SDKMirrorErrorMessage,
  SDKPartialAssistantMessage,
  SDKPermissionDeniedMessage,
  SDKResultMessage,
  SDKSystemMessage
} from '@anthropic-ai/claude-agent-sdk';
import { createHarnessEvent } from './event-factory';
import { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import {
  childRunRecordToEventData,
  createAdapterObservedChildRunRecord,
  type ChildRunRecord,
  type ChildRunStatus
} from './agent-runtime-contract';
import { isChiralityMcpAllowedToolName } from '@chirality/runtime-contracts/mcp/tool-names';
import { redactJsonLike } from './run-logger';
import {
  isToolResultFailure,
  summarizeToolDescriptor,
  summarizeToolInput,
  summarizeShellResultStreams,
  summarizeToolResult,
  withToolResultPersistence
} from './tool-evidence';
import {
  persistChildOutputArtifact,
  persistToolResultArtifact
} from './tool-result-artifacts';
import { getHarnessToolDescriptor, type HarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';
import { UIEvent } from '@chirality/runtime-contracts/types';

export type SdkMessageMapping = {
  uiEvents: UIEvent[];
  harnessEvents: HarnessEvent[];
  sdkSessionId?: string;
  sdkClaudeCodeVersion?: string;
};

export type SdkToolEvidenceState = {
  toolNamesByUseId: Map<string, string>;
  startedToolUseIds: Set<string>;
  childRunContext?: SdkChildRunEvidenceContext;
  childRunRecordsByTaskId: Map<string, ChildRunRecord>;
};

export type SdkChildRunEvidenceContext = {
  parentPersona: string;
  projectRoot: string;
  mode: string;
  parentTurnId?: string;
};

export function createSdkToolEvidenceState(
  childRunContext?: SdkChildRunEvidenceContext
): SdkToolEvidenceState {
  return {
    toolNamesByUseId: new Map(),
    startedToolUseIds: new Set(),
    childRunContext,
    childRunRecordsByTaskId: new Map()
  };
}

function readTextFromContentBlock(block: unknown): string | undefined {
  if (!block || typeof block !== 'object') {
    return undefined;
  }
  const candidate = block as { type?: unknown; text?: unknown };
  return candidate.type === 'text' && typeof candidate.text === 'string'
    ? candidate.text
    : undefined;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function readString(value: unknown): string | undefined {
  return typeof value === 'string' && value.length > 0 ? value : undefined;
}

function readOptionalString(value: unknown): string | undefined {
  return typeof value === 'string' ? value : undefined;
}

function readSessionId(message: SDKMessage): string | undefined {
  return isRecord(message) ? readString(message.session_id) : undefined;
}

function readMessageId(message: SDKMessage): string | undefined {
  return isRecord(message) ? readString(message.uuid) : undefined;
}

function readTextFromUnknownContent(content: unknown): string {
  if (typeof content === 'string') {
    return content;
  }
  if (!Array.isArray(content)) {
    return '';
  }

  return content.map(readTextFromContentBlock).filter(Boolean).join('');
}

function readTextFromMessageParam(message: unknown): string {
  if (!isRecord(message)) {
    return '';
  }

  return readTextFromUnknownContent(message.content);
}

function readBlockTypes(content: unknown): string[] {
  if (!Array.isArray(content)) {
    return [];
  }

  return content
    .map((block) => (isRecord(block) ? readString(block.type) : undefined))
    .filter((type): type is string => Boolean(type));
}

type ToolUseEvidence = {
  toolUseId?: string;
  toolName?: string;
  input?: unknown;
};

function descriptorForToolName(toolName: string | undefined): HarnessToolDescriptor | undefined {
  return toolName ? getHarnessToolDescriptor(toolName) : undefined;
}

function isSdkBuiltinEvidenceDescriptor(descriptor: HarnessToolDescriptor | undefined): boolean {
  return (
    descriptor?.surface === 'claude-agent-sdk-builtin' &&
    (descriptor.permissions.includes('read') ||
      descriptor.permissions.includes('workspace-write') ||
      descriptor.permissions.includes('shell'))
  );
}

function isShellDescriptor(descriptor: HarnessToolDescriptor | undefined): boolean {
  return Boolean(descriptor?.permissions.includes('shell'));
}

function isChiralityMcpTool(toolName: string | undefined): boolean {
  const descriptor = descriptorForToolName(toolName);
  return Boolean(
    descriptor?.surface === 'chirality-mcp' ||
      (toolName && isChiralityMcpAllowedToolName(toolName))
  );
}

function registerQueuedToolUse(
  state: SdkToolEvidenceState | undefined,
  toolUse: ToolUseEvidence
): void {
  if (state && toolUse.toolUseId && toolUse.toolName) {
    state.toolNamesByUseId.set(toolUse.toolUseId, toolUse.toolName);
  }
}

function createToolEvidenceData(input: {
  source: string;
  toolUseId?: string;
  toolName?: string;
  descriptor?: HarnessToolDescriptor;
  extra?: Record<string, unknown>;
}): Record<string, unknown> {
  return {
    source: input.source,
    ...summarizeToolDescriptor(input.descriptor),
    adapterToolUseId: input.toolUseId,
    adapterToolName: input.toolName,
    toolUseId: input.toolUseId,
    toolName: input.toolName,
    ...input.extra
  };
}

function readTaskId(message: SDKMessage): string | undefined {
  const record = message as unknown as Record<string, unknown>;
  return readString(record['task_id']);
}

function readToolUseId(message: SDKMessage): string | undefined {
  const record = message as unknown as Record<string, unknown>;
  return readString(record['tool_use_id']);
}

function readChildAgentName(message: SDKMessage, prior?: ChildRunRecord): string {
  const record = message as unknown as Record<string, unknown>;
  return (
    readString(record['subagent_type']) ??
    readString(record['task_type']) ??
    readString(record['workflow_name']) ??
    prior?.agentName ??
    'UNKNOWN_CHILD_AGENT'
  );
}

function createChildRunRecordForTaskMessage(input: {
  sessionId: string;
  message: SDKMessage;
  state?: SdkToolEvidenceState;
  status: ChildRunStatus;
  outputArtifactPath?: string;
}): ChildRunRecord | undefined {
  const context = input.state?.childRunContext;
  if (!context) {
    return undefined;
  }

  const taskId = readTaskId(input.message);
  const prior = taskId ? input.state?.childRunRecordsByTaskId.get(taskId) : undefined;
  const record = createAdapterObservedChildRunRecord({
    parentSessionId: input.sessionId,
    parentPersona: context.parentPersona,
    agentName: readChildAgentName(input.message, prior),
    projectRoot: context.projectRoot,
    mode: context.mode,
    status: input.status,
    parentTurnId: context.parentTurnId,
    outputArtifactPath: input.outputArtifactPath ?? prior?.outputArtifactPath,
    adapter: {
      adapterName: 'claude-agent-sdk',
      adapterSessionId: readSessionId(input.message),
      adapterTaskId: taskId,
      adapterToolUseId: readToolUseId(input.message)
    }
  });

  if (taskId) {
    input.state?.childRunRecordsByTaskId.set(taskId, record);
  }
  return record;
}

function childRunEventData(record: ChildRunRecord | undefined): Record<string, unknown> {
  return record ? childRunRecordToEventData(record) : {};
}

function summarizeTaskPatch(patch: unknown): Record<string, unknown> | undefined {
  if (!isRecord(patch)) {
    return undefined;
  }
  return redactJsonLike({
    status: readString(patch.status),
    keys: Object.keys(patch).sort(),
    outputFilePresent: readString(patch.output_file) !== undefined,
    summaryPresent: readString(patch.summary) !== undefined,
    usagePresent: patch.usage !== undefined
  });
}

function createInferredToolStartedEvent(input: {
  sessionId: string;
  message: SDKMessage;
  state?: SdkToolEvidenceState;
  toolUseId?: string;
  toolName?: string;
  parentToolUseId?: unknown;
  inferredFrom: string;
}): HarnessEvent[] {
  if (!input.state || !input.toolUseId || input.state.startedToolUseIds.has(input.toolUseId)) {
    return [];
  }

  input.state.startedToolUseIds.add(input.toolUseId);
  const descriptor = descriptorForToolName(input.toolName);
  return [
    createSdkEvent(
      input.sessionId,
      input.message,
      'tool.started',
      createToolEvidenceData({
        source: 'adapter',
        toolUseId: input.toolUseId,
        toolName: input.toolName,
        descriptor,
        extra: {
          parentToolUseId: input.parentToolUseId,
          startInferredFrom: input.inferredFrom
        }
      })
    )
  ];
}

function readToolUsesFromContent(content: unknown): ToolUseEvidence[] {
  if (!Array.isArray(content)) {
    return [];
  }

  return content.flatMap((block) => {
    if (!isRecord(block)) {
      return [];
    }
    const type = readString(block.type);
    if (type !== 'tool_use' && type !== 'server_tool_use') {
      return [];
    }
    return [
      {
        toolUseId: readString(block.id),
        toolName: readString(block.name),
        input: block.input
      }
    ];
  });
}

function readToolUseFromStreamEvent(message: SDKPartialAssistantMessage): ToolUseEvidence | undefined {
  const event = message.event as unknown;
  if (!isRecord(event) || event.type !== 'content_block_start') {
    return undefined;
  }
  const contentBlock = event.content_block;
  if (!isRecord(contentBlock)) {
    return undefined;
  }
  const type = readString(contentBlock.type);
  if (type !== 'tool_use' && type !== 'server_tool_use') {
    return undefined;
  }

  return {
    toolUseId: readString(contentBlock.id),
    toolName: readString(contentBlock.name),
    input: contentBlock.input
  };
}

function sdkEvidence(message: SDKMessage, extra?: Record<string, unknown>): Record<string, unknown> {
  const sdkSessionId = readSessionId(message);
  return redactJsonLike({
    adapterName: 'claude-agent-sdk',
    adapterSessionId: sdkSessionId,
    adapterMessageId: readMessageId(message),
    sdkSessionId,
    ...extra
  });
}

function createSdkEvent(
  sessionId: string,
  message: SDKMessage,
  type: Parameters<typeof createHarnessEvent>[0]['type'],
  data?: Record<string, unknown>
): HarnessEvent {
  return createHarnessEvent({
    sessionId,
    type,
    data: sdkEvidence(message, data)
  });
}

function mapAssistantToolUses(
  sessionId: string,
  message: SDKAssistantMessage,
  state?: SdkToolEvidenceState
): HarnessEvent[] {
  const content = message.message.content;
  return readToolUsesFromContent(content).map((toolUse) => {
    registerQueuedToolUse(state, toolUse);
    const descriptor = descriptorForToolName(toolUse.toolName);
    return createSdkEvent(
      sessionId,
      message,
      'tool.queued',
      createToolEvidenceData({
        source: 'model',
        toolUseId: toolUse.toolUseId,
        toolName: toolUse.toolName,
        descriptor,
        extra: {
          inputMetadata: summarizeToolInput(toolUse.input)
        }
      })
    );
  });
}

function mapSdkUserToolResultEvents(
  sessionId: string,
  message: SDKMessage,
  state?: SdkToolEvidenceState
): HarnessEvent[] {
  const record = message as Record<string, unknown>;
  if (record.tool_use_result === undefined) {
    return [];
  }

  const result = record.tool_use_result;
  const resultRecord = isRecord(result) ? result : {};
  const toolUseId =
    readString(record.parent_tool_use_id) ?? readString(resultRecord.tool_use_id);
  const toolName = toolUseId ? state?.toolNamesByUseId.get(toolUseId) : undefined;
  const descriptor = descriptorForToolName(toolName);
  if (!toolUseId || isChiralityMcpTool(toolName) || !isSdkBuiltinEvidenceDescriptor(descriptor)) {
    return [];
  }

  const resultMetadata = summarizeToolResult(result, descriptor);
  const lifecycleEvents = createInferredToolStartedEvent({
    sessionId,
    message,
    state,
    toolUseId,
    toolName,
    parentToolUseId: record.parent_tool_use_id,
    inferredFrom: 'tool_use_result'
  });
  const eventType = isToolResultFailure(result) ? 'tool.failed' : 'tool.completed';
  lifecycleEvents.push(
    createSdkEvent(
      sessionId,
      message,
      eventType,
      createToolEvidenceData({
        source: 'adapter',
        toolUseId,
        toolName,
        descriptor,
        extra: {
          parentToolUseId: record.parent_tool_use_id,
          failureSource: eventType === 'tool.failed' ? 'tool_use_result' : undefined,
          resultMetadata,
          shellResultMetadata: isShellDescriptor(descriptor)
            ? summarizeShellResultStreams(result)
            : undefined
        }
      })
    )
  );
  return lifecycleEvents;
}

async function mapSdkUserToolResultEventsWithArtifacts(
  sessionId: string,
  message: SDKMessage,
  state?: SdkToolEvidenceState
): Promise<HarnessEvent[]> {
  const record = message as Record<string, unknown>;
  if (record.tool_use_result === undefined) {
    return [];
  }

  const result = record.tool_use_result;
  const resultRecord = isRecord(result) ? result : {};
  const toolUseId =
    readString(record.parent_tool_use_id) ?? readString(resultRecord.tool_use_id);
  const toolName = toolUseId ? state?.toolNamesByUseId.get(toolUseId) : undefined;
  const descriptor = descriptorForToolName(toolName);
  if (!toolUseId || isChiralityMcpTool(toolName) || !isSdkBuiltinEvidenceDescriptor(descriptor)) {
    return [];
  }

  const artifactMetadata = await persistToolResultArtifact({
    sessionId,
    turnId: state?.childRunContext?.parentTurnId,
    toolUseId,
    toolName,
    descriptor,
    result
  });
  const resultMetadata = withToolResultPersistence(
    summarizeToolResult(result, descriptor),
    Boolean(artifactMetadata)
  );
  const lifecycleEvents = createInferredToolStartedEvent({
    sessionId,
    message,
    state,
    toolUseId,
    toolName,
    parentToolUseId: record.parent_tool_use_id,
    inferredFrom: 'tool_use_result'
  });
  const eventType = isToolResultFailure(result) ? 'tool.failed' : 'tool.completed';
  lifecycleEvents.push(
    createSdkEvent(
      sessionId,
      message,
      eventType,
      createToolEvidenceData({
        source: 'adapter',
        toolUseId,
        toolName,
        descriptor,
        extra: {
          parentToolUseId: record.parent_tool_use_id,
          failureSource: eventType === 'tool.failed' ? 'tool_use_result' : undefined,
          resultMetadata,
          shellResultMetadata: isShellDescriptor(descriptor)
            ? summarizeShellResultStreams(result)
            : undefined,
          artifactMetadata
        }
      })
    )
  );
  return lifecycleEvents;
}

function mapSdkUserMessage(
  sessionId: string,
  message: SDKMessage,
  state?: SdkToolEvidenceState
): SdkMessageMapping {
  const record = message as Record<string, unknown>;
  const shouldQueue = record.shouldQuery === false || record.priority === 'next' || record.priority === 'later';
  const messageEvent = createSdkEvent(sessionId, message, 'message.completed', {
    role: 'user',
    source: record.isSynthetic ? 'synthetic' : 'operator',
    text: readTextFromMessageParam(record.message),
    blockTypes: isRecord(record.message) ? readBlockTypes(record.message.content) : [],
    priority: record.priority,
    shouldQuery: record.shouldQuery,
    synthetic: record.isSynthetic === true,
    origin: record.origin,
    parentToolUseId: record.parent_tool_use_id,
    toolUseResultPresent: record.tool_use_result !== undefined,
    timestamp: record.timestamp
  });
  const toolResultEvents = mapSdkUserToolResultEvents(sessionId, message, state);

  return {
    sdkSessionId: readSessionId(message),
    uiEvents: [],
    harnessEvents: shouldQueue
      ? [
          ...toolResultEvents,
          messageEvent,
          createSdkEvent(sessionId, message, 'queue.enqueued', {
            queueKind: record.priority ?? 'deferred',
            shouldQuery: record.shouldQuery,
            origin: record.origin
          })
        ]
      : [...toolResultEvents, messageEvent]
  };
}

async function mapSdkUserMessageWithArtifacts(
  sessionId: string,
  message: SDKMessage,
  state?: SdkToolEvidenceState
): Promise<SdkMessageMapping> {
  const record = message as Record<string, unknown>;
  const shouldQueue = record.shouldQuery === false || record.priority === 'next' || record.priority === 'later';
  const messageEvent = createSdkEvent(sessionId, message, 'message.completed', {
    role: 'user',
    source: record.isSynthetic ? 'synthetic' : 'operator',
    text: readTextFromMessageParam(record.message),
    blockTypes: isRecord(record.message) ? readBlockTypes(record.message.content) : [],
    priority: record.priority,
    shouldQuery: record.shouldQuery,
    synthetic: record.isSynthetic === true,
    origin: record.origin,
    parentToolUseId: record.parent_tool_use_id,
    toolUseResultPresent: record.tool_use_result !== undefined,
    timestamp: record.timestamp
  });
  const toolResultEvents = await mapSdkUserToolResultEventsWithArtifacts(
    sessionId,
    message,
    state
  );

  return {
    sdkSessionId: readSessionId(message),
    uiEvents: [],
    harnessEvents: shouldQueue
      ? [
          ...toolResultEvents,
          messageEvent,
          createSdkEvent(sessionId, message, 'queue.enqueued', {
            queueKind: record.priority ?? 'deferred',
            shouldQuery: record.shouldQuery,
            origin: record.origin
          })
        ]
      : [...toolResultEvents, messageEvent]
  };
}

function readAssistantText(message: SDKAssistantMessage): string {
  const content = message.message.content;
  if (!Array.isArray(content)) {
    return '';
  }

  return content.map(readTextFromContentBlock).filter(Boolean).join('');
}

function readPartialText(message: SDKPartialAssistantMessage): string {
  const event = message.event as unknown;
  if (!event || typeof event !== 'object') {
    return '';
  }

  const candidate = event as {
    type?: unknown;
    delta?: { type?: unknown; text?: unknown };
  };
  if (candidate.type === 'content_block_delta' && typeof candidate.delta?.text === 'string') {
    return candidate.delta.text;
  }
  return '';
}

function isSystemInit(message: SDKMessage): message is SDKSystemMessage {
  return message.type === 'system' && 'subtype' in message && message.subtype === 'init';
}

function isCompactBoundary(message: SDKMessage): message is SDKCompactBoundaryMessage {
  return message.type === 'system' && 'subtype' in message && message.subtype === 'compact_boundary';
}

function isPermissionDenied(message: SDKMessage): message is SDKPermissionDeniedMessage {
  return message.type === 'system' && 'subtype' in message && message.subtype === 'permission_denied';
}

function isMirrorError(message: SDKMessage): message is SDKMirrorErrorMessage {
  return message.type === 'system' && 'subtype' in message && message.subtype === 'mirror_error';
}

export function mapSdkMessageToHarness(
  sessionId: string,
  message: SDKMessage,
  state?: SdkToolEvidenceState
): SdkMessageMapping {
  if (message.type === 'user') {
    return mapSdkUserMessage(sessionId, message, state);
  }

  if (isSystemInit(message)) {
    return {
      sdkSessionId: message.session_id,
      sdkClaudeCodeVersion: message.claude_code_version,
      uiEvents: [
        {
          type: 'session:init',
          data: {
            engineSessionId: message.session_id,
            adapterId: 'claude-agent-sdk',
            providerId: 'anthropic',
            claudeSessionId: message.session_id,
            model: message.model
          }
        }
      ],
      harnessEvents: [
        createHarnessEvent({
          sessionId,
          type: 'adapter.initialized',
          data: sdkEvidence(message, {
            sdkClaudeCodeVersion: message.claude_code_version,
            model: message.model,
            tools: message.tools,
            mcpServers: message.mcp_servers,
            permissionMode: message.permissionMode
          })
        })
      ]
    };
  }

  if (message.type === 'stream_event') {
    const text = readPartialText(message);
    const toolUse = readToolUseFromStreamEvent(message);
    if (toolUse) {
      registerQueuedToolUse(state, toolUse);
    }
    return {
      sdkSessionId: message.session_id,
      uiEvents: text
        ? [
            {
              type: 'chat:delta',
              data: {
                text
              }
            }
          ]
        : [],
      harnessEvents: [
        ...(text
          ? [
              createSdkEvent(sessionId, message, 'model.delta', { text }),
              createSdkEvent(sessionId, message, 'message.delta', {
                role: 'assistant',
                source: 'model',
                text,
                parentToolUseId: message.parent_tool_use_id,
                timeToFirstTokenMs: message.ttft_ms
              })
            ]
          : []),
        ...(toolUse
          ? [
              createSdkEvent(sessionId, message, 'tool.queued', {
                source: 'model',
                ...summarizeToolDescriptor(descriptorForToolName(toolUse.toolName)),
                adapterToolUseId: toolUse.toolUseId,
                adapterToolName: toolUse.toolName,
                toolUseId: toolUse.toolUseId,
                toolName: toolUse.toolName,
                inputMetadata: summarizeToolInput(toolUse.input),
                parentToolUseId: message.parent_tool_use_id
              })
            ]
          : [])
      ]
    };
  }

  if (message.type === 'assistant') {
    const text = readAssistantText(message);
    const content = message.message.content;
    const toolUseEvents = mapAssistantToolUses(sessionId, message, state);
    return {
      sdkSessionId: message.session_id,
      uiEvents: text
        ? [
            {
              type: 'chat:delta',
              data: {
                text
              }
            }
          ]
        : [],
      harnessEvents: [
        ...(text
          ? [
              createSdkEvent(sessionId, message, 'model.delta', { text }),
              createSdkEvent(sessionId, message, 'message.completed', {
                role: 'assistant',
                source: 'model',
                text,
                blockTypes: readBlockTypes(content),
                parentToolUseId: message.parent_tool_use_id,
                subagentType: message.subagent_type,
                taskDescription: message.task_description,
                requestId: message.request_id,
                error: message.error
              })
            ]
          : []),
        ...toolUseEvents
      ]
    };
  }

  if (message.type === 'result') {
    const result = message as SDKResultMessage;
    if (result.subtype === 'success') {
      if (result.deferred_tool_use) {
        registerQueuedToolUse(state, {
          toolUseId: result.deferred_tool_use.id,
          toolName: result.deferred_tool_use.name,
          input: result.deferred_tool_use.input
        });
      }
      return {
        sdkSessionId: result.session_id,
        uiEvents: [
          {
            type: 'chat:complete',
            data: {
              text: result.result
            }
          },
          {
            type: 'session:complete',
            data: {}
          },
          {
            type: 'process:exit',
            data: {
              exitCode: 0
            }
          }
        ],
        harnessEvents: [
          ...(result.deferred_tool_use
            ? [
                createSdkEvent(sessionId, result, 'tool.queued', {
                  source: 'adapter',
                  queueReason: 'deferred_tool_use',
                  ...summarizeToolDescriptor(
                    descriptorForToolName(result.deferred_tool_use.name)
                  ),
                  adapterToolUseId: result.deferred_tool_use.id,
                  adapterToolName: result.deferred_tool_use.name,
                  toolUseId: result.deferred_tool_use.id,
                  toolName: result.deferred_tool_use.name,
                  inputMetadata: summarizeToolInput(result.deferred_tool_use.input)
                })
              ]
            : []),
          createSdkEvent(sessionId, result, 'model.completed', {
            stopReason: result.stop_reason,
            numTurns: result.num_turns,
            terminalReason: result.terminal_reason
          }),
          createSdkEvent(sessionId, result, 'turn.completed', {
            totalCostUsd: result.total_cost_usd
          })
        ]
      };
    }

    return {
      sdkSessionId: result.session_id,
      uiEvents: [
        {
          type: 'process:exit',
          data: {
            exitCode: 1,
            error: result.errors.join('\n') || result.subtype,
            errorType: 'SDK_FAILURE',
            status: 500,
            severity: 'error',
            fatal: true,
            errorDetails: redactJsonLike({
              subtype: result.subtype,
              terminalReason: result.terminal_reason,
              permissionDenials: result.permission_denials
            })
          }
        }
      ],
      harnessEvents: [
        createSdkEvent(sessionId, result, 'turn.failed', {
          subtype: result.subtype,
          errors: result.errors,
          terminalReason: result.terminal_reason
        })
      ]
    };
  }

  if (isPermissionDenied(message)) {
    return {
      sdkSessionId: message.session_id,
      uiEvents: [
        {
          type: 'tool:result',
          data: {
            name: message.tool_name,
            ok: false,
            output: message.message
          }
        }
      ],
      harnessEvents: [
        createSdkEvent(sessionId, message, 'tool.permission', {
          behavior: 'deny',
          source: 'adapter',
          ...summarizeToolDescriptor(descriptorForToolName(message.tool_name)),
          adapterToolUseId: message.tool_use_id,
          adapterToolName: message.tool_name,
          toolUseId: message.tool_use_id,
          toolName: message.tool_name,
          agentId: message.agent_id,
          reason: message.decision_reason,
          reasonType: message.decision_reason_type,
          message: message.message
        }),
        createSdkEvent(sessionId, message, 'tool.failed', {
          source: 'adapter',
          failureSource: 'permission',
          ...summarizeToolDescriptor(descriptorForToolName(message.tool_name)),
          adapterToolUseId: message.tool_use_id,
          adapterToolName: message.tool_name,
          toolUseId: message.tool_use_id,
          toolName: message.tool_name,
          reason: message.decision_reason,
          message: message.message
        })
      ]
    };
  }

  if (isCompactBoundary(message)) {
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents: [
        createSdkEvent(sessionId, message, 'context.compacted', {
          adapterCompactMetadata: message.compact_metadata,
          compactMetadata: message.compact_metadata,
          replayImplication: 'sdk_transcript_linkage_required'
        })
      ]
    };
  }

  if (isMirrorError(message)) {
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents: [
        createSdkEvent(sessionId, message, 'runtime.mirror.error', {
          adapterMirrorKey: message.key,
          error: message.error,
          key: message.key
        })
      ]
    };
  }

  if (message.type === 'tool_progress') {
    const descriptor = descriptorForToolName(message.tool_name);
    const startedEvents = isSdkBuiltinEvidenceDescriptor(descriptor)
      ? createInferredToolStartedEvent({
          sessionId,
          message,
          state,
          toolUseId: message.tool_use_id,
          toolName: message.tool_name,
          parentToolUseId: message.parent_tool_use_id,
          inferredFrom: 'tool_progress'
        })
      : [];
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents: [
        ...startedEvents,
        createSdkEvent(sessionId, message, 'tool.progress', {
          ...summarizeToolDescriptor(descriptor),
          adapterToolUseId: message.tool_use_id,
          adapterToolName: message.tool_name,
          toolUseId: message.tool_use_id,
          toolName: message.tool_name,
          parentToolUseId: message.parent_tool_use_id,
          elapsedTimeSeconds: message.elapsed_time_seconds,
          taskId: message.task_id
        })
      ]
    };
  }

  if (message.type === 'tool_use_summary') {
    const onlyChiralityMcpTools =
      state &&
      message.preceding_tool_use_ids.length > 0 &&
      message.preceding_tool_use_ids.every((toolUseId) =>
        isChiralityMcpTool(state.toolNamesByUseId.get(toolUseId))
      );
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents: onlyChiralityMcpTools
        ? []
        : [
            createSdkEvent(sessionId, message, 'tool.completed', {
              source: 'adapter',
              summary: message.summary,
              precedingToolUseIds: message.preceding_tool_use_ids
            })
          ]
    };
  }

  if (message.type === 'system' && message.subtype === 'hook_started') {
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents: [
        createSdkEvent(sessionId, message, 'hook.started', {
          hookId: message.hook_id,
          hookName: message.hook_name,
          hookEvent: message.hook_event
        })
      ]
    };
  }

  if (message.type === 'system' && message.subtype === 'hook_progress') {
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents: [
        createSdkEvent(sessionId, message, 'hook.progress', {
          hookId: message.hook_id,
          hookName: message.hook_name,
          hookEvent: message.hook_event,
          stdout: message.stdout,
          stderr: message.stderr,
          output: message.output
        })
      ]
    };
  }

  if (message.type === 'system' && message.subtype === 'hook_response') {
    const eventType = message.outcome === 'success' ? 'hook.completed' : 'hook.failed';
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents: [
        createSdkEvent(sessionId, message, eventType, {
          hookId: message.hook_id,
          hookName: message.hook_name,
          hookEvent: message.hook_event,
          outcome: message.outcome,
          exitCode: message.exit_code,
          stdout: message.stdout,
          stderr: message.stderr,
          output: message.output
        })
      ]
    };
  }

  if (message.type === 'system' && message.subtype === 'status') {
    const harnessEvents: HarnessEvent[] = [];
    if (message.status === 'requesting') {
      harnessEvents.push(
        createSdkEvent(sessionId, message, 'model.request.started', {
          permissionMode: message.permissionMode
        })
      );
    }
    if (message.status === 'compacting') {
      harnessEvents.push(
        createSdkEvent(sessionId, message, 'context.compaction.started', {
          permissionMode: message.permissionMode
        })
      );
    }
    if (message.compact_result === 'success') {
      harnessEvents.push(
        createSdkEvent(sessionId, message, 'context.compacted', {
          compactResult: message.compact_result,
          replayImplication: 'sdk_transcript_linkage_required'
        })
      );
    }
    if (message.compact_result === 'failed') {
      harnessEvents.push(
        createSdkEvent(sessionId, message, 'context.compaction.failed', {
          compactResult: message.compact_result,
          compactError: message.compact_error
        })
      );
    }
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents
    };
  }

  if (message.type === 'system' && message.subtype === 'task_started') {
    const childRunRecord = createChildRunRecordForTaskMessage({
      sessionId,
      message,
      state,
      status: 'running'
    });
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents: [
        createSdkEvent(sessionId, message, 'subagent.started', {
          taskId: message.task_id,
          toolUseId: message.tool_use_id,
          description: message.description,
          subagentType: message.subagent_type,
          taskType: message.task_type,
          workflowName: message.workflow_name,
          skipTranscript: message.skip_transcript,
          ...childRunEventData(childRunRecord)
        })
      ]
    };
  }

  if (message.type === 'system' && message.subtype === 'task_progress') {
    const childRunRecord = createChildRunRecordForTaskMessage({
      sessionId,
      message,
      state,
      status: 'running'
    });
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents: [
        createSdkEvent(sessionId, message, 'subagent.progress', {
          taskId: message.task_id,
          toolUseId: message.tool_use_id,
          description: message.description,
          subagentType: message.subagent_type,
          usage: message.usage,
          lastToolName: message.last_tool_name,
          summary: message.summary,
          ...childRunEventData(childRunRecord)
        })
      ]
    };
  }

  if (message.type === 'system' && message.subtype === 'task_updated') {
    const status = message.patch.status;
    const eventType =
      status === 'completed'
        ? 'subagent.completed'
        : status === 'failed' || status === 'killed'
          ? 'subagent.failed'
          : 'subagent.progress';
    const patchRecord = isRecord(message.patch)
      ? (message.patch as unknown as Record<string, unknown>)
      : undefined;
    const outputArtifactPath = patchRecord ? readString(patchRecord['output_file']) : undefined;
    const childRunStatus: ChildRunStatus =
      status === 'completed'
        ? 'completed'
        : status === 'failed' || status === 'killed'
          ? 'failed'
          : 'running';
    const childRunRecord =
      childRunStatus === 'completed' && !outputArtifactPath
        ? undefined
        : createChildRunRecordForTaskMessage({
            sessionId,
            message,
            state,
            status: childRunStatus,
            outputArtifactPath
          });
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents: [
        createSdkEvent(sessionId, message, eventType, {
          taskId: message.task_id,
          status,
          patchMetadata: summarizeTaskPatch(message.patch),
          ...childRunEventData(childRunRecord)
        })
      ]
    };
  }

  if (message.type === 'system' && message.subtype === 'task_notification') {
    const eventType = message.status === 'completed' ? 'subagent.completed' : 'subagent.failed';
    const childRunRecord = createChildRunRecordForTaskMessage({
      sessionId,
      message,
      state,
      status: message.status === 'completed' ? 'completed' : 'failed',
      outputArtifactPath: message.output_file
    });
    return {
      sdkSessionId: message.session_id,
      uiEvents: [],
      harnessEvents: [
        createSdkEvent(sessionId, message, eventType, {
          taskId: message.task_id,
          toolUseId: message.tool_use_id,
          status: message.status,
          outputFile: message.output_file,
          summary: message.summary,
          usage: message.usage,
          skipTranscript: message.skip_transcript,
          ...childRunEventData(childRunRecord)
        })
      ]
    };
  }

  return {
    sdkSessionId: 'session_id' in message ? message.session_id : undefined,
    uiEvents: [],
    harnessEvents: []
  };
}

export async function mapSdkMessageToHarnessWithArtifacts(
  sessionId: string,
  message: SDKMessage,
  state?: SdkToolEvidenceState
): Promise<SdkMessageMapping> {
  if (message.type === 'user') {
    return mapSdkUserMessageWithArtifacts(sessionId, message, state);
  }

  const mapped = mapSdkMessageToHarness(sessionId, message, state);
  if (message.type !== 'system') {
    return mapped;
  }

  if (message.subtype === 'task_notification') {
    const event = mapped.harnessEvents[0];
    if (!event) {
      return mapped;
    }

    const childRunId = readString(event.data.childRunId);
    const agentName = readString(event.data.agentName) ?? readString(event.data.subagentType);
    const artifactMetadata = await persistChildOutputArtifact({
      sessionId,
      turnId: state?.childRunContext?.parentTurnId,
      taskId: message.task_id,
      childRunId,
      toolUseId: message.tool_use_id,
      agentName,
      status: message.status,
      outputFile: message.output_file,
      summary: message.summary,
      usage: message.usage,
      skipTranscript: message.skip_transcript
    });

    if (artifactMetadata) {
      event.data = {
        ...event.data,
        summary: '[stored in child output artifact]',
        outputArtifactPath: artifactMetadata.artifactRelativePath,
        childOutputArtifactMetadata: artifactMetadata
      };
    }
    return mapped;
  }

  if (message.subtype === 'task_updated') {
    const event = mapped.harnessEvents[0];
    const patchRecord = isRecord(message.patch)
      ? (message.patch as Record<string, unknown>)
      : undefined;
    if (!event || !patchRecord) {
      return mapped;
    }

    const summary = readOptionalString(patchRecord.summary);
    if (summary === undefined) {
      return mapped;
    }

    const artifactMetadata = await persistChildOutputArtifact({
      sessionId,
      turnId: state?.childRunContext?.parentTurnId,
      taskId: message.task_id,
      childRunId: readString(event.data.childRunId),
      toolUseId: readString(event.data.toolUseId),
      agentName: readString(event.data.agentName),
      status: readString(patchRecord.status),
      outputFile: readString(patchRecord.output_file),
      summary,
      usage: patchRecord.usage
    });

    if (artifactMetadata) {
      event.data = {
        ...event.data,
        summary: '[stored in child output artifact]',
        outputArtifactPath: artifactMetadata.artifactRelativePath,
        childOutputArtifactMetadata: artifactMetadata
      };
    }
    return mapped;
  }

  return mapped;
}
