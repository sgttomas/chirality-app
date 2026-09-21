import { randomUUID } from "node:crypto";
import { describeFailureDetails } from "./retirement-failure.js";
import {
  HOSTED_MODEL_ID_PATTERN,
  HOSTED_REASONING_EFFORT_PATTERN,
  RuntimeError,
  asHarnessError,
  type AgentEngineRunInput,
  type HarnessEvent,
  type IAttachmentResolver,
  type PreparedContextSuccessor,
  type SessionTurnRequest,
  type UIEvent
} from "@chirality/runtime-contracts";
import type { EngineRegistry } from "./engine-registry.js";
import type { ProjectRegistry } from "./project-registry.js";
import type { ResidencyCoordinator } from "./residency-coordinator.js";
import type { SessionStore } from "./session-store.js";
import type { RuntimeMethodService } from "./runtime-method-service.js";

interface ActiveTurn {
  controller: AbortController;
  engineInterrupt: () => Promise<void>;
  /** Caller-supplied reason recorded on the synthesized `turn.interrupted` terminal (for example `service-shutdown`). */
  reason?: string;
}

/** Per-turn override validation: absent means "use the session's value"; anything else must be a well-formed identifier. */
function validateTurnOverride(value: unknown, pattern: RegExp, field: "model" | "reasoningEffort"): string | undefined {
  if (value === undefined) return undefined;
  if (typeof value !== "string" || !pattern.test(value)) {
    throw new RuntimeError("INVALID_REQUEST", `Turn ${field} override is malformed`, 400, { reason: field === "model" ? "TURN_MODEL_INVALID" : "TURN_REASONING_EFFORT_INVALID" });
  }
  return value;
}

export interface RequiredToolReceipt {
  toolName: string;
  completed(): boolean;
}

const HARNESS_TERMINAL_TYPES = new Set([
  "turn.completed",
  "turn.failed",
  "turn.cancelled",
  "turn.interrupted"
]);

function normalizeEngineFailure(error: unknown, local: boolean): RuntimeError {
  if (error instanceof RuntimeError) return error;
  const harness = asHarnessError(error);
  switch (harness.type) {
    case "INVALID_REQUEST":
    case "PERSONA_NOT_FOUND":
    case "INSTRUCTION_ROOT_INVALID":
    case "WORKING_ROOT_INACCESSIBLE":
    case "WORKING_ROOT_CONFLICT":
    case "ATTACHMENT_FAILURE":
      return new RuntimeError("INVALID_REQUEST", harness.message, harness.status);
    case "TURN_IN_PROGRESS":
      return new RuntimeError("SESSION_TURN_IN_PROGRESS", harness.message, harness.status);
    case "SESSION_NOT_FOUND":
      return new RuntimeError("SESSION_NOT_FOUND", harness.message, harness.status);
    case "MODEL_UNAVAILABLE":
      return new RuntimeError("MODEL_UNAVAILABLE", harness.message, harness.status);
    case "MISSING_API_KEY":
    case "PROVIDER_AUTH_FAILURE":
      return new RuntimeError(
        local ? "OMLX_AUTHENTICATION_FAILED" : "ENGINE_UNAVAILABLE",
        harness.message,
        harness.status
      );
    case "PROVIDER_PROTOCOL_FAILURE":
      return new RuntimeError(
        local ? "OMLX_PROTOCOL_FAILURE" : "INTERNAL_FAILURE",
        harness.message,
        harness.status
      );
    case "INSTRUCTION_ADOPTION_PENDING":
      return new RuntimeError("INSTRUCTION_ADOPTION_PENDING", harness.message, harness.status);
    case "ENGINE_UNAVAILABLE":
    case "CONTEXT_EXHAUSTED":
    case "SDK_FAILURE":
      return new RuntimeError("ENGINE_UNAVAILABLE", harness.message, harness.status);
  }
}

export class TurnCoordinator {
  private readonly active = new Map<string, ActiveTurn>();
  private runtimeMethods?: RuntimeMethodService;

  constructor(
    private readonly projects: ProjectRegistry,
    private readonly sessions: SessionStore,
    private readonly engines: EngineRegistry,
    private readonly residency: ResidencyCoordinator,
    private readonly attachments?: IAttachmentResolver
  ) {}

  configureRuntimeMethods(methods: RuntimeMethodService): void {
    this.runtimeMethods = methods;
  }

  async *run(
    projectId: string,
    sessionId: string,
    request: SessionTurnRequest,
    toolNames: readonly string[] = [],
    requiredToolReceipts: readonly RequiredToolReceipt[] = []
  ): AsyncIterable<UIEvent> {
    await this.projects.requireAuthorized(projectId);
    let session = await this.sessions.get(projectId, sessionId);
    const key = `${projectId}\0${sessionId}`;
    if (this.active.has(key)) {
      throw new RuntimeError("SESSION_TURN_IN_PROGRESS", "Session already has an active turn", 409);
    }
    const engine = this.engines.resolve(session.engineSelection);
    const controller = new AbortController();
    const turnId = request.turnId ?? randomUUID();
    const message = request.message ?? request.prompt;
    if (message === undefined || message.trim() === "") {
      throw new RuntimeError("INVALID_REQUEST", "Turn message cannot be empty");
    }
    const local = session.engineSelection.providerId === "omlx";
    const modelOverride = validateTurnOverride(request.model, HOSTED_MODEL_ID_PATTERN, "model");
    const effortOverride = validateTurnOverride(request.reasoningEffort, HOSTED_REASONING_EFFORT_PATTERN, "reasoningEffort");
    const turnModel = modelOverride ?? request.opts?.model ?? session.engineSelection.model;
    const turnEffort = effortOverride ?? session.reasoningEffort;
    let releaseResidency = (): void => undefined;
    const activeTurn: ActiveTurn = {
      controller,
      engineInterrupt: () => engine.interrupt(sessionId)
    };
    this.active.set(key, activeTurn);
    let processExit: Extract<UIEvent, { type: "process:exit" }> | undefined;
    let turnErrorSeen = false;
    let terminalHarnessEvent: HarnessEvent | undefined;
    let terminalPersisted = false;
    let sessionInitSeen = false;
    let engineEventIndex = 0;
    let acceptedOwned = false;
    const contextSuccessor: PreparedContextSuccessor | undefined = session.adapterSession?.contextSuccessor;
    let successorRecorded = false;
    try {
      releaseResidency = local
        ? await this.residency.admitTurn(session.engineSelection.model)
        : () => undefined;
      const resolvedContext = this.runtimeMethods === undefined || session.schemaVersion !== "chirality.session/v3" ? undefined : await this.runtimeMethods.resolveForTurn(projectId, session, {
        interactionMode: request.interactionMode,
        permissionMode: request.permissionMode,
        methods: request.methods,
        workflow: request.workflow,
        taskSkill: request.taskSkill
      });
      if ((request.interactionMode ?? session.interactionMode) === "native-plan") {
        if (this.runtimeMethods === undefined) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan runtime is unavailable", 503);
        const capability = await this.runtimeMethods.getNativePlanCapability(projectId, sessionId);
        if (capability.status === "unavailable") throw new RuntimeError("ENGINE_UNAVAILABLE", capability.reason, 503);
      }
      const requestedTools = request.opts?.tools ?? [...toolNames];
      const admittedTools = resolvedContext === undefined ? requestedTools : await this.runtimeMethods!.restrictRequestedTools(
        projectId,
        resolvedContext.response.roleId,
        request.permissionMode ?? session.permissionMode,
        resolvedContext.response.methods,
        requestedTools
      );
      const input: AgentEngineRunInput = {
        projectId,
        // The engine sees the effective per-turn selection; the stored session keeps its default engine selection.
        session: modelOverride === undefined && effortOverride === undefined ? session : {
          ...session,
          engineSelection: { ...session.engineSelection, model: turnModel },
          ...(turnEffort === undefined ? {} : { reasoningEffort: turnEffort })
        },
        message,
        interactionMode: request.interactionMode ?? session.interactionMode ?? "chat",
        ...(turnEffort === undefined ? {} : { reasoningEffort: turnEffort }),
        opts: {
          model: turnModel,
          tools: admittedTools,
          maxTurns: request.opts?.maxTurns ?? 50,
          persona: request.opts?.persona ?? session.persona,
          mode: request.permissionMode ?? session.permissionMode ?? request.opts?.mode ?? session.mode,
          ...(request.opts?.subagentGovernance === undefined
            ? {}
            : { subagentGovernance: request.opts.subagentGovernance })
        },
        turnId,
        ...(contextSuccessor === undefined ? {} : { contextSuccessor }),
        ...(resolvedContext === undefined ? {} : {
          instructionContext: resolvedContext.response,
          runtimeTools: await this.runtimeMethods!.restrictRuntimeTools(
            projectId,
            resolvedContext.response.roleId,
            request.permissionMode ?? session.permissionMode,
            resolvedContext.response.methods,
            this.runtimeMethods!.runtimeTools(projectId, sessionId, turnId, admittedTools).filter(tool => tool.permission.operation !== "control" || engine.descriptor.capabilities.runtimeControlTools === true)
          )
        }),
        ...(request.attachments === undefined || request.attachments.length === 0
          ? {}
          : this.attachments === undefined
            ? (() => {
                throw new RuntimeError(
                  "INVALID_REQUEST",
                  "Attachment resolver is unavailable",
                  503
                );
              })()
            : {
                contentBlocks: (
                  await this.attachments.resolveAttachmentsToContentBlocks(
                    message,
                    request.attachments,
                    { projectId, sessionId, projectRoot: session.projectRoot }
                  )
                ).contentBlocks
              })
      };
      const acceptedData = {
        message,
        ...(request.attachments?.length ? { attachments: [...request.attachments] } : {}),
        ...(modelOverride === undefined ? {} : { model: modelOverride }),
        ...(effortOverride === undefined ? {} : { reasoningEffort: effortOverride })
      };
      const accepted = resolvedContext === undefined
        ? await this.sessions.appendEvent(projectId, { sessionId, turnId, type: "turn.accepted", data: acceptedData })
        : (await this.sessions.commitWithAcceptedTurn(session, { sessionId, turnId, type: "turn.accepted", data: acceptedData }, resolvedContext.snapshot)).event;
      acceptedOwned = true;
      yield { type: "harness:event", data: accepted };
      await engine.preflight(input);
      await this.sessions.update({ ...session, status: "running" });
      for await (const received of engine.startTurn(input)) {
        if (processExit !== undefined) {
          throw new RuntimeError(
            "INTERNAL_FAILURE",
            "Engine emitted an event after process:exit",
            502
          );
        }
        if (engineEventIndex === 0 && received.type !== "session:init") {
          throw new RuntimeError(
            "INTERNAL_FAILURE",
            "Engine must emit session:init first",
            502
          );
        }
        if (received.type === "process:exit") {
          processExit = received;
          continue;
        }
        if (received.type === "turn:error" && received.data.fatal) {
          turnErrorSeen = true;
        }
        if (received.type === "harness:event") {
          if (
            received.data.sessionId !== sessionId ||
            (received.data.turnId !== undefined && received.data.turnId !== turnId)
          ) {
            throw new RuntimeError(
              "INTERNAL_FAILURE",
              "Engine emitted an event outside the active session or turn",
              502
            );
          }
          if (HARNESS_TERMINAL_TYPES.has(received.data.type)) {
            if (terminalHarnessEvent !== undefined) {
              throw new RuntimeError(
                "INTERNAL_FAILURE",
                "Engine emitted multiple terminal harness events",
                500
              );
            }
            if (received.data.type === "turn.completed") {
              const missing = requiredToolReceipts
                .filter((receipt) => !receipt.completed())
                .map((receipt) => receipt.toolName);
              if (missing.length > 0) {
                throw new RuntimeError(
                  "REQUIRED_DELEGATION_MISSING",
                  `Required tool evidence is missing: ${missing.join(", ")}`,
                  422
                );
              }
            }
            terminalHarnessEvent = received.data;
            continue;
          }
          await this.sessions.persistEvent(projectId, received.data);
        }
        if (received.type === "chat:delta" && received.data.text) {
          await this.sessions.appendEvent(projectId, { sessionId, turnId, type: "message.delta", data: { text: received.data.text } });
        }
        if (received.type === "session:init") {
          if (sessionInitSeen || engineEventIndex !== 0) {
            throw new RuntimeError(
              "INTERNAL_FAILURE",
              "Engine emitted multiple or out-of-order session:init events",
              502
            );
          }
          if (
            received.data.adapterId !== engine.descriptor.adapterId ||
            received.data.providerId !== engine.descriptor.providerId ||
            (local && received.data.model !== turnModel)
          ) {
            throw new RuntimeError(
              "INTERNAL_FAILURE",
              "Engine initialization attribution does not match the selected adapter",
              502
            );
          }
          const residencyStatus = local ? await this.residency.status() : undefined;
          if (contextSuccessor !== undefined) {
            await this.sessions.recordProviderSpanSessionInit(projectId, sessionId, contextSuccessor.preparationId, { sessionInitEventId: randomUUID(), engineSessionId: received.data.engineSessionId, providerSpanId: received.data.providerSpanId ?? received.data.engineSessionId });
            successorRecorded = true;
          }
          const adapterSession = { ...(session.adapterSession ?? {}), engineSessionId: received.data.engineSessionId, ...(received.data.lastRuntimeTurnId === undefined ? {} : { lastRuntimeTurnId: received.data.lastRuntimeTurnId }) };
          delete adapterSession.contextSuccessor;
          session = {
            ...session,
            status: "running",
            engineSessionId: received.data.engineSessionId,
            engineSelection: {
              adapterId: received.data.adapterId,
              providerId: received.data.providerId,
              // A per-turn model override never rewrites the session's default selection.
              model: modelOverride === undefined ? received.data.model : session.engineSelection.model
            },
            adapterSession,
            ...(received.data.claudeSessionId === undefined
              ? {}
              : { claudeSessionId: received.data.claudeSessionId }),
            ...(residencyStatus?.epoch === undefined
              ? {}
              : { residencyEpoch: residencyStatus.epoch.epochId })
          };
          if (contextSuccessor !== undefined) {
            delete session.sdkSessionId;
            delete session.sdkTranscriptPath;
            delete session.sdkSessionStoreKey;
            if (received.data.claudeSessionId === undefined) delete session.claudeSessionId;
          }
          await this.sessions.update(session);
          sessionInitSeen = true;
        }
        yield received;
        engineEventIndex += 1;
      }
      if (!sessionInitSeen) {
        throw new RuntimeError(
          "INTERNAL_FAILURE",
          "Engine stream ended without session:init",
          502
        );
      }
      if (processExit === undefined) {
        throw new RuntimeError(
          "INTERNAL_FAILURE",
          "Engine stream ended without process:exit",
          502
        );
      }
      if (terminalHarnessEvent === undefined) {
        const missing = requiredToolReceipts
          .filter((receipt) => !receipt.completed())
          .map((receipt) => receipt.toolName);
        if (missing.length > 0) {
          throw new RuntimeError(
            "REQUIRED_DELEGATION_MISSING",
            `Required tool evidence is missing: ${missing.join(", ")}`,
            422
          );
        }
      }
      if (processExit.data.exitCode !== 0) {
        if (terminalHarnessEvent === undefined) {
          throw new RuntimeError(
            "ENGINE_UNAVAILABLE",
            processExit.data.error ?? "Engine exited without terminal failure evidence",
            processExit.data.status ?? 502
          );
        }
        if (terminalHarnessEvent.type === "turn.completed") {
          throw new RuntimeError(
            "INTERNAL_FAILURE",
            "Engine emitted turn.completed with a nonzero process exit",
            502
          );
        }
      }
      if (terminalHarnessEvent === undefined) {
        const completed = await this.sessions.appendEvent(projectId, {
          sessionId,
          turnId,
          type: controller.signal.aborted ? "turn.interrupted" : "turn.completed",
          data: controller.signal.aborted && activeTurn.reason !== undefined ? { reason: activeTurn.reason } : {}
        });
        terminalHarnessEvent = completed;
        terminalPersisted = true;
        yield { type: "harness:event", data: completed };
      } else {
        // The supplier reports that it stopped; the Runtime owns why it asked
        // for interruption. Preserve supplier details while recording that
        // cause on the same terminal before both persistence and publication.
        if (terminalHarnessEvent.type === "turn.interrupted" && controller.signal.aborted && activeTurn.reason !== undefined) {
          terminalHarnessEvent = { ...terminalHarnessEvent, data: { ...terminalHarnessEvent.data, reason: activeTurn.reason } };
        }
        await this.sessions.persistEvent(projectId, terminalHarnessEvent);
        terminalPersisted = true;
        yield { type: "harness:event", data: terminalHarnessEvent };
      }
      if (processExit.data.exitCode === 0 && terminalHarnessEvent.type !== "turn.completed") {
        throw new RuntimeError(
          "INTERNAL_FAILURE",
          "Engine emitted a successful process exit with a non-success terminal event",
          502
        );
      }
      await this.sessions.update(withLastUsed({
        ...session,
        status: controller.signal.aborted
          ? "interrupted"
          : terminalHarnessEvent.type === "turn.completed"
            ? "completed"
            : "failed"
      }, turnModel, turnEffort));
      await this.runtimeMethods?.applyPendingMethodChanges(projectId, sessionId, turnId);
      yield processExit;
    } catch (error) {
      const runtimeError = normalizeEngineFailure(error, local);
      if (contextSuccessor !== undefined && !successorRecorded) {
        const currentSuccessor = (await this.sessions.get(projectId, sessionId).catch(() => undefined))?.adapterSession?.contextSuccessor;
        if (currentSuccessor?.preparationId === contextSuccessor.preparationId) {
          await engine.cancelContextSuccessor?.(contextSuccessor.preparationId).catch(() => undefined);
          await this.sessions.failProviderSpanPreparation(projectId, sessionId, contextSuccessor.preparationId, { code: runtimeError.code, message: runtimeError.message }).catch(() => undefined);
        }
      }
      if (!terminalPersisted) {
        const failureDetails = controller.signal.aborted ? undefined : describeFailureDetails(error);
        const failed = await this.sessions.appendEvent(projectId, {
          sessionId,
          turnId,
          type: controller.signal.aborted ? "turn.interrupted" : "turn.failed",
          data: { code: runtimeError.code, message: runtimeError.message, ...(failureDetails ? { details: failureDetails } : {}), ...(controller.signal.aborted && activeTurn.reason !== undefined ? { reason: activeTurn.reason } : {}) }
        });
        yield { type: "harness:event", data: failed };
      }
      if (!turnErrorSeen) {
        yield {
          type: "turn:error",
          data: {
            phase: "mid-stream",
            errorType: runtimeError.code === "INSTRUCTION_ADOPTION_PENDING" ? "INSTRUCTION_ADOPTION_PENDING" : "SDK_FAILURE",
            message: runtimeError.message,
            status: runtimeError.status,
            severity: "error",
            fatal: true,
            // A machine reason (e.g. MODEL_NOT_IN_CATALOG) lets clients map the failure without parsing text.
            details: { runtimeCode: runtimeError.code, ...(typeof runtimeError.details?.reason === "string" ? { reason: runtimeError.details.reason } : {}) }
          }
        };
      }
      if (acceptedOwned) await this.sessions.update(withLastUsed({
        ...session,
        status: controller.signal.aborted ? "interrupted" : "failed"
      }, turnModel, turnEffort));
      if (acceptedOwned) await this.runtimeMethods?.applyPendingMethodChanges(projectId, sessionId, turnId);
      yield {
        type: "process:exit",
        data: {
          exitCode:
            processExit !== undefined && processExit.data.exitCode !== 0
              ? processExit.data.exitCode
              : controller.signal.aborted
                ? 130
                : 1,
          interrupted: controller.signal.aborted,
          error: runtimeError.message,
          errorType: runtimeError.code,
          status: runtimeError.status,
          severity: "error",
          fatal: true
        }
      };
    } finally {
      this.active.delete(key);
      releaseResidency();
    }
  }

  /** Whether this coordinator currently owns an active turn for the session. */
  isActive(projectId: string, sessionId: string): boolean {
    return this.active.has(`${projectId}\0${sessionId}`);
  }

  async interrupt(projectId: string, sessionId: string, reason?: string): Promise<void> {
    const active = this.active.get(`${projectId}\0${sessionId}`);
    if (active === undefined) return;
    if (reason !== undefined && active.reason === undefined) active.reason = reason;
    active.controller.abort();
    await active.engineInterrupt();
  }
}

/** Records the model and effort the turn actually ran with; the session's default selection is untouched. */
function withLastUsed<T extends { lastUsedModel?: string; lastUsedReasoningEffort?: string }>(record: T, model: string, reasoningEffort: string | undefined): T {
  const updated = { ...record, lastUsedModel: model };
  if (reasoningEffort === undefined) delete updated.lastUsedReasoningEffort;
  else updated.lastUsedReasoningEffort = reasoningEffort;
  return updated;
}
