export type RuntimeEventType =
  | "session.init"
  | "turn.accepted"
  | "turn.started"
  | "message.delta"
  | "tool.requested"
  | "tool.completed"
  | "delegation.started"
  | "delegation.completed"
  | "delegation.reviewed"
  | "compaction"
  | "turn.interrupted"
  | "turn.completed"
  | "turn.failed";

export interface RuntimeEvent<T = unknown> {
  schemaVersion: "chirality.event/v1";
  id: string;
  sequence: number;
  timestamp: string;
  projectId: string;
  sessionId: string;
  turnId: string;
  type: RuntimeEventType;
  data: T;
  attribution?: {
    adapterId: string;
    providerId: string;
    model: string;
    packageName?: string;
    packageVersion?: string;
    residencyEpoch?: string;
  };
}

export type RuntimeEventInput<T = unknown> = Omit<
  RuntimeEvent<T>,
  "schemaVersion" | "id" | "sequence" | "timestamp"
>;
