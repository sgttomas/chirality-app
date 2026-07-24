import type {
  EngineDescriptor,
  EngineSelection,
  SessionRecord,
  UIEvent
} from "./harness/index.js";

export interface ToolPermission {
  effect: "allow" | "deny";
  operation: "read" | "write" | "shell" | "network";
  roots?: readonly string[];
}

export interface RuntimeToolDefinition {
  name: string;
  description: string;
  inputSchema: Readonly<Record<string, unknown>>;
  permission: ToolPermission;
  execute(input: unknown, signal: AbortSignal): Promise<unknown>;
}

export interface RuntimeEngineTurnInput {
  projectId: string;
  projectRoot: string;
  sessionId: string;
  turnId: string;
  prompt: string;
  selection: EngineSelection;
  role: "agent0" | "agent1" | "agent2";
  tools: readonly RuntimeToolDefinition[];
  signal: AbortSignal;
  adapterSession?: Readonly<Record<string, unknown>>;
}

export interface RuntimeEngineTurnResult {
  engineSessionId: string;
  adapterSession?: Readonly<Record<string, unknown>>;
}

export interface RuntimeEnginePort {
  readonly descriptor: EngineDescriptor;
  readonly subject: string;
  preflight(input: RuntimeEngineTurnInput): Promise<void>;
  startTurn(input: RuntimeEngineTurnInput): AsyncIterable<UIEvent>;
  interrupt(sessionId: string): Promise<void>;
}

export function asHarnessSession(
  input: RuntimeEngineTurnInput,
  existing: SessionRecord
): SessionRecord {
  return {
    ...existing,
    sessionId: input.sessionId,
    projectRoot: input.projectRoot,
    engineSelection: input.selection,
    agentType: input.role === "agent0" ? 0 : input.role === "agent1" ? 1 : 2
  };
}

export interface ProviderCredentialPort {
  get(providerId: string): Promise<string | undefined>;
  status(providerId: string): Promise<{ configured: boolean }>;
}
