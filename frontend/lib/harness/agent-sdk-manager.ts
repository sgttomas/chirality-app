import { query, type Options as AgentSdkOptions, type Query, type SDKMessage } from "@anthropic-ai/claude-agent-sdk";

import {
  CLAUDE_CODE_SYSTEM_PROMPT_PRESET,
  CLAUDE_CODE_TOOLS_PRESET,
  DEFAULT_INCLUDE_PARTIAL_MESSAGES,
  DEFAULT_MAX_TURNS,
  DEFAULT_PERMISSION_MODE,
  DEFAULT_SETTING_SOURCES,
  LOG_TRUNCATE_USER_TEXT,
} from "./defaults";
import { mapSdkMessageToUiEvents } from "./agent-sdk-event-mapper";
import { appendLog } from "./logger";
import type { LogEntry, Session, TurnOpts, UIEvent } from "./types";

declare global {
  var __chiralityHarnessAgentSdkManager: AgentSdkManager | undefined;
}

type ActiveRun = {
  query: Query;
  abortController: AbortController;
  interruptRequested: boolean;
  killRequested: boolean;
};

function truncate(text: string, max: number): string {
  if (text.length <= max) {
    return text;
  }

  return `${text.slice(0, max)}...[truncated]`;
}

function createLogEntry(
  sessionId: string,
  level: LogEntry["level"],
  event: string,
  data?: Record<string, unknown>,
): LogEntry {
  return {
    timestamp: new Date().toISOString(),
    sessionId,
    level,
    event,
    data,
  };
}

function fireAndForgetLog(projectRoot: string, entry: LogEntry): void {
  void appendLog(projectRoot, entry);
}

function normalizeModel(model: unknown): string | undefined {
  if (typeof model !== "string") {
    return undefined;
  }

  const trimmed = model.trim();
  return trimmed ? trimmed : undefined;
}

function getMessageError(message: SDKMessage): string | null {
  if (message.type !== "result" || message.subtype === "success") {
    return null;
  }

  const firstError = message.errors.find((item) => typeof item === "string" && item.trim().length > 0);
  if (firstError) {
    return firstError;
  }

  if (message.subtype === "error_max_turns") {
    return "Turn limit reached (max_turns).";
  }

  return `Claude Agent SDK reported ${message.subtype}.`;
}

function resolveModelForLog(opts?: TurnOpts): string | null {
  if (typeof opts?.model !== "string") {
    return null;
  }

  const trimmed = opts.model.trim();
  return trimmed ? trimmed : null;
}

function splitCsvTools(value: string | undefined): string[] {
  if (typeof value !== "string") {
    return [];
  }

  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function resolveToolRestriction(opts: TurnOpts | undefined): AgentSdkOptions["tools"] {
  const toolsValue = opts?.toolsOverride ?? opts?.tools;
  const configuredTools = splitCsvTools(toolsValue);
  if (configuredTools.length > 0) {
    return configuredTools;
  }

  return {
    type: "preset",
    preset: CLAUDE_CODE_TOOLS_PRESET,
  };
}

function resolvePermissionSettings(opts: TurnOpts | undefined): {
  permissionMode: NonNullable<AgentSdkOptions["permissionMode"]>;
  allowDangerouslySkipPermissions?: boolean;
} {
  const mode = opts?.permissionMode ?? DEFAULT_PERMISSION_MODE;
  if (mode === "dontAsk") {
    return {
      permissionMode: "bypassPermissions",
      allowDangerouslySkipPermissions: true,
    };
  }

  return {
    permissionMode: mode,
  };
}

function toAgentSdkOptions(session: Session, opts: TurnOpts | undefined, abortController: AbortController): AgentSdkOptions {
  const permissionSettings = resolvePermissionSettings(opts);
  const disallowedTools = opts?.disallowedToolsOverride ?? opts?.disallowedTools ?? [];
  const autoApproveTools = opts?.autoApproveToolsOverride ?? opts?.autoApproveTools ?? [];

  const options: AgentSdkOptions = {
    cwd: session.projectRoot,
    abortController,
    permissionMode: permissionSettings.permissionMode,
    maxTurns: opts?.maxTurns ?? DEFAULT_MAX_TURNS,
    includePartialMessages: opts?.includePartialMessages ?? DEFAULT_INCLUDE_PARTIAL_MESSAGES,
    tools: resolveToolRestriction(opts),
    disallowedTools,
    allowedTools: autoApproveTools,
    settingSources: opts?.settingSources ?? [...DEFAULT_SETTING_SOURCES],
    systemPrompt: {
      type: "preset",
      preset: CLAUDE_CODE_SYSTEM_PROMPT_PRESET,
      append: opts?.systemPromptAppend,
    },
  };

  const model = normalizeModel(opts?.model);
  if (model) {
    options.model = model;
  }

  if (permissionSettings.allowDangerouslySkipPermissions) {
    options.allowDangerouslySkipPermissions = true;
  }

  if (opts?.pathToClaudeCodeExecutable) {
    options.pathToClaudeCodeExecutable = opts.pathToClaudeCodeExecutable;
  }

  if (session.claudeSessionId) {
    options.resume = session.claudeSessionId;
  }

  if (opts?.apiKey) {
    options.env = {
      ...process.env,
      ANTHROPIC_API_KEY: opts.apiKey,
    };
  }

  return options;
}

export class AgentSdkManager {
  private activeRuns = new Map<string, ActiveRun>();

  isRunning(sessionId: string): boolean {
    return this.activeRuns.has(sessionId);
  }

  interrupt(sessionId: string): boolean {
    const active = this.activeRuns.get(sessionId);
    if (!active) {
      return false;
    }

    active.interruptRequested = true;
    void active.query.interrupt().catch(() => {
      active.abortController.abort();
    });

    return true;
  }

  kill(sessionId: string): boolean {
    const active = this.activeRuns.get(sessionId);
    if (!active) {
      return false;
    }

    active.killRequested = true;
    active.abortController.abort();
    active.query.close();
    return true;
  }

  async *startTurn(session: Session, userMessage: string, opts?: TurnOpts): AsyncIterable<UIEvent> {
    if (this.isRunning(session.id)) {
      const conflictErr = new Error(`Session ${session.id} already has an in-flight turn.`);
      (conflictErr as Error & { code?: string }).code = "SESSION_CONFLICT";
      throw conflictErr;
    }

    const startedAt = Date.now();
    const abortController = new AbortController();
    const sdkQuery = query({
      prompt: userMessage,
      options: toAgentSdkOptions(session, opts, abortController),
    });

    const activeRun: ActiveRun = {
      query: sdkQuery,
      abortController,
      interruptRequested: false,
      killRequested: false,
    };

    this.activeRuns.set(session.id, activeRun);

    fireAndForgetLog(
      session.projectRoot,
      createLogEntry(session.id, "info", "turn:start", {
        userMessage: truncate(userMessage, LOG_TRUNCATE_USER_TEXT),
        persona: session.persona,
        mode: session.mode,
      }),
    );

    const resolvedModel = resolveModelForLog(opts);
    fireAndForgetLog(
      session.projectRoot,
      createLogEntry(session.id, "info", "turn:model", {
        resolvedModel,
        usedModelFlag: Boolean(resolvedModel),
      }),
    );

    let surfacedRuntimeError: string | null = null;

    try {
      for await (const sdkMessage of sdkQuery) {
        const mappedEvents = mapSdkMessageToUiEvents(sdkMessage, session.id);
        for (const uiEvent of mappedEvents) {
          if (uiEvent.type === "session:init") {
            fireAndForgetLog(
              session.projectRoot,
              createLogEntry(session.id, "info", "session:init", {
                claudeSessionId: uiEvent.claudeSessionId,
                model: uiEvent.model,
                tools: uiEvent.tools,
              }),
            );
          }

          if (uiEvent.type === "tool:start") {
            fireAndForgetLog(
              session.projectRoot,
              createLogEntry(session.id, "info", "tool:start", {
                toolUseId: uiEvent.toolUseId,
                toolName: uiEvent.name,
                inputSummary: truncate(JSON.stringify(uiEvent.input), LOG_TRUNCATE_USER_TEXT),
              }),
            );
          }

          if (uiEvent.type === "tool:result") {
            fireAndForgetLog(
              session.projectRoot,
              createLogEntry(session.id, "info", "tool:result", {
                toolUseId: uiEvent.toolUseId,
                isError: uiEvent.isError,
                contentLength: uiEvent.content.length,
              }),
            );
          }

          if (uiEvent.type === "session:complete") {
            fireAndForgetLog(
              session.projectRoot,
              createLogEntry(session.id, "info", "turn:complete", {
                costUsd: uiEvent.costUsd,
                inputTokens: uiEvent.usage.input_tokens,
                outputTokens: uiEvent.usage.output_tokens,
                durationMs: Date.now() - startedAt,
              }),
            );
          }

          if (uiEvent.type === "session:error") {
            fireAndForgetLog(
              session.projectRoot,
              createLogEntry(session.id, "warn", "turn:error", {
                error: uiEvent.error,
              }),
            );
          }

          yield uiEvent;
        }

        const resultError = getMessageError(sdkMessage);
        if (resultError) {
          surfacedRuntimeError = resultError;
        }
      }
    } catch (error) {
      surfacedRuntimeError = error instanceof Error ? error.message : String(error);
      fireAndForgetLog(
        session.projectRoot,
        createLogEntry(session.id, "error", "turn:error", {
          error: surfacedRuntimeError,
        }),
      );
      yield {
        type: "session:error",
        sessionId: session.id,
        error: surfacedRuntimeError,
      };
    } finally {
      this.activeRuns.delete(session.id);
      sdkQuery.close();
    }

    const signal = activeRun.interruptRequested ? "SIGINT" : activeRun.killRequested ? "SIGTERM" : null;
    const code = signal ? null : surfacedRuntimeError ? 1 : 0;

    fireAndForgetLog(
      session.projectRoot,
      createLogEntry(session.id, "info", "process:exit", {
        exitCode: code,
        signal,
        durationMs: Date.now() - startedAt,
      }),
    );

    yield {
      type: "process:exit",
      sessionId: session.id,
      code,
      signal,
    };
  }
}

export const agentSdkManager =
  globalThis.__chiralityHarnessAgentSdkManager ??
  (globalThis.__chiralityHarnessAgentSdkManager = new AgentSdkManager());
