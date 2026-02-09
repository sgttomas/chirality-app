import { agentSdkManager } from "./agent-sdk-manager";
import { PersonaManager } from "./persona-manager";
import { SessionManager } from "./session-manager";
import type { PersonaConfig, Session, SessionBootReason, SessionBootResult, TurnOpts, UIEvent } from "./types";

declare global {
  var __chiralityHarnessPersonaManager_v3: PersonaManager | undefined;
  var __chiralityHarnessSessionManager: SessionManager | undefined;
}

export const sessionManager =
  globalThis.__chiralityHarnessSessionManager ?? (globalThis.__chiralityHarnessSessionManager = new SessionManager());

export const personaManager =
  globalThis.__chiralityHarnessPersonaManager_v3 ?? (globalThis.__chiralityHarnessPersonaManager_v3 = new PersonaManager());

export { agentSdkManager };

export type StartHarnessTurnArgs = {
  sessionId: string;
  message: string;
  opts?: TurnOpts;
};

export type EnsureHarnessSessionBootedArgs = {
  sessionId: string;
  force?: boolean;
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

const BOOTSTRAP_TURN_MESSAGE =
  "Initialize this session using your current system and persona instructions. Reply with exactly: BOOTSTRAP_OK";
const BOOTSTRAP_TURN_OPTS: TurnOpts = {
  maxTurns: 1,
  permissionMode: "plan",
  includePartialMessages: false,
};

function markSessionUpdated(session: Session): void {
  session.updatedAt = new Date().toISOString();
}

async function saveSession(session: Session): Promise<void> {
  markSessionUpdated(session);
  await sessionManager.save(session);
}

function mergePersonaTurnDefaults(persona: PersonaConfig | null, opts: TurnOpts | undefined): TurnOpts {
  const merged: TurnOpts = {
    ...(opts ?? {}),
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

function normalizeTurnContext(value: unknown): string | null {
  if (typeof value !== "string") {
    return null;
  }

  const trimmed = value.trim();
  return trimmed ? trimmed : null;
}

function composeSystemPromptAppend(basePrompt: string | null, turnContext: string | null): string | undefined {
  if (basePrompt && turnContext) {
    return `${basePrompt}\n\nTurn-specific context:\n${turnContext}`;
  }

  if (basePrompt) {
    return basePrompt;
  }

  if (turnContext) {
    return `Turn-specific context:\n${turnContext}`;
  }

  return undefined;
}

function isResumeFailure(error: string, usedResume: boolean, sawSessionInit: boolean): boolean {
  if (!usedResume || sawSessionInit) {
    return false;
  }

  const lowered = error.toLowerCase();
  return RESUME_FAILURE_PATTERNS.some((pattern) => lowered.includes(pattern));
}

function classifyBootReason(session: Session, fingerprint: string, force: boolean): SessionBootReason {
  if (force) {
    return "forced";
  }

  if (!session.claudeSessionId) {
    return "missing_claude_session";
  }

  if (!session.bootFingerprint || !session.bootedAt) {
    return "missing_boot_metadata";
  }

  if (session.bootFingerprint !== fingerprint) {
    return "fingerprint_changed";
  }

  return "already_booted";
}

export async function ensureHarnessSessionBooted({
  sessionId,
  force = false,
  opts,
}: EnsureHarnessSessionBootedArgs): Promise<SessionBootResult> {
  const session = await sessionManager.resume(sessionId);
  const persona = session.persona ? await personaManager.load(session.persona) : null;
  const fingerprint = await personaManager.getBootFingerprint(persona, session.mode);
  const reason = classifyBootReason(session, fingerprint, force);
  const previousFingerprint = session.bootFingerprint ?? null;
  const previousClaudeSessionId = session.claudeSessionId ?? null;

  if (reason === "already_booted") {
    return {
      session,
      booted: false,
      reason,
      fingerprint,
      previousFingerprint,
      previousClaudeSessionId,
    };
  }

  if (force && session.claudeSessionId) {
    session.claudeSessionId = null;
    session.bootFingerprint = null;
    session.bootedAt = null;
    await saveSession(session);
  }

  let surfacedBootError: string | null = null;
  const bootTurnOpts: TurnOpts = {
    ...BOOTSTRAP_TURN_OPTS,
    ...(opts ?? {}),
    maxTurns: BOOTSTRAP_TURN_OPTS.maxTurns,
    permissionMode: BOOTSTRAP_TURN_OPTS.permissionMode,
    includePartialMessages: BOOTSTRAP_TURN_OPTS.includePartialMessages,
  };

  for await (const event of startHarnessTurn({
    sessionId,
    message: BOOTSTRAP_TURN_MESSAGE,
    opts: bootTurnOpts,
  })) {
    if (event.type === "session:error") {
      surfacedBootError = event.error;
    }
  }

  if (surfacedBootError) {
    throw new Error(`Session boot failed: ${surfacedBootError}`);
  }

  const updatedSession = await sessionManager.get(sessionId);
  if (!updatedSession.claudeSessionId) {
    throw new Error("Session boot failed: missing claudeSessionId after bootstrap.");
  }

  return {
    session: updatedSession,
    booted: true,
    reason,
    fingerprint,
    previousFingerprint,
    previousClaudeSessionId,
  };
}

export async function* startHarnessTurn({ sessionId, message, opts }: StartHarnessTurnArgs): AsyncIterable<UIEvent> {
  const session = await sessionManager.resume(sessionId);
  const persona = session.persona ? await personaManager.load(session.persona) : null;
  const globalModel = await personaManager.getGlobalModel();
  const bootFingerprint = await personaManager.getBootFingerprint(persona, session.mode);
  const turnContext = normalizeTurnContext(opts?.systemPromptAppend);
  const mergedOpts = mergePersonaTurnDefaults(persona, opts);
  const requestedModel = normalizeModelValue(mergedOpts.model);
  const configuredGlobalModel = normalizeModelValue(globalModel);

  if (requestedModel) {
    mergedOpts.model = requestedModel;
  } else if (configuredGlobalModel) {
    mergedOpts.model = configuredGlobalModel;
  } else {
    delete mergedOpts.model;
  }

  // Reset to a fresh Claude session when model or boot context drift is detected.
  // Boot context drift includes instruction-file changes and legacy sessions
  // that do not yet carry boot metadata.
  const desiredModel = mergedOpts.model;
  const modelChanged = Boolean(session.claudeSessionId && desiredModel && session.model !== desiredModel);
  const bootFingerprintChanged = Boolean(session.claudeSessionId && session.bootFingerprint !== bootFingerprint);
  const missingBootMetadata = Boolean(session.claudeSessionId && (!session.bootFingerprint || !session.bootedAt));

  if (modelChanged || bootFingerprintChanged || missingBootMetadata) {
    session.claudeSessionId = null;
    session.bootFingerprint = null;
    session.bootedAt = null;
    await saveSession(session);
  }

  // Boot-up behavior:
  // - Fresh Claude session (no resume ID): inject full project/persona prompt.
  // - Resumed Claude session: rely on persisted transcript memory and only append
  //   turn-scoped context if the caller provides it.
  const shouldBootstrapPrompt = !session.claudeSessionId;
  const basePrompt = shouldBootstrapPrompt
    ? await personaManager.buildSystemPrompt(session.projectRoot, persona, session.mode)
    : null;
  const systemPromptAppend = composeSystemPromptAppend(basePrompt, turnContext);
  if (systemPromptAppend) {
    mergedOpts.systemPromptAppend = systemPromptAppend;
  } else {
    delete mergedOpts.systemPromptAppend;
  }

  const hadResumeAtStart = Boolean(session.claudeSessionId);
  let attemptedFreshRetry = false;

  while (true) {
    const runSession = attemptedFreshRetry ? { ...session, claudeSessionId: null } : session;
    const bootingFreshSession = !runSession.claudeSessionId;
    let sawSessionInit = false;
    let shouldRetryWithoutResume = false;

    for await (const event of agentSdkManager.startTurn(runSession, message, mergedOpts)) {
      if (event.type === "session:init") {
        sawSessionInit = true;
        session.claudeSessionId = event.claudeSessionId;
        session.model = event.model; // Sync the authoritative model from the CLI init event
        if (bootingFreshSession) {
          session.bootFingerprint = bootFingerprint;
          session.bootedAt = new Date().toISOString();
        }
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
