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
