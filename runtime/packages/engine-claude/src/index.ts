import {
  HarnessError,
  type AgentEnginePort,
  type AgentEngineRunInput,
  type EngineDescriptor,
  type ProviderCredentialPort,
  type UIEvent
} from "@chirality/runtime-contracts";

export interface ClaudeTurnRuntimePort {
  preflight(input: AgentEngineRunInput, apiKey: string): Promise<void>;
  startTurn(input: AgentEngineRunInput, apiKey: string): AsyncIterable<UIEvent>;
  interrupt(sessionId: string): Promise<void>;
}

export interface ClaudeEngineAdapterOptions {
  adapterId: "anthropic-direct" | "claude-agent-sdk";
  packageName: "@anthropic-ai/sdk" | "@anthropic-ai/claude-agent-sdk";
  packageVersion: string;
  credentials: ProviderCredentialPort;
  runtime: ClaudeTurnRuntimePort;
}

export function createClaudeEngineAdapter(options: ClaudeEngineAdapterOptions): AgentEnginePort {
  const descriptor: EngineDescriptor = {
    adapterId: options.adapterId,
    providerId: "anthropic",
    packageName: options.packageName,
    packageVersion: options.packageVersion,
    capabilities: {
      credentials: true,
      tools: true,
      attachments: options.adapterId === "anthropic-direct",
      interruption: true,
      durableResume: options.adapterId === "claude-agent-sdk",
      compaction: options.adapterId === "claude-agent-sdk"
    }
  };
  const requireKey = async (): Promise<string> => {
    const key = await options.credentials.get("anthropic");
    if (key === undefined || key.trim() === "") {
      throw new HarnessError("MISSING_API_KEY", 401, "Anthropic credential is not configured");
    }
    return key;
  };
  return {
    descriptor,
    subject: descriptor.adapterId,
    async preflight(input) {
      await options.runtime.preflight(input, await requireKey());
    },
    async *startTurn(input) {
      yield* options.runtime.startTurn(input, await requireKey());
    },
    interrupt(sessionId) {
      return options.runtime.interrupt(sessionId);
    }
  };
}
