'use client';

import React, { useCallback, useEffect, useState } from 'react';
import {
  DEFAULT_WOVEN_WORKSPACE_THEME,
  WOVEN_WORKSPACE_THEMES,
  WOVEN_WORKSPACE_STORAGE_KEY,
  readWovenWorkspaceStateFromStorage,
  writeWovenWorkspaceThemeToStorage,
  type WovenWorkspaceTheme
} from '../../lib/woven-dialogue/woven-workspace-state';

// A browser session retains its choice even when persistence fails and every
// control unmounts. Weak keys keep server rendering and different windows isolated.
const sessionThemes = new WeakMap<object, WovenWorkspaceTheme>();

function currentSessionTheme(): WovenWorkspaceTheme {
  if (typeof window === 'undefined') return readPersistedTheme();
  const current = sessionThemes.get(window);
  if (current) return current;
  const stored = readPersistedTheme();
  const owner = window;
  sessionThemes.set(owner, stored);
  // This subscription belongs to the browser session, not any control. It must
  // survive closing both Settings and the popover while a Legacy window writes.
  owner.addEventListener?.('storage', (event: StorageEvent) => {
    if (event.key !== WOVEN_WORKSPACE_STORAGE_KEY && event.key !== null) return;
    const storage = browserStorage();
    if (!storage) return;
    // An inaccessible store is not evidence that the in-session choice changed.
    try { storage.getItem(WOVEN_WORKSPACE_STORAGE_KEY); } catch { return; }
    const next = readWovenWorkspaceStateFromStorage(storage).theme;
    sessionThemes.set(owner, next);
    applyTheme(next);
    owner.dispatchEvent?.(new CustomEvent('chirality-theme-change', { detail: next }));
  });
  return stored;
}

const THEME_LABELS: Record<WovenWorkspaceTheme, string> = {
  light: 'Light',
  dark: 'Dark',
  system: 'System'
};

/**
 * Every browser-only global is reached through here so the control renders in
 * a bare node environment (`renderToStaticMarkup`, `react-test-renderer`) with
 * no `window`, `localStorage` or `matchMedia` present. `system` needs no
 * `matchMedia` at all: it is resolved in CSS by `prefers-color-scheme`.
 */
function browserStorage(): Storage | undefined {
  if (typeof window === 'undefined') {
    return undefined;
  }
  try {
    return window.localStorage ?? undefined;
  } catch {
    return undefined;
  }
}

export function readPersistedTheme(): WovenWorkspaceTheme {
  const storage = browserStorage();
  if (!storage) {
    return DEFAULT_WOVEN_WORKSPACE_THEME;
  }
  return readWovenWorkspaceStateFromStorage(storage).theme;
}

export function applyTheme(theme: WovenWorkspaceTheme): void {
  if (typeof document === 'undefined') {
    return;
  }
  document.documentElement.setAttribute('data-theme', theme);
}

/**
 * Light / Dark / System selector for the compact top bar. Light is the rendered
 * and persisted default; the stored choice is read after mount so the server
 * markup stays deterministic, while `layout.tsx` stamps `data-theme` before
 * first paint so there is no flash.
 */
export function ThemeControl(): JSX.Element {
  const [theme, setTheme] = useState<WovenWorkspaceTheme>(
    DEFAULT_WOVEN_WORKSPACE_THEME
  );

  useEffect(() => {
    const stored = currentSessionTheme();
    setTheme(stored);
    applyTheme(stored);
    if (typeof window === 'undefined' || !window.addEventListener) return;
    const sync = (event: Event) => {
      const detail = (event as CustomEvent<WovenWorkspaceTheme>).detail;
      const next = WOVEN_WORKSPACE_THEMES.includes(detail) ? detail : readPersistedTheme();
      sessionThemes.set(window, next);
      setTheme(next);
      applyTheme(next);
    };
    window.addEventListener('chirality-theme-change', sync);
    return () => { window.removeEventListener('chirality-theme-change', sync); };
  }, []);

  const chooseTheme = useCallback((next: WovenWorkspaceTheme): void => {
    if (typeof window !== 'undefined') sessionThemes.set(window, next);
    setTheme(next);
    applyTheme(next);
    const storage = browserStorage();
    if (storage) {
      writeWovenWorkspaceThemeToStorage(storage, next);
    }
    if (typeof window !== 'undefined' && window.dispatchEvent) window.dispatchEvent(new CustomEvent('chirality-theme-change', { detail: next }));
  }, []);

  return (
    <div className="shell-theme" role="group" aria-label="Theme">
      {WOVEN_WORKSPACE_THEMES.map((value) => (
        <button
          key={value}
          type="button"
          className="shell-theme-option"
          data-theme-option={value}
          aria-pressed={theme === value}
          onClick={() => chooseTheme(value)}
        >
          {THEME_LABELS[value]}
        </button>
      ))}
    </div>
  );
}
