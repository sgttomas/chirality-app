import type { NativePlanClarificationAnswers, NativePlanClarificationQuestion } from "./delegated.js";

export const CHIRALITY_ROLE_NAMES = [
  "HELP_HUMAN",
  "HELPS_HUMANS",
  "WORKING_ITEMS",
  "TASK"
] as const;

export type ChiralityRoleName = (typeof CHIRALITY_ROLE_NAMES)[number];

export interface RoleDescriptor {
  id: ChiralityRoleName;
  agentType: 0 | 1 | 2;
  directEntry: boolean;
  defaultForNewChat: boolean;
  description: string;
  instruction: string;
  delegatesTo?: readonly ChiralityRoleName[];
  tools?: readonly string[];
}

export const CHIRALITY_ROLES: readonly RoleDescriptor[] = Object.freeze([
  Object.freeze({ id: "HELP_HUMAN", agentType: 0, directEntry: true, defaultForNewChat: true, description: "Meet the human, maintain alignment and continuity, and coordinate managers.", instruction: "agents/AGENT_HELP_HUMAN.md" }),
  Object.freeze({ id: "HELPS_HUMANS", agentType: 1, directEntry: true, defaultForNewChat: false, description: "Help conceive and design workflows, tools, and projects.", instruction: "agents/AGENT_HELPS_HUMANS.md" }),
  Object.freeze({ id: "WORKING_ITEMS", agentType: 1, directEntry: true, defaultForNewChat: false, description: "Organize implementation, delegate bounded work, and integrate results.", instruction: "agents/AGENT_WORKING_ITEMS.md" }),
  Object.freeze({ id: "TASK", agentType: 2, directEntry: false, defaultForNewChat: false, description: "Execute a bounded assignment, with a workflow when applicable.", instruction: "agents/AGENT_TASK.md" })
]);

export interface RolesResponse {
  schemaVersion: "chirality.roles/v3";
  defaultRole: "HELP_HUMAN";
  roles: readonly RoleDescriptor[];
}

export type MethodSource = "project" | "user" | "bundled";
export type MethodKind = "skill" | "workflow";

/** Stable public identity. A client never supplies or receives a source path. */
export interface QualifiedMethodReference {
  sourceRootId: string;
  source: MethodSource;
  kind: MethodKind;
  name: string;
}

export interface UnqualifiedMethodReference {
  kind: MethodKind;
  name: string;
}

export type MethodReference = QualifiedMethodReference | UnqualifiedMethodReference;

export interface MethodCompatibilityMapping {
  field: "Workflow" | "TaskSkill";
  original: string;
  normalizedAlias?: string;
  resolved: QualifiedMethodReference;
  mapping: "converted-alias" | "explicit-qualified-historical-workflow" | "unmapped-canonical-workflow";
}

export interface WorkflowToolRestrictions {
  capabilities?: readonly string[];
  /** An explicit empty list denies commands. Absence inherits the outer policy. */
  commands?: readonly string[];
}

export interface WorkflowExecutionMetadata {
  schemaVersion: 1;
  compatibleRoles: readonly ChiralityRoleName[];
  tools?: WorkflowToolRestrictions;
}

export type MethodNavigationCategory = "core" | "specialist" | "superseded";

/** Authoritative App navigation placement from the bundled catalog. Index-only; project and user packages never carry one. */
export type MethodNavigation = {
  category: MethodNavigationCategory;
  /** primary: shown at first glance; supporting: a bounded step of a primary workflow, shown under a disclosure. */
  tier: "primary" | "supporting";
  /** Position within its category (core) or group (specialist); 0-based. */
  order: number;
  /** Product display name when it differs from the identifier (Core only today). */
  displayName?: string;
  /** Specialist group; label as authored; order is the group's 0-based position among specialist groups. */
  group?: { key: string; label: string; order: number };
  /** Superseded only: the current replacement workflow name. */
  supersededBy?: string;
};

export interface MethodDescriptor extends QualifiedMethodReference {
  qualifiedId: string;
  description: string;
  central: boolean;
  compatibility: "canonical" | "legacy";
  executionRoleIds: readonly ChiralityRoleName[];
  resources: readonly string[];
  /** Standard package metadata preserved from entrypoint frontmatter when present. */
  metadata?: Readonly<Record<string, unknown>>;
  execution?: WorkflowExecutionMetadata;
  navigation?: MethodNavigation;
}

export type MethodCatalogIssueCode =
  | "duplicate-source-root"
  | "invalid-source-root"
  | "unreadable-source-root"
  | "entrypoint-escape"
  | "malformed-frontmatter"
  | "metadata-name-mismatch"
  | "malformed-execution-metadata"
  | "duplicate-method"
  | "resource-escape";

export interface MethodCatalogIssue {
  code: MethodCatalogIssueCode;
  sourceRootId: string;
  source: MethodSource;
  kind?: MethodKind;
  packageName?: string;
  message: string;
}

export interface MethodsResponse {
  schemaVersion: "chirality.methods/v3";
  methods: readonly MethodDescriptor[];
  malformedPackages: readonly MethodCatalogIssue[];
}

export interface MethodResourceDescriptor {
  path: string;
  sha256: string;
}

export interface MethodInspectionResponse {
  schemaVersion: "chirality.method-inspection/v3";
  method: MethodDescriptor;
  entrypoint: { content: string; sha256: string };
  resources: readonly MethodResourceDescriptor[];
}

export interface SelectedMethodResourceRequest {
  method: QualifiedMethodReference;
  paths: readonly string[];
}

export interface ResolveSelectedContextRequest {
  roleId: ChiralityRoleName;
  interactionMode: "chat" | "native-plan";
  permissionMode: "readOnly" | "ask" | "workspaceWrite" | "bypass";
  /** Ordered and allowed to contain more than one method. */
  methods: readonly MethodReference[];
  resources?: readonly SelectedMethodResourceRequest[];
  /** Explicit canonical selector retained for simple workflow callers. */
  workflow?: string;
  /** Legacy compatibility input. It never changes a role or grants capabilities. */
  taskSkill?: string;
}

export interface ResolvedContextDocument {
  method: QualifiedMethodReference;
  path: string;
  content: string;
  sha256: string;
}

export interface SelectedMethodDisposition {
  method: QualifiedMethodReference;
  selected: true;
  activeRoleCompatible: boolean;
  eligibleRoleIds: readonly ChiralityRoleName[];
  route: "primary" | "managed-delegation" | "unavailable";
}

export interface SuppliedContextEntry {
  kind: "root" | "project" | "role" | "catalog-description" | "selection-metadata" | "method-body" | "resource";
  id: string;
  content: string;
  sha256: string;
  method?: QualifiedMethodReference;
  /** Relative to the selected method package; never an absolute source path. */
  resourcePath?: string;
}

export interface ResolvedContextBasisPreview {
  id: string;
  sha256: string;
  /** Modes excluded; binds effective instruction bytes, methods, roles, sources, and policy. */
  instructionPolicySha256: string;
  sources: readonly { sourceRootId: string; source: MethodSource; version: string; rootSha256: string }[];
  persisted: false;
}

export interface ResolveSelectedContextResponse {
  schemaVersion: "chirality.selected-context/v3";
  roleId: ChiralityRoleName;
  methods: readonly MethodDescriptor[];
  documents: readonly ResolvedContextDocument[];
  dispositions: readonly SelectedMethodDisposition[];
  supplied: readonly SuppliedContextEntry[];
  executionRoots: Readonly<{
    workingRoot: { path: string; origin: "registered-project-root"; identitySha256: string };
    /** Base for reviewed repository-relative commands such as tools/.... */
    toolRoot: { path: string; origin: "trusted-runtime-instruction-root"; identitySha256: string };
  }>;
  basisPreview: ResolvedContextBasisPreview;
  compatibilityInputs: readonly ("Workflow" | "TaskSkill")[];
  compatibilityMappings: readonly MethodCompatibilityMapping[];
}

export interface ReplaceSelectedMethodsRequest {
  expectedBasisId?: string;
  expectedRevision?: number;
  roleId?: ChiralityRoleName;
  boundaryConfirmed?: boolean;
  selectionMode?: "replace" | "merge";
  /** Omission preserves the current ordered selection for a role-only transition. */
  methods?: readonly MethodReference[];
}

export interface ReplaceSelectedMethodsResponse {
  schemaVersion: "chirality.selected-methods/v3";
  sessionId: string;
  revision: number;
  methods: readonly QualifiedMethodReference[];
  basisPreview: ResolvedContextBasisPreview;
  transition: {
    /**
     * `prepared`: a reversible provider successor was prepared (engines that
     * re-project context). `additive`: the engine keeps its thread and the
     * changed instructions travel as an additive context update on the next
     * turn (the Codex app-server path).
     */
    status: "unchanged" | "prepared" | "additive";
    successorAvailable: boolean;
    preparationId?: string;
  };
}

export interface NativePlanAdapterQualification {
  adapterId: string;
  providerId: string;
  qualificationId: string;
  admissionSha256: string;
  evidenceClass: "native-adapter-qualified";
}

export interface NativePlanAdapterTrialAdmission {
  adapterId: string;
  providerId: string;
  dispositionId: string;
  admissionSha256: string;
  evidenceClass: "native-adapter-local-human-trial";
}

export type NativePlanAdapterAdmission = NativePlanAdapterQualification | NativePlanAdapterTrialAdmission;

export type NativePlanCapabilityResponse =
  | {
      schemaVersion: "chirality.native-plan-capability/v3";
      status: "unavailable";
      reason: string;
    }
  | {
      schemaVersion: "chirality.native-plan-capability/v3";
      status: "qualified";
      qualification: NativePlanAdapterQualification;
    }
  | {
      schemaVersion: "chirality.native-plan-capability/v3";
      status: "trial";
      admission: NativePlanAdapterTrialAdmission;
    };

export interface UnavailableNativePlanAdapterEvent {
  qualificationState: "unavailable";
  eventId: string;
  reason: string;
}

export interface QualifiedNativePlanAdapterEvent {
  qualificationState: "qualified";
  eventId: string;
  occurredAt: string;
  qualification: NativePlanAdapterQualification;
  /** Real supervisor/provider identity retained by production captures; legacy revisions may omit it. */
  binding?: {
    projectId: string;
    sessionId: string;
    clientTurnId: string;
    providerThreadId: string;
    providerTurnId: string;
  };
  plan: unknown;
}

export interface TrialNativePlanAdapterEvent {
  qualificationState: "trial";
  eventId: string;
  occurredAt: string;
  admission: NativePlanAdapterTrialAdmission;
  binding?: {
    projectId: string;
    sessionId: string;
    clientTurnId: string;
    providerThreadId: string;
    providerTurnId: string;
  };
  plan: unknown;
}

export type NativePlanAdapterEvent =
  | UnavailableNativePlanAdapterEvent
  | QualifiedNativePlanAdapterEvent
  | TrialNativePlanAdapterEvent;

export type AdmittedNativePlanAdapterEvent = QualifiedNativePlanAdapterEvent | TrialNativePlanAdapterEvent;

export interface NativePlanRevision {
  revision: number;
  sourceEvent: AdmittedNativePlanAdapterEvent;
}

export type NativePlanRevisionsResponse =
  | {
      schemaVersion: "chirality.native-plan-revisions/v3";
      status: "unavailable";
      reason: string;
      revisions: readonly [];
    }
  | {
      schemaVersion: "chirality.native-plan-revisions/v3";
      status: "qualified";
      qualification: NativePlanAdapterQualification;
      revisions: readonly NativePlanRevision[];
    }
  | {
      schemaVersion: "chirality.native-plan-revisions/v3";
      status: "trial";
      admission: NativePlanAdapterTrialAdmission;
      revisions: readonly NativePlanRevision[];
    };

export interface ExportNativePlanRequest {
  revision: number;
  targetRelativePath: string;
  overwrite?: boolean;
}

export interface ExportNativePlanResponse {
  schemaVersion: "chirality.native-plan-export/v3";
  sessionId: string;
  revision: number;
  targetRelativePath: string;
  sha256: string;
}

export interface NativePlanClarification {
  clientTurnId: string;
  providerThreadId: string;
  providerTurnId: string;
  requestId: string | number;
  itemId: string;
  questions: readonly NativePlanClarificationQuestion[];
  isBlocking: boolean;
  autoResolutionMs: number | null;
}

export type NativePlanClarificationsResponse =
  | {
      schemaVersion: "chirality.native-plan-clarifications/v3";
      status: "unavailable";
      reason: string;
      clarifications: readonly [];
    }
  | {
      schemaVersion: "chirality.native-plan-clarifications/v3";
      status: "qualified";
      qualification: NativePlanAdapterQualification;
      clarifications: readonly NativePlanClarification[];
    }
  | {
      schemaVersion: "chirality.native-plan-clarifications/v3";
      status: "trial";
      admission: NativePlanAdapterTrialAdmission;
      clarifications: readonly NativePlanClarification[];
    };

export interface ReplyNativePlanClarificationRequest {
  requestId: string | number;
  answers: NativePlanClarificationAnswers;
}

export interface ReplyNativePlanClarificationResponse {
  schemaVersion: "chirality.native-plan-clarification-reply/v3";
  sessionId: string;
  requestId: string | number;
  sent: true;
}

export interface FrozenInstructionBasisV3 {
  schemaVersion: "chirality.instruction-basis/v1";
  basisId: string;
  sessionId: string;
  createdAt: string;
  roleId: ChiralityRoleName;
  interactionMode: "chat" | "native-plan";
  permissionMode: "readOnly" | "ask" | "workspaceWrite" | "bypass";
  selectedMethods: readonly QualifiedMethodReference[];
  instructionPolicySha256?: string;
  compatibilityInputs: readonly ("Workflow" | "TaskSkill")[];
  compatibilityMappings: readonly MethodCompatibilityMapping[];
  suppliedEntries: readonly (SuppliedContextEntry & { origin: string; path: string })[];
  methodDispositions: readonly SelectedMethodDisposition[];
  continuationBoundary?: Readonly<Record<string, unknown>>;
}

export interface InstructionHistoryRecordV3 {
  schemaVersion: "chirality.instruction-history/v1";
  historyId: string;
  sessionId: string;
  sequence: number;
  timestamp: string;
  type: "selection.changed" | "resource.loaded" | "instruction-basis.resolved" | "method-change.requested" | "method-change.applied" | "method-change.failed" | "native-plan.revised" | "native-child.method-loaded" | "provider-span.prepared" | "provider-span.committed" | "provider-span.continued" | "provider-span.cancelled" | "provider-span.failed";
  [key: string]: unknown;
}

const SHA256 = /^[a-f0-9]{64}$/;

/** Runtime guard for a revision boundary; fixtures and unavailable events fail closed. */
export function assertQualifiedNativePlanEvent(
  event: NativePlanAdapterEvent
): asserts event is QualifiedNativePlanAdapterEvent {
  if (
    event === null || typeof event !== "object" ||
    event.qualificationState !== "qualified" ||
    typeof event.eventId !== "string" || event.eventId.trim() === "" ||
    typeof event.occurredAt !== "string" || !Number.isFinite(Date.parse(event.occurredAt)) ||
    event.qualification === null || typeof event.qualification !== "object" ||
    event.qualification.evidenceClass !== "native-adapter-qualified" ||
    !SHA256.test(event.qualification.admissionSha256) ||
    event.qualification.adapterId.trim() === "" ||
    event.qualification.providerId.trim() === "" ||
    event.qualification.qualificationId.trim() === ""
    || (event.binding !== undefined && (
      typeof event.binding.projectId !== "string" || event.binding.projectId.trim() === "" ||
      typeof event.binding.sessionId !== "string" || event.binding.sessionId.trim() === "" ||
      typeof event.binding.clientTurnId !== "string" || event.binding.clientTurnId.trim() === "" ||
      typeof event.binding.providerThreadId !== "string" || event.binding.providerThreadId.trim() === "" ||
      typeof event.binding.providerTurnId !== "string" || event.binding.providerTurnId.trim() === ""
    ))
  ) {
    throw new Error("Native Plan revisions require a qualified native adapter event");
  }
}

/** Runtime guard for either currently admitted operational disposition. */
export function assertAdmittedNativePlanEvent(
  event: NativePlanAdapterEvent
): asserts event is AdmittedNativePlanAdapterEvent {
  if (event.qualificationState === "qualified") { assertQualifiedNativePlanEvent(event); return; }
  if (
    event.qualificationState !== "trial" ||
    typeof event.eventId !== "string" || event.eventId.trim() === "" ||
    typeof event.occurredAt !== "string" || !Number.isFinite(Date.parse(event.occurredAt)) ||
    event.admission === null || typeof event.admission !== "object" ||
    Object.keys(event.admission).sort().join(",") !== "adapterId,admissionSha256,dispositionId,evidenceClass,providerId" ||
    event.admission.evidenceClass !== "native-adapter-local-human-trial" ||
    typeof event.admission.adapterId !== "string" || event.admission.adapterId.trim() === "" ||
    typeof event.admission.providerId !== "string" || event.admission.providerId.trim() === "" ||
    typeof event.admission.dispositionId !== "string" || event.admission.dispositionId.trim() === "" ||
    !SHA256.test(event.admission.admissionSha256) ||
    (event.binding !== undefined && (
      typeof event.binding.projectId !== "string" || event.binding.projectId.trim() === "" ||
      typeof event.binding.sessionId !== "string" || event.binding.sessionId.trim() === "" ||
      typeof event.binding.clientTurnId !== "string" || event.binding.clientTurnId.trim() === "" ||
      typeof event.binding.providerThreadId !== "string" || event.binding.providerThreadId.trim() === "" ||
      typeof event.binding.providerTurnId !== "string" || event.binding.providerTurnId.trim() === ""
    ))
  ) throw new Error("Native Plan event is not backed by an admitted adapter disposition");
}

export function nativePlanRevisionFromAdapterEvent(
  revision: number,
  event: NativePlanAdapterEvent
): NativePlanRevision {
  assertAdmittedNativePlanEvent(event);
  if (!Number.isSafeInteger(revision) || revision < 1) {
    throw new Error("Native Plan revision must be a positive safe integer");
  }
  return { revision, sourceEvent: event };
}
