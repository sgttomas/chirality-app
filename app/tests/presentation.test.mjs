// Pure display helpers (J6 D-1, D-2, D-3). Node 24 strips the TypeScript
// types of src/presentation.ts on import; no build step is involved.
import { test } from "node:test";
import assert from "node:assert/strict";
import {
  canonicalJson,
  nativePathText,
  readablePaths,
  reviewDigest,
  suppliedSummary,
} from "../src/presentation.ts";

test("review digest equals the vector the native A15 statement names (Rust canonical.rs)", async () => {
  // Same vector and value as act_control_a15.rs review_digest_vector_is_shared_with_the_app_view.
  const vector = { b: "x\u2028ü≈\u007f\u0001\n\"\\", a: [1, -2, true, null, { z: "😀", "é": 0, y: "\t\b\f\r" }], "😀": "astral key", "\uffff": "bmp max key" };
  const text = canonicalJson(vector);
  assert.ok(text.indexOf('"\uffff":') < text.indexOf('"😀":'), "code-point key order, not UTF-16 order");
  assert.equal(await reviewDigest(vector), "f0320f0cb802f23b0ca96ae972832215676a3c76e825efceb37c941e8e0e6d6b");
  assert.throws(() => canonicalJson({ x: 1.5 }));
});

test("native paths read as text; non-UTF-8 is marked; identities are not changed", () => {
  const bytes = (s) => Array.from(new TextEncoder().encode(s));
  const identity = { encoding: "unix_bytes", bytes: bytes("/Users/r/Prüfung lib") };
  assert.equal(nativePathText(identity), "/Users/r/Prüfung lib");
  const bad = nativePathText({ encoding: "unix_bytes", bytes: [47, 97, 0xff, 98, 0xc3] });
  assert.ok(bad.startsWith("[path is not valid UTF-8"), bad);
  assert.ok(bad.endsWith("/a\\xffb\\xc3"), bad);
  const wide = nativePathText({ encoding: "windows_utf16", codeUnits: [67, 58, 0xd800] });
  assert.ok(wide.startsWith("[path is not valid UTF-16") && wide.endsWith("C:\\u{d800}"), wide);
  assert.equal(nativePathText({ path: "x", bytes: 12 }), null, "manifest byte counts are not paths");
  const view = { selection: { root: identity, files: [{ path: "WORKFLOW.md", bytes: 12 }] } };
  const before = JSON.stringify(view);
  const shown = readablePaths(view);
  assert.equal(shown.selection.root, "/Users/r/Prüfung lib");
  assert.equal(shown.selection.files[0].bytes, 12);
  assert.equal(JSON.stringify(view), before, "display copy only; the reported identity is unchanged");
  const lines = (v) => JSON.stringify(v, null, 2).split("\n").length;
  assert.equal(lines(shown), 11);
  assert.ok(lines(view) > 30, "the raw identity printed one line per byte");
  assert.ok(!JSON.stringify(shown).includes("unix_bytes"));
});

test("run summary follows the latest supply check", () => {
  const run = { status: { supplied: "not yet checked" }, checks: [] };
  assert.equal(suppliedSummary(run), "not yet checked");
  run.checks.push({ state: "unverified", supplyReading: "supplied — not verified", readAt: "T1" });
  assert.equal(suppliedSummary(run), "unverified (supplied — not verified) at T1");
  run.checks.push({ state: "verified", supplyReading: "supplied", readAt: "T2" });
  assert.equal(suppliedSummary(run), "verified (supplied) at T2 (latest of 2 checks)");
  assert.equal(suppliedSummary({}), "see checks");
});
