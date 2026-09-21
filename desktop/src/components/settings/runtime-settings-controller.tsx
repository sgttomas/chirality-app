'use client';

import { useCallback, useEffect, useState } from 'react';
import { useRuntimeEpoch } from '../shell/runtime-connectivity-provider';

export type RuntimeModel = {
  id: string;
  kind: 'llm' | 'embedding' | 'reranker' | 'helper' | 'unknown';
  loaded: boolean;
  loading: boolean;
  managed?: boolean;
};

export type RuntimeResidencyStatus = {
  phase: 'NO_MODEL' | 'READY' | 'DRAINING' | 'UNLOADING' | 'LOADING';
  managedModelId?: string;
  epoch?: {
    epochId: string;
    modelId: string;
    activatedAt: string;
  };
  activeTurns: number;
  acceptingLocalTurns: boolean;
  models: readonly RuntimeModel[];
};

type RuntimeModelStatusResult =
  | { ok: true; residency: RuntimeResidencyStatus }
  | { ok: false; error: string };

/**
 * Local-model bridge only. The `runtime.daemon` install/start/stop/uninstall
 * operations are retired with the App-owned Runtime service (D-GOV-43): the
 * service is a child process of the App and needs no lifecycle controls.
 */
type ChiralityRuntimeBridge = {
  models?: {
    status: () => Promise<RuntimeModelStatusResult>;
    activate: (modelId: string) => Promise<RuntimeModelStatusResult>;
  };
};

type RuntimeWindow = typeof window & {
  chirality?: {
    runtime?: ChiralityRuntimeBridge;
  };
};

export type RuntimeSettingsViewProps = {
  bridgeAvailable: boolean;
  residency: RuntimeResidencyStatus | null;
  selectedModel: string;
  busyAction: 'status' | 'models' | null;
  error: string | null;
  onRefresh: () => void;
  onSelectedModelChange: (modelId: string) => void;
  onActivateModel: () => void;
};

function getRuntimeBridge(): ChiralityRuntimeBridge | undefined {
  if (typeof window === 'undefined') {
    return undefined;
  }
  return (window as RuntimeWindow).chirality?.runtime;
}

export function useRuntimeSettingsController({ localModels = true }: { localModels?: boolean } = {}): RuntimeSettingsViewProps {
  const [residency, setResidency] = useState<RuntimeResidencyStatus | null>(null);
  const [selectedModel, setSelectedModel] = useState('');
  const [busyAction, setBusyAction] = useState<'status' | 'models' | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [bridgeAvailable, setBridgeAvailable] = useState(false);
  const runtimeEpoch = useRuntimeEpoch();

  const applyResidency = useCallback((next: RuntimeResidencyStatus) => {
    setResidency(next);
    setSelectedModel((current) => {
      if (current && next.models.some((model) => model.id === current)) {
        return current;
      }
      return next.managedModelId ?? next.models.find((model) => model.kind === 'llm')?.id ??
        next.models.find((model) => model.kind === 'unknown')?.id ?? '';
    });
  }, []);

  const refresh = useCallback(async () => {
    const bridge = getRuntimeBridge();
    if (!bridge) {
      setBridgeAvailable(false);
      setResidency(null);
      return;
    }
    setBridgeAvailable(true);
    if (!localModels || !bridge.models) {
      setResidency(null);
      return;
    }
    setBusyAction('status');
    setError(null);
    try {
      const modelResult = await bridge.models.status();
      if (!modelResult.ok) {
        setError(modelResult.error);
        return;
      }
      applyResidency(modelResult.residency);
    } catch {
      setError('Unable to contact the Chirality runtime');
    } finally {
      setBusyAction(null);
    }
  }, [applyResidency, localModels]);

  // Re-probed on reconnect as well as on mount: this panel's content is a claim
  // about the Runtime, and a claim captured while the client was unbound is
  // exactly the one the operator opens it to check after it comes back.
  useEffect(() => {
    void refresh();
  }, [refresh, runtimeEpoch]);

  async function activateModel(): Promise<void> {
    const bridge = getRuntimeBridge();
    if (!bridge?.models || !localModels || !selectedModel) return;
    if (
      !window.confirm(
        `Activate the exact oMLX model “${selectedModel}”? Active local turns will be drained before a model switch.`
      )
    ) {
      return;
    }

    setBusyAction('models');
    setError(null);
    try {
      const result = await bridge.models.activate(selectedModel);
      if (!result.ok) {
        setError(result.error);
        return;
      }
      applyResidency(result.residency);
    } catch {
      setError('Unable to activate the selected oMLX model');
    } finally {
      setBusyAction(null);
    }
  }

  return { bridgeAvailable, residency, selectedModel, busyAction, error,
    onRefresh: () => void refresh(), onSelectedModelChange: setSelectedModel,
    onActivateModel: () => void activateModel() };
}
