import {
  AgentEnginePort,
  AgentEngineRunInput,
  EngineAdapterSubject,
  EngineCapabilities,
  PUBLIC_UI_EVENT_NAMES
} from './agent-engine-port.js';
import type { HarnessEvent } from './event-schema.js';
import { UIEvent } from './types.js';

export type EngineConformanceIssueCode =
  | 'STREAM_THREW'
  | 'UNKNOWN_UI_EVENT'
  | 'MISSING_SESSION_INIT'
  | 'MULTIPLE_SESSION_INIT'
  | 'MISSING_ENGINE_SESSION_ID'
  | 'MISSING_ADAPTER_ID'
  | 'MISSING_PROVIDER_ID'
  | 'MISSING_SESSION_INIT_MODEL'
  | 'SESSION_INIT_NOT_FIRST'
  | 'SESSION_INIT_ADAPTER_MISMATCH'
  | 'SESSION_INIT_PROVIDER_MISMATCH'
  | 'INVALID_DECLARED_CAPABILITY'
  | 'TOOLS_NOT_DECLARED'
  | 'ATTACHMENTS_NOT_DECLARED'
  | 'INTERRUPTION_NOT_DECLARED'
  | 'MISSING_PROCESS_EXIT'
  | 'MULTIPLE_PROCESS_EXIT'
  | 'PROCESS_EXIT_NOT_TERMINAL'
  | 'MISSING_INTERRUPTED_PROCESS_EXIT'
  | 'MISSING_HARNESS_TERMINAL'
  | 'MULTIPLE_HARNESS_TERMINAL'
  | 'HARNESS_TERMINAL_MISMATCH'
  | 'MISSING_TOOL_CALL_ID'
  | 'TOOL_RESULT_WITHOUT_START'
  | 'TOOL_START_WITHOUT_RESULT'
  | 'TOOL_PERMISSION_AFTER_RESULT'
  | 'MISSING_TOOL_PERMISSION'
  | 'COMPACTION_NOT_DECLARED'
  | 'COMPACTION_RESULT_WITHOUT_START'
  | 'COMPACTION_START_WITHOUT_RESULT'
  | 'PERSISTENCE_READ_FAILED'
  | 'MISSING_PERSISTED_EVENT'
  | 'UNREDACTED_EVIDENCE';

export type EngineConformanceIssue = {
  code: EngineConformanceIssueCode;
  message: string;
  eventIndex?: number;
  eventType?: string;
};

export type EngineConformanceOptions = {
  requireSessionInit?: boolean;
  requireEngineSessionId?: boolean;
  requireInterruptedProcessExit?: boolean;
  requireHarnessTerminal?: boolean;
  requireToolPermissionEvidence?: boolean;
  readPersistedEvents?: (sessionId: string) => Promise<readonly HarnessEvent[]>;
  forbiddenEvidenceValues?: readonly string[];
};

export type EngineConformanceReport = {
  subject: EngineAdapterSubject;
  passed: boolean;
  events: UIEvent[];
  eventTypes: string[];
  issues: EngineConformanceIssue[];
};

const PUBLIC_UI_EVENT_NAME_SET = new Set<string>(PUBLIC_UI_EVENT_NAMES);

function summarizeThrownError(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

function readEventType(event: unknown): string | undefined {
  return event && typeof event === 'object' && 'type' in event
    ? String((event as { type: unknown }).type)
    : undefined;
}

function isSessionInitEvent(event: UIEvent): event is Extract<UIEvent, { type: 'session:init' }> {
  return event.type === 'session:init';
}

function isProcessExitEvent(event: UIEvent): event is Extract<UIEvent, { type: 'process:exit' }> {
  return event.type === 'process:exit';
}

function isHarnessUiEvent(event: UIEvent): event is Extract<UIEvent, { type: 'harness:event' }> {
  return event.type === 'harness:event';
}

const CAPABILITY_NAMES = [
  'credentials',
  'tools',
  'attachments',
  'interruption',
  'durableResume',
  'compaction'
] as const satisfies readonly (keyof EngineCapabilities)[];

const HARNESS_TERMINAL_TYPES = new Set([
  'turn.completed',
  'turn.failed',
  'turn.cancelled',
  'turn.interrupted'
]);

const TOOL_EVENT_TYPES = new Set([
  'tool.queued',
  'tool.permission',
  'tool.started',
  'tool.progress',
  'tool.completed',
  'tool.failed'
]);

function toolCallId(event: HarnessEvent): string | undefined {
  for (const key of ['toolCallId', 'toolUseId', 'adapterToolUseId']) {
    const value = event.data[key];
    if (typeof value === 'string' && value.length > 0) {
      return value;
    }
  }
  return undefined;
}

function stableJson(value: unknown): string {
  try {
    return JSON.stringify(value);
  } catch {
    return String(value);
  }
}

async function evaluateEventStream(
  port: AgentEnginePort,
  input: AgentEngineRunInput,
  subject: EngineAdapterSubject,
  events: UIEvent[],
  options: EngineConformanceOptions,
  thrownError?: unknown
): Promise<EngineConformanceReport> {
  const issues: EngineConformanceIssue[] = [];
  const eventTypes = events.map((event) => readEventType(event) ?? '<missing>');

  for (const capability of CAPABILITY_NAMES) {
    if (typeof port.descriptor.capabilities[capability] !== 'boolean') {
      issues.push({
        code: 'INVALID_DECLARED_CAPABILITY',
        message: `Engine descriptor capability '${capability}' must be boolean`
      });
    }
  }
  if (!port.descriptor.capabilities.tools && input.opts.tools.length > 0) {
    issues.push({
      code: 'TOOLS_NOT_DECLARED',
      message: 'Turn supplied tools to an adapter that declares tools=false'
    });
  }
  if (
    !port.descriptor.capabilities.attachments &&
    input.contentBlocks?.some((block) => block.type === 'file')
  ) {
    issues.push({
      code: 'ATTACHMENTS_NOT_DECLARED',
      message: 'Turn supplied a file attachment to an adapter that declares attachments=false'
    });
  }
  if (options.requireInterruptedProcessExit && !port.descriptor.capabilities.interruption) {
    issues.push({
      code: 'INTERRUPTION_NOT_DECLARED',
      message: 'Interrupt conformance was requested for an adapter that declares interruption=false'
    });
  }

  if (thrownError !== undefined) {
    issues.push({
      code: 'STREAM_THREW',
      message: `Engine stream threw before terminal evidence: ${summarizeThrownError(thrownError)}`
    });
  }

  events.forEach((event, eventIndex) => {
    const eventType = readEventType(event);
    if (!eventType || !PUBLIC_UI_EVENT_NAME_SET.has(eventType)) {
      issues.push({
        code: 'UNKNOWN_UI_EVENT',
        message: `Engine emitted non-public UI event '${eventType ?? '<missing>'}'`,
        eventIndex,
        eventType
      });
    }
  });

  const sessionInitCount = events.filter(isSessionInitEvent).length;
  if (options.requireSessionInit !== false && sessionInitCount === 0) {
    issues.push({
      code: 'MISSING_SESSION_INIT',
      message: 'Engine did not emit session:init metadata'
    });
  }
  if (sessionInitCount > 1) {
    issues.push({
      code: 'MULTIPLE_SESSION_INIT',
      message: 'Engine emitted more than one session:init event'
    });
  }
  const firstSessionInitIndex = events.findIndex(isSessionInitEvent);
  if (firstSessionInitIndex > 0) {
    issues.push({
      code: 'SESSION_INIT_NOT_FIRST',
      message: 'session:init must precede every other public UI event',
      eventIndex: firstSessionInitIndex,
      eventType: 'session:init'
    });
  }

  events.forEach((event, eventIndex) => {
    if (!isSessionInitEvent(event)) {
      return;
    }

    if (options.requireEngineSessionId && !event.data.engineSessionId) {
      issues.push({
        code: 'MISSING_ENGINE_SESSION_ID',
        message: 'session:init did not include provider-neutral engineSessionId metadata',
        eventIndex,
        eventType: event.type
      });
    }
    if (!event.data.adapterId) {
      issues.push({
        code: 'MISSING_ADAPTER_ID',
        message: 'session:init did not include adapterId attribution',
        eventIndex,
        eventType: event.type
      });
    }
    if (!event.data.providerId) {
      issues.push({
        code: 'MISSING_PROVIDER_ID',
        message: 'session:init did not include providerId attribution',
        eventIndex,
        eventType: event.type
      });
    }
    if (!event.data.model) {
      issues.push({
        code: 'MISSING_SESSION_INIT_MODEL',
        message: 'session:init did not include model metadata',
        eventIndex,
        eventType: event.type
      });
    }
    if (event.data.adapterId !== port.descriptor.adapterId) {
      issues.push({
        code: 'SESSION_INIT_ADAPTER_MISMATCH',
        message: 'session:init adapterId does not match the selected adapter descriptor',
        eventIndex,
        eventType: event.type
      });
    }
    if (event.data.providerId !== port.descriptor.providerId) {
      issues.push({
        code: 'SESSION_INIT_PROVIDER_MISMATCH',
        message: 'session:init providerId does not match the selected adapter descriptor',
        eventIndex,
        eventType: event.type
      });
    }
  });

  const processExitIndexes = events
    .map((event, index) => (isProcessExitEvent(event) ? index : -1))
    .filter((index) => index >= 0);
  const processExitIndex = processExitIndexes[0] ?? -1;
  if (processExitIndex < 0) {
    issues.push({
      code: 'MISSING_PROCESS_EXIT',
      message: 'Engine did not emit terminal process:exit evidence'
    });
  } else if (processExitIndex !== events.length - 1) {
    issues.push({
      code: 'PROCESS_EXIT_NOT_TERMINAL',
      message: 'process:exit must be the final public UI event',
      eventIndex: processExitIndex,
      eventType: 'process:exit'
    });
  }
  if (processExitIndexes.length > 1) {
    issues.push({
      code: 'MULTIPLE_PROCESS_EXIT',
      message: 'Engine emitted more than one process:exit event'
    });
  }

  if (
    options.requireInterruptedProcessExit &&
    !events.some(
      (event) =>
        isProcessExitEvent(event) && event.data.exitCode === 130 && event.data.interrupted === true
    )
  ) {
    issues.push({
      code: 'MISSING_INTERRUPTED_PROCESS_EXIT',
      message: 'Interrupted turn did not emit process:exit with exitCode 130 and interrupted=true'
    });
  }

  const harnessEvents = events.filter(isHarnessUiEvent).map((event) => event.data);
  let persistedEvents: readonly HarnessEvent[] = [];
  if (options.readPersistedEvents) {
    try {
      persistedEvents = await options.readPersistedEvents(input.session.sessionId);
      const persistedIds = new Set(persistedEvents.map((event) => event.eventId));
      for (const event of harnessEvents) {
        if (!persistedIds.has(event.eventId)) {
          issues.push({
            code: 'MISSING_PERSISTED_EVENT',
            message: `Live harness event '${event.type}' was not present in durable replay evidence`,
            eventType: event.type
          });
        }
      }
    } catch (error) {
      issues.push({
        code: 'PERSISTENCE_READ_FAILED',
        message: `Could not read persisted engine evidence: ${summarizeThrownError(error)}`
      });
    }
  }
  const semanticHarnessEvents = options.readPersistedEvents ? persistedEvents : harnessEvents;
  const harnessTerminals = semanticHarnessEvents.filter((event) =>
    HARNESS_TERMINAL_TYPES.has(event.type)
  );
  if (options.requireHarnessTerminal && harnessTerminals.length === 0) {
    issues.push({
      code: 'MISSING_HARNESS_TERMINAL',
      message: 'Turn did not emit a canonical terminal harness event'
    });
  }
  if (harnessTerminals.length > 1) {
    issues.push({
      code: 'MULTIPLE_HARNESS_TERMINAL',
      message: 'Turn emitted more than one canonical terminal harness event'
    });
  }
  const processExit = processExitIndex >= 0 ? events[processExitIndex] : undefined;
  const harnessTerminal = harnessTerminals[0];
  if (processExit && isProcessExitEvent(processExit) && harnessTerminal) {
    const expectedTerminal =
      processExit.data.exitCode === 0
        ? 'turn.completed'
        : processExit.data.interrupted
          ? undefined
          : 'turn.failed';
    const interruptedTerminal =
      harnessTerminal.type === 'turn.interrupted' || harnessTerminal.type === 'turn.cancelled';
    if (
      (expectedTerminal && harnessTerminal.type !== expectedTerminal) ||
      (processExit.data.interrupted === true && !interruptedTerminal)
    ) {
      issues.push({
        code: 'HARNESS_TERMINAL_MISMATCH',
        message: `Harness terminal '${harnessTerminal.type}' conflicts with process exit ${processExit.data.exitCode}`
      });
    }
  }

  const toolEvents = semanticHarnessEvents.filter((event) => TOOL_EVENT_TYPES.has(event.type));
  const toolLifecycles = new Map<string, Array<{ event: HarnessEvent; index: number }>>();
  for (const event of toolEvents) {
    const id = toolCallId(event);
    const index = semanticHarnessEvents.indexOf(event);
    if (!id) {
      issues.push({
        code: 'MISSING_TOOL_CALL_ID',
        message: `Harness event '${event.type}' did not carry a provider-neutral tool call ID`,
        eventIndex: index,
        eventType: event.type
      });
      continue;
    }
    const lifecycle = toolLifecycles.get(id) ?? [];
    lifecycle.push({ event, index });
    toolLifecycles.set(id, lifecycle);
  }
  for (const [id, lifecycle] of toolLifecycles) {
    const started = lifecycle.find((item) => item.event.type === 'tool.started');
    const result = lifecycle.find(
      (item) => item.event.type === 'tool.completed' || item.event.type === 'tool.failed'
    );
    const permission = lifecycle.find((item) => item.event.type === 'tool.permission');
    if (result && !started) {
      issues.push({
        code: 'TOOL_RESULT_WITHOUT_START',
        message: `Tool call '${id}' completed without tool.started evidence`,
        eventIndex: result.index,
        eventType: result.event.type
      });
    }
    if (started && !result) {
      issues.push({
        code: 'TOOL_START_WITHOUT_RESULT',
        message: `Tool call '${id}' started without terminal tool evidence`,
        eventIndex: started.index,
        eventType: started.event.type
      });
    }
    if (permission && result && permission.index > result.index) {
      issues.push({
        code: 'TOOL_PERMISSION_AFTER_RESULT',
        message: `Tool call '${id}' recorded permission after its result`,
        eventIndex: permission.index,
        eventType: permission.event.type
      });
    }
    if (options.requireToolPermissionEvidence && result && !permission) {
      issues.push({
        code: 'MISSING_TOOL_PERMISSION',
        message: `Tool call '${id}' completed without permission evidence`,
        eventIndex: result.index,
        eventType: result.event.type
      });
    }
  }

  const compactionEvents = semanticHarnessEvents.filter(
    (event) =>
      event.type === 'context.compaction.started' ||
      event.type === 'context.compacted' ||
      event.type === 'context.compaction.failed'
  );
  if (compactionEvents.length > 0 && !port.descriptor.capabilities.compaction) {
    issues.push({
      code: 'COMPACTION_NOT_DECLARED',
      message: 'Adapter emitted compaction evidence while declaring compaction=false'
    });
  }
  let pendingCompactions = 0;
  for (const event of compactionEvents) {
    if (event.type === 'context.compaction.started') {
      pendingCompactions += 1;
    } else if (pendingCompactions === 0) {
      issues.push({
        code: 'COMPACTION_RESULT_WITHOUT_START',
        message: `Compaction terminal '${event.type}' has no preceding start`,
        eventType: event.type
      });
    } else {
      pendingCompactions -= 1;
    }
  }
  if (pendingCompactions > 0) {
    issues.push({
      code: 'COMPACTION_START_WITHOUT_RESULT',
      message: `${pendingCompactions} compaction lifecycle(s) did not emit a terminal result`
    });
  }

  const evidence = stableJson({ events, persistedEvents });
  for (const forbidden of options.forbiddenEvidenceValues ?? []) {
    if (forbidden.length > 0 && evidence.includes(forbidden)) {
      issues.push({
        code: 'UNREDACTED_EVIDENCE',
        message: 'Public or persisted evidence contains a forbidden sensitive value'
      });
    }
  }

  return {
    subject,
    passed: issues.length === 0,
    events,
    eventTypes,
    issues
  };
}

export async function runEngineConformance(
  port: AgentEnginePort,
  input: AgentEngineRunInput,
  options: EngineConformanceOptions = {}
): Promise<EngineConformanceReport> {
  const events: UIEvent[] = [];
  let thrownError: unknown;

  try {
    for await (const event of port.startTurn(input)) {
      events.push(event);
    }
  } catch (error) {
    thrownError = error;
  }

  return evaluateEventStream(port, input, port.subject, events, options, thrownError);
}

export async function runEngineInterruptConformance(
  port: AgentEnginePort,
  input: AgentEngineRunInput,
  options: EngineConformanceOptions = {}
): Promise<EngineConformanceReport> {
  const events: UIEvent[] = [];
  let thrownError: unknown;
  const iterator = port.startTurn(input)[Symbol.asyncIterator]();

  try {
    const first = await iterator.next();
    if (!first.done) {
      events.push(first.value);
    }

    await port.interrupt(input.session.sessionId);

    while (true) {
      const next = await iterator.next();
      if (next.done) {
        break;
      }
      events.push(next.value);
    }
  } catch (error) {
    thrownError = error;
  }

  return evaluateEventStream(
    port,
    input,
    port.subject,
    events,
    {
      ...options,
      requireInterruptedProcessExit: true
    },
    thrownError
  );
}
