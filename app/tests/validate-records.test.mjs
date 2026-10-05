// Schema check of what the skeleton writes, against the Design schemas as they are.
//
// Runs the Rust tests that produce the outputs, then validates with Ajv (JSON
// Schema 2020-12, from the offline npm cache):
// - every RS entry the decide flow wrote -> DEL-04-03 RS_RECORD.schema.json
//   (act_request bodies resolve into DEL-02-03 checkpoint-record-entries.schema.json);
// - the A16 offer and capture -> DEL-01-04 aac.offer / aac.capture-evidence schemas;
// - the package file -> DEL-02-03 $defs/decisionPackageFile;
// - the hosting lifecycle events and client-request records (when the Codex test ran)
//   -> DEL-01-01 hosting.lifecycle-event / hosting.client-request-record schemas.
// The Design files are read unchanged and registered by their declared IDs.

import { after, test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { readFileSync, existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";

const here = dirname(fileURLToPath(import.meta.url));
const app = join(here, "..");
const exec = join(app, "..", "execution");
const design = (pkg, del) => join(exec, pkg, "1_Working", del, "Design");
const D0101 = design("PKG-01_Native App and third-party harness integration", "DEL-01-01_Stock Codex hosting and supplier contract");
const D0104 = design("PKG-01_Native App and third-party harness integration", "DEL-01-04_Native requests, outcomes and attachments");
const D0203 = design("PKG-02_Workflow and role portability", "DEL-02-03_Workflow execution compatibility and round-trip support");
const D0402 = design("PKG-04_Human acts, autonomy and run evidence", "DEL-04-02_Visible autonomy and result standing");
const D0403 = design("PKG-04_Human acts, autonomy and run evidence", "DEL-04-03_Content-bound decisions and compact run records");
// One run owns these evidence exports until all schema assertions finish.
const out = mkdtempSync(join(tmpdir(), "chirality-skeleton-output-"));
const rustEnv = { ...process.env, CHIRALITY_TEST_OUTPUT_DIRECTORY: out };
after(() => rmSync(out, { recursive: true }));

const readJson = (p) => JSON.parse(readFileSync(p, "utf8"));

function validators() {
  const ajv = new Ajv2020({ strict: false, allErrors: true });
  const checkpoint = readJson(join(D0203, "checkpoint-record-entries.schema.json"));
  const settingsIn = readJson(join(D0402, "AS_SETTINGS_IN.schema.json"));
  // CC-R CI-1: register the authoritative declared schema IDs without rewriting.
  const rs = readJson(join(D0403, "RS_RECORD.schema.json"));
  const offer = readJson(join(D0104, "aac.offer.schema.json"));
  const capture = readJson(join(D0104, "aac.capture-evidence.schema.json"));
  const lifecycle = readJson(join(D0101, "hosting.lifecycle-event.schema.json"));
  const clientRequest = readJson(join(D0101, "hosting.client-request-record.schema.json"));
  ajv.addSchema(checkpoint);
  ajv.addSchema(settingsIn);
  ajv.addSchema(rs);
  for (const schema of [offer, capture, lifecycle, clientRequest]) ajv.addSchema(schema);
  const get = (id) => {
    const v = ajv.getSchema(id);
    assert.ok(v, `schema ${id} compiles`);
    return v;
  };
  return {
    entry: get(rs.$id),
    offer: get(offer.$id),
    capture: get(capture.$id),
    packageFile: get(`${checkpoint.$id}#/$defs/decisionPackageFile`),
    lifecycle: get(lifecycle.$id),
    clientRequest: get(clientRequest.$id),
  };
}

const ok = (v, x, what) => assert.ok(v(x), `${what}: ${JSON.stringify(v.errors, null, 1)}`);

test("Rust decide flow runs and produces outputs", () => {
  execFileSync("cargo", ["test", "--offline", "--locked", "--test", "decide_flow"], { cwd: join(app, "src-tauri"), stdio: "inherit", env: rustEnv });
  assert.ok(existsSync(join(out, "decide-records.jsonl")));
});

test("decision record and act-control objects validate against the Design schemas", () => {
  const V = validators();
  const lines = readFileSync(join(out, "decide-records.jsonl"), "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
  assert.equal(lines.length, 5);
  assert.deepEqual(lines.map((e) => e.kind), ["act_request", "evidence_limit", "act_request", "evidence_limit", "human_act"]);
  const requests = lines.filter((e) => e.kind === "act_request");
  for (const req of requests) {
    assert.deepEqual(req.body.requester, { kind: "agent" }, "unobserved requester identity remains absent");
    const limit = lines.find((e) => e.kind === "evidence_limit" && e.body.subjectRef === req.recordId);
    assert.equal(limit?.body.label, "requester identity not established");
  }
  for (const e of lines) ok(V.entry, e, `RS entry ${e.recordId}`);
  const act = lines.find((e) => e.kind === "human_act");
  assert.equal(act.body.actKind, "A16");
  assert.equal(act.body.relations.alternativeChosen, "ALT-2");
  ok(V.offer, readJson(join(out, "decide-offer.json")), "AAC offer");
  ok(V.capture, readJson(join(out, "decide-capture.json")), "AAC capture evidence");
  for (const p of readJson(join(out, "decide-package-files.json"))) ok(V.packageFile, p, "decision package file");

  // Negative controls: the validator is live on the same entry.
  const noRequest = structuredClone(act);
  delete noRequest.body.relations.requestRef;
  assert.equal(V.entry(noRequest), false, "A16 without requestRef must fail");
  const recorderAsActor = structuredClone(act);
  recorderAsActor.body.actKind = "A9";
  assert.equal(V.entry(recorderAsActor), false, "A9 is not a person's act kind");
  // ... and on the act_request body, which resolves into DEL-02-03's CE-4.
  const noAlternatives = structuredClone(requests[0]);
  delete noAlternatives.body.alternatives;
  assert.equal(V.entry(noAlternatives), false, "a decision package request without alternatives must fail");
});

test("hosting lifecycle events and client-request records validate", (t) => {
  const p = join(out, "hosting-records.json");
  if (!process.env.CHIRALITY_CODEX_BIN) {
    t.skip("CHIRALITY_CODEX_BIN not set: the Codex handshake test did not run here");
    return;
  }
  execFileSync("cargo", ["test", "--offline", "--locked", "--test", "handshake"], { cwd: join(app, "src-tauri"), stdio: "inherit", env: rustEnv });
  const V = validators();
  const h = readJson(p);
  assert.ok(h.lifecycleEvents.length >= 6);
  for (const e of h.lifecycleEvents) ok(V.lifecycle, e, `lifecycle ${e.transitionId}`);
  for (const r of h.clientRequests) ok(V.clientRequest, r, `client request ${r.method}`);
  assert.equal(h.modelTurnExercised, false);
});
