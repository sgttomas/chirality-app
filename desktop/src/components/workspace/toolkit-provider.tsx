'use client';

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode
} from 'react';
import type { HarnessOpts } from '@chirality/runtime-contracts/types';
import {
  buildHarnessOptsFromToolkit,
  createToolkitPreset,
  defaultToolkitState,
  defaultToolkitValues,
  sanitizeToolkitState,
  TOOLKIT_STORAGE_KEY,
  upsertToolkitPreset,
  type ToolkitPreset,
  type ToolkitValues
} from '../../lib/harness/toolkit';

type ToolkitContextValue = {
  hydrated: boolean;
  isToolkitVisible: boolean;
  setToolkitVisible: (visible: boolean) => void;
  storageWarning: string | null;
  dismissStorageWarning: () => void;
  values: ToolkitValues;
  updateValues: (patch: Partial<ToolkitValues>) => void;
  resetValues: () => void;
  optsPayload: HarnessOpts | undefined;
  presets: ToolkitPreset[];
  selectedPresetId: string | null;
  selectPreset: (presetId: string) => void;
  applySelectedPreset: () => void;
  savePreset: (name: string) => boolean;
  deleteSelectedPreset: () => void;
};

const ToolkitContext = createContext<ToolkitContextValue | null>(null);

const STORAGE_WARNING_UNAVAILABLE =
  'Toolkit local storage is unavailable. Settings will stay in memory for this session only.';
const STORAGE_WARNING_CORRUPT =
  'Toolkit local storage data was invalid and has been reset to defaults.';

export function ToolkitProvider({ children }: { children: ReactNode }): JSX.Element {
  const [state, setState] = useState(defaultToolkitState());
  const [hydrated, setHydrated] = useState(false);
  const [storageWritable, setStorageWritable] = useState(true);
  const [storageWarning, setStorageWarning] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }

    try {
      const raw = window.localStorage.getItem(TOOLKIT_STORAGE_KEY);
      if (raw) {
        try {
          setState(sanitizeToolkitState(JSON.parse(raw)));
        } catch {
          setState(defaultToolkitState());
          setStorageWarning(STORAGE_WARNING_CORRUPT);
          window.localStorage.removeItem(TOOLKIT_STORAGE_KEY);
        }
      }
    } catch {
      setState(defaultToolkitState());
      setStorageWritable(false);
      setStorageWarning(STORAGE_WARNING_UNAVAILABLE);
    } finally {
      setHydrated(true);
    }
  }, []);

  useEffect(() => {
    if (!hydrated || !storageWritable || typeof window === 'undefined') {
      return;
    }

    try {
      window.localStorage.setItem(TOOLKIT_STORAGE_KEY, JSON.stringify(state));
    } catch {
      setStorageWritable(false);
      setStorageWarning((existing) => existing ?? STORAGE_WARNING_UNAVAILABLE);
    }
  }, [state, hydrated, storageWritable]);

  const optsPayload = useMemo(() => buildHarnessOptsFromToolkit(state.values), [state.values]);

  useEffect(() => {
    if (!hydrated) {
      return;
    }
    const payload = optsPayload ? JSON.stringify(optsPayload) : '(empty)';
    console.info(`[toolkit] opts changed: ${payload}`);
  }, [optsPayload, hydrated]);

  const setToolkitVisible = useCallback((visible: boolean) => {
    console.debug(`[toolkit] visibility=${visible} t=${new Date().toISOString()}`);
    setState((existing) => ({
      ...existing,
      visible
    }));
  }, []);

  const dismissStorageWarning = useCallback(() => {
    setStorageWarning(null);
  }, []);

  const updateValues = useCallback((patch: Partial<ToolkitValues>) => {
    const fields = Object.keys(patch).join(',');
    console.debug(`[toolkit] updateValues fields=${fields} t=${new Date().toISOString()}`);
    setState((existing) => ({
      ...existing,
      values: {
        ...existing.values,
        ...patch
      }
    }));
  }, []);

  const resetValues = useCallback(() => {
    console.debug(`[toolkit] resetValues t=${new Date().toISOString()}`);
    setState((existing) => ({
      ...existing,
      values: defaultToolkitValues()
    }));
  }, []);

  const selectPreset = useCallback((presetId: string) => {
    setState((existing) => ({
      ...existing,
      selectedPresetId: presetId || null
    }));
  }, []);

  const applySelectedPreset = useCallback(() => {
    setState((existing) => {
      if (!existing.selectedPresetId) {
        return existing;
      }

      const selected = existing.presets.find((preset) => preset.id === existing.selectedPresetId);
      if (!selected) {
        return {
          ...existing,
          selectedPresetId: null
        };
      }

      console.debug(`[toolkit] applyPreset name=${selected.name} id=${selected.id} t=${new Date().toISOString()}`);
      return {
        ...existing,
        values: selected.values
      };
    });
  }, []);

  const savePreset = useCallback((name: string): boolean => {
    const normalizedName = name.trim();
    if (!normalizedName) {
      return false;
    }

    const nextPreset = createToolkitPreset(normalizedName, state.values);
    console.debug(`[toolkit] savePreset name=${normalizedName} id=${nextPreset.id} t=${new Date().toISOString()}`);
    setState((existing) => ({
      ...existing,
      presets: upsertToolkitPreset(existing.presets, nextPreset),
      selectedPresetId: nextPreset.id
    }));
    return true;
  }, [state.values]);

  const deleteSelectedPreset = useCallback(() => {
    setState((existing) => {
      if (!existing.selectedPresetId) {
        return existing;
      }

      const deleted = existing.presets.find((preset) => preset.id === existing.selectedPresetId);
      console.debug(`[toolkit] deletePreset name=${deleted?.name ?? 'unknown'} id=${existing.selectedPresetId} t=${new Date().toISOString()}`);
      return {
        ...existing,
        presets: existing.presets.filter((preset) => preset.id !== existing.selectedPresetId),
        selectedPresetId: null
      };
    });
  }, []);

  const value = useMemo<ToolkitContextValue>(
    () => ({
      hydrated,
      isToolkitVisible: state.visible,
      setToolkitVisible,
      storageWarning,
      dismissStorageWarning,
      values: state.values,
      updateValues,
      resetValues,
      optsPayload,
      presets: state.presets,
      selectedPresetId: state.selectedPresetId,
      selectPreset,
      applySelectedPreset,
      savePreset,
      deleteSelectedPreset
    }),
    [
      hydrated,
      state.visible,
      storageWarning,
      state.values,
      state.presets,
      state.selectedPresetId,
      setToolkitVisible,
      dismissStorageWarning,
      updateValues,
      resetValues,
      optsPayload,
      selectPreset,
      applySelectedPreset,
      savePreset,
      deleteSelectedPreset
    ]
  );

  return <ToolkitContext.Provider value={value}>{children}</ToolkitContext.Provider>;
}

export function useToolkit(): ToolkitContextValue {
  const value = useContext(ToolkitContext);
  if (!value) {
    throw new Error('useToolkit must be used inside ToolkitProvider');
  }
  return value;
}
