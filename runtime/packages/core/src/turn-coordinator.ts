import { randomUUID } from "node:crypto";
import {
  RuntimeError,
  asHarnessError,
  type AgentEngineRunInput,
  type HarnessEvent,
  type IAttachmentResolver,
  type SessionTurnRequest,
  type UIEvent
} from "@chirality/runtime-contracts";
import type { EngineRegistry } from "./engine-registry.js";
import type { ProjectRegistry } from "./project-registry.js";
import type { ResidencyCoordinator } from "./residency-coordinator.js";
import type { SessionStore } from "./session-store.js";

interface ActiveTurn {
  controller: AbortController;
  engineInterrupt: () => Promise<void>;
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
    case "ENGINE_UNAVAILABLE":
    case "CONTEXT_EXHAUSTED":
    case "SDK_FAILURE":
      return new RuntimeError("ENGINE_UNAVAILABLE", harness.message, harness.status);
  }
}

export class TurnCoordinator {
  private readonly active = new Map<string, ActiveTurn>();

  constructor(
    private readonly projects: ProjectRegistry,
    private readonly sessions: SessionStore,
    private readonly engines: EngineRegistry,
    private readonly residency: ResidencyCoordinator,
    private readonly attachments?: IAttachmentResolver
  ) {}

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
    let releaseResidency = (): void => undefined;
    this.active.set(key, {
      controller,
      engineInterrupt: () => engine.interrupt(sessionId)
    });
    let processExit: Extract<UIEvent, { type: "process:exit" }> | undefined;
    let turnErrorSeen = false;
    let terminalHarnessEvent: HarnessEvent | undefined;
    let terminalPersisted = false;
    let sessionInitSeen = false;
    let engineEventIndex = 0;
    try {
      releaseResidency = local
        ? await this.residency.admitTurn(session.engineSelection.model)
        : () => undefined;
      const input: AgentEngineRunInput = {
        session,
        message,
        opts: {
          model: request.opts?.model ?? session.engineSelection.model,
          tools: request.opts?.tools ?? [...toolNames],
          maxTurns: request.opts?.maxTurns ?? 50,
          persona: request.opts?.persona ?? session.persona,
          mode: request.opts?.mode ?? session.mode,
          ...(request.opts?.subagentGovernance === undefined
            ? {}
            : { subagentGovernance: request.opts.subagentGovernance })
        },
        turnId,
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
                    request.attachments
                  )
                ).contentBlocks
              })
      };
      const accepted = await this.sessions.appendEvent(projectId, {
        sessionId,
        turnId,
        type: "turn.accepted",
        data: { message }
      });
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
            (local && received.data.model !== session.engineSelection.model)
          ) {
            throw new RuntimeError(
              "INTERNAL_FAILURE",
              "Engine initialization attribution does not match the selected adapter",
              502
            );
          }
          const residencyStatus = local ? await this.residency.status() : undefined;
          session = {
            ...session,
            engineSessionId: received.data.engineSessionId,
            engineSelection: {
              adapterId: received.data.adapterId,
              providerId: received.data.providerId,
              model: received.data.model
            },
            adapterSession: {
              ...(session.adapterSession ?? {}),
              engineSessionId: received.data.engineSessionId
            },
            ...(received.data.claudeSessionId === undefined
              ? {}
              : { claudeSessionId: received.data.claudeSessionId }),
            ...(residencyStatus?.epoch === undefined
              ? {}
              : { residencyEpoch: residencyStatus.epoch.epochId })
          };
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
          data: {}
        });
        terminalHarnessEvent = completed;
        terminalPersisted = true;
        yield { type: "harness:event", data: completed };
      } else {
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
      yield processExit;
      await this.sessions.update({
        ...session,
        status: controller.signal.aborted
          ? "interrupted"
          : terminalHarnessEvent.type === "turn.completed"
            ? "completed"
            : "failed"
      });
    } catch (error) {
      const runtimeError = normalizeEngineFailure(error, local);
      if (!terminalPersisted) {
        const failed = await this.sessions.appendEvent(projectId, {
          sessionId,
          turnId,
          type: controller.signal.aborted ? "turn.interrupted" : "turn.failed",
          data: { code: runtimeError.code, message: runtimeError.message }
        });
        yield { type: "harness:event", data: failed };
      }
      if (!turnErrorSeen) {
        yield {
          type: "turn:error",
          data: {
            phase: "mid-stream",
            errorType: "SDK_FAILURE",
            message: runtimeError.message,
            status: runtimeError.status,
            severity: "error",
            fatal: true,
            details: { runtimeCode: runtimeError.code }
          }
        };
      }
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
      await this.sessions.update({
        ...session,
        status: controller.signal.aborted ? "interrupted" : "failed"
      });
    } finally {
      this.active.delete(key);
      releaseResidency();
    }
  }

  async interrupt(projectId: string, sessionId: string): Promise<void> {
    const active = this.active.get(`${projectId}\0${sessionId}`);
    if (active === undefined) return;
    active.controller.abort();
    await active.engineInterrupt();
  }
}
