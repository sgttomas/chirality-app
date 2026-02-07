import type { ToolResultInfo, ToolUseInfo, UIEvent, UsageInfo } from "./types";

type UnknownRecord = Record<string, unknown>;

function isRecord(value: unknown): value is UnknownRecord {
  return typeof value === "object" && value !== null;
}

function asString(value: unknown): string | null {
  return typeof value === "string" ? value : null;
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

export function parseNdjsonLine(line: string): unknown | null {
  const trimmed = line.trim();
  if (!trimmed) {
    return null;
  }

  try {
    return JSON.parse(trimmed);
  } catch {
    return null;
  }
}

export function extractToolUseFromAssistantMessage(message: unknown): ToolUseInfo[] {
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

    results.push({ toolUseId, name, input });
  }

  return results;
}

export function extractToolResultFromUserMessage(message: unknown): ToolResultInfo[] {
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

    results.push({ toolUseId, content, isError });
  }

  return results;
}

export function mapClaudeEventToUiEvents(event: unknown, sessionId: string): UIEvent[] {
  if (!isRecord(event)) {
    return [];
  }

  const type = asString(event.type);
  if (!type) {
    return [];
  }

  if (type === "system" && event.subtype === "init") {
    const claudeSessionId = asString(event.session_id);
    const model = asString(event.model) ?? "unknown";
    const tools = asStringArray(event.tools);

    return [
      {
        type: "session:init",
        sessionId,
        claudeSessionId,
        model,
        tools,
      },
    ];
  }

  if (type === "stream_event" && isRecord(event.event)) {
    const streamType = asString(event.event.type);

    if (streamType === "content_block_delta" && isRecord(event.event.delta)) {
      const deltaType = asString(event.event.delta.type);
      const text = asString(event.event.delta.text);

      if (deltaType === "text_delta" && text) {
        return [{ type: "chat:delta", sessionId, text }];
      }
    }

    if (streamType === "content_block_start" && isRecord(event.event.content_block)) {
      const blockType = asString(event.event.content_block.type);
      if (blockType === "tool_use") {
        const toolUseId = asString(event.event.content_block.id) ?? "unknown-tool-use";
        const name = asString(event.event.content_block.name) ?? "unknown-tool";
        const input = isRecord(event.event.content_block.input) ? event.event.content_block.input : {};

        return [{ type: "tool:start", sessionId, toolUseId, name, input }];
      }
    }

    return [];
  }

  if (type === "assistant") {
    const toolUses = extractToolUseFromAssistantMessage(event.message);
    return toolUses.map((toolUse) => ({
      type: "tool:start" as const,
      sessionId,
      toolUseId: toolUse.toolUseId,
      name: toolUse.name,
      input: toolUse.input,
    }));
  }

  if (type === "user") {
    const toolResults = extractToolResultFromUserMessage(event.message);
    return toolResults.map((toolResult) => ({
      type: "tool:result" as const,
      sessionId,
      toolUseId: toolResult.toolUseId,
      content: toolResult.content,
      isError: toolResult.isError,
    }));
  }

  if (type === "result") {
    const subtype = asString(event.subtype);

    if (subtype === "success") {
      const text = asString(event.result) ?? "";
      const costUsd = typeof event.total_cost_usd === "number" ? event.total_cost_usd : 0;
      const usage = toUsageInfo(event.usage);

      return [
        { type: "chat:complete", sessionId, text },
        { type: "session:complete", sessionId, costUsd, usage },
      ];
    }

    if (subtype === "error") {
      const error = asString(event.error) ?? "Claude Code reported an unknown error.";
      return [{ type: "session:error", sessionId, error }];
    }

    if (subtype === "max_turns") {
      return [{ type: "session:error", sessionId, error: "Turn limit reached (max_turns)." }];
    }

    // Claude CLI may emit additional error-like subtypes (for example: error_during_execution).
    const isError = event.is_error === true;
    if (isError) {
      const directError = asString(event.error);
      const errors = Array.isArray(event.errors)
        ? event.errors.filter((item): item is string => typeof item === "string")
        : [];

      const error =
        directError ??
        (errors.length > 0 ? errors[0] : `Claude Code result error${subtype ? ` (${subtype})` : ""}.`);

      return [{ type: "session:error", sessionId, error }];
    }
  }

  return [];
}
