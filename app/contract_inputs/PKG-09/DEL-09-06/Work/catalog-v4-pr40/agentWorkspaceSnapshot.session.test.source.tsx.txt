// The embedded agent's workspace snapshot publishes the model hash only for the model
// revision it was computed for. It once compared two different revision counters, so in
// the real app Start always refused with "Open a model and wait for its fingerprint"
// (first exposed by the RT-E1 webview journey; DEL-16-06 `Work/agent-live-session.md`).
// Start refuses with AGENT-WORKSPACE-NOT-READY exactly when the snapshot publishes no
// hash. Past that check, Start goes on to the native host, which jsdom lacks; that later
// failure is not the refusal under test.
import { act, renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as previewService from "../../services/previewService";
import * as hashService from "../../services/hashService";
import { bulkChangeModel } from "../../test-support/bulkChangeModel";
import { buildBulkChangeBatch } from "../bulk-change/bulkChange";
import { useWorkspaceSession } from "./workspaceSession";

afterEach(() => { vi.restoreAllMocks(); });

async function session() {
  vi.spyOn(previewService, "loadPreviewModel").mockResolvedValue(bulkChangeModel());
  const hook = renderHook(() => useWorkspaceSession());
  await waitFor(() => expect(hook.result.current.model.modelHash).not.toBeNull());
  return hook.result;
}
type Session = Awaited<ReturnType<typeof session>>;
async function startRefusal(result: Session) {
  let message = "";
  await act(async () => { try { await result.current.agent.start("r".repeat(48)); } catch (error) { message = (error as Error).message; } });
  await act(async () => { await result.current.agent.close().catch(() => {}); });
  return message;
}
async function applyBendRadius(result: Session, value: string) {
  const batch = await buildBulkChangeBatch(result.current.model.model!, [{ type: "component", id: "component:BEND-B" }], { kind: "bend-radius", value, unit: "m" }, hashService.canonicalJsonString, "agent-snapshot-edit");
  await act(async () => { await result.current.operations.handleQueueOperationBatch(batch); });
  const entry = result.current.operations.queuedBatches[0];
  await act(async () => { await result.current.operations.handleRunOperationBatch(entry, false); });
  await act(async () => { await result.current.operations.handleRunOperationBatch(result.current.operations.queuedBatches[0], true); });
}

describe("the embedded agent's workspace snapshot", () => {
  it("lets Start past the workspace check once the loaded model's hash is computed", async () => {
    const result = await session();
    expect(await startRefusal(result)).not.toBe("AGENT-WORKSPACE-NOT-READY");
  });

  it("does so again after an applied edit, once that model's hash is computed", async () => {
    const result = await session();
    await applyBendRadius(result, "0.2");
    await waitFor(() => expect(result.current.model.modelHash).not.toBeNull());
    expect(result.current.model.model!.components[0].geometry).toMatchObject({ bend_radius: { value: 0.2, unit: "m" } });
    expect(await startRefusal(result)).not.toBe("AGENT-WORKSPACE-NOT-READY");
  });

  it("never pairs the edited model's hash with the model an undo restores, before React re-renders", async () => {
    const result = await session();
    await applyBendRadius(result, "0.2");
    await waitFor(() => expect(result.current.model.modelHash).not.toBeNull());
    expect(await startRefusal(result)).not.toBe("AGENT-WORKSPACE-NOT-READY");
    // Undo and Start in one synchronous step: the snapshot is read from the closure of the
    // last render, whose hash belongs to the edited model, while the undo has already
    // restored the earlier model. Only the owner's live revision can refuse it.
    let started: Promise<unknown> | null = null;
    act(() => {
      result.current.operations.handleUndoSessionModelEdit();
      started = result.current.agent.start("r".repeat(48));
    });
    const refusal = await started!.then(() => "", (error: Error) => error.message);
    expect(refusal).toBe("AGENT-WORKSPACE-NOT-READY");
    await act(async () => { await result.current.agent.close().catch(() => {}); });
    await waitFor(() => expect(result.current.model.model!.components[0].geometry).toMatchObject({ bend_radius: { value: 0.15, unit: "m" } }));
    await waitFor(() => expect(result.current.model.modelHash).not.toBeNull());
    expect(await startRefusal(result)).not.toBe("AGENT-WORKSPACE-NOT-READY");
  });

  it("never publishes the hash from before an edit while the edited model's hash is pending", async () => {
    const result = await session();
    expect(await startRefusal(result)).not.toBe("AGENT-WORKSPACE-NOT-READY");
    // The next model's hash never arrives; every other hash still does.
    const computed = hashService.computeModelHash;
    vi.spyOn(hashService, "computeModelHash").mockImplementation((model) =>
      JSON.stringify(model).includes('"value":0.25') ? new Promise(() => {}) : computed(model));
    await applyBendRadius(result, "0.25");
    expect(result.current.model.model!.components[0].geometry).toMatchObject({ bend_radius: { value: 0.25, unit: "m" } });
    expect(await startRefusal(result)).toBe("AGENT-WORKSPACE-NOT-READY");
  });
});
