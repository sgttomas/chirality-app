import {
  HarnessError,
  type AgentEnginePort,
  type AgentEngineRunInput,
  type EngineDescriptor,
  type ProviderCredentialPort,
  type UIEvent
} from "@chirality/runtime-contracts";

export const PI_CODING_AGENT_PACKAGE_NAME = "@earendil-works/pi-coding-agent";
export const PI_CODING_AGENT_PACKAGE_VERSION = "0.80.10";

export interface PiTurnRuntimePort {
  preflight(input: AgentEngineRunInput, credential: string): Promise<void>;
  startTurn(
    input: AgentEngineRunInput,
    options: {
      credential: string;
      disableBuiltIns: true;
      disableAmbientResources: true;
      transcriptRoot: string;
    }
  ): AsyncIterable<UIEvent>;
  interrupt(sessionId: string): Promise<void>;
}

export interface PiOmlxEngineOptions {
  credentials: ProviderCredentialPort;
  runtime: PiTurnRuntimePort;
  transcriptRootFor(sessionId: string): string;
  isExactlyResident(modelId: string): Promise<boolean>;
}

export function createPiOmlxEngineAdapter(options: PiOmlxEngineOptions): AgentEnginePort {
  const descriptor: EngineDescriptor = {
    adapterId: "pi",
    providerId: "omlx",
    packageName: PI_CODING_AGENT_PACKAGE_NAME,
    packageVersion: PI_CODING_AGENT_PACKAGE_VERSION,
    capabilities: {
      credentials: true,
      tools: true,
      attachments: false,
      interruption: true,
      durableResume: false,
      compaction: true
    }
  };
  const credential = async (): Promise<string> => {
    const value = await options.credentials.get("omlx");
    if (value === undefined || value.trim() === "") {
      throw new HarnessError("PROVIDER_AUTH_FAILURE", 401, "oMLX credential is not configured");
    }
    return value;
  };
  const enforcePilot = async (input: AgentEngineRunInput): Promise<void> => {
    if (input.session.agentType !== 2) {
      throw new HarnessError("INVALID_REQUEST", 403, "Pi/oMLX is limited to Agent 2");
    }
    if (
      input.opts.tools.length !== 1 ||
      !["read_file", "read"].includes(input.opts.tools[0] ?? "")
    ) {
      throw new HarnessError(
        "INVALID_REQUEST",
        403,
        "Pi/oMLX pilot requires exactly one read-only Chirality tool"
      );
    }
    if (!(await options.isExactlyResident(input.opts.model))) {
      throw new HarnessError("MODEL_UNAVAILABLE", 409, "Exact oMLX model is not resident");
    }
  };
  return {
    descriptor,
    subject: "pi",
    async preflight(input) {
      await enforcePilot(input);
      await options.runtime.preflight(input, await credential());
    },
    async *startTurn(input) {
      await enforcePilot(input);
      yield* options.runtime.startTurn(input, {
        credential: await credential(),
        disableBuiltIns: true,
        disableAmbientResources: true,
        transcriptRoot: options.transcriptRootFor(input.session.sessionId)
      });
    },
    interrupt(sessionId) {
      return options.runtime.interrupt(sessionId);
    }
  };
}
