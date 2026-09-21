import { describe, expect, it } from "vitest";
import { RuntimeError } from "@chirality/runtime-contracts";
import { describeFailureDetails, withRetirementFailure } from "../packages/core/src/retirement-failure.js";

describe("withRetirementFailure", () => {
  it("does not attach a memoized cleanup rejection as its own cause", () => {
    const failure = new RuntimeError("ENGINE_UNAVAILABLE", "cleanup failed", 503, { reason: "DESCENDANT_RECONCILIATION_REQUIRED" });
    const once = withRetirementFailure(failure, failure);
    const twice = withRetirementFailure(once, failure);
    expect(twice).toBe(failure);
    expect(failure.cause).toBeUndefined();
    expect(describeFailureDetails(twice)).toEqual({ reason: "DESCENDANT_RECONCILIATION_REQUIRED" });
  });
  it("keeps the primary failure and attaches the retirement diagnostic as its cause", () => {
    const primary = new RuntimeError("ENGINE_UNAVAILABLE", "Codex request timed out", 503, { reason: "CODEX_PROTOCOL_FAILURE" });
    const retirement = new RuntimeError("ENGINE_UNAVAILABLE", "Observed worker descendants require reconciliation", 503, { reason: "DESCENDANT_RECONCILIATION_REQUIRED", detachedCount: 1 });
    const combined = withRetirementFailure(primary, retirement);
    expect(combined).toBe(primary);
    expect((combined as Error).cause).toBe(retirement);
    expect(combined).toMatchObject({ code: "ENGINE_UNAVAILABLE", message: "Codex request timed out", details: { reason: "CODEX_PROTOCOL_FAILURE" } });
  });
  it("aggregates when the primary already carries a cause, preserving its code, message and details", () => {
    const primary = new RuntimeError("INVALID_REQUEST", "primary", 400, { reason: "PRIMARY" });
    const first = new Error("first cleanup"), second = new Error("second cleanup");
    const once = withRetirementFailure(primary, first) as Error;
    const twice = withRetirementFailure(once, second);
    expect(twice).toBeInstanceOf(AggregateError);
    expect(twice).toMatchObject({ name: "RuntimeError", code: "INVALID_REQUEST", message: "primary", details: { reason: "PRIMARY" } });
    expect((twice as AggregateError).errors).toEqual([primary, second]);
  });
  it("passes a lone value through and never drops a retirement failure without a primary", () => {
    const retirement = new Error("cleanup");
    expect(withRetirementFailure(undefined, retirement)).toBe(retirement);
    const primary = new Error("primary");
    expect(withRetirementFailure(primary, undefined)).toBe(primary);
    expect(withRetirementFailure("not an error", retirement)).toBeInstanceOf(AggregateError);
  });
});

describe("describeFailureDetails", () => {
  it("projects bounded scalar details and the cause chain without stacks", () => {
    const retirement = new RuntimeError("ENGINE_UNAVAILABLE", "Observed worker descendants require reconciliation", 503,
      { reason: "DESCENDANT_RECONCILIATION_REQUIRED", detachedCount: 1, detachedPids: [4242], censusFailure: "x".repeat(600), nested: { dropped: true } });
    const primary = withRetirementFailure(new RuntimeError("ENGINE_UNAVAILABLE", "Codex request timed out", 503, { reason: "CODEX_PROTOCOL_FAILURE" }), retirement);
    const details = describeFailureDetails(primary)!;
    expect(details.reason).toBe("CODEX_PROTOCOL_FAILURE");
    expect(details.cause).toMatchObject({ name: "RuntimeError", code: "ENGINE_UNAVAILABLE", message: "Observed worker descendants require reconciliation",
      details: { reason: "DESCENDANT_RECONCILIATION_REQUIRED", detachedCount: 1, detachedPids: [4242] } });
    const cause = details.cause as { details: { censusFailure: string; nested?: unknown } };
    expect(cause.details.censusFailure.length).toBeLessThanOrEqual(513);
    expect(cause.details.nested).toBeUndefined();
    expect(JSON.stringify(details)).not.toContain("    at ");
  });
  it("returns undefined for plain errors with nothing to carry", () => {
    expect(describeFailureDetails(new Error("plain"))).toBeUndefined();
    expect(describeFailureDetails("string")).toBeUndefined();
  });
});
