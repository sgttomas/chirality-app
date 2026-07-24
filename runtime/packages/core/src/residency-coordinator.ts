import { randomUUID } from "node:crypto";
import { join } from "node:path";
import {
  RuntimeError,
  type OmlxControlPort,
  type OmlxModelStatus,
  type ResidencyEvidence,
  type ResidencyStatus
} from "@chirality/runtime-contracts";
import { appendJsonLine, atomicWriteJson, readJsonIfExists } from "./fs.js";

interface PersistedResidency {
  schemaVersion: "chirality.residency-state/v1";
  managedModelId?: string;
  epoch?: ResidencyStatus["epoch"];
}

export interface ResidencyCoordinatorOptions {
  drainTimeoutMs?: number;
  totalTimeoutMs?: number;
  pollIntervalMs?: number;
}

export class ResidencyCoordinator {
  private phase: ResidencyStatus["phase"] = "NO_MODEL";
  private managedModelId?: string;
  private epoch?: ResidencyStatus["epoch"];
  private activeTurns = 0;
  private transitioning = false;
  private initialized = false;
  private readonly waiters = new Set<() => void>();
  private readonly drainTimeoutMs: number;
  private readonly totalTimeoutMs: number;
  private readonly pollIntervalMs: number;
  private readonly stateFile: string;
  private readonly evidenceFile: string;

  constructor(
    private readonly control: OmlxControlPort,
    runtimeDirectory: string,
    options: ResidencyCoordinatorOptions = {}
  ) {
    this.drainTimeoutMs = options.drainTimeoutMs ?? 10 * 60_000;
    this.totalTimeoutMs = options.totalTimeoutMs ?? 20 * 60_000;
    this.pollIntervalMs = options.pollIntervalMs ?? 1_000;
    this.stateFile = join(runtimeDirectory, "model-residency.json");
    this.evidenceFile = join(runtimeDirectory, "model-residency.jsonl");
  }

  async status(): Promise<ResidencyStatus> {
    await this.initialize();
    const models = await this.control.listStatus();
    if (!this.transitioning) {
      await this.reconcile(models);
    }
    return {
      phase: this.phase,
      activeTurns: this.activeTurns,
      acceptingLocalTurns: this.phase === "READY" && !this.transitioning,
      models,
      ...(this.managedModelId === undefined ? {} : { managedModelId: this.managedModelId }),
      ...(this.epoch === undefined ? {} : { epoch: this.epoch })
    };
  }

  async admitTurn(modelId: string): Promise<() => void> {
    await this.initialize();
    if (!this.transitioning) {
      await this.reconcile(await this.control.listStatus());
    }
    if (this.transitioning || this.phase !== "READY") {
      throw new RuntimeError(
        "RESIDENCY_TRANSITION_IN_PROGRESS",
        "Local turns are not being admitted during model transition",
        409
      );
    }
    if (this.managedModelId !== modelId) {
      throw new RuntimeError(
        "MODEL_NOT_RESIDENT",
        `Exact local model is not resident: ${modelId}`,
        409
      );
    }
    this.activeTurns += 1;
    let released = false;
    return () => {
      if (released) return;
      released = true;
      this.activeTurns -= 1;
      if (this.activeTurns === 0) {
        for (const wake of this.waiters) wake();
        this.waiters.clear();
      }
    };
  }

  async activate(modelId: string, approvalReference: string): Promise<ResidencyStatus> {
    await this.initialize();
    if (modelId.trim() === "" || approvalReference.trim() === "") {
      throw new RuntimeError(
        "INVALID_REQUEST",
        "Model activation requires an exact model ID and non-empty approvalReference"
      );
    }
    if (this.transitioning) {
      throw new RuntimeError(
        "RESIDENCY_TRANSITION_IN_PROGRESS",
        "A model transition is already in progress",
        409
      );
    }
    await this.reconcile(await this.control.listStatus());
    this.transitioning = true;
    const transitionId = randomUUID();
    const previous = this.managedModelId;
    const startedAt = Date.now();
    await this.evidence({
      schemaVersion: "chirality.model-residency/v1",
      timestamp: new Date().toISOString(),
      transitionId,
      targetModelId: modelId,
      outcome: "started",
      approvalReference,
      ...(previous === undefined ? {} : { fromModelId: previous })
    });
    let unloadAttempted = false;
    try {
      const models = await this.control.listStatus();
      const target = models.find((model) => model.id === modelId);
      if (target === undefined || target.kind !== "llm") {
        throw new RuntimeError("MODEL_UNAVAILABLE", `Unknown exact oMLX LLM model: ${modelId}`, 404);
      }
      const conflicting = models.filter(
        (model) => model.kind === "llm" && model.loaded && model.id !== modelId
      );
      if (
        conflicting.some(
          (model) => model.id !== previous || (model.managed !== true && model.id !== previous)
        )
      ) {
        throw new RuntimeError(
          "RESIDENCY_UNMANAGED_CONFLICT",
          "An unmanaged local LLM prevents a safe activation",
          409,
          { loadedModelIds: conflicting.map((model) => model.id) }
        );
      }
      if (previous === modelId && target.loaded) {
        this.phase = "READY";
        return await this.completeActivation(modelId, transitionId, approvalReference, previous);
      }
      this.phase = "DRAINING";
      const drained = await this.waitForDrain(startedAt + this.drainTimeoutMs);
      if (!drained) {
        this.phase = previous === undefined ? "NO_MODEL" : "READY";
        throw new RuntimeError(
          "RESIDENCY_DRAIN_TIMEOUT",
          "Active local turns did not drain before the deadline",
          409
        );
      }
      if (previous !== undefined && previous !== modelId) {
        this.phase = "UNLOADING";
        // Once an unload request is transmitted its outcome can be ambiguous
        // (for example, oMLX may unload and the response may be lost). Clear
        // ownership before transmission so every such failure is fail-closed.
        unloadAttempted = true;
        this.managedModelId = undefined;
        this.epoch = undefined;
        await this.persist();
        await this.control.unload(previous, this.deadlineSignal(startedAt + this.totalTimeoutMs));
      }
      const refreshed = await this.control.listStatus(
        this.deadlineSignal(startedAt + this.totalTimeoutMs)
      );
      const refreshedTarget = refreshed.find((model) => model.id === modelId);
      if (refreshedTarget?.loaded !== true) {
        this.phase = "LOADING";
        await this.control.load(modelId, this.deadlineSignal(startedAt + this.totalTimeoutMs));
      }
      await this.waitUntilLoaded(modelId, startedAt + this.totalTimeoutMs);
      this.phase = "READY";
      return await this.completeActivation(modelId, transitionId, approvalReference, previous);
    } catch (error) {
      if (unloadAttempted) {
        this.phase = "NO_MODEL";
        this.managedModelId = undefined;
        this.epoch = undefined;
        await this.persist();
      } else {
        this.phase = previous === undefined ? "NO_MODEL" : "READY";
      }
      await this.evidence({
        schemaVersion: "chirality.model-residency/v1",
        timestamp: new Date().toISOString(),
        transitionId,
        targetModelId: modelId,
        outcome:
          error instanceof RuntimeError && error.code === "RESIDENCY_DRAIN_TIMEOUT"
            ? "aborted"
            : "failed",
        reason: error instanceof Error ? error.message : "Unknown transition failure",
        approvalReference,
        ...(previous === undefined ? {} : { fromModelId: previous })
      });
      throw error;
    } finally {
      this.transitioning = false;
    }
  }

  private async completeActivation(
    modelId: string,
    transitionId: string,
    approvalReference: string,
    previous?: string
  ): Promise<ResidencyStatus> {
    this.managedModelId = modelId;
    this.epoch = {
      epochId: randomUUID(),
      modelId,
      activatedAt: new Date().toISOString()
    };
    await this.persist();
    await this.evidence({
      schemaVersion: "chirality.model-residency/v1",
      timestamp: new Date().toISOString(),
      transitionId,
      targetModelId: modelId,
      outcome: "completed",
      epochId: this.epoch.epochId,
      approvalReference,
      ...(previous === undefined ? {} : { fromModelId: previous })
    });
    // `activate()` clears the transition flag in its outer `finally`. The
    // returned snapshot describes the post-return state, so do not leak the
    // transient false value that `status()` observes while this method is
    // still on the activation stack.
    return {
      ...(await this.status()),
      acceptingLocalTurns: true
    };
  }

  private async initialize(): Promise<void> {
    if (this.initialized) return;
    const state = await readJsonIfExists<PersistedResidency>(this.stateFile, {
      schemaVersion: "chirality.residency-state/v1"
    });
    this.managedModelId = state.managedModelId;
    this.epoch = state.epoch;
    if (this.managedModelId !== undefined) {
      const models = await this.control.listStatus();
      const current = models.find((model) => model.id === this.managedModelId);
      if (current?.loaded === true) {
        this.phase = "READY";
      } else {
        this.managedModelId = undefined;
        this.epoch = undefined;
        this.phase = "NO_MODEL";
        await this.persist();
      }
    }
    this.initialized = true;
  }

  private async reconcile(models: readonly OmlxModelStatus[]): Promise<void> {
    if (this.managedModelId === undefined) return;
    const managedModelId = this.managedModelId;
    const managed = models.find((model) => model.id === managedModelId);
    const conflictingLlm = models.some(
      (model) => model.kind === "llm" && model.id !== managedModelId && model.loaded
    );
    if (
      managed?.kind === "llm" &&
      managed.loaded === true &&
      managed.loading !== true &&
      !conflictingLlm
    ) {
      this.phase = "READY";
      return;
    }
    this.managedModelId = undefined;
    this.epoch = undefined;
    this.phase = "NO_MODEL";
    await this.persist();
    await this.evidence({
      schemaVersion: "chirality.model-residency/v1",
      timestamp: new Date().toISOString(),
      transitionId: randomUUID(),
      fromModelId: managedModelId,
      targetModelId: managedModelId,
      outcome: "failed",
      reason: conflictingLlm
        ? "External residency drift introduced another loaded LLM"
        : "Managed model is no longer loaded and ready",
      approvalReference: "runtime-residency-reconciliation"
    });
  }

  private async waitForDrain(deadline: number): Promise<boolean> {
    while (this.activeTurns > 0) {
      const remaining = deadline - Date.now();
      if (remaining <= 0) return false;
      await new Promise<void>((resolve) => {
        const timer = setTimeout(() => {
          this.waiters.delete(wake);
          resolve();
        }, Math.min(remaining, this.pollIntervalMs));
        const wake = (): void => {
          clearTimeout(timer);
          resolve();
        };
        this.waiters.add(wake);
      });
    }
    return true;
  }

  private async waitUntilLoaded(modelId: string, deadline: number): Promise<void> {
    while (Date.now() < deadline) {
      const models = await this.control.listStatus(this.deadlineSignal(deadline));
      const target = models.find((model) => model.id === modelId);
      if (target?.loaded === true && target.loading !== true) return;
      await new Promise((resolve) => setTimeout(resolve, this.pollIntervalMs));
    }
    throw new RuntimeError("OMLX_UNAVAILABLE", "Timed out waiting for oMLX model readiness", 504);
  }

  private deadlineSignal(deadline: number): AbortSignal {
    return AbortSignal.timeout(Math.max(1, deadline - Date.now()));
  }

  private persist(): Promise<void> {
    const state: PersistedResidency = {
      schemaVersion: "chirality.residency-state/v1",
      ...(this.managedModelId === undefined ? {} : { managedModelId: this.managedModelId }),
      ...(this.epoch === undefined ? {} : { epoch: this.epoch })
    };
    return atomicWriteJson(this.stateFile, state);
  }

  private evidence(value: ResidencyEvidence): Promise<void> {
    return appendJsonLine(this.evidenceFile, value);
  }
}
