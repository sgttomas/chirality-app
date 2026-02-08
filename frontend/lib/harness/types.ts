import type { SettingSource } from "@anthropic-ai/claude-agent-sdk";

export type SessionMode = "workbench" | "pipeline" | "direct";

export interface Session {
  id: string;
  createdAt: string;
  updatedAt: string;
  projectRoot: string;
  persona: string | null;
  mode: SessionMode;
  claudeSessionId: string | null;
  model: string | null;
  bootFingerprint: string | null;
  bootedAt: string | null;
}

export interface SessionSummary {
  id: string;
  createdAt: string;
  updatedAt: string;
  persona: string | null;
  mode: SessionMode;
  projectRoot: string;
  model: string | null;
  bootedAt: string | null;
}

export type SessionBootReason =
  | "already_booted"
  | "forced"
  | "missing_claude_session"
  | "missing_boot_metadata"
  | "fingerprint_changed";

export interface SessionBootResult {
  session: Session;
  booted: boolean;
  reason: SessionBootReason;
  fingerprint: string;
  previousFingerprint: string | null;
  previousClaudeSessionId: string | null;
}

export interface UsageInfo {
  input_tokens: number;
  output_tokens: number;
  cache_read_input_tokens?: number;
  cache_creation_input_tokens?: number;
}

export interface TurnOpts {
  permissionMode?: "default" | "acceptEdits" | "dontAsk" | "plan";
  model?: string;
  apiKey?: string;
  tools?: string;
  disallowedTools?: string[];
  autoApproveTools?: string[];
  toolsOverride?: string;
  disallowedToolsOverride?: string[];
  autoApproveToolsOverride?: string[];
  maxTurns?: number;
  systemPromptAppend?: string;
  systemPromptFile?: string;
  settingSources?: SettingSource[];
  // Test-only override used by validation tooling to inject a mocked SDK runtime path.
  pathToClaudeCodeExecutable?: string;
  verbose?: boolean;
  includePartialMessages?: boolean;
}

export type UIEvent =
  | { type: "chat:delta"; sessionId: string; text: string }
  | { type: "chat:complete"; sessionId: string; text: string }
  | {
      type: "tool:start";
      sessionId: string;
      toolUseId: string;
      name: string;
      input: Record<string, unknown>;
    }
  | {
      type: "tool:result";
      sessionId: string;
      toolUseId: string;
      content: string;
      isError: boolean;
    }
  | {
      type: "session:init";
      sessionId: string;
      claudeSessionId: string | null;
      model: string;
      tools: string[];
    }
  | { type: "session:complete"; sessionId: string; costUsd: number; usage: UsageInfo }
  | { type: "session:error"; sessionId: string; error: string }
  | { type: "process:exit"; sessionId: string; code: number | null; signal: string | null };

export interface PersonaConfig {
  id: string;
  sourceFile: string;
  body?: string;
  tools?: string;
  disallowedTools?: string[];
  autoApproveTools?: string[];
  maxTurns?: number;
}

export interface LogEntry {
  timestamp: string;
  sessionId: string;
  level: "debug" | "info" | "warn" | "error";
  event: string;
  data?: Record<string, unknown>;
}

export interface ToolUseInfo {
  toolUseId: string;
  name: string;
  input: Record<string, unknown>;
}

export interface ToolResultInfo {
  toolUseId: string;
  content: string;
  isError: boolean;
}
