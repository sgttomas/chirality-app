import { describe, expect, it } from "vitest";
import { createRolePolicyEvidence, RUNTIME_ROLES, type RolePolicyInput } from "../packages/core/src/role-policy.js";
const input: RolePolicyInput = { role: "agent2", policy: { allowedTools: ["read", "write"], readRoots: ["/project"], writeRoots: ["/project/output"], networkPosture: "off", processPolicy: "contained", delegationPolicy: "instruction-asserted-no-delegation" }, actual: { adapterId: "codex", providerId: "openai", model: "actual-a" } };
describe("K-ROLE-2 role parity and policy continuity", () => {
  it.each(RUNTIME_ROLES)("offers %s for every model with truthful labels", role => {
    for (const model of ["actual-a", "actual-b", "unknown-future-model"]) {
      expect(createRolePolicyEvidence({ ...input, role, actual: { ...input.actual, model } })).toMatchObject({ selectedRole: role, offeredRoles: RUNTIME_ROLES, enforcementLabel: "role not mechanically enforced", evidencePosture: "instruction-asserted", containmentEvidence: "declared-settings-only", actual: { model } });
    }
  });
  it("does not infer role from native descent or persist model assignment in digest", () => {
    const first = createRolePolicyEvidence(input);
    const second = createRolePolicyEvidence({ ...input, nativeDescendant: true, actual: { adapterId: "another", providerId: "another", model: "actual-b" } });
    expect(second.policyDigest).toBe(first.policyDigest);
    expect(second.selectedRole).toBe("agent2");
    expect(second.actual).not.toEqual(first.actual);
  });
  it("normalizes set order but binds role and every policy setting", () => {
    const digest = createRolePolicyEvidence(input).policyDigest;
    expect(createRolePolicyEvidence({ ...input, policy: { ...input.policy, allowedTools: ["write", "read", "read"] } }).policyDigest).toBe(digest);
    expect(createRolePolicyEvidence({ ...input, role: "agent0" }).policyDigest).not.toBe(digest);
    for (const policy of [ { allowedTools: ["read"] }, { readRoots: ["/other"] }, { writeRoots: ["/other"] }, { networkPosture: "on" as const }, { processPolicy: "other" }, { delegationPolicy: "other" } ]) expect(createRolePolicyEvidence({ ...input, policy: { ...input.policy, ...policy } }).policyDigest).not.toBe(digest);
  });
  it("rejects absent actual attribution or incomplete settings", () => {
    expect(() => createRolePolicyEvidence({ ...input, actual: { ...input.actual, model: "" } })).toThrow();
    expect(() => createRolePolicyEvidence({ ...input, policy: { ...input.policy, allowedTools: [""] } })).toThrow();
  });
});
