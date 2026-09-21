import { randomUUID } from 'node:crypto';
import { asHarnessError, HarnessError } from '@chirality/runtime-contracts/errors';
import { resolveRuntimeOptions } from './options';
import { evaluateSubagentGovernance } from './subagent-governance';
import { resolveHarnessToolPool } from './tool-pool';
import { appendHarnessEvent } from './session-events';
import { createHarnessEvent } from './event-factory';
import type { AgentEnginePort, AgentEngineRunInput } from '@chirality/runtime-contracts/agent-engine-port';
import type { ResolvedEngine } from './engine-registry';
import {
  AttachmentError,
  AttachmentFailureDetails,
  ContentBlock,
  HarnessOpts,
  IAttachmentResolver,
  IPersonaManager,
  ISessionManager,
  ResolvedOpts,
  SessionRecord,
  TurnErrorSeverity,
  TurnRequest,
  UIEvent
} from '@chirality/runtime-contracts/types';

const MAX_ATTACHMENT_WARNING_DETAILS = 3;
export type RunningHarnessTurn = {
  sessionId: string;
  events: AsyncIterable<UIEvent>;
  cancel(): Promise<void>;
};

type TurnEngineRunInput = {
  sessionId: string;
  message: string;
  opts?: HarnessOpts;
  attachments: string[];
};

type SubagentGovernanceEvaluator = typeof evaluateSubagentGovernance;
type RuntimeOptionsResolver = typeof resolveRuntimeOptions;

export type TurnEngineDependencies = {
  sessionManager: ISessionManager;
  personaManager: IPersonaManager;
  attachmentResolver: IAttachmentResolver;
  resolveEngine: (session: SessionRecord, opts: ResolvedOpts) => ResolvedEngine | Promise<ResolvedEngine>;
  resolveRuntimeOptions?: RuntimeOptionsResolver;
  evaluateSubagentGovernance?: SubagentGovernanceEvaluator;
};

type StreamTurnInput = {
  session: SessionRecord;
  engine: ResolvedEngine;
  message: string;
  opts: ResolvedOpts;
  contentBlocks?: ContentBlock[];
  releaseTurnLock: () => void;
  turnId: string;
};

function requireNonEmptyString(value: unknown, field: string): string {
  if (typeof value !== 'string' || value.trim().length === 0) {
    throw new HarnessError('INVALID_REQUEST', 400, `Missing or invalid '${field}'`);
  }

  return value.trim();
}

function requireStringArray(value: unknown, field: string): string[] {
  if (!Array.isArray(value) || value.some((item) => typeof item !== 'string')) {
    throw new HarnessError('INVALID_REQUEST', 400, `Field '${field}' must be an array of strings`);
  }

  return value;
}

function parseTurnRequest(value: unknown): TurnEngineRunInput {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Request body must be a JSON object');
  }

  const record = value as Record<string, unknown>;
  const sessionId = requireNonEmptyString(record.sessionId, 'sessionId');
  if (typeof record.message !== 'string') {
    throw new HarnessError('INVALID_REQUEST', 400, "Missing or invalid 'message'");
  }

  return {
    sessionId,
    message: record.message,
    opts: record.opts as HarnessOpts | undefined,
    attachments:
      record.attachments === undefined ? [] : requireStringArray(record.attachments, 'attachments')
  };
}

function basenameLike(rawPath: string): string {
  const segments = rawPath.split(/[\\/]/).filter((segment) => segment.length > 0);
  if (segments.length === 0) {
    return rawPath;
  }
  return segments[segments.length - 1];
}

function buildAttachmentWarningText(errors: AttachmentError[]): string | undefined {
  if (errors.length === 0) {
    return undefined;
  }

  const lines = errors
    .slice(0, MAX_ATTACHMENT_WARNING_DETAILS)
    .map((error) => `- ${basenameLike(error.path)}: ${error.reason}`);
  const remaining = errors.length - lines.length;
  if (remaining > 0) {
    lines.push(`- ... ${remaining} additional attachment error(s) omitted`);
  }

  return [
    `Attachment warning: ${errors.length} attachment(s) could not be processed. Continuing with available content.`,
    'Rejected attachments:',
    ...lines
  ].join('\n');
}

function classifyStreamErrorSeverity(status: number): TurnErrorSeverity {
  return status >= 500 ? 'error' : 'warning';
}

function buildAttachmentFailureDetails(errors: AttachmentError[]): AttachmentFailureDetails {
  return {
    category: 'ALL_ATTACHMENTS_FAILED_NO_TEXT',
    attachmentErrors: errors,
    rejectedAttachmentCount: errors.length
  };
}

function assertKnownAgentSdkTools(sessionId: string, opts: ResolvedOpts): void {
  const toolPool = resolveHarnessToolPool({
    sessionId,
    requestedTools: opts.tools,
    mode: opts.mode
  });

  if (toolPool.unknownTools.length === 0) {
    return;
  }

  const toolNames = toolPool.unknownTools.map((issue) => issue.toolName).join(', ');
  throw new HarnessError('INVALID_REQUEST', 400, `Unknown harness tool(s): ${toolNames}`, {
    category: 'UNKNOWN_TOOLS',
    unknownTools: toolPool.unknownTools
  });
}

export class TurnEngine {
  private readonly activeSessionTurns = new Set<string>();
  private readonly activeSessionEngines = new Map<string, AgentEnginePort>();
  private readonly resolveRuntimeOptions: RuntimeOptionsResolver;
  private readonly evaluateSubagentGovernance: SubagentGovernanceEvaluator;

  constructor(private readonly dependencies: TurnEngineDependencies) {
    this.resolveRuntimeOptions = dependencies.resolveRuntimeOptions ?? resolveRuntimeOptions;
    this.evaluateSubagentGovernance =
      dependencies.evaluateSubagentGovernance ?? evaluateSubagentGovernance;
  }

  async runTurn(request: TurnRequest | unknown): Promise<RunningHarnessTurn> {
    const input = parseTurnRequest(request);
    const session = await this.dependencies.sessionManager.resume(input.sessionId);

    if (this.activeSessionTurns.has(input.sessionId)) {
      throw new HarnessError(
        'TURN_IN_PROGRESS',
        409,
        'A turn is already in progress for this session',
        { sessionId: input.sessionId }
      );
    }

    this.activeSessionTurns.add(input.sessionId);
    let released = false;
    let cancellationPersisted = false;
    const releaseTurnLock = (): void => {
      if (released) {
        return;
      }
      released = true;
      this.activeSessionTurns.delete(input.sessionId);
    };

    try {
      let resolvedOpts = await this.resolveRuntimeOptions(session, input.opts);
      const engine = await this.dependencies.resolveEngine(session, resolvedOpts);
      if (engine.selection.model && engine.selection.model !== resolvedOpts.model) {
        resolvedOpts = { ...resolvedOpts, model: engine.selection.model };
      }
      if (engine.port.descriptor.capabilities.tools) {
        assertKnownAgentSdkTools(input.sessionId, resolvedOpts);
      }

      const attachmentResolution =
        await this.dependencies.attachmentResolver.resolveAttachmentsToContentBlocks(
          input.message,
          input.attachments
        );

      const warningText = buildAttachmentWarningText(attachmentResolution.errors);
      const contentBlocks: ContentBlock[] = warningText
        ? [{ type: 'text', text: warningText }, ...attachmentResolution.contentBlocks]
        : attachmentResolution.contentBlocks;
      const text = input.message.trim();
      const hasExecutableAttachment = attachmentResolution.contentBlocks.some(
        (block) => block.type === 'file'
      );

      if (!text && !hasExecutableAttachment) {
        throw new HarnessError(
          'ATTACHMENT_FAILURE',
          400,
          'Turn requires text content or at least one valid attachment',
          buildAttachmentFailureDetails(attachmentResolution.errors)
        );
      }

      await this.dependencies.personaManager.buildSystemPrompt(
        session.projectRoot,
        resolvedOpts.persona,
        resolvedOpts.mode,
        resolvedOpts.tools
      );

      const governanceDecision = await this.evaluateSubagentGovernance(
        resolvedOpts.persona,
        resolvedOpts.subagentGovernance
      );
      const effectiveOpts = governanceDecision.allowed
        ? {
            ...resolvedOpts,
            delegatedSubagents: governanceDecision.delegatedSubagents,
            delegatedAgentInstructions: governanceDecision.delegatedAgentInstructions
          }
        : {
            ...resolvedOpts,
            delegatedSubagents: [],
            delegatedAgentInstructions: {}
          };
      const turnMessage =
        !hasExecutableAttachment && warningText
          ? [warningText, input.message].filter((part) => part.trim().length > 0).join('\n\n')
          : input.message;
      const turnContentBlocks = hasExecutableAttachment ? contentBlocks : undefined;
      const turnId = `turn_${randomUUID()}`;
      const engineInput: AgentEngineRunInput = {
        session,
        message: turnMessage,
        opts: effectiveOpts,
        contentBlocks: turnContentBlocks,
        turnId
      };

      // Acceptance belongs to the route-independent lifecycle boundary. Persist the
      // raw user-authored text before provider preflight or iteration starts so replay
      // can recover an accepted message even when discovery/authentication fails before
      // a prompt is transmitted. appendHarnessEvent applies configured-key redaction.
      await appendHarnessEvent(
        createHarnessEvent({
          sessionId: input.sessionId,
          turnId,
          type: 'message.accepted',
          data: {
            turnId,
            role: 'user',
            text: input.message
          }
        })
      );

      try {
        await engine.port.preflight(engineInput);
      } catch (error) {
        const failure = asHarnessError(error);
        await appendHarnessEvent(
          createHarnessEvent({
            sessionId: input.sessionId,
            turnId,
            type: 'turn.failed',
            data: {
              turnId,
              adapterId: engine.selection.adapterId,
              providerId: engine.selection.providerId,
              model: engine.selection.model,
              errorType: failure.type,
              status: failure.status,
              message: failure.message,
              phase: 'preflight'
            }
          })
        );
        throw failure;
      }
      this.activeSessionEngines.set(input.sessionId, engine.port);

      return {
        sessionId: input.sessionId,
        events: this.streamTurn({
          session,
          engine,
          message: turnMessage,
          opts: effectiveOpts,
          contentBlocks: turnContentBlocks,
          releaseTurnLock,
          turnId
        }),
        cancel: async (): Promise<void> => {
          if (cancellationPersisted) {
            releaseTurnLock();
            return;
          }
          cancellationPersisted = true;
          try {
            // A transport disconnect is not an explicit user interrupt (D-APP-40).
            // Persist its own terminal outcome before best-effort provider shutdown.
            await appendHarnessEvent(
              createHarnessEvent({
                sessionId: input.sessionId,
                turnId,
                type: 'turn.cancelled',
                data: {
                  turnId,
                  reason: 'client_disconnect'
                }
              })
            );
            await (engine.port as AgentEnginePort & {
              cancel?(sessionId: string): Promise<void>;
            }).cancel?.(input.sessionId);
          } catch {
            // Stream cancellation is best-effort; the route still needs the lock released.
          } finally {
            this.activeSessionEngines.delete(input.sessionId);
            releaseTurnLock();
          }
        }
      };
    } catch (error) {
      this.activeSessionEngines.delete(input.sessionId);
      releaseTurnLock();
      throw error;
    }
  }

  async interrupt(sessionId: string): Promise<void> {
    const activeEngine = this.activeSessionEngines.get(sessionId);
    if (activeEngine) {
      await activeEngine.interrupt(sessionId);
      return;
    }
    throw new HarnessError('SESSION_NOT_FOUND', 404, `No active turn for session '${sessionId}'`, {
      sessionId
    });
  }

  private async *streamTurn(input: StreamTurnInput): AsyncIterable<UIEvent> {
    try {
      for await (const event of input.engine.port.startTurn({
        session: input.session,
        message: input.message,
        opts: input.opts,
        contentBlocks: input.contentBlocks,
        turnId: input.turnId
      })) {
        if (event.type === 'session:init') {
          const engineSessionId = event.data.engineSessionId;
          const isClaude = event.data.providerId === 'anthropic';
          await this.dependencies.sessionManager.save(input.session.sessionId, {
            engineSessionId,
            engineSelection: {
              adapterId: event.data.adapterId,
              providerId: event.data.providerId,
              model: event.data.model
            },
            adapterSession: {
              ...input.session.adapterSession,
              engineSessionId,
              packageName: input.engine.port.descriptor.packageName,
              packageVersion: input.engine.port.descriptor.packageVersion
            },
            ...(isClaude ? { claudeSessionId: event.data.claudeSessionId } : {}),
            model: event.data.model,
            ...(event.data.adapterId === 'claude-agent-sdk'
              ? {
                  sdkSessionId: engineSessionId,
                  sdkPackageVersion: input.engine.port.descriptor.packageVersion
                }
              : {})
          });
        }

        yield event;
      }
    } catch (error) {
      const harnessError = asHarnessError(error);
      const severity = classifyStreamErrorSeverity(harnessError.status);
      yield {
        type: 'turn:error',
        data: {
          phase: 'mid-stream',
          errorType: harnessError.type,
          message: harnessError.message,
          status: harnessError.status,
          severity,
          fatal: true,
          details: harnessError.details
        }
      };
      yield {
        type: 'process:exit',
        data: {
          exitCode: 1,
          interrupted: false,
          error: harnessError.message,
          errorType: harnessError.type,
          status: harnessError.status,
          severity,
          fatal: true,
          errorDetails: harnessError.details
        }
      };
    } finally {
      this.activeSessionEngines.delete(input.session.sessionId);
      input.releaseTurnLock();
    }
  }
}
