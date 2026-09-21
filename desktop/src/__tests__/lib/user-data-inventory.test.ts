import { describe, expect, it } from 'vitest';
import {
  rendererUserDataPreserved,
  snapshotRendererUserData,
  UPDATE_PATH_DESCRIPTION,
  UPDATE_PRESERVATION_NOTE,
  UPDATE_RUNNING_WORK_NOTE,
  USER_DATA_INVENTORY
} from '../../lib/shell/user-data-inventory';
import { CHAT_DRAFT_STORAGE_PREFIX } from '../../lib/harness/chat-draft';
import { PLAN_EXECUTION_STORAGE_PREFIX } from '../../lib/harness/plan-executions';
import { WOVEN_WORKSPACE_STORAGE_KEY } from '../../lib/woven-dialogue/woven-workspace-state';

function storageOf(entries: Record<string, string>) {
  const keys = Object.keys(entries);
  return { length: keys.length, key: (index: number) => keys[index] ?? null, getItem: (key: string) => entries[key] ?? null };
}

describe('user data inventory', () => {
  it('names every kind of user work the update path must preserve, each with an observable check', () => {
    expect(USER_DATA_INVENTORY.map(entry => entry.id)).toEqual([
      'chats', 'drafts', 'chat-folders', 'chat-settings', 'plan-executions', 'project-workflows', 'personal-workflows', 'preferences', 'sign-in'
    ]);
    for (const entry of USER_DATA_INVENTORY) {
      expect(entry.observable.length).toBeGreaterThan(20);
      expect(entry.location).not.toMatch(/\/Users\//);
    }
  });

  it('keeps its renderer-storage prefixes aligned with the modules that write them', () => {
    const prefixes = new Set(USER_DATA_INVENTORY.filter(entry => entry.store === 'renderer-storage').map(entry => entry.keyPrefix));
    expect(prefixes.has(`${CHAT_DRAFT_STORAGE_PREFIX}:`)).toBe(true);
    expect(prefixes.has(`${PLAN_EXECUTION_STORAGE_PREFIX}:`)).toBe(true);
    expect(prefixes.has(WOVEN_WORKSPACE_STORAGE_KEY)).toBe(true);
  });

  it('snapshots renderer storage by key and length only, and compares two snapshots', () => {
    const before = snapshotRendererUserData(storageOf({
      [`${CHAT_DRAFT_STORAGE_PREFIX}:/a:session:1:CHAT`]: '{"text":"draft"}',
      [`${PLAN_EXECUTION_STORAGE_PREFIX}:1`]: '[]',
      [WOVEN_WORKSPACE_STORAGE_KEY]: '{}',
      'chirality.projectRoot': '/a',
      unrelated: 'x'
    }), () => new Date('2026-09-12T20:00:00Z'));
    expect(before.takenAt).toBe('2026-09-12T20:00:00.000Z');
    expect(before.counts[`${CHAT_DRAFT_STORAGE_PREFIX}:`]).toBe(1);
    expect(before.counts[`${PLAN_EXECUTION_STORAGE_PREFIX}:`]).toBe(1);
    expect(before.counts['chirality.']).toBe(4);
    expect(before.digest).not.toContain('draft');
    expect(before.digest).not.toContain('unrelated');

    const same = snapshotRendererUserData(storageOf({
      unrelated: 'y',
      'chirality.projectRoot': '/a',
      [WOVEN_WORKSPACE_STORAGE_KEY]: '{}',
      [`${PLAN_EXECUTION_STORAGE_PREFIX}:1`]: '[]',
      [`${CHAT_DRAFT_STORAGE_PREFIX}:/a:session:1:CHAT`]: '{"text":"other"}'
    }));
    expect(rendererUserDataPreserved(before, same)).toBe(true);
    const lost = snapshotRendererUserData(storageOf({ 'chirality.projectRoot': '/a' }));
    expect(rendererUserDataPreserved(before, lost)).toBe(false);
  });

  it('describes the update path as a manual install and never as an applied update', () => {
    expect(UPDATE_PATH_DESCRIPTION).toContain('opens the installer in your browser');
    expect(UPDATE_PATH_DESCRIPTION).toContain('does not install updates');
    expect(UPDATE_PATH_DESCRIPTION).not.toMatch(/updated|has been installed|installs automatically/i);
    expect(UPDATE_PRESERVATION_NOTE).toContain('kept');
    expect(UPDATE_RUNNING_WORK_NOTE).toContain('Quitting Chirality to install stops it');
  });
});
