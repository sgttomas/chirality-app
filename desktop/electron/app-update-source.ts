export type AppUpdateSource = {
  /** Exact public GitHub latest-release API endpoint. */
  feedUrl: string;
  /** User-facing description of where checks go. */
  description: string;
};

/** Owner-authorized public release source; no authentication is sent. */
export const APP_UPDATE_FEED_URL = 'https://api.github.com/repos/sgttomas/chirality-app/releases/latest';
export const APP_UPDATE_RELEASE_ROOT = 'https://github.com/sgttomas/chirality-app/releases';
export const APP_UPDATE_ALLOWED_FEED_HOSTS: readonly string[] = ['api.github.com'];

export const UNCONFIGURED_RELEASE_SOURCE_DESCRIPTION =
  'No release source is configured for this build.';

/** The release source for this build, or `null` when none is configured. */
export function resolveAppUpdateSource(): AppUpdateSource | null {
  return { feedUrl: APP_UPDATE_FEED_URL, description: 'Public GitHub releases: sgttomas/chirality-app' };
}

/** User-facing summary of the source for the renderer state object. */
export function describeAppUpdateSource(
  source: AppUpdateSource | null
): { configured: boolean; description: string } {
  return source
    ? { configured: true, description: source.description }
    : { configured: false, description: UNCONFIGURED_RELEASE_SOURCE_DESCRIPTION };
}

export function isAllowlistedFeedHost(
  hostname: string,
  allowedHosts: readonly string[] = APP_UPDATE_ALLOWED_FEED_HOSTS
): boolean {
  const normalized = hostname.trim().toLowerCase();
  return normalized.length > 0 && allowedHosts.some((host) => host.toLowerCase() === normalized);
}
