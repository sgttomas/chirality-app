/**
 * What the user keeps across an application update, and where it lives.
 *
 * Chirality never installs an update itself: Check for Updates… reports a
 * newer version and Download opens the installer in the browser; the user
 * quits Chirality, installs the downloaded build, and reopens it. Everything
 * below is stored outside the application bundle, so replacing the bundle
 * leaves it in place. The inventory is the basis of the update acceptance
 * checks: each entry names the storage, the key prefix a renderer check can
 * count, and the observable that proves it survived.
 *
 * Pure and DOM-free so the acceptance test and the About wording share it.
 */

export type UserDataStore =
  /** Renderer web storage under the App's userData profile (Electron partition). */
  | 'renderer-storage'
  /** The App-owned Runtime service's data under userData/runtime. */
  | 'runtime-data'
  /** Inside the selected project folder. */
  | 'project-folder'
  /** The user's home directory, shared with other Codex clients. */
  | 'user-home';

export type UserDataInventoryEntry = {
  id: 'chats' | 'drafts' | 'chat-folders' | 'chat-settings' | 'plan-executions' | 'project-workflows' | 'personal-workflows' | 'preferences' | 'sign-in';
  label: string;
  store: UserDataStore;
  /** Where the data sits, in the user's terms (no private paths). */
  location: string;
  /** Storage key or key prefix, for stores a renderer check can enumerate. */
  keyPrefix?: string;
  /** What a person checks after reopening the updated application. */
  observable: string;
};

export const USER_DATA_INVENTORY: readonly UserDataInventoryEntry[] = Object.freeze([
  {
    id: 'chats',
    label: 'Chats and their history',
    store: 'runtime-data',
    location: 'Runtime data folder, per project, under the application profile',
    observable: 'Every chat listed before the update is listed after it, with its full transcript when opened.'
  },
  {
    id: 'drafts',
    label: 'Unsent drafts and attachments',
    store: 'renderer-storage',
    location: 'Application profile web storage',
    keyPrefix: 'chirality.chatDraft.v1:',
    observable: 'A draft typed before quitting is back in the composer of the same chat, with its attachments and selected workflows.'
  },
  {
    id: 'chat-folders',
    label: 'Per-chat folder bindings',
    store: 'renderer-storage',
    location: 'Application profile web storage',
    keyPrefix: 'chirality.wovenWorkspace.v1',
    observable: 'Each chat still opens in the folder it was created in; the navigator groups them by folder as before.'
  },
  {
    id: 'chat-settings',
    label: 'Per-chat model, reasoning, role and permission settings',
    store: 'renderer-storage',
    location: 'Application profile web storage, with the chat record in the Runtime',
    keyPrefix: 'chirality.chatDraft.v1:',
    observable: 'Reopening a chat restores its own selections; the new-chat defaults are unchanged.'
  },
  {
    id: 'plan-executions',
    label: 'Plan revision execution records',
    store: 'renderer-storage',
    location: 'Application profile web storage',
    keyPrefix: 'chirality.planExecutions.v1:',
    observable: 'An executed plan revision still reads as executed, with its attempts, rather than as awaiting first execution.'
  },
  {
    id: 'project-workflows',
    label: 'Saved project workflows',
    store: 'project-folder',
    location: '.chirality/workflows inside the project folder',
    observable: 'Project Specific workflows are listed unchanged in the Workflows tab.'
  },
  {
    id: 'personal-workflows',
    label: 'Saved personal workflows',
    store: 'user-home',
    location: '.chirality/workflows in the home folder',
    observable: 'Personal workflows are listed unchanged in the Workflows tab.'
  },
  {
    id: 'preferences',
    label: 'Application preferences',
    store: 'renderer-storage',
    location: 'Application profile web storage',
    keyPrefix: 'chirality.',
    observable: 'Appearance, layout, pinned and grouped chats, and the folder for new chats are as they were.'
  },
  {
    id: 'sign-in',
    label: 'Codex sign-in',
    store: 'user-home',
    location: 'Codex home, custodied by Codex',
    observable: 'The account row reads Signed in without a new sign-in ceremony.'
  }
]);

export type RendererUserDataSnapshot = {
  takenAt: string;
  /** Number of storage keys under each renderer-storage prefix. */
  counts: Record<string, number>;
  /** Digest of every renderer-storage key and value length, in key order. */
  digest: string;
};

type StorageLike = { length: number; key: (index: number) => string | null; getItem: (key: string) => string | null };

/**
 * A comparable picture of the renderer-storage half of the inventory. Two
 * snapshots taken before quitting and after reopening the updated build must
 * match for the renderer half to count as preserved. Values are never copied
 * out; only their key and length take part in the digest.
 */
export function snapshotRendererUserData(storage: StorageLike, now: () => Date = () => new Date()): RendererUserDataSnapshot {
  const prefixes = [...new Set(USER_DATA_INVENTORY.filter(entry => entry.store === 'renderer-storage' && entry.keyPrefix).map(entry => entry.keyPrefix as string))];
  const counts: Record<string, number> = Object.fromEntries(prefixes.map(prefix => [prefix, 0]));
  const keys: string[] = [];
  for (let index = 0; index < storage.length; index += 1) {
    const key = storage.key(index);
    if (key === null || !key.startsWith('chirality.')) continue;
    keys.push(key);
    for (const prefix of prefixes) if (key.startsWith(prefix)) counts[prefix] += 1;
  }
  keys.sort();
  const digest = keys.map(key => `${key}=${storage.getItem(key)?.length ?? 0}`).join('\n');
  return { takenAt: now().toISOString(), counts, digest };
}

/** True when the two snapshots describe the same renderer-storage contents. */
export function rendererUserDataPreserved(before: RendererUserDataSnapshot, after: RendererUserDataSnapshot): boolean {
  return before.digest === after.digest;
}

/**
 * The update path in one accurate sentence for each state of the download:
 * nothing is installed until the user does it, and quitting to install stops
 * any work still running in Chirality's runtime.
 */
export const UPDATE_PATH_DESCRIPTION = 'Download opens the installer in your browser. Chirality does not install updates: quit Chirality, install the downloaded build, then reopen it.';
export const UPDATE_PRESERVATION_NOTE = 'Your chats, drafts, per-chat folders and settings, saved workflows, preferences and sign-in are stored outside the application and are kept.';
export const UPDATE_RUNNING_WORK_NOTE = 'Work is running in this window. Quitting Chirality to install stops it; let it finish or stop it first.';
