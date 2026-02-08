import { claudeCodeManager } from "./claude-code-manager";
import { PersonaManager } from "./persona-manager";
import { SessionManager } from "./session-manager";
import type { PersonaConfig, Session, TurnOpts, UIEvent } from "./types";

declare global {
  var __chiralityHarnessPersonaManager_v2: PersonaManager | undefined;
  var __chiralityHarnessSessionManager: SessionManager | undefined;
}

export const sessionManager =
  globalThis.__chiralityHarnessSessionManager ?? (globalThis.__chiralityHarnessSessionManager = new SessionManager());

export const personaManager =
  globalThis.__chiralityHarnessPersonaManager_v2 ?? (globalThis.__chiralityHarnessPersonaManager_v2 = new PersonaManager());

export { claudeCodeManager };

export type StartHarnessTurnArgs = {
  sessionId: string;
  message: string;
  opts?: TurnOpts;
};

const RESUME_FAILURE_PATTERNS = [
  "--resume",
  "resume",
  "session not found",
  "could not find session",
  "invalid session",
  "no such session",
  "exited before a result event",
];

function markSessionUpdated(session: Session): void {
  session.updatedAt = new Date().toISOString();
}

async function saveSession(session: Session): Promise<void> {
  markSessionUpdated(session);
  await sessionManager.save(session);
}

function mergePersonaTurnDefaults(persona: PersonaConfig | null, opts: TurnOpts | undefined, systemPromptFile: string): TurnOpts {
  const merged: TurnOpts = {
    ...(opts ?? {}),
    systemPromptFile,
  };

  if (merged.tools === undefined && persona?.tools) {
    merged.tools = persona.tools;
  }

  if (merged.disallowedTools === undefined && persona?.disallowedTools) {
    merged.disallowedTools = persona.disallowedTools;
  }

  if (merged.autoApproveTools === undefined && persona?.autoApproveTools) {
    merged.autoApproveTools = persona.autoApproveTools;
  }

  if (merged.maxTurns === undefined && typeof persona?.maxTurns === "number") {
    merged.maxTurns = persona.maxTurns;
  }

  return merged;
}

function normalizeModelValue(model: unknown): string | undefined {
  if (typeof model !== "string") {
    return undefined;
  }

  const trimmed = model.trim();
  return trimmed ? trimmed : undefined;
}

function isResumeFailure(error: string, usedResume: boolean, sawSessionInit: boolean): boolean {
  if (!usedResume || sawSessionInit) {
    return false;
  }

  const lowered = error.toLowerCase();
  return RESUME_FAILURE_PATTERNS.some((pattern) => lowered.includes(pattern));
}

export async function* startHarnessTurn({ sessionId, message, opts }: StartHarnessTurnArgs): AsyncIterable<UIEvent> {
  const session = await sessionManager.resume(sessionId);
  const persona = session.persona ? await personaManager.load(session.projectRoot, session.persona) : null;
  const globalModel = await personaManager.getGlobalModel(session.projectRoot);
  const basePrompt = await personaManager.buildSystemPrompt(session.projectRoot, persona, session.mode);
  const systemPrompt = opts?.systemPromptAppend
    ? `${basePrompt}\n\nTurn-specific context:\n${opts.systemPromptAppend}`
    : basePrompt;
  const systemPromptFile = await personaManager.writeSystemPromptFile(session.projectRoot, session.id, systemPrompt);
  const mergedOpts = mergePersonaTurnDefaults(persona, opts, systemPromptFile);
  const requestedModel = normalizeModelValue(mergedOpts.model);
  const configuredGlobalModel = normalizeModelValue(globalModel);

  if (requestedModel) {
    mergedOpts.model = requestedModel;
  } else if (configuredGlobalModel) {
    mergedOpts.model = configuredGlobalModel;
  } else {
    delete mergedOpts.model;
  }

  // Detect model change: if the desired model differs from the session's active model,
  // we must start a fresh Claude session to ensure the model change takes effect.
  // We also reset if session.model is unknown (legacy session) to guarantee compliance.
  const desiredModel = mergedOpts.model;
  if (session.claudeSessionId && desiredModel && session.model !== desiredModel) {
    session.claudeSessionId = null;
    await saveSession(session);
  }

  const hadResumeAtStart = Boolean(session.claudeSessionId);
  let attemptedFreshRetry = false;

  while (true) {
    const runSession = attemptedFreshRetry ? { ...session, claudeSessionId: null } : session;
    let sawSessionInit = false;
    let shouldRetryWithoutResume = false;

    for await (const event of claudeCodeManager.startTurn(runSession, message, mergedOpts)) {
      if (event.type === "session:init") {
        sawSessionInit = true;
        session.claudeSessionId = event.claudeSessionId;
        session.model = event.model; // Sync the authoritative model from the CLI init event
        await saveSession(session);
      }

      if (event.type === "session:complete") {
        await saveSession(session);
      }

      if (
        event.type === "session:error" &&
        !attemptedFreshRetry &&
        hadResumeAtStart &&
        isResumeFailure(event.error, true, sawSessionInit)
      ) {
        shouldRetryWithoutResume = true;
      }

      if (event.type === "process:exit") {
        await saveSession(session);
        if (!attemptedFreshRetry && hadResumeAtStart && shouldRetryWithoutResume) {
          continue;
        }
      }

      yield event;
    }

    if (!attemptedFreshRetry && hadResumeAtStart && shouldRetryWithoutResume) {
      attemptedFreshRetry = true;
      continue;
    }

    break;
  }
}
