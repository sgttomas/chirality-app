#!/usr/bin/env node
// Fake `codex` executable for the standalone entry tests: answers `--version`
// and serves the fake app-server over stdio for `-c ... app-server`.
import { createFakeCodexServer } from "./fake-codex-app-server.mjs";
const args = process.argv.slice(2);
if (args.includes("--version")) { process.stdout.write(`codex-cli ${process.env.FAKE_CODEX_VERSION ?? "0.154.0"}\n`); process.exit(0); }
if (args[args.length - 1] !== "app-server") { process.stderr.write("fake codex: unsupported invocation\n"); process.exit(2); }
const server = createFakeCodexServer({ signedIn: process.env.FAKE_CODEX_SIGNED_IN !== "0" });
server.attach(chunk => process.stdout.write(chunk));
process.stdin.setEncoding("utf8");
process.stdin.on("data", chunk => server.feed(chunk));
process.stdin.on("end", () => process.exit(0));
process.on("SIGTERM", () => process.exit(0));
