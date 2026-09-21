import { PLAN_EXPORT_DIALOG_CHANNEL, type PlanExportTargetResult } from './plan-export-ipc-contract';
import { contextBridge, ipcRenderer, webUtils } from 'electron';
import {
  RUNTIME_CONNECTIVITY_CHANGED_CHANNEL,
  RUNTIME_CONNECTIVITY_QUERY_CHANNEL,
  type RuntimeConnectivitySnapshot
} from './runtime-connectivity';
import { RUNTIME_SERVICE_RESTART_CHANNEL } from './runtime-control-ipc-contract';
import { PRODUCT_INSTRUCTIONS_CHANNEL, type ProductInstructionsResult } from './product-instructions-ipc-contract';
import {
  APP_ABOUT_SHOW_CHANNEL,
  APP_UPDATE_CHANGED_CHANNEL,
  APP_UPDATE_CHECK_CHANNEL,
  APP_UPDATE_GET_CHANNEL,
  APP_UPDATE_OPEN_DOWNLOAD_CHANNEL,
  type AppUpdateOpenDownloadResult,
  type AppUpdateState
} from './app-update-ipc-contract';
import {
  ATTACHMENT_SELECT_FILES_CHANNEL,
  type AttachmentSelectFilesRequest,
  type AttachmentSelectFilesResult
} from './attachment-ipc-contract';

const SELECT_DIRECTORY_CHANNEL = 'chirality:select-directory';
const API_KEY_STORE_CHANNEL = 'chirality:api-key-store';
const API_KEY_REMOVE_CHANNEL = 'chirality:api-key-remove';
const API_KEY_STATUS_CHANNEL = 'chirality:api-key-status';
const PROVIDER_API_KEY_STORE_CHANNEL = 'chirality:provider-api-key-store';
const PROVIDER_API_KEY_REMOVE_CHANNEL = 'chirality:provider-api-key-remove';
const PROVIDER_API_KEY_STATUS_CHANNEL = 'chirality:provider-api-key-status';

contextBridge.exposeInMainWorld('chirality', {
  platform: process.platform,
  versions: {
    chrome: process.versions.chrome,
    electron: process.versions.electron,
    node: process.versions.node
  },
  selectDirectory: () => ipcRenderer.invoke(SELECT_DIRECTORY_CHANNEL),
  instructions: {
    get: (): Promise<ProductInstructionsResult> => ipcRenderer.invoke(PRODUCT_INSTRUCTIONS_CHANNEL, 'get'),
    open: (): Promise<ProductInstructionsResult> => ipcRenderer.invoke(PRODUCT_INSTRUCTIONS_CHANNEL, 'open'),
    restore: (): Promise<ProductInstructionsResult> => ipcRenderer.invoke(PRODUCT_INSTRUCTIONS_CHANNEL, 'restore')
  },
  folders: {
    registerRecent: (path: string) => ipcRenderer.invoke('chirality:folder-register-recent', path),
    pathForFile: (file: File): string => {
      try { return webUtils.getPathForFile(file); } catch { return ''; }
    },
    subscribeOpen: (listener: (intent: { path?: string; error?: string }) => void): (() => void) => {
      let active = true;
      const handler = (_event: unknown, intent: { path?: string; error?: string }) => { if (active) listener(intent); };
      ipcRenderer.on('chirality:folder-open-intent', handler);
      void ipcRenderer.invoke('chirality:folder-open-ready').catch(() => { if (active) listener({ error: 'Folder intent delivery is unavailable.' }); });
      return () => { active = false; ipcRenderer.removeListener('chirality:folder-open-intent', handler); };
    }
  },
  plans: {
    chooseExportTarget: (request: { projectRoot: string; revision: number }): Promise<PlanExportTargetResult> =>
      ipcRenderer.invoke(PLAN_EXPORT_DIALOG_CHANNEL, { operation: 'choose', projectRoot: request.projectRoot, revision: request.revision }),
    confirmOverwrite: async (request: { projectRoot: string; targetRelativePath: string }): Promise<boolean> =>
      (await ipcRenderer.invoke(PLAN_EXPORT_DIALOG_CHANNEL, { operation: 'confirm-overwrite', projectRoot: request.projectRoot, targetRelativePath: request.targetRelativePath })) === true
  },
  attachments: {
    /**
     * Native multi-file picker rooted at the project. Only contained copies of explicitly selected
     * supported files come back;
     * any other selection cancels the whole request with a reason.
     */
    selectFiles: (request: AttachmentSelectFilesRequest): Promise<AttachmentSelectFilesResult> =>
      ipcRenderer.invoke(ATTACHMENT_SELECT_FILES_CHANNEL, { projectRoot: request.projectRoot })
  },
  document: {
    // Desktop retains the frame-denying renderer policy, so inline PDF preview
    // remains unavailable for the MVP fallback.
    inlinePdfPreview: false,
    handoff: (request: { projectRoot: string; target: string; action: 'quick-look' | 'open' | 'reveal' } | { projectRoot: string; action: 'reveal-root' }) =>
      ipcRenderer.invoke('chirality:document-handoff', request)
  },
  apiKey: {
    store: (key: string) => ipcRenderer.invoke(API_KEY_STORE_CHANNEL, key),
    remove: () => ipcRenderer.invoke(API_KEY_REMOVE_CHANNEL),
    status: () => ipcRenderer.invoke(API_KEY_STATUS_CHANNEL)
  },
  providerApiKey: {
    store: (providerId: 'anthropic' | 'omlx', key: string) =>
      ipcRenderer.invoke(PROVIDER_API_KEY_STORE_CHANNEL, providerId, key),
    remove: (providerId: 'anthropic' | 'omlx') =>
      ipcRenderer.invoke(PROVIDER_API_KEY_REMOVE_CHANNEL, providerId),
    status: (providerId: 'anthropic' | 'omlx') =>
      ipcRenderer.invoke(PROVIDER_API_KEY_STATUS_CHANNEL, providerId)
  },
  runtime: {
    /**
     * Runtime connectivity as the main process sees it, including the state of
     * the App-owned Runtime service child under `service`. `get()` is for
     * mount-time hydration; `subscribe()` receives every later transition so the
     * top bar reflects a service that dies or returns without the renderer
     * polling. The unsubscribe function must be called on unmount: the listener
     * is held by `ipcRenderer`, which outlives any React tree.
     */
    connectivity: {
      get: (): Promise<RuntimeConnectivitySnapshot | null> =>
        ipcRenderer.invoke(RUNTIME_CONNECTIVITY_QUERY_CHANNEL),
      subscribe: (listener: (snapshot: RuntimeConnectivitySnapshot) => void): (() => void) => {
        const handler = (_event: unknown, snapshot: RuntimeConnectivitySnapshot): void => {
          listener(snapshot);
        };
        ipcRenderer.on(RUNTIME_CONNECTIVITY_CHANGED_CHANNEL, handler);
        return () => {
          ipcRenderer.removeListener(RUNTIME_CONNECTIVITY_CHANGED_CHANNEL, handler);
        };
      }
    },
    service: {
      /**
       * Operator retry after the main process gave up restarting the Runtime
       * service. Resolves with the service state once the relaunch settled.
       */
      restart: () => ipcRenderer.invoke(RUNTIME_SERVICE_RESTART_CHANNEL)
    }
  },
  /**
   * App-update checking as the main process owns it: `get()` hydrates on mount,
   * `check()` runs (or joins) a check and resolves with the settled state,
   * `openDownload()` hands the reported https download to the system browser,
   * `subscribe()` receives every later transition, and `onShowAbout()` fires
   * when the application menu asks for the About dialog. Unsubscribe on
   * unmount: the listeners are held by `ipcRenderer`, which outlives any React
   * tree. Nothing here downloads, installs or restarts.
   */
  appUpdate: {
    get: (): Promise<AppUpdateState> => ipcRenderer.invoke(APP_UPDATE_GET_CHANNEL),
    check: (): Promise<AppUpdateState> => ipcRenderer.invoke(APP_UPDATE_CHECK_CHANNEL),
    openDownload: (): Promise<AppUpdateOpenDownloadResult> =>
      ipcRenderer.invoke(APP_UPDATE_OPEN_DOWNLOAD_CHANNEL),
    subscribe: (listener: (state: AppUpdateState) => void): (() => void) => {
      const handler = (_event: unknown, state: AppUpdateState): void => {
        listener(state);
      };
      ipcRenderer.on(APP_UPDATE_CHANGED_CHANNEL, handler);
      return () => {
        ipcRenderer.removeListener(APP_UPDATE_CHANGED_CHANNEL, handler);
      };
    },
    onShowAbout: (listener: () => void): (() => void) => {
      const handler = (): void => {
        listener();
      };
      ipcRenderer.on(APP_ABOUT_SHOW_CHANNEL, handler);
      return () => {
        ipcRenderer.removeListener(APP_ABOUT_SHOW_CHANNEL, handler);
      };
    }
  }
});
