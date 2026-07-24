import { ContentBlock, ResolvedOpts, SessionRecord, UIEvent } from './types.js';

export type EngineAdapterSubject = string;

export type EngineCapabilities = {
  credentials: boolean;
  tools: boolean;
  attachments: boolean;
  interruption: boolean;
  durableResume: boolean;
  compaction: boolean;
};

export type EngineDescriptor = {
  adapterId: EngineAdapterSubject;
  providerId: string;
  packageName?: string;
  packageVersion?: string;
  capabilities: EngineCapabilities;
};

export type AgentEngineRunInput = {
  session: SessionRecord;
  message: string;
  opts: ResolvedOpts;
  contentBlocks?: ContentBlock[];
  turnId: string;
};

export interface AgentEnginePort {
  readonly descriptor: EngineDescriptor;
  /** @deprecated Use descriptor.adapterId. */
  readonly subject: EngineAdapterSubject;
  preflight(input: AgentEngineRunInput): Promise<void>;
  startTurn(input: AgentEngineRunInput): AsyncIterable<UIEvent>;
  interrupt(sessionId: string): Promise<void>;
}

export type RuntimeEngineContract = {
  port: AgentEnginePort;
  publicUiEvents: readonly UIEvent['type'][];
  providerMetadataAllowed: true;
};

export const PUBLIC_UI_EVENT_NAMES = [
  'session:init',
  'chat:delta',
  'chat:complete',
  'tool:result',
  'session:complete',
  'turn:error',
  'process:exit',
  'harness:event'
] as const satisfies readonly UIEvent['type'][];
