import { randomUUID } from "node:crypto";
import type { Dirent } from "node:fs";
import { access, mkdir, readdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import path from "node:path";

import type { Session, SessionMode, SessionSummary } from "./types";

const SESSIONS_DIR_PARTS = [".chirality", "sessions"] as const;

const SESSION_MODES: readonly SessionMode[] = ["workbench", "pipeline", "direct"];

type SessionRecord = Record<string, unknown>;

function isSessionMode(value: unknown): value is SessionMode {
  return typeof value === "string" && SESSION_MODES.includes(value as SessionMode);
}

function isObject(value: unknown): value is SessionRecord {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function toIsoString(value: unknown): string | null {
  if (typeof value !== "string") {
    return null;
  }

  const timestamp = Date.parse(value);
  if (Number.isNaN(timestamp)) {
    return null;
  }

  return new Date(timestamp).toISOString();
}

function buildSessionSummary(session: Session): SessionSummary {
  return {
    id: session.id,
    createdAt: session.createdAt,
    updatedAt: session.updatedAt,
    persona: session.persona,
    mode: session.mode,
    projectRoot: session.projectRoot,
  };
}

function parseSession(contents: string): Session | null {
  let parsed: unknown;
  try {
    parsed = JSON.parse(contents);
  } catch {
    return null;
  }

  if (!isObject(parsed)) {
    return null;
  }

  const id = typeof parsed.id === "string" ? parsed.id.trim() : "";
  const projectRoot = typeof parsed.projectRoot === "string" ? parsed.projectRoot.trim() : "";
  const createdAt = toIsoString(parsed.createdAt);
  const updatedAt = toIsoString(parsed.updatedAt);
  const persona = typeof parsed.persona === "string" ? parsed.persona : parsed.persona === null ? null : null;
  const mode = parsed.mode;
  const claudeSessionId =
    typeof parsed.claudeSessionId === "string"
      ? parsed.claudeSessionId
      : parsed.claudeSessionId === null
        ? null
        : null;

  if (!id || !projectRoot || !createdAt || !updatedAt || !isSessionMode(mode)) {
    return null;
  }

  return {
    id,
    createdAt,
    updatedAt,
    projectRoot: path.resolve(projectRoot),
    persona,
    mode,
    claudeSessionId,
  };
}

async function fileExists(targetPath: string): Promise<boolean> {
  try {
    await access(targetPath);
    return true;
  } catch {
    return false;
  }
}

export class SessionNotFoundError extends Error {
  constructor(sessionId: string) {
    super(`Session ${sessionId} was not found.`);
    this.name = "SessionNotFoundError";
  }
}

export class SessionManager {
  private readonly sessionPathById = new Map<string, string>();
  private readonly knownProjectRoots = new Set<string>();

  private sessionsDir(projectRoot: string): string {
    return path.join(path.resolve(projectRoot), ...SESSIONS_DIR_PARTS);
  }

  private sessionFilePath(projectRoot: string, sessionId: string): string {
    return path.join(this.sessionsDir(projectRoot), `${sessionId}.json`);
  }

  private async ensureSessionsDir(projectRoot: string): Promise<void> {
    await mkdir(this.sessionsDir(projectRoot), { recursive: true });
    this.knownProjectRoots.add(path.resolve(projectRoot));
  }

  private rememberSession(session: Session): void {
    const root = path.resolve(session.projectRoot);
    this.knownProjectRoots.add(root);
    this.sessionPathById.set(session.id, this.sessionFilePath(root, session.id));
  }

  private candidateProjectRoots(): string[] {
    const roots = new Set<string>(this.knownProjectRoots);
    roots.add(path.resolve(process.cwd()));
    roots.add(path.resolve(process.cwd(), ".."));
    return Array.from(roots);
  }

  private async loadFromPath(filePath: string): Promise<Session | null> {
    let contents: string;
    try {
      contents = await readFile(filePath, "utf8");
    } catch {
      return null;
    }

    const session = parseSession(contents);
    if (!session) {
      return null;
    }

    this.rememberSession(session);
    return session;
  }

  private async resolveSessionPath(sessionId: string): Promise<string | null> {
    const knownPath = this.sessionPathById.get(sessionId);
    if (knownPath && (await fileExists(knownPath))) {
      return knownPath;
    }

    for (const root of this.candidateProjectRoots()) {
      const candidate = this.sessionFilePath(root, sessionId);
      if (await fileExists(candidate)) {
        this.sessionPathById.set(sessionId, candidate);
        this.knownProjectRoots.add(path.resolve(root));
        return candidate;
      }
    }

    return null;
  }

  async create(projectRoot: string, persona: string | null, mode: SessionMode): Promise<Session> {
    const now = new Date().toISOString();
    const root = path.resolve(projectRoot);

    const session: Session = {
      id: randomUUID(),
      createdAt: now,
      updatedAt: now,
      projectRoot: root,
      persona: persona ?? null,
      mode,
      claudeSessionId: null,
    };

    await this.save(session);
    return session;
  }

  async resume(sessionId: string): Promise<Session> {
    return this.get(sessionId);
  }

  async save(session: Session): Promise<void> {
    const normalized: Session = {
      ...session,
      projectRoot: path.resolve(session.projectRoot),
      updatedAt: toIsoString(session.updatedAt) ?? new Date().toISOString(),
      createdAt: toIsoString(session.createdAt) ?? new Date().toISOString(),
      persona: session.persona ?? null,
      claudeSessionId: session.claudeSessionId ?? null,
    };

    await this.ensureSessionsDir(normalized.projectRoot);

    const filePath = this.sessionFilePath(normalized.projectRoot, normalized.id);
    const tempPath = `${filePath}.tmp-${process.pid}-${Date.now()}`;
    const payload = `${JSON.stringify(normalized, null, 2)}\n`;

    try {
      await writeFile(tempPath, payload, "utf8");
      await rename(tempPath, filePath);
    } catch (error) {
      await rm(tempPath, { force: true }).catch(() => undefined);
      throw error;
    }

    this.rememberSession(normalized);
  }

  async list(projectRoot?: string): Promise<SessionSummary[]> {
    const roots = projectRoot ? [path.resolve(projectRoot)] : this.candidateProjectRoots();
    const summariesById = new Map<string, SessionSummary>();

    for (const root of roots) {
      const sessionsDir = this.sessionsDir(root);
      let entries: Dirent<string>[];
      try {
        entries = await readdir(sessionsDir, { withFileTypes: true, encoding: "utf8" });
      } catch {
        continue;
      }

      for (const entry of entries) {
        if (!entry.isFile() || !entry.name.endsWith(".json")) {
          continue;
        }

        const filePath = path.join(sessionsDir, entry.name);
        const session = await this.loadFromPath(filePath);
        if (!session) {
          continue;
        }

        summariesById.set(session.id, buildSessionSummary(session));
      }
    }

    return Array.from(summariesById.values()).sort((a, b) => {
      return Date.parse(b.updatedAt) - Date.parse(a.updatedAt);
    });
  }

  async get(sessionId: string): Promise<Session> {
    const filePath = await this.resolveSessionPath(sessionId);
    if (!filePath) {
      throw new SessionNotFoundError(sessionId);
    }

    const session = await this.loadFromPath(filePath);
    if (!session) {
      throw new SessionNotFoundError(sessionId);
    }

    return session;
  }

  async delete(sessionId: string): Promise<void> {
    const filePath = await this.resolveSessionPath(sessionId);
    if (!filePath) {
      throw new SessionNotFoundError(sessionId);
    }

    await rm(filePath, { force: false });
    this.sessionPathById.delete(sessionId);
  }
}
