import { describe, expect, it } from "vitest";
import { hostedModelCatalog, resolveHostedModelSelection, validateHostedBootstrapStatus, validateHostedModelCatalogEntries } from "../packages/contracts/src/delegated.js";

const models = [
  { model: "gpt-default", isDefault: true, defaultReasoningEffort: "high", supportedReasoningEfforts: ["medium", "high", "xhigh"] },
  { model: "gpt-fast", isDefault: false, defaultReasoningEffort: "low", supportedReasoningEfforts: ["low", "medium"] }
];
const selection = { model: "gpt-default", reasoningEffort: "high" };
const base = { schema: "chirality-hosted-bootstrap-status/v1", projectId: "project", ceremony: "signed-in", admission: "ready", canStartLogin: false };

describe("hosted bootstrap status catalog exposure", () => {
  it("accepts the catalog and admitted selection only together and only while admission is ready", () => {
    expect(validateHostedBootstrapStatus({ ...base, models, selection })).toEqual({ ...base, models, selection });
    expect(validateHostedBootstrapStatus(base)).toEqual(base);
    expect(() => validateHostedBootstrapStatus({ ...base, models })).toThrow("Invalid hosted bootstrap status");
    expect(() => validateHostedBootstrapStatus({ ...base, selection })).toThrow("Invalid hosted bootstrap status");
    for (const admission of ["unavailable", "establishing"]) {
      expect(() => validateHostedBootstrapStatus({ ...base, admission, models, selection })).toThrow("Invalid hosted bootstrap status");
      expect(validateHostedBootstrapStatus({ ...base, admission })).toEqual({ ...base, admission });
    }
    expect(() => validateHostedBootstrapStatus({ ...base, ceremony: "pending", admission: "unavailable", models, selection })).toThrow();
  });
  it("rejects catalogs that break the codex-session invariants or a selection outside them", () => {
    const status = (override: Record<string, unknown>) => () => validateHostedBootstrapStatus({ ...base, models, selection, ...override });
    expect(status({ models: [] })).toThrow("Invalid hosted model catalog");
    expect(status({ models: Array.from({ length: 65 }, (_, index) => ({ ...models[1]!, model: `m${index}`, isDefault: index === 0 })) })).toThrow("Invalid hosted model catalog");
    expect(status({ models: [{ ...models[0]!, isDefault: false }, models[1]!] })).toThrow("Invalid hosted model catalog");
    expect(status({ models: [models[0]!, { ...models[1]!, isDefault: true }] })).toThrow("Invalid hosted model catalog");
    expect(status({ models: [{ ...models[0]!, defaultReasoningEffort: "low" }, models[1]!] })).toThrow("Invalid hosted model catalog");
    expect(status({ models: [{ ...models[0]!, supportedReasoningEfforts: ["high", "high"] }, models[1]!] })).toThrow("Invalid hosted model catalog");
    expect(status({ models: [{ ...models[0]!, model: "bad model" }, models[1]!] })).toThrow("Invalid hosted model catalog");
    expect(status({ models: [{ ...models[0]!, supportedReasoningEfforts: ["hi gh"] , defaultReasoningEffort: "hi gh" }, models[1]!] })).toThrow("Invalid hosted model catalog");
    expect(status({ models: [{ ...models[0]!, displayName: "extra" }, models[1]!] })).toThrow();
    expect(status({ models: [models[0]!, { ...models[1]!, model: "gpt-default" }] })).toThrow("Invalid hosted model catalog");
    expect(status({ selection: { model: "gpt-other", reasoningEffort: "high" } })).toThrow("Invalid hosted bootstrap status");
    expect(status({ selection: { model: "gpt-fast", reasoningEffort: "xhigh" } })).toThrow("Invalid hosted bootstrap status");
    expect(status({ selection: { model: "gpt-fast", reasoningEffort: "low", extra: true } })).toThrow();
    expect(validateHostedBootstrapStatus({ ...base, models, selection: { model: "gpt-fast", reasoningEffort: "medium" } }).selection).toEqual({ model: "gpt-fast", reasoningEffort: "medium" });
    expect(validateHostedModelCatalogEntries(models)).toEqual(models);
  });
});

describe("resolveHostedModelSelection", () => {
  const catalog = hostedModelCatalog(models);
  it("returns the admitted default when nothing is requested and never substitutes otherwise", () => {
    expect(catalog.default.model).toBe("gpt-default");
    expect(resolveHostedModelSelection(catalog)).toEqual({ model: "gpt-default", reasoningEffort: "high" });
    expect(resolveHostedModelSelection(catalog, { model: "gpt-fast", reasoningEffort: "medium" })).toEqual({ model: "gpt-fast", reasoningEffort: "medium" });
    expect(resolveHostedModelSelection(catalog, { model: "gpt-default", reasoningEffort: "xhigh" })).toEqual({ model: "gpt-default", reasoningEffort: "xhigh" });
  });
  it("rejects unknown models, unsupported efforts and malformed selections with machine reasons", () => {
    expect(() => resolveHostedModelSelection(catalog, { model: "gpt-unknown", reasoningEffort: "high" })).toThrow(expect.objectContaining({ code: "INVALID_REQUEST", status: 400, message: "Model 'gpt-unknown' is not in the authenticated Codex catalog", details: { reason: "MODEL_NOT_IN_CATALOG", model: "gpt-unknown", available: ["gpt-default", "gpt-fast"] } }));
    expect(() => resolveHostedModelSelection(catalog, { model: "gpt-fast", reasoningEffort: "xhigh" })).toThrow(expect.objectContaining({ code: "INVALID_REQUEST", status: 400, message: "Reasoning effort 'xhigh' is not supported by 'gpt-fast'", details: { reason: "REASONING_EFFORT_UNSUPPORTED", model: "gpt-fast", supported: ["low", "medium"] } }));
    for (const malformed of [{ model: "gpt-fast" }, { reasoningEffort: "low" }, { model: "gpt-fast", reasoningEffort: "low", extra: 1 }, { model: 1, reasoningEffort: "low" }, { model: "gpt-fast", reasoningEffort: "" }, [], "gpt-fast", null]) {
      expect(() => resolveHostedModelSelection(catalog, malformed)).toThrow(expect.objectContaining({ code: "INVALID_REQUEST", status: 400, details: { reason: "MODEL_SELECTION_INVALID" } }));
    }
    expect(() => hostedModelCatalog([{ ...models[0]!, isDefault: false }])).toThrow("Invalid hosted model catalog");
  });
});
