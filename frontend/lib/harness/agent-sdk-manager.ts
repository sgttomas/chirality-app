import { query, type Options as AgentSdkOptions, type Query, type SDKMessage, type SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";
import type { ContentBlock } from "./attachment-resolver";
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

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

type ActiveSubagentRun = {
  toolUseId: string;
  subagentType: string;
  description: string | null;
  startedAt: string;
  childToolStarts: number;
  childToolCompletes: number;
  childToolErrors: number;
};

const SDK_CLI_RELATIVE_PATH = path.join("node_modules", "@anthropic-ai", "claude-agent-sdk", "cli.js");
const DEFAULT_PATH_SEGMENTS = ["/opt/homebrew/bin", "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin"];

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

  const firstError = message.errors.find((item: unknown) => typeof item === "string" && item.trim().length > 0);
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

function normalizeOptionalString(value: unknown): string | null {
  if (typeof value !== "string") {
    return null;
  }

  const trimmed = value.trim();
  return trimmed ? trimmed : null;
}

function resolveClaudeExecutablePath(): string | undefined {
  const fromEnv = process.env.CHIRALITY_CLAUDE_CODE_EXECUTABLE?.trim();
  if (fromEnv) {
    return fromEnv;
  }

  const resourcesPath = (process as NodeJS.Process & { resourcesPath?: string }).resourcesPath;
  const candidates: string[] = [];
  if (typeof resourcesPath === "string" && resourcesPath.trim().length > 0) {
    candidates.push(path.join(resourcesPath, "app.asar.unpacked", SDK_CLI_RELATIVE_PATH));
    candidates.push(path.join(resourcesPath, "app.asar", SDK_CLI_RELATIVE_PATH));
    candidates.push(path.join(resourcesPath, SDK_CLI_RELATIVE_PATH));
  }

  candidates.push(path.join(process.cwd(), SDK_CLI_RELATIVE_PATH));

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }

  return undefined;
}

function prependPathSegment(pathValue: string | undefined, segment: string): string {
  if (!pathValue || pathValue.trim().length === 0) {
    return segment;
  }

  const segments = pathValue.split(":");
  if (segments.includes(segment)) {
    return pathValue;
  }

  return `${segment}:${pathValue}`;
}

function resolveNodeExecutable(env: NodeJS.ProcessEnv): string | undefined {
  const envOverride = env.CHIRALITY_NODE_EXECUTABLE?.trim();
  if (envOverride && fs.existsSync(envOverride)) {
    return envOverride;
  }

  const pathEntries = (env.PATH ?? "")
    .split(":")
    .map((entry) => entry.trim())
    .filter(Boolean);

  const searchEntries = [...new Set([...pathEntries, ...DEFAULT_PATH_SEGMENTS])];
  for (const entry of searchEntries) {
    const candidate = path.join(entry, "node");
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }

  return undefined;
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
  } else {
    const resolvedExecutablePath = resolveClaudeExecutablePath();
    if (resolvedExecutablePath) {
      options.pathToClaudeCodeExecutable = resolvedExecutablePath;
    }
  }

  // ---------------------------------------------------------------------------
  // Subagent injection — guarded assignment.
  //
  // The SDK's Options type may not yet expose `agents` in its TS definition.
  // We cast through Record<string, unknown> to isolate the breakage to this
  // single line if the SDK removes/renames the field. When the SDK type is
  // confirmed stable, replace with direct assignment: options.agents = ...
  // ---------------------------------------------------------------------------
  const hasAgents = opts?.agents && Object.keys(opts.agents).length > 0;
  if (hasAgents) {
    (options as Record<string, unknown>).agents = opts!.agents;
  }

  // ---------------------------------------------------------------------------
  // Task tool enforcement — when subagents are present, the model MUST have
  // access to the Task tool to invoke them. Enforce all three tool knobs:
  //
  //   1. tools      — if explicit array, ensure "Task" included
  //   2. disallowedTools — ensure "Task" is NOT present
  //   3. allowedTools    — ensure "Task" IS present (auto-approve)
  //
  // Also validate subagent definitions: strip "Task" from any subagent's
  // tools array to prevent nesting (least privilege).
  // ---------------------------------------------------------------------------
  if (hasAgents) {
    // 1. Tools: if explicit array (not preset), ensure "Task" is included
    if (Array.isArray(options.tools) && !options.tools.includes("Task")) {
      options.tools.push("Task");
    }

    // 2. disallowedTools: strip "Task" if present
    if (Array.isArray(options.disallowedTools) && options.disallowedTools.includes("Task")) {
      console.warn("[harness] Stripping 'Task' from disallowedTools — required for subagent invocation.");
      options.disallowedTools = options.disallowedTools.filter((t) => t !== "Task");
    }

    // 3. allowedTools: ensure "Task" is present for auto-approve
    if (Array.isArray(options.allowedTools) && !options.allowedTools.includes("Task")) {
      options.allowedTools = [...options.allowedTools, "Task"];
    }

    // Validate subagent definitions: strip "Task" from subagent tools to prevent nesting
    const agentsRecord = (options as Record<string, unknown>).agents as Record<string, { tools?: string[] }> | undefined;
    if (agentsRecord) {
      for (const [agentId, def] of Object.entries(agentsRecord)) {
        if (Array.isArray(def.tools) && def.tools.includes("Task")) {
          console.warn(`[harness] Stripping 'Task' from subagent '${agentId}' tools — nesting not permitted.`);
          def.tools = def.tools.filter((t) => t !== "Task");
        }
      }
    }
  }

  if (session.claudeSessionId) {
    options.resume = session.claudeSessionId;
  }

  const runtimeEnv: NodeJS.ProcessEnv = { ...process.env };
  if (opts?.apiKey) {
    runtimeEnv.ANTHROPIC_API_KEY = opts.apiKey;
  }
  for (const segment of DEFAULT_PATH_SEGMENTS) {
    runtimeEnv.PATH = prependPathSegment(runtimeEnv.PATH, segment);
  }

  const resolvedNodeExecutable = resolveNodeExecutable(runtimeEnv);
  if (resolvedNodeExecutable) {
    runtimeEnv.PATH = prependPathSegment(runtimeEnv.PATH, path.dirname(resolvedNodeExecutable));
    options.spawnClaudeCodeProcess = (spawnOptions) => {
      const command = spawnOptions.command === "node" ? resolvedNodeExecutable : spawnOptions.command;
      const childEnv: NodeJS.ProcessEnv = {
        ...spawnOptions.env,
        NODE_ENV: process.env.NODE_ENV ?? "production",
      };
      return spawn(command, spawnOptions.args, {
        cwd: spawnOptions.cwd,
        env: childEnv,
        signal: spawnOptions.signal,
        stdio: ["pipe", "pipe", "pipe"],
      });
    };
  }
  options.env = runtimeEnv;

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

  async *startTurn(session: Session, userMessage: string, opts?: TurnOpts, contentBlocks?: ContentBlock[]): AsyncIterable<UIEvent> {
    if (this.isRunning(session.id)) {
      const conflictErr = new Error(`Session ${session.id} already has an in-flight turn.`);
      (conflictErr as Error & { code?: string }).code = "SESSION_CONFLICT";
      throw conflictErr;
    }

    const startedAt = Date.now();
    const abortController = new AbortController();

    let promptValue: string | AsyncIterable<SDKUserMessage>;
    if (contentBlocks && contentBlocks.length > 0) {
      const userMsg: SDKUserMessage = {
        type: "user",
        message: { role: "user", content: contentBlocks } as SDKUserMessage["message"],
        parent_tool_use_id: null,
        session_id: session.claudeSessionId || session.id,
      };
      async function* singleMessage() {
        yield userMsg;
      }
      promptValue = singleMessage();
    } else {
      promptValue = userMessage;
    }

    const sdkQuery = query({
      prompt: promptValue,
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

    const injectedAgentIds = opts?.agents ? Object.keys(opts.agents) : [];
    if (injectedAgentIds.length > 0) {
      fireAndForgetLog(
        session.projectRoot,
        createLogEntry(session.id, "info", "subagent:registry_applied", {
          status: "applied",
          count: injectedAgentIds.length,
          agentIds: injectedAgentIds,
          appliedAt: new Date().toISOString(),
        }),
      );
    }

    const activeSubagentRuns = new Map<string, ActiveSubagentRun>();
    const toolParentByUseId = new Map<string, string | null>();
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
            const hadParentLink = toolParentByUseId.has(uiEvent.toolUseId);
            const parentToolUseId =
              normalizeOptionalString(uiEvent.parentToolUseId) ??
              normalizeOptionalString(toolParentByUseId.get(uiEvent.toolUseId));
            if (parentToolUseId) {
              toolParentByUseId.set(uiEvent.toolUseId, parentToolUseId);
            }

            fireAndForgetLog(
              session.projectRoot,
              createLogEntry(session.id, "info", "tool:start", {
                toolUseId: uiEvent.toolUseId,
                toolName: uiEvent.name,
                parentToolUseId,
                inputSummary: truncate(JSON.stringify(uiEvent.input), LOG_TRUNCATE_USER_TEXT),
              }),
            );

            if (uiEvent.name === "Task") {
              const startedAt = new Date().toISOString();
              const subagentType = normalizeOptionalString(uiEvent.input.subagent_type) ?? "unknown";
              const description = normalizeOptionalString(uiEvent.input.description);
              const subagentRun: ActiveSubagentRun = {
                toolUseId: uiEvent.toolUseId,
                subagentType,
                description,
                startedAt,
                childToolStarts: 0,
                childToolCompletes: 0,
                childToolErrors: 0,
              };
              activeSubagentRuns.set(uiEvent.toolUseId, subagentRun);
              fireAndForgetLog(
                session.projectRoot,
                createLogEntry(session.id, "info", "subagent:start", {
                  toolUseId: subagentRun.toolUseId,
                  subagentType: subagentRun.subagentType,
                  description: subagentRun.description,
                  status: "started",
                  startedAt: subagentRun.startedAt,
                }),
              );
            } else if (parentToolUseId && !hadParentLink) {
              const parentSubagentRun = activeSubagentRuns.get(parentToolUseId);
              if (parentSubagentRun) {
                parentSubagentRun.childToolStarts += 1;
                fireAndForgetLog(
                  session.projectRoot,
                  createLogEntry(session.id, "info", "subagent:child_tool_start", {
                    parentToolUseId,
                    subagentType: parentSubagentRun.subagentType,
                    childToolUseId: uiEvent.toolUseId,
                    childToolName: uiEvent.name,
                    childToolStarts: parentSubagentRun.childToolStarts,
                  }),
                );
              }
            }
          }

          if (uiEvent.type === "tool:progress") {
            const hadParentLink = toolParentByUseId.has(uiEvent.toolUseId);
            const parentToolUseId =
              normalizeOptionalString(uiEvent.parentToolUseId) ??
              normalizeOptionalString(toolParentByUseId.get(uiEvent.toolUseId));
            if (parentToolUseId) {
              toolParentByUseId.set(uiEvent.toolUseId, parentToolUseId);

              if (!hadParentLink) {
                const parentSubagentRun = activeSubagentRuns.get(parentToolUseId);
                if (parentSubagentRun) {
                  parentSubagentRun.childToolStarts += 1;
                  fireAndForgetLog(
                    session.projectRoot,
                    createLogEntry(session.id, "info", "subagent:child_tool_start", {
                      parentToolUseId,
                      subagentType: parentSubagentRun.subagentType,
                      childToolUseId: uiEvent.toolUseId,
                      childToolName: uiEvent.name,
                      childToolStarts: parentSubagentRun.childToolStarts,
                      source: "tool_progress",
                    }),
                  );
                }
              }
            }

            fireAndForgetLog(
              session.projectRoot,
              createLogEntry(session.id, "info", "tool:progress", {
                toolUseId: uiEvent.toolUseId,
                toolName: uiEvent.name,
                parentToolUseId,
                elapsedSeconds: uiEvent.elapsedSeconds,
              }),
            );
          }

          if (uiEvent.type === "tool:result") {
            const parentToolUseId =
              normalizeOptionalString(uiEvent.parentToolUseId) ??
              normalizeOptionalString(toolParentByUseId.get(uiEvent.toolUseId));
            if (parentToolUseId) {
              toolParentByUseId.set(uiEvent.toolUseId, parentToolUseId);
            }

            fireAndForgetLog(
              session.projectRoot,
              createLogEntry(session.id, "info", "tool:result", {
                toolUseId: uiEvent.toolUseId,
                parentToolUseId,
                isError: uiEvent.isError,
                contentLength: uiEvent.content.length,
              }),
            );

            if (parentToolUseId) {
              const parentSubagentRun = activeSubagentRuns.get(parentToolUseId);
              if (parentSubagentRun) {
                if (uiEvent.isError) {
                  parentSubagentRun.childToolErrors += 1;
                } else {
                  parentSubagentRun.childToolCompletes += 1;
                }

                fireAndForgetLog(
                  session.projectRoot,
                  createLogEntry(session.id, "info", "subagent:child_tool_result", {
                    parentToolUseId,
                    subagentType: parentSubagentRun.subagentType,
                    childToolUseId: uiEvent.toolUseId,
                    isError: uiEvent.isError,
                    childToolCompletes: parentSubagentRun.childToolCompletes,
                    childToolErrors: parentSubagentRun.childToolErrors,
                  }),
                );
              }
            }

            const subagentRun = activeSubagentRuns.get(uiEvent.toolUseId);
            if (subagentRun) {
              const finishedAt = new Date().toISOString();
              const terminalEvent = uiEvent.isError ? "subagent:interrupted" : "subagent:complete";
              const status = uiEvent.isError ? "interrupted" : "complete";
              fireAndForgetLog(
                session.projectRoot,
                createLogEntry(session.id, "info", terminalEvent, {
                  toolUseId: subagentRun.toolUseId,
                  subagentType: subagentRun.subagentType,
                  description: subagentRun.description,
                  status,
                  startedAt: subagentRun.startedAt,
                  finishedAt,
                  childToolStarts: subagentRun.childToolStarts,
                  childToolCompletes: subagentRun.childToolCompletes,
                  childToolErrors: subagentRun.childToolErrors,
                }),
              );
              activeSubagentRuns.delete(uiEvent.toolUseId);
            }

            toolParentByUseId.delete(uiEvent.toolUseId);
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
    const finishedAt = new Date().toISOString();

    for (const subagentRun of activeSubagentRuns.values()) {
      fireAndForgetLog(
        session.projectRoot,
        createLogEntry(session.id, "info", "subagent:interrupted", {
          toolUseId: subagentRun.toolUseId,
          subagentType: subagentRun.subagentType,
          description: subagentRun.description,
          status: "interrupted",
          startedAt: subagentRun.startedAt,
          finishedAt,
          childToolStarts: subagentRun.childToolStarts,
          childToolCompletes: subagentRun.childToolCompletes,
          childToolErrors: subagentRun.childToolErrors,
          reason: signal ?? surfacedRuntimeError ?? "process_exit",
        }),
      );
    }
    activeSubagentRuns.clear();
    toolParentByUseId.clear();

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
