// src/types/agentEvents.ts

export type OrchestrationMode = 'two_pass' | 'three_pass';

export type AgentPhase =
  | 'reasoning'    // CLI call to chirality-framework
  | 'generation'   // Matrices -> DS/SP/X/M deterministic scaffolds (+optional polish)
  | 'refinement'   // V1 -> V2 -> V3 alignment checks and diffs
  | 'finalize';    // Persist finals, mirror, RAG index, manifest

export type PhaseStatus = 'start' | 'success' | 'error';

export type DocKind = 'DS' | 'SP' | 'X' | 'M';

export interface AgentRunEvent {
  runId: string;
  seq: number;                 // monotonic sequence for ordering
  phase: AgentPhase;
  status: PhaseStatus;
  mode: OrchestrationMode;
  round?: 1 | 2 | 3;            // for three-pass refinement
  doc?: DocKind;                // for per-document events
  ms?: number;                  // elapsed for this step
  error?: string;               // if status === 'error'
  timestamp: string;            // ISO 8601
  details?: Record<string, unknown>;
}

// Optional: higher-level manifest for the run
export interface AgentRunManifest {
  runId: string;
  mode: OrchestrationMode;
  startedAt: string;
  finishedAt?: string;
  phases: Array<{
    phase: AgentPhase;
    round?: 1 | 2 | 3;
    startedAt: string;
    finishedAt?: string;
    steps?: Array<{
      doc?: DocKind;
      startedAt: string;
      finishedAt?: string;
      ms?: number;
      error?: string;
    }>;
  }>;
  files?: {
    indexJson?: string;       // path to runs/<run_id>/index.json
    runManifest?: string;     // path to runs/<run_id>/run_manifest.json
  };
}
