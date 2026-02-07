import { spawn, type ChildProcess } from "node:child_process";
import { mkdir, rename, writeFile } from "node:fs/promises";
import path from "node:path";

import {
  DEFAULT_MAX_TURNS,
  DEFAULT_PERMISSION_MODE,
  DEFAULT_SYSTEM_PROMPT,
  LOG_TRUNCATE_STREAM_LINE,
  LOG_TRUNCATE_USER_TEXT,
} from "./defaults";
import { filterChildEnv, redactForLogs } from "./env-filter";
import { appendLog } from "./logger";
import { mapClaudeEventToUiEvents, parseNdjsonLine } from "./stream-parser";
import type { LogEntry, Session, TurnOpts, UIEvent } from "./types";

declare global {
  var __chiralityHarnessManager: ClaudeCodeManager | undefined;
  var __chiralityHarnessSessionStore: Map<string, Session> | undefined;
}

type CloseInfo = { code: number | null; signal: string | null };

class AsyncQueue<T> {
  private values: T[] = [];
  private waiters: Array<(result: IteratorResult<T>) => void> = [];
  private isClosed = false;

  push(value: T): void {
    if (this.isClosed) {
      return;
    }

    const waiter = this.waiters.shift();
    if (waiter) {
      waiter({ value, done: false });
      return;
    }

    this.values.push(value);
  }

  close(): void {
    if (this.isClosed) {
      return;
    }

    this.isClosed = true;
    while (this.waiters.length > 0) {
      const waiter = this.waiters.shift();
      if (waiter) {
        waiter({ value: undefined as T, done: true });
      }
    }
  }

  async next(): Promise<IteratorResult<T>> {
    const value = this.values.shift();
    if (typeof value !== "undefined") {
      return { value, done: false };
    }

    if (this.isClosed) {
      return { value: undefined as T, done: true };
    }

    return new Promise<IteratorResult<T>>((resolve) => {
      this.waiters.push(resolve);
    });
  }

  [Symbol.asyncIterator](): AsyncIterator<T> {
    return {
      next: () => this.next(),
    };
  }
}

function truncate(text: string, max: number): string {
  if (text.length <= max) {
    return text;
  }

  return `${text.slice(0, max)}...[truncated]`;
}

function splitBufferedLines(
  chunk: Buffer,
  state: { buffer: string },
  onLine: (line: string) => void,
): void {
  state.buffer += chunk.toString("utf8");

  let newlineIndex = state.buffer.indexOf("\n");
  while (newlineIndex >= 0) {
    const line = state.buffer.slice(0, newlineIndex);
    state.buffer = state.buffer.slice(newlineIndex + 1);
    onLine(line);
    newlineIndex = state.buffer.indexOf("\n");
  }
}

function flushBufferedLine(state: { buffer: string }, onLine: (line: string) => void): void {
  if (!state.buffer.trim()) {
    state.buffer = "";
    return;
  }

  onLine(state.buffer);
  state.buffer = "";
}

function isResultEvent(event: unknown): boolean {
  if (!event || typeof event !== "object") {
    return false;
  }

  const record = event as Record<string, unknown>;
  return record.type === "result";
}

function isExitSignal(signal: NodeJS.Signals | null): string | null {
  return signal ? String(signal) : null;
}

async function writeSystemPromptFile(
  projectRoot: string,
  sessionId: string,
  promptText: string,
): Promise<string> {
  const promptsDir = path.join(projectRoot, ".chirality", "prompts");
  const filePath = path.join(promptsDir, `${sessionId}-system.txt`);
  const tmpPath = `${filePath}.tmp-${Date.now()}`;

  await mkdir(promptsDir, { recursive: true });
  await writeFile(tmpPath, promptText, "utf8");
  await rename(tmpPath, filePath);

  return filePath;
}

function buildClaudeArgs(session: Session, userMessage: string, promptFile: string, opts?: TurnOpts): string[] {
  const permissionMode = opts?.permissionMode ?? DEFAULT_PERMISSION_MODE;
  const maxTurns = opts?.maxTurns ?? DEFAULT_MAX_TURNS;

  const tools = opts?.toolsOverride ?? opts?.tools;
  const disallowedTools = opts?.disallowedToolsOverride ?? opts?.disallowedTools ?? [];
  const autoApproveTools = opts?.autoApproveToolsOverride ?? opts?.autoApproveTools ?? [];

  const args = [
    "-p",
    userMessage,
    "--output-format",
    "stream-json",
    "--max-turns",
    String(maxTurns),
    "--append-system-prompt-file",
    promptFile,
    "--permission-mode",
    permissionMode,
    "--include-partial-messages",
    "--verbose",
  ];

  if (session.claudeSessionId) {
    args.push("--resume", session.claudeSessionId);
  }

  if (typeof tools === "string" && tools.trim()) {
    args.push("--tools", tools);
  }

  for (const disallowed of disallowedTools) {
    args.push("--disallowedTools", disallowed);
  }

  for (const allowed of autoApproveTools) {
    args.push("--allowedTools", allowed);
  }

  return args;
}

function resolveClaudeExecutable(opts?: TurnOpts): string {
  const candidate = typeof opts?.claudeExecutable === "string" ? opts.claudeExecutable.trim() : "";
  if (!candidate) {
    return "claude";
  }

  // Guardrails: executable override is only honored in non-production runs.
  if (process.env.NODE_ENV === "production") {
    return "claude";
  }

  if (!path.isAbsolute(candidate)) {
    return "claude";
  }

  return candidate;
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

export class ClaudeCodeManager {
  private activeRuns = new Map<string, ChildProcess>();

  isRunning(sessionId: string): boolean {
    return this.activeRuns.has(sessionId);
  }

  interrupt(sessionId: string): boolean {
    const proc = this.activeRuns.get(sessionId);
    if (!proc) {
      return false;
    }

    try {
      return proc.kill("SIGINT");
    } catch {
      return false;
    }
  }

  kill(sessionId: string): boolean {
    const proc = this.activeRuns.get(sessionId);
    if (!proc) {
      return false;
    }

    let signaled = false;
    try {
      signaled = proc.kill("SIGTERM");
    } catch {
      signaled = false;
    }

    setTimeout(() => {
      const stillRunning = this.activeRuns.get(sessionId);
      if (stillRunning === proc) {
        try {
          stillRunning.kill("SIGKILL");
        } catch {
          // Ignore failures while attempting hard-kill.
        }
      }
    }, 5_000);

    return signaled;
  }

  async *startTurn(session: Session, userMessage: string, opts?: TurnOpts): AsyncIterable<UIEvent> {
    if (this.isRunning(session.id)) {
      const conflictErr = new Error(`Session ${session.id} already has an in-flight turn.`);
      (conflictErr as Error & { code?: string }).code = "SESSION_CONFLICT";
      throw conflictErr;
    }

    const startedAt = Date.now();
    const queue = new AsyncQueue<UIEvent>();

    let promptFile: string;
    try {
      promptFile =
        opts?.systemPromptFile ??
        (await writeSystemPromptFile(
          session.projectRoot,
          session.id,
          opts?.systemPromptAppend ?? DEFAULT_SYSTEM_PROMPT,
        ));
    } catch (error) {
      const msg = error instanceof Error ? error.message : String(error);
      throw new Error(`Failed to prepare system prompt file: ${msg}`);
    }

    const args = buildClaudeArgs(session, userMessage, promptFile, opts);
    const claudeExecutable = resolveClaudeExecutable(opts);
    const argsForLog = [...args];
    const promptIndex = argsForLog.indexOf("-p");
    if (promptIndex >= 0 && promptIndex + 1 < argsForLog.length) {
      argsForLog[promptIndex + 1] = "[USER_MESSAGE_REDACTED]";
    }
    const commandForLog = `${claudeExecutable} ${argsForLog
      .map((arg) => (arg.includes(" ") ? JSON.stringify(arg) : arg))
      .join(" ")}`;

    fireAndForgetLog(
      session.projectRoot,
      createLogEntry(session.id, "info", "turn:start", {
        userMessage: truncate(userMessage, LOG_TRUNCATE_USER_TEXT),
        persona: session.persona,
        mode: session.mode,
      }),
    );

    const childEnv = filterChildEnv(process.env);
    if (process.env.ANTHROPIC_API_KEY) {
      childEnv.ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
    }

    const child = spawn(claudeExecutable, args, {
      cwd: session.projectRoot,
      env: childEnv,
      stdio: ["ignore", "pipe", "pipe"],
    });

    this.activeRuns.set(session.id, child);

    fireAndForgetLog(
      session.projectRoot,
      createLogEntry(session.id, "info", "process:spawn", {
        command: commandForLog,
        pid: child.pid ?? null,
        redactions: process.env.ANTHROPIC_API_KEY ? { ANTHROPIC_API_KEY: redactForLogs(process.env.ANTHROPIC_API_KEY) } : undefined,
      }),
    );

    let sawResult = false;
    let spawnError: Error | null = null;

    const stdoutState = { buffer: "" };
    const stderrState = { buffer: "" };

    const emitMappedEvents = (parsedEvent: unknown): void => {
      if (isResultEvent(parsedEvent)) {
        sawResult = true;
      }

      const uiEvents = mapClaudeEventToUiEvents(parsedEvent, session.id);
      for (const event of uiEvents) {
        if (event.type === "session:init") {
          fireAndForgetLog(
            session.projectRoot,
            createLogEntry(session.id, "info", "session:init", {
              claudeSessionId: event.claudeSessionId,
              model: event.model,
              tools: event.tools,
            }),
          );
        }

        if (event.type === "tool:start") {
          fireAndForgetLog(
            session.projectRoot,
            createLogEntry(session.id, "info", "tool:start", {
              toolUseId: event.toolUseId,
              toolName: event.name,
              inputSummary: truncate(JSON.stringify(event.input), LOG_TRUNCATE_USER_TEXT),
            }),
          );
        }

        if (event.type === "tool:result") {
          fireAndForgetLog(
            session.projectRoot,
            createLogEntry(session.id, "info", "tool:result", {
              toolUseId: event.toolUseId,
              isError: event.isError,
              contentLength: event.content.length,
            }),
          );
        }

        if (event.type === "session:complete") {
          fireAndForgetLog(
            session.projectRoot,
            createLogEntry(session.id, "info", "turn:complete", {
              costUsd: event.costUsd,
              inputTokens: event.usage.input_tokens,
              outputTokens: event.usage.output_tokens,
              durationMs: Date.now() - startedAt,
            }),
          );
        }

        if (event.type === "session:error") {
          fireAndForgetLog(
            session.projectRoot,
            createLogEntry(session.id, "warn", "turn:error", {
              error: event.error,
            }),
          );
        }

        queue.push(event);
      }
    };

    const handleStdoutLine = (line: string): void => {
      if (!line.trim()) {
        return;
      }

      const parsedEvent = parseNdjsonLine(line);
      if (parsedEvent === null) {
        fireAndForgetLog(
          session.projectRoot,
          createLogEntry(session.id, "warn", "parse:error", {
            line: truncate(line, LOG_TRUNCATE_STREAM_LINE),
          }),
        );
        return;
      }

      emitMappedEvents(parsedEvent);
    };

    const handleStderrLine = (line: string): void => {
      if (!line.trim()) {
        return;
      }

      fireAndForgetLog(
        session.projectRoot,
        createLogEntry(session.id, "warn", "process:stderr", {
          line: truncate(line, LOG_TRUNCATE_STREAM_LINE),
        }),
      );
    };

    child.stdout?.on("data", (chunk: Buffer) => {
      splitBufferedLines(chunk, stdoutState, handleStdoutLine);
    });

    child.stderr?.on("data", (chunk: Buffer) => {
      splitBufferedLines(chunk, stderrState, handleStderrLine);
    });

    child.on("error", (error) => {
      spawnError = error;
      fireAndForgetLog(
        session.projectRoot,
        createLogEntry(session.id, "error", "process:error", {
          message: error.message,
          stack: error.stack,
        }),
      );
    });

    child.on("close", (code, signal) => {
      flushBufferedLine(stdoutState, handleStdoutLine);
      flushBufferedLine(stderrState, handleStderrLine);

      this.activeRuns.delete(session.id);

      if (!sawResult) {
        const errorMessage = spawnError
          ? `Claude process error: ${spawnError.message}`
          : `Claude exited before a result event (exitCode=${code ?? "null"}, signal=${signal ?? "null"}).`;

        queue.push({
          type: "session:error",
          sessionId: session.id,
          error: errorMessage,
        });
      }

      const closeInfo: CloseInfo = { code, signal: isExitSignal(signal) };
      queue.push({
        type: "process:exit",
        sessionId: session.id,
        code: closeInfo.code,
        signal: closeInfo.signal,
      });

      fireAndForgetLog(
        session.projectRoot,
        createLogEntry(session.id, "info", "process:exit", {
          exitCode: closeInfo.code,
          signal: closeInfo.signal,
          durationMs: Date.now() - startedAt,
        }),
      );

      queue.close();
    });

    for await (const event of queue) {
      yield event;
    }
  }
}

export function getHarnessSessionStore(): Map<string, Session> {
  if (!globalThis.__chiralityHarnessSessionStore) {
    globalThis.__chiralityHarnessSessionStore = new Map<string, Session>();
  }
  return globalThis.__chiralityHarnessSessionStore;
}

export const claudeCodeManager =
  globalThis.__chiralityHarnessManager ?? (globalThis.__chiralityHarnessManager = new ClaudeCodeManager());
