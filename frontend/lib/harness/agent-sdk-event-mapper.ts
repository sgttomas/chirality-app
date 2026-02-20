import type { SDKMessage } from "@anthropic-ai/claude-agent-sdk";

import type { ToolResultInfo, ToolUseInfo, UIEvent, UsageInfo } from "./types";

type UnknownRecord = Record<string, unknown>;

function isRecord(value: unknown): value is UnknownRecord {
  return typeof value === "object" && value !== null;
}

function asString(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

function normalizeParentToolUseId(value: unknown): string | null {
  if (typeof value !== "string") {
    return null;
  }
  const trimmed = value.trim();
  return trimmed ? trimmed : null;
}

function asStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value.filter((item): item is string => typeof item === "string");
}

function toUsageInfo(value: unknown): UsageInfo {
  if (!isRecord(value)) {
    return { input_tokens: 0, output_tokens: 0 };
  }

  const inputTokens = typeof value.input_tokens === "number" ? value.input_tokens : 0;
  const outputTokens = typeof value.output_tokens === "number" ? value.output_tokens : 0;

  const usage: UsageInfo = {
    input_tokens: inputTokens,
    output_tokens: outputTokens,
  };

  if (typeof value.cache_read_input_tokens === "number") {
    usage.cache_read_input_tokens = value.cache_read_input_tokens;
  }

  if (typeof value.cache_creation_input_tokens === "number") {
    usage.cache_creation_input_tokens = value.cache_creation_input_tokens;
  }

  return usage;
}

function stringifyToolResultContent(content: unknown): string {
  if (typeof content === "string") {
    return content;
  }

  if (Array.isArray(content)) {
    return content
      .map((item) => {
        if (typeof item === "string") {
          return item;
        }

        try {
          return JSON.stringify(item);
        } catch {
          return String(item);
        }
      })
      .join("\n");
  }

  if (content === null || typeof content === "undefined") {
    return "";
  }

  try {
    return JSON.stringify(content);
  } catch {
    return String(content);
  }
}

function extractToolUseFromAssistantMessage(message: unknown, parentToolUseId: string | null): ToolUseInfo[] {
  if (!isRecord(message) || !Array.isArray(message.content)) {
    return [];
  }

  const results: ToolUseInfo[] = [];

  for (const block of message.content) {
    if (!isRecord(block) || block.type !== "tool_use") {
      continue;
    }

    const toolUseId = asString(block.id) ?? "unknown-tool-use";
    const name = asString(block.name) ?? "unknown-tool";
    const input = isRecord(block.input) ? block.input : {};

    results.push({ toolUseId, name, input, parentToolUseId });
  }

  return results;
}

function extractToolResultFromUserMessage(message: unknown, parentToolUseId: string | null): ToolResultInfo[] {
  if (!isRecord(message) || !Array.isArray(message.content)) {
    return [];
  }

  const results: ToolResultInfo[] = [];

  for (const block of message.content) {
    if (!isRecord(block) || block.type !== "tool_result") {
      continue;
    }

    const toolUseId = asString(block.tool_use_id) ?? "unknown-tool-use";
    const isError = block.is_error === true;
    const content = stringifyToolResultContent(block.content);

    results.push({ toolUseId, content, isError, parentToolUseId });
  }

  return results;
}

function mapStreamDeltaToUiEvents(event: unknown, sessionId: string, parentToolUseId: string | null): UIEvent[] {
  if (!isRecord(event)) {
    return [];
  }

  const streamType = asString(event.type);
  if (!streamType) {
    return [];
  }

  if (streamType === "content_block_delta" && isRecord(event.delta)) {
    const deltaType = asString(event.delta.type);
    const text = asString(event.delta.text);
    if (deltaType === "text_delta" && text) {
      return [{ type: "chat:delta", sessionId, text }];
    }
    // Ignore thought deltas
    return [];
  }

  if (streamType === "content_block_start" && isRecord(event.content_block)) {
    const blockType = asString(event.content_block.type);

    // Ignore thought blocks
    if (blockType === "thought") {
      return [];
    }

    if (blockType === "tool_use") {
      const toolUseId = asString(event.content_block.id) ?? "unknown-tool-use";
      const name = asString(event.content_block.name) ?? "unknown-tool";
      const input = isRecord(event.content_block.input) ? event.content_block.input : {};
      return [{ type: "tool:start", sessionId, toolUseId, name, input, parentToolUseId }];
    }
  }

  return [];
}

function mapToolProgressToUiEvents(
  message: Extract<SDKMessage, { type: "tool_progress" }>,
  sessionId: string,
): UIEvent[] {
  const toolUseId = asString(message.tool_use_id) ?? "unknown-tool-use";
  const name = asString(message.tool_name) ?? "unknown-tool";
  const parentToolUseId = normalizeParentToolUseId(message.parent_tool_use_id);
  const elapsedSeconds = typeof message.elapsed_time_seconds === "number" ? message.elapsed_time_seconds : 0;

  return [{ type: "tool:progress", sessionId, toolUseId, name, elapsedSeconds, parentToolUseId }];
}

function mapTaskNotificationToUiEvents(message: SDKMessage, sessionId: string): UIEvent[] {
  if (message.type !== "system" || message.subtype !== "task_notification") {
    return [];
  }

  const toolUseId = asString(message.tool_use_id);
  if (!toolUseId) {
    return [];
  }

  const content = asString(message.summary) ?? `Task ${message.status}`;
  const isError = message.status !== "completed";

  return [
    {
      type: "tool:result",
      sessionId,
      toolUseId,
      content,
      isError,
      parentToolUseId: null,
    },
  ];
}

function mapResultToUiEvents(event: Extract<SDKMessage, { type: "result" }>, sessionId: string): UIEvent[] {
  if (event.subtype === "success") {
    return [
      {
        type: "chat:complete",
        sessionId,
        text: event.result,
      },
      {
        type: "session:complete",
        sessionId,
        costUsd: event.total_cost_usd,
        usage: toUsageInfo(event.usage),
      },
    ];
  }

  const explicitError = event.errors.find((item: unknown) => typeof item === "string" && item.trim().length > 0);
  const fallbackError =
    event.subtype === "error_max_turns"
      ? "Turn limit reached (max_turns)."
      : `Claude Agent SDK reported ${event.subtype}.`;

  return [
    {
      type: "session:error",
      sessionId,
      error: explicitError ?? fallbackError,
    },
  ];
}

export function mapSdkMessageToUiEvents(message: SDKMessage, sessionId: string): UIEvent[] {
  if (message.type === "system" && message.subtype === "init") {
    return [
      {
        type: "session:init",
        sessionId,
        claudeSessionId: message.session_id,
        model: message.model,
        tools: asStringArray(message.tools),
      },
    ];
  }

  if (message.type === "stream_event") {
    const parentToolUseId = normalizeParentToolUseId(message.parent_tool_use_id);
    return mapStreamDeltaToUiEvents(message.event as unknown, sessionId, parentToolUseId);
  }

  if (message.type === "assistant") {
    const parentToolUseId = normalizeParentToolUseId(message.parent_tool_use_id);
    const toolStarts = extractToolUseFromAssistantMessage(message.message, parentToolUseId);
    const toolEvents: UIEvent[] = toolStarts.map((toolUse) => ({
      type: "tool:start",
      sessionId,
      toolUseId: toolUse.toolUseId,
      name: toolUse.name,
      input: toolUse.input,
      parentToolUseId: toolUse.parentToolUseId,
    }));

    // Phase 1 correlation logging — Task tool invocations (subagent spawns)
    for (const toolUse of toolStarts) {
      if (toolUse.name === "Task") {
        const subagentType = asString(toolUse.input.subagent_type);
        const description = asString(toolUse.input.description);
        console.info(
          `[harness:subagent] Task tool invoked — toolUseId=${toolUse.toolUseId} subagent_type=${subagentType ?? "unknown"} description=${description ?? "none"}`,
        );
      }
    }

    // Defensive: log parent_tool_use_id if present on the raw message for subagent-origin correlation.
    // The SDK message shape may not always include this field, so we guard access.
    if (parentToolUseId) {
      console.info(
        `[harness:subagent] Message has parent_tool_use_id=${parentToolUseId} — subagent-origin message.`,
      );
    }

    if (toolEvents.length > 0) {
      return toolEvents;
    }

    if (message.error) {
      return [
        {
          type: "session:error",
          sessionId,
          error: `Assistant message error: ${message.error}`,
        },
      ];
    }

    return [];
  }

  if (message.type === "user") {
    const parentToolUseId = normalizeParentToolUseId(message.parent_tool_use_id);
    const toolResults = extractToolResultFromUserMessage(message.message, parentToolUseId);
    return toolResults.map((toolResult) => ({
      type: "tool:result",
      sessionId,
      toolUseId: toolResult.toolUseId,
      content: toolResult.content,
      isError: toolResult.isError,
      parentToolUseId: toolResult.parentToolUseId,
    }));
  }

  if (message.type === "tool_progress") {
    return mapToolProgressToUiEvents(message, sessionId);
  }

  if (message.type === "system" && message.subtype === "task_notification") {
    return mapTaskNotificationToUiEvents(message, sessionId);
  }

  if (message.type === "result") {
    return mapResultToUiEvents(message, sessionId);
  }

  if (message.type === "auth_status" && message.error) {
    return [
      {
        type: "session:error",
        sessionId,
        error: message.error,
      },
    ];
  }

  return [];
}
