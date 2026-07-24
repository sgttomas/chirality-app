export type OmlxModelKind = "llm" | "embedding" | "reranker" | "helper" | "unknown";

export interface OmlxModelStatus {
  id: string;
  kind: OmlxModelKind;
  loaded: boolean;
  loading: boolean;
  managed?: boolean;
  sizeBytes?: number;
}

export interface ResidencyEpoch {
  epochId: string;
  modelId: string;
  activatedAt: string;
}

export interface ResidencyStatus {
  phase: "NO_MODEL" | "READY" | "DRAINING" | "UNLOADING" | "LOADING";
  managedModelId?: string;
  epoch?: ResidencyEpoch;
  activeTurns: number;
  acceptingLocalTurns: boolean;
  models: readonly OmlxModelStatus[];
}

export interface OmlxControlPort {
  listStatus(signal?: AbortSignal): Promise<readonly OmlxModelStatus[]>;
  load(modelId: string, signal?: AbortSignal): Promise<void>;
  unload(modelId: string, signal?: AbortSignal): Promise<void>;
}

export interface ResidencyEvidence {
  schemaVersion: "chirality.model-residency/v1";
  timestamp: string;
  transitionId: string;
  fromModelId?: string;
  targetModelId: string;
  outcome: "started" | "completed" | "aborted" | "failed";
  reason?: string;
  epochId?: string;
  approvalReference: string;
}
