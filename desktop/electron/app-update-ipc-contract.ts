/**
 * Renderer-facing app-update contract, shared by the main-process controller
 * and the preload bridge without pulling `ipcMain` into the preload.
 *
 * Checking and access to the download only: nothing here downloads, installs
 * or restarts. The renderer's account menu and About dialog read one state
 * object, ask for a check, and may open the published download in the system
 * browser when a newer version is reported.
 */

export const APP_UPDATE_GET_CHANNEL = 'chirality:app-update-get';
export const APP_UPDATE_CHECK_CHANNEL = 'chirality:app-update-check';
export const APP_UPDATE_OPEN_DOWNLOAD_CHANNEL = 'chirality:app-update-open-download';
export const APP_UPDATE_CHANGED_CHANNEL = 'chirality:app-update-changed';
export const APP_ABOUT_SHOW_CHANNEL = 'chirality:app-about-show';

export type AppUpdateFailureCode = 'no-release-source' | 'policy' | 'network' | 'invalid-feed';

export type AppUpdateStatus = 'idle' | 'checking' | 'up-to-date' | 'update-available' | 'failed';

export type AppUpdateAvailable = {
  version: string;
  downloadUrl: string;
  releaseNotesUrl?: string;
  publishedAt?: string;
};

export type AppUpdateFailure = { code: AppUpdateFailureCode; message: string };

export type AppUpdateState = {
  /** `app.getVersion()` in the main process. */
  currentVersion: string;
  status: AppUpdateStatus;
  /** ISO timestamp, set after any completed check. */
  checkedAt?: string;
  failure?: AppUpdateFailure;
  available?: AppUpdateAvailable;
  /** `description` is user-facing, e.g. 'No release source is configured for this build.' */
  releaseSource: { configured: boolean; description: string };
};

export type AppUpdateOpenDownloadResult = { ok: boolean; error?: string };
