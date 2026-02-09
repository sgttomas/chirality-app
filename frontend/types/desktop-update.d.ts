export type DesktopUpdateCheckResult = {
  ok: boolean;
  currentVersion: string;
  latestVersion: string | null;
  latestTag: string | null;
  updateAvailable: boolean;
  downloadUrl: string;
  publishedAt: string | null;
  error?: string;
};

export type DesktopOpenDownloadResult = {
  ok: boolean;
  error?: string;
};

declare global {
  interface Window {
    chiralityDesktop?: {
      checkForUpdates: () => Promise<DesktopUpdateCheckResult>;
      openDownloadPage: (url?: string) => Promise<DesktopOpenDownloadResult>;
    };
  }
}

export {};
