type DirectorySelectionResult = {
  cancelled: boolean;
  path?: string;
  error?: string;
};

type AttachmentSelectionResult =
  | { cancelled: true; error?: string }
  | { cancelled: false; paths: string[] };

type RuntimeConnectivitySnapshotPayload = {
  state: 'connecting' | 'connected' | 'disconnected';
  failedAttempts: number;
  lastError: string | null;
  changedAt: string;
};

/**
 * `runtime.service.restart()` result, as `electron/runtime-control-ipc-contract.ts`
 * defines it: the service child's state after the relaunch settled, or the
 * redacted reason the main process refused or failed.
 */
type RuntimeServiceStatePayload = {
  status: 'idle' | 'starting' | 'ready' | 'restarting' | 'stopping' | 'stopped' | 'failed';
  pid: number | null;
  socketPath: string;
  clientTokenFile: string;
  restarts: number;
  recentFailures: number;
  lastExit: { code: number | null; signal: string | null; at: string } | null;
  lastError: string | null;
  nextRestartAt: string | null;
  changedAt: string;
};

type RuntimeServiceControlResultPayload =
  | { ok: true; service: RuntimeServiceStatePayload }
  | { ok: false; error: string };

/**
 * `appUpdate` state as `electron/app-update-ipc-contract.ts` defines it.
 * Checking and access to the download only; nothing downloads or installs.
 */
type AppUpdateStatePayload = {
  currentVersion: string;
  status: 'idle' | 'checking' | 'up-to-date' | 'update-available' | 'failed';
  checkedAt?: string;
  failure?: { code: 'no-release-source' | 'policy' | 'network' | 'invalid-feed'; message: string };
  available?: { version: string; downloadUrl: string; releaseNotesUrl?: string; publishedAt?: string };
  releaseSource: { configured: boolean; description: string };
};

type ChiralityBridge = {
  platform?: string;
  versions?: {
    chrome: string;
    electron: string;
    node: string;
  };
  selectDirectory?: () => Promise<DirectorySelectionResult>;
  /**
   * Native attachment picker rooted at a project folder. Returns canonical
   * absolute paths inside that folder with supported extensions only.
   */
  plans?: {
    chooseExportTarget: (request: { projectRoot: string; revision: number }) => Promise<{ cancelled: true; error?: string } | { cancelled: false; targetRelativePath: string }>;
    confirmOverwrite: (request: { projectRoot: string; targetRelativePath: string }) => Promise<boolean>;
  };
  attachments?: {
    selectFiles: (request: { projectRoot: string }) => Promise<AttachmentSelectionResult>;
  };
  /**
   * Partial by design. `apiKey`/`providerApiKey` remain narrowed locally by
   * their own consumers. Connectivity is declared because renderer clients
   * consume it directly. The retired `runtime.daemon`, `runtime.models` and
   * `runtime.hostedAccount` bridges are gone (D-GOV-43, A2); the preload now
   * exposes `runtime.service.restart()` for the retry after the App-owned
   * Runtime service gave up.
   */
  runtime?: {
    connectivity?: {
      get: () => Promise<RuntimeConnectivitySnapshotPayload | null>;
      subscribe: (
        listener: (snapshot: RuntimeConnectivitySnapshotPayload) => void
      ) => () => void;
    };
    service?: {
      /** Operator retry after the main process gave up restarting the service. */
      restart: () => Promise<RuntimeServiceControlResultPayload>;
    };
  };
  appUpdate?: {
    get: () => Promise<AppUpdateStatePayload>;
    check: () => Promise<AppUpdateStatePayload>;
    openDownload: () => Promise<{ ok: boolean; error?: string }>;
    subscribe: (listener: (state: AppUpdateStatePayload) => void) => () => void;
    onShowAbout: (listener: () => void) => () => void;
  };
  instructions?: {
    get: () => Promise<import('../../electron/product-instructions-ipc-contract').ProductInstructionsResult>;
    open: () => Promise<import('../../electron/product-instructions-ipc-contract').ProductInstructionsResult>;
    restore: () => Promise<import('../../electron/product-instructions-ipc-contract').ProductInstructionsResult>;
  };
};

declare global {
  interface Window {
    chirality?: ChiralityBridge;
  }
}

export {};
