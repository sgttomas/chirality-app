import { RuntimeError, type AgentEnginePort, type EngineSelection } from "@chirality/runtime-contracts";

export class EngineRegistry {
  private readonly engines = new Map<string, AgentEnginePort>();

  register(engine: AgentEnginePort): void {
    const key = this.key(engine.descriptor.adapterId, engine.descriptor.providerId);
    if (this.engines.has(key)) throw new Error(`Engine already registered: ${key}`);
    this.engines.set(key, engine);
  }

  resolve(selection: EngineSelection): AgentEnginePort {
    const engine = this.engines.get(this.key(selection.adapterId, selection.providerId));
    if (engine === undefined) {
      throw new RuntimeError(
        "ENGINE_UNAVAILABLE",
        `Engine ${selection.adapterId}/${selection.providerId} is unavailable`,
        503
      );
    }
    return engine;
  }

  descriptors(): readonly AgentEnginePort["descriptor"][] {
    return [...this.engines.values()].map((engine) => engine.descriptor);
  }

  private key(adapterId: string, providerId: string): string {
    return `${adapterId}\0${providerId}`;
  }
}
