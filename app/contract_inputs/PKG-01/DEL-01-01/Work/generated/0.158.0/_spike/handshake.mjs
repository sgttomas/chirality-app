#!/usr/bin/env node
// W11 pin spike (APP-V4-FIRST-INCREMENT-20260928) — Codex 0.158.0 app-server
// stdio handshake / unknown-method / exit observation. Spike evidence only.
//
// Usage: node handshake.mjs <scratch-root> <scenario> [launcher]
//   scenario: A  initialize(experimentalApi=false) -> initialized -> unknown request
//                -> unknown notification -> duplicate initialize -> close stdin
//             B  initialize(experimentalApi=true) -> initialized -> unknown request -> close stdin
//             C  unknown request BEFORE initialize -> initialize -> close stdin
//             D  initialize -> initialized -> SIGTERM (stdin left open)
//   launcher: "bin" (default; <scratch>/pkg/node_modules/.bin/codex, the npm wrapper)
//             "vendor" (the platform binary under @openai/codex-darwin-arm64/vendor)
//
// Environment given to the child: the parent's environment with CODEX_HOME set to
// <scratch>/codex-home (an otherwise empty scratch dir). No sign-in, no model turn.
// Writes a raw transcript to <scratch>/handshake/<scenario>-<launcher>.jsonl.
// Frames are newline-delimited JSON on stdout (as observed); stderr is kept raw.

import { spawn, execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync, readdirSync, statSync } from "node:fs";
import path from "node:path";

const [scratch, scenario = "A", launcher = "bin"] = process.argv.slice(2);
if (!scratch) { console.error("usage: handshake.mjs <scratch-root> <A|B|C|D> [bin|vendor]"); process.exit(2); }

const codexHome = path.join(scratch, "codex-home");
const cwd = path.join(scratch, "cwd");
mkdirSync(codexHome, { recursive: true });
mkdirSync(cwd, { recursive: true });
const outDir = path.join(scratch, "handshake");
mkdirSync(outDir, { recursive: true });

const exe = launcher === "vendor"
  ? path.join(scratch, "pkg/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex")
  : path.join(scratch, "pkg/node_modules/.bin/codex");

const t0 = Date.now();
const rel = () => Date.now() - t0;
const events = [];
const rec = (e) => events.push({ t_ms: rel(), ...e });

const child = spawn(exe, ["app-server"], {
  cwd,
  env: { ...process.env, CODEX_HOME: codexHome },
  stdio: ["pipe", "pipe", "pipe"],
});
rec({ kind: "spawn", exe: launcher, args: ["app-server"], pid: child.pid });

let buf = "";
child.stdout.on("data", (chunk) => {
  buf += chunk.toString("utf8");
  let i;
  while ((i = buf.indexOf("\n")) >= 0) {
    const line = buf.slice(0, i); buf = buf.slice(i + 1);
    let parsed = null;
    try { parsed = JSON.parse(line); } catch { /* keep raw */ }
    rec({ kind: "recv", raw: line, parsed_ok: parsed !== null, frame: parsed });
  }
});
let stderr = "";
child.stderr.on("data", (c) => { stderr += c.toString("utf8"); });

const send = (obj) => {
  const line = JSON.stringify(obj);
  child.stdin.write(line + "\n");
  rec({ kind: "send", raw: line });
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const initParams = (experimentalApi) => ({
  clientInfo: { name: "chirality-w11-spike", title: "Chirality W11 pin spike", version: "0.0.0-spike" },
  capabilities: { experimentalApi, requestAttestation: false },
});

function descendants(root) {
  const all = [String(root)];
  for (let i = 0; i < all.length; i++) {
    try { all.push(...execFileSync("pgrep", ["-P", all[i]]).toString().trim().split(/\s+/).filter(Boolean)); } catch {}
  }
  return all;
}
const seenCommands = new Map();
function psOf(pids) {
  if (!pids.length) return [];
  try {
    return execFileSync("ps", ["-o", "pid=,ppid=,command=", "-p", pids.join(",")]).toString().trim().split("\n")
      .map((l) => l.trim().replace(/\s+/g, " "));
  } catch { return []; }
}
function snapshot(label) {
  // Which processes / sockets / files the child tree has open (observation only).
  try {
    const pids = descendants(child.pid);
    const ps = psOf(pids);
    for (const l of ps) seenCommands.set(l.split(" ")[0], l);
    const lsof = execFileSync("lsof", ["-n", "-P", "-p", pids.join(",")], { maxBuffer: 1 << 24 }).toString();
    rec({ kind: "snapshot", label, pids, ps, lsof_lines: lsof.split("\n").length,
      lsof_network: lsof.split("\n").filter((l) => /\b(IPv4|IPv6)\b/.test(l)),
      lsof_unix_sockets: lsof.split("\n").filter((l) => /\bunix\b/.test(l)).map((l) => l.replace(/\s+/g, " ")),
      lsof_codex_paths: lsof.split("\n").filter((l) => /\.codex\b|codex-home/.test(l)).map((l) => l.replace(/\s+/g, " ")) });
  } catch (e) { rec({ kind: "snapshot", label, error: String(e) }); }
}

const exited = new Promise((resolve) => {
  child.on("exit", (code, signal) => { rec({ kind: "exit", code, signal }); resolve(); });
});

(async () => {
  await sleep(300);
  if (scenario === "C") {
    send({ jsonrpc: "2.0", id: 1, method: "chirality/spikeUnknownMethod", params: {} });
    await sleep(800);
    send({ jsonrpc: "2.0", id: 2, method: "initialize", params: initParams(false) });
    await sleep(1500);
    rec({ kind: "close-stdin" }); child.stdin.end();
  } else {
    send({ jsonrpc: "2.0", id: 1, method: "initialize", params: initParams(scenario === "B") });
    await sleep(1500);
    snapshot("after-initialize-response");
    send({ jsonrpc: "2.0", method: "initialized" });
    await sleep(1500);
    snapshot("after-initialized");
    if (scenario !== "D") {
      send({ jsonrpc: "2.0", id: 2, method: "chirality/spikeUnknownMethod", params: {} });
      await sleep(800);
    }
    if (scenario === "A") {
      send({ jsonrpc: "2.0", method: "chirality/spikeUnknownNotification", params: {} });
      await sleep(800);
      send({ jsonrpc: "2.0", id: 3, method: "initialize", params: initParams(false) });
      await sleep(800);
    }
    if (scenario === "D") {
      rec({ kind: "signal-sent", signal: "SIGTERM" }); child.kill("SIGTERM");
    } else {
      rec({ kind: "close-stdin" }); child.stdin.end();
    }
  }
  const timer = setTimeout(() => { rec({ kind: "no-exit-within-10s; sending SIGKILL" }); child.kill("SIGKILL"); }, 10000);
  await exited; clearTimeout(timer);
  await sleep(500);
  const survivors = [...seenCommands.keys()].filter((p) => { try { process.kill(Number(p), 0); return true; } catch { return false; } });
  rec({ kind: "descendants-alive-500ms-after-exit", pids: survivors, ps: psOf(survivors) });
  if (buf.length) rec({ kind: "recv-partial-at-exit", raw: buf });
  rec({ kind: "stderr", bytes: Buffer.byteLength(stderr), text: stderr });
  const listing = [];
  const walk = (d) => { for (const n of readdirSync(d)) { const p = path.join(d, n); const s = statSync(p, { throwIfNoEntry: false }); if (!s) continue; listing.push(path.relative(codexHome, p) + (s.isDirectory() ? "/" : ` (${s.size} B)`)); if (s.isDirectory()) walk(p); } };
  walk(codexHome);
  rec({ kind: "codex-home-after", entries: listing });
  const file = path.join(outDir, `${scenario}-${launcher}.jsonl`);
  writeFileSync(file, events.map((e) => JSON.stringify(e)).join("\n") + "\n");
  console.log(`wrote ${file} (${events.length} events)`);
})();
