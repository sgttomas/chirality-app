"use client";

import React, { useState, useRef, useEffect, useImperativeHandle, forwardRef } from "react";
import Convert from "ansi-to-html";

import { DirectoryPicker } from "./DirectoryPicker";
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
  newline: true,
  escapeXML: true,
  stream: false,
});

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

function summarizeValue(value: unknown, maxChars = 220): string {
  try {
    if (typeof value === "string") {
      return truncate(value, maxChars);
    }

    if (value === null || typeof value === "undefined") {
      return "";
    }

    return truncate(JSON.stringify(value), maxChars);
  } catch {
    return "[unserializable input]";
  }
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
    const [statusText, setStatusText] = useState<string>("Processing_Request");
    const [inFlightHarnessSessionId, setInFlightHarnessSessionId] = useState<string | null>(null);
    const [inFlightLocalSessionId, setInFlightLocalSessionId] = useState<string | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const autoPromptSent = useRef<Record<string, boolean>>({});
    const sessionsRef = useRef<LocalChatSession[]>([]);
    const sendPromptRef = useRef<(messageContent: string, localSessionId?: string) => Promise<void>>(async () => {});
    const applyProjectRootRef = useRef<(localSessionId: string, nextRoot: string, announce: boolean) => void>(() => {});

    useEffect(() => {
      sessionsRef.current = sessions;
    }, [sessions]);

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
          setStatusText("Typing_Response");
          appendStreamingDelta(localSessionId, event.text);
          return false;
        }
        case "chat:complete": {
          setStatusText("Processing_Request");
          finalizeAssistantMessage(localSessionId, event.text);
          return false;
        }
        case "tool:start": {
          // Map tool names to user-friendly status text
          const toolLabels: Record<string, string> = {
            "read_file": "Reading_File",
            "write_file": "Writing_File",
            "execute_command": "Executing_Command",
            "list_directory": "Scanning_Directory",
            "search_file_content": "Searching_Files",
            "glob": "Finding_Files"
          };
          setStatusText(toolLabels[event.name] || `Running_${event.name}`);
          return false;
        }
        case "tool:result": {
          setStatusText("Analyzing_Result");
          return false;
        }
        case "session:init": {
          updateHarnessMetadata(localSessionId, {
            sessionId: event.sessionId,
            claudeSessionId: event.claudeSessionId,
            model: event.model,
            tools: event.tools,
          });
          return false;
        }
        case "session:complete": {
          updateHarnessMetadata(localSessionId, {
            lastCompletedAt: new Date().toISOString(),
            lastCostUsd: event.costUsd,
          });
          appendAssistantMessage(
            localSessionId,
            `[session:complete] cost=$${event.costUsd.toFixed(6)} input=${event.usage.input_tokens} output=${event.usage.output_tokens}`,
          );
          return false;
        }
        case "session:error": {
          appendAssistantMessage(localSessionId, `[session:error] ${event.error}`);
          return false;
        }
        case "process:exit": {
          setIsLoading(false);
          setIsInterrupting(false);
          setInFlightHarnessSessionId(null);
          setInFlightLocalSessionId(null);
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
        finalizeWithError(localSessionId, messageText);
      } finally {
        if (!sawProcessExit) {
          setIsLoading(false);
          setIsInterrupting(false);
          setInFlightHarnessSessionId(null);
          setInFlightLocalSessionId(null);
        }
      }
    };
    sendPromptRef.current = sendPrompt;

    const handleInterrupt = async (): Promise<void> => {
      if (!isLoading || !inFlightHarnessSessionId || isInterrupting) {
        return;
      }

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
          setIsInterrupting(false);
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        appendAssistantMessage(
          inFlightLocalSessionId ?? activeSessionId,
          `[session:error] Interrupt failed: ${message}`,
        );
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
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [activeSessionId, sessions]);

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

    const sendMessage = async (): Promise<void> => {
      if (!input.trim()) {
        return;
      }

      await sendPrompt(input);
      setInput("");
    };

    return (
      <div className="chat-panel glass h-full w-full flex flex-row overflow-hidden min-h-0">
        <div
          className="session-sidebar flex flex-col h-full shrink-0 border-r border-[var(--color-border)] bg-[var(--color-surface-high)] shadow-xl"
          style={{ width: "220px" }}
        >
          <div className="panel-label flex justify-between items-center p-4 border-b border-[var(--color-border)] shrink-0 bg-[var(--color-surface-mid)]">
            <span className="text-[10px] tracking-[0.2em] font-black text-[var(--color-accent-orange)] uppercase">
              History
            </span>
            <button
              onClick={createNewSession}
              className="w-6 h-6 flex items-center justify-center rounded-md bg-white/5 border border-white/10 text-[var(--color-accent-orange)] font-black text-lg hover:bg-[var(--color-accent-orange)] hover:text-black transition-all"
            >
              +
            </button>
          </div>
          <div className="flex-grow overflow-y-auto custom-scrollbar">
            {sessions.map((session) => (
              <div
                key={session.id}
                className={`group relative p-4 border-b border-white/[0.05] cursor-pointer transition-all ${
                  activeSessionId === session.id
                    ? "bg-[var(--color-accent-orange)]/10 border-r-2 border-r-[var(--color-accent-orange)]"
                    : "hover:bg-white/5"
                }`}
                onClick={() => setActiveSessionId(session.id)}
              >
                <div className="font-mono text-[8px] opacity-30 mb-1.5 tracking-[0.1em]">{session.id}</div>
                <div
                  className={`truncate text-[10px] font-bold tracking-wider uppercase ${
                    activeSessionId === session.id ? "text-[var(--color-accent-orange)]" : "text-[var(--color-text-dim)]"
                  }`}
                >
                  {session.name}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex-grow flex flex-col min-w-0 h-full relative bg-[var(--color-surface-low)]">
          <div className="p-4 border-b border-[var(--color-border)] flex justify-between items-center shrink-0 bg-[var(--color-surface-high)] backdrop-blur-sm gap-3">
            <div className="flex flex-col gap-0.5 min-w-0">
              <span className="text-[9px] font-black tracking-[0.3em] text-[var(--color-accent-orange)] uppercase opacity-80">
                {mode === "agent" ? "Agent_Persona" : "Direct_Link"}
              </span>
              <span className="font-bold tracking-[0.1em] text-xs truncate uppercase text-[var(--color-text-main)]">
                {agentName}
                <span className="opacity-30 mx-2">{"//"}</span>
                <span className="text-[var(--color-text-dim)] text-[10px] lowercase italic font-normal">
                  {activeSession?.name}
                </span>
              </span>
              <span className="font-mono text-[9px] text-white/50 truncate">
                {activeSession?.harness.sessionId
                  ? `harness:${activeSession.harness.sessionId} ${activeSession.harness.model ? `(${activeSession.harness.model})` : ""}`
                  : "harness: not initialized"}
              </span>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              {isLoading && (
                <button
                  onClick={() => {
                    void handleInterrupt();
                  }}
                  disabled={isInterrupting || !inFlightHarnessSessionId}
                  className="text-[9px] font-mono text-red-300 uppercase tracking-widest bg-red-500/10 px-3 py-1.5 rounded border border-red-400/30 disabled:opacity-40"
                >
                  {isInterrupting ? "Interrupting..." : "Interrupt"}
                </button>
              )}

              <span className="text-[9px] font-mono uppercase tracking-widest bg-[var(--color-accent-orange)]/10 px-3 py-1.5 rounded border border-[var(--color-accent-orange)]/20 text-[var(--color-accent-orange)]">
                {isLoading ? "Turn Running" : "Ready"}
              </span>
            </div>
          </div>

          <div className="flex-grow overflow-y-auto font-mono text-sm min-h-0 custom-scrollbar">
            {activeSession?.messages.map((message, index) => (
              <div
                key={index}
                className={`p-6 border-b border-[var(--color-border)] ${message.role === "assistant" ? "bg-[var(--color-surface-low)]" : ""}`}
              >
                <div className="flex items-center gap-3 mb-3 opacity-40 text-[9px] uppercase tracking-[0.2em] font-black">
                  <span className={message.role === "assistant" ? "text-[var(--color-accent-orange)]" : "text-[var(--color-text-dim)]"}>
                    {message.role === "assistant" ? "CLAUDE" : "USER"}
                  </span>
                  <span className="w-1 h-1 bg-[var(--color-text-dim)] rounded-full" />
                  <span className="text-[var(--color-text-dim)]">{new Date().toLocaleTimeString()}</span>
                </div>

                {message.role === "assistant" ? (
                  <div
                    className="whitespace-pre-wrap leading-[1.7] text-[14px] text-[var(--color-text-main)] font-mono"
                    dangerouslySetInnerHTML={{ __html: convert.toHtml(message.content) }}
                  />
                ) : (
                  <div className="whitespace-pre-wrap leading-[1.7] text-[14px] text-[var(--color-text-main)] font-mono">{message.content}</div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="p-6 font-mono text-[10px] uppercase tracking-[0.3em] flex items-center gap-4 transition-all duration-500">
                <div className="flex gap-1.5 items-center">
                    <span className="w-1.5 h-1.5 bg-[var(--color-accent-orange)] rounded-full animate-[ping_1.5s_infinite]" />
                    <span className="w-1.5 h-1.5 bg-[var(--color-accent-orange)] rounded-full animate-[bounce_1s_infinite_100ms]" />
                    <span className="w-1.5 h-1.5 bg-[var(--color-accent-orange)] rounded-full animate-[ping_1.5s_infinite_200ms]" />
                </div>
                <span className="text-[var(--color-accent-orange)] opacity-80 animate-pulse">
                    {statusText}...
                </span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input shrink-0 bg-[var(--color-surface-high)] border-t border-[var(--color-border)] p-5 shadow-[0_-10px_30px_rgba(0,0,0,0.5)]">
            <div className="flex items-center">
              <input
                type="text"
                placeholder={placeholder}
                className="outline-none w-full bg-transparent font-mono text-[var(--color-text-main)] placeholder:text-white/10 text-sm tracking-wide flex-grow disabled:opacity-40"
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
    );
  },
);

ChatPanel.displayName = "ChatPanel";
