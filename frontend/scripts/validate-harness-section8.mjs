#!/usr/bin/env node

import { chmod, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const SCRIPT_DIR = path.dirname(SCRIPT_PATH);
const PROJECT_ROOT = path.resolve(SCRIPT_DIR, "..", "..");

const BASE_URL = process.env.HARNESS_BASE_URL ?? "http://127.0.0.1:3000";
const REQUEST_TIMEOUT_MS = Number(process.env.HARNESS_REQUEST_TIMEOUT_MS ?? "180000");

const ARTIFACT_ROOT =
  process.env.HARNESS_VALIDATION_ARTIFACT_ROOT ?? path.join(os.tmpdir(), "chirality-harness-validation");
const ARTIFACT_DIR = path.join(ARTIFACT_ROOT, "latest");

const HARNESS_LOG_PATH = path.join(PROJECT_ROOT, ".chirality", "logs", "harness.log");
const SESSIONS_DIR = path.join(PROJECT_ROOT, ".chirality", "sessions");
const AGENTS_DIR = path.join(PROJECT_ROOT, "agents");
const BOOT_TEST_PERSONA_ID = "BOOT_TEST_TMP";
const BOOT_TEST_PERSONA_FILE = path.join(PROJECT_ROOT, "agents", `AGENT_${BOOT_TEST_PERSONA_ID}.md`);
const SUBAGENT_ALLOWLIST_FOR_VALIDATION = ["ORCHESTRATOR", "RECONCILIATION"];

const SENTINELS = {
  deny: "UNAPPROVED_DENY_TEST",
  allow: "UNAPPROVED_ALLOW_TEST",
};

const tests = [];
const sessionsToCleanup = new Map();
const context = {
  smokeSessionId: null,
};

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function sanitizeRelPath(relPath) {
  return relPath.split(path.sep).join("/");
}

async function ensureDir(dirPath) {
  await mkdir(dirPath, { recursive: true });
}

async function writeTextArtifact(relPath, content) {
  const safeRelPath = sanitizeRelPath(relPath);
  const filePath = path.join(ARTIFACT_DIR, safeRelPath);
  await ensureDir(path.dirname(filePath));
  await writeFile(filePath, content, "utf8");
  return filePath;
}

async function writeJsonArtifact(relPath, value) {
  return writeTextArtifact(relPath, `${JSON.stringify(value, null, 2)}\n`);
}

function rememberSession(baseUrl, sessionId) {
  const existing = sessionsToCleanup.get(baseUrl) ?? new Set();
  existing.add(sessionId);
  sessionsToCleanup.set(baseUrl, existing);
}

function clearSessionFromCleanup(baseUrl, sessionId) {
  const existing = sessionsToCleanup.get(baseUrl);
  if (!existing) {
    return;
  }

  existing.delete(sessionId);
}

function withTimeoutSignal(timeoutMs) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(`Timed out after ${timeoutMs}ms`), timeoutMs);
  return {
    signal: controller.signal,
    clear: () => clearTimeout(timeout),
  };
}

async function requestJson(baseUrl, route, { method = "GET", body, timeoutMs = REQUEST_TIMEOUT_MS } = {}) {
  const url = `${baseUrl}${route}`;
  const payload = body === undefined ? undefined : JSON.stringify(body);
  const headers = payload ? { "Content-Type": "application/json" } : undefined;
  const timeout = withTimeoutSignal(timeoutMs);

  try {
    const res = await fetch(url, {
      method,
      headers,
      body: payload,
      signal: timeout.signal,
    });
    const text = await res.text();
    let json = null;

    try {
      json = text ? JSON.parse(text) : null;
    } catch {
      json = null;
    }

    return {
      url,
      status: res.status,
      headers: Object.fromEntries(res.headers.entries()),
      text,
      json,
    };
  } finally {
    timeout.clear();
  }
}

function parseSseBlock(rawBlock) {
  const block = rawBlock.replace(/\r/g, "").trim();
  if (!block) {
    return null;
  }

  let eventName = "message";
  const dataParts = [];

  for (const line of block.split("\n")) {
    if (line.startsWith("event:")) {
      eventName = line.slice("event:".length).trim();
      continue;
    }
    if (line.startsWith("data:")) {
      dataParts.push(line.slice("data:".length).trimStart());
    }
  }

  const dataRaw = dataParts.join("\n");
  let data = null;
  if (dataRaw) {
    try {
      data = JSON.parse(dataRaw);
    } catch {
      data = null;
    }
  }

  return {
    event: eventName,
    dataRaw,
    data,
  };
}

function normalizeAgentId(raw) {
  if (typeof raw !== "string") {
    return null;
  }

  const trimmed = raw.trim().replace(/^['"]|['"]$/g, "");
  if (!trimmed) {
    return null;
  }

  return trimmed.replace(/^AGENT_/i, "").replace(/\.md$/i, "").toUpperCase();
}

function splitFrontmatter(document) {
  const normalized = document.replace(/\r\n/g, "\n");
  const match = normalized.match(/^---\n([\s\S]*?)\n---(?:\n|$)/);
  if (!match) {
    return { frontmatter: "", body: normalized.trim() };
  }

  return {
    frontmatter: match[1],
    body: normalized.slice(match[0].length).trim(),
  };
}

function parseSubagentsFrontmatter(frontmatterText) {
  if (!frontmatterText) {
    return [];
  }

  const lines = frontmatterText.split("\n");
  const parsed = [];

  for (let index = 0; index < lines.length; index += 1) {
    const match = lines[index].match(/^\s*subagents\s*:\s*(.*)$/i);
    if (!match) {
      continue;
    }

    const inline = match[1].trim();
    if (inline) {
      for (const token of inline.split(",")) {
        const normalized = normalizeAgentId(token);
        if (normalized) {
          parsed.push(normalized);
        }
      }
      continue;
    }

    let cursor = index + 1;
    while (cursor < lines.length) {
      const itemMatch = lines[cursor].match(/^\s*-\s*(.+)\s*$/);
      if (!itemMatch) {
        break;
      }

      const normalized = normalizeAgentId(itemMatch[1]);
      if (normalized) {
        parsed.push(normalized);
      }
      cursor += 1;
    }
  }

  return [...new Set(parsed)];
}

function parseAgentTypeFromBody(body) {
  const match = body.match(/^AGENT_TYPE:\s*([0-2])\s*$/m);
  if (!match) {
    return null;
  }

  return Number.parseInt(match[1], 10);
}

async function resolveSubagentOffParityPersona() {
  for (const personaId of SUBAGENT_ALLOWLIST_FOR_VALIDATION) {
    const personaFile = path.join(AGENTS_DIR, `AGENT_${personaId}.md`);
    let personaRaw;
    try {
      personaRaw = await readFile(personaFile, "utf8");
    } catch {
      continue;
    }

    const { frontmatter } = splitFrontmatter(personaRaw);
    const declaredSubagents = parseSubagentsFrontmatter(frontmatter);
    if (declaredSubagents.length === 0) {
      continue;
    }

    const eligibleSubagents = [];
    for (const subagentId of declaredSubagents) {
      const subagentFile = path.join(AGENTS_DIR, `AGENT_${subagentId}.md`);
      let subagentRaw;
      try {
        subagentRaw = await readFile(subagentFile, "utf8");
      } catch {
        continue;
      }

      const { body } = splitFrontmatter(subagentRaw);
      if (parseAgentTypeFromBody(body) === 2) {
        eligibleSubagents.push(subagentId);
      }
    }

    if (eligibleSubagents.length > 0) {
      return {
        personaId,
        declaredSubagents,
        eligibleSubagents,
      };
    }
  }

  return null;
}

async function streamTurn(baseUrl, payload, artifactRelPath, onEvent) {
  const url = `${baseUrl}/api/harness/turn`;
  const timeout = withTimeoutSignal(REQUEST_TIMEOUT_MS);

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: timeout.signal,
    });

    if (!res.body) {
      const text = await res.text();
      const artifactPath = await writeTextArtifact(artifactRelPath, text);
      return {
        status: res.status,
        events: [],
        raw: text,
        artifactPath,
      };
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let raw = "";
    const events = [];

    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        break;
      }

      const chunk = decoder.decode(value, { stream: true });
      raw += chunk;
      buffer += chunk;

      let splitIndex = buffer.indexOf("\n\n");
      while (splitIndex >= 0) {
        const block = buffer.slice(0, splitIndex);
        buffer = buffer.slice(splitIndex + 2);

        const parsed = parseSseBlock(block);
        if (parsed) {
          events.push(parsed);
          if (onEvent) {
            await onEvent(parsed);
          }
        }

        splitIndex = buffer.indexOf("\n\n");
      }
    }

    const tail = decoder.decode();
    if (tail) {
      raw += tail;
      buffer += tail;
    }

    if (buffer.trim()) {
      const parsed = parseSseBlock(buffer);
      if (parsed) {
        events.push(parsed);
        if (onEvent) {
          await onEvent(parsed);
        }
      }
    }

    const artifactPath = await writeTextArtifact(artifactRelPath, raw);
    return {
      status: res.status,
      events,
      raw,
      artifactPath,
    };
  } finally {
    timeout.clear();
  }
}

function eventNames(events) {
  return events.map((event) => event.event);
}

function findEvent(events, eventName) {
  return events.find((event) => event.event === eventName);
}

function assertOrder(events, ordered) {
  let last = -1;
  for (const eventName of ordered) {
    const index = events.indexOf(eventName);
    assert(index >= 0, `Expected SSE event "${eventName}"`);
    assert(index > last, `Expected SSE event order ${ordered.join(" -> ")}`);
    last = index;
  }
}

async function readHarnessLogs() {
  try {
    const raw = await readFile(HARNESS_LOG_PATH, "utf8");
    const lines = raw.split("\n").map((line) => line.trim()).filter(Boolean);
    const parsed = [];

    for (const line of lines) {
      try {
        parsed.push(JSON.parse(line));
      } catch {
        // Skip malformed log lines.
      }
    }

    return parsed;
  } catch {
    return [];
  }
}

async function createSession(baseUrl, label, { persona = null, mode = "direct" } = {}) {
  const response = await requestJson(baseUrl, "/api/harness/session/create", {
    method: "POST",
    body: {
      projectRoot: PROJECT_ROOT,
      persona,
      mode,
    },
  });
  await writeJsonArtifact(`api/${label}-create.json`, response);

  assert(response.status === 201, `Expected 201 creating session (${label}), got ${response.status}`);
  const session = response.json?.session;
  assert(session && typeof session.id === "string", `Invalid create session payload for ${label}`);
  rememberSession(baseUrl, session.id);
  return session;
}

async function deleteSession(baseUrl, sessionId, label) {
  const response = await requestJson(baseUrl, `/api/harness/session/${encodeURIComponent(sessionId)}`, {
    method: "DELETE",
  });
  await writeJsonArtifact(`api/${label}-delete.json`, response);
  assert(response.status === 204, `Expected 204 deleting session ${sessionId}, got ${response.status}`);
  clearSessionFromCleanup(baseUrl, sessionId);
}

async function bootSession(baseUrl, sessionId, label, { force = false, opts } = {}) {
  const response = await requestJson(baseUrl, "/api/harness/session/boot", {
    method: "POST",
    body: {
      sessionId,
      force,
      ...(opts ? { opts } : {}),
    },
  });
  await writeJsonArtifact(`api/${label}-boot.json`, response);
  return response;
}

async function cleanupSessions() {
  const cleanupResults = [];

  for (const [baseUrl, ids] of sessionsToCleanup.entries()) {
    for (const sessionId of ids) {
      const response = await requestJson(baseUrl, `/api/harness/session/${encodeURIComponent(sessionId)}`, {
        method: "DELETE",
        timeoutMs: 30_000,
      }).catch((error) => ({ error: error instanceof Error ? error.message : String(error) }));

      cleanupResults.push({
        baseUrl,
        sessionId,
        response,
      });
    }
  }

  await writeJsonArtifact("cleanup/sessions.json", cleanupResults);
}

async function runTest(id, name, fn) {
  const startedAt = Date.now();
  try {
    const details = await fn();
    tests.push({
      id,
      name,
      status: "pass",
      durationMs: Date.now() - startedAt,
      details: details ?? {},
    });
  } catch (error) {
    tests.push({
      id,
      name,
      status: "fail",
      durationMs: Date.now() - startedAt,
      error: error instanceof Error ? error.message : String(error),
    });
  }
}

async function ensureMainServerReachable() {
  const response = await requestJson(BASE_URL, `/api/harness/session/list?projectRoot=${encodeURIComponent(PROJECT_ROOT)}`, {
    method: "GET",
    timeoutMs: 10_000,
  });
  await writeJsonArtifact("api/main-server-reachability.json", response);
  assert(
    response.status === 200,
    `Harness server is unreachable at ${BASE_URL}. Start frontend dev server before running this validation script.`,
  );
}

async function main() {
  await rm(ARTIFACT_DIR, { recursive: true, force: true });
  await ensureDir(path.join(ARTIFACT_DIR, "api"));
  await ensureDir(path.join(ARTIFACT_DIR, "sse"));
  await ensureDir(path.join(ARTIFACT_DIR, "logs"));
  await chmod(SCRIPT_PATH, 0o755);

  await runTest("setup.server_reachable", "Main harness server reachability", async () => {
    await ensureMainServerReachable();
    return { baseUrl: BASE_URL };
  });

  await runTest("regression.session_crud", "Session CRUD regression", async () => {
    const session = await createSession(BASE_URL, "crud");

    const listResponse = await requestJson(
      BASE_URL,
      `/api/harness/session/list?projectRoot=${encodeURIComponent(PROJECT_ROOT)}`,
      { method: "GET" },
    );
    await writeJsonArtifact("api/crud-list.json", listResponse);
    assert(listResponse.status === 200, `Expected 200 from session/list, got ${listResponse.status}`);
    assert(Array.isArray(listResponse.json), "Expected array response from session/list.");
    assert(listResponse.json.some((item) => item && item.id === session.id), "Newly created session missing from list.");

    const getResponse = await requestJson(BASE_URL, `/api/harness/session/${encodeURIComponent(session.id)}`, {
      method: "GET",
    });
    await writeJsonArtifact("api/crud-get.json", getResponse);
    assert(getResponse.status === 200, `Expected 200 from session/:id, got ${getResponse.status}`);
    assert(getResponse.json?.session?.id === session.id, "Session GET response did not match created session.");

    await deleteSession(BASE_URL, session.id, "crud");

    const afterDeleteResponse = await requestJson(BASE_URL, `/api/harness/session/${encodeURIComponent(session.id)}`, {
      method: "GET",
    });
    await writeJsonArtifact("api/crud-get-after-delete.json", afterDeleteResponse);
    const isNotFoundAfterDelete =
      afterDeleteResponse.status === 404 ||
      (afterDeleteResponse.status === 500 &&
        typeof afterDeleteResponse.json?.error === "string" &&
        afterDeleteResponse.json.error.toLowerCase().includes("not found"));
    assert(isNotFoundAfterDelete, `Expected not-found after delete, got status ${afterDeleteResponse.status}.`);

    return { sessionId: session.id };
  });

  await runTest("section8.session_boot_endpoint", "Session boot endpoint idempotency", async () => {
    const session = await createSession(BASE_URL, "boot-endpoint");

    const firstBoot = await bootSession(BASE_URL, session.id, "boot-endpoint-initial");
    assert(firstBoot.status === 200, `Expected 200 from first boot call, got ${firstBoot.status}`);
    assert(firstBoot.json?.boot?.booted === true, "Expected first boot call to perform bootstrap.");
    assert(typeof firstBoot.json?.session?.claudeSessionId === "string", "First boot call missing claudeSessionId.");
    assert(typeof firstBoot.json?.session?.bootFingerprint === "string", "First boot call missing bootFingerprint.");
    assert(typeof firstBoot.json?.session?.bootedAt === "string", "First boot call missing bootedAt.");

    const secondBoot = await bootSession(BASE_URL, session.id, "boot-endpoint-repeat");
    assert(secondBoot.status === 200, `Expected 200 from second boot call, got ${secondBoot.status}`);
    assert(secondBoot.json?.boot?.booted === false, "Expected second boot call to be a no-op.");
    assert(secondBoot.json?.boot?.reason === "already_booted", "Expected no-op boot reason to be already_booted.");

    return {
      sessionId: session.id,
      firstReason: firstBoot.json?.boot?.reason ?? null,
      secondReason: secondBoot.json?.boot?.reason ?? null,
      bootFingerprint: firstBoot.json?.session?.bootFingerprint ?? null,
    };
  });

  await runTest("section8.boot_fingerprint_drift", "Boot fingerprint drift triggers re-bootstrap", async () => {
    const personaInitial = `---\nmax_turns: 2\n---\nPersona bootstrap content v1\n`;
    const personaUpdated = `---\nmax_turns: 2\n---\nPersona bootstrap content v2\n`;
    await writeFile(BOOT_TEST_PERSONA_FILE, personaInitial, "utf8");

    try {
      const session = await createSession(BASE_URL, "boot-fingerprint", {
        persona: BOOT_TEST_PERSONA_ID,
        mode: "workbench",
      });

      const initialBoot = await bootSession(BASE_URL, session.id, "boot-fingerprint-initial");
      assert(initialBoot.status === 200, `Expected 200 from initial fingerprint boot, got ${initialBoot.status}`);
      const fingerprintBefore = initialBoot.json?.session?.bootFingerprint;
      assert(typeof fingerprintBefore === "string", "Initial boot fingerprint is missing.");

      await writeFile(BOOT_TEST_PERSONA_FILE, personaUpdated, "utf8");

      const driftBoot = await bootSession(BASE_URL, session.id, "boot-fingerprint-after-drift");
      assert(driftBoot.status === 200, `Expected 200 from drift boot call, got ${driftBoot.status}`);
      assert(driftBoot.json?.boot?.booted === true, "Expected drift boot call to re-bootstrap.");
      assert(
        driftBoot.json?.boot?.reason === "fingerprint_changed",
        `Expected drift boot reason fingerprint_changed, got ${driftBoot.json?.boot?.reason ?? "unknown"}.`,
      );

      const fingerprintAfter = driftBoot.json?.session?.bootFingerprint;
      assert(typeof fingerprintAfter === "string", "Drift boot fingerprint is missing.");
      assert(fingerprintAfter !== fingerprintBefore, "Boot fingerprint did not change after persona file update.");

      return {
        sessionId: session.id,
        reason: driftBoot.json?.boot?.reason ?? null,
        fingerprintBefore,
        fingerprintAfter,
      };
    } finally {
      await rm(BOOT_TEST_PERSONA_FILE, { force: true }).catch(() => undefined);
    }
  });

  await runTest("section8.smoke_stream", "Smoke stream ordering", async () => {
    const session = await createSession(BASE_URL, "smoke");

    const turn = await streamTurn(
      BASE_URL,
      {
        sessionId: session.id,
        message: "Respond with exactly: smoke harness ok",
        opts: { maxTurns: 1 },
      },
      "sse/turn-smoke.sse",
    );
    await writeJsonArtifact("api/smoke-turn-meta.json", {
      status: turn.status,
      events: eventNames(turn.events),
      artifactPath: turn.artifactPath,
    });

    assert(turn.status === 200, `Expected 200 from turn smoke request, got ${turn.status}`);
    const names = eventNames(turn.events);
    assertOrder(names, ["chat:delta", "chat:complete", "process:exit"]);

    const initEvent = findEvent(turn.events, "session:init");
    const claudeSessionId = initEvent?.data?.claudeSessionId;
    assert(typeof claudeSessionId === "string" && claudeSessionId.length > 0, "session:init missing claudeSessionId.");

    context.smokeSessionId = session.id;

    return {
      sessionId: session.id,
      claudeSessionId,
      events: names,
      artifactPath: turn.artifactPath,
    };
  });

  await runTest("section8.session_persistence_resume", "Session init persistence + --resume continuity", async () => {
    const sessionId = context.smokeSessionId;
    assert(typeof sessionId === "string" && sessionId.length > 0, "Smoke session was not captured.");

    const getBefore = await requestJson(BASE_URL, `/api/harness/session/${encodeURIComponent(sessionId)}`, {
      method: "GET",
    });
    await writeJsonArtifact("api/resume-get-before.json", getBefore);
    assert(getBefore.status === 200, `Expected 200 from session/:id before resume, got ${getBefore.status}`);
    const persistedBefore = getBefore.json?.session?.claudeSessionId;
    assert(typeof persistedBefore === "string" && persistedBefore.length > 0, "Persisted claudeSessionId missing before resume.");

    const sessionFilePath = path.join(SESSIONS_DIR, `${sessionId}.json`);
    const sessionFileRaw = await readFile(sessionFilePath, "utf8");
    await writeTextArtifact("logs/session-file-before-resume.json", sessionFileRaw);
    const sessionFileParsed = JSON.parse(sessionFileRaw);
    assert(
      sessionFileParsed?.claudeSessionId === persistedBefore,
      "Session file claudeSessionId does not match session API response.",
    );

    const resumeTurn = await streamTurn(
      BASE_URL,
      {
        sessionId,
        message: "Respond with exactly: resume harness ok",
        opts: { maxTurns: 1 },
      },
      "sse/turn-resume.sse",
    );
    await writeJsonArtifact("api/resume-turn-meta.json", {
      status: resumeTurn.status,
      events: eventNames(resumeTurn.events),
      artifactPath: resumeTurn.artifactPath,
    });
    assert(resumeTurn.status === 200, `Expected 200 from resume turn request, got ${resumeTurn.status}`);
    assertOrder(eventNames(resumeTurn.events), ["chat:complete", "process:exit"]);

    const resumeInit = findEvent(resumeTurn.events, "session:init");
    const resumedClaudeSessionId = resumeInit?.data?.claudeSessionId;
    assert(
      typeof resumedClaudeSessionId === "string" && resumedClaudeSessionId.length > 0,
      "Resume turn did not emit session:init with claudeSessionId.",
    );

    const getAfter = await requestJson(BASE_URL, `/api/harness/session/${encodeURIComponent(sessionId)}`, {
      method: "GET",
    });
    await writeJsonArtifact("api/resume-get-after.json", getAfter);
    assert(getAfter.status === 200, `Expected 200 from session/:id after resume, got ${getAfter.status}`);
    const persistedAfter = getAfter.json?.session?.claudeSessionId;
    assert(
      persistedAfter === resumedClaudeSessionId,
      "Persisted claudeSessionId after resume does not match latest session:init event.",
    );

    const logs = await readHarnessLogs();
    const turnStarts = logs.filter((entry) => entry && entry.sessionId === sessionId && entry.event === "turn:start");
    const processExits = logs.filter((entry) => entry && entry.sessionId === sessionId && entry.event === "process:exit");
    await writeJsonArtifact("logs/resume-runtime-markers.json", {
      turnStartCount: turnStarts.length,
      processExitCount: processExits.length,
    });
    assert(turnStarts.length >= 2, "Expected at least two turn:start log entries for initial + resumed turns.");
    assert(processExits.length >= 2, "Expected at least two process:exit log entries for initial + resumed turns.");

    return {
      sessionId,
      persistedClaudeSessionId: persistedBefore,
      resumedClaudeSessionId,
      turnStartCount: turnStarts.length,
      processExitCount: processExits.length,
    };
  });

  await runTest("section8.subagents_off_parity", "Subagents disabled parity (no side effects)", async () => {
    const parityPersona = await resolveSubagentOffParityPersona();
    assert(
      parityPersona,
      "Could not find an allowlisted Type 1 persona with declared AGENT_TYPE:2 subagents for parity validation.",
    );

    const session = await createSession(BASE_URL, "subagents-off", {
      persona: parityPersona.personaId,
      mode: "workbench",
    });

    const parityTurn = await streamTurn(
      BASE_URL,
      {
        sessionId: session.id,
        message: "Respond with exactly: subagents off parity ok",
        opts: {
          maxTurns: 1,
          subagentGovernance: {
            contextSealed: true,
            pipelineRunApproved: true,
            approvalRef: "validation/subagents-off",
            approvedBy: "section8-validator",
          },
        },
      },
      "sse/turn-subagents-off-parity.sse",
    );
    await writeJsonArtifact("api/subagents-off-parity-meta.json", {
      status: parityTurn.status,
      events: eventNames(parityTurn.events),
      artifactPath: parityTurn.artifactPath,
      personaId: parityPersona.personaId,
      declaredSubagents: parityPersona.declaredSubagents,
      eligibleSubagents: parityPersona.eligibleSubagents,
    });
    assert(parityTurn.status === 200, `Expected 200 from subagents-off parity turn, got ${parityTurn.status}`);
    assert(eventNames(parityTurn.events).includes("process:exit"), "Subagents-off parity turn did not emit process:exit.");

    const logs = await readHarnessLogs();
    const forbiddenEvents = new Set([
      "subagent:registry_applied",
      "subagent:start",
      "subagent:complete",
      "subagent:interrupted",
    ]);
    const subagentSideEffects = logs.filter((entry) => {
      return entry && entry.sessionId === session.id && forbiddenEvents.has(entry.event);
    });
    await writeJsonArtifact("logs/subagents-off-parity-side-effects.json", {
      sessionId: session.id,
      personaId: parityPersona.personaId,
      count: subagentSideEffects.length,
      events: subagentSideEffects,
    });

    assert(
      subagentSideEffects.length === 0,
      "Subagents-off parity regression: observed subagent lifecycle log side effects for flag-off path.",
    );

    return {
      sessionId: session.id,
      personaId: parityPersona.personaId,
      sideEffectCount: subagentSideEffects.length,
      eligibleSubagentCount: parityPersona.eligibleSubagents.length,
    };
  });

  await runTest("section8.permissions_dontask", "Permissions under dontAsk (deny + allow)", async () => {
    const denySession = await createSession(BASE_URL, "perm-deny");
    const denyTurn = await streamTurn(
      BASE_URL,
      {
        sessionId: denySession.id,
        message: `Use Bash to run: echo ${SENTINELS.deny}`,
        opts: {
          permissionMode: "dontAsk",
          tools: "Read",
          maxTurns: 2,
        },
      },
      "sse/turn-perm-deny.sse",
    );
    await writeJsonArtifact("api/perm-deny-meta.json", {
      status: denyTurn.status,
      events: eventNames(denyTurn.events),
      artifactPath: denyTurn.artifactPath,
    });
    assert(denyTurn.status === 200, `Expected 200 from deny turn, got ${denyTurn.status}`);
    assert(eventNames(denyTurn.events).includes("process:exit"), "Deny turn did not emit process:exit.");

    const denyBashExecution = denyTurn.events.find((event) => {
      return (
        event.event === "tool:result" &&
        event.data?.isError === false &&
        typeof event.data?.content === "string" &&
        event.data.content.includes(SENTINELS.deny)
      );
    });
    assert(!denyBashExecution, "Deny case unexpectedly executed Bash command output.");

    const allowSession = await createSession(BASE_URL, "perm-allow");
    const allowTurn = await streamTurn(
      BASE_URL,
      {
        sessionId: allowSession.id,
        message: `Use Bash to run: echo ${SENTINELS.allow}`,
        opts: {
          permissionMode: "dontAsk",
          tools: "Bash",
          autoApproveTools: ["Bash(echo *)"],
          maxTurns: 2,
        },
      },
      "sse/turn-perm-allow.sse",
    );
    await writeJsonArtifact("api/perm-allow-meta.json", {
      status: allowTurn.status,
      events: eventNames(allowTurn.events),
      artifactPath: allowTurn.artifactPath,
    });
    assert(allowTurn.status === 200, `Expected 200 from allow turn, got ${allowTurn.status}`);
    assert(eventNames(allowTurn.events).includes("process:exit"), "Allow turn did not emit process:exit.");

    const allowToolResult = allowTurn.events.find((event) => {
      return (
        event.event === "tool:result" &&
        event.data?.isError === false &&
        typeof event.data?.content === "string" &&
        event.data.content.includes(SENTINELS.allow)
      );
    });
    assert(Boolean(allowToolResult), "Allow case did not emit approved Bash tool result content.");

    return {
      denySessionId: denySession.id,
      allowSessionId: allowSession.id,
    };
  });

  await runTest("section8.interrupt_sigint", "Interrupt behavior (SIGINT path)", async () => {
    const session = await createSession(BASE_URL, "interrupt");
    let interruptResponse = null;
    let interruptAttempted = false;

    const sendInterrupt = async () => {
      if (interruptAttempted) {
        return;
      }
      interruptAttempted = true;
      interruptResponse = await requestJson(BASE_URL, "/api/harness/interrupt", {
        method: "POST",
        body: { sessionId: session.id },
      });
      await writeJsonArtifact("api/interrupt-response.json", interruptResponse);
    };

    const interruptTurn = await streamTurn(
      BASE_URL,
      {
        sessionId: session.id,
        message: "Use Bash to run exactly: sleep 20",
        opts: {
          permissionMode: "dontAsk",
          tools: "Bash",
          autoApproveTools: ["Bash(sleep *)"],
          maxTurns: 2,
        },
      },
      "sse/turn-interrupt.sse",
      async (event) => {
        if (!interruptAttempted && (event.event === "tool:start" || event.event === "session:init" || event.event === "chat:delta")) {
          await sendInterrupt();
        }
      },
    );

    if (!interruptAttempted) {
      await sendInterrupt();
    }

    assert(interruptResponse?.status === 200, `Expected 200 from interrupt endpoint, got ${interruptResponse?.status ?? "none"}`);
    assert(interruptResponse?.json?.ok === true, "Interrupt response body missing ok=true.");

    const names = eventNames(interruptTurn.events);
    assert(names.includes("process:exit"), "Interrupt turn did not emit process:exit.");
    assert(!names.includes("session:complete"), "Interrupt turn unexpectedly completed successfully.");

    const exitEvent = findEvent(interruptTurn.events, "process:exit");
    const signal = exitEvent?.data?.signal ?? null;
    const exitCode = exitEvent?.data?.code ?? null;
    const sessionErrorEvent = findEvent(interruptTurn.events, "session:error");
    const sessionErrorText =
      typeof sessionErrorEvent?.data?.error === "string" ? sessionErrorEvent.data.error : "";
    const sigintLike =
      signal === "SIGINT" ||
      sessionErrorText.toUpperCase().includes("SIGINT") ||
      sessionErrorText.toLowerCase().includes("interrupt");
    assert(sigintLike, "Interrupt path did not produce an SDK interruption marker.");

    return {
      sessionId: session.id,
      exitSignal: signal,
      exitCode,
      hasSessionError: sessionErrorText.length > 0,
      sessionError: sessionErrorText,
      interruptStatus: interruptResponse.status,
      interruptArtifact: path.join(ARTIFACT_DIR, "api", "interrupt-response.json"),
    };
  });

  await runTest("section8.sdk_native_stream", "SDK-native stream handling (no NDJSON parse layer)", async () => {
    const session = await createSession(BASE_URL, "sdk-native");

    const turn = await streamTurn(
      BASE_URL,
      {
        sessionId: session.id,
        message: "Respond with exactly: sdk native stream ok",
        opts: { maxTurns: 1 },
      },
      "sse/turn-sdk-native.sse",
    );
    await writeJsonArtifact("api/sdk-native-meta.json", {
      status: turn.status,
      events: eventNames(turn.events),
      artifactPath: turn.artifactPath,
    });

    assert(turn.status === 200, `Expected 200 from sdk-native turn, got ${turn.status}`);
    const names = eventNames(turn.events);
    assert(names.includes("chat:complete"), "SDK-native turn did not emit chat:complete.");
    assert(names.includes("process:exit"), "SDK-native turn did not emit process:exit.");

    const logs = await readHarnessLogs();
    const parseErrors = logs.filter((entry) => entry && entry.sessionId === session.id && entry.event === "parse:error");
    await writeJsonArtifact("logs/sdk-native-parse-errors.json", parseErrors);
    assert(parseErrors.length === 0, "SDK-native runtime unexpectedly emitted parse:error logs.");

    return {
      sessionId: session.id,
      parseErrorCount: parseErrors.length,
      eventCount: names.length,
    };
  });

  await cleanupSessions();

  const failed = tests.filter((test) => test.status === "fail");
  const summary = {
    generatedAt: new Date().toISOString(),
    baseUrl: BASE_URL,
    projectRoot: PROJECT_ROOT,
    artifactDir: ARTIFACT_DIR,
    totals: {
      total: tests.length,
      passed: tests.length - failed.length,
      failed: failed.length,
    },
    status: failed.length === 0 ? "pass" : "fail",
    tests,
  };

  const summaryPath = await writeJsonArtifact("summary.json", summary);
  console.log(JSON.stringify(summary, null, 2));
  console.log(`HARNESS_VALIDATION_SUMMARY_PATH=${summaryPath}`);
  console.log(`HARNESS_VALIDATION_STATUS=${summary.status}`);

  if (summary.status === "fail") {
    process.exitCode = 1;
  }
}

main().catch(async (error) => {
  try {
    await writeJsonArtifact("fatal-error.json", {
      error: error instanceof Error ? error.message : String(error),
      stack: error instanceof Error ? error.stack : null,
    });
  } catch {
    // Ignore artifact write failures on fatal path.
  }

  const message = error instanceof Error ? error.stack ?? error.message : String(error);
  console.error(message);
  process.exit(1);
});
