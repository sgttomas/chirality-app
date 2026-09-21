/**
 * macOS application menu template, extracted from `main.ts` so the structure
 * is unit-testable without an Electron runtime (`Menu` is never imported).
 *
 * The packaged bundle's `app.name` is the package name, so the default appMenu
 * labels would read "Quit chirality-frontend". The product is labelled
 * explicitly without renaming the app (which would move userData).
 */

import type { MenuItemConstructorOptions } from 'electron';

export type ApplicationMenuHandlers = {
  /** "Check for Updates…": run a check and surface the result in the renderer. */
  onCheckForUpdates: () => void;
  /** "About Chirality": ask the focused renderer to show the About dialog. */
  onShowAbout: () => void;
};

export const ABOUT_MENU_LABEL = 'About Chirality';
export const CHECK_FOR_UPDATES_MENU_LABEL = 'Check for Updates…';

export function buildApplicationMenuTemplate(
  handlers: ApplicationMenuHandlers
): MenuItemConstructorOptions[] {
  return [
    { label: 'Chirality', submenu: [
      { label: ABOUT_MENU_LABEL, click: () => handlers.onShowAbout() },
      { label: CHECK_FOR_UPDATES_MENU_LABEL, click: () => handlers.onCheckForUpdates() },
      { type: 'separator' }, { role: 'services' }, { type: 'separator' },
      { role: 'hide', label: 'Hide Chirality' }, { role: 'hideOthers' }, { role: 'unhide' }, { type: 'separator' },
      { role: 'quit', label: 'Quit Chirality' }
    ] },
    { label: 'File', submenu: [
      { label: 'Open Recent', role: 'recentDocuments', submenu: [{ role: 'clearRecentDocuments' }] },
      { type: 'separator' }, { role: 'close' }
    ] },
    { role: 'editMenu' }, { role: 'viewMenu' }, { role: 'windowMenu' }
  ];
}
