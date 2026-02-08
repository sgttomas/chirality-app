"use client";

import React, { useState, useRef, useEffect, useImperativeHandle, forwardRef } from "react";
import Convert from "ansi-to-html";

import type { UIEvent } from "@/lib/harness/types";

type ViewMode = "agent" | "direct";
type HarnessMode = "workbench" | "pipeline" | "direct";

type Message = {
  role: "user" | "assistant";
  content: string;
  streaming?: boolean;
};

type HarnessSessionMeta = {
  sessionId: string | null;
  claudeSessionId: string | null;
  mode: HarnessMode;
  persona: string | null;
  model: string | null;
  tools: string[];
  lastCompletedAt: string | null;
  lastCostUsd: number | null;
  projectRoot: string | null;
};

type LocalChatSession = {
  id: string;
  name: string;
  messages: Message[];
  cwd: string;
  harness: HarnessSessionMeta;
};

type HarnessSessionPayload = {
  id: string;
  createdAt: string;
  updatedAt: string;
  projectRoot: string;
  persona: string | null;
  mode: HarnessMode;
  claudeSessionId: string | null;
};

type ToolChipStatus = "running" | "done" | "error";

type ToolChip = {
  toolUseId: string;
  name: string;
  status: ToolChipStatus;
};

interface ChatPanelProps {
  agentName: string;
  width: number;
  onResize: (delta: number) => void;
  placeholder?: string;
  sessionId: string;
  autoPrompt?: string | null;
  mode?: ViewMode;
  harnessMode: HarnessMode;
  personaId: string | null;
  projectRoot: string | null;
}

export interface ChatPanelHandle {
  injectMessage: (message: string) => void;
}

const convert = new Convert({
  fg: "#f8fafc",
  bg: "transparent",
  newline: false, // whitespace-pre-wrap handles this
  escapeXML: true,
  stream: false,
});

/**
 * Pre-processes string to ensure ANSI escape codes are in a format 
 * ansi-to-html understands (converting literal \033 or \u001b if they exist).
 */
function prepareAnsiContent(content: string): string {
  if (!content) return "";
  return content
    .replace(/\\033/g, "\x1b")
    .replace(/\\u001b/g, "\x1b")
    .replace(/\\e/g, "\x1b");
}

function trimString(value: unknown): string | null {
  if (typeof value !== "string") {
    return null;
  }
  const trimmed = value.trim();
  return trimmed ? trimmed : null;
}

function truncate(text: string, maxChars: number): string {
  if (text.length <= maxChars) {
    return text;
  }
  return `${text.slice(0, maxChars)}...`;
}

const TOOL_STATUS_LABELS: Record<string, string> = {
  read_file: "Reading file",
  write_file: "Writing file",
  execute_command: "Running command",
  list_directory: "Scanning directory",
  search_file_content: "Searching files",
  glob: "Finding files",
};

const BRAILLE_SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"] as const;
const TOOL_CHIP_LIMIT = 4;
const TOOL_CHIP_SETTLE_MS = 2200;

function humanizeToolName(toolName: string): string {
  return toolName
    .replace(/[_-]+/g, " ")
    .trim()
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function toolStatusLabel(toolName: string): string {
  return TOOL_STATUS_LABELS[toolName] ?? humanizeToolName(toolName);
}

function formatCostUsd(cost: number | null): string {
  if (cost === null || Number.isNaN(cost)) {
    return "n/a";
  }
  if (cost < 0.01) {
    return `<$${0.01.toFixed(2)}`;
  }
  return `$${cost.toFixed(2)}`;
}

function shortSessionId(sessionId: string | null): string {
  if (!sessionId) {
    return "pending";
  }
  return sessionId.slice(0, 8);
}

function formatRunTime(isoTimestamp: string | null): string {
  if (!isoTimestamp) {
    return "--:--";
  }
  const parsed = new Date(isoTimestamp);
  if (Number.isNaN(parsed.getTime())) {
    return "--:--";
  }
  return parsed.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function formatFolderLabel(pathValue: string): string {
  const cleaned = pathValue.trim();
  if (!cleaned || cleaned === "~") {
    return "~";
  }

  const normalized = cleaned.replace(/\/+$/, "");
  if (!normalized) {
    return "/";
  }

  const parts = normalized.split("/").filter(Boolean);
  return parts[parts.length - 1] || "/";
}

function initialAssistantMessage(mode: ViewMode, agentName: string): Message {
  return {
    role: "assistant",
    content:
      mode === "agent"
        ? `System initialized. ${agentName} ready.`
        : "Direct connection established. Commands ready.",
  };
}

function buildHarnessMeta(
  harnessMode: HarnessMode,
  personaId: string | null,
  projectRoot: string | null,
  existing?: Partial<HarnessSessionMeta>,
): HarnessSessionMeta {
  const sameContract =
    existing?.mode === harnessMode &&
    (existing?.persona ?? null) === (personaId ?? null) &&
    (existing?.projectRoot ?? projectRoot ?? null) === (projectRoot ?? null);

  return {
    sessionId: sameContract ? existing?.sessionId ?? null : null,
    claudeSessionId: sameContract ? existing?.claudeSessionId ?? null : null,
    mode: harnessMode,
    persona: personaId ?? null,
    model: sameContract ? existing?.model ?? null : null,
    tools: sameContract ? existing?.tools ?? [] : [],
    lastCompletedAt: sameContract ? existing?.lastCompletedAt ?? null : null,
    lastCostUsd: sameContract ? existing?.lastCostUsd ?? null : null,
    projectRoot: projectRoot ?? existing?.projectRoot ?? null,
  };
}

function createLocalSession(
  mode: ViewMode,
  agentName: string,
  harnessMode: HarnessMode,
  personaId: string | null,
  projectRoot: string | null,
): LocalChatSession {
  return {
    id: crypto.randomUUID(),
    name: `Session ${new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`,
    messages: [initialAssistantMessage(mode, agentName)],
    cwd: projectRoot ?? "~",
    harness: buildHarnessMeta(harnessMode, personaId, projectRoot),
  };
}

function normalizeStoredSessions(
  raw: unknown,
  mode: ViewMode,
  agentName: string,
  harnessMode: HarnessMode,
  personaId: string | null,
  projectRoot: string | null,
): LocalChatSession[] {
  if (!Array.isArray(raw)) {
    return [];
  }

  const seenIds = new Set<string>();
  const normalized: LocalChatSession[] = [];

  for (const candidate of raw) {
    if (!candidate || typeof candidate !== "object") {
      continue;
    }

    const record = candidate as Record<string, unknown>;
    let id = trimString(record.id) ?? crypto.randomUUID();

    if (seenIds.has(id) || !Number.isNaN(Number(id))) {
      id = crypto.randomUUID();
    }

    seenIds.add(id);

    const rawMessages = Array.isArray(record.messages) ? record.messages : [];
    const messages: Message[] = rawMessages
      .map((message) => {
        if (!message || typeof message !== "object") {
          return null;
        }
        const msgRecord = message as Record<string, unknown>;
        const role = msgRecord.role === "user" || msgRecord.role === "assistant" ? msgRecord.role : null;
        const content = typeof msgRecord.content === "string" ? msgRecord.content : null;
        if (!role || content === null) {
          return null;
        }
        return { role, content, streaming: false } as Message;
      })
      .filter((message): message is Message => Boolean(message));

    const fallbackCwd = projectRoot ?? "~";
    const cwd = trimString(record.cwd) ?? fallbackCwd;

    const rawHarness =
      record.harness && typeof record.harness === "object"
        ? (record.harness as Partial<HarnessSessionMeta>)
        : undefined;

    const harness = buildHarnessMeta(harnessMode, personaId, projectRoot, {
      sessionId: trimString(rawHarness?.sessionId) ?? null,
      claudeSessionId: trimString(rawHarness?.claudeSessionId) ?? null,
      model: trimString(rawHarness?.model) ?? null,
      tools: Array.isArray(rawHarness?.tools)
        ? rawHarness.tools.filter((tool): tool is string => typeof tool === "string")
        : [],
      lastCompletedAt: trimString(rawHarness?.lastCompletedAt) ?? null,
      lastCostUsd: typeof rawHarness?.lastCostUsd === "number" ? rawHarness.lastCostUsd : null,
      mode: rawHarness?.mode,
      persona: rawHarness?.persona,
      projectRoot: trimString(rawHarness?.projectRoot) ?? projectRoot,
    });

    normalized.push({
      id,
      name: trimString(record.name) ?? `Session ${new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`,
      messages: messages.length > 0 ? messages : [initialAssistantMessage(mode, agentName)],
      cwd,
      harness,
    });
  }

  return normalized;
}

async function consumeSseStream(
  stream: ReadableStream<Uint8Array>,
  onEvent: (eventName: string, payload: string) => void,
): Promise<void> {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // SSE blocks are delimited by double newlines
    let boundaryIndex;
    while ((boundaryIndex = buffer.indexOf("\n\n")) >= 0) {
      const block = buffer.slice(0, boundaryIndex);
      buffer = buffer.slice(boundaryIndex + 2);

      let eventName = "message";
      let data = "";

      const lines = block.split("\n");
      for (const line of lines) {
        if (line.startsWith("event:")) {
          eventName = line.slice(6).trim();
        } else if (line.startsWith("data:")) {
          data += (data ? "\n" : "") + line.slice(5).trimStart();
        }
      }

      if (data) {
        onEvent(eventName, data);
      }
    }
  }

  reader.releaseLock();
}

export const ChatPanel = forwardRef<ChatPanelHandle, ChatPanelProps>(
  (
    {
      agentName,
      width,
      placeholder = "Send instruction...",
      sessionId: viewId,
      autoPrompt,
      mode = "agent",
      harnessMode,
      personaId,
      projectRoot,
    },
    ref,
  ) => {
    const [sessions, setSessions] = useState<LocalChatSession[]>([]);
    const [activeSessionId, setActiveSessionId] = useState<string>("");
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [isInterrupting, setIsInterrupting] = useState(false);
    const [statusText, setStatusText] = useState<string>("Ready");
    const [activeTools, setActiveTools] = useState<ToolChip[]>([]);
    const [spinnerFrameIndex, setSpinnerFrameIndex] = useState(0);
    const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);
    const [inFlightHarnessSessionId, setInFlightHarnessSessionId] = useState<string | null>(null);
    const [inFlightLocalSessionId, setInFlightLocalSessionId] = useState<string | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const autoPromptSent = useRef<Record<string, boolean>>({});
    const sessionsRef = useRef<LocalChatSession[]>([]);
    const sendPromptRef = useRef<(messageContent: string, localSessionId?: string) => Promise<void>>(async () => {});
    const applyProjectRootRef = useRef<(localSessionId: string, nextRoot: string, announce: boolean) => void>(() => {});
    const toolTimersRef = useRef<Record<string, number>>({});
    const toolNameByUseIdRef = useRef<Record<string, string>>({});

    useEffect(() => {
      sessionsRef.current = sessions;
    }, [sessions]);

    useEffect(() => {
      const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
      queueMicrotask(() => setPrefersReducedMotion(mediaQuery.matches));

      const handleChange = (event: MediaQueryListEvent) => {
        setPrefersReducedMotion(event.matches);
      };

      mediaQuery.addEventListener("change", handleChange);
      return () => {
        mediaQuery.removeEventListener("change", handleChange);
      };
    }, []);

    useEffect(() => {
      if (!isLoading || prefersReducedMotion) {
        return;
      }

      const intervalId = window.setInterval(() => {
        setSpinnerFrameIndex((previous) => (previous + 1) % BRAILLE_SPINNER_FRAMES.length);
      }, 90);

      return () => {
        window.clearInterval(intervalId);
      };
    }, [isLoading, prefersReducedMotion]);

    useEffect(() => {
      return () => {
        Object.values(toolTimersRef.current).forEach((timeoutId) => window.clearTimeout(timeoutId));
      };
    }, []);

    const clearToolTimer = (toolUseId: string): void => {
      const timeoutId = toolTimersRef.current[toolUseId];
      if (timeoutId !== undefined) {
        window.clearTimeout(timeoutId);
        delete toolTimersRef.current[toolUseId];
      }
    };

    const scheduleToolRemoval = (toolUseId: string, delayMs = TOOL_CHIP_SETTLE_MS): void => {
      clearToolTimer(toolUseId);
      toolTimersRef.current[toolUseId] = window.setTimeout(() => {
        setActiveTools((previous) => previous.filter((tool) => tool.toolUseId !== toolUseId));
        delete toolTimersRef.current[toolUseId];
        delete toolNameByUseIdRef.current[toolUseId];
      }, delayMs);
    };

    const resetToolChips = (): void => {
      Object.values(toolTimersRef.current).forEach((timeoutId) => window.clearTimeout(timeoutId));
      toolTimersRef.current = {};
      toolNameByUseIdRef.current = {};
      setActiveTools([]);
    };

    const upsertToolChip = (toolUseId: string, toolName: string, status: ToolChipStatus): void => {
      setActiveTools((previous) => {
        const next = previous.filter((tool) => tool.toolUseId !== toolUseId);
        next.push({ toolUseId, name: toolName, status });
        return next.slice(-TOOL_CHIP_LIMIT);
      });
    };

    const markToolResult = (toolUseId: string, isError: boolean): void => {
      const toolName = toolNameByUseIdRef.current[toolUseId] ?? "execute_command";
      upsertToolChip(toolUseId, toolName, isError ? "error" : "done");
      scheduleToolRemoval(toolUseId, isError ? 3000 : TOOL_CHIP_SETTLE_MS);
    };

    const updateSession = (localSessionId: string, updater: (session: LocalChatSession) => LocalChatSession): void => {
      setSessions((previous) => previous.map((session) => (session.id === localSessionId ? updater(session) : session)));
    };

    const appendAssistantMessage = (localSessionId: string, content: string): void => {
      updateSession(localSessionId, (session) => ({
        ...session,
        messages: [...session.messages, { role: "assistant", content, streaming: false }],
      }));
    };

    const appendUserAndPlaceholder = (localSessionId: string, content: string): void => {
      updateSession(localSessionId, (session) => ({
        ...session,
        messages: [
          ...session.messages,
          { role: "user", content, streaming: false },
          { role: "assistant", content: "", streaming: true },
        ],
      }));
    };

    const appendStreamingDelta = (localSessionId: string, deltaText: string): void => {
      updateSession(localSessionId, (session) => {
        const messages = [...session.messages];
        const last = messages[messages.length - 1];

        // If the last message is assistant and streaming, append to it
        if (last && last.role === "assistant" && last.streaming) {
          messages[messages.length - 1] = {
            ...last,
            content: `${last.content}${deltaText}`,
          };
          return { ...session, messages };
        }

        // Otherwise start a new streaming message
        messages.push({ role: "assistant", content: deltaText, streaming: true });
        return { ...session, messages };
      });
    };

    const finalizeAssistantMessage = (localSessionId: string, finalText: string): void => {
      updateSession(localSessionId, (session) => {
        const messages = [...session.messages];
        const last = messages[messages.length - 1];

        if (last && last.role === "assistant" && last.streaming) {
          messages[messages.length - 1] = {
            role: "assistant",
            content: finalText || last.content,
            streaming: false,
          };
          return { ...session, messages };
        }

        if (finalText) {
          messages.push({ role: "assistant", content: finalText, streaming: false });
        }

        return { ...session, messages };
      });
    };

    const finalizeWithError = (localSessionId: string, errorText: string): void => {
      updateSession(localSessionId, (session) => {
        const messages = [...session.messages];
        const last = messages[messages.length - 1];

        if (last && last.role === "assistant" && last.streaming) {
          messages[messages.length - 1] = {
            role: "assistant",
            content: `Error: ${errorText}`,
            streaming: false,
          };
          return { ...session, messages };
        }

        messages.push({ role: "assistant", content: `Error: ${errorText}`, streaming: false });
        return { ...session, messages };
      });
    };

    const updateHarnessMetadata = (
      localSessionId: string,
      values: Partial<
        Pick<
          HarnessSessionMeta,
          "sessionId" | "claudeSessionId" | "model" | "tools" | "projectRoot" | "lastCompletedAt" | "lastCostUsd"
        >
      >,
    ): void => {
      updateSession(localSessionId, (session) => ({
        ...session,
        harness: {
          ...session.harness,
          ...values,
          mode: harnessMode,
          persona: personaId ?? null,
        },
      }));
    };

    const applyProjectRoot = (localSessionId: string, nextRoot: string, announce: boolean): void => {
      updateSession(localSessionId, (session) => {
        const shouldResetSession = session.harness.projectRoot !== nextRoot;
        const announcement: Message = {
          role: "assistant",
          content: `System: project root set to ${nextRoot}. A new harness session will be created on the next turn.`,
          streaming: false,
        };
        const nextMessages =
          announce && shouldResetSession
            ? [...session.messages, announcement]
            : session.messages;

        return {
          ...session,
          cwd: nextRoot,
          messages: nextMessages,
          harness: {
            ...session.harness,
            sessionId: shouldResetSession ? null : session.harness.sessionId,
            claudeSessionId: shouldResetSession ? null : session.harness.claudeSessionId,
            model: shouldResetSession ? null : session.harness.model,
            tools: shouldResetSession ? [] : session.harness.tools,
            projectRoot: nextRoot,
            mode: harnessMode,
            persona: personaId ?? null,
          },
        };
      });
    };
    applyProjectRootRef.current = applyProjectRoot;

    const readErrorBody = async (response: Response): Promise<string> => {
      try {
        const parsed = (await response.json()) as { error?: unknown };
        if (typeof parsed?.error === "string" && parsed.error.trim()) {
          return parsed.error;
        }
      } catch {
        // Fall back to status text.
      }

      return `${response.status} ${response.statusText || "Request failed"}`.trim();
    };

    const ensureHarnessSession = async (localSessionId: string): Promise<HarnessSessionPayload> => {
      const localSession = sessionsRef.current.find((session) => session.id === localSessionId);
      if (!localSession) {
        throw new Error("Active session not found.");
      }

      const desiredRoot = localSession.harness.projectRoot ?? projectRoot;
      if (!desiredRoot) {
        throw new Error("Project root is required before starting a harness session.");
      }

      const desiredPersona = personaId ?? null;

      const hydrateFromServer = (serverSession: HarnessSessionPayload): HarnessSessionPayload => {
        updateSession(localSessionId, (session) => ({
          ...session,
          cwd: serverSession.projectRoot,
          harness: {
            ...session.harness,
            sessionId: serverSession.id,
            claudeSessionId: serverSession.claudeSessionId,
            projectRoot: serverSession.projectRoot,
            mode: serverSession.mode,
            persona: serverSession.persona,
          },
        }));

        return serverSession;
      };

      const createSession = async (): Promise<HarnessSessionPayload> => {
        const response = await fetch("/api/harness/session/create", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            projectRoot: desiredRoot,
            persona: desiredPersona,
            mode: harnessMode,
          }),
        });

        if (!response.ok) {
          const error = await readErrorBody(response);
          throw new Error(`Failed to create harness session: ${error}`);
        }

        const payload = (await response.json()) as { session?: HarnessSessionPayload };
        if (!payload?.session?.id) {
          throw new Error("Session create response was missing session metadata.");
        }

        return hydrateFromServer(payload.session);
      };

      const existingHarnessId = localSession.harness.sessionId;
      if (!existingHarnessId) {
        return createSession();
      }

      const loadResponse = await fetch(`/api/harness/session/${encodeURIComponent(existingHarnessId)}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      if (loadResponse.ok) {
        const payload = (await loadResponse.json()) as { session?: HarnessSessionPayload };
        const session = payload?.session;

        if (!session?.id) {
          throw new Error("Session load response was missing session metadata.");
        }

        const sameContract =
          session.mode === harnessMode &&
          session.projectRoot === desiredRoot &&
          (session.persona ?? null) === desiredPersona;

        if (sameContract) {
          return hydrateFromServer(session);
        }

        return createSession();
      }

      if (loadResponse.status !== 404) {
        const error = await readErrorBody(loadResponse);
        throw new Error(`Failed to load harness session: ${error}`);
      }

      return createSession();
    };

    const handleHarnessEvent = (event: UIEvent, localSessionId: string): boolean => {
      switch (event.type) {
        case "chat:delta": {
          setStatusText("Composing response");
          appendStreamingDelta(localSessionId, event.text);
          return false;
        }
        case "chat:complete": {
          setStatusText("Finalizing response");
          finalizeAssistantMessage(localSessionId, event.text);
          return false;
        }
        case "tool:start": {
          toolNameByUseIdRef.current[event.toolUseId] = event.name;
          clearToolTimer(event.toolUseId);
          upsertToolChip(event.toolUseId, event.name, "running");
          setStatusText(toolStatusLabel(event.name));
          return false;
        }
        case "tool:result": {
          markToolResult(event.toolUseId, event.isError);
          setStatusText(event.isError ? "Tool returned an error" : "Analyzing tool result");
          return false;
        }
        case "session:init": {
          setStatusText("Session initialized");
          updateHarnessMetadata(localSessionId, {
            sessionId: event.sessionId,
            claudeSessionId: event.claudeSessionId,
            model: event.model,
            tools: event.tools,
          });
          return false;
        }
        case "session:complete": {
          setStatusText("Turn complete");
          updateHarnessMetadata(localSessionId, {
            lastCompletedAt: new Date().toISOString(),
            lastCostUsd: event.costUsd,
          });
          return false;
        }
        case "session:error": {
          setStatusText("Session error");
          appendAssistantMessage(localSessionId, `[session:error] ${event.error}`);
          return false;
        }
        case "process:exit": {
          setIsLoading(false);
          setIsInterrupting(false);
          setStatusText("Ready");
          setInFlightHarnessSessionId(null);
          setInFlightLocalSessionId(null);
          resetToolChips();
          return true;
        }
        default:
          return false;
      }
    };

    const streamTurn = async (harnessSessionId: string, message: string, localSessionId: string): Promise<boolean> => {
      const apiKey = localStorage.getItem("anthropic_api_key") || undefined;
      
      const response = await fetch("/api/harness/turn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId: harnessSessionId,
          message,
          opts: { apiKey },
        }),
      });

      if (!response.ok) {
        const error = await readErrorBody(response);
        throw new Error(error);
      }

      if (!response.body) {
        throw new Error("No stream body returned from harness turn endpoint.");
      }

      let sawProcessExit = false;

      await consumeSseStream(response.body, (eventName, payload) => {
        if (!payload) {
          return;
        }

        let parsed: UIEvent;
        try {
          parsed = JSON.parse(payload) as UIEvent;
        } catch {
          appendAssistantMessage(localSessionId, `[session:error] malformed SSE payload for ${eventName}`);
          return;
        }

        sawProcessExit = handleHarnessEvent(parsed, localSessionId) || sawProcessExit;
      });

      return sawProcessExit;
    };

    const sendPrompt = async (messageContent: string, localSessionId = activeSessionId): Promise<void> => {
      const message = messageContent.trim();
      if (!message || isLoading) {
        return;
      }

      appendUserAndPlaceholder(localSessionId, message);
      resetToolChips();
      setStatusText("Preparing request");
      setIsLoading(true);
      setIsInterrupting(false);

      let sawProcessExit = false;

      try {
        const harnessSession = await ensureHarnessSession(localSessionId);
        setInFlightHarnessSessionId(harnessSession.id);
        setInFlightLocalSessionId(localSessionId);

        updateHarnessMetadata(localSessionId, {
          sessionId: harnessSession.id,
          claudeSessionId: harnessSession.claudeSessionId,
          projectRoot: harnessSession.projectRoot,
        });

        sawProcessExit = await streamTurn(harnessSession.id, message, localSessionId);
      } catch (error) {
        const messageText = error instanceof Error ? error.message : String(error);
        setStatusText("Request failed");
        finalizeWithError(localSessionId, messageText);
      } finally {
        if (!sawProcessExit) {
          setIsLoading(false);
          setIsInterrupting(false);
          setInFlightHarnessSessionId(null);
          setInFlightLocalSessionId(null);
          resetToolChips();
        }
      }
    };
    sendPromptRef.current = sendPrompt;

    const handleInterrupt = async (): Promise<void> => {
      if (!isLoading || !inFlightHarnessSessionId || isInterrupting) {
        return;
      }

      setStatusText("Interrupting turn");
      setIsInterrupting(true);

      try {
        const response = await fetch("/api/harness/interrupt", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ sessionId: inFlightHarnessSessionId }),
        });

        if (!response.ok) {
          const error = await readErrorBody(response);
          appendAssistantMessage(
            inFlightLocalSessionId ?? activeSessionId,
            `[session:error] Interrupt failed: ${error}`,
          );
          setStatusText("Interrupt failed");
          setIsInterrupting(false);
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        appendAssistantMessage(
          inFlightLocalSessionId ?? activeSessionId,
          `[session:error] Interrupt failed: ${message}`,
        );
        setStatusText("Interrupt failed");
        setIsInterrupting(false);
      }
    };

    useImperativeHandle(ref, () => ({
      injectMessage: (message: string) => {
        void sendPrompt(message);
      },
    }));

    useEffect(() => {
      const savedSessions = localStorage.getItem(`sessions_${viewId}`);
      if (savedSessions) {
        try {
          const parsed = JSON.parse(savedSessions) as unknown;
          const normalized = normalizeStoredSessions(
            parsed,
            mode,
            agentName,
            harnessMode,
            personaId,
            projectRoot,
          );

          if (normalized.length > 0) {
            setSessions(normalized);
            setActiveSessionId(normalized[0].id);
            return;
          }
        } catch {
          // Ignore malformed local storage payload and start fresh.
        }
      }

      const initialSession = createLocalSession(mode, agentName, harnessMode, personaId, projectRoot);
      setSessions([initialSession]);
      setActiveSessionId(initialSession.id);
    }, [viewId, mode, agentName, harnessMode, personaId, projectRoot]);

    useEffect(() => {
      if (sessions.length > 0) {
        localStorage.setItem(`sessions_${viewId}`, JSON.stringify(sessions));
      }
    }, [sessions, viewId]);

    useEffect(() => {
      if (!autoPrompt || !activeSessionId || isLoading) {
        return;
      }

      if (autoPromptSent.current[activeSessionId]) {
        return;
      }

      const targetSession = sessions.find((session) => session.id === activeSessionId);
      if (!targetSession || targetSession.messages.length !== 1) {
        return;
      }

      autoPromptSent.current[activeSessionId] = true;
      void sendPromptRef.current(autoPrompt, activeSessionId);
    }, [autoPrompt, activeSessionId, sessions, isLoading]);

    useEffect(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: prefersReducedMotion ? "auto" : "smooth" });
    }, [activeSessionId, sessions, prefersReducedMotion]);

    useEffect(() => {
      if (!projectRoot || !activeSessionId) {
        return;
      }

      const currentSession = sessionsRef.current.find((session) => session.id === activeSessionId);
      if (!currentSession || currentSession.harness.projectRoot === projectRoot) {
        return;
      }

      applyProjectRootRef.current(activeSessionId, projectRoot, false);
    }, [projectRoot, activeSessionId]);

    const createNewSession = (): void => {
      const newSession = createLocalSession(mode, agentName, harnessMode, personaId, projectRoot);
      setSessions((previous) => [newSession, ...previous]);
      setActiveSessionId(newSession.id);
    };

    const activeSession = sessions.find((session) => session.id === activeSessionId) ?? sessions[0];
    const activeHarness = activeSession?.harness;
    const modeLabel = mode === "agent" ? "Agent Persona" : "Direct Link";
    const sessionLabel = shortSessionId(activeHarness?.sessionId ?? null);
    const modelLabel = truncate(activeHarness?.model ?? "pending", 26);
    const rootLabel = formatFolderLabel(activeSession?.cwd ?? projectRoot ?? "~");
    const costLabel = formatCostUsd(activeHarness?.lastCostUsd ?? null);
    const lastRunLabel = formatRunTime(activeHarness?.lastCompletedAt ?? null);
    const statusBadge = isInterrupting ? "Interrupting" : isLoading ? "Turn running" : "Ready";
    const sessionRailWidth = Math.max(140, Math.min(220, Math.floor(width * 0.32)));
    const spinnerGlyph = prefersReducedMotion
      ? "•"
      : BRAILLE_SPINNER_FRAMES[spinnerFrameIndex % BRAILLE_SPINNER_FRAMES.length];

    const sendMessage = async (): Promise<void> => {
      if (!input.trim()) {
        return;
      }

      await sendPrompt(input);
      setInput("");
    };

    return (
      <div className="chat-panel h-full w-full min-h-0 overflow-hidden rounded-[inherit]">
        <div className="relative flex h-full min-h-0 overflow-hidden">
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 opacity-85"
            style={{
              backgroundImage:
                "radial-gradient(circle at 8% 10%, rgba(249,115,22,0.12), transparent 35%), radial-gradient(circle at 80% 0%, rgba(123,175,212,0.16), transparent 40%)",
            }}
          />

          <aside
            className="session-sidebar relative z-10 m-1 mr-0 flex h-[calc(100%-0.5rem)] shrink-0 flex-col rounded-xl border border-[var(--color-border)]/55 bg-[var(--color-surface-high)]/78 shadow-[0_10px_26px_rgba(0,0,0,0.34)]"
            style={{ width: `${sessionRailWidth}px` }}
          >
            <div className="panel-label flex shrink-0 items-center justify-between border-b border-[var(--color-border)]/55 bg-[var(--color-surface-mid)]/75 px-3 py-3">
              <div className="min-w-0">
                <span className="ui-type-mono-meta text-[9px] font-black text-[var(--color-accent-orange)]/85">
                  Session Ring
                </span>
                <span className="mono mt-1 block truncate text-[8px] uppercase tracking-[0.12em] text-[var(--color-text-dim)]/80">
                  Runtime slices
                </span>
              </div>
              <button
                type="button"
                onClick={createNewSession}
                className="ui-control ui-focus-ring flex h-6 w-6 items-center justify-center rounded-md text-[var(--color-accent-orange)] text-sm font-black hover:bg-[var(--color-accent-orange)]/15"
                title="Create new session"
              >
                +
              </button>
            </div>
            <div className="flex-grow overflow-y-auto p-2 custom-scrollbar">
              {sessions.map((session) => (
                <button
                  key={session.id}
                  type="button"
                  className={`ui-focus-ring group relative mb-1.5 w-full rounded-md border px-2.5 py-2.5 text-left transition-all ${
                    activeSessionId === session.id
                      ? "border-[var(--color-accent-orange)]/35 bg-[var(--color-accent-orange)]/12 shadow-[inset_0_0_0_1px_rgba(249,115,22,0.18)]"
                      : "border-transparent bg-white/[0.02] hover:border-[var(--color-border)]/80 hover:bg-white/[0.06]"
                  }`}
                  onClick={() => setActiveSessionId(session.id)}
                >
                  <div className="mono mb-1 text-[8px] tracking-[0.11em] text-[var(--color-text-dim)]/68">
                    {shortSessionId(session.harness.sessionId)}
                  </div>
                  <div
                    className={`truncate text-[10px] font-bold tracking-[0.14em] uppercase ${
                      activeSessionId === session.id ? "text-[var(--color-accent-orange)]" : "text-[var(--color-text-dim)]"
                    }`}
                  >
                    {session.name}
                  </div>
                </button>
              ))}
            </div>
          </aside>

          <div className="relative z-10 flex min-w-0 flex-1 flex-col py-1 pl-2 pr-1">
            <div className="shrink-0 rounded-xl border border-[var(--color-border)]/55 bg-[var(--color-surface-high)]/82 px-4 py-3 backdrop-blur-sm">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 flex flex-col gap-2">
                  <span className="mono text-[9px] font-black tracking-[0.19em] text-[var(--color-accent-orange)] uppercase opacity-85">
                    {modeLabel}
                  </span>
                  <span className="truncate text-xs font-bold tracking-[0.1em] uppercase text-[var(--color-text-main)]">
                    {agentName}
                    <span className="mx-2 text-[var(--color-text-dim)]/45">{"//"}</span>
                    <span className="text-[10px] font-medium lowercase italic text-[var(--color-text-dim)]">
                      {activeSession?.name}
                    </span>
                  </span>
                  <div className="flex flex-wrap items-center gap-1.5">
                    <span className="mono rounded border border-[var(--color-border)]/70 bg-[var(--color-surface-low)]/70 px-2 py-0.5 text-[9px] uppercase tracking-[0.1em] text-[var(--color-text-dim)]">
                      session {sessionLabel}
                    </span>
                    <span className="mono rounded border border-[var(--color-border)]/70 bg-[var(--color-surface-low)]/70 px-2 py-0.5 text-[9px] uppercase tracking-[0.1em] text-[var(--color-text-dim)]">
                      model {modelLabel}
                    </span>
                    <span className="mono rounded border border-[var(--color-border)]/70 bg-[var(--color-surface-low)]/70 px-2 py-0.5 text-[9px] uppercase tracking-[0.1em] text-[var(--color-text-dim)]">
                      cwd {rootLabel}
                    </span>
                    <span className="mono rounded border border-[var(--color-border)]/70 bg-[var(--color-surface-low)]/70 px-2 py-0.5 text-[9px] uppercase tracking-[0.1em] text-[var(--color-text-dim)]">
                      cost {costLabel}
                    </span>
                    <span className="mono rounded border border-[var(--color-border)]/70 bg-[var(--color-surface-low)]/70 px-2 py-0.5 text-[9px] uppercase tracking-[0.1em] text-[var(--color-text-dim)]">
                      last {lastRunLabel}
                    </span>
                  </div>
                </div>

                <div className="flex shrink-0 items-center gap-2">
                  {isLoading && (
                    <button
                      type="button"
                      onClick={() => {
                        void handleInterrupt();
                      }}
                      disabled={isInterrupting || !inFlightHarnessSessionId}
                      className="ui-focus-ring rounded-md border border-red-400/30 bg-red-500/10 px-3 py-1.5 text-[9px] font-mono uppercase tracking-[0.12em] text-red-200 disabled:opacity-40"
                    >
                      {isInterrupting ? "Interrupting..." : "Interrupt Turn"}
                    </button>
                  )}

                  <span
                    className={`mono rounded-md border px-3 py-1.5 text-[9px] uppercase tracking-[0.12em] ${
                      isLoading
                        ? "border-[var(--color-accent-orange)]/28 bg-[var(--color-accent-orange)]/12 text-[var(--color-accent-orange)]"
                        : "border-[var(--color-border)]/75 bg-[var(--color-surface-low)] text-[var(--color-text-dim)]"
                    } ${isLoading && !prefersReducedMotion ? "status-live" : ""}`}
                  >
                    {statusBadge}
                  </span>
                </div>
              </div>
            </div>

            <div className="custom-scrollbar mt-2 min-h-0 flex-grow overflow-y-auto px-1 pb-2 font-mono text-sm">
              <div className="space-y-2">
                {activeSession?.messages.map((message, index) => (
                  <div
                    key={index}
                    className={`rounded-xl border px-4 py-3 shadow-[0_8px_22px_rgba(0,0,0,0.24)] ${
                      message.role === "assistant"
                        ? "border-[var(--color-border)]/55 bg-[var(--color-surface-high)]/68"
                        : "border-[var(--color-border)]/45 bg-[var(--color-surface-low)]/42"
                    }`}
                  >
                    <div className="mb-2 flex items-center gap-2.5 text-[9px] font-black uppercase tracking-[0.16em] opacity-60">
                      <span className={message.role === "assistant" ? "text-[var(--color-accent-orange)]" : "text-[var(--color-text-dim)]"}>
                        {message.role === "assistant" ? "Assistant" : "User"}
                      </span>
                      {message.streaming && (
                        <span className="mono rounded border border-[var(--color-accent-orange)]/30 bg-[var(--color-accent-orange)]/12 px-1.5 py-0.5 text-[8px] tracking-[0.1em] text-[var(--color-accent-orange)]">
                          streaming
                        </span>
                      )}
                    </div>

                    {message.role === "assistant" ? (
                      <div className="ui-panel-soft whitespace-pre-wrap rounded-md border-[var(--color-border)]/60 px-4 py-3 font-mono text-[14px] leading-[1.7] text-[var(--color-text-main)]">
                        <span
                          dangerouslySetInnerHTML={{
                            __html: convert.toHtml(prepareAnsiContent(message.content)),
                          }}
                        />
                        {message.streaming ? (
                          <span
                            aria-hidden
                            className={`ml-1 inline-block text-[var(--color-accent-orange)] ${
                              prefersReducedMotion ? "opacity-80" : "animate-pulse"
                            }`}
                          >
                            ▍
                          </span>
                        ) : null}
                      </div>
                    ) : (
                      <div className="rounded-md border border-[var(--color-border)]/60 bg-[var(--color-surface-low)]/35 px-4 py-3 whitespace-pre-wrap font-mono text-[14px] leading-[1.7] text-[var(--color-text-main)]">
                        {message.content}
                      </div>
                    )}
                  </div>
                ))}
                {isLoading && (
                  <div className={`rounded-xl border border-[var(--color-border)]/55 bg-[var(--color-surface-high)]/72 px-4 py-3 shadow-[0_8px_22px_rgba(0,0,0,0.22)] ${prefersReducedMotion ? "" : "turn-waiting"}`}>
                    <div className="ui-panel-soft inline-flex items-center gap-2 rounded-md px-3 py-1.5">
                      <span
                        aria-hidden
                        className={`mono inline-flex w-4 justify-center text-[13px] text-[var(--color-accent-orange)] ${
                          prefersReducedMotion ? "" : "tracking-tight"
                        }`}
                      >
                        {spinnerGlyph}
                      </span>
                      <span className="mono text-[10px] uppercase tracking-[0.12em] text-[var(--color-accent-orange)]">
                        {statusText}
                      </span>
                    </div>
                    {activeTools.length > 0 && (
                      <div className="mt-2 flex flex-wrap items-center gap-1.5">
                        {activeTools.map((tool) => {
                          const isRunning = tool.status === "running";
                          const isError = tool.status === "error";

                          const chipClass = isRunning
                            ? "border-[var(--color-accent-orange)]/25 bg-[var(--color-accent-orange)]/10 text-[var(--color-accent-orange)]"
                            : isError
                              ? "border-red-400/35 bg-red-500/10 text-red-200"
                              : "border-[var(--color-judging)]/35 bg-[var(--color-judging)]/10 text-[var(--color-judging)]";

                          const iconClass = isRunning
                            ? "text-[var(--color-accent-orange)]"
                            : isError
                              ? "text-red-200"
                              : "text-[var(--color-judging)]";

                          const icon = isRunning ? spinnerGlyph : isError ? "✕" : "✓";

                          return (
                            <span
                              key={tool.toolUseId}
                              className={`mono inline-flex items-center gap-1.5 rounded border px-2 py-1 text-[9px] uppercase tracking-[0.1em] ${chipClass} ${
                                isRunning && !prefersReducedMotion ? "tool-chip-running" : ""
                              }`}
                              title={`${toolStatusLabel(tool.name)} (${tool.status})`}
                            >
                              <span className={`inline-flex w-3 justify-center ${iconClass}`}>{icon}</span>
                              <span className="max-w-[18rem] truncate">{truncate(toolStatusLabel(tool.name), 34)}</span>
                            </span>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}
              </div>
              <div ref={messagesEndRef} />
            </div>

            <div className="chat-input mt-2 shrink-0 rounded-xl border border-[var(--color-border)]/55 bg-[var(--color-surface-high)]/85 p-3 shadow-[0_-8px_24px_rgba(0,0,0,0.22)]">
              <div className="ui-panel-soft flex items-center rounded-md px-3 py-2">
                <input
                  type="text"
                  placeholder={placeholder}
                  className="mono w-full flex-grow bg-transparent text-sm tracking-wide text-[var(--color-text-main)] placeholder:text-white/20 outline-none disabled:opacity-40"
                  value={input}
                  onChange={(event) => setInput(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter") {
                      void sendMessage();
                    }
                  }}
                  autoFocus
                  disabled={isLoading}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  },
);

ChatPanel.displayName = "ChatPanel";
