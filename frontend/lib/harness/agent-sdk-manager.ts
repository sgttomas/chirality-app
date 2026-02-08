import { query, type Options as AgentSdkOptions, type Query, type SDKMessage } from "@anthropic-ai/claude-agent-sdk";

import { DEFAULT_INCLUDE_PARTIAL_MESSAGES, DEFAULT_MAX_TURNS, DEFAULT_PERMISSION_MODE } from "./defaults";
import { mapSdkMessageToUiEvents } from "./agent-sdk-event-mapper";
import type { Session, TurnOpts, UIEvent } from "./types";

declare global {
  var __chiralityHarnessAgentSdkManager: AgentSdkManager | undefined;
}

type ActiveRun = {
  query: Query;
  abortController: AbortController;
  interruptRequested: boolean;
  killRequested: boolean;
};

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

function toAgentSdkOptions(session: Session, opts: TurnOpts | undefined, abortController: AbortController): AgentSdkOptions {
  const options: AgentSdkOptions = {
    cwd: session.projectRoot,
    abortController,
    permissionMode: opts?.permissionMode ?? DEFAULT_PERMISSION_MODE,
    maxTurns: opts?.maxTurns ?? DEFAULT_MAX_TURNS,
    includePartialMessages: opts?.includePartialMessages ?? DEFAULT_INCLUDE_PARTIAL_MESSAGES,
  };

  const model = normalizeModel(opts?.model);
  if (model) {
    options.model = model;
  }

  if (opts?.settingSources) {
    options.settingSources = opts.settingSources;
  }

  if (opts?.pathToClaudeCodeExecutable) {
    options.pathToClaudeCodeExecutable = opts.pathToClaudeCodeExecutable;
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

    let surfacedRuntimeError: string | null = null;

    try {
      for await (const sdkMessage of sdkQuery) {
        const mappedEvents = mapSdkMessageToUiEvents(sdkMessage, session.id);
        for (const uiEvent of mappedEvents) {
          yield uiEvent;
        }

        const resultError = getMessageError(sdkMessage);
        if (resultError) {
          surfacedRuntimeError = resultError;
        }
      }
    } catch (error) {
      surfacedRuntimeError = error instanceof Error ? error.message : String(error);
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
