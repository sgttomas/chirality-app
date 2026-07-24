import { describe, expect, it } from "vitest";
import type { ProviderCredentialPort } from "@chirality/runtime-contracts";
import { OmlxClient } from "@chirality/engine-pi-omlx";

const credentials: ProviderCredentialPort = {
  async get(providerId) {
    return providerId === "omlx" ? "test-key" : undefined;
  },
  async status(providerId) {
    return { configured: providerId === "omlx" };
  }
};

describe("oMLX control client", () => {
  it("parses the real oMLX 0.5 status fields without model-name guessing", async () => {
    const client = new OmlxClient({
      credentials,
      fetchImpl: async () =>
        new Response(
          JSON.stringify({
            models: [
              {
                id: "Qwen3.6-35B-A3B-8bit",
                loaded: true,
                is_loading: false,
                model_type: "llm",
                engine_type: "batched",
                estimated_size: 35_000
              },
              {
                id: "bge-m3",
                loaded: true,
                is_loading: false,
                model_type: "embedding",
                engine_type: "embedding"
              },
              {
                id: "draft-model",
                loaded: false,
                is_loading: false,
                model_type: "llm",
                engine_type: "batched",
                is_helper: true
              }
            ]
          }),
          { status: 200, headers: { "content-type": "application/json" } }
        )
    });

    await expect(client.listStatus()).resolves.toEqual([
      {
        id: "Qwen3.6-35B-A3B-8bit",
        kind: "llm",
        loaded: true,
        loading: false,
        sizeBytes: 35_000
      },
      {
        id: "bge-m3",
        kind: "embedding",
        loaded: true,
        loading: false
      },
      {
        id: "draft-model",
        kind: "helper",
        loaded: false,
        loading: false
      }
    ]);
  });
});
