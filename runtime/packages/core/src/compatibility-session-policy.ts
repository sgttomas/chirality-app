import {
  RuntimeError,
  type EngineSelection,
  type ProviderCredentialPort
} from "@chirality/runtime-contracts";
import type { DefaultSessionPolicy } from "./runtime-service.js";

export interface CompatibilitySessionPolicyOptions {
  credentials: ProviderCredentialPort;
  availableAdapterIds(): readonly string[];
  env?: NodeJS.ProcessEnv;
}

export class CompatibilitySessionPolicy implements DefaultSessionPolicy {
  constructor(private readonly options: CompatibilitySessionPolicyOptions) {}

  async resolve(input: {
    projectId: string;
    persona: string;
    mode: string;
    agentType: 0 | 1;
  }): Promise<{ role: "agent0" | "agent1"; engineSelection: EngineSelection }> {
    const env = this.options.env ?? process.env;
    const explicit = env.CHIRALITY_HARNESS_PROVIDER?.trim().toLowerCase();
    const available = new Set(this.options.availableAdapterIds());
    const configured = (await this.options.credentials.status("anthropic")).configured;
    let adapterId: string;
    let providerId: string;
    if (explicit === "agentsdk" || explicit === "agent-sdk" || explicit === "claude-agent-sdk") {
      adapterId = "claude-agent-sdk";
      providerId = "anthropic";
    } else if (explicit === "anthropic") {
      adapterId = "anthropic-direct";
      providerId = "anthropic";
    } else if (explicit === "stub") {
      adapterId = "stub";
      providerId = "stub";
    } else {
      adapterId = configured ? "claude-agent-sdk" : "stub";
      providerId = configured ? "anthropic" : "stub";
    }
    if (!available.has(adapterId)) {
      throw new RuntimeError(
        "ENGINE_UNAVAILABLE",
        `Default engine adapter is unavailable: ${adapterId}`,
        503
      );
    }
    return {
      role: input.agentType === 0 ? "agent0" : "agent1",
      engineSelection: {
        adapterId,
        providerId,
        model: env.CHIRALITY_GLOBAL_MODEL?.trim() || "haiku"
      }
    };
  }
}
