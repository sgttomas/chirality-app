export interface ChiralityProjectManifestV1 {
  schemaVersion: "chirality.project/v1";
  projectId: string;
  displayName: string;
  workingRoot: string;
  instructionRoot: string;
  agentsOverlay?: string;
  defaultExecutionRoot: string;
  profiles: {
    domain: readonly string[];
    capability: readonly string[];
    dataBoundary: readonly string[];
  };
  enabledAdapterIds: readonly string[];
  embeddedUi: {
    declared: boolean;
    path?: string;
  };
  legacySessionRoots?: readonly string[];
}

export interface ChiralityProjectManifestV2
  extends Omit<ChiralityProjectManifestV1, "schemaVersion" | "instructionRoot"> {
  schemaVersion: "chirality.project/v2";
  instructionRoot: {
    mode: "runtime";
  };
}

export type ChiralityProjectManifest =
  | ChiralityProjectManifestV1
  | ChiralityProjectManifestV2;

export const CHIRALITY_INSTRUCTION_ROOT_ENV = "CHIRALITY_INSTRUCTION_ROOT";

export interface RegisteredProject {
  projectId: string;
  displayName: string;
  canonicalRoot: string;
  manifestPath: string;
  manifestHash: string;
  registeredAt: string;
  approval: {
    approvedBy: string;
    approvalReference: string;
  };
  clientId: string;
  enabledAdapterIds: readonly string[];
  legacySessionRoots: readonly string[];
}

export interface ProjectStatus {
  project: RegisteredProject;
  manifestDrift: boolean;
  adaptersEnabled: boolean;
}
