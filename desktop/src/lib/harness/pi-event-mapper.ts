import type { HarnessErrorType, UIEvent } from '@chirality/runtime-contracts/types';
import type { HarnessEventType } from '@chirality/runtime-contracts/event-schema';

export type PiHarnessEventDraft = {
  kind: 'harness';
  type: HarnessEventType;
  data: Record<string, unknown>;
};

export type PiUiEventDraft = {
  kind: 'ui';
  event: UIEvent;
};

export type PiMappedEvent = PiHarnessEventDraft | PiUiEventDraft;

export type PiTurnFailure = {
  errorType: HarnessErrorType;
  message: string;
  status: number;
};

export type PiEventMapperState = {
  currentAssistantText: string;
  lastAssistantText: string;
  failure?: PiTurnFailure;
  sawAgentEnd: boolean;
  sawSettled: boolean;
};

export type PiAgentSessionEventLike = {
  type: string;
  [key: string]: unknown;
};

export function createPiEventMapperState(): PiEventMapperState {
  return {
    currentAssistantText: '',
    lastAssistantText: '',
    sawAgentEnd: false,
    sawSettled: false
  };
}

function asRecord(value: unknown): Record<string, unknown> | undefined {
  return value && typeof value === 'object' ? (value as Record<string, unknown>) : undefined;
}

function asString(value: unknown): string | undefined {
  return typeof value === 'string' && value.length > 0 ? value : undefined;
}

function textFromContent(value: unknown): string {
  if (typeof value === 'string') {
    return value;
  }
  if (!Array.isArray(value)) {
    return '';
  }
  return value
    .map((block) => {
      const record = asRecord(block);
      return record?.type === 'text' ? asString(record.text) ?? '' : '';
    })
    .filter(Boolean)
    .join('\n');
}

function assistantText(message: unknown): string {
  const record = asRecord(message);
  if (record?.role !== 'assistant') {
    return '';
  }
  return textFromContent(record.content);
}

function usageData(message: unknown): Record<string, unknown> {
  const usage = asRecord(asRecord(message)?.usage);
  return usage ? { usage } : {};
}

function classifyProviderFailure(message: string): PiTurnFailure {
  const normalized = message.toLowerCase();
  if (
    normalized.includes('context length') ||
    normalized.includes('context window') ||
    normalized.includes('maximum context') ||
    normalized.includes('too many tokens')
  ) {
    return { errorType: 'CONTEXT_EXHAUSTED', message, status: 422 };
  }
  if (
    normalized.includes('unauthorized') ||
    normalized.includes('authentication') ||
    normalized.includes('invalid api key') ||
    normalized.includes('status 401') ||
    normalized.includes('status 403')
  ) {
    return { errorType: 'PROVIDER_AUTH_FAILURE', message, status: 503 };
  }
  if (normalized.includes('model') && (normalized.includes('not found') || normalized.includes('unavailable'))) {
    return { errorType: 'MODEL_UNAVAILABLE', message, status: 503 };
  }
  return { errorType: 'PROVIDER_PROTOCOL_FAILURE', message, status: 502 };
}

/**
 * Translate Pi's session event vocabulary into Chirality-owned public and rich
 * events. Terminal process evidence remains the adapter's responsibility so a
 * provider can never emit more than one `process:exit`.
 */
export function mapPiSessionEvent(
  event: PiAgentSessionEventLike,
  state: PiEventMapperState
): PiMappedEvent[] {
  switch (event.type) {
    case 'agent_start':
      return [{ kind: 'harness', type: 'message.started', data: { source: 'pi' } }];

    case 'turn_start':
      return [{ kind: 'harness', type: 'model.request.started', data: { source: 'pi' } }];

    case 'message_start': {
      if (asRecord(event.message)?.role === 'assistant') {
        state.currentAssistantText = '';
      }
      return [];
    }

    case 'message_update': {
      const assistantEvent = asRecord(event.assistantMessageEvent);
      if (assistantEvent?.type === 'text_delta') {
        const delta = asString(assistantEvent.delta) ?? '';
        if (!delta) {
          return [];
        }
        state.currentAssistantText += delta;
        return [
          { kind: 'harness', type: 'model.delta', data: { text: delta, source: 'pi' } },
          { kind: 'harness', type: 'message.delta', data: { text: delta, source: 'pi' } },
          { kind: 'ui', event: { type: 'chat:delta', data: { text: delta } } }
        ];
      }
      if (assistantEvent?.type === 'error') {
        const providerError = asRecord(assistantEvent.error);
        const message = asString(providerError?.errorMessage) ?? 'Pi provider stream failed';
        state.failure = classifyProviderFailure(message);
      }
      return [];
    }

    case 'message_end': {
      const messageRecord = asRecord(event.message);
      if (
        messageRecord?.role === 'assistant' &&
        (messageRecord.stopReason === 'error' || messageRecord.stopReason === 'aborted') &&
        asString(messageRecord.errorMessage)
      ) {
        state.failure = classifyProviderFailure(messageRecord.errorMessage as string);
      }
      const text = assistantText(event.message) || state.currentAssistantText;
      if (!text) {
        return [];
      }
      state.lastAssistantText = text;
      return [
        {
          kind: 'harness',
          type: 'message.completed',
          data: { text, source: 'pi', ...usageData(event.message) }
        }
      ];
    }

    case 'turn_end':
      return [
        {
          kind: 'harness',
          type: 'model.completed',
          data: { source: 'pi', ...usageData(event.message) }
        }
      ];

    // The neutral Chirality tool bridge owns permission and persisted tool
    // lifecycle evidence. Pi's events can contain raw model arguments and file
    // contents, so persisting them here would both duplicate the authoritative
    // lifecycle and bypass its redaction/summarization policy.
    case 'tool_execution_start':
    case 'tool_execution_update':
      return [];

    case 'tool_execution_end': {
      const name = asString(event.toolName) ?? 'unknown';
      const isError = event.isError === true;
      return [
        {
          kind: 'ui',
          event: {
            type: 'tool:result',
            data: { name, ok: !isError }
          }
        }
      ];
    }

    case 'compaction_start':
      return [
        {
          kind: 'harness',
          type: 'context.compaction.started',
          data: { reason: event.reason, source: 'pi' }
        }
      ];

    case 'compaction_end': {
      const failed = event.aborted === true || Boolean(asString(event.errorMessage));
      return [
        {
          kind: 'harness',
          type: failed ? 'context.compaction.failed' : 'context.compacted',
          data: {
            reason: event.reason,
            aborted: event.aborted === true,
            willRetry: event.willRetry === true,
            ...(asString(event.errorMessage) ? { error: event.errorMessage } : {}),
            source: 'pi'
          }
        }
      ];
    }

    case 'auto_retry_end':
      if (event.success === false && asString(event.finalError)) {
        state.failure = classifyProviderFailure(event.finalError as string);
      }
      return [];

    case 'agent_end':
      if (event.willRetry !== true) {
        state.sawAgentEnd = true;
      }
      return [];

    case 'agent_settled':
      state.sawSettled = true;
      return [];

    default:
      return [];
  }
}
