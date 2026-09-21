import {
  RuntimeError,
  type ChiralityRoleName,
  type QualifiedMethodReference
} from "@chirality/runtime-contracts";

export type TransitionSessionStatus = "idle" | "running" | "completed" | "failed" | "interrupted";

export interface MethodTransitionInput {
  sessionId: string;
  sessionStatus: TransitionSessionStatus;
  currentRoleId: ChiralityRoleName;
  nextRoleId?: ChiralityRoleName;
  currentMethods: readonly QualifiedMethodReference[];
  nextMethods: readonly QualifiedMethodReference[];
  methodCompatibility: "compatible" | "incompatible";
  boundaryConfirmed: boolean;
  activeProviderSpan?: {
    providerId: string;
    spanId: string;
  };
  recordContinuationBoundary?: boolean;
}

export interface MethodTransitionDecision {
  allowed: true;
  sessionId: string;
  roleId: ChiralityRoleName;
  selectedMethods: readonly QualifiedMethodReference[];
  incompatible: boolean;
  continuationBoundary?: {
    kind: "method-transition";
    fromRoleId: ChiralityRoleName;
    toRoleId: ChiralityRoleName;
    fromMethods: readonly QualifiedMethodReference[];
    toMethods: readonly QualifiedMethodReference[];
    providerId?: string;
    providerSpanId?: string;
  };
}

const NON_RUNNING = new Set<TransitionSessionStatus>([
  "idle",
  "completed",
  "failed",
  "interrupted"
]);

/** Enforces replacement boundaries without coupling method selection to role identity. */
export function evaluateMethodTransition(input: MethodTransitionInput): MethodTransitionDecision {
  const forbiddenSkills = input.nextMethods.filter(method => method.kind === "skill" && method.source !== "bundled");
  if (forbiddenSkills.length) {
    throw new RuntimeError(
      "FORBIDDEN",
      "Skills may be selected only from a trusted bundled source",
      403,
      {
        sessionId: input.sessionId,
        methods: forbiddenSkills.map(method => `${method.sourceRootId}:${method.source}:${method.kind}:${method.name}`)
      }
    );
  }
  const nextRoleId = input.nextRoleId ?? input.currentRoleId;
  const roleChanged = nextRoleId !== input.currentRoleId;
  const methodsChanged = !sameOrderedValues(input.currentMethods, input.nextMethods);
  const incompatible = roleChanged || (methodsChanged && input.methodCompatibility === "incompatible");

  if (incompatible && (!NON_RUNNING.has(input.sessionStatus) || !input.boundaryConfirmed)) {
    throw new RuntimeError(
      "RUNTIME_COMPATIBILITY_MISMATCH",
      "Incompatible role or method replacement requires a confirmed non-running boundary",
      409,
      {
        sessionId: input.sessionId,
        sessionStatus: input.sessionStatus,
        boundaryConfirmed: input.boundaryConfirmed
      }
    );
  }

  const shouldRecordBoundary =
    incompatible && (input.recordContinuationBoundary === true || input.activeProviderSpan !== undefined);
  return {
    allowed: true,
    sessionId: input.sessionId,
    roleId: nextRoleId,
    selectedMethods: [...input.nextMethods],
    incompatible,
    ...(shouldRecordBoundary
      ? {
          continuationBoundary: {
            kind: "method-transition" as const,
            fromRoleId: input.currentRoleId,
            toRoleId: nextRoleId,
            fromMethods: [...input.currentMethods],
            toMethods: [...input.nextMethods],
            ...(input.activeProviderSpan === undefined
              ? {}
              : {
                  providerId: input.activeProviderSpan.providerId,
                  providerSpanId: input.activeProviderSpan.spanId
                })
          }
        }
      : {})
  };
}

function sameOrderedValues(
  left: readonly QualifiedMethodReference[],
  right: readonly QualifiedMethodReference[]
): boolean {
  return left.length === right.length && left.every((value, index) => {
    const candidate = right[index];
    return candidate !== undefined && value.sourceRootId === candidate.sourceRootId &&
      value.source === candidate.source && value.kind === candidate.kind && value.name === candidate.name;
  });
}
