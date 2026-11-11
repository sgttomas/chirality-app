// RT-E1 milestone 2: the webview link of the component journey. The fixture's
// agent proposals are stamped by the embedded-agent session and applied phase by
// phase through the desktop batch service on the wasm engine; each correction's
// `before` text comes from the session's record producer (the texts
// swbpipe_read_records returns), so the applier itself confirms they are exact.
// The operation applier test (core/model_operations/operation_applier/tests/
// agent_m2_component_journey.rs) adds the person's own k and SIF entries and the
// solve. All data are invented.
import { describe, expect, it } from "vitest";
import fixture from "../../../../fixtures/model_operations/agent_m2_component_journey.json";
import type { PreviewModel } from "../types";
import { componentsAwaitingUserModifiers, engineDisplayNumber, recordBefore, stampAgentOperations, type RecordFamily } from "./embeddedAgentSession";
import { applyOperationBatch } from "./operationBatchService";
import { canonicalJsonString, computeModelHash } from "./hashService";
import { buildDeleteNodeIntent, buildDeletePipeIntent, buildDeleteSupportIntent } from "../features/model-tree/removalIntents";

const { proposalHandle, requestRef } = fixture.host;
const FAMILY: Record<string, RecordFamily> = { component: "components", support: "supports" };

async function resolveBefore(model: PreviewModel, placeholder: string): Promise<string> {
  const [, kind, name, key] = placeholder.split(":");
  const family = FAMILY[kind], id = `${kind}:${name}`;
  const record = (model as unknown as Record<string, Record<string, unknown>[]>)[family].find(entry => entry.id === id)!;
  const before = await recordBefore(family, record, await canonicalJsonString(record));
  expect(before[key], placeholder).toEqual(expect.any(String));
  return before[key];
}

describe("embedded agent milestone 2 component journey (webview link)", () => {
  it("applies every phase as one agent batch, corrections with record-producer before texts", async () => {
    let model = structuredClone(fixture.blank.model) as unknown as PreviewModel;
    for (const proposal of fixture.proposals) {
      const operations = await Promise.all((proposal.operations as Record<string, unknown>[]).map(async operation => {
        const change = operation.change as Record<string, string>;
        return change.before.startsWith("BEFORE:") ? { ...operation, change: { ...change, before: await resolveBefore(model, change.before) } } : operation;
      }));
      expect(operations.length).toBeLessThanOrEqual(16);
      const hash = await computeModelHash(model);
      const batch = { batch_id: `agent-${proposal.phase}`, operations: stampAgentOperations(operations, proposalHandle, requestRef), source_model_hash: hash!.value };
      const outcome = await applyOperationBatch(model, batch, hash);
      expect(outcome.validation.batch_validation_status, `${proposal.phase}: ${JSON.stringify(outcome.diagnostics)}`).toBe("passed");
      model = outcome.applied_model!;
      if (proposal.phase === "components") expect(componentsAwaitingUserModifiers(model)).toEqual(["component:bend-n3", "component:tee-n2"]);
    }
    expect(model.components.map(component => component.kind)).toEqual(["bend", "tee", "reducer", "valve", "expansion_joint"]);
    expect(model.supports.find(support => support.id === "support:n4-guide")?.restraints).toEqual(["UX"]);
  });

  it("returns deletion before texts the applier accepts for padded labels and exponent coordinates", async () => {
    let model = structuredClone(fixture.blank.model) as unknown as PreviewModel;
    for (const proposal of fixture.proposals.slice(0, 1)) {
      const hash = await computeModelHash(model);
      const outcome = await applyOperationBatch(model, { batch_id: "agent-geometry", operations: stampAgentOperations(proposal.operations as Record<string, unknown>[], proposalHandle, requestRef), source_model_hash: hash!.value }, hash);
      model = outcome.applied_model!;
    }
    const records = model as unknown as Record<string, Record<string, unknown>[]>;
    const [node, pipe] = [records.nodes[0], records.pipe_segments[0]];
    records.nodes.push({ ...node, id: "node:free-a", label: "  Free é A ", position: { x: 1e-7, y: 2.5e21, z: 0.1 + 0.2 } }, { ...node, id: "node:free-b", label: "\tFree B\n", position: { x: -1.5e-8, y: -0, z: 123456789.125 } });
    records.pipe_segments.push({ ...pipe, id: "pipe:free", label: " Free run ", from: "node:free-a", to: "node:free-b" });
    records.supports = [{ id: "support:free", label: "  Free stop  ", node: "node:free-a", restraints: ["UX"], family: "line_stop", provenance: "invented" }];
    const deletions: [RecordFamily, string, string, string][] = [["supports", "support:free", "Support", "delete_support"], ["pipe_segments", "pipe:free", "Element", "delete_pipe_run"], ["nodes", "node:free-a", "Node", "delete_node"], ["nodes", "node:free-b", "Node", "delete_node"]];
    for (const [family, id, objectType, changeKind] of deletions) {
      const record = records[family].find(entry => entry.id === id)!;
      const before = (await recordBefore(family, record, await canonicalJsonString(record))).delete;
      // The inspector's own Delete sends the same text (removalIntents.ts, since #29).
      const inspector = family === "supports" ? buildDeleteSupportIntent(record as unknown as PreviewModel["supports"][number], model)
        : family === "pipe_segments" ? buildDeletePipeIntent(record as unknown as PreviewModel["pipe_segments"][number], model)
        : buildDeleteNodeIntent(record as unknown as PreviewModel["nodes"][number], model);
      expect(inspector.change.before).toBe(before);
      const operation = { operation_id: `op:delete:${id}`, operation_kind: "delete", target: { object_type: objectType, ref: id }, change: { change_id: `change:delete:${id}`, change_kind: changeKind, field_label: "Deletion", field_path: family, before, after: "not_present", unit: "none", dimension: "dimensionless", source_note: "invented" }, rationale: "invented" };
      const hash = await computeModelHash(model);
      if (id === "node:free-a") {
        // An untrimmed label with ECMAScript numbers (what the inspector sent before #29) is refused as stale.
        const stale = { ...operation, change: { ...operation.change, before: "  Free é A ; x=1e-7; y=2.5e+21; z=0.30000000000000004" } };
        const refused = await applyOperationBatch(model, { batch_id: "agent-stale", operations: stampAgentOperations([stale], proposalHandle, requestRef), source_model_hash: hash!.value }, hash);
        expect(refused.validation.batch_validation_status).not.toBe("passed");
      }
      const outcome = await applyOperationBatch(model, { batch_id: `agent-${id}`, operations: stampAgentOperations([operation], proposalHandle, requestRef), source_model_hash: hash!.value }, hash);
      expect(outcome.validation.batch_validation_status, `${id} ${before}: ${JSON.stringify(outcome.diagnostics)}`).toBe("passed");
      model = outcome.applied_model!;
    }
    expect(model.nodes.map(entry => entry.id)).not.toContain("node:free-a");
  });

  it("formats numbers as the applier's display_number does", () => {
    expect([0, -0, 2, -3, 1e15, 2.5e21, 0.5, 1e-7, -1.5e-8, 1.2345e-12, 0.1 + 0.2, 123456789.125].map(engineDisplayNumber))
      .toEqual(["0", "0", "2", "-3", "1000000000000000", "2500000000000000000000", "0.5", "0.0000001", "-0.000000015", "0.0000000000012345", "0.30000000000000004", "123456789.125"]);
  });

  it("stops reporting a component once the person's k, SIFs and source are entered", () => {
    const model = { components: [
      { id: "b", kind: "bend", modifiers: { sif_user_value: { value: 1.5, unit: "none" }, flexibility_factor_user_value: { value: 2, unit: "none" }, source_reference: "person" } },
      { id: "r", kind: "bend", mechanics_interface: { solver_consumption: "curved_bend_macro_element" }, modifiers: { sif_user_value: { value: 1.5, unit: "none" }, flexibility_factor_user_value: { value: 2, unit: "none" }, source_reference: "person" } },
      { id: "rp", kind: "bend", mechanics_interface: { solver_consumption: "curved_bend_macro_element" }, modifiers: { sif_in_plane_user_value: { value: 2.1, unit: "none" }, sif_out_of_plane_user_value: { value: 1.8, unit: "none" }, flexibility_factor_user_value: { value: 2, unit: "none" }, source_reference: "person" } },
      { id: "t", kind: "tee", modifiers: { branch_header_sif_user_value: { value: 1.4, unit: "none" }, branch_branch_sif_user_value: { value: 1.6, unit: "none" }, flexibility_factor_user_value: { value: 1, unit: "none" }, source_reference: " " } },
      { id: "v", kind: "valve" }
    ] } as unknown as PreviewModel;
    // A realized bend with only the scalar SIF still awaits the directional pair.
    expect(componentsAwaitingUserModifiers(model)).toEqual(["r", "t"]);
  });
});
