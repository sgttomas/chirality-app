import { describe, expect, it, vi } from 'vitest';
import type { MenuItemConstructorOptions } from 'electron';
import {
  ABOUT_MENU_LABEL,
  buildApplicationMenuTemplate,
  CHECK_FOR_UPDATES_MENU_LABEL
} from '../../../electron/application-menu';

/**
 * The template was extracted verbatim from `main.ts`; everything except the
 * About item and the new Check for Updates item must read exactly as before.
 */

function build() {
  const onCheckForUpdates = vi.fn();
  const onShowAbout = vi.fn();
  const template = buildApplicationMenuTemplate({ onCheckForUpdates, onShowAbout });
  return { template, onCheckForUpdates, onShowAbout };
}

const submenuOf = (item: MenuItemConstructorOptions): MenuItemConstructorOptions[] =>
  item.submenu as MenuItemConstructorOptions[];

describe('buildApplicationMenuTemplate', () => {
  it('replaces the native about role with a click item and adds Check for Updates right after it', () => {
    const { template, onCheckForUpdates, onShowAbout } = build();
    const [about, check] = submenuOf(template[0]);
    expect(about.label).toBe(ABOUT_MENU_LABEL);
    expect(about.label).toBe('About Chirality');
    expect(about.role).toBeUndefined();
    expect(check.label).toBe(CHECK_FOR_UPDATES_MENU_LABEL);
    expect(check.label).toBe('Check for Updates…');
    expect(check.role).toBeUndefined();

    (about.click as () => void)();
    expect(onShowAbout).toHaveBeenCalledTimes(1);
    expect(onCheckForUpdates).not.toHaveBeenCalled();
    (check.click as () => void)();
    expect(onCheckForUpdates).toHaveBeenCalledTimes(1);
    expect(onShowAbout).toHaveBeenCalledTimes(1);
  });

  it('keeps every other item exactly as the previous inline template had it', () => {
    const { template } = build();
    expect(template).toHaveLength(5);
    expect(template[0].label).toBe('Chirality');
    expect(submenuOf(template[0]).slice(2)).toEqual([
      { type: 'separator' }, { role: 'services' }, { type: 'separator' },
      { role: 'hide', label: 'Hide Chirality' }, { role: 'hideOthers' }, { role: 'unhide' }, { type: 'separator' },
      { role: 'quit', label: 'Quit Chirality' }
    ]);
    expect(template[1]).toEqual({ label: 'File', submenu: [
      { label: 'Open Recent', role: 'recentDocuments', submenu: [{ role: 'clearRecentDocuments' }] },
      { type: 'separator' }, { role: 'close' }
    ] });
    expect(template.slice(2)).toEqual([{ role: 'editMenu' }, { role: 'viewMenu' }, { role: 'windowMenu' }]);
  });

  it('carries no auto-update, install or restart items', () => {
    const { template } = build();
    const labels = JSON.stringify(template).toLowerCase();
    expect(labels).not.toContain('install');
    expect(labels).not.toContain('restart');
    expect(labels).not.toContain('download');
  });
});
