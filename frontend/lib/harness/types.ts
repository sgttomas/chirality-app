import type { SettingSource, Options as AgentSdkOptions } from "@anthropic-ai/claude-agent-sdk";

// ---------------------------------------------------------------------------
// SubagentDefinition — compile-safe extraction from SDK's Options.agents type.
//
// If the SDK exports `agents` on Options we derive the per-agent value type
// automatically, keeping our contract in lockstep. If the field doesn't exist
// (older SDK, or type not yet shipped), the conditional resolves to `never`
// and the ternary falls through to a manual definition that mirrors the
// documented SDK shape.
// ---------------------------------------------------------------------------
type ExtractAgentDef<T> = T extends Record<string, infer V> ? V : never;
type MaybeSdkAgents = AgentSdkOptions extends { agents?: infer A } ? A : never;
type SdkAgentDef = ExtractAgentDef<NonNullable<MaybeSdkAgents>>;

export type SubagentDefinition = [SdkAgentDef] extends [never]
  ? {
      description: string;
      prompt: string;
      tools?: string[];
      model?: "sonnet" | "opus" | "haiku" | "inherit";
    }
  : SdkAgentDef;

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

export interface SubagentGovernance {
  contextSealed: boolean;
  pipelineRunApproved: boolean;
  approvalRef: string;
  approvedBy?: string;
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
  /** Human-authored delegation proof for Type 1 -> Type 2 subagent spawning. */
  subagentGovernance?: SubagentGovernance;
  /** SDK-native subagent definitions keyed by agent ID. Populated by persona injection logic. */
  agents?: Record<string, SubagentDefinition>;
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
      /** If present, this tool call originated inside a Task/subagent run. */
      parentToolUseId?: string | null;
    }
  | {
      type: "tool:result";
      sessionId: string;
      toolUseId: string;
      content: string;
      isError: boolean;
      /** If present, this tool result originated inside a Task/subagent run. */
      parentToolUseId?: string | null;
    }
  | {
      type: "tool:progress";
      sessionId: string;
      toolUseId: string;
      name: string;
      elapsedSeconds: number;
      /** If present, this tool progress originated inside a Task/subagent run. */
      parentToolUseId?: string | null;
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
  /** Human-readable agent description (parsed from frontmatter `description` field). */
  description?: string;
  /** Allowlisted Type 2 agent IDs this persona may spawn as subagents (parsed from frontmatter `subagents` CSV). */
  subagents?: string[];
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
  parentToolUseId: string | null;
}

export interface ToolResultInfo {
  toolUseId: string;
  content: string;
  isError: boolean;
  parentToolUseId: string | null;
}

export type AttachmentType = "image" | "document" | "text";

export interface Attachment {
  path: string;
  name: string;
  mimeType: string;
  type: AttachmentType;
}

export const ATTACHMENT_EXTENSIONS: readonly string[] = [
  ".png", ".jpg", ".jpeg", ".gif", ".webp",
  ".pdf",
  ".txt", ".md", ".csv",
];
