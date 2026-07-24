import type { EngineSelection, SessionRecord } from "./harness/types.js";
import type { HarnessOpts } from "./harness/types.js";

export interface RuntimeSessionRecord extends SessionRecord {
  schemaVersion: "chirality.session/v2";
  projectId: string;
  projectRoot: string;
  sessionId: string;
  createdAt: string;
  updatedAt: string;
  role: "agent0" | "agent1" | "agent2";
  parentSessionId?: string;
  engineSelection: EngineSelection;
  engineSessionId?: string;
  residencyEpoch?: string;
  status: "idle" | "running" | "completed" | "failed" | "interrupted";
  legacy?: {
    sourcePath: string;
    migratedAt: string;
  };
}

export interface CreateSessionRequest {
  projectId: string;
  role?: RuntimeSessionRecord["role"];
  engineSelection?: EngineSelection;
  persona?: string;
  mode?: string;
  parentSessionId?: string;
  approvalRef?: string;
  allowedWriteTargets?: string[];
}

export interface SessionTurnRequest {
  message?: string;
  prompt?: string;
  opts?: HarnessOpts;
  attachments?: string[];
  turnId?: string;
}
