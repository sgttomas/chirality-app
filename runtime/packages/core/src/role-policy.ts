import { createHash } from "node:crypto";

export const RUNTIME_ROLES = ["untyped", "agent0", "agent1", "agent2", "task"] as const;
export type RuntimeRole = typeof RUNTIME_ROLES[number];
export interface RolePolicySettings {
  allowedTools: string[];
  readRoots: string[];
  writeRoots: string[];
  networkPosture: "off" | "ask-per-destination" | "on";
  processPolicy: string;
  delegationPolicy: string;
}
export interface RolePolicyInput {
  role: RuntimeRole;
  policy: RolePolicySettings;
  actual: { adapterId: string; providerId: string; model: string };
  nativeDescendant?: boolean;
}
/** This digest binds declared settings; it is not a proof of containment enforcement. */
export function createRolePolicyEvidence(input: RolePolicyInput) {
  if (!RUNTIME_ROLES.includes(input.role)) throw new Error("Unknown runtime role");
  const normalize = (values: string[]) => {
    if (!Array.isArray(values) || values.some(v => typeof v !== "string" || !v.trim())) throw new Error("Invalid policy list");
    return [...new Set(values)].sort();
  };
  if (!["off", "ask-per-destination", "on"].includes(input.policy.networkPosture)) throw new Error("Invalid network posture");
  for (const value of [input.policy.processPolicy, input.policy.delegationPolicy, input.actual.adapterId, input.actual.providerId, input.actual.model]) {
    if (typeof value !== "string" || !value.trim()) throw new Error("Incomplete policy or actual attribution");
  }
  const posture = {
    schemaVersion: "chirality.role-policy/v1" as const,
    selectedRole: input.role,
    enforcementLabel: "role not mechanically enforced" as const,
    evidencePosture: "instruction-asserted" as const,
    nonDelegationEvidence: "instruction+config asserted" as const,
    settings: { allowedTools: normalize(input.policy.allowedTools), readRoots: normalize(input.policy.readRoots), writeRoots: normalize(input.policy.writeRoots), networkPosture: input.policy.networkPosture, processPolicy: input.policy.processPolicy, delegationPolicy: input.policy.delegationPolicy }
  };
  return {
    ...posture,
    offeredRoles: [...RUNTIME_ROLES],
    policyDigest: createHash("sha256").update(JSON.stringify(posture)).digest("hex"),
    actual: { ...input.actual },
    nativeDescendant: input.nativeDescendant === true,
    containmentEvidence: "declared-settings-only" as const
  };
}
